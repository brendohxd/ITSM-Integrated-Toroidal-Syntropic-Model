# Zenodo recovery deposits — 2026-08-02

**P2 arXiv:** skipped (endorsement pending)  
**Paper paths:** see `papers/PAPERS_NAMING.md`  
**Metadata source:** `Scripts/zenodo/zenodo_deposit_metadata.py`  
(inclusive descriptions; ORCID; website; GitHub; legacy DOI links)

## Records (after metadata refresh)

| Package | Status | ID | Review URL |
|---------|--------|-----|------------|
| CBR-001 | Published v1 + **new-version draft** (inclusive meta) | draft `21753798` (was `21745260`) | https://zenodo.org/uploads/21753798 |
| UVIR-003 | Published v1 + **new-version draft** | draft `21753799` (was `21745270`) | https://zenodo.org/uploads/21753799 |
| Claim hygiene | **Draft** (meta updated in place) | `21745276` | https://zenodo.org/uploads/21745276 |

See `ZENODO_LATEST_DRAFTS.json` and `ZENODO_METADATA_UPDATE.json`.

## Shared author metadata (all three)

- **Creator:** Boyd, Brendon  
- **ORCID:** https://orcid.org/0009-0007-4177-2612  
- **Website:** https://www.itsm-cosmology.org  
- **GitHub:** https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model  
- **Contact:** brendon.boyd@itsm-cosmology.org  
- **License:** CC-BY-4.0  

## Publish later

Review the draft URLs in the Zenodo UI, then click **Publish** for each new
version when ready (CBR/UVIR drafts supersede v1 metadata; claim-hygiene is
still first public version when published).

```powershell
# Re-apply metadata only (no publish):
$env:ZENODO_TOKEN = '...'   # never commit; rotate if pasted in chat
python Scripts/zenodo/update_zenodo_draft_metadata.py
```
