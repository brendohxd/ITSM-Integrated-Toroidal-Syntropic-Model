# R4C1-S4H continuation: exact moving symbol, pointwise formal metric

Date: 2026-09-29. Owner: Master Test 1 / conditional R4C1-v1/B1.
This is the next ordered calculation under the [frozen S4H contract](RES001_R4C1_TEMPORAL_PERSISTENCE_CONTRACT_2026-09-29.md), following its [chart and sampled-reconstruction report](RES001_R4C1_TEMPORAL_PERSISTENCE_REPORT_2026-09-29.md). No action, B1 inputs, chart rows, tolerance, or canonical gate was changed. The previous report remains valid as an account of its own initial screen; its then-open exact-principal task is addressed here only within the scope below.

**Decision:** `POINTWISE_FORMAL_HIGH_P_ENERGY_RATE` for the conditional regular B1 scalar graph; `INCOMPLETE_TEMPORAL_PERSISTENCE` for the full S4H contract. `physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`, `review_status=DEFERRED`. This is neither a finite-time constrained-IVP theorem nor a physical stability claim.

## Exact moving principal result

The executable forms the full moving chart from the pinned sixteen-row graph, its derivative, the S2 generator, the exact original-to-canonical transformation, and fixed comoving $k$. It reconstructs $C=D(F_{,t}+FA)_{\mathrm{ROWS}}T^{-1}D^{-1}+\dot D D^{-1}$, with $p=k/a$ and $\dot p=-Hp$, then extracts all 144 entries of $C_2,C_1$ by exact large-$p$ limits. The 16-by-12 graph identity and both S4G initial-event principal matrices replay exactly. The previous 24-sample high-precision check is a separate numerical diagnostic, not the proof of these limits.

For the registered regular chart,

\[
C(t,p)=p^2C_2+pC_1(t)+R(t,p),\qquad p\geq1.
\]

$C_2$ is the constant skew block on selected coordinates $P=\{6,7\}$:

\[
C_2[P,P]=\frac{\sqrt{165}}{33}
\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]

Every other entry of $C_2$ is zero. The projected slow block $A=C_1[K,K]$, $K=\{0,\ldots,11\}\setminus P$, has the **exact symbolic registered-B1-state** characteristic polynomial

\[
\chi_A(\lambda)=\frac{\lambda^2(\lambda^2+1)^2
(3\lambda^2+1)(13\lambda^2+13+u^2+v^2)}{39}.
\]

The polynomial obtained by removing the repeated $(\lambda^2+1)$ factor annihilates $A$ exactly; deleting any of its four factors does not. The B1 flow conserves

\[
J=a^3(u\dot v-v\dot u),\qquad \dot J=0,\qquad J(0)=1.
\]

On **any finite regular exact continuation** from that initial state, $u^2+v^2>0$. Thus the slow squared frequencies $1,\ 1/3,\ 1+(u^2+v^2)/13$ are strictly positive and distinct, and the zero eigenspace is semisimple. The 801-point B1 CSV alone did not prove interval existence; the subsequent [B1G exact homogeneous proof](RES001_R4C1_B1_GLOBAL_REGULARITY_REPORT_2026-09-29.md) now supplies it for the registered solution on $[0,4]$. The $u=v=0$ collision is explicitly excluded, not silently regularized.

## Pointwise metric and energy statement

On the real regular domain $a,H,C,\rho_m>0$, $u^2+v^2>0$, $k\ne0$, $p\geq1$, the four polynomial projectors of $A^2$ at eigenvalues $0,-1,-1/3,-[1+(u^2+v^2)/13]$ resolve the identity, are idempotent and mutually annihilating. The zero projector is killed by $A$. Their sum-of-squares metric $G$, constructed as in S4G but with moving coefficients, satisfies $A^TG+GA=0$ and $G\succeq I/4$ exactly. The observed denominator factors of $G$ and the corrected metric are $H$, $u^2+v^2$, $u^2+v^2+13$, and $3(u^2+v^2)+26$; all are nonzero on that domain.

Embed $G$ and $I_P$ into $M_0(t)$. With $S_1=M_0C_1+C_1^TM_0$ and $J_P=C_2[P,P]$, set the $K/P$ block of symmetric $M_1(t)$ to $-S_1[K,P]J_P^{-1}$, its transpose on $P/K$, and zero diagonal blocks. The full exact checks give

\[
M_0C_2+C_2^TM_0=0,\qquad
M_0C_1+C_1^TM_0+M_1C_2+C_2^TM_1=0.
\]

For each fixed regular state, $M=M_0+M_1/p\succeq I/8$ if $p\geq\max\{1,8\lVert M_1\rVert_F\}$; this threshold has **not** been bounded uniformly in time. The script differentiates every $M_0,M_1$ entry through the complete registered B1 flow and retains

\[
\dot M=\dot M_0+\frac{\dot M_1+HM_1}{p}
\]

for fixed comoving $k$. All 144 rational remainders $R$ have finite $p\to\infty$ limits. The only $p$-dependent denominator factors found in the full $C$ are $p$ and

\[
p^2+396H^2+18\dot\psi^2
  +6(\dot r^2+\dot u^2+\dot v^2),
\]

which do not vanish for real regular states and $p\geq1$. Consequently $MC+C^TM+\dot M=O(1)$ as $p\to\infty$ **at each fixed regular state**. This is a formal high-frequency statement; the physical EFT range of $p$ is unknown.

## Integrity, limitations and next gate

The four fresh non-overwriting attempt-01 runs pass, respectively, 278/278 exact principal, 193/193 spectral, 212/212 projector/metric, and 573/573 rational-remainder/flow checks. The final summary's 75 recorded input hashes were rechecked independently against live files and sidecars: 0 mismatches. All four current executables and eight generated JSON artifacts match their SHA-256 sidecars. A local PASS count does not confer physics closure or independent review.

| Calculation | Executable SHA-256 | Summary SHA-256 | Detail SHA-256 |
|---|---|---|---|
| [Moving principal](../../../Analysis/MasterTests/test_01_r4c1_moving_principal.py) | `060adab2d7928c1ba072617796145d19a9a5f2943685829a69a4529dbcc10ccb` | `79fdd57fb6f8f6682c40f9ea066b3f91a067ee8ec54397542100b21fa214352a` | `3dfe9b891844738312b0957da0ef4e23aec53aaf32a204cb26e0514d4770e635` |
| [Moving spectrum](../../../Analysis/MasterTests/test_01_r4c1_moving_spectrum.py) | `369677a86adf1856e00e30f61f8e3256dd2d54034e172b653dfa7474e6d10aab` | `a5abe1959655e4b278ffbd6282dfa3d8ef9e455297a485d49a10445292f78cca` | `52d633f5ac456b6790cceb2d65dab14d59cb2d5107c2313fa5429e76e872db42` |
| [Moving metric](../../../Analysis/MasterTests/test_01_r4c1_moving_metric.py) | `15dc947f35e9d3b03049bba4352a1e5c47b34bf12edc77d3c5252d33a683c3cf` | `f4ccfbb01969d848bc5390da5cd7008e4fd5ce14e2d2ef7109156189291e0020` | `c743348c84385ecd576d3a196f7e37f843d72ee2654b50d94deebf99611086a5` |
| [Moving energy](../../../Analysis/MasterTests/test_01_r4c1_moving_energy.py) | `53530ef536f9724833a79263c26130173bfcbcc8bc87b53fca3c151b7edaf059` | `402b9fc09f018d7a99872cfd4de3a3428f35324d51c70ff5604edce6281faabc` | `5d5e0fc8e065988c7d85bf98dfaa25c968f20975e6046071d1962625f3ea2c3a` |

The remaining S4H decision is **not** review-only. The separate B1G proof now establishes exact homogeneous background existence and regular chart conditions on $[0,4]$. Still required are explicit uniform lower/upper graph and metric constants, a uniform energy-rate constant and an allowed physical $p$-range; then constraint propagation, singular/zero modes, all sectors, healthy GR recovery and action acceptance need separate gates. Compactness of the proven regular interval yields abstract finite extrema, but not the frozen contract's explicit perturbation constants. No Test 1, Test 2/3, MAT-001, UVIR-003, Stage 4A, Derived or publication promotion follows. R9-MT1-S4H-MOVING, R9-MT1-B1G and inherited reviews remain deferred.
