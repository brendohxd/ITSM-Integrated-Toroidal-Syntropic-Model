"""
itsm_mock_jwst_spectrum.py
--------------------------
Illustrative mock JWST NIRSpec prediction for an NGC 4217-analog galaxy at z~14.
Shows ITSM-predicted suppression of CO and Na I D features relative to ΛCDM baseline.
Journal standard: white bg, serif, 600 dpi.
Output: Assets/Figures/itsm_mock_jwst_spectrum.png
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams.update({
    "font.family": "serif", "mathtext.fontset": "cm",
    "font.size": 11, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white",
    "axes.linewidth": 1.0, "xtick.direction": "in", "ytick.direction": "in",
    "xtick.major.size": 5, "ytick.major.size": 5,
    "xtick.minor.size": 2.5, "ytick.minor.size": 2.5,
    "xtick.minor.visible": True, "ytick.minor.visible": True,
    "legend.frameon": True, "legend.framealpha": 1.0,
    "legend.edgecolor": "black", "text.usetex": False,
})

# ── Physics ──────────────────────────────────────────────────────────────────
z = 14.0
# CO(3-2): rest 345.796 GHz = 0.867 mm -> observed
lam_CO_rest = 0.867e-3   # m  -> convert to microns
lam_CO_obs  = lam_CO_rest * (1 + z) * 1e6   # microns
# Na I D doublet: rest 589.3 nm
lam_NaI_rest = 589.3e-9  # m
lam_NaI_obs  = lam_NaI_rest * (1 + z) * 1e6  # microns

# Wavelength grid (microns)
lam = np.linspace(7.0, 17.5, 3000)

# ── Continuum ─────────────────────────────────────────────────────────────────
# Modified blackbody-like quasipower continuum
def continuum(lam, T_lam=10.5, alpha=0.3):
    return 1.0 + alpha * np.exp(-0.5 * ((lam - T_lam) / 4.0)**2)

cont = continuum(lam)

# ── Feature profiles (Gaussian) ───────────────────────────────────────────────
def gaussian(lam, lam0, sigma, amp):
    return amp * np.exp(-0.5 * ((lam - lam0) / sigma)**2)

# CO(3-2): absorption dip, sigma~0.25 microns, amplitude=-0.18 (ΛCDM)
sigma_CO   = 0.22
amp_CO_lcdm = -0.20
amp_CO_itsm = amp_CO_lcdm * (1 - 0.15)   # 15% suppression

# Na I D: absorption dip, sigma~0.18 microns, amplitude=-0.14 (ΛCDM)
sigma_NaI   = 0.18
amp_NaI_lcdm = -0.16
amp_NaI_itsm = amp_NaI_lcdm * (1 - 0.20)  # 20% suppression

# Additional minor ISM features (same in both models)
def minor_features(lam):
    return (gaussian(lam, 9.7,  0.35, -0.06) +   # silicate
            gaussian(lam, 11.3, 0.20, -0.04) +   # PAH
            gaussian(lam, 15.0, 0.25, -0.03))

flux_lcdm = (cont
             + gaussian(lam, lam_CO_obs,  sigma_CO,  amp_CO_lcdm)
             + gaussian(lam, lam_NaI_obs, sigma_NaI, amp_NaI_lcdm)
             + minor_features(lam))

flux_itsm = (cont
             + gaussian(lam, lam_CO_obs,  sigma_CO,  amp_CO_itsm)
             + gaussian(lam, lam_NaI_obs, sigma_NaI, amp_NaI_itsm)
             + minor_features(lam))

# Add realistic noise to ITSM (mock observed)
rng = np.random.default_rng(42)
noise = rng.normal(0, 0.018, lam.shape)
flux_itsm_noisy = flux_itsm + noise

# ── Figure ────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7.5, 4.2))

# ΛCDM baseline
ax.plot(lam, flux_lcdm, color="black", lw=1.5, ls="--", zorder=3,
        label=r"$\Lambda$CDM baseline (predicted continuum + features)")

# ITSM noisy mock
ax.plot(lam, flux_itsm_noisy, color="#1f5fa6", lw=1.0, alpha=0.55,
        zorder=2, label=r"ITSM mock spectrum (+ NIRSpec noise)")

# ITSM noiseless prediction
ax.plot(lam, flux_itsm, color="#1f5fa6", lw=2.0, zorder=3,
        label=r"ITSM prediction (noiseless)")

# Shaded feature windows
ax.axvspan(lam_CO_obs - 0.6, lam_CO_obs + 0.6,
           color="#f5a623", alpha=0.12, zorder=1)
ax.axvspan(lam_NaI_obs - 0.5, lam_NaI_obs + 0.5,
           color="#7b2d8b", alpha=0.12, zorder=1)

# Feature labels
ax.axvline(lam_CO_obs,  color="#f5a623", lw=1.0, ls=":", zorder=4)
ax.axvline(lam_NaI_obs, color="#7b2d8b", lw=1.0, ls=":", zorder=4)
ax.text(lam_CO_obs + 0.1, 0.705,
        f"CO(3-2)\n$\\lambda_{{\\rm obs}}={lam_CO_obs:.1f}\\,\\mu$m\n15% suppression",
        fontsize=8, color="#b8741a", va="bottom")
ax.text(lam_NaI_obs + 0.1, 0.705,
        f"Na I D\n$\\lambda_{{\\rm obs}}={lam_NaI_obs:.1f}\\,\\mu$m\n20% suppression",
        fontsize=8, color="#7b2d8b", va="bottom")

# JWST NIRSpec grating coverage band
ax.axvspan(7.0, 12.0, color="#e8f5e9", alpha=0.20, zorder=0)
ax.axvspan(12.0, 17.5, color="#e3f2fd", alpha=0.20, zorder=0)
ax.text(9.5,  1.43, "NIRSpec G140M", fontsize=7.5, color="#2e7d32",
        ha="center", style="italic")
ax.text(14.75, 1.43, "NIRSpec G235M", fontsize=7.5, color="#1565c0",
        ha="center", style="italic")

# Info box
ax.text(0.97, 0.97,
        "$z = 14.0$ | NGC 4217 analog\nJWST NIRSpec G140M/G235M\n"
        r"$a_0(z{=}14) \approx 15\,a_0(z{=}0)$",
        transform=ax.transAxes, fontsize=8, va="top", ha="right",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  edgecolor="black", alpha=0.9))

ax.set_xlim(7.0, 17.5)
ax.set_ylim(0.68, 1.50)
ax.set_xlabel(r"Observed wavelength $\lambda_{\rm obs}$ ($\mu$m)")
ax.set_ylabel(r"Normalized flux $F_{\lambda} / F_0$")
ax.set_title(
    "Mock JWST NIRSpec Spectrum — ITSM Falsifiable Prediction (Illustrative)",
    fontsize=11, pad=8)
ax.legend(loc="upper left", fontsize=8.5)

plt.tight_layout()

out = Path(__file__).parent.parent / "Assets" / "Figures" / "itsm_mock_jwst_spectrum.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, bbox_inches="tight")
print(f"Saved: {out}")
print(f"CO(3-2) observed: {lam_CO_obs:.2f} microns")
print(f"Na I D observed:  {lam_NaI_obs:.2f} microns")
