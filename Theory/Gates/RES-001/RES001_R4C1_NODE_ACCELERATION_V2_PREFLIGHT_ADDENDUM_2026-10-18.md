# Node acceleration V2: pre-execution implementation correction

18 October 2026. Inherit every scientific requirement, domain restriction,
rejection control, tolerance and hold in
RES001_R4C1_NODE_ACCELERATION_V1_CONTRACT_2026-10-18.md, SHA-256
4e81b770bcf5ad3b999ce34af37326803c1f73aba852b21f1d0bafb75c2a5f96.

The new V1 source failed AST preflight with an unexpected indent. The command
continued to write its sidecar despite that failure. It was not scientifically
executed and no node-acceleration receipt or result was produced. Preserve the
V1 source and sidecar at SHA-256
f91899a6add8ceff67b2358f63f6cc8f2ec8b18cc0d486a00039fa4b84250e1b.
This is an implementation failure, not a failure of the scalar equations.

V2 corrects the new blocks' indentation and retains the explicit three-value
interval_setup return. Verify AST and source dependencies before execution;
sidecar creation must stop if static validation fails. No equation, numerical
tolerance, frozen parent input, family, amplitude or angular partition is changed.

Executable: Analysis/MasterTests/test_01_r4c1_node_acceleration_v2.py.
Fresh outputs: Analysis/MasterTests/outputs/r4c1_node_acceleration_attempt_02.
Keep V1 and any subsequent failed attempts. The V2 source pins both this addendum
and the original contract and preflight-failed source. Exact read-only replay,
separate byte/metadata checks and an owning report remain required.

This correction supplies no scientific outcome. Stage 2 INCOMPLETE; Stage 3
NOT_ENTERED; full initial admission/evolution OPEN. Review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. No gate or parent
change, vault write, manuscript/site edit, commit/push, publication, provider
dispatch or model/runtime change.
