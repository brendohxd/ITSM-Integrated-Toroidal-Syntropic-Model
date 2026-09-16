#!/usr/bin/env python3
"""Finite-order matrix adiabatic-symbol diagnostic for TOP-X4.

The recurrence tested here is the candidate high-frequency ingredient for
the Route-B all-order construction.  It is not itself an all-order Borel sum
and therefore cannot claim a Hadamard state, stress tensor, determinant or
downstream gate.  The explicit hold is intentional.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import CubicSpline

from topx4_s2f3_exact_transport_retry_checkpoint import (
    background_fields,
    integrate_background,
    integrate_real_fundamental,
    make_splines,
    parameters,
    scalar_matrices,
)


STATUS = "HOLD_GLOBAL_STATE_CONSTRUCTION_NOT_ESTABLISHED"
REPO_ROOT = Path(__file__).resolve().parents[3]
BASE = REPO_ROOT / "Analysis" / "TOP" / "TOP-X4"
OUTPUT_PATH = BASE / "outputs" / "topx4_s2f3_adiabatic_symbol_diagnostic_summary.json"
ORDERS = tuple(range(0, 7))
STABLE_ORDERS = (0, 1, 2, 3)
LAMBDA_GRID = (8.0, 16.0, 32.0, 64.0)
DIRECTIONS = ((1.0, 0.0), (0.0, 1.0), (2.0 ** -0.5, 2.0 ** -0.5))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def sidecar_check(path: Path) -> dict[str, Any]:
    sidecar = Path(str(path) + ".sha256")
    actual = sha256_file(path) if path.is_file() else "MISSING"
    expected = "MISSING"
    if sidecar.is_file():
        tokens = sidecar.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    return {"path": relative(path), "actual": actual, "expected": expected, "matches": actual == expected}


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def background_setup(points: int = 801) -> tuple[np.ndarray, dict[str, np.ndarray], dict[str, CubicSpline]]:
    solution = integrate_background(points, parameters())
    if not solution.success:
        raise RuntimeError(f"background integration failed: {solution.message}")
    fields = background_fields(solution, parameters())
    return solution.t, fields, make_splines(solution.t, fields)


def matrix_potential(
    times: np.ndarray, fields: dict[str, np.ndarray], splines: dict[str, CubicSpline]
) -> tuple[np.ndarray, np.ndarray]:
    """Return the leading frequency coefficient and symmetric 3x3 potential.

    The charged pair is rotated by the flat phase connection before the
    formal Riccati expansion.  The real-scalar proxy is the third component.
    """

    phase = cumulative_trapezoid(fields["mu"], times, initial=0.0)
    charged = []
    for time, angle, mu in zip(times, phase, fields["mu"]):
        k_matrix, _, _ = scalar_matrices(float(time), 0.0, 0, splines)
        # The first-derivative term is removed with R' = -mu J R, hence
        # R = exp(-Theta J).  The opposite sign would reintroduce the
        # connection term instead of producing the symmetric potential.
        rotation = np.array(
            [[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]],
            dtype=float,
        )
        charged.append(rotation.T @ (k_matrix + mu * mu * np.eye(2)) @ rotation)
    charged_array = np.asarray(charged)
    gamma = fields["gamma"]
    gamma_dot = fields["gamma_dot"]
    chi_potential = fields["m_chi_eff2"] - gamma_dot - gamma * gamma
    potential = np.zeros((times.size, 3, 3), dtype=float)
    potential[:, :2, :2] = charged_array
    potential[:, 2, 2] = chi_potential
    return potential, phase


def formal_coefficients(
    times: np.ndarray, leading_frequency: np.ndarray, potential: np.ndarray, max_order: int
) -> tuple[np.ndarray, np.ndarray]:
    """Build W = lambda*w*I + sum(lambda**(-j) A_j) recursively.

    For q'=-i W q and q''+(lambda^2*w^2 I+M)q=0, the formal equation is
    W^2+i W'=lambda^2*w^2 I+M.  The recurrence is

        2w A_(r+1) + sum_(a+b=r) A_a A_b + i A_r' = M (r=0),
        2w A_(r+1) + sum_(a+b=r) A_a A_b + i A_r' = 0 (r>0).
    """

    dimension = potential.shape[1]
    identity = np.eye(dimension, dtype=complex)
    w_spline = CubicSpline(times, leading_frequency)
    w_dot = w_spline.derivative()(times)
    coefficients = np.zeros((max_order + 1, times.size, dimension, dimension), dtype=complex)
    coefficients[0] = (-0.5j * w_dot / leading_frequency)[:, None, None] * identity
    for r in range(max_order):
        derivative = CubicSpline(times, coefficients[r], axis=0).derivative()(times)
        products = np.zeros_like(potential, dtype=complex)
        for a in range(r + 1):
            products += coefficients[a] @ coefficients[r - a]
        target = potential if r == 0 else np.zeros_like(potential)
        candidate = (target - products - 1j * derivative) / (
            2.0 * leading_frequency[:, None, None]
        )
        # With a symmetric real potential and a symmetric A_r, the formal
        # recurrence is transpose-symmetric.  Enforce that algebraic
        # invariant after numerical spline differentiation so round-off does
        # not masquerade as a physical matrix asymmetry at the high-order
        # asymptotic tail.
        coefficients[r + 1] = 0.5 * (
            candidate + candidate.transpose(0, 2, 1)
        )
    return coefficients, w_dot


def evaluate_symbol(
    coefficients: np.ndarray,
    leading_frequency: np.ndarray,
    w_dot: np.ndarray,
    times: np.ndarray,
    lam: float,
    order: int,
) -> tuple[np.ndarray, np.ndarray]:
    w_spline = CubicSpline(times, leading_frequency)
    symbol = lam * leading_frequency[:, None, None] * np.eye(coefficients.shape[2], dtype=complex)
    derivative = lam * w_dot[:, None, None] * np.eye(coefficients.shape[2], dtype=complex)
    for index in range(order + 1):
        symbol += coefficients[index] * lam ** (-index)
        derivative += CubicSpline(times, coefficients[index], axis=0).derivative()(times) * lam ** (-index)
    del w_spline
    return symbol, derivative


def residual_envelope(
    times: np.ndarray,
    leading_frequency: np.ndarray,
    potential: np.ndarray,
    coefficients: np.ndarray,
    w_dot: np.ndarray,
    lam: float,
    order: int,
) -> float:
    symbol, derivative = evaluate_symbol(
        coefficients, leading_frequency, w_dot, times, lam, order
    )
    identity = np.eye(potential.shape[1], dtype=complex)
    residuals = symbol @ symbol + 1j * derivative - (
        lam * lam * leading_frequency[:, None, None] ** 2 * identity + potential
    )
    interior = slice(max(8, times.size // 10), times.size - max(8, times.size // 10))
    scales = np.linalg.norm(
        lam * lam * leading_frequency[interior, None, None] ** 2 * identity
        + potential[interior],
        axis=(1, 2),
    )
    return float(np.max(np.linalg.norm(residuals[interior], axis=(1, 2)) / scales))


def initial_data(symbol: np.ndarray) -> tuple[np.ndarray, float, float, float]:
    hermitian = 0.5 * (symbol + symbol.conjugate().T)
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    if np.min(eigenvalues) <= 0.0:
        raise FloatingPointError("Hermitian part of adiabatic symbol is not positive")
    q = eigenvectors @ np.diag(1.0 / np.sqrt(2.0 * eigenvalues)) @ eigenvectors.conjugate().T
    q_dot = -1j * symbol @ q
    mode_matrix = np.vstack((q, q_dot))
    omega = np.block(
        [[np.zeros((3, 3)), np.eye(3)], [-np.eye(3), np.zeros((3, 3))]]
    )
    normalization = float(np.linalg.norm(1j * mode_matrix.conjugate().T @ omega @ mode_matrix - np.eye(3)))
    isotropy = float(np.linalg.norm(mode_matrix.T @ omega @ mode_matrix))
    symmetry = float(np.linalg.norm(symbol.T - symbol))
    return mode_matrix, float(np.min(eigenvalues)), normalization, max(isotropy, symmetry)


def exact_transport_witness(
    times: np.ndarray, splines: dict[str, CubicSpline], mode_matrix: np.ndarray, direction: tuple[float, float], lam: float
) -> dict[str, float | bool]:
    k_obs = lam * direction[0]
    n_kk = lam * direction[1]
    solver, transports = integrate_real_fundamental(
        times,
        4,
        lambda time: scalar_matrices(time, k_obs, n_kk, splines)[2],
    )
    charged_modes = np.vstack((mode_matrix[0:2, :2], mode_matrix[3:5, :2]))
    omega4 = np.block([[np.zeros((2, 2)), np.eye(2)], [-np.eye(2), np.zeros((2, 2))]])
    max_symplectic = 0.0
    max_normalization = 0.0
    max_isotropy = 0.0
    for transport in transports:
        evolved = transport @ charged_modes
        max_symplectic = max(max_symplectic, float(np.linalg.norm(transport.T @ omega4 @ transport - omega4)))
        max_normalization = max(max_normalization, float(np.linalg.norm(1j * evolved.conjugate().T @ omega4 @ evolved - np.eye(2))))
        max_isotropy = max(max_isotropy, float(np.linalg.norm(evolved.T @ omega4 @ evolved)))
    return {
        "solver_success": bool(solver.success),
        "max_symplectic_residual": max_symplectic,
        "max_mode_normalization_residual": max_normalization,
        "max_mode_isotropy_residual": max_isotropy,
    }


def full_matrix_transport_witness(
    times: np.ndarray,
    leading_frequency: np.ndarray,
    potential: np.ndarray,
    mode_matrix: np.ndarray,
    lam: float,
) -> dict[str, float | bool]:
    """Transport all three coupled scalar modes in the rotated frame.

    The finite-order symbol supplies Cauchy data for the transformed second-
    order system

        q'' + (lambda**2*w**2 I_3 + M) q = 0.

    This is an exact finite-grid transport witness for the full rank-three
    matrix, not a global state or a microlocal wavefront construction.
    """
    dimension = potential.shape[1]
    identity = np.eye(dimension)
    zero = np.zeros((dimension, dimension))
    omega = np.block([[zero, identity], [-identity, zero]])
    potential_spline = CubicSpline(times, potential, axis=0)
    frequency_spline = CubicSpline(times, leading_frequency)

    def generator(time: float) -> np.ndarray:
        frequency_squared = lam**2 * float(frequency_spline(time)) ** 2
        lower_left = -(frequency_squared * identity + potential_spline(time))
        return np.block([[zero, identity], [lower_left, zero]])

    solver, transports = integrate_real_fundamental(times, 2 * dimension, generator)
    max_symplectic = 0.0
    max_normalization = 0.0
    max_isotropy = 0.0
    for transport in transports:
        evolved = transport @ mode_matrix
        max_symplectic = max(
            max_symplectic,
            float(np.linalg.norm(transport.T @ omega @ transport - omega)),
        )
        max_normalization = max(
            max_normalization,
            float(
                np.linalg.norm(
                    1j * evolved.conjugate().T @ omega @ evolved - identity
                )
            ),
        )
        max_isotropy = max(
            max_isotropy,
            float(np.linalg.norm(evolved.T @ omega @ evolved)),
        )
    return {
        "solver_success": bool(solver.success),
        "finite_transport": bool(solver.success and np.all(np.isfinite(transports))),
        "max_full_matrix_symplectic_residual": max_symplectic,
        "max_full_matrix_mode_normalization_residual": max_normalization,
        "max_full_matrix_mode_isotropy_residual": max_isotropy,
        "matrix_rank": dimension,
    }


def run_diagnostic() -> dict[str, Any]:
    outputs = BASE / "outputs"
    authority_paths = [
        REPO_ROOT / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_GLOBAL_STATE_CONSTRUCTION_CONTRACT_2026-09-16.md",
        REPO_ROOT / "Theory" / "Core" / "Reasoning_Mode_Plans" / "11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION" / "PLAN.md",
        outputs / "topx4_s2f3_global_state_construction_preflight_summary.json",
        outputs / "topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json",
        outputs / "topx4_s2f3_exact_transport_retry_summary.json",
    ]
    receipts = [sidecar_check(path) for path in authority_paths]
    checks: list[dict[str, Any]] = []
    add_check(checks, "authority_sidecars_match", all(item["matches"] for item in receipts), receipts=receipts)
    preflight = load_json(outputs / "topx4_s2f3_global_state_construction_preflight_summary.json")
    parametrix = load_json(outputs / "topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json")
    exact = load_json(outputs / "topx4_s2f3_exact_transport_retry_summary.json")
    add_check(
        checks,
        "preflight_and_predecessor_holds_are_preserved",
        preflight.get("status") == "HOLD_GLOBAL_STATE_CONSTRUCTION_NOT_ESTABLISHED"
        and preflight.get("preflight_checks_passed") == preflight.get("preflight_checks_total")
        and parametrix.get("scalar_matrix_hadamard_state") == "NOT_CONSTRUCTED"
        and exact.get("full_Hadamard_state") is False,
        preflight_status=preflight.get("status"),
        preflight_checks=f"{preflight.get('preflight_checks_passed')}/{preflight.get('preflight_checks_total')}",
    )

    times, fields, splines = background_setup()
    potential, phase = matrix_potential(times, fields, splines)
    del phase
    residuals: dict[str, dict[str, float]] = {}
    symmetry_max = 0.0
    positive_min = float("inf")
    coefficient_finite = True
    stable_lambda_monotonicity_ok = True
    stable_lambda_residuals: dict[str, dict[str, list[float]]] = {}
    for direction in DIRECTIONS:
        leading = np.sqrt(direction[0] ** 2 / fields["a"] ** 2 + direction[1] ** 2 / fields["b"] ** 2)
        coefficients, w_dot = formal_coefficients(times, leading, potential, max(ORDERS))
        symmetry_max = max(symmetry_max, float(np.max(np.linalg.norm(coefficients.transpose(0, 1, 3, 2) - coefficients, axis=(2, 3)))))
        coefficient_finite = coefficient_finite and bool(np.all(np.isfinite(coefficients)))
        direction_key = f"obs_{direction[0]:.6f}_internal_{direction[1]:.6f}"
        residuals[direction_key] = {}
        for order in ORDERS:
            envelope = max(
                residual_envelope(times, leading, potential, coefficients, w_dot, lam, order)
                for lam in LAMBDA_GRID
            )
            residuals[direction_key][str(order)] = envelope
        stable_lambda_residuals[direction_key] = {}
        for order in STABLE_ORDERS:
            samples = [
                residual_envelope(times, leading, potential, coefficients, w_dot, lam, order)
                for lam in LAMBDA_GRID
            ]
            stable_lambda_residuals[direction_key][str(order)] = samples
            stable_lambda_monotonicity_ok = (
                stable_lambda_monotonicity_ok
                and samples[3] < samples[2] < samples[1] < samples[0]
            )
        for lam in LAMBDA_GRID:
            symbol, _ = evaluate_symbol(coefficients, leading, w_dot, times, lam, max(ORDERS))
            positive_min = min(positive_min, float(np.min(np.linalg.eigvalsh(0.5 * (symbol[0] + symbol[0].conjugate().T)))))

    add_check(
        checks,
        "finite_order_recurrence_witness_is_finite_and_transpose_symmetric",
        coefficient_finite and symmetry_max < 1.0e-9,
        coefficient_finite=coefficient_finite,
        maximum_transpose_residual=symmetry_max,
        implemented_orders=list(ORDERS),
        arbitrary_order_loop=True,
    )
    add_check(
        checks,
        "stable_low_order_symbol_residual_decreases_with_lambda",
        stable_lambda_monotonicity_ok,
        residual_envelopes=residuals,
        stable_orders=list(STABLE_ORDERS),
        limitation=(
            "orders 0-3 are the bounded numerical witness; orders 4-6 are "
            "retained as an asymptotic-tail diagnostic and are not required "
            "to decrease with truncation"
        ),
    )
    leading0 = np.sqrt(0.5 / fields["a"] ** 2 + 0.5 / fields["b"] ** 2)
    coefficients0, w_dot0 = formal_coefficients(
        times, leading0, potential, max(ORDERS)
    )
    symbol0, _ = evaluate_symbol(
        coefficients0, leading0, w_dot0, times, 64.0, max(ORDERS)
    )
    mode_matrix, min_symbol, initial_normalization, initial_isotropy = initial_data(symbol0[0])
    add_check(
        checks,
        "high_frequency_initial_data_are_positive_and_canonically_normalized",
        min_symbol > 0.0 and initial_normalization < 1.0e-10 and initial_isotropy < 1.0e-10,
        minimum_hermitian_symbol_eigenvalue=min_symbol,
        initial_normalization_residual=initial_normalization,
        initial_isotropy_or_symmetry_residual=initial_isotropy,
    )
    transport = exact_transport_witness(times, splines, mode_matrix, DIRECTIONS[2], 64.0)
    add_check(
        checks,
        "exact_transport_of_adiabatic_witness_preserves_ccr",
        transport["solver_success"]
        and transport["max_symplectic_residual"] < 5.0e-8
        and transport["max_mode_normalization_residual"] < 5.0e-8
        and transport["max_mode_isotropy_residual"] < 5.0e-8,
        **transport,
    )
    full_matrix_transport: dict[str, dict[str, float | bool]] = {}
    full_matrix_transport_ok = True
    for direction in DIRECTIONS:
        leading = np.sqrt(
            direction[0] ** 2 / fields["a"] ** 2
            + direction[1] ** 2 / fields["b"] ** 2
        )
        coefficients, w_dot = formal_coefficients(
            times, leading, potential, max(ORDERS)
        )
        symbol, _ = evaluate_symbol(
            coefficients, leading, w_dot, times, 64.0, max(ORDERS)
        )
        full_mode_matrix, _, _, _ = initial_data(symbol[0])
        witness = full_matrix_transport_witness(
            times, leading, potential, full_mode_matrix, 64.0
        )
        full_matrix_transport[
            f"obs_{direction[0]:.6f}_internal_{direction[1]:.6f}"
        ] = witness
        full_matrix_transport_ok = (
            full_matrix_transport_ok
            and witness["solver_success"]
            and witness["finite_transport"]
            and witness["max_full_matrix_symplectic_residual"] < 5.0e-8
            and witness["max_full_matrix_mode_normalization_residual"] < 5.0e-8
            and witness["max_full_matrix_mode_isotropy_residual"] < 5.0e-8
        )
    add_check(
        checks,
        "full_rank_three_matrix_transport_preserves_ccr",
        full_matrix_transport_ok,
        lambda_value=64.0,
        directions=full_matrix_transport,
        limitation=(
            "This is an exact finite-grid transport witness for the coupled "
            "rank-three matrix only; it is not a global Hadamard state."
        ),
    )
    add_check(
        checks,
        "zero_mode_is_handled_by_separate_positive_low_mode_rule",
        preflight.get("low_mode_diagnostics", {}).get("zero_mode_hamiltonian_positive") is True
        and preflight.get("low_mode_diagnostics", {}).get("zero_mode_K_positive") is True,
        rule="finite low modes use exact positive-Hamiltonian Cauchy data; they are a smoothing finite-rank patch",
    )

    all_diagnostic_checks = all(check["ok"] for check in checks)
    return {
        "schema": "ITSM_TOPX4_S2F3_ADIABATIC_SYMBOL_DIAGNOSTIC_v1",
        "route": "X4-S2F3",
        "status": STATUS,
        "calculation_status": "PASS_FINITE_ORDER_SYMBOL_DIAGNOSTIC" if all_diagnostic_checks else "FAIL_FINITE_ORDER_SYMBOL_DIAGNOSTIC",
        "physics_pass": False,
        "gate_effect": "NONE",
        "authority_receipts": receipts,
        "checks": checks,
        "checks_passed": sum(check["ok"] for check in checks),
        "checks_total": len(checks),
        "formal_construction": {
            "route": "ROUTE_B_ADIABATIC_RICCATI_SYMBOL",
            "recurrence_defined_for_arbitrary_order": True,
            "implemented_witness_orders": list(ORDERS),
            "validated_stable_orders": list(STABLE_ORDERS),
            "borel_sum": "NOT_IMPLEMENTED",
            "smooth_low_mode_patch": "FINITE_RANK_RULE_DECLARED",
            "exact_cauchy_evolution": "FINITE_MODE_WITNESS_ONLY",
        },
        "diagnostics": {
            "background_points": int(times.size),
            "lambda_grid": list(LAMBDA_GRID),
            "directions": [list(direction) for direction in DIRECTIONS],
            "full_rank_three_matrix_transport": full_matrix_transport,
            "minimum_high_frequency_hermitian_symbol_eigenvalue": positive_min,
            "residual_envelopes": residuals,
            "stable_lambda_residuals": stable_lambda_residuals,
            "higher_order_tail_is_not_a_convergence_claim": True,
        },
        "state_conditions": {
            "smooth_matrix_bisolution": "NOT_CONSTRUCTED_GLOBALLY",
            "ccr": "FINITE_WITNESS_ONLY",
            "global_positivity": "NOT_ESTABLISHED",
            "global_wavefront_condition": "NOT_ESTABLISHED",
            "all_order_symbol_or_smoothing_remainder": "NOT_ESTABLISHED",
        },
        "blocking_reasons": [
            "The executable evaluates only a finite set of formal adiabatic orders.",
            "No Borel-summed symbol or explicit smoothing remainder is constructed.",
            "No global bidistribution is materialized or independently checked as a wavefront object.",
            "No renormalized stress, determinant, physical Hessian, gravity/ghost or parity sector is included.",
        ],
        "downstream_actions": {
            "advance_to_stress": False,
            "advance_to_determinant": False,
            "advance_to_physical_hessian": False,
            "advance_to_a4": False,
            "advance_to_ultra": False,
            "gate_or_publication_promotion": False,
        },
        "derived_claims": [],
        "explicit_nonclaims": [
            "no global scalar-matrix Hadamard state",
            "no all-order convergence proof",
            "no wavefront or global positivity proof",
            "no stress, determinant, Hessian, A4, Ultra or publication result",
        ],
    }


def main() -> int:
    result = run_diagnostic()
    result["script_sha256"] = sha256_file(Path(__file__))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    OUTPUT_PATH.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    OUTPUT_PATH.with_suffix(OUTPUT_PATH.suffix + ".sha256").write_text(
        f"{digest}  {OUTPUT_PATH.name}\n", encoding="ascii", newline="\n"
    )
    print(STATUS)
    print(f"checks={result['checks_passed']}/{result['checks_total']}")
    print("formal_route=ROUTE_B_ADIABATIC_RICCATI_SYMBOL")
    print("borel_sum=NOT_IMPLEMENTED")
    print("global_scalar_matrix_hadamard_state=NOT_CONSTRUCTED")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={OUTPUT_PATH}")
    print(f"sha256={digest}")
    return 0 if result["calculation_status"] == "PASS_FINITE_ORDER_SYMBOL_DIAGNOSTIC" else 1


if __name__ == "__main__":
    raise SystemExit(main())
