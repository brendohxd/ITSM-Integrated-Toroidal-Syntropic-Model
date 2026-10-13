# Unchanged R4C1: continuous constrained odd-response tail certificate (V1)

12 October 2026. Approved Stage2 research; conditional action/family inputs.
**841/841 local checks, exact immutable replay.** No new background or response
integration. All original trajectories, failed attempts, source pins and
sidecars remain untouched. This is a mathematical second-order tail certificate,
NOT full nonlinear/finite-solver error control, a physical cutoff or Stage2 GO.

## Scope and concrete result

All3 frozen families at the existing eta=1/4 member, coordinate k=20,40,80,
t in [0,1/20], original controlled initial prescription. The proof covers the
exact registered recipe and an outward parameter/seed box containing the stored
binary64 roundoff. It applies to the exact continuum response coefficients.
Archived samples are independent controls, not proof between samples.

Every odd harmonic above N is retained in the comparison, including both signs
of its Fourier pair. For the full constrained 22-field odd branch, the worst
uniform bounds across all9 registered family/mode cases are below:

| Retained odd cutoff N | Field L2 coefficient | Velocity L2 coefficient | Physical-gradient L2 coefficient |
|---|---:|---:|---:|
| 5 | 5.69e-7 | 5.69e-7 | 6.31e-7 |
| 9 | 1.31e-7 | 1.31e-7 | 1.46e-7 |
| 31 | 5.94e-9 | 5.94e-9 | 6.59e-9 |

These decimal upper bounds are conservatively rounded upward; exact dyadic
endpoints are in bounds.json. Norms are torus-average L2 in the exported field
variables, M_P=1 chart units: fields dimension0, velocity/physical gradient
dimension1. Multiply the coefficients by abs(epsilon)^2 for the signed
epsilon*abs(epsilon) second-order response. They are NOT observational errors,
percentages, finite-amplitude model accuracy or physical-energy densities.
The guaranteed norm upper bound scales as N^(-5/2); no fitted or sharp
asymptotic convergence-order claim is made.

## Operator and mass conventions: full coupling retained

The varied generic G3N4 vector action and full generic Hessian give

```text
alpha13=MU2*(c1+c3), MT2=MP2-alpha13,
f2=MU2*(c1+c4), sigma=-alpha13/MT2,
cV2=[MU2*c1+alpha13^2/(2MT2)]/f2,
m_w2=-(3c2+c3-c4)/(c1+c4)*H_dot +2H^2
     -K_Q/f2*psi_dot^2 +zeta/f2*(v*u_dot-u*v_dot)^2.
```

For arbitrary SYMBOLIC nonzero momentum, the full22 original Euler rows
reduce exactly on q_Vy=x, q_Sy=sigma*x, all other odd response fields zero,
to x_ddot+3H*x_dot+[cV2*(nk/a)^2+m_w2]*x=S_Vy(n)/f2. Every original row is
checked, not only the projected vector equation. This is an invariant LINEAR
second-order response branch for the declared source, not a nonlinear finite
invariant manifold. Mean/2k, metric/matter and regulator/constraint sectors
remain in the separate time-response owning report, not removed from the action.

The canonical a^(3/2)-rescaled mass is
m_X2=m_w2-(3/2)H_dot-(9/4)H^2. The frame H_dot coefficient is2 in G3,
-1/5 in B1 and -1/5-3eta/4 in the hierarchical family. Using m_X2 in the
damped frame equation is explicitly rejected. No mass is treated as a cutoff.

## Continuous background proof and explicit domain margins

The frozen homogeneous action supplies positive scalar kinetic/potential
terms, positive dust density and positive Mcos2. Exact identities are

```text
E_dot=-3H*(kin+rho), H_dot=-(kin+rho)/(2Mcos2),
[3Mcos2*H^2-E]_dot=0, [a^3*(u*v_dot-v*u_dot)]_dot=0,
[a^3*psi_dot]_dot=-a^3*beta*rho/K_Q,
[a^3*rho*exp(-beta*psi)]_dot=0.
```

While H>=0, E<=E0 and kin+rho<=2E0. Thus
H>=H0_lower-E0_upper*T/Mcos_lower. Its strictly positive margin rules out a
first zero of H before T, closing the bootstrap on the whole interval.
Then a<=a0_upper*exp(H0_upper*T). Positive dust is preserved by its integrating
factor. The phase equation gives

```text
psi_dot >= p0_lower/exp(3H0_upper*T)-beta_upper*E0_upper*T/K_lower >0,
psi_dot <= p0_upper,
rho >= rho0_lower/exp(3H0_upper*T),
J^2=Q0^2/a^6.
```

Positive potential also bounds the scalar amplitudes and velocities; finite
phase/clock and positive denominators give ordinary background continuation
through T. The proof does not require a fabricated exactly-zero constraint
for a rounded seed: the Friedmann defect is conserved, and both seeds are boxed.
Uniform expansion/phase lower margins (conservatively rounded DOWN) are:

| Family | H lower | psi_dot lower | Enclosing FRAME m_w2 interval |
|---|---:|---:|---:|
| G3 | 0.45693 | 0.045240 | [-1.06357, 0.28934] |
| B1 | 0.44741 | 0.045318 | [0.39846, 0.59668] |
| Hierarchical | 0.44662 | 0.045324 | [0.41395, 0.72473] |

All parameter products, square roots and bounds use256-bit dyadic outward
intervals with rational inputs. Exponential bounds carry geometric Taylor
remainders; pi is enclosed through rational alternating arctangent bounds and
the exact Machin tangent/branch identity. Floats are display/controls only.
Failed positive-potential, H/phase margin or denominator premises refuse the
certificate. Positive frame frequencies are verified in the declared momentum
scope; they do not classify all sectors, a GR limit, or an upper physical cutoff.

## Infinite forced-response proof

Use the auxiliary comparison parameter mu=1, NOT the potential parameter Lambda
or a physical cutoff. Set nu_n2=cV2*(nk/a)^2+mu^2 and
E_n=abs(x_dot_n)^2+nu_n2*abs(x_n)^2. Its exact derivative is

```text
E_n_dot=-6H*abs(x_dot_n)^2-2H*cV2*(nk/a)^2*abs(x_n)^2
        +2Re[(mu^2-m_w2)*conj(x_dot_n)*x_n+conj(x_dot_n)*F_n].
```

Since H>=0 and nu_n>=mu, Young's inequality gives
(sqrt(E_n))_dot<=L*sqrt(E_n)+abs(F_n), with explicit
L>=sup(abs(mu^2-m_w2))/(2mu). The zero initial energy is handled by applying
the comparison to sqrt(E_n+delta^2) and taking delta to0, not by dividing by0.
The same unforced comparison bounds the first mode: its initial energy and
the minimum nu_k give the explicit continuous amplitude W_k.

The source is S_Vy(n)=-D(t)*b_n/2, where D=3A*abs(psi_dot)^3*w*abs(w) and
b_n=-8*(-1)^((n-1)/2)/(pi*n*(n^2-4)) for positive odd n. Its equation forcing
is F_n=S_Vy(n)/f2. The signed nonanalytic source is not replaced by an ordinary
cubic Taylor vertex. With D_upper=3A_upper*p0_upper^3*W_k^2, zero initial
response yields sqrt(E_n)<=abs(b_n)*D_upper*T*exp(LT)/(2f2_lower).

Parseval counts BOTH complex Fourier signs. For n>=3,
b_n^2/2<=128/(pi^2*n^6), so the decreasing-integral test gives
sum_odd_n>N b_n^2/2<=128/(5*pi^2*N^5). Consequently

```text
sum_|n|>N E_n(t)
 <=[D_upper*T*exp(LT)/f2_lower]^2 *128/(5*pi_lower^2*N^5), 0<=t<=T.
```

The full22 field/velocity/physical-gradient estimates follow by multiplying
its square root by sqrt(1+sigma^2)/mu, sqrt(1+sigma^2), and
sqrt(1+sigma^2)/cV_lower respectively (cV_lower is the square-root speed).
This is a controlled mathematical continuation of the declared classical
operator; no physical UV completion or admissibility of arbitrarily high
frequency is asserted. The existing field named cutoff is only the potential
normalization Lambda in this calculation, not a derived physical cutoff.

## Provenance, checks and remaining work

Frozen contract SHA9d3688ec3aeba5fc6c202c7c28320a2ce0fe3319da6bd552bd2710ca4fa327b1.
Executable `Analysis/MasterTests/test_01_r4c1_three_family_odd_tail_v1.py`,
SHA0f45821dff77a69782fe6c7a781b977ab7bea6c2f03b632714634fb195fa01cc.
Fresh receipts `Analysis/MasterTests/outputs/r4c1_three_family_odd_tail_attempt_01/`:
summary SHAe4370b6e11294207039397de217a3a9e6f04488d669cb6eb76182378fbab92f2;
bounds SHAe1c27e3bc379b54d3577f1e6285435e1b8e5283ce2a37adcfea2770077643186;
formulas SHA9337c2c02ab93800150fe1466b17be0c29d3485044a3aa24dee70a2432ca6b0c;
scope SHA0becf6e7335eddd711ad41a5db46df2b30021112a6b3ecf3b1cb9e391e3577ed.
255 source pins/507 metadata records preserved. Three inherited UVIR documents
lack sidecars; their source bytes remain pinned, no sidecar manufactured.
Original trajectory SHA8a3e5df7765aca174b520a53a8a0ca01848941ec34032cba648c3a198ee9320d
is unchanged. Both the841-check execution and exact replay return exit0.
Private log hashes:505095fa6f887ea264e3f0d1dc9e483f9d48b2544b08fdc44208a82a57ac5985
and c08b00d69f55147972563664b74092763e2e1cfb9396f5cb384e98f0a1b6f18e.

Independent rational arithmetic, closed forced-oscillator/Parseval controls,
every378 archived first-mode/envelope and odd-prefix control, all22 symbolic
operator rows and rejection tests pass. The archive is NOT used to establish
continuous extrema. No finite solver or complete finite-amplitude nonlinear
remainder is certified. Next substantive work remains the full coupled
nonlinear/interaction and physical-window assessment, not a repeat integration.

No physical family admitted; Stage2 incomplete, STOP_AND_ASSESS_DOMAIN_UNRESOLVED;
Stage3 NOT ENTERED; identifying matter-residue/nonlinear-force matching absent.
Mean/physical-energy/fixed-charge/singular/quartic sectors, healthyGR/fullPPN,
ALL-sector continuous physical band and full nonlinear remainder remain open.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE;
Tests1-3 HOLD_SUBSTANTIVE; MAT-001 BLOCKED; UVIR-003 IN_PROGRESS;
K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED; TOP-X4 UNCHANGED.
Root goal ACTIVE/incomplete. No paper/PDF/publication/commit/push, provider/model,
runtime/dependency or vault operations.
