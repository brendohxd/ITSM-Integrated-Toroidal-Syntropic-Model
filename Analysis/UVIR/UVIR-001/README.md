# UVIR-001 reproducible calculation

This directory audits the tree-level condensate-to-phonon matching of the
minimally kinetic complex scalar declared in the v12 core architecture.

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-001/uvir001_symbolic.py
```

Outputs are written to `outputs/`:

- `uvir001_summary.json` records exact symbolic expressions, validation tests,
  and the scientific verdict;
- `uvir001_parameter_grid.csv` checks representative stable branches
  numerically.

`Validation status: PASS` means that the symbolic identities and numerical
controls succeeded. It does **not** mean the microscopic candidate generated
the required ITSM operator. The hypothesis verdict is reported separately.
