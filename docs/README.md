# ITSM site (`docs/`)

Multi-page recovery-era research site.

Current public gate snapshot: Tier-1 peer-review readiness audit **retains**
the Stage 5 hold (M2/M3/M6/M7 unmet). Track-A Conditional MAT kit and dual-status
probes exist; Derived `V`/`K_Q` remain NOT_COMPUTED/NOT_DERIVED; Stage 4A closed;
MAT physics PASS forbidden.

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
