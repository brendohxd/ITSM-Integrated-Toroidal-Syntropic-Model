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
python Analysis/UVIR/UVIR-003/uvir003_nonlinear_adm_action_provenance.py
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
## Three-dimensional khronon quartic audit

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_aether_stueckelberg_3d_quartic.py
```

This derives the complete 96-monomial flat-decoupling quartic basis, verifies
the earlier quadratic and cubic actions and checks an independently generated
one-dimensional quartic reduction. In elastic centre-of-mass kinematics it
proves the exact contact angular form and exact vanishing of `t/u` cubic
exchange. The `s` channel has zero spatial momentum and is the non-invertible
homogeneous khronon gauge orbit.

At quartic order the second-order constraint source is required through the
Schur complement `-J2^T C^(-1)J2/2`; third-order constraint solutions are not
needed. The output is an interaction-readiness diagnostic, not a physical
cutoff. The latter still requires the full gauge-regular constrained
cosmological `2-to-2` amplitude and physical eigenmode projection.

## Nonlinear ADM action provenance

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_nonlinear_adm_action_provenance.py
```

This verifies that the exact nonlinear
`gravity+aether+condensate+alignment` ADM parent block reproduces the FRW
minisuperspace and finite-`q` quadratic constraint matrix and source. At that
checkpoint the force completion and its perturbative rule were still open.
The subsequent Track-A audit below resolves the regulator definition and
derives the force-sector `J2` component, while retaining the non-analytic local
force-amplitude boundary.

## Force-completion options

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_force_completion_options.py
```

This checks three nonlinear completions of the Stage-A spatial regulator and
the two controlled treatments of exact `Y^(3/2)`. Track A is now selected:
`Delta_U psi = D_mu D^mu psi` is adopted for derivation, the exact deep-IR
operator is retained and its ordinary perturbative force analysis is assigned
to a declared local nonzero-gradient background.

## Track A force ADM expansion

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_track_a_force_adm_cubic.py
```

This expands `Q^2`, exact `Y^(3/2)` and the adopted regulator through direct
quartic ADM order on the homogeneous zero-gradient FRW branch. It verifies the
force contribution to the quadratic lapse/shift source: `Q^2` supplies lapse
and scalar-shift terms, the regulator supplies a lapse term only, and exact
`Y^(3/2)` supplies no `J2` term at the zero-gradient origin. The result is
`PASS_FORCE_SECTOR_J2_COMPONENT`.

## Origin-linear finite-q J2 component

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_full_j2_schur.py
```

This expands the fixed nonlinear parent action and combines its
`gravity+aether+condensate+alignment` source with the Track-A force result. It
regresses exactly to the previous finite-`q` linear source, assembles the
coefficient linear in lapse/scalar shift at the constraint origin in the
`(delta_N, Sigma=q_phys^2 beta)` convention, and verifies the
corresponding algebraic component
`-J2^T C^(-1)J2/2`.

The result is `PASS_ORIGIN_LINEAR_J2_COMPONENT`. The later dressing audit
shows that the complete second-order source is
`S2=partial_z L3[x,z1]`; consequently the earlier Schur interpretation is
provisional. The inverse-Laplacian shift representation still applies only
at `q_phys>0`, and the homogeneous gauge-orbit result is unchanged.

## Direct physical-field contact block

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_direct_contact_block.py
```

This expands the fixed nonlinear parent action with the lapse and scalar shift
held at their background values. It verifies the complete constraint-free
direct cubic and quartic physical-field components `L3[x,0]` and `L4[x,0]`
for `x=(R,delta_rho,vartheta,pi)`, including exact regression of the Track-A
force terms to the preceding ADM expansion.

The result is `PASS_X_ONLY_DIRECT_CONTACT_BLOCK`. It is not the
constraint-dressed `L3[x,z1]` or `L4[x,z1]`, a physical eigenmode projection,
or a cosmological `2-to-2` amplitude. Those require substituting
`z1=-C^(-1)J1` into every constraint-dependent cubic and quartic term and
combining the result with `-S2^T C^(-1)S2/2`.

## Constraint-dressing completeness audit

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_constraint_dressing_audit.py
```

The exact homogeneous lapse block proves that cubic constraint dependence is
not affine. In particular,

```text
S2_N - J2_N,origin = 2 B1 delta_N1 + 3 V delta_N1^2.
```

The result is `PASS_CONSTRAINT_DRESSING_COMPLETENESS_AUDIT`. The previously
derived `J2` and Schur expression remain verified origin-linear components,
but the full finite-`q` calculation must derive `S2` at `z1`, all scalar-shift
dressing, `L3[x,z1]` and `L4[x,z1]` before physical projection.

## Finite-q scalar-shift dressing sub-block

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_scalar_shift_dressing.py
```

This derives the exact gravity/aether extrinsic-curvature block through
quartic order for a nonzero-momentum scalar shift with one homogeneous soft
curvature leg. It verifies the nonlinear corrections to both `S2_N` and
`S2_Sigma` after substituting the finite-`q` solution `z1=-C^(-1)J1`.

The result is `PASS_SOFT_CURVATURE_SHIFT_DRESSING_SUBBLOCK`. It fixes a
genuine part of `L3[x,z1]` and `L4[x,z1]`, but it is not the complete
non-collinear three-momentum kernel. Generic `D_iR D_i beta` terms plus
condensate and Track-A force shift-advection dressing remain open. The
homogeneous gauge-orbit classification is unchanged.

## Generic gravity/aether scalar-shift kernel

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_generic_shift_kernel.py
```

This removes the soft-curvature restriction and retains the full
three-dimensional conformal-ADM structures `D_iD_j beta`,
`D_iR D_j beta`, `D_iR D_i beta`, and `(D delta_N)^2`. Constraint-degree
bookkeeping separates `J2_origin` from the nonlinear density contributing to
`S2=partial_z L3[x,z1]`.

The result is `PASS_GENERIC_GRAVITY_AETHER_SHIFT_DRESSING_KERNEL`. The generic
lapse and beta functional operators regress exactly to the verified soft
channel. Complete finite-`q` `S2` still requires condensate temporal
shift-advection and Track-A force shift-advection before the corrected Schur
functional and physical projection can be assembled.

## Complete finite-q S2 functional

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_complete_s2_operator.py
```

This adds the condensate temporal lapse/shift-advection dressing to the
generic gravity/aether operators and audits the Track-A force cubic block.
The force dependence is affine in lapse and scalar shift, so it contributes
no nonlinear correction beyond its verified `J2_origin` component.

The result is `PASS_COMPLETE_FINITE_Q_S2_FUNCTIONAL`. The complete
multi-sector source `S2=partial_z L3[x,z1]` and corrected Schur functional
`-S2^T C^(-1)S2/2` are assembled at `q_phys>0`. Complete generic
`L4[x,z1]`, physical scalar projection, the exchange-plus-contact amplitude,
and a physical cutoff remain open.

## Complete generic L4 contact functional

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_complete_l4_contact.py
```

This expands every fixed sector through fourth order while retaining the
generic first-order lapse and scalar shift `z1=-C^(-1)J1`. It verifies exact
regression to the direct `L4[x,0]` block and the soft-curvature shift channel.

The result is `PASS_COMPLETE_GENERIC_L4_X_Z1_CONTACT`. Combined with the
complete `S2`, the reduced quartic functional is assembled. Physical scalar
projection, the gauge-regular exchange-plus-contact amplitude, and a
physical cutoff remain open.

## Regular finite-q physical scalar basis

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_physical_scalar_basis.py
```

This introduces `Xi=(q_phys/H)R` and the gauge-invariant matter variables
`Q_rho` and `Q_chi`. The transformed kinetic matrix has a finite positive
low-`q` limit over the validated domain, while the exactly homogeneous `Xi`
mode remains excluded as the time-translation gauge orbit.

The result is `PASS_REGULAR_FINITE_Q_PHYSICAL_SCALAR_BASIS`. The leg-wise
cubic/quartic projection map is fixed, but projected momentum-space kernels,
the exchange-plus-contact amplitude, and a physical cutoff remain open.

## Complete factorized cubic momentum kernel

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_cubic_momentum_kernel.py
```

This polarizes the complete analytic `L3[x,z1]` functional over three
non-collinear Fourier legs, supplies the exact finite-`q` lapse/shear
resolver for every leg, and applies the full time-dependent map to
`(Xi,Q_rho,Q_chi,Pi)`.

The result is `PASS_FACTORIZED_FINITE_Q_PHYSICAL_CUBIC_KERNEL`. The exact
`|grad(pi)|^3` term has no ordinary Taylor kernel at the homogeneous
zero-gradient background, and the exactly homogeneous internal `Xi` channel
is not defined by the finite-`q` map. The reduced quartic kernel and exact
homogeneous projectors are addressed in the next checkpoint; the propagating
exchange-plus-reduced-contact amplitude and physical cutoff remain open.

## Reduced quartic momentum kernel and homogeneous projectors

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_reduced_quartic_momentum_kernel.py
```

This polarizes the complete analytic four-leg contact and derives the
physical two-leg constraint source directly from the verified cubic
functional. The three Schur pairings are assembled as
`-B_ab^T C(K)^(-1) B_cd` for nonzero internal momentum.

The result is `PASS_FACTORIZED_FINITE_Q_REDUCED_QUARTIC_KERNEL`. At exact
zero internal momentum, separate projectors remove the nonexistent
homogeneous `Sigma=-D^2 beta` coordinate and the `Xi` time-translation orbit,
while retaining the lapse constraint and `(Q_rho,Q_chi,Pi)` physical
subspace. This rule is algebraically audited but has not yet been inserted
into a propagating exchange calculation. The exchange-plus-reduced-contact
amplitude, unitarity criterion, physical cutoff, and local nonzero-gradient
exact-`Y` reduction remain open.

## Physical quadratic propagators and adiabaticity hold

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_physical_quadratic_propagators.py
```

This constructs the local frozen-time inverse quadratic kernel in the
finite-`q` physical basis `(Xi,Q_rho,Q_chi,Pi)` and the separately projected
exact-`q=0` response on `(Q_rho,Q_chi,Pi)`. It verifies positive kinetic
inertia, nonsingular finite-`q` constraints, inverse closure, pole pairing,
and positive residues for every sampled real positive-frequency pole.

The result is `HOLD_LOCAL_ADIABATIC_PHYSICAL_QUADRATIC_PROPAGATORS` rather
than a pass. All five `q_phys/H=100` samples have four real positive-frequency
modes with positive residues, but complex frozen-background pole pairs occur
at lower and intermediate momenta and in later exact-`q=0` snapshots. A
fixed-comoving-momentum WKB and time-domain transfer audit was therefore
required; its completed result is reported in the next section. No `2-to-2` amplitude, unitarity bound,
strong-coupling scale, or physical cutoff is claimed.

## Fixed-comoving adiabaticity and time-domain transfer

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_propagator_adiabaticity_transfer.py
```

This follows fixed comoving modes with `q_phys=k/a`, restores the exact
`K_dot`, `P_dot`, and `3H` terms in the physical second-order equations, and
evolves the kinetic-normalized gauge-invariant phase-space transfer. An
independent canonical reconstruction verifies the Hamiltonian form.

The transfer numerics pass: the maximum coarse/fine error is `1.30353e-4`,
the maximum second-order/canonical residual is `1.05500e-4`, and the maximum
local Hamiltonian-generator defect is `4.06385e-16`. The `q/H=100` trajectory
is a controlled adiabatic high-momentum subset.

The result is `HOLD_TIME_DEPENDENT_INFRARED_TRANSFER_INTERPRETATION`.
Frozen-pole exponentiation is quantitatively invalid in the nonadiabatic
domain, but the deepest sampled infrared trajectory (`q/H=0.01` initially)
still has a converged maximum normalized phase-space gain of `1.37708e27`.
That gain must be projected onto continuously tracked physical eigenmodes
before it can be classified as instability, gauge-continuation behavior, or
background squeezing. No `2-to-2` amplitude, unitarity bound,
strong-coupling scale, or physical cutoff is claimed.
