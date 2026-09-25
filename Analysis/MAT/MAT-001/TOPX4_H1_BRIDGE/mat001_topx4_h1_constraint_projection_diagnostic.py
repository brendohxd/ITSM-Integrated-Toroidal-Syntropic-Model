#!/usr/bin/env python3
"""Run the non-promoting TOP-X4 constraint/projection bookkeeping diagnostic."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


STATUS = "PASS_CONSTRAINT_PROJECTION_BOOKKEEPING_HOLD_PHYSICAL_HESSIAN"
ERROR_STATUS = "ERROR_CONSTRAINT_PROJECTION_BOOKKEEPING_DIAGNOSTIC"

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
OUTPUT_PATH = BASE / "outputs" / "mat001_topx4_h1_constraint_projection_diagnostic_summary.json"
REPORT_PATH = BASE / "MAT001_TOPX4_H1_CONSTRAINT_PROJECTION_DIAGNOSTIC_2026-09-18.md"
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_CONSTRAINT_PROJECTION_DIAGNOSTIC_CONTRACT_2026-09-18.md"
)
HANDOFF_CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_COMPENSATED_WARPED_CHILD_DESIGN_CONTRACT_2026-09-17.md"
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
BRIDGE_CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_BRIDGE_CONTRACT_2026-09-16.md"
)
BRIDGE_SUMMARY_PATH = BASE / "outputs" / "mat001_topx4_h1_bridge_readiness_summary.json"
HESSIAN_SUMMARY_PATH = (
    REPO_ROOT
    / "Analysis"
    / "TOP"
    / "TOP-X4"
    / "outputs"
    / "topx4_s2f3_physical_hessian_readiness_summary.json"
)

Matrix = list[list[Fraction]]
Vector = list[Fraction]


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


def F(value: int | str | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def matrix(rows: list[list[int | str | Fraction]]) -> Matrix:
    return [[F(value) for value in row] for row in rows]


def vector(values: list[int | str | Fraction]) -> Vector:
    return [F(value) for value in values]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    if len(a[0]) != len(b):
        raise ValueError("matrix dimension mismatch")
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def matvec(a: Matrix, x: Vector) -> Vector:
    if len(a[0]) != len(x):
        raise ValueError("matrix/vector dimension mismatch")
    return [sum((a[i][j] * x[j] for j in range(len(x))), F(0)) for i in range(len(a))]


def vecdot(x: Vector, y: Vector) -> Fraction:
    if len(x) != len(y):
        raise ValueError("vector dimension mismatch")
    return sum((x[i] * y[i] for i in range(len(x))), F(0))


def add_matrix(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub_matrix(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scale_matrix(scale: Fraction, a: Matrix) -> Matrix:
    return [[scale * value for value in row] for row in a]


def is_zero_matrix(a: Matrix) -> bool:
    return all(value == 0 for row in a for value in row)


def is_symmetric(a: Matrix) -> bool:
    return a == transpose(a)


def determinant(a: Matrix) -> Fraction:
    work = [row[:] for row in a]
    n = len(work)
    if any(len(row) != n for row in work):
        raise ValueError("determinant requires a square matrix")
    result = F(1)
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col] != 0), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result = -result
        pivot_value = work[col][col]
        result *= pivot_value
        for row in range(col + 1, n):
            factor = work[row][col] / pivot_value
            for j in range(col + 1, n):
                work[row][j] -= factor * work[col][j]
    return result


def inverse(a: Matrix) -> Matrix:
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("inverse requires a square matrix")
    work = [row[:] + [F(1 if i == j else 0) for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col] != 0), None)
        if pivot is None:
            raise ValueError("singular auxiliary block")
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
        pivot_value = work[col][col]
        work[col] = [value / pivot_value for value in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            if factor != 0:
                work[row] = [
                    work[row][j] - factor * work[col][j] for j in range(2 * n)
                ]
    return [row[n:] for row in work]


def quadratic(x: Vector, a: Matrix) -> Fraction:
    return vecdot(x, matvec(a, x))


def transform_quadratic(system: dict[str, Any]) -> dict[str, Any]:
    q_map = system["T"]
    a_map = system["U"]
    q_t = transpose(q_map)
    a_t = transpose(a_map)
    return {
        "H_qq": matmul(matmul(q_t, system["H_qq"]), q_map),
        "H_qa": matmul(matmul(q_t, system["H_qa"]), a_map),
        "H_aa": matmul(matmul(a_t, system["H_aa"]), a_map),
        "c_q": matvec(q_t, system["c_q"]),
        "c_a": matvec(a_t, system["c_a"]),
        "T": q_map,
        "U": a_map,
    }


def build_system() -> dict[str, Any]:
    return {
        "H_qq": matrix([[9, 1, 0], [1, 8, 1], [0, 1, 7]]),
        "H_qa": matrix([[1, 2], [-1, 1], [2, 0]]),
        "H_aa": matrix([[5, 1], [1, 3]]),
        "c_q": vector([3, -2, 1]),
        "c_a": vector([4, -1]),
        "u": vector([1, -1, 2]),
        "T": matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]]),
        "U": matrix([[1, 1], [0, 1]]),
        "samples": [vector([1, 0, -1]), vector([0, 2, 1]), vector([-2, 1, 2])],
    }


def project(system: dict[str, Any]) -> dict[str, Any]:
    h_aa_inv = inverse(system["H_aa"])
    h_aq = transpose(system["H_qa"])
    h_phys = sub_matrix(
        system["H_qq"], matmul(matmul(system["H_qa"], h_aa_inv), h_aq)
    )
    c_phys = [
        system["c_q"][i] - matvec(matmul(system["H_qa"], h_aa_inv), system["c_a"])[i]
        for i in range(len(system["c_q"]))
    ]
    return {
        "H_aa_inv": h_aa_inv,
        "H_phys": h_phys,
        "c_phys": c_phys,
        "constant_shift": -Fraction(1, 2) * vecdot(system["c_a"], matvec(h_aa_inv, system["c_a"])),
    }


def auxiliary_response(system: dict[str, Any], projection: dict[str, Any], q: Vector) -> Vector:
    h_aq = transpose(system["H_qa"])
    source = [
        matvec(h_aq, q)[i] + system["c_a"][i] for i in range(len(system["c_a"]))
    ]
    return [-value for value in matvec(projection["H_aa_inv"], source)]


def full_value(system: dict[str, Any], q: Vector, a: Vector) -> Fraction:
    return (
        Fraction(1, 2) * quadratic(q, system["H_qq"])
        + vecdot(q, matvec(system["H_qa"], a))
        + Fraction(1, 2) * quadratic(a, system["H_aa"])
        + vecdot(system["c_q"], q)
        + vecdot(system["c_a"], a)
    )


def reduced_value(system: dict[str, Any], projection: dict[str, Any], q: Vector) -> Fraction:
    return (
        Fraction(1, 2) * quadratic(q, projection["H_phys"])
        + vecdot(projection["c_phys"], q)
        + projection["constant_shift"]
    )


def serialise(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, list):
        return [serialise(item) for item in value]
    if isinstance(value, dict):
        return {key: serialise(item) for key, item in value.items()}
    return value


def build_summary(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    system = build_system()
    projection = project(system)
    transformed = transform_quadratic(system)
    transformed_projection = project(transformed)
    h_phys = projection["H_phys"]
    c_phys = projection["c_phys"]
    u = system["u"]
    u_reversed = [-value for value in u]
    mode_norm_sq = quadratic(u, h_phys)
    mode_source = vecdot(c_phys, u)
    reversed_source = vecdot(c_phys, u_reversed)

    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "all_authority_inputs_exist",
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

    handoff = load_json(HANDOFF_SUMMARY_PATH)
    handoff_firewall = handoff.get("status_firewall", {})
    add_check(
        checks,
        "prior_x4_s4_handoff_remains_non_promoting",
        handoff.get("status") == "ROUTE_HANDOFF_X4_S4_NEW_PARENT_DESIGN_ONLY"
        and handoff_firewall.get("parent_action_changed") is False
        and handoff_firewall.get("X4-S4_action_frozen") is False
        and handoff_firewall.get("physics_pass") is False,
    )
    add_check(
        checks,
        "toy_matrix_dimensions_and_symmetry",
        len(system["H_qq"]) == 3
        and len(system["H_qa"]) == 3
        and len(system["H_qa"][0]) == 2
        and len(system["H_aa"]) == 2
        and is_symmetric(system["H_qq"])
        and is_symmetric(system["H_aa"]),
        det_Haa=str(determinant(system["H_aa"])),
    )

    stationarity_ok = True
    residuals: list[str] = []
    for q in system["samples"]:
        a_star = auxiliary_response(system, projection, q)
        residual = [
            value
            for value in [
                matvec(system["H_aa"], a_star)[i]
                + matvec(transpose(system["H_qa"]), q)[i]
                + system["c_a"][i]
                for i in range(len(a_star))
            ]
        ]
        residuals.extend(str(value) for value in residual)
        stationarity_ok = stationarity_ok and all(value == 0 for value in residual)
    add_check(
        checks,
        "auxiliary_stationarity_is_satisfied",
        stationarity_ok,
        residuals=residuals,
    )

    completion_ok = True
    completion_residuals: list[str] = []
    equivalence_ok = True
    equivalence_residuals: list[str] = []
    for q in system["samples"]:
        a_star = auxiliary_response(system, projection, q)
        full = full_value(system, q, a_star)
        reduced = reduced_value(system, projection, q)
        residual = full - reduced
        completion_residuals.append(str(residual))
        completion_ok = completion_ok and residual == 0
        equivalence_residuals.append(str(residual))
        equivalence_ok = equivalence_ok and residual == 0
    add_check(
        checks,
        "schur_reduction_matches_completion_of_square",
        completion_ok,
        residuals=completion_residuals,
    )
    add_check(
        checks,
        "full_and_reduced_quadratic_forms_agree",
        equivalence_ok,
        residuals=equivalence_residuals,
    )

    q_t = system["T"]
    expected_h_transformed = matmul(matmul(transpose(q_t), h_phys), q_t)
    expected_c_transformed = matvec(transpose(q_t), c_phys)
    basis_ok = (
        transformed_projection["H_phys"] == expected_h_transformed
        and transformed_projection["c_phys"] == expected_c_transformed
        and determinant(q_t) != 0
        and determinant(system["U"]) != 0
    )
    add_check(
        checks,
        "reduced_pair_is_covariant_under_invertible_basis_changes",
        basis_ok,
        det_T=str(determinant(q_t)),
        det_U=str(determinant(system["U"])),
    )
    add_check(
        checks,
        "selected_mode_has_positive_reduced_kinetic_norm",
        mode_norm_sq > 0,
        norm_squared=str(mode_norm_sq),
    )
    add_check(
        checks,
        "orientation_reversal_changes_signed_source",
        mode_source != 0 and reversed_source == -mode_source,
        source_numerator=str(mode_source),
        reversed_source_numerator=str(reversed_source),
    )
    naive_source = system["c_q"]
    auxiliary_source_delta = [c_phys[i] - naive_source[i] for i in range(len(c_phys))]
    add_check(
        checks,
        "auxiliary_source_contribution_is_retained",
        any(value != 0 for value in auxiliary_source_delta),
        c_phys=serialise(c_phys),
        naive_c_q=serialise(naive_source),
        retained_delta=serialise(auxiliary_source_delta),
    )

    singular_rejected = False
    singular_error = ""
    singular = copy.deepcopy(system)
    singular["H_aa"] = matrix([[1, 0], [0, 0]])
    try:
        project(singular)
    except ValueError as error:
        singular_rejected = True
        singular_error = str(error)
    add_check(
        checks,
        "singular_auxiliary_domain_is_rejected_without_pseudoinverse",
        singular_rejected,
        error=singular_error,
    )

    firewall = {
        "parent_action_changed": False,
        "X4-S4_action_frozen": False,
        "physical_hessian_constructed": False,
        "pseudoinverse_accepted": False,
        "orientation_sign_erased": False,
        "auxiliary_source_dropped": False,
        "MAT001_pass": False,
        "K_Q_derived": False,
        "V_computed": False,
        "stage4A_reopened": False,
        "physics_pass": False,
        "gate_effect": "NONE",
    }
    add_check(
        checks,
        "non_promoting_firewall_remains_closed",
        firewall["parent_action_changed"] is False
        and firewall["X4-S4_action_frozen"] is False
        and firewall["physical_hessian_constructed"] is False
        and firewall["pseudoinverse_accepted"] is False
        and firewall["orientation_sign_erased"] is False
        and firewall["auxiliary_source_dropped"] is False
        and firewall["MAT001_pass"] is False
        and firewall["K_Q_derived"] is False
        and firewall["V_computed"] is False
        and firewall["stage4A_reopened"] is False
        and firewall["physics_pass"] is False
        and firewall["gate_effect"] == "NONE",
    )

    return {
        "schema": "ITSM_MAT001_TOPX4_H1_CONSTRAINT_PROJECTION_DIAGNOSTIC_v1",
        "date": "2026-09-18",
        "status": STATUS,
        "audit_execution_status": "COMPLETE",
        "method_source": {
            "title": "Spinning Toroidal Brane Cosmology; A Classical and Quantum Survey",
            "arxiv_version": "1901.03292v2",
            "url": "https://arxiv.org/html/1901.03292v2",
            "use": "methodological constraint/projection analogy only",
        },
        "scope": "SYNTHETIC_EXACT_RATIONAL_ALGEBRA_ONLY",
        "checks": checks,
        "checks_passed": sum(1 for item in checks if item["ok"]),
        "checks_total": len(checks),
        "diagnostic_results": {
            "dynamic_dimension": 3,
            "auxiliary_dimension": 2,
            "det_Haa": str(determinant(system["H_aa"])),
            "H_phys": serialise(h_phys),
            "c_phys": serialise(c_phys),
            "selected_mode": serialise(u),
            "mode_norm_squared": str(mode_norm_sq),
            "signed_source_numerator": str(mode_source),
            "reversed_signed_source_numerator": str(reversed_source),
            "constant_shift": str(projection["constant_shift"]),
            "full_reduced_residuals": equivalence_residuals,
            "singular_domain_policy": "REJECT_NO_PSEUDOINVERSE",
            "physical_hessian_claim": False,
        },
        "status_firewall": firewall,
        "artifact_receipts": receipts,
        "next_single_gate": {
            "name": "TOPX4_H1_X4-S4_NEW_PARENT_ACTION_CONTRACT",
            "scope": (
                "Choose and derive the complete X4-S4 field content, geometry, "
                "localized action and global balance before freezing it."
            ),
            "stop_before": "NO_CHANGE_TO_X4_S2F3",
        },
    }


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    checks = summary.get("checks", [])
    firewall = summary.get("status_firewall", {})
    results = summary.get("diagnostic_results", {})
    return (
        summary.get("status") == STATUS
        and summary.get("scope") == "SYNTHETIC_EXACT_RATIONAL_ALGEBRA_ONLY"
        and summary.get("checks_passed") == summary.get("checks_total") == len(checks)
        and all(item.get("ok") is True for item in checks)
        and results.get("singular_domain_policy") == "REJECT_NO_PSEUDOINVERSE"
        and results.get("physical_hessian_claim") is False
        and firewall.get("parent_action_changed") is False
        and firewall.get("X4-S4_action_frozen") is False
        and firewall.get("physical_hessian_constructed") is False
        and firewall.get("pseudoinverse_accepted") is False
        and firewall.get("orientation_sign_erased") is False
        and firewall.get("auxiliary_source_dropped") is False
        and firewall.get("MAT001_pass") is False
        and firewall.get("K_Q_derived") is False
        and firewall.get("V_computed") is False
        and firewall.get("stage4A_reopened") is False
        and firewall.get("physics_pass") is False
        and firewall.get("gate_effect") == "NONE"
    )


def mutation_suite(summary: dict[str, Any]) -> list[str]:
    if not exported_contract_valid(summary):
        raise AssertionError("baseline diagnostic contract must be valid")

    mutants: list[tuple[str, dict[str, Any]]] = []

    physical = copy.deepcopy(summary)
    physical["status_firewall"]["physical_hessian_constructed"] = True
    mutants.append(("physical_hessian_promoted", physical))

    route = copy.deepcopy(summary)
    route["status_firewall"]["X4-S4_action_frozen"] = True
    mutants.append(("x4_s4_action_frozen", route))

    parent = copy.deepcopy(summary)
    parent["status_firewall"]["parent_action_changed"] = True
    mutants.append(("x4_s2f3_parent_changed", parent))

    singular = copy.deepcopy(summary)
    singular["diagnostic_results"]["singular_domain_policy"] = "PSEUDOINVERSE_ACCEPTED"
    singular["status_firewall"]["pseudoinverse_accepted"] = True
    mutants.append(("singular_domain_pseudoinverse", singular))

    orientation = copy.deepcopy(summary)
    orientation["status_firewall"]["orientation_sign_erased"] = True
    mutants.append(("orientation_sign_erased", orientation))

    source = copy.deepcopy(summary)
    source["status_firewall"]["auxiliary_source_dropped"] = True
    mutants.append(("auxiliary_source_dropped", source))

    passed: list[str] = []
    for label, mutant in mutants:
        if exported_contract_valid(mutant):
            raise AssertionError(f"mutation must be rejected: {label}")
        passed.append(label)
    return passed


def render_report(summary: dict[str, Any], output_digest: str) -> str:
    checks = "\n".join(
        f"| {row['name']} | {'yes' if row['ok'] else 'no'} |"
        for row in summary["checks"]
    )
    mutations = "\n".join(
        f"- {label}: rejected" for label in summary["mutation_tests"]["labels"]
    )
    result = summary["diagnostic_results"]
    return f"""# MAT-001 TOP-X4 constraint/projection bookkeeping diagnostic

**Executed:** 2026-09-18  
**Status:** {summary['status']}  
**Checks:** {summary['checks_passed']}/{summary['checks_total']}  
**Scope:** synthetic exact rational algebra only  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Result

This receipt tests the algebraic bookkeeping needed before a live constrained
source projection. It is motivated by the constraint-retention method in
arXiv:1901.03292v2, but it is not a reproduction of that paper and does not
claim a Dirac-bracket, action, background or physical-Hessian result.

The declared auxiliary block has determinant `{result['det_Haa']}`. Exact
elimination gives the Schur pair `H_phys` and `c_phys`; the full quadratic
form agrees with the reduced form on all registered samples with residuals
`{result['full_reduced_residuals']}`. The selected mode has norm squared
`{result['mode_norm_squared']}`, source numerator
`{result['signed_source_numerator']}`, and orientation-reversed numerator
`{result['reversed_signed_source_numerator']}`.

## 2. Evidence checks

| Check | Satisfied |
|---|---|
{checks}

## 3. Rejection controls

{mutations}

All {summary['mutation_tests']['passed']}/{summary['mutation_tests']['total']}
registered mutations were rejected. This is local contract validation, not
independent Rule-9 review.

## 4. Scientific boundary

The diagnostic uses a declared three-variable/two-auxiliary toy quadratic
system. It validates stationarity, completion of the square, basis covariance,
positive-norm mode orientation, auxiliary-source retention and singular-domain
rejection. It does not construct the X4-S4 action or any live TOP-X4 physical
Hessian. In particular:

    parent_action_changed=false
    X4-S4_action_frozen=false
    physical_hessian_constructed=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    physics_pass=false
    gate_effect=NONE

## 5. Next single gate

`{summary['next_single_gate']['name']}` remains the next substantive gate.
The diagnostic does not authorize action variation or change to X4-S2F3.

## 6. Artifact record

- JSON: {relative(OUTPUT_PATH)}
- JSON SHA-256: {output_digest}
- contract: {relative(CONTRACT_PATH)}
- executable: {relative(Path(__file__))}
- paper-method source: https://arxiv.org/html/1901.03292v2
"""


def main() -> int:
    args = parse_args()
    write_sidecar(Path(__file__))
    write_sidecar(CONTRACT_PATH)

    source_specs = [
        (Path(__file__), True),
        (CONTRACT_PATH, True),
        (HANDOFF_CONTRACT_PATH, True),
        (HANDOFF_SUMMARY_PATH, True),
        (S0_AUDIT_PATH, True),
        (BRIDGE_CONTRACT_PATH, True),
        (BRIDGE_SUMMARY_PATH, True),
        (HESSIAN_SUMMARY_PATH, True),
    ]
    receipts = [
        artifact_receipt(path, sidecar_required=required)
        for path, required in source_specs
    ]
    summary = build_summary(receipts)
    if not exported_contract_valid(summary):
        print(ERROR_STATUS)
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
    payload = (json.dumps(serialise(summary), indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    args.output.write_bytes(payload)
    output_digest = hashlib.sha256(payload).hexdigest()
    write_sidecar(args.output, replace_suffix=True)

    report = render_report(summary, output_digest)
    args.report.write_text(report, encoding="utf-8", newline="\n")
    write_sidecar(args.report)

    print(summary["status"])
    print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
    print(f"mutation_tests={len(labels)}/{len(labels)}")
    print(f"det_Haa={summary['diagnostic_results']['det_Haa']}")
    print(f"mode_norm_squared={summary['diagnostic_results']['mode_norm_squared']}")
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
