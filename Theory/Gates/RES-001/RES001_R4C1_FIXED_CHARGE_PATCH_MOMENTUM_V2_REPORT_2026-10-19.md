# R4C1: opposite momentum signs survive a constrained fixed-charge patch test

19 October 2026. Unchanged-action Stage 2 / Master Test 1.
Conditional, local validation104/104; complete fresh eight-worker replay exact.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## What the result means

Fixing both global charges does NOT make the instantaneous momentum form
positive on every finite-tilt, inhomogeneous constraint-surface direction.
On regular patches of all nine registered cases, a radial-matter momentum
direction is positive while a regulator/metric-compensated direction is
negative. The actual lapse and spatial constraints and their metric response
are included. This is more specific than an unreduced scalar matrix sign.

It is NOT yet a physical ghost diagnosis, a below-cutoff instability or an
all-action no-go. This test does not supply the complete physical mode
equations, frequency/window or lower-regularity Cauchy theorem. An
instantaneous Hessian on a time-dependent constrained chart is not by itself
a conserved energy or a complete dynamical stability criterion.

The earlier homogeneous aligned fixed-both positive result remains intact:
that is a different domain with a different regulator rank. The joint
H/U/Ud root and finite regulator-acceleration cusp results also remain intact.
No initial state was adopted/evolved and no equation/action was changed.

## Scope and reduction, including clock orientation

Use the three registered diagnostic families at eta=1/4,1/64,1/1024, k=40,
continuous0<|e|<=1/500 and the existing joint-root H/U boxes. These maps are
not microscopic matching predictions. All quantities below use the existing
reference chart/units; no physical scale or canonical K_Q is identified.

On the initial slice h=I, psi_i=T_i=0, psi=0, u=Rc, v=0, retain the full
twelve-velocity complement y=(six K,three X,u_hat,v_hat,r_hat). The
original-action canonical equations give, with c=w^2 and s=psi_hat,

~~~text
L0 = y^T R y/2 + ell(s)^T y + f(s) - b*c*s*Z_hat
ell(s)=ell0+s*h
h_Kyy=-2*b*U*w^4, h_Xy=-b*U*w^3; other entries zero
p_Z=-b*c*s
E0=(P-ell)^T R^-1(P-ell)/2-f(s)
H_perp=p_psi*s+E0+p_T+J, J=partial_i(gamma*p_V^i).
~~~

The potential, curvature, Cartesian/phase, frame, regulator and cusp terms
have not been removed from E0. R comes from the unspecialized action, not a
B1-specialized kernel. Auxiliary reductions follow their own variations.

Choose psi=tau AFTER canonical variation. The clock bracket is s>0,
so N=1/s. It is not a simultaneous dust-time gauge. Solving the lapse
constraint and pulling back the action gives

~~~text
p_psi=-(E0+p_T+J)/s
H_psi=-p_psi=+(E0+p_T+J)/s.
~~~

The plus sign follows from the canonical action; reversing time flips all
Hessian signs and does not make an indefinite form definite.

For planar perturbations at h=I, the NONZERO-mode spatial gauge matrix for
(h_xz,h_yz,h_zz) is diag(partial_z,partial_z,2partial_z). The translation
kernel and physical mean metric pairs are retained, not inverted/deleted.
An odd reflected pair of compact supports below has int F=0 and hence
zero mean delta pi_zz. On this gauge section the solved nonzero-mode
pi_iz and p_psi drop from the canonical one-form; p_Z dZ and p_u du remain.
This is a pullback of the known constraint surface, NOT a new proof of the
complete arbitrary3D Dirac algebra or absence of further admissibility
conditions on the full Cauchy problem.

## Exactly fixed charges and metric compensation

Take smooth F supported strictly inside pi/6<theta<pi/3, theta=k*z, plus
its odd reflection. Hold configurations, p_V, p_v and p_T fixed, and set

~~~text
delta p_Z=F'/Z_z, delta pi_zz=F/2
delta C_z=-2partial_z(delta pi_zz)+delta p_Z*Z_z=0.
~~~

The other spatial rows vanish on this variation. The true lapse equation
solves p_psi, not p_T. Thus Q_dust=int p_T and
Q_U1=int(u*p_v-v*p_u) stay fixed EXACTLY. A separate radial delta p_u=chi
also preserves these constraints/charges; chi may have zero mean.
No mean dust-energy compensation or charge change is smuggled into the test.
The lapse flux J is retained and unchanged under these variations, not
deleted generally. Its contribution J/s participates in the differentiation.

The supports avoid c=0 and Z_z=0. Sufficiently small momentum amplitudes keep
p_Z<0 and s>0, leaving the original positive dust density unchanged. The
allowed perturbation neighborhood need not be uniform as e or eta approaches
zero. No force/regulator inverse is applied at any node.

## Full coupled curvature and a controlled patch inequality

Differentiate H_psi at fixed configurations/momenta first, then use the
LOCAL lapse constraint on the background. The exact result is

~~~text
B=-H_psi,ss
 =[K_Q*(1+c)-h^T R^-1 h]/p-6*A*abs(w)^3-2*b*c*Z_hat/p^2,
Z_hat=Ud*w^2-Rshift*Z_z.
~~~

Ud is the jointly adjusted coefficient, NOT U_dot. The full shift drift
and coupled inverse term remain. A nonzero off-shell lapse witness verifies
that this on-shell formula cannot be used as an off-shell identity.

R regularity is certified over the full signed amplitude interval by
||R0^-1(R-R0)||_infinity<1, with exact R0^-1. The Neumann bound supplies
N_R>=||R^-1||_infinity; no sampled determinant substitutes for this proof.
The existing shift inverse/error bounds and joint boxes enclose Ud and
Rshift, so B includes their uncertainties continuously in amplitude.

For delta P_zz=F and delta s=-F'/(b*c*Z_z), the negative of the restricted
quadratic form is

~~~text
-Q_F=integral[-(Rinv)_zzzz*F^2/p
             +2*[Rinv(P-ell0)]_zz*F*delta_s/p^2+B*delta_s^2].
~~~

Let Y bound the absolute mixed velocity, U in [Ul,Uu], a=e^2, and B>=Bmin.
On the chosen patch c in [a/4,3a/4] and
sqrt(3)*Ul*k*a/2<=|Z_z|<=Uu*k*a. Young's inequality bounds -Q_F below by
B0*||F'||^2/2-(A0+D0^2/(2B0))*||F||^2 with

~~~text
A0=N_R/p
D0=16*Y/(sqrt(3)*p^2*b*Ul*k*a^2)
B0=16*Bmin/(9*b^2*Uu^2*k^2*a^4).
~~~

Consequently -Q_F>0 if the ratio ||F'||^2/||F||^2 exceeds

~~~text
a^4*[9*N_R*b^2*Uu^2*k^2/(8*p*Bmin)
     +27*b^2*Y^2*Uu^4*k^2/(p^4*Ul^2*Bmin^2)].
~~~

The patch Poincare bound is 36*k^2. It exceeds this sufficient threshold
in EVERY case. The alpha factors are retained before taking e->0; this
does not assert a regular inverse at e=0.

Independently Q_u=int chi^2/p>0 and its mixed F/chi term vanishes at the
registered u_hat=0, v=0 slice. Thus the form has both signs after the stated
charge/constraint pullback. This construction does not require continual
projection of dynamics onto a slow graph or an inserted target coefficient.

## Numerical controls and preservation

All bounds below are conservative reference-chart values, not physical
frequencies, a measured acceleration scale or EFT cutoff.

| Control across all nine cases | Certified/observed bound |
| --- | --- |
| Neumann relative norm | <0.006005 |
| B lower bound | >14.99999990 |
| Young ratio threshold, all amplitudes | <2.868e-20 |
| Patch Poincare bound | 57600 |
| Original-coordinate R/affine/momenta/energy error | <3.743e-111 |
| Independent clock-Hessian error | <4.429e-102 |

The independent110-digit calculation polarizes the ORIGINAL four-coordinate
density with nonzero shift and spatial gradients, checks all144 R entries,
affine terms, momenta and full Legendre energy, and differentiates the clock
Hamiltonian at both tilt signs for each family/eta. Frozen normalized
tolerance1e-45. Its local dust source is derived with a nonzero lapse-flux
control. Those approximate first-jet controls are not newly admitted global
backgrounds and do not replace the outward interval certificates.

V1 stopped with an interval-input type exception before scientific receipts:
an exact integer reached a helper expecting _mpi_. Preserve its source,
sidecar, empty attempt01 and private traceback. V2 changes only maxupper's
input conversion and source pins; function-AST comparison confirms all other
functions are identical. An integer/interval smoke test passes. Equations,
precision, thresholds, ensembles and rejection tests did not change.

V2 completed104/104. A complete fresh eight-worker READ_ONLY replay returns
the same four payloads and four sidecars with sizes/mtimes unchanged.
All66 source pins/132 source-and-sidecar metadata records are unchanged.
An independent162-record guard additionally preserves earlier successes,
failed-attempt evidence and this new receipt set. No original hash or
executed source was refreshed to obtain a pass.

| Artifact | SHA-256 |
| --- | --- |
| V1 executable, preserved failure | e8e8837e6c70b6f8cb8db2a1daefca0054b2da9e95a0aaf189edf348e6b6c661 |
| V1 contract | 0f10ec33f71edfc11965286a08a96feb317b00e813716cbfae246856826baf09 |
| V2 type addendum | 90ab0c2ffa684c459af1a66c14e95e02e7c7805481eae2d7e34c2019c31d1d5e |
| V2 executable | 2706b05764eea2b9a34dc7be73f78022933a8c444e54f5c8b47b8ceb33fce74f |
| Attempt02 summary.json | 00a202fddd684b785c9ac5134af1b0b84538aeef413389f30c93901b70e06c37 |
| formulas.json | cb7dd16a7ce0aaf8b127790859cca324b3f2527a0886eb988889e18edcdc958a |
| certificates.json | 789cf864c5f78b799b8ff30d70d8fdc8883a2ba140a9cb0b6abb8c60d6490742 |
| independent.json | 1fb6dc643527450019933a959be926c6ec9f973d9cd7fcc6b664e0053f1194df |

Executable: Analysis/MasterTests/test_01_r4c1_fixed_charge_patch_momentum_v2.py.
Receipts: Analysis/MasterTests/outputs/r4c1_fixed_charge_patch_momentum_attempt_02/.
Use the existing itsm_env Python, --workers 16, a NEW --output directory, or
--replay pointing to attempt02. Runtime logs are ignored private artifacts.

## What must happen next

Determine the complete coupled characteristic/mode equations and the
admissible frequency/interaction domain. In particular test whether the
negative direction survives as a propagating excitation BELOW a justified
cutoff, or lies outside a controlled low-frequency effective description.
Do not use a potential parameter or a vacuum probe threshold as that cutoff.
No projection/removal of the offending direction or parent/action switch is
authorized by this report. Address node/rank-changing C2/weak persistence
and arbitrary3D constraints rather than quietly excluding them.

R9-MT1-FIXED-CHARGE-PATCH-MOMENTUM-V2: DEFERRED, not cleared. Inherit
REGULATOR-ACCELERATION-REGULARITY-V1, JOINT-NODE-VELOCITY-V2,
FINITE-TILT-CANONICAL-V2, THREE-FAMILY-FIXED-CHARGE-KINETIC-V3 and transitive
review debt. Provisional reuse is limited to this instantaneous planar-patch
form. Remaining substantive blockers are physical-mode/characteristic and
frequency/window identification, complete initial/Cauchy admission,
coordinate-momentum mixing/evolution/error bounds, healthy GR recovery and
both identifying matching inputs. Pending review alone is not the blocker.

Stage1 complete only in its registered linear prepared-dust scope; Stage2
INCOMPLETE; Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED;
TOP-X4 unchanged. No vault/manuscript/PDF/site, publication, commit/push,
provider/model/global-runtime change or new paid session.

Method reference only: [Husain and Pawlowski, arXiv:1108.1145](https://arxiv.org/abs/1108.1145)
illustrates imposing an irrotational-dust clock after canonical variation.
It is a different action/clock from the force-clock calculation above and
is not evidence for this ITSM sign result; the displayed reduction is
derived from the frozen original ITSM density and constraints.
