# M2/M3-U1 RCP-0 action ledger

**Date:** 2026-09-05  
**Route:** `M2/M3-U1_CONDENSATE_PORTAL_CONTROL`  
**Work package:** High H-1 / RCP-0 specification  
**Status:** `READY_FOR_MAX_DERIVATION_SCOPED_CONTROLS`  
**Physics pass:** `false`  
**Gate effect:** none  

## 1. Question and boundary

Can a finite-density complex field with a `U(1)`-invariant matter portal
produce a nonzero physical matter residue after amplitude-phase-metric
reduction?

This ledger freezes control actions and their non-inheritance rules. It does
not derive a force normalization, select a canonical ITSM action or solve the
coupled constraint problem.

Binding status remains:

- `MAT-001 BLOCKED`;
- `UVIR-003 IN_PROGRESS`;
- `K_Q NOT_DERIVED`;
- `V=C_m/sqrt(K_Q) NOT_COMPUTED`;
- observed `a_0` and the relation `cH_0/(2*pi)` are prohibited inputs.

## 2. Conventions

- spacetime dimension: four;
- signature: `(-,+,+,+)`;
- natural units: `hbar=c=1`;
- `[d^4x]=-4`, `[L]=4`, `[Phi]=1`, `[|Phi|^2]=2`, `[T_m]=4`;
- a multiplying function `F(|Phi|^2)` in `F T_m` must be dimensionless;
- `Phi=(rho/sqrt(2)) exp(i Theta)` unless a comparator's published
  normalization is being reproduced explicitly;
- `Theta` is dimensionless and `[rho]=1`;
- all source signs must be propagated from the displayed action rather than
  inferred from a force magnitude.

## 3. Namespace RCP-C0 — literature comparator

### 3.1 Frozen action

On the published fixed-background force calculation,

\[
S_{\rm C0}=\int d^4x\sqrt{-g}\left[
-g^{\mu\nu}\nabla_\mu\Phi^*\nabla_\nu\Phi
-m^2|\Phi|^2-\frac{\lambda_4}{2}|\Phi|^4
-\frac{|\Phi|^2}{\Lambda^2}J
\right].
\]

Here `[m]=[Lambda]=1`, `[lambda_4]=0`, `[J]=4`. For a baryonic
application the literature identifies `J=-T^mu_mu` subject to its convention.
The Max calculation must anchor the sign directly to that definition.

The homogeneous finite-density control is

\[
\Phi_0=v e^{i\mu t},\qquad
\mu^2=m^2+\lambda_4v^2,
\]

in the published normalization. This is a finite-charge condensate, not the
zero-density Lorentz-invariant vacuum.

### 3.2 Present and absent content

Present:

- one complex scalar;
- exact global `U(1)`;
- quartic repulsive self-interaction for `lambda_4>0`;
- explicit invariant source portal;
- finite-density amplitude-phase mixing.

Absent from the scoped force calculation:

- dynamical metric constraint reduction;
- ITSM active-vacuum identification;
- compact `T^3`, winding and moduli dynamics;
- reservoir action;
- a derived MOND/AQUAL operator or acceleration scale.

**Disposition:** `FROZEN_EXTERNAL_COMPARATOR`. Its equations may be reproduced;
its ontology, coefficients and gate status may not be inherited.

## 4. Namespace RCP-I1-T — literal off-shell trace-operator control

Define a bare matter action and its stress tensor before adding the portal:

\[
T^{(0)}_{\mu\nu}
=-\frac{2}{\sqrt{-g}}\frac{\delta S_m^{(0)}[\chi,g]}
{\delta g^{\mu\nu}},\qquad
T_m^{(0)}=g^{\mu\nu}T^{(0)}_{\mu\nu}.
\]

The literal trace-EFT control is

\[
\begin{split}
S_{\rm I1T}={}&\int d^4x\sqrt{-g}\left[
\frac{M_P^2}{2}R
-g^{\mu\nu}\nabla_\mu\Phi^*\nabla_\nu\Phi
-U(|\Phi|^2)
+F_T(|\Phi|^2)T_m^{(0)}
\right]\\
&+S_m^{(0)}[\chi,g],
\end{split}
\]

with

\[
U(s)=m^2s+\frac{\lambda_4}{2}s^2,
\qquad s=|\Phi|^2,
\]

and dimensionless `F_T(s)`. For direct comparison one may set
`F_T(s)=-s/Lambda^2`, but this is an explicit control choice, not a derived
ITSM coefficient.

This definition avoids the circular expression `F(s) T_m` in which `T_m`
would already include variation of the portal. Metric variation nevertheless
contains the functional response of `T_m^(0)` and must be retained. This route
is an EFT operator, not automatically a universal metric coupling.

**Disposition:** `FROZEN_LITERAL_TRACE_CONTROL`; suitable for an exact scoped
variation. It is not yet a complete ITSM matter theory.

## 5. Namespace RCP-I1-C — conformal-matter-metric completion

The cleaner universal off-shell completion is

\[
\begin{split}
S_{\rm I1C}={}&\int d^4x\sqrt{-g}\left[
\frac{M_P^2}{2}R
-g^{\mu\nu}\nabla_\mu\Phi^*\nabla_\nu\Phi
-U(|\Phi|^2)
\right]\\
&+S_m[\chi,\widetilde g_{\mu\nu}],
\qquad
\widetilde g_{\mu\nu}=A^2(s/M_*^2)g_{\mu\nu}.
\end{split}
\]

`A` is positive and dimensionless. The control is specified symbolically by
its background derivatives

\[
\alpha_1=\left.\frac{d\ln A}{ds}\right|_{s_0},
\qquad
\alpha_2=\left.\frac{d^2\ln A}{ds^2}\right|_{s_0},
\qquad s_0=|\Phi_0|^2.
\]

The Max calculation must derive the trace vertex from variation of
`S_m[chi,g_tilde]`; it may not paste in the RCP-C0 source. `alpha_1` has mass
dimension `-2`. Unless a symmetry or microscopic matching fixes `A`, the
physical residue will retain free matter-sector data.

This action is **ITSM-compatible in identity only** when `Phi` is interpreted
as the active vacuum condensate. It is not a complete ITSM parent because the
compact/winding and reservoir sectors are not present in the displayed local
control.

**Disposition:** `FROZEN_UNIVERSAL_COUPLING_ACTION_CLASS_FUNCTION_UNMATCHED`.
It may advance to Max symbolic reduction with `A`, `alpha_1` and `alpha_2`
kept explicit; it cannot make a numerical prediction.

## 6. Namespace RCP-PKM1 — separate metric-hosted candidate

RCP-PKM1 is exactly the frozen parent in
`Analysis/MAT/MAT-001/PKM1_METRIC_HOST/PKM1_P0_FINITE_DENSITY_PARENT_SPEC.md`.
Its matter sector is minimally coupled to one metric and it contains no direct
`F(|Phi|^2)T_m`, no separate force scalar and no appended portal.

It must not be combined with RCP-C0, RCP-I1-T or RCP-I1-C without a new
architecture decision and a fresh constraint count.

**Disposition:** `FROZEN_SEPARATE_CONTROL`; current PKM1 hold unchanged.

## 7. Expected background classes

| Namespace | Background permitted at next step | Background not licensed |
|---|---|---|
| RCP-C0 | Published homogeneous finite-density fixed-background comparator | Full gravitating ITSM background |
| RCP-I1-T | Exact solution of the displayed coupled action; FRW is preferred if finite density gravitates | Minkowski obtained only by ignoring condensate enthalpy |
| RCP-I1-C | Exact solution of Einstein, condensate and matter equations; FRW is preferred | Unspecified rigid support or cosmological-constant cancellation of nonzero enthalpy |
| RCP-PKM1 | Only backgrounds permitted by its frozen specification | A portal-sourced background imported from another namespace |

If an on-shell gravitating background is not available, the Max calculation
must remain a fixed-background response control and say so.

## 8. Physical target and relation to `K_Q`

The required result is not a standalone numerical `K_Q`. For a reduced
physical mode `u` and source covector `c_eff`, the target is

\[
g_{\rm can}=\frac{c_{\rm eff}^{T}u}{\sqrt{u^{T}Ku}},
\]

with sign fixed by an orientation convention. In a legitimate one-parent map,

\[
K_Q=\frac{Z_\phi}{f_\phi^2},\qquad
C_m=\frac{g_\phi}{f_\phi},\qquad
V=\frac{g_\phi}{\sqrt{Z_\phi}}.
\]

The portal may supply `g_phi` and the condensate may supply `Z_phi`, but the
full constrained projection is still required. A free `alpha_1`, `Lambda`,
`A(s)` or equivalent invariant means the physical normalization remains free.

## 9. Predeclared outcomes

| Result | Classification |
|---|---|
| Fixed-background source and healthy scalar modes reproduced | Comparator mechanism established only |
| Physical pole exists but depends on free `A`, `alpha_1` or `Lambda` | `CALCULABLE_FREE_NORMALIZATION`; MAT remains blocked |
| No static source after correct projection | `SCOPED_NO_GO_SOURCE_PROJECTION` |
| Required sign has a gradient/ghost instability | `SCOPED_NO_GO_STABILITY` |
| Metric completion violates hard local/lensing bounds | `SCOPED_NO_GO_RELATIVISTIC_COMPLETION` |
| Same parent fixes healthy residue and acceleration law blindly | Candidate for signed architecture review, not automatic gate pass |

## 10. Inputs prohibited from the derivation

- observed MOND/RAR acceleration scale;
- `cH_0/(2*pi)` or the van Putten alternative;
- SPARC likelihood or fitted transition radius;
- `C_obs=1` or `2/3`;
- a target healing length;
- `T^3` cycle count or winding chosen to normalize the force;
- P2 Casimir ratios;
- a phenomenological reservoir current.

## 11. Source hashes at freeze

```text
82fb9e195fbcaf7f1ae5edfecf9b3ab08f9d708d18b9403ae085c636ba7306c8  Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md
f28ab9e487f0b229d76ddeef77ee33258a9a56b687e12521407627299fd11d04  Theory/Core/ITSM_Tier1_Route_Test_Programme.md
eca9310648f6df10b0422f32fdd9225063c7565e7c46de0ee7bf8529cbe8f954  Theory/Gates/MAT-001/MAT-001_J1_JOINT_ACTION_NORMALIZATION.md
2122fc7658b248d77042bffd852ceb99a8e3fac76c71e0fede505d38520e7673  Analysis/MAT/MAT-001/M2_RADIAL_MATCHING/outputs/MAT-001_M2_RADIAL_HEAVY_REDUCTION.md
f836bbc0774b9d132b8c600cbb9c4db4dbb263b3ea063848c649b51c26457a01  Analysis/MAT/MAT-001/M4_INVARIANT_RESIDUE/outputs/MAT-001_M4_INVARIANT_RESIDUE_CONTROL.md
c0e0f1414beda764079a775b9b7fa1caad522feeb403f80b26bd5b5648424ff7  Analysis/MAT/MAT-001/PKM1_METRIC_HOST/PKM1_P0_FINITE_DENSITY_PARENT_SPEC.md
```

External literature:

- <https://arxiv.org/abs/2505.23900>;
- <https://doi.org/10.1016/j.physrep.2026.02.001>;
- <https://doi.org/10.1103/PhysRevD.99.076003>.

## 12. Handoff

RCP-C0, RCP-I1-T and RCP-I1-C are ready for the bounded Max calculations in
`03_MAX_BOUNDED_EXACT_REDUCTIONS/PLAN.md`. Stop before full metric constraint
elimination and the physical pole-residue decision; those remain Ultra.
