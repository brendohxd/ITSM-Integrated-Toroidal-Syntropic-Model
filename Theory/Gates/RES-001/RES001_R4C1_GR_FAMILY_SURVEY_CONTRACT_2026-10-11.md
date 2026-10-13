# R4C1 GR-family survey: bounded entry contract

Date: 11 October 2026. Version 1. Implements stage 2 of the approved
ITSM_DUST_GR_WEAKFIELD_EXECUTION_PLAN_2026-10-11.md. This entry is not
the full physical viability calculation or a new microscopic parent.

## Frozen families and declared scope

0<eta<=1; alpha_i=MU2*c_i/MP2; MP2=1, MU2=2 eta/3.
All families retain c1=1/5,c4=1/20 and hence alpha1=2 eta/15,
alpha14=eta/6. Archived G3: c2=-7/48,c3=-1/80. New B1-frame
continuation: c2=1/10,c3=-1/5. New hierarchical continuation:
c2=1/10,c3=-1/5+3 eta/16. Thus alpha13 is respectively eta/8,
0,eta^2/8, and alpha2 respectively -7 eta/72,eta/15,eta/15.
Use G3's frozen K_Q,b,zeta,g_r proportional-to-eta scalings,
A proportional to eta^(3/2), beta proportional to eta^2, and its exact
initial-data prescription (charge eta, not fixed nonzero charge).
No coordinate size, observed H0 or acceleration coefficient is fitted.

Reuse archived G3; do not rerun it as new work. For each NEW family,
integrate eta=(1,1/4,1/16,1/64,1/256,1/1024), t=[0,4],801 output
times, DOP853/Radau rtol=1e-11,atol=1e-13. Both methods must complete;
normalized state disagreement, Friedmann, charge and dust-integral drift
must each be <1e-8. No sampled time-balance claim is made without an
independent derivative calculation. Source coefficients remain constant
in time within each eta member. These are separate diagnostic families,
not parameter derivation or a repair of frozen B1/G1/G3 receipts.

## Unspecialized action and constraints

Use the generic complete R4C1 action Hessian in
Analysis/MasterTests/outputs/r4c1_g3n5_attempt_02/kernel.json, not
B1-evaluated matrices. Extract/rebuild its Fourier value/mixed/kinetic
blocks with generic constants before evaluating new backgrounds. Retain
all 22 source fields. Use the dust clock/norm/spatial gauge map with the
member's beta, not frozen B1 beta. Eliminate only the declared shift/Z
auxiliaries via the member-dependent inverse; never invert eta=0 or k=0
using a nonzero-mode inverse. Evaluate k=(20,40,80), t=(0,1,4) as snapshot
checks, with Hermiticity/auxiliary reconstruction normalized error <=1e-9.
Store full reduced matrices and all kinetic eigenvalues, including negative
values. A snapshot spectrum is not a uniform kinetic, gradient, causal,
hyperbolic, or physical-energy theorem. Mean mode is separately accounted
for without shift inversion. Missing full zero/constraint reduction remains
an explicit hold rather than an invented passing check.

Check the exact TT Hessian and vacuum vector/GR-normalization formulas,
finite-eta necessary signs, endpoint rank loss and canonical scalar ratios.
Retain unreduced generic auxiliary determinant and the distinct domains.

## External comparators frozen before evaluating new families

- GW170817 source: [Abbott et al., arXiv:1710.05834](https://arxiv.org/abs/1710.05834):
  conditional non-dispersive speed interval -3e-15 < c_T/c_EM-1 < 7e-16.
  Its source-emission/propagation assumptions and applicability in the
  actual derived physical frequency band must travel with any use.
- [Foster and Jacobson, gr-qc/0509083v2](https://arxiv.org/pdf/gr-qc/0509083),
  equations 10-11, and [Oost et al., 1802.04303v3](https://arxiv.org/pdf/1802.04303),
  equations 1.1-1.2: scalar-free Einstein-aether preferred-frame comparators,
  alpha_PPN1=-8(alpha3^2+alpha1 alpha4)/(2 alpha1-alpha1^2+alpha3^2),
  alpha_PPN2=alpha_PPN1/2-(alpha1+2alpha3-alpha4)
     *(2alpha1+3alpha2+alpha3+alpha4)/[(alpha13+alpha2)(2-alpha14)].
  Use their declared 2018 comparator bounds |alpha_PPN1|<=1e-4 and
  |alpha_PPN2|<=1e-7. These are frozen comparator thresholds, not a claim
  of the latest/full ITSM PPN likelihood, neutron-star sensitivities, or a
  substitute for the conformal matter/force calculation.
Use exact rational or cancellation-free expressions near eta=0. Do not
select eta to pass, calibrate a0, or call a comparator a full ITSM test.

## Physical decision and stopping condition

The entry receipts must explicitly distinguish these newly computed
necessary/snapshot results from outstanding finite-density physical
eigenstate interactions, complete characteristic/gradient domain, full
PPN, singular-domain continuation and controlled nonempty EFT band.
G3I's vacuum tree-amplitude scale is not the physical cutoff. A finite
canonical A/K_Q^(3/2) is not sufficient. Do not assume a higher ordinary
Taylor vertex for the unsmoothed Y^(3/2) interaction at Y=0.

GO requires the approved plan's full physical domain and GR evidence.
If essential physical-domain evidence is unresolved after this bounded
entry, output STOP_AND_ASSESS_DOMAIN_UNRESOLVED and request an explicit
continuation/action-selection decision. No family is admitted solely by
local checks. No automatic TOP-X4 pivot or dependent stage-3 prediction.

Outputs: formulas.json, diagnostics.json, matrices.json and summary.json,
with matching sidecars, immutable source pins and exact read-only replay.
Preserve every older failed/interrupted attempt and original sidecar.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
