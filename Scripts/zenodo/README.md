# Zenodo policy (recovery era)

## Decision (2026-08-02)

**Do not** deposit every gate micro-progression (CBR stage zips, UVIR subgate
slices, claim-hygiene mini-archives) — that clutters Zenodo.

**Do** deposit **paper packages** when a manuscript is ready for a public
archive (versioned share PDF + sources + checksums), e.g.:

| Paper | Directory | When to Zenodo |
|-------|-----------|----------------|
| **P1** | `papers/P1-Scale-Matching-Reconstruction/` | When you want a public DOI for the reconstruction note |
| **P2** | `papers/P2-Rectangular-T3-Casimir/` | After endorsement / arXiv path (or as preprint package if you choose) |
| Later P3/P4 | as written | After upstream gates close for their claims |

Gate numerics stay in **GitHub** (`Analysis/…`, `Theory/Gates/…`) until a paper
needs a citable freeze of its supporting code.

## Scrap prior segment deposits

```powershell
$env:ZENODO_TOKEN = 'YOUR_TOKEN'   # never commit; rotate if exposed
python Scripts/zenodo/scrap_gate_deposits.py --dry-run
python Scripts/zenodo/scrap_gate_deposits.py
```

Or delete manually: https://zenodo.org/me/uploads  
IDs listed in `scrap_gate_deposits.py`.

## Legacy tooling (optional)

Older scripts (`package_recovery_deposits.py`, `upload_recovery_deposits.py`,
`zenodo_deposit_metadata.py`) remain for reference but are **not** the default
workflow. Prefer paper-folder packaging when you do archive.
