"""
ITSM N-body Cluster Collision Simulator (Bullet Cluster Phase Separation)
Author: Brendon Boyd
Standards: Tier-1 Peer-Reviewed Physics Journal Framework (revtex4-2)
Protocol: Leapfrog Integration with sub-grid Acoustic Locking
Environment: Windows / Antigravity IDE Workspace Compatible
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Configure styling
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from itsm_plot_style import apply_tier1_style
    apply_tier1_style()
except ImportError:
    pass

# Constants
G = 4.30091e-6  # kpc (km/s)^2 M_sun^-1
M_sun = 1.0     # Mass units in solar masses

# Cluster Parameters
M_main = 1e14   # Main cluster mass (M_sun)
M_sub  = 2e13   # Sub cluster mass (M_sun)

# Spatial scale and softening
epsilon = 150.0  # Plummer softening length (kpc)
r_core  = 250.0  # Core radius of gas distributions (kpc)

# Locking parameters
v_c = 600.0     # Critical locking velocity (km/s)
delta_v = 50.0  # Transition width (km/s)
gamma_0 = 8.0   # Locking strength (Gyr^-1) - converted to internal units below

# Conversion factors
Gyr_to_s = 3.15576e16
kpc_to_km = 3.08567758e16
km_s_to_kpc_Gyr = Gyr_to_s / kpc_to_km  # ~1.0227
gamma_Gyr = gamma_0 / 1.0227  # Convert to internal units

# Time integration parameters
dt = 0.005  # Time step in Gyr
t_max = 2.5 # Maximum simulation time in Gyr
steps = int(t_max / dt)

# State arrays: [x_s1, x_g1, x_s2, x_g2] and velocities [v_s1, v_g1, v_s2, v_g2]
# Index 0: Main Stars, 1: Main Gas, 2: Sub Stars, 3: Sub Gas
masses = np.array([M_main * 0.85, M_main * 0.15, M_sub * 0.85, M_sub * 0.15])

# Initial Conditions (1D collision axis)
x = np.array([-1200.0, -1200.0, 1200.0, 1200.0])  # kpc
v = np.array([800.0, 800.0, -2200.0, -2200.0])    # km/s

def get_gas_density(x_val, x_center):
    # Core gas density profile
    return np.exp(-np.abs(x_val - x_center) / r_core)

def get_accelerations(x_pos, v_vel, t):
    a = np.zeros(4)
    
    # 1. Gravitational Forces (Plummer potential)
    for i in range(4):
        for j in range(4):
            if i != j:
                dx = x_pos[i] - x_pos[j]
                dist_sq = dx**2 + epsilon**2
                a[i] -= G * masses[j] * dx / (dist_sq**1.5)
                
    # 2. Ram Pressure and Acoustic Locking (Gas components only)
    # Gas 1 (Main Gas, index 1) passes through Gas 2 (Sub Gas, index 3)
    # Gas density at other gas position (cross-densities)
    rho_1_at_2 = get_gas_density(x_pos[3], x_pos[1])
    rho_2_at_1 = get_gas_density(x_pos[1], x_pos[3])
    
    v_rel = v_vel[1] - v_vel[3]
    
    # Ram pressure coefficient (scaled to match physical Bullet Cluster drag)
    C_ram = 6.0e-4
    
    # Ram pressure deceleration (opposing relative motion)
    a_ram_1 = -C_ram * rho_2_at_1 * v_rel * np.abs(v_rel)
    a_ram_2 = C_ram * rho_1_at_2 * v_rel * np.abs(v_rel)
    
    a[1] += a_ram_1
    a[3] += a_ram_2
    
    # 3. ITSM Acoustic Locking Drag
    # Activates when gas velocity relative to the background plenum (v_vel) drops below v_c
    for i in [1, 3]:
        speed = np.abs(v_vel[i])
        # Smooth activation function centered at v_c
        activation = 0.5 * (1.0 - np.tanh((speed - v_c) / delta_v))
        a_locking = -gamma_Gyr * activation * v_vel[i]
        a[i] += a_locking
        
    return a

# Leapfrog Integration Loop
history_x = []
history_v = []
time_array = []

# Initial acceleration
a = get_accelerations(x, v, 0.0)

for step in range(steps):
    t = step * dt
    history_x.append(x.copy())
    history_v.append(v.copy())
    time_array.append(t)
    
    # Kick drift kick step
    v_half = v + 0.5 * a * dt * km_s_to_kpc_Gyr
    x = x + v_half * dt * km_s_to_kpc_Gyr
    
    a_next = get_accelerations(x, v_half, t + dt)
    v = v_half + 0.5 * a_next * dt * km_s_to_kpc_Gyr
    a = a_next

history_x = np.array(history_x)
history_v = np.array(history_v)
time_array = np.array(time_array)

# Plotting Results
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 11), sharex=True)
fig.subplots_adjust(hspace=0.08)

# Component Colors
c_main_s = 'blue'
c_main_g = 'lightblue'
c_sub_s  = 'darkred'
c_sub_g  = 'orange'

# Top Panel: Trajectories
ax1.plot(time_array, history_x[:, 0], color=c_main_s, lw=2.5, label='Main Cluster Stars')
ax1.plot(time_array, history_x[:, 1], color=c_main_g, lw=2.0, ls='--', label='Main Cluster Gas (ICM)')
ax1.plot(time_array, history_x[:, 2], color=c_sub_s, lw=2.5, label='Sub-Cluster Stars (Bullet)')
ax1.plot(time_array, history_x[:, 3], color=c_sub_g, lw=2.0, ls='--', label='Sub-Cluster Gas (ICM)')

ax1.axhline(0, color='gray', ls=':', alpha=0.5)
ax1.set_ylabel('Position Along Collision Axis [kpc]', fontsize=14)
ax1.set_title('ITSM Bullet Cluster Collision Simulation\nPhase Separation Induced by Sub-Grid Acoustic Vacuum Locking', fontsize=15, pad=15)
ax1.legend(loc='upper right', fontsize=11, framealpha=0.95)
ax1.grid(True, which='both', ls=':', alpha=0.4)

# Highlight collision zone and offset
collision_idx = np.argmin(np.abs(history_x[:, 0] - history_x[:, 2]))
collision_time = time_array[collision_idx]
ax1.axvline(collision_time, color='purple', ls=':', alpha=0.7)
ax1.annotate('Collision Event', xy=(collision_time, -1000), xytext=(collision_time - 0.5, -800),
             arrowprops=dict(arrowstyle='->', color='purple'), fontsize=12)

# End state offset
end_idx = -1
offset_stars = np.abs(history_x[end_idx, 0] - history_x[end_idx, 2])
offset_gas = np.abs(history_x[end_idx, 1] - history_x[end_idx, 3])
offset_sep = np.abs(history_x[end_idx, 2] - history_x[end_idx, 3])

ax1.annotate('', xy=(t_max - 0.05, history_x[end_idx, 2]), xytext=(t_max - 0.05, history_x[end_idx, 3]),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax1.text(t_max - 0.35, (history_x[end_idx, 2] + history_x[end_idx, 3])/2, fr'$\Delta X \approx {offset_sep:.1f}$ kpc',
         fontsize=11, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8))

# Bottom Panel: Velocities
ax2.plot(time_array, history_v[:, 0], color=c_main_s, lw=2.5)
ax2.plot(time_array, history_v[:, 1], color=c_main_g, lw=2.0, ls='--')
ax2.plot(time_array, history_v[:, 2], color=c_sub_s, lw=2.5)
ax2.plot(time_array, history_v[:, 3], color=c_sub_g, lw=2.0, ls='--')

ax2.axhline(0, color='gray', ls=':', alpha=0.5)
ax2.axhline(v_c, color='purple', ls=':', alpha=0.6, label='Acoustic Locking $v_c = 600$ km/s')
ax2.axhline(-v_c, color='purple', ls=':', alpha=0.6)
ax2.set_xlabel('Time [Gyr]', fontsize=14)
ax2.set_ylabel('Velocity [km/s]', fontsize=14)
ax2.legend(loc='lower right', fontsize=11, framealpha=0.95)
ax2.grid(True, which='both', ls=':', alpha=0.4)

plt.tight_layout()
script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.abspath(os.path.join(script_dir, "..", "Assets", "Figures", "itsm_bullet_nbody_publication.png"))
os.makedirs(os.path.dirname(out_path), exist_ok=True)
plt.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Simulation successfully complete!")
print(f"Stellar offset at t = {t_max} Gyr: {offset_stars:.2f} kpc")
print(f"Gas offset at t = {t_max} Gyr: {offset_gas:.2f} kpc")
print(f"Bullet Sub-cluster Stars-Gas separation: {offset_sep:.2f} kpc")
print(f"Plot saved to: {out_path}")
