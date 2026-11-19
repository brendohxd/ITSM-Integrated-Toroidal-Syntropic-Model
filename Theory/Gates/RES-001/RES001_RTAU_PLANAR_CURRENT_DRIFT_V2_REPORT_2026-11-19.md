# A09.2 actual initial coupled-current derivative

19 November 2026. Conditional initial-derivative component COMPLETE_SCOPED.
Actual nonlinear background/operator/energy persistence remains OPEN.
R-tau UNADOPTED; original R4C1 unchanged; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result and physical meaning

On the full registered initial circle and certified root ball, the actual
canonical Euler and chart jets give

    ||L_t(0)||_(H2 to L2) <102.128,
    ||G_t(0)||_(L2 to H2) <6536.191.

L is the corrected projected coupled trace/current operator of the preceding
V2 owner, and G its identified initial inverse with bound below 8. The
derivative includes the local action coefficients, eliminated momentum map,
weighted means, transported residual-profile rank term and coordinate drift.
The constants use the registered dimensionless time/norm convention; they
are not physical growth rates, measured accelerations or cutoff scales.

This completes the previously missing actual INITIAL coefficient-derivative
budget. It does not extend the 14 November initial energy estimate over an
interval. No physical stability or instability verdict, healthy GR limit,
matching value or action adoption follows. The scalar current map is not the
complete twenty-direction Cauchy generator or nonlinear energy evolution.

## Actual action data and derivatives used

Reuse the frozen initial q,q_z,q_t, clock lapse, auxiliary secondary first
tangent and the certified root's third spatial shift derivative. Evaluate
the unspecialized full action over the entire circle/root enclosure. With
the original fixed coordinate z,

    p_t=L_q-D L_d,
    D p_t=D L_q-D^2 L_d.

The auxiliary primary p_Z and its derivatives remain zero. Its Euler residual
encloses zero consistently with the analytic secondary relation. The physical
Zdot is retained from the owning construction. Zddot and the second spatial
coefficient of p_t are neither supplied nor used. Zero padding of those unused
Taylor coefficients is computational storage, not an assertion about a field.

The recomputed temporal Hessian M=L_vv on the thirteen nonauxiliary slots has
a successful whole-root interval preconditioner with contraction <0.011614.
It gives a conservative inverse infinity-norm bound <6.070655. Candidate
solutions are enclosed by this inverse bound times their interval residual.
The prior certified inverse bound is also retained as an available fallback,
but the new preconditioner is the tighter bound actually used. Temporal
invertibility does not establish a positive physical kinetic signature.

## Material representation avoids an unsupported shift-rate input

The canonical coefficient function can be evaluated by writing

    v=v_n+Lie_S q,
    L0(q,v_n,d)=L(q,v_n+Lie_S q,d,S).

The action's shift covariance makes L0 independent of the representation
parameter S. For its derivative that parameter may be frozen while the
ACTUAL canonical q_t,p_t are retained. This is not the physical condition
Sdot=0. Let T_S be the field-index part of Lie_S, and v=q_t the registered
initial field rate. Then

    L0_q=L_q+T_S^T p, L0_d=L_d+S^z p,
    (v_n)_t=M^-1[p_t-L_vq v-L_vd Dv]-Lie_S v.

This is the derivative of the canonical normal-rate function along the actual
initial canonical jet. A possible physical shift derivative cancels. The
material gradient derivatives require only the actual second action
derivatives, the displayed rate, and the known canonical q_t,p_t. A large
third-action-derivative export is unnecessary.

For the explicit canonical lapse improvement F(q,d,p), its gradient rates are

    (F_xi)_t=sum_j F_xi,xj (q_t,d_t,p_t)_j.

Their first spatial coefficients retain p_t,z, d_t,z and all coefficient
gradients. Thus C0_t,C1_t,C2_t follow by differentiating the complete
canonical-density coefficient formulas of the current-operator V2 owner.
No regulator, frame, matter or mean term is removed.

## Trace direction and coordinate drift

Use the general Schur trace direction of the V2 operator. On the registered
initial metric its old-coordinate embedding has xx/yy entries a^2, all
other entries zero. Its first time tangent has the actual xx/yy metric rates.
This uses the conformal FIRST jet at that event, not future conformality.
All spatial derivatives of the embedding and its first time tangent remain.

For old-coordinate local coefficients A2,A1,A0 and zeta_z=J, zeta_t=J w,

    a2_new=J A2,
    a1_new=A1+A2 DlogJ,
    a0_new=A0/J.

At fixed new coordinate D_t=partial_t-w D_z, and J_t|new=J w_z. The required
initial coefficient derivatives are therefore

    a2_t=J[A2_t-w A2_z+w_z A2],
    a1_t=A1_t-w A1_z+(A2_t-w A2_z)DlogJ
                         +A2[w_zz+(DlogJ)w_z],
    a0_t=[A0_t-w A0_z-w_z A0]/J.

The independent geometric principal derivative agrees with these bounds:

    a2_t=a2_new[2*lambda_dot-mean_weighted(lambda_dot)
               -2*w*lambda_z-beta*(psi_dot-w*psi_z)].

The original initial map fixes its first chart jet w; no new residual origin
or harmonic history is selected. Other future coordinate histories require
their own transported coefficients and controls.

## Weighted nonlocal momentum component

Here T denotes the eliminated-momentum trace map of the 19 November current
operator, not the distinct cross normal form named T on 14 November. Keep
the old mean weights Omega=diag(1/J,1/J,1/J^2) and normalized residual profile
rP=1/J. Their initial time derivatives include J_t|new=J w_z. The term
P(rP)*mean(s f) and BOTH of its time derivatives are retained.

At the actual prepared metric the weighted normalization matrix is exactly

    N=diag(I0(2r),I0(2r),1/2), r=1/13000,
    ||N^-1||=2.

I0 denotes the modified Bessel function. This uses the transformed measure
and old mean definitions. It is not an ordinary new-chart mean or a new charge.
The canonical mean data are held as source coordinates while differentiating
the trace operator; this does not freeze their physical evolution.

The actual canonical Euler p_t and p_t,z, together with the paired field/
momentum-density coordinate transformation, bound U,U_t,s,s_t in the V2
trace-map formula. With alpha=||A||, alphat=||A_t||, omega=||Omega||,
omegat=||Omega_t||, nu=2, and

    d=||U||+(1+||P(rP)||)||s||,
    dt=||U_t||+(1+||P(rP)||)||s_t||+||P(rP_t)||||s||,

the complete sufficient bounds are

    ||T||<=alpha(1+nu*omega*alpha)d,
    ||T_t||<=(1+nu*omega*alpha)
              *[(alphat+alpha*nu*(omegat*alpha+omega*alphat))*d+alpha*dt].

The ordinary and nonlocal terms consequently give

    ||L_t||<=||a2_t||+||a1_t||/2+||a0_t||
                   +||Rvel_e,t||||T||+||Rvel_e||||T_t||.

Outward, conservatively rounded initial upper bounds are:

| Quantity | Bound |
|---|---:|
| a2_t | 0.820110 |
| a1_t | 0.130273 |
| a0_t | 10.961937 |
| eliminated normal metric rate Rvel_e | 1.740500 |
| its actual first time derivative | 3.053426 |
| momentum trace map T | 5.800587 |
| its full time derivative T_t | 41.694421 |
| full current operator derivative L_t | 102.127976 |
| initial inverse derivative G_t | 6536.190427 |

The receipt preserves binary interval endpoints and all subsidiary bounds,
including weight, normalizer, inverse-normalizer and residual-profile drift.
Every number is an upper bound with potential interval/triangle overestimation,
not a computed exact operator norm or observed physical rate.

## Persistence decision and next research question

The fixed-reference inverse margin would follow from an ACTUAL bound on
integral_0^t ||L_t(s)|| ds below 1/16, with the identified chart/range and the
remaining background/constraint/energy requirements preserved. An initial
derivative alone supplies none of those future estimates. Even if the same
conservative bound 102.128 were established uniformly, this particular
sufficient fixed-reference test would exhaust its margin near t=0.000612,
before the target 0.05. That hypothetical budget is not a certified lifetime,
an instability finding, or a prohibition on another justified continuation
argument or a recentered inverse estimate.

The unresolved work is now nonlinear background/domain persistence with the
actual mixed spatial regularity and continued energy/constraint reconstruction.
The new initial derivative budget can be reused; another inventory or isolated
initial cancellation would not complete that task. Derive a supporting
continuation/energy estimate or demonstrate a specific derivative/domain
obstruction. Do not evolve an unregistered finite Fourier truncation, prescribe
a coefficient history to pass the margin, assume future conformality, project
away physical modes, or adopt a new action merely because this is difficult.

## Evidence and provenance

[Contract](RES001_RTAU_PLANAR_CURRENT_DRIFT_V1_CONTRACT_2026-11-19.md);
[V2 correction](RES001_RTAU_PLANAR_CURRENT_DRIFT_V2_SPEC_2026-11-19.md);
[executable](../../../Analysis/MasterTests/test_rtau_planar_current_drift_v2.py);
[receipt](../../../Analysis/MasterTests/outputs/rtau_planar_current_drift_v2_20261119/receipt.json).
Main 19/19; 471 pins; SHA-256
`8cf441965c4f67a663c4845801be888c40f2bd1ed521e20eddc6401a9b64dc87`;
byte-identical replay. V1 passed 18/19 because its scalar identity compared
structurally different equivalent SymPy expressions. V2 compares their exact
difference with zero. Every numerical binary bound is identical to V1, whose
source and failed receipt remain intact and pinned. No tolerance was weakened.

[Separate audit](../../../Analysis/MasterTests/audit_rtau_planar_current_drift_v2.py);
[audit receipt](../../../Analysis/MasterTests/outputs/rtau_planar_current_drift_audit_v2_20261119/receipt.json).
15/15; 473 pins; SHA-256
`fce85723f75b76b1c6f7ec9429b7f22f2e286b33055d39328478bcfe8724662a`;
byte-identical replay. It independently checks two-field nonlinear-velocity
material identities, coordinate chain rules, weighted Bessel normalization,
the assembled interval budget and a counterexample to inferring future control
from an initial bound. It is not a second full action export or external
peer review. All original sources, sidecars and mtimes are preserved.

Provisional reuse is supported for these initial derivative enclosures under
their registered root/jet/chart assumptions. Inherit the corrected planar
current V2, planar gauge/momentum, canonical-density, temporal inverse,
certified higher jets, clock/auxiliary, initial-energy and symplectic/charge
review dependencies. Later review must examine the material parameter versus
physical shift distinction, missing-jet handling, weighted/profile drift,
interval inverse enclosure and the initial-versus-uniform estimate.

R-tau remains UNADOPTED; G1-G6 INCOMPLETE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED. Physical interactions/window, healthy GR
and identifying matching remain open. No manuscript/site edit, vault mutation,
provider dispatch, publication, commit or push.
