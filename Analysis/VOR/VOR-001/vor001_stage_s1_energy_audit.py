#!/usr/bin/env python3
"""VOR-001 finite-density and smooth-winding mathematical-template audit.

The fixed-background dimensionless U(1) energy is

  E = integral [|grad rho|^2/2 + rho^2 |grad theta|^2/2
                + lambda (rho^2-v^2)^2/4] d^3x.

This executable checks the S1 finite-density minimum and an S2 smooth-winding
pre-screen on a rectangular T^3. It does not validate a parent ITSM action,
defect solution, resonance spectrum, force law, or observable prediction.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import permutations
from pathlib import Path
from typing import Any, Callable

import numpy as np


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument("--N", type=int, default=32)
    parser.add_argument("--L1", type=float, default=1.0)
    parser.add_argument("--L2", type=float, default=1.0)
    parser.add_argument("--L3", type=float, default=1.0)
    parser.add_argument("--lam", type=float, default=1.0)
    parser.add_argument("--v", type=float, default=1.0)
    return parser.parse_args()


def validate_params(
    points: int,
    lengths: tuple[float, float, float],
    lam: float,
    v: float,
) -> None:
    if isinstance(points, bool) or not isinstance(points, int) or points < 8:
        raise ValueError("N must be an integer >= 8")
    for index, length in enumerate(lengths, start=1):
        if not math.isfinite(length) or length <= 0:
            raise ValueError(f"L{index} must be finite and positive")
    if not math.isfinite(lam) or lam <= 0:
        raise ValueError("lambda must be finite and positive")
    if not math.isfinite(v) or v <= 0:
        raise ValueError("v must be finite and positive")


def validate_winding(winding: tuple[int, int, int], points: int) -> None:
    if len(winding) != 3:
        raise ValueError("winding must have exactly three components")
    for component in winding:
        if isinstance(component, bool) or not isinstance(component, int):
            raise ValueError("winding components must be integers")
        if 2 * abs(component) >= points:
            raise ValueError("winding is at or beyond the sampling Nyquist limit")


def potential_derivatives(rho: float, lam: float, v: float) -> tuple[float, float]:
    first = lam * rho * (rho**2 - v**2)
    second = lam * (3 * rho**2 - v**2)
    return first, second


def build_fields(
    points: int,
    lengths: tuple[float, float, float],
    winding: tuple[int, int, int],
    v: float,
    phase_offset: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    validate_winding(winding, points)
    axes = [np.linspace(0.0, length, points, endpoint=False) for length in lengths]
    x_grid, y_grid, z_grid = np.meshgrid(*axes, indexing="ij")
    rho = np.full_like(x_grid, v)
    theta = phase_offset + 2 * math.pi * (
        winding[0] * x_grid / lengths[0]
        + winding[1] * y_grid / lengths[1]
        + winding[2] * z_grid / lengths[2]
    )
    return rho, theta


def periodic_gradient_sq(
    field: np.ndarray, spacings: tuple[float, float, float]
) -> np.ndarray:
    total = np.zeros_like(field, dtype=float)
    for axis, spacing in enumerate(spacings):
        derivative = (
            np.roll(field, -1, axis=axis) - np.roll(field, 1, axis=axis)
        ) / (2 * spacing)
        total += derivative**2
    return total


def phase_gradient_sq(
    theta: np.ndarray, spacings: tuple[float, float, float]
) -> np.ndarray:
    circle = np.exp(1j * theta)
    total = np.zeros_like(theta, dtype=float)
    for axis, spacing in enumerate(spacings):
        derivative = (
            np.roll(circle, -1, axis=axis) - np.roll(circle, 1, axis=axis)
        ) / (2 * spacing)
        total += np.abs(derivative) ** 2
    return total


def numerical_energy(
    rho: np.ndarray,
    theta: np.ndarray,
    lengths: tuple[float, float, float],
    lam: float,
    v: float,
) -> float:
    if rho.shape != theta.shape or rho.ndim != 3:
        raise ValueError("rho and theta must be matching three-dimensional arrays")
    if len(set(rho.shape)) != 1:
        raise ValueError("this audit requires an equal point count on all axes")
    points = rho.shape[0]
    spacings = tuple(length / points for length in lengths)
    density = (
        periodic_gradient_sq(rho, spacings) / 2
        + rho**2 * phase_gradient_sq(theta, spacings) / 2
        + lam * (rho**2 - v**2) ** 2 / 4
    )
    return float(np.sum(density) * math.prod(spacings))


def continuum_energy(
    winding: tuple[int, int, int],
    lengths: tuple[float, float, float],
    v: float,
) -> float:
    wave_norm_sq = sum(
        (2 * math.pi * component / length) ** 2
        for component, length in zip(winding, lengths)
    )
    return v**2 * wave_norm_sq * math.prod(lengths) / 2


def discrete_energy(
    points: int,
    winding: tuple[int, int, int],
    lengths: tuple[float, float, float],
    v: float,
) -> float:
    spacings = tuple(length / points for length in lengths)
    discrete_wave_norm_sq = sum(
        (
            math.sin(2 * math.pi * component / points) / spacing
        )
        ** 2
        for component, spacing in zip(winding, spacings)
    )
    return v**2 * discrete_wave_norm_sq * math.prod(lengths) / 2


def run_energy(
    points: int,
    lengths: tuple[float, float, float],
    winding: tuple[int, int, int],
    lam: float,
    v: float,
    phase_offset: float = 0.0,
) -> float:
    rho, theta = build_fields(points, lengths, winding, v, phase_offset)
    return numerical_energy(rho, theta, lengths, lam, v)


def catches_value_error(function: Callable[[], Any]) -> bool:
    try:
        function()
    except ValueError:
        return True
    return False


def main() -> None:
    args = parse_args()
    lengths = (args.L1, args.L2, args.L3)
    validate_params(args.N, lengths, args.lam, args.v)

    cases = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 1),
        (2, 0, 0),
    ]
    first_potential, second_potential = potential_derivatives(
        args.v, args.lam, args.v
    )

    numerical = {
        str(case): run_energy(args.N, lengths, case, args.lam, args.v)
        for case in cases
    }
    discrete = {
        str(case): discrete_energy(args.N, case, lengths, args.v)
        for case in cases
    }
    continuum = {
        str(case): continuum_energy(case, lengths, args.v) for case in cases
    }
    discrete_relative_errors = {
        key: abs(numerical[key] - discrete[key]) / discrete[key]
        for key in numerical
    }

    reflection_differences = {
        str(case): abs(
            run_energy(args.N, lengths, case, args.lam, args.v)
            - run_energy(
                args.N,
                lengths,
                tuple(-component for component in case),
                args.lam,
                args.v,
            )
        )
        for case in cases
    }

    isotropic_lengths = (1.0, 1.0, 1.0)
    permutation_cases = sorted(set(permutations((1, 2, 0))))
    permutation_energies = {
        str(case): run_energy(
            args.N, isotropic_lengths, case, args.lam, args.v
        )
        for case in permutation_cases
    }
    permutation_spread = max(permutation_energies.values()) - min(
        permutation_energies.values()
    )

    zero_energy = run_energy(
        args.N, lengths, (0, 0, 0), args.lam, args.v
    )
    shifted_zero_energy = run_energy(
        args.N, lengths, (0, 0, 0), args.lam, args.v, phase_offset=1.234
    )

    monotonic_cases = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]
    monotonic_energies = [
        run_energy(args.N, isotropic_lengths, case, args.lam, args.v)
        for case in monotonic_cases
    ]

    refinement_points = [16, 32, 64]
    refinement_case = (1, 0, 0)
    continuum_reference = continuum_energy(refinement_case, lengths, args.v)
    refinement_energies = [
        run_energy(points, lengths, refinement_case, args.lam, args.v)
        for points in refinement_points
    ]
    refinement_errors = [
        abs(energy - continuum_reference) / continuum_reference
        for energy in refinement_energies
    ]
    observed_orders = [
        math.log(refinement_errors[index] / refinement_errors[index + 1], 2)
        for index in range(len(refinement_errors) - 1)
    ]

    malformed_controls = {
        "boolean_grid_rejected": catches_value_error(
            lambda: validate_params(True, lengths, args.lam, args.v)
        ),
        "small_grid_rejected": catches_value_error(
            lambda: validate_params(7, lengths, args.lam, args.v)
        ),
        "zero_length_rejected": catches_value_error(
            lambda: validate_params(args.N, (0.0, 1.0, 1.0), args.lam, args.v)
        ),
        "nonfinite_length_rejected": catches_value_error(
            lambda: validate_params(
                args.N, (1.0, math.inf, 1.0), args.lam, args.v
            )
        ),
        "nonpositive_lambda_rejected": catches_value_error(
            lambda: validate_params(args.N, lengths, 0.0, args.v)
        ),
        "nonpositive_v_rejected": catches_value_error(
            lambda: validate_params(args.N, lengths, args.lam, 0.0)
        ),
        "noninteger_winding_rejected": catches_value_error(
            lambda: validate_winding((1, 0.5, 0), args.N)  # type: ignore[arg-type]
        ),
        "underresolved_winding_rejected": catches_value_error(
            lambda: validate_winding((args.N // 2, 0, 0), args.N)
        ),
        "shape_mismatch_rejected": catches_value_error(
            lambda: numerical_energy(
                np.ones((8, 8, 8)),
                np.ones((8, 8, 7)),
                lengths,
                args.lam,
                args.v,
            )
        ),
    }

    checks = {
        "S1_1_finite_density_minimum": (
            abs(first_potential) < 1e-14 and second_potential > 0
        ),
        "S1_2_global_U1_shift_is_gapless_control": (
            abs(zero_energy) < 1e-14 and abs(shifted_zero_energy) < 1e-14
        ),
        "S1_3_no_force_operator_or_packaging_parameter_used": True,
        "S2pre_1_integer_holonomy_is_declared": all(
            all(isinstance(component, int) for component in case) for case in cases
        ),
        "S2pre_2_numeric_energy_matches_exact_discrete_formula": (
            max(discrete_relative_errors.values()) < 1e-12
        ),
        "S2pre_3_nontrivial_sector_energy_is_positive": all(
            energy > 0 for energy in numerical.values()
        ),
        "S2pre_4_reflection_degeneracy": (
            max(reflection_differences.values()) < 1e-12
        ),
        "S2pre_5_isotropic_axis_permutation_covariance": (
            permutation_spread < 1e-12
        ),
        "S2pre_6_trivial_winding_recovers_background": abs(zero_energy) < 1e-14,
        "S2pre_7_energy_increases_across_selected_norm_sequence": all(
            monotonic_energies[index] < monotonic_energies[index + 1]
            for index in range(len(monotonic_energies) - 1)
        ),
        "S2pre_8_second_order_convergence_to_continuum_energy": (
            all(
                refinement_errors[index] > refinement_errors[index + 1]
                for index in range(len(refinement_errors) - 1)
            )
            and all(1.8 < order < 2.2 for order in observed_orders)
            and refinement_errors[-1] < 0.004
        ),
        "S2pre_9_all_malformed_inputs_are_rejected": all(
            malformed_controls.values()
        ),
        "result_is_not_promoted_to_research_or_physics_pass": True,
    }
    all_ok = all(checks.values())
    status = (
        "PASS_VOR001_S1_AND_S2PRE_MATH_TEMPLATE_ONLY"
        if all_ok
        else "FAIL_VOR001_S1_AND_S2PRE_MATH_TEMPLATE"
    )

    summary: dict[str, Any] = {
        "gate": "VOR-001",
        "stage": "S1 finite-density plus S2 smooth-winding pre-screen",
        "label": "mathematical-template-only",
        "status": status,
        "calculation_pass": all_ok,
        "research_gate_status": "OPEN_SCAFFOLD_ONLY",
        "physics_pass": False,
        "derived_claims": [],
        "parameters": {
            "N": args.N,
            "lengths": list(lengths),
            "lambda": args.lam,
            "v": args.v,
        },
        "finite_density_minimum": {
            "rho0": args.v,
            "potential_first_derivative": first_potential,
            "potential_second_derivative": second_potential,
        },
        "sector_energies": {
            "numeric": numerical,
            "exact_discrete": discrete,
            "continuum": continuum,
            "numeric_vs_discrete_relative_error": discrete_relative_errors,
        },
        "refinement": {
            "points": refinement_points,
            "energies": refinement_energies,
            "continuum_energy": continuum_reference,
            "relative_errors": refinement_errors,
            "observed_orders": observed_orders,
        },
        "symmetry_controls": {
            "reflection_absolute_differences": reflection_differences,
            "permutation_energies": permutation_energies,
            "permutation_spread": permutation_spread,
        },
        "malformed_input_controls": malformed_controls,
        "checks": checks,
        "hold": "HOLD_PARENT_ACTION_LOCAL_FLUCTUATIONS_AND_DEFECT_SECTOR",
        "scientific_boundary": (
            "This fixed-background dimensionless toy verifies a stable finite-density "
            "minimum and the numerical energy accounting of smooth integer-winding "
            "sectors. It is not the UVIR parent condensate action, a local fluctuation "
            "stability result, a defect solution, or a resonance mechanism."
        ),
        "forbidden_inferences": {
            "SWNT_mechanism_is_derived": False,
            "a0_or_force_normalization_is_derived": False,
            "defect_solution_is_derived": False,
            "resonance_spectrum_is_derived": False,
            "cosmology_lensing_PTA_or_SPARC_claim_is_supported": False,
        },
        "next": [
            "derive the same sector split from one declared parent condensate action",
            "expand local amplitude and phase fluctuations about nonzero winding",
            "defer defect cores to S3 and define resonance operationally before S4",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "vor001_stage_s1_energy_audit_summary.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("VOR-001 finite-density and smooth-winding template audit")
    for name, passed in checks.items():
        print(f"  [{'OK' if passed else 'FAIL'}] {name}")
    print("STATUS:", status)
    print("RESEARCH GATE: OPEN_SCAFFOLD_ONLY")
    print("HOLD: HOLD_PARENT_ACTION_LOCAL_FLUCTUATIONS_AND_DEFECT_SECTOR")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
