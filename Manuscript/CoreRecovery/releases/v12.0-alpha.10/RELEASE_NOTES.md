# ITSM Core v12.0-alpha.10

Date: 03 August 2026  
Label: Post–alpha.9 UVIR-003 path package

## Scientific advance

This release freezes the **post–alpha.9 UVIR-003 working path** in the core
manuscript narrative. It does **not** close the full UVIR-003 gate and does
**not** unlock MAT-001.

Relative to `12.0-alpha.9` (local tetrahedral four-leg kernel only), the
working tree recorded and the manuscript now cites:

| Subgate | Role |
|---------|------|
| `PASS_FRW_IN_IN_OBSERVABLE_PATH_DECLARED` | FRW attach for packet proxy + high-$q$ transfer skeleton |
| `PASS_FRW_MULTI_SLICE_MODE_PROJECTED_GREEN` | Multi-slice $K_{\mathrm{nn}}(t)$ + causal $G_{\mathrm{mp}}$ |
| `PASS_NONZERO_GRADIENT_FORCE_LOCAL` | Track-A $\|\nabla\pi\|^3$ about $v>0$; positive Hessian |
| `PASS_DECLARED_UNITARITY_EFT_CRITERION` | Scoped tree/NDA + Green health criterion |
| `PASS_KQ_MATCHING_INVENTORY_OPEN` | Invariants $Aq/K_Q$, $A/K_Q^{3/2}$; routes R1–R5 |

Also recorded in the programme layer (not all prose in the PDF):

- P3 outline-only skeleton (`papers/P3-Observational-Program/`)
- MAT-001 / DISK-001 / STAT-001 readiness checklists
- P3/P4 readiness map

## Scientific boundary

Still **not** established:

- cosmological S-matrix / optical theorem;
- matched physical strong-coupling cutoff;
- numeric Derived $K_Q$;
- MAT-001 matter–force vertex;
- full UVIR-003 PASS.

UVIR-003 remains **IN PROGRESS**. MAT-001 remains **BLOCKED**.

## Reproduction (selected)

```powershell
python Analysis\UVIR\UVIR-003\uvir003_local_four_leg_kernel.py
python Analysis\UVIR\UVIR-003\uvir003_frw_multi_slice_mode_green.py
python Analysis\UVIR\UVIR-003\uvir003_nonzero_gradient_force_local.py
python Analysis\UVIR\UVIR-003\uvir003_declared_unitarity_eft_criterion.py
python Analysis\UVIR\UVIR-003\uvir003_kq_matching_inventory.py
```

## Immutable path

```text
Manuscript/CoreRecovery/releases/v12.0-alpha.10/
```
