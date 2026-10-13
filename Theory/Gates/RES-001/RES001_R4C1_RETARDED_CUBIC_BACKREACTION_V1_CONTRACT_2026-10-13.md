# R4C1: retarded cubic backreaction and dust-clock timing, V1

Date: 13 October 2026. Frozen before the executable.
Owner: Master Test 1 / RES-001 / Stage 2 of the unchanged-action continuation.
Authority: operator approval for a bounded coupled-interaction/physical-window
calculation. The full dust-GR-weak-field objective and Stage-2 GO criteria
remain intact. This is not a new microscopic parent or a redefinition of GO.

## Calculation, state and boundaries

Use the newly checked generic planar WWR and intrinsic W4 functional with the
complete generic quadratic response Hessian. Use **retarded prepared data**
on t in [0,1/20], not a presumed finite-density FLRW S-matrix. Background and
first transverse standing wave follow the same varied action and approved
family initialization. W(0)=1, W_t(0)=0. The source-dependent mean and 2k
constraints are retained; their free reduced response coordinates and
velocities start at zero, as in the pinned time-response archive.

Retain all three families, their scalar/potential/portal/matter scalings and
their independent background prescription. Registered new grid:
eta=1/4,1/64,1/1024, coordinate k=40, all three families, both DOP853 and
Radau. This interrogates the common GR endpoint; it does not clear the
unexamined family/domain range or a continuous physical frequency band.

Solve the **full** evolving mean/2k coupled response, including lapse,
spatial metric, Cartesian scalars, phase/force, dust, normal/multiplier and
regulator constraints. Retain its affine offset, inverse and basis drift.
Do not continually project evolution onto a slow graph. Existing trajectories
are immutable controls for the eta=1/4 cases, not replacement response data.
Their 22-field accelerations were not all archived as actual derivatives;
derive which derivatives the new self-force uses before consuming them.

From L_WWR and L4 derive the order-three **transverse vector equation**.
Its external first-direction variation includes delta B=sigma delta W.
Thus the source is E_W+sigma E_B, not E_W alone. Reconstruct the compatible
third-order transverse shift from its own constraint as a check; do not
infer the full third-order metric/matter response is solved. Those remaining
order-three sectors and a full nonlinear solution remainder remain open.

Separate intrinsic contact and exchange through the complete second-order
response; decompose exchange by response-field sector for diagnosis only.
The **total**, not the chart-dependent sector split, is the timing diagnostic.
Use the correct frame mass and evolving volume in every Green function.

## Nonanalytic force and infinite spectra

Do not construct a Taylor cubic vertex for -A Y^(3/2) at Y=0. Prepared force
response is e|e| R_c; analytic response is e^2 R_a. The order-three force
source on this ray is -6 A |psi_dot|^3 |W| R_c,Vy. Keep its real directional
origin, including W=0. Retain the n=1,3,5 retarded force responses and compute
their multiplication by |cos(theta)| by **exact convolution**, not by an
angular quadrature that smooths the cusp. For positive odd m the coefficient
uses h_(m-n) r_n+h_(m+n) conjugate(r_n), where
h_l=2*(-1)^(|l|/2+1)/[pi*(l^2-1)] for even l (including h_0=2/pi), and zero
for odd l. Cosine prepared force responses are real; check that invariant.

Evolve third-order cusp modes 1,3,5. This finite list is not a finite-mode
closure. Provide analytic continuous bounds for (a) omitted second-order
force responses feeding the third-order source and (b) all omitted
third-order output modes. Leave numerical-solver error and a true nonlinear
remainder separate from these mathematical harmonic-tail certificates.
Scale second-order cusp states by eta^(7/2) and third-order cusp states by
eta^7 during integration to avoid absolute-tolerance loss at small eta.
Restore physical coefficients when recording data. This is a declared
numerical variable change, not a changed action, target fit or GR admission.

## Timing diagnostic and physical interpretation

At theta=0 the prepared reflection symmetries make the longitudinal/x
relative velocities vanish. In dust-clock gauge, T=0 and N=C_bg/C imply that
the dust velocity is the ADM normal and physical dust proper time is the
background tau. The signed transverse velocity in its orthonormal tetrad is
sqrt(h_yy)/a times the transverse chart velocity. This supplies a local
observable, not a coordinate oscillation frequency.

Let t0 be the first simple zero of W. With e>0, define
t1=-r_c(t0)/W_t(t0),
t2=-[w3(t0)+r_c,t(t0)*t1+W_tt(t0)*t1^2/2]/W_t(t0).
Then tau1=C_bg*t1 and tau2=C_bg*t2+C_bg,t*t1^2/2. The tetrad correction
Myy*W/2 vanishes at t0; prove that it does not alter t2. Under e reversal the
root expansion is t0+|e| t1+e^2 t2, not a sign-flipped clock shift.
Report coefficients in the initial positive frame-residue normalization
xi=sqrt(f2)*e (a(0)=1), and keep this distinct from a time-dependent
canonical mass substitution. A local W->W+gamma W^3 redefinition, applied
with the same physical prepared data, cannot alter the timing coefficient
at W=0; check that identity. This does not claim general nonlinear field
redefinition/counterterm equivalence has been completed.

These are **perturbative timing coefficients**, not validated derivatives of
an admitted exact nonlinear cosmology or a theory-matched prediction.
Quantify contact/exchange cancellation and eta dependence; do not impose
1/eta scaling or extrapolate a physical cutoff from samples. A finite clock
diagnostic does not remove missing physical-energy/GR/domain evidence.

## Uniform analytic controls in this new scope

For 0<eta<=1/4 the positive-potential background and exact conservation/charge
identities give E0<=3/4, 47/48<=M_cos^2<=11/10, 1/5<H0<3/5,
H>=1/5-(36/47)t>0, a<=100/97<11/10, |H_dot|<=36/47,
177 eta/1000<=psi_dot<=eta/5, J^2<=eta^2, 4/5<=cV^2<1 and |m_w^2|<5/2.
Prove the parameter/initial-energy identities, not just their numerical
values on the grid. With comparison mu=1, L=7/4, T=1/20, exp(LT)<=80/73 and
first-wave amplitude <=7/5. mu is not a physical energy or cutoff.

For k=40, X=a^(3/2)W obeys X''+q(t)X=0 with q>32^2 and
0<X'(0)<9/10. Compare with cos(32t)+X'(0)sin(32t)/32 using its Wronskian;
the first zero occurs before (11/7+9/320)/32<1/20. After its initial maximum,
X'^2+32^2 X^2 cannot decrease before that zero, giving |W_t(t0)|>25.
Prove these facts with exact rational inequalities and the inherited
certified pi bound. The root argument certifies the **linear** zero, not
the existence of the full nonlinear solution.

Use the established odd Fourier bound to derive a continuous second-order
tail-energy bound at N=5 with coefficient <=(63/456250)*eta^(7/2).
Use the Lipschitz force derivative and forced-oscillator comparison to
control its contribution to the third-order self-force/solution. Give an
explicit pointwise tail bound for the clock diagnostic; L2 alone does not
bound a value at theta=0. Include the remaining output tail from multiplying
the retained cusp responses by |cos|. No physical UV admission follows.

## Verification and preservation

- Exact self-force Euler/chain identities, external-shift variation, volume
  drift, dimensional/degree and derivative-dependency controls. No invented
  zero auxiliary accelerations. Unit norm sets nu identically zero; only
  actual required metric accelerations enter after the dependency audit.
- Explicit source/field-label bijections; independent Fourier controls for
  analytic and cusp sources; unexpanded clock/tetrad and reflection controls.
- Two-method agreement <=1e-7 normalized for new coefficient trajectories
  and timing coefficients. Same tolerance for eta=1/4 comparison against
  the immutable archived first/coupled response. Record every disagreement.
- Full 22-field second-order residuals and new third-order transverse/shift
  reconstruction checks at initial/interior/final/linear-root points.
  Record mean negative kinetic controls, not a ghost classification from
  an unreduced/pre-constraint matrix. Preserve old nonmonotonic responses.
- Frozen runtime choices: existing Python/libraries, rtol=1e-10,
  atol=1e-12, max_step=.001; no dependency/model/provider/runtime setup change.
- New versioned executable, fresh non-overwriting receipts, immediate
  sidecars, source/artifact pin checks before/after, byte-identical read-only
  replay, owning report and append-only execution/review indexes.

Register R9-MT1-RETARDED-CUBIC-V1 with all planar/source/time/tail/GR-survey
and transitive review debt; review DEFERRED, not cleared. No physical family
GO is supplied by this checkpoint. Stage2 remains INCOMPLETE /
STOP_AND_ASSESS_DOMAIN_UNRESOLVED until its complete physical criteria pass.
Stage3 NOT_ENTERED; identifying matter-residue/nonlinear-force matching absent.
Tests1-3 HOLD_SUBSTANTIVE; physics_pass=false; Rule9_cleared=false;
gate_effect=NONE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED;
V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED. No parent replacement,
vault mutation, manuscript/PDF edit, provider dispatch, publication, commit
or push. All original scientific files, hashes and failed attempts survive.
