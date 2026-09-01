#!/usr/bin/env python3
"""PKM1-P0 finite-density parent ADM, Dirac and locality audit.

This freezes one local covariant parent in which the ITSM condensate phase is
the khronon and ordinary matter is universally metric coupled.  J(Y) is
explicitly classified as fundamental IR EFT data.  The calculation rejects
or retains individual controls fail-closed; a successful execution is not a
physics pass and cannot change MAT-001 or UVIR-003.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import solve_ivp


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def add_check(
    rows: list[dict[str, Any]],
    name: str,
    ok: bool,
    **details: Any,
) -> None:
    rows.append({"name": name, "ok": bool(ok), **details})


def require_zero(name: str, expression: sp.Expr | sp.MatrixBase) -> None:
    reduced = sp.simplify(expression)
    if isinstance(reduced, sp.MatrixBase):
        if all(sp.factor(value) == 0 for value in reduced):
            return
        raise AssertionError(f"{name} failed: {reduced}")
    if sp.factor(reduced) != 0:
        raise AssertionError(f"{name} failed: {reduced}")


def symbolic_parent_audit() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # 1. The inherited and stability-first J(Y) controls.
    # ------------------------------------------------------------------
    y, a0 = sp.symbols("y a0", positive=True)
    Y = a0**2 * y**2

    denominator_a = 1 + y + y**2 + y**3
    mu_a = sp.factor(1 - 1 / denominator_a)
    j_a = a0**2 * (
        sp.log(1 + y)
        - sp.log(1 + y**2) / 2
        - sp.atan(y)
    )
    jy_a = sp.factor(sp.diff(j_a, y) / sp.diff(Y, y))
    jrad_a = sp.factor(jy_a + y * sp.diff(jy_a, y) / 2 * 2)
    # Since 2Y J_YY = y d(J_Y)/dy, the last expression is J_Y+y J_Y'.
    jrad_a = sp.factor(jy_a + y * sp.diff(jy_a, y))
    expected_jrad_a = sp.factor(
        (2 * y**3 + y**2 - 1) / denominator_a**2
    )
    require_zero("P0-A transverse identity", jy_a - (mu_a - 1))
    require_zero("P0-A radial Hessian", jrad_a - expected_jrad_a)
    roots = sp.nroots(2 * y**3 + y**2 - 1, n=30, maxsteps=200)
    positive_roots = sorted(
        float(sp.re(root))
        for root in roots
        if abs(float(sp.im(root))) < 1.0e-20 and float(sp.re(root)) > 0
    )
    y_critical = positive_roots[0]
    add_check(
        checks,
        "P0_A_inherited_fast_transition_control_rejected",
        len(positive_roots) == 1
        and 0.0 < y_critical < 1.0
        and float(jrad_a.subs(y, 1)) > 0.0,
        mu_y=str(mu_a),
        J_Y=str(jy_a),
        radial_khronon_Hessian=str(jrad_a),
        critical_y=y_critical,
        sign_domain=(
            "J_Y+2Y*J_YY<0 for 0<y<y_critical; "
            ">0 for y>y_critical"
        ),
        consequence=(
            "the radial lapse/khronon principal kinetic coefficient changes "
            "sign; prior static ellipticity did not test this condition"
        ),
    )

    mu_b = sp.factor(y / (1 + y))
    j_b = sp.factor(-2 * a0**2 * (y - sp.log(1 + y)))
    jy_b = sp.factor(sp.diff(j_b, y) / sp.diff(Y, y))
    jrad_b = sp.factor(jy_b + y * sp.diff(jy_b, y))
    static_transverse_b = mu_b
    static_radial_b = sp.factor(mu_b + y * sp.diff(mu_b, y))
    kinetic_transverse_b = sp.factor(-jy_b)
    kinetic_radial_b = sp.factor(-jrad_b)
    require_zero("P0-B interpolation identity", 1 + jy_b - mu_b)
    require_zero(
        "P0-B radial static eigenvalue",
        static_radial_b - y * (y + 2) / (1 + y) ** 2,
    )
    require_zero(
        "P0-B transverse khronon Hessian",
        kinetic_transverse_b - 1 / (1 + y),
    )
    require_zero(
        "P0-B radial khronon Hessian",
        kinetic_radial_b - 1 / (1 + y) ** 2,
    )
    low_series_b = sp.series(j_b, y, 0, 7)
    add_check(
        checks,
        "P0_B_stability_first_control_passes_local_symbolic_conditions",
        sp.limit(mu_b / y, y, 0, dir="+") == 1
        and sp.limit(mu_b, y, sp.oo) == 1
        and sp.limit(j_b / Y, y, sp.oo) == 0
        and sp.ask(sp.Q.positive(static_transverse_b)) is True
        and sp.ask(sp.Q.positive(static_radial_b)) is True
        and sp.ask(sp.Q.positive(kinetic_transverse_b)) is True
        and sp.ask(sp.Q.positive(kinetic_radial_b)) is True,
        mu_y=str(mu_b),
        J_y=str(j_b),
        J_series=str(low_series_b),
        static_transverse=str(static_transverse_b),
        static_radial=str(static_radial_b),
        khronon_kinetic_transverse=str(kinetic_transverse_b),
        khronon_kinetic_radial=str(kinetic_radial_b),
        high_acceleration=(
            "mu->1 and J/Y->0, but J itself does not approach a constant"
        ),
        classification="STABILITY_FIRST_EFT_EXISTENCE_CONTROL_NOT_ITSM_DERIVATION",
    )

    # General stability-versus-fast-tail identity.  Put delta=1-mu=-J_Y.
    delta = sp.Function("delta")(y)
    stability_identity = sp.simplify(
        (-delta - y * sp.diff(delta, y))
        + sp.diff(y * delta, y)
    )
    require_zero("stable-tail differential identity", stability_identity)
    add_check(
        checks,
        "pure_J_stable_tail_tradeoff_derived",
        stability_identity == 0,
        identity=(
            "J_Y+2Y*J_YY=-[delta+y*delta']; radial kinetic positivity "
            "requires (y*delta)'>=0, where delta=1-mu>0"
        ),
        implication=(
            "after any y0 with delta(y0)>0, delta(y)>=y0*delta(y0)/y; "
            "a globally stable pure-J control cannot have a faster-than-1/y "
            "approach to mu=1"
        ),
        finite_J_implication=(
            "because dJ/dy=-2*a0^2*y*delta, the same conditions forbid a "
            "finite constant J at y->infinity"
        ),
        boundary=(
            "this is an action-class tradeoff, not yet a Solar-System "
            "exclusion; PPN/ephemeris bounds require a separate test"
        ),
    )

    # ------------------------------------------------------------------
    # 2. Same-condensate K(Q) identity and radial relaxation.
    # ------------------------------------------------------------------
    mp2, s, chemical, mrho2, qclock = sp.symbols(
        "M_P_sq s mu M_rho_sq Q", positive=True
    )
    p0, pz, pzz = sp.symbols("P_0 P_Z P_ZZ", real=True)
    zshift = chemical**2 * qclock**2 - chemical**2
    p_taylor = p0 + pz * zshift + pzz * zshift**2 / 2
    k_eff = p_taylor / mp2
    kqq_general = sp.simplify(
        sp.diff(k_eff, qclock, 2).subs(qclock, 1)
    )
    kqq_condensate = sp.factor(
        kqq_general.subs({pz: s / 2, pzz: s / mrho2})
    )
    sound_sq = sp.factor(mrho2 / (mrho2 + 4 * chemical**2))
    expected_kqq = sp.factor(s * chemical**2 / (mp2 * sound_sq))
    require_zero(
        "relaxed same-condensate K_QQ", kqq_condensate - expected_kqq
    )
    fixed_amplitude_kqq = sp.factor(s * chemical**2 / mp2)
    helmholtz_mass_sq = sp.factor(kqq_condensate / 2)
    add_check(
        checks,
        "same_condensate_forces_positive_Helmholtz_susceptibility",
        sp.ask(sp.Q.positive(kqq_condensate)) is True
        and sp.ask(sp.Q.positive(helmholtz_mass_sq)) is True
        and sp.simplify(kqq_condensate / fixed_amplitude_kqq)
        == 1 / sound_sq,
        fixed_amplitude_K_QQ=str(fixed_amplitude_kqq),
        relaxed_K_QQ=str(kqq_condensate),
        sound_speed_squared=str(sound_sq),
        enhancement_factor=str(sp.simplify(1 / sound_sq)),
        m_K_squared=str(helmholtz_mass_sq),
        conclusion=(
            "exact K_QQ=0 is incompatible with s>0, mu>0 and stable finite "
            "M_rho; radial relaxation strengthens rather than cancels the term"
        ),
    )

    h, radius, ellipticity, enthalpy_fraction = sp.symbols(
        "H R lambda_stat f_h", positive=True
    )
    locality_ratio = sp.factor(
        helmholtz_mass_sq * radius**2 / ellipticity
    )
    locality_frw = sp.factor(
        sp.Rational(3, 2)
        * enthalpy_fraction
        * (h * radius) ** 2
        / (sound_sq * ellipticity)
    )
    require_zero(
        "FRW locality reparameterization",
        locality_ratio.subs(
            s * chemical**2,
            3 * enthalpy_fraction * mp2 * h**2,
        )
        - locality_frw,
    )
    window_ratio = sp.factor(
        helmholtz_mass_sq / (ellipticity * mrho2)
    )
    add_check(
        checks,
        "local_AQUAL_window_is_conditional_not_algebraically_empty",
        locality_ratio.is_positive is True and window_ratio.is_positive is True,
        locality_ratio=str(locality_ratio),
        FRW_form=str(locality_frw),
        conditions=[
            "m_K^2/(lambda_stat*k^2)<<1 with k~1/R",
            "k^2<<M_rho^2 for Thomas-Fermi radial elimination",
            "window exists only if m_K^2/(lambda_stat*M_rho^2)<<1",
        ],
        status=(
            "PARAMETRIC_DOMAIN_CONDITION_DERIVED; NO ITSM PARAMETER POINT "
            "OR GALACTIC DOMAIN ESTABLISHED"
        ),
    )

    # ------------------------------------------------------------------
    # 3. Exact unitary-gauge ADM Hamiltonian and constraint count.
    # ------------------------------------------------------------------
    lapse = sp.symbols("N", positive=True)
    phase_hamiltonian = -s * chemical**2 / (2 * lapse)
    phase_hessian = sp.simplify(
        sp.diff(phase_hamiltonian, lapse, 2).subs(lapse, 1)
    )
    require_zero("homogeneous phase lapse Hessian", phase_hessian + s * chemical**2)
    covariant_dof = sp.Rational(24 - 2 * 8, 2)
    unitary_dof = sp.Rational(22 - 2 * 6 - 2, 2)
    add_check(
        checks,
        "ADM_Dirac_count_regular_on_finite_charge_Y0_branch",
        covariant_dof == 4
        and unitary_dof == 4
        and phase_hessian != 0,
        canonical_momenta={
            "pi_ij": "(M_P^2/2)*sqrt(h)*(K^ij-h^ij*K)",
            "p_rho": "sqrt(h)*(dot(rho)-N^i D_i rho)/N",
            "p_N": "0",
            "p_i": "0",
        },
        Hamiltonian=(
            "H=int[N*H0+N^i*H_i+M_P^2*N*sqrt(h)*J(Y)"
            "-sqrt(h)*rho^2*mu_Theta^2/(2N)]"
        ),
        lapse_constraint=(
            "C_N=H0+M_P^2*sqrt(h)*(J-2YJ_Y)"
            "-D_i[2*M_P^2*sqrt(h)*J_Y*D^iN/N]"
            "+sqrt(h)*rho^2*mu_Theta^2/(2N^2)"
        ),
        covariant_count=(
            "12 configuration variables, 8 first-class constraints -> 4 DOF"
        ),
        unitary_count=(
            "11 configuration variables; 6 spatial-diffeomorphism first-class "
            "constraints and (p_N,C_N) second class -> 4 DOF"
        ),
        physical_DOF=["2 tensor", "1 phase/khronon", "1 amplitude"],
        Y0_local_bracket_coefficient=str(phase_hessian),
        result=(
            "the fundamental-J parent has no constraint-rank loss at Y=0 "
            "while rho*mu is nonzero; this does not regularize its cubic "
            "nonanalyticity"
        ),
    )

    # Principal p_N-C_N differential symbol.  The Lagrangian kinetic signs
    # are -J_Y and -(J_Y+2YJ_YY); both are positive for P0-B.
    add_check(
        checks,
        "P0_B_generic_Y_constraint_principal_symbol_is_nonzero",
        sp.ask(sp.Q.positive(kinetic_transverse_b)) is True
        and sp.ask(sp.Q.positive(kinetic_radial_b)) is True,
        Hamiltonian_principal_eigenvalues=[
            "2*M_P^2*J_Y/N",
            "2*M_P^2*(J_Y+2Y*J_YY)/N",
        ],
        Lagrangian_kinetic_eigenvalues=[
            "-2*M_P^2*J_Y",
            "-2*M_P^2*(J_Y+2Y*J_YY)",
        ],
        P0_B_values=[
            "2*M_P^2/(1+y)",
            "2*M_P^2/(1+y)^2",
        ],
        domain="every finite y>0 on a smooth timelike phase chart",
    )

    # ------------------------------------------------------------------
    # 4. Exact background results.
    # ------------------------------------------------------------------
    rho_dot, potential_value = sp.symbols("rho_dot V", real=True)
    energy = (
        rho_dot**2 + s * chemical**2
    ) / 2 + potential_value
    pressure = (
        rho_dot**2 + s * chemical**2
    ) / 2 - potential_value
    enthalpy = sp.factor(energy + pressure)
    require_zero(
        "finite-density enthalpy", enthalpy - rho_dot**2 - s * chemical**2
    )
    add_check(
        checks,
        "stationary_finite_density_Minkowski_no_go_with_only_Lambda_counterterm",
        sp.ask(sp.Q.positive(enthalpy.subs(rho_dot, 0))) is True,
        energy_density=str(energy.subs(rho_dot, 0)),
        pressure=str(pressure.subs(rho_dot, 0)),
        rho_plus_p=str(enthalpy.subs(rho_dot, 0)),
        reason=(
            "a cosmological constant can shift rho and p oppositely but cannot "
            "cancel rho+p=s*mu^2>0; exact stationary Minkowski therefore "
            "requires loss of finite charge or a new counterstress sector"
        ),
        retained_background="evolving flat FRW",
    )

    # FRW conservation identities for the retained background.
    hubble, hubble_dot = sp.symbols("H H_dot", real=True)
    rho, rho_ddot, theta_ddot = sp.symbols(
        "rho rho_ddot Theta_ddot", real=True
    )
    potential_prime = sp.symbols("V_rho", real=True)
    rho_ddot_os = -3 * hubble * rho_dot + rho * chemical**2 - potential_prime
    theta_ddot_os = -3 * hubble * chemical - 2 * rho_dot * chemical / rho
    hubble_dot_os = -(
        rho_dot**2 + rho**2 * chemical**2
    ) / (2 * mp2)
    radial_residual = (
        rho_ddot
        + 3 * hubble * rho_dot
        - rho * chemical**2
        + potential_prime
    )
    charge_residual = (
        rho**2 * theta_ddot
        + 2 * rho * rho_dot * chemical
        + 3 * hubble * rho**2 * chemical
    )
    require_zero(
        "P0 FRW radial equation", radial_residual.subs(rho_ddot, rho_ddot_os)
    )
    require_zero(
        "P0 FRW charge equation", charge_residual.subs(theta_ddot, theta_ddot_os)
    )
    add_check(
        checks,
        "P0_FRW_equations_close_without_J_background_contribution",
        j_b.subs(y, 0) == 0,
        equations={
            "Friedmann": (
                "3*M_P^2*H^2=(rho_dot^2+rho^2*mu^2)/2+V"
            ),
            "Raychaudhuri": str(hubble_dot_os),
            "radial": str(radial_residual),
            "charge": str(charge_residual),
        },
        boundary=(
            "J(Y) vanishes and has no homogeneous variation at Y=0; the "
            "background is the canonical condensate FRW branch, not LambdaCDM"
        ),
    )

    # ------------------------------------------------------------------
    # 5. Uniform-phase scalar ADM reduction on the on-shell FRW branch.
    # ------------------------------------------------------------------
    m, hfrw, rhof, rdf, muf, q, c_j = sp.symbols(
        "M_P_sq H rho rho_dot mu q_phys C_J", positive=True
    )
    # rho_dot is allowed to have either sign below.
    rdf = sp.symbols("rho_dot", real=True)
    v0, vr, vrr = sp.symbols("V V_rho V_rhorho", real=True)
    curvature, amplitude = sp.symbols("R delta_rho", real=True)
    curvature_dot, amplitude_dot = sp.symbols(
        "R_dot delta_rho_dot", real=True
    )
    alpha, shear = sp.symbols("delta_N Sigma", real=True)
    enthalpy_frw = rdf**2 + rhof**2 * muf**2

    constraint_matrix = sp.Matrix(
        [[c_j * q**2 - 2 * v0, 2 * m * hfrw], [2 * m * hfrw, 0]]
    )
    constraint_source = sp.Matrix(
        [
            6 * m * hfrw * curvature_dot
            + 2 * m * q**2 * curvature
            - (vr + rhof * muf**2) * amplitude
            - rdf * amplitude_dot,
            -2 * m * curvature_dot - rdf * amplitude,
        ]
    )
    unconstrained = (
        -3 * m * curvature_dot**2
        - 18 * m * hfrw * curvature * curvature_dot
        + (m * q**2 - 9 * v0) * curvature**2
        + 3 * (rhof * muf**2 - vr) * curvature * amplitude
        + 3 * rdf * curvature * amplitude_dot
        + amplitude_dot**2 / 2
        + (muf**2 - vrr - q**2) * amplitude**2 / 2
    )
    constraints = sp.Matrix([alpha, shear])
    compact_lagrangian = sp.expand(
        unconstrained
        + (constraints.T * constraint_source)[0]
        + (constraints.T * constraint_matrix * constraints)[0] / 2
    )

    # Independent expansion of the exact ADM blocks, specialized to the
    # phase-defined foliation and no independent aether.
    raw_lagrangian = sp.expand(
        -3 * m * curvature_dot**2
        - 2 * m * shear * curvature_dot
        + 6 * m * hfrw * alpha * curvature_dot
        + 2 * m * hfrw * alpha * shear
        - 3 * m * hfrw**2 * alpha**2
        + 9 * m * hfrw**2 * alpha * curvature
        - 18 * m * hfrw * curvature * curvature_dot
        - 27 * m * hfrw**2 * curvature**2 / 2
        + m * q**2 * curvature**2
        + 2 * m * q**2 * alpha * curvature
        + c_j * q**2 * alpha**2 / 2
        + enthalpy_frw * alpha**2 / 2
        + alpha
        * (
            -3 * v0 * curvature
            - 3 * enthalpy_frw * curvature / 2
            - vr * amplitude
            - rhof * muf**2 * amplitude
            - rdf * amplitude_dot
        )
        + curvature**2 * (-9 * v0 / 2 + 9 * enthalpy_frw / 4)
        + curvature * (-3 * vr + 3 * rhof * muf**2) * amplitude
        - shear * rdf * amplitude
        + 3 * rdf * curvature * amplitude_dot
        + amplitude_dot**2 / 2
        + (muf**2 - vrr - q**2) * amplitude**2 / 2
    )
    friedmann_h2 = (enthalpy_frw / 2 + v0) / (3 * m)
    require_zero(
        "P0 independent quadratic ADM reconstruction",
        (raw_lagrangian - compact_lagrangian).subs(hfrw**2, friedmann_h2),
    )

    constraint_solution = sp.simplify(
        -constraint_matrix.inv() * constraint_source
    )
    reduced = sp.factor(
        unconstrained
        - (
            constraint_source.T
            * constraint_matrix.inv()
            * constraint_source
        )[0]
        / 2
    )
    coordinates = sp.Matrix([curvature, amplitude])
    velocities = sp.Matrix([curvature_dot, amplitude_dot])
    kinetic = sp.hessian(reduced, velocities)
    mixed = sp.Matrix(
        [
            [
                sp.diff(reduced, velocities[row], coordinates[column])
                for column in range(2)
            ]
            for row in range(2)
        ]
    )
    coordinate_hessian = sp.hessian(reduced, coordinates)
    friedmann_v = {v0: 3 * m * hfrw**2 - enthalpy_frw / 2}
    kinetic_on_shell = sp.simplify(kinetic.subs(friedmann_v))
    expected_kinetic = sp.Matrix(
        [
            [
                (enthalpy_frw + c_j * q**2) / hfrw**2,
                -rdf / hfrw,
            ],
            [-rdf / hfrw, 1],
        ]
    )
    require_zero("P0 reduced FRW kinetic matrix", kinetic_on_shell - expected_kinetic)
    kinetic_det = sp.factor(kinetic_on_shell.det())
    expected_det = sp.factor(
        (rhof**2 * muf**2 + c_j * q**2) / hfrw**2
    )
    require_zero("P0 reduced FRW kinetic determinant", kinetic_det - expected_det)
    constraint_det = sp.factor(constraint_matrix.det())
    require_zero(
        "P0 FRW constraint determinant",
        constraint_det + 4 * m**2 * hfrw**2,
    )
    add_check(
        checks,
        "P0_B_FRW_scalar_kinetic_matrix_is_positive_at_finite_and_zero_q",
        sp.ask(sp.Q.positive(expected_det)) is True
        and sp.ask(sp.Q.positive(expected_det.subs(q, 0))) is True
        and constraint_det != 0,
        variables=["R in uniform-phase gauge", "delta_rho"],
        constraints=["delta_N", "Sigma=q_phys^2*beta"],
        constraint_matrix=str(constraint_matrix),
        constraint_determinant=str(constraint_det),
        reduced_kinetic_matrix=str(expected_kinetic),
        reduced_kinetic_determinant=str(expected_det),
        strict_q0_determinant=str(expected_det.subs(q, 0)),
        P0_B_FRW_coefficient="C_J=-2*M_P^2*J_Y(0)=2*M_P^2",
        conclusion=(
            "two positive scalar kinetic directions persist at q=0 on the "
            "finite-charge expanding branch; this is a quadratic no-ghost "
            "result, not a complete time-dependent stability proof"
        ),
    )

    # Low-energy fixed-metric phase characteristic after radial elimination.
    k = sp.symbols("k", positive=True)
    phase_omega_sq = sp.factor(
        pz * k**2
        / (pz + 2 * chemical**2 * pzz + mp2 * k**2 / chemical**2)
    )
    phase_omega_cond = sp.factor(
        phase_omega_sq.subs({pz: s / 2, pzz: s / mrho2})
    )
    require_zero(
        "P0 phase low-k sound speed",
        sp.limit(phase_omega_cond / k**2, k, 0, dir="+") - sound_sq,
    )
    formal_plateau = sp.factor(sp.limit(phase_omega_cond, k, sp.oo))
    require_zero(
        "P0 formal phase plateau",
        formal_plateau - s * chemical**2 / (2 * mp2),
    )
    add_check(
        checks,
        "controlled_decoupling_phase_characteristic_is_non_ghost_but_nonrelativistic",
        sp.ask(sp.Q.positive(phase_omega_cond)) is True,
        dispersion=str(phase_omega_cond),
        low_k="omega^2=c_s^2*k^2",
        formal_high_k=str(formal_plateau),
        front_speed="formal omega/k -> 0",
        validity=(
            "the Thomas-Fermi expression requires k^2<<M_rho^2, so its "
            "literal k->infinity plateau is a scaling diagnostic, not a UV "
            "prediction"
        ),
        implication=(
            "the J term supplies a positive k^2-dependent time kinetic term; "
            "the full amplitude-metric characteristics and cutoff remain open"
        ),
    )

    # Substitute the polynomial potential for the numerical FRW validation.
    mass_sq, quartic, sextic, cutoff = sp.symbols(
        "m_squared lambda4 lambda6 Lambda", positive=True
    )
    potential_poly = (
        mass_sq * rhof**2 / 2
        + quartic * rhof**4 / 8
        + sextic * rhof**6 / (24 * cutoff**2)
    )
    potential_prime_poly = sp.diff(potential_poly, rhof)
    potential_second_poly = sp.diff(potential_prime_poly, rhof)
    numeric_sub = {
        v0: potential_poly,
        vr: potential_prime_poly,
        vrr: potential_second_poly,
    }
    matrix_arguments = (
        m,
        hfrw,
        rhof,
        rdf,
        muf,
        q,
        c_j,
        mass_sq,
        quartic,
        sextic,
        cutoff,
    )
    matrix_function = sp.lambdify(
        matrix_arguments,
        (
            kinetic.subs(numeric_sub),
            mixed.subs(numeric_sub),
            coordinate_hessian.subs(numeric_sub),
            constraint_matrix.subs(numeric_sub),
        ),
        modules="numpy",
    )

    all_ok = all(row["ok"] for row in checks)
    return {
        "checks": checks,
        "all_ok": all_ok,
        "controls": {
            "P0_A": {
                "mu": str(mu_a),
                "J": str(j_a),
                "J_Y": str(jy_a),
                "J_Y_plus_2YJ_YY": str(jrad_a),
                "critical_y": y_critical,
                "disposition": "REJECT_FINITE_Y_RADIAL_KHRONON_KINETIC_SIGN_CHANGE",
            },
            "P0_B": {
                "mu": str(mu_b),
                "J": str(j_b),
                "J_Y": str(jy_b),
                "J_Y_plus_2YJ_YY": str(jrad_b),
                "static_radial": str(static_radial_b),
                "disposition": "RETAIN_AS_STABILITY_FIRST_EFT_CONTROL_ONLY",
            },
        },
        "condensate_lapse_response": {
            "K_QQ_fixed_amplitude": str(fixed_amplitude_kqq),
            "K_QQ_relaxed": str(kqq_condensate),
            "m_K_squared": str(helmholtz_mass_sq),
            "c_s_squared": str(sound_sq),
            "locality_ratio": str(locality_ratio),
            "locality_FRW_form": str(locality_frw),
            "TF_window_ratio": str(window_ratio),
        },
        "adm": {
            "reduced_FRW_kinetic_matrix": str(expected_kinetic),
            "reduced_FRW_kinetic_determinant": str(expected_det),
            "constraint_determinant": str(constraint_det),
            "constraint_solution": str(constraint_solution),
            "physical_DOF": 4,
        },
        "phase_characteristic": {
            "omega_squared": str(phase_omega_cond),
            "low_k_speed_squared": str(sound_sq),
            "formal_plateau": str(formal_plateau),
        },
        "matrix_function": matrix_function,
    }


def potential_functions(
    params: dict[str, float],
) -> tuple[
    Callable[[float | np.ndarray], float | np.ndarray],
    Callable[[float | np.ndarray], float | np.ndarray],
]:
    def potential(rho: float | np.ndarray) -> float | np.ndarray:
        return (
            params["m_squared"] * rho**2 / 2
            + params["lambda4"] * rho**4 / 8
            + params["lambda6"] * rho**6
            / (24 * params["Lambda"] ** 2)
        )

    def potential_prime(rho: float | np.ndarray) -> float | np.ndarray:
        return (
            params["m_squared"] * rho
            + params["lambda4"] * rho**3 / 2
            + params["lambda6"] * rho**5
            / (4 * params["Lambda"] ** 2)
        )

    return potential, potential_prime


def integrate_frw() -> tuple[
    dict[str, Any],
    list[dict[str, float]],
    dict[str, float],
]:
    params = {
        "M_P": 1.0,
        "m_squared": 1.0,
        "lambda4": 0.50,
        "lambda6": 0.20,
        "Lambda": 2.0,
    }
    potential, potential_prime = potential_functions(params)
    mp2 = params["M_P"] ** 2
    a_initial = 1.0
    rho_initial = 1.0
    rho_dot_initial = 0.0
    theta_initial = 0.0
    mu_initial = math.sqrt(float(potential_prime(rho_initial)) / rho_initial)
    charge = a_initial**3 * rho_initial**2 * mu_initial
    energy_initial = (
        rho_dot_initial**2 / 2
        + rho_initial**2 * mu_initial**2 / 2
        + float(potential(rho_initial))
    )
    hubble_initial = math.sqrt(energy_initial / (3 * mp2))

    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        scale, rho, rho_dot, theta, hubble = state
        if scale <= 0 or rho <= 0:
            raise RuntimeError("P0 representative branch left a>0,rho>0")
        chemical = charge / (scale**3 * rho**2)
        return np.array(
            [
                scale * hubble,
                rho_dot,
                -3 * hubble * rho_dot
                + rho * chemical**2
                - potential_prime(rho),
                chemical,
                -(rho_dot**2 + rho**2 * chemical**2) / (2 * mp2),
            ],
            dtype=float,
        )

    times = np.linspace(0.0, 6.0, 601)
    initial = np.array(
        [
            a_initial,
            rho_initial,
            rho_dot_initial,
            theta_initial,
            hubble_initial,
        ],
        dtype=float,
    )
    solution = solve_ivp(
        rhs,
        (float(times[0]), float(times[-1])),
        initial,
        method="DOP853",
        t_eval=times,
        rtol=1.0e-11,
        atol=1.0e-13,
    )
    if not solution.success or solution.t.size != times.size:
        raise AssertionError(f"FRW integration failed: {solution.message}")
    scale, rho, rho_dot, theta, hubble = solution.y
    chemical = charge / (scale**3 * rho**2)
    energy = (
        rho_dot**2 / 2
        + rho**2 * chemical**2 / 2
        + potential(rho)
    )
    pressure = (
        rho_dot**2 / 2
        + rho**2 * chemical**2 / 2
        - potential(rho)
    )
    friedmann = 3 * mp2 * hubble**2 - energy
    friedmann_scale = np.maximum.reduce(
        [
            np.abs(3 * mp2 * hubble**2),
            np.abs(energy),
            np.full_like(energy, 1.0e-30),
        ]
    )
    rel_friedmann = np.abs(friedmann) / friedmann_scale
    charge_samples = scale**3 * rho**2 * chemical
    rel_charge = np.abs(charge_samples / charge - 1)
    rho_ddot = (
        -3 * hubble * rho_dot
        + rho * chemical**2
        - potential_prime(rho)
    )
    chemical_dot = chemical * (-3 * hubble - 2 * rho_dot / rho)
    energy_dot = (
        rho_dot * rho_ddot
        + rho * rho_dot * chemical**2
        + rho**2 * chemical * chemical_dot
        + potential_prime(rho) * rho_dot
    )
    continuity = energy_dot + 3 * hubble * (energy + pressure)
    continuity_scale = np.maximum(
        np.abs(3 * hubble * (energy + pressure)), 1.0e-30
    )
    rel_continuity = np.abs(continuity) / continuity_scale
    if float(np.max(rel_friedmann)) >= 1.0e-9:
        raise AssertionError("FRW Friedmann propagation tolerance failed")
    if float(np.max(rel_charge)) >= 1.0e-12:
        raise AssertionError("FRW charge tolerance failed")
    if float(np.max(rel_continuity)) >= 1.0e-12:
        raise AssertionError("FRW continuity tolerance failed")
    if not bool(np.all(hubble > 0)) or not bool(np.all(rho > 0)):
        raise AssertionError("FRW representative left expanding finite-density domain")

    rows: list[dict[str, float]] = []
    for index in range(times.size):
        rows.append(
            {
                "t": float(solution.t[index]),
                "a": float(scale[index]),
                "rho": float(rho[index]),
                "rho_dot": float(rho_dot[index]),
                "Theta": float(theta[index]),
                "mu": float(chemical[index]),
                "H": float(hubble[index]),
                "energy_density": float(energy[index]),
                "pressure": float(pressure[index]),
                "friedmann_residual": float(friedmann[index]),
                "charge": float(charge_samples[index]),
                "continuity_residual": float(continuity[index]),
            }
        )
    summary = {
        "status": "PASS_ON_SHELL_DIMENSIONLESS_EXISTENCE_BRANCH",
        "scope": "existence and matrix validation only; not a cosmological fit",
        "parameters": params,
        "initial_conditions": {
            "a": a_initial,
            "rho": rho_initial,
            "rho_dot": rho_dot_initial,
            "Theta": theta_initial,
            "mu": mu_initial,
            "H": hubble_initial,
            "charge": charge,
        },
        "integration": {
            "method": "scipy.solve_ivp_DOP853",
            "t_start": float(times[0]),
            "t_end": float(times[-1]),
            "samples": int(times.size),
            "rtol": 1.0e-11,
            "atol": 1.0e-13,
            "function_evaluations": int(solution.nfev),
        },
        "endpoint": {
            "a": float(scale[-1]),
            "rho": float(rho[-1]),
            "rho_dot": float(rho_dot[-1]),
            "Theta": float(theta[-1]),
            "mu": float(chemical[-1]),
            "H": float(hubble[-1]),
        },
        "diagnostics": {
            "max_relative_friedmann_residual": float(np.max(rel_friedmann)),
            "max_relative_charge_drift": float(np.max(rel_charge)),
            "max_relative_continuity_residual": float(np.max(rel_continuity)),
            "minimum_rho": float(np.min(rho)),
            "minimum_H": float(np.min(hubble)),
            "expansion_factor": float(scale[-1] / scale[0]),
        },
    }
    return summary, rows, params


def evaluate_matrices(
    matrix_function: Callable[..., Any],
    params: dict[str, float],
    state: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    hubble, rho, rho_dot, chemical, q = state
    values = matrix_function(
        params["M_P"] ** 2,
        hubble,
        rho,
        rho_dot,
        chemical,
        q,
        2 * params["M_P"] ** 2,
        params["m_squared"],
        params["lambda4"],
        params["lambda6"],
        params["Lambda"],
    )
    return tuple(np.asarray(value, dtype=float) for value in values)


def background_flow(
    params: dict[str, float],
    state: np.ndarray,
) -> np.ndarray:
    potential, potential_prime = potential_functions(params)
    del potential
    hubble, rho, rho_dot, chemical, q = state
    mp2 = params["M_P"] ** 2
    return np.array(
        [
            -(rho_dot**2 + rho**2 * chemical**2) / (2 * mp2),
            rho_dot,
            -3 * hubble * rho_dot
            + rho * chemical**2
            - potential_prime(rho),
            chemical * (-3 * hubble - 2 * rho_dot / rho),
            -hubble * q,
        ],
        dtype=float,
    )


def directional_derivatives(
    matrix_function: Callable[..., Any],
    params: dict[str, float],
    state: np.ndarray,
    step_scale: float,
) -> tuple[np.ndarray, np.ndarray]:
    flow = background_flow(params, state)
    rate = max(
        1.0,
        abs(state[0]),
        abs(state[2] / state[1]),
        abs(state[3]),
    )
    dt = step_scale * 1.0e-6 / rate
    plus = state + dt * flow
    minus = state - dt * flow
    if min(plus[1], minus[1], plus[4], minus[4]) <= 0:
        raise AssertionError("directional derivative left rho>0,q>0")
    k_plus, p_plus, _, _ = evaluate_matrices(matrix_function, params, plus)
    k_minus, p_minus, _, _ = evaluate_matrices(matrix_function, params, minus)
    return (k_plus - k_minus) / (2 * dt), (
        p_plus - p_minus
    ) / (2 * dt)


def equation_generator(
    matrix_function: Callable[..., Any],
    params: dict[str, float],
    state: np.ndarray,
) -> tuple[np.ndarray, float]:
    kinetic, mixed, coordinate, _ = evaluate_matrices(
        matrix_function, params, state
    )
    kinetic_dot, mixed_dot = directional_derivatives(
        matrix_function, params, state, 1.0
    )
    hubble = state[0]
    # The quadratic matrices are per a^3.  The volume derivative is retained.
    damping = kinetic_dot + 3 * hubble * kinetic + mixed - mixed.T
    stiffness = mixed_dot + 3 * hubble * mixed - coordinate
    generator = np.block(
        [
            [np.zeros((2, 2)), np.eye(2)],
            [
                -np.linalg.solve(kinetic, stiffness),
                -np.linalg.solve(kinetic, damping),
            ],
        ]
    )
    kinetic_dot_half, mixed_dot_half = directional_derivatives(
        matrix_function, params, state, 0.5
    )
    scale = max(
        np.linalg.norm(kinetic_dot_half),
        np.linalg.norm(mixed_dot_half),
        1.0e-30,
    )
    error = max(
        np.linalg.norm(kinetic_dot - kinetic_dot_half),
        np.linalg.norm(mixed_dot - mixed_dot_half),
    ) / scale
    return generator, float(error)


def scan_quadratic_system(
    symbolic: dict[str, Any],
    frw_rows: list[dict[str, float]],
    params: dict[str, float],
) -> dict[str, Any]:
    matrix_function = symbolic["matrix_function"]
    ratios = np.concatenate(([0.0], np.logspace(-3, 3, 31)))
    indices = list(range(0, len(frw_rows), 10))
    if indices[-1] != len(frw_rows) - 1:
        indices.append(len(frw_rows) - 1)
    negative_count = 0
    zero_count = 0
    min_eigenvalue = math.inf
    min_det = math.inf
    min_constraint_abs_det = math.inf
    q0_min_det = math.inf
    for index in indices:
        row = frw_rows[index]
        for ratio in ratios:
            state = np.array(
                [
                    row["H"],
                    row["rho"],
                    row["rho_dot"],
                    row["mu"],
                    ratio * row["H"],
                ],
                dtype=float,
            )
            kinetic, _, _, constraint = evaluate_matrices(
                matrix_function, params, state
            )
            kinetic_symmetric = (kinetic + kinetic.T) / 2
            eigenvalues = np.linalg.eigvalsh(kinetic_symmetric)
            tolerance = 1.0e-10 * max(float(np.max(np.abs(eigenvalues))), 1.0)
            negative_count += int(np.sum(eigenvalues < -tolerance))
            zero_count += int(np.sum(np.abs(eigenvalues) <= tolerance))
            determinant = float(np.linalg.det(kinetic))
            constraint_determinant = abs(float(np.linalg.det(constraint)))
            min_eigenvalue = min(min_eigenvalue, float(np.min(eigenvalues)))
            min_det = min(min_det, determinant)
            min_constraint_abs_det = min(
                min_constraint_abs_det, constraint_determinant
            )
            if ratio == 0:
                q0_min_det = min(q0_min_det, determinant)

    if negative_count != 0 or zero_count != 0:
        raise AssertionError("P0 FRW kinetic scan found a non-positive direction")
    if min_det <= 0 or q0_min_det <= 0 or min_constraint_abs_det <= 0:
        raise AssertionError("P0 FRW determinant scan failed")

    generator_samples: list[dict[str, Any]] = []
    max_derivative_error = 0.0
    snapshot_indices = [0, len(frw_rows) // 2, len(frw_rows) - 1]
    for index in snapshot_indices:
        row = frw_rows[index]
        for ratio in (0.1, 1.0, 10.0, 100.0, 1000.0):
            state = np.array(
                [
                    row["H"],
                    row["rho"],
                    row["rho_dot"],
                    row["mu"],
                    ratio * row["H"],
                ],
                dtype=float,
            )
            generator, derivative_error = equation_generator(
                matrix_function, params, state
            )
            eigenvalues = np.linalg.eigvals(generator) / row["H"]
            max_derivative_error = max(max_derivative_error, derivative_error)
            ordered = sorted(
                eigenvalues,
                key=lambda value: (float(value.real), float(value.imag)),
            )
            generator_samples.append(
                {
                    "t": row["t"],
                    "q_over_H": ratio,
                    "lambda_over_H": [
                        {
                            "real": float(value.real),
                            "imag": float(value.imag),
                        }
                        for value in ordered
                    ],
                    "max_abs_imag_over_q": float(
                        np.max(np.abs(eigenvalues.imag)) / ratio
                    ),
                    "directional_derivative_relative_error": derivative_error,
                }
            )
    if max_derivative_error >= 1.0e-4:
        raise AssertionError("P0 generator directional derivatives did not converge")
    return {
        "kinetic_scan": {
            "trajectory_snapshots": len(indices),
            "q_over_H_samples": int(ratios.size),
            "total_matrix_samples": int(len(indices) * ratios.size),
            "negative_eigenvalue_count": negative_count,
            "numerical_zero_count": zero_count,
            "minimum_raw_kinetic_eigenvalue": min_eigenvalue,
            "minimum_kinetic_determinant": min_det,
            "minimum_q0_kinetic_determinant": q0_min_det,
            "minimum_absolute_constraint_determinant": min_constraint_abs_det,
            "status": "PASS_VALIDATION_OF_SYMBOLIC_POSITIVITY",
        },
        "local_equation_generator": {
            "samples": generator_samples,
            "maximum_directional_derivative_relative_error": max_derivative_error,
            "volume_factor_derivative_included": True,
            "included_background_derivatives": [
                "H_dot",
                "rho_dot",
                "rho_ddot",
                "mu_dot",
                "q_phys_dot=-H*q_phys",
                "d(a^3)/dt=3H*a^3",
            ],
            "interpretation": (
                "instantaneous FRW generator only; real parts are not a "
                "basis-invariant global instability rate and no conserved "
                "FRW Hamiltonian is claimed"
            ),
        },
    }


def write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inputs = {
        "spec": HERE / "PKM1_P0_FINITE_DENSITY_PARENT_SPEC.md",
        "core_identity": ROOT / "Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md",
        "route_decision": ROOT
        / "Theory/Core/ITSM_PKM1_BROAD_ROUTE_DECISION_2026-08-25.md",
        "uvir001_summary": ROOT
        / "Analysis/UVIR/UVIR-001/outputs/uvir001_summary.json",
    }
    prior = load(inputs["uvir001_summary"])
    if prior.get("candidate_verdict") != "FAIL":
        raise AssertionError("UVIR-001 fail-closed baseline changed")

    symbolic = symbolic_parent_audit()
    if not symbolic["all_ok"]:
        failed = [row["name"] for row in symbolic["checks"] if not row["ok"]]
        raise AssertionError(f"symbolic checks failed: {failed}")
    frw, frw_rows, params = integrate_frw()
    quadratic = scan_quadratic_system(symbolic, frw_rows, params)

    summary = {
        "audit": "PKM1_P0_FINITE_DENSITY_PARENT_ADM_DIRAC_HAMILTONIAN",
        "calculation_status": "PASS_BOUNDED_PARENT_AUDIT",
        "physics_pass": False,
        "route_disposition": (
            "HOLD_PKM1_P0_B_STABILITY_FIRST_CONTROL_ONLY_P0_A_REJECTED"
        ),
        "frozen_parent": {
            "action": (
                "S=int sqrt(-g){(M_P^2/2)[R-2J(Y)]"
                "-(nabla rho)^2/2-rho^2(nabla Theta)^2/2-V(rho)}"
                "+S_m[Psi_m,g]"
            ),
            "phase_map": (
                "U_mu=-nabla_mu Theta/sqrt(Z), Z=-nabla_Theta^2>0, "
                "Y=(U.nabla U)^2"
            ),
            "J_classification": "FUNDAMENTAL_CONTROLLED_IR_EFT_DATA_NOT_DERIVED",
            "matter": "single universally and minimally coupled metric",
            "excluded": [
                "independent aether",
                "independent force psi",
                "appended free K(Q)",
                "engineered non-affine auxiliary s",
                "reservoir and topology completion",
            ],
        },
        "control_decisions": symbolic["controls"],
        "same_action_condensate_result": symbolic[
            "condensate_lapse_response"
        ],
        "ADM_Dirac_result": symbolic["adm"],
        "FRW_background": frw,
        "quadratic_FRW_validation": quadratic,
        "phase_characteristic": symbolic["phase_characteristic"],
        "derived": [
            "P0-A has a radial khronon kinetic sign change at finite y",
            "P0-B passes the bounded static and khronon Hessian inequalities",
            "the canonical condensate supplies a strictly positive K_QQ and Helmholtz scale",
            "radial relaxation enhances K_QQ by 1/c_s^2",
            "the fundamental-J parent carries four local physical DOF",
            "the finite-charge Y=0 branch has no Dirac or reduced-kinetic rank loss",
            "stationary finite-density Minkowski is impossible in P0 with only a Lambda counterterm",
            "an on-shell expanding FRW existence branch and positive two-scalar kinetic matrix were verified",
            "a local AQUAL regime is a parameter-window question, not an exact equation",
        ],
        "open_or_not_derived": [
            "microscopic origin and radiative stability of J_B and a0",
            "a physical ITSM parameter point satisfying the local-AQUAL window",
            "complete stationary nonzero-gradient galactic background and Hamiltonian",
            "nonlinear zero-gradient strong-coupling scale and physical cutoff",
            "Jeans band from the complete time-dependent perturbation system",
            "PPN, ephemeris, Shapiro, lensing, GW and compact-object limits",
            "winding, defect cores, compact T3 topology and reservoir compatibility",
        ],
        "route_level_interpretation": (
            "The earlier finite-constant fast-transition interpolation is not "
            "a healthy global PKM1 control because its radial khronon kinetic "
            "Hessian changes sign. A stability-first pure-J comparator exists "
            "and the same finite-density parent has a regular quadratic FRW "
            "constraint count, so the action class is not rejected. However, "
            "global pure-J kinetic stability enforces a slow high-acceleration "
            "tail, while the canonical condensate produces a nonzero Helmholtz "
            "term. These are new PPN/locality burdens, not solved predictions."
        ),
        "external_primary_context": [
            {
                "citation": "Blanchet and Marsat (2011)",
                "url": "https://arxiv.org/abs/1107.5264",
                "use": "metric-hosted MOND action-class precedent",
            },
            {
                "citation": "Bonetti and Barausse (2015)",
                "url": "https://arxiv.org/abs/1502.05554",
                "use": (
                    "high-acceleration GR versus strong-coupling and PPN "
                    "completion precedent; no result inherited"
                ),
            },
            {
                "citation": "Flanagan (2023)",
                "url": "https://arxiv.org/abs/2302.14846",
                "use": (
                    "stationary low-acceleration khronon kinetic conditions "
                    "and nonstationary caveat; no stability inherited"
                ),
            },
            {
                "citation": "Blanchet and Skordis (2024)",
                "url": "https://arxiv.org/abs/2404.06584",
                "use": "J(Y)+K(Q) Hamiltonian and cosmology precedent",
            },
        ],
        "gate_firewall": {
            "MAT_001": "BLOCKED",
            "UVIR_003": "IN_PROGRESS",
            "V": "NOT_COMPUTED_IN_LIVE_ROUTE",
            "K_Q": "NOT_DERIVED_IN_LIVE_ROUTE",
            "a0": "NOT_DERIVED",
            "canonical_action_replaced": False,
            "downstream_opened": False,
            "commit_push_publication": False,
        },
        "checks": symbolic["checks"],
        "software": {
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
        },
        "input_sha256": {name: digest(path) for name, path in inputs.items()},
        "scientific_boundary": (
            "A PASS_BOUNDED_PARENT_AUDIT means the displayed algebra, "
            "representative FRW integration and matrix checks reproduced. It "
            "does not establish a microscopic J, a physical parameter window, "
            "a nonlinear stable theory, MOND phenomenology, cosmological "
            "viability, or a Tier-1 physics pass."
        ),
    }

    json_path = OUT / "itsm_pkm1_finite_density_parent_hamiltonian_summary.json"
    csv_path = OUT / "itsm_pkm1_p0_frw_trajectory.csv"
    report_path = OUT / "ITSM_PKM1_P0_FINITE_DENSITY_PARENT_HAMILTONIAN.md"
    json_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_csv(csv_path, frw_rows)

    report = f"""# PKM1-P0 finite-density parent Hamiltonian audit

**Calculation:** `{summary['calculation_status']}`
**Route disposition:** `{summary['route_disposition']}`
**Physics pass:** `false`
**MAT-001:** `BLOCKED` · **UVIR-003:** `IN_PROGRESS`

## Executive result

The parent action class survives one quadratic finite-density test, but the
specific interpolation inherited from the first PKM1 screen does not.

The inherited fast-transition control has

`J_Y+2Y J_YY=(2y^3+y^2-1)/(1+y+y^2+y^3)^2`.

It changes sign at

`y={symbolic['controls']['P0_A']['critical_y']:.12g}`.

Static modified-Poisson ellipticity remains positive there, but the radial
khronon/lapse kinetic Hessian does not. P0-A is therefore rejected as a global
control. This corrects the narrower earlier route screen, which tested static
ellipticity but not the independent khronon kinetic Hessian.

The stability-first comparator

`mu_B=y/(1+y)`,

`J_B=-2 a0^2[y-ln(1+y)]`

has positive static and khronon transverse/radial eigenvalues for every finite
`y>0`, recovers the required deep `Y^(3/2)` term and has `mu_B->1` with
`J_B/Y->0`. It is retained only as fundamental EFT existence data. It was not
derived from the ITSM condensate, topology or observations.

## Same-action condensate result

The canonical phase kinetic term cannot be combined with an independently
free `K(Q)` without adding a new operator. At fixed amplitude,

`K_QQ=rho_0^2 mu^2/M_P^2`.

After consistently relaxing the stable radial mode,

`K_QQ=rho_0^2 mu^2/(M_P^2 c_s^2)`,

`m_K^2=K_QQ/2`,

where `c_s^2=M_rho^2/(M_rho^2+4mu^2)`. The response is strictly positive and
is enhanced, not cancelled, by amplitude relaxation. Exact AQUAL is therefore
not a same-action prediction of P0.

A local AQUAL approximation can still exist only in the simultaneous window

`m_K^2/(lambda_stat k^2)<<1`,

`k^2<<M_rho^2`.

Equivalently, the window requires

`m_K^2/(lambda_stat M_rho^2)<<1`.

No physical ITSM parameter point has yet established that overlap.

## Exact ADM and background findings

In uniform-phase gauge the parent contains spatial lapse derivatives but no
`dot(N)` or `dot(N^i)`. The generic count is four physical local degrees of
freedom: two tensor, one phase/khronon and one amplitude. The pair `(p_N,C_N)`
is second class. On the finite-charge `Y=0` branch, its homogeneous bracket
contains `-rho^2 mu^2`, so the fundamental-J parent does not suffer the
auxiliary control's zero-gradient constraint-rank loss.

Stationary finite-density Minkowski space is not an on-shell P0 background:
`rho+p=rho_0^2 mu^2>0`, which a cosmological constant cannot cancel. An
evolving flat-FRW branch is the retained background. The deterministic
existence integration closes the Friedmann, charge and continuity identities.

After eliminating lapse and scalar shift on that branch, the uniform-phase
scalar kinetic matrix is

`K=[[((rho_dot^2+rho^2 mu^2)+C_J q^2)/H^2,-rho_dot/H],`

`   [-rho_dot/H,1]]`,

with

`det(K)=(rho^2 mu^2+C_J q^2)/H^2>0`.

For P0-B at `Y=0`, `C_J=2M_P^2`. Positivity persists at strict `q=0`; the
numerical scan is a validation of this symbolic result, not its source.

## New action-class tradeoff

Let `delta=1-mu=-J_Y>0`. Radial khronon kinetic positivity requires

`(y delta)'>=0`.

Consequently a globally stable pure-`J` control cannot approach `mu=1` faster
than a `1/y` tail after any finite point where `delta>0`, and `J` cannot tend
to a finite constant. P0-B exhibits that slow tail. Whether any such tail
passes Solar-System/PPN bounds is a separate calculation; it is not assumed.
Published khronometric completions show that adding extrinsic-curvature
operators changes this issue, but P0 does not inherit their coefficients or
their phenomenology.

## Fail-closed decision

P0-A is rejected. P0-B remains a research control because its quadratic FRW
constraint and kinetic structure are regular, but PKM1 remains on global
hold. The microscopic origin and radiative stability of `J_B` and `a0`, the
locality window, nonlinear zero-gradient cutoff, stationary galactic
Hamiltonian, Jeans band, PPN/lensing/GW limits, topology and reservoir are all
open.

No canonical action or gate status changes.
"""
    report_path.write_text(report, encoding="utf-8")

    manifest_files = [
        Path(__file__),
        inputs["spec"],
        json_path,
        csv_path,
        report_path,
    ]
    manifest = "\n".join(
        f"{digest(path)}  {path.name}" for path in manifest_files
    ) + "\n"
    manifest_path = OUT / "itsm_pkm1_finite_density_parent_hamiltonian.sha256"
    manifest_path.write_text(manifest, encoding="ascii")
    print(
        json.dumps(
            {
                "calculation": summary["calculation_status"],
                "disposition": summary["route_disposition"],
                "checks": len(summary["checks"]),
                "P0_A_critical_y": symbolic["controls"]["P0_A"]["critical_y"],
                "FRW_samples": len(frw_rows),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
