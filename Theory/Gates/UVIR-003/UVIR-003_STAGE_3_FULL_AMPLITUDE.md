# Gate UVIR-003: Physical-Basis Propagators and Exchange Amplitude
## Stage 3: Full Physical $2 \to 2$ Amplitude

### 1. Introduction
To test the unitarity bound of the $Y^{3/2}$ effective force law, we must assemble the complete tree-level $2 \to 2$ scattering amplitude $\mathcal{M}(s,t,u)$ for the physical scalar fluctuations $\delta\pi$. This amplitude consists of two distinct contributions:
1. The exchange diagrams (mediated by the local adiabatic background propagator, derived in Stage 2).
2. The direct 4-point contact interaction (derived from the quartic expansion of the fractional kinetic term).

### 2. The Quartic Contact Interaction
The non-linear gradient term is $\mathcal{L}_{grad} = \frac{l^2}{3} |\nabla \pi|^3$. We expand this around the local adiabatic background $\nabla \pi = \vec{g}_0 + \nabla \delta\pi$.

Defining $\delta \vec{g} = \nabla \delta\pi$ and taking the strict Taylor expansion of $|\vec{g}_0 + \delta \vec{g}|^3 = (g_0^2 + 2 \vec{g}_0 \cdot \delta \vec{g} + \delta g^2)^{3/2}$, the 4th-order term $\mathcal{L}^{(4)}$ in the fluctuation $\delta \vec{g}$ is:

$$ \mathcal{L}^{(4)} = l^2 \frac{g_0^3}{3} \left[ \frac{3}{8} \frac{(\delta \vec{g} \cdot \delta \vec{g})^2}{g_0^4} - \frac{3}{4} \frac{(\vec{g}_0 \cdot \delta \vec{g})^2 (\delta \vec{g} \cdot \delta \vec{g})}{g_0^6} + \frac{3}{8} \frac{(\vec{g}_0 \cdot \delta \vec{g})^4}{g_0^8} \right] $$

Simplifying this using the unit vector $\hat{g}_0 = \vec{g}_0 / g_0$:

$$ \mathcal{L}^{(4)} = \frac{l^2}{8 g_0} \left[ (\delta g^2)^2 - 2 (\hat{g}_0 \cdot \delta \vec{g})^2 (\delta g^2) + (\hat{g}_0 \cdot \delta \vec{g})^4 \right] $$

**Crucial Topological Cancellation:** If the fluctuation gradient $\delta \vec{g}$ is strictly longitudinal to the background ($\delta \vec{g} \parallel \hat{g}_0$), then $\delta g^2 = (\hat{g}_0 \cdot \delta \vec{g})^2$. 
In this exact limit, the bracket evaluates to $1 - 2(1) + 1 = 0$. The direct quartic contact interaction identically vanishes for strictly longitudinal fluctuations! The non-linear self-interactions only survive when transverse fluctuations are present.

### 3. The Full Amplitude $\mathcal{M}(s,t,u)$
The total tree-level amplitude is the sum of the $s, t,$ and $u$ channel exchange diagrams (from the cubic vertex) plus the local contact interaction $\mathcal{M}_{contact}$ derived from $\mathcal{L}^{(4)}$.

Let the incoming momenta be $p_1, p_2$ and outgoing be $p_3, p_4$. 
$$ \mathcal{M}_{total} = \mathcal{M}_s + \mathcal{M}_t + \mathcal{M}_u + \mathcal{M}_{contact} $$

From Stage 2, the cubic vertex is $V_3 \propto \frac{l^2}{g_0} (\vec{k}_1 \cdot \hat{g}_0)(\vec{k}_2 \cdot \hat{g}_0)(\vec{k}_3 \cdot \hat{g}_0)$.
The resulting $t$-channel exchange amplitude is:
$$ \mathcal{M}_t = \frac{l^4}{g_0^2} \frac{ [(\vec{p}_1 \cdot \hat{g}_0)(\vec{p}_3 \cdot \hat{g}_0)(\vec{q} \cdot \hat{g}_0)] [(\vec{p}_2 \cdot \hat{g}_0)(\vec{p}_4 \cdot \hat{g}_0)(\vec{q} \cdot \hat{g}_0)] }{q^2 + m_{eff}^2} $$

The contact amplitude evaluated for these same momenta is:
$$ \mathcal{M}_{contact} \propto \frac{l^2}{g_0} \sum_{perms} \left[ (\vec{p}_i \cdot \vec{p}_j)(\vec{p}_k \cdot \vec{p}_l) - 2 (\hat{g}_0 \cdot \vec{p}_i)(\hat{g}_0 \cdot \vec{p}_j)(\vec{p}_k \cdot \vec{p}_l) + (\hat{g}_0 \cdot \vec{p}_i)(\hat{g}_0 \cdot \vec{p}_j)(\hat{g}_0 \cdot \vec{p}_k)(\hat{g}_0 \cdot \vec{p}_l) \right] $$

### 4. Conclusion of Stage 3
We have successfully derived the full structure of the tree-level $2 \to 2$ amplitude. The presence of the background gradient $g_0$ dynamically suppresses the vertices: the cubic vertex scales as $g_0^{-1}$ and the quartic as $g_0^{-1}$. 

In the high-energy limit (or vanishing background $g_0 \to 0$), these amplitudes strongly diverge, signaling the breakdown of the $Y^{3/2}$ EFT and identifying the strong-coupling scale. In Stage 4, we will project this amplitude onto the s-wave ($J=0$) state to apply the strict perturbative unitarity bound and compute this exact strong-coupling scale $\Lambda_{strong}$.
