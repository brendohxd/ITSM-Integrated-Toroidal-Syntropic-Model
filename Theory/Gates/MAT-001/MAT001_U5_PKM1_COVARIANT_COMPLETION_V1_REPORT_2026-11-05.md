# U5: covariant presymplectic current and regular-P0-B rank comparison

5 November 2026. Conditional analytic result on the frozen PKM1-P0 action.
This report gives the argument; executable algebra controls corroborate it.
No finite matrix rank check alone establishes the continuum DOF count.

## 1. Precisely scoped result

On a smooth timelike phase foliation, rho>0, Z=-(dTheta)^2>0, and a compact
spatial slice with a regular positive metric, the P0-B lapse Hessian is strictly
negative and elliptic. With bounded coefficients and positive lower bounds
on lapse and amplitude, its inverse exists, including the homogeneous mode.
The pulled-back covariant presymplectic form agrees with the ADM canonical
form modulo boundary improvements. The resulting local reduced rank is eight:
four gravitational/condensate DOF, separately from ordinary matter fields.

This establishes the recovered U5 comparison on this domain. It does not
establish nonlinear evolution, a physical EFT/locality window, microscopic
J/a0 matching, or extension through amplitude zeros or non-timelike phase.
The result is not a canonical adoption of PKM1 and does not complete A0-A6.

## 2. Covariant variation

Signature (-,+,+,+); h_ab=delta g_ab; indices on h are raised with background
g, not interpreted as delta g^ab. Let W=sqrt(Z), U_a=-Theta_a/W,
P_a^b=delta_a^b+U_a U^b, and M=M_P^2. Then

    delta W=W U^a U^b h_ab/2+U^a nabla_a deltaTheta,
    delta U_a=-P_a^b nabla_b deltaTheta/W-U_a U^b U^c h_bc/2,
    delta a_a=delta U^b nabla_b U_a+U^b nabla_b delta U_a
                 -U^b deltaGamma^c_ba U_c,
    delta Y=-h^ab a_a a_b+2a^a delta a_a.

Here delta U^a=g^ab delta U_b-h^ab U_b. Define

    T^ba=-2 M J_Y U^b a^a,
    B^a=-2 M J_Y a^c nabla^a U_c-nabla_b T^ba.

The connection part of delta(-M J) is

    M J_Y a^a U^b U^c (nabla_b h_ca+nabla_a h_cb-nabla_c h_ba).

Its first and third terms cancel by relabeling indices. Integrating the
remaining metric derivative and then the phase derivative gives the force
presymplectic potential (vector, before multiplication by sqrt(-g))

    theta_J^b=T^ba delta U_a-B^a P_a^b deltaTheta/W
                         +M J_Y a^b U^a U^c h_ac.

The complete potential is

    theta^b = M/2 (nabla_a h^ba-nabla^b h)
              -nabla^b rho delta rho-rho^2 nabla^b Theta deltaTheta
              +theta_J^b+theta_m^b.

For commuting variations the presymplectic current is explicitly defined by

    omega^b(delta1,delta2)=delta1[sqrt(-g) theta^b(delta2)]
                          -delta2[sqrt(-g) theta^b(delta1)].

This includes variation of the volume, projector, W, connection and B; none
is held fixed in taking omega. It is a local differential expression in the
specified fields/variations, not a numerical positive norm assumption.

For completeness the force metric Euler coefficient multiplying h_ab is

    E_J^ab=M[J_Y a^a a^b-J g^ab/2
        +2 J_Y U^(a a^c nabla^(b) U_c
        -nabla_c(J_Y a^c U^a U^b)]
        -(B^c U_c)U^a U^b/2.

Parentheses symmetrize the two free indices in the third term. The equations
are E_g^ab=-M G^ab/2+T_cond^ab/2+E_J^ab+T_m^ab/2=0,
E_rho=Box rho-rho*(nabla Theta)^2-V_rho=0, and

    E_Theta=nabla_b[rho^2 nabla^b Theta+B^a P_a^b/W]=0,

with matter equations from the declared S_m. Diffeomorphism invariance gives
2 nabla_a E_g^ab=E_rho nabla^b rho+E_Theta nabla^b Theta plus matter terms.
Consequently phase evolution is not discarded by uniform-phase gauge:
where W>0 it follows from the retained metric, amplitude and matter equations.
On solutions and linearized solutions div(omega)=0 by the antisymmetrized
first-variation identity. It is not asserted off shell.

Adding a spacetime divergence to the Lagrangian changes theta by a field-space
exact improvement; adding an exact spacetime current changes surface terms.
Keep these ambiguities explicit. They do not change the compact-slice local
rank with fixed admissible boundary data.

Dimensions in mass powers: [rho]=[W]=[a]=1, [Theta]=[U]=0, [J]=2,
[J_Y]=0, [T]=3, [B]=4, [theta]=[omega]=3. Euler coefficients have dimensions
4 (metric/phase) and 3 (amplitude). No numerical physical scale is derived.

## 3. Pullback and constraints, not assumed constraint counts

On an admissible uniform-phase chart Theta=mu_Theta t, mu_Theta nonzero,
U is the unit normal and Y=|D ln N|^2. For tangents preserving this gauge,
deltaTheta=0 and delta U_a is parallel to U_a. Since a.U=0, the normal
component of theta_J vanishes identically. Its variation also vanishes
within this gauge family. The canonical phase surface term vanishes as well.
The Einstein-Hilbert boundary improvement yields the ADM surface potential

    integral_Sigma (pi^ij delta h_ij+p_rho delta rho),
    pi^ij=(M/2)sqrt(h)(K^ij-h^ij K),
    p_rho=sqrt(h)(rho_dot-N^i D_i rho)/N.

The DeWitt map on all six metric velocities is invertible and the amplitude
velocity has nonzero coefficient. J supplies only spatial lapse derivatives,
not lapse or shift velocities. Thus the primary constraints are exactly p_N
and the three p_i on this chart, with no additional primary metric/rho ones.
Shift preservation gives spatial momentum constraints. The canonical spatial
generator acts by Lie derivatives on h, pi, rho, p_rho and lapse; its brackets
close as the Lie algebra of spatial vector fields and transform the lapse
constraint covariantly. This derives the three spatial gauge directions and
their three primary partners rather than assuming eight covariant constraints.

Lapse preservation gives C_N=delta H/delta N. Invertibility of its derivative
fixes lapse consistency and its multiplier: p_N,C_N form a second-class pair,
and no additional lapse consistency constraint arises on the stated domain.
The reduced symplectic form before spatial reduction has seven canonical
pairs. Imposing the three independent spatial constraints and quotienting
their gauge directions leaves rank 14-6=8, hence four local physical DOF.
Equivalently the unitary Dirac count is (22-12-2)/2=4 AFTER this derivation.
Admissible gauge fixing and the Noether identity identify the covariant
quotient with this form; the arithmetic is not the proof of equivalence.

## 4. The FULL lapse Hessian, including zero mode

At fixed h, pi, rho and p_rho, the lapse-dependent Hamiltonian is

    H_N=int sqrt(h)[M N J(|D ln N|^2)-rho^2 mu_Theta^2/(2N)]

plus a term linear in N, which has zero second variation. Put delta N=N f,
a_i=D_i ln N. Direct differentiation, without imposing the lapse equation,
gives

    delta^2 H_N=int N sqrt(h){2M[J_Y |Df|^2+2J_YY(a.Df)^2]
                               -rho^2 mu_Theta^2 f^2/N^2}.

The terms proportional to f*a.Df cancel exactly. For P0-B,
J_Y=-1/(1+y), J_Y+2Y J_YY=-1/(1+y)^2, y=sqrt(Y)/a0.
Thus -delta^2 H_N is the sum of positive transverse/radial gradient forms
and a strictly positive mass form. For finite y<=y_max, N<=N_max and
rho>=rho_min>0 it bounds below

    int N sqrt(h)[2M/(1+y_max)^2 |Df|^2
                  +rho_min^2 mu_Theta^2/N_max^2 f^2].

These two coefficients retain their different dimensions; no dimensionally
inconsistent sum norm is used. Uniform positive metric/lapse bounds on a
compact slice make this a coercive H1 form. The weak H1->H^-1 inverse follows
from coercivity; smooth-patch elliptic regularity supplies the usual stronger
mapping where coefficients permit it. This is a conditional inverse at an
admitted solution, not proof that every prescribed background solves C_N.

For homogeneous N=1, flat spatial metric and finite charge, the symbol is

    C_N'[n]=-sqrt(h)(2M k_phys^2+rho^2 mu_Theta^2)n.

It is nonzero for every torus harmonic, including k=0. Removing finite charge
would change that zero-mode conclusion and is not permitted. This establishes
more than the old isolated homogeneous bracket coefficient.

## 5. On-shell background, regularity and global limits

The existing evolving FRW branch, not stationary finite-density Minkowski,
supplies the comparison background. On the homogeneous solution J(0)=0 and
a=0, so its background equations are the original Einstein/complex-scalar
equations with conserved scalar charge. The preserved background calculation
is reused; no new numerical trajectory or observational fit is claimed here.
The rank result applies to on-shell local solutions with the stated bounds,
not arbitrary prescribed off-shell fields or every stationary gradient patch.

J_B as a function of the acceleration vector is C2 but not C3 at a=0:
J_B=-|a|^2+2|a|^3/(3a0)+..., with finite continuous quadratic Hessian.
The singular scalar J_YY alone is not a rank pathology: J_YY*a_i*a_j tends
to zero. The homogeneous linearized current/form and lapse operator are
therefore well defined. This does NOT justify cubic regularity, arbitrary
derivative commutation at nodes, or nonlinear well-posedness across a=0.
Use smooth Y>0 patches for higher pointwise derivatives and a separately
defined quadratic/weak limit for the homogeneous comparison.

Compact T3 slices have no spatial boundary flux. Retain harmonic and charge
partners in the integrated current and do not call global U(1) a local gauge
degeneracy. Four LOCAL DOF does not specify the finite-dimensional global
phase space. Winding charts, core boundaries, rho=0, Z<=0, absent charge and
noncompact boundary data are separate domains; no rank claim crosses them.
Ordinary matter contributes its own constraints/DOF when specified and is
not included silently in this four-mode gravitational/condensate count.

## 6. Disposition and reproduction

U5 regular-chart comparison: COMPLETE_SCOPED, subject to deferred independent
review. No ADM/covariant local-rank discrepancy is established in this domain.
This removes no physical locality, matching, higher-order cutoff or global
completion holds. The earlier engineered auxiliary-s action is not this parent.

Executable: Analysis/MAT/MAT-001/PKM1_METRIC_HOST/u5_covariant_comparison_v1.py.
Fresh receipt: Analysis/MAT/MAT-001/PKM1_METRIC_HOST/outputs/u5_covariant_v1_20261105/receipt.json.
Its exact controls test normalized-normal variation, connection terms, phase
IBP, the full lapse Hessian, homogeneous zero-mode, DeWitt invertibility,
regularity limits and reduced canonical rank. The argument above, not a count
of passing checks, supplies the continuum comparison. Replay is recorded
separately after execution; no script or old receipt is overwritten.

Next supported recovered task: establish the actual same-action M4 source/kernel
inputs before attempting a physical residue. U7's old split-rank diagnostic
trigger is not established by this regular-domain result; other physical
obstructions remain separate. No new action, provider dispatch, gate closure,
vault mutation, publication, commit or push. physics_pass=false; review DEFERRED.
