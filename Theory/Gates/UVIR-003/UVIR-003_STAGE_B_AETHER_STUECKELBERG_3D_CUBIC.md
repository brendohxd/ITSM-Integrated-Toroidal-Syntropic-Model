# UVIR-003 - Stage B three-dimensional khronon cubic audit

Date: 2026-07-26
Branch: `recovery/v12-core-architecture`
Status: **3D flat-decoupling cubic vertex passed; physical 2-to-2 cutoff open**

## Executive result

The bounded one-dimensional khronon calculation has been extended to three
spatial dimensions. Starting from

```text
T = t + pi,
U_mu = -partial_mu T / sqrt[-(partial T)^2],
```

the diagnostic expands all four two-derivative Einstein-aether invariants
through cubic order and verifies the result directly against the normalized
aether expansion.

Define

```text
p_i  = partial_i pi,
v_i  = partial_i dot(pi),
H_ij = partial_i partial_j pi,
H    = trace(H_ij) = Delta pi.
```

After suppressing the overall factor `M_U^2`, the quadratic action is

```text
L2 = 1/2 [
  c14 v_i v_i
  - (c1+c3) H_ij H_ij
  - c2 H^2
].
```

The complete three-dimensional cubic vertex is

```text
L3 =
  -c14 [ddot(pi) p_i v_i + dot(pi) v_i v_i]
  +(c1+2c3-c4) p_i H_ij v_j
  +2c2 H p_i v_i
  +(c1+c3) dot(pi) H_ij H_ij
  +c2 dot(pi) H^2.
```

Setting all transverse derivatives to zero exactly reproduces the previous
one-dimensional result. This is a non-collinear operator-basis derivation, but
the metric and condensate are still held fixed.

## Constraint-elimination result

Let the quadratic constrained action be

```text
L2 = L2_physical + z^T J + z^T C z/2,
z1 = -C^(-1) J,
```

and write the constraint solution as `z=z1+z2+...`, where `z2` is quadratic in
the propagating fields. Then

```text
L2[z1+z2]
  = L2[z1] + (C z1 + J)^T z2 + z2^T C z2/2.
```

The linear `z2` term vanishes because `C z1+J=0`; the remaining term is
quartic. Likewise, inserting `z2` into `L3` first contributes at quartic
order. Therefore

```text
L_reduced^(3) = L3[physical fields, z1].
```

An explicit second-order lapse or shift solution is not needed for the reduced
cubic action. The future cosmological cubic calculation still requires the
complete cubic ADM vertex, but only the already-derived first-order
constraints must be substituted.

## Canonical NDA diagnostic

For a nonzero Fourier mode,

```text
chi_k = M_U sqrt(c14) |k| pi_k,
c_s^2 = c123/c14.
```

Counting `|omega| ~ c_s |k|` gives an operator-by-operator diagnostic

```text
L3_canonical
  ~ C_operator k^2 chi^3 / [M_U c14^(3/2)].
```

At the representative dimensionless point:

```text
c_s                         = 1.15470053838
M_U c14^(3/2)               = 0.02904737510
minimum operator NDA q      = 0.12577882373
corresponding NDA energy    = 0.14523687548
NDA q / H across trajectory = 0.2029 ... 1.6462
```

These numbers are not a physical cutoff. They depend on the chosen operator
basis, omit metric and condensate mixing, and use an unselected dimensionless
example. In particular, they do not establish a controlled hierarchy above
the background scale on that example.

## Why the cubic vertex still does not fix the cutoff

For linear dispersion `|omega|=c_s|k|`, energy and momentum conservation in a
three-point process require one momentum magnitude to equal the sum of the
other two. Equality in the triangle inequality forces the three spatial
momenta to be collinear. A non-collinear on-shell three-point amplitude is
therefore kinematically forbidden.

The physical interaction scale must instead be obtained from an on-shell
`2-to-2` amplitude containing:

1. the complete constrained cosmological cubic exchange vertices;
2. the quartic contact vertex;
3. projection onto the physical scalar eigenmodes;
4. an angular or partial-wave unitarity criterion.

The healthy nonprojectable theory's behavior depends on its full constraint
and operator content, as emphasized by Blas, Pujolàs and Sibiryakov,
[arXiv:1007.3503](https://arxiv.org/abs/1007.3503). This audit therefore does
not transfer a cutoff from a different Hořava model.

## Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_aether_stueckelberg_3d_cubic.py
```

Output:

- `Analysis/UVIR/UVIR-003/outputs/uvir003_aether_stueckelberg_3d_cubic_summary.json`

Expected footer:

```text
UVIR-003 three-dimensional khronon cubic vertex: VERIFIED
Reduced cubic second-order constraint correction: CANCELS
Noncollinear on-shell three-point amplitude: KINEMATICALLY_FORBIDDEN
Representative basis-dependent NDA momentum: 0.125778823734
Physical strong-coupling scale: NOT_YET_DERIVED
Full UVIR-003 gate: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_3D_CUBIC_AND_CONSTRAINT_IDENTITY
```
## Subsequent quartic status

The follow-on three-dimensional flat-decoupling quartic audit is now complete.
It derives 96 expanded monomials, the exact elastic contact angular form and
exactly vanishing elastic `t/u` cubic exchange. The centre-of-mass `s` channel
is the non-invertible homogeneous khronon gauge orbit. Quartic reduction
requires the second-order constraint Schur complement, although third-order
constraint solutions cancel. The physical cutoff therefore remains open
pending the full gauge-regular constrained cosmological amplitude.

See
`UVIR-003_STAGE_B_AETHER_STUECKELBERG_3D_QUARTIC.md`.
