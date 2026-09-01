# VOR-001 Stage S2 — Winding-Sector Energy from Declared Condensate Action

**Stage:** S2  
**Date:** 2026-08-07  
**Status:** `OPEN_SCAFFOLD_ONLY`  
**Branch:** `recovery/v12-core-architecture`  
**Claim:** None Derived  
**Predecessor:** VOR-001 S1 (`PASS_VOR001_S1_MATH_TEMPLATE_ONLY`)  
**physics_pass:** false

---

## 1. Purpose

Stage S1 audited a **toy** complex U(1) field on a fixed rectangular T³ —
constant density, smooth winding, purely dimensionless parameters.
That scaffold is mathematically clean but makes no connection to the ITSM
declared condensate sector.

Stage S2 asks a more structured question:

> Does the ITSM declared condensate action, evaluated on a smooth
> winding background with amplitude variation allowed, produce a
> winding-sector energy functional consistent with the S1 toy results
> in the appropriate limit?

This stage stays strictly within mathematical scaffolding. It does not:
- validate a force law or resonance spectrum
- connect winding energy to any observable
- advance UVIR-003, MAT-001, or any gate above Open

---

## 2. Declared condensate action (from ITSM Core Architecture §3.2)

The ITSM candidate microscopic order parameter is:

```
Phi = (rho / sqrt(2)) exp(i Theta)
```

The condensate action on the background spacetime is (schematically):

```
S_cond[Phi, g, U] = integral d^4x sqrt(-g) L_cond(rho, Theta, g, U)
```

where on a flat T³ spatial slice at fixed time, the spatial energy density is:

```
E_density = (1/2)|nabla rho|^2
          + (1/2) rho^2 |nabla Theta|^2
          + V_eff(rho; mu)
```

with the effective potential (at chemical potential mu):

```
V_eff(rho; mu) = V(rho) - (1/2) mu^2 rho^2
```

For the smooth winding sector:

```
Theta(x) = 2*pi*(n1*x/L1 + n2*y/L2 + n3*z/L3)
```

the winding integers n = (n1, n2, n3) are topologically protected on T³.

**Key difference from S1:** In S2, rho(x) is NOT fixed to the constant v.
Amplitude variation rho(x) = rho_0 + delta_rho(x) must be allowed, and the
equation of motion for rho must be checked — does the smooth winding sector
actually satisfy the amplitude EOM, or does the winding gradient source
amplitude modulation?

---

## 3. Analytic structure for S2 tests

### 3.1 EOM for rho in a smooth winding background

For a given winding vector n and box L = (L1, L2, L3), the rho EOM is:

```
-nabla^2 rho + rho |nabla Theta|^2 + dV_eff/drho = 0
```

Substituting the smooth winding Theta:

```
|nabla Theta|^2 = (2*pi)^2 * [n1^2/L1^2 + n2^2/L2^2 + n3^2/L3^2] = omega_n^2
```

For constant rho = rho_0, the EOM reduces to:

```
rho_0 * omega_n^2 + dV_eff/drho |_(rho_0) = 0
```

This modifies the equilibrium density: rho_0(n) != v in general.
The winding gradient acts as an effective mass term, shifting the minimum.

### 3.2 Energy at the winding-modified equilibrium

At rho_0(n) satisfying the EOM, the total energy is:

```
E(n, rho_0(n)) = (1/2) rho_0(n)^2 * omega_n^2 * V_T3
               + V_eff(rho_0(n)) * V_T3
```

where V_T3 = L1*L2*L3.

In the S1 limit (V_eff = (lambda/4)(rho^2 - v^2)^2, rho_0 = v):
- The EOM modification is order (omega_n^2 / lambda v^2) — small for strong coupling
- S2 must reduce to the S1 analytic formula in the lambda >> omega_n^2/v^2 limit

---

## 4. Tests for S2 (S2-T01 through S2-T06)

| ID | Name | Description | Pass criterion |
|----|------|-------------|----------------|
| **S2-T01** | EOM rho correction | For several n, solve the corrected rho_0(n) EOM numerically | rho_0(n) deviates from v by O(omega_n^2 / lambda v^2); recovers v as lambda → ∞ |
| **S2-T02** | S1 limit recovery | Verify S2 energy reduces to S1 analytic formula in lambda >> omega_n^2/v^2 | Relative deviation < 0.1% for lambda = 100, omega_n = 1 |
| **S2-T03** | Winding increases equilibrium energy | For fixed rho_0(n), E(n) > E(0) for n != 0 | Strict inequality for all nonzero n |
| **S2-T04** | Reflection degeneracy | E(n) = E(-n) at the EOM rho_0 | Exact symmetry to machine precision |
| **S2-T05** | Isotropy covariance (isotropic box) | E(n1,n2,n3) invariant under permutations for L1=L2=L3 | Relative deviation < 1e-10 |
| **S2-T06** | Amplitude variation sourced by winding | For large winding norm, rho_0(n) < v (winding suppresses amplitude) | rho_0(n) monotonically decreasing in |n| for isotropic box |

**Hostile-audit result (2026-08-25):** retain T02's preregistered criterion as
written. Its exact deviation at `lambda=100, omega=1, v=1` is `1/200 = 0.5%`,
so T02 is `FAIL_PREREGISTERED_NUMERICAL_CRITERION`. The earlier runner's
`lambda=100000` substitution did not test this row. T01 and T03-T06 survive
only with the exact broken/restored branch qualification recorded in the
joint VOR/TOP S2 audit.

---

## 5. What this stage does NOT address

- Connection to force law or SPARC predictions
- Connection to MAT-001 matching (V, K_Q, C_m)
- Any resonance, defect, or UVIR coupling
- The two-sector architecture (separate force field psi)
- Observable predictions: a₀, C_obs, H₀, PTA, lensing
- S3 (defect cores) — requires solving a nonlinear PDE for the vortex
- S4 (resonance definition)

---

## 6. Claim firewall

This stage does NOT claim:

- A derivation of the galactic rotation law from winding sectors
- Any connection between winding energy and vacuum energy or cosmological constant
- A microscopic identification of ITSM with a specific condensate
- Any result that advances the UVIR or MAT gate status

All outputs carry: `physics_pass: false`, `research_gate_status: OPEN_SCAFFOLD_ONLY`.

---

## 7. Relation to S1

| Property | S1 (done) | S2 (this stage) |
|----------|-----------|-----------------|
| rho | Fixed constant ρ₀ = v | Allowed to vary; EOM solved |
| V_eff | Quartic (λ/4)(ρ²-v²)² | Same form, but rho_0 shifts |
| Theta | Smooth winding 2π(n·x/L) | Same |
| Connection to ITSM | Toy model only | Uses declared condensate EOM |
| Analytic formula | Exact at ρ₀ = v | Modified by EOM correction |
| Novelty | Dimensional checks, basic positivity | EOM self-consistency, amplitude-winding coupling |

---

## 8. Unresolved decisions

1. Whether to use the quartic potential or the more general UVIR-001 tested potential
2. Whether mu is treated as a fixed parameter or derived from a charge constraint
3. Whether to extend to anisotropic box (S1 already covers this; S2 isotropic first)
4. Whether the EOM correction has a closed-form analytic solution or requires numerical iteration

---

## 9. Document control

**Version:** 0.1  
**Date:** 2026-08-07  
**Branch:** `recovery/v12-core-architecture`  
**Status:** `OPEN_SCAFFOLD_ONLY`
