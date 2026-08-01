# Zenodo recovery deposits

P2 arXiv is deferred (endorsement pending). Use these scripts to archive
validated **gate packages** and **claim-hygiene docs** on Zenodo instead.

## 1. Package

```powershell
conda activate itsm_env
cd <repo-root>
python Scripts/zenodo/package_recovery_deposits.py --git-sha (git rev-parse --short HEAD)
```

Output: `releases/zenodo/YYYY-MM-DD/`

| Zip | Content |
|-----|---------|
| `ITSM_CBR-001_Casimir_T3_v1.0.0.zip` | Stages 1–3B Casimir + backreaction |
| `ITSM_UVIR-003_LocalFourLeg_v0.10.0-pre.zip` | Four-leg / deformation / packet proxy |
| `ITSM_Recovery_ClaimHygiene_v1.3.0.zip` | Master plan, firewall, P1 reconstruction |

## 2. Upload

```powershell
# Token: https://zenodo.org/account/settings/applications/
# Scopes: deposit:write  (+ deposit:actions to publish)
$env:ZENODO_TOKEN = 'YOUR_TOKEN'   # never commit

# Draft only (recommended first):
python Scripts/zenodo/upload_recovery_deposits.py `
  --package-dir releases/zenodo/YYYY-MM-DD

# Publish after reviewing drafts in the Zenodo UI:
python Scripts/zenodo/upload_recovery_deposits.py `
  --package-dir releases/zenodo/YYYY-MM-DD --publish
```

Creates **new** depositions (does not version the legacy v11 Cosmology DOI).

## 3. Record DOIs

After publish, copy DOIs into:

- `releases/zenodo/YYYY-MM-DD/ZENODO_UPLOAD_RESULTS.json` (auto)
- `Theory/Core/ITSM_Master_Research_Plan.md` related links
- optional README badge later

## Security

Never commit `ZENODO_TOKEN` or `zenodo_secrets.json`.
