#!/usr/bin/env python3
"""MAT-001 R3: covariant conformal matter action and scoped ADM-source audit.

The calculation freezes a universal conformal metric coupling and varies an
exact massive-particle representative in ADM variables.  It establishes the
controlled limit in which the earlier Track-A linear source covector h=(0,0)
is recovered, while retaining the mixed lapse/phonon and moving-matter shift
vertices required by the covariant action.  It does not compute C_m, K_Q or V.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import sympy as sp


PASS_STATUS = "PASS_MAT001_R3_COVARIANT_MATTER_ACTION_SCOPED"
FAIL_STATUS = "FAIL_MAT001_R3_COVARIANT_MATTER_ACTION"


def parse_args() -> argparse.Namespace:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=base / "outputs")
    parser.add_argument("--self-test-mutations", action="store_true")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, **details: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), **details})


def exported_contract_valid(summary: dict[str, Any]) -> bool:
    controlled = summary.get("controlled_linear_limit") or {}
    covectors = controlled.get("J2_extra_force_covectors") or {}
    coefficients = controlled.get("coefficients") or {}
    firewall = summary.get("status_firewall") or {}
    action = summary.get("action_freeze") or {}
    return bool(
        action.get("adm_worldline_domain") == "N>0 and D^2=N^2-h_ij*w^i*w^j>0"
        and covectors.get("d") == ["-C_m"]
        and covectors.get("h") == ["0", "0"]
        and coefficients.get("psi_vertex") == "-C_m*m"
        and coefficients.get("mixed_psi_lapse") == "-C_m*m"
        and coefficients.get("mixed_psi_shift_moving") == "C_m*m*v/sqrt(1 - v**2)"
        and "only" in str(controlled.get("scope", ""))
        and all(
            firewall.get(key) is False
            for key in ("C_m_numeric_derived", "K_Q_numeric_derived", "V_computed", "MAT001_pass")
        )
    )


def derive() -> dict[str, Any]:
    # One spatial component is sufficient to test the indexed ADM identities:
    # w^i = dx^i/dt + N^i and D = sqrt(N^2-h_ij w^i w^j).
    n = sp.symbols("N", positive=True)
    beta, velocity = sp.symbols("beta v", real=True)
    psi, c_m, mass = sp.symbols("psi C_m m", real=True)
    a_psi = sp.exp(c_m * psi)
    w = velocity + beta
    d_tau_dt = sp.sqrt(n**2 - w**2)
    l_m = -mass * a_psi * d_tau_dt
    l_m_uncoupled = -mass * d_tau_dt
    l_int = sp.simplify(l_m - l_m_uncoupled)

    exact = {
        "dL_m_dN": sp.simplify(sp.diff(l_m, n)),
        "dL_m_dbeta": sp.simplify(sp.diff(l_m, beta)),
        "dL_int_dN": sp.simplify(sp.diff(l_int, n)),
        "dL_int_dbeta": sp.simplify(sp.diff(l_int, beta)),
        "dL_int_dpsi": sp.simplify(sp.diff(l_int, psi)),
    }

    background = {n: 1, beta: 0, velocity: 0, psi: 0}
    linear = {
        "psi_vertex": sp.simplify(sp.diff(l_int, psi).subs(background)),
        "pure_lapse_source": sp.simplify(sp.diff(l_int, n).subs(background)),
        "pure_shift_source": sp.simplify(sp.diff(l_int, beta).subs(background)),
        "mixed_psi_lapse": sp.simplify(
            sp.diff(l_int, psi, n).subs(background)
        ),
        "mixed_psi_shift_comoving": sp.simplify(
            sp.diff(l_int, psi, beta).subs(background)
        ),
        "mixed_psi_shift_moving": sp.simplify(
            sp.diff(l_int, psi, beta).subs({n: 1, beta: 0, psi: 0})
        ),
    }

    phi_n = sp.symbols("Phi_N", real=True)
    weak_l = sp.series(
        l_m.subs({n: 1 + phi_n, beta: 0}),
        psi,
        0,
        2,
    ).removeO()
    weak_l = sp.series(weak_l, phi_n, 0, 2).removeO()
    weak_l = sp.series(weak_l, velocity, 0, 3).removeO()
    weak_l = sp.expand(weak_l)
    weak_coefficients = {
        "rest": sp.simplify(weak_l.subs({psi: 0, phi_n: 0, velocity: 0})),
        "Phi_N": sp.simplify(sp.diff(weak_l, phi_n).subs({psi: 0, velocity: 0})),
        "psi": sp.simplify(sp.diff(weak_l, psi).subs({phi_n: 0, velocity: 0})),
        "v2": sp.simplify(
            sp.diff(weak_l, velocity, 2).subs({psi: 0, phi_n: 0, velocity: 0})
            / 2
        ),
    }

    # Diffeomorphism Ward identity for S_m[A(psi)^2 g, Psi_m]:
    # (1/sqrt(-g)) delta S_m/delta psi = alpha(psi) T_m,
    # nabla_mu T_m^{mu}{}_{nu} = alpha T_m nabla_nu psi.
    # For dust T_m=-rho_m and alpha=d ln A/dpsi=C_m.
    rho = sp.symbols("rho_m", positive=True)
    alpha = sp.simplify(sp.diff(sp.log(a_psi), psi))
    dust_trace = -rho
    exchange_coefficient = sp.simplify(alpha * dust_trace)

    checks: list[dict[str, Any]] = []
    add_check(checks, "conformal_factor_positive", a_psi.is_positive is True)
    add_check(
        checks,
        "exact_lapse_variation",
        sp.simplify(exact["dL_m_dN"] + mass * a_psi * n / d_tau_dt) == 0,
    )
    add_check(
        checks,
        "exact_shift_variation",
        sp.simplify(exact["dL_m_dbeta"] - mass * a_psi * w / d_tau_dt) == 0,
    )
    add_check(checks, "weak_newtonian_vertex", weak_coefficients["Phi_N"] == -mass)
    add_check(checks, "weak_phonon_vertex", weak_coefficients["psi"] == -c_m * mass)
    add_check(checks, "weak_kinetic_term", weak_coefficients["v2"] == mass / 2)
    add_check(checks, "linear_d_equals_minus_C_m", linear["psi_vertex"] == -c_m * mass)
    add_check(
        checks,
        "linear_interaction_h_zero_on_normalized_comoving_background",
        linear["pure_lapse_source"] == 0 and linear["pure_shift_source"] == 0,
    )
    add_check(
        checks,
        "mixed_lapse_vertex_retained",
        linear["mixed_psi_lapse"] == -c_m * mass,
    )
    add_check(
        checks,
        "comoving_mixed_shift_zero",
        linear["mixed_psi_shift_comoving"] == 0,
    )
    add_check(
        checks,
        "moving_matter_mixed_shift_retained",
        sp.simplify(
            linear["mixed_psi_shift_moving"]
            - c_m * mass * velocity / sp.sqrt(1 - velocity**2)
        )
        == 0,
    )
    add_check(checks, "dust_exchange_sign", exchange_coefficient == -c_m * rho)

    all_ok = all(row["ok"] for row in checks)
    return {
        "gate": "MAT-001",
        "remediation_item": "R3",
        "subgate_status": PASS_STATUS if all_ok else FAIL_STATUS,
        "calculation_status": "PASS" if all_ok else "FAIL",
        "action_freeze": {
            "metric_signature": "(-,+,+,+)",
            "matter_metric": "g_tilde_munu=A(psi)^2*g_munu",
            "conformal_factor_natural_units": "A(psi)=exp(C_m*(psi-psi_star))",
            "conformal_factor_SI": "A(psi_SI)=exp(C_m*(psi_SI-psi_star_SI)/c^2)",
            "normalization_point": "A(psi_star)=1",
            "adm_worldline_domain": "N>0 and D^2=N^2-h_ij*w^i*w^j>0",
            "worldline_orientation": "future-directed timelike",
            "matter_action": "S_m[Psi_m,g_tilde]",
            "interaction_definition": "S_int=S_m[Psi_m,A^2*g]-S_m[Psi_m,g]",
            "dust_representative": "S_pp=-sum_A m_A integral A(psi) ds_g",
            "no_double_counting": True,
        },
        "matter_variables": {
            "fundamental_representative": "massive worldlines x_A^mu(lambda)",
            "continuum_limit": "pressureless conserved-number dust",
            "baryon_density": "rho_b is rest-mass density in the controlled NR limit",
            "dynamical_not_external": True,
        },
        "adm_convention": {
            "line_element": "ds^2=-N^2 dt^2+h_ij(dx^i+N^i dt)(dx^j+N^j dt)",
            "particle_D": "D=sqrt(N^2-h_ij(v^i+N^i)(v^j+N^j))",
            "particle_L": "L_A=-m_A*A(psi)*D",
            "functional_sources": {
                "delta_Sm_delta_N": "-sqrt(h)*E_m",
                "delta_Sm_delta_Ni": "+sqrt(h)*j_i_m",
                "delta_Sm_delta_hij": "+N*sqrt(h)*S_m^ij/2",
            },
        },
        "exact_one_direction_representative": {k: str(v) for k, v in exact.items()},
        "controlled_linear_limit": {
            "background": "N=1, N^i=0, v^i=0, psi=psi_star",
            "coefficients": {k: str(v) for k, v in linear.items()},
            "J2_extra_force_covectors": {"d": ["-C_m"], "h": ["0", "0"]},
            "scope": (
                "h=(0,0) applies only to the linear extra-force source sector at "
                "the normalized comoving background. It does not erase the mixed "
                "rho_b*pi*delta_N vertex or moving-matter shift source."
            ),
        },
        "weak_field_recovery": {
            "lagrangian_order": "m*v^2/2-m*Phi_N-m*C_m*psi plus rest mass",
            "coefficients": {k: str(v) for k, v in weak_coefficients.items()},
            "continuum_interaction": "L_int_NR=-C_m*rho_b*psi",
        },
        "conservation_exchange": {
            "alpha": str(alpha),
            "ward_identity": "nabla_mu T_m^mu{}_nu=alpha*T_m*nabla_nu(psi)",
            "dust_trace": str(dust_trace),
            "dust_exchange": "Q_mp_nu=-C_m*rho_m*nabla_nu(psi)",
            "force_sector_balance": "nabla_mu T_psi^mu{}_nu=-Q_mp_nu on shell",
            "total_matter_plus_force_conserved": True,
            "status": "PASS_SCOPED_WARD_IDENTITY_FULL_MULTI_SECTOR_JOIN_NOT_RUN",
        },
        "scientific_boundaries": [
            "The conformal action is a selected MAT matter-force completion, not a UV completion.",
            "C_m remains an unmatched Wilson coefficient; K_Q and V are not computed.",
            "A purely conformal coupling does not complete the relativistic lensing gate.",
            "The full gravity+aether+condensate+force+dust constraint propagation is not run here.",
        ],
        "status_firewall": {
            "C_m_numeric_derived": False,
            "K_Q_numeric_derived": False,
            "V_computed": False,
            "MAT001_pass": False,
            "UVIR003_pass": False,
            "stage4A_reopened": False,
            "physics_pass": False,
        },
        "checks": checks,
        "n_checks": len(checks),
    }


def mutation_suite(summary: dict[str, Any]) -> None:
    require(summary["subgate_status"] == PASS_STATUS, "baseline must pass")
    require(exported_contract_valid(summary), "baseline exported contract")
    bad_sign = copy.deepcopy(summary)
    bad_sign["controlled_linear_limit"]["J2_extra_force_covectors"]["d"] = ["+C_m"]
    require(not exported_contract_valid(bad_sign), "sign-flipped d must fail")
    erased_mixed_lapse = copy.deepcopy(summary)
    erased_mixed_lapse["controlled_linear_limit"]["coefficients"]["mixed_psi_lapse"] = "0"
    require(not exported_contract_valid(erased_mixed_lapse), "erased mixed lapse must fail")
    fake_global_h = copy.deepcopy(summary)
    fake_global_h["controlled_linear_limit"]["scope"] = "h vanishes identically"
    require(not exported_contract_valid(fake_global_h), "global h claim must fail")
    for key in ("C_m_numeric_derived", "K_Q_numeric_derived", "V_computed", "MAT001_pass"):
        require(summary["status_firewall"][key] is False, key)


def main() -> None:
    args = parse_args()
    summary = derive()
    require(summary["calculation_status"] == "PASS", "R3 scoped derivation checks")
    require(exported_contract_valid(summary), "exported contract")
    if args.self_test_mutations:
        mutation_suite(summary)
        print("MUTATION_SUITE: PASS")
        return

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "mat001_r3_covariant_matter_action_summary.json"
    payload = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest().upper()
    (args.output_dir / "mat001_r3_covariant_matter_action_summary.sha256").write_text(
        f"{digest}  {output.name}\n", encoding="ascii"
    )
    print("MAT-001 R3 covariant matter action")
    print("  action:", summary["action_freeze"]["matter_metric"])
    print("  linear d,h:", summary["controlled_linear_limit"]["J2_extra_force_covectors"])
    print("  exchange:", summary["conservation_exchange"]["dust_exchange"])
    for row in summary["checks"]:
        print(f"  [{'OK' if row['ok'] else 'FAIL'}] {row['name']}")
    print("STATUS:", summary["subgate_status"])
    print("JSON_SHA256:", digest)


if __name__ == "__main__":
    main()
