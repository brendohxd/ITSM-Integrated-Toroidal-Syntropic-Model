# UVIR-003 Stage B — $K_Q$ matching inventory

Date: 2026-08-03

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS** (inventory + invariants; **$K_Q$ not derived**)

Subgate:
`PASS_KQ_MATCHING_INVENTORY_OPEN`

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

Numeric $K_Q$: **NOT_DERIVED**

## Purpose

Close the “no matching condition for $K_Q$” bookkeeping gap *as a research
object*: list redefinition invariants, catalogue matching routes, and state
exactly what a future Derived claim must compute. This replaces ad-hoc
speculation with a structured Open/Conditional map.

## Field redefinition

Under $\psi \mapsto s\psi$ ($s>0$):

| Quantity | Scales as |
|----------|-----------|
| $K_Q$ | $s^{-2}$ |
| $A$ | $s^{-3}$ |
| $\gamma$ | $s^{-2}$ |
| $C_m$ | $s^{-1}$ |
| background $q=\|\nabla\psi\|$ | $s$ |

### Invariants (verified symbolically)

| Invariant | Role |
|-----------|------|
| $A q / K_Q$ | **Primary** long-wavelength causality ratio |
| $A / K_Q^{3/2}$ | NDA / unitarity $\Lambda_\parallel = 1/\sqrt{A/K_Q^{3/2}}$ |
| $\gamma / K_Q$ | Regulator relative strength |
| $C_m / \sqrt{K_Q}$ | Matter–force mixed normalization |
| $C_m^{3/2}/\sqrt{A}$ | Related to $C_{\mathrm{obs}}$ architecture combo |

**Important:** $\Lambda_\parallel = K_Q^{3/4}/\sqrt{A}$ is fully redefinition-invariant
(equals $1/\sqrt{A/K_Q^{3/2}}$). Absolute $K_Q$ alone is not.

## Causality

\[
R_c(\theta)=\frac{3Aq(1+\cos^2\theta)}{K_Q}
=3\Bigl(\frac{Aq}{K_Q}\Bigr)(1+\cos^2\theta),
\qquad
q_\times(\theta)=\frac{K_Q}{3A(1+\cos^2\theta)}.
\]

Long-wavelength superluminality when $R_c>1$ (Stage-A addendum convention).

## Matching routes

| ID | Status | Fixes (if successful) |
|----|--------|------------------------|
| **R1** dimensional $K_Q=k_Q M_P^2$ | **Conditional** candidate | $K_Q/M_P^2=k_Q$ only |
| **R2** matter vertex (MAT-001) | **Open** (blocked) | $C_m,C_{\mathrm{obs}},K_Q$ class invariants |
| **R3** condensate / UV completion | **Open** | $K_Q$ from $S_\Phi+S_\psi$ |
| **R4** regulator $k_{\rm cross}$ | **Open** | $\gamma/K_Q$ mainly |
| **R5** AQUAL-class IR anchor | **Conditional** phenom | $C_{\mathrm{obs}}$; not $K_Q$ alone |

R1 with naive $(k_Q,C_{\rm IR})=(1,2/3)$ still yields $q_\times\sim(0.375\text{–}0.75)\,a_0$ —
**priority flag only** (`SPECULATIVE_NOT_A_DERIVATION`), not a theory failure claim.

## Non-claims

- No Derived numeric $K_Q$.  
- No confirmation of R1.  
- No MAT-001 unlock.  
- No UVIR-003 full-gate close.

## What “Derived $K_Q$” would require

1. Choose a primary route (default long-term: **R2** when UVIR admits MAT).  
2. State premises as Conditional.  
3. Compute invariant $Aq/K_Q$ or $A/K_Q^{3/2}$ from that calculation.  
4. Re-evaluate $q_\times$ and the declared unitarity window.  
5. Update the claim ledger only then.

## Reproduction

```powershell
conda activate itsm_env
python Analysis\UVIR\UVIR-003\uvir003_kq_matching_inventory.py
# expect: PASS_KQ_MATCHING_INVENTORY_OPEN
```

## Next

- **Done:** R2 interface + R3 sketch in  
  `UVIR-003_STAGE_B_MATCHING_ROUTE_PROGRAM.md`  
  (`PASS_MATCHING_ROUTE_PROGRAM_OPEN`). MAT target $V=C_m/\sqrt{K_Q}$.  
- MAT-001 remains **blocked** for Derived until UVIR full pass or Conditional handoff.  
- Optional: dig-harder R3 from $S_\Phi$; residual M2 IR HOLD.  

