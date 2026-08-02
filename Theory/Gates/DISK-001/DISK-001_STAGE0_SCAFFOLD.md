# DISK-001 Stage 0 — Conditional IR scaffold

Date: 2026-08-03  
Branch: `recovery/v12-core-architecture`  
Status: **PASS** (`PASS_DISK001_STAGE0_SCAFFOLD`)  
Full DISK-001 gate: **IN PROGRESS** (not closed)

## What passed

| Subgate | Result |
|---------|--------|
| Plummer sphere deep-MOND / AQUAL | `PASS_DISK001_SPHERE_PLUMMER_AQUAL` |
| Exponential disk midplane boost | `PASS_DISK001_EXP_DISK_MIDPLANE_AQUAL` |
| 2D curl residual measured | `PASS_DISK001_CURL_RESIDUAL_MEASURED` |

IR policy: **Conditional** AQUAL-class with declared \(C_{\mathrm{obs}}\sim 1\) and phenomenological \(a_0\) (Master Plan §6). No Derived \(\Cobs\), no dual RAR packaging.

## Code

```text
Analysis/DISK/DISK-001/
```

```powershell
python Analysis\DISK\DISK-001\disk001_stage0_run_all.py
```

## Scientific boundary

- Not SPARC validation or STAT-001.  
- Not nonlinear AQUAL Poisson (potential structure).  
- Not full DISK-001 PASS (sphere+disk+curl+**convergence** still incomplete).  
- Algebraic map \(g=f(|g_N|)g_N\) curl is a **diagnostic**, not a claim of zero curl.

## Next toward full DISK-001

1. Nonlinear AQUAL / Poisson 2D (or 3D) solver  
2. Resolution and box-size convergence  
3. Optional single-galaxy diagnostic curves under declared inputs  
4. Then `DISK-001_GATE_REPORT.md`  
