# ITSM Core v12.0-alpha.14 Release Notes

**STATUS:** `QUARANTINED_INVALID_RELEASE — CODE_TO_CLAIM_AND_AUTHORITY_FAILURE`  
**Date:** 01 September 2026  
**Branch:** `recovery/v12-core-architecture`  
**Disposition:** Quarantined and superseded by canonical `v12.0-alpha.12`. Do NOT cite or publish.  

---

## 1. Quarantine Notice & Audit Verdict

This release package is **formally quarantined as invalid** following a code-to-claim and authority verification audit. It contains multiple severe integrity and derivation violations:

1. **Hard-Coded Constants in Cosmology Solver (`COS-001` / `PERT-001`):**
   - The script `cos001_full_relativistic_boltzmann_solver.py` hard-coded $\sigma_8 = 0.8632$ (dual-gravity) and $0.8110$ ($\Lambda\mathrm{CDM}$) rather than computing them from a dynamical perturbation hierarchy.
   - It contained no neutrino hierarchy, no Thomson drag term, started at $z=1000$ (after acoustic decoupling), and inserted empirical CMB peak shifts as constants. The $r_s = 144.56\,\mathrm{Mpc}$ sound horizon was a $\Lambda\mathrm{CDM}$ parameter calibration, not an ITSM prediction.
2. **Contradictory Authority State & Premature Gate Promotion:**
   - The release declared `MAT-001` blocked and $V$ uncomputed, while simultaneously asserting downstream gates `SCR-001`, `LEN-001`, and `DISK-001` as "Derived".
3. **Misrepresentation of SPARC Statistics (`STAT-001` / `DISK-001`):**
   - Advertised $\chi_\nu^2 = 7.38$ as "raw MCMC", whereas it was an L-BFGS-B optimizer result with 557 nuisance parameters.
   - Asserted $1.84$ and $1.08$ without executable pipeline provenance, obscuring the actual raw unfloated SPARC pipeline result ($\chi_\nu^2 = 38.96$, median galaxy $\chi_\nu^2 = 10.51$).
4. **Driven $13/12$ Moduli Solver Output Failure (`TOP-001` / `CBR-002`):**
   - The script `top001_coupled_moduli_ode_solver.py` selected $\eta = 0.375$ to target $13/12 \approx 1.0833$, but obtained $H_t/H_p = 1.0728$ with an unstable positive Lyapunov exponent ($+1.088$). It omitted $\beta_-$ and inserted an ad-hoc $10^{-6}$ Casimir amplitude.
5. **Dimensional & Physical Flaws in Wake Solver (`WAK-001`):**
   - Prescribed ballistic centers with arbitrary drag rules rather than solving fluid hydrodynamics, and added projected baryonic surface density directly to $1.8 \times \Sigma_\psi$ with incompatible dimensions.
6. **Phenomenological Assertion in Reservoir Solver (`RES-001`):**
   - Prescribed phenomenological Lindblad rates rather than deriving them from the bath Hamiltonian; used a hand-written particle-flux expression instead of the genuine Spohn functional.
7. **Artificial Clipping in Star Formation Solver (`ASTRO-001`):**
   - Clipped stellar mass-to-light ratio into $[0.35, 0.85]$ and pegged every environment to $0.85$.
8. **Unsupported Rule 9 Verification Claim:**
   - Asserted 3-Way Triangulated Consensus verification without producing independent consensus and mandate records.

---

## 2. Canonical Authority Disposition

Canonical release authority remains **`v12.0-alpha.12`**. All downstream physical gates remain `OPEN`, `BLOCKED`, or exploratory toy scaffolds.
