# Density-only weakening fails the original coupled-energy control

3 November 2026. Exact adequacy control, not a new prepared-background
admission result. R-tau unadopted; original R4C1 unchanged. Review DEFERRED;
physics_pass=false; gate_effect=NONE; G1-G6 incomplete; goal ACTIVE.

## Scientific result

Weakening ONLY the compensated density from L2 to H^-1, while retaining
the other field/canonical momentum derivative orders, restores a defective
ordinary zero-speed pair in the original homogeneous R-tau control. It
therefore fails the standard uniformly positive order-zero principal-energy
test in that control. The original stronger-density energy still passes.

The new initial weak source/state chart and density-sector transport bound
remain valid in their stated scopes. Neither was a full coupled-energy
theorem. This exact adverse control shows why they cannot be promoted into
one merely by combining their check counts or initial bounds.

This calculation concerns the ORIGINAL homogeneous control. It does not
prove the same obstruction at the later registered vortical preparation,
does not establish ill-posedness of its full propagator, and is not an
all-R-tau or all-ITSM no-go. It identifies a failure of a proposed general
inference and a concrete regularity issue for the next energy calculation.

Owners: [frozen screen contract](RES001_RTAU_WEAK_DENSITY_ENERGY_SCREEN_V1_SPEC_2026-11-03.md),
[original complete physical norm](RES001_R4C1_RTAU_PHYSICAL_NORM_V2_REPORT_2026-10-31.md),
[initial weak chart](RES001_RTAU_COMPENSATED_SOURCE_CHART_V1_REPORT_2026-11-03.md),
and [density-sector estimate](RES001_RTAU_COMPENSATED_TRANSPORT_V2_REPORT_2026-11-03.md).

## Reuse the full original generator, including drift

The original scalar physical variables are

    Y=(sigma,kappa*V_z,kappa*du,kappa*dv,kappa*dr,kappa^2*dpsi,
                          Pi_Gamma,Pi_Vz,Pi_u,Pi_v,Pi_r,dpsi_dot).

Here the matter-field perturbations du,dv,dr are the original control's
notation, not the background-velocity symbols in its exported expressions.
The stored generator includes the original physical-map time derivative.
It comes from the complete new R-tau quadratic action, not an old R4C1
propagator. No Hessian or background theorem is rerun or transferred.

Use the original declared initial control

    (a,H,u,v,r,u_dot,v_dot,r_dot,p,psi,rho)
      =(1,sqrt(3469/4620),1,0,1,0,1,1/4,1/5,0,1/5).

Define W=diag(1/kappa,1,...,1) and Yweak=W*Y. Since kappa_dot=-H*kappa,

    Gweak=(W_dot+W*G_Y)*W^-1,
    (W_dot)_00=H/kappa.

In particular Gweak_00=-2H rather than the old -3H. Dropping this extra
drift is explicitly rejected. The nonzero-mode 1/kappa density weight and
the exact Bessel H^-1 weight are uniformly equivalent for kappa>=1/2,
with ratio between 1 and sqrt(5). Low-frequency regularization therefore
does not remove this high-frequency distinction. The torus mean is a
separate retained sector, not identified with the zero-speed branch.

## Keep the quartic branch when taking the ordinary limit

Extract exactly

    Gweak=kappa^2*A2weak+kappa*A1weak+O(1).

The force block A2weak on indices (5,11) remains

    [[0,1],[-5/33,0]],

and is invertible. Its cross blocks vanish at order kappa^2. At order
kappa the ordinary<-fast block vanishes, while the fast<-ordinary forcing
is NONZERO and is retained in the receipt.

For ordinary frequencies lambda=kappa*mu with bounded mu, the inverse fast
block is O(kappa^-2). With ordinary<-fast coupling O(1) and fast<-ordinary
coupling O(kappa), its Schur feedback is O(kappa^-1). Hence it cannot change
the leading ordinary A1weak block. This is the mixed-order Schur limit;
the force pair is not deleted from the system.

The complete ten-variable ordinary polynomial is unchanged:

    lambda^2*(lambda^2+1)^2*(3*lambda^2+1)*(13*lambda^2+14)/39.

But its zero eigenspace changes: algebraic multiplicity remains TWO,
while geometric multiplicity falls from TWO to ONE. Real characteristic
speeds alone therefore miss the adverse result.

## Exact chain and principal-energy obstruction

In ordinary order

    (sigma/kappa,F,U,V,R,Pi_Gamma,Pi_Vz,Pi_u,Pi_v,Pi_r), F=kappa*V_z,

the receipt verifies exact vectors

    r0=(0,-18i,0,0,0,12/11,0,0,0,0),
    r1=(33,0,0,0,0,0,-18i,0,0,0),
    A1weak*r0=0, A1weak*r1=r0.

Both Fourier parities are retained; conjugate negative modes turn these
complex amplitudes into real perturbations. An independent representation
uses D=Pi_Gamma-i*F/198, X=F+18i*D and P=Pi_Vz:

    sigmaweak_dot=0,
    D_dot=kappa*sigmaweak/33,
    X_dot=kappa*(P+6i*sigmaweak/11),
    P_dot=-kappa*X/3.

For the ordinary leading system, r1+kappa*t*r0 is an exact solution.
This is a principal-system statement, not an asserted solution of the
complete variable-coefficient prepared problem.

Suppose a positive Hermitian principal form H0 made this ordinary block
skew: H0*A1weak+A1weak^dagger*H0=0. The chain implies

    r0^dagger*H0*r0=r0^dagger*H0*A1weak*r1
                          =-(A1weak*r0)^dagger*H0*r1=0,

contradicting strict positivity. The independent two-dimensional Jordan
compression forces its first diagonal energy entry to vanish. The full
quartic skew condition also forces its order-zero ordinary/fast energy
cross block to vanish, because A2_fast is invertible; a hidden constant
fast cross term cannot repair this ordinary contradiction.

The original exported positive principal energy gives r0^dagger*H_old*r0=1
and passes both its ordinary and quartic skew identities. It controls sigma
at the original stronger order. There is no contradiction with that theorem.
This screen rejects the density-only weakening as the basis for the usual
uniform order-zero principal energy. It does not rule out every possible
different mixed norm or prove a full propagator instability.

## Evidence and next route

[Executable](../../../Analysis/MasterTests/test_rtau_weak_density_energy_screen_v1.py):
26/26 controls and byte-identical read-only replay COMPLETE. Diagnostic
PASS validates an ADVERSE scientific finding, not physical clearance.
Fresh [receipt](../../../Analysis/MasterTests/outputs/rtau_weak_density_energy_screen_v1_20261103/receipt.json)
SHA256 47aa8a3be990d883402df9e308e99434d6081a9579dbf643c10480736c160569.
All 219 current inherited pins, original control source hashes and snapshotted
sidecar bytes/timestamps are unchanged. No failed run occurred in this version.
Checks are same-author; independent review remains deferred.

Do not build the full coupled-energy claim from the weak static chart alone.
Next retain the physical density strength of the original complete norm,
or derive a genuinely equivalent complete action-observable norm. In the
prepared problem, the full auxiliary observable Z contains metric-gradient
mixing and must be retained with the quartic branch. Test whether an
action-derived periodic normal-form correction can control the surviving
Z_z density forcing without imposing an extra force derivative or deleting
the zero-speed partner. Include coefficient time drift, global means and
the original ensemble. This is a calculation route, not a new action or
physical branch prescription.

The weak-chart component bounds do not need to be rewritten or rehashed;
their full-energy promotion is held by this screen. Original P1/P2 and the
scoped homogeneous R-tau theorem acquire no concrete defect here. Full
prepared physical norm, actual background interval, nonlinear preservation,
interaction window and identifying matching remain incomplete. No a0 or
C_chi prediction follows. No vault mutation/sync, publication, dispatch,
commit/push, deployment or action adoption is included.
