
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ---------------------------------------------------------
# ITSM Vector 4: High-Redshift Assembly (The Syntropic Scaffold)
# Triple-Panel Comparative Visualization (Black Background)
# ---------------------------------------------------------

# 1. Simulation Parameters
n_particles = 800
dt = 0.1
steps = 250
r_res = 12.0  # The geometric resonance radius (The Scaffold)

# Initialize particles in a high-entropy "Early Universe" state
# We use the same seed for both models to show the divergence from identical starts
pos_init = np.random.normal(0, 18, (n_particles, 2))
vel_init = np.random.normal(0, 0.5, (n_particles, 2))

# 2. Physics Constants
G = 1.0  
syntropy_strength = 5.0 # High concentration at z > 14

# 3. Setup Visualization
plt.style.use('dark_background')
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), facecolor='black')

for ax in [ax1, ax2, ax3]:
    ax.set_xlim(-45, 45)
    ax.set_ylim(-45, 45)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('black')

# Plots
particles_std = ax1.scatter([], [], color='cyan', s=1.5, alpha=0.5)
particles_itsm = ax2.scatter([], [], color='red', s=1.5, alpha=0.5)

# Overlay Panel
overlay_std = ax3.scatter([], [], color='cyan', s=1.0, alpha=0.3, label='Standard')
overlay_itsm = ax3.scatter([], [], color='red', s=1.0, alpha=0.5, label='ITSM')

ax1.set_title("Standard Model\nStochastic Assembly", color='cyan', fontsize=12)
ax2.set_title("ITSM (z=14)\nGeometric Scaffold", color='red', fontsize=12)
ax3.set_title("Structural Divergence\nOverlapping Comparison", color='white', fontsize=12)
ax3.legend(loc='lower right', fontsize=8, frameon=False)

# Global data for the simulation loop
data_std = {'pos': pos_init.copy(), 'vel': vel_init.copy()}
data_itsm = {'pos': pos_init.copy(), 'vel': vel_init.copy()}

# 4. Physics Engine
def update(frame):
    # A. Standard Model Logic (Pure Newtonian Gravity)
    r_std = np.sqrt(np.sum(data_std['pos']**2, axis=1)).reshape(-1, 1) + 2.0
    acc_std = -G * data_std['pos'] / (r_std**2.5)
    data_std['vel'] += acc_std * dt
    data_std['pos'] += data_std['vel'] * dt

    # B. ITSM Model Logic (Newton + Toroidal Scaffold)
    r_itsm_vec = data_itsm['pos']
    r_itsm_mag = np.sqrt(np.sum(r_itsm_vec**2, axis=1)).reshape(-1, 1) + 1.0
    
    # Newtonian Component
    acc_newton = -G * r_itsm_vec / (r_itsm_mag**2.5)
    
    # Syntropic Scaffolding Component (The Mold)
    scaffold_force = -syntropy_strength * (r_itsm_mag - r_res) * (r_itsm_vec / (r_itsm_mag + 0.1))
    
    # Vacuum Condensate Spin
    v_spin_dir = np.column_stack([-r_itsm_vec[:,1], r_itsm_vec[:,0]]) / (r_itsm_mag + 0.1)
    spin_drag = 0.8 * (v_spin_dir - data_itsm['vel'])

    data_itsm['vel'] += (acc_newton + scaffold_force + spin_drag) * dt
    data_itsm['pos'] += data_itsm['vel'] * dt

    # Update Visuals
    particles_std.set_offsets(data_std['pos'])
    particles_itsm.set_offsets(data_itsm['pos'])
    
    # Update Overlay
    overlay_std.set_offsets(data_std['pos'])
    overlay_itsm.set_offsets(data_itsm['pos'])
    
    return particles_std, particles_itsm, overlay_std, overlay_itsm

# 5. Execution
ani = animation.FuncAnimation(fig, update, frames=steps, interval=40, blit=True)
plt.tight_layout()
plt.show()
