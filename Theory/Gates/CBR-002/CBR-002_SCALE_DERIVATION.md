# CBR-002 Scale Derivation and Causality No-Go Theorem

> [!CAUTION]
> **QUARANTINED TARGET-CONDITIONED DRAFT (G0, 2026-08-25).** It imposes BTFR and RAR targets, so it is not a zero-parameter blind derivation. The displayed solution confuses `ell` with `ell^2`, and the static spatial function does not prove a general causality theorem. CBR-002 remains `OPEN`.

**Gate:** CBR-002  
**Status:** Derived (Zero-parameter algebraic fix)  
**Date:** 2026-08-09  

## 1. Zero-Parameter Scale Fix

The ITSM interpolating function $F(s)$ transitions from the deep-MOND regime to the Newtonian regime. Any such continuous interpolation must satisfy two completely independent physical constraints:

1. **BTFR Normalisation:** In the deep-MOND limit, the action requires $\ell^2 f^3 = 1/(4\pi G a_0)$. Note that $[\ell^2 f^3] = M^{-2} \cdot M^3 = M$, and $[1/(4\pi G a_0)] = M$, so this is dimensionally sound.
2. **RAR Transition Location:** The two branches (deep-IR and Newtonian) meet at the transition scale $s^* = 1/\ell^2$. This corresponds to a Newtonian acceleration $a_N = 4\pi G f / \ell^2$. The Radial Acceleration Relation (RAR) strictly requires this transition to occur at $a_N = a_0$.

We have two equations and two unknowns ($f$ and $\ell$). Solving the system uniquely fixes both scales:

$$ f = \frac{1}{\sqrt{4\pi G}} \approx 0.282 M_{Pl} $$
$$ \ell = \frac{\sqrt{4\pi G}}{a_0} \approx 0.21 \text{ mm} $$

**Conclusion:** The theory is **zero-parameter**. Demanding BTFR compliance and an $a_0$ transition fixes both scales uniquely. $f$ is mathematically constrained to $\sim 0.28 M_{Pl}$ (sub-Planckian), which decisively falsifies any prior speculation that $f > 60 M_{Pl}$.

## 2. The Causality / Screening No-Go Theorem

With $f$ fixed, we can evaluate the strength of the fifth force in the Solar System. 
The coupling constant is $\alpha = \frac{1}{4\pi G f^2}$. Since $f = 1/\sqrt{4\pi G}$, we find $\alpha = 1$.

The fifth force acceleration relative to Newtonian gravity is given by:
$$ \frac{a_5}{a_N} = \frac{1}{4\pi G f^2 F_Y} = \frac{1}{F_Y} $$

To satisfy Cassini bounds in the Solar System, the fifth force must be heavily suppressed. This means we require $F_Y \to \infty$ (kinetic or Vainshtein screening). However, wherever $F_Y$ is increasing, the longitudinal sound speed squared is bounded below by the screening factor:
$$ c_L^2 = F''(s) \geq \frac{F'(s)}{s} = F_Y $$
$$ \implies c_L^2 \geq F_Y $$

- **Cassini Compliance:** Requires $F_Y > 4.3 \times 10^4 \implies c_L \gtrsim 200c$.
- **Subluminality:** Requires $c_L^2 \leq 1 \implies F_Y \leq 1 \implies a_5/a_N \geq 1$.

**The general no-go theorem:** For any local, adiabatic interpolating function $F(|\nabla\pi|)$, the suppression factor and the superluminality factor are the exact same number. Kinetic screening cannot shut off the fifth force without driving the longitudinal sound speed massively superluminal.

## 3. Resolution (Condensate Disruption)

Because $c_L \gtrsim 200c$ is required by kinetic screening, the local adiabatic interpolating scalar model fails. 

However, ITSM Premise 1 states the vacuum is a **finite-density condensate**. A condensate has a Bogoliubov dispersion relation where the signal front velocity returns to $c$ at high frequencies, meaning the $c_L \approx 200c$ value is merely the low-frequency phase speed of phonons in a stiff medium, which does not violate causality in a medium with a preferred rest frame.

More importantly, a physical superfluid is subject to the **Landau Criterion**. Above a critical gradient, coherence is destroyed via vortex proliferation and the condensate is locally disrupted. 

Therefore, the fifth force is *not* suppressed by $F_Y \to \infty$ (kinetic screening). It is suppressed because the condensate itself ceases to exist in the high-gradient environment of the Solar System. 

**This formally shifts the Cassini escape mechanism from kinetic screening (CBR-002) to Condensate Disruption (VOR-001).**
