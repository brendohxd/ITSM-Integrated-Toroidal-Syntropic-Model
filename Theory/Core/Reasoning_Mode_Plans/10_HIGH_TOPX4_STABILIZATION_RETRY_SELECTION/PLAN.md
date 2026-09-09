# High plan — TOP-X4 stabilization retry selection

**Mode:** High  
**Entry:** `X4-D2 HOLD_UNSTABILIZED` for frozen parent `X4-I1C`  
**Exit:** `COMPLETE`; `X4-S2F3` frozen for one Max retry  
**Gate effect:** none

## Objective

Determine whether one minimal, independently motivated modification can supply
a stable or metastable fourth-circle radius without importing an observed
scale. Do not rerun Max until one complete retry is frozen.

## Candidate screen

1. **`X4-S1` — altered classical condensate/winding sector.** Test whether a
   nonzero integer winding, a separately declared vacuum-energy sign and a
   condensate-supporting potential admit simultaneous field, radion and
   Einstein stationarity. A fixed-radion minimum at fixed fields is
   insufficient if the full stress tensor is off shell.
2. **`X4-S2` — sign-competing one-loop content.** Specify an actual additional
   periodic fermion or antiperiodic boson, its spin structure/boundary
   condition, mass, degrees of freedom, quantum state, regulator,
   counterterms and cutoff. A fitted Casimir coefficient is prohibited.
3. **`X4-S3` — classical flux/p-form stabilization.** Write the complete
   covariant kinetic and flux-quantization sector and test its stress tensor.
   Do not relabel scalar phase winding as a new flux contribution.
4. **`X4-S4` — orbifold/brane stabilization.** Treat as a different geometry,
   not a repair of the smooth `T3 x S1` parent. Require explicit junction
   conditions and localized counterterms before consideration.

## Required work

1. Perform a primary-literature audit of smooth-circle radion stabilization,
   Casimir signs, spin structures and flux compactification.
2. Write the exact Einstein-frame potential and full covariant stress for each
   candidate at the symbolic level.
3. Apply simultaneous field, radion and gravitational stationarity; do not
   minimize only a partial potential.
4. Check whether the putative minimum has a positive canonical radion Hessian
   and lies below a specified five-dimensional cutoff.
5. Reject any candidate requiring a coefficient or radius selected from
   `a0`, `H0`, SPARC, `2*pi` or another desired output.
6. Rank surviving candidates by added assumptions and freeze exactly one. If
   none survive the High prescreen, close TOP-X4 rather than escalating.

## Stop boundary

Stop after the selected action, state, boundary conditions, counterterms,
parameter domains and Max kill criteria are hashed. Do not run the new
background, KK determinant or coupled constraint calculation in this task.

## Reasoning transition

Remain on High for this selection. Return to Max only if a fully specified
candidate survives. Ultra remains closed until the new A1--A4 chain passes.

## Completion record — 2026-09-06

All four candidates were screened. `X4-S1` has a real conditional winding
minimum, but only in a changed vacuum sector yielding `AdS4 x S1` with zero
temporal charge. `X4-S3` supplied no distinct minimal flux on one smooth
circle, and `X4-S4` is a different orbifold/brane geometry. The minimum strict
sign-competing field content is `X4-S2F3`: three periodic massive 5D Dirac
spectators. Its action, state, boundary conditions, counterterms, parameter
domain and Max kill criteria are frozen in
`Theory/Gates/TOP-X4/TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md`.

The High algebraic prescreen completed 8/8 checks with `physics_pass=false`.
No determinant or new background was run. Continue only under plan 11 at Max.
