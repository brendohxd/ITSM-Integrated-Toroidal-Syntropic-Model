# UVIR-003 Stage B — Declared weakly-coupled domain (Stage 1 / M2)

Date: 2026-08-03

Branch: `recovery/v12-core-architecture`

Serial stage: **1** (see `UVIR-003_SERIAL_STAGE_ORDER.md`)

Calculation status: **PASS_BOUNDED** (evidence-bounded declaration; IR physics not solved)

Subgate:
`PASS_DECLARED_WEAK_COUPLING_DOMAIN`

Master Plan **M2**: **PASS_BOUNDED**  
(diagnostic control claimed only on the explicit analytic and sampled support below)

Full UVIR-003 gate: **IN PROGRESS**

MAT-001 gate PASS and downstream Derived use: **BLOCKED**

## Purpose

Complete Stage 1 of the serial order by stating the **evidence-bounded claim
domain** in which UVIR-003 has diagnostic stability / perturbative-control
support. IR HOLD modes and incomplete sectors remain outside that claim set
until a named future gate supplies new evidence.

This is **not** a fix of the complex-quartet IR transfer problem. It is the
peer-review-correct move: **do not smuggle HOLD modes as PASS**.

## In domain (include)

| Sector | Explicit admitted support | Evidence |
|--------|---------------------------|----------|
| Track-A nonzero-gradient force | Analytic \(A_{\rm IR}>0,\ v>0\); sampled \(A_{\rm IR}=1\), \(v\in\{0.05,0.1,0.25,0.5,1,2\}\) | `PASS_NONZERO_GRADIENT_FORCE_LOCAL` |
| High-\(q\) mode-projected Green proxy | Discrete \(q/H\in\{47.5,50,75,100\}\); representative two-time proxy \(t\in[0,8]\) | `PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN` |
| Local adiabatic packet norm | \(q_0/H=50\), narrow \(\sigma_{\ln q}=0.02\), same discrete support | `PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION` |
| Declared tree/NDA diagnostic | \(q/\Lambda_\parallel\le0.3\), \(u_L\le1\), evaluated at diagnostic \(A_{\rm IR}=K_Q=1\) | `PASS_DECLARED_UNITARITY_EFT_CRITERION` |
| Invariants + route maps | Algebraic interface only; numeric \(K_Q\) and physical cutoff unmatched | inventory + matching-route program |

These are analytic conditions plus discrete tested support, not a validated
continuous neighbourhood. The present audit also does not prove that evolution
cannot mix admitted data into excluded IR modes.

## Out of domain (exclude until named future gate)

| Sector | Why |
|--------|-----|
| IR transfer HOLD / complex-quartet modes | Structural HOLD on disk |
| Homogeneous zero-gradient \(Y^{3/2}\) S-matrix | Not Track-A programme |
| Full in-in nested integrals | Path only; not computed |
| Optical theorem / multi-channel unitarity | NOT_COMPUTED; out of UVIR Stage-1 scope |
| Derived \(K_Q\) / matched physical cutoff | Stages 2–4 |
| MAT-001 Derived vertex | Stage 3 |

## Explicit non-claims
- No continuous high-\(q\) interval is certified between sampled points.
- No dynamical no-leakage/closure theorem for the admitted sector is established.
- \(\Lambda_\parallel\) is a diagnostic NDA scale until matching fixes the normalization.

- IR modes are **not** declared healthy.  
- M3/M6 are **not** Derived-closed.  
- MAT is **not** unlocked.  
- UVIR-003 full gate is **not** PASS.

## Reproduce

```powershell
conda activate itsm_env
python Analysis\UVIR\UVIR-003\uvir003_declared_weak_coupling_domain.py
# expect: PASS_DECLARED_WEAK_COUPLING_DOMAIN
```

## Next (serial Stage 2 only)

1. Stage 2a — **DONE:** `INCOMPLETE_R3_UV_RESIDUE`
2. Stage 2b — **NEXT:** write the Conditional matching floor and scope
3. Stage 2c — re-evaluate causality/NDA under that floor
4. **Then** Stage 3 scoped MAT calculation, subject to the written handoff

Do **not** start MAT Derived work before Stage 2 exit is recorded.
