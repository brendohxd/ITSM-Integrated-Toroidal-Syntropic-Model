# Full SPARC nuisance-input check — 1 November 2026

The operator selected retrieval of measured uncertainties followed by a full
nuisance-marginalized analysis. The requested population is all 175 galaxies,
not an unexplained 152-galaxy selection. No real-data chains have yet run.

## Retrieval and provenance boundary

Astroquery/VizieR retrieval via the Strasbourg alias also failed with a connection
reset. After the earlier CDS/Harvard failures, the candidate archive record
https://zenodo.org/records/16284118 was inspected and its JSON API used to resolve
the catalogue's file link and checksum rather than trusting a raw guessed URL.
The archived catalogue and record response are retained in
`Data/SPARC_catalogue_archive_candidate_v1_20261101/`.

Catalogue: `SPARC_Lelli2016c.mrt`, 28,259 bytes.
SHA-256: `5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243`.
MD5: `6181df386bfc05868a3700c196e800da`, matching the record's published checksum.
The record identifies the SPARC authors and original project/paper. That
metadata and a checksum do not independently establish uploader authority or
byte identity with a fresh CDS response. Preserve the candidate provenance label.

The CDS primary column documentation was also checked:
https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/AJ/152/157?format=html&tex=true
It specifies distance errors in Mpc, inclination errors in degrees and quality
flags 1–3. It states that rotation-velocity errors exclude inclination systematic
uncertainty. Distance-method flag 1 uses a Hubble-flow calibration assuming
H0=73 km/s/Mpc; therefore these inputs are not calibration-free H0 measurements.

## Validation and parser defect

All 175 names are unique and join one-to-one to the existing local distance,
inclination and quality tables with no nominal-value differences. All distance
and inclination errors are positive. The recovered CamB row agrees with the
previous local VizieR cache, including 0.26 Mpc and 5 degrees errors.

Astropy's CDS reader rejected this file because the embedded byte description
does not match its data rows. No source repair was made. Two extraction methods
(whitespace tokens and explicitly checked actual fixed-width slices) agree on
all 175 nuisance rows. Actual zero-based slices: Name [0:11], D [15:21], e_D
[22:27], distance method [29:30], i [31:35], e_i [36:40], quality [113:116].
Whitespace token indices are 0,2,3,4,5,6,17 respectively. Data begin at line 99.
Results are saved in `nuisance_inputs.csv` and `validation.json`.

Q in {1,2} and nominal i>=30 degrees still selects 153. This does not establish
what other exclusion/version produced the old ledger's 152; that history remains
unresolved. Do not rewrite the old result or silently remove one galaxy.

## Next execution boundary

High acknowledgement is requested for implementing and reviewing the real-data
likelihood, physical support, measured-error priors and inclination/distance
transformations, including galaxies at edge-on boundaries and negative signed
gas contributions. Run a real-data pilot and review diagnostics before batching
all 175 on 16 processes. Preserve separate quality/low-inclination sensitivity
reporting; no full-sample exclusion may be selected by fit outcomes.

The synthetic fixture-1 convergence miss remains unchanged. The synthetic-only
v1 executable cannot simply be invoked on real data. Its cumulative checkpoints
occupied about 1.15 GiB for 16 jobs; the full-run implementation must use bounded
incremental checkpoint storage and check available space before launching.

This is still a conditional algebraic comparator, not an action-derived ITSM
prediction or full disk/lensing solution. Catalogue retrieval does not establish
model preference, close STAT/DISK/MAT or remove substantive parent holds.
No original data, receipts or sidecars were altered; no commit, push, publication
or vault mutation was performed. Rule-9 review remains deferred.
