# Canonical conditioning: six finite spectra improve; physical window stays open

20 October 2026. Unchanged R4C1 action and complete retained-planar n17 matrices.

## Outcome

An invertible canonical momentum shear resolves the registered finite-spectrum
consistency checks for all six eta=1/4 cases: both node orientations in G3,
B1-frame and hierarchical families. These cases previously failed the complete
rescaling/matching checks. All twelve smaller-eta cases remain numerically
unresolved. No family is selected or admitted as a physical theory here.

All eighteen transformations pass their 162 algebra controls. Overall the new
calculation is **303/361, UNRESOLVED**. Its 58 failed assertions are 29 numerical
issues evaluated at each of two working precisions: 12 rescaling failures,
12 left/right conjugate matching failures and 5 left-residual failures, each
counted twice. Comparing 303/361 with the earlier 305/347 as if they measured
the same test set would be incorrect.

## What changed, and what did not

For the original, not forcibly symmetrized, quadratic form

    S=[[K,C],[B,M]], F=M^(-1)*B, L=(F+F^T)/2,
    T=[[I,0],[-L,I]], original_u=T*new_v,
    T^T*Omega_can*T=Omega_can, S_new=T^T*S*T.

Only the shear generator L is made symmetric, so T is canonical. Both actual
mixed blocks are retained; no assumption B=C^T or M=M^T replaces input data.
The remainder B-M*L is kept, including its non-removable mixed coupling. The
transformation is invertible and constant at the frozen slice: no mode, sign,
constraint correction, mean, drift term or zero direction is removed.

The frozen [contract](RES001_R4C1_CANONICAL_CONDITIONING_V1_CONTRACT_2026-10-20.md)
precedes the executable and receipts. Exact generic symbolic controls check
the block formula, canonical two-form and Hamiltonian similarity. Independent
small controls retain negative-energy, growing, zero and antisymmetric-mixed
examples and reject singular M. The execution/algebra smoke passes 51/51.
The initial two-case preflight remains 37/41; its numerical data and checks
were reproduced in the full run, not overwritten or renamed into success.

Block algebra is repeated independently at 80 and 100 working digits, before
calling the unchanged V3 NumPy/OpenBLAS full-spectrum evaluator. It still uses
binary64 eigensolving and the original 1e-8 residual / 1e-6 spectral-comparison
criteria. The input is the sealed eighty-digit numerical matrix; 100-digit
working arithmetic does not recreate a more accurate physical operator.

## Numerical evidence

Worst orientation for each diagnostic, using the 100-digit transformed form:

| Family | eta | Canonical-rescaling discrepancy | Left conjugate-match discrepancy |
| --- | --- | ---: | ---: |
| G3 | 1/4 | 1.104e-7 | 5.819e-8 |
| G3 | 1/64 | 4.551e-6 | 3.174e-6 |
| G3 | 1/1024 | 0.8186 | 0.8704 |
| B1-frame | 1/4 | 1.084e-7 | 8.941e-8 |
| B1-frame | 1/64 | 4.847e-6 | 2.637e-6 |
| B1-frame | 1/1024 | 0.7081 | 0.8569 |
| Hierarchical | 1/4 | 6.402e-7 | 4.229e-7 |
| Hierarchical | 1/64 | 2.822e-6 | 2.604e-6 |
| Hierarchical | 1/1024 | 0.7917 | 0.8116 |

The middle-eta errors improve substantially but still exceed 1e-6. The smallest
eta remains poorly resolved; improvement is not uniform and must not be assumed.
Both orientations in the smallest-eta G3 and hierarchical cases, and orientation0
in the smallest-eta B1 case, fail the left-residual check. Worst: 4.754e-8.

Maximum recorded transformation/mapping diagnostics over all eighteen cases:

| Diagnostic | Maximum |
| --- | ---: |
| Mixed solve residual, 80 digits | 1.730e-64 |
| Mixed solve residual, 100 digits | 1.021e-84 |
| Shear-generator asymmetry | 0 |
| Algebraic inverse reassembly, 80 digits | 3.023e-72 |
| Algebraic inverse reassembly, 100 digits | 2.499e-92 |
| Complete transformed-form 80/100 comparison | 8.056e-59 |
| Back-transformed original-coordinate eigenpair residual | 4.498e-16 |
| Canonical action-norm back-transformation error | 7.136e-16 |

The computed 80/100 spectra are identical in binary64. This suggests that merely
increasing the shear arithmetic precision is not the next useful repair; the
remaining eigensystem conditioning/precision needs attention. It is not proof
that all underlying eigenvalues are ill-conditioned or that the theory fails.
The reassembly tests are algebraic identities, not independent continuum bounds;
the generic direct-product/similarity controls provide a separate formula check.

## Signs and nonoscillatory directions are not hidden

At the 100-digit working-form choice all 6696 mode records are retained:
2016 are classified oscillatory within numerical resolution, 216 as frozen
nonoscillatory diagnostics, and 4464 remain unresolved. Of 208 positive-frequency
frozen modes with assigned canonical action/Krein sign, 112 have positive and
96 negative sign. Another 800 positive-frequency modes still need degenerate-
subspace normalization. The six numerically passing cases therefore cannot
be advertised as a healthy or ghost-free branch.

These are frozen numerical classifications, with conditioning-based heuristic
uncertainties, not certified forward-error enclosures or physical instability
proofs. Negative-action and nonoscillatory directions are substantive evidence
to retain for the physical-admission analysis; do not dismiss them as gauge,
numerical noise or irrelevant without demonstrating that conclusion. Whether
they belong to an admitted physical perturbation space, and what evolution or
frequency window they imply, remains unresolved.

## Replay and provenance

The complete fresh eight-worker read-only replay recomputed all eighteen
transformations at both working precisions and every spectrum/mapping result.
It reproduced all scientific bytes exactly and printed READ_ONLY_REPLAY_EXACT,
returning exit 1 with the same 303/361 result and all 58 failed assertions.
An exact replay of unresolved numerical checks does not make them pass.

All 162 source pins / 324 source-sidecar metadata records and all 80 output files
retained their bytes, sizes, mtimes and file set. The external 502-record
preservation guard passed, including all 422 pre-run records, the preflight,
original V3 evidence and earlier failed attempts. Queue/register notes are
append-only; their previous bytes and sidecars are preserved in an ignored
local backup, and only those live index sidecars are refreshed.

Full output: `Analysis/MasterTests/outputs/r4c1_canonical_conditioning_v1_n17_attempt_01/`.
Eighteen shear/sidecar pairs retain both transformed matrices and generators;
eighteen spectrum/sidecar pairs retain both complete spectra and mapping controls.
Manifest and three aggregate pairs give 80 output files. There are 162 frozen
source pins and 324 source/sidecar metadata records. First run: at most16 bounded
spawn workers; spectrum evaluation follows after pool exit with one local BLAS
thread. No package, model/provider or host environment change.

| Aggregate receipt | SHA256 |
| --- | --- |
| summary.json | 590e7eef301edf0d543638f5612420086077139007a4e881f7b286697728c621 |
| independent.json | af0e99c5de4cd96c3b23319bfba99a9dc251e73656f7f52afa9f5fe894d44334 |
| formulas.json | 4691d0b5951f235478e69ecf649535376438ff17a9764ec623df0befd6bb3e7a |

Executable: `Analysis/MasterTests/test_01_r4c1_canonical_conditioning_v1.py`, SHA256
`013f84f8a342b68d8d2c86c18eeb3e9552599709b9f5ee5cd2462704992aef89`.
The original V3 matrices, failed spectra, sources and sidecars remain unchanged.
Private runtime logs stay ignored. No timing or billed-token saving is claimed.

## Next route and unchanged parent disposition

Use the sealed transformed forms for an eigensystem-level precision/conditioning
diagnostic, retaining every mode and all negative/nonoscillatory evidence. Do not
loosen thresholds, keep only the passing eta or mistake working-precision agreement
for physical admission. Registered n25/n33 refinement, simultaneous continuum-node
conditions, physical energy/clock and perturbation space, nonlinear persistence,
full interactions/cutoff and justified healthy-GR recovery remain necessary.

Stage1 remains complete only in its registered bounded linear prepared-dust
scope. Stage2 INCOMPLETE; Stage3 NOT_ENTERED; Tests1--3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS;
Stage4A CLOSED; TOP-X4 unchanged. Both identifying matching inputs are absent;
no numerical C_chi or a0 is derived here. Rule9 DEFERRED; Rule9_cleared=false;
inherit CANONICAL-SPECTRUM-V3, COUPLED-DESCRIPTOR-ACTION-V1 and transitive debt.
physics_pass=false; gate_effect=NONE. No state adoption/evolution, action or
microscopic-parent change, vault mutation, manuscript/site edits, publication,
commit or push.
