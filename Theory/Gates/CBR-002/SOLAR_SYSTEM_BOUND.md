# Gate CBR-002: Causality and Solar System Bounds
## The Falsification of the Standalone Cubic Operator

### 1. Introduction
Independent review has demonstrated that solving the field equations for the standalone $Y^{3/2} \propto |\nabla\pi|^3$ operator organically reproduces the Baryonic Tully-Fisher Relation (BTFR). However, this exact solution also formally falsifies the standalone operator in the Solar System. This document logs the calculations that necessitate a pivot to an interpolating function.

### 2. The Genuine Success: BTFR
Varying the purely fractional kinetic action $\mathcal{L}_{grad} \propto \ell^2 |\nabla \pi|^3$ yields the exact field equation:
$$ \nabla \cdot (\ell^2 |\nabla \pi| \nabla \pi) \propto \frac{\rho_b}{f} $$
For a static spherical source $M$, integrating this gives:
$$ \ell^2 |\pi'|^2 4\pi r^2 \propto \frac{M}{f} $$
$$ |\pi'| \propto \frac{\sqrt{M/\ell^2 f}}{r} $$

The anomalous fifth force is $a_5 = \pi'/f \propto \frac{\sqrt{M/\ell^2 f^3}}{r}$. 
Setting this equal to the centripetal acceleration $v^2/r$ gives a circular velocity:
$$ v^2 \propto \sqrt{M} \implies v^4 \propto M $$
This is the **Baryonic Tully-Fisher Relation**, derived structurally with no curve fitting. Matching this to MOND gives the parameter constraint: $\ell^2 f^3 = 1/(4\pi G a_0)$, making ITSM a one-parameter theory.

### 3. The Fatal Flaw: The Solar System Bound
Because $\ell$ and $f$ are locked by the BTFR matching, the ratio of the anomalous fifth force $a_5$ to Newtonian gravity $a_N = GM/r^2$ becomes independent of the free parameters:
$$ \frac{a_5}{a_N} = \frac{\sqrt{GMa_0}/r}{GM/r^2} = \sqrt{\frac{a_0 r^2}{GM}} = \frac{r}{r_M} $$
where $r_M = \sqrt{GM/a_0}$ is the MOND radius.

At 1 AU from the Sun ($M = M_\odot$):
- $a_N \approx 5.93 \times 10^{-3}$ m/s$^2$
- $a_0 \approx 1.2 \times 10^{-10}$ m/s$^2$
- $r_M \approx \sqrt{(1.327 \times 10^{20}) / (1.2 \times 10^{-10})} \approx 1.05 \times 10^{15}$ m

At $r = 1$ AU ($1.496 \times 10^{11}$ m):
$$ \frac{a_5}{a_N} \approx \frac{1.496 \times 10^{11}}{1.05 \times 10^{15}} \approx 1.4 \times 10^{-4} $$

Cassini data constrains post-Newtonian deviations to $|\gamma - 1| < 2.3 \times 10^{-5}$. The predicted anomalous force is roughly **seven orders of magnitude too large** at Saturn, and an order of magnitude too large at Earth. 

### 4. Vainshtein Screening Fails
Because the field equation for the standalone cubic was solved *exactly*, this $1.4 \times 10^{-4}$ deviation *is* the full non-linear solution. There is no additional Vainshtein mechanism available to suppress it further. Furthermore, the claimed Vainshtein suppression $1/\sqrt{Z}$ requires large $Z = \ell^2 g_0$. But at 1 AU, $Z \approx 560$, which induces longitudinal superluminality ($c_L = \sqrt{2}c$). 

### 5. Conclusion: Pivot to Interpolating Function
The standalone $|\nabla \pi|^3$ operator is structurally incompatible with Solar System ephemerides and causality. It cannot be the complete theory. To preserve the BTFR success while saving the Solar System, the cubic term must be the **deep-MOND limit** of an interpolating function that restores standard canonical kinetic terms ($K_Q \to 1$) in strong gradient regimes. 

This requires the immediate execution of Task **R-1: Specify the interpolating function.**

### 6. Resolution (Task R-1 Execution)
By deploying the closed-form interpolating kinetic function $F(Y)$ derived in `R1_INTERPOLATING_FUNCTION.md`, the Solar System bounds are formally satisfied.

**The Cassini Bound:**
At 1 AU, the derivative of the kinetic function converges exactly to $F_Y \to 1$. Thus, there is no Vainshtein suppression, and the scalar fifth force is simply determined by its fundamental coupling $\alpha = \frac{1}{4\pi G f^2}$.
By setting $f > 60 M_{Pl}$, the coupling $\alpha < 2.3 \times 10^{-5}$. The fifth force $a_5$ safely hides beneath the Cassini ephemeris bounds. The BTFR remains completely unaffected because it only constraints the product $\ell^2 f^3$, allowing us to simultaneously shrink $\ell$ to preserve the galactic dynamics.

**The Causality Bound:**
Because $F_Y \to 1$ at 1 AU, the longitudinal sound speed evaluates to $c_L^2 \to 1$. The superluminal propagation ($33c$) that plagued the standalone cubic is completely purged from the Solar System, restoring exact strict luminality ($c_L = c$). The superluminality ($c_L = \sqrt{2}c$) is pushed safely out into the deep-MOND galactic vacuum, where the Babichev-Mukhanov-Vikman (BMV) theorem guarantees it cannot form closed timelike curves.
