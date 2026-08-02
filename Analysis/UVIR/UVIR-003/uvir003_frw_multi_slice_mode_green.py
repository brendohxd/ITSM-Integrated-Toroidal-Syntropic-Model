#!/usr/bin/env python3
"""UVIR-003: multi-slice FRW local-kernel sampling + mode-projected two-time Green proxy.

Master plan remaining alpha.10 item 1 (post PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED):

  - Evaluate local kernel / reduced response at multiple FRW slices in the
    admitted high-q domain (not only the initial freeze).
  - Replace scalar T_gain with a mode-projected two-time Green proxy built from
    the existing high-q fixed-comoving transfer singular-value history.

What this is
------------
1. Multi-slice local kernel map K_slice(t) for fixed-comoving high-q modes by
   nearest-neighbour lookup of the assembled local four-leg kernel
   (exchange_plus_reduced_contact) at channel q_phys/H(t).
2. Mode-projected two-time Green proxy on a coarse FRW time grid:

      G_mp(t_out, t_in; mode) =
          K_nn(q_phys(t_in)/H(t_in))
          * SV_mode(t_out) / SV_mode(t_in)     for t_out >= t_in
          0                                     for t_out <  t_in

   where SV is the endpoint-normalized largest singular value of the gauge-
   invariant transfer for that fixed-comoving high-q mode (already computed by
   the propagator adiabaticity transfer integrator).

What this is *not*
------------------
- Nested interaction-picture in-in time integrals.
- Optical theorem / unitarity bound.
- MAT-001 unlock.
- Nonzero-gradient |grad(pi)|^3 (still held).

Pass criteria
-------------
1. >= N_min FRW slices with finite K lookup in high-q domain.
2. At least one high-q transfer mode time series loaded.
3. Causal Green proxy finite on the declared grid.
4. Explicit scientific boundary written to JSON.
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
        "--kernel-summary",
        type=Path,
        default=base / "outputs" / "uvir003_local_four_leg_kernel_summary.json",
    )
    parser.add_argument(
        "--packet-summary",
        type=Path,
        default=base
        / "outputs"
        / "uvir003_local_adiabatic_observable_norm_summary.json",
    )
    parser.add_argument(
        "--transfer-csv",
        type=Path,
        default=base / "outputs" / "uvir003_propagator_adiabaticity_transfer.csv",
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
        "--high-q-min",
        type=float,
        default=10.0,
        help="Minimum initial and/or local q/H treated as controlled high-q.",
    )
    parser.add_argument(
        "--n-slices",
        type=int,
        default=12,
        help="Number of FRW time slices for multi-slice kernel sampling.",
    )
    parser.add_argument(
        "--green-grid",
        type=int,
        default=8,
        help="Coarse time grid size for the mode-projected Green proxy.",
    )
    parser.add_argument(
        "--min-slice-hits",
        type=int,
        default=6,
        help="Minimum high-q slice samples with finite kernel lookup.",
    )
    parser.add_argument(
        "--prefer-mode-pair",
        type=str,
        default="physical_pair_1",
        help="Diagonal mode pair label for kernel lookup.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_csv_float_rows(path: Path) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({k: float(row[k]) for k in row})
    return rows


def complex_abs(rec: dict[str, Any]) -> float:
    return float(rec.get("abs", abs(complex(rec["real"], rec["imag"]))))


def build_kernel_table(
    case_results: list[dict[str, Any]], prefer_mode: str
) -> list[tuple[float, float, float, str, str]]:
    """Return list of (channel_q_over_H, K_real, K_abs, left, right)."""
    table: list[tuple[float, float, float, str, str]] = []
    for case in case_results:
        left = str(case.get("left_mode", ""))
        right = str(case.get("right_mode", ""))
        # Prefer diagonal preferred mode; still keep other diagonals as fallback
        if left != right:
            continue
        kernel = case.get("exchange_plus_reduced_contact")
        if not isinstance(kernel, dict):
            continue
        q = float(case["channel_q_over_H"])
        k_real = float(kernel["real"])
        k_abs = complex_abs(kernel)
        table.append((q, k_real, k_abs, left, right))
    # Sort preferred mode first at each q
    table.sort(key=lambda r: (0 if r[3] == prefer_mode else 1, r[0]))
    return table


def nearest_kernel(
    table: list[tuple[float, float, float, str, str]],
    q: float,
    prefer_mode: str,
) -> tuple[float, float, float, str, float] | None:
    """Nearest (q_ref, K_real, K_abs, mode, relative_q_error)."""
    if not table:
        return None
    preferred = [r for r in table if r[3] == prefer_mode]
    pool = preferred if preferred else table
    best = min(pool, key=lambda r: abs(r[0] - q))
    rel = abs(best[0] - q) / max(abs(q), 1.0e-12)
    return best[0], best[1], best[2], best[3], rel


def subsample_indices(n: int, m: int) -> list[int]:
    if m >= n:
        return list(range(n))
    return sorted({int(round(i * (n - 1) / (m - 1))) for i in range(m)})


def main() -> None:
    args = parse_args()

    frw_sum = load_json(args.frw_summary)
    require(
        "FRW branch verified",
        frw_sum.get("background_status")
        == "ON_SHELL_REPRESENTATIVE_BRANCH_VERIFIED"
        or frw_sum.get("calculation_status") == "PASS",
    )

    kernel_sum = load_json(args.kernel_summary)
    require(
        "local four-leg kernel pass",
        kernel_sum.get("subgate_status")
        == "PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL",
    )

    packet = load_json(args.packet_summary)
    require(
        "packet proxy pass",
        packet.get("subgate_status")
        == "PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION",
    )

    transfer_sum = load_json(args.transfer_summary)
    domain = load_json(args.exchange_domain)
    traj = load_csv_float_rows(args.frw_trajectory)
    require("trajectory nonempty", len(traj) > 10)
    transfer_rows = load_csv_float_rows(args.transfer_csv)
    require("transfer series nonempty", len(transfer_rows) > 10)

    kernel_table = build_kernel_table(
        kernel_sum.get("case_results") or [], args.prefer_mode_pair
    )
    require("kernel diagonal table nonempty", len(kernel_table) > 0)

    # Packet O for optional G = O * T style comparison
    packet_rows = packet.get("packet_results") or []
    best_packet = min(
        packet_rows,
        key=lambda r: abs(float(r["sigma_ln"]) - 0.05),
    )
    o_abs = float(best_packet["observable_abs"])
    q0_packet = float(packet.get("q0_over_H", 50.0))

    # High-q transfer modes (initial q/H)
    by_mode: dict[float, list[dict[str, float]]] = {}
    for row in transfer_rows:
        q_i = float(row["initial_q_over_H"])
        if q_i >= args.high_q_min:
            by_mode.setdefault(q_i, []).append(row)
    require("high-q transfer modes present", len(by_mode) > 0)
    for q_i, series in by_mode.items():
        series.sort(key=lambda r: r["t"])

    # Largest high-q label for the two-time Green (stays high-q longer on FRW).
    primary_q0 = max(by_mode.keys())
    primary_series = by_mode[primary_q0]

    t0 = traj[0]
    a0 = t0["a"]
    h0 = t0["H"]

    # Multi-slice kernel samples for each high-q comoving label
    slice_idx = subsample_indices(len(traj), args.n_slices)
    multi_slice_rows: list[dict[str, Any]] = []
    for q_label in sorted(by_mode.keys()):
        # fixed comoving k from initial q_phys = q_label * H0 at a=a0
        k_comov = q_label * h0 * a0
        for i in slice_idx:
            row = traj[i]
            q_phys = k_comov / row["a"]
            q_over_h = q_phys / row["H"]
            high_q_local = q_over_h >= args.high_q_min
            lookup = nearest_kernel(kernel_table, q_over_h, args.prefer_mode_pair)
            rec: dict[str, Any] = {
                "t": row["t"],
                "a": row["a"],
                "H": row["H"],
                "rho": row["rho"],
                "initial_q_over_H_label": q_label,
                "q_phys_over_H": q_over_h,
                "high_q_local": high_q_local,
            }
            if lookup is None or not high_q_local:
                rec.update(
                    {
                        "kernel_lookup_ok": False,
                        "kernel_q_ref": float("nan"),
                        "kernel_real": float("nan"),
                        "kernel_abs": float("nan"),
                        "kernel_mode": "",
                        "kernel_q_rel_error": float("nan"),
                    }
                )
            else:
                q_ref, k_real, k_abs, mode, rel = lookup
                rec.update(
                    {
                        "kernel_lookup_ok": True,
                        "kernel_q_ref": q_ref,
                        "kernel_real": k_real,
                        "kernel_abs": k_abs,
                        "kernel_mode": mode,
                        "kernel_q_rel_error": rel,
                    }
                )
            multi_slice_rows.append(rec)

    hits = [
        r
        for r in multi_slice_rows
        if r["kernel_lookup_ok"]
        and r["high_q_local"]
        and math.isfinite(float(r["kernel_abs"]))
    ]
    require(
        f"enough high-q multi-slice hits (>={args.min_slice_hits})",
        len(hits) >= args.min_slice_hits,
    )

    # Kernel variation diagnostics across hits
    k_abs_vals = np.array([float(r["kernel_abs"]) for r in hits], dtype=float)
    k_rel_span = float(
        (k_abs_vals.max() - k_abs_vals.min()) / max(k_abs_vals.max(), 1.0e-30)
    )

    # Restrict Green grid to times where the primary mode remains high-q local
    def q_over_h_at_series_index(index: int) -> float:
        t = primary_series[index]["t"]
        j = min(range(len(traj)), key=lambda i: abs(traj[i]["t"] - t))
        row = traj[j]
        k_comov = primary_q0 * h0 * a0
        return (k_comov / row["a"]) / row["H"]

    admissible_idx = [
        i
        for i in range(len(primary_series))
        if q_over_h_at_series_index(i) >= args.high_q_min
    ]
    require("primary mode has high-q time support", len(admissible_idx) >= 3)
    g_pick = subsample_indices(len(admissible_idx), min(args.green_grid, len(admissible_idx)))
    g_idx = [admissible_idx[i] for i in g_pick]
    g_times = [primary_series[i]["t"] for i in g_idx]

    def sv_at(index: int) -> float:
        return float(primary_series[index]["largest_normalized_singular_value"])

    def kernel_at_time(t: float) -> tuple[float, float, bool]:
        j = min(range(len(traj)), key=lambda i: abs(traj[i]["t"] - t))
        row = traj[j]
        k_comov = primary_q0 * h0 * a0
        q_over_h = (k_comov / row["a"]) / row["H"]
        lookup = nearest_kernel(kernel_table, q_over_h, args.prefer_mode_pair)
        if lookup is None or q_over_h < args.high_q_min:
            return float("nan"), q_over_h, False
        return lookup[2], q_over_h, True

    green_entries: list[dict[str, Any]] = []
    green_matrix = np.zeros((len(g_idx), len(g_idx)), dtype=float)
    for io, i_out in enumerate(g_idx):
        for ii, i_in in enumerate(g_idx):
            t_out = primary_series[i_out]["t"]
            t_in = primary_series[i_in]["t"]
            if t_out + 1.0e-15 < t_in:
                g_val = 0.0
                k_in = float("nan")
                q_in = float("nan")
                ok = True
            else:
                sv_out = sv_at(i_out)
                sv_in = sv_at(i_in)
                k_in, q_in, ok = kernel_at_time(t_in)
                if abs(sv_in) < 1.0e-300 or not math.isfinite(sv_in):
                    t_ratio = float("nan")
                else:
                    t_ratio = sv_out / sv_in
                g_val = (
                    k_in * t_ratio if ok and math.isfinite(t_ratio) else float("nan")
                )
            green_matrix[io, ii] = g_val if math.isfinite(g_val) else 0.0
            green_entries.append(
                {
                    "t_out": t_out,
                    "t_in": t_in,
                    "G_mp": g_val,
                    "causal_zero": bool(t_out + 1.0e-15 < t_in),
                    "kernel_abs_at_tin": k_in,
                    "q_phys_over_H_at_tin": q_in,
                    "kernel_lookup_ok": ok if t_out >= t_in else True,
                    "sv_out": sv_at(i_out),
                    "sv_in": sv_at(i_in),
                    "mode_initial_q_over_H": primary_q0,
                }
            )

    # Pass checks
    finite_hits = all(math.isfinite(float(r["kernel_abs"])) for r in hits)
    green_ok = all(
        (e["causal_zero"] and e["G_mp"] == 0.0)
        or (math.isfinite(float(e["G_mp"])) and e["kernel_lookup_ok"])
        for e in green_entries
    )
    # Diagonal of Green should match local K when SV ratio = 1
    diag_ok = True
    for i, gi in enumerate(g_idx):
        t = primary_series[gi]["t"]
        k_in, _, ok = kernel_at_time(t)
        g_diag = float(green_matrix[i, i])
        if not (ok and math.isfinite(k_in) and math.isfinite(g_diag)):
            diag_ok = False
            continue
        # Floating SV ratio at equal times is exactly 1 by construction
        if abs(g_diag - k_in) > 1.0e-8 * max(1.0, abs(k_in)):
            diag_ok = False

    passed = (
        finite_hits
        and len(hits) >= args.min_slice_hits
        and green_ok
        and diag_ok
        and len(by_mode) > 0
    )
    status = (
        "PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN"
        if passed
        else "FAIL_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN"
    )

    # Representative G_proxy update: O * endpoint SV of primary mode
    sv_end = sv_at(len(primary_series) - 1)
    g_proxy_mp = o_abs * abs(sv_end)

    summary = {
        "gate": "UVIR-003",
        "stage": "B_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN",
        "calculation_status": "PASS" if passed else "FAIL",
        "subgate_status": status,
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "physical_2_to_2_status": (
            "MULTI_SLICE_GREEN_PROXY_ESTABLISHED_FULL_IN_IN_NOT_COMPUTED"
        ),
        "definition": {
            "multi_slice_kernel": (
                "nearest-neighbour exchange_plus_reduced_contact at "
                "q_phys(t)/H(t) for fixed-comoving high-q labels"
            ),
            "mode_projected_two_time_green": (
                "G_mp(t_out,t_in) = K_nn(q(t_in)) * SV(t_out)/SV(t_in) "
                "for t_out>=t_in; 0 otherwise"
            ),
            "SV": "largest_normalized_singular_value of fixed-comoving transfer",
            "not_a_cross_section": True,
            "not_an_s_matrix": True,
            "not_a_unitarity_bound": True,
            "full_in_in_time_integrals": "NOT_COMPUTED",
            "nonzero_gradient_grad_pi_cubed": "HELD",
        },
        "dependencies": {
            "frw_background_status": frw_sum.get("background_status"),
            "kernel_subgate": kernel_sum.get("subgate_status"),
            "packet_subgate": packet.get("subgate_status"),
            "transfer_calculation_status": transfer_sum.get("calculation_status"),
            "exchange_domain_subgate": domain.get("subgate_status"),
            "admitted_external_q_over_H": domain.get("sampled_domain", {}).get(
                "admitted_initial_q_over_H_values", []
            ),
        },
        "parameters": {
            "high_q_min": args.high_q_min,
            "n_slices_requested": args.n_slices,
            "green_grid": args.green_grid,
            "prefer_mode_pair": args.prefer_mode_pair,
            "primary_mode_initial_q_over_H": primary_q0,
            "high_q_mode_labels": sorted(by_mode.keys()),
            "packet_q0_over_H": q0_packet,
            "packet_O_abs": o_abs,
        },
        "multi_slice": {
            "total_records": len(multi_slice_rows),
            "high_q_finite_hits": len(hits),
            "kernel_abs_min": float(k_abs_vals.min()),
            "kernel_abs_max": float(k_abs_vals.max()),
            "kernel_abs_median": float(np.median(k_abs_vals)),
            "kernel_abs_relative_span": k_rel_span,
            "max_kernel_q_rel_error": float(
                max(float(r["kernel_q_rel_error"]) for r in hits)
            ),
        },
        "mode_projected_green": {
            "times": g_times,
            "matrix_G_mp": green_matrix.tolist(),
            "diagonal_matches_local_kernel": diag_ok,
            "causal_structure": "strictly_upper_zero_for_t_out_lt_t_in",
            "G_proxy_abs_diagnostic": g_proxy_mp,
            "formula_G_proxy_diagnostic": "abs(O[sigma]) * abs(SV_endpoint primary high-q)",
        },
        "scientific_boundary": (
            "Promotes the declared FRW in-in path by (i) sampling the local "
            "four-leg kernel across multiple FRW slices in the high-q domain and "
            "(ii) assembling a causal mode-projected two-time Green proxy from "
            "existing transfer singular values. Does not evaluate nested in-in "
            "interaction integrals, does not establish unitarity, does not open "
            "the nonzero-gradient |grad(pi)|^3 sector, and does not unlock MAT-001."
        ),
        "next_required_calculation": [
            "nonzero-gradient |grad(pi)|^3 sector on a declared background",
            "optional: denser multi-slice kernel recompute (not NN lookup) at FRW-local backgrounds",
            "only then declared perturbative-unitarity / EFT-validity criterion",
        ],
        "diagnostics": {
            "finite_hits": finite_hits,
            "green_ok": green_ok,
            "diag_ok": diag_ok,
            "high_q_mode_count": len(by_mode),
        },
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_json = args.output_dir / "uvir003_frw_multi_slice_mode_green_summary.json"
    out_slices = args.output_dir / "uvir003_frw_multi_slice_kernel.csv"
    out_green = args.output_dir / "uvir003_frw_mode_projected_green.csv"

    with out_json.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    with out_slices.open("w", newline="", encoding="utf-8") as handle:
        fields = list(multi_slice_rows[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(multi_slice_rows)

    with out_green.open("w", newline="", encoding="utf-8") as handle:
        fields = list(green_entries[0].keys())
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(green_entries)

    print(f"High-q transfer modes: {sorted(by_mode.keys())}")
    print(f"Primary mode initial q/H: {primary_q0}")
    print(f"Multi-slice high-q kernel hits: {len(hits)} / {len(multi_slice_rows)}")
    print(
        f"K|abs| span: {float(k_abs_vals.min()):.6e} .. {float(k_abs_vals.max()):.6e} "
        f"(rel {k_rel_span:.3f})"
    )
    print(f"Green grid: {len(g_idx)} x {len(g_idx)}  diag_ok={diag_ok}")
    print(f"G_proxy abs diagnostic (O*SV_end): {g_proxy_mp:.6e}")
    print("Full in-in time integrals: NOT_COMPUTED")
    print("|grad(pi)|^3: HELD")
    print("S-matrix: NOT_ESTABLISHED")
    print("Unitarity: NOT_ESTABLISHED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print(f"STATUS: {status}")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
