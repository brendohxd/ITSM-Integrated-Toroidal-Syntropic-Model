#!/usr/bin/env python3
"""CBR-001 Stage 2: scan the biaxial rectangular-T^3 Casimir stress.

The validated Stage-1 lattice engine is evaluated for

    L1 = Lp,  L2 = L3 = Lt,  r = Lt / Lp

over a configurable aspect-ratio interval. Each observable is extrapolated to
N -> infinity with the same inverse-cutoff polynomial used in Stage 1.

Outputs:
    cbr001_stage2_scan.csv
    cbr001_stage2_stress.png
    cbr001_stage2_anisotropy.png

The default scan uses hbar*c = 1, Lp = 1, 61 logarithmically spaced points,
and 0.25 <= r <= 4. The cubic point r = 1 is always included.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from casimir_t3_lattice import extrapolate_to_infinity, lattice_stress


DEFAULT_CUTOFFS = (20, 30, 40, 60, 80, 120)


@dataclass(frozen=True)
class ScanRow:
    r: float
    Lp: float
    Lt: float
    rho: float
    p_p: float
    p_t: float
    delta_p: float
    trace: float
    pt_split: float
    rho_fit_rms: float
    pp_fit_rms: float
    pt_fit_rms: float

    @property
    def w_p(self) -> float:
        return self.p_p / self.rho

    @property
    def w_t(self) -> float:
        return self.p_t / self.rho


def _fit_limit(
    cutoffs: Sequence[int], values: Sequence[float], order: int
) -> tuple[float, float]:
    """Return the infinite-cutoff limit and RMS residual of the fit."""
    limit, coefficients = extrapolate_to_infinity(cutoffs, values, order=order)
    n = np.asarray(cutoffs, dtype=float)
    fitted = np.zeros_like(n)
    for power, coefficient in enumerate(coefficients):
        fitted += coefficient * (1.0 / n) ** power
    residual_rms = float(np.sqrt(np.mean((np.asarray(values) - fitted) ** 2)))
    return limit, residual_rms


def make_r_values(
    r_min: float, r_max: float, points: int, spacing: str
) -> np.ndarray:
    if not np.isfinite(r_min) or not np.isfinite(r_max):
        raise ValueError("r-min and r-max must be finite")
    if r_min <= 0.0 or r_max <= r_min:
        raise ValueError("Require 0 < r-min < r-max")
    if points < 3:
        raise ValueError("At least three scan points are required")

    if spacing == "log":
        values = np.geomspace(r_min, r_max, points)
    else:
        values = np.linspace(r_min, r_max, points)

    if r_min <= 1.0 <= r_max:
        values = np.append(values, 1.0)
    values = np.unique(values)
    values.sort()
    return values


def evaluate_ratio(
    r: float, Lp: float, cutoffs: Sequence[int], fit_order: int
) -> ScanRow:
    Lt = Lp * r
    results = [lattice_stress((Lp, Lt, Lt), cutoff) for cutoff in cutoffs]

    rho, rho_rms = _fit_limit(cutoffs, [item.rho for item in results], fit_order)
    p_p, pp_rms = _fit_limit(cutoffs, [item.p1 for item in results], fit_order)
    p2, p2_rms = _fit_limit(cutoffs, [item.p2 for item in results], fit_order)
    p3, p3_rms = _fit_limit(cutoffs, [item.p3 for item in results], fit_order)

    p_t = 0.5 * (p2 + p3)
    trace = -rho + p_p + 2.0 * p_t
    return ScanRow(
        r=r,
        Lp=Lp,
        Lt=Lt,
        rho=rho,
        p_p=p_p,
        p_t=p_t,
        delta_p=p_t - p_p,
        trace=trace,
        pt_split=abs(p2 - p3),
        rho_fit_rms=rho_rms,
        pp_fit_rms=pp_rms,
        pt_fit_rms=max(p2_rms, p3_rms),
    )


def write_scan_csv(path: Path, rows: Sequence[ScanRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "r",
                "Lp",
                "Lt",
                "rho",
                "p_p",
                "p_t",
                "p_t_minus_p_p",
                "trace",
                "p2_p3_abs_split",
                "w_p",
                "w_t",
                "rho_fit_rms",
                "p_p_fit_rms",
                "p_t_fit_rms",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    f"{row.r:.17g}",
                    f"{row.Lp:.17g}",
                    f"{row.Lt:.17g}",
                    f"{row.rho:.17g}",
                    f"{row.p_p:.17g}",
                    f"{row.p_t:.17g}",
                    f"{row.delta_p:.17g}",
                    f"{row.trace:.17g}",
                    f"{row.pt_split:.17g}",
                    f"{row.w_p:.17g}",
                    f"{row.w_t:.17g}",
                    f"{row.rho_fit_rms:.17g}",
                    f"{row.pp_fit_rms:.17g}",
                    f"{row.pt_fit_rms:.17g}",
                ]
            )


def plot_stress(path: Path, rows: Sequence[ScanRow]) -> None:
    r = np.array([row.r for row in rows])
    fig, ax = plt.subplots(figsize=(8.5, 5.5), constrained_layout=True)
    ax.plot(r, [row.rho for row in rows], label=r"$\rho$", linewidth=2.2)
    ax.plot(r, [row.p_p for row in rows], label=r"$p_p$", linewidth=2.0)
    ax.plot(r, [row.p_t for row in rows], label=r"$p_t$", linewidth=2.0)
    ax.axhline(0.0, color="black", linewidth=0.8, alpha=0.6)
    ax.axvline(1.0, color="0.4", linestyle="--", linewidth=1.0)
    ax.set_xscale("log", base=2)
    ax.set_xlabel(r"Aspect ratio $r=L_t/L_p$")
    ax.set_ylabel(r"Dimensionless stress ($\hbar c=1$, $L_p=1$)")
    ax.set_title(r"CBR-001 Stage 2: biaxial rectangular-$T^3$ stress")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_anisotropy(path: Path, rows: Sequence[ScanRow]) -> None:
    r = np.array([row.r for row in rows])
    fig, (top, bottom) = plt.subplots(
        2, 1, figsize=(8.5, 8.0), sharex=True, constrained_layout=True
    )

    top.plot(r, [row.delta_p for row in rows], color="tab:purple", linewidth=2.2)
    top.axhline(0.0, color="black", linewidth=0.8)
    top.axvline(1.0, color="0.4", linestyle="--", linewidth=1.0)
    top.set_ylabel(r"$\Delta p=p_t-p_p$")
    top.set_title("Directional pressure anisotropy")
    top.grid(True, which="both", alpha=0.25)

    bottom.plot(r, [row.w_p for row in rows], label=r"$w_p=p_p/\rho$")
    bottom.plot(r, [row.w_t for row in rows], label=r"$w_t=p_t/\rho$")
    bottom.axhline(1.0 / 3.0, color="black", linestyle=":", linewidth=1.0)
    bottom.axvline(1.0, color="0.4", linestyle="--", linewidth=1.0)
    bottom.set_xscale("log", base=2)
    bottom.set_xlabel(r"Aspect ratio $r=L_t/L_p$")
    bottom.set_ylabel("Directional equation-of-state ratio")
    bottom.grid(True, which="both", alpha=0.25)
    bottom.legend()

    fig.savefig(path, dpi=180)
    plt.close(fig)


def validate_scan(rows: Sequence[ScanRow]) -> tuple[bool, list[str]]:
    messages: list[str] = []
    cube = min(rows, key=lambda row: abs(row.r - 1.0))
    cube_isotropy = abs(cube.p_p - cube.p_t)
    cube_eos = max(abs(cube.p_p - cube.rho / 3.0), abs(cube.p_t - cube.rho / 3.0))
    max_trace = max(abs(row.trace) for row in rows)
    max_pt_split = max(row.pt_split for row in rows)
    finite = all(
        np.isfinite(value)
        for row in rows
        for value in (
            row.rho,
            row.p_p,
            row.p_t,
            row.delta_p,
            row.trace,
        )
    )
    shape_response = max(abs(row.delta_p) for row in rows)

    messages.append(f"cube isotropy error = {cube_isotropy:.3e}")
    messages.append(f"cube rho/3 error   = {cube_eos:.3e}")
    messages.append(f"max trace residual = {max_trace:.3e}")
    messages.append(f"max p2-p3 split    = {max_pt_split:.3e}")
    messages.append(f"max |delta p|      = {shape_response:.3e}")

    passed = all(
        [
            finite,
            abs(cube.r - 1.0) < 1.0e-14,
            cube_isotropy < 1.0e-9,
            cube_eos < 1.0e-9,
            max_trace < 1.0e-9,
            max_pt_split < 1.0e-9,
            shape_response > 1.0e-6,
        ]
    )
    return passed, messages


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan the biaxial rectangular-T^3 Casimir stress over r=Lt/Lp."
    )
    parser.add_argument("--r-min", type=float, default=0.25)
    parser.add_argument("--r-max", type=float, default=4.0)
    parser.add_argument("--points", type=int, default=61)
    parser.add_argument("--spacing", choices=("log", "linear"), default="log")
    parser.add_argument("--lp", type=float, default=1.0)
    parser.add_argument("--cutoffs", nargs="+", type=int, default=DEFAULT_CUTOFFS)
    parser.add_argument("--fit-order", type=int, choices=(1, 2, 3), default=2)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    parser.add_argument("--prefix", default="cbr001_stage2")
    args = parser.parse_args()

    if not np.isfinite(args.lp) or args.lp <= 0.0:
        raise ValueError("lp must be finite and positive")
    cutoffs = sorted(set(args.cutoffs))
    if any(cutoff < 1 for cutoff in cutoffs):
        raise ValueError("All cutoffs must be positive")
    if len(cutoffs) < args.fit_order + 2:
        raise ValueError("Not enough cutoffs for the requested fit order")

    r_values = make_r_values(args.r_min, args.r_max, args.points, args.spacing)
    print("CBR-001 Stage 2 — biaxial rectangular-T^3 shape scan")
    print(
        f"Lp={args.lp:g}, r=[{r_values[0]:g}, {r_values[-1]:g}], "
        f"points={len(r_values)}, cutoffs={cutoffs}"
    )

    rows: list[ScanRow] = []
    for index, r in enumerate(r_values, start=1):
        row = evaluate_ratio(float(r), args.lp, cutoffs, args.fit_order)
        rows.append(row)
        print(
            f"[{index:3d}/{len(r_values):3d}] r={r:9.6f} "
            f"rho={row.rho: .8e} pp={row.p_p: .8e} "
            f"pt={row.p_t: .8e} delta={row.delta_p: .8e}"
        )

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"{args.prefix}_scan.csv"
    stress_path = output_dir / f"{args.prefix}_stress.png"
    anisotropy_path = output_dir / f"{args.prefix}_anisotropy.png"

    write_scan_csv(csv_path, rows)
    plot_stress(stress_path, rows)
    plot_anisotropy(anisotropy_path, rows)

    passed, messages = validate_scan(rows)
    print()
    print("Validation:")
    for message in messages:
        print(f"  {message}")
    print()
    print(f"CSV:             {csv_path}")
    print(f"Stress plot:     {stress_path}")
    print(f"Anisotropy plot: {anisotropy_path}")
    print(f"STATUS: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
