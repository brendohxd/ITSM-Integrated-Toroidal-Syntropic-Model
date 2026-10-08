# R4C1-G3V: supplemental constrained-regularity cross-check

Date: 8 October 2026. Scope: frozen G3V prerequisite, not full scattering.
Claim Conditional; research PROCEED_PROVISIONALLY; review DEFERRED.
physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## Disposition

The original implementation passes 379/379 local checks. The separate
implementation passes 376/376 local checks. Both replay their own sealed
JSON artifacts byte-for-byte. Their shared six coefficients agree over all
216 archived chart events: 1,296 comparisons, maximum normalized difference
1.1102230246251565e-16. Check counts are not summed or called physics closure.

The surviving force interaction is C2 but not C3 on the tested transverse
direction at the homogeneous origin. Regular first-order auxiliary
elimination does not remove its leading even cubic-amplitude cusp within
the declared nonzero-mode domain. Ordinary full trilinear Taylor scattering
on this background remains HOLD_SUBSTANTIVE. This does not establish a
classical-evolution no-go, quantum inconsistency, or an all-action no-go.

This is a second local implementation by the same agent using the same
archived backgrounds, not an independent Rule-9 reviewer or new data fit.

## Governing evidence

- [Frozen G3V contract](RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_CONTRACT_2026-10-08.md):
  SHA-256 53940518eeff7ca46fb5a9373db6e4637360eeedaeffcba6044af5cc580ac3ac.
- [R4C1 action freeze](RES001_R4C1_ACTION_FREEZE_2026-09-25.md):
  SHA-256 81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3.
- [Original frozen G3V report](RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_REPORT_2026-10-08_v1.md):
  SHA-256 952b4315a5607358a4fc0250a9ab67efc90577dda77f006b357fc1cbd74eeb27.
- [Earlier integrity addendum](RES001_R4C1_G3V_SOURCE_INTEGRITY_ADDENDUM_2026-10-08.md):
  SHA-256 6bd6808e2240354fd29b7204215e3bf0a33f53a109035afb0ed41d88b8a11834.

The new receipt pins its direct and inherited sources. No action, parameter,
background trajectory, frozen sampling domain, or old result is retuned.
The original failed 112/113 background derivative assertion remains
preserved; its later refinement has its own bounded evidence.

## Calculation and limits

The cross-check reconstructs the metric connection, four frame invariants,
projector, transverse metric-shift constraint, quadratic mass terms and
Euler-Lagrange equation. The homogeneous dust lapse constraint imposes
delta N=0 at first order. The nonzero-mode shift elimination retains the
metric contribution to the gradient weight; it is not a fixed-metric probe.

For p=dot(psi) and f^2=M_U^2(c1+c4), the proper-time transverse field
w has canonical comoving field X=a^(3/2) f w. In the frozen G3 family,

\[
c_V^2=\frac45+\frac{3\eta}{8(8-\eta)},\qquad
m_w^2=2(\dot H+H^2)-18p^2+\frac{6J_0^2}{13},
\]
\[
m_X^2=\frac{\dot H}{2}-\frac{H^2}{4}
      -18p^2+\frac{6J_0^2}{13}.
\]

These mass expressions use the frozen reduced-Planck-unit chart and
constant f. Their agreement is not an all-mode stability certification.
The shift denominator and nonzero-mode domain remain mandatory.

With arbitrary homogeneous lapse N and the reconstructed shift,

\[
Y=\epsilon^2p^2w^2/N^2,\qquad
\mathcal L_{\rm force}=-a^3 A|\epsilon p w|^3/N^2.
\]

For the prescribed real cosine mode, the spatial average of |cos|^3 is
4/(3 pi). At N=1 the averaged comoving canonical coefficient is

\[
C_X=\frac{4A|p|^3}{3\pi\,a^{3/2}f^3}.
\]

Thus F(epsilon)=-C_X |epsilon|^3 has third derivative -6C_X from the
right and +6C_X from the left. All 216 archived events have nonzero C_X;
its sampled range is 1.882517674085886e-15 to 0.014257312936844367.
These are sampled archived values, not a proof over a continuous domain.

The regular auxiliary-stationarity argument is limited to the declared
invertible nonzero-mode block. No complete second-order scalar/zero-mode
constraint sources, full quartic Schur action, scattering amplitude or
physical EFT cutoff are supplied. In particular, the direct regulator
term -b(Delta_2)^2/2 is not the full reduced quartic interaction.

A=0 removes this force term. p=0 removes this transverse cusp, but the
finite-k scalar force-gradient cusp remains. Neither control certifies
full-action C3 regularity.

## Supplementary numerical checks

An unexpanded 60-digit connection/projector calculation independently
checks the symbolic jets at h=0.001, 0.0005 and 0.00025. The largest
normalized second-order frame-invariant error falls from
1.0312444617293294e-7 to 2.578112318545028e-8 to
6.445281524001666e-9. This is consistent with the expected halving
convergence. At the finest step the normalized one-sided third-derivative
values are -6 and +6, with deviations below 4.77e-53.
The 60-digit arithmetic checks local algebra; it does not upgrade the
double-precision archived backgrounds to that accuracy.

For the cross-implementation comparison define
d(x,y)=abs(x-y)/max(1,abs(x),abs(y)), and match rows on (eta,method,t,k).

| Original field | Cross-check field | Maximum d |
| --- | --- | --- |
| K_vector | kinetic_weight | 0 |
| G_vector | gradient_weight | 0 |
| vector_mass_w | physical_tilt_mass_squared | 1.1102230246251565e-16 |
| canonical_X_mass | canonical_mass_squared | 1.1102230246251565e-16 |
| local_frozen_frequency_squared | canonical_frequency_squared | 0 |
| averaged_cusp_X_coefficient | comoving_cusp_coefficient | 1.734723475976807e-18 |

The supplemental 1e-12 consistency tolerance is not a newly preregistered
physics decision. Both receipts have zero failed/unknown local assertions.
The comparison log is retained privately at
.local/itsm-context/output-3c2f8c26318d453b8ac1678c460d3e9b.txt,
SHA-256 235578f1d2fc48eac5de0c0bc8e4c3a81036ae768196cb0201ef774ae357102e.
The field mapping and normalization above specify this supplementary
comparison independently of that ignored log.

## Sealed artifacts and reproduction

- [Original versioned source](../../../Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity_v1.py):
  SHA-256 875aefe980e4b78a1173a69bbd129d81a7dc4b2b0872c0a16774bc7c177bfe8b.
- [Original receipt](../../../Analysis/MasterTests/outputs/r4c1_g3v_attempt_01/summary.json):
  SHA-256 07e85fbd5c13b7390be3dadad723a36f445aa065d678b51f8070255834157cae.
- [Cross-check source](../../../Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity_crosscheck.py):
  SHA-256 4898f85f20e30bb0ba3c61492d97657bde0163b3bf74a67c60ba38d9cf027f19.
- [Cross-check receipt](../../../Analysis/MasterTests/outputs/r4c1_g3v_crosscheck_attempt_01/summary.json):
  SHA-256 b752415f0d5741c80a47dca5c699f7dc2ca54d31fc43ba04ded4c335939bf492.
- [Cross-check formulas](../../../Analysis/MasterTests/outputs/r4c1_g3v_crosscheck_attempt_01/formulas.json):
  SHA-256 7a2a05e4240d668153d14a45a0d9dc7dab4a5c9d167c9a54c98fb51d70b7cb09.
- [Cross-check grid](../../../Analysis/MasterTests/outputs/r4c1_g3v_crosscheck_attempt_01/grid.json):
  SHA-256 bbb332d89a5a63af119c6f7c34580516ca450e19dc46c67a4d0a31c61d3a859b.

Run from the existing repository using the established interpreter:

~~~powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity_v1.py --replay
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_g3_coupled_vertex_regularity_crosscheck.py --replay
~~~

Original replay: four JSON payloads byte-identical, exit 0.
Cross-check replay: three JSON payloads byte-identical, exit 0.
The replay modes do not rewrite sealed results.

## Source-recovery incident: attribution and preservation

This continuation's initial inventory incorrectly treated the unversioned
G3V executable as absent. An agent Add File patch replaced the existing
source. This is an identified agent error, not evidence of an unknown
outside writer for that overwrite. The later run refused the existing
output directory, and the replacement was preserved separately rather
than used to rewrite the earlier result.

The original source was recovered from the ITSM memory bank's observed
source document doc_7f3b1fd8c0667d2632d832db. Its normalized no-final-LF
text hash is be791b3f6796237165495ff9b12fe11761417cb597ac92bb6e2c4c2f00af22e1.
Restoring the original final LF produces the exact receipt/sidecar hash
875aefe980e4b78a1173a69bbd129d81a7dc4b2b0872c0a16774bc7c177bfe8b.
The live unversioned source now matches that hash as well as the separately
sealed v1 source. The original receipt, report, output payloads and their
sidecars are unchanged. Replaying the recovered source confirms the
original payloads byte-for-byte.

The earlier integrity addendum recorded the writer as unidentified in its
audit. This new note supplies the attribution established from this
continuation's recorded patch and recovery; it does not rewrite that
historical note or attribute unrelated file changes.

The temporary recovery text is retained in ignored local storage at
.local/itsm-context/g3v-crosscheck-provenance-2026-10-08-closure/recovered-source.txt,
with the same original source hash. Its redundant staging copy is removed
from Analysis/MasterTests only after that backup is hash-verified.
The deferred-register pre-append snapshot is retained in the same private
directory, SHA-256 2e679e4ed0fd5393f6f3a66aab14761127c95dca2333fce9c15148a903ab2eca.

## Next scientific decision and inherited holds

The next bounded route is an explicit nonanalytic treatment of this
homogeneous action, or a separately justified nonzero projected-gradient
on-shell background/domain for an ordinary vertex expansion. Neither is
implemented or assumed here. Smoothing away the force term, dropping it,
or transferring a vacuum amplitude would change the problem.

Inherit R9-MT1-G3V, R9-MT1-G3V-V1-INTEGRITY and all their substantive and
review dependencies; record this supplement as R9-MT1-G3V-CROSSCHECK.
Pending review alone does not block provisional research. The regularity
obstruction, missing full-sector constraints and missing scattering/cutoff
calculations remain substantive dependencies.

Canonical Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No manuscript/PDF edit, promotion, publication, commit, push, provider
dispatch, model change or vault mutation is performed in this task.

