#!/usr/bin/env python3
"""Preflight the next TOP-X4 global scalar-state construction gate.

This is deliberately a readiness calculation, not a Hadamard-state claim.
It checks the registered low-mode stability and the hypotheses visible in the
repository, then refuses to promote a finite-grid transport or a local
parametrix to a globally admissible state until an all-order
pseudodifferential/adiabatic construction is actually implemented.
"""

from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path
from typing import Any

import numpy as np

from topx4_s2f3_exact_transport_retry_checkpoint import (
    background_fields,
    integrate_background,
    make_splines,
    parameters,
    scalar_matrices,
)


STATUS = "HOLD_GLOBAL_STATE_CONSTRUCTION_NOT_ESTABLISHED"
REPO_ROOT = Path(__file__).resolve().parents[3]
BASE = REPO_ROOT / "Analysis" / "TOP" / "TOP-X4"
OUTPUT_PATH = BASE / "outputs" / "topx4_s2f3_global_state_construction_preflight_summary.json"


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
    gate = REPO_ROOT / "Theory" / "Gates" / "TOP-X4"
    core = REPO_ROOT / "Theory" / "Core" / "Reasoning_Mode_Plans" / "11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION"
    outputs = BASE / "outputs"
    return [
        gate / "TOPX4_S2F3_GLOBAL_STATE_CONSTRUCTION_CONTRACT_2026-09-16.md",
        core / "PLAN.md",
        outputs / "topx4_a1_background_summary.json",
        outputs / "topx4_s2f3_dynamic_state_subtraction_summary.json",
        outputs / "topx4_s2f3_exact_transport_retry_summary.json",
        outputs / "topx4_s2f3_covariant_scalar_matrix_summary.json",
        outputs / "topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json",
    ]


def low_mode_diagnostics() -> dict[str, Any]:
    params = parameters()
    solution = integrate_background(801, params)
    fields = background_fields(solution, params)
    splines = make_splines(solution.t, fields)

    min_k = float("inf")
    min_hamiltonian = float("inf")
    min_a = float(np.min(fields["a"]))
    min_b = float(np.min(fields["b"]))
    min_rho = float(np.min(fields["rho"]))
    zero_mode_eigenvalues: list[float] = []
    for time in solution.t:
        k_matrix, hessian, _ = scalar_matrices(float(time), 0.0, 0, splines)
        k_eigenvalues = np.linalg.eigvalsh(k_matrix)
        hessian_eigenvalues = np.linalg.eigvalsh(hessian)
        min_k = min(min_k, float(np.min(k_eigenvalues)))
        min_hamiltonian = min(min_hamiltonian, float(np.min(hessian_eigenvalues)))
        zero_mode_eigenvalues.extend(float(value) for value in hessian_eigenvalues)

    charge = fields["charge"]
    charge_drift = float(np.max(np.abs(charge / charge[0] - 1.0)))
    finite = bool(solution.success and np.all(np.isfinite(solution.y)))
    positive_domain = bool(min_a > 0.0 and min_b > 0.0 and min_rho > 0.0)
    return {
        "solver_success": bool(solution.success),
        "sample_count": int(solution.t.size),
        "finite_background": finite,
        "positive_registered_domain": positive_domain,
        "minimum_a": min_a,
        "minimum_b": min_b,
        "minimum_rho": min_rho,
        "minimum_zero_mode_K_eigenvalue": min_k,
        "minimum_zero_mode_hamiltonian_eigenvalue": min_hamiltonian,
        "zero_mode_K_positive": bool(min_k > 0.0),
        "zero_mode_hamiltonian_positive": bool(min_hamiltonian > 0.0),
        "registered_charge_relative_drift": charge_drift,
        "charge_conservation_check": bool(charge_drift < 1.0e-9),
        "spatial_momentum_monotonicity_argument": (
            "For the registered scalar matrices, k_n^2 enters both K and the "
            "upper-left Hamiltonian block as k_n^2 I_2; positivity of the zero "
            "mode therefore controls every nonzero spatial momentum mode."
        ),
        "zero_mode_eigenvalue_count": len(zero_mode_eigenvalues),
    }


def run_preflight() -> dict[str, Any]:
    receipts = [sidecar_check(path) for path in authority_paths()]
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "all_predecessor_authority_sidecars_match",
        all(item["matches"] for item in receipts),
        receipts=receipts,
    )

    outputs = {path.name: load_json(path) for path in authority_paths() if path.suffix == ".json" and path.is_file()}
    a1 = outputs["topx4_a1_background_summary.json"]
    dynamic = outputs["topx4_s2f3_dynamic_state_subtraction_summary.json"]
    exact = outputs["topx4_s2f3_exact_transport_retry_summary.json"]
    matrix = outputs["topx4_s2f3_covariant_scalar_matrix_summary.json"]
    parametrix = outputs["topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json"]

    add_check(
        checks,
        "a1_background_authority_is_preserved",
        a1.get("status") == "PASS_TOPX4_A1_CONTROL_BACKGROUND_ONLY"
        and a1.get("physics_pass") is False
        and a1.get("gate_effect") == "NONE",
        status=a1.get("status"),
        physics_pass=a1.get("physics_pass"),
    )
    add_check(
        checks,
        "prior_dynamic_wkb_failure_is_preserved",
        dynamic.get("status") == "FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT"
        and dynamic.get("calculation_checks_passed") == 11
        and dynamic.get("calculation_checks_total") == 12,
        status=dynamic.get("status"),
        check_counts=f"{dynamic.get('calculation_checks_passed')}/{dynamic.get('calculation_checks_total')}",
    )
    add_check(
        checks,
        "finite_transport_is_not_relabelled_as_hadamard",
        exact.get("full_Hadamard_state") is False
        and exact.get("covariant_5D_subtraction") == "NOT_DERIVED"
        and exact.get("renormalized_stress") == "NOT_COMPUTED",
        full_Hadamard_state=exact.get("full_Hadamard_state"),
        covariant_5D_subtraction=exact.get("covariant_5D_subtraction"),
    )
    add_check(
        checks,
        "local_parametrix_boundary_is_preserved",
        parametrix.get("scalar_matrix_hadamard_parametrix") == "DERIVED_LOCAL_U0_U2"
        and parametrix.get("scalar_matrix_hadamard_state") == "NOT_CONSTRUCTED"
        and parametrix.get("physics_pass") is False,
        local_parametrix=parametrix.get("scalar_matrix_hadamard_parametrix"),
        scalar_matrix_hadamard_state=parametrix.get("scalar_matrix_hadamard_state"),
    )

    low_modes = low_mode_diagnostics()
    add_check(
        checks,
        "registered_background_and_zero_mode_are_finite_and_positive",
        low_modes["finite_background"]
        and low_modes["positive_registered_domain"]
        and low_modes["zero_mode_K_positive"]
        and low_modes["zero_mode_hamiltonian_positive"]
        and low_modes["charge_conservation_check"],
        **low_modes,
    )
    add_check(
        checks,
        "principal_scalar_operator_is_normally_hyperbolic",
        parametrix.get("local_parametrix", {}).get("dimension") == 5
        and len(matrix.get("off_shell_operator", {}).get("H", [])) == 3
        and matrix.get("scalar_matrix_operator") == "DERIVED_FIXED_METRIC_OFF_SHELL",
        dimension=parametrix.get("local_parametrix", {}).get("dimension"),
        rank=len(matrix.get("off_shell_operator", {}).get("H", [])),
        scalar_matrix_operator=matrix.get("scalar_matrix_operator"),
    )
    add_check(
        checks,
        "corrected_endomorphism_and_flat_bundle_curvature_are_preserved",
        matrix.get("off_shell_operator", {}).get("E") == "-H"
        and matrix.get("off_shell_operator", {}).get("cartesian_Omega_AB") == "0"
        and parametrix.get("local_parametrix", {}).get("cartesian_Omega_AB") == "0"
        and parametrix.get("local_parametrix", {}).get("phase_aligned_Omega_AB") == "0 on smooth patch",
        endomorphism=matrix.get("off_shell_operator", {}).get("E"),
        cartesian_Omega=parametrix.get("local_parametrix", {}).get("cartesian_Omega_AB"),
        phase_aligned_Omega=parametrix.get("local_parametrix", {}).get("phase_aligned_Omega_AB"),
    )

    source_text = inspect.getsource(run_preflight)
    forbidden = [token for token in ("observed" + "_acceleration", "hubble" + "_target", "galaxy" + "_target", "desired" + "_radius") if token in source_text]
    add_check(checks, "observational_target_firewall", not forbidden, forbidden_token_hits=forbidden)

    all_preflight_checks_pass = all(check["ok"] for check in checks)
    state_conditions = {
        "smooth_matrix_bisolution": False,
        "ccr": False,
        "global_positivity": False,
        "global_wavefront_condition": False,
        "all_order_symbol_or_smoothing_remainder": False,
        "low_mode_smoothing_patch": False,
        "state_coordinate_covariance": False,
    }
    return {
        "schema": "ITSM_TOPX4_S2F3_GLOBAL_STATE_PREFLIGHT_v1",
        "gate": "TOP-X4",
        "route": "X4-S2F3",
        "status": STATUS,
        "calculation_status": "PREFLIGHT_PASS" if all_preflight_checks_pass else "PREFLIGHT_FAIL",
        "physics_pass": False,
        "gate_effect": "NONE",
        "rule9_review": {
            "status": "THREE_WAY_CLEARANCE_NOT_MET",
            "completed_independent_reports": 0,
        },
        "authority_receipts": receipts,
        "preflight_checks": checks,
        "preflight_checks_passed": sum(check["ok"] for check in checks),
        "preflight_checks_total": len(checks),
        "low_mode_diagnostics": low_modes,
        "selected_route": "ROUTE_A_PSEUDODIFFERENTIAL_PROJECTION_NOT_YET_IMPLEMENTED",
        "state_conditions": state_conditions,
        "construction_status": {
            "global_scalar_matrix_hadamard_state": "NOT_CONSTRUCTED",
            "smooth_state_bisolution": "NOT_CONSTRUCTED",
            "renormalized_stress": "NOT_COMPUTED",
            "determinant": "NOT_COMPUTED",
            "counterterm_normalizations": "NOT_FIXED",
        },
        "blocking_reasons": [
            "No all-order matrix pseudodifferential symbol recursion is implemented.",
            "No Borel-summed or theorem-instantiated Cauchy-data projector is attached to this operator.",
            "No actual coupled smooth bisolution, CCR verification or global positivity calculation exists.",
            "The finite registered interval does not by itself provide the global wavefront proof.",
            "The low-mode positivity result is a prerequisite control, not a global Hadamard-state construction.",
        ],
        "next_required_action": (
            "Implement Route A with an explicit all-order symbol recursion, a smoothing low-mode patch, "
            "exact Cauchy evolution and theorem-backed wavefront/positivity justification; then rerun "
            "the state conditions before any stress or determinant work."
        ),
        "downstream_actions": {
            "advance_to_stress": False,
            "advance_to_determinant": False,
            "advance_to_physical_hessian": False,
            "advance_to_a4": False,
            "advance_to_ultra": False,
            "gate_or_publication_promotion": False,
        },
    }


def main() -> int:
    result = run_preflight()
    result["script_sha256"] = sha256_file(Path(__file__))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    OUTPUT_PATH.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    OUTPUT_PATH.with_suffix(OUTPUT_PATH.suffix + ".sha256").write_text(
        f"{digest}  {OUTPUT_PATH.name}\n", encoding="ascii", newline="\n"
    )
    print(STATUS)
    print(f"preflight_checks={result['preflight_checks_passed']}/{result['preflight_checks_total']}")
    print(f"zero_mode_hamiltonian_positive={result['low_mode_diagnostics']['zero_mode_hamiltonian_positive']}")
    print("global_scalar_matrix_hadamard_state=NOT_CONSTRUCTED")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={OUTPUT_PATH}")
    print(f"sha256={digest}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
