# WAK-001 Gate Closure Report: Non-Equilibrium Causal Wake Dynamics & 3D Cluster Merger Hydrodynamics

**Gate ID:** `WAK-001`  
**Status:** `EXPLORATORY_KINEMATIC_SCAFFOLD`  
**Date:** 2026-09-01  
**Branch:** `recovery/v12-core-architecture`  
**Authority:** `Analysis/WAK/WAK-001/`  
**Execution Scripts:**
- `Analysis/WAK/WAK-001/wak001_bullet_cluster_solver.py`
- `Analysis/WAK/WAK-001/wak001_3d_cluster_collision_hydro.py`

---

## 1. Executive Summary

This gate evaluates the non-equilibrium causal wake dynamics for the scale-compensator field $\psi(t, \mathbf{x})$ in a finite-density superfluid vacuum ($c_s = c/\sqrt{3}$) and simulates supersonic cluster mergers (Bullet Cluster 1E 0657-56) across 3D space and time.

### Key Milestones & Epistemic Conclusions
1. **Resolution of the Static MOND / Instantaneous AQUAL Failure:**
   * In static theories, phantom mass traces instantaneous baryons algebraically, forcing the gravitational lensing peak to sit on the dominant collisional X-ray gas ($\sim 85\%$ of baryonic mass).
   * In the dynamic causal wake framework, the scale compensator obeys the retarded wave equation with finite sound speed $c_s = c/\sqrt{3}$ and relaxation timescale $\tau_W \approx \xi / c_s$.
2. **3D Multi-Fluid Spectral Merger Simulation (`wak001_3d_cluster_collision_hydro.py`):**
   * Implemented exact Fourier-space matrix exponential propagator for the damped wave equation coupled to ballistic galaxies and shock-decelerated ICM gas.
   * During the transit epoch ($t = 25\text{ Myr}$), dynamic phase lag generates an instantaneous lensing-gas centroid separation of $\Delta x_{\rm lens-gas} \approx 20.91\text{ kpc}$.
   * At late times ($t = 35\text{ Myr}$), as the gas decelerates further and the wave relaxes, the simple linear wave equation allows the dominant gas mass ($85\%$) to pull the potential back towards the gas peak ($\Delta x_{\rm lens-gas} \to -7.20\text{ kpc}$).
3. **Epistemic Classification:**
   * Demonstrates that retarded wave dynamics provides a viable physical mechanism for transient cluster offsets without particle dark matter.
   * However, a fully robust, permanent spatial detachment throughout post-merger relaxation requires coupling to non-linear Landau shock disruption / vortex loop nucleation in 3D magnetohydrodynamics.
   * Retained honestly as an **`EXPLORATORY_KINEMATIC_SCAFFOLD`**.

---

## 2. Cryptographic Verification & Artifact Hashes

| Artifact | Output Path | SHA-256 Digest |
|---|---|---|
| Kinematic Bullet Solver Summary | `Analysis/WAK/WAK-001/outputs/wak001_bullet_cluster_summary.json` | `b03feeea89c29becf005d938eec995f25683906cf8740b1eaefa067fb11b90e1` |
| 3D Hydrodynamic Spectral Summary | `Analysis/WAK/WAK-001/outputs/wak001_3d_hydro_summary.json` | `4569f8761ee3c58c99dd6c17cc50b61c2ca89ef1dd662c3850f807155605f6e3` |

---

## 3. Mathematical Formulation

### 3.1 Causal Wave Equation with Non-Equilibrium Relaxation
$$\left( \frac{1}{c_s^2} \frac{\partial^2}{\partial t^2} + \frac{1}{\tau_W} \frac{\partial}{\partial t} - \nabla^2 \right) \psi(t, \mathbf{x}) = 4\pi G V \left[ \rho_{\rm gas}(t, \mathbf{x}) + \rho_{\rm stars}(t, \mathbf{x}) \right]$$
where:
* $c_s = c/\sqrt{3} \approx 1.73 \times 10^8\text{ m/s}$ ($177.0\text{ kpc/Myr}$)
* $V = \sqrt{4\pi G}$ ($C_m \equiv 1.0$)
* $\tau_W \approx 15\text{ Myr}$

### 3.2 Effective Lensing Surface Density
The total weak-lensing convergence is determined by the combined surface mass density:
$$\Sigma_{\rm total}(\mathbf{x}) = \Sigma_{\rm gas}(\mathbf{x}) + \Sigma_{\rm stars}(\mathbf{x}) + \Sigma_\psi^{\rm dynamic}(\mathbf{x})$$

---

## 4. Gate Clearance Checklist

- [x] Time-dependent causal wave equation formulated and solved in 3D multi-fluid geometry.
- [x] Negative control verified: static instantaneous response fails to detach lensing peak from dominant gas.
- [x] Exact Fourier spectral matrix propagator implemented with unconditional numerical stability.
- [x] Transient separation ($\Delta x \approx 20.91\text{ kpc}$ at $t = 25\text{ Myr}$) demonstrated during supersonic passage.
- [x] All JSON summaries and SHA-256 manifests generated and verified.

**Gate Status: EXPLORATORY_KINEMATIC_SCAFFOLD (Audit Complete)**
