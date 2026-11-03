# R-tau initial weak canonical rates and momentum-tangent assembly

3 November 2026. Conditional component of the confirmed-High coupled
observable-norm bundle. R-tau unadopted; original R4C1 unchanged. Review
DEFERRED; physics_pass=false; gate_effect=NONE; G1-G6 incomplete.

## Result

The complete initial UNREDUCED canonical rate map now has quantitative
weak-space bounds using the actual prepared action coefficients. All
thirteen field rates and all thirteen momentum rates are retained, as
are the auxiliary observable and its time rate. The caller's shift
variation remains explicit. The differentiated momentum-constraint
tangent is controlled in H^-2, including field-generator drift.

The moving weighted compatibility pairing extends to an H^-2 source rate.
It therefore need not impose the earlier sufficient H^-1 rate assumption.
This resolves that assumption at the raw canonical source-assembly level,
not the complete transported free-coordinate graph. A bounded map into a
weaker space is not a stability, energy or solution-existence theorem.

Owners: [whole bundle](RES001_RTAU_COUPLED_OBSERVABLE_NORM_V1_CONTRACT_2026-11-02.md),
[initial weak graph](RES001_RTAU_WEAK_GRAPH_V1_REPORT_2026-11-03.md),
[moving range](RES001_RTAU_MOVING_RANGE_V1_REPORT_2026-11-03.md),
[full mixed action](RES001_R4C1_RTAU_MIXED_OPERATOR_V4_REPORT_2026-11-01.md)
and [canonical point kernel](RES001_R4C1_RTAU_EVOLUTION_KERNEL_V2_REPORT_2026-11-01.md).
The [V1 contract](RES001_RTAU_WEAK_CANONICAL_RATE_V1_SPEC_2026-11-03.md) and
[V2 implementation correction](RES001_RTAU_WEAK_CANONICAL_RATE_V2_SPEC_2026-11-03.md)
were frozen before their respective executions.

## Data controls and canonical rows

Use normalized periodic Bessel norms and Euclidean canonical-slot norms.
There are thirteen nonauxiliary slots: metric six, independent frame three,
u/v/r and psi. Z is reconstructed from the secondary relation and p_Z=0.
Define

    P0=||delta p_nonaux||L2, Q1=||delta q_nonaux||H1,
    F2=||delta psi||H2, U1=||delta S||H1.

Q1 also contains psi in H1; F2 supplies its stronger force-observable
control. These are sufficient input controls, not a selected physical
energy or a claim that arbitrary independent inputs satisfy the full
constraint/charge/density graph. Model coefficients retain their declared
diagnostic units; no microscopic matching value is inferred.

Write H_ij=L_yi,yj for the preserved 48-slot action Hessian. The actual
Legendre row gives, with v=delta q_t,

    M*v=delta p-L_vq*delta q-L_vd*delta q_z
                            -L_vS*delta S-L_vSz*delta S_z.

The inverse bound is inherited from the actual thirteen-rate calculation.
The auxiliary field/gradient columns of these rows and every auxiliary
velocity coupling are checked EXACTLY absent before exclusion. The
shift columns are retained. The coordinate shift has not been declared a
physical zero, nor has a physical mode been removed.

For every nonauxiliary momentum,

    delta p_i,t=delta L_qi-D_z(delta L_di).

Separate Z and Z_z from the other thirteen field/rate/gradient inputs.
For a smooth coefficient g and Z variation zeta in L2,

    g*zeta_z=D_z(g*zeta)-g_z*zeta,
    D_z(g*zeta_z)=D_z^2(g*zeta)-D_z(g_z*zeta).

These exact distribution identities give H^-1 control for a first
auxiliary-gradient term and H^-2 for its differentiated force flux.
The coefficient derivatives come from the actual exported Hessian dz
intervals; none is omitted as a frozen-coefficient approximation.

The first twelve flux rows have no Z_z column, exactly. The psi flux row
has a strictly negative nonzero coupling L_psi_z,Z_z. Consequently the
ordinary twelve momentum rates are controlled in H^-1 and the force
momentum rate in H^-2. This keeps the quartic force branch and all its
lower-order couplings. The metric Frobenius conversion uses sqrt(2).

The already verified complete auxiliary variation gives Z in L2 and
Z_t in H^-2 after composition with the new field-rate bound. No extra
derivative of a rough metric velocity is introduced by that composition.

For each row in the following table, its norm is at most the sum of the
four input controls times the listed conservative upward-rounded constants:

| Output norm | P0 | Q1 | F2 | U1 |
| --- | ---: | ---: | ---: | ---: |
| field rate L2 | 24.020615 | 60.831961 | 0 | 24.916378 |
| auxiliary Z, L2 | 0 | 0.000521956 | 1.000347 | 0 |
| auxiliary Z_t, H^-2 | 24.046822 | 64.368093 | 0 | 24.943563 |
| ordinary momentum rate H^-1 | 56.643463 | 152.293785 | 0.000263036 | 62.346102 |
| force momentum rate H^-2 | 21.446805 | 56.885657 | 0.455757013 | 23.630209 |
| full momentum-tangent rate H^-2 | 272.566186 | 705.385606 | 0.000928569 | 287.126664 |

The last row is derived below. These are bounds between different spaces;
they are not physical growth exponents, numerical errors, observational
fits or a positive Hamiltonian form.

## Full momentum-tangent time assembly

Let B(q) be the actual metric/frame generator in
Lie_xi q=q_z*xi^z+B(q)*xi_z. It is linear in q, with zero scalar rows.
Let K(p)*delta q=(delta B)^T*p. For canonical perturbations x=delta q,
pi=delta p, the spatial momentum tangent is

    delta E=D_z[B^T*pi+K(p)*x]
                         -e_z*(pi.q_z+p.x_z).

Differentiate every factor, using background field rate v_b=q_t and
perturbation rate v=x_t:

    delta E_t=D_z[B^T*pi_t+B(v_b)^T*pi+K(p_t)*x+K(p)*v]
          -e_z*(pi_t.q_z+pi.v_b,z+p_t.x_z+p.v_z).

In particular B_t, delta B_t and the background momentum rate are
retained. The background p and p_z are freshly evaluated from the same
action over the whole certified initial-root ball. The independent
Hessian spatial chain enclosures overlap those raw p_z enclosures.
Background p_t is reconstructed from the preserved affine Euler forcing
plus L_vq*v_b+L_vd*v_b,z, as in the preceding moving-range calculation,
now for all thirteen momenta. The new receipt exports these intervals
for reproducible reuse; they are not reference-background substitutions.

For ordinary pi_t in H^-1, multiplication by B and its first derivative
and then one outer derivative gives an H^-2 bound. The force pi_psi,t
does NOT enter this differentiated B flux: B's scalar rows vanish exactly.
It is still present in -e_z*pi_t.q_z. Its multiplier psi_z has an H^-2
multiplier bound from psi_z, psi_zz and psi_zzz. Thus no force H^-3 term
is concealed in the assembly.

More explicitly, use Frobenius/supremum upper bounds and write

    C_o=||B||infinity+||B_z||infinity
                       +||q_z,ordinary||infinity+||q_zz,ordinary||infinity,
    C_f=psi_z,max+sqrt(2)*psi_zz,max+psi_zzz,max,
    C_p=||B(v_b)||infinity+||v_b,z||infinity,
    C_q=||K(p_t)||infinity+||p_t||infinity,
    C_v=||K(p)||infinity+||p||infinity+||p_z||infinity.

Then

    ||delta E_t||H^-2 <= C_o*||pi_t,ordinary||H^-1
           +C_f*||pi_psi,t||H^-2+C_p*P0+C_q*Q1+C_v*||v||L2.

The last p.v_z term is treated as D_z(p.v)-p_z.v, rather than demanding
v_z in L2. For an H^-2 multiplier g the sufficient bound
||g||infinity+sqrt(2)||g_z||infinity+||g_zz||infinity follows by duality
from the periodic H2 product rule. This proves the last table row with
the actual prepared scalar derivative bounds.

This identity is also the source-assembly rule when known free fields
are separated from the trace/eliminated-momentum unknowns. However their
TIME-DEPENDENT embedding and gauge/mean partners must still be inserted
to obtain the actual free-coordinate source rate. The receipt does not
claim that this final composition has been calculated. Nor does it use
this estimate to replace the exact Ward cancellations on constrained data.

## Moving compatibility in the justified weaker rate space

The preceding report left the actual source-rate regularity open. Its
mean condition uses the smooth weight w=1/(2a), a=exp(lambda),
|lambda|,|lambda_z|,|lambda_zz|<=r=1/13000. Therefore

    ||w||H2 <=exp(r)/2*sqrt(1+2r^2+(r^2+r)^2)
             <0.500038468.

For s_t in H^-2 the pairing <s_t,w> is consequently continuous. With
the other first-jet terms already established,

    |c_t| <=0.007314224*||f_t||L2+1.168826*||f||H1
            +0.500038468*||s_t||H^-2+0.433383316*||s||H^-1.

The smaller displayed weight bound compared with the earlier sufficient
H1 bound reflects a sharper estimate, not a reduction in the norm's
derivative order. No new physical regularity condition is adopted.

A flat-coefficient regulator control explains the distinction: eliminating
Z from b*Z^2/2-b*Z_z*psi_z gives a quartic force rate proportional to
-b*D_z^4 psi. The sequence psi_n=n^-2*exp(i*n*z) has bounded H2 norm
and bounded force-rate H^-2 norm, while its rate H^-1 norm grows like n.
This is a differential-order control, not a new physical background or a
claim that the actual coupled evolution grows like n. A well-posed wave
can have an instantaneous rate in a weaker space than its state.

## Verification and preservation

[Executable V2](../../../Analysis/MasterTests/test_rtau_weak_canonical_rate_v2.py):
20/20 checks; fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_weak_canonical_rate_v2_20261103/receipt.json)
SHA256 de3869925a976f3bebb4fa7d9774c4c8e21adc7557ce528041db377252447d14.
Read-only recalculation/replay completed with byte-identical receipt bytes.
All 219 inherited source hashes and existing sidecar bytes/timestamps
were preserved. The original direct point-kernel audits were reused,
not repeated or described as a new physical result.

The preserved V1 attempt failed on an exact integer zero at an interval
endpoint reader, before returning a scientific receipt. Its
[source](../../../Analysis/MasterTests/test_rtau_weak_canonical_rate_v1.py),
specification, sidecars and
[failure](../../../Analysis/MasterTests/outputs/rtau_weak_canonical_rate_v1_20261103/failure.json)
remain unchanged. V2 changes numeric conversion at that boundary and adds
provenance pins; the equations, controls and acceptance are unchanged.

Exact weak-product and momentum time-product controls reject omitted
coefficient and generator drift. Sparse zero/nonzero checks are made
against the complete actual Hessian export. Same-author checks are not
external scientific review or full physical clearance.

## Next deciding calculation

Compose these rows with the existing periodic gauge-velocity and coupled
density/trace inverse on the compatible graph. Retain the background
coordinate drift, variation of gauge velocity, momentum-density pullback,
physical modulus rates, both charges and the physical clock flow. Then
test the actual density/gauge generator and its strong/weak domains;
do not infer a strong symplectic inverse from the order-minus-two density
block or omit G_dot/T_dot. The quartic and zero-speed/subleading sectors
must remain in the same system.

The initial unreduced weak map is now controlled, but a physical mixed
energy estimate, moving free-coordinate domain, coupled background tube,
finite-time bound and interaction window remain incomplete. No identifying
matching input or concrete P1/P2/Thermodynamics/original-R4C1 paper defect
arose. No manuscript/site claim changes are warranted. Goal ACTIVE;
original G1-G6 remain incomplete. No new action adoption, dispatch, vault
mutation, publication, commit, push or deployment.
