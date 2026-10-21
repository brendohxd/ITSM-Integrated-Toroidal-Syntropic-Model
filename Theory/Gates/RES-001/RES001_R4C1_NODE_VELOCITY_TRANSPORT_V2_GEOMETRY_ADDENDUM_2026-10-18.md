# Node velocity transport V2: retain the general volume-gradient term

18 October 2026. Supplement the V1 frozen contract; preserve V1 source and its
59/59 initial-only receipts. The V1 exported `C_general` expression was labeled
too broadly: for arbitrary planar spatial metric it omitted

    (gamma*V^z - V^2*R)*partial_z(log sqrt(h)).

This term AND its first-time derivative vanish on the registered initial slice:
h_z=0 and h_dot_z=0. Thus the derived first-time nodal transport, its independent
coordinate checks and nine necessary-slope enclosures do not change. This is
not an assertion that the omitted term vanishes during evolution.

The new V2 executable reuses only frozen V1 utilities, keeps its own contract,
source pins and fresh receipts, and verifies the complete arbitrary-first-jet
product-rule identity before imposing the initial restrictions. Explicitly
reject deletion of the volume-gradient term in the general expression. Rename
the old restricted expression as initial-only; export the complete general one.
Recompute all initial-only controls and compare their payloads with preserved V1
bytes. A fresh exact read-only replay must protect source and receipt bytes and
metadata separately. The V1 historical general-label error is not relabeled as
a correct general formula and is not silently edited.

All V1 regularity, limits, precision and thresholds remain unchanged. In
particular the action-derived coupled frame acceleration is NOT computed by
this scalar-transport calculation. The selected regulator velocity remains
UNRESOLVED, not certified and not rejected. No initial state is adopted/evolved.
Stage2 INCOMPLETE; Stage3 NOT_ENTERED; physics_pass=false; gate_effect=NONE;
Rule9_cleared=false; review DEFERRED; physical window and identifying matching
inputs remain open. No change of action, provider/runtime, manuscript/site,
vault, commit/push, publication or submission.
