#!/usr/bin/env python3
from pathlib import Path
import re
import json

cfg = json.load(open("config.json", encoding="utf-8"))
folders = cfg["folders"]
input_md = Path(folders["output"]) / f"{cfg['project_name']}_manuscript.md"
if not input_md.exists():
    # maybe older path:
    input_md = Path("06_output") / f"{cfg['project_name']}_manuscript.md"

output_md = Path(folders["output"]) / f"{cfg['project_name']}_manuscript_clean.md"

text = input_md.read_text(encoding="utf-8")
lines = text.splitlines()
out_lines = []
for i, line in enumerate(lines):
    # detect top-level chapter heading: line starting with '# ' or '#\t' or '#\xa0'
    if re.match(r'^\s*#\s+', line):
        # ensure blank line before and a page break token for pandoc latex output
        out_lines.append("\n\n\\newpage\n\n")
        out_lines.append(line.strip() + "\n")
    else:
        out_lines.append(line + "\n")

# write
output_md.write_text("".join(out_lines), encoding="utf-8")
print("✅ Clean manuscript written to:", output_md)
