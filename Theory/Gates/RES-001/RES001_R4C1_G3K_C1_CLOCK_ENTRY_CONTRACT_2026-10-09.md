# R4C1-G3K-C1: preferred-clock entry contract

Date: 9 October 2026. Test-1 prerequisite; unchanged R4C1/G3T/G3K inputs.
Conditional; PROCEED_PROVISIONALLY; review DEFERRED.
physics_pass=false; Rule9_cleared=false; gate_effect=NONE.

## Scope and decision

Determine whether the registered homogeneous tilted metric/frame admits
a globally single-valued REAL preferred clock with dT=-mu U_flat, mu>0,
on I x T3. Separately derive the orientation-preserving paired-branch
clock-map domain of the inherited HEALTHY FIXED-FRAME comparator.

This is a geometric and necessary clock-map entry audit. It is not the
coupled characteristic/energy-residue classification, global field-Cauchy
theorem, physical cutoff, ghost theorem or all-action no-go.

Use the actual T3 quotient. A locally exact preferred-clock potential,
a circle-valued potential or a clock on the universal cover must not be
called a global real time function on the quotient.

## Frozen inputs

G3K report:
Theory/Gates/RES-001/RES001_R4C1_G3_FINITE_K_SCALAR_REPORT_2026-10-08.md,
SHA-256 81c11fc9cc9efbb9ad6b2d6f0e2bd26653a13d2fb126031b4941ae326f782c31.
G3K receipt:
Analysis/MasterTests/outputs/r4c1_g3k_attempt_02/summary.json,
SHA-256 131e175a3d1a6979a7c3a68a6f5d84a21b533ce01a7850066fcfde5800d2d6ab.
G3K samples:
Analysis/MasterTests/outputs/r4c1_g3k_attempt_02/samples.json,
SHA-256 69102fff332222f34684151e08a218fd92c6ae7a5153fd49d5900cf9e4b430d5.
G3T initial data:
Analysis/MasterTests/outputs/r4c1_g3t_attempt_02/initial_data.json,
SHA-256 c1b80b7c8cd1fd74e07fe797214a56f6c14f32f0416bb3966f6371cf4a85d243.
G3T trajectories:
Analysis/MasterTests/outputs/r4c1_g3t_attempt_02/trajectories.npy,
SHA-256 470bdd1212e45fb3334e549003a6d6233f26f396043924c2ccb9b20bf13c18cd.
Original G3 family/failed background receipt:
Analysis/MasterTests/outputs/r4c1_g3_attempt_01/summary.json,
SHA-256 930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75.

Verify every inherited G3K scientific source pin and sidecar. Retain failed
parent assertions and their declared scope. No background or mode is
reintegrated/refitted. The field key K is the assumed conditional K_Q;
the family cutoff=2 is not a certified physical EFT cutoff.

## Exact geometric tests

On the homogeneous B=0 background:
g=diag(-N^2,a_parallel^2,a_perp^2,a_perp^2),
U=(sqrt(1+w^2)/N,w/a_parallel,0,0), with a_parallel,N>0.
U_flat=-N sqrt(1+w^2) dt+a_parallel w dx.

1. Derive normalization and the exact Frobenius three-form U_flat wedge dU_flat.
2. Derive a local real potential and positive integrating factor for nonzero
   fixed-sign w(t). Check its gradient, timelike norm and future orientation.
3. Test its change under x -> x+L_x, L_x>0.
4. For ANY continuous positive mu(t,x,y,z), use the x-cycle integral at fixed
   (t,y,z) to test whether -mu U_flat can equal dT for a single-valued real T.
   The integral of a positive mu around this compact cycle is strictly positive.
   Establish the implication analytically; samples are not a proof for all mu.
5. Retain the w=0 global-clock control and the negative-tilt sign control.
   Frobenius/local integrability alone is not sufficient global exactness.
6. Do not extend a homogeneous fixed-sign theorem to spatially varying or
   sign-changing configurations without a separate argument.

L_x=1 is used only as a reference coordinate period in numerical witnesses;
the exact theorem must hold for arbitrary L_x>0 and must not select a
physical cosmic torus size.

## Comparator clock-map tests

Let C=c_psi^2>=0, d=b/K>0, v=w/sqrt(1+w^2).
For P>0, Omega=+/-sqrt(C P^2+d P^4);
inverse proper-clock covectors are omega=gamma Omega+w P,
p=gamma P+w Omega. Derive dp/dP and the condition that BOTH signed
branches preserve time/map orientation.

Derive the turning equation and solve its positive boundary without using
a fitted target. An admitted comparator band is not the coupled-domain
solution or an action-derived EFT cutoff. Treat C=0, d=0, v=0 and
v^2 C>=1 as separate controls, never by invalid limiting division.

Use all 24 initial states and 16 saved evolved jets at t=.0005,.001
from the eight archived G3T runs: 40 unique background events.
The coefficient C=6 A sqrt(Y)/K uses each event's Y=(w psi_dot/N)^2.
Check the 24 initial finite-C turning values against G3K healthy_controls.
The G3T healthy_control_P_turn belongs to its C=0 comparator; match that
separate limit and never confuse it with the finite-gradient comparator.

For every event independently bracket the unexpanded turning polynomial
from x=0, doubling the upper bound until its sign changes. Compare a
50-digit mpmath bisection root and SciPy brentq with the closed expression:
normalized discrepancy <=1e-10.
Check normalized turning residual <=1e-10 and strict interior/exterior
classification at P/P_turn=(0,.5,.9,.999,1.001,1.1,2).
Do not require or infer any coupled root is healthy.

## Independent geometric witnesses and rejection tests

For all 40 events evaluate normalization/local-clock identities with
normalized discrepancy <=1e-10. With reference L_x=1 and
mu(x)=exp(e cos(2 pi x/L_x)), e=(0,1/4,1), compare SciPy quadrature and
50-digit mpmath quadrature with the positive Bessel integral:
normalized discrepancy <=1e-10.
These witnesses supplement, not replace, the exact positive-period proof.

Reject: confusing local Frobenius with a global clock; accepting a
circle-valued clock as real time; using a universal-cover boost to remove
the quotient holonomy; importing the healthy comparator as the coupled
physical cutoff; deleting complex/growing G3K modes; dividing at k=0 or
w^2=1/5. Preserve all 120 parent events and all 14 roots per event.
Formal complex preferred covectors are not real energy/momentum pole data.

## Disposition

If the exact positive-period contradiction holds, reject only the global
U-orthogonal REAL-clock route for the stated homogeneous fixed-sign tilted
T3 backgrounds. Retain local preferred patches and the possibility of a
non-orthogonal global time subject to coupled characteristic/energy-domain
analysis. No full physical ghost, instability, no-go or cutoff follows.

Record direct/transitive G3K review/scientific debt as DEFERRED.
Tests 1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 unchanged.
No action/parameter/threshold change, manuscript/PDF edit, vault mutation,
provider dispatch, commit, push, promotion or publication.

