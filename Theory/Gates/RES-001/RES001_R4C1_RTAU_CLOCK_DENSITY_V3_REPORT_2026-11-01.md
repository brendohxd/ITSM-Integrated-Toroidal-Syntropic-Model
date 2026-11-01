# R-tau higher initial jets and direct local clock-density check

1 November 2026. Conditional comparison result; review DEFERRED.
physics_pass=false; gate_effect=NONE. R-tau is unadopted; original R4C1
and its canonical G1-G6 status remain unchanged.

## Result and decisive distinction

The reconstructed local lapse density has now been differentiated explicitly
and compared with the action-derived clock current at the three registered
numerical-centre points. The full residual is below 6.053e-13. Omitting the
regulator flux gives errors up to 4.171e-5; omitting the lapse-density
improvement gives errors up to 3.261e-4. The source terms matter.

This is NOT a precise continuum local-clock certificate. The independent
whole-root interval residual is approximately [-572.459,555.703]. It
contains zero but loses too much cancellation to decide exact closure.
No actual residual of that magnitude, physical failure or healthy evolution
is inferred from this wide enclosure. The centre tests and the continuum
bound have different scopes and are recorded separately.

Additional continuum initial bounds have been established without assuming
a finite Fourier tail: the third shift derivative and the spatial derivative
of the particular nonauxiliary acceleration are finite on every certified root.
These support subsequent local/operator work, not a finite-time theorem.

Owner: [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md).
Immediate inputs: [explicit clock current](RES001_R4C1_RTAU_CLOCK_FLUX_V1_REPORT_2026-11-01.md),
[initial construction](RES001_R4C1_RTAU_INITIAL_ACCELERATION_V1_REPORT_2026-11-01.md),
and [mixed operator](RES001_R4C1_RTAU_MIXED_OPERATOR_V4_REPORT_2026-11-01.md).
The [higher-jet/local-density contract](RES001_R4C1_RTAU_CLOCK_DENSITY_V1_CONTRACT_2026-11-01.md)
was frozen before execution. No action coefficient, ensemble or matching
input changes; no target acceleration is used.

## Obtain the root's third derivative from its equation

The existing certificate controls S,S_z,S_zz in a C2 ball. It does NOT
control the difference of third derivatives from the finite Fourier centre.
The new calculation does not differentiate that error radius as if it did.

The full momentum equation is a nonsingular second-order ODE for the
initial shift on the positive force-rest-norm patch. Its principal matrix
comes from the previously derived arbitrary-tilt action coefficient, scaled
by the positive initial metric/lapse factor a^3/N. The fixed profiles and
positive rest norm make its lower coefficients smooth. Its C2 root therefore
bootstraps to the differentiability needed here through that ODE.

For E_S=L_S-partial_z(L_Sz), differentiating once gives

    partial_z E_S = f-K*S_zzz,
    K=L_Sz,Sz,
    f=partial_z E_S evaluated with the UNKNOWN S_zzz jet set to zero.

The zero value is an affine-coefficient extraction device, not a projected
physical state. For the exact root E_S=0, S_zzz=K^-1*f. Taylor coefficients
use the correct factorials: the second coefficient of S is S_zz/2, while
the second coefficient of S_z is S_zzz/2. All existing C2 errors remain.

The all-root, whole-circle inverse bound implies

    ||S_zzz||_2 < 0.155352.

This bounds the actual root, rather than assuming the centre's third
Fourier derivative is exact. At each centre point, retaining and removing
the highest jet reproduces the affine extraction identity within the frozen
1e-35 control. No modes or forced Fourier tails have been deleted.

## Acceleration derivative and actual auxiliary first tangent

For the particular Euler inverse M13*a0=R13,

    a0_z=M13^-1*(R13_z-M13_z*a0).

The new higher spatial jets carry the certified S_zzz bound into R_z.
Combining the preceding temporal inverse and actual coefficient derivatives
gives the coarse whole-circle bound

    ||a0_z||_2 < 13.927.

The actual auxiliary first tangent Zdot=-partial_t(Delta_h psi) is retained
before evaluating the local density time derivative. It could be ignored
in the earlier momentum derivatives, which were proven independent of it;
it cannot be ignored in the time derivative of the complete action density.
No Zddot is assumed: the needed temporal coefficients multiplying that
unused auxiliary acceleration are exactly zero. Quantitative Zddot control
remains open for later uses that genuinely require it.

## The LOCAL lapse density includes a spatial improvement

Let Lbar be the clock-substituted nonmatter density, pi=Lbar_v,
Rvel=v-Lie_S(q), and let the raw N/Nz derivatives be taken BEFORE substituting
N=exp(-beta psi), Nz=-beta*N*psi_z. Define

    Ihat=Lbar-pi.Rvel,
    B_N=N*L_Nz,
    I_density=N*E_N,nonmatter=Ihat-partial_z B_N.

Ihat and I_density have the same periodic integral but are not the same
local density. The test computes

    I_density,t = Ihat_t-partial_z(B_N,t),
    residual = I_density,t
      -partial_z(I_density*S^z+N*sqrt(h)*F^z).

The independent raw lapse-gradient Hessian supplies B_N,t and its spatial
derivative. Terms from the clock pullback and every spatial Euler flux are
retained. The frozen current executable supplies F^z; a replacement bare
dust equation is not used. Raw-versus-clock gradient chain rules are checked.

The particular a0/Sdot=0 representation is only a way to evaluate this scalar
density derivative. It is not a physical choice of zero shift drift. A paired
coordinate acceleration changes a by Lie_T(q) and Sdot by T, with the same
initial coordinate value/velocity. The density time derivative is unchanged.
The executable tests nonzero T,T_z,T_zz and corresponding a,a_z at every
centre point; the change is below its 1e-30 control. The actual coordinate
gauge construction from the preceding owner remains in force.

## Centre comparison and limits of the continuum enclosure

All three numerical-centre checks pass the frozen 1e-8 diagnostic tolerance.
These points use the centre's actual analytic Fourier derivatives, not an
assumption about the exact root's higher derivatives. Interval residuals
control arithmetic and particular-inverse errors, not displacement from
the numerical centre to the exact root.

| z | full residual, approximately | omit regulator flux | omit lapse improvement |
|---|---:|---:|---:|
| 0.3 | -6.0524e-13 | 4.1707e-5 | 2.1840e-4 |
| 1.1 | 5.8574e-13 | -2.6182e-5 | -3.2609e-4 |
| 2.4 | 2.8665e-13 | 1.7973e-6 | 1.6279e-4 |

The first omission is an explicit rejection check. The second is an exported
diagnostic whose intervals also exclude zero. Neither result is an observed
cosmological residual or a measurement of model preference.

Across the exact-root uncertainty, separate component boxes for the
acceleration, its derivative and other cancelling terms yield the much
wider bound [-572.4583,555.7021]. This is not remotely a 1e-8 continuum
accuracy certificate. Broad zero containment is recorded as a bounding
sanity check, not physical clearance. The continuum local-clock status
therefore remains OPEN despite successful centre diagnostics.

## Reproducibility and preservation

[Executable V3](../../../Analysis/MasterTests/test_01_r4c1_rtau_clock_density_v3.py):
23/23, no failed/unknown checks, exact recomputing read-only replay.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_clock_density_v3_attempt_01/summary.json)
SHA256 9bec36b8aaa37c511779cd420e5b351203f8c9be787e6b0d1593230215a786b3.
Controls include the independent analytic higher-jet coefficient, highest-jet
affine extraction, interval-certified particular/derivative inverses, raw
lapse chain rules, paired gauge-drift invariance and source omission.
Same-author controls are not independent external scientific review.

Two incomplete implementation attempts remain preserved:

- [V2 context specification](RES001_R4C1_RTAU_CLOCK_DENSITY_V2_SPEC_2026-11-01.md):
  V1 used a standard scalar on a nonzero-width interval in a bound; the
  extracted frozen-current namespace also needed its explicit mpmath module.
- [V3 normalization specification](RES001_R4C1_RTAU_CLOCK_DENSITY_V3_SPEC_2026-11-01.md):
  V2's external reconstruction path needed literal zero profile slots cast
  to the same spatial-jet type. Values and derivatives were unchanged.

Both failure records are NOT_COMPLETED. No equation, field, uncertainty
domain or acceptance tolerance changed. Source/sidecar bytes and mtimes,
original results and unrelated work are preserved. No additional audit was
launched merely to increase check counts.

## Next route and model implications

More centre samples will not repair the continuum enclosure. The preferred
next check is a constraint-consistent local residual identity: retain the
actual lapse/momentum/frame/auxiliary equations and verify their cancellation
in the local clock balance. Use the explicit action-derived current, not a
bare appeal to global conservation or an assumed missing microscopic input.
If that identity cannot be established, retain its exact missing term or
condition. Do not relax the accuracy criterion or call the wide interval
a physical no-go.

The actual prepared physical symplectic/characteristic calculation remains
the next substantive admission route. It must retain regulator quartic terms
and background-gradient mixing, general permitted perturbations, means,
gauge/constraint drift and root uncertainty. No homogeneous-principal shortcut
or new action adoption is authorized. Sharp final gauge quadrature, higher
auxiliary bounds, transverse spatial wavevectors, finite-time persistence,
interactions/window and identifying matching remain incomplete.

This strengthens an internal classical consistency check for an UNADOPTED
comparison action; it does not close canonical ITSM or provide an acceleration
prediction. No concrete paper correction is made. P1/P2, Thermodynamics,
original R4C1 and the site are unchanged. G1-G6 incomplete; no canonical
promotion, external dispatch, vault mutation, publication or commit/push.
