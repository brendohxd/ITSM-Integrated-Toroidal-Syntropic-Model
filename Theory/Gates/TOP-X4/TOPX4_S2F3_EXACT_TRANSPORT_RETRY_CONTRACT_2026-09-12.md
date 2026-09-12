# TOP-X4 X4-S2F3 Exact-Transport Retry Contract (2026-09-12)

## 1. Purpose and relation to the failed checkpoint

This contract freezes one bounded follow-up to
`FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT`. It does not alter, supersede, or
retroactively pass that negative result. The failed branchwise fourth-order
WKB state remains rejected over its complete registered grid.

The retry asks a narrower question: can the registered A1 background support
finite, canonically normalized exact transport of all scalar modes, including
the low modes for which the local WKB iterate failed, together with a distinct
finite-order Dirac state construction?

The calculation may establish an exact scalar symplectic transport and an
exact Dirac unitary transport. It may not claim a full Hadamard state,
state-order convergence sufficient for renormalization, a covariant
five-dimensional stress subtraction, a semiclassical background, a physical
Hessian, radion stabilization, parity/anomaly clearance, A4 entry, Ultra
entry, phenomenology, architecture promotion, or publication readiness.

## 2. Frozen background, grid, dimensions, and initial surface

- Background: the registered A1 zero-winding finite-charge control on
  `t in [0,1]`.
- Primary background grid: 801 points; resolution witness: 401 points.
- Integrator: DOP853 with background `rtol=1e-11`, `atol=1e-13` and transport
  `rtol=1e-10`, `atol=1e-12`.
- Mode grid: `k_obs in {1,2,4,8,16,32}` and `n in {0,1,2,4}`.
- UV trend sequence: `k_obs in {8,16,32}`, evaluated separately at every
  registered `n`.
- Cauchy surface: the original A1 initial surface `t_*=0`. It is not shifted
  away from the prior failure.
- Equal-mass Dirac control: `N_F=3`, `m_F=sqrt(m_phi_squared)=1` in the
  registered dimensionless A1 units. This is not an absolute mass prediction.

Five-dimensional natural-unit dimensions are

`[rho]=[sigma]=[pi]=3/2`, `[Psi]=2`, `[k_obs/a]=[n/b]=[mu]=[m_F]=1`,
`[K]=2`, `[H_D]=1`, and `[P_+]=0`. Scale factors are dimensionless. No new
dimensionful coefficient is introduced.

## 3. Charged-scalar Hamiltonian and exact transport

Use the exact canonical system already derived from the frozen action. With
`v=(v_sigma,v_pi)^T`, `p=v_dot+mu*J*v`, and
`J=[[0,-1],[1,0]]`, define

`H_2=1/2 (p-mu*J*v)^T(p-mu*J*v)+1/2 v^T K v`.

For `z=(v,p)^T`, this is `H_2=1/2 z^T G z`, where

`G=[[K+mu^2 I, mu J],[-mu J,I]]`.

With the canonical symplectic matrix
`Omega=[[0,I],[-I,0]]`, exact transport obeys

`z_dot=A_s z`, `A_s=Omega G`.

At `t_*=0`, take the two eigenvectors of `A_s` with eigenvalues of negative
imaginary part and normalize the mode matrix `F` so that

`i F^dagger Omega F=I` and `F^T Omega F=0`.

The exact fundamental matrix `S_s` obeys `S_s_dot=A_s S_s`, `S_s(0)=I`.
This low-mode prescription uses no scalar WKB iterate. It is an instantaneous
positive-Hamiltonian quasifree candidate followed by exact transport, not a
Hadamard or renormalized-stress claim.

The real-scalar proxy is transported independently with

`u_ddot+Omega_chi^2 u=0`,

using normalized positive-frequency data at `t_*=0`. Its canonical Wronskian
must be preserved by exact transport.

## 4. Separate Dirac state construction

After the spin-connection-removing rescaling
`Psi_c=(a^3 b)^(1/2) Psi`, each neutral spectator obeys

`i d_t Psi_c=H_D Psi_c`,

with

`H_D=alpha_1*k_obs/a+alpha_4*n/b+beta*m_F`.

The five Hermitian matrices `alpha_1,...,alpha_4,beta` must square to the
identity and mutually anticommute. The instantaneous positive-energy
projector is

`P=(I+H_D/omega)/2`,

where `omega^2=k_obs^2/a^2+n^2/b^2+m_F^2`.

Define the first-order superadiabatic correction

`P_1=-(i/(2 omega))[P_dot,P]`, `S=[P_1,P]`,

and retract it to an exact rank-two projector,

`P_ad1=exp(S) P exp(-S)`.

This retraction preserves the first-order expansion while making Hermiticity
and idempotency exact up to numerical precision. The two-dimensional range of
`P_ad1(0)` is then evolved with the exact Dirac equation. The construction is
finite order. It is not an infinite-order Dirac adiabatic state and therefore
does not establish the Hadamard condition or authorize point-split stress
renormalization.

The method follows the distinction between scalar and spinor adiabatic
constructions emphasized by Barbero et al.,
[`arXiv:1805.05107`](https://arxiv.org/abs/1805.05107), and the infinite-order
Hadamard boundary for Dirac states described by Hollands,
[`gr-qc/9906076`](https://arxiv.org/abs/gr-qc/9906076). The coupled-scalar
initial-surface hazard remains visible in Baacke and Kevlishvili,
[`arXiv:0910.1128`](https://arxiv.org/abs/0910.1128).

## 5. Preregistered checks

The bounded checkpoint passes only if all checks below pass on both the
primary and resolution-witness grids where applicable:

1. Every frozen authority sidecar matches, including the prior failed
   contract, output, and receipt.
2. The prior status remains exactly
   `FAIL_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT`, with 11/12 checks and the same
   three failed low-mode branch combinations.
3. The dimension ledger above is encoded without any observational target or
   absolute-mass claim.
4. Hamilton's equations generated by `G` reproduce the exact charged-scalar
   second-order equation, and the constant-background symplectic eigenvalues
   reproduce the prior charged branches.
5. `K` and `G` are positive definite for every registered scalar mode and
   sampled time. This is a state-existence control, not a coupled-gravity
   Hessian.
6. Initial charged-scalar mode normalization and isotropy residuals are below
   `1e-12`.
7. Charged-scalar exact transport preserves `S_s^T Omega S_s=Omega`,
   `iF^dagger Omega F=I`, and `F^T Omega F=0` to maximum Frobenius residual
   below `5e-8`.
8. Every real-scalar frequency remains positive, and its exact transport
   preserves the canonical Wronskian below `5e-8`.
9. All scalar modes, including the three previously failed low-mode
   combinations, remain finite under exact transport.
10. For each `n`, final charged-scalar and real-scalar instantaneous-basis
    mixing decreases strictly along `k_obs=8,16,32`. This is a UV trend only,
    not a convergence proof to infinite adiabatic order.
11. The five Dirac Clifford matrices are Hermitian and obey their Clifford
    algebra to residual below `1e-14`; every `H_D` is Hermitian.
12. Every `P_ad1(0)` is Hermitian, rank two, and idempotent to residual below
    `1e-12`.
13. For every registered mode, the first-order projector reduces the local
    invariance defect relative to `P`; the maximum ratio must be below `0.25`.
    `P_ad1_dot` at the initial boundary is evaluated with the fixed five-point
    forward derivative on each registered grid.
14. Exact Dirac transport preserves the two-state inner-product matrix below
    `5e-8`, and its final instantaneous negative-energy leakage is finite.
15. For each `n`, final Dirac leakage decreases strictly along
    `k_obs=8,16,32`.
16. Static-background scalar and Dirac controls produce mixing/leakage below
    `1e-10`.
17. Primary-versus-witness differences in the maximum normalization residuals
    and UV endpoint-mixing envelopes are below `2e-5`.
18. Wrong scalar symplectic sign, broken Dirac Clifford sign, scalar-WKB reuse,
    static-vacuum reuse, and observational-target mutations are rejected.

The thresholds are numerical and method-level. They are not fitted to an
observational value or stabilization target.

## 6. Status semantics and stop rule

If all checks pass, the only permitted status is

`PASS_EXACT_SCALAR_DIRAC_TRANSPORT_HOLD_HADAMARD_STRESS_AND_HESSIAN`.

That status means only that a finite, normalized exact transport exists for
the tested scalar and Dirac candidate data. It must retain:

- `physics_pass=false`;
- `gate_effect=NONE`;
- `full_Hadamard_state=false`;
- `covariant_5D_subtraction=NOT_DERIVED`;
- `renormalized_stress=NOT_COMPUTED`;
- `advance_to_semiclassical_background=false`;
- `advance_to_hessian=false`;
- `advance_to_a4=false`;
- `advance_to_ultra=false`.

If any check fails, the status is
`FAIL_EXACT_SCALAR_DIRAC_TRANSPORT_CHECKPOINT` and no continuation is
authorized. In either case, Rule-9 three-way independent clearance remains
unmet unless three independent reports are actually attached.
