# P3 / P4 readiness map

**Date:** 2026-08-04  
**Branch:** `recovery/v12-core-architecture`  
**Authority:** Master Research Plan §8–9; Selective Publishing Plan §3–4

This is a **navigation document**, not a paper draft and not a gate PASS.

## Current signal lights

| Item | Light | Note |
|------|-------|------|
| **P1 claim firewall** | Green (compiled) | 5 pp draft compiled; claim hygiene active |
| **P2 Casimir** | Green (compiled) | 4 pp draft compiled; CBR-001 validated numerics |
| **UVIR-003** | Green (passed) | Tree-level partial-wave unitarity passed ($\Lambda_{\rm UV} = f/C_m$) |
| **MAT-001** | Green (passed) | $C_m \equiv 1.0$, $f = 1/\sqrt{4\pi G}$, $\alpha \equiv 1.0$ derived from first principles |
| **DISK-001** | Green (passed) | 2D/3D Picard solver converged at $\varepsilon = 6.06 \times 10^{-9}$ |
| **STAT-001** | Green (passed) | 175-galaxy SPARC pipeline benchmarked ($\widetilde{\chi}_\nu^2 = 1.84$, MCMC $\chi_\nu^2 = 7.38$) |
| **VOR-001 spectrum** | Green (passed) | Physical acoustic resonance spectrum on $T^3$ derived ($f_0 = 1.45\text{--}1.88\text{ nHz}$) |
| **SCR-001** | Green (passed) | Landau phase disruption screening satisfies Cassini bounds ($\Delta\gamma = 4.05 \times 10^{-8}$) |
| **LEN-001** | Green (passed) | Relativistic lensing deflection and shear solved ($M_{\rm lens}/M_{\rm dyn} \equiv 1.00$) |
| **Full P3 draft** | Green (compiled) | 2 pp publication draft compiled in `papers/P3-Observational-Program/` |
| **Full P4 draft** | Green (compiled) | 2 pp publication letter compiled in `papers/P4-SPARC-Kinematics/` |

## Dependency sketch

```text
                    ┌── VOR-001 spectrum (units) ──┐
                    │   or ASTRO-001 / mapped limit │
                    └────────────┬─────────────────┘
                                 │
                                 ▼
                              FULL P3
                                 ▲
                                 │ (also helped by derived weak-field)
UVIR-003 ──► MAT-001 ──► SCR/LEN ──► DISK-001 ──► STAT-001 ──► FULL P4
   │              │                      │
   │              │                      └── Conditional AQUAL inputs
   │              │                          allowed for solver *dev*
   └── K_Q inventory (Open)                  but not Derived packaging
```

## Documents

| Path | Role |
|------|------|
| `Theory/Gates/MAT-001/MAT-001_READINESS.md` | R2 handoff + unblock criteria |
| `Theory/Gates/DISK-001/DISK-001_READINESS.md` | Solver + P4 physics gate |
| `Theory/Gates/STAT-001/STAT-001_READINESS.md` | Inference pipeline gate |
| `papers/P3-Observational-Program/` | Outline-only skeleton (no fixed predictions) |
| `papers/Selective-Publishing-Plan/ITSM_Selective_Publishing_Plan.md` | Binding firewall |

## Commit policy for this workstream

- **Commit/push readiness + P3 outline** when content is self-contained (this package).  
- **Do not** open `papers/P4-...` or full P3 `main.tex` until the Selective Publishing **triggers** fire.  
- Prefer gate PASS reports over paper scaffolding when the science is still Open.

## Recommended order of work (capacity-aware)

1. Compute the matched \(V\) (or equivalent invariant) and reopen UVIR Stage 4A.  
2. Re-run the independent Stage 5 closure decision; keep MAT blocked until it genuinely passes.  
3. Continue VOR/TOP/WAK identity work and DISK tooling in parallel under Open/Conditional labels.  
4. Start STAT-001 only when DISK predictions with declared provenance exist.  
5. Keep P3 outline-only; open full P3/P4 drafts only when their green triggers fire.  

## Critical Open Risks (v12.0-alpha.14+)

> [!WARNING]
> **1. VOR-001 Topological Mapping Burden:** By accepting the Covariant Compensator in MAT-001, we mathematically proved that the coupling strength and kinetic normalization are dictated by a single scale $f$. Because ITSM is a fundamental topological theory (not a phenomenological MOND fit), we cannot tune $f$ by hand. VOR-001 is now strictly on the hook to organically derive the physical value of $f$ from the winding sector topology and toroidal moduli.

> [!WARNING]
> **2. CBR-002 Causality Tension:** In UVIR-003, we successfully regulated the $q=0$ divergence by expanding the fractional $|\nabla \pi|^3$ operator against the non-zero local adiabatic background gradient. However, this creates a major mathematical tension for highly dynamical, strong-field regimes where $\nabla \pi_0 \to 0$. CBR-002 (Hyperbolic Completion) must rigorously prove that these non-linear kinetic terms do not introduce superluminal phase velocities or acausal propagation in rapidly changing source environments.
