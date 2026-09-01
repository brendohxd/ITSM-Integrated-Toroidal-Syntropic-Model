import sys

try:
    from classy import Class
    import numpy as np
    print("SUCCESS: Imported classy successfully!")
    
    cosmo = Class()
    cosmo.set({
        'H0': 73.97,
        'Omega_b': 0.048,
        'Omega_cdm': 0.192,
        'Omega_Lambda': 0.0,
        'Omega_fld': 0.760,
        'fluid_equation_of_state': 'ITSM',
        'itsm_n0': 3.0,
        'itsm_na': 0.0,
        'use_ppf': 'yes'
    })
    cosmo.compute()
    print("SUCCESS: Computed cosmology with ITSM parameters!")
    
    # Retrieve H(z) from CLASS
    z = np.linspace(0, 2.0, 5)
    H_class = np.array([cosmo.Hubble(zi) for zi in z])  # returned in units of Mpc^-1
    c_kms = 299792.458
    H_class_kms = H_class * c_kms
    
    # Analytical calculation
    Om_m = 0.240
    Om_fld = 0.760
    H_analytical = 73.97 * np.sqrt(Om_m * (1 + z)**3 + Om_fld * (1 + z)**-3)
    
    print("Redshift   H_class [km/s/Mpc]   H_analytical [km/s/Mpc]   Diff")
    for zi, hc, ha in zip(z, H_class_kms, H_analytical):
        print(f"{zi:8.2f}   {hc:20.6f}   {ha:23.6f}   {abs(hc-ha):10.2e}")
        
except Exception as e:
    print("ERROR:", e)
    sys.exit(1)
