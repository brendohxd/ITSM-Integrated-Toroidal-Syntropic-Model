# MAT-001 J2 — Basis-covariant physical-mode projection

**Date:** 2026-08-05
**Branch:** `recovery/v12-core-architecture`
**Subgate:** `PASS_MAT001_J2_BASIS_COVARIANT_MODE_PROJECTION_TEMPLATE`
**Projection identity:** `DERIVED_TEMPLATE`
**Live action export:** `NOT_PROVIDED`
**V status:** **NOT_COMPUTED**
**MAT-001:** **BLOCKED**
**UVIR-003:** **IN_PROGRESS**
**Stage 4A:** **closed**
**physics_pass:** **false**

## Purpose

Derive the correct canonical matter-source coupling to a physical dynamical
mode after algebraic constraints are eliminated, and prove that the result is
invariant under invertible field-basis changes.

This provides the method needed for a later live-action match. The present
audit uses exact rational template matrices and does not claim that they are
the ITSM UVIR matrices.

## Quadratic convention

For dynamical fields \(x\), algebraic constraints \(z\), and matter source
\(\rho\), take

\[
L=\frac12\dot x^T K\dot x-\frac12x^TAx-x^TBz-\frac12z^TCz
  +\rho(d^Tx+h^Tz).
\]

The constraint equation gives

\[
z=C^{-1}(\rho h-B^Tx),
\]

so the reduced operator and source covector are

\[
A_{\rm eff}=A-BC^{-1}B^T,
\qquad
c_{\rm eff}=d-BC^{-1}h.
\]

For any nonzero physical-mode direction \(u\), its canonical source coupling
is

\[
g_{\rm can}=\frac{c_{\rm eff}^Tu}{\sqrt{u^TKu}}.
\]

The single-field limit is \(g_\phi/\sqrt{Z_\phi}\), reproducing the J1
same-action structural identity for \(V\) without assigning it a number.

## Basis covariance

Under \(x=Ry\) and \(z=Sw\),

\[
K_y=R^TKR,
\quad
c_{{\rm eff},y}=R^Tc_{\rm eff},
\quad
u_y=R^{-1}u.
\]

Therefore \(g_{{\rm can},y}=g_{\rm can}\). The executable verifies this
exactly for two generalized eigenmodes while also transforming the constraint
sector and reproducing the Schur-reduced blocks.

## Executable record

```powershell
python Analysis\MAT\MAT-001\J2_MODE_PROJECTION\mat001_j2_basis_covariant_mode_projection.py
# expect: PASS_MAT001_J2_BASIS_COVARIANT_MODE_PROJECTION_TEMPLATE
```

Outputs:

```text
Analysis/MAT/MAT-001/J2_MODE_PROJECTION/outputs/mat001_j2_basis_covariant_mode_projection_summary.json
Analysis/MAT/MAT-001/J2_MODE_PROJECTION/outputs/mat001_j2_basis_covariant_mode_projection_summary.sha256
```

Accepted deterministic SHA-256:

```text
599065CD407A499BE8414FFF226C10889CA6BFE668E74A2C8E11E251D3C0D82E
```

## Checks

Nine checks cover:

1. exact fail-closed handoff input;
2. algebraic-constraint elimination;
3. generalized \(K\)-orthonormal modes;
4. Schur-block covariance;
5. canonical coupling invariance;
6. the J1 single-field limit;
7. inconsistent-projection negative controls;
8. malformed matrix and vector rejection; and
9. live-export and claim firewalls.

The negative controls demonstrate that the result changes if the source
covector or mode vector is not transformed, Euclidean normalization replaces
the kinetic norm, or constraint-source dressing is omitted.

## Live-action blocker

This template does not receive the following objects from one declared live
UVIR action chart:

- the dynamical kinetic metric \(K\);
- the algebraic constraint matrix \(C\) and mixing block \(B\);
- the matter source covectors \(d,h\); and
- the physical mode direction \(u\) in that same chart.

Until those objects have explicit action-level provenance, the projection
method cannot produce a numerical \(V\).

## Scientific boundary

This is a symbolic method PASS, not a live matching or physics PASS. It does
not identify a live eigenmode, derive \(K_Q\), compute \(V\), reopen Stage 4A,
pass MAT-001 or UVIR-003, or authorize downstream Derived observables or a new
manuscript freeze.
