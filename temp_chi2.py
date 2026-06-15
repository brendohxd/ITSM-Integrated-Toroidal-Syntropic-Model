import os
import numpy as np
import pandas as pd

H0_kms_mpc = 71.2 # or 73.0, let's use 71.24
C_LIGHT = 299792.458
H0_si = H0_kms_mpc / (3.086e19)
a0_kms2 = (C_LIGHT * H0_si) / (2.0 * np.pi)
a0 = a0_kms2 * 3.086e16 # convert km/s^2 to (km/s)^2 / kpc

chi2_sum = 0.0
dof_sum = 0
sparc_path = 'SPARC_data'

for f in os.listdir(sparc_path):
    if not f.endswith('.dat'): continue
    df = pd.read_csv(os.path.join(sparc_path, f), sep=r'\s+', comment='#', names=['Rad','Vobs','errV','Vgas','Vdisk','Vbulge','SBdisk','SBbulge'])
    df.fillna({'Vbulge':0}, inplace=True)
    v_bar_sq = np.abs(df['Vgas'])*df['Vgas'] + 0.5*np.abs(df['Vdisk'])*df['Vdisk'] + 0.7*np.abs(df['Vbulge'])*df['Vbulge']
    v_bar_sq = np.maximum(v_bar_sq, 0.1)
    g_bar = v_bar_sq / df['Rad']
    g_tot = g_bar + (2/3)*np.sqrt(g_bar * a0)
    v_pred = np.sqrt(g_tot * df['Rad'])
    
    chi2 = np.sum(((df['Vobs'] - v_pred) / df['errV'])**2)
    chi2_sum += chi2
    dof_sum += len(df)

print(f"Global Zero-Param Chi2_nu: {chi2_sum / dof_sum:.2f} across {dof_sum} degrees of freedom")
