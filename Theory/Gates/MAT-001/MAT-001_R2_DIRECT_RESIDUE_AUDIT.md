# MAT-001 — R2 direct residue audit (canonical response template)

**Branch:** `recovery/v12-core-architecture`
**UVIR-003:** **IN_PROGRESS**
**MAT-001:** **BLOCKED**
**physics_pass:** **false**
**V_status:** **NOT_COMPUTED** (locked in this audit)
**Stage 4A:** **CLOSED**
**Subgate (audit only):** `PASS_MAT001_R2_DIRECT_RESIDUE_AUDIT`

## Question

In the quadratic template below, can the redefinition-invariant vertex residual
$V=C_m/\sqrt{K_Q}$ be identified with the canonical matter response poles
without quoting a standalone numerical $K_Q$?

## Quadratic template (not live eigenmode extraction)

\[
L_2=\tfrac12\,\psi\,D\,\psi - C_m\rho_b\psi,\qquad
D=K_Q P,\qquad
\chi=\sqrt{K_Q}\,\psi.
\]

Then

\[
\frac{\chi}{\rho_b}=\frac{V}{P},
\qquad
S_{\mathrm{eff}}[\rho_b]\propto -\tfrac12 V^2\,\rho_b\,P^{-1}\rho_b.
\]

### Coefficient roles (do not collapse)

| Object | Coefficient |
|--------|-------------|
| Canonical matter-source **vertex** | $V$ |
| Mixed field–source response pole ($\chi/\rho_b$) | $V$ |
| Source–source exchange pole | $V^2$ |

Constraint reduction, physical mode projection, and same-action matching to the
live UVIR eigenmode remain **absent**. This is a structural template identity,
not a numeric extraction from the force-sector physical basis.

## Verdict

| Level | Answer |
|-------|--------|
| Form (template) | **YES** — vertex $V$; mixed pole $V$; exchange $V^2$; standalone numeric $K_Q$ need not be quoted once $V$ is known |
| This branch | **NOT_COMPUTED** — no live residue evaluation; promotion path removed |

## Domain

- $K_Q>0$ and positive chart scale (finite)
- $C_m$ **signed** finite nonzero (sign of $V$ retained)
- Reject NaN / $\pm\infty$ via `math.isfinite`

## Upstream contracts

| Artifact | Required |
|----------|----------|
| Matching route program | `PASS_MATCHING_ROUTE_PROGRAM_OPEN`, $K_Q$ NOT_DERIVED, MAT BLOCKED |
| $K_Q$ inventory | `PASS_KQ_MATCHING_INVENTORY_OPEN`, $K_Q$ NOT_DERIVED |
| Scoped MAT | `PASS_MAT001_SCOPED_CALCULATION_PROVISIONAL`, $V$ NOT_COMPUTED, `mat001_pass: false` |
| **J1 joint action** | `PASS_MAT001_J1_JOINT_ACTION_NORMALIZATION_IDENTITY`, $V$ NOT_COMPUTED, `V_form_status=SAME_ACTION_IDENTITY_DERIVED`, `mat001_pass: false`, `physics_pass: false` |

Force Track-A summary is **optional** (absence allowed).

## Reproduce (Windows PowerShell)

```powershell
python Analysis\MAT\MAT-001\R2_DIRECT_RESIDUE\mat001_r2_direct_residue_audit.py
# expect exit code 0
# STATUS: PASS_MAT001_R2_DIRECT_RESIDUE_AUDIT
# V_status: NOT_COMPUTED
```

Outputs:

```text
Analysis/MAT/MAT-001/R2_DIRECT_RESIDUE/outputs/mat001_r2_direct_residue_audit_summary.json
Analysis/MAT/MAT-001/R2_DIRECT_RESIDUE/outputs/mat001_r2_direct_residue_audit_summary.sha256
```

## Blockers to a future computed $V$

1. Declared microscopic action with kinetic + matter couplings
2. Constraint reduction
3. Mode projection / same-action matching to live IR force field
4. **Separate provenance contract** (this audit never promotes $V$ from flags alone)

## Explicit non-claims

No MAT PASS · no physics_pass · no UVIR full PASS · no Derived $K_Q$ · no computed $V$ · no Stage 4A unlock · no live eigenmode extraction · no SPARC/$H_0$/dual RAR · audit PASS $\neq$ numeric extraction.
