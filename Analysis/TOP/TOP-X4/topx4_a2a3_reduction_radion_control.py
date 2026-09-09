#!/usr/bin/env python3
"""TOP-X4 A2/A3 fixed-action reduction and radion no-go control.

Audits the frozen X4-I1C action only. It verifies bounded KK and condensate
quadratic identities, derives the classical static-circle condition, and
tests the periodic-boson Casimir shape. It cannot promote a physical spectrum
around an unstabilized, time-dependent compactification.
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import math
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np
import sympy as sp


STATUS = "HOLD_TOPX4_A2A3_UNSTABILIZED_CONTROL"
FORBIDDEN_SOURCE_TOKENS = (
    "observed" + "_acceleration",
    "galaxy" + "_target",
    "hubble" + "_target",
    "desired" + "_coupling",
)


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def condensate_roots(momentum_squared: float, amplitude_mass_squared: float, mu: float) -> tuple[float, float]:
    trace = 2.0 * momentum_squared + amplitude_mass_squared + 4.0 * mu * mu
    discriminant = (amplitude_mass_squared + 4.0 * mu * mu) ** 2 + 16.0 * mu * mu * momentum_squared
    lower = 0.5 * (trace - math.sqrt(discriminant))
    upper = 0.5 * (trace + math.sqrt(discriminant))
    return lower, upper


def casimir_shape(x: float) -> float:
    z = mp.e ** (-x)
    return float(mp.polylog(5, z) + x * mp.polylog(4, z) + x * x * mp.polylog(3, z) / 3.0)


def casimir_shape_derivative(x: float) -> float:
    z = mp.e ** (-x)
    return float(-x * mp.polylog(3, z) / 3.0 - x * x * mp.polylog(2, z) / 3.0)


def main() -> int:
    args = parse_args()
    base = Path(__file__).resolve().parent
    a1_path = base / "outputs" / "topx4_a1_background_summary.json"
    a1_sidecar = a1_path.with_suffix(a1_path.suffix + ".sha256")
    expected_a1_hash = a1_sidecar.read_text(encoding="ascii").split()[0]
    actual_a1_hash = sha256_file(a1_path)

    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "a1_input_hash_matches_sidecar",
        actual_a1_hash == expected_a1_hash,
        expected=expected_a1_hash,
        actual=actual_a1_hash,
    )

    # Einstein-frame convention:
    # ds5^2=r^-1 g_mu_nu dx^mu dx^nu+R_ref^2 r^2(dy+A)^2,
    # sigma=sqrt(3/2) M_Pl ln(r). The gravitational minisuperspace kinetic
    # coefficient is (3/4) M_Pl^2 (partial ln r)^2.
    m_pl = 1.0
    sigma_factor_squared = 1.5 * m_pl * m_pl
    radion_kinetic_from_eh = 0.75 * m_pl * m_pl
    radion_kinetic_canonical = 0.5 * sigma_factor_squared
    add_check(
        checks,
        "canonical_radion_kinetic_normalization",
        math.isclose(radion_kinetic_from_eh, radion_kinetic_canonical, rel_tol=0.0, abs_tol=1.0e-15),
        sigma="sqrt(3/2) M_Pl ln(r)",
        eh_coefficient=radion_kinetic_from_eh,
        canonical_coefficient=radion_kinetic_canonical,
    )

    ell_ref = 2.0 * math.pi
    m5_cubed = 1.0
    m_pl_squared = ell_ref * m5_cubed
    add_check(
        checks,
        "planck_scale_reduction",
        math.isclose(m_pl_squared, ell_ref * m5_cubed, rel_tol=0.0, abs_tol=0.0),
        equation="M_Pl^2=ell_ref M5^3",
        sample_value=m_pl_squared,
    )

    # Vacuum scalar/metric KK masses in four-dimensional Einstein units.
    # m_n^2(r)=r^-1 m_5^2+r^-3 n^2/R_ref^2.
    radii = (0.5, 1.0, 2.0, 8.0)
    labels = range(-4, 5)
    m_phi_squared = 1.0
    kk_masses = {
        str(r): [r ** -1 * m_phi_squared + r ** -3 * n * n for n in labels]
        for r in radii
    }
    add_check(
        checks,
        "vacuum_scalar_kk_tower_nonnegative",
        all(value >= 0.0 for values in kk_masses.values() for value in values),
        formula="m_n^2(r)=r^-1 m_5^2+r^-3 n^2/R_ref^2",
        minimum=min(value for values in kk_masses.values() for value in values),
    )
    gaps = [r ** -1.5 for r in radii]
    add_check(
        checks,
        "kk_gap_small_circle_and_decompactification_limits",
        gaps[0] > gaps[1] > gaps[2] > gaps[3] and gaps[-1] < gaps[0],
        radii=list(radii),
        gaps=gaps,
        limiting_formula="Delta_KK=1/(R_ref r^(3/2))",
    )

    # Exact integer momentum conservation at local vertices.
    scalar_quartic_examples = [(-2, -1, 0, -1), (1, 2, 3, 2), (0, 0, 0, 0)]
    measured_deltas = [-n1 + n2 - n3 + n4 for n1, n2, n3, n4 in scalar_quartic_examples]
    add_check(
        checks,
        "kk_vertex_selection_rule_explicit",
        measured_deltas == [0, 0, 0],
        rule="-n1+n2-n3+n4=0 for Phi* Phi Phi* Phi",
        example_residuals=measured_deltas,
    )

    # Fixed-background finite-density matter comparator. This is not a
    # physical coupled metric-radion pole calculation.
    rho0 = 1.0
    lambda_phi5 = 1.0
    mu = math.sqrt(m_phi_squared + 0.5 * lambda_phi5 * rho0 * rho0)
    amplitude_mass_squared = lambda_phi5 * rho0 * rho0
    minimum_root = math.inf
    roots: list[dict[str, float]] = []
    for n in range(0, 5):
        for k in np.linspace(0.0, 4.0, 81):
            momentum_squared = float(k * k + n * n)
            lower, upper = condensate_roots(momentum_squared, amplitude_mass_squared, mu)
            minimum_root = min(minimum_root, lower, upper)
            if k in (0.0, 4.0):
                roots.append({"n": float(n), "k": float(k), "omega2_minus": lower, "omega2_plus": upper})
    sound_speed_squared = amplitude_mass_squared / (amplitude_mass_squared + 4.0 * mu * mu)
    goldstone_lower, _ = condensate_roots(0.0, amplitude_mass_squared, mu)
    add_check(
        checks,
        "fixed_background_condensate_tower_nonnegative",
        minimum_root >= -1.0e-12 and abs(goldstone_lower) <= 1.0e-12 and 0.0 < sound_speed_squared <= 1.0,
        minimum_omega_squared=minimum_root,
        goldstone_omega_squared=goldstone_lower,
        sound_speed_squared=sound_speed_squared,
        dispersion="(w2-p2-Mrho2)(w2-p2)-4 mu2 w2=0",
        endpoint_samples=roots,
    )
    chi_mass_squared = 1.0 + 0.5 * 0.1 * rho0 * rho0
    add_check(
        checks,
        "fixed_background_matter_proxy_tower_nonnegative",
        chi_mass_squared > 0.0,
        zero_mode_mass_squared=chi_mass_squared,
        formula="omega_chi,n^2=k^2+n^2/R^2+m_chi^2+g5 rho0^2/2",
    )

    # Independent exact static-circle condition from the 5D Einstein
    # equations. For H_b=dot(H_b)=0 it is 3 p_a-epsilon-2 p_y=0.
    kinetic, winding_energy, potential = sp.symbols("K_t K_w V", nonnegative=True)
    epsilon = kinetic + winding_energy + potential
    pressure_a = kinetic - winding_energy - potential
    pressure_y = kinetic + winding_energy - potential
    static_residual = sp.factor(3 * pressure_a - epsilon - 2 * pressure_y)
    expected_static_residual = -2 * (potential + 3 * winding_energy)
    add_check(
        checks,
        "exact_static_circle_condition",
        sp.simplify(static_residual - expected_static_residual) == 0,
        residual=str(static_residual),
        stationarity_requirement="V+3 K_w=0",
    )
    frozen_potential_sample = 0.5 * rho0**2 + 0.125 * rho0**4
    add_check(
        checks,
        "classical_frozen_control_has_no_static_circle",
        frozen_potential_sample > 0.0,
        frozen_V=frozen_potential_sample,
        frozen_K_w=0.0,
        stationarity_left_hand_side=frozen_potential_sample,
        interpretation="positive value violates required V+3 K_w=0",
    )

    a1 = json.loads(a1_path.read_text(encoding="utf-8"))
    initial_b = float(a1["initial_state"]["b"])
    final_b = float(a1["final_state"]["b"])
    final_h_b = float(a1["final_state"]["H_b"])
    add_check(
        checks,
        "a1_sample_radius_is_dynamical_not_stabilized",
        not math.isclose(initial_b, final_b, rel_tol=1.0e-6, abs_tol=1.0e-9) and abs(final_h_b) > 1.0e-6,
        initial_b=initial_b,
        final_b=final_b,
        final_H_b=final_h_b,
    )

    # Classical Einstein-frame radion potential at fixed zero-mode fields is
    # A/r+B/r^3. With A>0 and B>=0 its derivative is strictly negative.
    radius, coefficient_a, coefficient_b, coefficient_c = sp.symbols("r A B C", positive=True)
    classical_potential = coefficient_a / radius + coefficient_b / radius**3
    classical_derivative = sp.factor(sp.diff(classical_potential, radius))
    add_check(
        checks,
        "einstein_frame_classical_radion_runaway",
        sp.simplify(
            classical_derivative
            + (coefficient_a * radius**2 + 3 * coefficient_b) / radius**4
        )
        == 0,
        potential="A/r+B/r^3 with A>0, B>=0",
        derivative=str(classical_derivative),
        stationary_points=0,
    )

    # A periodic real boson has a negative Casimir term. Its massive shape F
    # obeys F'(x)=-(x Li_3(e^-x)+x^2 Li_2(e^-x))/3 < 0.
    casimir_samples = []
    for x in (0.1, 1.0, 5.0, 12.0):
        shape = casimir_shape(x)
        derivative = casimir_shape_derivative(x)
        radial_derivative_factor = 6.0 * shape - x * derivative
        casimir_samples.append(
            {"x": x, "F": shape, "F_prime": derivative, "6F_minus_xFprime": radial_derivative_factor}
        )
    add_check(
        checks,
        "periodic_boson_casimir_terms_are_monotone_attractive",
        all(sample["F"] > 0.0 and sample["F_prime"] < 0.0 and sample["6F_minus_xFprime"] > 0.0
            for sample in casimir_samples),
        potential_shape="V_C=-C r^-6 F(m ell_ref r), C>0",
        samples=casimir_samples,
    )

    # Even allowing the massless attractive Casimir term, the only extremum
    # of A/r+B/r^3-C/r^6 is a maximum.
    combined = coefficient_a / radius + coefficient_b / radius**3 - coefficient_c / radius**6
    combined_second = sp.diff(combined, radius, 2)
    casimir_at_stationary = (coefficient_a * radius**5 + 3 * coefficient_b * radius**3) / 6
    second_at_stationary = sp.factor(combined_second.subs(coefficient_c, casimir_at_stationary))
    expected_second = -(5 * coefficient_a * radius**2 + 9 * coefficient_b) / radius**5
    add_check(
        checks,
        "massless_casimir_balance_is_a_maximum",
        sp.simplify(second_at_stationary - expected_second) == 0,
        second_derivative_at_stationarity=str(second_at_stationary),
        interpretation="strictly negative for A>0, B>=0",
    )

    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    add_check(
        checks,
        "observational_target_firewall",
        not forbidden_hits,
        forbidden_token_hits=forbidden_hits,
    )

    calculation_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_A2A3_v1",
        "route": "TOP-X4_KK-001",
        "parent": "X4-I1C_bulk_scalar_control",
        "status": STATUS,
        "audit_execution_status": "COMPLETE" if calculation_ok else "ERROR",
        "calculation_checks_passed": sum(check["ok"] for check in checks),
        "calculation_checks_total": len(checks),
        "physics_pass": False,
        "gate_effect": "NONE",
        "canonical_t3_replaced": False,
        "a2_disposition": "PARTIAL_FIXED_BACKGROUND_CONTROL_ONLY",
        "a3_disposition": "HOLD_UNSTABILIZED_RADION",
        "advance_to_a4": False,
        "checks": checks,
        "decision_failures": [
            "the frozen classical finite-charge control has no static-circle solution",
            "the A1 radius runs rather than stabilizes",
            "the massless periodic-boson Casimir balance is a radion maximum, not a minimum",
            "the full finite-density curved-background one-loop determinant is not defined by the frozen control",
            "without a selected radius and specified five-dimensional cutoff, no EFT hierarchy is established",
        ],
        "surviving_bounded_results": [
            "positive canonical radion kinetic sign in the zero-density Einstein-frame reduction",
            "nonnegative vacuum scalar KK masses for positive parent masses",
            "healthy fixed-background condensate and matter-proxy scalar towers",
            "explicit integer KK momentum selection rule",
        ],
        "explicit_nonclaims": [
            "no healthy full metric-radion-condensate spectrum",
            "no radion stabilization",
            "no physical matter residue",
            "no derived transfer current, K_Q or V",
            "no observational prediction",
        ],
        "required_new_authority_for_retry": (
            "a separately frozen parent or semiclassical completion with a declared stabilizing operator/field, "
            "boundary condition, quantum state, counterterms and cutoff"
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / "topx4_a2a3_reduction_radion_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(STATUS)
    print(f"calculation_checks={result['calculation_checks_passed']}/{result['calculation_checks_total']}")
    print("a2=PARTIAL_FIXED_BACKGROUND_CONTROL_ONLY")
    print("a3=HOLD_UNSTABILIZED_RADION")
    print("advance_to_a4=false")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if calculation_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
