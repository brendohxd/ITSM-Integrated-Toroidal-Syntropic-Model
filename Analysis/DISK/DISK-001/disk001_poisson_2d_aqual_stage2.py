#!/usr/bin/env python3
"""DISK-001 Stage 2: referee-grade tightening of 2D nonlinear AQUAL Poisson.

Improvements over Stage 1
-------------------------
1. **Consistent 2D free-space Newtonian BC**
   For midplane surface density the linear Poisson problem is 2D:
     ∇²Φ_N = 4π G Σ
   Free-space Green function ∝ log R (not the 3D soft monopole used in Stage 1).
   BC: solve linear Newtonian problem with Dirichlet multipole
     Φ_N|∂Ω = 2 G M log(R / R_ref)  (with soft core), then use that Φ_N as
     outer Dirichlet data for nonlinear Picard (standard outer-match practice).

2. **Residual of the discrete operator**
   Stage 1 residual used np.gradient estimates, which need not match the FD
   stencil. Stage 2 residual is ||A[μ(Φ)] Φ − b|| / ||b|| using the *same*
   matrix as the linear solve (interior rows only).

3. **Domain / resolution**
   Larger box relative to source scales; higher odd grids; documented
   convergence table.

4. **Still Conditional IR only** — not Derived C_obs, not SPARC, not full PASS.

Pass criteria (Stage 2 methods bar)
-----------------------------------
- Finest discrete relative residual < 1e-3
- Potential curl rel < 1e-10 (potential structure)
- Residual decreases under refinement (finest < coarsest / 2 or monotone trend)
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
    p.add_argument("--n-list", type=int, nargs="+", default=[49, 73, 97, 129])
    p.add_argument(
        "--half-box-kpc",
        type=float,
        default=24.0,
        help="Half-box; should be ≫ source scales for BC quality.",
    )
    p.add_argument("--mass", type=float, default=5.0e9)
    p.add_argument("--rx-kpc", type=float, default=2.0)
    p.add_argument("--ry-kpc", type=float, default=1.0)
    p.add_argument("--picard-max", type=int, default=80)
    p.add_argument("--picard-tol", type=float, default=1e-10)
    p.add_argument("--omega", type=float, default=0.7, help="Picard under-relaxation")
    return p.parse_args()


def density_sigma(X: np.ndarray, Y: np.ndarray, mass: float, sx: float, sy: float) -> np.ndarray:
    return (mass / (2.0 * np.pi * sx * sy)) * np.exp(
        -0.5 * ((X / sx) ** 2 + (Y / sy) ** 2)
    )


def log_multipole_bc(
    X: np.ndarray, Y: np.ndarray, mass: float, soft: float, r_ref: float
) -> np.ndarray:
    """2D free-space monopole: Φ = 2 G M log(R_soft / R_ref)."""
    R = np.sqrt(X * X + Y * Y + soft * soft)
    return 2.0 * G_SPARC * mass * np.log(R / r_ref)


def face_mu(phi: np.ndarray, dx: float, dy: float, a0_eff: float) -> tuple[np.ndarray, np.ndarray]:
    dphi_dy, dphi_dx = np.gradient(phi, dy, dx)
    gmag = np.sqrt(dphi_dx**2 + dphi_dy**2)
    # Floor gradient to avoid μ→0 singularity far out with flat Φ
    gmag = np.maximum(gmag, 1e-12 * a0_eff)
    mu_c = simple_mu_interpolating(gmag / a0_eff)
    mu_x = 0.5 * (mu_c[:, 1:] + mu_c[:, :-1])
    mu_y = 0.5 * (mu_c[1:, :] + mu_c[:-1, :])
    return mu_x, mu_y


def assemble_div_mu_grad(
    n: int,
    dx: float,
    dy: float,
    mu_x: np.ndarray,
    mu_y: np.ndarray,
    boundary: np.ndarray,
) -> sparse.csr_matrix:
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []

    def idx(i: int, j: int) -> int:
        return i * n + j

    inv_dx2 = 1.0 / (dx * dx)
    inv_dy2 = 1.0 / (dy * dy)
    for i in range(n):
        for j in range(n):
            p = idx(i, j)
            if boundary[i, j]:
                rows.append(p)
                cols.append(p)
                data.append(1.0)
                continue
            mx_r = mu_x[i, j]
            mx_l = mu_x[i, j - 1]
            my_u = mu_y[i, j]
            my_d = mu_y[i - 1, j]
            c_c = -(mx_r + mx_l) * inv_dx2 - (my_u + my_d) * inv_dy2
            for q, c in (
                (idx(i, j + 1), mx_r * inv_dx2),
                (idx(i, j - 1), mx_l * inv_dx2),
                (idx(i + 1, j), my_u * inv_dy2),
                (idx(i - 1, j), my_d * inv_dy2),
            ):
                rows.append(p)
                cols.append(q)
                data.append(c)
            rows.append(p)
            cols.append(p)
            data.append(c_c)
    return sparse.csr_matrix((data, (rows, cols)), shape=(n * n, n * n))


def discrete_residual(
    A: sparse.csr_matrix,
    phi: np.ndarray,
    rhs: np.ndarray,
    interior: np.ndarray,
) -> float:
    """||Aφ − b||_2 / ||b||_2 on interior degrees of freedom."""
    r = A @ phi.ravel() - rhs
    m = interior.ravel()
    num = float(np.linalg.norm(r[m]))
    den = float(np.linalg.norm(rhs[m])) + 1e-30
    return num / den


def curl_rel(gx: np.ndarray, gy: np.ndarray, dx: float, dy: float, mask: np.ndarray) -> float:
    dgy_dy, dgy_dx = np.gradient(gy, dy, dx)
    dgx_dy, dgx_dx = np.gradient(gx, dy, dx)
    curl = dgy_dx - dgx_dy
    curl_rms = float(np.sqrt(np.mean(curl[mask] ** 2)))
    g_rms = float(np.sqrt(np.mean(gx[mask] ** 2 + gy[mask] ** 2)))
    return curl_rms / max(g_rms / max(dx, 1e-30), 1e-30)


def solve_newtonian(
    n: int, dx: float, dy: float, sigma: np.ndarray, phi_bc: np.ndarray, boundary: np.ndarray
) -> np.ndarray:
    """Linear Poisson ∇²Φ = 4πGΣ with Dirichlet BC."""
    mu_x = np.ones((n, n - 1))
    mu_y = np.ones((n - 1, n))
    A = assemble_div_mu_grad(n, dx, dy, mu_x, mu_y, boundary)
    rhs = (4.0 * np.pi * G_SPARC * sigma).ravel()
    bmask = boundary.ravel()
    rhs = rhs.copy()
    rhs[bmask] = phi_bc.ravel()[bmask]
    return spsolve(A, rhs).reshape(n, n)


def solve_one(
    n: int,
    half_box: float,
    mass: float,
    sx: float,
    sy: float,
    ir,
    picard_max: int,
    picard_tol: float,
    omega: float,
) -> dict:
    if n % 2 == 0:
        n += 1
    xs = np.linspace(-half_box, half_box, n)
    ys = np.linspace(-half_box, half_box, n)
    dx = float(xs[1] - xs[0])
    dy = float(ys[1] - ys[0])
    X, Y = np.meshgrid(xs, ys, indexing="xy")
    sigma = density_sigma(X, Y, mass, sx, sy)
    soft = 0.25 * min(sx, sy)
    r_ref = half_box
    phi_bc = log_multipole_bc(X, Y, mass, soft, r_ref)

    boundary = np.zeros((n, n), dtype=bool)
    boundary[0, :] = boundary[-1, :] = boundary[:, 0] = boundary[:, -1] = True
    interior = ~boundary

    # Newtonian start with same BC
    phi = solve_newtonian(n, dx, dy, sigma, phi_bc, boundary)
    a0_eff = a0_effective(ir)

    history = []
    last_A = None
    last_rhs = None
    for it in range(picard_max):
        mu_x, mu_y = face_mu(phi, dx, dy, a0_eff)
        # Floor face μ away from zero for matrix conditioning
        mu_x = np.maximum(mu_x, 1e-8)
        mu_y = np.maximum(mu_y, 1e-8)
        A = assemble_div_mu_grad(n, dx, dy, mu_x, mu_y, boundary)
        rhs = (4.0 * np.pi * G_SPARC * sigma).ravel().copy()
        rhs[boundary.ravel()] = phi_bc.ravel()[boundary.ravel()]
        phi_star = spsolve(A, rhs).reshape(n, n)
        phi_new = (1.0 - omega) * phi + omega * phi_star
        # Enforce BC exactly
        phi_new[boundary] = phi_bc[boundary]
        delta = float(np.max(np.abs(phi_new - phi)))
        phi = phi_new
        res = discrete_residual(A, phi, rhs, interior)
        history.append({"iter": it, "max_dphi": delta, "discrete_rel_residual": res})
        last_A, last_rhs = A, rhs
        scale = float(np.max(np.abs(phi))) + 1e-30
        if delta < picard_tol * scale and res < 1e-6:
            break

    assert last_A is not None and last_rhs is not None
    # Final residual with μ frozen at solution
    mu_x, mu_y = face_mu(phi, dx, dy, a0_eff)
    mu_x = np.maximum(mu_x, 1e-8)
    mu_y = np.maximum(mu_y, 1e-8)
    A = assemble_div_mu_grad(n, dx, dy, mu_x, mu_y, boundary)
    rhs = (4.0 * np.pi * G_SPARC * sigma).ravel().copy()
    rhs[boundary.ravel()] = phi_bc.ravel()[boundary.ravel()]
    res = discrete_residual(A, phi, rhs, interior)

    dphi_dy, dphi_dx = np.gradient(phi, dy, dx)
    gx, gy = -dphi_dx, -dphi_dy
    mask = interior.copy()
    mask[1:3, :] = mask[-3:-1, :] = mask[:, 1:3] = mask[:, -3:-1] = False
    mask &= (X**2 + Y**2) > (0.5 * min(sx, sy)) ** 2
    c_rel = curl_rel(gx, gy, dx, dy, mask)

    # Algebraic map contrast on Newtonian field
    dN_dy, dN_dx = np.gradient(
        solve_newtonian(n, dx, dy, sigma, phi_bc, boundary), dy, dx
    )
    gNx, gNy = -dN_dx, -dN_dy
    gx_a = np.zeros_like(gx)
    gy_a = np.zeros_like(gy)
    for i in range(n):
        for j in range(n):
            v = aqual_g_from_gN(np.array([gNx[i, j], gNy[i, j]]), ir)
            gx_a[i, j] = v[0]
            gy_a[i, j] = v[1]
    c_alg = curl_rel(gx_a, gy_a, dx, dy, mask)

    j_p = int(np.argmin(np.abs(xs - sx)))
    i_p = int(np.argmin(np.abs(ys - 0.0)))
    g_probe = float(np.hypot(gx[i_p, j_p], gy[i_p, j_p]))

    return {
        "n": int(n),
        "dx": dx,
        "half_box_kpc": half_box,
        "picard_iters": len(history),
        "final_max_dphi": history[-1]["max_dphi"],
        "discrete_rel_residual": res,
        "curl_potential_rel": c_rel,
        "curl_algebraic_map_rel": c_alg,
        "g_probe": g_probe,
        "history_tail": history[-3:],
    }


def main() -> None:
    args = parse_args()
    ir = default_conditional_ir()
    results = []
    for n in args.n_list:
        print(f"Stage2 solve n={n} box=±{args.half_box_kpc} ...")
        row = solve_one(
            n,
            args.half_box_kpc,
            args.mass,
            args.rx_kpc,
            args.ry_kpc,
            ir,
            args.picard_max,
            args.picard_tol,
            args.omega,
        )
        results.append(row)
        print(
            f"  res={row['discrete_rel_residual']:.3e}  "
            f"curl_phi={row['curl_potential_rel']:.3e}  "
            f"curl_alg={row['curl_algebraic_map_rel']:.3e}  "
            f"iters={row['picard_iters']}"
        )

    finest = results[-1]
    coarsest = results[0]
    residuals = [r["discrete_rel_residual"] for r in results]
    res_ok = finest["discrete_rel_residual"] < 1e-3
    all_res_ok = all(r < 1e-3 for r in residuals)
    curl_ok = finest["curl_potential_rel"] < 1e-10
    # Refinement: either residual improves, or all grids already at solver floor
    floor = 1e-8
    at_floor = all(r < floor for r in residuals)
    improve = finest["discrete_rel_residual"] <= 0.5 * coarsest[
        "discrete_rel_residual"
    ] + 1e-15
    improve = improve or (
        finest["discrete_rel_residual"] < coarsest["discrete_rel_residual"] / 3.0
    )
    refine_ok = bool(improve or at_floor)
    passed = bool(res_ok and all_res_ok and curl_ok and refine_ok)

    summary = {
        "gate": "DISK-001",
        "stage": "STAGE2_POISSON_2D_AQUAL_TIGHT",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": (
            "PASS_DISK001_2D_AQUAL_STAGE2_RESIDUAL_BC"
            if passed
            else "FAIL_DISK001_2D_AQUAL_STAGE2"
        ),
        "equation": "div(mu(|grad Phi|/a0_eff) grad Phi) = 4 pi G Sigma",
        "bc": "Dirichlet from 2D log multipole on outer boundary; Newtonian start",
        "residual_definition": (
            "||A[mu(Phi)] Phi - b||_2 / ||b||_2 on interior DOFs "
            "(same discrete operator as the linear solve)"
        ),
        "ir": ir.to_dict(),
        "a0_eff": a0_effective(ir),
        "model": {
            "density": "elliptical_gaussian_Sigma",
            "mass_Msun": args.mass,
            "sigma_x_kpc": args.rx_kpc,
            "sigma_y_kpc": args.ry_kpc,
            "half_box_kpc": args.half_box_kpc,
        },
        "method": {
            "nonlinear": "under-relaxed Picard + sparse direct solve",
            "omega": args.omega,
            "picard_tol": args.picard_tol,
        },
        "pass_criteria": {
            "finest_discrete_rel_residual_lt": 1e-3,
            "curl_potential_rel_lt": 1e-10,
            "residual_improves_vs_coarsest": True,
        },
        "convergence": results,
        "diagnostics": {
            "finest_discrete_rel_residual": float(finest["discrete_rel_residual"]),
            "finest_curl_potential_rel": float(finest["curl_potential_rel"]),
            "coarsest_discrete_rel_residual": float(coarsest["discrete_rel_residual"]),
            "all_grids_residual_lt_1e-3": bool(all_res_ok),
            "all_grids_at_solver_floor_1e-8": bool(at_floor),
            "res_ok": bool(res_ok),
            "curl_ok": bool(curl_ok),
            "refine_ok": bool(refine_ok),
        },
        "scientific_boundary": (
            "Stage-2 methods tightening for 2D midplane Conditional AQUAL. "
            "Not 3D/R–z, not SPARC, not Derived C_obs, not full DISK-001 PASS. "
            "2D log BC is the correct free-space monopole for planar Poisson; "
            "higher multipoles of the elliptical source are not matched on ∂Ω."
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "next_required_calculation": [
            "Axisymmetric R–z nonlinear AQUAL",
            "Multipole BC expansion beyond monopole",
            "DISK-001_GATE_REPORT when full pass criteria met",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    path = args.output_dir / "disk001_poisson_2d_aqual_stage2_summary.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    # CSV convergence table for methods appendix
    import csv

    csv_path = args.output_dir / "disk001_stage2_convergence.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "n",
                "dx",
                "discrete_rel_residual",
                "curl_potential_rel",
                "curl_algebraic_map_rel",
                "picard_iters",
                "g_probe",
            ],
        )
        w.writeheader()
        for row in results:
            w.writerow({k: row[k] for k in w.fieldnames})

    print(f"STATUS: {summary['subgate_status']}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
