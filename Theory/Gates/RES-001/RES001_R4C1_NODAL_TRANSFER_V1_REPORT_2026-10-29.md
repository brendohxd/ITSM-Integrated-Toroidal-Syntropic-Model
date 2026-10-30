# G1 full-action junction condition and the missing concentration estimate

29 October 2026. **Conditional; Rule-9 DEFERRED; physics_pass=false;
gate_effect=NONE; G1-G6 INCOMPLETE.**

## Finding

The original covariant auxiliary equation forbids the model's scalar normal-
gradient jump IF the full solution/limit has continuous metric/frame and an
ordinary auxiliary field with the stated traces. This is a conditional
full-action junction result, not another fixed-background model identity.

However, finite original action alone does not imply the uniform rescaled
auxiliary norm needed for that transfer. An explicit thin-layer test has
vanishing original auxiliary-square cost but a concentrated inner auxiliary
limit. This test does not solve the coupled equations. In fact it leaves a
nonzero second-derivative delta residual in the scalar equation. It is NOT
an adopted repair, new physical state or added node source.

The corrected model-branch rejection therefore stands, while a full-action
weak-solution rejection remains unproved. The exact missing requirement is
an ON-SHELL current/compactness estimate or an action-derived coupled layer.

## 1. Retain the original auxiliary operator and boundary term

Use [R4C1's frozen action](RES001_R4C1_ACTION_FREEZE_2026-09-25.md) and
[first variation](RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md):

    Delta psi = div(h grad psi)-a dot grad psi,
    E_Z=b*(Z+Delta psi),
    Delta_dagger Z=div(h grad Z+Z*a),
    E_psi=-div(K_Q*Q*n-3*A*sqrt(Y)*h*grad psi)
           +b*Delta_dagger Z-beta*rho.

Integrating only the declared regulator term by parts gives

    L_reg = b/2*(Z+Delta psi)^2-b/2*(Delta psi)^2
            -b*div(Z*h*grad psi).

The boundary flux is retained. Smooth periodicity removes an outer spatial
torus boundary, not a possible internal nodal jump. Temporal boundary data
are not changed. On shell Z=-Delta psi; the scalar equation contains
-b*Delta_dagger*Delta psi. It is generally incorrect to replace this by
-b*Delta^2 psi: their first-order acceleration terms differ. The executable
checks the completion, elimination sign and formal-adjoint difference.

## 2. Conditional full-action junction law

Let Sigma={phi=0}, N=dphi. Assume the metric/frame are continuous and
piecewise C1 with bounded one-sided derivatives, psi is continuous and
piecewise C2, and Z is an ordinary piecewise C2 function with finite
one-sided value/derivative traces. Products in the currents must be locally
integrable. These are hypotheses to be justified for a solution, not
regularity obtained from the previous check counts.

Tangential continuity gives [grad psi]=lambda*N. The surface term in E_Z is

    b*lambda*h(N,N)*delta(phi).

With no auxiliary surface distribution, source-free E_Z requires lambda=0
where h(N,N)>0. In the registered local orthonormal frame
n=(sqrt(1+w^2),0,w,0), a moving nodal normal is N=(-v,0,0,1), and

    h(N,N)=1+w^2*v^2; at w=0 it equals1.

In the necessary inner normal chart the corresponding coefficient is
a+location^2*v^2>=a=4/625>0. Real motion of that model interface cannot
cancel its scalar gradient jump. No persistence theorem for the evolving
full frame is inferred from the initial-frame formula.

Once the scalar gradient jump vanishes, a discontinuity [Z] would generate
the highest scalar surface term b*h(N,N)*[Z]*delta_prime(phi). Other regular
currents and a nonnegative dust Radon surface density cannot cancel this
double layer. Thus [Z]=0 in this class as well. The remaining scalar surface
balance is

    b*(N.h.[grad Z]+Z*N.[a])-beta*rho_surface=0.

A jump in frame acceleration or an actual dust surface density is not
silently set to zero here. Their derivation and conservation would still be
required. In particular this law does not allow prescribing a shell merely
to cancel the earlier model residual.

## 3. Why finite original action does not supply the transfer norm

Let c be the POSITIVE corrected coefficient c3 from INNER_CAUCHY_V2.
As a diagnostic, smooth just its c*T^3*abs(X) component by adding

    r_epsilon=c*T^3*(sqrt(X^2+epsilon^2*T^2)-abs(X)).

The bound abs(r_epsilon)<=abs(c)*epsilon*T^4 is uniform. At each fixed X!=0,
the correction's initial time jets through order4 vanish; it changes neither
the initial fields nor velocities. This is a test family for an estimate,
not a proposed on-shell continuation. Its induced leading normal auxiliary
core is

    Zcore_epsilon=-a*c*epsilon^2*T^5/(X^2+epsilon^2*T^2)^(3/2).

Exact integration gives

    integral Zcore_epsilon dX = -2*a*c*T^3,
    integral abs(Zcore_epsilon)^2 dX
      =3*pi*a^2*c^2*T^5/(8*epsilon).

Moreover, for a smooth compactly supported test function phi,

    abs(<Zcore_epsilon+2*a*c*T^3*delta(X),phi>)
      <=2*a*abs(c)*epsilon*T^4*norm(phi_prime)_infinity.

This proves the concentrated weak limit quantitatively; it is not a fitted
delta approximation. The kernel mass and first moment are both2, and its
square integral is3*pi/8. Independent Gaussian pairings and quadrature check
the exact identities without setting the bound.

Return to the original chart: t=epsilon^2*T,w=epsilon*X and
Zphysical=epsilon^5*Zcore_epsilon. On 0<T<1, with measure dw dt,

    (b/2)*integral Zphysical^2 dw dt
       = (b*pi*a^2*c^2/32)*epsilon^12.

A smooth bounded physical volume/normal-coordinate Jacobian preserves the
power. Dividing by the outer inner-action scaling epsilon^13 instead gives
a norm growing as1/epsilon. The original core has amplitude O(t^2) and first
t/w derivatives O(t), so it causes no first-order off-shell action divergence.
The square cost is positive here, not an assumed coercive total Hamiltonian.
The whole-line integral is a local chart test norm. A fixed smooth spatial
localization retains the core scaling and introduces outer-tail terms; it
does not replace the torus mean, charge or conservation equations. Those
on-shell/global requirements have not been imposed on this test family.

Thus even finiteness of this auxiliary-square sector does not supply uniform
rescaled L2 compactness. The other original field equations MAY exclude
such families; this off-shell example is not an on-shell counterexample to
those equations. It prevents using finiteness alone as that missing proof.

## 4. The simple concentration is not a coupled repair

In the normal model, the concentrated limit changes the scalar residual by

    2*b*a^2*c*T^3*delta_second(X).

The coefficient is enclosed in

    [3.56453541405924e-7,3.66715659193282e-7],

which excludes zero across the inherited c3 range. The uniform scalar
correction tends to zero as a distribution; its time derivatives do too.
Also X^2*delta(X)=0, so the temporal auxiliary term does not cancel this
highest normal double derivative. A dust Radon measure cannot provide the
missing delta_second term. No such source exists in the declared model.

Consequently one cannot repair the auxiliary junction by this smoothing and
then ignore the scalar equation. A viable layer, if one exists in R4C1,
must derive the coupled metric/frame/scalar/matter response and all constraints
from the original action. No freely chosen concentration is adopted here.

## 5. Evidence and remaining calculation

Contract: [nodal transfer V1](RES001_R4C1_NODAL_TRANSFER_V1_CONTRACT_2026-10-29.md).
Executable: Analysis/MasterTests/test_01_r4c1_nodal_transfer_v1.py.
Receipt: Analysis/MasterTests/outputs/r4c1_nodal_transfer_v1_attempt_01/summary.json.
SHA256: b77447a1d97dfb8711594db66f3ec8ada3ac19d741fc3b5e9f886312189b4b71.
37/37 computational checks; no failed/unknown rows;254 pins; exact replay.

Next derive an on-shell concentration budget or show that the full equations
enforce the regular transfer class. Retain the original formal adjoint,
frame/metric current products, dust positivity/conservation and global
means/charges. Neither an assumed compactness class nor a test smoothing
supplies G1/G3 admission. G1-G6, physical normalization/window, matching and
numerical prediction remain incomplete. No manuscript/publication changes.
