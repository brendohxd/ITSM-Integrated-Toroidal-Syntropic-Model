# UVIR-003 Stage B — Causality domain under Conditional matching (M3 documentation)

Date: 2026-08-03

Branch: `recovery/v12-core-architecture`

Calculation status: **PASS** (domain mapped under explicit Conditional premises)

Subgate:
`PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING`

Claim status: **Conditional** (not Derived)

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED**

Master Plan criterion: **M3** (causality in declared domain) — **documented**, not closed as Derived

## Purpose

Map the Stage-A long-wavelength causality window \(R_c\le 1\) under an **explicit
Conditional matching hypothesis set** (R1 structure from the \(K_Q\) inventory /
Conditional \(K_Q\) estimate), without promoting \(k_Q\) or \(C_{\mathrm{IR}}\)
to Derived.

This is the Master Plan critical-path step: **document M3 under Conditional
premises**, not fake-close UVIR-003.

## Premises (all Conditional)

| Symbol | Premiss |
|--------|---------|
| \(K_Q\) | \(K_Q = k_Q M_P^2 = k_Q/(8\pi G)\) — R1 dimensional analogy |
| \(A\) | \(A = C_{\mathrm{IR}}/(12\pi G\,a_0)\) — architecture force normalization |
| \(R_c\) | \(R_c(\theta)=3 A q (1+\cos^2\theta)/K_Q\); causal when \(R_c\le 1\) |
| \(q_\times\) | \(q_\times(\theta)/a_0 = k_Q/[2 C_{\mathrm{IR}}(1+\cos^2\theta)]\) |
| \(k_Q,C_{\mathrm{IR}}\) | Free Conditional Wilson coefficients on the scan grid |

Analytic identities (machine-checked):

\[
\frac{q_\times}{a_0}=\frac{k_Q}{2 C_{\mathrm{IR}}(1+\cos^2\theta)},\qquad
R_c=\frac{q/a_0}{q_\times/a_0}.
\]

## Scan

Script:
`Analysis/UVIR/UVIR-003/uvir003_causality_domain_under_conditional_matching.py`

| Grid | Values |
|------|--------|
| \(k_Q\) | \(0.25, 0.5, 1, 2, 4\) |
| \(C_{\mathrm{IR}}\) | \(0.5, 2/3, 1, 1.5\) |
| \(q/a_0\) | \(0.1 \ldots 3\) |
| directions | parallel (\(\cos\theta=1\)), perp (\(\cos\theta=0\)) |

Outputs:

- `outputs/uvir003_causality_domain_conditional_summary.json`
- `outputs/uvir003_causality_domain_conditional_scan.csv` (320 rows)
- `outputs/uvir003_causality_domain_summary_table.csv`

## Headline results (Conditional)

| Point | Parallel \(q_\times/a_0\) | Note |
|-------|--------------------------|------|
| Naive \((k_Q,C_{\mathrm{IR}})=(1,2/3)\) | **0.375** | Background gradients \(\sim a_0\) sit **outside** this Conditional causal window |
| \((1,0.5)\) parallel | 0.5 | Milder |
| \((2,2/3)\) parallel | 0.75 | Still \(q\sim a_0\) marginal/outside |
| \((4,0.5)\) parallel | 2.0 | Larger \(k_Q\) opens room for \(q\sim a_0\) |

**Priority flag (not theory failure):** under the naive R1 point, the
Conditional causal domain does **not** cover order-\(a_0\) gradients. That
motivates real matching (R2 MAT / R3 UV data), not a packaging claim that
“the theory is superluminal.”

## Explicit non-claims

| Claim | Status |
|-------|--------|
| \(k_Q\) Derived | **NOT_DERIVED** |
| \(C_{\mathrm{IR}}\) Derived | **NOT_DERIVED** |
| \(K_Q\) numeric from action | **NOT_DERIVED** |
| UVIR-003 M3 closed as Derived | **NO** — still PARTIAL until matched invariants |
| Physical cutoff (M6) | **OPEN** |
| MAT-001 unlock | **BLOCKED** |

## Scientific boundary

This subgate makes M3 **referee-documentable** under Conditional R1 premises.
It does **not** replace matching. Full UVIR-003 PASS still requires matched
invariants (toward M6) and a programme decision on residual PARTIAL items (M2
IR HOLD, optional optical theorem scope).

## Reproduce

```powershell
conda activate itsm_env
python Analysis\UVIR\UVIR-003\uvir003_causality_domain_under_conditional_matching.py
# expect: PASS_CAUSALITY_DOMAIN_UNDER_CONDITIONAL_MATCHING
```

## Next required calculation

1. Replace Conditional \((k_Q,C_{\mathrm{IR}})\) with matched invariants from a
   **named route** (prefer R2 once force domain accepted; R3 if UV data exist).
2. Re-evaluate \(q_\times(\theta)\) and the \(R_c\le 1\) domain after matching.
3. Physical cutoff / strong-coupling scale once normalization is fixed (M6).
