import os
import requests
from markitdown import MarkItDown
import time

# Tier 1 Priority Papers (Critical Gaps)
papers = [
    ("ProgressMeasures_Grokking_2023", "https://arxiv.org/pdf/2301.05217.pdf"),
    ("BridgingLTH_Grokking_2023", "https://arxiv.org/pdf/2310.19470.pdf"),
    ("MesaOptimization_Transformers_2023", "https://arxiv.org/pdf/2309.05858.pdf"),
    ("WhyCanGPT_ICL_2022", "https://arxiv.org/pdf/2212.10559.pdf"),
    # Tier 2 Priority Papers (Strengthening)
    ("Kaplan_ScalingLaws_2020", "https://arxiv.org/pdf/2001.08361.pdf"),
    ("Wei_EmergentAbilities_2022", "https://arxiv.org/pdf/2206.07682.pdf"),
]

output_dir = "research_artifacts/scorecard_dataset/essays/papers"
os.makedirs(output_dir, exist_ok=True)

md = MarkItDown()

for name, url in papers:
    print(f"Processing {name}...")
    
    # Check if md file already exists
    md_path = os.path.join(output_dir, f"{name}.md")
    if os.path.exists(md_path):
        print(f"  {name}.md already exists, skipping.")
        continue

    # Download or handle URL
    try:
        content_path = None
        if url.endswith(".pdf"):
            pdf_path = os.path.join(output_dir, f"{name}.pdf")
            if not os.path.exists(pdf_path):
                print(f"  Downloading {url}...")
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"})
                response.raise_for_status()
                with open(pdf_path, "wb") as f:
                    f.write(response.content)
            content_path = pdf_path
        else:
            # For non-PDF URLs
            print(f"  Downloading/Processing {url}...")
            ext = ".html"
            html_path = os.path.join(output_dir, f"{name}{ext}")
            if not os.path.exists(html_path):
                 response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"})
                 response.raise_for_status()
                 with open(html_path, "wb") as f:
                     f.write(response.content)
            content_path = html_path

        # Convert
        print(f"  Converting {content_path} to markdown...")
        result = md.convert(content_path)
        
        with open(md_path, "w") as f:
            f.write(result.text_content)
        
        print(f"  Saved to {md_path}")
        
    except Exception as e:
        print(f"  ERROR processing {name}: {e}")

    # Be nice to ArXiv
    time.sleep(2)

print("Done.")
