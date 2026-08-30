# MAT-001 M4 invariant source-pole residue control

**Calculation:** `PASS_GENERIC_INVARIANCE_AND_NEGATIVE_CONTROLS`  
**Disposition:** `M4_CONTROL_PASS_LIVE_RESIDUE_BLOCKED`  
**MAT-001:** `BLOCKED` · **V:** `NOT_COMPUTED` · **K_Q:** `NOT_DERIVED`

## What was established

For the explicit constrained quadratic form

`A_eff = A - B C^-1 B^T`, `c_eff = d - B C^-1 h`,

the signed canonical source-pole residue is

`g_can = (c_eff^T u)/sqrt(u^T K u)`.

The exact symbolic control recovers the generalized physical modes, retains
the source dressing from the algebraic constraint, and gives couplings
`['5/2', '7/3']`. Under simultaneous `x=R y`, `z=S w` changes,
the K-metric mode projection is exactly invariant. Reversing the anchored mode
flips the signed residue. Negative controls reject Euclidean projection and
untransported modes/covectors.

## Why this is not a MAT result

The repository's live-export inventory does not provide the complete same-action
`K,A,B,C,d,h` matrices and physical mode direction required for the UVIR
parent. Existing J2/R2 artifacts explicitly label themselves templates rather
than live eigenmode extraction. Therefore this control cannot compute a
numeric `V`; it only establishes the necessary invariant method and freezes
the missing-input boundary.

No MAT, UVIR, Stage 4A, SPARC, H0, or downstream claim is promoted.
