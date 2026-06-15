"""
itsm_running_coupling.py
------------------------
Publication figure: Running BTFR coupling g(mu) vs kinematic scale mu/a0.

Adheres to tier-1 journal standards (PRD/JCAP/PRL):
  - White background, black axes, print-safe colors
  - Serif (Computer Modern-style) fonts, 300 dpi
  - No decorative glow or dark-mode styling

Output: Assets/Figures/itsm_running_coupling.png
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# ── Journal style ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":          "serif",
    "mathtext.fontset":     "cm",
    "font.size":            11,
    "axes.linewidth":       1.0,
    "axes.labelsize":       12,
    "axes.titlesize":       12,
    "xtick.direction":      "in",
    "ytick.direction":      "in",
    "xtick.major.size":     5,
    "ytick.major.size":     5,
    "xtick.minor.size":     2.5,
    "ytick.minor.size":     2.5,
    "xtick.minor.visible":  True,
    "ytick.minor.visible":  True,
    "legend.frameon":       True,
    "legend.framealpha":    1.0,
    "legend.edgecolor":     "black",
    "legend.fontsize":      10,
    "figure.facecolor":     "white",
    "axes.facecolor":       "white",
    "savefig.facecolor":    "white",
    "text.usetex":          False,
})

# ── ITSM RG parameters ────────────────────────────────────────────────────────
g0        = 2.0 / 3.0      # tree-level UV coupling
g_star    = 1.0             # IR fixed point
Lambda_UV = 10.0            # EFT cutoff in units of a0

# Running coupling:
#   g(mu) = g0 + Delta_Gamma(mu)
#   Delta_Gamma(mu) = (1/3) * [1 - ln(1 + Lambda^2/mu^2) / ln(1 + Lambda^2)]
mu = np.linspace(0.02, Lambda_UV, 2000)
ln_denom = np.log(1.0 + Lambda_UV**2)

def delta_gamma(m):
    return (1.0 / 3.0) * (1.0 - np.log(1.0 + Lambda_UV**2 / m**2) / ln_denom)

g_mu = g0 + delta_gamma(mu)

# ── Figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 4.2))

# Shaded 1-loop correction corridor
ax.fill_between(mu, g0, g_mu,
                color="#a8c8f0", alpha=0.45, zorder=1,
                label=r"1-loop correction $\Delta\Gamma(\mu)$")

# Running coupling curve
ax.plot(mu, g_mu,
        color="#1f5fa6", lw=2.0, zorder=3,
        label=r"Running coupling $g(\mu) = g_0 + \Delta\Gamma(\mu)$")

# Tree-level UV baseline
ax.axhline(g0, color="black", lw=1.2, ls="--", zorder=2,
           label=r"UV tree-level $g_0 = 2/3$")

# IR fixed point
ax.axhline(g_star, color="#b22222", lw=1.2, ls="-.", zorder=2,
           label=r"IR fixed point $g^{\ast} = 1$")

# EFT cutoff
ax.axvline(Lambda_UV, color="#555555", lw=0.9, ls=":", zorder=2,
           label=r"EFT cutoff $\Lambda_{\rm UV} = 10\,a_0$")

# ── Delta Gamma bracket annotation ────────────────────────────────────────────
mu_bracket = 2.5
ax.annotate("",
            xy=(mu_bracket, g_star), xytext=(mu_bracket, g0),
            textcoords="data",
            arrowprops=dict(arrowstyle="<->", color="#1f5fa6", lw=1.4))
ax.text(mu_bracket + 0.25, (g0 + g_star) / 2.0,
        r"$\Delta\Gamma(0) = 1/3$",
        color="#1f5fa6", fontsize=10, va="center", ha="left")

# ── Regime labels ─────────────────────────────────────────────────────────────
ax.text(8.5, 0.618, "UV\n(galactic inner)",
        fontsize=8.5, ha="center", va="bottom", color="#444444",
        style="italic")
ax.text(1.0, 0.978, "IR (outskirts / cosmic)",
        fontsize=8.5, ha="center", va="top", color="#b22222",
        style="italic")

# RG flow arrow along the curve
ax.annotate("",
            xy=(1.2, g0 + delta_gamma(1.2)),
            xytext=(3.5, g0 + delta_gamma(3.5)),
            textcoords="data",
            arrowprops=dict(arrowstyle="<-", color="#1f5fa6",
                            lw=1.2, mutation_scale=12))

# ── Axes formatting ───────────────────────────────────────────────────────────
ax.set_xlim(0.0, Lambda_UV + 0.4)
ax.set_ylim(0.60, 1.09)
ax.set_xlabel(r"Kinematic scale $\mu\,/\,a_0$")
ax.set_ylabel(r"Running coupling $g(\mu)$")
ax.set_title(
    r"Born-Infeld RG Flow: $g_0 = 2/3 \;\longrightarrow\; g^{\ast} = 1$",
    fontsize=11, pad=6)

# y-tick labels at key values
ax.set_yticks([2/3, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00])
ax.set_yticklabels([r"$2/3$", "0.70", "0.75",
                    "0.80", "0.85", "0.90", "0.95", "1.00"])

ax.legend(loc="lower right", fontsize=9.5)
plt.tight_layout()

# ── Save ──────────────────────────────────────────────────────────────────────
out = Path(__file__).parent.parent / "Assets" / "Figures" / "itsm_running_coupling.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=600, bbox_inches="tight")
print(f"Saved: {out}")
