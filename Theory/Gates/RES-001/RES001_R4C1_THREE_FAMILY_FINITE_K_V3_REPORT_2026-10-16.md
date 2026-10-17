# R4C1: finite-k canonical/principal structure across three families

16 October 2026. Master Test1 / RES-001 / unchanged-action Stage2.
Conditional.602/602 local derivation checks; exact read-only replay passed.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Outcome and meaning

The three diagnostic continuations share the same kind of nonzero-mode
obstruction previously established for B1. All have positive time/kinetic
blocks and positive nonzero principal squared speeds on the declared domain,
but the declared wave-scale formulation has a defective zero-speed branch.
Their instantaneous dust-clock canonical energy also has a negative spatial
trace direction. Changing among these coefficient families does not remove
either of those features.

This is a completed bounded derivation, including adverse findings, not a
physical stability pass. It does not prove a propagating ghost, an all-action
no-go, or ill-posedness in every possible weighted mixed-order formulation.
The earlier CUSP3 finite-mode evolution result is unchanged: constraint
compatibility and controlled short-time numerical checks did not promise
positive energy or a physical interaction window.

## Scope and ensemble boundary

Start from the full generic22-field Hessian, not new coefficients inserted into
an already-specialized B1 matrix. The frozen V1 contract and V2/V3 compute
addenda in this folder own the task. Exact sign statements use0<eta<=1/4;
numerical points are eta=1/4,1/64,1/1024 in archived_G3, new_B1_frame and
new_hierarchical. These are diagnostic maps, not microscopic predictions.

Use the nonzero z-directed Fourier family k=(0,0,ell), ell>0,
p=ell/a; on the coordinate2*pi torus ell is an integer. Gauge/reduction:
T=0, alpha=-beta*Pi, nu=0, k_i*M_ij=0; solve S_i,Z only on the regular
nonzero-mode block. Retain all ten remaining complex coordinates and the
local complex phase. The exactly homogeneous chart is separate: the singular
1/ell auxiliary inverse is not extended to ell=0.

The earlier positive homogeneous fixed-both-charge kinetic block used its
declared ensemble/clock reduction. That result is not imported here as an
extra local fixed-density or fixed-dust-charge restriction. No branch is
deleted, no charge is reset, and no coefficients or old backgrounds are retuned.
This calculation does NOT supply a full fixed-global-charge energy theorem
for the finite-amplitude nonlinear forced state.

## Complete action and canonical map

With v=a^3 and dagger the Fourier adjoint, the export retains every value,
mixed and velocity entry:

```text
L2/v = y^dagger*A*y/2 + Re(y_dot^dagger*R*y) + y_dot^dagger*K*y_dot/2
p_y  = v*(K*y_dot+R*y)
HH_yy = v*(R^dagger*K^-1*R-A)
HH_yp = -R^dagger*K^-1
HH_pp = K^-1/v.
```

The SO(2) order is h=(Mxx+Myy)/sqrt(2), TT+=(Mxx-Myy)/sqrt(2),
TTx=Mxy, Vlong=Vz, Vtrans1=Vx, Vtrans2=Vy, du,dv,dr,Pi.
Define M=MP2, Tm=MP2-MU2*(c1+c3),
Mc=MP2+MU2*(c1+3*c2+c3)/2, cL=MU2*(c1+c2+c3),
f2=MU2*(c1+c4), and Kh=Tm*Mc/(2*cL). Then

```text
K = diag(Kh,Tm/4,Tm/2,f2,f2,f2,1,1,1,K_Q).
```

Here K_Q denotes the declared diagnostic coefficient, not a new derivation of
canonical MAT-001 matching. Exact Bernstein certificates prove the required
family signs on the registered open eta interval, including eta=1/4.
eta=0 remains excluded; positivity at eta>0 proves no uniform endpoint control.

The unreduced momentum pulls back to the displayed p_y, with vanishing
auxiliary-momentum contributions. Fixed T,nu coordinates need not have zero
momenta: their coordinate variations vanish. The evolving canonical identity
J*HH*Mmap-Mmap*G-Mmap_dot=0 retains coefficient and volume drift. Omitting
that drift gives a normalized witness as large as0.45719191677847293.

## Principal modes and exact defective branch

The independently derived generic real-space ADM/frame/regulator density
agrees with the full-kernel principal scalar blocks. Its regulator equation
Z=-(Delta Pi+psi_dot*div V) gives the retained negative action square
-b*abs(Delta Pi+psi_dot*div V)^2/2. Dropping its quartic term fails a nonzero
rejection control.

The eight ordinary wave branches have squared coefficients:

- TT metric: cT2=M/Tm, multiplicity2.
- Transverse frame: cV2=(2*M*c1-MU2*c1^2+MU2*c3^2)/
  [2*(c1+c4)*Tm], multiplicity2.
- Complex radial and real reservoir:1, multiplicity2.
- Complex phase:1+zeta*(u0^2+v0^2), multiplicity1.
- Coupled scalar wave: cS2=M*(2*M-f2)/(4*Kh*f2), multiplicity1.

There is also one dispersive branch omega^2~(b/K_Q)*p^4, with
b/K_Q=5/33 in all three maps, and one zero-speed/slow branch. Positivity of
these nonzero coefficients proves neither causality nor a physical EFT window.

For c=omega/p, the leading p^22 determinant is

```text
-det(K)*(b/K_Q)*c^2*(c^2-cT2)^2*(c^2-cV2)^2
              *(c^2-1)^2*(c^2-cPhase2)*(c^2-cS2).
```

For sigma=omega/p^2, the leading p^40 determinant is
det(K)*sigma^18*(sigma^2-b/K_Q). Its zero factors represent slower branches,
not extra modes. Full factors, multiplicities and normalization are retained.

The scalar wave companion, on states(h,Vlong,c*h,c*Vlong), is

```text
C = [[0,0,1,0], [0,0,0,1],
     [-M/(4*Kh),0,0,M/(sqrt(2)*Kh)],
     [0,0,M/(sqrt(2)*f2),0]].
e0=(0,1,0,0), e1=(2*sqrt(2),0,0,1)
C*e0=0, C*e1=e0.
```

Its characteristic polynomial is lambda^2*(lambda^2-cS2). A zero column and
an explicit nonzero3x3 minor -M/(4*Kh) prove rank3 on the regular domain.
Thus the zero root has algebraic multiplicity2 but only one eigenvector.
Every registered family inherits this defect. Real roots alone do not supply
a complete wave-scale basis. The mixed second-time/fourth-spatial-order system
still requires its own action/constraint-compatible weighted estimate; no
general all-formulations ill-posedness theorem is asserted here.

## Energy sign, not a ghost declaration

Completing the positive momentum square does not make HH positive. The
leading zero-velocity trace energy is

```text
H_trace = -a^3*M*p^2*abs(h)^2/8.
```

An explicit zero-velocity canonical state has p_y=v*R*y, not p_y=0.
All216 frozen full-action probes retain negative energy on this trace
direction; the values range from-2098.5609155709963 to-1.9999999999999996
in the registered basis/units. These sizes are not measured physical scales.

The frozen principal scalar elimination also has coefficient
f2-2*M=eta/6-2<0. This is ONLY the frozen principal coefficient. V3 does not
derive the complete evolving slow action for the new families, and does not
replace or modify the older B1 evolving coefficient -11/6. A singular
asymptotic elimination and a time-dependent clock/canonical generator must not
be mistaken for a finite-k invertible canonical restriction or a local ghost
proof. The role of these signs in a genuinely justified physical domain is
still substantive work.

## Numerical and reproducibility controls

Use all378 unchanged leading-background nodes from18 CUSP3 histories (two
previously integrated methods, three families and three eta values). No new
time integrations were performed in this task. Canonical/action/one-form checks
use ell=80 at every node. Full frozen canonical spectra and zero-velocity
energy checks use ell=4,40,80,128 at nodes0,10,20:216 diagnostics, not an
evolved-stability certificate or continuous-time error bound.

| Normalized control | Maximum | Acceptance |
| --- | ---: | ---: |
| Symbolic/numeric full action binding | 7.342883571142847e-16 | 1e-9 |
| Evolving Hamilton/Euler identity | 2.782816691520363e-13 | 1e-9 |
| Canonical momentum one-form | 1.9826180014273941e-16 | 1e-9 |
| Auxiliary constraints/inverse | 8.881784197001252e-16 | 1e-9 |
| Full frozen eigenpairs | 5.980752096227136e-15 | 1e-9 |

The smallest sampled kinetic eigenvalue is0.000162760416666667. Ordinary
eigenvalue magnitudes are basis-dependent; the exact diagonal/sign identities
are the sign evidence. No physical cutoff is inferred.602 controls include
many repeated point/grid checks, not602 independent physical discoveries or
independent Rule9 reviewers.

Executable: `Analysis/MasterTests/test_01_r4c1_three_family_finite_k_v3.py`.
Receipts: `Analysis/MasterTests/outputs/r4c1_three_family_finite_k_attempt_04/`.

| Artifact | SHA-256 |
| --- | --- |
| V3 executable | 4b9158ebef8f11b0a5166ccfacbe946bc364cfbab36514624f0ea4a9455de55d |
| Summary | f94d85d36539097867490f0ce84a656267a56ec61acc170d55a873f2a69a614f |
| Formulas | de72acd9c46919652db15fac0de15c47044af7e210b2160631d196f15da3a22f |
| Numerics | 7ce3d9031412ce986d831448a32ac6c40ea4f8fb00ba37a0202acf92dbc2904c |
| Verification | 2405a627e84b8f131260b91b18c627b9dbb9d3e3594adc1c36b61066989cd6d4 |
| Scope | 0a5ced8bb5d838ac89c59d62d3c51569e50b17d620047bf1d0a0607ecb445347 |

Exact read-only replay reproduced all artifact/sidecar bytes and preserved
output metadata.381 source pins and759 source/sidecar hash-size-mtime records
were preserved, with three historical absent sidecars still explicitly
unverified. No old scientific file, sidecar or result was rewritten.

Attempts01/02 (V1) and03 (V2) remain interrupted, with no mathematical pass.
Attempt02 returned Windows0xC0000005 during an unchanged-source diagnostic
retry; its native cause is unassigned. The private trace/log remains local.
V3 binds compact coefficients exactly to the same generic action and proves
characteristic factors before substituting primitive couplings, avoiding the
large expansion. Numeric/action/sign-certificate functions have identical ASTs
across V1/V2/V3; thresholds and physical inputs did not change. The addenda
retain the distinction between algebra representation and physical equations.

Reproduce with itsm_env Python and `--replay` pointing to attempt04. No runtime,
security, library, provider or model configuration was changed.

## Decision and next meaningful question

R9-MT1-THREE-FAMILY-FINITE-K-V3: review DEFERRED, not cleared. Inherit CUSP3
evolution V1, homogeneous fixed-charge kinetic V3, B1 nonzero characteristic,
generic kernel/evolving reduction and all transitive debt. Retrieval packet
ctx_aeb6e4fb11881d09cc7da893 located prior kinetic evidence
doc_8c3e84738ae6c13527bdf731; live source hashes, not memory labels, govern.

The scoped derivation is complete; physical stability remains unresolved.
The Jordan defect and retained energy signs are substantive findings, not
review-only holds. A useful next bounded route is an action-preserving weighted
mixed-order estimate for the coupled slow/dispersive system, then a physical
interaction-window assessment. Do not automatically alter the action, delete
the dust branch, adopt the homogeneous ensemble locally, or pivot to TOP-X4.

No family receives physical GO. Stage2 INCOMPLETE; Stage3 NOT_ENTERED;
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Full nonlinear/fixed-charge admission and remainder, healthy GR/local gravity,
causality/window and genuine matter-residue/nonlinear-force matching remain.
Native goal remains paused. No publication, manuscript/PDF, website, vault
mutation, commit or push. Living queue/review-register checkpoint is append-only
with original bytes/digests retained privately.
