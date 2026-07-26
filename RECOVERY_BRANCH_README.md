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

The newest frozen manuscript release is `12.0-alpha.2`. It contains the
frame-sector normalization correction, ADM-readiness and
background-completion screens, and the representative FRW background
existence derivation.

The scalar perturbation ADM programme has passed finite-wavenumber constraint
elimination on the representative evolving branch. The apparent strict
low-wavenumber rank loss is now identified as the homogeneous time-translation
gauge orbit: the two gauge-invariant matter scalars retain a positive regular
`q=0` kinetic block across the trajectory. The flat-decoupling khronon cubic
basis is now verified in three spatial dimensions and exactly reduces to the
previous longitudinal result. A constraint-order identity shows that the
first-order lapse and shift solutions suffice for the reduced cubic action;
explicit second-order corrections cancel. Linear on-shell three-point
kinematics force collinearity, so the physical strong-coupling scale must come
from the complete constrained `2-to-2` exchange-plus-quartic-contact
amplitude. These bounded results do not establish full perturbative stability,
observational viability, or a completed cosmology.

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
