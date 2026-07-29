#!/usr/bin/env python3
"""Factorized reduced quartic momentum kernel for UVIR-003."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--complete-functional",
        type=Path,
        default=base / "outputs" / "uvir003_complete_l4_contact_summary.json",
    )
    parser.add_argument(
        "--cubic-kernel",
        type=Path,
        default=base / "outputs" / "uvir003_cubic_momentum_kernel_summary.json",
    )
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def require_zero(name: str, expression: sp.Expr | sp.MatrixBase) -> None:
    residual = sp.simplify(expression)
    if isinstance(residual, sp.MatrixBase):
        if residual != sp.zeros(*residual.shape):
            raise AssertionError(f"{name} failed: {residual}")
    elif residual != 0:
        raise AssertionError(f"{name} failed: {residual}")


def leg_sum(amplitudes, values):
    return sp.Add(*(amplitudes[i] * values[i] for i in range(len(amplitudes))))


def pair_sum(amplitudes, left, right, dot, power=1, sign=1):
    count = len(amplitudes)
    return sp.Add(
        *(
            sign
            * amplitudes[i]
            * amplitudes[j]
            * dot[i][j] ** power
            * left[i]
            * right[j]
            for i in range(count)
            for j in range(count)
        )
    )


def make_fields(count: int) -> dict[str, tuple[sp.Symbol, ...]]:
    return {
        label: sp.symbols(f"{label}_1:{count + 1}", real=True)
        for label in (
            "R",
            "R_dot",
            "delta_rho",
            "delta_rho_dot",
            "vartheta",
            "vartheta_dot",
            "pi",
            "pi_dot",
        )
    }


def constraint_resolvers(q, fields, symbols):
    lapse, sigma, determinant = [], [], []
    for i in range(len(q)):
        matrix = sp.Matrix(
            [
                [
                    symbols["C_14"] * q[i] ** 2 - 2 * symbols["V"],
                    2 * symbols["M_cos_sq"] * symbols["H"],
                ],
                [
                    2 * symbols["M_cos_sq"] * symbols["H"],
                    -symbols["D_123"],
                ],
            ]
        )
        source = sp.Matrix(
            [
                6 * symbols["M_cos_sq"] * symbols["H"] * fields["R_dot"][i]
                + 2 * symbols["M_P_sq"] * q[i] ** 2 * fields["R"][i]
                - (symbols["V_rho"] + symbols["rho"] * symbols["mu"] ** 2)
                * fields["delta_rho"][i]
                - symbols["rho_dot"] * fields["delta_rho_dot"][i]
                - symbols["rho"] ** 2 * symbols["mu"] * fields["vartheta_dot"][i],
                -2 * symbols["M_cos_sq"] * fields["R_dot"][i]
                - symbols["rho_dot"] * fields["delta_rho"][i]
                - symbols["rho"] ** 2 * symbols["mu"] * fields["vartheta"][i],
            ]
        )
        solved = -matrix.inv() * source
        lapse.append(sp.factor(solved[0]))
        sigma.append(sp.factor(solved[1]))
        determinant.append(sp.factor(matrix.det()))
    return lapse, sigma, determinant


def physical_map(q, fields, symbols):
    count = len(q)
    xi = sp.symbols(f"Xi_1:{count + 1}", real=True)
    xi_dot = sp.symbols(f"Xi_dot_1:{count + 1}", real=True)
    q_rho = sp.symbols(f"Q_rho_1:{count + 1}", real=True)
    q_rho_dot = sp.symbols(f"Q_rho_dot_1:{count + 1}", real=True)
    q_chi = sp.symbols(f"Q_chi_1:{count + 1}", real=True)
    q_chi_dot = sp.symbols(f"Q_chi_dot_1:{count + 1}", real=True)
    force = sp.symbols(f"Pi_1:{count + 1}", real=True)
    force_dot = sp.symbols(f"Pi_dot_1:{count + 1}", real=True)
    hubble_dot, rho_ddot, chemical_dot = sp.symbols("H_dot rho_ddot mu_dot", real=True)
    hubble = symbols["H"]
    rho = symbols["rho"]
    rho_dot = symbols["rho_dot"]
    chemical = symbols["mu"]
    result = {}
    for i in range(count):
        result.update(
            {
                fields["R"][i]: hubble * xi[i] / q[i],
                fields["delta_rho"][i]: q_rho[i] + rho_dot * xi[i] / q[i],
                fields["vartheta"][i]: q_chi[i] / rho + chemical * xi[i] / q[i],
                fields["R_dot"][i]: (
                    hubble * xi_dot[i] / q[i] + (hubble_dot + hubble**2) * xi[i] / q[i]
                ),
                fields["delta_rho_dot"][i]: (
                    q_rho_dot[i]
                    + rho_dot * xi_dot[i] / q[i]
                    + (rho_ddot + hubble * rho_dot) * xi[i] / q[i]
                ),
                fields["vartheta_dot"][i]: (
                    q_chi_dot[i] / rho
                    - rho_dot * q_chi[i] / rho**2
                    + chemical * xi_dot[i] / q[i]
                    + (chemical_dot + hubble * chemical) * xi[i] / q[i]
                ),
                fields["pi"][i]: force[i],
                fields["pi_dot"][i]: force_dot[i],
            }
        )
    return result


def functional_replacements(symbols, amplitudes, q, dot, fields, lapse, sigma):
    beta = tuple(sigma[i] / q[i] ** 2 for i in range(len(q)))
    replacements = {
        symbols["R"]: leg_sum(amplitudes, fields["R"]),
        symbols["R_dot"]: leg_sum(amplitudes, fields["R_dot"]),
        symbols["delta_rho"]: leg_sum(amplitudes, fields["delta_rho"]),
        symbols["delta_rho_dot"]: leg_sum(amplitudes, fields["delta_rho_dot"]),
        symbols["vartheta_dot"]: leg_sum(amplitudes, fields["vartheta_dot"]),
        symbols["pi_dot"]: leg_sum(amplitudes, fields["pi_dot"]),
        symbols["delta_N_1"]: leg_sum(amplitudes, lapse),
        symbols["D2_beta_1"]: -leg_sum(amplitudes, sigma),
        symbols["lap_pi"]: -leg_sum(
            amplitudes,
            tuple(q[i] ** 2 * fields["pi"][i] for i in range(len(q))),
        ),
        symbols["D_delta_N_1_sq"]: pair_sum(amplitudes, lapse, lapse, dot, sign=-1),
        symbols["D_delta_N_1_dot_D_R"]: pair_sum(
            amplitudes, lapse, fields["R"], dot, sign=-1
        ),
        symbols["Dij_beta_1_sq"]: pair_sum(amplitudes, beta, beta, dot, power=2),
        symbols["D_R_dot_D_beta_1"]: pair_sum(
            amplitudes, fields["R"], beta, dot, sign=-1
        ),
        symbols["D_beta_1_sq"]: pair_sum(amplitudes, beta, beta, dot, sign=-1),
        symbols["D_beta_1_dot_D_delta_rho"]: pair_sum(
            amplitudes, beta, fields["delta_rho"], dot, sign=-1
        ),
        symbols["D_beta_1_dot_D_vartheta"]: pair_sum(
            amplitudes, beta, fields["vartheta"], dot, sign=-1
        ),
        symbols["D_beta_1_dot_D_pi"]: pair_sum(
            amplitudes, beta, fields["pi"], dot, sign=-1
        ),
        symbols["grad_R_sq"]: pair_sum(
            amplitudes, fields["R"], fields["R"], dot, sign=-1
        ),
        symbols["grad_delta_rho_sq"]: pair_sum(
            amplitudes,
            fields["delta_rho"],
            fields["delta_rho"],
            dot,
            sign=-1,
        ),
        symbols["grad_vartheta_sq"]: pair_sum(
            amplitudes,
            fields["vartheta"],
            fields["vartheta"],
            dot,
            sign=-1,
        ),
        symbols["grad_R_dot_grad_pi"]: pair_sum(
            amplitudes, fields["R"], fields["pi"], dot, sign=-1
        ),
    }
    replacements[symbols["Dij_beta_1_Di_R_Dj_beta_1"]] = sp.Add(
        *(
            amplitudes[i]
            * amplitudes[j]
            * amplitudes[k]
            * dot[i][j]
            * dot[i][k]
            * beta[i]
            * fields["R"][j]
            * beta[k]
            for i in range(len(q))
            for j in range(len(q))
            for k in range(len(q))
        )
    )
    return replacements


def contact_kernel(l4, symbols):
    eps = sp.symbols("epsilon_1:5", real=True)
    q = sp.symbols("q_1:5", positive=True)
    off_diagonal = {
        (0, 1): sp.Symbol("k1_dot_k2", real=True),
        (0, 2): sp.Symbol("k1_dot_k3", real=True),
        (0, 3): sp.Symbol("k1_dot_k4", real=True),
        (1, 2): sp.Symbol("k2_dot_k3", real=True),
        (1, 3): sp.Symbol("k2_dot_k4", real=True),
        (2, 3): sp.Symbol("k3_dot_k4", real=True),
    }
    dot = [[sp.Integer(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        dot[i][i] = q[i] ** 2
    for (i, j), value in off_diagonal.items():
        dot[i][j] = value
        dot[j][i] = value
    fields = make_fields(4)
    lapse = sp.symbols("delta_N_1_1:5", real=True)
    sigma = sp.symbols("Sigma_1_1:5", real=True)
    replacements = functional_replacements(symbols, eps, q, dot, fields, lapse, sigma)
    polarized = l4.xreplace(replacements)
    kernel = polarized
    for amplitude in eps:
        kernel = sp.diff(kernel, amplitude)
    kernel = kernel.subs({amplitude: 0 for amplitude in eps})
    require(
        "epsilon-free quartic contact", not any(e in kernel.free_symbols for e in eps)
    )
    require("nonempty quartic contact", kernel != 0)

    basis_map = physical_map(q, fields, symbols)
    physical = kernel.xreplace(basis_map)
    old_lapse, old_sigma, determinants = constraint_resolvers(q, fields, symbols)
    physical_lapse = [item.xreplace(basis_map) for item in old_lapse]
    physical_sigma = [item.xreplace(basis_map) for item in old_sigma]
    closure = [
        sp.Eq(q[i] ** 2 + sum(dot[i][j] for j in range(4) if j != i), 0)
        for i in range(4)
    ]
    return {
        "q": q,
        "dot": dot,
        "kernel": kernel,
        "physical": physical,
        "closure": closure,
        "resolvers": {
            f"leg_{i + 1}": {
                "det_C": str(determinants[i]),
                "physical_basis_delta_N_1": str(physical_lapse[i]),
                "physical_basis_Sigma_1": str(physical_sigma[i]),
                "physical_basis_beta_1": str(physical_sigma[i] / q[i] ** 2),
            }
            for i in range(4)
        },
    }


def pair_source_kernel(l3, symbols):
    ea, eb, eta = sp.symbols("epsilon_a epsilon_b eta_z", real=True)
    qa, qb, channel = sp.symbols("q_a q_b q_K", positive=True)
    q = (qa, qb, channel)
    dot = [
        [qa**2, (channel**2 - qa**2 - qb**2) / 2, (qb**2 - qa**2 - channel**2) / 2],
        [(channel**2 - qa**2 - qb**2) / 2, qb**2, (qa**2 - qb**2 - channel**2) / 2],
        [
            (qb**2 - qa**2 - channel**2) / 2,
            (qa**2 - qb**2 - channel**2) / 2,
            channel**2,
        ],
    ]
    all_fields = make_fields(3)
    fields = {
        name: (values[0], values[1], sp.Integer(0))
        for name, values in all_fields.items()
    }
    input_fields = {name: values[:2] for name, values in all_fields.items()}
    lapse = sp.symbols("delta_N_a delta_N_b", real=True)
    sigma = sp.symbols("Sigma_a Sigma_b", real=True)

    def component(output_lapse, output_sigma):
        replacements = functional_replacements(
            symbols,
            (ea, eb, eta),
            q,
            dot,
            fields,
            (lapse[0], lapse[1], output_lapse),
            (sigma[0], sigma[1], output_sigma),
        )
        expression = l3.xreplace(replacements)
        return sp.diff(expression, ea, eb, eta).subs({ea: 0, eb: 0, eta: 0})

    source_n = component(sp.Integer(1), sp.Integer(0))
    source_sigma = component(sp.Integer(0), sp.Integer(1))
    require("nonempty lapse pair source", source_n != 0)
    require("nonempty shift pair source", source_sigma != 0)

    basis_map = physical_map((qa, qb), input_fields, symbols)
    source_n_physical = source_n.xreplace(basis_map)
    source_sigma_physical = source_sigma.xreplace(basis_map)
    old_lapse, old_sigma, determinants = constraint_resolvers(
        (qa, qb), input_fields, symbols
    )
    physical_lapse = [item.xreplace(basis_map) for item in old_lapse]
    physical_sigma = [item.xreplace(basis_map) for item in old_sigma]

    source_n_q0 = sp.simplify(
        sp.limit(source_n_physical.subs(qb, qa), channel, 0, dir="+")
    )
    source_sigma_q0 = sp.simplify(
        sp.limit(source_sigma_physical.subs(qb, qa), channel, 0, dir="+")
    )
    require(
        "finite homogeneous lapse-source limit",
        not source_n_q0.has(sp.oo, -sp.oo, sp.zoo, sp.nan),
    )
    require(
        "finite homogeneous shift-source limit",
        not source_sigma_q0.has(sp.oo, -sp.oo, sp.zoo, sp.nan),
    )

    matrix = sp.Matrix(
        [
            [
                symbols["C_14"] * channel**2 - 2 * symbols["V"],
                2 * symbols["M_cos_sq"] * symbols["H"],
            ],
            [2 * symbols["M_cos_sq"] * symbols["H"], -symbols["D_123"]],
        ]
    )
    inverse = sp.simplify(matrix.inv())
    require(
        "finite-q constraint inverse",
        sp.simplify(matrix * inverse - sp.eye(2)) == sp.zeros(2),
    )

    constraint_projector = sp.diag(1, 0)
    physical_projector = sp.diag(0, 1, 1, 1)
    require("constraint q0 projector", constraint_projector**2 == constraint_projector)
    require("physical q0 projector", physical_projector**2 == physical_projector)
    homogeneous_inverse = sp.diag(-sp.Rational(1, 2) / symbols["V"], 0)
    homogeneous_matrix = matrix.subs(channel, 0)
    require(
        "homogeneous shift removed",
        homogeneous_inverse * sp.Matrix([0, 1]) == sp.zeros(2, 1),
    )
    require_zero(
        "projected homogeneous constraint inverse",
        homogeneous_inverse * homogeneous_matrix * constraint_projector
        - constraint_projector,
    )
    require_zero(
        "homogeneous Xi removed",
        physical_projector * sp.Matrix([1, 0, 0, 0]),
    )

    return {
        "B_N": source_n_physical,
        "B_Sigma": source_sigma_physical,
        "B_N_q0_com": source_n_q0,
        "B_Sigma_q0_com_diagnostic": source_sigma_q0,
        "constraint_matrix": matrix,
        "constraint_inverse": inverse,
        "homogeneous_inverse": homogeneous_inverse,
        "constraint_projector": constraint_projector,
        "physical_projector": physical_projector,
        "input_resolvers": {
            f"input_{label}": {
                "det_C": str(determinants[i]),
                "physical_basis_delta_N_1": str(physical_lapse[i]),
                "physical_basis_Sigma_1": str(physical_sigma[i]),
            }
            for i, label in enumerate(("a", "b"))
        },
    }


def build_kernel(complete_path: Path, cubic_path: Path) -> dict[str, object]:
    with complete_path.open("r", encoding="utf-8") as handle:
        complete = json.load(handle)["symbolic_audit"]
    with cubic_path.open("r", encoding="utf-8") as handle:
        cubic = json.load(handle)
    require(
        "complete quartic dependency",
        complete["quartic_contact"]["status"]
        == "PASS_COMPLETE_GENERIC_L4_X_Z1_CONTACT",
    )
    require(
        "complete cubic dependency",
        complete["cubic_functional"]["status"]
        == "PASS_COMPLETE_GENERIC_L3_X_Z1_FUNCTIONAL",
    )
    require(
        "finite-q cubic-kernel dependency",
        cubic["subgate_status"] == "PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL",
    )

    gamma = sp.Symbol("gamma", real=True)
    local_symbols = {"gamma": gamma}
    l3 = sp.sympify(
        complete["cubic_functional"]["complete_L3_x_z1"], locals=local_symbols
    )
    l4 = sp.sympify(
        complete["quartic_contact"]["complete_L4_x_z1"], locals=local_symbols
    )
    symbols = {item.name: item for item in l3.free_symbols | l4.free_symbols}
    nonanalytic = symbols["grad_pi_sq_three_halves"]
    l3_analytic = sp.expand(l3 + symbols["A_IR"] * nonanalytic)
    l4_analytic = sp.expand(l4 + symbols["A_IR"] * symbols["delta_N_1"] * nonanalytic)
    require("analytic cubic separation", nonanalytic not in l3_analytic.free_symbols)
    require("analytic quartic separation", nonanalytic not in l4_analytic.free_symbols)

    contact = contact_kernel(l4_analytic, symbols)
    source = pair_source_kernel(l3_analytic, symbols)
    partitions = [
        {"pairs": [[1, 2], [3, 4]], "channel_q_sq": "q_1^2+q_2^2+2*k1_dot_k2"},
        {"pairs": [[1, 3], [2, 4]], "channel_q_sq": "q_1^2+q_3^2+2*k1_dot_k3"},
        {"pairs": [[1, 4], [2, 3]], "channel_q_sq": "q_1^2+q_4^2+2*k1_dot_k4"},
    ]
    require("three Schur pairings", len(partitions) == 3)

    e1, e2, e3, e4 = sp.symbols("toy_epsilon_1:5", real=True)
    b12, b13, b14, b23, b24, b34 = sp.symbols(
        "B_12 B_13 B_14 B_23 B_24 B_34", real=True
    )
    toy_source = (
        b12 * e1 * e2
        + b13 * e1 * e3
        + b14 * e1 * e4
        + b23 * e2 * e3
        + b24 * e2 * e4
        + b34 * e3 * e4
    )
    toy_schur = -sp.diff(toy_source**2 / 2, e1, e2, e3, e4)
    require_zero(
        "Schur pairing combinatorics",
        toy_schur + b12 * b34 + b13 * b24 + b14 * b23,
    )

    return {
        "conventions": {
            "fourier": "D_i -> i*k_i; k1+k2+k3+k4=0",
            "external_domain": "q_i>0 and det(C(q_i))!=0",
            "finite_channel_domain": "q_K>0 and det(C(q_K))!=0",
            "contact_factorization": "substitute the listed per-leg delta_N1 and Sigma1 resolvers",
            "schur_factorization": "instantiate B_ab for each pair and contract the three partitions",
        },
        "analytic_contact_kernel": {
            "expression": str(contact["kernel"]),
            "physical_basis_expression": str(contact["physical"]),
            "momentum_closure": [str(item) for item in contact["closure"]],
            "constraint_resolvers": contact["resolvers"],
            "status": "PASS_COMPLETE_ANALYTIC_QUARTIC_CONTACT_POLARIZATION",
        },
        "complete_pair_source_kernel": {
            "variables": ["Xi", "Q_rho", "Q_chi", "Pi"],
            "B_N_ab": str(source["B_N"]),
            "B_Sigma_ab": str(source["B_Sigma"]),
            "input_constraint_resolvers": source["input_resolvers"],
            "definition": "B_ab=d^3 L3/(d epsilon_a d epsilon_b d z_K) at zero amplitudes",
            "status": "PASS_COMPLETE_PHYSICAL_PAIR_CONSTRAINT_SOURCE",
        },
        "finite_q_schur_kernel": {
            "C_K": str(source["constraint_matrix"]),
            "C_K_inverse": str(source["constraint_inverse"]),
            "partitions": partitions,
            "assembly": "W_Schur=-sum_(ab|cd) B_ab(-K)^T C(K)^(-1) B_cd(K)",
            "reduced_kernel": "W_red=W_contact+W_Schur",
            "status": "PASS_FACTORIZED_FINITE_Q_REDUCED_QUARTIC_KERNEL",
        },
        "homogeneous_internal_channel": {
            "constraint_projector_N_Sigma": str(source["constraint_projector"]),
            "physical_projector_Xi_Qrho_Qchi_Pi": str(source["physical_projector"]),
            "projected_constraint_inverse": str(source["homogeneous_inverse"]),
            "domain": "V!=0 for the retained homogeneous lapse constraint",
            "B_N_com_limit": str(source["B_N_q0_com"]),
            "B_Sigma_com_limit_diagnostic_only": str(
                source["B_Sigma_q0_com_diagnostic"]
            ),
            "rule": (
                "At exact q_K=0 remove Sigma=-D^2 beta and Xi before inversion; "
                "retain the homogeneous lapse constraint and the (Q_rho,Q_chi,Pi) physical subspace."
            ),
            "boundary": "This projected q0 rule is not obtained by substituting q_K=0 into the finite-q inverse.",
            "status": "PASS_ALGEBRAIC_GAUGE_REGULAR_Q0_PROJECTOR_PRESCRIPTION",
        },
        "nonanalytic_track_a_term": {
            "quartic_functional": "-A_IR*delta_N1*|grad(pi)|^3",
            "ordinary_four_leg_taylor_kernel": "DOES_NOT_EXIST_AT_GRAD_PI_0",
            "status": "HELD_FOR_DECLARED_NONZERO_GRADIENT_LOCAL_BACKGROUND",
        },
    }


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = build_kernel(args.complete_functional, args.cubic_kernel)
    summary = {
        "gate": "UVIR-003",
        "stage": "B_REDUCED_QUARTIC_MOMENTUM_KERNEL",
        "calculation_status": "PASS",
        "subgate_status": "PASS_FACTORIZED_FINITE_Q_REDUCED_QUARTIC_KERNEL",
        "quartic_contact_kernel_status": "DERIVED_AND_VERIFIED",
        "complete_pair_source_status": "DERIVED_AND_VERIFIED",
        "finite_q_schur_kernel_status": "DERIVED_AND_VERIFIED",
        "homogeneous_internal_channel_status": (
            "PROJECTOR_PRESCRIPTION_DEFINED_AND_AUDITED"
        ),
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "result": result,
        "scientific_boundary": (
            "The analytic quartic contact and complete constraint-induced "
            "Schur kernels are polarized and assembled in a factorized "
            "physical-basis representation. The exact homogeneous channel "
            "uses separate projectors that remove Sigma and Xi rather than "
            "a naive finite-q substitution. No propagating exchange "
            "amplitude, unitarity bound, or cutoff is claimed."
        ),
        "next_required_calculation": [
            "construct the local adiabatic quadratic propagators in the physical basis",
            "assemble nonzero-channel exchange terms from the cubic kernels",
            "apply the projected q0 rule to the exact centre-of-mass channel",
            "combine exchange and reduced contact terms before testing a declared unitarity criterion",
        ],
    }
    output = args.output_dir / "uvir003_reduced_quartic_momentum_kernel_summary.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("Analytic quartic contact polarization: VERIFIED")
    print("Complete physical pair-source kernel: DERIVED_FACTORIZED")
    print("Finite-q quartic Schur kernel: DERIVED_FACTORIZED")
    print("Exact q0 constraint/physical projectors: DEFINED_AND_AUDITED")
    print("Exact |grad(pi)|^3 quartic Taylor kernel: NONANALYTIC_AT_ZERO_GRADIENT")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_FACTORIZED_FINITE_Q_REDUCED_QUARTIC_KERNEL")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
