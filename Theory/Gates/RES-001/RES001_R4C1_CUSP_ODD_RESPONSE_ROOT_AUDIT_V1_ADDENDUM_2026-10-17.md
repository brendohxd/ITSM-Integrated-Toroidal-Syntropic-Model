# Lower odd response: stored wave-zero controls

17 October 2026. Additive control under the CUSP_ODD_RESPONSE_TAIL_V1 contract.
The primary report, source, 199-check receipt and all hashes remain unchanged.

The primary program checked the21 stored time nodes per run. This separate
versioned audit checks the additionally stored wave-zero sample in all18 runs,
both lower modes1,3:36 energy controls. Its58 total controls include root-time,
parent/provenance and preservation checks. All passed, with exact read-only replay.

At each root the background scale factor need not be interpolated:
a>=1 implies

    E_n(root)<=|r_n_dot|^2+[cV2*(40*n)^2+1]*|r_n|^2.

This conservative upper energy is below the already proved bound in every
stored case (maximum normalized excess0). Root times lie in[0,1/20].
No new integration, interpolation, amplitude fitting or changed criterion.
The continuous proof remains the energy/Duhamel argument in the parent report,
not the finite sample agreement.

Executable: Analysis/MasterTests/test_01_r4c1_cusp_odd_response_root_audit_v1.py.
Source SHAf3418441fb088ac5320e508139b62a658b5491d2d1ab549e91b721ce225f8946.
Receipts: Analysis/MasterTests/outputs/r4c1_cusp_odd_response_root_audit_attempt_01/.
Summary SHAcc709dd431d8d1d11d1273eb7591aa2f9ac515b61307fef42515db9a11fc2632.
Run the executable with existing itsm_env Python -B; add --replay for reproduction.
Both returned0; replay printed READ_ONLY_REPLAY_EXACT and preserved output bytes,
sidecars, sizes and modification times. All parent source pins and available
sidecars verified; the three inherited absent sidecars remain explicit.

This completes the stored-sample coverage of the lower response package without
changing its scope. Inherit R9-MT1-CUSP-ODD-RESPONSE-TAIL-V1 and all transitive debt;
review DEFERRED, Rule9_cleared=false, physics_pass=false, gate_effect=NONE.
No full coupled order-|e|^3 tail or nonlinear remainder, physical window, healthy
GR, matching or publication clearance follows. Stage2 incomplete; Stage3 not
entered; native full goal active. No commit, push or external action.
