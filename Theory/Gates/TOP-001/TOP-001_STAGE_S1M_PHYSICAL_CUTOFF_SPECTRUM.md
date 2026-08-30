# TOP-001 S1M — Physical-cutoff spectrum robustness

**Date:** 2026-08-05
**Branch:** `recovery/v12-core-architecture`
**Subgate:** `PASS_TOP001_S1M_PHYSICAL_CUTOFF_SPECTRUM_INVARIANCE`
**Research gate:** `OPEN_SCAFFOLD_ONLY`
**physics_pass:** **false**

## Purpose

Close the cutoff caveat identified by the modular basis-equivalence audit.
Equivalent lattice bases must be compared using a physical reciprocal
eigenvalue cutoff, not identical boxes of integer coordinate labels.

For direct basis $B$ and reciprocal label $m$, define

\[
\ell(B,m)=m^T(B^{-1}B^{-T})m,
\qquad
|k|^2=(2\pi)^2\ell.
\]

Under $B'=BM$, $M\in SL(3,\mathbb Z)$, and $m'=M^Tm$, the value of
$\ell$ is unchanged exactly.

## Complete physical-cutoff enumeration

The audit independently enumerates integer labels in each basis and retains
only $\ell\leq\ell_{\max}$. It certifies that every retained spectrum is
complete using

\[
\frac{(N+1)^2}{\lVert Q^{-1}\rVert_\infty}>\ell_{\max},
\qquad Q=B^{-1}B^{-T}.
\]

For positive-definite $Q$, $\lambda_{\min}(Q)\geq1/\lVert Q^{-1}\rVert_\infty$.
Any label outside the coordinate box has Euclidean norm at least $N+1$, so
the certified lower bound excludes all omitted labels from the physical
cutoff domain. A second enumeration at $N+2$ must be byte-for-byte
spectrally identical.

## Executable record

```powershell
python Analysis\TOP\TOP-001\top001_s1m_physical_cutoff_spectrum_audit.py
# expect: PASS_TOP001_S1M_PHYSICAL_CUTOFF_SPECTRUM_INVARIANCE
```

Default inputs:

```text
ell_max = 2
N = 10
refined N = 12
raw-label negative-control box N_raw = 2
```

Outputs:

```text
Analysis/TOP/TOP-001/outputs/top001_s1m_physical_cutoff_spectrum_summary.json
Analysis/TOP/TOP-001/outputs/top001_s1m_physical_cutoff_spectrum_summary.sha256
```

Accepted deterministic JSON SHA-256:

```text
74DDDFC767EF0BBC196C0BAAC5B44B086F36A5D6714B79829E624C0BE6632F41
```

## Exact result

All four declared modular charts independently return:

| Quantity | Result |
|---|---:|
| Modes below cutoff | 358 |
| Distinct eigenvalues | 179 |
| Maximum degeneracy | 2 |
| Canonical spectrum SHA-256 | `0DFB9BABC04832AAA37FCD65C7A5EC2B49B2A5F77587A41ABF6A8F2D4EF3D96C` |

The exact rational eigenvalue multisets, degeneracy profiles and transformed
label bijections agree. Refining the enumeration box does not change them.

## Negative and separation controls

- Comparing identical raw boxes $|m_i|\leq2$ in the original and elementary
  shear charts produces different spectra because $M^T$ maps some labels
  outside the raw box. This is the expected false discrepancy.
- A left-acting volume-preserving ambient deformation
  $B_{\rm physical}=\operatorname{diag}(2,1,1/2)B$ passes its own completeness
  certificate and produces a different spectrum. It is a physical shape
  change in the declared ambient metric, not a basis relabelling.
- Zero/negative/non-rational cutoffs, invalid boxes, singular bases and invalid
  modular maps fail closed.

## Scientific boundary

This is an exact fixed-boundary spectral-identity audit. It does not compute a
Casimir energy or stress, select a shear, derive a modulus action, establish
stability, prefer a twisted topology, assign significance to $1,4,7$, or
produce $13/12$, $H_0$, $a_0$, $C_{\rm obs}$, or cosmology. TOP-001
remains `OPEN_SCAFFOLD_ONLY` with `physics_pass: false`.
