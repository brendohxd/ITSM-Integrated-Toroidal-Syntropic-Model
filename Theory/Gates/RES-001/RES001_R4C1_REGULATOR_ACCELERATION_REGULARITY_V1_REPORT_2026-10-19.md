# R4C1 regulator acceleration: a finite cusp limits higher smoothness

19 October 2026. Unchanged-action Stage2. Local200/200 checks; complete fresh
eight-worker replay exact, exit zero. This is a regularity result for the
registered initial profile class, NOT a physical-domain GO or an all-action no-go.

## What this adds

The [joint H/U/velocity construction](RES001_R4C1_JOINT_NODE_VELOCITY_V2_REPORT_2026-10-19.md)
still satisfies the three necessary conditions proved there. It is not
overwritten or rejected by this calculation.

The original action nevertheless forces a leading absolute-value cusp in the
regulator second-time acceleration near each simple profile node. For the
registered profiles and a regular coupled complement, its cusp-induced part is

    delta_A(Z_tt) = K0*|w| + O(|w|^3),
    K0 = A*(6*p*U+3*H0*p^2+2*beta*p^3)/b > 0.

The leading coefficient is enclosed as strictly positive in all nine tested
family/eta boxes. The exact two-sided limit, not a fitted power law, gives

    jump(partial_z Z_tt) = 2*K0*|partial_z w(node)|.

Thus a C3 spacetime extension of Z cannot be assumed for this registered
nonzero-amplitude analytic-profile class. The cusp component of Z_tt itself is
finite and continuous. This does NOT rule out C2/weak solutions, identify a
physical ghost, reject other initial data, or reject R4C1/ITSM. It does not prove
any of those weaker solutions exist either.

No additional C3 requirement is imposed on the programme. The result matters
where an argument actually assumes that higher smoothness. A physical Cauchy/
energy domain still needs its appropriate, explicitly justified function space.
No state is adopted or evolved; Stage2 INCOMPLETE; Stage3 NOT_ENTERED.

## 1. Original coupled block structure

Use the original twelve proper metric/frame/Cartesian velocities

    y=(Kxx,Kxy,Kxz,Kyy,Kyz,Kzz,Xx,Xy,Xz,u_hat,v_hat,r_hat)

and force/regulator velocities p=psi_hat, Z_hat. Work on the independently
varied future unit/dust branch and registered initial slice, not a pre-variation
normalization. The scalar/regulator temporal coefficient is -b*w^2, and

    L_y,Z_hat = 0,
    h = L_y,p,
    h_Kyy = -2*b*U*w^4, h_Xy = -b*U*w^3,

with all other h entries zero. These identities come from the complete original
first-jet density, including acceleration/regulator terms; they are not inferred
from a frozen-metric scalar operator.

Let R=L_y,y be the original complement Hessian. It is analytic in w and its
nodal determinant is

    det R(0) = -16*M_cosmo*D_T^5*(MU2*(c1+c4))^3,
    D_T = MP2-MU2*(c1+c3),
    M_cosmo = MP2+MU2*(c1+3*c2+c3)/2.

The actual nodal matrix is checked entry by entry before using its block
determinant. D_T, M_cosmo and MU2*(c1+c4) are positive in every registered case.
Consequently R^-1 exists and is bounded in a local neighbourhood of each node.
This is not a uniform full-profile, eta=0 or physical reduced-Hessian theorem.
In particular the negative determinant of this unreduced complement is NOT
used to declare a physical ghost.

There is no inversion of the singular psi/Z temporal block at w=0.

## 2. Scalar current and local dust density

For the original cusp L_cusp=-A*Y^(3/2), Y=hp^{mu nu}psi_mu psi_nu,
independent variation gives

    Epsi_cusp = 3*A*nabla_mu(sqrt(Y)*hp^{mu nu}psi_nu).

On the declared initial slice p>0, c=w^2 and the COMPLETE metric drift gives

    c_t=2*(H-H0)*c, c_z=2*w*wprime, (log sqrt(h))_t=3H.
    a_psi=-U-(3H-H0-q)*p+p*Rshift*wprime/w.

The last quotient is used only off the node and by its undivided regular limit.
Rshift is the odd analytic solution of the original coercive momentum problem.
At a simple node Rshift=0 and Rshift*wprime/w -> qnode. This is the same
necessary regulator limit used in the joint construction, not an evolution law.

Retaining volume drift, metric drift and shift flux yields exactly

    Epsi_cusp = 3*A*|w|^3*
       [-2*p*U-H0*p^2+p^2*(q-Rshift*wprime/w)].

Do not drop the h_dot contribution from c_t. The original cusp lapse energy
is -2*A*p^3*|w|^3. Its contribution to the LOCAL lapse-derived dust density is

    delta_A rho = +2*A*p^3*|w|^3.

The independently varied future-dust source is -beta*rho, so its cusp
contribution is -2*A*beta*p^3*|w|^3. Replacing local density by mean density
would omit the last term in K0.

## 3. Coupled response cannot cancel the leading term

The cusp has no complement-velocity dependence. Its original coordinate
metric/frame forces, converted to proper-velocity rows, have leading entries

    f_Kxx=f_Kzz=-A*p^3*|w|^3,
    f_Kyy=-4*A*p^3*|w|^3,
    f_Xy=-3*A*p^3*w*|w|,

with the other entries zero. The metric row factors follow from
K=(h_dot-L_shift h)/(2N); the full coordinate density independently checks
the complement normalization.

Isolate the cusp-induced acceleration by bookkeeping at FIXED initial jets,
rederiving the lapse density. This does not adopt an A=0 model or claim its
fixed jets solve its own mean constraint. The exact response has

    delta_A y_t = R^-1*f_cusp,
    delta_A Z_tt =
       [h^T*R^-1*f_cusp-Epsi_cusp+beta*delta_A rho]/(b*w^2).

The metric/frame response is retained, not prescribed to vanish. Since
h=O(w^3), f_cusp=O(|w|^2) and R^-1 is locally bounded, its contribution after
division by b*w^2 is O(|w|^3). It cannot cancel a term proportional to |w|.

Analytic reflection of the exact longitudinal shift gives
q-Rshift*wprime/w ->0. Dividing only off the node and taking the two-sided
limit therefore proves the K0 formula above. This is an exact local order/
limit argument, not a numerical remainder divided by a vanishing amplitude.

The non-cusp initial ingredients are analytic in the normal coordinate for
the declared profiles and regular complement. They cannot remove the
absolute-value corner. Full analytic acceleration profiles, global constraint
persistence and temporal error bounds have NOT been constructed here.

## 4. Nine outward coefficient enclosures

Keep the same families at eta=1/4,1/64,1/1024, k=40 and
continuous0<|e|<=1/500. U ranges over each certified joint box. The following
reference-chart K0 bounds are deliberately outward-coarsened:

| Family | eta=1/4 | eta=1/64 | eta=1/1024 |
|---|---:|---:|---:|
| archived G3 | [0.004060,0.004180] | [2.496e-6,2.573e-6] | [2.314e-9,2.385e-9] |
| new B1-frame | [0.003983,0.004100] | [2.493e-6,2.570e-6] | [2.313e-9,2.385e-9] |
| new hierarchical | [0.003976,0.004093] | [2.493e-6,2.570e-6] | [2.313e-9,2.385e-9] |

Every lower bound is positive. At a simple cosine-profile node
|partial_z w|=k*|e|, so the derivative jump is nonzero for each e!=0.
It tends to zero as e->0; no uniform stratum equivalence or GR theorem follows.

These are conditional diagnostic chart quantities involving assumed A,b,beta
and the registered background/data. They do not identify microscopic parameters,
an absolute physical scale, C_chi or a numerical observational acceleration.

## 5. Independent controls, replay and preservation

The full original four-coordinate density is independently polarized in all
twelve proper velocities at both amplitude signs. All144 complement entries
and12 scalar/complement mixings are retained. At mp.dps=110:

- Maximum normalized complement discrepancy <3.743e-111, tolerance1e-50.
- Maximum scalar/complement-mixing discrepancy <6.304e-108, tolerance1e-50.
- Original-coordinate current, lapse and dust variations retain metric/volume
  drift, both node orientations and both normal sides.
- Maximum coupled normalized limit error <9.903e-30 at |x|=1e-12 (tol1e-20),
  and <9.903e-42 at |x|=1e-18 (tol1e-30).

The local analytic time extensions in those current checks supply only the
required first jets; they are not an evolved metric/frame background. The
coupled response is separately solved using the full complement. The local
normal probes exercise the leading limit; they are not finite-x remainder
certificates, independent reviewers or an evolution theorem.

All200 local checks pass with zero failed/unknown checks. The final source/
contract bytes were frozen after AST preflight, before execution. Full replay
with eight rather than sixteen workers recomputes everything exactly, exit0.
All60 pinned inputs and120 source/sidecar metadata records, plus all8 original
output/sidecar bytes, sizes and mtimes remain unchanged. A separate external
140-record guard additionally preserves earlier joint-success/failure receipts
and prior independent controls. No old hash/result or failed attempt is edited.

    python -B Analysis/MasterTests/test_01_r4c1_regulator_acceleration_regularity_v1.py --replay Analysis/MasterTests/outputs/r4c1_regulator_acceleration_regularity_attempt_01 --workers 8

| Artifact | SHA-256 |
|---|---|
| Analysis/MasterTests/outputs/r4c1_regulator_acceleration_regularity_attempt_01/summary.json | 49ba1e1d77c4333015d4bfed7ec19d203b91644fbc433d9d2c08f05b749b0d99 |
| Analysis/MasterTests/outputs/r4c1_regulator_acceleration_regularity_attempt_01/formulas.json | c1324b1a5e1735f106a2207fb659c2a89b6940bbf861fefed9915672a3b217b8 |
| Analysis/MasterTests/outputs/r4c1_regulator_acceleration_regularity_attempt_01/certificates.json | c48f4051b6f5619a96577a7035492c2d9942c30e3c2fa15b82d480a5f6a3fc02 |
| Analysis/MasterTests/outputs/r4c1_regulator_acceleration_regularity_attempt_01/independent.json | 5193a77abfbcd575081ce85a079f873e78f0139920f9031493f02ae36289269d |
| Analysis/MasterTests/test_01_r4c1_regulator_acceleration_regularity_v1.py | d5c17a544394aa3d46b51ef467fe9d1ddfbc650bb07feb63d4467d0adc2b502a |
| Theory/Gates/RES-001/RES001_R4C1_REGULATOR_ACCELERATION_REGULARITY_V1_CONTRACT_2026-10-19.md | 59462dfb66d34db504ccf152addffcbbfbc8afa8ba58618f982bf8961ece2b06 |

## 6. Actual disposition and next route

The new result is a higher-regularity obstruction for this initial profile
class. It neither undoes the joint necessary root nor proves an admissible
C2/weak nonlinear solution. In particular no extra smoothness rule is used
to halt all research or manufacture a physical rejection.

Next determine the complete coupled acceleration/constraint system and the
actual lower-regularity Cauchy/energy domain. State the regularity needed by
that system, prove it or retain the obstruction, and establish persistence
and controlled nonlinear errors before any physical-window claim. Do not
replace the original cusp by a smooth regulator, choose a new parent action,
or continually project evolution onto the algebraic initial graph.

R9-MT1-REGULATOR-ACCELERATION-REGULARITY-V1 is DEFERRED, inheriting JOINT-NODE-
VELOCITY-V2, COUPLED-NODE-ACCELERATION-V4 and all transitive review dependencies.
Rule9_cleared=false. This same-author locally checked theorem is not review
clearance or a publication-ready physical conclusion.

Stage1 original bounded linear prepared-dust acceptance only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED; TOP-X4 unchanged;
physics_pass=false; gate_effect=NONE. Full initial admission/persistence, physical
Hessian/Cauchy/energy domain, nonlinear remainder/window, healthy GR and both
identifying matching inputs remain open. No state adoption/evolution, vault
mutation, manuscript/PDF/site edit, publication/submission, commit/push,
action/provider/model/global-runtime change is included.
