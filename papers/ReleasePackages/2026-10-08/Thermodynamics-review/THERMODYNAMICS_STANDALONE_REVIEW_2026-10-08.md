# Thermodynamics standalone review — 8 October 2026

## Disposition

`STANDALONE_METHODS_NOTE_CONDITIONALLY_REVIEWED`.

The v0.7.1 manuscript is coherent as a bounded thermodynamic-accounting and
claim-hygiene paper. It is not a completed syntropic-cosmology result, and
this local review is not independent peer review. `publication_ready=false`,
Rule-9 review remains deferred, and the underlying R4C1 physics status remains
`physics_pass=false`.

## Review boundary and evidence

- Read the complete 537-line source
  `ITSM_Covariant_Entropy_Accounting_v0.7.1-conditional-draft.tex`.
- Reviewed the existing five-page PDF and rendered all five pages; no clipping,
  overlap, missing equation, or unreadable figure was found.
- Source SHA-256:
  `d7d0514c87744ad6f8c1efbdb788f385b3672da060349b42e5476664225f9dd3`.
- Current PDF SHA-256:
  `aa10d73273b37c574555ed0c877a9d06a8be38bb8fa9a89b61387f8de7871364`.

## Findings

1. **Entropy identity — locally consistent.** Starting from the declared
   sector balance, particle-current balance, local-equilibrium Gibbs relation,
   and Euler relation, the manuscript obtains
   `div S_A=(q_A-mu_A n_A Gamma_A)/T_A`. The transfer-sign convention is
   stated and the two-sector Onsager example correctly makes positivity a
   constitutive result rather than a consequence of total conservation.

2. **Compact-topology statement — correctly bounded.** The periodic divergence
   integral vanishes on smooth boundaryless flat `T^3`; the manuscript does not
   turn that into external inflow, zero entropy production, or a topology-only
   source. It separately flags zero modes and global state data.

3. **R4C1 bridge — provenance-consistent.** The displayed
   `Q_mp^nu=beta T_m nabla^nu psi` and
   `Q_syn^nu=-(g_r/2)s r nabla^nu r` match the frozen first-variation report.
   The homogeneous balance equations and sign of the reservoir transfer match
   the interacting-background report, including its finest sector-balance
   residual `7.963880541709535e-8`.

4. **Claim firewall — effective.** The paper explicitly withholds positive
   entropy production, heat-death avoidance, a thermodynamic Hessian result,
   particle creation, acceleration, and observational viability. It separates
   the thermodynamic Hessian from the quadratic field-stability matrices.

## Required before public submission

- Author cold proofread and metadata/declaration confirmation.
- Independent thermodynamics review; this local review cannot substitute for it.
- Decide whether the standalone methods note remains separate from R4C1.
- Supply temperatures, chemical potentials, particle rates, constitutive
  transport, constrained entropy-Hessian eigenvalues, and a solved background
  before making any positive syntropic claim.
- Preserve the R4C1 parent holds: missing full all-sector conservation
  verification, `K_Q` matching, `V` computation, stability/constraint closure,
  and observational derivation remain outside this paper's scope.

No manuscript equation, PDF, source hash, or parent gate was changed by this
review. No commit, push, provider dispatch, publication, or Rule-9 clearance
occurred.
