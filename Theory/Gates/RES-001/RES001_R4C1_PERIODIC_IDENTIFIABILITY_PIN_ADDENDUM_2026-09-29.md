# R4C1-C2P: transitive source-pin addendum before attempt 02

Date: 2026-09-29. Owner: Master Test 3 / R4C1-C2.
The [original C2 contract](RES001_R4C1_PERIODIC_IDENTIFIABILITY_CONTRACT_2026-09-29.md)
(SHA-256 `dd711d678c824e7f414b9170c164fc3cc101d880134df9d58012a5c0ddbf6d7a`)
and attempt-01 receipt (SHA-256
`d84689e19df53d29a03cc3f2d0c510d5e54c0681a86090fa7cfbe4c78a5e4dfb`)
remain unchanged. Attempt 01 passed 107/107 local checks but its executable
only checked eight direct source pins; it did not itself rehash the
transitive source maps embedded in the pinned C1 and T2P1 receipts before
reading the B1 parameter literal. A separate read-only recheck found all
eight T2P1 and five C1 source paths matched their recorded hashes.

For attempt 02, before importing T2P1 definitions or reading B1 parameters,
rehash every `source_sha256` member in both pinned parent receipts and
check any present `.sha256` sidecar. Explicitly require that the B1 script
`Analysis/MasterTests/test_01_r4c1_interacting_background.py` has the
T2P1-recorded SHA-256
`1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f`.
Fail before calculation on any absence or mismatch. Preserve attempt 01;
write attempt 02 as a separate immutable receipt.

This is a provenance-hardening addendum only. The action, B1 literal,
source, A ratios, grids, solver, physics equations, thresholds and status
rules from C2 are frozen and unchanged. A new local PASS still does not
derive `C_chi`, `a0` or canonical Test 3, and Rule 9 remains deferred.
