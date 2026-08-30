# ITSM Core Identity Briefing

> **MANDATORY PREREQUISITE:** Every agent (human or AI) MUST read and internalize
> this document before performing any work on the ITSM repository. See GEMINI.md
> Rule 7. Subagents are READ-ONLY and must report findings back to the parent
> agent — see GEMINI.md Rule 8.

---

## 1. The Core Proposition

> The observable vacuum is an active finite-density condensate whose low-energy
> excitations, global circulation sectors, compact boundary conditions, and
> exchanges with matter and a reservoir may have gravitational consequences.

This is the **identity** of the ITSM. Everything else — predictions, mechanisms,
rotation curves, Hubble tension — is downstream. If a piece of work contradicts
this identity, the work is wrong, not the identity.

## 2. The Five Pillars

| # | Pillar | Content |
|---|--------|---------|
| 1 | **Finite-density condensate** | The vacuum has a nonzero order parameter `Phi = (rho/sqrt(2)) exp(i Theta)` with `rho0 != 0`. Finite density is declared, not assumed. |
| 2 | **Low-energy excitations** | Phonons and amplitude modes of the condensate. The IR EFT is derived from the UV condensate action, not postulated. |
| 3 | **Global circulation & winding** | Quantized vorticity and winding numbers on compact topology. The vortex sector is distinct from the phonon sector. |
| 4 | **Compact boundary conditions** | Spatial topology is `T^3` (three-torus). Periodic boundary conditions create topology-dependent stress, moduli, and mode structure. |
| 5 | **Reservoir / syntropic exchange** | The condensate is an open system exchanging with a reservoir. This sector is tagged `RES-001` and is `OPEN SCAFFOLD`. |

## 3. Methodology — The Iron Rule

```
Identity first → derive mechanisms second → restore predictions only afterward.
```

- You do NOT start from a desired prediction and work backward.
- You do NOT promote a claim beyond its recorded gate status.
- You do NOT fabricate a derivation to match an empirical target.
- Honest failure is **always** superior to fabricated success.

## 4. Gate System

The ITSM uses a formal gate system to track what is derived vs. assumed vs. open.
Gates are **fail-closed**: a gate is `BLOCKED` or `IN_PROGRESS` until every item
on its checklist is satisfied. No shortcut, no override.

### Current Gate Statuses (authoritative source: `active_research.md`)

| Gate | Status | Key Note |
|------|--------|----------|
| UVIR-001 | CLOSED NEGATIVE | Born-Infeld does not derive square-root law |
| UVIR-002 | CLOSED PROVISIONAL | Y^(3/2) local EFT identified as candidate |
| **UVIR-003** | **PASS_UNITARITY** | Non-derivative contact amplitude A = C_m⁴ ρ_b / f⁴ satisfies tree-level unitarity; cutoff Λ_UV = f/C_m |
| **MAT-001** | **R5-P1 EVALUATION_COMPLETE** | Conformal trace conservation fixes C_m ≡ 1; CBR-002 scale matching fixes f = 1/√(4πG), V = √(4πG), α ≡ 1 |
| MAT-001 R1–R4 | COMPLETE | Convention, provenance, action, residue contract |
| MAT-001 R5 | R5-P1 EVALUATED | Scale-compensator fork executed; all 8 artifacts verified & SHA-256 hashed |
| TOP-001 | OPEN SCAFFOLD | Physical moduli dynamics |
| VOR-001 S0–S1 | COMPLETE | Vocabulary + 3D smooth-winding energy audit |
| VOR-001 S2 | PASS_DIMENSIONAL_AUDIT | Two-scale hierarchy verified: ξ_gal = 0.090 kpc, ℓ = 0.21 mm; Landau Condensate Disruption screening |
| WAK-001 | OPEN SCAFFOLD | C2 mode-projected Green function |
| RES-001 | OPEN SCAFFOLD | R0 null control + R1 minimal route |
| **DISK-001** | **PASS_STAGE5** | 2D/3D nonlinear AQUAL Picard solver converged at ε = 6.06 × 10⁻⁹ |
| **STAT-001** | **DIAGNOSTIC_BENCHMARK** | Full SPARC evaluated: χ² = 18,092 (clean Q1+Q2, 0 global free params) |
| SCR-001 | NOT_STARTED | Screening gate (Landau disruption mechanism identified but not formally gate-tested) |
| LEN-001 | NOT_STARTED | Lensing gate |
| CBR-001 | COMPLETE_SCOPED_NEGATIVE | Free-field calculation supplies a scoped negative result; no 13/12 attractor |
| CBR-002 | SCALE_DERIVATION_COMPLETE | f = 1/√(4πG), ℓ = √(4πG)/a₀ derived from BTFR matching |

### What Has Been Derived (v12.0 Results)

The following parameters were previously `NOT_COMPUTED` and have now been derived
via the R5-P1 scale-compensator evaluation:

- **C_m ≡ 1.0** — Fixed uniquely by conformal Weyl trace conservation (T^μ_μ)
- **K_Q = f²** — The dilaton kinetic normalization from the scale-compensator action
- **V = C_m / √K_Q = 1/f = √(4πG)** — The effective matter coupling residue
- **α ≡ 4πG V² = 1.0** — The dimensionless AQUAL coupling strength (exact)
- **f = 1/√(4πG) ≈ 0.282 M_Pl** — The symmetry-breaking condensate scale
- **ℓ = √(4πG)/a₀ ≈ 0.21 mm** — The mesoscopic transition healing length

All derivation artifacts are SHA-256 hashed in `Theory/Gates/MAT-001/MAT-001_R5_P1_SPEC.md`.

## 5. Claim Hygiene — What Remains Open

The following items remain open problems or leading-order approximations:

- `13/12` Casimir ratio — leading-order 1D cycle factorization; full 3D Epstein tensor correction uncomputed
- `H0 = 72.97` — a zero-parameter geometric prediction from the 13/12 ratio; matches SH0ES to 0.07σ but depends on the 13/12 derivation above
- `4/9 → 1` renormalization flow — motivated conjecture (beta function postulated with IR fixed point g*=1); η not derived from first principles
- `S8 = 0.863` — **honestly reported as unsolved**; ITSM worsens the S8 weak-lensing tension
- Screening unification — Cassini algebraic compliance uses Δ = (2/3)√(a₀/g_N); physical mechanism is Landau Condensate Disruption; formal unification pending
- Bullet Cluster — qualitative N-body treatment only; full 3D hydrodynamic simulation not performed

## 6. Critical Path (Updated)

The former singular blocker (MAT-001) has been resolved via R5-P1. The current
critical path is:

```
Next priorities:
├─ SCR-001 (NOT_STARTED): Formal screening gate — unify Landau disruption with Cassini PPN bounds
├─ LEN-001 (NOT_STARTED): Gravitational lensing predictions from AQUAL field equation
├─ 3D Epstein Tensor: Full T³ Casimir backreaction to verify/correct 13/12 ratio
└─ Galaxy-by-Galaxy DISK-001: Connect Picard solver to individual SPARC surface-density profiles
```

## 7. What Agents Must NOT Do

1. **Fabricate results** — see GEMINI.md Rules 1, 3, 6
2. **Reverse-engineer constants** — see GEMINI.md Rule 2
3. **Write to the repository** if you are a subagent — see GEMINI.md Rule 8
4. **Promote claims beyond gate status** — e.g., do not claim the 4/9→1 flow is proven, or that S8 is resolved
5. **Ignore open problems** — S8, screening unification, 3D Epstein correction, and Bullet Cluster quantitative prediction are all honestly open

## 8. Canonical Documents

| Document | Purpose |
|----------|---------|
| `GEMINI.md` | Scientific integrity rules (binding) |
| `active_research.md` | Authoritative gate dashboard |
| `Theory/Core/ITSM_Core_Architecture.md` | Constitutional architecture |
| `Theory/Gates/MAT-001/` | MAT-001 gate documents (including R5-P1 artifacts) |
| `Theory/Gates/UVIR-003/` | UVIR-003 gate documents |
| `Theory/Gates/VOR-001/` | VOR-001 healing length and screening documents |
| `Manuscript/ITSM_Core_Cosmology_v12.0.tex` | Official v12.0 core manuscript |

---

*This document is referenced by GEMINI.md Rule 7. Last updated: 2026-08-29 (v12.0 reintegration).*
