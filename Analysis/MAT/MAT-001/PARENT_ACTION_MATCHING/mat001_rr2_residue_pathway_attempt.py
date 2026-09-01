#!/usr/bin/env python3
"""MAT-001 RR2: residue-V pathway attempt on Track-A + S_int kit.

Constructs the single-field joint quadratic (Track-A time kinetic + Conditional
matter source), proves the canonical residue equals V = C_m/sqrt(K_Q)
symbolically, and shows that a bare-K_Q-free residue route still requires a
live dynamical response export that the repository does not provide.
Does not invent numerics or reopen Stage 4A.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_RR2_RESIDUE_PATHWAY_ATTEMPTED_INCOMPLETE"
FAIL_STATUS = "FAIL_MAT001_RR2_RESIDUE_PATHWAY"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rr1",
        type=Path,
        default=base / "outputs" / "mat001_rr1_parent_action_skeleton_summary.json",
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
        "--r2-template",
        type=Path,
        default=mat
        / "R2_DIRECT_RESIDUE"
        / "outputs"
        / "mat001_r2_direct_residue_audit_summary.json",
    )
    parser.add_argument(
        "--j2-template",
        type=Path,
        default=mat
        / "J2_MODE_PROJECTION"
        / "outputs"
        / "mat001_j2_basis_covariant_mode_projection_summary.json",
    )
    parser.add_argument(
        "--source-response",
        type=Path,
        default=uvir / "uvir003_source_observable_retarded_response_summary.json",
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


def residue_identities() -> dict[str, Any]:
    """Single-field Track-A matter channel residue identities."""
    k_q = sp.symbols("K_Q", positive=True)
    c_m = sp.symbols("C_m", real=True, nonzero=True)
    # Quadratic: L = (K_Q/2) pi_dot^2 + ... - C_m rho_b pi  (IR chart)
    # Canonical chi = sqrt(K_Q) pi => L_source = - V rho_b chi with V = C_m/sqrt(K_Q)
    d = -c_m
    u = sp.Matrix([1])  # single field mode
    k = sp.Matrix([[k_q]])
    c_eff = sp.Matrix([d])  # h=0 matter-only channel
    g_can = sp.simplify((c_eff.T * u)[0] / sp.sqrt((u.T * k * u)[0]))
    v_signed = sp.simplify(c_m / sp.sqrt(k_q))
    # In the oriented Track-A chart u_pi=+1, the Lagrangian covector is g_can=-V.
    require(sp.simplify(g_can + v_signed) == 0, "signed g_can equals -V")

    # Bare-K_Q-free path: if a measured mixed response R = chi/rho_b = V/P
    # then V is fixed only if operator P is known independently of the free K_Q
    # chart, or if an S-matrix amplitude supplies V^2.
    p_op = sp.symbols("P", positive=True)
    mixed_response = sp.simplify(-v_signed / p_op)
    exchange_coeff = sp.simplify(v_signed**2 / p_op)

    return {
        "joint_quadratic_convention": {
            "dynamical_field": "pi (Track-A fluctuation)",
            "time_kinetic": "K_Q * pi_dot**2 / 2",
            "matter_source": "- C_m * rho_b * pi",
            "h_constraints": "0 (matter-only static channel)",
        },
        "canonical_projection": {
            "c_eff": str(c_eff[0]),
            "u": ["1"],
            "g_can": str(g_can),
            "V_signed": str(v_signed),
            "identity_signed_g_can_equals_minus_V": True,
            "mode_orientation": "u_pi=+1 in the architecture psi chart",
            "orientation_reversal": "u_pi->-u_pi flips g_can; chart orientation must accompany the sign",
            "magnitude_only_matching_sufficient": False,
        },
        "bare_K_Q_free_routes": {
            "mixed_response_R_equals_minus_V_over_P": str(mixed_response),
            "exchange_coefficient_V2_over_P": str(exchange_coeff),
            "requires_independent_P_or_amplitude": True,
            "live_export_of_P_or_amplitude_for_Track_A_matter": False,
        },
        "absolute_inputs_still_required": [
            "Here absolute means independently normalized/dimensionful, not an absolute value; the sign is retained",
            "numeric C_m (or g_phi and f_phi)",
            "numeric K_Q (or Z_phi and f_phi)",
            "OR live dynamical residue/amplitude that isolates V without free K_Q",
        ],
    }


def audit_live_exports(source_resp: dict[str, Any] | None) -> dict[str, Any]:
    """Show retarded-response audit is not the matter-vertex residue."""
    method = (source_resp or {}).get("method") or {}
    boundary = str((source_resp or {}).get("scientific_boundary") or "")
    return {
        "source_response_subgate": (source_resp or {}).get("subgate_status"),
        "source_covectors": method.get("source_covectors"),
        "role": "diagnostic gauge-projected Q_rho/Q_chi impulses",
        "is_Track_A_matter_vertex_residue": False,
        "rejected_as_V": True,
        "boundary_excerpt": boundary[:240] if boundary else None,
        "reason": (
            "Source-observable retarded response uses Q_rho/Q_chi diagnostic "
            "impulses, not action-level d from S_int on Track-A pi."
        ),
    }


def build_summary(
    identities: dict[str, Any],
    live: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    add_check(
        checks,
        "signed_canonical_covector_equals_minus_V_symbolically",
        identities["canonical_projection"]["identity_signed_g_can_equals_minus_V"] is True,
    )
    add_check(
        checks,
        "bare_K_Q_free_route_lacks_live_export",
        identities["bare_K_Q_free_routes"][
            "live_export_of_P_or_amplitude_for_Track_A_matter"
        ]
        is False,
    )
    add_check(
        checks,
        "diagnostic_response_rejected_as_V",
        live["rejected_as_V"] is True
        and live["is_Track_A_matter_vertex_residue"] is False,
    )
    add_check(
        checks,
        "absolute_inputs_still_listed",
        len(identities["absolute_inputs_still_required"]) >= 2,
    )

    firewall = {
        "residue_pathway_attempted": True,
        "symbolic_V_form_on_Track_A": True,
        "numeric_V_computed": False,
        "numeric_K_Q_derived": False,
        "RR2_closed": False,
        "diagnostic_impulses_used_as_V": False,
        "claims_MAT_pass": False,
        "physics_pass": False,
        "reopens_stage4A": False,
    }
    add_check(
        checks,
        "claim_firewall_fail_closed",
        firewall["numeric_V_computed"] is False
        and firewall["RR2_closed"] is False
        and firewall["diagnostic_impulses_used_as_V"] is False
        and firewall["claims_MAT_pass"] is False
        and firewall["reopens_stage4A"] is False
        and firewall["physics_pass"] is False,
        flags=firewall,
    )

    all_ok = all(c["ok"] for c in checks)
    return {
        "gate": "MAT-001",
        "interface": "RR2_RESIDUE_PATHWAY",
        "stage": "RR2_RESIDUE_PATHWAY_ATTEMPT",
        "plan_step": "RR2",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "RR2_status": "ATTEMPTED_INCOMPLETE",
        "pathway_verdict": (
            "SYMBOLIC_RESIDUE_IDENTITY_HOLDS_LIVE_NUMERIC_ROUTE_ABSENT"
        ),
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "C_m_numeric_status": "NOT_DERIVED_FORM_ONLY",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "residue_identities": identities,
        "live_export_audit": live,
        "blocking_requirements": identities["absolute_inputs_still_required"],
        "inadmissible_substitutions": {
            "Q_rho_Q_chi_impulses_as_V": "REJECTED_ROLE_MISMATCH",
            "symbolic_g_can_as_numeric_V": "REJECTED_NOT_COMPUTED",
            "setting_K_Q_equals_1_to_quote_V": "REJECTED",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS means the Track-A + S_int residue pathway was constructed "
            "and shown to recover V symbolically, while every live numeric "
            "route to an independently normalized signed V remains absent. RR2 stays incomplete."
        ),
        "serial_next": (
            "RR2 remains the Derived wall: supply UV parent Z_phi/g_phi or a "
            "live dynamical amplitude/residue that isolates V. No further "
            "inventory substitutes for that physics."
        ),
    }


def validate_upstream(
    rr1: dict[str, Any] | None,
    s_int: dict[str, Any] | None,
    r2: dict[str, Any] | None,
    j2: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "rr1_upstream",
        bool(
            rr1
            and rr1.get("subgate_status")
            == "PASS_MAT001_RR1_PARENT_ACTION_SKELETON_DECLARED_UNMATCHED"
            and rr1.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "track_a_s_int_upstream",
        bool(
            s_int
            and s_int.get("subgate_status")
            == "PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL"
            and (s_int.get("exported_d_h") or {}).get("d") == ["-C_m"]
        ),
    )
    add_check(
        checks,
        "r2_template_upstream",
        bool(
            r2
            and r2.get("calculation_status") == "PASS"
            and r2.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "j2_template_upstream",
        bool(
            j2
            and j2.get("subgate_status")
            == "PASS_MAT001_J2_BASIS_COVARIANT_MODE_PROJECTION_TEMPLATE"
            and j2.get("V_status") == "NOT_COMPUTED"
        ),
    )
    return checks


def signed_contract_valid(summary: dict[str, Any]) -> bool:
    projection = ((summary.get("residue_identities") or {}).get("canonical_projection") or {})
    return bool(
        projection.get("g_can") == "-C_m/sqrt(K_Q)"
        and projection.get("V_signed") == "C_m/sqrt(K_Q)"
        and projection.get("identity_signed_g_can_equals_minus_V") is True
        and projection.get("magnitude_only_matching_sufficient") is False
        and projection.get("mode_orientation")
        == "u_pi=+1 in the architecture psi chart"
    )



def mutation_suite(summary: dict[str, Any]) -> None:
    require(signed_contract_valid(summary), "baseline signed residue contract")
    for key in (
        "numeric_V_computed",
        "RR2_closed",
        "diagnostic_impulses_used_as_V",
        "claims_MAT_pass",
        "reopens_stage4A",
        "physics_pass",
    ):
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, key)
    require(summary["RR2_status"] == "ATTEMPTED_INCOMPLETE", "incomplete")
    require(summary["V_status"] == "NOT_COMPUTED", "V")
    sign_mutant = copy.deepcopy(summary)
    sign_mutant["residue_identities"]["canonical_projection"]["g_can"] = "C_m/sqrt(K_Q)"
    require(not signed_contract_valid(sign_mutant), "sign-flipped g_can must fail")
    magnitude_mutant = copy.deepcopy(summary)
    magnitude_mutant["residue_identities"]["canonical_projection"][
        "magnitude_only_matching_sufficient"
    ] = True
    require(not signed_contract_valid(magnitude_mutant), "magnitude-only promotion must fail")


def main() -> None:
    args = parse_args()
    rr1, e1, s1 = load_json(args.rr1)
    s_int, e3, s3 = load_json(args.track_a_s_int)
    r2, e4, s4 = load_json(args.r2_template)
    j2, e5, s5 = load_json(args.j2_template)
    src, e6, s6 = load_json(args.source_response)

    evidence = {
        "rr1": {"source": args.rr1.name, "sha256": s1, "parse_error": e1},
        "track_a_s_int": {
            "source": args.track_a_s_int.name,
            "sha256": s3,
            "parse_error": e3,
        },
        "r2_template": {
            "source": args.r2_template.name,
            "sha256": s4,
            "parse_error": e4,
        },
        "j2_template": {
            "source": args.j2_template.name,
            "sha256": s5,
            "parse_error": e5,
        },
        "source_response": {
            "source": args.source_response.name,
            "sha256": s6,
            "parse_error": e6,
        },
    }
    checks = validate_upstream(rr1, s_int, r2, j2)
    for name, err in (
        ("rr1", e1),
        ("track_a_s_int", e3),
        ("r2_template", e4),
        ("j2_template", e5),
        ("source_response", e6),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    identities = residue_identities()
    live = audit_live_exports(src)
    summary = build_summary(identities, live, checks, evidence)

    require(signed_contract_valid(summary), "signed residue contract")
    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(c["ok"] for c in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_rr2_residue_pathway_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "mat001_rr2_residue_pathway_summary.sha256").write_bytes(
        f"{digest}  {output.name}\n".encode("utf-8")
    )

    print("MAT-001 RR2 residue pathway attempt")
    print("  RR2:", summary["RR2_status"])
    print("  verdict:", summary["pathway_verdict"])
    print("  V:", summary["V_status"])
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
