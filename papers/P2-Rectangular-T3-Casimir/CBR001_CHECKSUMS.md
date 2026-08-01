# CBR-001 frozen artifact checksums (P2)

**Date:** 2026-08-01  
**Branch:** `recovery/v12-core-architecture`  
**Purpose:** reproducible anchors for Paper 2 tables/figures. Recompute after any CBR-001 code change.

Algorithm: SHA-256 (PowerShell `Get-FileHash -Algorithm SHA256`).

| Artifact | SHA-256 |
|----------|---------|
| `Analysis/Casimir/CBR-001/cbr001_stage1.csv` | `9E6874226FAA68E0397D48C31FAF3DD80F4C25CE8CA3102C5CD22D621D25BB5B` |
| `Analysis/Casimir/CBR-001/stage2_outputs/cbr001_stage2_scan.csv` | `9257F3A67CB577BF6ABD0DC29E53AB27C127AC602C26E66342D9D0F9125C6B13` |
| `Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_thresholds.csv` | `370B02480FF0E35DB0590D1793E88324D9622E98F3199C7D805F6A1ACD68EC8A` |
| `Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_summary.json` | `4AD9223CE32C5A30378610B11DE5263E8BE1DEE57BFBC94D085BBD392FED5281` |

## Stage-3B headline counts (from summary JSON)

| Class | Count (by initial shape) |
|-------|--------------------------|
| ATTRACTOR | 0 |
| QUASI_PLATEAU | 0 |
| TRANSIENT_CROSSING | 5 |
| NO_CROSSING | 2 |
| INVALID | 1 |

## Reproduce

```powershell
conda activate itsm_env
cd Analysis\Casimir\CBR-001
python casimir_t3_lattice.py
python cbr001_stage2_standalone.py
python cbr001_stage3_backreaction.py
python cbr001_stage3b_ratio_test.py
Get-FileHash stage3b_outputs\cbr001_stage3b_summary.json -Algorithm SHA256
```
