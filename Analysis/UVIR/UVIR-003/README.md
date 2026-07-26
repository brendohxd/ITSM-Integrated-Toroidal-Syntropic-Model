# UVIR-003 Stage A and Stage B diagnostics

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

The bounded Stage B diagnostics are:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_frame_sector_speeds.py
python Analysis/UVIR/UVIR-003/uvir003_zero_gradient_force_block.py
python Analysis/UVIR/UVIR-003/uvir003_causality_check.py
python Analysis/UVIR/UVIR-003/uvir003_force_strong_coupling_estimate.py
python Analysis/UVIR/UVIR-003/uvir003_conditional_kq_estimate.py
```

The zero-gradient force-block check proves quadratic factorization only for
the declared Stage-A truncation. It finds one positive `z=2` force scalar for
`K_Q > 0` and `gamma > 0`, while showing that `K_Q` alone is not identifiable
until a physical field normalization is fixed by microscopic or matter
matching. The remaining metric-aether-condensate reduction, nonzero-gradient
mixing, covariant regulator and physical cutoff remain open.
