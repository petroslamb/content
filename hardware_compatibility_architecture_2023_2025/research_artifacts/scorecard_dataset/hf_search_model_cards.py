import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence

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
    Lightweight markdown table parser that mirrors the core logic of
    parse_scored_architectures.parse_markdown_tables but returns a list
    of dict rows (stringly typed) for convenience.
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
    section: Optional[str] = None,
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
        if section is not None and str(r.get("Section", "")).strip() != section:
            continue
        selected.append(r)
    return selected


def search_hf_for_architectures(
    only_ids: Optional[Sequence[str]] = None,
    section: Optional[str] = None,
    max_candidates: int = 10,
) -> Dict[str, List[HFMatch]]:
    """
    For each selected architecture in scored_architectures.md, query the
    Hugging Face Hub using its *architecture name* and return a list of
    plausible matches per ID. This script does not modify any files; it
    is a helper for the manual HF step described in the playbook.
    """
    api = HfApi()
    rows = load_rows_for_search(only_ids=only_ids, section=section)

    results: Dict[str, List[HFMatch]] = {}

    for r in rows:
        id_ = str(r.get("ID", "")).strip()
        arch = str(r.get("Architecture", "")).strip()
        if not arch:
            continue

        notes = str(r.get("Notes", "")).strip()
        source = str(r.get("Source / Paper", "")).strip()
        paper_hint = ""
        # Crude heuristic: look for an arXiv ID in Notes/Source.
        for text in (notes, source):
            for token in text.split():
                if token.startswith("arXiv:") or "arxiv.org/abs/" in token:
                    paper_hint = token
                    break
            if paper_hint:
                break

        query = arch.split("(")[0].strip()
        print(f\"\\n=== ID {id_}: {arch} (query={query!r})\")
        try:
            models = api.list_models(search=query, sort=\"downloads\", direction=-1, limit=max_candidates)
        except Exception as e:
            print(f\"  [WARN] HF search failed: {e}\")
            continue

        matches: List[HFMatch] = []
        arch_tokens = {t.lower() for t in query.replace(\"/\", \" \").split() if t}

        for m in models:
            repo = m.id
            repo_l = repo.lower()
            # Simple relevance: require at least one arch token in the repo id.
            if arch_tokens and not any(tok in repo_l for tok in arch_tokens):
                continue

            has_paper = False
            snippet = \"\"
            try:
                readme_path = hf_hub_download(repo_id=repo, filename=\"README.md\")
                text = Path(readme_path).read_text(encoding=\"utf-8\", errors=\"ignore\")
                low = text.lower()
                if paper_hint and paper_hint.lower().split(\"/\")[-1].split(\".\")[0] in low:
                    has_paper = True
                # Grab a short snippet from the top of the card for inspection.
                snippet = \"\\n\".join(text.splitlines()[:15])
            except Exception:
                snippet = \"(could not load README.md)\"

            # Simple score: downloads + bonus if paper is mentioned.
            dl = m.downloads or 0
            score = float(dl) + (1e6 if has_paper else 0.0)
            match = HFMatch(
                id=id_,
                architecture=arch,
                repo_id=repo,
                score=score,
                has_paper_hint=has_paper,
                model_card_snippet=snippet,
            )
            matches.append(match)

        # Sort best-first by score.
        matches.sort(key=lambda x: x.score, reverse=True)
        if not matches:
            print(\"  No plausible HF repos found.\")
        else:
            for m in matches:
                flag = \"*\" if m.has_paper_hint else \" \"
                print(f\"  {flag} {m.repo_id} (score={m.score:.0f}, has_paper={m.has_paper_hint})\")
        results[id_] = matches

    return results


def main() -> None:
    # Default CLI behavior: search for all IDs with empty Model_Locations
    # (or without any huggingface.co URLs) and any Analyzed state.
    rows = parse_markdown_tables()
    ids_needing_hf: List[str] = []
    for r in rows:
        id_ = str(r.get(\"ID\", \"\")).strip()
        if not id_:
            continue
        loc_raw = str(r.get(\"Model_Locations\", \"\") or \"\").strip()
        if not loc_raw or \"huggingface.co\" not in loc_raw:
            ids_needing_hf.append(id_)

    if not ids_needing_hf:
        print(\"All rows already have HF locations or no locations needed.\")
        return

    print(f\"Will search HF for {len(ids_needing_hf)} IDs.\")
    search_hf_for_architectures(only_ids=ids_needing_hf)


if __name__ == \"__main__\":  # pragma: no cover
    main()

