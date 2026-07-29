# UVIR-003 Stage B reduced quartic momentum kernel

Date: 2026-07-29
Branch: `recovery/v12-core-architecture`
Scope: analytic four-leg contact, complete constraint Schur kernel, and exact homogeneous-channel projectors

## Decision

The complete analytic quartic contact and constraint-induced Schur terms are
now polarized and assembled as a factorized physical-basis kernel. The result
is

```text
PASS_FACTORIZED_FINITE_Q_REDUCED_QUARTIC_KERNEL.
```

For nonzero external and internal spatial momenta,

```text
W_red = W_contact + W_Schur,

W_Schur = -sum_(ab|cd) B_ab(-K)^T C(K)^(-1) B_cd(K),
```

where the sum runs over `(12|34)`, `(13|24)`, and `(14|23)`. The two-leg
source `B_ab` is obtained by varying the already verified complete cubic
functional once with respect to the output constraint and once with respect
to each physical input leg.

## Contact polarization

The four-leg contact is extracted by differentiating the analytic
`L4[x,z1]` functional once with respect to each external leg amplitude.
Momentum conservation is imposed through

```text
k1+k2+k3+k4=0,
q_i^2 + sum_(j!=i) k_i.k_j = 0.
```

The representation retains named first-order lapse and shear entries and
supplies exact physical-basis resolvers for every leg. It includes the generic
non-collinear Hessian and scalar-shift contractions without flattening their
repeated rational denominators.

## Complete pair source and Schur term

For a pair `(a,b)` and output constraint momentum
`K=-(k_a+k_b)`, the script derives

```text
B_ab = (B_N, B_Sigma)^T
     = d^3 L3/(d epsilon_a d epsilon_b d z_K)
```

after applying the time-dependent `(Xi,Q_rho,Q_chi,Pi)` map to the two input
legs. The first-order input lapse and shear are retained factorwise with their
exact resolvers. A symbolic toy-source regression verifies the coefficient
and sign of all three Schur pairings.

## Exact homogeneous internal channel

The finite-`q` constraint inverse is not continued by naive substitution.
At exact `q_K=0`, the scalar shift coordinate

```text
Sigma=-D^2 beta
```

does not exist as an independent homogeneous variable. The algebraic rule is

```text
P_constraint = diag(1,0)        on (delta_N,Sigma),
G_constraint(0) = diag(-1/(2V),0),
P_physical = diag(0,1,1,1)      on (Xi,Q_rho,Q_chi,Pi).
```

For `V!=0`, the exact homogeneous channel retains the lapse constraint and the
`(Q_rho,Q_chi,Pi)` physical subspace while removing both `Sigma` and the
verified homogeneous `Xi` time-translation orbit. The script verifies
projector idempotence, annihilation of the excluded directions, the projected
constraint-inverse identity, and a finite centre-of-mass lapse-source limit.

This is a gauge-regular algebraic prescription for assembling the next
amplitude calculation. It is not itself a propagating exchange amplitude or
a unitarity result.

## Nonanalytic Track-A boundary

The exact term

```text
-A_IR delta_N1 |grad(pi)|^3
```

has no ordinary four-leg Taylor kernel at the homogeneous zero-gradient
background. It remains assigned to the declared local nonzero-gradient
analysis and is not silently smoothed in this calculation.

## Boundary

Still open:

- local adiabatic quadratic propagators in the physical basis;
- the nonzero-channel propagating exchange terms;
- application of the exact homogeneous projector to the centre-of-mass
  exchange channel;
- the combined exchange-plus-reduced-contact amplitude;
- a declared unitarity criterion and physical cutoff;
- the local nonzero-gradient exact-`Y` reduction.

UVIR-003 remains in progress and MAT-001 remains blocked.

## Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_complete_l4_contact.py
python Analysis/UVIR/UVIR-003/uvir003_cubic_momentum_kernel.py
python Analysis/UVIR/UVIR-003/uvir003_reduced_quartic_momentum_kernel.py
```

Expected final status:

```text
STATUS: PASS_FACTORIZED_FINITE_Q_REDUCED_QUARTIC_KERNEL
```

Machine-readable output:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_reduced_quartic_momentum_kernel_summary.json
```
