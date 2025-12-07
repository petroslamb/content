import re
import sys
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import requests
from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / "scored_architectures.csv"
TECHNIQUES_PATH = BASE_DIR.parent / "techniques_for_scoring.md"
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


def load_missing_ids() -> List[str]:
    with CSV_PATH.open(newline="") as f:
        rows = list(__import__("csv").DictReader(f))
    missing = [r["ID"] for r in rows if r["Param_Billions"].strip() == "[]"]
    return missing


def parse_techniques_sections() -> Dict[str, List[str]]:
    """
    Map scorecard IDs (A*/B*/C*) -> raw section text from techniques_for_scoring.md.
    """
    text = TECHNIQUES_PATH.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    sections = []
    current_title = None
    current_lines: List[str] = []

    for line in lines:
        if line.startswith("## "):
            if current_title is not None:
                sections.append((current_title, "".join(current_lines)))
            current_title = line.strip()
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)
    if current_title is not None:
        sections.append((current_title, "".join(current_lines)))

    id_to_sections: Dict[str, List[str]] = {}

    id_pattern = re.compile(
        r"Status:.*?Scored in `scorecard_dataset/scored_architectures\.md` \(([^)]+)\)"
    )

    def expand_token(tok: str) -> List[str]:
        tok = tok.strip()
        if not tok:
            return []
        # Handle ranges like B14–B16 or A2–A3 (note: en dash)
        if "–" in tok or "-" in tok:
            dash = "–" if "–" in tok else "-"
            left, right = [p.strip() for p in tok.split(dash, 1)]
            prefix_left = left[0]
            m_left = re.match(r"([A-Z])(\d+)", left)
            if not m_left:
                return []
            prefix = m_left.group(1)
            start = int(m_left.group(2))
            m_right = re.match(r"([A-Z])?(\d+)", right)
            if not m_right:
                return []
            end_prefix = m_right.group(1) or prefix
            end = int(m_right.group(2))
            if end_prefix != prefix:
                # Unexpected, ignore mixed-prefix ranges.
                return []
            return [f"{prefix}{i}" for i in range(start, end + 1)]
        return [tok]

    for title, body in sections:
        for m in id_pattern.finditer(body):
            ids_str = m.group(1)
            tokens = [t.strip() for t in ids_str.split(",")]
            for tok in tokens:
                for id_ in expand_token(tok):
                    id_to_sections.setdefault(id_, []).append(body)

    return id_to_sections


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
    techniques_for_scoring.md and resolve arXiv IDs when we can.
    Returns a mapping ID -> list of PaperSpec.
    """
    id_to_sections = parse_techniques_sections()
    result: Dict[str, List[PaperSpec]] = {}

    for id_ in missing_ids:
        sections = id_to_sections.get(id_)
        if not sections:
            # Some IDs (e.g., vendor-specific docs) may not have canonical papers.
            print(f"[INFO] No techniques section found for ID={id_}, skipping.", file=sys.stderr)
            continue
        papers: List[PaperSpec] = []
        for section in sections:
            papers.extend(extract_papers_from_section(section))
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
    # Simple text extraction per page; formatted as plain Markdown.
    reader = PdfReader(str(pdf_path))
    chunks: List[str] = []
    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception as e:  # pragma: no cover - best-effort extraction
            print(f"[WARN] Text extraction failed for {pdf_path}: {e}", file=sys.stderr)
            text = ""
        chunks.append(text)
    md_text = "\n\n".join(chunks)
    md_path.write_text(md_text, encoding="utf-8")


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
