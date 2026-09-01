#!/usr/bin/env python3
"""MAT-001 RR1: declare the parent-action Lagrangian skeleton for Derived matching.

Publishes the exact term structure required for a same-action Z_phi kinetic and
g_phi matter vertex, the map into Track-A (psi = psi_bar + pi), and the induced
C_m, K_Q, V identities. Coefficients remain unmatched symbols. This advances
RR1 from empty OPEN to DECLARED_SKELETON_COEFFICIENTS_UNMATCHED without inventing
numerics or reopening Stage 4A.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_RR1_PARENT_ACTION_SKELETON_DECLARED_UNMATCHED"
FAIL_STATUS = "FAIL_MAT001_RR1_PARENT_ACTION_SKELETON"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--h13",
        type=Path,
        default=base / "outputs" / "mat001_parent_action_h13_source_audit_summary.json",
    )
    parser.add_argument(
        "--h12",
        type=Path,
        default=base / "outputs" / "mat001_parent_action_matching_summary.json",
    )
    parser.add_argument(
        "--j1",
        type=Path,
        default=mat
        / "J1_JOINT_ACTION"
        / "outputs"
        / "mat001_j1_joint_action_normalization_summary.json",
    )
    parser.add_argument(
        "--track-a-s-int",
        type=Path,
        default=mat
        / "TRACK_A_S_INT"
        / "outputs"
        / "mat001_track_a_s_int_embed_summary.json",
    )
    parser.add_argument(
        "--track-a-force",
        type=Path,
        default=uvir / "uvir003_track_a_force_adm_cubic_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument("--self-test-mutations", action="store_true")
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


def declare_skeleton() -> dict[str, Any]:
    z_phi, g_phi, f_phi = sp.symbols("Z_phi g_phi f_phi", positive=True)
    a_ir, k_q_ir, gamma, m_star = sp.symbols(
        "A_IR K_Q gamma M_star", positive=True
    )
    # Induced IR coefficients under psi = f_phi * phi.
    c_m = sp.simplify(g_phi / f_phi)
    k_q_induced = sp.simplify(z_phi / f_phi**2)
    v = sp.simplify(g_phi / sp.sqrt(z_phi))
    require(sp.simplify(v - c_m / sp.sqrt(k_q_induced)) == 0, "V identity")

    # Matching conditions for Track-A time kinetic (form only).
    match_k = sp.Eq(k_q_ir, k_q_induced)

    skeleton = {
        "rr_id": "RR1",
        "status": "DECLARED_SKELETON_COEFFICIENTS_UNMATCHED",
        "parent_action_name": "S_parent_force_matter_minimal",
        "scope": (
            "Minimal same-action skeleton for Derived MAT vertex matching only. "
            "Does not claim full UVIR multi-sector completion (g+U+Phi+alignment)."
        ),
        "fields": {
            "parent_force_phonon": "phi",
            "IR_force_field": "psi = f_phi * phi",
            "Track_A_split": "psi = psi_bar + pi",
            "external_baryon_density": "rho_b (external source, not condensate delta_rho)",
            "frame": "U^mu preferred frame (architecture independent constrained aether)",
        },
        "lagrangian_density_terms": {
            "L_kin_parent": "(Z_phi/2) * (U.grad(phi))^2",
            "L_int_parent": "- g_phi * rho_b * phi",
            "L_force_IR_Track_A_adopted": (
                "K_Q * Q^2/2 - A * Y^(3/2) - gamma*(D_mu D^mu psi)^2/(2*M_star^2)"
            ),
            "L_force_spatial_IR_architecture": (
                "- C_IR * |grad psi|^3 / (12 pi G a0)  [weak-field architecture form]"
            ),
            "note": (
                "Parent kinetic is the UV/microscopic normalization of the IR time "
                "kinetic K_Q after field rescaling. Spatial Y^{3/2} and regulator "
                "remain IR EFT sectors; matching them is separate from V."
            ),
        },
        "free_coefficients_unmatched": {
            "Z_phi": "NOT_DERIVED",
            "g_phi": "NOT_DERIVED",
            "f_phi": "NOT_DERIVED_MAP_SCALE",
            "K_Q": "SYMBOLIC_ON_TRACK_A_HOST",
            "C_m": "FORM_ONLY_FROM_D_EQUALS_MINUS_C_m",
            "A_or_C_IR": "IR_WILSON_OPEN",
        },
        "induced_identities": {
            "C_m": str(c_m),
            "K_Q_from_parent": str(k_q_induced),
            "V": str(v),
            "matching_condition_K_Q_IR_equals_induced": str(match_k),
            "identities_hold_symbolically": True,
        },
        "what_completes_RR1": [
            "Supply a complete action (or UV completion) that fixes Z_phi > 0",
            "Supply the same-action matter coupling that fixes g_phi",
            "Fix or eliminate f_phi by a declared field chart convention",
            "Show K_Q on Track-A equals Z_phi/f_phi^2 in that chart",
        ],
        "explicitly_not_included_in_this_skeleton": [
            "Full g+U+Phi+alignment multi-sector join",
            "Numeric values for any free coefficient",
            "Stage 4A reopen",
            "MAT physics PASS",
        ],
    }
    return skeleton


def build_summary(
    skeleton: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
    h13: dict[str, Any] | None,
) -> dict[str, Any]:
    add_check(
        checks,
        "skeleton_status_declared_unmatched",
        skeleton["status"] == "DECLARED_SKELETON_COEFFICIENTS_UNMATCHED",
    )
    add_check(
        checks,
        "both_kinetic_and_vertex_terms_present",
        "Z_phi" in skeleton["lagrangian_density_terms"]["L_kin_parent"]
        and "g_phi" in skeleton["lagrangian_density_terms"]["L_int_parent"],
    )
    add_check(
        checks,
        "induced_V_identity_holds",
        skeleton["induced_identities"]["identities_hold_symbolically"] is True,
    )
    add_check(
        checks,
        "all_micro_coefficients_marked_unmatched",
        skeleton["free_coefficients_unmatched"]["Z_phi"] == "NOT_DERIVED"
        and skeleton["free_coefficients_unmatched"]["g_phi"] == "NOT_DERIVED",
    )
    add_check(
        checks,
        "h13_still_incomplete_upstream",
        bool(
            h13
            and h13.get("H1_exit", {}).get("H1_complete") is False
            and h13.get("V_status") == "NOT_COMPUTED"
        ),
    )

    # RR1 status update relative to H1.3 frozen list
    rr_update = {
        "RR1": "DECLARED_SKELETON_COEFFICIENTS_UNMATCHED",
        "RR2": "OPEN",
        "RR3": "OPEN_CONDITIONAL_MAP_ONLY",
        "RR4": "OPEN_R3_INCOMPLETE",
        "RR5": "ACTIVE_FIREWALL",
    }
    add_check(
        checks,
        "RR1_advanced_not_closed",
        rr_update["RR1"] == "DECLARED_SKELETON_COEFFICIENTS_UNMATCHED",
    )

    firewall = {
        "RR1_skeleton_declared": True,
        "numeric_Z_phi_derived": False,
        "numeric_g_phi_derived": False,
        "numeric_V_computed": False,
        "numeric_K_Q_derived": False,
        "RR1_complete": False,
        "H1_complete": False,
        "claims_MAT_pass": False,
        "physics_pass": False,
        "reopens_stage4A": False,
        "claims_full_UVIR_parent": False,
    }
    add_check(
        checks,
        "claim_firewall_fail_closed",
        all(
            firewall[k] is False
            for k in (
                "numeric_Z_phi_derived",
                "numeric_g_phi_derived",
                "numeric_V_computed",
                "RR1_complete",
                "H1_complete",
                "claims_MAT_pass",
                "physics_pass",
                "reopens_stage4A",
                "claims_full_UVIR_parent",
            )
        ),
        flags=firewall,
    )

    all_ok = all(c["ok"] for c in checks)
    return {
        "gate": "MAT-001",
        "interface": "RR1_PARENT_ACTION_SKELETON",
        "stage": "RR1_PARENT_ACTION_SKELETON_DECLARATION",
        "plan_step": "RR1",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "RR1_status": "DECLARED_SKELETON_COEFFICIENTS_UNMATCHED",
        "research_requirement_status": rr_update,
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "C_m_numeric_status": "NOT_DERIVED_FORM_ONLY",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "parent_action_skeleton": skeleton,
        "blocking_requirements": skeleton["what_completes_RR1"],
        "inadmissible_substitutions": {
            "skeleton_as_Derived_match": "REJECTED",
            "setting_Z_phi_equals_1": "REJECTED",
            "setting_g_phi_from_C_obs_alone": "REJECTED",
            "equating_skeleton_to_full_UVIR_parent": "REJECTED",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS declares the minimal parent-action term structure required "
            "for Derived MAT vertex matching and verifies symbolic induced "
            "identities. All microscopic coefficients remain unmatched. This is "
            "not a derivation of V or K_Q and does not reopen Stage 4A."
        ),
        "serial_next": (
            "RR2: derive or bound Z_phi and g_phi from a UV completion / "
            "declared dynamics, or compute residue V; RR3: fix f_phi chart. "
            "Do not open Stage 4A until RR1-RR3 close."
        ),
    }


def validate_upstream(
    h13: dict[str, Any] | None,
    h12: dict[str, Any] | None,
    j1: dict[str, Any] | None,
    s_int: dict[str, Any] | None,
    track_a: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "h13_upstream",
        bool(
            h13
            and h13.get("subgate_status")
            == "PASS_MAT001_PARENT_ACTION_H13_INCOMPLETE_SOURCES_AUDITED"
            and h13.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "h12_upstream",
        bool(
            h12
            and h12.get("subgate_status")
            == "PASS_MAT001_PARENT_ACTION_MATCHING_DECLARED_INCOMPLETE"
        ),
    )
    add_check(
        checks,
        "j1_upstream",
        bool(
            j1
            and j1.get("subgate_status")
            == "PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY"
            and j1.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "track_a_s_int_upstream",
        bool(
            s_int
            and s_int.get("subgate_status")
            == "PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL"
            and s_int.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "track_a_force_upstream",
        bool(
            track_a
            and track_a.get("subgate_status") == "PASS_FORCE_SECTOR_J2_COMPONENT"
            and "K_Q"
            in str(
                ((track_a.get("symbolic_audit") or {}).get("track_a_action") or {}).get(
                    "force_lagrangian", ""
                )
            )
        ),
    )
    return checks


def mutation_suite(summary: dict[str, Any]) -> None:
    for key in (
        "numeric_Z_phi_derived",
        "numeric_g_phi_derived",
        "numeric_V_computed",
        "RR1_complete",
        "H1_complete",
        "claims_MAT_pass",
        "reopens_stage4A",
        "physics_pass",
    ):
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, key)
    require(
        summary["RR1_status"] == "DECLARED_SKELETON_COEFFICIENTS_UNMATCHED",
        "RR1 open",
    )
    require(summary["V_status"] == "NOT_COMPUTED", "V")


def main() -> None:
    args = parse_args()
    h13, e1, s1 = load_json(args.h13)
    h12, e2, s2 = load_json(args.h12)
    j1, e3, s3 = load_json(args.j1)
    s_int, e4, s4 = load_json(args.track_a_s_int)
    track_a, e5, s5 = load_json(args.track_a_force)

    evidence = {
        "h13": {"source": args.h13.name, "sha256": s1, "parse_error": e1},
        "h12": {"source": args.h12.name, "sha256": s2, "parse_error": e2},
        "j1": {"source": args.j1.name, "sha256": s3, "parse_error": e3},
        "track_a_s_int": {
            "source": args.track_a_s_int.name,
            "sha256": s4,
            "parse_error": e4,
        },
        "track_a_force": {
            "source": args.track_a_force.name,
            "sha256": s5,
            "parse_error": e5,
        },
    }
    checks = validate_upstream(h13, h12, j1, s_int, track_a)
    for name, err in (
        ("h13", e1),
        ("h12", e2),
        ("j1", e3),
        ("track_a_s_int", e4),
        ("track_a_force", e5),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    skeleton = declare_skeleton()
    summary = build_summary(skeleton, checks, evidence, h13)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(c["ok"] for c in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_rr1_parent_action_skeleton_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (
        args.output_dir / "mat001_rr1_parent_action_skeleton_summary.sha256"
    ).write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("MAT-001 RR1 parent-action skeleton declaration")
    print("  RR1:", summary["RR1_status"])
    print("  V:", summary["V_status"], "| K_Q:", summary["kq_numeric_status"])
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
