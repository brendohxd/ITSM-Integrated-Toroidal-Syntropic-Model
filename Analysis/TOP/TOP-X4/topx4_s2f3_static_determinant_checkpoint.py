#!/usr/bin/env python3
"""Plan-11 static parity-even determinant checkpoint for TOP-X4 X4-S2F3.

This is a bounded zero-density Minkowski4 x S1 calculation.  It derives and
cross-checks the decompactification-subtracted one-loop Casimir determinant.
It does not evaluate the parity-odd determinant phase, solve the finite-charge
semiclassical background, or calculate a physical radion pole.
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import math
from pathlib import Path
from typing import Any, Callable

import mpmath as mp


STATUS = "PASS_STATIC_PARITY_EVEN_DETERMINANT_HOLD_PARITY_ODD_AND_FINITE_CHARGE"
SCHEMA = "ITSM_TOPX4_S2F3_STATIC_DETERMINANT_v1"
FORBIDDEN_TARGET_TOKENS = (
    "observed" + "_acceleration",
    "hubble" + "_target",
    "galaxy" + "_target",
    "desired" + "_radius",
)
CONTROL_FILES = (
    "active_research.md",
    "Theory/Core/ITSM_TOPX4_KK001_ROUTE_PLAN_2026-09-06.md",
    "Theory/Core/Reasoning_Mode_Plans/11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION/PLAN.md",
    "Theory/Gates/TOP-X4/TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md",
)


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def mp_string(value: mp.mpf, digits: int = 30) -> str:
    return mp.nstr(value, digits)


def shape_polylog(x: mp.mpf) -> mp.mpf:
    """Massive periodic real-scalar shape F(x), with F(0)=zeta(5)."""
    if x == 0:
        return mp.zeta(5)
    z = mp.exp(-x)
    return mp.polylog(5, z) + x * mp.polylog(4, z) + x * x * mp.polylog(3, z) / 3


def shape_prime(x: mp.mpf) -> mp.mpf:
    if x == 0:
        return mp.mpf("0")
    z = mp.exp(-x)
    return -(x * mp.polylog(3, z) + x * x * mp.polylog(2, z)) / 3


def shape_second(x: mp.mpf) -> mp.mpf:
    if x == 0:
        return -mp.zeta(3) / 3
    z = mp.exp(-x)
    return -(
        mp.polylog(3, z)
        + x * mp.polylog(2, z)
        - x * x * mp.polylog(1, z)
    ) / 3


def shape_bessel(x: mp.mpf, images: int = 160) -> mp.mpf:
    """Poisson-image/Bessel representation of the same finite shape."""
    if x == 0:
        return mp.zeta(5)
    prefactor = mp.sqrt(2) * x ** mp.mpf("2.5") / (3 * mp.sqrt(mp.pi))
    return prefactor * mp.fsum(
        mp.besselk(mp.mpf("2.5"), image * x) / image ** mp.mpf("2.5")
        for image in range(1, images + 1)
    )


def shape_proper_time(
    x: mp.mpf,
    images: int,
    log_cutoff: mp.mpf,
) -> mp.mpf:
    """Finite proper-time image sum after explicitly omitting Poisson image 0.

    With circumference set to one, the subtracted scalar potential is
    V_C=-F(x)*3/(4*pi^2).  The dimensionless shape is

      F(x) = 1/(24*sqrt(pi)) sum_{q>=1} int_0^inf
             ds s^(-7/2) exp[-x^2 s-q^2/(4s)].

    The integral is evaluated with s=exp(u) and symmetric log cutoffs.
    """
    total = mp.mpf("0")
    for image in range(1, images + 1):
        q = mp.mpf(image)

        def integrand(u: mp.mpf) -> mp.mpf:
            s = mp.exp(u)
            return mp.exp(-mp.mpf("2.5") * u - x * x * s - q * q / (4 * s))

        total += mp.quad(integrand, [-log_cutoff, mp.mpf("0"), log_cutoff])
    return total / (24 * mp.sqrt(mp.pi))


def massive_combination(x: mp.mpf, fermions: int, ratio_phi: mp.mpf, ratio_chi: mp.mpf) -> mp.mpf:
    return (
        4 * fermions * shape_polylog(x)
        - 2 * shape_polylog(ratio_phi * x)
        - shape_polylog(ratio_chi * x)
    )


def massive_combination_prime(
    x: mp.mpf,
    fermions: int,
    ratio_phi: mp.mpf,
    ratio_chi: mp.mpf,
) -> mp.mpf:
    return (
        4 * fermions * shape_prime(x)
        - 2 * ratio_phi * shape_prime(ratio_phi * x)
        - ratio_chi * shape_prime(ratio_chi * x)
    )


def massive_combination_second(
    x: mp.mpf,
    fermions: int,
    ratio_phi: mp.mpf,
    ratio_chi: mp.mpf,
) -> mp.mpf:
    return (
        4 * fermions * shape_second(x)
        - 2 * ratio_phi * ratio_phi * shape_second(ratio_phi * x)
        - ratio_chi * ratio_chi * shape_second(ratio_chi * x)
    )


def stationarity_equation(
    x: mp.mpf,
    fermions: int,
    ratio_phi: mp.mpf,
    ratio_chi: mp.mpf,
    wrong_fermion_sign: bool = False,
) -> mp.mpf:
    if wrong_fermion_sign:
        q = (
            -4 * fermions * shape_polylog(x)
            - 2 * shape_polylog(ratio_phi * x)
            - shape_polylog(ratio_chi * x)
        )
        q_prime = (
            -4 * fermions * shape_prime(x)
            - 2 * ratio_phi * shape_prime(ratio_phi * x)
            - ratio_chi * shape_prime(ratio_chi * x)
        )
    else:
        q = massive_combination(x, fermions, ratio_phi, ratio_chi)
        q_prime = massive_combination_prime(x, fermions, ratio_phi, ratio_chi)
    gamma = -5 * mp.zeta(5)
    return q - x * q_prime / 5 + gamma


def bisect_root(function: Callable[[mp.mpf], mp.mpf], left: mp.mpf, right: mp.mpf) -> mp.mpf:
    f_left = function(left)
    f_right = function(right)
    if f_left == 0:
        return left
    if f_right == 0:
        return right
    if mp.sign(f_left) == mp.sign(f_right):
        raise ValueError("bisection interval does not bracket a root")
    for _ in range(220):
        middle = (left + right) / 2
        f_middle = function(middle)
        if f_middle == 0 or abs(right - left) < mp.mpf("1e-48") * max(1, abs(middle)):
            return middle
        if mp.sign(f_middle) == mp.sign(f_left):
            left, f_left = middle, f_middle
        else:
            right, f_right = middle, f_middle
    return (left + right) / 2


def scan_roots(
    function: Callable[[mp.mpf], mp.mpf],
    x_min: mp.mpf = mp.mpf("1e-4"),
    x_max: mp.mpf = mp.mpf("60"),
    intervals: int = 1000,
) -> list[mp.mpf]:
    log_min = mp.log10(x_min)
    log_max = mp.log10(x_max)
    grid = [mp.power(10, log_min + (log_max - log_min) * i / intervals) for i in range(intervals + 1)]
    roots: list[mp.mpf] = []
    previous_x = grid[0]
    previous_value = function(previous_x)
    for current_x in grid[1:]:
        current_value = function(current_x)
        if mp.sign(previous_value) != mp.sign(current_value):
            root = bisect_root(function, previous_x, current_x)
            if not roots or abs(root - roots[-1]) > mp.mpf("1e-20") * max(1, abs(root)):
                roots.append(root)
        previous_x, previous_value = current_x, current_value
    return roots


def classify_root(
    x: mp.mpf,
    fermions: int,
    ratio_phi: mp.mpf,
    ratio_chi: mp.mpf,
) -> dict[str, Any]:
    q_prime = massive_combination_prime(x, fermions, ratio_phi, ratio_chi)
    q_second = massive_combination_second(x, fermions, ratio_phi, ratio_chi)
    alpha = -q_prime / (5 * x**4)
    f_second = 20 * alpha * x**3 + q_second
    residual = stationarity_equation(x, fermions, ratio_phi, ratio_chi)
    max_mass_to_cutoff = min(mp.mpf("0.04"), mp.mpf("0.1") * x / (2 * mp.pi))
    accepted_static = alpha > 0 and f_second > 0 and max_mass_to_cutoff > 0
    return {
        "x": mp_string(x),
        "alpha": mp_string(alpha),
        "f_second": mp_string(f_second),
        "stationarity_residual": mp_string(residual, 12),
        "maximum_mF_over_Lambda5_from_registered_bounds": mp_string(max_mass_to_cutoff),
        "static_parity_even_minimum": bool(accepted_static),
    }


def file_hash_record(repository_root: Path, relative_path: str) -> dict[str, Any]:
    path = repository_root / relative_path
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    sidecar_path = path.with_suffix(path.suffix + ".sha256")
    recorded = sidecar_path.read_text(encoding="ascii").strip() if sidecar_path.exists() else ""
    return {
        "path": relative_path.replace("\\", "/"),
        "sha256": digest,
        "sidecar_present": sidecar_path.exists(),
        "sidecar_matches": digest in recorded.lower(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mp.mp.dps = 70
    checks: list[dict[str, Any]] = []
    repository_root = Path(__file__).resolve().parents[3]

    authority_hashes = [file_hash_record(repository_root, item) for item in CONTROL_FILES]
    add_check(
        checks,
        "frozen_authority_sidecars_match",
        all(item["sidecar_present"] and item["sidecar_matches"] for item in authority_hashes),
        files=authority_hashes,
    )

    # Direct proper-time derivation in the static product frame:
    # V_b,J = -(ell/(32*pi^(5/2))) sum_{q>=1} int ds s^(-7/2)
    #          exp[-m^2 s-q^2 ell^2/(4s)]
    #       = -3 F(m ell)/(4*pi^2 ell^4).
    # Under g_J=r^-1 g_E and ell=ell_ref*r, V_E=r^-2 V_J, hence r^-6.
    add_check(
        checks,
        "mass_dimensions_and_einstein_frame_scaling",
        True,
        five_dimensional_field_dimensions={"real_scalar": "3/2", "Dirac": "2", "bulk_vacuum_density": "5"},
        product_frame_potential_dimension=4,
        einstein_frame_potential_dimension=4,
        product_frame_scalar="V_b,J=-3 F(m ell)/(4 pi^2 ell^4)",
        weyl_relation="g_J=r^-1 g_E, sqrt(-g_J)=r^-2 sqrt(-g_E)",
        einstein_frame_scalar="V_b,E=-3 r^-6 F(m ell_ref r)/(4 pi^2 ell_ref^4)",
        bulk_counterterm="V_Lambda,E=Lambda5 ell_ref/r; alpha=4 pi^2 Lambda5/(3 mF^5)",
    )

    representation_samples = []
    for x_text in ("0.1", "0.5", "1", "2.5306790213096324", "8"):
        x = mp.mpf(x_text)
        polylog_value = shape_polylog(x)
        bessel_value = shape_bessel(x)
        relative_error = abs(bessel_value - polylog_value) / abs(polylog_value)
        representation_samples.append(
            {
                "x": x_text,
                "polylog": mp_string(polylog_value),
                "bessel": mp_string(bessel_value),
                "relative_error": mp_string(relative_error, 12),
            }
        )
    bessel_relative_tolerance = mp.mpf("1e-14")
    add_check(
        checks,
        "polylog_and_poisson_bessel_representations_agree",
        all(
            mp.mpf(item["relative_error"]) < bessel_relative_tolerance
            for item in representation_samples
        ),
        samples=representation_samples,
        relative_tolerance=mp_string(bessel_relative_tolerance),
    )

    proper_time_samples = []
    for x_text in ("0.5", "2.5306790213096324"):
        x = mp.mpf(x_text)
        target = shape_polylog(x)
        coarse = shape_proper_time(x, images=18, log_cutoff=mp.mpf("13"))
        fine = shape_proper_time(x, images=28, log_cutoff=mp.mpf("17"))
        proper_time_samples.append(
            {
                "x": x_text,
                "polylog": mp_string(target),
                "proper_time_coarse": mp_string(coarse),
                "proper_time_fine": mp_string(fine),
                "fine_relative_error": mp_string(abs(fine - target) / abs(target), 12),
                "cutoff_change_relative": mp_string(abs(fine - coarse) / abs(fine), 12),
                "poisson_image_zero_included": False,
            }
        )
    proper_time_fine_tolerance = mp.mpf("1e-11")
    proper_time_cutoff_change_tolerance = mp.mpf("5e-9")
    add_check(
        checks,
        "proper_time_cutoff_and_image_sum_converge_after_decompactification_subtraction",
        all(
            mp.mpf(item["fine_relative_error"]) < proper_time_fine_tolerance
            and mp.mpf(item["cutoff_change_relative"])
            < proper_time_cutoff_change_tolerance
            for item in proper_time_samples
        ),
        samples=proper_time_samples,
        subtraction="Poisson image q=0 omitted before integration",
        fine_relative_tolerance=mp_string(proper_time_fine_tolerance),
        cutoff_change_relative_tolerance=mp_string(proper_time_cutoff_change_tolerance),
    )

    small_x = mp.mpf("1e-7")
    small_limit_error = abs(shape_polylog(small_x) - mp.zeta(5)) / mp.zeta(5)
    large_values = [shape_polylog(mp.mpf(value)) for value in ("8", "12", "20")]
    add_check(
        checks,
        "massless_and_large_mass_limits",
        small_limit_error < mp.mpf("1e-13") and large_values[0] > large_values[1] > large_values[2] > 0,
        x_small=mp_string(small_x),
        massless_relative_error=mp_string(small_limit_error, 12),
        large_x_samples={key: mp_string(value) for key, value in zip(("8", "12", "20"), large_values)},
    )

    spinor_dimension = 2 ** ((5 - 1) // 2)
    graviton_degrees = 5 * (5 - 3) // 2
    field_counts = []
    for fermions in (1, 2, 3, 4):
        beta = spinor_dimension * fermions - 3
        field_counts.append(
            {
                "periodic_5D_Dirac_fields": fermions,
                "massive_shape_coefficient": beta,
                "massless_gravity_coefficient_over_zeta5": -graviton_degrees,
                "strict_small_radius_repulsion": beta > graviton_degrees,
            }
        )
    add_check(
        checks,
        "functional_determinant_sign_and_degree_count",
        spinor_dimension == 4
        and graviton_degrees == 5
        and not field_counts[1]["strict_small_radius_repulsion"]
        and field_counts[2]["strict_small_radius_repulsion"],
        real_periodic_scalar_sign="attractive",
        periodic_5D_Dirac_ratio_to_real_scalar=-spinor_dimension,
        five_dimensional_graviton_degrees=graviton_degrees,
        parent_massive_real_bosons=3,
        counts=field_counts,
        limitation="flat zero-density gauge-fixed degree count only; not the finite-charge curved determinant",
    )

    equal_function = lambda x: stationarity_equation(x, 3, mp.mpf("1"), mp.mpf("1"))
    equal_roots = scan_roots(equal_function)
    equal_classified = [classify_root(root, 3, mp.mpf("1"), mp.mpf("1")) for root in equal_roots]
    equal_root = equal_roots[0] if len(equal_roots) == 1 else mp.nan
    equal_cutoff_at_upper_mass = 2 * mp.pi * mp.mpf("0.04") / equal_root if len(equal_roots) == 1 else mp.inf
    add_check(
        checks,
        "equal_mass_zero_vacuum_stationary_minimum_reproduced_without_saved_root",
        len(equal_roots) == 1
        and equal_classified[0]["static_parity_even_minimum"]
        and abs(equal_root - mp.mpf("2.5306790213096324")) < mp.mpf("2e-15")
        and equal_cutoff_at_upper_mass < mp.mpf("0.1"),
        root_scan_domain=["1e-4", "60"],
        root_scan_log_intervals=1000,
        roots=equal_classified,
        delta_KK_over_Lambda5_at_mF_over_Lambda5_0p04=mp_string(equal_cutoff_at_upper_mass),
        root_seed_policy="no saved numerical root supplied; all sign-changing log-grid intervals bisected",
    )

    nf2_function = lambda x: stationarity_equation(x, 2, mp.mpf("1"), mp.mpf("1"))
    nf2_roots = scan_roots(nf2_function)
    nf2_samples = {value: mp_string(nf2_function(mp.mpf(value))) for value in ("1e-4", "0.01", "0.1", "1", "10", "60")}
    add_check(
        checks,
        "nf2_is_marginal_at_x0_and_has_no_positive_zero_cc_stationary_root_in_scan",
        len(nf2_roots) == 0
        and 4 * 2 - 3 == graviton_degrees
        and all(mp.mpf(value) < 0 for value in nf2_samples.values()),
        small_radius_massive_coefficient=5,
        massless_gravity_coefficient=-5,
        root_scan_domain=["1e-4", "60"],
        roots=[mp_string(root) for root in nf2_roots],
        stationarity_samples=nf2_samples,
        scope="numerical scan plus exact coefficient equality; not a proof beyond the registered domain",
    )

    wrong_sign_function = lambda x: stationarity_equation(
        x,
        3,
        mp.mpf("1"),
        mp.mpf("1"),
        wrong_fermion_sign=True,
    )
    wrong_sign_roots = scan_roots(wrong_sign_function)
    add_check(
        checks,
        "deliberate_wrong_fermion_sign_mutation_is_rejected",
        len(wrong_sign_roots) == 0
        and wrong_sign_function(mp.mpf("1e-4")) < 0
        and wrong_sign_function(mp.mpf("60")) < 0,
        roots=[mp_string(root) for root in wrong_sign_roots],
        expected_failure="all massive and massless terms are attractive, so the registered balance disappears",
    )

    mutation_x = equal_root
    full_shape = shape_bessel(mutation_x, images=160)
    omitted_first_image = (
        mp.sqrt(2)
        * mutation_x ** mp.mpf("2.5")
        / (3 * mp.sqrt(mp.pi))
        * mp.fsum(
            mp.besselk(mp.mpf("2.5"), image * mutation_x) / image ** mp.mpf("2.5")
            for image in range(2, 161)
        )
    )
    omitted_relative = abs(omitted_first_image - full_shape) / abs(full_shape)
    add_check(
        checks,
        "deliberate_omitted_poisson_image_mutation_is_detected",
        omitted_relative > mp.mpf("0.5"),
        x=mp_string(mutation_x),
        omitted_image=1,
        relative_difference=mp_string(omitted_relative),
    )

    ratio_grid = tuple(mp.mpf(value) for value in ("0.5", "0.75", "1", "1.25", "1.5", "1.75", "2"))
    ratio_scan: list[dict[str, Any]] = []
    grid_survivors = 0
    grid_no_root = 0
    grid_rejected_roots = 0
    for ratio_phi in ratio_grid:
        for ratio_chi in ratio_grid:
            function = lambda x, rp=ratio_phi, rc=ratio_chi: stationarity_equation(x, 3, rp, rc)
            roots = scan_roots(function, intervals=520)
            classified = [classify_root(root, 3, ratio_phi, ratio_chi) for root in roots]
            accepted = [root for root in classified if root["static_parity_even_minimum"]]
            grid_survivors += len(accepted)
            if not roots:
                grid_no_root += 1
            grid_rejected_roots += len(classified) - len(accepted)
            ratio_scan.append(
                {
                    "mPhi_over_mF": mp_string(ratio_phi, 6),
                    "mChi_over_mF": mp_string(ratio_chi, 6),
                    "roots": classified,
                }
            )
    add_check(
        checks,
        "registered_mass_ratio_grid_reports_all_found_roots",
        len(ratio_scan) == 49 and grid_survivors > 0,
        grid_values=[mp_string(value, 6) for value in ratio_grid],
        grid_points=len(ratio_scan),
        accepted_static_roots=grid_survivors,
        rejected_roots=grid_rejected_roots,
        points_with_no_root=grid_no_root,
        records=ratio_scan,
        limitation="coarse deterministic grid; not continuous-domain robustness and not finite-density evidence",
    )

    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_TARGET_TOKENS if token in source_text]
    add_check(
        checks,
        "observational_target_firewall",
        not forbidden_hits,
        forbidden_token_hits=forbidden_hits,
    )

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": SCHEMA,
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "status": STATUS if all_ok else "ERROR_STATIC_DETERMINANT_CHECKPOINT",
        "audit_execution_status": "COMPLETE" if all_ok else "ERROR",
        "calculation_checks_passed": sum(check["ok"] for check in checks),
        "calculation_checks_total": len(checks),
        "physics_pass": False,
        "gate_effect": "NONE",
        "advance_to_a4": False,
        "advance_to_ultra": False,
        "advance_to_finite_charge": False,
        "quantum_definition": {
            "background": "static Minkowski4 x S1 zero-density control",
            "state": "positive-frequency Minkowski vacuum",
            "method": "proper-time heat kernel plus Poisson resummation",
            "equivalent_representation": "modified-Bessel K_5/2 and polylogarithms",
            "subtraction": "decompactified Poisson image q=0 removed",
            "renormalization": "finite nonlocal Casimir part separated from local renormalized bulk vacuum term",
            "spin_structure": "periodic for all three 5D Dirac spectators",
        },
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checks": checks,
        "checkpoint_decision": "HOLD_BEFORE_FINITE_CHARGE",
        "hold_reasons": [
            "the parity-odd determinant phase and global/nonperturbative spin-structure audit are not completed",
            "the finite-charge background changes the scalar spectrum and has not been varied from a complete one-loop effective action",
            "no Hadamard/adiabatic state or state-order convergence calculation exists for an evolving background",
            "no coupled metric-radion-amplitude-phase constraint reduction or physical radion mass has been calculated",
            "the mass-ratio test is a coarse static grid rather than the required continuous finite-charge robustness domain",
        ],
        "bounded_result": (
            "The static parity-even decompactification-subtracted determinant reproduces the frozen equal-mass "
            "minimum and sign/degree count. This is a determinant checkpoint only, not X4-D2_RETRY or a physics pass."
        ),
        "explicit_nonclaims": [
            "no parity/anomaly clearance",
            "no finite-charge stabilized background",
            "no physical radion mass",
            "no complete five-dimensional EFT domain",
            "no nonperturbative circle-stability proof",
            "no canonical topology change",
            "no K_Q or V derivation",
            "no observational prediction or publication clearance",
        ],
        "primary_source_basis": [
            {
                "citation": "Ponton and Poppitz, JHEP 06 (2001) 019",
                "identifier": "arXiv:hep-ph/0105021",
                "used_for": "independent comparison of periodic massive scalar/Dirac determinant and stabilization conditions",
            },
            {
                "citation": "Witten, Nucl. Phys. B 195 (1982) 481",
                "identifier": "DOI:10.1016/0550-3213(82)90007-4",
                "used_for": "nonperturbative spin-structure question only; not treated as completed here",
            },
        ],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / "topx4_s2f3_static_determinant_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n",
        encoding="ascii",
        newline="\n",
    )

    print(result["status"])
    print(f"calculation_checks={result['calculation_checks_passed']}/{result['calculation_checks_total']}")
    print("checkpoint_decision=HOLD_BEFORE_FINITE_CHARGE")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print("advance_to_a4=false")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
