# Local Rule-9 TOP-X4/BBN evidence and review packet

**Date:** 2026-09-16  
**Branch:** `recovery/v12-core-architecture`  
**Packet status:** `READY_FOR_INDEPENDENT_REVIEW_ONLY`  
**Rule-9 status:** `THREE_WAY_CLEARANCE_NOT_MET`  
**External review dispatch:** `NOT_PERFORMED`

## 1. Purpose and binding boundary

This is a local evidence-preparation packet for independent review of
the current TOP-X4 and BBN-001 recovery boundaries. It is not a review
report, a consensus record or a publication package. The historical
triangulated synthesis listed below is context only and does not clear
the current TOP-X4/BBN receipts.

The packet preserves `MAT-001=BLOCKED`, `K_Q=NOT_DERIVED`,
`V=NOT_COMPUTED`, `UVIR-003=IN_PROGRESS`, BBN-001's control/upstream
hold, `physics_pass=false` and `gate_effect=NONE`. No independent
reviewer has been assigned by this artifact.

## 2. Review protocol

- Frame: assign one reviewer to each role and provide this manifest and the listed artifacts.
- Compare: each role independently checks its prompt, hashes and bounded results, then records disagreements.
- Decide: only after all three reports are present may the roles be cross-checked against canonical sources; this packet itself cannot clear Rule-9.

## 3. Role-separated review prompts

| Role | Reviewer | Report | Prompt |
|---|---|---|---|
| Role A — Mathematical and dimensional auditor | `NOT_ASSIGNED` | `NOT_RECEIVED` | Independently inspect the frozen actions, operator conventions, dimensions, state boundaries, BBN field semantics and the Dirac/parity/anomaly contract. Recompute or symbolically check any claimed bounded identity that is in scope. Identify missing operator, phase, spin-structure, anomaly or unit information. Do not infer a value and do not promote any gate. |
| Role B — Numerical and pipeline auditor | `NOT_ASSIGNED` | `NOT_RECEIVED` | Independently replay the registered executables, verify JSON byte identity and SHA-256 sidecars, and exercise the declared negative/rejection controls. Check that the BBN preflight is presence-only and that the TOP-X4 readiness audit does not silently substitute static, finite-order or parity-even data. Report environment limits and any mismatch; do not repair or reinterpret a failing receipt inside the review. |
| Role C — Claim-hygiene and gate-ledger auditor | `NOT_ASSIGNED` | `NOT_RECEIVED` | Compare the receipts against the canonical identity, active research dashboard, recovery queue and publication firewall. Check every Derived/Conditional/Open/Rejected boundary, the BBN CONTROL_ONLY and upstream hold, TOP-X4 physics_pass=false, and the absence of Rule-9 self-certification. Flag any status divergence or downstream claim. Do not clear Rule-9 without independent Role A and Role B reports and a final cross-check. |

No role is self-certified here. A missing report is a failed Rule-9 prerequisite, not an implied pass.

## 4. Unresolved questions

- The Hamiltonian-form curved five-dimensional Dirac operator and homogeneous spin connection are now derived on the registered metric; can this be extended to the complete finite-charge background, state domain and normalization required by the determinant?
- What dimension-appropriate infinite-order Dirac Hadamard construction supplies the state and wavefront conditions required for stress renormalization?
- What regulator/reference phase and spin-structure data define the parity-odd determinant, including any spectral-flow or global contribution?
- Which local/global anomaly terms occur for the frozen field content, and what quantized counterterms cancel them without importing an external result?
- Can the BBN interface receive physical T_gamma, dT_gamma/dt, T_nu, H, baryon normalization, plenum density, Q_mp^mu, Q_syn^mu, S_N, G_eff and perturbation matching from one action-derived chart?
- Have all receipt hashes, sidecars and role-separated reports been independently compared against the current canonical documents?

## 5. Current status firewall

| Item | Binding status |
|---|---|
| `MAT-001` | `BLOCKED` |
| `K_Q` | `NOT_DERIVED` |
| `V` | `NOT_COMPUTED` |
| `UVIR-003` | `IN_PROGRESS` |
| `BBN-001` | `CONTROL_ONLY_AND_BLOCKED_UPSTREAM` |
| `TOP-X4` | `PHYSICS_PASS_FALSE` |
| `physics_pass` | `false` |
| `gate_effect` | `NONE` |
| `publication_status` | `NOT_A_PHYSICS_CLAIM_FOR_THIS_PACKET` |
| `external_review_dispatch` | `NOT_PERFORMED` |

No BBN input, `Q^mu`, `S_N`, `G_eff`, perturbation matching, Dirac completion, parity phase, anomaly cancellation, quantized counterterm, determinant, stress, physical Hessian, gate promotion or publication claim is inferred from this packet.

## 6. Authoritative source documents

| Label | Path | SHA-256 |
|---|---|---|
| Core operating rules | `GEMINI.md` | `5660cd00371b51566c63d07bcaed76b443c450220fc9ff5269fb61635fe183e7` |
| Canonical identity briefing | `Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md` | `3edb52a2c200f18059aa716aacc9b125a2c7b80f2b95086519ba260c443b9a5c` |
| Master research plan | `Theory/Core/ITSM_Master_Research_Plan.md` | `9260f49780e644c418545a88e59b5273f5fbcc088a1b6c2aaa1016e34461ac74` |
| Recovery execution queue | `Theory/Core/ITSM_Recovery_Execution_Queue.md` | `55f8b636f20563646b2dab17550ec0689a7d37414f2fb90a7250038a2b5687f7` |
| Active research dashboard | `active_research.md` | `d0e8c4695eb26c5cde4c00ec2f66777613995875cf5ac16460318e3fa90e6b4e` |
| Recovery branch guide | `RECOVERY_BRANCH_README.md` | `9ea1c9a8fba7292a2fa25822ac70370dbd175caf6e5ddcf279656458b4d2cff4` |
| TOP-X4 Plan 11 parent freeze | `Theory/Gates/TOP-X4/TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md` | `37205506697e1f70f12b9ea3d8b093ccbccf11bbf0c19b680d00a43f28c6f945` |
| TOP-X4 Plan 11 calculation plan | `Theory/Core/Reasoning_Mode_Plans/11_MAX_TOPX4_S2F3_SEMICLASSICAL_STABILIZATION/PLAN.md` | `a935fbb4b2cc2206ed7a22910716203e427071e21d347214b59fea62bdc9c73f` |
| TOP-X4 Dirac/parity/anomaly contract | `Theory/Gates/TOP-X4/TOPX4_S2F3_DIRAC_PARITY_ANOMALY_READINESS_CONTRACT_2026-09-16.md` | `d49da5217c1078467424af3210c4f983db2f9d73195185b486bab9628c8a14f8` |
| TOP-X4 scoped curved Dirac-operator contract | `Theory/Gates/TOP-X4/TOPX4_S2F3_CURVED_DIRAC_OPERATOR_CONTRACT_2026-09-16.md` | `65280699a5e641d2ffcc61fc4e97d1b28670cbcf9256330184d7c3d1593809b6` |
| BBN-001 action-derived input contract | `Analysis/Cosmology/BBN-001/bbn001_action_derived_input_contract.json` | `b92161b4db0989b8712480c91add05e8c60ec497e6d41c865308efe1a1883768` |

## 7. Authoritative receipt manifest

All receipt entries below require a matching `.sha256` sidecar. `sidecar_matches` is recorded in the machine-readable manifest.

| Label | Path | SHA-256 | Sidecar |
|---|---|---|---|
| TOP-X4 static determinant JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_static_determinant_summary.json` | `b2addbfc34f6e3aec3fc0141342f30de4d56cb31a5dff37c59d7ff15281e493a` | `MATCH` |
| TOP-X4 static determinant receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_STATIC_CHECKPOINT_RECEIPT_2026-09-09.md` | `32365e16dbccf9709682b7202fb43cb0c1215ba2bd624b13a82aafe16e504317` | `MATCH` |
| TOP-X4 finite-charge operator JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_finite_charge_operator_summary.json` | `b2440221e9bfd5bcd56a40f29e3a731b0fbd44d43d2ab86ef7f300e7c121c4e6` | `MATCH` |
| TOP-X4 finite-charge operator receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_FINITE_CHARGE_OPERATOR_CHECKPOINT_2026-09-12.md` | `9444089b268f8093595e256b0a882185ef18812cd2ab50a0ac26b01ca1ddd1a6` | `MATCH` |
| TOP-X4 dynamic state JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_dynamic_state_subtraction_summary.json` | `8e920c5e699b898891fca1dc6ade0edb5359fefbaaed785698e88c8109d4280b` | `MATCH` |
| TOP-X4 dynamic state receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_DYNAMIC_STATE_SUBTRACTION_CHECKPOINT_2026-09-12.md` | `c5de6ec4f180d5781d095db427308cb73b50712299e789572cee657502fe88a9` | `MATCH` |
| TOP-X4 exact transport JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_exact_transport_retry_summary.json` | `94ca65dd08419b650a8a135ddc5e7a6adf550ef788ee7a8759fa143786315747` | `MATCH` |
| TOP-X4 exact transport receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_EXACT_TRANSPORT_RETRY_CHECKPOINT_2026-09-12.md` | `5b58d5ae4b7dfcf7c15e9ac53679cb1cb5babb595ca864881e9f28abe8b17f59` | `MATCH` |
| TOP-X4 D5 readiness JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_hadamard_subtraction_readiness_summary.json` | `95395d22a459b72423ce8c1cb2df35e0d42f76581a3a339cbc0d5acf2e50ab90` | `MATCH` |
| TOP-X4 D5 readiness receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_HADAMARD_SUBTRACTION_READINESS_2026-09-12.md` | `9c7e4f3001382b7b37e0e737d1249d641c6ba1df6cf1e4e1e56af0700a8865ec` | `MATCH` |
| TOP-X4 covariant scalar JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_covariant_scalar_matrix_summary.json` | `c7f9b3e9d4f00c99df93f25b8d9eccf9162472fc3c66ee26fe19c43f389dd777` | `MATCH` |
| TOP-X4 covariant scalar receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_COVARIANT_SCALAR_MATRIX_CHECKPOINT_2026-09-12.md` | `8f96b809710aec90e1b6a6dc044e3f77542be26b34404af4304edfa62d7b58d9` | `MATCH` |
| TOP-X4 scalar parametrix JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_scalar_matrix_hadamard_parametrix_summary.json` | `becaa3ef1ce19a8545335c49b868cc3479fcf1a7b4044ac1cda7f939fbfadc08` | `MATCH` |
| TOP-X4 scalar parametrix receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_SCALAR_MATRIX_HADAMARD_PARAMETRIX_CHECKPOINT_2026-09-12.md` | `af0a02ad844f6eba1ac51c6fd46309645ac458e3f0a79b71bba4d6f1446405e9` | `MATCH` |
| TOP-X4 global scalar state JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_global_state_construction_summary.json` | `fef8df00183333cc6fb18382c77fab397cd7c2caf740752d6c29ebf36da44428` | `MATCH` |
| TOP-X4 global scalar state receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_GLOBAL_STATE_CONSTRUCTION_2026-09-16.md` | `ccef90d07ec2606f850c096f08e8498f312e63fae3d38d3156599a27169794f4` | `MATCH` |
| TOP-X4 physical Hessian JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_physical_hessian_readiness_summary.json` | `557e7b4ae7ddfb3402e15aa72eaf829b695446c7681964d3b9870b60ad434950` | `MATCH` |
| TOP-X4 physical Hessian receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_PHYSICAL_HESSIAN_READINESS_2026-09-16.md` | `d0dc919881e48bcd74b7ae9076987d8932a0bdcd32687e3b54aa1f6f6b728a64` | `MATCH` |
| TOP-X4 Dirac/parity/anomaly JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_dirac_parity_anomaly_readiness_summary.json` | `a87901a070b0d9d81aaea599c6075bc06a6900da8df2a4d4d73ee5e60749d4a9` | `MATCH` |
| TOP-X4 Dirac/parity/anomaly receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_DIRAC_PARITY_ANOMALY_READINESS_2026-09-16.md` | `c65e8891e9ff4b2ba9ec238a523c58036c8e0e5895426c387d8121828863d700` | `MATCH` |
| TOP-X4 scoped curved Dirac-operator JSON | `Analysis/TOP/TOP-X4/outputs/topx4_s2f3_curved_dirac_operator_summary.json` | `54364768bfa4008f587011e8f1cc82effe6aa0facbab55e7f5808bc6bea9adb2` | `MATCH` |
| TOP-X4 scoped curved Dirac-operator receipt | `Analysis/TOP/TOP-X4/TOPX4_S2F3_PLAN11_CURVED_DIRAC_OPERATOR_2026-09-16.md` | `eaa917479f80893d883c17c6a56170f4b6a523310ace1b5b9e45f430fa8fd26b` | `MATCH` |
| BBN-001 upstream preflight JSON | `Analysis/Cosmology/BBN-001/outputs/bbn001_upstream_interface_preflight_summary.json` | `b7a102b2531d7dbbc75eef2d3fc3a418ec445ff54a59426a95f6499295d7fd02` | `MATCH` |
| BBN-001 contract validation JSON | `Analysis/Cosmology/BBN-001/outputs/bbn001_action_derived_input_contract_summary.json` | `54273901f9d91a487c5e94919cc193130e5b1e48c492abc324ed4c4f75ef90e7` | `MATCH` |

## 8. Historical context (not current clearance)

The following document records an earlier audit context. It is not treated as independent review of the current TOP-X4 or BBN packet:

| Label | Path | SHA-256 | Sidecar |
|---|---|---|---|
| Historical Rule-9 synthesis (context only; not current TOP-X4 clearance) | `Theory/Verification/TRIANGULATED_CONSENSUS_SYNTHESIS_REPORT.md` | `8147e99a32a02b3218030d79e31525acbe2a2cc16b3d7b35972f49e5b4fa5b9f` | `MATCH` |

## 9. Final decision

```text
THREE_WAY_CLEARANCE_NOT_MET
physics_pass=false
gate_effect=NONE
external_review_dispatch=NOT_PERFORMED
```

This packet is complete only as a local handoff surface. It must not be cited as Role A, Role B or Role C review, and it must not be used to promote any scientific or publication gate.
