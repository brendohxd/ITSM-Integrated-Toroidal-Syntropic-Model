# R4C1-S4A: full scalar graph metric and evolution-estimate diagnostic

Date: 2026-09-26. Frozen before executable and new numerical results.
Branch: recovery/v12-core-architecture. Owner: Master Test 1 / R4C1-v1/B1.
Claim status: Conditional. Review DEFERRED; physics_pass=false; gate_effect=NONE.

## Question and scope

S3 controls only the frozen zero-principal sector in a specified graph norm.
Extend that same norm to all six reduced scalar fields and their velocities.
Construct its exact evolving metric and energy derivative; measure the four
already registered full-system endpoint transfers in that metric. Determine
which ingredients of a complete coupled evolution estimate are available.
This step does not promise a uniform PDE estimate or nonlinear well-posedness.

The complete candidate action and variation already exist. Reopening the
canonical Test-1 action-input hold by adopting this candidate is a separate
scientific decision; no repeat variation or automatic adoption is intended.

## Fixed inputs and coordinates

Use the unchanged S1 constrained matrices/auxiliary solutions, S2 matrices
and two-method transfer artifact, and S3 report/contract. Verify their hashes
and transitive receipt dependencies before computing. Never call an upstream
main() or overwrite its receipts. Inherit R9-MT1-S3/S2/S1/B1/VARIATION.

On the regular expanding B1 chart, q=(du,dv,dr,dpsi,dtau,w), q=R(t,k)x and
Z=(x,xdot). Use the FULL twelve-dimensional map

    q=[R,0]Z,  qdot=[Rdot,R]Z,
    Zdot=A Z,  A=[[0,I],[-W,-G]],  W=Vc+Mcdot.

Differentiate at fixed comoving k, with the B1 background equations; only then
set p=k/a. Retain every principal/subprincipal term and all scalar directions.
No leading fast-mode embedding, zero-mode projection, pressure, damping,
action change, parameter fitting or deletion of the Jordan vector is allowed.

Reconstruct lapse, shift, delta epsilon and z by the S1 linear auxiliary map.
Verify the dust multiplier/normalization and z=-delta Delta identities.
Define D=(C^4 delta epsilon+4 beta rho_m delta psi)/rho_m and v_d=p dtau/C.

## Fixed norm and exact identities

Use the S3 reference-unit graph rows, now on the entire Z space:

    delta f, p delta f, delta fdot  (f=u,v,r);
    sqrt(K_Q) delta psidot; sqrt(b) delta Delta_psi;
    sqrt(M_U^2 c14) wdot; sqrt(M_U^2 cL) p w;
    D; v_d.

This is a declared diagnostic norm, not an invariant energy or Hamiltonian.
Dimensional quantities are expressed in the same fixed B1 reference units
as S3; no new physical units or normalization constants are derived. For a
Sobolev extension sum (1+|k|^2)^s times its squared mode norm over nonzero T3
modes, with the reference length understood. Higher derivatives and mixed
orders in the rows are part of the space, not a claim of equal-order control.

Export F with these 15 rows, S=F^T F, and L=Fdot+F A. Verify

    d/dt ||F Z||^2 = Z^T E Z,
    E=Fdot^T F+F^T Fdot+A^T S+S A= L^T F+F^T L.

Establish exact rank by an explicit 12-row minor if possible; report its
domain and every singular factor. An unresolved or vanishing minor does not
justify an inverse. H=0, k=0, rho_m=0 and all inherited S1 singular domains
remain excluded. Do not import S3's restricted minor as the full rank proof.

Where S is positive definite define the instantaneous norm-growth bound
mu=0.5*lambda_max(E,S). A complete uniform energy argument would require a
time-integrable, wave-number-independent upper bound on mu, or a separately
derived uniformly equivalent symmetrizer. Finite samples supply neither.
A growing mu alone does not prove actual solution growth or ill-posedness.

## Numerical and rejection checks

Use background events (0,0.5,1,2,3,4) and physical p=2*pi*2^j, j=0,...,8,
only for local metric/rate diagnostics. Use the pinned S2 endpoint transfers
at t=4 for k=2*pi*n, n=(1,2,4,8), retaining BOTH DOP853 and Radau outputs.
The induced amplification is ||F(4) T F(0)^+|| on the image of F(0), or the
equivalent square Cholesky-factor formula. No new trajectory is implied by
reweighting saved transfers. Report endpoint norms and method discrepancies.

Use at least 50-decimal arithmetic for Gram/Cholesky calculations; compare
induced norms against independent generalized-eigenvalue calculations to
relative 1e-8. Background/transfer inputs retain their original accuracy.
Use relative 1e-5 for comparison between the two inherited transfer methods.
Report metric rank and conditioning, and numerical failures without masking.

Reject missing Rdot, missing Fdot in the energy derivative, missing Mcdot
in the generator, and replacing the 12-component map with the two-component
S3 restriction. Verify the rate formula against a centered derivative along
the background and full generator at a regular event (h=1e-6, relative 1e-5).
Any failed verification keeps the result UNVALIDATED. Preserve failed attempts
before changing code or thresholds. No target coefficient or observations.

## Decision and next obligation

Distinguish exact reconstruction/rank, finite-mode transfer evidence,
instantaneous rate diagnostics and a uniform full evolution theorem. Only
the first three are this checkpoint's deliverables. Record whether the fixed
metric produces a useful estimate or needs a separately justified equivalent
symmetrizer. A new norm cannot be chosen after the run to manufacture a pass.

Full coupled uniform estimates, homogeneous/singular sectors, all-sector
stability, causality, EFT cutoff, healthy GR recovery and physical matching
remain open unless separately established. Rule9_cleared=false;
research_execution=PROCEED_PROVISIONALLY for this diagnostic only;
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED. No provider dispatch, model change, commit or publication.
