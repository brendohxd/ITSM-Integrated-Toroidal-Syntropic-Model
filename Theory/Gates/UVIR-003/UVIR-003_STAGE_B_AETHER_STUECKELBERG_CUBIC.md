# UVIR-003 - Stage B bounded aether Stueckelberg cubic audit

Date: 2026-07-26
Branch: `recovery/v12-core-architecture`
Status: **one-dimensional flat-decoupling vertex basis passed; physical cutoff open**

## Scope

This calculation restores the preferred-time scalar through

```text
T = t + pi,
U_mu = -partial_mu T / sqrt[-(partial T)^2],
```

and expands the four-operator Einstein-aether action through cubic order. The
profile is longitudinal and one dimensional, and the metric is held flat.
This is a bounded decoupling-limit vertex audit, not the full cosmological
cubic ADM reduction.

The khronon representation is appropriate because hypersurface-orthogonal
Einstein-aether theory is equivalent to the infrared limit of the extended
Hořava theory; see Jacobson,
[arXiv:1001.4823](https://arxiv.org/abs/1001.4823). The broader literature
also shows why a strong-coupling conclusion must be tied to the selected
nonprojectable action and its constraint structure rather than inferred from
a quadratic rank count alone; see Blas, Pujolàs and Sibiryakov,
[arXiv:1007.3503](https://arxiv.org/abs/1007.3503), and Papazoglou and
Sotiriou, [arXiv:0911.1299](https://arxiv.org/abs/0911.1299).

## Derived vertex basis

With the overall factor `M_U^2` suppressed and

```text
c14  = c1 + c4,
c123 = c1 + c2 + c3,
```

the longitudinal quadratic Lagrangian is

```text
L2 = 1/2 [c14 pi_tx^2 - c123 pi_xx^2].
```

The cubic Lagrangian is

```text
L3 =
  - c14 pi_t pi_tx^2
  + c123 pi_t pi_xx^2
  - c14 pi_tt pi_tx pi_x
  + (2 c123 - c14) pi_tx pi_x pi_xx.
```

The diagnostic derives these terms from the normalized aether and the four
two-derivative invariants, then independently checks every coefficient.

For each nonzero Fourier mode, the quadratic longitudinal variable is
canonically normalized by

```text
chi_k = M_U sqrt(c14) |k| pi_k,
```

with scalar speed squared `c123/c14`. At the representative dimensionless
point this is `4/3`; the canonical prefactor is `0.1936491673`. These numbers
describe only the selected example.

## Why no physical scale is reported

A unique physical strong-coupling scale cannot be extracted from this
one-dimensional truncation. It omits:

- non-collinear momentum-triad dependence;
- second-order lapse and scalar-shift response;
- evolving-background terms;
- condensate and metric mixing;
- projection onto the complete physical eigenmode basis.

Single-direction cubic terms can also be rearranged by integrations by parts
and on-shell identities. Assigning a cutoff before the full triad amplitude
and constrained physical basis are fixed would make the answer
representation dependent.

The result is therefore:

```text
VERTEX_BASIS = DERIVED_IN_ONE_DIMENSIONAL_FLAT_DECOUPLING_LIMIT
PHYSICAL_STRONG_COUPLING_SCALE = NOT_YET_DERIVED
UVIR-003 = IN_PROGRESS
MAT-001 = BLOCKED
```

## Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_aether_stueckelberg_cubic.py
```

Output:

- `Analysis/UVIR/UVIR-003/outputs/uvir003_aether_stueckelberg_cubic_summary.json`

Expected footer:

```text
UVIR-003 bounded Stueckelberg cubic vertex basis: VERIFIED
Longitudinal scalar speed squared: 1.33333333333
Physical strong-coupling scale: NOT_YET_DERIVED
Full UVIR-003 gate: IN_PROGRESS
MAT-001: BLOCKED
STATUS: PASS_BOUNDED_VERTEX_BASIS
```
