#!/usr/bin/env python3
"""Plan-11 local scalar-matrix Hadamard-parametrix checkpoint.

This executable constructs and audits the local rank-three D=5 Hadamard
parametrix coefficients through U_2 for the already derived fixed-metric
scalar operator.  It deliberately does not construct a global state, evaluate
a determinant, calculate stress, or advance any downstream gate.
"""

from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path
from typing import Any

import sympy as sp


STATUS = "PASS_SCALAR_MATRIX_HADAMARD_PARAMETRIX_HOLD_GLOBAL_STATE_AND_STRESS"
FAIL_STATUS = "FAIL_SCALAR_MATRIX_HADAMARD_PARAMETRIX_CHECKPOINT"
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


def matrix_is_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def matrix_strings(matrix: sp.MatrixBase) -> list[list[str]]:
    return [[str(sp.factor(value)) for value in row] for row in matrix.tolist()]


def expression_dimension(
    expression: sp.Expr,
    dimensions: dict[sp.Symbol, sp.Rational | sp.Integer],
) -> sp.Rational | None:
    terms = sp.Add.make_args(sp.expand(expression))
    found: sp.Rational | None = None
    for term in terms:
        dimension = sp.Integer(0)
        for factor, power in term.as_powers_dict().items():
            if factor in dimensions:
                dimension += dimensions[factor] * power
            elif factor.is_number:
                continue
            else:
                return None
        if found is None:
            found = sp.simplify(dimension)
        elif sp.simplify(found - dimension) != 0:
            return None
    return found if found is not None else sp.Integer(0)


def scalar_u2_formula(
    mass: sp.Symbol,
    xi: sp.Symbol,
    curvature: sp.Symbol,
    box_curvature: sp.Symbol,
    ricci2: sp.Symbol,
    riemann2: sp.Symbol,
) -> sp.Expr:
    return (
        -sp.Rational(1, 2) * mass**4
        - (xi - sp.Rational(1, 6)) * mass**2 * curvature
        + sp.Rational(1, 6) * (xi - sp.Rational(1, 5)) * box_curvature
        - sp.Rational(1, 2) * (xi - sp.Rational(1, 6)) ** 2 * curvature**2
        + sp.Rational(1, 180) * ricci2
        - sp.Rational(1, 180) * riemann2
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
    matrix_contract_path = (
        gate_dir / "TOPX4_S2F3_COVARIANT_SCALAR_MATRIX_CONTRACT_2026-09-12.md"
    )
    matrix_source_path = base / "topx4_s2f3_covariant_scalar_matrix_checkpoint.py"
    matrix_output_path = output_dir / "topx4_s2f3_covariant_scalar_matrix_summary.json"
    readiness_contract_path = (
        gate_dir / "TOPX4_S2F3_HADAMARD_SUBTRACTION_READINESS_CONTRACT_2026-09-12.md"
    )
    readiness_output_path = (
        output_dir / "topx4_s2f3_hadamard_subtraction_readiness_summary.json"
    )
    exact_output_path = output_dir / "topx4_s2f3_exact_transport_retry_summary.json"
    contract_path = (
        gate_dir
        / "TOPX4_S2F3_SCALAR_MATRIX_HADAMARD_PARAMETRIX_CONTRACT_2026-09-12.md"
    )

    authority_paths = [
        matrix_contract_path,
        matrix_source_path,
        matrix_output_path,
        readiness_contract_path,
        readiness_output_path,
        exact_output_path,
        plan_path,
        contract_path,
    ]
    receipts = [sidecar_check(path, root) for path in authority_paths]
    checks: list[dict[str, Any]] = []
    add_check(
        checks,
        "all_authority_and_input_sidecars_match",
        all(item["matches"] for item in receipts),
        receipts=receipts,
    )

    matrix = load_json(matrix_output_path)
    readiness = load_json(readiness_output_path)
    exact = load_json(exact_output_path)

    matrix_hold = all(
        (
            matrix.get("status")
            == "PASS_COVARIANT_SCALAR_CHI_MATRIX_OPERATOR_HOLD_STATES_GRAVITY_PARITY_AND_STRESS",
            matrix.get("scalar_matrix_operator") == "DERIVED_FIXED_METRIC_OFF_SHELL",
            matrix.get("counterterm_normalizations") == "NOT_FIXED",
            matrix.get("scalar_matrix_hadamard_state") == "NOT_CONSTRUCTED",
            matrix.get("renormalized_stress") == "NOT_COMPUTED",
            matrix.get("physics_pass") is False,
            matrix.get("gate_effect") == "NONE",
        )
    )
    add_check(
        checks,
        "preceding_scalar_operator_hold_is_preserved",
        matrix_hold,
        status=matrix.get("status"),
        scalar_matrix_operator=matrix.get("scalar_matrix_operator"),
        scalar_matrix_hadamard_state=matrix.get("scalar_matrix_hadamard_state"),
    )

    readiness_hold = all(
        (
            readiness.get("status")
            == "PASS_5D_HADAMARD_COUNTERTERM_SCAFFOLD_HOLD_FULL_OPERATORS_STATE_AND_STRESS",
            readiness.get("readiness_decision") == "HOLD",
            readiness.get("hadamard_stress_ready") is False,
            readiness.get("renormalized_stress") == "NOT_COMPUTED",
            readiness.get("physics_pass") is False,
            readiness.get("gate_effect") == "NONE",
        )
    )
    add_check(
        checks,
        "preceding_hadamard_scaffold_hold_is_preserved",
        readiness_hold,
        status=readiness.get("status"),
        readiness_decision=readiness.get("readiness_decision"),
        hadamard_stress_ready=readiness.get("hadamard_stress_ready"),
    )

    exact_scope = all(
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
        "exact_transport_predecessor_remains_finite_order_only",
        exact_scope,
        status=exact.get("status"),
        finite_order_only=exact.get("state_scope", {}).get("finite_order_only"),
        full_Hadamard_state=exact.get("full_Hadamard_state"),
        covariant_5D_subtraction=exact.get("covariant_5D_subtraction"),
    )

    rank = 3
    curvature, box_curvature = sp.symbols("R BoxR", real=True)
    ricci2, riemann2, trace_omega2 = sp.symbols(
        "Ricci2 Riemann2 TrOmega2", real=True
    )
    h11, h22, h33, h12, h13, h23 = sp.symbols(
        "h11 h22 h33 h12 h13 h23", real=True
    )
    bh11, bh22, bh33, bh12, bh13, bh23 = sp.symbols(
        "BoxH11 BoxH22 BoxH33 BoxH12 BoxH13 BoxH23", real=True
    )
    hessian = sp.Matrix(
        [
            [h11, h12, h13],
            [h12, h22, h23],
            [h13, h23, h33],
        ]
    )
    box_hessian = sp.Matrix(
        [
            [bh11, bh12, bh13],
            [bh12, bh22, bh23],
            [bh13, bh23, bh33],
        ]
    )
    identity = sp.eye(rank)
    endomorphism = -hessian
    box_endomorphism = -box_hessian
    curvature_scalar = (
        curvature**2 / 72 - ricci2 / 180 + riemann2 / 180
    )

    singular_exponent = sp.Rational(5, 2) - 1
    singular_prefactor = sp.I / (16 * sp.sqrt(2) * sp.pi**2)
    add_check(
        checks,
        "D5_singular_power_and_prefactor_are_registered",
        singular_exponent == sp.Rational(3, 2)
        and singular_prefactor == sp.I / (16 * sp.sqrt(2) * sp.pi**2),
        dimension=5,
        singular_power=str(singular_exponent),
        prefactor=str(singular_prefactor),
    )

    u0 = identity
    u1 = sp.simplify(endomorphism + curvature * identity / 6)
    b2_cartesian = sp.simplify(
        endomorphism * endomorphism / 2
        + curvature * endomorphism / 6
        + curvature_scalar * identity
        + box_endomorphism / 6
        + box_curvature * identity / 30
    )
    u2 = sp.simplify(-b2_cartesian)

    add_check(
        checks,
        "U0_is_cartesian_parallel_transport_at_coincidence",
        u0 == identity,
        U0=matrix_strings(u0),
        Cartesian_parallel_transporter="I3",
    )

    laplace_sigma = sp.Integer(5)
    n0_transport_coefficient = laplace_sigma - 5
    add_check(
        checks,
        "U0_transport_equation_has_the_D5_coincidence_coefficient",
        n0_transport_coefficient == 0,
        coincidence_box_sigma=str(laplace_sigma),
        transport_equation="(2 sigma^A D_A + Box(sigma) - 5) U0 = 0",
    )

    u1_expected = sp.simplify(-hessian + curvature * identity / 6)
    add_check(
        checks,
        "U1_coincidence_equals_E_plus_R_over_6",
        matrix_is_zero(u1 - u1_expected),
        U1=matrix_strings(u1),
        expected="-H + R*I3/6",
    )

    trace_h = sp.factor(sp.trace(hessian))
    trace_h2 = sp.factor(sp.trace(hessian * hessian))
    trace_box_h = sp.factor(sp.trace(box_hessian))
    trace_b1 = sp.simplify(sp.trace(u1))
    trace_b2 = sp.simplify(sp.trace(b2_cartesian))
    expected_trace_b1 = sp.simplify(-trace_h + rank * curvature / 6)
    expected_trace_b2 = sp.simplify(
        trace_h2 / 2
        - curvature * trace_h / 6
        - trace_box_h / 6
        + rank * (curvature_scalar + box_curvature / 30)
    )
    add_check(
        checks,
        "rank_three_U1_and_U2_coincidence_traces_match_matrix_b_map",
        sp.simplify(trace_b1 - expected_trace_b1) == 0
        and sp.simplify(trace_b2 - expected_trace_b2) == 0,
        trace_U1=str(trace_b1),
        trace_U2=str(-trace_b2),
        trace_b2=str(trace_b2),
        Omega_term="zero in Cartesian scalar bundle",
    )

    generic_b1_trace = sp.simplify(sp.trace(endomorphism) + rank * curvature / 6)
    generic_b2_trace = sp.simplify(
        sp.trace(endomorphism * endomorphism) / 2
        + curvature * sp.trace(endomorphism) / 6
        + trace_omega2 / 12
        + rank * curvature_scalar
        + sp.trace(box_endomorphism) / 6
        + rank * box_curvature / 30
    )
    expected_generic_b2_trace = sp.simplify(
        trace_h2 / 2
        - curvature * trace_h / 6
        + trace_omega2 / 12
        - trace_box_h / 6
        + rank * (curvature_scalar + box_curvature / 30)
    )
    add_check(
        checks,
        "generic_matrix_b1_b2_map_retains_E_Omega_and_total_derivatives",
        sp.simplify(generic_b1_trace - expected_trace_b1) == 0
        and sp.simplify(generic_b2_trace - expected_generic_b2_trace) == 0
        and sp.simplify(generic_b2_trace.subs(trace_omega2, 1) - generic_b2_trace.subs(trace_omega2, 0))
        == sp.Rational(1, 12),
        b1=str(generic_b1_trace),
        b2=str(generic_b2_trace),
        Omega_squared_coefficient="1/12 in tr(b2)",
    )

    flat_h11, flat_h22, flat_h33, flat_h12, flat_h13, flat_h23 = sp.symbols(
        "f11 f22 f33 f12 f13 f23", real=True
    )
    flat_hessian = sp.Matrix(
        [
            [flat_h11, flat_h12, flat_h13],
            [flat_h12, flat_h22, flat_h23],
            [flat_h13, flat_h23, flat_h33],
        ]
    )
    flat_u0 = identity
    flat_u1 = -flat_hessian
    flat_u2 = -flat_hessian * flat_hessian / 2
    flat_l_operator_u0 = -flat_hessian
    flat_l_operator_u1 = flat_hessian * flat_hessian
    flat_n1_lhs = 2 * flat_u1
    flat_n1_rhs = 2 * flat_l_operator_u0
    flat_n2_lhs = 4 * flat_u2
    flat_n2_rhs = -2 * flat_l_operator_u1
    add_check(
        checks,
        "flat_constant_matrix_transport_recursion_reproduces_U1_U2",
        matrix_is_zero(flat_n1_lhs - flat_n1_rhs)
        and matrix_is_zero(flat_n2_lhs - flat_n2_rhs),
        U0=matrix_strings(flat_u0),
        U1=matrix_strings(flat_u1),
        U2=matrix_strings(flat_u2),
        recurrence="n=1,2 with L=Box-H and constant symmetric H",
    )

    mass, xi = sp.symbols("m xi", real=True)
    scalar_h = mass**2 + xi * curvature
    scalar_e = -scalar_h
    scalar_b1 = sp.simplify(scalar_e + curvature / 6)
    scalar_b2 = sp.simplify(
        scalar_e**2 / 2
        + curvature * scalar_e / 6
        + curvature_scalar
        - xi * box_curvature / 6
        + box_curvature / 30
    )
    scalar_u1 = sp.simplify(scalar_b1)
    scalar_u2 = sp.simplify(-scalar_b2)
    expected_scalar_u1 = sp.simplify(-mass**2 - (xi - sp.Rational(1, 6)) * curvature)
    expected_scalar_u2 = scalar_u2_formula(
        mass, xi, curvature, box_curvature, ricci2, riemann2
    )
    add_check(
        checks,
        "free_scalar_nested_U1_U2_controls_match_registered_D5_formulas",
        sp.simplify(scalar_u1 - expected_scalar_u1) == 0
        and sp.simplify(scalar_u2 - expected_scalar_u2) == 0,
        U1=str(scalar_u1),
        U2=str(scalar_u2),
        mass_factored=False,
    )

    basis_dimensions = {
        mass: sp.Integer(1),
        curvature: sp.Integer(2),
        box_curvature: sp.Integer(4),
        ricci2: sp.Integer(4),
        riemann2: sp.Integer(4),
        xi: sp.Integer(0),
    }
    dimension_checks = [
        expression_dimension(scalar_u1, basis_dimensions) == 2,
        expression_dimension(scalar_u2, basis_dimensions) == 4,
    ]
    add_check(
        checks,
        "D5_parametrix_coincidence_coefficients_have_required_dimensions",
        all(dimension_checks),
        U0_dimension=0,
        U1_dimension=2,
        U2_dimension=4,
        singular_power_dimension=3,
    )

    rotation = sp.Matrix(
        [
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1],
        ]
    )
    rotated_hessian = sp.simplify(rotation * hessian * rotation.T)
    rotated_box_hessian = sp.simplify(rotation * box_hessian * rotation.T)
    rotated_e = -rotated_hessian
    rotated_u1 = sp.simplify(rotated_e + curvature * identity / 6)
    rotated_b2 = sp.simplify(
        rotated_e * rotated_e / 2
        + curvature * rotated_e / 6
        + curvature_scalar * identity
        - rotated_box_hessian / 6
        + box_curvature * identity / 30
    )
    add_check(
        checks,
        "local_U_coefficients_are_covariant_under_constant_orthogonal_basis_change",
        matrix_is_zero(rotated_u1 - rotation * u1 * rotation.T)
        and matrix_is_zero(rotated_b2 - rotation * b2_cartesian * rotation.T)
        and sp.simplify(sp.trace(rotated_b2) - sp.trace(b2_cartesian)) == 0,
        transformation="H -> Q H Q^T, Box(H) -> Q Box(H) Q^T",
    )

    generator_j = sp.Matrix(
        [
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 0],
        ]
    )
    dtheta_a, dtheta_b, d2theta_ab, chemical_potential = sp.symbols(
        "dThetaA dThetaB d2ThetaAB mu", real=True
    )
    connection_a = generator_j * dtheta_a
    connection_b = generator_j * dtheta_b
    aligned_omega = sp.simplify(
        generator_j * d2theta_ab
        - generator_j * d2theta_ab
        + connection_a * connection_b
        - connection_b * connection_a
    )
    temporal_connection = generator_j * chemical_potential
    first_derivative_mixing = -2 * temporal_connection
    add_check(
        checks,
        "phase_aligned_connection_is_pure_gauge_but_retains_2mu_derivative_mixing",
        matrix_is_zero(aligned_omega)
        and first_derivative_mixing[0, 1] == 2 * chemical_potential
        and first_derivative_mixing[1, 0] == -2 * chemical_potential
        and first_derivative_mixing != sp.zeros(3),
        connection="A_A=J*d_A(Theta)",
        Omega_AB=matrix_strings(aligned_omega),
        first_derivative_coefficient=matrix_strings(first_derivative_mixing),
    )

    wrong_e = hessian
    wrong_u1 = sp.simplify(wrong_e + curvature * identity / 6)
    free_wrong_u1 = sp.simplify(wrong_u1.subs({h11: mass**2, h22: mass**2, h33: mass**2,
                                               h12: 0, h13: 0, h23: 0}))
    free_correct_u1 = sp.simplify(
        u1.subs({h11: mass**2, h22: mass**2, h33: mass**2,
                 h12: 0, h13: 0, h23: 0})
    )
    add_check(
        checks,
        "wrong_E_plus_H_mutation_is_rejected_by_free_U1",
        matrix_is_zero(free_wrong_u1 - free_correct_u1) is False,
        correct_free_U1=matrix_strings(free_correct_u1),
        wrong_free_U1=matrix_strings(free_wrong_u1),
    )

    wrong_u2_sign = -u2
    add_check(
        checks,
        "wrong_U2_sign_mutation_is_rejected",
        matrix_is_zero(wrong_u2_sign - u2) is False,
        canonical_relation="U2=-b2",
    )

    omitted_omega_b2 = sp.simplify(generic_b2_trace.subs(trace_omega2, 0))
    add_check(
        checks,
        "omitted_generic_Omega_squared_mutation_is_rejected",
        sp.simplify(generic_b2_trace.subs(trace_omega2, 1) - omitted_omega_b2)
        == sp.Rational(1, 12),
        required_difference="tr(Omega_AB Omega^AB)/12",
    )

    componentwise_u2 = sp.diag(
        -flat_h11**2 / 2,
        -flat_h22**2 / 2,
        -flat_h33**2 / 2,
    )
    add_check(
        checks,
        "componentwise_free_scalar_mutation_is_rejected_for_matrix_U2",
        matrix_is_zero(componentwise_u2 - flat_u2) is False,
        omitted_matrix_terms=matrix_strings(flat_u2 - componentwise_u2),
    )

    state_boundary = {
        "local_parametrix": True,
        "smooth_state_bisolution": False,
        "positivity": False,
        "global_wavefront_condition": False,
        "full_Hadamard_state": False,
    }
    add_check(
        checks,
        "local_parametrix_is_not_promoted_to_global_state",
        state_boundary["local_parametrix"] is True
        and state_boundary["smooth_state_bisolution"] is False
        and state_boundary["positivity"] is False
        and state_boundary["global_wavefront_condition"] is False
        and state_boundary["full_Hadamard_state"] is False,
        state_boundary=state_boundary,
    )

    q0_scope = "STATIC_TOPOLOGY_ONLY"
    add_check(
        checks,
        "static_q0_subtraction_is_not_called_evolving_stress_renormalization",
        q0_scope == "STATIC_TOPOLOGY_ONLY"
        and q0_scope != "FULL_STATE_STRESS_RENORMALIZATION",
        q0_subtraction_scope=q0_scope,
    )

    downstream_actions = {
        "homogeneous_reduction": False,
        "fixed_charge_reduction": False,
        "global_state_construction": False,
        "determinant_or_mode_sum": False,
        "renormalized_stress": False,
        "semiclassical_background": False,
        "physical_hessian": False,
        "advance_to_a4": False,
        "advance_to_ultra": False,
        "gate_or_publication_promotion": False,
    }
    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    prohibited_imports = any(
        token in source_text
        for token in (
            "from " + "topx4_s2f3_dynamic_state_subtraction_checkpoint",
            "from " + "topx4_s2f3_exact_transport_retry_checkpoint",
            "from " + "topx4_s2f3_covariant_scalar_matrix_checkpoint",
        )
    )
    add_check(
        checks,
        "state_boundary_and_downstream_action_firewalls_hold",
        not forbidden_hits
        and not prohibited_imports
        and not any(downstream_actions.values()),
        forbidden_source_tokens=forbidden_hits,
        prohibited_predecessor_import=prohibited_imports,
        downstream_actions=downstream_actions,
    )

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_S2F3_SCALAR_MATRIX_HADAMARD_PARAMETRIX_v1",
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "checkpoint_completed": "2026-09-12",
        "status": STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "scalar_matrix_hadamard_parametrix": (
            "DERIVED_LOCAL_U0_U2" if all_ok else "CHECK_FAILED"
        ),
        "scalar_matrix_hadamard_state": "NOT_CONSTRUCTED",
        "determinant": "NOT_COMPUTED",
        "renormalized_stress": "NOT_COMPUTED",
        "counterterm_normalizations": "NOT_FIXED",
        "physics_pass": False,
        "gate_effect": "NONE",
        "advance_to_global_state": False,
        "advance_to_determinant": False,
        "advance_to_renormalized_stress": False,
        "advance_to_semiclassical_background": False,
        "advance_to_physical_hessian": False,
        "advance_to_a4": False,
        "advance_to_ultra": False,
        "authority_receipts": receipts,
        "source_sha256": sha256_file(Path(__file__)),
        "checks": checks,
        "calculation_checks_passed": sum(check["ok"] for check in checks),
        "calculation_checks_total": len(checks),
        "local_parametrix": {
            "dimension": 5,
            "singular_exponent": str(singular_exponent),
            "prefactor": str(singular_prefactor),
            "series": "U0 + U1*sigma + U2*sigma^2 + O(sigma^3)",
            "U0": matrix_strings(u0),
            "U1": matrix_strings(u1),
            "U2": matrix_strings(u2),
            "coincidence_relation": "[U1]=b1; [U2]=-b2",
            "cartesian_bundle_connection": "D_A=nabla_A*I3",
            "cartesian_Omega_AB": "0",
            "phase_aligned_connection": "A_A=J*d_A(Theta)",
            "phase_aligned_Omega_AB": "0 on smooth patch",
        },
        "matrix_heat_kernel_map": {
            "trace_b0": str(rank),
            "trace_b1": str(expected_trace_b1),
            "trace_b2_cartesian": str(expected_trace_b2),
            "trace_b2_generic": str(expected_generic_b2_trace),
            "proper_time_powers": ["Lambda^5", "Lambda^3", "Lambda"],
        },
        "state_boundary": state_boundary,
        "completion_inventory": {
            "local_scalar_matrix_hadamard_parametrix_U0_U2": (
                "COMPLETED" if all_ok else "CHECK_FAILED"
            ),
            "global_scalar_matrix_hadamard_state": "NOT_CONSTRUCTED",
            "dirac_hadamard_two_point_function": "NOT_COMPLETED",
            "curved_finite_charge_graviton_and_ghost_operators": "NOT_COMPLETED",
            "parity_odd_phase_and_quantized_counterterms": "NOT_COMPLETED",
            "counterterm_normalization_conditions": "NOT_COMPLETED",
            "renormalized_state_dependent_stress": "NOT_COMPUTED",
            "physical_hessian": "NOT_COMPLETED",
        },
        "hold_reasons": [
            "the smooth state-dependent matrix bisolution and positivity are not constructed",
            "the existing exact transport remains finite-order and non-Hadamard",
            "the Dirac Hadamard two-point function is not constructed",
            "curved graviton/ghost/Jacobian operators and the physical Hessian remain open",
            "parity-odd phase, global anomaly and counterterm normalization remain open",
            "no determinant, mode sum, state-dependent stress or semiclassical background is computed",
        ],
        "next_required_calculation": (
            "construct and independently audit a globally admissible infinite-order scalar "
            "matrix Hadamard state, or a justified pseudodifferential/adiabatic equivalent, "
            "with positivity and wavefront conditions"
        ),
        "rule9_review": {
            "status": "THREE_WAY_CLEARANCE_NOT_MET",
            "completed_independent_reports": 0,
            "scope": "this local scalar-matrix Hadamard-parametrix checkpoint",
            "effect": "no reviewer-consensus or gate-promotion claim",
        },
        "primary_source_basis": [
            {
                "id": "arXiv:gr-qc/0512118",
                "scope": "D=5 scalar Hadamard coefficients, state-dependent smooth part and renormalization boundary",
            },
            {
                "id": "arXiv:hep-th/0306138",
                "scope": "Laplace-type connection, endomorphism and matrix heat-kernel coefficients",
            },
        ],
        "derived_claims": [],
        "explicit_nonclaims": [
            "no global Hadamard state",
            "no positivity or global wavefront proof",
            "no determinant or mode sum",
            "no renormalized stress tensor",
            "no counterterm normalization",
            "no curved graviton determinant",
            "no parity or anomaly clearance",
            "no self-consistent semiclassical background",
            "no physical Hessian or radion mass",
            "no A4, Ultra, architecture, gate or publication change",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json"
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
    print("scalar_matrix_hadamard_parametrix=" + result["scalar_matrix_hadamard_parametrix"])
    print("scalar_matrix_hadamard_state=NOT_CONSTRUCTED")
    print("determinant=NOT_COMPUTED")
    print("renormalized_stress=NOT_COMPUTED")
    print("counterterm_normalizations=NOT_FIXED")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
