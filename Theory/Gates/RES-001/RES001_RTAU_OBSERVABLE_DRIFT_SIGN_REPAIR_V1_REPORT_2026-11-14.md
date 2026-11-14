# Correction to the initial observable coefficient drift

The historical V2 executable and report have the wrong sign in the
conformal scale contribution to the auxiliary background rate. They are
preserved. This note supersedes that signed formula only; the corrected
calculation is `test_rtau_density_operator_drift_v3.py` under the frozen
sign-repair contract of the same date.

For the registered initial conformal metric, write

    Z=-exp(-2 lambda)(psi_zz+lambda_z psi_z), L=lambda_t.
    Z_t=-2 L Z-exp(-2 lambda)
        (psi_tzz+lambda_z psi_tz+L_z psi_z).

V2 used +2 L Z. Differentiating the defining geometric expression gives
the negative sign, in agreement with the independently prepared auxiliary
velocity in the clock-density V3 calculation. V3 checks both identities.
The independent geometric differentiation is the substantive sign check;
the additional algebraic defect bookkeeping check is not independent evidence.

V3 passed all twelve recorded controls, verified 389 pinned inputs and
replayed byte for byte without modifying the original inputs or sidecars.
Its receipt is
`Analysis/MasterTests/outputs/rtau_density_operator_drift_v3_20261114/receipt.json`.

The auxiliary coefficient's absolute whole-circle bound remains
0.0002159520861002147131145398118093318. All eight input coefficient
bounds also remain identical, with maximum 88.51572237361152 (rounded).
The existing conservative bound 89 U8 therefore survives this correction.
This happens because the calculation encloses the scale contribution
symmetrically; it does not make the two signed formulas equivalent.

Scope: this repairs the signed initial time drift of the physical-density
observable's auxiliary coefficient. The static observable map and the
separate physical-density projection algebra do not use this background
time-rate sign. Future numerical physical-density remainder composition
must use V3. The corrected-density state-map and trace-source results are
not promoted or broadened by this repair. Controlled evolution, the other
generator rows and physical clearance remain open.

R-tau remains an unadopted comparator. Review DEFERRED;
physics_pass=false; gate_effect=NONE. Hashes and replay certify integrity
and computational scope, not physical acceptance.
