# R4C1-B1G: exact homogeneous background regularity contract

Date: 2026-09-29. Owner: conditional Master Test 1 / R4C1-v1/B1.
This is a bounded continuation of the frozen S4H temporal-persistence
contract, not an alteration of the B1 action, coefficients, initial data or
numerical sample. Rule-9 review is deferred, not cleared.

## Pinned authority and domain

Use the unchanged R4C1 [B1 contract](RES001_R4C1_INTERACTING_BACKGROUND_CONTRACT_2026-09-25.md), [owning report](RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md), executable and S2 polynomial background flow. Verify saved SHA-256 sidecars and transitive pins. Work with the registered positive-root initial H, a=1, u=1, u_dot=0, v=0, v_dot=1, r=1, r_dot=1/4, psi=0, psi_dot=1/5, rho_m=1/5, tau=0, the registered rational parameters, and the requested interval t in [0,4]. Do not infer exact interval properties from the CSV samples. This task concerns the **homogeneous ODE only**, not the full constrained perturbation system or a physical EFT domain.

## Ordered exact proof obligations

1. Reconstruct the exact rational B1 energy E from the action-derived kinetic,
   scalar and portal potentials plus dust. Independently verify its gradients
   against the pinned polynomial flow, M_cos^2=11/10, the positive initial
   energy and H0^2=E0/(3 M_cos^2). All potential terms used in a positivity
   argument must actually be nonnegative for real fields at the registered
   coefficients. A sign conflict rejects the argument.
2. Differentiate the full Friedmann constraint 3 M_cos^2 H^2-E along the
   complete pinned flow. Require exact zero, not a sampled residual. Prove
   the exact energy identity E_dot=-3H(K_s+rho_m). Check the initial
   constraint exactly. If the identity or initial condition fails, do not
   project H onto the constraint or claim regularity.
3. On any local solution, prove a>0, rho_m>0 and C=exp(beta psi)>0 from
   their first-order equations. Use exact charge conservation to show
   J=a^3(u v_dot-v u_dot)=1. Combining positive rho_m with the preserved
   constraint must keep H>0 on the local interval. No numerical sign scan
   can replace this step.
4. For every finite T, derive explicit finite upper bounds from E<=E0 for
   all velocities, amplitudes, rho_m and H; then bound a, psi/C and tau.
   Derive explicit positive lower bounds for rho_m, H and u^2+v^2 over
   [0,T], using J=1 for the last. State their dependence on T and E0.
   Apply the local-Lipschitz ODE continuation theorem to exclude finite-time
   blow-up. If a required state variable or denominator lacks a bound,
   report INCOMPLETE, not GLOBAL_REGULARITY.
5. Specify the resulting nonzero-mode chart domain, including the condition
   p=k/a>=1. Do not convert a formal high-p domain into a physical EFT
   cutoff or claim that the n=1 torus mode satisfies the coarse analytic
   bound. The explicit interval constants for the **perturbation** metric
   and energy rate remain a separate S4H obligation.

Preserve failed attempts; never overwrite prior receipts or run an earlier
receipt-writing main. Record direct/inherited Rule-9 debt and source hashes.
Even if all homogeneous regularity checks pass, `physics_pass=false`,
`gate_effect=NONE`, `Rule9_cleared=false`, and all Master Test 1, Test 2/3,
MAT-001, UVIR-003, Stage 4A, Derived and publication holds remain.
