# R4C1-G3V: sealed-source integrity addendum

Date: 8 October 2026. Owning scope: the original G3V 379/379 run.
Review DEFERRED; physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## Result and corrected reproduction path

The final integrity check found that the unversioned calculation script
had changed after its successful sealed run and replay. Its live bytes
no longer matched the receipt's script hash. Subsequent reads showed
further changes. The writer and the replacement implementation's
scientific validity have not been established in this audit.

The saved 379/379 result files remained unchanged. The exact original
source was recovered from this session's retained literal, preserved at
a distinct versioned path, and verified against the original receipt.
A new nonmutating replay from that versioned source reproduced all four
original JSON payloads byte-for-byte and exited 0.

Use these sealed files for this result:

- [Original calculation source](../../../Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity_v1.py):
  SHA-256 `875aefe980e4b78a1173a69bbd129d81a7dc4b2b0872c0a16774bc7c177bfe8b`.
- [Frozen scientific report](RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_REPORT_2026-10-08_v1.md):
  SHA-256 `952b4315a5607358a4fc0250a9ab67efc90577dda77f006b357fc1cbd74eeb27`.
- [Original receipt](../../../Analysis/MasterTests/outputs/r4c1_g3v_attempt_01/summary.json):
  SHA-256 `07e85fbd5c13b7390be3dadad723a36f445aa065d678b51f8070255834157cae`.

The frozen report's unversioned source link and original replay command
identify the path used at execution time. This addendum supplies the
reproduction path after the detected source drift. It does not validate
or overwrite the changing unversioned replacement. The frozen report
is copied byte-for-byte, retaining its original content and hash.

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity_v1.py --replay
```

The versioned source has the same bytes and SHA-256 as the original
executed source, so its receipt script hash remains correct. Its location
retains the same repository-root resolution. No old output is rewritten.

## Evidence, failures and holds

The failed final-audit log is retained in ignored local storage:
`.local/itsm-context/output-679f40bf201947608b7cb0d453226606.txt`,
SHA-256 `01009df3cc5406ca2e25c774c6817280629c53cc8a297f2a334cb105af2fdb81`.
Its exact failed assertion is the mismatch of the unversioned script
against the pinned artifact hash. The replacement source was observed
at hashes ff1d030eca406e2b0184424afb73c27d2c2fa50a2827f827d940f0a02e6229a2
and then 1144769941ca0d8f34868a10096cf829cfd2580a69a8cc247d20395bb7f2c00e;
these are observations of a changing file, not new sealed results.

The successful versioned replay log is
`.local/itsm-context/output-cc745f2ee03740f9b4c4e5d3649cb39d.txt`,
SHA-256 `d8c962a09844a32e24ea750f2ab59d2cff651b49ecd44f8c13e961263650b504`.
Both the failed audit and replay outputs remain available. An earlier
register append refused an existing backup directory before changing
the register; a new guarded backup was used, preserving its prior prefix.

Scientific disposition is unchanged: the bounded constrained-regularity
test passes; ordinary full cubic Taylor scattering on homogeneous G3 is
HOLD_SUBSTANTIVE. Full finite-density scattering, G3I amplitude survival,
physical EFT cutoff and validity window remain unresolved.
The replacement script is not covered by the original 379/379 receipt.

R9-MT1-G3V and all its review/scientific dependencies remain inherited.
Canonical Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No action change, publication, commit, push, provider dispatch, memory
mutation or replacement-source overwrite is performed by this addendum.