# ITSM Core Recovery and Manuscript Reconstruction Plan

Version: 0.1  
Programme: CRA-001 / CRA-002  
Branch: `recovery/v12-core-architecture`

## Purpose

This plan rebuilds the Integrated Toroidal-Syntropic Model (ITSM) around the
physical architecture that recurs across its earlier versions while retaining
the mathematical corrections established by the later research gates. It does
not restore an older manuscript wholesale and it does not patch v11.4.1 in
place.

The governing rule is:

> First preserve the identity of the model. Then derive the mechanisms. Only
> afterward restore the predictions.

## Preserved baseline

The v11.4.1-era repository state is preserved by the annotated Git tag
`v11.4.1-pre-core-recovery`. The existing manuscript remains a provenance
record. Recovery work occurs in a separate modular tree and must not overwrite
the baseline until the new architecture has passed an internal hostile review.

## Recovered physical core

The modern reconstruction treats ITSM as a layered, driven, finite-density
system:

1. a complex condensate order parameter with amplitude and phase modes;
2. a finite-density background admitting winding, circulation and defects;
3. an emergent infrared phonon sector;
4. local matter--plenum exchange;
5. reservoir--plenum throughput for the open observable subsystem;
6. compact `T^3` boundary conditions and dynamical shape moduli;
7. causal wake relaxation or memory, if it can be derived;
8. a possible non-equilibrium anisotropic-stress sector.

These ingredients are architecture, not completed predictions. Their precise
actions and coefficients remain subject to the gates below.

## Non-negotiable separations

### UV condensate versus IR phonon

The analytic microscopic condensate action and the non-analytic low-energy
phonon action describe different levels. The `Y^(3/2)` operator may be an
emergent finite-density action; it must not be attributed directly to the
current Born--Infeld expression.

### Local exchange versus cosmological throughput

Use distinct currents:

- `Q_mp^nu` for local matter--plenum exchange;
- `Q_syn^nu` for reservoir--plenum throughput.

The complete matter + plenum + reservoir system remains covariantly conserved.

### Topology versus numerical coefficients

Topology determines periodic boundary conditions, allowed modes, winding
sectors, defect classes and shape-dependent stress. Numerical coefficients
such as `2/3` or `13/12` require separate matching calculations; they may not
be inferred solely by counting dimensions or cycles.

### Derived results versus observational ambitions

SPARC, lensing, the Hubble tension, CMB, NANOGrav, JWST and cluster collisions
remain downstream applications. They cannot be promoted to core predictions
until the field sector responsible for each observable has closed its gate.

## Work packages

### CRA-001 -- Canonical core architecture

Deliverables:

- `Theory/Core/ITSM_Core_Architecture.md`;
- a declared field and sector inventory;
- the UV/IR hierarchy;
- conservation identities;
- toroidal mode and zero-mode conventions;
- a prohibited-claims register.

Pass condition: every later equation can be assigned to exactly one declared
sector and no sector violates total covariant conservation.

### CRA-002 -- Claim migration

Deliverable: `Theory/Core/ITSM_Claim_Migration_Ledger.csv`.

Every material legacy claim is classified as `Derived`, `Conditional`, `Open`
or `Rejected`, with its evidence, dependencies, manuscript action and owning
research gate. Rejected claims remain in the provenance record but do not
appear as live predictions.

### UVIR-001 -- Condensate-to-phonon matching

Starting from a finite-density complex field, determine whether integrating out
the amplitude mode yields a stable `P(X) proportional to X^(3/2)` phase action
with the required sign and normalization.

Required checks:

- dimensional consistency;
- existence of the finite-density branch;
- positivity of the compressibility and Hamiltonian;
- amplitude-mode mass and separation of scales;
- phonon sound cone and strong-coupling scale;
- matching to `G`, `a0` and field normalization.

UVIR-001 result (2026-07-17): **closed negative for the declared minimal
candidate**. The canonical mass--quartic--sextic complex scalar has a stable
timelike branch and yields `P(Z) proportional to (Z-m^2)^(3/2)` in the pure
sextic limit, but its static expansion begins at quadratic order because
`P_Z = rho0^2/2 > 0`. It does not generate the required spatial `Y^(3/2)`
operator. See `Theory/Gates/UVIR-001/UVIR-001_GATE_REPORT.md`.

### UVIR-002 -- Select an alternative microscopic route

Compare three explicit replacements: a controlled nonrelativistic
gradient-dominated branch, a two-field split between background density and
force phonon, and a noncanonical preferred-frame condensate. Select a route
only after checking stability, derivative control, technical naturalness and
the existence of the spatial `Y^(3/2)` operator.

UVIR-002 result (2026-07-17): **closed as a provisional route selection**. The
standalone nonrelativistic `X<0` branch produces the cubic spatial term but has
`P_XX < 0` and is rejected. A two-field split is useful but insufficient alone.
The selected successor is a two-sector preferred-frame force EFT: retain the
complex condensate for density, circulation and topology, and use a separate
force scalar with independent temporal `Q` and spatial `Y` invariants. The
simple cubic truncation degenerates at zero gradient and its coefficient is
unmatched. See `Theory/Gates/UVIR-002/UVIR-002_ROUTE_SELECTION.md`.

### UVIR-003 -- Validate the selected preferred-frame action

Declare one covariant two-sector action, fix the status of `U^mu`, count its
constraints and propagating degrees of freedom, and derive the quadratic action
about cosmological, zero-gradient and galactic backgrounds. The gate must find
a controlled zero-gradient completion, a positive kinetic/gradient domain, a
cutoff and a symmetry or matching explanation for the operator hierarchy.
MAT-001 remains blocked until this gate passes.

UVIR-003 Stage-A result (2026-07-17): **validated necessary conditions; full
gate in progress**. To avoid double counting, the working action uses an
independent unit timelike `U^mu` aligned dynamically with the condensate
current. The complete four-term frame basis is retained. A projected `k^4`
operator conditionally regularizes the force scalar at zero gradient in the
frozen-Minkowski decoupling limit. The metric/aether/condensate constraints,
coupled Hamiltonian, strong-coupling scale and operator naturalness remain
unresolved. See `Theory/Gates/UVIR-003/UVIR-003_STAGE_A_REPORT.md`.

UVIR-003 Stage-B readiness result (2026-07-26): **scalar ADM reduction
blocked pending an on-shell background completion**. The declared Minkowski
finite-density condensate has `rho_Phi+p_Phi=mu^2*rho0^2>0`; a constant
vacuum-energy subtraction cannot cancel this enthalpy. A covariant
reservoir/driver action, a controlled rigid-support limit, or a consistent
cosmological background must be declared before lapse and shift are
eliminated. The frame-sector literature map is also normalized by
`alpha_i=(M_U^2/M_P^2)c_i`; bare equality with the published Einstein-aether
coefficients holds only if `M_U=M_P`. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_ADM_READINESS.md`.

UVIR-003 Stage-B background-completion result (2026-07-26): **minimal exact
Minkowski support routes rejected; evolving flat-FRW route selected**. Vacuum
energy and the ghost-condensate point have zero enthalpy. A homogeneous
two-derivative `P(X)` support scalar would require `P_X<0` to cancel the
condensate, while short-wavelength gradient health requires `P_X>0`. Rigid
support is valid only as a controlled decoupling approximation, and importing
a higher-derivative NEC-violating sector would require a new action and gate.
The next calculation is therefore an on-shell evolving FRW background with
conserved condensate charge or a separately derived charge-transfer source.
This selects the route but does not solve the background or unblock the scalar
ADM reduction. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_BACKGROUND_COMPLETION.md`.

UVIR-003 Stage-B FRW-background result (2026-07-26): **representative on-shell
evolving branch verified; scalar ADM background blocker removed**. On the
comoving isotropic aether branch,
`M_cos^2=M_P^2+(M_U^2/2)(c1+3c2+c3)`. The alignment and constant-force
background terms vanish, while the condensate obeys
`d(a^3 rho^2 mu)/dt=0`. A dimensionless expanding solution preserves the
Friedmann constraint to `2.13e-10` relative residual, with charge drift at
machine precision and continuity residual below `1.90e-15`. The example is
an existence proof, not a physical parameter selection or COS-001 fit. The
next UVIR-003 task is the time-dependent scalar perturbation and constraint
reduction on this background. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_FRW_BACKGROUND.md`.

UVIR-003 Stage-B scalar-ADM principal result (2026-07-26):
**subhorizon principal block reduced and positive at the representative
dimensionless point; full finite-wavelength system remains open**. In
aether-unitary scalar gauge, lapse and scalar shift elimination gives
`K_R=2 M_P^2 F(1-alpha13)/alpha123` and
`G_R=M_P^2(2-alpha14)/alpha14`, independently reproducing the published
Einstein-aether spin-0 speed. The condensate kinetic determinant introduces
`q_ADM^2=(rho_dot^2+rho^2 mu^2)/(M_U^2 c14)`, so the frozen-coefficient audit
is controlled only for `q_phys >> max(H,q_ADM)`. The representative point
passes principal positivity but has `s0^2=1.31018`, leaving multicone global
causality open. The next calculation must retain the full time dependence and
all finite-`q` terms through the strict low-`q` limit. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_SCALAR_ADM_PRINCIPAL.md`.

UVIR-003 Stage-B finite-`q` scalar result (2026-07-26): **quadratic
finite-wavenumber constraints eliminated; strict low-wavenumber kinetic-rank
hold**. The exact time-dependent quadratic action retains the background,
`q_phys^0`, `q_phys^2` and scalar-shift `q_phys^4` terms. Its reduced kinetic
determinant is proportional to `q_phys^2`. Across 48,861 representative
samples with `10^-3 <= q_phys/H <= 10^3`, every kinetic matrix has three
positive and no negative eigenvalues and the constraints remain nonsingular.
One direction loses kinetic rank at `q_phys=0`, so the follow-on task is the
low-`q` gauge-orbit and cubic interaction audit. This is not a ghost verdict or
a full stability pass. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_SCALAR_ADM_FINITE_Q.md`.

UVIR-003 Stage-B low-`q` scalar result (2026-07-26): **homogeneous gauge orbit
identified; physical `q=0` kinetic block positive on the representative
branch**. The exact null direction `(H,rho_dot,mu)` is the tangent to the FRW
background under a homogeneous time translation. The invariant variables
`Q_rho=delta_rho-(rho_dot/H)R` and
`Q_theta=vartheta-(mu/H)R` retain two positive kinetic eigenvalues at all 801
trajectory points. The smallest finite-`q` eigenvector converges to the same
orbit. A cutoff inferred by normalizing its vanishing eigenvalue is therefore
rejected as gauge dependent. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_SCALAR_LOW_Q_GAUGE.md`.

UVIR-003 Stage-B bounded cubic result (2026-07-26): **longitudinal
flat-decoupling Stueckelberg vertex basis derived; physical interaction scale
open**. Restoring `T=t+pi` gives the quadratic combinations `c14` and `c123`
and four checked cubic longitudinal operators. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_AETHER_STUECKELBERG_CUBIC.md`.

UVIR-003 Stage-B three-dimensional cubic result (2026-07-26): **complete 3D
flat-decoupling khronon cubic basis and constraint-order identity passed;
physical `2-to-2` cutoff open**. The tensor vertex exactly reduces to the
longitudinal result. For an invertible algebraic constraint block, the
first-order lapse and shift solutions suffice at cubic order because every
explicit second-order correction cancels by quadratic stationarity. A
basis-dependent diagnostic gives `q_NDA=0.125778823734` at the unselected
dimensionless point, but it is not a physical cutoff. Linear on-shell
three-point kinematics force collinearity. The next invariant calculation is
the complete constrained scalar `2-to-2` amplitude with cubic exchange,
quartic contact and physical eigenmode projection. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_AETHER_STUECKELBERG_3D_CUBIC.md`.

UVIR-003 Stage-B three-dimensional quartic result (2026-07-26): **complete
flat-decoupling quartic basis passed; physical `2-to-2` amplitude held on the
homogeneous `s`-channel gauge orbit**. The expansion contains 96 monomials,
reproduces the quadratic and cubic results and matches an independent
one-dimensional quartic reduction. The elastic contact coefficient is
`4[c123^2/c14-(2c123-c14)cos^2(theta)]`; elastic `t/u` cubic exchange vanishes
exactly. Quartic reduction requires the second-order constraint Schur
complement `-J2^T C^(-1)J2/2`, but not third-order constraint solutions. The
next step is the full evolving-FRW cubic and quartic constrained scalar action,
physical eigenmode projection and gauge-regular unitarity amplitude. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_AETHER_STUECKELBERG_3D_QUARTIC.md`.

UVIR-003 Stage-B nonlinear ADM action-provenance result (2026-07-26): **the
exact `g+U+Phi+alignment` parent block is verified; the full cosmological `J2`
is held on force-sector completion**. The nonlinear ADM coefficients reproduce
the FRW minisuperspace, finite-`q` constraint matrix, `J1` source and alignment
phase stiffness. The projected regulator still lacks its evolving-frame
covariant completion, and `Y^(3/2)=|epsilon|^3 Y2^(3/2)` about `Y=0` does not
define an ordinary analytic cubic Taylor vertex. Complete the force action and
its perturbative prescription before forming the full `J2` and quartic Schur
complement. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_NONLINEAR_ADM_ACTION_PROVENANCE.md`.

UVIR-003 Stage-B force-completion comparison and selection (2026-07-26):
**Track A selected; the rest-space Laplacian is adopted for derivation and
exact `Y^(3/2)` is retained on a declared local nonzero-gradient force
background**. The comparison proves that no analytic smoothing at `Y=0`
preserves the exact deep-IR branch. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_FORCE_COMPLETION_OPTIONS.md`.

UVIR-003 Stage-B Track-A force ADM result (2026-07-26): **the homogeneous
zero-gradient force action is verified through direct quartic order and its
lapse/shift `J2` component is derived**. The temporal `Q^2` term supplies lapse
and scalar-shift sources, the adopted regulator supplies a lapse source only,
and exact `Y^(3/2)` is constraint independent at cubic amplitude order on
this background. The complete multi-sector `J2` is not yet assembled and the
non-analytic physical force amplitude remains assigned to the separate
nonzero-gradient local calculation. See
`Theory/Gates/UVIR-003/UVIR-003_STAGE_B_TRACK_A_FORCE_ADM_CUBIC.md`.

### MAT-001 -- Matter coupling and `C_proj`

Derive the baryon--phonon vertex and calculate the observable Wilson
coefficient. The geometric `2/3` trace ratio is an input motivation, not the
answer. Field redefinitions and kinetic normalization must be fixed before the
coefficient can be compared with data.

### SCR-001 -- High-gradient screening

Construct a single action or controlled matching prescription that retains the
low-acceleration `Y^(3/2)` branch while suppressing anomalous forces in
weak-metric, high-acceleration environments. Validate against ephemerides and
binary dynamics rather than comparing an acceleration ratio directly with a
PPN bound.

### LEN-001 -- Relativistic and lensing completion

Derive the physical metric, the two weak-field metric potentials, light
deflection, Shapiro delay, PPN parameters and gravitational-wave propagation.
A purely conformal massive-matter force is insufficient by itself.

### DISK-001 -- Periodic nonlinear disk solver

Solve the `p=3` nonlinear elliptic equation on a compensated periodic domain.
Validate manufactured, spherical and exponential-disk sources before applying
the solver to a controlled SPARC subset. Measure the curl-field correction and
the radius-dependent effective coupling.

### TOP-001 and VOR-001 -- Shape and circulation

Derive a shape-modulus action for the rectangular torus and a circulation or
defect sector compatible with a complex condensate. Establish which degrees of
freedom are local fields, global moduli or topological sectors.

### WAK-001 -- Causal wake dynamics

Test whether the original wake concept can be represented by a hyperbolic,
retarded or relaxation equation with a positive energy and causal
characteristics. Static field response must be recovered in the appropriate
limit.

### CBR-002 -- Driven anisotropic stress

Only after the reservoir, shape and wake sectors are derived, test whether
their combined anisotropic stress admits a maintained non-equilibrium state.
Do not insert `13/12` into a constitutive coefficient. CBR-001 remains the
baseline result: free periodic scalar Casimir stress produces anisotropy but no
persistent `13/12` attractor.

### COS-001 and PERT-001 -- Coherent cosmology

Choose one declared fiducial background and derive perturbation equations from
the same action and exchange currents. CMB, growth and `S8` calculations must
not mix parameters from incompatible background branches.

## Manuscript reconstruction

The new manuscript lives in `Manuscript/CoreRecovery/` and is modular. Its
first alpha is an architecture and status paper, not a claim to have replaced
Lambda-CDM.

Planned order:

1. Scope and status
2. Core fields and architecture
3. UV/IR hierarchy
4. Conservation and exchange
5. Weak-field EFT
6. Topology, circulation and Casimir result
7. Wake and non-equilibrium dynamics
8. Cosmological status
9. Open closure gates
10. Falsifiability

## Claims excluded from the recovered core

The following may be discussed only as historical or rejected claims unless a
new gate replaces their derivation:

- persistent `13/12` from cycle counting;
- `H0 = 72.97` as a parameter-free prediction;
- direct derivation of the square-root force from the present Born--Infeld
  action;
- `C_proj = 2/3` as an already matched local force coefficient;
- the proposed `2/3 -> 1` beta-function flow;
- exact Solar-System or PPN compliance without a relativistic solution;
- the historical SPARC `p=0.62`;
- SPARC as an independent measurement of cosmic `H0`;
- a NANOGrav frequency interval obtained by assigning frequency units to `a0`;
- a quantitative Bullet Cluster solution from a static or illustrative wake;
- the displayed Jeans/IMF explanation of very low mass-to-light ratios;
- global zero-free-parameter wording;
- any fixed reservoir redshift law not derived from a sector action.

## Internal review before replacement

Before the v12 alpha can replace the baseline manuscript:

1. audit every equation against the canonical architecture;
2. check dimensions, signs and boundary conditions;
3. label every postulate, fitted coefficient and matching assumption;
4. verify that no rejected claim has returned under new language;
5. reproduce every numerical result from clean commands;
6. compile the complete manuscript without unresolved references;
7. run an adversarial scientific review.

## Immediate dependency order

The recommended order after the architecture draft is:

`UVIR-001 -> UVIR-002 -> UVIR-003 -> MAT-001 -> (SCR-001, LEN-001) -> DISK-001 ->`
`(TOP-001, VOR-001, WAK-001, reservoir) -> CBR-002 ->`
`(COS-001, PERT-001)`.

This order prevents an observational fit or a tuned constitutive source from
being mistaken for a derivation of the underlying mechanism.
