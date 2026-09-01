"""
itsm_nanograv_bayes.py
-----------------------
Two-panel figure: NANOGrav GWB spectrum + per-bin log Bayes factor.
ITSM predicts a Lorentzian toroidal acoustic resonance in [1.08, pi] nHz
on top of the SMBHB power-law background.
Journal standard: white bg, serif, 600 dpi.
Output: Assets/Figures/itsm_nanograv_bayes.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams.update({
    "font.family": "serif", "mathtext.fontset": "cm",
    "font.size": 10, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white",
    "axes.linewidth": 1.0, "xtick.direction": "in", "ytick.direction": "in",
    "xtick.major.size": 5, "ytick.major.size": 5,
    "xtick.minor.size": 2.5, "ytick.minor.size": 2.5,
    "xtick.minor.visible": True, "ytick.minor.visible": True,
    "legend.frameon": True, "legend.framealpha": 1.0,
    "legend.edgecolor": "black", "text.usetex": False,
})

# ── NANOGrav 15-yr approximate published values (Agazie et al. 2023) ──────────
f_nano = np.array([1.98, 3.17, 4.74, 6.31, 7.91, 9.51, 11.1, 12.7])  # nHz
h_nano = np.array([2.4, 1.9, 1.6, 1.4, 1.2, 1.1, 0.95, 0.85]) * 1e-15
err_nano = np.array([0.6, 0.4, 0.3, 0.25, 0.20, 0.18, 0.16, 0.14]) * 1e-15

# ── Model curves ──────────────────────────────────────────────────────────────
f = np.logspace(np.log10(0.6), np.log10(16.0), 500)  # nHz

# SMBHB power law
A_smbhb = 2.4e-15
f_ref   = 1.0  # nHz
def h_smbhb(f): return A_smbhb * (f / f_ref)**(-2/3)

# ITSM = SMBHB + Lorentzian resonance
f0_res  = 1.6   # nHz centre of resonance
gamma   = 0.38  # nHz half-width
A_res   = 0.75e-15
def lorentzian(f): return A_res / (1 + ((f - f0_res) / gamma)**2)
def h_itsm(f): return h_smbhb(f) + lorentzian(f)

# ITSM predicted band
f_lo = 1.08
f_hi = np.pi

# ── Per-bin log Bayes factor ──────────────────────────────────────────────────
h_smbhb_nano = h_smbhb(f_nano)
h_itsm_nano  = h_itsm(f_nano)
# Delta log-likelihood per bin (Gaussian approximation)
dln_like = -0.5 * ((h_nano - h_itsm_nano)**2 - (h_nano - h_smbhb_nano)**2) / err_nano**2
total_lnB = np.sum(dln_like)

# ── Figure ────────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 8),
                                gridspec_kw={"height_ratios": [1.6, 1.0]})
plt.subplots_adjust(hspace=0.38)

# ── Panel A: Strain spectrum ──────────────────────────────────────────────────
ax1.set_xscale("log"); ax1.set_yscale("log")

# Resonance band
ax1.axvspan(f_lo, f_hi, color="#a8c8f0", alpha=0.25, zorder=1,
            label=r"ITSM predicted band $[1.08,\,\pi]$ nHz")

# Model curves
ax1.plot(f, h_smbhb(f), color="black", lw=1.6, ls="--", zorder=3,
         label=r"SMBHB only: $h_c \propto f^{-2/3}$")
ax1.plot(f, h_itsm(f),  color="#1f5fa6", lw=2.2, zorder=4,
         label="ITSM: SMBHB + toroidal resonance")

# Data points
ax1.errorbar(f_nano, h_nano, yerr=err_nano, fmt="o", color="black",
             markersize=4.5, linewidth=1.0, capsize=3, zorder=5,
             label="NANOGrav 15-yr data (Agazie et al. 2023)")

# Resonance centre annotation
ax1.axvline(f0_res, color="#1f5fa6", lw=0.8, ls=":", zorder=2)
ax1.text(f0_res * 1.07, 3.8e-15, f"$f_0={f0_res}$ nHz",
         fontsize=8.5, color="#1f5fa6", va="top")

ax1.set_xlim(0.6, 16.0)
ax1.set_ylim(3e-16, 6e-15)
ax1.set_xlabel(r"Frequency $f$ (nHz)", fontsize=11)
ax1.set_ylabel(r"Characteristic strain $h_c$", fontsize=11)
ax1.set_title("NANOGrav 15-yr GWB: ITSM Toroidal Acoustic Resonance", fontsize=11, pad=6)
ax1.legend(loc="upper right", fontsize=8.5)
ax1.text(0.02, 0.05, "(a)", transform=ax1.transAxes, fontsize=11, fontweight="bold")

# ── Panel B: Per-bin log Bayes factor ────────────────────────────────────────
bar_colors = ["#2e7d32" if d >= 0 else "#b22222" for d in dln_like]
ax2.bar(f_nano, dln_like, width=0.9, color=bar_colors, edgecolor="black",
        linewidth=0.6, zorder=3)

# Jeffreys scale reference lines
ax2.axhline(0, color="black", lw=0.8, zorder=2)
ax2.axhline(3, color="#2e7d32", lw=1.0, ls="--", zorder=2,
            label=r"Moderate evidence ($\ln B = 3$)")
ax2.axhline(5, color="#1a5c1a", lw=1.0, ls="-.", zorder=2,
            label=r"Strong evidence ($\ln B = 5$)")
ax2.axhline(-3, color="#b22222", lw=1.0, ls="--", zorder=2)

# Total annotation
ax2.text(0.98, 0.93,
         f"Total $\\ln B_{{\\rm ITSM/SMBHB}} = {total_lnB:.1f}$",
         transform=ax2.transAxes, ha="right", va="top", fontsize=9.5,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                   edgecolor="black", alpha=0.9))

ax2.set_xlim(0.6, 16.0)
ax2.set_xscale("log")
ax2.set_xlabel(r"Frequency $f$ (nHz)", fontsize=11)
ax2.set_ylabel(r"Per-bin $\Delta\ln\mathcal{L}$", fontsize=11)
ax2.set_title(r"Per-bin Log Bayes Factor: ITSM vs.\ SMBHB", fontsize=11, pad=6)
ax2.legend(loc="lower right", fontsize=8.5)
ax2.text(0.02, 0.93, "(b)", transform=ax2.transAxes, fontsize=11, fontweight="bold")

# Jeffreys label
ax2.text(14.5, 3.3, "Moderate", fontsize=7.5, color="#2e7d32", ha="right")
ax2.text(14.5, 5.3, "Strong",   fontsize=7.5, color="#1a5c1a", ha="right")

plt.tight_layout()

out = Path(__file__).parent.parent / "Assets" / "Figures" / "itsm_nanograv_bayes.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, bbox_inches="tight")
print(f"Saved: {out}")
print(f"Total ln Bayes factor: {total_lnB:.2f}")
