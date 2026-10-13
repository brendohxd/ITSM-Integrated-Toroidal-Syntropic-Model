# RES-001 R4C1 three-family charge/domain audit V5

13 October 2026. Claim Conditional; local audit complete in the scope below.
Stage 2 and the native full goal remain ACTIVE / INCOMPLETE.
`physics_pass=false`, `gate_effect=NONE`, `Rule9_cleared=false`.
Rule-9 review is DEFERRED; pending review is not the substantive blocker.

## Result and scope

**4063/4063** local checks pass, with exact read-only replay of all six receipt
files and sidecars. Separate read-only QA passes **714/714**, checking 289
source hashes, 286 available source sidecars, three inherited known absences,
six artifact sidecars and all18cases. No failed or unknown current checks.
This is reproducibility evidence, not independent review or physical clearance.

The original quadratic retarded response conserves phase and dust charges in
the registered tests, and its independently differentiated lapse-constraint
density agrees with the Euler-assigned derivative. Its quadratic prepared
charges differ from the background charges: conserved does not mean prepared
at fixed background charge. The prior cubic timing warning and its data are
unchanged; its fixed-charge interpretation remains unresolved.

Follow GEMINI, core identity, the 11 October master plan and the approved
unchanged R4C1 Stage-2 continuation. All three families, eta1/4,1/64,1/1024,
k40,t[0,1/20], DOP853/Radau,21nodes per case:18cases/378nodes. **Zero old ODE
integrations rerun.** Generic action/kernel variation precedes family maps;
no substitutions into already-specialized B1 matrices. Stage1 is complete only
in its registered linear B1 prepared-dust scope, not physical dust clearance.

V1 contract and GR-control, V2 binding, V3 algebra, V4 clock and V5 parameter
addenda remain frozen. Executable
`Analysis/MasterTests/test_01_r4c1_three_family_charge_domain_v5.py`, SHA
`a3c9d3077fcf03d25b761f2b43e3503e7a71d4b4d217dd7720af1b966da0d575`.
Input retarded V2 trajectories SHA
`40c39678028c3fdc1d42fce9dc96f3132530a470a1a86b71a37f046dcb913107`;
owning retarded report SHA
`782ee5d6a21bcabfeb2b99947c54e9c1b048cfcfd67e11bdcaa1f3ca34cfcd99`.

## Action-derived currents and prepared charges

For J_mu=v partial_mu u-u partial_mu v and h^(mu nu)=g^(mu nu)+n^mu n^nu,
direct same-action variation gives

\[
j_{U(1)}^\mu=\sqrt{-g}[g^{\mu\nu}+\zeta(u^2+v^2)h^{\mu\nu}]J_\nu,
\qquad p_\tau^\mu=-\sqrt{-g}\epsilon C^2g^{\mu\nu}\partial_\nu\tau.
\]

With Euler densities E_x=partial L/partial x-partial_mu(partial L/partial x_mu),
the off-shell identities are partial_mu j^mu=v E_u-u E_v and
partial_mu p_tau^mu=-E_tau. Arbitrary derivatives of momentum coefficients
are retained; evolving background coefficients are not treated as constant.

For the first transverse w cos(kz) wave, the quadratic mean coefficients are

\[
\begin{split}
Q_2=a^3[&u\delta\dot v+\delta u\dot v-v\delta\dot u-\delta v\dot u
 +(\tfrac12\mathrm{tr}M-\alpha)j
 -\tfrac12\zeta(u^2+v^2)jw^2],\quad j=u\dot v-v\dot u,\\
P_2={}&a^3C^3E_m+\frac{a^3\rho}{C}
 [\tfrac12\mathrm{tr}M-\alpha+2\beta\Pi+\dot T/C].
\end{split}
\]

Dust clock T=0 gives alpha=-beta Pi and **three** beta Pi in the bracket.
All22 generic mean source fields, volume, alignment, lapse, density and drift
remain. All52 homogeneous conservation-row and both wave-forced identities
vanish exactly using the full Friedmann constraint, not numeric target values.

The original zero free-mean preparation has Q2(0)=-eta^3/26 and, with f2=eta/6,
Q2/f2=-3 eta^2/13. All18cases verify this recipe. Its initial Q2 values at the
three etas are -0.0006009615384615385, -1.4671912560096155e-7 and
-3.582009902367225e-11. For xi=sqrt(f2)e and w(0)=1, initial dust coefficients:

| Family | eta | P2 / f2 |
| --- | --- | ---: |
| G3 | 1/4 | -325.08625212831953 |
| G3 | 1/64 | -320.3709111762921 |
| G3 | 1/1024 | -320.0856462290597 |
| B1 frame | 1/4 | -319.8528383218027 |
| B1 frame | 1/64 | -319.94987991847995 |
| B1 frame | 1/1024 | -319.9562411963668 |
| Hierarchical | 1/4 | -320.11610056578877 |
| Hierarchical | 1/64 | -319.9492743016355 |
| Hierarchical | 1/1024 | -319.9562042357277 |

Both methods agree at initialization. Preserve hierarchical nonmonotonicity;
no asymptotic law is imposed from three samples. P2 is a quadratic correction
in P(e)=P_background+e2 P2+..., not negative total dust charge or density.
Finite-amplitude positivity is not certified. No original charge or initial
data is changed to make Q2 or P2 vanish.

## Independent density drift and finite current control

The inherited reconstruction solves Em from the lapse constraint but assigns
Em_dot from the dust Euler row. Verifying that assigned value using the same
Euler row would be circular. This audit differentiates the entire affine lapse
graph along the full stored mean flow, retaining source/coefficient/basis and
background drift, then compares with the assigned derivative. No helper edit.

Max abs(Em_dot_graph-Em_dot_assigned)/(1+abs(Em_dot_assigned)) is
`2.390825147671723e-15`. Maximum charge derivatives are
`3.8163916471489756e-17` for Q2, `1.9539925233402755e-14` for P2.
Observed absolute drift: Q2 `2.0080725277038525e-14`, P2 `6.0021498882179e-10`.
Maximum Q2 drift / eta3 is `1.398971216648448e-12`, not normalization by Q2(0).
Registered cancellation-scaled errors are at most `6.026573126465635e-13`
and `2.274375570294737e-11` for Q2 and P2.

Independent 80-digit unexpanded ADM/normalized-frame currents at nodes0,10,20
use central amplitudes1e-6,5e-7,2.5e-7. Maximum finest-amplitude error divided
by1+abs(coefficient) is `3.1007156613454476e-15`. The two-angle average is exact
only for the quadratic coefficient; finite profile values are not full nonlinear
on-shell charge certificates. No nonanalytic force cusp is smoothed.

The archive lacks full background data at wave-root events. Fresh independent
numeric root-background comparison is explicitly UNAVAILABLE; no interpolation,
invented background or old ODE rerun. Generic all-time identities include the
wave zero within their domain; existing root controls remain untouched. These
small observed errors do not certify a finite solver/nonlinear error bound.

## Homogeneous kinetic and normal-domain control

Generic13-field kinetic congruence is
diag(-2 Mcos2/3,MT2/4 [five shears],f2 [three frame modes],1,1,1,K_Q), with
Mcos2=MP2+MU2(c1+3c2+c3)/2,MT2=MP2-MU2(c1+c3),f2=MU2(c1+c4).
Before normal elimination, the volume/normal principal block is

\[
K_{x\nu}=\begin{pmatrix}-2M_{\rm cos}^2/3&-M_U^2c_2\\
-M_U^2c_2&-M_U^2(c_1+c_2+c_3+c_4)\end{pmatrix},\qquad
h_\nu=-2M_{\rm cos}^2/(3a^3\det K_{x\nu}).
\]

| Family | Mcos2 | MT2 | det K(x,nu) |
| --- | --- | --- | --- |
| G3 | 1-eta/12 | 1-eta/8 | eta(352-111 eta)/8640 |
| B1 frame | 1+eta/10 | 1 | eta(eta+30)/450 |
| Hierarchical | 1+eta/10+eta2/16 | 1-eta2/8 | eta(75 eta3+180 eta2+1232 eta+960)/14400 |

eta2/eta3 mean eta squared/cubed. All families have f2=eta/6 and the declared
diagnostic K_Q=3 eta. Continuous positive kinetic/normal denominators are proved
on **0<eta<=1/4** with exact positive-coordinate polynomials, not samples alone.
Require a>0,C>0 and the declared background/clock chart. This is a nonempty
denominator domain, NOT an admitted physical frequency/momentum window.
Extra kinetic/normal coefficients vanish at eta0; no singular inverse there.
Metric coefficients approaching one are only principal controls, not a healthy
GR theorem. Old B1 eta1 h_nu=-330/(31 a3) is only a matching control.

## Canonical clocks and Einstein–dust countercontrol

For aligned homogeneous variables the same-action Hamiltonian retains

\[
H_{\rm other}=-3p_x^2/(4M_{\rm cos}^2\mathcal V)
 +(p_R^2+p_r^2)/(2\mathcal V)+p_\psi^2/(2K_Q\mathcal V)
 +Q^2/(2\mathcal VR^2)+\mathcal V V_{\rm hom}.
\]

Dust-clock H=Cbg H_other/C has volume curvature -3 Cbg/(2 Mcos2 volume C).
Force-clock H=-psi_clock_rate sqrt(Z), with the entire physical radicand
Z=2 K_Q volume[-H_other+p_psi2/(2 K_Q volume)-C P_tau], gives

\[
\det H_{(p_x,P_\tau)}=-3\dot\psi_0^2C^2K_Q^3\mathcal V^2/
 (2M_{\rm cos}^2Z^2).
\]

Require Z>0,positive Mcos2,K_Q,volume,C and a nonzero selected clock rate.
Exact full-radicand and direct compact Hessian-component tests retain every
radial/phase/dust momentum and potential term. V_hom is the homogeneous frozen
potential, NOT the missing canonical MAT invariant V; K_Q=3 eta is a diagnostic
choice, NOT microscopic matching. Einstein–dust removes extra sectors before
eta0 inverses and has d2H/dpx2=-3/(2 MP2 volume) in the varying-dust ensemble.
Hence this homogeneous sign alone is not a local propagating-ghost criterion.
No health/GR proof, negative-record deletion or charge-ensemble sign repair.

## Preservation, receipts and reproduction

V1 missing B and V4 missing registered A were implementation errors before
trajectory analysis. V2 and V3 were deliberately interrupted compiler controls;
V3 preserved54exact conservation messages. No full verdict or interrupted-stack
observation is claimed for them. All V1–V4 sources/sidecars and private error/
progress records survive; none wrote accepted scientific charge receipts.
V5 fully binds the declared maps and keeps equivalent explicit-H coefficient
domain/compact-clock algebra without changing thresholds or mathematics.

Fresh directory `Analysis/MasterTests/outputs/r4c1_three_family_charge_domain_attempt_05/`:

- summary.json: `54cd5450b784a21cfcac496ea7dc0e8b8ac4ebc5a74199225894919e54c2455e`
- formulas.json: `2337bb0b7b58be0c6e4fae9f971a334280091a3465f7ccc3384de1ea4f8f2b3a`
- canonical.json: `ce19a6128cd295b109393440ef999e8bb343505ef6e23488f4c8d17fba89e6aa`
- charge_records.json: `6dc3c5fe4d6c79f7edaef6f19580ed7cc7900fa42f185077e74a83d7f093220f`
- scope.json: `99f202352f9acfac4ad842a948d11e8d61aef1ddc13d155fb8d93479994668da`
- verification.json: `1128508ef9ef48eb1aa27437844b98603cd9b71e847fc9d28c32cc1b9eb5ffc7`

```powershell
& 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Scripts/itsm_context.py run -- 'C:/Users/brend/anaconda3/envs/itsm_env/python.exe' -B Analysis/MasterTests/test_01_r4c1_three_family_charge_domain_v5.py --replay Analysis/MasterTests/outputs/r4c1_three_family_charge_domain_attempt_05
```

Execution38248/replay27089 TERMINALexit0, `READ_ONLY_REPLAY_EXACT`. Every output
byte/sidecar compared without writes; source/sidecar metadata unchanged.
No live charge-domain numerical or replay job remains. Replay is not review.

Before append-only updates, entire queue/register and old sidecars were saved
privately. Required history: queue96710-byte prefix SHA
`d82c767e7615f118d2b188f20f8ad38b066fbccd9c2511d048f121a92ac8bef3`;
register169759-byte prefix SHA
`b7189a4cca7eba5a8263cab6a4f44a3d11838be710092c3636f692e9b423f8b1`.
Preserve mixed line endings byte-for-byte. Only living-index digests refresh;
no frozen scientific sidecar rewrites. Private drafts/logs/QA are not publications.

## Next bounded control and substantive holds

Define a NEW frozen fixed-charge preparation/comparison within the unchanged
action, preserving this original varying-charge preparation and all receipts.
No assumed cancellation or better cutoff, projection away of volume/constraints,
or resetting of original initial conditions. This control is not yet calculated.

Full physical energy/fixed-charge/constraint/zero-mode/singular admission,
quartic/all-sector characteristic and frequency domains, numerical/nonlinear
remainder, tensor/local-gravity compatibility and justified GR recovery remain
open. Prior coupled timing warning is unchanged and preparation-specific, not
an all-action no-go, physical scattering amplitude or cutoff. No family GO.
Stage3 still needs identifying matter-residue AND nonlinear-force matching;
assumed-coefficient residues are not identification. No C_chi/a0 or target fit.

Register R9-MT1-THREE-FAMILY-CHARGE-DOMAIN-V5 inherits RETARDED-CUBIC-V1,
PLANAR-WWR, GR-FAMILY-SURVEY, THREE-FAMILY-NONANALYTIC-ENTRY, RESPONSE-ENTRY,
TIME-RESPONSE, ODD-TAIL, G3I/G3N4, G3N5 mean-energy and all transitive review
debt. Provisional reuse only in scope; Rule-9 DEFERRED, no self-certification.
Stage2 INCOMPLETE / STOP_AND_ASSESS_DOMAIN_UNRESOLVED with approved same-action
continuation; Stage3 NOT_ENTERED; native full goal ACTIVE and INCOMPLETE.
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
canonical K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
No manuscript/PDF/vault/provider/model/runtime/commit/push/publication changes.
Native vault tools unavailable; no vault mutation.
