# MAT-001 ST2: a finite quantum threshold does not select the remaining physical input

13 October 2026. Result `MAT001-ST2-v1`; claim **Conditional**.
[Frozen contract](MAT001_ST2_HEAVY_THRESHOLD_SCREEN_CONTRACT_2026-10-13.md),
SHA `23cd8257796169a97045961cd5bd7624fd829f557cc2869ee38f9d2859e9a0e7`.

## Result

One explicitly declared heavy real scalar produces a calculable bulk kinetic
threshold. It changes the ST1 normalization but does not fix the independently
allowed renormalized kinetic coefficient. The curvature coupling and potential
also require retained renormalization inputs. A nonconformal heavy coupling
can change the same-scale probe's fractional mass vertex, but no full physical
pole or numerical ITSM coupling is identified.

There is a second, independent obstruction in the conformal-heavy subclass:
the one-loop Einstein potential has a strictly positive logarithmic slope.
Its vacuum scalar cannot simply be presumed to sit at a constant background
with a gapless pole. This is a scoped result for the displayed bulk control,
not a no-go theorem for ITSM or all quantum/finite-density completions.

Disposition: `THRESHOLD_COMPUTED_RENORMALIZED_INPUTS_AND_PHYSICAL_BACKGROUND_OPEN`.

## 1. Bulk determinant and renormalization inputs

The contract retains the complex finite-density condensate and adds a separate
real H with mass squared `X=g sigma^2`, g>0. Quantize H only; all other fields
and probes are external. Its Euclidean operator is

```text
D=-nabla_E^2+X+eta R,  E=-(X+eta R)
Gamma_H=(1/2) Tr log D.
```

The standard a4 bulk terms `E^2/2+RE/6` give
`X^2/2+(eta-1/6)XR+O(R^2)`. In the declared pole convention the corresponding
real-field effective-action pole is

```text
Gamma_pole = integral sqrt(g_Eucl) [
  -X^2/(64 pi^2 epsilon) -(eta-1/6) X R/(32 pi^2 epsilon)
  +curvature-squared and total-derivative terms].
```

Thus sigma^4 and sigma^2 R counterterms are needed in the generic subclass;
curvature-squared terms remain required even when eta=1/6. The integrated
Box X term vanishes on the boundaryless compact bulk control. Expanding
Box(sigma^2) and retaining only its gradient-squared part would invent a
kinetic UV pole by omitting the compensating sigma Box sigma term.

For one real scalar, the specified minimal-subtraction finite potential is
`U1=X^2[ln(X/mu^2)-3/2]/(64 pi^2)`. Its linear-curvature Euclidean coefficient
is `(eta-1/6) X[ln(X/mu^2)-1]/(32 pi^2)`. Euclidean gravity is `-F R/2`,
whereas the Lorentzian convention is `+F R/2`; this fixes the sign of Delta F.
No sign is imported from a paper using a different Lorentzian convention.

The external curved-space scalar potential provides an independent control:
[Markkanen et al., JHEP06(2018)040](https://arxiv.org/abs/1804.02020), scalar
equation (20), expands the curvature-shifted mass `X+(eta-1/6)R`. Only that
scalar local-potential structure is used, not its Standard Model calculation.
The determinant/pole convention and bulk coefficients were checked against
[Vassilevich, Phys. Rept.388(2003)279](https://arxiv.org/abs/hep-th/0306138),
equations 2.2, 2.31-32, 3.6 and 4.27-28, including through alphaXiv raw pages.

## 2. Independent finite kinetic calculation

Expand the real-field determinant around constant X. Its quadratic term is
`Gamma2=-(1/4) integral delta X(q) delta X(-q) I(q)`, with q=p_E^2. The
renormalized bubble difference and its small-momentum coefficient are

```text
I(q)-I(0)=-(1/(16 pi^2)) integral_0^1 dx ln[1+x(1-x)q/X]
I'(0)=-1/(96 pi^2 X).
```

The independent convergent radial momentum integral gives
`J3=integral d^4l/(2pi)^4 (l^2+X)^(-3)=1/(32 pi^2 X)`, and
`I'(0)=-2 J3 integral_0^1 x(1-x) dx`. Comparing Gamma2 with
`Delta Z (grad sigma)^2/2` gives

```text
Delta Z=(X')^2/(192 pi^2 X)=g/(48 pi^2).
```

The real-field half and the quadratic-expansion minus sign are both essential.
This finite threshold is not the full coefficient: `Z=zeta(mu)+Delta Z`.
The local kinetic operator is independently allowed in the parent action,
even though this particular H determinant has no bulk kinetic UV pole.

## 3. Loop-corrected frame and signed probe vertex

Write the displayed one-loop two-derivative coefficients as

```text
L=ln(g sigma^2/mu^2)
a=(eta-1/6)g/(16 pi^2), b=g/(48 pi^2), c=g^2/(64 pi^2)
f=xi-a(L-1)
F=sigma^2 f
Z=zeta+b
U=sigma^4 [lambda/4+c(L-3/2)].
```

For F>0, `g_E=(F/M_P^2)g_J`. With `tau=ln(sigma/sigma0)` oriented toward
increasing sigma, the local Einstein normalization is

```text
K_tau=M_P^2 B_local
B_local=Z/f+6(1-a/f)^2
m_E=m_J M_P/sqrt(F),  m_J=m_a0 (sigma/sigma0)^p
r=d ln(m_E)/d tau=p-1+a/f
V_ST2,local=r/(M_P sqrt(B_local)), g_can=-V_ST2,local.
```

Admit the strictly positive finite kinetic interior only. The metric mixing
must be included, and the source sign follows variation of the declared
worldline mass. The normalization method agrees with the general scalar-tensor
coefficient structure in [Jarv et al., PRD91 024041](https://arxiv.org/abs/1411.1947).
These are off-shell block/mass-vertex identities, not a computed live physical
mode residue. K_tau is not canonical ITSM K_Q.

This expression is exact algebra in the displayed truncated action, not an
all-orders prediction. The strict loop expansion was separately checked:

```text
B0=6+zeta/xi
Delta B=b/xi+zeta a(L-1)/xi^2-12a/xi
V_ST2,local=(1/(M_P sqrt(B0))) [p-1+a/xi-(p-1)Delta B/(2B0)]
             +higher-loop terms.
```

At eta=1/6, a=0 and p=1 still cancels the direct mass/frame vertex.
For generic eta, the logarithmic F slope changes that conclusion: the p=1
vertex numerator is a/f. This is a parameterized running-frame effect, not
a derivation of a baryon coupling or proof of a massless static force.
The B_tree=0 Weyl gauge boundary is excluded. A partial determinant does not
establish complete anomalous Ward identities or create a physical gauge mode.

## 4. Identifiability survives the calculated threshold

At fixed F and heavy determinant, `partial B_local/partial zeta=1/f`.
For nonzero r, varying the independent kinetic input changes the normalized
vertex. This cannot be removed by a positive sigma-chart rescaling. The
executable checks the simultaneous transformations of g, xi, zeta and lambda.

The registered off-shell counterfamily has identical g=1/4, eta=1/6, xi=1/4,
sigma0=2, L0=0, p=0, M_P=1 and retained condensate/reference inputs:

| Independent zeta | B_local | Signed local V (rounded) |
|---:|---:|---:|
| 1/2 | 8.00211085799 | -0.35350675601 |
| 2 | 14.00211085799 | -0.26724109596 |
| 6 | 30.00211085799 | -0.18256776304 |

They are positive-kinetic coefficient controls, not solutions of the complete
radiatively corrected background or observationally admissible ITSM models.
Their differing residues demonstrate underdetermination of this control.

A scheme change that redistributes a finite local term between renormalized
input and threshold while keeping full F,Z,U fixed does NOT change physics.
The executable checks that invariance. The counterfamily instead changes an
independent physical boundary input at fixed determinant; it is not a claimed
scheme ambiguity in an already matched observable.

Heavy-H-only scale cancellation, treating g and eta as fixed at this order,
requires `d xi/d ln(mu)=-2a` and `d lambda/d ln(mu)=8c`. These equations retain
arbitrary xi/lambda boundary values; they do not select them. No full-theory
beta functions, fixed point, compositeness condition or ultraviolet matching
boundary has been computed. Setting allowed bare coefficients to zero is
an additional microscopic hypothesis requiring justification.

## 5. Radiative potential and background obstruction

The Einstein potential is `U_E=M_P^4 U/F^2`. In the eta=1/6 subclass,

```text
U_E=(M_P^4/xi^2) [lambda/4+g^2/(64pi^2)(L-3/2)]
d U_E/d tau=M_P^4 g^2/(32pi^2 xi^2)>0.
```

No finite constant-sigma vacuum stationary point exists at this displayed
order for g>0. A finite quartic boundary-value change only adds an Einstein
constant; it cannot erase that slope. A Jordan potential extremum is not by
itself the Einstein scalar stationarity condition in a varying-F theory.
Additional fields, explicit scale-breaking operators, finite-density/reservoir
balance or a different matched parent require separate declared calculations.
This is not a solved cosmological trajectory, mass spectrum or general no-go.

## 6. Verification and preserved incomplete attempts

[Executable](../../../Analysis/MAT/MAT-001/ST2_HEAVY_THRESHOLD/mat001_st2_heavy_threshold_screen.py),
SHA `67df769d9ff2dd1732b482834db8004b8b8bc6b9d78338fee78e0317ba5318eb`.
[Attempt-03 receipt](../../../Analysis/MAT/MAT-001/ST2_HEAVY_THRESHOLD/outputs/st2_attempt_03/summary.json),
SHA `1bec7f5737b89d13ca9ba0aa315f00166185b7aa6067cadb7ee950f8214161f5`.
**107/107 local checks**, no failed/unknown checks, 12 rational/mass-law
controls at 80-decimal arithmetic precision. All ten source pins independently
rehash correctly; contract/executable/receipt sidecars match. Arithmetic errors:

```text
max convergent radial integral relative error: 2.10843958865e-81
max finite-momentum bubble derivative relative error: 2.97619047619e-58
max independent signed mass-frame derivative error: 5.27109897162e-82.
```

The bubble uses three finite nonzero momentum evaluations and a quadratic
Richardson extrapolation; its error is distinct from 80-digit rounding.
Nine negative controls retain real-field factors, curvature/source signs,
metric mixing, running-frame dependence, kinetic input freedom, potential,
total-derivative cancellation and canonical nonpromotion. These are same-parent
checks, not independent Rule-9 review or an exact finite-volume determinant.

Two earlier runs were interrupted without scientific receipts. Attempt 01
returned exit 1 with no stdout after a prolonged run; attempt 02 instrumented
the identical source and reached the counterfamily check before its delay.
No failed scientific assertion was observed; no pass is inferred from progress.
Their exact source is preserved privately as
`.local/itsm-context/st2_interrupted_attempt01_source.py`, SHA
`b472f42beb2549603ca3615a407648fd5c4e2229c3242af9517bd20fd2e8c922`.
The private attempt note, trace wrapper and heartbeat preserve that history.
The diagnostic did not establish exactly which symbolic call stalled.

Attempt 03 strips the nonzero M_P sqrt(B) factor before simplifying the
wrong-source-sign negative control. The zero/nonzero rejection criterion is
equivalent in the registered positive interior. No action, parameter, contract,
physical domain or acceptance threshold changed. Its actual run and a fresh
untraced replay both completed in seconds. Successful optimizer output is
`.local/itsm-context/output-fb84293b9f5b4b33ba76b6016791fef9.txt`, SHA
`5842b2b79a5994991491a0caf1b5b9d7100470db4f274ead72407ddda9323b82`.

The fresh ignored `.local/itsm-context/st2_replay_2026_10_13/` receipt and
sidecar match attempt 03 byte-for-byte. The original ST2 and preceding ST1
receipt/sidecar hashes, byte sizes and modification timestamps remain unchanged
through replay (four protected files). This verifies reproducibility, not physics.

Reproduce only into a new output directory:

```powershell
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MAT/MAT-001/ST2_HEAVY_THRESHOLD/mat001_st2_heavy_threshold_screen.py --out .local/itsm-context/st2_new_replay
```

## 7. Missing physical inputs and next research boundary

The condensate metric embedding g_bar is fixed in the parent, not silently
redefined after the loop. For generic running F it is no longer a sigma-free
spectator in the final Einstein chart. A complete finite-density constraint
calculation must retain that induced coupling. The new H/portal and probe mass
law are assumptions, not microscopic identifications with ITSM or baryons.

Substantive missing inputs remain: independently justified renormalized
boundary values or a microscopic relation selecting them; a consistent
radiative background and live constrained physical pole; nonlinear
preferred-frame/reservoir and Y^(3/2) matching; physical GR/observable metric
and cutoff; finite-volume/state/quantum boundary completion. Analytic local
vacuum heavy-field coefficients do not supply the missing finite-density
nonanalytic spatial law. No measured Newton constant or galactic target is used.

The next identifying work must specify a justified UV matching condition or
microscopic mechanism and carry its background/source constraints through to
the physical mode. The present one-loop threshold alone is insufficient.
Inherit ST1, route, R4/R5 and relevant core/UVIR review debt. The ITSM memory
workflow preserved Conditional status and inherited dependencies; evidence
comes from pinned current sources and the declared calculation, not memory.

```text
research_execution=PROCEED_PROVISIONALLY (scoped diagnostic reuse)
canonical_matching=HOLD_SUBSTANTIVE
canonical_Tests_1_3=HOLD_SUBSTANTIVE
MAT-001=BLOCKED
UVIR-003=IN_PROGRESS
V=NOT_COMPUTED
K_Q=NOT_DERIVED
Stage4A=CLOSED
TOP-X4=UNCHANGED
physics_pass=false
gate_effect=NONE
review_status=DEFERRED
Rule9_cleared=false.
```

Only new ST2 scientific artifacts and the living deferred-review entry/digest
are written. Private backups, instrumentation, logs and replay remain ignored.
No memory/vault/provider/runtime/manuscript/commit/push/publication change.
