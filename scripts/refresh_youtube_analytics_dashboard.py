#!/usr/bin/env python3
"""Run the read-only YouTube analytics dashboard refresh in dependency order."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_PAYLOAD_PATH = REPO_ROOT / "experiments" / "youtube-analytics" / "dashboard" / "dashboard_payload.json"
SNAPSHOT_DIR = REPO_ROOT / "experiments" / "youtube-analytics" / "snapshots"


def run_step(args: list[str]) -> None:
    print("+ " + " ".join(args))
    subprocess.run(args, cwd=REPO_ROOT, check=True)


def save_compact_snapshot(payload_path: Path = DASHBOARD_PAYLOAD_PATH, snapshot_dir: Path = SNAPSHOT_DIR) -> Path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from build_youtube_analytics_dashboard import compact_snapshot_payload  # noqa: PLC0415

    payload = json.loads(payload_path.read_text())
    compact = compact_snapshot_payload(payload)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    snapshot_path = snapshot_dir / f"{stamp}.json"
    snapshot_text = json.dumps(compact, indent=2, sort_keys=False) + "\n"
    snapshot_path.write_text(snapshot_text)
    (snapshot_dir / "latest.json").write_text(snapshot_text)
    return snapshot_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since-days", type=int, default=30)
    parser.add_argument("--report-date", default=None)
    parser.add_argument(
        "--skip-reporting-download",
        action="store_true",
        help="Use already downloaded Reporting API CSVs instead of downloading latest reports.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    python = sys.executable

    run_step(
        [
            python,
            "scripts/fetch_youtube_analytics.py",
            "--scope",
            "all-channel",
            "--since-days",
            str(args.since_days),
        ]
    )
    reporting_cmd = [
        python,
        "scripts/sync_youtube_reporting_reports.py",
        "--since-days",
        str(args.since_days),
    ]
    if args.skip_reporting_download:
        reporting_cmd.append("--no-download")
    run_step(reporting_cmd)
    run_step(
        [
            python,
            "scripts/analyze_youtube_srt_content.py",
            "--ledger",
            "experiments/youtube-analytics/metrics_ledger.json",
            "--output",
            "experiments/youtube-analytics/content_rubric.json",
        ]
    )
    report_cmd = [python, "scripts/build_youtube_decision_report.py"]
    if args.report_date:
        report_cmd.extend(["--report-date", args.report_date])
    run_step(report_cmd)
    run_step([python, "scripts/build_youtube_analytics_dashboard.py"])
    snapshot_path = save_compact_snapshot()
    print(f"Wrote dashboard snapshot: {snapshot_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
