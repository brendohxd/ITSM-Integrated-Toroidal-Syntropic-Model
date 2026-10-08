# R4C1-G3S: equal-Newton family's coupled scalar symbol

Date: 2026-09-30. Owner: Master Test 1 / conditional R4C1-v1.
Frozen before the new executable or any G3S scientific calculation.
Scientific classification: CONDITIONAL; review DEFERRED; gate effect NONE.

## Question and inherited scope

Does G3's equal-Newton coefficient family retain real propagating scalar
characteristics once the metric, dust and regulator constraints and all
time-dependent canonical terms are included? Does it remove S2's defective
zero-speed principal branch? These are necessary diagnostics, not complete
well-posedness, causality, physical-cutoff or healthy-GR proofs.

Read the owning [G3 report](RES001_R4C1_EQUAL_NEWTON_FAMILY_REPORT_2026-09-30.md)
and [S1](RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md) /
[S2](RES001_R4C1_SCALAR_PROPAGATION_REPORT_2026-09-26.md) reports.
G3's original 112/113 failure and separately passing refinement remain intact.
No B1 numerically evaluated operator can stand in for G3's operator.

## Fixed inputs and calculation

Use the unchanged R4C1 action and the generic symbolic S1 preconstraint and
reduced K,M,V export, not S2's B1-specialized matrices. Substitute G3's
coefficients with symbolic eta, 0<eta<=1. Use the G3 contract's potential,
couplings and initial-data family without retuning. Derive the background
flow from the pinned B1 action equations with those new coefficients.

For q=(delta u,delta v,delta r,delta psi,delta tau,w), diagonalize the exact
kinetic squares using q=J y with J[:,4]=(udot,vdot,rdot,psidot,C,k/a).
Normalize the entire action by a^(3/2) and square weights
(1,1,1,K_Q,D,M_U^2*c14), where
D=4*H^2*M_c^2*M_t^2/(M_U^2*cL). Require H>0,a>0,C>0,k!=0 and the original
S1 nonzero auxiliary determinant. Do not cross eta=0 with an inverse.

Derivatives are at fixed comoving k. Build R, M_c,V_c,G=M_c-M_c^T and
W=V_c+dM_c/dt, and check the original Euler-equation transformation.
Only afterward substitute k=a*p to extract the physical-momentum symbol.
Eliminate the single p^4 force block using BOTH p^3 cross blocks. Calculate
the full five-dimensional slow characteristic determinant, its zero-root
multiplicity and eigenvector defect, and the nonzero branch coefficients.
Do not assume the B1 polynomial or discard a negative slow potential entry
without its gyroscopic term. Exact zero modes and a pressureful matter
completion are outside this registered chart.

## Registered verification and interpretation

- Exact canonical kinetic identity, symmetry/variational identities and
  transformation from the retained-field equations; reject omitted Rdot,
  omitted M_cdot and omitted fast-block elimination.
- Pin all direct inputs and inherited dependency hashes before computation.
  Reject a deliberately false source pin without creating an output.
- Use all six stored G3 eta values and both background methods at
  t=(0,.5,1,2,3,4). Check the new symbolic flow against the pinned pure RHS
  to normalized 1e-12. Numerically compare the new preconstraint Schur
  complement and its reduced kinetic matrix for n=(1,2,4,8), to normalized
  1e-8. These samples are accuracy checks, not independent physical gates.
- At physical p=(20,40,80,160), record every full canonical frequency root,
  its pencil residual (<1e-8), and discrepancies from the EXACT derived
  propagating branches. A 0.05 discrepancy at p=160 is a diagnostic reach
  criterion, not proof of an EFT-admissible mode or a threshold to retune.
- Any real leading growth, unresolved branch, failed identity or integrity
  mismatch must be reported. Purely imaginary propagating roots do not
  establish a diagonalizable zero branch or all-sector stability. Wider
  cones and quartic dispersion retain their physical validity questions.
- New numbered attempt directory only; refuse existing outputs. Preserve
  failure receipts. A replay recomputes in memory, never invokes any older
  receipt-producing main(), and verifies byte identity.

No target-data fit, provider dispatch, PDF work, commit, push or publication.
No prediction of a0, C_chi or C_proj=2/3 is supplied. Test 1 remains open
unless its full owning requirements are met. Inherit provisional review debt
R9-MT1-VARIATION/B1/G1/S1/S2/G2/G3; register G3S separately.
Canonical Tests 1–3 HOLD_SUBSTANTIVE; physics_pass=false,
Rule9_cleared=false; MAT-001 BLOCKED, UVIR-003 IN_PROGRESS,
K_Q NOT_DERIVED, V NOT_COMPUTED, Stage4A CLOSED, TOP-X4 unchanged.
