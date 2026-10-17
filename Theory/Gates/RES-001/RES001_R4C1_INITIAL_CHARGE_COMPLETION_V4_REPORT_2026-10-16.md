# R4C1 prepared initial data: higher-order charge and mean-constraint audit

16 October 2026. Master Test1 / RES-001 / unchanged-action Stage2.
Claim Conditional. Local validation392/392; exact read-only replay passed.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Answer and significance

The archived experiment fixes both global charges through quadratic order.
It is not already a complete nonlinear fixed-charge solution. This audit
identifies two next-order initial corrections on its declared slice, without
altering the experiment:

1. The explicit lift of the quadratic phase-velocity counter has an exact
   fourth-order U(1) charge defect. An exact charge-only phase completion
   exists on a stated nonsingular domain.
2. The existing nonanalytic force supplies a nonzero mean lapse source at
   order |e|^3. A necessary additional mean volume-velocity counter cancels
   the resulting dust-charge coefficient in the chosen initial recipe.

Thus these initial mean-charge equations show no obstruction at the orders
calculated. This is useful compatibility information, NOT a proof that the
prepared wave belongs to the full nonlinear fixed-charge constraint surface.
Neither charge cancellation nor a positive homogeneous kinetic block proves
stability at finite wavelength or a physical validity window.

## Inputs and restricted initial slice

Use the frozen25September R4C1 action, generic action-derived scalar/dust
currents, sealed affine rows, the G3N4 nonanalytic force-source export, complete
three-family maps and all18 archived initial events of fixed-charge retarded
attempt03. There are nine distinct family/eta points, duplicated by two solvers.
No new evolution or B1-specialized operator transplant was performed.

At the initial event: h_ij=a^2 delta_ij, uniform force/dust clocks, N=1,
u=R>0,v=0,u_dot=0, v_dot=d+e^2 c2 and frame boost V_y=e*cos(kz)/a.
The exact future unit normalization is retained. All three archived shift
components are included, including the nonzero second-harmonic longitudinal
shift in B1-frame/hierarchical and the archived third transverse shift.
Exact arbitrary-three-vector-shift identities prove that these initial
charges and Y do not depend on those shifts; they were not set to zero.

The lift is explicitly defined, not claimed to be a unique nonlinear
continuation of a finite perturbative jet. Regulator/multiplier coefficients
remain archived and unchanged; their complete higher-order constraint rows
have NOT been solved by this current calculation. Time scope is INITIAL only.

## Exact charge calculation and its domain

With sigma=zeta*R^2/2 and charges per coordinate cell volume (the full torus
integrals multiply by (2*pi)^3), direct Cartesian momentum differentiation
and a complete periodic average give

```text
Q0 = a^3 R d,
Q(e) = a^3 R (d+e^2 c2) (1-sigma e^2),
c2 = d sigma,
Q_lift(e)-Q0 = -Q0 sigma^2 e^4.
```

In the exact reference-unit eta recipe this defect is -eta^5 e^4/676.
This is a truncation effect of that explicit lift, not evidence that the
action violates its Noether identity. The archived floating coefficients
also have a small nonzero Q2 residual; both contributions are separately
recorded, not silently replaced by an exact rational recipe.

The exact charge-only completion and remainder are

```text
v_dot_complete = d/(1-sigma e^2),
v_dot_complete-d-d sigma e^2 = d sigma^2 e^4/(1-sigma e^2),
|remainder| <= 2 |d| sigma^2 |e|^4,  0<=sigma e^2<=1/2.
```

The local angular coefficient additionally requires
1-zeta*R^2*e^2>0: a positive averaged denominator alone is insufficient.
The pole, R=0, H=0 and eta=0 are excluded from their respective inversions.
This completion changes initial data. Its nonzero linear lapse contribution
at order e^4 is -d^2 sigma^2; other fourth-order sources have not been summed.
It is therefore NOT an all-constraint completion.

The literal coefficient lift has background global dust charge, apart from
the reported floating mean-density residual. It nevertheless lacks the
third-order mean lapse response described next. Do not conflate these two
statements into a claimed dust-charge violation by the action.

## Nonanalytic mean source and necessary additional counter

Independently varying the exact normalized-frame density, retaining the lapse
measure, agrees with the already sealed generic G3N4 source:

```text
L_cusp = -A a^3 |psi_dot e cos(kz)|^3 / N^2,
(1/a^3) dL_cusp/dN at N=1 = 2 A |psi_dot|^3 |e|^3 |cos(kz)|^3,
m3 = <|cos(kz)|^3> = 4/(3*pi).
```

The quadratic two-angle rule would give1/2 instead of4/(3*pi); it is rejected
for this source. This is a real directional |e|^3 calculation, not an ordinary
cubic Taylor vertex at Y=0. The spatially nonconstant source is retained.

Let M=M_cos2. The generic charge Jacobian for phase/volume-velocity counters is

```text
J = [[a^3 R, 0], [-a^3 d/C, 2 a^3 M H/C]],
det J = 2 a^6 R M H/C.
```

If the missing lapse source is absorbed into density while the old free
velocities are kept, its mean dust-charge coefficient is
P3_free=8 A a^3 |psi_dot|^3/(3*pi*C). Within the chosen slice the necessary NEW
initial counters and lapse-derived density coefficient are

```text
delta v_dot_3 = 0,
delta x_dot_3 = -4 A |psi_dot|^3/(3*pi*M*H),
epsilon_3(z) = (2 A |psi_dot|^3/C^4) (|cos(kz)|^3-m3).
```

These multiply |e|^3. They cancel the two integrated charge coefficients and
the mean lapse coefficient at this order. The nonconstant density is not
discarded. In the exact diagnostic eta scaling,
delta x_dot_3=-8 eta^(9/2)/(2625*pi*M*H). Dimensional checks give x_dot units
of inverse time: [A]=1,[psi_dot]=1,[M]=2,[H]=1; zeta*R^2 and e are dimensionless.
Reference-unit eta recipes are not microscopic predictions or cosmological
H0 measurements.

The new mean |e|^3 initial correction first feeds the retained transverse
response at degree4, while the phase e^4 correction first feeds it at degree5.
This perturbative grading does not recalculate an evolved observable. It
provides no mechanism to erase the archived cubic timing warning.

## Verification, provenance and preserved failures

Exact generic identities, independent80-digit full-period quadratures,
direct ADM current evaluations and both predeclared lapse finite-difference
steps pass. Controls use |e|=1/500,1/1000,1/2000, both signs and arbitrary
periodic angles, with all-angle lower bounds for initial density positivity.
These amplitudes are diagnostics, not a physical EFT window.

| Control | Observed value |
| --- | ---: |
| Initial physical-slice/velocity discrepancy against archive | 3.3333333333e-16 |
| Sealed affine charge/density normalized residual | 1.8908753187e-16 |
| Archived Q2 floating residual | 3.8461538462e-20 |
| Archived mean-density floating residual | 5.3290705182e-15 |
| Direct-current normalized identity error | 1.5080446662e-82 |
| Exact charge-only completion normalized error | 1.6218766067e-83 |
| Independent lapse finite-difference relative error | 2.0000000000e-12 |
| Lowest all-angle diagnostic density lower bound | 0.1997359315 |

392 checks include repeated case/amplitude controls, not392 independent
physical tests. Numerical agreement is not a certified nonlinear evolution
remainder or physical stability proof.

V1 did not parse; V2 failed two prerequisite identity assertions37/39 and
skipped numerics; V3 failed the overly narrow zero-shift slice379/391.
Their files, sidecars and any receipts are preserved. The V3 failures exposed
a real missing constraint-generated shift in the test, not bad archived data.
V4 explicitly retains it. All physical formulas are BYTE-IDENTICAL across
failed V2, failed V3 and accepted V4; tolerances and old data were not changed.

Accepted executable:
`Analysis/MasterTests/test_01_r4c1_initial_charge_completion_v4.py`.
Receipts:
`Analysis/MasterTests/outputs/r4c1_initial_charge_completion_attempt_04/`.
Exact read-only replay passed;347 source hashes and691 source/sidecar metadata
records were preserved. Three known historical sidecar absences are explicitly
inherited, not called verified.

| Artifact | SHA-256 |
| --- | --- |
| V4 executable | af22270b76b72d29a04bdfba366464bcc2482ec5f2e41f5ffe66061fee7f4020 |
| summary.json | 8e16a7c05b5f9ce9054b6f37726f715abccb2b78ab45507a8e97e7552e5cfa01 |
| formulas.json, identical V2/V3/V4 | b1f62daaebdb1602ccc20350669b22aeb601d7e8d8cccad4626e420e317bb6f3 |
| numerics.json | 37de8c682b1ebc57a61bf6840a94a3c890718eed549e02b5ca9fcd35589d9a6c |
| verification.json | 417b2d33499a0dffb8a3b876f6bd968855271ff8fdedbe851fe0e2b2f0d6ba7e |

## Disposition and next substantive question

R9-MT1-INITIAL-CHARGE-COMPLETION-V1: DEFERRED, not cleared. Inherit homogeneous
kinetic V3, fixed-charge retarded V3, charge/domain V5, G3N4 force coverage,
mean-mode energy, PLANAR-WWR and all transitive review debt. Memory packet
ctx_6a8acb95790fb45b62d7aa37 (source doc_df615eb9e73755dd46e1e4e2) supplied
continuity; current source files and hashes govern the calculation.

Substantive blockers within the stated INITIAL-order diagnostic:
NONE_WITHIN_STATED_SCOPE after arbitrary-shift correction, exact identities,
independent controls and replay. Provisional reuse is limited to that scope.

Complete nonlinear admission remains OPEN: the necessary higher-order data
must satisfy ALL local constraints in a declared canonical chart and evolve
without projection. Constrained finite-k energy/characteristics, quartic
dispersion, coupled interaction/error control, tensor/local gravity/healthy
GR and genuinely identifying matter/nonlinear-force matching are still required.
No family receives physical GO. No automatic TOP-X4 or new-parent switch.

Stage1 remains complete only in its registered linear B1 dust scope. Stage2
INCOMPLETE; Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 UNCHANGED; physics_pass=false; gate_effect=NONE; Rule9_cleared=false.
The native goal was reported paused at the start of this bounded user-approved
continuation; this report does not claim to have resumed or completed it.
No manuscript/PDF, runtime, model/provider, security setting, vault mutation,
publication, commit or push was performed.
