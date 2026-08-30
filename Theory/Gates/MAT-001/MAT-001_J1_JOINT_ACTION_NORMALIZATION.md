# MAT-001 — J1 joint-action normalization identity

**Date:** 2026-08-04
**Branch:** `recovery/v12-core-architecture`
**Subgate:** `PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY`
**Research-gate status:** `BLOCKED_MATCHING_INPUTS_OPEN`
**V numeric status:** **NOT_COMPUTED**
**MAT-001 PASS:** **false**
**UVIR-003:** **IN_PROGRESS**
**physics_pass:** **false**

## Question

What does the invariant

\[
V=\frac{C_m}{\sqrt{K_Q}}
\]

become when the matter vertex and kinetic normalization genuinely originate in
one parent action?

## Same-action identity

Declare a parent field $\phi$ with the relevant quadratic kinetic coefficient
and matter vertex

\[
\mathcal L_{\rm parent}\supset
\frac{Z_\phi}{2}(U\!\cdot\!\nabla\phi)^2
-g_\phi\rho_b\phi,
\qquad Z_\phi>0.
\]

For a positive field-chart map $\psi=f_\phi\phi$, substitution gives

\[
K_Q=\frac{Z_\phi}{f_\phi^2},
\qquad
C_m=\frac{g_\phi}{f_\phi},
\qquad
V=\frac{g_\phi}{\sqrt{Z_\phi}}.
\]

The same expression is the source coefficient of the canonically normalized
field $\phi_c=\sqrt{Z_\phi}\phi$. Thus the chart-ratio route and the direct
canonical-residue route are algebraically identical when both terms come from
one declared action.

## Covariance checks

- Parent rescaling $\phi'=r\phi$ gives
  $Z_\phi'=Z_\phi/r^2$ and $g_\phi'=g_\phi/r$, leaving
  $g_\phi'/\sqrt{Z_\phi'}=g_\phi/\sqrt{Z_\phi}$.
- IR rescaling $\psi'=s\psi$ gives $K_Q'=K_Q/s^2$ and
  $C_m'=C_m/s$, leaving $C_m'/\sqrt{K_Q'}=V$.
- Zero or negative $Z_\phi$, zero chart scale, non-finite inputs, and an
  upstream premature `V=COMPUTED` claim are rejected by negative controls.

## What this advances

J1 replaces an abstract chart-invariance statement with an explicit one-action
normalization formula. It also isolates the remaining physical task: obtain
both $Z_\phi$ and $g_\phi$ from the same microscopic action, or calculate
the equivalent on-shell source residue directly.

No numerical value follows from this template. The symbols $Z_\phi$ and
$g_\phi$ remain unmatched physical inputs, and the map to the live IR field
must still be justified.

## Reproduce

```powershell
python Analysis\MAT\MAT-001\J1_JOINT_ACTION\mat001_j1_joint_action_normalization.py
# expect: PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY
# V numeric: NOT_COMPUTED
# MAT PASS: false; UVIR: IN_PROGRESS; Stage 4A: closed
```

Generated evidence:

- `Analysis/MAT/MAT-001/J1_JOINT_ACTION/outputs/mat001_j1_joint_action_normalization_summary.json`
- `Analysis/MAT/MAT-001/J1_JOINT_ACTION/outputs/mat001_j1_joint_action_normalization_summary.sha256`

## Explicit non-claims

- No numerical $V$ or $K_Q$
- No microscopic derivation of $Z_\phi$ or $g_\phi$
- No assertion that the template parent action is the ITSM microscopic action
- No MAT-001 or UVIR-003 PASS
- No Stage 4A unlock
- No downstream Derived, SPARC, $H_0$, or dual-RAR claim
