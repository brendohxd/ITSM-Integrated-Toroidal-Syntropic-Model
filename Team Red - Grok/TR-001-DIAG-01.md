# TR-001-DIAG-01 — Provisional Diagnostic Evidence

**Classification:** Provisional diagnostic output only.  
**Not a completion of TR-001-v2.**  
**Canonical status:** None. No updates to manuscript, changelog, Notion, or any canonical claims are authorised from this run.

## Execution Metadata

- **Task ID:** TR-001-DIAG-01
- **Script executed:** `tr001_v2_diagnostic.py`
- **Execution command:** `python "Team Red - Grok\tr001_v2_diagnostic.py"`
- **Date/Time of execution:** 2026-07-14
- **Machine:** Windows 10/11 (user machine)
- **CPU cores used:** 16
- **Random seed:** 42
- **Re-optimization scope:** Only the worst 30 galaxies (by Δχ²) were re-optimised. No other galaxies were touched.
- **Path amendments:** All input/output paths were made relative to `__file__` for portability (original frozen package used hardcoded paths).

## Input & Output Hashes (at time of execution)

- Input CSV: `redteam_C23_vs_C1_comparison.csv`
- Output directory: `Team Red - Grok/Outputs/TR001_v2_Results/`

## Key Observations (Provisional)

- Mean Δχ² remained strongly negative (−36.81), consistent with prior runs.
- Median Δχ² was mild (−0.76), indicating the mean is driven by a small number of extreme outliers.
- 10% trimmed mean (−6.88) shows a moderate residual aggregate preference for C=1 even after outlier removal.
- **Boundary saturation observed:** Multiple re-optimisations of the worst galaxies hit the lower bounds on nuisance parameters (`u_d`, `d_scale`, `i_scale`). This behaviour requires systematic comparison between the C=2/3 and C=1 models before interpretation.
- Two galaxies (UGC02953 and UGC06787) produced extreme Δχ² values and dominate the mean.

## Interpretation Constraints

- The trimmed mean indicates a residual lean toward C=1 but **does not constitute a formal statistical significance test**.
- Boundary saturation is noted as an observation only. No conclusion is drawn about model validity.
- **No physical interpretation or canonical claim is authorised** from this diagnostic run.
- This output is preserved solely for traceability and independent review.

## Deliverables Included

- `summary_statistics.csv`
- `top_worst_galaxies.csv`
- `reoptimized_worst_galaxies.csv`
- Execution log (stdout)

**Status:** Evidence preserved. Awaiting Team Amber reproduction and Violet audit.
