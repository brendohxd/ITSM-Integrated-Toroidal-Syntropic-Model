
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ---------------------------------------------------------
# ITSM Vector 4: Bullet Cluster Separation (Sim 2)
# Deconstructing the "Collisionless" Dark Matter Narrative
# ---------------------------------------------------------

# 1. Simulation Parameters
n_particles = 800
dt = 0.1
steps = 250

# Define Cluster Nodes (The Dense Hulls)
# [x, y, vx, vy]
cluster_l = np.array([-30.0, 0.0, 6.0, 0.0])
cluster_r = np.array([30.0, 0.0, -6.0, 0.0])

# Initialize Gas Clouds (The Diffuse Fog)
gas_l = np.random.normal([-30, 0], 6, (n_particles // 2, 2))
gas_r = np.random.normal([30, 0], 6, (n_particles // 2, 2))
v_gas_l = np.ones_like(gas_l) * [6, 0]
v_gas_r = np.ones_like(gas_r) * [-6, 0]

# 2. Setup Visualization
plt.style.use('dark_background')
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), facecolor='black')

for ax in [ax1, ax2, ax3]:
    ax.set_xlim(-50, 50)
    ax.set_ylim(-30, 30)
    ax.set_aspect('equal')
    ax.axis('off')

# Plot Holders
pink_gas = ax1.scatter([], [], color='hotpink', s=2, alpha=0.4)
cyan_wake = ax2.scatter([], [], color='cyan', s=15, marker='+', alpha=0.3)
galaxy_nodes = ax2.scatter([], [], color='white', s=80, marker='*')

# Overlap Panel
overlap_gas = ax3.scatter([], [], color='hotpink', s=1.5, alpha=0.2)
overlap_wake = ax3.scatter([], [], color='cyan', s=8, marker='+', alpha=0.3)
overlap_nodes = ax3.scatter([], [], color='white', s=50, marker='*')

# Titles
ax1.set_title("Stalled Baryonic Gas\n(X-ray Friction)", color='hotpink', fontsize=12)
ax2.set_title("Metric Acoustic Wake\n(Gravitational Lensing)", color='cyan', fontsize=12)
ax3.set_title("Decoupling Event\n(ITSM Kinetic Separation)", color='white', fontsize=12)

# 3. Physics Engine
def update(frame):
    global cluster_l, cluster_r, gas_l, gas_r, v_gas_l, v_gas_r

    # A. Galaxies (Hulls) punch through unimpeded
    cluster_l[:2] += cluster_l[2:] * dt
    cluster_r[:2] += cluster_r[2:] * dt

    # B. Gas (Fog) stalls in the center (Impact Zone)
    gas_l += v_gas_l * dt
    gas_r += v_gas_r * dt
    
    # Simulate friction/deceleration at the collision interface
    v_gas_l[gas_l[:, 0] > -5] *= 0.85
    v_gas_r[gas_r[:, 0] < 5] *= 0.85

    # C. Acoustic Wake Logic (Lensing)
    # The lensing follows the GALAXY nodes because they maintain velocity
    # We generate a "wake" trailing the stars
    wake_l = cluster_l[:2] - (cluster_l[2:] * np.random.uniform(0, 1.5, (100, 1)))
    wake_r = cluster_r[:2] - (cluster_r[2:] * np.random.uniform(0, 1.5, (100, 1)))
    all_wakes = np.vstack([wake_l, wake_r])

    # Refresh Visuals
    pink_gas.set_offsets(np.vstack([gas_l, gas_r]))
    cyan_wake.set_offsets(all_wakes)
    galaxy_nodes.set_offsets(np.vstack([cluster_l[:2], cluster_r[:2]]))
    
    # Update Overlay
    overlap_gas.set_offsets(np.vstack([gas_l, gas_r]))
    overlap_wake.set_offsets(all_wakes)
    overlap_nodes.set_offsets(np.vstack([cluster_l[:2], cluster_r[:2]]))
    
    return pink_gas, cyan_wake, galaxy_nodes, overlap_gas, overlap_wake, overlap_nodes

# 4. Execution
ani = animation.FuncAnimation(fig, update, frames=steps, interval=30, blit=True)
plt.tight_layout()
plt.show()
