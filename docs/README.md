# ITSM site (`docs/`)

Multi-page recovery-era research site.

Current public gate snapshot: MAT-001 free-sector export and Track-A Conditional
`S_int` embed are complete as fail-closed partial passes. Track-A hosts matter
`d=(-C_m)`, `h=(0,0)` with symbolic `K_Q` only. Numeric `V` remains
`NOT_COMPUTED`; free-sector join and MAT physics PASS remain closed.

WAK-001 also remains Open: its common identity-route rubric selects none of
C1/C2/C3, with C2 retained only as the most developed calculation scaffold.

RES-001 likewise selects none of R1/R2/R3, retains R0 as control, and keeps
R1 as an unselected Conditional scaffold.

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
