#!/usr/bin/env python3
"""UVIR-003 Stage B: quartic khronon and 2-to-2 readiness audit.

Expands the normalized hypersurface-orthogonal Einstein-aether field through
quartic order on a three-dimensional flat decoupling background.  The script
verifies the previous quadratic and cubic results, checks the independent
one-dimensional quartic reduction, and evaluates contact plus resolvable
exchange contributions for representative centre-of-mass kinematics.

The centre-of-mass s-channel carries zero spatial momentum.  Because the flat
khronon inverse propagator is proportional to |q|^2, that channel lies on the
homogeneous gauge orbit and cannot be inverted in this decoupling description.
The reported t/u-plus-contact values are therefore readiness diagnostics, not
a physical scattering amplitude or strong-coupling scale.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Callable

import sympy as sp

from uvir003_aether_stueckelberg_3d_cubic import representative_inputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=base / "outputs",
        help="Directory for the JSON summary.",
    )
    parser.add_argument(
        "--frw-summary",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_summary.json",
        help="Verified representative FRW summary.",
    )
    parser.add_argument(
        "--frw-trajectory",
        type=Path,
        default=base / "outputs" / "uvir003_frw_background_trajectory.csv",
        help="Verified representative FRW trajectory.",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def require_zero(name: str, expression: sp.Expr) -> None:
    result = sp.factor(sp.expand(expression))
    if result != 0:
        raise AssertionError(f"{name} failed: {result}")


def truncate(expression: sp.Expr, epsilon: sp.Symbol, order: int) -> sp.Expr:
    return sp.series(expression, epsilon, 0, order + 1).removeO().expand()


def jet_symbols() -> dict[str, object]:
    pi_t, pi_tt = sp.symbols("pi_t pi_tt", real=True)
    p = sp.Matrix(sp.symbols("p_1:4", real=True))
    v = sp.Matrix(sp.symbols("v_1:4", real=True))
    h11, h22, h33, h12, h13, h23 = sp.symbols(
        "H_11 H_22 H_33 H_12 H_13 H_23",
        real=True,
    )
    hessian = sp.Matrix(
        [
            [h11, h12, h13],
            [h12, h22, h23],
            [h13, h23, h33],
        ]
    )
    return {
        "pi_t": pi_t,
        "pi_tt": pi_tt,
        "p": p,
        "v": v,
        "hessian": hessian,
        "hessian_components": (h11, h22, h33, h12, h13, h23),
    }


def normalized_aether_series(
    epsilon: sp.Symbol,
    jets: dict[str, object],
) -> tuple[sp.Matrix, sp.Matrix]:
    pi_t = jets["pi_t"]
    pi_tt = jets["pi_tt"]
    p = jets["p"]
    v = jets["v"]
    hessian = jets["hessian"]
    p_squared = (p.T * p)[0]

    inverse_norm = truncate(
        (
            1
            + 2 * epsilon * pi_t
            + epsilon**2 * (pi_t**2 - p_squared)
        )
        ** -sp.Rational(1, 2),
        epsilon,
        3,
    )
    u_contravariant = sp.Matrix(
        [truncate((1 + epsilon * pi_t) * inverse_norm, epsilon, 3)]
        + [
            truncate(-epsilon * p[index] * inverse_norm, epsilon, 3)
            for index in range(3)
        ]
    )

    def time_derivative(expression: sp.Expr) -> sp.Expr:
        result = sp.diff(expression, pi_t) * pi_tt
        for index in range(3):
            result += sp.diff(expression, p[index]) * v[index]
        return sp.expand(result)

    def spatial_derivative(expression: sp.Expr, direction: int) -> sp.Expr:
        result = sp.diff(expression, pi_t) * v[direction]
        for index in range(3):
            result += (
                sp.diff(expression, p[index])
                * hessian[direction, index]
            )
        return sp.expand(result)

    d_u = sp.zeros(4, 4)
    for component in range(4):
        d_u[0, component] = time_derivative(u_contravariant[component])
        for direction in range(3):
            d_u[direction + 1, component] = spatial_derivative(
                u_contravariant[component],
                direction,
            )
    return u_contravariant, d_u


def aether_lagrangian(
    epsilon: sp.Symbol,
    u_contravariant: sp.Matrix,
    d_u: sp.Matrix,
    couplings: tuple[sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Expr:
    c1, c2, c3, c4 = couplings
    metric = sp.diag(-1, 1, 1, 1)
    invariant_1 = sp.expand(
        sum(
            metric[a, a] * metric[m, m] * d_u[a, m] ** 2
            for a in range(4)
            for m in range(4)
        )
    )
    divergence = sum(d_u[index, index] for index in range(4))
    invariant_2 = sp.expand(divergence**2)
    invariant_3 = sp.expand(
        sum(d_u[a, b] * d_u[b, a] for a in range(4) for b in range(4))
    )
    invariant_4 = sp.expand(
        sum(
            u_contravariant[a]
            * u_contravariant[b]
            * metric[m, m]
            * d_u[a, m]
            * d_u[b, m]
            for a in range(4)
            for b in range(4)
            for m in range(4)
        )
    )
    return sp.expand(
        -sp.Rational(1, 2)
        * (
            c1 * invariant_1
            + c2 * invariant_2
            + c3 * invariant_3
            - c4 * invariant_4
        )
    )


def one_dimensional_quartic(
    epsilon: sp.Symbol,
    couplings: tuple[sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol],
) -> tuple[sp.Expr, dict[str, sp.Symbol]]:
    c1, c2, c3, c4 = couplings
    pi_t, pi_tt, p, v, h = sp.symbols(
        "pi_t pi_tt p_1 v_1 H_11",
        real=True,
    )
    inverse_norm = truncate(
        (
            1
            + 2 * epsilon * pi_t
            + epsilon**2 * (pi_t**2 - p**2)
        )
        ** -sp.Rational(1, 2),
        epsilon,
        3,
    )
    u = sp.Matrix(
        [
            truncate((1 + epsilon * pi_t) * inverse_norm, epsilon, 3),
            truncate(-epsilon * p * inverse_norm, epsilon, 3),
        ]
    )

    def dt(expression: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(expression, pi_t) * pi_tt
            + sp.diff(expression, p) * v
        )

    def dx(expression: sp.Expr) -> sp.Expr:
        return sp.expand(
            sp.diff(expression, pi_t) * v
            + sp.diff(expression, p) * h
        )

    d_u = sp.Matrix([[dt(u[0]), dt(u[1])], [dx(u[0]), dx(u[1])]])
    metric = sp.diag(-1, 1)
    invariant_1 = sp.expand(
        sum(
            metric[a, a] * metric[m, m] * d_u[a, m] ** 2
            for a in range(2)
            for m in range(2)
        )
    )
    divergence = d_u[0, 0] + d_u[1, 1]
    invariant_2 = sp.expand(divergence**2)
    invariant_3 = sp.expand(
        sum(d_u[a, b] * d_u[b, a] for a in range(2) for b in range(2))
    )
    invariant_4 = sp.expand(
        sum(
            u[a]
            * u[b]
            * metric[m, m]
            * d_u[a, m]
            * d_u[b, m]
            for a in range(2)
            for b in range(2)
            for m in range(2)
        )
    )
    lagrangian = sp.expand(
        -sp.Rational(1, 2)
        * (
            c1 * invariant_1
            + c2 * invariant_2
            + c3 * invariant_3
            - c4 * invariant_4
        )
    )
    return sp.expand(lagrangian).coeff(epsilon, 4), {
        "pi_t": pi_t,
        "pi_tt": pi_tt,
        "p": p,
        "v": v,
        "h": h,
    }


def symbolic_quartic_vertex() -> dict[str, object]:
    epsilon = sp.symbols("epsilon", real=True)
    c1, c2, c3, c4 = sp.symbols("c_1 c_2 c_3 c_4", real=True)
    couplings = (c1, c2, c3, c4)
    jets = jet_symbols()
    pi_t = jets["pi_t"]
    pi_tt = jets["pi_tt"]
    p = jets["p"]
    v = jets["v"]
    hessian = jets["hessian"]

    u, d_u = normalized_aether_series(epsilon, jets)
    lagrangian = aether_lagrangian(epsilon, u, d_u, couplings)
    quadratic = sp.expand(lagrangian).coeff(epsilon, 2)
    cubic = sp.expand(lagrangian).coeff(epsilon, 3)
    quartic = sp.expand(lagrangian).coeff(epsilon, 4)

    p_squared = (p.T * p)[0]
    v_squared = (v.T * v)[0]
    hessian_squared = sp.trace(hessian.T * hessian)
    hessian_trace = sp.trace(hessian)
    p_dot_v = (p.T * v)[0]
    p_hessian_v = (p.T * hessian * v)[0]
    c14 = c1 + c4
    expected_quadratic = sp.expand(
        (
            c14 * v_squared
            - (c1 + c3) * hessian_squared
            - c2 * hessian_trace**2
        )
        / 2
    )
    expected_cubic = sp.expand(
        -c14 * (pi_tt * p_dot_v + pi_t * v_squared)
        + (c1 + 2 * c3 - c4) * p_hessian_v
        + 2 * c2 * hessian_trace * p_dot_v
        + (c1 + c3) * pi_t * hessian_squared
        + c2 * pi_t * hessian_trace**2
    )
    require_zero("quadratic regression", quadratic - expected_quadratic)
    require_zero("cubic regression", cubic - expected_cubic)

    h11, h22, h33, h12, h13, h23 = jets["hessian_components"]
    replacements = {
        p[1]: 0,
        p[2]: 0,
        v[1]: 0,
        v[2]: 0,
        h22: 0,
        h33: 0,
        h12: 0,
        h13: 0,
        h23: 0,
    }
    collinear_quartic = sp.expand(quartic.subs(replacements))
    independent_1d, one_d_symbols = one_dimensional_quartic(
        epsilon,
        couplings,
    )
    one_d_substitution = {
        one_d_symbols["pi_t"]: pi_t,
        one_d_symbols["pi_tt"]: pi_tt,
        one_d_symbols["p"]: p[0],
        one_d_symbols["v"]: v[0],
        one_d_symbols["h"]: h11,
    }
    require_zero(
        "independent one-dimensional quartic reduction",
        collinear_quartic - independent_1d.subs(one_d_substitution),
    )

    polynomial_variables = (
        pi_t,
        pi_tt,
        *tuple(p),
        *tuple(v),
        *jets["hessian_components"],
    )
    quartic_terms = len(sp.Poly(quartic, *polynomial_variables).terms())
    require("nonempty quartic vertex", quartic_terms > 0)
    return {
        "couplings": couplings,
        "jets": jets,
        "quadratic": expected_quadratic,
        "cubic": expected_cubic,
        "quartic": quartic,
        "collinear_quartic": collinear_quartic,
        "quartic_expanded_term_count": quartic_terms,
    }


def symbolic_mode_jet(
    omega: sp.Expr,
    wavevector: tuple[sp.Expr, sp.Expr, sp.Expr],
) -> tuple[sp.Expr, ...]:
    kx, ky, kz = wavevector
    return (
        -sp.I * omega,
        -(omega**2),
        sp.I * kx,
        sp.I * ky,
        sp.I * kz,
        omega * kx,
        omega * ky,
        omega * kz,
        -(kx * kx),
        -(ky * ky),
        -(kz * kz),
        -(kx * ky),
        -(kx * kz),
        -(ky * kz),
    )


def symbolic_polarized_coefficient(
    expression: sp.Expr,
    variables: tuple[sp.Symbol, ...],
    modes: list[tuple[sp.Expr, tuple[sp.Expr, sp.Expr, sp.Expr]]],
) -> sp.Expr:
    mode_values = [
        symbolic_mode_jet(omega, wavevector)
        for omega, wavevector in modes
    ]
    result = 0
    count = len(modes)
    for subset_size in range(count + 1):
        sign = -1 if (count - subset_size) % 2 else 1
        for indices in itertools.combinations(range(count), subset_size):
            summed = tuple(
                sum(mode_values[index][slot] for index in indices)
                for slot in range(14)
            )
            result += sign * expression.subs(dict(zip(variables, summed)))
    return sp.factor(sp.expand(result))


def elastic_static_exchange_identity(
    symbolic: dict[str, object],
) -> dict[str, str]:
    jets = symbolic["jets"]
    variables = (
        jets["pi_t"],
        jets["pi_tt"],
        *tuple(jets["p"]),
        *tuple(jets["v"]),
        *jets["hessian_components"],
    )
    omega, x, y = sp.symbols("omega x y", real=True)
    incoming = (omega, (sp.Integer(0), sp.Integer(0), sp.Integer(1)))
    outgoing_as_incoming = (-omega, (-y, sp.Integer(0), -x))
    static_transfer = (
        sp.Integer(0),
        (y, sp.Integer(0), x - 1),
    )
    vertex = symbolic_polarized_coefficient(
        symbolic["cubic"],
        variables,
        [incoming, outgoing_as_incoming, static_transfer],
    )
    angle_identity = x**2 + y**2 - 1
    remainder = sp.rem(
        sp.Poly(vertex, y),
        sp.Poly(angle_identity, y),
    ).as_expr()
    require_zero("elastic static-transfer cubic vertex", remainder)
    quotient = sp.factor(sp.cancel(vertex / angle_identity))
    return {
        "vertex_factorization": str(vertex),
        "angular_identity": "x^2+y^2=1",
        "quotient": str(quotient),
        "consequence": (
            "elastic COM t/u cubic exchange vertices vanish exactly"
        ),
    }
def elastic_contact_identity(
    symbolic: dict[str, object],
) -> dict[str, str]:
    jets = symbolic["jets"]
    variables = (
        jets["pi_t"],
        jets["pi_tt"],
        *tuple(jets["p"]),
        *tuple(jets["v"]),
        *jets["hessian_components"],
    )
    omega, x, y = sp.symbols("omega x y", real=True)
    modes = [
        (omega, (sp.Integer(0), sp.Integer(0), sp.Integer(1))),
        (omega, (sp.Integer(0), sp.Integer(0), -sp.Integer(1))),
        (-omega, (-y, sp.Integer(0), -x)),
        (-omega, (y, sp.Integer(0), x)),
    ]
    contact = symbolic_polarized_coefficient(
        symbolic["quartic"],
        variables,
        modes,
    )
    angle_reduced = sp.rem(
        sp.Poly(sp.expand(contact), y),
        sp.Poly(y**2 - (1 - x**2), y),
    ).as_expr()
    c1, c2, c3, c4 = symbolic["couplings"]
    c123 = c1 + c2 + c3
    c14 = c1 + c4
    on_shell = sp.factor(
        sp.together(angle_reduced.subs(omega**2, c123 / c14))
    )
    expected = sp.factor(
        4 * (c123**2 / c14 - (2 * c123 - c14) * x**2)
    )
    require_zero("elastic quartic contact angular form", on_shell - expected)
    angular_average = sp.factor(
        sp.integrate(expected, (x, -1, 1)) / 2
    )
    return {
        "unit_momentum_contact": str(expected),
        "angular_average": str(angular_average),
        "scope": (
            "contact term only; not the complete gauge-regular amplitude"
        ),
    }
def quartic_constraint_identity() -> dict[str, str]:
    c, j2, z2 = sp.symbols("C J_2 z_2", nonzero=True)
    quartic_constraint_terms = c * z2**2 / 2 + j2 * z2
    reduced = sp.expand(quartic_constraint_terms.subs(z2, -j2 / c))
    require_zero(
        "quartic second-order constraint Schur complement",
        reduced + j2**2 / (2 * c),
    )
    return {
        "second_order_solution": "z2=-C^{-1}J2",
        "reduced_quartic_action": (
            "L_reduced^(4)=L4[x,z1]-J2^T*C^{-1}*J2/2"
        ),
        "third_order_solution": "not required at quartic order",
        "scope": (
            "algebraic constraints with an invertible quadratic constraint matrix"
        ),
    }
def evaluator(
    expression: sp.Expr,
    couplings: tuple[sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol],
    jets: dict[str, object],
    values: dict[str, float],
) -> tuple[Callable[..., complex], tuple[sp.Symbol, ...]]:
    variables = (
        jets["pi_t"],
        jets["pi_tt"],
        *tuple(jets["p"]),
        *tuple(jets["v"]),
        *jets["hessian_components"],
    )
    substituted = expression.subs(
        {
            couplings[0]: values["c1"],
            couplings[1]: values["c2"],
            couplings[2]: values["c3"],
            couplings[3]: values["c4"],
        }
    )
    return sp.lambdify(variables, substituted, modules="math"), variables


def mode_jet(omega: float, wavevector: tuple[float, float, float]) -> tuple[complex, ...]:
    kx, ky, kz = wavevector
    p = (1j * kx, 1j * ky, 1j * kz)
    v = (omega * kx, omega * ky, omega * kz)
    hessian = (
        -(kx * kx),
        -(ky * ky),
        -(kz * kz),
        -(kx * ky),
        -(kx * kz),
        -(ky * kz),
    )
    return (-1j * omega, -(omega**2), *p, *v, *hessian)


def add_jets(jets: list[tuple[complex, ...]]) -> tuple[complex, ...]:
    if not jets:
        return (0j,) * 14
    return tuple(sum(values) for values in zip(*jets, strict=True))


def polarized_coefficient(
    function: Callable[..., complex],
    modes: list[tuple[float, tuple[float, float, float]]],
) -> complex:
    mode_values = [mode_jet(omega, wavevector) for omega, wavevector in modes]
    result = 0j
    count = len(mode_values)
    for subset_size in range(count + 1):
        sign = -1 if (count - subset_size) % 2 else 1
        for indices in itertools.combinations(range(count), subset_size):
            summed = add_jets([mode_values[index] for index in indices])
            result += sign * complex(function(*summed))
    return result


def negate_mode(
    mode: tuple[float, tuple[float, float, float]],
) -> tuple[float, tuple[float, float, float]]:
    omega, wavevector = mode
    return -omega, tuple(-component for component in wavevector)


def add_modes(
    first: tuple[float, tuple[float, float, float]],
    second: tuple[float, tuple[float, float, float]],
) -> tuple[float, tuple[float, float, float]]:
    return (
        first[0] + second[0],
        tuple(
            first[1][index] + second[1][index]
            for index in range(3)
        ),
    )


def inverse_kernel(
    mode: tuple[float, tuple[float, float, float]],
    values: dict[str, float],
) -> float:
    omega, wavevector = mode
    k_squared = sum(component**2 for component in wavevector)
    return k_squared * (
        values["c14"] * omega**2 - values["c123"] * k_squared
    )


def scattering_readiness(
    symbolic: dict[str, object],
    values: dict[str, float],
    exchange_identity: dict[str, str],
    contact_identity: dict[str, str],
) -> dict[str, object]:
    cubic_function, _ = evaluator(
        symbolic["cubic"],
        symbolic["couplings"],
        symbolic["jets"],
        values,
    )
    quartic_function, _ = evaluator(
        symbolic["quartic"],
        symbolic["couplings"],
        symbolic["jets"],
        values,
    )
    sound_speed = math.sqrt(values["c123"] / values["c14"])
    momentum = 1.0
    energy = sound_speed * momentum
    angles = (30.0, 60.0, 90.0, 120.0, 150.0)
    samples: list[dict[str, object]] = []
    zero_tolerance = 1e-12

    for angle_degrees in angles:
        angle = math.radians(angle_degrees)
        outgoing = (
            momentum * math.sin(angle),
            0.0,
            momentum * math.cos(angle),
        )
        modes = [
            (energy, (0.0, 0.0, momentum)),
            (energy, (0.0, 0.0, -momentum)),
            (-energy, tuple(-component for component in outgoing)),
            (-energy, outgoing),
        ]
        contact = polarized_coefficient(quartic_function, modes)
        require(
            f"real contact at {angle_degrees} degrees",
            abs(contact.imag) < 1e-9,
        )
        expected_contact = 4 * (
            values["c123"] ** 2 / values["c14"]
            - (2 * values["c123"] - values["c14"])
            * math.cos(angle) ** 2
        )
        require(
            f"contact angular identity at {angle_degrees} degrees",
            abs(contact.real - expected_contact) < 1e-9,
        )
        channels: dict[str, object] = {}
        exchange_sum = 0j
        partitions = {
            "s": ((0, 1), (2, 3)),
            "t": ((0, 2), (1, 3)),
            "u": ((0, 3), (1, 2)),
        }
        for name, (left, right) in partitions.items():
            internal = negate_mode(add_modes(modes[left[0]], modes[left[1]]))
            internal_k_squared = sum(
                component**2 for component in internal[1]
            )
            kernel = inverse_kernel(internal, values)
            if internal_k_squared < zero_tolerance:
                channels[name] = {
                    "status": "HOMOGENEOUS_GAUGE_MODE_NOT_INVERTIBLE",
                    "internal_omega": internal[0],
                    "internal_k_squared": internal_k_squared,
                    "inverse_kernel": kernel,
                }
                continue
            left_vertex = polarized_coefficient(
                cubic_function,
                [modes[left[0]], modes[left[1]], internal],
            )
            right_internal = negate_mode(internal)
            right_vertex = polarized_coefficient(
                cubic_function,
                [modes[right[0]], modes[right[1]], right_internal],
            )
            exchange = -(left_vertex * right_vertex) / kernel
            require(
                f"real {name}-exchange at {angle_degrees} degrees",
                abs(exchange.imag) < 1e-8,
            )
            require(
                f"vanishing {name}-exchange at {angle_degrees} degrees",
                abs(exchange.real) < 1e-8,
            )
            channels[name] = {
                "status": "VANISHES_EXACTLY_IN_ELASTIC_COM",
                "internal_omega": internal[0],
                "internal_k_squared": internal_k_squared,
                "inverse_kernel": kernel,
                "left_vertex": {
                    "real": left_vertex.real,
                    "imaginary": left_vertex.imag,
                },
                "right_vertex": {
                    "real": right_vertex.real,
                    "imaginary": right_vertex.imag,
                },
                "exchange_contribution": 0.0,
            }

        partial = contact + exchange_sum
        canonical_partial = partial / (
            values["M_U"] ** 2 * values["c14"] ** 2 * momentum**4
        )
        samples.append(
            {
                "angle_degrees": angle_degrees,
                "contact_coefficient": contact.real,
                "resolved_exchange_sum": exchange_sum.real,
                "contact_plus_resolved_exchange": partial.real,
                "canonical_partial_amplitude_at_k_equals_1": (
                    canonical_partial.real
                ),
                "channels": channels,
                "status": "INCOMPLETE_S_CHANNEL_GAUGE_OBSTRUCTION",
            }
        )

    require(
        "s-channel obstruction present in every COM sample",
        all(
            sample["channels"]["s"]["status"]
            == "HOMOGENEOUS_GAUGE_MODE_NOT_INVERTIBLE"
            for sample in samples
        ),
    )
    return {
        "kinematics": "CENTRE_OF_MASS_ALL_INCOMING",
        "external_momentum": momentum,
        "external_energy": energy,
        "sound_speed": sound_speed,
        "static_exchange_identity": exchange_identity,
        "contact_identity": contact_identity,
        "samples": samples,
        "status": "PARTIAL_ONLY_S_CHANNEL_GAUGE_OBSTRUCTION",
        "physical_interpretation": (
            "The flat-decoupling contact term is reproducible and elastic "
            "t/u cubic exchange vanishes exactly, but the COM s-channel probes "
            "the homogeneous khronon gauge orbit. The full constrained "
            "cosmological scalar system is required before an invariant "
            "2-to-2 amplitude or cutoff can be assigned."
        ),
    }


def build_summary(
    symbolic: dict[str, object],
    values: dict[str, float],
    scattering: dict[str, object],
    exchange_identity: dict[str, str],
    contact_identity: dict[str, str],
    constraint_identity: dict[str, str],
) -> dict[str, object]:
    return {
        "stage": "B_AETHER_STUECKELBERG_3D_QUARTIC",
        "calculation_status": "PASS_QUARTIC_BASIS_WITH_2_TO_2_GAUGE_HOLD",
        "scope": {
            "geometry": "FLAT_METRIC_DECOUPLING_LIMIT",
            "spatial_dimension": 3,
            "aether": "HYPERSURFACE_ORTHOGONAL",
            "order": "QUARTIC_IN_PI",
        },
        "symbolic_result": {
            "overall_factor": "M_U^2",
            "quartic_lagrangian": str(symbolic["quartic"]),
            "collinear_quartic_lagrangian": str(
                symbolic["collinear_quartic"]
            ),
            "expanded_term_count": symbolic["quartic_expanded_term_count"],
            "quadratic_regression": "PASS",
            "cubic_regression": "PASS",
            "independent_one_dimensional_reduction": "PASS",
            "elastic_static_exchange_identity": exchange_identity,
            "elastic_contact_identity": contact_identity,
        },
        "constraint_elimination": constraint_identity,
        "representative_branch": {
            "parameters": values,
            "scattering_readiness": scattering,
        },
        "interpretation": {
            "quartic_contact_basis_status": "DERIVED_AND_VERIFIED",
            "elastic_com_t_u_exchange_status": "VANISHES_EXACTLY",
            "s_channel_status": "HOMOGENEOUS_GAUGE_MODE_NOT_INVERTIBLE",
            "complete_2_to_2_amplitude_status": "NOT_YET_DERIVED",
            "physical_strong_coupling_scale_status": "NOT_YET_DERIVED",
            "quartic_constraint_order": (
                "SECOND_ORDER_CONSTRAINT_SOURCE_REQUIRED"
            ),
            "next_required_calculation": [
                "FULL_COSMOLOGICAL_CUBIC_VERTEX_ON_FIRST_ORDER_CONSTRAINTS",
                "FULL_COSMOLOGICAL_QUARTIC_VERTEX_WITH_SECOND_ORDER_CONSTRAINT_SCHUR_COMPLEMENT",
                "PHYSICAL_SCALAR_EIGENMODE_PROJECTION",
                "GAUGE_REGULAR_COMPLETE_2_TO_2_AMPLITUDE",
                "PARTIAL_WAVE_UNITARITY_CRITERION",
            ],
        },
        "gate_status": {
            "UVIR-003": "IN_PROGRESS",
            "MAT-001": "BLOCKED",
        },
    }


def main() -> None:
    args = parse_args()
    symbolic = symbolic_quartic_vertex()
    exchange_identity = elastic_static_exchange_identity(symbolic)
    contact_identity = elastic_contact_identity(symbolic)
    constraint_identity = quartic_constraint_identity()
    values, _ = representative_inputs(
        args.frw_summary,
        args.frw_trajectory,
    )
    scattering = scattering_readiness(
        symbolic,
        values,
        exchange_identity,
        contact_identity,
    )
    summary = build_summary(
        symbolic,
        values,
        scattering,
        exchange_identity,
        contact_identity,
        constraint_identity,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = (
        args.output_dir / "uvir003_aether_stueckelberg_3d_quartic_summary.json"
    )
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("UVIR-003 three-dimensional khronon quartic basis: VERIFIED")
    print(
        "Expanded quartic monomials: "
        f"{symbolic['quartic_expanded_term_count']}"
    )
    print("Independent one-dimensional reduction: VERIFIED")
    print("Elastic COM quartic contact angular form: VERIFIED")
    print("Elastic COM t/u cubic exchange: VANISHES_EXACTLY")
    print("Quartic second-order constraint Schur complement: VERIFIED")
    print("COM s-channel: HOMOGENEOUS_GAUGE_MODE_NOT_INVERTIBLE")
    print("Complete physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("Physical strong-coupling scale: NOT_YET_DERIVED")
    print("Full UVIR-003 gate: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_QUARTIC_BASIS_WITH_2_TO_2_GAUGE_HOLD")


if __name__ == "__main__":
    main()
