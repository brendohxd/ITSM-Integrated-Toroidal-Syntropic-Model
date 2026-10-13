# Covariant entropy accounting for interacting ITSM sectors

Current version: 0.7.1-conditional-draft  
Canonical source: ITSM_Covariant_Entropy_Accounting_v0.7.1-conditional-draft.tex  
Canonical PDF: Boyd_2026_Covariant_Entropy_Accounting_Interacting_Sectors_v0.7.1-conditional-draft.pdf  
Status: conditional manuscript; local author/external-review draft; not submitted

## v0.7.1 structural refinement

- leads with the model-independent entropy-accounting problem rather than
  repository-history corrections;
- retains the v0.6.0 withdrawals in a later provenance subsection;
- explains why conditional R4C1 is used as a bounded reversible-exchange stress
  test rather than as evidence of a completed cosmology; and
- separates necessary thermodynamic conditions, observational claim
  extensions, and independent-review governance.

No entropy-production, Hessian, acceleration, or observational claim was
promoted by this editorial revision.

The canonical v0.7.1 PDF compiles to five pages; all pages, PDF metadata, and
the matching SHA-256 sidecar were inspected locally on 1 October 2026.

## What changed from v0.6.0

The v0.6.0 source and PDF are preserved unchanged for provenance. Their
topology-implies-inflow, exact entropy-cancellation, heat-death-avoidance, and
acceleration claims are not retained.

The v0.7.0 manuscript instead:

- derives the sector entropy identity
  div S_A = (q_A - mu_A n_A Gamma_A)/T_A;
- proves that total stress conservation does not fix total entropy production;
- shows that compact T3 removes net boundary flux rather than supplying it;
- applies the accounting to the action-derived R4C1 exchange currents;
- separates reversible exchange, particle creation, entropy production,
  thermodynamic stability, field stability, and acceleration; and
- states the missing constitutive, Hessian, perturbative, and observational
  work required for a positive syntropic claim.

## Build

    conda activate itsm_env
    cd papers\Syntropic-Thermodynamics
    .\Build-Syntropic-Thermodynamics.ps1

The builder writes the versioned PDF directly and creates a matching SHA-256
sidecar. It does not alter or remove the historical v0.6.0 files.

The [8 October standalone review record](../ReleasePackages/2026-10-08/Thermodynamics-review/THERMODYNAMICS_STANDALONE_REVIEW_2026-10-08.md)
confirms the conditional methods-note scope and records the remaining review
and positive-claim dependencies.
