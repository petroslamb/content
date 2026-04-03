import os
import asyncio
from playwright.async_api import async_playwright

INPUT_DIR = "../mermaid_custom"
OUTPUT_DIR = "../mermaid_custom_images"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mermaid Renderer</title>
</head>
<body>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true });
    </script>
    <div class="mermaid">
        {MERMAID_CONTENT}
    </div>
</body>
</html>
"""

async def render_diagram(page, file_path, output_path):
    with open(file_path, "r") as f:
        content = f.read()

    html_content = HTML_TEMPLATE.replace("{MERMAID_CONTENT}", content)
    
    # We'll use a data URL to load the HTML content
    # But wait, data URLs can be tricky with imports. 
    # Let's write a temporary html file.
    temp_html = "temp_render.html"
    with open(temp_html, "w") as f:
        f.write(html_content)

    await page.goto(f"file://{os.path.abspath(temp_html)}")
    
    # Wait for the SVG to be generated
    try:
        await page.wait_for_selector(".mermaid svg", timeout=5000)
        
        # Get the element
        element = await page.query_selector(".mermaid")
        
        # Screenshot
        await element.screenshot(path=output_path)
        print(f"Rendered: {output_path}")
    except Exception as e:
        print(f"Failed to render {file_path}: {e}")
    finally:
        if os.path.exists(temp_html):
            os.remove(temp_html)

async def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Set viewport big enough
        await page.set_viewport_size({"width": 1920, "height": 1080})

        files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".mermaid")]
        
        for file in files:
            input_path = os.path.join(INPUT_DIR, file)
            output_filename = file.replace(".mermaid", ".png")
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            
            print(f"Processing {file}...")
            await render_diagram(page, input_path, output_path)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
