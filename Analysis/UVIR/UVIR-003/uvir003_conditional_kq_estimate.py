#!/usr/bin/env python3
"""UVIR-003 causality addendum: conditional K_Q estimate (speculative).

This is NOT a derivation of K_Q. It tests one candidate matching hypothesis
by dimensional analogy and reports what it would imply for the causality
addendum's q_cross threshold IF that hypothesis holds and IF the Wilson
coefficients it introduces (k_Q, C_IR) take their naively expected O(1)
values. Every premise is flagged explicitly in the output.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
        help="Directory for the conditional-estimate JSON summary.",
    )
    return parser.parse_args()


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    k_Q, M_P, G, a0, C_IR, cos_theta = sp.symbols(
        "k_Q M_P G a0 C_IR cos_theta", positive=True
    )

    # Candidate hypothesis: the temporal Q-kinetic term, written in the
    # a0-normalized invariant Q_norm=U.nabla(psi)/a0 declared in
    # UVIR-002_ROUTE_SELECTION.md ("Q=U^mu nabla_mu psi/a0"), takes the same
    # M_P^2*a0^2 EFT-normalization prefactor already forced (by dimensional
    # necessity, given only M_P and a0 are declared scales) on the force
    # operator's C_IR term, with no subtracted background (Q0=0, matching
    # Stage A's own Q=dot(pi) treatment). This is not derived from the
    # declared action or prior architecture; it is introduced only by the
    # conditional-estimate gate note and flagged as a candidate throughout.
    K_Q_candidate = k_Q * M_P**2
    A_declared = C_IR / (12 * sp.pi * G * a0)  # confirmed relation, not speculative
    M_P_sq = 1 / (8 * sp.pi * G)

    K_Q_explicit = K_Q_candidate.subs(M_P**2, M_P_sq)
    q_cross = sp.simplify(K_Q_explicit / (3 * A_declared * (1 + cos_theta**2)))

    rows = []
    for label, ct in [("theta=0 (along background gradient)", 1), ("theta=90deg (perpendicular)", 0)]:
        expr = sp.simplify(q_cross.subs(cos_theta, ct))
        numeric_ratio = sp.simplify(expr.subs({k_Q: 1, C_IR: sp.Rational(2, 3)}) / a0)
        rows.append(
            {
                "direction": label,
                "q_cross_formula": str(expr),
                "q_cross_over_a0_at_kQ1_CIR23": str(numeric_ratio),
                "q_cross_over_a0_numeric": float(numeric_ratio),
            }
        )

    summary = {
        "gate": "UVIR-003",
        "addendum": "CONDITIONAL_K_Q_ESTIMATE",
        "status": "SPECULATIVE_NOT_A_DERIVATION",
        "premises_none_confirmed": [
            "K_Q = k_Q * M_P^2 with Q0=0 (candidate dimensional-analogy matching introduced only by this conditional-estimate note; not derived from the action or prior architecture)",
            "k_Q ~ O(1) (no derivation exists; pure NDA-style guess)",
            "C_IR ~ 2/3 (already only a 'Conditional' matching hypothesis per the ledger, not confirmed)",
        ],
        "q_cross_estimates": rows,
        "interpretation": (
            "IF all three premises hold, q_cross falls in the range ~0.375-0.75 "
            "times a0 - i.e. the same order as a0 itself, and below it. Since the "
            "force operator is designed to be physically relevant for background "
            "gradients q at and above a0, this would put the long-wavelength "
            "force mode at or past its own superluminal threshold across most of "
            "the regime the theory is built to describe. This does NOT confirm a "
            "problem - every premise is unconfirmed - but it means the missing "
            "K_Q matching condition is not a routine bookkeeping gap: filling it "
            "with the most naively expected values lands close to or past the "
            "causality threshold, which is a reason to prioritize deriving K_Q "
            "rigorously rather than treating it as a formality."
        ),
        "not_yet_done": [
            "an actual derivation of K_Q from a microscopic or matching argument",
            "checking whether the M_P^2*a0^2 prefactor candidate for the Q-kinetic term is even the right structure (vs. e.g. a different scale entirely)",
            "resolving C_IR itself, which the ledger already lists as unresolved",
        ],
    }
    json_path = args.output_dir / "uvir003_conditional_kq_estimate_summary.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-003 conditional K_Q estimate: SPECULATIVE, not a derivation")
    for row in rows:
        print(f"  {row['direction']}: q_cross ~ {row['q_cross_over_a0_numeric']:.3f} * a0")
    print("STATUS: SPECULATIVE_NOT_A_DERIVATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
