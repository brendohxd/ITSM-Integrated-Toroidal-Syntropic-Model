# Master ITSM test programme

**Date:** 2026-09-24  
**Status:** Active user-directed research order; scientific gates remain fail-closed  
**Applies to:** recovery branch `recovery/v12-core-architecture`  
**Authority:** This programme orders research work. It does not supersede the Core Identity, signed parent-action contracts, gate decisions, or claim statuses.

## 1. Purpose and execution rule

This programme consolidates the major foundational, observational, cosmological,
and high-redshift tests into one ordered portfolio. Observational programmes
that depend on an action-derived prediction do not begin as prediction tests
until their upstream foundations pass. Methods controls may be developed in
parallel when they cannot be mistaken for an ITSM prediction.

Under the operator's 25 September 2026
[Rule-9 deferred-review policy](ITSM_RULE9_DEFERRED_REVIEW_POLICY.md), pending
review alone does not prevent the next bounded research step. Locally checked
inputs may be reused provisionally with their scope and inherited review
dependencies recorded. The physical prerequisites below remain binding;
canonical closure and publication readiness still require review.

The current programme-level priority is Test 1, **Covariant Action and Source
Vector**. Its entry audit finds that the repository's action inventory is still
schematic and the reservoir exchange current has no selected action-level
origin. The owning contract is
`Theory/Gates/ITSM_MASTER_TEST_01_SOURCE_VECTOR_CLOSURE_CONTRACT_2026-09-24.md`.

The previously selected TOP-X4 `X4-S4-C1` curved-slice calculation remains a
separate candidate-specific lane. It is queued while Test 1 owns the active
programme priority. Its route-selection receipt is not a curved-background
solution or an accepted parent.

## 2. Dependency clarifications

The numbered list is the default priority order. The following dependencies
must be honoured when freezing each test contract:

1. Test 1 must identify and freeze a complete off-shell action before source,
   weak-field, stability, or thermodynamic claims can be derived from it.
2. Test 2 first derives the weak-field response with all independent
   coefficients explicit. Its fixed `2/3` version cannot pass until Test 4
   independently derives the projection factor from the same declared route.
3. Test 3 follows the action-level weak-field and projection results. Derive
   the homogeneous `H(z)` and deceleration history from the declared action or
   a separately specified background solution without using observed `a0` to
   select a coefficient. Use `q_dec` for the cosmological deceleration
   parameter to distinguish it from a force-gradient variable.
4. Test 5's action-level physical-mode and stability requirements constrain
   whether the response from Test 2 is admissible. A formal weak-field equation
   is not a pass if its parent has a ghost, gradient instability, ill-posed
   evolution, or no controlled domain.
5. Tests 6 and 7 use the frozen action and its admissible backgrounds. They may
   have bounded subcalculations in parallel, but their required pass/failure
   decisions belong before the full observational programmes.
6. Tests 8--21 use one frozen action, coefficient set, and declared nuisance
   model wherever the observable predictions overlap. No route is retuned
   between galaxies, lensing, clusters, CMB, BBN, gravitational waves, or JWST.

## 3. Foundational gates

| Priority | Test | Required calculation and decision rule |
|---:|---|---|
| 1 | **Covariant action and Source Vector** | Vary one fully specified off-shell action. Derive the matter, plenum, and (where present) reservoir stress tensors and exchange currents. Verify on-shell total conservation, a finite nonsingular transfer current, and the declared uncoupled GR limit. Bianchi consistency alone does not derive constituent currents. Keep matter--plenum exchange, reservoir throughput, and condensate-number source distinct unless the action relates them. |
| 2 | **Weak-field closure** | Derive the metric equations, matter Euler equation, and controlled modified-Poisson limit. Test whether they yield `g_tot = g_bar + C_proj sqrt(g_bar a0)` and list every approximation, boundary condition, and matter coupling. Retain `C_proj` as an unknown until Test 4 supplies it. If no derivation exists, label the force law as a conditional or empirical EFT input. |
| 3 | **Blind acceleration-coefficient audit** | Reconstruct the historical `a0` equations, then derive `C_chi` in `a0=C_chi c H0` without using observed `a0`. Preregister and compare `C_chi=1`, `2 pi`, `1/(2 pi)`, `sqrt(1-q_dec)/(2 pi)`, and the independently derived result. Only afterward compare to SPARC, bTFR, and weak-lensing data. Derive `a0(z)` from the same action/background. |
| 4 | **Projection-factor audit** | Derive the `2/3` factor from `T^3` eigenmodes/projectors or the matter--phonon EFT. Trace every other occurrence of `2/3` and show that unrelated trace, tensor, and fitting factors are not conflated. |
| 5 | **Causality, stability, and mathematical closure** | Derive the quadratic action, constrained kinetic matrix, characteristics, hyperbolicity, ghost and gradient conditions, `c_s^2(k,a)`, and EFT cutoff. Test whether reconstructed `Q(z)` histories are differentiable, invertible, Lipschitz, and uniquely forward-integrable from independent initial conditions. A ghost, nonunique evolution, target insertion, or absence of a nonempty controlled domain is a failure. |
| 6 | **Syntropic thermodynamic stability** | Derive entropy production, heat capacities, and the coupled matter--plenum Hessian. Report all Hessian eigenvalues and transition redshifts. Distinguish generalized-second-law compliance, an acceleration transition, and genuine thermodynamic stability. |
| 7 | **Local and strong-field gravity** | Derive `G_eff(k,z)`, `dot G/G`, gravitational slip, and the complete PPN metric. Test Solar-System, pulsar, BBN, and multimessenger constraints, including Mercury, Cassini, Shapiro delay, light bending, redshift, S2 precession, and GW170817. Verify each numerical bound against its primary source when the owning contract is frozen. |

## 4. Core dark-matter and lensing tests

These are downstream of the foundational gates. Limited methods development may
continue, but results remain controls until the same action supplies the
prediction.

| Priority | Test | Required run and pass condition |
|---:|---|---|
| 8 | **Complete SPARC reanalysis** | Refit all 175 galaxies using the fixed, blindly derived `C_chi`. Marginalize distance, inclination, gas, stellar `M/L`, thickness, and within-galaxy covariance. Use galaxy-level nested cross-validation. Compare ITSM with Newtonian baryons, MOND/AQUAL/QUMOND, `C=1`, `C=2/3`, NFW, and flexible halos using held-out likelihood and Bayesian evidence. |
| 9 | **SPARC secondary observables** | Test `X=V/R` versus `Y=d ln I/d ln R`, gas-fraction residuals, acceleration regimes, RAR, and bTFR. Report residual-correlation significance separately from rejection of universal `a0`. |
| 10 | **Cross-scale galaxy test** | Require one fixed shear law and `a0` across SPARC, M31 (`2--167 kpc`), four KiDS stacked weak-lensing profiles, and DESI--ACT--HSC gas/lensing ratios. Forward-model M31 anisotropy, tidal rejection, and nonequilibrium terms. No scale-dependent retuning. |
| 11 | **Diffuse and almost-dark galaxies** | Fit complete two-dimensional velocity and dispersion fields for UDG-1 and LSB-6. Preregister `sigma_los(R)`, enclosed mass, and lensing for TTT J1237327+143535 before spectroscopy. Simulate cuspy and cored satellite progenitors through identical tidal histories. |
| 12 | **Strong-lensing consistency** | Derive null geodesics and jointly fit lensing and dynamics for SDSS J0946+1006, JVAS B1938+666, and TDCOSMO systems. Marginalize mass sheets, `kappa_ext`, Jeans anisotropy, and mass-map shape degeneracy. Test LEN-001's `M_lens/M_dyn=1` prediction. |
| 13 | **Merging-cluster suite** | Use one plenum-field solution for convergence peaks, gas, galaxies, X-ray temperature, shock Mach surfaces, radio emission, and merger timing for the Bullet Cluster, A520, and El Gordo. Include El Gordo's `d_DM>740 kpc` criterion as a source-specific comparator, not a universal ITSM threshold. Preregister new-merger lensing peaks before maps are released. |
| 14 | **Cluster-population validation** | Predict CHEX-MATE discontinuities, shocks, cold fronts, radio associations, halo profiles through `5 r_500c`, and Euclid lensing-selected counts after documented detection algorithms. Compare with direct ITSM `N`-body simulations, not only idealized fields. |

## 5. Expansion, Hubble tension, and structure

| Priority | Test | Required run and pass condition |
|---:|---|---|
| 15 | **Full interacting-cosmology likelihood** | Implement the ITSM background and scalar perturbations in CLASS or equivalent. Evolve baryons, matter, and plenum density/velocity perturbations separately. Fit `Q^mu`, `n`, `w_p(z)`, neutrino mass, curvature, and sound speed to CMB, DESI, supernova, RSD, and lensing data, including nested `Q^mu=0`. |
| 16 | **Interaction-mechanism discriminators** | Calculate `delta_eff=Q/(H rho_m)`, `beta_ITSM(k,z)`, drag, effective-mass evolution, and equivalence-principle violation. Compare against matched-`(theta_s,z_eq)` LambdaCDM, matched-background `w`CDM, CPL, and other interacting models. Separate distinctive ITSM effects from shifted calibration parameters. |
| 17 | **DESI expansion and growth tests** | Predict `w_eff(z)`, crossing redshift, tomographic `Omega_m^fit(z)`, `f sigma_8`, Weyl potentials, CMB lensing, and `P(k)`. Include SPT-3G, ACT, Planck lensing, DESI bispectrum/relative-mode nuisance operators, and the four-point function. Report posterior displacement, `Delta chi^2`, AIC/BIC, and Bayesian evidence separately. |
| 18 | **Pre-recombination and BBN gate** | Couple the action-derived plenum sector to a BBN network. Predict D/H, `Y_p`, `Delta N_eff`, `G_eff`, `r_s`, `r_d`, CMB TT/TE/EE, anisotropic stress, and Ly-alpha-scale transfer. Marginalize nuclear rates, neutron lifetime, and empirical LBT helium; use joint likelihoods only when upstream histories and units are physically supplied. |
| 19 | **Complete Hubble-tension test** | One parameter set must reproduce `r_s`, `D_A(z*)`, `D_M/r_d`, `D_H/r_d`, `M_B`, `H(z)`, `H0`, `S8`, and growth. Compare early-only, late-only, and complete ITSM with LambdaCDM, CPL, axion EDE, Hot-NEDE/DRMD, dark QCD, and multi-axion ladder models using common priors and nested-sampling evidence. |
| 20 | **Independent H0 coefficient branches** | Keep Cepheid, TRGB, spectroscopic JAGB, megamaser, time-delay lens, bright-siren, and dark-siren posteriors separate. Recompute peculiar velocities and lens potentials under ITSM. Marginalize host weighting, incompleteness, mass--redshift correlations, and GW-population parameters. Propagate full non-Gaussian posteriors into `a0=C_chi c H0`. |
| 21 | **Geometry, topology, and rest frame** | Derive `D_M(z)`, `D_H(z)`, distance sums, and radial--transverse BAO consistency on the actual ITSM manifold. Separate physical topology from calibration `epsilon` and FLRW `Omega_K`. Derive directional redshift perturbations and test DESI tracers against the standard CMB kinematic dipole. |

## 6. High-redshift and multimessenger extensions

These extensions are indispensable when the relevant ITSM mechanism makes a
prediction:

- **JWST pipeline:** Generate selection-matched ITSM light cones for EPOCHS-DR2
  and JADES. Predict counts, UV luminosity and stellar-mass functions, star
  formation, sizes, UV slopes, clustering bias, and field variance. Separate
  spectroscopic objects from photometric candidates.
- **Sharp-daybreak test:** Preregister the first-luminous-halo redshift and
  minimum mass. Secure galaxies beyond `z=15`, or old populations near
  `z~14`, falsify a variant that predicts a sharp onset near `z=15`.
- **Early-structure controls:** Compare with bursty LambdaCDM/Shark, axion EDE,
  transient negative-sound-speed growth, PBH Poisson seeding, wave dark matter,
  and both SIDM little-red-dot mechanisms. A JWST abundance fit alone is not
  distinctive evidence.
- **Black-hole predictions:** Predict little-red-dot duty cycle, X-ray/IR
  ratio, V-shaped SED incidence, black-hole/stellar-mass ratio, nuclear
  inflow, halo concentration, and LISA merger distribution. Identify a
  correlated observable unavailable to competitors.
- **GW propagation:** Derive tensor, vector, and scalar equations and
  calculate `c_GW`, dispersion, damping, photon--GW delay, `alpha_M(z)`, and
  `D_L^GW/D_L^EM`. Apply propagation and standard-siren likelihoods separately.
- **Stochastic/PTA backgrounds:** Predict `Omega_GW(f)`, polarization, and
  spectral width across PTA and LVK bands. Apply official LVK stochastic
  limits and the O1--O4a scalar-induced-background likelihood. VOR-001 must
  independently reproduce the proposed `1.45--1.88 nHz` `T^3` modes.
- **Particle-dark-matter falsifier:** State whether plenum--nucleus scattering
  is predicted. If so, derive recoil, target-mass scaling, solar capture, and
  neutrino signals. If not, preregister a statistically secure repeatable
  multi-target recoil spectrum as a falsifier of the pure replacement model.

## 7. Dedicated topology and Casimir gates

- **CBR-001:** Renormalized rectangular-`T^3` Casimir stress scan; verify the
  isotropic `r_0=1` limit, `epsilon=0`, Hamiltonian and continuity residuals,
  and analytic small-anisotropy benchmarks.
- **CBR-002 / Stage 3B:** Derive
  `Pi_req=(H^2/kappa)[dx/dN+x(3+d ln H/dN)]` from the declared equations.
- **Density-topology test:** Generate ITSM density fields and blindly compare
  the genus statistic `g(nu; M,z,R_smooth)` with frozen smoothing and selection.

## 8. Rules for every test

1. Freeze predictions and exclusions before examining target data where
   possible.
2. Use identical datasets, priors, nuisance models, and selection functions
   for ITSM and competitors.
3. Report held-out likelihoods and posterior-predictive checks, not training
   fit `chi^2` alone.
4. Report `Delta chi^2`, AIC, BIC, and Bayesian evidence together. Do not call
   a multi-sigma displacement model preference without prior-volume evidence.
5. Do not retune plenum parameters between rotation curves, lensing, clusters,
   CMB, and JWST.
6. Maintain a falsification table naming the outcome that rejects each ITSM
   variant.
7. Verify numerical bounds, dataset releases, and likelihood versions from
   primary sources when the individual gate contract is frozen.
8. Keep method controls, conditional fits, and action-derived predictions
   explicitly separate. A script `PASS`, hash match, or reviewer agreement is
   not by itself a physics pass.

## 9. Current programme boundary

This programme changes the priority order only. It does not change the live
scientific statuses: `UVIR-003=IN_PROGRESS`, `MAT-001=BLOCKED`,
`K_Q=NOT_DERIVED`, `V=NOT_COMPUTED`, `Stage4A=CLOSED`, and
`physics_pass=false`. Test 1 is held at action completion before variation.
TOP-X4 `X4-S4-C1` remains a separate queued lane; if resumed, its next gate is
`TOPX4_H1_X4-S4_CURVED_SLICE_BACKGROUND_OUTPUT_TEST`.
