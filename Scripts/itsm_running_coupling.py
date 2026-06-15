"""
itsm_running_coupling.py
------------------------
Publication figure: Running BTFR coupling g(mu) vs kinematic scale mu/a0.

Shows the 1-loop Born-Infeld RG flow from the UV tree-level baseline
g0 = 2/3 to the IR fixed point g* = 1, with the Delta-Gamma = 1/3
one-loop correction shaded.

Output: Assets/Figures/itsm_running_coupling.png
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.linewidth": 1.2,
    "axes.labelsize": 13,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "xtick.minor.size": 3,
    "ytick.minor.size": 3,
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "legend.framealpha": 0.9,
    "legend.fontsize": 10,
    "text.usetex": False,
})

# ── ITSM RG parameters ───────────────────────────────────────────────────────
g0        = 2.0 / 3.0          # tree-level UV coupling
g_star    = 1.0                 # IR fixed point
Lambda_UV = 10.0                # EFT cutoff in units of a0

# Callan-Symanzik running coupling from the 1-loop regulated integral
#   g(mu) = g0 + Delta_Gamma(mu)
#   Delta_Gamma(mu) = (1/3) * [1 - ln(1 + Lambda_UV^2/mu^2)
#                                  / ln(1 + Lambda_UV^2/a0^2)]
# where mu is in units of a0 (so a0 = 1).

mu_over_a0 = np.linspace(0.01, Lambda_UV, 2000)   # mu / a0

ln_denom = np.log(1.0 + Lambda_UV**2)              # = ln(1 + Lambda^2/a0^2)

def Delta_Gamma(mu):
    return (1.0 / 3.0) * (1.0 - np.log(1.0 + Lambda_UV**2 / mu**2) / ln_denom)

g_mu = g0 + Delta_Gamma(mu_over_a0)

# ── Figure ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7.0, 4.8))
fig.patch.set_facecolor("#0d0d14")
ax.set_facecolor("#0d0d14")

# Shaded corridor between g0 and g_star
ax.fill_between(mu_over_a0, g0, g_mu,
                color="#5b8fff", alpha=0.18, zorder=1,
                label=r"1-loop correction $\Delta\Gamma(\mu)$")

# Running coupling curve
ax.plot(mu_over_a0, g_mu,
        color="#5b8fff", lw=2.5, zorder=3,
        label=r"Running coupling $g(\mu)$")

# UV baseline
ax.axhline(g0, color="#aaaaaa", lw=1.2, ls="--", zorder=2,
           label=r"Tree-level UV baseline $g_0 = 2/3$")

# IR fixed point
ax.axhline(g_star, color="#ff6b6b", lw=1.6, ls="-.", zorder=2,
           label=r"IR fixed point $g^* = 1$")

# UV cutoff vertical
ax.axvline(Lambda_UV, color="#ffcc55", lw=1.0, ls=":", zorder=2,
           label=r"EFT cutoff $\Lambda_{\rm UV} = 10\,a_0$")

# Annotation arrow: flow direction
ax.annotate("",
            xy=(0.8, 0.96), xycoords="axes fraction",
            xytext=(0.8, 0.72), textcoords="axes fraction",
            arrowprops=dict(arrowstyle="->", color="#ff6b6b", lw=1.8))
ax.text(0.815, 0.84, "RG flow\n(IR)", transform=ax.transAxes,
        color="#ff6b6b", fontsize=9, va="center")

# Delta Gamma bracket
mu_mid = Lambda_UV * 0.25
g_mid  = g0 + Delta_Gamma(mu_mid)
ax.annotate("",
            xy=(mu_mid, g_star), xytext=(mu_mid, g0),
            arrowprops=dict(arrowstyle="<->", color="#5b8fff", lw=1.5))
ax.text(mu_mid + 0.25, (g0 + g_star) / 2,
        r"$\Delta\Gamma(0) = \frac{1}{3}$",
        color="#5b8fff", fontsize=10, va="center")

# Key value annotations
ax.text(0.02, g0 + 0.012, r"$g_0 = 2/3 \approx 0.667$",
        color="#cccccc", fontsize=9, transform=ax.get_yaxis_transform())
ax.text(0.02, g_star + 0.012, r"$g^* = 1$",
        color="#ff6b6b", fontsize=9, transform=ax.get_yaxis_transform())

# Regime labels
ax.text(0.12, 0.12, "UV regime\n(galactic scales,\nhigh $\\mu$)",
        transform=ax.transAxes, color="#aaaaaa", fontsize=8.5,
        ha="center", va="bottom",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#1a1a2e", alpha=0.7))
ax.text(0.35, 0.88, "IR regime\n($\\mu \\to 0$, cosmological\nacceleration scale)",
        transform=ax.transAxes, color="#aaaaaa", fontsize=8.5,
        ha="center", va="top",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#1a1a2e", alpha=0.7))

# Axes
ax.set_xlim(0.0, Lambda_UV + 0.3)
ax.set_ylim(0.60, 1.08)
ax.set_xlabel(r"Kinematic scale $\mu\,/\,a_0$", color="white")
ax.set_ylabel(r"Running coupling $g(\mu)$", color="white")
ax.tick_params(colors="white", which="both")
for spine in ax.spines.values():
    spine.set_edgecolor("#444444")

# Title
ax.set_title(
    r"ITSM Born-Infeld RG Flow: $g(\mu) = g_0 + \Delta\Gamma(\mu)$",
    color="white", fontsize=12, pad=10)

# Legend
legend = ax.legend(loc="lower left", facecolor="#1a1a2e",
                   edgecolor="#444444", labelcolor="white")

plt.tight_layout()

# ── Save ─────────────────────────────────────────────────────────────────────
out = Path(__file__).parent.parent / "Assets" / "Figures" / "itsm_running_coupling.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved: {out}")
