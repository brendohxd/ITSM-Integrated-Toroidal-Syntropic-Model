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
