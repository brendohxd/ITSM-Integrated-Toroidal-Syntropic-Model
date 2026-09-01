# MAT-001 declared $S_{\rm int}$ and $d,h$ placement

**Status:** `PASS_MAT001_S_INT_DH_DECLARATION_LIVE_CHART_BLOCKED`  
**$S_{\rm int}$:** `DECLARED_CONDITIONAL_FORM`  
**IR $d,h$:** `FORM_DERIVED_IR_SINGLE_FIELD_TEMPLATE`  
**Live UVIR $d,h$:** `NOT_EXPORTED`  
**MAT-001:** **BLOCKED**  
**V:** **NOT_COMPUTED**  
**UVIR-003:** **IN_PROGRESS**  
**Stage 4A:** **CLOSED**  
**Physics pass:** `false`

## Purpose

After free-sector $K,C$ export, the next critical-path gap is the matter
source channel. This checkpoint:

1. declares the Conditional architecture/J1 interaction form;
2. derives IR single-field source covectors $(d,h)$ in the J2 convention;
3. verifies that they recover $|V|=C_m/\sqrt{K_Q}$ in that IR chart;
4. tests placement into the live free-sector UVIR chart and fails closed.

## Declared interaction

\[
S_{\rm int}\supset\int\mathrm{d}t\,\mathrm{d}^3x\,(-C_m\rho_b\psi)
\qquad\text{(architecture weak-field / R2 template)}
\]

Parent chart equivalent: $-g_\phi\rho_b\phi$ with $\psi=f_\phi\phi$, inducing
$C_m=g_\phi/f_\phi$.

This is a **Conditional form declaration**, not a microscopic match of
$g_\phi$, $Z_\phi$ or a live UVIR force completion.

## IR template export

Under the J2 source sector $\rho(d^Tx+h^Tz)$ with $\rho=\rho_b$, single
dynamical field $x=(\psi)$ and no algebraic constraints:

| Object | Value |
|---|---|
| $d$ | $(-C_m)$ |
| $h$ | empty |
| $c_{\rm eff}$ | $(-C_m)$ |
| $\lvert g_{\rm can}\rvert$ | $C_m/\sqrt{K_Q}=V$ |

## Live free-sector placement

The free-sector chart is $(R,\delta\rho,\vartheta;\delta N,\Sigma)$. It does
**not** contain the IR force field $\psi$. Condensate $\delta\rho$ is not
baryonic $\rho_b$. Therefore live UVIR free-sector $d,h$ remain
`NOT_EXPORTED`.

### Rejected substitutions

- $\delta\rho$ as $\rho_b$
- diagnostic $Q_\rho,Q_\chi$ impulses as $d,h$
- Newtonian $\Phi_N$ matter coupling as the force vertex
- silently pasting IR-template $d,h$ into the free-sector bundle

## Decision

The interaction form is declared and the IR $d,h$ algebra is executable.
Live same-action matching remains blocked until the force field (or a
justified map onto it) lives in the quadratic action used for MAT wiring.

## Reproduction

```text
python -B Analysis/MAT/MAT-001/S_INT_DH_EXPORT/mat001_s_int_dh_export_audit.py
```

Expected:

```text
STATUS: PASS_MAT001_S_INT_DH_DECLARATION_LIVE_CHART_BLOCKED
```

Evidence:

- `Analysis/MAT/MAT-001/S_INT_DH_EXPORT/outputs/mat001_s_int_dh_export_summary.json`
- `Analysis/MAT/MAT-001/S_INT_DH_EXPORT/outputs/mat001_s_int_dh_export_summary.sha256`

```text
SHA-256: AF8488CE3F4F2FC985E108A123BEA70B21408755EB6A6A26E1D67DE97402021E
```

Two consecutive runs are byte-identical. Internal mutations reject promotion of
live $d,h$ export, numeric matching, $V$, MAT pass and physics pass.

## Serial next

Embed $\psi$ (or parent $\phi$) with declared $S_{\rm int}$ in the live
quadratic used for matching, extract action-level $d,h$ there, resolve the
free-sector $M_v$ residual, then select $u$ and rerun live J2.
