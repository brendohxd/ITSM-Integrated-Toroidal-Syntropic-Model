# R4C1 three-family coupled initial-response checkpoint (V2)

12 October 2026. Owner: unchanged-action Stage 2 of the dust/GR/weak-field plan.
Operator approval: continue the unchanged R4C1 action with a bounded coupled-
interaction/physical-window calculation. This is an initial-data checkpoint,
NOT completion of that physical-window calculation or admission of a family.

## Result and scope

V2: **970/970 local checks; exact read-only replay.** The six V1 source-identity
failures are repaired by completing the paired mixed-derivative map. The
numerical `initial_response.json` is BYTE-IDENTICAL to V1. Neither an action
coefficient, source, initial datum nor acceptance tolerance was changed.

All three registered families, six eta values and k=20,40,80 remain. Each event
retains the quadratic mean and complex +/-2k source, including its sine part:
108 initial-response records with all 22 original Euler rows reconstructed.
The maximum normalized full-row residual is 1.7584673488565992e-13, below the
frozen 1e-9 threshold. Raw coefficient time derivatives also pass an independent
five-point directional check at the unchanged 1e-8 threshold.

The homogeneous branch uses all six metric components and only the Z inverse;
it never substitutes k=0 into a nonzero-mode shift inverse. The nonzero branch
uses the member-dependent auxiliary inverse and clock/unit constraints. Its
forced affine auxiliary offset and time drift are retained. Dust density,
dust-density velocity and normal multiplier are recovered from the unreduced
lapse, dust and normal equations. Setting every response to zero, or dropping
the forced auxiliary offset, is explicitly rejected.

All 54 mean records retain negative eigenvalues of the signed reduced kinetic
matrix. These are reported, not deleted or relabelled healthy. This checkpoint
does NOT complete their physical-energy/fixed-charge constraint classification.

The nonanalytic force keeps e*abs(e), w*abs(w), and its full odd-harmonic formula
and forcing-tail bound. No ordinary cubic Taylor vertex, smoothing, finite
invariant manifold or evolved-response tail certificate is asserted.

## Preserved failed attempt and diagnosis

V1 remains **FAIL_LOCAL_CHECKS, 958/964**, with exact read-only replay returning
exit 1 and the SAME six residuals. It is not retroactively passed. Its time map
introduced W_ttz and W_tzz, but its spatial map omitted the paired derivatives
d_z(W_tt)=W_ttz and d_z(W_tz)=W_tzz. An independent read-only evaluation of the
missing terms cancels every failed identity exactly for symbolic eta in each
family. V2 adds both terms and exact commuting-derivative tests, rather than
setting either jet to zero. Original G3N4 sources and historical scope remain.

V1 source SHA-256:
f44f532ce85ba213f1fd7d3aa9d1ab700833065b74596429ac264c56da937cad.
V1 failed summary:
e4dbb787ebfdef15fe87566fb3a9a39f130932f023799df897466180997e7d16.
V1 and V2 identical numerical initial-response artifact:
efade1b2d4f8abc4faf27ad8308f8d5264e41cdde2e64d36dffa4640faeaf8ed.

## Reproducibility

Frozen original contract:
`RES001_R4C1_THREE_FAMILY_RESPONSE_ENTRY_V1_CONTRACT_2026-10-12.md`
(fa737c57c36a76561ef24a492d707701ba735b0e68454bb17233eebdb41c84d1).
Frozen repair supplement:
`RES001_R4C1_THREE_FAMILY_RESPONSE_ENTRY_V2_DISPOSITION_2026-10-12.md`
(32b387254924dfa6f6efe1af48a9a078ffa923ce79b8e495d4205c4dd2d40123).
V2 executable: `Analysis/MasterTests/test_01_r4c1_three_family_response_entry_v2.py`
(edf40da0c75f47d6e9a2e9b2386e524d30510d931f15dd21945645bf1cb55434).
New receipt directory: `Analysis/MasterTests/outputs/r4c1_three_family_response_entry_attempt_02/`.
Summary: 2ebf35fb122449725d8ebfbb4483d260eec5abe22f8ef6115627fe9798db64ad.
Formulas: 0436fa3ea231b74d718df29956914c26364d245487f0bd0040cf0278f9f6a112.
Controls: 320fe56a39f2f54fecee462bd32e38617ef3d2474cb3152fbbda6ebc83248e30.
233 inherited/source pins and 463 source/sidecar metadata records are preserved.
Three inherited UVIR documents have no sidecar; their source bytes are pinned.
Missing historical sidecars were neither manufactured nor overwritten.

Private execution/replay logs stay ignored and are not publication artifacts.
New execution: output-443f5fcb9f9846dbbf20b2d4010e0e50.txt,
SHA 772de886f98036539c583ae282be26be2afdadc28acaf42ccff4cd6e953e117f.
V1 exact failed replay: output-1ef0e185e1634edabb35a324af9365d2.txt,
SHA 29cd34009cac47014e84dc106d9c6aa823fdd20126b89bc74350e5cfcec3bdb6.
V2 exact passed replay: output-afa1d587402d4dcaab37732f3e161199.txt,
SHA 6527865fcb9c65159d73d1cddecd64f0eff8267073131314a24cea2e2810cba2.

## What is still required

The next bounded same-action task is the TIME-DEPENDENT sourced response:
derive its drifting affine reduction, evolve the prepared first-order mode and
second-order mean/2k response, reconstruct all 22 fields, independently check
that the recovered dust-density derivative is an actual time derivative, and
retain the odd nonanalytic forcing. Initial algebraic compatibility alone does
not establish propagation, a nonlinear remainder or a controlled physical band.

Full finite-density interactions, complete quartic/constraint reduction,
continuous all-sector frequency/momentum validity, physical-energy/mean/
fixed-charge/singular-domain treatment, healthy GR recovery and full conformal-
matter PPN remain substantive requirements. Positive sampled frequencies do not
replace them. No physical family admitted; Stage 2 incomplete and
STOP_AND_ASSESS_DOMAIN_UNRESOLVED. Stage 3 NOT ENTERED: genuine identifying
matter-residue and nonlinear-force matching is absent. This is not an all-action
no-go theorem.

Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Root goal ACTIVE/incomplete. No manuscript/PDF, publication, commit/push,
provider/model/runtime/dependency or vault changes.
