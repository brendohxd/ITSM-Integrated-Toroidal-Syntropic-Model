# STAT-001: Statistical Inference Pipeline

## Context & Objectives
This gate clears the path for rigorous evaluation of rotation curves (e.g., SPARC dataset) using the Derived Path variables (where $V_{eff} = C_m/f$ locks the IR coupling).

Historically, the ITSM pipeline suffered from B9 dual RAR packaging (arbitrarily forcing $C_{obs} = 2/3$ and $a_0 = cH_0/2\pi$). 

STAT-001 establishes an honest statistical test comparing:
1. **Geometric Path**: $a_0 = cH_0/2\pi$ and $C_{obs} = V_{eff}$.
2. **Phenomenological Path**: $a_0 = 3700 \text{ (km/s)}^2/\text{kpc}$ and $C_{obs} = V_{eff}$.

## Methodology
- **Data**: SPARC rotation curve `.dat` files.
- **Model**: Algebraic deep-MOND approximation derived from the AQUAL nonlinear field. $V_{bar}^2 = V_{gas}^2 + \Upsilon_{disk} V_{disk}^2 + \Upsilon_{bulge} V_{bulge}^2$.
- **Map**: $V_{obs} = \sqrt{R \cdot g_{obs}}$ where $g_{obs} = |g_N| \nu(|g_N|/a_{0,eff})$.
- **Nuisance Parameters**: $\Upsilon_{disk}$ and $\Upsilon_{bulge}$ fitted per galaxy.
- **Prior**: Strict log-normal priors on mass-to-light ratios ($\log_{10} \Upsilon_{disk} \sim \mathcal{N}(-0.301, 0.1^2)$, $\log_{10} \Upsilon_{bulge} \sim \mathcal{N}(-0.155, 0.1^2)$) as per Lelli et al.
- **Parallelization**: Optimization is parallelized across galaxies using a 16-core pool.

## Pass Criteria
- Code successfully computes total $\chi^2$, BIC, and AIC for both geometric and phenomenological branches without crashing.
- Evaluates the theoretical models rigorously without arbitrary fine-tuning of $C_{obs}$ or $a_0$.
