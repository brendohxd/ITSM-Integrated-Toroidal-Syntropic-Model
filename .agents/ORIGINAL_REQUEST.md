# Original User Request

## Initial Request — 2026-06-15T04:16:16Z

Modify the CLASS (Cosmic Linear Anisotropy Solving System) simulation code to swap out its standard cosmological engine for the physics and parameters of the Integrated Toroidal-Syntropic Model (ITSM).

Working directory: c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim
Integrity mode: demo

## Verification Resources
You can reference the existing `itsm_mcmc_multicore.py` script in the root repository to understand the exact mathematical expansion history ($H(z)$) and parameter constraints of the ITSM model.

## Requirements

### R1. Modify CLASS Core
Clone the standard CLASS repository and read `background.c` to understand the expected behavior. Modify the core C codebase to deeply integrate the ITSM exact expansion history equations in place of standard $\Lambda$CDM.

### R2. Compile and Expose Python Wrapper
Compile the modified CLASS C codebase successfully and ensure the `classy` Python wrapper is exposed and importable within a Python script without errors.

### R3. Automated Background Verification
Write a Python test script (`verify_background.py`) that imports your modified `classy` module, runs a simulation, and programmatically asserts that the output Hubble expansion history $H(z)$ mathematically matches the theoretical ITSM equations.

### R4. Generate Cosmological Spectra
Write a Python plotting script (`plot_spectra.py`) that generates a visual comparison of the Cosmic Microwave Background (CMB) Power Spectrum ($C_l$) and the Matter Power Spectrum ($P(k)$) between the standard $\Lambda$CDM model and your modified ITSM engine.

### R5. Network Constraints
You must use network access solely to clone the CLASS repository and install any standard pip dependencies required for your verification scripts.

## Acceptance Criteria

### Compilation & Integration
- [ ] The modified CLASS C codebase compiles without fatal errors.
- [ ] The `classy` Python module can be imported cleanly.

### Verification Script
- [ ] `verify_background.py` executes successfully.
- [ ] `verify_background.py` prints "PASS" or a programmatic assertion success, confirming that the simulated $H(z)$ matches the ITSM equations within a reasonable numerical tolerance.

### Cosmological Output
- [ ] `plot_spectra.py` executes successfully.
- [ ] `plot_spectra.py` saves output plots visually comparing the CMB and Matter Power spectra between the two engines.
