# Full planar variational evolution backend: frozen contract

28 October 2026. Conditional; Rule-9 DEFERRED; G1-G6 INCOMPLETE;
physics_pass=false; gate_effect=NONE.

Implement the original R4C1 action in implicit weak form before attempting
evolution. Preserve all six metric, three frame, u,v,r,psi,Z and dust-clock
coordinates plus the dust multiplier. Keep lapse/gradient and shift/gradient
variations, the unit-frame chart and radial-multiplier reconstruction. No
slow graph, stationary-node assumption or full-matrix nodal inversion.

The old initial-acceleration engine sets R3=0 and cannot be used unchanged
away from its initial flat slice. Derive the full nonlinear spatial Ricci
weak density and its divergence B. BEFORE fixing lapse, use

    N*sqrt(h)*R3 = N*L_GammaGamma - N_z*B + partial_z(N*B).

The local lapse constraint must retain the resulting divergence. A torus
integral of a derivative vanishing does not delete the local term. Keep the
original Einstein/GHY convention, normalized-frame lapse gradient, full
temporal/spatial regulator, potentials and original conformal dust action.

Deliver executable L(q,q_t,q_z,S,S_z,N,N_z) and its first variational
derivatives for16 q entries (the original14 plus tau,epsilon). The implicit
Euler equations and constraint equations must require no division by w^2.
Derive the moving-interface condition from distributional integration by
parts, rather than imposing it or reusing a fixed-node jump formula.

Validate with the pinned original full coordinate density, including general
nonflat metric jets and nonzero lapse gradient. Check all six metric curvature
Euler entries against the independent3D Ricci/Einstein variation, lapse
curvature variation, a conformal analytic benchmark, direct first variations
and exact initial-node first variations. Use110 decimal digits, complex
steps1e-20 and1e-26 where applicable, normalized tolerance1e-18, four general
jets and both node orientations. Preserve every failure; use fresh receipts
and immutable replay. Pin original sources and sidecars.

State a candidate variational domain where all original action products and
first variations are integrable. This is NOT an adopted invariant solution
space. Identify the estimate needed to evolve there. Quantify why naive
unweighted source control is insufficient near g=b*w^2 using a registered-
weight countersequence with explicit constants. Such a countersequence is
not claimed to be a physically admitted perturbation or an action no-go.

No weak solution, existence/uniqueness, background admission or time interval
is accepted from this backend or action-domain membership alone. A separate
controlled approximation and evolved estimates are required. Retain the
known cusp/interfaces and all physical/matching holds. No parent/state
adoption, memory mutation, provider dispatch, publication or commit/push.
