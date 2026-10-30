# G1 weighted node diagnostic: the pole does not by itself reject weak evolution

29 October 2026. **Conditional; Rule-9 DEFERRED; physics_pass=false;
gate_effect=NONE. G1-G6 INCOMPLETE.**

## Result

The [uniform auxiliary pole proof](RES001_R4C1_AUXILIARY_POLE_V2_REPORT_2026-10-29.md)
excludes the stated locally integrable third-time field-jet class. A separate
calculation now checks how the ORIGINAL action weights that derivative. It
does not choose a new weighting or weaken the earlier proof.

In the fourteen-field chart (twelve complement fields, psi, Z), its time-mass
matrix on the registered initial slice is

    M = [ B       C       0     ]
        [ C^T     d      -b*w^2 ]
        [ 0      -b*w^2   0     ],
    d=K_Q*(1+w^2)-6*A*p*abs(w)^3,
    C_hyy=-b*Z*w^2, C_Vy=-b*Z*w, all other C entries zero.

Thus M*e_Z=-b*w^2*e_psi exactly. The isolated singular contribution has image

    M*(Delta(jZ)*e_Z)= -b*(297/2800000)*abs(w)*e_psi + O(abs(w)^3).

It tends to zero at the node, even though Delta(jZ) itself is not locally
integrable. This is the action's kinetic degeneracy, not a regularization
introduced to hide a divergent field derivative. All fourteen-by-fourteen
matrix entries agree with six independent original 56-slot Hessian exports;
the largest normalized discrepancy is below 2.31e-66.

## Uniform bound for the full coupled time-mass image

Retain all twelve complement third-time jets, not just the singular column.
Using the sealed pole remainder and exact inherited envelopes, let r=1/1000,
JF bound abs(Delta(jPsi))/abs(w), Mj bound each abs(Delta(j_y))/abs(w),
CF bound sum(abs(C_i))/w^2, C0=297/2800000, and B the pole remainder.
The outward interval maximum row-sum norm of B is at most 1 on [-r,r].
With D=K_Q*(1+r^2)+6*A*p*r^3, the row bounds are

    complement: (Mj + CF*JF*r^2)*abs(w),
    scalar:     (CF*Mj*r^2 + D*JF + b*C0 + B*r^2)*abs(w),
    auxiliary:  b*JF*r^2*abs(w).

The receipt retains all three exact rational constants. Their maximum L is
less than 246806944172267. Therefore

    norm_infinity(M_physical*Delta(j14)) <= L*abs(w).

This is a uniform initial-slice integrability/zero-trace result for the full
coupled time-mass image in the fixed zero-free-shift representative. The
large conservative L is not an accuracy estimate or stability constant for
future evolution. It supplies no time interval or physical frequency window.

In particular M*j is only one term in partial_t^2 Pi: coefficient drift,
lower-order currents and constraints still have to be included. This report
does not identify the displayed bound with a completed canonical momentum
transport calculation or with physical symplectic normalization.

## Isolated distribution kernel and its limits

Use w as a smooth local normal coordinate; abs(wprime)=2/25 at either node.
Multiplication of normal distributions gives

    w^2*delta(w)=0,
    w^2*delta_prime(w)=0,
    w^2*delta_second(w)=2*delta(w).

The executable verifies these identities and the next derivative by their
actions on arbitrary smooth test-function jets. Hence the isolated time-mass
column cannot distinguish a formal Z-jerk extension differing by node-supported
delta or delta_prime terms. The nonzero delta_second result is a rejection
control: this is a specific finite kernel, not arbitrary invisibility of all
singularities. No finite-part extension of 1/abs(w), delta coefficient or
junction law is selected.

This does NOT prove nonuniqueness of physical evolution. Such a time-slice
distribution may be incompatible with a genuine time-dependent field, the
full differentiated constraints, canonical currents or inherited regularity.
The kernel of the entire constraint/current system has not been calculated.
It does explain why simply dividing by w^2 and demanding an unweighted L1
third-time field jet is stronger than the isolated original weak equation.

## Evidence and next calculation

Contract: [weighted node V1](RES001_R4C1_WEIGHTED_NODE_V1_CONTRACT_2026-10-29.md).
Executable: Analysis/MasterTests/test_01_r4c1_weighted_node_v1.py.
Receipt: Analysis/MasterTests/outputs/r4c1_weighted_node_v1_attempt_01/summary.json.
SHA256: bfc845002c91896139f2b9bbe1eb4cd6b138db755134e00e1287ce6a034b34e3.
17/17 checks, no failed/unknown rows, 235 source pins; READ_ONLY_REPLAY_EXACT.

Next retain the full initial first-order canonical currents, coefficient drift,
clock/lapse/shift constraints and both nodal traces. Determine which, if any,
formal node-supported directions the original full system removes, and what
existence/selection data remain missing before a time-compatible continuation
can be claimed. A finite set of initial trace identities still cannot establish
short-time persistence. Do not silently add a weak junction prescription or
adopt a new parent/state/cutoff to pass the gate.

Both results stand together: the unweighted regularity class fails, while the
weighted kinetic image is locally integrable. Weak continuation remains OPEN;
it is neither admitted nor excluded by this diagnostic. G1 background admission,
G2 physical reduction, G3 evolution, G4 window, and G5-G6 matching/prediction
remain incomplete. Review-only debt permits scoped provisional reuse, not
publication or canonical promotion. No paper, PDF, site, commit or push changes.
