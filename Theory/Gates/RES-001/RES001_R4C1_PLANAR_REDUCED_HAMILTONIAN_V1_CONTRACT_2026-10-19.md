# Frozen contract: full regular-planar constrained Hamiltonian

19 October 2026. Approved unchanged-action Stage-2 continuation. Rule-9
DEFERRED; physics_pass=false; gate_effect=NONE; no physical-window clearance.

## Required movement toward the full objective

Supply the actual nonlinear Hamiltonian whose constrained second variation
is needed for the coupled mode calculation. Do not replace the mode/window
objective with another isolated kinetic sign test, repeat the old G3K-C2
axis audit, or infer physical modes from the previous patch Hessian.
This milestone supplies the reduction, not the missing spectrum/window.

Retain ALL planar metric/frame/Cartesian/radial/force/regulator/dust fields,
potential, curvature, acceleration, lapse flux, both fixed global charges,
all mean metric pairs, and the residual global longitudinal constraint.
Parameter maps/action/scalings unchanged. Never divide at a profile node.

## Exact continuum construction to test

Use normalized coordinate average < >, with physical integrated quantities
obtained by restoring coordinate-cell volume. Spatial metric gauge:
h=[[G(z),m],[m^T,L]], where G is symmetric2x2 and m,L are spatial constants
but genuine time-dependent canonical coordinates. Require h positive definite.
Do NOT remove mean h_xz,h_yz,h_zz as if spatial diffeomorphisms gauged them.

After the original independent unit/dust variations, use psi=tau, s>0.
Keep T's inhomogeneous modes, NOT a simultaneous T=t gauge. Polar variables
R>0,theta replace u,v by an exact finite canonical transformation; this is
the zero-winding phase chart near the original Cartesian initial section.
Fix <p_theta>=Qtheta, <p_T>=Qdust and quotient their global origins only.
The fluctuating phase/dust canonical pairs remain; p_T>0 is required.

At fixed canonical pi_AB and other remaining fields/momenta, define

    S=pi_AB*(G_AB)' + p_Vj*(V^j)' + (p_Vz*V^z)'
      +p_R*R'+p_theta*theta'+p_r*r'+p_Z*Z'+p_T*T'.

The symmetric AB contraction includes BOTH off-diagonal terms. A local
longitudinal inverse exists only if <S>=0. Explicitly handle it: choose
the global-translation chart <sin(k*z)*V_y>=0 with
d=<sin(k*z)*(V_y)'> !=0. Write p_Vy=p_Vy0+lambda*sin(k*z), with p_Vy0
orthogonal to this sine. Then lambda=-<S0>/d solves the residual global
constraint. Its canonical one-form contribution is lambda*d(gauge)=0.
Keep/reject the chart denominator explicitly; never silently subtract a
nonzero mean source. Transverse translation kernels are not inverted.

Let I_z be the zero-mean periodic primitive, applied AFTER <S>=0, and

    rvec=(p_Vx*V_z/2,p_Vy*V_z/2,I_z(S)/2), A=<h^-1>,
    M=(P_mx/2,P_my/2,P_L),
    cvec=A^-1*(M-<h^-1*rvec>), pi_iz=h^-1*(rvec+cvec).

Prove A is positive definite when h is uniformly positive definite, so no
additional mean-momentum singularity is invented. Verify all three actual
spatial constraints and <pi_iz>=M; retain the three mean canonical pairs.

Restore Cartesian momenta and the original six-component metric convention
p_hij=pi_ij on diagonals, 2*pi_ij off diagonal; P_y=(2*p_h,p_V,p_cart)/sqrt(h).
Set psi spatially constant. From the FULL original-action Legendre inverse,

    s=-p_Z/(sqrt(h)*b*V^2),
    H_perp=p_psi*s+E0+Edust+partial_z(F),
    Edust=p_T*sqrt(C(tau)^2+h^zz*T'^2),
    F=gamma*h^zi*p_Vi,
    p_psi=-(E0+Edust+partial_z(F))/s,
    Hpsi=-<p_psi>=<(E0+Edust)/s-F*partial_z(1/s)>.

Do NOT drop the last term because <partial_z(F)>=0. Keep the original
R^-1, phase alignment, potential, spatial Ricci and regulator terms in E0.
Check the exact canonical one-form pullback after all these reductions.
State the formal dimensions: S has mass degree4, I_z(S), metric/frame
momenta and Hpsi density degree3; polar/dust pairs have their own degrees.
No numerical reference chart is promoted to microscopic scale matching.

## Execution, controls and limits

Freeze a versioned executable and source/contract sidecars before execution.
Fresh output and parent-only receipts, bounded Windows-spawn parallel cases
(max16 workers). Standalone optimizer; immutable original-action helpers.
No package installation/global runtime change. Preserve failures and hashes.

Require exact symbolic identities for the constraint solution, mean system,
polar map, clock orientation, origin/translation quotient and flux identity.
Check the original unreduced canonical diffeomorphism/lapse generators and
one-form on n=17,25,33 odd periodic grids for all9 family/eta cases. Use
declared analytic, regular, NODELESS method controls, not replacement ITSM
states. Retain a nonzero mean metric-momentum control, nonzero global
constraint correction, spatial Ricci and clock-weighted flux. Frozen
normalized binary64 tolerance1e-8; grid agreement is diagnostic, not a
continuum Cauchy/constraint-algebra theorem. Exact identities govern.

Use the independently implemented original mpmath density at80 decimal
digits to check all coupled momenta/Legendre energy at one nontrivial point
per case, with the same1e-8 binary64 comparison tolerance. Do not compare a
routine only to itself. Check small gauge/charge-preserving variations for
canonical pullback. Rejection controls: omitted mean metric momenta, global
constraint, lapse flux, curvature, fixed-charge conditions or positive
branch/domain guards. Never claim sampled absence of zeros proves that the
registered w=e*cos(k*z) profile is globally nodeless; it has exact nodes.

Replay the full calculation read-only with exact receipt/sidecar bytes and
sizes/mtimes. Guard inherited sources and previous failed/successful evidence.
Owning report and append-only queue/review entries must distinguish this
regular-planar functional from full arbitrary3D reduction, actual finite-
frequency modes, rank-changing C2/weak persistence and a physical cutoff.

Stage2 remains incomplete and Stage3 unentered. No state adoption/evolution,
new action/parent, smoothing, projection of negative directions, vault write,
manuscript/PDF/site, model/provider dispatch, publication, commit or push.
