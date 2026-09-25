# Tests 1–3: derivations, counterexamples and incomplete requirements

Date: 2026-09-25. Working analytical report; independent review pending.
Branch: recovery/v12-core-architecture. Gate effect: NONE.

Operator update, 25 September: independent Rule-9 review is now `DEFERRED`.
The [continuation policy](../Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md) permits
provisional reuse of these locally supported results within the scopes in
the [review register](../Verification/ITSM_RULE9_DEFERRED_REVIEW_REGISTER.md).
Review-only delay is not a research blocker; the substantive requirements
below remain open. Existing receipts retain their original clearance fields.

## 1. Decision, not a claim of three physics passes

| Test | Verified bounded result | Canonical requirement still absent |
|---|---|---|
| 1: action/source vector | Conditional conformal source and stress identities; an explicit reservoir witness shows what conservation does not determine | One accepted, complete ITSM matter/plenum/reservoir action, sector split, admissible finite-density background and GR limit |
| 2: weak field | Spherical conditional force law; universal pointwise extension rejected both locally and on periodic T3; missing harmonic flux identified | Parent-derived metric and force action, exchange-source projection, matched coefficient, physical periodic solution and approximation error |
| 3: blind coefficient | Static-action reference-scale degeneracy and conditional redshift formulas; historical text inventory extended | Complete historical reconstruction, genuinely blinded independent derivation, unique C_chi, action-derived H(z), and subsequent held-out comparison |

Local symbolic receipts are respectively 29/29, 11/11, 9/9; the separate T3
addendum is 19/19. Counts include identities and successful rejection tests.
They are not counts of completed physics requirements. Every receipt retains
`physics_pass=false`, `canonical_test_complete=false`, `gate_effect=NONE`,
and `Rule9=NOT_COMPLETED`.

The initial Test 1 entry hold remains correct **for the complete canonical
action**. The bounded calculation subsequently varied an existing conditional
matter module and a separate nonuniqueness witness. It did not secretly adopt
that witness as the missing ITSM parent.

## 2. Sources and conventions

The controlling work order is
`Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md`; the Test 1 entry
contract and `ITSM_TESTS_01_03_BOUNDED_AUDIT_CONTRACT_2026-09-24.md` bound this
calculation. Conditional source inputs are the working CoreRecovery sections
02, 04 and 05; existing UVIR-001 rejection and MAT-001 matching holds remain
binding. The T3 follow-up has its own dated addendum and does not replace
the original local 11/11 receipt.

Use signature (-+++), natural units c=hbar=1 in the covariant witness, and
T_mu_nu=-2/sqrt(-g) delta S/delta g^mu_nu. All displayed sector divergences
use contravariant stress and raised currents. Scalars have ordinary covariant
derivatives; no nonminimal curvature coupling is inserted.

The conformal-source calculation is consistent with the standard Einstein-frame
matter construction in [Damour and Esposito-Farese](https://arxiv.org/pdf/gr-qc/9602056).
The conditional nonlinear-Poisson/curl distinction has the original
[Bekenstein–Milgrom action](https://articles.adsabs.harvard.edu/pdf/1984ApJ...286....7B)
as precedent. Neither reference supplies the absent ITSM matching constants
or reservoir. The equations below are checked for the explicitly stated
actions, not inferred to hold because another theory uses a similar form.

## 3. Test 1: a source derivation and its exact boundary

### 3.1 Conditional conformal matter module

For S_m[A(psi)^2 g,chi], A=exp(beta psi), varying psi at fixed Einstein-frame
metric gives

```
(1/sqrt(-g)) delta S_m/delta psi = beta T_m,
Q_mp^nu = beta T_m grad^nu psi.
```

This follows directly from delta g_tilde_mu_nu=2 beta g_tilde_mu_nu delta psi
and the stress definition. Matter diffeomorphism invariance then gives
div T_m=E_chi grad chi+beta T_m grad psi; on its matter equation E_chi=0,
the nonzero divergence is the stated current. Bianchi consistency alone
would not have selected A, beta or this current.

The explicit matter scalar used to verify the sign is
L_m=-A^2(grad chi)^2/2-A^4 V_m. Its trace and equation are

```
T_m = -A^2 (grad chi)^2 - 4 A^4 V_m,
E_chi = A^2 box chi + 2 beta A^2 grad psi . grad chi - A^4 V_m,chi.
```

For pressureless matter, T_m=-rho and T_m^mu_nu=rho u^mu u^nu.
Projecting its sourced divergence perpendicular to u gives

```
u . grad u^nu = -beta (g^nu_alpha+u^nu u_alpha) grad^alpha psi.
```

The temporal projection gives grad_mu(rho u^mu)=beta rho u.grad psi.
For homogeneous comoving dust Q_mp^0=+beta rho dot(psi). These signs agree
with the independently computed homogeneous scalar-matter energy balance;
the dust projection itself is the analytic derivation here, not a numerical
dust simulation.

### 3.2 Explicit witness, not a new accepted parent

The full witness Lagrangian and domain are frozen in the bounded contract.
Write s=u^2+v^2, Phi=(u+i v)/sqrt(2), and

```
L_P = -[(grad u)^2+(grad v)^2+Z(grad psi)^2]/2 - V_P - W,
L_R = -(grad r)^2/2 - V_R,
W = lambda*s*r^2/4.
```

V_P=m_P^2 s/2+lambda_P s^2/4, V_R=m_R^2 r^2/2+lambda_R r^4/4,
and V_m=m_m^2 chi^2/2. Z>0; squared masses and quartics are nonnegative.
The Einstein–Hilbert term Mpl^2 R/2 completes this comparator action.
Periodic spatial fields and compactly supported temporal variations (or
the appropriate gravitational boundary term) define the variation.

Varying each kinetic term and potential gives

```
E_u = box u - partial_u(V_P+W),
E_v = box v - partial_v(V_P+W),
E_r = box r - partial_r(V_R+W),
E_psi = Z box psi + beta T_m.
```

Metric variation gives T_P^mu_nu=grad^mu u grad^nu u+grad^mu v grad^nu v
+Z grad^mu psi grad^nu psi+g^mu_nu L_P; T_R and T_m have their corresponding
kinetic dyad plus g^mu_nu L. For a scalar f, metric compatibility and
commutation of second scalar derivatives give
div[grad f grad f-g(grad f)^2/2]=(box f) grad f. Applying the potential
chain rule yields the following exact off-shell identities:

```
div T_P = E_u grad u + E_v grad v + E_psi grad psi - Q_mp + Q_syn,
div T_R = E_r grad r - Q_syn,
div T_m = E_chi grad chi + Q_mp,
Q_syn^nu = -W_r grad^nu r = -lambda*(u^2+v^2)*r*grad^nu r/2.
```

Thus total stress is conserved on shell. The script verifies all four
components in arbitrary flat-chart first/second derivative data and performs
separate homogeneous FLRW continuity checks with arbitrary H. The covariant
extension follows from the tensor identity just given, not from treating
flat jets as a curved-background or Einstein-equation solver.

Moving a constant fraction eta of interaction stress between sectors gives
T_P'=T_P+eta g W and T_R'=T_R-eta g W. Their sum is unchanged, but
Q_syn'=Q_syn+eta grad W. Therefore total conservation cannot fix a sector
exchange convention when the interaction-stress assignment is missing.
Changing the actual interaction W would introduce further physical freedom;
this calculation does not select such an interaction for ITSM.

The U(1) current j^nu=v grad^nu u-u grad^nu v obeys div j=0 on shell because
V_P+W depends on u,v only through s. Q_syn can nevertheless be nonzero.
Energy transfer and condensate-number production are not interchangeable.

### 3.3 Regularity, dimensions and GR

On finite smooth fields and finite positive A, both witness currents are
finite polynomials/exponentials with no inverse coupling or inverse field.
Exact beta=0 and lambda=0 limits agree with their continuous limits. This
does not prove global regularity of solutions, quantum renormalization, an
irreversible reservoir, thermodynamic stability, or a finite-density vacuum.

Natural-unit dimensions are [u]=[v]=[r]=[chi]=1, [psi]=0, [Z]=2,
[m_i^2]=2, [beta]=[lambda_i]=[lambda]=0, [L]=[T]=4, [Q]=5,
[j]=3, [div j]=4. Every displayed current has the appropriate mass dimension.

At beta=0, zero extra fields and derivatives remove extra stress and recover
Einstein gravity with ordinary scalar matter. This is a comparator GR branch,
not a proved limit of a finite-density ITSM solution. Zero transfer alone
is insufficient: an uncoupled reservoir with r=0 and dot(r)=1 still has
energy density 1/2 in the normalized witness units.

## 4. Test 2: conditional force and the T3 correction

The declared static action varies to

```
laplacian Phi_N = 4*pi*G*rho,
div[(|grad psi|/a0) grad psi] = 4*pi*G*(Cm/CIR)*rho.
```

The parent covariant action has not derived this cubic spatial-gradient term.
For the spherical positive-mass branch, regular-origin flux and no added
homogeneous flux give q^2=(Cm/CIR)*a0*G*M(<r)/r^2. With the same conditional
matter coupling the extra inward force is Cm*q, hence

```
g_tot = g_N + C_obs*sqrt(a0*g_N),
C_obs = Cm^(3/2)/sqrt(CIR).
```

This uses weak potentials, slow matter, a quasistatic force sector, positive
coefficients, spherical alignment and declared boundary conditions. In SI
units [Phi_N]=[psi]=L^2/T^2 and [a0]=[q]=L/T^2; Cm,CIR are dimensionless.
The conformal factor is exp(2 Cm psi/c^2). To first order it changes the
matter-metric potentials to Phi_m=Phi_E+Cm psi and Psi_m=Psi_E-Cm psi.
Identifying Phi_E with the Newtonian solution above is an additional static
baseline approximation; the full Einstein-frame metric and its extra-sector
backreaction have not been solved.

Cm=CIR=1 already gives C_obs=1 rather than 2/3. Choosing Cm^3/CIR=4/9
would impose the desired coefficient, not derive it. The existing canonical
UVIR-001 failure to generate this spatial cubic term is not repaired here.

### 4.1 Global topology is not spherical symmetry

For a periodic T3 source, use compensated density contrast, not an isolated
positive total mass in a periodic Poisson equation. The source integral must
vanish. A small, approximately spherical compensated patch can be a local
control, but its error from the surrounding field and compact geometry has
not been bounded. Topology alone also does not specify a flat spatial metric.

For an explicit allowed flat-T3 snapshot set Phi_N=cos x+2 cos y on periods
2*pi. Its Laplacian has zero mean; an adequate homogeneous density ensures
nonnegative total density. The algebraic candidate
v=grad Phi_N/|grad Phi_N|^(1/2) has the correct nonlinear flux divergence,
but at x=y=pi/4 its curl_z=-10^(3/4)/50, not zero. It therefore cannot be
a scalar gradient. This rejects a universal pointwise force prescription
on T3, not the periodic nonlinear PDE or the entire ITSM identity.

### 4.2 Harmonic flux was missing from two working equations

In the flat periodic, S_Q=0 baseline the correct global decomposition is

```
|grad phi| grad phi/a0 = (Cm/CIR) grad Phi_N + curl H + h0,
h0 = mean[|grad phi| grad phi/a0 - (Cm/CIR) grad Phi_N].
```

Proof: the difference is divergence-free. For each nonzero Fourier vector n,
n.F_n=0 and H_n=i n cross F_n/|n|^2 gives i n cross H_n=F_n. The zero mode
is h0 and cannot be a periodic curl. It is a solution-dependent flux mode,
not a new tunable acceleration or condensate phase winding.

The omission is not harmless in general: for phi=sin x+(b/2)sin(2x),
mean grad phi=0, yet d/db mean(|grad phi| grad phi)|_(b=0)=4/(3*pi).
Periodicity does not force zero mean nonlinear flux. Working CoreRecovery
section 05 and P1's compact-source equation are corrected accordingly;
frozen releases and existing PDFs are not changed or revalidated.
For nonzero S_Q an independently derived source contribution is required;
for curved spatial metrics the harmonic representatives depend on the metric.

## 5. Test 3: what the force action actually identifies

Besides force-field chart freedom, the static sector has a reference-scale
freedom: a0 -> ell*a0 and CIR -> ell*CIR, ell>0. This leaves CIR/a0 and the
entire static action unchanged, but changes C_chi=a0/(cH) by ell.
The force determines the combination

```
a_dyn = (Cm^3/CIR)*a0,
C_dyn = a_dyn/(cH) = C_obs^2*C_chi,
```

not a0 and C_obs independently. This is an identifiability result for the
declared static sector, not a no-go theorem against an eventual parent
normalization that independently fixes them. Matching and an action-derived
background are still required. [cH]=[c^2/L]=L/T^2 verifies dimensions but
cannot determine a dimensionless coefficient.

The frozen candidate set remains 1, 2*pi, 1/(2*pi), sqrt(1-q_dec)/(2*pi),
and an absent independent action-derived result. No observed a0 or H0 value
was input to the symbolic calculation. Because historical values had already
been seen, this is data-independent calculation, **not fresh analyst blinding**.
No observational ranking or coefficient selection has been performed.

For constant C_chi, a0(z)/a0(0)=H(z)/H(0) is conditional. For the curvature
branch it is H(z)/H(0)*sqrt[(1-q_dec(z))/(1-q_dec(0))], in the positive real
domain q_dec<1, with
d ln a0/dN=-(1+q_dec)-q_dec,N/[2(1-q_dec)]. Neither expression supplies H(z).
Fixed comoving length and a0 proportional to c^2/L_phys give a0 proportional
to a^-1; fixed physical length gives constant a0. Simultaneous fixed comoving
length and L_phys=c/H require q_dec=0. Present-epoch matching alone does not
establish a time-dependent topology relation.

### 5.1 Historical provenance and its limits

The separate lexical inventory covers declared history/manuscript/P1 text
plus main-branch text at commit 8183db8feb97fe0aa59c9ce8e99d37ac5559128a.
The source hashes, encodings, per-file matches and context windows are in
`Analysis/MasterTests/outputs/acceleration_history_inventory.json` and its
companion JSONL. Three legacy main files require declared CP1252 decoding;
the warnings are retained. This is not a mathematical parser or proof that
every original equation has been recovered.
The inventory is a source-hashed snapshot made before the later working
conservation-section correction. It was not refreshed after the user parked
historical work; it must not be advertised as a current-worktree hash check.

| Family | Available provenance | Disposition |
|---|---|---|
| Multiplier 2*pi*cH0 | `Theory/History/FullArchive/manuscripts/07_v5-line-2026-03-09/v5.1-v5.5_delta_notes.md`, lines 27, 61–64 | Historical extraction reports multiplier with inconsistent numerical packaging; original equation-level reconstruction remains incomplete |
| Divisor cH0/(2*pi) | `Theory/History/FullArchive/manuscripts/08_v5.7-v6.0-2026-03-09/v5.7_source.md`, line 63; v5.8/v5.9 line 63 | Available transcriptions assert topology derivation, but do not supply action matching; not accepted as Derived |
| v7.2 circulation-to-acceleration chain | `ITSM_TEST_03_HISTORICAL_CHAIN_ADDENDUM_2026-09-25.md`; pinned transcription lines 57, 61, 65 | Exact audit rejects the chain as transcribed: `kappa/ell=c` is a speed, while the printed middle expression is `cH0`; the original PDF remains unverified and no independent `C_chi` follows |
| DSM divisor, explicitly conditional | P1 `main.tex`, equation `a0-phen` | Current phenomenological present-epoch scale postulate |
| c^2/(2*pi*L), L=alpha*c/H0 | P1 `main.tex`, topology-scale discussion | Additional modulus/length relation, not fixed by T3 identity |
| Unit and sqrt(1-q_dec)/(2*pi) | User programme and bounded audit contract | Preregistered comparators here; historical origin not asserted without source recovery |

The multiplier/divisor ratio is exactly 4*pi^2, so exchanging them is not
notation-only. This audit does not import any historical observed value to
choose between them. Listed PDFs and unavailable/unknown aliases remain an
explicit coverage gap; the earlier 499-hit scan is preserved separately.
For the pinned v7.2 transcription, the additional exact audit finds
`kappa/(2*pi*ell)=c/(2*pi)` but the printed middle expression is
`c*H0/(2*pi)`: the ratio is `H0`, so the displayed equality drops a frequency
factor and equates quantities with different dimensions. A flat periodic
geodesic can carry nonzero cycle circulation with zero intrinsic spatial
acceleration, so circulation alone does not repair the inference. This rejects
that chain **as transcribed**, not the unverified original PDF or every possible
model with an additional dynamical relation. The receipt records no observed
input, derives no `C_chi`, and leaves full historical reconstruction open.

## 6. Requirement-level continuation and review

The user directed work back to the current recovery theory; historical
reconstruction is parked, not declared complete. The live Stage-B FRW record
already contains a representative dimensionless on-shell expanding control
with no reservoir exchange. It must not be described as though no background
calculation exists. What remains absent is the complete selected interacting
parent and its physical, matched cosmological prediction, not all homogeneous
equations whatsoever.

The current RES-001 E0/E1 record requires a surviving system parent before
selecting reservoir variables and their interaction. The RCP-I1-C action class
has an unmatched conformal function and explicitly omits reservoir content;
it cannot be joined silently to the separate Track-A or TOP-X4 namespaces.
Proceeding beyond the current-action disposition therefore requires an
explicit action-selection/completion decision, not another numerical receipt.
The working conservation section's stale two-bath/Spohn claim was also
corrected against the actual current single-mode Kerr implementation; this
changes claim accuracy, not the absent action-level reservoir physics.

1. Test 1 needs selection and freezing of a complete identity-preserving
   parent, including S_R, S_int, sector-stress assignment, finite-density
   state and renormalization scope. The witness cannot be promoted to fill
   this gap. Existing rejected parents remain rejected in their tested scope.
2. Test 2 needs the parent-derived metric/force/Euler system, Test 4's matching,
   Test 5's admissibility, exchange projection, physical periodic solution,
   and quantified local approximation. A conditional solver may test methods
   but cannot supply missing parent physics.
3. Test 3 needs equation-level provenance closure, a declared reference
   normalization, an independent data-blinded derivation and H(z), followed
   only then by preregistered observational comparisons.
4. Roles A/B/C review of the exact sealed evidence is deferred under the
   operator's current policy. Scoped provisional research continues while
   this is pending. Final canonical promotion and publication readiness
   still require the applicable scientific checklist and review.

The active goal is **not complete**. MAT-001 remains BLOCKED, UVIR-003
IN_PROGRESS, K_Q NOT_DERIVED, V NOT_COMPUTED, Stage4A CLOSED. No downstream
Derived promotion, commit, push, deployment or publication is authorized by
these local results.

### 6.1 Approved current-action continuation: R4C1

The user subsequently approved a separately labelled four-dimensional
reservoir completion using the current v12 fields, without changing TOP-X4
or canonical gate statuses. The [R4C1 first-variation report](RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md)
records the frozen candidate and 119/119 exact local checks. It retains the
current frame/alignment/force operators, adds a neutral reversible reservoir
portal and explicit dust matter, and derives conditional interface currents.
The full U(1) current includes the alignment contribution; energy exchange
does not imply charge creation. This is not adoption of the earlier witness
as a canonical parent. The subsequent [complete classical variation report](RES-001/RES001_R4C1_FULL_VARIATION_REPORT_2026-09-25.md)
supplies the frame/regulator metric variation and general Ward ledger,
supported by 162/162 checks and two exact four-dimensional off-shell probes.
The [R4C1-B1 continuation](RES-001/RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md)
then supplies one finite-time homogeneous interacting background control,
48/48 checks, with conserved finite charge and nonzero currents. Its
constraint residual is 3.41e-12; its separately differenced sector balances
reach 7.96e-8. This arbitrary classical parameter point is not a calibrated
or stability-verified cosmology and has no demonstrated EFT scale hierarchy.
The [R4C1-G1 audit](RES-001/RES001_R4C1_GR_LIMIT_REPORT_2026-09-25.md)
then passes 56/56 checks that include rejection of a false GR implication:
turning off exchange while retaining the B1 frame gives G_cos/G_static=5/6.
The registered six-member family approaches an Einstein-dust background,
but K_T=eta/6 vanishes and A/K_Q^(3/2) grows as eta^(-1/2). It does not
establish a healthy perturbative GR limit or rule out every other path.
The charge-energy bound also distinguishes the scalar-free endpoint from
GR with separately conserved spectator scalar matter. This is a physical
limitation, not solely a label or Rule-9 obstacle. Test 2 must distinguish
bare G from measured static response; the full matched law is still open.
Healthy continuous GR recovery, interacting physical perturbations, scale
validity, unique coefficient matching and Rule-9 review remain open.
Historical reconstruction stays parked. The programme objective above
remains incomplete; no gate or publication status changes.

The [R4C1-C1 current-action audit](RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md)
adds 63/63 checks. Unlike section 5's unchanged-action reference rescaling,
A -> lambda A at fixed K_Q,b,beta changes an invariant physical coupling.
Nevertheless, the full homogeneous background equations and classical
pre-constraint quadratic action are A-independent. Registered A ratios
1/4,1,4 yield identical state/current histories, while the conditional
spherical force amplitudes have ratios 2,1,1/2. Direct radial variation
retains the regulator and exposes the condition for neglecting it.
Thus background plus linear matching alone cannot predict this nonlinear
force coefficient. This does not prove a complete galaxy solution, a healthy
parameter interval, or an all-parent no-go. No C_chi or a0(z) is selected.

The [R4C1-S1 scalar reduction](RES-001/RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md)
now passes 71/71 checks with all four auxiliary constraints retained. It
exports the pre-constraint and reduced K,M,V and proves positivity of the
classical scalar kinetic form at B1 coefficients in the regular H!=0, k!=0
chart. All 6,408 sampled matrices also have positive inertia (6,0,0). This
addresses a real missing calculation without implying gradient/all-sector
stability, a healthy GR limit or matching of A. S1 inherits the unreviewed
variation/background evidence; R9-MT1-S1 is deferred and available for
provisional downstream diagnostics.

The [26 September R4C1-S2 propagation report](RES-001/RES001_R4C1_SCALAR_PROPAGATION_REPORT_2026-09-26.md)
passes 56/56 checks, derives the formal scalar branches and verifies two-method
finite-time transfers. The double zero branch is defective in the leading
scaled chart, so well-posedness remains unestablished. The wider condensate
cone and quartic force dispersion also require causal/EFT interpretation.
The first failed implementation is preserved; its missing-Mcdot principal
term was corrected without changing physics or tolerances. No full stability
claim or canonical closure follows. Review of this corrected result is deferred.

The [R4C1-S3 regularity disposition](RES-001/RES001_R4C1_ZERO_BRANCH_REPORT_2026-09-26.md)
passes 57/57 checks: an exact Jordan sequence rejects the equal-order bound,
but a preregistered original-variable graph norm has a finite positive large-p
limit on the restricted frozen zero sector with explicit derivative/domain
requirements. The independent pressureless control supports the regularity
distinction. The full coupled initial-value problem remains unproved; this
does not erase S2's degeneracy or establish an all-formulation pathology.

### 6.2 Requirement-level status after R4C1-G1/C1/S1/S2/S3

This is a completion audit against the actual programme, not a claim that
check totals fulfill its requirements. 'Supported' below is candidate/local
evidence, not independent review or canonical admission.

| Requirement | Current evidence and disposition | Remaining obligation |
|---|---|---|
| Test 1: specified off-shell action, fields, units, matter metric, boundaries and sector split | R4C1-v1 freeze supplies a complete classical candidate; dust and reversible neutral reservoir scope explicit | Canonical parent acceptance, physical applicability and independent review remain open |
| Test 1: every field/metric variation, stress tensors, source vectors and conservation | First-current and full-variation reports give explicit equations, stresses, Ward ledger, regular portal/current controls and split dependence; B1 supplies nonzero-current on-shell control | Independent mathematical/numerical verification; do not infer microscopic, irreversible or radiation/BBN completion |
| Test 1: charge distinct from energy exchange | Alignment-corrected conserved U(1) current, S_N=0; portal energy transfer may reverse | Any proposed production/thermodynamic mechanism needs a separate derivation |
| Test 1: declared uncoupled GR control | Algebraic scalar-free Einstein-dust endpoint supported; G1 rejects zero exchange alone as sufficient and flags a nonuniform registered perturbative path; S1/S2 reduce interacting scalar constraints, certify the bounded kinetic form and derive formal propagation/evolution | Healthy physical parent/limit, zero-branch well-posedness, causality, homogeneous/singular sectors and EFT validity remain unestablished; not an all-path failure |
| Test 2: metric, Euler and modified-Poisson system | Conditional conformal Euler law and local static variational form; G1 fixes frame-control static G; C1 retains the radial regulator | Complete coupled inhomogeneous matching and a nonempty common approximation/EFT domain |
| Test 2: topology and boundaries | Periodic counterexample rejects universal pointwise algebraic law; harmonic flux restored in working equations | Physical compensated periodic solution and quantified local error |
| Test 2: numerical projection factor | C_proj remains explicit | Independent Test-4 derivation; 2/3 cannot be imposed to claim closure |
| Test 3: historical equation reconstruction | Partial lexical/equation provenance; the v7.2 circulation chain is rejected as written in its available transcription | Parked by user direction; original-source verification and complete equation-history reconstruction remain open |
| Test 3: unique blind C_chi | C1 proves homogeneous/classical-linear data cannot identify physical A; static reference redundancy also remains | A target-independent matching principle and genuinely independent blinded derivation |
| Test 3: registered comparator set and observational ordering | Four symbolic comparators retained; C1 rejects reverse target assignment as prediction | Independent fifth result absent; no target-data comparison or ranking is justified yet |
| Test 3: H(z), q_dec and a0(z) from the same physics | B1 is a finite-time uncalibrated action-derived homogeneous control; C1 degeneracy leaves its history unchanged | Physical cosmology, local-frame matching, projection and acceleration evolution not derived |
| Every test: provenance, reproducibility, rejection checks and review | Frozen contracts, source pins, reproducible receipts and explicit false-claim controls available | Independent Roles A/B/C have not reviewed this exact evidence; no self-certification |

The missing acceleration matching is a physics input, while independent
review is a separate evidence requirement. Neither is repaired by renaming
a status. The [local review workflow](../../docs/ITSM_MASTER_TEST_REVIEW.md)
now prepares source-hashed private snapshots and exact role mandates without
dispatch. Its pre-S1 roster checks ten receipt dependency chains, includes the
complete Core Identity and current governance in every prompt and preserves
failed/unknown checks. Reviews are deferred; earlier partial outputs and
snapshots remain preserved. The mandatory GEMINI example is an explicit
target-priming limitation; fresh sessions and phase-labelled directories
alone cannot establish blinding or permission isolation. Paid/provider
review still requires its own authority and verified runtime boundaries.
The earlier snapshot contains none of S1-S3 and must not be called their review.
Substantive programme requirements remain open. The next candidate research
step is a frozen complete coupled principal/subprincipal evolution estimate
in declared mixed-regularity scalar spaces, using the corrected S2 equations
and S3 original-variable reconstruction. Independent review is outside the
active research critical path until resumed by the operator.
