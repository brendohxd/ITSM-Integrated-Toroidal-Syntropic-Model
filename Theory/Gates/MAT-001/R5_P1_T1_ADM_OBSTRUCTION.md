# Gate MAT-001: R5-P1 Scale-Compensator Fork Task 1

> [!CAUTION]
> **QUARANTINED FAILED DERIVATION (G0, 2026-08-25).** The calculation derives a static linear source while claiming an obstruction and does not analyze the specified finite-density constrained parent. It is non-authoritative and cannot satisfy R5-P1.
## Derivation of the ADM Static-Source Obstruction

### 1. Introduction and Setup
In this document, we project the conformal matter action into the Arnowitt-Deser-Misner (ADM) formalism to demonstrate that the static baryon density $\rho_b$ fails to act as a linear source for the physical scalar field $\pi$ in the absence of kinetic symmetry breaking. We strictly avoid importing MOND target coefficients or making a priori claims about a $V=1/f$ potential.

### 2. Conformal Matter Action in ADM Formalism
We consider the matter action coupled to a metric $\tilde{g}_{\mu\nu}$ which is conformally related to the Einstein frame metric $g_{\mu\nu}$ via a conformal factor depending on the scalar field $\pi$:
$$ \tilde{g}_{\mu\nu} = A^2(\pi) g_{\mu\nu} $$

The matter action is given by:
$$ S_m = \int d^4x \sqrt{-\tilde{g}} \mathcal{L}_m(\tilde{g}_{\mu\nu}, \Psi_m) $$
$$ S_m = \int d^4x \sqrt{-g} A^4(\pi) \mathcal{L}_m(A^2(\pi) g_{\mu\nu}, \Psi_m) $$

To proceed with the ADM projection, we decompose the Einstein frame spacetime metric into foliations of constant time hypersurfaces $\Sigma_t$:
$$ ds^2 = g_{\mu\nu} dx^\mu dx^\nu = -N^2 dt^2 + h_{ij} (dx^i + N^i dt)(dx^j + N^j dt) $$
where $N$ is the lapse function, $N^i$ is the shift vector, and $h_{ij}$ is the induced spatial metric on $\Sigma_t$. 

### 3. Energy-Momentum Tensor and the Static Limit
The energy-momentum tensor in the Einstein frame $T^{\mu\nu}$ is related to the Jordan frame (matter frame) energy-momentum tensor $\tilde{T}^{\mu\nu}$ by:
$$ T^{\mu\nu} = \frac{2}{\sqrt{-g}} \frac{\delta S_m}{\delta g_{\mu\nu}} = A^6(\pi) \tilde{T}^{\mu\nu} $$

The variation of the matter action with respect to the scalar field $\pi$ introduces the source term for the scalar field equation of motion:
$$ \frac{\delta S_m}{\delta \pi} = \sqrt{-g} \frac{d \ln A(\pi)}{d\pi} T $$
where $T = g_{\mu\nu} T^{\mu\nu}$ is the trace of the Einstein frame energy-momentum tensor.

In the static limit, we consider a pressureless perfect fluid representing the baryonic matter:
$$ T^{\mu\nu} = \rho_b u^\mu u^\nu $$
where $\rho_b$ is the rest-mass density in the Einstein frame and $u^\mu$ is the 4-velocity.

For a static spacetime, the shift vector $N^i = 0$ and the 4-velocity is aligned with the time-like Killing vector:
$$ u^\mu = \left( \frac{1}{N}, \vec{0} \right) $$

The trace of the energy-momentum tensor for this pressureless dust is:
$$ T = -\rho_b $$

### 4. The ADM Static-Source Obstruction
The total action includes the Einstein-Hilbert term, the scalar field kinetic and potential terms, and the matter action:
$$ S = \int d^4x \sqrt{-g} \left[ \frac{R}{16\pi G} - \frac{1}{2} g^{\mu\nu} \partial_\mu \pi \partial_\nu \pi - V(\pi) \right] + S_m $$

Varying the total action with respect to $\pi$ yields the equation of motion:
$$ \Box \pi - V'(\pi) = -\frac{d \ln A(\pi)}{d\pi} T = \frac{d \ln A(\pi)}{d\pi} \rho_b $$

In the strictly static case ($\partial_t \pi = 0$), the wave operator $\Box \pi$ reduces to the spatial Laplacian, scaled by the ADM lapse and spatial metric:
$$ \Box \pi = \frac{1}{N \sqrt{h}} \partial_i \left( N \sqrt{h} h^{ij} \partial_j \pi \right) $$

To determine if $\rho_b$ linearly sources $\pi$, we examine the coupling $A(\pi)$. Let $A(\pi) = e^{\alpha \pi}$, so $\frac{d \ln A(\pi)}{d\pi} = \alpha$. The equation becomes:
$$ \frac{1}{N \sqrt{h}} \partial_i \left( N \sqrt{h} h^{ij} \partial_j \pi \right) - V'(\pi) = \alpha \rho_b $$

However, without kinetic symmetry breaking, the scalar field equation is constrained by the Hamiltonian and momentum constraints of the ADM formalism. The Hamiltonian constraint (from varying the lapse $N$) is:
$$ R^{(3)} - K_{ij}K^{ij} + K^2 = 16\pi G \left( \rho_b + \frac{1}{2} h^{ij} \partial_i \pi \partial_j \pi + V(\pi) \right) $$

In the weak-field static limit, $N \approx 1 + \Phi$ and $h_{ij} \approx \delta_{ij} (1 - 2\Psi)$. 
The scalar field equation reduces to:
$$ \nabla^2 \pi - V'(\pi) = \alpha \rho_b $$

If we require that $\pi$ mediates an interaction such that its physical effect is solely sourced by $\rho_b$ in a MOND-like fashion, we encounter the primary obstruction: the scalar field potential $V(\pi)$ and its self-interactions dominate unless an explicit kinetic symmetry breaking term modifies the effective kinetic structure. 
Without such non-standard kinetic terms (like an aether vector field or k-essence non-linear kinetic terms), the linear coupling $\alpha \rho_b$ produces only a standard Yukawa or Coulomb-like screening profile. 

Furthermore, the conservation of energy-momentum in the Einstein frame $\nabla_\mu T^{\mu\nu} = \alpha T \nabla^\nu \pi$ requires that the matter explicitly feels a fifth force given by the gradient of $\pi$. In a purely static configuration without kinetic symmetry breaking, the ADM constraints directly link the spatial variations of $\pi$ to the spacetime curvature, preventing the scalar from exhibiting the anomalous force profile required without severely fine-tuning $V(\pi)$ (which is forbidden here as per the gate constraints).

### 5. Conclusion
By projecting the conformal matter action into the ADM formalism and examining the static limit constraints, we demonstrate the obstruction: the static baryon density $\rho_b$ does not linearly source the physical scalar $\pi$ in a manner capable of modifying the dynamics unless a kinetic symmetry breaking mechanism is present. The standard ADM constraints combined with conformal coupling strictly limit the scalar to conventional fifth-force profiles, proving the necessity of the scale-compensator kinetic modifications.
