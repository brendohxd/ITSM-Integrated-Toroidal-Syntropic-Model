# Actual initial corrected-density row and physical-density reconstruction

5 November 2026. High confirmed by operator. Conditional component on the
unchanged prepared R-tau comparator. R-tau remains UNADOPTED. This does not
complete the prepared coupled-generator/domain calculation or G1-G6.

## Actual row retained

Use the reorganized other-sector action identity, not rho renamed as Sigma:

    M=N mu, Sigma=rho+e_force+b Z^2/2, I_other=M Sigma,
    (partial_t-S D)Sigma=C Sigma-N trK f
      -(p/mu)D(M f_s)-f_s[(Np)_z+S_z s]-W_f
      +bN[T s(Z_z-beta s Z)-trK Z^2/2]+Ward_defect/M,
    C=-N trK, s=psi_z, T=kappa trK-2Kupzz.

The Ward term has its existing exact constrained-background/tangent scope;
the numerical centre is not assumed to be an exact solution. All ordinary
metric/frame work in W_f remains. The momentum current remains

    pi_t=D J+Rloc,
    J=S pi-M f_s+d Z_z-2beta d Z s,
    Rloc=beta M(e_force-Sigma)-beta L_reg,
    L_reg=b M Z^2/2-d Z_z s+beta d Z s^2, d=b M kappa.

Let sigma=delta Sigma, xi=delta pi, zeta=delta Z, chi=delta psi,
P=Dinv P0 on the original periodic circle, r=beta d s, a=bN T s,
c=a/d, alpha=-(p f_ps+f_s). Define the complete linearized remainders

    J0=delta J-S xi-d D zeta,
    R0=delta Rloc-r D zeta,
    sigma_t-S Dsigma=C sigma+a D zeta+F0,
    A_p=N alpha, Fbar=F0-A_p D(delta p),
    Gchi=-beta Np chi+s delta S.

F0 is the entire variation of the first displayed equation after extracting
the named transport/reaction/auxiliary terms, including delta S Sigma_z.
It is not a freely chosen source or a deleted sector. The actual two-step
corrected variable w=sigma-cPxi-alpha Dchi obeys

    w_t-S Dw=Cw+(Cc-c_t+S c_z)Pxi+Fbar
       +(C alpha-alpha_t+S alpha_z-alpha S_z)Dchi
       -alpha N_z delta p-alpha D Gchi
       +c[mean(S xi)-S mean(xi)]-c mean(d_z zeta)
       -c P0(J0)-c P0(r zeta)+c P(r_z zeta)-c P(R0).

The delta Z_z and delta p_z cancellations use a=cd and A_p=N alpha.
Coefficient time derivatives, scalar-gradient transport and every primitive
mean are retained. The original source calculation checked this complete
normal form before any old constraint-lift estimate was applied.

## Corrected norm composition

The old source executable is reexecuted: its 20 controls pass and all its
unreduced row coefficients reproduce exactly. Only its original-coordinate
inequalities in (w_L2,Q_H1,P_L2,force_H2,harmonic velocity) are reused.
The old lifted or weakened-density estimates are NOT used. The raw field-rate
and corrective-shift coefficients precede the faulty constraint lift; their
dependence on unreduced canonical norms is retained.

Compose these inequalities with the full configuration/momentum maps of
corrected momentum lift V2 and the force H2 inverse V3. For U the SUM of the
eight registered strong/global input norms plus the independent harmonic
coordinate-velocity norm, the outward interval bounds give

    ||initial original-coordinate density source||L2 <= 102113 U,
    upper initial L2 norm growth rate of w <= 102113 U.

The second inequality includes the scalar transport contribution. It does
not bound w_t itself in L2 by deleting S Dw. The receipt exports the separate
input-wise source and norm-rate coefficients. The large constants are
conservative initial coordinate estimates, not physical couplings, useful
accuracy guarantees, an energy theorem or a time-uniform bound.

## Physical rho, including the compensation

The exact Legendre differential at fixed canonical momentum is

    delta e_force=(p/mu)xi-(p f_p/mu)delta mu
                   -sum f_q delta q-f_s Dchi.

Consequently the physical density is reconstructed by

    delta rho=w+cPxi-p f_ps Dchi-(p/mu)xi
                +(p f_p/mu)delta mu+sum f_q delta q-bZ zeta.

The f_q partials hold p,s fixed. A generic-field derivative is not evaluated
by freezing the metric/frame dependence of f. The corrected maps yield

    ||delta rho||L2 <= 15 U8,

where U8 is the sum of the eight strong/global norms, excluding harmonic
coordinate velocity. The largest input coefficient is below 14.565496;
the receipt contains all eight intervals. This is a reconstruction bound,
not a new density evolution theorem or a positivity claim about matter.

## Verification and preserved attempts

Usable executable: `Analysis/MasterTests/test_rtau_actual_corrected_density_v4.py`.
Receipt: `Analysis/MasterTests/outputs/rtau_actual_corrected_density_v4_20261105/receipt.json`.
20/20 controls pass and immutable replay is byte-identical. This includes the
reproduced raw-source calculation, corrected lift composition, physical-rho
identity, mean/transport rejection tests and source preservation. These are
same-author computational controls; independent Rule-9 review is DEFERRED.

V1 preserves the preliminary rate result. V2 and V3 fail during the additional
physical-map coefficient evaluation: interval dependence lets a generic Y
enclosure cross zero, so fractional powers produce complex intervals. V3's
gamma^2-1 rearrangement does not repair this enclosure. These are preserved
implementation/enclosure failures, not observed negative physical Y.
V4 uses exact generic first/second force derivative formulas evaluated with
the already certified conformal-background sum-of-squares Y enclosure from
force-pair V2. This preserves generic metric/frame partials while using the
proper background value. No interval is clipped, imaginary part discarded,
input/threshold changed or physical Y<0 continuation adopted. Only zeroth
spatial coefficients are used in the added physical-map bound; unused higher
jet slots do not impose a zero higher background derivative.

## Still open and next calculation

The initial row/source and physical-density reconstruction bounds are
complete within the declared compatible norm scope. The full comparison
against the registered twenty-direction operator is NOT YET ASSEMBLED.
It must retain the actual physical-variable map and its time derivative,
and classify principal couplings without burying derivative loss in a
bounded remainder. Moving Green/range/charge maps, compatible-domain
persistence, full coupled energy and a useful t=0.05 tube remain OPEN.

Thus the overall corrected-density/full-generator task remains INCOMPLETE.
No physical stability, interacting validity window, matching input, numerical
acceleration prediction or canonical action adoption follows. The next task
is the density row's full coupled principal comparison, then moving-map
transport, as required by the preserved preparation.

Direct dependencies: corrected Sigma lift V4 and descendants, raw unreduced
density source, exact other-sector lapse/current identities, normal-form
owners, and the registered canonical/gauge norm maps, all pinned by receipt.
Inherited reviews remain DEFERRED; scientific parent holds remain unchanged.
physics_pass=false; gate_effect=NONE; no vault mutation, provider dispatch,
publication, commit/push, deployment or runtime reconfiguration.
