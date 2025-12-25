import os
import subprocess
from markitdown import MarkItDown

def convert_pdfs_in_directory(pdf_dir, output_dir):
    """
    Simulates conversion using MarkItDown (which typically is a CLI or lib).
    Since I installed `markitdown`, I will try to use it as a library if possible, 
    or fall back to subprocess if it's primarily a CLI tool.
    
    Actually, looking at standard usage for the tool 'markitdown', it's often:
    markitdown input.pdf > output.md
    
    Let's stick to the library if available, but the simplest robust way 
    given the unknown specific version is often the CLI wrapper if it exposes one.
    
    However, the user asked to "use markitdown in a venv". 
    I will instantiate the class as per standard docs if available.
    """
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    md = MarkItDown()

    for filename in os.listdir(pdf_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, filename)
            md_filename = os.path.splitext(filename)[0] + ".md"
            md_path = os.path.join(output_dir, md_filename)
            
            print(f"Converting {filename} to {md_filename}...")
            
            try:
                # Based on typical usage: result = md.convert(pdf_path)
                result = md.convert(pdf_path)
                
                # Check if result has text content directly or needs .text_content
                content = result.text_content if hasattr(result, 'text_content') else str(result)
                
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(content)
                    
                print(f"Successfully converted {filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

if __name__ == "__main__":
    pdf_dir = "pdf"
    markdown_dir = "markdown"
    convert_pdfs_in_directory(pdf_dir, markdown_dir)
