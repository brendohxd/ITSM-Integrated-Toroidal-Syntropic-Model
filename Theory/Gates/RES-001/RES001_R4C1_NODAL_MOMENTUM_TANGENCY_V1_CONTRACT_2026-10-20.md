# Frozen contract: complete initial reduced momentum flow and node tangency

20 October 2026. Approved unchanged-action R4C1 Stage2. Review DEFERRED.

Continue the current nine-case global nodal lift, without repeating its
completed initial-coordinate audit. Compute ALL remaining canonical momentum
rates and test the first time preservation of the auxiliary node conditions.
This is a prerequisite for, not a replacement of, the full descriptor spectrum
and physical window. Preserve the original full objective and all holds.

## Exact reduced chart and force law

Retain the three G_AB field pairs, three mean h_iz pairs, all three frame
fields, radial amplitude R, internal phase, reservoir r, dust, Z and s.
Use the finite canonical polar map, not instantaneous Cartesian basis freezing.
Keep only the prescribed global phase/dust origins quotiented, their charges
fixed, and the remaining global translation chart. Project tangent directions
onto those gauge sections; do not project the base state or a physical mode.

Use Theta=Theta_other-g*s*dZ, g=b*sqrt(h)*V^2. For every canonical coordinate Q
whose momentum is retained,

    Qdot=H_P, Pdot=-H_Q-s*g_Q*Zdot.

The last term includes all metric/frame responses. Mean-coordinate terms
are integrated with their correct canonical factors; global phase/dust and
translation tangent projections are explicit. Reconstruct eliminated spatial
momenta by the existing constraint solution, never a singular V^2 inverse.

Use the verified initial Qdot, Zdot=Ud*w^2/p and the scalar-rate derivative
from the ORIGINAL regulator equation:

    sdot=[-U-(3H-Hbg-Rprime)*p+p*R*wprime/w]/p.

At each simple node R*wprime/w has the analytic limit Rprime; do not set it
to zero or divide by w there. No U(t)*w(t,z)^2 evolution is adopted. Initial
gdot=g*(5H-2Hbg)/p includes metric volume and changing frame norm. Test the
FULL regulator row H_Z-g*sdot-s*gdot over the whole period, not nodes only.

## Independent checks and stable first derivatives

Compare every momentum rate to the ORIGINAL unreduced first-order generator
with initial N=1/p, S^z=Rshift/p and S^y=Sy/p. Keep independent Z_hat and
the multiplier term N*(p_Z+g*s)*Z_hat when varying positions at fixed original
p_Z. Vary before using that constraint. Do not use the regular inverse at
nodes. The original local pi fields/p_V remain fixed for these unreduced
variations; polar canonical momenta transform exactly. Retain all sectors,
means, charges and the initial local density from the current lift.

Independently require the original conserved phase/dust density currents on
this initial slice:

    p_theta_dot=partial_z(Rshift*p_theta)/p,
    p_T_dot=partial_z(Rshift*p_T)/p.

For initial momentum first variations ONLY, use the exact closed-torus flat-
metric, constant-lapse identity delta integral(sqrt(h)*R3/s)=0. Derive it from
delta R3=partial_i partial_j delta h_ij-Delta tr(delta h); on planar data it
is -(delta h_xx+delta h_yy)second. This avoids subtracting a noisy integrated
curvature divergence. The underlying functional and reference retain R3.
Validate that its second variation is NONZERO (e.g. h=diag(exp(2a),exp(-2a),1),
R3=-2*a_prime^2). Never use this first-variation identity to remove curvature
from a future Hessian, evolution away from this slice or mode spectrum.

Use complex steps1e-18 and1e-22 for the forces. Freeze normalized1e-7 for the
independent generator comparison and1e-4 relative to the nonzero phase/dust
current amplitudes. Record raw, relative and step discrepancies. Omitting the
two-form cross must have a separately recorded nonzero effect; do not claim
that an effect below the binary64 floor has been physically resolved.

## Actual initial node-preservation test

Construct the complete initial reduced tangent (Qdot,Pdot,sdot,Zdot) without
integrating in time or projecting onto a prescribed slow graph. Reconstruct
fields nonlinearly in the fixed-charge/gauge chart and retain explicit clock
tau in C(tau). At initial nodes the coordinate node velocity is0 for the
given first jet; this is NOT imposed on general perturbations or future nodes.

Differentiate the undivided nodal energy compatibility

    C_E=E0+Edust+div(F)+sqrt(h)*K_Q*s^2

at an exact node, where E0 already contains -sqrt(h)*K_Q*s^2/2. Also test
chi=Z+s*div(V). Use complex directional steps1e-18 and1e-22 along the INITIAL
tangent to avoid subtracting near-zero real energies. Record derivatives
before any classification. Normalize the C_E derivative by K_Q*p times the
maximum of H and |sdot| (reference units). Freeze1e-4 for sampled consistency;
this is not a continuous-time or infinite-hierarchy certificate. If larger
than this, retain a warning/unresolved result; do not retune data or tolerance.

Keep energy balance explicit: Hpsi is not assumed constant, because the
force-clock matter conformal factor is time dependent. Check the variational
balance with H_tau, whose initial matter contribution is beta*Qdust/p.

## Verification and disposition

All9 frozen cases; n=17,25,33, both shifted node orientations. Use the original
8/12 shift control and current joint inputs unchanged. No discarded events.
Separate implementation checks, sampled tangency disposition and physical
clearance. Preserve warnings/failures and their exact assertions.

Freeze versioned source/contract sidecars before execution. Fresh receipts,
bounded Windows-spawn parallelism (max16), parent-only writes, standalone
optimizer and complete fresh read-only exact replay with external immutable
metadata guards. Only guarded append-only research/review documentation changes.

No state adoption/evolution, action/parent change, smoothing, node removal,
paid provider/model/runtime change, vault-management write, manuscript/site,
publication, commit or push. Stage2 remains INCOMPLETE and Stage3 NOT_ENTERED
unless their actual full acceptance requirements are separately proved.
