# Complete initial Euler descriptor with the physical dust-density chart retained

29 October 2026, Australia/Perth. Conditional; review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE. G1-G6 INCOMPLETE.

## Result and significance

The six registered nonzero-tilt point records now have a complete UNREDUCED
initial Euler descriptor from the verified full weak action, with explicit
clock and dust-multiplier time directions. All16 field equations, the local
lapse equation and all three shift equations agree with the existing initial
flow at the frozen numerical point tolerance. No small residual is set to zero.

This bridges the existing physical-density engine to the action with an
explicit clock and multiplier. It is new implementation/input evidence, not
a replacement for the earlier initial tangency calculation or proof of G1
background admission. It does not compute the actual gauge-reduced frequency
source in the [principal compatibility map](RES001_R4C1_PRINCIPAL_SOURCE_COMPATIBILITY_V1_REPORT_2026-10-29.md).
Actual cusp projection, node transport/domain and controlled evolution remain
open. The principal and exact-band obstructions remain unchanged.

## 1. Original action fixes the density and clock conversion

The original ADM dust density on a homogeneous-clock spatial slice is

    L_dust = sqrt(h)*epsilon*(C^2*tau_dot^2/N - N*C^4)/2,
    C=exp(beta*psi).

Vary before applying the multiplier equation. Its declared future root is
tau_dot=N*C. The lapse variation and clock momentum then give

    rho=epsilon*C^4,
    Pi_tau=sqrt(h)*epsilon*C^3=sqrt(h)*rho/C,
    (partial L_dust/partial psi)_on_constraint=-N*sqrt(h)*beta*rho.

These follow from the pinned action and first-variation report; this is not
a newly chosen matter law. At the registered psi=0, C=1, N=1 initial slice,
epsilon and rho have equal VALUES. Differentiating their relation before
specializing gives, in the existing unit-lapse chart,

    epsilon_dot=rho_dot-4*beta*p*rho,
    tau_ddot=beta*p, p=psi_dot=1/20.

Here beta=1/40, hence tau_ddot=1/800. The density derivative is the parent's
independently computed Hamiltonian/lapse-flux physical-density derivative,
not a rate assigned from the clock equation being tested. The separately
varied current requires

    rho_dot=R*rho_z+(-3*H+Rprime+beta*p)*rho,

and the full action's clock Euler row agrees with that current after the
conversion. Equating epsilon_dot with rho_dot would corrupt this comparison.
No existing source, equation or sidecar was changed to obtain this result.
The earlier engine used a physical-density chart rather than an explicit
epsilon transport slot; it is not retroactively declared erroneous.

## 2. Complete action inputs and transport directions

The preceding raw export stores the original56-slot jet, complete gradient
and complete56-by56 Hessian at the two stored interior points and both sides
of both alignment nodes, at angular offset0.01. All physical cubic, metric,
frame, condensate, radion, regulator, clock, multiplier, lapse and shift
crosses remain. These are the already registered point records, not new
solutions or a state selection. No exact-node Hessian is inferred.

Its layout is q16,v16,d16,S3,Sz3,N,Nz, with
q=(h6,V3,u,v,r,psi,Z,tau,epsilon). The unused multiplier velocity and spatial
derivative density slots have zero gradient/Hessian columns. Their stored
zero representatives do NOT set the actual multiplier rate in Dt(q).

For the completed descriptor, Dt(q_epsilon) is the converted epsilon_dot;
Dt(v_tau) is beta*p. Dz(q_epsilon)=rho_z because psi_z=0 on this slice.
Use the original14 physical accelerations, mixed/spatial derivatives, local
density and shift jet. Retain original unit lapse and the existing initial
shift-time chart. The absent second multiplier derivatives multiply identically
zero density columns; no physical value is inferred for them.

With g=L_A and K=L_AA, the actual unreduced equations are

    E_i=g_qi-(K*DtA)_vi-(K*DzA)_di, i=0,...,15,
    E_N=g_N-(K*DzA)_Nz,
    E_Sj=g_Sj-(K*DzA)_Szj.

Let Dt0 remove ONLY the14 physical acceleration entries. Define

    F_i=g_qi-(K*Dt0A)_vi-(K*DzA)_di.

The complete coefficient is K[v16,v_physical14], a16-by14 map, so
E16=F16-K[v16,v_physical14]*acc14. The executable explicitly checks the
14 physical-row identity; the two additional field rows are checked directly
with the full action. The known clock acceleration and multiplier rate stay
in F. This F16 is NOT the principal-frequency forcing F(c); source/gauge/
constraint transport must still be derived before using that different map.

In particular, the exported initial auxiliary forcing is nonzero at every
one of these six points (smallest magnitude greater than3.58e-12 in reference
units). It cannot simply be labelled a homogeneous auxiliary source. This
does not prove the corresponding reduced frequency component is nonzero:
they are distinct objects, and the intervening transformation is still open.

## 3. Verification, numerical scope and retained residuals

| Item | Evidence |
|---|---|
| Raw full-action export | 72/72 controls; full Hessian symmetry and two-step agreement, original density/momenta/force split and independent real first/second directional variations |
| Raw replay | All six point files AND summary reproduced byte for byte, using one worker after the two-worker original run |
| Completed clock/density descriptor | 68/68 exact identities and complete initial-point controls; byte-exact replay |
| Largest normalized field Euler residual | Less than1.468e-52 over all16 rows at all six points |
| Largest absolute local lapse residual | Less than6.824e-59 |
| Largest absolute shift residual | Less than3.017e-59 |
| Omission rejection | Equating multiplier/physical-density rates and removing the required clock acceleration both fail; smallest normalized mismatch exceeds9.97e-4 |

The tolerance remains1e-18. Calculations use110 digits with stored65-digit
point inputs; complex steps1e-20/1e-26 and real directional controls are
retained. These observed discrepancies are point implementation checks, not
certified interval enclosures, continuum residual bounds or time errors.
Every nonzero Euler and constraint residual is stored. Same-author methods
and replay do not provide independent scientific review.

Executables under Analysis/MasterTests/:
export_01_r4c1_unreduced_jet_v1.py and test_01_r4c1_clock_density_source_v1.py.
Contracts: RES001_R4C1_UNREDUCED_JET_EXPORT_V1_CONTRACT_2026-10-29.md and
RES001_R4C1_CLOCK_DENSITY_SOURCE_V1_CONTRACT_2026-10-29.md.

| Owning receipt under Analysis/MasterTests/outputs/ | SHA256 |
|---|---|
| r4c1_unreduced_jet_v1_attempt_01/summary.json | ddc97689a189fb07c5fffe8e4a4052694f6d7bf9d67a35e26ec95c6a3b5fbde4 |
| r4c1_clock_density_source_v1_attempt_01/summary.json | 342ad03354a13a650ef73798c43066a5af9dcabe021abd4714a779a40e4ace90 |

The raw manifest pins six separate full-derivative files and has183 source
pins. The completed descriptor verifies192 source/export pins and sidecars
before and after calculation. Immutable originals, earlier failed attempts,
scientific digests and unrelated manuscript changes remain unchanged. Live
indices receive only backed-up append-only additions and current digests.

## Next actual research requirement

Transport the actual source/descriptor through the time-dependent clock,
lapse/density and spatial gauge/shift reductions, retaining inhomogeneous
constraint sources, moving bases, means and coefficient drift. Distinguish
an initial equation source from a frequency-dependent perturbation source.
Then establish nodal traces/mixed weights and evolution preservation before
applying a nonzero-tilt inverse or calling the cusp tails admissible. Neither
the six point controls nor the finite initial time jet establish existence,
uniqueness, an evolved interval or a physical window.

No new state, parent, projector, cutoff or branch selection is adopted. No
manuscript/PDF, site, publication, commit/push, provider dispatch or vault
mutation. G1-G6 INCOMPLETE; Stage2 INCOMPLETE; Stage3 NOT_ENTERED;
MAT-001 BLOCKED; K_Q NOT_DERIVED; V NOT_COMPUTED; UVIR-003 IN_PROGRESS;
Stage4A CLOSED. PROCEED_PROVISIONALLY for this original-action initial-point
descriptor; HOLD_SUBSTANTIVE for actual reduced-source/domain/time/window/
matching claims. Inherit original action/backend, charge normalization,
root/kinetic/force/cusp/jerk/node/constraint/current/Ward and principal/finite-
band review dependencies. Review DEFERRED, not cleared.
