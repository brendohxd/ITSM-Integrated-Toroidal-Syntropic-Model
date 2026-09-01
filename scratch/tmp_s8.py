import camb
from camb import model
import numpy as np

def get_S8(H0, w, omega_m):
    ombh2 = 0.02237
    h = H0 / 100.0
    h2 = h**2
    omch2 = omega_m * h2 - ombh2
    
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=0.06, omk=0)
    pars.set_dark_energy(w=w, wa=0, dark_energy_model='fluid')
    pars.InitPower.set_params(As=2.1e-9, ns=0.9649)
    pars.set_matter_power(redshifts=[0.], kmax=2.0)
    pars.NonLinear = model.NonLinear_none
    results = camb.get_results(pars)
    
    sigma8 = np.array(results.get_sigma8())[0]
    S8 = sigma8 * np.sqrt(omega_m / 0.3)
    return sigma8, S8

s8_255, S8_255 = get_S8(72.50, -1.27, 0.255)
print(f'H0=72.50, w=-1.27, Om=0.255 -> sigma8={s8_255:.4f}, S8={S8_255:.4f}')

s8_277, S8_277 = get_S8(72.91, -1.27, 0.277)
print(f'H0=72.91, w=-1.27, Om=0.277 -> sigma8={s8_277:.4f}, S8={S8_277:.4f}')
