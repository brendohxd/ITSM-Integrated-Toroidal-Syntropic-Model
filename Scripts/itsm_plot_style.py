"""
Utility module for standardizing Matplotlib plot aesthetics across the ITSM repository.
Enforces a consistent, publication-ready (Tier-1) style for all generated figures.
"""
import matplotlib.pyplot as plt

def apply_tier1_style():
    """
    Applies unified Tier-1 peer-review standard formatting to all matplotlib figures.
    Ensures white backgrounds, standard serif LaTeX fonts, and consistent sizing.
    """
    plt.rcParams.update({
        "text.usetex": False,
        "text.latex.preamble": r"\usepackage{amsmath}",
        "font.family": "serif",
        "font.size": 14,
        "axes.titlesize": 16,
        "axes.labelsize": 15,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "legend.fontsize": 12,
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "axes.edgecolor": "black",
        "text.color": "black",
        "axes.labelcolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "grid.color": "#e0e0e0",
        "grid.alpha": 0.5,
        "lines.linewidth": 2.0
    })
