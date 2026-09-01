"""
Utility module for standardizing Matplotlib plot aesthetics across the ITSM repository.
Enforces a consistent, publication-ready (Tier-1) style for all generated figures.

DPI note: DPI is NOT set globally here. Scripts set dpi explicitly in savefig() only
when needed (e.g., for final submission rendering). Development runs use matplotlib default.
"""
import matplotlib.pyplot as plt

def apply_tier1_style():
    """
    Applies unified Tier-1 peer-review standard formatting to all matplotlib figures.
    Ensures white backgrounds, standard serif LaTeX fonts, and consistent sizing.
    DPI is intentionally left at matplotlib default — set it explicitly in savefig()
    only when preparing final submission-ready exports.
    """
    plt.rcParams.update({
        "text.usetex":          False,
        "text.latex.preamble":  r"\usepackage{amsmath}",
        "font.family":          "serif",
        "mathtext.fontset":     "cm",
        "font.size":            14,
        "axes.titlesize":       16,
        "axes.labelsize":       15,
        "xtick.labelsize":      13,
        "ytick.labelsize":      13,
        "legend.fontsize":      12,
        "axes.linewidth":       1.0,
        "xtick.direction":      "in",
        "ytick.direction":      "in",
        "xtick.major.size":     5,
        "ytick.major.size":     5,
        "xtick.minor.size":     2.5,
        "ytick.minor.size":     2.5,
        "xtick.minor.visible":  True,
        "ytick.minor.visible":  True,
        "axes.facecolor":       "white",
        "figure.facecolor":     "white",
        "savefig.facecolor":    "white",
        "axes.edgecolor":       "black",
        "text.color":           "black",
        "axes.labelcolor":      "black",
        "xtick.color":          "black",
        "ytick.color":          "black",
        "grid.color":           "#e0e0e0",
        "grid.alpha":           0.5,
        "lines.linewidth":      2.0,
        "legend.frameon":       True,
        "legend.framealpha":    1.0,
        "legend.edgecolor":     "black",
    })
