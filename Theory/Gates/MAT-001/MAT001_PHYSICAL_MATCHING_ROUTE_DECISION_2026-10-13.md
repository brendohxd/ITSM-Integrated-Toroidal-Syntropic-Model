# MAT-001: physical matching target and route decision

Date: 13 October 2026. Result ID: `MAT001-MATCHING-ROUTE-2026-10-13`.
Owner: MAT-001 / Master Test 1 matching interface.
Claim: **Conditional route synthesis and coefficient-chart identities**.
Research execution: `PROCEED_PROVISIONALLY` for this synthesis and preparation
of an identifying matching proposal. Review: `DEFERRED`; `Rule9_cleared=false`.
`physics_pass=false`; `gate_effect=NONE`.

## 1. Decision

The current action class supplies a parameterized matter coupling, but does
not select its numerical value. The MAT R5 decision proves that independent
`C_m` and `K_Q` leave `V=C_m/sqrt(K_Q)` free. R4C1 likewise declares independent
`beta,K_Q,A,b`. Substituting their diagnostic family values computes a value
for that assumed family; it does not determine the ITSM coupling.

The useful next target is the physical matter response after constraints and
mode normalization. A microscopic matching calculation must supply both the
matter residue and the nonlinear force invariant. This is a route decision,
not a repeat of the already completed identifiability tests.

Two separable questions remain:

1. **Identification:** what action-level mechanism fixes the coupling or bounds
   it using independently specified physical input?
2. **Admissibility:** does the same candidate have a healthy constrained mode,
   controlled frequency/domain, and the required gravitational limits?

A parameterized residue can be calculated before numerical identification.
Its algebraic existence does not establish either question above.

## 2. Put the one-field target in a matter-defined chart

R4C1 defines `C(psi)=exp(beta psi)` and `gtilde=C^2 g`. Work first on the
declared positive-beta branch, with constant finite `beta>0`, `K_Q,A,b>0`,
signature `(-+++)`, and `c=hbar=1`. Define a field chart, not an extra field:

```text
theta_m = ln C = beta psi
K_theta = K_Q/beta^2
A_theta = A/beta^3
b_theta = b/beta^2
```

The subscript distinguishes this `theta_m` from the condensate phase `Theta`.
Use the already eliminated regulator only in its permitted bulk/boundary
convention. Its force-sector action then reads

```text
L_force = K_theta (n.grad theta_m)^2/2
          - A_theta [h^(mu nu) grad_mu theta_m grad_nu theta_m]^(3/2)
          - b_theta (Delta theta_m)^2/2
gtilde = exp(2 theta_m) g.
```

The auxiliary formulation gives the same chart change if its field is also
transported as `z_theta=beta z`; its boundary convention is retained.
The chart has matter normalization fixed by the declared conformal factor.
It is invariant under the positive simultaneous rescaling
`psi -> s psi`, `beta -> beta/s`, `K_Q -> K_Q/s^2`,
`A -> A/s^3`, `b -> b/s^2`.

For an **isolated one-field** reduction with this time-kinetic term, the
existing orientation convention gives

```text
V_bare = beta/sqrt(K_Q) = 1/sqrt(K_theta)
g_can = -V_bare
lambda_force = A/K_Q^(3/2) = A_theta/K_theta^(3/2)
ell_force_sq = b/K_Q = b_theta/K_theta.
```

`V_bare` names the coefficient ratio; this report does not identify it with a
full coupled R4C1 physical-mode residue. The quantities have mass dimensions
`[theta_m]=0`, `[K_theta]=2`, `[A_theta]=1`, `[b_theta]=0`,
`[V_bare]=-1`, `[lambda_force]=-2`, `[ell_force_sq]=-2`.
Each action term has dimension four. A numerical dimensionful coupling needs
independent dimensional input as well as a mechanism selecting the relation.

On a negative-beta branch, the cubic coefficient is `A/abs(beta)^3`, while
the anchored signed residue must retain the sign of beta. At beta=0 this
chart is unavailable; use the original decoupled matter control. The
positive-beta formulas must not be extended through that singular chart.

This recasts the missing information precisely: **derive the temporal and
spatial response of the field which changes the matter metric**. Choosing a
normalization for the separate force scalar cannot supply that response.

## 3. The coupled matching target

The signed R4 contract, for its declared algebraic-constraint quadratic form,
requires

```text
A_eff = A_block - B C_block^(-1) B^T
c_eff = d - B C_block^(-1) h
g_can(u) = c_eff^T u / sqrt(u^T K_eff u).
```

Here `A_block` is a quadratic matrix, distinct from the cubic Wilson
coefficient `A`; `C_block` is a constraint matrix, distinct from the conformal
factor `C(psi)`. The physical-mode orientation must be transported with the
fields and source covectors. Require finite positive kinetic norm and
invertible constraints in the actual domain. Keep the signed vertex separate
from the source-source exchange coefficient, which involves its square.

For time-dependent or derivative-mixed reductions, derive the corresponding
reduced response operator from that action; do not assume the displayed
simple algebraic template covers every R4C1 sector. No live mode or pole has
been extracted in this report.

As an explanatory one-field matching interface, a particle action
`-integral m(q) ds` with canonical fluctuation `dchi=sqrt(Z) dq` has

```text
V_mass = d ln m/dchi = (d ln m/dq)/sqrt(Z)
L_src = -rho_b V_mass delta chi.
```

This assumes a local derivative-free mass dependence, a single normalized
mode, and a pressureless weak-field source. In the declared conformal chart
`m_E=m_0 C(psi)`, it reproduces `beta/sqrt(K_Q)` for the isolated force
block. It explains the required microscopic question, but does not supply
the function `m(q)`, its scale, or a universal Standard-Model coupling. The
full constrained source dressing remains required when the fields mix.

## 4. Existing routes and their actual disposition

| Route | Established boundary | Consequence for the next proposal |
|---|---|---|
| Bare normalization or `K_Q=1` | A field convention leaves the invariant residue free | Do not use it as identifying input |
| Condensate susceptibility alone | `psi` is a separate force field; R3 has no derived `S_Phi -> S_psi` kinetic match | Supply an explicit mode/operator bridge before equating phase susceptibility with `K_Q` |
| Minimal radial/heavy-mode portal | Live static radial source absent; tested derivative mixing gives a contact response; tested mass mixing gaps or retains free parameters | A different symmetry-protected completion must state what changes and survive the soft-source test |
| Scale compensator | `1/f` can express a candidate coupling but leaves a physical scale and full projection to determine | Derive or independently fix `f`, the background and mode overlap; preserve the quarantined T4/T5 sign/projection drafts |
| Direct source-pole method | M4 validates an invariant method; its live same-action inputs are incomplete | Use it to extract a supplied parent's response, not to turn assumed coefficients into predictions |
| Compact topology/homogeneous and linear data | R4C1 C2 does not select `A/K_Q^(3/2)` | Match the nonlinear coefficient separately |
| Reservoir/open-gravity literature | Provides construction and consistency methods | It supplies no selected numerical ITSM matter residue |

The current finite-density condensate and separate force field cannot be
identified by naming both excitations phonons. The action must show the
physical map, source coupling, background and retained mode content.

## 5. Concrete next calculation: screen one identifying parent mechanism

Before investing in another full reduction, a proposed microscopic matching
route must supply this small, reviewable calculation:

1. State the joint action/operators connecting the finite-density condensate,
   force mode and matter response, with the symmetry and physical scale or
   independently specified inputs that fix the relation. Declare the charge
   or chemical-potential ensemble and the finite-density background. New
   operators or fields belong to a separately declared candidate.
2. In its controlled soft/low-energy limit, derive a nonzero **static** matter
   source and the temporal quadratic coefficient in one chart. A purely
   `rho_b dot(pi)` vertex does not supply the required static source. Track
   possible extra modes and whether the intended force mode becomes massive.
3. Display the remaining independent parameters and vary them while holding
   the claimed matching inputs fixed. If an allowed continuous family changes
   the normalized residue, the route remains numerically underdetermined.
   A symbolic expression in unspecified parameters is a parameterized result.
4. If it survives identification, obtain the complete constrained quadratic
   source bundle and anchored physical-mode map from the **same** action.
   Check domain, positive kinetic norms, constraints and the physical window.
5. Match `A/K_Q^(3/2)` and the regulator ratio in that same route. Their
   values or bounds and domain must be compatible with the full theory.
   The canonical MAT/UVIR checklist still decides gate closure.

Success at the cheap screen means there is new identifying information and a
surviving calculation to perform. Failure means stop that numerical-prediction
route at its stated scope; it need not reject a parameterized EFT as a whole.
An independently measured/calibrated input may make an EFT predictive, but
must be labelled as such and must not be relabelled a first-principles constant.

The cheapest useful proposal is one that demonstrates its coefficient relation
and independent scale **before** a large stability computation. This report
does not select or instantiate a new parent. Matching proposal preparation
may proceed while the unchanged-action physical-domain investigation continues;
dependent physical weak-field or Stage-3 prediction work remains held.

## 6. Current boundary and review dependencies

The 13 October fixed-charge retarded V3 report states that its timing warning
survives the registered preparation change, no family receives physical GO,
and both identifying Stage-3 matching inputs remain absent. This is a bounded
reported result, not a universal no-go or a new calculation reproduced here.

Inherited review dependencies: MAT R4/R5; M4 and M2 controls; R4C1 action
freeze and C2 periodic-identifiability work; `R9-MT1-FIXED-CHARGE-RETARDED-V1`
and its transitive dependencies insofar as its reported current disposition
is used. All remain DEFERRED, not independently cleared.

Substantive blockers for a numerical physical residue: identifying microscopic
or independently justified matching input, a live healthy constrained mode,
admitted physical domain, and compatible nonlinear-force matching. Those are
not review-only holds. No blocker prevents this bounded route synthesis.

```text
review_status=DEFERRED
Rule9_cleared=false
research_execution=PROCEED_PROVISIONALLY (route synthesis only)
numerical_matching_execution=HOLD_SUBSTANTIVE
canonical_Tests_1_3=HOLD_SUBSTANTIVE
MAT-001=BLOCKED
UVIR-003=IN_PROGRESS
K_Q=NOT_DERIVED
V=NOT_COMPUTED
Stage4A=CLOSED
physics_pass=false
gate_effect=NONE
```

## 7. Evidence and verification scope

The authority instructions, R4/R5, R4C1 action freeze, M2/M4 reports and
R5 pathway survey were read through EOF. Other cited long documents were
read at their specific matching/status sections. Hashes below identify the
versions used; they do not certify the reports' scientific conclusions or
their transitive numerical receipts. No upstream numerical pipeline was
rerun. The coefficient-chart and mass-response equations are explicit
algebraic consequences with assumptions given above; they are not a new
physical-mode calculation. No old audit is counted as a new scientific test.

Local SymPy 1.14.0 checked the positive-beta chart transformations, invariant
ratios, logarithmic conformal-mass derivative and displayed mass dimensions
exactly; the command exited zero. The private optimizer output artifact is
`.local/itsm-context/output-83e62c1c7be24502ad47456f5abe3aca.txt`, SHA-256
`5ec9c3dc3ea25fefa1ad4d5be19dd6e535809e18867a561ce0852a90c539ce11`.
This is algebra verification only and supplies no independent scientific review
or numerical matching input. The output log remains ignored and local.

| Source (repository relative) | SHA-256 |
|---|---|
| `GEMINI.md` | `5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12` |
| `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md` | `d6195c4e4472c5473e43246e583dbb3f648bdf5a47740d44845fb9cc854250fa` |
| `Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md` | `3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809` |
| `Theory/Core/ITSM_GOAL_ROUTE_UPDATE_2026-10-09.md` | `76858ec29fec00d730cad2857b3a4982714e3798aa70ad6a92389fa038604ba5` |
| `Theory/Gates/MAT-001/MAT-001_R5_MICROSCOPIC_MATCHING_DECISION.md` | `ab8e743913f2e4fd0f5823581514345d598b2d1a1eb92e6d0d04f57447ed69b4` |
| `Theory/Gates/MAT-001/MAT-001_R4_SIGNED_RESIDUE_CONTRACT.md` | `63be12f8eaf36745c3c3c249cbb15a266de08fa1ceecc1e069512d5729345386` |
| `Theory/Gates/MAT-001/MAT-001_R2_DIRECT_RESIDUE_AUDIT.md` | `50e151c90abceca81bda237d36b268134bcd7748c8299ddacd213413a262fd15` |
| `Theory/Gates/MAT-001/MAT-001_R5_PATHWAY_SURVEY_2026-08-07.md` | `35114b8a319866fb8241af6528c6178a6f3b5dea0da60ad19032c967d179151a` |
| `Theory/Gates/MAT-001/R5_P1_T4_BACKGROUND_EQUATIONS.md` | `1cf776eb69fb1faed0298bd7514f86dd5834c0440223842e1c5aa1e9203d6a97` |
| `Theory/Gates/MAT-001/R5_P1_T5_SIGNED_RESIDUE.md` | `2cf597507194180d075e9dcb2a3843e2dc13947a574eed879d5f3f8a6e601e3e` |
| `Analysis/MAT/MAT-001/M4_INVARIANT_RESIDUE/outputs/MAT-001_M4_INVARIANT_RESIDUE_CONTROL.md` | `f836bbc0774b9d132b8c600cbb9c4db4dbb263b3ea063848c649b51c26457a01` |
| `Analysis/MAT/MAT-001/M2_RADIAL_MATCHING/outputs/MAT-001_M2_RADIAL_HEAVY_REDUCTION.md` | `2122fc7658b248d77042bffd852ceb99a8e3fac76c71e0fede505d38520e7673` |
| `Theory/Gates/UVIR-003/UVIR-003_STAGE_B_R3_UV_RESIDUE_AUDIT.md` | `23c6a5311c706f031801a0f24aa55b0721a756683f5bf98bf879ff12341839dc` |
| `Theory/Core/ITSM_Core_Architecture.md` | `332489b09476a4403e8bbebe81b3ff329a114005daa1cf39e8b4738f95b9ac8a` |
| `Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md` | `81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3` |
| `Theory/Gates/RES-001/RES001_R4C1_PERIODIC_IDENTIFIABILITY_REPORT_2026-09-29.md` | `2a861c556d3bae3dc20f1d85c4b7cbf21681188147d3f91b07bc4a5164183d5f` |
| `Theory/Core/ITSM_DUST_GR_WEAKFIELD_STAGE_DISPOSITION_2026-10-11.md` | `c62cca1052c5e3c2faac60871de31e71730af2b3360c3c22e4f312846de6ea9a` |
| `Theory/Gates/RES-001/RES001_R4C1_FIXED_CHARGE_RETARDED_V3_REPORT_2026-10-13.md` | `002011c7c9092bca3de1f16797adab3cbbf4932665544ea6cfcad969dad24225` |

The ITSM memory skill supplied continuity and authority guidance; its live
vault was empty and supplied no scientific evidence. The standalone context
optimizer was active for local reads; no billed-token savings are asserted.
