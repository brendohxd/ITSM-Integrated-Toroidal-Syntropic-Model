# Ultra plan — coupled constraints, U5 and M4 physical residue

**Required reasoning:** Ultra  
**Scope:** one bounded gate-critical parent calculation  
**Entry condition:** a Max reduction supplies a frozen action, on-shell
background and non-empty stable scalar-sector domain  
**Gate effect:** none until independently reviewed and signed  

## Do not start if

- the off-shell matter operator is undefined;
- the finite-density background is not on shell;
- the parent action or parameter chart is still changing;
- Max found a ghost/gradient failure or no valid EFT domain;
- the calculation would need observed `a_0` or another target as input.

## U-0 — freeze the calculation contract

Record action/input hashes, background, boundary conditions, gauge, fields,
source convention, expected constraints and kill criteria. Select one parent
only. Do not combine `RCP-I1`, `RCP-C0` and PKM1 terms.

## U-1 — complete constrained dynamics

1. Expand amplitude, phase, lapse, shift and spatial metric perturbations to
   the required order.
2. Perform the complete ADM/Dirac analysis: primary/secondary constraints,
   first-/second-class split, brackets, rank and physical DOF.
3. Repeat the rank analysis on zero-gradient and declared nonzero-gradient
   backgrounds.
4. Derive the reduced Hamiltonian and kinetic/gradient matrices.
5. Identify all ghosts, Jeans bands, singular constraints and strong-coupling
   limits.

## U-2 — U5 covariant phase-space check

- derive the presymplectic potential and current directly from the same action;
- identify gauge degeneracies and compact/zero-mode boundary terms;
- compute the covariant on-shell DOF/rank;
- compare with ADM/Dirac results;
- classify disagreement as an algebra error, boundary effect, chart boundary or
  parent pathology without inserting a repair operator.

## U-3 — M4 invariant matter pole residue

1. Construct the fully reduced physical kernel and source vector.
2. Diagonalize physical eigenmodes.
3. Invert the kernel on the physical subspace.
4. Locate poles and calculate their signed residues.
5. Verify field-redefinition invariance.
6. Reproduce the static force from the appropriate zero-frequency limit.
7. Compare with `V=C_m/sqrt(K_Q)=g_phi/sqrt(Z_phi)` only after the physical
   projection.
8. State whether the normalization is derived, free, zero or ill-defined.

This is the decisive `M2/M3-U1` calculation.

## U-4 — causality, EFT and relativistic admissibility

Only if U-1 through U-3 survive:

- derive characteristics, front speeds and physical cutoff;
- test zero-density, zero-coupling and high-acceleration GR limits;
- calculate both weak-field metric potentials;
- evaluate equivalence-principle and preferred-frame structure;
- derive PPN and Shapiro-delay limits;
- derive lensing and GW propagation from the same metric/action.

Stop at the first hard exclusion and preserve it.

## U-5 — blind coefficient decision

Without using observed values, determine whether the parent fixes:

- the physical matter residue;
- nonlinear force coefficient;
- healing/screening scale;
- any acceleration transition;
- any topology-sensitive normalized quantity.

Only after recording the blind result may it be compared with `a_0` or another
observable. A remaining `v/Lambda^2`, arbitrary function or Wilson coefficient
means the mechanism is calculable but not predictive.

## Exit classifications

- `SURVIVES_FOR_SIGNED_ARCHITECTURE_REVIEW`;
- `CALCULABLE_FREE_NORMALIZATION_MAT_REMAINS_BLOCKED`;
- `SCOPED_NO_GO_PHYSICAL_MODE_OR_RESIDUE`;
- `HOLD_BACKGROUND_OR_CONSTRAINT_INCOMPLETE`.

None is a generic `CLEARED` result.

## Cost-control checkpoints

Stop and package after U-1, U-2 and U-3 separately. If U-1 fails, do not spend
Ultra reasoning on U-2 through U-5. After each checkpoint switch to High or
Medium for report writing, hashes and repository hygiene.

