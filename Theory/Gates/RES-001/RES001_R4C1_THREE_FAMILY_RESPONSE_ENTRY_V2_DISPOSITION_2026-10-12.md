# Three-family response entry: V1 failure disposition and V2 contract supplement

12 October 2026. Owner: unchanged R4C1 Stage 2. Frozen BEFORE V2 execution.
The V1 contract, source, failed receipt and sidecars remain immutable.
No action, family, initial data, response source, tolerance or acceptance scope
is changed. This supplement corrects the derivative implementation, not physics.

V1 source: f44f532ce85ba213f1fd7d3aa9d1ab700833065b74596429ac264c56da937cad.
V1 summary: e4dbb787ebfdef15fe87566fb3a9a39f130932f023799df897466180997e7d16.
V1 initial_response.json: efade1b2d4f8abc4faf27ad8308f8d5264e41cdde2e64d36dffa4640faeaf8ed.
V1 result: FAIL_LOCAL_CHECKS, 958/964, six symbolic source-identity failures.
All 108 initial-response events passed their full 22-field residual checks,
but the original package remains failed and does not certify compatibility.

## Diagnosis and explicit repair

V1 introduced the independent third mixed jets in its time chain rule:
d_t(W_zz)=W_tzz and d_t(W_tz)=W_ttz. Its spatial chain rule omitted the
paired terms d_z(W_tz)=W_tzz and d_z(W_tt)=W_ttz. Thus the temporal and
longitudinal source identities retained one half of each cancellation.

An independent read-only calculation of the missing contributions from the
saved preexisting sources proves exact cancellation of ALL six failed residuals
for symbolic eta in all three families. It adds, without changing any source,

```text
temporal correction = [partial_(W_tz)(S_Sz+S_Vz)] W_tzz/a
longitudinal correction = 2[partial_(W_tt) S_Mzz] W_ttz.
```

V2 completes the paired spatial derivative map and adds exact tests for
d_t d_z=d_z d_t at the retained mixed-jet order. Neither mixed jet is set to
zero to make a check pass. Sources are not edited. The original G3N4 checks
retain their original lower-jet implementation and scope; no historical report
is silently replaced by this expanded derivative-map result.

V2 must use a fresh attempt_02, preserve and pin every V1 source/artifact,
and reproduce initial_response.json BYTE-IDENTICALLY to V1. Both receipts
receive exact read-only replay (V1 is expected to remain an exit-1 failure).
Retain every old failed assertion and every physical/review hold. All original
V1 numerical thresholds stay unchanged: chain-rule control <=1e-8,
full 22-field residual <=1e-9, auxiliary/Fourier checks <=1e-10.

## Unchanged physical boundary

The entry covers family-dependent source equations and compatible INITIAL
second-order data, not a full time trajectory, nonlinear remainder or physical
frequency/momentum window. No family admitted. Stage 2 incomplete;
STOP_AND_ASSESS_DOMAIN_UNRESOLVED; Stage 3 NOT ENTERED; identifying matching
absent. Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
No publication/commit/push/model/provider/runtime/dependency/vault changes.
