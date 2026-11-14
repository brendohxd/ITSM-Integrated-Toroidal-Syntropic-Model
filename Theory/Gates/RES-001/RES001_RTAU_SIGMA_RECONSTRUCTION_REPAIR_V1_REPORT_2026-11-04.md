# Corrected Sigma reconstruction and initial dependent bounds

4 November 2026. High calculation bundle. This report owns the corrected
results; the separate coordinate-defect report preserves the original error
and the historical dependent-use hold.

## Outcome and meaning

The rho/Sigma substitution error is repaired for the INITIAL constraint
reconstruction and the explicitly recomputed descendants below. The unchanged
R-tau comparator still has an invertible compensated-current constraint map
on the registered prepared background. This does not establish a physically
admitted evolving domain, a complete generator, stability, or a time tube.
R-tau remains UNADOPTED, not a silently chosen new canonical action.

The original V2 reconstruction and its old dependent receipts remain held for
their Sigma-norm interpretation. New results replace their prospective use;
they do not rewrite the old records or make the old calculation correct.

## Correct current and trace operator

The required identities, with M=N mu, are

    Sigma = rho + e_force + b Z^2/2,  e_force=p f_p-f,
    I_total = M rho,                 I_other=M Sigma,
    delta I_total = M delta Sigma + rho delta M
                    - M(delta e_force+b Z delta Z).

The canonical Legendre differential retains the full measure and field terms:

    delta e_force = (p/mu) delta pi_psi - p f_p delta mu/mu
                    - sum(f_q delta q) - f_s delta s.

V4 reconstructs I_other directly from L_other=L_total-M f-L_reg and the
other-sector improved lapse current. It retains all ordinary momenta; the
other-sector clock momentum vanishes by the pinned action's exact dependency
structure. This removal applies only to the compensated-current calculation.
The spatial momentum constraint still contains the TOTAL clock momentum and
its force-field source. All torus means, integration partners and independent
total-I/U1 charge tangents remain required. No new fixed Sigma charge is used.

For transverse metric trace f_tr, delta hxx=delta hyy=a^2 f_tr,

    L_Sigma = L_current + c0*f_tr + c1*D_z f_tr,
    c0=-I_total-M*p*f_p-M*a^2*(f_hxx+f_hyy),
    c1=-b*M*Z*kappa*psi_z.

The f_h derivatives hold proper clock velocity and spatial gradient fixed.
The exact auxiliary variation is delta Z=-kappa*psi_z*D_z f_tr. Generic exact
compensation algebra and the independent direct other-action coefficient
calculation are both retained. Interval overlap is only a consistency control,
not the proof of an identity.

The reference shift is -8/25, so the nonzero reference mass is 17/16 and the
retained mean mass is -4951/8400. The reference inverse norm is 8400/4951.
The actual H1 -> H^-1 perturbation includes the previous current-operator
error, |c0+8/25| and |c1|; the sixteen cells each retain the full prepared root
uncertainty. Their maximum certified Neumann contraction is below 0.351154;
the resulting Green norm is below 2.614835. Rational endpoint controls verify
the Green enclosure independently. No harmonic truncation is used in this
inverse estimate. A negative constraint mean mass is retained, not interpreted
as a physical kinetic signature or an instability verdict.

## New reproducible results

All receipt paths below are under `Analysis/MasterTests/outputs/`. Each new
package passed its listed component checks and a separate byte-identical replay.
These are same-author controls; independent Rule-9 review remains DEFERRED.

| Executable in Analysis/MasterTests | Receipt directory | Checks | Bounded result |
| --- | --- | --- | --- |
| test_rtau_sigma_coordinate_defect_v1.py | rtau_sigma_coordinate_defect_v1_20261104 | 13/13 | Exact omitted-term diagnosis, preservation, reference controls |
| test_rtau_strong_constraint_lift_v4.py | rtau_strong_constraint_lift_v4_20261104 | 147/147 | Initial Sigma reconstruction and trace-gradient smoothing remainder |
| audit_rtau_strong_constraint_lift_v2.py | rtau_strong_constraint_lift_audit_v2_20261104 | 28/28 | Independent periodic, all-frequency and rational endpoint controls |
| test_rtau_strong_force_coordinate_v3.py | rtau_strong_force_coordinate_v3_20261104 | 20/20 | Initial auxiliary/force-coordinate inverse, with mean retained |
| test_rtau_momentum_rate_lift_v2.py | rtau_momentum_rate_lift_v2_20261104 | 11/11 | Initial momentum lift and H1 remainder in corrected strong norm |
| test_rtau_ordinary_velocity_remainder_v2.py | rtau_ordinary_velocity_remainder_v2_20261104 | 11/11 | Ordinary velocity H1 and eight gradient-row L2 remainders |
| test_rtau_ordinary_momentum_remainder_v3.py | rtau_ordinary_momentum_remainder_v3_20261104 | 13/13 | Nine ordinary momentum-row L2 remainders |

The force/metric inverse feedback is below 0.002129. Its old value is not
reused. The full input-wise constants and norm conventions are in the new
receipts, not just these rounded summaries. If U is the sum of the eight
registered strong-data norms and harmonic coordinate velocity norm, conservative
uniform row bounds are 57465 U for the velocity/gradient remainder and 38429 U
for the ordinary momentum remainder. These large estimates do not demonstrate
useful finite-time accuracy, small physical interactions, or a physical cutoff.

The core initial reconstruction pins 348 sources, including the older failures.
Each descendant also pins its corrected parents. Original sources, hashes and
sidecars remain unchanged; mutable navigation preimages were archived locally.

## Preserved attempts and execution-spec clarifications

V3 reconstruction records 127/143 controls, with all sixteen failed controls
testing numerical exact zero after interval subtraction. Such subtraction
cannot establish exact zero across a nonzero-width interval. V4 instead uses
the existing exact action-dependency proof and an interval consistency control.
V3 also omitted the TOTAL clock momentum from one longitudinal source bound;
V4 restores it. Neither V3 nor its quantitative bounds are accepted for reuse.

Some descendant execution specifications retained historical wording while
receiving new version headers. For clarity: the audit V2 audits reconstruction
V4, not the held reconstruction V2; its mean shift is the full compensated
shift -8/25. The force-coordinate V3 specification's polynomial-comparison
discussion describes the earlier V1-to-V2 repair. V3 additionally recomputes
all constants using the new Sigma reconstruction. Its statement about unchanged
coefficients applies to that earlier polynomial repair, not to V3's constants.
The executable parent paths, this report and the repair contract define the
current scope. The pinned specifications and history are preserved.

## Next supported calculation and unresolved requirements

Continue with the actual force-pair remainder using these corrected parents.
Then assemble density/physical-variable rates and moving Green/range/gauge
maps, retaining constraint and charge transport. The complete coupled norm
estimate and evolving domain through t=0.05 remain OPEN; no continually
projected evolution or residual-only substitute is authorized.

There is no new numerical acceleration prediction, microscopic matching input,
SPARC inference or canonical promotion. No concrete P1/P2 or Thermodynamics
claim requires alteration from this bounded unpublished correction alone;
any R4C1 preparation using the affected new estimates must cite these corrected
versions. No paper release, external dispatch, vault mutation or Git delivery
was performed. G1-G6 INCOMPLETE; Rule-9 DEFERRED; physics_pass=false;
gate_effect=NONE; goal remains ACTIVE.
