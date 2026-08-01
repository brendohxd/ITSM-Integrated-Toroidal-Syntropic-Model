# Paper directory and PDF naming (recovery era)

Canonical names match **paper identity** and include **content title + version**.

## PDF filename scheme (required for share / Zenodo / email)

```text
Boyd_<YYYY>_<ContentTitleSlug>_v<SEMVER>[-status].pdf
```

| Part | Rule | Example |
|------|------|---------|
| Author | `Boyd` | `Boyd` |
| Year | manuscript calendar year | `2026` |
| Content title slug | short, readable, no spaces; underscores between words; no hype slogans | `Present-Epoch_Scale_Matching_Cobs_Hygiene` |
| Version | from that paper’s `VERSION` file | `v0.1.0-draft` |

### Status tags (use when needed)

| Tag | When |
|-----|------|
| `draft` | pre-arXiv / internal (default now) |
| `preprint` | after public preprint DOI/arXiv |
| `submitted` | under review |
| `accepted` / `published` | post-acceptance; prefer journal version of record |

Bump `VERSION` when claims, tables, or figures change materially.  
Do **not** put “Geometric-Invariants” or “parameter-free” in filenames.

## Canonical table (current)

| ID | Directory | `VERSION` | Canonical PDF |
|----|-----------|-----------|---------------|
| **P1** | `papers/P1-Scale-Matching-Reconstruction/` | `0.1.0-draft` | `Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.1.0-draft.pdf` |
| **P2** | `papers/P2-Rectangular-T3-Casimir/` | `0.1.0-draft` | `Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Free-Field_Backreaction_v0.1.0-draft.pdf` |

Full titles (for metadata, not full filesystem strings):

- **P1:** Present-epoch scale matching, the weak-field invariant \(C_{\rm obs}\), and no-go results for a cubic \(T^3\) geometric story  
- **P2:** Anisotropic Casimir stress on rectangular flat \(T^3\) and the absence of a free-field \(H_t/H_p=13/12\) attractor  

## Build behaviour

- LaTeX still builds `main.pdf` (engine entry point).  
- Build scripts **also** write the canonical named PDF from `VERSION` + fixed content slug.  
- Old short names without year/version must not be reintroduced as the share name.

## Versioning advice

1. Start at `0.1.0-draft` for recovery-era drafts.  
2. `0.x.y` while claim set or figures move; `1.0.0-preprint` at first public archive; `1.0.0` only if you freeze a citable preprint record.  
3. Keep one `VERSION` file per paper directory (single line, no quotes).  
4. After each intentional bump, rebuild so the PDF filename matches `VERSION`.  
5. Zenodo / email / collaborators: attach the **canonical** named PDF, not only `main.pdf`.

## Renamed directories (do not reintroduce)

| Old path | Why wrong |
|----------|-----------|
| `papers/P1-Geometric-Invariants/` | Implies geometric invariants established |
| `papers/P2-Casimir-Backreaction/` | Less specific than rectangular \(T^3\) free-field scope |

## Related

- Selective publishing: `papers/Selective-Publishing-Plan/`  
- P2 arXiv: deferred pending endorsement  
