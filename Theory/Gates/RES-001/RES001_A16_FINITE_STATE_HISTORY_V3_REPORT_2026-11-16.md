# A16.2: finite-time scalar chart and bounded condensate history

16 November 2026. Conditional original R4C1/B1; High confirmed by operator.
Disposition: COMPLETE_SCOPED_MAP_AND_EXACT_HISTORY_GAIN_BOUNDS.
The full A16.2 reduction/physical-mechanism route remains OPEN.
physics_pass=false; gate_effect=NONE; Rule-9 review DEFERRED.

## What this adds

The twelve reconstructed scalar values now have an exact inverse with bounds
over the registered time interval, rather than only at its initial event.
Eliminating four condensate variables yields exact two-time history laws for
both the eight retained variables and the pressure observation. Hidden
initial-state forcing and feedback are both retained, with explicit finite
gain bounds. No two-time kernel has yet been numerically evaluated here.

The [preceding evolution calculation](RES001_A16_PRESSURE_EVOLUTION_V3_REPORT_2026-11-16.md)
showed a controlled pressure response and a high-mode sign reversal. This
calculation supplies a finite-time coordinate and history framework for that
response. It does not add a fundamental force, adopt Campbell's ontology,
prove irreversible memory, or identify condensate state with entropy.

## Finite-time scalar state and its inverse

Keep the existing reconstructed configurations (area, longitudinal frame,
modulus squared, local phase, reservoir and force) and six rates. Area/frame
rates are coordinate rates; the remaining four retain their proper-frame
lapse corrections. Let E embed the original twelve scalar coordinates and
S=Q E reconstruct the twelve scalar values. The unchanged full generator
has vanishing scalar/complement cross blocks.

The map is block triangular:

    S = [ A  0 ],       S_inverse = [ A_inverse                     0         ].
        [ D  A ]                   [ -A_inverse D A_inverse       A_inverse ]

The condensate part of A maps (delta u,delta v) to
(delta s,delta theta), s=u^2+v^2, with determinant 2. Its direct inverse is

    delta u = u delta s/(2s) - v delta theta,
    delta v = v delta s/(2s) + u delta theta.

Thus det(S)=4 wherever the local phase chart is defined. Cancellation in the
determinant does not define the phase map at s=0. The full interval uses the
pinned exact-background enclosure and the enlarged rational box from the
earlier continuous numerical certificate. On that box:

- s > 0.97603;
- ||S||_infinity <4.393 and ||S_inverse||_infinity <2.071;
- ||d_t S_inverse||_infinity <5.449.

These are outward-rounded bounds in the stated chart, not invariant physical
constants. They hold throughout [0,1/20] at ell=4,8,16,32,64. Positive a,
rho and C are retained. Zero momentum and global phase/winding changes are
outside this local chart.

The exact scalar generator is

    G_scalar = (S_dot+S L_scalar) S_inverse.

Both inverse identities, its derivative identity and generator recomposition
are verified symbolically. The original full-vector propagator plus bounded
coordinate maps gives a finite full-scalar propagator bound. Its conservative
endpoint bounds range from about 9.03e4 to 2.53e9 across the five modes;
they are not useful small-error estimates or measured amplification factors.
The separately certified pressure trajectory remains the sharper result for
its particular initial direction.

## Declared 8+4 split and actual hidden principal operator

Retain

    R=(area,Vx,delta r,Pi,area_dot,Vx_dot,proper_r_rate,P_n).

Eliminate only

    h=(delta u,delta v,proper_u_rate/p,proper_v_rate/p), p=ell/a.

This is a diagnostic split of the same constrained linear chart. Calling h
hidden does not make it an autonomous physical or thermodynamic reservoir.
The full mixed generator is derived from the action export, with the lapse,
map drift and p_dot=-H p intact. Omitting the momentum drift subtracts H
from each scaled condensate-rate row; that omission is rejected exactly.

The actual hidden principal matrix is

    D_hidden = p J_K + Remainder,
    J_K = [ 0  I ],    K=I+w w^T/13, w=(v,-u)^T.
          [-K  0 ]

The squared characteristic values of this projected hidden block are 1 and
1+s/13. They are not a determination of physical coupled-mode propagation
speeds or a causality verdict. A unit-speed principal guess is explicitly
rejected. This K agrees with the condensate weight already present in the
[earlier full-vector propagator owner](RES001_R4C1_G3N5_DUST_UNIFORM_PROPAGATOR_REPORT_2026-10-11.md);
it is not a new field or coefficient.

Use W=diag(K,I). It obeys W>=I and W<=1.07875 I on the box. The principal
part is exactly W-skew. Keep the full energy derivative

    E=h^dagger W h,
    E_dot=h^dagger (W_dot+W D_hidden+D_hidden^dagger W) h.

The residual after subtracting p J_K has no growing momentum power. The
Gershgorin upper bound of half the displayed Hermitian derivative gives
mu>=0 with E_dot<=2 mu E. W_dot includes the actual rotating background;
dropping it is rejected. Consequently

    ||U_h(t,s)||_(W(s)->W(t)) <= exp(mu(t-s)),
    ||U_h(t,s)||_infinity <= c_W exp(mu(t-s)),
    c_W=2 sqrt(W_upper)<2.078.

The factor 2 converts four-component infinity input norm to Euclidean norm.
The matrix norm uses complex moduli; coefficient bounds may conservatively
use absolute real and imaginary parts. W is an evolution weight, not a
physical Hamiltonian. No full-system bound was transferred to this hidden
block; its generator and energy derivative were calculated separately.

## Exact history laws and what the gains do not prove

Write the actual mixed equations as

    R_dot=A R+B h,       h_dot=C R+D_hidden h,
    P=P_R R+P_h h.

The time-ordered U_h solves its nonautonomous initial-value problem. Then

    R_dot=A R+B(t)U_h(t,0)h0
          +integral_0^t B(t)U_h(t,s)C(s)R(s) ds,

    P=P_R R+P_h(t)U_h(t,0)h0
      +integral_0^t P_h(t)U_h(t,s)C(s)R(s) ds.

These are deterministic identities, with noncommuting propagation and the
original initial data. A frozen exponential is not substituted for U_h.
An independent noncommuting polynomial fixture verifies both Volterra
identities and rejects omission of hidden initial data.

For the previously certified radial seed, R(0)=0 and
h0=(0,0,1/ell,0). Independently differentiating the actual pressure observation
gives, at the registered initial event in all five modes:

    d_t[P_h(t) U_h(t,0) h0] = -2341/840,
    P_R B h0 = 0.

The total initial proper pressure-rate result agrees because the initial
lapse perturbation vanishes. Setting hidden initial data to zero would lose
this nonzero response despite the initially matched retained values.

Let b,c and ph bound the infinity operator norms of B,C and P_h. The uniform
retained and pressure kernel gains are bounded by c_W exp(mu T) b c and
c_W exp(mu T) ph c respectively, T=1/20. All constants are exported as exact
rational upper bounds. Selected outward-rounded displays are:

| ell | mu upper | Weighted amplification upper at T | Retained kernel gain upper | Pressure kernel gain upper |
| --- | ---: | ---: | ---: | ---: |
| 4 | 2.066 | 1.109 | 805.43 | 167.22 |
| 8 | 1.053 | 1.055 | 833.59 | 151.01 |
| 16 | 0.547 | 1.028 | 945.19 | 158.72 |
| 32 | 0.294 | 1.015 | 1194.86 | 192.74 |
| 64 | 0.167 | 1.009 | 1707.12 | 269.73 |

For an independently bounded retained history M_R=sup||R||, the omitted
feedback at time t would be bounded by T times the kernel gain times M_R.
Those coefficients are approximately 40.27--85.36 for the retained RHS and
7.55--13.49 for pressure. These are upper bounds on an omitted term, not
errors in the evolved retained solution. No M_R is assumed here. The bounds
do not justify discarding feedback or claiming a useful instantaneous law,
short memory, decay time, dissipation or thermal closure.

## Verification, preserved failures and evidence

The main calculation passes 59/59 controls. Its independent audit passes
90/90 using its own exact-rational interval evaluator, direct trace/determinant
identities, independently differentiated background/weight and pressure maps,
and exponential-series tail bounds. It imports neither the numerical solver
nor the dyadic arithmetic implementation. This is separate computational
verification by the same assistant, not independent peer review.

Both packages replay byte-identically, including the main formulas and all
receipt sidecars. Seven final preservation/replay checks pass. All 709 pinned
inputs retain their hashes; pre/post source timestamp checks also pass.

V1's 52/53 receipt is preserved: its unit-speed principal assumption failed,
while its finite map and direct Euclidean finite-mode bounds were computed.
V2 derives the actual moving weight; its 58/59 receipt is also preserved.
Its only failure was a SymPy characteristic-polynomial generator that dropped
the requested real-symbol assumptions. V3 uses a direct determinant identity.
The V2 and V3 formula artifacts are byte-identical. No equation or coefficient
was changed to make the final test pass. See the
[V1 note](RES001_A16_FINITE_STATE_HISTORY_V1_ATTEMPT_NOTE_2026-11-16.md) and
[V2 note](RES001_A16_FINITE_STATE_HISTORY_V2_ATTEMPT_NOTE_2026-11-16.md).

- [Contract](RES001_A16_FINITE_STATE_HISTORY_V3_CONTRACT_2026-11-16.md).
- [709-input manifest](RES001_A16_FINITE_STATE_HISTORY_V3_INPUTS_2026-11-16.json).
- [Executable](../../../Analysis/MasterTests/test_a16_finite_state_history_v3.py).
- [Main receipt](../../../Analysis/MasterTests/outputs/a16_finite_state_history_v3_20261116/receipt.json), SHA256 `e2f6d4f5fd1b17faee3e9188cb4f59d5896bda8607527f0064412d05d3f051af`.
- [Exact formulas](../../../Analysis/MasterTests/outputs/a16_finite_state_history_v3_20261116/formulas.json).
- [Independent audit](../../../Analysis/MasterTests/outputs/a16_finite_state_history_audit_v1_20261116/receipt.json), SHA256 `283a9549ad9020634b2b33371d4192f670fbb3342395977bc727ededeade88b7`.
- [Replay/preservation receipt](../../../Analysis/MasterTests/outputs/a16_finite_state_history_v3_verification_20261116/receipt.json).

Next: evaluate the actual time-dependent kernels with controlled numerical
error and compare the retained history evolution against the certified full
response. Test whether any useful reduction follows without deleting initial
state or feedback. A16.5 time-scale separation is still open; failure of a
small instantaneous approximation is not failure of the exact history law.

All physical and matching qualifications remain: no nonlinear validity
window, healthy coupled modes, entropy production, new mechanism, MAT/GR
clearance, numerical acceleration prediction or publication promotion.
R-tau remains separate and unadopted. No paper/PDF, site, external review,
bulk vault sync, commit, push or deployment was performed.
