# R4C1-G3N4: coupled source ledger and force-coverage disposition

Date: 9 October 2026. Version 1. Master Test 1, frozen R4C1 action.
Conditional, locally checked research; Rule-9 review DEFERRED, not cleared.
physics_pass=false; gate_effect=NONE. The response solution remains open.

## Outcome and the original coverage gap

The original G3N4 run passes 46/46 registered local checks and reproduces
exactly in read-only replay. It exports the analytic second-order sources
for all 22 response fields, the temporal/longitudinal source identities,
the unsmoothed transverse force and its infinite odd harmonic tail.

The original force.json also asserts that the other second-order force
sources vanish on the first-order transverse direction. That assertion
was not field-by-field tested by its executable. Thus the original 46/46
receipt, by itself, does not establish that contract requirement. Its
coupled_plane_wave_sources_verified flag must be interpreted within its
registered checks, not as full evolution or unrestricted physics closure.

A separately frozen force-coverage supplement now supplies the missing
field-by-field variations: 455/455 local checks, exact read-only replay.
No original G3N4 source, output or sidecar was edited. The original check
count and the supplement's count remain distinct; neither is a physical
Test-1 pass or independent scientific review.

The combined registered ledger is available for provisional coupled-response
work in the inherited (t,z) chart. It is not a solved response, a general
three-dimensional T3 reduction or a finite-mode invariant evolution.

## Owning inputs and immutable receipts

The [G3N4 contract](RES001_R4C1_G3N4_COUPLED_SOURCE_CONTRACT_2026-10-09.md)
has SHA-256 a5f5880e894c544794fa46e7e68dfdd07c4960d44791751521b402cd8bb9a2b6.
The frozen R4C1 action remains
81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3.
Inherit the G3N3, G3N2, G3V and full transitive scientific/review debt.

Original executable:
Analysis/MasterTests/test_01_r4c1_g3n4_coupled_source_v1.py,
SHA-256 080bb2c0aef277dda5a57f3f61a449e4da2f92813f84af05f5fa711666e29144.
Original output directory: Analysis/MasterTests/outputs/r4c1_g3n4_attempt_01.

- summary.json: 6dde40b37ca40409566151c997bcc663edd923f1119fdcd019728a87dfd450e1.
- formulas.json: 1dee96271de67aec5336ac84753c18728a65e130e05c1c7731559c5a6a49727a.
- force.json: 03b9116e8dcc367216364a4898fbdfb78d036918a48f715453555b952ca6c76a.
- independent.json: ea9db7167daa3598e0c3425e5ee969c862aa93e6dfdeb1465e96795048a3eaf3.

[Force-coverage contract](RES001_R4C1_G3N4_FORCE_COVERAGE_CONTRACT_2026-10-09.md),
SHA-256 a772168e982dc77b77f8301879f32bba073a37e01ce7c332f12e4bfcd266ae23.
Supplement executable: Analysis/MasterTests/test_01_r4c1_g3n4_force_coverage_v1.py,
SHA-256 8474fd75bcab4c31da804dc41db813063c1186e2a937b6939a364ad153c6aff8.
Supplement directory: Analysis/MasterTests/outputs/r4c1_g3n4_force_attempt_01.

- summary.json: ea235d26bb91f33b5c134d161d26df33ae52cee415433b59d3eedf6d1ac4e287.
- formulas.json: e042b6b365cc1fded9b799643a4d90881eef1520839f5a31eef8d7edcfce9c57.
- independent.json: dcd529971dc9eac6449619fc26284f3ea18a357f6406f44e35fb93145868d45e.

All listed files have matching sidecars. The original run checks 116 source
pins / 113 available sidecars; the supplement checks 122 / 119. The same
three inherited sidecars remain absent, with the underlying bytes pinned:

- Theory/Gates/UVIR-003/UVIR-003_STAGE_B_FORCE_COMPLETION_OPTIONS.md.sha256.
- Theory/Gates/UVIR-003/UVIR-003_STAGE_B_NONZERO_GRADIENT_FORCE_LOCAL.md.sha256.
- Theory/Gates/UVIR-003/UVIR-003_STAGE_B_TRACK_A_FORCE_ADM_CUBIC.md.sha256.

No sidecar was invented to hide this inherited availability condition.

## Analytic response construction

Use independent e, the first-order transverse amplitude, and d, the response
variation. Later d has perturbative size e^2. The analytic source functional
is the e^2 d coefficient of the frozen density divided by background a^3.
All response values and time/spatial jets remain independent in variation.

The fields are alpha, Sx,Sy,Sz, Mxx,Mxy,Mxz,Myy,Myz,Mzz, Vx,Vy,Vz,
du,dv,dr, Pi,T,Em,Z,nu,LambdaU. The metric lapse, all shifts and all six
spatial metric entries are retained. Cartesian condensate/reservoir,
dust, auxiliary regulator, frame normal and unit-multiplier equations
are not replaced by a metric-frozen or one-amplitude ansatz.

The normalized frame n belongs to the frozen force/alignment/regulator
extension. In L_U, U=(1+d nu)n retains the independent normal variation.
The unit equation fixes nu and the normal equation determines the multiplier
response in a later solve. They must not be dropped by normalizing L_U.
Cosmic time has tau0_dot=C=exp(beta psi0), not tau=t.

For each response R with functional coefficients A_R, B_Rt, B_Rz, the
Euler source divided by a^3 is

```text
S_R = A_R - (partial_t+3H) B_Rt - partial_z B_Rz.
```

The EH+GHY ADM kinetic bulk, four original frame invariants, alignment,
temporal-force kinetic, first-derivative regulator, Cartesian scalar
kinetics/potentials/portal, dust and multiplier sectors are included.
Spatial Ricci is independent of e in this first-order vector chart;
its e^2 d coefficient vanishes. This is not its removal from the theory
or from the quadratic response kernel. Fixed/periodic boundaries retain
the inherited surface convention.

All 22 analytic sources and their functional coefficients are exported
before and after the G3 first-order shift solution. Variation precedes
B=-eta W/(8-eta). The zero-response quadratic vector action agrees exactly
with the complete G3V action, including gravity and the regular shift term.

Writing p=psi_dot and J=v0 u_dot-u0 v_dot, the checked direct sources include

```text
S_Z  = b [p W W_dot + (p_dot+2H p) W^2],
S_Pi = -K_Q [(p_dot+3H p)W^2 + 2p W W_dot],
S_du = zeta [(J_dot+3H J)v0 W^2 + 2J v_dot W^2 + 2J v0 W W_dot],
S_dv = -zeta [(J_dot+3H J)u0 W^2 + 2J u_dot W^2 + 2J u0 W W_dot].
```

The Z source recovers the G3N3 direct term. It is not the full Z solution:
Pi_zz/a^2 and (p/a) partial_z(V_z) remain in the coupled regulator equation.
Zero direct sources for dr,T,Em,LambdaU do not imply zero responses; these
fields remain coupled through the response kernel and constraints. The
normal-frame source is retained and exported.

## Registered source-consistency identities

In the declared G3 family, define E_W as the Euler derivative of the
shift-reduced quadratic vector action. With K_v=eta/6, its equation is

```text
W_tt = -3H W_t + [4/5+3eta/(8(8-eta))] W_zz/a^2
       -[2(H_dot+H^2)-18p^2+6J^2/13] W.
```

The registered quadratic-source temporal combination is

```text
T_src = -(partial_t+3H) S_alpha + 2H(S_Mxx+S_Myy+S_Mzz)
        +partial_z(S_Sz+S_Vz)/a
        +u_dot S_du+v_dot S_dv+r_dot S_dr+p S_Pi
        +C S_T+epsilon_dot S_Em+lambda_dot S_LambdaU.
P_src = a(partial_t+4H) S_Sz + 2 partial_z S_Mzz.
```

Exact exported-formula checks, now included in the supplement receipt, give

```text
T_src = (H W-W_t) E_W,
P_src = W_z E_W.
```

Thus both registered combinations vanish on the first-order vector shell,
and their off-shell residuals have not been discarded. The ADM/boost gauge
weights are exported in the original formulas. No assertion about every
three-dimensional Ward identity or a new background solution is made.

## Unsmoothed force: field coverage and harmonic tail

Keep -A Y^(3/2) separate from the analytic expansion. The supplement derives
the normalized-projector and volume variations before any shift solution:

```text
Y0 = p^2 e^2 W^2,
delta Y = p^2 [2eW Vy+e^2 W^2(Myy-2alpha)]
          +2p e^2 W^2 Pi_t,
delta volume/a^3 = alpha+(Mxx+Myy+Mzz)/2.
```

For this original pure transverse direction the force Euler sources are

```text
S_Vy    = -3A |p|^3 e|e| W|W|,
S_alpha =  2A |peW|^3,
S_Myy   = -2A |peW|^3,
S_Mxx   = S_Mzz = -A |peW|^3/2,
S_Pi    = 3A |e|^3 [(2|p|p_dot+3H p|p|)|W|^3
                    +3p|p| W|W| W_dot].
```

Only S_Vy starts at degree 2 in directional amplitude. The displayed lapse,
diagonal metric and Pi terms start at degree 3; they are not identically zero.
The other 16 direct force Euler sources are zero on this direction, not
zero solutions of the coupled response equations. Every value/time/spatial
variation coefficient, the Euler chain rule, amplitude degree, both signs
and e=0,p=0,W=0 nodes are checked. No division by sqrt(Y), p, W or e occurs.
Controls reject using unnormalized U in the force projector, dropping the
volume variation or replacing e|e| by e^2.

Independent numerical controls use an exact rest-frame norm identity,
not smoothing: q_rest=q+h v [E+(v.q)/(gamma+1)], Y=q_rest.h^-1.q_rest,
E=(psi_t-N^i psi_i)/N, gamma=sqrt(1+v.h.v). This agrees exactly with
the projected covariant norm and stays valid at zero boost without
cancellation or division by v^2. The ADM domain remains admissible.

For W=cos(chi)+(1/3)cos(3chi)=(4/3)cos(chi)^3, W|W| has zero mean/even
coefficients by half-period antisymmetry. Its general positive odd cosine
coefficient is

```text
f_m = -5120 sin(m pi/2) /
      [pi m (m^2-4)(m^2-16)(m^2-36)],  m positive odd.
```

The first three are 1024/(315pi), 1024/(567pi), 1024/(2079pi). The nonzero
infinite odd tail remains explicit. It is not a physical cutoff, a closed
first/third-mode system or a finite Fourier invariant manifold.

## Independent controls, replay and preserved failures

Original analytic mixed variations: two generic off-shell response jets,
unexpanded geometry, 50-digit mpmath, e=d at 1e-3,5e-4,2.5e-4. Errors are

```text
jet 0: 4.2502834e-11, 1.0625709e-11, 2.6564272e-12;
jet 1: 5.1060275e-12, 1.2765068e-12, 3.1912671e-13.
```

They decrease under the frozen <=1e-5 final bound. Independent 50-digit
force quadratures for odd modes 1,3,...,31 have maximum normalized error
1.305060893599705e-54 under <=1e-12.

Supplement: 240 field/chart comparisons at three response steps each,
including both signs of e,p,W and separate p=0/W=0 controls. Maximum final
normalized error is 7e-21 (maximum over all steps 1.12e-19), under the
separately frozen <=1e-12 bound. These are generic local jets, not integrated
physical solutions; 50-digit controls do not upgrade inherited trajectory
precision. Both receipts have zero registered failed/unknown checks.

Original G3 eta1_independent_fd_balances remains failed:
1.1005635230674148e-7 against <1e-7. Original G3N3 attempt_01 remains failed
at 512/514: reject_direct_source_as_full_Z_solution and
all_direct_harmonics_exact_reconstruction. Its structural-equality/trig
assertion disposition and new v2 are preserved; no old receipt is rewritten
and no physical acceptance threshold was relaxed here.

Exact replay preserves all eight original output/sidecar files and all six
supplement files byte-for-byte, including length and last-write timestamps.
Source pins/available sidecars pass before and after calculation. The
optimizer receipt summaries were inspected with failures, unknowns and
parent holds retained; summaries alone were not used as hash verification.
Private execution logs stay in ignored .local, not publication artifacts.

## Next owning calculation and unchanged parent status

Next: derive the complete coupled response kernel and compatible initial
data, keeping lapse/shift/normal/multiplier/dust/auxiliary constraints and
the homogeneous sector separate from nonzero-mode inverses. Use the
registered source ledger, retaining unsmoothed forcing and the harmonic
tail. A source-only calculation does not establish response existence,
uniqueness, boundedness or stability. General T3 data, physical Cauchy/DAE
domain, cutoff and healthy continuous GR recovery remain substantive.

No new canonical numerical K_Q, computed matching V, physical Hessian,
PPN/weak-field closure, blind coefficient selection or observational fit
is supplied. Existing C1/C2 clock-domain and principal-symbol findings,
including their restricted scope and substantive obstructions, remain intact.

Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
Review dependency: R9-MT1-G3N4 and inherited R9-MT1-G3N3/G3N2/G3V debt,
DEFERRED, not cleared. Native goal was usageLimited earlier, then the user's
resume/edit took effect and a fresh controller snapshot reported ACTIVE;
the full eight-route/Tests-1-3 objective is incomplete.

No action replacement, manuscript/PDF edit, vault mutation, provider
dispatch, commit, push, canonical promotion or publication occurred.
