# R4C1-C3: conditional force-scale transport and H-tracking compatibility

Date: 9 October 2026. Version 1, frozen before execution.
Master Test 3 necessary-condition diagnostic, not a physical a0(z) prediction.
Conditional; physics_pass=false; gate_effect=NONE; Rule9_cleared=false;
review DEFERRED. Canonical force response and microscopic matching remain open.

## Existing results are not repeated or weakened

C1 already proves that A is invisible to the aligned homogeneous/classical
linear branch and cannot be selected by its background/linear data. C2 checks
its physical distinction in a separate conditional periodic contrast problem.
This checkpoint asks a different question: how would C1's separately
conditional instantaneous spherical scale transform into the matter clock,
and what would a constant C_chi require over an evolving B1 background?

Pin the action (81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3),
C1 report (c4af4084ae83f7ed70d63f44700a0ebfc2c394ed7d79cd0061e3efe279b7dc0a),
B1 report/contract/receipt/source/trajectory and the new 22-field background
matching receipt. Do not run any old receipt-writing main or retune B1.

No new force response is supplied. Retain C1's weak-potential, spherical,
frozen-frame, regulator-subleading, compensated local-source and negligible
backreaction/time-response assumptions. No common physical domain with B1,
quasistatic remainder, physical cutoff or healthy weak-field branch is proved.
This is a formal transport implication if that approximation is available,
not an observation or a substitute for the missing coupled calculation.

## Exact constant-local-C bookkeeping and conditional time transport

Use c=hbar=1. Distinguish homogeneous C=exp(beta psi_bar) from the unknown
projection P=C_proj. The matter metric is C^2 g. For a local patch with C
frozen during the comparison, r_m=C r_E, dt_m=C dt_E, M_E=C M_m and
rho_E=C^4 rho_m. Derive rather than assert the instantaneous map of the same
Newtonian component: G_m=C^2 G_E. G_E denotes C1's unspecified G_static,
not bare G or a newly computed coupled G_eff(k,z).

Compare the static action density with its local unit map:
A_m=A/C, b_m=b, K_Q,m=K_Q/C^2, z_m=z_E/C^2 and beta_m=beta.
Check both regulator terms, cubic term and source/flux map. The constant-C
map is not the full conformal action transformation for C(t,x); derivative
terms and adiabatic errors are not discarded from that unknown physical solve.

Conditional C1 scale transport must give

```text
a_dyn,E = beta^3/(12*pi*G_E*A)
a_dyn,m = a_dyn,E/C
a_m = C a_E; dt_m = C dt_E
S = H_E+beta psi_dot; H_m = S/C
C_dyn = a_dyn,m/H_m = beta^3/(12*pi*A*G_E*S)
C_chi = C_dyn/P^2, only if g_psi=P sqrt(g_bar*a0) is established.
```

With the frozen constant A,beta, derive the general necessary condition for
constant C_chi: G_E(t)*S(t)*P(t)^2 must be constant. Keep G_E and P unspecified.
Do not assume P=2/3, bare G, constant measured G or a microscopic A value.
For a separately declared constant-G_E/constant-P control only, show that
the B1 initial action-derived S_dot is strictly negative. Do not extend that
failure of automatic H-tracking to running-G/P branches or all ITSM parents.
Verify invariance under the existing positive psi-chart rescaling and the
regulator-subleading flux ratio under local matter units. Wrong matter-clock,
source/mass or scale transport factors must leave nonzero exact residuals.

## Frozen numerical witness and thresholds

Read, do not regenerate, B1's 801 samples on t_E in [0,4]. Use its unchanged
beta=2/5, K_Q=3 and M_cos^2=11/10. Compute C, a_m, H_m and rho_m^matter.
Take t_ref=4 solely as the benchmark's reference endpoint, not present cosmic
time. Define z_ref=a_m(t_ref)/a_m(t)-1 as a formal scale-factor coordinate.
It is not a fitted observable redshift: a radiation/photon model and distance
likelihood are absent. No BBN/CMB/galaxy data or SI calibration enters.

Under the declared constant-G_E/P control, record only normalized profiles
a_dyn,m(t)/a_dyn,m(t_ref)=C_ref/C and
C_chi(t)/C_chi(t_ref)=S_ref/S; neither fixes A, P or a0 in physical units.
Reject a false constant coefficient profile if its maximum separation from
unity exceeds 1e-4. Check original fields/parameters/source hashes unchanged.

Use five-point centered finite differences on 201,401,801 sample subsets.
Check the matter-clock expansion identity, matter-frame dust continuity,
and both normalized-profile logarithmic derivatives against the B1 action
rates. Finest normalized error <=1e-6 for each; 201-to-801 improvement >=4
unless both <=1e-10. These new transport diagnostics do not alter any earlier
physics threshold or repair the preserved original G3 balance failure.
Monitor positivity/finite values at all samples; no unsampled or global
admissibility theorem follows. Exact replay is read-only and refuses mismatch.

## Integrity and full-goal boundary

Use new versioned source/attempt files, reject overwrite, verify transitive
pins/available sidecars before and after, preserve all inherited G3/N3 failures
and declared sidecar absences. No stop, restart or duplicate of the original
G3N5 worker, action change, manuscript/PDF/vault change, model dispatch,
runtime configuration, commit, push or publication is authorized here.

Full Test-1 constraints/evolution/stability/GR, coupled physical Test-2 response,
independent blinded Test-3 matching and canonical a0(z) remain required.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
