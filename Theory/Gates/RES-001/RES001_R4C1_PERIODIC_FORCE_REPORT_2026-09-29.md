# R4C1-T2P1: periodic-force mean obstruction and conditional contrast probe

Date: 2026-09-29. Owner: Master Test 2 / conditional R4C1-v1.
The [T2P1 contract](RES001_R4C1_PERIODIC_FORCE_CONTRACT_2026-09-29.md)
(SHA-256 `2f660751bd0155833643b3388672bb0462dbe5af703385875eda370b021d3645`)
was frozen before the numerical attempts. The R4C1 action, B1 parameter
literal, first variation and C1 coefficient report were not changed.

**Disposition:** An action-derived, aligned-frame flat-FRW scalar equation
has an exact nonzero mean response for positive mean dust on compact `T^3`.
A separately declared static *contrast* snapshot with the finite `b`
regulator has a convergent three-dimensional pseudospectral control.
This is a necessary-condition and numerical-method result, **not** a
coupled physical torus solution or a canonical weak-field law.
`physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`,
`review_status=DEFERRED`; Tests 1–3 and parent gates remain held.

## 1. Action-derived equation and zero mode

Under the contract's flat FRW metric, aligned fixed frame, constant
positive couplings, dust constraint `T_m=-rho` and the frozen auxiliary
boundary convention, the varied scalar equation is

\[
 -K_Q a^{-3}\partial_t(a^3\dot\psi)
 +3A a^{-3}\nabla_x\!\cdot
   (|\nabla_x\psi|\nabla_x\psi)
 -b a^{-4}\Delta_x^2\psi-\beta\rho=0.
\]

The homogeneous limit agrees with the pinned B1 scalar equation. Both
spatial divergences integrate to zero on a periodic torus. Therefore

\[
 K_Q a^{-3}\partial_t(a^3\dot{\bar\psi})=-\beta\bar\rho.
\]

For `beta>0` and positive mean dust, a fully static scalar in this
fixed-frame FRW reduction is incompatible with that exact mean equation.
This rejects a *particular frozen-frame static-total-source shortcut*,
not a time-dependent background, a compensated contrast, or every ITSM
formulation. It also does not solve perturbed Einstein, frame or dust
constraints. The zero mode must not be removed by inserting positive total
mass into a periodic Poisson equation.

Subtracting the mean equation, then taking only the declared `a=1`
snapshot with the **contrast** time derivative and metric/frame responses
neglected, gives the conditional spatial equation

\[
 3A\nabla\!\cdot(|\nabla\psi|\nabla\psi)
 -b\Delta^2\psi=\beta\,\delta\rho,
 \qquad \bar\psi=\overline{\delta\rho}=0.
\]

The positive convex spatial energy used in the discrete method is
`J=sum[A|grad psi|^3+b(Delta psi)^2/2+beta delta_rho psi]` up to
cell volume. Its stationary equation is the displayed contrast equation.
The finite regulator `b=5/11` is retained; the earlier unregulated
spherical asymptotic is not substituted for this periodic problem.
No bound is known for the omitted time, metric, frame or dust terms.

## 2. Frozen three-dimensional numerical control

The contract fixes `K_Q=3`, `A=2/7`, `b=5/11`, `beta=2/5`,
`rho_bar=1/5` and
`delta_rho=(cos x+2 cos y+3 cos z)/50` on a `2*pi`-periodic cubic torus.
The total density is everywhere at least `2/25>0`, while its contrast
has exactly zero mean. Pseudospectral odd grids `N=17,25,33`, a
zero-mean gauge and a convex-energy stationary solver are specified before
comparison. The analytic `A=0` linear control, sign mutation, weak
Fourier residuals, grid convergence and off-shell energy-gradient check
provide separate diagnostics; they are not independent full physics solvers.

The first executable attempt failed **6/46** local checks: its L-BFGS
iteration did not reach the frozen strong-residual tolerance on the
larger grids, and three associated weak checks failed. That
[attempt-01 receipt](../../../Analysis/MasterTests/outputs/r4c1_t2p1_attempt_01/summary.json)
is preserved, SHA-256
`1dfd8346d4e7957de4ea04bab1389c3feaf1242a0d84602e4b853540facf33f4`.
The solver was changed to damped Newton with the exact discrete Hessian
and positive Fourier preconditioner; the frozen action, source, grids,
coefficients and acceptance thresholds were not changed.

The [attempt-02 receipt](../../../Analysis/MasterTests/outputs/r4c1_t2p1_attempt_02/summary.json)
(SHA-256 `fb59f3bf28e1b57c5294448f011731e805fe2f7928d12d40de210abb24f762bc`)
passes **46/46** local checks, with zero failed or unknown checks. At all
three grids the normalized strong collocation residual is approximately
`3.2572e-8` (threshold `1e-5`). The largest specified weak Fourier
residual is `2.547e-8` (threshold `1e-5`). Omitting the `b` term at the
nonlinear solution leaves normalized residual about `0.919`, so the
regulator is quantitatively indispensable for this probe. The three
fundamental cosine coefficients change by at most `2.851e-9` relatively
from `N=25` to `33` (threshold `5e-3`); this is a grid diagnostic, not a
continuum error bound. The independent off-shell directional finite
difference differs from the analytic discrete energy gradient by
`1.717e-8` relatively (threshold `1e-5`). A static nonzero total-density
mean is explicitly rejected by the zero-mode compatibility control.

The [executable](../../../Analysis/MasterTests/test_02_r4c1_periodic_force.py)
has SHA-256 `8e1b398c70cd1308252d743acbb4d2a7fcef02c28d3b79b0f124f5c3f85a6727`.
It pins the contract and seven upstream sources by SHA-256 and parses
the B1 parameter literal without executing an older receipt producer.
The receipt records NumPy `2.4.6`, SciPy `1.17.1` and SymPy `1.14.0`.
All results are local validation, not independent peer review.

## 3. Remaining scientific and review holds

The solved discrete contrast snapshot does not demonstrate a physical
periodic galaxy, the full metric/Euler response, a controlled weak-field
and quasistatic domain, the `2/3` projection factor, or a physical
overlap with the S4H-U formal high-momentum range. It does not determine
`C_chi` or the empirical `a_0`, and no observational data entered this
probe. C1's independent `A`/background nonidentifiability still applies.
The result cannot promote Test 2, Test 3, MAT-001, UVIR-003, Stage 4A,
the R4C1 parent or publication readiness.

Rule-9 review is deferred under the operator policy, not cleared.
The eventual independent review must inspect the FRW variation and signs,
auxiliary boundary convention, mean-mode argument, pseudospectral weak
form, first-attempt failure, Newton correction and scope of the grid
diagnostics. The substantive next Test-2 gate is a coupled perturbed
metric/frame/dust/Euler calculation with a bounded quasistatic reduction
on an admissible periodic background; its viability may depend on the
unresolved Test-1 physical-domain and constrained-IVP questions.
