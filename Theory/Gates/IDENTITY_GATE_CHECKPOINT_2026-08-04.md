# Parallel identity-gate checkpoint - 2026-08-04

**Branch:** `recovery/v12-core-architecture`
**Scope:** TOP-001, VOR-001 and WAK-001 mathematical/Conditional research lanes
**Framework status changed:** no
**Manuscript freeze created:** no
**Physical prediction restored:** no

## Purpose

This checkpoint records bounded progress on three parallel identity pillars.
Each result is useful as a reproducible gate input, but none closes its owning
research gate or changes the status of a cosmological, force-law, lensing,
cluster, PTA or SPARC claim.

## TOP-001 - fixed-volume full-triaxial chart

The reviewed biaxial scaffold remains unchanged. A separate two-coordinate
log-shape chart now tests

```text
L_i = V^(1/3) exp(alpha_i),
alpha_x + alpha_y + alpha_z = 0.
```

The full-triaxial audit passes nine checks covering fixed volume, the cubic
negative control, positive non-cubic sample diagnostics, smooth approach to
the cubic point, axis-permutation covariance, refinement below 1%, scale
invariance, malformed inputs and the claim firewall.

```text
PASS_TOP001_S1_TRIAXIAL_FIXED_VOLUME_TEMPLATE
physics_pass: false
research_gate_status: OPEN_SCAFFOLD_ONLY
```

The saved summary SHA-256 is
`27922C6398BD16E71813A171A1A817105DC4F1EE5AAC846175F750B2C4B41F8A`.
Independent reruns reproduce the hash. Empty and non-finite diagnostic
lattices are independently rejected by the executable guards.

Boundary: no modulus action, Casimir tensor, twisted-space preference,
backreaction, `13/12`, `H0`, `a0`, `Cobs` or cosmology.

## VOR-001 - finite density and smooth winding

The inherited first draft failed because it compared a second-order discrete
energy directly with the continuum formula using tolerances smaller than the
known discretization error. That draft was preserved outside the repository.

The replacement separates the exact central-difference energy from the
continuum energy, verifies machine-level agreement with the discrete formula,
and independently measures second-order continuum convergence. It also checks
the stable finite-density minimum, global `U(1)` shift, integer sectors,
positivity, reflection, permutation covariance, the zero-winding control,
selected norm monotonicity and malformed inputs.

```text
PASS_VOR001_S1_AND_S2PRE_MATH_TEMPLATE_ONLY
physics_pass: false
research_gate_status: OPEN_SCAFFOLD_ONLY
```

The deterministic summary SHA-256 is
`7A2590C15F3920FECA02836FAE8B1F37E9CA121CEFB4723D54624360C55D2ADD`.

Boundary: no parent condensate validation, defect solution, resonance
spectrum, SWNT mechanism, `a0`, force normalization, cosmology, lensing, PTA,
SPARC or `13/12` result.

## WAK-001 - constrained Route-II preparation

The Route-II local trial family now has five additional bounded audits:

| Audit | Result | Summary SHA-256 |
|---|---|---|
| Local constrained variation | `PASS_WAK001_W2_1_LOCAL_VARIATION_IDENTITIES` | `16890ED3F02A6532838F98130859DCEE5FB0740DED89A82A6944C5356230D5EE` |
| Finite-`q` mode inventory | `PASS_WAK001_W2_5_MODE_COUNTING_PRESCREEN` | `673CB9B8183D070830FEF51F0746FA277816A772987D83E93A049579399508E8` |
| Parent-Hessian readiness | `PASS_WAK001_COUPLED_HESSIAN_READINESS_AUDIT` | `D82F5D61BB9B97E115300C34165D9B2BB41111863E41E50B629543C9315AB5BF` |
| Zero-background factorization | `PASS_WAK001_ZERO_BACKGROUND_QUADRATIC_FACTORIZATION_TEMPLATE` | `D969D2BC8E8EC12E302B13F20AB15271BFCD70779A858074A5438AAF92B5DA62` |
| Microscopic identity inventory | `PASS_WAK001_MICROSCOPIC_IDENTITY_EVIDENCE_INVENTORY` | `D085E8EEF798C1877B0CEB0C09C4F0AA3731EEBA9E09A2B5907FDBF5CD8C81AB` |

The zero-background result is deliberately narrow. For the declared local
trial density, `Wbar=0`, `nabla Wbar=0`, `J_W=0` and no explicit bilinear
operator derive a factorized W-dependent quadratic block. Metric and frame
couplings return at cubic order. A nonzero background or explicit bilinear
invalidates the factorization.

The canonical evidence inventory finds no map from `W` to
`(Xi,Q_rho,Q_chi,Pi)`, no independent microscopic parent derivation and no
internal constitutive closure. The microscopic identity therefore remains
`UNRESOLVED`.

Boundary: `physics_pass` remains false; no source, exchange current,
dissipation, physical wake stress, AQUAL correction, cluster offset or
observable wake law is derived.

## Combined decision

1. Retain TOP-001 and VOR-001 as `OPEN_SCAFFOLD_ONLY`.
2. Retain WAK-001 as Open under
   `HOLD_WAK001_MICROSCOPIC_IDENTITY_MAP_UNDECLARED` and the cubic-constraint
   hold.
3. Do not write these results into a frozen manuscript release. They are
   candidates for the next working manuscript only after a dedicated
   manuscript integration and review.
4. Keep the natural next tasks separate:
   - TOP: a carefully scoped CBR-001 interface, without target packaging;
   - VOR: parent-action local fluctuations before defects or resonance;
   - WAK: one microscopic identity closure route before sourcing or damping.
