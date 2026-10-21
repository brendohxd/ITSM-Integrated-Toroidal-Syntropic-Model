# R4C1 regular-planar Hamiltonian: means, charges and global constraint retained

19 October 2026. Conditional unchanged-action Stage-2 calculation.
Local493/493; full fresh eight-worker read-only replay exact.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result and purpose

The nonlinear regular-planar Hamiltonian needed for a coupled second-variation
calculation is now explicit and executable. It retains the full metric,
frame, matter, phase, reservoir, regulator and inhomogeneous dust response.
It solves the known spatial constraints without deleting the three mean
metric canonical pairs or silently projecting away the global momentum
constraint. Both global charges are fixed, but their local fluctuations
remain dynamical. The clock-weighted lapse flux and spatial Ricci remain.

This supplies a necessary reduction, NOT the missing physical spectrum or
validity window. Numerical controls here are nodeless method controls,
not replacement registered backgrounds or newly admitted physical states.
The actual w=e*cos(k*z) profiles have exact nodes. The regular inverse
cannot establish their global domain merely because a finite grid misses
those nodes. The prior opposite-sign patch form is not removed or repaired.

## Exact regular-planar spatial reduction

Use normalized coordinate average < >; multiply by coordinate-cell volume
for integrated quantities. Work in the local planar gauge section

~~~text
h(z) = [[G(z),m],[m^T,L]],
G symmetric positive2x2; m=(h_xz,h_yz), L=h_zz spatially constant.
~~~

m and L remain time-dependent canonical coordinates. Their momenta are
P_mA=2<pi_Az>, P_L=<pi_zz>; their deletion would lose physical mean pairs.
Only the nonzero spatial modes of h_iz are fixed by the local gauge.
Throughout the component formulas, pi_iz and pi_AB denote the contravariant
momentum-density components pi^{iz} and pi^{AB}, not metric-lowered momenta.

This section has the expected local gauge kernel. A residual planar spatial
diffeomorphism would give delta h_Az=a_A and delta h_zz=2a_z, constant in z.
The Lie derivative yields h(z)*xi'(z)=a. Periodicity implies
A*a=0, where A=<h^-1>. For nonzero real x,

~~~text
x^T A x = <x^T h^-1 x> > 0.
~~~

Thus A is positive definite, a=0 and xi'=0. Only constant translations
remain. This is a local regular-planar statement, not an arbitrary3D/global
gauge-existence theorem. Transverse constant translations act trivially on
planar fields; the longitudinal one is handled below.

After the independent original unit/dust variations and force clock
psi=tau, the original spatial constraints become

~~~text
C_A = -2*(h_Ak*pi_kz)' + (p_VA*V^z)'
C_z = -2*(h_zk*pi_kz)' + S
S = pi_AB*G_AB' + p_Vj*(V^j)' + (p_Vz*V^z)'
    + p_R*R' + p_theta*theta' + p_r*r' + p_Z*Z' + p_T*T'.
~~~

Symmetric AB contraction counts pi_xy twice. V^z is CONTRAVARIANT; the
field label Vz in code/contract does not mean the lowered component.
The psi contribution vanishes because the clock has psi_i=0.

The necessary remaining global equation is <S>=0, not permission to discard
the mean of an arbitrary source. Choose the longitudinal-origin chart

~~~text
f=<sin(k*z)*V^y>=0, d=<sin(k*z)*(V^y)'> !=0
p_Vy=p_Vy0+lambda*sin(k*z), <sin(k*z)*p_Vy0>=0
lambda=-<S0>/d.
~~~

Here S0 uses p_Vy0. This solves the global constraint exactly. Its term in
the canonical one-form is lambda*delta f=0 on the gauge section. The bracket
with constant longitudinal translation is d. A vanishing d is a chart
singularity, not a new physical exclusion; do not divide there.

Now I_z is the zero-mean periodic primitive applied to the zero-mean S.
The complete solution of the three remaining spatial rows is

~~~text
rvec=(p_Vx*V^z/2, p_Vy*V^z/2, I_z(S)/2)
M=(P_mx/2,P_my/2,P_L)
cvec=A^-1*(M-<h^-1*rvec>)
pi_iz=h^-1*(rvec+cvec).
~~~

Indeed h*pi_z-rvec is constant, so all C_i vanish, and averaging gives
<pi_iz>=M. A's positivity proves that fixing the mean momenta introduces
no additional singular mean system on the stated positive-metric domain.

## Fixed charges, one-form and full Hamiltonian

Use the exact finite polar map u=R*cos(theta), v=R*sin(theta), R>0:

~~~text
p_u=p_R*cos(theta)-p_theta*sin(theta)/R
p_v=p_R*sin(theta)+p_theta*cos(theta)/R
p_u*delta u+p_v*delta v=p_R*delta R+p_theta*delta theta
u*p_v-v*p_u=p_theta.
~~~

This is a local zero-winding phase chart, not an adopted winding sector.
Write p_theta=Qtheta+fluctuation and p_T=Qdust+fluctuation, with fluctuations
and theta,T of zero coordinate mean. Quotient only the two global origins
at fixed Qtheta,Qdust; retain both local canonical pairs. The corresponding
fixed-charge origin terms are exact boundary terms. T=t is NOT also imposed.

The remaining canonical one-form is the average of the G_AB, V, R, phase,
r, Z and dust pairs, plus P_m*delta m+P_L*delta L. The solved pi_iz drop
only against the removed NONZERO-mode metric variations. The solved p_psi
becomes the Hamiltonian, not a deleted field equation. Off-diagonal original
metric momenta are restored as p_hij=2*pi_ij; diagonal p_hii=pi_ii.

Let vcell=sqrt(det h), c=V^i*h_ij*V^j, s=psi_hat>0. The ORIGINAL full
twelve-velocity Legendre complement Rmat, affine ell and f give

~~~text
P_y=(2*p_h,p_V,p_cart)/vcell
s=-p_Z/(vcell*b*c)
E0=vcell*[(P_y-ell)^T Rmat^-1(P_y-ell)/2-f]
Edust=p_T*sqrt(C(tau)^2+h^zz*T'^2)
F=gamma*h^zi*p_Vi
H_perp=p_psi*s+E0+Edust+F'
p_psi=-(E0+Edust+F')/s
Hpsi=-<p_psi>=<(E0+Edust)/s-F*(1/s)'>.
~~~

The clock bracket is s, so N=1/s>0 follows after variation. E0 includes
the full potential, curvature, frame/acceleration, temporal force, cusp,
regulator, Cartesian and phase-alignment contributions. No specialized B1
matrix or target coefficient is substituted. The flux F' integrates to
zero without a weight, but F'/s generally does NOT. Omitting it changes
the reduced Hamiltonian and its future Hessian.

Formal pre-chart dimensions are consistent: S has mass degree4, I_z(S)
and metric/frame momenta degree3, E0/Edust degree4, s degree1 and Hpsi
density degree3. The dust and angular canonical pairs retain their own
degrees. Numerical reference recipes do not identify physical microscopic
scales, canonical K_Q or the unresolved matching V.

## Verification and what was not tested

Exact symbolic identities verify the metric constraint solution, finite
polar canonical map/charge, clock orientation, translation correction and
source degrees. The continuum positivity/gauge argument is displayed above.

All9 family/eta cases use the unchanged registered parameter maps on
n=17,25,33 odd periodic method grids. The method inputs have an analytic
positive-metric bound lambda_min(h)>=0.973 and |V^x|>=0.069, hence nonzero
tilt independently of sampled node absence. These are declared nodeless
controls, NOT the registered e*cos profile and NOT physical-domain evidence.
Rmat inversion in the controls is numerical; no uniform Rmat or Cauchy
theorem is inferred from these grids.

The controls compare restored fields/momenta with the ORIGINAL unreduced
lapse/diffeomorphism generators and canonical one-form. A separate80-digit
original mpmath density checks every coupled momentum and full Legendre
energy at one nontrivial point per case. Frozen normalized binary64
tolerance1e-8; the high-precision comparison does not make the underlying
binary64 grid a certified continuum evolution.

| Observed control over all27 grid cases | Bound |
| --- | --- |
| Largest original spatial-constraint residual, unnormalized | <1.468e-9 |
| Canonical one-form pullback discrepancy | <1.084e-19 |
| Original-density momenta/energy discrepancy | <1.954e-15 |
| Smallest nonzero mean source before translation correction | >1.033e-4 |
| Smallest absolute clock-weighted flux contribution | >3.552e-7 |
| Smallest absolute spatial-Ricci contribution | >0.3222 |

Omitting harmonics, the global constraint, lapse flux or curvature is
explicitly rejected by nonzero controls. Negative dust, changed charges,
zero tilt, reversed force clock, zero translation denominator and polar
origin tests require the appropriate rejection message. Exact profile-node
identities are checked separately, not asserted from a positive grid minimum.
Grid agreement is a diagnostic only. Most493 rows repeat controls across
cases/grids; they are not493 independent physical discoveries.

All493 local checks pass. Complete fresh eight-worker replay reproduces
three scientific JSONs and three sidecars with original bytes/sizes/mtimes.
All69 source pins/138 source-and-sidecar metadata records remain unchanged.
A separate174-record guard also preserves earlier successes and failed
attempt evidence. No failed source or scientific hash was rewritten.

| Artifact | SHA-256 |
| --- | --- |
| Frozen contract | b61365cab8e359cdb9d542510f5138405bee75394f4e8a3abf9bd182d2bb0b55 |
| V1 executable | f03a2b9ac794569994be8112b0ba1746b8e596669c2d693c9c7310bd48cab27b |
| Attempt01 summary.json | 15c8fe9411701187e047e6e1454116b4460708f7166821cc226eef6aa8727076 |
| formulas.json | e0f29f23f15714b7d254bdfee0e0d6c28784173e08f8caf9bc9cfac42deadf43 |
| independent.json | 3d175b86326214375c4839ace9f75c3a1ec71236f67b0be245f3b799646f81db |

Executable: Analysis/MasterTests/test_01_r4c1_planar_reduced_hamiltonian_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_planar_reduced_hamiltonian_attempt_01/.
Use existing itsm_env Python with --workers 16 and a NEW --output, or
--replay pointing to attempt01. Runtime journals remain private/ignored.

## Next dependency and scientific disposition

The next calculation must define the actual mixed-order/nodal domain and
linearize the complete constrained functional, including background drift
and coordinate-momentum mixing. Do not feed the registered nodes through
this regular inverse, replace them with a grid that misses them, smooth
the action, discard the negative direction or adopt the nodeless controls
as replacement states. A regular-patch mode calculation may inform the
domain, but cannot by itself establish a global T3 physical window.

The older G3K-C2 axis principal result is not rerun and remains valid in
its original scope. Memory search chunk chk_9af2c4550adff50555522b97 located
the older finite-k clock-domain report; live canonical sources, not that
retrieval record, govern this new derivation.

R9-MT1-PLANAR-REDUCED-HAMILTONIAN-V1: DEFERRED. Inherit FIXED-CHARGE-PATCH-
MOMENTUM-V2, finite-tilt canonical/backend and all transitive review debt.
Provisional reuse is limited to the displayed regular-planar functional.
Missing full characteristic/mode and interaction/frequency-window evidence,
rank-changing C2/weak initial admission/persistence, arbitrary3D closure,
nonlinear error control, healthy GR and identifying matching inputs remain
SUBSTANTIVE. Pending review alone does not block further bounded research.

Stage1 registered linear prepared-dust scope only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED;
TOP-X4 unchanged; physics_pass=false; gate_effect=NONE.
No state adoption/evolution, vault-management write, manuscript/PDF/site,
publication, commit/push, action/provider/model/global-runtime change.
