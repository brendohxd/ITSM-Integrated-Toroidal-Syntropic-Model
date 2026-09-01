# CBR-001 — Stage 1 numerical validation

CBR-001 Stage 1 status: PASS

This package contains the periodic rectangular-`T^3` Casimir lattice solver and
the successful cubic-cutoff ledger used to validate the mathematical engine.

## Validated

- cutoff convergence
- cubic isotropy
- thermodynamic pressure derivative
- conformal trace
- permutation symmetry
- dimensional scaling

No cosmological backreaction or 13/12 claim tested at this stage.

## Run

From this directory, using the repository Conda environment:

```powershell
conda activate itsm_env
python casimir_t3_lattice.py
```

The default case is the symmetric cube `L1 = L2 = L3 = 1`. The run should end
with `STATUS: PASS`.

For the first biaxial anisotropy smoke test:

```powershell
python casimir_t3_lattice.py `
  --lengths 1 1.25 1.25 `
  --csv cbr001_r1p25.csv
```

This case should satisfy `p1 != p2` and `p2 = p3`.
