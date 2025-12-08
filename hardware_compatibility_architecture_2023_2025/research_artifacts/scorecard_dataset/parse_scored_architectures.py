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
    # Fresh parse from markdown (authoritative for core scores and row set)
    df_md = parse_markdown_tables(text)

    # If a previous CSV exists, preserve metadata columns like Param_Billions, Model_Locations,
    # Analyzed, and Section where possible instead of clobbering them.
    if csv_path.exists():
        df_old = pd.read_csv(csv_path)
        if "ID" in df_old.columns:
            df_old = df_old.set_index("ID")

            # Helper to merge a single column from old CSV into the markdown frame.
            def merge_column(col: str, prefer_md: bool = True) -> None:
                nonlocal df_md, df_old
                if col not in df_md.columns and col not in df_old.columns:
                    return
                # Start with existing markdown values if present.
                if col not in df_md.columns:
                    df_md[col] = ""
                # Old values keyed by ID (as strings to be robust)
                if col in df_old.columns:
                    old_series = df_old[col]
                    mapped = df_md["ID"].map(lambda i: old_series.get(i, old_series.get(str(i), "")))
                else:
                    mapped = pd.Series([""] * len(df_md))

                # Decide per‑row whether to keep MD value or pull from old CSV.
                def choose(md_val, old_val):
                    md_str = "" if pd.isna(md_val) else str(md_val).strip()
                    old_str = "" if pd.isna(old_val) else str(old_val).strip()
                    if prefer_md:
                        # If markdown has a non‑empty value, keep it; otherwise fall back to old CSV.
                        return md_val if md_str != "" else old_val
                    # If markdown is empty, but old CSV has a value, use the old value.
                    return old_val if old_str != "" else md_val

                df_md[col] = [choose(m, o) for m, o in zip(df_md[col], mapped)]

            # Param_Billions / Model_Locations exist only in CSV; always prefer old values.
            merge_column("Param_Billions", prefer_md=False)
            merge_column("Model_Locations", prefer_md=False)
            # Analyzed and Section may be edited in MD; prefer markdown when non‑empty.
            merge_column("Analyzed", prefer_md=True)
            merge_column("Section", prefer_md=True)

    df_md.to_csv(csv_path, index=False)
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
