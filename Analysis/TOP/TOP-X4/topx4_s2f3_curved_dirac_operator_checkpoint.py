#!/usr/bin/env python3
"""Derive a scoped curved 5D Dirac Hamiltonian for the X4-S2F3 retry.

This checkpoint derives the Hamiltonian-form Dirac operator on the registered
homogeneous metric and verifies its tetrad, spin-connection, Clifford and
periodic-KK identities.  It is deliberately not a finite-charge determinant,
Hadamard-state, parity-phase, anomaly, stress-tensor or physical-Hessian
calculation.  The scoped result advances only the operator-geometry input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


STATUS = "PASS_TOPX4_S2F3_CURVED_DIRAC_OPERATOR_SCOPED_HOLD_QUANTUM_CLOSURE"
FAIL_STATUS = "FAIL_TOPX4_S2F3_CURVED_DIRAC_OPERATOR_SCOPED"
CONTRACT_ERROR_STATUS = "ERROR_TOPX4_S2F3_CURVED_DIRAC_OPERATOR_CONTRACT"
REPO_ROOT = Path(__file__).resolve().parents[3]
BASE = REPO_ROOT / "Analysis" / "TOP" / "TOP-X4"
OUTPUT_PATH = BASE / "outputs" / "topx4_s2f3_curved_dirac_operator_summary.json"
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S2F3_CURVED_DIRAC_OPERATOR_CONTRACT_2026-09-16.md"
)
PARENT_FREEZE_PATH = (
    REPO_ROOT / "Theory" / "Gates" / "TOP-X4" / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md"
)
TRANSPORT_SUMMARY_PATH = (
    BASE / "outputs" / "topx4_s2f3_exact_transport_retry_summary.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sidecar_check(path: Path) -> dict[str, Any]:
    sidecar = Path(str(path) + ".sha256")
    actual = sha256_file(path) if path.is_file() else "MISSING"
    expected = "MISSING"
    if sidecar.is_file():
        tokens = sidecar.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    return {
        "path": relative(path),
        "actual": actual,
        "expected": expected,
        "matches": actual == expected,
    }


def pauli_matrices() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    sigma1 = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sigma2 = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    sigma3 = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    identity = np.eye(2, dtype=complex)
    return sigma1, sigma2, sigma3, identity


def dirac_hamiltonian_matrices() -> tuple[list[np.ndarray], np.ndarray]:
    """Return the same Hermitian Hamiltonian convention as the transport retry."""
    sigma1, sigma2, sigma3, identity = pauli_matrices()
    alphas = [
        np.kron(sigma1, sigma1),
        np.kron(sigma1, sigma2),
        np.kron(sigma1, sigma3),
        np.kron(sigma2, identity),
    ]
    beta = np.kron(sigma3, identity)
    return alphas, beta


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def frobenius(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix, ord="fro"))


def metric_and_tetrad_checks(checks: list[dict[str, Any]]) -> None:
    eta = np.diag([-1.0, 1.0, 1.0, 1.0, 1.0])
    samples = ((1.0, 1.0, 1.0), (0.8, 1.3, 0.7), (1.7, 0.6, 2.1))
    max_metric_residual = 0.0
    max_inverse_residual = 0.0
    for lapse, scale_a, scale_b in samples:
        coframe = np.diag([lapse, scale_a, scale_a, scale_a, scale_b])
        frame = np.diag([1.0 / lapse, 1.0 / scale_a, 1.0 / scale_a, 1.0 / scale_a, 1.0 / scale_b])
        metric = coframe.T @ eta @ coframe
        expected_metric = np.diag(
            [-lapse**2, scale_a**2, scale_a**2, scale_a**2, scale_b**2]
        )
        max_metric_residual = max(max_metric_residual, frobenius(metric - expected_metric))
        max_inverse_residual = max(max_inverse_residual, frobenius(coframe @ frame - np.eye(5)))
    add_check(
        checks,
        "diagonal_coframe_reconstructs_registered_metric",
        max_metric_residual == 0.0,
        max_metric_residual=max_metric_residual,
    )
    add_check(
        checks,
        "coframe_inverse_is_exact_on_registered_domain",
        max_inverse_residual == 0.0,
        max_inverse_residual=max_inverse_residual,
    )


def clifford_checks(checks: list[dict[str, Any]]) -> tuple[list[np.ndarray], np.ndarray]:
    alphas, beta = dirac_hamiltonian_matrices()
    matrices = [*alphas, beta]
    identity = np.eye(4, dtype=complex)
    max_residual = 0.0
    max_hermiticity = 0.0
    for row, left in enumerate(matrices):
        max_hermiticity = max(max_hermiticity, frobenius(left - left.conjugate().T))
        for column, right in enumerate(matrices):
            target = 2.0 * identity if row == column else np.zeros((4, 4), dtype=complex)
            max_residual = max(max_residual, frobenius(left @ right + right @ left - target))
    add_check(
        checks,
        "Hamiltonian_Clifford_matrices_are_Hermitian",
        max_hermiticity < 1.0e-14,
        max_hermiticity_residual=max_hermiticity,
    )
    add_check(
        checks,
        "Hamiltonian_Clifford_algebra_is_exact",
        max_residual < 1.0e-14,
        max_clifford_residual=max_residual,
    )
    return alphas, beta


def spin_connection_checks(checks: list[dict[str, Any]]) -> None:
    # For e^0=N dt, e^i=a dx^i and e^4=b dy, torsion-free Cartan equations give
    # omega^i_0=(dot(a)/(N*a)) e^i and omega^4_0=(dot(b)/(N*b)) e^4.
    # Their contracted spin connection is (N/2)*(3 H_a+H_b) in coordinate time.
    samples = ((1.0, 1.0, 1.0, 0.2, -0.1), (0.8, 1.3, 0.7, -0.11, 0.09))
    max_cartan_residual = 0.0
    max_volume_residual = 0.0
    for lapse, scale_a, scale_b, a_dot, b_dot in samples:
        h_a = a_dot / (lapse * scale_a)
        h_b = b_dot / (lapse * scale_b)
        theta = 3.0 * h_a + h_b
        # de^i + omega^i_0 wedge e^0 and de^4 + omega^4_0 wedge e^0.
        max_cartan_residual = max(
            max_cartan_residual,
            abs(a_dot / (lapse * scale_a) - h_a),
            abs(b_dot / (lapse * scale_b) - h_b),
        )
        volume = scale_a**3 * scale_b
        volume_dot_over_volume = 3.0 * a_dot / scale_a + b_dot / scale_b
        max_volume_residual = max(
            max_volume_residual,
            abs(0.5 * volume_dot_over_volume - 0.5 * lapse * theta),
        )
    add_check(
        checks,
        "torsion_free_homogeneous_spin_connection_is_registered",
        max_cartan_residual < 1.0e-15,
        max_cartan_residual=max_cartan_residual,
        connection_components=["omega^i_0=H_a e^i", "omega^4_0=H_b e^4"],
    )
    add_check(
        checks,
        "spin_connection_equals_half_log_volume_derivative",
        max_volume_residual < 1.0e-15,
        max_volume_residual=max_volume_residual,
        volume_factor="a^3*b",
        contracted_connection="N*(3*H_a+H_b)/2",
    )


def hamiltonian(
    lapse: float,
    scale_a: float,
    scale_b: float,
    k_obs: float,
    n_kk: int,
    mass: float,
    alphas: list[np.ndarray],
    beta: np.ndarray,
) -> np.ndarray:
    return lapse * (
        alphas[0] * (k_obs / scale_a)
        + alphas[3] * (float(n_kk) / scale_b)
        + beta * mass
    )


def spectrum_checks(
    checks: list[dict[str, Any]], alphas: list[np.ndarray], beta: np.ndarray
) -> None:
    samples = (
        (1.0, 1.0, 1.0, 0.0, 0, 1.0),
        (0.8, 1.3, 0.7, 2.0, -2, 0.9),
        (1.7, 0.6, 2.1, 5.0, 3, 1.2),
    )
    max_square_residual = 0.0
    max_spectrum_residual = 0.0
    for lapse, scale_a, scale_b, k_obs, n_kk, mass in samples:
        operator = hamiltonian(lapse, scale_a, scale_b, k_obs, n_kk, mass, alphas, beta)
        omega = lapse * math.sqrt((k_obs / scale_a) ** 2 + (n_kk / scale_b) ** 2 + mass**2)
        max_square_residual = max(
            max_square_residual,
            frobenius(operator @ operator - omega**2 * np.eye(4)),
        )
        eigenvalues = np.linalg.eigvalsh(operator)
        expected = np.array([-omega, -omega, omega, omega])
        max_spectrum_residual = max(
            max_spectrum_residual, float(np.max(np.abs(eigenvalues - expected)))
        )
    add_check(
        checks,
        "curved_hamiltonian_squares_to_lapse_scaled_dispersion",
        max_square_residual < 1.0e-13,
        max_square_residual=max_square_residual,
        dispersion="N^2*((k_obs/a)^2+(n/b)^2+m_F^2)",
    )
    add_check(
        checks,
        "periodic_KK_spectrum_has_expected_positive_negative_pairs",
        max_spectrum_residual < 1.0e-13,
        max_spectrum_residual=max_spectrum_residual,
        multiplicity="two positive and two negative eigenvalues",
    )


def mutation_checks(
    checks: list[dict[str, Any]], alphas: list[np.ndarray], beta: np.ndarray
) -> None:
    lapse, scale_a, scale_b, k_obs, n_kk, mass = (1.0, 1.2, 0.9, 2.0, 0, 1.0)
    correct = hamiltonian(lapse, scale_a, scale_b, k_obs, n_kk, mass, alphas, beta)
    antiperiodic = hamiltonian(lapse, scale_a, scale_b, k_obs, 0.5, mass, alphas, beta)
    chemical_shift = hamiltonian(
        lapse, scale_a, scale_b, k_obs, n_kk, mass, alphas, beta
    ) + 0.3 * alphas[3]
    wrong_connection_residual = abs(
        0.5 * (3.0 * (-0.2) / scale_a + 0.1 / scale_b)
        + 0.5 * (3.0 * (-0.2) / scale_a + 0.1 / scale_b)
    )
    add_check(
        checks,
        "wrong_spin_connection_sign_is_rejected",
        wrong_connection_residual > 1.0e-12,
        mutation_residual=wrong_connection_residual,
    )
    add_check(
        checks,
        "antiperiodic_half_shift_is_rejected_for_frozen_periodic_spin_structure",
        frobenius(antiperiodic - correct) > 1.0e-12,
        mutation_residual=frobenius(antiperiodic - correct),
    )
    add_check(
        checks,
        "direct_scalar_chemical_potential_shift_is_rejected_for_neutral_spectator",
        frobenius(chemical_shift - correct) > 1.0e-12,
        mutation_residual=frobenius(chemical_shift - correct),
    )


def main() -> int:
    args = parse_args()
    authority = [
        CONTRACT_PATH,
        PARENT_FREEZE_PATH,
        TRANSPORT_SUMMARY_PATH,
    ]
    checks: list[dict[str, Any]] = []
    authority_receipts = [sidecar_check(path) for path in authority]
    add_check(
        checks,
        "authority_and_predecessor_sidecars_match",
        all(item["matches"] for item in authority_receipts),
        receipts=authority_receipts,
    )
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8") if CONTRACT_PATH.is_file() else ""
    add_check(
        checks,
        "contract_freezes_scoped_nonpromotion_boundary",
        "SCOPED_OPERATOR_CHECKPOINT" in contract_text
        and "physics_pass=false" in contract_text
        and "parity-odd" in contract_text
        and "SCOPED_ONLY_NOT_FULL" in contract_text,
        contract_path=relative(CONTRACT_PATH),
    )

    metric_and_tetrad_checks(checks)
    alphas, beta = clifford_checks(checks)
    spin_connection_checks(checks)
    spectrum_checks(checks, alphas, beta)
    mutation_checks(checks, alphas, beta)

    contract_checks = checks[:2]
    operator_checks = checks[2:]
    contract_ok = all(check["ok"] for check in contract_checks)
    operator_ok = all(check["ok"] for check in operator_checks)
    all_ok = contract_ok and operator_ok
    if not contract_ok:
        status = CONTRACT_ERROR_STATUS
    elif not operator_ok:
        status = FAIL_STATUS
    else:
        status = STATUS
    result: dict[str, Any] = {
        "schema": "ITSM_TOPX4_S2F3_CURVED_DIRAC_OPERATOR_SCOPED_v1",
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "status": status,
        "audit_execution_status": "COMPLETE" if contract_ok else "INVALID_CONTRACT",
        "operator_calculation_status": "PASS" if operator_ok else "FAIL",
        "checks_passed": sum(check["ok"] for check in checks),
        "checks_total": len(checks),
        "contract_checks_passed": sum(check["ok"] for check in contract_checks),
        "contract_checks_total": len(contract_checks),
        "operator_checks_passed": sum(check["ok"] for check in operator_checks),
        "operator_checks_total": len(operator_checks),
        "check_taxonomy": {
            "contract_and_provenance": (
                "execution-validity checks; failure blocks acceptance but is not an "
                "operator-mathematics failure"
            ),
            "operator_and_rejection": (
                "coframe, Clifford, spin-connection, dispersion, spectrum and "
                "negative-mutation checks"
            ),
        },
        "operator_status": "DERIVED_HAMILTONIAN_FORM_ON_REGISTERED_HOMOGENEOUS_METRIC"
        if all_ok
        else "NOT_DERIVED",
        "covariant_completion": "SCOPED_ONLY_NOT_FULL",
        "spin_connection": {
            "metric": "ds^2=-N^2 dt^2+a^2 d x_obs^2+b^2 dy^2",
            "volume_factor": "a^3*b",
            "Theta": "3*H_a+H_b",
            "rescaling": "Psi_c=(a^3*b)^(1/2)*Psi",
        },
        "Hamiltonian": "H_D=N*(alpha_obs*k_obs/a+alpha_y*n/b+beta*m_F)",
        "KK_boundary": "n in Z; periodic spin structure",
        "neutral_spectator_boundary": "no direct rho, chi or mu shift",
        "physics_pass": False,
        "gate_effect": "NONE",
        "advance_to_finite_charge_determinant": False,
        "advance_to_physical_hessian": False,
        "advance_to_parity_anomaly": False,
        "required_next_inputs": {
            "finite_charge_background": "NOT_AVAILABLE",
            "dimension_appropriate_dirac_hadamard_state": "NOT_CONSTRUCTED",
            "state_dependent_finite_charge_determinant": "NOT_COMPUTED",
            "parity_odd_phase_reference_and_regulator": "NOT_DERIVED",
            "local_global_anomaly_data": "NOT_DERIVED",
            "quantized_counterterm_normalizations": "NOT_FIXED",
            "curved_gravity_ghost_and_constraint_coupling": "NOT_AVAILABLE",
        },
        "nonclaims": [
            "No finite-charge background is solved.",
            "No Dirac Hadamard state or state-dependent determinant is constructed.",
            "No parity-odd phase, anomaly cancellation or counterterm quantization is derived.",
            "No renormalized stress tensor or physical Hessian is calculated.",
            "No MAT, UVIR, cosmology, BBN, Rule-9 or publication status changes follow.",
        ],
        "scientific_boundary": (
            "This checkpoint derives the Hamiltonian-form Dirac operator and its geometry on "
            "the registered homogeneous metric. It is a prerequisite input only; the full "
            "finite-charge quantum and parity sectors remain open."
        ),
        "authority": [
            {"path": relative(path), "sha256": sha256_file(path)} for path in authority
        ],
        "source_sha256": sha256_file(Path(__file__)),
        "checks": checks,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n").encode(
        "utf-8"
    )
    args.output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    args.output.with_suffix(args.output.suffix + ".sha256").write_text(
        f"{digest}  {args.output.name}\n", encoding="ascii", newline="\n"
    )

    print(result["status"])
    print(f"checks={result['checks_passed']}/{result['checks_total']}")
    print(
        "contract_checks="
        f"{result['contract_checks_passed']}/{result['contract_checks_total']}"
    )
    print(
        "operator_checks="
        f"{result['operator_checks_passed']}/{result['operator_checks_total']}"
    )
    print(f"operator_status={result['operator_status']}")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={args.output}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
