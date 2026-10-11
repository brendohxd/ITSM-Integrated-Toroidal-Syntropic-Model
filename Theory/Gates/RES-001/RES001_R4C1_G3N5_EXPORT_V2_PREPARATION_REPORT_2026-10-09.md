# G3N5 export v2 preparation: bottleneck located, full execution pending

Date: 9 October 2026. This is an implementation-preparation report, not a
scientific output receipt or a passing full-kernel calculation.
Status: EXPORT_IMPLEMENTATION_PREFLIGHT_PASS_FULL_EXECUTION_NOT_RUN.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## Evidence and bounded change

The original v1 worker remains active at the latest session poll with no
terminal result and no attempt-01 summary. All three read-only stack samples
located the same scientific call site: `derive` line 274, exporting quadratic
sector expressions through `tidy` line 42, inside SymPy multivariate
factorization. A stack location proves an implementation stage, not the
outcome of any scientific assertion or independent control.

The [frozen v2 addendum](RES001_R4C1_G3N5_EXPORT_V2_ADDENDUM_2026-10-09.md)
permits exact expanded serialization rather than factorization solely for
printing. The separately created v2 source is
`Analysis/MasterTests/test_01_r4c1_g3n5_response_kernel_v2.py`, SHA-256
7321e53304864f0832a3e5a6ce3fce5dc2d156d3fa12d29df267b93910730b3f.
The addendum SHA-256 is
fbd2a6085c0b2909a1549bb0bbefe32ed87696f124cb4778e797d7659990e7f0.
Both have new matching sidecars. The v1 source still hashes to
0863c4b150a3184d152263da2fa65f4f50f5b344653294cf8fc99326b62295f7.

Each export is reconstructed exactly from its printed additive terms and
must reproduce both the symbolic expression and its canonical expanded
string. The audit retains those terms, the expression hash and term count.
This avoids both generic factorization and a huge left-associated parser
tree. It changes representation, not equations, domain or acceptance rules.

## Actually executed implementation checks

- AST parse succeeds for v1 and v2.
- ASTs match for all ten unchanged helper functions/classes: tidy, Jet2,
  zeros, mm, trace, scalar, exact, numeric_inputs, raw_analytic, independent.
- Every `derive` statement before its export block matches exactly.
- FIELDS, COORDS and M_NAMES definitions match exactly.
- A rational 110-variable polynomial and zero expression both reconstruct
  exactly while SymPy factorization is deliberately prohibited in this
  small serializer test. This is not the full 110-jet scientific kernel.
- All 130 input source pins and 127 available sidecars match. The three
  previously declared missing sidecars remain missing and explicit.

No full v2 derivation, unexpanded-density comparison, response solve or
exact output replay has been executed. No full-kernel PASS is claimed.
The previously checked temporal block remains 54/54 on its own boundary;
it has not been compared with either full-kernel result.

## Execution choice and next work

The operator has been asked whether to stop only the original export-bound
calculation and run the corrected version, or keep the original alive.
No stop or second expensive run was performed while that choice is pending.
This replaces blind waiting with a diagnosed, scope-preserving alternative,
not a restart merely because an observation window elapsed.

After an execution decision, inspect the full result and every failed or
unknown check, preserve the attempt, and replay successful outputs exactly.
Use a new versioned temporal comparator for the v2 source pin if v2 is used;
do not rewrite the existing temporal receipt. Then proceed to compatible
constraints, initial data and coupled response with homogeneous data and
the unsmoothed force/harmonic tail retained. The goal remains full nonlinear
constrained evolution, not a replacement by this unreduced kernel.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
All earlier failures and review dependencies are inherited. No original
scientific source, receipt or frozen sidecar was edited. No manuscript/PDF,
vault, provider, runtime configuration, commit, push, promotion or publication
change was made. The goal remains active and incomplete.
