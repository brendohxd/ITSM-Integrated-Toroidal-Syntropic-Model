# Gate CBR-002: Task R-1
## The Exact Interpolating Function and the Causality Theorem

### 1. The Design Constraints
To preserve the structural Baryonic Tully-Fisher Relation (BTFR) derived from the $Y^{3/2}$ operator, while simultaneously passing the stringent Solar System bounds (Cassini) and avoiding gross causality violations, we must construct an interpolating kinetic function $F(Y)$, where $Y = (\nabla \pi)^2$.

The function must satisfy:
1. **Deep MOND ($Y \to 0$):** $F_Y \to \frac{\ell^2}{2} Y^{1/2}$, yielding $F(Y) \to \frac{\ell^2}{3} Y^{3/2}$.
2. **Solar System ($Y \to \infty$):** $F_Y \to 1$, yielding a canonical kinetic term $F(Y) \to Y$. 

By forcing $F_Y \to 1$ at high gradients, we abandon Vainshtein screening and instead rely on **weak fundamental coupling**. By setting the fundamental scalar coupling $\alpha = \frac{1}{4\pi G f^2} < 2.3 \times 10^{-5}$ (which requires $f > 60 M_{Pl}$), we safely pass the Cassini bound. Because the BTFR only constrains the combination $\ell^2 f^3 = 1/(4\pi G a_0)$, we can freely raise $f$ and shrink $\ell$ to preserve the exact MOND phenomenology.

### 2. The Interpolating Function
We define the exact closed-form derivative of the kinetic function:
$$ F_Y = \frac{A \sqrt{Y}}{1 + A \sqrt{Y}} \quad \text{where} \quad A = \frac{\ell^2}{2} $$
Integrating this yields the exact ITSM interpolating action:
$$ F(Y) = Y - \frac{2}{A} \sqrt{Y} + \frac{2}{A^2} \ln(1 + A \sqrt{Y}) $$

**Asymptotic Limits:**
- As $Y \to \infty$ (Solar System): $F_Y \to 1$. (Canonical).
- As $Y \to 0$ (Deep MOND): $\ln(1+A\sqrt{Y}) \approx A\sqrt{Y} - \frac{A^2 Y}{2} + \frac{A^3 Y^{3/2}}{3}$. 
  This yields $F(Y) \to \frac{2A}{3} Y^{3/2} = \frac{\ell^2}{3} Y^{3/2}$. (Exact MOND recovery).

### 3. The Superluminality Theorem
The local longitudinal sound speed is $c_L^2 = \frac{F_Y + 2Y F_{YY}}{F_Y} = 1 + 2Y \frac{F_{YY}}{F_Y}$.
Because $F_Y$ must transition from $0$ (at $Y=0$) to $1$ (at $Y=\infty$), the Mean Value Theorem dictates that $F_{YY}$ **must be strictly positive** in the transition region.
Therefore, $2Y \frac{F_{YY}}{F_Y} > 0$, meaning **$c_L^2 > 1$ is a strict mathematical inevitability for ANY interpolating MOND function.** It cannot be tuned away.

### 4. The Babichev-Mukhanov-Vikman (BMV) Resolution
For our specific interpolating function, the sound speed evaluates to:
$$ c_L^2 = \frac{2 + A \sqrt{Y}}{1 + A \sqrt{Y}} $$
- In the Solar System ($Y \to \infty$): $c_L^2 \to 1$. **Strictly luminal.**
- In Deep MOND ($Y \to 0$): $c_L^2 \to 2$. **Superluminal.**

This solves the Reviewer's challenge perfectly. The superluminality is purged from the Solar System where it would cause acute observational and causal crises. It is pushed exclusively into the deep-MOND galactic vacuum. As proven by Babichev, Mukhanov, and Vikman (2007), superluminal group velocities in non-linear scalar EFTs do not allow for the construction of closed timelike curves (CTCs) as long as the background is dynamically stable, because the characteristic Cauchy cones remain globally hyperbolic. 

The theory is causally safe, passes Cassini, and preserves the BTFR.
