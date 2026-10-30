# Total initial scalar jerk: finite extension and explicit weak interface

28 October 2026, Australia/Perth. Conditional; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## Result and meaning

For the registered unchanged-action B1 eta=1/4,e=1/500,k=40 quartic
construction, the TOTAL initial scalar jerk j=psi_ttt has a finite continuous
extension through both node orientations. Its analytic part has no remaining
pole. The already derived physical cusp is retained.

Conservative reference-unit magnitude bounds over the full root box are

    |j| < 133.660   near |w|<=1/1000,
    |j| < 2975.311  away from |w|<1/2000.

These overlapping domains cover the periodic profile. The bounds are not
predictions of those values or useful-accuracy/time-evolution estimates.
They establish finiteness. The total initial jerk is locally Lipschitz and
belongs to spatial H1, but not H2, for the registered periodic profile and
its torus embedding. This is a statement about an INITIAL time jet, not an
admissible evolved solution space or an existence/uniqueness theorem.
The Lipschitz/H1 membership follows from the analytic expressions and cusp;
no numerical Lipschitz-norm or temporal energy estimate is claimed.

The [joint C4 exclusion](RES001_R4C1_QUARTIC_JERK_TRANSPORT_V2_REPORT_2026-10-27.md)
and [continuous initial acceleration certificate](RES001_R4C1_QUARTIC_INITIAL_ACCELERATION_V1_REPORT_2026-10-27.md)
remain unchanged. The new result resolves the possible analytic pole which
the former report explicitly left open. A weaker initial regularity exists;
an evolved weak or classical background has not been established.

## 1. Derive the source before dividing by w

Derive the analytic Vy Euler forcing from the original normalized-frame
density, retaining metric volume/time drift, frame spatial terms, the temporal
regulator, condensate phase current and the shift. Take variations BEFORE
inserting Z=U*w^2+W*w^4 and Zdot=Ud*w^2. The analytic partition is the same
exact original-minus-cusp split already checked in the parent calculation.
The physical cusp is recombined separately; physical A is not set to zero.

Only the zero-acceleration forcing is extracted. The actual coupled
acceleration still uses the complete B(w), not a frozen metric or a diagonal
scalar approximation. Eliminate Rsecond by its original constrained-shift ODE,
then set R=w*T using the removable T=R/w quotient.

The exact source is odd in w at fixed(wprime,T,Rprime). Its quotient by w
is even and has no node denominator. Outward interval arithmetic gives

    |fy_analytic[Vy]/w| < 53.329816,  |w|<=e/2.

The stored exact expressions permit replay. All twelve signed parent
full-original directional/AD source controls, including both node orientations,
agree with the NEW symbolic source at normalized errors below4.94e-66,
against the frozen1e-18 criterion. These independently computed controls
were reused rather than rerunning the completed full-generator audit.
The comparison uses the source BEFORE ODE elimination and the same polynomial
shift representative, so its truncation is not mistaken for an exact ODE.

## 2. Retain the coupled inverse response

Exact matrix identities show that(hxx,hyy,hzz,Vy) is an isolated kinetic
sector of B(w). All other directions remain in the original generator and
parent bounds; this isolation is derived, not a physical-sector truncation.
The inverse Vy/metric crosses vanish at w=0 and are odd in w. The certified
inverse and first inverse-derivative norms therefore control those crosses
divided by w. They are not set to zero away from the node.

With aPsi fixed by its original regulator equation and C the scalar cross,

    ay_analytic[Vy]/w = B_inv[Vy,Vy]*(fy_analytic[Vy]/w+b*Z*aPsi)
       +sum_hdiag (B_inv[Vy,hdiag]/w)
                         *(fy_analytic[hdiag]-C[hdiag]*aPsi).

All terms have removable analytic node limits. Using the entire registered
root box and existing exact inverse/shift errors gives

    |ay_analytic[Vy]/w| < 1340.376,
    |partial_z(aPsi)| < 0.012406.

Insert them, the metric trace bound and full shift/volume terms into the
already coordinate-verified differentiated regulator equation. Add the
controlled jerk cusp. This yields the total bounds above without zeroing a
numerical residual or discarding coupled fields. Away from the nodes the
original nonzero-w equation supplies the second magnitude bound.

## 3. Weak derivative and interface term

The actual coupled cusp component is derived from the complete isolated
four-direction inverse, including all metric crosses. Its positive branch
has the exact form w*F(w), where F is analytic and even and

    F(0)=9/560000.

Thus j_cusp=|w|*F(w). Near a simple alignment node, w=sigma*x+O(x^3),
|sigma|=2/25. The second WEAK normal derivative has the singular contribution

    partial_z^2 j = (regular part)
                  +(9/3500000)*delta(z-z_node)

at each simple node. The analytic jerk cannot cancel this delta. The first
weak derivative is bounded with a jump and no delta, explaining H1 membership;
the nonzero second-derivative delta excludes H2. No arbitrary L2 field is
assigned a nodal value: the particular computed jerk has a continuous
representative.

Independent integration-by-parts controls use tests1 and cos(2theta) on one
profile period containing both node orientations. The full cusp, rather than
only its leading model, is integrated. Regular second-derivative terms alone
miss +/-5.142857142857e-6 in those tests. Including the derived node jumps
restores the weak identity with normalized errors below4.51e-93, against1e-30.
If the torus contains multiple profile periods, the interface sum repeats at
ALL corresponding nodes; it is not reduced to two nodes on a larger domain.

For g=b*w^2, multiplication g*partial_z^2 j kills this particular delta
because g(node)=0. Also g*j has a C2 normal cusp contribution proportional
to |w|^3. These facts do NOT allow division by g across a node or equating
g*jsecond with(g*j)second. Product-rule and interface terms must be retained
in the actual transport equation. No Hamiltonian/momentum/charge propagation
identity has been proved by these integration controls alone.

## 4. Verification and preservation

Executable: Analysis/MasterTests/test_01_r4c1_quartic_total_jerk_v1.py.
Method: RES001_R4C1_QUARTIC_TOTAL_JERK_V1_METHOD_2026-10-28.md under the
frozen graded-transport contract.30/30 exact/interval/reused-generator/weak
controls pass, with no failed or unknown rows. A fresh recomputation returns
READ_ONLY_REPLAY_EXACT.148 parent/current source artifacts are pinned and
unchanged. Same-author methods/replay are not independent peer review.

Receipt: Analysis/MasterTests/outputs/r4c1_quartic_total_jerk_v1_attempt_01/summary.json,
SHA256 fd5f9b4d3e84f02548a8c2b34174aa2fb3cd8870c0f26b5280919ba4ff69f9b6.
Exact source/quotient/kernel expressions, conservative outward binary
enclosures and all controls are retained. No earlier scientific file,
sidecar, failed attempt, manuscript or retained PDF is changed.

## Next required work

Now calculate actual initial alignment transport and Hamiltonian/momentum/
charge tangency with the interface structure retained. Track all three frame
components, not just Vy, and do not impose stationary nodes. Use the original
varied action/Noether identities with vector terms; Bianchi assignment is
insufficient. Initial tangency is still distinct from persistence or an IVP.
Establish a meaningful graded evolution space and estimates before physical
perturbations or a claimed time interval.

Inherit all original-action, root, initial acceleration, force, cusp and
geometry review dependencies. PROCEED_PROVISIONALLY for the scoped finite
initial jerk and weak interface result. HOLD_SUBSTANTIVE for actual constraint
transport, background admission, time evolution, physical modes/window/GR and
matching. Stage2 INCOMPLETE; Stage3 NOT_ENTERED; MAT-001 BLOCKED;
K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED.
No new parent/state adoption, vault mutation, dispatch, publication,
commit/push or deployment.
