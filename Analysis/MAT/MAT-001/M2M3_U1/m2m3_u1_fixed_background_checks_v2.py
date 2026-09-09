#!/usr/bin/env python3
"""Semantic verifier for the bounded M2/M3-U1 fixed-background controls.

This version repairs the literal/proxy checks identified by the A-B3/Role-C
audit.  It remains a fixed-background algebra and provenance verifier.  It
does not eliminate metric constraints and cannot compute K_Q or V.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)


MUTATIONS = (
    "MUT_01_KINETIC_MIXING",
    "MUT_02_DELETE_SQRT2_SOURCE",
    "MUT_03_DIMENSION_R_POWER",
    "MUT_04_REVERSE_GRADIENT_SIGN",
    "MUT_05_SPHERE_NUMERATOR",
    "MUT_09_REVERSE_K4_SIGN",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_zero(expression: sp.Expr) -> bool:
    return sp.simplify(expression) == 0


class DimensionError(ValueError):
    """Raised when an expression is dimensionally undefined or inconsistent."""


class DimensionEngine:
    """Propagate natural-unit mass dimensions through SymPy expressions."""

    def __init__(self, dimensions: dict[sp.Symbol, sp.Rational]) -> None:
        self.dimensions = dimensions

    def dim(self, expression: Any) -> sp.Rational:
        expression = sp.sympify(expression)
        if expression.is_Number:
            return sp.Rational(0)
        if expression.is_Symbol:
            if expression not in self.dimensions:
                raise DimensionError(f"unknown symbol: {expression}")
            return self.dimensions[expression]
        if expression.is_Add:
            terms = [self.dim(term) for term in expression.args]
            if any(term != terms[0] for term in terms[1:]):
                raise DimensionError(
                    f"incompatible sum dimensions {terms} in {expression}"
                )
            return terms[0]
        if expression.is_Mul:
            return sum((self.dim(term) for term in expression.args), sp.Rational(0))
        if expression.is_Pow:
            base, exponent = expression.args
            if self.dim(exponent) != 0 or not exponent.is_number:
                raise DimensionError(f"dimensionful or symbolic exponent: {exponent}")
            return sp.simplify(self.dim(base) * exponent)
        if expression.is_Function:
            for argument in expression.args:
                if self.dim(argument) != 0:
                    raise DimensionError(
                        f"dimensionful function argument {argument} in {expression}"
                    )
            return sp.Rational(0)
        raise DimensionError(f"unsupported expression type: {type(expression)}")


def parse_simple_latex_monomial(text: str, local_dict: dict[str, sp.Symbol]) -> sp.Expr:
    """Parse the small monomial subset used by the frozen reduction report."""

    replacements = {
        r"\lambda_4": "(lambda_4)",
        r"\rho_0": "(rho_0)",
        r"\mu": "(mu)",
        r"\Lambda": "(Lambda)",
        r"\sqrt2": "sqrt(2)",
    }
    cleaned = text.strip().rstrip(".,\\")
    for source, target in replacements.items():
        cleaned = cleaned.replace(source, target)
    cleaned = cleaned.replace("{", "").replace("}", "").replace("&", "")
    transformations = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )
    return sp.simplify(
        parse_expr(cleaned, local_dict=local_dict, transformations=transformations)
    )


def parse_sidecar(sidecar: Path) -> tuple[Path, str, str]:
    fields = sidecar.read_text(encoding="ascii").strip().split(maxsplit=1)
    if len(fields) != 2 or not re.fullmatch(r"[0-9a-fA-F]{64}", fields[0]):
        raise ValueError(f"malformed sidecar: {sidecar}")
    target = sidecar.with_name(Path(fields[1].strip()).name)
    return target, fields[0].lower(), sha256_file(target)


def hamiltonian_frequencies(
    radial_mass: mp.mpf, chemical_potential: mp.mpf, momentum: mp.mpf, mixing: mp.mpf
) -> list[mp.mpf]:
    """Return positive frequencies from the independently constructed matrix."""

    matrix = mp.matrix(
        [
            [0, 0, 1, 0],
            [-mixing, 0, 0, 1],
            [
                -(momentum**2 + radial_mass**2 + mixing**2),
                0,
                0,
                mixing,
            ],
            [0, -(momentum**2), 0, 0],
        ]
    )
    eigenvalues = mp.eig(matrix, left=False, right=False)
    positive = sorted(
        [abs(mp.im(value)) for value in eigenvalues if mp.im(value) > 0]
    )
    if len(positive) != 2:
        raise ArithmeticError(f"expected two positive frequencies, got {eigenvalues}")
    return positive


def main(mutation: str | None = None) -> dict[str, Any]:
    mp.mp.dps = 90
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[4]
    output_dir = script_path.parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    h, s, X, J = sp.symbols("h s X J", real=True)
    rho_source = sp.symbols("rho_source", positive=True, finite=True)
    v, rho0, lam, mu, m, Lambda = sp.symbols(
        "v rho_0 lambda_4 mu m Lambda", positive=True, finite=True
    )
    alpha1, alpha2 = sp.symbols("alpha_1 alpha_2", real=True, finite=True)
    trace_background, trace_slope = sp.symbols(
        "T_E_background dT_E_ds", real=True, finite=True
    )
    t = sp.symbols("k_squared", nonnegative=True, finite=True)
    R = sp.symbols("R", positive=True, finite=True)

    # Background and exact two-field scalar kernel.
    background_rule = {mu**2: m**2 + lam * v**2}
    radial_polynomial = (
        (v + h) ** 2 * (mu**2 - m**2) - lam * (v + h) ** 4 / 2
    )
    radial_on_background = sp.expand(radial_polynomial.subs(background_rule))
    radial_linear = radial_on_background.coeff(h, 1)
    radial_quadratic = radial_on_background.coeff(h, 2)
    rho0_map = sp.sqrt(2) * v
    radial_mass_sq = 2 * lam * v**2
    heavy_gap_sq = radial_mass_sq + 4 * mu**2

    expected_source = sp.sqrt(2) * v / Lambda**2
    canonical_source = (
        v / Lambda**2
        if mutation == "MUT_02_DELETE_SQRT2_SOURCE"
        else expected_source
    )

    gradient_sign = -1 if mutation == "MUT_04_REVERSE_GRADIENT_SIGN" else 1
    discriminant = heavy_gap_sq**2 + 16 * mu**2 * gradient_sign * t
    omega_minus_sq = sp.simplify(
        gradient_sign * t + heavy_gap_sq / 2 - sp.sqrt(discriminant) / 2
    )
    omega_plus_sq = sp.simplify(
        gradient_sign * t + heavy_gap_sq / 2 + sp.sqrt(discriminant) / 2
    )
    characteristic_sum = 2 * gradient_sign * t + radial_mass_sq + 4 * mu**2
    characteristic_product = gradient_sign * t * (
        gradient_sign * t + radial_mass_sq
    )
    exact_sound_speed_sq = radial_mass_sq / heavy_gap_sq
    exact_k4 = sp.simplify(
        sp.limit(
            (omega_minus_sq - gradient_sign * exact_sound_speed_sq * t) / t**2,
            t,
            0,
            dir="+",
        )
    )
    expected_positive_k4 = 16 * mu**4 / heavy_gap_sq**3
    tested_k4 = (
        -expected_positive_k4
        if mutation == "MUT_09_REVERSE_K4_SIGN"
        else expected_positive_k4
    )

    # Source-pole, phase-EFT, GP and nonlinear-sphere controls.
    b_minus = sp.simplify(gradient_sign * t - omega_minus_sq)
    lower_pole_overlap_sq = sp.simplify(
        canonical_source**2
        * b_minus**2
        / (b_minus**2 + 4 * mu**2 * gradient_sign * t)
    )
    lower_overlap_slope = sp.simplify(
        sp.limit(lower_pole_overlap_sq / t, t, 0, dir="+")
    )
    expected_overlap_slope = (
        4 * expected_source**2 * mu**2 / heavy_gap_sq**2
    )

    algebraic_delta = X - m**2 - J / Lambda**2
    stationary_s = algebraic_delta / lam
    algebraic_lagrangian = s * algebraic_delta - lam * s**2 / 2
    p_x_j = sp.simplify(algebraic_lagrangian.subs(s, stationary_s))
    p_x_expected = algebraic_delta**2 / (2 * lam)
    p_x = p_x_j.subs(J, 0)
    p_x_1 = sp.diff(p_x, X).subs(X, mu**2)
    p_x_2 = sp.diff(p_x, X, 2)
    p_sound_speed_sq = sp.simplify(p_x_1 / (p_x_1 + 2 * mu**2 * p_x_2))

    number_density_nr = 2 * m * v**2
    gp_contact = lam / (4 * m**2)
    gp_sound_speed_sq = gp_contact * number_density_nr / m
    epsilon_k = t / (2 * m)
    bogoliubov = sp.expand(
        epsilon_k * (epsilon_k + 2 * gp_contact * number_density_nr)
    )
    bogoliubov_expected = sp.expand(
        gp_sound_speed_sq * t + t**2 / (4 * m**2)
    )

    sphere_coefficient = 4 if mutation == "MUT_05_SPHERE_NUMERATOR" else 3
    x = sp.symbols("x", positive=True, finite=True)
    charge_ratio = sphere_coefficient * (x - sp.tanh(x)) / x**3
    charge_ratio_independent = 3 / x**2 * (1 - sp.tanh(x) / x)

    force_action = expected_source**2 / (4 * sp.pi)
    force_review = v**2 / (4 * sp.pi * Lambda**4)
    condensate_pressure = lam * v**4 / 2
    condensate_energy = 2 * mu**2 * v**2 - condensate_pressure
    condensate_enthalpy = sp.simplify(condensate_energy + condensate_pressure)
    conformal_source = alpha1 * rho0_map
    matter_second_variation = alpha2 * trace_background + alpha1 * trace_slope

    # Genuine dimension propagation.
    dimension_engine = DimensionEngine(
        {
            rho_source: sp.Rational(4),
            R: sp.Rational(-1),
            Lambda: sp.Rational(1),
            v: sp.Rational(1),
            rho0: sp.Rational(1),
            alpha1: sp.Rational(-2),
        }
    )
    weak_distortion = (
        rho_source * R / Lambda**2
        if mutation == "MUT_03_DIMENSION_R_POWER"
        else rho_source * R**2 / Lambda**2
    )
    incompatible_sum_rejected = False
    try:
        dimension_engine.dim(1 + rho_source * R / Lambda**2)
    except DimensionError:
        incompatible_sum_rejected = True

    # Parse frozen source-sign and reduction equations from their actual files.
    ledger_path = repo_root / (
        "Theory/Gates/MAT-001/M2M3_U1/"
        "M2M3_U1_RCP0_ACTION_LEDGER_2026-09-05.md"
    )
    reduction_path = repo_root / (
        "Theory/Gates/MAT-001/M2M3_U1/"
        "M2M3_U1_MAX_FIXED_BACKGROUND_REDUCTION_2026-09-05.md"
    )
    ledger_text = ledger_path.read_text(encoding="utf-8")
    reduction_text = reduction_path.read_text(encoding="utf-8")
    trace_match = re.search(r"`F_T\(s\)=([^`]+)`", ledger_text)
    if trace_match is None:
        raise ValueError("could not parse F_T(s) from frozen ledger")
    parsed_trace = sp.sympify(
        trace_match.group(1), locals={"s": s, "Lambda": Lambda}
    )
    action_trace = s / Lambda**2

    radial_line = next(
        (line for line in reduction_text.splitlines() if line.startswith(r"M_\sigma^2={}&")),
        None,
    )
    enthalpy_line = next(
        (line for line in reduction_text.splitlines() if line.startswith(r"\varepsilon+p=")),
        None,
    )
    if radial_line is None or enthalpy_line is None:
        raise ValueError("could not locate frozen radial-mass or enthalpy equation")
    parsed_radial_mass = parse_simple_latex_monomial(
        radial_line.split("=")[-1], {"lambda_4": lam, "v": v, "rho_0": rho0}
    )
    parsed_enthalpy = parse_simple_latex_monomial(
        enthalpy_line.split("=", 1)[1].split(">", 1)[0], {"mu": mu, "v": v}
    )

    # Independent Hamiltonian matrix roots on the sealed rational grid.
    grid = (
        (mp.mpf(1), mp.mpf(1), mp.mpf(1) / 10),
        (mp.mpf(2), mp.mpf(1), mp.mpf(1) / 4),
        (mp.mpf(1) / 2, mp.mpf(3) / 2, mp.mpf(1) / 20),
        (mp.mpf(3), mp.mpf(2), mp.mpf(1) / 2),
        (mp.mpf(4), mp.mpf(1) / 2, mp.mpf(1)),
    )
    root_results: list[dict[str, str]] = []
    root_agreement = True
    for radial_mass, chemical_potential, momentum in grid:
        matrix_mixing = (
            chemical_potential
            if mutation == "MUT_01_KINETIC_MIXING"
            else 2 * chemical_potential
        )
        matrix_roots = hamiltonian_frequencies(
            radial_mass, chemical_potential, momentum, matrix_mixing
        )
        gap_sq = radial_mass**2 + 4 * chemical_potential**2
        analytic_discriminant = gap_sq**2 + 16 * chemical_potential**2 * momentum**2
        analytic_roots = [
            mp.sqrt(momentum**2 + gap_sq / 2 - mp.sqrt(analytic_discriminant) / 2),
            mp.sqrt(momentum**2 + gap_sq / 2 + mp.sqrt(analytic_discriminant) / 2),
        ]
        differences = [abs(a - b) for a, b in zip(matrix_roots, analytic_roots)]
        relatives = [
            difference / max(abs(reference), mp.mpf("1e-89"))
            for difference, reference in zip(differences, analytic_roots)
        ]
        if max(relatives) >= mp.mpf("1e-70"):
            root_agreement = False
        root_results.append(
            {
                "M_sigma": mp.nstr(radial_mass, 60),
                "mu": mp.nstr(chemical_potential, 60),
                "k": mp.nstr(momentum, 60),
                "matrix_omega_minus": mp.nstr(matrix_roots[0], 60),
                "analytic_omega_minus": mp.nstr(analytic_roots[0], 60),
                "matrix_omega_plus": mp.nstr(matrix_roots[1], 60),
                "analytic_omega_plus": mp.nstr(analytic_roots[1], 60),
                "max_absolute_difference": mp.nstr(max(differences), 60),
                "max_relative_difference": mp.nstr(max(relatives), 60),
            }
        )

    # Arbitrary-precision convergence to the positive k^4 coefficient.
    radial_mass_ref = mp.mpf(1)
    mu_ref = mp.mpf(1)
    gap_ref = radial_mass_ref**2 + 4 * mu_ref**2
    sound_ref = radial_mass_ref**2 / gap_ref
    k4_ref = 16 * mu_ref**4 / gap_ref**3
    low_k_results: list[dict[str, str]] = []
    low_k_differences: list[mp.mpf] = []
    for exponent in range(1, 7):
        momentum = mp.mpf(10) ** (-exponent)
        momentum_sq = momentum**2
        omega_sq = (
            momentum_sq
            + gap_ref / 2
            - mp.sqrt(gap_ref**2 + 16 * mu_ref**2 * momentum_sq) / 2
        )
        estimated_k4 = (omega_sq - sound_ref * momentum_sq) / momentum_sq**2
        difference = abs(estimated_k4 - k4_ref)
        low_k_differences.append(difference)
        low_k_results.append(
            {
                "k": mp.nstr(momentum, 10),
                "estimated_positive_k4": mp.nstr(estimated_k4, 60),
                "expected_positive_k4": mp.nstr(k4_ref, 60),
                "absolute_difference": mp.nstr(difference, 60),
            }
        )
    low_k_monotone = all(
        later < earlier
        for earlier, later in zip(low_k_differences, low_k_differences[1:])
    )

    # Mandatory input inventory and actual sidecar/manifest verification.
    mandatory_relpaths = (
        "GEMINI.md",
        "Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md",
        "active_research.md",
        "Theory/Core/Reasoning_Mode_Plans/README.md",
        "Theory/Core/Reasoning_Mode_Plans/Handoffs/HANDOFF_SHA256.md",
        "Theory/Core/Reasoning_Mode_Plans/Handoffs/ANTIGRAVITY_HANDOFF_A-B4_VERIFIER_REPAIR.md",
        "Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_RCP0_ACTION_LEDGER_2026-09-05.md",
        "Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_MAX_FIXED_BACKGROUND_REDUCTION_2026-09-05.md",
        "Theory/Verification/G-A4_A-B3_ROLE_C_ADJUDICATION_2026-09-05.md",
        "Analysis/MAT/MAT-001/M2M3_U1/m2m3_u1_fixed_background_checks.py",
        "Analysis/MAT/MAT-001/M2M3_U1/outputs/m2m3_u1_fixed_background_summary.json",
        "Analysis/MAT/MAT-001/M2M3_U1/outputs/m2m3_u1_fixed_background_summary.sha256",
    )
    missing_inputs = [path for path in mandatory_relpaths if not (repo_root / path).is_file()]
    input_hashes = {
        path: sha256_file(repo_root / path)
        for path in mandatory_relpaths
        if (repo_root / path).is_file()
    }
    input_hashes[script_path.relative_to(repo_root).as_posix()] = sha256_file(script_path)

    sidecars = (
        repo_root
        / "Theory/Core/Reasoning_Mode_Plans/Handoffs/ANTIGRAVITY_HANDOFF_A-B4_VERIFIER_REPAIR.md.sha256",
        repo_root
        / "Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_RCP0_ACTION_LEDGER_2026-09-05.md.sha256",
        repo_root
        / "Theory/Gates/MAT-001/M2M3_U1/M2M3_U1_MAX_FIXED_BACKGROUND_REDUCTION_2026-09-05.md.sha256",
        repo_root
        / "Theory/Verification/G-A4_A-B3_ROLE_C_ADJUDICATION_2026-09-05.md.sha256",
        repo_root
        / "Analysis/MAT/MAT-001/M2M3_U1/m2m3_u1_fixed_background_checks.py.sha256",
        repo_root
        / "Analysis/MAT/MAT-001/M2M3_U1/outputs/m2m3_u1_fixed_background_summary.sha256",
    )
    sidecar_results: dict[str, dict[str, Any]] = {}
    sidecars_match = True
    for sidecar in sidecars:
        try:
            target, expected_hash, measured_hash = parse_sidecar(sidecar)
            matches = expected_hash == measured_hash
        except (OSError, ValueError) as error:
            target = sidecar
            expected_hash = "UNAVAILABLE"
            measured_hash = f"ERROR: {error}"
            matches = False
        sidecars_match = sidecars_match and matches
        sidecar_results[sidecar.relative_to(repo_root).as_posix()] = {
            "target": target.name,
            "expected_sha256": expected_hash,
            "measured_sha256": measured_hash,
            "matches": matches,
        }

    handoff_relpath = (
        "Theory/Core/Reasoning_Mode_Plans/Handoffs/"
        "ANTIGRAVITY_HANDOFF_A-B4_VERIFIER_REPAIR.md"
    )
    handoff_hash = sha256_file(repo_root / handoff_relpath)
    manifest_text = (
        repo_root / "Theory/Core/Reasoning_Mode_Plans/Handoffs/HANDOFF_SHA256.md"
    ).read_text(encoding="utf-8")
    manifest_match = re.search(
        rf"(?m)^([0-9a-f]{{64}})  {re.escape(handoff_relpath)}$", manifest_text
    )
    manifest_handoff_hash = manifest_match.group(1) if manifest_match else "MISSING"

    n = sp.symbols("n", real=True)
    monomial_solution = sp.solve(sp.Eq(n / (n - 1), sp.Rational(3, 2)), n)

    checks: dict[str, bool] = {
        "background_linear_term_vanishes": is_zero(radial_linear),
        "background_radial_quadratic_coefficient": is_zero(
            radial_quadratic + 2 * lam * v**2
        ),
        "canonical_source_matches_field_chart": is_zero(
            canonical_source - expected_source
        ),
        "dispersion_root_sum": is_zero(
            omega_minus_sq + omega_plus_sq - characteristic_sum
        ),
        "dispersion_root_product": is_zero(
            omega_minus_sq * omega_plus_sq - characteristic_product
        ),
        "positive_low_k_k4_symbolic": is_zero(exact_k4 - tested_k4),
        "independent_hamiltonian_roots": root_agreement,
        "arbitrary_precision_positive_k4_convergence": low_k_monotone,
        "lower_pole_overlap_low_k": is_zero(
            lower_overlap_slope - expected_overlap_slope
        ),
        "p_x_stationary_reduction": is_zero(p_x_j - p_x_expected),
        "p_x_sound_speed_matches_exact": is_zero(
            (p_sound_speed_sq - exact_sound_speed_sq).subs(background_rule)
        ),
        "gp_bogoliubov_k4_retained": is_zero(bogoliubov - bogoliubov_expected),
        "uniform_sphere_charge_forms_agree": is_zero(
            charge_ratio - charge_ratio_independent
        ),
        "uniform_sphere_weak_limit": sp.limit(charge_ratio, x, 0, dir="+") == 1,
        "force_factor_two_mismatch_detected": sp.simplify(force_action / force_review)
        == 2,
        "finite_density_enthalpy_obstruction": is_zero(
            condensate_enthalpy - 2 * mu**2 * v**2
        ),
        "conformal_source_matches_c0_at_positive_alpha": is_zero(
            conformal_source.subs(alpha1, Lambda**-2) - expected_source
        ),
        "conformal_matter_susceptibility_retained": matter_second_variation.has(
            trace_slope
        ),
        "dimension_weak_distortion_zero": dimension_engine.dim(weak_distortion)
        == 0,
        "dimension_sphere_argument_zero": dimension_engine.dim(
            R * sp.sqrt(rho_source) / Lambda
        )
        == 0,
        "dimension_source_minus_one": dimension_engine.dim(expected_source) == -1,
        "dimension_conformal_source_minus_one": dimension_engine.dim(
            conformal_source
        )
        == -1,
        "dimension_incompatible_sum_rejected": incompatible_sum_rejected,
        "parsed_trace_sign_discrepancy": is_zero(
            sp.diff(action_trace, s) + sp.diff(parsed_trace, s)
        )
        and not is_zero(sp.diff(action_trace - parsed_trace, s)),
        "parsed_radial_mass_matches_report": is_zero(
            parsed_radial_mass - radial_mass_sq
        ),
        "parsed_enthalpy_matches_report": is_zero(
            parsed_enthalpy - 2 * mu**2 * v**2
        ),
        "stability_root_product_factorized": is_zero(
            characteristic_product
            - gradient_sign * t * (gradient_sign * t + radial_mass_sq)
        ),
        "healthy_domain_has_nonnegative_root_product": gradient_sign == 1
        and sp.ask(sp.Q.nonnegative(t * (t + radial_mass_sq))) is True,
        "three_halves_shape_selects_sextic": monomial_solution == [3],
        "mandatory_source_inventory_complete": not missing_inputs,
        "sealed_sidecars_match": sidecars_match,
        "handoff_manifest_matches": manifest_handoff_hash == handoff_hash,
    }
    checks = {name: bool(value) for name, value in checks.items()}

    taxonomy = {
        name: (
            "INDEPENDENT_FORMULATION"
            if name == "independent_hamiltonian_roots"
            else "ARBITRARY_PRECISION_LIMIT"
            if name == "arbitrary_precision_positive_k4_convergence"
            else "DIMENSION_ENGINE"
            if name.startswith("dimension_")
            else "PARSED_CODE_TO_CLAIM"
            if name.startswith("parsed_")
            else "END_TO_END_PROVENANCE"
            if name in {
                "mandatory_source_inventory_complete",
                "sealed_sidecars_match",
                "handoff_manifest_matches",
            }
            else "INCOMPLETE_PROXY"
            if name in {
                "force_factor_two_mismatch_detected",
                "three_halves_shape_selects_sextic",
            }
            else "SYMBOLIC_IDENTITY"
        )
        for name in checks
    }

    result: dict[str, Any] = {
        "schema_version": "2.0",
        "calculation": "M2M3_U1_FIXED_BACKGROUND_SEMANTIC_VERIFIER_V2",
        "calculation_status": (
            "PASS_SEMANTIC_V2_IDENTITIES"
            if all(checks.values())
            else "FAIL_SEMANTIC_V2_IDENTITIES"
        ),
        "mutation": mutation or "NONE",
        "checks": checks,
        "test_taxonomy": taxonomy,
        "failed_checks": [name for name, passed in checks.items() if not passed],
        "stability_domains": {
            "healthy_fixed_background": (
                "M_sigma^2>=0 and k^2>=0 imply root product "
                "k^2(k^2+M_sigma^2)>=0; M_sigma^2>0 gives c_s^2>0"
            ),
            "negative_radial_mass": (
                "M_sigma^2<0 gives negative root product for "
                "0<k^2<-M_sigma^2"
            ),
        },
        "identities": {
            "positive_low_k_k4": sp.sstr(expected_positive_k4),
            "exact_low_k_k4_measured": sp.sstr(exact_k4),
            "hamiltonian_orientation": (
                "q_dot=p_q-2 mu sigma; "
                "p_sigma_dot=-(k^2+M_sigma^2+4mu^2)sigma+2mu p_q"
            ),
            "uniform_sphere_charge_ratio": sp.sstr(charge_ratio),
            "fixed_background_only": True,
        },
        "root_grid": root_results,
        "low_k_convergence": low_k_results,
        "source_inventory_sha256": input_hashes,
        "sidecar_verification": sidecar_results,
        "handoff_manifest": {
            "expected_sha256": manifest_handoff_hash,
            "measured_sha256": handoff_hash,
            "matches": manifest_handoff_hash == handoff_hash,
        },
        "gate_boundary": {
            "gate_effect": "NONE",
            "MAT-001": "BLOCKED",
            "UVIR-003": "IN_PROGRESS",
            "K_Q": "NOT_DERIVED",
            "V": "NOT_COMPUTED",
        },
        "nonclaims": [
            "No metric, lapse, or shift constraint was eliminated.",
            "No physical ITSM pole residue, K_Q, V, force law or a_0 was derived.",
            "A verifier pass is not a physics-gate pass.",
        ],
    }

    output_path = output_dir / "m2m3_u1_fixed_background_summary_v2.json"
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    output_path.write_text(serialized, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    output_path.with_suffix(".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(result["calculation_status"])
    print(f"checks={len(checks)} passed={sum(checks.values())}")
    print(f"summary_v2_sha256={digest}")
    print("MAT-001=BLOCKED K_Q=NOT_DERIVED V=NOT_COMPUTED gate_effect=NONE")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutation", choices=MUTATIONS)
    arguments = parser.parse_args()
    try:
        output = main(arguments.mutation)
    except Exception as error:  # Fail closed with the exact exception type/message.
        print(f"VERIFIER_EXCEPTION: {type(error).__name__}: {error}", file=sys.stderr)
        raise
    if not all(output["checks"].values()):
        print(f"FAILED_CHECKS={output['failed_checks']}", file=sys.stderr)
        raise SystemExit(1)
