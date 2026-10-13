# R4C1: wider GR-family entry survey and physical-domain disposition

Date: 11 October 2026. Owner: Master Test 1 / conditional R4C1.
Local result: **310/310**, zero failed/unknown registered checks, exact
read-only scientific replay. **Stage 2 is NOT complete.**
Decision: **STOP_AND_ASSESS_DOMAIN_UNRESOLVED**. No physical family admitted.
This is a checked entry survey, not the missing full coupled-interaction,
physical-window or GR-limit proof. Review DEFERRED; physics_pass=false;
gate_effect=NONE; Rule9_cleared=false. Stage 3 has not been entered.

## 1. Families and new calculation

The [approved plan](../../Core/ITSM_DUST_GR_WEAKFIELD_EXECUTION_PLAN_2026-10-11.md)
retains the unchanged R4C1 action and archived G3. The two NEW families have
alpha1=2 eta/15, alpha14=eta/6. B1-frame continuation: alpha13=0,
alpha2=eta/15. Hierarchical continuation: alpha13=eta^2/8,alpha2=eta/15.
Both use G3's scalar scalings, including A proportional to eta^(3/2), and
its initial charge eta. Old G1's different cubic scaling is not repaired.

Each new family is integrated at six registered eta values, [0,4],801 times,
using DOP853/Radau at 1e-11/1e-13. All 24 integrations complete with finite
sampled fields and positive a,H,rho_m. Worst two-method normalized state
disagreement is 1.4912574081172593e-11. Worst recorded Friedmann/charge/dust
drift is 1.9365620218536606e-11. No independent finite-difference sector-balance
claim is added. The original G3 112/113 failure and refinement remain intact.

| New family | Normalized background error at eta=1 | At eta=1/1024 |
|---|---:|---:|
| B1-frame continuation | 0.8608207741981918 | 0.0014914419771830645 |
| Hierarchical continuation | 0.8151847213232006 | 0.0014914340719114952 |

Both errors decrease on the registered grid toward the Einstein-dust CONTROL.
This is finite-time background evidence, not uniform full-theory GR recovery.

## 2. Generic action, constraints and retained spectra

The complete unspecialized 22-field Hessian is evaluated using each member's
coefficients, background and beta-dependent clock/gauge map. No B1-evaluated
matrix is repurposed. Shift/Z elimination uses the member-dependent inverse
only for nonzero k. Mean mode omits shift inversion and eliminates Z separately.
The raw TT Hessian verifies K_TT=(MP2-MU2 c13)/2 and G_TT=MP2/(2a^2).

Full reduced A,R,K and auxiliary D/inverse matrices are retained at t=0,1,4
and coordinate modes 0,20,40,80: 144 snapshots. All 108 NONZERO-mode sampled
kinetic matrices have positive spectra, minimum eigenvalue
0.00016276041666666666. Every one of the 36 MEAN-mode snapshots contains
a negative kinetic eigenvalue, retained unfiltered. A snapshot sign is not
a complete physical energy-residue/ghost classification; the mean/global
constraint and fixed-charge treatment remain necessary. No all-time kinetic,
full gradient, characteristic or nonlinear stability theorem is supplied.

The exact coefficient formulas and generic inverse domains are in
[formulas.json](../../../Analysis/MasterTests/outputs/r4c1_gr_family_survey_attempt_01/formulas.json).
All families approach common Newton normalization and tensor principal cone
as eta approaches zero, but K_vector=eta/6 and K_Q=3 eta lose rank there.
No endpoint inverse or healthy continuous-limit claim is made.

In M_P reference units, A/K_Q^(3/2)=2 sqrt(3)/63 has mass dimension -2,
beta/sqrt(K_Q)=(2 sqrt(3)/15) eta^(3/2) has mass dimension -1,
and f_frame^2=(eta/6) M_P^2 has dimension 2. Finiteness of one scalar
invariant is not control of all canonical interactions. These are values
of assumed diagnostic parameters, NOT microscopic matching or predicted a0.

## 3. Frozen compatibility comparators, not full ITSM likelihoods

The non-dispersive [GW170817 source](https://arxiv.org/abs/1710.05834) and
scalar-free preferred-frame formulas from
[Foster/Jacobson](https://arxiv.org/pdf/gr-qc/0509083) and
[Oost et al.](https://arxiv.org/pdf/1802.04303) were fixed in the
pre-execution contract. Their assumptions and limited applicability remain.
Neither a full conformal-matter/force PPN calculation nor a latest combined
likelihood is claimed.

- B1-frame has luminal principal tensors at every sampled eta, but all six
  sampled points fail the declared scalar-free PPN comparator.
- Hierarchical points fail both declared comparators across the sample grid.
- The continuous families are NOT excluded by those sampled failures.
  Under the non-dispersive speed comparator, archived G3 requires roughly
  eta below 1.12e-14; hierarchical roughly below 1.0583e-7. Exact inequalities
  are exported. They are conditional restrictions, not selected parameters
  or evidence of a healthy tiny-eta physical window.

Nothing is fitted to observed acceleration or a Hubble target. Physical
frequency-band applicability, background redshift/propagation and complete
local-gravity predictions remain substantive. Review deferral is not why
these families lack physical admission.

## 4. Stop point and uncompleted obligations

The bounded entry checks do NOT compute the complete finite-density physical
eigenstate cubic/quartic interactions. G3I's fixed-metric vacuum amplitude
and shrinking order-one probe scale remain a warning, not a full physical
cutoff for these new families. Metric/matter mixing and constrained physical
amplitudes must determine whether that scale survives. The unsmoothed
Y^(3/2) force cannot be replaced by an unavailable ordinary third Taylor vertex.

Still missing: complete coupled gradients/characteristics and Cauchy domain;
zero/singular/fixed-charge endpoint reduction; full conformal-matter PPN;
and a controlled nonempty physical band incorporating quartic dispersion,
background scales and interactions. Therefore no GO condition is satisfied.
The operator-approved stop-and-assess condition applies. This is not an
all-action no-go, automatic TOP-X4 pivot or permission to enter a dependent
weak-field/numerical-coefficient prediction.

The next action-selection decision is whether to continue R4C1 with one
bounded COUPLED interaction/window calculation or select a different parent.
This entry does not autonomously adopt, tune or dispatch either route.

## 5. Reproducibility and preserved history

- [Contract](RES001_R4C1_GR_FAMILY_SURVEY_CONTRACT_2026-10-11.md):
  aa3a8ced3935b2ca0a8f72ee56bcf22a17049e4ff80b8f3e527113cdddeb29b1.
- [Executable v2](../../../Analysis/MasterTests/test_01_r4c1_gr_family_survey_v2.py):
  94361b3545770efdb1c4b3cbcf30e4a9c10064105f19e9dce5cd878239a7ed42.
- [Receipt](../../../Analysis/MasterTests/outputs/r4c1_gr_family_survey_attempt_01/summary.json):
  a41bd5979cc25b0afcbde50fa195882cc58ee95f8e0472867f63288e52354ecf.
- Generic kernel: cf30a7e334d154e492f8ca7bde92cf95754390b602f4914e5b6ba8fed90a74e3.

Use itsm_env Python -B with executable v2; --replay followed by
Analysis/MasterTests/outputs/r4c1_gr_family_survey_attempt_01 verifies exact
artifact/sidecar bytes. 417 original input/source/available-sidecar files
preserve hashes, sizes and mtimes through calculation. v1's NumPy boolean
JSON TypeError happened before receipt creation; source, sidecar and private
failure log remain. Only boolean export conversion changed for v2.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Review: R9-MT1-GR-FAMILY-SURVEY plus G1/G2/G3/S1/G3I, full generic
variation/G3N5 and inherited review, all DEFERRED. No canonical promotion.
