# Retained 20-direction ordinary/quartic principal assembly

4 November 2026. Conditional component of the
[actual prepared coupled-energy contract](RES001_RTAU_PREPARED_COUPLED_ENERGY_V1_CONTRACT_2026-11-04.md),
following the [ordinary Ward energy](RES001_RTAU_ORDINARY_WARD_ENERGY_V4_REPORT_2026-11-04.md).
R-tau remains an UNADOPTED comparator. Original R4C1 and all G1-G6
requirements remain unchanged. Review DEFERRED; physics_pass=false;
gate_effect=NONE.

## Result and limits

The initial mixed principal calculation now retains all 20 nonzero-mode
directions: 18 ordinary directions, including both zero-speed coordinates,
and the physical force/auxiliary pair. Both directions of ordinary/force
coupling are derived and bounded on the whole registered initial-root
enclosure. Neither a branch nor its forcing is projected away.

The force energy has positive weights and the necessary spatial-coefficient
terms cancel at formal principal order. A same-strength order-minus-one
change removes the two order-k cross blocks, with an explicit bound for
the additional FROZEN-symbol remainder. Whole-root bounds include

    0.1513824795 < omega_fast^2/k^4 < 0.1516479396,
    ||S1||_2 <0.601920,
    |k|>=2 suffices for invertibility of I+S1/k,
    ||R_normalform,frozen||_2 <0.241609,
    5.24554e-8*|Y20|^2 <= E_symbol <=7.752273e6*|Y20|^2.

The |k| threshold is a mathematical sufficient condition for this frozen
principal transformation, in the original registered coordinate units.
It is NOT a physical cutoff, a permitted EFT/interaction window or an
accuracy claim for the actual system at k=2. Its omitted order-zero terms
are still unbounded in the required full energy. The energy equivalence
constants are deliberately conservative, not growth or propagation rates.

The result proves the stated initial principal assembly and formal
highest-order energy cancellations. It does NOT prove a full global
variable-coefficient evolution inequality. Spatial composition terms,
coefficient/gauge/constraint/Green drift, T_dot, charge/range/harmonic
partners and an evolving background tube remain required. A pointwise
symbol change is not exact Fourier decoupling for varying coefficients.
No low mode, torus mean or generated Fourier tail is declared absent.

## Physical pair, coefficients and secondary metric mixing

Use original-coordinate canonical xi=delta pi_psi, not an assumed normal
velocity perturbation. With h=a^2 I initially, define

    kappa=a^-2, s=psi_bg,z, lambda_z=a_z/a,
    mu=a^3, M=N*mu, d=b*M*kappa,
    m=L_vpsi,vpsi>0, aphi=1/m,
    vphi=(L_vpsi,psiz+S*m)/m,
    d_z=d*(lambda_z-beta*s).

All temporal force derivatives retain the full norm-cubed force. Its
positive-Y root branch and the existing force-temporal/ordinary-velocity
separation are inherited and checked; no clock-only kinetic substitute is
used. The lapse remains N=exp(-beta*psi).

The auxiliary observable contains

    delta Z=kappa*k^2*chi-i*kappa*k*s*u+lower symbol orders,
    u=(delta hxx+delta hyy)/(2a^2).

For example, the exact conformal scalar Laplacian also has the
-i*kappa*lambda_z*k*chi term. This contributes to the first force row
below; it is not discarded as if the Laplacian had constant coefficients.
With the strong leading trace graph,

    u=i*c*P_Vz/(a^2*k), c=gamma/a,
    delta Z=kappa*k^2*chi+hmetric*P_Vz+lower orders,
    hmetric=kappa*s*c/a^2.

The physical Z is retained. Replacing it by kappa*k^2*chi would lose both
metric mixing and its differentiated forcing.

## Fast highest and first derivative rows

For the material-frame symbol A(k)=k^2*A2+k*A1+order zero, the fast blocks
are

    A2_fast = [[0, kappa*aphi],[-d,0]],
    A1_fast = i*[[-vphi, -(2*kappa*aphi_z+kappa*lambda_z*aphi)],
                  [d_z-beta*d*s, -vphi]].

The first off-diagonal coefficient comes from applying the full background
scalar Laplacian to aphi*xi. It uses the actual derivative m_z from the
exported spatial Hessian derivative, aphi_z=-m_z/m^2. No higher derivative
of an error radius is assumed.

The second off-diagonal coefficient also uses the full clock/regulator
current. Its relevant exact terms are

    D_z(d*Z_z)-2*beta*D_z(d*s*Z)+beta*d*s*Z_z
      =d*Z_zz+(d_z-beta*d*s)*Z_z
                         -2*beta*D_z(d*s)*Z.

The last term stays in the unassembled order-zero remainder. The local
other-sector identity supplies -beta*M*delta Sigma rather than an
independent high-gradient source. The completed strong-density change
keeps that source at its declared order; it is not set to zero.

Use the physical fast energy weights

    Hfast=diag(d/kappa,aphi)=diag(b*M,1/m).

Hfast*A2_fast is pointwise skew. Write B1=A1_fast/i. For the differential
operator -A2_fast*D_z^2+B1*D_z, the formal first-derivative coefficient in
the energy adjoint sum is

    2*(Hfast*A2_fast)_z+Hfast*B1-B1^T*Hfast.

This vanishes exactly using d_z=d*(lambda_z-beta*s). Thus the coefficient
gradients are included in, and needed for, the principal cancellation.
Deleting aphi_z or the -beta*d*s term fails the exact symbolic control.
This formal cancellation does not bound the full order-zero/time terms.

The quartic squared coefficient is kappa*aphi*d>0. Its stated interval
uses the same action and uncertainty, with the exact volume/lapse relation
for d retained. It is not an independently matched physical scale.

## Both order-k cross blocks

Keep ordinary Y18=(w,Q8,P9) from the Ward-energy owner. Let X=E*Q+
i*c*vtrace*P_Vz, with all nine ordinary canonical momenta retained. The
material ordinary velocity and momentum rows are

    v=Mordinary^-1*(P-i*Brel*X),
    Pdot/k=-i*Brel^T*v+Grel*X.

The auxiliary-gradient/ordinary-configuration coefficient is exactly

    A_hxx=A_hyy=-d*s/(2a^2), A_other_ordinary=0.

It follows by varying the physical volume factor in -d*Z_z*psi_z at the
conformal initial slice. The full exported Hessian is separately checked
for consistency with this identity and its exact zero flux columns.
Thus the ordinary<-force block has momentum rows i*A_q*Z. There is no
order-k force term in the ordinary configuration or corrected-density row.
The latter uses the completed strong-density source estimate, not a fresh
assumption of vanishing density forcing.

For the reverse block define Tq=L_vpsi,qordinary. Retain the FULL shift
Schur response. If Cshift,Dshift and Kshift are the exported ordinary
velocity/gradient/shift blocks, then in MATERIAL velocities

    Dshift_rel=Dshift+S*Cshift,
    W_shift= -Kshift^-1*(Cshift^T*v+i*Dshift_rel^T*X).

Here W_shift=(delta S^x_z,delta S^y_z,delta S^z_z). All three shift-gradient
directions remain; its third component enters clock kinematics.
The advection conversion S*Cshift is
retained. The leading reverse Z row is

    (Bfo*Y18)_Z = -kappa*aphi*Tq*X
                 -i*kappa*s*W_shift[2]
                 -i*kappa*s*t*v/a^2
                 +i*vphi*hmetric*P_Vz,

where t*v=(v_hxx+v_hyy)/2. These four terms respectively come from the
clock Legendre field differential, shift correction, secondary metric
variation and the secondary lift in force advection. Direct symbolic
substitution verifies their full combination. The xi reverse row is zero
at order k on this strong constraint graph; its ordinary current/volume/
force sources remain at order zero. A source-level local lapse identity,
not a weak numerical residual, is needed for that statement.

## Retained-pair normal form and exact frozen remainder

Assemble

    D=diag(0_18,A2_fast),
    B=[[Aordinary,Bof],[Bfo,A1_fast]],
    Bdiag=diag(Aordinary,A1_fast).

A2_fast is invertible everywhere in the registered enclosure. Set

    S1_of=-Bof*A2_fast^-1,
    S1_fo=A2_fast^-1*Bfo,
    S1_oo=S1_ff=0, T=I+S1/k.

Then B+[S1,D]=Bdiag. This is an invertible change retaining the fast pair,
not a slow-graph projection. For the frozen truncated symbol the EXACT
identity is

    T*(k^2*D+k*B)*T^-1
      =k^2*D+k*Bdiag+(S1*B-Bdiag*S1)*T^-1.

The final term is bounded by the numerator norm divided by
1-||S1||/|k|. The whole-root estimate ||S1||<0.601920 gives the threshold
and remainder bound at the top. No limit of an untracked fast response or
truncation of forced tails is substituted for this identity.

With Hordinary from the actual ordinary-energy certificate and Hfast as
above, the transformed symbol norm uses H0=diag(Hordinary,Hfast) and
E_symbol(Y20)=(T*Y20)^*H0*(T*Y20). Its stated lower/upper bounds follow from
the existing ordinary constants, positive fast weights and
1-||S1||/|k| <= singular_values(T) <=1+||S1||/|k|.

When coefficients vary, composing this symbol change with spatial
operators also generates S1_z, coefficient-gradient and nonlocal terms.
They are not equal to the frozen matrix remainder. Time-dependent changes
also generate T_dot and moving constraint/Green/gauge terms. These remain
explicitly OPEN, so no full energy or finite-time claim follows here.

## Verification and preservation

Executable `Analysis/MasterTests/test_rtau_mixed_principal_assembly_v1.py`;
[frozen criteria](RES001_RTAU_MIXED_PRINCIPAL_ASSEMBLY_V1_SPEC_2026-11-04.md).
Receipt `Analysis/MasterTests/outputs/rtau_mixed_principal_assembly_v1_20261104/receipt.json`.
SHA256:

    261a512ad5447b388063451eb993eee7b0638f8e6e3cac3e4a45bf028e49b51b

28/28 bounded controls and byte-identical replay COMPLETE. Checks include
the highest/first formal fast energy identities, rejection of omitted
coefficient gradients, full regulator-current and secondary/Legendre/
metric/shift algebra, an independent exact finite-block normal-form
identity, actual coefficient/zero-column consistency, retained cross
blocks and all original pins. These remain same-author controls, not
independent scientific review.

All 219 original input pins and 286 source pins in this receipt are
unchanged; snapshotted sidecars and timestamps were preserved. All previous
failed/inconclusive attempts remain. No action Hessian was rerun.

## Next required work

Derive and bound the actual variable-coefficient composition and full
order-zero remainder, including derivatives of this normal form, the
ordinary energy and zero-charge coordinate, exact elliptic reconstruction,
auxiliary/clock terms and the moving gauge/Green/range map. Retain all
global means, charge tangents and harmonic/modulus partners. Then establish
actual coefficient/domain persistence before integrating through any time
interval. The original target [0,0.05] remains a target, not a consequence
of this principal result.

The domain-first goal remains ACTIVE. Full coupled energy, actual time
tube, interactions/window, genuinely identifying matching and dependent
numerical predictions remain incomplete. No paper/site promotion, action
adoption, vault write/sync, dispatch, publication or Git delivery occurred.
