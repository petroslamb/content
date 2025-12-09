import re
import sys
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import requests

try:
    # Prefer MarkItDown for PDF → Markdown conversion; it has a simple
    # Python API and does not require explicit LLM configuration for PDFs.
    from markitdown import MarkItDown
except Exception:  # pragma: no cover - environment / optional dependency
    MarkItDown = None  # type: ignore[assignment]


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / "scored_architectures.csv"
MD_PATH = BASE_DIR.parent / "scored_architectures.md"
PAPERS_ROOT = BASE_DIR

ARXIV_API = "https://export.arxiv.org/api/query"


@dataclass
class PaperSpec:
    title: str
    arxiv_id: Optional[str] = None

    @property
    def pdf_url(self) -> Optional[str]:
        if self.arxiv_id:
            # Strip any version suffix (e.g., 2001.04451v2 -> 2001.04451)
            base_id = self.arxiv_id.split("v")[0]
            return f"https://arxiv.org/pdf/{base_id}.pdf"
        return None


def load_missing_ids(
    include_analyzed: bool = False,
    only_ids: Optional[Sequence[str]] = None,
    section: Optional[str] = None,
) -> List[str]:
    """
    Determine which IDs should be considered for the PDF→Markdown pipeline,
    based on the canonical markdown scorecard.

    Args:
        include_analyzed: If False (default), only include rows where the
            `Analyzed` column in scored_architectures.md is empty. If True,
            rows are eligible regardless of Analyzed.
        only_ids: Optional whitelist of IDs to consider. If provided, only
            IDs in this list will be returned.
        section: Optional section filter; when set, only include rows whose
            `Section` column matches this value exactly.
    """
    # Import markdown parser from the parent scorecard module.
    if str(BASE_DIR.parent) not in sys.path:
        sys.path.append(str(BASE_DIR.parent))
    from parse_scored_architectures import parse_markdown_tables  # type: ignore

    text = MD_PATH.read_text(encoding="utf-8")
    df = parse_markdown_tables(text)

    id_whitelist = {str(i) for i in only_ids} if only_ids is not None else None

    def is_empty_params(val: Optional[str]) -> bool:
        s = (str(val) if val is not None else "").strip()
        return s in {"", "[]"}

    missing: List[str] = []
    for _, row in df.iterrows():
        id_ = str(row.get("ID", "")).strip()
        if not id_:
            continue
        if id_whitelist is not None and id_ not in id_whitelist:
            continue

        row_section = str(row.get("Section", "")).strip()
        if section is not None and row_section != section:
            continue

        analyzed = str(row.get("Analyzed", "")).strip()
        if not include_analyzed and analyzed:
            # Skip rows explicitly marked as analyzed when include_analyzed=False.
            continue

        if not is_empty_params(row.get("Param_Billions", "")):
            continue

        missing.append(id_)
    return missing


def parse_techniques_sections() -> Dict[str, List[str]]:
    """
    Legacy helper that used to map scorecard IDs to sections from
    techniques_for_scoring.md. That file has been removed from the
    pipeline; this function now returns an empty mapping so that the
    downstream logic relies solely on scored_architectures.* data.
    """
    return {}


def extract_papers_from_section(section_text: str) -> List[PaperSpec]:
    """
    Extract PaperSpec entries from a section body.
    We look at 'Canonical paper(s)' and 'Representative papers' bullets.
    """
    papers: List[PaperSpec] = []
    lines = section_text.splitlines()

    collect_following_bullets = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- **Canonical paper:**") or stripped.startswith(
            "- **Canonical papers:**"
        ):
            collect_following_bullets = "Canonical papers" in stripped
            # Extract any titles/arxiv ids on this line itself.
            papers.extend(_extract_paper_specs_from_line(stripped))
            continue
        if stripped.startswith("- **Representative papers:**"):
            collect_following_bullets = True
            continue
        if collect_following_bullets:
            if stripped.startswith("- ") or stripped.startswith("* "):
                papers.extend(_extract_paper_specs_from_line(stripped))
            elif stripped.startswith("## ") or stripped == "" or stripped.startswith(
                "- **Summary:**"
            ):
                # End of the bullet block
                collect_following_bullets = False

    # Deduplicate by title
    unique: Dict[str, PaperSpec] = {}
    for p in papers:
        key = p.title.strip()
        if key not in unique:
            unique[key] = p
        elif not unique[key].arxiv_id and p.arxiv_id:
            unique[key].arxiv_id = p.arxiv_id

    return list(unique.values())


def _extract_paper_specs_from_line(line: str) -> List[PaperSpec]:
    titles = re.findall(r"\*([^*]+)\*", line)
    arxiv_ids = re.findall(r"arXiv:([0-9.]+)", line)
    specs: List[PaperSpec] = []
    # If there is exactly one arxiv_id on this line, attach it to all titles here.
    arxiv_id = arxiv_ids[0] if len(arxiv_ids) == 1 else None
    for t in titles:
        specs.append(PaperSpec(title=t.strip(), arxiv_id=arxiv_id))
    return specs


def search_arxiv_for_title(title: str) -> Optional[str]:
    """
    Find an arXiv ID for a given title, if possible, using the arXiv API.
    """
    query = f'ti:"{title}"'
    params = {
        "search_query": query,
        "start": 0,
        "max_results": 1,
    }
    try:
        resp = requests.get(ARXIV_API, params=params, timeout=15)
    except Exception as e:  # pragma: no cover - best-effort network call
        print(f"[WARN] arXiv query failed for title={title!r}: {e}", file=sys.stderr)
        return None
    if resp.status_code != 200:
        print(
            f"[WARN] arXiv query status {resp.status_code} for title={title!r}",
            file=sys.stderr,
        )
        return None
    import xml.etree.ElementTree as ET

    root = ET.fromstring(resp.text)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entry = root.find("a:entry", ns)
    if entry is None:
        print(f"[WARN] No arXiv entry for title={title!r}", file=sys.stderr)
        return None
    id_text = entry.find("a:id", ns)
    if id_text is None or not id_text.text:
        return None
    # id_text looks like http://arxiv.org/abs/2001.04451v2
    path = urllib.parse.urlparse(id_text.text).path
    arxiv_with_version = path.split("/")[-1]
    base_id = arxiv_with_version.split("v")[0]
    return base_id


def ensure_papers_for_ids(missing_ids: List[str]) -> Dict[str, List[PaperSpec]]:
    """
    For each missing ID, infer the canonical/representative papers from
    scored_architectures.md and resolve arXiv IDs when we can.

    Returns a mapping ID -> list of PaperSpec.
    """
    # Import markdown parser from the parent scorecard module.
    if str(BASE_DIR.parent) not in sys.path:
        sys.path.append(str(BASE_DIR.parent))
    from parse_scored_architectures import parse_markdown_tables  # type: ignore

    id_to_sections = parse_techniques_sections()

    # Preload markdown rows for arXiv extraction.
    text = MD_PATH.read_text(encoding="utf-8")
    df = parse_markdown_tables(text)
    id_to_row = {str(r["ID"]).strip(): r for _, r in df.iterrows() if str(r.get("ID", "")).strip()}

    result: Dict[str, List[PaperSpec]] = {}

    for id_ in missing_ids:
        sections = id_to_sections.get(id_)
        papers: List[PaperSpec] = []

        # Primary path: infer arXiv IDs directly from the markdown scorecard.
        if not sections:
            row = id_to_row.get(id_)
            if row is None:
                print(
                    f"[INFO] No markdown row found for ID={id_}, skipping.",
                    file=sys.stderr,
                )
                continue

            # Prefer explicit arXiv links from Model_Locations when present.
            arxiv_ids: List[str] = []

            raw_locs = str(row.get("Model_Locations", "") or "").strip()
            if raw_locs:
                try:
                    locs = __import__("json").loads(raw_locs)
                    if isinstance(locs, list):
                        for url in locs:
                            m = re.search(r"arxiv\.org/abs/([0-9.]+)", str(url))
                            if m:
                                arxiv_ids.append(m.group(1))
                except Exception:
                    pass

            # Also scan Notes / Source / Paper for arXiv IDs as a backup.
            for field in ("Notes", "Source / Paper"):
                raw = str(row.get(field, "") or "").strip()
                for m in re.finditer(r"arXiv:([0-9.]+)", raw):
                    arxiv_ids.append(m.group(1))
                for m in re.finditer(
                    r"https?://arxiv\.org/abs/([0-9.]+)", raw, flags=re.IGNORECASE
                ):
                    arxiv_ids.append(m.group(1))

            # Normalize IDs by dropping version suffixes and trailing dots.
            arxiv_ids = sorted({aid.split("v")[0].rstrip(".") for aid in arxiv_ids})

            if not arxiv_ids:
                print(
                    f"[INFO] No arXiv links in markdown for ID={id_}, skipping.",
                    file=sys.stderr,
                )
                continue

            # Use the scorecard's Source / Paper field as a human-readable title
            # fallback; it is only used for logging and directory naming.
            title = str(
                row.get("Source / Paper") or row.get("Architecture") or id_
            ).strip()
            for aid in arxiv_ids:
                papers.append(PaperSpec(title=title, arxiv_id=aid))

        if not papers:
            print(f"[INFO] No papers extracted for ID={id_}, skipping.", file=sys.stderr)
            continue

        # Resolve missing arXiv IDs where possible.
        for p in papers:
            if not p.arxiv_id:
                arxiv_id = search_arxiv_for_title(p.title)
                if arxiv_id:
                    p.arxiv_id = arxiv_id

        papers_with_urls = [p for p in papers if p.pdf_url]
        if not papers_with_urls:
            print(f"[INFO] No PDFs resolvable for ID={id_}, skipping.", file=sys.stderr)
            continue
        result[id_] = papers_with_urls

    return result


def download_pdf(url: str, dest: Path) -> bool:
    if dest.exists():
        return True
    try:
        resp = requests.get(url, timeout=60)
    except Exception as e:  # pragma: no cover - network
        print(f"[WARN] Download failed for {url}: {e}", file=sys.stderr)
        return False
    if resp.status_code != 200 or "application/pdf" not in resp.headers.get(
        "Content-Type", ""
    ):
        print(
            f"[WARN] Unexpected response for {url}: status={resp.status_code}, "
            f"content-type={resp.headers.get('Content-Type')}",
            file=sys.stderr,
        )
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)
    return True


def convert_pdf_to_markdown(pdf_path: Path, md_path: Path) -> None:
    md_path.parent.mkdir(parents=True, exist_ok=True)
    if MarkItDown is None:
        raise RuntimeError(
            "markitdown is not available. Install it in the papers venv with:\n"
            "  cd scorecard_dataset/papers && .venv/bin/pip install markitdown"
        )
    # Use MarkItDown to convert the PDF into Markdown. For our use case we only
    # need structured text for parameter searches, so the default configuration
    # (no external LLMs) is sufficient.
    try:
        md = MarkItDown()
        result = md.convert(str(pdf_path))
        md_text = result.markdown or result.text_content or ""
        md_path.write_text(md_text, encoding="utf-8")
    except Exception as e:  # pragma: no cover - best-effort conversion
        print(f"[WARN] markitdown conversion failed for {pdf_path}: {e}", file=sys.stderr)
        # Fallback: write an empty stub to avoid breaking downstream scripts.
        if not md_path.exists():
            md_path.write_text("", encoding="utf-8")


def main() -> None:
    missing_ids = load_missing_ids()
    print(f"Found {len(missing_ids)} IDs with missing weights.")

    id_to_papers = ensure_papers_for_ids(missing_ids)
    if not id_to_papers:
        print("No papers resolved; nothing to do.")
        return

    for id_, papers in id_to_papers.items():
        id_dir = PAPERS_ROOT / id_
        pdf_dir = id_dir / "pdf"
        md_dir = id_dir / "markdown"
        pdf_dir.mkdir(parents=True, exist_ok=True)
        md_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n=== ID {id_}: downloading {len(papers)} paper(s) ===")
        for idx, p in enumerate(papers, start=1):
            if not p.pdf_url:
                continue
            safe_stem = re.sub(r"[^a-zA-Z0-9]+", "_", p.title)[:80].strip("_") or f"paper_{idx}"
            pdf_path = pdf_dir / f"{safe_stem}.pdf"
            md_path = md_dir / f"{safe_stem}.md"

            print(f"  -> {p.title} ({p.arxiv_id or 'no-arxiv-id'})", flush=True)
            if download_pdf(p.pdf_url, pdf_path):
                try:
                    convert_pdf_to_markdown(pdf_path, md_path)
                except Exception as e:  # pragma: no cover - best-effort conversion
                    print(f"[WARN] Markdown conversion failed for {pdf_path}: {e}", file=sys.stderr)
            else:
                print(f"[WARN] Skipping conversion for {pdf_path} (download failed)", file=sys.stderr)


if __name__ == "__main__":  # pragma: no cover
    main()
