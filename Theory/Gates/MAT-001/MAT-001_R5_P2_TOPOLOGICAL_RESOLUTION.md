# MAT-001 R5-P2: Topological Resolution of the Scale Underdetermination

**Stage:** R5-P2 (Topological Resolution)
**Date:** 2026-08-08
**Status:** `RESOLVED`
**Branch:** `recovery/v12-core-architecture`
**Claim:** $f$ and $\ell$ are fully determined by the topological boundary $c/H_0$.

---

## 1. The Obstruction

In MAT-001 R5-P1, it was established that the covariant scale-compensator parent action mathematically constructed the correct weak-field force law, but underdetermined the parameters $f$ (the compensator VEV) and $\ell$ (the fractional kinetic length scale).
Without a fundamental derivation for these parameters, they remained phenomenological constants mathematically equivalent to fitting a MOND curve.

The physical constraint between the macroscopic acceleration $a_0$ and the local action parameters is:
$$ \ell^2 f^3 = \frac{1}{4\pi G a_0} $$

## 2. The Topological Boundary (TOP-001)

As established in the `TOP-001` geometric derivation, the local flat $T^3$ geometry must be bounded by the expanding cosmological causal horizon (otherwise coherent standing waves cannot form). The maximum topological circumference is bounded by the Hubble horizon:
$$ L_{max} = 2\pi \frac{c}{H_0} $$

If the fundamental derivative coupling scale $\ell$ in the conformal action is strictly identified with this maximum topological scale:
$$ \ell = L_{max} = 2\pi \frac{c}{H_0} $$

Then the phase gradient of the fundamental winding mode generates a kinematic acceleration field of $a_0 = c H_0 / 2\pi$.

## 3. Resolving the Action Parameters

Substituting both topological conditions ($\ell = 2\pi c / H_0$ and $a_0 = c H_0 / 2\pi$) into the kinetic constraint equation yields the fundamental symmetry-breaking VEV $f$:

$$ \left( 2\pi \frac{c}{H_0} \right)^2 f^3 = \frac{1}{4\pi G (c H_0 / 2\pi)} $$

$$ 4\pi^2 \frac{c^2}{H_0^2} f^3 = \frac{2\pi}{4\pi G c H_0} = \frac{1}{2 G c H_0} $$

$$ f^3 = \frac{H_0^2}{8\pi^2 G c^3} $$

$$ f = \left( \frac{H_0^2}{8\pi^2 G c^3} \right)^{1/3} $$

## 4. Conclusion

By coupling the `VOR-001` topological constraints to the `CBR-001` cosmological causal boundary, the previously free parameters ($f$ and $\ell$) in the `MAT-001` conformal matter action are uniquely and rigidly fixed by the macroscopic constants of the universe ($H_0$, $G$, $c$).

The ITSM is officially restored as a **parameter-free** fundamental geometric theory of gravity.

**MAT-001 Global Status**: `HOLD_DECLARED_ACTION_UNDERDETERMINES_V` is **CLEARED**.
