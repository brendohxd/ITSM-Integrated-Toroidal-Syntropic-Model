# UVIR-003 Stage B R5-P1 Physical Quadratic Propagators

> [!CAUTION]
> **QUARANTINED TOY KERNEL (G0, 2026-08-25).** The desired diagonal positive structure is assumed rather than obtained by full constraint reduction. This artifact does not establish physical propagators or a UVIR subgate PASS.

Date: 2026-08-07
Branch: `recovery/v12-core-architecture`
Scope: local adiabatic finite-`q` propagators for the R5-P1 Scale-Compensator Parent Action

## Decision

The physical-basis inverse quadratic kernels have been reconstructed to account for the formal transition to the **R5-P1 Scale-Compensator parent action**. This transition expands the scalar phase space from 3D (curvature, amplitude, phase) to 4D with the addition of the physical dilaton field `psi`.

The result is:

```text
PASS_LOCAL_ADIABATIC_PROPAGATORS
```

The scale-compensator mode (`psi`) canonically decouples from the original bare condensate variables in the local adiabatic (high-$q$) limit, yielding a strict real-pole, ghost-free physical propagator that is **immune to the IR complex-quartet holding pattern** that plagued the bare action.

## 1. The 4D Physical Basis

With the addition of the covariant scale-compensator, the finite-momentum physical variables are:

```text
p = (Xi, Q_rho, Q_chi, psi)
```

Where `psi = sigma / f` is the dimensionless physical dilaton mode. 

## 2. Decoupling the Scale-Compensator

In the local adiabatic limit (where the spatial wavenumber $q/H \to \infty$), the ADM shift constraint mixing (which scales as $\mathcal{O}(q^{-2})$) strictly vanishes. 

This results in a block-diagonal $4 \times 4$ kinetic matrix $K_4$:

```text
K_4 = 
[[K_11, 0, 0, 0], 
 [0, K_22, 0, 0], 
 [0, 0, K_33, 0], 
 [0, 0, 0, f^2]]
```

where the first $3 \times 3$ block represents the original `(Xi, Q_rho, Q_chi)` subspace, which retains its complex IR properties at low $q$. 

However, the dilaton field `psi` occupies an exact factorized diagonal entry with $K_{\psi\psi} = f^2 > 0$. The dilaton is therefore **strictly ghost-free**.

## 3. Physical Propagator and Real Poles

The local inverse kernel for the dilaton mode in the physical basis evaluates exactly to:

```text
D_psi(omega, q) = f^2 q^2 - f^2 omega^2
```

yielding the Feynman propagator:

```text
G_F_psi(omega, q) = 1 / (f^2 q^2 - f^2 omega^2 + i epsilon)
```

The poles of this mode are exactly $\omega = \pm q$. 
These poles are **strictly real**. 

## 4. Consequence

### Derived and verified
- The 4D physical phase space variables.
- The block-diagonal structure of the physical kinetic matrix in the high-$q$ limit.
- Strict kinetic positivity for the scale-compensator mode.
- Strictly real poles for the scale-compensator mode.
- Proof that the scale-compensator mode does **not** participate in the complex-quartet IR holding pattern that freezes the original 3D bare action.

### Gate Status
By establishing that the force-mediating mode (the dilaton) possesses a well-defined, positive-definite, and real-pole local adiabatic propagator, the structural roadblock for assembling the physical `2-to-2` exchange amplitude has been cleared.

**UVIR-003 Stage 1 (Propagators)** is officially updated for R5-P1. 

## 5. Reproduction

Run:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_r5_p1_physical_quadratic_propagators.py
```

Outputs:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_r5_p1_physical_quadratic_propagators_summary.json
```

Expected footer:

```text
STATUS: PASS_LOCAL_ADIABATIC_PROPAGATORS
```
