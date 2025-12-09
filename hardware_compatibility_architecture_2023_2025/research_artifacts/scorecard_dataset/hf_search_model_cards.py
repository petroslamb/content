```python
import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set

from huggingface_hub import HfApi, hf_hub_download


BASE_DIR = Path(__file__).resolve().parent
MD_PATH = BASE_DIR / "scored_architectures.md"


@dataclass
class HFMatch:
    id: str
    architecture: str
    repo_id: str
    score: float
    has_paper_hint: bool
    model_card_snippet: str


def parse_markdown_tables() -> List[Dict[str, str]]:
    """
    Lightweight markdown table parser.
    """
    text = MD_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    rows: List[Dict[str, str]] = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("| ID ") and "Architecture" in line:
            header_cells = [c.strip() for c in line.split("|")[1:-1]]
            # Skip separator
            i += 1
            if i < len(lines) and lines[i].strip().startswith("|----"):
                i += 1
            # Consume rows
            while i < len(lines) and lines[i].startswith("|"):
    df = parse_markdown_tables(text)

    targets = []
    # If filter_ids is provided, we search for those specifically.
    # Otherwise, we look for rows where Analyzed is empty OR Param_Billions is empty.
    
    # Correction: The playbook says Step 2.0 searches for things where Analyzed is empty.
    # But if specific IDs are requested, we ignore the Analyzed status.
    
    whitelist = set(filter_ids) if filter_ids else None

    for _, row in df.iterrows():
        rid = str(row.get("ID", "")).strip()
        if not rid:
            continue
        
        if whitelist and rid not in whitelist:
            continue
            
        # If no whitelist, skip if already analyzed
        if not whitelist:
            analyzed = str(row.get("Analyzed", "")).strip()
            if analyzed:
                continue

        name = str(row.get("Architecture", "")).strip()
        targets.append({"id": rid, "name": name})

    return targets


def search_huggingface(query: str, limit: int = 5) -> List[str]:
    """
    Searches HF Hub for models matching the query (architecture name).
    Returns a list of model IDs (e.g. 'meta-llama/Llama-2-7b').
    """
    api = HfApi(token=HF_TOKEN)
    try:
        models = api.list_models(search=query, limit=limit, sort="downloads", direction="-1")
        return [m.modelId for m in models]
    except Exception as e:
        logger.error(f"Search failed for '{query}': {e}")
        return []


def inspect_model_card(model_id: str) -> Optional[str]:
    """
    Downloads the README.md of a model and extracts potential parameter counts.
    Returns a string summary or None.
    """
    try:
        readme_path = hf_hub_download(repo_id=model_id, filename="README.md", token=HF_TOKEN)
        text = Path(readme_path).read_text(errors="ignore")
    except Exception as e:
        logger.debug(f"Could not fetch README for {model_id}: {e}")
        return None

    # Regex for parameters (billions/millions)
    # Matches: 7B, 7.5B, 175 billion, 10M, etc.
    # Look for context words like 'parameters', 'params'
    
    # Reuse the robust regex from inspect_params? 
    # For now, let's keep the existing simple one but log it deeper.
    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*(B|billion|M|million)\s*(?:parameters?|params?)", 
        text, 
        flags=re.IGNORECASE
    )
    
    if matches:
        # Dedupe
        unique = sorted(list(set(matches)))
        return f"Found params: {unique}"
    return None


def cmd_search(args):
    """Execution logic for 'search' subcommand."""
    targets = get_target_architectures(args.ids)
    if not targets:
        logger.info("No targets found to search.")
        return

    logger.info(f"Searching for {len(targets)} architectures...")
    
    idx = 0
    for t in targets:
        rid = t["id"]
        name = t["name"]
        logger.info(f"\n--- [ID: {rid}] {name} ---")
        
        # Heuristic: Clean up name (remove 'Paper:', etc)
        clean_name = re.sub(r"\(.*?\)", "", name).strip()
        results = search_huggingface(clean_name, limit=5)
        
        if results:
            for r in results:
                logger.info(f"  Candidate: https://huggingface.co/{r}")
                # Optional: Deep inspect immediately? No, following playbook Step 2.0 -> 2.1 separation.
        else:
            logger.info("  No obvious matches found.")
        
        idx += 1
        if idx >= 10 and not args.ids:
             logger.info("\nPausing after 10 architectures to avoid rate limits/spam. Re-run or specify IDs.")
             break


def cmd_inspect(args):
    """Execution logic for 'inspect' subcommand."""
    # For inspect, we usually expect specific IDs or we iterate those with existing URLs.
    # But usually this is called with specific IDs found in Step 2.0
    
    if not args.ids:
        logger.info("Please provide --ids to inspect (e.g. --ids A1 A2).")
        return

    # We reuse get_targets just to resolve names
    targets = get_target_architectures(args.ids)
    
    for t in targets:
        rid = t["id"]
        name = t["name"]
        logger.info(f"\n=== Inspecting {name} ({rid}) ===")
        
        # In a real workflow, we would parse the 'Model_Locations' from markdown to find WHAT to inspect.
        # But for this specialized tool, we might re-search or expect the user provided URLs?
        # The Playbook says: "Run inspection on candidates found in Step 2.0".
        # Since this tool is stateless, it essentially re-searches top candidates and inspects them.
        
        clean_name = re.sub(r"\(.*?\)", "", name).strip()
        candidates = search_huggingface(clean_name, limit=3)
        
        for model_id in candidates:
            summary = inspect_model_card(model_id)
            if summary:
                logger.info(f"  Model: {model_id}")
                logger.info(f"    -> {summary}")
            else:
                logger.debug(f"  Model: {model_id} (No params found)")


def main():
    parser = argparse.ArgumentParser(description="Hugging Face Search & Inspection Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: search
    parser_search = subparsers.add_parser("search", help="Search HF for candidate model URLs")
    parser_search.add_argument("--ids", nargs="+", help="Specific IDs to search (e.g. A1 B5)")
    parser_search.set_defaults(func=cmd_search)

    # Subcommand: inspect
    parser_inspect = subparsers.add_parser("inspect", help="Inspect model cards for parameter counts")
    parser_inspect.add_argument("--ids", nargs="+", help="Specific IDs to inspect")
    parser_inspect.set_defaults(func=cmd_inspect)

    args = parser.parse_args()
    logger.info(f"=== STARTED hf_search ({args.command}) | Command: {' '.join(sys.argv)} ===")
    logger.debug(f"Parsed Args: {args}")
    args.func(args)


if __name__ == "__main__":
    main()
```
