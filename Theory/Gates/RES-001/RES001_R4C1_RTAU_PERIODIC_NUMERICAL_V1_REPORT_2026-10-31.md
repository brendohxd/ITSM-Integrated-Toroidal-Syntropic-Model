# R-tau coupled periodic candidate: numerical solve, continuum certificate open

31 October 2026. Conditional research; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau remains unadopted.

## Outcome

A nontrivial finite-amplitude periodic numerical candidate now satisfies the
full projected shift equations and both inherited global charge targets.
The independent integrated momentum residuals are small and all sampled
densities are positive. The same frozen candidate passes denser shifted-grid
controls without refitting. This is progress beyond the local principal
symbol; it is NOT yet an admitted continuum nonlinear preparation.

The [owning periodic-preparation contract](RES001_R4C1_RTAU_PERIODIC_PREPARATION_V1_CONTRACT_2026-10-31.md)
still requires explicit continuum tail and nonlinear inverse/domain bounds.
Neither is supplied by the finite-grid evidence here. No certificate of
finite-time nonlinear evolution, full canonical interactions or physical
window follows from this candidate.

## Frozen data and actual coupled equations

The [numerical specification](RES001_R4C1_RTAU_PERIODIC_NUMERICAL_V1_SPEC_2026-10-31.md)
freezes epsilon=1/1000, period 2*pi and nonconstant metric, all three frame
components, condensate, reservoir and force profiles BEFORE the solve.
Exact profile derivatives, the nonlinear Z reduction and positive clock
lapse are retained. Frame velocities include the actual metric drift.
The transverse frame profile never vanishes on the real initial circle;
no independent frame mode is deleted to enforce alignment.

The two free continuation parameters are the mean expansion H and the
condensate velocity omega. Their normalized global charge targets, inherited
from old B1, are I_clock=1/5 and Q_U1=1. They are NOT observational fits,
new microscopic predictions or changes to the action coefficients.

For every spatial point the full physical candidate density is differentiated
BEFORE clock/lapse substitution. Independent local shift values/derivatives,
lapse value/derivative and condensate velocities give

    E_S=L_S-d_z(L_Sz),
    E_N,nonmatter=L_N-d_z(L_Nz),
    rho=E_N,nonmatter/sqrt(h),
    I_clock=average(E_N,nonmatter/C),
    Q_U1=average(u*pi_v-v*pi_u).

Dust epsilon is set to zero only when extracting the nonmatter lapse row;
the physical density is subsequently reconstructed from that row. The full
force, regulator, metric and frame terms are present. The changed local
clock exchange is not replaced by bare-dust continuity.

All three shifts use mean-zero coordinate gauge. Every nonconstant real
Fourier mode available on each odd grid is retained; the solver does not
project the result back onto the three input harmonics. Mean-shift gauge
and integrated momentum equations are distinct: the latter are evaluated
and recorded independently. Reflection parity of the trial data is a
diagnostic initial-data choice, not a projected time-evolution prescription.

## Numerical result and resolution controls

Full local derivatives use 40-digit action differentiation. Fourier assembly
and the frozen aligned inverse used as a chord-iteration preconditioner use
double precision. The preconditioner is not asserted to be the validated
inverse of the actual nonlinear operator.

| Grid | Projected/charge residual after four evaluations | Minimum sampled rho |
|---|---|---|
| 9 | 1.241e-13 | 0.19372081297 |
| 17 | 1.218e-13 | 0.19372078417 |
| 33 | 1.220e-13 | 0.19372078417 |

For the frozen 33-point candidate,

    H=0.8665251363152258,
    omega=0.9999999097130079.

The stored receipt includes every shift coefficient and residual history.
The largest sampled physical tilt is about 4.732e-5, inside the separately
proved local principal-symbol ball. This is not a proof that every nearby
physical mode or nonlinear trajectory stays in that domain.

The [off-grid specification](RES001_R4C1_RTAU_PERIODIC_OFFGRID_V1_SPEC_2026-10-31.md)
fixes that candidate without refitting and evaluates it on 65 and 129 nodes
shifted by 0.37 grid intervals:

| Off-grid nodes | Full sampled shift residual | Minimum sampled rho |
|---|---|---|
| 65 | 8.260e-13 | 0.19373573663 |
| 129 | 3.137e-12 | 0.19372458187 |

Both grids give I_clock=0.20000000000000037 and Q_U1 within 4.5e-14 of one.
Integrated momentum residuals are below 6.3e-16. Maximum sampled density
is below 0.204571. These are sampled properties, not rigorous extrema.

Omitting the lapse Euler flux changes the clock charge to about
0.2000000009649213. The explicit rejection control detects this difference;
correct charge matching is not obtained by dropping the flux.

Fine-grid residual Fourier coefficients beyond the candidate's harmonic 16
reach about 1.45e-13 and 5.49e-13 respectively. The increased fine-grid
residuals must NOT be called monotonic convergence or an infinite-tail bound.
Double-precision differentiation is a possible numerical contributor; this
turn does not establish the source of that increase. It supplies no interval
rounding certificate, continuum residual norm or rigorous nonlinear inverse.

## Verification and preserved scientific holds

[Primary executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_periodic_numerical_v1.py),
[primary receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_periodic_numerical_v1_attempt_01/summary.json):
10/10, no failed/unknown checks; SHA256
58fc8db6b8d10ee57f2974e0415685ded3cfe9e80745044b19b551b7827c0d60.

[Off-grid executable](../../../Analysis/MasterTests/audit_01_r4c1_rtau_periodic_offgrid_v1.py),
[off-grid receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_periodic_offgrid_v1_attempt_01/summary.json):
12/12, no failed/unknown checks; SHA256
9ce854b879a05de463596f9a45a0d75bc2897cbc1253adca11e06caf9f5d1bad.

Both complete read-only recomputing replays are byte-identical. Pinned
sources/sidecars retain bytes and modification times. The off-grid control
changes discretization, not the underlying physical-density implementation;
it is not an independent external scientific reviewer.

Next perform the owning contract's actual continuum residual/tail and
nonlinear inverse/domain certification, using this frozen candidate. More
finite-grid agreement alone will not finish that requirement. Preserve the
observed nonmonotonic residuals. Global charge and momentum compatibility
must remain in the certificate, with positive density and actual force-cusp
regularity. If a quantitative bound fails, retain the obstruction and this
candidate without relabeling it as admitted.

Reduced physical interactions, finite-time nonlinear domain, physical window,
realistic matter, GR/local compatibility and identifying matching remain
INCOMPLETE. Original G1-G6 incomplete; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED. No canonical adoption, manuscript/site change, publication,
commit/push, provider dispatch or vault mutation. Goal ACTIVE; High last confirmed.
