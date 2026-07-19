#!/usr/bin/env python3
"""CBR-001 Stage 3A: validated biaxial cosmological backreaction.

The solver treats the rectangular-T^3 Casimir tensor as a perturbative source
on a positive de Sitter background. It does not search for 13/12.

Dimensionless conventions:
    H_bg = 1
    kappa = 1
    rho_bg = 3
    hbar*c/L_*^4 is absorbed into epsilon

The independent variable is the mean e-fold N = ln(a). The evolved variables
are ln(r) and delta = H_t - H_p; H is recovered from the Hamiltonian
constraint at every right-hand-side evaluation.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator


H_BG = 1.0
KAPPA = 1.0
RHO_BG = 3.0 * H_BG**2 / KAPPA
DEFAULT_R0 = (0.5, 1.0, 2.0)
DEFAULT_EPSILON = (0.0, 1.0e-8, 1.0e-6, 1.0e-4)


@dataclass(frozen=True)
class CasimirState:
    rho: np.ndarray
    p_p: np.ndarray
    p_t: np.ndarray
    delta_p: np.ndarray
    u_x: np.ndarray


@dataclass(frozen=True)
class RunResult:
    r0: float
    epsilon: float
    N: np.ndarray
    a: np.ndarray
    r: np.ndarray
    delta: np.ndarray
    rho_C: np.ndarray
    p_p_C: np.ndarray
    p_t_C: np.ndarray
    delta_p: np.ndarray
    H: np.ndarray
    H_p: np.ndarray
    H_t: np.ndarray
    H_t_over_H_p: np.ndarray
    delta_over_H: np.ndarray
    casimir_fraction: np.ndarray
    constraint_residual: np.ndarray
    continuity_residual: np.ndarray


class CasimirInterpolator:
    """Thermodynamically consistent PCHIP representation of Stage-2 data.

    At fixed mean scale a=1, define

        u(x) = r^(8/3) rho_hat(r),  x = ln(r).

    Conservation requires d u/dx = -(2/3) Delta p. We therefore construct a
    shape-preserving PCHIP for the Stage-2 fixed-volume pressure anisotropy and
    integrate it, anchoring u at the cubic data point. Directional pressures
    then follow from the trace relation. This reproduces all three Stage-2
    columns while preserving continuity between tabulated points.
    """

    def __init__(self, csv_path: Path) -> None:
        data = np.genfromtxt(csv_path, delimiter=",", names=True)
        required = {"r", "rho", "p_p", "p_t"}
        if data.dtype.names is None or not required.issubset(data.dtype.names):
            raise ValueError(f"Stage-2 CSV is missing columns: {sorted(required)}")

        r = np.asarray(data["r"], dtype=float)
        rho_hat = np.asarray(data["rho"], dtype=float)
        pp_hat = np.asarray(data["p_p"], dtype=float)
        pt_hat = np.asarray(data["p_t"], dtype=float)
        if np.any(~np.isfinite(r)) or np.any(np.diff(r) <= 0.0) or np.any(r <= 0.0):
            raise ValueError("Stage-2 aspect ratios must be finite, positive, and sorted")

        self.csv_path = csv_path.resolve()
        self.r_min = float(r[0])
        self.r_max = float(r[-1])
        self.x_min = float(np.log(r[0]))
        self.x_max = float(np.log(r[-1]))
        self._x = np.log(r)

        volume_shape_scale = r ** (8.0 / 3.0)
        self._u_data = volume_shape_scale * rho_hat
        self._dp_data = volume_shape_scale * (pt_hat - pp_hat)
        self._pp_data = volume_shape_scale * pp_hat
        self._pt_data = volume_shape_scale * pt_hat

        cube_index = int(np.argmin(np.abs(r - 1.0)))
        if abs(r[cube_index] - 1.0) > 1.0e-14:
            raise ValueError("Stage-2 CSV must contain the cubic point r=1")
        self._anchor_x = float(self._x[cube_index])
        self._anchor_u = float(self._u_data[cube_index])

        self._delta_p = PchipInterpolator(
            self._x, self._dp_data, extrapolate=False
        )
        self._delta_p_integral = self._delta_p.antiderivative()
        self._anchor_integral = float(self._delta_p_integral(self._anchor_x))

        reconstructed = self.evaluate(N=np.zeros_like(r), r=r)
        self.validation = {
            "rho_max_abs_error": float(
                np.max(np.abs(reconstructed.rho - self._u_data))
            ),
            "rho_global_relative_error": self._global_relative_error(
                reconstructed.rho, self._u_data
            ),
            "p_p_global_relative_error": self._global_relative_error(
                reconstructed.p_p, self._pp_data
            ),
            "p_t_global_relative_error": self._global_relative_error(
                reconstructed.p_t, self._pt_data
            ),
            "cube_delta_p": float(self.evaluate(0.0, 1.0).delta_p),
        }

    @staticmethod
    def _global_relative_error(actual: np.ndarray, reference: np.ndarray) -> float:
        scale = max(float(np.max(np.abs(reference))), 1.0e-30)
        return float(np.max(np.abs(actual - reference)) / scale)

    def _check_r(self, r: np.ndarray) -> None:
        if np.any(~np.isfinite(r)) or np.any(r < self.r_min) or np.any(r > self.r_max):
            raise ValueError(
                f"Aspect ratio left Stage-2 support [{self.r_min}, {self.r_max}]"
            )

    def evaluate(
        self, N: float | np.ndarray, r: float | np.ndarray
    ) -> CasimirState:
        r_array = np.asarray(r, dtype=float)
        N_array = np.asarray(N, dtype=float)
        self._check_r(r_array)
        x = np.log(r_array)

        delta_p_shape = np.asarray(self._delta_p(x), dtype=float)
        integral = np.asarray(self._delta_p_integral(x), dtype=float)
        u = self._anchor_u - (2.0 / 3.0) * (
            integral - self._anchor_integral
        )
        u_x = -(2.0 / 3.0) * delta_p_shape

        decay = np.exp(-4.0 * N_array)
        rho = decay * u
        delta_p = decay * delta_p_shape
        p_p = (rho - 2.0 * delta_p) / 3.0
        p_t = (rho + delta_p) / 3.0
        return CasimirState(
            rho=np.asarray(rho),
            p_p=np.asarray(p_p),
            p_t=np.asarray(p_t),
            delta_p=np.asarray(delta_p),
            u_x=np.asarray(decay * u_x),
        )


def positive_hubble(delta: np.ndarray, rho_C: np.ndarray, epsilon: float) -> np.ndarray:
    rho_total = RHO_BG + epsilon * rho_C
    radicand = (KAPPA * rho_total + delta**2 / 3.0) / 3.0
    if np.any(radicand <= 0.0) or np.any(~np.isfinite(radicand)):
        raise RuntimeError("Hamiltonian constraint has no positive expanding branch")
    return np.sqrt(radicand)


def solve_run(
    source: CasimirInterpolator,
    r0: float,
    epsilon: float,
    N_eval: np.ndarray,
    rtol: float,
    atol: float,
) -> RunResult:
    if not source.r_min <= r0 <= source.r_max:
        raise ValueError(f"r0={r0} lies outside Stage-2 interpolation support")

    def rhs(N: float, state: np.ndarray) -> np.ndarray:
        log_r, delta = state
        r = float(np.exp(log_r))
        casimir = source.evaluate(N, r)
        H = float(positive_hubble(np.asarray(delta), casimir.rho, epsilon))
        return np.array(
            [
                delta / H,
                -3.0 * delta + KAPPA * epsilon * float(casimir.delta_p) / H,
            ],
            dtype=float,
        )

    solution = solve_ivp(
        rhs,
        (float(N_eval[0]), float(N_eval[-1])),
        np.array([np.log(r0), 0.0], dtype=float),
        method="DOP853",
        t_eval=N_eval,
        rtol=rtol,
        atol=atol,
    )
    if not solution.success:
        raise RuntimeError(f"ODE integration failed: {solution.message}")

    N = solution.t
    a = np.exp(N)
    r = np.exp(solution.y[0])
    delta = solution.y[1]
    casimir = source.evaluate(N, r)
    H = positive_hubble(delta, casimir.rho, epsilon)
    H_p = H - 2.0 * delta / 3.0
    H_t = H + delta / 3.0
    rho_total = RHO_BG + epsilon * casimir.rho

    constraint_raw = 3.0 * H**2 - delta**2 / 3.0 - KAPPA * rho_total
    constraint_scale = np.maximum.reduce(
        [3.0 * H**2, np.abs(KAPPA * rho_total), np.ones_like(H)]
    )
    constraint_residual = np.abs(constraint_raw) / constraint_scale

    d_rho_dt = -4.0 * H * casimir.rho + delta * casimir.u_x
    continuity_term_p = H_p * (casimir.rho + casimir.p_p)
    continuity_term_t = 2.0 * H_t * (casimir.rho + casimir.p_t)
    continuity_raw = d_rho_dt + continuity_term_p + continuity_term_t
    continuity_scale = np.maximum.reduce(
        [
            np.abs(d_rho_dt),
            np.abs(continuity_term_p) + np.abs(continuity_term_t),
            np.abs(H * casimir.rho),
            np.full_like(H, 1.0e-30),
        ]
    )
    continuity_residual = np.abs(continuity_raw) / continuity_scale

    return RunResult(
        r0=r0,
        epsilon=epsilon,
        N=N,
        a=a,
        r=r,
        delta=delta,
        rho_C=casimir.rho,
        p_p_C=casimir.p_p,
        p_t_C=casimir.p_t,
        delta_p=casimir.delta_p,
        H=H,
        H_p=H_p,
        H_t=H_t,
        H_t_over_H_p=H_t / H_p,
        delta_over_H=delta / H,
        casimir_fraction=epsilon * casimir.rho / rho_total,
        constraint_residual=constraint_residual,
        continuity_residual=continuity_residual,
    )


def run_summary(run: RunResult) -> dict[str, float]:
    return {
        "r0": run.r0,
        "epsilon": run.epsilon,
        "final_r": float(run.r[-1]),
        "final_delta_over_H": float(run.delta_over_H[-1]),
        "final_H_t_over_H_p": float(run.H_t_over_H_p[-1]),
        "max_abs_log_shape_change": float(
            np.max(np.abs(np.log(run.r / run.r0)))
        ),
        "max_abs_delta_over_H": float(np.max(np.abs(run.delta_over_H))),
        "max_abs_casimir_fraction": float(np.max(np.abs(run.casimir_fraction))),
        "max_constraint_residual": float(np.max(run.constraint_residual)),
        "max_continuity_residual": float(np.max(run.continuity_residual)),
    }


def validate_controls(runs: Sequence[RunResult]) -> dict[str, Any]:
    zero_runs = [run for run in runs if run.epsilon == 0.0]
    zero_delta = max(float(np.max(np.abs(run.delta))) for run in zero_runs)
    zero_r = max(float(np.max(np.abs(run.r - run.r0))) for run in zero_runs)
    zero_H = max(float(np.max(np.abs(run.H - H_BG))) for run in zero_runs)
    epsilon_zero_passed = max(zero_delta, zero_r, zero_H) < 1.0e-12

    isotropic_runs = [run for run in runs if run.r0 == 1.0]
    isotropic_delta = max(
        float(np.max(np.abs(run.delta))) for run in isotropic_runs
    )
    isotropic_r = max(float(np.max(np.abs(run.r - 1.0))) for run in isotropic_runs)
    isotropic_split = max(
        float(np.max(np.abs(run.H_t - run.H_p))) for run in isotropic_runs
    )
    isotropic_passed = max(isotropic_delta, isotropic_r, isotropic_split) < 1.0e-12

    return {
        "epsilon_zero": {
            "max_abs_delta": zero_delta,
            "max_abs_r_minus_r0": zero_r,
            "max_abs_H_minus_one": zero_H,
            "passed": epsilon_zero_passed,
        },
        "isotropic_r0_one": {
            "max_abs_delta": isotropic_delta,
            "max_abs_r_minus_one": isotropic_r,
            "max_abs_Ht_minus_Hp": isotropic_split,
            "passed": isotropic_passed,
        },
    }


def analytic_benchmark(
    source: CasimirInterpolator, runs: Sequence[RunResult], epsilon: float
) -> dict[str, Any]:
    cases: list[dict[str, float]] = []
    for run in runs:
        if run.epsilon != epsilon or run.r0 == 1.0:
            continue
        delta_p0 = float(source.evaluate(0.0, run.r0).delta_p)
        S = KAPPA * epsilon * delta_p0 / H_BG**2
        expected_shear = S * (np.exp(-3.0 * run.N) - np.exp(-4.0 * run.N))
        expected_log_r = np.log(run.r0) + S * (
            (1.0 - np.exp(-3.0 * run.N)) / 3.0
            - (1.0 - np.exp(-4.0 * run.N)) / 4.0
        )

        shear_scale = max(float(np.max(np.abs(expected_shear))), 1.0e-30)
        shape_scale = max(
            float(np.max(np.abs(expected_log_r - np.log(run.r0)))), 1.0e-30
        )
        shear_error = float(
            np.max(np.abs(run.delta_over_H - expected_shear)) / shear_scale
        )
        shape_error = float(
            np.max(np.abs(np.log(run.r) - expected_log_r)) / shape_scale
        )
        cases.append(
            {
                "r0": run.r0,
                "epsilon": epsilon,
                "S": S,
                "shear_relative_error": shear_error,
                "shape_relative_error": shape_error,
            }
        )

    maximum = max(
        max(case["shear_relative_error"], case["shape_relative_error"])
        for case in cases
    )
    return {
        "epsilon": epsilon,
        "cases": cases,
        "maximum_relative_error": maximum,
        "passed": maximum < 1.0e-5,
    }


def _relative_curve_difference(
    baseline: np.ndarray, tight: np.ndarray, scale_floor: float = 1.0e-30
) -> float:
    scale = max(float(np.max(np.abs(tight))), scale_floor)
    return float(np.max(np.abs(baseline - tight)) / scale)


def tolerance_crosscheck(
    source: CasimirInterpolator,
    baseline_runs: Sequence[RunResult],
    N_eval: np.ndarray,
    epsilon: float,
    tight_rtol: float,
    tight_atol: float,
) -> dict[str, Any]:
    cases: list[dict[str, float]] = []
    selected = [
        run
        for run in baseline_runs
        if run.epsilon == epsilon and run.r0 in (0.5, 2.0)
    ]
    for baseline in selected:
        tight = solve_run(
            source,
            r0=baseline.r0,
            epsilon=baseline.epsilon,
            N_eval=N_eval,
            rtol=tight_rtol,
            atol=tight_atol,
        )
        r_error = _relative_curve_difference(baseline.r, tight.r)
        shear_error = _relative_curve_difference(
            baseline.delta_over_H, tight.delta_over_H
        )
        ratio_deviation_error = _relative_curve_difference(
            baseline.H_t_over_H_p - 1.0,
            tight.H_t_over_H_p - 1.0,
        )
        cases.append(
            {
                "r0": baseline.r0,
                "epsilon": epsilon,
                "r_relative_difference": r_error,
                "shear_relative_difference": shear_error,
                "hubble_ratio_deviation_relative_difference": ratio_deviation_error,
            }
        )

    maximum = max(max(value for key, value in case.items() if key.endswith("difference")) for case in cases)
    return {
        "epsilon": epsilon,
        "tight_rtol": tight_rtol,
        "tight_atol": tight_atol,
        "cases": cases,
        "maximum_relative_difference": maximum,
        "passed": maximum < 1.0e-6,
    }


def write_runs_csv(path: Path, runs: Sequence[RunResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "N",
        "a",
        "r",
        "rho_C",
        "p_p_C",
        "p_t_C",
        "delta_p",
        "H",
        "H_p",
        "H_t",
        "H_t_over_H_p",
        "delta_over_H",
        "casimir_fraction",
        "constraint_residual",
        "continuity_residual",
        "r0",
        "epsilon",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for run in runs:
            for index in range(len(run.N)):
                writer.writerow(
                    {
                        "N": f"{run.N[index]:.17g}",
                        "a": f"{run.a[index]:.17g}",
                        "r": f"{run.r[index]:.17g}",
                        "rho_C": f"{run.rho_C[index]:.17g}",
                        "p_p_C": f"{run.p_p_C[index]:.17g}",
                        "p_t_C": f"{run.p_t_C[index]:.17g}",
                        "delta_p": f"{run.delta_p[index]:.17g}",
                        "H": f"{run.H[index]:.17g}",
                        "H_p": f"{run.H_p[index]:.17g}",
                        "H_t": f"{run.H_t[index]:.17g}",
                        "H_t_over_H_p": f"{run.H_t_over_H_p[index]:.17g}",
                        "delta_over_H": f"{run.delta_over_H[index]:.17g}",
                        "casimir_fraction": f"{run.casimir_fraction[index]:.17g}",
                        "constraint_residual": f"{run.constraint_residual[index]:.17g}",
                        "continuity_residual": f"{run.continuity_residual[index]:.17g}",
                        "r0": f"{run.r0:.17g}",
                        "epsilon": f"{run.epsilon:.17g}",
                    }
                )


def _epsilon_label(epsilon: float) -> str:
    return "0" if epsilon == 0.0 else f"{epsilon:.0e}"


def plot_matrix(
    path: Path,
    runs: Sequence[RunResult],
    value_getter: Any,
    ylabel: str,
    title: str,
    symlog_linthresh: float,
) -> None:
    r0_values = sorted({run.r0 for run in runs})
    epsilon_values = sorted({run.epsilon for run in runs})
    colors = plt.cm.viridis(np.linspace(0.12, 0.88, len(epsilon_values)))
    fig, axes = plt.subplots(
        1, len(r0_values), figsize=(13.5, 4.3), sharex=True, sharey=True,
        constrained_layout=True,
    )
    if len(r0_values) == 1:
        axes = np.array([axes])

    for axis, r0 in zip(axes, r0_values):
        for color, epsilon in zip(colors, epsilon_values):
            run = next(
                item for item in runs if item.r0 == r0 and item.epsilon == epsilon
            )
            axis.plot(
                run.N,
                value_getter(run),
                color=color,
                linewidth=1.8,
                label=rf"$\epsilon={_epsilon_label(epsilon)}$",
            )
        axis.axhline(0.0, color="0.25", linewidth=0.8)
        axis.set_title(rf"$r_0={r0:g}$")
        axis.set_xlabel("E-fold N")
        axis.grid(True, alpha=0.25)
        axis.set_yscale("symlog", linthresh=symlog_linthresh)

    axes[0].set_ylabel(ylabel)
    axes[-1].legend(loc="best", fontsize=8)
    fig.suptitle(title)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def make_plots(output_dir: Path, runs: Sequence[RunResult]) -> dict[str, Path]:
    paths = {
        "shape": output_dir / "cbr001_stage3_shape.png",
        "shear": output_dir / "cbr001_stage3_shear.png",
        "hubble_ratio": output_dir / "cbr001_stage3_hubble_ratio.png",
    }
    plot_matrix(
        paths["shape"],
        runs,
        lambda run: np.log(run.r / run.r0),
        r"$\ln(r/r_0)$",
        "CBR-001 Stage 3A: accumulated shape response",
        symlog_linthresh=1.0e-10,
    )
    plot_matrix(
        paths["shear"],
        runs,
        lambda run: run.delta_over_H,
        r"$\delta/H$",
        "CBR-001 Stage 3A: dimensionless biaxial shear",
        symlog_linthresh=1.0e-10,
    )
    plot_matrix(
        paths["hubble_ratio"],
        runs,
        lambda run: run.H_t_over_H_p - 1.0,
        r"$H_t/H_p-1$",
        "CBR-001 Stage 3A: directional Hubble-ratio deviation",
        symlog_linthresh=1.0e-10,
    )
    return paths


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Validate biaxial Bianchi-I Casimir backreaction on de Sitter."
    )
    parser.add_argument(
        "--stage2-csv",
        type=Path,
        default=script_dir / "stage2_outputs" / "cbr001_stage2_scan.csv",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=script_dir / "stage3_outputs"
    )
    parser.add_argument("--r0", nargs="+", type=float, default=DEFAULT_R0)
    parser.add_argument(
        "--epsilon", nargs="+", type=float, default=DEFAULT_EPSILON
    )
    parser.add_argument("--n-max", type=float, default=10.0)
    parser.add_argument("--samples", type=int, default=501)
    parser.add_argument("--rtol", type=float, default=1.0e-11)
    parser.add_argument("--atol", type=float, default=1.0e-16)
    args = parser.parse_args()

    if args.n_max <= 0.0 or args.samples < 11:
        raise ValueError("Require n-max > 0 and at least 11 output samples")
    if any(epsilon < 0.0 for epsilon in args.epsilon):
        raise ValueError("epsilon values must be non-negative")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    source = CasimirInterpolator(args.stage2_csv)
    N_eval = np.linspace(0.0, args.n_max, args.samples)

    print("CBR-001 Stage 3A — perturbative biaxial cosmological backreaction")
    print(f"Stage-2 source: {source.csv_path}")
    print(f"H_bg={H_BG:g}, kappa={KAPPA:g}, rho_bg={RHO_BG:g}")
    print(
        f"N=[0, {args.n_max:g}], samples={args.samples}, "
        f"rtol={args.rtol:.1e}, atol={args.atol:.1e}"
    )

    runs: list[RunResult] = []
    for r0 in args.r0:
        for epsilon in args.epsilon:
            run = solve_run(
                source,
                r0=float(r0),
                epsilon=float(epsilon),
                N_eval=N_eval,
                rtol=args.rtol,
                atol=args.atol,
            )
            runs.append(run)
            print(
                f"r0={r0:g} epsilon={epsilon:.0e} "
                f"max|delta/H|={np.max(np.abs(run.delta_over_H)):.3e} "
                f"ln(rf/r0)={np.log(run.r[-1] / run.r0):+.3e}"
            )

    controls = validate_controls(runs)
    max_constraint = max(
        float(np.max(run.constraint_residual)) for run in runs
    )
    max_continuity = max(
        float(np.max(run.continuity_residual)) for run in runs
    )
    benchmark_epsilon = min(
        epsilon for epsilon in args.epsilon if epsilon > 0.0
    )
    benchmark = analytic_benchmark(source, runs, benchmark_epsilon)
    crosscheck_epsilon = max(args.epsilon)
    tolerance = tolerance_crosscheck(
        source,
        runs,
        N_eval,
        epsilon=crosscheck_epsilon,
        tight_rtol=1.0e-13,
        tight_atol=1.0e-18,
    )

    interpolation_passed = max(
        source.validation["rho_global_relative_error"],
        source.validation["p_p_global_relative_error"],
        source.validation["p_t_global_relative_error"],
    ) < 1.0e-4 and abs(source.validation["cube_delta_p"]) < 1.0e-12

    validations = {
        "source_interpolation": {
            **source.validation,
            "threshold": 1.0e-4,
            "passed": interpolation_passed,
        },
        **controls,
        "hamiltonian_constraint": {
            "maximum_normalized_residual": max_constraint,
            "threshold": 1.0e-9,
            "passed": max_constraint < 1.0e-9,
        },
        "casimir_continuity": {
            "maximum_normalized_residual": max_continuity,
            "threshold": 1.0e-7,
            "passed": max_continuity < 1.0e-7,
        },
        "small_epsilon_benchmark": benchmark,
        "tolerance_crosscheck": tolerance,
    }
    overall_passed = all(
        item["passed"] for item in validations.values()
    )

    csv_path = output_dir / "cbr001_stage3_runs.csv"
    summary_path = output_dir / "cbr001_stage3_summary.json"
    write_runs_csv(csv_path, runs)
    plot_paths = make_plots(output_dir, runs)

    summary = {
        "stage": "CBR-001 Stage 3A",
        "status": "PASS" if overall_passed else "FAIL",
        "scope_statement": (
            "Stage 3A does not test or establish the ITSM 13/12 ratio. "
            "It validates the cosmological backreaction engine required for "
            "that later test."
        ),
        "conventions": {
            "H_bg": H_BG,
            "kappa": KAPPA,
            "rho_bg": RHO_BG,
            "source_prefactor": "hbar*c/L_*^4 absorbed into epsilon",
            "independent_variable": "N=ln(a)",
        },
        "run_matrix": {
            "r0": [float(value) for value in args.r0],
            "epsilon": [float(value) for value in args.epsilon],
            "N_max": args.n_max,
            "samples": args.samples,
        },
        "runs": [run_summary(run) for run in runs],
        "validations": validations,
        "outputs": {
            "csv": str(csv_path),
            "summary": str(summary_path),
            **{name: str(path) for name, path in plot_paths.items()},
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print()
    print("Validation:")
    for name, details in validations.items():
        metric = details.get(
            "maximum_normalized_residual",
            details.get(
                "maximum_relative_error",
                details.get("maximum_relative_difference", "control"),
            ),
        )
        print(f"  {name:28s} {'PASS' if details['passed'] else 'FAIL'}  {metric}")
    print()
    print(f"CSV:     {csv_path}")
    print(f"Summary: {summary_path}")
    for name, path in plot_paths.items():
        print(f"{name:12s} {path}")
    print(f"STATUS: {'PASS' if overall_passed else 'FAIL'}")
    return 0 if overall_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
