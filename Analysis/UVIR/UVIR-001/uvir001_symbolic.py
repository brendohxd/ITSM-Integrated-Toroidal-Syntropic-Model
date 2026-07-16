#!/usr/bin/env python3
"""UVIR-001 tree-level condensate-to-phonon matching audit.

The calculation tests the minimally kinetic complex scalar declared in the
v12 core architecture.  A successful numerical/symbolic validation does not
mean that the microscopic candidate succeeds: the hypothesis verdict is
reported separately from the calculation status.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
        help="Directory for the JSON summary and numerical grid CSV.",
    )
    return parser.parse_args()


def require_zero(name: str, expression: sp.Expr) -> None:
    simplified = sp.simplify(expression)
    if simplified != 0:
        raise AssertionError(f"{name} failed: {simplified}")


def positive_branch(
    z: float, m2: float, lam4: float, lam6: float, cutoff: float
) -> float:
    delta = z - m2
    discriminant = lam4 * lam4 + 4.0 * lam6 * delta / (cutoff * cutoff)
    if delta <= 0.0 or lam6 <= 0.0 or discriminant < 0.0:
        raise ValueError("No positive branch for the supplied parameters")
    return (cutoff * cutoff / lam6) * (-lam4 + math.sqrt(discriminant))


def pressure_from_s(s: float, lam4: float, lam6: float, cutoff: float) -> float:
    return lam4 * s * s / 8.0 + lam6 * s**3 / (12.0 * cutoff * cutoff)


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Positive symbols select the stable branch used by the gate.
    s, z, m2 = sp.symbols("s Z m2", positive=True)
    lam4, lam6, cutoff = sp.symbols("lambda4 lambda6 Lambda", positive=True)
    mu, q = sp.symbols("mu q", positive=True)

    potential = (
        sp.Rational(1, 2) * m2 * s
        + sp.Rational(1, 8) * lam4 * s**2
        + lam6 * s**3 / (24 * cutoff**2)
    )
    lagrangian_tf = sp.Rational(1, 2) * s * z - potential
    branch_equation = sp.simplify(2 * sp.diff(lagrangian_tf, s))
    expected_branch = z - m2 - lam4 * s / 2 - lam6 * s**2 / (4 * cutoff**2)
    require_zero("background branch", branch_equation - expected_branch)

    z_on_shell = m2 + lam4 * s / 2 + lam6 * s**2 / (4 * cutoff**2)
    pressure_on_shell = sp.simplify(lagrangian_tf.subs(z, z_on_shell))
    expected_pressure = lam4 * s**2 / 8 + lam6 * s**3 / (12 * cutoff**2)
    require_zero("on-shell pressure", pressure_on_shell - expected_pressure)

    radial_curvature = sp.simplify(lam4 * s + lam6 * s**2 / cutoff**2)
    dz_ds = sp.diff(z_on_shell, s)
    p_z = sp.simplify(sp.diff(pressure_on_shell, s) / dz_ds)
    p_zz = sp.simplify(sp.diff(p_z, s) / dz_ds)
    require_zero("envelope identity P_Z", p_z - s / 2)
    require_zero("P_ZZ", p_zz - s / radial_curvature)

    sound_speed_sq = sp.simplify(p_z / (p_z + 2 * z_on_shell * p_zz))
    expected_sound = sp.simplify(radial_curvature / (radial_curvature + 4 * z_on_shell))
    require_zero("sound speed", sound_speed_sq - expected_sound)

    pole_gap_sq = sp.simplify(radial_curvature + 4 * z_on_shell)
    charge_density = mu * s
    compressibility = sp.simplify(s + 4 * mu**2 * s / radial_curvature)

    # Exact pure-sextic limit.
    delta = z - m2
    s_sextic = 2 * cutoff * sp.sqrt(delta) / sp.sqrt(lam6)
    pressure_sextic = 2 * cutoff * delta ** sp.Rational(3, 2) / (3 * sp.sqrt(lam6))
    require_zero(
        "pure-sextic branch",
        expected_branch.subs({lam4: 0, s: s_sextic}),
    )
    require_zero(
        "pure-sextic pressure",
        pressure_on_shell.subs({lam4: 0, s: s_sextic}) - pressure_sextic,
    )
    radial_sextic = sp.simplify(radial_curvature.subs({lam4: 0, s: s_sextic}))
    require_zero("pure-sextic curvature", radial_sextic - 4 * delta)
    sound_sextic = sp.simplify(
        expected_sound.subs({lam4: 0, s: s_sextic})
    )
    require_zero(
        "pure-sextic sound speed",
        sound_sextic - (z - m2) / (2 * z - m2),
    )

    # Full quadratic amplitude/phase dispersion relation.
    k2, omega2 = sp.symbols("k2 omega2", nonnegative=True)
    dispersion_polynomial = sp.expand(
        (omega2 - k2 - radial_curvature) * (omega2 - k2)
        - 4 * z_on_shell * omega2
    )
    b = radial_curvature + 4 * z_on_shell
    omega_plus = sp.simplify(
        k2 + b / 2 + sp.sqrt(b**2 + 16 * z_on_shell * k2) / 2
    )
    omega_minus = sp.simplify(
        k2 + b / 2 - sp.sqrt(b**2 + 16 * z_on_shell * k2) / 2
    )
    require_zero(
        "gapped dispersion root",
        dispersion_polynomial.subs(omega2, omega_plus),
    )
    require_zero(
        "Goldstone dispersion root",
        dispersion_polynomial.subs(omega2, omega_minus),
    )
    require_zero("pole gap", omega_plus.subs(k2, 0) - pole_gap_sq)
    require_zero("Goldstone at k=0", omega_minus.subs(k2, 0))

    # Static expansion around the timelike finite-density background.
    delta0 = sp.symbols("Delta0", positive=True)
    a_coeff = 2 * cutoff / (3 * sp.sqrt(lam6))
    static_difference = a_coeff * (
        (delta0 - q**2) ** sp.Rational(3, 2) - delta0 ** sp.Rational(3, 2)
    )
    static_series = sp.series(static_difference, q, 0, 6).removeO()
    expected_static_series = (
        -sp.Rational(3, 2) * a_coeff * sp.sqrt(delta0) * q**2
        + sp.Rational(3, 8) * a_coeff * q**4 / sp.sqrt(delta0)
    )
    require_zero("static finite-density expansion", static_series - expected_static_series)
    static_q2_coefficient = sp.simplify(static_series.coeff(q, 2))
    if static_q2_coefficient == 0:
        raise AssertionError("Finite-density static q^2 coefficient unexpectedly vanished")

    # High-density pure-sextic cubic interactions and strong-coupling estimate.
    eps, dt, grad2 = sp.symbols("epsilon dt grad2")
    z_fluctuation = mu**2 + 2 * eps * mu * dt + eps**2 * (dt**2 - grad2)
    expanded = sp.series(a_coeff * z_fluctuation ** sp.Rational(3, 2), eps, 0, 4).removeO()
    quadratic = sp.simplify(expanded.coeff(eps, 2))
    cubic = sp.simplify(expanded.coeff(eps, 3))
    require_zero(
        "high-density quadratic action",
        quadratic - (3 * a_coeff * mu * dt**2 - sp.Rational(3, 2) * a_coeff * mu * grad2),
    )
    require_zero(
        "high-density cubic action",
        cubic - (a_coeff * dt**3 - sp.Rational(3, 2) * a_coeff * dt * grad2),
    )
    canonical_f_sq = sp.simplify(6 * a_coeff * mu)
    cubic_strong_scale = sp.simplify((canonical_f_sq ** sp.Rational(3, 2) / a_coeff) ** sp.Rational(1, 2))

    # Numerical scan verifies positivity and the q^2, rather than q^3, static power.
    rows: list[dict[str, float]] = []
    for lam4_value in (0.0, 0.5, 2.0):
        for mu2_value in (1.1, 2.0, 10.0):
            m2_value = 1.0
            lam6_value = 1.0
            cutoff_value = 1.0
            s0 = positive_branch(mu2_value, m2_value, lam4_value, lam6_value, cutoff_value)
            mr2 = lam4_value * s0 + lam6_value * s0 * s0 / cutoff_value**2
            gap2 = mr2 + 4.0 * mu2_value
            cs2 = mr2 / gap2
            compress = s0 + 4.0 * mu2_value * s0 / mr2
            p0 = pressure_from_s(s0, lam4_value, lam6_value, cutoff_value)
            delta_value = mu2_value - m2_value
            q1 = 1.0e-3 * math.sqrt(delta_value)
            q2 = 2.0e-3 * math.sqrt(delta_value)
            s1 = positive_branch(mu2_value - q1**2, m2_value, lam4_value, lam6_value, cutoff_value)
            s2 = positive_branch(mu2_value - q2**2, m2_value, lam4_value, lam6_value, cutoff_value)
            y1 = -(pressure_from_s(s1, lam4_value, lam6_value, cutoff_value) - p0)
            y2 = -(pressure_from_s(s2, lam4_value, lam6_value, cutoff_value) - p0)
            effective_power = math.log(y2 / y1) / math.log(q2 / q1)
            q2_coefficient_ratio = (y1 / q1**2) / (s0 / 2.0)
            rows.append(
                {
                    "lambda4": lam4_value,
                    "mu_squared": mu2_value,
                    "rho0_squared": s0,
                    "radial_curvature_squared": mr2,
                    "physical_gap_squared": gap2,
                    "sound_speed_squared": cs2,
                    "charge_compressibility": compress,
                    "static_effective_power": effective_power,
                    "static_q2_coefficient_ratio": q2_coefficient_ratio,
                }
            )

    validation = {
        "positive_condensate_branch": all(row["rho0_squared"] > 0.0 for row in rows),
        "positive_radial_curvature": all(row["radial_curvature_squared"] > 0.0 for row in rows),
        "positive_physical_gap": all(row["physical_gap_squared"] > 0.0 for row in rows),
        "positive_compressibility": all(row["charge_compressibility"] > 0.0 for row in rows),
        "subluminal_positive_sound_speed": all(0.0 < row["sound_speed_squared"] < 1.0 for row in rows),
        "static_power_is_quadratic": all(abs(row["static_effective_power"] - 2.0) < 2.0e-5 for row in rows),
        "static_q2_coefficient_matches_PZ": all(abs(row["static_q2_coefficient_ratio"] - 1.0) < 2.0e-5 for row in rows),
        "symbolic_identities": True,
    }
    validation_pass = all(validation.values())

    csv_path = args.output_dir / "uvir001_parameter_grid.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "gate": "UVIR-001",
        "validation_status": "PASS" if validation_pass else "FAIL",
        "candidate_verdict": "FAIL",
        "candidate_verdict_scope": (
            "The declared minimally kinetic single complex scalar with analytic mass, "
            "quartic, and sextic potential does not generate a leading spatial Y^(3/2) "
            "operator on its stable timelike finite-density branch."
        ),
        "broader_architecture_status": "OPEN",
        "mat001_status": "BLOCKED_PENDING_ALTERNATIVE_UVIR_ROUTE",
        "expressions": {
            "potential_in_s": sp.sstr(potential),
            "background_equation": sp.sstr(expected_branch),
            "pressure_on_shell": sp.sstr(pressure_on_shell),
            "radial_curvature_squared": sp.sstr(radial_curvature),
            "physical_gap_squared": sp.sstr(pole_gap_sq),
            "P_Z": sp.sstr(p_z),
            "P_ZZ": sp.sstr(p_zz),
            "sound_speed_squared": sp.sstr(sound_speed_sq),
            "charge_density": sp.sstr(charge_density),
            "charge_compressibility": sp.sstr(compressibility),
            "pure_sextic_rho_squared": sp.sstr(s_sextic),
            "pure_sextic_pressure": sp.sstr(pressure_sextic),
            "pure_sextic_sound_speed_squared": sp.sstr(sound_sextic),
            "static_series": sp.sstr(static_series),
            "high_density_quadratic": sp.sstr(quadratic),
            "high_density_cubic": sp.sstr(cubic),
            "canonical_normalization_F_squared": sp.sstr(canonical_f_sq),
            "cubic_strong_coupling_estimate": sp.sstr(cubic_strong_scale),
            "dispersion_omega_minus_squared": sp.sstr(omega_minus),
            "dispersion_omega_plus_squared": sp.sstr(omega_plus),
        },
        "validation": validation,
        "numerical_grid_rows": len(rows),
        "outputs": {
            "parameter_grid_csv": csv_path.name,
        },
    }
    summary_path = args.output_dir / "uvir001_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(f"Validation status: {'PASS' if validation_pass else 'FAIL'}")
    print("UVIR-001 candidate verdict: FAIL")
    print("Reason: the stable finite-density branch has a nonzero q^2 term and no controlled leading |q|^3 term.")
    print(f"Summary: {summary_path}")
    print(f"Grid: {csv_path}")
    return 0 if validation_pass else 1


if __name__ == "__main__":
    raise SystemExit(run())
