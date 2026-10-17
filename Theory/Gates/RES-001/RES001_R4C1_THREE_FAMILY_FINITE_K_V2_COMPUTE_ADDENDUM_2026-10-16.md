# R4C1 finite-k V2: bounded rational identity verification

V1 source b8313ded09dbf8c72611ca9e93ef0396c471e9ab8f09f4a4e173ff5456e50c58
and interrupted attempts01/02 are retained. Attempt01 was manually interrupted
without an accepted receipt. The unchanged-source diagnostic retry02 exited
3221225477 (Windows0xC0000005), after reaching the generic determinant identity;
the private trace showed expand/factor calls and its final dump was incomplete.
The native exit's root cause is unassigned. No runtime/security changes follow.

V2 changes only the representation/algorithm used for exact checks. It cancels
rational factors before optional factorization, rather than expanding first.
The two determinant checks use leading_factor/target_factor-1=0 as an exact
rational identity. Both sides are polynomials in the frequency variable on the
declared regular coupling domain: equality as rational functions entails
identical polynomials, including roots and multiplicities, by continuation.
No evaluation at a root and no numerical tolerance replaces the identity.
An explicit doubled-target rejection control protects determinant normalization.

The generic Hessian, action reduction, independent density, principal blocks,
determinant factors, family maps, canonical/numerical checks, domain and physical
warnings remain unchanged. This is not a correction of a physical result: V1
produced none. Dependent numerics still stop if an exact prerequisite fails.
V2 outputs must be new attempt03 receipts and exact replay. Keep Rule9 deferred,
physics_pass=false and all original scientific/nonlinear/window/matching holds.
