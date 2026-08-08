# MAT-001 R5-P1 Scale-Compensator Parent Fork — Specification

**Stage:** R5-P1  
**Date:** 2026-08-07  
**Status:** `OPEN_RESEARCH_CANDIDATE`  
**Branch:** `recovery/v12-core-architecture`  
**Claim:** None Derived — research candidate only  
**Global status:** MAT-001 `BLOCKED` | V `NOT_COMPUTED` | K_Q `NOT_DERIVED` | Stage 4A `CLOSED`

---

## 1. Purpose

R5 proved that the declared R3 conformal matter action and Track-A force action
leave `C_m` and `K_Q` as independent Wilson coefficients. The action form
therefore underdetermines `V = C_m / sqrt(K_Q)`. The R5 hold can be lifted
only by:

1. a named microscopic parent action with a calculation of `g_phi / sqrt(Z_phi)`;
2. a live on-shell signed matter-to-physical-mode residue in a declared chart; or
3. an independently justified coefficient relation with enough physical input to
   fix or bound `V`.

R5-P1 is an attempt at Path (1). It tests whether a **conformal compensator /
dilaton-superfluid parent action** can correlate kinetic normalisation and
matter coupling through one physical scale `f` — without importing any MOND
target or phenomenological coefficient.

This is a bounded research fork. It does not advance MAT-001, unlock Stage 4A,
or constitute a physical prediction until all eight required artifacts are
completed and all rejection gates are tested.

---

## 2. Motivation: the compensator construction

In the minimal toy chart (`psi = sigma / f`, where `sigma` is the dilaton /
conformal compensator and `f` its decay scale):

```
L_kin = (f^2 / 2)(d psi)^2      =>   K_Q = f^2
L_m   = -rho_b exp(psi)          =>   C_m = 1
```

Therefore:

```
V = C_m / sqrt(K_Q) = 1 / f
```

The same result appears in the canonical `sigma` chart where `K_Q = 1` and
`C_m = 1/f`, giving `V = 1/f` invariantly.

**Why this differs from setting K_Q = 1 by convention:** the relation
`K_Q = f^2`, `C_m = 1` follows from the compensator construction, not from a
normalisation choice. One physical scale `f` fixes `V`. This is the feature
that distinguishes R5-P1 from all rejected shortcuts.

**Critical caveat:** the above is a pre-projection result. The finite-density
theory has mixed phonon/dilaton modes. The physical signed residue must be
computed AFTER full diagonalisation of the scalar kinetic/gradient matrix.
`V = 1/f` before mode projection is NOT an admissible Derived claim.

**Primary literature anchors:**
- Argurio, Hoyos & Musso, Phys. Rev. D 102, 076011 (2020): finite-density
  phonon-dilaton mixing is real and modifies the mode content.
- Fuks, Goodsell & Kang, JHEP 10 (2020) 044: compensator matter couplings are
  controlled by a dilaton decay scale.

---

## 3. Minimal parent action form (to be varied, not assumed)

The candidate parent action on a background spacetime with metric `g_mu_nu`,
preferred frame `U^mu`, and condensate `Phi = (rho/sqrt(2)) exp(i Theta)`:

```
S_parent = S_EH[g]
         + S_dilaton[sigma, g]          -- conformal compensator sector
         + S_cond[Phi, g, U]            -- finite-density condensate sector
         + S_coupling[sigma, Phi]       -- dilaton-condensate coupling
         + S_m[Psi_m, A(psi)^2 g]      -- conformal matter action
```

where `psi = sigma / f`, `A = exp(C_m (psi - psi_*))`.

**The field/unit chart, symmetry table, and all couplings must be declared
explicitly before variation.** The script must enforce that no coefficient is
inserted from a MOND target.

---

## 4. Required artifacts (all eight before advancing)

| # | Artifact | File | Status |
|---|----------|------|--------|
| 1 | Covariant parent action + field/units table | `mat001_r5_p1_parent_action.py` | TODO |
| 2 | Symmetry-breaking and DOF ledger | `mat001_r5_p1_dof_ledger.py` | TODO |
| 3 | Homogeneous finite-density background equations | `mat001_r5_p1_background.py` | TODO |
| 4 | Complete scalar quadratic action after constraints | `mat001_r5_p1_quadratic.py` | TODO |
| 5 | Kinetic/gradient eigenvalues + physical-mode map | `mat001_r5_p1_modes.py` | TODO |
| 6 | Signed matter-to-physical-mode residue `g_phys` | `mat001_r5_p1_residue.py` | TODO |
| 7 | Cutoff and strong-coupling estimate | `mat001_r5_p1_cutoff.py` | TODO |
| 8 | Screening, PPN and lensing applicability statement | `mat001_r5_p1_gravity_tests.py` | TODO |

Plus: mutation tests that reject (a) coefficient insertion from MOND target,
(b) pre-projection `V = 1/f` promotion, (c) wrong-sign matter residue.

---

## 5. Rejection gates (any one kills the fork)

| Gate | Rejection condition |
|------|-------------------|
| Ghost | Extra ghost mode in the physical scalar spectrum |
| Gradient instability | Wrong sign in spatial kinetic eigenvalue |
| Strong coupling | Zero or diverging coupling in declared galactic regime |
| Extra long-range scalar | New massless mode with unacceptable PPN/lensing signature |
| Screening failure | Solar System constraint violated |
| No galactic overlap | No healthy parameter domain overlaps the required galactic weak-field regime |
| Coefficient imported | Any coupling inserted from MOND/SPARC phenomenology rather than derived |

**Decision rule:** advance only if the same healthy parameter domain derives or
rigorously bounds `g_phys` without importing `C_obs`. Otherwise freeze the fork
as rejected and retain the R5 HOLD.

---

## 6. Prior results ruling in / ruling out

### 6.1 Ruled out: standard superfluid dark matter coupling (Berezhiani-Khoury)

The BK phonon-baryon coupling is explicitly undetermined in their action — a
dimensionless coefficient introduced without derivation from the phonon kinetic
normalisation. This supports the R5 HOLD; it does not provide a route to close it.

### 6.2 Ruled out: minimal shift-symmetric density portal

The auxiliary-density Lagrangian `L = nX - (lambda/3)n^3 - eta n rho_b`:
- Derives the 3/2 pressure structure (correct)
- Phase enters through derivatives in `X` → portal gives `rho_b pi_dot` vertex,
  NOT a direct static `rho_b pi` source
- Any explicit phase portal adding `rho_b pi` has an independent soft-breaking
  coefficient unless a further symmetry constrains it

This alternative is therefore not a static-force matching route under R5-P1.

### 6.3 Pending: exact ADM static-source obstruction re-derivation

Task C1a: re-derive in the exact ITSM phase chart (including ADM variables)
whether the static source `rho_b pi` is absent or present. The pathway survey's
conclusion must be verified in the declared ITSM coordinates, not just the
generic field theory.

---

## 7. What this stage does NOT address

- Numeric value of `V` (requires completing artifacts 4–6)
- UVIR-003 amplitude or unitarity criterion
- Reopening Stage 4A
- Any observational prediction: a₀, C_obs, H₀, PTA, SPARC, lensing, S8
- Resonance spectrum or defect solution
- Any MAT-001 PASS or UVIR PASS

---

## 8. Claim firewall

This specification does NOT constitute:

- A Derived value of `V`, `K_Q`, `C_m`, `g_phi`, `Z_phi`, or `f`
- A derivation of the galactic force law
- A closing of MAT-001 or UVIR-003
- Evidence for or against any observational claim

Until artifact 6 (signed residue) is computed, all claim-status fields
remain: `MAT-001 BLOCKED | V NOT_COMPUTED | K_Q NOT_DERIVED | Stage 4A CLOSED`.

---

## 9. Reproduction

```powershell
# All scripts to be added to Analysis/MAT/MAT-001/R5_P1/
# Run order: parent_action -> dof_ledger -> background -> quadratic -> modes -> residue -> cutoff -> gravity_tests
```

---

## 10. Document control

**Version:** 0.1  
**Date:** 2026-08-07  
**Branch:** `recovery/v12-core-architecture`  
**Status:** `OPEN_RESEARCH_CANDIDATE` — no physics pass, no Derived claims
