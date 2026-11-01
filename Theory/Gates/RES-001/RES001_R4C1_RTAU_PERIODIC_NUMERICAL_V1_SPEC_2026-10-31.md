# R-tau periodic numerical candidate: frozen V1 specification

This executes the periodic-preparation contract's numerical candidate stage,
not its continuum acceptance. Tail and inverse/domain bounds remain required.
Use the full R-tau physical density, positive clock branch and exact nonlinear
Z reduction. High last confirmed; no changed coefficients or parent adoption.

Freeze epsilon=1/1000, period 2*pi, planar k=1. Initial metric is conformal,
lambda=epsilon*cos(z)/13, h=exp(2*lambda)*I. Scalars are
u=1+epsilon*cos(z)/17, v=epsilon*cos(2z)/19,
r=1+epsilon*cos(3z)/23, psi=epsilon*(cos(z)/29+cos(2z)/31).
Physical frame V=epsilon*((1+cos(z)/2)/37,cos(2z)/41,sin(z)/43).
It has all three frame components and a nonzero transverse component.
This diagnostic initial-data choice is not a microscopic prediction.

Metric velocity is 2*h*(H+epsilon*cos(2z)/31). Scalar velocities are
u_dot=epsilon*cos(2z)/53, v_dot=omega+epsilon*cos(z)/59,
r_dot=1/4+epsilon*cos(z)/61, psi_dot=1/5+epsilon*cos(3z)/47.
Physical frame velocities are epsilon*(cos(2z)/67,cos(z)/71,sin(2z)/73),
converted to the actual coordinate-frame variables including metric drift.
All spatial derivatives, including Z_z, come from these exact profiles.

Free continuation data are H and omega; target normalized clock and U(1)
charges are 1/5 and 1, inherited from old B1. No target acceleration is used.
At each node differentiate the original full density BEFORE lapse substitution
using independent S,S_z,N,N_z and scalar velocities. After differentiation
evaluate N=exp(-beta*psi), N_z=-beta*N*psi_z, tau_dot=1, epsilon_dust=0
to isolate nonmatter lapse flux. Reconstruct rho from E_N/sqrt(h), and
charge integrals from actual canonical momenta, retaining both lapse fluxes.

Use odd collocation sizes 9,17,33 with every nonconstant real Fourier mode;
all three shifts have mean zero as the coordinate gauge. Solve full projected
E_S=L_S-d_z(L_Sz) and both mean charge equations with frozen aligned inverse
as a chord-iteration preconditioner. Maximum 30 steps, residual <1e-10.
This is a numerical candidate, not a proof of convergence or uniqueness.
Record integrated momentum residuals separately; failure cannot be repaired
by suppressing their mean. Reflection parity is a control, not a projection
of evolution: scalars/diagonal metric/Vx,Vy are even, Vz is odd.

Use 40-digit local physical-action differentiation and double-precision
Fourier assembly. Preserve all attempts; record positive density, lapse,
tilt, parameter shifts, all shift coefficients and full residual histories.
Compare grids and independent omitted-flux/reconstruction controls. Do not
declare continuum tail bounds or a nonlinear admitted solution from these
finite grids. Fresh receipt and immutable replay. Full periodic preparation
remains INCOMPLETE until the owning contract's explicit bounds are proved.
Review DEFERRED; physics_pass=false; gate_effect=NONE; no new action or state.
