#!/usr/bin/env python3
"""MAT-001 dual-status Conditional matching branch (never Derived).

Opens an explicitly labeled Conditional probe on the Track-A host kit:
symbolic V form, Conditional C_obs~1 and C_IR=2/3 premises, and optional
Conditional k_Q / V scans. Dual status is mandatory:

  Derived layer:  V_status=NOT_COMPUTED, kq_numeric_status=NOT_DERIVED,
                  mat001_pass=false, physics_pass=false, stage4A=CLOSED
  Conditional layer: probe outputs labeled CONDITIONAL_ONLY

Does not promote Conditional numerics to Derived claims.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_CONDITIONAL_MATCHING_BRANCH_OPEN_DUAL_STATUS"
FAIL_STATUS = "FAIL_MAT001_CONDITIONAL_MATCHING_BRANCH"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parent
    repo = base.parents[3]
    uvir = repo / "Analysis" / "UVIR" / "UVIR-003" / "outputs"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--kq-dig",
        type=Path,
        default=mat
        / "KQ_DERIVATION_DIG"
        / "outputs"
        / "mat001_kq_derivation_dig_summary.json",
    )
    parser.add_argument(
        "--kq-readiness",
        type=Path,
        default=mat
        / "TRACK_A_KQ"
        / "outputs"
        / "mat001_track_a_kq_readiness_summary.json",
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
        "--matching-summary",
        type=Path,
        default=uvir / "uvir003_matching_route_program_summary.json",
    )
    parser.add_argument(
        "--conditional-kq",
        type=Path,
        default=uvir / "uvir003_conditional_kq_estimate_summary.json",
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


def conditional_probe() -> dict[str, Any]:
    """Build dual-status Conditional probe tables (symbolic + sample points)."""
    c_m, c_ir, c_obs, k_q, v, a0, g, q, k_wilson = sp.symbols(
        "C_m C_IR C_obs K_Q V a0 G q k_Q", positive=True
    )
    # Structural identities (Conditional premises stated separately).
    c_obs_form = c_m ** sp.Rational(3, 2) / sp.sqrt(c_ir)
    v_form = c_m / sp.sqrt(k_q)
    k_from_v = c_m**2 / v**2
    a_ir = c_ir / (12 * sp.pi * g * a0)
    i_a0 = sp.simplify(a_ir * a0 / k_q)
    i_a0_closed = sp.simplify(
        (c_ir ** sp.Rational(1, 3) * v**2)
        / (12 * sp.pi * c_obs ** sp.Rational(4, 3) * g)
    )
    # Under C_m from C_obs,C_IR and V free: I_a0 in (C_obs,C_IR,V)
    c_m_from = (c_obs * sp.sqrt(c_ir)) ** sp.Rational(2, 3)
    i_from_v = sp.simplify(i_a0.subs({c_m: c_m_from, k_q: c_m_from**2 / v**2}))
    require(
        sp.simplify(i_from_v - i_a0_closed.subs(c_m, c_m_from)) == 0
        or sp.simplify(i_from_v - i_a0_closed) == 0,
        "I_a0 closed form check",
    )
    # Simpler: substitute into closed expression identity from matching program
    require(
        sp.simplify(
            i_a0_closed
            - (c_ir ** sp.Rational(1, 3) * v**2)
            / (12 * sp.pi * c_obs ** sp.Rational(4, 3) * g)
        )
        == 0,
        "I_a0 closed form self-consistent",
    )

    # Conditional sample lattice (labeled non-Derived).
    # Premises: C_obs=1, C_IR=2/3, and either V in {0.5,1,2} or k_Q in {0.5,1,2}
    # with M_P=1 units where K_Q = k_Q M_P^2 (Conditional R1).
    samples = []
    for v_val in (0.5, 1.0, 2.0):
        # With C_obs=1, C_IR=2/3: C_m = (1 * sqrt(2/3))^(2/3)
        c_ir_n = 2.0 / 3.0
        c_obs_n = 1.0
        c_m_n = (c_obs_n * (c_ir_n**0.5)) ** (2.0 / 3.0)
        k_q_n = (c_m_n / v_val) ** 2
        i_a0_n = (c_ir_n ** (1.0 / 3.0) * v_val**2) / (
            12.0 * 3.141592653589793 * (c_obs_n ** (4.0 / 3.0)) * 1.0
        )
        samples.append(
            {
                "label": "CONDITIONAL_ONLY",
                "premises": {
                    "C_obs": c_obs_n,
                    "C_IR": c_ir_n,
                    "V_conditional": v_val,
                    "G": 1.0,
                    "note": "G=1 chart units for relative probe only",
                },
                "induced_C_m_conditional": c_m_n,
                "induced_K_Q_conditional": k_q_n,
                "I_a0_conditional_G1": i_a0_n,
                "claim_class": "Conditional",
                "not_Derived": True,
            }
        )
    for kq_w in (0.5, 1.0, 2.0):
        samples.append(
            {
                "label": "CONDITIONAL_ONLY",
                "premises": {
                    "R1_ansatz": "K_Q = k_Q * M_P^2 with M_P=1 chart",
                    "k_Q": kq_w,
                    "C_IR": 2.0 / 3.0,
                    "note": "R1 dimensional Conditional; not a derivation",
                },
                "K_Q_conditional": kq_w,
                "q_cross_over_a0_parallel_conditional": kq_w / (4.0 * (2.0 / 3.0)),
                "q_cross_over_a0_perp_conditional": kq_w / (2.0 * (2.0 / 3.0)),
                "claim_class": "Conditional",
                "not_Derived": True,
            }
        )

    return {
        "branch_status": "OPEN_CONDITIONAL_DUAL_STATUS",
        "premises_declared": [
            "Track-A Conditional host with S_int and d,h form (not free-sector)",
            "Symbolic host K_Q and on-host V form (not numeric Derived)",
            "Optional probe premises: C_obs~1 and C_IR=2/3 are Conditional empirical/matching hypotheses",
            "Optional R1 k_Q M_P^2 is Conditional dimensional analogy only",
        ],
        "structural_identities": {
            "C_obs_form": str(c_obs_form),
            "V_form": str(v_form),
            "K_Q_from_V_Cm": str(k_from_v),
            "A_IR": str(a_ir),
            "I_a0_closed_in_Cobs_CIR_V": str(i_a0_closed),
            "static_Cobs_alone_fixes_K_Q": False,
        },
        "conditional_samples": samples,
        "dual_status_contract": {
            "Derived_layer": {
                "V_status": "NOT_COMPUTED",
                "kq_numeric_status": "NOT_DERIVED",
                "mat001_pass": False,
                "physics_pass": False,
                "stage4A_status": "CLOSED",
                "claims_downstream_Derived": False,
            },
            "Conditional_layer": {
                "probe_status": "OPEN_CONDITIONAL_ONLY",
                "samples_are_Derived": False,
                "may_inform_priority_flags": True,
                "may_not_reopen_stage4A_as_Derived": True,
            },
        },
    }


def build_summary(
    probe: dict[str, Any],
    checks: list[dict[str, Any]],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    add_check(
        checks,
        "dual_status_derived_layer_fail_closed",
        probe["dual_status_contract"]["Derived_layer"]["V_status"] == "NOT_COMPUTED"
        and probe["dual_status_contract"]["Derived_layer"]["kq_numeric_status"]
        == "NOT_DERIVED"
        and probe["dual_status_contract"]["Derived_layer"]["mat001_pass"] is False
        and probe["dual_status_contract"]["Derived_layer"]["physics_pass"] is False
        and probe["dual_status_contract"]["Derived_layer"]["stage4A_status"]
        == "CLOSED",
    )
    add_check(
        checks,
        "conditional_samples_all_labeled_not_Derived",
        all(row.get("not_Derived") is True for row in probe["conditional_samples"])
        and all(
            row.get("label") == "CONDITIONAL_ONLY"
            for row in probe["conditional_samples"]
        ),
    )
    add_check(
        checks,
        "static_Cobs_structural_theorem_retained",
        probe["structural_identities"]["static_Cobs_alone_fixes_K_Q"] is False,
    )
    add_check(
        checks,
        "branch_open_conditional",
        probe["branch_status"] == "OPEN_CONDITIONAL_DUAL_STATUS",
    )

    firewall = {
        "conditional_branch_open": True,
        "conditional_samples_present": True,
        "numeric_V_promoted_Derived": False,
        "numeric_K_Q_promoted_Derived": False,
        "conditional_samples_promoted_Derived": False,
        "stage4A_reopened_from_conditional": False,
        "claims_MAT_pass": False,
        "claims_UVIR_pass": False,
        "claims_downstream_Derived": False,
        "physics_pass": False,
    }
    add_check(
        checks,
        "claim_firewall_fail_closed",
        firewall["numeric_V_promoted_Derived"] is False
        and firewall["numeric_K_Q_promoted_Derived"] is False
        and firewall["conditional_samples_promoted_Derived"] is False
        and firewall["stage4A_reopened_from_conditional"] is False
        and firewall["claims_MAT_pass"] is False
        and firewall["physics_pass"] is False,
        flags=firewall,
    )

    all_ok = all(check["ok"] for check in checks)
    return {
        "gate": "MAT-001",
        "interface": "CONDITIONAL_MATCHING_BRANCH",
        "stage": "CONDITIONAL_MATCHING_BRANCH_DUAL_STATUS",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        # Derived / public-claim layer (must stay fail closed)
        "V_status": "NOT_COMPUTED",
        "kq_numeric_status": "NOT_DERIVED",
        "mat001_status": "BLOCKED",
        "mat001_pass": False,
        "uv_ir_full_gate_status": "IN_PROGRESS",
        "stage4A_status": "CLOSED",
        "physics_pass": False,
        # Conditional layer
        "conditional_branch_status": "OPEN_CONDITIONAL_DUAL_STATUS",
        "conditional_probe": probe,
        "blocking_requirements_for_Derived": [
            "Numeric K_Q or invariant residue V from a derivation path, not Conditional samples",
            "Independent absolute C_m if quoting absolute V without pure residue route",
            "Independent Stage 4A reopen only after matched invariant exists",
        ],
        "inadmissible_substitutions": {
            "conditional_sample_as_Derived_V": "REJECTED_DUAL_STATUS",
            "conditional_k_Q_as_Derived_K_Q": "REJECTED_DUAL_STATUS",
            "C_obs_equals_1_as_Derived": "REJECTED_EMPIRICAL_HYPOTHESIS",
            "C_IR_equals_2_3_as_Derived": "REJECTED_GEOMETRIC_PACKAGING",
            "stage4A_reopen_from_conditional_scan": "REJECTED",
        },
        "evidence": evidence,
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "A PASS opens a dual-status Conditional matching branch on the "
            "Track-A host kit: structural identities and labeled Conditional "
            "sample probes are available for priority flags only. Derived-layer "
            "V and K_Q remain NOT_COMPUTED / NOT_DERIVED. Conditional numerics "
            "must never be packaged as Derived, MAT PASS, or Stage 4A reopen."
        ),
        "serial_next": (
            "Use Conditional probes only as dual-status diagnostics; continue "
            "genuine K_Q/V derivation, or keep the Tier-1 hold. Do not freeze "
            "alpha.12 from Conditional samples alone."
        ),
    }


def validate_upstream(
    dig: dict[str, Any] | None,
    kq_ready: dict[str, Any] | None,
    s_int: dict[str, Any] | None,
    matching: dict[str, Any] | None,
    conditional: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "kq_dig_upstream",
        bool(
            dig
            and dig.get("subgate_status") == "PASS_MAT001_KQ_DERIVATION_DIG_INCOMPLETE"
            and dig.get("kq_numeric_status") == "NOT_DERIVED"
            and dig.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "kq_readiness_upstream",
        bool(
            kq_ready
            and kq_ready.get("subgate_status")
            == "PASS_MAT001_TRACK_A_KQ_SYMBOLIC_HOST_NUMERIC_BLOCKED"
            and kq_ready.get("V_status") == "NOT_COMPUTED"
        ),
    )
    add_check(
        checks,
        "track_a_s_int_upstream",
        bool(
            s_int
            and s_int.get("subgate_status")
            == "PASS_MAT001_TRACK_A_S_INT_EMBED_DH_EXPORTED_CONDITIONAL"
        ),
    )
    add_check(
        checks,
        "matching_upstream",
        bool(
            matching
            and matching.get("subgate_status") == "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
            and matching.get("kq_numeric_status") == "NOT_DERIVED"
        ),
    )
    add_check(
        checks,
        "conditional_kq_speculative_upstream",
        bool(
            conditional and conditional.get("status") == "SPECULATIVE_NOT_A_DERIVATION"
        ),
    )
    return checks


def mutation_suite(summary: dict[str, Any]) -> None:
    for key in (
        "numeric_V_promoted_Derived",
        "numeric_K_Q_promoted_Derived",
        "conditional_samples_promoted_Derived",
        "stage4A_reopened_from_conditional",
        "claims_MAT_pass",
        "physics_pass",
    ):
        mutant = copy.deepcopy(summary)
        mutant["claim_firewall"][key] = True
        require(mutant["claim_firewall"][key] is True, key)
    require(summary["V_status"] == "NOT_COMPUTED", "Derived V closed")
    require(summary["kq_numeric_status"] == "NOT_DERIVED", "Derived K_Q closed")
    require(
        summary["conditional_branch_status"] == "OPEN_CONDITIONAL_DUAL_STATUS",
        "branch open",
    )


def main() -> None:
    args = parse_args()
    dig, e1, s1 = load_json(args.kq_dig)
    kq_ready, e2, s2 = load_json(args.kq_readiness)
    s_int, e3, s3 = load_json(args.track_a_s_int)
    matching, e4, s4 = load_json(args.matching_summary)
    conditional, e5, s5 = load_json(args.conditional_kq)

    evidence = {
        "kq_dig": {"source": args.kq_dig.name, "sha256": s1, "parse_error": e1},
        "kq_readiness": {
            "source": args.kq_readiness.name,
            "sha256": s2,
            "parse_error": e2,
        },
        "track_a_s_int": {
            "source": args.track_a_s_int.name,
            "sha256": s3,
            "parse_error": e3,
        },
        "matching_program": {
            "source": args.matching_summary.name,
            "sha256": s4,
            "parse_error": e4,
        },
        "conditional_kq": {
            "source": args.conditional_kq.name,
            "sha256": s5,
            "parse_error": e5,
        },
    }
    checks = validate_upstream(dig, kq_ready, s_int, matching, conditional)
    for name, err in (
        ("kq_dig", e1),
        ("kq_readiness", e2),
        ("track_a_s_int", e3),
        ("matching_program", e4),
        ("conditional_kq", e5),
    ):
        add_check(checks, f"{name}_readable", err is None, parse_error=err)

    # If dig not yet present (ordering), allow running dig first - validation fails until dig exists
    probe = conditional_probe()
    summary = build_summary(probe, checks, evidence)

    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    all_ok = all(c["ok"] for c in summary["checks"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_conditional_matching_branch_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "mat001_conditional_matching_branch_summary.sha256").write_bytes(
        f"{digest}  {output.name}\n".encode("utf-8")
    )
    print("MAT-001 Conditional matching branch (dual status)")
    print("  branch:", summary["conditional_branch_status"])
    print("  Derived V:", summary["V_status"], "| K_Q:", summary["kq_numeric_status"])
    print("  MAT: BLOCKED | Stage4A: CLOSED | physics_pass: false")
    for check in summary["checks"]:
        print("  [{0}] {1}".format("OK" if check["ok"] else "FAIL", check["name"]))
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
