# R4C1: conditional four-dimensional reservoir candidate

Date: 2026-09-25. Version: R4C1-v1, frozen before its executable.
Authority: user approval to develop a separate 4D reservoir completion using
the current v12 fields. This is not adoption as the canonical parent.
Owner: Master Test 1 / RES-001 R2 exploratory action lane.
Status: `CONDITIONAL_ACTION_CANDIDATE`; gate effect: `NONE`.

## 1. Scope and provenance

Retain the recovery density/topology field Phi, independent constrained frame
U, separate force field psi, and Einstein metric. Add a neutral real reservoir
r with a U(1)-invariant potential interaction. This is a **closed, reversible,
classical field model**, not an irreversible bath, microscopic derivation,
Spohn calculation, condensate-number source, or accepted cosmology.

Operator sources, not claims of parent acceptance:

- `../UVIR-001/UVIR-001_GATE_REPORT.md`, section 2: canonical complex scalar
  and quartic/sextic potential. Its negative spatial-IR result is retained.
- `../UVIR-003/UVIR-003_STAGE_A_REPORT.md`: all four frame invariants,
  current alignment, and the conditional force sector.
- `../UVIR-003/UVIR-003_STAGE_B_TRACK_A_FORCE_ADM_CUBIC.md`: the subsequently
  selected projected-derivative regulator. Stage A's earlier undefined
  regulator is not used as though complete.
- `../../../Manuscript/CoreRecovery/sections/04_conservation_exchange.tex`:
  the conditional conformal matter metric and distinction between energy and
  charge exchange. No GKSL pump/rate is imported.
- `RES001_TIER1_CLAIM_AUDIT_AND_ULTRA_ENTRY_SPEC_2026-09-05.md`: R2 route
  requirements. This candidate does not satisfy its surviving-parent gate.

New choices are the reservoir potential/portal, an explicit irrotational
pressureless dust matter realization, and the normalized off-shell projector
below. They are assumptions to test, not deductions from the source papers.
Dust is a bounded physical matter model, not a Standard Model, radiation,
pressure, vortical-fluid or BBN completion. Relativistic fluid actions provide
background context ([Brown 1993](https://arxiv.org/abs/gr-qc/9304026)); the
specific action below is defined here and must be varied directly.

## 2. Fields, chart, domain, and boundaries

Signature (-+++), c=hbar=1, [coordinate]=-1. Spacetime is I x T3 with a
dynamical Lorentzian metric; no flat-space solution is presumed. Phi=(u+iv)/sqrt2,
s=u^2+v^2. Use Cartesian u,v in variations, including s=0. Smooth periodic
u,v allow winding; phase coordinates are used only where s>0.

Independent fields: g_mn, U^m, lambda_U, u, v, psi, r, dust proper-time scalar
tau, dust multiplier epsilon, and regulator auxiliary z. Constants are real.

Define, **before** imposing the multiplier equation,

```
ell = sqrt(-g_mn U^m U^n),    n^m = U^m/ell,
h^mn = g^mn + n^m n^n,       a^m = n^k nabla_k n^m,
theta = nabla_m n^m,
J_m = v partial_m u - u partial_m v,
Q = n^m partial_m psi,       Y = h^mn partial_m psi partial_n psi,
Delta psi = h^mn nabla_m nabla_n psi + theta Q
          = nabla_m(h^mn partial_n psi) - a^m partial_m psi.
```

The projected derivative acts on every tensor index. In a hypersurface-normal
frame, Delta is the intrinsic leaf Laplacian; on arbitrary timelike frames
the displayed covariant operator is the definition, not a claim of a global
foliation or a healthy vortical principal symbol. On the unit constraint n=U
and it reproduces the selected Track-A operator. Normalizing inside h, Q,
alignment and the regulator is an explicit off-shell extension; it must not
be silently substituted into other lanes' off-shell variation ledgers.

Work on smooth finite fields with future timelike U and ell bounded away from
zero. Then Y>=0 even off the unit constraint. First variations include Y=0;
higher Taylor vertices there are not asserted analytic. Do not normalize J,
divide by s, or extend the n chart to null U. Physical dust has epsilon>=0,
timelike tau gradient and no caustic in the patch; multiplier variation is
unrestricted before selecting that physical solution domain.

Mass dimensions:

| Quantity | Dimension |
|---|---|
| g, U, n, psi, beta, c_i, lambda_4, lambda_6, lambda_r, g_r | 0 |
| u, v, r, M_P, M_U, m, m_r, Lambda | 1 |
| tau | -1 |
| K_Q, z | 2 |
| A | 1 |
| b | 0 |
| zeta | -2 |
| epsilon, lambda_U, rho_Lambda | 4 |

psi is a dimensionless gravitational-potential chart, not a canonically
normalized mass-dimension-one scalar. b names the entire regulator
coefficient gamma/M_*^2; [gamma]=2 in this chart if that notation is used.
These are unit assignments, not values or matching of K_Q, A, b, or beta.
The field-rescaling-invariant physical couplings remain to be derived.

Take M_P,Lambda>0; m^2,m_r^2,lambda_4,lambda_r,g_r>=0; lambda_6>0;
K_Q,A,b,zeta>0 for the exploratory interior. The c_i remain unspecified real
constants, **not certified stable**. Exact-zero controls may lie on its
boundary. There is no observed a0, H0 or coefficient target in this action.

Use periodic spatial variations and fixed endpoint fields, or compactly
supported interior variations. Add the Einstein Gibbons-Hawking-York term
M_P^2 integral_boundary sqrt(|gamma|) sigma K, with outward unit normal,
sigma=normal^2 and K=gamma^mn nabla_m normal_n. Fix the boundary metric and
U,u,v,psi,r,tau,z. The multipliers have no derivatives. The first-order
auxiliary action below fixes the regulator's boundary convention; eliminating
z in the bulk is not permission to drop its induced surface term on a
different boundary-value problem.

## 3. Fully specified classical candidate action

S = integral sqrt(-g) [M_P^2 R/2 - rho_Lambda + L_P + L_R + L_m] + S_GHY.
There is no optional unspecified S_W or extra interaction in R4C1-v1.

```
V(s) = m^2 s/2 + lambda_4 s^2/8 + lambda_6 s^3/(24 Lambda^2),
V_R(r) = m_r^2 r^2/2 + lambda_r r^4/4,
W(s,r) = g_r s r^2/4,

L_P = -[(nabla u)^2+(nabla v)^2]/2 - V(s) - W(s,r)
      + L_U + L_align + L_force,

L_U = -M_U^2/2 [
  c1 (nabla_m U_n)(nabla^m U^n)
 +c2 (nabla_m U^m)^2
 +c3 (nabla_m U_n)(nabla^n U^m)
 -c4 (U^k nabla_k U_m)(U^l nabla_l U^m)]
 +lambda_U (U^2+1)/2,

L_align = -zeta h^mn J_m J_n/2,
L_force = K_Q Q^2/2 - A Y^(3/2)
          + b z^2/2 - b h^mn (partial_m z)(partial_n psi)
          - b z a^m partial_m psi,

L_R = -(nabla r)^2/2 - V_R(r),
C(psi) = exp(beta psi),     gtilde_mn = C^2 g_mn,
L_m = -epsilon [C^2 (nabla tau)^2 + C^4]/2.
```

L_m is exactly sqrt(-gtilde)/sqrt(-g) times
-epsilon [(nabla_tilde tau)^2+1]/2. It is not a current inserted into a
continuity equation. The portal belongs wholly to L_P in the baseline split.
No ordinary quadratic Y term is silently added. The absent operator's
radiative stability and all coupled constraint questions remain open.

For b>0, the auxiliary equation must give z=-Delta psi. Integrating by parts
then gives -b (Delta psi)^2/2 in the bulk. At b=0, omit this decoupled auxiliary
instead of dividing its equation by b. This parameter endpoint changes
constraint rank and is not a regularity result for the physical spectrum.

## 4. First checkpoint and rejection tests

First checkpoint: derive the u,v,r,psi,tau,epsilon,z equations; explicitly
vary the algebraic scalar/alignment stress blocks; derive the two interface
currents and the full U(1) current. This is not yet the all-sector metric and
frame-constraint audit required to pass Master Test 1.

Before claiming that checkpoint, test:

1. Action dimensions, dust constraint and matter trace variation.
2. Off-shell matter/reservoir Ward identities from their varied stresses,
   including the matter multiplier equation; wrong current signs rejected.
3. U(1) variation including the derivative-dependent alignment term on an
   inhomogeneous frame. Reject bare-J conservation as the general charge law.
4. Portal regularity at g_r=0 and s=0; beta=0 matter control; exact zero versus
   symbolic limit. No coupling, density, or charge division.
5. Interaction-stress reassignment: moving fraction eta of -W to L_R changes
   the named Q_syn while leaving the total action/stress unchanged.
6. Normalized-projector metric variation: vary U as an independent
   contravariant field and retain its metric-induced normalization change.
7. Auxiliary elimination sign, the acceleration term in Delta and its formal
   adjoint, and the flat-FRW intrinsic-Laplacian limit. Reject a covariant
   Hessian trace that omits theta Q and reject dropping the acceleration
   term outside a geodesic frame.
8. A declared GR endpoint and explicit rejection of 'zero exchange = pure GR'.

The operational **algebraic GR endpoint** sets beta=g_r=0,
M_U^2=zeta=K_Q=A=b=0, u=v=r=0, psi constant, lambda_U=0 and omits z.
The remaining metric/matter action is Einstein-dust with rho_Lambda. U has
no dynamical kinetic term at that endpoint. A healthy continuous GR limit
from finite-density, propagating-frame solutions is NOT presumed and must
remain a separate hold. At beta=g_r=0 alone the other sectors still gravitate.

## 5. Firewall and next obligation

This freeze permits only candidate calculations. It neither replaces the
canonical Test-1 entry contract nor changes TOP-X4. Full metric/frame
variation, coupled constraints, a finite-density on-shell background,
continuous GR recovery, hyperbolicity, quantum completion, matter extension,
and independent review are required before stronger claims. No net positive
entropy production or nonzero condensate-number source is stipulated.

```
candidate=R4C1-v1
candidate_status=CONDITIONAL
canonical_test_01_action_input_complete=false
canonical_source_vector_derived=false
full_metric_frame_variation_verified=false
finite_density_background_verified=false
continuous_healthy_GR_limit_verified=false
Rule9=NOT_CLEARED
K_Q=NOT_DERIVED
V=NOT_COMPUTED
Stage4A=CLOSED
MAT-001=BLOCKED
UVIR-003=IN_PROGRESS
physics_pass=false
gate_effect=NONE
```
