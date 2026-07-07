"""
gpe_transverse_test_gpu.py
-----------------------
GPU-accelerated version using CuPy.
"""
import cupy as cp
import time


def setup_grid(N, L):
    dx = L / N
    x = cp.linspace(-L/2, L/2, N, endpoint=False)
    X, Y, Z = cp.meshgrid(x, x, x, indexing='ij')
    k1d = 2*cp.pi*cp.fft.fftfreq(N, d=dx)
    KX, KY, KZ = cp.meshgrid(k1d, k1d, k1d, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    K2_safe = K2.copy(); K2_safe[0, 0, 0] = 1e-12
    return dx, X, Y, Z, KX, KY, KZ, K2, K2_safe


def moving_potential(X, Y, Z, L, t, v, V0, sigma):
    x0 = -L/4 + v*t
    dxp = ((X - x0 + L/2) % L) - L/2
    r2 = dxp**2 + Y**2 + Z**2
    return V0 * cp.exp(-r2 / (2*sigma**2))


def helmholtz_energy_split(psi, dx, KX, KY, KZ, K2_safe):
    rho = cp.abs(psi)**2
    # cp.gradient exists in modern CuPy, returns list of arrays
    grad_psi = cp.array(cp.gradient(psi, dx, dx, dx))
    j = cp.imag(cp.conj(psi) * grad_psi)
    u = j / cp.maximum(rho, 1e-6)

    U_k = [cp.fft.fftn(u[i]) for i in range(3)]
    k_arr = [KX, KY, KZ]
    kdotU = sum(k_arr[i]*U_k[i] for i in range(3))
    U_long_k = [kdotU * k_arr[i] / K2_safe for i in range(3)]
    U_trans_k = [U_k[i] - U_long_k[i] for i in range(3)]

    u_long = [cp.real(cp.fft.ifftn(U_long_k[i])) for i in range(3)]
    u_trans = [cp.real(cp.fft.ifftn(U_trans_k[i])) for i in range(3)]

    E_long = 0.5 * cp.sum(rho * sum(u_long[i]**2 for i in range(3))) * dx**3
    E_trans = 0.5 * cp.sum(rho * sum(u_trans[i]**2 for i in range(3))) * dx**3
    return float(E_long), float(E_trans)


def run_gpe(N=48, L=30.0, v=1.0, V0=3.0, sigma=1.5, g=1.0, rho0=1.0,
            dt=0.01, n_steps=800, verbose=False, report_every=100):
    dx, X, Y, Z, KX, KY, KZ, K2, K2_safe = setup_grid(N, L)
    psi = cp.sqrt(rho0) * cp.ones((N, N, N), dtype=complex)

    history = []
    for step in range(n_steps):
        t = step * dt
        psi_k = cp.fft.fftn(psi); psi_k *= cp.exp(-1j*K2*dt/4.0); psi = cp.fft.ifftn(psi_k)
        V = moving_potential(X, Y, Z, L, t + dt/2, v, V0, sigma)
        psi *= cp.exp(-1j*(V + g*cp.abs(psi)**2)*dt)
        psi_k = cp.fft.fftn(psi); psi_k *= cp.exp(-1j*K2*dt/4.0); psi = cp.fft.ifftn(psi_k)

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
    min_density = float(cp.abs(psi).min()**2)
    return E_long, E_trans, frac_trans, min_density, history


def single_run_detailed(v=2.0, sigma=1.5, N=48, n_steps=800):
    print(f"=== SINGLE RUN: v={v}, sigma={sigma}, N={N} ===")
    E_long, E_trans, frac_trans, min_rho, history = run_gpe(
        N=N, v=v, sigma=sigma, n_steps=n_steps, verbose=True)

    print()
    print("=== VORTEX NUCLEATION DIAGNOSTIC ===")
    print(f"Background density rho0 = 1.0")
    print(f"Minimum density reached anywhere in the box: {min_rho:.6f}")
    print(f"Final transverse energy fraction: {frac_trans:.4f}")
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
    # Sync GPU before timing
    cp.cuda.Stream.null.synchronize()
    print(f"\nScan took {time.time()-t0:.1f}s")
    return results


def resolution_check(v=1.0, resolutions=(48, 64, 96), n_steps=800):
    print(f"=== RESOLUTION CHECK at v={v} ===")
    print(f"{'N':>6} | {'dx':>10} | {'E_long':>10} | {'E_trans':>10} | {'frac_trans':>10}")
    print("-" * 70)
    for N in resolutions:
        E_long, E_trans, frac_trans, min_rho, _ = run_gpe(N=N, v=v, n_steps=n_steps)
        dx = 30.0 / N
        print(f"{N:>6} | {dx:>10.4f} | {E_long:>10.4f} | {E_trans:>10.4f} | {frac_trans:>10.4f}")


def obstacle_geometry_scan(sigmas=(0.3, 0.5, 0.8, 1.5), v=1.0, N=64, n_steps=1000):
    print(f"=== OBSTACLE GEOMETRY SCAN at v={v}, N={N} ===")
    print(f"{'sigma':>10} | {'E_long':>10} | {'E_trans':>10} | {'frac_trans':>10}")
    print("-" * 65)
    for sigma in sigmas:
        E_long, E_trans, frac_trans, min_rho, _ = run_gpe(N=N, v=v, sigma=sigma, n_steps=n_steps)
        print(f"{sigma:>10.2f} | {E_long:>10.4f} | {E_trans:>10.4f} | {frac_trans:>10.4f}")


if __name__ == "__main__":
    single_run_detailed(v=2.0, sigma=1.5, N=48, n_steps=800)
    print()
    velocity_scan()
    print()
    resolution_check(v=1.0, resolutions=(48, 64))
    print()
    # obstacle_geometry_scan()
