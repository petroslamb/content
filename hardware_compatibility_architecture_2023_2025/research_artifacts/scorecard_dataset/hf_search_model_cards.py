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
                row_line = lines[i]
                cells = [c.strip() for c in row_line.split("|")[1:-1]]
                if len(cells) == len(header_cells) and cells[0] != "ID":
                    row = dict(zip(header_cells, cells))
                    rows.append(row)
                i += 1
            continue
        i += 1
    return rows


def load_rows_for_search(
    only_ids: Optional[Sequence[str]] = None,
) -> List[Dict[str, str]]:
    id_whitelist = {str(x) for x in only_ids} if only_ids is not None else None
    rows = parse_markdown_tables()
    selected: List[Dict[str, str]] = []
    for r in rows:
        id_ = str(r.get("ID", "")).strip()
        if not id_:
            continue
        if id_whitelist is not None and id_ not in id_whitelist:
            continue
        selected.append(r)
    return selected


def search_hf_for_architectures(only_ids: Optional[Sequence[str]] = None, max_candidates: int = 5) -> None:
    """
    Step 2.0: Search Phase. Find candidate Repos for rows that need them.
    """
    api = HfApi()
    rows = load_rows_for_search(only_ids=only_ids)
    print(f"--- Step 2.0: Searching HF for {len(rows)} architectures ---")

    for r in rows:
        id_ = r.get("ID", "")
        arch = r.get("Architecture", "")
        # Filter Logic: Only search if Model_Locations is likely empty or user forced it
        # But for CLI, we just search what is passed.
        
        query = arch.split("(")[0].strip()
        print(f"\n[ID: {id_}] Searching for '{query}'...")
        
        try:
            models = api.list_models(search=query, sort="downloads", direction=-1, limit=max_candidates)
        except Exception as e:
            print(f"  [WARN] Search failed: {e}")
            continue

        if not models:
            print("  No results found.")
            continue

        for m in models:
            print(f"  * Candidate: https://huggingface.co/{m.id} (Downloads: {m.downloads})")


def inspect_existing_locations(only_ids: Optional[Sequence[str]] = None) -> None:
    """
    Step 2.1 Prong A: Inspect existing URLs for parameters.
    """
    rows = load_rows_for_search(only_ids=only_ids)
    print(f"--- Step 2.1(A): Inspecting known locations for {len(rows)} architectures ---")
    
    # Simple regex for "X B parameters" or "X M parameters"
    # Matches: 7B, 7.0B, 130M, etc.
    param_pattern = re.compile(r"(\d+(?:\.\d+)?)\s*([BM])\s*parameters?", re.IGNORECASE)

    for r in rows:
        id_ = r.get("ID", "")
        loc_str = r.get("Model_Locations", "")
        if not loc_str or "huggingface.co" not in loc_str:
            continue

        # Parse JSON list if possible, else naive string extract
        urls: List[str] = []
        try:
            # Handle markdown/JSON mix if needed, but playbook says it's a JSON list.
            # Safety cleanup if it has code blocks
            clean_loc = loc_str.replace("`", "").strip()
            if clean_loc.startswith("["):
                urls = ast.literal_eval(clean_loc)
            elif "http" in clean_loc:
                 urls = [clean_loc]
        except Exception:
            # Fallback regex extraction
            urls = re.findall(r"https://huggingface\.co/[\w\-\./]+", loc_str)

        hf_urls = [u for u in urls if "huggingface.co" in u]
        if not hf_urls:
            continue

        print(f"\n[ID: {id_}] Inspecting {len(hf_urls)} HF URLs...")
        
        found_params: Set[float] = set()

        for url in hf_urls:
            # Extract repo_id from URL: https://huggingface.co/org/repo
            parts = url.replace("https://huggingface.co/", "").strip("/").split("/")
            if len(parts) < 2:
                continue
            repo_id = "/".join(parts[:2])
            
            print(f"  Fetching README for {repo_id}...")
            try:
                readme_path = hf_hub_download(repo_id=repo_id, filename="README.md")
                text = Path(readme_path).read_text(encoding="utf-8", errors="ignore")
                
                # Regex Search
                matches = param_pattern.findall(text)
                for (num_str, unit) in matches:
                    val = float(num_str)
                    if unit.upper() == "M":
                        val /= 1000.0
                    found_params.add(round(val, 3))
            except Exception as e:
                print(f"    Failed to fetch/parse: {e}")

        if found_params:
            sorted_params = sorted(list(found_params))
            print(f"  -> SUGGESTION: Set Param_Billions = {sorted_params}")
        else:
            print("  -> No parameters found in READMEs.")


def main():
    parser = argparse.ArgumentParser(description="Tool to search HF for scorecard architectures.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command: Search
    parser_search = subparsers.add_parser("search", help="Step 2.0: Search HF for candidates.")
    parser_search.add_argument("--ids", nargs="+", help="Specific IDs to process (e.g. A1 B2).")

    # Command: Inspect
    parser_inspect = subparsers.add_parser("inspect", help="Step 2.1A: Inspect existing locations for params.")
    parser_inspect.add_argument("--ids", nargs="+", help="Specific IDs to process.")

    args = parser.parse_args()

    if args.command == "search":
        search_hf_for_architectures(only_ids=args.ids)
    elif args.command == "inspect":
        inspect_existing_locations(only_ids=args.ids)


if __name__ == "__main__":
    main()
```
