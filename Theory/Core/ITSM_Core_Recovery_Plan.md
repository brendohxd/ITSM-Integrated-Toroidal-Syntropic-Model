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

`UVIR-001 -> MAT-001 -> (SCR-001, LEN-001) -> DISK-001 ->`
`(TOP-001, VOR-001, WAK-001, reservoir) -> CBR-002 ->`
`(COS-001, PERT-001)`.

This order prevents an observational fit or a tuned constitutive source from
being mistaken for a derivation of the underlying mechanism.
