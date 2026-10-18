# R4C1 node acceleration: selected regulator continuation is incompatible

18 October 2026. Unchanged-action Stage 2. V2 passes 48/48 local checks;
complete fresh read-only replay is exact, exit zero. The result is a bounded
incompatibility of the selected initial continuation, not physical clearance.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Finding and relation to the previous certificate

For all nine registered family/eta cases and every nonzero amplitude
`0<|e|<=1/500`, the selected continuation `Z=U0*w^2`, `Z_dot=Ud0*w^2` fails a
necessary scalar-acceleration compatibility condition at each simple profile
node. The conclusion assumes finite continuous force-scalar normal acceleration
and finite regulator/metric/frame jets in the declared initial sector. It does
not exclude a weak/distributional formulation or other initial continuations.

The [known initial-surface certificate](RES001_R4C1_INITIAL_ADMISSION_V1_REPORT_2026-10-18.md)
remains unchanged and true within its stated scope. It certified known initial
constraints, both charges and positive local dust; it explicitly left higher
and acceleration consistency, full admission and evolution open. This result
resolves one of those missing requirements negatively for that particular
higher-order regulator choice. It does not invalidate the certified constraint
surface, alter an archived preparation, or prove an all-action no-go theorem.

## 1. Both scalar equations come from the original density

Write `K=K_Q`, `p` for the proper force-scalar velocity, `hp=g^{-1}+n*n`,
`Q=n.grad psi`, `Y=grad psi.hp.grad psi`, and `acc=n.nabla n`. The original
force/regulator density is

    L = K Q^2/2 - A Y^(3/2) + b Z^2/2
        - b grad Z.hp.grad psi - b Z acc.grad psi.

Its force momentum is

    Ppsi = K Q n - 3A sqrt(Y) hp.grad psi - b hp.grad Z - b Z acc.

Vary the conformally coupled dust independently before imposing its own
multiplier equation. Its force-scalar source is `-beta*epsilon*C^4`, reducing
to `-beta*rho` on this `C=1` slice. The frame, metric, Cartesian and potential
terms have no direct psi variation. Their effects are not frozen away: the
normalized frame, acceleration, covariant divergence and constrained geometry
remain in the scalar equations and in the mean/local matter equations.

Use the parent's exact initial slice, `w=e*cos(kz)`, `k=40`, `V_dot_y=-Hbg*w`,
uniform `p`, prospective mean expansion `H`, and longitudinal shift `R=Sz`.
The unreduced regulator equation becomes

    EZ/b = Z + w^2 [a_psi+(3H-Hbg-R')p] - R*w*w'*p,

where `a_psi` is the force-scalar normal acceleration. This follows from the
original Euler variation, not an assumed self-adjoint spatial operator. The
acceleration term in the density is essential to the result.

At a simple node use a local coordinate `zeta_node`, `w=s*zeta_node+o(zeta_node)`,
`R=r1*zeta_node+o(zeta_node)` and `Z/w^2 -> U`. The inherited odd shift sector
gives `R=0` at the node. Taking the regular-side limit, without dividing at the
node itself, requires

    a_psi = -U-(3H-Hbg)p+2*r1*p.

Independently the force-scalar equation evaluated at the node is

    Epsi_node = -K [a_psi+(3H-r1)p] + 2b U s^2 - beta*rho_node = 0.

It retains the shift gradient and the regulator spatial Hessian
`Z_zz=2U*s^2`. The original C2 cusp has zero divergence in both one-sided node
limits; no ordinary third cusp derivative is introduced. Simultaneous finite
continuous acceleration therefore requires

    G = (K+2b*s^2)U - K*Hbg*p - K*p*r1 - beta*rho_node = 0.       (1)

Dimensions in the frozen dimensionless-psi chart are `[K]=2`, `[b]=[beta]=0`,
`[Hbg]=[p]=[s]=[r1]=1`, `[U]=2`, `[rho]=4`; every term of (1) has mass
dimension four. The frame amplitude `e` is dimensionless. No physical constant
or matching coefficient is newly determined by this calculation.

## 2. Test the selected continuation without subtracting through zero

The parent selected

    U0=Hbg*p+beta*rho0/K,  rho0=1/5,  s^2=k^2*e^2.

It kept the action-derived quadratic regulator coefficients as a DECLARED
higher-order continuation, not a unique or already admitted exact solution.
Use the complete parent's energy `E`, local lapse flux `J`, and mean identity
`rho0=-<E>` at its certified mean root. Then

    rho_node=-E_node-J_node,
    (rho_node-rho0)/e^2 = <Edelta>-Edelta_node-J_node/e^2,

where `Edelta=(E-Ebase(H,D))/e^2`. The spatially constant base cancels exactly;
only the averaged flux vanishes, never its local value. Thus for the old U0,

    G/e^2 = 2b U0 k^2 - K*p*(R'_node/e^2)
            - beta [<Edelta>-Edelta_node-J_node/e^2].           (2)

The symbolic numerator is divided by e^2 before interval evaluation; its
constant/linear terms vanish and its remaining analytic powers are even.
The genuine cusp contributes `-2A*p^3*|e|*cos^3(theta)` on the reduced quadrant.
The phase charge and regulator velocity remain in the complete energy.
The independently enclosed alpha and |e| ranges contain the physical relation
`alpha=e^2`; enlarging to this rectangle makes the bound conservative.

The inherited bracket contains the certified mean root. Equation (2) is
enclosed over that entire bracket, not at an inserted or newly selected H.
No observed acceleration, coefficient fitting, extra root solve or family
selection is used.

## 3. Scaled shift errors are uniformly controlled

Reuse the exact frozen three-term shift approximation, not a new finite-mode
fit. Its complete variable-coefficient residual starts at `alpha^4`.
For each residual term `c_n*alpha^n`, `n>=4`, and
`0<alpha<=amax_exact=1/250000`,

    alpha^(n-1) <= amax_out^n/amax_exact,

where `amax_out` is the outward upper maximum used by the parent. Its
coercivity/error estimates are linear in the residual norm, with fixed
positive coercivity and coefficient bounds on the registered range.
Consequently the parent's maximum error divided by amax_exact bounds the
NORMALIZED shift error uniformly. This is not a fixed absolute error divided
by alpha near zero. The same argument applies to the shift-gradient error.

Across the nine cases the conservative normalized bounds include

    |delta R|/e^2 < 1.892e-15,
    |delta R'|/e^2 < 1.514e-13.

These errors are included in every energy and node-gradient enclosure. Odd
periodicity sets the exact node value R to zero; its derivative error remains.
The zero-amplitude homogeneous control is not rejected and no regular inverse
is extended through the globally aligned stratum.

## 4. Every registered case has a strictly nonzero defect

Outward interval evaluation uses mpmath.iv at 80 decimal digits. All nine
cases succeed with the first frozen partition, 16 angular boxes; no bracket,
tolerance, family, amplitude or partition-sequence change is made. Independent
coordinate controls and high-precision endpoint inspection use 110 digits,
above the contract's 80-digit control baseline, at the unchanged 1e-50
normalized tolerance. The following displayed bounds are rounded outward
from the saved binary interval endpoints:

| Family | eta | Enclosure of G/e^2 |
|---|---:|---:|
| Archived G3 | 1/4 | [11.8221, 11.8805] |
| Archived G3 | 1/64 | [0.0293084, 0.0293419] |
| Archived G3 | 1/1024 | [1.08963e-4, 1.09049e-4] |
| B1-frame | 1/4 | [12.8427, 12.8946] |
| B1-frame | 1/64 | [0.0296250, 0.0296484] |
| B1-frame | 1/1024 | [1.09183e-4, 1.09232e-4] |
| Hierarchical | 1/4 | [12.5248, 12.5742] |
| Hierarchical | 1/64 | [0.0296194, 0.0296425] |
| Hierarchical | 1/1024 | [1.09182e-4, 1.09232e-4] |

All intervals are strictly positive. This is a continuous-amplitude bound for
both signs, not nine sampled finite-amplitude residuals or an extrapolated
asymptotic claim. G itself tends to zero as e tends to zero; no nonzero
amplitude-independent lower gap for G is asserted. These are diagnostic
reference-unit quantities, not cosmological measurements or EFT cutoffs.

Exact leading coefficients computed from periodic monomial averages lie in
their respective full enclosures. Those leading controls alone are not the
finite-amplitude proof. The certificate depends on the pinned equations,
declared sector and correctness of the interval implementation; it is not a
formal verification of that library or independent peer review.

## 5. Necessary correction, not an adopted repair

If the same ansatz is continued with a different U, it must at least satisfy

    (K+2b*k^2*e^2)U=K*Hbg*p+K*p*R'_node+beta*rho_node.

H, R and rho must be solved WITH U; substituting their old values into this
equation is not a repaired coupled solution. At zero amplitude the Jacobian
of the mean equation and node equation with respect to (H,U) is

    [ -6M Hbg       0 ]
    [ -6beta M Hbg  K ],       determinant = -6M Hbg K != 0,

with `M=MP2+MU2*(c1+3c2+c3)/2` on these fixed registered points. Together
with differentiability and the local coercive shift inverse, this supports
only local implicit-function reasoning for this necessary pair of equations.
There is no quantified finite-amplitude repair, new regulator-velocity
completion, higher consistency, full admission or evolution theorem here.
No repaired state is adopted or evolved. A further bounded calculation must
solve and certify the coupled completion and its remaining constraints.

## Verification, preservation and next use

V2: 48/48 local checks, zero failed/unknown rows, exit zero. The original
four-coordinate density controls retain a normalized frame, all six nonzero
metric second-time jets, nonzero shift time jets, arbitrary finite scalar
acceleration and regulator second-time jet, and both slope signs. The largest
recorded normalized EZ discrepancy is 2.363e-112; node Epsi controls record
floating zero. They do not turn floating zero into an exact proof.

Complete fresh read-only replay recomputes all five JSON payloads. All ten
payload/sidecar bytes, sizes and mtimes remain unchanged. Byte equality and
metadata preservation have separate error messages. Source pins and their
sidecars/metadata are checked before and after each calculation. Original
parent sources, certificates, archives, failed attempts and sidecars remain.

The [V2 preflight addendum](RES001_R4C1_NODE_ACCELERATION_V2_PREFLIGHT_ADDENDUM_2026-10-18.md)
preserves V1's syntax/preflight failure and accidental sidecar creation after
that failure. V1 was never scientifically executed. V2 supplies corrected
indentation, the three-value return and additional dimension/leading controls;
no physical equation, parent input or numerical tolerance was changed.

R9-MT1-NODE-ACCELERATION-V2 is DEFERRED, not cleared. Inherit initial-admission,
initial-constraint, regulator-node, canonical/preparation/generic-family and
transitive review debt. Reuse only the necessary condition and bounded
rejection of the selected continuation. Do not treat it as a positive admitted
state or as rejection of every initial condition of the R4C1 action.

Stage1 original linear prepared-dust acceptance only; Stage2 INCOMPLETE;
Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 unchanged; physics_pass=false; gate_effect=NONE. The physical Hessian,
Cauchy/energy domain, nonlinear remainder, physical validity window, healthy
GR and both genuinely identifying matching inputs remain required.

No vault mutation, manuscript/PDF/site edit, commit/push, publication/submission,
new action/parent, provider dispatch or model/runtime change is included.

## Frozen artifacts

| Artifact | SHA-256 |
|---|---|
| V1 contract | 4e81b770bcf5ad3b999ce34af37326803c1f73aba852b21f1d0bafb75c2a5f96 |
| Preserved V1 preflight-failed source | f91899a6add8ceff67b2358f63f6cc8f2ec8b18cc0d486a00039fa4b84250e1b |
| V2 addendum | 255484635f5a6f665ce65484cb665d640951e8b7400f482c4289a8ca99cfb0eb |
| V2 executable | 1e77ba8e8fc9d09d3e7e4a3a556405fa45dd5ce0dbf89580ff7ae2df106a9a7c |
| summary.json | 825e3e39624d4533bcfb0e9db115cbc4695794f300d1f69b31463710f2c38804 |
| equations.json | 2a42a055cd690d70b20ec8257b279de771aa1c7ea54bf4befcfe198816064e3d |
| normalization.json | 447192694f9d65cd7791cfe93444dfe9a7d2566dfc99f453f590ae00825c668f |
| independent.json | 17a1eb375d1c45c02f18df3c3ed9a02635a03713446676db27eed987997f8d19 |
| cases.json | c279f6077cab86ce3dcdf964079d37234c98deafc8a0c68b917b3249a6478c86 |

Executable: Analysis/MasterTests/test_01_r4c1_node_acceleration_v2.py.
Receipts: Analysis/MasterTests/outputs/r4c1_node_acceleration_attempt_02.

    python -B Analysis/MasterTests/test_01_r4c1_node_acceleration_v2.py --replay Analysis/MasterTests/outputs/r4c1_node_acceleration_attempt_02

New executions require fresh nonexistent output directories. Only mutable
execution/review indexes receive guarded appends and refreshed index digests.
