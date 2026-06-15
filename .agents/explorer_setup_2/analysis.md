# Technical Analysis Report: Integrating the Integrated Toroidal-Syntropic Model (ITSM) into CLASS

**Author:** Explorer Setup 2 (`teamwork_preview_explorer`)  
**Date:** 2026-06-15T05:12:00Z  
**Status:** READ-ONLY EXPLORATION REPORT  
**Target Codebase:** Cosmic Linear Anisotropy Solving System (CLASS) C/Python API  

---

## 1. Executive Summary
This report analyzes the cloned CLASS codebase located at `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim` and details the exact mathematical and code-level modifications required to integrate the Integrated Toroidal-Syntropic Model (ITSM) equations.

The investigation focuses on:
1. Identifying how the background Hubble parameter $H(z)$ and its conformal derivative $H'$ are defined, computed, and exposed to Python in CLASS.
2. Formulating the mathematical translation of the ITSM expansion history—specifically its syntropic decay component—into the native variables used by CLASS.
3. Outlining two distinct integration strategies: **Direct Friedmann Modification (Strategy 1)** and **Fluid Component Mapping (Strategy 2)**, detailing the exact files, functions, line numbers, and code snippets for implementation.

---

## 2. CLASS Codebase Structure Analysis

### 2.1. Declaration of Background Structure and Indices
**File:** `include/background.h`  
**Key References:**
- **Lines 43–215:** Defines `struct background` which holds all background cosmological parameters, index mappings, and the precomputed interpolation tables.
- **Lines 159–160:** Declares the indices for the background quantities:
  ```c
  int index_bg_H;             /**< Hubble parameter in \f$Mpc^{-1}\f$ */
  int index_bg_H_prime;       /**< its derivative w.r.t. conformal time */
  ```
- **Lines 197–203:** Declares additional short/normal/long format vector indices, including critical density, comoving distance, conformal time, proper time, and sound horizon.

### 2.2. Computation of the Hubble Parameter $H(z)$
**File:** `source/background.c`  
**Key References:**
- **Line 371:** `int background_functions(...)`  
  This is the core function where CLASS evaluates all background densities, pressures, and the expansion rate at a given scale factor $a$.
- **Line 579:** The Friedmann equation is assumed:
  ```c
  pvecback[pba->index_bg_H] = sqrt(rho_tot-pba->K/a/a);
  ```
  *Note on Units:* In CLASS, all densities are normalized such that $\rho_{\text{class}} = \frac{8 \pi G}{3 c^2} \rho_{\text{physical}}$, meaning $H^2 = \rho_{\text{tot}} - \frac{K}{a^2}$.
- **Line 582:** The conformal time derivative $H' \equiv \frac{dH}{d\tau}$ is computed using the second Friedmann (acceleration) equation:
  ```c
  pvecback[pba->index_bg_H_prime] = - (3./2.) * (rho_tot + p_tot) * a + pba->K/a;
  ```

### 2.3. Integration and Interpolation of the Background
**File:** `source/background.c`  
- **Line 2589:** `int background_derivs(...)`  
  Calculates the derivatives of integrated background variables (conformal time $\tau$, proper time $t$, sound horizon $r_s$, and densities of decaying dark matter/radiation/fluid) with respect to the independent integration variable $\ln(a)$.
  ```c
  H = pvecback[pba->index_bg_H];
  dy[pba->index_bi_time] = 1./H;
  dy[pba->index_bi_tau] = 1./a/H;
  ```
- **Line 132:** `int background_at_z(...)`  
  Interpolates the background table at a requested redshift $z$ using $\ln(a) = -\ln(1+z)$ with a spline interpolator:
  ```c
  class_call(array_interpolate_spline(..., loga, ..., pvecback, ...), ...);
  ```

### 2.4. Python Exposure via classy
**File:** `python/classy.pyx`  
**Key References:**
- **Line 2864:** `def Hubble(self, z):`  
  Exposes the Hubble rate $H(z)$ to Python. It maps the redshift array to $\ln(a)$, calls the C function `background_at_z` to interpolate the background values, and retrieves `pvecback[self.ba.index_bg_H]`:
  ```python
  for iz, redshift in enumerate(zarr):
      if background_at_z(&self.ba,redshift,long_info,inter_normal,&last_index,pvecback)==_FAILURE_:
          ...
      H[iz] = pvecback[self.ba.index_bg_H]
  ```
- **Line 3160:** `def get_background(self):`  
  Exposes the full background table as a Python dictionary. It retrieves the column names using `background_output_titles` and the raw data array via `background_output_data`, formatting them into a dictionary of numpy arrays.

---

## 3. ITSM Cosmology and Modified Friedmann Equation

In the Integrated Toroidal-Syntropic Model (ITSM), the dark energy component is replaced by the "Syntropic Decay" of the active Superfluid Plenum. 

### 3.1. Mathematical Formulation
The Hubble parameter evolution is modified by replacing the cosmological constant ($\Omega_\Lambda$) with a redshift-evolving dark energy density $\Omega_{\text{itsm}}(z)$:
$$ H(z)^2 = H_0^2 \left[ \Omega_m (1+z)^3 + \Omega_r (1+z)^4 + \Omega_k (1+z)^2 + (1 - \Omega_m - \Omega_r - \Omega_k) (1+z)^{-n(z)} \right] $$

Where the decay parameter $n(z)$ evolves dynamically:
$$ n(z) = n_0 + n_a \frac{z}{1+z} = n_0 + n_a (1 - a) $$

This translates to the scale-factor-dependent energy density:
$$ \rho_{\text{itsm}}(a) = \rho_{\text{itsm}, 0} \, a^{n_0 + n_a (1 - a)} $$

### 3.2. Mapping to an Effective Fluid Equation of State $w_{\text{itsm}}(a)$
By applying the energy conservation equation $\frac{d\rho_{\text{itsm}}}{d\ln a} = -3(1+w_{\text{itsm}}(a))\rho_{\text{itsm}}$, we derive:
$$ \ln\rho_{\text{itsm}}(a) = \ln\rho_{\text{itsm}, 0} + \left( n_0 + n_a(1-a) \right)\ln(a) $$
Differentiating with respect to $\ln(a)$ (recalling $\frac{da}{d\ln a} = a$):
$$ \frac{d\ln\rho_{\text{itsm}}}{d\ln a} = n_0 + n_a(1-a) - n_a \, a \ln(a) $$
Thus:
$$ -3(1 + w_{\text{itsm}}(a)) = n_0 + n_a(1-a) - n_a \, a \ln(a) $$
$$ w_{\text{itsm}}(a) = -1 - \frac{1}{3} \left[ n_0 + n_a(1-a) - n_a \, a \ln(a) \right] $$

For $n_0 = 3$ and $n_a = 0$ (canonical syntropic volume decay):
$$ w_{\text{itsm}}(a) = -2 \quad \text{(constant phantom equation of state)} $$

The corresponding derivative with respect to the scale factor is:
$$ \frac{dw_{\text{itsm}}}{da} = \frac{n_a}{3} (2 + \ln(a)) $$

The analytic integral of the energy conservation equation $\int_a^{1} 3 \frac{1+w_{\text{itsm}}(a')}{a'} da'$ is:
$$ \text{integral\_fld} = \ln \left( \frac{\rho(a)}{\rho(1)} \right) = \left( n_0 + n_a(1-a) \right) \ln(a) $$

---

## 4. Integration Strategies for CLASS

### 4.1. Strategy 1: Direct Friedmann Equation Modification
This strategy hardcodes the ITSM equations directly into the background solver, replacing standard cosmological constant or fluid dark energy.

#### Code Modifications:
1. **`include/background.h`**:
   Add new parameters to `struct background`:
   ```c
   double itsm_n0;
   double itsm_na;
   short use_itsm;
   ```
2. **`source/input.c`**:
   Initialize defaults in `input_default_params` (around line 5914):
   ```c
   pba->use_itsm = _FALSE_;
   pba->itsm_n0 = 3.0;
   pba->itsm_na = 0.0;
   ```
   Read input parameters in `input_read_parameters` (around line 3300):
   ```c
   class_read_double("itsm_n0", pba->itsm_n0);
   class_read_double("itsm_na", pba->itsm_na);
   class_read_short("use_itsm", pba->use_itsm);
   ```
3. **`source/background.c`**:
   In `background_functions` (line 579), replace standard Hubble parameter calculation:
   ```c
   if (pba->use_itsm == _TRUE_) {
     double rho_itsm = (1.0 - pba->Omega0_m - pba->Omega0_r - pba->Omega0_k) * pow(pba->H0, 2) * pow(a, pba->itsm_n0 + pba->itsm_na * (1.0 - a));
     // Exclude other DE components, add rho_itsm to rho_tot
     pvecback[pba->index_bg_H] = sqrt(rho_tot + rho_itsm - pba->K/a/a);
     
     // Update derivative H_prime
     double w_itsm = -1.0 - (pba->itsm_n0 + pba->itsm_na * (1.0 - a) - pba->itsm_na * a * log(a)) / 3.0;
     double p_itsm = w_itsm * rho_itsm;
     pvecback[pba->index_bg_H_prime] = - (3./2.) * (rho_tot + rho_itsm + p_tot + p_itsm) * a + pba->K/a;
   } else {
     pvecback[pba->index_bg_H] = sqrt(rho_tot-pba->K/a/a);
     pvecback[pba->index_bg_H_prime] = - (3./2.) * (rho_tot + p_tot) * a + pba->K/a;
   }
   ```

### 4.2. Strategy 2: Fluid Component Mapping (Recommended)
Instead of modifying the Friedmann equation directly, we map the ITSM dark energy component to CLASS's built-in fluid component (`fld`). This preserves the standard Friedmann logic, automatically utilizes CLASS's robust perturbation equations (including the PPF approximation to safely handle $w < -1$), and avoids changing standard gravity modules.

#### Code Modifications:
1. **`include/background.h`**:
   - **Line 15:** Append `ITSM` to `enum equation_of_state`:
     ```c
     enum equation_of_state {CLP, EDE, ITSM};
     ```
   - Add parameters to `struct background`:
     ```c
     double itsm_n0;
     double itsm_na;
     ```
2. **`source/input.c`**:
   - **Line 3291:** Parse `ITSM` string:
     ```c
     else if ((strstr(string1,"ITSM") != NULL) || (strstr(string1,"itsm") != NULL)) {
       pba->fluid_equation_of_state = ITSM;
     }
     ```
   - **Line 3302:** Read parameters if `fluid_equation_of_state == ITSM`:
     ```c
     if (pba->fluid_equation_of_state == ITSM) {
       class_read_double("itsm_n0", pba->itsm_n0);
       class_read_double("itsm_na", pba->itsm_na);
       class_read_double("cs2_fld", pba->cs2_fld);
     }
     ```
   - **Line 5914:** Initialize defaults:
     ```c
     pba->itsm_n0 = 3.0;
     pba->itsm_na = 0.0;
     ```
3. **`source/background.c`**:
   Modify `background_w_fld` to return ITSM equation of state, derivative, and initial density integral:
   - **Line 678 (within the first switch block):**
     ```c
     case ITSM:
       *w_fld = -1.0 - (pba->itsm_n0 + pba->itsm_na * (1.0 - a) - pba->itsm_na * a * log(a)) / 3.0;
       break;
     ```
   - **Line 713 (within the derivative switch block):**
     ```c
     case ITSM:
       *dw_over_da_fld = pba->itsm_na * (log(a) + 2.0) / 3.0;
       break;
     ```
   - **Line 736 (within the integral switch block):**
     ```c
     case ITSM:
       *integral_fld = (pba->itsm_n0 + pba->itsm_na * (1.0 - a)) * log(a);
       break;
     ```

---

## 5. Verification Method

Once implemented, the integration can be verified using the following steps:
1. **Compilation:** Recompile CLASS and the Cython wrapper:
   ```bash
   make clean
   make
   ```
2. **Verification Script:** Run a Python script comparing the classy outputs against the analytical `H_itsm`:
   ```python
   from classy import Cosmology
   import numpy as np

   # Initialize CLASS with ITSM parameters
   cosmo = Cosmology()
   cosmo.set({
       'H0': 73.97,
       'Omega_b': 0.048,
       'Omega_cdm': 0.192,
       'Omega_Lambda': 0.0,
       'Omega_fld': 0.760,
       'fluid_equation_of_state': 'ITSM',
       'itsm_n0': 3.0,
       'itsm_na': 0.0
   })
   cosmo.compute()

   # Compare with analytical H(z)
   z = np.linspace(0, 2.0, 10)
   H_class = cosmo.Hubble(z) # in units of 1/Mpc, need to multiply by c to get km/s/Mpc
   c_kms = 299792.458
   H_class_kms = H_class * c_kms / 100.0 # class returns H/c, so convert to km/s/Mpc

   print("Redshift  H_class [km/s/Mpc]  H_analytical [km/s/Mpc]")
   for zi, hc in zip(z, H_class_kms):
       ha = 73.97 * np.sqrt(0.240 * (1+zi)**3 + 0.760 * (1+zi)**-3)
       print(f"{zi:8.2f}  {hc:20.4f}  {ha:23.4f}")
   ```
