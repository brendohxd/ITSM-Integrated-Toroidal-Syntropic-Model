# Gate CBR-002: Causality and Solar System Bounds
## Diagnostic limits of the standalone cubic operator

### 1. Introduction
The standalone $Y^{3/2}\propto|\nabla\pi|^3$ operator produces the structural BTFR scaling in a static spherical ansatz. The same ansatz exposes a large unscreened-force diagnostic, but it is not a relativistic PPN calculation and does not by itself falsify every completion. This document records that bounded result and the work still required.

### 2. The Genuine Success: BTFR
Varying the purely fractional kinetic action $\mathcal{L}_{grad} \propto \ell^2 |\nabla \pi|^3$ yields the exact field equation:
$$ \nabla \cdot (\ell^2 |\nabla \pi| \nabla \pi) \propto \frac{\rho_b}{f} $$
For a static spherical source $M$, integrating this gives:
$$ \ell^2 |\pi'|^2 4\pi r^2 \propto \frac{M}{f} $$
$$ |\pi'| \propto \frac{\sqrt{M/\ell^2 f}}{r} $$

The anomalous fifth force is $a_5 = \pi'/f \propto \frac{\sqrt{M/\ell^2 f^3}}{r}$. 
Setting this equal to the centripetal acceleration $v^2/r$ gives a circular velocity:
$$ v^2 \propto \sqrt{M} \implies v^4 \propto M $$
This is the **Baryonic Tully-Fisher scaling**, derived structurally with no curve fitting. Matching its normalization to the empirical MOND scale imposes the target-conditioned relation $\ell^2 f^3=1/(4\pi G a_0)$; it is not a blind parameter prediction and does not make the full ITSM a one-parameter theory.

### 3. The Solar-System force-ratio diagnostic
Because $\ell$ and $f$ are locked by the BTFR matching, the ratio of the anomalous fifth force $a_5$ to Newtonian gravity $a_N = GM/r^2$ becomes independent of the free parameters:
$$ \frac{a_5}{a_N} = \frac{\sqrt{GMa_0}/r}{GM/r^2} = \sqrt{\frac{a_0 r^2}{GM}} = \frac{r}{r_M} $$
where $r_M = \sqrt{GM/a_0}$ is the MOND radius.

At 1 AU from the Sun ($M = M_\odot$):
- $a_N \approx 5.93 \times 10^{-3}$ m/s$^2$
- $a_0 \approx 1.2 \times 10^{-10}$ m/s$^2$
- $r_M \approx \sqrt{(1.327 \times 10^{20}) / (1.2 \times 10^{-10})} \approx 1.05 \times 10^{15}$ m

At $r = 1$ AU ($1.496 \times 10^{11}$ m):
$$ \frac{a_5}{a_N} \approx \frac{1.496 \times 10^{11}}{1.05 \times 10^{15}} \approx 1.4 \times 10^{-4} $$

Cassini constrains the metric PPN parameter $|\gamma-1|<2.3\times10^{-5}$. The displayed fifth-force ratio is not itself $|\gamma-1|$, so these quantities cannot be compared as identical observables. The $1.4\times10^{-4}$ force-ratio diagnostic nevertheless shows that a relativistic matter-metric and screening calculation is load-bearing; it does not by itself establish a Cassini exclusion or an order-of-magnitude count.

### 4. Limits of the standalone ansatz
Within the declared static, spherical standalone-cubic ansatz, the displayed profile is the exact nonlinear radial solution. This does not constitute the full relativistic PPN solution and does not exclude screening supplied by additional action terms or a distinct microscopic phase. Any claim involving $Z$, longitudinal characteristics or Vainshtein behavior must be rederived from the complete kinetic matrix in the same background and convention.

### 5. Conclusion: completion required
The standalone $|\nabla \pi|^3$ operator is not yet a viable complete Solar-System theory. To preserve its structural BTFR scaling, a completion must supply a relativistic matter metric, a controlled characteristic cone and a derived high-gradient response. An interpolating function is one candidate route, not an established resolution.

This motivates a fail-closed screening/completion gate rather than a physics PASS.

### 6. Open candidate: condensate disruption / Landau criterion

Condensate disruption is a physically motivated candidate within ITSM's finite-density identity, but it is presently **not derived**. A valid route must obtain the excitation spectrum and critical velocity from the parent action, solve the environmental profile and defect transition, project the physical matter metric, and calculate PPN and lensing observables. Until those steps pass, no claim that the Solar System destroys the condensate or shuts off the fifth force is authorized.

The target-conditioned scale matching proposed in `CBR-002_SCALE_DERIVATION.md` does not fix $f$ and $\ell$ as a blind prediction and cannot be used to declare either kinetic screening falsified or condensate disruption proven. CBR-002 and VOR-001 therefore remain open.
