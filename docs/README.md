# ITSM site (`docs/`)

Multi-page recovery-era research site.

Current public gate snapshot: MAT-001 live-export inventory completed fail closed;
partial cross-chart matrices do not yet form the required same-action bundle and
`V` remains `NOT_COMPUTED`.

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
```powershell
cd docs
python -m http.server 8080
```
