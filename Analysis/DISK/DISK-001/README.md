# DISK-001 — Stage 0 scaffold (Conditional IR tooling)

**Gate status:** IN PROGRESS (Stage 0 only)  
**IR policy:** Conditional AQUAL-class with **declared** `C_obs ~ 1` and phenomenological `a0`  
**Not:** Derived `C_obs`, SPARC validation, full DISK-001 PASS

## Run

```powershell
conda activate itsm_env
cd Analysis\DISK\DISK-001
python disk001_stage0_run_all.py   # algebraic benchmarks
python disk001_stage1_run_all.py   # nonlinear AQUAL methods package
python disk001_poisson_2d_aqual_stage2.py  # Stage 2 residual+BC tightening
python disk001_poisson_rz_aqual.py         # Stage 3 axisymmetric R–z AQUAL
```

## Modules

| Script | Role |
|--------|------|
| `disk001_ir_law.py` | Declared IR + simple-μ AQUAL helpers (B9 guard) |
| `disk001_sphere_benchmark.py` | Plummer sphere deep-MOND / AQUAL checks |
| `disk001_disk_midplane.py` | Thin exponential disk midplane boost |
| `disk001_curl_residual.py` | 2D curl residual of algebraic AQUAL map |
| `disk001_stage0_run_all.py` | Stage 0 suite |
| `disk001_sphere_nonlinear_aqual.py` | Spherical AQUAL≡algebraic identity + mass convergence |
| `disk001_poisson_2d_aqual.py` | 2D nonlinear AQUAL Poisson (Picard FD, Stage 1) |
| `disk001_poisson_2d_aqual_stage2.py` | Stage 2: discrete residual + 2D log BC + convergence CSV |
| `disk001_poisson_rz_aqual.py` | Stage 3: axisymmetric \((R,z)\) nonlinear AQUAL |
| `disk001_stage1_run_all.py` | Stage 1 suite |

## Outputs

`outputs/disk001_*_summary.json` and sample curves.

## Authority

- `Theory/Gates/DISK-001/DISK-001_READINESS.md`
- Master Plan §6 (Conditional AQUAL baseline)
- Selective Publishing B1/B9/B15 (no dual RAR, no SPARC-as-H0)
