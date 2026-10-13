# R4C1 covariant finite-density exchange model

Current version: 0.1.1-conditional-draft  
Canonical PDF: Boyd_2026_Covariant_Finite-Density_Exchange_Model_v0.1.1-conditional-draft.pdf  
Status: conditional theory manuscript; not canonically promoted; not submitted

## Main contribution

The declared R4C1 action produces explicit, nonsingular matter--plenum and
plenum--reservoir exchange currents whose sector balances sum to total
conservation. Its formal physical dust-density coordinate has
K_D = a^5 rho_m/k^2 > 0 in the uncoupled limit, exactly matching an independent
coupled-fluid EFT normalization.

This revision makes the three claim levels explicit: action-level source-vector
closure, dynamical stability, and phenomenological success.  It improves the
paper's ordering and states the reversible-reservoir assumption without
importing an unprovided entropy or particle-production mechanism.

## Required limitations

- the density Hamiltonian has an indefinite growing-mass direction;
- the equal-Newton family retains a defective double zero-speed scalar root;
- homogeneous matching does not identify the nonlinear force coefficient;
- compact T3 requires a zero-mean static contrast source;
- a universal pointwise square-root shortcut fails a curl test;
- finite regulator b makes the arbitrarily weak fixed-scale response linear;
- no a0, 2/3 coefficient, observational fit, positive entropy-production claim,
  particle-production source, or all-sector quantum closure is derived.

## Build

    conda activate itsm_env
    cd papers\R4C1-Covariant-Exchange-Model
    .\Build-R4C1-Covariant-Exchange-Model.ps1

The builder creates a versioned PDF and SHA-256 sidecar. It does not modify the
gate reports or their frozen receipts.

## Conditional review package — 8 October 2026

The existing v0.1.1 conditional draft has a bounded local review package:

- [review report](../ReleasePackages/2026-10-08/R4C1-review/R4C1_CONDITIONAL_REVIEW_REPORT_2026-10-08.md)
- [machine-readable manifest](../ReleasePackages/2026-10-08/R4C1-review/R4C1_CONDITIONAL_REVIEW_MANIFEST.json)
- [source archive](../ReleasePackages/2026-10-08/R4C1-review/ITSM_R4C1_source_v0.1.1-conditional-draft_2026-10-08.zip)

This package is conditionally reviewable but not publication-ready: Rule-9
review remains deferred, `physics_pass=false`, `K_Q=NOT_DERIVED`,
`V=NOT_COMPUTED`, and the substantive stability, cutoff, all-sector, and
action-to-observable holds remain active. The manuscript source (`main.tex`) and
canonical PDF were not changed; only these documentation pointers were added.
