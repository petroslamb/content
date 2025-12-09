import argparse
import csv
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

# Re-use logic from fetch_and_convert regarding papers root
from fetch_and_convert_papers import PAPERS_ROOT, ensure_papers_for_ids, load_missing_ids
from utils import setup_logger

logger = setup_logger("inspect_params")

def extract_param_counts_from_text(text: str) -> List[float]:
    """
    Extract parameter counts from text, normalized to billions.

    Heuristic: look for patterns like '175B-parameter', '110M parameters',
    '340 million parameters', etc. Ignores numbers not tied to 'parameter'.
    """
    # 2025-12-09: Updated regex to include negative lookahead for token/data units
    # and broadened suffix acceptance for 'model', 'dense', 'MoE'.
    pattern = re.compile(
        r"([0-9][0-9,]*(?:\.\d+)?)\s*(?:"
        r"(?:B|billion|b)"
        r"|\s*[-–]?\s*(?:B|billion|b)"
        r"|\s*(?:M|million|m)"
        r"|\s*[-–]?\s*(?:M|million|m)"
        r")"
        r"(?![\s-]*?(?:tokens|examples|samples|rows|bytes|words))",  # Negative Lookahead: Exclude if followed by data units
        re.IGNORECASE,
    )

    results: List[float] = []
    
    # We iterate manually to log rejections? 
    # extract_param_counts_from_text is a helper used by explicit line scan.
    # For full debug logging of REJECTIONS, we need to inspect what *would* have matched
    # if not for the lookahead. That's complex with a single regex.
    # Instead, we trust the regex for extraction and log what WAS extracted.
    
    for m in pattern.finditer(text):
        full = m.group(0)
        num_str = m.group(1).replace(",", "")
        unit_match = re.search(r"(B|billion|M|million)", full, re.IGNORECASE)
        # Regex structure guarantees B/M is present but let's be safe
        if not unit_match:
             # This effectively catches cases where the pattern says B/M but our sub-search fails? unlikely.
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


def collect_param_snippets_for_ids(ids: List[str]) -> Dict[str, List[Dict]]:
    """
    Return a mapping:
      ID -> list of { file, line, params, snippet }
    """
    # We assume PDFs/Markdowns are already downloaded via fetch_and_convert_papers
    # But we can try to ensure them if missing? 
    # For inspection tool, we generally assume they exist.
    
    # We still need to know WHICH papers belong to an ID.
    id_to_papers = ensure_papers_for_ids(ids)

    results: Dict[str, List[Dict]] = {}

    for id_, papers in id_to_papers.items():
        # Scan the markdown directory for this ID
        md_dir = PAPERS_ROOT / id_ / "markdown"
        if not md_dir.exists():
            logger.debug(f"No markdown dir for {id_}")
            continue
        
        # We can scan *all* markdowns in the folder, as sometimes names differ slightly
        for md_path in md_dir.glob("*.md"):
            try:
                text = md_path.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                logger.error(f"Failed to read {md_path}: {e}")
                continue
                
            # Robust pass: scan whole text to find offsets
            matches = extract_param_counts_for_file(text, md_path.name)
            if matches:
                 results.setdefault(id_, []).extend(matches)
            else:
                 logger.debug(f"No matches in {md_path.name}")

    return results


def extract_param_counts_for_file(text: str, filename: str) -> List[Dict]:
    # We need to reuse the pattern from extract_param_counts_from_text or keep them in sync.
    # Duplicating here for the "search entire line" logic.
    pattern = re.compile(
        r"([0-9][0-9,]*(?:\.\d+)?)\s*(?:"
        r"(?:B|billion|b)"
        r"|\s*[-–]?\s*(?:B|billion|b)"
        r"|\s*(?:M|million|m)"
        r"|\s*[-–]?\s*(?:M|million|m)"
        r")"
        r"(?![\s-]*?(?:tokens|examples|samples|rows|bytes|words))", 
        re.IGNORECASE,
    )
    
    lines = text.splitlines()
    found = []
    
    # Iterate lines to find context easily
    for i, line in enumerate(lines):
        # We search line-by-line.
        if pattern.search(line):
            # Extract specific counts
            counts = extract_param_counts_from_text(line)
            if not counts:
                # This implies pattern matched but extraction logic (dedupe/float conversion) failed?
                # Or maybe the regex differs slightly.
                logger.debug(f"[{filename}:{i+1}] Regex matched but extraction returned empty. Line: {line[:50]}...")
                continue
            
            # Context
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            snippet_lines = lines[start:end]
            formatted_snippet = []
            for j, sl in enumerate(snippet_lines):
                lineno = start + j + 1
                marker = ">>>" if lineno == (i + 1) else "   "
                formatted_snippet.append(f"{marker} {lineno}: {sl}")

            found.append({
                "file": filename,
                "line": i + 1,
                "params": counts,
                "snippet": "\n".join(formatted_snippet)
            })
    return found


def write_report(results: Dict[str, List[Dict]], report_path: Path):
    from datetime import datetime
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Inspection Report: Candidate Parameters\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for id_ in sorted(results.keys()):
            f.write(f"## ID: {id_}\n")
            snippets = results[id_]
            for entry in snippets:
                params_str = ", ".join(f"{v}B" for v in entry["params"])
                f.write(f"### File: `{entry['file']}`\n")
                f.write(f"**Line:** {entry['line']} | **Candidates:** `{params_str}`\n\n")
                f.write("```text\n")
                f.write(entry["snippet"] + "\n")
                f.write("```\n\n")
                f.write("---\n\n")
    logger.info(f"Report written to {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect markdown files for parameter counts with context.")
    parser.add_argument("--ids", nargs="+", help="Specific IDs to inspect (e.g., A1).")
    parser.add_argument("--report", help="Path to write a markdown report of findings (e.g. candidates.md).")
    args = parser.parse_args()

    logger.info(f"=== STARTED inspect_params | Command: {' '.join(sys.argv)} ===")
    logger.debug(f"Parsed Args: {args}")

    # Pass args to load_missing_ids to handle whitelist logic
    ids_to_process = load_missing_ids(only_ids=args.ids, include_analyzed=True)
    
    if not ids_to_process:
        logger.info("No IDs found to process.")
        return

    logger.info(f"Inspecting Markdowns for {len(ids_to_process)} IDs...")
    
    results = collect_param_snippets_for_ids(ids_to_process)
    
    if not results:
        logger.info(f"No parameter patterns found in markdowns for these IDs.")
        return

    # Console Output
    for id_ in sorted(results.keys()):
        print(f"\n=== ID {id_} ===")
        snippets = results[id_]
        for entry in snippets:
            params_str = ", ".join(f"{v}B" for v in entry["params"])
            print(f"-- {entry['file']} @ line {entry['line']}  -> Candidates: [{params_str}]")
            print(entry["snippet"])
            print("")
            
    # Report Output
    if args.report:
        write_report(results, Path(args.report))


if __name__ == "__main__":
    main()
