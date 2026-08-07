# UVIR-003: STAGE 1 - LOCAL ADIABATIC QUADRATIC PROPAGATORS

## 1. Objective
Derive the local adiabatic quadratic propagators in the physical basis (for the physical mode $\pi$ and transverse tensor modes $h_{ij}$) to evaluate the exchange amplitude. This explicitly sets up the $2 \to 2$ exchange amplitude while avoiding naive $q \to 0$ substitutions or Taylor-expanded kernels for the exact $|\nabla \pi|^3$ operator.

## 2. The Local Adiabatic Background
We consider perturbations around a local background $\bar{\pi}$. To avoid infrared divergences and unphysical $q \to 0$ extrapolations, we treat the background exactly in a local patch, defining the metric perturbation and scalar fluctuation $\pi = \bar{\pi} + \delta \pi$.

The effective action at quadratic order in fluctuations involves the kinetic terms for the physical scalar mode $\pi$ (Galileon/EFT of inflation scalar) and the transverse-traceless tensor modes $h_{ij}$. 

The background induces an effective metric for the scalar perturbations.
$$ G^{\mu\nu} = \eta^{\mu\nu} + \frac{c}{\Lambda^3} \partial^\mu \partial^\nu \bar{\pi} $$
where $c$ is the coupling constant and $\Lambda$ is the strong coupling scale.

## 3. Quadratic Action and Propagator Matrix
For the scalar fluctuation $\delta\pi$ and the tensor $h_{ij}$, the quadratic action takes the form:
$$ S^{(2)} = \int d^4x \sqrt{-g} \left[ \frac{1}{2} Z^{\mu\nu} \partial_\mu \delta\pi \partial_\nu \delta\pi + \frac{M_{Pl}^2}{8} \left( \eta^{\mu\rho} \eta^{\nu\sigma} - \frac{1}{2} \eta^{\mu\nu} \eta^{\rho\sigma} \right) \partial_\alpha h_{\mu\nu} \partial^\alpha h_{\rho\sigma} + \mathcal{L}_{mix} \right] $$

In the decoupling limit and working in the strictly physical basis where we avoid gauge redundancies, we diagonalize the $\delta\pi$ - $h_{ij}$ kinetic mixing.

### 3.1 Scalar Propagator
The scalar propagator in momentum space, in the background $Z^{\mu\nu}$, is the inverse of the kinetic operator:
$$ \Delta_{\pi}(k) = \frac{-i}{Z^{\mu\nu} k_\mu k_\nu - i\epsilon} $$
To maintain the exact structure for the $|\nabla\pi|^3$ operators without Taylor expanding the kernel, $Z^{\mu\nu}$ is kept as an exact function of the local background derivatives $\partial\partial\bar{\pi}$, capturing the Vainshtein screening effects inherently:
$$ Z^{\mu\nu}(\bar{\pi}) = \eta^{\mu\nu} - \frac{c}{\Lambda^3} (\eta^{\mu\alpha} \eta^{\nu\beta} - \eta^{\mu\nu} \eta^{\alpha\beta}) \partial_\alpha \partial_\beta \bar{\pi} $$

### 3.2 Tensor Propagator
For the tensor modes, the propagator is standard but evaluated on the flat background (or the effective acoustic geometry if generalized):
$$ \Delta_{h}^{\mu\nu\rho\sigma}(k) = \frac{-i}{k^2 - i\epsilon} \Pi^{\mu\nu\rho\sigma} $$
where the polarization tensor $\Pi^{\mu\nu\rho\sigma}$ is the transverse-traceless projector:
$$ \Pi^{\mu\nu\rho\sigma} = \frac{1}{2} (P^{\mu\rho} P^{\nu\sigma} + P^{\mu\sigma} P^{\nu\rho} - P^{\mu\nu} P^{\rho\sigma}) $$
with $P^{\mu\nu} = \eta^{\mu\nu} - \frac{k^\mu k^\nu}{k^2}$.

## 4. Setting up the $2 \to 2$ Exchange Amplitude
With the uncoupled propagators derived, the $2 \to 2$ exchange amplitude $\mathcal{M}(s,t,u)$ is constructed by contracting the exact interaction vertices with $\Delta_{\pi}(k)$ and $\Delta_{h}(k)$. By keeping $Z^{\mu\nu}$ unexpanded, we ensure unitarity bounds can be checked robustly against the physical modes rather than pathological gauge artifacts, successfully setting the stage for evaluating the positivity bounds.
