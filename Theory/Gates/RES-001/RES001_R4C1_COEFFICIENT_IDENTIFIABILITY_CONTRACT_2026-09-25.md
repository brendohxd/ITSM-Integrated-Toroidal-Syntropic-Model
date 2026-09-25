# R4C1-C1: current-action acceleration-coefficient identifiability

Date: 2026-09-25. Frozen before the executable. Owner: Master Test 3,
with conditional Test-2 normalization checks. Action R4C1-v1 is unchanged.
Gate effect NONE; this is not a coefficient selection or observational fit.

## Question and authority

Does the homogeneous action-derived background, its interface currents,
and its classical linear equations determine the spatial force coefficient?
Test the specific possible degeneracy A -> lambda A, lambda>0, with all
other action constants, initial data, topology and coordinate units fixed.
Do not reinterpret varying a physical coefficient as an unchanged action
under field redefinition. Do not assume these parameters are all viable.

Pin the immutable action and reviewed local implementation inputs:

- Action freeze: 81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3.
- Full variation executable: aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0.
- B1 background executable: 1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f.
- G1 GR-limit executable: 0730de78971da97345517477115ace91bd0b9c1c0ae0b136c07067854a38a710.

Here 'reviewed local' means inspected in this task, not independent peer
review or Rule-9 clearance. Historical reconstruction remains parked.
No paid review, model dispatch, commit, push or publication is authorized.

## Required derivations

1. Use the full normalized-projector variation, not only the reduced ODE's
   parameter list, to determine the A-dependence on the aligned homogeneous
   branch. Test the Lagrangian, metric and frame blocks, connection momentum,
   and force-field flux. Preserve both nonzero B1 exchange currents.
2. Analyze f(q)=A|q|^3 in the physical spatial gradient q, including its
   gradient and Hessian at q=0. Do not differentiate Y^(3/2) twice in Y and
   mistake a singular coordinate derivative for a divergent field Hessian.
   The normalized timelike chart is smooth; q=0 on the background. Determine
   whether the full pre-constraint quadratic action depends on A. Inference
   to reduced modes is conditional on a regular constraint reduction; no
   interacting stability, invertibility or third-order analyticity is assumed.
3. Under psi_new=sigma psi, sigma>0, derive the transformations of K_Q,A,b,
   beta and z. Check invariants A/K_Q^(3/2), b/K_Q and beta/sqrt(K_Q).
   Decide whether changing only A can be a pure chart rescaling.
4. At fixed T3 periods, use a nonzero periodic field probe psi=d cos(k x),
   k=2 pi n/L, integer n!=0. Integrate the cubic and regulator energies.
   Show any A-dependence is a bulk operator, not a discarded surface term.
   This is an off-shell probe, not a self-consistent galaxy/dust solution.
5. Directly vary the local static force action, retaining the regulator.
   In a separately declared spherical, regulator-subleading approximation,
   integrate the positive-beta, outward-positive-gradient branch. Derive
   its force normalization with all coefficients explicit. Keep G_static
   distinct from bare G. This does not establish that the approximation is
   physically available in B1, nor a global positive isolated source on T3.
6. Retain C_proj as unknown. Relate the conditional dynamic scale to
   C_proj^2 a0 and determine its sensitivity to A at fixed H and other inputs.
   For the registered comparator set 1, 2 pi, 1/(2 pi),
   sqrt(1-q_dec)/(2 pi), q_dec<1, test whether inserting a desired coefficient
   merely solves for an otherwise free A. Do not select any such value.
   No observed a0, H0, fitted data or external likelihood enters execution.

## Registered numerical control and rejection tests

Use B1 with A/A_B1=(1/4,1,4). All other inputs are unchanged. Integrate each
with DOP853, rtol=1e-11, atol=1e-13 on [0,4], and compare 801 common samples.
Require completion and finite states, normalized Friedmann residual and
charge/dust drift <1e-8, and maximum normalized trajectory/current difference
<1e-12. Record exact equality if obtained; it is expected from identical
equations, not a new independent validation of the integrator.

As a sensitivity control change K_Q to 4 K_Q at otherwise B1 inputs. Its
initial constraint fixes its own H. Require a nonzero trajectory difference
>1e-6, so identical A-runs are not explained by ignoring all parameter changes.
Retain analytic evidence as the basis of structural nonidentifiability.

Reject these mutations or interpretations:

- Replace Y^(3/2) by Y while claiming the same vanishing quadratic variation.
- Change A alone while claiming all canonically normalized couplings are fixed.
- Omit the factor three in the force flux variation.
- Hold the spherical force amplitude fixed while changing only A.
- Assume a third analytic Taylor vertex exists at zero spatial gradient.
- Infer unique C_chi from identical H(t), q_dec(t), charge or exchange currents.
- Claim physical viability, a predicted a0(z), fresh analyst blinding or
  completed Rule-9 review from these calculations.

Check pin rejection before receipt overwrite and reproducibility of the
receipt. Preserve all failure and unknown records; no thresholds are retuned.

## Interpretation limits

The strongest permitted conclusion is a classical structural degeneracy of
the specified background and linear equations, with a physical nonlinear
operator distinction and a conditional static-response consequence. It is
not an all-parent no-go, a nonlinear cosmological solution, renormalized
matching or evidence that every A admits a stable controlled EFT.
Quantum corrections, nonlinear backgrounds and microscopic matching could
break this degeneracy but are not supplied by this audit.

The analyst has prior exposure to historical coefficient and observational
context. This is target-independent algebra, not a genuinely fresh blind
derivation. A candidate result can therefore never clear that independent
review requirement by self-certification. Tests 1-3 remain incomplete unless
their actual requirement-level completion audit succeeds.

MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; Rule9 NOT_CLEARED; physics_pass=false; gate_effect=NONE.
