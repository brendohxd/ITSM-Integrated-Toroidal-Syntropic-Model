# ITSM UVIR-003 — local four-leg kernel slice (post alpha.9)

**Version:** 0.10.0-pre (working gate slice, not MAT-001 unlock)  
**Date:** 2026-08-02  
**Git:** `a57ed29` on `recovery/v12-core-architecture`  

## Included subgates

- `PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL` (alpha.9 freeze)
- `PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT` (+ optional dense_edge tag)
- `PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION` (packet proxy, **not** S-matrix)

## Claim boundary

Local frozen-time analytic kernel + deformation + packet-average proxy only.
**Not established:** cosmological S-matrix, unitarity bound, strong-coupling
scale, physical cutoff, MAT-001.

## Reproduce

```powershell
conda activate itsm_env
cd Analysis/UVIR/UVIR-003
python uvir003_local_four_leg_kernel.py
python uvir003_four_leg_kinematic_deformation.py
python uvir003_local_adiabatic_observable_norm.py
```

## Repository

https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model
