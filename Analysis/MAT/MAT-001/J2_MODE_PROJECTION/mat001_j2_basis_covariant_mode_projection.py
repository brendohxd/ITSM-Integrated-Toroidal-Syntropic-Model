#!/usr/bin/env python3
"""MAT-001 J2: basis-covariant canonical physical-mode projection template.

The audit derives the invariant source coupling after algebraic constraints
are eliminated. It uses an exact rational toy chart to test the method and
consumes the fail-closed UVIR-to-MAT handoff contract. It does not import live
UVIR action matrices and therefore does not compute V.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import sympy as sp


PASS_STATUS = "PASS_MAT001_J2_BASIS_COVARIANT_MODE_PROJECTION_TEMPLATE"
FAIL_STATUS = "FAIL_MAT001_J2_BASIS_COVARIANT_MODE_PROJECTION_TEMPLATE"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--handoff-summary",
        type=Path,
        default=mat
        / "HANDOFF"
        / "outputs"
        / "mat001_uvir_handoff_contract_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.is_file():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}:{exc}"
    if not isinstance(data, dict):
        return None, "top_level_not_object"
    return data, None


def handoff_contract(data: dict[str, Any] | None) -> bool:
    return bool(
        data
        and data.get("subgate_status") == "PASS_MAT001_UVIR_HANDOFF_CONTRACT_BLOCKED"
        and data.get("calculation_status") == "PASS"
        and data.get("handoff_audit_pass") is True
        and data.get("structural_handoff_status") == "READY_FOR_SCOPED_PROJECTION_AUDIT"
        and data.get("numeric_matching_status") == "BLOCKED_INPUTS_NOT_DERIVED"
        and data.get("V_status") == "NOT_COMPUTED"
        and data.get("mat001_pass") is False
        and data.get("physics_pass") is False
        and data.get("stage4A_status") == "CLOSED"
    )


def require_symmetric(matrix: sp.Matrix, name: str) -> None:
    if matrix.rows != matrix.cols:
        raise ValueError(f"{name} must be square")
    if matrix != matrix.T:
        raise ValueError(f"{name} must be symmetric")


def require_positive_definite(matrix: sp.Matrix, name: str) -> None:
    require_symmetric(matrix, name)
    if not all(value > 0 for value in matrix.cholesky().diagonal()):
        raise ValueError(f"{name} must be positive definite")


def require_invertible(matrix: sp.Matrix, name: str) -> None:
    if matrix.rows != matrix.cols or matrix.det() == 0:
        raise ValueError(f"{name} must be square and invertible")


def effective_blocks(
    A: sp.Matrix,
    B: sp.Matrix,
    C: sp.Matrix,
    d: sp.Matrix,
    h: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix]:
    """Return A_eff and c_eff after eliminating algebraic z.

    Convention:
      L = 1/2 xdot^T K xdot - 1/2 x^T A x - x^T B z
          - 1/2 z^T C z + rho (d^T x + h^T z)
      z = C^-1 (rho h - B^T x)
      A_eff = A - B C^-1 B^T
      c_eff = d - B C^-1 h
    """
    require_symmetric(A, "A")
    require_invertible(C, "C")
    require_symmetric(C, "C")
    if B.shape != (A.rows, C.rows):
        raise ValueError("B shape is incompatible with A and C")
    if d.shape != (A.rows, 1) or h.shape != (C.rows, 1):
        raise ValueError("source vectors have incompatible shapes")
    C_inv = C.inv()
    return (
        sp.simplify(A - B * C_inv * B.T),
        sp.simplify(d - B * C_inv * h),
    )


def canonical_coupling(K: sp.Matrix, source: sp.Matrix, mode: sp.Matrix) -> sp.Expr:
    require_positive_definite(K, "K")
    if source.shape != mode.shape or mode.shape != (K.rows, 1):
        raise ValueError("source and mode must be compatible column vectors")
    norm_sq = sp.simplify((mode.T * K * mode)[0])
    if norm_sq <= 0:
        raise ValueError("mode kinetic norm must be positive")
    return sp.simplify((source.T * mode)[0] / sp.sqrt(norm_sq))


def expect_value_error(action: Callable[[], Any]) -> bool:
    try:
        action()
    except ValueError:
        return True
    except Exception:
        return False
    return False


def rows(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)]


def vector(vector_value: sp.Matrix) -> list[str]:
    return [str(vector_value[i, 0]) for i in range(vector_value.rows)]


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def main() -> None:
    args = parse_args()
    handoff, handoff_error = load_json(args.handoff_summary)
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "upstream_fail_closed_handoff_contract",
        handoff_contract(handoff),
        source=args.handoff_summary.name,
        parse_error=handoff_error,
    )

    # Exact two-mode plus one-constraint template. A is selected so that the
    # Schur-reduced A_eff has generalized eigenpairs (2,e1) and (3,e2).
    K = sp.diag(4, 9)
    B = sp.Matrix([[1], [2]])
    C = sp.Matrix([[5]])
    h = sp.Matrix([2])
    c_eff_target = sp.Matrix([5, 7])
    d = sp.simplify(c_eff_target + B * C.inv() * h)
    A_eff_target = sp.diag(8, 27)
    A = sp.simplify(A_eff_target + B * C.inv() * B.T)

    A_eff, c_eff = effective_blocks(A, B, C, d, h)
    add_check(
        checks,
        "constraint_elimination_recovers_effective_blocks",
        A_eff == A_eff_target and c_eff == c_eff_target,
        A_eff=rows(A_eff),
        c_eff=vector(c_eff),
        formula="A_eff=A-B*C^-1*B^T; c_eff=d-B*C^-1*h",
    )

    modes = {
        "mode_1": {"e": sp.Matrix([sp.Rational(1, 2), 0]), "lambda": sp.Rational(2)},
        "mode_2": {"e": sp.Matrix([0, sp.Rational(1, 3)]), "lambda": sp.Rational(3)},
    }
    mode_rows: list[dict[str, Any]] = []
    for name, entry in modes.items():
        e = entry["e"]
        eigenvalue = entry["lambda"]
        eigen_ok = sp.simplify(A_eff * e - eigenvalue * K * e) == sp.zeros(2, 1)
        norm = sp.simplify((e.T * K * e)[0])
        coupling = canonical_coupling(K, c_eff, e)
        mode_rows.append(
            {
                "name": name,
                "e": vector(e),
                "generalized_eigenvalue": str(eigenvalue),
                "generalized_eigen_equation_exact": eigen_ok,
                "kinetic_norm": str(norm),
                "canonical_source_coupling": str(coupling),
            }
        )
    add_check(
        checks,
        "generalized_modes_are_K_orthonormal",
        all(row["generalized_eigen_equation_exact"] and row["kinetic_norm"] == "1" for row in mode_rows)
        and sp.simplify((modes["mode_1"]["e"].T * K * modes["mode_2"]["e"])[0]) == 0,
        modes=mode_rows,
    )

    # Simultaneous dynamical x=R y and constraint z=S w basis changes.
    R = sp.Matrix([[1, 1], [0, 1]])
    S = sp.Matrix([[2]])
    require_invertible(R, "R")
    require_invertible(S, "S")
    K_y = sp.simplify(R.T * K * R)
    A_y = sp.simplify(R.T * A * R)
    B_y = sp.simplify(R.T * B * S)
    C_y = sp.simplify(S.T * C * S)
    d_y = sp.simplify(R.T * d)
    h_y = sp.simplify(S.T * h)
    A_eff_y, c_eff_y = effective_blocks(A_y, B_y, C_y, d_y, h_y)
    add_check(
        checks,
        "schur_blocks_transform_covariantly",
        sp.simplify(A_eff_y - R.T * A_eff * R) == sp.zeros(2, 2)
        and sp.simplify(c_eff_y - R.T * c_eff) == sp.zeros(2, 1),
        dynamical_basis_map="x=R*y",
        constraint_basis_map="z=S*w",
    )

    coupling_invariance_rows = []
    for name, entry in modes.items():
        e_x = entry["e"]
        e_y = sp.simplify(R.inv() * e_x)
        g_x = canonical_coupling(K, c_eff, e_x)
        g_y = canonical_coupling(K_y, c_eff_y, e_y)
        coupling_invariance_rows.append(
            {
                "name": name,
                "g_original": str(g_x),
                "g_transformed": str(g_y),
                "exact": sp.simplify(g_x - g_y) == 0,
            }
        )
    add_check(
        checks,
        "canonical_mode_couplings_are_basis_invariant",
        all(row["exact"] for row in coupling_invariance_rows),
        results=coupling_invariance_rows,
        identity="g_can=(c_eff^T*u)/sqrt(u^T*K*u)",
    )

    Z_phi, alpha = sp.symbols("Z_phi alpha", positive=True)
    g_phi = sp.symbols("g_phi", real=True, nonzero=True)
    K_single = sp.Matrix([[Z_phi]])
    c_single = sp.Matrix([g_phi])
    u_single = sp.Matrix([1])
    g_single = canonical_coupling(K_single, c_single, u_single)
    K_rescaled = sp.Matrix([[alpha**2 * Z_phi]])
    c_rescaled = sp.Matrix([alpha * g_phi])
    g_rescaled = canonical_coupling(K_rescaled, c_rescaled, u_single)
    add_check(
        checks,
        "single_field_limit_recovers_J1_identity",
        sp.simplify(g_single - g_phi / sp.sqrt(Z_phi)) == 0
        and sp.simplify(g_single - g_rescaled) == 0,
        result="g_phi/sqrt(Z_phi)",
        relation_to_J1="This is the structural V identity, not a numerical V computation.",
    )

    oriented_mode = modes["mode_2"]["e"]
    oriented_coupling = canonical_coupling(K, c_eff, oriented_mode)
    reversed_coupling = canonical_coupling(K, c_eff, -oriented_mode)
    add_check(
        checks,
        "mode_orientation_reversal_flips_signed_coupling",
        sp.simplify(reversed_coupling + oriented_coupling) == 0,
        oriented_coupling=str(oriented_coupling),
        reversed_coupling=str(reversed_coupling),
        rule="u -> -u implies g_can -> -g_can; an eigenvector orientation anchor is mandatory",
    )

    # Use the second mode because it has components along both transformed
    # y-basis directions; the first mode is accidentally fixed by this R and
    # would make several deliberately wrong operations numerically coincide.
    sample_e = modes["mode_2"]["e"]
    correct = canonical_coupling(K, c_eff, sample_e)
    wrong_untransformed_source = canonical_coupling(K_y, c_eff, R.inv() * sample_e)
    wrong_untransformed_mode = canonical_coupling(K_y, c_eff_y, sample_e)
    euclidean_original = sp.simplify((c_eff.T * sample_e)[0] / sp.sqrt((sample_e.T * sample_e)[0]))
    e_y_sample = R.inv() * sample_e
    euclidean_transformed = sp.simplify((c_eff_y.T * e_y_sample)[0] / sp.sqrt((e_y_sample.T * e_y_sample)[0]))
    source_without_constraint = d
    wrong_omit_constraint = canonical_coupling(K, source_without_constraint, sample_e)
    negative_controls = {
        "untransformed_source_covector_changes_result": sp.simplify(correct - wrong_untransformed_source) != 0,
        "untransformed_mode_vector_changes_result": sp.simplify(correct - wrong_untransformed_mode) != 0,
        "euclidean_normalization_is_not_basis_invariant": sp.simplify(euclidean_original - euclidean_transformed) != 0,
        "omitting_constraint_source_dressing_changes_result": sp.simplify(correct - wrong_omit_constraint) != 0,
        "absolute_value_erases_mode_orientation": (
            sp.simplify(sp.Abs(correct) - sp.Abs(-correct)) == 0
            and sp.simplify(correct - (-correct)) != 0
        ),
    }
    add_check(
        checks,
        "projection_negative_controls_detect_inconsistent_operations",
        all(negative_controls.values()),
        cases=negative_controls,
    )

    malformed = {
        "singular_constraint_matrix": expect_value_error(
            lambda: effective_blocks(A, B, sp.zeros(1, 1), d, h)
        ),
        "nonsymmetric_kinetic_matrix": expect_value_error(
            lambda: canonical_coupling(sp.Matrix([[1, 1], [0, 1]]), c_eff, sample_e)
        ),
        "indefinite_kinetic_matrix": expect_value_error(
            lambda: canonical_coupling(sp.diag(1, -1), c_eff, sample_e)
        ),
        "zero_kinetic_norm_mode": expect_value_error(
            lambda: canonical_coupling(K, c_eff, sp.zeros(2, 1))
        ),
        "wrong_source_shape": expect_value_error(
            lambda: canonical_coupling(K, sp.Matrix([1]), sample_e)
        ),
        "singular_basis_map": expect_value_error(lambda: require_invertible(sp.zeros(2, 2), "R")),
    }
    add_check(
        checks,
        "malformed_projection_inputs_rejected",
        all(malformed.values()),
        cases=malformed,
    )

    live_export = {
        "action_level_dynamical_kinetic_metric": "NOT_PROVIDED_TO_THIS_TEMPLATE",
        "action_level_algebraic_constraint_matrix": "NOT_PROVIDED_TO_THIS_TEMPLATE",
        "action_level_matter_source_covectors": "NOT_PROVIDED_TO_THIS_TEMPLATE",
        "physical_mode_direction_in_same_chart": "NOT_PROVIDED_TO_THIS_TEMPLATE",
        "numeric_V": "NOT_COMPUTED",
    }
    firewall = {
        "uses_live_UVIR_action_matrices": False,
        "computes_numeric_V": False,
        "derives_numeric_K_Q": False,
        "reopens_stage4A": False,
        "claims_MAT_pass": False,
        "claims_UVIR_pass": False,
        "claims_downstream_Derived": False,
        "physics_pass": False,
    }
    add_check(
        checks,
        "live_export_and_claim_firewall_fail_closed",
        all(status in {"NOT_PROVIDED_TO_THIS_TEMPLATE", "NOT_COMPUTED"} for status in live_export.values())
        and all(value is False for value in firewall.values()),
        live_export=live_export,
        flags=firewall,
    )

    all_ok = all(check["ok"] for check in checks)
    subgate = PASS_STATUS if all_ok else FAIL_STATUS
    summary: dict[str, Any] = {
        "gate": "MAT-001",
        "stage": "J2_BASIS_COVARIANT_PHYSICAL_MODE_PROJECTION",
        "label": "exact_symbolic_template_not_live_matching",
        "subgate_status": subgate,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "projection_identity_status": "DERIVED_TEMPLATE",
        "live_action_export_status": "NOT_PROVIDED",
        "numeric_matching_status": "BLOCKED_LIVE_ACTION_EXPORT_REQUIRED",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "quadratic_convention": {
            "lagrangian": "1/2 xdot^T K xdot - 1/2 x^T A x - x^T B z - 1/2 z^T C z + rho(d^T x + h^T z)",
            "constraint_solution": "z=C^-1(rho*h-B^T*x)",
            "effective_operator": "A_eff=A-B*C^-1*B^T",
            "effective_source": "c_eff=d-B*C^-1*h",
            "canonical_projection": "g_can=(c_eff^T*u)/sqrt(u^T*K*u)",
            "signed_residue_rule": "g_can is signed in an anchored mode orientation; u -> -u flips g_can",
            "basis_maps": "x=R*y; z=S*w; u_y=R^-1*u; c_eff_y=R^T*c_eff; K_y=R^T*K*R",
        },
        "exact_template": {
            "K": rows(K),
            "A": rows(A),
            "B": rows(B),
            "C": rows(C),
            "d": vector(d),
            "h": vector(h),
            "A_eff": rows(A_eff),
            "c_eff": vector(c_eff),
            "modes": mode_rows,
        },
        "checks": checks,
        "n_checks": len(checks),
        "live_action_export": live_export,
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS derives and verifies the canonical source-projection identity, including "
            "constraint-source dressing and field-basis covariance, on an exact symbolic "
            "template. It does not show that the current UVIR action exports the required "
            "matrices, identify a live physical eigenmode, compute V or K_Q, reopen Stage 4A, "
            "or authorize MAT/UVIR/downstream physics claims."
        ),
        "serial_next": (
            "Inventory the live UVIR quadratic reduction for K, C, B, d and h in one named "
            "field chart. Wire them only if their action-level provenance and dimensions are "
            "explicit; otherwise retain BLOCKED_LIVE_ACTION_EXPORT_REQUIRED."
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_j2_basis_covariant_mode_projection_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "mat001_j2_basis_covariant_mode_projection_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("MAT-001 J2 basis-covariant physical-mode projection")
    print("  projection identity: DERIVED_TEMPLATE")
    print("  live action export: NOT_PROVIDED | V: NOT_COMPUTED")
    for check in checks:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(subgate))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
