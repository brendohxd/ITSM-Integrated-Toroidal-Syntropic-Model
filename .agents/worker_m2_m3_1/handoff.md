# Handoff Report: CLASS Integration of ITSM Fluid Equation of State

**Milestones Completed**: Milestone 2 & 3 (CLASS C Integration, Compilation, and Verification)
**Target Location**: `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim`
**Environment**: Windows, Conda (`itsm_env`), MinGW-w64 (gcc/g++)

---

## 1. Observation
- Standard CLASS (`v3.3.4`) was modified to include the **Integrated Toroidal-Syntropic Model (ITSM)** dark energy fluid equation of state.
- Windows compilation of Cython extensions defaults to Microsoft Visual C++ (MSVC), which is absent or fails under the custom MinGW environment.
- On Windows (Python 3.8+), DLL dependencies compiled with MinGW (such as `libgcc_s_seh-1.dll`, `libstdc++-6.dll`, `libwinpthread-1.dll` from the Strawberry toolchain) are not loaded from the system `PATH` dynamically, leading to `ImportError: DLL load failed` upon importing `classy` if not handled.

---

## 2. Logic Chain
1. **Model Implementation (C level)**:
   - Added `ITSM` to `equation_of_state` enum in `include/background.h` and variables `itsm_n0`, `itsm_na` in `struct background`.
   - Updated `source/input.c` to parse `'ITSM'` for `fluid_equation_of_state`, assign default values (`n0=3.0, na=0.0`), and read parameters `itsm_n0`, `itsm_na`.
   - Programmed the mathematical equations for $w(a)$, $dw/da$, and the analytical integral of the scaling density $\int 3\frac{1+w}{a'}da'$ inside `background_w_fld` in `source/background.c`.
   - Updated `python/cclassy.pxd` to expose `itsm_n0` and `itsm_na` in the Cython struct declarations.
2. **Build patches**:
   - Overrode `base_path` in `source/input.c` to default to `"."` on Windows to avoid backslash escaping issues in the internal parser.
   - Fixed math constant `M_PI_2` not being declared under standard C++ compiler in `tools/hyperspherical.c` by adding a fallback macro definition.
   - Updated `setup.py` to use `mingw32-make` instead of `make` when `os.name == "nt"`.
3. **Compilation**:
   - Compiled the static library `libclass.a` using `mingw32-make libclass.a -j`.
   - Solved PEP 517 build issues by creating `setup.cfg` containing `[build] compiler = mingw32`, which forces `pip install` to compile with the MinGW toolchain instead of defaulting to MSVC.
   - Installed `classy` in editable/develop mode using `python -m pip install -e .`.
4. **DLL Load Path Configuration**:
   - Patched `__init__.py` of `classy` to dynamically scan the system `PATH` on Windows for directories containing compiler executables (`g++.exe`/`gcc.exe`) or the required standard library DLL (`libstdc++-6.dll`) and add them to Python's DLL directory search path via `os.add_dll_directory()`.

---

## 3. Caveats
- **DLL Search Paths**: Standard python scripts running `classy` must be aware that if the MinGW/Strawberry compiler bin path (`C:\Strawberry\c\bin`) is removed from the `PATH` environment variable, the auto-detection in `__init__.py` will not find it, causing DLL import failure. The toolchain bin folder must remain in `PATH`.
- **Parameter Conflict**: When using `fluid_equation_of_state = 'ITSM'` (or any non-standard EoS), do not set `Omega_Lambda` in the initialization dictionary. Doing so conflicts with `Omega_fld` and triggers a CLASS fatal input check error.

---

## 4. Conclusion
- The CLASS Boltzmann solver now natively supports the ITSM toroidal-syntropic fluid model via the custom `ITSM` option.
- The wrapper builds, installs, and runs flawlessly on Windows using MinGW.
- Integration tests confirm that the numerical scaling of the fluid matches the analytical model within relative tolerances of $\sim 1.8 \times 10^{-8}$ (well within expected floating-point ODE solver integration limits).

---

## 5. Verification Method
- Execute the verification script:
  ```powershell
  C:\Users\brend\anaconda3\envs\itsm_env\python.exe verify_itsm.py
  ```
- The output displays the relative difference compared to analytical behavior ($a^{n_0 + n_a(1-a)}$) for a simple phantom case ($n_0=3.0, n_a=0.0$) and a general varying-exponent case ($n_0=3.2, n_a=-0.5$).
- Both cases must pass with a max relative difference $< 10^{-7}$.

### Sample Output:
```text
--- Running Verification for n0=3.0, na=0.0 ---
Max relative difference (z <= 10): 1.3928e-08
Verification passed successfully!

Redshift   CLASS Ratio   Analytical Ratio   Rel. Diff
   0.000      1.000000           1.000000    0.00e+00
   0.500      0.296372           0.296372    1.43e-09
   1.000      0.125019           0.125019    3.22e-09
   2.000      0.037052           0.037052    5.77e-09
   4.999      0.004632           0.004632    1.01e-08
   9.997      0.000752           0.000752    1.39e-08

--- Running Verification for n0=3.2, na=-0.5 ---
Max relative difference (z <= 10): 1.7955e-08
Verification passed successfully!
...
ALL VERIFICATIONS PASSED SUCCESSFULLY!
```
