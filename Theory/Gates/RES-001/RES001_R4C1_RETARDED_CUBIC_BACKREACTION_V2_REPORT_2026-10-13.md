# R4C1 retarded coupled cubic response and dust-clock timing: V2

Date: 13 October 2026. Owner: Master Test 1 / RES-001 / Stage 2.
Report status: LOCAL_CHECKED_REPLAY_EXACT. The new report sidecar seals this
version after delivery checks; canonical admission is unchanged.

## Result and admission boundary

All 18 registered numerical cases completed, with 1160/1160 local checks,
zero failed/unknown checks, and 577/577 separate read-only provenance,
coverage and dust-clock semantic checks. The exact compiler-only preflight
passed 136/136 controls. These are computational checks, not physical GO.
Full read-only replay recomputed all 18 cases and reproduced all six receipt
files and their sidecars byte-for-byte. Execution and replay exited zero.

The total normalized timing correction grows over the three registered eta
samples in all three families. Including the complete second-order coupled
response did not eliminate this growth. This improves on a contact-only or
fixed-metric warning, but is neither a proved asymptotic law nor a physical
scattering amplitude, strong-coupling cutoff, admitted nonlinear timing
prediction or all-action no-go theorem. The sector decomposition is
chart-dependent; only its total is the declared clock diagnostic.

Stage 1 remains complete only in its registered linear B1 prepared-dust scope.
Stage 2 is INCOMPLETE / STOP_AND_ASSESS_DOMAIN_UNRESOLVED, with the operator's
unchanged-action research continuation active. Stage 3 is NOT_ENTERED:
identifying matter-residue and nonlinear-force matching inputs remain absent.
Rule-9 review is DEFERRED, not cleared. `physics_pass=false`,
`Rule9_cleared=false`, `gate_effect=NONE`. No physical family is admitted.

## Frozen scope and retained sectors

The original scientific contract is
`RES001_R4C1_RETARDED_CUBIC_BACKREACTION_V1_CONTRACT_2026-10-13.md`, SHA
`5d5cd3a16397a33bac46b398ea2987eca96915895305708a0a21c845bf375d94`.
The exact compiler replacement is specified in
`RES001_R4C1_RETARDED_CUBIC_V2_COMPUTE_ADDENDUM_2026-10-13.md`, SHA
`579528e428056db1b59e7f9a737e7285c29f46d82047c3aeafab6f13a06bed45`.

Use the same R4C1 action, three registered families and scalar/background
scalings. These diagnostic choices are not microscopic predictions.
The new grid is eta=1/4,1/64,1/1024; coordinate torus mode k=40;
t in [0,1/20]; W(0)=1 and W_t(0)=0; DOP853 and Radau at each point.
This discrete grid is not an all-sector physical momentum/frequency band.

The evolving mean and 2k responses retain all 22 original field labels,
metric/dust/scalar/frame/regulator/normal/multiplier constraints, affine
source offsets, inverse-constraint drift and basis drift. The full 26+20
reduced response states are evolved, not continually projected onto a slow
graph. The six force-response states and 26 downstream third-response states
give 78 complex states, realified for integration. The third-order result
solves only the sourced transverse coefficient and reconstructs its shift;
it does not claim to solve every third-order field or the full nonlinear
equations. Source-dependent constraints remain present in the prepared data.

The generic planar WWR and intrinsic W4 functional is varied before family
and first-shift specialization. The first-direction variation includes
delta B=sigma delta W, so its source is S_eff=E_W+sigma E_B. The independent
third-order shift reconstruction uses the unreduced source S_B and
S_W=S_eff-sigma S_B; it does not double-count the shift source.
The first frame mass is m_w2, never the a^(3/2)-transformed mass m_X2.
Only the metric/norm second-time derivatives actually required by the
coefficient dependency audit are consumed. Unit norm makes nu identically
zero; unarchived auxiliary accelerations are not invented.

The real force cusp is not Taylor-expanded at Y=0. Its prepared response
has e|e| parity, and the transverse third source is
-6 A |psi_dot|^3 |W| R_c,Vy. Retained odd modes 1,3,5 are multiplied by
|cos(theta)| using its exact infinite Fourier convolution. Analytic contact
sources use an exact eight-angle finite-polynomial Fourier control; that
quadrature is not applied to the cusp. Second and third cusp states are
scaled by eta^(7/2) and eta^7 for numerical precision and restored in
recorded physical coefficients. No action or tolerance is changed.

## Clock definition and numerical results

At theta=0 the prepared reflection symmetries remove longitudinal/x
relative velocity. Dust-clock gauge T=0 gives alpha=-beta Pi at second
order. Choosing N=C_bg/C implements that clock constraint in the unexpanded
truncated geometry. The dust velocity is its ADM normal and its Jordan
proper clock is background tau. Its signed transverse tetrad velocity is
sqrt(h_yy)/a times the transverse chart velocity. The unexpanded geometry is
a control of this truncated configuration, not an exact nonlinear solution.

For the first simple zero t0 of W, the directional root expansion is

```text
t_zero = t0 + |e| t1 + e^2 t2,
t1 = -r_c(t0)/W_t(t0),
t2 = -[w3(t0)+r_c,t(t0)*t1+W_tt(t0)*t1^2/2]/W_t(t0),
tau1 = C_bg*t1,
tau2 = C_bg*t2 + C_bg,t*t1^2/2.
```

The tetrad correction Myy*W/2 vanishes at t0. A local W->W+gamma W^3
coordinate change with the same physical prepared data cannot change this
zero coefficient through that local term. This does not establish general
nonlinear field-redefinition/counterterm equivalence. The initial positive
frame residue is f2=eta/6 in MP2=1 units, and xi=sqrt(f2)*e at a(0)=1.
These units and assumed coefficients are not identifying microscopic matching.
The stored label `tau2_per_xi_squared` denotes d_tau=tau2/f2, the coefficient
multiplying xi^2. It is not division by a particular finite prepared xi^2.

DOP853 values below are reproduced by the independent Radau control:

| Family | eta | d_tau=tau2/f2 | eta*d_tau |
|---|---:|---:|---:|
| G3 | 1/4 | 0.1782112578 | 0.04455281445 |
| G3 | 1/64 | 2.807288956 | 0.04386388994 |
| G3 | 1/1024 | 44.84805457 | 0.04379692829 |
| B1 frame | 1/4 | 0.1132063489 | 0.02830158723 |
| B1 frame | 1/64 | 1.796256837 | 0.02806651307 |
| B1 frame | 1/1024 | 28.71297179 | 0.02804001151 |
| Hierarchical | 1/4 | 0.07557058051 | 0.01889264513 |
| Hierarchical | 1/64 | 1.753740235 | 0.02740219117 |
| Hierarchical | 1/1024 | 28.67008521 | 0.02799813008 |

Near-constant eta*d_tau at the smaller registered eta values is an
observed approximate inverse-eta behaviour, not an imposed acceptance rule
or a derived limiting law. In particular, the hierarchical family has a
substantial change between eta=1/4 and the smaller samples; retain it.
No family was selected using the desired acceleration coefficient or data.

At eta=1/1024, contact/frame/metric contributions to d_tau are respectively
37.98766122/6.857993286/0.002403461475 in G3,
27.30472907/1.404220093/0.004026011914 in B1, and
27.27122997/1.394828916/0.004029704856 in the hierarchical family.
Regulator contributions remain negative and small. Scalar, cusp and root-chain
contributions are retained in the receipts, not set to zero. At eta=1/4 the
hierarchical frame contribution is negative (-0.004480842091), whereas it is
positive at the smaller eta points. No monotonic sector response is imposed.
The split is diagnostic, not a set of independently observable amplitudes.

Maximum normalized two-method disagreement is 1.4524029033396102e-10 for
the new scaled trajectories and 4.4035495564259416e-12 for the clock
coefficients; the frozen threshold is 1e-7. Full 22-field second-order
residuals reach 1.4735896345094886e-12, and unreduced third-vector/shift
residuals reach 4.58678864171037e-16, against a 1e-9 threshold.
Read-only semantic QA gives max |alpha+beta Pi|=3.3881317890172014e-21
at the registered clock-worldline controls, with T and T_t exactly zero.
All 72 sampled negative mean kinetic records are retained; an unreduced
negative matrix entry/eigenvalue is not classified here as a physical ghost.
Two-method agreement is not a certified numerical-mirror error bound.

## Exact-recipe continuous background and linear-zero proof

These mathematical controls apply to 0<eta<=1/4, k=40, t in [0,1/20]
for the approved exact recipe. They do not enclose binary64 seed/solver error
or prove physical admissibility of all Fourier modes.

The positive scalar/reservoir/portal potentials, positive K_Q=3eta and dust
give the exact initial non-frame energy

```text
E0=1/5+65eta/32+13eta^2/168
   +(1/480+3/28+3/50)eta^3 < 3/4.
```

Here K_Q is the conditional action input, not the still-missing canonical
derived K_Q. The M_cos2 coefficients are 1-eta/12 (G3), 1+eta/10 (B1)
and 1+eta/10+eta^2/16 (hierarchical); all lie in [47/48,11/10].
The varied homogeneous action gives E_dot=-3H(kin+rho),
H_dot=-(kin+rho)/(2M_cos2), and preserves 3M_cos2 H^2-E.
While H>=0, E<=E0 and kin+rho<=2E0; hence

```text
1/5 < H0 < 3/5,
|H_dot| <= 36/47,
H(t) >= 1/5-(36/47)t > 0,
1 <= a(t) <= exp(3/100) <= 100/97 < 11/10.
```

The positive margin prevents a first zero of H before T and closes the
bootstrap. Positive dust is preserved by its integrating factor. Potential
bounds control scalar amplitudes/velocities, permitting the background
continuation throughout this interval for each eta>0. This is not a uniform
physical-energy admission at the singular endpoint eta=0.

The phase and charge identities are
[a^3 psi_dot]_dot=-a^3 beta rho/K_Q and
a^3(u v_dot-v u_dot)=eta. Since beta=(2/5)eta^2 and psi_dot(0)=eta/5,

```text
psi_dot >= (eta/5)*(1-9/100)-eta/200 = 177eta/1000,
psi_dot <= eta/5,  J^2 <= eta^2.
```

For all three families, f2=eta/6, cV2>=4/5 and cV2<4/5+3/224<1.
The absolute H_dot coefficient in the frame mass is at most 2;
K_Q/f2=18 and zeta/f2=6/13. Thus
|m_w2|<=72/47+18/25+9/200+3/104<5/2.
With mathematical comparison mu=1 and L=7/4, the damped oscillator norm
obeys (sqrt(E_n))_dot<=L sqrt(E_n)+|F_n|. The zero initial norm is handled
through sqrt(E_n+delta^2), delta down to zero. Since exp(LT)<=80/73,
the unforced first mode satisfies W^2< (121/80)*(80/73)^2 <49/25.
Neither mu nor the potential parameter Lambda is a physical cutoff.

For X=a^(3/2)W, q=cV2*k^2/a^2+m_w2-(3/2)H_dot-(9/4)H^2
exceeds (80/121)*1600-5/2-81/100>32^2, and
0<X_t(0)=(3/2)H0<9/10. While X and
y=cos(32t)+X_t(0)sin(32t)/32 are positive,
(X_t y-X y_t)_t=(32^2-q)Xy<0 implies X<=y.
Consequently the first X zero precedes
(11/7+9/320)/32=3583/71680<1/20, using pi<22/7.
X initially rises because X_t(0)>0. While X>0, X_tt=-qX<0, so X_t decreases
and X has exactly one positive peak before the zero.
After that peak, (X_t^2+32^2X^2)_t=-2(q-32^2)XX_t>=0.
Since X_peak>=1 and a^(3/2)<6/5, |W_t(t0)|>=32/a^(3/2)>25.
This certifies a simple linear zero only, not a nearby exact nonlinear root.

## Infinite force and clock-tail controls

Let B0=1008/228125. The force-amplitude bound is
D=3A|psi_dot|^3 W|W|, with |D|<=42eta^(9/2)/3125;
D_upper*T*exp(LT)/f2<=B0*eta^(7/2).
For positive odd n,
b_n=-8(-1)^((n-1)/2)/[pi n(n^2-4)] and
sqrt(E_n)<=|b_n| B0 eta^(7/2)/2.
Parseval counts both Fourier signs. The tail estimate
sum_odd_n>5 b_n^2/2<=128/(5*pi^2*5^5)<1/1024
gives a continuous tail-energy square-root bound
R5 eta^(7/2), R5=B0/32=63/456250.

The absolute coefficient sum is independently controlled:
sum_odd_n>=3 1/[n(n^2-4)]=1/12 by telescoping the partial fractions
-1/(4n)+1/[8(n-2)]+1/[8(n+2)]. Including n=1 gives
sum_positive_odd |b_n|=10/(3pi)<10/9<25/16.
Therefore both the full pointwise r_c and its velocity are bounded by
R eta^(7/2), with R=(25/16)B0. This is an absolute Fourier estimate;
it is not a claim that an L2 bound alone controls a point value.

The omitted second-response value and velocity at theta=0 satisfy
|delta r_c|<=r_tail eta^(7/2), r_tail=3R5/k, and
|delta r_c,t|<=rd_tail eta^(7/2), rd_tail=(3/50)B0.
The value uses the full gradient norm with Sobolev factor 3/k.
For the velocity, the exact omitted absolute coefficient sum is
sum_odd_n>=7 |b_n|=2/(35pi)<3/50.

Set P=72/625 and G=T exp(LT)<=4/73. The third-force Lipschitz factor
is at most P eta^(7/2). Its omitted-input response satisfies
sqrt(E_third_input_tail)<=G P R5 eta^7 and
|delta w3_input(theta=0)|<=3G P R5 eta^7/k.

For omitted positive odd outputs m>=7 and retained n<=5,
|h_(m-n)|,|h_(m+n)|<=12/m^2. The worst endpoint control is
98/9<12; the required denominator ratio increases for m>=7.
Since sum_retained |r_n|<=R eta^(7/2)/2, the acceleration coefficient is
bounded by 12 P R eta^7/m^2. Applying the same damped Green estimate and
sum_odd_m>5 m^-3<=1/50 yields
|delta w3_output(theta=0)|<=3G P*12R eta^7/(50k).
All infinite sums here are mathematical continuations of the declared
classical operator; they are not admissions of arbitrary physical UV modes.

The clock uses d=25, Cmax=1001/1000 and Cdotmax=1001/800000.
These follow from psi<=eta/100, beta psi<=1/16000 and
C_dot=C beta psi_dot<=C/800. With
w_tail=3G P R5/k+3G P*12R/(50k),

```text
|delta tau1| <= (Cmax*r_tail/d)*eta^(7/2),
|delta tau2| <= {Cmax*[w_tail/d
    +(R*r_tail+rd_tail*R+(9/5)*R*r_tail)/d^2]
    +Cdotmax*R*r_tail/d^2}*eta^7.
```

The 9/5 factor uses W_tt/W_t=-3H at the linear zero. Both the full and
truncated r_c and its velocity obey the same R bound, controlling the
quadratic root-chain difference without an assumed zero cusp.
Exact rational bounds are exported; nextafter-rounded floats display upper
bounds only. At eta=1/4 the raw-coordinate coefficients have tail bounds
3.239537671232877e-9 (tau1) and 2.275362367138388e-12 (tau2).
At eta=1/1024 they are 1.2068218258145739e-17 and 3.1576996117032964e-29.
These bound harmonic omission ONLY for the exact recipe. They do not bound
binary64 integration error, all nonlinear terms or a physical prediction.
For the coefficient multiplying xi^2, divide the tau2 tail by f2. The tiny
high-order harmonic tail is not an accuracy estimate for the whole timing
calculation and must not be substituted for its unproved numerical remainder.

## Provenance, reproducibility and preserved attempts

Executable: `Analysis/MasterTests/test_01_r4c1_retarded_cubic_backreaction_v2.py`,
SHA `760a853d7fa79216286e9751efed3f920a6958a65aefbef8e0c3e63b4b4a5ab3`.
V1 SHA `e0d4de2c9743f72d84aa1e18e8699b1a911fa99a5233b3ef70e0c9944e2b8da9`
and its sidecar remain intact. V1 was deliberately interrupted at the
global-factorization stage, before integration; no complete V1 result,
exception trace or scientific PASS/FAIL receipt is invented. V2 replaces
that implementation with exact product-rule coefficient collection, checked
against direct full unreduced W/B Euler expansion before specialization.
No scientific term, prepared datum, solver tolerance or acceptance rule changed.

Fresh receipts are under
`Analysis/MasterTests/outputs/r4c1_retarded_cubic_backreaction_attempt_02/`:

| Artifact | SHA256 |
|---|---|
| summary.json | 40424d9dca24ff5d6b9107432545b839274b0fa72238256ba4994c71e1522038 |
| formulas.json | aed0e6cc2308c347a164d2a41a796b25fdee6b6ec1d0a2d460f61a5ebc8c3da5 |
| bounds.json | c3fd95730f892c696ba88f6505c7d5af1e93e88f3b3724c53dabfab0732e762f |
| trajectories.json | 40c39678028c3fdc1d42fce9dc96f3132530a470a1a86b71a37f046dcb913107 |
| scope.json | 63ef5b4ad53a916baa027347856f2f86211948e86c763cf9c3ff78b2f2e8f3bc |
| verification.json | 8dfcb2d5d68a5175b9f9a0f70879992dad1b6a1a3794e66ad8731002d4a4142a |

All 271 source pins, 268 available source sidecars and six new artifact
sidecars passed separate read-only QA. Three inherited absent UVIR sidecars
remain explicitly absent, not manufactured. Original source/time failures
remain 958/964 and 10395/10449. The old coupled trajectory retains SHA
`8a3e5df7765aca174b520a53a8a0ca01848941ec34032cba648c3a198ee9320d`.
At eta=1/4 the newly integrated background/coupled response is checked
against that immutable archive at the frozen 1e-7 normalized threshold.

Existing runtime: Python3.13.9, numpy2.4.6, scipy1.17.1, sympy1.14.0;
rtol1e-10, atol1e-12, max_step .001. The inherited compiler binding has
53 controls. Scientific receipt replay recomputed all 18 cases, returned
READ_ONLY_REPLAY_EXACT, and compared every generated artifact/sidecar without
overwriting. Replay is reproducibility evidence, not independent review.
Private output logs and local QA scripts are not publication artifacts.

The owning execution queue and deferred-review register receive append-only
entries. Delivery verified that the queue's original 94302-byte prefix retains
SHA `6049b5e6c8e3e508e719459eb9dfaa47eacefd48e2e783340d5c774425fba818`
and the register's original 167345-byte prefix retains
SHA `ff69a9559eb7013549f677e96a35f89f06541dc6f4c09bb8a1499cbf0e18f9d3`.
The register's seven historical CRLF sequences remain intact. Before editing,
both entire ledgers and their original sidecar bytes were preserved in a
private snapshot. Only these mutable living-index digests are refreshed after
the append; no frozen scientific source, failed attempt, original trajectory
or scientific sidecar is rewritten. These index changes document the result,
not an evidence replacement or promotion.

## Remaining physical decisions and next work

The prior frame/contact warning is no longer unsupported by coupled exchange
in this registered retarded experiment. Nevertheless, extrapolating a physical
cutoff or universal failure from this one preparation would exceed the result.
Before Stage-2 GO, the complete physical-energy/constraint/fixed-charge and
singular/zero-mode treatment, scalar/vector/tensor characteristic and quartic
dispersion domains, controlled finite numerical/nonlinear remainder, full
tensor/local-gravity compatibility and justified GR recovery are still needed.
The shrinking-amplitude interpretation of the sampled normalized coefficient
is a perturbative warning, not an independently admitted frequency window.

Continue only within the operator-approved unchanged-action route. Do not
automatically select TOP-X4, a different parent or a desired acceleration
coefficient. Stage 3 still requires genuine identifying matching, not a residue
computed from assumed coefficients. The native full goal remains ACTIVE and
INCOMPLETE; this bounded diagnostic does not redefine its acceptance.

Register `R9-MT1-RETARDED-CUBIC-V1` with PLANAR-WWR, GR-FAMILY-SURVEY,
THREE-FAMILY-NONANALYTIC-ENTRY, RESPONSE-ENTRY, TIME-RESPONSE, ODD-TAIL,
G3I/G3N4 and all transitive review debt. Review is DEFERRED; this same-source
algebra, two-method control and replay are not independent review clearance.
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
canonical K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
No manuscript/PDF, vault, provider/model/runtime, commit/push or publication
change is included in this checkpoint.
