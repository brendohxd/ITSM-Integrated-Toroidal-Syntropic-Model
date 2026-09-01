# TOP-001 Stage S1 — Fixed-boundary full-triaxial rectangular $T^3$ audit

**Date:** 2026-08-04
**Branch:** `recovery/v12-core-architecture`
**Status:** `OPEN_SCAFFOLD_ONLY`
**physics_pass:** **false** (always)
**Revision:** S1 hardened continuation (refinement ≤1%, scale invariance, smooth cubic)

## Purpose

Extend the **reviewed biaxial** fixed-volume scaffold with an independent
**full-triaxial** rectangular $T^3$ geometry audit at fixed volume, using
**two independent log-shape coordinates**.

Does **not** replace or overwrite:

```text
Analysis/TOP/TOP-001/top001_shape_template_audit.py
Analysis/TOP/TOP-001/outputs/top001_shape_template_audit_summary.json
```

## Log-shape chart

\[
L_i = V^{1/3}\,e^{\alpha_i},\qquad
\alpha_x+\alpha_y+\alpha_z=0,\qquad
\alpha_z=-(\alpha_x+\alpha_y).
\]

Independent coordinates: $(\alpha_x,\alpha_y)$.
Cubic limit: $(\alpha_x,\alpha_y)=(0,0)$.

## Executable

```text
Analysis/TOP/TOP-001/top001_s1_triaxial_fixed_volume_audit.py
```

```powershell
python Analysis\TOP\TOP-001\top001_s1_triaxial_fixed_volume_audit.py
# expect: PASS_TOP001_S1_TRIAXIAL_FIXED_VOLUME_TEMPLATE
# physics_pass: False
```

Outputs:

```text
Analysis/TOP/TOP-001/outputs/top001_s1_triaxial_fixed_volume_summary.json
Analysis/TOP/TOP-001/outputs/top001_s1_triaxial_fixed_volume_summary.sha256
```

## Checks (hardened template)

| Check | Intent |
|-------|--------|
| Fixed volume preserved | $\prod L_i=V$, $\sum\alpha_i=0$ |
| Cubic limit | $A\approx 0$ |
| Non-cubic diagnostics | $A>0$ off cubic (sample chart, not theorem) |
| Smooth approach to cubic | small $\alpha$ ⇒ small $A$ relative to strong triaxial |
| Axis-permutation covariance | moments transform; $A$ invariant |
| Refinement | relative $\Delta A \le 1\%$ default (biaxial review parity) |
| Volume scale invariance | same $\alpha$, $V$ vs $8V$ ⇒ same $\hat k$ moments |
| Malformed inputs | nonpositive/NaN/Inf $V$, nonfinite $\alpha$, bad $n_{\max}$ rejected |
| Claim firewall | packaging flags false |

## Explicit non-claims

- No modulus action $S_{\mathrm{mod}}$
- No Casimir tensor / free-field stress recompute
- No twisted $E_2/E_3$ preference
- No backreaction
- No $13/12$, $H_0$, $a_0$, $C_{\mathrm{obs}}$, cosmology
- Not a TOP research-gate PASS beyond template S1 geometry

## Relation to gate stages

Implements GATE_SPEC Stage **S1** (S1.1–S1.6) for the full-triaxial chart under
Route **T1** fixed BC. Stages S2+ remain future work. No Project Relay involvement.
