# R4C1: complete cusp-order response in explicit mixed and weak norms

17 October 2026. Master Test 1 / RES-001 / unchanged-action Stage 2.
Claim: Conditional. Main V3 local validation 354/354; companion 45/45.
Both immutable read-only replays passed, including hash/size/mtime preservation.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result and exact limits

The full order-|e|^3 source, constraint reduction and forced response now have
explicit continuous-time estimates in the registered planar, fixed-case
scope. These include the infinite even-mode tail, the retained m=+-2 pair,
the separate mean chart and reconstruction of all 22 field equations.
This advances beyond the earlier lower transverse response alone.

This is NOT a controlled all-order nonlinear remainder or a physical validity
window. Some reconstructed constraint fields are bounded only in negative
spatial Sobolev norms. Constants are very conservative; no useful accuracy,
positive canonical energy, physical cutoff or healthy GR limit is admitted.
LambdaU_dot is not bounded: the zero LambdaU velocity slot in the Euler
reconstruction is unused, not a physical prediction of zero time derivative.

Domain: the unchanged generic 22-field action; archived_G3, new_B1_frame and
new_hierarchical, each at eta=1/4,1/64,1/1024; the registered regular background
and leading w(t) cos(40z) preparation on the coordinate 2*pi torus;
0<=t<=1/20. Output k=(0,0,40m), m even. Zero is treated separately.
The estimate is not an all-direction, arbitrary-background, continuous-eta,
eta=0 endpoint or arbitrary-amplitude theorem.

All order-three states and sources below are normalized by
s_eta=eta^(7/2), as in the parent cusp evolution. The lower odd coefficients
are the directional e|e| response; this does not revive the rejected ordinary
cubic Taylor vertex at the cusp. The original nonanalytic interaction remains.

## Complete source and exact identities

For every even output m, the seven inputs are

~~~text
[r_(m-1)/s_eta, r_dot_(m-1)/s_eta,
 r_(m+1)/s_eta, r_dot_(m+1)/s_eta, c_(m-1), c_(m+1), h_m].

c_n = -4 sin(n*pi/2)/[pi*n*(n^2-4)]            (signed odd n),
h_m = 12 (-1)^(m/2)/[pi*(m^2-1)*(m^2-9)].

h_m = (c_(m-1)+c_(m+1))/2,
m*h_m = (3/2)*(c_(m-1)-c_(m+1)).
~~~

The full 27-by-7 matrix is exported: 22 Euler sources, the time derivative
of the lapse source, and the four auxiliary-source derivatives. The generic
61-coefficient WWR polarization, forced lower accelerations/third derivatives,
the direct |cos|^3 source and evolving background/momentum drift all remain.
Both temporal and longitudinal source Ward identities are verified exactly,
including every free lower-state column and the direct/forced convolution
terms. No division by w is used at a leading-wave zero.

The same cosine/complex Fourier convention is retained. In particular,
c_1=h_0=4/(3*pi), c_3=4/(15*pi), h_2=4/(5*pi). Cosine amplitudes are not
substituted for these complex Fourier coefficients.

## Action-derived coupled reduction

Each exact parameter case is substituted into the UNSPECIALIZED Hessian
before reduction. No B1-specialized operator receives new coefficients.
With F the physical embedding, U the auxiliary embedding, and V=U^dagger LB F,

~~~text
K = F^dagger LK F - V^dagger D_inverse V,
u_source = -U D_inverse S_aux,
u_source_dot = -U (D_inverse_dot S_aux + D_inverse S_aux_dot),
f_acc = K^(-1) F^dagger (S + EA u_source + EB u_source_dot).
~~~

The nonzero chart keeps ten complex coordinates/twenty evolution states.
The mean keeps thirteen coordinates/twenty-six states and only its regular Z
auxiliary inverse. Its six metric coordinates remain; no 1/m expression is
evaluated on that chart. The inherited charge-compatible mean preparation is
checked against both archived methods in every case. Nonzero free order-three
initial data are zero; their sourced auxiliaries and density are not deleted.

For the mean, r_-1=r_1 and their velocities agree for all time: their real
linear equations and zero initial data agree. Its spatially odd shift sources
therefore average to zero. The temporal source identity preserves the remaining
mean constraint with the inherited initial charge preparation. A homogeneous
fixed-both-charge condition is not imposed locally on nonzero modes.

All 22 reconstructed Euler equations are checked, including density,
multiplier and auxiliary equations, not merely the reduced accelerations.
The density-rate and auxiliary drifts are retained. The generic Hessian
contains no LambdaU time-jet term; no actual LambdaU_dot conclusion follows
from choosing zero in that unused Euler-velocity slot.

## Continuous bound, including the infinite tail

Reuse the complete LOW-RANK-WEIGHTED-EVOLUTION-V2 map and positive norm:

~~~text
z_m = Tw (I+U_fast/ell)^(-1) B_balance SO2^dagger (y_m,y_dot_m),
E_m = z_m^dagger Q z_m,  Q>=I/10,  ell=40m.
~~~

Every balance, fast/wave map, source and background derivative remains.
The complete Schur denominator is d=1-g/ell^2>=1, not the rejected cubic
inverse. Source-to-acceleration, weighted forcing and full reconstruction
matrices are exported coefficientwise. Their actual Laurent powers determine
the estimates; no desired decay order is imposed.

The continuous background box is inherited from its proved energy/dust/clock
balances, not sampled extrema:

~~~text
1<=a<=20/19, 1/5<=H<=1,
|u|,|u_dot|,|v|,|v_dot|,|r|,|r_dot|<=2,
eta/10<=psi_dot<=eta/5, 1/6<=rho<=1/4, 1<=C<=250/249.
~~~

For the leading wave, the inherited joint energy bounds give |mV2|<9 and
40 sqrt(cV2)/a>12. Its positive energy without a mass term obeys the
conservative Ew_dot<=8Ew, giving |w|<=25/19 and |w_dot|<=50<205/4.
The companion independently verifies these outward constants.

Let P=45/10108. The lower bound gives
|r_n_dot|/s_eta<=P|c_n| and
|r_n|/s_eta<=P|c_n|/(12|n|).
The first new output m=4 includes n=3: an n>=4 coefficient estimate must NOT
be applied to it. The companion instead proves, for all odd |n|>=3,

~~~text
|c_n| <= 36/[5*pi*|n|^3],
36/(5*n^3)-4/[n*(n^2-4)]
 = 16*(n^2-9)/[5*n^3*(n^2-4)] >= 0.
~~~

Together with |m+-1|>=3|m|/4 and pi>3, this proves the existing V3 seven-input
majorants on |m|>=4:

~~~text
[ (64P/27)|m|^-4, (128P/9)|m|^-3,
  (64P/27)|m|^-4, (128P/9)|m|^-3,
  (128/9)|m|^-3, (128/9)|m|^-3, (1024/105)|m|^-4 ].
~~~

Exact outward rational interval arithmetic bounds every complete forcing
coefficient on this box. For each of the nine cases it yields a finite
rational C_j and the inherited rational mu_j such that

~~~text
||f_m||_Q <= C_j/|m|,
sqrt(E_m(t)) <= C_j*t*exp(mu_j*t/2)/|m|
             <= C_j*exp(mu_j/40)/(20|m|).

sup_(0<=t<=1/20) sum_(|m|>N, m even) |m|^(2s) E_m(t)
 <= (C_j^2/200)*exp(mu_j/20)*N^(2s-1)/(1-2s),
N integer >=4, s<1/2.
~~~

This is a conservative bound, not a sharp asymptotic response law.
The signed-mode estimate uses absolute Laurent powers/reality and the same
positive Schur denominator. The sum over all integers bounds the even subset.
No finite-mode scan supplies the all-mode integral comparison.

The retained m=+-2 pair receives its own explicit continuous forcing constant
from the complete numerator at ell=80, not from a sampled trajectory. Its
seven input bounds are [P/27,4P/9,P/405,4P/45,4/9,4/45,4/15].
The companion exports its full weighted estimate and all field/Euler-velocity
reconstructions in every case.

For the mean, exact outward row sums provide finite rational G_j, M_j, Y_j:

~~~text
||Y_mean(t)||_inf <= exp(G_j/20)*(Y_j+M_j/20).
~~~

Here G_j bounds its full 26-state generator, M_j its full forcing, and Y_j
the inherited initial state. All rational values, source maps, field bounds
and exponential expressions are in the case receipts. There is no use of a
nonzero-mode inverse, positive canonical-energy assertion or sampled maximum.

## Regularity wall: why this does not admit a physical window

The worst common sufficient bounds for nonzero reconstructed fields are:

| Component | Spatial H^s range supported by this bound |
| --- | --- |
| Metric/scalar/transverse fields and lapse (nonzero-chart entries) | s<3/2 |
| Longitudinal frame Vz, shift Sz and regulator Z | s<1/2 |
| Density Em and multiplier LambdaU | s<-1/2 |
| Ordinary dynamical velocities | s<1/2 |
| Density velocity | s<-1/2 |
| Regulator velocity | s<-3/2 |

Some gauge/symmetry entries vanish and some families have stronger zero
entries. The complete row-by-row statements remain in the exports. The
LambdaU velocity slot is unused; an actual derivative bound is NOT admitted.
These are sufficient estimates, not claims that the true response saturates
them, is singular, or cannot have better regularity.

In particular this does not control all fields as ordinary pointwise-small
classical perturbations, or close the nonlinear products needed for an
all-order error theorem. The inherited mu_j factors are also enormous.
Large majorants do not show observed growth or physical instability; they
fail to certify useful accuracy. Neither a potential parameter nor a vacuum
probe threshold is identified with a physical cutoff.

The next scientific requirement is a useful finite-amplitude constrained
remainder/interaction estimate in an appropriate physical norm and domain.
It must address this derivative/constraint regularity loss and physical
energy/ensemble interpretation, not repeat the completed finite-mode fits.
The singular eta=0, negative homogeneous trace energy, wave-scale Jordan
warning, retarded timing and nonmonotonic complementary findings remain.

## Independent controls and preservation

Main V3: all nine cases, 354/354 local checks, no failures/unknowns.
There are 2646 full-action comparisons over all 378 unchanged background
nodes and output m=0,2,4,6,8,12,32, plus 63 leading-wave-zero probes.
All 756 retained mean/first-even source comparisons remain compatible with
their original receipts. Independent angular convolution controls use
8192 periodic points at three unchanged nodes per case, all seven outputs.
No new time integration or target data are used.

| Control | Largest normalized residual | Frozen limit |
| --- | ---: | ---: |
| Complete forcing | 3.450833082106672e-16 | 1e-9 |
| Auxiliary reconstruction | 5.419679046604451e-20 | 1e-9 |
| Auxiliary drift | 3.452120832583336e-18 | 1e-9 |
| Full generator | 3.2455154071045936e-16 | 1e-9 |
| All 22 equations | 7.660883145668331e-13 | 1e-9 |
| Retained source comparisons | 1.6553796869408876e-16 | 1e-9 |
| Independent periodic convolution | 2.007811473815384e-15 | 1e-9 |
| Wave-zero equations/forcing/drift | 4.881107284266039e-16 | 1e-9 |

The constant/retained-pair companion passes 45/45 analytical/provenance checks.
Both full packages replayed exactly, preserving every artifact hash, size and
mtime. Main V3 verifies 440 source pins/877 metadata records. Three inherited
absent sidecars remain explicit; their source bytes are still hash-pinned.
Same-agent independent computations are not independent peer review.

V1 and V2 failed attempts remain unchanged and both replayed exactly as failed.
V1 was 13/17: an ordinary transpose was used instead of the conjugate transpose
in the new implementation's complex kinetic Schur term. Its exact acceleration
rejection had residual -78961/1152 in flattened entries 0,2,20,22.
V2 was 23/26: a combined numerical function evaluated the nonzero inverse at
m=0 before selecting the already-separate mean result. V3 selects a distinct
mean function BEFORE evaluation. Neither error was repaired in the parent
action, independent reducer, old results or failed receipts.

## Reproduction and sealed artifacts

Contracts: CUSP3_COUPLED_TAIL_V1_CONTRACT, V2_CONJUGATION_ADDENDUM,
V3_ZERO_CHART_ADDENDUM and CONSTANTS_V1_ADDENDUM, all 17 October 2026.

~~~text
python -B Analysis/MasterTests/test_01_r4c1_cusp3_coupled_tail_v3.py \
  --replay Analysis/MasterTests/outputs/r4c1_cusp3_coupled_tail_attempt_03
python -B Analysis/MasterTests/test_01_r4c1_cusp3_coupled_constants_v1.py --replay
~~~

Main full replay ended normally with READ_ONLY_REPLAY_EXACT, exit0.
The companion also ended with READ_ONLY_REPLAY_EXACT, exit0.

| Artifact | SHA-256 |
| --- | --- |
| V3 executable | 4753b2a55745ef774e310853ed866575d821a0aeebfe8485c9887af0ecd3efc2 |
| Main attempt03 summary | a9645d8477a2693514181be81df293360f22b37ec6574701f9b6c5898c30012c |
| Constant/retained-pair executable | 03dfe68d53ae896589767cbd7a7f47564e9ae0b8f6853a2aafc5ba4b9c96d59c |
| Companion attempt01 summary | ae576de4b785e0f66bc29d4fdea01925b2113742b266ceddbf6374f28f3ec87a |
| Failed V1 attempt01 summary | cf7c7ecfb63ddf738833b7392b57074edf40c5047b30710c10d134063619692a |
| Failed V2 attempt02 summary | f7e6bd2c1909e29fbc84b7670dc0954b9e04315785341d0e3c2f9470e8b9c1e5 |

## Deferred review and programme disposition

R9-MT1-CUSP3-COUPLED-TAIL-V3, including the constant/retained-pair companion:
provisional reuse is supported ONLY within the fixed-case, prepared planar
order-three mixed/weak-norm scope above. No substantive blocker remains for
that bounded estimate. Its weak regularity, huge constants, missing useful
all-order remainder and physical energy/domain interpretation block stronger
physical uses. Review DEFERRED, not cleared.

Inherit LOW-RANK-WEIGHTED-EVOLUTION-V2, CUSP-ODD-RESPONSE-TAIL-V1 and its root
audit, CUSP3-EVOLUTION-V1, THREE-FAMILY-FINITE-K-V3, homogeneous fixed-charge
kinetic V3, generic action/evolving reduction and all transitive review debt.

Stage1 complete only in its registered linear B1 dust scope. Stage2 INCOMPLETE,
no physical family GO; Stage3 NOT_ENTERED. Tests1-3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 UNCHANGED. The diagnostic K_Q=3eta and background
potential are inputs, not the missing microscopic matching calculations.
Actual matching of matter residue and nonlinear force normalization remains
necessary before any genuinely theory-fixed numerical weak-field prediction.

Native full goal ACTIVE/incomplete. No manuscript/PDF, website, vault mutation,
publication/submission, commit/push, paid provider dispatch or model/runtime/
security configuration change is included.
