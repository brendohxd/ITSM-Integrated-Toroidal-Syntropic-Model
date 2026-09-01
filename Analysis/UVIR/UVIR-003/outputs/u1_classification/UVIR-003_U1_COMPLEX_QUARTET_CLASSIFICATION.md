# UVIR-003 U1 controlled complex-quartet classification

**Calculation status:** `PASS_REPRODUCIBLE_CLASSIFICATION_PIPELINE`  
**Physics status:** `HOLD_TIER1_CLOSURE`  
**U1 disposition:** `FREEZE_UNCONTROLLED_LINEAR_RESPONSE_ON_DECLARED_BACKGROUND`

## Result

All five tested on-shell, dimensionless neighboring cases contain an off-axis
complex quartet and amplify retained-matter input. In the baseline case the
quartet occupies t=2.90 to 6.19; the full transfer gain is
1.377081e+27, the retained-matter-input gain is
3.237312e+24, and a source/readout projected onto
Q_rho/Q_chi retains response 1.432637e+19.

The corresponding normalization-specific linearity ceiling is 6.980137e-20.
This is not a physical cosmological amplitude bound. It is evidence that the
declared linear evolution does not control generic normalized sources above
that level without a nonlinear backreaction calculation.

## Classification

The quartet is not classified as controlled Jeans growth: its signed
Hamiltonian-energy/Krein character, calibrated physical timescale, and
nonlinear saturation are missing. It is not classified as a gauge/chart
artifact because the gauge-projected matter response survives and the
time-orbit annihilation residual is small. The high-q real control means the
finite-q quartet alone is not proof of PDE non-hyperbolicity.

The only defensible bounded verdict is
`UNRESOLVED_BACKGROUND_PATHOLOGY_OR_UNCONTROLLED_RESPONSE`. U1 is frozen by
the preregistered uncontrolled-backreaction criterion. This is not a global
no-go theorem for every ITSM action or background.

## Environment caveat

The runtime versions are recorded in the JSON. The live `itsm_env` package
set differs from the dirty `environment.yml` NumPy pin, so the environment is
recorded but not claimed to be an exact lockfile reproduction.
