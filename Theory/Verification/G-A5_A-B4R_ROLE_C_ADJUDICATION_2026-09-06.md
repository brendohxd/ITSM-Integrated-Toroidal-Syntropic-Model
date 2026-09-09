# G-A5 / A-B4R Role-C adjudication

**Date:** 2026-09-06  
**Branch:** `recovery/v12-core-architecture`  
**Role:** Codex parent / Role C — claim hygiene, verifier repair and gate reconciliation  
**Status:** `ADJUDICATED_WITH_LOCAL_VERIFIER_REPAIR_AND_INDEPENDENCE_HOLD`  
**Gate effect:** none  
**Commit/push/publication:** not performed

## 1. Decision

The two external packages do not establish an action freeze or a physics-gate
pass.

1. Grok `G-A5` supplies a useful negative/narrowing result. The mixed
   quartic-sextic parent approaches the `3/2` phase-EFT exponent only in the
   sextic-dominated regime. A symmetry-allowed quartic generically restores
   quadratic behaviour in the infrared. The pure-S6 shape is therefore
   classified as `S6_SHAPE_CONDITIONAL_ON_UNPROTECTED_TUNING`.
2. The completed Antigravity `A-B4` report is rejected because its candidate
   had a wrong low-`k` `k^4` sign, did not assert convergence to that
   coefficient, retained a literal stability boolean, used Hamiltonian mixing
   signs inconsistent with its displayed Lagrangian, and overclaimed source
   provenance.
3. A genuinely fresh Antigravity attempt was started, corrected several of
   those issues and then failed first on a LaTeX-to-SymPy parser defect and
   subsequently on repeated model-stream interruptions. It returned no
   complete report or sealed manifest.
4. Codex, as the repository-writing parent, constructed and audited a new
   versioned verifier without replacing the original baseline. The local v2
   checker passes 32 semantic checks, two isolated runs are byte-identical,
   and all nine declared scientific/filesystem mutations are detected.
5. The Codex result is accepted as a local verifier repair. It is not presented
   as independent Role-B confirmation. Rule-9 triangulation therefore retains
   an independence hold.

The binding scientific boundary remains:

- `MAT-001 BLOCKED`;
- `UVIR-003 IN_PROGRESS`;
- `K_Q NOT_DERIVED`;
- `V=C_m/sqrt(K_Q) NOT_COMPUTED`;
- RCP-2/U5/M4 coupled metric work is not opened;
- downstream screening, PPN, lensing, disks and cosmology cannot inherit a
  pass.

## 2. Sealed intake and provenance

| Artifact | SHA-256 | Disposition |
|---|---|---|
| Grok `G-A5` sealed handoff | `c1eab2753795bc97a6984539c94f03a3b049f4de1c6b9fb9c2248eaf269bdec2` | Manifest match |
| Grok exact report body | `2a884460cbd702af373f34e230217f7de6ec42b647f3ce3e9b4e76b9cec0ed65` | Independently reproduced from returned text |
| Grok complete assistant content | `2a528b148641e233476b2ae13e326d6d85984f841e98472aa05e4ec855812966` | Reviewed |
| Antigravity `A-B4` sealed handoff | `d49b2263076f6929da2ec415ab44cd5a03f63d1708e4cd42bcf9afa9e9f7177d` | Manifest match |
| Rejected old-session Antigravity candidate | `5dbffea8b5d38cc24ce9b775464bf268e0d4a98ddc5b8e96bf3cb20a5996b653` | Not imported |
| Rejected old-session Antigravity complete response | `c3ebc4be943c979ef7e41a90b3196aefe7dfe3cb4f653b36ce8070a711943f67` | Reviewed; claimed report-body hash did not reproduce from delivered text |
| Interrupted fresh-session Antigravity draft | `50c0d2bbbe6fbe978bd8b47fbf1ad15e279e491fe2be694722a8e4b3b0ac2d0e` | Temporary untrusted draft; not imported |
| Codex v2 semantic verifier | `3c6b3e1706ea3a067932bc81c4495299e412c8aad61a405bac4b4078e687b851` | Accepted local candidate tooling |
| Codex v2 isolated audit harness | `618a8ba6441c8e2183c1223ab4709ea1462c66e1f529c8bf63ea17061e8ad128` | Accepted local audit tooling |
| Codex v2 semantic summary | `a5d06aa4207ca19164dc3c66d8bfef17ad950775ab683948c8203232b90cb13b` | Two isolated runs byte-identical after final dashboard reconciliation |
| Codex v2 audit manifest | `97bfb500674e08d44450347385b8c3842c910f4baa4d7a3c77ad2582b38d77c1` | Reviewed after final dashboard reconciliation |

Hash equality proves artifact identity and deterministic reproduction. It does
not establish a physics pass or external reviewer independence.

## 3. G-A5 mathematical adjudication

For

\[
U(s)=m^2s+\frac{\lambda_4}{2}s^2+\frac{\kappa_3}{3}s^3,
\qquad \kappa_3>0,
\]

the positive algebraic branch obeys

\[
X_R-m^2=\lambda_4s+\kappa_3s^2
\]

and

\[
P=\frac{\lambda_4}{2}s^2+\frac{2\kappa_3}{3}s^3.
\]

The effective exponent is

\[
p_{\rm eff}
=\frac{d\ln|P|}{d\ln|X_R-m^2|}
=\frac{6(\lambda_4+\kappa_3s)}{3\lambda_4+4\kappa_3s},
\]

so

\[
p_{\rm eff}-\frac32
=\frac{3\lambda_4}{2(3\lambda_4+4\kappa_3s)}.
\]

Consequently:

- `4 kappa_3 s << 3 lambda_4` gives `p_eff -> 2`;
- `4 kappa_3 s >> 3 lambda_4` gives `p_eff -> 3/2`;
- exact `3/2` at finite `s` requires `lambda_4=0` in this truncation;
- global `U(1)` does not forbid `s^2`, so a pure sextic action is not protected
  by the declared symmetry;
- a natural order-one quartic and `kappa_3~1/Lambda_W^2` push sextic dominance
  outside `s<<Lambda_W^2`;
- a loop-sized quartic can leave a mathematical strip, but that strip is a
  tuned, UV-dependent control rather than a naturalness-closed parent.

### Corrections to the returned G-A5 text

1. The statement that `m^2s` removes the constant phase-shift symmetry is
   false. Global `U(1)` is the exact constant shift
   `Theta -> Theta + constant`; it simply does not forbid `s^2`.
2. The one-vertex self-contraction of a sextic vertex that generates a quartic
   counterterm is a tadpole/self-contraction, not a bubble.
3. The listed dimension-six operators form an unreduced inventory. Integration
   by parts and equations of motion must be applied before claiming an
   independent operator basis.
4. Fixed-charge and fixed-chemical-potential local spectra agree only with the
   stated nonzero-mode/global-constraint qualification. Their homogeneous
   modes are not interchangeable.

These corrections do not overturn the naturalness disposition.

## 4. Why the completed external A-B4 classification was rejected

The exact lower branch

\[
\omega_-^2=k^2+\frac{M_H^2}{2}
-\frac12\sqrt{M_H^4+16\mu^2k^2}
\]

has expansion

\[
\omega_-^2
=\frac{M_\sigma^2}{M_H^2}k^2
+\frac{16\mu^4}{M_H^6}k^4+O(k^6).
\]

The completed external candidate instead set the `k^4` coefficient negative.
Its reported numerical slopes approached `+0.128`, while its prose declared
`-0.128`; its pass condition checked only monotonic convergence toward the
sound-speed term. The same candidate assigned
`stability_domain_proven=True` instead of executing a symbolic proof. Its
Hamiltonian matrix corresponded to the opposite mixing orientation from the
displayed `+2 mu sigma q_dot` Lagrangian. Its provenance predicate checked
only file existence rather than sealed expected hashes.

Detecting the eight mutations supplied in the old report could not validate
scientific properties those mutations did not test.

## 5. Parent-repaired v2 verifier

The original v1 checker and its output are preserved unchanged. The new files
are:

```text
Analysis/MAT/MAT-001/M2M3_U1/
  m2m3_u1_fixed_background_checks_v2.py
  m2m3_u1_fixed_background_checks_v2.py.sha256
  m2m3_u1_verifier_v2_audit.py
  m2m3_u1_verifier_v2_audit.py.sha256
  outputs/m2m3_u1_fixed_background_summary_v2.json
  outputs/m2m3_u1_fixed_background_summary_v2.sha256
  outputs/m2m3_u1_verifier_v2_audit_manifest.json
  outputs/m2m3_u1_verifier_v2_audit_manifest.sha256
```

### Measured execution results

- Original v1 baseline: two successful isolated runs; both summaries retained
  SHA-256
  `391fcb099453ae493056c786b6f784b857d2b2f0a8f2626c8ed161cdc0f77c10`.
- Candidate v2: `32/32` declared checks passed in each isolated run.
- Candidate v2 output: both runs produced SHA-256
  `a5d06aa4207ca19164dc3c66d8bfef17ad950775ab683948c8203232b90cb13b`.
- Complete output trees matched byte-for-byte before mutation.
- All copied source files matched their repository source hashes.
- Independent Hamiltonian-root relative differences were at most
  `2.462e-89` on the five predeclared rational triples.
- At `M_sigma=mu=1`, the measured `k^4` estimate converged monotonically from
  `0.127592031095...` at `k=1e-1` to `0.12799999999995904...` at `k=1e-6`,
  toward the exact positive value `0.128`.

### Mutation results

| Mutation | Scientific/filesystem object changed | Detected |
|---|---|---|
| `MUT_01_KINETIC_MIXING` | `2 mu` changed to `mu` in the Hamiltonian matrix | yes |
| `MUT_02_DELETE_SQRT2_SOURCE` | canonical source lost `sqrt(2)` | yes |
| `MUT_03_DIMENSION_R_POWER` | `rho R^2/Lambda^2` changed to `rho R/Lambda^2` | yes |
| `MUT_04_REVERSE_GRADIENT_SIGN` | physical `k^2` sign reversed | yes |
| `MUT_05_SPHERE_NUMERATOR` | uniform-sphere numerator coefficient changed | yes |
| `MUT_06_SIDECAR_BYTE_MUTATION` | one real output byte changed on disk | yes |
| `MUT_07_EXTRA_RUN2_FILE` | real extra file added only to run 2 | yes |
| `MUT_08_MARKDOWN_FORMULA` | parsed radial-mass formula changed in copied report | yes |
| `MUT_09_REVERSE_K4_SIGN` | positive exact `k^4` coefficient reversed | yes |

The bounded local tooling classification is:

`VERIFIER_V2_CANDIDATE_COMPLETE_ALL_PREDECLARED_MUTATIONS_DETECTED`.

This is a calculation/verifier classification only.

## 6. Action-class and reasoning decision

The present pure-S6 parent does not satisfy the frozen RCP-2 entry conditions:

- the lower-order operator hierarchy is not symmetry-protected;
- the on-shell gravitating finite-density background remains unspecified;
- the matter interface and its physical normalization remain free;
- the complete EFT/strong-coupling domain is not fixed;
- no signed metric-reduced pole residue exists.

Therefore do not spend the Ultra coupled-calculation budget on this action as
currently written. Retain it as a conditional tuned control and possible
classification/no-go result. A later distinct action may reopen RCP-2 only if
it supplies an explicit symmetry or UV matching mechanism that controls the
quartic and derivative operators without using observational targets.

## 7. Next ordered work

1. Complete the independent P2 Casimir/backreaction reproducibility and
   hostile manuscript freeze. It does not depend on MAT-001 and remains the
   closest bounded publication candidate.
2. Run the exact winding/phase-normalization audit as a separate topology
   result. Do not join it to a force coefficient until a parent survives.
3. If Route 1 continues, specify a new symmetry/UV-complete parent at High and
   perform its blind Max parent-to-EFT reduction before any Ultra work.
4. Seek fresh external Role-B confirmation of the v2 verifier only when a
   stable, compact execution channel is available. Do not treat that repeat as
   a prerequisite for using the local checker as internal tooling.

## 8. Explicit non-claims

This adjudication does not derive a spatial `Y^(3/2)` force action, nonlinear
screening law, `K_Q`, `V`, `a_0`, topology coefficient, PPN parameter, lensing
potential, SPARC prediction, cosmological solution or publication-ready ITSM
core theory.
