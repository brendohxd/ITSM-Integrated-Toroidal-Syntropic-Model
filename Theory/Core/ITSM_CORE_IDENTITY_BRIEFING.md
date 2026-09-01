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
| **UVIR-003** | **IN_PROGRESS** | Stage 5 holds tier-1 closure (M2/M3/M6/M7 hold); physical interaction scale, matching, and EFT cutoff remain open |
| **MAT-001** | **BLOCKED** | Conditional Track-A form kit only; $V = C_m/\sqrt{K_Q}$ not computed; parent $Z_\phi, g_\phi$ incomplete |
| MAT-001 R1–R4 | COMPLETE | Convention, provenance, action, residue contract |
| MAT-001 R5 | RESEARCH_FORK | Scale-compensator exploratory fork; parent matching remains underdetermined |
| TOP-001 / CBR-002 | SCOPED_NEGATIVE | Free Casimir energy dilutes to isotropy; persistent $13/12$ is an unstable driven toy model |
| VOR-001 | OPEN SCAFFOLD | Bogoliubov acoustic phonons on $\mathbb{T}^3$; macroscopic circulation matching open |
| SCR-001 | OPEN | Universal coupling unproven; Landau disruption is an unverified heuristic mechanism |
| LEN-001 | OPEN | Lensing potentials, metric, and wave propagation unclosed downstream of $V$ |
| DISK-001 | METHODS_ONLY | Conditional AQUAL/Picard methods plus a repaired algebraic SPARC comparator; no morphology-independent ITSM coupling derived |
| STAT-001 | NOT_STARTED_AS_CLOSED_GATE | Invalid optimizer/MCMC claims quarantined; repaired comparator is optimization-only with raw likelihood separated from priors |
| WAK-001 | KINEMATIC_RETARDED_FIELD_CONTROL_ONLY | Dimensionally consistent 3D scalar-field control with prescribed sources; no hydrodynamics, shocks, or lensing observable |
| RES-001 | PHENOMENOLOGICAL_TWO_BATH_GKSL_CONTROL_ONLY | Detailed-balance thermal GKSL comparator; no microscopic ITSM Hamiltonian or $Q^\mu$ |
| ASTRO-001 | NEWTONIAN_SINGLE_SCALE_LOGNORMAL_CONTROL_ONLY | Unclipped Newtonian Jeans/lognormal baseline fails to yield a Salpeter tail; no ITSM IMF or mass-to-light prediction |
| COS-001 / PERT-001 | PROXY_CALIBRATION_ONLY | Unmodified CAMB $\Lambda$CDM reference only; no ITSM Boltzmann hierarchy, transfer functions, or $S_8$ prediction |

### Current Canonical Boundary (v12.0-alpha.12 Baseline)

In the canonical v12.0-alpha.12 authority baseline:
- **$V = C_m/\sqrt{K_Q}$** remains **`NOT_COMPUTED`**
- **$K_Q$** remains **`NOT_DERIVED`**
- **$\text{MAT-001}$** remains **`BLOCKED`**
- **$\text{UVIR-003}$** remains **`IN_PROGRESS`** (Tier-1 hold)
- **Downstream "Derived" claims** for screening, lensing, disk dynamics, and cosmology are strictly forbidden until upstream gates close.

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
2. **Retain the Derived-claim firewall (B1, B7/B8/B9, B13, B15):**
   - These research topics may be investigated, but their historical or reintegrated numerical packaging is **not cleared as Derived**. In particular, $f$, $\alpha$, $V$, $a_0$, a physical PTA mode, and an ITSM SPARC prediction remain blocked or conditional under their parent gates.
3. **Explicitly Protect Open Research Pathways (B12, B14):**
   - Agents and subagents MUST NOT treat investigating *driven non-linear Casimir backreaction* (`CBR-002`/`TOP-001`) or *physical star formation* (`ASTRO-001`) as forbidden research, provided all derivations obey dimensional consistency (Rule 4) and report exact measured results (Rule 1 & Rule 3).

## 7. Critical Path (Current Sprint)

```
Active priority:
└─ PKM1: one bounded A0–A6 metric-hosted condensate-foliation parent test
   ├─ full ADM/Dirac count at Y>0 and Y=0
   ├─ reduced Hamiltonian, characteristics, cutoff and source response
   └─ only a survivor may open PPN/lensing/GW/topology tests
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

*This document is referenced by GEMINI.md Rule 7. Last updated: 2026-09-01 (fail-closed c50 repair; no downstream gate clearance).*
