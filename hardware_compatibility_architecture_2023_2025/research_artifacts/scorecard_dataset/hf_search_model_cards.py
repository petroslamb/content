#!/usr/bin/env python3
import argparse
import ast
import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set

import pandas as pd
from huggingface_hub import HfApi, hf_hub_download

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
MD_PATH = BASE_DIR / "scored_architectures.md"
HF_TOKEN = os.getenv("HF_TOKEN")

@dataclass
class HFMatch:
    id: str
    architecture: str
    repo_id: str
    score: float
    has_paper_hint: bool
    model_card_snippet: str


def parse_markdown_tables() -> pd.DataFrame:
    """
    Lightweight markdown table parser. Returns a DataFrame.
    """
    if not MD_PATH.exists():
        logger.error(f"Markdown file not found at {MD_PATH}")
        return pd.DataFrame()

    text = MD_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    data = []
    
    # Simple state machine to find tables (looking for | ID | header)
    headers = None
    in_table = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            continue
            
        cells = [c.strip() for c in stripped.split("|")[1:-1]]
        
        if "ID" in cells and "Architecture" in cells:
            headers = cells
            in_table = True
            continue
            
        if in_table and set(stripped) <= set("|-: "):
            # Separator line
            continue
            
        if in_table and headers:
            # Data row
            if len(cells) == len(headers):
                row = dict(zip(headers, cells))
                data.append(row)
            # Handle potentially mismatched columns leniently if needed, 
            # but usually strict is better.
            
    return pd.DataFrame(data)


def get_target_architectures(filter_ids: Optional[List[str]] = None) -> List[Dict[str, str]]:
    df = parse_markdown_tables()
    if df.empty:
        return []

    targets = []
    whitelist = set(filter_ids) if filter_ids else None

    for _, row in df.iterrows():
        rid = str(row.get("ID", "")).strip()
        if not rid:
            continue
        
        if whitelist:
            if rid not in whitelist:
                continue
        else:
            # If no whitelist, skip if already analyzed
            analyzed = str(row.get("Analyzed", "")).strip()
            if analyzed.lower() == "analyzed":
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
        # Use simple filter if needed, but search is usually enough
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
    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*(B|billion|M|million)\s*(?:parameters?|params?)", 
        text, 
        flags=re.IGNORECASE
    )
    
    if matches:
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
        
        clean_name = re.sub(r"\(.*?\)", "", name).strip()
        results = search_huggingface(clean_name, limit=5)
        
        if results:
            for r in results:
                logger.info(f"  Candidate: https://huggingface.co/{r}")
        else:
            logger.info("  No obvious matches found.")
        
        idx += 1
        if idx >= 10 and not args.ids:
             logger.info("\nPausing after 10 architectures to avoid rate limits/spam. Re-run or specify IDs.")
             break


def cmd_inspect(args):
    """Execution logic for 'inspect' subcommand."""
    if not args.ids:
        logger.info("Please provide --ids to inspect (e.g. --ids A1 A2).")
        return

    targets = get_target_architectures(args.ids)
    
    for t in targets:
        rid = t["id"]
        name = t["name"]
        logger.info(f"\n=== Inspecting {name} ({rid}) ===")
        
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
    args.func(args)


if __name__ == "__main__":
    main()
