import argparse
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
CSV_PATH = BASE_DIR / "scored_architectures.csv"
MD_PATH = BASE_DIR / "scored_architectures.md"
PAPERS_ROOT = BASE_DIR / "papers"

ARXIV_API = "https://export.arxiv.org/api/query"

from parse_scored_architectures import parse_markdown_tables
from utils import setup_logger

logger = setup_logger("fetch_papers")


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
    """
    text = MD_PATH.read_text(encoding="utf-8")
    df = parse_markdown_tables(text)

    id_whitelist = {str(i) for i in only_ids} if only_ids is not None else None

    def is_empty_params(val: Optional[str]) -> bool:
        s = (str(val) if val is not None else "").strip()
        return s in {"", "[]"}

    missing: List[str] = []
    # If using dataframe from parse_markdown_tables (which returns a DF), iterate rows
    # Note: parse_markdown_tables returns a PD DataFrame
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
        
        # If we provided specific IDs, we process them regardless of param state (force mode)
        # Otherwise, check if params are empty
        if id_whitelist is None:
             if not is_empty_params(row.get("Param_Billions", "")):
                continue

        missing.append(id_)
    return missing


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
    except Exception as e:
        logger.warning(f"arXiv query failed for title={title!r}: {e}")
        return None
    if resp.status_code != 200:
        logger.warning(f"arXiv query status {resp.status_code} for title={title!r}")
        return None
    import xml.etree.ElementTree as ET

    root = ET.fromstring(resp.text)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entry = root.find("a:entry", ns)
    if entry is None:
        logger.warning(f"No arXiv entry for title={title!r}")
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
    """
    # Preload markdown rows for arXiv extraction.
    text = MD_PATH.read_text(encoding="utf-8")
    df = parse_markdown_tables(text)
    id_to_row = {str(r["ID"]).strip(): r for _, r in df.iterrows() if str(r.get("ID", "")).strip()}

    result: Dict[str, List[PaperSpec]] = {}

    for id_ in missing_ids:
        papers: List[PaperSpec] = []
        row = id_to_row.get(id_)
        if row is None:
            logger.info(f"No markdown row found for ID={id_}, skipping.")
            continue

        # Prefer explicit arXiv links from Model_Locations when present.
        arxiv_ids: List[str] = []

        raw_locs = str(row.get("Model_Locations", "") or "").strip()
        if raw_locs:
            try:
                # Handle possible python literal list or JSON
                import ast
                # Clean markdown backticks if present
                clean = raw_locs.replace("`", "").strip()
                if clean.startswith("["):
                     locs = ast.literal_eval(clean)
                else:
                     locs = [clean]
                
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
            logger.debug(f"No arXiv links in markdown for ID={id_}, skipping.")
            continue

        title = str(
            row.get("Source / Paper") or row.get("Architecture") or id_
        ).strip()
        for aid in arxiv_ids:
            papers.append(PaperSpec(title=title, arxiv_id=aid))

        # Check PDF resolution
        papers_with_urls = [p for p in papers if p.pdf_url]
        if not papers_with_urls:
            logger.debug(f"No PDFs resolvable for ID={id_}, skipping.")
            continue
        result[id_] = papers_with_urls

    return result


def download_pdf(url: str, dest: Path) -> bool:
    if dest.exists():
        logger.debug(f"Skipping download (exists): {dest.name}")
        return True
    try:
        logger.info(f"Downloading {url}...")
        resp = requests.get(url, timeout=60)
    except Exception as e:
        logger.warning(f"Download failed for {url}: {e}")
        return False
    if resp.status_code != 200 or "application/pdf" not in resp.headers.get(
        "Content-Type", ""
    ):
        logger.warning(
            f"Unexpected response for {url}: status={resp.status_code}, "
            f"content-type={resp.headers.get('Content-Type')}"
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
    if md_path.exists() and md_path.stat().st_size > 0:
        # Do not overwrite existing non-empty markdown
        logger.debug(f"Skipping conversion (exists): {md_path.name}")
        return

    try:
        logger.info(f"Converting {pdf_path.name} to markdown...")
        md = MarkItDown()
        result = md.convert(str(pdf_path))
        md_text = result.markdown or result.text_content or ""
        if not md_text:
             logger.warning(f"Conversion produced empty text for {pdf_path.name}")
             return
        md_path.write_text(md_text, encoding="utf-8")
    except Exception as e:
        logger.error(f"markitdown conversion failed for {pdf_path}: {e}")
        # Do not create empty files on failure


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and convert PDFs for scorecard architectures.")
    parser.add_argument("--ids", nargs="+", help="Specific IDs to process (e.g. A1 B2). If omitted, finds all missing.")
    args = parser.parse_args()

    logger.info(f"=== STARTED fetch_papers | Command: {' '.join(sys.argv)} ===")
    logger.debug(f"Parsed Args: {args}")

    missing_ids = load_missing_ids(only_ids=args.ids, include_analyzed=bool(args.ids))
    if not missing_ids:
        logger.info("No IDs to process.")
        return

    logger.info(f"Processing {len(missing_ids)} IDs.")

    id_to_papers = ensure_papers_for_ids(missing_ids)
    if not id_to_papers:
        logger.info("No papers resolved; nothing to do.")
        return

    for id_, papers in id_to_papers.items():
        id_dir = PAPERS_ROOT / id_
        pdf_dir = id_dir / "pdf"
        md_dir = id_dir / "markdown"
        pdf_dir.mkdir(parents=True, exist_ok=True)
        md_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"=== ID {id_}: downloading {len(papers)} paper(s) ===")
        for idx, p in enumerate(papers, start=1):
            if not p.pdf_url:
                continue
            safe_stem = re.sub(r"[^a-zA-Z0-9]+", "_", p.title)[:80].strip("_") or f"paper_{idx}"
            # Include arxiv id in filename to avoid collisions
            if p.arxiv_id:
                  safe_stem = f"{safe_stem}_{p.arxiv_id}"
            
            pdf_path = pdf_dir / f"{safe_stem}.pdf"
            md_path = md_dir / f"{safe_stem}.md"

            if download_pdf(p.pdf_url, pdf_path):
                convert_pdf_to_markdown(pdf_path, md_path)
            else:
                logger.warning(f"Skipping conversion (download failed) for {p.title}")


if __name__ == "__main__":
    main()
