# RES-001 — Reservoir / $Q_{\mathrm{syn}}$ constitutive gate (scaffold)

**Document type:** Open gate specification  
**Gate ID:** RES-001  
**Status:** `OPEN_SCAFFOLD_ONLY`  
**Date:** 2026-08-04  
**Branch:** `recovery/v12-core-architecture`  
**Claim restoration:** **none**

## Question

Can reservoir–plenum throughput $Q_{\mathrm{syn}}^\nu$ be realized as an
energy-accounted constitutive or action-level sector such that:

1. total matter + plenum + reservoir conservation holds;
2. $Q_{\mathrm{mp}}$ (local matter–plenum) is not silently identified with $Q_{\mathrm{syn}}$;
3. no free generic creation rate, $H_0$, or $13/12$ packaging is smuggled;
4. optional later interface to WAK Route I/II does not double-count currents?

## First executable

```text
PASS_RES001_QSYN_CONSTITUTIVE_INVENTORY_OPEN
Analysis/RES/RES-001/res001_qsyn_constitutive_inventory.py
```

The common R1/R2/R3 evidence rubric now returns
`NO_ROUTE_SELECTABLE_ON_CURRENT_EVIDENCE`. R1 is retained only as the most
developed calculation scaffold; R0 remains the no-throughput control. See
`RES-001_STAGE1_CONSTITUTIVE_ROUTE_EVIDENCE_RUBRIC.md`.

## Non-claims

No Derived creation law, NEC-violating Minkowski support, cosmology, or
RES research-gate PASS.
