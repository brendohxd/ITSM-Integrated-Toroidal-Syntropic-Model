# UVIR-003 Stage A

Stage A declares the preferred-frame architecture and validates necessary
flat-background decoupling-limit conditions for:

- an independently dynamical unit timelike frame aligned with, but not
  algebraically identified with, the condensate current;
- the four-operator Einstein-aether kinetic basis;
- a force scalar with independent temporal and spatial invariants;
- a higher-spatial-derivative candidate regulator for the zero-gradient limit.

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_stage_a.py
```

Outputs:

- `outputs/uvir003_stage_a_summary.json`
- `outputs/uvir003_stage_a_checks.csv`

`STATUS: PASS` validates Stage-A algebra. It does not close UVIR-003. The full
metric/aether/condensate constraint reduction, strong-coupling calculation and
matter coupling remain outstanding, so MAT-001 stays blocked.
