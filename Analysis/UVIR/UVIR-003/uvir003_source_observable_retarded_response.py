#!/usr/bin/env python3
"""UVIR-003 gauge-projected source-to-observable retarded-response audit.

The coupled finite-q scalar block is

    p = (Xi, Q_rho, Q_chi).

Generalized impulse covectors are restricted to (Q_rho,Q_chi), so they
annihilate the homogeneous time-translation orbit.  Retarded evolution uses
the exact time-dependent kinetic-normalized generator, while readouts retain
only the gauge-invariant matter observables (Q_rho,Q_chi).

The Track-A force mode Pi is not omitted from the ITSM framework: it
factorizes exactly from this coupled quadratic block and is outside the
complex-quartet mixing question addressed here.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.linalg import expm

from uvir003_mode_resolved_transfer_robustness import (
    build_generator_series,
    variation_cases,
)
from uvir003_physical_quadratic_propagators import (
    evaluate_physical_matrices,
    symbolic_propagators,
)
from uvir003_propagator_adiabaticity_transfer import (
    observable_normalization,
)
from uvir003_scalar_adm_finite_q import (
    background_parameters,
    load_inputs,
)


MATTER_SELECTOR = np.asarray(
    [
        [0.0, 0.0],
        [1.0, 0.0],
        [0.0, 1.0],
    ],
    dtype=float,
)
MATTER_LABELS = ("Q_rho", "Q_chi")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base / "outputs",
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
        "--initial-q-over-H",
        type=float,
        default=0.01,
    )
    parser.add_argument(
        "--substeps",
        type=int,
        default=4,
        help="Base midpoint-Magnus substeps per trajectory interval.",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run only the baseline case for development checks.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def inverse_square_root(matrix: np.ndarray) -> np.ndarray:
    symmetric = (matrix + matrix.T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(symmetric)
    require(
        "positive projector Gram matrix",
        bool(np.all(eigenvalues > 1.0e-14)),
    )
    return (
        eigenvectors
        @ np.diag(1.0 / np.sqrt(eigenvalues))
        @ eigenvectors.T
    )


def normalized_source_and_readout(
    kinetic: np.ndarray,
    hubble: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return unit-norm matter impulse columns and matter readout rows."""

    normalization, _ = observable_normalization(kinetic, hubble)
    inverse_normalization = np.linalg.inv(normalization)
    dimension = kinetic.shape[0]
    zero = np.zeros((dimension, MATTER_SELECTOR.shape[1]))
    source_x = np.vstack(
        [
            zero,
            np.linalg.solve(kinetic, MATTER_SELECTOR),
        ]
    )
    source_raw = normalization @ source_x
    source = source_raw @ inverse_square_root(source_raw.T @ source_raw)

    coordinate_readout = np.hstack(
        [MATTER_SELECTOR.T, np.zeros_like(MATTER_SELECTOR.T)]
    )
    readout_raw = coordinate_readout @ inverse_normalization
    readout = (
        inverse_square_root(readout_raw @ readout_raw.T)
        @ readout_raw
    )
    return source, readout


def build_projection_series(
    symbolic: dict[str, object],
    params: dict[str, float],
    rows: list[dict[str, float]],
    comoving_momentum: float,
) -> dict[str, Any]:
    sources: list[np.ndarray] = []
    readouts: list[np.ndarray] = []
    orbit_residuals: list[float] = []
    source_support_residuals: list[float] = []
    readout_support_residuals: list[float] = []
    source_position_jump_residuals: list[float] = []
    readout_velocity_support_residuals: list[float] = []
    source_orthonormality_residuals: list[float] = []
    readout_orthonormality_residuals: list[float] = []

    for row in rows:
        physical_q = comoving_momentum / row["a"]
        state = np.asarray(
            [
                row["H"],
                row["rho"],
                row["rho_dot"],
                row["mu"],
                physical_q,
            ],
            dtype=float,
        )
        kinetic, _, _ = evaluate_physical_matrices(
            symbolic,
            params,
            state,
        )
        source, readout = normalized_source_and_readout(
            kinetic,
            row["H"],
        )
        sources.append(source)
        readouts.append(readout)
        normalization, _ = observable_normalization(
            kinetic,
            row["H"],
        )
        source_x = np.linalg.solve(normalization, source)
        generalized_force = kinetic @ source_x[3:]
        readout_x = readout @ normalization
        source_support_residuals.append(
            float(
                np.linalg.norm(generalized_force[0])
                / max(np.linalg.norm(generalized_force), 1.0e-30)
            )
        )
        readout_support_residuals.append(
            float(
                np.linalg.norm(readout_x[:, 0])
                / max(np.linalg.norm(readout_x), 1.0e-30)
            )
        )
        source_position_jump_residuals.append(
            float(np.linalg.norm(source_x[:3]))
        )
        readout_velocity_support_residuals.append(
            float(np.linalg.norm(readout_x[:, 3:]))
        )
        source_orthonormality_residuals.append(
            float(np.linalg.norm(source.T @ source - np.eye(2)))
        )
        readout_orthonormality_residuals.append(
            float(np.linalg.norm(readout @ readout.T - np.eye(2)))
        )

        time_orbit = np.asarray(
            [row["H"], row["rho_dot"], row["mu"]],
            dtype=float,
        )
        physical_covectors = np.asarray(
            [
                [-row["rho_dot"] / row["H"], 1.0, 0.0],
                [
                    -row["rho"] * row["mu"] / row["H"],
                    0.0,
                    row["rho"],
                ],
            ],
            dtype=float,
        )
        orbit_residuals.append(
            float(
                np.linalg.norm(physical_covectors @ time_orbit)
                / max(
                    np.linalg.norm(physical_covectors)
                    * np.linalg.norm(time_orbit),
                    1.0e-30,
                )
            )
        )

    return {
        "sources": sources,
        "readouts": readouts,
        "maximum_time_orbit_annihilation_residual": max(
            orbit_residuals
        ),
        "maximum_direct_Xi_source_support": max(
            source_support_residuals
        ),
        "maximum_direct_Xi_readout_support": max(
            readout_support_residuals
        ),
        "maximum_source_position_jump_residual": max(
            source_position_jump_residuals
        ),
        "maximum_readout_velocity_support": max(
            readout_velocity_support_residuals
        ),
        "maximum_source_orthonormality_residual": max(
            source_orthonormality_residuals
        ),
        "maximum_readout_orthonormality_residual": max(
            readout_orthonormality_residuals
        ),
    }


def interval_steps(
    generators: list[np.ndarray],
    times: np.ndarray,
    substeps: int,
) -> list[np.ndarray]:
    steps: list[np.ndarray] = []
    dimension = generators[0].shape[0]
    for index in range(len(times) - 1):
        interval = float(times[index + 1] - times[index])
        step = np.eye(dimension)
        for substep in range(substeps):
            fraction = (substep + 0.5) / substeps
            generator = (
                (1.0 - fraction) * generators[index]
                + fraction * generators[index + 1]
            )
            step = expm(generator * interval / substeps) @ step
        steps.append(step)
    return steps


def off_axis_quartet_flags(
    generators: list[np.ndarray],
    hubbles: np.ndarray,
) -> np.ndarray:
    flags: list[bool] = []
    for generator, hubble in zip(generators, hubbles, strict=True):
        eigenvalues = np.linalg.eigvals(generator)
        scale = max(
            float(np.max(np.abs(eigenvalues))),
            float(hubble),
            1.0e-30,
        )
        tolerance = 1.0e-9 * scale
        flags.append(
            bool(
                np.any(
                    (np.abs(eigenvalues.real) > tolerance)
                    & (np.abs(eigenvalues.imag) > tolerance)
                )
            )
        )
    return np.asarray(flags, dtype=bool)


def spectral_data(
    response: np.ndarray,
) -> tuple[float, np.ndarray, np.ndarray]:
    left, singular_values, right = np.linalg.svd(response)
    return float(singular_values[0]), right[0], left[:, 0]


def direction_weights(vector: np.ndarray) -> dict[str, float]:
    denominator = max(float(np.dot(vector, vector)), 1.0e-30)
    return {
        label: float(vector[index] ** 2 / denominator)
        for index, label in enumerate(MATTER_LABELS)
    }


def evaluate_response_grid(
    case_name: str,
    series: dict[str, Any],
    projection: dict[str, Any],
    fine_steps: list[np.ndarray],
    coarse_steps: list[np.ndarray],
    quartet_flags: np.ndarray,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    times = series["times"]
    q_over_h = series["q_over_h"]
    sources = projection["sources"]
    readouts = projection["readouts"]
    source_summaries: list[dict[str, Any]] = []

    quartet_indices = np.flatnonzero(quartet_flags)
    require("off-axis quartet present", bool(len(quartet_indices)))
    quartet_start = int(quartet_indices[0])
    quartet_end = int(quartet_indices[-1])

    global_maximum = -math.inf
    global_record: dict[str, Any] = {}
    maximum_absolute_difference = 0.0
    maximum_through_quartet = -math.inf
    through_quartet_record: dict[str, Any] = {}
    maximum_real_pole_only = -math.inf

    for source_index in range(len(times)):
        fine_state = sources[source_index].copy()
        coarse_state = sources[source_index].copy()
        source_maximum = -math.inf
        source_maximum_index = source_index
        source_maximum_difference = 0.0

        for observation_index in range(source_index, len(times)):
            fine_response = readouts[observation_index] @ fine_state
            coarse_response = readouts[observation_index] @ coarse_state
            gain, input_direction, output_direction = spectral_data(
                fine_response
            )
            difference = float(
                np.linalg.norm(fine_response - coarse_response)
            )
            maximum_absolute_difference = max(
                maximum_absolute_difference,
                difference,
            )
            source_maximum_difference = max(
                source_maximum_difference,
                difference,
            )

            crosses_quartet = bool(
                np.any(quartet_flags[source_index : observation_index + 1])
            )
            record = {
                "source_index": source_index,
                "observation_index": observation_index,
                "source_t": float(times[source_index]),
                "observation_t": float(times[observation_index]),
                "source_q_over_H": float(q_over_h[source_index]),
                "observation_q_over_H": float(
                    q_over_h[observation_index]
                ),
                "gain": gain,
                "crosses_complex_quartet": crosses_quartet,
                "input_direction": direction_weights(input_direction),
                "output_direction": direction_weights(output_direction),
            }
            if gain > source_maximum:
                source_maximum = gain
                source_maximum_index = observation_index
            if gain > global_maximum:
                global_maximum = gain
                global_record = record
            if crosses_quartet and gain > maximum_through_quartet:
                maximum_through_quartet = gain
                through_quartet_record = record
            if not crosses_quartet:
                maximum_real_pole_only = max(
                    maximum_real_pole_only,
                    gain,
                )

            if observation_index < len(times) - 1:
                fine_state = (
                    fine_steps[observation_index] @ fine_state
                )
                coarse_state = (
                    coarse_steps[observation_index] @ coarse_state
                )

        source_summaries.append(
            {
                "case": case_name,
                "source_index": source_index,
                "source_t": float(times[source_index]),
                "source_q_over_H": float(q_over_h[source_index]),
                "maximum_gain": source_maximum,
                "maximum_observation_index": source_maximum_index,
                "maximum_observation_t": float(
                    times[source_maximum_index]
                ),
                "maximum_observation_q_over_H": float(
                    q_over_h[source_maximum_index]
                ),
                "coarse_to_fine_relative_error": (
                    source_maximum_difference
                    / max(source_maximum, 1.0)
                ),
            }
        )

    trace_source_index = int(global_record["source_index"])
    trace_rows: list[dict[str, Any]] = []
    trace_state = sources[trace_source_index].copy()
    for observation_index in range(trace_source_index, len(times)):
        response = readouts[observation_index] @ trace_state
        gain, input_direction, output_direction = spectral_data(response)
        trace_rows.append(
            {
                "case": case_name,
                "source_index": trace_source_index,
                "observation_index": observation_index,
                "source_t": float(times[trace_source_index]),
                "observation_t": float(times[observation_index]),
                "source_q_over_H": float(q_over_h[trace_source_index]),
                "observation_q_over_H": float(
                    q_over_h[observation_index]
                ),
                "gain": gain,
                "crosses_complex_quartet": bool(
                    np.any(
                        quartet_flags[
                            trace_source_index : observation_index + 1
                        ]
                    )
                ),
                "input_Q_rho_weight": direction_weights(
                    input_direction
                )["Q_rho"],
                "input_Q_chi_weight": direction_weights(
                    input_direction
                )["Q_chi"],
                "output_Q_rho_weight": direction_weights(
                    output_direction
                )["Q_rho"],
                "output_Q_chi_weight": direction_weights(
                    output_direction
                )["Q_chi"],
            }
        )
        if observation_index < len(times) - 1:
            trace_state = (
                fine_steps[observation_index] @ trace_state
            )

    result = {
        "maximum_gauge_projected_matter_response": global_maximum,
        "maximum_response_record": global_record,
        "maximum_through_quartet_response": maximum_through_quartet,
        "maximum_through_quartet_record": through_quartet_record,
        "maximum_real_pole_only_response": maximum_real_pole_only,
        "quartet_start_index": quartet_start,
        "quartet_end_index": quartet_end,
        "quartet_start_t": float(times[quartet_start]),
        "quartet_end_t": float(times[quartet_end]),
        "quartet_start_q_over_H": float(q_over_h[quartet_start]),
        "quartet_end_q_over_H": float(q_over_h[quartet_end]),
        "coarse_to_fine_relative_error": (
            maximum_absolute_difference
            / max(global_maximum, 1.0)
        ),
    }
    return result, source_summaries, trace_rows


def evaluate_case(
    case: dict[str, Any],
    symbolic: dict[str, object],
    initial_ratio: float,
    base_substeps: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    params = background_parameters(case["frw"], case["alignment"])
    params["zeta_align"] = case["alignment"]
    series = build_generator_series(
        symbolic,
        params,
        case["rows"],
        initial_ratio,
    )
    projection = build_projection_series(
        symbolic,
        params,
        case["rows"],
        series["comoving_momentum"],
    )
    effective_substeps = max(
        base_substeps,
        int(math.ceil(0.32 / initial_ratio)),
    )
    fine_steps = interval_steps(
        series["exact_generators"],
        series["times"],
        effective_substeps,
    )
    coarse_steps = interval_steps(
        series["exact_generators"],
        series["times"],
        max(1, effective_substeps // 2),
    )
    quartet_flags = off_axis_quartet_flags(
        series["frozen_generators"],
        series["hubbles"],
    )
    response, source_rows, trace_rows = evaluate_response_grid(
        case["name"],
        series,
        projection,
        fine_steps,
        coarse_steps,
        quartet_flags,
    )
    numerical_pass = (
        response["coarse_to_fine_relative_error"] < 5.0e-4
        and projection[
            "maximum_time_orbit_annihilation_residual"
        ]
        < 1.0e-12
        and projection["maximum_direct_Xi_source_support"] < 1.0e-14
        and projection["maximum_direct_Xi_readout_support"] < 1.0e-14
        and projection["maximum_source_position_jump_residual"]
        < 1.0e-12
        and projection["maximum_readout_velocity_support"] < 1.0e-12
        and projection["maximum_source_orthonormality_residual"]
        < 1.0e-12
        and projection["maximum_readout_orthonormality_residual"]
        < 1.0e-12
    )
    survives = response["maximum_through_quartet_response"] > 1.0
    result = {
        "case": case["name"],
        "family": case["family"],
        "variation": case["variation"],
        "initial_q_over_H": initial_ratio,
        "final_q_over_H": float(series["q_over_h"][-1]),
        "effective_midpoint_substeps": effective_substeps,
        "maximum_time_orbit_annihilation_residual": projection[
            "maximum_time_orbit_annihilation_residual"
        ],
        "maximum_direct_Xi_source_support": projection[
            "maximum_direct_Xi_source_support"
        ],
        "maximum_direct_Xi_readout_support": projection[
            "maximum_direct_Xi_readout_support"
        ],
        "maximum_source_position_jump_residual": projection[
            "maximum_source_position_jump_residual"
        ],
        "maximum_readout_velocity_support": projection[
            "maximum_readout_velocity_support"
        ],
        "maximum_source_orthonormality_residual": projection[
            "maximum_source_orthonormality_residual"
        ],
        "maximum_readout_orthonormality_residual": projection[
            "maximum_readout_orthonormality_residual"
        ],
        **response,
        "numerical_status": (
            "PASS_PROJECTED_RETARDED_RESPONSE_NUMERICS"
            if numerical_pass
            else "HOLD_PROJECTED_RETARDED_RESPONSE_NUMERICS"
        ),
        "response_status": (
            "GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_QUARTET"
            if survives
            else "NO_AMPLIFIED_GAUGE_PROJECTED_MATTER_RESPONSE"
        ),
    }
    return result, source_rows, trace_rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    require("positive initial q/H", args.initial_q_over_H > 0)
    require("positive substeps", args.substeps > 0)
    baseline_frw, baseline_rows = load_inputs(
        args.frw_summary,
        args.frw_trajectory,
    )
    symbolic = symbolic_propagators()
    cases = variation_cases(
        baseline_frw,
        baseline_rows,
        args.quick,
    )

    case_results: list[dict[str, Any]] = []
    source_rows: list[dict[str, Any]] = []
    trace_rows: list[dict[str, Any]] = []
    for case in cases:
        result, case_sources, case_trace = evaluate_case(
            case,
            symbolic,
            args.initial_q_over_H,
            args.substeps,
        )
        case_results.append(result)
        source_rows.extend(case_sources)
        trace_rows.extend(case_trace)

    all_numerics_pass = all(
        result["numerical_status"]
        == "PASS_PROJECTED_RETARDED_RESPONSE_NUMERICS"
        for result in case_results
    )
    all_responses_survive = all(
        result["response_status"]
        == "GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_QUARTET"
        for result in case_results
    )
    if not all_numerics_pass:
        subgate_status = "HOLD_SOURCE_OBSERVABLE_RESPONSE_NUMERICS"
    elif all_responses_survive:
        subgate_status = (
            "PASS_GAUGE_PROJECTED_MATTER_RESPONSE_SURVIVES_WITH_SCOPE"
        )
    else:
        subgate_status = "HOLD_GAUGE_PROJECTED_RESPONSE_CLASSIFICATION"

    summary = {
        "gate": "UVIR-003",
        "stage": "B_SOURCE_OBSERVABLE_RETARDED_RESPONSE",
        "calculation_status": (
            "PASS" if subgate_status.startswith("PASS") else "HOLD"
        ),
        "subgate_status": subgate_status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "tested_case_count": len(case_results),
        "all_projected_response_numerics_pass": all_numerics_pass,
        "all_tested_cases_retain_amplified_matter_response": (
            all_responses_survive
        ),
        "method": {
            "coupled_basis": ["Xi", "Q_rho", "Q_chi"],
            "source_covectors": ["Q_rho", "Q_chi"],
            "observable_covectors": ["Q_rho", "Q_chi"],
            "source_rule": (
                "Generalized impulses have zero Xi support and the "
                "corresponding original-field covectors annihilate "
                "(H,rho_dot,mu)."
            ),
            "normalization": (
                "Source columns and observable rows are orthonormalized "
                "inside their retained matter subspaces using the "
                "kinetic-normalized phase-space metric."
            ),
            "retarded_transfer": (
                "Exact time-dependent midpoint-Magnus evolution with "
                "K_dot, P_dot, 3H, and normalization derivatives."
            ),
            "force_mode_scope": (
                "Pi factorizes exactly at quadratic order and is not part "
                "of the coupled complex-quartet block."
            ),
        },
        "case_results": case_results,
        "scientific_boundary": (
            "An amplified Q_rho/Q_chi retarded response from a source "
            "with no Xi or homogeneous time-translation support is a "
            "gauge-projected finite-duration response on the tested "
            "dimensionless branch. It is not by itself an all-background "
            "instability theorem, a physical parameter fit, an S-matrix "
            "amplitude, or a strong-coupling scale."
        ),
        "next_required_calculation": [
            "identify a controlled real-pole and adiabatic exchange domain",
            "project the verified cubic and quartic kernels onto the physical source and observable channels",
            "assemble the gauge-regular exchange plus reduced-contact 2-to-2 amplitude",
            "derive a unitarity or strong-coupling bound only from the completed physical amplitude",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = (
        args.output_dir
        / "uvir003_source_observable_retarded_response_summary.json"
    )
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_csv(
        args.output_dir
        / "uvir003_source_observable_retarded_response_sources.csv",
        source_rows,
    )
    write_csv(
        args.output_dir
        / "uvir003_source_observable_retarded_response_trace.csv",
        trace_rows,
    )

    print("Gauge-projected source covectors: COMPLETE")
    print("Retained Q_rho/Q_chi observables: COMPLETE")
    print(
        "Projected retarded-response numerics: "
        + ("PASS" if all_numerics_pass else "HOLD")
    )
    print(
        "Response through complex-quartet interval: "
        + ("SURVIVES" if all_responses_survive else "UNRESOLVED")
    )
    print("Physical instability theorem: NOT_ESTABLISHED")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(f"STATUS: {subgate_status}")


if __name__ == "__main__":
    main()
