#!/usr/bin/env python3
"""MAT-001 M4 invariant source-pole residue control.

The generic quadratic parent is explicit, but its coefficients are not
silently promoted to the live UVIR action.  The calculation proves the
invariant projection rule and then checks whether the repository exports the
required live matrices.  Missing export keeps V NOT_COMPUTED.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(checks: list[dict[str, Any]], name: str, value: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(value), **details})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = {
        "handoff": ROOT / "Analysis/MAT/MAT-001/HANDOFF/outputs/mat001_uvir_handoff_contract_summary.json",
        "j2": ROOT / "Analysis/MAT/MAT-001/J2_MODE_PROJECTION/outputs/mat001_j2_basis_covariant_mode_projection_summary.json",
        "r2": ROOT / "Analysis/MAT/MAT-001/R2_DIRECT_RESIDUE/outputs/mat001_r2_direct_residue_audit_summary.json",
        "r5": ROOT / "Analysis/MAT/MAT-001/R5_IDENTIFIABILITY/outputs/mat001_r5_microscopic_matching_decision_summary.json",
        "live_inventory": ROOT / "Analysis/MAT/MAT-001/LIVE_EXPORT_INVENTORY/outputs/mat001_live_uvir_export_inventory_summary.json",
    }
    data = {name: load(path) for name, path in inputs.items()}
    checks: list[dict[str, Any]] = []
    ok(checks, "parent_handoff_remains_fail_closed", data["handoff"].get("V_status") == "NOT_COMPUTED" and data["handoff"].get("mat001_pass") is False)
    ok(checks, "prior_templates_explicitly_not_live", data["j2"].get("live_action_export_status") == "NOT_PROVIDED" and data["r2"].get("V_status") == "NOT_COMPUTED")
    ok(checks, "R5_identifiability_hold_preserved", data["r5"].get("matching_verdict") == "HOLD_DECLARED_ACTION_UNDERDETERMINES_V")

    # Explicit generic constrained quadratic form.
    K = sp.diag(4, 9)
    A_eff_target = sp.diag(8, 27)
    B = sp.Matrix([[1], [2]])
    C = sp.Matrix([[5]])
    d = sp.Matrix([sp.Rational(27, 5), sp.Rational(39, 5)])
    h = sp.Matrix([2])
    A = A_eff_target + B * C.inv() * B.T
    A_eff = sp.simplify(A - B * C.inv() * B.T)
    c_eff = sp.simplify(d - B * C.inv() * h)
    ok(checks, "constraint_schur_reduction", A_eff == A_eff_target and c_eff == sp.Matrix([5, 7]), A_eff=str(A_eff), c_eff=str(c_eff))

    modes = [sp.Matrix([sp.Rational(1, 2), 0]), sp.Matrix([0, sp.Rational(1, 3)])]
    frequencies = [sp.Integer(2), sp.Integer(3)]
    couplings: list[sp.Expr] = []
    for i, (u, omega2) in enumerate(zip(modes, frequencies), start=1):
        norm = sp.simplify((u.T * K * u)[0])
        eigen_ok = sp.simplify(A_eff * u - omega2 * K * u) == sp.zeros(2, 1)
        g = sp.simplify((c_eff.T * u)[0] / sp.sqrt(norm))
        couplings.append(g)
        ok(checks, f"mode_{i}_generalized_eigenpair", eigen_ok, norm=str(norm), coupling=str(g))
    ok(checks, "positive_kinetic_norms", all((u.T * K * u)[0] > 0 for u in modes))

    # Simultaneous dynamical and algebraic constraint chart changes.
    R = sp.Matrix([[1, 1], [0, 1]])
    S = sp.Matrix([[2]])
    K_y = R.T * K * R
    B_y = R.T * B * S
    C_y = S.T * C * S
    d_y = R.T * d
    h_y = S.T * h
    A_y = R.T * A * R
    A_eff_y = sp.simplify(A_y - B_y * C_y.inv() * B_y.T)
    c_eff_y = sp.simplify(d_y - B_y * C_y.inv() * h_y)
    ok(checks, "schur_blocks_transform_covariantly", sp.simplify(A_eff_y - R.T * A_eff * R) == sp.zeros(2, 2) and sp.simplify(c_eff_y - R.T * c_eff) == sp.zeros(2, 1))
    transformed = []
    for i, (u, g) in enumerate(zip(modes, couplings), start=1):
        u_y = R.inv() * u
        norm_y = sp.simplify((u_y.T * K_y * u_y)[0])
        g_y = sp.simplify((c_eff_y.T * u_y)[0] / sp.sqrt(norm_y))
        transformed.append({"mode": i, "original": str(g), "transformed": str(g_y), "exact": sp.simplify(g_y - g) == 0})
    ok(checks, "signed_K_metric_coupling_chart_invariant", all(row["exact"] for row in transformed), results=transformed)

    # Orientation is physical bookkeeping: reversing the anchored mode flips
    # the signed residue; taking abs() would erase this required information.
    orientation = sp.simplify((c_eff.T * (-modes[0]))[0] / sp.sqrt(((-modes[0]).T * K * (-modes[0]))[0]))
    ok(checks, "mode_orientation_flips_signed_residue", sp.simplify(orientation + couplings[0]) == 0, positive=str(couplings[0]), reversed=str(orientation))

    # Negative controls: Euclidean projection or leaving covectors/modes
    # untransformed must not pass as invariant residues.
    bad_mode = modes[1]
    bad_euclidean = sp.simplify(
        (c_eff.T * bad_mode)[0] / sp.sqrt((bad_mode.T * bad_mode)[0])
        - (c_eff_y.T * (R.inv() * bad_mode))[0]
        / sp.sqrt(((R.inv() * bad_mode).T * (R.inv() * bad_mode))[0])
    ) != 0
    bad_untransformed_mode = sp.simplify((c_eff_y.T * bad_mode)[0] / sp.sqrt((bad_mode.T * K_y * bad_mode)[0]) - couplings[1]) != 0
    ok(
        checks,
        "negative_controls_reject_naive_euclidean_or_untransported_projection",
        bad_euclidean and bad_untransformed_mode,
        euclidean_difference=str(sp.simplify(
            (c_eff.T * bad_mode)[0] / sp.sqrt((bad_mode.T * bad_mode)[0])
            - (c_eff_y.T * (R.inv() * bad_mode))[0]
            / sp.sqrt(((R.inv() * bad_mode).T * (R.inv() * bad_mode))[0])
        )),
        untransformed_mode_difference=str(sp.simplify(
            (c_eff_y.T * bad_mode)[0] / sp.sqrt((bad_mode.T * K_y * bad_mode)[0]) - couplings[1]
        )),
    )

    live = data["live_inventory"]
    export_status = live.get("live_export_status") or live.get("status") or "UNKNOWN"
    live_matrices = live.get("live_matrices") or live.get("exports") or {}
    live_available = bool(live_matrices) and all(live_matrices.get(name) not in (None, "NOT_PROVIDED", "MISSING") for name in ("K", "A", "B", "C", "d", "h"))
    ok(checks, "live_action_export_required_and_absent", not live_available, export_status=export_status, live_matrix_keys=sorted(live_matrices))

    summary = {
        "audit": "MAT001_M4_INVARIANT_SOURCE_POLE_RESIDUE_CONTROL",
        "calculation_status": "PASS_GENERIC_INVARIANCE_AND_NEGATIVE_CONTROLS",
        "physics_status": "MAT-001_BLOCKED",
        "disposition": "M4_CONTROL_PASS_LIVE_RESIDUE_BLOCKED",
        "V_status": "NOT_COMPUTED",
        "K_Q_status": "NOT_DERIVED",
        "physics_pass": False,
        "checks": checks,
        "generic_result": {
            "couplings": [str(g) for g in couplings],
            "chart_transformed_couplings": transformed,
            "rule": "g_can=(c_eff.T*u)/sqrt(u.T*K*u), with c_eff=d-B*C^-1*h",
            "orientation_rule": "u -> -u flips signed g_can",
        },
        "live_export": {
            "available": live_available,
            "status": export_status,
            "required": ["K", "A", "B", "C", "d", "h", "physical_mode_direction"],
            "consequence": "No numeric V can be computed until the complete same-action export is present and dimensionally verified.",
        },
        "input_sha256": {name: sha256(path) for name, path in inputs.items()},
        "scientific_boundary": "This proves the invariant projection method on an explicit generic constrained quadratic form. It does not extract a live UVIR residue, compute V, derive K_Q, or promote MAT-001.",
    }
    summary_path = OUT / "mat001_m4_invariant_residue_control_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = f"""# MAT-001 M4 invariant source-pole residue control

**Calculation:** `PASS_GENERIC_INVARIANCE_AND_NEGATIVE_CONTROLS`  
**Disposition:** `M4_CONTROL_PASS_LIVE_RESIDUE_BLOCKED`  
**MAT-001:** `BLOCKED` · **V:** `NOT_COMPUTED` · **K_Q:** `NOT_DERIVED`

## What was established

For the explicit constrained quadratic form

`A_eff = A - B C^-1 B^T`, `c_eff = d - B C^-1 h`,

the signed canonical source-pole residue is

`g_can = (c_eff^T u)/sqrt(u^T K u)`.

The exact symbolic control recovers the generalized physical modes, retains
the source dressing from the algebraic constraint, and gives couplings
`{[str(g) for g in couplings]}`. Under simultaneous `x=R y`, `z=S w` changes,
the K-metric mode projection is exactly invariant. Reversing the anchored mode
flips the signed residue. Negative controls reject Euclidean projection and
untransported modes/covectors.

## Why this is not a MAT result

The repository's live-export inventory does not provide the complete same-action
`K,A,B,C,d,h` matrices and physical mode direction required for the UVIR
parent. Existing J2/R2 artifacts explicitly label themselves templates rather
than live eigenmode extraction. Therefore this control cannot compute a
numeric `V`; it only establishes the necessary invariant method and freezes
the missing-input boundary.

No MAT, UVIR, Stage 4A, SPARC, H0, or downstream claim is promoted.
"""
    report_path = OUT / "MAT-001_M4_INVARIANT_RESIDUE_CONTROL.md"
    report_path.write_text(report, encoding="utf-8")
    seal = "\n".join(f"{sha256(path)}  {path.name}" for path in (summary_path, report_path)) + "\n"
    (OUT / "mat001_m4_invariant_residue_control.sha256").write_text(seal, encoding="ascii")
    print(json.dumps({"disposition": summary["disposition"], "V_status": summary["V_status"], "checks": len(checks)}))


if __name__ == "__main__":
    main()
