# R4C1 Stage 2: three-family nonanalytic coupled entry, v1

12 October 2026. Owner: Master Test 1 / conditional unchanged R4C1.
Direct human approval call_Ynm2vLPRqrAaeDzfmolSS14D supplies continuation
authority; it does not clear physics or independent review.

**364/364 local checks, zero failed/unknown; exact read-only replay.**
This bounded follow-up is complete. **Stage 2 is NOT complete; no family is
physically admitted.** Decision STOP_AND_ASSESS_DOMAIN_UNRESOLVED.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.
Stage 3 NOT ENTERED; identifying matter/nonlinear-force matching absent.

## 1. What was new, and what was reused

The [entry survey](RES001_R4C1_GR_FAMILY_SURVEY_REPORT_2026-10-11.md) and
[G3V covariant regularity result](RES001_R4C1_G3_COUPLED_VERTEX_REGULARITY_REPORT_2026-10-08.md)
already supplied checked action-level ingredients. They were reused, not
rerun or rewritten. The prior finding that Y^(3/2) lacks an ordinary third
Taylor derivative is not a new discovery here.

New work: specialize the UNSPECIALIZED covariant transverse density for ALL
three registered families; retain metric-shift elimination and action-derived
background flow; compare each with the complete generic 22-field Hessian.
Derive explicit nonanalytic field-space response and its unprojected harmonic
content, and evaluate necessary amplitude/frequency conditions. No frozen
B1 matrix was given new coefficients. No background integration or fit.

The frozen grid is six eta values, k=20,40,80, t=0: **54 events**. The
initialization is the registered G3 prescription with charge eta and
psi_dot=eta/5. Original G3 initial arrays and new-family survey matrices are
unchanged. G3's older 112/113 failure remains failed and preserved.

## 2. Coupled transverse coefficients: family differences matter

Let f^2=M_U^2(c1+c4), M_T^2=M_P^2-M_U^2(c1+c3), J0=v u_dot-u v_dot.
The actual nonzero-mode transverse shift and gradient are

```text
B_z = -M_U^2(c1+c3) w_z/M_T^2
K_V = f^2
G_V = M_U^2 c1 + (M_U^2)^2(c1+c3)^2/(2 M_T^2)
R_V = M_U^2(c4-3c2-c3) H
```

The dust lapse constraint and homogeneous scalar/matter contributions travel
with the inherited covariant derivation. Both transverse polarizations are
isolated from the other sectors at LINEAR order, not nonlinearly.
Maximum normalized coefficient difference from the full 22-field Hessian:
**1.3322207580996574e-16**. Archived new-family initial matrices match exactly.

For X=a^(3/2) f w and constant member coefficients, write

```text
m_X^2 = d_H H_dot - H^2/4 - 18 psi_dot^2 + 6 J0^2/13
d_H(G3) = 1/2
d_H(B1-frame) = -17/10
d_H(hierarchical) = -17/10 - 3 eta/4
omega_X^2(k,t) = c_V^2 k^2/a^2 + m_X^2
```

Using G3's mass expression for either new family would be incorrect. At the
registered INITIAL states, all six G3 m_X^2 values are negative; all six
B1-frame and hierarchical values are positive. This is not an all-time
stability theorem, a ghost classification or healthy GR recovery.

All 54 local frozen frequencies squared are positive. Their minima are
319.9512156996597 (G3), 320.1540346927625 (B1-frame), and
320.15410831601827 (hierarchical), in M_P=1 reference units. The k=20
H/omega values range approximately 0.0145--0.0514. These momenta are
chart diagnostics, not observed galaxy wavelengths or an admitted EFT band.

Interior K_V/G_V, tensor and auxiliary denominator signs are explicit in
formulas.json for 0<eta<=1. K_V=eta/6 loses rank at eta=0. No endpoint or
mean mode is inverted using the nonzero-mode shift inverse. The full
zero/fixed-charge classification remains open.

## 3. A nonanalytic classical response, without invented Taylor vertices

Retain the leading local rest-space projected gradient

```text
q = grad(Pi)/a + psi_dot*w
F(q) = A |q|^3
grad_q F = 3 A |q| q
Hessian_q F = 3 A (|q| I + q q^T/|q|), q!=0
Hessian_q F(0) = 0 by continuous extension
||Hessian_q F||_2 = 6 A |q|
```

Thus on the field-space ball |q|<=R the force gradient is Lipschitz with
constant 6 A R. This retains the mixed force/vector variables:
q=grad(phi)/(a sqrt(K_Q))+psi_dot V/f, phi=sqrt(K_Q) Pi, V=f w.
It is a field-space bound, NOT a controlled spatial PDE result, quantum
completion or full second-order metric/matter solution.

For a pure transverse direction C_local=A|psi_dot|^3/f^3. All three families
give C_local=(12 sqrt(6)/7)|psi_dot|^3 in the reference chart. All 54 events
retain C_local>0. The two-sided third derivatives of -C|epsilon|^3 are
-6C and +6C; no common ordinary trilinear Taylor vertex is supplied.
G3V's stationary auxiliary argument keeps its invertible nonzero-mode scope.
Changing the family does not remove that obstruction. A=0 removes the term;
psi_dot=0 removes only this transverse cusp, not the scalar-gradient cusp.
Positive psi chart rescaling leaves the physical cusp coefficient unchanged.

## 4. Why continuous projection onto one cosine would lose forcing

For an instantaneous real transverse cosine profile, the nonlinear force is
proportional to cos(x)|cos(x)|. Its full Fourier series contains every odd
harmonic, with coefficients

```text
b_n = -8 (-1)^((n-1)/2)/[pi n(n^2-4)], odd n
b_n = 0, even n
<|cos(x)|^4> = 3/8
fundamental-only discarded L2 energy = 3/8 - 32/(9 pi^2)
```

The discarded force RMS divided by the full force RMS is
**0.198305505756623 (about 19.8%)**. This is a norm statement about this
specified forcing profile, NOT a 19.8% error estimate for ITSM predictions
or the evolved coupled solution. The full forcing must not be continuously
projected onto its fundamental.

For N>=3 an explicit upper bound on mean-square tail beyond N is
128/(5 pi^2 N^5), using n^2-4>=n^2/2 and the integral bound on sum n^-6.
Exact product-to-sum algebra, independent quadrature and Parseval checks
were retained. N=9,31,127 tails all satisfy this bound. A finite harmonic
sum is not declared the full nonlinear evolution or an EFT cutoff.

## 5. Necessary conditions, not a physical validity window

The receipt exports H/omega and an isolated 1%-cusp-force criterion
|V|<=0.01 omega^2/(3 C_local), plus a separate small-tilt chart diagnostic
|V|<=f/100. These control only their NAMED local contributions. No amplitude
was selected; neither criterion controls every interaction or evolution error.

The regulator is retained: fourth spatial differences of the full coupled
Pi-Pi action coefficient agree with -24 b/a^4. All full reduced matrices and
mixed entries are stored. The direct transverse quartic remains

```text
-b [psi_dot*w*w_dot + (psi_ddot+2 H psi_dot)w^2]^2/2.
```

It is NOT the full constrained quartic Schur action or a complete eigenstate
amplitude. Neither b/K_Q, potential Lambda, a positive quadratic spectrum,
this cusp amplitude tolerance nor G3I's fixed-metric probe threshold supplies
a physical cutoff. Frozen GW/PPN comparators retain their original limited
scope; no new external fit or comparator-based family selection was made.

Still required: full nonlinear dynamical metric/matter sources including
mean and generated modes, scalar/constraint J2/J3 and complete quartic
reduction, physical eigenstate interactions, a controlled CONTINUOUS
frequency/momentum band, all-sector characteristics/healthy GR, and full
conformal-matter PPN. This entry admits no physical family and is not an
all-action no-go. An unchanged-action nonanalytic classical calculation can
continue under the supplied authority; smoothing or dropping the force,
changing the background/parent or pivoting to TOP-X4 is not implied.

Next bounded calculation: assemble the metric/matter and auxiliary
second-order response to the real coupled perturbations, retaining the
mean/second-harmonic sources and the full odd nonanalytic forcing, before
claiming a reduced nonlinear system or an interaction-controlled band.

## 6. Sealed provenance and immutable replay

- [Contract](RES001_R4C1_THREE_FAMILY_NONANALYTIC_ENTRY_V1_CONTRACT_2026-10-12.md):
  c6bf573ef346815a8ad8c9c5c7724858bde06124bcf1fc1681293ec87910b78a.
- [Executable v1](../../../Analysis/MasterTests/test_01_r4c1_three_family_nonanalytic_entry_v1.py):
  ab0f65fb8b99043714abbd152f45ac1d438931a91debac5d06d6fb28ec86d04d.
- [Receipt](../../../Analysis/MasterTests/outputs/r4c1_three_family_nonanalytic_entry_attempt_01/summary.json):
  0b06579cbab005fe454023fc1a2a2f89b48f15463ea5a3dc5b7712828db67fdf.
- formulas.json: ddec4df84777cea5d9346d72c8a16b4d1010955221b571a523a1cce172704fc0.
- controls.json: a7872020fa8ab308dffac46960d498a98b347de6294973a63f45ce3816df20c0.
- grid.json: 26ed71964cef28d7e7573342ffd0be14afa1c9cbeebc580bb219f036191d3656.
- matrices.json: 114be21bf23e6ddb5138d44d46dcff5283ab15ec0d84d147febd5f3966b6c1c7.

219 pinned scientific sources and 435 source/available-sidecar metadata
records are verified/preserved. All five new payloads and sidecars replay
byte-identically without writes. These are independent IMPLEMENTATION
controls by the same agent, not independent Rule-9 scientific review.

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_three_family_nonanalytic_entry_v1.py --replay Analysis/MasterTests/outputs/r4c1_three_family_nonanalytic_entry_attempt_01
```

Both initial execution and replay exited 0, with no scientific/implementation
failure. Private execution/replay logs remain ignored; no originals, failed
attempts or their sidecars were replaced.

R9-MT1-THREE-FAMILY-NONANALYTIC-ENTRY inherits GR-FAMILY-SURVEY, G3V/
G3V-CROSSCHECK/G3I, generic variation/G3N5 and all inherited review debt.
Review DEFERRED, not a research blocker. Physical admission remains blocked
by the substantive inputs above. Stage 1 acceptance keeps its bounded B1
linear scope. Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED;
TOP-X4 UNCHANGED. Root goal ACTIVE/incomplete. No commit/push/publication,
provider/model/runtime/dependency changes, manuscript/PDF edits or vault ops.
