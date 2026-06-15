import os
import sys

# Ensure compiler path is added for DLL load on Windows
if sys.platform == 'win32':
    for path in os.environ.get('PATH', '').split(';'):
        if os.path.isdir(path):
            if os.path.exists(os.path.join(path, 'g++.exe')) or os.path.exists(os.path.join(path, 'gcc.exe')) or os.path.exists(os.path.join(path, 'libstdc++-6.dll')):
                try:
                    os.add_dll_directory(path)
                except Exception:
                    pass

from classy import Class
import numpy as np

def run_verification(n0, na):
    print(f"\n--- Running Verification for n0={n0}, na={na} ---")
    cosmo = Class()
    cosmo.set({
        'H0': 73.97,
        'Omega_b': 0.048,
        'Omega_cdm': 0.192,
        'Omega_fld': 0.760,
        'fluid_equation_of_state': 'ITSM',
        'itsm_n0': n0,
        'itsm_na': na,
        'use_ppf': 'yes'
    })
    cosmo.compute()

    bg = cosmo.get_background()
    z = bg['z']
    rho_fld = bg['(.)rho_fld']
    
    # Calculate scale factor
    a = 1.0 / (1.0 + z)
    
    # Compute analytical scaling
    analytical_ratio = a**(n0 + na * (1.0 - a))
    
    # Compute CLASS scaling (index -1 is z=0, today)
    class_ratio = rho_fld / rho_fld[-1]
    
    # Filter for z <= 10 (where dark energy dominates/is relevant and numerical noise is minimal)
    mask = z <= 10.0
    rel_diff = np.abs(class_ratio[mask] - analytical_ratio[mask]) / analytical_ratio[mask]
    max_rel_diff = np.max(rel_diff)
    
    print(f"Max relative difference (z <= 10): {max_rel_diff:.4e}")
    assert max_rel_diff < 1e-7, f"Verification failed: max relative diff {max_rel_diff:.4e} exceeds tolerance 1e-7"
    print("Verification passed successfully!")
    
    # Print a small table of values
    test_redshifts = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0]
    print("\nRedshift   CLASS Ratio   Analytical Ratio   Rel. Diff")
    for rz in test_redshifts:
        # Find closest redshift in the CLASS array
        idx = np.argmin(np.abs(z - rz))
        actual_z = z[idx]
        c_val = class_ratio[idx]
        a_val = analytical_ratio[idx]
        diff_val = np.abs(c_val - a_val) / a_val
        print(f"{actual_z:8.3f}   {c_val:11.6f}   {a_val:16.6f}   {diff_val:9.2e}")

if __name__ == '__main__':
    try:
        # Test Case 1: Simple phantom case (n0=3.0, na=0.0)
        run_verification(3.0, 0.0)
        
        # Test Case 2: General time-varying case (n0=3.2, na=-0.5)
        run_verification(3.2, -0.5)
        
        print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")
        sys.exit(0)
    except Exception as e:
        print(f"\nVERIFICATION FAILED: {e}", file=sys.stderr)
        sys.exit(1)
