# Initial R-tau trace response to force and frame momentum rates

This component follows the [trace rate contract](RES001_RTAU_TRACE_GREEN_RATE_V1_CONTRACT_2026-11-09.md)
and [moving momentum lift](RES001_RTAU_MOVING_MOMENTUM_RATE_V1_REPORT_2026-11-09.md).
It uses the prepared initial chart and the corrected Sigma trace operator
$L_\Sigma=A_2D^2+A_1D+K$, with $A_2=-Na$ and $D=\partial_z$. The
[corrected lift](RES001_RTAU_SIGMA_RECONSTRUCTION_REPAIR_V1_REPORT_2026-11-04.md)
controls the original projected inverse $G_1:H^{-1}\to H^1$ with its
nonzero mean block. $K$ includes the nonlocal momentum reconstruction.

## Isolated longitudinal force term

Write the unreduced trace constraint with eliminated momenta on the left
as a sum of differential trace terms minus $\sum_i v_i^{\rm mat}\delta p_{e,i}$.
After differentiating, retain the terms linear in the trace rate in the
left operator. The part of the differentiated longitudinal relative
momentum lift independent of the trace rate adds
$mD\zeta$ to the right, with $m=v_{h_{zz}}^{\rm mat}u_L(D\psi)d$.
Here $v_{h_{zz}}^{\rm mat}=(q_t-\mathcal L_Sq)_{h_{zz}}$ comes from the
prepared metric and shift. The source has this plus sign because the
momentum term was on the left with a minus sign. The finite-rank
normalization and other moving-source terms from the momentum lift
remain in the source remainder.

For periodic tests, $\langle mD\zeta,v\rangle=-\langle\zeta,D(mv)\rangle$,
so $\|mD\zeta\|_{H^{-1}}\le(\|m\|_\infty+\|Dm\|_\infty)\|\zeta\|_{L^2}$.
Applying $G_1$ therefore controls both the isolated trace response in
$H^1$ and its gradient in $L^2$. This is how the actual trace equation
absorbs the isolated longitudinal derivative.

## Rough projected trace inverse

Let $r=A_2^{-1}$, $J=(1-D^2)^{-1}$ and $E=-Jr$. Then
$A_2(D^2-1)E=I$ in distributions on the entire circle and

$$
 L_\Sigma E-I=(A_1D+K+A_2)E,\qquad
 G_2=E-G_1(L_\Sigma E-I).
$$

Multiplication by $r$ is bounded on $H^{-2}$ by duality with $H^2$.
In the registered Bessel norm it is bounded by
$e=\|r\|_\infty+2\|Dr\|_\infty+\|D^2r\|_\infty$, using the product
rule with the norm $\|v\|_{H^2}^2=\|v\|^2+2\|Dv\|^2+\|D^2v\|^2$.
The residual factor from $L^2$ to $H^{-1}$ is bounded by
$\ell=\|A_1\|_\infty+\|DA_1\|_\infty+\|K\|_{L^2\to L^2}+\|A_2\|_\infty$.
Thus $G_2:H^{-2}\to L^2$ has norm at most $e(1+\|G_1\|\ell)$.
For uniqueness, a homogeneous $L^2$ solution satisfies
$f=-E(A_1D+K+A_2)f\in H^1$. The existing inverse then gives $f=0$.
On $H^{-1}$ inputs this extension agrees with $G_1$. The construction
inverts the projected trace equation, including its mean. Full spatial
compatibility and both charges still constrain the physical input.

## Frame-rate trace gradient

Put $C=N\gamma/a^2$ and $v=\delta p_{V^z,t}$. The rough source
$D(Cv)$ is in $H^{-2}$ when $v\in H^{-1}$. With
$f_v=G_2D(Cv)$, divide the trace equation by $A_2$ and integrate using
$P=D^{-1}P_0$:

$$
 Df_v-rCv=
 -P\big[(Dr)Cv+rA_1Df_v+rKf_v\big]-\langle rCv\rangle.
$$

In particular $rC=-\gamma/a^3$ is the same leading frame coefficient
as in the initial trace-gradient lift. The weighted mean is retained
as an $H^{-1}$ dual pairing. With $C_1=\|C\|_\infty+\|DC\|_\infty$,
$F=\|G_2\|C_1$ and $\|P\|_{H^{-1}\to L^2}\le 2$, the displayed
gradient remainder is bounded by
$e(3C_1+2\ell F)\|v\|_{H^{-1}}$. This separates the potentially rough
leading term from the bounded remainder for the actual frame input
coefficient.

## Certified initial constants

Sixteen circle cells each retain the full registered root uncertainty.
The coefficient derivatives are evaluated with first action differentials
and spatial Taylor jets. The $A_1$ value and its compensation agree
with the pinned interval enclosures on every cell. These overlap tests
are consistency checks on the analytic coefficient formulas.

| Operator or response | Outward upper bound |
| --- | --- |
| Projected trace inverse $H^{-1}\to H^1$ | 2.614835 |
| Projected trace inverse $H^{-2}\to L^2$ | 9.979373 |
| Trace $H^1$ from the isolated longitudinal term per $\|\zeta\|_{L^2}$ | 0.0002287 |
| Trace $L^2$ from $D(Cv)$ per $\|v\|_{H^{-1}}$ | 9.982011 |
| Gradient remainder $L^2$ after subtracting $-\gamma v/a^3$, per $\|v\|_{H^{-1}}$ | 71.556011 |

The [V3 executable](../../../Analysis/MasterTests/test_rtau_trace_green_rate_v3.py)
checks the pinned inputs, original mean block, exact parametrix algebra
and periodic coefficient product rule. The
[receipt](../../../Analysis/MasterTests/outputs/rtau_trace_green_rate_v3_20261109/receipt.json)
contains 40/40 checks and all 387 source pins were verified. The read-only
replay returned byte-identical receipt bytes.
The [V1 execution disposition](RES001_RTAU_TRACE_GREEN_RATE_V1_ATTEMPT_2026-11-09.md)
and [V2 receipt construction failure](RES001_RTAU_TRACE_GREEN_RATE_V2_FAILURE_2026-11-09.md)
preserve the earlier attempts.

## Remaining moving equation

At the initial slice the differentiated projected equation has the form
$L_\Sigma f_t=D(Cv)+mD\zeta+\mathcal S_{\rm rest}-\dot L_\Sigma f$,
where $\mathcal S_{\rm rest}$ includes the differentiated density and
force-clock terms, the derivative of the frame source coefficient, the
moving momentum normalization, and gauge/modulus and charge partners.
These are separate from the two responses controlled here. The actual
operator drift and the remaining source rates and their compatibility
must still be assembled. This result supplies the weak trace mapping
needed to do that on the prepared slice. A09.1 stays open. R-tau unadopted,
review DEFERRED, physics_pass=false, gate_effect=NONE.
