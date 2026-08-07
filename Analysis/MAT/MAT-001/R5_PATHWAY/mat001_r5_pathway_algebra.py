#!/usr/bin/env python3
"""R5 pathway algebra: distinguish candidate mechanisms from matching closure.

Tests two bounded parent-action ideas without promoting MAT-001:
(1) a shift-symmetric finite-density density portal, and
(2) a conformal-compensator/dilaton normalization toy.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp

PASS_STATUS = "PASS_MAT001_R5_PATHWAY_ALGEBRA_RESEARCH_ONLY"
FAIL_STATUS = "FAIL_MAT001_R5_PATHWAY_ALGEBRA"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument("--self-test-mutations", action="store_true")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_summary() -> dict[str, Any]:
    lam, eta, x0, f = sp.symbols("lambda eta X_0 f", positive=True, finite=True)
    rho, pi_dot, pi, shift = sp.symbols("rho pi_dot pi shift", real=True, finite=True)
    n = sp.symbols("n", nonnegative=True, finite=True)
    x = x0 - pi_dot
    lagrangian = n * x - lam * n**3 / 3 - eta * n * rho
    n_branch = sp.sqrt((x - eta * rho) / lam)
    p_eff = sp.simplify(lagrangian.subs(n, n_branch))
    expected = 2 * (x - eta * rho) ** sp.Rational(3, 2) / (3 * sp.sqrt(lam))

    direct_static_phase_source = sp.simplify(sp.diff(p_eff, pi))
    phase_shift_residual = sp.simplify(p_eff.subs(pi, pi + shift) - p_eff)
    density_source = sp.simplify(sp.diff(p_eff, rho).subs({rho: 0, pi_dot: 0}))
    rho_pi_dot_vertex = sp.simplify(
        sp.diff(p_eff, rho, pi_dot).subs({rho: 0, pi_dot: 0})
    )

    kq_psi = f**2
    cm_psi = sp.Integer(1)
    v_psi = sp.simplify(cm_psi / sp.sqrt(kq_psi))
    kq_sigma = sp.Integer(1)
    cm_sigma = 1 / f
    v_sigma = sp.simplify(cm_sigma / sp.sqrt(kq_sigma))

    checks = [
        {
            "name": "density_auxiliary_stationary",
            "ok": sp.simplify(sp.diff(lagrangian, n).subs(n, n_branch)) == 0,
        },
        {
            "name": "density_portal_effective_pressure",
            "ok": sp.simplify(p_eff - expected) == 0,
        },
        {"name": "phase_shift_invariance", "ok": phase_shift_residual == 0},
        {
            "name": "shift_symmetry_forbids_direct_static_pi_rho_source",
            "ok": direct_static_phase_source == 0,
        },
        {
            "name": "density_portal_generates_derivative_rho_pi_dot_vertex",
            "ok": rho_pi_dot_vertex != 0,
        },
        {
            "name": "dilaton_chart_residue_invariant",
            "ok": sp.simplify(v_psi - v_sigma) == 0,
        },
        {
            "name": "dilaton_candidate_residue_is_one_over_f",
            "ok": sp.simplify(v_psi - 1 / f) == 0,
        },
    ]

    return {
        "status": PASS_STATUS if all(row["ok"] for row in checks) else FAIL_STATUS,
        "scope": "RESEARCH_CANDIDATE_ALGEBRA_ONLY",
        "density_portal": {
            "parent_lagrangian": "n*X - lambda*n^3/3 - eta*n*rho_b",
            "positive_branch_n": str(n_branch),
            "effective_pressure": str(p_eff),
            "linear_density_source_at_background": str(density_source),
            "phase_shift_residual": str(phase_shift_residual),
            "direct_static_pi_rho_source": str(direct_static_phase_source),
            "rho_pi_dot_vertex": str(rho_pi_dot_vertex),
            "decision": "REJECT_AS_STANDALONE_STATIC_FORCE_MATCHING_ROUTE",
            "reason": "A U(1)-preserving density portal depends on the phase through derivatives. It can generate a rho_b*pi_dot vertex but no direct static rho_b*pi source.",
        },
        "dilaton_compensator": {
            "sigma_chart": {
                "K_Q": str(kq_sigma),
                "C_m": str(cm_sigma),
                "V": str(v_sigma),
            },
            "psi_equals_sigma_over_f_chart": {
                "K_Q": str(kq_psi),
                "C_m": str(cm_psi),
                "V": str(v_psi),
            },
            "decision": "ADVANCE_TO_BOUNDED_PARENT_ACTION_FORK",
            "unresolved": [
                "finite-density phonon-dilaton mode count and kinetic mixing",
                "signed residue of the physical eigenmode after constraint reduction",
                "ghost, gradient and strong-coupling domains",
                "screening, post-Newtonian and lensing constraints",
            ],
        },
        "recommended_route_order": [
            "Prove the minimal shift-symmetric portal static-source obstruction in the declared ITSM chart.",
            "Construct a scale-compensator plus finite-density parent action with one declared decay scale f.",
            "Reduce the full scalar constraint system and project the signed matter residue onto the physical mode.",
            "Reject the fork unless stability, cutoff and local-gravity constraints close in the same parameter domain.",
        ],
        "external_primary_anchors": [
            {
                "doi": "10.1103/PhysRevD.92.103510",
                "role": "superfluid dark matter parent proposal; matter coupling introduced phenomenologically",
            },
            {
                "doi": "10.1088/1475-7516/2018/09/021",
                "role": "relativistic completion discussion; unusual soft U(1)-breaking baryon coupling remains an assumption",
            },
            {
                "doi": "10.1007/JHEP09(2022)066",
                "role": "radial-mode integration and relativistic superfluid EFT matching methodology",
            },
            {
                "doi": "10.48550/arXiv.2108.07275",
                "role": "microscopic impurity/probe coupling matching methodology",
            },
            {
                "doi": "10.1103/PhysRevD.102.076011",
                "role": "finite-density phonon-dilaton mixing and Ward-identity constraints",
            },
            {
                "doi": "10.1007/JHEP10(2020)044",
                "role": "conformal-compensator matter coupling through a dilaton scale",
            },
        ],
        "claim_firewall": {
            "closes_R5": False,
            "computes_numeric_V": False,
            "derives_ITSM_K_Q": False,
            "validates_dilaton_parent": False,
            "changes_mode_count": False,
            "claims_MAT_pass": False,
            "reopens_stage4A": False,
        },
        "global_status": {
            "MAT-001": "BLOCKED",
            "V": "NOT_COMPUTED",
            "K_Q": "NOT_DERIVED",
            "Stage4A": "CLOSED",
        },
        "checks": checks,
    }


def validate(summary: dict[str, Any]) -> bool:
    firewall = summary["claim_firewall"]
    return bool(
        summary["status"] == PASS_STATUS
        and summary["scope"] == "RESEARCH_CANDIDATE_ALGEBRA_ONLY"
        and summary["density_portal"]["direct_static_pi_rho_source"] == "0"
        and summary["density_portal"]["decision"]
        == "REJECT_AS_STANDALONE_STATIC_FORCE_MATCHING_ROUTE"
        and summary["dilaton_compensator"]["decision"]
        == "ADVANCE_TO_BOUNDED_PARENT_ACTION_FORK"
        and all(value is False for value in firewall.values())
        and summary["global_status"]
        == {
            "MAT-001": "BLOCKED",
            "V": "NOT_COMPUTED",
            "K_Q": "NOT_DERIVED",
            "Stage4A": "CLOSED",
        }
        and all(row["ok"] for row in summary["checks"])
    )


def mutation_suite(summary: dict[str, Any]) -> None:
    require(validate(summary), "baseline validation")
    mutants: list[dict[str, Any]] = []
    static_source = copy.deepcopy(summary)
    static_source["density_portal"]["direct_static_pi_rho_source"] = "g"
    mutants.append(static_source)
    premature_close = copy.deepcopy(summary)
    premature_close["claim_firewall"]["closes_R5"] = True
    mutants.append(premature_close)
    numeric_v = copy.deepcopy(summary)
    numeric_v["global_status"]["V"] = "COMPUTED"
    mutants.append(numeric_v)
    dilaton_pass = copy.deepcopy(summary)
    dilaton_pass["claim_firewall"]["validates_dilaton_parent"] = True
    mutants.append(dilaton_pass)
    for index, mutant in enumerate(mutants, start=1):
        require(not validate(mutant), f"mutation {index} must fail closed")


def main() -> None:
    args = parse_args()
    summary = build_summary()
    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return
    require(validate(summary), "summary validation")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_r5_pathway_algebra_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "mat001_r5_pathway_algebra_summary.sha256").write_text(
        f"{digest}  {output.name}\n", encoding="utf-8"
    )
    print("MAT-001 R5 pathway algebra")
    print("  density portal:", summary["density_portal"]["decision"])
    print("  dilaton route:", summary["dilaton_compensator"]["decision"])
    print("STATUS:", summary["status"])
    print("JSON_SHA256:", digest)


if __name__ == "__main__":
    main()
