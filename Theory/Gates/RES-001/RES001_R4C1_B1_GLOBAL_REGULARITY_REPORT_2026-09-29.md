# R4C1-B1G: exact forward regularity of the homogeneous control

Date: 2026-09-29. Owner: conditional Master Test 1 / R4C1-v1/B1.
The [B1G contract](RES001_R4C1_B1_GLOBAL_REGULARITY_CONTRACT_2026-09-29.md) was frozen before this calculation. It retains the original [B1 action-derived equations and inputs](RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md) and the S4H interval obligation. This is a theorem for the **registered classical homogeneous ODE**, not for the inhomogeneous constrained system or a physically calibrated cosmology.

Decision: EXACT_HOMOGENEOUS_FORWARD_REGULARITY for the registered positive-root B1 solution, including the closed interval $[0,4]$. The executable passes 40/40 local algebra and source checks. The conclusion follows from the argument below, not from that count or the 801-point CSV. Physics pass is false, gate effect is NONE, Rule 9 is not cleared, and review remains deferred.

## Exact energy and constraint

At the frozen rational coefficients, put $s=u^2+v^2$, $M_{\rm cos}^2=11/10$, $K=\dot u^2+\dot v^2+\dot r^2+3\dot\psi^2$, and

$$
E=\frac K2+\frac s2+\frac{s^2}{24}+\frac{s^3}{480}
  +r^2+\frac{r^4}{28}+\frac{3sr^2}{28}+\rho_m.
$$

Every displayed potential coefficient is positive; $E\geq\rho_m>0$ for real fields and positive dust. Differentiation through the complete pinned B1 flow gives the exact identities

$$
\frac{dE}{dt}=-3H(K+\rho_m),\qquad
\frac{d}{dt}\left(3M_{\rm cos}^2H^2-E\right)=0.
$$

The independently registered initial values give $E_0=3469/1400$, $H_0^2=3469/4620$, $H_0>0$, and zero initial constraint. No square-root projection or periodic reinsertion of the Friedmann equation is used during evolution. The action-derived scalar gradients, dust equation and $-2M_{\rm cos}^2\dot H=K+\rho_m$ match the pinned polynomial ODE exactly.

The flow also preserves

$$
I_{\rm dust}=\frac{a^3\rho_m}{C}=\frac15,\qquad
J=a^3(u\dot v-v\dot u)=1,\qquad C=e^{(2/5)\psi}.
$$

On any local solution, $a>0$ and $C>0$ follow from their scalar linear equations and positive initial values. Therefore $\rho_m=C/(5a^3)>0$. The preserved constraint then gives $H^2=E/(3M_{\rm cos}^2)>0$; continuity and $H_0>0$ keep $H>0$. Hence $E$ decreases and $0<H\leq H_0$ throughout the local forward solution.

## Explicit finite-time bounds and continuation

For any finite $T\geq0$, define $v_*=\sqrt{2E_0}$ and $w_*=\sqrt{2E_0/3}$. On the local solution for $0\leq t\leq T$:

- $|\dot u|,|\dot v|,|\dot r|\leq v_*$ and $|\dot\psi|\leq w_*$; also $s\leq2E_0$, $|r|\leq\sqrt{E_0}$, $0<\rho_m\leq E_0$.
- $1\leq a\leq e^{H_0T}$, $|\psi|\leq w_*T$, $e^{-(2/5)w_*T}\leq C\leq e^{(2/5)w_*T}$, and $|\tau|\leq T e^{(2/5)w_*T}$ for the registered $\tau(0)=0$.
- The exact dust integral yields

$$
\rho_m\geq\frac15 e^{-[3H_0+(2/5)w_*]T},
\qquad
H\geq\sqrt{\frac{\rho_{m,\min}(T)}{3M_{\rm cos}^2}}>0.
$$

- Cauchy-Schwarz, $J=1$ and $\dot u^2+\dot v^2\leq2E_0$ give

$$
s=u^2+v^2\geq
\frac{e^{-6H_0T}}{2E_0}>0.
$$

The registered autonomous first-order vector field, enlarged by $\dot\psi=p_\psi$ (where $p_\psi=\dot\psi$ is the existing velocity state) and $\dot\tau=C$, is polynomial and thus locally Lipschitz. These bounds cover every state coordinate on each finite forward interval. A finite maximal time would contradict the ODE continuation theorem. The unique exact homogeneous solution therefore exists for all finite $t\geq0$, stays in $a,C,\rho_m,H,s>0$, and in particular qualifies on the requested $[0,4]$ interval. This removes the earlier **background-existence and chart-regularity** uncertainty; the CSV remains a numerical approximation, not the proof.

For the S4F/S4H graph, the separate $p=k/a\geq1$ condition is guaranteed over $[0,T]$ whenever the formal comoving mode satisfies $k\geq e^{H_0T}$. This is a conservative sufficient condition, not a claim about the registered lowest mode or a physical EFT cutoff. Exact interval bounds for the perturbation metric $M(t,p)$, its upper graph equivalence and its energy-rate constant have **not** been calculated from these background bounds.

## Provenance and unchanged holds

The [executable](../../../Analysis/MasterTests/test_01_r4c1_b1_global_regularity.py) SHA-256 is 85c65db213eacc6806fc5ee370311790fad3987896143b4119ec8168b27eb17d. The non-overwriting [attempt-01 summary](../../../Analysis/MasterTests/outputs/r4c1_b1_global_regularity_attempt_01/summary.json) SHA-256 is f28578a16cda58f907e5c8af97023aedfb818919b2eff131a70dbaf70f767caa; its [detail](../../../Analysis/MasterTests/outputs/r4c1_b1_global_regularity_attempt_01/detail.json) SHA-256 is ccdcc3d375067ca03821e5b9d038bf45e5f500f7056c545fd92798bb65392560. Seven direct input hashes and all three output/source sidecars were rechecked without mismatch. Earlier B1 and S4H receipts were not overwritten.

The proof is restricted to the specified positive-parameter, zero-spatial-winding classical homogeneous B1 control. It does not bound the inhomogeneous constraints, singular or zero modes, full perturbation transfer, GR limit, semiclassical regime, physical cutoff, weak-field law or acceleration coefficient. The next S4H task is to turn the now-rigorous background bounds into **explicit uniform** projector/metric and energy constants over $[0,4]$ on a declared formal $p$ domain, then address the remaining physical and parent gates. Test 1 and Tests 2/3 remain incomplete; MAT-001 BLOCKED, UVIR-003 IN_PROGRESS, K_Q NOT_DERIVED, V NOT_COMPUTED, Stage 4A CLOSED, and publication hold unchanged. R9-MT1-B1G and inherited reviews are deferred, not cleared.
