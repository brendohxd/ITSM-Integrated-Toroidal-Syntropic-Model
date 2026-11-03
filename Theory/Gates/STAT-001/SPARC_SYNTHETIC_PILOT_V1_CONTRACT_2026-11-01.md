# Synthetic conditional sampler pilot v1

Authorized scope: validate a new local MCMC implementation before any real SPARC
inference. The catalogue uncertainties could not be retrieved; no uncertainty
values are supplied to real galaxies by this run. No new action is adopted.

Model: fixed empirical a0=1.2e-10 m/s2, C=1, algebraic simple-nu comparator.
It is not a disk AQUAL solution or an ITSM prediction. Units: r in kpc, template
velocities in km/s. Signed squared template contributions are retained; points
with nonpositive total inward baryonic acceleration give zero parameter support,
not clipped predictions. Distance scales radii by d and squared templates by d.
Predict nominal deprojected catalogue velocity as Vmodel*sin(i)/sin(i0), keeping
the observed velocities/errors fixed. The Gaussian likelihood includes its
normalizer. This avoids a parameter-dependent data-coordinate Jacobian.
Changing inclination does not reconstruct photometry/thickness: this is a
declared simplified comparator, unsuitable for a complete physical disk fit.

Parameters are log10 Udisk, d=D/D0, i in degrees, and log10 Ubulge only where
the simulated bulge exists. Independent Gaussian priors in these coordinates:
log10 Udisk centered log10(.5), log10 Ubulge centered log10(.7), both 0.1 dex;
d centered 1 with sigma .07; i centered i0 with sigma 3 degrees. Support d>0,
0<i<90. The last two uncertainty values are synthetic fixture choices only.
Normalizers of the fixed truncated priors are parameter-independent; no
posterior evidence or prior-normalized cross-model comparison is calculated.

Four synthetic fixtures: with/without bulge crossed with i0=45/70 degrees,
32 radii .5..20 kpc and independent Gaussian 2.5 km/s errors. Truth is at the
prior centers; this favorable fixture does NOT establish general calibration
or prove recovery for real degeneracies. Retain all fixture outcomes.

Run 16 independent ensemble jobs using spawn processes, one BLAS thread each;
64 walkers, 10,000 steps, 2,000 discarded warm-up, deterministic distinct seeds.
Checkpoint every 1,000 steps in exclusive new files, including chain, log density
and random state without pickle. This version saves restart ingredients but
does not yet implement a resume CLI. All original files remain untouched.

Independent formula/control checks precede sampling: scalar versus vectorized
acceleration, physical-support rejection, response to inclination displacement,
and fixed coordinate likelihood Jacobian. No automatic acceptance if any fails.

Diagnostics use walker zero selected in advance from each independently seeded
ensemble, not interacting walkers treated as independent chains. Report rank
normalized/folded split Rhat, estimated autocorrelation ESS and retained length.
Provisional criteria: Rhat<1.01, summed fixed-walker ESS>=400 per parameter,
retained length>=50 times every estimated tau, with finite positive tau.
These are necessary diagnostics, not proof of mixing. Report interval coverage
and acceptance separately, without selecting fixtures or rerunning for success.
This is not broad simulation-based calibration, prior sensitivity, held-out
validation, nested sampling or real-data goodness of fit. Unmet criteria stay
unmet; no full SPARC batch follows automatically from this synthetic check.

DISK/STAT/MAT holds persist. Rule-9 is deferred. No H0/coefficient inference,
publication, commit, push, external provider dispatch or vault mutation.
