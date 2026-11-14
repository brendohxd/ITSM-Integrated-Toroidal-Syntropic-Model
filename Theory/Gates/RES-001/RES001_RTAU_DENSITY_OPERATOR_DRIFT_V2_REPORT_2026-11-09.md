# Initial R-tau density operator row and observable coefficient drift

This initial-slice result follows the [component contract](RES001_RTAU_DENSITY_OPERATOR_DRIFT_V1_CONTRACT_2026-11-09.md).
The [corrected-density owner](RES001_RTAU_ACTUAL_CORRECTED_DENSITY_V1_REPORT_2026-11-05.md)
supplies the initial source and corrected lifts. The
[periodic principal owner](RES001_RTAU_PERIODIC_PRINCIPAL_COMPOSITION_V2_REPORT_2026-11-04.md)
uses $Y_{20}=(w,Q_8,P_9,\zeta,\xi)$ in ordinary/force block order.

## Density row

In the original periodic chart, $D=\partial_z$, $P=D^{-1}P_0$ and
$w=\delta\Sigma-cP\xi-\alpha D\chi$. The corrected-density owner's full
row is $(\partial_t-SD)w=\mathcal R_w$. Its $D\zeta$ and $D\delta p$ terms
cancel using $a=cd$ and $A_p=N\alpha$. The primitive produces
$c[\langle S\xi\rangle-S\langle\xi\rangle]-c\langle d_z\zeta\rangle$
as well as the retained $P_0$ and $P$ source terms. Physical-time transport
$SDw$ remains in the actual operator.

The registered mixed principal operator has zero material $w$ row.
The periodic principal change $T=I+iPS_1$ has $e_w^*S_1=0$, giving
$e_w^*T=e_w^*$ on the whole circle. The comparison uses the existing
initial $\|\mathcal R_w\|_{L^2}\le102113\,U$ bound in the compatible
norm, including the independent harmonic coordinate velocity. Both
zero-speed coordinates and both fast directions are retained.

## Explicit observable coefficient drift

$$
 \delta\rho=w+cP\xi-\frac p\mu\xi-pf_{ps}D\chi
            +\sum_i B_i\delta q_i-bZ\zeta,
 \qquad B_i=f_{q_i}+pf_p\frac{\mu_{q_i}}\mu .
$$

The $q_i$ partials fix $p,s$. At fixed original coordinate, $P$ is
time independent. Holding the unreduced arguments fixed gives the coefficient
rates $c_t,-(p/\mu)_t,-(pf_{ps})_t,(B_i)_t,-bZ_t$. The calculation uses
actual initial field rates and an action-derived enclosing normal $p_t$
interval. The generic force partials use the certified positive value
interval for $Y$ and the first derivative of the full metric contraction
of the rest-space force vector. Metric and frame dependence are retained.

On the registered conformal initial first jet write $h_t=2Lh$,
$s=\psi_z$, $\kappa=a^{-2}$ and $\lambda=\log a$. Then
$Z_t=2LZ-\kappa[(\psi_t)_{zz}+\lambda_z(\psi_t)_z+L_zs]$.

With the corrected compatible lifts the resulting bound is
$\|\dot R_{\mathrm{coeff}}X\|_{L^2}\le89U_8$, where $U_8$ sums the eight
original strong/global input norms. The largest per-input upper enclosure
is below 88.516. The reconstructed arguments carry separate rates with
their own Sobolev order.

## Moving compatible maps

For differentiable inverse data $LG=Q$, $GL=P_{\mathrm d}$ with
$P_{\mathrm d}G=G=GQ$, differentiation gives

$$
 \dot G=-G\dot L G+G\dot Q+\dot P_{\mathrm d}G.
$$

The domain projector $P_{\mathrm d}$ differs from the periodic primitive.
For $s=Qs$, $G\dot Qs=0$, while the domain term can remain. The compatible
solution rate is $\dot x=G(\dot s-\dot Lx)+\dot P_{\mathrm d}x$ with
$(I-Q)\dot s=\dot Qs$. An exact rank-one control verifies the identity and
detects dropping the domain term. The actual reconstructed source and
charge/gauge transport still need derivative-order estimates.

The [V2 executable](../../../Analysis/MasterTests/test_rtau_density_operator_drift_v2.py)
verified 386 pins, 9/9 local checks and byte-identical replay of the
[receipt](../../../Analysis/MasterTests/outputs/rtau_density_operator_drift_v2_20261109/receipt.json).
The [V1 arithmetic failure](RES001_RTAU_DENSITY_OPERATOR_DRIFT_V1_FAILURE_2026-11-09.md)
is preserved. A09.1 remains open for the actual moving reconstruction.
R-tau unadopted, review DEFERRED, physics_pass=false, gate_effect=NONE.
