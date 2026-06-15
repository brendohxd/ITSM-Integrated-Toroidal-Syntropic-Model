# CLASS Simulation Setup & Codebase Analysis Report

## 1. Executive Summary
This report analyzes the setup procedure for the standard public Cosmic Linear Anisotropy Solving System (CLASS) simulation for Milestone 1. We outline the precise Git clone commands to place the repository in the designated target directory and list the key source files within the CLASS codebase responsible for calculating the background Hubble parameter $H(z)$.

- **Repository URL**: `https://github.com/lesgourg/class_public.git`
- **Target Directory**: `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim`
- **Objective**: Establish a clone plan and identify target files to locate background Hubble parameter calculation logic.

---

## 2. Git Clone Plan

To safely clone the public CLASS repository into the local workspace without interfering with other experimental setups, follow the procedure below.

### 2.1 Verification & Pre-requisites
1. **Parent Directory Existence**: The parent directory `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental` exists (verified during the explorer investigation).
2. **Target Directory State**: Before cloning, verify if the directory `CLASS_Sim` already exists. 
   - If it does not exist, `git clone` will create it automatically.
   - If it exists and is non-empty, `git clone` will fail. Any existing files must be moved or the directory removed before running the clone command.

### 2.2 Cloning Command
Run the following command in PowerShell/Command Prompt:

```powershell
git clone https://github.com/lesgourg/class_public.git "c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim"
```

### 2.3 Post-Clone Verification
After executing the clone command, verify that:
1. The directory `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim` contains files like `Makefile`, `source/`, `include/`, `python/`, and `tools/`.
2. Running `git status` within that folder shows it is on the default branch (usually `master`) and clean.

---

## 3. Targeted Files in CLASS Codebase

In CLASS, cosmological equations are solved in a modular structure where each physical phenomenon is represented by a separate module. The background evolution of the universe (densities of species, conformal time, and the Hubble parameter $H$) is handled in the **background** module.

Below is the file checklist and explanation of where the Hubble parameter $H(z)$ is computed.

### 3.1 Key Files to Inspect

| File Path | Description / Key Focus |
|---|---|
| `include/background.h` | Header defining the background structure `struct background`, which stores cosmological parameters, background quantities, and the indices for the background interpolation table. |
| `source/background.c` | Contains the implementation of the background module, including equations, integration, and interpolation functions. |
| `python/classy.pyx` | Cython wrapper compiling the C code to the Python `classy` module. Defines how Python retrieves background parameters (including $H$). |
| `source/input.c` | Parses cosmological input parameters (e.g., $H_0$, $h$, $\Omega_b$) and stores them in the background structure. |

### 3.2 Detailed Code Locations to Investigate

#### A. `include/background.h`
This file defines the indices used to access elements of the background vector `pvecback`. Look for:
- `index_bg_H`: Index of the Hubble parameter $H$ in the background vector.
- `index_bg_H_conf`: Index of the conformal Hubble parameter $\mathcal{H} = aH$.
- `index_bg_a`: Index of the scale factor $a$.
- `index_bg_z`: Index of the redshift $z$.
- Struct declaration `struct background` which holds global background variables and the interpolation table `tau_table`, `background_table`.

#### B. `source/background.c`
This is the core C file where the numerical calculation takes place.
1. **`background_init`**:
   - Integrates the background equations from the early universe ($a \approx 10^{-10}$) to the present ($a = 1$).
   - Fills the interpolation table `background_table` as a function of conformal time $\tau$ (or scale factor $a$).
2. **`background_derivs` / `background_equations`**:
   - Defines the system of differential equations integrated by the ODE solver.
   - Computes the total energy density $\rho_{\text{tot}}$ as the sum of individual species (baryons, cold dark matter, photons, neutrinos, dark energy, curvature, etc.).
   - Computes the conformal Hubble parameter $\mathcal{H}$ using the Friedmann equation:
     $$\mathcal{H}^2 = a^2 H^2 = \frac{8\pi G}{3} a^2 \rho_{\text{tot}} - k$$
   - Stores the value of $H$ (Hubble parameter) and $\mathcal{H}$ (conformal Hubble parameter) at each step.
3. **`background_at_tau`**:
   - Takes a given conformal time $\tau$ and uses cubic spline/linear interpolation on `background_table` to output the background vector `pvecback`.
   - The caller can access the Hubble parameter via `pvecback[pba->index_bg_H]`.

#### C. `python/classy.pyx`
This Cython file implements the interface that allows Python users to query background parameters.
- Look for the `get_background()` method in the Python wrapper. This method typically retrieves the background evolution history as a Python dictionary.
- It iterates over the background table, calling `background_at_tau` for each step, and extracts values corresponding to `index_bg_z` (redshift) and `index_bg_H` (Hubble parameter).
- This is where the conversion between C-level data structures and Python dictionaries/numpy arrays is handled.

---

## 4. Recommendations for Implementer
Once the cloning is complete:
1. Open `include/background.h` and search for `index_bg_H`.
2. Open `source/background.c`, search for the function `background_derivs` or `background_equations` and locate the line where `pvecback[pba->index_bg_H]` or `H` is computed from the sum of densities.
3. Trace how different cosmological components (e.g., standard dark energy vs. modified gravity/syntropic terms) contribute to the Hubble parameter. This will be crucial for implementing the Integrated Toroidal Syntropic Model (ITSM) modifications.
