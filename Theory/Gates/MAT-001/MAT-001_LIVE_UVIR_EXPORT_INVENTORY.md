# MAT-001 live UVIR quadratic-export inventory

**Status:** `PASS_MAT001_LIVE_UVIR_EXPORT_INVENTORY_BLOCKED`
**Live bundle:** `PARTIAL_NOT_SAME_CHART`
**MAT-001:** **BLOCKED**
**V:** **NOT_COMPUTED**
**UVIR-003:** **IN_PROGRESS**
**Stage 4A:** **CLOSED**
**Physics pass:** `false`

## Purpose

MAT J2 established the basis-covariant source projection

\[
g_{\rm can}=\frac{c_{\rm eff}^{T}u}{\sqrt{u^{T}Ku}},
\qquad
c_{\rm eff}=d-BC^{-1}h,
\]

but did not consume live action matrices. This checkpoint inventories the
current UVIR-003 exports for the required objects (K,C,B,d,h,u). It records
partial evidence, chart mismatches and missing objects explicitly. It does not
fill gaps with template data or diagnostic response probes.

## Inventory result

| Object | Live status | Evidence and boundary |
|---|---|---|
| (K) | `PARTIAL_EXPORTED_PHYSICAL_CHART` | Exact symbolic physical kinetic matrix in ((\Xi,Q_\rho,Q_\chi)); dimensions are not explicit in the export |
| (C) | `PARTIAL_EXPORTED_ORIGINAL_CHART` | Exact finite-(q) constraint matrix in the original ((R,\delta\rho,\vartheta;\delta N,\Sigma)) chart |
| (B) | `PARTIAL_EMBEDDED_IN_CONSTRAINT_SOURCE` | The finite-(q) (J_1) source is exported, including velocity-dependent terms, but it is not isolated as the J2 template block |
| (d) | `NOT_EXPORTED` | No direct action-level matter-source covector on the dynamical fields |
| (h) | `NOT_EXPORTED` | No action-level matter-source covector on the algebraic constraints |
| (u) | `NOT_SELECTED_IN_SAME_CHART` | A physical-basis map exists, but a map is not a selected physical eigenmode direction |

The gauge-projected (Q_\rho,Q_\chi) impulses in the retarded-response audit
are diagnostic probes. They are not derived from the required matter
interaction and cannot be relabelled as (d,h).

## Decision

The live same-action bundle is **not ready** for the J2 numerical projection.
The inventory itself passes because it verifies the current evidence contracts
and fails closed on every missing or mismatched role. No numerical (V),
(K_Q), MAT pass, UVIR pass or downstream Derived claim follows.

## Blocking requirements

1. derive (d,h) from one declared matter interaction in the live quadratic
   action;
2. express (K,C,B,d,h) in one named chart and normalization convention;
3. report the dimensions of every object in that chart;
4. select the physical mode (u) in the same chart;
5. rerun J2 and only then evaluate a canonical source coupling.

## Reproduction

```text
python Analysis/MAT/MAT-001/LIVE_EXPORT_INVENTORY/mat001_live_uvir_export_inventory.py
```

Expected terminal status:

```text
STATUS: PASS_MAT001_LIVE_UVIR_EXPORT_INVENTORY_BLOCKED
```

Machine-readable evidence:

- `Analysis/MAT/MAT-001/LIVE_EXPORT_INVENTORY/outputs/mat001_live_uvir_export_inventory_summary.json`
- `Analysis/MAT/MAT-001/LIVE_EXPORT_INVENTORY/outputs/mat001_live_uvir_export_inventory_summary.sha256`

## Scientific boundary

A pass means the live exports have been inventoried against the J2 interface
and the exact blocker map is now executable. It is not a matter-coupling
calculation and does not promote partial symbolic matrices into a complete
same-chart action export.
