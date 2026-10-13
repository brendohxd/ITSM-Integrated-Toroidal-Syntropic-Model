# P1 local release preparation - 8 October 2026

Result ID: `P1-RELEASE-PREP-2026-10-08`. Current manuscript: `0.2.0-rc2`.

The local cold read and portable source build are complete. The current
source package is for author/reviewer preparation. Source corrections below
remain unapplied, and no public upload or independent scientific review is
recorded. This report is the current preparation record; it does not mark
the older submission checklist's author or review steps complete.

## Scope and authority

`review_status=DEFERRED`, `Rule9_cleared=false`,
`research_execution=PROCEED_PROVISIONALLY`, `gate_effect=NONE`, and
`publication_ready=false`. Applicable scientific requirements are inherited
from GEMINI, Core Identity, the selective publishing plan and the P1 README.
`MAT-001=BLOCKED`, `UVIR-003=IN_PROGRESS`, `K_Q=NOT_DERIVED`, and
`V=NOT_COMPUTED` are unchanged. No reviewer or paid provider was dispatched.

## What was checked

The entire 620-line manuscript, 132-line bibliography, README, submission
checklist, cover letter, and build helper were read. This is a parent-agent
assessment, not independent Role-A/B/C clearance.

- Varying the stated static scalar action gives
  `(C_IR/(4*pi*G*a0))*div(|grad psi| grad psi) - C_m*rho_b = 0`.
  On the positive-coefficient, regular-origin spherical branch,
  `|grad psi|^2/a0=(C_m/C_IR)*g_N`, and the matter force gives
  `C_obs=C_m^(3/2)/sqrt(C_IR)` as written.
- Under `psi -> s*psi`, `C_m -> C_m/s` and `C_IR -> C_IR/s^3`.
  The displayed invariant is unchanged. This does not determine its value.
- For `C_obs=2/3`, `a0_eff=(4/9)*a0` and the asymptotic velocity ratio is
  `sqrt(2/3)=0.8164965809`, a reduction of `18.3503419%`. This is the
  manuscript's conditional spherical comparison; no catalogue was fitted.
- With illustrative `H0=70 km/s/Mpc`, direct unit conversion gives
  `a0=1.0824013602e-10 m/s^2`, `a0_eff=4.8106727122e-11 m/s^2`, and
  `m=h*H0/c^2=9.38195035e-33 eV/c^2`. The manuscript uses rounded values.
- Fixed comoving moduli and `L_phys=c/H` imply `Hdot=-H^2`, hence `q_dec=0`.
  This conditional result does not exclude an independent evolving modulus.
- With the metric contraction understood, a unit vector gives
  `gamma^ij h_ij=3-1=2`, so the projector rank ratio is `2/3`.
- The [Planck primary abstract](https://arxiv.org/abs/1502.01593) confirms
  `R_i>0.97*chi_rec` for the cubic model. Its likelihood-ratio criterion and
  separate 99% polarization matched-circle bound should be distinguished.
  `L=2*R_i` and the stated approximate distance conversion give
  `L/(c/H0)>2*0.97*3.15=6.111`. This retains the cited cosmological/search
  assumptions; it is not a fresh bound derived within ITSM.
- The [COMPACT bibliographic entry](https://arxiv.org/abs/2210.11426) was
  checked against its primary title, authors and abstract. Neither referenced
  analysis was numerically reproduced.

## Corrections identified before the next manuscript freeze

1. **Equation 17 notation:** the compact-source flux uses undefined `varphi`
   while its action and preceding equations use `psi`. Use `psi` consistently.
2. **Equation 12 contraction:** define `Tr_gamma(h)=gamma^ij*h_ij` explicitly
   for the general Riemannian statement. The rank result is unchanged.
3. **Coefficient branch and units:** state `a0>0`, `C_m>0`, `C_IR>0`,
   dimensionless coefficients, and potential dimensions `L^2 T^-2` before
   taking the positive square root. This records the branch already used.
4. **Figure 2:** its artwork says "Topological Projection Factor" and
   "Vacuum drag acts strictly within the 2D transverse shear plane of the
   plenum." These positive physical assertions conflict with the caption's
   disclaimer and the manuscript's un-derived coupling. Remove this figure
   from the next draft, or replace it with a neutral rank-projector schematic.
   The proposed patch removes its inclusion and preserves the original asset.
5. **Table I:** remove unsupported attribution to unspecified prior proposals;
   describe the dual coefficient choice as a conditional normalization shift
   rather than a completed RAR fit rejection.
6. **Keywords:** REVTeX reports that `showkeys` is needed to display the declared
   keywords. Add it if retaining the checklist's visible-keywords requirement.

`P1_SOURCE_CORRECTIONS_2026-10-08.patch` records these exact edits in
`apply_patch` format. It is unapplied. Apply only to the recorded source hash,
assign a new manuscript/PDF version, and rebuild/inspect the revised result.
It does not change a parent action, empirical coefficient, gate or old receipt.

## Source package and build evidence

`ITSM_P1_source_v0.2.0-rc2_2026-10-08.zip` contains exactly `main.tex`,
`references.bib`, generated `main.bbl`, and the two original figure PDFs.
It contains no vault, conversations, private context, or compiler logs.
The packaged source restricts `graphicspath` to `figures/`; a text comparison
confirmed this and trailing-newline normalization are its only changes.
Thirteen citation keys match thirteen bibliography entries, with none missing.

Using the installed MiKTeX, three TeX passes and BibTeX completed with exit
zero. Package installation and shell escape were disabled. The final recorder
has 257 input records and zero repository inputs. TeX class/font dependencies
are provided by the existing installation; the source archive is not a bundled
TeX runtime. The archive itself was opened and its five entries verified.

The new verification build has six pages. All six were rendered and visually
inspected. There is no text overlap, clipped equation, unresolved reference or
missing figure. Page 6 has loose spacing in the code-availability block; the
underfull-box warnings are retained. The Figure-2 claim problem is substantive
presentation work still pending. No TeX error, undefined citation/reference or
overfull box appears in the final log. Benign nameref and disabled-shell-escape
warnings and the keyword warning remain.

The verification PDF is a separate build dated 8 October through `today`.
It does not replace the canonical 1 October PDF or its sidecar. The canonical
PDF hash is `0fefc03fae9024f78728ea80c170ca29e9e3d5152546a48cea8b2948c8d1352a`.
Exact inputs/outputs are listed in `P1_PREPARATION_MANIFEST.json`.

## Remaining author and release decisions

- Cold author proofread and confirmation of contact details, ORCID, affiliation,
  acknowledgement, and the AI-use statement. The manuscript/cover letter
  already assert author review; that assertion must be affirmed by the author
  before upload, not inferred from this local assessment.
- Applicable independent review remains deferred, with no consensus claimed.
- Confirm venue/categories, any arXiv endorsement requirement, and the actual
  external-release decision. No account or deposit metadata was changed.

## File-editing limitation

`apply_patch` failed both creation of a repository plan and a narrow update to
the existing manuscript, including an approved outside-sandbox creation retry.
Creating the plan with `apply_patch` in the allowed local artifact directory
worked, and copying that completed file into the repository then worked with
matching hashes. The cause has not been established; this is not evidence that
all repository writes are blocked. No firewall, ACL or security setting was
changed. Original manuscript updates remain pending until the file-editing
path works. New dated documents and the package preserve this preparation.

Final provenance check: all nine original P1 inputs and both source figures
match their recorded hashes. BibTeX also reports one style warning:
`Warning--jnrlst (dependency: not reversed) set 1`. Its exit code is zero;
all thirteen cited keys are present. This diagnostic remains recorded.
