# CBR-001 Stage 2 — biaxial shape scan

Run from this directory with the repository Conda environment:

```powershell
conda activate itsm_env
python cbr001_stage2_standalone.py
```

The default scan covers `0.25 <= r <= 4`, where `r = Lt/Lp`, and always
includes the cubic point `r = 1`. It extrapolates each point using the validated
Stage-1 cutoff sequence and produces:

- `cbr001_stage2_scan.csv`
- `cbr001_stage2_stress.png`
- `cbr001_stage2_anisotropy.png`

Stage 2 maps `rho(r)`, `p_p(r)`, `p_t(r)`, and `p_t(r) - p_p(r)`. It does not
perform cosmological backreaction or test the `13/12` claim.
