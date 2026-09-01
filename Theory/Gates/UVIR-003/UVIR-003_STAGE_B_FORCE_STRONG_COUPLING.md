# UVIR-003 — Stage B item 9 (partial): longitudinal force-sector IR NDA scale

Status: **partial NDA estimate — longitudinal direction, IR (below-`k_cross`)
regime only; not a completed physical strong-coupling cutoff and not
numerically evaluable pending a `K_Q` matching condition**

This advances one input to Stage B roadmap item 9. It does not close that item
or UVIR-003.

## Executive result

The Stage-A force operator `-A|v+\nabla\pi|^3` was expanded around
`v=(q,0,0)`, the fluctuation was normalized by the temporal kinetic term, and
the cubic derivative coefficient was read using the same order-of-magnitude
NDA method used in `UVIR-001_GATE_REPORT.md` Section 7.

The deliberately restricted result is

\[
\boxed{\Lambda_{\rm NDA,long}^{\rm (IR)}
\sim\frac{K_Q^{3/4}}{\sqrt A}}.
\]

This is a **time-normalized longitudinal derivative scale in the
`k^2`-dominated IR truncation**. It is not yet the physical EFT cutoff because
the spatial normalization is anisotropic, the transverse modes were not
carried through, the `k^4` Lifshitz regime has different power counting, and no
loop or unitarity analysis was performed.

A numeric value is also unavailable: `K_Q` has no matching condition in the
current architecture. The same missing coefficient blocks the long-wavelength
causality test.

## 1. Cubic vertex

Expanding `E=A|v+\nabla\pi|^3` to third order in
`(d_x,d_y,d_z)=\nabla\pi` around `v=(q,0,0)` gives

\[
E_{\rm quad}=3Aq\,d_x^2+\tfrac32Aq\,d_y^2+\tfrac32Aq\,d_z^2,
\]
\[
E_{\rm cubic}=A\,d_x^3+\tfrac32A\,d_xd_y^2+\tfrac32A\,d_xd_z^2.
\]

The accompanying script verifies both expressions directly by symbolic series
expansion. The quadratic term agrees with the Stage-A Hessian
`diag(6Aq,3Aq,3Aq)`.

## 2. Restricted NDA estimate

With dimensionless `psi` and `pi`, the time-normalized field is
`chi=sqrt(K_Q) pi`. The longitudinal cubic interaction becomes

\[
-\frac{A}{K_Q^{3/2}}(\partial_x\chi)^3.
\]

The inverse square root of this dimension-`-2` coefficient gives the displayed
IR NDA derivative scale. This step normalizes time, not the full anisotropic
quadratic action; it therefore must not be promoted to a physical cutoff.

## 3. Classification

**Mechanically verified:**

- the cubic vertex around the declared nonzero-gradient background;
- the restricted formula
  `Lambda_NDA,long^(IR) ~ K_Q^(3/4)/sqrt(A)`.

**Open:**

- a matching condition and numeric value for `K_Q`;
- transverse-mode canonical normalization;
- `k^4`-dominated Lifshitz power counting;
- a loop or unitarity analysis establishing the physical EFT cutoff
  `Lambda_EFT`;
- comparison of `k_light` with that physical `Lambda_EFT`, not merely with the
  restricted IR NDA scale.

## 4. Reproduction

```powershell
python Analysis/UVIR/UVIR-003/uvir003_force_strong_coupling_estimate.py
```

Expected footer:

```text
UVIR-003 Stage B item 9 (longitudinal, IR-only): cubic vertex VERIFIED
Longitudinal IR NDA scale (time-normalized, not physical cutoff): K_Q**(3/4)/sqrt(A)
Numeric evaluation: BLOCKED on missing K_Q matching condition
STATUS: OPEN_PENDING_K_Q_MATCHING_CONDITION
```
