import re
from pathlib import Path

repo_root = Path(r"c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model")
broken_macros = [r"\azero", r"\Cobs", r"\Cm", r"\CIR", r"\Ttwo", r"\Tthree"]

results = {}
for md_file in repo_root.glob("**/*.md"):
    if ".git" in md_file.parts:
        continue
    try:
        text = md_file.read_text(encoding="utf-8")
        found = [m for m in broken_macros if m in text]
        if found:
            results[str(md_file.relative_to(repo_root))] = found
    except Exception as e:
        pass

print("Files containing broken macros:")
for f, m in results.items():
    print(f"  {f}: {m}")
