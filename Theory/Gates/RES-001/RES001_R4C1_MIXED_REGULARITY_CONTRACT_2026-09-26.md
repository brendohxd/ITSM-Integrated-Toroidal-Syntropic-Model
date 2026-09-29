# R4C1-S4B: one-extra-dust-derivative coupled estimate diagnostic

Date: 2026-09-26. Frozen before executable and new numerical results.
Branch: recovery/v12-core-architecture. Owner: Master Test 1 / R4C1-v1/B1.
Claim status: Conditional. Review DEFERRED; Rule9_cleared=false;
physics_pass=false; gate_effect=NONE.

## Question

S4A proved that its fixed full scalar graph metric admits a logarithmic norm
rate growing at least as p/2. Test the precise additional derivative suggested
by the independently varied dust continuity control. This is a new, stronger
Sobolev domain, not a uniformly equivalent change of norm. No pressure term,
damping, constraint deletion, action change, parameter retuning, new matter
coupling or altered S4A result is allowed.

## Frozen map and domain

Read the pinned S4A full 15-by-12 graph map F(t,k) and S2 full generator
A=[[0,I],[-W,-G]], with W=Vc+Mcdot. Verify the source/sidecar and transitive
receipt hashes before using them. Inherit R9-MT1-S4A/S3/S2/S1/B1/VARIATION.
The unchanged B1 chart requires a>0, H>0, rho_m>0, finite positive C,
nonzero torus mode k=2*pi*n and the S1 auxiliary-rank conditions.

At fixed comoving k set p=k/a, v_d=p*delta tau/C. Append exactly one row

    p*v_d = p^2*delta tau/C

to F. Denote the resulting 16-by-12 matrix by F_1 and S_1=F_1^T F_1.
Use coefficient one in the same B1 reference units as S4A. Do not optimize
this coefficient or choose a different p power after inspecting results.
The torus Sobolev space is the square-summable mode collection with norm
sum_(k!=0) (1+|k|^2)^s ||F_1 Z_k||^2 at a declared fixed s, where the
reference length and physical-to-comoving conversion are as in S1. This adds
one spatial derivative of dust tilt to the S4A domain. It remains a diagnostic
graph norm, not the physical Hamiltonian or a certified invariant energy.

Differentiate at fixed k, so pdot=-H*p. Verify exactly

    d/dt(p*v_d) = p*(d/dt v_d-H*v_d)

under the S2 time-dependent generator and B1 background flow. Use
L_1=F_1dot+F_1 A and E_1=L_1^T F_1+F_1^T L_1. Check the full twelve-dimensional
identity d||F_1 Z||^2/dt=Z^T E_1 Z. S4A's rank minor remains a subminor of F_1;
verify its hash and nonzero-domain meaning, but do not claim a uniform lower
metric bound merely from pointwise rank.

## Fixed diagnostics and decision rule

Evaluate mu_1=0.5*lambda_max(E_1,S_1) at the same six B1 coefficient times
(0,0.5,1,2,3,4) and physical p=2*pi*2^j, j=0,...,8. Retain the S4A mu
alongside it as a comparator, without overwriting old samples. Evaluate the
two existing S2 full endpoint transfers at t=4 for n=(1,2,4,8), with both
DOP853 and Radau endpoints. Report all numbers and graph conditioning.

Use at least 60-decimal arithmetic for positive-metric Cholesky/SVD and an
independent generalized-eigenvalue route to transfer amplification. Require
relative agreement <1e-8; inherit the <1e-5 two-solver tolerance. A centered
background derivative at fixed k with h=1e-6 must agree with E_1 to relative
<1e-5. Negative controls must detect omission of pdot=-Hp, Fdot, Mcdot and
accidental reuse of the old fifteen-row metric. Any failed source, rank,
derivative or method check yields UNVALIDATED; preserve the failed outputs.

A finite grid with bounded-looking mu_1 or amplification does not prove a
uniform estimate. A positive full-system bound requires an analytic
wave-number-independent mu_1 (or a rigorously justified alternative energy)
over a specified background time/domain, integration of that bound, and
well-defined constraint reconstruction. If an exact high-p witness or
unbounded rate is found in F_1, record a negative result for this new space.
Do not infer ill-posedness from a local rate alone. If unresolved, state
exactly which symbolic estimate remains open.

Keep k=0, H=0, auxiliary singularities, other spin sectors, causality,
cutoff, healthy GR recovery and physical matching outside this checkpoint.
No Test-1, MAT-001, UVIR-003, Stage-4A or publication promotion follows.
