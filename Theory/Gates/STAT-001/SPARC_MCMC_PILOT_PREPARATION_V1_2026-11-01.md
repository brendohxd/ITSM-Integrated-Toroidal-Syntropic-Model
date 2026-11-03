# Fresh SPARC MCMC pilot preparation — 1 November 2026

Status: PREPARATION_ONLY. No chains have been started. This document is a
proposed execution setup, not an approved statistical contract or gate pass.

## Operator-requested computing setup

- 64 walkers per ensemble; four independently seeded ensembles per galaxy.
- Initial allocation: 10,000 steps per walker. The first 2,000 are provisionally
  designated warm-up, subject to diagnostics; no fixed step count proves mixing.
- 16 Windows-spawn worker processes, distributing galaxy/ensemble jobs.
  Numerical-library thread counts are set to one before importing NumPy/SciPy.
  No nested process pools. Actual CPU occupancy depends on available jobs and I/O.
- A four-galaxy pilot can provide 16 independent ensemble jobs. Galaxy selection
  must be fixed from input properties before examining the new fit outcomes.
- Preserve chains, independently generated seeds, acceptance statistics,
  dependency versions, model/input hashes and restart state in a fresh directory.
- Convergence requires autocorrelation/ESS diagnostics and agreement between
  independent ensembles. Ensemble walkers are not treated as independent chains.
  Exact thresholds and extension limits remain to be reviewed before sampling.

## Required before statistical implementation

1. Explicit High acknowledgement under the operator's reasoning-switch policy.
2. Retrieve measured distance and inclination uncertainties and validate units,
   identifiers, completeness and provenance against the 175 local radial tables.
3. Reconcile the 153-galaxy direct Q={1,2}, i>=30 selection against the ledger's
   152-galaxy repaired comparator, retaining all exclusions and historical outputs.
4. Freeze the precise conditional force law, units, parameterization, nuisance
   transformations, prior densities/Jacobians, likelihood normalization and scope.
5. Validate against independent numerical likelihood controls and synthetic
   parameter recovery before real-data inference. Include prior sensitivity.

The existing local CSVs contain nominal distance/inclination and quality values,
but not their uncertainties. The base Anaconda environment has Astroquery,
Astropy and emcee; the itsm_env environment has emcee but lacks the former two.
No installation or runtime reconfiguration is needed merely to retrieve inputs.

Retrieval attempts this session did not obtain the catalogue. The installed
Astroquery rejected an initial unsupported `cache` keyword; after correcting
that call, the sandbox reported DNS resolution failure. Authorized network
execution reached a connection reset at the CDS endpoint; the official Harvard
mirror timed out, and a read-only GET attempt at CDS also reset. No catalogue
or provenance file was created. These errors establish failed retrieval, not
the cause of the network failures. No firewall, proxy or TLS setting was changed.

Do not reuse the old hierarchical 10% down-weighting of boundary-hitting galaxies
as a dust correction. Do not add a silent velocity-error floor, point-dependent
distance/inclination draws, target-selected exclusions or a cosmic-H0 claim.
Inclination nuisance treatment is not a demonstrated removal of inclination
dependence; stellar/dust uncertainty needs its own justified model.

## Interpretation boundary

Any initial algebraic force-law run is a conditional comparator, not a full disk
field solution or an action-derived ITSM prediction. No global model preference,
closed STAT/DISK gate or physical matching follows merely from sampler convergence.
Rule-9 review remains deferred; substantive missing inputs remain real blockers.
No commit, push, publication, model dispatch or vault mutation is included.
