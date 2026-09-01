#!/usr/bin/env python3
"""UVIR-003: declare FRW in-in / two-time observable path (not a finished S-matrix).

Promotion step after the local adiabatic packet proxy.

What this does
--------------
1. Loads the verified FRW representative branch trajectory.
2. Loads the local packet-averaged kernel proxy O[sigma] (requires prior
   PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION).
3. Loads the fixed-comoving transfer summary and isolates the *high-q controlled
   adiabatic subset* as the only transfer data allowed into the proxy.
4. Declares an explicit two-time skeleton:

      G_proxy(t_out, t_in; sigma) = O[sigma] * T_gain(q_label)

   where T_gain is the endpoint normalized phase-space gain for a controlled
   high-q transfer sample (diagnostic, not a cosmological cross section).

5. Records adiabaticity / scope diagnostics along the FRW trajectory (H(t), a(t),
   q_phys/H = (q/H)_freeze * (H_freeze/H) * (a_freeze/a) for fixed comoving k).

What this does *not* do
-----------------------
- Full nested time integrals of interaction-picture in-in diagrams.
- Optical theorem / unitarity bounds.
- MAT-001 unlock.
- Treating the local tetrahedral kernel as already an S-matrix element.

Pass criteria (this subgate)
----------------------------
- FRW trajectory finite and on-shell residuals already verified by prior gate.
- Packet proxy summary present and PASS.
- High-q controlled transfer subset identifiable.
- Declared path JSON written with explicit scientific_boundary.
- No claim that G_proxy is a physical rate.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--frw-trajectory",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_trajectory.csv",
    )
    parser.add_argument(
        "--frw-summary",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_summary.json",
    )
    parser.add_argument(
        "--packet-summary",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_local_adiabatic_observable_norm_summary.json",
    )
    parser.add_argument(
        "--transfer-summary",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_propagator_adiabaticity_transfer_summary.json",
    )
    parser.add_argument(
        "--exchange-domain",
        type=Path,
        default=base / "outputs" / "uvir003_controlled_exchange_domain_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument(
        "--sigma-ln",
        type=float,
        default=0.05,
        help="Packet width to pick from packet summary (closest match).",
    )
    parser.add_argument(
        "--high-q-min-initial",
        type=float,
        default=10.0,
        help="Min initial q/H for transfer samples treated as controlled high-q.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    args = parse_args()

    frw_sum = load_json(args.frw_summary)
    require(
        "FRW branch verified",
        frw_sum.get("background_status")
        == "ON_SHELL_REPRESENTATIVE_BRANCH_VERIFIED"
        or frw_sum.get("calculation_status") == "PASS",
    )

    packet = load_json(args.packet_summary)
    require(
        "packet proxy pass",
        packet.get("subgate_status")
        == "PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION",
    )

    transfer = load_json(args.transfer_summary)
    domain = load_json(args.exchange_domain)

    # Trajectory
    rows = []
    with args.frw_trajectory.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({k: float(row[k]) for k in row})
    require("trajectory nonempty", len(rows) > 10)
    t0 = rows[0]
    t1 = rows[-1]

    # Packet O[sigma]
    packet_rows = packet["packet_results"]
    best = min(
        packet_rows,
        key=lambda r: abs(float(r["sigma_ln"]) - args.sigma_ln),
    )
    o_abs = float(best["observable_abs"])
    o_real = float(best["observable_real"])
    sigma_used = float(best["sigma_ln"])

    # High-q controlled transfer subset
    mode_results = transfer.get("mode_results") or []
    high_q = [
        m
        for m in mode_results
        if float(m.get("initial_q_over_H", 0.0)) >= args.high_q_min_initial
        and m.get("numerical_status") == "CONVERGED_GAUGE_INVARIANT_TRANSFER"
    ]
    # Prefer samples that stay relatively controlled (lower max adiabaticity)
    high_q_sorted = sorted(
        high_q,
        key=lambda m: float(m.get("maximum_real_mode_adiabaticity", 1e99)),
    )
    require("at least one high-q transfer sample", len(high_q_sorted) > 0)
    best_transfer = high_q_sorted[0]
    t_gain = float(best_transfer["endpoint_normalized_phase_space_gain"])
    q_label = float(best_transfer["initial_q_over_H"])

    # Declared proxy (explicit, not physical rate)
    g_proxy_abs = o_abs * abs(t_gain)
    g_proxy_real = o_real * t_gain  # diagnostic only if T_gain real-positive

    # Trajectory scale of fixed-comoving mode matching freeze q0
    q0_over_h = float(packet.get("q0_over_H", 50.0))
    h0 = t0["H"]
    a0 = t0["a"]
    trajectory_q = []
    for row in rows[:: max(1, len(rows) // 40)]:
        # fixed comoving k from initial q_phys = (q0/H)*H at a=a0
        # q_phys(t) = k/a, k = q0_over_h * H0 * a0
        k_comov = q0_over_h * h0 * a0
        q_phys = k_comov / row["a"]
        q_over_h = q_phys / row["H"]
        trajectory_q.append(
            {
                "t": row["t"],
                "a": row["a"],
                "H": row["H"],
                "rho": row["rho"],
                "q_phys_over_H_fixed_comoving": q_over_h,
            }
        )

    admitted = domain.get("sampled_domain", {}).get(
        "admitted_initial_q_over_H_values", []
    )

    # Pass: path declared, dependencies present, proxy finite
    finite = math.isfinite(g_proxy_abs) and math.isfinite(o_abs) and math.isfinite(
        t_gain
    )
    nonzero = o_abs > 0.0
    # Transfer hold is allowed — we only use high-q subset as diagnostic
    transfer_hold = transfer.get("calculation_status") == "HOLD"
    passed = finite and nonzero and len(high_q_sorted) > 0
    status = (
        "PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED"
        if passed
        else "FAIL_FRW_IN_IN_OBSERVABLE_PATH"
    )

    summary = {
        "gate": "UVIR-003",
        "stage": "B_FRW_IN_IN_OBSERVABLE_PATH",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": (
            "IN_IN_PATH_DECLARED_FULL_DIAGRAM_NOT_ESTABLISHED"
        ),
        "definition": {
            "local_packet_proxy": "O[sigma] from local adiabatic observable norm",
            "two_time_skeleton": "G_proxy = O[sigma] * T_gain(high-q transfer)",
            "T_gain": (
                "endpoint_normalized_phase_space_gain on controlled high-q "
                "fixed-comoving transfer sample"
            ),
            "not_a_cross_section": True,
            "not_an_s_matrix": True,
            "not_a_unitarity_bound": True,
            "full_in_in_time_integrals": "NOT_COMPUTED",
        },
        "dependencies": {
            "frw_background_status": frw_sum.get("background_status"),
            "packet_subgate": packet.get("subgate_status"),
            "transfer_calculation_status": transfer.get("calculation_status"),
            "transfer_hold_retained": transfer_hold,
            "exchange_domain_subgate": domain.get("subgate_status"),
            "admitted_external_q_over_H": admitted,
        },
        "packet_selection": {
            "requested_sigma_ln": args.sigma_ln,
            "used_sigma_ln": sigma_used,
            "observable_real": o_real,
            "observable_abs": o_abs,
            "q0_over_H": q0_over_h,
            "mode_pair": packet.get("mode_pair"),
        },
        "transfer_selection": {
            "high_q_min_initial": args.high_q_min_initial,
            "high_q_sample_count": len(high_q_sorted),
            "chosen_initial_q_over_H": q_label,
            "endpoint_normalized_phase_space_gain": t_gain,
            "maximum_real_mode_adiabaticity": float(
                best_transfer.get("maximum_real_mode_adiabaticity", float("nan"))
            ),
            "numerical_status": best_transfer.get("numerical_status"),
        },
        "frw_window": {
            "t_initial": t0["t"],
            "t_final": t1["t"],
            "a_initial": t0["a"],
            "a_final": t1["a"],
            "H_initial": t0["H"],
            "H_final": t1["H"],
            "samples": len(rows),
        },
        "trajectory_fixed_comoving_q_over_H_sample": trajectory_q,
        "declared_proxy": {
            "G_proxy_abs": g_proxy_abs,
            "G_proxy_real_diagnostic": g_proxy_real,
            "formula": "abs(O)*abs(T_gain)",
        },
        "scientific_boundary": (
            "Declares how a local packet proxy will attach to the FRW branch "
            "and to controlled high-q transfer diagnostics. Does not evaluate "
            "full in-in nested time integrals, does not establish unitarity, "
            "and does not unlock MAT-001. Transfer summary may remain HOLD for "
            "infrared modes; only high-q controlled samples enter the proxy."
        ),
        "next_required_calculation": [
            "evaluate local kernel (or reduced response) at multiple FRW slices "
            "in the admitted high-q domain, not only the initial freeze",
            "replace scalar T_gain with mode-projected two-time Green's function "
            "from the reduced quadratic system",
            "nonzero-gradient |grad(pi)|^3 sector",
            "only then declared perturbative-unitarity / EFT-validity criterion",
        ],
        "diagnostics": {
            "proxy_finite": finite,
            "packet_nonzero": nonzero,
            "high_q_transfer_available": len(high_q_sorted) > 0,
        },
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json = args.output_dir / "uvir003_frw_in_in_observable_path_summary.json"
    out_csv = args.output_dir / "uvir003_frw_in_in_q_over_H_track.csv"
    with out_json.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        fields = list(trajectory_q[0].keys())
        w = csv.DictWriter(handle, fieldnames=fields)
        w.writeheader()
        w.writerows(trajectory_q)

    print(f"FRW samples: {len(rows)}  a: {t0['a']:.4g} -> {t1['a']:.4g}")
    print(f"Packet O|abs| (sigma={sigma_used}): {o_abs:.6e}")
    print(f"High-q transfer samples: {len(high_q_sorted)}  chosen q/H={q_label}")
    print(f"T_gain: {t_gain:.6e}")
    print(f"G_proxy abs (diagnostic): {g_proxy_abs:.6e}")
    print("Full in-in time integrals: NOT_COMPUTED")
    print("S-matrix: NOT_ESTABLISHED")
    print("Unitarity: NOT_ESTABLISHED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(f"STATUS: {status}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
