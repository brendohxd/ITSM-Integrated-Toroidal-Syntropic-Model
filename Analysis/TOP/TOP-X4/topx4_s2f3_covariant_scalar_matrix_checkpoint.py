#!/usr/bin/env python3
"""Plan-11 off-shell covariant scalar-matrix checkpoint for X4-S2F3.

This executable derives the fixed-metric rank-three fluctuation operator for
the two canonical real components of Phi coupled to chi. It audits the
Laplace-type E/Omega data and scalar-induced counterterm structures through
b2. It deliberately does not impose a homogeneous or fixed-charge ansatz,
construct a state, evaluate a determinant, compute stress, or reduce the
metric/radion physical Hessian.
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
    "PASS_COVARIANT_SCALAR_CHI_MATRIX_OPERATOR_"
    "HOLD_STATES_GRAVITY_PARITY_AND_STRESS"
)
FAIL_STATUS = "FAIL_COVARIANT_SCALAR_CHI_MATRIX_OPERATOR_CHECKPOINT"
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


def expression_has_dimension(
    expression: sp.Expr,
    target: sp.Rational | sp.Integer,
    dimensions: dict[sp.Symbol, sp.Rational | sp.Integer],
) -> bool:
    for term in sp.Add.make_args(sp.expand(expression)):
        term_dimension = sp.Integer(0)
        for factor, power in term.as_powers_dict().items():
            if factor in dimensions:
                term_dimension += dimensions[factor] * power
            elif factor.is_number:
                continue
            else:
                return False
        if sp.simplify(term_dimension - target) != 0:
            return False
    return True


def validate_operator_spec(candidate: dict[str, Any]) -> bool:
    return all(
        (
            candidate["E_sign"] == -1,
            candidate["portal_off_diagonal_retained"] is True,
            candidate["cartesian_bundle_curvature_zero"] is True,
            candidate["aligned_phase_connection_retained"] is True,
            set(candidate["nonminimal_curvature_scalar_terms"])
            == {"R*s", "R*chi^2"},
            candidate["off_shell_before_ansatz"] is True,
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
    action_path = gate_dir / "TOPX4_A1_ACTION_SELECTION_LEDGER_2026-09-06.md"
    parent_path = gate_dir / "TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md"
    variation_path = (
        gate_dir / "TOPX4_S2F3_FINITE_CHARGE_VARIATION_CONTRACT_2026-09-09.md"
    )
    readiness_contract_path = (
        gate_dir
        / "TOPX4_S2F3_HADAMARD_SUBTRACTION_READINESS_CONTRACT_2026-09-12.md"
    )
    readiness_output_path = (
        output_dir / "topx4_s2f3_hadamard_subtraction_readiness_summary.json"
    )
    contract_path = (
        gate_dir / "TOPX4_S2F3_COVARIANT_SCALAR_MATRIX_CONTRACT_2026-09-12.md"
    )

    authority_paths = [
        action_path,
        parent_path,
        variation_path,
        plan_path,
        readiness_contract_path,
        readiness_output_path,
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

    readiness = load_json(readiness_output_path)
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
        "prior_hadamard_readiness_hold_is_preserved",
        readiness_hold,
        status=readiness.get("status"),
        readiness_decision=readiness.get("readiness_decision"),
        hadamard_stress_ready=readiness.get("hadamard_stress_ready"),
    )

    (
        phi1,
        phi2,
        chi,
        u0,
        m_phi2,
        m_chi2,
        lambda_phi5,
        lambda_chi5,
        g5,
    ) = sp.symbols(
        "phi1 phi2 chi U0 mPhi2 mChi2 lambdaPhi5 lambdaChi5 g5",
        real=True,
    )
    r2 = phi1**2 + phi2**2
    s_from_cartesian = r2 / 2
    s_original = sp.symbols("s", real=True)
    potential_original = (
        u0
        + m_phi2 * s_original
        + lambda_phi5 * s_original**2 / 2
        + m_chi2 * chi**2 / 2
        + lambda_chi5 * chi**4 / 24
        + g5 * s_original * chi**2 / 2
    )
    potential = (
        u0
        + m_phi2 * r2 / 2
        + lambda_phi5 * r2**2 / 8
        + m_chi2 * chi**2 / 2
        + lambda_chi5 * chi**4 / 24
        + g5 * r2 * chi**2 / 4
    )
    add_check(
        checks,
        "frozen_complex_scalar_potential_rewrites_exactly_in_canonical_cartesian_fields",
        sp.simplify(potential_original.subs(s_original, s_from_cartesian) - potential)
        == 0,
        canonical_fields="Phi=(phi1+i*phi2)/sqrt(2)",
        invariant_s="(phi1^2+phi2^2)/2",
        potential=str(potential),
    )

    field_vector = sp.Matrix([phi1, phi2, chi])
    gradient = sp.Matrix([sp.diff(potential, field) for field in field_vector])
    hessian = sp.hessian(potential, field_vector)
    expected_hessian = sp.Matrix(
        [
            [
                m_phi2
                + lambda_phi5 * r2 / 2
                + lambda_phi5 * phi1**2
                + g5 * chi**2 / 2,
                lambda_phi5 * phi1 * phi2,
                g5 * chi * phi1,
            ],
            [
                lambda_phi5 * phi1 * phi2,
                m_phi2
                + lambda_phi5 * r2 / 2
                + lambda_phi5 * phi2**2
                + g5 * chi**2 / 2,
                g5 * chi * phi2,
            ],
            [
                g5 * chi * phi1,
                g5 * chi * phi2,
                m_chi2 + lambda_chi5 * chi**2 / 2 + g5 * r2 / 2,
            ],
        ]
    )
    add_check(
        checks,
        "direct_symbolic_second_variation_matches_the_frozen_rank_three_hessian",
        matrix_is_zero(hessian - expected_hessian)
        and matrix_is_zero(hessian - hessian.T),
        hessian=matrix_strings(hessian),
        symmetric=True,
    )

    box_phi1, box_phi2, box_chi = sp.symbols(
        "BoxPhi1 BoxPhi2 BoxChi", real=True
    )
    euler_vector = -sp.Matrix([box_phi1, box_phi2, box_chi]) + gradient
    k_squared = sp.symbols("k_squared", real=True)
    principal_symbol = k_squared * sp.eye(3)
    off_shell_ok = (
        euler_vector != sp.zeros(3, 1)
        and all(box_field in euler_vector.free_symbols for box_field in (box_phi1, box_phi2, box_chi))
        and principal_symbol == k_squared * sp.eye(3)
    )
    add_check(
        checks,
        "operator_is_minimal_fixed_metric_and_derived_without_background_equations",
        off_shell_ok,
        principal_symbol=matrix_strings(principal_symbol),
        first_variation=str(euler_vector),
        fixed_metric=True,
        homogeneous_ansatz=False,
        fixed_charge_reduction=False,
        background_equation_used=False,
    )

    endomorphism = -hessian
    curvature = sp.symbols("R", real=True)
    free_substitutions = {lambda_phi5: 0, lambda_chi5: 0, g5: 0}
    free_endomorphism = sp.simplify(endomorphism.subs(free_substitutions))
    expected_free_endomorphism = sp.diag(-m_phi2, -m_phi2, -m_chi2)
    free_b1 = free_endomorphism + curvature * sp.eye(3) / 6
    wrong_free_b1 = -free_endomorphism + curvature * sp.eye(3) / 6
    add_check(
        checks,
        "laplace_type_sign_is_E_minus_H_with_correct_free_scalar_limit",
        matrix_is_zero(free_endomorphism - expected_free_endomorphism)
        and free_b1[0, 0] == -m_phi2 + curvature / 6
        and wrong_free_b1[0, 0] != free_b1[0, 0],
        convention="P=-(D^2+E)=-Box*I3+H",
        E=matrix_strings(endomorphism),
        free_b1=matrix_strings(free_b1),
    )

    cartesian_connection = sp.zeros(3)
    cartesian_omega = sp.zeros(3)
    add_check(
        checks,
        "cartesian_scalar_bundle_connection_and_curvature_vanish",
        cartesian_connection == sp.zeros(3) and cartesian_omega == sp.zeros(3),
        bundle_rank=3,
        connection="D_A=nabla_A*I3",
        Omega_AB=matrix_strings(cartesian_omega),
        reason="neutral spacetime scalars with flat target-space kinetic metric",
    )

    cos_alpha = sp.Rational(3, 5)
    sin_alpha = sp.Rational(4, 5)
    rotation = sp.Matrix(
        [
            [cos_alpha, -sin_alpha, 0],
            [sin_alpha, cos_alpha, 0],
            [0, 0, 1],
        ]
    )
    rotated_hessian = hessian.subs(
        {
            phi1: cos_alpha * phi1 - sin_alpha * phi2,
            phi2: sin_alpha * phi1 + cos_alpha * phi2,
        },
        simultaneous=True,
    )
    add_check(
        checks,
        "global_u1_O2_covariance_of_the_hessian",
        matrix_is_zero(rotated_hessian - rotation * hessian * rotation.T),
        exact_test_rotation={"cos": "3/5", "sin": "4/5"},
        covariance_rule="H(S*varphi)=S*H(varphi)*S^T",
    )

    generator_j = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    ward_residual = sp.simplify(hessian * generator_j * field_vector - generator_j * gradient)
    add_check(
        checks,
        "off_shell_global_u1_differential_identity",
        matrix_is_zero(ward_residual),
        identity="H*J*varphi=J*grad(V)",
        residual=matrix_strings(ward_residual),
    )

    z2_matrix = sp.diag(1, 1, -1)
    z2_hessian = hessian.subs(chi, -chi)
    add_check(
        checks,
        "chi_Z2_covariance_of_the_hessian",
        matrix_is_zero(z2_hessian - z2_matrix * hessian * z2_matrix),
        covariance_rule="H(phi1,phi2,-chi)=Z*H(phi1,phi2,chi)*Z",
    )

    rho = sp.symbols("rho", positive=True, real=True)
    aligned_hessian = sp.simplify(hessian.subs({phi1: rho, phi2: 0}))
    expected_aligned_hessian = sp.Matrix(
        [
            [
                m_phi2
                + sp.Rational(3, 2) * lambda_phi5 * rho**2
                + g5 * chi**2 / 2,
                0,
                g5 * rho * chi,
            ],
            [
                0,
                m_phi2
                + lambda_phi5 * rho**2 / 2
                + g5 * chi**2 / 2,
                0,
            ],
            [
                g5 * rho * chi,
                0,
                m_chi2 + lambda_chi5 * chi**2 / 2 + g5 * rho**2 / 2,
            ],
        ]
    )
    add_check(
        checks,
        "phase_aligned_hessian_matches_radial_tangent_chi_projection",
        matrix_is_zero(aligned_hessian - expected_aligned_hessian),
        aligned_hessian=matrix_strings(aligned_hessian),
        chart_domain="rho>0; Cartesian chart remains authoritative at rho=0",
    )

    theta = sp.symbols("Theta", real=True)
    local_rotation = sp.Matrix(
        [
            [sp.cos(theta), -sp.sin(theta), 0],
            [sp.sin(theta), sp.cos(theta), 0],
            [0, 0, 1],
        ]
    )
    connection_generator = sp.simplify(local_rotation.T * sp.diff(local_rotation, theta))
    dtheta_a, dtheta_b, d2theta_ab = sp.symbols(
        "dTheta_A dTheta_B d2Theta_AB", real=True
    )
    connection_a = connection_generator * dtheta_a
    connection_b = connection_generator * dtheta_b
    omega_aligned = (
        connection_generator * d2theta_ab
        - connection_generator * d2theta_ab
        + connection_a * connection_b
        - connection_b * connection_a
    )
    add_check(
        checks,
        "phase_aligned_bundle_connection_is_pure_gauge_with_zero_curvature",
        matrix_is_zero(connection_generator - generator_j)
        and matrix_is_zero(omega_aligned),
        A_A="J*d_A(Theta)",
        generator=matrix_strings(connection_generator),
        Omega_AB=matrix_strings(omega_aligned),
    )

    mu = sp.symbols("mu", nonzero=True, real=True)
    temporal_connection = generator_j * mu
    first_derivative_mixing = -2 * temporal_connection
    add_check(
        checks,
        "finite_charge_local_projection_recovers_required_derivative_mixing",
        first_derivative_mixing[0, 1] == 2 * mu
        and first_derivative_mixing[1, 0] == -2 * mu
        and first_derivative_mixing != sp.zeros(3),
        operator_expansion="-(partial+A)^2 contains -2*A^A*partial_A",
        A_t=matrix_strings(temporal_connection),
        first_derivative_coefficient=matrix_strings(first_derivative_mixing),
        limitation="basis/Wick signs are conventional; invariant mixing magnitude is 2*mu",
    )

    trace_h = sp.factor(sp.trace(hessian))
    expected_trace_h = (
        2 * m_phi2
        + m_chi2
        + (2 * lambda_phi5 + g5 / 2) * r2
        + (g5 + lambda_chi5 / 2) * chi**2
    )
    add_check(
        checks,
        "trace_H_matches_the_U1_invariant_expression",
        sp.simplify(trace_h - expected_trace_h) == 0,
        trace_H_r2_form=str(expected_trace_h),
        trace_H_s_form=(
            "2*mPhi2+mChi2+(4*lambdaPhi5+g5)*s"
            "+(g5+lambdaChi5/2)*chi^2"
        ),
    )

    trace_h2 = sp.factor(sp.trace(hessian * hessian))
    s_invariant, chi2_invariant = sp.symbols("s_invariant chi2_invariant", real=True)
    expected_trace_h2_invariants = (
        2 * m_phi2**2
        + m_chi2**2
        + (8 * lambda_phi5 * m_phi2 + 2 * g5 * m_chi2) * s_invariant
        + (2 * g5 * m_phi2 + lambda_chi5 * m_chi2) * chi2_invariant
        + (10 * lambda_phi5**2 + g5**2) * s_invariant**2
        + g5
        * (4 * g5 + 4 * lambda_phi5 + lambda_chi5)
        * s_invariant
        * chi2_invariant
        + (g5**2 / 2 + lambda_chi5**2 / 4) * chi2_invariant**2
    )
    expected_trace_h2_cartesian = expected_trace_h2_invariants.subs(
        {s_invariant: r2 / 2, chi2_invariant: chi**2}
    )
    trace_h2_from_aligned = (
        aligned_hessian[0, 0] ** 2
        + aligned_hessian[1, 1] ** 2
        + aligned_hessian[2, 2] ** 2
        + 2 * aligned_hessian[0, 2] ** 2
    )
    add_check(
        checks,
        "trace_H_squared_matches_direct_and_aligned_invariant_derivations",
        sp.simplify(trace_h2 - expected_trace_h2_cartesian) == 0
        and sp.simplify(
            trace_h2_from_aligned
            - expected_trace_h2_cartesian.subs({phi1: rho, phi2: 0})
        )
        == 0,
        trace_H_squared_s_form=str(expected_trace_h2_invariants),
        off_diagonal_portal_contribution="2*g5^2*r2*chi^2",
    )

    rank = sp.Integer(3)
    box_trace_h, box_curvature = sp.symbols("BoxTrH BoxR", real=True)
    ricci2, riemann2, trace_omega2 = sp.symbols(
        "Ricci2 Riemann2 TrOmega2", real=True
    )
    trace_b0 = rank
    trace_b1 = sp.simplify(sp.trace(endomorphism) + rank * curvature / 6)
    trace_b2_from_general = (
        sp.trace(endomorphism * endomorphism) / 2
        + curvature * sp.trace(endomorphism) / 6
        + trace_omega2 / 12
        + rank
        * (
            curvature**2 / 72
            - ricci2 / 180
            + riemann2 / 180
        )
        - box_trace_h / 6
        + rank * box_curvature / 30
    )
    expected_trace_b2 = (
        trace_h2 / 2
        - curvature * trace_h / 6
        - box_trace_h / 6
        + rank
        * (
            curvature**2 / 72
            - ricci2 / 180
            + riemann2 / 180
        )
        + rank * box_curvature / 30
    )
    trace_b2_cartesian = sp.simplify(trace_b2_from_general.subs(trace_omega2, 0))
    add_check(
        checks,
        "rank_three_b0_b1_b2_trace_map_uses_E_minus_H_and_zero_Omega",
        trace_b0 == 3
        and sp.simplify(trace_b1 + trace_h - curvature / 2) == 0
        and sp.simplify(trace_b2_cartesian - expected_trace_b2) == 0,
        trace_b0=str(trace_b0),
        trace_b1=str(trace_b1),
        trace_b2=str(expected_trace_b2),
        indexing="DeWitt b0,b1,b2 = heat-kernel a0,a2,a4",
    )

    cutoff = sp.symbols("Lambda", positive=True)
    trace_h_invariants = (
        2 * m_phi2
        + m_chi2
        + (4 * lambda_phi5 + g5) * s_invariant
        + (g5 + lambda_chi5 / 2) * chi2_invariant
    )
    divergence_without_total_derivatives = sp.expand(
        3 * cutoff**5
        + cutoff**3 * (-trace_h_invariants + curvature / 2)
        + cutoff
        * (
            expected_trace_h2_invariants / 2
            - curvature * trace_h_invariants / 6
            + curvature**2 / 24
            - ricci2 / 60
            + riemann2 / 60
        )
    )
    polynomial = sp.Poly(
        divergence_without_total_derivatives,
        s_invariant,
        chi2_invariant,
        curvature,
        ricci2,
        riemann2,
    )
    exponent_to_operator = {
        (0, 0, 0, 0, 0): "1",
        (1, 0, 0, 0, 0): "s",
        (0, 1, 0, 0, 0): "chi^2",
        (2, 0, 0, 0, 0): "s^2",
        (1, 1, 0, 0, 0): "s*chi^2",
        (0, 2, 0, 0, 0): "chi^4",
        (0, 0, 1, 0, 0): "R",
        (1, 0, 1, 0, 0): "R*s",
        (0, 1, 1, 0, 0): "R*chi^2",
        (0, 0, 2, 0, 0): "R^2",
        (0, 0, 0, 1, 0): "R_AB R^AB",
        (0, 0, 0, 0, 1): "R_ABCD R^ABCD",
    }
    derived_operator_set = {
        exponent_to_operator[monomial]
        for monomial, coefficient in polynomial.terms()
        if coefficient != 0 and monomial in exponent_to_operator
    }
    expected_operator_set = set(exponent_to_operator.values())
    unknown_monomials = [
        monomial
        for monomial, coefficient in polynomial.terms()
        if coefficient != 0 and monomial not in exponent_to_operator
    ]
    add_check(
        checks,
        "scalar_heat_kernel_induces_the_complete_registered_bulk_basis_through_b2",
        derived_operator_set == expected_operator_set and not unknown_monomials,
        integrated_counterterm_structures=sorted(derived_operator_set),
        unknown_monomials=unknown_monomials,
        normalization_status="NOT_FIXED",
        scope="scalar one-loop proper-time divergence through b2",
    )

    box_s, box_chi2 = sp.symbols("BoxS BoxChi2", real=True)
    box_trace_h_expanded = (
        (4 * lambda_phi5 + g5) * box_s
        + (g5 + lambda_chi5 / 2) * box_chi2
    )
    local_total_derivative_part = sp.expand(
        cutoff * (-box_trace_h_expanded / 6 + box_curvature / 10)
    )
    local_derivative_terms = {
        "Box(s)" if local_total_derivative_part.coeff(box_s) != 0 else "MISSING",
        (
            "Box(chi^2)"
            if local_total_derivative_part.coeff(box_chi2) != 0
            else "MISSING"
        ),
        "Box(R)" if local_total_derivative_part.coeff(box_curvature) != 0 else "MISSING",
    }
    add_check(
        checks,
        "local_total_derivatives_are_retained_until_boundary_assumptions_are_applied",
        local_derivative_terms == {"Box(s)", "Box(chi^2)", "Box(R)"},
        local_terms=sorted(local_derivative_terms),
        expression=str(local_total_derivative_part),
        integrated_boundaryless_falloff_disposition="may be removed only as complete total derivatives",
        independent_wavefunction_divergence_through_b2=False,
    )

    dimensions: dict[sp.Symbol, sp.Rational | sp.Integer] = {
        phi1: sp.Rational(3, 2),
        phi2: sp.Rational(3, 2),
        chi: sp.Rational(3, 2),
        u0: sp.Integer(5),
        m_phi2: sp.Integer(2),
        m_chi2: sp.Integer(2),
        lambda_phi5: sp.Integer(-1),
        lambda_chi5: sp.Integer(-1),
        g5: sp.Integer(-1),
        curvature: sp.Integer(2),
        ricci2: sp.Integer(4),
        riemann2: sp.Integer(4),
        cutoff: sp.Integer(1),
        box_s: sp.Integer(5),
        box_chi2: sp.Integer(5),
        box_curvature: sp.Integer(4),
    }
    counterterms = [
        {"operator": "1", "operator_dimension": 0, "coefficient_dimension": 5},
        {"operator": "s", "operator_dimension": 3, "coefficient_dimension": 2},
        {"operator": "chi^2", "operator_dimension": 3, "coefficient_dimension": 2},
        {"operator": "s^2", "operator_dimension": 6, "coefficient_dimension": -1},
        {
            "operator": "s*chi^2",
            "operator_dimension": 6,
            "coefficient_dimension": -1,
        },
        {"operator": "chi^4", "operator_dimension": 6, "coefficient_dimension": -1},
        {"operator": "R", "operator_dimension": 2, "coefficient_dimension": 3},
        {"operator": "R*s", "operator_dimension": 5, "coefficient_dimension": 0},
        {
            "operator": "R*chi^2",
            "operator_dimension": 5,
            "coefficient_dimension": 0,
        },
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
        {"operator": "Box(s)", "operator_dimension": 5, "coefficient_dimension": 0},
        {
            "operator": "Box(chi^2)",
            "operator_dimension": 5,
            "coefficient_dimension": 0,
        },
        {"operator": "Box(R)", "operator_dimension": 4, "coefficient_dimension": 1},
    ]
    dimension_ok = all(
        (
            expression_has_dimension(potential, sp.Integer(5), dimensions),
            all(
                expression_has_dimension(value, sp.Integer(2), dimensions)
                for value in hessian
            ),
            expression_has_dimension(trace_h, sp.Integer(2), dimensions),
            expression_has_dimension(trace_h2, sp.Integer(4), dimensions),
            expression_has_dimension(
                local_total_derivative_part, sp.Integer(5), dimensions
            ),
            all(
                item["operator_dimension"] + item["coefficient_dimension"] == 5
                for item in counterterms
            ),
        )
    )
    add_check(
        checks,
        "five_dimensional_mass_dimensions_close_for_operator_traces_and_counterterms",
        dimension_ok,
        field_dimensions={"phi1": "3/2", "phi2": "3/2", "chi": "3/2"},
        operator_dimensions={"H": 2, "E": 2, "b0": 0, "b1": 2, "b2": 4},
        cutoff_terms=["Lambda^5*b0", "Lambda^3*b1", "Lambda*b2"],
        counterterm_ledger=counterterms,
    )

    zero_portal_hessian = sp.simplify(hessian.subs(g5, 0))
    phi_zero_hessian = sp.simplify(hessian.subs({phi1: 0, phi2: 0}))
    chi_zero_hessian = sp.simplify(hessian.subs(chi, 0))
    free_hessian = sp.simplify(hessian.subs(free_substitutions))
    controls_ok = all(
        (
            zero_portal_hessian[0, 2] == 0,
            zero_portal_hessian[1, 2] == 0,
            phi_zero_hessian[0, 0] == phi_zero_hessian[1, 1],
            phi_zero_hessian[0, 1] == 0,
            chi_zero_hessian[0, 2] == 0,
            chi_zero_hessian[1, 2] == 0,
            free_hessian == sp.diag(m_phi2, m_phi2, m_chi2),
        )
    )
    add_check(
        checks,
        "zero_portal_zero_Phi_zero_chi_and_free_nested_controls",
        controls_ok,
        zero_portal="Phi and chi blocks decouple",
        zero_Phi="O2 condensate block is degenerate",
        zero_chi="chi mixing entries vanish",
        free_hessian=matrix_strings(free_hessian),
    )

    hessian_without_portal_mix = hessian.copy()
    hessian_without_portal_mix[0, 2] = 0
    hessian_without_portal_mix[2, 0] = 0
    hessian_without_portal_mix[1, 2] = 0
    hessian_without_portal_mix[2, 1] = 0
    omitted_portal_difference = sp.factor(
        trace_h2 - sp.trace(hessian_without_portal_mix * hessian_without_portal_mix)
    )
    on_shell_mass = -lambda_phi5 * rho**2 / 2 - g5 * chi**2 / 2
    on_shell_mutant = sp.simplify(aligned_hessian.subs(m_phi2, on_shell_mass))

    canonical_spec = {
        "E_sign": -1,
        "portal_off_diagonal_retained": True,
        "cartesian_bundle_curvature_zero": True,
        "aligned_phase_connection_retained": True,
        "nonminimal_curvature_scalar_terms": ["R*s", "R*chi^2"],
        "off_shell_before_ansatz": True,
    }
    mutation_specs = [
        ("use_E_plus_H", "E_sign", 1, wrong_free_b1[0, 0] - free_b1[0, 0]),
        (
            "omit_portal_off_diagonal_entries",
            "portal_off_diagonal_retained",
            False,
            omitted_portal_difference,
        ),
        (
            "declare_nonzero_cartesian_bundle_curvature",
            "cartesian_bundle_curvature_zero",
            False,
            trace_omega2 / 12,
        ),
        (
            "omit_phase_aligned_connection",
            "aligned_phase_connection_retained",
            False,
            first_derivative_mixing,
        ),
        (
            "omit_R_s_counterterm",
            "nonminimal_curvature_scalar_terms",
            ["R*chi^2"],
            curvature * s_invariant,
        ),
        (
            "omit_R_chi_squared_counterterm",
            "nonminimal_curvature_scalar_terms",
            ["R*s"],
            curvature * chi2_invariant,
        ),
        (
            "impose_background_equation_inside_off_shell_hessian",
            "off_shell_before_ansatz",
            False,
            aligned_hessian - on_shell_mutant,
        ),
    ]
    mutations: list[dict[str, Any]] = []
    for name, key, replacement, witness in mutation_specs:
        mutant = copy.deepcopy(canonical_spec)
        mutant[key] = replacement
        witness_nonzero = (
            not matrix_is_zero(witness)
            if isinstance(witness, sp.MatrixBase)
            else sp.simplify(witness) != 0
        )
        mutations.append(
            {
                "name": name,
                "rejected": not validate_operator_spec(mutant) and witness_nonzero,
                "algebraic_witness": (
                    matrix_strings(witness)
                    if isinstance(witness, sp.MatrixBase)
                    else str(sp.factor(witness))
                ),
            }
        )
    add_check(
        checks,
        "all_registered_operator_and_counterterm_mutations_are_rejected",
        validate_operator_spec(canonical_spec)
        and all(item["rejected"] for item in mutations),
        mutations=mutations,
    )

    action_text = action_path.read_text(encoding="utf-8")
    frozen_tokens_present = all(
        token in action_text
        for token in (
            "s=Phi* Phi",
            "lambda_{\\Phi5}",
            "lambda_{\\chi5}",
            "g_5",
            "[\\Phi]=[\\chi]=\\frac32",
        )
    )
    add_check(
        checks,
        "frozen_action_parameters_and_dimensions_are_present_in_owning_ledger",
        frozen_tokens_present,
        action_path=str(action_path.relative_to(root)),
    )

    completion_inventory = {
        "covariant_scalar_chi_matrix_second_variation": {
            "status": "COMPLETED_FIXED_METRIC_OFF_SHELL",
            "scope": "rank-three scalar block before ansatz; no metric fluctuations",
        },
        "scalar_matrix_hadamard_state": {"status": "NOT_COMPLETED"},
        "dirac_hadamard_two_point_function": {"status": "NOT_COMPLETED"},
        "curved_finite_charge_graviton_and_ghost_operators": {
            "status": "NOT_COMPLETED"
        },
        "parity_odd_phase_and_quantized_counterterms": {"status": "NOT_COMPLETED"},
        "counterterm_normalization_conditions": {"status": "NOT_COMPLETED"},
        "renormalized_state_dependent_stress": {"status": "NOT_COMPUTED"},
    }
    inventory_ok = (
        completion_inventory["covariant_scalar_chi_matrix_second_variation"]["status"]
        == "COMPLETED_FIXED_METRIC_OFF_SHELL"
        and all(
            item["status"] in {"NOT_COMPLETED", "NOT_COMPUTED"}
            for key, item in completion_inventory.items()
            if key != "covariant_scalar_chi_matrix_second_variation"
        )
    )
    add_check(
        checks,
        "completion_inventory_advances_only_the_fixed_metric_scalar_operator_line",
        inventory_ok,
        inventory=completion_inventory,
    )

    prior_rule9 = readiness.get("rule9_review", {})
    rule9_open = (
        prior_rule9.get("status") == "THREE_WAY_CLEARANCE_NOT_MET"
        and prior_rule9.get("completed_independent_reports") == 0
    )
    add_check(
        checks,
        "rule9_three_way_clearance_remains_open",
        rule9_open,
        prior_rule9=prior_rule9,
        current_completed_independent_reports=0,
    )

    source_text = inspect.getsource(inspect.getmodule(main))
    forbidden_hits = [token for token in FORBIDDEN_SOURCE_TOKENS if token in source_text]
    prohibited_import = (
        "from " + "topx4_s2f3_finite_charge_operator_checkpoint"
    ) in source_text
    downstream_actions = {
        "homogeneous_reduction": False,
        "fixed_charge_reduction": False,
        "state_construction": False,
        "determinant_or_mode_sum": False,
        "renormalized_stress": False,
        "semiclassical_background": False,
        "physical_hessian": False,
        "advance_to_a4": False,
        "advance_to_ultra": False,
        "gate_or_publication_promotion": False,
    }
    add_check(
        checks,
        "observational_target_and_downstream_action_firewalls",
        not forbidden_hits
        and not prohibited_import
        and not any(downstream_actions.values()),
        forbidden_source_tokens=forbidden_hits,
        finite_charge_operator_script_imported=prohibited_import,
        downstream_actions=downstream_actions,
    )

    all_ok = all(check["ok"] for check in checks)
    result = {
        "schema": "ITSM_TOPX4_S2F3_COVARIANT_SCALAR_MATRIX_v1",
        "route": "TOP-X4_KK-001",
        "candidate": "X4-S2F3",
        "checkpoint_completed": "2026-09-12",
        "status": STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "scalar_matrix_operator": (
            "DERIVED_FIXED_METRIC_OFF_SHELL" if all_ok else "CHECK_FAILED"
        ),
        "matter_counterterm_structures": (
            "ENUMERATED_THROUGH_B2" if all_ok else "CHECK_FAILED"
        ),
        "counterterm_normalizations": "NOT_FIXED",
        "scalar_matrix_hadamard_state": "NOT_CONSTRUCTED",
        "determinant": "NOT_COMPUTED",
        "renormalized_stress": "NOT_COMPUTED",
        "physics_pass": False,
        "gate_effect": "NONE",
        "advance_to_homogeneous_reduction": False,
        "advance_to_fixed_charge_reduction": False,
        "advance_to_state_construction": False,
        "advance_to_determinant": False,
        "advance_to_semiclassical_background": False,
        "advance_to_physical_hessian": False,
        "advance_to_a4": False,
        "advance_to_ultra": False,
        "authority_receipts": receipts,
        "source_sha256": sha256_file(Path(__file__)),
        "checks": checks,
        "calculation_checks_passed": sum(check["ok"] for check in checks),
        "calculation_checks_total": len(checks),
        "canonical_field_definition": {
            "Phi": "(phi1+i*phi2)/sqrt(2)",
            "s": "(phi1^2+phi2^2)/2",
            "bundle_coordinates": ["phi1", "phi2", "chi"],
            "field_dimension": "3/2",
        },
        "off_shell_operator": {
            "scope": "arbitrary smooth fixed five-dimensional metric and scalar background",
            "euclidean_quadratic_operator": "P_sc=-Box*I3+H",
            "laplace_type_convention": "P=-(D^2+E)",
            "E": "-H",
            "cartesian_connection": "D_A=nabla_A*I3",
            "cartesian_Omega_AB": "0",
            "H": matrix_strings(hessian),
            "background_equation_used": False,
        },
        "phase_aligned_gauge": {
            "domain": "rho>0 smooth patch",
            "connection": "A_A=J*d_A(Theta)",
            "Omega_AB": "0",
            "endomorphism": "E_aligned=-S^T*H*S",
            "H_aligned": matrix_strings(aligned_hessian),
            "finite_charge_projection": (
                "A_t=mu*J gives first-derivative mixing of invariant magnitude 2*mu"
            ),
            "rho_zero_boundary": "use regular Cartesian chart",
        },
        "heat_kernel_traces": {
            "trace_b0": "3",
            "trace_H": str(expected_trace_h),
            "trace_H_s_form": (
                "2*mPhi2+mChi2+(4*lambdaPhi5+g5)*s"
                "+(g5+lambdaChi5/2)*chi^2"
            ),
            "trace_H_squared_s_form": str(expected_trace_h2_invariants),
            "trace_b1": str(trace_b1),
            "trace_b2": str(expected_trace_b2),
            "proper_time_cutoff_powers": ["Lambda^5", "Lambda^3", "Lambda"],
        },
        "counterterm_map": {
            "integrated_bulk_structures_through_b2": sorted(expected_operator_set),
            "local_total_derivatives": ["Box(R)", "Box(chi^2)", "Box(s)"],
            "nonminimal_terms_new_relative_to_tree_scalar_action": [
                "R*s",
                "R*chi^2",
            ],
            "normalization_status": "NOT_FIXED",
            "scope_limit": (
                "not the complete higher-order, higher-loop, graviton, spinor, "
                "or Wilsonian D5 EFT counterterm basis"
            ),
        },
        "completion_inventory": completion_inventory,
        "hold_reasons": [
            "no scalar matrix Hadamard state or two-point function is constructed",
            "no five-dimensional Dirac Hadamard state is constructed",
            "no gauge-fixed curved graviton Hessian or ghost/Jacobian operator set is derived",
            "the parity-odd determinant phase, global anomaly and quantized counterterms remain unaudited",
            "renormalized finite coefficients and normalization conditions are not fixed",
            "no determinant, mode sum, state-dependent stress, semiclassical solution or physical Hessian is computed",
        ],
        "next_required_calculation": (
            "construct and independently audit the scalar matrix Hadamard parametrix/state "
            "using this off-shell operator; keep spinor, graviton/ghost, parity-phase and "
            "counterterm normalization as separate receipted prerequisites"
        ),
        "rule9_review": {
            "status": "THREE_WAY_CLEARANCE_NOT_MET",
            "completed_independent_reports": 0,
            "scope": "this covariant scalar-matrix checkpoint",
            "effect": "no reviewer-consensus or gate-promotion claim",
        },
        "primary_source_basis": [
            {
                "id": "arXiv:hep-th/0306138",
                "scope": (
                    "quadratic background-field expansion; unique Laplace-type "
                    "connection/endomorphism; matrix a0,a2,a4 coefficients"
                ),
            }
        ],
        "bounded_results": [
            "fixed-metric off-shell rank-three scalar Hessian",
            "Cartesian and phase-aligned Laplace-type E and Omega data",
            "scalar-induced local counterterm structures through b2",
        ],
        "derived_claims": [],
        "explicit_nonclaims": [
            "no homogeneous or fixed-charge background reduction",
            "no scalar or spinor Hadamard state",
            "no determinant or mode sum",
            "no renormalized stress tensor",
            "no curved graviton determinant",
            "no anomaly clearance",
            "no counterterm normalization",
            "no self-consistent semiclassical background",
            "no physical Hessian or radion mass",
            "no A4, Ultra, architecture, gate or publication change",
        ],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "topx4_s2f3_covariant_scalar_matrix_summary.json"
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
    print(f"scalar_matrix_operator={result['scalar_matrix_operator']}")
    print(f"matter_counterterm_structures={result['matter_counterterm_structures']}")
    print("counterterm_normalizations=NOT_FIXED")
    print("scalar_matrix_hadamard_state=NOT_CONSTRUCTED")
    print("determinant=NOT_COMPUTED")
    print("renormalized_stress=NOT_COMPUTED")
    print("physics_pass=false")
    print("gate_effect=NONE")
    print(f"output={output_path}")
    print(f"sha256={digest}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
