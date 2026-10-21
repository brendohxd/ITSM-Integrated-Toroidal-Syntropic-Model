# Weak-generator V1: incomplete run, preserved interface failure

21 October 2026. This is a failed execution record, not operator or physical
admission. Source and all attempted receipts remain immutable.

## Exact outcome

`r4c1_weak_generator_realization_v1_attempt_01/summary.json` records
572/627 checks,55 failed,0 unknown, validation WEAK_DESCRIPTOR_UNRESOLVED.
All54 registered tasks entered the full coupled calculation. The failure list
was inspected in full and grouped without discarding any failed assertion:

-9 n17/orientation0 tasks raise AttributeError at the inherited original-
 functional mixed-value control: the check object lacks the method `small`.
-45 other tasks raise the same AttributeError at the inherited full-Ricci
 control. Those controls were not completed and cannot be counted as passes.
-The all-cases-complete assertion fails because all54 records are incomplete.

The preceding per-case stationarity, two-step full Hessian/response,
symmetry and nonzero-drift/velocity-omission controls were recorded, but the
overall calculation remains failed. No theorem or physical clearance is
inferred from the partial checks.

## Frozen evidence

-Executable `test_01_r4c1_weak_generator_realization_v1.py`:
 a51ef58242419032c9438c432130c7b9b7490aa45bf1bb2714dadc28229fa0a2.
-Contract:9aab26ec3f9e30909ff14e246f540bd8ab5301c14a090c9395c99acecac2c196.
-summary.json:2bfdbd80f3172256795edfe2f0251695f385e5017a8d828a1999a1dd477e5e03.
-independent.json:ca1715b3dc4a04b9a247ec2ee6236f1d5ee652524d60c77a65d01a2cc9365a82.
-formulas.json:a30623f240e1124e463873271f5e32a8114ee79c24406b21120aa5fc71cb1582.
-Private run log:`.local/itsm-context/output-ffdaf979dfce4cc5a44d85000690b303.txt`,
 a8d71402eea0c8a1b241877e824d3a6abd11c73abf4b877575168b9b558cedc2.

The unsealed method preflight first returned31/32 because a Fourier helper
overwrote, rather than summed, terms sharing an exponent. Its exact source
snapshot is private `weak-generator-method-preflight-01.py`, hash
30046302f10a2758dba7287ab6a72d5c711834b93dc397e60b58334e184e1585;
the failed log is `output-08599aeb1f00470ab005b0e6cd79c580.txt`, hash
b13effdfd58ef6e8da798896953c54eeb79a72cce979a733f11a41b8d4e95f16.
After collecting equal-exponent coefficients, the unsealed method preflight
returned32/32 (`output-1a292f3653f0497c8bd301a958b1bdca.txt`, hash
05172efcd0d4200fb6d70b331de62cc8d9dc3ee9074a93b9a3ccb40adae09a99).
The above V1 source was then frozen before the full run. No equations, sample
sets or acceptance thresholds were changed in that method repair.

## Next permitted implementation

V2 may supply an explicit local check-interface adapter for the unchanged
legacy mixed/Ricci controls, test both acceptance and rejection, and repeat
the entire registered calculation in fresh receipts. No old source or attempt
is to be edited, relabelled as passed, or silently overwritten. V1 has not
received a full failed-result replay; no such verification is claimed.

Stage2 INCOMPLETE; Stage3 NOT_ENTERED; MAT-001 BLOCKED; K_Q NOT_DERIVED;
V NOT_COMPUTED; UVIR-003 IN_PROGRESS; Stage4A CLOSED; Rule9 DEFERRED;
physics_pass=false; gate_effect=NONE. Native goal remains PAUSED. No physical
state, new action/parent, public upload, commit/push or provider change.
