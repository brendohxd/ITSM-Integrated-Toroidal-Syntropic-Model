# G1 necessary model: corrected affine Cauchy matching and nodal rejection

29 October 2026. **Conditional; Rule-9 DEFERRED; physics_pass=false;
gate_effect=NONE; G1-G6 INCOMPLETE.**

## Finding and its precise scope

The regular off-node self-similar branch of INNER_BALANCE_V1, with its actual
registered source interval and zero initial field/velocity differences,
develops two nonzero nodal flux jumps at finite positive inner time T.
Both coefficients exclude zero by validated interval bounds. This branch
therefore cannot be glued into a source-free function-valued weak solution
of that necessary model across the node.

This is NOT a full R4C1 weak-solution no-go. The required uniform nonlinear
space-time limit from the original coupled action to this model remains
unproved. No extra nodal source, distributional field, smoothing, different
initial data or future boundary condition is introduced to repair the result.

Earlier no-jump INITIAL current results remain valid: the new jumps are
proportional to T^2 and T^3, so vanish at T=0 with the time derivatives
previously tested. The earlier whole-line Hermite gap also remains valid;
it was never a proof of causal Cauchy compatibility.

## V1 invalidity and V2 correction

The final audit caught an affine-matching error in V1: it connected the full
inhomogeneous state directly to a homogeneous basis without subtracting the
continuing forcing's particular solution. V1's 17/17 receipt is preserved
unchanged, but its connection/jump interpretation is INVALID. The unsealed
draft report/review entry was backed up exactly and prominently annotated;
no live research index adopted its conclusion.

V2 uses the same equations, source, data, precision, orders and matching
point. It checks the exact particular solution in both ODEs and validates
reconstruction of the full state after affine matching. The CORRECTED
coefficients below still exclude zero. See the
[V2 implementation note](RES001_R4C1_INNER_CAUCHY_V2_IMPLEMENTATION_NOTE_2026-10-29.md).

## 1. Cauchy problem actually tested

Let a=4/625, b=5/44, K=3/4, L=9/560000 and S0=-b*Q0. The inherited root
box gives approximately

    -0.000465812306826 < S0 < -0.000452620112661.

For Psi=abs(X)^7*F(s), Z=abs(X)^5*G(s), s=T/X^2, the necessary model is

    K*F'' - b*((1+4*a*s^2)*G''-14*a*s*G'+20*a*G) = S0,
    G+(1+4*a*s^2)*F''-22*a*s*F'+42*a*F = L*s,
    F(0)=F'(0)=G(0)=G'(0)=0.

The implied initial higher jets reproduce the registered source/pole
coefficients; they are not independently adjusted. The denominator
1+4*a*s^2 has no real zero. This four-dimensional linear model Cauchy
solution continues along finite real s without selecting a Fourier boundary
condition. Its finite-time nodal traces require s tending to positive
infinity, not another small-s Taylor fit.

## 2. Controlled connection to the large-s basis

The four indicial exponents are 2,5/2,3,7/2. Each homogeneous basis function
is normalized to leading F coefficient 1. Two modes are exact polynomials:

    F2=s^2-(K+26*b*a)/(420*b*a^2),
    G2=-6*a*s^2+(K+6*b*a)/(10*b*a),
    F3=s^3-(K+6*b*a)/(20*b*a^2)*s,
    G3=K/(b*a)*s.

For each power r, write F=sum f_k*s^(r-2*k), G=sum g_k*s^(r-2*k), with
f_0=1 and g_0=-a*(4*r^2-26*r+42). With rho=r-2*k,

    g_k=(rho+2)*(rho+1)*((K/b)*f_(k-1)-g_(k-1))
          /(a*(4*r^2-18*r+20)),
    f_k=-(g_k+(rho+2)*(rho+1)*f_(k-1))
          /(a*(4*r^2-26*r+42)).

No recurrence resonance occurs after the selected leading exponent. For
rho<=-10, the weighted coefficient norm max(abs(f_k),abs(g_k)/(K/b))
grows by less than 160 per step. The executable proves this bound from
positive polynomial inequalities. At s=16 the all-tail ratio is at most
160/256=5/8. Order128 Frobenius expansions enclose both values and first
derivatives, including the entire tail. The polynomial modes terminate
exactly. This proves convergent large-s representations, not fitted powers.

The exact particular solution is

    Fp(s)=L*s/(20*a)+S0/(840*b*a^2),
    Gp(s)=-S0/(20*b*a).

Its state (Fp,Fp',Gp,Gp') is SUBTRACTED before connection to the homogeneous
basis and added back for a full-state reconstruction check. Its reconstructed
fields are combinations of abs(X)^5*T, abs(X)^7 and abs(X)^5, so it does
not supply a first spatial derivative jump at the node. It must nevertheless
be retained to obtain the correct homogeneous coefficients.

The two independent unit-forcing Cauchy responses (S=1,L=0) and (S=0,L=1)
are transferred from 0 to 16 by sixteen unit interval-Taylor steps:
120 decimal interval digits, order512, analytic disk radius2. Every step
records a rational denominator bound, linear-ODE/Gronwall majorant, Cauchy
tail and enclosing state. The largest local Taylor tail is below 1.24e-79.
The final matching coefficients use an interval residual and Neumann bound,
not the midpoint inverse as evidence. Its matrix norm is below 4.89e-88;
coefficient numerical enclosure errors are below 9.47e-73 for both responses.
The wider physical-input ranges below arise from the root box, not numerical
precision. An independent DOP853 control agrees below 5.70e-12 normalized
error and is not used to set the certificate intervals.

## 3. Actual connection coefficients and flux jumps

Combining both responses with the full S0 interval and fixed L gives

| Leading F power | Enclosed actual coefficient, rounded outward |
|---|---:|
| 2 | [-9.261409, -8.996889] |
| 5/2 | [0.0835370, 0.0862926] |
| 3 | [0.0382909, 0.0393933] |
| 7/2 | [-0.00155683, -0.00151276] |

Call the integer-power coefficients c2 and c3. The convergent half-integer
series become even powers of X near the node at fixed T>0. They cannot
cancel the first spatial derivative jumps of the integer modes. Those modes
give

    Psi = c3*abs(X)*T^3 + terms with no first-derivative jump,
    Z   = -6*a*c2*abs(X)*T^2 + terms with no first-derivative jump.

Since partial_X^2 abs(X)=2*delta(X), the residual of
K*Psi_TT-b*L(Z)-S0*abs(X)^3 has node term

    (12*b*a^2*c2)*T^2*delta(X),
    12*b*a^2*c2 in [-0.000517292,-0.000502517].

The normalized auxiliary residual Z+L(Psi)-L*abs(X)^3*T has node term

    (2*a*c3)*T^3*delta(X),
    2*a*c3 in [0.000490123,0.000504235].

Here the symbol L on the auxiliary forcing denotes the constant9/560000;
L(Psi) denotes the differential operator defined in INNER_BALANCE_V1.
The unnormalized original model auxiliary row multiplies this residual by b.
Each interval excludes zero throughout the inherited source range. These
node sources would be required to support this branch; they are NOT present
in the declared source-free model and are not added to the physical action.

## 4. Consequence and remaining route

Reject source-free function-valued nodal gluing of this regular self-similar
model Cauchy branch. Do not use the nonzero-frequency whole-line inverse to
announce the registered forward solution. Do not erase the failure by
altering S0, selecting a different source or deleting an integer mode.

The missing original nonlinear limit matters: full coupled terms or an
additional nonuniform layer could invalidate the assumed leading expansion.
Neither has been derived. Other model weak classes, uniqueness of a general
non-self-similar weak continuation and all full-action weak continuations
remain outside this rejection. No R4C1/ITSM/T3 all-action conclusion follows.

Next determine whether the original finite-action/current bounds enforce
this model as a sufficiently strong limit to pass nodal fluxes, or identify
the missing leading contribution from the same coupled equations. A defect
measure or extra layer must be action-derived and conserved, not supplied
as a chosen junction source. This is now the substantive domain question;
another initial-trace or Fourier-gap calculation cannot answer it.

## 5. Evidence

Contract: [inner Cauchy V1](RES001_R4C1_INNER_CAUCHY_V1_CONTRACT_2026-10-29.md).
Executable: Analysis/MasterTests/test_01_r4c1_inner_cauchy_v2.py.
Receipt: Analysis/MasterTests/outputs/r4c1_inner_cauchy_v2_attempt_01/summary.json.
SHA256: af69719181338bae198181b7f6ee973cbcfb65a0166e160f206d973e8edfadd3.
21/21 validation checks; no failed/unknown rows; 250 pins; READ_ONLY_REPLAY_EXACT.
The model's physical compatibility test FAILS despite its computational
validation passing. G1-G6, full background/domain/persistence, physical
normalization/window and identifying matching remain incomplete.
