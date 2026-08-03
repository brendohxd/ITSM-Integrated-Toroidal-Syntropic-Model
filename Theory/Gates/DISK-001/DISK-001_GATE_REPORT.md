# DISK-001 Gate Report — Methods package (Stages 0–4)

**Date:** 2026-08-03  
**Branch:** `recovery/v12-core-architecture`  
**Gate:** DISK-001  

| Field | Value |
|-------|--------|
| **Report status** | **PARTIAL PASS — methods package** |
| **Subgate tag** | `PASS_DISK001_METHODS_PACKAGE_STAGES_0_TO_4` |
| **Full Master Plan DISK-001** | **IN PROGRESS** (not closed for morphology-independent coupling claims) |
| **IR policy** | **Conditional** AQUAL-class; declared \(C_{\mathrm{obs}}=1\), phenomenological \(a_0\) |
| **MAT-001** | **BLOCKED** (upstream) |
| **P4** | **Not unlocked** (needs full DISK-001 + STAT-001) |

---

## 1. Executive summary (referee-facing)

DISK-001 now has a **reproducible numerical methods package** for Conditional
AQUAL-class dynamics under **explicitly declared** \((a_0,C_{\mathrm{obs}})\):

- algebraic sphere/disk benchmarks and curl diagnostics (Stage 0);  
- spherical AQUAL≡algebraic **identity theorem** + mass-integral convergence (Stage 1);  
- 2D midplane nonlinear AQUAL Poisson with **discrete residual** \(\varepsilon\sim10^{-9}\) and 2D log BC (Stage 2);  
- axisymmetric \((R,z)\) nonlinear AQUAL with residual \(\sim10^{-9}\) (Stage 3);  
- **domain-truncation sensitivity** \(\approx 4.8\%\) on interior midplane \(g(R)\) and midplane diagnostics (Stage 4).

This report **does not** claim:

- Derived \(\Cobs\) or topology-derived \(a_0\);  
- SPARC validation, global \(p\)-values, or cosmic \(H_0\) from galaxies;  
- dual RAR packaging \(a_0=cH_0/2\pi\) with \(C_{\mathrm{obs}}=2/3\) (**B9**);  
- full Master Plan closure of DISK-001 for morphology-independent coupling.

A hostile reader should treat Stages 0–4 as a **methods appendix**, not a
galactic-dynamics science result.

---

## 2. Declared inputs (must appear in any reuse)

| Input | Value used in package | Origin label |
|-------|----------------------|--------------|
| \(a_0\) | \(3700\,(\mathrm{km\,s^{-1}})^2\,\mathrm{kpc^{-1}}\) | `phenomenological_input` (≈ empirical MOND scale; **not** geometric derivation) |
| \(C_{\mathrm{obs}}\) | \(1.0\) | Conditional default (Master Plan §6); **not** MAT-001 matched |
| \(\mu(x)\) | \(x/\sqrt{1+x^2}\) | standard simple interpolating function |
| \(a_{0,\mathrm{eff}}\) | \(C_{\mathrm{obs}}^2 a_0\) | deep-MOND limit \(\lvert g\rvert=C_{\mathrm{obs}}\sqrt{a_0\lvert g_N\rvert}\) |

**B9 guard:** dual packaging with \(C_{\mathrm{obs}}=2/3\) and geometric \(a_0=cH_0/2\pi\) is refused in `disk001_ir_law.py`.

---

## 3. Master Plan pass condition vs this report

| Master Plan wording | Status in this package |
|---------------------|-------------------------|
| Periodic nonlinear solver | **Partial:** nonlinear AQUAL Poisson in 2D and axisymmetric \(R\)–\(z\); not a full 3D periodic box |
| Sphere + disk | **Yes (methods):** Plummer sphere; exp/sech² disk; thin midplane limits |
| Curl quantified | **Yes:** algebraic-map curl and potential-field curl (potential ≈ FD noise) |
| Morphology-independent coupling claim | **Forbidden** until full gate + STAT-001 |

**Verdict:** methods package **PASS**; full DISK-001 for P4 physics claims **not** PASS.

---

## 4. Stage ledger

| Stage | Tag | One-line result |
|-------|-----|-----------------|
| 0 | `PASS_DISK001_STAGE0_SCAFFOLD` | Algebraic AQUAL sphere/disk; curl of algebraic map measured |
| 1 | `PASS_DISK001_STAGE1_NONLINEAR_AQUAL` | Spherical identity theorem; 2D Picard FD (gradient residual, Stage-1 bar) |
| 2 | `PASS_DISK001_2D_AQUAL_STAGE2_RESIDUAL_BC` | Discrete \(\varepsilon\sim10^{-9}\); 2D log free-space BC |
| 3 | `PASS_DISK001_RZ_NONLINEAR_AQUAL` | Axisymmetric \(R\)–\(z\); residual \(\sim10^{-9}\); axis metric improves under refinement |
| 4 | `PASS_DISK001_BC_SENSITIVITY_MIDPLANE` | Domain sensitivity \(\approx 4.75\%\) interior; midplane boost \(\langle g/g_N\rangle\approx 2.38\) |

Detail notes:

- `DISK-001_STAGE0_SCAFFOLD.md`  
- `DISK-001_STAGE1_NONLINEAR_AQUAL.md`  
- `DISK-001_STAGE2_RESIDUAL_BC.md`  
- `DISK-001_STAGE3_RZ_AQUAL.md`  
- `DISK-001_STAGE4_BC_MIDPLANE.md`  

---

## 5. Quantitative highlights (from machine summaries)

### Residual (same discrete operator as solve)

- 2D Stage 2 (finest grids): \(\varepsilon \sim 10^{-9}\)  
- \(R\)–\(z\) Stage 3: \(\varepsilon \sim 10^{-9}\)  
- Stage 4 domains: \(\varepsilon \sim 10^{-9}\)

### Domain truncation (Stage 4)

- Penultimate \(R_{\max}=28\,\mathrm{kpc}\) vs largest \(40\,\mathrm{kpc}\):  
  max rel midplane \(\Delta g \approx 4.75\%\) for \(0.5 R_d \le R \le 7\,\mathrm{kpc}\).  
- Residual interpretation: monopole Dirichlet BC is **adequate at ~5%** for
  this interior annulus under the tested mass/scale; multipole BC would be
  needed to push well below that if a paper demands it.

### Potential vs algebraic AQUAL (Stage 4)

- Max rel difference \(\sim 30\%\) on the comparison annulus.  
- **Not a bug:** the nonlinear potential solution is not the algebraic map
  \(g=f(\lvert g_N\rvert)g_N\). Both are reported; only the potential field is
  used as the dynamical \(g=-\nabla\Phi\).

### Curl

- Potential \(g=-\nabla\Phi\): relative curl at FD noise (\(\sim 10^{-17}\) in 2D Stage 2).  
- Algebraic map: relative curl \(\sim 10^{-3}\) (contrast diagnostic).

---

## 6. Reproduction

```powershell
conda activate itsm_env
cd Analysis\DISK\DISK-001
python disk001_stage0_run_all.py
python disk001_stage1_run_all.py
python disk001_poisson_2d_aqual_stage2.py
python disk001_poisson_rz_aqual.py
python disk001_bc_sensitivity_midplane.py
```

Primary outputs under `Analysis/DISK/DISK-001/outputs/`.

Environment: project `itsm_env` (NumPy, SciPy). No random seeds (deterministic FD).

---

## 7. What remains for **full** DISK-001 PASS

| Item | Why |
|------|-----|
| Multipole (or free-space integral) outer BC | Reduce domain sensitivity below ~few % if required |
| Compact \(T^3\) compensated-source protocol (optional) | P1 hygiene if periodic cosmology box is claimed |
| Agreed full-pass numerical criteria signed in this report’s successor | Explicit thresholds for production use |
| STAT-001 | Required before P4 global inference |
| MAT-001 (for Derived IR lane) | Optional if staying Conditional for fits |

---

## 8. Claim hygiene for downstream papers

| Allowed now | Forbidden now |
|-------------|----------------|
| Cite as Conditional IR disk **methods** under declared inputs | “DISK proves morphology-independent ITSM coupling” |
| Use solver for controlled numerical experiments | Dual RAR (**B9**), SPARC-as-\(H_0\) (**B15**) |
| Point P4 authors to Stages 0–4 as infrastructure | Claim Derived \(\Cobs\) from this gate |

---

## 9. Decision

**PARTIAL PASS — methods package (Stages 0–4).**  

Full Master Plan DISK-001 remains **open**. P4 remains **gated** on full DISK
closure (as defined by the programme) **and** STAT-001.

Signed as gate documentation on branch `recovery/v12-core-architecture`
(commit to be recorded at push time).
