# R4C1-G3K: coupled finite-k scalar action and clock-domain contract

Date: 8 October 2026. Owner: conditional R4C1-v1 / G3T / Master Test 1.
Frozen after analytic planning and source reads, before the executable.
Conditional; PROCEED_PROVISIONALLY; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Scope and scientific decision

Derive the complete quadratic scalar Fourier action for propagation along
the tilt axis on the previously sealed G3T homogeneous backgrounds.
Retain metric, longitudinal frame, condensate, reservoir, force and regulator
couplings. Retain lapse/dust and longitudinal-shift constraints.
This is a closed axisymmetric scalar sector, not the complete tensor/vector/
arbitrary-direction spectrum, a physical S-matrix or an EFT cutoff.

A dust-clock kinetic sign or a frozen eigenvalue is not alone a physical
ghost/instability verdict. Keep all signs, roots and constraint singularities.
Use the aligned S1/G3S limit and the healthy preferred-frame regulator control
to prevent gauge/clock artifacts being promoted to physical exclusions.

## Exact action and gauge

1. Signature (-+++). Let a_parallel(t),a_perp(t) be the G3T reference scales.
   Retain a scalar transverse curvature xi(t,x):
   gamma_xx=a_parallel^2, gamma_yy=gamma_zz=a_perp^2 exp(2xi).
   Radial metric perturbation is removed by the longitudinal spatial
   diffeomorphism only for k!=0. Use physical shift B(t,x), lapse N(t,x),
   U0=sqrt(1+w^2)/N, Ux=(w-B sqrt(1+w^2)/N)/a_parallel.
2. Derive the exact first-derivative scalar-sector action from the covariant
   frame/projector and Einstein ADM/GHY terms. Define orthonormal jets
   e0 f=(f_dot-B f_x/a_parallel)/N, e1 f=f_x/a_parallel;
   nu=N_x/(N a_parallel),
   Kx=(H_parallel-B_x/a_parallel)/N,
   F0=(H_perp+xi_dot-B xi_x/a_parallel)/N, F1=xi_x/a_parallel,
   d0=e0 w/sqrt(1+w^2)+nu, d1=e1 w/sqrt(1+w^2)+Kx.
   Verify I1=-d0^2+d1^2+2(gamma F0+w F1)^2,
   I2=(w d0+gamma d1+2 gamma F0+2 w F1)^2,
   I3=(w d0+gamma d1)^2+2(gamma F0+w F1)^2,
   I4=(gamma d0+w d1)^2 and the exact normalized projector.
3. Retain Q_f=gamma e0 f+w e1 f and S_f=w e0 f+gamma e1 f.
   Force Y=S_psi^2, alignment Y_J=S_J^2; regulator is
   b z^2/2-b S_z S_psi-b z (gamma d0+w d1) S_psi.
   Use the original scalar/portal potential and canonical u,v,r terms.
   On the stated smooth patch S_psi>0, the exact force term is -A S_psi^3.
   At the aligned zero-gradient control use only its valid C2 Hessian,
   never claim a third Taylor vertex.
4. Derive R3=-(4 xi_xx+6 xi_x^2)/a_parallel^2 and its explicit periodic
   integration-by-parts boundary density. The first-derivative Einstein
   density is M_P^2 N V[
   xi_x^2/a_parallel^2+2(N_x/N)xi_x/a_parallel^2-2Kx F0-F0^2],
   V=a_parallel a_perp^2 exp(2xi).
   Check the action before and after this spatial boundary transformation.
5. Vary the dust multiplier before using tau=t, N=exp(-beta psi).
   Lapse variation determines epsilon/rho_m. Eliminate only these algebraic
   dust-clock variables. Keep q=(xi,w,u,v,r,psi,z), B and B_x; no B_dot.
   Verify the homogeneous action matches G3T under
   alpha=alpha_bg+2xi/3, sigma=sigma_bg-xi/3.

## Fourier constraints and evolution coefficients

6. Form the Hessian in (q,q_dot,q_x,B,B_x), evaluate at xi=0, spatial
   gradients zero, B=B_x=0, and the full evolving G3T fields/velocities.
   For each k!=0 construct
   T=L_dd, W=L_dq+i k L_dx,
   Vmat=L_qq+i k(L_qx-L_xq)+k^2 L_xx,
   F=L_Bd-i k L_Bxd,
   G=L_Bq+i k L_Bx-i k L_Bxq+k^2 L_Bxx,
   A_B=L_BB+k^2 L_BxBx.
   Preserve Hermitian signs and explicit variable-index meanings.
   Eliminate B only when A_B!=0:
   Tred=T-F_dagger F/A_B, Wred=W-F_dagger G/A_B,
   Vred=Vmat-G_dagger G/A_B.
7. Derive each coefficient time derivative at fixed comoving k using the
   actual G3T background flow, including scale factors and accelerations.
   Export the nonautonomous operator
   Tred q_ddot+(Tred_dot+Wred-Wred_dagger)q_dot
              +(Wred_dot-Vred)q=0.
   Reconstruct the unreduced field and shift equations after elimination.
   Do not use a frozen action pencil that drops coefficient derivatives.
8. Verify the generic shift coefficient and its G3 substitution. Classify
   every zero/sign surface explicitly; never invert k=0 or a vanishing
   shift coefficient. Evaluate the analytically predicted finite-tilt
   rank surface separately without performing its singular reduction.
   A Schur-chart failure does not itself prove a physical singularity.
9. Aligned isotropic control: w=w_dot=z=z_dot=0. Its reduced kinetic
   form must agree with S1/G3S after the dust-clock/radial-gauge mapping:
   Tred=V C diag(Dbar,eta/6,1,1,1,3eta,0),
   Dbar=144(1-eta/12)(1-eta/8)/eta.
   Verify the z row has no velocity coupling and can be eliminated
   algebraically in that control. Recover the old positive six-field
   kinetic weights, not an incorrectly frozen metric Hessian.

## Frozen numerical checks

Initial jets: all 24 G3T cases, k=(20,40,80): 72 events.
Evolved jets: G3T's four evolved eta/tilt cases, both saved methods,
t=(0.0005,0.001), the same k: 48 events; total 120.
Use the sealed arrays and full G3T flow; do not re-integrate or retune the
background to choose a different result. All roots/inertias are retained.

For every event require Hermitian Tred,Vred, nonzero shift denominator,
finite matrices, reconstructed constraint/variational residuals <=1e-9,
and normalized complete frozen-operator eigenpair residual <=1e-7.
Report complete 14-dimensional eigenvalue sets, positive real parts,
and matrix rank/inertia; positivity and absence of growth are NOT pass
requirements for this diagnostic. Use a static congruence only to
condition the instantaneous eigenproblem; never omit derivatives of a
time-dependent canonical normalization in an evolution claim.
Cross-method coefficient/root-set discrepancies must be retained;
require normalized coefficient agreement <=1e-6 at shared evolved jets.

Independent direct-connection/action benchmark uses the G3T diagnostic
geometry, w=3/10, w_dot=-2/7, xi=7/100, xi_dot=-11/100,
xi_x=13/100, xi_xx=3/100, w_x=17/100, B_x=37/100,
psi_dot=1/8, psi_x=1/20, z=2/25, z_dot=3/100,z_x=-1/25,
u=3/4,v=1/5,r=3/5 with velocities (1/10,-2/25,7/100)
and gradients (3/100,-1/50,1/100), eta=1/4.
Use N=9/10, N_x=-beta N psi_x and the defining metric/connection.
Check action/invariants/projector identities <=1e-12.
Independent central-difference jet Hessian uses h=(1e-4,5e-5,2.5e-5);
require finest normalized error <=1e-5, retaining every error.

For eta=(1,1/1024), tilt=1/4, k=(20,80), integrate the resulting
time-dependent scalar perturbation equations with both DOP853 and Radau
over [0,1e-3], rtol=1e-10,atol=1e-12,51 samples.
Use unit normalized initial delta_psi and zero other fields/velocities;
the physical perturbation amplitude is 1e-12 for the smooth-gradient
patch diagnostic. Use the archived background with its stated numerical
interpolation or the same fixed on-shell flow; preserve the choice and
check its agreement with the sealed trajectory.
Require finite successful runs and cross-method normalized state
difference <=1e-7. Reconstruct the shift at every sample and retain
physical-gradient fractional amplitudes; require <=0.01.
A domain exit is preserved and blocks dependent smooth-patch use.
No long-time, uniform PDE or physical EFT theorem follows.

## Clock control and evidence

Retain the healthy fixed-frame scalar with preferred dispersion
Omega^2=c_psi^2 P^2+(b/K_Q)P^4, c_psi^2=6A sqrt(Y)/K_Q>0.
Verify the Lorentz covector mapping from dust proper frequency/momentum,
and its extra dust-zero-k roots. Derive the momentum turning criterion
v^2(c_psi^2+2(b/K_Q)P^2)^2=c_psi^2+(b/K_Q)P^2.
This is a comparator and cannot be substituted for the coupled spectrum
or an action-derived cutoff. Global preferred leaves on I x T3 remain open.

Pin this contract, G3T, S1/G3S and all inherited sources. New numbered
outputs only, immediate sidecars, nonmutating byte-identity replay;
preserve every failed implementation/source/receipt. Register R9-MT1-G3K
with all G3T/G3V/G3I/G3DF/G3S/variation/PD1/Track-A review and physics debt.
Canonical Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No parameter/action change, provider dispatch, memory mutation,
manuscript/PDF edit, commit, push, promotion or publication.
