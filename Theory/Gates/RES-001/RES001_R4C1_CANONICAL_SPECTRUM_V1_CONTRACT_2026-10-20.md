# Canonical constrained-spectrum contract: full matrices before physical claims

20 October 2026. Continue the unchanged R4C1 coupled operator route. No state
adoption/evolution, new action or physical validity window is assumed.

## Complete retained calculation

Materialize the FULL retained finite-grid Hessian/descriptor and constrained
canonical generator, not an isolated sector or a few selected eigenvalues.
Keep all fields, fixed charges/local fluctuations, mean metric pairs, nonlinear
constraint pullback, Ricci, potential, cusp, two-form crosses and background
drift. Do not discard negative, zero, growing or ill-conditioned directions.

Start with n=17 for ALL nine inherited family/eta cases and both node
orientations. This gives eighteen complete matrices. The executor must also
support n=25 and33 for subsequent registered-grid refinement with fresh output.
Coarsest-grid results do not close the spectrum/domain objective; n25/n33,
simultaneous continuum traces and arbitrary-direction completion remain required.

Use a cached exact-second-differential evaluator rather than repeating hundreds
of expensive nonlinear gradient solves. For the stationary augmented functional
F(X,y), its temporal block is F_yy=-volume*R/(n*s). Thus

    H''v=F_XX*v+F_Xy*dy,
    dy=(n*s)*(volume*R)^(-1)*F_yX*v.

The factor n*s is mandatory. Verify the cached actions against the existing
100-digit full coupled operator and independent finite differences. Use
80-decimal arithmetic for matrix construction, retaining actual matrix symmetry
errors; do not symmetrize a failed matrix into passing.

The original cusp is C2, not generally C3. At a registered zero of Y, the
composite Y^(3/2)=O(norm(delta V)^3) has zero second derivative because Y is a
nonnegative quadratic frame norm to leading order and dY=0 there. A cached
implementation may use this C2 limit ONLY after checking dY=0. It must reject
the nonstationary primitive x^(3/2) at x=0. No third cusp tensor is created.

## Constraint-compatible canonical coordinates

Use only the existing global phase/dust/translation quotients. Build complete
orthonormal bases for their prescribed tangent sections; retain all other
zero/harmonic modes and the three mean metric pairs.

At the exact node solve the same full two-row auxiliary constraint block.
Keep its coupling to ALL other variables. At regular points use
delta P_Z=-g*delta s-s*delta g; never divide by g at a node. Include the
discrete spatial-average factors when constructing the canonical embedding E.
On n17 the resulting dimension should be 2*(11*n-1)=372, before any physical
frequency/domain restriction. This is a finite-grid chart count, not a
continuum propagating degree-of-freedom assertion.

Check E^T*Omega*E=Omega_can, and retain the changing embedding:

    S=E^T*(K*E-Omega*E_dot),
    K*v=H''v-dOmega[v]*Xdot.

The node part of E_dot is annihilated by the exact initial null rows; retain
the regular Darboux-map derivative. Verify this identity rather than silently
freezing the canonical map. Require normalized symmetry/canonical/Schur and
cached-action controls <=1e-8. No omitted-drift or frozen-y shortcut is allowed.

## Mode normalization and uncertainty

Compute all frozen canonical eigenvalues, not a favourable subset. Numerical
diagonal balancing may be used only as an invertible CONSTANT symplectic
congruence, with all signs/directions retained. Recompute under an independently
fixed canonical rescaling and compare complete spectra. Do not call balancing
itself a physical energy norm.

For resolvable oscillatory modes report the action-derived symplectic norm
i*u^dagger*Omega_can*u and its energy/Krein sign, retaining near-zero-norm,
complex, zero and ill-conditioned modes as unresolved where appropriate.
Use the declared positive initial clock rate to report reference-proper-time
rates p*lambda_psi and dimensionless p*lambda_psi/H. Do not invent SI units or
infer stability of the evolving background from a frozen spectrum.

Record left/right eigenvector conditioning and backward errors. Fixed
numerical criteria: <=1e-8 backward residual, <=1e-6 canonical-rescaling
spectral agreement. These are diagnostics, not certified eigenvalue error
bounds or a physical cutoff. Preserve raw spectra when precision fails;
do not relabel unresolved modes as stable or remove them.

## Execution and preservation

Freeze contract and versioned sources after AST preflight before execution.
Use bounded Windows-spawn workers (max16), with parent-only append-only case
receipts and ignored progress. A local per-worker BLAS thread limit may avoid
oversubscription; it changes no host/provider configuration. No installation,
paid model/provider dispatch or global runtime reconfiguration is authorized.

Preserve completed case receipts if interrupted; a resume must validate their
source/input/sidecar identities and never overwrite them. Final acceptance
requires complete fresh read-only replay and external metadata guards.
Partial cases or manifests alone are not evidence that a process is live.

Stage2 remains INCOMPLETE and Stage3 NOT_ENTERED unless their original complete
acceptance is independently met. Continuum/weighted-domain admission,
time-dependent evolution/persistence, nonlinear interactions/cutoff, healthy
GR and both identifying matching inputs remain substantive. Rule9 DEFERRED;
physics_pass=false; gate_effect=NONE. No action change, state adoption/
evolution, vault mutation, manuscript/site, publication, commit or push.
