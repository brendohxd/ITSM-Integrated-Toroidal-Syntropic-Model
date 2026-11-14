# R-tau weighted range and charge tangency on the prepared first jet

The [frozen calculation](RES001_RTAU_WARD_RANGE_RATE_V1_CONTRACT_2026-11-09.md)
identifies the weighted longitudinal compatibility rate with a weak
pairing of the actual spatial Ward identity. On an exact constrained
canonical Euler/auxiliary first jet this rate vanishes. At a finite
prepared centre the background residual produces a separate, bounded
scalar forcing from the total shift perturbation. Both integrated
charge rates also vanish under the exact Euler/auxiliary hypotheses.

## The compatibility rate is a residual pairing

Use the original circle mean $\langle\cdot\rangle$ and $D=\partial_z$.
The [periodic canonical inverse](RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_REPORT_2026-11-01.md)
and [moving range owner](RES001_RTAU_MOVING_RANGE_V1_REPORT_2026-11-03.md)
use the longitudinal source $s_L$, trace $f$, background trace momentum
$P_{\rm tr}$ and

$$
 \omega=\frac1{2a},\quad
 R=\frac{(Da)P_{\rm tr}-aDP_{\rm tr}}2,\quad
 F=Rf+\omega s_L,\quad c=\langle F\rangle.
$$

Writing $\delta C_L$ for the canonical longitudinal residual, the
integrating factor gives $\omega\delta C_L=D W-F$, with
$W=a\delta p_{e,L}-aP_{\rm tr}f/2$. Thus
$c=-\langle\omega\delta C_L\rangle$ for any data in the initial
decomposition. The projected solve has $D W=F-c$ and hence
$\delta C_L=-c/\omega$. The transverse residuals vanish on the
projected solve with their periodic source means satisfied. Neither
operation prescribes the physical momentum means.

Differentiate on the prepared first jet, with $L=a_t/a$ and
$\omega_t=-L\omega$. The conformal metric and its conformal first
derivative justify this pairing and its first derivative. The moving
free-field and gauge contributions are part of the actual source
$s_{L,t}$. The relation is

$$
 \dot c=-\langle\omega\,\delta\dot C_L+\omega_t\,\delta C_L\rangle.
$$

The weight and its derivatives are smooth. The pairing is also valid
with the weak source-rate order from the
[canonical rate owner](RES001_RTAU_WEAK_CANONICAL_RATE_V2_REPORT_2026-11-03.md).
This derivation differentiates the residual identity along the actual
canonical rates. It does not assume that the evolved state was
continually projected onto the initial inverse's range.

## Ward substitution and finite-centre term

The [current transport owner](RES001_R4C1_RTAU_CURRENT_TRANSPORT_V2_REPORT_2026-11-01.md)
gives $\delta\dot C=\mathcal L_S\delta C+\mathcal L_{\delta S}C$ when
the full canonical Euler and auxiliary equations are used. For any
planar shift $v$, $(\mathcal L_v C)_L=D(v^z C_L)+\sum_i C_i Dv^i$.
For projected initial data substitute $\delta C_L=-c/\omega$ and
retain the index term. Integrating the periodic shift derivative
gives the scalar equation at that instant

$$
 \dot c=\langle-L+S^z D\log a\rangle\,c+\mathcal E,\qquad
 \mathcal E=\left\langle\delta S^z(D\omega)C_L+
                         \sum_i\delta S^iD(\omega C_i)\right\rangle.
$$

This includes all components of the total perturbation shift, including
any coordinate correction. The finite-centre term requires only its
$L^2$ norm because integration by parts moves the derivative onto the
smooth background coefficient. The transverse source means and their
derivatives follow directly from their periodic derivative form.

Using the actual first action differentials and spatial jets on the
whole root ball gives

$$
 |\mathcal E|\le0.004801\,\|\delta S\|_{L^2},\qquad
 \langle-L+S^zD\log a\rangle\in[-0.866836,-0.866214].
$$

The former is a conservative coefficient enclosure, with no assigned
value for the actual shift perturbation. The latter is an initial
compatibility coefficient. It carries no finite-time damping or
physical stability conclusion. At an exact constrained background
$C=0$ and for a compatible initial perturbation $c=0$, so $\dot c=0$.
For general approximate initial data the residual contribution must
be retained and the Ward equation still requires its stated rate
hypotheses.

## Charge and gauge boundaries

The same current owner gives $\delta\dot I=D(S^z\delta I+I\delta S^z+
\delta\mathcal F^z)$ and a periodic divergence for the phase-charge
rate. Testing these distributional divergences against the constant
function yields zero integrated rates. Here $I$ is the actual total
current. No fixed compensated-density charge, phase quotient or time
quotient is used. This establishes the scalar tangency conditions for
an exact compatible Euler/auxiliary jet. It does not construct the
differentiated trace inverse, solve for the dynamical mean and gauge
rates or show that the candidate admits a compatible trajectory.

The [V2 executable](../../../Analysis/MasterTests/test_rtau_ward_range_rate_v2.py)
checked 388 source pins and 10/10 controls. The
[receipt](../../../Analysis/MasterTests/outputs/rtau_ward_range_rate_v2_20261109/receipt.json)
replayed byte for byte. The [V1 exact-expression comparison failure](RES001_RTAU_WARD_RANGE_RATE_V1_FAILURE_2026-11-09.md)
is preserved. The next A09.1 calculation is the actual differentiated
projected trace equation and rate reconstruction, using the scalar
tangency identities in their declared scope. R-tau unadopted, review
DEFERRED, physics_pass=false, gate_effect=NONE.
