import re
from pathlib import Path

path = Path(r"c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\papers\Selective-Publishing-Plan\ITSM_Selective_Publishing_Plan.md")
content = path.read_text(encoding="utf-8")

# Replacements for custom macros
replacements = {
    r"\azero": r"a_0",
    r"\Cobs": r"C_{\mathrm{obs}}",
    r"\Cm": r"C_m",
    r"\CIR": r"C_{\mathrm{IR}}",
    r"\Ttwo": r"T^2",
    r"\Tthree": r"T^3",
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Standardize \( ... \) to $ ... $
def replace_parens(match):
    math_text = match.group(1).strip()
    return f"${math_text}$"

content = re.sub(r"\\\((.*?)\\\)", replace_parens, content)

path.write_text(content, encoding="utf-8")
print(f"Updated {path}")
