# UVIR-003 Progress Log

> [!IMPORTANT]
> **Scoped progress record; not a gate decision.** G0 retained this extracted technical history because its claim boundaries are compatible with the signed Stage-5 HOLD. Detailed numerical statements remain subject to producer/input/hash and pinned-environment verification. This file does not close M2, M3, M6 or M7 and cannot promote UVIR-003 or MAT-001.

This log stores the detailed finite-`q` reduction and constraint-dressing audits extracted from the core architecture document to preserve technical detail while keeping the constitution clean.

## Scalar ADM Subgate and Finite-q Reduction

The first scalar ADM subgate was completed in a controlled frozen-coefficient,
subhorizon limit. In aether-unitary scalar gauge, lapse and scalar shift
elimination independently reproduces the exact Einstein-aether spin-0 speed
and yields a positive principal block at the representative dimensionless
point. The condensate constraint introduces
`q_ADM^2=(rho_dot^2+rho^2 mu^2)/(M_U^2 c14)`, so that principal result is
restricted to `q_phys >> max(H,q_ADM)`.

The complete quadratic finite-`q` reduction has now also been performed on the
evolving branch. For all 48,861 representative samples with
`10^-3 <= q_phys/H <= 10^3`, the reduced kinetic inertia is three positive and
zero negative and the lapse-momentum constraint matrix is nonsingular. The
exact on-shell determinant is proportional to `q_phys^2`, so one kinetic
direction loses rank as `q_phys -> 0`. The follow-on gauge audit identifies
that direction exactly as `(H,rho_dot,mu)`, the homogeneous time-translation
orbit. Two gauge-invariant matter combinations retain a positive regular
`q=0` kinetic block across the representative trajectory. The rank loss is
therefore a gauge endpoint rather than a third physical homogeneous scalar.

The flat-decoupling khronon expansion is now verified through cubic order in
three spatial dimensions and exactly reproduces the earlier longitudinal
basis. For algebraic lapse and shift constraints, stationarity of the
first-order solution cancels every explicit second-order constraint correction
from the reduced cubic action. Linear-dispersion energy and momentum
conservation also force an on-shell three-point spatial triangle to be
collinear. The follow-on three-dimensional flat-decoupling quartic audit
contains 96 expanded monomials and gives the exact elastic contact form
`4[c123^2/c14-(2c123-c14)cos^2(theta)]`. Elastic `t/u` cubic exchange vanishes
exactly, while the centre-of-mass `s` channel is the non-invertible homogeneous
khronon gauge orbit. At quartic order the second-order constraint source enters
through `-J2^T C^(-1) J2/2`; third-order constraint solutions are unnecessary.
Consequently the physical interaction scale still requires the complete
gauge-regular constrained cosmological `2-to-2` amplitude and physical
eigenmode projection. 

## Constraint-Dressing Audit

The exact nonlinear `g+U+Phi+alignment` ADM parent block
reproduces the FRW and finite-`q` quadratic constraint data. Track A adopts the
rest-space Laplacian
`D_mu D^mu psi=h^{mu nu}nabla_mu nabla_nu psi+theta Q` and retains exact
`Y^(3/2)` for a declared local nonzero-gradient perturbative force analysis.
The homogeneous zero-gradient force action is verified through direct quartic
order: `Q^2` supplies lapse and scalar-shift `J2` components, the regulator
supplies a lapse component only, and exact `Y^(3/2)` is constraint independent
at cubic amplitude order on that background. The finite-`q` multi-sector
coefficient linear in constraints at the origin is assembled in the
`(delta_N,Sigma=q_phys^2 beta)` convention.

The constraint-dressing audit reclassifies this coefficient as
`J2_origin`, not the complete second-order source. The correct quantity is
`S2=partial_z L3[x,z1]`; the associated quartic correction is
`-S2^T C^(-1)S2/2`. The origin-linear formulas remain verified components.
This result is restricted to `q_phys>0` and does not reclassify the
homogeneous gauge orbit. The generic three-dimensional gravity/aether
constraint density and its nonlinear lapse/shift functional operators are now
verified at `q_phys>0`. Adding the condensate temporal shift-advection
operators completes the multi-sector finite-`q` `S2`; the Track-A force cubic
block is affine in the constraints and therefore adds no nonlinear correction
beyond `J2_origin`. The complete generic `L4[x,z1]` contact and reduced
quartic functionals are also assembled. The basis
`(Xi,Q_rho,Q_chi)` has a finite positive low-`q` kinetic limit, with no
exactly homogeneous `Xi` mode. A source-to-observable retarded-response audit
removes direct `Xi` and homogeneous time-translation source support and reads
only retained `(Q_rho,Q_chi)`. All five tested dimensionless cases retain
amplified response through the complex-quartet interval. This resolves the
direct gauge-source attribution question with scope, not an all-background
instability theorem. The Track-A `Pi` mode remains factorized at quadratic
order. Explicit vertex projection, the gauge-regular amplitude, physical
cutoff and global multicone-causality testing remain open.
