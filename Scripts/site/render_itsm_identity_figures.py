#!/usr/bin/env python3
"""Render ITSM identity figures with documented flow directions.

Authority (Master Research Plan §2):
  - Open dual polarity: entropy (exhaust) / syntropy (intake)
  - Toroidal *circuit* geometry as identity intuition
  - Flat T^3 fundamental domain is a rectangular parallelepiped (NOT this doughnut)

This script draws the *embedded torus of revolution* as a **circuit schematic**
for recirculating flow (poloidal + toroidal directions). It must never be
captioned as flat T^3 (that category error is recovery ban B10).

Flow convention (matches Scripts/itsm_3d_toroidal_manifold.py + identity dual):
  - Poloidal (along minor circle, +φ): syntropic *intake* direction Q_syn
  - Toroidal (along major circle, +θ): circuit / entropy *exhaust* transport
    along the open loop (schematic dual polarity — not a Derived coefficient)

Outputs (site-ready dark aesthetic):
  docs/assets/web/hero_circuit_flow.png|.webp   (1920×1080)
  docs/assets/web/split_open_circuit.png|.webp  (1400×900)
  Assets/Figures/itsm_circuit_flow_identity.png (publication white optional)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "docs" / "assets" / "web"
FIG = REPO / "Assets" / "Figures"

# Torus parameters (dimensionless schematic)
R = 3.0  # major radius
r = 1.05  # minor radius

VOID = "#05060c"
GOLD = "#d4b06a"
ICE = "#8eb6ff"
EXHAUST = "#e07a5f"
INTAKE = "#6ec6ff"


def torus_surface(n_theta: int = 72, n_phi: int = 48):
    theta = np.linspace(0, 2 * np.pi, n_theta)
    phi = np.linspace(0, 2 * np.pi, n_phi)
    th, ph = np.meshgrid(theta, phi)
    x = (R + r * np.cos(ph)) * np.cos(th)
    y = (R + r * np.cos(ph)) * np.sin(th)
    z = r * np.sin(ph)
    return x, y, z


def point(theta: float, phi: float) -> np.ndarray:
    return np.array(
        [
            (R + r * np.cos(phi)) * np.cos(theta),
            (R + r * np.cos(phi)) * np.sin(theta),
            r * np.sin(phi),
        ]
    )


def e_poloidal(theta: float, phi: float) -> np.ndarray:
    """Unit vector in +φ (poloidal / minor-circle) direction — syntropy intake."""
    # ∂r/∂φ = (-r sinφ cosθ, -r sinφ sinθ, r cosφ)
    v = np.array(
        [
            -r * np.sin(phi) * np.cos(theta),
            -r * np.sin(phi) * np.sin(theta),
            r * np.cos(phi),
        ]
    )
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def e_toroidal(theta: float, phi: float) -> np.ndarray:
    """Unit vector in +θ (toroidal / major-circle) direction — circuit exhaust transport."""
    # ∂r/∂θ = (-(R+r cosφ) sinθ, (R+r cosφ) cosθ, 0)
    v = np.array(
        [
            -(R + r * np.cos(phi)) * np.sin(theta),
            (R + r * np.cos(phi)) * np.cos(theta),
            0.0,
        ]
    )
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def style_dark_3d(ax, elev: float = 22, azim: float = 38):
    ax.set_facecolor(VOID)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor((1, 1, 1, 0.08))
    ax.yaxis.pane.set_edgecolor((1, 1, 1, 0.08))
    ax.zaxis.pane.set_edgecolor((1, 1, 1, 0.08))
    ax.tick_params(colors="#6b7694", labelsize=8)
    ax.grid(False)
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-4.2, 4.2)
    ax.set_zlim(-2.2, 2.2)
    try:
        ax.set_box_aspect((1, 1, 0.55))
    except Exception:
        pass
    ax.view_init(elev=elev, azim=azim)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])


def draw_torus_with_flows(ax, dense: bool = True):
    x, y, z = torus_surface()
    ax.plot_surface(
        x,
        y,
        z,
        color="#1a2744",
        alpha=0.38,
        edgecolor="#4a5f8a",
        linewidth=0.15,
        rstride=2,
        cstride=2,
        shade=True,
    )

    # Highlight a few poloidal rings + one toroidal guide
    phi_ring = np.linspace(0, 2 * np.pi, 120)
    for th0 in (0.4, 2.1, 3.8, 5.2):
        pr = np.array([point(th0, p) for p in phi_ring])
        ax.plot(pr[:, 0], pr[:, 1], pr[:, 2], color=GOLD, lw=0.9, alpha=0.55)

    theta_guide = np.linspace(0, 2 * np.pi, 160)
    tg = np.array([point(t, 0.35) for t in theta_guide])
    ax.plot(tg[:, 0], tg[:, 1], tg[:, 2], color=EXHAUST, lw=1.4, alpha=0.85)

    # Sample arrows: poloidal (intake) and toroidal (exhaust circuit)
    n_u = 10 if dense else 7
    n_v = 6 if dense else 4
    for i, th in enumerate(np.linspace(0.15, 2 * np.pi - 0.15, n_u, endpoint=False)):
        for j, ph in enumerate(np.linspace(0.2, 2 * np.pi - 0.2, n_v, endpoint=False)):
            p = point(th, ph)
            # Poloidal / syntropy intake
            ep = e_poloidal(th, ph)
            ax.quiver(
                p[0],
                p[1],
                p[2],
                ep[0],
                ep[1],
                ep[2],
                length=0.55,
                color=INTAKE,
                normalize=True,
                arrow_length_ratio=0.35,
                linewidth=0.9,
                alpha=0.95,
            )
            # Toroidal / exhaust circuit (sparser)
            if j % 2 == 0:
                et = e_toroidal(th, ph)
                ax.quiver(
                    p[0],
                    p[1],
                    p[2],
                    et[0],
                    et[1],
                    et[2],
                    length=0.7,
                    color=EXHAUST,
                    normalize=True,
                    arrow_length_ratio=0.32,
                    linewidth=0.85,
                    alpha=0.9,
                )


def render_hero():
    """16:9 hero: circuit flow schematic for site background."""
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=VOID)
    ax = fig.add_axes([0.02, 0.04, 0.96, 0.9], projection="3d")
    style_dark_3d(ax, elev=24, azim=42)
    draw_torus_with_flows(ax, dense=True)

    # Title block in figure coordinates
    fig.text(
        0.04,
        0.94,
        "Open toroidal circuit (identity schematic)",
        color=GOLD,
        fontsize=18,
        fontweight="medium",
        fontfamily="serif",
    )
    fig.text(
        0.04,
        0.90,
        r"Poloidal $+\varphi$: syntropic intake $Q_{\mathrm{syn}}$  ·  "
        r"Toroidal $+\theta$: circuit / entropy exhaust transport  ·  "
        r"Not flat $T^{3}$ (see fundamental domain)",
        color="#9aa6c2",
        fontsize=11,
        fontfamily="sans-serif",
    )

    legend = [
        Line2D([0], [0], color=INTAKE, lw=2.5, label=r"Syntropy intake (poloidal $+\varphi$)"),
        Line2D([0], [0], color=EXHAUST, lw=2.5, label=r"Entropy / circuit (toroidal $+\theta$)"),
        Line2D([0], [0], color=GOLD, lw=1.5, label="Poloidal guide rings"),
    ]
    ax.legend(
        handles=legend,
        loc="upper right",
        facecolor="#0a0d18",
        edgecolor="#d4b06a55",
        labelcolor="#e8eefc",
        fontsize=10,
        framealpha=0.9,
    )

    WEB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    raw = WEB / "_hero_raw.png"
    fig.savefig(raw, dpi=100, facecolor=VOID)
    plt.close(fig)
    # ensure exact 1920×1080
    im = Image.open(raw).convert("RGB")
    im = im.resize((1920, 1080), Image.Resampling.LANCZOS)
    im.save(WEB / "hero_toroidal.png", "PNG", optimize=True)
    im.save(WEB / "hero_toroidal.webp", "WEBP", quality=85, method=6)
    im.save(FIG / "itsm_circuit_flow_identity.png", "PNG", optimize=True)
    raw.unlink(missing_ok=True)
    print("hero_toroidal 1920x1080 OK")


def render_pillars_split():
    """14:9 dual panel: open circuit + dual polarity labels for pillars section."""
    fig = plt.figure(figsize=(14, 9), dpi=100, facecolor=VOID)

    # Left: 3D circuit
    ax1 = fig.add_axes([0.03, 0.12, 0.52, 0.8], projection="3d")
    style_dark_3d(ax1, elev=20, azim=35)
    draw_torus_with_flows(ax1, dense=False)
    ax1.set_title(
        "Circuit geometry (embedded torus schematic)",
        color=GOLD,
        fontsize=13,
        pad=8,
        fontfamily="serif",
    )

    # Right: conceptual dual-polarity diagram
    ax2 = fig.add_axes([0.58, 0.14, 0.38, 0.72])
    ax2.set_facecolor(VOID)
    for spine in ax2.spines.values():
        spine.set_color("#2a3550")
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_title(
        "Open dual polarity (identity)",
        color=GOLD,
        fontsize=13,
        pad=10,
        fontfamily="serif",
    )

    # Reservoir box
    ax2.add_patch(
        plt.Rectangle((1.2, 7.2), 7.6, 1.8, fill=False, edgecolor=GOLD, lw=1.5, ls="--")
    )
    ax2.text(5, 8.1, "Reservoir $R$\n(total system conserved)", ha="center", va="center",
             color="#e8eefc", fontsize=11)

    # Plenum torus symbol
    ax2.add_patch(plt.Circle((5, 4.0), 1.6, fill=False, edgecolor="#8eb6ff", lw=2))
    ax2.add_patch(plt.Circle((5, 4.0), 0.7, fill=False, edgecolor="#4a5f8a", lw=1.2))
    ax2.text(5, 4.0, "Plenum\ncircuit", ha="center", va="center", color="#c5d6f5", fontsize=10)

    # Intake arrow (down into plenum) — syntropy
    ax2.annotate(
        "",
        xy=(3.2, 5.4),
        xytext=(2.5, 7.1),
        arrowprops=dict(arrowstyle="-|>", color=INTAKE, lw=2.2),
    )
    ax2.text(1.5, 6.2, r"$Q_{\mathrm{syn}}$" + "\nintake\n(syntropy)", color=INTAKE, fontsize=10)

    # Exhaust arrow (out of plenum)
    ax2.annotate(
        "",
        xy=(7.5, 7.1),
        xytext=(6.8, 5.4),
        arrowprops=dict(arrowstyle="-|>", color=EXHAUST, lw=2.2),
    )
    ax2.text(7.6, 6.0, "entropy\nexhaust", color=EXHAUST, fontsize=10)

    # Matter exchange
    ax2.add_patch(
        plt.Rectangle((3.5, 0.8), 3.0, 1.2, fill=False, edgecolor="#9aa6c2", lw=1.3)
    )
    ax2.text(5, 1.4, r"Matter $\Psi_m$" + "\n" + r"$Q_{\mathrm{mp}}$ local", ha="center",
             va="center", color="#9aa6c2", fontsize=10)
    ax2.annotate(
        "",
        xy=(5, 2.2),
        xytext=(5, 2.9),
        arrowprops=dict(arrowstyle="<|-|>", color="#9aa6c2", lw=1.6),
    )

    ax2.text(
        5,
        0.25,
        "Not a closed steam engine · total system conserved",
        ha="center",
        color="#6b7694",
        fontsize=9,
        style="italic",
    )

    fig.text(
        0.5,
        0.04,
        r"Identity schematic only — flow directions: poloidal $+\varphi$ intake, toroidal $+\theta$ circuit. "
        r"Not a Derived Wilson coefficient diagram. Flat $T^3$ is a rectangular domain (see TOP/P1).",
        ha="center",
        color="#6b7694",
        fontsize=9,
    )

    WEB.mkdir(parents=True, exist_ok=True)
    raw = WEB / "_split_raw.png"
    fig.savefig(raw, dpi=100, facecolor=VOID)
    plt.close(fig)
    im = Image.open(raw).convert("RGB")
    im = im.resize((1400, 900), Image.Resampling.LANCZOS)
    im.save(WEB / "split_open_circuit.png", "PNG", optimize=True)
    im.save(WEB / "split_open_circuit.webp", "WEBP", quality=85, method=6)
    # also alias for site index name
    im.save(WEB / "split_fluid.png", "PNG", optimize=True)
    im.save(WEB / "split_fluid.webp", "WEBP", quality=85, method=6)
    raw.unlink(missing_ok=True)
    print("split_open_circuit / split_fluid 1400x900 OK")


def main():
    print("Rendering identity figures with documented flow directions...")
    render_hero()
    render_pillars_split()
    print("Done. Wired outputs under docs/assets/web/")


if __name__ == "__main__":
    main()
