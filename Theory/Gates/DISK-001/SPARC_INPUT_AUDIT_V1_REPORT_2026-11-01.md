# SPARC input readiness — 1 November 2026

## Result and scope

The local radial-table collection is structurally usable for further data work:
175 galaxies, 3,391 measurements, no malformed/nonfinite rows, nonpositive
radii/errors or non-increasing radii under the registered checks. This is not a
new fit, independent provenance certification, ITSM prediction or gate clearance.
DISK-001 remains methods-only; STAT-001 is not closed. Rule-9 review is deferred.

Contract: `SPARC_INPUT_AUDIT_V1_CONTRACT_2026-11-01.md`.
Executable: `Analysis/DISK/DISK-001/sparc_input_audit_v1.py`.
Fresh receipt: `Analysis/DISK/DISK-001/outputs/sparc_input_audit_v1_20261101/receipt.json`.
The receipt pins all local input files and the executable. Exact deterministic
read-only replay passed. An independent NumPy loadtxt/Pandas reader agreed on
175 standard files, 3,391 rows, 361 negative gas entries and 93 errors below 1 km/s.

## Findings

| Check | Observation | Consequence |
|---|---|---|
| Duplicate files | 328 DAT files: 175 standard tables plus 153 alternates | Count galaxies once; leave all original files intact |
| Alternate identity | All 153 pairs differ in bytes but agree in parsed numerical rows | Preserve both hashes; numerical agreement does not establish external provenance |
| Signed gas contribution | 361 selected rows have negative Vgas | Preserve sign; do not replace signed contributions with unsigned squares |
| Reported uncertainties | 93 selected rows have errV below 1 km/s | A 1 km/s floor changes the likelihood; it must not be applied silently |
| Catalogue joins | All three CSV tables join to all 175 radial-table names | Name coverage is complete under these local checks |
| Misleading CSV names | MassModels has only Name/Dist/i; Q_flags is byte-identical to it | Obtain quality from SPARC_Qual; radial components are in DAT tables |
| Sample accounting | Q in {1,2} and i >= 30 selects 153 from these local CSVs | Reconcile with the ledger's 152-galaxy repaired comparison before reusing that selection |

The last discrepancy is unresolved here. It could reflect an additional cut,
different metadata or input version; this audit does not choose an explanation
or modify the old result. The independent reader also confirmed Q_flags and
MassModels are byte-identical.

The CSV fields alone do not provide distance/inclination uncertainties, their
covariance or a complete nuisance model. The local README attributes this
collection to an information-projection companion dataset, so numerical
structure and local hashes must not be confused with verified upstream identity.

## Pipeline boundary and next work

The inspected `disk001_sparc_galaxy_pipeline.py` uses a fixed acceleration scale,
an algebraic acceleration interpolation, a 1 km/s error floor and clipping of
negative total baryonic squared speed. It labels its output physics_pass=true.
That label does not override the current methods-only owning status or turn this
algebraic comparator into a solved disk AQUAL equation or an ITSM prediction.
The old executable and receipts were preserved and were not rerun or rewritten.

Next, reconcile the 152/153 selection against the repaired comparator's exact
inputs and exclusions; verify authoritative catalogue provenance and uncertainty
fields; then identify the new paper's exact 147-galaxy membership, lensing data,
covariance and selection. Do not assume either local quality-cut sample equals
that paper's sample. Build the common nuisance/data interface before new fits.
An ITSM-specific comparison additionally needs independently justified force
and metric/lensing predictions. Conditional controls must be labelled as such.

No downloads, fitting, acceleration-target tuning, publication, vault mutation,
commit or push were performed by this audit. Original inputs, hashes, alternate
files and unrelated dirty work were preserved.

## Reproduction

Using the existing scientific Python environment:

```powershell
python -B Analysis/DISK/DISK-001/sparc_input_audit_v1.py --output <new-receipt-path>
python -B Analysis/DISK/DISK-001/sparc_input_audit_v1.py --verify Analysis/DISK/DISK-001/outputs/sparc_input_audit_v1_20261101/receipt.json
```

Output creation is exclusive: an existing receipt is never overwritten.
Verification is read-only and requires byte-identical reconstructed output.
