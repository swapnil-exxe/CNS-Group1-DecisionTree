import os
import subprocess
import re

OUTPUT_DIR = "/Users/swapnil/Documents/cns/GROUP 1 — DECISION TREE/Research_Papers"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def compile_pdf(html_path, pdf_path):
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    subprocess.run(cmd, check=True)
    with open(pdf_path, "rb") as f:
        data = f.read()
    pages = len(re.findall(rb'/Type\s*/Page\b', data))
    return pages

print("PDF compilation helper ready.")
