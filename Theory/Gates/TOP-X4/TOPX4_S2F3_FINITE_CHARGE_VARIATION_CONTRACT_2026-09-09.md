# TOP-X4 `X4-S2F3` finite-charge variation contract

**Date:** 2026-09-09
**Status:** `FINITE_CHARGE_OPERATOR_CHECKPOINT`; dynamic determinant held
**Physics pass:** false
**Gate effect:** none

## 1. Bounded question

Before constructing an evolving-state determinant, determine the finite-charge
quadratic operator that replaces the zero-density scalar degree count and
freeze how the semiclassical action must be varied. This checkpoint does not
insert the static Casimir potential into the A1 background and does not solve
the finite-charge semiclassical equations.

## 2. Complete action-level variation boundary

The calculation must start from

\[
 \Gamma=S_{I1C}+\Gamma_{\rm even}+\Gamma_{\rm odd}+\Gamma_{\rm ct},
\]

with the quantum sources defined covariantly before imposing the homogeneous
ansatz:

\[
 T^{(q)}_{AB}=-\frac{2}{\sqrt{-G}}
 \frac{\delta\Gamma_q}{\delta G^{AB}},\qquad
 E_i^{(q)}=+\frac{1}{\sqrt{-G}}\frac{\delta\Gamma_q}{\delta\phi_i},
 \quad \phi_i\in\{\rho,\theta,\chi\}.
\]

The diffeomorphism and global-`U(1)` Ward identities are mandatory consistency
conditions. Fixed-charge reduction may occur only after this variation. For
the homogeneous phase momentum

\[
 Q=a^3b\rho^2\mu,
\]

the phase Routhian is

\[
 L_Q=-\frac{NQ^2}{2a^3b\rho^2}.
\]

Its radial variation reproduces `-rho*mu^2`, while its lapse and both scale-
factor variations give the positive phase-kinetic energy and pressure. This
prevents an external fixed chemical potential from being silently substituted
for the frozen fixed-global-charge ensemble.

## 3. Constant-background charged scalar operator

On a constant, zero-winding background, write the canonical fluctuations as

\[
 \rho(x)=\rho_0+\sigma(x),\qquad
 \theta(x)=\mu t+\frac{\pi(x)}{\rho_0}.
\]

After applying the background equation `U_r=rho_0*mu^2`, the quadratic
Lagrangian is

\[
 \mathcal L_2=\frac12\dot\sigma^2+\frac12\dot\pi^2
 +2\mu\sigma\dot\pi
 -\frac12k_n^2(\sigma^2+\pi^2)-\frac12M_\sigma^2\sigma^2,
\]

where

\[
 k_n^2=k_{\rm obs}^2+\frac{n^2}{b^2},\qquad
 M_\sigma^2=U_{rr}-\mu^2.
\]

The mode equation is

\[
 (\omega^2-k_n^2-M_\sigma^2)(\omega^2-k_n^2)
 -4\mu^2\omega^2=0.
\]

At zero momentum it contains one Goldstone mode and one amplitude mode with
`omega_+^2=M_sigma^2+4*mu^2`. The Goldstone low-momentum speed is

\[
 c_s^2=\frac{M_\sigma^2}{M_\sigma^2+4\mu^2}.
\]

Thus the zero-density bookkeeping cannot be carried unchanged into the
finite-charge determinant. The two real condensate degrees of freedom become
one gapless and one gapped mixed branch. The neutral spectator-fermion
operator has no direct `mu` shift, although the evolving metric makes every
mode state dependent through `a(t)` and `b(t)`.

## 4. What this checkpoint can and cannot establish

The executable checkpoint may establish the algebra above, the nested
zero-charge factorization, the fixed-charge metric/radial variations, the
periodic KK momentum and the neutral-spectator boundary. It must also reject
an omitted amplitude-phase mixing term and a wrong-sign fixed-charge
Routhian.

It cannot establish:

- an evolving Hadamard/adiabatic state;
- adiabatic-order convergence or a renormalized state-dependent stress tensor;
- the coupled metric-radion-amplitude-phase constraint reduction;
- a physical radion pole or positive radion mass;
- parity-odd phase, anomaly or quantized-counterterm consistency;
- a continuous accepted EFT/stabilization domain.

The next calculation must construct the coupled time-dependent mode system on
the A1 background, declare its state and subtraction terms, and test
adiabatic-order convergence. A4 and Ultra remain closed.
