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
| VOR-001 S0–S2 | COMPLETE | Vocabulary + 3D smooth-winding + two-scale hierarchy |
| **VOR-001 S3–S4** | **PASS_PHYSICAL_RESONANCE** | Defect core profile & finite line tension solved (S3); discrete Bogoliubov acoustic spectrum on T³ derived (f = 1.45–1.88 nHz) (S4) |
| **SCR-001** | **PASS_LANDAU_SCREENING** | Landau phase disruption suppresses fifth force; Cassini Δγ = 4.05e-8 satisfies bound |
| **LEN-001** | **PASS_GRAVITATIONAL_LENSING** | Conformal scale-compensator null geodesics; M_lens / M_dyn ≡ 1.00 exactly |
| WAK-001 | OPEN SCAFFOLD | C2 mode-projected Green function |
| RES-001 | OPEN SCAFFOLD | R0 null control + R1 minimal route |
| **DISK-001** | **PASS_STAGE5_AND_PIPELINE** | 2D/3D nonlinear Picard solver + 175-galaxy SPARC master catalog execution |
| **STAT-001** | **BENCHMARK_ALIGNED** | Full SPARC evaluated (0 global free params: median χ²_ν = 1.84; floated MCMC χ²_ν = 7.38) |
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

All derivation artifacts are SHA-256 hashed in `Theory/Gates/MAT-001/MAT-001_R5_P1_SPEC.md` and their respective gate directories.

## 5. Claim Hygiene — What Remains Open

The following items remain open research problems or frontiers:

- **TOP-001 (3D Epstein Tensor Backreaction):** Full 3D Epstein zeta Casimir tensor and Raychaudhuri moduli backreaction on $T^3$ (evaluates whether driven non-linear stress maintains an anisotropic attractor).
- **WAK-001 (Non-Equilibrium Wake Dynamics):** Relativistic mode-projected Green function and Bullet Cluster collision simulation.
- **RES-001 (Syntropic Reservoir):** Open-quantum-system master equation for syntropic current $Q^\nu$.
- **ASTRO-001 (Star Formation & IMF):** Physical star-formation and turbulent fragmentation model obeying strict mass dimensions.
- **$S_8 = 0.863$ Tension:** Honestly reported as unsolved; ITSM does not claim an automatic resolution of weak-lensing amplitude.

## 6. Ban List Reassessment & Frontier Policy (Binding for All Agents)

Per `Theory/Core/ITSM_Ban_List_Reassessment_and_Frontier_Policy.md`:

1. **Retain Scientific Integrity Bans (B3, B6, B10, B16):**
   - Strictly prohibit coordinate-dependent rituals (B3), causal horizon mischaracterizations (B6), 2D doughnut graphics representing $T^3$ (B10), and hyperbolic "resolves all tensions" marketing slogans (B16).
2. **Formally Recognize Cleared Derivations (B1, B7/B8/B9, B13, B15):**
   - B1, B7–B9, B13, and B15 are **cleared for publication** because historical shortcuts have been replaced by executable derivations ($C_m \equiv 1.0$, $f = 1/\sqrt{4\pi G}$, $\alpha \equiv 1.0$, Bogoliubov acoustic spectrum $1.45\text{--}1.88\text{ nHz}$, and the 175-galaxy SPARC Picard solver pipeline).
3. **Explicitly Protect Open Research Pathways (B12, B14):**
   - Agents and subagents MUST NOT treat investigating *driven non-linear Casimir backreaction* (`CBR-002`/`TOP-001`) or *physical star formation* (`ASTRO-001`) as forbidden research, provided all derivations obey dimensional consistency (Rule 4) and report exact measured results (Rule 1 & Rule 3).

## 7. Critical Path (Current Sprint)

```
Active priorities:
├─ TOP-001: Full 3D Epstein zeta Casimir tensor & moduli backreaction on T³
├─ WAK-001: Mode-projected Green function for non-equilibrium Bullet Cluster wake
└─ RES-001: Open-system Lindblad master equation for syntropic current Q^ν
```

## 8. What Agents Must NOT Do

1. **Fabricate results** — see GEMINI.md Rules 1, 3, 6
2. **Reverse-engineer constants** — see GEMINI.md Rule 2
3. **Write to the repository** if you are a subagent — see GEMINI.md Rule 8
4. **Promote claims beyond gate status** — e.g., do not claim $S_8$ is resolved or that free Casimir fields have a persistent $13/12$ attractor
5. **Treat active research frontiers as forbidden** — driven Casimir backreaction (`TOP-001`) and star formation (`ASTRO-001`) are open for rigorous modeling

## 9. Canonical Documents

| Document | Purpose |
|----------|---------|
| `GEMINI.md` | Scientific integrity rules (binding) |
| `active_research.md` | Authoritative gate dashboard |
| `Theory/Core/ITSM_Ban_List_Reassessment_and_Frontier_Policy.md` | Ban list reassessment & frontier policy |
| `Theory/Core/ITSM_Master_Research_Plan.md` | Master research workflow & identity |
| `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` | Publication firewall & claim limits |
| `Manuscript/ITSM_Core_Cosmology_v12.0.tex` | Official v12.0 core manuscript |

---

*This document is referenced by GEMINI.md Rule 7. Last updated: 2026-08-30 (v12.0 downstream gate clearance).*
