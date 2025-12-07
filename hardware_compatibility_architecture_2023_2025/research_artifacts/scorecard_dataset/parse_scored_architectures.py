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
    lines = text.splitlines()
    rows = []
    current_header = None

    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect header row: starts with '|' and contains 'ID'
        if line.startswith("|") and "ID" in line:
            # Next line should be separator with dashes
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("|----"):
                header_cells = [normalize_header_cell(c) for c in line.split("|")]
                # Drop leading/trailing empty cells from split
                header = [c for c in header_cells if c]
                current_header = header
                i += 2  # skip separator
                # Consume table rows
                while i < len(lines) and lines[i].startswith("|"):
                    row_line = lines[i]
                    cells = [c.strip() for c in row_line.split("|")]
                    cells = [c for c in cells if c]  # drop empty due to edges
                    # Skip separator-like or malformed rows
                    if set(cells[0]) == {"-"}:
                        i += 1
                        continue
                    if len(cells) != len(current_header):
                        i += 1
                        continue
                    row_dict = dict(zip(current_header, cells))
                    rows.append(row_dict)
                    i += 1
                continue
        i += 1

    if not rows:
        raise RuntimeError("No tables parsed from scored_architectures.md")

    df = pd.DataFrame(rows)
    # Try to coerce numeric columns where appropriate
    for col in ["Year", "GA", "MAL", "PAR", "H", "STI", "IM", "E"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].str.replace("**", "", regex=False), errors="ignore")
    return df


def main() -> None:
    root = Path(__file__).resolve().parent
    md_path = root / "scored_architectures.md"
    csv_path = root / "scored_architectures.csv"

    text = md_path.read_text(encoding="utf-8")
    df = parse_markdown_tables(text)
    df.to_csv(csv_path, index=False)
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()

