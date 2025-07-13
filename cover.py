#!/usr/bin/env python3
"""
cover_and_extract_all.py

Usage:
    python3 cover_and_extract_all.py <pdf_dir> <output_dir>

This script:
1. Scans the given directory for all PDF files.
2. For each PDF:
    - Renders the first two pages as PNGs (150 DPI).
    - Extracts the abstract text.
3. Generates a single README.md that showcases all PDFs, preview pages, and abstracts.

Dependencies:
    pip install PyMuPDF
"""

import sys
import os
import re
import fitz  # PyMuPDF
from pathlib import Path

def render_pages(doc, pdf_path, out_dir, dpi=150, max_pages=2):
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    image_paths = []
    for i in range(min(len(doc), max_pages)):
        page = doc[i]
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img_path = os.path.join(out_dir, f"{base}_page{i+1}.png")
        pix.save(img_path)
        image_paths.append(os.path.basename(img_path))  # relative path
        print(f"✔ Saved page {i+1} image: {img_path}")
    return image_paths

def extract_abstract(doc):
    """
    Try to extract abstract from first 1-2 pages of the PDF.
    """
    text = ""
    for i in range(min(2, len(doc))):
        text += doc[i].get_text()

    # Match "Abstract" section: simple heuristic
    match = re.search(r"(?i)(abstract)[\s\n]*[:\-–]*([\s\S]{100,1000})", text)
    if match:
        abstract_raw = match.group(2).strip()
        # Stop at first heading-like line (heuristic)
        abstract_clean = re.split(r"\n[A-Z][^\n]{0,80}\n", abstract_raw)[0].strip()
        return abstract_clean
    return None

def generate_readme(output_dir, pdf_entries):
    readme_path = os.path.join(output_dir, "README.md")
    output_dir_name = os.path.basename(os.path.abspath(output_dir))
    with open(readme_path, "w") as f:
        f.write(f"# 📚 {output_dir_name} 论文精选\n\n")
        for base_pdf, image_list, abstract in pdf_entries:
            base_name = os.path.splitext(base_pdf)[0]
            f.write(f"## [{base_name}]({base_pdf})\n\n")
            if abstract:
                f.write(f"**📝 摘要**：\n\n> {abstract}\n\n")
            f.write("<table><tr>\n")
            for img in image_list:
                f.write(f'  <td><img src="./{img}" alt="Page image" width="500"/></td>\n')
            f.write("</tr></table>\n\n")
    print(f"📄 Generated master README: {readme_path}")

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <pdf_dir> <output_dir>")
        sys.exit(1)

    pdf_dir = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    pdf_entries = []

    for pdf_file in sorted(Path(pdf_dir).glob("*.pdf")):
        orig_name = pdf_file.name
        # 检查文件名是否包含空格
        if " " in orig_name:
            new_name = orig_name.replace(" ", "_")
            new_path = pdf_file.with_name(new_name)
            # 重命名文件
            pdf_file.rename(new_path)
            print(f"⚠️ 文件名包含空格，已重命名为: {new_name}")
            pdf_file = new_path  # 更新 pdf_file 为新路径

        print(f"📎 Processing {pdf_file.name}...")
        try:
            doc = fitz.open(pdf_file)
            image_list = render_pages(doc, pdf_file, output_dir)
            abstract = extract_abstract(doc)

            pdf_target = os.path.join(output_dir, pdf_file.name)
            if not os.path.exists(pdf_target):
                with open(pdf_file, "rb") as src, open(pdf_target, "wb") as dst:
                    dst.write(src.read())

            pdf_entries.append((pdf_file.name, image_list, abstract))
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")

    generate_readme(output_dir, pdf_entries)

if __name__ == "__main__":
    main()
