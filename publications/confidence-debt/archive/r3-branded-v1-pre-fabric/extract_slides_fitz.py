import fitz
import os

def extract_slides():
    pdf_path = "publications/confidence-debt/artifacts/notebooklm/confidence-debt-slides-r3.pdf"
    output_dir = "publications/confidence-debt/artifacts/slides/confidence-debt-slides-r3"
    os.makedirs(output_dir, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        output_path = os.path.join(output_dir, f"slide-{i+1:03d}.png")
        pix.save(output_path)
        print(f"Saved {output_path}")

if __name__ == "__main__":
    extract_slides()
