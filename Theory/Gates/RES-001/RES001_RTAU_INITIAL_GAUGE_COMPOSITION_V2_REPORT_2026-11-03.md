# R-tau initial gauge-closed weak canonical rate map

3 November 2026. Conditional component of the confirmed-High observable-
norm bundle. R-tau unadopted; original R4C1 unchanged. Review DEFERRED;
physics_pass=false; gate_effect=NONE; original G1-G6 incomplete.

## Result and scope

The initial compatible canonical graph now has a bounded spatial-gauge-
closed weak rate construction. The periodic corrective shift is solved,
instead of remaining an independent caller input. Full field AND canonical
momentum rates receive that correction and the background coordinate
drift. Physical metric-modulus rates and harmonic coordinate velocities
are retained. The initial density/trace inverse supplies the input lift.

This is an INITIAL canonical weak rate map on the declared compatible
graph. It does not supply the density-coordinate time row, evolving Green
inverse, a positive physical energy, a finite-time domain theorem or a
background tube. In particular the large conservative constants below
are not growth exponents or evidence of physical stability/instability.

Owners: [bundle](RES001_RTAU_COUPLED_OBSERVABLE_NORM_V1_CONTRACT_2026-11-02.md),
[weak rate rows](RES001_RTAU_WEAK_CANONICAL_RATE_V2_REPORT_2026-11-03.md),
[initial compatible graph](RES001_RTAU_WEAK_GRAPH_V1_REPORT_2026-11-03.md),
[periodic gauge solve and paired rates](RES001_R4C1_RTAU_GAUGE_VELOCITY_V1_REPORT_2026-11-01.md)
and [initial symplectic chart](RES001_R4C1_RTAU_SYMPLECTIC_CHARGE_FRAME_V1_REPORT_2026-11-01.md).
The [V1 contract](RES001_RTAU_INITIAL_GAUGE_COMPOSITION_V1_SPEC_2026-11-03.md)
and [V2 exact-expression correction](RES001_RTAU_INITIAL_GAUGE_COMPOSITION_V2_SPEC_2026-11-03.md)
were frozen before execution.

## Initial gauge construction with retained drift

Use the existing fixed initial adapted coordinate zeta, J=d zeta/dz,
with the declared positive bounds j<=J<=u and background coordinate
velocity w. Background metric h=diag(a^2,a^2,Abar^2) in that coordinate.
Initial perturbations are already in the spatial gauge: their mixed and
longitudinal metric variations are constants in zeta, including physical
moduli. The background moving chart is shared by the perturbations;
the corrective multiplier keeps their rates in this gauge.

First evaluate the affine zero-correction canonical rate v0 in the
original coordinate. This is a decomposition step, not the final physical
shift prescription. Form the metric sources b_i from

    Tq*(v0-Lie_w delta q).

The background Lie term includes tensor index terms, even for constant
metric-modulus perturbations. Solve the actual periodic row

    b_x+hxx*xi_x'=c_x, b_y+hyy*xi_y'=c_y,
    b_z+2*Abar^2*xi_z'=c_z,
    c_x=mean(b_x/hxx)/mean(1/hxx), similarly y,
    c_z=mean(b_z).

Use the mean-free periodic primitive and add the independent harmonic
coordinate velocities. The c_i are physical metric-modulus rates; they
are not replaced by zero. Convert the correction to the original chart:

    sigma=(xi_x,xi_y,xi_z/J).

Insert sigma and its spatial derivative in ALL canonical rate rows. The
existing action controls establish the field Lie response and dual
momentum-density response to this multiplier. Finally transform both
corrected rows together:

    v_new=Tq*(v_corrected-Lie_w delta q),
    p_t,new=Tp*(p_t,corrected-Lie_w^dual delta p).

This construction does not independently project the metric onto a graph
or suppress a complementary mode. It fixes coordinate freedom at the
initial slice. A future conformal metric or time-uniform gauge inverse
has not been assumed.

## Closing the shift norm and lifting compatible input data

Let P0,Q1,F2 be the original-coordinate canonical input controls of the
weak-rate owner. Let H be the Euclidean norm of the three retained
harmonic coordinate velocities in zeta. Write W=||w||infinity,
P=||w_z||infinity, r=1/13000. The actual field L2 pullback bound is

    Fq=max(1,u,j^-2), A=Fq*sqrt(u).

With Cxi the larger inherited periodic H1 inverse bound,

    ||b||L2 <= A*(||v0||L2+(W+2P)*Q1),
    ||xi||H1 <= Cxi*||b||L2+H,
    ||sigma||H1 <= Cback*||xi||H1,
    Cback=[max(1,u,1/j)+r/j]/sqrt(j).

The last factor retains the actual derivative and measure conversion of
xi_z/J; it reuses the corrected V2 canonical auxiliary pullback argument.
The initial Legendre bound supplies

    ||v0||L2 <=24.020615*P0+60.831961*Q1.

Substitution closes the prior caller-shift input U1 in every weak row.
Harmonic coordinate velocities remain inputs. The modulus-rate output
obeys ||c|| <=exp(4r)*||b||L2 and is evaluated separately.

For the compatible graph let D be the owning assembled source norm Dminus,
including its required weighted range, source means, momentum means and
separate global charge conditions. D is not the physical scalar density
alone. Put Qf=||free configuration||H1 and Pf=||free momentum||L2 in the
original coordinate after the global charge completion.

The unknown trace slots are delta hxx=delta hyy=a^2*f. The three eliminated
momenta occupy hxz,hyz,hzz slots. Consequently the previous graph bounds
give the exact sufficient norm lift

    Q1 <= Qf+sqrt(2)*exp(2r)*(1+2r)*C_f*D,
    P0 <= Pf+sqrt(C_px^2+C_py^2+C_pz^2)*D.

Here C_f and C_pi are the outward binary bounds of the weak-graph receipt.
Free configuration includes metric-modulus data; D includes retained
momentum means. No homogeneous or harmonic physical data are set to zero.
Both perturbation parities and the exact weighted longitudinal range remain.

## Negative-Sobolev pullbacks and density weights

For a rate r transformed as T(z)*r(z(zeta)), its pairing with a test phi
is the original-coordinate pairing with

    J*T*phi(zeta(z)).

For ordinary canonical momentum T=Tp=1/(J*Tq), so this test multiplier
is 1/Tq. For the force momentum, a scalar density, it is exactly one.
For the auxiliary Z, a scalar FIELD, it is J. Conflating the last two
would give an incorrect H^-2 pullback.

For a generic weight g and J=zeta_z, the required test derivatives are

    D_z(g*phi(zeta))=g_z*phi+g*J*phi',
    D_z^2(g*phi(zeta))=g_zz*phi+(2g_z*J+g*J_z)*phi'
                                                   +g*J^2*phi''.

Use dz=d zeta/J and |J_z|<=r*u, |J_zz|<=(r+r^2)*u. With
G0=max(1,u^2,1/j), sufficient dual bounds are

    A_p1=G0*[max(1,u)+2r]/sqrt(j),
    A_p2=[max(1,u^2)+r*u/sqrt(2)]/sqrt(j),
    A_Z2=[u*max(1,u^2)+sqrt(2)*r*u+(r+r^2)*u
                                      +3r*u^2/sqrt(2)]/sqrt(j).

The H2 norm uses ||phi||L2^2+2||phi'||L2^2+||phi''||L2^2. The formulas
bound the chain-rule diagonal and off-diagonal terms, rather than
treating a nonconstant coordinate change as an isometry.

For background momentum-density drift,

    Lie_w^dual delta p=D_z(w*delta p)-T(w_z)^T*delta p.

Its ordinary H^-1 norm is <=(W+2P)*P0; for force momentum the index term
vanishes, giving the sufficient H^-2 bound W*P0. Scalar auxiliary drift
w*delta Z_z has H^-2 bound <=(W+P)*||delta Z||L2. These terms, as well as
the corrective multiplier's response, are included in the following rows.

## Explicit compatible-input bounds

Each output norm is at most the sum of D,Qf,Pf,F2,H times the corresponding
conservative upward-rounded constants below. Outputs use the adapted
coordinate norm; inputs D,Qf,Pf,F2 use the original-coordinate conventions
above. These are initial mixed-space estimates, not a physical data-energy
equivalence or a differential inequality in time.

| Output | D | Qf | Pf | F2 | H |
| --- | ---: | ---: | ---: | ---: | ---: |
| field rate L2 | 167010.808 | 4353.901 | 1719.209 | 0 | 24.934 |
| ordinary momentum rate H^-1 | 417950.588 | 10897.821 | 4299.687 | 0.000263218 | 62.408477 |
| force momentum rate H^-2 | 158344.870 | 4128.573 | 1629.218 | 0.455957133 | 23.647860 |
| auxiliary Z L2 | 0.015437570 | 0.000521997 | 0 | 1.000424 | 0 |
| auxiliary Z_t H^-2 | 167379.768 | 4364.315 | 1721.949 | 0.000267577 | 24.973386 |
| periodic corrector H1, adapted | 6604.591 | 172.179 | 67.988 | 0 | 1 |
| corrective shift H1, original | 6606.624 | 172.232 | 68.009 | 0 | 1.000308 |
| physical metric-modulus rates | 2335.076 | 60.874422 | 24.037251 | 0 | 0 |

The large bounds come from composing conservative operator inequalities.
They do not imply exponential growth with these coefficients. The
canonical momentum rates include all components, so their physical
modulus conjugates can still be paired with smooth mean weights; no
momentum partners or symplectic cross terms have been discarded.

## Verification and preserved failed control

[Executable V2](../../../Analysis/MasterTests/test_rtau_initial_gauge_composition_v2.py):
21/21 controls, exact read-only replay COMPLETE.
[Receipt](../../../Analysis/MasterTests/outputs/rtau_initial_gauge_composition_v2_20261103/receipt.json)
SHA256 9d8151f9ee1d458434de39c1a1332c6c8d0a32a6c1d901948f12aad8bf500352.
All 219 inherited source hashes and existing sidecar bytes/timestamps
were preserved. Existing canonical point controls were reused.

The exact composition fixture has nonzero metric-modulus perturbations,
nonconstant background coordinate drift, nonzero modulus rates and
nonzero harmonic coordinate inputs. It verifies the full field Lie
correction, periodicity and the retained constants. Additional exact
tests distinguish scalar field/density pullbacks, retain the canonical
Jacobian in every field/momentum pairing and verify both test-function
chain rules. Same-author controls are not independent external review.

The preserved V1 [source](../../../Analysis/MasterTests/test_rtau_initial_gauge_composition_v1.py)
and [19/20 receipt](../../../Analysis/MasterTests/outputs/rtau_initial_gauge_composition_v1_20261103/receipt.json)
contain the failed generic H2 equality check. Inspection showed equivalent
Derivative/Subs forms did not reduce under simplify alone. Both
expand-then-simplify and doit-then-simplify give exact zero. V2 expands
the exact difference before testing zero and adds an independent
polynomial-composite check. No equation, term, domain or acceptance
criterion was removed; V1 files and sidecars are unchanged.

## Remaining deciding work

The caller-shift row is now closed at the initial weak canonical level.
The density-coordinate TIME row and evolving Green inverse remain open.
Use the existing direct density/current transport identities to compose
the actual density/gauge generator without omitting G_dot or T_dot.
The order-minus-two density block is still a weak symplectic map;
its strong inverse is not assumed.

Then test the physical mixed energy and zero-speed/quartic/subleading
couplings on their actual domain. The current weaker-output estimates
cannot supply that energy, a controlled background tube, nonlinear
preservation or the target [0,.05]. No frozen-chart or continually
projected evolution is substituted. Physical clock flow and both global
charges remain; deferred review does not clear scientific blockers.

No new microscopic match or concrete P1/P2/Thermodynamics/original-R4C1
manuscript defect arose. No paper/site claim update is warranted. Goal
ACTIVE; whole observable-norm bundle and original G1-G6 incomplete.
No action adoption, vault mutation/sync, dispatch, publication, commit,
push or deployment.
