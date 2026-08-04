#!/usr/bin/env python3
"""UVIR-003 Stage 2c: causality + NDA diagnostics under Conditional matching floor.

Re-evaluates long-wavelength causality domain and NDA Lambda_|| diagnostics
using the Stage 2b floor parameter P (k_Q or Z_psi*r_rho) and C_IR — without
promoting any point to Derived K_Q.

Inputs:
  PASS_CONDITIONAL_MATCHING_FLOOR
  PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING (structure reuse)
  optional declared unitarity / force strong-coupling NDA summaries

physics_pass: false
MAT unlock: no
UVIR full PASS: no
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir", type=Path, default=base / "outputs")
    p.add_argument(
        "--floor-summary",
        type=Path,
        default=base / "outputs" / "uvir003_conditional_matching_floor_summary.json",
    )
    p.add_argument(
        "--causality-summary",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_causality_domain_conditional_summary.json",
    )
    p.add_argument(
        "--nda-summary",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_force_strong_coupling_estimate_summary.json",
    )
    p.add_argument(
        "--P-grid",
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


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    args = parse_args()
    floor = load_json(args.floor_summary)
    caus = load_json(args.causality_summary)
    nda = load_json(args.nda_summary)

    checks: list[dict[str, Any]] = []

    floor_ok = (
        floor is not None
        and floor.get("subgate_status") == "PASS_CONDITIONAL_MATCHING_FLOOR"
        and (floor.get("stage_2_exit") or {}).get("status")
        == "CONDITIONAL_WITH_SCOPE"
    )
    checks.append(
        {
            "name": "stage_2b_floor_present",
            "ok": floor_ok,
            "got": None if floor is None else floor.get("subgate_status"),
        }
    )

    caus_ok = (
        caus is not None
        and caus.get("subgate_status")
        == "PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING"
    )
    checks.append(
        {
            "name": "prior_causality_conditional_present",
            "ok": caus_ok,
            "got": None if caus is None else caus.get("subgate_status"),
        }
    )

    # --- Causality under floor P, C_IR ---
    P, C_IR, cos_th, qoa = sp.symbols(
        "P C_IR cos_theta q_over_a0", positive=True
    )
    q_cross = sp.simplify(P / (2 * C_IR * (1 + cos_th**2)))
    R_c = sp.simplify(qoa / q_cross)
    I_a0 = sp.Rational(2, 3) * C_IR / P

    rows = []
    for p_val in args.P_grid:
        for c_val in args.CIR_grid:
            for ct, direction in ((1.0, "parallel"), (0.0, "perp")):
                qc = float(
                    q_cross.subs({P: p_val, C_IR: c_val, cos_th: ct})
                )
                for qa in args.q_over_a0_grid:
                    rc = float(
                        R_c.subs(
                            {
                                P: p_val,
                                C_IR: c_val,
                                cos_th: ct,
                                qoa: qa,
                            }
                        )
                    )
                    rows.append(
                        {
                            "P": p_val,
                            "C_IR": c_val,
                            "direction": direction,
                            "q_cross_over_a0": qc,
                            "q_over_a0": qa,
                            "R_c": rc,
                            "causal_Rc_le_1": rc <= 1.0 + 1e-15,
                            "I_a0": float(
                                I_a0.subs({P: p_val, C_IR: c_val})
                            ),
                        }
                    )

    id_ok = True
    for r in rows:
        qc = r["q_cross_over_a0"]
        expected = r["q_over_a0"] / qc if qc != 0 else float("inf")
        if abs(expected - r["R_c"]) > 1e-9 * max(1.0, abs(expected)):
            id_ok = False
            break
    checks.append({"name": "causality_identity_Rc_equals_q_over_qcross", "ok": id_ok})

    # Naive comparison
    naive_par = [
        r
        for r in rows
        if abs(r["P"] - 1.0) < 1e-15
        and abs(r["C_IR"] - 2.0 / 3.0) < 1e-12
        and r["direction"] == "parallel"
        and abs(r["q_over_a0"] - 1.0) < 1e-15
    ]
    naive_ok = (
        len(naive_par) == 1
        and abs(naive_par[0]["q_cross_over_a0"] - 0.375) < 1e-12
        and abs(naive_par[0]["R_c"] - 8.0 / 3.0) < 1e-12
    )
    checks.append(
        {
            "name": "naive_comparison_point_consistent",
            "ok": naive_ok,
            "label": "NON_DERIVED_COMPARISON_ONLY",
        }
    )

    n_rows = len(rows)
    n_causal = sum(1 for r in rows if r["causal_Rc_le_1"])
    checks.append(
        {
            "name": "causality_scan_nonempty",
            "ok": n_rows > 0,
            "n_rows": n_rows,
            "n_causal": n_causal,
            "causal_fraction": n_causal / n_rows if n_rows else None,
        }
    )

    # Domain summary: max q/a0 causal per (P, CIR, direction)
    domain = []
    for p_val in args.P_grid:
        for c_val in args.CIR_grid:
            for direction in ("parallel", "perp"):
                subset = [
                    r
                    for r in rows
                    if r["P"] == p_val
                    and r["C_IR"] == c_val
                    and r["direction"] == direction
                    and r["causal_Rc_le_1"]
                ]
                qmax = max((r["q_over_a0"] for r in subset), default=float("nan"))
                qc = next(
                    r["q_cross_over_a0"]
                    for r in rows
                    if r["P"] == p_val
                    and r["C_IR"] == c_val
                    and r["direction"] == direction
                )
                domain.append(
                    {
                        "P": p_val,
                        "C_IR": c_val,
                        "direction": direction,
                        "q_cross_over_a0": qc,
                        "max_sampled_q_over_a0_with_Rc_le_1": qmax,
                        "I_a0": float(I_a0.subs({P: p_val, C_IR: c_val})),
                    }
                )

    # --- NDA Lambda_|| under floor (diagnostic only) ---
    # Lambda_|| = K_Q^{3/4}/sqrt(A), K_Q = P/(8 pi G), A = C_IR/(12 pi G a0)
    # Lambda_||^4 ~ ... keep symbolic; numeric only with G=1,a0=1 diagnostic units
    K_Q, A, G, a0 = sp.symbols("K_Q A G a0", positive=True)
    lam = K_Q ** sp.Rational(3, 4) / sp.sqrt(A)
    K_Q_floor = P / (8 * sp.pi * G)
    A_floor = C_IR / (12 * sp.pi * G * a0)
    lam_floor = sp.simplify(
        lam.subs({K_Q: K_Q_floor, A: A_floor})
    )
    # At diagnostic G=1, a0=1:
    lam_diag_rows = []
    for p_val in args.P_grid:
        for c_val in args.CIR_grid:
            val = float(
                lam_floor.subs(
                    {P: p_val, C_IR: c_val, G: 1.0, a0: 1.0}
                )
            )
            lam_diag_rows.append(
                {
                    "P": p_val,
                    "C_IR": c_val,
                    "Lambda_parallel_diagnostic_G1_a0_1": val,
                    "units": "diagnostic_only_G_eq_1_a0_eq_1",
                    "claim": "NOT_PHYSICAL_CUTOFF",
                }
            )
    checks.append(
        {
            "name": "nda_lambda_expressed_under_floor",
            "ok": len(lam_diag_rows) > 0 and all(
                r["Lambda_parallel_diagnostic_G1_a0_1"] > 0 for r in lam_diag_rows
            ),
            "formula": str(lam_floor),
        }
    )

    nda_prior = None
    if nda is not None:
        nda_prior = (nda.get("longitudinal_ir_nda_scale") or {}).get(
            "formula_in_K_Q_A"
        ) or nda.get("subgate_status") or nda.get("calculation_status")
    checks.append(
        {
            "name": "prior_nda_summary_optional",
            "ok": True,
            "present": nda is not None,
            "got": nda_prior,
        }
    )

    firewall = {
        "Derived_K_Q": False,
        "physical_cutoff_Derived": False,
        "MAT_PASS": False,
        "UVIR_full_PASS": False,
        "naive_promoted": False,
        "observational_claim": False,
    }
    checks.append(
        {
            "name": "claim_firewall",
            "ok": all(v is False for v in firewall.values()),
            "flags": firewall,
        }
    )

    all_ok = all(c["ok"] for c in checks) and floor_ok
    subgate = (
        "PASS_STAGE2C_FLOOR_DIAGNOSTICS"
        if all_ok
        else "FAIL_STAGE2C_FLOOR_DIAGNOSTICS"
    )

    summary: dict[str, Any] = {
        "gate": "UVIR-003",
        "stage": "B_STAGE2C_FLOOR_DIAGNOSTICS",
        "serial_stage": "2c",
        "calculation_status": "PASS" if all_ok else "FAIL",
        "subgate_status": subgate,
        "claim_status": "Conditional",
        "physics_pass": False,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "kq_numeric_status": "NOT_DERIVED",
        "analytic": {
            "I_a0": str(I_a0),
            "q_cross_over_a0": str(q_cross),
            "R_c": str(R_c),
            "Lambda_parallel_under_floor": str(lam_floor),
            "P_meaning": "k_Q (R1) or Z_psi*r_rho (R3 residual rename)",
        },
        "naive_comparison_only": {
            "label": "NON_DERIVED_COMPARISON_ONLY",
            "P": 1.0,
            "C_IR": 2.0 / 3.0,
            "q_cross_parallel_over_a0": 0.375,
            "R_c_parallel_at_q_eq_a0": float(8.0 / 3.0),
            "I_a0": float(4.0 / 9.0),
        },
        "domain_summary": domain,
        "nda_diagnostic_rows": lam_diag_rows,
        "scan_diagnostics": {
            "n_rows": n_rows,
            "n_causal": n_causal,
            "identity_ok": id_ok,
        },
        "checks": checks,
        "claim_firewall": firewall,
        "scientific_boundary": (
            "Re-evaluates causality domain and NDA Lambda diagnostic under Stage 2b "
            "Conditional floor parameter P. Does not derive K_Q, does not establish "
            "physical cutoff, does not unlock MAT or close UVIR-003."
        ),
        "next_required": [
            "Stage 3: scoped MAT calculation under 2b handoff (no MAT PASS)",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out = args.output_dir / "uvir003_stage2c_floor_diagnostics_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    out.write_bytes(payload)
    h = hashlib.sha256(payload).hexdigest()
    (
        args.output_dir / "uvir003_stage2c_floor_diagnostics_summary.sha256"
    ).write_bytes(f"{h}  {out.name}\n".encode("utf-8"))

    with (args.output_dir / "uvir003_stage2c_floor_causality_scan.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("UVIR-003 Stage 2c floor diagnostics")
    print("  physics_pass: False | MAT: BLOCKED | UVIR: IN_PROGRESS")
    print(f"  causality rows: {n_rows}, causal: {n_causal}")
    for c in checks:
        print(f"  [{'OK' if c['ok'] else 'FAIL'}] {c['name']}")
    print("STATUS:", subgate)
    print("JSON_SHA256:", h)
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
