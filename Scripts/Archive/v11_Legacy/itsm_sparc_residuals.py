import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import concurrent.futures
import multiprocessing
# ITSM Constants
c = 299792.458 # km/s
H0_km_s_Mpc = 72.97 # km/s/Mpc (ITSM predicted local value)
Mpc_to_km = 3.085677581e19
H0_s = H0_km_s_Mpc / Mpc_to_km # s^-1
a0_m_s2 = (c * 1000 * H0_s) / (2 * np.pi) # m/s^2

# Conversion for a0 into (km/s)^2 / kpc for galactic scales
kpc_to_m = 3.085677581e19 / 1000.0 # m
a0_kpc_s2 = a0_m_s2 / 1000.0 * (3.154e7)**2 / 1e9 # Not straightforward, let's use standard units
# Wait, R is in kpc, V is in km/s.
# a_0 = V^2 / R -> a_0 in (km/s)^2 / kpc
# 1 pc = 3.086e13 km -> 1 kpc = 3.086e16 km
a0_km_s2_kpc = a0_m_s2 * (3.085677581e19 / 1e3) / (1000.0**2) 
# Actually, the standard value of a0 in SPARC units is around 3600 (km/s)^2 / kpc
# Let's compute it:
a0_sparc_units = a0_m_s2 * 3.085677581e19 / 1e3 # (m/s^2) * (m/kpc) / (m^2/km^2)
# Let's just use the known value 1.08e-10 m/s^2 -> ~3700 (km/s)^2 / kpc
a0_sparc = a0_m_s2 * 3.086e16 / 1e3 # (km/s)^2 / kpc

# Let's fix Y_disk and Y_bulge for simple baseline
Y_disk = 0.5
Y_bulge = 0.7

def load_sparc_data(data_dir):
    files = glob.glob(os.path.join(data_dir, "*_rotmod.dat"))
    if not files:
        print(f"No _rotmod.dat files found in {data_dir}")
        return []
        
    all_data = []
    for f in files:
        # Columns: Rad, Vobs, errV, Vgas, Vdisk, Vbulge, SBdisk, SBbulge
        try:
            data = np.loadtxt(f, comments='#')
            if data.ndim == 1:
                data = data.reshape(1, -1)
            for row in data:
                all_data.append(row)
        except Exception as e:
            pass
    return np.array(all_data)

def compute_residuals(data):
    # data: [Rad, Vobs, errV, Vgas, Vdisk, Vbulge, ...]
    R = data[:, 0]
    V_obs = data[:, 1]
    err_V = data[:, 2]
    V_gas = data[:, 3]
    V_disk = data[:, 4]
    V_bulge = data[:, 5]

    # Newtonian Baseline
    V_bar_sq = V_gas * np.abs(V_gas) + Y_disk * V_disk**2 + Y_bulge * V_bulge**2
    # Ensure positive for sqrt
    V_bar_sq = np.maximum(V_bar_sq, 0)
    V_bar = np.sqrt(V_bar_sq)
    
    # MOND (Simple Interpolating Function)
    # V_MOND = sqrt(V_bar^2 / (1 - exp(-V_bar^2 / (R * a0))))
    x = V_bar_sq / (R * a0_sparc + 1e-10)
    V_mond_sq = V_bar_sq / (1 - np.exp(-x) + 1e-10)
    V_mond = np.sqrt(np.maximum(V_mond_sq, 0))
    
    # ITSM (Superfluid Plenum Shear)
    # V_ITSM = sqrt(V_bar^2 + (2/3) * sqrt(V_bar^2 * R * a0))
    V_itsm_sq = V_bar_sq + (2.0/3.0) * np.sqrt(V_bar_sq * R * a0_sparc)
    V_itsm = np.sqrt(np.maximum(V_itsm_sq, 0))

    # Residuals: dV / sigma_V
    res_newt = (V_obs - V_bar) / err_V
    res_mond = (V_obs - V_mond) / err_V
    res_itsm = (V_obs - V_itsm) / err_V
    
    return res_newt, res_mond, res_itsm

def plot_residuals(res_newt, res_mond, res_itsm, output_path="itsm_sparc_residuals.png"):
    plt.figure(figsize=(10, 6))
    
    sns.kdeplot(res_newt, label='Newtonian', fill=True, color='red', alpha=0.3)
    sns.kdeplot(res_mond, label='MOND (Simple)', fill=True, color='blue', alpha=0.3)
    sns.kdeplot(res_itsm, label='ITSM (Superfluid Plenum)', fill=True, color='green', alpha=0.5)
    
    plt.xlim(-10, 10)
    plt.axvline(0, color='black', linestyle='--', alpha=0.7)
    plt.title(f"SPARC Residual Distribution (N={len(res_itsm)} points)", fontsize=14)
    plt.xlabel(r"$\Delta V / \sigma_V$", fontsize=12)
    plt.ylabel("Probability Density", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved to {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "SPARC_data")
    
    print("Loading SPARC dataset...")
    data = load_sparc_data(data_dir)
    
    if len(data) > 0:
        print(f"Loaded {len(data)} data points.")
        num_cores = multiprocessing.cpu_count() or 4
        print(f"Utilizing {num_cores} cores for parallel SPARC residual analysis.")
        
        chunks = np.array_split(data, num_cores)
        res_newt_list, res_mond_list, res_itsm_list = [], [], []
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
            futures = [executor.submit(compute_residuals, chunk) for chunk in chunks]
            for future in concurrent.futures.as_completed(futures):
                n, m, i = future.result()
                res_newt_list.append(n)
                res_mond_list.append(m)
                res_itsm_list.append(i)
                
        res_newt = np.concatenate(res_newt_list)
        res_mond = np.concatenate(res_mond_list)
        res_itsm = np.concatenate(res_itsm_list)
        
        # Calculate reduced chi-squared for ITSM
        chi2_itsm = np.sum(res_itsm**2)
        dof = len(res_itsm) - 1 # Zero free parameters technically
        chi2_nu = chi2_itsm / dof
        
        print(f"ITSM Reduced Chi-Squared: {chi2_nu:.3f}")
        
        out_plot = os.path.join(base_dir, "itsm_sparc_residuals.png")
        plot_residuals(res_newt, res_mond, res_itsm, out_plot)
    else:
        print("Failed to execute due to missing data.")
