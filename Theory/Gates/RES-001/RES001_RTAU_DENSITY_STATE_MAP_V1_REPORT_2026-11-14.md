# Initial corrected-density row in the twenty-direction state

Conditional A09.1 result under the
[frozen contract](RES001_RTAU_DENSITY_STATE_MAP_V1_CONTRACT_2026-11-14.md).
The corrected-density row has an exact initial state-map identification
and a bounded material-frame remainder in the registered twenty-direction
L2 norm, with the finite-dimensional partners retained explicitly. This
is a density-row comparison; it does not identify the other nineteen
rows of the actual generator with the principal construction.

## Exact canonical state map

Use the original prepared periodic planar coordinate. The ordinary
configuration/canonical momentum slots, in order, are

    O = (hxx,hxy,hyy,Vx,Vy,Vz,u,v,r) = (0,1,3,6,7,8,9,10,11).

These are the nine slots of the Ward and mixed principal owners.
Let E be their nine-by-eight configuration complement, with first
column (1,0,-1,0,...), second column selecting hxy, and the remaining
six columns selecting Vx,Vy,Vz,u,v,r. Set

    R=(E^T E)^-1 E^T,
    vtrace=(1,0,1,0,...),
    R E=I8, R vtrace=0,
    E R+vtrace vtrace^T/2=I9.

For the actual canonical perturbation define

    phi=R delta q_O,
    Q8=-i D phi,
    P9=delta p_O,
    Y20=(w,Q8,P9,zeta,xi),
    w=delta Sigma-c P xi-alpha D chi,
    zeta=delta Z, xi=delta pi_psi.

The factors of i match the registered Fourier convention D=i k and
X=k delta q. For real fields Q8 is an equivalent complex representation
with the same norm. This definition uses actual derivatives. It does
not impose the leading principal trace graph as an exact constraint.
The trace f and eliminated metric momenta are supplied by the corrected
coupled current/momentum inverse. The force configuration is reconstructed
from the actual auxiliary relation and its retained mean by the corrected
force/metric inverse.

Recover phi=mean(phi)+i P Q8. The eight Q8 components have zero original
coordinate means on the physical gradient domain. Their configuration
means remain separate partners. The free ordinary configuration is
E phi in the O slots, with the three eliminated metric moduli in the
original slots hxz,hyz,hzz. Their initial pullback weights are J,J,J^2,
J=a/mean(a). Retain the force mean, the three eliminated momentum means
and the independent harmonic coordinate velocity. The original weighted
range and total-I/U1 charge conditions restrict admissible tuples of
these variables; this list does not declare new physical freedoms.

## Norm conversion and actual density row

The normalized periodic primitive has L2-to-H1 norm at most sqrt(2).
Since ||E||=sqrt(2),

    ||q_free,ordinary||H1
      <= 2||Q8||L2+sqrt(2)|mean(phi)|+Cmod |metric_moduli|.

On the prepared profiles r=1/13000 gives
Cmod<=exp(4r)*sqrt(1+4r^2)<1.000307752. The free canonical momentum
norm, including xi, is bounded by the corresponding P9/xi subvector of
Y20. If U is the existing nine-input norm sum, these facts imply

    U <= 5||Y20||L2+sqrt(2)|mean(phi)|+Cmod |metric_moduli|
         +|force_mean|+sqrt(3)|eliminated_momentum_means|
         +|harmonic_coordinate_velocity|.

All finite-dimensional norms here are Euclidean. This is an upper bound
on the actual compatible domain, rather than an admission theorem for
arbitrary state/global data. Existing corrected inverses provide the
remaining canonical reconstruction with their domain qualifications.

The complete corrected-density equation is

    w_t=S D w+Rw,

with the original mean commutators and couplings in Rw. The registered
material principal density row is zero. The existing full initial source
receipt bounds Rw by Cw U, with Cw<102112.769724. Therefore the actual
material density row is a bounded L2 remainder with coefficients

| Input | Outward upper bound for ||Rw||L2 |
| --- | --- |
| ||Y20||L2 | 510563.848617 |
| |mean(phi)| | 144409.263835 |
| |metric_moduli| | 102144.195081 |
| |force_mean| | 102112.769724 |
| |eliminated momentum means| | 176864.505263 |
| |harmonic coordinate velocity| | 102112.769724 |

The physical-time transport S D w remains an unbounded differential
term with its natural domain. It is not included in this material
remainder constant. Both ordinary zero-speed directions and the
zeta/xi pair remain among the twenty coordinates.

## Moving map and periodic normal form

E and R are constant slot maps, so phi_t=R delta q_O,t and
Q8_t=-i D R delta q_O,t in distributions. Configuration means and
metric-modulus rates use their actual canonical/gauge owners.
The density time row uses the complete corrected normal-form and
physical-map drift calculations, and the
[assembled trace-source estimate](RES001_RTAU_TRACE_SOURCE_COMPOSITION_V1_REPORT_2026-11-14.md)
controls the differentiated trace reconstruction on compatible initial
jets. The Ward tangency and independent charge partners are retained;
they do not imply finite-time range preservation.

For the existing periodic normal form Z20=T Y20 with T=I+i P S1,
the coefficient template has identically zero density row in S1.
Thus e_w T=e_w, e_w T_z=0 and, along any differentiable admissible
continuation of that template, e_w T_t=0. No numerical rate of the
other S1 entries is needed for this density-row identity. This statement
does not construct that continuation or bound the other transformed
generator rows. It explains why a frozen similarity transform alone
would be insufficient in general, while this particular row has no
normal-form time-drift contribution.

The full periodic inverse bound gives ||Y20||<=2.512053||Z20||. In the
normal-form state the corresponding density remainder coefficient is
below 1282562.991226, with the same explicit global-partner terms.
The physical-time density advection is still S D w.

## Physical density and remaining acceptance requirements

Physical delta rho remains the distinct observable

    delta rho=w+cPxi-(p/mu)xi-p f_ps Dchi+B delta q-bZ zeta.

Its [existing projected equation](RES001_RTAU_PHYSICAL_DENSITY_RATE_V1_REPORT_2026-11-09.md)
retains second derivatives of the force pair, first-derivative ordinary
couplings and coefficient/primitive commutators. In particular the
nonzero coefficient -a_rho d multiplying D^2 zeta is not an L2-bounded
remainder on the energy state. The corrected w coordinate carries the
zero material principal density row. A single numerical total for the
physical-rho remainder was left unevaluated in its owner and is still
an explicit next obligation. That gap prevents treating this component
as completion of every requirement of the wider A09.1 comparison.

The [executable](../../../Analysis/MasterTests/test_rtau_density_state_map_v1.py)
verified 408 source pins and eight controls. Exact complement and
periodic mean/recovery identities, all twenty coordinates, and the
stored principal/normal-form zero rows were checked. The
[receipt](../../../Analysis/MasterTests/outputs/rtau_density_state_map_v1_20261114/receipt.json)
replayed byte for byte. This is same-author provisional evidence.

Next calculate the physical-rho remainder total and audit its domain
and map-drift obligations. Full actual-generator, finite-centre Euler
and evolving energy/domain requirements remain open. R-tau UNADOPTED,
review DEFERRED, Rule9_cleared=false, physics_pass=false, gate_effect=NONE.
