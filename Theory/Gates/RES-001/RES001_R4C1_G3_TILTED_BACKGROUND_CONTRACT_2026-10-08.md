# R4C1-G3T: tilted homogeneous background and regulator-clock test

Date: 8 October 2026. Owner: conditional R4C1-v1 / G3 / Master Test 1.
Frozen after analytic planning and source screening, before the executable.
Conditional; PROCEED_PROVISIONALLY; review DEFERRED; Rule9_cleared=false;
physics_pass=false; gate_effect=NONE.

## Purpose and decision boundary

G3V blocks ordinary cubic Taylor vertices at homogeneous Y=0. Test a
different, nearby homogeneous axisymmetric Bianchi-I branch with a frame
tilt and Y>0, using the unchanged action and six G3 parameter sets.
Construct constraint-compatible initial data and a local reduced IVP,
then determine regulator velocity rank in the dust clock.

A tilted dust-time Hessian is not by itself a physical ghost theorem.
A healthy preferred-frame higher-spatial-derivative scalar, written in a
tilted clock, can exhibit extra time roots. Include that exact control.
Do not announce a physical ghost, an all-background no-go, or a physical
cutoff from a dust-time subblock. Full finite-k constraints, the preferred
Cauchy domain and physical momentum/frequency window remain required.

## Frozen derivation

1. Signature (-+++), I x T3; all fields homogeneous, with equal transverse
   scales and tilt only along x. Use
   a_parallel=exp(alpha+2 sigma), a_perp=exp(alpha-sigma),
   H_parallel=alpha_dot+2 sigma_dot, H_perp=alpha_dot-sigma_dot,
   gamma=sqrt(1+w^2).
   Keep lapse N, physical shift B and B_dot in the direct metric/connection:
   g00=-N^2+B^2, g0x=a_parallel B;
   U0=gamma/N, Ux=(w-B gamma/N)/a_parallel.
   Verify norm/projector and cancellation of B/B_dot/N_dot from the
   homogeneous first-order action. Spatial momentum variation in this
   physical-unit chart is linked to the frame equation, not discarded.
2. Derive all four frame invariants, Q,Y, acceleration and Delta psi directly
   from the connection/projector. Check
   Y=w^2 psi_dot^2/N^2,
   Delta=[w^2(psi_ddot-N_dot psi_dot/N)
          +w w_dot psi_dot+2 H_perp w^2 psi_dot]/N^2.
   Add the Einstein ADM/GHY term, u,v,r potentials/portal, current alignment,
   force Q term, exact Y^(3/2) and original first-order z regulator.
3. On the smooth patch w>0, psi_dot>0, derive the full homogeneous action,
   its lapse equation and dust multiplier equation before gauge fixing.
   Use tau=t, N=1/C, C=exp(beta psi), and eliminate only lapse/epsilon.
   Do not eliminate z as an algebraic first-order auxiliary when its
   velocity mixes with psi_dot. Keep q=(alpha,sigma,w,u,v,r,psi,z).
   Check the reduced dust energy identity E=-exp(3alpha) rho_m/C and
   conserved U(1) charge including alignment. Verify the w=0 action
   reduces to the original isotropic G3 background action.
4. Export the 8x8 velocity Hessian. With m=H_psi,z=-b exp(3alpha) w^2/N,
   verify H_z,z=0 and the psi/z principal determinant -m^2.
   Check det H=-m^2 det R, where R excludes psi,z, and give an explicit
   congruence/inertia argument. Determine R rank and full inertia on the
   registered data; retain every rank loss. These describe the dust-clock
   homogeneous system, not finite-k physical residues.
5. Check the geometry/frame Hessian independently against the coefficients
   of Carruthers and Jacobson, arXiv:1011.6466v2, Eq.7, with
   w=sinh(theta), sigma=-sigma_plus, and their c_i replaced by
   (M_U^2/M_P^2)c_i. Respect their opposite signature and overall action
   normalization; do not transfer their stability claims to R4C1.
6. Healthy-control calculation: L=K (n.partial pi)^2/2-b(Delta pi)^2/2,
   constant n=(gamma,w,0,0) in flat spacetime, K,b>0, A=0.
   Preferred coordinates T=gamma t-w x, X=gamma x-w t give
   Omega=gamma omega-w k, P=gamma k-w omega.
   Verify D=K Omega^2-b P^4. At dust k=0 the nonzero roots have
   omega^2=K gamma^2/(b w^4), Omega=gamma omega, P=-w omega.
   Show these are points of the same preferred-frame dispersion, not a
   new independent preferred-frame field. Derive |v_group|=2 gamma/|w|
   there and the tilted-slice turning condition
   P_turn=sqrt(K/b) gamma/(2|w|).
   Keep this a comparator, not the full interacting spectrum.
7. After eliminating z in the bulk, export the coefficient of psi_ddot^2,
   -b exp(3alpha) w^4/(2N^3), and its nonzero highest-derivative Hessian.
   Compare with the healthy control. No physical instability conclusion
   may be based on this coefficient alone.

## Frozen numerical data and validation

Use archived G3 initial states at t=0 and unchanged parameters.
eta=(1,1/4,1/16,1/64,1/256,1/1024), w=(1/2,1/4,1/8,1/16): 24 cases.
Set alpha=sigma=0, sigma_dot=w_dot=z_dot=0. Retain u,v,r,psi and their
initial coordinate velocities (initial C=1). Set
z=w^2[H psi_dot+beta rho_m/K_Q], which matches the original G3 psi
acceleration at this initial jet after converting to the dust clock.
Solve the full lapse equation for the expanding H root nearest original H,
with rho_m equal to its positive archived initial value. Keep all roots,
rejections and normalized residuals; do not insert H as a fitting target.
Require normalized lapse/EL/Noether residuals <=1e-10 at initial jets,
finite nonzero Y, full Hessian rank 8, and residual check of all eight
reduced equations. Do not require kinetic positivity to pass an
obstruction audit; export its signs and inertia honestly.

Independent direct-covariant diagnostic jets:
a_parallel=7/5, a_perp=6/5, H_parallel=2/5, H_perp=1/3,
N=9/10, N_dot=1/11, B=-1/5, B_dot=1/9,
w=3/10, w_dot=-2/7, psi_dot=1/8, psi_ddot=-1/11.
All connection/invariant/projector/action identities must match exactly
symbolically. Independent central-difference velocity Hessian of the
direct homogeneous action at these jets uses h=1e-4,5e-5,2.5e-5 and
requires finest normalized maximum error <=1e-5, retaining all errors.

For eta=(1,1/1024), w=(1/4,1/16), integrate the full reduced 16-component
IVP over dust t in [0,1e-3] with DOP853 and Radau, rtol=1e-10,
atol=1e-12, 51 samples. Require success/finiteness, w>0, psi_dot>0,
rho_m>0, normalized energy and charge drift <=1e-8, and cross-method
normalized state difference <=1e-8. A domain exit is retained and blocks
dependent local smooth-background use. No long-time attractor, continuum
bound or physical EFT window follows from these short integrations.

## Evidence and authority

Pin this contract, action, G3/G3V receipts, exact versioned source and all
inherited scientific pins. Never run an old output-writing main.
Use a new numbered output directory, refuse existing paths, retain failures,
write immediate sidecars and implement nonmutating byte-identity replay.
Use a distinct G3T filename; do not edit the unversioned G3V source.

Register R9-MT1-G3T with G3V/G3I/G3DF and all inherited variation,
B1/G1/G2/S1/S2/S3/G3 branches, PD1 and applicable Track-A review debt.
The nearby background has different symmetry/initial data from G3.
Ordinary homogeneous-G3 scattering remains blocked by its retained cusp.
Full physical scattering/cutoff/healthy GR and Tests1-3 remain open.
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 unchanged. No action change, provider dispatch,
memory mutation, manuscript/PDF edit, commit, push, promotion or publication.
