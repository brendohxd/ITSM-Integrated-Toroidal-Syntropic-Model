# ITSM Changelog & Archive History

## Version 9.1.0 — Hierarchical $H_0$ Methodology & Manuscript Correction (2026-05-23)

### Methodological Investigation
- **Hierarchical Bayesian H0 Analysis:** Executed a full investigation into population-level $H_0$ inference from the 176-galaxy SPARC MCMC chain library using three distinct estimator implementations:
  - `itsm_hierarchical_h0.py` — Full raw-sample likelihood (5-hour run, $\mu_{H_0} = 69.089 \pm 0.005$ km/s/Mpc). Archived; identified as statistically overcounted (treats 7.3M MCMC samples as independent observations, inflating statistical weight by ~41,600×).
  - `itsm_hierarchical_h0_fast.py` — Gaussian-convolution approximation (~3 seconds, $\mu_{H_0} = 65.26 \pm 0.62$ km/s/Mpc). Archived; invalidated by non-Gaussianity of per-galaxy posteriors.
  - `itsm_hierarchical_h0_correct.py` — IS-corrected logsumexp marginal estimator per Mandel, Farr & Gair (2019) MNRAS 486, 1086 (~2.5-hour run). Posterior pinned to prior boundary ($\mu_{H_0} = 55.1$ km/s/Mpc), confirming that individual SPARC galaxies do not sufficiently constrain $H_0$ for population inference.
- **Shape Diagnostic:** `itsm_h0_shape_diagnostic.py` revealed per-galaxy $H_0$ posterior standard deviations average $12.40$ km/s/Mpc (versus $14.4$ km/s/Mpc for a completely flat uniform distribution). 89.8% of galaxies have $\sigma_{H_0} > 5$ km/s/Mpc — confirming posteriors are near-flat and individually uninformative for hierarchical $H_0$ extraction. This finding is reserved for future work with independent distance priors.

### Repository Structure
- **New `Analysis/` directory:** Added `Analysis/Hierarchical_H0/` as a structured methodology development area, separate from primary manuscript scripts. Contains all four scripts above plus a full `Archive/` of three MCMC result sets with summary statistics and diagnostic plots.
- **Archive hygiene:** All superseded result directories (`results_full_rawsample_5hr/`, `results_fast_gaussian/`, `results_is_corrected/`) moved to `Analysis/Hierarchical_H0/Archive/` with descriptive naming. No results deleted.

### Manuscript Correction (`Manuscript/Main.tex`)
- **H0 paragraph reframed (line 439):** Replaced overclaiming language ("independently derives the exact value of the local Cosmic Distance Ladder") with peer-review defensible framing. The reported $H_0 = 72.49 \pm 0.31$ km/s/Mpc is now correctly described as a median-of-posteriors statistic, with explicit acknowledgement of the $a_0$–baryonic normalisation degeneracy at the single-galaxy level. Hierarchical population inference is explicitly reserved for future work. Value and figure unchanged.
- **Recompiled:** `Main.pdf` recompiled clean, 24 pages, zero errors.

### Git Provenance
- Commit `e20165e` — selective add (README, Main.tex, Main.pdf, Analysis/). Remaining modified scripts from prior sessions left unstaged to preserve atomic commit discipline.
- Full directory backup created at `ITSM_BACKUP_20260523_1326` prior to any changes.

---

## Current Version (v9.0.1 / Final Peer-Review Submission Release)
- **Citation Logic:** Resolved hardcoded bibliography citation chains ([?] placeholders) by normalizing the pdflatex compilation sequence and manual `\bibitem` integration.
- **Asset Sanitization:** Standardized all plot titles (specifically `itsm_n_evolution.png` and `itsm_desi_bao_empirical_validation.png`) to native Matplotlib `fontweight='bold'` to excise raw LaTeX markup artifacts.
- **Build Verification:** Verified 24-page `Main.pdf` structural stability; successfully cleared all floating environment float warnings.
- **Final Validation:** Confirmed manuscript structural integrity and bibliographical resolution for formal external distribution.

## Version 9.0 (Release Candidate 1)
- **Superfluid Microphysics:** Formalized the ultra-light scalar field and non-thermal BEC topology.
- **Manuscript Architecture Refactor:** Reorganized the entire manuscript into a finalized four-section architecture to improve logical flow from foundational theory to empirical validation. This included resolving minor LaTeX compilation errors that arose from the new structure.
- **Hydrodynamic Derivation:** Replaced the 2/3 geometric analogy with explicit Onsager-Feynman and Gross-Pitaevskii vortex mechanics.
- **PPN Compliance:** Derived Parameterized Post-Newtonian (PPN) metric expansions to explicitly satisfy Cassini constraints.
- **CMB Acoustic Protection:** Added Thermodynamic Decoupling function $\Xi(z)$ to mathematical proof and visualizations.
- **Vacuum Quenching Falsifiability:** Established extreme-energy falsifiability metrics for AGN and the Bullet Cluster.
- **4D Thermodynamic Decoupling:** Excised the 5D embedding manifold in favor of strict 4D conformal decoupling ($\Theta = 3H$) for the Syntropic Source Vector.
- **Predictive Shield Matrix:** Added comprehensive matrices explicitly contrasting ITSM's predictive capacity and zero-free-parameter ontology against MOND and $\Lambda$CDM.
- **Topological Clarifications:** Added explicit physical intuition for the macroscopic "Stirrer" and the $2/3$ dimensional projection factor via the demagnetization tensor analogy.
- **Journal Layout Polish:** Reverted to a clean single-column `revtex4-2` layout with manual `\parbox` table formatting to ensure optimal readability and margin compliance.
- **Academic Standardization:** Scrubbed all non-academic terminology (e.g., ATS references) from scripts and documentation, and replaced legacy `eqnarray` with modern `align` environments.
- **Computational Suite Expansion:** Standardized 11 fully integrated Python simulation engines, routing all generative assets to centralized structural hubs.

## Version 8.3
- **Mathematical Unification:** Standardized the $g_{eff}$ formula utilizing the canonical Plenum Shear Ansatz across all simulations.
- **Evidence Upgrade:** Removed hypothetical NGC 1560 data in favor of a robust 175-galaxy global SPARC database validation.
- **Syntropic Expansion:** Added explicit validation against DESI 2024 BAO measurements demonstrating organic $(1+z)^{-3}$ volumetric decay.
- **NANOGrav Refinement:** Upgraded stochastic background resonance profile from Gaussian to mathematically rigorous Lorentzian.
- **Publication Scripts:** Finalized 8 distinct Python validation scripts, formatted for journal-quality `matplotlib` LaTeX rendering.
- **Literature Integration:** Incorporated formal citations for JWST high-redshift data (Labbé et al.), DESI 2024, and SPARC.

## Version 8.2 (Iterative Refinement)
- Replaced empirical mockups with generative programmatic data tests.
- Formatted `Main.tex` for high-impact standard journals (APS/PRD style).
- Introduced the JADES-GS-z14-0 scaffold contrast model.

## Version 7.7
- Expanded the $a_0$ topological derivation.
- Introduced foundational Python scripts for acoustic wake visualization and drag saturation.
- Consolidated disparate LaTeX drafts into a unified manuscript.

## Version 5.x - 7.x
- Initial conception of the Syntropic Source Vector ($Q^\nu$).
- Derivation of the macroscopic yield threshold ($a_0$).
- Drafted the Toroidal phase space boundary limits.

## Version 3.x
- Foundational hypothesis: Challenging the necessity of non-baryonic dark matter through Superfluid Plenum dynamics.