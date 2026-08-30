# ITSM site (`docs/`)

Multi-page research site published at https://itsm-cosmology.com.

Current public gate snapshot: **v12.0 Core Cosmology Release**.
- **MAT-001 / CBR-002:** EVALUATION_COMPLETE (`C_m ≡ 1.0`, `f = 1/√(4πG)`, `V = √(4πG)`, `α ≡ 1.0` derived).
- **UVIR-003:** PASS_UNITARITY (tree-level non-derivative contact scattering; `Λ_UV = f/C_m`).
- **DISK-001:** PASS_STAGE5 (2D/3D nonlinear AQUAL Picard solver converged at `ε = 6.06 × 10⁻⁹`).
- **STAT-001:** DIAGNOSTIC_BENCHMARK (`χ² = 18,092` clean Q1+Q2 with 0 global free parameters; `χ²_ν = 7.38` floated MCMC).
- **Active Downstream Queue:** SCR-001 (screening), LEN-001 (lensing), TOP-001 (3D Epstein Casimir tensor), and galaxy-by-galaxy DISK-001 pipeline.

| Page | Purpose |
|------|---------|
| `index.html` | Home / entry |
| `vision.html` | Aims, positioning, pillars, success criteria |
| `architecture.html` | Sectors & separations |
| `research.html` | Gate map & freeze status |
| `papers.html` | P1–P4 programme |
| `claims.html` | Status labels & three buckets |
| `reproduce.html` | Clone & run gates |

**Live domain:** https://itsm-cosmology.com  
**Deploy:** `gh-pages` branch root (see repo Settings → Pages)

## Visual assets

The assets/web/*_v2.png figures are purpose-built conceptual illustrations
for the recovery-era site. They are not numerical outputs, observational
evidence, or replacements for executable gate reports. Earlier assets are
retained as provenance and fallback material.

The shared background adds a slow CSS-only toroidal field and star drift. This
motion is decorative rather than a numerical simulation, does not receive
pointer input, and remains static when the visitor requests reduced motion.

```powershell
cd docs
python -m http.server 8080
```
