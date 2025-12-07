import csv
import json
import re
from pathlib import Path
from typing import Dict, List

from fetch_and_convert_papers import (
    PAPERS_ROOT,
    CSV_PATH,
    ensure_papers_for_ids,
    load_missing_ids,
)


def extract_param_counts_from_text(text: str) -> List[float]:
    """
    Extract parameter counts from text, normalized to billions.

    Heuristic: look for patterns like '175B-parameter', '110M parameters',
    '340 million parameters', etc. Ignores numbers not tied to 'parameter'.
    """
    pattern = re.compile(
        r"(\d+(?:\.\d+)?)\s*(?:"
        r"(?:B|billion)"
        r"|\s*[-–]?\s*B"
        r"|\s*[-–]?\s*billion"
        r"|\s*(?:M|million)"
        r"|\s*[-–]?\s*M"
        r"|\s*[-–]?\s*million"
        r")"
        r"[^\\n]{0,40}?"
        r"parameters?",
        re.IGNORECASE,
    )

    results: List[float] = []
    for m in pattern.finditer(text):
        full = m.group(0)
        num_str = m.group(1)
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


def parse_markdowns_for_ids() -> Dict[str, Dict[str, List]]:
    """
    Returns mapping:
      ID -> {"params": [floats_in_billions], "sources": [arxiv_abs_urls]}
    for IDs that currently have no Param_Billions and for which we can
    find at least one parameter count in the markdown.
    """
    missing_ids = load_missing_ids()
    id_to_papers = ensure_papers_for_ids(missing_ids)

    results: Dict[str, Dict[str, List]] = {}

    for id_, papers in id_to_papers.items():
        all_params: List[float] = []
        all_sources: List[str] = []

        for idx, p in enumerate(papers, start=1):
            stem = safe_stem_from_title(p.title, idx)
            md_path = PAPERS_ROOT / id_ / "markdown" / f"{stem}.md"
            if not md_path.exists():
                continue
            text = md_path.read_text(encoding="utf-8", errors="ignore")
            params = extract_param_counts_from_text(text)
            if params:
                all_params.extend(params)
                if p.arxiv_id:
                    all_sources.append(f"https://arxiv.org/abs/{p.arxiv_id}")

        if not all_params:
            continue

        params_unique = sorted({round(v, 3) for v in all_params})
        sources_unique = sorted(set(all_sources))

        results[id_] = {
            "params": params_unique,
            "sources": sources_unique,
        }

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
    id_to_info = parse_markdowns_for_ids()
    if not id_to_info:
        print("No parameter counts found in markdowns.")
        return

    print(f"Found parameter counts for {len(id_to_info)} IDs:", sorted(id_to_info.keys()))

    with CSV_PATH.open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    updated = 0
    for row in rows:
        id_ = row["ID"]
        info = id_to_info.get(id_)
        if not info:
            continue
        if row["Param_Billions"].strip() != "[]":
            continue  # do not override existing weights

        params = info["params"]
        sources = info["sources"]

        row["Param_Billions"] = json.dumps(params)

        existing_urls = parse_list_field(row.get("Model_Locations", ""))
        merged = sorted(set(existing_urls + sources))
        row["Model_Locations"] = json.dumps(merged)
        updated += 1

    if not updated:
        print("No CSV rows updated (no matching IDs with empty Param_Billions).")
        return

    with CSV_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated {updated} rows in {CSV_PATH}.")


if __name__ == "__main__":  # pragma: no cover
    main()

