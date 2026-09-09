# P2 hostile internal read (Track A)

> [!CAUTION]
> **Superseded 2026-09-05.** The `GO` below is withdrawn. The Tier-1 re-audit
> found stale artifact hashes, a Stage-2 scale-convention mismatch, an
> underived physical mapping for `epsilon`, and overly broad free-field
> language for an instantaneous `a^-4` stress closure. See
> `Theory/Gates/TOP-001/P2_CBR001_TIER1_HOSTILE_REAUDIT_2026-09-05.md`.

**Date:** 2026-08-01  
**Reader role:** tier-1 referee style, claim firewall  
**Manuscript:** `papers/P2-Rectangular-T3-Casimir/main.tex`  
**Firewall:** Selective Publishing B1–B16  

## Verdict

**Historical verdict withdrawn.** The current candidate remains on publication
hold pending independent Role-A/Role-B review, sensitivity checks and an
independent noncubic evaluator.
Not overclaiming attractor / H0 / a0. Science rests on CBR-001 Stages 1–3B.

## Ban-list skim (abstract + conclusions)

| Ban | Status |
|-----|--------|
| B1–B3 geometric a0 | Clean — explicitly denied |
| B4–B6 super-horizon L=c/H0 as model | Clean — rectangular lattice only; CMB separate |
| B7–B9 projector / C_obs | Clean — not discussed as positive |
| B10 doughnut T3 | Clean — rectangular fundamental domain |
| B12 13/12 attractor or 72.97 prediction | Clean — historical packaging only; transient only |
| B13–B15 PTA/JWST/SPARC | Clean — out of scope |
| B16 zero free params | Clean |

## Findings (severity)

### Must fix (applied)

1. **Undefined $\kappa$** in shear/Hamiltonian equations — define $\kappa=8\pi G$.  
2. **$\epsilon$ amplitude** used in table without one-line definition linking to Stage-3A dimensionless Casimir fraction.  
3. **Bibliography after appendix** — move `\bibliography` before appendix for revtex hygiene, or keep single trailing bib (kept trailing; rebuild OK). Prefer bibliography before appendix if rebuild complains.

### Should fix (applied)

4. One-sentence **data/code availability** in conclusions pointing at CBR-001 + checksums.  
5. Explicit that **$H_t=72.97$** appears only as historical packaging under test, not as a secondary result.  
6. State Stage-3A de Sitter + small-source scope again in conclusions.

### Optional / later

7. Full Edery formula cross-check against code comment block (ledger already PASS Stage-1).  
8. External co-reader before journal submit.  
9. Zenodo DOI freeze of CBR-001 outputs at arXiv time.

## Positive

- Correct T³ rectangular figure discipline.  
- Classification vocabulary matches Stage-3B.  
- Companion P1 cited only for hygiene.  
- CBR-002 left open honestly.  
- Checksums appendix present.

## Go / no-go for arXiv

| Gate | Status |
|------|--------|
| Claim firewall | **GO** |
| Reproducibility anchors | **GO** |
| Cover letter | **GO** |
| Hostile fixes | **GO** (this pass) |
| External co-author/read | optional |
