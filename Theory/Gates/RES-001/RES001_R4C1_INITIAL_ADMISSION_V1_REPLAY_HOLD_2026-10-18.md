# Initial-admission V1: preserve the failed exact replay

18 October 2026. Execution/provenance hold, frozen before diagnostic comparison.

The original V1 execution completed exit0, 217/217 local checks and nine
strict interval certificates. Its files and sidecars remain unchanged.
The full fresh replay completed exit1 at the exact comparison of proof.json:

    ValueError: replay byte/metadata mismatch proof.json

The replay compared summary.json first without reporting a mismatch. It then
stopped on proof.json, so it did NOT compare the later certificate/archive
payloads. Do not describe this replay as successful or assume those files match.

The exact cause and extent are UNKNOWN at this note's freeze time. In particular
neither a harmless serialization explanation nor a physics failure is inferred.
A fresh unchanged-V1 execution to a NEW attempt02 directory has been started
to preserve recomputed payloads for exact field-level comparison. Never replace
the original attempt, source, sidecars, bounds or failed execution evidence.

V1 source SHA-256:
d994707a9261e276b6d9fcb3377acfd75387ce8cdac10f7756e2f791c5787e0a.
Original summary:
993b5cfffcb4b7c4106656a6929dfcc0379858c53e6556f60bb5b56b24ec5f4c.
Original proof:
b96ee17ec3d3f14500d0bf59d786411f5e241cbbb238ef49f3dc34657a18646b.
Failed replay output digest (private optimizer log retained locally):
d33119fae2e00d82ba7d642aea44f07c13209210facd1fa1bdb4016988d048aa.

Known initial-surface certificates remain the original run's bounded output,
not an exact-replay-cleared package. Full initial-data admission, Stage2 and
physical validity remain OPEN; Stage3 not entered; physics_pass=false;
gate_effect=NONE; review DEFERRED; Rule9_cleared=false. No state is adopted
or evolved, no existing artifact/hash is repaired, and no action, model,
runtime, vault, publication or Git change is performed by this note.
