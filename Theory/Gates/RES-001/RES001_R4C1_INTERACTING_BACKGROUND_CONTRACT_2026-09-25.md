# R4C1-B1 interacting finite-charge background contract

Date: 2026-09-25. Candidate action: R4C1-v1, unchanged.
Owner: Master Test 1 / conditional RES-001 R2 candidate.
Status: `FROZEN_BACKGROUND_CONTROL`; gate effect: `NONE`.

## 1. Question and scope

Does the same fully varied classical R4C1 action admit an expanding,
finite-charge, interacting solution on I x T3? Check the independent metric
constraint, frame equation and energy balances, rather than projecting the
solution onto a constraint at every step. This is an existence/control test
at preregistered dimensionless inputs, not a calibrated cosmology, quantum
stress calculation, stability proof or canonical Test-1 pass.

Action SHA256: `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3`.
Full variation executable SHA256:
`aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0`.
These files must be unchanged. Do not replace their regulator, matter
coupling, current, portal allocation or frame with another model.

## 2. Registered homogeneous branch

Use ds^2=-N(t)^2 dt^2+a(t)^2 dx_i dx_i on a flat compact T3, coordinate
periods set to one in the reference mass units. All fields are spatially
homogeneous, with zero spatial winding. Set U=(1/N,0,0,0) only after using
the full variations to recover the frame equation and its multiplier.
Phi=(u+iv)/sqrt2 has nonzero temporal U(1) charge. Integrate u,v in Cartesian
variables; do not eliminate phase velocity using a preimposed charge law.

Alignment, Y and Delta psi vanish on this background, but psi(t) need not be
constant. Their homogeneous first variations must be checked consistently.
The auxiliary equation gives z=0. No higher analytic Taylor vertex of
Y^(3/2) at Y=0 or homogeneous scattering amplitude is inferred.

After lapse variation choose N=1. Retain H as an independent evolved variable.
Obtain lambda_U from the full vector equation. Derive the reduced lapse and
scale-factor equations and check against the full four-dimensional stresses.
Recover the frozen dust fields through tau_dot=exp(beta psi),
epsilon=rho_m exp(-4 beta psi), including their continuity equation.

## 3. Parameters and initial data fixed before execution

All numbers are dimensionless in one arbitrary reference mass unit; they
are not observed a0, H0, abundances or cosmological density parameters.

```
M_P^2=1, M_U^2=2/3,
(c1,c2,c3,c4)=(1/5,1/10,-1/5,1/20),
K_Q=3, A=2/7, b=5/11, zeta=1/13,
beta=2/5, g_r=3/7,
m^2=1, lambda_4=1/3, lambda_6=1/5, Lambda=2,
m_r^2=2, lambda_r=1/7, rho_Lambda=0.
```

This separate background parameter point deliberately has c1+c3=0 and
M_cos^2=M_P^2+M_U^2(c1+3c2+c3)/2=11/10. This is a declared diagnostic
choice, not derivation or observational fitting of these coefficients. The
earlier off-shell Ward probes had different arbitrary coefficients; their
results and inputs remain unchanged. No parameter adjustment is allowed
after observing this background's numerical outcome.

```
t_initial=0, t_final=4,
a=1, u=1, u_dot=0, v=0, v_dot=1,
r=1, r_dot=1/4, psi=0, psi_dot=1/5,
rho_m=1/5, tau=0.
```

Choose the positive initial H from the action-derived Friedmann constraint
once. Subsequently evolve Raychaudhuri; do not reset H from that constraint.
Initial comoving charge is one in the registered unit comoving volume.
Nonzero g_r,beta and initial velocities permit both exchange currents to be
nonzero. Positive or monotonic net throughput is not a pass requirement:
the frozen reservoir is reversible, not an irreversible source.

## 4. Verification and rejection conditions

1. Symbolically derive the background action with unfixed lapse. Check its
   lapse, scale-factor, scalar and dust equations. Independently insert the
   background into the previously varied full tensor equations to derive
   lambda_U, frame stress, force stress and all spatial vector equations.
2. Integrate with DOP853 at rtol=1e-8/atol=1e-10 (coarse), DOP853 at
   rtol=1e-11/atol=1e-13 (fine), and Radau at rtol=1e-11/atol=1e-13
   (different-method cross-check). Use dense output and no constraint
   projection. The time interval and initial fields must remain fixed.
3. Require completion, finite fields, a>0, H>0, rho_m>0, and u^2+v^2>1e-6
   throughout 801 common equally spaced output points. This sampled
   admissibility is not a proof against arbitrarily narrow unsampled events.
4. Require the fine normalized Friedmann residual and relative comoving
   charge/dust-integral drift each <1e-8. Normalize a metric residual by
   1+the absolute magnitudes of both sides; invariant drift by
   max(1,abs(initial invariant)). Record coarse and fine values separately.
5. Require max componentwise |fine-Radau|/(1+|fine|)<1e-8 and
   |fine-coarse|/(1+|fine|)<1e-6 on the common grid. The fine constraint
   residual must improve on the coarse result or both must be <1e-12.
6. Check the three sector balances using five-point centered finite
   differences of sampled energy densities, NOT derivatives supplied by the
   integration RHS. Compare grids with 201,401,801 samples. Require the
   finest normalized maximum residual <1e-7 and improvement by a factor of
   at least four from 201 to 801 samples, unless both are already <1e-9.
   Use the measured full frame stress in the plenum density and pressure.
7. Require max|Q_mp^0| and max|Q_syn^0| each >1e-5 to exclude a disguised
   zero-exchange solution. Independently verify scalar charge conservation;
   do not identify energy exchange with a condensate-number source.
8. Run a beta=g_r=0 control at otherwise identical field initial data,
   recalculating only its initial H from its own declared constraint. Both
   action-derived exchange currents must vanish. This is not pure GR because
   the uncoupled fields and frame still gravitate.
9. Negative controls: (a) perturb initial H by +1e-3 without changing any
   other datum; (b) flip only the reservoir portal force sign in the RHS.
   Each must fail the unchanged action-derived Friedmann audit with maximum
   normalized residual >1e-5. Do not repair the action or its diagnostics to
   accommodate these deliberately wrong runs.
10. Hash the frozen inputs, executable, machine receipt and fine trajectory.
    Preserve failures and report exact maxima, not just passing counts.

If any requirement fails, report the measured failure and investigate
implementation or route validity. Do not retune this preregistered point or
relax its thresholds to create a pass. No inference to globally stable,
observationally admissible or uniquely selected cosmology follows from a
successful local control.

## 5. Publication and goal boundary

A successful result would establish a numerical classical background control
for R4C1, beyond the previous zero-exchange Stage-B example. It would not
derive matching constants, irreversible thermodynamics, a BBN/Einstein-
Boltzmann prediction, healthy continuous GR recovery, or the physical
perturbation Hessian. Independent Rule-9 review remains outstanding.

The full Tests 1-3 goal stays open. No historical reconstruction, TOP-X4
change, canonical gate promotion or publication is authorized by this test.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; Rule9 NOT_CLEARED; physics_pass=false; gate_effect=NONE.
