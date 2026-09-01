#!/usr/bin/env python3
"""UVIR-003: causality domain under *Conditional* matching premises (not Derived).

Critical-path documentation of Master Plan criterion M3 (causality), without
claiming a Derived K_Q.

Premises (all Conditional — R1 structure from CONDITIONAL_KQ_ESTIMATE)
---------------------------------------------------------------------
  K_Q = k_Q M_P^2 = k_Q / (8 π G)
  A   = C_IR / (12 π G a0)     # architecture force normalization
  R_c(θ) = 3 A q (1+cos²θ) / K_Q
  superluminal (Stage-A long-wavelength convention) when R_c > 1
  q_×(θ) / a0 = k_Q / [2 C_IR (1+cos²θ)]

This script maps (k_Q, C_IR, θ, q/a0) and reports the Conditional domain
where R_c ≤ 1. Status remains Conditional / Open for Derived claims.

Tier-1 use: explicit premises table + quantitative domain; no packaging as
“theory proven causal.”
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--kQ-grid",
        type=float,
        nargs="+",
        default=[0.25, 0.5, 1.0, 2.0, 4.0],
    )
    p.add_argument(
        "--CIR-grid",
        type=float,
        nargs="+",
        default=[0.5, 2.0 / 3.0, 1.0, 1.5],
    )
    p.add_argument(
        "--q_over_a0-grid",
        type=float,
        nargs="+",
        default=[0.1, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0],
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    k_Q, C_IR, cos_th, q_over_a0 = sp.symbols(
        "k_Q C_IR cos_theta q_over_a0", positive=True
    )
    # q_cross / a0
    qcross_over_a0 = sp.simplify(
        k_Q / (2 * C_IR * (1 + cos_th**2))
    )
    # R_c = 3 A q / K_Q * (1+cos^2) = (q/a0) / (q_cross/a0)
    # because q_cross = K_Q/(3A(1+cos^2)) ⇒ 3A(1+cos^2)/K_Q = 1/q_cross
    # R_c = q/q_cross = (q/a0) / (q_cross/a0)
    Rc = sp.simplify(q_over_a0 / qcross_over_a0)

    rows = []
    for kQ in args.kQ_grid:
        for cIR in args.CIR_grid:
            for ct, label in ((1.0, "parallel"), (0.0, "perp")):
                qc = float(qcross_over_a0.subs({k_Q: kQ, C_IR: cIR, cos_th: ct}))
                for qa in args.q_over_a0_grid:
                    rc = float(
                        Rc.subs(
                            {
                                k_Q: kQ,
                                C_IR: cIR,
                                cos_th: ct,
                                q_over_a0: qa,
                            }
                        )
                    )
                    rows.append(
                        {
                            "k_Q": kQ,
                            "C_IR": cIR,
                            "direction": label,
                            "q_cross_over_a0": qc,
                            "q_over_a0": qa,
                            "R_c": rc,
                            "causal_Rc_le_1": rc <= 1.0 + 1e-15,
                        }
                    )

    # Reference naive point
    naive = [
        r
        for r in rows
        if abs(r["k_Q"] - 1.0) < 1e-15
        and abs(r["C_IR"] - 2.0 / 3.0) < 1e-12
        and abs(r["q_over_a0"] - 1.0) < 1e-15
    ]

    # Domain summary: for each (kQ, CIR, direction), max q/a0 still causal
    domain = []
    for kQ in args.kQ_grid:
        for cIR in args.CIR_grid:
            for label in ("parallel", "perp"):
                subset = [
                    r
                    for r in rows
                    if r["k_Q"] == kQ
                    and r["C_IR"] == cIR
                    and r["direction"] == label
                    and r["causal_Rc_le_1"]
                ]
                qmax = max((r["q_over_a0"] for r in subset), default=float("nan"))
                qc = next(
                    r["q_cross_over_a0"]
                    for r in rows
                    if r["k_Q"] == kQ
                    and r["C_IR"] == cIR
                    and r["direction"] == label
                )
                domain.append(
                    {
                        "k_Q": kQ,
                        "C_IR": cIR,
                        "direction": label,
                        "q_cross_over_a0": qc,
                        "max_sampled_q_over_a0_with_Rc_le_1": qmax,
                    }
                )

    # Audit sanity: analytic identities
    id_ok = True
    for r in rows:
        qc = r["q_cross_over_a0"]
        expected_rc = r["q_over_a0"] / qc if qc != 0 else float("inf")
        if abs(expected_rc - r["R_c"]) > 1e-9 * max(1.0, abs(expected_rc)):
            id_ok = False
            break

    # At naive (kQ=1, CIR=2/3), parallel q_cross/a0 = 0.375
    naive_parallel_qc = float(
        qcross_over_a0.subs({k_Q: 1, C_IR: sp.Rational(2, 3), cos_th: 1})
    )
    naive_ok = abs(naive_parallel_qc - 0.375) < 1e-12

    passed = id_ok and naive_ok and len(rows) > 0
    summary = {
        "gate": "UVIR-003",
        "stage": "B_CAUSALITY_DOMAIN_CONDITIONAL_MATCHING",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": (
            "PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING"
            if passed
            else "FAIL_CAUSALITY_DOMAIN_CONDITIONAL"
        ),
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "claim_status": "Conditional",
        "premises": [
            "K_Q = k_Q M_P^2 with M_P^2 = 1/(8 pi G) (R1 dimensional analogy — Conditional)",
            "A = C_IR/(12 pi G a0) (architecture force normalization)",
            "R_c = 3 A q (1+cos^2 theta)/K_Q; causal when R_c <= 1 (Stage-A LW convention)",
            "k_Q and C_IR are free Conditional Wilson coefficients in this scan",
        ],
        "not_a_derivation_of": [
            "k_Q",
            "C_IR",
            "K_Q",
            "physical cutoff",
            "MAT-001 vertex",
        ],
        "analytic": {
            "q_cross_over_a0": str(qcross_over_a0),
            "R_c": str(Rc),
            "naive_parallel_q_cross_over_a0": naive_parallel_qc,
        },
        "naive_point_q_over_a0_equals_1": naive,
        "domain_summary": domain,
        "diagnostics": {
            "identity_Rc_equals_q_over_qcross": id_ok,
            "naive_parallel_qc_is_3_8": naive_ok,
            "n_scan_rows": len(rows),
        },
        "scientific_boundary": (
            "Maps the Conditional causality domain under R1-structure matching "
            "premises. Does not derive k_Q or C_IR. Does not close UVIR-003 M3 "
            "as Derived. Does not unlock MAT-001. The naive (k_Q,C_IR)=(1,2/3) "
            "point still places q_cross ~ 0.375 a0 (parallel), so background "
            "gradients of order a0 sit outside the Conditional causal window — "
            "a priority flag for real matching, not a proof of theory failure."
        ),
        "master_plan_criterion": "M3_causality_declared_domain (documentation only)",
        "next_required_calculation": [
            "Replace Conditional (k_Q, C_IR) with matched invariants from R2/R3",
            "Re-evaluate domain after matching",
            "Physical cutoff once normalization fixed",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "uvir003_causality_domain_conditional_summary.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    with (args.output_dir / "uvir003_causality_domain_conditional_scan.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        fields = list(rows[0].keys())
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    with (args.output_dir / "uvir003_causality_domain_summary_table.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        fields = list(domain[0].keys())
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(domain)

    print("Conditional premises: K_Q=k_Q M_P^2, A=C_IR/(12 pi G a0)")
    print(f"Naive parallel q_cross/a0 = {naive_parallel_qc:.6f} (expect 0.375)")
    print(f"Scan rows: {len(rows)}")
    print("STATUS:", summary["subgate_status"])
    print("UVIR-003 full gate: IN_PROGRESS | MAT-001: BLOCKED")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
