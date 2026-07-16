# UVIR-002 route comparison

This calculation compares three successor routes after UVIR-001 rejected the
minimal canonical single-complex-scalar matching candidate:

1. a nonrelativistic gradient-dominated single-field branch;
2. a two-field split between background density and force mediation;
3. a preferred-frame force EFT with independent temporal and spatial
   invariants.

Run from the repository root:

```powershell
python Analysis/UVIR/UVIR-002/uvir002_route_comparison.py
```

Outputs are written to `outputs/`:

- `uvir002_summary.json` contains the symbolic identities and gate statuses;
- `uvir002_route_scores.csv` records the comparison criteria and verdicts.

`STATUS: PASS` means the comparison calculation reproduced its analytic
checks. It does not mean that UV microscopic closure has passed. The selected
two-sector preferred-frame architecture remains provisional and must pass
UVIR-003 before MAT-001 can begin.
