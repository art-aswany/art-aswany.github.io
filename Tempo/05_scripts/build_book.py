import os
import subprocess
from pathlib import Path
import json

# تحميل config.json
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# المجلدات
manuscript_folder = Path(config["folders"]["manuscript"]) / "linked"
output_folder = Path(config["folders"]["output"])
templates_folder = Path(config["folders"]["templates"])
covers_folder = Path("03_covers/covers_output")

output_folder.mkdir(exist_ok=True)

# order.txt داخل linked/
order_file = manuscript_folder / "order.txt"
if not order_file.exists():
    raise FileNotFoundError("❌ order.txt غير موجود في 01_manuscript/linked/")

# دمج الفصول
merged_file = output_folder / f"{config['project_name']}_manuscript.md"
with open(order_file, "r", encoding="utf-8") as f:
    files = [line.strip() for line in f if line.strip()]

with open(merged_file, "w", encoding="utf-8") as outfile:
    for file in files:
        chapter_path = manuscript_folder / file
        if not chapter_path.exists():
            raise FileNotFoundError(f"❌ الملف مفقود: {chapter_path}")
        with open(chapter_path, "r", encoding="utf-8") as infile:
            outfile.write(infile.read())
            outfile.write("\n\n\\newpage\n\n")  # يبدأ كل فصل بصفحة جديدة

print(f"✅ Unified manuscript: {merged_file}")

# نسخة نظيفة
clean_file = output_folder / f"{config['project_name']}_manuscript_clean.md"
with open(merged_file, "r", encoding="utf-8") as f:
    content = f.read()

# تنظيف: إزالة فراغات زائدة
content = content.replace("\n\n\n", "\n\n")

with open(clean_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ Clean manuscript: {clean_file}")

# --- توليد EPUB ---
cover_epub = covers_folder / "cover_front_300dpi.png"
epub_out = output_folder / f"{config['project_name']}.epub"
css_file = templates_folder / config["templates"]["epub"]

if css_file.exists() and cover_epub.exists():
    cmd = [
        "pandoc", str(clean_file),
        "-o", str(epub_out),
        "--epub-cover-image", str(cover_epub),
        "--css", str(css_file),
        "--toc", "--toc-depth=2",
        "--top-level-division=chapter"
    ]
    subprocess.run(cmd, check=True)
    print(f"📘 EPUB generated: {epub_out}")
else:
    print("⚠️ EPUB skipped (cover or css missing)")

# --- توليد PDF ---
cover_pdf = covers_folder / "cover_full_3735x2700.pdf"
pdf_out = output_folder / f"{config['project_name']}.pdf"
template_pdf = templates_folder / config["templates"]["pdf"]

if template_pdf.exists():
    cmd = [
        "pandoc", str(clean_file),
        "-o", str(pdf_out),
        "--pdf-engine=xelatex",
        "--template", str(template_pdf)
    ]
    subprocess.run(cmd, check=True)
    print(f"📕 PDF generated: {pdf_out}")
else:
    print("⚠️ PDF skipped (template missing)")

# --- توليد DOCX ---
docx_out = output_folder / f"{config['project_name']}.docx"
reference_docx = templates_folder / config["templates"]["docx"]

if reference_docx.exists():
    cmd = [
        "pandoc", str(clean_file),
        "-o", str(docx_out),
        "--reference-doc", str(reference_docx)
    ]
    subprocess.run(cmd, check=True)
    print(f"📄 DOCX generated: {docx_out}")
else:
    print("⚠️ DOCX skipped (reference missing)")
