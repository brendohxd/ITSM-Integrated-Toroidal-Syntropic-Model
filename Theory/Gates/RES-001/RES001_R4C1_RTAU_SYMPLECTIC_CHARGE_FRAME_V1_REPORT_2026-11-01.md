# Prepared R-tau initial symplectic chart and global charge frame

1 November 2026. Conditional comparison; review DEFERRED.
physics_pass=false; gate_effect=NONE; R-tau unadopted; G1-G6 incomplete.

## Result and necessary interpretation

The coupled canonical inverse now supports an explicit initial weak
two-form in current-density coordinates, retaining the harmonic metric
moduli, weighted momenta and all cross terms. The global clock/phase and
residual-translation directions have a nonzero root-uniform response
determinant. Thus their initial tangent roles can be distinguished rather
than guessed from a kinetic sign or zero characteristic speed.

After spatial coordinate reduction, the fixed-I/Q tangent level has
presymplectic characteristic directions X_I and X_Q. The clock identity
H0=-I makes X_H0=-X_I the physical unit-clock evolution. Quotienting this
direction as if it were coordinate gauge would remove the evolution being
studied. The correct next calculation uses the surrounding spatially
reduced canonical Hamiltonian, with flow tangent to the declared charge
levels. No new physical ensemble is adopted by using off-level derivatives
to define that Hamiltonian vector field.

This establishes an INITIAL LINEAR weak chart and charge classification,
not a quantitative prepared evolution generator or physical energy norm.
The nonlinear constraint manifold, finite-time persistence and interaction
window remain unproved. The zero-speed and indefinite-gradient-energy
warnings remain substantive; they are not removed by charge bookkeeping.

Owner: [prepared-Cauchy contract](RES001_R4C1_RTAU_PREPARED_CAUCHY_V1_CONTRACT_2026-10-31.md).
Use the [actual coupled inverse](RES001_R4C1_RTAU_COUPLED_PERIODIC_INVERSE_V1_REPORT_2026-11-01.md),
[canonical graph](RES001_R4C1_RTAU_CANONICAL_DENSITY_GRAPH_V2_REPORT_2026-11-01.md),
[mixed two-form](RES001_R4C1_RTAU_MIXED_OPERATOR_V4_REPORT_2026-11-01.md)
and [clock identity](RES001_R4C1_RTAU_CLOCK_IDENTITY_V2_REPORT_2026-11-01.md).
The [charge-frame contract](RES001_R4C1_RTAU_SYMPLECTIC_CHARGE_FRAME_V1_CONTRACT_2026-11-01.md)
was frozen before execution.

## Auxiliary, coordinate and harmonic sectors

The independent auxiliary pair is p_Z=0 and
E_Z=b*N*sqrt(h)*(Z+Delta psi)=0. The coefficient b*N*sqrt(h) is nonzero
on the declared positive branch. Eliminating this pair contributes no
delta Z wedge delta p_Z term and does not flatten the other sectors.
The original lapse/multiplier/clock reconstruction remains in force.

At this fixed initial slice use the already established compatible spatial
gauge and its fixed pullback J=a/Abar. Its harmonic metric variations are

    delta h_xz=J*delta m_x,
    delta h_yz=J*delta m_y,
    delta h_zz=J^2*delta m_z.

Their conjugate momentum variations are

    delta Pi_x=average(J*delta p_hxz),
    delta Pi_y=average(J*delta p_hyz),
    delta Pi_z=average(J^2*delta p_hzz).

These are not simply the original-coordinate means eta_i used to label
the coupled inverse. At fixed configuration before replacing trace by
density, the eta-to-Pi factors are positive. With ell=1/13000 they are

    transverse: 1/I0(2*ell),
    longitudinal: 1/I0(ell)^2,

where I0 is the modified Bessel function. Conservative positive enclosures
are exp(-4ell) to exp(4ell), and exp(-2ell) to 1 respectively. The actual
density inverse also makes Pi depend on density/free-field inputs; those
cross terms must remain. Harmonic metric or momentum data are not deleted.

Write delta hxx=a^2*f+d, delta hyy=a^2*f-d, P=delta p_hxx+delta p_hyy
and p_d=delta p_hxx-delta p_hyy. The initial spatially reduced two-form is

    Omega(1,2)=average[a^2*(f1*P2-P1*f2)
      +d1*p_d2-p_d1*d2+hxy1*p_xy2-p_xy1*hxy2
      +sum_frame/scalars(q1*p2-p1*q2)]
      +sum_i(m_i1*Pi_i2-Pi_i1*m_i2).

The reconstructed eliminated momenta and trace are the actual nonlocal
solutions of the owning inverse. Substituting them into this formula is
the complete initial pullback. A future moving gauge changes the map and
must be transported; it is not assumed frozen by this fixed-time formula.

The nonzero-mode spatial gauge inverse was established by the owning gauge
calculation. Constant x/y translations act trivially on the planar stratum.
The residual longitudinal translation acts nontrivially and has its actual
momentum compatibility; it is not a new physical mode. The origin witness
below makes its linear coordinate quotient regular without imposing a
reflection restriction on general perturbations.

## Density block, adjoints and weak normalization

Let G=L^-1 be the certified coupled trace inverse. At fixed other inputs,
the density/trace-momentum block of the two-form is

    K=G^* multiplication(a^2).

When f also depends on momenta, its pullback creates momentum/momentum and
other cross blocks. For an abstract linear embedding
(f,P)=(G*r+C*P,P), the momentum/momentum block is
C^* multiplication(a^2)-multiplication(a^2)*C. The actual graph and moduli
terms must all be substituted, rather than retaining K alone.

For the longitudinal momentum map put w0=1/a, w=w0/average(w0),
P_b=p_hxx+p_hyy for the BACKGROUND and R=a*(lambda_z*P_b-P_b,z)/2. Then

    T_z=(I-w*average)*(P_b/2+w0*Dinv*P0*R),
    T_z^*=(P_b/2-R*Dinv*P0*w0)*(I-1*average(w* .)).

Multiplications act in the displayed order. The antiderivative is skew
adjoint on the mean-free circle. Likewise

    T_x^*=-p_hxz+p_hxz*average(a^-2* .)/average(a^-2),

and similarly for y. Thus the full scalar inverse adjoint uses

    L^*=partial_z^2 multiplication(A2)
          -partial_z multiplication(A1)+multiplication(A0)
          -T_x^* multiplication(Rvel_hxz)
          -T_y^* multiplication(Rvel_hyz)
          -T_z^* multiplication(Rvel_hzz),
    G^*=(L^*)^-1.

Variable-coefficient derivatives and weighted means are essential. The
periodic Green identity is verified with its complete boundary divergence;
that divergence vanishes only after periodic integration.

The principal density block is

    K ~ a/(N*k^2),
    0.99989638596212 < k^2*K_principal < 1.00010362477486

throughout the certified initial-root ball. This is derivative order -2,
not a constant canonical normalization. The density column is smoothing
on flat L2 coordinates; a bounded strong symplectic inverse on an
unweighted L2 product does not follow. The appropriate weak/Sobolev pairing
and the physical mixed derivative counts must be retained. Finite charge
constraints cannot remove all these nonzero-harmonic directions.

The inherited Neumann representation gives an analytic 64-term remainder
bound below 2.991e-17 for the density pairing block in the L2 bilinear norm.
This is an operator-tail estimate, not a claim that a finite Fourier
evolution or 64 explicit PDE iterations were run.

## Clock Hamiltonian and the actual global frame

With p=Lbar_v and Rvel=v-Lie_S q, the action gives

    I=integral(Lbar-p*Rvel),
    integral(p*Lie_S q)=-integral(S*E_S),
    H_total=H0-integral(S*E_S), H0=-I.

The spatial improvement integrates to zero on the torus, but remains in
the local density chart. For Omega=dq wedge dp, the clock Hamiltonian
vector is X_H0=-X_I. On a fixed-I level it obeys
Omega(X_H0,delta)=-delta I=0 while remaining a nonzero physical time flow.
Treating this characteristic direction as pure coordinate gauge would
turn the Cauchy problem into a space of time orbits, a different task.

For regularity witnesses use normalized physical volume V=average(sqrt(h)),
phase average B=average(v), and origin A=average(u*sin z). These witness
directions; no phase or time gauge is adopted. Columns are the flows
X_I, X_Q and residual constant-adapted-coordinate translation X_P. At the
prepared data the response matrix has the pattern

    [ negative_nonzero, 0, 0 ]
    [ finite,          1, 0 ]
    [ 0,               0, negative_nonzero ].

The zeros follow from spatial invariance and the certified background
reflection signature, not from a restriction on allowed perturbations.
The exact profile responses are

    X_I V=-3*average(a^3*(H+epsilon*cos(2z)/31)),
    X_P A=-(epsilon/17)*average(sin(z)^2/J),
    X_Q B=average(u)=1.

The periodic Lie-shift volume divergence cancels in the first integral.
Root-uniform magnitude bounds give

    |X_I V| >2.59884466,
    |X_P A| >2.94072401e-5,
    |det response| >7.64248491e-5.

The residual origin is therefore a regular coordinate direction. The
clock and phase charge differentials remain independent after spatial
reduction. The action's internal U(1) invariance gives {I,Q}=0; spatial
invariance gives commuting residual momentum/charge observables. On the
regular initial spatial quotient, the fixed-I/Q tangent level consequently
has characteristic span(X_I,X_Q), by canonical duality and finite-codimension
annihilation. No additional fieldwise null is inferred from fixing these
two global charges. In particular a zero characteristic SPEED at k!=0
is not thereby coordinate gauge.

For defining the Hamiltonian vector field one can retain I/Q values as
mathematical transverse parameters. The prior inverse already controls
the mean block for arbitrary current source, and average(u)=1 controls
the phase-charge mean. Actual physical evolution still lies on the
operator-declared fixed-charge level. This is not a new ensemble choice,
automatic phase Routh quotient or permission to quotient physical time.

## Evolution formulation and what has not been calculated

If y is the spatial canonical tangent and Y=T(t)*y the actual density/gauge
chart, its generator and two-form must obey

    G_Y=(T_dot+T*A_can)*T^-1,
    Omega_Y=T^-* Omega_can T^-1,
    Omega_Y_dot+G_Y^* Omega_Y+Omega_Y G_Y=0.

The chart derivative is not an isospectral optional term. For the coupled
Green operator G_dot=-G*L_dot*G. Global charge rows and charge-flow vectors
must also be transported with the background; their initial membership
in a kernel does not justify repeatedly projecting out their evolution.

For the next actual generator calculation, use the more direct action
route where possible. The exact local clock equation supplies

    delta I_dot=partial_z[S^z*delta I+I*delta S^z
                       +delta(N*sqrt(h)*F^z)].

Express its explicit current, field velocities and canonical momentum
equations through the certified inverse, auxiliary secondary relation and
gauge-velocity solve. This incorporates density-map drift through the
equations, rather than silently omitting it or requiring an unnecessary
large third-derivative expansion. Compare with the transport identity in
its actual registered scope. The prior initial spatial-gauge velocity
change must be applied consistently to qdot, shift and momentum-density
flow; it is a coordinate change, not a physical zero-shift prescription.

The quantitative prepared generator, its physical norm and any finite-time
bound are NOT computed by this report. Constraint-graph curvature, moving
projectors, moduli/charge sectors and the zero-speed branch remain in that
task. Do not claim evolution merely from the initial weak chart.

## Verification and disposition

[Executable](../../../Analysis/MasterTests/test_01_r4c1_rtau_symplectic_charge_frame_v1.py):
25/25, exact immutable replay COMPLETE.
[Receipt](../../../Analysis/MasterTests/outputs/r4c1_rtau_symplectic_charge_frame_v1_attempt_01/summary.json)
SHA256 cd40137244f6969a8ba737e26a684721e89d9ea8b40bd5263769baa18e743a13.
Root-uniform frame bounds use the certified H ball and fixed profiles.
Independent 64/128-point profile sums match the Bessel identities below
1e-100, against frozen 1e-40. Exact algebra rejects omitted coefficient
derivatives, weighted mean adjoints, antiderivative signs, momentum cross
blocks and chart time derivatives.

The finite rational matrix and oscillator examples in the executable are
explicit algebra controls of adjoint/pullback/transport formulas. They are
not substitutes for the continuum proof, actual prepared spectra or a
physical finite-mode evolution run. The field-level statements use the
action's Legendre/Noether identities and certified functional inverse.
Same-author checks are not independent external review.

No concrete manuscript defect or identifying microscopic input is supplied.
Transverse modes, nonlinear admission/persistence, interactions/validity
window, GR/local compatibility and matching remain open. The original
unchanged R4C1 is not repaired or promoted. Goal ACTIVE and incomplete;
review DEFERRED; physics_pass=false; gate_effect=NONE. No paper/site change,
action adoption, external dispatch, vault mutation, publication or commit/push.
