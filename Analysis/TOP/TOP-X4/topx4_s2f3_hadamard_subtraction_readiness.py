#!/usr/bin/env python3
"""Plan-11 five-dimensional Hadamard/subtraction readiness checkpoint.

This executable validates a universal local subtraction scaffold and audits
the currently frozen X4-S2F3 operator/state inventory. It deliberately does
not compute a renormalized stress tensor, a semiclassical background, or a
physical Hessian.
"""

from __future__ import annotations

import copy
import hashlib
import inspect
import json
from pathlib import Path
from typing import Any

import sympy as sp


STATUS = (
    "PASS_5D_HADAMARD_COUNTERTERM_SCAFFOLD_"
    "HOLD_FULL_OPERATORS_STATE_AND_STRESS"
)
FAIL_STATUS = "FAIL_HADAMARD_SUBTRACTION_READINESS_CHECKPOINT"
FORBIDDEN_SOURCE_TOKENS = (
    "observed" + "_acceleration",
    "hubble" + "_target",
    "galaxy" + "_target",
    "desired" + "_radius",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sidecar_check(path: Path, root: Path) -> dict[str, Any]:
    sidecar = Path(str(path) + ".sha256")
    actual = sha256_file(path) if path.is_file() else "MISSING"
    expected = "MISSING"
    if sidecar.is_file():
        tokens = sidecar.read_text(encoding="ascii").split()
        expected = tokens[0].lower() if tokens else "MALFORMED"
    return {
        "path": str(path.relative_to(root)),
        "actual": actual,
        "expected": expected,
        "matches": actual == expected,
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def validate_scaffold(candidate: dict[str, Any]) -> bool:
    required_gravity_terms = {
        "1",
        "R",
        "R^2",
        "R_AB R^AB",
        "R_ABCD R^ABCD",
    }
    return all(
        (
            candidate["dimension"] == 5,
            candidate["bulk_logarithm"] is False,
            set(candidate["gravity_terms"]) == required_gravity_terms,
            candidate["q0_subtraction_scope"] == "STATIC_TOPOLOGY_ONLY",
            candidate["finite_order_state_is_hadamard"] is False,
            candidate["graviton_ghost_jacobian_required"] is True,
            candidate["matrix_E_and_Omega_required"] is True,
        )
    )


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    base = root / "Analysis" / "TOP" / "TOP-X4"
    output_dir = base / "outputs"
    gate_dir = root / "Theory" / "Gates" / "TOP-X4"
    plan_path = (
        root
        / "Theory"
        / "Core"
        / "Reasoning_Mode_Plans"
        / "11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION"
        / "PLAN.md"
    )
    contract_path = (
        gate_dir
        / "TOPX4_S2F3_HADAMARD_SUBTRACTION_READINESS_CONTRACT_2026-09-12.md"
    )
    finite_operator_path = output_dir / "topx4_s2f3_finite_charge_operator_summary.json"
    dynamic_path = output_dir / "topx4_s2f3_dynamic_state_subtraction_summary.json"
    exact_path = output_dir / "topx4_s2f3_exact_transport_retry_summary.json"
    static_path = output_dir / "topx4_s2f3_static_determinant_summary.json"
    action_path = gate_dir / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md"
    parent_path = gate_dir / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md"
    variation_path = gate_dir / "TOPX4_S2F3_FINITE_CHARGE_VARIATION_CONTRACT_2026-09-09.md"

    authority_paths = [
        contract_path,
        parent_path,
        action_path,
        variation_path,
        plan_path,
        finite_operator_path,
        dynamic_path,
        exact_path,
        static_path,
    ]
    receipts = [sidecar_check(path, root) for path in authority_paths]
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "all_authority_and_input_sidecars_match",
        all(item["matches"] for item in receipts),
        receipts=receipts,
    )

    finite_operator = load_json(finite_operator_path)
    dynamic = load_json(dynamic_path)
    exact = load_json(exact_path)
    static = load_json(static_path)

    prior_dynamic_preserved = all(
        (
            dynamic.get("status") == "FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT",
            dynamic.get("calculation_checks_passed") == 11,
            dynamic.get("calculation_checks_total") == 12,
            dynamic.get("state_declaration", {}).get("full_Hadamard_claim") is False,
            dynamic.get("subtraction_declaration", {}).get("stress_integral_or_KK_sum_performed")
            is False,
        )
    )
    add_check(
        checks,
        "failed_dynamic_state_result_is_preserved_as_negative_evidence",
        prior_dynamic_preserved,
        status=dynamic.get("status"),
        checks_passed=dynamic.get("calculation_checks_passed"),
        checks_total=dynamic.get("calculation_checks_total"),
    )

    exact_scope_locked = all(
        (
            exact.get("status")
            == "PASS_EXACT_SCALAR_DIRAC_TRANSPORT_HOLD_HADAMARD_STRESS_AND_HESSIAN",
            exact.get("state_scope", {}).get("finite_order_only") is True,
            exact.get("full_Hadamard_state") is False,
            exact.get("covariant_5D_subtraction") == "NOT_DERIVED",
            exact.get("renormalized_stress") == "NOT_COMPUTED",
        )
    )
    add_check(
        checks,
        "exact_transport_scope_remains_finite_order_and_non_hadamard",
        exact_scope_locked,
        state_scope=exact.get("state_scope"),
        full_Hadamard_state=exact.get("full_Hadamard_state"),
        covariant_5D_subtraction=exact.get("covariant_5D_subtraction"),
        renormalized_stress=exact.get("renormalized_stress"),
    )

    dimension = sp.Integer(5)
    singular_exponent = sp.Rational(dimension, 2) - 1
    alpha_5 = sp.gamma(sp.Rational(dimension, 2) - 1) / (
        (2 * sp.pi) ** sp.Rational(dimension, 2)
    )
    singular_prefactor = sp.simplify(alpha_5 / 2)
    target_prefactor = 1 / (16 * sp.sqrt(2) * sp.pi**2)
    add_check(
        checks,
        "five_dimensional_hadamard_exponent_and_prefactor",
        singular_exponent == sp.Rational(3, 2)
        and sp.simplify(singular_prefactor - target_prefactor) == 0,
        exponent=str(singular_exponent),
        alpha_5=str(sp.simplify(alpha_5)),
        propagator_prefactor=str(singular_prefactor),
        required_U_depth=["U0", "U1", "U2"],
    )

    m, xi, curvature = sp.symbols("m xi R", real=True)
    box_curvature, ricci2, riemann2 = sp.symbols(
        "BoxR Ricci2 Riemann2", real=True
    )
    q = xi - sp.Rational(1, 6)
    u0 = sp.Integer(1)
    u1 = -m**2 - q * curvature
    u2 = (
        -sp.Rational(1, 2) * m**4
        - q * m**2 * curvature
        + sp.Rational(1, 6) * (xi - sp.Rational(1, 5)) * box_curvature
        - sp.Rational(1, 2) * q**2 * curvature**2
        + sp.Rational(1, 180) * ricci2
        - sp.Rational(1, 180) * riemann2
    )
    hadamard_coefficients_ok = all(
        (
            u0 == 1,
            sp.expand(u1).coeff(m, 2) == -1,
            sp.expand(u1).coeff(curvature, 1) == -q,
            sp.expand(u2).coeff(m, 4) == -sp.Rational(1, 2),
            sp.expand(u2).coeff(ricci2, 1) == sp.Rational(1, 180),
            sp.expand(u2).coeff(riemann2, 1) == -sp.Rational(1, 180),
            sp.expand(u2).coeff(box_curvature, 1)
            == sp.Rational(1, 6) * (xi - sp.Rational(1, 5)),
        )
    )
    add_check(
        checks,
        "scalar_U0_U1_U2_coincidence_controls",
        hadamard_coefficients_ok,
        u0=str(u0),
        u1=str(u1),
        u2=str(sp.expand(u2)),
        limitation="single scalar control; not a coupled matrix parametrix",
    )

    logarithmic_bulk_index = sp.Rational(dimension, 2)
    no_bulk_log = logarithmic_bulk_index.is_integer is False
    add_check(
        checks,
        "smooth_boundaryless_D5_has_no_bulk_logarithmic_heat_kernel_term",
        no_bulk_log,
        would_require_integer_dewitt_index=str(logarithmic_bulk_index),
        bulk_logarithm=False,
        finite_renormalization_ambiguity_still_present=True,
    )

    E, omega2 = sp.symbols("E Omega2", commutative=True)
    box_E = sp.symbols("BoxE", commutative=True)
    b0 = sp.Integer(1)
    b1 = E + curvature / 6
    b2_from_a4 = sp.expand(
        (
            60 * box_E
            + 60 * curvature * E
            + 180 * E**2
            + 12 * box_curvature
            + 5 * curvature**2
            - 2 * ricci2
            + 2 * riemann2
            + 30 * omega2
        )
        / 360
    )
    b2_target = (
        E**2 / 2
        + curvature * E / 6
        + omega2 / 12
        + curvature**2 / 72
        - ricci2 / 180
        + riemann2 / 180
        + box_E / 6
        + box_curvature / 30
    )
    add_check(
        checks,
        "general_laplace_type_b0_b1_b2_map",
        b0 == 1 and sp.simplify(b2_from_a4 - b2_target) == 0,
        convention="P=-(D^2+E)",
        indexing="DeWitt b0,b1,b2 correspond to heat-kernel a0,a2,a4",
        b0=str(b0),
        b1=str(b1),
        b2=str(b2_target),
    )

    scalar_integrated_b1 = sp.simplify(b1.subs(E, -xi * curvature))
    scalar_integrated_b2 = sp.simplify(
        b2_target.subs(
            {
                E: -xi * curvature,
                omega2: 0,
                box_E: -xi * box_curvature,
                box_curvature: 0,
            }
        )
    )
    scalar_b2_expected = (
        sp.Rational(1, 2) * q**2 * curvature**2
        - sp.Rational(1, 180) * ricci2
        + sp.Rational(1, 180) * riemann2
    )
    add_check(
        checks,
        "minimal_scalar_specialization_matches_integrated_dewitt_controls",
        sp.simplify(scalar_integrated_b1 + q * curvature) == 0
        and sp.simplify(scalar_integrated_b2 - scalar_b2_expected) == 0,
        mass_treatment="mass factored as exp(-m^2 s)",
        integrated_b1=str(scalar_integrated_b1),
        integrated_b2=str(scalar_integrated_b2),
        total_derivatives="dropped only for this integrated boundaryless control",
    )

    cutoff_terms: list[dict[str, Any]] = []
    cutoff_ok = True
    for k, expected_coefficient, expected_power in (
        (0, sp.Rational(2, 5), 5),
        (1, sp.Rational(2, 3), 3),
        (2, sp.Integer(2), 1),
    ):
        coefficient = sp.simplify(1 / (sp.Rational(dimension, 2) - k))
        power = int(dimension - 2 * k)
        cutoff_ok = cutoff_ok and coefficient == expected_coefficient and power == expected_power
        cutoff_terms.append(
            {
                "dewitt_coefficient": f"b{k}",
                "cutoff_coefficient": str(coefficient),
                "cutoff_power": power,
            }
        )
    add_check(
        checks,
        "proper_time_cutoff_powers_are_Lambda5_Lambda3_Lambda1",
        cutoff_ok,
        terms=cutoff_terms,
        common_factor="(4*pi)^(-5/2) times determinant/statistics prefactor",
    )

    dimension_ledger = [
        {
            "term": f"Lambda^{5 - 2 * k} b{k}",
            "cutoff_dimension": 5 - 2 * k,
            "coefficient_dimension": 2 * k,
            "lagrangian_dimension": 5,
        }
        for k in range(3)
    ]
    add_check(
        checks,
        "all_D5_local_divergence_terms_have_lagrangian_dimension_five",
        all(
            row["cutoff_dimension"] + row["coefficient_dimension"] == 5
            for row in dimension_ledger
        ),
        ledger=dimension_ledger,
    )

    gravity_counterterms = [
        {"operator": "1", "operator_dimension": 0, "coefficient_dimension": 5},
        {"operator": "R", "operator_dimension": 2, "coefficient_dimension": 3},
        {"operator": "R^2", "operator_dimension": 4, "coefficient_dimension": 1},
        {
            "operator": "R_AB R^AB",
            "operator_dimension": 4,
            "coefficient_dimension": 1,
        },
        {
            "operator": "R_ABCD R^ABCD",
            "operator_dimension": 4,
            "coefficient_dimension": 1,
        },
    ]
    add_check(
        checks,
        "five_independent_pure_gravity_counterterms_are_retained",
        len(gravity_counterterms) == 5
        and all(
            item["operator_dimension"] + item["coefficient_dimension"] == 5
            for item in gravity_counterterms
        )
        and gravity_counterterms[-1]["operator"] == "R_ABCD R^ABCD",
        counterterms=gravity_counterterms,
        D5_euler_boundary="Riemann-squared may not be removed using the D4 Euler identity",
    )

    action_text = action_path.read_text(encoding="utf-8")
    matter_inputs_present = all(
        token in action_text
        for token in ("lambda_{\\Phi5}", "lambda_{\\chi5}", "g_5", "m_\\Phi^2", "m_\\chi^2")
    )
    matter_map = {
        "required_local_inputs": [
            "tr(E)",
            "tr(E^2)",
            "tr(Omega_AB Omega^AB)",
            "Box E before local variation",
        ],
        "frozen_action_parameters": [
            "m_Phi^2",
            "m_chi^2",
            "lambda_Phi5",
            "lambda_chi5",
            "g_5",
        ],
        "status": "NOT_DERIVED_WITHOUT_COVARIANT_MATRIX_SECOND_VARIATION",
    }
    add_check(
        checks,
        "interacting_scalar_sector_requires_a_separate_matter_counterterm_map",
        matter_inputs_present and matter_map["status"].startswith("NOT_DERIVED"),
        map=matter_map,
    )

    parent_text = parent_path.read_text(encoding="utf-8")
    topology_ok = all(
        phrase in parent_text
        for phrase in (
            "unorbifolded smooth-circle control",
            "no fixed-point counterterms",
            "decompactified",
        )
    )
    add_check(
        checks,
        "smooth_circle_has_no_internal_boundary_or_fixed_point_terms",
        topology_ok,
        circle="periodic smooth S1",
        internal_boundary=False,
        half_integer_boundary_coefficients=False,
        noncompact_falloff_assumption="must still be declared",
    )

    static_definition = static.get("quantum_definition", {})
    dynamic_subtraction = dynamic.get("subtraction_declaration", {})
    q0_scope_ok = all(
        (
            static_definition.get("background")
            == "static Minkowski4 x S1 zero-density control",
            static_definition.get("subtraction")
            == "decompactified Poisson image q=0 removed",
            dynamic_subtraction.get("covariant_5D_stress_subtraction") == "NOT_DERIVED",
            dynamic_subtraction.get("counterterm_map") == "NOT_DERIVED",
            dynamic_subtraction.get("stress_integral_or_KK_sum_performed") is False,
        )
    )
    add_check(
        checks,
        "static_q0_subtraction_is_not_promoted_to_dynamic_stress_renormalization",
        q0_scope_ok,
        static_subtraction=static_definition.get("subtraction"),
        static_background=static_definition.get("background"),
        covariant_dynamic_subtraction=dynamic_subtraction.get(
            "covariant_5D_stress_subtraction"
        ),
    )

    dirac_local_map = {
        "parity_even_magnitude": "from squared Dirac-type Laplace operator",
        "free_spin_connection_endomorphism": "E=-R/4 I with mass factored separately",
        "bundle_curvature": "Omega_AB contains spin curvature",
        "spinor_dimension_in_D5": 4,
        "parity_odd_phase": "NOT_CAPTURED_BY_SQUARING",
        "D5_Hadamard_construction": (
            "NOT_SUPPLIED_BY_CURRENT_EVIDENCE_OR_CITED_4D_EVEN_DIMENSION_CONTROLS"
        ),
    }
    static_holds = " ".join(static.get("hold_reasons", [])).lower()
    add_check(
        checks,
        "dirac_square_scaffolds_only_the_parity_even_magnitude",
        "parity-odd" in static_holds
        and dirac_local_map["parity_odd_phase"] == "NOT_CAPTURED_BY_SQUARING",
        map=dirac_local_map,
    )

    static_gravity_check = next(
        (
            item
            for item in static.get("checks", [])
            if item.get("name") == "functional_determinant_sign_and_degree_count"
        ),
        {},
    )
    finite_scope = finite_operator.get("finite_charge_spectrum", {}).get("scope")
    state_scope = exact.get("state_scope", {})
    inventory = {
        "covariant_scalar_chi_matrix_second_variation": {
            "status": "NOT_COMPLETED",
            "evidence": finite_scope,
        },
        "scalar_matrix_hadamard_state": {
            "status": "NOT_COMPLETED",
            "evidence": state_scope.get("charged_scalar"),
        },
        "dirac_hadamard_two_point_function": {
            "status": "NOT_COMPLETED",
            "evidence": state_scope.get("Dirac"),
        },
        "curved_finite_charge_graviton_and_ghost_operators": {
            "status": "NOT_COMPLETED",
            "evidence": static_gravity_check.get("limitation"),
        },
        "parity_odd_phase_and_quantized_counterterms": {
            "status": "NOT_COMPLETED",
            "evidence": next(
                (
                    reason
                    for reason in exact.get("hold_reasons", [])
                    if "parity-odd" in reason
                ),
                "MISSING_EXPLICIT_HOLD",
            ),
        },
        "gravitational_and_matter_counterterm_normalizations": {
            "status": "NOT_COMPLETED",
            "evidence": exact.get("covariant_5D_subtraction"),
        },
    }
    inventory_ok = all(item["status"] == "NOT_COMPLETED" for item in inventory.values())
    inventory_ok = inventory_ok and all(
        (
            finite_scope == "constant-background principal operator before gravity constraints",
            state_scope.get("finite_order_only") is True,
            state_scope.get("Hadamard_claim") is False,
            static_gravity_check.get("five_dimensional_graviton_degrees") == 5,
            static_gravity_check.get("limitation")
            == "flat zero-density gauge-fixed degree count only; not the finite-charge curved determinant",
        )
    )
    add_check(
        checks,
        "field_by_field_completion_inventory_is_fail_closed",
        inventory_ok,
        inventory=inventory,
    )

    hadamard_stress_ready = all(
        item["status"] == "COMPLETED" for item in inventory.values()
    )
    add_check(
        checks,
        "readiness_decision_holds_before_any_stress_integral",
        hadamard_stress_ready is False,
        hadamard_stress_ready=hadamard_stress_ready,
        renormalized_stress="NOT_COMPUTED",
        decision="HOLD",
    )

    review_records = [
        finite_operator.get("rule9_review", {}),
        dynamic.get("rule9_review", {}),
        exact.get("rule9_review", {}),
    ]
    rule9_open = all(
        record.get("status") == "THREE_WAY_CLEARANCE_NOT_MET"
        and record.get("completed_independent_reports") == 0
        for record in review_records
    )
    add_check(
        checks,
        "rule9_three_way_clearance_remains_open",
        rule9_open,
        prior_review_records=review_records,
    )

    canonical_scaffold = {
        "dimension": 5,
        "bulk_logarithm": False,
        "gravity_terms": [
            "1",
            "R",
            "R^2",
            "R_AB R^AB",
            "R_ABCD R^ABCD",
        ],
        "q0_subtraction_scope": "STATIC_TOPOLOGY_ONLY",
        "finite_order_state_is_hadamard": False,
        "graviton_ghost_jacobian_required": True,
        "matrix_E_and_Omega_required": True,
    }
    mutations: list[dict[str, Any]] = []
    mutation_specs = [
        ("add_D5_bulk_logarithm", "bulk_logarithm", True),
        (
            "omit_Riemann_squared_counterterm",
            "gravity_terms",
            ["1", "R", "R^2", "R_AB R^AB"],
        ),
        ("promote_q0_to_full_stress_subtraction", "q0_subtraction_scope", "FULL_STRESS"),
        ("promote_finite_order_state_to_hadamard", "finite_order_state_is_hadamard", True),
        ("omit_graviton_ghost_jacobian", "graviton_ghost_jacobian_required", False),
        ("omit_matrix_bundle_terms", "matrix_E_and_Omega_required", False),
    ]
    for name, key, replacement in mutation_specs:
        mutant = copy.deepcopy(canonical_scaffold)
        mutant[key] = replacement
        rejected = not validate_scaffold(mutant)
        mutations.append({"name": name, "rejected": rejected})
    add_check(
        checks,
        "all_registered_scope_mutations_are_rejected",
        validate_scaffold(canonical_scaffold)
        and all(item["rejected"] for item in mutations),
        mutations=mutations,
    )

    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    add_check(
        checks,
        "observational_target_firewall",
        not forbidden_hits,
        forbidden_source_tokens=forbidden_hits,
    )

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_S2F3_HADAMARD_SUBTRACTION_READINESS_v1",
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "checkpoint_completed": "2026-09-12",
        "status": STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "readiness_decision": "HOLD" if all_ok else "FAIL",
        "hadamard_stress_ready": False,
        "full_Hadamard_state": False,
        "renormalized_stress": "NOT_COMPUTED",
        "physics_pass": False,
        "gate_effect": "NONE",
        "advance_to_semiclassical_background": False,
        "advance_to_hessian": False,
        "advance_to_a4": False,
        "advance_to_ultra": False,
        "authority_receipts": receipts,
        "source_sha256": sha256_file(Path(__file__)),
        "checks": checks,
        "calculation_checks_passed": sum(check["ok"] for check in checks),
        "calculation_checks_total": len(checks),
        "universal_D5_scaffold": {
            "laplace_operator_convention": "P=-(D^2+E)",
            "heat_kernel_index_map": "DeWitt b0,b1,b2 = heat-kernel a0,a2,a4",
            "hadamard_singular_power": "3/2",
            "hadamard_prefactor": "i/(16*sqrt(2)*pi^2)",
            "hadamard_U_depth": ["U0", "U1", "U2"],
            "bulk_logarithm": False,
            "proper_time_cutoff_terms": cutoff_terms,
            "pure_gravity_counterterms": gravity_counterterms,
        },
        "matter_counterterm_boundary": matter_map,
        "dirac_parity_even_boundary": dirac_local_map,
        "completion_inventory": inventory,
        "hold_reasons": [
            "the interacting charged-scalar/chi covariant matrix second variation is not completed",
            "no scalar matrix or Dirac Hadamard two-point function is constructed",
            "no gauge-fixed curved finite-charge graviton Hessian and ghost/Jacobian operator set exists",
            "the parity-odd determinant phase, global anomaly and quantized counterterms remain unaudited",
            "the gravitational and matter counterterm normalization conditions are not fixed",
            "no state-dependent renormalized stress or regulator/scale/state-order stability test is computed",
        ],
        "next_required_calculation": (
            "derive the off-shell covariant scalar/chi matrix Laplace-type operator before the "
            "homogeneous ansatz, including its E and Omega data; keep spinor, graviton/ghost, "
            "parity-phase and state construction as separately receipted prerequisites"
        ),
        "rule9_review": {
            "status": "THREE_WAY_CLEARANCE_NOT_MET",
            "completed_independent_reports": 0,
            "scope": "this Hadamard/subtraction readiness checkpoint",
            "effect": "no reviewer-consensus or gate-promotion claim",
        },
        "primary_source_basis": [
            {
                "id": "arXiv:gr-qc/0512118",
                "scope": "D5 scalar Hadamard singularity, ambiguity and gravitational counterterms",
            },
            {
                "id": "arXiv:hep-th/0306138",
                "scope": "general Laplace-type heat-kernel coefficients and spin/gravity operator boundary",
            },
            {
                "id": "arXiv:gr-qc/9906076",
                "scope": (
                    "finite-order versus infinite-order Dirac adiabatic/Hadamard boundary; "
                    "stated for even dimensions, not a D5 completion"
                ),
            },
            {
                "id": "arXiv:math-ph/0109010",
                "scope": "adiabatic states and Hadamard subclass boundary",
            },
            {
                "id": "arXiv:1209.2604",
                "scope": "pseudodifferential construction of scalar Hadamard states",
            },
            {
                "id": "arXiv:2108.11630",
                "scope": (
                    "pseudodifferential construction of Dirac Hadamard states under stated "
                    "even-dimensional hypotheses; not a D5 completion"
                ),
            },
        ],
        "derived_claims": [],
        "explicit_nonclaims": [
            "no full scalar or spinor Hadamard state",
            "no renormalized stress tensor",
            "no finite-charge determinant",
            "no curved graviton determinant",
            "no anomaly clearance",
            "no self-consistent semiclassical background",
            "no physical Hessian or radion mass",
            "no A4, Ultra, architecture, gate or publication change",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "topx4_s2f3_hadamard_subtraction_readiness_summary.json"
    payload = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output_path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    output_path.with_suffix(output_path.suffix + ".sha256").write_text(
        f"{digest}  {output_path.name}\n", encoding="ascii", newline="\n"
    )

    print(result["status"])
    print(
        f"checks={result['calculation_checks_passed']}/"
        f"{result['calculation_checks_total']}"
    )
    print("readiness_decision=HOLD")
    print("hadamard_stress_ready=false")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
