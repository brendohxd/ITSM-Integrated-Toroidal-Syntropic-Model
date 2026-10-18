# ITSM regulator-node completion checkpoint - 18 October 2026

Operator-authorized documentation, commit and push on
`recovery/v12-core-architecture`, following `e759f104`. This supplements the
[earlier 18 October checkpoint](ITSM_RESEARCH_CHECKPOINT_2026-10-18.md); it
does not revise that frozen evidence, select a new action, adopt or evolve a
state, or clear a physical gate.

## What advanced, and what it means

| Calculation | Owning evidence | Result and boundary |
|---|---|---|
| Regulator-node acceleration preflight | [V1 contract](../Gates/RES-001/RES001_R4C1_NODE_ACCELERATION_V1_CONTRACT_2026-10-18.md) and [V2 preflight addendum](../Gates/RES-001/RES001_R4C1_NODE_ACCELERATION_V2_PREFLIGHT_ADDENDUM_2026-10-18.md) | V1 failed its static syntax preflight and was never scientifically run. V2 preserves that failed source and repairs only the executable preflight defect. |
| Selected regulator continuation | [Node-acceleration V2 report](../Gates/RES-001/RES001_R4C1_NODE_ACCELERATION_V2_REPORT_2026-10-18.md) | 48/48 local checks and a complete exact read-only replay. For all nine registered family/eta cases and every `0<|e|<=1/500`, the selected `U0` continuation fails the stated necessary scalar node-acceleration condition. This is a scoped negative result, not an all-action no-go and not a rejection of the previously certified known constraint surface. |
| Restricted coupled completion | [Coupled V1 report](../Gates/RES-001/RES001_R4C1_COUPLED_NODE_COMPLETION_V1_REPORT_2026-10-18.md) with [endpoint addendum](../Gates/RES-001/RES001_R4C1_COUPLED_NODE_COMPLETION_V1_ENDPOINT_ADDENDUM_2026-10-18.md) | 104/104 local checks and a complete exact read-only replay. Strict rectangle-face signs, `F_H<0`, and a positive coupled Schur derivative certify a unique root of the restricted mean/node `H,U` system for all nine cases and the continuous registered amplitude interval. Both global charges, the full local lapse flux, and positive local density are retained. |

The coupled construction solves

```text
F = <E> + rho0 = 0,
B = G - beta*F = K_Q*(U-U0) + e^2*Dnode = 0
```

together on the unchanged action and declared initial slice. The exact shift
inverse and its `H,U` sensitivities have fresh residual/coercivity bounds over
the full rectangle; the old `U0`-only errors are not reused. The stored
intervals give the global endpoint-safe bounds

```text
|U-U0| <= 17.492*e^2,
|Z-Zold| <= 17.492*e^4*cos^2(theta).
```

The second bound is a controlled change of the regulator initial field. It is
not a nonlinear evolution remainder. The retained choice
`Z_dot=Ud0*w^2` is still an explicitly unproved higher-order velocity
continuation. No corrected state is adopted or evolved.

The approximate coupled roots converge within five Newton evaluations; the
largest saved point residual is below `7.825e-76`. Separate original-action
8/12-harmonic Galerkin controls differ by less than `8.630e-54` in the saved
normalization. These are numerical controls, not the existence proof and not
independent peer review; the interval face, derivative, density, and
residual/coercivity certificates carry the restricted proof.

## Replay and preservation result

The node-acceleration replay preserved all ten output/sidecar files, all 29
source pins, and all 58 source/sidecar metadata records while reproducing
48/48 checks exactly. The coupled replay preserved all eight output/sidecar
files, the same counts of source pins and metadata records, and reproduced
104/104 checks exactly. Both replay processes exited zero.

```powershell
python -B Analysis/MasterTests/test_01_r4c1_node_acceleration_v2.py --replay Analysis/MasterTests/outputs/r4c1_node_acceleration_attempt_02
python -B Analysis/MasterTests/test_01_r4c1_coupled_node_completion_v1.py --replay Analysis/MasterTests/outputs/r4c1_coupled_node_completion_attempt_01
```

The V1 preflight failure, V2 executable, coupled executable, contracts,
addenda, reports, receipts, sidecars, and existing append-only execution and
deferred-review records are retained. Old reports and checkpoints remain
unchanged.

## Consequences for the live programme

This checkpoint supplies a necessary-compatible restricted initial
construction after the selected `U0` continuation failed. It does not prove
full initial-data admission, retained regulator-velocity compatibility,
higher node time-consistency, persistence, or the complete rank-changing
constrained acceleration system. It also does not provide arbitrary-three-
dimensional closure, the physical constrained Hessian, a Cauchy/energy
domain, a nonlinear evolution remainder, a nonempty physical momentum or
frequency window, healthy GR recovery, or either missing identifying matching
input.

Stage 1 remains complete only in its registered linear prepared-dust scope.
Stage 2 remains `INCOMPLETE`; Stage 3 is `NOT_ENTERED`. Tests 1-3 remain
`HOLD_SUBSTANTIVE`; MAT-001 `BLOCKED`; UVIR-003 `IN_PROGRESS`;
`K_Q=NOT_DERIVED`; `V=NOT_COMPUTED`; Stage 4A `CLOSED`; TOP-X4 unchanged.
Review is `DEFERRED`, `Rule9_cleared=false`, `physics_pass=false`, and
`gate_effect=NONE`. Deferred review permits only the bounded provisional reuse
recorded in the register; it is not canonical promotion or publication
readiness.

## Commit and publication scope

This checkpoint includes only the regulator-node acceleration and coupled-node
completion sources, frozen outputs, contracts, reports, addenda, sidecars,
their guarded execution/review index appends, this evidence map, its exact-byte
manifest, and the matching changelog entry.

Separate main-manuscript working TeX/PDF/BibTeX files, the conditional
architecture figure and generator, and the scratch CUSP3 QA script remain
local, untouched, and unstaged. Private optimizer output, logs, raw chats and
recordings, vault data, and credentials are excluded. No website deployment,
paper submission, vault synchronization, provider dispatch, or runtime change
is included.

## Integrity verification

The [manifest](ITSM_NODE_COMPLETION_CHECKPOINT_2026-10-18.manifest.json)
records exact byte lengths, SHA-256 digests, selected scientific source pins,
and the unchanged holds. Run the existing checker from the repository root:

```powershell
python -B Scripts/verify_research_checkpoint.py --manifest Theory/Verification/ITSM_NODE_COMPLETION_CHECKPOINT_2026-10-18.manifest.json
```

For staged blobs add `--revision INDEX`; for the committed snapshot add
`--revision HEAD`. A `PASS_CHECKPOINT_INTEGRITY_ONLY` result verifies this
artifact boundary, not physical validity or review clearance.
