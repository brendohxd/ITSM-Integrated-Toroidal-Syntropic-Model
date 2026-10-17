# R4C1: local constraints at the first omitted cusp order

16 October 2026. Master Test1 / RES-001 / unchanged-action Stage2.
Claim Conditional. Local validation693/693; exact read-only replay passed.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result and meaning

The previous INITIAL-CHARGE-COMPLETION V4 counter is compatible with all seven
local Cauchy/auxiliary rows at the INITIAL directional order |e|^3. The proof
treats the mean separately and holds for arbitrary nonzero periodic harmonic.
It does not discard the nonconstant density or the infinite source harmonics.

At the registered numerical probes, the resulting initial data also admit a
jet satisfying all22 linear sourced equations and differentiated auxiliary
constraints. A separate unreduced linear solve agrees. This extends the prior
mean-charge compatibility result to local initial consistency at this order.

The necessary completion is not just the direct cusp force: the lower-order
e|e| frame response has zero initial displacement/velocity but NONZERO initial
acceleration. Its coupling through the action-derived WWR sources is required
for the temporal and spatial source Ward identities. Dropping it fails those
identities by explicit nonzero terms.

No all-orders constraint solution, finite-time evolution, full infinite-mode
acceleration bound, physical energy positivity, propagating stability, physical
frequency window, cutoff or healthy GR limit follows. No family receives GO.

## Calculation from the unchanged action

Inputs are the generic22-field kernel, generic pre-shift WWR Euler export,
G3N4 nonanalytic source export, complete family maps, previous accepted charge
report/receipts and18 immutable retarded initial events. The latter represent
nine distinct family/eta points with two archived method labels; this task
does not perform two new time integrations or independent experiments.

The first wave has W=cos(kz),W_t=0,k=40. Set f=|cos(kz)|^3 and pd=psi_dot>0.
With f2=MU2*(c1+c4), the initially zero lower cusp response has

```text
W_cusp,tt = D*cos(kz)*|cos(kz)|,
D = -3*A*pd^3/f2,
B_cusp,tt = sigma*W_cusp,tt,
sigma = -MU2*(c1+c3)/(MP2-MU2*(c1+c3)).
```

These are coefficients of e|e|, not new finite initial displacements.
Polarizing the GENERIC quadratic WWR source with this acceleration adds the
following |e|^3 source coefficients, each multiplying f:

| Row | Additional coefficient |
| --- | --- |
| Mxx and Mzz | -3*A*c2*pd^3/[2*(c1+c4)] |
| Myy | 3*A*pd^3*(c1-c2-c3+2*c4)/[2*(c1+c4)] |
| nu | -3*A*pd^3*(c2+c3)/(c1+c4) |

The other mixed source VALUES vanish at this initial event, not for arbitrary
later times. The auxiliary-source TIME DERIVATIVES do not all vanish:

```text
d_t S_Sz = A*pd^3*(c1+3*c2+c4)/(a*(c1+c4)) * d_z f,
d_t S_Z  = -3*A*b*pd^4/[MU2*(c1+c4)] * f,
d_t S_Sx = d_t S_Sy = 0.
```

The direct force supplies S_alpha=2*A*pd^3*f, S_Mxx=S_Mzz=-A*pd^3*f/2,
S_Myy=-2*A*pd^3*f and the force-current derivative in the Pi row. Their
binding, the mixed coefficients, and the source drift are checked exactly
before family substitution. No specialized B1 operator was transplanted.

Complete temporal and longitudinal source Ward residuals vanish exactly.
If the mixed acceleration/drift terms are omitted, the respective residuals
are -3*H*A*pd^3*f and -A*pd^3*d_z f. These are rejection witnesses, not a
failure of the completed action-derived source or a theory no-go.

## Pointwise initial constraints and spectral treatment

The seven rows are alpha,Sx,Sy,Sz,Em,Z,LambdaU. Their primary derivative
structure is checked from the generic kernel rather than assumed. The
previous necessary mean counter and density are retained:

```text
xdot3 = -4*A*pd^3/(3*pi*M_cos2*H),
epsilon3(z) = 2*A*pd^3/C^4 * (f-4/(3*pi)).
```

They multiply |e|^3. The new phase-velocity coefficient at this order is0;
other new free initial positions/velocities are0. Mean diagonal metric
velocities equal2*xdot3/3. The local density is not set to0. This is a NEW
coefficient response; old preparations and reconstructed shifts are untouched.

The exact source coefficients for exp(2*i*m*k*z) are

```text
h_m = 12*(-1)^m / [pi*(4*m^2-1)*(4*m^2-9)],  m integer,
h_0 = 4/(3*pi).
```

Product-to-sum gives this expression without fitting. Cosine-node limits
retain the C2 |cos|^3 profile; no analytic cubic Taylor vertex at Y=0 is
inserted. The seven constraint identities hold for m=0 and arbitrary
nonzero harmonic. Finite numerical probes of the full equation jet use
m=0,1,2,4,8,16; they are not a truncation-based proof for all accelerations.

## Numerical controls and immutable provenance

All three families; eta=1/4,1/64,1/1024; both archived initial events per point;
six probe harmonics:108 full22-equation initial jets. The evolving reduction
retains operator/background drift, multiplier and density continuity. The
independent control solves the original22 equations plus differentiated
auxiliary constraints, without the Schur-reduced acceleration matrix.

| Control | Observed maximum |
| --- | ---: |
| Full22-equation normalized residual | 1.6070226845e-16 |
| Differentiated auxiliary-constraint residual | 1.0493429050e-16 |
| Independent unreduced linear-solve residual | 3.2709087814e-17 |
| Independent/reference jet comparison | 9.8101863831e-15 |
| Reduced kinetic matrix condition number, reference basis | 1.1322316913e8 |

Independent80-digit full-period quadrature confirms the six Fourier controls.
The high-precision solve operates on the exported FLOATING matrix, not on
80-digit physical coefficients. Its Hermitian normal equations square the
condition number; all original equation residuals are still checked. These
are algorithmic controls, not certified numerical/evolution error bounds.
The condition number is basis-dependent and not a physical cutoff.

V1 stopped before a complete receipt because the installed mpmath1.3.0
Householder QR routine mishandled a zero-diagonal full-rank comparison matrix.
Its first23-by18 matrix independently had rank18, singular values0.04167 to
1.98747. A simple full-rank3-by2 example reproduced the QR failure. V2 uses
an80-digit Hermitian-normal-equation LU control, with separate real/complex
zero-diagonal witnesses. No physical source, tolerance or old datum changed.
V1, its sidecar and incomplete attempt01 record remain preserved.

V2/attempt02 passes693/693 local controls, including repeated probe checks,
and exact read-only replay. It verifies358 source pins and preserves713
source/sidecar hash-size-mtime records; three historical absent sidecars
remain explicitly inherited, not newly verified.

Executable: `Analysis/MasterTests/test_01_r4c1_cusp3_local_initial_jet_v2.py`.
Receipts: `Analysis/MasterTests/outputs/r4c1_cusp3_local_initial_jet_attempt_02/`.

| Artifact | SHA-256 |
| --- | --- |
| V2 executable | 978a08558d741c6cdfcb80504036be922f4984c06b0510bed8240f1039621869 |
| summary.json | e3b7146960b8ce2d46eed1178204902659625bb06ef6c41763fea5ecbe2e82a1 |
| formulas.json | 27816da0a3815949d14d4fb8c645b02856d2646eb1cfd5b32aad48e60dacd267 |
| initial_jets.json | 7784a56d445bfe1dcd66465f8238d44075abc3b6a66f2d9455d5c465472b1df2 |
| verification.json | 8d310f8dd62b9ec02b01da68676b994203acf9129086a470936c0942c30baa9e |

## Disposition and next boundary

R9-MT1-CUSP3-LOCAL-INITIAL-JET-V1: review DEFERRED, not cleared. Inherit
INITIAL-CHARGE-COMPLETION V4, homogeneous kinetic V3, fixed-charge retarded V3,
charge/domain V5, G3N4 force coverage, generic WWR/evolving reduction and all
transitive debt. Memory packet ctx_dcb93220d01aac5977bf6f69 supplied continuity;
live accepted files/hashes govern, not an older memory search hit.

Substantive blockers NONE_WITHIN_STATED_SCOPE for this INITIAL |e|^3 result,
given exact action-source/constraint identities, independent controls and
replay. Provisional reuse is limited to that scope. Full nonlinear admission,
all-order initial remainder and the unsummed infinite-mode acceleration norm
remain OPEN. The qdd arrays fix the derivatives entering these equations;
unused higher derivatives of auxiliary variables are not an evolved solution.

Next substantive question: extend the completed source/constraint treatment
to unprojected evolution in its registered domain, with suitable harmonic
and error control. Do not repeat the initial mean sign/charge checks or
promote the result to a physical stability window. Finite-k energy and all
characteristics/quartic dispersion, physical interactions, tensor/local
gravity/healthy GR and genuine matching remain required. The earlier retarded
timing warning remains unchanged.

Stage1 complete only registered linear B1 scope; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 UNCHANGED; physics_pass=false; gate_effect=NONE; Rule9_cleared=false.
The paused native goal state was not changed. No manuscript/PDF, publication,
commit/push, vault, model/provider/runtime or security configuration changes.
