# ITSM Experiments

This directory contains standalone computational experiments, proofs-of-concept, and sandbox simulations used to validate various physical mechanisms and hypotheses within the Integrated Toroidal-Syntropic Model (ITSM). 

Unlike the core cosmology scripts in the `Scripts/` directory which are used to generate the figures and statistics for the main manuscript, the contents here represent exploratory or falsification tests.

## Contents

### 1. GPE_Transverse
**Path:** `/Experiments/GPE_Transverse/`

Contains 3D Gross-Pitaevskii Equation (GPE) solvers (both CPU-multicore and GPU-accelerated) designed to model the energy dissipation of a moving 'baryonic' potential within a periodic toroidal ($T^3$) superfluid. 

These scripts were utilized to rigorously test the hypothesis that the $C_{proj} = 2/3$ factor emerges strictly from macroscopic fluid dynamics (specifically, transverse vortex shedding vs. longitudinal acoustic radiation). The high-resolution parametric scans run by these scripts established a $19\%$ transverse ceiling, formally falsifying the hydrodynamic origin hypothesis and leading to the adoption of the rigid Transverse-Traceless (TT) tensor trace derivation.

* **`gpe_transverse_test.py`** - Base test script.
* **`gpe_transverse_test_cpu.py`** - Multicore (scipy.fft) implementation for broad parameter scanning.
* **`gpe_transverse_test_gpu.py`** - CuPy-accelerated version for high-resolution 3D grids.
