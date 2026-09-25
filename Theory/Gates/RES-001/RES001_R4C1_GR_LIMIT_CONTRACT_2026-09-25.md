# R4C1-G1: GR interpretation and perturbative-limit audit

Date: 2026-09-25. Action R4C1-v1 is unchanged. Gate effect: `NONE`.
Owner: Master Test 1; static normalization also informs Test 2.
Status: `FROZEN_LIMIT_AUDIT`, not a predicted physics pass.

## Questions and frozen inputs

Separate three logically different statements: vanishing exchange at fixed
frame coefficients; the exact algebraic endpoint in the action freeze; and
a continuous family of classical backgrounds/physical perturbations. A pass
of an algebra/implementation check is not a pass of any of these physical
claims. Reject false implications rather than adjusting the frozen action.

Pin these sources:

- R4C1 action: `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3`.
- Full variation executable: `aa62287597554b3292f9186c815d0f3b2bcb4c1e7496a52af1db07af6a857dd0`.
- B1 background executable: `1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f`.

The current canonical gates and complete Tests 1-3 objective remain open.
No TOP-X4, historical reconstruction, reviewer dispatch or publication work
is authorized by this contract.

## 1. Zero exchange is not an action-level GR limit

At beta=g_r=0 keep the frame coefficients of B1. For the isolated frame-
metric response control take Phi=r=0 and psi constant, so the extra scalar
sectors do not source linear metric/frame perturbations. Derive the static
Newtonian response directly from the full varied tensors and independently
from the reduced static action, not just by inserting a literature formula.

Use g_tt=-exp(2 phi), g_ij=exp(-2 chi) delta_ij, U=exp(-phi) partial_t.
Spatial sources represent quasistatic nonzero Fourier modes or local
linear response, not an isolated positive mass on a globally empty T3.
Enforce the compact zero-mode compatibility condition where appropriate.
This is not a static dust-equilibrium solution or the full PPN metric.

Compare the derived coupling to G_cos=1/(8 pi M_cos^2), already derived from
the action. Use alpha_i=(M_U^2/M_P^2)c_i when cross-checking literature, not
bare c_i. A reference is Oost, Mukohyama and Wang, arXiv:1802.04303v2,
equations (2.6) and (3.6): https://arxiv.org/html/1802.04303v2.
No observational bounds from that paper are being applied to R4C1 here.

Independently derive the homogeneous scalar charge-energy bound from sums
of squares. Distinguish a pure Einstein-dust background from GR with
separately conserved spectator scalar matter at nonzero charge.

## 2. Registered continuous family (eta labels solutions, not time)

For 0<eta<=1 use B1 parameters with

```
M_U^2 = eta (M_U^2)_B1,
(zeta,K_Q,A,b,g_r) = eta (zeta,K_Q,A,b,g_r)_B1,
beta = eta^2 beta_B1.
```

Keep M_P, all c_i, scalar mass/potential parameters and rho_Lambda fixed.
Initial data are B1 with u,v_dot,r,r_dot multiplied by sqrt(eta), and
psi_dot multiplied by eta; u_dot=v=psi=tau=0 still. Dust density and a remain
unchanged. Set initial H from this family's own constraint once, then
evolve without projection on t in [0,4]. Every member has separately
conserved initial charge eta. This is explicitly NOT a fixed-charge limit.
The beta scaling is declared so beta/K_Q tends to zero; no rate/coupling
is varied during an individual integration.

At eta=0 do not evaluate beta/K_Q or invert a vanishing kinetic matrix.
Compare against the separately defined exact Einstein-dust solution:

```
H_g = sqrt(rho_m(0)/(3 M_P^2)),
a_GR(t) = [1+(3/2)H_g t]^(2/3),
H_GR(t) = H_g/[1+(3/2)H_g t],
rho_m,GR(t) = rho_m(0)/a_GR(t)^3.
```

Run eta=(1,1/4,1/16,1/64,1/256,1/1024) using DOP853,
rtol=1e-11, atol=1e-13, and 801 common samples. Require all integrations to
finish, normalized Friedmann residual <1e-8, and drift of charge/dust
integrals normalized by max(1,abs(initial)) <1e-8. Compare a,H,rho_m to
the exact dust control with max |member-GR|/(1+|GR|). Require decreasing
sampled errors and a last-step error-reduction ratio between 2 and 6 for
the factor-four eta reduction. Record all values if these tests fail;
do not retune the family or reinterpret it as calibrated cosmology.

## 3. Physical transverse mode and canonical normalization

Derive the zero-scalar flat-background transverse quadratic action directly,
retaining the metric vector shift. Use N=1, gamma_ij=delta_ij, shift B_y(t,x),
and the exact unit parametrization

```
U^0=sqrt(1+w_y^2), U^y=w_y-B_y sqrt(1+w_y^2).
```

Set the spatial metric vector perturbation to zero by the usual transverse
spatial gauge. Retain its nondynamical shift, solve its constraint for a
nonzero wave number, and derive the physical kinetic/gradient coefficients.
Do not infer physical rank from a metric-frozen velocity block alone.
The zero Fourier mode and the scalar sector require separate treatment.

Track the actual kinetic coefficient and canonical field normalization as
eta approaches zero, not only a ratio called a mode speed. Compare the
canonical force-field coefficients under psi_c=sqrt(K_Q) psi. Retain the
exact nonanalytic |grad psi_c|^3 operator; do not call its coefficient a
verified scattering cutoff or analytic three-point vertex.

Reject these claims if contradicted: zero exchange implies GR; luminal
tensor propagation implies GR; a smooth background limit proves a uniformly
regular perturbation limit; and a bare c_i substitution is equivalent to the
required alpha_i normalization. Do not infer an all-path no-go from a rank
change or a divergence in the specifically registered canonical chart.

## Interpretation boundary

This audit may establish that a claimed GR shortcut is false, or that the
declared family has a smooth background limit but an unverified/nonuniform
perturbative limit. Neither outcome by itself rejects every R4C1 parameter
choice. The interacting B1 physical Hessian, scalar constraints, quantum/EFT
scale hierarchy and independent review remain required before viability.
Hash every output and record exact failure/success scopes. MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
Rule9 NOT_CLEARED; physics_pass=false; gate_effect=NONE.
