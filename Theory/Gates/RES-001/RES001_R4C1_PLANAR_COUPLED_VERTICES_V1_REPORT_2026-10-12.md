# R4C1: planar coupled interaction functional, V1

Date: 12 October 2026. Owner: Master Test 1 / RES-001 / approved Stage 2.
Disposition: **GENERIC_PLANAR_WWR_AND_INTRINSIC_CONTACT_CHECKED_PHYSICAL_INTERACTION_OPEN**.
Computational validation: 176/176 local checks, byte-identical read-only replay.
Physical clearance: false. Stage 2 and the full native goal remain incomplete.

## What this checkpoint resolves

The earlier fixed-metric vacuum probe did not include the coupled response.
This calculation derives from the unchanged covariant action the analytic
coupling of two y-polarized transverse waves W to **all 22 independent response
fields**, allowing W and its first ADM shift B to depend on t,x,z. It also
derives the intrinsic analytic fourth coefficient on that first-direction
ray. No metric/matter response is set to zero because its direct source is
zero. No physical scattering amplitude or frequency window is supplied.

The action is expanded in the exact quotient ring
`e^5=d^2=e^3*d=0`. The `e^2 d` coefficient is the WWR functional, linear in
response value/t/x/z jets; `e^4` is the intrinsic contact. d remains an
independent variation, not a solved response. U=(1+d nu)n is varied with the
normalized force/alignment frame n, so the independent normal equation is
retained. Einstein+GHY uses the frozen ADM boundary convention.

Generic action variation precedes every family substitution. Source labels
are explicit, not an alphabetical-to-physical positional assumption:

`alpha,Sx,Sy,Sz,Mxx,Mxy,Mxz,Myy,Myz,Mzz,Vx,Vy,Vz,du,dv,dr,Pi,T,Em,Z,nu,LambdaU`.

The exported family parameter maps contain coefficients entering these new
vertices. The other potential/portal/background scalings remain governed by
the pinned family-survey prescription, not newly fixed by a vanishing direct
source. No background initialization or scalar matching is replaced here.

All nine analytic action sectors are exported. Spatial Ricci has zero direct
WWR/contact coefficient because the first direction leaves h unchanged;
its complete quadratic response contribution remains in the pinned generic
110-jet Hessian. Scalar/potential/portal, dust and multiplier direct WWR
coefficients vanish on this ray, but their equations and induced responses
remain in the coupled system. Analytic direct Euler sources are nonzero for
alpha, Sx, Sz, Mxx, Mxz, Myy, Mzz, Vx, Vz, du, dv, Pi, Z and nu. The
nonanalytic Vy source is retained separately.

## Exact identities and new contact

The x/z exchange identity is exact, with corresponding metric off-diagonal
labels exchanged. Setting all x derivatives to zero exactly reproduces the
old **unspecialized** collinear WWR functional and quadratic vector action.
This is an identity check, not another integration of the completed archive.

Write alpha13=MU2(c1+c3), MT2=MP2-alpha13, f2=MU2(c1+c4),
sigma=-alpha13/MT2 and J=v0*u_dot-u0*v_dot. Only after variation is the first
nonzero transverse shift set to B=sigma W. No mean-mode Laplacian inverse
is introduced. The generic vector Euler expression is

\[
 E_W=-f^2\left[W_{tt}+3HW_t-\frac{c_V^2}{a^2}(W_{xx}+W_{zz})+m_w^2W\right],
\]

\[
 c_V^2=\frac{M_U^2c_1+\alpha_{13}^2/(2M_T^2)}{f^2},\qquad
 m_w^2=-\frac{3c_2+c_3-c_4}{c_1+c_4}\dot H+2H^2
       -\frac{K_Q\dot\psi^2}{f^2}+\frac{\zeta J^2}{f^2}.
\]

This is the **frame** mass, not the mass after a time-dependent canonical
rescaling. With the complete commuting mixed-third-derivative map, the
temporal/x/z source Ward identities hold generically off the linear vector
shell: their residuals after subtracting `(H W-W_t) E_W`, `W_x E_W` and
`W_z E_W`, respectively, are identically zero. Coefficient drift and all
retained source fields are included. This is not a full nonlinear Ward audit.

The intrinsic analytic coefficient is

\[
 \mathcal L_{4,\mathrm{intr}}=
 \frac{M_U^2W^2}{2}\left[-c_{123}W_t^2
 +G_4\frac{W_x^2+W_z^2}{a^2}\right],\qquad
 G_4=c_1-\frac{c_1-3c_3}{2}\sigma-(c_3-c_4)\sigma^2,
\]

where c123=c1+c2+c3. This compact form follows from the exported unreduced
coefficient, not from imposing a fixed metric. H cancels in this specific
intrinsic coefficient; it has not been dropped from the source functional
or quadratic equation. The independent B=H=0 control gives exactly
`MU2 W^2[-c123 W_t^2+c1(W_x^2+W_z^2)/a^2]/2`.

For the local fixed-coefficient normalization chi=sqrt(f2) W, all three
families have f2=eta/6 in the MP=1 chart. The exact eta-to-zero contact limits
are as follows; these are **off-shell contact coefficients**, not amplitudes:

| Family | lim eta C_time | lim eta C_spatial |
| --- | --- | --- |
| archived G3 | -1/2 | 12/5 |
| new B1-frame | -6/5 | 12/5 |
| new hierarchical | -6/5 | 12/5 |

Here `L4_intr=chi^2[C_time chi_t^2+C_spatial |grad chi|^2/a^2]`.
Thus a 1/eta contact remains a warning in all families, including the luminal
tensor control. **Exchange cancellations have not been decided.** The old
probe already contains a counterexample in which off-shell quartic terms
exist but an on-shell amplitude vanishes. No contact-only physical cutoff,
all-action no-go, or healthy-GR conclusion is drawn. MT2>=7/8 for G3 and the
hierarchical family, and MT2=1 for B1, on 0<eta<=1; the first transverse
shift denominator is nonsingular there. Other constraint domains are not
cleared by this observation.

## Nonanalytic force and controls

The covariantly computed projected-gradient coefficients are exactly
`Y[e^2]=psi_dot^2 W^2`, `Y[e d]=2 psi_dot^2 W R_Vy` and `Y[e^4]=0`.
The first-ray force density is `-A |psi_dot e W|^3`. For a fixed response ray
d=e^2, its e^4 coefficient is
`-3 A |psi_dot|^3 sign(e) W |W| R_Vy`; independent positive and negative
directions reproduce the distinct one-sided limits. A prepared cusp response
itself changes sign when e reverses, so a fixed response ray must not be
misidentified with a solution. No division by W is used at its zeros.
The density is C2 and not C3 at a nonzero-coefficient zero-crossing; its force
is C1. There is no ordinary Taylor cubic vertex at Y=0. The prior mathematical
odd-tail certificate is retained and not promoted to a physical UV domain.

Independent controls use **unexpanded** ADM metrics, inverse matrices,
connections, scalar/matter/auxiliary actions and normal-frame variation at
80 decimal digits, on two planar response jets. All nine sectors are checked
separately at the three frozen step sizes. Largest final normalized errors:
WWR `4.6118329166433705e-12`; intrinsic W4 `4.992940234179819e-13`.
Degree/dimension, inverse, norm, rotation, collinear, omission, force-direction
and generic Ward controls pass. These numerical coefficient controls do not
constitute a continuous physical remainder bound.

## Reproducibility and preservation

Contract: `RES001_R4C1_PLANAR_COUPLED_VERTICES_V1_CONTRACT_2026-10-12.md`,
SHA-256 `8238acc979693a2a24c3a8445ba31b449c97277ece23de3cb785cf6206ecc423`.
Executable: `Analysis/MasterTests/test_01_r4c1_planar_coupled_vertices_v1.py`,
SHA-256 `0e8352d933e9dccfa12bf1bb10bbbcb16d8949ae6fc97a0a9ba20e356c1ad751`.
Fresh output: `Analysis/MasterTests/outputs/r4c1_planar_coupled_vertices_attempt_01/`.

| Artifact | SHA-256 |
| --- | --- |
| formulas.json | 852b657c9023244a76cc49494b6adb08510d4eeb74bd95ec390ff11bc6b0789a |
| independent.json | fa5e232d5adc08b9f8911e9dbdb3504d906a396c43ec08a58e01ce94584498c3 |
| scope.json | 298c3d82911cdc1aa42c7c7895c8bb36d4c8501b12ec2ce91f4061170c6f8ec1 |
| summary.json | 9e6ab752a0a57d95bcfdcac85ef67e59d0b9e0758eb73e12656d349b933c3268 |

Execution session 79067 and replay session 7972 are TERMINAL exit 0.
Read-only QA verified 262 inherited/new source pins, 259 available source
sidecars and all four new artifact sidecars. Three known historically absent
sidecars remain absent. The 958/964 source-Ward failure and 10395/10449
time-response failure remain failed and hash-pinned. The original coupled
trajectory SHA remains
`8a3e5df7765aca174b520a53a8a0ca01848941ec34032cba648c3a198ee9320d`.
No completed trajectory integration, old source or scientific receipt was
rerun/rewritten. Private execution/replay/QA logs remain ignored and local.

## Next owning calculation and full-goal disposition

Use these generic vertices with the complete constrained quadratic response,
physical external-state normalization and a declared finite-density state/
boundary prescription. Retain metric, matter, scalar/phase and auxiliary
exchange, spatial Ricci, the nonanalytic force, mean/IR sectors and drift.
Static exchange in pressureless matter and FLRW time dependence must not be
silently treated as a vacuum S-matrix. Resolve endpoint/retarded prescriptions
and control background adiabaticity before inferring an interaction scale.
Establish the physical-energy norm, quartic-dispersion frequency/momentum
domain and nonlinear remainder; then assess the shrinking probe scale and
GR recovery in that actual coupled domain. Do not derive a cutoff from the
potential parameter, this contact alone, or another compatibility counter.

Stage 1 remains complete **only** in its registered linear B1 prepared-dust
scope. Stage 2 remains INCOMPLETE / STOP_AND_ASSESS_DOMAIN_UNRESOLVED; no family
is admitted physically. The approved same-action research continuation is
active. Stage 3 remains NOT_ENTERED: identifying matter-residue and nonlinear
force matching inputs remain missing. The full native goal is ACTIVE and
incomplete, with meaningful progress here, not a repeated external impasse.

R9-MT1-PLANAR-WWR-V1 and inherited reviews are DEFERRED, not cleared.
Tests 1-3 HOLD_SUBSTANTIVE; physics_pass=false; gate_effect=NONE;
Rule9_cleared=false; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED;
V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED. The ITSM memory skill's
provenance/claim boundaries were followed; its native vault tools were absent,
so the canonical repository was used without vault mutation. No new parent,
manuscript/PDF edit, provider/model dispatch, commit, push or publication.
