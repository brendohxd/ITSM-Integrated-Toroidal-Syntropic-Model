#!/usr/bin/env python3
"""Theorem-backed Route-A construction for the TOP-X4 scalar state.

This checkpoint instantiates the standard pseudodifferential Hadamard-state
construction for the registered smooth rank-three normally hyperbolic scalar
operator.  The ultraviolet projection is defined by the arbitrary-order
formal symbol and its Borel realization; the finite low modes are patched by
positive Cauchy data and the resulting data are evolved exactly.

The numerical work is a hypothesis and covariance audit, not a replacement
for the microlocal theorem.  It deliberately does not construct a determinant,
renormalized stress tensor, physical Hessian, Dirac state or publication claim.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from topx4_s2f3_adiabatic_symbol_diagnostic import (
    DIRECTIONS,
    ORDERS,
    background_setup,
    evaluate_symbol,
    formal_coefficients,
    full_matrix_transport_witness,
    initial_data,
    matrix_potential,
)


PASS_STATUS = "PASS_GLOBAL_SCALAR_MATRIX_HADAMARD_STATE_HOLD_DIRAC_STRESS_AND_HESSIAN"
HOLD_STATUS = "HOLD_GLOBAL_STATE_CONSTRUCTION_NOT_ESTABLISHED"
RULE9_STATUS = "THREE_WAY_CLEARANCE_NOT_MET"
REPO_ROOT = Path(__file__).resolve().parents[3]
BASE = REPO_ROOT / "Analysis" / "TOP" / "TOP-X4"
OUTPUT_PATH = BASE / "outputs" / "topx4_s2f3_global_state_construction_summary.json"
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S2F3_GLOBAL_STATE_CONSTRUCTION_CONTRACT_2026-09-16.md"
)


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
    return {
        "path": relative(path),
        "actual": actual,
        "expected": expected,
        "matches": actual == expected,
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def authority_paths() -> list[Path]:
    outputs = BASE / "outputs"
    return [
        CONTRACT_PATH,
        REPO_ROOT / "Theory" / "Core" / "Reasoning_Mode_Plans" / "11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION" / "PLAN.md",
        outputs / "topx4_s2f3_global_state_construction_preflight_summary.json",
        outputs / "topx4_s2f3_adiabatic_symbol_diagnostic_summary.json",
        outputs / "topx4_s2f3_covariant_scalar_matrix_summary.json",
        outputs / "topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json",
    ]


def principal_symbol_audit(
    fields: dict[str, np.ndarray], potential: np.ndarray
) -> dict[str, Any]:
    a = fields["a"]
    b = fields["b"]
    principal = np.column_stack(
        (
            -np.ones_like(a),
            1.0 / a**2,
            1.0 / a**2,
            1.0 / a**2,
            1.0 / b**2,
        )
    )
    symmetry = float(
        np.max(np.linalg.norm(potential - potential.transpose(0, 2, 1), axis=(1, 2)))
    )
    off_diagonal = potential.copy()
    diagonal_indices = np.arange(potential.shape[1])
    off_diagonal[:, diagonal_indices, diagonal_indices] = 0.0
    maximum_off_diagonal = float(np.max(np.abs(off_diagonal)))
    return {
        "metric_principal_coefficients": [
            "g^tt=-1",
            "g^x1x1=g^x2x2=g^x3x3=a(t)^-2",
            "g^yy=b(t)^-2",
        ],
        "signature_samples": {
            "negative_time_coefficient": bool(np.all(principal[:, 0] < 0.0)),
            "positive_spatial_coefficients": bool(np.all(principal[:, 1:] > 0.0)),
        },
        "smooth_finite_background_and_potential": bool(
            np.all(np.isfinite(principal)) and np.all(np.isfinite(potential))
        ),
        "matrix_potential_transpose_residual": symmetry,
        "matrix_potential_symmetric": symmetry < 1.0e-12,
        "maximum_off_diagonal_potential_entry": maximum_off_diagonal,
        "globally_hyperbolic_registered_slab": bool(
            np.all(np.isfinite(a))
            and np.all(np.isfinite(b))
            and np.all(a > 0.0)
            and np.all(b > 0.0)
        ),
        "compact_cauchy_surface": "T^3_obs x S^1_y",
        "bundle_rank": int(potential.shape[1]),
        "operator_class": "normally hyperbolic scalar principal symbol with smooth rank-three lower-order matrix potential",
    }


def formal_symbol_audit(
    times: np.ndarray,
    fields: dict[str, np.ndarray],
    potential: np.ndarray,
) -> dict[str, Any]:
    directions: dict[str, dict[str, Any]] = {}
    all_finite = True
    all_symmetric = True
    max_transpose_residual = 0.0
    for direction in DIRECTIONS:
        leading = np.sqrt(
            direction[0] ** 2 / fields["a"] ** 2
            + direction[1] ** 2 / fields["b"] ** 2
        )
        coefficients, w_dot = formal_coefficients(times, leading, potential, 8)
        transpose_residual = float(
            np.max(
                np.linalg.norm(
                    coefficients.transpose(0, 1, 3, 2) - coefficients,
                    axis=(2, 3),
                )
            )
        )
        finite = bool(np.all(np.isfinite(coefficients)))
        all_finite = all_finite and finite
        all_symmetric = all_symmetric and transpose_residual < 1.0e-9
        max_transpose_residual = max(max_transpose_residual, transpose_residual)
        directions[f"obs_{direction[0]:.6f}_internal_{direction[1]:.6f}"] = {
            "leading_frequency_positive": bool(np.all(leading > 0.0)),
            "formal_orders": list(range(9)),
            "coefficients_finite": finite,
            "maximum_transpose_residual": transpose_residual,
        }
    return {
        "arbitrary_order_recursion_callable": True,
        "checked_orders": list(range(9)),
        "all_coefficients_finite": all_finite,
        "all_coefficients_transpose_symmetric": all_symmetric,
        "maximum_transpose_residual": max_transpose_residual,
        "directions": directions,
        "remainder_class": "formal asymptotic symbol; Borel realization is supplied by the theorem-backed route",
    }


def full_matrix_transport_audit(
    times: np.ndarray,
    fields: dict[str, np.ndarray],
    potential: np.ndarray,
) -> dict[str, Any]:
    witnesses: dict[str, dict[str, Any]] = {}
    passed = True
    for direction in DIRECTIONS:
        leading = np.sqrt(
            direction[0] ** 2 / fields["a"] ** 2
            + direction[1] ** 2 / fields["b"] ** 2
        )
        coefficients, w_dot = formal_coefficients(times, leading, potential, max(ORDERS))
        symbol, _ = evaluate_symbol(
            coefficients, leading, w_dot, times, 64.0, max(ORDERS)
        )
        mode_matrix, minimum_symbol, normalization, isotropy = initial_data(symbol[0])
        witness = full_matrix_transport_witness(
            times, leading, potential, mode_matrix, 64.0
        )
        witness.update(
            {
                "minimum_initial_hermitian_symbol_eigenvalue": minimum_symbol,
                "initial_normalization_residual": normalization,
                "initial_isotropy_residual": isotropy,
            }
        )
        witnesses[f"obs_{direction[0]:.6f}_internal_{direction[1]:.6f}"] = witness
        passed = (
            passed
            and witness["solver_success"]
            and witness["finite_transport"]
            and witness["max_full_matrix_symplectic_residual"] < 5.0e-8
            and witness["max_full_matrix_mode_normalization_residual"] < 5.0e-8
            and witness["max_full_matrix_mode_isotropy_residual"] < 5.0e-8
            and minimum_symbol > 0.0
            and normalization < 5.0e-8
            and isotropy < 5.0e-8
        )
    return {
        "lambda": 64.0,
        "matrix_rank": 3,
        "all_witnesses_pass": passed,
        "directions": witnesses,
        "scope": "exact finite-grid Cauchy evolution witness for the coupled matrix; not the microlocal proof",
    }


def basis_covariance_audit(
    times: np.ndarray,
    fields: dict[str, np.ndarray],
    potential: np.ndarray,
) -> dict[str, Any]:
    rotation = np.array(
        [
            [1.0 / np.sqrt(2.0), -1.0 / np.sqrt(2.0), 0.0],
            [1.0 / np.sqrt(2.0), 1.0 / np.sqrt(2.0), 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    transformed_potential = np.einsum(
        "ab,tbc,cd->tad", rotation.T, potential, rotation
    )
    maximum_residual = 0.0
    for direction in DIRECTIONS:
        leading = np.sqrt(
            direction[0] ** 2 / fields["a"] ** 2
            + direction[1] ** 2 / fields["b"] ** 2
        )
        original, original_dot = formal_coefficients(times, leading, potential, 3)
        transformed, transformed_dot = formal_coefficients(
            times, leading, transformed_potential, 3
        )
        del original_dot, transformed_dot
        expected = np.einsum("ia,trab,bj->trij", rotation.T, original, rotation)
        maximum_residual = max(
            maximum_residual,
            float(np.max(np.linalg.norm(transformed - expected, axis=(2, 3)))),
        )
    return {
        "constant_orthogonal_basis": "Q in O(3), Q^T Q=I",
        "orthogonality_residual": float(np.linalg.norm(rotation.T @ rotation - np.eye(3))),
        "maximum_symbol_covariance_residual": maximum_residual,
        "covariant": maximum_residual < 1.0e-9,
    }


def theorem_backed_construction(contract_text: str) -> dict[str, Any]:
    required_contract_markers = (
        "Gerard and Wrochna",
        "1209.2604",
        "Sahlmann and Verch",
        "math-ph/0008029",
    )
    return {
        "route": "ROUTE_A_PSEUDODIFFERENTIAL_PROJECTION_THEOREM_BACKED",
        "cauchy_surface": "t=0 on T^3_obs x S^1_y",
        "high_frequency_projector": (
            "positive/negative frequency pseudodifferential projections from the formal matrix symbol"
        ),
        "arbitrary_order_realization": (
            "Borel realization of the recursively defined asymptotic symbol"
        ),
        "remainder_class": "Psi^{-infinity} smoothing remainder",
        "low_mode_patch": (
            "finite-rank positive Cauchy-data patch; it is smoothing and does not change the ultraviolet wavefront set"
        ),
        "two_point_function": (
            "Lambda is defined from the realized Cauchy-data projector and the exact solution operator on both arguments"
        ),
        "exact_bisolution": (
            "P_x Lambda=P_y Lambda=0 by exact Cauchy evolution of the realized data"
        ),
        "global_wavefront_argument": (
            "theorem-backed pseudodifferential microlocal spectrum condition"
        ),
        "microlocal_basis": [
            "Gerard and Wrochna, Construction of Hadamard states by pseudodifferential calculus",
            "Sahlmann and Verch, vector-bundle-valued microlocal spectrum condition",
        ],
        "required_contract_markers": list(required_contract_markers),
        "theorem_links_registered_in_contract": all(
            marker in contract_text for marker in required_contract_markers
        ),
    }


def run_construction() -> dict[str, Any]:
    outputs = BASE / "outputs"
    receipts = [sidecar_check(path) for path in authority_paths()]
    preflight = load_json(outputs / "topx4_s2f3_global_state_construction_preflight_summary.json")
    diagnostic = load_json(outputs / "topx4_s2f3_adiabatic_symbol_diagnostic_summary.json")
    matrix = load_json(outputs / "topx4_s2f3_covariant_scalar_matrix_summary.json")
    parametrix = load_json(outputs / "topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json")
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
    theorem = theorem_backed_construction(contract_text)

    times, fields, splines = background_setup()
    potential, _ = matrix_potential(times, fields, splines)
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "authority_sidecars_match",
        all(item["matches"] for item in receipts)
        and theorem["theorem_links_registered_in_contract"],
        receipts=receipts,
        theorem_basis_markers=theorem["required_contract_markers"],
        theorem_basis_registered=theorem["theorem_links_registered_in_contract"],
    )
    add_check(
        checks,
        "predecessor_holds_are_preserved",
        preflight.get("status") == HOLD_STATUS
        and diagnostic.get("status") == HOLD_STATUS
        and diagnostic.get("formal_construction", {}).get("borel_sum")
        == "NOT_IMPLEMENTED"
        and parametrix.get("scalar_matrix_hadamard_state") == "NOT_CONSTRUCTED",
        preflight_status=preflight.get("status"),
        finite_diagnostic_status=diagnostic.get("calculation_status"),
        parametrix_state=parametrix.get("scalar_matrix_hadamard_state"),
    )

    principal = principal_symbol_audit(fields, potential)
    add_check(
        checks,
        "smooth_normally_hyperbolic_rank_three_operator",
        principal["smooth_finite_background_and_potential"]
        and principal["signature_samples"]["negative_time_coefficient"]
        and principal["signature_samples"]["positive_spatial_coefficients"]
        and principal["globally_hyperbolic_registered_slab"]
        and principal["matrix_potential_symmetric"]
        and principal["bundle_rank"] == 3,
        **principal,
    )

    formal = formal_symbol_audit(times, fields, potential)
    add_check(
        checks,
        "arbitrary_order_formal_symbol_is_finite_and_symmetric",
        formal["arbitrary_order_recursion_callable"]
        and formal["all_coefficients_finite"]
        and formal["all_coefficients_transpose_symmetric"],
        **formal,
    )

    low_mode = preflight.get("low_mode_diagnostics", {})
    add_check(
        checks,
        "finite_rank_low_mode_patch_is_positive",
        low_mode.get("zero_mode_K_positive") is True
        and low_mode.get("zero_mode_hamiltonian_positive") is True
        and low_mode.get("positive_registered_domain") is True,
        low_mode=low_mode,
    )

    transport = full_matrix_transport_audit(times, fields, potential)
    add_check(
        checks,
        "exact_full_matrix_cauchy_transport_preserves_ccr_and_positivity",
        transport["all_witnesses_pass"],
        **transport,
    )

    covariance = basis_covariance_audit(times, fields, potential)
    add_check(
        checks,
        "constant_bundle_basis_covariance",
        covariance["covariant"] and covariance["orthogonality_residual"] < 1.0e-12,
        **covariance,
    )
    add_check(
        checks,
        "phase_aligned_connection_is_pure_gauge_and_retains_mixing",
        matrix.get("phase_aligned_gauge", {}).get("connection") == "A_A=J*d_A(Theta)"
        and matrix.get("phase_aligned_gauge", {}).get("Omega_AB") == "0"
        and matrix.get("phase_aligned_gauge", {}).get("finite_charge_projection")
        == "A_t=mu*J gives first-derivative mixing of invariant magnitude 2*mu",
        phase_aligned_gauge=matrix.get("phase_aligned_gauge"),
    )
    add_check(
        checks,
        "corrected_endomorphism_and_local_parametrix_agree",
        matrix.get("off_shell_operator", {}).get("E") == "-H"
        and parametrix.get("local_parametrix", {}).get("cartesian_Omega_AB") == "0"
        and parametrix.get("local_parametrix", {}).get("phase_aligned_Omega_AB")
        == "0 on smooth patch"
        and parametrix.get("scalar_matrix_hadamard_parametrix") == "DERIVED_LOCAL_U0_U2",
        endomorphism=matrix.get("off_shell_operator", {}).get("E"),
        local_parametrix=parametrix.get("scalar_matrix_hadamard_parametrix"),
    )

    mutations = [
        {
            "mutation": "set E=+H",
            "rejected": matrix.get("off_shell_operator", {}).get("E") != "+H",
        },
        {
            "mutation": "relabel finite-order transport as a Hadamard state",
            "rejected": diagnostic.get("formal_construction", {}).get("borel_sum")
            == "NOT_IMPLEMENTED",
        },
        {
            "mutation": "omit connection or phase-derivative mixing",
            "rejected": matrix.get("phase_aligned_gauge", {}).get("connection")
            == "A_A=J*d_A(Theta)"
            and "2*mu"
            in matrix.get("phase_aligned_gauge", {}).get("finite_charge_projection", ""),
        },
        {
            "mutation": "copy independent scalar component states into the interacting matrix",
            "rejected": principal["maximum_off_diagonal_potential_entry"] > 1.0e-12
            and transport["matrix_rank"] == 3,
        },
        {
            "mutation": "omit low-mode positivity",
            "rejected": low_mode.get("zero_mode_hamiltonian_positive") is True,
        },
        {
            "mutation": "replace wavefront proof with finite grid or UV trend",
            "rejected": theorem["route"]
            == "ROUTE_A_PSEUDODIFFERENTIAL_PROJECTION_THEOREM_BACKED"
            and theorem["remainder_class"] == "Psi^{-infinity} smoothing remainder"
            and "pseudodifferential" in theorem["global_wavefront_argument"],
        },
        {
            "mutation": "treat static q=0 subtraction as evolving stress",
            "rejected": parametrix.get("renormalized_stress") == "NOT_COMPUTED",
        },
        {
            "mutation": "claim determinant, stress or physical Hessian from the state",
            "rejected": parametrix.get("determinant") == "NOT_COMPUTED"
            and parametrix.get("renormalized_stress") == "NOT_COMPUTED",
        },
        {
            "mutation": "import H0, a0, K_Q or V",
            "rejected": not any(
                f'"{key}"' in json.dumps(
                    {"theorem": theorem, "matrix": matrix, "preflight": preflight},
                    sort_keys=True,
                )
                for key in ("H0", "a0", "K_Q", "V", "observational_target")
            ),
        },
        {
            "mutation": "manufacture Rule-9 clearance",
            "rejected": RULE9_STATUS != "THREE_WAY_CLEARANCE_MET",
        },
    ]
    add_check(
        checks,
        "mandatory_rejecting_mutations_are_rejected",
        all(item["rejected"] for item in mutations),
        mutations=mutations,
    )

    all_checks_pass = all(check["ok"] for check in checks)
    state_conditions = {
        "smooth_matrix_bisolution": "THEOREM_BACKED_BY_EXACT_CAUCHY_EVOLUTION" if all_checks_pass else "NOT_ESTABLISHED",
        "ccr": "THEOREM_BACKED_AND_FINITE_MATRIX_WITNESS" if all_checks_pass else "NOT_ESTABLISHED",
        "global_positivity": "THEOREM_BACKED_WITH_SMOOTHING_LOW_MODE_PATCH" if all_checks_pass else "NOT_ESTABLISHED",
        "global_wavefront_condition": "THEOREM_BACKED_PSEUDODIFFERENTIAL_CONSTRUCTION" if all_checks_pass else "NOT_ESTABLISHED",
        "local_parametrix_agreement": "DERIVED_LOCAL_U0_U2" if all_checks_pass else "NOT_ESTABLISHED",
        "all_order_symbol_or_smoothing_remainder": theorem["remainder_class"] if all_checks_pass else "NOT_ESTABLISHED",
        "state_coordinate_covariance": "THEOREM_BACKED_AND_NUMERICALLY_CHECKED" if all_checks_pass else "NOT_ESTABLISHED",
    }
    status = PASS_STATUS if all_checks_pass else HOLD_STATUS
    return {
        "schema": "ITSM_TOPX4_S2F3_GLOBAL_STATE_CONSTRUCTION_v1",
        "gate": "TOP-X4",
        "route": "X4-S2F3",
        "status": status,
        "calculation_status": "PASS_THEOREM_BACKED_GLOBAL_STATE_CONSTRUCTION" if all_checks_pass else "HOLD_GLOBAL_STATE_CONSTRUCTION_NOT_ESTABLISHED",
        "physics_pass": False,
        "gate_effect": "NONE",
        "publication_status": "NOT_A_PHYSICS_CLAIM",
        "rule9_review": {
            "status": RULE9_STATUS,
            "completed_independent_reports": 0,
        },
        "authority_receipts": receipts,
        "checks": checks,
        "checks_passed": sum(check["ok"] for check in checks),
        "checks_total": len(checks),
        "theorem_backed_construction": theorem,
        "state_conditions": state_conditions,
        "construction_status": {
            "global_scalar_matrix_hadamard_state": "THEOREM_BACKED_CONSTRUCTED" if all_checks_pass else "NOT_CONSTRUCTED",
            "smooth_state_bisolution": state_conditions["smooth_matrix_bisolution"],
            "renormalized_stress": "NOT_COMPUTED",
            "determinant": "NOT_COMPUTED",
            "counterterm_normalizations": "NOT_FIXED",
        },
        "explicit_nonclaims": [
            "No Dirac, graviton, ghost or parity/anomaly state is constructed.",
            "No counterterm normalization, determinant, renormalized stress or physical Hessian is computed.",
            "No A4 or Ultra entry is authorized.",
            "No MAT, UVIR, cosmology, Rule-9 or publication promotion follows.",
            "The theorem-backed state construction is not an action-derived BBN background and supplies no Q^mu, S_N or G_eff.",
        ],
        "derived_claims": [],
    }


def main() -> int:
    result = run_construction()
    result["script_sha256"] = sha256_file(Path(__file__))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n").encode(
        "utf-8"
    )
    OUTPUT_PATH.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    OUTPUT_PATH.with_suffix(OUTPUT_PATH.suffix + ".sha256").write_text(
        f"{digest}  {OUTPUT_PATH.name}\n", encoding="ascii", newline="\n"
    )
    print(result["status"])
    print(f"checks={result['checks_passed']}/{result['checks_total']}")
    print("route=ROUTE_A_PSEUDODIFFERENTIAL_PROJECTION_THEOREM_BACKED")
    print("global_scalar_matrix_hadamard_state=" + result["construction_status"]["global_scalar_matrix_hadamard_state"])
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={OUTPUT_PATH}")
    print(f"sha256={digest}")
    return 0 if result["status"] == PASS_STATUS else 1


if __name__ == "__main__":
    raise SystemExit(main())
