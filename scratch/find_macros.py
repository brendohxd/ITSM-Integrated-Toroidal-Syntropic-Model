import re
from pathlib import Path

file_path = Path(r"c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\papers\Selective-Publishing-Plan\ITSM_Selective_Publishing_Plan.md")
content = file_path.read_text(encoding="utf-8")

# Find all \command patterns
macros = set(re.findall(r"\\[a-zA-Z]+", content))
standard_latex = {
    r"\rm", r"\mathrm", r"\operatorname", r"\Tr", r"\sim", r"\pi", r"\rho", r"\gamma", r"\theta",
    r"\delta", r"\Delta", r"\Omega", r"\omega", r"\approx", r"\le", r"\ge", r"\to", r"\rightarrow",
    r"\Rightarrow", r"\times", r"\int", r"\partial", r"\nabla", r"\dots", r"\cdots", r"\sqrt",
    r"\frac", r"\quad", r"\qquad", r"\in", r"\mathbb", r"\mathcal", r"\gtrsim", r"\lesssim",
    r"\nu", r"\mu", r"\alpha", r"\beta", r"\kappa", r"\Sigma", r"\sigma", r"\tau", r"\epsilon",
    r"\varepsilon", r"\pm", r"\equiv", r"\ne", r"\hbar", r"\infty", r"\Upsilon", r"\Psi", r"\Phi", r"\Theta"
}

non_standard = [m for m in macros if m not in standard_latex]
print("Non-standard macros found:")
for m in sorted(non_standard):
    print(f"  {m}")
