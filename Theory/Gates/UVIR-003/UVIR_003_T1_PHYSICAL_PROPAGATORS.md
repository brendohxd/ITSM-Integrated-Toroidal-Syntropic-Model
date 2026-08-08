# Gate UVIR-003: Physical Scattering Amplitude and Unitarity Bound
## Task 1: Local Adiabatic Quadratic Propagators in Physical Basis

### 1. Introduction
To evaluate the tree-level $2 \to 2$ scattering amplitude of the physical scalar modulus $\pi$, we must first define its propagator. 

Because the ITSM scale-compensator model is highly non-linear in the deep-MOND regime (where the kinetic term scales as $Y^{3/2}$), the theory admits no free asymptotic states in an absolute vacuum. Instead, fluctuations only propagate coherently over a local, non-zero background gradient $\nabla \pi_0$. 
This requires us to calculate the **local adiabatic quadratic propagator**.

### 2. The Local Adiabatic Background
We expand the physical scalar field around a classical, locally static background gradient:
$$ \pi(x,t) = \pi_0(x) + \phi(x,t) $$
We assume the background gradient $\vec{g} = \nabla \pi_0$ is varying sufficiently slowly over the distance scales relevant to the scattering process, allowing us to treat it as a constant vector $\vec{g}$ (the adiabatic approximation).

The physical ghost-free action in the deep-MOND regime ($|\vec{g}| \to 0$) is dominated by the fractional kinetic term:
$$ \mathcal{L}_{\text{MOND}} = - \frac{\ell^2}{6} \left( -\frac{1}{2} \partial_\mu \pi \partial^\mu \pi \right)^{3/2} $$
Note: For clarity of the metric signature $(- + + +)$ and proper relativistic treatment of fluctuations, we define $X = -\frac{1}{2} \partial_\mu \pi \partial^\mu \pi$. The background satisfies $X_0 = \frac{1}{2} |\vec{g}|^2$.

### 3. Quadratic Action for Fluctuations
Expanding $\mathcal{L}_{\text{MOND}}$ to quadratic order in the fluctuations $\phi$, we generate the effective kinetic matrix:
$$ \mathcal{L}^{(2)}_{\phi} = \frac{1}{2} K^{\mu\nu} \partial_\mu \phi \partial_\nu \phi $$
Because the background gradient $\vec{g}$ breaks local Lorentz invariance (it defines a preferred spatial direction), the kinetic matrix $K^{\mu\nu}$ is non-trivial. 
As proven in CBR-002, the longitudinal speed of sound in the deep-MOND limit is strictly $c_s^2 = 2$. The temporal and spatial gradients decouple as:
$$ \mathcal{L}^{(2)}_{\phi} = \frac{Z^2}{2} \left( \dot{\phi}^2 - c_s^2 (\nabla \phi)^2 \right) $$
where the wave-function renormalization factor $Z^2$, derived in MAT-001 Task 6, is strictly proportional to the background gradient:
$$ Z^2 \propto \ell^2 |\vec{g}| $$

### 4. Canonical Normalization and the Physical Propagator
To evaluate scattering amplitudes, we must canonically normalize the field:
$$ \hat{\phi} = Z \phi $$
In terms of the canonical field $\hat{\phi}$, the free quadratic Lagrangian is standard:
$$ \mathcal{L}^{(2)}_{\hat{\phi}} = \frac{1}{2} \dot{\hat{\phi}}^2 - \frac{c_s^2}{2} (\nabla \hat{\phi})^2 $$

Applying the standard canonical quantization rules, we invert the quadratic operator to find the momentum-space Feynman propagator. For a four-momentum $p^\mu = (\omega, \vec{k})$, the local adiabatic propagator is:
$$ \Delta_F(\omega, \vec{k}) = \frac{-i}{-\omega^2 + c_s^2 |\vec{k}|^2 - i\epsilon} $$
where $c_s^2 = 2$.

### 5. Implications for Scattering
*   **No Absolute Vacuum States:** The presence of $Z \propto |\vec{g}|^{1/2}$ in the canonical normalization means that as the background gradient vanishes ($|\vec{g}| \to 0$), the original field fluctuations $\phi = \hat{\phi}/Z$ diverge. The propagator is only physically well-defined on top of the Toroidal Plenum's acoustic wake.
*   **Modified Dispersion:** The $c_s^2 = 2$ dispersion relation means the internal exchange momentum $p^2$ in Feynman diagrams must be evaluated using the modified metric $G^{\mu\nu} = \text{diag}(-1, c_s^2, c_s^2, c_s^2)$. 

This fully specifies the physical, canonically normalized quadratic propagator required to compute the internal lines of the $2 \to 2$ exchange diagrams in Task 2.
