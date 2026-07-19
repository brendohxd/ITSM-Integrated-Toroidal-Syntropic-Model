#!/usr/bin/env python3
"""
CBR-001 Stage 1: Rectangular T^3 Casimir lattice-sum solver.

Massless real scalar field with periodic boundary conditions on a rectangular
three-torus. The calculation is performed in dimensionless units hbar*c = 1.

For side lengths L = (L1, L2, L3), define
    R_n^2 = (n1 L1)^2 + (n2 L2)^2 + (n3 L3)^2.

The renormalized Casimir energy density is evaluated as
    rho = -(1 / (2 pi^2)) * sum_{n in Z^3, n != 0} R_n^{-4}.

Directional pressures follow from
    p_i = -(1 / A_i) dE/dL_i
and are evaluated analytically as
    p_i = (1 / (2 pi^2)) *
          [S4 - 4 L_i^2 sum_n n_i^2 R_n^{-6}].

The direct cube cutoff converges as a power series in 1/N. The script evaluates
several cutoffs and extrapolates each observable to N -> infinity.

Usage:
    python casimir_t3_lattice.py
    python casimir_t3_lattice.py --lengths 1 1.5 1.5
    python casimir_t3_lattice.py --cutoffs 20 30 40 60 80 120 160
    python casimir_t3_lattice.py --csv cbr001_stage1.csv

Expected cube benchmark:
    rho * L^4 / (hbar*c) ~= -0.83753691
    p1 = p2 = p3 = rho / 3
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np


PREFAC = 1.0 / (2.0 * np.pi**2)
CUBE_RHO_BENCHMARK = -0.83753691


@dataclass(frozen=True)
class StressResult:
    cutoff: int
    lengths: tuple[float, float, float]
    rho: float
    p1: float
    p2: float
    p3: float
    energy: float

    @property
    def pressures(self) -> np.ndarray:
        return np.array([self.p1, self.p2, self.p3], dtype=float)

    @property
    def trace(self) -> float:
        # Mixed-index trace for diag(-rho, p1, p2, p3).
        return -self.rho + self.p1 + self.p2 + self.p3


def _validate_lengths(lengths: Sequence[float]) -> tuple[float, float, float]:
    if len(lengths) != 3:
        raise ValueError("Exactly three side lengths are required.")
    values = tuple(float(x) for x in lengths)
    if not all(np.isfinite(x) and x > 0.0 for x in values):
        raise ValueError("All side lengths must be finite and positive.")
    return values  # type: ignore[return-value]


def lattice_stress(
    lengths: Sequence[float],
    cutoff: int,
) -> StressResult:
    """
    Evaluate rho and directional pressures using a symmetric integer cube
    n_i in [-N, N], excluding the zero mode.

    The implementation loops over n1 and vectorizes the n2-n3 plane, avoiding
    allocation of the full three-dimensional lattice.
    """
    if cutoff < 1:
        raise ValueError("cutoff must be at least 1")

    L1, L2, L3 = _validate_lengths(lengths)
    N = int(cutoff)

    axis = np.arange(-N, N + 1, dtype=np.float64)
    n2, n3 = np.meshgrid(axis, axis, indexing="ij")
    transverse_r2 = (n2 * L2) ** 2 + (n3 * L3) ** 2

    s4 = 0.0
    q1 = 0.0
    q2 = 0.0
    q3 = 0.0

    for n1_int in range(-N, N + 1):
        n1 = float(n1_int)
        r2 = (n1 * L1) ** 2 + transverse_r2
        mask = r2 > 0.0

        r2_nonzero = r2[mask]
        inv_r4 = r2_nonzero ** -2
        inv_r6 = r2_nonzero ** -3

        s4 += float(np.sum(inv_r4))
        q1 += float(np.sum((n1 * n1) * inv_r6))
        q2 += float(np.sum((n2[mask] ** 2) * inv_r6))
        q3 += float(np.sum((n3[mask] ** 2) * inv_r6))

    rho = -PREFAC * s4
    p1 = PREFAC * (s4 - 4.0 * L1 * L1 * q1)
    p2 = PREFAC * (s4 - 4.0 * L2 * L2 * q2)
    p3 = PREFAC * (s4 - 4.0 * L3 * L3 * q3)
    volume = L1 * L2 * L3

    return StressResult(
        cutoff=N,
        lengths=(L1, L2, L3),
        rho=rho,
        p1=p1,
        p2=p2,
        p3=p3,
        energy=volume * rho,
    )


def extrapolate_to_infinity(
    cutoffs: Sequence[int],
    values: Sequence[float],
    order: int = 2,
) -> tuple[float, np.ndarray]:
    """
    Fit y(N) = y_inf + a1/N + ... + a_order/N^order.

    Returns y_inf and the full coefficient vector.
    """
    n = np.asarray(cutoffs, dtype=float)
    y = np.asarray(values, dtype=float)

    if len(n) != len(y):
        raise ValueError("cutoffs and values must have the same length")
    if len(n) < order + 2:
        raise ValueError(
            f"At least {order + 2} cutoff values are required for order {order}."
        )

    columns = [np.ones_like(n)]
    columns.extend((1.0 / n) ** power for power in range(1, order + 1))
    design = np.column_stack(columns)
    coefficients, *_ = np.linalg.lstsq(design, y, rcond=None)
    return float(coefficients[0]), coefficients


def finite_difference_pressures(
    lengths: Sequence[float],
    cutoff: int,
    relative_step: float = 1.0e-5,
) -> np.ndarray:
    """Check p_i = -(1/A_i) dE/dL_i by central finite differences."""
    base = np.asarray(_validate_lengths(lengths), dtype=float)
    volume = float(np.prod(base))
    pressures = np.empty(3, dtype=float)

    for i in range(3):
        step = relative_step * base[i]
        plus = base.copy()
        minus = base.copy()
        plus[i] += step
        minus[i] -= step

        e_plus = lattice_stress(plus, cutoff).energy
        e_minus = lattice_stress(minus, cutoff).energy
        derivative = (e_plus - e_minus) / (2.0 * step)

        area_i = volume / base[i]
        pressures[i] = -derivative / area_i

    return pressures


def scaling_test(
    lengths: Sequence[float],
    cutoff: int,
    scale: float = 1.7,
) -> dict[str, float]:
    """
    Verify rho(lambda L) = lambda^-4 rho(L),
    p_i(lambda L) = lambda^-4 p_i(L), and E(lambda L)=lambda^-1 E(L).
    """
    base = lattice_stress(lengths, cutoff)
    scaled_lengths = tuple(scale * x for x in base.lengths)
    scaled = lattice_stress(scaled_lengths, cutoff)

    rho_error = abs(scaled.rho * scale**4 / base.rho - 1.0)
    pressure_error = float(
        np.max(np.abs(scaled.pressures * scale**4 / base.pressures - 1.0))
    )
    energy_error = abs(scaled.energy * scale / base.energy - 1.0)

    return {
        "rho_relative_error": float(rho_error),
        "pressure_max_relative_error": pressure_error,
        "energy_relative_error": float(energy_error),
    }


def permutation_test(lengths: Sequence[float], cutoff: int) -> float:
    """Swap L1 and L2 and verify that p1 and p2 swap with them."""
    L1, L2, L3 = _validate_lengths(lengths)
    original = lattice_stress((L1, L2, L3), cutoff)
    swapped = lattice_stress((L2, L1, L3), cutoff)

    expected = np.array([original.p2, original.p1, original.p3])
    return float(np.max(np.abs(swapped.pressures - expected)))


def write_csv(path: Path, results: Iterable[StressResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["cutoff", "L1", "L2", "L3", "rho", "p1", "p2", "p3", "trace", "energy"]
        )
        for result in results:
            writer.writerow(
                [
                    result.cutoff,
                    *result.lengths,
                    result.rho,
                    result.p1,
                    result.p2,
                    result.p3,
                    result.trace,
                    result.energy,
                ]
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rectangular T^3 Casimir lattice-sum solver and validation suite."
    )
    parser.add_argument(
        "--lengths",
        nargs=3,
        type=float,
        default=(1.0, 1.0, 1.0),
        metavar=("L1", "L2", "L3"),
    )
    parser.add_argument(
        "--cutoffs",
        nargs="+",
        type=int,
        default=(20, 30, 40, 60, 80, 120),
    )
    parser.add_argument(
        "--fit-order",
        type=int,
        choices=(1, 2, 3),
        default=2,
    )
    parser.add_argument(
        "--fd-step",
        type=float,
        default=1.0e-5,
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("cbr001_stage1.csv"),
    )
    args = parser.parse_args()

    lengths = _validate_lengths(args.lengths)
    cutoffs = sorted(set(args.cutoffs))
    if any(n < 1 for n in cutoffs):
        raise ValueError("All cutoffs must be positive.")

    print("CBR-001 Stage 1 — rectangular T^3 Casimir stress")
    print(f"Lengths: L1={lengths[0]:.8g}, L2={lengths[1]:.8g}, L3={lengths[2]:.8g}")
    print()
    print(
        f"{'N':>6} {'rho':>16} {'p1':>16} {'p2':>16} "
        f"{'p3':>16} {'trace':>13}"
    )

    results: list[StressResult] = []
    for cutoff in cutoffs:
        result = lattice_stress(lengths, cutoff)
        results.append(result)
        print(
            f"{cutoff:6d} {result.rho:16.10f} {result.p1:16.10f} "
            f"{result.p2:16.10f} {result.p3:16.10f} "
            f"{result.trace:13.3e}"
        )

    observables = {
        "rho": [r.rho for r in results],
        "p1": [r.p1 for r in results],
        "p2": [r.p2 for r in results],
        "p3": [r.p3 for r in results],
    }
    extrapolated: dict[str, float] = {}
    for name, values in observables.items():
        limit, _ = extrapolate_to_infinity(
            cutoffs, values, order=args.fit_order
        )
        extrapolated[name] = limit

    print()
    print(f"N -> infinity extrapolation (order {args.fit_order} in 1/N):")
    for name in ("rho", "p1", "p2", "p3"):
        print(f"  {name:>3} = {extrapolated[name]: .12f}")

    finest = results[-1]
    fd_pressures = finite_difference_pressures(
        lengths, finest.cutoff, relative_step=args.fd_step
    )
    fd_relative = np.abs(
        (fd_pressures - finest.pressures)
        / np.maximum(np.abs(finest.pressures), 1.0e-30)
    )

    print()
    print(f"Validation at N={finest.cutoff}:")
    print(f"  analytic pressures    = {finest.pressures}")
    print(f"  finite-difference p_i = {fd_pressures}")
    print(f"  max FD relative error = {np.max(fd_relative):.3e}")
    print(f"  conformal trace       = {finest.trace:.3e}")
    print(f"  permutation abs error = {permutation_test(lengths, finest.cutoff):.3e}")

    scale_errors = scaling_test(lengths, finest.cutoff)
    print(
        "  scaling errors        = "
        f"rho {scale_errors['rho_relative_error']:.3e}, "
        f"p {scale_errors['pressure_max_relative_error']:.3e}, "
        f"E {scale_errors['energy_relative_error']:.3e}"
    )

    cube = np.allclose(lengths, (1.0, 1.0, 1.0), rtol=0.0, atol=1.0e-14)
    if cube:
        cube_error = abs(extrapolated["rho"] - CUBE_RHO_BENCHMARK)
        isotropy_error = max(
            abs(extrapolated["p1"] - extrapolated["rho"] / 3.0),
            abs(extrapolated["p2"] - extrapolated["rho"] / 3.0),
            abs(extrapolated["p3"] - extrapolated["rho"] / 3.0),
        )
        print(f"  cube rho benchmark err= {cube_error:.3e}")
        print(f"  cube isotropy error   = {isotropy_error:.3e}")

    write_csv(args.csv, results)
    print()
    print(f"Saved cutoff ledger to: {args.csv.resolve()}")

    # Conservative pass/fail thresholds for the validation run.
    checks = [
        abs(finest.trace) < 1.0e-10,
        np.max(fd_relative) < 1.0e-6,
        permutation_test(lengths, finest.cutoff) < 1.0e-10,
        scale_errors["rho_relative_error"] < 1.0e-10,
        scale_errors["pressure_max_relative_error"] < 1.0e-10,
        scale_errors["energy_relative_error"] < 1.0e-10,
    ]
    if cube:
        checks.extend(
            [
                abs(extrapolated["rho"] - CUBE_RHO_BENCHMARK) < 5.0e-5,
                isotropy_error < 1.0e-10,
            ]
        )

    if all(checks):
        print("STATUS: PASS")
        return 0

    print("STATUS: FAIL — inspect the validation diagnostics above.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

