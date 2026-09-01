#!/usr/bin/env python3
"""UVIR-003: local adiabatic observable normalization (not an S-matrix).

Problem addressed
-----------------
The local four-leg kernel K(q) is residue-normalized at a frozen-time snapshot.
A cosmological S-matrix is not defined.  This script records an *explicit*
substitute: a Gaussian wave-packet average of the local combined kernel over
the controlled adiabatic exchange domain,

    O[sigma] = sum_i w_i K(q_i) / sum_i w_i,
    w_i = exp( -(ln(q_i/q0))^2 / (2 sigma^2) ),

using already-admitted external ratios and the assembled local kernel values
from the tetrahedral four-leg summary.

Diagnostics (pass conditions)
-----------------------------
1. Weights are positive and finite on the admitted domain.
2. As sigma -> 0 (narrow packet), O approaches the on-shell kernel at q0.
3. Imaginary part of O remains negligible if each K_i is real within tolerance.
4. No unitarity, optical theorem, or cross-section is claimed.

This is a declared *observable proxy normalization*, not a physical amplitude.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--kernel-summary",
        type=Path,
        default=base / "outputs" / "uvir003_local_four_leg_kernel_summary.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base / "outputs",
    )
    parser.add_argument(
        "--q0-over-H",
        type=float,
        default=50.0,
        help="Packet centre in units of H (must appear in kernel cases).",
    )
    parser.add_argument(
        "--sigmas",
        type=float,
        nargs="+",
        default=[0.02, 0.05, 0.10, 0.20, 0.40],
        help="Gaussian widths in ln(q/q0).",
    )
    parser.add_argument(
        "--left-mode",
        type=str,
        default=None,
        help="Optional mode label filter (default: first available pair at q0).",
    )
    parser.add_argument(
        "--right-mode",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--narrow-tol",
        type=float,
        default=5.0e-2,
        help="Max relative |O-K0|/|K0| for narrowest sigma.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def complex_from(rec: dict[str, float]) -> complex:
    return complex(rec["real"], rec["imag"])


def main() -> None:
    args = parse_args()
    summary = load_json(args.kernel_summary)
    require(
        "local four-leg dependency",
        summary.get("subgate_status")
        == "PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL",
    )
    cases = summary["case_results"]
    require("cases present", len(cases) > 0)

    # Group kernels by (q/H, left, right)
    by_key: dict[tuple[float, str, str], complex] = {}
    for case in cases:
        key = (
            float(case["initial_q_over_H"]),
            str(case["left_mode"]),
            str(case["right_mode"]),
        )
        by_key[key] = complex_from(case["exchange_plus_reduced_contact"])

    ratios = sorted({k[0] for k in by_key})
    require("q0 in sampled ratios", any(abs(r - args.q0_over_H) < 1e-12 for r in ratios))

    # Choose a mode pair present at q0
    candidates = [
        (lm, rm)
        for (r, lm, rm) in by_key
        if abs(r - args.q0_over_H) < 1e-12
    ]
    require("mode pair at q0", len(candidates) > 0)
    if args.left_mode and args.right_mode:
        pair = (args.left_mode, args.right_mode)
        require("requested mode pair present", pair in candidates)
    else:
        # Prefer identical-species lowest labels for stability
        pair = sorted(candidates, key=lambda p: (p[0] != p[1], p[0], p[1]))[0]

    left_mode, right_mode = pair
    series: list[tuple[float, complex]] = []
    for r in ratios:
        key = (r, left_mode, right_mode)
        if key in by_key:
            series.append((r, by_key[key]))
    require("series length >= 2", len(series) >= 2)

    k0 = by_key[(args.q0_over_H, left_mode, right_mode)]
    packet_rows: list[dict[str, Any]] = []
    for sigma in args.sigmas:
        require("positive sigma", sigma > 0.0)
        weights = []
        values = []
        for r, k in series:
            w = math.exp(-0.5 * (math.log(r / args.q0_over_H) / sigma) ** 2)
            weights.append(w)
            values.append(k)
        wsum = sum(weights)
        require("positive weight sum", wsum > 0.0)
        obs = sum(w * k for w, k in zip(weights, values)) / wsum
        rel = abs(obs - k0) / max(abs(k0), 1.0e-30)
        imag_frac = abs(obs.imag) / max(abs(obs), 1.0e-30)
        packet_rows.append(
            {
                "sigma_ln": sigma,
                "observable_real": obs.real,
                "observable_imag": obs.imag,
                "observable_abs": abs(obs),
                "on_shell_abs": abs(k0),
                "relative_deviation_from_on_shell": rel,
                "imaginary_fraction": imag_frac,
                "weight_sum": wsum,
                "effective_support_count": sum(1 for w in weights if w > 0.01 * max(weights)),
            }
        )

    # Narrowest sigma should approach on-shell
    narrow = min(packet_rows, key=lambda row: row["sigma_ln"])
    wide = max(packet_rows, key=lambda row: row["sigma_ln"])
    narrow_ok = narrow["relative_deviation_from_on_shell"] < args.narrow_tol
    imag_ok = all(row["imaginary_fraction"] < 1.0e-8 for row in packet_rows)
    monotone_hint = (
        wide["relative_deviation_from_on_shell"]
        >= narrow["relative_deviation_from_on_shell"] - 1.0e-12
    )
    # Monotone is diagnostic only; do not hard-fail if sampling is sparse
    passed = narrow_ok and imag_ok
    status = (
        "PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION"
        if passed
        else "FAIL_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION"
    )

    out = {
        "gate": "UVIR-003",
        "stage": "B_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": (
            "LOCAL_PACKET_PROXY_DEFINED_S_MATRIX_NOT_ESTABLISHED"
        ),
        "definition": {
            "observable": (
                "Gaussian average of local combined four-leg kernel over "
                "admitted external q/H samples in ln(q/q0)."
            ),
            "weight": "w = exp(-(ln(q/q0))^2 / (2 sigma^2))",
            "not_an_s_matrix": True,
            "not_a_unitarity_bound": True,
            "not_a_cross_section": True,
        },
        "mode_pair": {"left": left_mode, "right": right_mode},
        "q0_over_H": args.q0_over_H,
        "on_shell_kernel": {
            "real": k0.real,
            "imag": k0.imag,
            "abs": abs(k0),
        },
        "sampled_ratios": ratios,
        "packet_results": packet_rows,
        "diagnostics": {
            "narrow_sigma": narrow["sigma_ln"],
            "narrow_relative_deviation": narrow[
                "relative_deviation_from_on_shell"
            ],
            "narrow_tolerance": args.narrow_tol,
            "narrow_ok": narrow_ok,
            "imaginary_ok": imag_ok,
            "wide_relative_deviation": wide[
                "relative_deviation_from_on_shell"
            ],
            "monotone_deviation_with_width_diagnostic": monotone_hint,
        },
        "scientific_boundary": (
            "Defines a local adiabatic packet-averaged proxy for the frozen "
            "kernel only. Does not construct FRW asymptotic states, optical "
            "theorem checks, strong-coupling scales, or MAT-001 matching."
        ),
        "next_required_calculation": [
            "optional denser homogeneous-edge deformation scan",
            "promote packet proxy to true in-in correlator on FRW trajectory",
            "nonzero-gradient |grad(pi)|^3 sector",
            "only then declared unitarity / EFT-validity criterion",
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = (
        args.output_dir / "uvir003_local_adiabatic_observable_norm_summary.json"
    )
    csv_path = args.output_dir / "uvir003_local_adiabatic_observable_norm.csv"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(out, handle, indent=2, sort_keys=True)
        handle.write("\n")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        fields = list(packet_rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(packet_rows)

    print(f"Mode pair: {left_mode}, {right_mode}")
    print(f"q0/H: {args.q0_over_H}")
    print(f"On-shell |K|: {abs(k0):.6e}")
    print(
        f"Narrow sigma={narrow['sigma_ln']}: "
        f"rel dev={narrow['relative_deviation_from_on_shell']:.3e}"
    )
    print(
        f"Wide sigma={wide['sigma_ln']}: "
        f"rel dev={wide['relative_deviation_from_on_shell']:.3e}"
    )
    print("S-matrix: NOT_ESTABLISHED")
    print("Unitarity bound: NOT_ESTABLISHED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(f"STATUS: {status}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
