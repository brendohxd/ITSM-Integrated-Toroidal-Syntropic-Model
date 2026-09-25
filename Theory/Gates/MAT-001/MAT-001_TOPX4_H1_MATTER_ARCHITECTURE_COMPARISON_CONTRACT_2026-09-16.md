# MAT-001 TOP-X4 H1 physical-matter architecture comparison contract

**Date:** 2026-09-16  
**Status:** `FROZEN_NON_PROMOTING_ARCHITECTURE_COMPARISON`  
**Parent:** unchanged `X4-S2F3`  
**Allowed effect:** route recommendation only  
**Gate effect:** none

## 1. Question

For a future TOP-X4 child action intended to address MAT-001 H1, which one
matter architecture should be investigated first:

1. physical matter propagating in the smooth five-dimensional bulk; or
2. physical matter localized on a four-dimensional hypersurface and coupled
   minimally to its induced metric?

The comparison must not add either sector to the frozen parent. It may derive
kinematic source-coupling identities from the already verified Einstein-frame
metric chart, but it may not call those identities a physical MAT residue.

## 2. Frozen reduction chart

Use the verified TOP-X4 Einstein-frame ansatz

\[
 ds_5^2=r^{-1}g_{\mu\nu}dx^\mu dx^\nu
 +R_{\rm ref}^2r^2dy^2,
 \qquad
 \sigma=\sqrt{\frac32}M_{\rm Pl}\ln r.
\]

The volume and inverse-metric scalings are

\[
 \sqrt{-G}=R_{\rm ref}r^{-1}\sqrt{-g},
 \qquad G^{\mu\nu}=r g^{\mu\nu}.
\]

These equations are a kinematic reduction chart. They do not supply a stable
background or a physical eigenmode.

## 3. Exact controls to execute

### 3.1 Brane-induced metric control

For a matter hypersurface at fixed `y`, the induced metric is

\[
 \gamma_{\mu\nu}=r^{-1}g_{\mu\nu}
 =A_b^2(\sigma)g_{\mu\nu},
 \qquad
 A_b(\sigma)=r^{-1/2}
 =\exp\!\left[-\frac{\sigma}{\sqrt6M_{\rm Pl}}\right].
\]

The kinematic Einstein-frame trace coupling is therefore controlled by

\[
 \alpha_b\equiv\frac{d\ln A_b}{d\sigma}
 =-\frac{1}{\sqrt6M_{\rm Pl}}.
\]

This is a source-covector component in the unreduced scalar system, not the
physical H1 residue. The sign must still be transported through the R4 source
convention and the complete constrained mode projection.

### 3.2 Bulk zero-mode scalar control

For a minimally coupled massive five-dimensional real scalar `X`, use the
reference-circle normalization

\[
 X(x,y)=\left(2\pi R_{\rm ref}\right)^{-1/2}x_0(x)+\cdots.
\]

The four-dimensional zero-mode kinetic coefficient is independent of `r`,
while

\[
 m_{x_0}^2(\sigma)=m_5^2r^{-1},
 \qquad
 m_{x_0}(\sigma)=m_5
 \exp\!\left[-\frac{\sigma}{\sqrt6M_{\rm Pl}}\right].
\]

Thus this minimal massive-scalar control has the same logarithmic radion-mass
derivative as the brane-induced metric. It does not establish a universal
Standard Model matter action: gauge, Higgs, Yukawa, chiral-fermion and anomaly
structure must be specified together.

### 3.3 Operator-shape test

The radion inherited from Einstein--Hilbert reduction has a derivative-
quadratic kinetic operator. Track A instead requires a spatial operator
homogeneous of degree three in first derivatives, `Y^(3/2)` or
`|grad psi|^3`.

An invertible point-field redefinition changes field-dependent coefficients
but preserves derivative homogeneity. Therefore a canonical radion cannot be
identified directly with the Track-A field by a constant normalization or
regular point transformation. The direct map must be rejected unless new
dynamics produces the required nonanalytic IR operator. A constrained mixed
radion--condensate mode remains open.

## 4. Non-numerical comparison criteria

No arbitrary weighted score is permitted. Compare exact structural
requirements instead.

| Requirement | Bulk physical matter | Brane-localized physical matter |
|---|---|---|
| Preserves the current smooth-circle geometry | yes at the classical action level | no; a localized defect/action is added |
| Avoids physical-matter KK towers | no | yes by construction |
| Four-dimensional chiral matter without an added bulk chirality mechanism | not supplied on the current smooth `S1` | possible within the declared 4D matter action |
| Universal physical metric visible at the source vertex | requires a complete reduced bulk matter theory | explicit induced metric at kinematic level |
| Junction/localized counterterm problem | absent | compulsory |
| Changes the S2F3 determinant and stabilization problem | yes, through the full bulk spectrum | yes, through localized stress, boundary data and counterterms |
| Directly supplies Track-A `Y^(3/2)` | no | no |

## 5. Decision rule

Recommend the brane-induced-metric option as the **lead source-projection
candidate** only if all of the following remain explicit:

- it is a new child theory, not a modification silently inherited by S2F3;
- the hypersurface action, localization, tension, compact consistency,
  junction conditions and localized counterterms remain open;
- `alpha_b` is only an unreduced kinematic source component;
- the direct radion-to-Track-A map is rejected;
- only a future constrained mixed mode may be tested against H1; and
- no numerical `K_Q`, `V`, MAT or Stage-4A status follows.

Retain bulk physical matter as the comparison/control route. Do not call it a
physical Standard Model completion unless its chirality, complete KK spectrum,
interactions, anomalies, cutoff and loop contribution to radion stabilization
are frozen.

## 6. Primary-source anchors

- Appelquist, Cheng and Dobrescu, *Bounds on Universal Extra Dimensions*,
  Phys. Rev. D 64, 035002 (2001),
  <https://arxiv.org/abs/hep-ph/0012100>: putting Standard Model fields in the
  bulk creates physical KK towers and a compactification-scale phenomenology.
- Papavassiliou and Santamaria, *Chiral fermions and gauge-fixing in
  five-dimensional theories*, Phys. Rev. D 63, 125014 (2001),
  <https://arxiv.org/abs/hep-ph/0102019>: a chiral four-dimensional fermion
  construction uses orbifold/parity structure and additional fermionic data.
- Kofman, Martin and Peloso, *Exact identification of the radion and its
  coupling to the observable sector*, Phys. Rev. D 70, 085015 (2004),
  <https://arxiv.org/abs/hep-ph/0401189>: radion/bulk-scalar mixing requires
  quadratic-action diagonalization and normalized physical modes before a
  brane coupling is physical.
- Maeda and Wands, *Dilaton-gravity on the brane*, Phys. Rev. D 62, 124009
  (2000), <https://arxiv.org/abs/hep-th/0008188>: localized matter and bulk
  scalar gravity induce nontrivial effective brane equations and exchange.

These sources constrain architecture. They do not validate ITSM or supply its
missing physical Hessian.

## 7. Binding non-promotion boundary

```text
comparison_status=FROZEN_NON_PROMOTING
parent_action_changed=false
lead_candidate=UNDECIDED_UNTIL_EXECUTION
child_freeze_authorized=false
direct_radion_track_a_map=NOT_DERIVED
physical_mode=NOT_IDENTIFIED
signed_residue=NOT_COMPUTED
K_Q=NOT_DERIVED
V=NOT_COMPUTED
MAT-001=BLOCKED
Stage4A=CLOSED
physics_pass=false
gate_effect=NONE
```
