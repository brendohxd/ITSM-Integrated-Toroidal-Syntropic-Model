# RES-001 Stage 0 — $Q_{\mathrm{syn}}$ constitutive inventory

**Date:** 2026-08-04  
**Status:** `OPEN_SCAFFOLD_ONLY`  
**Subgate:** `PASS_RES001_QSYN_CONSTITUTIVE_INVENTORY_OPEN`  
**physics_pass:** **false**

## Reproduce

```powershell
python Analysis\RES\RES-001\res001_qsyn_constitutive_inventory.py
# expect: PASS_RES001_QSYN_CONSTITUTIVE_INVENTORY_OPEN
```

## Boundary

Inventory + conservation partition only. No Derived throughput law.
