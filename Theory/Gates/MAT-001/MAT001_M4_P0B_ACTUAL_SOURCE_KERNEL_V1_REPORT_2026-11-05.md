# M4 P0-B: actual matter-source dressing and evolving scalar kernel

5 November 2026. First actual-parent M4 component, not full physical pole
extraction. The operator confirmed High. U5 and the generic M4 method are
reused without rerunning or replacing their original calculations.

## Result and limitations

The P0-B scalar kernel now has its actual minimally metric-coupled external
matter source, including constraint dressing, derivative-source terms and
source-contact term. Both nonzero torus modes and the actual homogeneous
scalar mode are exported separately. The full time-dependent Euler operator
and source are retained. This completes the source/kernel component.

A physical stationary pole/residue is NOT established. The expanding parent
has time-dependent coefficients and no time-translation symmetry in general.
The next response calculation must use a specified Green-function problem or
prove a controlled local/adiabatic approximation before reading a pole. No
arbitrary instantaneous eigenvalue or frozen frequency is called physical.
Full M4 remains INCOMPLETE; live Track-A V is NOT_COMPUTED. This is a P0-B
external linear-response calculation, not a new matter microphysics model or
a fully dynamical matter-fluid perturbation calculation.

## 1. Actual input and source conventions

Use the frozen P0 action, its evolving homogeneous condensate background and
uniform-phase scalar gauge. Cosmic background lapse is one; the scalar metric
perturbations are delta g00=-2 alpha, delta g0i=partial_i beta,
delta gij=2 a^2 R deltaij. Define physical q=|k|/a and
Sigma=Delta beta/a^2=-q^2 beta. This Sigma is the shift-divergence variable,
NOT the compensated R-tau density that shares the same letter elsewhere.

For conserved external probe stress on the matter-free background define

    delta_e=T_m^00, j=partial_i T_m^0i, tau=a^2 deltaij T_m^ij.

Direct variation delta S_m=(1/2) int a^3 T_m^ab delta g_ab, including
periodic spatial integration by parts, gives per real Fourier mode

    L_source/a^3=-alpha*delta_e+Sigma*j/q^2+R*tau,  q!=0.

No force-scalar vertex or freely normalized source is appended. Real modes
use the same normalized Fourier inner product as the parent quadratic form;
complex modes require conjugate pairing rather than extra source factors.

Stress conservation is essential, not a density-only static prescription:

    dot(delta_e)+3H delta_e+H tau+j=0,
    dot(j)+5H j-q^2 stress_longitudinal=0.

The latter is the divergence of the spatial conservation equation. Pressure
trace and longitudinal/anisotropic stress need not be identified. The code
independently checks the FRW covariant divergence for an inhomogeneous scalar
stress tensor. These equations restrict permissible probe histories; the
export itself does not invent a nonconserved density source.

## 2. Same-parent reduction, with source retained

Write x=(R,delta_rho), c=(alpha,Sigma), M=M_P^2, r=rho,
v=dot rho, mu=dot Theta, and q=|k|/a. The original parent blocks are

    C=[[C_J q^2-2V,2MH],[2MH,0]],
    B_v=[[6MH,-v],[-2M,0]],
    B_x=[[2M q^2,-(V_rho+r mu^2)],[0,-v]],
    K0=diag(-6M,1), D0=[[-18MH,0],[3v,0]],
    F0=[[2M q^2-18V,3(r mu^2-V_rho)],
        [3(r mu^2-V_rho),mu^2-V_rhorho-q^2]].

C_J=2M on the homogeneous P0-B background. The frozen parent code supplies
these blocks and their raw/compact comparison. This calculation reconstructs
and uses them explicitly; it does not claim a fresh full tensor action
variation. The new matter vector is h=(-delta_e,j/q^2), f=(tau,0), with
b=B_v dot x+B_x x. The full action is

    L/a^3=dot x^T K0 dot x/2+dot x^T D0 x+x^T F0 x/2
           +c^T(b+h)+c^T C c/2+x^T f.

For q!=0 and H!=0, det C=-4M^2 H^2. Elimination gives

    c=-C^-1(b+h),
    K=K0-B_v^T C^-1 B_v,
    D=D0-B_v^T C^-1 B_x,
    F=F0-B_x^T C^-1 B_x,
    s_v=-B_v^T C^-1 h, s_x=f-B_x^T C^-1 h,
    contact=-h^T C^-1 h/2.

The receipt exports every matrix and source expression. The derivative
source and contact are not discarded. A source-independent Schur reduction
followed by coupling to unreduced fields would miss them.

The background Friedmann relation 3MH^2=(v^2+r^2 mu^2)/2+V recovers the
parent nonzero-mode kinetic matrix

    K=[[(v^2+r^2 mu^2+C_J q^2)/H^2,-v/H],[-v/H,1]].

Positive kinetic weight alone does not establish a physical cutoff, gradient
health or a valid pole interpretation.

## 3. Time dependence and response prescription

Varying the FULL action measure gives the operator

    O=K d_t^2+(dot K+3HK+D-D^T)d_t+(dot D+3HD-F),
    O x=s_eff, s_eff=s_x-dot s_v-3H s_v.

The derivatives act on all background and source dependence, including
dot q=-Hq. The bare coordinate Hessian F is not the complete time-dependent
mass term. The executable derives this Euler identity independently with
arbitrary time-dependent matrix functions and the a^3 measure.

Under an invertible time-dependent field chart x=R(t)y,
s_v transforms to R^T s_v and s_x to R^T s_x+dot R^T s_v. Hence s_eff
transforms to R^T s_eff, with its derivative terms necessary for covariance.
The retarded response requires initial/boundary conditions: a Green operator
with O_t G_R(t,t')=delta(t-t')I and the corresponding jump/measure convention.
This report exports O; it does not compute G_R or claim pole residues from it.
Any approximation to local frequency poles must establish background-scale
and EFT overlap and error control. Those requirements remain open.

## 4. Actual k=0 is not the q->0 nonzero-mode inverse

At actual k=0 the periodic scalar shift has identically zero divergence.
Sigma cannot be varied as an independent homogeneous constraint multiplier.
Set it absent in the original action BEFORE reducing. Only alpha remains,
with C_h=-2V, B_vh=(6MH,-v) and
B_xh=(0,-(V_rho+r mu^2)). The scalar sources are h_h=-delta_e and f=(tau,0).
The same one-constraint formulas export K_h,D_h,F_h,s_vh,s_xh and contact.
This chart requires V!=0. At V=0 return to the original constrained system;
failure of this algebraic inverse is not itself a physical pathology.

On the background constraint,

    K_h=[[3M(v^2+r^2 mu^2)/V,-3MHv/V],
         [-3MHv/V,1+v^2/(2V)]],
    det K_h=3M r^2 mu^2/V.

It differs from K(q->0). For V>0 and finite charge this particular homogeneous
kinetic matrix is positive, but this is not a substitute for imposing the
chosen global charge/background tangent conditions. Harmonic vector shifts
and total-momentum compatibility are separate; they are not encoded by j/q^2.
The homogeneous energy-source conservation equation retains tau and j=0.

The old parent's two-constraint expression advertised at strict q=0 must
therefore be treated as a NONZERO-MODE LIMIT, not reused as the actual
homogeneous reduction without this distinction. Preserve the old artifacts;
this correction does not invalidate U5's local DOF result or prove a new ghost.
Other uses of that old strict-zero interpretation require this scoped caveat.

## 5. Verification, units and follow-through

The script derives the constraint solution with sources and the reduced
quadratic/source coefficients, tests against an independent exact rational
stationary-constraint solution, derives the time-dependent Euler identity,
checks field-chart covariance, source conservation and the separate
homogeneous reduction. It rejects dropped contact/derivative-source terms
and conflating the homogeneous mode with a nonzero-mode limit.

Mass dimensions: [R]=[alpha]=0, [delta_rho]=1, [Sigma]=[H]=[mu]=[q]=1,
[M]=2, [delta_e]=[tau]=4, [j]=5. Thus j/q^2 has dimension 3 and every
term in L/a^3 has dimension 4. The two field components have different
dimensions; no Euclidean mode normalization or equal-unit residue is assumed.

Producer: Analysis/MAT/MAT-001/PKM1_METRIC_HOST/m4_actual_source_kernel_v1.py.
Fresh receipt: Analysis/MAT/MAT-001/PKM1_METRIC_HOST/outputs/m4_actual_source_kernel_v1_20261105/receipt.json.
Source hashes and separate immutable replay accompany verification. These
are same-author controls, not external peer review. No old source is edited.

Next task: derive the appropriate physical source-to-metric response and
determine whether a controlled pole/residue limit exists, using this export.
An evolving response is not automatically a static source-pole match, and
free J/a0 inputs do not become microscopic predictions. M4 remains open until
that actual requirement is answered or a scoped obstruction is demonstrated.
No action adoption, observed-target input, new provider session, vault mutation,
publication or Git delivery. Rule-9 DEFERRED; physics_pass=false; gate_effect=NONE;
MAT-001 BLOCKED; V NOT_COMPUTED; K_Q NOT_DERIVED; UVIR-003 IN_PROGRESS.
