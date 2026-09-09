# Gate UVIR-003: Physical-Basis Propagators and Exchange Amplitude
## Stage 4: Unitarity Bounds and Transverse Channel Breakdown (QUARANTINED LEGACY DRAFT)

> [!CAUTION]
> This file is superseded provenance, not a current gate decision. It assumes
> an interpolating function and coupling that were not derived from the parent
> action, and its cutoff does not close the current constrained amplitude.
> Current authority is `UVIR-003 IN_PROGRESS`, `MAT-001 BLOCKED`; use the Stage
> 5 parent decision and `active_research.md`.

### 1. Introduction
This legacy draft assumes the Stage 5 expression
$\Lambda_{strong}=Z^{9/8}/\ell$ and applies a perturbative unitarity bound in
the surviving transverse channel. The current parent-gate decision does not
accept that assumption as an exact ITSM cutoff.

### 2. The Transverse Channel Cutoff
The interaction energy scales are strictly determined by the dimensionless kinetic normalization factor $Z = \ell^2 g_0$. The cutoff for the cubic transverse interactions was derived as:
$$ \Lambda_{strong} = \frac{Z^{9/8}}{\ell} = \frac{(\ell^2 g_0)^{9/8}}{\ell} = \ell^{5/4} g_0^{9/8} $$

This scaling reveals a profound feature of the theory: **The strong-coupling scale is entirely dependent on the local background gravitational gradient $g_0$.** 

### 3. Solar System Weak Coupling
By executing Task R-1, we pivoted to an exact interpolating function that transitions to a canonical kinetic term ($K_Q \to 1$) in the high-gradient regimes (like the Solar System).
In this limit:
- The fundamental scalar coupling is set extremely weak ($\alpha < 2.3 \times 10^{-5}$).
- The theory becomes strictly luminal ($c_L = c$).
- Because the non-linear fractional terms shut off, the strong coupling cutoff $\Lambda \to M_{Pl}$.
The theory is perfectly unitary and weakly coupled near massive bodies.

### 4. Deep-MOND Unitarity Breakdown
In the deep-MOND galactic outskirts, the gradient $g_0$ becomes extremely small. The exact interpolating function recovers the $Y^{3/2}$ fractional kinetic limit. 
As $g_0 \to 0$ (the absolute vacuum):
$$ Z \to 0 \implies \Lambda_{strong} \to 0 $$

The cutoff of the theory crashes to zero. The transverse channel becomes infinitely strongly coupled. Tree-level scattering amplitudes rapidly violate the perturbative unitarity bound $|a_0(s)| \le 1$. 
This means that **tree-level results for the scalar fluctuations are not trustworthy in the deep-MOND vacuum.**

### 5. Conclusion: A Known Affliction
The failure of perturbative unitarity in the $g_0 \to 0$ transverse channel is not a fatal mathematical error; it is a **known, structural affliction of all MOND-like effective field theories (AQUAL, k-essence, TeVeS).** 

Because the fractional kinetic operator $Y^{3/2}$ is required to structurally reproduce the Baryonic Tully-Fisher Relation ($v^4 \propto M$), the resulting vanishing cutoff $\Lambda \to 0$ in vacuum is an unavoidable theoretical trade-off. 
The interpolating function successfully cures the Solar System causality and bounds, but the theory remains strongly coupled in the deep vacuum. Any quantum processes or high-energy scattering in the galactic outskirts must rely on a yet-unknown UV completion.

### Historical gate-status assertion (superseded)

This draft recorded `UVIR-003: CLOSED (PROVISIONAL)`. That promotion is
quarantined. Current status is `UVIR-003 IN_PROGRESS`; the complete constrained
amplitude, matched invariant and physical cutoff remain open.
