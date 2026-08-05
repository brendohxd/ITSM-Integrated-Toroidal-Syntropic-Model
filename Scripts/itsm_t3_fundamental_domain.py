"""
ITSM — correct schematic of a flat 3-torus (T^3) fundamental domain.

A 3-torus is NOT the doughnut surface embedded in R^3 (that is T^2).
The standard presentation of flat T^3 is a rectangular (or cubic) parallelepiped
with opposite faces identified.  This script draws that cube with face-pairing
arrows and optional rectangular anisotropy.

Outputs:
  Assets/Figures/itsm_t3_fundamental_domain.png
  Assets/Figures/itsm_t3_fundamental_domain.pdf
  papers/P1-Scale-Matching-Reconstruction/figures/ (copy of cubic PDF/PNG)
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import patheffects
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def _face(verts, idxs):
    return [verts[i] for i in idxs]


def _halo(lw: float = 3.5, color: str = "white"):
    return [patheffects.withStroke(linewidth=lw, foreground=color)]


def draw_t3_domain(
    Lx: float = 1.0,
    Ly: float = 1.0,
    Lz: float = 1.0,
    title: str | None = None,
    out_stem: str = "itsm_t3_fundamental_domain",
) -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    out_dir = os.path.join(repo_root, "Assets", "Figures")
    os.makedirs(out_dir, exist_ok=True)

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
        _face(v, [0, 1, 2, 3]),
        _face(v, [4, 5, 6, 7]),
        _face(v, [0, 1, 5, 4]),
        _face(v, [3, 2, 6, 7]),
        _face(v, [0, 3, 7, 4]),
        _face(v, [1, 2, 6, 5]),
    ]

    fig = plt.figure(figsize=(8.2, 7.2))
    ax = fig.add_subplot(111, projection="3d")

    coll = Poly3DCollection(
        faces,
        alpha=0.08,
        facecolor="#5dade2",
        edgecolor="0.2",
        linewidths=1.6,
    )
    ax.add_collection3d(coll)

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
    for i, j in edges:
        ax.plot(*zip(v[i], v[j]), color="0.1", lw=1.8, zorder=2)

    # Identification arrows (through-cube); labels OUTSIDE so they clear the fill
    ax.quiver(
        0.0,
        0.5 * Ly,
        0.5 * Lz,
        Lx,
        0,
        0,
        color="#922b21",
        arrow_length_ratio=0.08,
        lw=2.4,
        normalize=False,
        zorder=5,
    )
    ax.text(
        0.5 * Lx,
        -0.28 * Ly,
        0.35 * Lz,
        r"$L_x$",
        color="#922b21",
        fontsize=13,
        fontweight="bold",
        ha="center",
        path_effects=_halo(4),
        zorder=10,
    )

    ax.quiver(
        0.5 * Lx,
        0.0,
        0.5 * Lz,
        0,
        Ly,
        0,
        color="#145a32",
        arrow_length_ratio=0.08,
        lw=2.4,
        normalize=False,
        zorder=5,
    )
    ax.text(
        Lx + 0.22 * Lx,
        0.55 * Ly,
        0.62 * Lz,
        r"$L_y$",
        color="#145a32",
        fontsize=13,
        fontweight="bold",
        ha="left",
        path_effects=_halo(4),
        zorder=10,
    )

    ax.quiver(
        0.5 * Lx,
        0.5 * Ly,
        0.0,
        0,
        0,
        Lz,
        color="#1a5276",
        arrow_length_ratio=0.08,
        lw=2.4,
        normalize=False,
        zorder=5,
    )
    ax.text(
        0.5 * Lx,
        Ly + 0.14 * Ly,
        0.72 * Lz,
        r"$L_z$",
        color="#1a5276",
        fontsize=13,
        fontweight="bold",
        ha="center",
        path_effects=_halo(4),
        zorder=10,
    )

    # Face-pairing labels: black with white halo, outside faces
    face_kw = dict(fontsize=12, fontweight="bold", color="0.05", path_effects=_halo(4), zorder=10)
    ax.text(-0.12 * Lx, 0.5 * Ly, 0.5 * Lz, r"$A$", ha="right", va="center", **face_kw)
    ax.text(Lx + 0.12 * Lx, 0.5 * Ly, 0.5 * Lz, r"$A'$", ha="left", va="center", **face_kw)
    ax.text(0.5 * Lx, -0.14 * Ly, 0.15 * Lz, r"$B$", ha="center", va="top", **face_kw)
    ax.text(0.5 * Lx, Ly + 0.14 * Ly, 0.15 * Lz, r"$B'$", ha="center", va="bottom", **face_kw)
    ax.text(0.5 * Lx, 0.5 * Ly, -0.16 * Lz, r"$C$", ha="center", va="top", **face_kw)
    ax.text(0.5 * Lx, 0.5 * Ly, Lz + 0.14 * Lz, r"$C'$", ha="center", va="bottom", **face_kw)

    # Non-contractible cycle along x (dashed), label outside with halo + bbox
    t = np.linspace(0, Lx, 80)
    y0, z0 = 0.18 * Ly, 0.22 * Lz
    ax.plot(t, np.full_like(t, y0), np.full_like(t, z0), color="#6c3483", lw=2.4, ls="--", zorder=6)
    ax.text(
        0.52 * Lx,
        y0 - 0.22 * Ly,
        z0 - 0.05 * Lz,
        r"non-contractible cycle $\gamma_x$",
        color="#4a235a",
        fontsize=10,
        fontweight="bold",
        ha="center",
        path_effects=_halo(3.5),
        bbox=dict(
            boxstyle="round,pad=0.25",
            facecolor="white",
            edgecolor="#6c3483",
            alpha=0.92,
            linewidth=0.8,
        ),
        zorder=12,
    )

    if title is None:
        cubic = abs(Lx - Ly) < 1e-12 and abs(Ly - Lz) < 1e-12
        shape = "cubic" if cubic else "rectangular"
        title = (
            r"Flat $T^3$ fundamental domain ("
            + shape
            + r"): opposite faces identified"
            "\n"
            r"$T^3 \simeq \mathbb{R}^3 / \Lambda$  (not the doughnut surface $T^2 \subset \mathbb{R}^3$)"
        )
    ax.set_title(title, fontsize=11, pad=12, color="0.1")

    ax.set_xlabel(r"$x$", labelpad=6)
    ax.set_ylabel(r"$y$", labelpad=6)
    ax.set_zlabel(r"$z$", labelpad=6)

    pad = 0.32 * max(Lx, Ly, Lz)
    ax.set_xlim(-pad, Lx + pad)
    ax.set_ylim(-pad, Ly + pad)
    ax.set_zlim(-pad, Lz + pad)
    try:
        ax.set_box_aspect((Lx, Ly, Lz))
    except Exception:
        pass

    ax.view_init(elev=22, azim=-55)
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    # Soften / remove dense grid that washes out labels
    ax.grid(False)
    ax.xaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    ax.yaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    ax.zaxis._axinfo["grid"]["color"] = (1, 1, 1, 0)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.fill = False
        axis.pane.set_edgecolor("0.85")
        axis.pane.set_alpha(0.15)

    fig.text(
        0.5,
        0.02,
        r"Identifications: $A\sim A'$, $B\sim B'$, $C\sim C'$.  "
        r"Cubic: $L_x=L_y=L_z$.  Rectangular: independent $L_i$.",
        ha="center",
        fontsize=9,
        color="0.2",
    )

    for ext in ("png", "pdf"):
        path = os.path.join(out_dir, f"{out_stem}.{ext}")
        fig.savefig(path, dpi=400, bbox_inches="tight", facecolor="white")
        print(f"Wrote {path}")
    plt.close(fig)

    # Keep P1 paper figures/ in sync for the cubic domain
    if out_stem == "itsm_t3_fundamental_domain":
        p1_fig = Path(repo_root) / "papers" / "P1-Scale-Matching-Reconstruction" / "figures"
        p1_fig.mkdir(parents=True, exist_ok=True)
        for ext in ("png", "pdf"):
            src = Path(out_dir) / f"{out_stem}.{ext}"
            dst = p1_fig / f"{out_stem}.{ext}"
            shutil.copy2(src, dst)
            print(f"Copied {dst}")


def main() -> None:
    draw_t3_domain(1.0, 1.0, 1.0, out_stem="itsm_t3_fundamental_domain")
    draw_t3_domain(1.0, 1.15, 0.90, out_stem="itsm_t3_rectangular_domain")


if __name__ == "__main__":
    main()
