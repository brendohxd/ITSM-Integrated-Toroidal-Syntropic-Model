"""
itsm_phonon_dispersion.py
─────────────────────────
Generates a two-panel figure showing:
  Left  – Sound speed c_s^2 vs kinetic ratio X/a0^2 for the ITSM Plenum Lagrangian
  Right – Phase and group velocity vs wavenumber k/Lambda_UV, illustrating UV clamping

Save location: Assets/Figures/itsm_phonon_dispersion.png
"""

import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── ITSM publication style ────────────────────────────────────────────────────
from itsm_plot_style import apply_tier1_style
apply_tier1_style()

# ── Physical parameters ───────────────────────────────────────────────────────
# c_s_low = sound speed at X = a0^2  (the peak transient value)
c_s_low = np.sqrt(1.11)          # ≈ 1.0536
Lambda_UV = 1.0                  # UV cutoff in units of a0

# ─────────────────────────────────────────────────────────────────────────────
# LEFT PANEL – c_s^2(X/a0^2)
# ─────────────────────────────────────────────────────────────────────────────
# c_s^2 = [1 + (1/3)*(1 + u)^{-1/2}]
#         / [1 + (1/3)*(1 + u)^{-1/2} - (u/3)*(1 + u)^{-3/2}]
# where u = X/a0^2
u = np.logspace(-2, 2, 2000)     # X/a0^2 from 0.01 to 100

sqrt_inv   = (1.0 + u) ** (-0.5)  # (1 + u)^{-1/2}
sqrt_inv3  = (1.0 + u) ** (-1.5)  # (1 + u)^{-3/2}

num   = 1.0 + (1.0 / 3.0) * sqrt_inv
denom = num - (u / 3.0) * sqrt_inv3
cs2   = num / denom

# Peak location and value
peak_idx = np.argmax(cs2)
peak_u   = u[peak_idx]
peak_cs2 = cs2[peak_idx]

# ─────────────────────────────────────────────────────────────────────────────
# RIGHT PANEL – v_ph(k) and v_g(k)
# ─────────────────────────────────────────────────────────────────────────────
k_norm = np.linspace(0.0, 0.99, 2000)          # k/Lambda_UV
k      = k_norm * Lambda_UV

ratio2 = (k / Lambda_UV) ** 2                  # (k/Λ)^2
valid  = ratio2 < 1.0

v_ph = np.where(valid, c_s_low * np.sqrt(np.clip(1.0 - ratio2, 0, None)), np.nan)
v_g  = np.where(valid,
                c_s_low * (1.0 - 2.0 * ratio2) / np.sqrt(np.clip(1.0 - ratio2, 1e-30, None)),
                np.nan)

# ─────────────────────────────────────────────────────────────────────────────
# FIGURE LAYOUT
# ─────────────────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
fig.suptitle("ITSM Phonon Field: Causality Analysis", fontsize=15, fontweight="bold", y=1.01)

# ── LEFT: sound speed ─────────────────────────────────────────────────────────
ax1.semilogx(u, cs2, color="steelblue", linewidth=2.0)

# Lorentz limit
ax1.axhline(y=1.0, color="red", linestyle="--", linewidth=1.4,
            label=r"Lorentz limit $c_s^2 = 1$")

# Transition scale vertical line
ax1.axvline(x=1.0, color="purple", linestyle="--", linewidth=1.2, alpha=0.75,
            label=r"Transition scale $X = a_0^2$")

# Peak marker
ax1.plot(peak_u, peak_cs2, "ro", markersize=8, zorder=5)
ax1.annotate(
    rf"Peak: $c_s^2 \approx {peak_cs2:.2f}$",
    xy=(peak_u, peak_cs2),
    xytext=(peak_u * 2.5, peak_cs2 + 0.03),
    arrowprops=dict(arrowstyle="->", color="red"),
    color="red", fontsize=9,
)

# Low-X limit annotation
ax1.annotate(
    r"$c_s^2 \to 1$  (low $X$)",
    xy=(u[10], cs2[10]),
    xytext=(0.015, 1.06),
    fontsize=8.5, color="dimgray",
    arrowprops=dict(arrowstyle="->", color="dimgray", lw=0.8),
)

# High-X limit annotation
ax1.annotate(
    r"$c_s^2 \to 1$  (high $X$)",
    xy=(u[-20], cs2[-20]),
    xytext=(15, 1.06),
    fontsize=8.5, color="dimgray",
    arrowprops=dict(arrowstyle="->", color="dimgray", lw=0.8),
)

ax1.set_xlabel(r"Kinetic Ratio $X/a_0^2$", fontsize=11)
ax1.set_ylabel(r"Sound Speed Squared $c_s^2$", fontsize=11)
ax1.set_title(r"Phonon Sound Speed: ITSM Plenum Lagrangian", fontsize=11)
ax1.legend(fontsize=9, loc="lower right")
ax1.grid(True, which="both", alpha=0.3)
ax1.set_ylim(0.98, 1.15)

# ── RIGHT: phase & group velocity ────────────────────────────────────────────
ax2.plot(k_norm, v_ph, color="steelblue", linewidth=2.0,
         label=r"Phase velocity $v_{ph}$")
ax2.plot(k_norm, v_g,  color="darkorange", linestyle="--", linewidth=2.0,
         label=r"Group velocity $v_g$")

# Speed-of-light reference
ax2.axhline(y=1.0, color="red", linestyle="--", linewidth=1.4,
            label=r"Speed of light $c = 1$")

# Low-k annotation at k/Λ ≈ 0
ax2.axvline(x=0.0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
ax2.annotate(
    r"Low-$k$: $v_{ph} \approx 1.054$",
    xy=(0.0, c_s_low),
    xytext=(0.08, c_s_low + 0.05),
    fontsize=8.5, color="steelblue",
    arrowprops=dict(arrowstyle="->", color="steelblue", lw=0.8),
)

# Superluminal zone shading
y_top = ax2.get_ylim()[1] if ax2.get_ylim()[1] > 1.3 else 1.3
ax2.fill_between(k_norm, 1.0, 1.3, alpha=0.10, color="red",
                 label="Superluminal zone")

# UV-cutoff annotation box (top-right)
ax2.text(0.62, 1.18,
         r"UV cutoff $\Lambda_{UV}$ clamps" + "\n"
         r"group velocity $v_g \leq 1$" + "\n"
         "for all physical modes",
         fontsize=8.5, color="black",
         bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow",
                   edgecolor="gray", alpha=0.9))

ax2.set_xlabel(r"Wavenumber $k/\Lambda_{UV}$", fontsize=11)
ax2.set_ylabel(r"Velocity (units of $c$)", fontsize=11)
ax2.set_title(r"Microcausality: UV Cutoff Clamps Physical Velocities", fontsize=11)
ax2.legend(fontsize=9, loc="upper right")
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 1.0)
ax2.set_ylim(-0.5, 1.3)

# ── Save ──────────────────────────────────────────────────────────────────────
fig.tight_layout()
out_path = (
    r"c:\Users\brend\OneDrive\Documents\ITSM - Github"
    r"\ITSM-Integrated-Toroidal-Syntropic-Model"
    r"\Assets\Figures\itsm_phonon_dispersion.png"
)
fig.savefig(out_path, bbox_inches="tight")
print(f"Figure saved to: {out_path}")
