# Project: ITSM CLASS Integration

## Architecture
- CLASS (C codebase) integrated with the Integrated Toroidal-Syntropic Model (ITSM) expansion history equations.
- Expose the C core functionality through the Python wrapper `classy`.
- Automated test script `verify_background.py` to compare CLASS outputs against theoretical model equations.
- Plotting script `plot_spectra.py` to visualize CMB ($C_l$) and Matter Power ($P(k)$) spectra.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| 1 | Setup & Clone | Clone CLASS, investigate background.c and build tools | none | DONE (ID: f839fe29-c1d3-449d-8825-5b4890ee9399) |
| 2 | Core C Modification | Implement ITSM expansion history in background C code | M1 | IN_PROGRESS (ID: e3668c7e-f892-4bb6-bbab-a33baa1655d9) |
| 3 | Compile & Wrap | Compile CLASS C code and build/install classy wrapper | M2 | IN_PROGRESS (ID: e3668c7e-f892-4bb6-bbab-a33baa1655d9) |
| 4 | Verification Script | Develop verify_background.py to assert H(z) matches ITSM | M3 | PLANNED |
| 5 | Spectra Plotting | Develop plot_spectra.py to plot CMB and P(k) | M4 | PLANNED |
| 6 | E2E & Hardening | Final verification, reviews, and adversarial tests | M5 | PLANNED |

## Interface Contracts
### CLASS Core C ↔ classy Python Wrapper
- Standard CLASS parameters (`H0`, `Omega_b`, `Omega_cdm`, etc.) passed via `classy.Class()` dict.
- ITSM background Hubble parameter $H(z) = H_0 \sqrt{\Omega_m (1+z)^3 + (1 - \Omega_m)(1+z)^{-n}}$ implemented in `background.c` where $\Omega_m = \Omega_b + \Omega_{cdm}$ (or custom mapping).
- `classy.Hubble(z)` or `background_h` matches the ITSM equation within $10^{-5}$ relative tolerance.
