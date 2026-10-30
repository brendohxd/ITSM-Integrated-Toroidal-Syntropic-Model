# G1 near-node time scale and necessary transport model

29 October 2026. **Conditional; Rule-9 DEFERRED; physics_pass=false;
gate_effect=NONE; G1-G6 INCOMPLETE.**

## What is proved and what remains open

The initial auxiliary cusp has a positive, explicitly enclosed node
coefficient independent of the local H and shift terms. Together with the
proved third-time pole, it identifies an initial derivative-ratio scale
proportional to w^2. This is a controlled initial statement, not an existence
time or a physical cutoff. A necessary anisotropic transport model is
identified and checked against the full original initial Jacobi coefficients.
Its whole-line normal Fourier/Hermite problem has no exact nonzero-frequency
level resonance at the registered constants.

The model is NOT an admitted R4C1 background or a causal propagator. Its
metric/constraint completion, uniform original nonlinear space-time remainder,
actual source domain and original Cauchy/junction compatibility remain OPEN.
No formal balance or sampled operator comparison is used to close those gaps.

## 1. Controlled initial source and scale

Keep the registered B1-frame eta=1/4,e=1/500,k=40 and all inherited physical
root/charge/shift data. Delta is the original physical-minus-analytic cubic
bookkeeping partition, not a replacement action. On the initial slice,

    aPsi=-3*H*p+HB*p+T*wprime*p-U-W*w^2+Rprime*p,
    p=1/20, T=R/w, Rprime=T*wprime+w*T_z.

Substituting this coupled scalar acceleration into the exact parent
auxiliary cusp quotient cancels H and the shift in its node value:

    Q0 = lim Delta(aZ)/abs(w)
       = (A*p/b)*(3*p*HB+6*U+2*beta*p^2),
    S0 = -b*Q0,
    A=1/28, b=5/44, beta=1/40.

HB is the registered background input, not an independently fitted
observational Hubble coefficient. This result does not identify K_Q or C_chi.
The certified restricted root box gives

    0.003983056991420032 < Q0 < 0.004099148300068451.

The exact finite-w quotient identity, with all complement responses retained,
is

    Delta(aZ)/abs(w)-Q0
      = (C_y^T*r_y)/(b*w^3)+(6*A*p*W/b)*w^2
        -(3*A*p^2/b)*w*T_z.

Use the sealed CF,Ma,T_z bounds, not a fitted normal power. It follows that

    abs(Delta(aZ)/abs(w)-Q0) <= C_Q*abs(w),
    C_Q < 0.003701036048289, 0<abs(w)<=1/1000.

In particular this cusp acceleration is positive on that entire frozen
neighborhood. Combine with the auxiliary pole remainder on its proved
smaller range 0<abs(w)<=2^-27. Exact rational bounds in the receipt imply

    25.0338035887013*w^2
       < Delta(aZ)/Delta(jZ)
       < 77.2903388377192*w^2.

This ratio compares INITIAL derivatives in the declared dimensionless chart.
It does not bound future derivatives or justify any finite time step. The
shrinking scale motivates t=epsilon^2*T; it does not impose an observational
cutoff or make an isolated Fourier grid a continuum solution.

## 2. Necessary inner balance with retained coupled directions

Put w=epsilon*X, t=epsilon^2*T. The cusp balances suggest

    Delta Z=epsilon^5*Z_inner,
    Delta psi=epsilon^7*Psi_inner,
    Delta V_i=epsilon^6*V_i_inner.

All six metric components, condensate/radion, clock/multiplier, three shifts
and lapse remain in the initial Jacobi comparison. Their weights are
h6:7,V3:6,u/v/r:7,psi:7,Z:5,tau:9,epsilon_multiplier:3,S3:6,N:7.
All six coefficient types are inspected in the original twenty-row chart.
The five necessary scalar/auxiliary/frame rows have the following leading
template, with sigma=wprime(node)=+/-2/25 and

    L = X^2*partial_T^2 + sigma^2*partial_X^2,
    E_density=2*A*p^3*abs(X)^3,
    K=3/4:

    K*Psi_TT - b*L(Z) = S0*abs(X)^3,
    Z + L(Psi) + p*X*V_y,T + p*sigma*V_z,X = 0,
    V_y,TT=-(9/28000)*X*abs(X),
    V_x,TT=V_z,TT=0.

The clock/lapse leading relations retain E_density,T=0 and
Theta_T=N_inner+beta*Psi. The density term is included ONCE in S0. For
zero leading initial V_z,V_z,T, its zero leading solution follows from its
equation; the normal-frame divergence term is not deleted from the template.
The actual original finite-w auxiliary potential, frame-time coupling,
normal-frame divergence and scalar-Z time drift are independently checked.

The four existing full-Jacobi node orientations have maximum scaled-template
deviation below 4.35e-10, at abs(w) approximately 2e-5. This is a numerical
implementation control, not a uniform operator-error theorem or a claimed
convergence order. The remaining twelve metric/phase/shift rows and the
full nonlinear constraints are not solved by this template. An evolving
background remainder has not been bounded.

The leading initial jets reproduce the independent parent values:
Psi_TTT(0,X)=(9/560000)*abs(X), and the auxiliary third-time cusp coefficient
is (K/b)*(9/560000)=297/2800000. These coefficients were derived from the
registered action/kinetic response before the comparisons; no target fit.

## 3. Retain the auxiliary potential and coefficient commutators

With zero leading initial frame data,
V_y=-(9/56000)*X*abs(X)*T^2 and V_z=0. Eliminating Z gives the necessary
fourth-order model

    [L^2+(33/5)*partial_T^2] Psi
       = (S0/b)*abs(X)^3
         +6*(9/560000)*(4/625)*abs(X)*T.

The +Z term in the auxiliary equation is retained: it has leading inner
order even though it is lower order in a fixed-point high-frequency symbol.
Likewise L^2 cannot be replaced by its frozen constant-coefficient square:

    L^2 = X^4*partial_T^4
          +2*a*X^2*partial_T^2*partial_X^2
          +4*a*X*partial_T^2*partial_X
          +2*a*partial_T^2+a^2*partial_X^4, a=4/625.

The two coefficient-derivative terms are leading here. Exact commutation
with partial_T gives the diagnostic factorization

    L^2+(33/5)*partial_T^2
      = (L+i*sqrt(33/5)*partial_T)(L-i*sqrt(33/5)*partial_T).

This is an algebraic factorization, not a choice of physical complex fields
or a causal boundary condition.

## 4. Nonzero-frequency model gap, with its domain restrictions

Only for the local whole-line normal model, Fourier transform T. At real
omega!=0, L_omega=a*d_X^2-omega^2*X^2. Rescaling X gives the Hermite
oscillator eigenvalues -sqrt(a)*abs(omega)*(2*n+1). The ordinary Hermite
normalization/ODE is documented by [NIST DLMF 18.3](https://dlmf.nist.gov/18.3)
and [18.8](https://dlmf.nist.gov/18.8); the executable independently verifies
the ground state, all-level raising commutator and nearest-level identities.

The FOURTH-order model level coefficients are therefore

    [a*(2*n+1)^2-33/5]*omega^2,
    a*(2*n+1)^2-33/5 = [4*(2*n+1)^2-4125]/625.

For n<=15 these coefficients are at most -281/625. For n>=16 they are at
least 231/625. Monotonicity and exact polynomial factorizations prove the
all-level absolute gap 231/625; this is not a truncated level scan. On finite
orthonormal Hermite spans,

    norm(u) <= 625/(231*omega^2)*norm(P_omega*u).

The opposite signs of the nearest levels are retained. An absolute gap does
not imply positivity, stability or a ghost-free action. No minimum omega,
physical EFT window or observable spectrum is inferred. Omega=0 remains a
separate sector. The source abs(X)^3 is not globally L2 on this normal line;
this estimate cannot simply be applied to it without justified matching or
localization and all induced commutators. This local whole-line model is not
the original compact torus, and no original zero mode/charge/mean is removed.

Most importantly the Fourier inverse would require a temporal domain and
boundary prescription. It is not automatically a forward Cauchy solution
with the actual initial data. No such prescription is adopted here.

## 5. Evidence and next gate

Contract: [inner balance V1](RES001_R4C1_INNER_BALANCE_V1_CONTRACT_2026-10-29.md).
Executable: Analysis/MasterTests/test_01_r4c1_inner_balance_v1.py.
Receipt: Analysis/MasterTests/outputs/r4c1_inner_balance_v1_attempt_01/summary.json.
SHA256: 4802390fc31a255135c339af0fa8efbe7a53166d245834ef06586ae2ee9d81f0.
52/52 checks, no failed/unknown rows; 243 source pins; READ_ONLY_REPLAY_EXACT.

Next test the necessary model against its actual Cauchy data and finite-time
nodal flux/junction requirements before using its gap as an inversion route.
A solution must also have the full metric/constraint completion and a uniform
remainder in the original evolving equations. A formal model solution alone
does not satisfy G1 or G3. Those objectives, physical normalization/window,
identifying matching and numerical prediction remain incomplete. All older
proofs, failed attempts, sidecars and manuscript/publication states remain.
