# WAK-001 gate specification - causal plenum wake

**Date opened:** 2026-08-03
**Status:** Open
**Claim class:** Open research route; identity pillar retained
**Depends on:** CRA-001 conservation inventory; UVIR-003 mode content;
MAT-001 matter vertex for observable normalization
**Feeds:** CBR-002, LEN-001, DISK-001 transient extensions, PERT-001

## 1. Question

Can ITSM's historical fluid-wake intuition be represented by a well-posed,
causal and energy-accounted non-equilibrium degree of freedom whose static
limit is compatible with, but not double-counted against, the Conditional
AQUAL-class IR response?

The gate is passed only by a declared action or constitutive system. A wake
illustration, streamline plot or analogy is not evidence of a physical wake.

## 2. Frozen commitments

1. The complete declared system obeys covariant stress-energy conservation.
2. The spin-2 sector remains minimally coupled to the matter light cone.
3. The static AQUAL-class response is the Conditional comparison baseline.
4. A wake must possess initial data and autonomous time evolution. An
   instantaneous elliptic field is not a memory sector.
5. Energy throughput does not imply anisotropic stress without a constitutive
   relation or action.
6. Old quantitative wake, lensing-offset and Bullet Cluster claims remain
   Rejected packaging. They are not restored by opening this gate.

## 3. Degrees of freedom and bookkeeping fork

Before Stage 1, select exactly one route.

### Route I - internal constitutive variable

`W` is an internal non-equilibrium variable of the plenum. Its energy and
momentum are included in `T_P^{mu nu}`. The conservation equations remain

```text
nabla_mu T_m^{mu nu} = Q_mp^nu,
nabla_mu T_P^{mu nu} = -Q_mp^nu + Q_syn^nu,
nabla_mu T_R^{mu nu} = -Q_syn^nu.
```

No separate `T_W^{mu nu}` or wake exchange current is allowed on this route.

### Route II - independent wake sector

`W` has its own stress tensor and an interaction-derived exchange current
`I_W^nu`:

```text
nabla_mu T_m^{mu nu} = Q_mp^nu,
nabla_mu T_P^{mu nu} = -Q_mp^nu + Q_syn^nu - I_W^nu,
nabla_mu T_W^{mu nu} = I_W^nu,
nabla_mu T_R^{mu nu} = -Q_syn^nu.
```

The four equations must sum identically to zero. `I_W^nu` may not be silently
identified with `Q_mp^nu`, `Q_syn^nu`, or a condensate-number source.

## 4. Candidate hierarchy

The candidates are tests, not adopted laws.

### W0 - no-memory control

The static force sector alone. This is the required null comparison and fixes
what must not be counted again as a wake.

### WR - advected relaxation template

```text
tau_W D_U W + W = kappa_W S_W,
D_U = U^mu nabla_mu.
```

Necessary conditions in a local rest-frame linearization are `tau_W > 0`, a
causal declared transport velocity, decay of the source-free solution, and a
bounded source-response functional. `S_W` must be built from declared fields
and projected consistently with the tensor character of `W`.

The static limit is `W -> kappa_W S_W`; that limit must either vanish from the
observable force law or be matched as an explicit correction. It must never
duplicate the AQUAL response already produced by `psi`.

### WH - hyperbolic field candidate

A second-order candidate may be considered only if propagation rather than
relaxation is physically required:

```text
Z_W D_U^2 W + Gamma_W D_U W
  - c_W^2 h^{mu nu} nabla_mu nabla_nu W + M_W^2 W = J_W.
```

The gate must derive the signs, tensor projectors and stress tensor from a
declared action. At linear order, `Z_W > 0`, `Gamma_W >= 0`, `M_W^2 >= 0` and
a causal characteristic cone are necessary but not sufficient conditions.

## 5. Gate stages

| Stage | Required result | Status |
|---|---|---|
| 0. Interface freeze | Declare W0, bookkeeping fork, source and observable interfaces | **This document - complete as a scaffold** |
| 1. Linear template | Dispersion, characteristics, decay and static-limit audit | **Template only; not physical matching** |
| 2. Energy accounting | Positive/bounded energy or non-negative entropy production; exact exchange cancellation | **Route II selected for Conditional calculation; free template passes; stress variation and exchange remain Open** |
| 3. Covariant completion | Action or controlled constitutive theory on the evolving FRW branch | Open |
| 4. Coupled perturbations | No ghosts/gradient instabilities and causal global cone structure with UVIR modes | Blocked by Stages 2-3 and UVIR-003 |
| 5. Matter/metric matching | Derive source, matter vertex, physical metric and lensing response | Blocked by MAT-001 |
| 6. Observation | Controlled disk/transient/cluster tests with locked nuisance policy | Blocked by Stages 4-5 |

Stage 0 does not change any claim-ledger status. Stage 1 can validate a
mathematical template only. WAK-001 cannot pass before Stages 2-5 pass.

## 6. Required tests

### Mathematical tests

- source-free modes decay rather than grow;
- the principal symbol is hyperbolic where the candidate is used;
- the characteristic cone is causal relative to the declared physical metric;
- the initial-value problem is well posed;
- energy is positive/bounded, or a covariant entropy-production inequality is
  derived for a dissipative constitutive route;
- the exact sum of sector exchange equations vanishes;
- the `omega -> 0` limit is finite and explicitly reconciled with W0;
- the response decouples in the limit selected by the parent interaction.

### Numerical tests

- manufactured impulse and sinusoidal-source solutions;
- convergence under time-step and spatial-grid refinement;
- periodic-box advection without spurious norm growth;
- conservation-budget residual at every step;
- negative controls with `tau_W <= 0`, acausal transport or wrong exchange
  signs must fail;
- parameter scans report domains, not a preferred numerical value.

### Physical tests, after matching

- distinguish steady galactic response from genuine time-dependent memory;
- compute whether any wake stress gravitates through the declared metric;
- compare lensing and dynamical centroids without inserting an offset by hand;
- demonstrate compatibility with disk, Solar-System and GW constraints;
- report a null result if the matched wake is negligible.

## 7. Pass, hold and fail criteria

**PASS_WAK_001** requires all of the following:

1. one bookkeeping route selected without double counting;
2. a declared covariant action or controlled dissipative closure;
3. stable and causal coupled characteristics in its stated domain;
4. explicit positive/bounded energy or entropy accounting;
5. a controlled static limit compatible with the AQUAL baseline;
6. interaction-derived matter and metric observables; and
7. reproducible numerical tests including negative controls.

Use **HOLD** when the model is mathematically viable but its source,
normalization, physical metric or UVIR coupling is unmatched.

Use **FAIL** for unavoidable instability, acausality, double counting,
non-conservation, or a singular/static limit incompatible with the recovered
force sector.

## 8. Claim firewall

| Statement | Current classification |
|---|---|
| A finite-density plenum may support causal memory | Open |
| The WR template is a possible stable mathematical model for `tau_W > 0` | Conditional on its declared toy domain |
| ITSM contains a derived physical wake law | Not derived |
| A wake explains galaxy rotation curves | Not derived; static AQUAL baseline is separate |
| A detached wake explains cluster lensing offsets | Rejected old packaging; reopen only after Stages 3-6 |
| Wake stress maintains the `13/12` torus ratio | Not derived; belongs downstream to CBR-002 |

## 9. Immediate next calculation

Route II is selected only as the first Conditional calculation route; see
`WAK-001_STAGE2_BOOKKEEPING_ROUTE.md`. Its free local template passes the
declared Hamiltonian, dispersion, cone, susceptibility and negative-control
screen. Next vary one declared trial action with respect to `W`, `g_mu_nu` and
`U^mu`, then compare the resulting mode against `Phi`, `U` and `psi`. Keep
`J_W=0` until duplication is excluded. Do not promote the physical wake claim.
