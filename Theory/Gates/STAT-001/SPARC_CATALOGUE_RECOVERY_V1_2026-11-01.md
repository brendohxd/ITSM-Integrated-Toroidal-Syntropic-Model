# SPARC nuisance-input recovery — 1 November 2026

Routine preparation at Medium; no new real-data MCMC was launched.

Fresh official catalogue retrieval remains unsuccessful. A bounded inspection
of the local Astroquery/VizieR cache found four cached responses: three reduced
catalogue queries and one full-column response for **CamB only**. The latter
contains measured uncertainty fields absent from the local CSV exports:

| Galaxy | D (Mpc) | e_D (Mpc) | i (degrees) | e_i (degrees) | Quality |
|---|---|---|---|---|---|
| CamB | 3.36 | 0.26 | 65 | 5 | 2 |

These are a historical cached source record, not a fresh upstream verification.
The extraction used pickletools opcode inspection to recover the embedded
VOTable XML without executing/unpickling the cache. The original cache was not
modified. XML, ECSV, selected nuisance CSV and provenance hashes are preserved in
`Data/SPARC_uncertainties_cached_v1_20261101/`.

This recovers one object's uncertainty fields, not the full 175-object input
contract: 174 galaxies still lack these fields in the inspected material.
Reported error bars also do not establish a Gaussian prior or an independent
distance/inclination covariance; those modelling choices need review.
Do not propagate CamB's errors to other galaxies.

The local Q={1,2}, i>=30 cut still yields 153. The ledger's 152-galaxy comparator
has not been reconciled with its exact source/exclusions; no sample was silently
adjusted and no previous number was replaced. Full real-data batching remains
on hold for this substantive input work, separately from deferred Rule-9 review.

Synthetic chains, failed convergence criterion and original sidecars were left
unchanged. No commit, push, publication or vault mutation was performed.
