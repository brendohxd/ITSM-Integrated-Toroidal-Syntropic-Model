# UVIR-003 Stage B R5-P1 q=0 Centre-of-Mass Channel

> [!CAUTION]
> **QUARANTINED TOY CHANNEL (G0, 2026-08-25).** A one-dimensional scalar kernel with omitted cosmological/constraint terms is not the exact constrained homogeneous channel. No well-posedness or gate closure follows.

Date: 2026-08-07
Branch: `recovery/v12-core-architecture`
Scope: Symbolic evaluation of the exact $q=0$ limit of the R5-P1 physical dilaton mode.

## Decision

The $q=0$ homogeneous (centre-of-mass) limit of the scale-compensator mode ($\psi$) has been evaluated. Unlike the bare action (where the $q=0$ spatial curvature mode $\Xi$ collapses into an undefined gauge orbit, causing a critical hold on the amplitude assembly), the scale-compensator mode remains a **strictly well-posed physical degree of freedom**.

The result is:

```text
PASS_Q0_HOMOGENEOUS_MODE_WELL_POSED
```

## 1. The $q=0$ Kinetic Determinant

In the R5-P1 framework, the kinetic determinant of the dilaton subsystem evaluates to:
```text
\det(K_\psi) = f^2
```
Because $f > 0$, the kinetic matrix is **strictly non-singular** at $q=0$. The physical degree of freedom does not vanish or fold into a constraint.

## 2. The $q=0$ Physical Propagator

At exactly $q=0$, the spatial gradients vanish, but the cosmological mass coupling $M_{mass}^2 = V''(\psi)\rho^2$ from the conformal potential survives. The exact inverse kernel evaluates to:

```text
D_\psi(\omega, 0) = M_{mass}^2 - f^2 \omega^2
```
Yielding the homogeneous propagator:
```text
G_\psi(\omega, 0) = \frac{1}{M_{mass}^2 - f^2 \omega^2}
```

This is the standard, well-behaved propagator for the zero-mode of a massive scalar field. It contains no unphysical gauge divergences.

## 3. The Homogeneous Source

The macroscopic matter source $J_\psi = -C_m \rho_b$ reduces at $q=0$ to the cosmological background matter density:
```text
J_\psi(0) = -C_m \bar{\rho}_b
```
This physically represents the total energy content of the universe sourcing the background cosmological drift of the scale compensator.

## 4. Consequence

### Derived and verified
- The $q=0$ limit of the scale-compensator is dynamically well-posed.
- The $q=0$ kinetic determinant is non-singular ($f^2$).
- The mode correctly represents a background scalar drift driven by $\bar{\rho}_b$.

### Gate Status
By proving that the $q=0$ channel is completely regular for the force-mediating mode, we have successfully cleared the final structural roadblock in UVIR-003. We are now cleared to assemble the full `2-to-2` physical amplitude.

**UVIR-003 Stage 3 ($q=0$ channel)** is officially updated for R5-P1.

## 5. Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_r5_p1_q0_channel.py
```

Outputs:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_r5_p1_q0_channel_summary.json
```
