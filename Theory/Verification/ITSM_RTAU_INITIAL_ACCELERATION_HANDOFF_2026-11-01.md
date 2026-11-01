# R-tau initial acceleration handoff - 1 November 2026

Goal ACTIVE. High remains last confirmed; never infer a setting change.
Owner: [initial construction report](../Gates/RES-001/RES001_R4C1_RTAU_INITIAL_ACCELERATION_V1_REPORT_2026-11-01.md).

Primary 23/23, exact replay; SHA256
dbcdacf8954e1cc59a2ebc42b91cd77f7a8e3473c2c54906b1f94e506455154d.
Audit V2 11/11, exact replay; SHA256
a0e30b7444c0831ecb76fd985122ff9dd6be045a14b112ced9fd9e2ceda86208.
Audit V1 10/11 remains preserved: incorrect extra count of 13 bounds
instead of the actual 12. Explicit schema correction changes no physics.

Actual initial thirteen-coordinate Euler family is a=a0+Lie_T(q),
a0=M13^-1 R13, T=Sdot. Coordinate two-jet zeta=zeta0+t Jw gives
transformed b_x=a0_xz/J and b_z=a0_zz/J^2+Abar^2*(-8r lambda_dot+6r^2).
Periodic gauge integrals fix c_x,c_y,c_z and xi; additive coordinate
translations enforce <T_old>_z=0. Sdot_new includes a nonzero baseline
coordinate term as well as xi. Mean metric accelerations are retained.

Construction is FUNCTIONAL with coarse all-root bounds, not sharp numerical
final gauge quadrature. ||a||_2<530.385 is deliberately loose and is not a
time-error/physical-window claim. Centre samples validate only a0. Zdot
is now fixed from the auxiliary first time tangent, with prepared bound
<0.000475041. Quantitative Zddot/higher-derivative bounds remain OPEN.
Action Noether identities give initial momentum/global-charge consistency;
an explicit local clock-reconstruction evolution check remains OPEN.

Next tighten final gauge/acceleration enclosures and higher auxiliary/gauge
derivative control, verify local clock reconstruction and complete actual
physical symplectic/characteristic admission. Do not redo root fitting,
coordinate preparation or replace the result by homogeneous propagation.
Do not assume finite-time preservation or evolving conformal shapes.

Planar scope only; general transverse wavevectors, physical quotient,
evolution, interactions/window and identifying matching remain open.
R-tau unadopted; G1-G6 incomplete; review DEFERRED; physics_pass=false;
gate_effect=NONE. No paper/site change, action adoption, dispatch, vault
mutation, publication or commit/push.
