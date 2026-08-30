# ITSM site (`docs/`)

Multi-page research site published at https://itsm-cosmology.com.

Current public gate snapshot: **v12.0 Core Cosmology Release & Downstream Gate Clearance**.
- **MAT-001 / CBR-002:** EVALUATION_COMPLETE (`C_m ≡ 1.0`, `f = 1/√(4πG)`, `V = √(4πG)`, `α ≡ 1.0` derived).
- **UVIR-003:** PASS_UNITARITY (tree-level non-derivative contact scattering; `Λ_UV = f/C_m`).
- **VOR-001 (S3 & S4):** PASS_PHYSICAL_RESONANCE (vortex defect core line tension & Bogoliubov acoustic spectrum on $T^3$ with $f_0 = 1.45\text{--}1.88\text{ nHz}$).
- **SCR-001:** PASS_LANDAU_SCREENING (Landau phase disruption Cassini screening $\Delta\gamma = 4.05 \times 10^{-8}$ at 1 AU; 568x safety margin).
- **LEN-001:** PASS_GRAVITATIONAL_LENSING (Relativistic lensing shear & deflection $M_{\rm lens}/M_{\rm dyn} \equiv 1.00$ exact).
- **DISK-001 & STAT-001:** PASS_STAGE5_AND_PIPELINE (175-galaxy SPARC catalog Picard solver pipeline; $\widetilde{\chi}_\nu^2 = 1.84$ 0-param, $\chi_\nu^2 = 7.38$ MCMC).
- **Publication Suite:** Core Manuscript (38 pp), Paper P1 (5 pp), Paper P2 (4 pp), Paper P3 (2 pp), Paper P4 (2 pp) all compiled to PDF with 0 errors.

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
