Integrated Toroidal-Syntropic Model (ITSM)
Relativistic Field Equations, Superfluid Dynamics, and Multi-Scale Falsifiability
Overview
The Integrated Toroidal-Syntropic Model (ITSM) is a theoretical framework that resolves modern cosmological tensions by deconstructing the nature of non-baryonic dark matter. Instead of unverified particle halos, the ITSM identifies the vacuum as an active Superfluid Plenum—a Bose-Einstein condensate with an inherent toroidal geometry (\chi = 2\pi).
By modeling the universe as an Open Thermodynamic Manifold, the ITSM introduces a continuous Syntropic Source Vector (Q^\nu) that accounts for the rapid structural maturity of the early universe (the "JWST crisis") and galactic rotation curve anomalies.
🚀 Key Mathematical Foundations
 * The Yield Threshold (a_0): Derived from macroscopic circulation quantization:
   
 * The Fractional Lagrangian: An unconditionally stable, ghost-free modification to the Einstein-Hilbert action:
   
 * Geometric Scaffolding: Redefines the z > 14 timeline via a toroidal geometric mold.
📊 Empirical Validations (Computational Appendix)
This repository contains the Python scripts used to generate the primary empirical validations of the ITSM.
1. Kinematic Crush Test (NGC 1560)
Validates the a_0 thresholding effect against the SPARC database. The ITSM perfectly tracks the "baryonic wiggle" at 5 kpc where Newtonian physics fails.
 * File: itsm_ngc1560_validation.py
 * Asset: ngc1560_plot.png
2. High-Redshift Assembly (JADES-GS-z14-0)
A triple-panel simulation contrasting the stochastic assembly of \LambdaCDM against the ITSM’s geometric scaffolding. It proves that the toroidal vacuum organizes matter into mature disks significantly faster than standard models.
 * File: itsm_z14_scaffold.py
 * Asset: itsm_z14_scaffold.png
3. Bullet Cluster Kinetic Separation
Demonstrates that gravitational lensing (the metric wake) decouples from the stalled gas bulk during cluster collisions as a fluid-dynamic necessity.
 * File: itsm_bullet_decoupling.py
 * Asset: itsm_bullet_decoupling.png
📂 Repository Structure
├── Manuscript/
│   └── ITSM_v7.7_Master.pdf        # Complete LaTeX Manuscript
├── Scripts/
│   ├── itsm_ngc1560_validation.py  # Rotation Curve Engine
│   ├── itsm_z14_scaffold.py        # High-Redshift Sim
│   └── itsm_bullet_decoupling.py   # Cluster Collision Sim
├── Assets/
│   ├── ngc1560_plot.png            # Validation Plots
│   ├── itsm_z14_scaffold.png
│   └── itsm_bullet_decoupling.png
└── README.md                       # This file

👨‍🔬 About the Author
Brendon Boyd is an Independent Researcher based in Perth, Western Australia, operating as an Absolute Truth Seeker & Analyst. The pursuit is mandated by a commitment to analyze queries through the deconstruction of standard narratives and the examination of objective causal chains. By prioritizing raw, verifiable accuracy over societal or institutional inertia, this work seeks to discern the objective truth of the Superfluid Plenum through deep-dive analysis of astrophysical anomalies.
⚖️ Ethical AI Declaration
Generative AI has been utilized in this project strictly as a computational torque wrench. Its application is confined to the synthesis of formatting, grammatical structuring, and the parsing of original mathematical derivations into publication-ready LaTeX. While AI assists in pressure-testing logic and streamlining structural execution, it does not originate the underlying physics or the ontological insights of the ITSM. The core architecture remains the original work of the author.
🛠️ Usage
To replicate the results locally:
 * Clone the repository: git clone https://github.com/BrendonBoyd/ITSM.git
 * Install dependencies: pip install numpy pandas matplotlib
 * Run any validation script: python Scripts/itsm_ngc1560_validation.py
Citation
If utilizing this framework or the associated computational scripts in your research, please cite:
> Boyd, B. (2026). The Integrated Toroidal-Syntropic Model: Relativistic Field Equations, Topology-Induced Superfluid Dynamics, and Multi-Scale Falsifiability.
> 

print(f"a0 = {a0:.2e} m/s²")

# Plot
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(r, vpure, 'r-', label='Pure ITSM')
ax.plot(r, vsupp, 'orange-', label='EFE Suppressed')
ax.plot(r, vn, 'b--', label='Newtonian')
ax.set(xscale='log', xlabel='Radius (kpc)', ylabel='Velocity (km/s)', title='ITSM Rotation Curves (a0 Alignment)')
ax.legend(); ax.grid(True, alpha=0.3)
plt.show()
