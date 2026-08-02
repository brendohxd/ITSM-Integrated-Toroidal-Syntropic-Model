# Scrap segment deposits — paper-only Zenodo

**Decision:** Do not keep (or re-upload) small gate-progression deposits.
They clutter Zenodo. Public archives should track **papers** (P1, P2, …), not
every CBR/UVIR subgate zip.

## Records to remove (owner)

| ID | Record | Notes |
|----|--------|-------|
| 21745260 | CBR-001 v1 | published |
| 21745270 | UVIR-003 v1 | published |
| 21745276 | Claim hygiene | draft |
| 21753798 | CBR-001 new version draft | draft |
| 21753799 | UVIR-003 new version draft | draft |

```powershell
$env:ZENODO_TOKEN = 'YOUR_TOKEN'   # never commit
python Scripts/zenodo/scrap_gate_deposits.py --dry-run
python Scripts/zenodo/scrap_gate_deposits.py
```

Or: https://zenodo.org/me/uploads → delete each.

## Keep in Git

All science remains under `Analysis/`, `Theory/Gates/`, `papers/`.
