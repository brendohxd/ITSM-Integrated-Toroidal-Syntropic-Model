# R4C1-S4H-U: explicit uniform formal energy envelope on B1

Date: 2026-09-29. Owner: conditional Master Test 1 / R4C1-v1/B1.
The [S4H-U contract](RES001_R4C1_S4H_UNIFORM_ENVELOPE_CONTRACT_2026-09-29.md)
was frozen before this calculation. It continues the unchanged
[S4H temporal-persistence contract](RES001_R4C1_TEMPORAL_PERSISTENCE_CONTRACT_2026-09-29.md),
the [exact moving-symbol report](RES001_R4C1_S4H_MOVING_SYMBOL_REPORT_2026-09-29.md)
and the [B1G homogeneous regularity proof](RES001_R4C1_B1_GLOBAL_REGULARITY_REPORT_2026-09-29.md).

**Decision:** An explicit finite-time energy estimate exists for the
registered reduced regular B1 nonzero-mode graph on a declared **formal**
high-$p$ domain. This is a conditional mathematical result, not a physical
stability or Master Test-1 pass. The final executable passes 1093/1093
local checks, including five positive/rejection controls.
physics_pass=false, gate_effect=NONE, Rule9_cleared=false and
review_status=DEFERRED remain binding.

## Rational enclosure of the exact B1 interval

The B1G identities give $E_0=3469/1400$, $H_0^2=3469/4620$,
$M_{\rm cos}^2=11/10$, decreasing positive energy, a conserved dust
integral and nonzero angular charge. The rational bound $e<11/4$ follows
from the series through $1/4!$ and a geometric upper bound $1/100$ on
the remaining tail. Exact integer comparisons establish
$(11/4)^4<60$, $(11/4)^{16}<10^8$ and $(11/4)^{24}<10^{11}$.
Using the B1G inequalities for every $t\in[0,4]$, this yields the
deliberately coarse enclosing box

| Quantity | Certified enclosure |
|---|---|
| $H$ | $10^{-5}\leq H\leq1$ |
| $s=u^2+v^2$ | $10^{-12}\leq s\leq5$ |
| $\rho_m$ | $10^{-9}\leq\rho_m\leq3$ |
| $a$ and $C$ | $1\leq a\leq60$; $1/60\leq C\leq60$ |
| amplitudes/velocities | $|u|,|v|,|\dot u|,|\dot v|,|\dot r|\leq3$; $|r|,|\dot\psi|\leq2$ |

For example, the dust integral gives
$\rho_m>1/[5(11/4)^{16}]>10^{-9}$, so the exact Friedmann
constraint implies $H^2>10^{-10}$. The charge bound gives
$s>1/[5(11/4)^{24}]>10^{-12}$. These are interval statements
from the exact ODE, not extrema sampled from the B1 CSV.

## Certified rational-envelope construction

The executable reconstructs the complete moving $12$-by-$12$
generator $C(t,p)$ with fixed comoving $k$ and $p=k/a$, and reloads
the pinned $C_2,C_1,M_0,M_1$. It rechecks exactly

\[
M_0C_2+C_2^{T}M_0=0,\qquad
M_0C_1+C_1^{T}M_0+M_1C_2+C_2^{T}M_1=0.
\]

For every nonzero entry of $M_0,M_1,C_1,\dot M_0,\dot M_1$ and
$R=C-p^2C_2-pC_1$, it cancels the rational expression, factors its
denominator and bounds every numerator monomial with exact algebraic
coefficient ceilings and the box above. The only certified denominator
classes encountered are $H$, $s$, $s+13$, $3s+26$, $p$ and
$p^2+S$, with

\[
S=396H^2+18\dot\psi^2
  +6(\dot r^2+\dot u^2+\dot v^2)\geq0.
\]

Every numerator's $p$-degree is at most its certified denominator
$p$-degree, so the same entry bound holds for **all** $p\geq1$.
An unrecognized pole, an excessive $p$-degree or an undeclared free
symbol is rejected rather than numerically sampled. Full B1-flow
derivatives are retained. The resulting Frobenius upper bounds are

| Matrix | Uniform Frobenius bound on the box, $p\geq1$ |
|---|---:|
| $M_0$ | $B_0=10^{40}$ |
| $M_1$ | $B_1=10^{13}$ |
| $C_1$ | $B_{C1}=10^6$ |
| $\dot M_0$ | $B_{\dot0}=10^{61}$ |
| $\dot M_1$ | $B_{\dot1}=10^{20}$ |
| $R$ | $B_R=10^{12}$ |

The earlier exact projector identity gives $M_0\succeq I/4$.
Set $p_0=8B_1=8\times10^{13}$. For every $t\in[0,4]$ and
$p\geq p_0$, the moving metric $M=M_0+M_1/p$ obeys the explicit
graph bounds

\[
\frac18 I\preceq M(t,p)
 \preceq\left(10^{40}+\frac18\right)I .
\]

The B1 vector field is polynomial and its exact regular solution is
smooth. Every metric denominator is uniformly separated from zero on
this box, so $M(t,k/a(t))$ is smooth for each admitted fixed $k$.
These are equivalence bounds in the inherited S4F graph-weighted
selected chart, not a statement across its singular-chart boundaries.

Since $\dot p=-Hp$, the exact energy-rate identity after the two
principal cancellations is

\[
\begin{split}
\mathcal E={}&M_0R+R^TM_0+M_1C_1+C_1^TM_1+\dot M_0\\
&+\frac{M_1R+R^TM_1+\dot M_1+HM_1}{p}.
\end{split}
\]

The matrix-norm bounds and $H\leq1$ yield

\[
\|\mathcal E\|_2\leq
2B_0B_R+2B_1B_{C1}+B_{\dot0}
+\frac{2B_1B_R+B_{\dot1}+B_1}{p_0}
=B_{\mathcal E},
\qquad 8B_{\mathcal E}<10^{62}.
\]

Consequently, for a solution of this reduced moving linear system,
$\mathscr E=z^TMz$ satisfies
$\dot{\mathscr E}\leq10^{62}\mathscr E$ and hence
$\mathscr E(t)\leq e^{10^{62}t}\mathscr E(0)$ on $[0,4]$.
This estimate is rigorous but extraordinarily loose.

To retain $p=k/a\geq p_0$ over the interval using $a\leq60$,
it suffices to take $k\geq4.8\times10^{15}$. For axial torus
modes $k=2\pi|n|$, the still more conservative sufficient integer
condition is $|n|\geq8\times10^{14}$. These conditions define a
nonempty **formal** mode set. No action-derived EFT cutoff has been
computed, so whether it contains even one **physical** mode is unknown.

## Verification, failures and unchanged gates

Attempt 01 stopped before calculation because its script contained
one mistyped expected digest for the pinned S4H energy-detail JSON;
the mismatch was detected and that failed receipt is preserved.
Attempt 02 established the constants with 1088/1088 local checks.
Attempt 03 added two positive and three negative envelope controls,
reproduced the same constants byte-for-byte at the result-field level,
and passes 1093/1093 checks with zero failed or unknown checks.
Its 81 recorded source pins and their sidecars were independently
rechecked against live files with zero mismatches; the final script
and two JSON artifact sidecars also match.

The final [executable](../../../Analysis/MasterTests/test_01_r4c1_s4h_uniform_envelope.py)
SHA-256 is
719bc8b03e42da1c65e7095cf1c62f0dc42ec8a9741495fee686971308d17cd4.
The [attempt-03 summary](../../../Analysis/MasterTests/outputs/r4c1_s4h_uniform_attempt_03/summary.json)
SHA-256 is
23ef971f2a708e8dcccb6f609767a6d680fcc24adf45a9bd243043193817b2b0;
its [detail](../../../Analysis/MasterTests/outputs/r4c1_s4h_uniform_attempt_03/detail.json)
SHA-256 is
335e65ea235503849f0cf347ae898b9226149f99216fa66a9b8f5a862819a370.
Prior B1 and S4H receipts were not overwritten.

This completes the **formal interval-envelope obligation** for the
registered reduced regular B1 graph only. It does not prove propagation
of the full constrained initial-value problem, singular/zero modes,
wider phase cones, all-sector causality/stability, a physically usable
high-$p$ window, healthy GR recovery, canonical action acceptance,
weak-field closure, a blind $a_0$ coefficient or empirical prediction.
The next scientific question is whether a physical EFT range overlaps
this formal bound, or whether a sharper admissible estimate exists,
followed by the full constrained-system and GR-limit requirements.
Master Tests 1-3 remain incomplete; MAT-001 BLOCKED, UVIR-003
IN_PROGRESS, $K_Q$ NOT_DERIVED, $V$ NOT_COMPUTED, Stage 4A CLOSED,
Rule-9 review deferred and publication on hold.
