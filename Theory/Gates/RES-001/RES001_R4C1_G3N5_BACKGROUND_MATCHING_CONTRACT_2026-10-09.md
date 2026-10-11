# G3N5 background matching: full first variation and on-shell input conditions

Date: 9 October 2026. Version 1, frozen before execution.
Master Test 1 / conditional R4C1-v1. physics_pass=false; gate_effect=NONE;
Rule9_cleared=false; review DEFERRED.

## Missing input, not a replacement goal

B1 already derives and evolves an interacting aligned homogeneous background.
Do not advertise another homogeneous calculation as general nonlinear T3
evolution. This checkpoint checks the match between those background equations
and all 22 response-field tadpoles of the G3N5 chart. It also checks the
background Hamiltonian propagation identity before any constraint-compatible
inhomogeneous response is constructed. The original full-kernel calculation
remains separate; no stop, restart or duplicate full-kernel run is authorized
by this checkpoint.

Use the frozen R4C1 action, SHA-256
81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3,
and the original G3N5 22-field chart without changing fields, signs or units.
The B1 report hashes to
48b49fddd9066d6df783eb336e00d49374f3845ec38414ee53fe0fad812348d8.
Its old receipt and trajectory remain immutable. The arbitrary off-shell jets
used to check local densities are not substituted for its evolved background.

## Required exact calculation

1. Derive the direct four-dimensional first-order ADM metric/inverse,
   connection, normalized n and raw U=(1+d nu)n with all x/y/z derivatives.
   Retain alpha, three shifts, six metric components, three frame velocities,
   du,dv,dr,Pi,T,Em,Z,nu,LambdaU and their independent jets.
2. Retain all four raw frame invariants, EH+GHY ADM bulk, the full potential,
   canonical scalars, temporal force, dust, unit multiplier and regulator.
   Show rather than assume that alignment, projected Y and regulator have
   no first-order bulk density about this specific aligned z=0 background.
   This does not delete them from the quadratic or nonlinear calculation.
3. Retain the linear spatial-Ricci divergence explicitly and verify that its
   periodic Euler operator is zero. It is not zero as a local density.
4. Compare the entire first-order density with a separate compact linear
   formula. Export every sector and all 22 background Euler expressions.
   Retain background coefficient derivatives and the 3H measure term.
5. Independently vary the lapse-unfixed homogeneous action with raw frame
   norm sigma, dust multipliers and regulator still present. Only afterward
   impose N=1, sigma=1, sigma_dot=0, tau_dot=C and z=0. Compare its lapse,
   scale, scalar, dust and raw-normal Euler expressions with the 22-field
   first variation. The unit equation must not be used to discard the
   normal-frame equation that determines lambda_U.
6. Derive the off-shell time-reparametrization Noether identity of that raw
   homogeneous action, including the multiplier Euler expressions. Verify
   the unreduced identity exactly before imposing a background equation.

Define rho=epsilon0*C^4, C=exp(beta psi0),
M_cos^2=MP2+MU2*(c1+3*c2+c3)/2 and
K_s=u_dot^2+v_dot^2+r_dot^2+K_Q*psi_dot^2.
Verify that all 22 tadpoles are precisely the B1 equations plus identically
zero symmetry components. In particular retain the Friedmann condition,
Raychaudhuri equation, lambda_U equation, scalar equations, conformal dust
continuity and psi source sign. Derive, do not impose, the off-shell identity
relating the time derivative of the Friedmann residual to these equations.
Wrong psi/dust source signs must fail this unchanged identity.

Explicit solved background rates are allowed only on a>0, C>0,
M_cos^2>0 and K_Q>0. Preserve the unsolved equations on singular boundaries;
do not divide by K_Q, M_cos^2, dust density, scalar amplitude or charge there.
Zero exchange alone is not pure GR. No continuous healthy GR inference is
permitted from this background matching.

## Independent local-density control, frozen thresholds

Use the already frozen v1 exact-unexpanded four-dimensional density routine
as a different implementation, without running its main or changing it.
Compare the non-Ricci first-order coefficient on its two generic all-direction
jets at 50-digit precision against centered first differences at
d=1e-3,5e-4,2.5e-4. Final normalized error <=1e-5; errors decrease or both
adjacent errors <=1e-12 at the arithmetic floor. The Ricci divergence has its
separate exact test. These are illustrative off-shell local jets, not a
numerical on-shell solution or an independent journal replication.

## Integrity and outstanding scope

Use new versioned source and attempt receipts only, refusing overwrite.
Verify direct/transitive source pins and available sidecars before and after.
Preserve original G3/N3 failures and inherited sidecar absences. Exact replay
must leave bytes, sidecars, lengths and timestamps unchanged.

Full G3N5 kernel execution and its independent temporal comparison, compatible
inhomogeneous initial data, nonlinear coupled response/evolution, physical
Cauchy/DAE domain, stability, EFT cutoff and healthy continuous GR remain open.
The homogeneous sector must be retained in that future solution. Review-only
debt remains deferred, not cleared. Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged. No action replacement, manuscript/PDF/vault change, provider
dispatch, runtime change, commit, push, promotion or publication.
