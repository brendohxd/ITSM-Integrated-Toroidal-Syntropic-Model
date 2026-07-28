#!/usr/bin/env python3
"""UVIR-003 regular finite-q physical-scalar basis and projection map.

Separates the homogeneous time-translation orbit from the two matter gauge
invariants and rescales the spatially varying preferred-time mode by q/H:

    Xi       = (q_phys/H) R,
    Q_rho    = delta_rho - (rho_dot/H) R,
    Q_chi    = rho [vartheta - (mu/H) R].

For q_phys>0 the inverse map is nonsingular.  Its q->0 kinetic limit is finite
because the Xi column follows the verified time-shift direction divided by q.
The exactly homogeneous Xi mode is absent, so this construction does not
restore or canonically normalize the q=0 gauge orbit.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

from uvir003_complete_l4_contact import symbolic_audit as l4_audit
from uvir003_scalar_adm_finite_q import (
    background_parameters,
    evaluate_matrices,
    load_inputs,
    symbolic_reduction,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base / "outputs",
        help="Directory for JSON and CSV outputs.",
    )
    parser.add_argument(
        "--frw-summary",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_summary.json",
    )
    parser.add_argument(
        "--frw-trajectory",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_trajectory.csv",
    )
    parser.add_argument(
        "--alignment",
        type=float,
        default=1.0,
        help="Diagnostic-only alignment value, matching the finite-q audit.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def require_zero(
    name: str,
    expression: sp.Expr | sp.MatrixBase,
) -> None:
    reduced = sp.simplify(expression)
    if isinstance(reduced, sp.MatrixBase):
        if all(sp.factor(value) == 0 for value in reduced):
            return
        raise AssertionError(f"{name} failed: {reduced}")
    if sp.factor(reduced) != 0:
        raise AssertionError(f"{name} failed: {reduced}")


def matrix_limit(
    matrix: sp.MatrixBase,
    variable: sp.Symbol,
    point: int,
) -> sp.Matrix:
    return sp.Matrix(
        matrix.rows,
        matrix.cols,
        lambda row, col: sp.factor(
            sp.limit(matrix[row, col], variable, point)
        ),
    )


def symbolic_basis() -> dict[str, object]:
    reduction = symbolic_reduction()
    expressions = reduction["expressions"]
    symbols = reduction["symbols"]
    kinetic = expressions["kinetic"]
    q = symbols["q"]
    hubble = symbols["H"]
    rho = symbols["rho"]
    rho_dot = symbols["rho_dot"]
    chemical = symbols["mu"]

    mcos2 = sp.Symbol("M_cos_sq", positive=True)
    d123 = sp.Symbol("D_123", positive=True)
    c14 = sp.Symbol("C_14", positive=True)
    potential = expressions["potential"]
    enthalpy = rho_dot**2 + rho**2 * chemical**2
    friedmann = {
        hubble**2: (enthalpy + 2 * potential) / (6 * mcos2)
    }

    # y=(R,delta_rho,vartheta)=T p, with
    # p=(Xi,Q_rho,Q_chi).  The Xi column is the time-shift orbit divided by q.
    transform = sp.Matrix(
        [
            [hubble / q, 0, 0],
            [rho_dot / q, 1, 0],
            [chemical / q, 0, 1 / rho],
        ]
    )
    inverse = sp.Matrix(
        [
            [q / hubble, 0, 0],
            [-rho_dot / hubble, 1, 0],
            [-rho * chemical / hubble, 0, rho],
        ]
    )
    require_zero("basis inverse", inverse * transform - sp.eye(3))

    physical_kinetic = sp.simplify(transform.T * kinetic * transform)
    physical_limit = matrix_limit(
        physical_kinetic.subs(friedmann), q, 0
    )
    require(
        "finite physical q0 limit",
        not physical_limit.has(sp.oo, -sp.oo, sp.zoo, sp.nan),
    )

    expected_determinant = sp.factor(
        2
        * mcos2
        * hubble**2
        * (2 * mcos2 - 3 * d123)
        * c14
        / (
            c14 * d123 * q**2
            - 2 * d123 * potential
            + 4 * mcos2**2 * hubble**2
        )
    )
    require_zero(
        "physical-basis determinant",
        (
            physical_kinetic.det()
            - expected_determinant
        ).subs(friedmann),
    )
    determinant_limit = sp.factor(
        sp.limit(
            expected_determinant.subs(friedmann),
            q,
            0,
        )
    )
    require(
        "nonzero physical determinant limit",
        determinant_limit != 0,
    )

    time_shift = sp.Matrix([hubble, rho_dot, chemical])
    require_zero(
        "Xi column follows time-shift orbit",
        q * transform[:, 0] - time_shift,
    )

    # Exact time-dependent field map. q_dot=-H q for fixed comoving momentum.
    xi, q_rho, q_chi = sp.symbols("Xi Q_rho Q_chi", real=True)
    xi_dot, q_rho_dot, q_chi_dot = sp.symbols(
        "Xi_dot Q_rho_dot Q_chi_dot", real=True
    )
    hubble_dot, rho_ddot, chemical_dot = sp.symbols(
        "H_dot rho_ddot mu_dot", real=True
    )
    q_dot = -hubble * q
    h_over_q_dot = hubble_dot / q - hubble * q_dot / q**2
    rho_dot_over_q_dot = rho_ddot / q - rho_dot * q_dot / q**2
    mu_over_q_dot = chemical_dot / q - chemical * q_dot / q**2

    field_map = {
        "R": "H*Xi/q_phys",
        "delta_rho": "Q_rho+rho_dot*Xi/q_phys",
        "vartheta": "Q_chi/rho+mu*Xi/q_phys",
        "R_dot": (
            "H*Xi_dot/q_phys"
            "+(H_dot/q_phys+H^2/q_phys)*Xi"
        ),
        "delta_rho_dot": (
            "Q_rho_dot+rho_dot*Xi_dot/q_phys"
            "+(rho_ddot/q_phys+H*rho_dot/q_phys)*Xi"
        ),
        "vartheta_dot": (
            "Q_chi_dot/rho-rho_dot*Q_chi/rho^2"
            "+mu*Xi_dot/q_phys"
            "+(mu_dot/q_phys+H*mu/q_phys)*Xi"
        ),
    }
    symbolic_velocity_map = sp.Matrix(
        [
            hubble * xi_dot / q + h_over_q_dot * xi,
            (
                q_rho_dot
                + rho_dot * xi_dot / q
                + rho_dot_over_q_dot * xi
            ),
            (
                q_chi_dot / rho
                - rho_dot * q_chi / rho**2
                + chemical * xi_dot / q
                + mu_over_q_dot * xi
            ),
        ]
    )

    l4 = l4_audit()
    require(
        "complete L4 dependency",
        l4["quartic_contact"]["status"]
        == "PASS_COMPLETE_GENERIC_L4_X_Z1_CONTACT",
    )

    return {
        "_reduction": reduction,
        "transform": transform,
        "inverse": inverse,
        "physical_kinetic": physical_kinetic,
        "physical_q0_limit": physical_limit,
        "physical_determinant": expected_determinant,
        "physical_determinant_q0": determinant_limit,
        "field_map": field_map,
        "symbolic_velocity_map": symbolic_velocity_map,
        "projection_rule": {
            "cubic": (
                "V_phys_abc(k1,k2,k3)="
                "T^i_a(k1)T^j_b(k2)T^k_c(k3)V_ijk"
            ),
            "quartic": (
                "W_phys_abcd(k1,k2,k3,k4)="
                "T^i_a(k1)T^j_b(k2)T^k_c(k3)T^l_d(k4)W_ijkl"
            ),
            "time_dependence": (
                "replace dot(y)=T dot(p)+dot(T)p using q_dot=-H q"
            ),
            "momentum_rule": (
                "each external leg carries its own nonzero q_phys; "
                "the exactly homogeneous Xi leg is excluded as gauge"
            ),
        },
    }


def representative_scan(
    reduction: dict[str, object],
    frw: dict[str, object],
    rows: list[dict[str, float]],
    alignment: float,
) -> tuple[dict[str, object], list[dict[str, float]]]:
    params = background_parameters(frw, alignment)
    matrix_function = reduction["matrix_function"]
    ratios = np.logspace(-3, 3, 49)
    scan_rows: list[dict[str, float]] = []
    global_minimum = math.inf
    global_maximum_condition = 0.0
    low_q_minimum = math.inf
    low_q_maximum = -math.inf

    for ratio in ratios:
        ratio_minimum = math.inf
        ratio_condition = 0.0
        for row in rows:
            q = ratio * row["H"]
            state = np.array(
                [row["H"], row["rho"], row["rho_dot"], row["mu"], q],
                dtype=float,
            )
            kinetic, _, _, _ = evaluate_matrices(
                matrix_function, params, state
            )
            transform = np.array(
                [
                    [row["H"] / q, 0.0, 0.0],
                    [row["rho_dot"] / q, 1.0, 0.0],
                    [row["mu"] / q, 0.0, 1.0 / row["rho"]],
                ],
                dtype=float,
            )
            projected = transform.T @ kinetic @ transform
            projected = (projected + projected.T) / 2
            eigenvalues = np.linalg.eigvalsh(projected)
            ratio_minimum = min(ratio_minimum, float(eigenvalues[0]))
            ratio_condition = max(
                ratio_condition,
                float(eigenvalues[-1] / eigenvalues[0]),
            )
        require(f"positive basis inertia at q/H={ratio}", ratio_minimum > 0)
        global_minimum = min(global_minimum, ratio_minimum)
        global_maximum_condition = max(
            global_maximum_condition, ratio_condition
        )
        if ratio <= 1.0e-2:
            low_q_minimum = min(low_q_minimum, ratio_minimum)
            low_q_maximum = max(low_q_maximum, ratio_minimum)
        scan_rows.append(
            {
                "q_over_H": float(ratio),
                "minimum_physical_basis_eigenvalue": ratio_minimum,
                "maximum_physical_basis_condition": ratio_condition,
            }
        )

    low_q_variation = low_q_maximum / low_q_minimum
    require("bounded low-q physical basis", low_q_variation < 1.05)
    return (
        {
            "trajectory_samples": len(rows),
            "q_over_H_minimum": float(ratios[0]),
            "q_over_H_maximum": float(ratios[-1]),
            "q_samples": len(ratios),
            "total_matrix_samples": len(rows) * len(ratios),
            "inertia": "3_POSITIVE_0_NEGATIVE_FOR_Q_GT_0",
            "minimum_eigenvalue": global_minimum,
            "maximum_condition_number": global_maximum_condition,
            "low_q_minimum_eigenvalue_variation_ratio": low_q_variation,
            "q0_interpretation": (
                "Xi has no exactly homogeneous mode; Q_rho and Q_chi "
                "reduce to the verified two-dimensional q=0 physical block"
            ),
        },
        scan_rows,
    )


def serializable_symbolic(symbolic: dict[str, object]) -> dict[str, object]:
    return {
        "variables": [
            "Xi=(q_phys/H)R",
            "Q_rho=delta_rho-(rho_dot/H)R",
            "Q_chi=rho[vartheta-(mu/H)R]",
        ],
        "inverse_map": str(symbolic["transform"]),
        "forward_map": str(symbolic["inverse"]),
        "physical_kinetic_matrix": str(symbolic["physical_kinetic"]),
        "physical_q0_limit": str(symbolic["physical_q0_limit"]),
        "physical_determinant": str(symbolic["physical_determinant"]),
        "physical_determinant_q0": str(
            symbolic["physical_determinant_q0"]
        ),
        "field_and_velocity_map": symbolic["field_map"],
        "symbolic_velocity_map": str(symbolic["symbolic_velocity_map"]),
        "vertex_projection": symbolic["projection_rule"],
        "status": "PASS_REGULAR_FINITE_Q_PHYSICAL_SCALAR_BASIS",
    }


def write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    symbolic = symbolic_basis()
    reduction = symbolic["_reduction"]
    frw, rows = load_inputs(args.frw_summary, args.frw_trajectory)
    representative, scan_rows = representative_scan(
        reduction, frw, rows, args.alignment
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_PHYSICAL_SCALAR_BASIS",
        "calculation_status": "PASS",
        "subgate_status": "PASS_REGULAR_FINITE_Q_PHYSICAL_SCALAR_BASIS",
        "basis_status": "DERIVED_AND_VERIFIED",
        "vertex_projection_map_status": "DEFINED",
        "projected_vertex_status": "NOT_YET_EVALUATED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "symbolic_result": serializable_symbolic(symbolic),
        "representative_branch": representative,
        "scientific_boundary": (
            "The finite-q physical-scalar basis has a finite positive low-q "
            "kinetic limit and excludes the exactly homogeneous Xi gauge "
            "mode. The leg-wise vertex projection map is fixed, but the "
            "projected cubic/quartic kernels and 2-to-2 amplitude have not "
            "yet been evaluated."
        ),
        "next_required_calculation": [
            "express the complete cubic functional as momentum-space kernels",
            "apply the leg-wise physical-basis map to cubic and quartic kernels",
            "assemble exchange and contact contributions in a declared local adiabatic regime",
            "test the homogeneous internal channel with the gauge-regular projection",
            "apply a declared unitarity criterion only if the amplitude is finite",
        ],
    }
    json_path = (
        args.output_dir / "uvir003_physical_scalar_basis_summary.json"
    )
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_csv(
        args.output_dir / "uvir003_physical_scalar_basis_scan.csv",
        scan_rows,
    )

    print("Finite-q physical scalar basis: VERIFIED")
    print("Physical-basis q->0 kinetic limit: FINITE")
    print("Representative physical-basis inertia: 3_POSITIVE_0_NEGATIVE")
    print("Exactly homogeneous Xi mode: EXCLUDED_AS_GAUGE")
    print("Leg-wise cubic/quartic projection map: DEFINED")
    print("Projected physical vertices: NOT_YET_EVALUATED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_REGULAR_FINITE_Q_PHYSICAL_SCALAR_BASIS")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
