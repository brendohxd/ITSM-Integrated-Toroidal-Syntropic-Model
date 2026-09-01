# MAT-001 Conditional matching branch (dual status)

**Status:** `PASS_MAT001_CONDITIONAL_MATCHING_BRANCH_OPEN_DUAL_STATUS`  
**Conditional branch:** `OPEN_CONDITIONAL_DUAL_STATUS`  
**Derived V:** **NOT_COMPUTED**  
**Derived $K_Q$:** **NOT_DERIVED**  
**MAT-001:** **BLOCKED**  
**Stage 4A:** **CLOSED**  
**Physics pass:** `false`

## Dual status

| Layer | Fields |
|---|---|
| **Derived / claim** | `V_status=NOT_COMPUTED`, `kq_numeric_status=NOT_DERIVED`, `mat001_pass=false`, Stage 4A closed |
| **Conditional probe** | Labeled `CONDITIONAL_ONLY` samples under explicit premises (`C_obs~1`, `C_IR=2/3`, optional R1 $k_Q$ or free $V$) |

Conditional numerics are **priority diagnostics only**. They must not be packaged as Derived, MAT PASS, or Stage 4A reopen.

## Reproduction

```text
python -B Analysis/MAT/MAT-001/CONDITIONAL_MATCHING_BRANCH/mat001_conditional_matching_branch.py
# STATUS: PASS_MAT001_CONDITIONAL_MATCHING_BRANCH_OPEN_DUAL_STATUS
# SHA-256: 1BB9DE0646CDA8A8C577B19D37B6DFE1D04B29A3AECBA182519BC93A431975EC
```
