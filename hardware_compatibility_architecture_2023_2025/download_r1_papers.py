import os
import requests
from markitdown import MarkItDown
import time

# New R1-relevant papers (associative memory, retrieval, SSM limitations)
papers = [
    # Core associative memory / retrieval theory
    ("TestTimeRegression_2025", "https://arxiv.org/pdf/2501.12352.pdf"),
    ("FactualRecall_AssociativeMemory_2024", "https://arxiv.org/pdf/2412.06538.pdf"),
    ("RetrievalHead_LongContext_2024", "https://arxiv.org/pdf/2404.15574.pdf"),
    
    # SSM retrieval limitations
    ("Mamba2_SSM_Duality_2024", "https://arxiv.org/pdf/2405.21060.pdf"),
    ("SSM_SkillGap_GatherAggregate_2025", "https://arxiv.org/pdf/2504.18574.pdf"),
    ("SSM_Transformer_MechanisticEval_2025", "https://arxiv.org/pdf/2505.15105.pdf"),
    
    # Induction heads and ICL
    ("DualRoute_InductionHeads_2025", "https://arxiv.org/pdf/2504.03022.pdf"),
    ("BeyondInductionHeads_Circuits_2025", "https://arxiv.org/pdf/2505.16694.pdf"),
    ("WhichAttentionHeads_ICL_2025", "https://arxiv.org/pdf/2502.14010.pdf"),
    
    # Additional foundational
    ("FFN_KeyValue_Memory_2020", "https://arxiv.org/pdf/2012.14913.pdf"),
    ("LinearTransformers_FastWeights_2021", "https://arxiv.org/pdf/2102.11174.pdf"),
    
    # Needle-in-haystack / long context
    ("BABILong_11M_Haystack_2024", "https://arxiv.org/pdf/2402.10790.pdf"),
    ("LongMamba_ReceptiveField_2025", "https://arxiv.org/pdf/2504.16053.pdf"),
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

    # Download
    try:
        pdf_path = os.path.join(output_dir, f"{name}.pdf")
        if not os.path.exists(pdf_path):
            print(f"  Downloading {url}...")
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"})
            response.raise_for_status()
            with open(pdf_path, "wb") as f:
                f.write(response.content)

        # Convert
        print(f"  Converting {pdf_path} to markdown...")
        result = md.convert(pdf_path)
        
        with open(md_path, "w") as f:
            f.write(result.text_content)
        
        print(f"  Saved to {md_path}")
        
    except Exception as e:
        print(f"  ERROR processing {name}: {e}")

    # Be nice to ArXiv
    time.sleep(1)

print("Done.")
