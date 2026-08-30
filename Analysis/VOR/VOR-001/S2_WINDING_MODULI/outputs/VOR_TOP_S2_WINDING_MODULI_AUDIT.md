# VOR/TOP S2 winding and moduli hostile audit

**Calculation:** `PASS_HOSTILE_SYMBOLIC_AUDIT`  
**Disposition:** `REPAIR_VOR_S2_AND_REJECT_WINDING_ONLY_GENERIC_MODULI_STABILIZATION`  
**VOR-001/TOP-001:** `OPEN_SCAFFOLD_ONLY` · **physics pass:** `false`

## Winding-amplitude result

For `e=(1/2) rho^2 omega^2 + (lambda/4)(rho^2-v^2)^2`, the global
constant-amplitude minimum is

- `rho^2=v^2-omega^2/lambda` below `omega^2=lambda v^2`, with
  `e=omega^2(2 lambda v^2-omega^2)/(4 lambda)`;
- `rho=0` above the threshold, with `e=lambda v^4/4`.

S2-T01 and T03-T06 survive with the branch qualification. S2-T02 does not:
at the preregistered `lambda=100`, `omega=1`, `v=1`, the exact relative S1
deviation is `1/200` = `0.500%`, not below `0.1%`.
The earlier runner used `lambda=100000.0` and therefore did
not execute the specified point.

## Fixed-volume moduli result

With `L_i=L0 exp(alpha_i)` and `sum alpha_i=0`, the cubic point is stationary
only when `n1^2=n2^2=n3^2` (or after the amplitude has restored to zero). A
symmetric winding sector has a conditional local shape minimum while its
broken branch exists. A single-cycle winding has a fixed-volume runaway:
elongating its wound cycle drives `omega^2` and the winding energy toward zero.

Winding energy alone therefore does **not** generically stabilize the torus
shape. Modular reindexing covariance is exact, but it is a redundancy—not a
dynamical stabilization mechanism.

No `2*pi`, `2/3`, `13/12`, `L=c/H`, force coupling, `a0`, or cosmological
attractor is inferred.
