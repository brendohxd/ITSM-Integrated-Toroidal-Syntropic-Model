#!/usr/bin/env python3
"""Purpose-built 4:3 dark gallery cards for itsm-cosmology.com homepage.

Outputs (exact 1200×900, black void, no CSS crop needed):
  docs/assets/web/card_wake.{png,webp}
  docs/assets/web/card_t3.{png,webp}
  docs/assets/web/card_phonon.{png,webp}

Content is schematic / identity-level (Master Plan §2), not Derived packaging.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "docs" / "assets" / "web"

VOID = "#05060c"
GOLD = "#d4b06a"
ICE = "#8eb6ff"
MUTED = "#9aa6c2"
W, H = 1200, 900  # 4:3 site cards


def save_fig(fig: plt.Figure, stem: str) -> None:
    WEB.mkdir(parents=True, exist_ok=True)
    raw = WEB / f"_{stem}_raw.png"
    fig.savefig(raw, dpi=100, facecolor=VOID, bbox_inches=None, pad_inches=0)
    plt.close(fig)
    im = Image.open(raw).convert("RGB")
    if im.size != (W, H):
        im = im.resize((W, H), Image.Resampling.LANCZOS)
    im.save(WEB / f"{stem}.png", "PNG", optimize=True)
    im.save(WEB / f"{stem}.webp", "WEBP", quality=86, method=6)
    raw.unlink(missing_ok=True)
    print(f"  {stem} {im.size} OK")


# ---------------------------------------------------------------------------
# Card 1 — Wake / continuous plenum drag (full field in frame)
# ---------------------------------------------------------------------------
def render_wake() -> None:
    # Domain chosen so streamlines + wake fully fit with margin
    x = np.linspace(-2.8, 6.2, 420)
    y = np.linspace(-3.4, 3.4, 360)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)
    R_yield = 1.0

    wake_mask = X > R_yield
    X_safe = np.clip(X, R_yield, None)
    wake_envelope = np.exp(-(Y**2) / (0.45 + 0.28 * X_safe)) * np.exp(
        -(X_safe - R_yield) / 5.5
    )
    k_ph = 3.6
    wake_osc = 0.5 * np.cos(k_ph * np.sqrt((X - R_yield) ** 2 + Y**2)) + 0.5
    base = 0.04 * np.exp(-R / 2.2)
    dens = base.copy()
    dens[wake_mask] += (wake_envelope * wake_osc * 0.42)[wake_mask]

    R_safe = np.where(R < 0.08, 0.08, R)
    U_inf = 1.0
    u = U_inf * (1 - (R_yield**2 / R_safe**2) * np.cos(2 * Theta))
    v = U_inf * (-(R_yield**2 / R_safe**2) * np.sin(2 * Theta))

    fig = plt.figure(figsize=(12, 9), dpi=100, facecolor=VOID)
    # Leave room for caption band inside image (not cut by CSS)
    ax = fig.add_axes([0.08, 0.14, 0.84, 0.78])
    ax.set_facecolor(VOID)

    cmap = mcolors.LinearSegmentedColormap.from_list(
        "wake", ["#05060c", "#0a1532", "#005f8e", "#00b4d8", "#a8f0ff"], N=256
    )
    ax.pcolormesh(X, Y, dens, cmap=cmap, shading="auto", vmin=0, vmax=0.48)
    ax.streamplot(
        X,
        Y,
        u,
        v,
        color=(1, 1, 1, 0.38),
        linewidth=0.7,
        density=1.15,
        arrowstyle="-|>",
        arrowsize=1.0,
    )
    ax.scatter([0], [0], c=GOLD, s=90, edgecolors="white", linewidths=0.8, zorder=5)
    ax.add_patch(
        Circle(
            (0, 0),
            R_yield,
            fill=False,
            ec="#ff4d6d",
            ls="--",
            lw=2.0,
            zorder=4,
        )
    )

    ax.set_xlim(-2.5, 5.8)
    ax.set_ylim(-3.1, 3.1)
    ax.set_aspect("equal")
    ax.tick_params(colors=MUTED, labelsize=9)
    for sp in ax.spines.values():
        sp.set_color("#2a3550")
    ax.set_xlabel(r"$x / r_{a_0}$", color=MUTED, fontsize=11)
    ax.set_ylabel(r"$y / r_{a_0}$", color=MUTED, fontsize=11)
    ax.set_title(
        "Continuous plenum drag / acoustic wake  (not collisionless halo DM)",
        color=GOLD,
        fontsize=13,
        pad=10,
        fontfamily="serif",
    )

    fig.text(
        0.5,
        0.045,
        r"Yellow: baryonic node · Dashed: yield boundary $g_N \sim a_0$ (schematic) · "
        r"Streamlines: continuous fluid response · Identity-level schematic (WAK-001)",
        ha="center",
        color=MUTED,
        fontsize=9,
    )
    save_fig(fig, "card_wake")


# ---------------------------------------------------------------------------
# Card 2 — Flat T^3 rectangular fundamental domain (dark)
# ---------------------------------------------------------------------------
def render_t3() -> None:
    Lx, Ly, Lz = 1.35, 1.0, 0.85  # rectangular (not cube)
    v = np.array(
        [
            [0, 0, 0],
            [Lx, 0, 0],
            [Lx, Ly, 0],
            [0, Ly, 0],
            [0, 0, Lz],
            [Lx, 0, Lz],
            [Lx, Ly, Lz],
            [0, Ly, Lz],
        ],
        dtype=float,
    )
    faces = [
        [v[i] for i in idxs]
        for idxs in (
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [3, 2, 6, 7],
            [0, 3, 7, 4],
            [1, 2, 6, 5],
        )
    ]
    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]

    fig = plt.figure(figsize=(12, 9), dpi=100, facecolor=VOID)
    ax = fig.add_axes([0.02, 0.12, 0.96, 0.78], projection="3d")
    ax.set_facecolor(VOID)

    coll = Poly3DCollection(
        faces,
        alpha=0.18,
        facecolor="#1a2744",
        edgecolor=ICE,
        linewidths=1.1,
    )
    ax.add_collection3d(coll)
    for i, j in edges:
        ax.plot(*zip(v[i], v[j]), color="#c5d6f5", lw=1.5, alpha=0.85)

    # Identification arrows
    ax.quiver(0, 0.5 * Ly, 0.5 * Lz, Lx, 0, 0, color="#ff6b6b", lw=2, arrow_length_ratio=0.08)
    ax.quiver(0.5 * Lx, 0, 0.5 * Lz, 0, Ly, 0, color="#7dcea0", lw=2, arrow_length_ratio=0.08)
    ax.quiver(0.5 * Lx, 0.5 * Ly, 0, 0, 0, Lz, color=ICE, lw=2, arrow_length_ratio=0.08)
    ax.text(0.5 * Lx, -0.12 * Ly, 0.5 * Lz, r"$L_x$", color="#ff6b6b", fontsize=12)
    ax.text(Lx + 0.05, 0.5 * Ly, 0.5 * Lz, r"$L_y$", color="#7dcea0", fontsize=12)
    ax.text(0.5 * Lx, Ly + 0.05, 0.45 * Lz, r"$L_z$", color=ICE, fontsize=12)

    ax.text(-0.1 * Lx, 0.5 * Ly, 0.5 * Lz, r"$A$", color=MUTED, fontsize=11, ha="right")
    ax.text(Lx + 0.08 * Lx, 0.5 * Ly, 0.5 * Lz, r"$A'$", color=MUTED, fontsize=11)
    ax.text(0.5 * Lx, -0.12 * Ly, 0.15 * Lz, r"$B$", color=MUTED, fontsize=11, ha="center")
    ax.text(0.5 * Lx, Ly + 0.1 * Ly, 0.15 * Lz, r"$B'$", color=MUTED, fontsize=11, ha="center")
    ax.text(0.15 * Lx, 0.15 * Ly, -0.12 * Lz, r"$C$", color=MUTED, fontsize=11)
    ax.text(0.15 * Lx, 0.15 * Ly, Lz + 0.08 * Lz, r"$C'$", color=MUTED, fontsize=11)

    # Non-contractible cycle
    t = np.linspace(0, Lx, 60)
    y0, z0 = 0.25 * Ly, 0.3 * Lz
    ax.plot(t, np.full_like(t, y0), np.full_like(t, z0), color=GOLD, lw=2.0, ls="--")
    ax.text(0.45 * Lx, y0 - 0.12 * Ly, z0, r"$\gamma_x$ non-contractible", color=GOLD, fontsize=9)

    pad = 0.35
    ax.set_xlim(-pad, Lx + pad)
    ax.set_ylim(-pad, Ly + pad)
    ax.set_zlim(-pad, Lz + pad)
    try:
        ax.set_box_aspect((Lx, Ly, Lz))
    except Exception:
        pass
    ax.view_init(elev=20, azim=-52)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.fill = False
        axis.pane.set_edgecolor((1, 1, 1, 0.06))
    ax.grid(False)

    fig.text(
        0.5,
        0.93,
        r"Flat $T^3$ fundamental domain — opposite faces identified  ($A\!\sim\!A'$, $B\!\sim\!B'$, $C\!\sim\!C'$)",
        ha="center",
        color=GOLD,
        fontsize=13,
        fontfamily="serif",
    )
    fig.text(
        0.5,
        0.04,
        r"Rectangular parallelepiped $\mathbb{R}^3/\Lambda$  ·  not the doughnut surface $T^2\subset\mathbb{R}^3$  ·  TOP-001 / P1 hygiene",
        ha="center",
        color=MUTED,
        fontsize=9,
    )
    save_fig(fig, "card_t3")


# ---------------------------------------------------------------------------
# Card 3 — IR phonon / force sector schematic dispersion (dark)
# ---------------------------------------------------------------------------
def render_phonon() -> None:
    """Schematic linear phonon branch + optional higher modes — identity UV≠IR."""
    k = np.linspace(0, 3.2, 400)
    c_s = 1.0
    omega = c_s * k  # linear acoustic branch (schematic)
    # soft UV completion sketch (not a Derived cutoff)
    omega_soft = c_s * k / np.sqrt(1 + (k / 2.4) ** 2)

    fig = plt.figure(figsize=(12, 9), dpi=100, facecolor=VOID)
    ax = fig.add_axes([0.12, 0.16, 0.78, 0.72])
    ax.set_facecolor(VOID)

    ax.plot(k, omega, color=ICE, lw=2.4, label=r"IR phonon $\omega \approx c_s k$ (schematic)")
    ax.plot(
        k,
        omega_soft,
        color=GOLD,
        lw=1.8,
        ls="--",
        label=r"Illustrative UV-softened branch (not a Derived cutoff)",
    )
    ax.axvspan(0, 1.1, color=ICE, alpha=0.06)
    ax.axvspan(2.0, 3.2, color=GOLD, alpha=0.05)
    ax.text(0.35, 2.55, "IR force\nsector", color=ICE, fontsize=11, ha="center")
    ax.text(2.55, 2.55, "UV condensate\n(separate sector)", color=GOLD, fontsize=11, ha="center")

    ax.set_xlim(0, 3.2)
    ax.set_ylim(0, 3.0)
    ax.set_xlabel(r"Wavenumber $k$ (schematic units)", color=MUTED, fontsize=12)
    ax.set_ylabel(r"Frequency $\omega$", color=MUTED, fontsize=12)
    ax.tick_params(colors=MUTED, labelsize=10)
    for sp in ax.spines.values():
        sp.set_color("#2a3550")
    ax.grid(True, color="#1e2840", ls=":", lw=0.8)
    ax.set_title(
        r"IR phonon / force sector  ·  UV condensate $\neq$ IR force  (Master Plan §3)",
        color=GOLD,
        fontsize=13,
        pad=12,
        fontfamily="serif",
    )
    ax.legend(
        loc="lower right",
        facecolor="#0a0d18",
        edgecolor="#d4b06a55",
        labelcolor="#e8eefc",
        fontsize=9,
    )
    fig.text(
        0.5,
        0.04,
        "Identity-level schematic only — not a fitted spectrum or Derived cutoff scale",
        ha="center",
        color=MUTED,
        fontsize=9,
    )
    save_fig(fig, "card_phonon")


def main() -> None:
    print("Rendering purpose-built 4:3 gallery cards (black void)...")
    render_wake()
    render_t3()
    render_phonon()
    print(f"Wrote cards to {WEB}")


if __name__ == "__main__":
    main()
