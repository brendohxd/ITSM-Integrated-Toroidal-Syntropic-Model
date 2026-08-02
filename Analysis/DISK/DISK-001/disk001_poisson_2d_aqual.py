#!/usr/bin/env python3
"""DISK-001 Stage 1: 2D nonlinear AQUAL Poisson (Picard + sparse linear solves).

Solves on a Cartesian domain (midplane model with vertical Gaussian thickness):

  ∇ · [ μ(|∇Φ|/a0_eff) ∇Φ ] = 4π G ρ

with μ(x)=x/√(1+x²), a0_eff=C_obs² a0 (declared Conditional IR), Dirichlet
Φ=Φ_N on the outer boundary (Newtonian multipole / free-space soft potential).

Peer-review diagnostics
-----------------------
1. Discrete PDE residual ||∇·(μ∇Φ) - 4πGρ|| / ||4πGρ|| after convergence.
2. Curl of g=-∇Φ (should be FD-noise for a potential field).
3. Resolution study: residual and probe |g| vs grid spacing.
4. Explicit contrast: algebraic AQUAL map on g_N is *not* the same object as
   this potential solution; curl of the algebraic map is reported separately.

This is a methods-grade Stage-1 solver, not a production galactic dynamics
pipeline and not a full DISK-001 PASS.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

from disk001_ir_law import (
    a0_effective,
    aqual_g_from_gN,
    default_conditional_ir,
    simple_mu_interpolating,
)

G_SPARC = 4.30091e-6


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--n-list",
        type=int,
        nargs="+",
        default=[33, 49, 65],
        help="Odd grid sizes for convergence study.",
    )
    p.add_argument("--half-box-kpc", type=float, default=10.0)
    p.add_argument("--mass", type=float, default=5.0e9, help="M_sun")
    p.add_argument("--rx-kpc", type=float, default=2.0, help="elliptical Gaussian σ_x")
    p.add_argument("--ry-kpc", type=float, default=1.0, help="elliptical Gaussian σ_y")
    p.add_argument("--picard-max", type=int, default=40)
    p.add_argument("--picard-tol", type=float, default=1e-8)
    return p.parse_args()


def density_field(X: np.ndarray, Y: np.ndarray, mass: float, sx: float, sy: float) -> np.ndarray:
    """Normalised elliptical Gaussian density (M_sun/kpc^3) as 2D midplane model."""
    amp = mass / (2.0 * np.pi * sx * sy)
    # Treat as surface density Σ for 2D Poisson: use Σ with 2D divergence
    # (units: we adopt 2D Poisson ∇·(μ∇Φ)=4πGΣ with Σ in M_sun/kpc²)
    sigma = amp * np.exp(-0.5 * ((X / sx) ** 2 + (Y / sy) ** 2))
    # amp above is for 3D-like; renormalise so ∫Σ dA = mass
    # amp_2d = mass/(2π sx sy) for Σ
    sigma = (mass / (2.0 * np.pi * sx * sy)) * np.exp(
        -0.5 * ((X / sx) ** 2 + (Y / sy) ** 2)
    )
    return sigma


def newtonian_soft_potential(
    X: np.ndarray, Y: np.ndarray, mass: float, soft: float
) -> np.ndarray:
    """Φ_N = -G M / sqrt(R²+ε²) (2D midplane soft monopole for BC)."""
    R = np.sqrt(X * X + Y * Y + soft * soft)
    return -G_SPARC * mass / R


def face_mu_from_phi(phi: np.ndarray, dx: float, dy: float, a0_eff: float) -> tuple[np.ndarray, np.ndarray]:
    """μ on x- and y-faces from cell-centred Φ (interior-sized arrays)."""
    # grad at cell centres
    dphidy, dphidx = np.gradient(phi, dy, dx)
    gmag = np.sqrt(dphidx**2 + dphidy**2)
    mu_c = simple_mu_interpolating(gmag / a0_eff)
    # face μ by averaging adjacent cells
    mu_x = 0.5 * (mu_c[:, 1:] + mu_c[:, :-1])  # between j and j+1
    mu_y = 0.5 * (mu_c[1:, :] + mu_c[:-1, :])  # between i and i+1
    return mu_x, mu_y


def assemble_operator(
    n: int,
    dx: float,
    dy: float,
    mu_x: np.ndarray,
    mu_y: np.ndarray,
    boundary_mask: np.ndarray,
) -> sparse.csr_matrix:
    """Discrete ∇·(μ ∇Φ) for interior unknowns; Dirichlet rows for boundary."""
    N = n * n
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []

    def idx(i: int, j: int) -> int:
        return i * n + j

    for i in range(n):
        for j in range(n):
            p = idx(i, j)
            if boundary_mask[i, j]:
                rows.append(p)
                cols.append(p)
                data.append(1.0)
                continue
            # five-point with face μ
            # x-faces: between (i,j-1)-(i,j) and (i,j)-(i,j+1)
            mx_r = mu_x[i, j]  # face j|j+1 → mu_x shape (n, n-1), index j
            mx_l = mu_x[i, j - 1]
            my_u = mu_y[i, j]  # face i|i+1 → mu_y shape (n-1, n)
            my_d = mu_y[i - 1, j]
            c_c = 0.0
            # ∂x (μ ∂x Φ) ≈ (μ_r (Φ_{j+1}-Φ_j) - μ_l (Φ_j-Φ_{j-1})) / dx²
            c_c += -(mx_r + mx_l) / (dx * dx)
            c_c += -(my_u + my_d) / (dy * dy)
            # neighbours
            for q, c in (
                (idx(i, j + 1), mx_r / (dx * dx)),
                (idx(i, j - 1), mx_l / (dx * dx)),
                (idx(i + 1, j), my_u / (dy * dy)),
                (idx(i - 1, j), my_d / (dy * dy)),
            ):
                rows.append(p)
                cols.append(q)
                data.append(c)
            rows.append(p)
            cols.append(p)
            data.append(c_c)
    return sparse.csr_matrix((data, (rows, cols)), shape=(N, N))


def pde_residual(
    phi: np.ndarray, sigma: np.ndarray, dx: float, dy: float, a0_eff: float
) -> float:
    """Relative RMS residual of ∇·(μ∇Φ) − 4πGΣ on the interior."""
    # arrays: axis0 ↔ y, axis1 ↔ x (meshgrid default indexing='xy')
    dphi_dy, dphi_dx = np.gradient(phi, dy, dx)
    gmag = np.sqrt(dphi_dx**2 + dphi_dy**2)
    mu = simple_mu_interpolating(gmag / a0_eff)
    Fx = mu * dphi_dx
    Fy = mu * dphi_dy
    _, dFx_dx = np.gradient(Fx, dy, dx)
    dFy_dy, _ = np.gradient(Fy, dy, dx)
    div = dFx_dx + dFy_dy
    rhs = 4.0 * np.pi * G_SPARC * sigma
    m = np.ones_like(div, dtype=bool)
    m[0, :] = m[-1, :] = m[:, 0] = m[:, -1] = False
    num = float(np.sqrt(np.mean((div[m] - rhs[m]) ** 2)))
    den = float(np.sqrt(np.mean(rhs[m] ** 2))) + 1e-30
    return num / den


def curl_z(gx: np.ndarray, gy: np.ndarray, dx: float, dy: float) -> np.ndarray:
    dgy_dy, dgy_dx = np.gradient(gy, dy, dx)
    dgx_dy, dgx_dx = np.gradient(gx, dy, dx)
    return dgy_dx - dgx_dy


def solve_aqual_2d(
    n: int,
    half_box: float,
    mass: float,
    sx: float,
    sy: float,
    ir,
    picard_max: int,
    picard_tol: float,
) -> dict:
    xs = np.linspace(-half_box, half_box, n)
    ys = np.linspace(-half_box, half_box, n)
    dx = xs[1] - xs[0]
    dy = ys[1] - ys[0]
    X, Y = np.meshgrid(xs, ys, indexing="xy")
    # indexing xy: X[i,j]=xs[j], Y[i,j]=ys[i] — wait meshgrid indexing='xy'
    # actually with indexing='xy', X.shape=(n,n) with X[row,col] - for 'xy'
    # X[i,j] varies with j. We'll use indexing='ij' for clarity: axis0=y? 
    # Use indexing='xy' consistently: row=y, col=x if we pass ys, xs...
    # Standard: X, Y = meshgrid(xs, ys) default indexing xy → X[j] varies,
    # Y shape (len(ys), len(xs)), Y[i,:] = ys[i].
    sigma = density_field(X, Y, mass, sx, sy)
    soft = 0.5 * min(sx, sy)
    phi_N = newtonian_soft_potential(X, Y, mass, soft)
    a0_eff = a0_effective(ir)

    # Initial guess: Newtonian
    phi = phi_N.copy()
    boundary = np.zeros((n, n), dtype=bool)
    boundary[0, :] = boundary[-1, :] = boundary[:, 0] = boundary[:, -1] = True

    history = []
    for it in range(picard_max):
        mu_x, mu_y = face_mu_from_phi(phi, dx, dy, a0_eff)
        A = assemble_operator(n, dx, dy, mu_x, mu_y, boundary)
        rhs = (4.0 * np.pi * G_SPARC * sigma).ravel()
        # Dirichlet BC
        bmask = boundary.ravel()
        rhs = rhs.copy()
        rhs[bmask] = phi_N.ravel()[bmask]
        phi_new = spsolve(A, rhs).reshape(n, n)
        delta = float(np.max(np.abs(phi_new - phi)))
        phi = phi_new
        res = pde_residual(phi, sigma, dx, dy, a0_eff)
        history.append({"iter": it, "max_dphi": delta, "rel_pde_residual": res})
        if delta < picard_tol * (float(np.max(np.abs(phi))) + 1e-30):
            break

    dphidy, dphidx = np.gradient(phi, dy, dx)
    gx, gy = -dphidx, -dphidy  # g = -∇Φ
    curl = curl_z(gx, gy, dx, dy)
    m = np.ones_like(curl, dtype=bool)
    m[2:-2, 2:-2] = True
    m &= (X**2 + Y**2) > (0.3 * min(sx, sy)) ** 2
    curl_rms = float(np.sqrt(np.mean(curl[m] ** 2)))
    g_rms = float(np.sqrt(np.mean((gx[m] ** 2 + gy[m] ** 2))))
    curl_rel = curl_rms / max(g_rms / dx, 1e-30)

    # Algebraic map on Newtonian g for contrast
    dphiN_dy, dphiN_dx = np.gradient(phi_N, dy, dx)
    gNx, gNy = -dphiN_dx, -dphiN_dy
    gx_a = np.zeros_like(gx)
    gy_a = np.zeros_like(gy)
    for i in range(n):
        for j in range(n):
            v = aqual_g_from_gN(np.array([gNx[i, j], gNy[i, j]]), ir)
            gx_a[i, j], gy_a[i, j] = v[0], v[1]
    curl_a = curl_z(gx_a, gy_a, dx, dy)
    curl_a_rms = float(np.sqrt(np.mean(curl_a[m] ** 2)))
    curl_a_rel = curl_a_rms / max(
        float(np.sqrt(np.mean(gx_a[m] ** 2 + gy_a[m] ** 2))) / dx, 1e-30
    )

    # Probe |g| at (sx, 0)
    j_p = int(np.argmin(np.abs(xs - sx)))
    i_p = int(np.argmin(np.abs(ys - 0.0)))
    g_probe = float(np.hypot(gx[i_p, j_p], gy[i_p, j_p]))

    return {
        "n": n,
        "dx": dx,
        "picard_iters": len(history),
        "final_max_dphi": history[-1]["max_dphi"],
        "rel_pde_residual": history[-1]["rel_pde_residual"],
        "curl_potential_rel": curl_rel,
        "curl_algebraic_map_rel": curl_a_rel,
        "g_probe": g_probe,
        "picard_history_tail": history[-3:],
    }


def main() -> None:
    args = parse_args()
    ir = default_conditional_ir()
    results = []
    for n in args.n_list:
        if n % 2 == 0:
            n += 1
        print(f"Solving n={n} ...")
        results.append(
            solve_aqual_2d(
                n,
                args.half_box_kpc,
                args.mass,
                args.rx_kpc,
                args.ry_kpc,
                ir,
                args.picard_max,
                args.picard_tol,
            )
        )
        print(
            f"  residual={results[-1]['rel_pde_residual']:.3e}  "
            f"curl_Φ={results[-1]['curl_potential_rel']:.3e}  "
            f"curl_alg={results[-1]['curl_algebraic_map_rel']:.3e}"
        )

    finest = results[-1]
    # Pass criteria (tier-1 methods bar for Stage 1 scaffold, not production):
    # - PDE residual < 5% on finest grid (2D FD + Picard is coarse but honest)
    # - potential curl ≪ O(1) (relative to g/dx)
    # - residual improves or stays controlled across refinement
    res_ok = finest["rel_pde_residual"] < 0.05
    curl_ok = finest["curl_potential_rel"] < 0.05
    residuals = [r["rel_pde_residual"] for r in results]
    # not required to be monotone if boundary layers dominate, but finest should
    # not be the worst by a large factor
    refine_ok = finest["rel_pde_residual"] <= 1.5 * min(residuals) + 1e-12
    passed = bool(res_ok and curl_ok and refine_ok)

    summary = {
        "gate": "DISK-001",
        "stage": "STAGE1_POISSON_2D_AQUAL",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": (
            "PASS_DISK001_2D_NONLINEAR_AQUAL_PICARD"
            if passed
            else "FAIL_DISK001_2D_NONLINEAR_AQUAL"
        ),
        "equation": "div(mu(|grad Phi|/a0_eff) grad Phi) = 4 pi G Sigma",
        "mu": "x/sqrt(1+x^2)",
        "ir": ir.to_dict(),
        "a0_eff": a0_effective(ir),
        "model": {
            "density": "elliptical_gaussian_surface_density",
            "mass_Msun": args.mass,
            "sigma_x_kpc": args.rx_kpc,
            "sigma_y_kpc": args.ry_kpc,
            "half_box_kpc": args.half_box_kpc,
            "bc": "Dirichlet Phi = soft Newtonian monopole on boundary",
        },
        "method": {
            "discretization": "cell-centred 5-point FD with face-averaged mu",
            "nonlinear": "Picard linearisation + scipy.sparse.linalg.spsolve",
            "picard_tol": args.picard_tol,
        },
        "convergence": results,
        "diagnostics": {
            "finest_rel_pde_residual": float(finest["rel_pde_residual"]),
            "finest_curl_potential_rel": float(finest["curl_potential_rel"]),
            "finest_curl_algebraic_map_rel": float(finest["curl_algebraic_map_rel"]),
            "res_ok": bool(res_ok),
            "curl_ok": bool(curl_ok),
            "refine_ok": bool(refine_ok),
        },
        "scientific_boundary": (
            "2D midplane nonlinear AQUAL Poisson with Picard FD method under "
            "declared Conditional IR. Dirichlet Newtonian soft BC; not a full "
            "3D disk, not SPARC fitting, not Derived C_obs. Algebraic AQUAL map "
            "is reported only as a contrast diagnostic (generally nonzero curl). "
            "Full DISK-001 PASS still requires stricter residual targets, 3D or "
            "axisymmetric R–z, and published convergence tables."
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "disk001_poisson_2d_aqual_summary.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"STATUS: {summary['subgate_status']}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
