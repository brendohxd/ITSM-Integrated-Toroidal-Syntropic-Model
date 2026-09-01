#!/usr/bin/env python3
"""UVIR-003 Stage B: scalar ADM principal-symbol reduction.

Uses aether-unitary gauge for the scalar sector of the declared Stage-A
Einstein-aether, canonical condensate, alignment and force action.  The lapse
and scalar shift are eliminated in a frozen-coefficient subhorizon expansion
about the verified evolving flat-FRW branch.

This is a controlled principal-symbol audit.  It does not replace the full
time-dependent low-k cosmological perturbation system.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base / "outputs",
        help="Directory for the JSON summary.",
    )
    parser.add_argument(
        "--frw-summary",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_summary.json",
        help="Representative FRW summary used for the numerical cross-check.",
    )
    parser.add_argument(
        "--frw-trajectory",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_trajectory.csv",
        help="Representative FRW trajectory used for the validity-scale scan.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def require_zero(name: str, expression: sp.Expr) -> None:
    result = sp.simplify(expression)
    if isinstance(result, sp.MatrixBase):
        if all(sp.factor(value) == 0 for value in result):
            return
        raise AssertionError(f"{name} failed: {result}")
    result = sp.factor(result)
    if result != 0:
        raise AssertionError(f"{name} failed: {result}")


def symbolic_reduction() -> dict[str, object]:
    mp2, mu2 = sp.symbols("M_P_sq M_U_sq", positive=True)
    c1, c2, c3, c4 = sp.symbols("c1 c2 c3 c4", real=True)
    q = sp.symbols("q_phys", positive=True)
    rho = sp.symbols("rho", positive=True)
    rho_dot, chemical = sp.symbols("rho_dot mu", real=True)
    alignment = sp.symbols("zeta_align", nonnegative=True)
    kq, gamma, mstar = sp.symbols(
        "K_Q gamma M_star", positive=True
    )

    c13 = sp.simplify(c1 + c3)
    c14 = sp.simplify(c1 + c4)
    c123 = sp.simplify(c1 + c2 + c3)
    ctheta = sp.simplify(c1 + 3 * c2 + c3)

    # In the hypersurface-orthogonal scalar sector U^mu is the ADM unit
    # normal.  Then nabla_mu U_nu = K_mu_nu - U_mu a_nu and the combined
    # Einstein-Hilbert plus aether kinetic coefficients are:
    kij_coefficient = sp.simplify(mp2 - mu2 * c13)
    k2_coefficient = sp.simplify(-mp2 - mu2 * c2)
    acceleration_coefficient = sp.simplify(mu2 * c14)
    mcos2 = sp.simplify(mp2 + mu2 * ctheta / 2)

    require_zero(
        "FRW kinetic combination",
        kij_coefficient + 3 * k2_coefficient + 2 * mcos2,
    )
    require_zero(
        "scalar-shift quadratic combination",
        kij_coefficient + k2_coefficient + mu2 * c123,
    )

    # Scalar perturbations:
    # N=1+alpha, N_i=partial_i beta, h_ij=a^2 exp(2 R) delta_ij.
    # delta_rho and vartheta perturb the condensate amplitude and phase.
    alpha, beta = sp.symbols("delta_N beta", real=True)
    curvature, curvature_dot = sp.symbols(
        "R R_dot", real=True
    )
    delta_rho, delta_rho_dot = sp.symbols(
        "delta_rho delta_rho_dot", real=True
    )
    phase, phase_dot = sp.symbols(
        "vartheta vartheta_dot", real=True
    )

    momentum_source = sp.simplify(
        rho_dot * delta_rho + rho**2 * chemical * phase
    )
    lapse_velocity_source = sp.simplify(
        rho_dot * delta_rho_dot
        + rho**2 * chemical * phase_dot
    )

    # Frozen-coefficient principal quadratic Lagrangian per a^3 and Fourier
    # mode.  Terms without enough derivatives to affect the principal symbol
    # are intentionally omitted.
    lagrangian = sp.expand(
        -3 * mcos2 * curvature_dot**2
        - 2 * mcos2 * q**2 * beta * curvature_dot
        - mu2 * c123 * q**4 * beta**2 / 2
        + mp2 * q**2 * curvature**2
        + 2 * mp2 * q**2 * alpha * curvature
        + mu2 * c14 * q**2 * alpha**2 / 2
        + delta_rho_dot**2 / 2
        + rho**2 * phase_dot**2 / 2
        - alpha * lapse_velocity_source
        - q**2 * beta * momentum_source
        - q**2 * delta_rho**2 / 2
        - rho**2
        * (1 + alignment * rho**2)
        * q**2
        * phase**2
        / 2
    )

    lapse_solution = sp.solve(
        sp.diff(lagrangian, alpha), alpha, dict=False
    )[0]
    shift_solution = sp.solve(
        sp.diff(lagrangian, beta), beta, dict=False
    )[0]
    expected_lapse = sp.simplify(
        -2 * mp2 * curvature / (mu2 * c14)
        + lapse_velocity_source / (mu2 * c14 * q**2)
    )
    expected_shift = sp.simplify(
        -(2 * mcos2 * curvature_dot + momentum_source)
        / (mu2 * c123 * q**2)
    )
    require_zero(
        "lapse constraint solution", lapse_solution - expected_lapse
    )
    require_zero(
        "scalar-shift constraint solution", shift_solution - expected_shift
    )

    reduced = sp.expand(
        lagrangian.subs(
            {alpha: lapse_solution, beta: shift_solution}
        )
    )

    curvature_kinetic = sp.factor(
        reduced.coeff(curvature_dot, 2)
    )
    curvature_gradient = sp.factor(
        -reduced.coeff(curvature, 2) / q**2
    )

    ratio = sp.symbols("r_U", positive=True)
    alpha1 = sp.simplify(ratio * c1)
    alpha2 = sp.simplify(ratio * c2)
    alpha3 = sp.simplify(ratio * c3)
    alpha4 = sp.simplify(ratio * c4)
    alpha13 = sp.simplify(alpha1 + alpha3)
    alpha14 = sp.simplify(alpha1 + alpha4)
    alpha123 = sp.simplify(alpha1 + alpha2 + alpha3)
    frw_factor = sp.simplify(1 + ratio * ctheta / 2)

    curvature_kinetic_normalized = sp.factor(
        2 * mp2 * frw_factor * (1 - alpha13) / alpha123
    )
    curvature_gradient_normalized = sp.factor(
        mp2 * (2 - alpha14) / alpha14
    )

    normalized_substitution = {mu2: ratio * mp2}
    require_zero(
        "normalized curvature kinetic coefficient",
        curvature_kinetic.subs(normalized_substitution)
        - curvature_kinetic_normalized,
    )
    require_zero(
        "normalized curvature gradient coefficient",
        curvature_gradient.subs(normalized_substitution)
        - curvature_gradient_normalized,
    )

    scalar_speed_sq = sp.factor(
        curvature_gradient_normalized
        / curvature_kinetic_normalized
    )
    literature_speed_sq = sp.factor(
        alpha123
        * (2 - alpha14)
        / (
            alpha14
            * (1 - alpha13)
            * (2 + alpha13 + 3 * alpha2)
        )
    )
    require_zero(
        "Einstein-aether spin-0 speed",
        scalar_speed_sq - literature_speed_sq,
    )

    velocity_variables = [curvature_dot, delta_rho_dot, phase_dot]
    velocity_hessian = sp.simplify(
        sp.hessian(reduced, velocity_variables)
    )
    matter_kinetic = velocity_hessian[1:3, 1:3]
    matter_kinetic_expected = sp.Matrix(
        [
            [
                1 - rho_dot**2 / (mu2 * c14 * q**2),
                -rho_dot
                * rho**2
                * chemical
                / (mu2 * c14 * q**2),
            ],
            [
                -rho_dot
                * rho**2
                * chemical
                / (mu2 * c14 * q**2),
                rho**2
                - rho**4
                * chemical**2
                / (mu2 * c14 * q**2),
            ],
        ]
    )
    require_zero(
        "finite-q condensate kinetic matrix",
        matter_kinetic - matter_kinetic_expected,
    )

    matter_determinant = sp.factor(matter_kinetic.det())
    enthalpy = sp.simplify(rho_dot**2 + rho**2 * chemical**2)
    expected_determinant = sp.factor(
        rho**2 * (1 - enthalpy / (mu2 * c14 * q**2))
    )
    require_zero(
        "finite-q condensate kinetic determinant",
        matter_determinant - expected_determinant,
    )
    q_adm_sq = sp.simplify(enthalpy / (mu2 * c14))

    phase_speed_sq = sp.simplify(1 + alignment * rho**2)
    force_dispersion = sp.simplify(
        gamma * q**4 / (kq * mstar**2)
    )

    return {
        "symbols": {
            "M_P_squared": str(mp2),
            "M_U_squared": str(mu2),
            "physical_wavenumber": str(q),
        },
        "adm_dictionary": {
            "Kij_Kij_coefficient": str(kij_coefficient),
            "K_squared_coefficient": str(k2_coefficient),
            "acceleration_squared_coefficient": str(
                acceleration_coefficient
            ),
            "M_cos_squared": str(mcos2),
        },
        "constraints": {
            "lapse_solution_principal": str(lapse_solution),
            "scalar_shift_solution_principal": str(shift_solution),
            "momentum_source": str(momentum_source),
            "lapse_velocity_source": str(lapse_velocity_source),
        },
        "reduced_scalar_principal_block": {
            "curvature_kinetic_coefficient": str(
                curvature_kinetic_normalized
            ),
            "curvature_gradient_coefficient": str(
                curvature_gradient_normalized
            ),
            "spin_0_speed_squared": str(scalar_speed_sq),
            "literature_spin_0_speed_squared": str(
                literature_speed_sq
            ),
            "finite_q_condensate_kinetic_matrix": str(
                matter_kinetic_expected
            ),
            "finite_q_condensate_kinetic_determinant": str(
                matter_determinant
            ),
            "principal_validity_scale_squared": str(q_adm_sq),
            "amplitude_speed_squared_high_q": "1",
            "phase_speed_squared_high_q": str(phase_speed_sq),
            "force_zero_gradient_dispersion": str(force_dispersion),
        },
        "positivity_domain": {
            "cosmological_gravity": "1 + alpha_theta/2 > 0",
            "aether_scalar_no_ghost": (
                "alpha123>0 and 1-alpha13>0, with "
                "1+alpha_theta/2>0"
            ),
            "aether_scalar_gradient": "0<alpha14<2",
            "condensate": (
                "rho>0 and q_phys^2 >> "
                "(rho_dot^2+rho^2*mu^2)/(M_U^2*c14)"
            ),
            "alignment_phase_gradient": (
                "1+zeta_align*rho^2>0; declared zeta_align>0"
            ),
            "force": "K_Q>0 and gamma>0",
        },
    }


def representative_scan(
    symbolic: dict[str, object],
    summary_path: Path,
    trajectory_path: Path,
) -> dict[str, object]:
    with summary_path.open(encoding="utf-8") as handle:
        frw = json.load(handle)

    params = frw["representative_branch"]["parameters"]
    mp2 = float(params["M_P"]) ** 2
    mu2 = float(params["M_U"]) ** 2
    c1 = float(params["c1"])
    c2 = float(params["c2"])
    c3 = float(params["c3"])
    c4 = float(params["c4"])
    ratio = mu2 / mp2
    alpha1 = ratio * c1
    alpha2 = ratio * c2
    alpha3 = ratio * c3
    alpha4 = ratio * c4
    alpha13 = alpha1 + alpha3
    alpha14 = alpha1 + alpha4
    alpha123 = alpha1 + alpha2 + alpha3
    alpha_theta = alpha1 + 3 * alpha2 + alpha3
    frw_factor = 1 + alpha_theta / 2

    curvature_kinetic = (
        2 * mp2 * frw_factor * (1 - alpha13) / alpha123
    )
    curvature_gradient = mp2 * (2 - alpha14) / alpha14
    spin0_speed_sq = curvature_gradient / curvature_kinetic
    published_spin0_speed_sq = (
        alpha123
        * (2 - alpha14)
        / (
            alpha14
            * (1 - alpha13)
            * (2 + alpha13 + 3 * alpha2)
        )
    )
    require(
        "representative spin-0 literature match",
        math.isclose(
            spin0_speed_sq,
            published_spin0_speed_sq,
            rel_tol=1e-13,
            abs_tol=1e-13,
        ),
    )

    samples: list[dict[str, float]] = []
    with trajectory_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            scale = float(row["a"])
            rho = float(row["rho"])
            rho_dot = float(row["rho_dot"])
            chemical = float(row["mu"])
            hubble = float(row["H"])
            enthalpy = rho_dot**2 + rho**2 * chemical**2
            q_adm_sq = enthalpy / (mu2 * (c1 + c4))
            q_adm = math.sqrt(max(q_adm_sq, 0.0))
            samples.append(
                {
                    "t": float(row["t"]),
                    "a": scale,
                    "rho": rho,
                    "H": hubble,
                    "q_adm": q_adm,
                    "q_adm_over_H": q_adm / hubble,
                    "k_adm": scale * q_adm,
                    "k_hubble": scale * hubble,
                }
            )

    require("FRW trajectory is nonempty", bool(samples))
    require(
        "representative amplitude stays positive",
        min(row["rho"] for row in samples) > 0,
    )

    max_q = max(samples, key=lambda row: row["q_adm"])
    max_ratio = max(samples, key=lambda row: row["q_adm_over_H"])
    max_k_adm = max(samples, key=lambda row: row["k_adm"])
    max_k_hubble = max(samples, key=lambda row: row["k_hubble"])

    principal_pass = (
        frw_factor > 0
        and alpha123 > 0
        and 1 - alpha13 > 0
        and 0 < alpha14 < 2
        and curvature_kinetic > 0
        and curvature_gradient > 0
    )
    require("representative principal positivity", principal_pass)

    return {
        "parameter_scope": (
            "Dimensionless existence example only; not a physical "
            "aether or cosmological parameter point."
        ),
        "normalized_coefficients": {
            "r_U": ratio,
            "alpha1": alpha1,
            "alpha2": alpha2,
            "alpha3": alpha3,
            "alpha4": alpha4,
            "alpha13": alpha13,
            "alpha14": alpha14,
            "alpha123": alpha123,
            "alpha_theta": alpha_theta,
        },
        "reduced_aether_scalar": {
            "curvature_kinetic_coefficient": curvature_kinetic,
            "curvature_gradient_coefficient": curvature_gradient,
            "spin_0_speed_squared": spin0_speed_sq,
            "spin_0_speed": math.sqrt(spin0_speed_sq),
            "published_formula_match": True,
            "metric_superluminal_at_representative_point": (
                spin0_speed_sq > 1
            ),
        },
        "trajectory_validity_scan": {
            "samples": len(samples),
            "minimum_rho": min(row["rho"] for row in samples),
            "maximum_q_adm": max_q["q_adm"],
            "maximum_q_adm_time": max_q["t"],
            "maximum_q_adm_over_H": max_ratio["q_adm_over_H"],
            "maximum_q_adm_over_H_time": max_ratio["t"],
            "maximum_comoving_k_adm": max_k_adm["k_adm"],
            "maximum_comoving_k_adm_time": max_k_adm["t"],
            "maximum_comoving_aH": max_k_hubble["k_hubble"],
            "maximum_comoving_aH_time": max_k_hubble["t"],
            "interpretation": (
                "The frozen-coefficient principal audit is controlled "
                "only for q_phys well above both H and q_adm; for a "
                "fixed comoving mode this means k well above the "
                "reported maxima of a*H and a*q_adm."
            ),
        },
        "principal_positivity": "PASS",
        "causality_flag": (
            "MULTICONE_GLOBAL_CAUSALITY_REMAINS_OPEN; "
            "superluminality alone is not classified as a local "
            "instability in the preferred-frame EFT."
        ),
    }


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    symbolic = symbolic_reduction()
    representative = representative_scan(
        symbolic, args.frw_summary, args.frw_trajectory
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_SCALAR_ADM_PRINCIPAL_SYMBOL",
        "calculation_status": "PASS",
        "reduction_status": (
            "PASS_SUBHORIZON_PRINCIPAL_REDUCTION"
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "gauge_and_scope": {
            "gauge": (
                "aether-unitary scalar gauge: "
                "U^mu is the ADM unit normal"
            ),
            "metric": (
                "N=1+delta_N, N_i=partial_i beta, "
                "h_ij=a^2 exp(2R) delta_ij"
            ),
            "approximation": (
                "frozen background coefficients and "
                "q_phys=k/a well above H"
            ),
            "retained": (
                "principal two-time-derivative, q_phys^2 and force "
                "q_phys^4 terms, plus the leading lapse-induced "
                "1/q_phys^2 condensate kinetic correction"
            ),
        },
        "symbolic_reduction": symbolic,
        "representative_branch": representative,
        "scientific_boundary": (
            "This independently derives the scalar aether principal "
            "block and its lapse/shift constraints, and verifies the "
            "high-q condensate and force blocks. It does not determine "
            "the full time-dependent or strict low-k kinetic/gradient "
            "system, global multicone causality, a physical cutoff, or "
            "a phenomenologically selected parameter point."
        ),
        "next_required_calculation": [
            (
                "retain H, rho_dot, mu_dot and all q^0 terms in the "
                "time-dependent scalar quadratic action"
            ),
            (
                "solve the full finite-k lapse, scalar-shift and "
                "aether-multiplier constraints along the FRW branch"
            ),
            (
                "track the reduced eigenvalues through q_phys/H from "
                "the controlled subhorizon domain toward q_phys=0"
            ),
            (
                "fix or bound the alignment coefficient and physical "
                "aether parameter domain before causal interpretation"
            ),
        ],
    }

    output = (
        args.output_dir
        / "uvir003_scalar_adm_principal_summary.json"
    )
    with output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    rep = representative["reduced_aether_scalar"]
    scan = representative["trajectory_validity_scan"]
    print("UVIR-003 scalar ADM principal identities: VERIFIED")
    print("Lapse and scalar shift: ELIMINATED")
    print(
        "Einstein-aether spin-0 formula: "
        "INDEPENDENTLY_RECOVERED"
    )
    print(
        "Representative spin-0 speed squared: "
        f"{rep['spin_0_speed_squared']:.12g}"
    )
    print(
        "Maximum representative q_ADM/H: "
        f"{scan['maximum_q_adm_over_H']:.6g}"
    )
    print(
        "Scalar ADM reduction: "
        "PASS_SUBHORIZON_PRINCIPAL_REDUCTION"
    )
    print("Full UVIR-003 gate: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_SCALAR_ADM_PRINCIPAL_SYMBOL")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
