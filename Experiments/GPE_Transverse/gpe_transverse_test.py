"""
gpe_transverse_test.py
-----------------------
Tests whether energy dissipated by a moving 'baryonic' potential in a 3D
periodic superfluid (T^3 analog) splits into transverse (incompressible/
vortical) vs longitudinal (compressible/phonon) channels, and whether
that fraction approaches 2/3 as ITSM's Cproj derivation would need.

Units: hbar = m = 1. Sound speed c_s = sqrt(g*rho0) = 1. Healing length = 1.

Three modes below:
  1. single_run_detailed()  -- watch E_long/E_trans evolve over time for one run,
                               with explicit vortex-nucleation diagnostic
  2. velocity_scan()        -- sweep v, find where transverse fraction peaks
  3. resolution_check()     -- confirm a result isn't a grid artifact
"""
import numpy as np
import time


def setup_grid(N, L):
    dx = L / N
    x = np.linspace(-L/2, L/2, N, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    k1d = 2*np.pi*np.fft.fftfreq(N, d=dx)
    KX, KY, KZ = np.meshgrid(k1d, k1d, k1d, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K2_safe = K2.copy(); K2_safe[0, 0, 0] = 1e-12
    return dx, X, Y, Z, KX, KY, KZ, K2, K2_safe


def moving_potential(X, Y, Z, L, t, v, V0, sigma):
    x0 = -L/4 + v*t
    dxp = ((X - x0 + L/2) % L) - L/2  # minimum-image distance, respects periodicity
    r2 = dxp**2 + Y**2 + Z**2
    return V0 * np.exp(-r2 / (2*sigma**2))


def helmholtz_energy_split(psi, dx, KX, KY, KZ, K2_safe):
    """Decompose flow kinetic energy into compressible (irrotational/longitudinal)
    and incompressible (solenoidal/transverse) parts via Fourier projection."""
    rho = np.abs(psi)**2
    grad_psi = np.array(np.gradient(psi, dx, dx, dx))
    j = np.imag(np.conj(psi) * grad_psi)          # mass current
    u = j / np.maximum(rho, 1e-6)                  # velocity field

    U_k = [np.fft.fftn(u[i]) for i in range(3)]
    k_arr = [KX, KY, KZ]
    kdotU = sum(k_arr[i]*U_k[i] for i in range(3))
    U_long_k = [kdotU * k_arr[i] / K2_safe for i in range(3)]
    U_trans_k = [U_k[i] - U_long_k[i] for i in range(3)]

    u_long = [np.real(np.fft.ifftn(U_long_k[i])) for i in range(3)]
    u_trans = [np.real(np.fft.ifftn(U_trans_k[i])) for i in range(3)]

    E_long = 0.5 * np.sum(rho * sum(u_long[i]**2 for i in range(3))) * dx**3
    E_trans = 0.5 * np.sum(rho * sum(u_trans[i]**2 for i in range(3))) * dx**3
    return E_long, E_trans


def run_gpe(N=48, L=30.0, v=1.0, V0=3.0, sigma=1.5, g=1.0, rho0=1.0,
            dt=0.01, n_steps=800, verbose=False, report_every=100):
    """Core evolution. If verbose, prints E_long/E_trans/frac as it develops over time."""
    dx, X, Y, Z, KX, KY, KZ, K2, K2_safe = setup_grid(N, L)
    psi = np.sqrt(rho0) * np.ones((N, N, N), dtype=complex)

    history = []
    for step in range(n_steps):
        t = step * dt
        psi_k = np.fft.fftn(psi); psi_k *= np.exp(-1j*K2*dt/4.0); psi = np.fft.ifftn(psi_k)
        V = moving_potential(X, Y, Z, L, t + dt/2, v, V0, sigma)
        psi *= np.exp(-1j*(V + g*np.abs(psi)**2)*dt)
        psi_k = np.fft.fftn(psi); psi_k *= np.exp(-1j*K2*dt/4.0); psi = np.fft.ifftn(psi_k)

        if verbose and (step % report_every == 0 or step == n_steps - 1):
            E_long, E_trans = helmholtz_energy_split(psi, dx, KX, KY, KZ, K2_safe)
            total = E_long + E_trans
            frac = E_trans/total if total > 0 else 0
            history.append((t, E_long, E_trans, frac))
            print(f"  t={t:6.2f}  E_long={E_long:10.4f}  E_trans={E_trans:10.4f}  "
                  f"frac_transverse={frac:.4f}")

    E_long, E_trans = helmholtz_energy_split(psi, dx, KX, KY, KZ, K2_safe)
    total = E_long + E_trans
    frac_trans = E_trans/total if total > 0 else 0
    min_density = np.abs(psi).min()**2
    return E_long, E_trans, frac_trans, min_density, history


def single_run_detailed(v=2.0, sigma=1.5, N=48, n_steps=800):
    """Watch one run develop over time, with explicit vortex-nucleation check."""
    print(f"=== SINGLE RUN: v={v}, sigma={sigma}, N={N} ===")
    E_long, E_trans, frac_trans, min_rho, history = run_gpe(
        N=N, v=v, sigma=sigma, n_steps=n_steps, verbose=True)

    print()
    print("=== VORTEX NUCLEATION DIAGNOSTIC ===")
    print(f"Background density rho0 = 1.0")
    print(f"Minimum density reached anywhere in the box: {min_rho:.6f}")
    print(f"(Density near 0 = vortex core present; density staying near 1.0 = no vortices)")
    print(f"Healing length in these units: 1.000")
    print(f"Object width (sigma) in healing lengths: {sigma}")
    print(f"Object velocity in units of sound speed c_s: {v}")
    print()
    print(f"Final transverse energy fraction: {frac_trans:.4f}")
    print(f"(2/3 = 0.6667 would match the ITSM prediction)")
    return E_long, E_trans, frac_trans, min_rho


def velocity_scan(velocities=(0.3, 0.5, 0.7, 1.0, 1.3, 1.6, 2.0), N=48, n_steps=800):
    print(f"=== VELOCITY SCAN (N={N}) ===")
    print(f"{'v (c_s)':>10} | {'E_long':>10} | {'E_trans':>10} | {'frac_trans':>10} | "
          f"{'min_density':>12} | {'vortices?':>10}")
    print("-" * 80)
    t0 = time.time()
    results = []
    for v in velocities:
        E_long, E_trans, frac_trans, min_rho, _ = run_gpe(N=N, v=v, n_steps=n_steps)
        nucleated = "YES" if min_rho < 0.1 else "no"
        results.append((v, E_long, E_trans, frac_trans, min_rho, nucleated))
        print(f"{v:>10.2f} | {E_long:>10.4f} | {E_trans:>10.4f} | {frac_trans:>10.4f} | "
              f"{min_rho:>12.6f} | {nucleated:>10}")
    print(f"\nScan took {time.time()-t0:.1f}s")
    return results


def resolution_check(v=1.0, resolutions=(48, 64, 96), n_steps=800):
    print(f"=== RESOLUTION CHECK at v={v} ===")
    print(f"{'N':>6} | {'dx (healing lengths)':>20} | {'E_long':>10} | {'E_trans':>10} | {'frac_trans':>10}")
    print("-" * 70)
    for N in resolutions:
        E_long, E_trans, frac_trans, min_rho, _ = run_gpe(N=N, v=v, n_steps=n_steps)
        dx = 30.0 / N
        print(f"{N:>6} | {dx:>20.4f} | {E_long:>10.4f} | {E_trans:>10.4f} | {frac_trans:>10.4f}")


def obstacle_geometry_scan(sigmas=(0.3, 0.5, 0.8, 1.5), v=1.0, N=64, n_steps=1000):
    """PRIORITY NEXT STEP -- untested tonight. Sharper obstacles may shed more
    coherent vortex rings and less diffuse sound than the smooth wide Gaussian
    tested so far. This is the real open question."""
    print(f"=== OBSTACLE GEOMETRY SCAN at v={v}, N={N} ===")
    print(f"{'sigma (healing lengths)':>25} | {'E_long':>10} | {'E_trans':>10} | {'frac_trans':>10}")
    print("-" * 65)
    for sigma in sigmas:
        E_long, E_trans, frac_trans, min_rho, _ = run_gpe(N=N, v=v, sigma=sigma, n_steps=n_steps)
        print(f"{sigma:>25.2f} | {E_long:>10.4f} | {E_trans:>10.4f} | {frac_trans:>10.4f}")


if __name__ == "__main__":
    # Reproduces tonight's Claude-sandbox results exactly
    single_run_detailed(v=2.0, sigma=1.5, N=48, n_steps=800)
    print()
    velocity_scan()
    print()
    resolution_check(v=1.0, resolutions=(48, 64))
    print()
    # The actual next step -- not run tonight, this is what needs real hardware:
    # obstacle_geometry_scan()
