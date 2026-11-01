# R-tau frozen candidate: continuum residual and density enclosures

31 October 2026. Claim Conditional; review DEFERRED.
physics_pass=false; gate_effect=NONE. R-tau remains unadopted.

## Outcome and actual remaining wall

The frozen numerical periodic candidate now has outward interval/Taylor
enclosures over the ENTIRE spatial circle, including its full shift Euler
residual, positive density and both global charge defects. This replaces
sampled-grid evidence for those bounded quantities; it does not turn the
approximate candidate into an exact solution.

The missing part of the [periodic-preparation acceptance](RES001_R4C1_RTAU_PERIODIC_PREPARATION_V1_CONTRACT_2026-10-31.md)
is a quantitative nonlinear inverse/domain and existence certificate with
actual global momentum/charge compatibility. Residual bounds alone cannot
establish existence. No full nonlinear initial-data admission, evolution,
reduced interactions or physical window is claimed here.

## Frozen inputs and equivalent force evaluation

The exact binary floating values of the stored 33-node candidate are reused:
H=0.8665251363152258, omega=0.9999999097130079 and all stored shift
coefficients. No refitting, altered packet, coefficient match or action change.
All prescribed metric/frame/condensate/reservoir/force profiles and their
spatial derivatives remain those of the numerical specification.

Follow the [interval contract](RES001_R4C1_RTAU_INTERVAL_RESIDUAL_V1_CONTRACT_2026-10-31.md).
The implementation uses 40-digit outward mpmath interval operations and
fourth-order spatial Taylor jets underneath reverse action differentiation.
Rational control parameters are enclosed from their exact ratios. Stored
candidate floating numbers are treated as their exact binary values.
Exact binary interval endpoint tuples are retained in the receipt; decimal
displays below are rounded conservatively for readability.

On this conformal packet only, evaluate the original force norm as the
equivalent sum of squares of its boosted rest-space gradient:

    Y=|G+V*(psi_normal+(V.dot(G))/(gamma+1))|^2,
    gamma=sqrt(1+|V|^2), G=(0,0,psi_z/exp(lambda)).

This avoids subtracting nearly equal temporal terms. The K_Q term and every
other action sector are unchanged. Full density AND independent lapse/shift/
velocity gradients are compared against the original implementation at real
points. No alternative action is introduced by this algebraic identity.

The transverse component has a strictly positive analytic lower bound on
the frozen circle. In particular Vx>=epsilon/(2*37),
|Vz|<=epsilon/43, |psi_z|<=epsilon*(1/29+2/31),
|lambda|<=epsilon/13 and |psi|<=epsilon*(1/29+1/31).
Bound the actual longitudinal shift by the sum of the absolute stored
Fourier coefficients. With p_min=1/5-epsilon/47 and N_max=exp(beta*|psi|_max),

    q_rest,x >= epsilon/(2*37) * [
       (p_min-S_bound*|psi_z|_max)/N_max
       -(epsilon/43)*exp(epsilon/13)*|psi_z|_max/2 ]
       > 2.702e-6.

Thus the spatial force norm does not cross its zero branch on this fixed
prepared circle. This justifies the spatial differentiability used here;
it does NOT erase the general norm-cubed force's nonanalytic amplitude
behaviour at the aligned background or prove a whole nearby solution domain.

## Whole-circle Taylor enclosure, with spatial flux retained

Let G_a=L_Sa and F_a=L_Saz after independent local action differentiation.
The full continuum constraint is E_a=G_a-d_z(F_a). If the spatial jet
coefficient is the derivative divided by its factorial, then

    (E_a)_n=(G_a)_n-(n+1)*(F_a)_(n+1), n=0,1,2,3.

Four action-gradient jet orders are needed for the third derivative of the
Euler residual. This calculation does not differentiate a sampled array or
reuse a double-precision spectral derivative matrix.

Partition the circle into equal cells with exact centers and half-width
h=pi/cell_count. Evaluate the center coefficients through order two and
the third coefficient over the WHOLE cell. Taylor's theorem gives

    sup_cell |E_a| <= sum_(n=0..2) |(E_a)_n(center)|*h^n
                     +sup_cell |(E_a)_3|*h^3.

Every interval operation is retained. All 388 exported cell residual,
density and charge interval pairs were additionally checked to be finite
and ordered; each cell residual upper endpoint lies within its reported
global maximum. This check prevents a nonfinite endpoint from being hidden
by a min/max accumulator.

The same full lapse Euler flux gives rho=(L_N-d_z(L_Nz))/sqrt(h).
For the normalized clock integral, exact periodic integration by parts gives

    I_clock=average((L_N-beta*psi_z*L_Nz)/C).

The U(1) integral is average(u*pi_v-v*pi_u). Center Taylor quadrature
includes its quadratic term and a third-derivative interval remainder;
the odd linear term integrates to zero within each symmetric cell.
No flux, mean, clock exchange or physical field sector is omitted.

## Results in the declared control units

| Cells | sup abs(E_Sx) | sup abs(E_Sy) | sup abs(E_Sz) | Density lower bound |
|---|---|---|---|---|
| 32 | <2.926e-11 | <3.157e-9 | <4.370e-6 | >0.19004 |
| 64 | <1.839e-12 | <2.012e-10 | <2.755e-7 | >0.19265 |

The column labels refer to absolute component bounds; these are not physical
observational units or a new EFT cutoff. The density lower bound applies to
the entire frozen approximate candidate, rather than just sampled nodes.

For 64 cells the global charge defect bounds are

    |I_clock-1/5| < 2.070e-7,
    |Q_U1-1| < 1.157e-9.

These enclosures are much looser than the earlier sampled ~1e-14 charge
errors. That is conservatism in the enclosure, not evidence the frozen
candidate was altered or its numerical fit degraded. Likewise the interval
shift bound is an upper bound, not a measurement of a 1e-7 physical defect.

This is a continuum C0 residual bound, including contributions from all
harmonics of the actual profiles. It is NOT a separately proved Fourier
l1 tail norm. The next inverse argument must use the stated function-space
bound or supply another norm estimate; it cannot silently substitute one.

## Verification, implementation failures and next task

[Executable V3](../../../Analysis/MasterTests/test_01_r4c1_rtau_interval_residual_v3.py),
[spatial interval helper V3](../../../Analysis/MasterTests/r4c1_interval_spatial_jet_v3.py),
[receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_interval_residual_v3_attempt_01/summary.json):
39/39, no failures/unknowns; exact recomputing read-only replay.
SHA256 d116cbb8c71241c4e3c85c1b260f082f5e30306dbf51243d26e446e36e797484.

Controls include elementary derivative identities through fourth order,
original physical-density and gradient containment, and a zero-crossing
square test. Source and sidecar bytes/mtimes remain unchanged. This is
same-author provisional computer-assisted evidence, not independent peer
review or formal verification of the interval software implementation.

V1's mixed arithmetic-dispatch error and V2's unnecessarily negative square
enclosure are preserved with their sealed sources and private logs. Neither
produced a scientific receipt. The [V3 implementation addendum](RES001_R4C1_RTAU_INTERVAL_RESIDUAL_V3_ADDENDUM_2026-10-31.md)
records valid arithmetic repairs with unchanged action, packet and precision.

Next execute the [quantitative inverse contract](RES001_R4C1_RTAU_PERIODIC_INVERSE_V1_CONTRACT_2026-10-31.md):
actual derivative/domain bound, mean-mode compatibility, defect/contraction
inequalities and positive density throughout the candidate correction ball.
Its proposed constants and radius are NOT yet validated. Do not repeat root
fitting or call the existence certificate complete from this residual bound.

Original G1-G6 incomplete; identifying matching remains absent. No parent
adoption, manuscript/site change, publication, provider dispatch, vault mutation
or commit/push. Native goal ACTIVE; High last confirmed.
