# UVIR-003 Stage A and Stage B diagnostics

Stage A declares the preferred-frame architecture and validates necessary
flat-background decoupling-limit conditions for:

- an independently dynamical unit timelike frame aligned with, but not
  algebraically identified with, the condensate current;
- the four-operator Einstein-aether kinetic basis;
- a force scalar with independent temporal and spatial invariants;
- a higher-spatial-derivative candidate regulator for the zero-gradient limit.

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_stage_a.py
```

Outputs:

- `outputs/uvir003_stage_a_summary.json`
- `outputs/uvir003_stage_a_checks.csv`

`STATUS: PASS` validates Stage-A algebra. It does not close UVIR-003. The full
metric/aether/condensate constraint reduction, strong-coupling calculation and
matter coupling remain outstanding, so MAT-001 stays blocked.

The bounded Stage B diagnostics are:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_frame_sector_speeds.py
python Analysis/UVIR/UVIR-003/uvir003_adm_readiness.py
python Analysis/UVIR/UVIR-003/uvir003_background_completion.py
python Analysis/UVIR/UVIR-003/uvir003_frw_background.py
python Analysis/UVIR/UVIR-003/uvir003_zero_gradient_force_block.py
python Analysis/UVIR/UVIR-003/uvir003_causality_check.py
python Analysis/UVIR/UVIR-003/uvir003_force_strong_coupling_estimate.py
python Analysis/UVIR/UVIR-003/uvir003_conditional_kq_estimate.py
python Analysis/UVIR/UVIR-003/uvir003_scalar_adm_principal.py
python Analysis/UVIR/UVIR-003/uvir003_scalar_adm_finite_q.py
```

The zero-gradient force-block check proves quadratic factorization only for
the declared Stage-A truncation. It finds one positive `z=2` force scalar for
`K_Q > 0` and `gamma > 0`, while showing that `K_Q` alone is not identifiable
until a physical field normalization is fixed by microscopic or matter
matching. The remaining metric-aether-condensate reduction, nonzero-gradient
mixing, covariant regulator and physical cutoff remain open.

The scalar ADM readiness audit finds that the declared Minkowski plus
finite-density condensate background is off shell:
`rho_Phi+p_Phi=mu^2*rho0^2>0`. A constant vacuum-energy subtraction cannot
cancel this enthalpy. The reservoir/driver background and its scalar
perturbation response must be declared before lapse and shift can be
eliminated consistently. It also corrects the exact Einstein-aether
coefficient map to `alpha_i=(M_U^2/M_P^2)c_i`; bare `alpha_i=c_i` is valid
only if `M_U=M_P`.

The background-completion screen rejects a constant vacuum term, a healthy
two-derivative `P(X)` scalar and the ghost-condensate point as exact Minkowski
support for the nonzero condensate enthalpy. Prescribed rigid support is
decoupling-only. The selected least-assumptive route is a self-consistent
evolving flat-FRW background.

The FRW background calculation derives
`M_cos^2=M_P^2+(M_U^2/2)(c1+3c2+c3)`, the amplitude equation and exact
conservation of `a^3*rho^2*mu`. It verifies a regular representative
dimensionless expanding branch with independently monitored Friedmann,
continuity and charge residuals. This removes the background blocker: the
scalar ADM reduction is ready to begin on the evolving branch, but is not yet
performed.

The scalar ADM principal-symbol calculation now performs the first controlled
part of that reduction. In aether-unitary scalar gauge it eliminates the lapse
and scalar shift for frozen background coefficients at `q_phys=k/a >> H`,
independently recovers the published Einstein-aether spin-0 speed, and derives
the finite-`q` condensate kinetic determinant. The representative branch
passes principal positivity, but its scalar aether speed is superluminal
relative to the metric and the audit is controlled only above the additional
`q_ADM` scale. The full time-dependent, finite-`q` and strict low-`q` system
remains open.

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_scalar_adm_principal.py
```

The time-dependent finite-`q` calculation completes the quadratic
metric-aether-condensate constraint elimination on the same FRW branch. It
retains all background, `q_phys^0` and `q_phys^2` terms, includes the
coefficient derivatives along the trajectory, and scans 48,861 matrices over
`10^-3 <= q_phys/H <= 10^3`. Every sampled nonzero-wavenumber kinetic matrix
has three positive and no negative eigenvalues, while the constraints remain
nonsingular. The exact reduced kinetic determinant is proportional to
`q_phys^2`, however, so one direction loses kinetic rank as `q_phys -> 0`.
This is a low-`q` hold pending cubic canonical normalization, not a ghost
verdict or a completed stability proof.

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_scalar_adm_finite_q.py
```

## Low-q gauge-orbit and bounded cubic audits

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_scalar_low_q_gauge.py
python Analysis/UVIR/UVIR-003/uvir003_aether_stueckelberg_cubic.py
```

The low-`q` audit proves that the collapsing finite-wavenumber kinetic
direction approaches the homogeneous time-translation orbit. The two
independent gauge-invariant matter combinations retain a positive regular
`q=0` kinetic block across the representative trajectory. A strong-coupling
scale obtained by normalizing the vanishing gauge direction is therefore
rejected as gauge dependent.

The bounded Stueckelberg calculation derives the longitudinal one-dimensional
flat-decoupling quadratic and cubic aether vertex basis and identifies the
canonical nonzero Fourier mode. The subsequent three-dimensional audit
completes that flat-decoupling basis and proves that first-order lapse and
shift constraints suffice at cubic order. It still does not supply the
physical cosmological strong-coupling scale, which requires the constrained
cosmological `2-to-2` exchange-plus-contact amplitude and projection onto the
complete physical eigenmode basis.

## Three-dimensional khronon cubic audit

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_aether_stueckelberg_3d_cubic.py
```

This extends the bounded flat-decoupling khronon calculation to the complete
three-dimensional cubic operator basis and verifies its collinear reduction.
It also proves that explicit second-order lapse and shift solutions cancel out
of the reduced cubic action: only the first-order constraints are required at
cubic order.

The reported operator-by-operator NDA momentum is diagnostic only. A
non-collinear on-shell three-point process is forbidden by linear-dispersion
kinematics, while a physical cutoff requires the constrained cosmological
`2-to-2` exchange-plus-contact amplitude and physical eigenmode projection.
