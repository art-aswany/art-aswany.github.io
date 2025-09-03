#!/usr/bin/env python3
# generate_links.py
# يولّد قوائم روابط (GitHub Pages + raw) لملفات داخل authentic/Images و authentic/Resources
# حفظ الناتج في: images_links.txt , resources_links.txt , all_links.txt

import os
from urllib.parse import quote

# ------- عدّلت لك هنا USERNAME و REPO_NAME -------
BASE_URL = "https://art-aswany.github.io/authentic"
RAW_BASE = "https://raw.githubusercontent.com/art-aswany/art-aswany.github.io/main/authentic"
# --------------------------------------------------

# المسارات المحلية (تفترض أن هذا السكربت موضوع في جذر المستودع)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
AUTH_DIR = os.path.join(ROOT_DIR, "authentic")

FOLDERS = {
    "Images": os.path.join(AUTH_DIR, "Images"),
    "Resources": os.path.join(AUTH_DIR, "Resources"),
}

def encode_segment(s):
    # يشفر كل جزء من المسار حتى يكون صالحًا داخل URL
    return quote(s)

def make_pages_link(path_components):
    encoded = "/".join(encode_segment(p) for p in path_components)
    return f"{BASE_URL}/{encoded}"

def make_raw_link(path_components):
    encoded = "/".join(encode_segment(p) for p in path_components)
    return f"{RAW_BASE}/{encoded}"

def collect_files(folder_path):
    results = []
    if not os.path.exists(folder_path):
        return results
    for root, dirs, files in os.walk(folder_path):
        # ترتيب ثابت للملفات
        files_sorted = sorted(files, key=lambda x: x.lower())
        rel_root = os.path.relpath(root, AUTH_DIR)  # e.g. "Images" or "Images/sub"
        for fname in files_sorted:
            if fname.startswith("."):
                continue
            # بناء قائمة أجزاء المسار بالنسبة لمجلد authentic
            if rel_root == ".":
                comps = [fname]
            else:
                comps = rel_root.split(os.sep) + [fname]
            results.append(comps)
    return results

images_links = []
resources_links = []
all_lines = []

# جمع وإنشاء الروابط
for key, folder in FOLDERS.items():
    items = collect_files(folder)
    if not items:
        continue
    all_lines.append(f"--- {key} ---")
    for comps in items:
        pages = make_pages_link(comps)
        raw = make_raw_link(comps)
        if key == "Images":
            images_links.append(pages)
            all_lines.append(f"Image (page): {pages}")
            all_lines.append(f"Image (raw) : {raw}")
        else:
            resources_links.append(pages)
            all_lines.append(f"Resource (page): {pages}")
            all_lines.append(f"Resource (raw) : {raw}")
    all_lines.append("")  # سطر فارغ للفصل

# كتابة الملفات الناتجة
with open("images_links.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(images_links))

with open("resources_links.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(resources_links))

with open("all_links.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(all_lines))

print("✅ Finished: created images_links.txt, resources_links.txt, all_links.txt")
