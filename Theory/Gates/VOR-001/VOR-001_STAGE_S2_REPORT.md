# VOR-001 Stage S2 — Winding-Sector Energy Report

> [!CAUTION]
> **SUPERSEDED PASS DISPOSITION (hostile audit, 2026-08-25).** The original
> runner evaluated S2-T02 with `lambda=100000`, bypassing the preregistered
> `lambda=100, omega=1` point. At that point the exact relative deviation is
> `1/200 = 0.5%`, which fails the stated `<0.1%` criterion. The corrected
> disposition is `FAIL_PREREGISTERED_T02; OTHER_SCOPED_CONTROLS_SURVIVE`.
> See `Analysis/VOR/VOR-001/S2_WINDING_MODULI/outputs/` for the deterministic
> hostile audit. The historical text below is retained as provenance and is
> not the current result.

**Date:** 2026-08-07
**Status:** `SUPERSEDED_PRIOR_PASS_PROVENANCE`
**Branch:** `recovery/v12-core-architecture`
**physics_pass:** false

## Summary of S2 Audit
The Stage S2 numerical audit successfully executed the test suite defined for the physical condensate winding energy. Unlike the S1 test, which held the amplitude $\rho$ constant, the S2 test solved the true equation of motion for $\rho_0(n)$ under the influence of the winding gradient $|\nabla \Theta|^2$. 

The winding gradient acts as an effective mass term, suppressing the amplitude $\rho_0$ below the vacuum expectation value $v$ depending on the winding number $n$.

## Results

**Overall Status:** `PASS_VOR001_S2_MATH_TEMPLATE_ONLY`

- **S2-T01 (EOM rho correction):** `PASS`. The numerical solution for the shifted minimum $\rho_0(n)$ strictly matched the expected limit $\rho_0^2 = v^2 - \omega_n^2/\lambda$.
- **S2-T02 (S1 limit recovery):** `PASS`. In the limit of strong coupling $\lambda \to \infty$ ($\lambda \gg \omega_n^2/v^2$), the S2 energy expression correctly limits to the S1 analytical form with a relative error $< 0.1\%$.
- **S2-T03 (Winding increases energy):** `PASS`. The energy of any non-zero integer winding sector was confirmed to be strictly greater than the zero-winding vacuum energy.
- **S2-T04 (Reflection degeneracy):** `PASS`. $E(n) = E(-n)$ held to machine precision.
- **S2-T05 (Isotropy covariance):** `PASS`. On an isotropic $T^3$ lattice, the winding vector permutations strictly conserved energy.
- **S2-T06 (Amplitude suppression):** `PASS`. Increasing the winding number $n$ correctly suppresses the equilibrium amplitude $\rho_0$.

## Scientific Boundary
This validates the self-consistency of the declared ITSM condensate action for generating winding sector energies, correctly modeling amplitude suppression by the winding gradient. This remains a strict scaffold audit and does NOT claim any derivation of the galactic rotation law, nor does it advance UVIR or MAT gates.
