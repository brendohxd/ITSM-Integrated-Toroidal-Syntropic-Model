# Homogeneous B1: positive instantaneous reduced kinetics, evolving domain open

29 October 2026. Conditional independent G2/G4 control. Review DEFERRED;
Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result and significance

The old, already justified homogeneous B1 control has an exactly positive
ten-field kinetic block at its initial event after the actual nonzero-mode
shift and auxiliary equations are solved. This calculation supplies a
constraint-reduced quadratic action and an instantaneous canonical momentum
map. It is more specific than the earlier formal graph energy, and it does
not replace the registered vortical G1 preparation.

The result is local to the homogeneous control's initial event. It does not
establish positivity of the full Hamiltonian, gradient stability, propagation
on an interval, nonlinear stability in a neighbourhood of alignment, a physical
frequency window, a GR limit, or admission of the nodal warning probes. In
particular the zero-tilt auxiliary degeneracy cannot be extrapolated through
the finite-tilt Legendre inverse, which divides by V^2. No family GO or parent
promotion follows.

## Background and elimination

The [contract](RES001_R4C1_B1_REDUCED_KINETIC_V1_CONTRACT_2026-10-29.md) reuses
the [original B1 action-derived control](RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md)
and its [homogeneous existence theorem](RES001_R4C1_B1_GLOBAL_REGULARITY_REPORT_2026-09-29.md).
It does not rerun that theorem. At the initial event a=C=1, H is the positive
square root of 3469/4620, (u,v,r)=(1,0,1), their velocities are (0,1,1/4),
psi_dot=1/5, rho_m=1/5, and the spatial frame and Z vanish. The old B1
coefficients include K_Q=3, b=5/11, g_r=3/7, c_2=1/10 and
M_U^2(c_1+c_4)=1/6. These are declared control inputs, not matching results.
The later eta=1/4 B1-frame family has different coefficients and is not used.

For a nonzero planar torus wave k, use delta tau=0 and
delta h_xz=delta h_yz=delta h_zz=0. The multiplier variation is performed
before elimination. On the future branch it fixes N=tau_dot/C; the clock
gauge therefore gives N=exp(-beta delta psi) at this event. Its spatial
derivative is retained in the original frame and curvature terms. The
remaining lapse equation fixes epsilon, since its epsilon coefficient is
nonzero. It is not an additional vacuum Hamiltonian constraint on the ten
fields. This is a local gauge reduction near strictly positive dust; it does
not prove that the recovered density remains positive during perturbation
evolution. The clock equation follows from the original diffeomorphism
identity when the remaining field equations and solved constraints hold.

Use metric amplitudes delta h=a^2 gamma and frame amplitudes delta V=a^-1 v.
Their velocity increments include 2H gamma and -H v respectively. All three
shift values and their derivatives are retained in the local second variation.
The calculation starts with eleven amplitudes, including Z, their velocities
and spatial derivatives. The Z velocity row vanishes on this aligned
background; Z is then eliminated by its own equation, not set to zero.
The physical norm-cubed force has zero C2 Taylor coefficient at zero
projected gradient. The original nonzero A term remains in independent
finite-perturbation checks; an A=0 action is not adopted.

After Hermitian Fourier assembly, the algebraic block in order
(delta Z,Sx,Sy,Sz) is

$$D=\operatorname{diag}(5/11,k^2/2,k^2/2,-k^2/15),
\qquad \det D=-k^6/132.$$

It is invertible for real k != 0. A negative shift pivot is an algebraic
constraint pivot, not a propagating kinetic eigenvalue. k=0 requires a
separate reduction. In particular the regulator equation is
delta Z=k^2 delta psi-i k psi_dot v_z, consistent with variation of
Z+Delta psi=0 at this homogeneous event. The full shift solution, rather
than a transverse-only truncation, is exported in the receipt.

## Kinetic and canonical normalization

Order the remaining amplitudes as
(gamma_xx,gamma_xy,gamma_yy,v_x,v_y,v_z,delta u,delta v,delta r,delta psi).
The reduced Lagrangian per Fourier pair has the form

$$L_2=\tfrac12\dot q^\dagger M\dot q
       +\operatorname{Re}(\dot q^\dagger Bq)
       +\tfrac12q^\dagger Qq,$$

with Hermitian M,Q. All q/velocity, odd-spatial-derivative, curvature,
potential, matter and regulator coefficients are retained in the exported
matrices. At this event the only off-diagonal entries of M are
M_13=M_31=4, and

$$\operatorname{diag}M=(17/4,1/2,17/4,1/6,1/6,1/6,1,1,1,3).$$

Its eigenvalues are
33/4, 1/4, 1/2, 1/6 (three times), 1 (three times), and 3.
Consequently M >= (1/6) I and det M=11/768 in this declared amplitude
convention. The exact LDL decomposition and R with R^T R=M are exported;
they define unit instantaneous kinetic coordinates. This rescaling fixes
neither an SI matter residue nor the microscopic nonlinear force coefficient.

The momentum and Hamiltonian are

$$\pi=M\dot q+Bq,\qquad
H_2=\tfrac12(\pi-Bq)^\dagger M^{-1}(\pi-Bq)-\tfrac12q^\dagger Qq.$$

For the convention omega=dq wedge dpi, its pullback to (q,q_dot) is

$$\Omega=\begin{pmatrix}B-B^\dagger&M\\-M&0\end{pmatrix}.$$

The antisymmetric B contribution is retained and the canonical pullback is
checked exactly. For example B_(gamma_xx,v_z)=ik/2 and
B_(v_z,delta psi)=-ik/15 are present. Dropping such terms would not give the
same momentum map. The symplectic determinant is (det M)^2, so the frozen
form is nondegenerate. These complex-mode expressions mean the corresponding
real two-quadrature form; direct sine/cosine assembly is checked separately.
Time derivatives of B, moving constraints, the volume factor and the full
time-dependent generator have not been computed here. A frozen two-form is
not a proof of conserved perturbation energy or interval-wide normalization.

## Verification and preservation

The [versioned executable](../../../Analysis/MasterTests/test_01_r4c1_b1_reduced_kinetic_v1.py)
passes 41/41 checks. The [fresh summary with complete matrices](../../../Analysis/MasterTests/outputs/r4c1_b1_reduced_kinetic_v1_attempt_01/summary.json)
has SHA-256 `829b013edc716cb2a7c9a2a4161bf2830186b0d68673b8b57e3928deb5a1d53a`.
Its recomputing read-only replay is byte-identical, exit 0. Seven directly
pinned files and their seven sidecars retain both bytes and modification times
through calculation and replay. This independent control does not imply
independent external review of the original action implementation.

The exact algebra checks Hermitian assembly, all eliminated equations, the
stationary pullback, LDL inertia and the canonical two-form map. Independent
real directional second differences evaluate the original physical density
with A retained at three directions and steps 1e-12 and 1e-16. The largest
normalized discrepancy at the smaller step is 5.724e-19; convergence retains
the expected O(step) C2 remainder from the physical norm-cubed term. Separate
real-quadrature identities are exact at k=1,7,40. Those finite samples are
controls; the symbolic nonzero-k algebra supplies the stated k scope.

## Next work and unchanged holds

The direct continuation of this independent control is to obtain its
background-dependent quadratic coefficients and their actual time drift,
then test coupled propagation and interaction bounds. Do not repeat the B1
existence proof or use a frozen-frequency scan as its replacement. This
control can inform G2/G4 while the registered vortical G1 route still needs
an on-shell nonlinear current estimate or a demonstrated scoped rejection.
Neither route silently replaces the other.

G1-G6 INCOMPLETE; Stage 2 INCOMPLETE; Stage 3 NOT_ENTERED; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage 4A CLOSED.
Inherited action/B1/backend/constraint review remains DEFERRED. No manuscript,
PDF, website, vault, action, adopted initial state, commit or push is changed.
