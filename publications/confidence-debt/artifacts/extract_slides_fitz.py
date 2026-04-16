import fitz  # PyMuPDF
from pathlib import Path
import sys

def extract_slides(pdf_path, output_root, dpi=300):
    pdf_path = Path(pdf_path)
    output_root = Path(output_root)
    output_dir = output_root / pdf_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    padding = max(3, len(str(len(doc))))
    matrix = fitz.Matrix(dpi / 72, dpi / 72)

    print(f"Extracting {len(doc)} pages from {pdf_path}...")
    for i, page in enumerate(doc):
        page_num = i + 1
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        output_path = output_dir / f"slide-{page_num:0{padding}d}.png"
        pix.save(output_path)
        print(f"  Saved {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_slides_fitz.py <pdf_path> <output_root> [dpi]")
        sys.exit(1)

    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    extract_slides(sys.argv[1], sys.argv[2], dpi)
