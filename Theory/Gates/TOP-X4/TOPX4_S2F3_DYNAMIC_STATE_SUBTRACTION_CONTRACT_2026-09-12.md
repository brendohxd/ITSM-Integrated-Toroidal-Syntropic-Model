# TOP-X4 X4-S2F3 Dynamic State/Subtraction Contract (2026-09-12)

## Purpose and authority

This contract freezes the next bounded Plan-11 calculation after the finite-charge operator checkpoint. It is subordinate to the recovery-branch core, the X4-S2F3 parent freeze, the A1 action-selection ledger, and the finite-charge variation contract.

The calculation may construct the evolving linear mode system on the already registered A1 background and may test finite-order scalar adiabatic ultraviolet diagnostics. It may not claim a renormalized stress tensor, a physical Hessian, radion stabilization, anomaly clearance, architecture promotion, A4 entry, Ultra entry, or a publication result.

## Frozen background and field definitions

- Background: the A1 zero-winding five-dimensional Einstein plus complex-scalar plus real-scalar-proxy control.
- Metric: `ds_5^2=-dt^2+a(t)^2 d\vec{x}^2+b(t)^2dy^2`, with `y~y+2*pi` and circumference `2*pi*b`.
- Complex scalar: `Phi=(rho/sqrt(2))*exp(i theta)`, `mu=theta_dot`, `h=rho_dot/rho`, `Theta=3H_a+H_b`, and conserved charge `a^3*b*rho^2*mu`.
- Canonical phase fluctuation: `pi=rho*delta_theta`; radial fluctuation: `sigma=delta rho`.
- Comoving mode: `k_n^2=k_obs^2/a^2+n^2/b^2`, with integer `n`.
- Registered numerical interval: `t in [0,1]`; primary grid 1601 points and resolution witness 801 points; DOP853 with `rtol=1e-11`, `atol=1e-13`.
- Registered mode grid: `k_obs in {1,2,4,8,16,32}` and `n in {0,1,2,4}`. The preregistered UV subset is `k_obs>=16`.

## Exact quadratic system to be tested

Per comoving volume, before the volume rescaling, the charged scalar quadratic Lagrangian is

`L_2/A = 1/2 sigma_dot^2 + 1/2(pi_dot-h*pi)^2 + 2*mu*sigma*(pi_dot-h*pi) - 1/2*k_n^2*(sigma^2+pi^2) - 1/2*M_sigma^2*sigma^2`,

where `A=a^3*b` and `M_sigma^2=U_{,rho rho}-mu^2`.

With `v=sqrt(A)*(sigma,pi)^T`, `gamma=Theta/2`, and after removing only explicit total derivatives, the canonical form must be

`L_2 = 1/2 v_dot^T v_dot + mu(v_sigma*v_pi_dot-v_pi*v_sigma_dot) - 1/2 v^T K v`,

with

- `K_ss=k_n^2+M_sigma^2-gamma^2-gamma_dot`,
- `K_pp=k_n^2-gamma^2-gamma_dot-2*h*gamma-h^2-h_dot`,
- `K_sp=K_ps=mu_dot+2*mu*gamma=-2*mu*h` after applying charge conservation.

The exact mode equation must therefore be checked as

`v_ddot+2*mu*J*v_dot+(K+mu_dot*J)*v=0`, with `J=[[0,-1],[1,0]]`.

The constant-background limit must reproduce the prior finite-charge determinant. Omitting the charge mixing or using an incorrect charge-evolution law is a required rejecting mutation.

The real-scalar proxy fluctuation is a separate scalar oscillator with

`Omega_chi^2=k_n^2+m_chi^2+(lambda_chi5/2)*chi^2+(g5/2)*rho^2-gamma_dot-gamma^2`.

The three neutral massive Dirac fields remain spectator operators at this checkpoint. Their spinor transport, normalization, determinant phase, and adiabatic subtraction must not be replaced by scalar WKB formulae.

## State and subtraction declaration

For ultraviolet diagnostics only, define the two frozen-symbol charged-scalar branches from the constant-coefficient determinant evaluated on the evolving background:

`omega_pm^2 = [2*k_n^2+C +/- sqrt(C^2+16*mu^2*k_n^2)]/2`, where `C=M_sigma^2+4*mu^2`.

For each positive scalar branch (including `chi`), define the iterative frequencies

- `W^(0)=omega`,
- `(W^(2))^2=omega^2-(1/2)W^(0)_ddot/W^(0)+(3/4)(W^(0)_dot/W^(0))^2`,
- `(W^(4))^2=omega^2-(1/2)W^(2)_ddot/W^(2)+(3/4)(W^(2)_dot/W^(2))^2`.

The associated finite-order scalar candidate data are

`u=1/sqrt(2W)` and `u_dot=(-iW-W_dot/(2W))*u`.

The scalar branchwise subtraction ingredients are declared as `|u|^2_ad=1/(2W)` and `|u_dot|^2_ad=W/2+W_dot^2/(8W^3)` at orders 0, 2, and 4. These are ultraviolet diagnostics and ingredients only. They are not a covariant five-dimensional `T_AB` subtraction for the coupled scalar-spinor system.

The compactification-sensitive quantity must be formed only after removing the decompactified reference:

`Delta_KK[F] = sum_{n in Z} F(n/b) - b*integral_{-infinity}^{infinity} dp_y F(p_y)`.

No stress integral or KK sum is authorized in this checkpoint.

## Preregistered checks and thresholds

The checkpoint passes only if all of the following hold:

1. Frozen authority sidecars match.
2. Both A1 integrations complete on a finite positive domain and conserve the registered global charge to relative error below `1e-9`.
3. The canonical transformation differs from the unscaled action only by the declared total derivative.
4. The exact canonical equation and the constant-background determinant regression are algebraically exact.
5. Every scalar frequency and every iterated `W^(2)`, `W^(4)` on the registered grid is real and positive over the tested interior interval.
6. For every preregistered UV mode, `max|W^(4)-W^(2)|/W^(2) < max|W^(2)-W^(0)|/W^(0)` separately for each scalar branch.
7. The maximum UV fourth-order correction is below `1e-3`.
8. Primary-versus-witness differences in the reported UV correction envelopes are below `2e-4`.
9. Candidate scalar initial data satisfy the canonical Wronskian to absolute residual below `1e-12`.
10. Omitting finite-charge mixing and mutating the charge law are rejected.
11. The script does not import or relabel the static-vacuum determinant as a dynamic calculation and contains no observational target.

Endpoint derivative points are excluded from the convergence envelope by evaluating the central 90 percent of the interval. This exclusion is numerical, fixed in advance, and does not remove any background or frequency positivity check.

## Status semantics and stop rule

If every registered check passes, the only allowed status is:

`PASS_DYNAMIC_SCALAR_ADIABATIC_UV_HOLD_FULL_STATE_STRESS_AND_HESSIAN`.

Even under that status:

- `physics_pass=false`;
- `gate_effect=NONE`;
- `advance_to_renormalized_stress=false`;
- `advance_to_a4=false`;
- `advance_to_ultra=false`;
- the full X4-S2F3 Hadamard state remains open;
- the Dirac adiabatic state and parity/anomaly audit remain open;
- the covariant five-dimensional subtraction and counterterm map remain open;
- the metric-radion-amplitude-phase constrained Hessian remains open;
- Rule-9 three-way independent clearance remains unmet unless three independent reports are actually attached.

Any failed registered check produces `FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT` and authorizes no continuation.
