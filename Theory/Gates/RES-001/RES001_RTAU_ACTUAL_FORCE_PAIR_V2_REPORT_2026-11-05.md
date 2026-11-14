# Actual initial force-pair remainder with corrected Sigma reconstruction

5 November 2026. Conditional initial component of the domain-first goal and
the actual-generator remainder contract. The operator explicitly confirmed
High before this calculation. R-tau remains UNADOPTED; original R4C1 and
all G1-G6 requirements are unchanged. Rule-9 review remains DEFERRED.

## Result and scope

The actual initial auxiliary/force-momentum rows now have explicit L2
remainders relative to the registered variable-coefficient, 20-direction
principal operator. The calculation composes the corrected Sigma constraint
reconstruction with the complete force current, metric-dependent auxiliary
variation, coefficient time derivatives, material commutators and paired
gauge correction. Both directions of ordinary/force coupling remain present.

For U equal to the sum of the nine registered strong/global input norms,

    ||R_Z||L2 <= 5221 U,
    ||R_xi||L2 <= 30709 U.

These are conservative mathematical constants in the frozen benchmark's
original-coordinate norm. They are not physical couplings, cutoff scales,
growth rates, accuracy guarantees, or a numerical acceleration prediction.
The full input-wise constants and coefficient enclosures are in the receipt.
Large initial constants do not establish a useful finite-time estimate.

The independent density row, moving Green/range/charge maps, full coupled
generator, evolving-domain energy and t=0.05 tube remain OPEN. The result
does not establish stability, a physical validity window or action adoption.

## Fixed variables, background and current

Use chi=delta psi, xi=delta pi_psi and zeta=delta Z. The canonical momentum
is the original-coordinate density, not an assumed normal velocity. The
strong density coordinate is

    w=delta Sigma-c P xi-alpha D chi,
    Sigma=rho+e_force+b Z^2/2,
    I_total=M rho, I_other=M Sigma, M=N mu.

All original charge tangents, means, harmonic/modulus partners and compatible
range restrictions remain. The corrected lift V4 and new descendants are
used exclusively for numerical estimates. No held V2 reconstruction or its
old numerical descendant bounds are restored. Their bytes remain preserved.

The full force is f=K_Q*(gamma*p+Vz*s)^2/2-A*Y^(3/2), where p is proper
clock velocity and s=psi_z. All derivatives are on the registered Y>0 branch.
The action's positive temporal coefficient is m=(mu/N)*f_pp. Define

    aphi=1/m, vphi=N*f_ps/f_pp,
    kappa=a^-2, lambda=a_z/a, ell=kappa*lambda,
    d=b*M*kappa.

The exact current inherited from the other-sector lapse owner is

    pi_t=D(S*pi-M*f_s+d*D Z-2*beta*d*Z*s)
          +beta*M*(e_force-Sigma)-beta*L_reg,
    L_reg=b*M*Z^2/2-d*(D Z)*s+beta*d*Z*s^2.

Its entire variation is retained. The local regulator term changes the
first derivative coefficient to d_z-beta*d*s. It cannot be dropped while
retaining the regulator flux alone. The source is I_other/M, not total rho
relabeled as Sigma. The TOTAL clock momentum stays in the spatial constraint.

## Clock, metric and auxiliary assembly

Before paired gauge correction, the exact material clock row is

    chi_t-S D chi=aphi*xi-vphi*D chi+sum(B_j*delta q_j).

The lapse variation in B_psi and all metric/frame force Legendre derivatives
remain. B_j and their first two spatial derivatives are evaluated from the
closed full force and frozen spatial jets. Their values are independently
checked for consistency with the cached action Hessian; exact generic force
derivative identities establish their formula. The ordinary temporal block
does not mix with the clock velocity. The H1 raw-velocity estimate is applied
only to ordinary rows; the clock's xi derivatives stay in the force principal
block. No H1 estimate for an arbitrary L2 xi is assumed.

On the conformal INITIAL slice the full auxiliary variation is

    zeta=-kappa*D^2 chi-ell*D chi+sum(P_j*delta q_j+Q_j*D delta q_j),
    P_0=P_3=a^-4*lambda*s, P_5=a^-4*D s,
    Q_0=Q_3=-a^-4*s/2, Q_5=a^-4*s/2,

with other P_j,Q_j zero. Its coefficient time derivatives use the actual
registered initial metric and clock velocities, including spatial derivatives.
The initial conformal velocity identity is used at this instant only; no
future conformal solution, derivative of an error radius or new background
ansatz is imposed. A justified third background shift bound is reused.

Material differentiation includes the exact commutator of
-kappa D^2-ell D with S D. The full clock AND metric gauge variations cancel
their higher derivatives together and leave xi_gauge*D Z_bg. Omitting only
the metric part fails the independent gauge control. Original-coordinate
pullback bounds and the harmonic gauge input are included.

## Principal and remainder separation

The retained force self-block is

    zeta_t-S D zeta=-kappa*aphi*D^2 xi
       -(2*kappa*aphi_z+ell*aphi)*D xi-vphi*D zeta
       + ordinary-to-force first-derivative coupling + R_Z,
    xi_t-S D xi=d*D^2 zeta+(d_z-beta*d*s)*D zeta
                 -vphi*D xi+R_xi.

For D q=L Y18+R_q and v_raw=V_raw Y18+R_v, the reverse derivative
coupling has coefficient

    -kappa*B_ordinary*L+Q_aux*V_raw+vphi*Q_aux*L.

It remains principal, not hidden in an asserted bounded L2 remainder. Its
equivalence to the registered shift-Schur form uses the existing exact
canonical projection/Schur identities and

    V_raw=V_projected-B_gauge*shift_gradient,
    Q_aux*B_gauge=(0,0,kappa*s).

Raw ordinary velocities are used before the full paired gauge correction;
mixing projected metric velocities with an uncorrected clock row would lose
this cancellation. The existing full ordinary/force matrix, both zero-speed
directions and all torus tails remain. No slow-graph projection is made.

The momentum remainder contains the differentiated canonical force source,
regulator field/measure response, coefficient gradients, the corrected Sigma
source and local force Legendre variation. The auxiliary remainder contains
B_j,zz field terms, metric/momentum smoothing derivatives, raw ordinary
velocity remainders, coefficient time derivatives and material commutators.
The independent audit expands the COMPLETE current and auxiliary differential
identities, including these remainders, rather than checking only symbols.

## Reproducibility and preservation

Executables:

- Analysis/MasterTests/test_rtau_actual_force_pair_v2.py: 29/29 controls.
- Analysis/MasterTests/audit_rtau_actual_force_pair_v1.py: 18/18 controls.

Fresh receipts:

- Analysis/MasterTests/outputs/rtau_actual_force_pair_v2_20261105/receipt.json
- Analysis/MasterTests/outputs/rtau_actual_force_pair_audit_v1_20261105/receipt.json

Both packages completed byte-identical replay. The audit independently checks
the complete canonical-current and auxiliary decompositions, instantaneous
time-coefficient derivatives, force sum-of-squares identity, relevant
all-integer-frequency inequalities and outward rational rounding of the
uniform summaries. These are same-author controls, not independent Rule-9
clearance. Parent check counts and hashes do not establish physical closure.

V1 failed at mpmath interval-left multiplication of a spatial jet. The source,
specification, immediate hash and failure receipt remain unchanged. V2 uses
a commutative scalar/jet dispatcher; it does not change equations, precision,
coefficients, domains or acceptance criteria. No full action Hessian was rerun.
Original sources, sidecars, failed attempts and unrelated edits were preserved.

## Next supported calculation

Assemble the actual corrected-density row and its physical-variable map,
then moving Green/range and charge/gauge transport. Keep physical clock flow,
T_dot, H_dot and all applicable domain-persistence requirements. An initial
row bound is not proof that the compatible range persists under evolution.
Interactions/window, identifying matching and numerical weak-field prediction
remain incomplete. No new action, observational fit, publication, provider
dispatch, vault mutation, commit, push or deployment was performed.

physics_pass=false; gate_effect=NONE; G1-G6 INCOMPLETE.
