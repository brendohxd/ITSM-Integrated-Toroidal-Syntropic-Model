#!/usr/bin/env python3
"""Factorized finite-q cubic momentum kernel for UVIR-003."""

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
        "--output-dir",
        type=Path,
        default=base / "outputs",
    )
    return parser.parse_args()


def require(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"{name} failed")


def leg_sum(eps, values):
    return sp.Add(*(eps[i] * values[i] for i in range(3)))


def pair_sum(eps, left, right, dot, power=1, sign=1):
    return sp.Add(
        *(
            sign * eps[i] * eps[j] * dot[i][j] ** power * left[i] * right[j]
            for i in range(3)
            for j in range(3)
        )
    )


def constraint_solution(q, fields, symbols):
    lapse, sigma, determinant = [], [], []
    for i in range(3):
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
    xi = sp.symbols("Xi_1:4", real=True)
    xi_dot = sp.symbols("Xi_dot_1:4", real=True)
    q_rho = sp.symbols("Q_rho_1:4", real=True)
    q_rho_dot = sp.symbols("Q_rho_dot_1:4", real=True)
    q_chi = sp.symbols("Q_chi_1:4", real=True)
    q_chi_dot = sp.symbols("Q_chi_dot_1:4", real=True)
    force = sp.symbols("Pi_1:4", real=True)
    force_dot = sp.symbols("Pi_dot_1:4", real=True)
    hubble_dot, rho_ddot, chemical_dot = sp.symbols("H_dot rho_ddot mu_dot", real=True)
    hubble = symbols["H"]
    rho = symbols["rho"]
    rho_dot = symbols["rho_dot"]
    chemical = symbols["mu"]
    result = {}
    for i in range(3):
        result.update(
            {
                fields["R"][i]: hubble * xi[i] / q[i],
                fields["delta_rho"][i]: (q_rho[i] + rho_dot * xi[i] / q[i]),
                fields["vartheta"][i]: (q_chi[i] / rho + chemical * xi[i] / q[i]),
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


def build_kernel(source_path: Path) -> dict[str, object]:
    with source_path.open("r", encoding="utf-8") as handle:
        source = json.load(handle)["symbolic_audit"]
    require(
        "complete cubic dependency",
        source["cubic_functional"]["status"]
        == "PASS_COMPLETE_GENERIC_L3_X_Z1_FUNCTIONAL",
    )
    require(
        "complete quartic dependency",
        source["quartic_contact"]["status"] == "PASS_COMPLETE_GENERIC_L4_X_Z1_CONTACT",
    )

    gamma = sp.Symbol("gamma", real=True)
    l3 = sp.sympify(
        source["cubic_functional"]["complete_L3_x_z1"],
        locals={"gamma": gamma},
    )
    symbols = {item.name: item for item in l3.free_symbols}
    l3_analytic = sp.expand(l3 + symbols["A_IR"] * symbols["grad_pi_sq_three_halves"])
    require(
        "nonanalytic term separated",
        symbols["grad_pi_sq_three_halves"] not in l3_analytic.free_symbols,
    )

    eps = sp.symbols("epsilon_1:4", real=True)
    q = sp.symbols("q_1:4", positive=True)
    q1, q2, q3 = q
    dot = [
        [
            q1**2,
            (q3**2 - q1**2 - q2**2) / 2,
            (q2**2 - q1**2 - q3**2) / 2,
        ],
        [
            (q3**2 - q1**2 - q2**2) / 2,
            q2**2,
            (q1**2 - q2**2 - q3**2) / 2,
        ],
        [
            (q2**2 - q1**2 - q3**2) / 2,
            (q1**2 - q2**2 - q3**2) / 2,
            q3**2,
        ],
    ]
    fields = {
        label: sp.symbols(f"{label}_1:4", real=True)
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
    lapse = sp.symbols("delta_N_1_1:4", real=True)
    sigma = sp.symbols("Sigma_1_1:4", real=True)
    beta = tuple(sigma[i] / q[i] ** 2 for i in range(3))

    replacements = {
        symbols["R"]: leg_sum(eps, fields["R"]),
        symbols["R_dot"]: leg_sum(eps, fields["R_dot"]),
        symbols["delta_rho"]: leg_sum(eps, fields["delta_rho"]),
        symbols["delta_rho_dot"]: leg_sum(eps, fields["delta_rho_dot"]),
        symbols["vartheta_dot"]: leg_sum(eps, fields["vartheta_dot"]),
        symbols["pi_dot"]: leg_sum(eps, fields["pi_dot"]),
        symbols["delta_N_1"]: leg_sum(eps, lapse),
        symbols["D2_beta_1"]: -leg_sum(eps, sigma),
        symbols["lap_pi"]: -leg_sum(
            eps,
            tuple(q[i] ** 2 * fields["pi"][i] for i in range(3)),
        ),
        symbols["D_delta_N_1_sq"]: pair_sum(eps, lapse, lapse, dot, sign=-1),
        symbols["D_delta_N_1_dot_D_R"]: pair_sum(eps, lapse, fields["R"], dot, sign=-1),
        symbols["Dij_beta_1_sq"]: pair_sum(eps, beta, beta, dot, power=2),
        symbols["D_R_dot_D_beta_1"]: pair_sum(eps, fields["R"], beta, dot, sign=-1),
        symbols["D_beta_1_dot_D_delta_rho"]: pair_sum(
            eps, beta, fields["delta_rho"], dot, sign=-1
        ),
        symbols["D_beta_1_dot_D_vartheta"]: pair_sum(
            eps, beta, fields["vartheta"], dot, sign=-1
        ),
        symbols["D_beta_1_dot_D_pi"]: pair_sum(eps, beta, fields["pi"], dot, sign=-1),
        symbols["grad_R_sq"]: pair_sum(eps, fields["R"], fields["R"], dot, sign=-1),
        symbols["grad_delta_rho_sq"]: pair_sum(
            eps,
            fields["delta_rho"],
            fields["delta_rho"],
            dot,
            sign=-1,
        ),
        symbols["grad_vartheta_sq"]: pair_sum(
            eps,
            fields["vartheta"],
            fields["vartheta"],
            dot,
            sign=-1,
        ),
        symbols["grad_R_dot_grad_pi"]: pair_sum(
            eps, fields["R"], fields["pi"], dot, sign=-1
        ),
    }
    replacements[symbols["Dij_beta_1_Di_R_Dj_beta_1"]] = sp.Add(
        *(
            eps[i]
            * eps[j]
            * eps[k]
            * dot[i][j]
            * dot[i][k]
            * beta[i]
            * fields["R"][j]
            * beta[k]
            for i in range(3)
            for j in range(3)
            for k in range(3)
        )
    )

    polarized = l3_analytic.xreplace(replacements)
    kernel = sp.diff(polarized, eps[0], eps[1], eps[2]).subs(
        {eps[0]: 0, eps[1]: 0, eps[2]: 0}
    )
    require(
        "epsilon-free cubic coefficient",
        not any(item in kernel.free_symbols for item in eps),
    )
    require(
        "nonempty cubic coefficient",
        kernel != 0,
    )

    lapse_solution, sigma_solution, determinants = constraint_solution(
        q, fields, symbols
    )
    basis_map = physical_map(q, fields, symbols)
    physical_kernel = kernel.xreplace(basis_map)
    physical_lapse = [item.xreplace(basis_map) for item in lapse_solution]
    physical_sigma = [item.xreplace(basis_map) for item in sigma_solution]

    return {
        "conventions": {
            "fourier": "D_i -> i*k_i; k1+k2+k3=0",
            "dot_products": {
                "k1_dot_k2": str(dot[0][1]),
                "k1_dot_k3": str(dot[0][2]),
                "k2_dot_k3": str(dot[1][2]),
            },
            "domain": "q_i>0 and det(C(q_i))!=0 for every leg",
            "factorization": (
                "substitute the listed per-leg delta_N1 and Sigma1 "
                "resolvers into the factorized kernel"
            ),
        },
        "analytic_cubic_kernel": {
            "expression": str(kernel),
            "constraint_placeholders": [
                "delta_N_1_i",
                "Sigma_1_i",
            ],
            "coefficient_extraction": (
                "d^3 L3(epsilon_1,e_2,e_3)"
                "/(d epsilon_1 d epsilon_2 d epsilon_3) at epsilon_i=0"
            ),
            "status": "PASS_COMPLETE_ANALYTIC_CUBIC_POLARIZATION",
        },
        "physical_basis_kernel": {
            "variables": ["Xi", "Q_rho", "Q_chi", "Pi"],
            "expression": str(physical_kernel),
            "map_includes_dot_T": True,
            "status": "PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL",
        },
        "constraint_resolvers": {
            f"leg_{i + 1}": {
                "det_C": str(determinants[i]),
                "old_basis_delta_N_1": str(lapse_solution[i]),
                "old_basis_Sigma_1": str(sigma_solution[i]),
                "physical_basis_delta_N_1": str(physical_lapse[i]),
                "physical_basis_Sigma_1": str(physical_sigma[i]),
                "physical_basis_beta_1": str(physical_sigma[i] / q[i] ** 2),
            }
            for i in range(3)
        },
        "nonanalytic_track_a_term": {
            "functional": "-A_IR*|grad(pi)|^3",
            "ordinary_trilinear_taylor_kernel": ("DOES_NOT_EXIST_AT_GRAD_PI_0"),
            "status": "HELD_FOR_DECLARED_NONZERO_GRADIENT_LOCAL_BACKGROUND",
        },
        "homogeneous_channel": {
            "exact_q0_Xi": "EXCLUDED_AS_TIME_TRANSLATION_GAUGE_ORBIT",
            "naive_s_channel_projection": "NOT_DEFINED",
            "consequence": ("q=0 cannot be substituted into this finite-q kernel"),
        },
    }


def run() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = build_kernel(args.complete_functional)
    summary = {
        "gate": "UVIR-003",
        "stage": "B_COMPLETE_CUBIC_MOMENTUM_KERNEL",
        "calculation_status": "PASS",
        "subgate_status": ("PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL"),
        "analytic_cubic_kernel_status": "DERIVED_AND_VERIFIED",
        "physical_basis_projection_status": "DERIVED_FOR_Q_I_GT_0",
        "exact_ir_kernel_status": "NONANALYTIC_AT_ZERO_GRADIENT",
        "homogeneous_internal_channel_status": ("NOT_DEFINED_BY_FINITE_Q_MAP"),
        "physical_2_to_2_status": "NOT_YET_DERIVED",
        "full_gate_status": "IN_PROGRESS",
        "mat001_status": "BLOCKED",
        "result": result,
        "scientific_boundary": (
            "The complete analytic cubic functional is polarized and mapped "
            "to a factorized physical-basis kernel with exact per-leg z1 "
            "resolvers. The exact |grad(pi)|^3 functional has no Taylor "
            "kernel at zero gradient, and the homogeneous internal Xi "
            "channel is outside the finite-q map. No amplitude or cutoff "
            "is claimed."
        ),
        "next_required_calculation": [
            "polarize the complete reduced quartic functional",
            "construct local adiabatic propagators",
            "derive a gauge-regular zero-momentum internal-channel prescription",
            "assemble the amplitude only after that prescription passes",
        ],
    }
    output = args.output_dir / "uvir003_cubic_momentum_kernel_summary.json"
    with output.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    print("Complete analytic cubic polarization: VERIFIED")
    print("Finite-q constraint resolvers: EXPLICIT_PER_LEG")
    print("Physical-basis cubic kernel: DERIVED_FACTORIZED")
    print("Exact |grad(pi)|^3 Taylor kernel: NONANALYTIC_AT_ZERO_GRADIENT")
    print("Homogeneous internal Xi channel: NOT_DEFINED_BY_FINITE_Q_MAP")
    print("Physical 2-to-2 amplitude: NOT_YET_DERIVED")
    print("UVIR-003: IN_PROGRESS")
    print("MAT-001: BLOCKED")
    print("STATUS: PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
