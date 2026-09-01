"""
gpe_transverse_test_cpu.py
-----------------------
Multicore CPU-accelerated version using scipy.fft (workers=-1).
Tests whether energy dissipated by a moving 'baryonic' potential in a 3D
periodic superfluid (T^3 analog) splits into transverse (incompressible/
vortical) vs longitudinal (compressible/phonon) channels.
"""
import numpy as np
import scipy.fft as fft
import time

def run_gpe(N=48, L=30.0, v=1.0, V0=3.0, sigma=1.5, g=1.0, rho0=1.0,
            dt=0.01, n_steps=800):
    dx = L / N
    x = np.linspace(-L/2, L/2, N, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    k1d = 2*np.pi*np.fft.fftfreq(N, d=dx)
    KX, KY, KZ = np.meshgrid(k1d, k1d, k1d, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K2_safe = K2.copy(); K2_safe[0,0,0] = 1e-12

    psi = np.sqrt(rho0) * np.ones((N, N, N), dtype=complex)

    def moving_potential(t):
        x0 = -L/4 + v*t
        dxp = ((X - x0 + L/2) % L) - L/2  # minimum-image, respects periodicity
        r2 = dxp**2 + Y**2 + Z**2
        return V0 * np.exp(-r2 / (2*sigma**2))

    def energy_split(psi):
        rho = np.abs(psi)**2
        grad_psi = np.array(np.gradient(psi, dx, dx, dx))
        j = np.imag(np.conj(psi) * grad_psi)
        u = j / np.maximum(rho, 1e-6)
        U_k = [fft.fftn(u[i], workers=-1) for i in range(3)]
        k_arr = [KX, KY, KZ]
        kdotU = sum(k_arr[i]*U_k[i] for i in range(3))
        U_long_k = [kdotU * k_arr[i] / K2_safe for i in range(3)]
        U_trans_k = [U_k[i] - U_long_k[i] for i in range(3)]
        u_long = [np.real(fft.ifftn(U_long_k[i], workers=-1)) for i in range(3)]
        u_trans = [np.real(fft.ifftn(U_trans_k[i], workers=-1)) for i in range(3)]
        E_long = 0.5*np.sum(rho*sum(u_long[i]**2 for i in range(3)))*dx**3
        E_trans = 0.5*np.sum(rho*sum(u_trans[i]**2 for i in range(3)))*dx**3
        return E_long, E_trans

    for step in range(n_steps):
        t = step * dt
        psi_k = fft.fftn(psi, workers=-1); psi_k *= np.exp(-1j*K2*dt/4.0); psi = fft.ifftn(psi_k, workers=-1)
        V = moving_potential(t + dt/2)
        psi *= np.exp(-1j*(V + g*np.abs(psi)**2)*dt)
        psi_k = fft.fftn(psi, workers=-1); psi_k *= np.exp(-1j*K2*dt/4.0); psi = fft.ifftn(psi_k, workers=-1)

    E_long, E_trans = energy_split(psi)
    total = E_long + E_trans
    frac_trans = E_trans/total if total > 0 else 0
    min_density = np.abs(psi).min()**2
    return E_long, E_trans, frac_trans, min_density

def obstacle_geometry_scan(sigmas=(0.3, 0.5, 0.7, 0.9, 1.2, 1.5, 2.0), v=1.0, N=64, n_steps=1000):
    """
    Scans the obstacle width (sigma) in units of the healing length.
    Goal: Identify if there is a 'sweet spot' in object geometry that 
    forces the transverse energy fraction closer to 0.666 (2/3).
    """
    print(f"=== OBSTACLE GEOMETRY SCAN at v={v}, N={N} ===")
    print(f"{'sigma (healing lengths)':>25} | {'E_long':>10} | {'E_trans':>10} | {'frac_trans':>10} | {'min_density':>12}")
    print("-" * 80)
    for sigma in sigmas:
        E_long, E_trans, frac_trans, min_rho = run_gpe(N=N, v=v, sigma=sigma, n_steps=n_steps)
        print(f"{sigma:>25.2f} | {E_long:>10.4f} | {E_trans:>10.4f} | {frac_trans:>10.4f} | {min_rho:>12.6f}")

if __name__ == "__main__":
    t0 = time.time()
    obstacle_geometry_scan()
    print(f"\nTotal execution time: {time.time()-t0:.1f}s")
