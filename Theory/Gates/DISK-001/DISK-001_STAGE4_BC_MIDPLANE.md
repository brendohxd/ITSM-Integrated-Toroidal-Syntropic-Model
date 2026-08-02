# DISK-001 Stage 4 — BC domain sensitivity + midplane \(g(R)\)

Date: 2026-08-03  
Branch: `recovery/v12-core-architecture`  
Status: **PASS** (`PASS_DISK001_BC_SENSITIVITY_MIDPLANE`)  
Full DISK-001 gate: **IN PROGRESS**

## Purpose

Quantify the leading outer-boundary truncation error of the Stage-3 monopole
Dirichlet condition, and document midplane accelerations under Conditional IR
in a form a methods referee can audit.

This is **domain-truncation sensitivity**, not a full multipole expansion on
\(\partial\Omega\). That limitation is stated explicitly.

## Method

- Solver: Stage-3 axisymmetric \(R\)–\(z\) Picard AQUAL (same discrete residual).  
- Domains: \(R_{\max}\in\{16,20,28,40\}\,\mathrm{kpc}\), \(Z_{\max}=0.4\,R_{\max}\).  
- Resolution: \(n_R\) scaled to keep \(\Delta R\) roughly fixed.  
- Sensitivity metric: max relative difference in midplane \(|g|(R)\) for
  \(0.5 R_d \le R \le 7\,\mathrm{kpc}\) between each domain and the largest.  
- Midplane diagnostics on largest domain: \(\langle g/g_N\rangle\), potential vs
  algebraic AQUAL map difference, outer \(v_c=\sqrt{gR}\) flatness.

## Results

| \(R_{\max}\) | residual | max rel \(\Delta g\) vs \(R_{\max}=40\) (interior) |
|-------------:|---------:|--------------------------------------------------:|
| 16 | \(\sim10^{-9}\) | (vs largest; see CSV) |
| 20 | \(\sim10^{-9}\) | … |
| 28 | \(\sim10^{-9}\) | **\(4.75\%\)** (penultimate vs largest) |
| 40 | \(\sim10^{-9}\) | reference |

Largest-domain midplane (Conditional \(C_{\mathrm{obs}}=1\)):

- mean \(g/g_N\) boost \(\approx 2.38\) on the comparison annulus,  
- max \(|g_{\mathrm{pot}}-g_{\mathrm{alg}}|/g_{\mathrm{pot}}\approx 0.30\)  
  (expected: algebraic map \(\neq\) nonlinear potential solution).

Pass criteria: residual \(<10^{-3}\), domain sensitivity \(<5\%\), boost \(>1.02\).

## Reproduction

```powershell
python Analysis\DISK\DISK-001\disk001_bc_sensitivity_midplane.py
# expect: PASS_DISK001_BC_SENSITIVITY_MIDPLANE
```

Outputs:

- `outputs/disk001_bc_sensitivity_midplane_summary.json`
- `outputs/disk001_stage4_domain_sensitivity.csv`
- `outputs/disk001_midplane_gR_largest_domain.csv`

## Scientific boundary

- Conditional IR; not Derived \(\Cobs\); not SPARC.  
- Monopole BC remains; sensitivity bounds truncation, does not remove it.  
- Full DISK-001 PASS still requires formal gate-report sign-off and any extra
  criteria you choose (e.g. multipole BC, external code comparison).

## Next

1. Optional multipole BC  
2. Optional declared-input single-galaxy diagnostic  
3. `DISK-001_GATE_REPORT.md` when full-pass criteria are agreed  
