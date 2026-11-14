# Actual constraint momentum lift: controlled H1 remainder

4 November 2026. High acknowledged for the actual-rate bundle. Component
of RES001_RTAU_ACTUAL_RATE_ASSEMBLY_V1_SPEC_2026-11-04.md, following the
[strong reconstruction bundle](RES001_RTAU_STRONG_RECONSTRUCTION_BUNDLE_V1_REPORT_2026-11-04.md).
R-tau UNADOPTED; review DEFERRED; physics_pass=false; gate_effect=NONE.
Original R4C1 and all G1-G6 requirements remain unchanged and incomplete.

## Result

The three eliminated metric momenta now have an explicit local leading
lift from the free frame momenta, with H1-controlled remainders. This gives
the derivative information needed when composing the actual canonical rates;
an L2 bound for the eliminated momenta alone would not supply it.

This is an initial constraint-map estimate, not the assembled generator,
its full remainder, an evolving constraint theorem or a background time tube.

## Exact reconstruction and retained constants

At the actual conformal initial metric put

    m_x=m_y=a^2, m_z=2*a^2, u_i=1/m_i, ell_i=Vz/m_i,
    K_i(delta q)=delta B_i^T*p_background,
    rho=delta p.q_background,z+p_background.delta q_z.

The full canonical momentum tangent is exactly

    D_z(m_i*delta p_elim,i-Vz*delta p_frame,i+K_i(delta q))
        =delta_iz*rho.

This retains the variation of the field-dependent generator B. In the
original field ordering, the nonzero K entries are

    K_x=p_hxz*dq_hxx+p_hyz*dq_hxy+2*p_hzz*dq_hxz-p_Vx*dq_Vz,
    K_y=p_hxz*dq_hxy+p_hyz*dq_hyy+2*p_hzz*dq_hyz-p_Vy*dq_Vz,
    K_z=p_hxz*dq_hxz+p_hyz*dq_hyz+2*p_hzz*dq_hzz-p_Vz*dq_Vz.

For already compatible data, mean(rho)=0. With the original mean-free
periodic primitive P, the exact remainders are

    R_i=delta p_elim,i-ell_i*delta p_frame,i
       =-u_i*K_i(delta q)+delta_iz*u_i*P(rho)+u_i*C_i,
    C_i=[eta_i-mean(ell_i*delta p_frame,i)
                +mean(u_i*K_i(delta q))-delta_iz*mean(u_i*P(rho))]
         /mean(u_i).

eta_i is the retained original-coordinate mean of delta p_elim,i. Thus the
weighted constant is solved from its actual mean; it is not set to zero.
The original longitudinal compatibility and both global charge conditions
remain required. These formulas do not admit arbitrary input tuples.

## Continuum bounds

Write Qc=||delta q_13||H1, Pc=||delta p_13||L2, and let

    k0_i=||K_i||infinity, k1_i=||D_z K_i||infinity,
    u0_i=||u_i||infinity, u1_i=||D_z u_i||infinity,
    U_i=u0_i+u1_i, d_i=1/inf(u_i), e_i=||ell_i||infinity,
    p0=||p_background||infinity, q1=||q_background,z||infinity.

All vector/matrix norms use the registered Euclidean coordinate convention.
The cached background momentum and its spatial derivative bound k0,k1.
The certified profiles give positive inf(u_i) and the u/ell bounds. No
new Hessian is evaluated and no derivative of a certification radius is used.

The product rule and the all-integer-mode bound ||P||L2->H1<=sqrt(2) give

    ||rho||L2 <=q1*Pc+p0*Qc,
    |C_i| <=d_i*(|eta_i|+e_i*Pc+u0_i*k0_i*Qc
                               +delta_iz*u0_i*||rho||L2),
    ||R_i||H1 <=U_i*((k0_i+k1_i)*Qc
                               +delta_iz*sqrt(2)*||rho||L2+|C_i|).

These estimates never differentiate an arbitrary L2 momentum. The preceding
strong reconstruction provides explicit Qc and Pc bounds in its eight-input
norm, including the force mean and all three eliminated-momentum means.
The receipt composes them into three eight-column H1 remainder bounds and
records every binary outward constant, together with the full Qc/Pc lift.
The estimates cover the entire original circle and certified initial-root
ball; no physical mode, parity or tail is removed.

## Evidence and continuation

[Executable](../../../Analysis/MasterTests/test_rtau_momentum_rate_lift_v1.py),
[frozen criteria](RES001_RTAU_MOMENTUM_RATE_LIFT_V1_SPEC_2026-11-04.md),
and [receipt](../../../Analysis/MasterTests/outputs/rtau_momentum_rate_lift_v1_20261104/receipt.json).
11/11 same-author component controls pass. Controls include exact variable-
coefficient constraint and weighted-constant identities, a nonconstant
nonzero-mean fixture and the all-frequency primitive inequality. Omitting
the leading frame-momentum lift produces unbounded H1 growth in an exact
constant-coefficient Fourier control. This is not independent Rule-9 review.
Immutable replay is recorded in the continuation handoff after execution.

NEXT within the acknowledged-High rate bundle: combine this momentum lift
and the previous metric-gradient remainder with the actual Legendre inverse,
paired corrective gauge and coordinate transport. Derive the field/velocity
rate remainder in the same strong variables, then the momentum/force rows
and moving-map connection. No completed reconstruction is to be repeated as
a substitute for that rate calculation. The full actual-generator remainder,
T_dot/H_dot, evolving domain and physical window remain OPEN.
No action adoption, matching input, paper/site promotion, vault write,
model dispatch, Git delivery or publication follows from this component.
