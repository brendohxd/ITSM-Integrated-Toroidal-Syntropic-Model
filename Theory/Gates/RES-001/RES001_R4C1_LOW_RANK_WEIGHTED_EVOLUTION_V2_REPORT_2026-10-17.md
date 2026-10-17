# R4C1: repaired inverse and complete weighted linear evolution

17 October 2026. Master Test 1 / RES-001 / unchanged-action Stage 2.
Claim: Conditional. V2 local validation: 671/671, zero failures/unknowns.
Immutable replay: PASS, READ_ONLY_REPLAY_EXACT, all nine cases; terminal exit0.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result and scope

The inverse-construction obstruction has been resolved for all nine registered
fixed parameter cases. The full inverse, complete transformed generator,
positive mixed-order evolution norm and explicit continuous-time linear bound
are established within the domain below. This advances the mathematical
evolution problem; it does not establish a physical interaction window,
positive canonical energy, nonlinear stability, or healthy GR recovery.

Use the unchanged unspecialized generic 22-field action, before separate
substitution of archived_G3, new_B1_frame and new_hierarchical at exact
eta=1/4,1/64,1/1024. All ten complex coordinates/twenty evolution states,
local phase, auxiliary reconstruction, coefficient drift and p_dot=-H*p
remain. No slow-graph projection or local homogeneous charge condition is
imposed. Domain: k=(0,0,ell), ell>=4, 0<=s<=t<=1/20, the registered regular
background and initial prescription. On the coordinate 2*pi torus ell is an
integer. Exactly ell=0 and eta=0 are excluded. This is not a continuous-eta,
all-direction, arbitrary-background or full nonlinear theorem.

## Exact repair

In the mixed-order chart, reorder the fast coordinates to the final two
positions and write U=[[0,A],[B,0]], with an 18+2 partition. For q=1/ell,

~~~text
D = I_2-q^2*B*A
d = det(D)
(I+q*U)^(-1) =
  [[ I_18+q^2*A*D^(-1)*B, -q*A*D^(-1)],
   [ -q*D^(-1)*B,          D^(-1)      ]].
~~~

Both full 20x20 products are exactly the identity. In every registered case
det(B*A)=0 and d=1-g/ell^2, where
g=-a^2*beta^2*f2/b<0 and f2=MU2*(c1+c4).
Thus d>=1 on the declared positive-a, nonzero-ell
domain. The exact numerator includes a nonzero cubic-in-q correction missed
by the earlier construction. The executable also verifies U^5=g*U^3; it
makes no minimal-degree-polynomial claim.

For the first archived_G3, eta=1/4 case, g=-11*a^2/48000. The corrected inverse
minus the rejected cubic inverse has precisely these two nonzero entries:

~~~text
delta[9,3]  = -11*i*a^3*psi_dot*(60*H*psi_dot+rho)/(2000*ell^3*d)
delta[19,3] =  11*i*a^3*(60*H*psi_dot+rho)/(1440000*ell^3*d).
~~~

Indices are zero-based in the inherited balanced twenty-state chart. These
terms retain the evolving background/dust contribution. The previous
U^3=g*U assertion remains false and its failed receipt remains unchanged.

The complete generator, including every nonpositive coefficient, is

~~~text
w = Tw*(I+U/ell)^(-1)*B_balance*SO2^dagger*(y,y_dot)
G_w = ell^2*F + ell*L + drift + sum_(j=0..7)(N_j/ell^j)/d
drift = Tw_dot*Tw^(-1).
~~~

The notation B_balance distinguishes the full balance map from the rectangular
Schur block B above. Zero coefficients remain exported. Exact coefficientwise
identities bind this expression to the full action-derived evolving generator,
rather than only its principal terms. Both positive-power symbols are Q-skew;
Q is a positive diagonal matrix plus a positive rank-one contribution and
Q>=I/10. Every balance, fast-map, wave-map and Q derivative is retained.

## Continuous-time estimate and limits

With E=w^dagger*Q(t)*w,

~~~text
E_dot <= mu*E,
sqrt(E(t)) <= exp(mu*(t-s)/2)*sqrt(E(s)).
~~~

Exact outward rational constants are stored in each case receipt. Display
values below are rounded summaries, not the exact bounding constants.

| Family | eta=1/4 | eta=1/64 | eta=1/1024 |
| --- | ---: | ---: | ---: |
| archived_G3 | 31910.76851 | 486720.66495 | 7766849.31088 |
| new_B1_frame | 15509.19322 | 231658.87810 | 3692002.37669 |
| new_hierarchical | 11811.38296 | 226476.49639 | 3686682.84442 |

The background box is certified from the unchanged homogeneous energy/dust
balances and parameter map, not from sampled maxima:

~~~text
1<=a<=20/19, 1/5<=H<=1,
|u|,|u_dot|,|v|,|v_dot|,|r|,|r_dot|<=2,
eta/10<=psi_dot<=eta/5, 1/6<=rho<=1/4, 1<=C<=250/249.
~~~

On shell, V>=0 and energy_dot=-3H*(kinetic+rho), so energy stays below its
initial value <1. The H differential comparison prevents H from reaching
zero; the clock equation uses the checked beta/K_Q=2eta/15 scaling.
The clock and dust-charge bootstraps keep the trajectory inside the box
through t=1/20. Exact rational interval rows bound all complete Hermitian
remainder coefficients, with d>=1 and Q>=I/10.
Here V denotes the declared R4C1 background potential and K_Q=3eta is an input;
neither is a derivation of the outstanding microscopic MAT matching quantities.

These constants are very conservative: even the smallest endpoint exponent
mu/40 exceeds 295. The result controls linear existence/growth in this norm,
but does not certify useful small perturbative error. The listed bounds
become larger toward smaller eta; they supply no uniform endpoint or GR
estimate and do not prove that the actual physical growth diverges there.
The weights mix spatial derivative orders in inherited reference units;
neither mu nor ell is a derived physical cutoff or observed accuracy.

## Independent controls and retained failed attempt

All 378 unchanged background nodes from 18 earlier trajectories are used,
ell=4,80: 756 independent full-action comparisons. No new time integration.

| Control | Largest residual | Frozen requirement |
| --- | ---: | ---: |
| Full generator binding | 3.064657688319131e-14 | <=1e-9 |
| Evolving energy-derivative identity | 2.82445849633537e-15 | <=1e-9 |
| Two-sided inverse product | 2.502880715182787e-16 | <=1e-9 |
| Independent dense-inverse binding | 3.818657217671698e-17 | <=1e-9 |
| Auxiliary reconstruction | 4.1274365611846766e-14 | <=1e-9 |

V1 attempt01 remains FAILED, 186/189. Its first two case estimates passed;
the third case stopped at the frozen absolute >1e-12 binary64 omission
visibility control, whose value was 1.0519200528062109e-15. Remaining-case
totals were consequently incomplete. The exact inverse/generator did not
fail. V2 explicitly changes this control under its frozen addendum; no
action/generator tolerance is lowered.

V2 retains all former visibility results, including FAIL for eta=1/1024 in
each family. It proves the missing correction is nonzero symbolically, then
independently inverts the full 20x20 matrix with 90 decimal digits at the
exact unchanged on-shell initial event, ell=4,80. The largest relative
correction discrepancy is 2.3118793850897528e-73 (required <=1e-50);
largest corrected product residual is 8.45009347586168e-93 and largest
dense-inverse discrepancy 1.439427732524683e-92 (both required <=1e-60).
All extra terms remain. Numeric visibility is not used to declare them zero.

## Provenance and disposition

Contracts: LOW_RANK_INVERSE_V1_CONTRACT and V2_OMISSION_ADDENDUM, same date.
Executables: Analysis/MasterTests/test_01_r4c1_low_rank_inverse_v1.py and v2.py.
V1 receipts: Analysis/MasterTests/outputs/r4c1_low_rank_inverse_attempt_01/.
V2 receipts: Analysis/MasterTests/outputs/r4c1_low_rank_inverse_attempt_02/.
Each complete case includes formulas, exact bounds, all controls and metadata.

V2 source SHA509ac31676e703a585fd44c7de82cec326ee285e20b98c194afd9dd5f68c9030.
V2 summary SHA7ceafaf52d8fe217f4b3f598a47cf75e50b7e4118f7b97bed66c322938f450f7.
V1 failed summary SHA25016a8308b1681d02d5e1421ec28548a55508b1d8b8a0afa7af3f2d422f6bf3.
412 source pins and 821 source/available-sidecar metadata records are preserved.
Three inherited missing sidecars remain explicitly unverified. Same-agent
exact and independent-computation controls are not independent peer review.
The failed V1 receipt also replayed exactly, retaining its exit1 and all three
failed controls. The successful V2 replay preserved all case/summary/sidecar
bytes, sizes and modification times. No process was interrupted or restarted.

R9-MT1-LOW-RANK-WEIGHTED-EVOLUTION-V2: provisional reuse is supported within the
fixed-case linear scope by the exact generator/coercivity/domain proof and
independent controls. Inherit THREE-FAMILY-FINITE-K-V3, WEIGHTED-CUBIC-REJECTION-V1,
LOW-RANK-INVERSE-V1, CUSP3-EVOLUTION-V1, homogeneous fixed-charge kinetic V3,
generic action/evolving reduction and all transitive deferred review debt.

Next substantive question: connect the complete coupled linear evolution to
the finite-amplitude constrained interaction/remainder and a physical validity
window. A useful error/amplitude criterion and physical interpretation of the
canonical energy are still needed. The old negative trace energy, wave-scale
Jordan defect, singular eta=0 endpoint, retarded timing warning, nonmonotonic
finite-mode results and homogeneous-ensemble distinction remain intact.
The CUSP3 evolution report (SHAaf0878a2d20c48d9a99189940952ef8714f68bd0f99dc2ae09ecb056d05cd186)
already covers the sampled mean and first even harmonic at order |e|^3.
The new CUSP_ODD_RESPONSE_TAIL_V1 report of this date bounds the complete lower
odd transverse response. Its 199 controls and exact replay do not yet bound
the full order-|e|^3 coupled response or all-order remainder. The remaining
forced-response/tail estimate must retain those coupled fields and the
separate mean constraint chart before supporting finite-amplitude use.
The additional CUSP_ODD_RESPONSE_ROOT_AUDIT_V1 addendum covers all stored
wave-zero samples (58/58 controls and exact replay) without changing the proof.
Repeating the completed two-solver finite-mode comparison does not supply it.

Stage1 remains complete only in its registered linear B1 dust scope. Stage2
INCOMPLETE, no physical family GO; Stage3 NOT_ENTERED. Tests1-3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 UNCHANGED. The native full goal is ACTIVE/incomplete.
No commit, push, publication, submission, website, manuscript/PDF, vault mutation,
provider dispatch or runtime/model configuration change.
