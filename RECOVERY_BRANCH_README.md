# ITSM v12 core-recovery branch

This is the working guide for `recovery/v12-core-architecture`. The recovery
branch rebuilds the ITSM core from explicit actions, derivations, diagnostics,
and falsifiable gates. Legacy v11 documents remain historical inputs; they are
not the scientific status authority for this branch.

## Start here

- Core architecture: `Theory/Core/ITSM_Core_Architecture.md`
- Recovery plan: `Theory/Core/ITSM_Core_Recovery_Plan.md`
- Claim migration ledger: `Theory/Core/ITSM_Claim_Migration_Ledger.csv`
- Gate worklog: `Theory/Gates/RECOVERY_SESSION_WORKLOG.md`
- Manuscript workflow: `Manuscript/CoreRecovery/README.md`
- Manuscript changes: `Manuscript/CoreRecovery/CHANGELOG.md`

## Manuscript status

The newest frozen manuscript release is `12.0-alpha.3`. It includes the
finite-`q` and low-`q` scalar ADM results, the three-dimensional cubic and
quartic interaction-readiness audits, and the nonlinear ADM action-provenance
checkpoint. Earlier releases remain immutable under `releases/`.

The scalar perturbation ADM programme has passed finite-wavenumber constraint
elimination on the representative evolving branch. The apparent strict
low-wavenumber rank loss is now identified as the homogeneous time-translation
gauge orbit: the two gauge-invariant matter scalars retain a positive regular
`q=0` kinetic block across the trajectory. The flat-decoupling khronon cubic
basis is now verified in three spatial dimensions and exactly reduces to the
previous longitudinal result. A constraint-order identity shows that the
first-order lapse and shift solutions suffice for the reduced cubic action;
explicit second-order corrections cancel. Linear on-shell three-point
kinematics force collinearity. The subsequent flat-decoupling quartic audit
finds 96 expanded monomials, a finite exact elastic contact term and exactly
vanishing elastic `t/u` cubic exchange. The centre-of-mass `s` channel carries
zero spatial momentum and lies on the non-invertible homogeneous khronon gauge
orbit. At quartic order the second-order constraint source is genuinely needed
through a Schur complement. The physical strong-coupling scale therefore still
requires the complete gauge-regular constrained cosmological `2-to-2`
amplitude. The exact nonlinear `g+U+Phi+alignment` ADM parent block now has
verified FRW and finite-`q` quadratic provenance. The full cosmological `J2`
is not yet assembled. Track A now adopts the rest-space Laplacian
`D_mu D^mu psi` and retains exact `Y^(3/2)` for a declared local
nonzero-gradient perturbative force analysis. The homogeneous zero-gradient
force action is verified through direct quartic order and its lapse/shift `J2`
component is derived, but the complete multi-sector source and physical
amplitude remain open. These bounded results do not establish full
perturbative stability, observational viability, or a completed cosmology.

## Repository rules for recovery work

1. Treat the claim migration ledger and gate reports as the status record.
2. Keep derived, conditional, open, and rejected claims visibly distinct.
3. Put ongoing manuscript edits in `ITSM_Core_working.tex` and `sections/`.
4. Never overwrite a versioned manuscript PDF or its source tree.
5. Freeze every manuscript version under
   `Manuscript/CoreRecovery/releases/v<version>/`.
6. Update the manuscript changelog and `VERSION` in the same commit as a new
   release.

The root `README.md` and root `CHANGELOG.md` contain substantial legacy v11
history. They are retained for provenance and must not be read as the current
v12 recovery claim set.
