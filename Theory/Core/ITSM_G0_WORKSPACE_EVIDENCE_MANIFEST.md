# ITSM G0 workspace and evidence manifest

**Snapshot ID:** `G0-SNAPSHOT-2026-08-25T17-01-44+08-00`

**Captured:** `2026-08-25T17:01:44.5638789+08:00`

**Purpose:** non-destructive Phase-G0 freeze of the pre-existing recovery
worktree before authority repair. This manifest changes no scientific status.

## 1. Environment and Git identity

| Field | Raw result |
|---|---|
| Workspace root | `C:/Users/brend/OneDrive/Documents/ITSM - Github/ITSM-Integrated-Toroidal-Syntropic-Model` |
| Time zone | `W. Australia Standard Time (UTC+08:00) Perth` |
| Git | `git version 2.53.0.windows.3` |
| Branch | `recovery/v12-core-architecture` |
| HEAD | `4310a9ad7bc27b7e0f4169586210818761119936` |
| Recorded upstream | `origin/recovery/v12-core-architecture` |
| Local-reference divergence | `+2 -0` |
| Upstream ref tip | `c17a6dbe6efb53c0f92c08955f5306f5528bc054` |
| Staged changes | none |
| `core.autocrlf` | `true` |
| Remote | `https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model.git` |

No fetch was performed. The upstream and divergence fields describe only the
locally recorded remote-tracking ref and must not be presented as live GitHub
state.

The two commits ahead of that ref are:

| Commit | Date | Subject |
|---|---|---|
| `7cd687d42eff9939198841d2432ab138b7719de6` | `2026-08-09T00:30:37+08:00` | Revert hallucinated alpha.13 overclaims, fake MCMC results, and post-hoc MAT-001 derivations |
| `4310a9ad7bc27b7e0f4169586210818761119936` | `2026-08-09T00:32:10+08:00` | Update GEMINI.md with mandatory dimensional and contradiction checks |

## 2. Snapshot method

The inventory was produced from the following read-only commands:

```powershell
git status --porcelain=v2 --branch
git diff --name-status
git diff --cached --name-status
git ls-files --others --exclude-standard
git hash-object --path <path> -- <path>
git ls-files --stage -- <path>
Get-FileHash -Algorithm SHA256 -LiteralPath <path>
```

`SHA-256` is the raw filesystem-byte hash. `Index blob` and `working blob` are
Git hashes after the path's configured normalization. `Same` in the final
column means that Git-normalized content matches the index even though
`git status` reported the path modified; it does not mean that raw bytes match.

## 3. Pre-existing dirty and untracked inventory

| Status | Path | Bytes | SHA-256 | Index blob | Working blob | Substantive against index |
|---|---|---:|---|---|---|---|
| `M` | `Analysis/MAT/MAT-001/HANDOFF/outputs/mat001_uvir_handoff_contract_summary.json` | 7,398 | `015311b17d857057a06c29b88a07d69d3bb92e21b0f6d32153309cff7c7af8f9` | `3271e0368fc5e74d9b69cde84d1234418faaf3a1` | `dd3be5376e099d579f7a0b189bc57112227d775b` | Yes |
| `M` | `Analysis/MAT/MAT-001/HANDOFF/outputs/mat001_uvir_handoff_contract_summary.sha256` | 108 | `f46c158519cb67a3d95a8734ad2984c3ee0409c0e48b5b76f42798d7e4895ad9` | `92506d45fe5a627aa9a48a9cb5f167405c7e6f39` | `0598b72570549c9f0d5cc82836b8264a047e6891` | Yes |
| `M` | `Analysis/MAT/MAT-001/R5_IDENTIFIABILITY/outputs/mat001_r5_microscopic_matching_decision_summary.sha256` | 120 | `b6db777641d4d5ac56d98a99bab2b06a7f1876d5399e25a7b3b3377eca79931f` | `6e3ebfdc1f77d8b738b07f007665d9e733f1aa4b` | `6e3ebfdc1f77d8b738b07f007665d9e733f1aa4b` | Same |
| `M` | `Analysis/UVIR/UVIR-003/outputs/uvir003_local_four_leg_kernel.csv` | 6,423 | `878907eba7e10de68fc0b7feb97493e74fe5e49ab50f948cac19e666a0ab730b` | `01d423fda70ecee120ae706551181aa5996368bb` | `01d423fda70ecee120ae706551181aa5996368bb` | Same |
| `M` | `Analysis/UVIR/UVIR-003/outputs/uvir003_local_four_leg_kernel_summary.json` | 293,282 | `18bede3d906211d7457658585ac3ebd04eac0b5f9abdddc7acea13e798da06c5` | `7ae2241625dc45b0d2ca0fa9ecc4b8e21d7f4d30` | `7ae2241625dc45b0d2ca0fa9ecc4b8e21d7f4d30` | Same |
| `M` | `GEMINI.md` | 6,934 | `5660cd00371b51566c63d07bcaed76b443c450220fc9ff5269fb61635fe183e7` | `a6361e1188bdff27c3d9f838373fee4277f83ff5` | `b1a31d0c36db6d536088c99ef9b45b6b595e9892` | Yes |
| `M` | `RECOVERY_BRANCH_README.md` | 27,005 | `8e4e39706e6d54efeb28c1c3c58d3ce876b2bf6cfd56ba8ac56b7ed4e2b18463` | `71e0776983a2d9b272304bce375dfb0c49db1748` | `ba8ef517096456571af0b856ffe7ef03a9f4cdeb` | Yes |
| `M` | `Theory/Core/ITSM_Claim_Migration_Ledger.csv` | 38,199 | `5522b59ea96ecafea5c9302ab0c77dfe891644975768bfaa8e290955eb934a9e` | `b4a79cf22cd7500c51705c8c35e990f6e2362592` | `9c7af9269eebc5549874c36b56e3d7bae49b4551` | Yes |
| `M` | `Theory/Core/ITSM_Core_Architecture.md` | 18,160 | `001adca1bb2ca4dc32a1e62206f520b1161be06340526bd6edf2fea3eab79162` | `9b73d28a7ffbfac4d26201c6f31c35183f169fdd` | `0b5c38344e8faebe61484687cc38d47659b39f24` | Yes |
| `M` | `Theory/Core/ITSM_Master_Research_Plan.md` | 31,391 | `68815fe4b4511273a9cb9d8456dc24add0a8034dcffb4fe84d8766eefabd290f` | `40b4d479370cb70340e0317c59951b47453f6b38` | `f3f26b198309e090850e094fde9f32267992de70` | Yes |
| `M` | `Theory/Core/ITSM_Tier1_Forward_Plan.md` | 11,887 | `3fae58c3f8aa843ea0a44d9d1c9d201054d90c45ae3860f976fa15723b69e713` | `13ae963a7ded52f2737ba56202ed2939756b3cdb` | `59ebec70bf47d38cc095b26c52b490ed3ff80ba1` | Yes |
| `M` | `Theory/Gates/CBR-002/SOLAR_SYSTEM_BOUND.md` | 4,791 | `22c982833ffd6698450b6d12c80aa825c0273ac45a3d11da9fc0ce145c5ebe9a` | `5e91c8d07883c1e9517be89f514fc3d5cbf7fd5f` | `26d4229572d6a10a4b72c4bb49b4a515e536efc8` | Yes |
| `M` | `Theory/Gates/VOR-001/VOR-001_GATE_SPEC.md` | 17,160 | `80b371ad9bcd8f635c7ba4f9ccad817fa29b425bb09cc28df5e79ff465699ef1` | `182dc3110c1543b52fe6cb71c926e06b04814885` | `eddf43b79e8f9458f6580e3d82c130094fcfe16f` | Yes |
| `??` | `Manuscript/ITSM_Core_Cosmology_v11.4.1.md` | 166,981 | `8576acc18bb78cfaf55df48143d1700a211e539a473aa9c04a0bd435d7b1f8e3` | untracked | `a78fe6efed142c4ada201fd71a633c9501879919` | New |
| `??` | `Manuscript/ITSM_Core_Cosmology_v11.4.1.pdf` | 11,434,507 | `7a7e5cc859fb80f6b81e00d4341fe14b06c57ce00b4e0572319f634499ee1231` | untracked | `89c0c4efd5394831b773b316e4ab3b630b679f1b` | New |
| `??` | `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md` | 5,533 | `635e3a4e770b2336e89dcfb87313fc5a262f77999adf919ed7c1a547410c9c71` | untracked | `58726d798aee9b7f0086ccae1425c4ad4a343bde` | New |
| `??` | `Theory/Core/ITSM_Tier1_Route_Test_Programme.md` | 28,011 | `f2f5077d35c4aad97c0bdc6c82f694cb69fcee3cab6f84b9fcb964567854d850` | untracked | `d969f72f57e406ec3b00f66e3ff9ae3b26010c46` | New |
| `??` | `Theory/Gates/CBR-002/CBR-002_SCALE_DERIVATION.md` | 3,666 | `ab73b84db121f970e5c3f6d7fee767e86a0435fd3eccb3aca9b4dc83f2e0f414` | untracked | `cbd4023489ffd0b750a6c53e3c4b113fc39b9201` | New |
| `??` | `Theory/Gates/UVIR-003/UVIR-003_PROGRESS.md` | 4,796 | `52bdb325828669d1825a72d480007b6961165a56dd550d0f91861a2a0af01164` | untracked | `14bf3fb21f5936615cb23160a0651d850c6e80fc` | New |
| `??` | `Theory/Gates/VOR-001/HEALING_LENGTH_TEST.md` | 1,526 | `a003cf1b462cf62a41eae1a8d988a61bd4632aaa885ba4dd86a7962cfcf2adef` | untracked | `f3157dc1ea17b2a757f5dbcbd6f704b19a2abd02` | New |

Snapshot totals: **10 substantively modified tracked files**, **3 status-only
tracked paths whose normalized blobs match the index**, and **7 untracked
artifacts**. No path was staged.

## 4. Triangulated-audit prompt seals

Rule 9 mandates were hashed as UTF-8 before dispatch. Auditors are read-only.

| Role | Prompt bytes | SHA-256 |
|---|---:|---|
| A — mathematical/dimensional | 986 | `079b6422cdb09ee090e9fa3393d8afbdae2f0cc5a056bf1af8847247e6eddfae` |
| B — numerical/pipeline | 1,002 | `931d390d1f448c1e7459c4807d7115471194f0e076082d310aced78d672e283c` |
| C — claim/gate ledger | 1,165 | `dde3375145b5723c2adfc526017b8c1324e37564e0f681a52987b26db81057bf` |

The complete prompt texts remain in the execution transcript associated with
this G0 run. Their reports cannot change the repository or gate status; the
parent audit must reproduce and cross-reference every accepted finding.

## 5. Initial interpretation boundaries

- A dirty marker is not proof of a scientific or content change.
- A matching Git blob is evidence only that normalized content equals the
  index; the raw-byte hashes above still preserve the observed line endings.
- An untracked manuscript or gate note has no canonical authority merely by
  existing in a canonical-looking directory.
- This manifest records state; it does not adopt, repair, quarantine, or delete
  any pre-existing artifact.
- G0 files created after this snapshot are audit products and are intentionally
  absent from the pre-existing inventory.
