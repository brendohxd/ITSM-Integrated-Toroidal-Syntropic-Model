# Actual initial ordinary principal energy from the longitudinal Ward identity

4 November 2026. Conditional component of the
[prepared coupled-energy contract](RES001_RTAU_PREPARED_COUPLED_ENERGY_V1_CONTRACT_2026-11-04.md).
R-tau is still an UNADOPTED comparator. Original R4C1 and G1-G6 requirements
are unchanged. Review DEFERRED; physics_pass=false; gate_effect=NONE.

## Result, scope and remaining wall

The leading trace-kinematic identity is now derived EXACTLY from the
declared action, including arbitrary frame tilt. It is no longer supported
only by the ordinary strong-graph V1 interval consistency test.

On the WHOLE registered initial-root enclosure, the ordinary action-energy
complement is coercive and its generator is invertible. Retaining its
zero-speed partner gives an explicit positive FROZEN PRINCIPAL energy for
all 18 ordinary directions. This extends beyond the previous off-shell
reference control. It does not extend beyond the principal scope below.

The sufficient relative bounds are

    temporal normalized perturbation <0.094789435,
    action-energy complement perturbation <0.539715,
    normalized complement-inverse perturbation <0.919581 <1.

An explicit, deliberately conservative full ordinary norm estimate is

    1.07346e-7 * |Y|^2 <= E_ordinary(Y) <= 4.580380e6 * |Y|^2,

where Y=(w,Q8,P9), Q has the eight independent gradient-scaled ordinary
configurations and P all nine ordinary canonical momenta. Both zero-speed
directions are retained. These constants are momentum independent; their
large ratio is an estimate, not a measured instability or propagation rate.

**Scope:** the initial local frozen ordinary principal symbol in the
principal spatial-metric gauge, with common background advection removed.
Coefficients range over the full exported prepared-root enclosure, not a
finite set of sample points. The action's stationary elimination of shift
gradients is retained. The result restricts to compatible global tangents;
it does not prove that an arbitrary local amplitude tuple has a global
charge/range completion. No unproved freedom of such tuples is needed for
the local action identity.

**Still open:** the force/auxiliary quartic pair and its cross-sector mixing;
the actual variable-coefficient operator, spatial commutators, T_dot,
G_dot, gauge/range drift and all global symplectic/harmonic partners; a
preserved background-domain tube; nonlinear interactions and a physical
validity window. This is NOT acceptance of the full coupled-energy
contract, a finite-time PDE theorem, a canonical ghost clearance or a
demonstration of ITSM phenomenology.

## Exact action identity, before any inverse or interval bound

Freeze a point of the conformal initial slice and use orthonormal material
derivatives temporarily. Keep arbitrary K_ij, spatial frame derivatives
D_i V^j and normal frame velocity X^i. Write the pinned normalized-frame
derivative tensor as

    a=X+K V,
    B_00=V.a/gamma, B_0j=a_j,
    B_i0=V.D_i V/gamma+(K V)_i,
    B_ij=D_i V^j+gamma*K_ij.

Consider the simultaneous derivative variation

    delta(D_z Vz)=gamma*e, delta(Sz_z)=e,
    delta K_zz=-e, delta X_z=Vz*e.

All other independent derivative entries are held fixed. This is a
directional algebraic identity, not a restriction imposed on a physical
mode. The full a variation vanishes. In B_z0 the two changes are Vz*e and
-Vz*e; in B_zz they are gamma*e and -gamma*e. Every other component is
unchanged. Thus all 16 components of B and its acceleration contraction
are invariant. All normalized-frame kinetic invariants are invariant,
including their c1,c2,c3,c4 coefficients; no alignment is assumed.

The ADM term alone supplies

    delta[MP2*(tr K^2-(tr K)^2)/2]
        =MP2*(K_xx+K_yy)*e.

There is no quadratic-in-e remainder. The spatial-curvature term is
independent of this direction. The ordinary scalar, alignment, force and
R-tau clock-spatial regulator terms have no D_z Vz or shift-gradient
derivative along it: normal scalar velocities involve the shift itself,
not its gradient. Those sectors are retained, not removed from the action.

Restore the actual initial h=a^2 I and lapse N. Orthonormal metric normal
derivatives are material h_t/(N*a^2), frame spatial derivative is D_z Vz,
and shift-gradient variation is N*e. Multiplication by N*a^3 gives

    gamma*L_(D_z Vz)+N*L_(Sz_z)
        =a*MP2*(v_hxx+v_hyy)/2.

Here v is the material ordinary field velocity. This scaling restores N
and a explicitly; it is not an assumption of conformal future evolution.
After stationary Schur elimination of the full shift-gradient block,
L_(Sz_z)=0 at principal order. With t=(1/2,0,1/2,0,...), this gives

    Brel[:,Vz]=(a*MP2/gamma)*t,
    Grel[:,Vz]=Grel[Vz,:]=0.

The registered MP2=1 is read from the immutable parameter source. For
c=gamma/(a*MP2), the exact trace lift is

    X=k*delta qordinary=E*Q+i*c*vtrace*P_Vz,
    vtrace=(1,0,1,0,0,0,0,0,0).

Since Pdot/k=-i*Brel^T*v+Grel*X, the identity proves

    (v_hxx+v_hyy)/2=i*c*(Pdot/k)_Vz.

Thus the principal trace graph is preserved for arbitrary local ordinary
derivatives. This is an action proof, not a replacement of an uncertain
interval residual by zero. The original exported B/G enclosures are also
checked separately for consistency with it. The identity concerns leading
derivatives; lower-order graph, constraint and ensemble transport remain
in the full owning contract.

## Action energy and the retained zero-speed partner

For frozen real symmetric M,Grel and real Brel, the canonical rows are

    v=M^-1*(P-i*Brel*X),
    Pdot/k=-i*Brel^T*v+Grel*X.

The unrestricted canonical quadratic form is

    Hcan=(P-i*Brel*X)^* M^-1 (P-i*Brel*X)-X^*Grel*X.

Its derivative is zero: the G terms cancel and the remaining expression
is the real part of -i*v^*(Brel+Brel^T)*v. The proved trace identity makes
the constrained X reconstruction obey Xdot/k=v, so the same conservation
identity holds on the strong trace graph. This is a frozen-coefficient
identity only; coefficient and basis derivatives have not been set to zero
in the actual evolving problem.

The exact ordinary stationary direction has

    Q_Vz=-2i*c, P_hxx=P_hyy=1,

and all other entries zero. Its kinetic combination and gradient energy
both vanish. It is retained as a coordinate, not deleted as gauge. Define

    z=i*Q_Vz/(2c),
    x_Q=Q with Q_Vz omitted from the complement,
    x_Pxx=P_hxx-z, x_Pyy=P_hyy-z,
    x_Pother=P_other.

This invertible change separates z and a 16-dimensional complement x.
The local principal generator has the exact block form

    zdot/k=b*x, xdot/k=C*x.

The coercive restriction Hcan(x) is conserved. Certified invertibility of C
allows the stationary coordinate

    zeta=z-b*C^-1*x.

Keep density w as the second zero-speed coordinate. Its zero principal row
uses the completed strong-density source estimate, whose bounded lower-order
terms remain required. The positive ordinary principal energy is

    E_ordinary=|w|^2+|zeta|^2+Hcan(x).

No numerical eigenvector fitting or choice of weights to obtain desired
speeds enters this construction. A positive controlling energy obtained in
this way is not a positivity theorem for the entire canonical Hamiltonian.

## Whole-root certificates and explicit norm constants

Reuse the immutable mixed Hessian and certified shift inverse. Whiten the
temporal Schur complement before subtraction and use the certified inverse
of I+E_M, ||E_M||_2<=delta_M<0.094789435. Whiten the action-energy complement
by its exact rational-reference energy W_h. The reference normalized
generator is exactly skew-adjoint with minimum squared frequency 1/3,
so its inverse 2-norm is sqrt(3). No midpoint spectrum is substituted.

The direct expanded interval calculation in V2 gave sufficient errors
1.727798885 and 1.730869986, both inconclusive. V3/V4 retain that result and
bound the same quantities in factored form. Let

    Cnormal=U*(I+E_M)^-1*V+Z,
    U=W_h^-1*F*W_m, V=W_m^T*K*W_h,
    K=P-i*Brel*X.

With reference operator norms u0,v0 and outward difference bounds
dU,dV,dZ,dGrad, use

    dH <= (v0+dV)^2*delta_M/(1-delta_M)
                               +2*v0*dV+dV^2+dGrad <0.539715,
    dC <= dU*(v0+dV)/(1-delta_M)
          +u0*delta_M*(v0+dV)/(1-delta_M)+u0*dV+dZ,
    sqrt(3)*dC <0.919581.

All norms are bounded by explicit Frobenius or sqrt(one*infinity) bounds.
The inverse certificate uses a consistent Euclidean two-norm throughout.
These are bounds over the whole initial enclosure, not target fits.
They yield conservative complement constants

    0.01336341043416*|x|^2 <= Hcan(x) <= 47.67695112071*|x|^2,
    ||Cnormal^-1||_2 <21.537676,
    ||b*C^-1||_2 <72.569179.

For Y=(w,Q8,P9), the exact coordinate change F*Y=(w,z,x) has

    ||F||_F^2=17+3/(4c^2),
    ||F^-1||_F^2=19+4c^2.

The further zeta shear and these bounds give the full ordinary estimate
at the top of this report. Its exact outward endpoints are stored in the
receipt. The leading full gradient reconstruction also obeys

    |Y|^2 <= |w|^2+|X|^2+|P|^2
          <= max(2,1+2*c_max^2)*|Y|^2.

Thus no trace gradient or ordinary momentum is hidden by the coordinate
norm. The exact global Green reconstruction and its lower orders are not
proved by this leading-order equivalence. The algebra applies to signed
nonzero k; no Fourier parity is discarded. The torus zero mode remains a
separate finite-dimensional/global problem.

## Evidence, implementation history and preservation

Executable: `Analysis/MasterTests/test_rtau_ordinary_ward_energy_v4.py`.
[Frozen V4 criteria](RES001_RTAU_ORDINARY_WARD_ENERGY_V4_SPEC_2026-11-04.md).
Receipt: `Analysis/MasterTests/outputs/rtau_ordinary_ward_energy_v4_20261104/receipt.json`.
SHA256:

    19c3a5ef90791c0d0619d7664337c42724f97136788c1dc7202dc662b337af50

31/31 bounded controls and byte-identical replay COMPLETE. Controls include
all 16 frame tensor components, acceleration, ADM and lapse/volume scaling,
source-definition checks, a separate generic canonical-energy identity,
exact reference complement and full-18 energy cancellations, invertible
zero/complement charts, original enclosure consistency and all input pins.
Checks remain same-author evidence, not independent review clearance.

Preserved V1 stopped in the interval library's complex conjugation before
producing an energy result. V2 used explicit Re(z)-i*Im(z), preserving its
equations and producing the inconclusive expanded bounds. V3 factored those
bounds without changing the action or acceptance. V4 completed ordinary
norm constants and made the inverse norm convention explicit. V2, V3 and
V4 all replay byte-identically. No old failed attempt or sidecar was edited.
All 219 original pins and snapshotted source/sidecar bytes and timestamps
are unchanged. No action Hessian was rerun.

## Next supported calculation

The previous candidate trace identity is resolved at leading action order.
Continue the same coupled-energy contract with the retained quartic pair:
derive and control its coupling to this ordinary energy, including the
metric part of the auxiliary observable and actual shift/gauge/constraint
reconstruction. Then bound the full spatial and time-dependent remainder,
including the zero-charge coordinate's coefficient derivatives and global
partners. A pointwise principal symmetrizer is useful input to that task,
not a substitute for it or for actual background-domain persistence.

The domain-first goal remains ACTIVE. Full mixed energy, a time tube,
interactions/window, genuinely identifying matching and dependent numerical
predictions remain incomplete. No paper or website claim is promoted by
this component. No action adoption, vault write/sync, provider dispatch,
publication, commit, push or deployment occurred.
