# TOP-001 S2 — CBR-001 bridge (referee-grade scaffold)

**Branch:** `recovery/v12-core-architecture`<br>
**Status:** `OPEN_SCAFFOLD_ONLY`<br>
**physics_pass:** **false** (always)<br>
**Subgate (template only):** `PASS_TOP001_S2_CBR001_BRIDGE_TEMPLATE`<br>
**Not:** TOP research-gate PASS · not physics PASS<br>

## Purpose

Bridge **TOP-owned** fixed-volume rectangular $T^3$ geometry samples into the
existing **CBR-001** free-scalar Casimir lattice tool
(`casimir_t3_lattice.lattice_stress`), which is the **numerical authority**.

## Samples (fixed $V$)

| Sample | Chart | Intent |
|--------|-------|--------|
| cubic | $(\alpha_x,\alpha_y)=(0,0)$ | pressure isotropy control |
| biaxial | $(0.12,0.12)$ ⇒ $L_x=L_y\neq L_z$ | genuine two-equal-length biaxial |
| triaxial | $(0.25,-0.10)$ | three distinct $L_i$ |

\[
L_i = V^{1/3}\,e^{\alpha_i},\qquad \alpha_x+\alpha_y+\alpha_z=0.
\]

## Checks

1. $V$ finite and $>0$; cutoff a positive integer; cutoffs strictly increasing
2. Fixed-volume preservation
3. Genuinely triaxial sample
4. Cubic pressure isotropy
5. Anisotropic pressure (biaxial + triaxial)
6. Axis-permutation covariance of $(\rho,p_i)$
7. Uniform-length scaling $\rho,p\propto s^{-4}$ via CBR `scaling_test`
8. Multi-cutoff refinement: **measured** successive $|\Delta\rho|/|\rho|$ must
   **improve** (final pair change $<$ first pair change) — no invented absolute
   continuum tolerance
9. Malformed / non-finite input rejection
10. Claim firewall

## Reproduce

```powershell
python Analysis\TOP\TOP-001\top001_s2_cbr001_bridge_audit.py
# expect: PASS_TOP001_S2_CBR001_BRIDGE_TEMPLATE
# physics_pass: False
# research_gate_status: OPEN_SCAFFOLD_ONLY
```

Outputs:

```text
Analysis/TOP/TOP-001/outputs/top001_s2_cbr001_bridge_summary.json
Analysis/TOP/TOP-001/outputs/top001_s2_cbr001_bridge_summary.sha256
```

## Explicit non-claims

- No TOP research-gate PASS; no `physics_pass`
- No $S_{\mathrm{mod}}$ / dynamical shape potential
- No twisted $E_2/E_3$ preference
- No persistent free-field $13/12$ attractor
- No $H_0$, $a_0$, $C_{\mathrm{obs}}$, or cosmology
- Template PASS ≠ physics PASS

## Limitations

Finite lattice cutoff $N$; free massless scalar on rectangular $T^3$ only;
fixed BC / fixed volume; no driven stress (CBR-002); continuum extrapolation
is diagnostic only.
