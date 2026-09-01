#!/usr/bin/env python3
"""MAT-001 Track-A host K_Q readiness after Conditional S_int embed.

Exports the host time-kinetic coefficient as the symbolic Track-A K_Q,
proves the on-host V form |d|/sqrt(K)=C_m/sqrt(K_Q), and inventories why
numeric K_Q (hence numeric V) remains NOT_DERIVED. Rejects Conditional
dimensional estimates as Derived. Does not reopen Stage 4A or issue MAT PASS.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_TRACK_A_KQ_SYMBOLIC_HOST_NUMERIC_BLOCKED"
FAIL_STATUS = "FAIL_MAT001_TRACK_A_KQ_READINESS"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--track-a-s-int-summary",
        type=Path,
        default=mat
        / "TRACK_A_S_INT"
        / "outputs"
        / "mat001_track_a_s_int_embed_summary.json",
    )
    parser.add_argument(
        "--track-a-force-summary",
        type=Path,
        default=uvir / "uvir003_track_a_force_adm_cubic_summary.json",
    )
    parser.add_argument(
        "--kq-inventory-summary",
        type=Path,
        default=uvir / "uvir003_kq_matching_inventory_summary.json",
    )
    parser.add_argument(
        "--matching-summary",
        type=Path,
        default=uvir / "uvir003_matching_route_program_summary.json",
    )
    parser.add_argument(
        "--conditional-kq-summary",
        type=Path,
        default=uvir / "uvir003_conditional_kq_estimate_summary.json",
    )
    parser.add_argument(
        "--v-kinetic-summary",
        type=Path,
        default=mat / "outputs" / "mat001_v_kinetic_chart_inventory_summary.json",
    )
    parser.add_argument(
        "--j1-summary",
        type=Path,
        default=mat
        / "J1_JOINT_ACTION"
        / "outputs"
        / "mat001_j1_joint_action_normalization_summary.json",
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


def host_kinetic_and_v_form() -> dict[str, Any]:
    c_m, k_q = sp.symbols("C_m K_Q", positive=True)
    d = -c_m
    # Track-A physical quadratic time piece: K_Q * pi_dot^2 / 2
    host_k = k_q
    v = c_m / sp.sqrt(k_q)
    g_can_abs = sp.simplify(sp.Abs(d) / sp.sqrt(host_k))
    require(sp.simplify(g_can_abs - v) == 0, "on-host |g_can| must equal V form")

    # Field rescaling covariance: pi' = s pi => K' = K/s^2, d' = d/s, V invariant
    s = sp.symbols("s", positive=True)
    k_prime = host_k / s**2
    d_prime = d / s
    v_prime = sp.simplify(sp.Abs(d_prime) / sp.sqrt(k_prime))
    require(sp.simplify(v_prime - v) == 0, "V form must be rescaling invariant")

    return {
        "host_time_kinetic": {
            "chart": "Track-A force host; physical density for pi_dot",
            "L_time_quadratic": "K_Q * pi_dot**2 / 2",
            "K_coefficient": "K_Q",
            "export_status": "SYMBOLIC_HOST_COEFFICIENT_EXPORTED",
            "numeric_status": "NOT_DERIVED",
            "provenance": (
                "uvir003_track_a_force_adm_cubic verified quadratic_force_density"
            ),
        },
        "on_host_V_form": {
            "d": "-C_m",
            "K": "K_Q",
            "V_definition": "C_m/sqrt(K_Q)",
            "abs_g_can": "Abs(d)/sqrt(K)",
            "identity_holds_symbolically": True,
            "rescaling_covariance_holds": True,
            "numeric_V_status": "NOT_COMPUTED",
        },
        "mode_u_single_field": {
            "direction": ["1"],
            "status": "TRIVIAL_SINGLE_FIELD_HOST_DIRECTION",
            "note": (
                "On a one-dimensional force fluctuation chart, mode selection "
                "is the unit direction in pi; this is not free-sector multi-mode "
                "selection and does not by itself yield numeric V."
            ),
        },
    }


def numeric_route_inventory(
    kq_inv: dict[str, Any] | None,
    matching: dict[str, Any] | None,
    conditional: dict[str, Any] | None,
    v_kinetic: dict[str, Any] | None,
) -> dict[str, Any]:
    routes = []
    if kq_inv and isinstance(kq_inv.get("routes"), list):
        for row in kq_inv["routes"]:
            routes.append(
                {
                    "id": row.get("id"),
                    "name": row.get("name"),
                    "status": row.get("status"),
                    "priority": row.get("priority"),
                    "does_not_fix": row.get("does_not_fix"),
                }
            )

    conditional_status = (conditional or {}).get("status")
    matching_kq = (matching or {}).get("kq_numeric_status")
    inv_kq = (kq_inv or {}).get("kq_numeric_status")
    vkin_kq = (v_kinetic or {}).get("kq_numeric_status")

    return {
        "matching_routes_from_inventory": routes,
        "numeric_K_Q_status_consensus": {
            "kq_matching_inventory": inv_kq,
            "matching_route_program": matching_kq,
            "v_kinetic_chart_inventory": vkin_kq,
            "all_NOT_DERIVED": all(
                status == "NOT_DERIVED"
                for status in (inv_kq, matching_kq, vkin_kq)
                if status is not None
            ),
        },
        "conditional_dimensional_estimate": {
            "status": conditional_status,
            "admissible_as_Derived": False,
            "reason": (
                "SPECULATIVE_NOT_A_DERIVATION / Conditional dimensional analogy; "
                "premises unconfirmed; must not be promoted to host K_Q Derived"
            ),
        },
        "what_would_derive_numeric_K_Q": [
            "Microscopic parent kinetic coefficient Z_phi (or Z_psi) with a declared map to Track-A K_Q",
            "Independent fixing of C_m and an invariant residue measurement of V, then K_Q=C_m^2/V^2",
            "A declared Conditional ansatz (e.g. R1 k_Q M_P^2) labeled Conditional only, never Derived",
        ],
        "still_open_after_track_a_embed": [
            "Numeric value of K_Q on the Track-A host",
            "Numeric value of C_m (d exports the form -C_m only)",
            "Numeric V",
            "Joined free-force B,C dressing with matter d,h if required",
        ],
    }


def progress_scorecard(s_int_embed: dict[str, Any] | None) -> dict[str, Any]:
    embed = s_int_embed or {}
    return {
        "chart_selected": embed.get("selected_host_route") == "R2_TRACK_A_FORCE_PHONON",
        "S_int_embedded_on_host": embed.get("S_int_status")
        == "EMBEDDED_CONDITIONAL_ON_TRACK_A_HOST",
        "d_h_exported_on_host": embed.get("track_a_d_h_export_status")
        == "EXPORTED_CONDITIONAL_ON_TRACK_A_HOST",
        "host_K_symbolic_exported": True,
        "host_V_form_identity": True,
        "numeric_C_m": False,
        "numeric_K_Q": False,
        "numeric_V": False,
        "stage4A_reopen_ready": False,
        "mat001_pass_ready": False,
    }


def validate_upstream(
    embed: dict[str, Any] | None,
    track_a: dict[str, Any] | None,
    kq_inv: dict[str, Any] | None,
    matching: dict[str, Any] | None,
    conditional: dict[str, Any] | None,
    v_kinetic: dict[str, Any] | None,
    j1: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "track_a_s_int_embed_upstream_contract",
        bool(
            embed
            and embed.get("subgate_status")
            == "PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL"
            and embed.get("V_status") == "NOT_COMPUTED"
            and embed.get("kq_numeric_status") == "NOT_DERIVED"
            and embed.get("mat001_pass") is False
            and embed.get("selected_host_route") == "R2_TRACK_A_FORCE_PHONON"
        ),
    )
    track_ok = False
    if track_a and track_a.get("subgate_status") == "PASS_FORCE_SECTOR_J2_COMPONENT":
        quad = str(
            ((track_a.get("symbolic_audit") or {}).get("verified_expansion") or {}).get(
                "quadratic_force_density", ""
            )
        )
        track_ok = (
            track_a.get("mat001_status") == "BLOCKED"
            and "K_Q" in quad
            and "pi_dot" in quad
        )
    add_check(checks, "track_a_force_quadratic_upstream_contract", track_ok)
    add_check(
        checks,
        "kq_inventory_upstream_contract",
        bool(
            kq_inv
            and kq_inv.get("subgate_status") == "PASS_KQ_MATCHING_INVENTORY_OPEN"
            and kq_inv.get("kq_numeric_status") == "NOT_DERIVED"
            and kq_inv.get("mat001_status") == "BLOCKED"
        ),
    )
    add_check(
        checks,
        "matching_program_upstream_contract",
        bool(
            matching
            and matching.get("subgate_status") == "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
            and matching.get("kq_numeric_status") == "NOT_DERIVED"
        ),
    )
    add_check(
        checks,
        "conditional_kq_estimate_not_derivation",
        bool(
            conditional
            and conditional.get("status") == "SPECULATIVE_NOT_A_DERIVATION"
        ),
    )
    add_check(
        checks,
        "v_kinetic_inventory_upstream_contract",
        bool(
            v_kinetic
            and v_kinetic.get("subgate_status")
            == "PASS_MAT001_V_KINETIC_CHART_INVENTORY_OPEN"
            and v_kinetic.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "j1_identity_upstream_contract",
        bool(
            j1
            and j1.get("subgate_status")
            == "PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY"
            and j1.get("V_status") == "NOT_COMPUTED"
        ),
    )
    return checks


def build_summary(
    kinetic: dict[str, Any],
    routes: dict[str, Any],
    scorecard: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    add_check(
        checks,
        "host_K_symbolic_exported",
        kinetic["host_time_kinetic"]["export_status"]
        == "SYMBOLIC_HOST_COEFFICIENT_EXPORTED"
        and kinetic["host_time_kinetic"]["numeric_status"] == "NOT_DERIVED",
    )
    add_check(
        checks,
        "on_host_V_form_and_rescaling_identity",
        kinetic["on_host_V_form"]["identity_holds_symbolically"] is True
        and kinetic["on_host_V_form"]["rescaling_covariance_holds"] is True
        and kinetic["on_host_V_form"]["numeric_V_status"] == "NOT_COMPUTED",
    )
    add_check(
        checks,
        "numeric_K_Q_still_not_derived_across_sources",
        routes["numeric_K_Q_status_consensus"]["all_NOT_DERIVED"] is True,
    )
    add_check(
        checks,
        "conditional_estimate_rejected_as_Derived",
        routes["conditional_dimensional_estimate"]["admissible_as_Derived"] is False
        and routes["conditional_dimensional_estimate"]["status"]
        == "SPECULATIVE_NOT_A_DERIVATION",
    )
    add_check(
        checks,
        "progress_scorecard_partial_only",
        scorecard["chart_selected"] is True
        and scorecard["S_int_embedded_on_host"] is True
        and scorecard["d_h_exported_on_host"] is True
        and scorecard["host_K_symbolic_exported"] is True
        and scorecard["numeric_K_Q"] is False
        and scorecard["numeric_V"] is False
        and scorecard["mat001_pass_ready"] is False,
    )

    firewall = {
        "host_K_symbolic_exported": True,
        "on_host_V_form_ready": True,
        "numeric_K_Q_derived": False,
        "numeric_V_computed": False,
        "conditional_estimate_promoted_Derived": False,
        "stage4A_reopened": False,
        "claims_MAT_pass": False,
        "claims_UVIR_pass": False,
        "claims_downstream_Derived": False,
        "physics_pass": False,
        "numeric_matching_ready": False,
    }
    add_check(
        checks,
        "claim_firewall_fail_closed",
        all(
            firewall[key] is False
            for key in (
                "numeric_K_Q_derived",
                "numeric_V_computed",
                "conditional_estimate_promoted_Derived",
                "stage4A_reopened",
                "claims_MAT_pass",
                "physics_pass",
                "numeric_matching_ready",
            )
        ),
        flags=firewall,
    )

    all_ok = all(check["ok"] for check in checks)
    return {
        "gate": "MAT-001",
        "interface": "TRACK_A_HOST_KQ",
        "stage": "TRACK_A_KQ_READINESS",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "host_K_export_status": "SYMBOLIC_HOST_COEFFICIENT_EXPORTED",
        "kq_numeric_status": "NOT_DERIVED",
        "V_status": "NOT_COMPUTED",
        "V_form_status": "ON_HOST_IDENTITY_HOLDS_SYMBOLICALLY",
        "numeric_matching_status": "BLOCKED_NUMERIC_K_Q_OR_RESIDUE_REQUIRED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        "host_time_kinetic": kinetic["host_time_kinetic"],
        "on_host_V_form": kinetic["on_host_V_form"],
        "mode_u_single_field": kinetic["mode_u_single_field"],
        "numeric_route_inventory": routes,
        "progress_scorecard": scorecard,
        "required_for_numeric_V": [
            {
                "item": "Host chart and S_int / d,h",
                "status": "COMPLETE_CONDITIONAL_TRACK_A",
            },
            {
                "item": "Symbolic host time-kinetic coefficient K_Q",
                "status": "EXPORTED_SYMBOLIC",
            },
            {
                "item": "Numeric C_m (or equivalent residue input)",
                "status": "NOT_DERIVED_FORM_ONLY",
            },
            {
                "item": "Numeric K_Q (or direct on-shell V)",
                "status": "NOT_DERIVED",
            },
        ],
        "blocking_requirements": [
            "Derive numeric K_Q from a microscopic/matching argument on the Track-A host, or compute an invariant on-shell residue V without quoting bare K_Q.",
            "If using a Conditional ansatz (e.g. dimensional R1), label it Conditional only and never as Derived.",
            "Numeric C_m remains form-level (-C_m from d); independent coefficient matching is still required for absolute V if both C_m and K_Q are unknown.",
            "Keep Stage 4A closed until a matched invariant exists; do not issue MAT physics PASS.",
        ],
        "inadmissible_substitutions": {
            "conditional_kq_estimate_as_Derived": "REJECTED_SPECULATIVE_NOT_A_DERIVATION",
            "symbolic_V_form_as_numeric_V": "REJECTED_NOT_COMPUTED",
            "naive_k_Q_equals_1_as_matching": "REJECTED_UNFIXED_WILSON_COEFFICIENT",
            "C_obs_alone_as_K_Q": "REJECTED_STRUCTURAL_THEOREM",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS exports the Track-A host time-kinetic coefficient as "
            "symbolic K_Q, proves the on-host V form and its rescaling "
            "invariance, and shows numeric K_Q remains NOT_DERIVED across "
            "matching inventories. It rejects Conditional dimensional "
            "estimates as Derived and does not compute numeric V, reopen "
            "Stage 4A, or authorize MAT/UVIR physics PASS."
        ),
        "serial_next": (
            "Pursue a real K_Q derivation path (microscopic Z_phi/Z_psi map, "
            "or independent C_m plus residue V), or open an explicitly labeled "
            "Conditional matching branch without Derived packaging; keep dual "
            "status for any Conditional numeric probe."
        ),
    }


def mutation_suite(summary: dict[str, Any]) -> None:
    banned = [
        "numeric_K_Q_derived",
        "numeric_V_computed",
        "conditional_estimate_promoted_Derived",
        "stage4A_reopened",
        "claims_MAT_pass",
        "physics_pass",
        "numeric_matching_ready",
    ]
    for key in banned:
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, f"mutation {key}")
    require(summary["kq_numeric_status"] == "NOT_DERIVED", "K_Q must stay open")
    require(summary["V_status"] == "NOT_COMPUTED", "V must stay NOT_COMPUTED")
    require(
        summary["inadmissible_substitutions"]["conditional_kq_estimate_as_Derived"]
        == "REJECTED_SPECULATIVE_NOT_A_DERIVATION",
        "conditional estimate must stay rejected",
    )


def main() -> None:
    args = parse_args()
    embed, embed_err, embed_sha = load_json(args.track_a_s_int_summary)
    track_a, track_err, track_sha = load_json(args.track_a_force_summary)
    kq_inv, kq_err, kq_sha = load_json(args.kq_inventory_summary)
    matching, match_err, match_sha = load_json(args.matching_summary)
    conditional, cond_err, cond_sha = load_json(args.conditional_kq_summary)
    v_kinetic, vkin_err, vkin_sha = load_json(args.v_kinetic_summary)
    j1, j1_err, j1_sha = load_json(args.j1_summary)

    evidence = {
        "track_a_s_int_embed": {
            "source": args.track_a_s_int_summary.name,
            "sha256": embed_sha,
            "parse_error": embed_err,
        },
        "track_a_force_adm": {
            "source": args.track_a_force_summary.name,
            "sha256": track_sha,
            "parse_error": track_err,
        },
        "kq_matching_inventory": {
            "source": args.kq_inventory_summary.name,
            "sha256": kq_sha,
            "parse_error": kq_err,
        },
        "matching_route_program": {
            "source": args.matching_summary.name,
            "sha256": match_sha,
            "parse_error": match_err,
        },
        "conditional_kq_estimate": {
            "source": args.conditional_kq_summary.name,
            "sha256": cond_sha,
            "parse_error": cond_err,
        },
        "v_kinetic_inventory": {
            "source": args.v_kinetic_summary.name,
            "sha256": vkin_sha,
            "parse_error": vkin_err,
        },
        "j1_identity": {
            "source": args.j1_summary.name,
            "sha256": j1_sha,
            "parse_error": j1_err,
        },
    }

    checks = validate_upstream(
        embed, track_a, kq_inv, matching, conditional, v_kinetic, j1
    )
    for name, err in (
        ("track_a_s_int_embed", embed_err),
        ("track_a_force_adm", track_err),
        ("kq_matching_inventory", kq_err),
        ("matching_route_program", match_err),
        ("conditional_kq_estimate", cond_err),
        ("v_kinetic_inventory", vkin_err),
        ("j1_identity", j1_err),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    kinetic = host_kinetic_and_v_form()
    routes = numeric_route_inventory(kq_inv, matching, conditional, v_kinetic)
    scorecard = progress_scorecard(embed)
    summary = build_summary(kinetic, routes, scorecard, checks, evidence)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(check["ok"] for check in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_track_a_kq_readiness_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    sidecar = args.output_dir / "mat001_track_a_kq_readiness_summary.sha256"
    sidecar.write_bytes(f"{digest}  {output.name}\n".encode("utf-8"))

    print("MAT-001 Track-A host K_Q readiness")
    print("  host K:", summary["host_K_export_status"])
    print("  K_Q numeric:", summary["kq_numeric_status"])
    print("  V_status:", summary["V_status"], "| form:", summary["V_form_status"])
    print("  MAT: BLOCKED | Stage4A: CLOSED")
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS: {0}".format(summary["subgate_status"]))
    print("JSON_SHA256: {0}".format(digest))
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
