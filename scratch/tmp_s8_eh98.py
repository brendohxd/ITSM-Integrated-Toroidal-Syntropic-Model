import numpy as np
from scipy.integrate import quad

def eh98_transfer(k, omega_m, h, omega_b=0.048, Tcmb=2.725):
    # EH98 Without BAO wiggles
    theta2p7 = Tcmb / 2.7
    om_h2 = omega_m * h**2
    om_b_h2 = omega_b * h**2
    
    zeq = 2.50e4 * om_h2 * theta2p7**-4
    keq = 7.46e-2 * om_h2 * theta2p7**-2
    
    b1 = 0.313 * om_h2**-0.419 * (1 + 0.607 * om_h2**0.674)
    b2 = 0.238 * om_h2**0.223
    zd_prime = 1291 * om_h2**0.251 / (1 + 0.659 * om_h2**0.828)
    zd = zd_prime * (1 + b1 * om_b_h2**b2)
    
    R_eq = 31.5 * om_b_h2 * theta2p7**-4 * (1000 / zeq)
    Rd = 31.5 * om_b_h2 * theta2p7**-4 * (1000 / zd)
    
    s = 44.5 * np.log(9.83 / om_h2) / np.sqrt(1 + 10 * om_b_h2**0.75)
    
    q = k / (13.41 * keq)
    a1 = (46.9 * om_h2)**0.670 * (1 + (32.1 * om_h2)**-0.532)
    a2 = (12.0 * om_h2)**0.424 * (1 + (45.0 * om_h2)**-0.582)
    alpha_c = a1**(-omega_b/omega_m) * a2**(-(omega_b/omega_m)**3)
    
    b1 = 0.944 / (1 + (14.1 * om_h2)**-0.708)
    b2 = 0.395 * om_h2**-0.0266
    beta_c = 1 / (1 + b1 * ((omega_m - omega_b)/omega_m)**b2)
    
    f = 1 / (1 + (k * s / 5.4)**4)
    
    C = 14.2 / alpha_c + 386 / (1 + 69.9 * q**1.08)
    T0 = np.log(np.e + 1.8 * beta_c * q) / (np.log(np.e + 1.8 * beta_c * q) + C * q**2)
    
    return T0

def get_sigma8_approx(omega_m, h, A_s=2.1e-9, ns=0.9649):
    # W(k R) window function
    def W(x):
        return 3 * (np.sin(x) - x * np.cos(x)) / x**3
    
    R = 8.0 # Mpc/h
    
    # Delta^2(k) = A_s (k/k0)^(n_s-1) T(k)^2 (k/(H0/c))^4 ...
    # We will just calculate the ratio of sigma8 between two cosmologies
    def integrand(k, om, h_val):
        # k in h/Mpc
        T = eh98_transfer(k * h_val, om, h_val)
        # Power spectrum P(k) ~ k^ns * T^2
        # Delta^2 ~ k^3 P(k)
        # We compute relative variance
        return k**(ns + 2) * T**2 * W(k * R)**2
    
    return quad(integrand, 1e-4, 1e2, args=(omega_m, h))[0]

# Reference (Planck LCDM)
var_ref = get_sigma8_approx(0.315, 0.6736)
sigma8_ref = 0.811 # standard approx

# For Om=0.255
var_255 = get_sigma8_approx(0.255, 0.725)
sigma8_255 = sigma8_ref * np.sqrt(var_255 / var_ref)

# For Om=0.277
var_277 = get_sigma8_approx(0.277, 0.7291)
sigma8_277 = sigma8_ref * np.sqrt(var_277 / var_ref)

print(f"Om=0.255, h=0.725: sigma8_rel = {sigma8_255:.4f}, S8 = {sigma8_255 * np.sqrt(0.255/0.3):.4f}")
print(f"Om=0.277, h=0.7291: sigma8_rel = {sigma8_277:.4f}, S8 = {sigma8_277 * np.sqrt(0.277/0.3):.4f}")
