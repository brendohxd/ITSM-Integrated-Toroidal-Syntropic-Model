# Initial R-tau momentum means, gauge moduli and direct trace rate

The [frozen calculation](RES001_RTAU_GAUGE_MEAN_TRACE_RATE_V1_CONTRACT_2026-11-09.md)
supplies the actual canonical rates of the three retained eliminated
momentum means on the prepared initial slice. It also bounds the direct
metric trace rate, corrective shift and three metric-modulus rates in the
corrected compatible norm. This gives the rate data against which to test
the independently differentiated projected trace equation.

## Actual canonical means

Use original periodic coordinates, $D=\partial_z$, and the retained
canonical means $\eta_j=\langle\delta p_j\rangle$ for
$j=h_{xz},h_{yz},h_{zz}$. In the affine original-coordinate decomposition
the corrective shift is initially zero. The corresponding Euler
momentum rate is $\delta L_{q_j}^{(0)}-D(\delta L_{q_{j,z}}^{(0)})$.
The flux has zero periodic mean, including distributional derivatives.
This formula includes the full auxiliary field dependence of the action.
For $H$ the registered mixed Hessian the mean of the first term is
evaluated with the configuration, velocity and gradient columns,
the $H_{j,13}\zeta$ contribution, and
$\langle H_{j,41}D\zeta\rangle=-\langle (DH_{j,41})\zeta\rangle$.
The auxiliary velocity column is absent. No derivative of an arbitrary
$L^2$ auxiliary field is required for the mean.

Let $\sigma$ be the actual periodic corrective shift pulled back from
the adapted chart, with the independent harmonic velocities retained.
The [paired gauge owner](RES001_RTAU_PAIRED_GAUGE_RATE_V2_REPORT_2026-11-04.md)
gives its dual canonical response

$$
 \delta p_{j,t}^{\rm gauge}=
 D(\sigma^z p_j)-\sum_i K_{ij}D\sigma^i,\qquad
 K_{ij}=(\partial_{q_j}B_i)^T p .
$$

The first term integrates to zero, but the metric index term generally
does not. Differentiation of the actual metric generator gives

$$
\begin{aligned}
 \dot\eta_x&=\langle\delta L_{h_{xz}}^{(0)}
       -2p_{h_{zz}}D\sigma^x-p_{h_{xz}}D\sigma^z\rangle,\\
 \dot\eta_y&=\langle\delta L_{h_{yz}}^{(0)}
       -2p_{h_{zz}}D\sigma^y-p_{h_{yz}}D\sigma^z\rangle,\\
 \dot\eta_L&=\langle\delta L_{h_{zz}}^{(0)}
       -2p_{h_{zz}}D\sigma^z\rangle.
\end{aligned}
$$

These are dynamical rates. They cannot be set to zero by choosing a
periodic antiderivative. For example the transverse index term can
have a nonzero mean with a varying longitudinal metric momentum.

## Moving coordinate weight and direct trace

The [initial gauge composition](RES001_RTAU_INITIAL_GAUGE_COMPOSITION_V2_REPORT_2026-11-03.md)
determines $\sigma$ and the metric-modulus rates from its periodic
weighted solve. For the canonical momentum in adapted coordinates,
$\delta\bar p_j=\delta p_j/(J T_{q,j})$, so the original mean is
$\eta_j=\langle T_{q,j}\delta\bar p_j\rangle_{\bar z}$.
Its derivative in that representation includes both
$T_{q,j}\partial_t\delta\bar p_j$ and
$(\partial_t T_{q,j})_{\bar z}\delta\bar p_j$.
For the selected metric slots the field weights are
$J^{-1},J^{-1},J^{-2}$. The original-coordinate calculation above
evaluates the same mean without replacing the adapted weight by a
constant or introducing an adapted momentum mean as an extra charge.

The background metric has the registered conformal first jet,
$L=a_t/a$. The physical metric trace coordinate
$f=(\delta h_{xx}+\delta h_{yy})/(2a^2)$ therefore obeys

$$
 f_t=\frac{\delta\dot h_{xx}^{\,\rm corrected}
                 +\delta\dot h_{yy}^{\,\rm corrected}}{2a^2}-2Lf.
$$

The field rates are the gauge-closed canonical rates in the original
chart. This formula includes the moving scale and provides a direct
weak trace rate without imposing future conformality.

## Quantitative initial bounds

The calculation composes the corrected configuration and momentum
lifts, the affine Hessian rows and the original corrective shift map.
It uses the gauge owner's bounds before its older weak-graph input
composition. The nine input coefficients retain the independent
harmonic coordinate velocity. If $U$ is the sum of those norms,
outward rounded constants multiplying $U$ are:

| Output | Upper bound per $U$ |
| --- | ---: |
| $\lvert\dot\eta_x\rvert$ | 26272 |
| $\lvert\dot\eta_y\rvert$ | 26273 |
| $\lvert\dot\eta_L\rvert$ | 25240 |
| $\|f_t\|_{L^2}$ | 203916 |
| $\|\sigma\|_{H^1}$ | 11408 |
| Metric-modulus rate vector norm | 4032 |

These conservative bounds are in the original prepared benchmark's
norm conventions. The [V2 executable](../../../Analysis/MasterTests/test_rtau_gauge_mean_trace_rate_v2.py)
verified 388 source pins and 12/12 local checks. The
[receipt](../../../Analysis/MasterTests/outputs/rtau_gauge_mean_trace_rate_v2_20261109/receipt.json)
replayed byte for byte. The [V1 preflight failure](RES001_RTAU_GAUGE_MEAN_TRACE_RATE_V1_FAILURE_2026-11-09.md)
is preserved. The next step is to differentiate the actual projected
trace equation with these mean and gauge rates, then compare its solution
with the direct $f_t$ above on the compatible first jet. The evolving
inverse and finite-time domain remain open. R-tau unadopted, review
DEFERRED, physics_pass=false, gate_effect=NONE.
