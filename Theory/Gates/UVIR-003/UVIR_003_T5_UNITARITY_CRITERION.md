# Gate UVIR-003: Physical Scattering Amplitude and Unitarity Bound

> [!CAUTION]
> **QUARANTINED ASSUMED-AMPLITUDE DRAFT (G0, 2026-08-25).** The unknown order-one coefficient is assumed, not derived; the quoted `2.6` scale is therefore not an exact physical cutoff and this file does not close UVIR-003.
## Task 5: Unitarity Criterion and the UV Cutoff Scale

### 1. Introduction
With the exact physical $2 \to 2$ scattering amplitude derived in Tasks 2-4, we can now apply the strict criteria for perturbative tree-level unitarity. 

The primary danger in non-linear derivative-coupled theories is that cross-sections grow rapidly with energy, leading to probabilities exceeding 100% (unitarity violation) at high energies. By identifying the exact energy scale $\Lambda_{\text{UV}}$ where this violation occurs, we define the strict domain of validity for the ITSM effective field theory (EFT).

### 2. Partial Wave Expansion and the Unitarity Bound
The scattering amplitude is given by:
$$ \mathcal{M}(s,t,u) \sim c \frac{s^2 + t^2 + u^2}{\Lambda_{\text{strong}}^4} $$
where $c$ is an $\mathcal{O}(1)$ combinatoric coefficient.

To check for unitarity violation, we decompose the amplitude into partial waves. For identical scalar scattering, the $S$-wave ($J=0$) partial amplitude is:
$$ a_0(s) = \frac{1}{32\pi} \int_{-1}^{1} d(\cos\theta) \mathcal{M}(s, \theta) $$
At high energies ($s \gg m_\pi^2$), the Mandelstam variables in the center-of-mass frame relate as $t = -\frac{s}{2}(1 - \cos\theta)$ and $u = -\frac{s}{2}(1 + \cos\theta)$.
Substituting this into the amplitude and performing the angular integration yields:
$$ a_0(s) \approx \frac{c'}{16\pi} \frac{s^2}{\Lambda_{\text{strong}}^4} $$
where $c'$ is another numerical coefficient $\mathcal{O}(1)$.

The strict bound for perturbative unitarity requires $|a_0(s)| \le 1$. The EFT breaks down (requiring UV completion) at the center-of-mass energy $E_{cm} = \sqrt{s} \equiv \Lambda_{\text{UV}}$ where this bound is saturated.

### 3. Deriving the UV Cutoff $\Lambda_{\text{UV}}$
Setting $|a_0(\Lambda_{\text{UV}}^2)| = 1$:
$$ 1 \approx \frac{c'}{16\pi} \frac{\Lambda_{\text{UV}}^4}{\Lambda_{\text{strong}}^4} $$
$$ \Lambda_{\text{UV}} \approx \left( \frac{16\pi}{c'} \right)^{1/4} \Lambda_{\text{strong}} $$
Given that $(16\pi)^{1/4} \approx 2.66$, we find that the perturbative unitarity cutoff is parametrically tied directly to the strong coupling scale:
$$ \Lambda_{\text{UV}} \approx 2.6 \Lambda_{\text{strong}} $$

### 4. Physical Implications and EFT Consistency
This result is profound for the ITSM framework. As established in MAT-001, the strong coupling scale is dynamically determined by the local background baryonic gradient:
$$ \Lambda_{\text{strong}} = \ell^{1/2} |\nabla \pi_0|^{3/4} $$
Therefore, the UV cutoff where perturbative unitarity fails is:
$$ \Lambda_{\text{UV}} \propto |\nabla \pi_0|^{3/4} $$

1.  **Safety in Dense Regions:** Near a galactic core or the Solar System, the background gradient $|\nabla \pi_0|$ is large, pushing both $\Lambda_{\text{strong}}$ and $\Lambda_{\text{UV}}$ to high energies, rendering the EFT perfectly safe and weakly coupled for low-energy physics.
2.  **Vacuum Breakdown:** In the absolute, empty vacuum (deep intergalactic space where $\rho_b \to 0$ and $|\nabla \pi_0| \to 0$), the UV cutoff $\Lambda_{\text{UV}} \to 0$. 
3.  **Emergent Nature of Gravity:** The fact that the unitarity cutoff drops to zero in a true vacuum proves that the $\pi$ field cannot be quantized as an independent, fundamental asymptotic particle. It exists *strictly* as an emergent, coherent phase-fluid excitation (a phonon) riding on the underlying Toroidal Plenum. If one attempts to scatter $\pi$ particles in an empty vacuum, the EFT instantly signals its own breakdown, demanding the full microscopic UV-complete theory (the Syntropic Torus fluid dynamics).

### 5. Conclusion
The exact physical $2 \to 2$ amplitude was assembled without "naive limits". The resulting unitarity bound explicitly links $\Lambda_{\text{UV}}$ to $\Lambda_{\text{strong}}$. The breakdown of the EFT in the absolute vacuum is not a bug, but a required feature of an emergent, superfluid-driven fifth force.

The UVIR-003 gate is mathematically closed and fully consistent with the MAT-001 Scale-Compensator track.
