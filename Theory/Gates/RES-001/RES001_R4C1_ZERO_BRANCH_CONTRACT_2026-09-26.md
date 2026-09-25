# R4C1-S3: zero branch and original-variable regularity

Date: 2026-09-26. FROZEN_BEFORE_EXECUTABLE. Master Test 1.
Action and B1 parameters unchanged; no new pressure, damping or projection.

## Question and inputs

Resolve what S2's defective zero-speed symbol does and does not imply.
Trace its Jordan chain into the original constrained fields and dust density,
and distinguish equal-order canonical norms from a declared original-variable
differential-order norm. This is not a general nonlinear well-posedness proof.

Pin S2 executable 745fd890250e965f3d1e5d562d72667e12c16ca6608fad9a72439fa735fcbbda,
S2 matrices 6e5379d6fa05ee7a3c78c78d9d731de14f4346c28425857fd3a02ed155d30e70,
S2 receipt 56a4db658ae24d86211148abaffc1b9cf4d3d5aceed2e732df1270abda737735,
S2 report 653541272bfe9b1ddfd82d7083cd77ba30e421daa3b7162816783d5ed03633d9,
and S1 matrices 27d5a7130293866373ec1a98fbb6d0be0036421ef937416f77dd05b80f61349a.
Check transitive receipt pins. Inherit unreviewed R9-MT1-S2/S1/B1/VARIATION;
review DEFERRED, with provisional diagnostic use allowed.

## Exact leading-symbol question

Use Z=(p*x_slow,xdot_slow), with p=k/a, and freeze coefficients at a fixed
background event only for this local principal calculation. S2 gives
Zdot=p*A*Z, A=[[0,I],[-L2,-G1]]. Restrict to the coupled normalized T,W
block; derive an exact zero-eigenvector e0 and generalized vector e1 with
A*e1=e0. Construct the spectral projector P0 and nilpotent N=A*P0.
Verify P0^2=P0, N^2=0, N!=0 and
exp(p*t*A)*P0=P0+p*t*N. Display an explicit unit-normalized initial sequence
showing failure of a p-uniform bound in the stated equal-order Z norm.
Do not turn this chart-dependent statement into an all-formulation no-go.

Independently derive the irrotational pressureless matter control from the
frozen dust action, with fixed Minkowski metric and constant C and density.
Its linear continuity and Euler equations must be varied before imposing
the multiplier constraint. Determine the density/velocity principal matrix
and the derivative needed for a bounded mixed-regularity linear estimate.
This control is not a replacement for the coupled curved solution.

## Reconstruction and preregistered graph norm

Use the exact S1 auxiliary solutions and S2 time-dependent R map.
The Einstein-frame rest density perturbation is
delta rho=C^4*delta epsilon+4*beta*rho*delta psi on the dust constraint.
The dust tilt relative to the ADM normal is v_d=p*delta tau/C;
the relative frame/dust tilt is w-v_d. Derive these identifications and
verify the dust normalization and multiplier equation. Retain coordinate
lapse/shift separately and do not call them propagating observables.

Embed the slow principal sector into the six canonical fields using the
leading fast-mode Schur relation, including the derivative of its coefficient
at fixed comoving k when reconstructing velocities. This embedding is an
asymptotic relation, not an exact solution of the full time-dependent equations.
Reconstruct q, qdot, lapse, shift, delta epsilon and delta rho on both Jordan
vectors. Export the exact maps and all leading powers of p.

Before seeing the result, define the positive graph norm as the sum of
squares of these reference-unit quantities:

```
delta f, p*delta f, delta fdot  (f=u,v,r);
sqrt(K_Q)*delta psidot; sqrt(b)*delta Delta_psi;
sqrt(M_U^2*c14)*wdot; sqrt(M_U^2*cL)*p*w;
delta rho/rho; v_d.
```

It is an explicit differential-order/Sobolev diagnostic, NOT the physical
Hamiltonian or a unique invariant energy. It requires rho>0 and inherits
the regular S1/S2 chart. It is not permissible to choose extra weights
after the run merely to suppress growth. Report its rank and conditioning.

Let F(p) map the two Jordan amplitudes into those quantities and B=F^T F.
Evaluate the restricted transfer E(t)=[[1,p*t],[0,1]] using its induced B
norm and compare with the equal-order canonical norm. Use coefficient times
(0,0.5,1,2,3,4), principal duration t=1 in reference units and
p=2*pi*2^j for j=0,...,8. These are local-symbol probes, not full trajectories.
Report all amplifications and exact large-p powers. If a rescaling of the
Jordan amplitudes has a finite positive graph-metric limit, derive it from
the exported powers and state explicitly the added derivative requirement.
Do not call numerical boundedness over this finite grid a uniform theorem.

Checks: source hashes; exact Jordan/projector identities; independent dust
Euler/continuity variation; exact reconstruction/normalization identities;
rejection of an invertible p-uniform diagonalizer for a Jordan block; graph
metric rank and agreement between Cholesky and generalized-eigenvalue
amplification to relative 1e-8. Negative controls must detect dropping the
generalized eigenvector and claiming equal-order boundedness from a
derivative-weighted norm. Unknown/failed ranks remain unresolved.

## Decision boundaries

Distinguish (a) failure of a uniform equal-order estimate in the displayed
canonical chart, (b) a declared derivative-weighted estimate/control, and
(c) the still-unproved complete constrained initial-value problem. No
coordinate-dependent numerical success establishes (c). Record whether
the pressureless mechanism contributes, whether a true additional coupling
pathology is demonstrated, and exactly what remains open.

No canonical promotion, provider dispatch, model switch, commit or push.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; physics_pass=false; Rule9_cleared=false.
