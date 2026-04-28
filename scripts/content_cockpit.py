#!/usr/bin/env python3
"""Read-only local cockpit over Phase 2 content-agent readers."""

from __future__ import annotations

import argparse
import html
import json
import mimetypes
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

import content_agent


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_ARTIFACT_MAX_BYTES = 2_000_000
MAX_RECENT_LIMIT = 50
TEXT_MIME_TYPES = {
    "application/json",
    "application/x-yaml",
    "application/yaml",
    "text/markdown",
}
TEXT_SUFFIXES = {
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}
VALID_GATE_DECISIONS = {"approve", "reject", "defer"}
MAX_ACTION_BODY_BYTES = 64_000


@dataclass(frozen=True)
class CockpitConfig:
    host: str
    port: int
    package_arg: str | None
    limit: int
    artifact_max_bytes: int


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clamp_limit(value: str | None, default: int) -> int:
    if not value:
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return max(1, min(parsed, MAX_RECENT_LIMIT))


def first_query_value(query: dict[str, list[str]], key: str) -> str | None:
    values = query.get(key)
    if not values:
        return None
    value = values[0].strip()
    return value or None


def cockpit_status_payload(package_arg: str | None, limit: int) -> dict[str, object]:
    return {
        "kind": "content_cockpit_status",
        "schema_version": 1,
        "generated_at": utc_now(),
        "readers": [
            "content_agent.build_status_report",
        ],
        "status": content_agent.build_status_report(package_arg=package_arg, limit=limit),
    }


def cockpit_gate_list_payload(package_arg: str | None, status_filter: str) -> dict[str, object]:
    return {
        "kind": "content_cockpit_gate_list",
        "schema_version": 1,
        "generated_at": utc_now(),
        "readers": [
            "content_agent.build_review_list_report",
        ],
        "review_gates": content_agent.build_review_list_report(
            package_arg=package_arg,
            status_filter=status_filter,
        ),
    }


def cockpit_gate_payload(identifier: str) -> dict[str, object]:
    return {
        "kind": "content_cockpit_gate",
        "schema_version": 1,
        "generated_at": utc_now(),
        "readers": [
            "content_agent.build_review_inspect_report",
        ],
        "review_gate": content_agent.build_review_inspect_report(identifier),
    }


def cockpit_next_payload(package_arg: str) -> dict[str, object]:
    return {
        "kind": "content_cockpit_next",
        "schema_version": 1,
        "generated_at": utc_now(),
        "readers": [
            "content_agent.build_next_report",
        ],
        "next": content_agent.build_next_report(package_arg),
    }


def parse_json_bytes(raw: bytes) -> object:
    if not raw.strip():
        return None
    return json.loads(raw.decode("utf-8"))


def run_content_agent(args: list[str]) -> dict[str, object]:
    return run_repo_command([str(content_agent.REPO_ROOT / "content-agent"), *args])


def run_repo_command(command: list[str]) -> dict[str, object]:
    proc = subprocess.run(
        command,
        cwd=content_agent.REPO_ROOT,
        capture_output=True,
        text=True,
    )
    stdout_payload: object | None
    try:
        stdout_payload = json.loads(proc.stdout) if proc.stdout.strip() else None
    except json.JSONDecodeError:
        stdout_payload = proc.stdout
    payload: dict[str, object] = {
        "kind": "content_cockpit_content_agent_command",
        "schema_version": 1,
        "generated_at": utc_now(),
        "command": shlex.join(command),
        "returncode": proc.returncode,
        "success": proc.returncode == 0,
        "stdout": stdout_payload,
    }
    if proc.stderr.strip():
        payload["stderr"] = proc.stderr
    return payload


def editorial_report_action_payload(package_arg: str) -> dict[str, object]:
    if not package_arg.strip():
        raise ValueError("package is required")
    return run_repo_command(
        [
            str(content_agent.REPO_ROOT / ".venv/bin/python"),
            str(content_agent.REPO_ROOT / "scripts/generate_editorial_report.py"),
            "--package",
            package_arg.strip(),
            "--stdout",
        ]
    )


def validation_action_payload(package_arg: str | None) -> dict[str, object]:
    args = ["validate"]
    if package_arg:
        args.extend(["--package", package_arg])
    args.extend(["--format", "json"])
    return run_content_agent(args)


def gate_decision_action_payload(
    gate_identifier: str,
    outcome: str,
    *,
    reason: str,
    decided_by: str,
) -> dict[str, object]:
    if outcome not in VALID_GATE_DECISIONS:
        raise ValueError("decision must be approve, reject, or defer")
    if not reason.strip():
        raise ValueError("decision reason is required")
    args = [
        "review",
        outcome,
        "--gate",
        gate_identifier,
        "--reason",
        reason.strip(),
        "--decided-by",
        decided_by.strip() or "content-cockpit",
        "--format",
        "json",
    ]
    return run_content_agent(args)


def repo_artifact_path(value: str) -> Path:
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = content_agent.REPO_ROOT / candidate
    resolved = candidate.resolve()
    try:
        relpath = resolved.relative_to(content_agent.REPO_ROOT)
    except ValueError as exc:
        raise ValueError("artifact path must stay inside the repository") from exc
    for part in relpath.parts:
        if part.startswith(".") and part != ".github":
            raise ValueError("artifact path cannot reference local hidden files")
    return resolved


def is_text_artifact(path: Path, mime_type: str | None) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES:
        return True
    if mime_type in TEXT_MIME_TYPES:
        return True
    return bool(mime_type and mime_type.startswith("text/"))


def json_bytes(payload: object) -> bytes:
    return json.dumps(payload, indent=2, default=str).encode("utf-8")


def page_shell(title: str, body: str, config: CockpitConfig) -> bytes:
    initial = {
        "package": config.package_arg,
        "limit": config.limit,
    }
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f8fa;
      --surface: #ffffff;
      --line: #d8dde6;
      --muted: #5b6575;
      --text: #18202f;
      --accent: #176b87;
      --warn: #a15c00;
      --bad: #a12626;
      --good: #0f7a4f;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    header {{
      padding: 18px 24px 14px;
      border-bottom: 1px solid var(--line);
      background: var(--surface);
      position: sticky;
      top: 0;
      z-index: 2;
    }}
    h1 {{
      margin: 0 0 12px;
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0;
    }}
    h2 {{
      margin: 0 0 10px;
      font-size: 15px;
      letter-spacing: 0;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    main {{
      width: min(1440px, 100%);
      margin: 0 auto;
      padding: 18px 24px 32px;
    }}
    .toolbar {{
      display: flex;
      align-items: end;
      flex-wrap: wrap;
      gap: 10px;
    }}
    label {{
      display: grid;
      gap: 4px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
    }}
    input, select, button {{
      height: 34px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--text);
      font: inherit;
    }}
    input, select {{ padding: 0 10px; min-width: 180px; }}
    input[type="number"] {{ min-width: 76px; width: 86px; }}
    button {{
      padding: 0 14px;
      background: var(--accent);
      border-color: var(--accent);
      color: white;
      cursor: pointer;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(12, minmax(0, 1fr));
      gap: 14px;
      align-items: start;
    }}
    section {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--surface);
      padding: 14px;
      min-width: 0;
    }}
    .span-12 {{ grid-column: span 12; }}
    .span-8 {{ grid-column: span 8; }}
    .span-6 {{ grid-column: span 6; }}
    .span-4 {{ grid-column: span 4; }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 14px;
    }}
    .metric {{
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px;
      background: #fbfcfd;
    }}
    .metric .label {{ color: var(--muted); font-size: 12px; }}
    .metric .value {{ margin-top: 4px; font-size: 18px; font-weight: 700; overflow-wrap: anywhere; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
    }}
    th, td {{
      padding: 8px 7px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      overflow-wrap: anywhere;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      background: #fbfcfd;
    }}
    code, pre {{
      font: 12px/1.45 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }}
    pre {{
      margin: 0;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 6px;
      overflow: auto;
      background: #fbfcfd;
      max-height: 62vh;
    }}
    .muted {{ color: var(--muted); }}
    .badge {{
      display: inline-block;
      padding: 2px 7px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #f7f8fa;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }}
    .badge.good {{ color: var(--good); border-color: #9ad3bd; background: #effaf5; }}
    .badge.warn {{ color: var(--warn); border-color: #e3bd7a; background: #fff8eb; }}
    .badge.bad {{ color: var(--bad); border-color: #e3a0a0; background: #fff3f3; }}
    .stack {{ display: grid; gap: 14px; }}
    .path-list {{ margin: 0; padding-left: 18px; }}
    .error {{ color: var(--bad); font-weight: 700; }}
    @media (max-width: 900px) {{
      main, header {{ padding-left: 14px; padding-right: 14px; }}
      .grid, .summary {{ display: block; }}
      section, .metric {{ margin-bottom: 12px; }}
      input {{ min-width: 0; width: min(100%, 340px); }}
    }}
  </style>
  <script>window.COCKPIT_INITIAL = {json.dumps(initial)};</script>
</head>
<body>
{body}
</body>
</html>
""".encode("utf-8")


def index_page(config: CockpitConfig) -> bytes:
    body = """
<header>
  <h1>Content Agent Cockpit</h1>
  <div class="toolbar">
    <label>Package
      <input id="package-input" placeholder="optional package key">
    </label>
    <label>Recent limit
      <input id="limit-input" type="number" min="1" max="50">
    </label>
    <button id="refresh-button" type="button">Refresh</button>
    <a id="json-link" href="/api/status" target="_blank">JSON</a>
  </div>
</header>
<main>
  <div id="action-output" class="stack"></div>
  <div id="status" class="stack"></div>
</main>
<script>
const initial = window.COCKPIT_INITIAL || {};
const params = new URLSearchParams(window.location.search);
const packageInput = document.getElementById("package-input");
const limitInput = document.getElementById("limit-input");
packageInput.value = params.get("package") || initial.package || "";
limitInput.value = params.get("limit") || initial.limit || 5;
document.getElementById("refresh-button").addEventListener("click", loadStatus);
packageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") loadStatus();
});
const validateButton = document.createElement("button");
validateButton.id = "validate-button";
validateButton.type = "button";
validateButton.textContent = "Rerun Validation";
validateButton.addEventListener("click", rerunValidation);
document.querySelector(".toolbar").appendChild(validateButton);
const editorialReportButton = document.createElement("button");
editorialReportButton.id = "editorial-report-button";
editorialReportButton.type = "button";
editorialReportButton.textContent = "Editorial Report";
editorialReportButton.addEventListener("click", runEditorialReport);
document.querySelector(".toolbar").appendChild(editorialReportButton);

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[char]));
}

function badge(value) {
  const raw = String(value ?? "unknown");
  let cls = "badge";
  if (["passed", "completed", "resolved", "true"].includes(raw)) cls += " good";
  if (["pending", "warning", "deferred", "gated"].includes(raw)) cls += " warn";
  if (["failed", "error", "invalid", "rejected", "false"].includes(raw)) cls += " bad";
  return `<span class="${cls}">${esc(raw)}</span>`;
}

function artifact(path, label) {
  if (!path) return '<span class="muted">none</span>';
  return `<a href="/artifact?path=${encodeURIComponent(path)}" target="_blank">${esc(label || path)}</a>`;
}

function gateHref(gate) {
  const id = gate.gate_id || gate.path;
  return `/gate?gate=${encodeURIComponent(id)}`;
}

function setJsonLink(query) {
  document.getElementById("json-link").href = `/api/status?${query.toString()}`;
}

async function loadStatus() {
  const query = new URLSearchParams();
  const packageValue = packageInput.value.trim();
  const limitValue = limitInput.value.trim();
  if (packageValue) query.set("package", packageValue);
  if (limitValue) query.set("limit", limitValue);
  setJsonLink(query);
  document.getElementById("status").innerHTML = '<section class="span-12">Loading...</section>';
  const response = await fetch(`/api/status?${query.toString()}`);
  const payload = await response.json();
  if (!response.ok) {
    document.getElementById("status").innerHTML = `<section><div class="error">${esc(payload.error || response.statusText)}</div></section>`;
    return;
  }
  renderStatus(payload);
  await loadNextAction(packageValue || (payload.status?.package?.package || ""));
}

async function rerunValidation() {
  const packageValue = packageInput.value.trim();
  const output = document.getElementById("action-output");
  output.innerHTML = '<section>Running validation...</section>';
  const response = await fetch("/api/validate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({package: packageValue || null})
  });
  const payload = await response.json();
  output.innerHTML = `<section><h2>Validation Rerun</h2><pre>${esc(JSON.stringify(payload, null, 2))}</pre></section>`;
  await loadStatus();
}

async function runEditorialReport() {
  const packageValue = packageInput.value.trim();
  const output = document.getElementById("action-output");
  if (!packageValue) {
    output.innerHTML = '<section><div class="error">Select a package before running the editorial report.</div></section>';
    return;
  }
  output.innerHTML = '<section>Running editorial report...</section>';
  const response = await fetch("/api/editorial-report", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({package: packageValue})
  });
  const payload = await response.json();
  output.innerHTML = renderEditorialReportResult(payload, response.ok);
}

function renderEditorialReportResult(payload, ok) {
  const report = payload.stdout && typeof payload.stdout === "object" ? payload.stdout : null;
  if (!ok || !report || report.kind !== "editorial_automation_report") {
    return `<section><h2>Editorial Report</h2><pre>${esc(JSON.stringify(payload, null, 2))}</pre></section>`;
  }
  const counts = report.severity_counts || {};
  const findings = (report.findings || []).slice(0, 12).map((finding) => `
    <tr>
      <td>${badge(finding.severity || "advisory")}</td>
      <td>${esc(finding.check_id || "")}</td>
      <td>${artifact(finding.path, finding.line ? `${finding.path}:${finding.line}` : finding.path)}</td>
      <td>${esc(finding.message || "")}</td>
    </tr>`).join("");
  const suggestions = renderListItems((report.source_improvement_suggestions || []).map((item) => item.suggestion || item.id));
  return `<section>
    <h2>Editorial Report</h2>
    <table><tbody>
      <tr><th>Package</th><td>${esc(report.package?.key || "")}</td></tr>
      <tr><th>Live draft</th><td>${artifact(report.package?.live_draft_path)}</td></tr>
      <tr><th>Counts</th><td>${esc(counts.error || 0)} errors, ${esc(counts.warning || 0)} warnings, ${esc(counts.advisory || 0)} advisory</td></tr>
      <tr><th>State effects</th><td><code>${esc(JSON.stringify(report.state_effects || {}))}</code></td></tr>
    </tbody></table>
    <h2 style="margin-top:14px">Findings</h2>
    <table>
      <thead><tr><th>Severity</th><th>Check</th><th>Path</th><th>Message</th></tr></thead>
      <tbody>${findings || '<tr><td colspan="4" class="muted">No findings.</td></tr>'}</tbody>
    </table>
    <h2 style="margin-top:14px">Source Improvement Suggestions</h2>
    <ul class="path-list">${suggestions || '<li class="muted">none</li>'}</ul>
    <details style="margin-top:14px"><summary>Raw report</summary><pre>${esc(JSON.stringify(report, null, 2))}</pre></details>
  </section>`;
}

function renderStatus(payload) {
  const report = payload.status || {};
  const gates = report.review_gates || {};
  const runs = report.recent_runs || {};
  const health = report.validation_health || {};
  const root = report.root_surfaces || {};
  const yamlRuns = runs.yaml_run_records || [];
  const legacyRuns = runs.legacy_json_logs || [];
  const summary = `
    <div class="summary">
      <div class="metric"><div class="label">Validation</div><div class="value">${badge(String(health.success === true))}</div></div>
      <div class="metric"><div class="label">Pending Gates</div><div class="value">${esc(gates.pending_count || 0)}</div></div>
      <div class="metric"><div class="label">Recent Runs</div><div class="value">${esc(yamlRuns.length + legacyRuns.length)}</div></div>
      <div class="metric"><div class="label">Workflow Contracts</div><div class="value">${esc(root.workflow_yaml_count || 0)}</div></div>
    </div>`;
  document.getElementById("status").innerHTML = `
    ${summary}
    <div class="grid">
      <section class="span-4">${renderPackage(report.package, root)}</section>
      <section class="span-8">${renderValidation(health)}</section>
      <section class="span-12" id="next-action-section">${renderNextPlaceholder(report.package)}</section>
      <section class="span-12">${renderGates(gates)}</section>
      <section class="span-12">${renderRuns(yamlRuns, legacyRuns)}</section>
    </div>`;
}

function renderNextPlaceholder(pkg) {
  if (!pkg) {
    return '<h2>Next Action</h2><p class="muted">Select a package to resolve the next action.</p>';
  }
  return '<h2>Next Action</h2><p class="muted">Resolving...</p>';
}

async function loadNextAction(packageValue) {
  const section = document.getElementById("next-action-section");
  if (!section || !packageValue) return;
  const response = await fetch(`/api/next?package=${encodeURIComponent(packageValue)}`);
  const payload = await response.json();
  if (!response.ok) {
    section.innerHTML = `<h2>Next Action</h2><div class="error">${esc(payload.error || response.statusText)}</div>`;
    return;
  }
  section.innerHTML = renderNextAction(payload.next || {});
}

function renderListItems(items) {
  return (items || []).map((item) => `<li>${esc(item)}</li>`).join("");
}

function renderGateBlockers(gates) {
  return (gates || []).map((gate) => `
    <tr>
      <td>${badge(gate.status)}</td>
      <td><a href="${gateHref(gate)}">${esc(gate.gate_id || gate.path)}</a></td>
      <td>${esc(gate.workflow_id || "")}</td>
      <td>${esc(gate.stop_reason || "")}</td>
    </tr>`).join("");
}

function renderNextAction(next) {
  const blockers = renderListItems(next.blocking_issues || []);
  const commands = renderListItems(next.suggested_commands || []);
  const gateRows = renderGateBlockers(next.pending_review_gate_blockers || []);
  return `<h2>Next Action</h2>
    <table><tbody>
      <tr><th>Next stage</th><td>${esc(next.next_stage || "none")}</td></tr>
      <tr><th>Effective workflow</th><td>${esc(next.effective_workflow || next.next_stage || "none")}</td></tr>
      <tr><th>Effective action</th><td>${esc(next.effective_next_action || next.next_packet_action || "none")}</td></tr>
      <tr><th>Can execute</th><td>${badge(String(next.can_execute === true || next.effective_can_execute === true))}</td></tr>
      <tr><th>Requires approval</th><td>${badge(String(next.requires_approval === true || next.effective_requires_approval === true))}</td></tr>
      <tr><th>Pipeline profile</th><td>${esc(next.pipeline_profile || "none")}</td></tr>
    </tbody></table>
    <h2 style="margin-top:14px">Blocking Issues</h2>
    <ul class="path-list">${blockers || '<li class="muted">none</li>'}</ul>
    <h2 style="margin-top:14px">Pending Gate Blockers</h2>
    <table>
      <thead><tr><th>Status</th><th>Gate</th><th>Workflow</th><th>Reason</th></tr></thead>
      <tbody>${gateRows || '<tr><td colspan="4" class="muted">No pending gate blockers.</td></tr>'}</tbody>
    </table>
    <h2 style="margin-top:14px">Suggested Commands</h2>
    <ul class="path-list">${commands || '<li class="muted">none</li>'}</ul>`;
}

function renderPackage(pkg, root) {
  if (!pkg) {
    return `<h2>Package State</h2>
      <p class="muted">No package filter selected.</p>
      <table><tbody>
        <tr><th>Gate contracts</th><td>${esc(root.gate_contract_count || 0)}</td></tr>
        <tr><th>Pipeline profiles</th><td>${esc(root.pipeline_profile_count || 0)}</td></tr>
        <tr><th>Policy</th><td>${artifact(root.harness_policy_path || "harness_policy.yaml")}</td></tr>
      </tbody></table>`;
  }
  const stages = (pkg.stages || []).map((stage) => `
    <tr>
      <td>${esc(stage.stage)}</td>
      <td>${badge(String(stage.done === true))}</td>
      <td>${esc(stage.last_updated || "")}</td>
    </tr>`).join("");
  return `<h2>Package State</h2>
    <table><tbody>
      <tr><th>Package</th><td>${esc(pkg.package)}</td></tr>
      <tr><th>Kind</th><td>${esc(pkg.kind)}</td></tr>
      <tr><th>Current stage</th><td>${esc(pkg.current_stage || "none")}</td></tr>
      <tr><th>Umbrella route</th><td>${esc(pkg.umbrella_route || "none")}</td></tr>
      <tr><th>Status file</th><td>${artifact(pkg.status_path)}</td></tr>
    </tbody></table>
    <h2 style="margin-top:14px">Lifecycle Stages</h2>
    <table>
      <thead><tr><th>Stage</th><th>Done</th><th>Updated</th></tr></thead>
      <tbody>${stages || '<tr><td colspan="3" class="muted">No stage records.</td></tr>'}</tbody>
    </table>`;
}

function renderValidation(health) {
  const counts = health.severity_counts || {};
  const findings = (health.top_findings || []).map((finding) => `
    <tr>
      <td>${badge(finding.severity || "info")}</td>
      <td>${esc(finding.surface || "")}</td>
      <td>${artifact(finding.path, finding.path || "")}</td>
      <td>${esc(finding.message || "")}</td>
    </tr>`).join("");
  return `<h2>Validation Health</h2>
    <table><tbody>
      <tr><th>Mode</th><td>${esc(health.mode || "")}</td></tr>
      <tr><th>Findings</th><td>${esc(health.finding_count || 0)} total, ${esc(counts.error || 0)} errors, ${esc(counts.warning || 0)} warnings</td></tr>
      <tr><th>Evidence counts</th><td><code>${esc(JSON.stringify(health.execution_evidence_counts || {}))}</code></td></tr>
    </tbody></table>
    <h2 style="margin-top:14px">Top Findings</h2>
    <table>
      <thead><tr><th>Severity</th><th>Surface</th><th>Path</th><th>Message</th></tr></thead>
      <tbody>${findings || '<tr><td colspan="4" class="muted">No findings.</td></tr>'}</tbody>
    </table>`;
}

function renderGates(gates) {
  const rows = [...(gates.pending || []), ...(gates.resolved || []), ...(gates.invalid || [])].map((gate) => `
    <tr>
      <td>${badge(gate.status)}</td>
      <td><a href="${gateHref(gate)}">${esc(gate.gate_id || gate.path)}</a></td>
      <td>${esc(gate.package_key || gate.package || "")}</td>
      <td>${esc(gate.workflow_id || "")}<br><span class="muted">${esc(gate.step_id || "")}</span></td>
      <td>${esc(gate.gate_type || gate.gate_contract || "")}</td>
      <td>${esc(gate.created_at || gate.decided_at || "")}</td>
      <td>${artifact(gate.path, "artifact")}</td>
    </tr>`).join("");
  return `<h2>Review Gates</h2>
    <table>
      <thead><tr><th>Status</th><th>Gate</th><th>Package</th><th>Workflow</th><th>Class</th><th>Time</th><th>File</th></tr></thead>
      <tbody>${rows || '<tr><td colspan="7" class="muted">No review gates.</td></tr>'}</tbody>
    </table>`;
}

function renderRuns(yamlRuns, legacyRuns) {
  const yamlRows = yamlRuns.map((run) => `
    <tr>
      <td>${badge(run.terminal_status || "recorded")}</td>
      <td>${esc(run.run_id || "")}</td>
      <td>${esc(run.package_key || run.package || "")}</td>
      <td>${esc(run.workflow_id || "")}</td>
      <td>${esc(run.ended_at || run.started_at || "")}</td>
      <td>${artifact(run.path, "artifact")}</td>
    </tr>`).join("");
  const legacyRows = legacyRuns.map((run) => `
    <tr>
      <td>${badge(run.status || run.kind || "recorded")}</td>
      <td>${esc(run.run_id || run.gate_id || "")}</td>
      <td>${esc(run.package_key || run.package || "")}</td>
      <td>${esc(run.workflow || run.stage || "")}</td>
      <td>${esc(run.timestamp || "")}</td>
      <td>${artifact(run.path, "artifact")}</td>
    </tr>`).join("");
  return `<h2>Recent Run Records</h2>
    <table>
      <thead><tr><th>Status</th><th>Run</th><th>Package</th><th>Workflow</th><th>Time</th><th>File</th></tr></thead>
      <tbody>${yamlRows}${legacyRows || ""}${(!yamlRows && !legacyRows) ? '<tr><td colspan="6" class="muted">No recent run records.</td></tr>' : ""}</tbody>
    </table>`;
}

loadStatus();
</script>
"""
    return page_shell("Content Agent Cockpit", body, config)


def gate_page(config: CockpitConfig, gate_identifier: str) -> bytes:
    body = f"""
<header>
  <h1>Review Gate</h1>
  <div class="toolbar">
    <a href="/">Cockpit</a>
    <a id="gate-json-link" href="/api/gate?gate={quote(gate_identifier)}" target="_blank">JSON</a>
  </div>
</header>
<main>
  <div id="decision-output" class="stack"></div>
  <div id="gate" class="stack">Loading...</div>
</main>
<script>
const gateIdentifier = {json.dumps(gate_identifier)};
function esc(value) {{
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({{
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }}[char]));
}}
function badge(value) {{
  const raw = String(value ?? "unknown");
  let cls = "badge";
  if (["passed", "completed", "resolved", "true"].includes(raw)) cls += " good";
  if (["pending", "warning", "deferred", "gated"].includes(raw)) cls += " warn";
  if (["failed", "error", "invalid", "rejected", "false"].includes(raw)) cls += " bad";
  return `<span class="${{cls}}">${{esc(raw)}}</span>`;
}}
function artifact(path, label) {{
  if (!path) return '<span class="muted">none</span>';
  return `<a href="/artifact?path=${{encodeURIComponent(path)}}" target="_blank">${{esc(label || path)}}</a>`;
}}
async function submitDecision(outcome) {{
  const reasonInput = document.getElementById("decision-reason");
  const output = document.getElementById("decision-output");
  const reason = reasonInput ? reasonInput.value.trim() : "";
  if (!reason) {{
    output.innerHTML = '<section><div class="error">Decision reason is required.</div></section>';
    return;
  }}
  output.innerHTML = '<section>Recording decision...</section>';
  const response = await fetch("/api/gate/decision", {{
    method: "POST",
    headers: {{"Content-Type": "application/json"}},
    body: JSON.stringify({{
      gate: gateIdentifier,
      outcome,
      reason,
      decided_by: "content-cockpit"
    }})
  }});
  const payload = await response.json();
  output.innerHTML = `<section><h2>Decision Result</h2><pre>${{esc(JSON.stringify(payload, null, 2))}}</pre></section>`;
  await loadGate();
}}
async function loadGate() {{
  const response = await fetch(`/api/gate?gate=${{encodeURIComponent(gateIdentifier)}}`);
  const payload = await response.json();
  if (!response.ok) {{
    document.getElementById("gate").innerHTML = `<section><div class="error">${{esc(payload.error || response.statusText)}}</div></section>`;
    return;
  }}
  const report = payload.review_gate || {{}};
  const gate = report.gate || {{}};
  const artifactData = report.artifact || {{}};
  const evidence = artifactData.evidence || {{}};
  const showDecisionControls = gate.status === "pending";
  const previewPaths = (evidence.preview_paths || []).map((path) => `<li>${{artifact(path)}}</li>`).join("");
  const evidencePaths = (evidence.evidence_paths || []).map((path) => `<li>${{artifact(path)}}</li>`).join("");
  const decisionControls = showDecisionControls ? `
      <section class="span-12">
        <h2>Gate Decision</h2>
        <label>Reason
          <input id="decision-reason" placeholder="required decision reason">
        </label>
        <div class="toolbar" style="margin-top:10px">
          <button type="button" onclick="submitDecision('approve')">Approve</button>
          <button type="button" onclick="submitDecision('reject')">Reject</button>
          <button type="button" onclick="submitDecision('defer')">Defer</button>
        </div>
      </section>` : "";
  document.getElementById("gate").innerHTML = `
    <div class="grid">
      <section class="span-4">
        <h2>Gate Summary</h2>
        <table><tbody>
          <tr><th>Status</th><td>${{badge(gate.status)}}</td></tr>
          <tr><th>Gate</th><td>${{esc(gate.gate_id || "")}}</td></tr>
          <tr><th>Package</th><td>${{esc(gate.package_key || gate.package || "")}}</td></tr>
          <tr><th>Workflow</th><td>${{esc(gate.workflow_id || "")}}</td></tr>
          <tr><th>Step</th><td>${{esc(gate.step_id || "")}}</td></tr>
          <tr><th>Created</th><td>${{esc(gate.created_at || "")}}</td></tr>
          <tr><th>Artifact</th><td>${{artifact(gate.path)}}</td></tr>
        </tbody></table>
      </section>
      <section class="span-8">
        <h2>Evidence Links</h2>
        <table><tbody>
          <tr><th>Preview</th><td><ul class="path-list">${{previewPaths || '<li class="muted">none</li>'}}</ul></td></tr>
          <tr><th>Evidence</th><td><ul class="path-list">${{evidencePaths || '<li class="muted">none</li>'}}</ul></td></tr>
          <tr><th>Run record</th><td>${{artifact((artifactData.run || {{}}).run_record_path)}}</td></tr>
          <tr><th>Resolved run</th><td>${{artifact((artifactData.run || {{}}).resolved_run_path)}}</td></tr>
        </tbody></table>
      </section>
      <section class="span-12">
        <h2>Exact Gate Artifact</h2>
        <pre>${{esc(JSON.stringify(artifactData, null, 2))}}</pre>
      </section>
      ${{decisionControls}}
    </div>`;
}}
loadGate();
</script>
"""
    return page_shell("Review Gate", body, config)


class CockpitHandler(BaseHTTPRequestHandler):
    config: CockpitConfig

    server_version = "ContentCockpit/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        try:
            if parsed.path in {"/", "/index.html"}:
                self.send_bytes(index_page(self.config), "text/html; charset=utf-8")
                return
            if parsed.path == "/gate":
                gate = first_query_value(query, "gate")
                if not gate:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "missing gate query parameter")
                    return
                self.send_bytes(gate_page(self.config, gate), "text/html; charset=utf-8")
                return
            if parsed.path == "/api/status":
                package_arg = first_query_value(query, "package") or self.config.package_arg
                limit = clamp_limit(first_query_value(query, "limit"), self.config.limit)
                self.send_json(cockpit_status_payload(package_arg, limit))
                return
            if parsed.path == "/api/next":
                package_arg = first_query_value(query, "package") or self.config.package_arg
                if not package_arg:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "package is required")
                    return
                self.send_json(cockpit_next_payload(package_arg))
                return
            if parsed.path == "/api/gates":
                package_arg = first_query_value(query, "package") or self.config.package_arg
                status_filter = first_query_value(query, "status") or "all"
                if status_filter not in {"pending", "resolved", "all"}:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "status must be pending, resolved, or all")
                    return
                self.send_json(cockpit_gate_list_payload(package_arg, status_filter))
                return
            if parsed.path == "/api/gate":
                gate = first_query_value(query, "gate")
                if not gate:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "missing gate query parameter")
                    return
                self.send_json(cockpit_gate_payload(gate))
                return
            if parsed.path == "/artifact":
                path_value = first_query_value(query, "path")
                if not path_value:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "missing path query parameter")
                    return
                self.send_artifact(path_value)
                return
            self.send_json_error(HTTPStatus.NOT_FOUND, "not found")
        except Exception as exc:  # pragma: no cover - server response path
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            body = self.read_json_body()
            if parsed.path == "/api/validate":
                package_arg = body.get("package") if isinstance(body.get("package"), str) else self.config.package_arg
                payload = validation_action_payload(package_arg)
                status = HTTPStatus.OK if payload.get("success") is True else HTTPStatus.BAD_REQUEST
                self.send_json(payload, status)
                return
            if parsed.path == "/api/editorial-report":
                package_arg = body.get("package") if isinstance(body.get("package"), str) else self.config.package_arg
                if not package_arg:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "package is required")
                    return
                payload = editorial_report_action_payload(package_arg)
                status = HTTPStatus.OK if payload.get("success") is True else HTTPStatus.BAD_REQUEST
                self.send_json(payload, status)
                return
            if parsed.path == "/api/gate/decision":
                gate = body.get("gate")
                outcome = body.get("outcome")
                reason = body.get("reason")
                decided_by = body.get("decided_by", "content-cockpit")
                if not isinstance(gate, str) or not gate.strip():
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "gate is required")
                    return
                if not isinstance(outcome, str):
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "outcome is required")
                    return
                if not isinstance(reason, str):
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "reason is required")
                    return
                if not isinstance(decided_by, str):
                    decided_by = "content-cockpit"
                payload = gate_decision_action_payload(
                    gate,
                    outcome,
                    reason=reason,
                    decided_by=decided_by,
                )
                status = HTTPStatus.OK if payload.get("success") is True else HTTPStatus.BAD_REQUEST
                self.send_json(payload, status)
                return
            self.send_json_error(HTTPStatus.NOT_FOUND, "not found")
        except ValueError as exc:
            self.send_json_error(HTTPStatus.BAD_REQUEST, str(exc))
        except Exception as exc:  # pragma: no cover - server response path
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def read_json_body(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        if length > MAX_ACTION_BODY_BYTES:
            raise ValueError("request body is too large")
        raw = self.rfile.read(length)
        payload = parse_json_bytes(raw) if raw else {}
        if payload is None:
            return {}
        if not isinstance(payload, dict):
            raise ValueError("request body must be a JSON object")
        return payload

    def send_json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_bytes(json_bytes(payload), "application/json; charset=utf-8", status)

    def send_json_error(self, status: HTTPStatus, message: str) -> None:
        self.send_json({"success": False, "error": message}, status)

    def send_bytes(
        self,
        body: bytes,
        content_type: str,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        self.send_response(status.value)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_artifact(self, path_value: str) -> None:
        path = repo_artifact_path(path_value)
        if not path.exists():
            self.send_json_error(HTTPStatus.NOT_FOUND, f"artifact not found: {path_value}")
            return
        if path.is_dir():
            entries = [item.relative_to(content_agent.REPO_ROOT).as_posix() for item in sorted(path.iterdir())]
            body = "\n".join(entries).encode("utf-8")
            self.send_bytes(body, "text/plain; charset=utf-8")
            return
        mime_type, _ = mimetypes.guess_type(path.name)
        if is_text_artifact(path, mime_type):
            data = path.read_bytes()
            truncated = len(data) > self.config.artifact_max_bytes
            if truncated:
                data = data[: self.config.artifact_max_bytes]
                data += b"\n\n[content-cockpit truncated this artifact preview]\n"
            self.send_bytes(data, "text/plain; charset=utf-8")
            return
        self.send_bytes(path.read_bytes(), mime_type or "application/octet-stream")

    def log_message(self, format: str, *args: object) -> None:
        sys.stderr.write("content-cockpit: " + (format % args) + "\n")


def build_handler(config: CockpitConfig) -> type[CockpitHandler]:
    class ConfiguredCockpitHandler(CockpitHandler):
        pass

    ConfiguredCockpitHandler.config = config
    return ConfiguredCockpitHandler


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Serve the read-only Phase 2 local cockpit.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host interface to bind. Defaults to localhost.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to bind.")
    parser.add_argument("--package", dest="package_arg", help="Optional default package key/path.")
    parser.add_argument("--limit", type=int, default=content_agent.DEFAULT_RECENT_LIMIT, help="Recent run limit.")
    parser.add_argument(
        "--artifact-max-bytes",
        type=int,
        default=DEFAULT_ARTIFACT_MAX_BYTES,
        help="Maximum bytes to show for text artifact previews.",
    )
    parser.add_argument("--once", action="store_true", help="Print one read-only snapshot instead of serving HTTP.")
    parser.add_argument("--format", choices=["json", "html"], default="json", help="Output format for --once.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = CockpitConfig(
        host=args.host,
        port=args.port,
        package_arg=args.package_arg,
        limit=max(1, min(args.limit, MAX_RECENT_LIMIT)),
        artifact_max_bytes=max(1, args.artifact_max_bytes),
    )
    if args.once:
        if args.format == "html":
            sys.stdout.buffer.write(index_page(config))
            return
        print(json.dumps(cockpit_status_payload(config.package_arg, config.limit), indent=2, default=str))
        return

    server = ThreadingHTTPServer((config.host, config.port), build_handler(config))
    url = f"http://{config.host}:{config.port}/"
    print(f"content-cockpit serving {url}")
    print("press Ctrl-C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\ncontent-cockpit stopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
