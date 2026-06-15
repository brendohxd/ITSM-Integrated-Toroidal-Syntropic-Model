# Handoff Report - explorer_setup_2

## 1. Observation
We observed the following declarations and definitions in the CLASS codebase:
* **Background structure indices in `include/background.h`:**
  - Lines 159–160:
    ```c
    int index_bg_H;             /**< Hubble parameter in \f$Mpc^{-1}\f$ */
    int index_bg_H_prime;       /**< its derivative w.r.t. conformal time */
    ```
* **Background solver equations in `source/background.c`:**
  - Line 579 (Hubble parameter computation):
    ```c
    pvecback[pba->index_bg_H] = sqrt(rho_tot-pba->K/a/a);
    ```
  - Line 582 (conformal derivative of Hubble parameter):
    ```c
    pvecback[pba->index_bg_H_prime] = - (3./2.) * (rho_tot + p_tot) * a + pba->K/a;
    ```
  - Line 2589: The derivatives function `int background_derivs(...)` which computes:
    ```c
    dy[pba->index_bi_tau] = 1./a/H;
    ```
  - Line 664: The fluid equation of state selector function `int background_w_fld(...)`.
* **Python wrapping in `python/classy.pyx`:**
  - Line 2864: The Python-level method exposing $H(z)$ to Python:
    ```python
    def Hubble(self, z):
        ...
        H[iz] = pvecback[self.ba.index_bg_H]
        ...
    ```
  - Line 3160: The Python-level method exposing the full background table:
    ```python
    def get_background(self):
        ...
    ```
* **ITSM Cosmological Parameters:**
  - Observed in `Scripts/itsm_desi_bao.py` line 32:
    ```python
    H_itsm = H0_itsm * np.sqrt(Om_itsm * (1+z)**3 + (1-Om_itsm) * (1+z)**-3)
    ```
  - Observed in `Scripts/itsm_desi_evolving_n.py` lines 30–36:
    ```python
    def H_itsm(z, H0, Om, n0, na):
        n_z = n0 + na * z / (1.0 + z)
        radicand = Om * (1 + z)**3 + (1 - Om) * (1 + z)**(-n_z)
    ```

## 2. Logic Chain
1. **CLASS Interpolation Table:** CLASS integrates background variables with respect to $\ln(a)$ and stores them in a `background_table`. Any lookup of background values (including by the Python wrapper's `Hubble` and `get_background` methods) interpolates from this precomputed table.
2. **Centrality of `background_functions`:** The values stored in `background_table` are evaluated inside the C function `background_functions` in `source/background.c`. The Hubble parameter $H$ is computed strictly at line 579: `pvecback[pba->index_bg_H] = sqrt(rho_tot-pba->K/a/a)`.
3. **ITSM Physics Mapping:** In a flat universe, the ITSM syntropic decay modifies the expansion history by adding a dark energy term scaling as $(1+z)^{-n(z)} = a^{n_0 + n_a (1-a)}$.
4. **Effective Fluid Equivalence:** Under energy conservation, this component behaves as an effective fluid with equation of state $w_{\text{fld}}(a) = -1 - \frac{1}{3}[n_0 + n_a(1-a) - n_a a \ln(a)]$.
5. **Strategy Selection:**
   - *Strategy 1 (Direct)* changes the Friedmann equation itself inside `background_functions`. This requires manual adjustments of $H$ and $H'$ derivatives, which risks breaking standard General Relativity assumptions in other modules (e.g. perturbations).
   - *Strategy 2 (Fluid Mapping)* maps the ITSM component to CLASS's built-in `fld` component by defining $w_{\text{fld}}(a)$ and its analytical integral in `background_w_fld`. This automatically ensures that:
     - The Friedmann solver works out-of-the-box.
     - Perturbation equations (using the PPF approximation for $w < -1$) are solved correctly.
     - No modifications are needed to the C++ core gravity solver or the Cython wrapper.

## 3. Caveats
- We did not compile or run test cases because of the strict read-only constraint of our exploration.
- The analysis assumes that the Superfluid Plenum's effect on the background is fully described by the effective evolving dark energy density component. Any other coupled/non-adiabatic interactions (e.g. direct energy exchange with baryons/radiation) would require modifying the conservation equations of those components in `background_derivs`.

## 4. Conclusion
Integrating the ITSM model into CLASS is best accomplished by using **Strategy 2 (Fluid Mapping)**. By mapping the Plenum's syntropic decay to CLASS's native `fld` component with an effective equation of state $w(a) = -1 - \frac{1}{3}[n_0 + n_a(1-a) - n_a a \ln(a)]$, we can leverage CLASS's existing background integration, PPF perturbation engine, and Cython wrapper without hardcoding modifications to the core Friedmann solver.

## 5. Verification Method
To verify the implementation of Strategy 2:
1. Compile the modified CLASS solver:
   ```bash
   make clean && make
   ```
2. Initialize classy in Python and set the parameters:
   ```python
   from classy import Cosmology
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
   ```
3. Verify that the output of `cosmo.Hubble(z)` matches the analytical formula $H(z) = 73.97 \sqrt{0.240(1+z)^3 + 0.760(1+z)^{-3}}$ within machine precision.
