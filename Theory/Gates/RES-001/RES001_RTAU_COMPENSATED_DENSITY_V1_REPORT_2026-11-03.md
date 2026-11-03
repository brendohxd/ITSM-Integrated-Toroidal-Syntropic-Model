# R-tau action-derived compensated density and surviving metric work

3 November 2026. Conditional exact operator result within the confirmed-
High observable-norm bundle. R-tau remains an unadopted comparator;
original R4C1 unchanged. Review DEFERRED; physics_pass=false;
gate_effect=NONE; original G1-G6 incomplete.

## Result and its limit

The full action supplies an invertible compensated density observable
whose regulator contribution has NO p_zz or Z_zz term in its material
time row. Here p is the normal CLOCK velocity and Z=-Delta_h psi. Thus
the fourth-spatial-derivative regulator contribution to this density row
cancels exactly. A nonzero metric-work term proportional to Z_z remains.

The correct force normalization is its full normal-clock Legendre energy,
including the independent plenum frame and norm-cubed force interaction.
It is not generally K_Q*p^2/2. The quartic force mode remains in its own
field equations. This cancellation does not prove a positive physical
energy, strong rate bound, controlled coupled evolution or time tube.

Owners: [bundle](RES001_RTAU_COUPLED_OBSERVABLE_NORM_V1_CONTRACT_2026-11-02.md),
[weak density row](RES001_RTAU_WEAK_DENSITY_ROW_V2_REPORT_2026-11-03.md),
[actual mixed action](RES001_R4C1_RTAU_MIXED_OPERATOR_V4_REPORT_2026-11-01.md)
and [frozen specification](RES001_RTAU_COMPENSATED_DENSITY_V1_SPEC_2026-11-03.md).
The old [homogeneous physical-norm result](RES001_R4C1_RTAU_PHYSICAL_NORM_V2_REPORT_2026-10-31.md)
is reused only in its original scope. The vault continuity pointer
chk_4545d607e49dfa0650f668f9 identifies that older source; its current local
file was checked directly. No old homogeneous theorem is transferred to
the prepared inhomogeneous background.

## Derive the force normalization before choosing the observable

Use the declared planar variables

    mu=sqrt(h), kappa=h^{zz}, p=(psi_t-S^z*psi_z)/N, s=psi_z,
    c=V.h.V, gamma=sqrt(1+c), w=V^z,
    Y=c*p^2+2*gamma*w*p*s+(kappa+w^2)*s^2.

The actual force term, kept with its nonzero norm-cubed interaction, is

    f=K_Q*(gamma*p+w*s)^2/2-A*Y^(3/2),
    f_p=K_Q*gamma*(gamma*p+w*s)
                         -3*A*(c*p+gamma*w*s)*sqrt(Y).

The prepared mixed-action receipt already proves strict Y>0 on the
initial root ball. No third derivative at a Y=0 cusp is inferred here.
The actual source's velocity dependency is checked: apart from the old
regulator, the normal scalar velocity enters only this force sector.
R-tau explicitly removes the old temporal regulator and replaces it by
the clock-spatial regulator. Thus the coordinate canonical momentum is

    pi_psi=mu*f_p.

This is derived from L_force=N*mu*f and p=(psi_t-S^z*s)/N. It includes
the frame tilt and A term. The action-normalized Legendre energy is

    e_force=p*f_p-f
      =K_Q*(gamma^2*p^2-w^2*s^2)/2
           +A*sqrt(Y)*[Y-3*p*(c*p+gamma*w*s)].

No positivity/coercivity of this expression is assumed. It is not
identified with a complete Hilbert/renormalized stress tensor. K_Q,A,b
remain coefficients of the declared diagnostic action, not newly derived
microscopic matching values. The MAT-001 matching hold is unchanged.

An exact nonzero-tilt control rejects substituting the clock-only kinetic
energy K_Q*p^2/2. At the old homogeneous rest configuration V=0,s=0,
the expression reduces to K_Q*p^2/2, consistent with the previous linear
control. This value/first-variation limit does not make the norm-cubed
interaction C3 at its zero-gradient point.

## Static cancellation and invertibility

Split the same improved density into the other action sectors, the full
force sector and the on-secondary regulator:

    rho=R_other+f-p*f_p-b*Z^2/2,
    R_other=[L_other-sum_other pi_i*(q_t^i-Lie_S q^i)-D_z B0]/(N*mu).

B0 is the existing lapse/curvature/frame improvement, retained in full.
The force term has no lapse-gradient improvement of its own. Define

    Sigma=rho+e_force+b*Z^2/2.

Then Sigma=R_other exactly. Static force Legendre energy and auxiliary
regulator energy cancel out of this density combination. The other
action sectors still carry their lapse, frame, metric and matter dependence.

This is an observable change with derivative dSigma/drho=1. Physical rho
is recovered as Sigma-e_force-b*Z^2/2. No density fluctuation, charge,
phase, Fourier mode, harmonic datum or physical clock flow is deleted.
Sigma is not fixed pointwise, and its mean is not imposed as a new charge.

## General planar geometry and regulator time calculation

Let D_t=partial_t-S^z*D_z, trK=h^{ij}K_ij, Kupzz=K^{zz}, and

    T=kappa*trK-2*Kupzz.

Full metric transport gives

    D_t mu/mu=N*trK+S^z_z,
    D_t kappa=-2*N*Kupzz-2*kappa*S^z_z,
    D_t s=(N*p)_z+S^z_z*s.

These identities retain transverse shifts and all six metric/extrinsic
entries. The exact material/spatial commutator is
[D_t,D_z]=S^z_z*D_z. With Z=-mu^-1*D_z(mu*kappa*s), it follows that

    D_t Z=-N*trK*Z
                    -mu^-1*D_z[mu*N*T*s+mu*kappa*(N*p)_z].

Coordinate-index terms cancel in deriving this equation; metric work
does not. No homogeneous, conformal-future or zero-gradient restriction
is imposed by these generic planar identities.

The clock regulator density and its scalar Euler row are

    L_reg=b*N*mu*(Z^2/2-kappa*Z_z*s+beta*Z*kappa*s^2),
    E_reg=-beta*L_reg
          -D_z[b*N*mu*(-kappa*Z_z+2*beta*Z*kappa*s)].

The same action current is

    F=b*N^2*mu*[Z*kappa*p_z+Z*T*s-p*kappa*Z_z].

Use N_z=-beta*N*s and the secondary equation. In the material Sigma row,
the complete regulator contribution is

    R_reg=F_z/(N*mu)+(p/mu)*E_reg+b*Z*D_t Z
                                   -b*N*(beta*p-trK)*Z^2/2
         =b*N*[T*s*(Z_z-beta*s*Z)-trK*Z^2/2].

The coefficients of Z_zz and p_zz in the first line vanish exactly.
The second line is the full residual, not a selected subset. Its
Z_z coefficient b*N*T*s is generally nonzero. An independent positive
periodic profile agrees with the generic identity, and an explicit
nonzero-metric-work probe rejects dropping the residual.

On a fixed metric with K=0 this regulator work vanishes. Setting K=0
on the evolving prepared problem would be an additional restriction;
it has not been made. For coupled perturbations the residual includes
delta K, delta trK, delta kappa, delta s and delta Z_z. It must be
handled together with metric dynamics, not treated as already bounded
in a strong physical energy norm.

## Keep the entire force and other-sector remainder

For completeness define

    E_other=L_other,psi-D_z L_other,psi_z,
    W_f=sum_metric_frame[f_q*D_t q], holding p,s fixed.

The force scalar Euler equation includes the clock-lapse terms:

    pi_psi,t=D_z(S^z*pi_psi)-D_z(N*mu*f_s)
                                  +beta*N*mu*e_force+E_other+E_reg.

The physical matter density obeys its existing current law. Combining
these equations gives the material compensated row

    D_t Sigma=N*(beta*p-trK)*Sigma-N*trK*f
            -(p/mu)*D_z(N*mu*f_s)-f_s*[(N*p)_z+S^z_z*s]
            -W_f+(p/mu)*E_other+R_reg
            +Ward_defect/(N*mu).

The Ward defect is the original momentum-constraint divergence. It
vanishes on the exact constrained background/tangent, not by assuming a
finite numerical centre has zero defect. The full force work and other
action scalar row are RETAINED. In particular the frame is independent;
it is not aligned to the clock to simplify this equation.

This row removes the highest regulator terms from the density equation
while retaining the quartic force equation. It suggests the next mixed-
regularity estimate, but no quantitative bound for the complete compensated
rate or coupled energy has been established in this calculation.

## Verification, preservation and scientific disposition

[Executable](../../../Analysis/MasterTests/test_rtau_compensated_density_v1.py):
27/27 exact/source controls; fresh
[receipt](../../../Analysis/MasterTests/outputs/rtau_compensated_density_v1_20261103/receipt.json)
SHA256 51eb265de42ce4b32c35595a9f930742832f50e85b90e44fa04855591a32d522.
Read-only replay returned byte-identical receipt bytes. All 219 inherited
source hashes and existing sidecar bytes/timestamps were preserved.
No new failed attempt occurred; earlier failures remain intact.

Checks include actual force-source/repair dependencies, the generic
Legendre calculation, static density inversion, the material-row algebra,
regulator Euler variation, all cancelled and surviving derivative terms,
an independent periodic-profile identity, and full-metric transport with
nonzero transverse shifts and off-diagonal metric data. These are
same-author controls, not independent scientific review.

NEXT: quantify the complete compensated remainder on the actual prepared
root domain, including W_f,E_other and the surviving metric/regulator
stress. Test its coupling to the canonical/gauge rows, physical zero-speed
sector and quartic mode. A coercive action/observable-based energy and
its moving-basis/Green drift are still required before a finite-time
claim. Do not replace this task with arbitrary positive weights.

The controlled coupled background tube, nonlinear preservation, interacting
validity window, transverse perturbations, GR/local compatibility and
identifying matching remain open. No numerical C_chi or a0 follows.
No concrete defect in current P1/P2/Thermodynamics/original-R4C1 papers is
established by this unadopted-comparator identity; no paper/site claim
change is warranted. Goal ACTIVE; full bundle and original G1-G6 incomplete.
No action adoption, provider dispatch, vault sync/mutation, publication,
commit, push or deployment.
