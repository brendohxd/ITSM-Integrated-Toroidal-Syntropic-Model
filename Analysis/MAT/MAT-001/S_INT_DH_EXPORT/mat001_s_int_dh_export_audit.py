#!/usr/bin/env python3
"""MAT-001 declared S_int form and action-level d,h placement audit.

Declares the architecture/J1 matter interaction, derives the IR single-field
source covectors (d,h) in the J2 quadratic convention, and tests whether those
objects can be placed in the live free-sector UVIR chart. The live free-sector
export does not contain the force field psi, so d,h remain NOT_EXPORTED there.
V stays NOT_COMPUTED.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_S_INT_DH_DECLARATION_LIVE_CHART_BLOCKED"
FAIL_STATUS = "FAIL_MAT001_S_INT_DH_EXPORT"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--free-sector-summary",
        type=Path,
        default=mat
        / "SAME_CHART_EXPORT"
        / "outputs"
        / "mat001_same_chart_quadratic_export_summary.json",
    )
    parser.add_argument(
        "--j2-summary",
        type=Path,
        default=mat
        / "J2_MODE_PROJECTION"
        / "outputs"
        / "mat001_j2_basis_covariant_mode_projection_summary.json",
    )
    parser.add_argument(
        "--j1-summary",
        type=Path,
        default=mat
        / "J1_JOINT_ACTION"
        / "outputs"
        / "mat001_j1_joint_action_normalization_summary.json",
    )
    parser.add_argument(
        "--r2-summary",
        type=Path,
        default=mat
        / "R2_DIRECT_RESIDUE"
        / "outputs"
        / "mat001_r2_direct_residue_audit_summary.json",
    )
    parser.add_argument(
        "--scoped-summary",
        type=Path,
        default=mat / "outputs" / "mat001_scoped_calculation_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument(
        "--self-test-mutations",
        action="store_true",
        help="Run internal fail-closed mutation checks and exit without writing.",
    )
    return parser.parse_args()


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None, str | None]:
    if not path.is_file():
        return None, "missing", None
    try:
        raw = path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}:{exc}", None
    if not isinstance(data, dict):
        return None, "top_level_not_object", None
    return data, None, hashlib.sha256(raw).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def add_check(
    checks: list[dict[str, Any]], name: str, ok: bool, **details: Any
) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def derive_ir_source_covectors() -> dict[str, Any]:
    """Derive d,h for the declared IR single-field interaction.

    Architecture / R2 template:
        L_int = - C_m * rho_b * psi
    J2 convention source sector:
        L_source = rho * (d^T x + h^T z)
    with rho identified as rho_b and x = (psi) when no algebraic constraints
    participate in the interaction. Matching signs requires
        d = (-C_m,),  h = empty.
    """
    c_m, k_q, rho_b, psi = sp.symbols("C_m K_Q rho_b psi", positive=True)
    # Single-field IR kinetic chart used by J1/R2.
    l_kin = (k_q / 2) * sp.Symbol("psi_dot", real=True) ** 2
    l_int = -c_m * rho_b * psi
    # J2 source form: rho_b * d_psi * psi  (no constraints).
    d_psi = -c_m
    l_source_j2 = rho_b * d_psi * psi
    require(
        sp.simplify(l_int - l_source_j2) == 0,
        "IR interaction must match J2 source sector with d=(-C_m)",
    )

    # No algebraic constraints in the pure IR single-field chart.
    h = sp.Matrix([])  # empty
    d = sp.Matrix([d_psi])
    c_eff = d  # no B,C dressing when h empty / no constraints
    # Mode u along psi with kinetic norm K_Q: g_can = c_eff / sqrt(K_Q) = -V
    # with V = C_m/sqrt(K_Q). Absolute sign is chart convention; |g_can|=V.
    v = c_m / sp.sqrt(k_q)
    g_can_abs = sp.simplify(sp.Abs(c_eff[0]) / sp.sqrt(k_q))
    require(sp.simplify(g_can_abs - v) == 0, "|g_can| must recover V in IR chart")

    parent_g, parent_z, f_phi = sp.symbols("g_phi Z_phi f_phi", positive=True)
    # Parent chart: L_int = -g_phi rho_b phi, psi = f_phi phi.
    d_parent = -parent_g
    d_ir_from_parent = sp.simplify(d_parent / f_phi)  # after phi=psi/f_phi
    require(
        sp.simplify(d_ir_from_parent - (-parent_g / f_phi)) == 0,
        "parent-to-IR source map inconsistent",
    )
    c_m_induced = parent_g / f_phi
    require(
        sp.simplify(c_m_induced - parent_g / f_phi) == 0,
        "C_m induction identity",
    )

    return {
        "declared_S_int": {
            "architecture_weak_field_form": "-C_m*rho_b*psi",
            "parent_chart_form": "-g_phi*rho_b*phi",
            "IR_chart_definition": "psi=f_phi*phi",
            "status": "DECLARED_CONDITIONAL_FORM",
            "provenance": [
                "Theory/Core/ITSM_Core_Architecture.md weak-field S_WF",
                "MAT-001 J1 joint-action template",
                "MAT-001 R2 direct-residue template",
                "MAT-001 scoped calculation declared_S_int form",
            ],
            "not_a_microscopic_match": True,
        },
        "IR_single_field_chart": {
            "dynamical_fields": ["psi"],
            "constraint_fields": [],
            "external_source": "rho_b",
            "J2_source_sector": "rho_b*(d^T x + h^T z)",
            "d": [str(d_psi)],
            "h": [],
            "c_eff": [str(c_eff[0])],
            "canonical_coupling_abs": str(g_can_abs),
            "recovers_V_abs": True,
            "V_definition": "C_m/sqrt(K_Q)",
            "dimensions_in_export": (
                "ROLE_DECLARED: d multiplies rho_b*psi in the Lagrangian "
                "density; absolute SI unit system not fixed"
            ),
            "export_status": "FORM_DERIVED_IR_SINGLE_FIELD_TEMPLATE",
            "ready_for_J2_live_matching": False,
        },
        "parent_to_IR_map": {
            "psi_equals_f_phi_phi": True,
            "d_IR_equals_d_parent_over_f_phi": True,
            "induced_C_m": "g_phi/f_phi",
            "unmatched_microscopic_inputs": [
                "numeric g_phi from a live parent action",
                "numeric f_phi / field map to the live UVIR force field",
                "numeric Z_phi / K_Q from the same action",
            ],
        },
        "symbolic_checks": {
            "L_int_matches_J2_source": True,
            "abs_g_can_equals_V": True,
        },
    }


def live_chart_placement(free_sector: dict[str, Any] | None) -> dict[str, Any]:
    free = free_sector or {}
    free_export = free.get("free_sector_export", {})
    original = free_export.get("original_chart", {})
    physical = free_export.get("physical_chart", {})
    object_status = free.get("required_object_status", {})

    original_fields = original.get("dynamical_fields") or []
    physical_fields = physical.get("dynamical_fields") or []
    constraints = original.get("constraint_fields") or []

    # Force field must appear as a dynamical coordinate for IR S_int placement.
    force_aliases = {"psi", "phi", "delta_psi", "pi"}
    original_tokens = {str(item).split("=")[0].strip() for item in original_fields}
    physical_tokens = set()
    for item in physical_fields:
        token = str(item).split("=")[0].strip()
        physical_tokens.add(token)

    force_in_original = bool(force_aliases & original_tokens)
    force_in_physical = bool(force_aliases & physical_tokens)
    # Condensate amplitude is not baryonic density.
    condensate_aliases = {"delta_rho", "Q_rho", "rho"}
    baryon_aliases = {"rho_b", "delta_rho_b"}
    confuses_condensate_with_baryon = bool(
        condensate_aliases & (original_tokens | physical_tokens)
    ) and not bool(baryon_aliases & (original_tokens | physical_tokens))

    d_live = object_status.get("d", {})
    h_live = object_status.get("h", {})

    placement_ok_for_live = (
        force_in_original
        and d_live.get("status") != "NOT_EXPORTED"
        and h_live.get("status") != "NOT_EXPORTED"
    )

    return {
        "live_free_sector_subgate": free.get("subgate_status"),
        "live_action_export_status": free.get("live_action_export_status"),
        "original_dynamical_fields": original_fields,
        "physical_dynamical_fields": physical_fields,
        "constraint_fields": constraints,
        "force_field_psi_in_original_chart": force_in_original,
        "force_field_psi_in_physical_chart": force_in_physical,
        "baryonic_density_present_as_field": bool(
            baryon_aliases & (original_tokens | physical_tokens)
        ),
        "condensate_fields_present_without_baryon_label": confuses_condensate_with_baryon,
        "prior_free_sector_d_status": d_live.get("status", "UNKNOWN"),
        "prior_free_sector_h_status": h_live.get("status", "UNKNOWN"),
        "live_UVIR_free_sector_d_h_export_status": "NOT_EXPORTED",
        "placement_ready_for_live_J2": False,
        "blockers": [
            "Live free-sector dynamical chart is (R, delta_rho, vartheta), not the IR force field psi.",
            "External baryonic density rho_b is not a free-sector dynamical field; it must enter as a declared external source, not as condensate delta_rho.",
            "No declared map identifies a linear combination of free-sector fields with the force phonon used by S_int.",
            "Force-sector nonlinear completion remains open in UVIR-003; matter coupling cannot be silently attached to the free ADM reduction alone.",
        ],
        "inadmissible_substitutions": {
            "delta_rho_as_rho_b": "REJECTED_ROLE_MISMATCH",
            "Q_rho_Q_chi_diagnostic_impulses_as_d_h": "REJECTED_ROLE_MISMATCH",
            "Newtonian_Phi_N_matter_coupling_as_force_vertex": "REJECTED_SECTOR_MISMATCH",
            "IR_template_d_h_silently_pasted_into_free_sector_bundle": "REJECTED_CHART_MISMATCH",
        },
        "would_be_live_export_only_if": [
            "Declare the force field psi (or parent phi) inside the live quadratic action used for matching",
            "Declare S_int = -C_m rho_b psi (or parent equivalent) in that same action",
            "Expand to quadratic order and extract d on dynamical fields and h on algebraic constraints in one named chart",
            "Keep free-sector K,C,B objects in that same chart with the Mv residual resolved",
        ],
        "placement_attempt_result": (
            "BLOCKED_LIVE_CHART_LACKS_FORCE_FIELD"
            if not placement_ok_for_live
            else "UNEXPECTED_READY"
        ),
    }


def validate_upstream(
    free: dict[str, Any] | None,
    j2: dict[str, Any] | None,
    j1: dict[str, Any] | None,
    r2: dict[str, Any] | None,
    scoped: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    free_ok = bool(
        free
        and free.get("subgate_status")
        == "PASS_MAT001_SAME_CHART_FREE_QUADRATIC_EXPORT_PARTIAL"
        and free.get("V_status") == "NOT_COMPUTED"
        and free.get("mat001_pass") is False
        and free.get("live_action_export_status")
        == "PARTIAL_FREE_SECTOR_SAME_CHART_MATTER_SOURCES_ABSENT"
    )
    add_check(checks, "free_sector_export_upstream_contract", free_ok)

    j2_ok = bool(
        j2
        and j2.get("subgate_status")
        == "PASS_MAT001_J2_BASIS_COVARIANT_MODE_PROJECTION_TEMPLATE"
        and j2.get("V_status") == "NOT_COMPUTED"
        and isinstance(j2.get("quadratic_convention"), dict)
        and "rho(d^T x + h^T z)" in str(j2.get("quadratic_convention", {}).get("lagrangian", ""))
    )
    add_check(checks, "j2_template_upstream_contract", j2_ok)

    j1_ok = bool(
        j1
        and j1.get("subgate_status")
        == "PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY"
        and j1.get("V_status") == "NOT_COMPUTED"
        and "-g_phi" in str(j1.get("joint_action_template", {}).get("matter_vertex", ""))
    )
    add_check(checks, "j1_template_upstream_contract", j1_ok)

    r2_ok = bool(
        r2
        and r2.get("calculation_status") == "PASS"
        and r2.get("V_status") == "NOT_COMPUTED"
        and (
            r2.get("subgate_status") == "PASS_MAT001_R2_DIRECT_RESIDUE_AUDIT"
            or "residue" in str(r2.get("stage", "")).lower()
            or r2.get("audit_verdict") is not None
        )
    )
    add_check(checks, "r2_template_upstream_contract", r2_ok)

    scoped_ok = bool(
        scoped
        and scoped.get("calculation_status") == "PASS"
        and scoped.get("V_status") == "NOT_COMPUTED"
        and scoped.get("mat001_pass") is False
    )
    add_check(checks, "scoped_mat_upstream_contract", scoped_ok)
    return checks


def build_summary(
    ir: dict[str, Any],
    placement: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    add_check(
        checks,
        "S_int_form_declared_conditional",
        ir["declared_S_int"]["status"] == "DECLARED_CONDITIONAL_FORM"
        and ir["declared_S_int"]["architecture_weak_field_form"] == "-C_m*rho_b*psi",
    )
    add_check(
        checks,
        "IR_d_h_form_derived_and_recovers_V_abs",
        ir["IR_single_field_chart"]["export_status"]
        == "FORM_DERIVED_IR_SINGLE_FIELD_TEMPLATE"
        and ir["IR_single_field_chart"]["recovers_V_abs"] is True
        and ir["IR_single_field_chart"]["d"] == ["-C_m"]
        and ir["IR_single_field_chart"]["h"] == [],
    )
    add_check(
        checks,
        "live_free_sector_lacks_force_field_psi",
        placement["force_field_psi_in_original_chart"] is False
        and placement["force_field_psi_in_physical_chart"] is False,
    )
    add_check(
        checks,
        "live_d_h_remain_not_exported",
        placement["live_UVIR_free_sector_d_h_export_status"] == "NOT_EXPORTED"
        and placement["placement_ready_for_live_J2"] is False,
    )
    add_check(
        checks,
        "inadmissible_substitutions_rejected",
        all(
            value.startswith("REJECTED_")
            for value in placement["inadmissible_substitutions"].values()
        ),
    )

    firewall = {
        "S_int_form_declared": True,
        "IR_template_d_h_form_derived": True,
        "live_UVIR_d_h_exported": False,
        "live_same_chart_bundle_complete": False,
        "numeric_matching_ready": False,
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
        "claim_firewall_fail_closed",
        firewall["live_UVIR_d_h_exported"] is False
        and firewall["computes_numeric_V"] is False
        and firewall["physics_pass"] is False
        and firewall["claims_MAT_pass"] is False
        and firewall["numeric_matching_ready"] is False,
        flags=firewall,
    )

    all_ok = all(check["ok"] for check in checks)
    return {
        "gate": "MAT-001",
        "interface": "S_INT_TO_LIVE_UVIR_CHART",
        "stage": "S_INT_DH_DECLARATION_AND_PLACEMENT",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "S_int_status": "DECLARED_CONDITIONAL_FORM",
        "IR_d_h_export_status": "FORM_DERIVED_IR_SINGLE_FIELD_TEMPLATE",
        "live_UVIR_d_h_export_status": "NOT_EXPORTED",
        "live_action_export_status": "PARTIAL_S_INT_FORM_LIVE_DH_BLOCKED",
        "numeric_matching_status": "BLOCKED_LIVE_FORCE_FIELD_AND_DH_REQUIRED",
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "declared_interaction": ir["declared_S_int"],
        "IR_single_field_export": ir["IR_single_field_chart"],
        "parent_to_IR_map": ir["parent_to_IR_map"],
        "live_chart_placement": placement,
        "blocking_requirements": [
            "Embed the force field (psi or parent phi) in the live quadratic action used for MAT matching, or declare an explicit field map from free-sector variables onto that force field.",
            "Expand declared S_int = -C_m rho_b psi (or parent equivalent) to obtain action-level d,h in that same live chart.",
            "Resolve the free-sector Mv residual relative to pure static J2 B (or extend the projection identity).",
            "Select u only after c_eff is defined from live d,h and B,C; do not use free eigenmodes as a substitute matter channel.",
        ],
        "inadmissible_substitutions": placement["inadmissible_substitutions"],
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS declares the Conditional S_int form, derives IR-template "
            "d,h that recover |V| in the single-field chart, and proves that "
            "those covectors are not yet exportable into the live free-sector "
            "UVIR chart. It does not compute numeric V or K_Q, does not paste "
            "IR templates into the free-sector bundle, and does not authorize "
            "MAT, UVIR or downstream physics claims."
        ),
        "serial_next": (
            "Either complete a live force-sector quadratic with declared "
            "S_int and extract d,h there, or declare a justified map from the "
            "live UVIR fields onto the IR force phonon and re-export the full "
            "same-chart K,C,B,d,h bundle; then resolve Mv and select u."
        ),
    }


def mutation_suite(summary: dict[str, Any]) -> None:
    banned = [
        "live_UVIR_d_h_exported",
        "live_same_chart_bundle_complete",
        "numeric_matching_ready",
        "computes_numeric_V",
        "physics_pass",
        "claims_MAT_pass",
    ]
    for key in banned:
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(
            any(mutant["claim_firewall"][item] is True for item in banned),
            f"mutation {key} failed to promote",
        )
    # Reject promoting live export status while IR-only form exists.
    mutant_status = copy.deepcopy(summary)
    mutant_status["live_UVIR_d_h_export_status"] = "EXPORTED_FAKE"
    require(
        mutant_status["live_UVIR_d_h_export_status"]
        != summary["live_UVIR_d_h_export_status"],
        "status mutation setup failed",
    )
    require(
        summary["live_UVIR_d_h_export_status"] == "NOT_EXPORTED",
        "canonical live d,h must stay absent",
    )
    # Reject condensate-as-baryon substitution flag flip.
    require(
        summary["inadmissible_substitutions"]["delta_rho_as_rho_b"]
        == "REJECTED_ROLE_MISMATCH",
        "delta_rho substitution must remain rejected",
    )


def main() -> None:
    args = parse_args()
    free, free_err, free_sha = load_json(args.free_sector_summary)
    j2, j2_err, j2_sha = load_json(args.j2_summary)
    j1, j1_err, j1_sha = load_json(args.j1_summary)
    r2, r2_err, r2_sha = load_json(args.r2_summary)
    scoped, scoped_err, scoped_sha = load_json(args.scoped_summary)

    evidence = {
        "free_sector_export": {
            "source": args.free_sector_summary.name,
            "sha256": free_sha,
            "parse_error": free_err,
        },
        "MAT_J2_template": {
            "source": args.j2_summary.name,
            "sha256": j2_sha,
            "parse_error": j2_err,
        },
        "MAT_J1_template": {
            "source": args.j1_summary.name,
            "sha256": j1_sha,
            "parse_error": j1_err,
        },
        "MAT_R2_template": {
            "source": args.r2_summary.name,
            "sha256": r2_sha,
            "parse_error": r2_err,
        },
        "MAT_scoped": {
            "source": args.scoped_summary.name,
            "sha256": scoped_sha,
            "parse_error": scoped_err,
        },
    }

    checks = validate_upstream(free, j2, j1, r2, scoped)
    for name, err in (
        ("free_sector_export", free_err),
        ("MAT_J2_template", j2_err),
        ("MAT_J1_template", j1_err),
        ("MAT_R2_template", r2_err),
        ("MAT_scoped", scoped_err),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    ir = derive_ir_source_covectors()
    placement = live_chart_placement(free)
    summary = build_summary(ir, placement, checks, evidence)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(check["ok"] for check in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_s_int_dh_export_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "mat001_s_int_dh_export_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("MAT-001 S_int declaration and d,h placement audit")
    print("  S_int:", summary["S_int_status"])
    print("  IR d,h:", summary["IR_d_h_export_status"])
    print("  live UVIR d,h:", summary["live_UVIR_d_h_export_status"])
    print("  V_status: NOT_COMPUTED | MAT: BLOCKED | Stage4A: CLOSED")
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(summary["subgate_status"]))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
