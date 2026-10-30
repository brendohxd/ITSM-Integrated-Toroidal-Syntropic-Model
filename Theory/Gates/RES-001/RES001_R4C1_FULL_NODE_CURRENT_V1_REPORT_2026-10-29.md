# G1 full initial nodal currents: no additional jump source at this order

29 October 2026. **Conditional; Rule-9 DEFERRED; physics_pass=false;
gate_effect=NONE; G1-G6 INCOMPLETE.**

## Finding

On the unchanged registered B1-frame preparation, the original spatial
currents and their first time derivatives have matching traces at both
alignment nodes. This includes the clock current and the lapse/shift
constraint fluxes, not only the physical fourteen-field kinetic matrix.
The cusp partition has uniform bounds

    norm(Delta(Pi_z))                 <= 5.8125e-11*abs(w)^3,
    norm(Delta(Dt Pi_z))              < 493715*w^2,
    norm(Dz Delta(Dt Pi_z))           < 29701884*abs(w),
    norm(Delta(Dt local_source))      < 3379463*abs(w),
    norm(Delta(Dtt Pi_t))             < 327914042735916*abs(w),

on 0<abs(w)<=1/1000 in the original twenty-row chart and the fixed zero-free-
shift representative. The receipt retains exact outward rational constants;
the rounded upper bounds above are not accuracy or time-stability estimates.

Consequently excising a node and taking the two-sided limit adds no spatial
delta source from these current jumps in the initial Euler equations or
their once-differentiated time equations. This is an initial distributional
compatibility result. It is not a proof that a time-dependent weak solution
exists, that its initial current derivatives are attained, or that it is
unique. It does not restore the excluded unweighted L1 third-time field jet.

## Full action and bookkeeping

For Y20=(q16,S3,N), use the original 56-slot weak action and

    local_source = (L_q16,L_S3,L_N),
    Pi_t = (L_v16,0,0,0,0),
    Pi_z = (L_d16,L_Sz3,L_Nz),
    E20 = local_source - Dt Pi_t - Dz Pi_z.

All metric/frame/phase/radion/scalar/auxiliary, clock/multiplier, lapse and
shift sectors remain. Delta is the fixed-initial-fields physical-minus-
analytic-cubic partition. Its local density is adjusted by the original
lapse equation; the analytic summand is not adopted as a different physical
background or a mean-charge solution.

The exact rational complex-disk majorant now covers the full analytic
PHYSICAL density with variable lapse, lapse gradient and spatial curvature.
Only the cubic summand and separately calculated dust are removed for this
bound, with exact original-code AST guards. The conformal factor is used
only in the removed dust expression; no other coupling is changed. All
222 inverse and five square-root domains remain safe. The absolute bound
is below 64 on complex radius delta=1/1000 polydiscs containing every
registered initial physical jet. Hence

    H2=2*64/delta^2=128000000,
    H3=6*64/delta^3=384000000000.

The earlier fixed-lapse majorant is not reused for lapse derivatives. Dust
is handled by its exact original constraint and currents, including
rho=epsilon*C^4, epsilon_t=rho_t-4*beta*p*rho, and tau_tt=beta*p.

## Uniform flux and drift calculation

Let r=1/1000. The inherited exact cusp accelerations obey

    abs(Delta(a_y))<=Ma*abs(w)^2,
    abs(Delta(a_y,z))<=Md*abs(w),
    abs(Delta(aZ))<=Mz*abs(w), abs(Delta(aZ,z))<=Mzz.

There are twelve complement fields; Delta(aPsi)=0. The only physical
spatial-current Hessian coefficient multiplying aZ is

    L_dpsi,vZ = b*w^3*T, T=R/w.

All clock/shift/lapse flux entries in that column vanish. This column and
the temporal-current column are independently checked against all six
original full 56-slot Hessian exports. Thus

    norm(Delta(Dt Pi_z)_analytic)
      <= 12*H2*Ma*w^2 + b*Tmax*Mz*abs(w)^4.

For its normal derivative, retain the spatial coefficient drift and the
bounded aZ,z term. The analytic density is quadratic in first derivatives,
so mixed derivative-slot Hessian coefficients depend on q,S,N. Their
initial spatial l1 drift is below 20; B1's transverse shift obeys the
explicit coarse rational envelope checked in the executable. The resulting
analytic bound is

    240*H3*Ma*w^2 + 12*H2*Md*abs(w)
      +b*(3*wpmax*Tmax*Mz+r*Tzmax*Mz+Tmax*Mzz)*abs(w)^3.

The physical cubic flux is varied before initial restriction. On the slice,

    Pi_z,cubic = 3*A*p^2*T*w^3*abs(w),
    Dt Pi_z,cubic = 3*A*T*w^3*abs(w)*F,
    F=p^2*(6*H-3*HB)+2*p*aPsi.

Its normal derivative retains T_z, wprime and aPsi_z; it is O(abs(w)^3)
uniformly. Both orientations are checked by exact symbolic identities.

The dust terms have an independent exact check. Put D=2*A*p^3,
J=3*T*wprime+Rprime and
J_z=3*T_z*wprime-4800*T*w+Rsecond. Then

    Delta(Pi_tau,t)=D*abs(w)^3,
    Delta(Dt Pi_tau,t)=D*abs(w)^3*J,
    Delta(Dt Pi_tau,z)=-D*T*w*abs(w)^3*J,
    Delta(Dtt Pi_tau,t)=D*abs(w)^3*(J^2+w*T*J_z).

The last identity solves the genuinely free multiplier second-time jet by
the varied clock equation. Independently differentiating the original
action with the stored actual time jets agrees at both finite-difference
steps; the largest relative partition discrepancy is below 1.34e-26. No
multiplier/density rate is equated incorrectly and volume drift is retained.

For temporal current second derivatives, retain M*Delta(j14), all coefficient
drift, Delta(a_y,z), and the mixed Z-gradient coefficient b*w^3*T. The
effective time-direction l1 bound is below 4000 in each analytic/physical
partition. The analytic third-derivative contribution is bounded by
8000*H3*(12*Ma*r+Mz)*abs(w). The cubic temporal second derivative is fixed by
the already exported full cubic scalar source and the above normal flux
derivative, both O(abs(w)^3); it is not approximated by a generic smooth
third derivative of abs(w)^3 at the node. Dust uses the clock identity above.
These contributions give the displayed finite temporal-current bound even
though the unweighted auxiliary third-time jet is not L1.

## Kernel and limits of the conclusion

In ALL20 once-differentiated Euler rows, a change in the isolated auxiliary
third-time jet enters only through -b*w^2 in the scalar row. The other
terms involve already fixed accelerations and spatial/time drift; they do
not supply a new coefficient multiplying that third-time trace. The clock,
shift and lapse rows therefore do not remove the formal delta/delta_prime
kernel at this order. Both temporal and spatial current columns also kill
these distributions. This calculation goes beyond the earlier isolated
fourteen-field mass test, but is still an initial-jet statement.

It does NOT establish an arbitrary distributional freedom in a real
time-dependent solution. Higher compatibility, kinematic trace attainability,
global constraints/charges/means and a specified function space may remove
or forbid such extensions. No finite part, smoothing, nodal boundary law,
singular gauge, new state, cutoff or action is chosen here.

## Evidence and next target

Contract: [full node current V1](RES001_R4C1_FULL_NODE_CURRENT_V1_CONTRACT_2026-10-29.md).
Executable: Analysis/MasterTests/test_01_r4c1_full_node_current_v1.py.
Receipt: Analysis/MasterTests/outputs/r4c1_full_node_current_v1_attempt_01/summary.json.
SHA256: 20903f24484d1b0fec37e00b036182404638edd68984a84bef33c1692ae64a92.
71/71 checks, no failed/unknown rows; 239 source pins; READ_ONLY_REPLAY_EXACT.
Twelve complete physical/analytic current exports reuse six original
profiles and preserve all nonzero initial residuals. Uniform conclusions
come from the bounds, not from fitting their traces.

Next address actual near-node time transport, rather than repeating initial
current identities. Determine necessary coupled space-time scaling and
whether the original constraints permit a time-compatible weak continuation
with controlled remainder. Do not mistake a formal inner expansion or the
absence of an initial jump source for an admitted background. G1-G6,
physical normalization/window and identifying matching remain incomplete.
