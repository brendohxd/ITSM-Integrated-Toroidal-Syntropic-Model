# R4C1: a controlled infinite odd-mode lower response

17 October 2026. Master Test1 / RES-001 / unchanged-action Stage2.
Claim Conditional. 199/199 local controls; exact read-only replay passed.
Review DEFERRED, Rule9_cleared=false, physics_pass=false, gate_effect=NONE.

## What changed

The lower transverse cusp response now has a continuous-time, infinite-mode
tail estimate. Earlier CUSP3 evolution sampled the lower modes1,3 alongside
the mean/first even coupled outputs. This result bounds every omitted odd
lower mode analytically, rather than adding another finite sample.

It does not yet bound the full order-|e|^3 coupled response or the all-order
nonlinear remainder. The complete mean, metric/frame, matter/dust and regulator
equations are not replaced by this transverse component estimate.

Scope: leading w(t)*cos(40z), w(0)=1,w_dot(0)=0; zero initial lower response.
All three unchanged families, exact eta=1/4,1/64,1/1024, original homogeneous
initial prescription and time[0,1/20] in action reference units. This is the
same leading waveform as CUSP3, not the different cos+(cos3)/3 G3N4 probe.
No eta=0, arbitrary waveform/background/direction or physical cutoff theorem.

## Action binding and continuous background

The generic mass/speed and lower wave equation are bound to the accepted
planar action and CUSP3 source implementation. The source coefficient is a
COMPLEX Fourier coefficient; cosine amplitudes would be twice as large.

For n odd, either sign,

~~~text
r_n_ddot+3H*r_n_dot+[cV2*(40*n/a)^2+mV2]*r_n = F(t)*c_n
F(t) = -3*A*abs(psi_dot)^3*w*abs(w)/f2
c_n = -4*sin(n*pi/2)/[pi*n*(n^2-4)].
~~~

All other n have zero lower source. This does not eliminate the nonzero
even/mean sources at the next order. In particular c_5=-4/(105*pi) is nonzero.
The formula is inherited; the continuous response/tail bound is new.

The exact action coefficients give

~~~text
f2=eta/6, K_Q=3eta, A=2eta^(3/2)/7, zeta=eta/13,
mV2=2H^2+B*Hdot-18*psi_dot^2+(6/13)*J^2,
J=u*v_dot-u_dot*v,
B=(-3c2-c3+c4)/(c1+c4).
~~~

For all nine cases, cV2>=1/10, MC>=3/4 and |B|<=2. The homogeneous energy,
Friedmann and dust-charge identities are checked exactly. The original
positive potential and initial energy<1 imply kinetic+rho<2 and J^2<=4.
The bootstrap gives H in[1/5,1], a in[1,20/19] and
eta/10<=psi_dot<=eta/5 through t=1/20. Thus

~~~text
|1-mV2| <= 1+2+8/3+18/400+24/13 < 8.
~~~

These are proof bounds on the continuous background, not sampled extrema.
V and K_Q here are declared R4C1 inputs, not microscopic MAT matching results.

## Complete modified-wave energy

Define the positive mathematical energy

~~~text
E_n = |r_n_dot|^2+[cV2*(40*n/a)^2+1]*|r_n|^2.
~~~

The exact derivative retains momentum/background drift and the mass coupling:

~~~text
E_n_dot =
  -6H*|r_n_dot|^2
  -2H*cV2*(40*n/a)^2*|r_n|^2
  +2Re[(1-mV2)*conj(r_n_dot)*r_n]
  +2Re[F*c_n*conj(r_n_dot)].
~~~

Since H>0 and the position weight is at least1, Cauchy/Young gives
E_n_dot<=8E_n+2*|F*c_n|*sqrt(E_n). The same calculation applies to the leading
unsourced wave. Its initial position weight and a<=20/19 yield
|w|<=(20/19)*exp(4t)<=25/19: exp(1/5)<=5/4 follows from comparison with the
geometric series. No division by w or by its time zero is used.

With the actual A/f2 scaling,

~~~text
|F(t)| <= eta^(7/2)*(180/2527)
sqrt(E_n(t)) <= eta^(7/2)*P*|c_n|,  P=45/10108,
0<=t<=1/20.
~~~

The inhomogeneous Gronwall/Duhamel estimate follows by applying the energy
inequality to sqrt(E_n+delta), then taking delta down to zero; it remains
valid at zero initial energy and through the leading wave zero. This is the
ordinary lower transverse equation, not the physical Hamiltonian of all fields.

## Tail bounds

Use homogeneous Fourier weights in theta=40z:
the norm squared is the sum over both signed harmonics of |n|^(2s)*|r_n|^2.
The physical spatial derivative factors 40/a have already been kept in E_n.
This Fourier convention is not a microscopic matching or physical momentum cutoff.

For integer N>=4, the exact coefficient satisfies
|c_n|<=16/(3*pi*|n|^3) when |n|>N. The residual inequality reduces to
4*(n^2-16)/[3*n^3*(n^2-4)]>=0. Summing both signs and comparing a positive
decreasing series with its integral gives

~~~text
sum_|n|>N |n|^(2s)*|r_n_dot|^2 / eta^7
 <= 7200*N^(2s-5) / [6385729*pi^2*(5-2s)],       s<5/2,

sum_|n|>N |n|^(2s)*|r_n|^2 / eta^7
 <= 18000*N^(2s-7) / [2305248169*pi^2*(7-2s)],  s<7/2.
~~~

For displacement, E_n supplies the additional factor
a_max^2/(cV2*40^2)<=5/722. The displayed bounds diverge at their endpoint
exponents; this proves a limitation of these bounds, not sharp regularity
or divergence of an actual solved response. Modes1,3 and all old responses
are retained. No finite invariant Fourier subspace is claimed.

This supplies one of the missing inputs for estimating the all-mode mixed
order-|e|^3 source. That source and its full constraint reduction must still
be bounded, including auxiliary-source drift and the separate mean sector.
The full nonlinear remainder, physical energy, GR/local-gravity limits and
matching obligations remain independently necessary for the programme.

## Verification, provenance and disposition

The continuous argument uses exact identities, positive comparisons and
explicit constants. Independent controls use all18 immutable CUSP3 runs:
their leading initial data and zero lower initial data match the recipe;
every stored lower1,3 energy is below the proved bound (largest excess0).
Those sampled controls do not supply or replace the continuous proof.
Nonzero controls retain the omitted fifth mode, momentum drift and mass
coupling, and reject cosine/complex amplitude confusion.

Contract: RES001_R4C1_CUSP_ODD_RESPONSE_TAIL_V1_CONTRACT_2026-10-17.md.
Executable: Analysis/MasterTests/test_01_r4c1_cusp_odd_response_tail_v1.py.
Receipts: Analysis/MasterTests/outputs/r4c1_cusp_odd_response_tail_attempt_01/.
Run with the existing itsm_env Python and -B; repeat with --replay for the
exact read-only reproduction. Both returned0; replay printed READ_ONLY_REPLAY_EXACT.

Executable SHA7e575552a5f2322f81cef53223a3a5c2a64dd87018b808f3b1ef5649a48a085c.
Summary SHAc908e715864be379d28445c3f5e32d173d23986b5db291c79eb1836dc94ed602.
Formulas SHAd2d422cd09ee2d9eb4103b864e4a5c0e37b0845c6dcf8bb31801ad5243a7f924.
374 source pins/745 source and available-sidecar metadata records preserved.
Three inherited missing sidecars remain explicit. Same-agent exact and
independent-computation controls are not independent peer review.

R9-MT1-CUSP-ODD-RESPONSE-TAIL-V1: NONE_WITHIN_STATED_LOWER_RESPONSE_SCOPE;
provisional reuse is supported by the all-n energy and integral bounds.
Inherit CUSP3-EVOLUTION-V1, G3N4 force coverage, generic action/evolving
reduction and all transitive deferred review debt. This result is independent
of the still-running complete weighted-generator replay.

Stage1 complete only its registered linear B1 dust scope; Stage2 INCOMPLETE,
no physical family GO; Stage3 NOT_ENTERED; Tests1-3 HOLD_SUBSTANTIVE;
MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED;
Stage4A CLOSED; TOP-X4 UNCHANGED; native full goal ACTIVE/incomplete.
No commit, push, publication, submission, website/manuscript/PDF, vault mutation,
provider dispatch or model/runtime configuration change.
