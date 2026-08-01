"""
ITSM — correct schematic of a flat 3-torus (T^3) fundamental domain.

A 3-torus is NOT the doughnut surface embedded in R^3 (that is T^2).
The standard presentation of flat T^3 is a rectangular (or cubic) parallelepiped
with opposite faces identified.  This script draws that cube with face-pairing
arrows and optional rectangular anisotropy.

Outputs:
  Assets/Figures/itsm_t3_fundamental_domain.png
  Assets/Figures/itsm_t3_fundamental_domain.pdf
"""

from __future__ import annotations

import os
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def _face(verts, idxs):
    return [verts[i] for i in idxs]


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

    # Corner vertices of the fundamental parallelepiped [0,Lx]x[0,Ly]x[0,Lz]
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

    # Six faces (for wireframe / light fill)
    faces = [
        _face(v, [0, 1, 2, 3]),  # bottom z=0
        _face(v, [4, 5, 6, 7]),  # top z=Lz
        _face(v, [0, 1, 5, 4]),  # y=0
        _face(v, [3, 2, 6, 7]),  # y=Ly
        _face(v, [0, 3, 7, 4]),  # x=0
        _face(v, [1, 2, 6, 5]),  # x=Lx
    ]

    fig = plt.figure(figsize=(8.2, 7.2))
    ax = fig.add_subplot(111, projection="3d")

    coll = Poly3DCollection(
        faces,
        alpha=0.12,
        facecolor="steelblue",
        edgecolor="0.25",
        linewidths=1.4,
    )
    ax.add_collection3d(coll)

    # Emphasize cube edges
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
        ax.plot(*zip(v[i], v[j]), color="0.15", lw=1.6)

    # Opposite-face identification arrows (three independent S^1 cycles)
    # Cycle 1: x-direction (faces x=0 <-> x=Lx)
    ax.quiver(
        0.0,
        0.5 * Ly,
        0.5 * Lz,
        Lx,
        0,
        0,
        color="#c0392b",
        arrow_length_ratio=0.08,
        lw=2.2,
        normalize=False,
    )
    ax.text(0.5 * Lx, 0.5 * Ly - 0.12 * max(Lx, Ly, Lz), 0.5 * Lz, r"$L_x$", color="#c0392b", fontsize=12)

    # Cycle 2: y-direction
    ax.quiver(
        0.5 * Lx,
        0.0,
        0.5 * Lz,
        0,
        Ly,
        0,
        color="#1e8449",
        arrow_length_ratio=0.08,
        lw=2.2,
        normalize=False,
    )
    ax.text(0.5 * Lx + 0.06 * Lx, 0.5 * Ly, 0.5 * Lz, r"$L_y$", color="#1e8449", fontsize=12)

    # Cycle 3: z-direction
    ax.quiver(
        0.5 * Lx,
        0.5 * Ly,
        0.0,
        0,
        0,
        Lz,
        color="#2471a3",
        arrow_length_ratio=0.08,
        lw=2.2,
        normalize=False,
    )
    ax.text(0.5 * Lx, 0.5 * Ly + 0.06 * Ly, 0.55 * Lz, r"$L_z$", color="#2471a3", fontsize=12)

    # Face-pairing labels
    ax.text(-0.08 * Lx, 0.5 * Ly, 0.5 * Lz, r"$A$", fontsize=11, ha="right")
    ax.text(Lx + 0.08 * Lx, 0.5 * Ly, 0.5 * Lz, r"$A'$", fontsize=11)
    ax.text(0.5 * Lx, -0.08 * Ly, 0.5 * Lz, r"$B$", fontsize=11, ha="center")
    ax.text(0.5 * Lx, Ly + 0.08 * Ly, 0.5 * Lz, r"$B'$", fontsize=11, ha="center")
    ax.text(0.5 * Lx, 0.5 * Ly, -0.1 * Lz, r"$C$", fontsize=11, ha="center")
    ax.text(0.5 * Lx, 0.5 * Ly, Lz + 0.08 * Lz, r"$C'$", fontsize=11, ha="center")

    # Non-contractible cycle example (midplane loop along x, closed by identification)
    t = np.linspace(0, Lx, 80)
    y0, z0 = 0.22 * Ly, 0.28 * Lz
    ax.plot(t, np.full_like(t, y0), np.full_like(t, z0), color="#8e44ad", lw=2.0, ls="--")
    ax.text(
        0.55 * Lx,
        y0 - 0.08 * Ly,
        z0,
        r"non-contractible cycle $\gamma_x$",
        color="#8e44ad",
        fontsize=9,
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
    ax.set_title(title, fontsize=11, pad=12)

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_zlabel(r"$z$")

    pad = 0.25 * max(Lx, Ly, Lz)
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
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.fill = False
        axis.pane.set_edgecolor("0.7")

    # Caption strip as figure text
    fig.text(
        0.5,
        0.02,
        r"Identifications: $A\sim A'$, $B\sim B'$, $C\sim C'$.  "
        r"Cubic: $L_x=L_y=L_z$.  Rectangular: independent $L_i$.",
        ha="center",
        fontsize=9,
        color="0.25",
    )

    for ext in ("png", "pdf"):
        path = os.path.join(out_dir, f"{out_stem}.{ext}")
        fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
        print(f"Wrote {path}")
    plt.close(fig)


def main() -> None:
    # Default: cubic domain (isotropic three-axis case used for a0 motivation)
    draw_t3_domain(1.0, 1.0, 1.0, out_stem="itsm_t3_fundamental_domain")
    # Also export a mildly rectangular example for companion Casimir paper
    draw_t3_domain(1.0, 1.15, 0.90, out_stem="itsm_t3_rectangular_domain")


if __name__ == "__main__":
    main()
