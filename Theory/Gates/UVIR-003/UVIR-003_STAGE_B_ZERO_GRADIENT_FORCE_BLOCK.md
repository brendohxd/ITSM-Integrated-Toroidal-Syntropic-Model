# UVIR-003 Stage B - zero-gradient force block and K_Q identifiability

Status: **partial pass for the declared zero-gradient force block only; full
UVIR-003 remains in progress**

## 1. Question

Stage A requires a coupled perturbation calculation about a Minkowski metric,
a constant unit frame and a constant force background. The first bounded
question is whether the force perturbation mixes with lapse, shift, metric,
frame or condensate perturbations at quadratic order, and whether `K_Q` can be
determined from the declared EFT.

## 2. Quadratic factorization

Write

```text
psi = psi_bar + epsilon pi
U = U_bar + epsilon delta_U
g = eta + epsilon delta_g
```

Because `psi_bar` is constant, every derivative of `psi` starts at first
perturbative order. Therefore

```text
Q = epsilon dot(pi) + O(epsilon^2)
Q^2 = epsilon^2 dot(pi)^2 + O(epsilon^3).
```

Corrections involving the aether, lapse or shift first enter the squared term
at cubic order. Similarly,

```text
Y = epsilon^2 |grad(pi)|^2 + O(epsilon^3)
Y^(3/2) = O(epsilon^3).
```

The Hessian of `|grad(pi)|^3` vanishes at zero background gradient. Finally,

```text
Delta_U psi = epsilon Laplacian(pi) + O(epsilon^2),
```

so frame and metric corrections to the squared regulator also begin at cubic
order.

For the operators declared in Stage A, the quadratic action factorizes as

```text
S^(2) = S^(2)_[g,U,Phi] + S^(2)_pi,

S^(2)_pi = (1/2) integral [
  K_Q dot(pi)^2 - (gamma/M_*^2) Laplacian(pi)^2
].
```

This factorization does not require lapse, shift or aether multipliers to be
solved first because none occurs in the force block. It does not solve the
remaining metric-aether-condensate block.

## 3. Reduced Hamiltonian and mode

The canonical momentum and Hamiltonian density are

```text
p_pi = K_Q dot(pi),

H_pi^(2) = p_pi^2/(2 K_Q)
         + gamma Laplacian(pi)^2/(2 M_*^2).
```

For positive `K_Q`, `gamma` and `M_*^2`, this block is nonnegative and contains
one scalar mode with

```text
omega^2 = gamma k^4/(K_Q M_*^2).
```

The homogeneous shift mode has zero frequency and nonnegative energy. The
result is a `z=2` force branch within the restricted regulator definition.

## 4. Why K_Q cannot be derived here

Under a positive constant field redefinition `psi_c = s psi`, the coefficients
transform as

```text
K_Q   -> K_Q/s^2
A     -> A/s^3
gamma -> gamma/s^2
C_m   -> C_m/s
q     -> s q.
```

The combinations

```text
gamma/K_Q
A/K_Q^(3/2)
C_m/sqrt(K_Q)
A q/K_Q
```

are invariant, but `K_Q` alone is not. This is an identifiability result, not
merely a missing numerical estimate. The Stage-A EFT cannot derive a
standalone value of `K_Q`. A parent microscopic calculation or the matter
vertex must fix the physical normalization of `psi`; matching must then
determine invariant coefficient combinations. The speculative estimate
`K_Q ~ M_P^2` remains an assumption.

## 5. Dependency consequence

Requiring a numerical `K_Q` before any structural UVIR-003 progress would
create a circular dependency because MAT-001 is intended to match the matter
normalization but is itself downstream of UVIR-003.

The non-circular split is:

1. UVIR-003 derives the stable and causal domain in field-redefinition
   invariant ratios.
2. MAT-001 or a parent microscopic completion fixes the physical normalization
   and selects a point in that domain.
3. The selected point is checked against the UVIR-003 inequalities.

This does not unblock MAT-001 yet because the remaining coupled
metric-aether-condensate block, nonzero-gradient mixing, regulator covariance,
technical naturalness and physical cutoff remain open.

## 6. Scope limits

This partial pass does not establish:

- the reduced scalar, vector and tensor Hamiltonians of the `g-U-Phi` block;
- stability on a nonzero force-gradient background;
- a covariant completion of `Delta_U`;
- the physical Lifshitz-regime cutoff;
- radiative protection of the missing canonical spatial operator;
- a numerical value for `K_Q`.

It also assumes that Stage B does not add an independent quadratic mixing
operator absent from the declared Stage-A truncation.

## 7. Reproduction

```powershell
python Analysis/UVIR/UVIR-003/uvir003_zero_gradient_force_block.py
```

Expected footer:

```text
UVIR-003 Stage B zero-gradient force block: FACTORIZATION VERIFIED
Reduced force mode: one positive z=2 scalar for K_Q>0 and gamma>0
Numeric K_Q from current EFT: NOT IDENTIFIABLE
STATUS: PARTIAL_PASS_ZERO_GRADIENT_FORCE_BLOCK_ONLY
Full UVIR-003 gate: IN_PROGRESS
```
