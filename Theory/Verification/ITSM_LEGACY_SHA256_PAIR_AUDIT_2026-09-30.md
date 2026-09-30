# Legacy SHA-256 pair audit — 30 September 2026

Status: `PROVENANCE_DIAGNOSTIC_ONLY`. This is an append-only inventory of
observed byte/hash disagreements. It is not a scientific gate report, a
security attribution, a Rule-9 review, or authorization to rewrite a receipt.
The original files and sidecars listed below were not changed by this audit.

## Scope and method

- Checkout: `recovery/v12-core-architecture` at
  `9f998adac904b9a5c9274e15fe5723c1111feb05`.
- Enumerated 453 repository-visible `.sha256` paths with
  `rg --files -g '*.sha256'`. This is not an audit of ignored or hidden local
  artifacts, the removable-drive copy, or the live GitHub remote.
- A *conventional pair* has exactly one `64-hex-digest  basename` record,
  and the file obtained by removing `.sha256` from the sidecar path exists
  with that basename. Digest letter case is normalized to lowercase for
  display below; SHA-256 was calculated over the file's current raw bytes.
  Of 357 such pairs, 339 matched and 18 did not.
- The other 96 paths were outside this narrow pair rule. Some sidecars are
  multi-target manifests or hash-only records; a missing implied stem is
  not necessarily a missing artifact. This audit makes no pass/fail claim
  about those 96 formats.
- For **each** of the 18 mismatches, the local source bytes and local sidecar
  bytes were separately compared with their exact Git `HEAD` blobs and
  matched. The disagreement is present in the committed checkout, not an
  uncommitted working-tree modification discovered in this session. Git
  history records bytes; this does not establish why they diverged or who
  caused it.

## Conventional pairs whose recorded hash does not match the file

The middle column is the digest **recorded in the existing sidecar**. The
next column is SHA-256 of the current file, which also matches that file's
Git `HEAD` blob. Commit columns are the latest commit touching the source
and sidecar, respectively; they are not an attribution of cause.

| Source path (append `.sha256` for its sidecar) | Sidecar digest | Current file digest | Last source / sidecar touch |
|---|---|---|---|
| `Theory/Verification/TRIANGULATED_CONSENSUS_SYNTHESIS_REPORT.md` | `0d3baa8ed0161d86813529d1ada72fba3ae0065a127bfec0801e24f50702da30` | `8147e99a32a02b3218030d79e31525acbe2a2cc16b3d7b35972f49e5b4fa5b9f` | `ca29a6e / ca29a6e` |
| `Theory/Verification/ROLE_A_MATHEMATICAL_DIMENSIONAL_AUDIT_REPORT.md` | `4dfc0989031f6b3bb733482c7a2e4ed2a983972712698d2fca033d69fdb2b94b` | `fd58ffd782460d8aded347176937aae90712a9c362d140b83da5b23c369c8890` | `ca29a6e / ca29a6e` |
| `Theory/Verification/ROLE_B_NUMERICAL_PIPELINE_AUDIT_REPORT.md` | `e4822919cb5e47f0001194bd99690752596c764fe97755c2860c78f54d7a84e6` | `64ca74427f15d177de779737485af786e19d84816561154c3b82c9058b9d66d4` | `ca29a6e / ca29a6e` |
| `Theory/Verification/ROLE_C_CLAIM_HYGIENE_GATE_LEDGER_AUDIT_REPORT.md` | `8f3a509e60b5d22c42d5976699195dc0fb7544a73f9bef920146386ee3e23f32` | `f327f34c793db6c38c6fc82386af8d3af1af18d2a7c8c3724bee67bc9962bc1c` | `ca29a6e / ca29a6e` |
| `Analysis/Astro/ASTRO-001/outputs/astro001_jeans_fragmentation_summary.json` | `4a5b4549df038a59617345f1da2c696601dfa64d52bf14b152b04028210623fe` | `ef87df449f2c426c2e44256abe78af871835537ec777a00a3cc3c3e17affdafb` | `a003e69 / a003e69` |
| `Analysis/Astro/ASTRO-001/outputs/astro001_genuine_excursion_set_summary.json` | `7f255d2da9add0f3e66d9701def3c960f41ed6459ea2f80192c69b9ac1ed049e` | `39936ae2186b51cde146101cbdeb2db2a6af5462613eb08bcadfe0abe781f69e` | `ca29a6e / ca29a6e` |
| `Analysis/Cosmology/COS-001/outputs/cos001_pert001_boltzmann_summary.json` | `2b011ee25c9b1b56565a5e4bd27e56a75c6b0ee888c28c4b9442fff35013b470` | `5aae14812c87770b4cc64905e38ab4957878fb3f28743dec1769ee0fee3a10e4` | `3640111 / 3640111` |
| `Analysis/Cosmology/COS-001/outputs/cos001_genuine_boltzmann_growth_summary.json` | `68a9f5a2657b031604b651aca2bf0c687456cf90ddbeb2a44672378e3187d542` | `c45ca1c54c2587af7fc3bf0b832c31fe61a19307ddb62d679f594df111543d64` | `ca29a6e / ca29a6e` |
| `Analysis/DISK/DISK-001/outputs/disk001_sparc_galaxy_pipeline_summary.json` | `370091055274c509ae9d73793104095f11672d4188d6c3f6574fdddd6e17fddc` | `ec6f554fb09c9186e32bbb4960796e453d8bf962dc239acb7a9e15bf6cc8e09d` | `6684eee / 6684eee` |
| `Analysis/DISK/DISK-001/outputs/disk001_sparc_multitier_mcmc_summary.json` | `6ac178d289dfc16f9acd1b32544f511c5d9255eae1bd880b4efe73ff92efdd46` | `8ab2992773a588b217b5ec77e62447f70a495a3e8192e7ac33cbd3f05e3d8788` | `ca29a6e / ca29a6e` |
| `Analysis/Lensing/LEN-001/outputs/len001_gravitational_lensing_summary.json` | `b78f1a98c2be77d604b631ff2ccc15ca114ab75f477ecb474437668ce80993e6` | `8cb80dedd79690fc6e70c1d8d2ec5b9e13aa0b51a40450c64fe30ebe5e16c54c` | `6684eee / 6684eee` |
| `Analysis/RES/RES-001/outputs/res001_lindblad_master_equation_summary.json` | `3990b572cdbaad69e0fae08fe9cb975d4edc3be0ddc005d01c8338f3d0c9e1e1` | `4963814475c68c6416dd6c5f505230bf5fdca45785caf199648c03c2c2076f7c` | `ab203ad / ab203ad` |
| `Analysis/Screening/SCR-001/outputs/scr001_landau_screening_summary.json` | `30bc66c6a228ea44478f55383490a50907e13a6ad58126cbb568033dc286f837` | `5c697bf2cc23f9016ecfad069e77ad0a6d72377100b10d6e1073478aab82d49b` | `6684eee / 6684eee` |
| `Analysis/VOR/VOR-001/outputs/vor001_s3_physical_defect_core_summary.json` | `4e58601ff5d5cecee26b152737553a862e54855ec9404dcc21238b86edb2e4f6` | `49c4d1f7daff04319efb4c0c31452eeb97410b32d00d8f3707918f3c6c2683b3` | `6684eee / 6684eee` |
| `Analysis/VOR/VOR-001/outputs/vor001_s4_physical_resonance_summary.json` | `079d8632eb9178add5e0df495bb13b5b0a65a9441080aa4ca3b67b09719c5751` | `99d213e25b8f43b656f42c85b2b92e83460c11da9249db88ba5bb974a08e68f2` | `6684eee / 6684eee` |
| `Analysis/WAK/WAK-001/outputs/wak001_bullet_cluster_summary.json` | `b03feeea89c29becf005d938eec995f25683906cf8740b1eaefa067fb11b90e1` | `f6164f98b0cd7329033ff993afc5a7f226492c2b46b32c0cc3b834eeb2b99d8d` | `cf5b7ae / cf5b7ae` |
| `Analysis/WAK/WAK-001/outputs/wak001_retarded_wave_lensing_summary.json` | `2758389a33f756f232bb62b1208f0df2972da652bbebdb2544f46321cc134a91` | `ecf834d7ae42d9e615e10ac2d588d9e05340ca9fd62a4f6f31892500a1e8e0b8` | `ca29a6e / ca29a6e` |
| `papers/P2-Rectangular-T3-Casimir/CBR001_CHECKSUMS.md` | `4b2af2c05f54c80bf201ec4f2dcfa7aa8547182c716d4cfc8a9d4571d3b89411` | `caf6825c35b60215ed36661707f803a6f8846535071083536db350284a319d36` | `202bcc2 / 5b52863` |

## Interpretation and containment boundary

Four older Rule-9 reports, thirteen older sector-output summaries and one
Casimir checksum document have failed their *conventional sidecar* check.
Those sidecars must not be cited as proof that their present source bytes
were sealed. The corresponding source content is still inspectable, but
scientific claims require their owning gate evidence and separate review.
No cause, motive, or intrusion is inferred from these mismatches.

The separate current R4C1-T2P3 check found 23 unique pinned paths matching
their recorded bytes/sidecars at audit time. That bounded result does not
validate all 453 repository-visible sidecars or upgrade T2P3 to a physical
weak-field solution. T2P3 remains provisional and uncommitted.

No original source, historical receipt, sidecar, gate report or claim status
is repaired or changed here. Any future correction should be versioned and
compared with the preserved Git history and, if the operator elects, the
separately held offline copy. This note does not change `physics_pass=false`,
`MAT-001=BLOCKED`, `UVIR-003=IN_PROGRESS`, `K_Q=NOT_DERIVED`,
`V=NOT_COMPUTED`, `Stage4A=CLOSED` or deferred Rule-9 clearance.
