# Prepared R-tau constrained principal calculation

1 November 2026. Conditional action-comparison result; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau unadopted; G1-G6 incomplete.

## Result and deciding limitation

The actual prepared-data planar nonzero-covector principal problem now has
a controlled shift reduction. Its ten-variable kinetic form is positive on
the full certified initial-root ball, with coordinate-velocity lower bound
greater than 0.11315132. The auxiliary/force sector supplies a positive
quartic branch; its k-cubed coupling to the other fields is retained.

The fresh rest-control ordinary polynomial is resolved, and all three
prepared-centre pencils agree with the tilted-frame cone comparison below
to better than 2.54e-50, against the frozen 1e-28 tolerance. These numerical
comparisons are NOT a whole-root determinant theorem. The zero-speed
reference branch has a Jordan partner, and the reference principal
gradient energy is indefinite. Consequently positive kinetics and real
reference characteristic speeds do not establish a physical evolution
estimate, strong hyperbolicity or a validity window.

The [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md)
still owns physical admission. Inputs are the [mixed operator](RES001_R4C1_RTAU_MIXED_OPERATOR_V4_REPORT_2026-11-01.md),
[velocity tangent](RES001_R4C1_RTAU_VELOCITY_TANGENT_V2_REPORT_2026-10-31.md),
[compatible gauge](RES001_R4C1_RTAU_SPATIAL_GAUGE_V1_REPORT_2026-10-31.md)
and [initial clock identity](RES001_R4C1_RTAU_CLOCK_IDENTITY_V2_REPORT_2026-11-01.md).
The [principal contract](RES001_R4C1_RTAU_PREPARED_PRINCIPAL_V1_CONTRACT_2026-11-01.md)
was frozen before execution. The unchanged original R4C1 action is not
repaired or promoted by this unadopted R-tau comparison.

## Actual action blocks and shift reduction

Start with the full clock-substituted 48-slot Hessian, including all six
metric fields, independent frame, u/v/r/psi/Z and shift/shift-gradient slots.
For a nonzero planar covector, the compatible spatial gauge has principal
condition delta h_xz=delta h_yz=delta h_zz=0. This fixes three coordinate
directions at principal order. It does not remove their homogeneous torus
moduli, enforce a future conformal ansatz or complete the lower-order gauge.

The remaining dynamic slots are

    q=(hxx,hxy,hyy,Vx,Vy,Vz,u,v,r,psi).

Use w=delta S_z and d=partial_z delta q. From the actual density define

    K=L_ww, C=L_vw, D=L_dw,
    M=L_vv-C*K^-1*C^T,
    B=L_vd-C*K^-1*D^T,
    G=L_dd-D*K^-1*D^T.

The principal shift equation is w=-K^-1*(C^T*v+D^T*d). K is indefinite,
not a physical kinetic form. Its rest value diag(1/2,1/2,-1/15) is
nonsingular. The full-root bound ||K0^-1*(K-K0)||_infinity<0.068612
establishes a Neumann inverse; its explicit remainder is included. The
principal lapse has already been reconstructed on the declared clock branch.
No new physical condition Sdot=0 is introduced.

The reduced quadratic density and frozen Euler pencil are

    L2=1/2*v^T*M*v+v^T*B*d+1/2*d^T*G*d,
    P(omega,k)=omega^2*M-omega*k*(B+B^T)+k^2*G,

before auxiliary elimination and its higher spatial orders. Spatially
varying coefficients, basis drift and lower-order Euler terms belong to
the remaining full evolution problem; they have not been set to zero in
the original mixed operator or claimed negligible in a time estimate.

## Whole-root kinetic bound, with its normalization

The exact reference M0 has metric eigenvalues 33/4,1/2,1/4, three frame
entries 1/6, three matter entries 1, and force entry 3. Its minimum is at
least 1/8, independently checked by rational positive principal minors.

A direct absolute interval perturbation gives the inconclusive value
1/8-0.66660071<0. This remains preserved. To retain the trace/difference
structure, use an explicit congruence R with R^T*M0*R=I, applied to the
RAW velocity and velocity/shift blocks before the interval Schur operation.
In the metric xx/yy plane its normalized columns are proportional to
(1,1)/sqrt(33/2) and sqrt(2)*(1,-1); xy has factor sqrt(2), the three
frame columns sqrt(6), matter columns 1, and force column 1/sqrt(3).
Every square root is outward-enclosed.

The actual full-root interval gives

    ||R^T*M*R-I||_infinity < 0.094789435,
    x^T*M*x > (1-0.094789435)/8 * |x|^2
              > 0.11315132 * |x|^2.

This is the reduced principal coordinate-velocity form on the INITIAL
planar gauge slice. It carries the entire certified C2 root uncertainty
and all circle positions. It is not a universal normalization, observable,
full physical Hamiltonian bound or a result for unrestricted transverse
wavevectors. Torus means and both charge conditions remain separate; the
earlier velocity-tangent theorem covers their stated instantaneous scope.

## Retain the force/auxiliary sector in the mixed-order limit

The independent Z has no temporal or shift-gradient couplings. Its gradient
couples to no other field gradient except psi_z. These zero statements
are verified in the actual full-root Hessian. Let

    mZ=L_ZZ>0, Cpsi=L_Zz,psiz<0, A=L_Zz,qslow.

For ordinary omega=O(k), scale delta psi=chi/k and delta Z=k*zeta.
The leading psi equation requires Cpsi*zeta=0; the leading Z equation
then fixes chi from A*qslow. Thus zeta=0 in this limit, while psi has a
nonzero, slaved subleading amplitude. It is not deleted from the physical
system. Eliminating Z first produces an induced k^2 slow stiffness and
k^3 slow/psi mixing; solving the fast response cancels that induced term.
Omitting the mixing leaves a spurious slow stiffness of about 4.94e-10
at z=0.3. Exact independent Schur algebra and actual coefficient controls
check the cancellation.

The ordinary pencil consequently uses the nine slow fields, retaining
the separate tenth dynamic force branch. For omega=O(k^2), the verified
absence of force-velocity cross couplings gives

    omega^2/k^4 = Cpsi^2/(mZ*M_psipsi),
    0.15111844 < omega^2/k^4 < 0.15191291

on the full certified initial root, in the original coordinate units.
The omitted coordinate advection is lower order for this quartic limit.
This is a formal high-frequency branch coefficient of the declared
diagnostic action. It is not a demonstrated physical EFT cutoff, permitted
frequency window, microscopic matching or numerical acceleration prediction.

## Ordinary cones and the explicit zero-speed warning

From the fresh action blocks, the normalized rest-control determinant is

    c^2*(c^2-1)^4*(c^2-1/3)*(c^2-4/5)^2*(c^2-14/13).

The four metric-luminal pairs comprise the two tensor polarizations plus
condensate amplitude and reservoir. The two vector pairs have squared
speed 4/5; the frame scalar has 1/3. The condensate phase has 14/13,
and one ordinary pair has zero speed. The zero-speed characteristic at
k!=0 must not be confused with the torus zero Fourier mode.

For the cone comparison use c=a*(omega/k+S^z)/N, physical frame
Vphys=a*V and gamma=sqrt(1+|Vphys|^2). For a rest squared speed s2 define

    Cone_s2=c^2-1+(1/s2-1)*(gamma*c-Vphys_z)^2.

The frame scalar/vector comparison uses s2=1/3,4/5. The phase term is
derived directly from the alignment action, not assumed metric-luminal:

    t=zeta*(u^2+v^2),
    Phase=(1+t)*(c^2-1)-t*(gamma*c-Vphys_z)^2.

It gives 14/13 at the rest reference. Its kinetic coefficient is
1-t*|Vphys|^2. The phase cone is superluminal relative to the metric in
this reference; this was already present in the action. Nonnegative roots
do not establish microscopic causality, and this phase result is not a
gravitational-wave speed prediction.

The degree-18 normalized determinant is compared at 19 distinct values
of c at z=0.3,1.1,2.4 and at an independent rational tilted-frame control.
All discrepancies are below 2.54e-50. The tilted control uses
V=(100,200,300)/4993, gamma=5007/4993, solely as off-shell coefficient data.
No new physical initial state is adopted. These are strong numerical
controls of the cone comparison, not an exact arbitrary-tilt determinant
proof or a theorem about the full variable-coefficient PDE.

At the dust characteristic omega=-S^z*k, an 8x8 minor of the slow pencil
has reference-inverse perturbation norm <0.010939 on the full initial-root
ball. Hence its rank is at least eight there. A nonzero minor does not
alone prove the ninth eigenvalue exactly zero throughout that family.

At the exact rest control, the double zero root has only one eigenvector.
For the Fourier generator in variables (k*qslow,qslow_dot), the audit gives
an explicit Jordan pair: w0 has only the Vz configuration component one;
w1 has hxx=hyy=2i and Vz velocity one, with A*w1=w0 and A*w0=0.
The generalized zero eigenspace has dimension two. A uniform equal-order
diagonalization cannot be inferred. An action-based physical mixed norm
and the actual constraint/density mapping are still needed.

The reference principal gradient energy is also indefinite: the static
metric trace and tensor directions have opposite signs in -d^T*G*d/2.
The audit gives -1/4 and +1/4 per squared Fourier amplitude in its stated
normalization. This does not identify a physical ghost or prove a new UV
instability; the physical density and mixed derivative-count mapping has
not been completed. It does rule out treating the positive kinetic bound
as an already positive full principal Hamiltonian.

## Verification, preserved attempts and next decision

[Executable V3](../../../Analysis/MasterTests/test_01_r4c1_rtau_prepared_principal_v3.py):
30/30, exact immutable replay; session 9504 terminal exit 0.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_prepared_principal_v3_attempt_01/summary.json)
SHA256 9689901a50cf2a41f51dea63ce8bbf5f01b8a5fccdab92337d23a6ff7636f152.

[Interpretation audit V2](../../../Analysis/MasterTests/audit_01_r4c1_rtau_prepared_principal_v2.py):
15/15, exact replay.
[Audit receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_prepared_principal_audit_v2_attempt_01/summary.json)
SHA256 d168acacc483ed9026fab18b80702675b92349b0c68d92388bcf05f020bae345.
It derives the Jordan pair, energy-sign directions, alignment co-metric
and mixed-order Schur cancellation independently from the exported blocks.
These same-author checks are not independent external peer review.

V1 remains at 16/22: its comparison omitted the existing alignment cone,
and the absolute interval kinetic bound was inconclusive. V2 remains at
21/25: it restores alignment and proves positivity but used insufficiently
accurate interval-inverse midpoints in point comparisons. [V3 specification](RES001_R4C1_RTAU_PREPARED_PRINCIPAL_V3_SPEC_2026-11-01.md)
uses 24 Neumann terms and an explicit point tail <1e-40, retaining the
five-term whole-root bound and unchanged 1e-28 acceptance. Audit V1 remains
at 14/15: [audit V2](RES001_R4C1_RTAU_PREPARED_PRINCIPAL_AUDIT_V2_SPEC_2026-11-01.md)
replaces structural polynomial equality with exact expanded-difference zero.
No equation, physical coefficient, allowed mode or threshold was removed.

The next deciding calculation is the actual constrained physical
configuration/momentum/density graph and a controlled mixed-norm evolution
operator on the prepared slice, including the zero-speed sector, both
global charges, torus means, auxiliary secondary relation, coefficient and
gauge-projector drift. Do not substitute more rest spectra, the old
homogeneous [0,0.05] estimate, or an arbitrary positive weighting for that
task. Transverse modes, nonlinear persistence, interactions/window and
genuine identifying matching remain open. No concrete manuscript change
follows from this candidate-only calculation. Goal ACTIVE and incomplete;
review DEFERRED. No action adoption, provider dispatch, vault mutation,
publication, commit, push or deployment.
