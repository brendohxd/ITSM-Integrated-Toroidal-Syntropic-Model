# Second node consistency: the specified quadratic continuation fails

27 October 2026. R9-MT1-SECOND-NODE-CONSISTENCY-V1.
Claim Conditional; expanded G1 INCOMPLETE. Review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Outcome and exact scope

For the registered new_B1_frame case eta=1/4, e=1/500, k=40, the exact implicit
joint H/U/Ud construction with Z=U*w^2 and Zdot=Ud*w^2 fails an additional
necessary regulator-node condition under the stated joint classical regularity.
The outward trace enclosure is

    222.2495786027... <= Q <= 230.2037361865... .

The lower bound is strictly positive. A deliberately coarser enclosure is
[222,231]. The nonzero result uses the inherited exact-root/shift boxes and
new exact action-derived coefficients, not the printed point root or a fitted
finite-angle limit. Both node orientations give the same trace.

This rejects ONLY this specified quadratic initial-profile continuation in this
regularity class. It does not reject every initial state, weaker solution,
parameter value, diagnostic family, R4C1 or ITSM. The previous three-condition
joint root remains valid for its explicitly necessary-only scope. No original
result, source, sidecar or failed attempt is overwritten.

## 1. Necessary condition from the original regulator equation

The original equation, divided by constant b, is

    E_Z/b = Z + div(hp*grad psi) - acc.grad psi,
    hp=g_inverse+n*n, acc=n.nabla n.

At the reference initial node, h=I, hdot=2H I, V=Vdot=0,
psi=0, psidot=p spatially constant, and the registered shift time derivatives
vanish. For sufficiently regular joint time/normal continuation,

    Q = partial_t^2(E_Z/b)|node
      = aZ|node + partial_z^2(aPsi)|node
                    + p*partial_z(aVz)|node.       (1)

For example, C4 psi, C3 metric/frame and C2 Z with the needed joint derivatives
and continuous acceleration traces are sufficient. This is not asserted to be
the weakest possible regularity. It is not a weak-solution exclusion.

To see the cancellation directly, V(t,node)=O(t^2), hence c=VhV=O(t^4) and
c_t=O(t^3). The scalar spatial gradient starts at O(t^2). In the full coordinate
regulator operator the only quadratic-time contributions are Z, psi_zz and
p*partial_z(Vz); all other terms vanish at that order under these initial
hypotheses. No metric acceleration or general spatial-gradient coefficient is
deleted from the original equation. Initial node velocity is zero; the second
transport term is proportional to the initial normal derivative of E_Z, which
vanishes for this initial structure. No persistent nodal trajectory is assumed.

Four independent full-ADM coordinate controls retain arbitrary metric and
off-diagonal accelerations, spatial acceleration gradients and scalar third/fourth
time jets, with both slope signs. They verify (1) at normalized 1e-30.

## 2. Original scalar equation fixes the regular-side aZ trace

Let x measure distance from a node, with

    w=sigma*x-sigma*k^2*x^3/6+O(x^5),
    R=r1*x+r3*x^3/6+O(x^5),
    rho=rho_node+rho2*x^2+o(x^2),
    aPsi=a0+a2*x^2+o(x^2).

The undivided regulator equation gives

    a0=-U-(3H-Hbg-2r1)p,
    a2=p*(2r3-r1*k^2)/3.                           (2)

Use the ORIGINAL scalar current

    J=K_Q*n*(n.grad psi)-3A*sqrt(Y)*hp*grad psi
        -b*(hp*grad Z+Z*acc),
    E_psi=-div(J)-beta*rho.

The cusp's contribution to this initial scalar equation and energy is
O(|x|^3): c=O(x^2), c_t=O(x^2), psi_z=0 initially, and R=O(x).
Its quadratic normal coefficient is therefore zero. This composite order
statement permits a smooth arithmetic coefficient extraction; it does not
change A or define an ordinary third cusp tensor at alignment.

The kinetic scalar contribution through x^2 follows by differentiating its full
current, retaining the metric volume and shift. For the regulator current the
time divergence contributes b*sigma^2*aZ*x^2 at this order. Its spatial part is

    b*partial_z[2U*w*w' - U*ty0*w^3] + higher-order terms,

where ty0=partial_z S_y at the node. Thus

    E_psi[x^2] = b*sigma^2*aZ
      -K_Q*(a2+sigma^2*a0)
      -K_Q*p*(-r3/2+(5H-2Hbg-3r1)*sigma^2)
      -4bU*sigma^2*k^2-3bU*ty0*sigma^3-beta*rho2.    (3)

All dependent-momentum, local-density and geometric contributions must be
included in rho2 and the acceleration slopes; replacing rho by its mean would
change this condition. The independent scalar-current verifier computes the
full coordinate divergence, not formula (3), on four nontrivial metric/frame/
shift/field Taylor controls. It passes 4/4 at normalized 1e-30.

This extra check is essential: the earlier approximate-Q calculation already
used the candidate formula (3), so agreement between that Q and a symbolic
evaluation alone would not independently verify the scalar trace formula.

## 3. Coupled metric/frame and shift jets from the action

Derive the selected off-diagonal metric Euler row and the longitudinal-frame
row's first normal jet before setting their accelerations. At this B1 reference,
the derived metric row is -Ah/2=0, so Ah=0. It is a result, not frozen gravity.
The longitudinal-frame slope is

    partial_z(aVz)=3*(Hbg-r1)*sigma^2/5
                       -3U*sigma^2/11-2r3/5.       (4)

General diagonal metric accelerations, transverse-frame slope and other unused
acceleration symbols were retained until their cancellation was checked.
The original shift ODE, differentiated at the node, gives

    r3=10*sigma^2*(H-9Hbg/20-11r1/20).              (5)

No old frequency or numerical spatial fit determines (4) or (5). The original
potential/canonical/force contributions to these particular selected rows vanish
on the initial slice; they are not removed from generic equations. The flat
N=1 spatial Ricci Euler force is zero only at this initial slice.

rho2 is derived independently from the full proper Legendre energy and the
LOCAL flux partial_z(gamma*h_inverse[z,i]*pV_i). Its exact rational expression,
along with the two Euler rows and Q, is in the enclosure receipt. The formulas
contain no floating coefficients. Their evaluations agree with the independent
AD/Taylor calculation at normalized errors below 4.3e-63 in the registered point
control; those point comparisons do not supply the interval certificate.

## 4. Exact-background enclosure and interpretation

Substitute sigma^2=(40/500)^2=4/625 and the exact B1-family parameter map.
The resulting Q is a rational polynomial in H,Hbg,U,r1. Use the FULL inherited
joint H/U boxes, the original background-H enclosure and the joint certificate's
controlled normalized shift-gradient box times alpha=1/250000 for r1.
Equation (5) eliminates the higher shift jet exactly. These bounds contain the
exact implicit root and exact shift, including their documented errors.

Pinned mpmath interval arithmetic at 80 digits evaluates Q outside zero on these
boxes; exact outward binary endpoints are retained in the receipt. No box was
narrowed after observing the result. This is an executable enclosure argument
conditional on the exact source derivation and trusted arithmetic implementation,
not proof-kernel verification or independent academic review.

The approximate central trace is 225.788914664 in reference units. It is not a
physical frequency, cutoff or observational acceleration. Its sign at the exact
specified construction follows from the enclosure and analytic/independent
derivation, not from the apparent stability of its printed decimal digits.

## 5. Verification and preserved failure

- Second-node geometry/approximate-trace executable: 18/18 local method checks.
- Exact coefficient/enclosure V2: 11/11 checks, including nonzero outward interval.
- Separate original scalar-current verifier: 4/4 checks.
- All three successful executables freshly recomputed with READ_ONLY_REPLAY_EXACT.
  Original receipt/sidecar bytes were not rewritten. Same-author implementations
  and replays do not constitute independent scientific review.
- Enclosure V1 stopped before mathematical checks because its loader omitted
  shared potential parameters. Its original source/sidecar and traceback remain.
  V2 uses the existing canonical loader's exact shared source, with integral
  float literals represented as the same exact integers. No action, equation,
  tolerance or interval box changed.

| Receipt | SHA256 |
|---|---|
| second-node consistency V1 summary | 2fe36ca4652b276172fe3473897655d41c9e4a4f18be3f4e915e5f363cef23e2 |
| second-node enclosure V2 summary | ad053bf3d816bad7983281ff9d16cf52671398face84249ced7e4f47b51afd24 |
| independent scalar trace V1 | f16a1e0ab3b69bb864ab7c0f179269d9cec0e65c00dc891a408844b2c617e030 |

Each is under Analysis/MasterTests/outputs/ in its named fresh attempt directory.
Executable/contract/dependency hashes, interval inputs and exact formulas are
in the receipts. The scientific source owners and prior necessary constructions
remain unchanged. No review clearance or canonical promotion follows.

## 6. Next supported G1 work: higher initial-profile freedom

The quadratic Z profile is a chosen initial-data ansatz, not an operator in the
action. The already approved unchanged-action diagnostic Z=U*w^2+W*w^4 supplies
a candidate additional initial datum. At fixed H/U/shift jets, the analytic
normal-order calculation suggests the partial gain

    partial_W Q=-(K_Q/b+14*sigma^2)=-4181/625.       (6)

This local partial sensitivity was checked in the preceding method controls,
but it is NOT the derivative along the full constraint surface. W changes the
global shift and mean/root equations. Derive and certify a new JOINT mean,
node-field, node-time and second-node construction with positive dust and fixed
charges; do not patch W and reuse an old root certificate. No W value or repaired
physical state is adopted by this report.

Continue that supported same-action test under the expanded goal. A successful
four-condition construction would still be necessary-only progress; further
admission, regularity, evolution, physical modes/window, GR and genuine matching
remain. G1-G6 stay incomplete. No new parent, manuscript/site/publication, vault,
commit/push, provider or global runtime change occurred. Inherit the original
joint/acceleration/transport/constraint/source and transitive deferred review debt.
