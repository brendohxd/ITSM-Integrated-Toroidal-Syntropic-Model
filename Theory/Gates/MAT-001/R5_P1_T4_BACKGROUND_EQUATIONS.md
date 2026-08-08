# Gate MAT-001: R5-P1 Scale-Compensator Fork Task 4
## Background Equations and Constrained Scalar Reduction

### 1. Introduction
With the exact interpolating kinetic function $F(Y)$ defined and the physical degrees of freedom formally accounted for, we now derive the classical field equations for the background geometry and the physical scalar modulus $\pi$. This establishes the exact macroscopic dynamics governing the syntropic flow and galactic rotation curves.

### 2. The Einstein-Frame Action
The total action in the Einstein frame, incorporating the exact interpolating kinetic function $F(Y)$ derived in CBR-002, is:
$$ S = \int d^4x \sqrt{-g} \left[ \frac{R}{16\pi G} + \mathcal{L}_\pi \right] + S_m[\tilde{g}_{\mu\nu}, \Psi_m] $$
where the scalar Lagrangian $\mathcal{L}_\pi$ for purely spatial, static gradients ($Y = (\nabla \pi)^2$) is:
$$ \mathcal{L}_\pi = F(Y) = Y - \frac{4}{\ell^2} \sqrt{Y} + \frac{8}{\ell^4} \ln\left(1 + \frac{\ell^2}{2} \sqrt{Y}\right) $$
and matter couples to the Jordan frame metric $\tilde{g}_{\mu\nu} = e^{2\pi/f} g_{\mu\nu}$.

### 3. The Scalar Equation of Motion
Varying the action with respect to the scalar field $\pi$ yields the generalized Poisson equation. The variation of the matter action with respect to the conformal coupling generates a source term proportional to the trace of the matter stress-energy tensor $T$:
$$ \nabla_\mu \left( 2 F_Y \nabla^\mu \pi \right) = \frac{T}{f} $$

For a non-relativistic, static baryon mass distribution $\rho_b$, the trace is $T \approx -\rho_b$. For strictly spatial gradients ($\nabla^\mu = \nabla$), the equation of motion reduces to:
$$ \nabla \cdot ( F_Y \nabla \pi ) = \frac{\rho_b}{2f} $$

Substituting the exact derivative $F_Y = \frac{\frac{\ell^2}{2} |\nabla \pi|}{1 + \frac{\ell^2}{2} |\nabla \pi|}$, we obtain the fundamental background equation:
$$ \nabla \cdot \left( \frac{\frac{\ell^2}{2} |\nabla \pi|}{1 + \frac{\ell^2}{2} |\nabla \pi|} \nabla \pi \right) = \frac{\rho_b}{2f} $$

### 4. Asymptotic Limits of the Background Equation
This single, non-linear field equation dictates the gravitational response across all length scales.

**A. The Deep-MOND Limit ($|\nabla \pi| \to 0$):**
In galactic outskirts, the denominator approaches 1. The equation becomes:
$$ \nabla \cdot \left( \frac{\ell^2}{2} |\nabla \pi| \nabla \pi \right) = \frac{\rho_b}{2f} $$
Integrating this for a spherical source mass $M$ yields the Baryonic Tully-Fisher Relation ($v^4 \propto M$), where the force is dictated exactly by $a_5 = \sqrt{2GM a_0}/r$ (under the constraint $\ell^2 f^3 = \frac{1}{4\pi G a_0}$).

**B. The Solar System Limit ($|\nabla \pi| \to \infty$):**
In strong gradient regimes near stars, the term $\frac{\ell^2}{2} |\nabla \pi|$ dominates the denominator, and the fraction $F_Y \to 1$. The equation becomes a standard linear Poisson equation:
$$ \nabla^2 \pi = \frac{\rho_b}{2f} $$
Because we have forced the fundamental scalar coupling to be extremely weak ($\alpha = \frac{1}{4\pi G f^2} < 2.3 \times 10^{-5}$), the resulting scalar fifth force in this linear regime is too weak to violate the Cassini bound, keeping the Solar System indistinguishable from pure General Relativity.

### 5. Conclusion
The background field equation successfully interpolates between a weakly-coupled canonical scalar in the Solar System (passing ephemeris bounds) and a strongly-coupled fractional kinetic scalar in the galactic vacuum (producing exact MOND dynamics). The derivation of these background equations successfully concludes Task 4 of the MAT-001 Scale-Compensator Fork.
