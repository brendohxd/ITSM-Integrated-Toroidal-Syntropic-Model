# RES-001 — Reservoir / \(Q_{\mathrm{syn}}\) constitutive gate (scaffold)

**Document type:** Open gate specification  
**Gate ID:** RES-001  
**Status:** `OPEN_SCAFFOLD_ONLY`  
**Date:** 2026-08-04  
**Branch:** `recovery/v12-core-architecture`  
**Claim restoration:** **none**

## Question

Can reservoir–plenum throughput \(Q_{\mathrm{syn}}^\nu\) be realized as an
energy-accounted constitutive or action-level sector such that:

1. total matter + plenum + reservoir conservation holds;
2. \(Q_{\mathrm{mp}}\) (local matter–plenum) is not silently identified with \(Q_{\mathrm{syn}}\);
3. no free generic creation rate, \(H_0\), or \(13/12\) packaging is smuggled;
4. optional later interface to WAK Route I/II does not double-count currents?

## First executable

```text
PASS_RES001_QSYN_CONSTITUTIVE_INVENTORY_OPEN
Analysis/RES/RES-001/res001_qsyn_constitutive_inventory.py
```

## Non-claims

No Derived creation law, NEC-violating Minkowski support, cosmology, or
RES research-gate PASS.
