# CBR-001 portable candidate checksums (P2)

**Date:** 2026-09-09
**Branch:** `recovery/v12-core-architecture`  
**Status:** candidate internal freeze; independent Role-A/Role-B audits pending
**Gate effect:** none
**Algorithm:** SHA-256

These hashes identify the repaired code/output candidate used by the P2 draft.
They do not establish a physics pass or authorize release.

## Portability contract

- Every CSV writer fixes `lineterminator="\n"`; hashes do not depend on the
  host operating system's default record terminator.
- Stage-3A and Stage-3B JSON output paths are filenames relative to the summary
  directory. No absolute workstation path is serialized.
- The two-run harness creates clean OS-temporary source copies and uses
  explicit Stage-2 paths, preventing a fresh Stage-2 run from being bypassed by
  a stale tracked `stage2_outputs/` file.
- PNG bytes are frozen for the recorded environment; a different Matplotlib or
  Pillow stack may render equivalent data to different bytes.

Recorded environment:

```text
Python 3.13.9
NumPy 2.4.6
SciPy 1.17.1
Matplotlib 3.10.9
```

## Frozen candidate source

| Artifact | SHA-256 |
|---|---|
| `Analysis/Casimir/CBR-001/casimir_t3_lattice.py` | `5f0515fab37cdfc0de837bcbc36011260815c5275dc6755a3226144811f04b87` |
| `Analysis/Casimir/CBR-001/cbr001_stage2_standalone.py` | `433bd620acfc20c61fb71df208890008537955ef99577d1524bb2bca35dbd153` |
| `Analysis/Casimir/CBR-001/cbr001_stage3_backreaction.py` | `8d1cbd56470f7a1ee06287fa8c467bb3f4b7140a78bc938d12a63843c57ff523` |
| `Analysis/Casimir/CBR-001/cbr001_stage3b_ratio_test.py` | `63d6b0c3ac76fb93d68388205fa6cdea9563796faec48ccaacf1b81eff0e21c5` |
| `Analysis/Casimir/CBR-001/p2_reproduction_a0_harness.py` | `fddef971ccb5a8a734c0b04dc563bfb1e6f8d2c8c03003cd80d6d59ff6cf76f1` |

## Frozen manuscript candidate

| Artifact | SHA-256 |
|---|---|
| `papers/P2-Rectangular-T3-Casimir/main.tex` | `49f1cf6c6ddd0a83d3dc5fe0f0323a47a84f2554baaaeed26c2f43df7458120e` |
| `papers/P2-Rectangular-T3-Casimir/references.bib` | `4ee33f31f5ec9bbbf1ced19d8eab4a76525544fa6ba13f499bbd1f26fe744426` |
| `papers/P2-Rectangular-T3-Casimir/Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control_v0.1.0-draft.pdf` | `000c3b047bd7d1b189f5bb67ef67eed43b85beeaf9fee1273c8ea9e2c3113e8a` |

The PDF was rebuilt from the listed source on 2026-09-09, checked for
unresolved citations and overfull text, rendered to five page images, and
visually inspected page by page. That is a local artifact check, not
independent peer review or release authorization.

## Frozen candidate outputs

| Artifact | SHA-256 |
|---|---|
| `Analysis/Casimir/CBR-001/cbr001_stage1.csv` | `57847f382bafa562827413f19f416dbc3da004c95996413d05e0cb7fde0bb47c` |
| `Analysis/Casimir/CBR-001/stage2_outputs/cbr001_stage2_scan.csv` | `fe648629545f40a29ca3bdc93a5978c59d85210d9157918eb191d45e2056a4d9` |
| `Analysis/Casimir/CBR-001/stage2_outputs/cbr001_stage2_stress.png` | `e8228c8ba26a3b4e3341153893aa3a88bc0edf1afbbe17c8dc2033fcddf992ba` |
| `Analysis/Casimir/CBR-001/stage2_outputs/cbr001_stage2_anisotropy.png` | `b609b780e2fbf386cd43b79f14f8cffb08fd137d7db978d859170ed9e6b131a4` |
| `Analysis/Casimir/CBR-001/stage3_outputs/cbr001_stage3_runs.csv` | `433c6fba6d70373949829ee4ec586bf0e31fba7833dfc1d225c14863022e0f19` |
| `Analysis/Casimir/CBR-001/stage3_outputs/cbr001_stage3_summary.json` | `f6b8a9e649334c2dac679c96c58f619d6b86b8def944512631646665747d320b` |
| `Analysis/Casimir/CBR-001/stage3_outputs/cbr001_stage3_shape.png` | `53ecd1ea196449b7af72408bea9a405e2c0aebb956b32be3f0473b2cb023aa4d` |
| `Analysis/Casimir/CBR-001/stage3_outputs/cbr001_stage3_shear.png` | `a25c5e9acd33e4ba4d67aede705850907673a5de1a731b9b36a53b522e08a88e` |
| `Analysis/Casimir/CBR-001/stage3_outputs/cbr001_stage3_hubble_ratio.png` | `d0d88e5efd49f1d1381ee84d3dd812f7281244876c70ab8b100a0507670b8a95` |
| `Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_runs.csv` | `c99c427d971c8689e4fa0d9f5e3f01a66d70253655e501f1eb2e665ec97e1ffe` |
| `Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_thresholds.csv` | `94b0ae4c6381ce3843952609d26ee9c73309a0b5275872c1ba97463702db37c4` |
| `Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_summary.json` | `9a5e80d2f713f01b02b7ea14c2460a344bcb2fcfdf814ea6696677d465c2ce3b` |
| `Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_ratio.png` | `1013ac954d1ed8dbf122c496cfbc889c2fd9dd306f77c43977ca50c88dd2b97f` |
| `Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_phase_space.png` | `207962eb7522be76c6bf1579b78238929a1947a48bd03647f5a06dadea79b9fa` |
| `Analysis/Casimir/CBR-001/stage3b_outputs/cbr001_stage3b_threshold_epsilon.png` | `8fab00f95d0a49651bcd19ec3c175edd8d23248507066fabbf98af2e204e5bd1` |

## Stage-3B headline counts

| Class | Count by initial shape |
|---|---:|
| `ATTRACTOR` | 0 |
| `QUASI_PLATEAU` | 0 |
| `TRANSIENT_CROSSING` | 5 |
| `NO_CROSSING` | 2 |
| `INVALID` | 1 |

The fresh candidate retains 463 recorded integrations and 377 valid runs.
These are bounded results of the declared instantaneous `a^-4` closure, not a
general dynamical-QFT no-go theorem.

## Exact chained reproduction

From the repository root:

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\Casimir\CBR-001\casimir_t3_lattice.py --csv Analysis\Casimir\CBR-001\cbr001_stage1.csv
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\Casimir\CBR-001\cbr001_stage2_standalone.py --output-dir Analysis\Casimir\CBR-001\stage2_outputs
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\Casimir\CBR-001\cbr001_stage3_backreaction.py --stage2-csv Analysis\Casimir\CBR-001\stage2_outputs\cbr001_stage2_scan.csv --output-dir Analysis\Casimir\CBR-001\stage3_outputs
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\Casimir\CBR-001\cbr001_stage3b_ratio_test.py --stage2-csv Analysis\Casimir\CBR-001\stage2_outputs\cbr001_stage2_scan.csv --output-dir Analysis\Casimir\CBR-001\stage3b_outputs
```

For a non-mutating two-run audit instead:

```powershell
C:\Users\brend\anaconda3\envs\itsm_env\python.exe Analysis\Casimir\CBR-001\p2_reproduction_a0_harness.py
```

## Superseded 2026-08-01 raw-byte anchors

The three old CSV digests reproduce when the current numerical payload is
written with Windows CRLF records. The checkout stores LF-normalized files, so
those raw hashes were newline-dependent rather than evidence of numerical
drift. The old JSON digest was also workstation-path-dependent. This explains
the former mismatch but does not make the old raw-byte freeze portable.
