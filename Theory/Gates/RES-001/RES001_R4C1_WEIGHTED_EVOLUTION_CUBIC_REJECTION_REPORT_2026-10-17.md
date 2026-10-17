# R4C1 weighted evolution: a rejected inverse, not an action rejection

17 October 2026. Master Test 1 / RES-001 / unchanged-action Stage 2.
Claim: Conditional. Local estimate: **FAIL, 37/38 exact construction checks**.
The failed receipt reproduced exactly in read-only replay, including its failure.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result in plain language

The proposed full-state weighted estimate is NOT established. The first
registered exact case exposed an invalid matrix-inverse shortcut: its assumed
cubic identity is false when the complete evolving/dust terms are retained.
This is a mathematical obstruction to this particular proof construction,
not an observational rejection, a new ghost finding or an all-action no-go.

The calculation preserves useful partial structure: the positive principal
norm and its wave/dispersive skew identities pass in this case. But those
facts do not justify using a false inverse to obtain the full transformed
generator or an energy bound. Dependent interval and numerical evolution
controls were not admitted. The remaining eight registered cases have no
completed estimate from this attempt.

## Owning scope and exact failure

The 16 October finite-k V3 report owns the continuation. The new V1 contract
and V2-V4 addenda preserve the unchanged generic action and restrict the final
exact-case calculation to archived_G3, eta=1/4. It uses k=(0,0,ell), ell>0,
p=ell/a, T=0, alpha=-beta*Pi, nu=0, and the regular auxiliary reduction.
All ten complex coordinates/twenty evolution states and the local phase are
retained. No positive homogeneous fixed-charge ensemble is imposed locally.

The mixed-order balance uses p*h, ordinary-wave positions, Vlong,
p^2*Pi-i*p*psi_dot*Vlong, ordinary velocities, Vlong_dot, and
Pi_dot-i*psi_dot*Vlong_dot/p, with the full balance-map derivative.
The fast/nonfast commutator determines U. In this exact case

```text
g = -11*a^2/48000
T_fast = I + U/ell
proposed_inverse = I - U/(ell*(1-g/ell^2))
                       + U^2/(ell^2*(1-g/ell^2)).
```

That inverse requires U^3=g*U. The COMPLETE residual R=U^3-g*U is nonzero:

```text
R[9,3]  = 11*i*a^3*psi_dot*(60*H*psi_dot+rho_m)/2000
R[19,3] = -11*i*a^3*(60*H*psi_dot+rho_m)/1440000.
```

Indices are zero-based in the exported balanced twenty-state order, before
the subsequent wave-map transformation. Both nonzero entries connect the
retained longitudinal coordinate to fast regulator coordinates. All other
entries vanish. The artifact stores the full matrix, including its zero rows.
These terms cannot be deleted by calling the state slow or by dropping
background/dust contributions. On the registered positive H,psi_dot,rho_m
background they are not zero.

This inverse failure is exact, not a label mismatch or a failed tolerance.
The defect is R/[ell^3*(1-g/ell^2)] in the proposed product inverse. Independent
binary64 products at the unchanged archived initial event give:

| ell | infinity norm of T_fast*proposed_inverse-I |
| --- | ---: |
| 4 | 7.220295302550586e-6 |
| 80 | 9.025498071698508e-10 |

The exact identity matters: the ell=80 defect alone could fall below a 1e-9
sampled tolerance while still invalidating an exact proof. No acceptance
criterion was relaxed to admit it. Values use the inherited reference units
and basis; they are not physical cutoff scales or observational errors.

## What is and is not verified

37/38 construction identities/controls pass for this single exact case,
including the complete generic-action kinetic inverse, background balances,
mixed-order map, fast commutator, wave-map inverse, principal Q-skew identities,
positive diagonal-plus-rank-one norm structure and pre-inverse coefficient
reconstruction. The only failed check is generic_fast_cubic_inverse_identity.

The later proposed remainder export is preserved as a REJECTED construction,
not a valid complete transformed generator. It must not be reused for a
continuous-time estimate until a correct inverse and full coefficientwise
identity are established. No interval constant, useful growth bound, new
trajectory integration, nine-case estimate or physical window was obtained.

The wavenumber rescalings are changes of mathematical norm in the inherited
reference normalization. p has inverse-length dimension; balancing different
field/derivative orders does not introduce a physical matching scale. The
positive norm is not the instantaneous canonical Hamiltonian. Previous
negative trace energy, the wave-scale Jordan defect, singular eta=0 endpoint,
retarded timing warning and homogeneous-ensemble distinction remain intact.

## Compute history and preserved attempts

No computational interruption is presented as a mathematical pass:

1. V1 / weighted_evolution_attempt_01 was interrupted after more than ten
   minutes without a receipt. The optimizer buffered subprocess stdout.
2. The separate same-V1 diagnostic attempt02 located polynomial GCD work in
   acceleration-matrix construction and returned native 0xC0000005.
3. V2 / attempt03 bypassed that GCD representation but stopped at a syntactic
   Laurent-extraction limitation. Its ValueError receipt is preserved.
4. V3 / attempt04 added exact univariate Laurent extraction/reconstruction,
   then returned native 0xC0000005 during expression expansion.
5. V4 / attempt05 substituted each registered parameter case into the generic
   action before algebra, then returned native 0xC0000005 before completion.
6. A direct, isolated first-case check completed normally and exposed the
   cubic failure. The versioned rejection executable then recorded the full
   failed receipt and replayed it exactly, without periodic stack tracing.

The native crash causes are UNASSIGNED. Trace locations and different
invocation outcomes do not prove a cause. No library, interpreter, operating-
system, security, provider or model configuration was changed. Private traces
stay in the ignored local directory. All prior sources, attempts and sidecars
are retained; no earlier valid result was replaced or reclassified as failed.

## Reproducibility and provenance

Executable: Analysis/MasterTests/test_01_r4c1_weighted_cubic_rejection_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_weighted_cubic_rejection_attempt_01/.
Use the known itsm_env Python with -B, then the same command with --replay.
Both return exit 1 because the scientific estimate FAILED. Replay additionally
prints READ_ONLY_FAILED_RECEIPT_REPLAY_EXACT; it does not turn failure into PASS.

| Artifact | SHA-256 |
| --- | --- |
| Rejection executable | 022b5a0d4dc20a95de92f8cdebf9dc903e47412b0167a01bdc7cf3ee4d55c45a |
| Summary | aa3092b89e861a85a004552a74273574aec5df538bcb3f293e3c676f88c3e621 |
| Verification | a9759e3252e6af412934e42bdc65c67eda799c74d75cb9a61e0f20134008b64e |
| Complete cubic residual | 64083e1895a85d7bdf24dc411dbf46605a7ee1a4690ce09882a47e2e342dc4ed |
| Rejected construction formulas | 7637a4013838428d62b94bf854c6443713e82f5144901edb147a145f3c9278e3 |

401 source pins and 799 source/available-sidecar hash-size-mtime records were
preserved. Three inherited absent sidecars remain explicitly unverified.
Read-only replay preserved all output bytes, sidecars and metadata. These are
same-agent controls, not independent Rule-9 review. The private memory audit
was readable/valid; continuity retrieval doc_8c3e84738ae6c13527bdf731 refers to
the homogeneous fixed-charge kinetic report in this gate folder. Live source
hashes and the owning nonzero-mode report, not that older retrieval, govern.
No vault sync, proposal, mutation or admission was performed.

## Decision and next bounded route

R9-MT1-WEIGHTED-CUBIC-REJECTION-V1; review DEFERRED, not cleared. Inherit
THREE-FAMILY-FINITE-K-V3, CUSP3-EVOLUTION-V1, generic kernel/evolving reduction,
homogeneous fixed-charge kinetic V3 and all transitive review debt.

Stop this construction at the exact failed prerequisite. The next bounded
calculation is to determine the full minimal-polynomial/low-rank inverse of
I+U/ell, retaining its extra nonzero terms, and verify the complete transformed
generator BEFORE attempting an energy constant or carrying it to the other
cases. An extended inverse is a possible repair, not a proved result here.
No action change or automatic TOP-X4 pivot is warranted by this proof failure.

Stage1 remains complete only in its registered linear B1 dust scope. Stage2
INCOMPLETE; no family physical GO; Stage3 NOT_ENTERED. Tests1-3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 UNCHANGED. Full nonlinear/fixed-charge admission,
physical energy/window, healthy GR/local gravity and identifying matching
inputs remain missing independently of this rejected inverse.

Native goal remains paused. No publication, manuscript/PDF, website, commit
or push. Only the living queue and deferred-review register receive an
append-only checkpoint, with original bytes/digests retained privately.
