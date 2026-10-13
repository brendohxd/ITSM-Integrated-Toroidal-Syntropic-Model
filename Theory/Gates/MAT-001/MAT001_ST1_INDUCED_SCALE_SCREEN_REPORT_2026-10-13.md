# MAT-001 ST1: a static source exists, but the physical kinetic ratio remains free

13 October 2026. Result ID `MAT001-ST1-v1`. Claim **Conditional**.
Owner: separate induced-scale scalar-tensor matching control.
[Frozen contract](MAT001_ST1_INDUCED_SCALE_SCREEN_CONTRACT_2026-10-13.md), SHA
`d3708431f19d7d78451a3ffb641d8b715171b36400b2c439d6dfadd4a2fbbb7b`.

## Result and scope

For the declared separate scalar-tensor action, the metric transformation
correlates the scalar kinetic normalization and matter source. A genuine
parameterized nonzero static source exists with fixed Jordan particle masses.
It is not an identified numerical ITSM coupling: the physical kinetic ratio
and the choice of matter-mass law remain inputs, and the selected ITSM spatial
force EFT has not been matched.

| Registered choice | Calculated outcome |
|---|---|
| Fixed Jordan masses, p=0 and positive kinetic interior | Nonzero normalized static source; physical ratio B remains free |
| Jordan masses proportional to the same scalar, p=1 | Exact cancellation of the fractional Einstein mass response |
| Local Weyl kinetic relation B=0 | No canonically normalizable scalar; p=1 is a gauge redundancy, p!=1 imposes a trace condition |

Disposition: `PARAMETERIZED_STATIC_SOURCE_EXISTS_NUMERICAL_IDENTIFICATION_OPEN`.
This is a new declared control, not rehabilitation of the quarantined R5-P1
chain, a canonical action selection or a full finite-density gravity result.

## 1. Action and frame transformation

The contract defines

```text
F(sigma)=xi sigma^2; xi>0; sigma>0
S_J = integral sqrt(-g_J) [F R_J/2-zeta (grad_J sigma)^2/2]
      +S_Phi[Phi,g_E]+S_probe[sigma,g_J]+S_boundary
g_E=(F/M_P^2) g_J
xi sigma0^2=M_P^2
S_probe=-sum_a integral m_a0 (sigma/sigma0)^p ds_J.
```

The complex finite-density condensate is retained with the declared
quartic/sextic action, minimal to g_E. This particular placement is an
assumption: after the variable change its action has no direct sigma
dependence. It neither fixes the force coefficient nor replaces the
condensate by a real scalar. The finite-density curved background and
metric/frame/reservoir completion are not solved. A flat metric with nonzero
condensate stress is not asserted an on-shell solution.

Set `tau=ln(sigma/sigma0)`, oriented toward increasing sigma. Then

```text
g_J=exp(-2 tau) g_E
sqrt(-g_J)/sqrt(-g_E)=exp(-4 tau)
R_J=exp(2 tau)[R_E+6 Box_E tau-6 (grad_E tau)^2].
```

The bulk gravitational term gives a retained divergence `3 M_P^2 Box_E tau`.
Its surface term cancels the corresponding part of the transformed F K
boundary action in the declared boundary convention. The transformed bulk is

```text
L_E = M_P^2 R_E/2 -M_P^2 B (grad_E tau)^2/2
B=6+zeta/xi.
```

The six is metric-scalar mixing. It is absent from an incorrect normalization
based only on the Jordan scalar kinetic term. The general coefficient check
`M_P^2[zeta/F+3(F'/F)^2/2] (d sigma/d tau)^2=M_P^2 B`
recovers the same result. A sigma^4 potential would become an Einstein-frame
constant, not a mechanism selecting B or stabilizing tau; this screen uses
the separate sigma potential exactly zero.

## 2. Signed normalized matter source

The worldline element transforms as `ds_J=exp(-tau) ds_E`. Therefore

```text
m_E(tau)=m_a0 exp[(p-1)tau]
effective probe metric=exp[2(p-1)tau] g_E.
```

In the finite positive interior `0<B<infinity`, define the physical canonical
scalar of this control by

```text
chi=M_P sqrt(B) tau
K_tau=M_P^2 B
V_ST1=d ln(m_E)/d chi=(p-1)/(M_P sqrt(B))
L_src=-rho_b V_ST1 delta chi
g_can=-V_ST1=(1-p)/(M_P sqrt(B)).
```

`[K_tau]=2`, `[V_ST1]=[g_can]=-1`. The signed source is distinct from its
squared exchange coefficient. K_tau is the normalization of this candidate's
Lorentz-invariant scalar; it is **not** the canonical ITSM K_Q. No field map
to the preferred-frame force sector has been established.

The scalar equation in the constant-sigma reference chart is
`M_P^2 B Box_E tau=(1-p) T`, or `Box_E chi=-V_ST1 T`. For pressureless
probes `T=-rho_b`, this becomes `Box_E chi=V_ST1 rho_b`.
The local vacuum Fourier exchange kernel is

```text
R_ST1(omega,k)=V_ST1^2/(omega^2-k^2)
R_ST1(0,k)=-V_ST1^2/k^2, for k!=0.
```

This establishes the local scalar static source when p!=1. It is not a
global torus inverse or the full finite-density weak-field response. Torus
sources must be compensated; no zero-mode inverse is used. The ordinary
quadratic spatial gradient in this action does not produce ITSM's selected
Y^(3/2) operator or the square-root galactic force law.

## 3. Independent Jordan trace/source check

At constant sigma0, let `F0=xi sigma0^2`, `F'_0=2 xi sigma0`. Varying the
metric conformally gives the linear trace equation, while varying sigma
gives its scalar equation:

```text
F0 R_lin-3 F'_0 Box(delta sigma)+T=0
zeta Box(delta sigma)+(F'_0/2) R_lin+p T/sigma0=0.
```

The p T/sigma0 term comes from varying the explicit particle mass; it must
not be omitted. Eliminating R_lin gives

```text
(zeta+6 xi) Box(delta sigma)=(1-p)T/sigma0,
M_P^2 B Box(delta tau)=(1-p)T.
```

This independently checks the normalized source and the gravitational mixing
coefficient. The metric/scalar variation identities are analytic inputs;
the executable performs their explicit linear elimination and comparison.
It does not implement a general full ADM or finite-density constraint solver.

## 4. Matter-scale cancellation and the Weyl boundary

For p=1, the Jordan mass increase exactly cancels the conformal worldline
factor: m_E=m_a0. The direct matter source for chi is zero. At B>0 the
scalar still has its free kinetic dynamics and gravitational stress; zero
direct source does not imply that the whole theory is pure GR.

Local Weyl symmetry of the declared scalar/gravity control has

```text
zeta=-6 xi; B=0
g_J -> exp(-2 alpha(x)) g_J
sigma -> exp(alpha(x)) sigma
g_E unchanged.
```

At p=1, all retained matter/condensate actions depend on the invariant g_E;
the sigma variable is a redundant representation of the metric. There is no
independent scalar pole to normalize. At p!=1, the unnormalized scalar
equation requires `(1-p)T=0` in this zero-potential model. Generic massive
pressureless sources do not satisfy it. A potential or new operators would
define a different candidate.

Do not insert B=0 into the canonical source expression and call its divergence
a physical force. Likewise `xi=1/6,zeta=+1` gives B=12, not the Weyl-degenerate
point in this action's sign convention. The exact Weyl relation has the
opposite Jordan kinetic sign. B<0 is a negative scalar kinetic direction in
this simple Einstein-frame control and is outside the admitted interior.

## 5. What remains free, and the conditional bound

The chart change `sigma'=s sigma`, `xi'=xi/s^2`, `zeta'=zeta/s^2`,
`sigma0'=s sigma0`, s>0, leaves `xi sigma0^2`, tau, B and the normalized
source invariant. B is therefore a physical ratio, not a removable field
normalization.

For p=0, the frozen rational counterfamily uses `M_P=1`, `xi=1/4`,
`sigma0=2`, identical condensate action/state inputs, and

| B | zeta | Signed V_ST1 (rounded diagnostic) |
|---:|---:|---:|
| 8 | 1/2 | -0.3535533905932738 |
| 14 | 2 | -0.2672612419124244 |
| 30 | 6 | -0.1825741858350554 |

These are arbitrary parameter controls in units of the chosen M_P, not
physical ITSM constants. They have the same reference Einstein gravitational
coefficient and, at constant tau with no probe background, the same retained
condensate/background equations; their source residues differ. No new
background integration is claimed. The declared action cannot numerically
select V_ST1 from those background inputs.

An explicit additional restriction `zeta>=0` yields B>=6 and, for p=0,

```text
abs(V_ST1)<=1/(sqrt(6) M_P).
```

This is a **Conditional bound for that subclass**. Positivity of the full
Einstein scalar only requires B>0, permitting -6xi<zeta<0. The bound must
not be extended to that broader domain or promoted as a canonical ITSM bound.
The approach to B=0 supplies no established perturbative cutoff/window.

In the local massless universal-probe gravity control, the ratio of scalar
to tensor exchange is `alpha_force=2 M_P^2 V_ST1^2=2(p-1)^2/B`. Thus
`G_N,control=G_E(1+alpha_force)`, `G_E=1/(8 pi M_P^2)`. Treating an observed
Newton response as G_E without the scalar/matter/frame calculation would
import a normalization assumption. No observed G_N or local-gravity bound is
fitted or used to select B here. This is not the full ITSM Cavendish/PPN metric.

## 6. Verification, failure preservation and provenance

[Executable](../../../Analysis/MAT/MAT-001/ST1_INDUCED_SCALE/mat001_st1_induced_scale_screen.py)
SHA `9bdfcc476d50fc7fee1e53b3698655ab5d058274f8d8e485553685ea88f8efdf`.
[Attempt-02 receipt](../../../Analysis/MAT/MAT-001/ST1_INDUCED_SCALE/outputs/st1_attempt_02/summary.json)
SHA `5e3b504bf9551ac368caea908192e167f202e68543b1a4badedd9dbdb564ef15`.

Actual result: **78/78 local checks**, zero failed/unknown, six rational
coefficient/mass-law cases at 80-decimal arithmetic precision. All ten receipt
source pins were independently rehashed with no mismatches. The maximum
Jordan/Einstein source-normalization discrepancy is `1.317774743e-82`; the
maximum direct/canonical static-exchange discrepancy is `6.588873715e-83`.
These are arithmetic comparisons for specified controls, not measured physics
or independent Rule-9 review.

The fresh replay into ignored `.local/itsm-context/st1_replay_2026_10_13/`
matched the receipt and sidecar byte-for-byte. Attempt-02 is 14085 bytes;
the two original files' sizes and timestamps remain unchanged through replay.
Actual dimension checking acts on the coefficient expressions, including
dimensionless pi, rather than on supplied labels. Negative controls catch
omitted metric mixing, lost matter-frame factor, incorrect Weyl sign,
erased source sign, inserted same-scale source, unbacked Newton normalization
and premature canonical promotion. The singular Weyl branch is classified
before canonical normalization; it is never evaluated as a finite pole.

Attempt-01 exited 1 before creating a scientific receipt: the dimensional
expression walker did not recognize pi as a dimensionless numerical constant.
Its complete private failure log is
`.local/itsm-context/output-82b37e28376f4d24a9851a41daa67845.txt`, SHA
`e555d120fd0c654c91716ee9e606a252d10ddf9044cddc437cd65cbe8cbd692a`.
The failed executable version is preserved privately at
`.local/itsm-context/st1_attempt01_source.py`, SHA
`8dc08ca25d33c3501288f819753178b7ff5f409679cbd5caa8313d944fbb34d5`.
The only repair was recognizing symbolic numerical constants as dimensionless;
no action, matching relation, assertion expectation or parameter set changed.
The frozen contract retained its bytes. Do not relabel the failed run successful.

Reproduce into a new protected output directory:

```powershell
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MAT/MAT-001/ST1_INDUCED_SCALE/mat001_st1_induced_scale_screen.py --out .local/itsm-context/st1_new_replay
```

Primary source controls: [Jarv et al., PRD 91, 024041](https://arxiv.org/abs/1411.1947)
supports the frame-invariant matter/kinetic normalization method; its general
transformation and scalar-tensor coefficient sections were checked.
[Sotiriou and Faraoni, RMP 82, 451](https://arxiv.org/abs/0805.1726)
provides an independent discussion of the degenerate Brans-Dicke scalar,
including cancellation of its Einstein kinetic term. Our coefficient map
`omega_BD=zeta/(4xi)` gives B=4omega_BD+6, with B=0 at omega_BD=-3/2.
The control action and its mass assignments are declared here; neither paper
fixes an ITSM coupling. No paper's full theory or numerical claims are reproduced.

## 7. Next permitted step and governing holds

This screen supplies a valid parameterized static source in its positive
interior. It reduces this candidate's normalization ambiguity to B and the
matter mass assignment p; it supplies no selection principle for either.
A subsequent mechanism must determine that physical ratio or rigorously bound
it from independent inputs, and produce the intended IR force action. A
fully scale-following mass assignment or an exact local Weyl compensator does
not provide the required nonzero scalar force in this declared class.

The finite-density condensate was retained as a spectator, not used to derive
the new force field. Its microscopic bridge, the preferred-frame spatial law,
full gravitational/constraint domain, cutoff and observable metric remain
substantive missing inputs. Pending review alone does not prevent diagnostics.
No canonical selection, Stage-3 physical prediction or TOP-X4 pivot follows.

Inherit the route and RM1 reports for scope/authority, the R4 signed convention,
and the relevant R5/UVIR action boundaries. These are not independently reviewed
inputs. Review DEFERRED; the new result is Conditional with inherited review debt.

```text
research_execution=PROCEED_PROVISIONALLY (control and identifying diagnostics)
canonical_matching=HOLD_SUBSTANTIVE
canonical_Tests_1_3=HOLD_SUBSTANTIVE
MAT-001=BLOCKED
UVIR-003=IN_PROGRESS
K_Q=NOT_DERIVED
V=NOT_COMPUTED
Stage4A=CLOSED
physics_pass=false
gate_effect=NONE
review_status=DEFERRED
Rule9_cleared=false
```

The memory-bank workflow supplied authority/continuity guidance; current
pinned repository sources and the declared new calculation supply evidence.
Only new scientific artifacts and the living deferred-review entry are written.
Optimizer/replay/failure backups stay private and ignored. No memory mutation,
provider/model dispatch, manuscript, publication, commit or push is included.
