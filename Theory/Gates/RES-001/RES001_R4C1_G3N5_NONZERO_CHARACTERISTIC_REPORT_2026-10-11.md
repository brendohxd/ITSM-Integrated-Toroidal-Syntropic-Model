# G3N5 nonzero-mode canonical and mixed-order characteristic audit

Date: 11 October 2026 (Australia/Perth). Version 1.
Status: CONDITIONAL_NONZERO_FAMILY_WITH_ZERO_SPEED_JORDAN_OBSTRUCTION.
physics_pass=false; gate_effect=NONE; Rule9_cleared=false; review DEFERRED.

## Outcome

The bounded one-direction audit is complete. The frozen R4C1/B1 action has an
explicit checked nonzero-mode canonical Hamiltonian, eight ordinary wave
branches, one spatially dispersive branch and one zero-speed/slow branch.
The positive ten-coordinate time matrix does not establish physical stability:
the specified wave-scale reduction has a zero-speed Jordan defect, the full
Hamiltonian retains a negative spatial trace direction, and the formal evolving
slow action has time coefficient **-11/6**. No adverse result is removed.

Main v2 passes **121/121 local checks and exact read-only replay**. The separate
real-space principal-density derivation passes **9/9 and exact replay**. These
are local calculations by the same agent, not independent external reviewers.
Computational acceptance establishes the derivation, including its adverse
disposition; it is not a physics pass or a general no-go for ITSM.

The [frozen contract](RES001_R4C1_G3N5_NONZERO_CHARACTERISTIC_CONTRACT_2026-10-11.md)
and [assertion-correction addendum](RES001_R4C1_G3N5_NONZERO_ASSERTION_V2_ADDENDUM_2026-10-11.md)
own this task. Inputs remain the unchanged full 22-field kernel,
[constraint-response report](RES001_R4C1_G3N5_CONSTRAINT_RESPONSE_REPORT_2026-10-10.md)
and [homogeneous energy report](RES001_R4C1_G3N5_MEAN_MODE_ENERGY_REPORT_2026-10-11.md).

## Domain and canonical structure

Family k=(ell,0,0), ell>0; integer ell on coordinate periods 2*pi, with the
negative conjugate mode included. p=ell/a is a formal dimensionless physical
wavenumber, not a measured scale. Use B1's unchanged parameters, positive
a,C,rho_m and saved 257 coefficient points on t_E in [0,0.05]. K_Q=3 is a
registered action parameter, not a microscopic derivation.

Use T=0, alpha=-beta*Pi, nu=0 and k_i M_ij=0. Eliminate S_i and Z only on the
checked regular block. Recover density and norm multiplier as in the parent
reduction. No local complex phase is quotiented, no new dust charge is fixed,
and no homogeneous negative direction is discarded.

For the full reduced action, v=a^3 and dagger denotes the Fourier adjoint:

```text
L2 = v*(y^dagger A y/2 + Re(y_dot^dagger R y)
        + y_dot^dagger K y_dot/2)
p_y = v*(K y_dot+R y)
H2 = (y,p_y)^dagger HH (y,p_y)/2
HH_yy = v*(R^dagger K^(-1) R-A)
HH_yp = -R^dagger K^(-1); HH_pp = K^(-1)/v.
```

All mixed/value blocks are exported, not just eigenvalues. The unreduced
momentum one-form pulls back to this p_y exactly. T and nu have fixed coordinate
variations, not necessarily zero momenta: dT=dnu=0 eliminates their one-form
contribution. Confusing fixed coordinates with null-velocity primary momenta
caused an explicitly preserved v1 assertion failure, not a changed constraint.
Auxiliary momenta vanish; their velocity-dependent reconstruction adds no
hidden symplectic term. The canonical map obeys

```text
J*HH*M - M*L_Euler - M_dot = 0,
M = [[I,0],[v*R,v*K]].
```

Coefficient derivatives and the a^3 measure are retained. In a cell-normalized
cosine/sine basis the +/- Fourier pair has twenty real coordinates and twenty
real canonical pairs; the compact notation uses ten complex coordinates.
This is a chart count, not a global physical degree-of-freedom theorem.

SO(2) coordinates are h=(M11+M22)/sqrt(2), TT+=(M11-M22)/sqrt(2), TTx=M12,
Vx,Vy,Vz,du,dv,dr,Pi. K is exactly diagonal in this basis:

```text
diag(33/4,1/4,1/2,1/6,1/6,1/6,1,1,1,3), det(K)=11/768.
```

It is background independent and positive on this registered nonzero chart.
The k=0 chart is different and remains in its owning report, with the original
negative homogeneous direction. A singular 1/k shift inverse is not continued
to it.

## Mixed-order dispersion and eigenvectors

The Z equation gives Z=-(Delta Pi+psi_dot*div V). Its elimination retains
-b*|Delta Pi+psi_dot*div V|^2/2; therefore the force scalar has a p^4 term.
It would be incorrect to classify the full action as an ordinary second-order
wave system or discard Pi in a large-p limit.

For harmonic e^(-i*omega*t), the principal pencil is
P=K*omega^2-i*omega*(R_pr^dagger-R_pr)+A_pr. With c=omega/p, its complete
wave-scale determinant is the leading p^22 coefficient:

```text
-c^2*(c^2-1)^4*(5*c^2-4)^2*(3*c^2-1)
 *(13*c^2-u0^2-v0^2-13)/449280.
```

With sigma=omega/p^2, its complete fast-scale determinant has leading p^40
coefficient sigma^18*(33*sigma^2-5)/2304. The zero factors in this fast-scale
polynomial represent slower branches; they are not nineteen additional modes.

| Branch | Leading frequency law | Count |
| --- | --- | --- |
| TT metric | omega^2=p^2 | 2 |
| Transverse frame | omega^2=(4/5)*p^2 | 2 |
| Complex radial and real r | omega^2=p^2 | 2 |
| Complex phase | omega^2=[1+(u0^2+v0^2)/13]*p^2 | 1 |
| Frame scalar | omega^2=p^2/3 | 1 |
| Force-scalar dispersive | omega^2=(5/33)*p^4+subleading terms | 1 |
| Zero-speed/slow | omega/p -> 0 | 1 |

All nonzero wave squared speeds and the fast squared coefficient are positive
for real u0,v0. This is a formal result of the declared action, not a physical
light-cone, EFT-window or all-background stability certificate.

The residual scalar wave pencil after leading fast-block elimination is

```text
[[33*c^2/4+1/4, -c/sqrt(2)],[-c/sqrt(2), c^2/6]].
```

Its four-state frequency companion, with states (h,Vx,c*h,c*Vx), is

```text
[[0,0,1,0], [0,0,0,1],
 [-1/33,0,0,4/(33*sqrt(2))], [0,0,3*sqrt(2),0]].
```

At c=0, algebraic multiplicity is two but geometric multiplicity is one:
e0=(0,1,0,0), e1=(2*sqrt(2),0,0,1), C*e0=0 and C*e1=e0. The same chain
is checked in the complete eighteen-state wave companion, with all tensor,
vector and matter branches included. Nonzero scalar roots and the separate
fast companion have the expected simple eigenspaces; matter eigenvectors and
the zero-radius degeneracy are checked explicitly.

Thus a complete ordinary wave-scale characteristic basis is absent in the
stated reduction. Real roots alone are insufficient. For the standard
first-/second-order criterion see [Gundlach and Martin-Garcia](https://arxiv.org/html/gr-qc/0506037v1),
Definitions 1-2 and Lemma 1. Their theorem is not automatically a theorem for
this fourth-spatial-order mixed system. The defect does not establish that
every possible weighted formulation is ill-posed. Pressureless-dust variables,
the regularity norm and the constraint-preserving mixed-order evolution still
need a proper uniform estimate. No global strong-hyperbolicity claim is made.

## Evolving formal slow action and retained energy signs

Transform the complete evolving action before taking p->infinity:
h,du,dv,dr scale as 1/p; Pi=i*psi_dot*Vx/p+chi/p^2; p_dot=-H*p. This map is
invertible at finite p>0. Keep all coefficient derivatives. An explicit
Hermitian total-derivative boundary term transfers auxiliary velocities;
then eliminate the regular five-variable algebraic block
diag(1/4,-G_matter,-1,-b). Here det(G_matter)=1+(u0^2+v0^2)/13>0 and b=5/11.

For the remaining Vx, write Lslow/v=Kslow*|Vx_dot|^2/2+
Rslow*Re(Vx_dot^* Vx)+Aslow*|Vx|^2/2. The exact coefficients are

```text
Kslow = -11/6
Rslow = -121*H/30-11*psi_dot/15
Aslow = -253*H^2/30-22*H*psi_dot/15+203*psi_dot^2/75
        +r_dot^2+u_dot^2+v_dot^2.
```

The independent full-Euler route gives the same action equation:

```text
E2=11/6; E1=11*H/2
E0=11*H^2/3-22*H*psi_dot/15-419*psi_dot^2/150
   -5*(r_dot^2+u_dot^2+v_dot^2)/6-869*rho_m/450
E2*Vx_ddot+E1*Vx_dot+E0*Vx=0.
```

The negative slow coefficient is compatible with positive full-chart K because
the asymptotic elimination also uses a stiff spatial trace block with an
indefinite energy sign. This limit is not an invertible finite-k canonical
restriction. Do not normalize the ODE and erase the action prefactor, or call
it a proven physical ghost without the physical window and reduction analysis.

The complete Hamiltonian already retains a negative spatial trace direction:
after completing its positive momentum square, the leading h energy at zero
velocity is -a^3*p^2*|h|^2/8. Thus no full positive-energy certificate follows
from HH_pp>0. Frozen instantaneous frequencies/growth rates are saved as
diagnostics, not conclusions about evolution on the time-dependent background.

## Verification, failed attempts and preservation

The main calculation matches ell=1 to every saved reduced coefficient/map.
It checks complete canonical momentum pullbacks, the evolving Hamilton/Euler
identity, Hermitian/real symplectic forms, SO(2) separation, all principal
blocks against a separate real-space ADM/frame/regulator density, both
determinant scales, eigenvectors/Jordan chains, slow action/Euler equivalence,
singular ranks and exact serialization roundtrips.

At 257 saved background points the normalized Hamilton/Euler residual is
1.1103e-16. Frozen eigen controls at p=1,2,4,8,16,32,64,128 at initial/middle/final
points have residual <=3.5269e-15. Both real quadratures have zero symplectic
residual. The registered limits remain <=1e-10. Sampling is not a full-time
stability proof or physical cutoff derivation.

Main v1 remains FAIL_LOCAL_CHECKS, 103/106; separate principal v1 remains
FAIL_LOCAL_CHECKS, 7/9. The [addendum](RES001_R4C1_G3N5_NONZERO_ASSERTION_V2_ADDENDUM_2026-10-11.md)
records their exact assertion defects and the new versioned corrections.
The principal-density formulas are byte-identical between v1/v2; negative
coefficients and Jordan evidence remain unchanged. An initial main startup
stopped before calculation because its new source sidecar had not yet been
created; adding that new sidecar did not edit the source or old evidence.

Source checks preserve 371 registered input/sidecar files in hash, size and
last-write time. The replay preservation audit covers 379 unique files,
including the current outputs. Old G3/N3 failures, five binary64 response-v1
failures (120/125) and three inherited sidecar absences remain declared.

Reproduction (all paths repository-relative):

```text
python -B Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_characteristic_v2.py --replay Analysis/MasterTests/outputs/r4c1_g3n5_nonzero_characteristic_attempt_02
python -B Analysis/MasterTests/test_01_r4c1_g3n5_nonzero_principal_v2.py --replay Analysis/MasterTests/outputs/r4c1_g3n5_nonzero_principal_attempt_02
```

[Main receipt](../../../Analysis/MasterTests/outputs/r4c1_g3n5_nonzero_characteristic_attempt_02/summary.json):
610b8b58037d60c694093b045a55745df0f39858b829447ac18d7d2e2bf88020.
[Separate receipt](../../../Analysis/MasterTests/outputs/r4c1_g3n5_nonzero_principal_attempt_02/summary.json):
cf753b645edee69813aefa050ee1719b0d2d8d34a44ba28c1b89ef8859dcaa8c.
[Full matrices](../../../Analysis/MasterTests/outputs/r4c1_g3n5_nonzero_characteristic_attempt_02/matrices.json),
[characteristics/slow coefficients](../../../Analysis/MasterTests/outputs/r4c1_g3n5_nonzero_characteristic_attempt_02/formulas.json)
and [diagnostics](../../../Analysis/MasterTests/outputs/r4c1_g3n5_nonzero_characteristic_attempt_02/diagnostics.json)
retain the complete evidence.

## What remains and permitted reuse

Provisional reuse is allowed for the exact canonical map, principal decomposition,
formal dispersion, Jordan obstruction and evolving slow coefficients in this
one family. Rule-9 is DEFERRED, not cleared; it does not alone block research.
The defect and negative slow action are substantive findings, not review-only
or label-only blockers.

Next bounded question: can the pressureless-dust and dispersive sectors admit
an action-preserving constraint-compatible weighted evolution estimate, and
what does the negative slow energy represent within an actually justified
physical window? Do not change couplings, remove the slow branch or import the
extra fixed-dust homogeneous ensemble to manufacture a healthy result.

Other directions/backgrounds, physical cutoff/window and causality, nonlinear
unsmoothed force, healthy GR, G_eff/PPN, weak-field closure and microscopic
matching remain. Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003
IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
No manuscript/PDF, vault/runtime/provider/model change, commit, push, site
deployment, submission or canonical promotion is included. Queue/register
entries are append-only with their previous byte prefixes retained.
