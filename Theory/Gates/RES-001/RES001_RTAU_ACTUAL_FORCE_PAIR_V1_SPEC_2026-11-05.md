# Actual initial force-pair remainder V1: execution specification

5 November 2026. The operator explicitly confirmed High and instructed proceed.
This satisfies the pending setting condition in the preserved 4 November
force-pair contract; its scientific requirements remain unchanged.

## Exact rows and comparison

Work in the original canonical coordinate xi=delta pi_psi, chi=delta psi,
zeta=delta Z and corrected w=delta Sigma-c P xi-alpha D chi. The normal
force temporal coefficient m=(mu/N)f_pp is positive on the registered Y>0
branch. Use aphi=1/m and vphi=N*f_ps/f_pp, not a scalar-only surrogate.
The exact material clock row before the paired spatial gauge correction is

    chi_t-S D chi = aphi*xi-vphi*D chi+sum(B_j*delta q_j),
    B_j = -(N/f_pp)*(f_p*delta_j log mu
                      +f_pgamma*delta_j gamma+f_pw*delta_j Vz
                      +f_pkappa*delta_j kappa)
          - beta*N*p*delta_j,psi.

The last term is the lapse variation, not a dropped source. Derive the
momentum row by linearizing the previously proved exact current

    pi_t=D(S*pi-M*f_s+d*D Z-2*beta*d*Z*s)
          +beta*M*(e_force-Sigma)-beta*L_reg,
    L_reg=b*M*Z^2/2-d*(D Z)*s+beta*d*Z*s^2.

Use delta Sigma=w+c P xi+alpha D chi. Keep all current and local terms
together: in particular, the coefficient of D zeta is d_z-beta*d*s.
Only the corrected compensated-current background and reconstruction are
allowed for the Sigma source. Retain original global/charge conditions.

For the auxiliary row, differentiate the FULL linearized spatial Laplacian,
not zeta=-kappa D^2 chi alone. At the conformal initial slice let
lambda=a_z/a, kappa=a^-2, ell=kappa*lambda. Then

    zeta=-kappa*D^2 chi-ell*D chi+sum(P_j*q_j+Q_j*D q_j),
    P_0=P_3=a^-4*lambda*s, P_5=a^-4*D s,
    Q_0=Q_3=-a^-4*s/2, Q_5=a^-4*s/2,

with all other P_j,Q_j zero. Differentiate these coefficients using the
actual registered initial metric velocity and psi velocity. Their instantaneous
conformal form is an initial-data identity, not an assumed future solution.
Retain material-advection commutators. Use raw ordinary canonical velocities
in this row before adding the complete paired gauge correction; replacing
only those velocities by projected ones would omit clock/gauge cancellation.

The principal force block is the registered variable-coefficient block

    zeta_t-S D zeta = -kappa*aphi*D^2 xi
       -(2*kappa*aphi_z+ell*aphi)*D xi-vphi*D zeta
       + registered ordinary-to-force first-derivative coupling + R_Z,
    xi_t-S D xi = d*D^2 zeta+(d_z-beta*d*s)*D zeta
                  -vphi*D xi+R_xi.

Keep the reverse ordinary-to-force coupling exactly. If D q=L Y18+R_q
and v_raw=V_raw Y18+R_v, its differential coefficient is

    -kappa*B_ordinary*L+Q_aux*V_raw+vphi*Q_aux*L.

Verify its equivalence to the registered full shift-Schur expression:
V_raw=V_projected-B_gauge*shift_gradient and
Q_aux*B_gauge=(0,0,kappa*s). The clock and metric gauge high derivatives
cancel TOGETHER, leaving the exact scalar Lie correction xi_gauge*D Z_bg.
Do not count a first-derivative cross block as an L2 remainder.

## Constants, controls and limits

Reuse corrected ordinary reconstruction and smoothing remainders, not held
older bounds. Bound B_j and its first two spatial derivatives from the closed
full force and frozen spatial jets. Reuse a justified bound on the third
background shift derivative where state construction requires it. Do not infer
derivatives from an interval radius. Ordinary raw-velocity remainders follow
from the full temporal inverse, metric/momentum smoothing and zeroth terms.
Include paired gauge and coordinate pullback constants and the harmonic input.

Produce explicit nine-input L2 remainder constants in the corrected strong
norm, with all 20 principal directions and finite-dimensional partners kept.
Use exact symbolic generic current, auxiliary, material and gauge identities;
independent periodic controls; full-force derivative controls; whole-circle
root enclosures; and byte-identical replay. Interval overlap with the cached
Hessian is a consistency check only, not an identity proof. Preserve failures,
old sources, sidecars and unrelated edits; add new sources and fresh receipts.

Acceptance is the INITIAL force-pair component only. The actual density row,
moving Green/range maps, complete generator, energy/domain persistence,
time tube, interactions/window and identifying matching remain incomplete.
R-tau UNADOPTED; Rule-9 DEFERRED; physics_pass=false; gate_effect=NONE.
