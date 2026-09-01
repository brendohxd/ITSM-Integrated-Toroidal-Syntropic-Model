#!/usr/bin/env python3
"""CBR-001 Stage 3B: reachability and stability test for H_t/H_p = 13/12.

This script reuses the validated Stage-3A Casimir interpolation, de Sitter
background, Hamiltonian constraint, and biaxial shear equation. It does not
assume that 13/12 is correct: it distinguishes an unreachable target, a tuned
transient, a quasi-plateau, and a genuine attractor.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from cbr001_stage3_backreaction import (
    H_BG,
    KAPPA,
    RHO_BG,
    CasimirInterpolator,
)


Q_TARGET = 13.0 / 12.0
X_TARGET = 3.0 / 38.0
S_MIN_ANALYTIC = 128.0 / 171.0
N_PEAK_ANALYTIC = float(np.log(4.0 / 3.0))
F_PEAK_ANALYTIC = 27.0 / 256.0
CLASSIFICATIONS = {
    "NO_CROSSING",
    "TRANSIENT_CROSSING",
    "QUASI_PLATEAU",
    "ATTRACTOR",
    "INVALID",
}
DEFAULT_R0 = (1.01, 1.05, 1.10, 1.25, 1.50, 2.0, 3.0, 4.0)


def q_from_x(x: float | np.ndarray) -> np.ndarray:
    x_array = np.asarray(x, dtype=float)
    return (1.0 + x_array / 3.0) / (1.0 - 2.0 * x_array / 3.0)


def x_from_q(q: float | np.ndarray) -> np.ndarray:
    q_array = np.asarray(q, dtype=float)
    return 3.0 * (q_array - 1.0) / (2.0 * q_array + 1.0)


def finite_or_none(value: float) -> float | None:
    return float(value) if np.isfinite(value) else None


def json_default(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    raise TypeError("Unsupported JSON value")


@dataclass
class RatioRun:
    run_id: int
    run_kind: str
    perturbation: str
    r0: float
    epsilon: float
    delta0: float
    valid: bool
    invalid_reason: str
    N: np.ndarray
    r: np.ndarray
    delta: np.ndarray
    q: np.ndarray
    x: np.ndarray
    rho_C: np.ndarray
    H: np.ndarray
    H_p: np.ndarray
    H_t: np.ndarray
    casimir_fraction: np.ndarray
    constraint_residual: np.ndarray
    continuity_residual: np.ndarray
    max_q: float = np.nan
    N_at_max_q: float = np.nan
    first_crossing_N: float = np.nan
    last_crossing_N: float = np.nan
    dwell_0p1: float = 0.0
    dwell_1: float = 0.0
    q_at_N_10: float = np.nan
    q_at_N_20: float = np.nan
    classification: str = "INVALID"
    stability: dict[str, Any] = field(default_factory=dict)

    def to_record(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "run_kind": self.run_kind,
            "perturbation": self.perturbation,
            "r0": self.r0,
            "epsilon": self.epsilon,
            "delta0": self.delta0,
            "max_q": finite_or_none(self.max_q),
            "N_at_max_q": finite_or_none(self.N_at_max_q),
            "first_crossing_N": finite_or_none(self.first_crossing_N),
            "last_crossing_N": finite_or_none(self.last_crossing_N),
            "dwell_time_within_0p1_percent": self.dwell_0p1,
            "dwell_time_within_1_percent": self.dwell_1,
            "q_at_N_10": finite_or_none(self.q_at_N_10),
            "q_at_N_20": finite_or_none(self.q_at_N_20),
            "max_abs_delta_over_H": finite_or_none(
                float(np.max(np.abs(self.x))) if self.x.size else np.nan
            ),
            "max_abs_casimir_fraction": finite_or_none(
                float(np.max(np.abs(self.casimir_fraction)))
                if self.casimir_fraction.size
                else np.nan
            ),
            "minimum_H_p": finite_or_none(
                float(np.min(self.H_p)) if self.H_p.size else np.nan
            ),
            "minimum_H_t": finite_or_none(
                float(np.min(self.H_t)) if self.H_t.size else np.nan
            ),
            "constraint_residual": finite_or_none(
                float(np.max(self.constraint_residual))
                if self.constraint_residual.size
                else np.nan
            ),
            "continuity_residual": finite_or_none(
                float(np.max(self.continuity_residual))
                if self.continuity_residual.size
                else np.nan
            ),
            "classification": self.classification,
            "valid": self.valid,
            "invalid_reason": self.invalid_reason,
        }


def longest_dwell(N: np.ndarray, q: np.ndarray, relative_band: float) -> float:
    if N.size < 2:
        return 0.0
    inside = np.abs(q / Q_TARGET - 1.0) <= relative_band
    if not np.any(inside):
        return 0.0
    indices = np.flatnonzero(inside)
    splits = np.flatnonzero(np.diff(indices) > 1)
    starts = np.r_[0, splits + 1]
    ends = np.r_[splits, len(indices) - 1]
    return float(
        max(N[indices[end]] - N[indices[start]] for start, end in zip(starts, ends))
    )


def crossing_times(N: np.ndarray, q: np.ndarray) -> list[float]:
    if N.size < 2:
        return []
    f = q - Q_TARGET
    crossings: list[float] = []
    for index in range(len(N) - 1):
        left = f[index]
        right = f[index + 1]
        if left == 0.0:
            crossings.append(float(N[index]))
        elif left * right < 0.0:
            fraction = -left / (right - left)
            crossings.append(float(N[index] + fraction * (N[index + 1] - N[index])))
    if f[-1] == 0.0:
        crossings.append(float(N[-1]))
    return crossings


def classify_run(run: RatioRun) -> None:
    if not run.valid:
        run.classification = "INVALID"
        return
    reached = run.max_q >= Q_TARGET * (1.0 - 1.0e-9)
    if not reached:
        run.classification = "NO_CROSSING"
    elif run.dwell_1 >= 1.0:
        run.classification = "QUASI_PLATEAU"
    else:
        run.classification = "TRANSIENT_CROSSING"


class RatioIntegrator:
    def __init__(
        self,
        source: CasimirInterpolator,
        N_eval: np.ndarray,
        rtol: float,
        atol: float,
    ) -> None:
        self.source = source
        self.N_eval = N_eval
        self.rtol = rtol
        self.atol = atol
        self._next_run_id = 1

    def _allocate_id(self) -> int:
        run_id = self._next_run_id
        self._next_run_id += 1
        return run_id

    def _empty_invalid(
        self,
        run_kind: str,
        perturbation: str,
        r0: float,
        epsilon: float,
        delta0: float,
        reason: str,
    ) -> RatioRun:
        empty = np.array([], dtype=float)
        return RatioRun(
            run_id=self._allocate_id(),
            run_kind=run_kind,
            perturbation=perturbation,
            r0=r0,
            epsilon=epsilon,
            delta0=delta0,
            valid=False,
            invalid_reason=reason,
            N=empty,
            r=empty,
            delta=empty,
            q=empty,
            x=empty,
            rho_C=empty,
            H=empty,
            H_p=empty,
            H_t=empty,
            casimir_fraction=empty,
            constraint_residual=empty,
            continuity_residual=empty,
        )

    def run(
        self,
        r0: float,
        epsilon: float,
        delta0: float = 0.0,
        run_kind: str = "grid",
        perturbation: str = "baseline",
    ) -> RatioRun:
        if epsilon < 0.0:
            return self._empty_invalid(
                run_kind, perturbation, r0, epsilon, delta0, "negative_epsilon"
            )
        if r0 < self.source.r_min or r0 > self.source.r_max:
            return self._empty_invalid(
                run_kind, perturbation, r0, epsilon, delta0, "initial_r_outside_domain"
            )

        initial_source = self.source.evaluate(0.0, r0)
        initial_rho_total = RHO_BG + epsilon * float(initial_source.rho)
        initial_radicand = (
            KAPPA * initial_rho_total + delta0**2 / 3.0
        ) / 3.0
        if initial_rho_total <= 0.0:
            return self._empty_invalid(
                run_kind, perturbation, r0, epsilon, delta0, "rho_total_nonpositive"
            )
        if initial_radicand <= 0.0:
            return self._empty_invalid(
                run_kind, perturbation, r0, epsilon, delta0, "no_real_expanding_branch"
            )
        initial_H = float(np.sqrt(initial_radicand))
        if initial_H - 2.0 * delta0 / 3.0 <= 0.0:
            return self._empty_invalid(
                run_kind, perturbation, r0, epsilon, delta0, "initial_Hp_nonpositive"
            )
        if initial_H + delta0 / 3.0 <= 0.0:
            return self._empty_invalid(
                run_kind, perturbation, r0, epsilon, delta0, "initial_Ht_nonpositive"
            )

        initial_drive = KAPPA * epsilon * float(initial_source.delta_p) / initial_H
        if r0 == self.source.r_max and initial_drive >= 0.0:
            return self._empty_invalid(
                run_kind,
                perturbation,
                r0,
                epsilon,
                delta0,
                "initial_boundary_outward",
            )
        if r0 == self.source.r_min and initial_drive <= 0.0:
            return self._empty_invalid(
                run_kind,
                perturbation,
                r0,
                epsilon,
                delta0,
                "initial_boundary_outward",
            )

        def quantities(N: float, state: np.ndarray) -> tuple[float, Any, float, float, float, float]:
            log_r, delta = state
            r = float(np.exp(log_r))
            r_clipped = float(np.clip(r, self.source.r_min, self.source.r_max))
            casimir = self.source.evaluate(N, r_clipped)
            rho_total = RHO_BG + epsilon * float(casimir.rho)
            radicand = (KAPPA * rho_total + delta**2 / 3.0) / 3.0
            H = float(np.sqrt(max(radicand, 1.0e-30)))
            H_p = H - 2.0 * delta / 3.0
            H_t = H + delta / 3.0
            return r, casimir, rho_total, radicand, H_p, H_t

        def rhs(N: float, state: np.ndarray) -> np.ndarray:
            _, casimir, _, radicand, _, _ = quantities(N, state)
            H = float(np.sqrt(max(radicand, 1.0e-30)))
            delta = float(state[1])
            return np.array(
                [
                    delta / H,
                    -3.0 * delta
                    + KAPPA * epsilon * float(casimir.delta_p) / H,
                ],
                dtype=float,
            )

        def domain_event(N: float, state: np.ndarray) -> float:
            r = float(np.exp(state[0]))
            return min(r - self.source.r_min, self.source.r_max - r)

        def density_event(N: float, state: np.ndarray) -> float:
            return quantities(N, state)[2]

        def expanding_event(N: float, state: np.ndarray) -> float:
            return quantities(N, state)[3]

        def hp_event(N: float, state: np.ndarray) -> float:
            return quantities(N, state)[4]

        def ht_event(N: float, state: np.ndarray) -> float:
            return quantities(N, state)[5]

        events = [domain_event, density_event, expanding_event, hp_event, ht_event]
        for event in events:
            event.terminal = True
            event.direction = -1.0

        try:
            solution = solve_ivp(
                rhs,
                (float(self.N_eval[0]), float(self.N_eval[-1])),
                np.array([np.log(r0), delta0], dtype=float),
                method="DOP853",
                t_eval=self.N_eval,
                rtol=self.rtol,
                atol=self.atol,
                events=events,
            )
        except (RuntimeError, ValueError, FloatingPointError) as error:
            return self._empty_invalid(
                run_kind,
                perturbation,
                r0,
                epsilon,
                delta0,
                f"integration_exception:{type(error).__name__}",
            )

        event_names = [
            "left_stage2_domain",
            "rho_total_nonpositive",
            "no_real_expanding_branch",
            "Hp_nonpositive",
            "Ht_nonpositive",
        ]
        triggered = [
            name
            for name, times in zip(event_names, solution.t_events)
            if len(times) > 0
        ]
        completed = solution.success and solution.t[-1] >= self.N_eval[-1] - 1.0e-10
        invalid_reason = "" if completed else (triggered[0] if triggered else solution.message)

        N = solution.t
        r = np.exp(solution.y[0])
        delta = solution.y[1]
        casimir = self.source.evaluate(N, np.clip(r, self.source.r_min, self.source.r_max))
        rho_total = RHO_BG + epsilon * casimir.rho
        radicand = (KAPPA * rho_total + delta**2 / 3.0) / 3.0
        H = np.sqrt(np.maximum(radicand, 1.0e-30))
        H_p = H - 2.0 * delta / 3.0
        H_t = H + delta / 3.0
        x = delta / H
        q = H_t / H_p

        constraint_raw = 3.0 * H**2 - delta**2 / 3.0 - KAPPA * rho_total
        constraint_scale = np.maximum.reduce(
            [3.0 * H**2, np.abs(KAPPA * rho_total), np.ones_like(H)]
        )
        constraint_residual = np.abs(constraint_raw) / constraint_scale

        d_rho_dt = -4.0 * H * casimir.rho + delta * casimir.u_x
        continuity_p = H_p * (casimir.rho + casimir.p_p)
        continuity_t = 2.0 * H_t * (casimir.rho + casimir.p_t)
        continuity_raw = d_rho_dt + continuity_p + continuity_t
        continuity_scale = np.maximum.reduce(
            [
                np.abs(d_rho_dt),
                np.abs(continuity_p) + np.abs(continuity_t),
                np.abs(H * casimir.rho),
                np.full_like(H, 1.0e-30),
            ]
        )
        continuity_residual = np.abs(continuity_raw) / continuity_scale
        casimir_fraction = epsilon * casimir.rho / rho_total

        run = RatioRun(
            run_id=self._allocate_id(),
            run_kind=run_kind,
            perturbation=perturbation,
            r0=r0,
            epsilon=epsilon,
            delta0=delta0,
            valid=completed,
            invalid_reason=invalid_reason,
            N=N,
            r=r,
            delta=delta,
            q=q,
            x=x,
            rho_C=casimir.rho,
            H=H,
            H_p=H_p,
            H_t=H_t,
            casimir_fraction=casimir_fraction,
            constraint_residual=constraint_residual,
            continuity_residual=continuity_residual,
        )
        self._summarize(run)
        classify_run(run)
        return run

    @staticmethod
    def _summarize(run: RatioRun) -> None:
        if run.N.size == 0:
            return
        max_index = int(np.nanargmax(run.q))
        run.max_q = float(run.q[max_index])
        run.N_at_max_q = float(run.N[max_index])
        crossings = crossing_times(run.N, run.q)
        if not crossings and abs(run.max_q / Q_TARGET - 1.0) <= 1.0e-8:
            crossings = [run.N_at_max_q]
        if crossings:
            run.first_crossing_N = crossings[0]
            run.last_crossing_N = crossings[-1]
        run.dwell_0p1 = longest_dwell(run.N, run.q, 0.001)
        run.dwell_1 = longest_dwell(run.N, run.q, 0.01)
        if run.N[-1] >= 10.0:
            run.q_at_N_10 = float(np.interp(10.0, run.N, run.q))
        if run.N[-1] >= 20.0:
            run.q_at_N_20 = float(np.interp(20.0, run.N, run.q))


def root_threshold(
    integrator: RatioIntegrator,
    r0: float,
    coarse_runs: Sequence[RatioRun],
    all_runs: list[RatioRun],
) -> tuple[RatioRun | None, dict[str, Any]]:
    valid = sorted(
        [run for run in coarse_runs if run.valid], key=lambda run: run.epsilon
    )
    bracket: tuple[float, float] | None = None
    for left, right in zip(valid[:-1], valid[1:]):
        f_left = left.max_q - Q_TARGET
        f_right = right.max_q - Q_TARGET
        if f_left == 0.0:
            bracket = (left.epsilon, left.epsilon)
            break
        if f_left < 0.0 <= f_right:
            bracket = (left.epsilon, right.epsilon)
            break

    delta_p0 = float(integrator.source.evaluate(0.0, r0).delta_p)
    analytic_estimate = (
        S_MIN_ANALYTIC / delta_p0 if delta_p0 > 0.0 else np.nan
    )
    base_info: dict[str, Any] = {
        "r0": r0,
        "bracket_low": None,
        "bracket_high": None,
        "epsilon_threshold": None,
        "analytic_small_source_epsilon": finite_or_none(analytic_estimate),
        "root_residual": None,
        "classification": "NO_CROSSING" if valid else "INVALID",
    }
    if bracket is None:
        return None, base_info

    base_info["bracket_low"], base_info["bracket_high"] = bracket
    if bracket[0] == bracket[1]:
        epsilon_root = bracket[0]
    else:
        def objective(epsilon: float) -> float:
            run = integrator.run(
                r0,
                epsilon,
                run_kind="root_search",
                perturbation="brentq",
            )
            all_runs.append(run)
            if not run.valid:
                raise ValueError("Root search entered an invalid trajectory")
            return run.max_q - Q_TARGET

        try:
            epsilon_root = float(
                brentq(
                    objective,
                    bracket[0],
                    bracket[1],
                    xtol=1.0e-10,
                    rtol=1.0e-10,
                    maxiter=60,
                )
            )
        except (ValueError, RuntimeError):
            base_info["classification"] = "INVALID"
            return None, base_info

    threshold_run = integrator.run(
        r0,
        epsilon_root,
        run_kind="threshold",
        perturbation="baseline",
    )
    all_runs.append(threshold_run)
    if not threshold_run.valid:
        base_info["classification"] = "INVALID"
        return None, base_info

    base_info.update(
        {
            "epsilon_threshold": epsilon_root,
            "root_residual": abs(threshold_run.max_q - Q_TARGET),
            "classification": threshold_run.classification,
        }
    )
    return threshold_run, base_info


def stability_test(
    integrator: RatioIntegrator,
    baseline: RatioRun,
    all_runs: list[RatioRun],
) -> dict[str, Any]:
    delta_shift = 0.01 * X_TARGET * H_BG
    variations = [
        (baseline.r0 * 0.99, baseline.epsilon, 0.0, "r0_x_0p99"),
        (baseline.r0 * 1.01, baseline.epsilon, 0.0, "r0_x_1p01"),
        (baseline.r0, baseline.epsilon * 0.99, 0.0, "epsilon_x_0p99"),
        (baseline.r0, baseline.epsilon * 1.01, 0.0, "epsilon_x_1p01"),
        (baseline.r0, baseline.epsilon, -delta_shift, "delta0_minus_1pct_target"),
        (baseline.r0, baseline.epsilon, delta_shift, "delta0_plus_1pct_target"),
    ]
    cases: list[dict[str, Any]] = []
    valid_late_q: list[float] = []
    for r0, epsilon, delta0, label in variations:
        run = integrator.run(
            r0,
            epsilon,
            delta0=delta0,
            run_kind="stability",
            perturbation=label,
        )
        all_runs.append(run)
        if run.valid:
            valid_late_q.append(run.q_at_N_20)
        cases.append(
            {
                "perturbation": label,
                "valid": run.valid,
                "invalid_reason": run.invalid_reason,
                "crossing_time_change": finite_or_none(
                    run.first_crossing_N - baseline.first_crossing_N
                    if np.isfinite(run.first_crossing_N)
                    and np.isfinite(baseline.first_crossing_N)
                    else np.nan
                ),
                "maximum_q_change": finite_or_none(run.max_q - baseline.max_q),
                "dwell_1_percent_change": run.dwell_1 - baseline.dwell_1,
                "late_q_change": finite_or_none(
                    run.q_at_N_20 - baseline.q_at_N_20
                ),
                "classification": run.classification,
            }
        )

    late_spread = (
        max(valid_late_q) - min(valid_late_q) if len(valid_late_q) >= 2 else np.inf
    )
    nearby_convergence = bool(
        np.isfinite(late_spread) and late_spread < 1.0e-4
    )
    peak_deviation = abs(baseline.max_q - 1.0)
    late_deviation = abs(baseline.q_at_N_20 - 1.0)
    decays_to_one = late_deviation < max(0.1 * peak_deviation, 1.0e-8)
    attractor = bool(
        baseline.dwell_1 >= 5.0
        and nearby_convergence
        and not decays_to_one
    )
    if attractor:
        baseline.classification = "ATTRACTOR"
    elif baseline.dwell_1 >= 1.0:
        baseline.classification = "QUASI_PLATEAU"
    else:
        baseline.classification = "TRANSIENT_CROSSING"

    result = {
        "cases": cases,
        "late_q_spread": finite_or_none(late_spread),
        "nearby_trajectories_converge": nearby_convergence,
        "decays_toward_one": decays_to_one,
        "attractor": attractor,
        "final_classification": baseline.classification,
    }
    baseline.stability = result
    return result


def amplitude_regime(run: RatioRun | None) -> str:
    if run is None or not run.valid:
        return "UNAVAILABLE"
    fraction = float(np.max(np.abs(run.casimir_fraction)))
    if fraction < 0.01:
        return "PERTURBATIVE"
    if fraction < 0.1:
        return "MARGINAL"
    return "NONPERTURBATIVE"


def write_runs_csv(path: Path, runs: Sequence[RatioRun]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "run_id",
        "run_kind",
        "perturbation",
        "r0",
        "epsilon",
        "delta0",
        "max_q",
        "N_at_max_q",
        "first_crossing_N",
        "last_crossing_N",
        "dwell_time_within_0p1_percent",
        "dwell_time_within_1_percent",
        "q_at_N_10",
        "q_at_N_20",
        "max_abs_delta_over_H",
        "max_abs_casimir_fraction",
        "minimum_H_p",
        "minimum_H_t",
        "constraint_residual",
        "continuity_residual",
        "classification",
        "valid",
        "invalid_reason",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for run in sorted(runs, key=lambda item: item.run_id):
            writer.writerow(run.to_record())


def write_thresholds_csv(path: Path, thresholds: Sequence[dict[str, Any]]) -> None:
    fieldnames = [
        "r0",
        "bracket_low",
        "bracket_high",
        "epsilon_threshold",
        "analytic_small_source_epsilon",
        "root_residual",
        "max_q",
        "N_at_max_q",
        "first_crossing_N",
        "last_crossing_N",
        "dwell_time_within_0p1_percent",
        "dwell_time_within_1_percent",
        "q_at_N_10",
        "q_at_N_20",
        "max_abs_casimir_fraction",
        "classification",
        "amplitude_regime",
        "decays_toward_one",
        "attractor",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for threshold in thresholds:
            writer.writerow({name: threshold.get(name) for name in fieldnames})


def select_plot_runs(
    r0_values: Sequence[float],
    coarse_by_r0: dict[float, list[RatioRun]],
    thresholds: dict[float, RatioRun],
) -> list[RatioRun]:
    selected: list[RatioRun] = []
    for r0 in r0_values:
        if r0 in thresholds:
            selected.append(thresholds[r0])
            continue
        valid = [run for run in coarse_by_r0[r0] if run.valid]
        if valid:
            selected.append(max(valid, key=lambda run: run.max_q))
    return selected


def plot_ratio(path: Path, runs: Sequence[RatioRun]) -> None:
    fig, axes = plt.subplots(2, 4, figsize=(15.5, 7.5), sharex=True, sharey=True, constrained_layout=True)
    for axis, run in zip(axes.flat, runs):
        axis.plot(run.N, run.q, color="tab:blue", linewidth=2.0)
        axis.axhline(Q_TARGET, color="tab:red", linestyle="--", linewidth=1.2)
        axis.axhline(1.0, color="0.3", linestyle=":", linewidth=1.0)
        axis.set_title(
            rf"$r_0={run.r0:g}$, $\epsilon={run.epsilon:.3g}$"
            + "\n"
            + run.classification
        )
        axis.grid(True, alpha=0.25)
        axis.set_xlabel("E-fold N")
    for axis in axes[:, 0]:
        axis.set_ylabel(r"$q=H_t/H_p$")
    fig.suptitle("CBR-001 Stage 3B: target reachability and late-time return")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_phase_space(path: Path, runs: Sequence[RatioRun]) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.5), constrained_layout=True)
    colors = plt.cm.viridis(np.linspace(0.08, 0.92, max(len(runs), 1)))
    for color, run in zip(colors, runs):
        ax.plot(run.r, run.x, color=color, linewidth=1.8, label=rf"$r_0={run.r0:g}$")
        ax.scatter([run.r[0]], [run.x[0]], color=color, marker="o", s=24)
        ax.scatter([run.r[-1]], [run.x[-1]], color=color, marker="x", s=30)
    ax.axhline(X_TARGET, color="tab:red", linestyle="--", linewidth=1.2, label=r"$x=3/38$")
    ax.axhline(0.0, color="0.3", linestyle=":", linewidth=1.0)
    ax.set_xlabel(r"Aspect ratio $r$")
    ax.set_ylabel(r"$x=\delta/H$")
    ax.set_title("CBR-001 Stage 3B: shear-shape phase space")
    ax.grid(True, alpha=0.25)
    ax.legend(ncol=2, fontsize=8)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_thresholds(path: Path, threshold_rows: Sequence[dict[str, Any]]) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.5), constrained_layout=True)
    reached = [row for row in threshold_rows if row.get("epsilon_threshold") is not None]
    if reached:
        r = np.array([row["r0"] for row in reached], dtype=float)
        numerical = np.array([row["epsilon_threshold"] for row in reached], dtype=float)
        analytic = np.array([row["analytic_small_source_epsilon"] for row in reached], dtype=float)
        ax.plot(r, numerical, "o-", linewidth=2.0, label="Numerical threshold")
        ax.plot(r, analytic, "s--", linewidth=1.5, label="Small-source estimate")
        for row in reached:
            ax.annotate(
                row["classification"],
                (row["r0"], row["epsilon_threshold"]),
                xytext=(4, 5),
                textcoords="offset points",
                fontsize=7,
            )
    missing = [row for row in threshold_rows if row.get("epsilon_threshold") is None]
    for row in missing:
        ax.annotate(
            row["classification"],
            (row["r0"], 1.0e-6),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            fontsize=7,
        )
    ax.set_yscale("log")
    ax.set_xlabel(r"Initial aspect ratio $r_0$")
    ax.set_ylabel(r"Threshold source amplitude $\epsilon$")
    ax.set_title(r"CBR-001 Stage 3B: amplitude required to reach $13/12$")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def analytic_checks() -> dict[str, Any]:
    q_at_target_x = float(q_from_x(X_TARGET))
    x_at_target_q = float(x_from_q(Q_TARGET))
    N_grid = np.linspace(0.0, 5.0, 200001)
    profile = np.exp(-3.0 * N_grid) - np.exp(-4.0 * N_grid)
    index = int(np.argmax(profile))
    numeric_peak_N = float(N_grid[index])
    numeric_peak = float(profile[index])
    numeric_s_min = X_TARGET / numeric_peak
    passed = all(
        [
            abs(q_at_target_x - Q_TARGET) < 1.0e-14,
            abs(x_at_target_q - X_TARGET) < 1.0e-14,
            abs(numeric_peak_N - N_PEAK_ANALYTIC) < 2.5e-5,
            abs(numeric_peak - F_PEAK_ANALYTIC) < 1.0e-10,
            abs(numeric_s_min - S_MIN_ANALYTIC) < 1.0e-9,
        ]
    )
    return {
        "q_target": Q_TARGET,
        "x_target": X_TARGET,
        "q_from_x_target": q_at_target_x,
        "x_from_q_target": x_at_target_q,
        "analytic_peak_N": N_PEAK_ANALYTIC,
        "numeric_peak_N": numeric_peak_N,
        "analytic_profile_maximum": F_PEAK_ANALYTIC,
        "numeric_profile_maximum": numeric_peak,
        "analytic_S_minimum": S_MIN_ANALYTIC,
        "numeric_S_minimum": numeric_s_min,
        "outside_strict_small_perturbation_regime": S_MIN_ANALYTIC > 0.1,
        "passed": passed,
    }


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Test reachability and stability of H_t/H_p = 13/12."
    )
    parser.add_argument(
        "--stage2-csv",
        type=Path,
        default=script_dir / "stage2_outputs" / "cbr001_stage2_scan.csv",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=script_dir / "stage3b_outputs"
    )
    parser.add_argument("--r0", nargs="+", type=float, default=DEFAULT_R0)
    parser.add_argument("--epsilon-min", type=float, default=1.0e-6)
    parser.add_argument("--epsilon-max", type=float, default=10.0)
    parser.add_argument("--epsilon-points", type=int, default=49)
    parser.add_argument("--n-max", type=float, default=20.0)
    parser.add_argument("--samples", type=int, default=2001)
    parser.add_argument("--rtol", type=float, default=1.0e-10)
    parser.add_argument("--atol", type=float, default=1.0e-14)
    args = parser.parse_args()

    if args.epsilon_min <= 0.0 or args.epsilon_max <= args.epsilon_min:
        raise ValueError("Require 0 < epsilon-min < epsilon-max")
    if args.epsilon_points < 8 or args.n_max < 20.0 or args.samples < 201:
        raise ValueError("Grid must use >=8 amplitudes, N_max>=20, and >=201 samples")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    source = CasimirInterpolator(args.stage2_csv)
    N_eval = np.linspace(0.0, args.n_max, args.samples)
    integrator = RatioIntegrator(source, N_eval, args.rtol, args.atol)
    epsilon_grid = np.geomspace(
        args.epsilon_min, args.epsilon_max, args.epsilon_points
    )

    print("CBR-001 Stage 3B — 13/12 reachability and stability test")
    print(f"q_target={Q_TARGET:.12f}, x_target={X_TARGET:.12f}")
    print(
        f"r0={list(args.r0)}, epsilon=[{args.epsilon_min:g}, {args.epsilon_max:g}], "
        f"points={args.epsilon_points}, N=[0, {args.n_max:g}]"
    )

    all_runs: list[RatioRun] = []
    coarse_by_r0: dict[float, list[RatioRun]] = {}
    for r0 in args.r0:
        coarse: list[RatioRun] = []
        for epsilon in epsilon_grid:
            run = integrator.run(float(r0), float(epsilon))
            coarse.append(run)
            all_runs.append(run)
        coarse_by_r0[float(r0)] = coarse
        valid = [run for run in coarse if run.valid]
        max_q = max((run.max_q for run in valid), default=np.nan)
        print(
            f"r0={r0:g}: valid={len(valid):2d}/{len(coarse):2d}, "
            f"largest valid max(q)={max_q:.9f}"
        )

    threshold_runs: dict[float, RatioRun] = {}
    threshold_rows: list[dict[str, Any]] = []
    stability_results: dict[str, Any] = {}
    for r0 in args.r0:
        threshold_run, info = root_threshold(
            integrator,
            float(r0),
            coarse_by_r0[float(r0)],
            all_runs,
        )
        if threshold_run is not None:
            stability = stability_test(integrator, threshold_run, all_runs)
            stability_results[f"r0={r0:g}"] = stability
            threshold_runs[float(r0)] = threshold_run
            info["classification"] = threshold_run.classification
            info.update(
                {
                    "max_q": threshold_run.max_q,
                    "N_at_max_q": threshold_run.N_at_max_q,
                    "first_crossing_N": finite_or_none(
                        threshold_run.first_crossing_N
                    ),
                    "last_crossing_N": finite_or_none(
                        threshold_run.last_crossing_N
                    ),
                    "dwell_time_within_0p1_percent": threshold_run.dwell_0p1,
                    "dwell_time_within_1_percent": threshold_run.dwell_1,
                    "q_at_N_10": threshold_run.q_at_N_10,
                    "q_at_N_20": threshold_run.q_at_N_20,
                    "max_abs_casimir_fraction": float(
                        np.max(np.abs(threshold_run.casimir_fraction))
                    ),
                    "amplitude_regime": amplitude_regime(threshold_run),
                    "decays_toward_one": stability["decays_toward_one"],
                    "attractor": stability["attractor"],
                }
            )
            print(
                f"  threshold r0={r0:g}: epsilon={threshold_run.epsilon:.9g}, "
                f"class={threshold_run.classification}, "
                f"dwell_1%={threshold_run.dwell_1:.3f}"
            )
        else:
            info.update(
                {
                    "max_q": None,
                    "N_at_max_q": None,
                    "first_crossing_N": None,
                    "last_crossing_N": None,
                    "dwell_time_within_0p1_percent": None,
                    "dwell_time_within_1_percent": None,
                    "q_at_N_10": None,
                    "q_at_N_20": None,
                    "max_abs_casimir_fraction": None,
                    "amplitude_regime": "UNAVAILABLE",
                    "decays_toward_one": None,
                    "attractor": False,
                }
            )
            print(f"  threshold r0={r0:g}: {info['classification']}")
        threshold_rows.append(info)

    analytic = analytic_checks()
    valid_runs = [run for run in all_runs if run.valid]
    max_constraint = max(
        float(np.max(run.constraint_residual)) for run in valid_runs
    )
    max_continuity = max(
        float(np.max(run.continuity_residual)) for run in valid_runs
    )
    root_residuals = [
        row["root_residual"]
        for row in threshold_rows
        if row.get("root_residual") is not None
    ]
    max_root_residual = max(root_residuals, default=0.0)
    candidate_late_deviation = max(
        (abs(run.q_at_N_20 - 1.0) for run in threshold_runs.values()),
        default=0.0,
    )
    asymptotic_passed = candidate_late_deviation < 1.0e-6

    validations = {
        "q_x_identity": {
            "error": abs(float(q_from_x(X_TARGET)) - Q_TARGET),
            "passed": abs(float(q_from_x(X_TARGET)) - Q_TARGET) < 1.0e-14,
        },
        "analytic_small_source": analytic,
        "hamiltonian_constraint": {
            "maximum_residual": max_constraint,
            "threshold": 1.0e-9,
            "passed": max_constraint < 1.0e-9,
        },
        "casimir_continuity": {
            "maximum_residual": max_continuity,
            "threshold": 1.0e-7,
            "passed": max_continuity < 1.0e-7,
        },
        "bracketed_roots": {
            "root_count": len(threshold_runs),
            "maximum_target_residual": max_root_residual,
            "threshold": 1.0e-7,
            "passed": max_root_residual < 1.0e-7,
        },
        "late_time_decay": {
            "maximum_candidate_abs_q20_minus_one": candidate_late_deviation,
            "threshold": 1.0e-6,
            "passed": asymptotic_passed,
        },
        "classification_vocabulary": {
            "used": sorted({run.classification for run in all_runs}),
            "passed": all(run.classification in CLASSIFICATIONS for run in all_runs),
        },
    }
    overall_passed = all(item["passed"] for item in validations.values())

    runs_path = output_dir / "cbr001_stage3b_runs.csv"
    thresholds_path = output_dir / "cbr001_stage3b_thresholds.csv"
    summary_path = output_dir / "cbr001_stage3b_summary.json"
    ratio_path = output_dir / "cbr001_stage3b_ratio.png"
    phase_path = output_dir / "cbr001_stage3b_phase_space.png"
    threshold_plot_path = output_dir / "cbr001_stage3b_threshold_epsilon.png"

    write_runs_csv(runs_path, all_runs)
    write_thresholds_csv(thresholds_path, threshold_rows)
    plot_runs = select_plot_runs(args.r0, coarse_by_r0, threshold_runs)
    plot_ratio(ratio_path, plot_runs)
    plot_phase_space(phase_path, [run for run in plot_runs if run.valid])
    plot_thresholds(threshold_plot_path, threshold_rows)

    reached = [row for row in threshold_rows if row["epsilon_threshold"] is not None]
    classifications = {
        label: sum(1 for row in threshold_rows if row["classification"] == label)
        for label in sorted(CLASSIFICATIONS)
    }
    summary = {
        "stage": "CBR-001 Stage 3B",
        "status": "PASS" if overall_passed else "FAIL",
        "target": {
            "q": Q_TARGET,
            "x": X_TARGET,
            "identity": "q=(1+x/3)/(1-2x/3)",
        },
        "analytic_check": analytic,
        "scope": {
            "mathematical_reachability": (
                f"Bracketed thresholds found for {len(reached)} of {len(args.r0)} initial shapes."
            ),
            "transient_crossing": (
                "A threshold touch or crossing is classified separately from a maintained state."
            ),
            "dynamical_attraction": (
                "ATTRACTOR requires five e-folds within 1%, nearby-trajectory convergence, "
                "and no subsequent decay toward q=1."
            ),
            "physically_plausible_amplitude": (
                "Thresholds are labeled PERTURBATIVE, MARGINAL, or NONPERTURBATIVE "
                "using the maximum Casimir fraction."
            ),
        },
        "asymptotic_expectation": {
            "expected": "delta/H -> 0 and q -> 1 because the source redshifts as a^-4",
            "maximum_candidate_abs_q20_minus_one": candidate_late_deviation,
            "confirmed": asymptotic_passed,
        },
        "run_grid": {
            "r0": [float(value) for value in args.r0],
            "epsilon_min": args.epsilon_min,
            "epsilon_max": args.epsilon_max,
            "epsilon_points": args.epsilon_points,
            "N_max": args.n_max,
            "samples": args.samples,
            "total_integrations_recorded": len(all_runs),
            "valid_integrations": len(valid_runs),
        },
        "thresholds": threshold_rows,
        "stability_tests": stability_results,
        "classification_counts_by_initial_shape": classifications,
        "validations": validations,
        "outputs": {
            "runs_csv": str(runs_path),
            "thresholds_csv": str(thresholds_path),
            "summary_json": str(summary_path),
            "ratio_plot": str(ratio_path),
            "phase_space_plot": str(phase_path),
            "threshold_plot": str(threshold_plot_path),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2, default=json_default) + "\n", encoding="utf-8")

    print()
    print("Validation:")
    for name, details in validations.items():
        print(f"  {name:26s} {'PASS' if details['passed'] else 'FAIL'}")
    print()
    print(f"Runs:       {runs_path}")
    print(f"Thresholds: {thresholds_path}")
    print(f"Summary:    {summary_path}")
    print(f"STATUS: {'PASS' if overall_passed else 'FAIL'}")
    return 0 if overall_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
