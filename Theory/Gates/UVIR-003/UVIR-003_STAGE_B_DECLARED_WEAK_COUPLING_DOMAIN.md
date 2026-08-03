# UVIR-003 Stage B — Declared weakly-coupled domain (Stage 1 / M2)

Date: 2026-08-03

Branch: `recovery/v12-core-architecture`

Serial stage: **1** (see `UVIR-003_SERIAL_STAGE_ORDER.md`)

Calculation status: **PASS** (domain frozen; IR physics not solved)

Subgate:
`PASS_DECLARED_WEAK_COUPLING_DOMAIN`

Master Plan **M2**: **PASS_BOUNDED**  
(weak coupling claimed only inside the declared include list)

Full UVIR-003 gate: **IN PROGRESS**

MAT-001: **BLOCKED** (serial: Stage 3)

## Purpose

Complete Stage 1 of the serial order: state the **weakly-coupled domain** in
which UVIR-003 may claim stability / perturbative control, and permanently
exclude IR HOLD modes and other incomplete sectors from that claim set.

This is **not** a fix of the complex-quartet IR transfer problem. It is the
peer-review-correct move: **do not smuggle HOLD modes as PASS**.

## In domain (include)

| Sector | Evidence |
|--------|----------|
| Track-A nonzero-gradient force | `PASS_NONZERO_GRADIENT_FORCE_LOCAL` |
| High-\(q\) mode-projected Green proxy | `PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN` |
| Local adiabatic packet norm | `PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION` |
| Declared tree/NDA unitarity criterion | `PASS_DECLARED_UNITARITY_EFT_CRITERION` |
| Invariants + matching route maps | inventory + matching-route program |

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

1. Stage 2a — dig-harder R3 (\(Z_\psi,r_\rho\))  
2. Stage 2b — Conditional matching floor if 2a incomplete  
3. Stage 2c — re-evaluate causality/NDA under floor  
4. **Then** Stage 3 MAT-001  

Do **not** start MAT Derived work before Stage 2 exit is recorded.
