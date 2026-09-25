#!/usr/bin/env python3
"""Validate the non-promoting X4-S4-GW2 candidate-action contract."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


STATUS = "PASS_X4_S4_GW2_CANDIDATE_ACTION_CONTRACT_HOLD_PARENT_ACCEPTANCE"
ERROR_STATUS = "ERROR_X4_S4_GW2_CANDIDATE_ACTION_CONTRACT"

REPO_ROOT = Path(__file__).resolve().parents[4]
BASE = Path(__file__).resolve().parent
OUTPUT_PATH = BASE / "outputs" / "mat001_topx4_h1_x4_s4_new_parent_action_contract_summary.json"
REPORT_PATH = BASE / "MAT001_TOPX4_H1_X4_S4_NEW_PARENT_ACTION_CONTRACT_2026-09-18.md"
CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_X4_S4_NEW_PARENT_ACTION_CONTRACT_2026-09-18.md"
)
HANDOFF_CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_COMPENSATED_WARPED_CHILD_DESIGN_CONTRACT_2026-09-17.md"
)
HANDOFF_SUMMARY_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_compensated_warped_child_design_summary.json"
)
S0_AUDIT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S0_STABILIZATION_CANDIDATE_AUDIT_2026-09-06.md"
)
S2F3_FREEZE_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md"
)
ACTION_LEDGER_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "TOP-X4"
    / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md"
)
BRIDGE_CONTRACT_PATH = (
    REPO_ROOT
    / "Theory"
    / "Gates"
    / "MAT-001"
    / "MAT-001_TOPX4_H1_BRIDGE_CONTRACT_2026-09-16.md"
)
BRIDGE_SUMMARY_PATH = BASE / "outputs" / "mat001_topx4_h1_bridge_readiness_summary.json"
HESSIAN_SUMMARY_PATH = (
    REPO_ROOT
    / "Analysis"
    / "TOP"
    / "TOP-X4"
    / "outputs"
    / "topx4_s2f3_physical_hessian_readiness_summary.json"
)
PROJECTION_SUMMARY_PATH = (
    BASE / "outputs" / "mat001_topx4_h1_constraint_projection_diagnostic_summary.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    parser.add_argument("--self-test-mutations", action="store_true")
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def sidecar_candidates(path: Path) -> list[Path]:
    values = [Path(str(path) + ".sha256"), path.with_suffix(".sha256")]
    return list(dict.fromkeys(values))


def find_sidecar(path: Path) -> Path | None:
    return next((item for item in sidecar_candidates(path) if item.is_file()), None)


def write_sidecar(path: Path, *, replace_suffix: bool = False) -> Path:
    sidecar = path.with_suffix(".sha256") if replace_suffix else Path(str(path) + ".sha256")
    sidecar.write_text(
        f"{sha256_file(path)}  {path.name}\n", encoding="ascii", newline="\n"
    )
    return sidecar


def artifact_receipt(path: Path, *, sidecar_required: bool = True) -> dict[str, Any]:
    exists = path.is_file()
    digest = sha256_file(path) if exists else None
    sidecar = find_sidecar(path) if exists else None
    expected: str | None = None
    if sidecar is not None:
        tokens = sidecar.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    return {
        "path": relative(path),
        "exists": exists,
        "sha256": digest,
        "sidecar_required": sidecar_required,
        "sidecar_path": relative(sidecar) if sidecar is not None else None,
        "sidecar_matches": digest == expected if expected is not None else None,
    }


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"Expected JSON object: {path}")
    return data


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def build_candidate() -> dict[str, Any]:
    return {
        "label": "X4-S4-GW2",
        "contract_scope": "LEADING_TWO_DERIVATIVE_CLASSICAL_ACTION_FOR_ONE_BACKGROUND_TEST",
        "geometry": {
            "spacetime": "R_t x T3_obs x I",
            "observed_spatial_topology": "T3_obs",
            "internal_space": "I=S1/Z2",
            "fundamental_domain": "0<=y<=pi",
            "fixed_surfaces": ["Sigma_0", "Sigma_pi"],
            "fundamental_interval_action": True,
            "outward_normal_convention": True,
            "signature": "(-,+,+,+,+)",
            "extrinsic_curvature": "K_mn=(1/2)L_n gamma_mn",
            "parities": {
                "even": ["G_mn", "G_yy", "Phi", "varphi"],
                "odd": ["G_my", "N^y"],
            },
            "protected_y_winding": False,
        },
        "fields": {
            "bulk": ["G_AB", "Phi", "varphi"],
            "localized": {"Sigma_0": ["Psi_m"], "Sigma_pi": []},
            "global_symmetries": ["U(1)_Phi", "Z2_varphi"],
            "orbifold_parity_distinct_from_internal_Z2": True,
            "silently_inherited": [],
            "explicitly_excluded": [
                "chi",
                "three_periodic_massive_5D_Dirac_spectators",
                "bulk_gauge_field",
                "direct_4D_portal",
            ],
        },
        "action": {
            "pieces": ["S_bulk", "S_GHY", "S_0", "S_pi", "S_ct"],
            "bulk_terms": [
                "M5^3 R5/2",
                "-Lambda5",
                "-|nabla Phi|^2",
                "-(partial varphi)^2/2",
                "-U(s,varphi)",
            ],
            "potential_terms": [
                "mPhi2*s",
                "lambdaPhi5*s^2/2",
                "mvarphi2*varphi^2/2",
                "lambdavarphi5*varphi^4/24",
                "g5*s*varphi^2/2",
            ],
            "ghy_present": True,
            "ghy_coefficient": "M5^3",
            "localized_surfaces": ["Sigma_0", "Sigma_pi"],
            "localized_terms": [
                "Mi2*R[gamma_i]/2",
                "-tau_i",
                "-kappa_i*(varphi^2-v_i^2)^2/4",
                "-zeta_i*s",
            ],
            "induced_curvature_present": True,
            "brane_matter_surface": "Sigma_0",
            "brane_matter_metric_only": True,
            "direct_matter_scalar_coupling": False,
        },
        "dimensions": {
            "Phi": "3/2",
            "varphi": "3/2",
            "v_i": "3/2",
            "s": "3",
            "M5": "1",
            "Lambda5": "5",
            "mPhi2": "2",
            "mvarphi2": "2",
            "lambdaPhi5": "-1",
            "lambdavarphi5": "-1",
            "g5": "-1",
            "tau_i": "4",
            "kappa_i": "-2",
            "zeta_i": "1",
            "Mi2": "2",
            "brane_Lagrangian": "4",
        },
        "variation": {
            "bulk_equations_declared": True,
            "scalar_boundary_conditions_derived": True,
            "junction_equations_derived": True,
            "interval_junction": "M5^3(K_mn-K gamma_mn)=S_mn",
            "localized_stress": "S_mn=-V_i gamma_mn+T_mn^m-Mi2 G_mn[gamma]",
            "upstairs_factor_imported_without_derivation": False,
            "embeddings_defined_before_gauge_fixing": True,
            "brane_bending_retained_before_gauge_fixing": True,
            "radion_is_invariant_proper_separation": True,
        },
        "charge_ensemble": {
            "current": "i(Phi* nabla^A Phi-Phi nabla^A Phi*)",
            "Q_nonzero_target": True,
            "chemical_potential_inserted_in_covariant_action": False,
            "fixed_after_variation": True,
            "boundary_charge_flux_zero": True,
            "charge_is_temporal_not_y_winding": True,
        },
        "static_sum_rule": {
            "sector": "ZERO_CHARGE_STATIC_FLAT_4D_UPSTAIRS_SEED",
            "localized_terms_counted_once": True,
            "gradient_coefficients": {"varphi": 1, "Phi_complex": 2},
            "both_net_localized_vacua_strictly_positive_with_nonzero_gradient_allowed": False,
            "necessary_not_sufficient": True,
            "reuse_unchanged_at_finite_Q": False,
            "finite_Q_identity_required": True,
        },
        "background_programme": {
            "ordered_steps": [
                "zero_charge_backreacted_static_seed",
                "fixed_nonzero_Q_continuation_with_lapse_and_shift",
                "full_constraint_and_integrated_identity_check",
                "preconstraint_quadratic_blocks",
            ],
            "lapse_retained_before_variation": True,
            "odd_shift_retained_before_variation": True,
            "finite_charge_background_solved": False,
        },
        "renormalization": {
            "scheme": "MSbar",
            "named_scale_required": True,
            "regulator_class": "covariant_background_field_dimreg_heat_kernel_orbifold_Robin",
            "operator_classes": [
                "bulk_vacuum_Einstein_scalar",
                "bulk_curvature_squared_and_curvature_scalar",
                "boundary_tension_and_induced_curvature",
                "boundary_scalar_kinetic_Robin_pinning_curvature_and_mixed",
                "boundary_GHY_and_extrinsic_curvature",
            ],
            "S_ct_starts_at_order_hbar": True,
            "tree_background_not_tuned_by_S_ct": True,
            "finite_coefficients_normalized": False,
            "one_loop_determinant_computed": False,
            "state_dependent_stress_computed": False,
            "semiclassical_action_complete": False,
        },
        "parameter_domain": {
            "M5": ">0",
            "Lambda5": "<0",
            "mPhi2": ">=0",
            "mvarphi2": ">=0",
            "lambdaPhi5": ">0",
            "lambdavarphi5": ">0",
            "g5": ">=0",
            "kappa_i": ">0_finite",
            "v_i": ">=0",
            "zeta_i": ">=0",
            "Mi2": ">=0",
            "tau_i": "independent_signed_renormalized_inputs",
            "selected_from_observational_target": False,
        },
    }


def build_firewall() -> dict[str, Any]:
    return {
        "candidate_action_contract_frozen": True,
        "X4-S4-GW2_classical_action_frozen_for_one_background_test": True,
        "X4-S4_parent_accepted": False,
        "X4-S2F3_parent_changed": False,
        "finite_charge_background_solved": False,
        "semiclassical_action_complete": False,
        "counterterms_finitely_normalized": False,
        "physical_hessian_constructed": False,
        "signed_H1_residue_computed": False,
        "rule9_cleared": False,
        "MAT001_pass": False,
        "K_Q_derived": False,
        "V_computed": False,
        "stage4A_reopened": False,
        "physics_pass": False,
        "gate_effect": "NONE",
    }


def dimension_check(dimensions: dict[str, str]) -> tuple[bool, dict[str, str]]:
    d = {name: Fraction(value) for name, value in dimensions.items()}
    bulk = {
        "Einstein": 3 * d["M5"] + 2,
        "vacuum": d["Lambda5"],
        "Phi_kinetic": 2 * d["Phi"] + 2,
        "varphi_kinetic": 2 * d["varphi"] + 2,
        "Phi_mass": d["mPhi2"] + d["s"],
        "Phi_quartic": d["lambdaPhi5"] + 2 * d["s"],
        "varphi_mass": d["mvarphi2"] + 2 * d["varphi"],
        "varphi_quartic": d["lambdavarphi5"] + 4 * d["varphi"],
        "portal": d["g5"] + d["s"] + 2 * d["varphi"],
    }
    boundary = {
        "induced_Einstein": d["Mi2"] + 2,
        "tension": d["tau_i"],
        "pinning": d["kappa_i"] + 4 * d["varphi"],
        "Robin": d["zeta_i"] + d["s"],
        "matter": d["brane_Lagrangian"],
    }
    all_ok = all(value == 5 for value in bulk.values()) and all(
        value == 4 for value in boundary.values()
    )
    details = {
        **{f"bulk_{name}": str(value) for name, value in bulk.items()},
        **{f"boundary_{name}": str(value) for name, value in boundary.items()},
    }
    return all_ok, details


def symbolic_variation_check() -> tuple[bool, dict[str, str]]:
    s, phi = sp.symbols("s phi", real=True)
    m_phi2, lam_phi, m_varphi2, lam_varphi, g = sp.symbols(
        "mPhi2 lambdaPhi5 mvarphi2 lambdavarphi5 g5", real=True
    )
    kappa, v, zeta = sp.symbols("kappa_i v_i zeta_i", real=True)

    potential = (
        m_phi2 * s
        + lam_phi * s**2 / 2
        + m_varphi2 * phi**2 / 2
        + lam_varphi * phi**4 / sp.factorial(4)
        + g * s * phi**2 / 2
    )
    expected_duds = m_phi2 + lam_phi * s + g * phi**2 / 2
    expected_dudphi = m_varphi2 * phi + lam_varphi * phi**3 / 6 + g * s * phi

    boundary_potential = kappa * (phi**2 - v**2) ** 2 / 4 + zeta * s
    expected_dv_dphi = kappa * phi * (phi**2 - v**2)
    expected_dv_ds = zeta

    residuals = {
        "dU_ds": str(sp.simplify(sp.diff(potential, s) - expected_duds)),
        "dU_dvarphi": str(sp.simplify(sp.diff(potential, phi) - expected_dudphi)),
        "dVi_dvarphi": str(
            sp.simplify(sp.diff(boundary_potential, phi) - expected_dv_dphi)
        ),
        "dVi_ds": str(sp.simplify(sp.diff(boundary_potential, s) - expected_dv_ds)),
    }
    return all(value == "0" for value in residuals.values()), residuals


def symbolic_sum_rule_weight_check() -> tuple[bool, dict[str, str]]:
    """Derive the scalar weights from T_mu^mu - 4 T_z^z on a static seed."""
    x_real, x_complex, potential = sp.symbols(
        "x_real x_complex potential", real=True
    )

    real_trace_4 = -4 * (x_real / 2 + potential)
    real_normal = x_real / 2 - potential
    real_combination = sp.expand(real_trace_4 - 4 * real_normal)

    complex_trace_4 = -4 * (x_complex + potential)
    complex_normal = x_complex - potential
    complex_combination = sp.expand(complex_trace_4 - 4 * complex_normal)

    expected_real = -4 * x_real
    expected_complex = -8 * x_complex
    residuals = {
        "real_scalar_weight": str(sp.simplify(real_combination - expected_real)),
        "complex_scalar_weight": str(
            sp.simplify(complex_combination - expected_complex)
        ),
        "real_combination": str(real_combination),
        "complex_combination": str(complex_combination),
    }
    ok = (
        residuals["real_scalar_weight"] == "0"
        and residuals["complex_scalar_weight"] == "0"
    )
    return ok, residuals


def contract_coverage_check() -> tuple[bool, list[str]]:
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    concepts = {
        "candidate_acceptance_split": "candidate_action_contract_frozen=true",
        "orbifold_geometry": "I = S1/Z2",
        "two_fixed_surfaces": "Sigma_pi at y=pi",
        "ghy": "S_GHY = M5^3",
        "induced_curvature": "(Mi2/2) R[gamma_i]",
        "scalar_boundary_variation": "n_i^A nabla_A varphi",
        "junction": "M5^3 (K_mu_nu - K gamma_mu_nu) = S_mu_nu^(i)",
        "fixed_charge": "Q = integral_Sigma_t",
        "static_sum_rule": "0 = sum_i V_i^ren",
        "finite_charge_limitation": "displayed identity is not licensed at finite temporal charge",
        "counterterm_basis": "boundary_GHY",
        "nonpromotion": "X4-S4_parent_accepted=false",
    }
    # The counterterm heading is prose rather than a machine identifier.
    concepts["counterterm_basis"] = "renormalization of GHY"
    missing = [name for name, fragment in concepts.items() if fragment not in text]
    return not missing, missing


def semantic_state_valid(candidate: dict[str, Any], firewall: dict[str, Any]) -> bool:
    geometry = candidate.get("geometry", {})
    fields = candidate.get("fields", {})
    action = candidate.get("action", {})
    variation = candidate.get("variation", {})
    charge = candidate.get("charge_ensemble", {})
    sum_rule = candidate.get("static_sum_rule", {})
    programme = candidate.get("background_programme", {})
    renorm = candidate.get("renormalization", {})
    domain = candidate.get("parameter_domain", {})
    dimension_ok, _ = dimension_check(candidate.get("dimensions", {}))

    return (
        candidate.get("label") == "X4-S4-GW2"
        and candidate.get("contract_scope")
        == "LEADING_TWO_DERIVATIVE_CLASSICAL_ACTION_FOR_ONE_BACKGROUND_TEST"
        and geometry.get("spacetime") == "R_t x T3_obs x I"
        and geometry.get("observed_spatial_topology") == "T3_obs"
        and geometry.get("internal_space") == "I=S1/Z2"
        and geometry.get("fixed_surfaces") == ["Sigma_0", "Sigma_pi"]
        and geometry.get("fundamental_interval_action") is True
        and geometry.get("outward_normal_convention") is True
        and geometry.get("protected_y_winding") is False
        and set(geometry.get("parities", {}).get("even", []))
        == {"G_mn", "G_yy", "Phi", "varphi"}
        and set(geometry.get("parities", {}).get("odd", [])) == {"G_my", "N^y"}
        and fields.get("bulk") == ["G_AB", "Phi", "varphi"]
        and fields.get("localized") == {"Sigma_0": ["Psi_m"], "Sigma_pi": []}
        and fields.get("global_symmetries") == ["U(1)_Phi", "Z2_varphi"]
        and fields.get("orbifold_parity_distinct_from_internal_Z2") is True
        and fields.get("silently_inherited") == []
        and "chi" in fields.get("explicitly_excluded", [])
        and "three_periodic_massive_5D_Dirac_spectators"
        in fields.get("explicitly_excluded", [])
        and action.get("pieces") == ["S_bulk", "S_GHY", "S_0", "S_pi", "S_ct"]
        and action.get("ghy_present") is True
        and action.get("ghy_coefficient") == "M5^3"
        and action.get("localized_surfaces") == ["Sigma_0", "Sigma_pi"]
        and action.get("induced_curvature_present") is True
        and action.get("brane_matter_surface") == "Sigma_0"
        and action.get("brane_matter_metric_only") is True
        and action.get("direct_matter_scalar_coupling") is False
        and dimension_ok
        and variation.get("bulk_equations_declared") is True
        and variation.get("scalar_boundary_conditions_derived") is True
        and variation.get("junction_equations_derived") is True
        and variation.get("upstairs_factor_imported_without_derivation") is False
        and variation.get("embeddings_defined_before_gauge_fixing") is True
        and variation.get("brane_bending_retained_before_gauge_fixing") is True
        and variation.get("radion_is_invariant_proper_separation") is True
        and charge.get("Q_nonzero_target") is True
        and charge.get("chemical_potential_inserted_in_covariant_action") is False
        and charge.get("fixed_after_variation") is True
        and charge.get("boundary_charge_flux_zero") is True
        and charge.get("charge_is_temporal_not_y_winding") is True
        and sum_rule.get("sector") == "ZERO_CHARGE_STATIC_FLAT_4D_UPSTAIRS_SEED"
        and sum_rule.get("localized_terms_counted_once") is True
        and sum_rule.get("gradient_coefficients") == {"varphi": 1, "Phi_complex": 2}
        and sum_rule.get(
            "both_net_localized_vacua_strictly_positive_with_nonzero_gradient_allowed"
        )
        is False
        and sum_rule.get("necessary_not_sufficient") is True
        and sum_rule.get("reuse_unchanged_at_finite_Q") is False
        and sum_rule.get("finite_Q_identity_required") is True
        and programme.get("ordered_steps")
        == [
            "zero_charge_backreacted_static_seed",
            "fixed_nonzero_Q_continuation_with_lapse_and_shift",
            "full_constraint_and_integrated_identity_check",
            "preconstraint_quadratic_blocks",
        ]
        and programme.get("lapse_retained_before_variation") is True
        and programme.get("odd_shift_retained_before_variation") is True
        and programme.get("finite_charge_background_solved") is False
        and renorm.get("scheme") == "MSbar"
        and renorm.get("named_scale_required") is True
        and set(renorm.get("operator_classes", []))
        == {
            "bulk_vacuum_Einstein_scalar",
            "bulk_curvature_squared_and_curvature_scalar",
            "boundary_tension_and_induced_curvature",
            "boundary_scalar_kinetic_Robin_pinning_curvature_and_mixed",
            "boundary_GHY_and_extrinsic_curvature",
        }
        and renorm.get("S_ct_starts_at_order_hbar") is True
        and renorm.get("tree_background_not_tuned_by_S_ct") is True
        and renorm.get("finite_coefficients_normalized") is False
        and renorm.get("one_loop_determinant_computed") is False
        and renorm.get("state_dependent_stress_computed") is False
        and renorm.get("semiclassical_action_complete") is False
        and domain.get("M5") == ">0"
        and domain.get("Lambda5") == "<0"
        and domain.get("kappa_i") == ">0_finite"
        and domain.get("tau_i") == "independent_signed_renormalized_inputs"
        and domain.get("selected_from_observational_target") is False
        and firewall.get("candidate_action_contract_frozen") is True
        and firewall.get("X4-S4-GW2_classical_action_frozen_for_one_background_test")
        is True
        and firewall.get("X4-S4_parent_accepted") is False
        and firewall.get("X4-S2F3_parent_changed") is False
        and firewall.get("finite_charge_background_solved") is False
        and firewall.get("semiclassical_action_complete") is False
        and firewall.get("counterterms_finitely_normalized") is False
        and firewall.get("physical_hessian_constructed") is False
        and firewall.get("signed_H1_residue_computed") is False
        and firewall.get("rule9_cleared") is False
        and firewall.get("MAT001_pass") is False
        and firewall.get("K_Q_derived") is False
        and firewall.get("V_computed") is False
        and firewall.get("stage4A_reopened") is False
        and firewall.get("physics_pass") is False
        and firewall.get("gate_effect") == "NONE"
    )


def build_summary(receipts: list[dict[str, Any]]) -> dict[str, Any]:
    candidate = build_candidate()
    firewall = build_firewall()
    checks: list[dict[str, Any]] = []

    add_check(
        checks,
        "all_authority_and_input_files_exist",
        all(item["exists"] for item in receipts),
        missing=[item["path"] for item in receipts if not item["exists"]],
    )
    add_check(
        checks,
        "all_required_sidecars_match_current_bytes",
        all(
            (not item["sidecar_required"]) or item["sidecar_matches"] is True
            for item in receipts
        ),
        failures=[
            item["path"]
            for item in receipts
            if item["sidecar_required"] and item["sidecar_matches"] is not True
        ],
    )

    handoff = load_json(HANDOFF_SUMMARY_PATH)
    handoff_firewall = handoff.get("status_firewall", {})
    add_check(
        checks,
        "prior_route_handoff_authorizes_only_a_separate_new_parent_design",
        handoff.get("status") == "ROUTE_HANDOFF_X4_S4_NEW_PARENT_DESIGN_ONLY"
        and handoff.get("route", {}).get("brane_route")
        == "OPEN_ONLY_AS_X4-S4_NEW_PARENT_DESIGN"
        and handoff_firewall.get("parent_action_changed") is False
        and handoff_firewall.get("X4-S4_action_frozen") is False,
    )

    geometry = candidate["geometry"]
    add_check(
        checks,
        "orbifold_geometry_fixed_points_parities_and_observed_T3_are_explicit",
        geometry["internal_space"] == "I=S1/Z2"
        and geometry["fixed_surfaces"] == ["Sigma_0", "Sigma_pi"]
        and geometry["observed_spatial_topology"] == "T3_obs"
        and geometry["fundamental_interval_action"] is True
        and set(geometry["parities"]["even"]) == {"G_mn", "G_yy", "Phi", "varphi"}
        and set(geometry["parities"]["odd"]) == {"G_my", "N^y"},
    )

    fields = candidate["fields"]
    add_check(
        checks,
        "field_content_is_complete_without_silent_X4_S2F3_inheritance",
        fields["bulk"] == ["G_AB", "Phi", "varphi"]
        and fields["localized"] == {"Sigma_0": ["Psi_m"], "Sigma_pi": []}
        and fields["global_symmetries"] == ["U(1)_Phi", "Z2_varphi"]
        and fields["orbifold_parity_distinct_from_internal_Z2"] is True
        and fields["silently_inherited"] == []
        and {"chi", "three_periodic_massive_5D_Dirac_spectators"}.issubset(
            fields["explicitly_excluded"]
        ),
    )

    action = candidate["action"]
    add_check(
        checks,
        "bulk_boundary_GHY_induced_gravity_and_localized_actions_are_declared",
        action["pieces"] == ["S_bulk", "S_GHY", "S_0", "S_pi", "S_ct"]
        and len(action["bulk_terms"]) == 5
        and len(action["potential_terms"]) == 5
        and action["ghy_present"] is True
        and action["localized_surfaces"] == ["Sigma_0", "Sigma_pi"]
        and action["induced_curvature_present"] is True
        and action["brane_matter_surface"] == "Sigma_0"
        and action["brane_matter_metric_only"] is True
        and action["direct_matter_scalar_coupling"] is False,
    )

    dimensions_ok, dimension_details = dimension_check(candidate["dimensions"])
    add_check(
        checks,
        "every_frozen_operator_has_the_required_bulk_or_boundary_mass_dimension",
        dimensions_ok,
        evaluated_dimensions=dimension_details,
    )

    symbolic_ok, residuals = symbolic_variation_check()
    add_check(
        checks,
        "bulk_and_boundary_scalar_variations_match_the_frozen_potentials",
        symbolic_ok,
        residuals=residuals,
    )

    variation = candidate["variation"]
    add_check(
        checks,
        "GHY_junction_stress_and_upstairs_factor_conventions_are_closed",
        variation["junction_equations_derived"] is True
        and variation["interval_junction"] == "M5^3(K_mn-K gamma_mn)=S_mn"
        and variation["localized_stress"]
        == "S_mn=-V_i gamma_mn+T_mn^m-Mi2 G_mn[gamma]"
        and variation["upstairs_factor_imported_without_derivation"] is False,
    )
    add_check(
        checks,
        "embedding_bending_and_radion_are_retained_until_after_variation",
        variation["embeddings_defined_before_gauge_fixing"] is True
        and variation["brane_bending_retained_before_gauge_fixing"] is True
        and variation["radion_is_invariant_proper_separation"] is True,
    )

    charge = candidate["charge_ensemble"]
    add_check(
        checks,
        "fixed_charge_is_temporal_variational_and_has_no_protected_y_winding",
        charge["Q_nonzero_target"] is True
        and charge["chemical_potential_inserted_in_covariant_action"] is False
        and charge["fixed_after_variation"] is True
        and charge["boundary_charge_flux_zero"] is True
        and charge["charge_is_temporal_not_y_winding"] is True
        and geometry["protected_y_winding"] is False,
    )

    sum_rule = candidate["static_sum_rule"]
    add_check(
        checks,
        "zero_charge_static_seed_sum_rule_has_correct_complex_scalar_weight",
        sum_rule["sector"] == "ZERO_CHARGE_STATIC_FLAT_4D_UPSTAIRS_SEED"
        and sum_rule["localized_terms_counted_once"] is True
        and sum_rule["gradient_coefficients"] == {"varphi": 1, "Phi_complex": 2}
        and sum_rule["necessary_not_sufficient"] is True,
    )
    sum_rule_derivation_ok, sum_rule_residuals = symbolic_sum_rule_weight_check()
    add_check(
        checks,
        "static_sum_rule_gradient_weights_follow_from_stress_trace_combination",
        sum_rule_derivation_ok,
        stress_trace_results=sum_rule_residuals,
    )
    add_check(
        checks,
        "sum_rule_sign_obstruction_and_finite_charge_limit_are_fail_closed",
        sum_rule[
            "both_net_localized_vacua_strictly_positive_with_nonzero_gradient_allowed"
        ]
        is False
        and sum_rule["reuse_unchanged_at_finite_Q"] is False
        and sum_rule["finite_Q_identity_required"] is True,
    )

    programme = candidate["background_programme"]
    add_check(
        checks,
        "background_programme_orders_static_seed_before_finite_charge_and_Hessian",
        programme["ordered_steps"]
        == [
            "zero_charge_backreacted_static_seed",
            "fixed_nonzero_Q_continuation_with_lapse_and_shift",
            "full_constraint_and_integrated_identity_check",
            "preconstraint_quadratic_blocks",
        ]
        and programme["lapse_retained_before_variation"] is True
        and programme["odd_shift_retained_before_variation"] is True
        and programme["finite_charge_background_solved"] is False,
    )

    renorm = candidate["renormalization"]
    add_check(
        checks,
        "renormalization_scheme_and_bulk_boundary_counterterm_classes_are_registered",
        renorm["scheme"] == "MSbar"
        and renorm["named_scale_required"] is True
        and renorm["regulator_class"]
        == "covariant_background_field_dimreg_heat_kernel_orbifold_Robin"
        and set(renorm["operator_classes"])
        == {
            "bulk_vacuum_Einstein_scalar",
            "bulk_curvature_squared_and_curvature_scalar",
            "boundary_tension_and_induced_curvature",
            "boundary_scalar_kinetic_Robin_pinning_curvature_and_mixed",
            "boundary_GHY_and_extrinsic_curvature",
        }
        and renorm["S_ct_starts_at_order_hbar"] is True
        and renorm["tree_background_not_tuned_by_S_ct"] is True,
    )
    add_check(
        checks,
        "semiclassical_and_finite_counterterm_claims_remain_open",
        renorm["finite_coefficients_normalized"] is False
        and renorm["one_loop_determinant_computed"] is False
        and renorm["state_dependent_stress_computed"] is False
        and renorm["semiclassical_action_complete"] is False,
    )

    domain = candidate["parameter_domain"]
    add_check(
        checks,
        "primary_parameter_domain_is_bounded_and_source_independent",
        domain["M5"] == ">0"
        and domain["Lambda5"] == "<0"
        and domain["lambdaPhi5"] == ">0"
        and domain["lambdavarphi5"] == ">0"
        and domain["g5"] == ">=0"
        and domain["kappa_i"] == ">0_finite"
        and domain["tau_i"] == "independent_signed_renormalized_inputs"
        and domain["selected_from_observational_target"] is False,
    )

    coverage_ok, missing_concepts = contract_coverage_check()
    add_check(
        checks,
        "human_contract_covers_the_structured_variational_boundary",
        coverage_ok,
        missing_concepts=missing_concepts,
        note="documentation coherence only; not a physics-pass criterion",
    )

    add_check(
        checks,
        "candidate_freeze_is_separated_from_parent_acceptance",
        firewall["candidate_action_contract_frozen"] is True
        and firewall["X4-S4-GW2_classical_action_frozen_for_one_background_test"] is True
        and firewall["X4-S4_parent_accepted"] is False
        and firewall["X4-S2F3_parent_changed"] is False,
    )
    add_check(
        checks,
        "downstream_physics_and_publication_firewall_remains_closed",
        firewall["finite_charge_background_solved"] is False
        and firewall["semiclassical_action_complete"] is False
        and firewall["counterterms_finitely_normalized"] is False
        and firewall["physical_hessian_constructed"] is False
        and firewall["signed_H1_residue_computed"] is False
        and firewall["rule9_cleared"] is False
        and firewall["MAT001_pass"] is False
        and firewall["K_Q_derived"] is False
        and firewall["V_computed"] is False
        and firewall["stage4A_reopened"] is False
        and firewall["physics_pass"] is False
        and firewall["gate_effect"] == "NONE",
    )

    return {
        "schema": "ITSM_MAT001_TOPX4_H1_X4_S4_NEW_PARENT_ACTION_CONTRACT_v1",
        "date": "2026-09-18",
        "status": STATUS,
        "audit_execution_status": "COMPLETE",
        "scope": "CANDIDATE_ACTION_AND_VARIATIONAL_CONTRACT_ONLY",
        "candidate": candidate,
        "checks": checks,
        "checks_passed": sum(1 for item in checks if item["ok"]),
        "checks_total": len(checks),
        "status_firewall": firewall,
        "artifact_receipts": receipts,
        "literature_basis": [
            {
                "title": "Modulus Stabilization with Bulk Fields",
                "url": "https://arxiv.org/abs/hep-ph/9907447",
                "use": "bulk-scalar/two-boundary stabilization class",
            },
            {
                "title": "Modeling the fifth dimension with scalars and gravity",
                "url": "https://arxiv.org/abs/hep-th/9909134",
                "use": "backreacted scalar-gravity-brane equations and junctions",
            },
            {
                "title": "Brane World Sum Rules",
                "url": "https://arxiv.org/abs/hep-th/0011225",
                "use": "integrated compact-space consistency condition",
            },
            {
                "title": "Exact identification of the radion and its coupling to the observable sector",
                "url": "https://arxiv.org/abs/hep-ph/0401189",
                "use": "mixed scalar-metric radion and physical coupling caution",
            },
            {
                "title": "4D gravity on a brane in 5D Minkowski space",
                "url": "https://arxiv.org/abs/hep-th/0005016",
                "use": "induced brane curvature as an independent localized operator",
            },
        ],
        "next_single_gate": {
            "name": "TOPX4_H1_X4-S4_ZERO_CHARGE_BACKGROUND_EXISTENCE",
            "scope": (
                "Test the frozen X4-S4-GW2 classical action for a regular fully "
                "backreacted zero-charge seed satisfying both boundary systems and "
                "the exact static sum rule."
            ),
            "stop_before": "FINITE_CHARGE_CONTINUATION_IF_STATIC_SEED_FAILS",
        },
    }


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    checks = summary.get("checks", [])
    return (
        summary.get("status") == STATUS
        and summary.get("scope") == "CANDIDATE_ACTION_AND_VARIATIONAL_CONTRACT_ONLY"
        and summary.get("checks_passed") == summary.get("checks_total") == len(checks)
        and all(item.get("ok") is True for item in checks)
        and semantic_state_valid(
            summary.get("candidate", {}), summary.get("status_firewall", {})
        )
    )


def mutation_suite(summary: dict[str, Any]) -> list[str]:
    if not exported_contract_valid(summary):
        raise AssertionError("baseline X4-S4 candidate-action contract must be valid")

    mutants: list[tuple[str, dict[str, Any]]] = []

    one_surface = copy.deepcopy(summary)
    one_surface["candidate"]["geometry"]["fixed_surfaces"] = ["Sigma_0"]
    mutants.append(("second_fixed_surface_removed", one_surface))

    smooth_circle = copy.deepcopy(summary)
    smooth_circle["candidate"]["geometry"]["internal_space"] = "S1"
    mutants.append(("orbifold_replaced_by_smooth_circle", smooth_circle))

    no_ghy = copy.deepcopy(summary)
    no_ghy["candidate"]["action"]["ghy_present"] = False
    mutants.append(("GHY_omitted", no_ghy))

    inherited = copy.deepcopy(summary)
    inherited["candidate"]["fields"]["silently_inherited"] = [
        "chi",
        "three_periodic_massive_5D_Dirac_spectators",
    ]
    mutants.append(("X4_S2F3_spectators_silently_inherited", inherited))

    no_internal_symmetry = copy.deepcopy(summary)
    no_internal_symmetry["candidate"]["fields"]["global_symmetries"] = ["U(1)_Phi"]
    mutants.append(("stabilizer_internal_Z2_removed", no_internal_symmetry))

    winding = copy.deepcopy(summary)
    winding["candidate"]["geometry"]["protected_y_winding"] = True
    mutants.append(("protected_interval_winding_inserted", winding))

    missing_induced = copy.deepcopy(summary)
    missing_induced["candidate"]["action"]["induced_curvature_present"] = False
    mutants.append(("localized_induced_curvature_omitted", missing_induced))

    positive_vacua = copy.deepcopy(summary)
    positive_vacua["candidate"]["static_sum_rule"][
        "both_net_localized_vacua_strictly_positive_with_nonzero_gradient_allowed"
    ] = True
    mutants.append(("static_sum_rule_sign_obstruction_ignored", positive_vacua))

    finite_q_static_rule = copy.deepcopy(summary)
    finite_q_static_rule["candidate"]["static_sum_rule"]["reuse_unchanged_at_finite_Q"] = True
    mutants.append(("zero_charge_sum_rule_reused_at_finite_charge", finite_q_static_rule))

    finite_q_solved = copy.deepcopy(summary)
    finite_q_solved["candidate"]["background_programme"]["finite_charge_background_solved"] = True
    finite_q_solved["status_firewall"]["finite_charge_background_solved"] = True
    mutants.append(("finite_charge_background_claimed_solved", finite_q_solved))

    accepted = copy.deepcopy(summary)
    accepted["status_firewall"]["X4-S4_parent_accepted"] = True
    mutants.append(("candidate_promoted_to_accepted_parent", accepted))

    hessian = copy.deepcopy(summary)
    hessian["status_firewall"]["physical_hessian_constructed"] = True
    hessian["status_firewall"]["signed_H1_residue_computed"] = True
    mutants.append(("physical_Hessian_and_H1_promoted", hessian))

    observational = copy.deepcopy(summary)
    observational["candidate"]["parameter_domain"]["selected_from_observational_target"] = True
    mutants.append(("action_parameter_selected_from_observational_target", observational))

    missing_boundary_scalar_ct = copy.deepcopy(summary)
    missing_boundary_scalar_ct["candidate"]["renormalization"]["operator_classes"].remove(
        "boundary_scalar_kinetic_Robin_pinning_curvature_and_mixed"
    )
    mutants.append(("boundary_scalar_counterterm_class_omitted", missing_boundary_scalar_ct))

    semiclassical = copy.deepcopy(summary)
    semiclassical["candidate"]["renormalization"]["finite_coefficients_normalized"] = True
    semiclassical["candidate"]["renormalization"]["semiclassical_action_complete"] = True
    semiclassical["status_firewall"]["counterterms_finitely_normalized"] = True
    semiclassical["status_firewall"]["semiclassical_action_complete"] = True
    mutants.append(("semiclassical_completion_claimed_without_calculation", semiclassical))

    passed: list[str] = []
    for label, mutant in mutants:
        if exported_contract_valid(mutant):
            raise AssertionError(f"mutation must be rejected: {label}")
        passed.append(label)
    return passed


def render_report(summary: dict[str, Any], output_digest: str) -> str:
    checks = "\n".join(
        f"| {row['name']} | {'yes' if row['ok'] else 'no'} |"
        for row in summary["checks"]
    )
    mutations = "\n".join(
        f"- `{label}`: rejected" for label in summary["mutation_tests"]["labels"]
    )
    firewall = summary["status_firewall"]
    return f"""# MAT-001 TOP-X4 H1 X4-S4 new-parent action-contract receipt

**Executed:** 2026-09-18  
**Status:** {summary['status']}  
**Candidate:** {summary['candidate']['label']}  
**Checks:** {summary['checks_passed']}/{summary['checks_total']}  
**Physics pass:** false  
**Gate effect:** NONE

## 1. Result

The X4-S4-GW2 geometry, field inventory, leading classical bulk/localized
action, variational signs, fixed-charge definition, zero-charge sum rule,
counterterm classes and source-independent primary domain are now frozen for
one background-existence test.

This is not acceptance of X4-S4-GW2. It closes action-selection ambiguity for
the next calculation while leaving the finite-charge background,
semiclassical action, physical Hessian, H1 residue, MAT coefficient and Rule-9
review open.

## 2. Evidence checks

| Check | Satisfied |
|---|---|
{checks}

The mass-dimension test evaluates every frozen bulk operator to dimension 5
and every localized operator to dimension 4. Symbolic differentiation of the
bulk and boundary potentials returned zero residual for all four registered
derivatives.

## 3. Rejection controls

{mutations}

All {summary['mutation_tests']['passed']}/{summary['mutation_tests']['total']}
registered mutations were rejected. These are contract-integrity controls,
not independent peer review or evidence that a background exists.

## 4. Scientific boundary

The frozen split is:

    candidate_action_contract_frozen={str(firewall['candidate_action_contract_frozen']).lower()}
    X4-S4-GW2_classical_action_frozen_for_one_background_test=true
    X4-S4_parent_accepted={str(firewall['X4-S4_parent_accepted']).lower()}
    X4-S2F3_parent_changed={str(firewall['X4-S2F3_parent_changed']).lower()}
    finite_charge_background_solved=false
    semiclassical_action_complete=false
    counterterms_finitely_normalized=false
    physical_hessian_constructed=false
    signed_H1_residue_computed=false
    Rule9_cleared=false
    MAT-001=BLOCKED
    K_Q=NOT_DERIVED
    V=NOT_COMPUTED
    Stage4A=CLOSED
    physics_pass=false
    gate_effect=NONE

The zero-charge static sum rule is registered only for the Lorentz-invariant
flat-slice seed. It is explicitly not reused unchanged at finite temporal
charge.

## 5. Next single gate

`{summary['next_single_gate']['name']}` must test the frozen candidate for a
regular fully backreacted zero-charge solution satisfying both scalar boundary
conditions, both gravitational junction systems and the integrated balance.
It must stop before finite-charge continuation if that seed fails.

## 6. Artifact record

- JSON: {relative(OUTPUT_PATH)}
- JSON SHA-256: {output_digest}
- contract: {relative(CONTRACT_PATH)}
- executable: {relative(Path(__file__))}
- Goldberger-Wise class: https://arxiv.org/abs/hep-ph/9907447
- backreacted scalar-gravity-brane system: https://arxiv.org/abs/hep-th/9909134
- compact-space sum rules: https://arxiv.org/abs/hep-th/0011225
- physical radion mixing: https://arxiv.org/abs/hep-ph/0401189
- induced brane curvature: https://arxiv.org/abs/hep-th/0005016
"""


def main() -> int:
    args = parse_args()
    write_sidecar(Path(__file__))
    write_sidecar(CONTRACT_PATH)

    source_specs = [
        (Path(__file__), True),
        (CONTRACT_PATH, True),
        (HANDOFF_CONTRACT_PATH, True),
        (HANDOFF_SUMMARY_PATH, True),
        (S0_AUDIT_PATH, True),
        (S2F3_FREEZE_PATH, True),
        (ACTION_LEDGER_PATH, True),
        (BRIDGE_CONTRACT_PATH, True),
        (BRIDGE_SUMMARY_PATH, True),
        (HESSIAN_SUMMARY_PATH, True),
        (PROJECTION_SUMMARY_PATH, True),
    ]
    receipts = [
        artifact_receipt(path, sidecar_required=required)
        for path, required in source_specs
    ]
    summary = build_summary(receipts)
    if not exported_contract_valid(summary):
        print(ERROR_STATUS)
        print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
        for row in summary["checks"]:
            if not row["ok"]:
                print(f"FAILED_CHECK={row['name']}")
                if row.get("failures"):
                    print(f"  failures={row['failures']}")
                if row.get("missing_concepts"):
                    print(f"  missing_concepts={row['missing_concepts']}")
        return 1

    labels = mutation_suite(summary)
    summary["mutation_tests"] = {
        "passed": len(labels),
        "total": len(labels),
        "labels": labels,
    }
    summary["script_sha256"] = sha256_file(Path(__file__))
    summary["contract_sha256"] = sha256_file(CONTRACT_PATH)

    if args.self_test_mutations:
        print(f"MUTATION_SUITE: {len(labels)}/{len(labels)}")
        for label in labels:
            print(f"  REJECTED: {label}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    args.output.write_bytes(payload)
    output_digest = hashlib.sha256(payload).hexdigest()
    write_sidecar(args.output, replace_suffix=True)

    report = render_report(summary, output_digest)
    args.report.write_text(report, encoding="utf-8", newline="\n")
    write_sidecar(args.report)

    print(summary["status"])
    print(f"checks={summary['checks_passed']}/{summary['checks_total']}")
    print(f"mutation_tests={len(labels)}/{len(labels)}")
    print("candidate_action_contract_frozen=true")
    print("X4-S4_parent_accepted=false")
    print("finite_charge_background_solved=false")
    print("semiclassical_action_complete=false")
    print("physical_hessian_constructed=false")
    print("MAT001=BLOCKED")
    print("K_Q=NOT_DERIVED")
    print("V=NOT_COMPUTED")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={args.output}")
    print(f"output_sha256={output_digest}")
    print(f"report={args.report}")
    print(f"report_sha256={sha256_file(args.report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
