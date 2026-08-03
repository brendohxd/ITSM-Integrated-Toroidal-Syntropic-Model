#!/usr/bin/env python3
"""DISK-001 Stage 3: axisymmetric (R,z) nonlinear AQUAL Poisson.

Equation (axisymmetric cylindrical, no φ dependence)
----------------------------------------------------
  (1/R) ∂_R [ R μ(|∇Φ|/a0_eff) ∂_R Φ ]
  +     ∂_z [   μ(|∇Φ|/a0_eff) ∂_z Φ ]  = 4π G ρ

with μ(x)=x/√(1+x²), a0_eff = C_obs² a0 (declared Conditional IR).

Discretisation
--------------
Cell-centred Φ on a half-plane grid R∈[0,Rmax], z∈[-Zmax,Zmax].
Face-centred μ; 5-point divergence form with geometric R weights.
Axis R=0: regularity ∂_R Φ = 0 (mirror / one-sided Neumann row).
Outer boundary: Dirichlet from 3D soft Newtonian monopole
  Φ = -G M / sqrt(R²+z²+ε²)  (correct free-space monopole in 3D).

Nonlinear solver: under-relaxed Picard + sparse direct solve; residual is
||A[μ(Φ)] Φ − b|| / ||b|| on interior DOFs (same A as the linear step).

Peer-review status
------------------
Methods package under Conditional IR. Not SPARC fitting, not Derived C_obs,
not full DISK-001 PASS (would still want multipole BC, thicker tests, paper table).
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

from disk001_ir_law import a0_effective, default_conditional_ir, simple_mu_interpolating

G_SPARC = 4.30091e-6  # kpc (km/s)^2 / M_sun


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--n-list",
        type=int,
        nargs="+",
        default=[33, 49, 65],
        help="Radial cells (nr); nz = 2*(nr//2)+1 odd vertical cells.",
    )
    p.add_argument("--Rmax", type=float, default=20.0)
    p.add_argument("--Zmax", type=float, default=8.0)
    p.add_argument("--mass", type=float, default=5.0e9)
    p.add_argument("--Rd", type=float, default=3.0, help="radial disk scale kpc")
    p.add_argument("--zd", type=float, default=0.3, help="vertical sech^2 scale kpc")
    p.add_argument("--picard-max", type=int, default=60)
    p.add_argument("--picard-tol", type=float, default=1e-10)
    p.add_argument("--omega", type=float, default=0.65)
    return p.parse_args()


def double_exp_disk_density(
    R: np.ndarray, z: np.ndarray, mass: float, Rd: float, zd: float
) -> np.ndarray:
    """ρ(R,z) ∝ e^{-R/Rd} sech²(z/(2 zd)) normalised to total mass M.

    Analytic integral: ∫ e^{-R/Rd} 2π R dR = 2π Rd²,
    ∫ sech²(z/(2zd)) dz = 4 zd.
    So ∫ ρ dV = A * 2π Rd² * 4 zd = M ⇒ A = M / (8π Rd² zd).
    """
    A = mass / (8.0 * np.pi * Rd**2 * zd)
    return A * np.exp(-R / Rd) * (1.0 / np.cosh(z / (2.0 * zd))) ** 2


def soft_newtonian_3d(R: np.ndarray, z: np.ndarray, mass: float, soft: float) -> np.ndarray:
    return -G_SPARC * mass / np.sqrt(R * R + z * z + soft * soft)


def gradients_rz(phi: np.ndarray, dR: float, dz: float) -> tuple[np.ndarray, np.ndarray]:
    """∂Φ/∂z (axis0), ∂Φ/∂R (axis1) with arrays shaped (nz, nr)."""
    dphi_dz, dphi_dR = np.gradient(phi, dz, dR)
    return dphi_dR, dphi_dz


def face_mu_rz(
    phi: np.ndarray, dR: float, dz: float, a0_eff: float
) -> tuple[np.ndarray, np.ndarray]:
    dR_phi, dz_phi = gradients_rz(phi, dR, dz)
    gmag = np.sqrt(dR_phi**2 + dz_phi**2)
    gmag = np.maximum(gmag, 1e-12 * a0_eff)
    mu_c = simple_mu_interpolating(gmag / a0_eff)
    # faces: R-direction between j and j+1 → shape (nz, nr-1)
    mu_R = 0.5 * (mu_c[:, 1:] + mu_c[:, :-1])
    # z-direction between i and i+1 → shape (nz-1, nr)
    mu_z = 0.5 * (mu_c[1:, :] + mu_c[:-1, :])
    return mu_R, mu_z


def assemble_rz_operator(
    nr: int,
    nz: int,
    R: np.ndarray,
    dR: float,
    dz: float,
    mu_R: np.ndarray,
    mu_z: np.ndarray,
    boundary: np.ndarray,
) -> sparse.csr_matrix:
    """Discrete axisymmetric ∇·(μ∇Φ) with geometric R weights.

    Interior: for cell (i,j) with radius R_j > 0,
      (1/R_j) * [ R_{j+1/2} μ_R (Φ_{j+1}-Φ_j)/dR
                - R_{j-1/2} μ_R (Φ_j-Φ_{j-1})/dR ] / dR
      + [ μ_z (Φ_{i+1}-Φ_i)/dz - μ_z (Φ_i-Φ_{i-1})/dz ] / dz
    """
    n = nr * nz
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []

    def idx(i: int, j: int) -> int:
        return i * nr + j

    inv_dR = 1.0 / dR
    inv_dz = 1.0 / dz
    inv_dR2 = inv_dR * inv_dR
    inv_dz2 = inv_dz * inv_dz

    # face radii
    R_face = 0.5 * (R[1:] + R[:-1])  # length nr-1, between j and j+1

    for i in range(nz):
        for j in range(nr):
            p = idx(i, j)
            if boundary[i, j]:
                rows.append(p)
                cols.append(p)
                data.append(1.0)
                continue

            Rj = float(R[j])
            # R faces: between j-1|j and j|j+1
            m_rp = mu_R[i, j] if j < nr - 1 else mu_R[i, j - 1]
            # Inner face at j=0: mirror Neumann ⇒ flux through R=0 vanishes;
            # use R_rm → 0, and only the outer radial face contributes, with
            # doubled weight equivalent to Φ_{-1}=Φ_0 (zero gradient across axis).
            if j == 0:
                R_rp = 0.5 * (R[0] + R[1])
                m_rp = mu_R[i, 0]
                coef_p = (R_rp * m_rp) / (Rj * dR * dR)
                coef_m = 0.0
                c_c = -coef_p
                terms = [(idx(i, j + 1), coef_p)]
            else:
                m_rm = mu_R[i, j - 1]
                R_rp = R_face[j] if j < nr - 1 else R[j] + 0.5 * dR
                R_rm = R_face[j - 1]
                if j == nr - 1:
                    # boundary cell handled above
                    R_rp = R[j] + 0.5 * dR
                coef_p = (R_rp * m_rp) / (Rj * dR * dR) if j < nr - 1 else 0.0
                coef_m = (R_rm * m_rm) / (Rj * dR * dR)
                c_c = -(coef_p + coef_m)
                terms = []
                if j < nr - 1:
                    terms.append((idx(i, j + 1), coef_p))
                terms.append((idx(i, j - 1), coef_m))

            if i + 1 < nz:
                mz_u = mu_z[i, j]
                c_c -= mz_u * inv_dz2
                terms.append((idx(i + 1, j), mz_u * inv_dz2))
            if i - 1 >= 0:
                mz_d = mu_z[i - 1, j]
                c_c -= mz_d * inv_dz2
                terms.append((idx(i - 1, j), mz_d * inv_dz2))

            rows.append(p)
            cols.append(p)
            data.append(c_c)
            for q, c in terms:
                rows.append(p)
                cols.append(q)
                data.append(c)

    return sparse.csr_matrix((data, (rows, cols)), shape=(n, n))


def discrete_residual(
    A: sparse.csr_matrix, phi: np.ndarray, rhs: np.ndarray, interior: np.ndarray
) -> float:
    r = A @ phi.ravel() - rhs
    m = interior.ravel()
    return float(np.linalg.norm(r[m]) / (np.linalg.norm(rhs[m]) + 1e-30))


def solve_linear(
    nr: int,
    nz: int,
    R: np.ndarray,
    dR: float,
    dz: float,
    rho: np.ndarray,
    phi_bc: np.ndarray,
    boundary: np.ndarray,
    mu_R: np.ndarray | None = None,
    mu_z: np.ndarray | None = None,
) -> tuple[np.ndarray, sparse.csr_matrix, np.ndarray]:
    if mu_R is None:
        mu_R = np.ones((nz, nr - 1))
        mu_z = np.ones((nz - 1, nr))
    assert mu_z is not None
    A = assemble_rz_operator(nr, nz, R, dR, dz, mu_R, mu_z, boundary)
    rhs = (4.0 * np.pi * G_SPARC * rho).ravel().copy()
    bmask = boundary.ravel()
    rhs[bmask] = phi_bc.ravel()[bmask]
    phi = spsolve(A, rhs).reshape(nz, nr)
    return phi, A, rhs


def solve_one(
    nr: int,
    Rmax: float,
    Zmax: float,
    mass: float,
    Rd: float,
    zd: float,
    ir,
    picard_max: int,
    picard_tol: float,
    omega: float,
) -> dict:
    # Half-integer radial cells: R_j = (j+1/2) dR ∈ (0, Rmax), avoids R=0 centre.
    # Axis regularity: Neumann by mirroring across R=0 (special stencil at j=0).
    nz = 2 * (nr // 2) + 1  # odd
    if nr < 8 or nz < 8:
        raise ValueError("grid too small")
    dR = Rmax / nr
    R = (np.arange(nr) + 0.5) * dR
    z = np.linspace(-Zmax, Zmax, nz)
    dz = float(z[1] - z[0])
    RR, ZZ = np.meshgrid(R, z, indexing="xy")

    rho = double_exp_disk_density(RR, ZZ, mass, Rd, zd)
    soft = 0.25 * zd
    phi_bc_field = soft_newtonian_3d(RR, ZZ, mass, soft)

    boundary = np.zeros((nz, nr), dtype=bool)
    boundary[0, :] = boundary[-1, :] = True  # z outer
    boundary[:, -1] = True  # R outer
    interior = ~boundary

    phi, _, _ = solve_linear(nr, nz, R, dR, dz, rho, phi_bc_field, boundary)
    a0_eff = a0_effective(ir)
    history = []

    for it in range(picard_max):
        mu_R, mu_z = face_mu_rz(phi, dR, dz, a0_eff)
        mu_R = np.maximum(mu_R, 1e-8)
        mu_z = np.maximum(mu_z, 1e-8)
        phi_star, A, rhs = solve_linear(
            nr, nz, R, dR, dz, rho, phi_bc_field, boundary, mu_R, mu_z
        )
        phi_new = (1.0 - omega) * phi + omega * phi_star
        phi_new[boundary] = phi_bc_field[boundary]
        delta = float(np.max(np.abs(phi_new - phi)))
        phi = phi_new
        res = discrete_residual(A, phi, rhs, interior)
        history.append({"iter": it, "max_dphi": delta, "discrete_rel_residual": res})
        if delta < picard_tol * (float(np.max(np.abs(phi))) + 1e-30) and res < 1e-6:
            break

    mu_R, mu_z = face_mu_rz(phi, dR, dz, a0_eff)
    mu_R = np.maximum(mu_R, 1e-8)
    mu_z = np.maximum(mu_z, 1e-8)
    A = assemble_rz_operator(nr, nz, R, dR, dz, mu_R, mu_z, boundary)
    rhs = (4.0 * np.pi * G_SPARC * rho).ravel().copy()
    rhs[boundary.ravel()] = phi_bc_field.ravel()[boundary.ravel()]
    res = discrete_residual(A, phi, rhs, interior)

    dR_phi, dz_phi = gradients_rz(phi, dR, dz)
    gR, gz = -dR_phi, -dz_phi
    i0 = int(np.argmin(np.abs(z)))
    g_mid = np.sqrt(gR[i0, :] ** 2 + gz[i0, :] ** 2)
    # Axis regularity: even extension in R ⇒ (Φ_{j=1}-Φ_{j=0})/dR → 0 as dR→0
    # for smooth solutions (leading Φ ~ a(z) R^2 near axis).
    dphi_dR_inner = (phi[:, 1] - phi[:, 0]) / dR
    g_char = float(np.max(g_mid)) + 1e-30
    axis_ok_metric = float(np.sqrt(np.mean(dphi_dR_inner**2))) / g_char

    j_p = int(np.argmin(np.abs(R - Rd)))
    g_probe = float(g_mid[j_p])

    return {
        "nr": int(nr),
        "nz": int(nz),
        "dR": dR,
        "dz": dz,
        "R_inner": float(R[0]),
        "picard_iters": len(history),
        "discrete_rel_residual": res,
        "final_max_dphi": history[-1]["max_dphi"] if history else float("nan"),
        "axis_dphi_dR_rms_over_g_char": axis_ok_metric,
        "g_probe_midplane_R_eq_Rd": g_probe,
        "history_tail": history[-3:],
    }


def main() -> None:
    args = parse_args()
    ir = default_conditional_ir()
    results = []
    for nr in args.n_list:
        print(f"R–z solve nr={nr} Rmax={args.Rmax} Zmax={args.Zmax} ...")
        row = solve_one(
            nr,
            args.Rmax,
            args.Zmax,
            args.mass,
            args.Rd,
            args.zd,
            ir,
            args.picard_max,
            args.picard_tol,
            args.omega,
        )
        results.append(row)
        print(
            f"  res={row['discrete_rel_residual']:.3e}  "
            f"axis_dphi_dR={row['axis_dphi_dR_rms_over_g_char']:.3e}  "
            f"iters={row['picard_iters']}"
        )

    finest = results[-1]
    coarsest = results[0]
    residuals = [r["discrete_rel_residual"] for r in results]
    axis_vals = [r["axis_dphi_dR_rms_over_g_char"] for r in results]
    res_ok = finest["discrete_rel_residual"] < 1e-3
    all_ok = all(r < 5e-3 for r in residuals)
    # Axis FD slope residual should be modest; preferably non-increasing with n
    axis_ok = finest["axis_dphi_dR_rms_over_g_char"] < 0.15
    axis_improves = axis_vals[-1] <= axis_vals[0] * 1.05
    floor = all(r < 1e-7 for r in residuals)
    improve = finest["discrete_rel_residual"] <= coarsest["discrete_rel_residual"] + 1e-15
    refine_ok = bool(improve or floor or finest["discrete_rel_residual"] < 1e-6)
    passed = bool(res_ok and all_ok and axis_ok and refine_ok)

    summary = {
        "gate": "DISK-001",
        "stage": "STAGE3_POISSON_RZ_AQUAL",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": (
            "PASS_DISK001_RZ_NONLINEAR_AQUAL"
            if passed
            else "FAIL_DISK001_RZ_NONLINEAR_AQUAL"
        ),
        "equation": (
            "(1/R) d_R [R mu d_R Phi] + d_z [mu d_z Phi] = 4 pi G rho"
        ),
        "coordinates": "axisymmetric cylindrical (R,z)",
        "bc": {
            "axis_R0": "Neumann regularity d_R Phi = 0",
            "outer": "Dirichlet 3D soft Newtonian monopole",
        },
        "residual_definition": (
            "||A[mu(Phi)] Phi - b||_2 / ||b||_2 interior DOFs, same A as solve"
        ),
        "ir": ir.to_dict(),
        "a0_eff": a0_effective(ir),
        "model": {
            "density": "exp(-R/Rd) sech^2(z/(2 zd))",
            "mass_Msun": args.mass,
            "Rd_kpc": args.Rd,
            "zd_kpc": args.zd,
            "Rmax": args.Rmax,
            "Zmax": args.Zmax,
        },
        "method": {
            "nonlinear": "under-relaxed Picard + sparse direct",
            "omega": args.omega,
            "picard_tol": args.picard_tol,
        },
        "pass_criteria": {
            "finest_discrete_rel_residual_lt": 1e-3,
            "axis_dphi_dR_rms_over_g_char_lt": 0.15,
        },
        "convergence": results,
        "diagnostics": {
            "finest_discrete_rel_residual": float(finest["discrete_rel_residual"]),
            "finest_axis_dphi_dR_rms_over_g_char": float(
                finest["axis_dphi_dR_rms_over_g_char"]
            ),
            "axis_metric_nonincreasing": bool(axis_improves),
            "res_ok": bool(res_ok),
            "axis_ok": bool(axis_ok),
            "refine_ok": bool(refine_ok),
        },
        "scientific_boundary": (
            "Axisymmetric R–z nonlinear AQUAL under declared Conditional IR. "
            "Outer BC is soft 3D monopole (multipoles of the disk not matched). "
            "Not SPARC fitting, not Derived C_obs, not full DISK-001 PASS "
            "(full PASS still wants multipole BC audit, thicker resolution study, "
            "and optional comparison to independent MOND disk codes)."
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "next_required_calculation": [
            "Multipole / larger-domain BC sensitivity",
            "Compare midplane g(R) to thin-disk limits",
            "DISK-001_GATE_REPORT when full criteria agreed",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "disk001_poisson_rz_aqual_summary.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")
    with (args.output_dir / "disk001_stage3_rz_convergence.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        fields = [
            "nr",
            "nz",
            "dR",
            "dz",
            "discrete_rel_residual",
            "axis_dphi_dR_rms_over_g_char",
            "picard_iters",
            "g_probe_midplane_R_eq_Rd",
        ]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in results:
            w.writerow({k: row[k] for k in fields})

    print(f"STATUS: {summary['subgate_status']}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
