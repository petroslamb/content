import csv
import json
import re
from pathlib import Path
from typing import Dict, List

from fetch_and_convert_papers import PAPERS_ROOT, ensure_papers_for_ids, load_missing_ids


def extract_param_counts_from_text(text: str) -> List[float]:
    """
    Extract parameter counts from text, normalized to billions.

    Heuristic: look for patterns like '175B-parameter', '110M parameters',
    '340 million parameters', etc. Ignores numbers not tied to 'parameter'.
    """
    pattern = re.compile(
        r"([0-9][0-9,]*(?:\.\d+)?)\s*(?:"
        r"(?:B|billion)"
        r"|\s*[-–]?\s*B"
        r"|\s*[-–]?\s*billion"
        r"|\s*(?:M|million)"
        r"|\s*[-–]?\s*M"
        r"|\s*[-–]?\s*million"
        r")"
        r"[^\n]{0,40}?"
        r"parameters?",
        re.IGNORECASE,
    )

    results: List[float] = []
    for m in pattern.finditer(text):
        full = m.group(0)
        num_str = m.group(1).replace(",", "")
        unit_match = re.search(r"(B|billion|M|million)", full, re.IGNORECASE)
        if not unit_match:
            continue
        unit = unit_match.group(1).lower()
        try:
            val = float(num_str)
        except ValueError:
            continue
        if unit in ("b", "billion"):
            results.append(val)
        elif unit in ("m", "million"):
            results.append(val / 1000.0)

    # Deduplicate and sort, rounded to 3 decimals for stability.
    unique = sorted({round(v, 3) for v in results})
    return unique


def safe_stem_from_title(title: str, idx: int) -> str:
    stem = re.sub(r"[^a-zA-Z0-9]+", "_", title)[:80].strip("_")
    return stem or f"paper_{idx}"


def collect_param_snippets_for_ids() -> Dict[str, List[Dict[str, List]]]:
    """
    Return a mapping:
      ID -> list of {
         "file": markdown filename,
         "line": 1-based line number of the match,
         "params": [floats_in_billions],
         "snippet": small window of surrounding lines
      }

    This does NOT modify the CSV; it is a discovery/debug tool that surfaces
    candidate parameter mentions so the agent can manually verify which belong
    to the target architecture (vs. baselines) before any dataset updates.
    """
    missing_ids = load_missing_ids()
    id_to_papers = ensure_papers_for_ids(missing_ids)

    results: Dict[str, List[Dict[str, List]]] = {}

    for id_, papers in id_to_papers.items():
        for idx, p in enumerate(papers, start=1):
            stem = safe_stem_from_title(p.title, idx)
            md_path = PAPERS_ROOT / id_ / "markdown" / f"{stem}.md"
            if not md_path.exists():
                continue
            text = md_path.read_text(encoding="utf-8", errors="ignore")
            lines = text.splitlines()
            for i, line in enumerate(lines):
                # Look for any parameter-like phrase on this line.
                window = "\n".join(lines[max(0, i - 2) : min(len(lines), i + 3)])
                params = extract_param_counts_from_text(window)
                if not params:
                    continue
                snippet = {
                    "file": md_path.name,
                    "line": i + 1,
                    "params": sorted({round(v, 3) for v in params}),
                    "snippet": window,
                }
                results.setdefault(id_, []).append(snippet)

    return results


def parse_list_field(raw: str) -> List[str]:
    raw = (raw or "").strip()
    if not raw or raw == "[]":
        return []
    try:
        val = json.loads(raw)
        if isinstance(val, list):
            return [str(x) for x in val]
    except Exception:
        pass
    return []


def main() -> None:
    """
    Discovery-mode CLI:

    - Finds IDs with missing weights (via load_missing_ids()).
    - Scans their markdown files for parameter-like phrases.
    - Prints, for each match:
        * ID
        * markdown filename
        * line number
        * candidate parameter values (in billions)
        * a small snippet of surrounding lines

    This script NO LONGER writes back to scored_architectures.csv. The agent
    is expected to read these snippets, decide which counts truly correspond
    to the target model, and then update the CSV via a separate, explicit step.
    """
    id_to_snippets = collect_param_snippets_for_ids()
    if not id_to_snippets:
        print("No parameter-like snippets found in markdowns.")
        return

    print(f"Found parameter-like snippets for {len(id_to_snippets)} IDs:", sorted(id_to_snippets.keys()))
    for id_ in sorted(id_to_snippets.keys()):
        print(f"\n=== ID {id_} ===")
        for entry in id_to_snippets[id_]:
            params_str = ", ".join(str(v) for v in entry["params"]) or "[]"
            print(f"-- {entry['file']} @ line {entry['line']}  params≈[{params_str}]")
            print(entry["snippet"])
            print()


if __name__ == "__main__":  # pragma: no cover
    main()
