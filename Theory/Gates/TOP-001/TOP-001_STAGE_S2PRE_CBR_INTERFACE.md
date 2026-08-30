# TOP-001 S2-pre — CBR-001 interface template

**Date:** 2026-08-04  
**Status:** `OPEN_SCAFFOLD_ONLY`  
**Subgate:** `PASS_TOP001_S2PRE_CBR_INTERFACE_TEMPLATE`  
**physics_pass:** **false**

## Result

Declares the TOP→CBR-001 geometry handoff `(L1,L2,L3)` / fixed-volume log-shape
chart and free-scalar mode-lattice diagnostics. Does **not** recompute Casimir
stress (CBR-001 owns that) and does not write $S_{\mathrm{mod}}$.

## Reproduce

```powershell
python Analysis\TOP\TOP-001\top001_s2pre_cbr_interface_audit.py
# expect: PASS_TOP001_S2PRE_CBR_INTERFACE_TEMPLATE
```

## Non-claims

No $13/12$, $H_0$, $a_0$, $C_{\mathrm{obs}}$, twisted preference, or TOP gate PASS.
