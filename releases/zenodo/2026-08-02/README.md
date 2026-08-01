# Zenodo recovery deposits — 2026-08-02

**Status:** uploaded as **drafts only** (not published)  
**Branch/commit:** `recovery/v12-core-architecture` @ `a57ed29`  
**P2 arXiv:** skipped (endorsement pending)

## Draft uploads

| Package | Deposition | Reserved DOI (active after publish) | Review URL |
|---------|------------|-------------------------------------|------------|
| CBR-001 Casimir gate | `21745260` | `10.5281/zenodo.21745260` | https://zenodo.org/uploads/21745260 |
| UVIR-003 four-leg slice | `21745270` | `10.5281/zenodo.21745270` | https://zenodo.org/uploads/21745270 |
| Recovery claim hygiene | `21745276` | `10.5281/zenodo.21745276` | https://zenodo.org/uploads/21745276 |

`published: false` in `ZENODO_UPLOAD_RESULTS.json`.

## Local packages

See `INDEX.json` and the three zip archives in this folder.

## Publish later (manual or script)

```powershell
# After reviewing drafts in the Zenodo UI, either click Publish there, or:
$env:ZENODO_TOKEN = '...'   # do not commit; rotate if ever pasted in chat
python Scripts/zenodo/upload_recovery_deposits.py `
  --package-dir releases/zenodo/2026-08-02 --publish
```

Prefer **UI publish** if drafts already exist (the upload script always creates *new* depositions).
