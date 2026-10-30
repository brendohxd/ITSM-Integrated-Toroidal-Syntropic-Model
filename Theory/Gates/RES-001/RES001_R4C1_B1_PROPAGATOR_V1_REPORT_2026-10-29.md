# Homogeneous B1: controlled full finite-mode linear propagation

29 October 2026. Conditional independent G2/G3 control. Review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result and limits

The full twenty-component linear propagator on the old, already registered
homogeneous B1 solution is now certified on t in [0,1/20] for the three
dimensionless comoving controls k=1,7,40. All ten reduced fields and their
velocities evolve together. Fast oscillations, drift, regulator and matter
effects are retained. No continually projected slow graph is used.

Every control meets the frozen 1e-8 continuous full-state accuracy requirement
after conversion to the physical kinetic-induced norm. Bounds below are
rounded outward; exact rational certificates are in the receipt.

| Comoving k | Continuous relative state-error bound | Logarithmic-norm upper bound | Growth majorant upper bound |
|---|---:|---:|---:|
| 1 | 1.213e-30 | 15.880 | 2.213 |
| 7 | 7.059e-30 | 8.940 | 1.564 |
| 40 | 7.477e-24 | 144.314 | 1360.582 |

This accepts the **specified finite-mode linear control**, not G3 as a whole.
It is not an all-frequency estimate, a nonlinear solution, an open domain
near alignment, a physical EFT window, GR recovery, or admission/replacement
of the registered vortical G1 preparation. Those distinctions remain
substantive; check counts and numerical precision do not remove them.

## Inputs, equations and domain

The [contract](RES001_R4C1_B1_PROPAGATOR_V1_CONTRACT_2026-10-29.md) was frozen
before calculation. Reuse the actual generic coefficients and background flow
of [B1_KINETIC_DRIFT_V1](RES001_R4C1_B1_KINETIC_DRIFT_V1_REPORT_2026-10-29.md),
the [explicit lapse-flux dust reconstruction](RES001_R4C1_B1_DUST_RECONSTRUCTION_V1_REPORT_2026-10-29.md),
and the existing B1 homogeneous existence theorem. No coefficient, charge,
initial background or action is selected using a target result.

For x=(q,q_dot), retain the original-action generator

$$\dot x=G(t,k)x,\qquad
G=\begin{pmatrix}0&I\\
-M^{-1}(\dot B-Q)&-M^{-1}(\dot M+B-B^\dagger)
\end{pmatrix},\qquad M=a^3M_0.$$

The actual background is evolved through its own equations, including H_dot;
neither it nor the perturbations are projected back onto a desired graph or
Friedmann root. The certified background tube, in the existing order
(a,H,u,v,r,u_dot,v_dot,r_dot,psi_dot,psi,rho), is centered on the registered
initial values and has radii

$$ (1/10,1/10,1/50,7/100,1/25,1/5,3/10,3/10,1/10,1/50,1/10). $$

All eleven strict first-exit/Picard inequalities pass. The tube is convex,
has a,H,rho>0, and bounds the true solution on this interval. In particular
1<=a<1.1. The centered degree-32 background polynomial lies in the same tube.
Its continuous infinity-norm residual is below 4.624e-32; a Lipschitz bound
below 8.280, initial rounding and Gronwall accumulation give actual background
error below 3.498e-33 throughout the interval. The background existence
theorem is reused rather than inferred from this polynomial's small residual.

The reduced algebraic block has determinant -a^6 k^6/132, so the Z and three
shift solutions remain regular for these nonzero modes. The remaining lapse
equation supplies the density and scaled dust multiplier; the original
clock continuity identity holds on the preserved background constraint.
Every nonzero Fourier pair has zero first-order spatial mean. Second-order
mean/charge backreaction, the zero mode and nonlinear harmonic generation
are outside this linear certificate.

## Continuous error proof and physical norm

The proof arithmetic uses the pinned 256-bit dyadic interval/Taylor kernel:
endpoint rounding is integer floor/ceiling outward. A constant unit-modulus
Fourier parity makes the generator real. Reality, invertibility and agreement
of the q/q_dot phases are checked exactly; both real quadratures and the
conjugate Fourier partner are retained.

Let R0^T R0=M0 be the parent's exact normalization. For fixed k use
W=diag(k,...,k,1+2k^2/5) on the ten fields and transform x, after the parity,
by diag(W R0,R0). Call the transformed generator A and state y. This is a
coordinate/norm choice, not a new state, frequency selection rule or cutoff.

On 64 dyadic tiles the full propagator is approximated by centered order-24
Taylor matrices. Each tile starts from the preceding approximate endpoint,
not from the identity. Dyadic endpoint continuation is exact; all interface
jump bounds are zero. Every tile's coefficient hash and error budget is
stored. The continuous defect includes:

- low-order coefficient rounding residuals;
- every high product-convolution tail and Taylor-model coefficient remainder;
- generator error induced by the certified background uncertainty.

For the high tail the proof uses
sum_(j+l>=24) ||A_j||_F ||Phi_l||_F, together with the coefficient-remainder
norm times sum_l ||Phi_l||_F. All 192 tiles have nonzero retained high tails.
For background forcing it uses the verified coefficient Lipschitz bound,
the background error, and the approximate full propagator norm. Omitting
these terms is not justified by agreement with another solver.

Gershgorin bounds on the explicitly symmetrized A give a logarithmic 2-norm
majorant mu. If D_j bounds the complete continuous defect on tile j and J_j
its interface jump, the accumulated Frobenius/2-norm error is bounded by

$$E_y\le e^{\mu T}\left[\sum_j hD_j+\sum_jJ_j\right].$$

The majorant exponential is itself bounded with outward-rounded rational
arithmetic. This controls the full fundamental matrix and therefore every
initial state, not only the independent numerical probes or the endpoint.

Define the full-state kinetic-induced norm by

$$\|x\|_{K,t}^2=a(t)^3\left(q^\dagger M_0q+
\dot q^\dagger M_0\dot q\right).$$

This uses the declared dimensionless control time/field units. It is an SPD
state norm induced by the kinetic matrix, **not** the full Hamiltonian energy
and not a claim that the restoring block is positive. Since 1<=a<1.1 and
(6/5)^2>(11/10)^3, the continuous error in that norm obeys

$$\|x-\widetilde x\|_{K,t}
\le (6/5)\max(W)E_y\,\|x(0)\|_{K,0}.$$

The table states this converted bound. The approximating matrix is therefore
accurate for arbitrary initial directions in this finite-dimensional linear
sector; no observational or acceleration coefficient is fitted.

## Reconstructed variables and density restriction

The certified reconstruction contains Z, all three physical shift amplitudes,
delta rho and delta E=C_background^4 delta epsilon. Their rows are evaluated
on the actual background and full state. A separate reconstruction estimate
retains both state error and background-coefficient uncertainty. Rounded-up
output bounds per unit transformed initial norm are 6.947e-29, 6.120e-30
and 3.303e-25 for k=1,7,40 respectively.

The same bounds give sufficient initial kinetic-norm amplitude limits for
|delta rho|<=rho_min/2 throughout the interval, with rho_min supplied by
the strict tube:

| k | Sufficient maximum initial norm, rounded down |
|---|---:|
| 1 | 1.3615e-4 |
| 7 | 4.2355e-5 |
| 40 | 5.6413e-7 |

This guarantees positivity of the **linearly reconstructed density** on top
of the positive background. It is not a finite-amplitude nonlinear solution
or a bound on the omitted nonlinear response. Epsilon is recovered through
the original positive conformal factor, not a new matter prescription.

## Verification and preservation

The [versioned executable](../../../Analysis/MasterTests/test_01_r4c1_b1_propagator_v1.py)
passes 62/62 checks. Its [fresh full certificate](../../../Analysis/MasterTests/outputs/r4c1_b1_propagator_v1_attempt_01/summary.json)
SHA-256 is `93c5d85618d4546b61b6a74961d04d93da35e2ad95dc20d3b57b4ce4e38dce10`.
The complete recomputing replay is byte-identical, including all local
polynomial hashes, bounds and final matrices. All twenty direct input files
and their twenty sidecars retain bytes and modification times through both
runs. The main receipt is approximately 460 kB; redundant full polynomial
dumps are avoided without removing their deterministic reconstruction.

A [separate exact-Fraction aggregation audit](../../../Analysis/MasterTests/audit_01_r4c1_b1_propagator_v1.py)
passes 49/49 and its own replay is exact. Its [receipt](../../../Analysis/MasterTests/outputs/r4c1_b1_propagator_aggregation_v1_attempt_01/summary.json)
SHA-256 is `12932a21132f4e9647413c35eee0db57a5472951c8a944d62df01dd559dfba45`.
It checks the recorded inequalities with independent rational arithmetic and
an independent exponential majorant. It does not independently regenerate
the local Taylor defects; that is the role of the main replay. Neither is
external scientific peer review or Rule-9 clearance.

A separate DOP853 integration of the same full background/generator gives
final transformed-matrix entry differences below 4.441e-15, 7.861e-14 and
2.822e-11. These are lower-precision numerical diagnostics, not proofs of the
much smaller dyadic certificate bounds. No agreement-based error bar replaces
the continuous residual/accumulation argument.

## Next substantive work and parent holds

This finite-mode linear control is complete in its registered scope. Do not
spend the next bundle on another precision or spectrum sweep. The substantive
next task is the nonlinear interaction/near-alignment validity question:
whether the original action admits a controlled domain around this linear
sector, retaining the known finite-tilt/nodal warnings and singular regulator
structure. A finite set of accurate linear modes does not answer that question.
The original vortical G1 on-shell current/domain problem remains open; this
control is not its substitute or an automatic parent-action selection.

G1-G6 INCOMPLETE; Stage 2 INCOMPLETE; Stage 3 NOT_ENTERED; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage 4A CLOSED.
Identifying matching inputs are absent and the old B1 GR/normalization holds
remain. Review DEFERRED; no action/state adoption, manuscript/PDF/site change,
vault mutation, provider dispatch, commit or push.
