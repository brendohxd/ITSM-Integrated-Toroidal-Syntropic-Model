#!/usr/bin/env python3
"""UVIR-003 Stage B: low-q scalar gauge-orbit and cubic-readiness audit.

Tests whether the kinetic direction that collapses in the finite-q scalar ADM
reduction approaches a physical propagating mode or the homogeneous
time-translation orbit of the verified FRW background.

The audit derives the exact q=0 null vector, constructs two gauge-invariant
matter combinations, scans their physical kinetic block, and measures the
alignment of the smallest finite-q eigenvector with the background
time-shift direction.

This script does not assign a strong-coupling scale.  If the collapsing
direction is gauge, canonical normalization of that direction is not a
physical operation.  The subsequent three-dimensional khronon audit supplies
the flat-decoupling cubic basis; the physical target is now the constrained
cosmological 2-to-2 amplitude.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base / "outputs",
        help="Directory for the JSON summary and compact CSV scan.",
    )
    parser.add_argument(
        "--frw-summary",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_summary.json",
        help="Verified representative FRW summary.",
    )
    parser.add_argument(
        "--frw-trajectory",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_trajectory.csv",
        help="Verified representative FRW trajectory.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def require_zero(name: str, expression: sp.Expr | sp.MatrixBase) -> None:
    result = sp.simplify(expression)
    if isinstance(result, sp.MatrixBase):
        if all(sp.factor(value) == 0 for value in result):
            return
        raise AssertionError(f"{name} failed: {result}")
    if sp.factor(result) != 0:
        raise AssertionError(f"{name} failed: {result}")


def symbolic_gauge_orbit() -> dict[str, object]:
    mcos2, d123, c14 = sp.symbols(
        "M_cos_sq D_123 C_14", positive=True
    )
    hubble = sp.symbols("H", nonzero=True, real=True)
    rho = sp.symbols("rho", positive=True)
    rho_dot, chemical = sp.symbols("rho_dot mu", real=True)
    potential = sp.symbols("V", positive=True)
    q = sp.symbols("q_phys", nonnegative=True)

    enthalpy = sp.simplify(rho_dot**2 + rho**2 * chemical**2)
    constraint_matrix = sp.Matrix(
        [
            [c14 * q**2 - 2 * potential, 2 * mcos2 * hubble],
            [2 * mcos2 * hubble, -d123],
        ]
    )
    velocity_source = sp.Matrix(
        [
            [6 * mcos2 * hubble, -rho_dot, -rho**2 * chemical],
            [-2 * mcos2, 0, 0],
        ]
    )
    unconstrained_kinetic = sp.diag(-6 * mcos2, 1, rho**2)
    kinetic = sp.simplify(
        unconstrained_kinetic
        - velocity_source.T
        * constraint_matrix.inv()
        * velocity_source
    )

    time_shift = sp.Matrix([hubble, rho_dot, chemical])
    friedmann = {
        hubble**2: (enthalpy + 2 * potential) / (6 * mcos2)
    }
    q0_kinetic = kinetic.subs(q, 0)
    require_zero(
        "homogeneous time-shift null vector",
        (q0_kinetic * time_shift).subs(friedmann),
    )

    invariants = sp.Matrix(
        [
            [-rho_dot / hubble, 1, 0],
            [-chemical / hubble, 0, 1],
        ]
    )
    require_zero(
        "gauge-invariant matter combinations",
        invariants * time_shift,
    )

    # R=0 is a valid homogeneous time-slicing for H!=0.  The columns below
    # span delta_rho and chi=rho*vartheta, so the phase normalization remains
    # regular as the representative rho evolves.
    physical_slice = sp.Matrix(
        [
            [0, 0],
            [1, 0],
            [0, 1 / rho],
        ]
    )
    physical_kinetic = sp.simplify(
        physical_slice.T * q0_kinetic * physical_slice
    )
    physical_determinant = sp.factor(
        physical_kinetic.det().subs(friedmann)
    )
    physical_trace = sp.factor(
        sp.trace(physical_kinetic).subs(friedmann)
    )

    expected_determinant = sp.factor(
        (2 * mcos2 - 3 * d123)
        * (enthalpy + 2 * potential)
        / (
            2
            * (
                -3 * d123 * potential
                + 2 * mcos2 * potential
                + mcos2 * enthalpy
            )
        )
    )
    require_zero(
        "physical q0 determinant",
        physical_determinant - expected_determinant,
    )

    return {
        "kinetic_matrix": kinetic,
        "q0_kinetic_matrix": q0_kinetic,
        "time_shift_vector": time_shift,
        "invariant_map": invariants,
        "physical_q0_kinetic": physical_kinetic,
        "physical_q0_determinant": physical_determinant,
        "physical_q0_trace": physical_trace,
        "constraint_matrix": constraint_matrix,
        "symbols": {
            "M_cos_sq": mcos2,
            "D_123": d123,
            "C_14": c14,
            "H": hubble,
            "rho": rho,
            "rho_dot": rho_dot,
            "mu": chemical,
            "V": potential,
            "q_phys": q,
        },
    }


def load_inputs(
    summary_path: Path,
    trajectory_path: Path,
) -> tuple[dict[str, object], list[dict[str, float]]]:
    with summary_path.open(encoding="utf-8") as handle:
        frw = json.load(handle)
    rows: list[dict[str, float]] = []
    with trajectory_path.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            rows.append({key: float(value) for key, value in raw.items()})
    require("verified FRW status", frw["calculation_status"] == "PASS")
    require("nonempty FRW trajectory", bool(rows))
    return frw, rows


def parameters(frw: dict[str, object]) -> dict[str, float]:
    branch = frw["representative_branch"]
    params = branch["parameters"]
    derived = branch["derived_parameters"]
    result = {
        "M_cos_sq": float(derived["M_cos_squared"]),
        "D_123": float(params["M_U"]) ** 2
        * float(derived["c123"]),
        "C_14": float(params["M_U"]) ** 2
        * float(derived["c14"]),
        "m_squared": float(params["m_squared"]),
        "lambda4": float(params["lambda4"]),
        "lambda6": float(params["lambda6"]),
        "Lambda": float(params["Lambda"]),
    }
    require("positive M_cos_sq", result["M_cos_sq"] > 0)
    require("positive D_123", result["D_123"] > 0)
    require("positive C_14", result["C_14"] > 0)
    require(
        "positive aether scalar numerator",
        2 * result["M_cos_sq"] - 3 * result["D_123"] > 0,
    )
    return result


def potential(rho: float, params: dict[str, float]) -> float:
    return (
        params["m_squared"] * rho**2 / 2
        + params["lambda4"] * rho**4 / 8
        + params["lambda6"]
        * rho**6
        / (24 * params["Lambda"] ** 2)
    )


def kinetic_matrix(
    row: dict[str, float],
    q_over_h: float,
    params: dict[str, float],
) -> tuple[np.ndarray, np.ndarray]:
    mcos2 = params["M_cos_sq"]
    d123 = params["D_123"]
    c14 = params["C_14"]
    hubble = row["H"]
    rho = row["rho"]
    rho_dot = row["rho_dot"]
    chemical = row["mu"]
    q = q_over_h * hubble
    constraint = np.array(
        [
            [
                c14 * q**2 - 2 * potential(rho, params),
                2 * mcos2 * hubble,
            ],
            [2 * mcos2 * hubble, -d123],
        ],
        dtype=float,
    )
    source = np.array(
        [
            [
                6 * mcos2 * hubble,
                -rho_dot,
                -rho**2 * chemical,
            ],
            [-2 * mcos2, 0.0, 0.0],
        ],
        dtype=float,
    )
    bare = np.diag([-6 * mcos2, 1.0, rho**2])
    kinetic = bare - source.T @ np.linalg.solve(
        constraint, source
    )
    return kinetic, constraint


def normalized_kinetic(
    kinetic: np.ndarray,
    rho: float,
) -> np.ndarray:
    transform = np.diag([1.0, 1.0, 1.0 / rho])
    result = transform.T @ kinetic @ transform
    return (result + result.T) / 2


def representative_scan(
    frw: dict[str, object],
    rows: list[dict[str, float]],
) -> tuple[dict[str, object], list[dict[str, float]]]:
    params = parameters(frw)
    ratios = [0.001, 0.01, 0.1, 1.0, 10.0]
    alignment_rows: list[dict[str, float]] = []

    for ratio in ratios:
        cosines: list[float] = []
        minimum_eigenvalues: list[float] = []
        for row in rows:
            kinetic, _ = kinetic_matrix(row, ratio, params)
            normalized = normalized_kinetic(kinetic, row["rho"])
            eigenvalues, eigenvectors = np.linalg.eigh(normalized)
            smallest_vector = eigenvectors[:, 0]
            time_shift = np.array(
                [
                    row["H"],
                    row["rho_dot"],
                    row["rho"] * row["mu"],
                ],
                dtype=float,
            )
            time_shift /= np.linalg.norm(time_shift)
            cosines.append(
                abs(float(smallest_vector @ time_shift))
            )
            minimum_eigenvalues.append(float(eigenvalues[0]))

        alignment_rows.append(
            {
                "q_over_H": ratio,
                "minimum_time_shift_alignment_cosine": min(cosines),
                "mean_time_shift_alignment_cosine": (
                    sum(cosines) / len(cosines)
                ),
                "minimum_smallest_kinetic_eigenvalue": min(
                    minimum_eigenvalues
                ),
                "maximum_smallest_kinetic_eigenvalue": max(
                    minimum_eigenvalues
                ),
            }
        )

    physical_minimum = math.inf
    physical_maximum = -math.inf
    physical_condition_maximum = 0.0
    q0_constraint_singular_minimum = math.inf
    q0_rank_failures = 0
    for row in rows:
        kinetic, constraint = kinetic_matrix(row, 0.0, params)
        rho = row["rho"]
        physical_slice = np.array(
            [
                [0.0, 0.0],
                [1.0, 0.0],
                [0.0, 1.0 / rho],
            ],
            dtype=float,
        )
        physical = physical_slice.T @ kinetic @ physical_slice
        eigenvalues = np.linalg.eigvalsh(
            (physical + physical.T) / 2
        )
        physical_minimum = min(
            physical_minimum, float(eigenvalues[0])
        )
        physical_maximum = max(
            physical_maximum, float(eigenvalues[-1])
        )
        physical_condition_maximum = max(
            physical_condition_maximum,
            float(eigenvalues[-1] / eigenvalues[0]),
        )
        q0_constraint_singular_minimum = min(
            q0_constraint_singular_minimum,
            float(
                np.min(
                    np.linalg.svd(
                        constraint, compute_uv=False
                    )
                )
            ),
        )
        full_normalized = normalized_kinetic(kinetic, rho)
        if np.linalg.matrix_rank(full_normalized, tol=1.0e-9) != 2:
            q0_rank_failures += 1

    require("positive invariant q0 block", physical_minimum > 0)
    require(
        "well-conditioned invariant q0 block",
        physical_condition_maximum < 2,
    )
    require(
        "q0 constraints remain nonsingular",
        q0_constraint_singular_minimum > 1.0e-8,
    )
    require("q0 rank is two throughout", q0_rank_failures == 0)
    require(
        "low-q mode follows time-shift orbit",
        alignment_rows[0][
            "minimum_time_shift_alignment_cosine"
        ]
        > 1 - 1.0e-12,
    )

    return (
        {
            "parameter_scope": (
                "Dimensionless representative branch only; no physical "
                "aether or cosmological parameter selection."
            ),
            "time_shift_orbit": {
                "raw_velocity_direction": (
                    "(H, rho_dot, mu)"
                ),
                "instantaneously_phase_normalized_direction": (
                    "(H, rho_dot, rho*mu)"
                ),
                "interpretation": (
                    "This is the tangent to "
                    "(ln a(t), rho(t), Theta(t)) under a homogeneous "
                    "time translation."
                ),
            },
            "gauge_invariant_variables": [
                "Q_rho=delta_rho-(rho_dot/H)*R",
                "Q_theta=vartheta-(mu/H)*R",
            ],
            "finite_q_alignment_scan": alignment_rows,
            "physical_q0_slice": {
                "variables": [
                    "Q_rho in R=0 slicing",
                    "rho*Q_theta in R=0 slicing",
                ],
                "minimum_kinetic_eigenvalue": physical_minimum,
                "maximum_kinetic_eigenvalue": physical_maximum,
                "maximum_condition_number": (
                    physical_condition_maximum
                ),
                "q0_rank_failures": q0_rank_failures,
                "minimum_constraint_singular_value": (
                    q0_constraint_singular_minimum
                ),
                "inertia": "2_POSITIVE_0_NEGATIVE",
            },
            "strong_coupling_decision": {
                "naive_scale_from_collapsing_eigenvalue": (
                    "REJECTED_AS_GAUGE_DEPENDENT"
                ),
                "reason": (
                    "The collapsing eigenvector converges to the "
                    "homogeneous time-translation orbit. Dividing cubic "
                    "vertices by its vanishing quadratic norm would "
                    "canonically normalize a gauge direction and can "
                    "manufacture a spurious q-dependent strong-coupling "
                    "scale."
                ),
                "physical_scale_status": (
                    "NOT_YET_DERIVED"
                ),
            },
        },
        alignment_rows,
    )


def serializable_symbolic(
    symbolic: dict[str, object],
) -> dict[str, object]:
    return {
        "q0_null_vector": str(symbolic["time_shift_vector"]),
        "q0_null_identity": (
            "K_red(q=0)*(H,rho_dot,mu)^T=0 on the Friedmann "
            "background"
        ),
        "gauge_invariant_map": str(symbolic["invariant_map"]),
        "physical_q0_kinetic_matrix": str(
            symbolic["physical_q0_kinetic"]
        ),
        "physical_q0_determinant": str(
            symbolic["physical_q0_determinant"]
        ),
        "physical_q0_trace": str(
            symbolic["physical_q0_trace"]
        ),
        "positive_symbolic_domain": [
            "M_cos_sq>0",
            "D_123>0",
            "2*M_cos_sq-3*D_123>0",
            (
                "-3*D_123*V+2*M_cos_sq*V"
                "+M_cos_sq*(rho_dot^2+rho^2*mu^2)>0"
            ),
        ],
    }


def write_csv(
    path: Path,
    rows: list[dict[str, float]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0].keys())
        )
        writer.writeheader()
        writer.writerows(rows)


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    symbolic = symbolic_gauge_orbit()
    frw, rows = load_inputs(args.frw_summary, args.frw_trajectory)
    representative, alignment_rows = representative_scan(
        frw, rows
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_SCALAR_LOW_Q_GAUGE_ORBIT",
        "calculation_status": "PASS",
        "gauge_orbit_status": (
            "IDENTIFIED_HOMOGENEOUS_TIME_TRANSLATION"
        ),
        "cubic_readiness_status": (
            "REQUIRES_STUECKELBERG_OR_GAUGE_INVARIANT_TRIAD_ACTION"
        ),
        "strong_coupling_scale_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "symbolic_result": serializable_symbolic(symbolic),
        "representative_branch": representative,
        "scientific_boundary": (
            "The q->0 rank loss has been identified as the homogeneous "
            "time-translation orbit, and the two gauge-invariant matter "
            "combinations have a positive regular q=0 kinetic block on "
            "the representative branch. This rejects a naive physical "
            "strong-coupling scale inferred solely from the vanishing "
            "eigenvalue. It does not prove nonlinear weak coupling. A "
            "The complete three-dimensional flat-decoupling cubic "
            "basis has subsequently been derived. A physical "
            "interaction scale still requires the constrained "
            "cosmological 2-to-2 amplitude."
        ),
        "next_required_calculation": [
            (
                "restore the preferred-time Stückelberg/khronon scalar "
                "or use an explicitly gauge-invariant cubic basis"
            ),
            (
                "substitute the first-order lapse and scalar-shift "
                "constraints into the complete cosmological cubic action"
            ),
            (
                "derive the quartic contact vertex and combine it with "
                "the cubic-exchange contribution"
            ),
            (
                "canonically normalize only the physical propagating "
                "modes and derive an invariant 2-to-2 unitarity scale"
            ),
            (
                "compare the resulting scales with H, physical momenta "
                "and the declared EFT cutoff"
            ),
        ],
    }

    json_path = (
        args.output_dir
        / "uvir003_scalar_low_q_gauge_summary.json"
    )
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    csv_path = (
        args.output_dir
        / "uvir003_scalar_low_q_gauge_alignment.csv"
    )
    write_csv(csv_path, alignment_rows)

    alignment = representative["finite_q_alignment_scan"][0]
    physical = representative["physical_q0_slice"]
    print("UVIR-003 low-q scalar null identity: VERIFIED")
    print(
        "Collapsing direction: HOMOGENEOUS_TIME_TRANSLATION_ORBIT"
    )
    print(
        "Minimum q/H=1e-3 time-shift alignment cosine: "
        f"{alignment['minimum_time_shift_alignment_cosine']:.15g}"
    )
    print(
        "Gauge-invariant q=0 kinetic inertia: "
        f"{physical['inertia']}"
    )
    print(
        "Naive strong-coupling inference from lambda_min: REJECTED"
    )
    print("Physical cubic interaction scale: NOT_YET_DERIVED")
    print("Full UVIR-003 gate: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_LOW_Q_GAUGE_ORBIT_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
