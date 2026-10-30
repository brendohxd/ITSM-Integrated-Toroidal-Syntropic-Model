# Force-architecture comparison V1: retain R4C1 for one physical-sector test

Work initiated 23 October 2026. Result ID:
ITSM-FORCE-ARCHITECTURE-COMPARISON-V1. Claim: **Conditional**.
Rule-9 DEFERRED; physics_pass=false; gate_effect=NONE.

## 1. Decision first

**Neither architecture has demonstrated an admitted, healthy physical force
window.** The recommendation is nevertheless to retain **unchanged R4C1** for
ONE bounded physical-admissibility/normalization calculation, not automatically
extend the material-derivative hierarchy or claim a physical winner.

The question is whether the actual full constraints admit the relevant
scalar-rate perturbations and what kinetic/symplectic normalization and
principal evolution they have. Negative restricted Hamiltonian curvature alone
does not answer this. Require a physical-sector result or an explicitly bounded
obstruction; if another uncontrolled hierarchy is required, STOP for an operator
architecture decision. Do not proceed by accumulating numerical agreements.

This is a resource/dependency judgment, not a theorem of superior viability:

- R4C1 already has a declared joint action, exact implicit initial constraint
  construction and a nontrivial first-material-order compatibility result.
- P0-B avoids the separate direct matter-residue issue by changing the force
  host to the metric. It does not solve the live MAT gate or identify its J/a0.
  The new calculation below adds a substantial conditional local-gravity
  restriction, rather than demonstrating its missing physical window.
- Both still owe physical-domain and identifying input evidence. No numerical
  C_chi/a0 prediction, observational fitting, new parent or TOP-X4 pivot follows.

Free EFT coefficients do not by themselves invalidate an EFT. They do prevent
the particular theory-fixed numerical prediction sought in Stage 3. Conditional
papers can be assessed on their own scoped claims without solving all of ITSM.

## 2. Consolidated R4C1 evidence; no upstream audit rerun

| Reused result | Established within its scope | Still not established |
|---|---|---|
| Bounded prepared dust | Registered linear prepared-data calculation and finite-mode error control | Physical/canonical dust closure |
| Material-seed feasibility | Changing-background forcing cancels frozen forcing at first material order for declared seeds; both terms retained | Higher/rank-changing consistency, full finite-time admission/persistence |
| Scalar-rate energy | Restricted curvature is negative; it cannot simply serve as a positive norm | Admitted physical ghost, exponential growth or complete coupled energy |
| Weak-generator realization | Bounded mathematical realization and restored terms | Cauchy well-posedness or stable physical evolution |
| GR-family survey | Controlled backgrounds and scoped finite-eta spectrum/comparator calculations | Healthy endpoint, full PPN or physical cutoff overlap |
| Finite-b weak source | At fixed source shape/scale the conditional static response becomes linear as amplitude tends to zero | A universal square-root asymptote; a finite intermediate physical window also remains unproved |
| Frame scattering | Shrinking order-one scale in the declared vacuum/fixed-metric probe | A coupled finite-density physical cutoff |

Owners are the [material-seed report](../Gates/RES-001/RES001_R4C1_MATERIAL_SEED_FEASIBILITY_V1_REPORT_2026-10-21.md),
[energy report](../Gates/RES-001/RES001_R4C1_SCALAR_RATE_ENERGY_V1_REPORT_2026-10-21.md),
[weak-generator report](../Gates/RES-001/RES001_R4C1_WEAK_GENERATOR_REALIZATION_V2_REPORT_2026-10-21.md),
[GR survey](../Gates/RES-001/RES001_R4C1_GR_FAMILY_SURVEY_REPORT_2026-10-11.md),
[weak-source report](../Gates/RES-001/RES001_R4C1_WEAK_SOURCE_REPORT_2026-09-29.md)
and [frame probe](../Gates/RES-001/RES001_R4C1_G3_FRAME_SCATTERING_REPORT_2026-10-08.md).
Their current bytes and available sidecars were pinned/checked; these numerical
pipelines were not rerun. Small background defects remain nonzero. The earlier
frozen D(A^2) result was not erased by first material compatibility.

The [matching decision](../Gates/MAT-001/MAT001_PHYSICAL_MATCHING_ROUTE_DECISION_2026-10-13.md)
and RM1/ST1/ST2 reports retain distinct outcomes: the tested radial mass portal
does not provide the required soft static gapless-phase source; ST1 supplies a
parameterized source but free kinetic/mass-scale data; ST2's calculated threshold
does not select renormalization/background inputs. Neither matter residue nor
nonlinear force normalization is identified by choosing a field chart.

## 3. New P0-B calculation: from the retained action to local force

Use the [P0 decision](ITSM_PKM1_P0_PARENT_DECISION_2026-08-25.md) and its
[frozen parent](../../Analysis/MAT/MAT-001/PKM1_METRIC_HOST/PKM1_P0_FINITE_DENSITY_PARENT_SPEC.md).
No operator is added. P0-A stays rejected. P0-B is a designed EFT control,
not a microscopic ITSM derivation.

On rho>0 and Z=-(d Theta)^2>0, take the canonical condensate and
S_grav=(M_P^2/2) integral sqrt(-g)[R-2J(Y)], with universal matter metric,
U=-dTheta/sqrt(Z), Y=a_mu a^mu. In the local phase-aligned ADM chart U=n.

Write N=exp(phi), h_ij=exp(-2 psi)delta_ij. The exact spatial-curvature
identity and integration by parts give

    N sqrt(h) R3 = exp(phi-psi)[4 Delta psi-2|D psi|^2]
    integral N sqrt(h) R3
      = integral exp(phi-psi)[2|D psi|^2-4 D phi.D psi].

At leading weak-metric order, with the nonlinear J response retained,

    L_local = M_P^2[|D psi|^2-2 D phi.D psi-J(|D phi|^2)]
              + M_P^2 Kcal_QQ phi^2/2 - rho_b phi.

Here Kcal_QQ denotes the induced condensate susceptibility, NOT the live
separate-force-field K_Q. For
F(N,rho)=rho^2 mu_c^2/(2N)-N V(rho), local radial equilibration gives
V_rho=rho mu_c^2 and M_rho^2=V_rhorho-mu_c^2>0. Its Schur complement is

    F_NN-F_Nrho^2/F_rhorho
      = rho^2 mu_c^2 + 4 rho^2 mu_c^4/M_rho^2
      = M_P^2 Kcal_QQ,
    c_s^2=M_rho^2/(M_rho^2+4 mu_c^2),
    Kcal_QQ=rho^2 mu_c^2/(M_P^2 c_s^2)>0.

An independent P(X) differentiation in the executable gives the same expression.
The spatial equation is Delta(psi-phi)=0. Setting the *declared local*
harmonic/boundary difference to zero, the lapse and matter equations become

    div[mu_B(|D phi|/a0) D phi]+m_K^2 phi=rho_b/(2 M_P^2),
    m_K^2=Kcal_QQ/2,
    matter acceleration = -D phi,
    mu_B(y)=y/(1+y).

This is a leading local reduction, not a complete stationary gravitating
finite-density solution. The known finite-charge Minkowski obstruction remains.
A cosmological subtraction, torus mean equation, harmonic sector, background
drift and preferred-frame solution cannot be supplied by deleting them.
When the ellipticity becomes small, weak-metric/background errors must be
small relative to the retained operator, not merely absolutely small.

Dimensions in natural units: [rho]=[mu_c]=[M_rho]=[M_P]=[a0_geom]=1,
[J]=[Kcal_QQ]=[m_K^2]=2, [phi]=[psi]=0; L_local has dimension four.
In SI, Phi=c^2 phi, a0_SI=c^2 a0_geom, and g=|D Phi|.

## 4. Stable tail and exact conditional spherical remainder

Let delta(y)=1-mu(y)>0. The retained pure-J radial kinetic condition gives

    J_Y+2Y J_YY = -[delta+y delta'] <= 0,
    (y delta)' >= 0.

Thus y delta(y)>=y0 delta(y0) for y>=y0. In the local spherical reduction
with the Helmholtz/background terms negligible, mu(g/a0)g=g_N.
Consequently g-g_N=g delta >= a0 y0 delta(y0). This is a pure-J tradeoff,
not an all-metric-theory no-go.

For P0-B the regular positive root is

    g=(g_N+sqrt(g_N^2+4 a0 g_N))/2,
    d=g-g_N,
    d=a0-d^2/g_N,
    0 <= a0-d <= a0^2/g_N.

The leading high-acceleration correction is therefore an extra **inward**
acceleration a0, with an explicit algebraic remainder. Nothing in this
calculation sets a0 to an observed galactic value or derives it from H0.

## 5. Planetary restriction: two thresholds, not a statistical exclusion

For signed radial acceleration A_R=-a0, Gauss' equation and
<cos f>_time=-e give

    <dot varpi>=-a0 sqrt(1-e^2)/(n a),
    n=sqrt(GM/a^3).

The independent numerical implementations use (i) Cartesian time evolution
and (ii) Binet inverse-radius evolution versus orbital angle, with the exact
positive-root force. No primary code was imported by the verifier. Both agree
with the signed leading secular result in the registered small-force controls.

The source is [Fienga et al., arXiv:1601.00947v1](https://arxiv.org/abs/1601.00947),
Table 1. C1/C2 use 35%/5% postfit-residual-change acceptance thresholds.
They are NOT Gaussian sigmas, independent likelihoods or an ITSM ephemeris refit.
JPL's [approximate elements](https://ssd.jpl.nasa.gov/planets/approx_pos.html)
and [astrodynamic constants](https://ssd.jpl.nasa.gov/astro_par.html) provide
the scale conversion, not new fitted planetary initial conditions.

| Planet / criterion | Accepted precession (mas/Julian century) | Leading inward-sign necessary a0 upper (m/s^2) |
|---|---|---:|
| Mercury C1 | [-3.1,3.1] | 2.32968e-13 |
| Mercury C2 | [-1.05,1.05] | 7.89086e-14 |
| Saturn C1 | [-3.8,6.2] | 5.63871e-14 |
| Saturn C2 | [-0.15,0.25] | 2.22581e-15 |

The two criteria are retained separately, not averaged or statistically combined.
These are conditional leading-order scale restrictions; a0 is still free.
This is not the latest combined ephemeris bound and is not an all-PKM1 rejection.

For the force-remainder contribution evaluated in first-order orbital averaging,
a conservative relative bound is a0/(e*g_N,aphelion). At these leading upper
scales its maximum is 1.7832e-8. This controls that algebraic correction ONLY,
not the complete orbital-perturbation, preferred-frame, background, boundary,
quasistatic or ephemeris-fitting errors. The physical application requires
those omitted effects to be controlled; no cancellation or screening is assumed.

## 6. Relativistic and actual-window disposition

The local leading static potentials agree only with their declared boundary
conditions. This is not a full gamma/beta/preferred-frame calculation.
The [Cassini constant-gamma benchmark](https://doi.org/10.1038/nature01997)
is retained, but the actual radio observable has NOT been fitted. A changed
potential is not exhausted by substituting a constant gamma into the GR formula.
The [INPOP20a actual-data WRSS table](https://arxiv.org/html/2211.04881v1)
is kept separate from its simulated BepiColombo forecasts; no forecast is used
as an observed exclusion.

In unitary gauge J depends on N, D_i N and h^ij, not derivatives of h^ij.
It therefore adds no TT derivative principal term. The retained EH tensor
principal block has c_T^2=1. This does not establish the physical cutoff,
scalar/vector health, damping, or applicability throughout the
[GW170817 counterpart frequency/path domain](https://arxiv.org/abs/1710.05834).
The [foliation comparator](https://arxiv.org/abs/1107.5264) explicitly warns
about preferred-frame dynamics; it supplies no finite-density ITSM completion.

For positive tolerances, the necessary partial momentum band is

    m_K^2/(epsilon_H*lambda_min) < k^2 < epsilon_TF*M_rho^2.

A complete local candidate band must also satisfy background, compactification
and interaction restrictions, schematically

    max[m_K^2/(epsilon_H*lambda_min),
        Omega_bg^2/(epsilon_bg*c^2*lambda_min),
        (2*pi)^2/(epsilon_L*L_min^2)]
      < k^2
      < min[epsilon_TF*M_rho^2, k_interaction_bound^2].

This is a necessary scale separation, NOT a sufficient existence/stability
theorem. Discrete torus-mode membership, the mean equation, actual coupled
characteristics, source-frequency error control and a separate frequency
interaction bound remain required. No action-derived physical cutoff,
on-shell galactic background or complete quasistatic error budget was supplied.
The three hypothetical partial-band examples prove parameter sensitivity only.

**Result: actual physical window UNRESOLVED.** A potential mass parameter or
a freely chosen numerical ceiling was not called the physical cutoff.

## 7. Verification, preservation and work-order consequence

[Package and reproduction instructions](../../Analysis/MAT/MAT-001/PKM1_METRIC_HOST/LOCALITY_2026_10_23/README.md).

- V1 failed 1 of 99 checks: weak symbolic positivity inference before exact
  factorization. Its executable, hash and failed receipt remain.
- V2: 99/99 local checks, zero failed/unknown; fresh read-only exact replay.
- Separate Binet/SI verifier: 19/19, zero failed/unknown; fresh exact replay.
- Maximum Binet/Cartesian precession difference: 2.03777e-14 rad/orbit.
- Maximum registered relative deviation from the first-order orbital result:
  7.2746e-4 (coarse control); smaller force controls reduce it.
- 60 existing source/sidecar/dirty files retained their hashes, sizes and native
  integer mtimes during calculation. All 15 pre-existing dirty files are retained.
- Contract was frozen in the task's authorized secondary workspace before
  execution; the later Core copy has the identical hash. The original task
  artifacts remain; integration uses byte comparisons, not regenerated results.
- The historical receipt integration field records its original run location,
  not the later integrated state. No original scientific sidecar is refreshed.
  The mutable deferred register is appended only after byte-preserving backup.
- The standalone optimizer handled canonical reads. Outside-root task receipts
  used bounded structured inspection; its root boundary was not reconfigured.
- Local independent implementation is NOT independent peer review.

For the next bounded R4C1 task require the actual constraint-admissible sector,
retained means/fixed charges, background two-form drift and a justified physical
kinetic/symplectic map. A frozen Hessian sign, graph norm, finite residual or
one more initial-time derivative alone is not its acceptance criterion.
The further interaction/gravity/force overlap and both genuine matching inputs
would remain necessary even after that task. No expensive PKM1 completion is
opened by this comparison.

## 8. Independent paper track: no new refinement sweep

Repository candidates remain P1 0.2.0-rc7 and P2 0.2.0-rc4. Their current
README/VERSION/SUBMISSION bytes were checked; papers/PDFs were not edited or
rebuilt. P1 still needs the author's final proofread/declaration and metadata/
category decisions plus applicable review. P2 retains the 18/19 stringent
sensitivity failure and unchanged bounded no-attractor classification; final
author confirmation, applicable review and explicit upload/venue decisions
remain. These scoped release decisions need not await full MAT/UVIR closure.
This report does not independently verify an external submission/deposit state.

## 9. Exact principal provenance and unchanged gates

| Artifact | SHA256 |
|---|---|
| Contract V1 | f47060a8d2fb2dcea2c3fa5af6199c13cbb731927fc37bffba83fa4954ab6006 |
| Frozen inputs | 521a7c7838aadaabdcebe0e81cae21abf84d4aa7e67031ad9d2d41018cbd3c8f |
| V2 executable | 0ff06a09d075cd68c020aed2cf401233aac1201c1fc92dc72a0f49d56e70e641 |
| V1 failed receipt | 99f4597a0f1b303f69368f413d0e77bbc44cd0b5d1564391c942426ee1defb46 |
| V2 receipt | 25fd99c937c1cd48defb21dd2ae567d1867cdef415c710963a819ecad56eb3db |
| Independent verifier | 00104897d57d8e0f2a2f23c88faab660440a426b0dc02db062c369dbc1aa5fce |
| Independent receipt | 99feef8fd96f010804e2937de937c11b42abf57ceb0ddbeac95cfbfb1715d116 |

All direct source hashes are in the frozen inputs. Inherit the checked-scope
R4C1 material/seed, energy, weak-generator, initial-admission, GR-family,
weak-source/frame-probe and MAT R4/R5/RM1/ST1/ST2 review dependencies; the
PKM1 parent decision and its local controls remain provisionally used.
Review DEFERRED; Rule9_cleared=false. Local diagnostic research may proceed,
but missing substantive inputs still hold dependent physical claims.

Stage1 accepted only in its registered linear prepared-dust scope;
Stage2 INCOMPLETE; Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS;
Stage4A CLOSED; TOP-X4 unchanged; physics_pass=false; gate_effect=NONE.
No canonical action change, new parent, vault mutation, publication, commit,
push, provider/model dispatch or security/global runtime setting change occurred.

