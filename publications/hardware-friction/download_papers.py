import os
import requests
from markitdown import MarkItDown
import time

papers = [
    ("Vaswani_Attention_2017", "https://arxiv.org/pdf/1706.03762.pdf"),
    ("Ramsauer_Hopfield_2020", "https://arxiv.org/pdf/2008.02217.pdf"),
    ("Ba_FastWeights_2016", "https://arxiv.org/pdf/1610.06258.pdf"),
    ("VonOswald_GradientDescent_2023", "https://arxiv.org/pdf/2212.07677.pdf"),
    ("Garg_ImpliticLearning_2022", "https://arxiv.org/pdf/2208.01066.pdf"),
    ("Xie_BayesianInference_2022", "https://arxiv.org/pdf/2111.02080.pdf"),
    ("Elhage_Circuits_2021", "https://transformer-circuits.pub/2021/framework/index.html"),
    ("Olsson_InductionHeads_2022", "https://arxiv.org/pdf/2209.11895.pdf"),
    ("Deletang_Compression_2024", "https://arxiv.org/pdf/2309.10668.pdf"),
    ("Frankle_LotteryTicket_2019", "https://arxiv.org/pdf/1803.03635.pdf"),
    ("Power_Grokking_2022", "https://arxiv.org/pdf/2201.02177.pdf"),
    ("Gu_Mamba_2024", "https://arxiv.org/pdf/2312.00752.pdf"),
    ("Lieber_Jamba_2024", "https://arxiv.org/pdf/2403.19887.pdf"),
    ("De_Griffin_2024", "https://arxiv.org/pdf/2402.19427.pdf"),
    ("Beck_xLSTM_2024", "https://arxiv.org/pdf/2405.04517.pdf"),
    ("Sun_RetNet_2023", "https://arxiv.org/pdf/2307.08621.pdf"),
    ("Poli_Hyena_2023", "https://arxiv.org/pdf/2302.10866.pdf"),
    ("Perez_TuringCompleteness_2019", "https://arxiv.org/pdf/1901.03429.pdf"),
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
            # For non-PDF URLs (like HTML), markitdown might handle directly or we might download HTML
            # MarkItDown typically handles files. Let's see if we can pass the URL directly or download content.
            # Usually better to download.
            print(f"  Downloading/Processing {url}...")
            # For transformer-circuits, it's HTML. Let's download the HTML page.
            # Or assume MarkItDown can handle it if we pass a local file.
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
    time.sleep(1)

print("Done.")
