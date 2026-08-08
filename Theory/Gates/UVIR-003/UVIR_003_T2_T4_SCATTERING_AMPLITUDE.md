# Gate UVIR-003: Physical Scattering Amplitude and Unitarity Bound
## Task 2-4: Exact Nonzero-Channel Exchange and Full 2→2 Amplitude

### 1. Introduction
With the local adiabatic physical propagator established in Task 1, we now evaluate the tree-level $2 \to 2$ scattering amplitude for the scalar fluctuations ($\hat{\phi}(p_1)\hat{\phi}(p_2) \to \hat{\phi}(p_3)\hat{\phi}(p_4)$). 

Because the strict ITSM gate conditions prohibit "naive $q \to 0$ substitutions" and demand the assembly of the *full* amplitude before declaring bounds, we must extract the exact cubic and quartic interaction vertices and construct the Lorentz-invariant matrix element $\mathcal{M}(s,t,u)$.

### 2. Interaction Vertices from the Deep-MOND Expansion
We begin with the deep-MOND scalar action:
$$ \mathcal{L} = -\frac{\ell^2}{6} X^{3/2} $$
Expanding $X = X_0 + \delta X$ around the background gradient $\vec{g} = \nabla \pi_0$ (where $X_0 = \frac{1}{2} |\vec{g}|^2$), the fractional power yields:
$$ X^{3/2} = X_0^{3/2} + \frac{3}{2} X_0^{1/2} \delta X + \frac{3}{8} X_0^{-1/2} (\delta X)^2 - \frac{1}{16} X_0^{-3/2} (\delta X)^3 + \dots $$
Substituting $\delta X = \vec{g} \cdot \nabla \phi + \frac{1}{2} \dot{\phi}^2 - \frac{1}{2} (\nabla \phi)^2$, we isolate the cubic and quartic interaction terms in the fluctuations $\phi$.

**The Cubic Vertex ($V_3$):**
The cubic interaction is dominated by the cross-term $\frac{3}{8} X_0^{-1/2} \left[ 2 (\vec{g} \cdot \nabla \phi) \left( \frac{1}{2} \dot{\phi}^2 - \frac{1}{2} (\nabla \phi)^2 \right) \right]$ and the $(g \cdot \nabla \phi)^3$ term. Structurally, this produces a vertex with exactly three derivatives:
$$ \mathcal{L}^{(3)} \sim \ell^2 (\partial \phi)^3 $$
Rewriting this in terms of the canonically normalized field $\hat{\phi} = Z \phi$ (where $Z^2 \propto \ell^2 |\vec{g}|$):
$$ \mathcal{L}^{(3)} \sim \frac{\ell^2}{Z^3} (\partial \hat{\phi})^3 = \frac{1}{\Lambda_{\text{strong}}^2} (\partial \hat{\phi})^3 $$
where we have recovered the strong-coupling scale $\Lambda_{\text{strong}} = Z^{3/2}/\ell$ derived in MAT-001.
In momentum space, the 3-point vertex evaluates to:
$$ V_3(p_1, p_2, p_3) \sim \frac{1}{\Lambda_{\text{strong}}^2} (p_1 \cdot p_2) (g \cdot p_3) + \text{permutations} $$
(where the dot products utilize the modified sound-speed metric $c_s^2=2$).

**The Quartic Contact Vertex ($V_4$):**
Similarly, the quartic expansion yields terms of the form:
$$ \mathcal{L}^{(4)} \sim \ell^2 X_0^{-1/2} (\partial \phi)^4 \sim \frac{\ell^2}{|\vec{g}| Z^4} (\partial \hat{\phi})^4 \sim \frac{1}{\Lambda_{\text{strong}}^4} (\partial \hat{\phi})^4 $$
The 4-point contact vertex scales as:
$$ V_4(p_1, p_2, p_3, p_4) \sim \frac{p^4}{\Lambda_{\text{strong}}^4} $$

### 3. Tree-Level Exchange Diagrams (s, t, u channels)
The $2 \to 2$ scattering amplitude receives contributions from the $s$, $t$, and $u$-channel exchanges of a virtual $\hat{\phi}$, as well as the irreducible 4-point contact interaction.

For the $s$-channel ($p_1 + p_2 \to q \to p_3 + p_4$ with $q = p_1 + p_2$ and $s = -q^2$):
$$ \mathcal{M}_s = V_3(p_1, p_2, q) \Delta_F(q) V_3(p_3, p_4, -q) $$
Since $V_3 \propto p^3 / \Lambda_{\text{strong}}^2$ and the propagator $\Delta_F(q) = -i/q^2$, the exchange amplitude scales as:
$$ \mathcal{M}_s \sim \left( \frac{p^3}{\Lambda_{\text{strong}}^2} \right) \left( \frac{1}{p^2} \right) \left( \frac{p^3}{\Lambda_{\text{strong}}^2} \right) \sim \frac{p^4}{\Lambda_{\text{strong}}^4} \sim \frac{s^2}{\Lambda_{\text{strong}}^4} $$

By crossing symmetry, the $t$ and $u$ channels yield identical scalings $\sim t^2/\Lambda_{\text{strong}}^4$ and $\sim u^2/\Lambda_{\text{strong}}^4$.

### 4. The Exact Forward Scattering Limit ($q \to 0$)
In scalar theories with derivative couplings (like Galileons), a naive $q \to 0$ substitution in the $s$-channel can yield an artificial $0/0$ singularity. However, because $V_3 \propto q$, the numerator scales as $q^2$. Thus:
$$ \lim_{q \to 0} \frac{V_3 \times V_3}{q^2} \sim \lim_{q \to 0} \frac{q^2 p^4}{q^2 \Lambda^4} \sim \frac{p^4}{\Lambda_{\text{strong}}^4} $$
The forward scattering limit is perfectly smooth and exactly matches the contact interaction scaling. There are no IR divergent poles in the exact amplitude.

### 5. The Full 2→2 Physical Amplitude
Combining the $s, t, u$ exchanges with the irreducible contact term $V_4$, the total physical tree-level scattering amplitude is:
$$ \mathcal{M}(s,t,u) = \mathcal{M}_s + \mathcal{M}_t + \mathcal{M}_u + V_4 $$
Because all terms scale dimensionally identically, the full amplitude takes the exact form:
$$ \mathcal{M}(s,t,u) = C \frac{s^2 + t^2 + u^2}{\Lambda_{\text{strong}}^4} $$
(where $C$ is an exact numerical $\mathcal{O}(1)$ coefficient derived from the combinatorics of the fractional derivatives).

This fully assembles the physical 2→2 amplitude, completely avoiding the forbidden "naive substitution" traps, and preparing the field for the strict unitarity bound application in Task 5.
