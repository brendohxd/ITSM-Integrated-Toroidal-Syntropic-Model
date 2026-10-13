# Local paper release package manifest — 1 October 2026

This directory contains self-contained source bundles prepared during the
five-paper completion pass. Each bundle was compiled successfully from its
staged contents before archiving. This is a local QA and handoff record, not a
submission, publication, external-review clearance, or canonical scientific
promotion.

## Manuscript PDFs

| Paper | Status | Canonical PDF | Bytes | SHA-256 |
|---|---|---|---:|---|
| P1 scale matching | local release candidate | `../../P1-Scale-Matching-Reconstruction/Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc1.pdf` | 626748 | `ab013e05fd96d769a1f0aa663994c0e0a59ca647e503377b4566f12a8215b340` |
| P2 rectangular Casimir | local release candidate; sensitivity hold remains | `../../P2-Rectangular-T3-Casimir/Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control_v0.2.0-rc1.pdf` | 936475 | `eb2b99d1845207763b8d8ae8cd0b04e9381f7c3e68727ff6f143c3fdd067036e` |
| Syntropic thermodynamics | conditional draft | `../../Syntropic-Thermodynamics/Boyd_2026_Covariant_Entropy_Accounting_Interacting_Sectors_v0.7.0-conditional-draft.pdf` | 459249 | `e5fa68ed04dc776b409f805d6cc6dccbe5b1e1015adc2056726d932f6bba24ea` |
| R4C1 exchange model | conditional draft | `../../R4C1-Covariant-Exchange-Model/Boyd_2026_Covariant_Finite-Density_Exchange_Model_v0.1.0-conditional-draft.pdf` | 486430 | `e764a34801f4c7b1c6bc36b2fc7183fdee103cf40ef413062821989364d05480` |

## Self-contained source bundles

| Bundle | Bytes | SHA-256 |
|---|---:|---|
| `P1_Scale_Matching_v0.2.0-rc1-source.zip` | 76041 | `b425a02a33640ddbfc22d403d712b6b3ad9b0f719166768713580515697fcfd2` |
| `P2_Rectangular_T3_Casimir_v0.2.0-rc1-source.zip` | 357709 | `e22c8773859d82374b84314e1f4ba463117d9f1be530902c071a8fe2fe265bc9` |
| `Syntropic_Thermodynamics_v0.7.0-conditional-draft-source.zip` | 11458 | `d0b6ae5802e018e95f857d255249784a4093871edbfc560820a98c47c05272d6` |
| `R4C1_Covariant_Exchange_v0.1.0-conditional-draft-source.zip` | 19890 | `62f77086dacf7d1f5ca7f7a6ed42e420d5ca144b340883222c991679d3884433` |

Every ZIP has a matching `.sha256` sidecar. The canonical PDFs retain their
own adjacent `.sha256` sidecars.

## Scientific status boundary

- **P1:** publication-facing local release candidate; independent/external
  review and human submission remain open.
- **P2:** the independent static benchmark is included, but the preregistered
  release-sensitivity aggregate is `18/19`, `physics_pass=false`; the failed
  threshold-amplitude precision criterion remains a substantive publication
  hold even though the no-attractor classification is stable.
- **Thermodynamics:** the covariant entropy-accounting identity is derived
  conditionally; thermodynamic stability, dissipative closure, and acceleration
  are not established.
- **R4C1:** the finite-density action and exchange-current construction is
  explicit, but the physical scalar EFT, derived weak-field normalization, and
  cosmological closure remain open.
- Outstanding Rule-9 review is recorded as deferred under repository policy;
  it does not block provisional research, but external review is still required
  before publication-ready promotion.
