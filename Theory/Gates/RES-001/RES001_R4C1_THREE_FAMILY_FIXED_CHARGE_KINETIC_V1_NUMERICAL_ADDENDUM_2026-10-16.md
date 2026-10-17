# Fixed-charge homogeneous kinetic V1: execution and numerical addendum

16 October 2026. Frozen before the new executable is run.
Parent scope contract: 15 October V1, SHA-256
f071f31d7890e2b9e47650f30f9e216fbabf196a4f387a54bce078e8a3cc8d77.
The old working note remains unverified historical evidence and is untouched.
The existing Python environment now imports SymPy 1.14.0 and mpmath 1.3.0.
This observation does not establish the cause of the earlier process exits.

## Exact generic-action calculation

Use all 22 unspecialized mean fields. Extract the value, mixed and velocity
blocks from the exported action kernel before substituting any family map.
Check the density equation alpha=T_dot/C-beta*Pi; unit equation nu=0;
regulator Z equation b*Z=0; lapse primary momentum; homogeneous shift rows;
normal-block and density-chain inverse domains. Only then use the force-psi
clock Pi=0 and the corresponding lapse substitution.

Apply the evolving Cartesian-to-polar map and its nonlinear boundary generator.
All background derivatives act BEFORE an instantaneous orbit section u=R,
v_cartesian=0, u_dot=Rdot, v_dot=Q/(a^3*R). Check cyclic-angle and dust-origin
identities. Perform the two partial Legendre/Routh eliminations, retaining
the alignment-dependent angular Routh term and its boost curvature.

Verify the proposed kinetic matrices, exact principal minors and congruence
signatures, and independently differentiate the homogeneous Hamiltonian.
Use the already frozen diagnostic family maps without fitting or selection.
The result is restricted to homogeneous quadratic momentum/kinetic signs.
The full potential, physical characteristics, cutoff/window, nonlinear
remainder, original preparation admission and healthy GR remain separate.

## Archived-background controls

Use all 18 archived V3 runs and 21 nodes per run: 378 nodes, with their original
floating-point values converted through repr to 80-decimal arithmetic. No
interpolation, reintegration, charge reset or replacement of background H.

In the (x,R,r,five shear,three frame) basis, let

```text
G = diag(-2*M/3,1,1,Tm/4 [five],f2 [three]),
bvec = (2*M*H,-Rdot,-rdot,0,...,0)^T,
U = potential + rho + angular_energy_density,
W = 3*M*H^2-(Rdot^2+rdot^2+K*psi_dot^2)/2,
D = W-U.
```

Keep the raw action-derived fixed-both matrix with W and compare it with the
on-shell formula containing U. Verify the exact difference

```text
K_raw-K_shell = -D*bvec*bvec^T/(2*U*W).
```

This accounts explicitly for the archived constraint residual and must not be
called a repair of the saved background. Require the exact numerical identity
residual <=1e-50*max(1,matrix infinity norms). Report the observed raw/shell
difference and its bound |D|*||bvec*bvec^T||_inf/(2*|U*W|). The background
constraint control is |D|/(1+|U|+|W|)<=1e-7; this is a numerical control,
not a continuous finite-error certificate. Report its size relative to
K*psi_dot^2 as well, because that small scale conditions the clock reduction.

At every node require the stated positive quantities, W>0 and nonzero normal
determinant. Compute signed eigenvalues at 80 decimal digits for the active
3x3 fixed block and 4x4 variable-dust block, with the eight diagonal shear/frame
directions retained. Classify zero only within 1e-50*max(1,max|eigenvalue|).
Record signed minima/maxima and dimensions: 12 pairs at fixed U(1), 11 pairs
after the additional fixed-dust/global-origin quotient. This is a different
ensemble, not a change to the old prepared wave or its retarded timing result.

Require both methods to use identical saved time grids. Compare corresponding
background controls and kinetic eigenvalues at normalized tolerance 1e-7.
No tolerance is adjusted after inspecting the new results.

## Independent finite Hamiltonian controls

Use nine separate exact-initial-recipe controls (three families times three
registered eta values), not projected archived nodes. Construct H from that
recipe's Friedmann constraint at 80 digits and identify it explicitly as an
independent constrained control. Differentiate the unexpanded positive-clock
square-root Hamiltonian by central differences in all 11 momenta, including
mixed derivatives, and compare against inverse(K_fixed)/a^3.

Use h=1e-6*F/(1+sum|B*p|+max|B_ii|), then h/2. Require positive radicands at
every finite probe, and normalized Hessian error <=1e-10 at each step, with
the errors and step sizes retained. No convergence order or full physical
remainder is inferred from this numerical control.

## Provenance and rejection controls

Version the new executable, pin this addendum and the scope contract, inherit
the V3 immutable source manifest and its three known historical absent
sidecars, and check all existing source/sidecar hashes, sizes and mtimes before
and after. New receipts are written only to a fresh directory; failures and
exceptions remain visible. Exact read-only replay must reproduce every byte.

Reject omitted polar-basis/boundary drift, omitted density/normal/regulator
constraints, missing angular alignment, wrong Routh sign, missing dust Schur
term, erased varying-charge negative direction, eta=0 inversion, and any
promotion of kinetic positivity to full stability or a conserved energy.

Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE;
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
canonical K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Full native programme remains incomplete. No publication, commit or push.
