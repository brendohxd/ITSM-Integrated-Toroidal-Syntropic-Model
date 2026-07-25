#!/usr/bin/env python3
"""UVIR-003 Stage-A causality addendum: force-sector characteristic speed.

Checks the regulated force dispersion relation already derived in
uvir003_stage_a.py for bounded phase/group velocity. This does not repeat
the Stage-A action derivation; it takes the boxed dispersion relation as
given and asks whether it stays subluminal.
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
        help="Directory for the causality-check JSON summary.",
    )
    return parser.parse_args()


def require_zero(name: str, expression: sp.Expr) -> None:
    simplified = sp.simplify(expression)
    if simplified != 0:
        raise AssertionError(f"{name} failed: {simplified}")


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    amplitude, k_q, gamma, m_star, q, k = sp.symbols(
        "A K_Q gamma M_star q k", positive=True
    )
    cosine = sp.symbols("cos_theta", real=True)

    omega_sq = (
        3 * amplitude * q * (1 + cosine**2) * k**2 + gamma * k**4 / m_star**2
    ) / k_q

    # ------------------------------------------------------------------
    # 1. Long-wavelength (k -> 0) phase velocity and its threshold in q.
    # ------------------------------------------------------------------
    v_ph_sq = sp.simplify(omega_sq / k**2)
    v_ph_sq_zero_k = sp.simplify(sp.limit(v_ph_sq, k, 0))
    expected_zero_k = 3 * amplitude * q * (1 + cosine**2) / k_q
    require_zero(
        "long-wavelength phase velocity squared",
        v_ph_sq_zero_k - expected_zero_k,
    )
    q_cross = sp.simplify(sp.solve(sp.Eq(expected_zero_k, 1), q)[0])

    # ------------------------------------------------------------------
    # 2. Short-wavelength (k -> infinity) phase and group velocity limits.
    # ------------------------------------------------------------------
    v_ph_sq_limit = sp.limit(v_ph_sq, k, sp.oo)
    omega = sp.sqrt(omega_sq)
    v_group = sp.diff(omega, k)
    v_group_limit = sp.limit(v_group, k, sp.oo)
    v_group_leading = sp.simplify(
        sp.limit(v_group / k, k, sp.oo)
    )  # confirms v_g grows linearly in k, i.e. unboundedly
    expected_leading = 2 * sp.sqrt(gamma / (k_q * m_star**2))
    require_zero("group velocity leading coefficient", v_group_leading - expected_leading)

    # ------------------------------------------------------------------
    # 3. Light-crossing wavenumber, valid only when K_Q > 3Aq(1+cos^2 theta).
    # ------------------------------------------------------------------
    k_light_sq = sp.simplify(
        m_star**2 * (k_q - 3 * amplitude * q * (1 + cosine**2)) / gamma
    )

    # ------------------------------------------------------------------
    # 4. Numerical illustration at representative parameter values.
    # ------------------------------------------------------------------
    numeric_cases = [
        ("subluminal_at_k0_moderate_q", 1.0, 1.0, 0.5, 0.1, 1.0, 1.0),
        ("superluminal_at_k0_large_q", 1.0, 1.0, 0.5, 1.0, 1.0, 1.0),
        ("moderate_q_perpendicular", 1.0, 1.0, 0.5, 0.1, 0.0, 1.0),
    ]
    rows = []
    subs_common = {amplitude: 1.0, k_q: 1.0, gamma: 0.5, m_star: 1.0}
    for name, va, vkq, vgamma, vq, vcos, _ in numeric_cases:
        subs = {amplitude: va, k_q: vkq, gamma: vgamma, q: vq, cosine: vcos}
        v_ph_sq_k0 = float(v_ph_sq_zero_k.subs(subs))
        rows.append(
            {
                "case": name,
                "A": va,
                "K_Q": vkq,
                "gamma": vgamma,
                "q": vq,
                "cos_theta": vcos,
                "v_ph_sq_at_k0": v_ph_sq_k0,
                "superluminal_at_long_wavelength": v_ph_sq_k0 > 1.0,
            }
        )

    ks = [1.0, 10.0, 100.0, 1000.0]
    growth_rows = []
    for kv in ks:
        subs = {amplitude: 1.0, k_q: 1.0, gamma: 0.5, m_star: 1.0, q: 0.1, cosine: 1.0, k: kv}
        v_ph_sq_val = float(v_ph_sq.subs(subs))
        growth_rows.append({"k": kv, "v_ph_sq": v_ph_sq_val})
    monotonically_diverging = all(
        growth_rows[i + 1]["v_ph_sq"] > growth_rows[i]["v_ph_sq"]
        for i in range(len(growth_rows) - 1)
    )
    if not monotonically_diverging:
        raise AssertionError("expected v_ph_sq to grow monotonically with k")

    summary = {
        "gate": "UVIR-003",
        "addendum": "STAGE_A_CAUSALITY",
        "revises_stage_a_pass": False,
        "long_wavelength": {
            "v_ph_squared_at_k0": str(expected_zero_k),
            "superluminal_threshold_q": str(q_cross),
            "depends_on_regulator": False,
            "verdict": "CONDITIONAL_ON_K_Q_OVER_A_RATIO",
        },
        "short_wavelength": {
            "v_ph_squared_limit_k_to_infinity": str(v_ph_sq_limit),
            "v_group_limit_k_to_infinity": str(v_group_limit),
            "v_group_leading_coefficient": str(v_group_leading),
            "verdict": "UNBOUNDED_FOR_ALL_POSITIVE_A_K_Q_GAMMA",
        },
        "light_crossing_wavenumber_squared": str(k_light_sq),
        "physical_eft_cutoff_comparison": "NOT_PERFORMED_REQUIRES_COMPLETED_STAGE_B_ITEM_9",
        "numeric_illustration": rows,
        "growth_check": growth_rows,
        "not_yet_done": [
            "fix K_Q relative to A via canonical normalization or matching",
            "evaluate q_cross against physically relevant background gradient ~a0",
            "derive the physical EFT cutoff for the full anisotropic cubic-plus-k4 system (Stage B item 9)",
            "compare k_light against the physical EFT cutoff",
            "covariant regulator and foliation-causality check on vortical U backgrounds",
        ],
        "status": "OPEN",
    }
    json_path = args.output_dir / "uvir003_causality_addendum_summary.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print(
        "UVIR-003 Stage-A causality addendum: long-wavelength speed "
        "CONDITIONAL (depends on K_Q/A vs q)"
    )
    print("Short-wavelength speed: UNBOUNDED for all positive K_Q, A, gamma (structural)")
    print("Physical EFT cutoff comparison: NOT PERFORMED (requires completed Stage B item 9)")
    print("STATUS: OPEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
