# MAT-001 same-chart free-sector quadratic export

**Status:** `PASS_MAT001_SAME_CHART_FREE_QUADRATIC_EXPORT_PARTIAL`  
**Live bundle:** `PARTIAL_FREE_SECTOR_SAME_CHART_MATTER_SOURCES_ABSENT`  
**MAT-001:** **BLOCKED**  
**V:** **NOT_COMPUTED**  
**UVIR-003:** **IN_PROGRESS**  
**Stage 4A:** **CLOSED**  
**Physics pass:** `false`

## Purpose

The live-export inventory showed that \(K\) was only published in the physical
scalar chart while \(C\) and the constraint source lived in the original chart,
and that the pure static J2 block \(B\) was not isolated. This checkpoint
exports free-sector objects without inventing matter couplings:

1. \(K\) and \(C\) in the original \((R,\delta\rho,\vartheta;\delta N,\Sigma)\) chart;
2. exact linear decomposition of the constraint source into field map \(M_x\) and
   velocity map \(M_v\);
3. a static J2 \(B\) candidate \(B=M_x^{T}\) together with an explicit nonzero
   \(M_v\) residual;
4. free kinetic metric transformed into the physical \((\Xi,Q_\rho,Q_\chi)\) chart.

## Result

| Object | Status after this checkpoint |
|---|---|
| \(K\) (original) | Exported from the finite-\(q\) reduced kinetic Hessian |
| \(K\) (physical) | Exported via the static basis transform \(y=Tp\) |
| \(C\) | Exported; constraint basis unchanged under dynamical redefinition |
| \(B\) static candidate | Isolated as \(M_x^{T}\); not pure-static-J2 ready |
| \(M_v\) residual | Nonzero and retained (not erased) |
| \(d,h\) | Still `NOT_EXPORTED` (no declared external-matter \(S_{\rm int}\)) |
| \(u\) | Still `NOT_SELECTED` (matter channel \(c_{\rm eff}\) absent) |

## Decision

This is a free-sector export advance, not a MAT unlock. Numerical matching,
\(V\), \(K_Q\), Stage 4A reopen and physics claims remain forbidden. The pure
static J2 template is still incomplete because \(M_v\neq 0\), and the matter
vertex channel is still missing.

## Blocking requirements retained

1. declare one external-matter interaction and derive action-level \(d,h\);
2. resolve the velocity residual relative to the J2 static convention, or extend
   the projection identity;
3. select \(u\) only after \(c_{\rm eff}\) is defined;
4. fix one absolute unit/normalization system before numerical matching.

## Reproduction

```text
python -B Analysis/MAT/MAT-001/SAME_CHART_EXPORT/mat001_same_chart_quadratic_export.py
```

Expected terminal status:

```text
STATUS: PASS_MAT001_SAME_CHART_FREE_QUADRATIC_EXPORT_PARTIAL
```

Machine-readable evidence:

- `Analysis/MAT/MAT-001/SAME_CHART_EXPORT/outputs/mat001_same_chart_quadratic_export_summary.json`
- `Analysis/MAT/MAT-001/SAME_CHART_EXPORT/outputs/mat001_same_chart_quadratic_export_summary.sha256`

Two consecutive runs produced byte-identical JSON. Internal mutation checks
reject promotion of complete-bundle, numeric-matching, \(V\), MAT-pass and
physics-pass flags without writing outputs.

```text
SHA-256: 6DE89DB28C85FAA42A67E5221FB039F488F1D85E83F863693A5FEB37E648F807
```

## Scientific boundary

A pass means free-sector \(K\), \(C\) and the exact source decomposition are now
exported in one declared original chart, with a transformed free kinetic metric
in the physical chart. It is not a matter-coupling calculation and does not
complete the live same-action \(K,C,B,d,h,u\) bundle required for J2 matching.
