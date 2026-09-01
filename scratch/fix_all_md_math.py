import re
from pathlib import Path

repo_root = Path(r"c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model")

replacements = {
    r"\azero": r"a_0",
    r"\Cobs": r"C_{\mathrm{obs}}",
    r"\Cm": r"C_m",
    r"\CIR": r"C_{\mathrm{IR}}",
    r"\Ttwo": r"T^2",
    r"\Tthree": r"T^3",
}

target_dirs = ["Theory", "papers", "Analysis"]

updated_files = []
for target in target_dirs:
    dir_path = repo_root / target
    for md_file in dir_path.glob("**/*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            orig = content
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            # Also convert \( \) to $ $ if present
            def replace_parens(match):
                math_text = match.group(1).strip()
                return f"${math_text}$"
            content = re.sub(r"\\\((.*?)\\\)", replace_parens, content)

            if content != orig:
                md_file.write_text(content, encoding="utf-8")
                updated_files.append(str(md_file.relative_to(repo_root)))
        except Exception as e:
            print(f"Error on {md_file}: {e}")

print(f"Fixed {len(updated_files)} files:")
for f in updated_files:
    print(f"  {f}")
