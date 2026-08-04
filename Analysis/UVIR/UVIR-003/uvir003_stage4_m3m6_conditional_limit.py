#!/usr/bin/env python3
"""UVIR-003 Stage 4: M3/M6 upgrade OR permanent Conditional programme limit.

Serial Stage 4 (UVIR-003_SERIAL_STAGE_ORDER / Master Plan critical path):
  Goal: substitute matched V (and C_obs) into route maps → re-evaluate
  q_x, Lambda_||  — *or* accept permanent Conditional M3/M6 scope.

Exit criterion (either branch):
  A. Derived path: M3 not OPEN/PARTIAL once matched V + invariants applied
  B. Programme path: explicit permanent Conditional limit for M3/M6

This package executes branch B when Stage 3 leaves V NOT_COMPUTED
(K_Q NOT_DERIVED). It does NOT invent a numeric V, promote R1 naive, or
claim physical cutoff as Derived.

Does NOT:
  - compute V or K_Q
  - issue UVIR-003 full-gate PASS (Stage 5)
  - issue MAT-001 PASS
  - authorize downstream Derived use
  - promote (P,C_IR)=(1,2/3) to Derived

Exit:
  PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT
  stage_4_exit_status: PERMANENT_CONDITIONAL_M3_M6
  physics_pass: false
  full_gate_status: IN_PROGRESS
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    mat = base.parents[1] / "MAT" / "MAT-001" / "outputs"
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--floor-summary",
        type=Path,
        default=base / "outputs" / "uvir003_conditional_matching_floor_summary.json",
    )
    p.add_argument(
        "--stage2c-summary",
        type=Path,
        default=base / "outputs" / "uvir003_stage2c_floor_diagnostics_summary.json",
    )
    p.add_argument(
        "--mat-summary",
        type=Path,
        default=mat / "mat001_scoped_calculation_summary.json",
    )
    p.add_argument(
        "--matching-summary",
        type=Path,
        default=base / "outputs" / "uvir003_matching_route_program_summary.json",
    )
    p.add_argument(
        "--weak-coupling-domain",
        type=Path,
        default=base / "outputs" / "uvir003_declared_weak_coupling_domain_summary.json",
    )
    return p.parse_args()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def require(name: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(f"{name}" + (f": {detail}" if detail else ""))


def upgrade_identities_if_v_known() -> dict[str, Any]:
    """Structural maps that *would* apply under Derived V (branch A scaffold)."""
    C_obs, C_IR, V, G, a0, q, cos_th = sp.symbols(
        "C_obs C_IR V G a0 q cos_theta", positive=True
    )
    # Matching-route: I_a0 = C_IR^{1/3} V^2 / (12 pi G C_obs^{4/3})
    I_a0 = sp.simplify(
        C_IR ** sp.Rational(1, 3)
        * V**2
        / (12 * sp.pi * G * C_obs ** sp.Rational(4, 3))
    )
    # A = C_IR / (12 pi G a0); Aq/K_Q at q = A * q / K_Q
    # with K_Q from V and C_m: C_m = (C_obs * sqrt(C_IR))^{2/3}, K_Q = C_m^2 / V^2
    C_m = (C_obs * sp.sqrt(C_IR)) ** sp.Rational(2, 3)
    K_Q = sp.simplify(C_m**2 / V**2)
    A = C_IR / (12 * sp.pi * G * a0)
    Aq_over_KQ = sp.simplify(A * q / K_Q)
    # Causality ratio structure under R1/R3 floor uses free P; under R2:
    # P_eff related to K_Q chart — leave symbolic note only
    # NDA: Lambda_|| ~ K_Q^{3/4} / sqrt(A)
    Lam = sp.simplify(K_Q ** sp.Rational(3, 4) / sp.sqrt(A))
    return {
        "I_a0_from_Cobs_CIR_V": str(I_a0),
        "K_Q_from_Cobs_CIR_V": str(K_Q),
        "Aq_over_KQ": str(Aq_over_KQ),
        "Lambda_parallel_structural": str(Lam),
        "status": "SCAFFOLD_ONLY_REQUIRES_DERIVED_V",
        "note": (
            "Branch A upgrade maps. Not applied numerically because Stage 3 "
            "left V NOT_COMPUTED / K_Q NOT_DERIVED."
        ),
    }


def permanent_conditional_policy() -> dict[str, Any]:
    """Programme decision text for Stage 4 exit branch B."""
    return {
        "decision": "PERMANENT_CONDITIONAL_M3_M6_LIMIT",
        "authority": (
            "UVIR-003_SERIAL_STAGE_ORDER Stage 4 exit B; "
            "UVIR-003_FULL_GATE_CLOSURE_CHECKLIST programme decision; "
            "Master Plan §5 serial critical path"
        ),
        "rationale": [
            "Stage 3 scoped MAT left V=C_m/sqrt(K_Q) NOT_COMPUTED",
            "K_Q remains NOT_DERIVED (inventory + R3 incomplete)",
            "R2 cannot close Derived Aq/K_Q without V",
            "R3 residue audit Classification C — no Z_psi r_rho",
            "R1 naive (P,C_IR)=(1,2/3) forbidden as Derived packaging",
        ],
        "M3_policy": {
            "status": "PERMANENT_CONDITIONAL_WITH_SCOPE",
            "meaning": (
                "Causality domain documented under Stage 2b Conditional floor "
                "(free P, C_IR) and Stage 2c diagnostics. Referee-grade "
                "Conditional-with-scope — not Derived matched Aq/K_Q."
            ),
            "domain_basis": [
                "PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING",
                "PASS_CONDITIONAL_MATCHING_FLOOR",
                "PASS_STAGE2C_FLOOR_DIAGNOSTICS",
            ],
            "forbidden": [
                "Claim Derived causality close without matched Aq/K_Q",
                "Promote naive q_x/a0=0.375 parallel as Derived",
            ],
        },
        "M6_policy": {
            "status": "PERMANENT_CONDITIONAL_NDA_DIAGNOSTIC",
            "meaning": (
                "Physical cutoff remains Conditional NDA diagnostic under "
                "floor parameter P (Lambda_|| structure). Not a Derived "
                "matched strong-coupling scale."
            ),
            "domain_basis": [
                "PASS_DECLARED_UNITARITY_EFT_CRITERION (tree/NDA path)",
                "PASS_CONDITIONAL_MATCHING_FLOOR",
                "PASS_STAGE2C_FLOOR_DIAGNOSTICS",
            ],
            "forbidden": [
                "Claim physical cutoff as Derived without matched norm",
                "Optical theorem / S-matrix unitarity from this package",
            ],
        },
        "reopen_criteria_for_Derived_upgrade": [
            "Compute V from declared S_int once force kinetic / K_Q chart available",
            "Or derive Z_psi r_rho (R3) or independent k_Q (R1) as Derived",
            "Then re-run Stage 4 branch A: substitute into I_a0, q_x, Lambda_||",
        ],
        "does_not_authorize": [
            "UVIR-003 full_gate_status = PASS (Stage 5 programme decision)",
            "MAT-001 PASS",
            "Downstream Derived SCR/LEN/DISK/P3/P4 packaging",
            "SPARC / H0 validation",
        ],
    }


def main() -> None:
    args = parse_args()
    floor = load_json(args.floor_summary)
    s2c = load_json(args.stage2c_summary)
    mat = load_json(args.mat_summary)
    match = load_json(args.matching_summary)
    weak = load_json(args.weak_coupling_domain)

    checks: list[dict[str, Any]] = []

    floor_ok = (
        floor is not None
        and floor.get("subgate_status") == "PASS_CONDITIONAL_MATCHING_FLOOR"
        and floor.get("stage_2_exit", {}).get("status") == "CONDITIONAL_WITH_SCOPE"
    )
    checks.append(
        {
            "name": "stage_2b_floor_and_exit_present",
            "ok": floor_ok,
            "got": None if floor is None else floor.get("subgate_status"),
        }
    )

    s2c_ok = (
        s2c is not None
        and s2c.get("subgate_status") == "PASS_STAGE2C_FLOOR_DIAGNOSTICS"
    )
    checks.append(
        {
            "name": "stage_2c_diagnostics_present",
            "ok": s2c_ok,
            "got": None if s2c is None else s2c.get("subgate_status"),
        }
    )

    mat_ok = (
        mat is not None
        and mat.get("subgate_status") == "PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL"
        and mat.get("mat001_pass") is False
    )
    checks.append(
        {
            "name": "stage_3_mat_scoped_present_no_pass",
            "ok": mat_ok,
            "got": None if mat is None else mat.get("subgate_status"),
            "mat001_pass": None if mat is None else mat.get("mat001_pass"),
        }
    )

    match_ok = (
        match is not None
        and match.get("subgate_status") == "PASS_MATCHING_ROUTE_PROGRAM_OPEN"
    )
    checks.append(
        {
            "name": "matching_route_program_present",
            "ok": match_ok,
            "got": None if match is None else match.get("subgate_status"),
        }
    )

    weak_ok = (
        weak is not None
        and weak.get("subgate_status") == "PASS_DECLARED_WEAK_COUPLING_DOMAIN"
    )
    checks.append(
        {
            "name": "stage1_weak_coupling_domain_present",
            "ok": weak_ok,
            "got": None if weak is None else weak.get("subgate_status"),
        }
    )

    # V availability determines branch
    v_status = None if mat is None else mat.get("V_status")
    kq_status = None if mat is None else mat.get("kq_numeric_status")
    v_computed = v_status not in (None, "NOT_COMPUTED") and bool(
        mat.get("provisional_invariant_map", {}).get("V_computed_this_stage")
    )
    require(
        "honest_V_gate",
        (mat is None) or (v_status == "NOT_COMPUTED") or v_computed,
        f"unexpected V_status={v_status}",
    )

    if v_computed:
        branch = "A_DERIVED_V_UPGRADE"
        # Not reachable with current Stage 3 package; scaffold only.
        stage4_exit = {
            "status": "DERIVED_V_UPGRADE_PENDING_IMPLEMENTATION",
            "branch": branch,
            "allows_UVIR_full_PASS": False,
            "allows_MAT_PASS": False,
            "note": "V present but full upgrade calculator not implemented in this package",
        }
        decision = {
            "decision": "V_AVAILABLE_BUT_UPGRADE_NOT_AUTO",
            "note": "Re-run dedicated Derived upgrade once V path is complete",
        }
        m3_status = "PARTIAL_PENDING_V_SUBSTITUTION"
        m6_status = "OPEN_PENDING_V_SUBSTITUTION"
        branch_ok = False  # force explicit implementation before PASS
    else:
        branch = "B_PERMANENT_CONDITIONAL"
        decision = permanent_conditional_policy()
        stage4_exit = {
            "status": "PERMANENT_CONDITIONAL_M3_M6",
            "branch": branch,
            "M3": decision["M3_policy"]["status"],
            "M6": decision["M6_policy"]["status"],
            "M7": "OPEN_MAT_BLOCKED_FOR_PASS",
            "allows_stage5_programme_decision": True,
            "allows_UVIR_full_PASS": False,
            "allows_MAT_PASS": False,
            "allows_downstream_Derived": False,
            "reopen_to_branch_A_when": decision["reopen_criteria_for_Derived_upgrade"],
        }
        m3_status = decision["M3_policy"]["status"]
        m6_status = decision["M6_policy"]["status"]
        branch_ok = True

    checks.append(
        {
            "name": "branch_selected_honestly_from_V_status",
            "ok": (not v_computed and branch == "B_PERMANENT_CONDITIONAL")
            or (v_computed and branch == "A_DERIVED_V_UPGRADE"),
            "V_status": v_status,
            "kq_numeric_status": kq_status,
            "branch": branch,
        }
    )
    checks.append(
        {
            "name": "stage4_exit_permanent_conditional_when_V_missing",
            "ok": branch_ok
            and stage4_exit["status"] == "PERMANENT_CONDITIONAL_M3_M6"
            and stage4_exit["allows_UVIR_full_PASS"] is False
            and stage4_exit["allows_MAT_PASS"] is False,
            "exit": stage4_exit["status"],
        }
    )

    scaffold = upgrade_identities_if_v_known()
    checks.append(
        {
            "name": "branch_A_scaffold_present_not_applied_as_Derived",
            "ok": scaffold["status"] == "SCAFFOLD_ONLY_REQUIRES_DERIVED_V",
        }
    )

    # Naive still non-derived
    naive_ban = True
    if floor is not None:
        naive = floor.get("naive_comparison_only", {})
        naive_ban = naive.get("label") == "NON_DERIVED_COMPARISON_ONLY" or (
            floor.get("claim_firewall", {}).get("R1_naive_promoted_to_Derived") is False
        )
    checks.append(
        {
            "name": "naive_R1_not_promoted",
            "ok": naive_ban,
        }
    )

    firewall = {
        "Derived_K_Q": False,
        "Derived_V": False,
        "Derived_M3_close": False,
        "Derived_physical_cutoff_M6": False,
        "R1_naive_promoted_to_Derived": False,
        "MAT001_PASS": False,
        "UVIR003_full_PASS": False,
        "downstream_Derived_use_authorized": False,
        "observational_claim": False,
        "permanent_Conditional_M3_M6_recorded": True,
    }
    checks.append(
        {
            "name": "claim_firewall",
            "ok": all(
                (v is True) if k == "permanent_Conditional_M3_M6_recorded" else (v is False)
                for k, v in firewall.items()
            ),
            "flags": firewall,
        }
    )

    # Stage 5 still required for full gate
    checks.append(
        {
            "name": "stage5_still_required_for_full_gate",
            "ok": stage4_exit.get("allows_UVIR_full_PASS") is False
            and stage4_exit.get("allows_stage5_programme_decision") is True,
        }
    )

    all_ok = all(c["ok"] for c in checks) and branch_ok
    subgate = (
        "PASS_STAGE4_PERMANENT_CONDITIONAL_M3_M6_LIMIT"
        if all_ok
        else "FAIL_STAGE4_M3_M6"
    )

    master_plan_criteria = {
        "M1": "PASS_BOUNDED",
        "M2": "PASS_BOUNDED",
        "M3": m3_status,
        "M4": "PASS_SCOPED",
        "M5": "PASS_INVENTORY_K_Q_NOT_DERIVED",
        "M6": m6_status,
        "M7": "OPEN_MAT_BLOCKED_FOR_PASS",
        "interpretation": (
            "Stage 4 exit B freezes M3/M6 as permanent Conditional-with-scope "
            "(programme limit). This is not Derived close and not full-gate PASS. "
            "Stage 5 must decide whether Conditional M3/M6 + M1–M5 are sufficient "
            "for full_gate_status=PASS under declared policy."
        ),
    }

    summary: dict[str, Any] = {
        "gate": "UVIR-003",
        "stage": "B_STAGE4_M3_M6_LIMIT",
        "serial_stage": 4,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "claim_status": "Conditional_permanent_programme_limit",
        "physics_pass": False,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "kq_numeric_status": "NOT_DERIVED",
        "V_status": v_status if v_status is not None else "UNKNOWN",
        "branch": branch,
        "stage_4_exit": stage4_exit,
        "programme_decision": decision,
        "master_plan_criteria_after_stage4": master_plan_criteria,
        "branch_A_scaffold_if_V_later": scaffold,
        "prior_artifacts": {
            "stage_2b": None if floor is None else floor.get("subgate_status"),
            "stage_2c": None if s2c is None else s2c.get("subgate_status"),
            "stage_3_mat": None if mat is None else mat.get("subgate_status"),
            "matching_route": None if match is None else match.get("subgate_status"),
            "stage_1_domain": None if weak is None else weak.get("subgate_status"),
        },
        "checks": checks,
        "n_checks": len(checks),
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Stage 4 programme decision: permanent Conditional M3/M6 limit "
            "because matched V is not available. Documents referee-grade "
            "Conditional-with-scope for causality and NDA cutoff diagnostics. "
            "Does not derive K_Q/V, does not close UVIR full gate, does not "
            "issue MAT PASS, does not authorize downstream Derived use."
        ),
        "next_required": [
            "Stage 5: UVIR-003 full-gate programme decision under declared policy "
            "(Conditional M3/M6 accepted or not for PASS)",
            "Optional reopen: compute V and re-run Stage 4 branch A for Derived upgrade",
            "No MAT PASS or downstream Derived packaging before Stage 5",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "uvir003_stage4_m3m6_conditional_limit_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest()
    (
        args.output_dir / "uvir003_stage4_m3m6_conditional_limit_summary.sha256"
    ).write_bytes(f"{h}  {out.name}\n".encode("utf-8"))

    print("UVIR-003 Stage 4 M3/M6 permanent Conditional limit")
    print(f"  branch: {branch}")
    print(f"  stage_4_exit: {stage4_exit['status']}")
    print(f"  M3: {m3_status}")
    print(f"  M6: {m6_status}")
    print("  physics_pass: False | MAT: BLOCKED | UVIR: IN_PROGRESS")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
