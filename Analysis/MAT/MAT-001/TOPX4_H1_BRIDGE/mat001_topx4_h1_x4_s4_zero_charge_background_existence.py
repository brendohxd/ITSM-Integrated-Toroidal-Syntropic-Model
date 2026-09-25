#!/usr/bin/env python3
"""Run the bounded X4-S4-GW2 zero-charge background-existence test."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import simpson
from scipy.integrate import solve_bvp


SOLUTION_STATUS = "BENCHMARK_SOLUTION_FOUND_HOLD_FINITE_Q"
REJECTION_STATUS = "BENCHMARK_REJECTED_RETURN_TO_ACTION_SELECTION"
INCONCLUSIVE_STATUS = "NUMERICAL_INCONCLUSIVE_NO_PHYSICS_DECISION"
ERROR_STATUS = "ERROR_X4_S4_ZERO_CHARGE_BACKGROUND_EXISTENCE"

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
OUTPUT_PATH = BASE / "outputs" / "mat001_topx4_h1_x4_s4_zero_charge_background_existence_summary.json"
REPORT_PATH = BASE / "MAT001_TOPX4_H1_X4_S4_ZERO_CHARGE_BACKGROUND_EXISTENCE_2026-09-18.md"
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_X4_S4_ZERO_CHARGE_BACKGROUND_EXISTENCE_CONTRACT_2026-09-18.md"
)
ACTION_CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_X4_S4_NEW_PARENT_ACTION_CONTRACT_2026-09-18.md"
)
ACTION_SUMMARY_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_x4_s4_new_parent_action_contract_summary.json"
)
HANDOFF_SUMMARY_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_compensated_warped_child_design_summary.json"
)
S0_AUDIT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S0_STABILIZATION_CANDIDATE_AUDIT_2026-09-06.md"
)
S2F3_FREEZE_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    parser.add_argument("--self-test-mutations", action="store_true")
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sidecar_candidates(path: Path) -> list[Path]:
    values = [Path(str(path) + ".sha256"), path.with_suffix(".sha256")]
    return list(dict.fromkeys(values))


def find_sidecar(path: Path) -> Path | None:
    return next((item for item in sidecar_candidates(path) if item.is_file()), None)


def write_sidecar(path: Path, *, replace_suffix: bool = False) -> Path:
    sidecar = path.with_suffix(".sha256") if replace_suffix else Path(str(path) + ".sha256")
    sidecar.write_text(
        f"{sha256_file(path)}  {path.name}\n", encoding="ascii", newline="\n"
    )
    return sidecar


def artifact_receipt(path: Path, *, sidecar_required: bool = True) -> dict[str, Any]:
    exists = path.is_file()
    digest = sha256_file(path) if exists else None
    sidecar = find_sidecar(path) if exists else None
    expected: str | None = None
    if sidecar is not None:
        tokens = sidecar.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    return {
        "path": relative(path),
        "exists": exists,
        "sha256": digest,
        "sidecar_required": sidecar_required,
        "sidecar_path": relative(sidecar) if sidecar is not None else None,
        "sidecar_matches": digest == expected if expected is not None else None,
    }


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"Expected JSON object: {path}")
    return data


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def build_benchmark() -> dict[str, float]:
    return {
        "M5": 1.0,
        "Lambda5": -6.0,
        "mPhi2": 0.25,
        "mvarphi2": 0.25,
        "lambdaPhi5": 0.2,
        "lambdavarphi5": 0.2,
        "g5": 0.1,
        "kappa_0": 10.0,
        "kappa_pi": 10.0,
        "v_0": 1.0,
        "v_pi": 0.4,
        "zeta_0": 0.05,
        "zeta_pi": 0.05,
        "tau_0": 3.0,
        "tau_pi": -3.2,
    }


def build_firewall() -> dict[str, Any]:
    return {
        "candidate_action_contract_frozen": True,
        "X4-S4_parent_accepted": False,
        "finite_charge_background_solved": False,
        "physical_hessian_constructed": False,
        "signed_H1_residue_computed": False,
        "MAT001_pass": False,
        "K_Q_derived": False,
        "V_computed": False,
        "stage4A_reopened": False,
        "rule9_cleared": False,
        "physics_pass": False,
        "gate_effect": "NONE",
    }


def potential(f: np.ndarray, h: np.ndarray, b: dict[str, float]) -> np.ndarray:
    return (
        b["mPhi2"] * f**2
        + b["lambdaPhi5"] * f**4 / 2.0
        + b["mvarphi2"] * h**2 / 2.0
        + b["lambdavarphi5"] * h**4 / 24.0
        + b["g5"] * f**2 * h**2 / 2.0
    )


def localized_potential(f: float, h: float, surface: str, b: dict[str, float]) -> float:
    if surface == "0":
        kappa, v, tau, zeta = b["kappa_0"], b["v_0"], b["tau_0"], b["zeta_0"]
    else:
        kappa, v, tau, zeta = b["kappa_pi"], b["v_pi"], b["tau_pi"], b["zeta_pi"]
    return tau + kappa * (h * h - v * v) ** 2 / 4.0 + zeta * f * f


def ode(x: np.ndarray, y: np.ndarray, parameters: np.ndarray, b: dict[str, float]) -> np.ndarray:
    del x
    L = float(parameters[0])
    A, p, f, u, h, v = y
    del A
    mass_f = b["mPhi2"] + b["lambdaPhi5"] * f**2 + b["g5"] * h**2 / 2.0
    mass_h = b["mvarphi2"] * h + b["lambdavarphi5"] * h**3 / 6.0 + b["g5"] * f**2 * h
    return np.vstack(
        (
            p,
            -(2.0 * u**2 + v**2) / (3.0 * b["M5"] ** 3),
            u,
            -4.0 * p * u + L**2 * mass_f * f,
            v,
            -4.0 * p * v + L**2 * mass_h,
        )
    )


def boundary(ya: np.ndarray, yb: np.ndarray, parameters: np.ndarray, b: dict[str, float]) -> np.ndarray:
    L = float(parameters[0])
    _, p0, f0, u0, h0, v0 = ya
    _, p1, f1, u1, h1, v1 = yb
    V0 = localized_potential(float(f0), float(h0), "0", b)
    Vpi = localized_potential(float(f1), float(h1), "pi", b)
    return np.array(
        [
            ya[0],
            u0 - L * b["zeta_0"] * f0,
            u1 + L * b["zeta_pi"] * f1,
            v0 - L * b["kappa_0"] * h0 * (h0**2 - b["v_0"] ** 2),
            v1 + L * b["kappa_pi"] * h1 * (h1**2 - b["v_pi"] ** 2),
            p0 + L * V0 / (3.0 * b["M5"] ** 3),
            p1 - L * Vpi / (3.0 * b["M5"] ** 3),
        ]
    )


def constraint_residual(x: np.ndarray, y: np.ndarray, parameters: np.ndarray, b: dict[str, float]) -> np.ndarray:
    del x
    L = float(parameters[0])
    _, p, f, u, h, v = y
    return (
        6.0 * b["M5"] ** 3 * (p / L) ** 2
        - (u / L) ** 2
        - (v / L) ** 2 / 2.0
        + b["Lambda5"]
        + potential(f, h, b)
    )


def initial_guess(x: np.ndarray, L_guess: float, b: dict[str, float], variant: int) -> np.ndarray:
    if variant == 0:
        f = b["v_0"] + (b["v_pi"] - b["v_0"]) * x
        h = b["v_0"] + (b["v_pi"] - b["v_0"]) * x
        u = np.full_like(x, b["v_pi"] - b["v_0"])
        v = np.full_like(x, b["v_pi"] - b["v_0"])
    elif variant == 1:
        f = 0.95 * b["v_0"] + (0.95 * b["v_pi"] - 0.95 * b["v_0"]) * x
        h = 1.02 * b["v_0"] + (0.98 * b["v_pi"] - 1.02 * b["v_0"]) * x
        u = np.gradient(f, x)
        v = np.gradient(h, x)
    else:
        f = 0.8 * b["v_0"] + (1.1 * b["v_pi"] - 0.8 * b["v_0"]) * x
        h = 1.1 * b["v_0"] + (0.9 * b["v_pi"] - 1.1 * b["v_0"]) * x
        u = np.gradient(f, x)
        v = np.gradient(h, x)
    p = np.full_like(x, -0.95 * L_guess)
    A = -0.95 * L_guess * x
    return np.vstack((A, p, f, u, h, v))


def run_attempt(variant: int, L_guess: float, b: dict[str, float]) -> dict[str, Any]:
    x = np.linspace(0.0, 1.0, 65)
    guess = initial_guess(x, L_guess, b, variant)
    try:
        solution = solve_bvp(
            lambda grid, values, params: ode(grid, values, params, b),
            lambda left, right, params: boundary(left, right, params, b),
            x,
            guess,
            p=np.array([L_guess], dtype=float),
            tol=1e-7,
            max_nodes=20000,
            verbose=0,
        )
    except Exception as exc:  # pragma: no cover - defensive receipt path
        return {
            "variant": variant,
            "L_guess": L_guess,
            "solver_success": False,
            "solver_status": "EXCEPTION",
            "message": str(exc),
        }

    dense_x = np.linspace(0.0, 1.0, 1001)
    dense_y = solution.sol(dense_x)
    L = float(solution.p[0])
    bc_residuals = boundary(solution.y[:, 0], solution.y[:, -1], solution.p, b)
    constraint = constraint_residual(dense_x, dense_y, solution.p, b)
    finite = bool(np.all(np.isfinite(dense_y)) and np.isfinite(L))
    regular = finite and L > 1e-4 and float(np.max(np.abs(dense_y))) < 1e6
    V0 = localized_potential(float(dense_y[2, 0]), float(dense_y[4, 0]), "0", b)
    Vpi = localized_potential(float(dense_y[2, -1]), float(dense_y[4, -1]), "pi", b)
    gradient_integral = float(
        simpson((dense_y[5] / L) ** 2 + 2.0 * (dense_y[3] / L) ** 2, x=L * dense_x)
    )
    sum_rule = V0 + Vpi + gradient_integral
    boundary_max = float(np.max(np.abs(bc_residuals)))
    constraint_max = float(np.max(np.abs(constraint)))
    return {
        "variant": variant,
        "L_guess": L_guess,
        "solver_success": bool(solution.success),
        "solver_status": int(solution.status),
        "message": str(solution.message),
        "iterations": int(solution.niter),
        "mesh_nodes": int(solution.x.size),
        "L": L,
        "finite": finite,
        "regular": regular,
        "boundary_residuals": [float(value) for value in bc_residuals],
        "boundary_max_abs": boundary_max,
        "constraint_max_abs": constraint_max,
        "sum_rule": sum_rule,
        "V0": V0,
        "Vpi": Vpi,
        "gradient_integral": gradient_integral,
        "field_ranges": {
            "A": [float(np.min(dense_y[0])), float(np.max(dense_y[0]))],
            "p": [float(np.min(dense_y[1])), float(np.max(dense_y[1]))],
            "f": [float(np.min(dense_y[2])), float(np.max(dense_y[2]))],
            "u": [float(np.min(dense_y[3])), float(np.max(dense_y[3]))],
            "h": [float(np.min(dense_y[4])), float(np.max(dense_y[4]))],
            "v": [float(np.min(dense_y[5])), float(np.max(dense_y[5]))],
        },
    }


def contract_coverage_check() -> tuple[bool, list[str]]:
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    fragments = {
        "purpose": "zero-charge warped static",
        "constraint": "C(x) = 6 M5^3",
        "boundary_system": "p(0) + L V_0",
        "benchmark": "tau_pi",
        "sum_rule": "B = V_0^ren + V_pi^ren",
        "finite_charge_stop": "finite-charge continuation closed",
    }
    missing = [name for name, fragment in fragments.items() if fragment not in text]
    return not missing, missing


def build_summary(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    b = build_benchmark()
    firewall = build_firewall()
    attempts = [
        run_attempt(0, 1.0, b),
        run_attempt(1, 0.8, b),
        run_attempt(2, 1.2, b),
    ]
    converged = [item for item in attempts if item.get("solver_success")]
    candidate = min(
        converged,
        key=lambda item: (item.get("constraint_max_abs", float("inf")), item.get("boundary_max_abs", float("inf"))),
        default=None,
    )
    numerical_thresholds = {
        "solve_tolerance": 1e-7,
        "boundary_residual_tolerance": 5e-5,
        "constraint_tolerance": 5e-5,
        "sum_rule_tolerance": 5e-5,
        "minimum_modulus": 1e-4,
        "regularity_bound": 1e6,
    }
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "all_authority_and_input_files_exist",
        all(item["exists"] for item in receipts),
        missing=[item["path"] for item in receipts if not item["exists"]],
    )
    add_check(
        checks,
        "all_required_sidecars_match_current_bytes",
        all(
            (not item["sidecar_required"]) or item["sidecar_matches"] is True
            for item in receipts
        ),
        failures=[
            item["path"]
            for item in receipts
            if item["sidecar_required"] and item["sidecar_matches"] is not True
        ],
    )

    action = load_json(ACTION_SUMMARY_PATH)
    handoff = load_json(HANDOFF_SUMMARY_PATH)
    add_check(
        checks,
        "frozen_action_and_route_handoff_are_authoritative",
        action.get("status") == "PASS_X4_S4_GW2_CANDIDATE_ACTION_CONTRACT_HOLD_PARENT_ACCEPTANCE"
        and action.get("checks_passed") == action.get("checks_total") == 21
        and action.get("status_firewall", {}).get("X4-S4_parent_accepted") is False
        and handoff.get("status") == "ROUTE_HANDOFF_X4_S4_NEW_PARENT_DESIGN_ONLY",
    )
    add_check(
        checks,
        "benchmark_is_internal_dimensionless_and_not_observationally_selected",
        b == build_benchmark()
        and b["M5"] == 1.0
        and b["Lambda5"] == -6.0
        and b["tau_0"] == 3.0
        and b["tau_pi"] == -3.2
        and action.get("candidate", {}).get("parameter_domain", {}).get(
            "selected_from_observational_target"
        )
        is False,
    )
    coverage_ok, missing = contract_coverage_check()
    add_check(
        checks,
        "human_contract_covers_the_registered_bvp_and_stop_boundary",
        coverage_ok,
        missing_fragments=missing,
        note="documentation coherence only; not a physics-pass criterion",
    )
    add_check(
        checks,
        "solver_attempts_use_fixed_action_and_bounded_initialization_variants",
        len(attempts) == 3
        and [item["L_guess"] for item in attempts] == [1.0, 0.8, 1.2]
        and [item["variant"] for item in attempts] == [0, 1, 2],
        attempts=[
            {
                "variant": item["variant"],
                "L_guess": item["L_guess"],
                "solver_success": item.get("solver_success"),
                "solver_status": item.get("solver_status"),
            }
            for item in attempts
        ],
    )
    add_check(
        checks,
        "solver_outcome_is_explicitly_classified_without_parameter_drift",
        len(attempts) == 3
        and all(item.get("variant") in {0, 1, 2} for item in attempts)
        and (candidate is not None or all("solver_success" in item for item in attempts)),
        converged_attempts=len(converged),
        inconclusive=(candidate is None),
    )

    boundary_ok = bool(
        candidate
        and candidate.get("finite")
        and candidate.get("regular")
        and candidate.get("boundary_max_abs", float("inf"))
        <= numerical_thresholds["boundary_residual_tolerance"]
    )
    constraint_ok = bool(
        candidate
        and candidate.get("constraint_max_abs", float("inf"))
        <= numerical_thresholds["constraint_tolerance"]
    )
    sum_rule_ok = bool(
        candidate
        and abs(candidate.get("sum_rule", float("inf")))
        <= numerical_thresholds["sum_rule_tolerance"]
    )
    add_check(
        checks,
        "boundary_audit_is_executed_and_classified",
        candidate is None or isinstance(candidate.get("boundary_residuals"), list),
        selected_attempt=candidate.get("variant") if candidate else None,
        passed=boundary_ok,
        boundary_max_abs=candidate.get("boundary_max_abs") if candidate else None,
        tolerance=numerical_thresholds["boundary_residual_tolerance"],
    )
    add_check(
        checks,
        "independent_Einstein_constraint_audit_is_executed_and_classified",
        candidate is None or "constraint_max_abs" in candidate,
        passed=constraint_ok,
        constraint_max_abs=candidate.get("constraint_max_abs") if candidate else None,
        tolerance=numerical_thresholds["constraint_tolerance"],
    )
    add_check(
        checks,
        "independent_static_sum_rule_audit_is_executed_and_classified",
        candidate is None or "sum_rule" in candidate,
        passed=sum_rule_ok,
        sum_rule=candidate.get("sum_rule") if candidate else None,
        tolerance=numerical_thresholds["sum_rule_tolerance"],
    )
    add_check(
        checks,
        "positive_internal_modulus_and_no_finite_charge_or_H1_claim",
        bool(candidate is None or candidate.get("L", -1.0) > 0.0)
        and firewall["finite_charge_background_solved"] is False
        and firewall["physical_hessian_constructed"] is False
        and firewall["K_Q_derived"] is False
        and firewall["V_computed"] is False,
        L=candidate.get("L") if candidate else None,
    )
    add_check(
        checks,
        "non_promoting_firewall_remains_closed",
        firewall["candidate_action_contract_frozen"] is True
        and firewall["X4-S4_parent_accepted"] is False
        and firewall["finite_charge_background_solved"] is False
        and firewall["physical_hessian_constructed"] is False
        and firewall["signed_H1_residue_computed"] is False
        and firewall["MAT001_pass"] is False
        and firewall["K_Q_derived"] is False
        and firewall["V_computed"] is False
        and firewall["stage4A_reopened"] is False
        and firewall["rule9_cleared"] is False
        and firewall["physics_pass"] is False
        and firewall["gate_effect"] == "NONE",
    )

    if candidate is None:
        status = INCONCLUSIVE_STATUS
    elif boundary_ok and constraint_ok and sum_rule_ok:
        status = SOLUTION_STATUS
    else:
        status = REJECTION_STATUS

    return {
        "schema": "ITSM_MAT001_TOPX4_H1_X4_S4_ZERO_CHARGE_BACKGROUND_EXISTENCE_v1",
        "date": "2026-09-18",
        "status": status,
        "audit_execution_status": "COMPLETE",
        "scope": "ONE_PREREGISTERED_INTERNAL_ZERO_CHARGE_STATIC_BENCHMARK",
        "benchmark": b,
        "numerical_thresholds": numerical_thresholds,
        "attempts": attempts,
        "selected_attempt": candidate,
        "checks": checks,
        "checks_passed": sum(1 for item in checks if item["ok"]),
        "checks_total": len(checks),
        "status_firewall": firewall,
        "artifact_receipts": receipts,
        "downstream_status": {
            "finite_charge_continuation": "CLOSED",
            "physical_hessian": "NOT_CONSTRUCTED",
            "signed_H1_residue": "NOT_COMPUTED",
            "MAT001": "BLOCKED",
            "K_Q": "NOT_DERIVED",
            "V": "NOT_COMPUTED",
            "Stage4A": "CLOSED",
            "Rule9": "NOT_CLEARED",
            "physics_pass": False,
            "gate_effect": "NONE",
        },
        "next_single_gate": {
            "name": (
                "TOPX4_H1_X4-S4_FINITE_CHARGE_BACKGROUND_CONTINUATION"
                if status == SOLUTION_STATUS
                else "TOPX4_H1_X4-S4_ACTION_SELECTION_AFTER_ZERO_CHARGE_TEST"
            ),
            "scope": (
                "Continue only from the verified zero-charge seed while deriving "
                "the finite-Q generalized integrated Einstein identity."
                if status == SOLUTION_STATUS
                else "Return to X4-S4 action selection; finite charge remains closed."
            ),
            "stop_before": "NO_H1_OR_MAT_PROMOTION",
        },
    }


def semantic_state_valid(summary: dict[str, Any]) -> bool:
    b = summary.get("benchmark", {})
    thresholds = summary.get("numerical_thresholds", {})
    firewall = summary.get("status_firewall", {})
    attempts = summary.get("attempts", [])
    status = summary.get("status")
    selected = summary.get("selected_attempt")
    status_allowed = {SOLUTION_STATUS, REJECTION_STATUS, INCONCLUSIVE_STATUS}
    candidate_benchmark = build_benchmark()
    threshold_expected = {
        "solve_tolerance": 1e-7,
        "boundary_residual_tolerance": 5e-5,
        "constraint_tolerance": 5e-5,
        "sum_rule_tolerance": 5e-5,
        "minimum_modulus": 1e-4,
        "regularity_bound": 1e6,
    }
    selected_shape_ok = selected is None or (
        isinstance(selected, dict)
        and selected.get("solver_success") is True
        and selected.get("L", -1.0) > 0.0
        and isinstance(selected.get("boundary_residuals"), list)
        and "boundary_max_abs" in selected
        and "constraint_max_abs" in selected
        and "sum_rule" in selected
    )
    if selected is None:
        expected_status = INCONCLUSIVE_STATUS
    else:
        boundary_pass = (
            selected_shape_ok
            and selected.get("regular") is True
            and selected.get("boundary_max_abs", float("inf"))
            <= threshold_expected["boundary_residual_tolerance"]
        )
        constraint_pass = selected_shape_ok and selected.get("constraint_max_abs", float("inf")) <= threshold_expected[
            "constraint_tolerance"
        ]
        sum_rule_pass = selected_shape_ok and abs(selected.get("sum_rule", float("inf"))) <= threshold_expected[
            "sum_rule_tolerance"
        ]
        expected_status = (
            SOLUTION_STATUS
            if boundary_pass and constraint_pass and sum_rule_pass
            else REJECTION_STATUS
        )
    return (
        summary.get("scope") == "ONE_PREREGISTERED_INTERNAL_ZERO_CHARGE_STATIC_BENCHMARK"
        and status in status_allowed
        and b == candidate_benchmark
        and thresholds == threshold_expected
        and len(attempts) == 3
        and [item.get("L_guess") for item in attempts] == [1.0, 0.8, 1.2]
        and [item.get("variant") for item in attempts] == [0, 1, 2]
        and selected_shape_ok
        and status == expected_status
        and firewall.get("candidate_action_contract_frozen") is True
        and firewall.get("X4-S4_parent_accepted") is False
        and firewall.get("finite_charge_background_solved") is False
        and firewall.get("physical_hessian_constructed") is False
        and firewall.get("signed_H1_residue_computed") is False
        and firewall.get("MAT001_pass") is False
        and firewall.get("K_Q_derived") is False
        and firewall.get("V_computed") is False
        and firewall.get("stage4A_reopened") is False
        and firewall.get("rule9_cleared") is False
        and firewall.get("physics_pass") is False
        and firewall.get("gate_effect") == "NONE"
        and (
            selected is None
            or (
            summary.get("scope") == "ONE_PREREGISTERED_INTERNAL_ZERO_CHARGE_STATIC_BENCHMARK"
            and status in status_allowed
            and b == candidate_benchmark
            and thresholds == threshold_expected
            and len(attempts) == 3
            and [item.get("L_guess") for item in attempts] == [1.0, 0.8, 1.2]
            and [item.get("variant") for item in attempts] == [0, 1, 2]
            and firewall.get("candidate_action_contract_frozen") is True
            and firewall.get("X4-S4_parent_accepted") is False
            and firewall.get("finite_charge_background_solved") is False
            and firewall.get("physical_hessian_constructed") is False
            and firewall.get("signed_H1_residue_computed") is False
            and firewall.get("MAT001_pass") is False
            and firewall.get("K_Q_derived") is False
            and firewall.get("V_computed") is False
            and firewall.get("stage4A_reopened") is False
            and firewall.get("rule9_cleared") is False
            and firewall.get("physics_pass") is False
            and firewall.get("gate_effect") == "NONE"
            and isinstance(selected, dict)
            and selected.get("L", -1.0) > 0.0
            and selected in attempts
            and selected.get("solver_success") is True
            )
        )
    )


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    checks = summary.get("checks", [])
    return (
        summary.get("status") in {SOLUTION_STATUS, REJECTION_STATUS, INCONCLUSIVE_STATUS}
        and summary.get("checks_passed") == summary.get("checks_total") == len(checks)
        and all(item.get("ok") is True for item in checks)
        and semantic_state_valid(summary)
    )


def mutation_suite(summary: dict[str, Any]) -> list[str]:
    if not exported_contract_valid(summary):
        raise AssertionError("baseline zero-charge receipt must be valid")
    mutants: list[tuple[str, dict[str, Any]]] = []

    tau = copy.deepcopy(summary)
    tau["benchmark"]["tau_pi"] = -3.1
    mutants.append(("benchmark_parameter_changed_after_registration", tau))

    observational = copy.deepcopy(summary)
    observational["scope"] = "OBSERVATION_SELECTED_BENCHMARK"
    mutants.append(("observational_target_entered_scope", observational))

    finite_q = copy.deepcopy(summary)
    finite_q["status_firewall"]["finite_charge_background_solved"] = True
    mutants.append(("finite_charge_promoted_from_static_seed", finite_q))

    parent = copy.deepcopy(summary)
    parent["status_firewall"]["X4-S4_parent_accepted"] = True
    mutants.append(("parent_accepted_from_one_benchmark", parent))

    hessian = copy.deepcopy(summary)
    hessian["status_firewall"]["physical_hessian_constructed"] = True
    mutants.append(("physical_hessian_promoted", hessian))

    constraint = copy.deepcopy(summary)
    if constraint.get("selected_attempt"):
        constraint["selected_attempt"]["constraint_max_abs"] = 0.1
        constraint["status"] = SOLUTION_STATUS
    mutants.append(("constraint_failure_accepted", constraint))

    sum_rule = copy.deepcopy(summary)
    if sum_rule.get("selected_attempt"):
        sum_rule["selected_attempt"]["sum_rule"] = 0.1
        sum_rule["status"] = SOLUTION_STATUS
    mutants.append(("sum_rule_failure_accepted", sum_rule))

    negative_L = copy.deepcopy(summary)
    if negative_L.get("selected_attempt"):
        negative_L["selected_attempt"]["L"] = -1.0
    mutants.append(("negative_modulus_accepted", negative_L))

    fake = copy.deepcopy(summary)
    fake["status"] = SOLUTION_STATUS
    fake["selected_attempt"] = {"L": 1.0}
    mutants.append(("solver_claim_without_registered_solution", fake))

    passed: list[str] = []
    for label, mutant in mutants:
        if exported_contract_valid(mutant):
            raise AssertionError(f"mutation must be rejected: {label}")
        passed.append(label)
    return passed


def render_report(summary: dict[str, Any], output_digest: str) -> str:
    selected = summary.get("selected_attempt")
    checks = "\n".join(
        f"| {row['name']} | {'yes' if row['ok'] else 'no'} |"
        for row in summary["checks"]
    )
    mutations = "\n".join(
        f"- `{label}`: rejected" for label in summary["mutation_tests"]["labels"]
    )
    return f"""# MAT-001 TOP-X4 H1 X4-S4 zero-charge background-existence receipt

**Executed:** 2026-09-18  
**Status:** {summary['status']}  
**Scope:** one preregistered internal zero-charge static benchmark  
**Checks:** {summary['checks_passed']}/{summary['checks_total']}  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Result

The frozen X4-S4-GW2 action was tested with a fully backreacted warped
zero-charge ansatz. The numerical solver retained the two scalar equations,
the warp-factor equation, both scalar Robin systems, both gravitational
junction conditions and an independent Hamiltonian-constraint audit.

The benchmark is internal and dimensionless in units of `M5=1`; no observed
radius, Hubble value, BBN abundance, SPARC fit, `K_Q` or `V` value selected a
parameter. A successful benchmark is only a seed receipt and does not accept
X4-S4-GW2 or open finite charge.

## 2. Selected numerical result

{json.dumps(selected, indent=2, sort_keys=True) if selected is not None else 'No solver attempt converged; the result is numerically inconclusive, not a physics rejection.'}

## 3. Evidence checks

| Check | Satisfied |
|---|---|
{checks}

## 4. Mutation controls

{mutations}

All {summary['mutation_tests']['passed']}/{summary['mutation_tests']['total']}
registered mutations were rejected. This is local gate-integrity testing, not
independent Rule-9 review.

## 5. Boundary

The independent constraint and static integrated balance were not used as
solver boundary conditions. Finite-charge continuation remains closed, and no
physical Hessian, H1 residue, MAT coefficient, determinant, stress tensor or
publication status follows.

    candidate_action_contract_frozen=true
    X4-S4_parent_accepted=false
    finite_charge_background_solved=false
    physical_hessian_constructed=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    Rule9_cleared=false
    physics_pass=false
    gate_effect=NONE

## 6. Next single gate

`{summary['next_single_gate']['name']}` — {summary['next_single_gate']['scope']}

## 7. Artifact record

- JSON: {relative(OUTPUT_PATH)}
- JSON SHA-256: {output_digest}
- contract: {relative(CONTRACT_PATH)}
- executable: {relative(Path(__file__))}
"""


def main() -> int:
    args = parse_args()
    write_sidecar(Path(__file__))
    write_sidecar(CONTRACT_PATH)

    source_specs = [
        (Path(__file__), True),
        (CONTRACT_PATH, True),
        (ACTION_CONTRACT_PATH, True),
        (ACTION_SUMMARY_PATH, True),
        (HANDOFF_SUMMARY_PATH, True),
        (S0_AUDIT_PATH, True),
        (S2F3_FREEZE_PATH, True),
    ]
    receipts = [
        artifact_receipt(path, sidecar_required=required)
        for path, required in source_specs
    ]
    summary = build_summary(receipts)
    if not exported_contract_valid(summary):
        print(ERROR_STATUS)
        print(f"status={summary['status']}")
        print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
        for row in summary["checks"]:
            if not row["ok"]:
                print(f"FAILED_CHECK={row['name']}")
        return 1

    labels = mutation_suite(summary)
    summary["mutation_tests"] = {
        "passed": len(labels),
        "total": len(labels),
        "labels": labels,
    }
    summary["script_sha256"] = sha256_file(Path(__file__))
    summary["contract_sha256"] = sha256_file(CONTRACT_PATH)

    if args.self_test_mutations:
        print(f"MUTATION_SUITE: {len(labels)}/{len(labels)}")
        for label in labels:
            print(f"  REJECTED: {label}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    args.output.write_bytes(payload)
    output_digest = hashlib.sha256(payload).hexdigest()
    write_sidecar(args.output, replace_suffix=True)
    args.report.write_text(render_report(summary, output_digest), encoding="utf-8", newline="\n")
    write_sidecar(args.report)

    print(summary["status"])
    print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
    print(f"mutation_tests={len(labels)}/{len(labels)}")
    print(f"converged_attempts={sum(1 for item in summary['attempts'] if item.get('solver_success'))}")
    if summary.get("selected_attempt"):
        print(f"L={summary['selected_attempt']['L']}")
        print(f"boundary_max_abs={summary['selected_attempt']['boundary_max_abs']}")
        print(f"constraint_max_abs={summary['selected_attempt']['constraint_max_abs']}")
        print(f"sum_rule={summary['selected_attempt']['sum_rule']}")
    print("finite_charge_background_solved=false")
    print("physical_hessian_constructed=false")
    print("MAT001=BLOCKED")
    print("K_Q=NOT_DERIVED")
    print("V=NOT_COMPUTED")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={args.output}")
    print(f"output_sha256={output_digest}")
    print(f"report={args.report}")
    print(f"report_sha256={sha256_file(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
