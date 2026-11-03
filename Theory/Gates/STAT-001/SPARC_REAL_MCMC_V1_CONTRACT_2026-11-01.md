# Full SPARC conditional MCMC v1 — frozen execution scope

Operator approval: measured-uncertainty nuisance marginalization for all 175
SPARC galaxies, 16 CPU worker processes; High confirmed for implementation.

This is a **conditional algebraic simple-nu comparator**, with fixed empirical
a0=1.2e-10 m/s2 and C=1. No numerical ITSM prediction, disk AQUAL field solve,
lensing comparison, H0 inference, Bayesian evidence or model preference follows.
All 175 are included, with quality/nominal inclination recorded. No fit-based
cuts. Quality-3 and low-inclination results are exploratory; diagnostic success
does not cure noncircular motions or the simplified geometry.

Use the archived candidate catalogue, checksum-verified against its record,
with the exact source/provenance limits documented in the full input check.
Every radial file, parsed nuisance table and producer/dependency script is
pinned in the fresh run contract. No source data or prior receipts are edited.

Parameters: log10 Udisk, d=D/D0, i in degrees; log10 Ubulge only for nonzero
bulge templates. Independent priors: log10 Udisk Normal(log10(.5),.1 dex),
log10 Ubulge Normal(log10(.7),.1 dex), d Normal(1,e_D/D0) truncated d>0,
i Normal(i0,e_i) truncated 0<i<90. Measured uncertainties are catalogue entries,
not uniform invented errors. Gaussianity and independence remain modelling
assumptions, not catalogue facts. Catalogue distance calibration is inherited.

Likelihood in fixed nominal deprojected velocity coordinates:
predicted V=Vmodel(d,U)*sin(i)/sin(i0), with fixed reported errV and Gaussian
normalizer retained. No hidden error floor. Distance scales radius by d and
squared baryonic templates by d. Signed gas contributions retained. Reject
parameter proposals with nonpositive total inward baryonic squared speed;
never clip or drop radial points. This domain restriction is a limitation of
the inward scalar comparator, not a statement about general vector gravity.
The Gaussian log priors are evaluated in declared sampled coordinates; no
missing lognormal Jacobian is required in log10 U coordinates. Fixed prior
normalizers cancel within each posterior; no evidence integral is calculated.

No photometry/thickness reconstruction under inclination change, gas-template
uncertainty, full radial error covariance or dust-population forward model is
included. Shared galaxy-level D/i draws induce correlated predictions, but do
not supply an unmeasured covariance matrix. Interpret intervals accordingly.

Four independent 64-walker ensembles per galaxy, 10,000 steps initially,
2,000 warm-up. Distinct fixed seeds and prior-dispersed initial states sampled
by rejection on physical support; edge-on i0=90 handled by truncated proposals.
16 Windows spawn workers, one numerical-library thread each. Save incremental
1,000-step blocks, random states and posterior arrays without pickle; resume
requires the same pinned run contract. No prior checkpoint is overwritten.
Check conservative disk allowance plus 3 GiB reserve before launching.

Real pilot membership fixed before sampling: CamB, NGC7814, NGC5907, UGC01281
(disk/bulge, edge-on and prior boundary controls). Run independent scalar
likelihood checks and the synthetic controls before sampling. Retain pilot
diagnostic failures; do not replace members or thresholds to obtain success.
The all-175 batch follows only after reviewing pilot numerical and convergence
diagnostics. Pilot success is not broad calibration or prior sensitivity.

Diagnostics: preselected walker zero from each independent ensemble, rank/folded
split Rhat<1.01, summed autocorrelation ESS>=400 per parameter, each retained
length>=50*tau with finite positive tau. Walkers within one ensemble are not
treated as independent chains. Report all failures, intervals and acceptance;
Rhat/ESS estimates do not prove mixing. The raw chi2 at marginal medians is
not a maximum-likelihood statistic, reduced chi2 or posterior predictive check.

No global p-value, AIC/BIC/evidence, universal scale or cosmological claim is
authorized from this single-model run. Prior sensitivity and broader recovery
tests remain necessary for publication. Rule-9 review is deferred; substantive
MAT/DISK/STAT and action/metric holds remain. No commit, push or publication.
