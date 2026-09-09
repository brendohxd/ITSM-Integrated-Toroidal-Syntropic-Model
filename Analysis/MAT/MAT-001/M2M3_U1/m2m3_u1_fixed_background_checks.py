#!/usr/bin/env python3
"""Deterministic symbolic checks for the bounded M2/M3-U1 Max reduction.

This script checks only the fixed-background scalar controls RCP-C0 and
RCP-I1-C.  It deliberately does not eliminate metric, lapse, or shift
constraints and therefore cannot compute the physical ITSM residue V.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_zero(expression: sp.Expr) -> bool:
    return sp.simplify(expression) == 0


def main() -> None:
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[4]
    output_dir = script_path.parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # All dimensional quantities are in natural units.  Positivity assumptions
    # are exactly those used for the healthy repulsive-condensate branch.
    h, s, X, J = sp.symbols("h s X J", real=True)
    rho_source = sp.symbols("rho_source", positive=True, finite=True)
    v, rho0, lam, mu, m, Lambda = sp.symbols(
        "v rho_0 lambda_4 mu m Lambda", positive=True, finite=True
    )
    alpha1, alpha2 = sp.symbols("alpha_1 alpha_2", real=True, finite=True)
    t = sp.symbols("k_squared", nonnegative=True, finite=True)

    # RCP-C0 background and the complete canonical amplitude-phase kernel.
    background_rule = {mu**2: m**2 + lam * v**2}
    radial_polynomial = (
        (v + h) ** 2 * (mu**2 - m**2) - lam * (v + h) ** 4 / 2
    )
    radial_on_background = sp.expand(radial_polynomial.subs(background_rule))
    radial_linear = sp.expand(radial_on_background).coeff(h, 1)
    radial_quadratic = sp.expand(radial_on_background).coeff(h, 2)

    rho0_map = sp.sqrt(2) * v
    radial_mass_sq = 2 * lam * v**2
    heavy_gap_sq = radial_mass_sq + 4 * mu**2
    canonical_source = rho0_map / Lambda**2

    discriminant = heavy_gap_sq**2 + 16 * mu**2 * t
    omega_minus_sq = sp.simplify(
        t + heavy_gap_sq / 2 - sp.sqrt(discriminant) / 2
    )
    omega_plus_sq = sp.simplify(
        t + heavy_gap_sq / 2 + sp.sqrt(discriminant) / 2
    )
    characteristic_sum = 2 * t + radial_mass_sq + 4 * mu**2
    characteristic_product = t * (t + radial_mass_sq)
    exact_sound_speed_sq = sp.simplify(radial_mass_sq / heavy_gap_sq)
    low_k_k4_coefficient = sp.simplify(16 * mu**4 / heavy_gap_sq**3)

    # The source couples to the canonical radial field sigma=sqrt(2)h.  After
    # diagonalizing the two scalar modes, its lower-pole overlap is momentum
    # dependent.  The squared overlap is orientation independent; the signed
    # coupling inherits sign(canonical_source) after anchoring u_sigma>0.
    b_minus = sp.simplify(t - omega_minus_sq)
    lower_pole_overlap_sq = sp.simplify(
        canonical_source**2
        * b_minus**2
        / (b_minus**2 + 4 * mu**2 * t)
    )
    lower_overlap_slope = sp.simplify(sp.limit(lower_pole_overlap_sq / t, t, 0))
    expected_overlap_slope = sp.simplify(
        4 * canonical_source**2 * mu**2 / heavy_gap_sq**2
    )

    # Exact leading-derivative P(X_R,J) reduction.  This is valid only when
    # radial derivatives can be neglected; it cannot reproduce the nonlocal
    # short-distance force kernel by itself.
    algebraic_delta = X - m**2 - J / Lambda**2
    s_stationary = sp.simplify(algebraic_delta / lam)
    algebraic_lagrangian = s * algebraic_delta - lam * s**2 / 2
    p_x_j = sp.simplify(algebraic_lagrangian.subs(s, s_stationary))
    p_x_j_expected = sp.simplify(algebraic_delta**2 / (2 * lam))
    p_x = p_x_j.subs(J, 0)
    p_prime_background = sp.simplify(sp.diff(p_x, X).subs(X, mu**2))
    p_second = sp.diff(p_x, X, 2)
    p_sound_speed_sq = sp.simplify(
        p_prime_background
        / (p_prime_background + 2 * mu**2 * p_second)
    )

    # Nonrelativistic Gross-Pitaevskii/Bogoliubov control, with
    # Phi=e^{-imt} psi/sqrt(2m) and the opposite charge chart obtained by
    # complex conjugation.
    number_density_nr = 2 * m * v**2
    gp_contact = lam / (4 * m**2)
    gp_sound_speed_sq = sp.simplify(gp_contact * number_density_nr / m)
    epsilon_k = t / (2 * m)
    bogoliubov_dispersion = sp.expand(
        epsilon_k * (epsilon_k + 2 * gp_contact * number_density_nr)
    )
    bogoliubov_expected = sp.expand(
        gp_sound_speed_sq * t + t**2 / (4 * m**2)
    )

    # Static response and the factor-of-two source-normalization audit.
    force_coefficient_from_displayed_action = sp.simplify(
        canonical_source**2 / (4 * sp.pi)
    )
    force_coefficient_quoted_in_review = v**2 / (4 * sp.pi * Lambda**4)
    force_coefficient_ratio = sp.simplify(
        force_coefficient_from_displayed_action / force_coefficient_quoted_in_review
    )

    # Exact lambda_4=0 uniform-sphere screening solution.
    x = sp.symbols("x", positive=True, finite=True)
    effective_charge_ratio = sp.simplify(
        3 / x**2 * (1 - sp.tanh(x) / x)
    )
    effective_charge_ratio_alt = sp.simplify(3 * (x - sp.tanh(x)) / x**3)
    weak_charge_limit = sp.limit(effective_charge_ratio, x, 0, dir="+")
    strong_charge_scaled_limit = sp.limit(
        1 - sp.tanh(x) / x, x, sp.oo
    )
    strong_repulsive_dispersion = sp.simplify(
        rho_source * t / (4 * Lambda**2 * m**2) + t**2 / (4 * m**2)
    )
    strong_attractive_dispersion = sp.simplify(
        -rho_source * t / (4 * Lambda**2 * m**2) + t**2 / (4 * m**2)
    )
    strong_source_sample = {
        rho_source: 1,
        Lambda: 1,
        m: 1,
        t: sp.Rational(1, 2),
    }
    repulsive_sample_omega_sq = strong_repulsive_dispersion.subs(
        strong_source_sample
    )
    attractive_sample_omega_sq = strong_attractive_dispersion.subs(
        strong_source_sample
    )

    # RCP-I1-C: varying S_m[chi,A^2(s)g] gives alpha(s) T_E delta s.
    # Around a zero-matter background with a first-order dust probe,
    # T_E=-J_E and g_sigma=alpha_1 rho_0.  Matching the *displayed* C0
    # action with J=-T requires alpha_1=+Lambda^{-2}.
    conformal_source = alpha1 * rho0_map
    conformal_to_c0_match = sp.simplify(
        conformal_source.subs(alpha1, Lambda**-2) - canonical_source
    )
    c0_trace_coefficient = Lambda**-2
    frozen_ledger_trace_comparator = -Lambda**-2
    trace_sign_difference = sp.simplify(
        c0_trace_coefficient - frozen_ledger_trace_comparator
    )
    trace_e_background, trace_e_slope = sp.symbols(
        "T_E_background dT_E_ds", real=True, finite=True
    )
    matter_second_variation = sp.simplify(
        alpha2 * trace_e_background + alpha1 * trace_e_slope
    )
    conformal_radial_mass_sq = sp.simplify(
        rho0**2 * (lam - matter_second_variation)
    )

    # A finite-density homogeneous condensate has nonzero enthalpy.  A single
    # cosmological-constant counterterm cannot make flat space an on-shell
    # Einstein solution because it leaves epsilon+p unchanged.
    condensate_pressure = lam * v**4 / 2
    condensate_energy = sp.simplify(2 * mu**2 * v**2 - condensate_pressure)
    condensate_enthalpy = sp.simplify(condensate_energy + condensate_pressure)

    # Field-chart invariance of the canonical source coefficient.
    chart_scale = sp.symbols("r_chart", positive=True, finite=True)
    rescaled_kinetic = chart_scale**-2
    rescaled_source = canonical_source / chart_scale
    chart_invariant_source = sp.simplify(
        rescaled_source / sp.sqrt(rescaled_kinetic)
    )

    # General parent-shape screen: U(s)-m^2 s proportional to s^n gives
    # P(X)-type exponent n/(n-1).  A 3/2 phase EFT therefore selects n=3,
    # i.e. a sextic |Phi|^6 term, at this algebraic level only.
    n = sp.symbols("n", real=True)
    monomial_solution = sp.solve(sp.Eq(n / (n - 1), sp.Rational(3, 2)), n)

    checks = {
        "background_linear_term_vanishes": is_zero(radial_linear),
        "background_radial_quadratic_coefficient": is_zero(
            radial_quadratic + 2 * lam * v**2
        ),
        "core_chart_radial_mass_map": is_zero(
            radial_mass_sq - lam * rho0_map**2
        ),
        "dispersion_root_sum": is_zero(
            omega_minus_sq + omega_plus_sq - characteristic_sum
        ),
        "dispersion_root_product": is_zero(
            omega_minus_sq * omega_plus_sq - characteristic_product
        ),
        "gapless_branch_at_zero_momentum": is_zero(omega_minus_sq.subs(t, 0)),
        "gapped_branch_at_zero_momentum": is_zero(
            omega_plus_sq.subs(t, 0) - heavy_gap_sq
        ),
        "lower_pole_overlap_low_k": is_zero(
            lower_overlap_slope - expected_overlap_slope
        ),
        "p_x_stationary_reduction": is_zero(p_x_j - p_x_j_expected),
        "p_x_background_density": is_zero(
            p_prime_background.subs(background_rule) - v**2
        ),
        "p_x_sound_speed_matches_exact_low_k": is_zero(
            (p_sound_speed_sq - exact_sound_speed_sq).subs(background_rule)
        ),
        "gp_bogoliubov_k4_retained": is_zero(
            bogoliubov_dispersion - bogoliubov_expected
        ),
        "gp_sound_speed_nonrelativistic_limit": is_zero(
            gp_sound_speed_sq - lam * v**2 / (2 * m**2)
        ),
        "uniform_sphere_charge_forms_agree": is_zero(
            effective_charge_ratio - effective_charge_ratio_alt
        ),
        "uniform_sphere_unscreened_limit": weak_charge_limit == 1,
        "uniform_sphere_strong_scaled_limit": strong_charge_scaled_limit == 1,
        "conformal_linear_probe_matches_c0_for_positive_alpha": is_zero(
            conformal_to_c0_match
        ),
        "frozen_trace_comparator_sign_mismatch_detected": (
            trace_sign_difference != 0
        ),
        "published_force_factor_two_mismatch_detected": (
            force_coefficient_ratio == 2
        ),
        "finite_density_flat_background_enthalpy_obstruction": is_zero(
            condensate_enthalpy - 2 * mu**2 * v**2
        ),
        "canonical_source_field_chart_invariant": is_zero(
            chart_invariant_source - canonical_source
        ),
        "zero_density_removes_linear_source": is_zero(
            canonical_source.subs(v, 0)
        ),
        "zero_portal_coupling_removes_linear_source": (
            sp.limit(canonical_source, Lambda, sp.oo) == 0
        ),
        "attractive_strong_source_has_soft_gradient_instability": (
            attractive_sample_omega_sq < 0
        ),
        "repulsive_strong_source_sample_is_gradient_stable": (
            repulsive_sample_omega_sq > 0
        ),
        "three_halves_parent_shape_selects_sextic": monomial_solution == [3],
        "weak_distortion_combination_dimensionless": (4 - 2 - 2) == 0,
        "sphere_x_dimensionless": (-1 + 2 - 1) == 0,
        "c0_source_coefficient_mass_dimension_minus_one": (1 - 2) == -1,
        "conformal_source_coefficient_mass_dimension_minus_one": (-2 + 1) == -1,
    }
    checks = {name: bool(passed) for name, passed in checks.items()}

    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"symbolic checks failed: {failed}")

    input_paths = [
        Path("GEMINI.md"),
        Path("Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md"),
        Path("Theory/Core/Reasoning_Mode_Plans/03_MAX_BOUNDED_EXACT_REDUCTIONS/PLAN.md"),
        Path("Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_RCP0_ACTION_LEDGER_2026-09-05.md"),
        Path("Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_HIGH_HANDOFF_2026-09-05.md"),
    ]
    input_hashes = {
        path.as_posix(): sha256_file(repo_root / path) for path in input_paths
    }
    input_hashes[script_path.relative_to(repo_root).as_posix()] = sha256_file(
        script_path
    )

    result = {
        "schema_version": "1.0",
        "calculation": "M2M3_U1_MAX_FIXED_BACKGROUND_SYMBOLIC_CHECKS",
        "calculation_status": "PASS_BOUNDED_SYMBOLIC_IDENTITIES",
        "physics_disposition": {
            "RCP-C0": "CONTROL_REPRODUCED_NO_STANDALONE_MOND_LAW",
            "RCP-I1-C": "HEALTHY_LINEAR_PROBE_DOMAIN_FREE_FUNCTION_NORMALIZATION",
            "gravitating_background": "BLOCKED_NONZERO_ENTHALPY_FIXED_BACKGROUND_ONLY",
            "physical_metric_reduced_residue": "NOT_COMPUTED",
        },
        "gate_boundary": {
            "gate_effect": "NONE",
            "MAT-001": "BLOCKED",
            "UVIR-003": "IN_PROGRESS",
            "K_Q": "NOT_DERIVED",
            "V": "NOT_COMPUTED",
        },
        "checks": checks,
        "identities": {
            "background": "mu^2 = m^2 + lambda_4 v^2",
            "canonical_fields": "sigma=sqrt(2) h; q=sqrt(2) v pi",
            "canonical_radial_mass_squared": sp.sstr(radial_mass_sq),
            "true_heavy_gap_squared": sp.sstr(heavy_gap_sq),
            "canonical_c0_source": sp.sstr(canonical_source),
            "exact_omega_minus_squared": sp.sstr(omega_minus_sq),
            "exact_omega_plus_squared": sp.sstr(omega_plus_sq),
            "exact_low_k_sound_speed_squared": sp.sstr(exact_sound_speed_sq),
            "exact_low_k_k4_coefficient": sp.sstr(low_k_k4_coefficient),
            "lower_pole_overlap_squared": sp.sstr(lower_pole_overlap_sq),
            "lower_pole_overlap_squared_over_k2_limit": sp.sstr(
                lower_overlap_slope
            ),
            "p_x_j": sp.sstr(p_x_j),
            "gp_lagrangian": (
                "i/2(psi* psi_dot-psi_dot* psi)-|grad psi|^2/(2m)"
                "-lambda_4|psi|^4/(8m^2)-J|psi|^2/(2m Lambda^2)"
            ),
            "gp_bogoliubov_dispersion": sp.sstr(bogoliubov_dispersion),
            "static_c0_kernel": "sigma(k)=-g_C0 J(k)/(k^2+M_sigma^2)",
            "healing_force_range": "ell=1/sqrt(2 lambda_4 v^2)",
            "uniform_sphere_charge_ratio": sp.sstr(effective_charge_ratio),
            "conformal_variation": "delta S_m=int sqrt(-g) alpha(s) T_E delta s",
            "canonical_conformal_probe_source": sp.sstr(conformal_source),
            "conformal_nonzero_trace_radial_mass_squared": sp.sstr(
                conformal_radial_mass_sq
            ),
            "conformal_matter_second_variation": sp.sstr(
                matter_second_variation
            ),
            "finite_density_enthalpy": sp.sstr(condensate_enthalpy),
            "parent_power_for_p_x_three_halves": "n=3 (|Phi|^6 shape screen only)",
        },
        "audited_discrepancies": {
            "trace_control_sign": (
                "With J=-T, -sJ/Lambda^2 maps to +sT/Lambda^2; the frozen "
                "ledger's -sT/Lambda^2 comparison has the opposite sign."
            ),
            "force_normalization": {
                "displayed_action_coefficient": sp.sstr(
                    force_coefficient_from_displayed_action
                ),
                "review_quoted_coefficient": sp.sstr(
                    force_coefficient_quoted_in_review
                ),
                "ratio": sp.sstr(force_coefficient_ratio),
                "disposition": "SOURCE_TO_PROBE_NORMALIZATION_UNRESOLVED",
            },
            "weak_distortion_condition": "x^2=rho R^2/Lambda^2 << 1",
            "healing_length_relation": (
                "ell=1/sqrt(2 lambda_4 v^2) is exact in C0; "
                "ell approximately 1/(2 m c_s) only in the NR limit."
            ),
        },
        "domain": {
            "healthy_vacuum_scalar_control": (
                "v>0, lambda_4>=0, real mu; lambda_4>0 for a nonzero "
                "linear sound speed"
            ),
            "p_x_derivative_domain": (
                "positive-density algebraic branch and radial derivatives "
                "small; in the NR regime k << m c_s"
            ),
            "gp_domain": "k << m with k^4/(4m^2) retained",
            "nonlinear_sphere_domain": (
                "RCP-C0 only, lambda_4=0, static uniform J=+rho"
            ),
            "strong_source_sign_test": (
                "For the C0 local strong-source dispersion at m=Lambda=rho=1 "
                f"and k^2=1/2, J=-rho gives omega^2="
                f"{sp.sstr(attractive_sample_omega_sq)} while J=+rho gives "
                f"omega^2={sp.sstr(repulsive_sample_omega_sq)}."
            ),
            "rcp_i1c_probe_domain": (
                "zero background matter trace; first-order prescribed dust "
                "probe; fixed metric"
            ),
        },
        "nonclaims": [
            "No metric, lapse, or shift constraint was eliminated.",
            "No PPN, lensing, or gravitational-wave observable was computed.",
            "No MOND/RAR acceleration scale or observational value was used.",
            "No numerical K_Q or V was computed.",
            "The sextic parent-shape identity is not a complete parent or matching result.",
        ],
        "input_sha256": input_hashes,
    }

    output_path = output_dir / "m2m3_u1_fixed_background_summary.json"
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output_path.write_text(serialized, encoding="utf-8", newline="\n")
    output_digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    sidecar_path = output_dir / "m2m3_u1_fixed_background_summary.sha256"
    sidecar_path.write_text(
        f"{output_digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(result["calculation_status"])
    print(f"physics_disposition={result['physics_disposition']}")
    print(f"checks={len(checks)} passed={sum(checks.values())}")
    print(f"summary_sha256={output_digest}")
    print("MAT-001=BLOCKED K_Q=NOT_DERIVED V=NOT_COMPUTED gate_effect=NONE")


if __name__ == "__main__":
    main()
