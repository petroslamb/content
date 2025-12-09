import re
from pathlib import Path

import pandas as pd


def normalize_header_cell(cell: str) -> str:
    cell = cell.strip().strip("|").strip()
    # Strip markdown bold and italics
    cell = cell.replace("**", "").replace("*", "").strip()
    if cell.lower() in {"h", "score (h)", "h-score"}:
        return "H"
    if cell.lower() in {"e", "score (e)", "e-score"}:
        return "E"
    if cell == "Technique":
        return "Architecture"
    return cell


def parse_markdown_tables(text: str) -> pd.DataFrame:
    """Parse all score tables from scored_architectures.md into a DataFrame.

    This implementation is deliberately permissive so that new sections/tables
    (including final‑pass additions) are always captured.
    """
    lines = text.splitlines()
    rows = []

    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect canonical header row
        if line.startswith("| ID ") and "Architecture" in line:
            # Parse header cells, dropping edge pipes
            header_cells = [normalize_header_cell(c) for c in line.split("|")[1:-1]]
            header = header_cells
            # Skip separator line if present
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("|----"):
                i += 2
            else:
                i += 1
            # Consume table rows
            while i < len(lines) and lines[i].startswith("|"):
                row_line = lines[i]
                cells = [c.strip() for c in row_line.split("|")[1:-1]]
                if not cells or cells[0] == "ID":
                    i += 1
                    continue
                if len(cells) != len(header):
                    i += 1
                    continue
                row_dict = dict(zip(header, cells))
                rows.append(row_dict)
                i += 1
            continue
        i += 1

    if not rows:
        raise RuntimeError("No tables parsed from scored_architectures.md")

    df = pd.DataFrame(rows)
    # Coerce numeric columns where appropriate
    for col in ["Year", "GA", "MAL", "PAR", "STI", "IM"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].str.replace("**", "", regex=False), errors="ignore")
    # Derive H and E if needed
    if "H" not in df.columns and all(c in df.columns for c in ["GA", "MAL", "PAR"]):
        df["H"] = df["GA"] + df["MAL"] + df["PAR"]
    if "E" not in df.columns and all(c in df.columns for c in ["STI", "IM"]):
        df["E"] = df["STI"] + df["IM"]
    return df


def main() -> None:
    root = Path(__file__).resolve().parent
    md_path = root / "scored_architectures.md"
    csv_path = root / "scored_architectures.csv"

    text = md_path.read_text(encoding="utf-8")
    # Fresh parse from markdown: scored_architectures.md is the sole source of truth.
    df_md = parse_markdown_tables(text)

    # Overwrite the CSV completely with the parsed markdown.
    df_md.to_csv(csv_path, index=False)
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
