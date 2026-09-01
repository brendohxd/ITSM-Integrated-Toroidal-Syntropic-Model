#!/usr/bin/env python3
"""DISK-001 Stage 4: outer-BC sensitivity + midplane g(R) diagnostics.

Peer-review questions
---------------------
1. How much does the interior midplane acceleration change when the outer
   Dirichlet domain is enlarged (proxy for multipole / truncation error of the
   soft monopole BC used in Stage 3)?
2. How does midplane |g|(R) from the R–z nonlinear AQUAL solve compare to
   (a) Newtonian midplane g_N from the same 3D soft field, and
   (b) the algebraic Conditional AQUAL map applied to that g_N?

This does **not** implement a full multipole expansion on ∂Ω; it quantifies
domain-truncation sensitivity, which is the leading BC error for a monopole
Dirichlet condition, and is standard methods practice.

Conditional IR only. Not SPARC. Not full DISK-001 PASS.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from disk001_ir_law import a0_effective as a0_eff_fn
from disk001_ir_law import aqual_g_magnitude, default_conditional_ir
from disk001_poisson_rz_aqual import (
    discrete_residual,
    double_exp_disk_density,
    face_mu_rz,
    gradients_rz,
    soft_newtonian_3d,
    solve_linear,
)


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument("--nr", type=int, default=49, help="radial cells (fixed ΔR density via Rmax/nr)")
    p.add_argument("--mass", type=float, default=5.0e9)
    p.add_argument("--Rd", type=float, default=3.0)
    p.add_argument("--zd", type=float, default=0.3)
    p.add_argument(
        "--domains",
        type=float,
        nargs="+",
        default=[16.0, 20.0, 28.0, 40.0],
        help="Rmax values; Zmax = Rmax * z_aspect",
    )
    p.add_argument("--z-aspect", type=float, default=0.4, help="Zmax/Rmax")
    p.add_argument("--picard-max", type=int, default=50)
    p.add_argument("--omega", type=float, default=0.65)
    p.add_argument("--picard-tol", type=float, default=1e-10)
    p.add_argument(
        "--compare-Rmax",
        type=float,
        default=7.0,
        help="Interior radius for domain-sensitivity comparison (kpc).",
    )
    return p.parse_args()


def solve_rz_midplane(
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
    nz = 2 * (nr // 2) + 1
    dR = Rmax / nr
    R = (np.arange(nr) + 0.5) * dR
    z = np.linspace(-Zmax, Zmax, nz)
    dz = float(z[1] - z[0])
    RR, ZZ = np.meshgrid(R, z, indexing="xy")
    rho = double_exp_disk_density(RR, ZZ, mass, Rd, zd)
    soft = 0.25 * zd
    phi_bc = soft_newtonian_3d(RR, ZZ, mass, soft)
    boundary = np.zeros((nz, nr), dtype=bool)
    boundary[0, :] = boundary[-1, :] = True
    boundary[:, -1] = True
    interior = ~boundary

    phi, _, _ = solve_linear(nr, nz, R, dR, dz, rho, phi_bc, boundary)
    a0e = a0_eff_fn(ir)
    last_res = float("nan")
    for _ in range(picard_max):
        mu_R, mu_z = face_mu_rz(phi, dR, dz, a0e)
        mu_R = np.maximum(mu_R, 1e-8)
        mu_z = np.maximum(mu_z, 1e-8)
        phi_star, A, rhs = solve_linear(
            nr, nz, R, dR, dz, rho, phi_bc, boundary, mu_R, mu_z
        )
        phi_new = (1.0 - omega) * phi + omega * phi_star
        phi_new[boundary] = phi_bc[boundary]
        delta = float(np.max(np.abs(phi_new - phi)))
        phi = phi_new
        last_res = discrete_residual(A, phi, rhs, interior)
        if delta < picard_tol * (float(np.max(np.abs(phi))) + 1e-30) and last_res < 1e-6:
            break

    dR_phi, dz_phi = gradients_rz(phi, dR, dz)
    gR, gz = -dR_phi, -dz_phi
    i0 = int(np.argmin(np.abs(z)))
    g_mid = np.sqrt(gR[i0, :] ** 2 + gz[i0, :] ** 2)
    # Newtonian midplane from soft monopole (diagnostic, not self-consistent disk N)
    phi_N = soft_newtonian_3d(RR, ZZ, mass, soft)
    dNR, dNz = gradients_rz(phi_N, dR, dz)
    gN_mid = np.sqrt(dNR[i0, :] ** 2 + dNz[i0, :] ** 2)
    # better: Newtonian from linear solve
    phi_N_sol, _, _ = solve_linear(nr, nz, R, dR, dz, rho, phi_bc, boundary)
    dNR, dNz = gradients_rz(phi_N_sol, dR, dz)
    gN_mid = np.sqrt((-dNR[i0, :]) ** 2 + (-dNz[i0, :]) ** 2)
    g_alg = aqual_g_magnitude(gN_mid, ir)

    return {
        "R": R,
        "g_mid": g_mid,
        "gN_mid": gN_mid,
        "g_alg": np.asarray(g_alg, dtype=float),
        "residual": last_res,
        "Rmax": Rmax,
        "Zmax": Zmax,
        "dR": dR,
    }


def interp_g(R_src: np.ndarray, g_src: np.ndarray, R_tgt: np.ndarray) -> np.ndarray:
    return np.interp(R_tgt, R_src, g_src, left=np.nan, right=np.nan)


def main() -> None:
    args = parse_args()
    ir = default_conditional_ir()
    domains = sorted(args.domains)
    runs = []
    for Rmax in domains:
        Zmax = args.z_aspect * Rmax
        # keep roughly fixed ΔR: nr scales with Rmax relative to baseline 20
        nr = max(33, int(round(args.nr * (Rmax / 20.0))))
        if nr % 2 == 0:
            nr += 1
        print(f"Domain Rmax={Rmax} Zmax={Zmax} nr={nr} ...")
        sol = solve_rz_midplane(
            nr,
            Rmax,
            Zmax,
            args.mass,
            args.Rd,
            args.zd,
            ir,
            args.picard_max,
            args.picard_tol,
            args.omega,
        )
        runs.append(sol)
        print(f"  residual={sol['residual']:.3e}")

    # Reference = largest domain
    ref = runs[-1]
    R_ref = ref["R"]
    mask = (R_ref <= args.compare_Rmax) & (R_ref >= 0.5 * args.Rd)
    sens_rows = []
    for sol in runs[:-1]:
        g_i = interp_g(sol["R"], sol["g_mid"], R_ref[mask])
        g_r = ref["g_mid"][mask]
        ok = np.isfinite(g_i) & np.isfinite(g_r) & (g_r > 0)
        if not np.any(ok):
            rel = float("nan")
        else:
            rel = float(np.max(np.abs(g_i[ok] - g_r[ok]) / g_r[ok]))
        sens_rows.append(
            {
                "Rmax": sol["Rmax"],
                "Zmax": sol["Zmax"],
                "max_rel_diff_vs_largest_domain": rel,
                "residual": sol["residual"],
            }
        )

    # Midplane diagnostics on largest domain
    R = ref["R"]
    g = ref["g_mid"]
    gN = ref["gN_mid"]
    g_alg = ref["g_alg"]
    m = (R >= 0.5 * args.Rd) & (R <= args.compare_Rmax)
    boost = float(np.mean(g[m] / np.maximum(gN[m], 1e-30)))
    alg_vs_pot = float(
        np.max(np.abs(g[m] - g_alg[m]) / np.maximum(g[m], 1e-30))
    )
    # Outer slope: deep-MOND-ish g ~ 1/R for point mass; for disk g ~ flatter
    # Report v_c = sqrt(g R) flatness: std/mean on outer annulus
    outer = (R > 2.0 * args.Rd) & (R < 0.6 * ref["Rmax"])
    if np.count_nonzero(outer) >= 4:
        vc = np.sqrt(np.maximum(g[outer] * R[outer], 0.0))
        flatness = float(np.std(vc) / (np.mean(vc) + 1e-30))
    else:
        flatness = float("nan")

    # Pass: largest residual small; domain sensitivity on interior < 5% between
    # second-largest and largest (truncation under control)
    res_ok = ref["residual"] < 1e-3
    if sens_rows:
        # compare penultimate domain to largest
        sens = sens_rows[-1]["max_rel_diff_vs_largest_domain"]
        sens_ok = np.isfinite(sens) and sens < 0.05
    else:
        sens = float("nan")
        sens_ok = False
    boost_ok = boost > 1.02  # MOND boost present under Conditional IR
    passed = bool(res_ok and sens_ok and boost_ok)

    summary = {
        "gate": "DISK-001",
        "stage": "STAGE4_BC_SENSITIVITY_MIDPLANE",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": (
            "PASS_DISK001_BC_SENSITIVITY_MIDPLANE"
            if passed
            else "FAIL_DISK001_BC_SENSITIVITY"
        ),
        "ir": ir.to_dict(),
        "method": {
            "solver": "Stage-3 R–z Picard AQUAL",
            "bc": "Dirichlet soft 3D Newtonian monopole",
            "sensitivity": (
                "vary Rmax (Zmax=aspect*Rmax), fixed mass/Rd/zd; "
                "max relative midplane |g| difference for R<=compare_Rmax "
                "vs largest domain"
            ),
        },
        "domains": [
            {"Rmax": s["Rmax"], "Zmax": s["Zmax"], "residual": s["residual"]}
            for s in runs
        ],
        "sensitivity_vs_largest": sens_rows,
        "midplane_largest_domain": {
            "compare_Rmax": args.compare_Rmax,
            "mean_g_over_gN_boost": boost,
            "max_rel_diff_potential_vs_algebraic_AQUAL": alg_vs_pot,
            "vc_flatness_std_over_mean_outer": flatness,
            "note_algebraic_vs_potential": (
                "Algebraic AQUAL map on midplane g_N is not identical to "
                "|-grad Phi| from the nonlinear R–z solve; difference is expected "
                "and reported, not forced to zero."
            ),
        },
        "pass_criteria": {
            "largest_residual_lt": 1e-3,
            "domain_sens_max_rel_lt": 0.05,
            "mean_boost_gt": 1.02,
        },
        "diagnostics": {
            "res_ok": bool(res_ok),
            "sens_ok": bool(sens_ok),
            "boost_ok": bool(boost_ok),
            "penultimate_vs_largest_max_rel": sens,
        },
        "scientific_boundary": (
            "Domain-truncation sensitivity for monopole Dirichlet BC and "
            "midplane g(R) diagnostics under Conditional IR. Not a full multipole "
            "BC implementation; not SPARC; not Derived C_obs; not full DISK-001 PASS."
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "next_required_calculation": [
            "Optional multipole expansion BC",
            "Optional single-galaxy diagnostic under declared inputs",
            "DISK-001_GATE_REPORT when full-pass criteria are formally signed off",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "disk001_bc_sensitivity_midplane_summary.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    # Midplane curve from largest domain
    with (args.output_dir / "disk001_midplane_gR_largest_domain.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.writer(f)
        w.writerow(["R_kpc", "g_potential", "gN", "g_algebraic_AQUAL"])
        for i in range(len(R)):
            w.writerow([R[i], g[i], gN[i], g_alg[i]])

    with (args.output_dir / "disk001_stage4_domain_sensitivity.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "Rmax",
                "Zmax",
                "max_rel_diff_vs_largest_domain",
                "residual",
            ],
        )
        w.writeheader()
        for row in sens_rows:
            w.writerow(row)

    print(f"Interior domain sensitivity (penultimate vs largest): {sens:.4e}")
    print(f"Mean g/gN boost (largest domain): {boost:.4f}")
    print(f"Max |g_pot - g_alg|/g_pot: {alg_vs_pot:.4e}")
    print(f"STATUS: {summary['subgate_status']}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
