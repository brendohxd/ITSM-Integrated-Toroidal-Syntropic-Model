# R4C1-S3: zero-branch regularity disposition

Date: 2026-09-26. Master Test 1, conditional R4C1-v1/B1.
Validation: 57/57 checks, no failed/unknown check in the current receipt.
Review DEFERRED; physics_pass=false; gate_effect=NONE; Rule9_cleared=false.

## Decision

S2's Jordan block is real, but its interpretation depends on the variables
and spatial regularity. Two distinct propositions are now established:

1. The frozen zero-principal system has no wave-number-uniform bound in the
   displayed equal-order canonical norm. An explicit unit initial sequence
   grows like p at fixed positive duration.
2. On the same frozen zero sector, the preregistered original-variable graph
   norm admits a finite positive large-p limit after an explicit derivative
   rescaling, for a>0, H>0, rho_m>0 and 5H+4*psi_dot!=0. This yields a bounded
   large-p transfer for each fixed regular background event in that different
   norm, not a cure of the equal-order bound.

The complete coupled initial-value problem is NOT proved well posed. The
fast-mode embedding is asymptotic, the coefficient event is frozen and the
comparison covers only the zero-principal sector. All propagating branches,
subleading couplings, changing coefficients, constraints and the desired
function spaces must be treated together before making that stronger claim.
No extra dust pressure, altered action, damping, parameter retuning or
eigenvector deletion is used.

Owning [contract](RES001_R4C1_ZERO_BRANCH_CONTRACT_2026-09-26.md);
upstream [S2](RES001_R4C1_SCALAR_PROPAGATION_REPORT_2026-09-26.md) and
[S1](RES001_R4C1_SCALAR_CONSTRAINT_REPORT_2026-09-25.md).

## 1. Exact obstruction in the stated canonical norm

For Z=(p*x_T,p*x_W,xdot_T,xdot_W), the frozen leading equations are
Zdot=p*A*Z with

\[
 A=\begin{pmatrix}
 0&0&1&0\\0&0&0&1\\1/33&0&0&2/\sqrt{11}\\
 0&0&-2/\sqrt{11}&0
 \end{pmatrix}.
\]

Let e0=(0,1,0,0)^T and e1=(-6*sqrt(11),0,0,1)^T. Then A e0=0 and
A e1=e0. The exact zero projector P0=I+3A^2 satisfies P0^2=P0;
N=A P0 is nonzero with N^2=0. Hence

\[
 e^{p\Delta t A}P_0=P_0+p\Delta t N.
\]

Since ||e1||^2=397 and e0 is orthogonal to e1, the unit initial sequence
e1/sqrt(397) has squared norm

\[
 \left\|e^{p\Delta t A}\frac{e_1}{\sqrt{397}}\right\|^2
 =1+\frac{p^2\Delta t^2}{397}.
\]

For any fixed Delta t>0 this is unbounded as p increases. Dropping e1 or
claiming a complete eigenbasis would remove legitimate data. A p-uniform
bounded invertible diagonalizer cannot diagonalize a Jordan block. This
statement concerns the displayed norm; it is not a theorem about every
physical formulation of the constrained model.

## 2. Independent pressureless-dust control

Vary the frozen matter action at fixed Minkowski metric, constant C0 and
epsilon0>0, about tau=C0*t. Its second-order density before imposing the
multiplier constraint is

\[
 L_m^{(2)}=\frac{\epsilon_0 C_0^2}{2}
 [\delta\dot\tau^2-(\partial_x\delta\tau)^2]
 +C_0^3\delta\epsilon\,\delta\dot\tau.
\]

The multiplier gives delta taudot=0. The tau equation, with
delta rho=C0^4 delta epsilon, rho0=epsilon0*C0^4 and v=-partial_x delta tau/C0,
then gives

\[
 \delta\dot\rho+\rho_0\partial_xv=0,\qquad \dot v=0.
\]

For the real cosine-density/sine-velocity mode and D=delta rho/rho0, the
transfer on (D,v) is [[1,-p*Delta t],[0,1]]. On (D,p*v) it is instead
[[1,-Delta t],[0,1]]. Thus the linear density estimate needs one more spatial
derivative of initial velocity than an equal-order density/velocity norm.
This is a derived matter-sector control, not a replacement for the coupled
B1 equations or a nonlinear pre-caustic theorem. The mechanism is not unique
to ITSM; the full coupled zero branch still contains both dust and frame.

## 3. Reconstruction in original constrained variables

Use S1's exact auxiliary solutions and S2's q=R*x, including Rdot. Embed the
T,W slow sector in the six fields using the leading fast-mode Schur relation,
and differentiate that embedding at fixed comoving k when reconstructing
qdot. This keeps its subleading velocity terms but does not turn the leading
embedding into an exact full solution.

On the dust constraint,

\[
 \delta\rho_m=C^4\delta\epsilon+4\beta\rho_m\delta\psi,
 \qquad v_d=\frac{p\delta\tau}{C},\qquad v_{U-d}=w-v_d.
\]

Here v_d is dust tilt relative to the ADM normal; it is not the coordinate
velocity with the shift omitted. These expressions follow from
u^(m)_a=-partial_a tau/C and rho_m=epsilon*C^4 on shell. The multiplier
equation and linear matter normalization vanish exactly after reconstruction.
Lapse, shift, delta epsilon and the regulator are exported, not promoted to
additional physical modes. The regulator identity remains z=-delta Delta.

The frozen graph norm is the sum of squares of

```
delta f, p*delta f, delta fdot (f=u,v,r);
sqrt(K_Q)*delta psidot; sqrt(b)*delta Delta_psi;
sqrt(M_U^2*c14)*wdot; sqrt(M_U^2*cL)*p*w;
delta rho_m/rho_m; v_d.
```

It is a differential-order reference-unit norm, not the Hamiltonian or a
claimed unique invariant energy. No weights were selected after the result.
Let F(p) map the amplitudes on (e0,e1) into these quantities, and B=F^T F.
The first column is O(1); the second is O(p). Thus use the explicitly
different Jordan-amplitude coordinates (j0,p*j1). Their graph map is
F(p)*diag(1,1/p), and their transfer is [[1,Delta t],[0,1]].

All limiting graph rows vanish except the frame-gradient and density rows:

\[
 F_\infty\big|_{\mathrm{frame,density}}=
 \begin{pmatrix}
 \sqrt{10}/(5a^{3/2})&-\sqrt{10}/(5Ha^{3/2})\\
 -\sqrt6(115H+4\dot\psi)/(60a^{3/2}\rho_m)
       &11\sqrt6/(6a^{3/2}\rho_m)
 \end{pmatrix}.
\]

Its determinant is

\[
 -\frac{\sqrt{15}(5H+4\dot\psi)}{150Ha^3\rho_m}.
\]

For the stated nonzero domain this is a rank-two minor, so the limiting Gram
matrix is positive definite. Continuity then supplies finite upper/lower
Gram bounds for sufficiently large p at each such fixed event. Combined
with the p-independent rescaled transfer, this proves a bounded large-p
estimate for this restricted frozen system in this graph norm. It does not
provide a uniform constant over an unverified domain approaching H=0,
rho_m=0 or 5H+4*psi_dot=0, nor a theorem for the full time-dependent system.

## 4. Numerical comparison and failed attempt

The six coefficient times are (0,0.5,1,2,3,4). For principal duration one,
evaluate p=2*pi*2^j, j=0,...,8. These are local-symbol probes, not another
set of full cosmological trajectories. At the largest p, the equal-order
operator amplification is about 80.74 and continues to grow without bound.

| Background time | Graph amplification at largest sampled p | Large-p graph limit |
|---|---:|---:|
| 0 | 549.10 | 550.33 |
| 0.5 | 1256.31 | 1259.02 |
| 1 | 1933.68 | 1938.39 |
| 2 | 1554.17 | 1557.27 |
| 3 | 1333.72 | 1335.88 |
| 4 | 1345.16 | 1347.33 |

These constants are large and reference-chart dependent. A finite limit is
not small amplification or physical stability. At these six events the
additional domain factor 5H+4*psi_dot ranges from about 5.133 to 0.716;
this is not an analytic certificate for every intermediate time.

Attempt 01 failed 54/55: the two numerical norm calculations disagreed by
1.2634727222473163e-8, exceeding the frozen 1e-8 tolerance. The unscaled Gram
condition number reached roughly 9.6e15. The failed receipt, code and outputs
are retained in `Analysis/MasterTests/outputs/r4c1_s3_attempt_01/`.

The corrected calculation uses the algebraically identical diagonal
rescaling and 50-decimal arithmetic. Cholesky/SVD and an independent
generalized-eigenvalue polynomial now agree to about 8.95e-44 for the same
inputs. This is arithmetic agreement, NOT fifty-digit physical accuracy:
background inputs retain their original floating-point/integration accuracy.
No action, graph norm, grid or tolerance was changed. The raw normalization
and rescaled transfer equivalences are checked exactly.

## 5. Provenance and remaining obligation

Run:

```
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_01_r4c1_zero_branch.py
```

The [receipt](../../../Analysis/MasterTests/outputs/test_01_r4c1_zero_branch_summary.json)
has SHA-256 1507c9b40b7a76985a81e520780fed6631eca59880870ae208d60d9587a6f374.
Its matrix artifact exports the original q/qdot/auxiliary/density maps,
projector/Jordan identities and graph powers; the sample artifact retains
all comparisons and conditioning. The failed receipt hash is
538101b569dc8798af9249d4b4c47c8952265eef8a48683a0c84c4d072201361.

R9-MT1-S3 inherits R9-MT1-S2/S1/B1/VARIATION. All review is deferred; the
bounded results can be used provisionally. The scientific task that remains
is a complete coupled principal/subprincipal evolution estimate in explicitly
declared mixed-regularity spaces, including time-dependent constraints and
all scalar branches. A pressureless control or a leading-sector norm cannot
replace that calculation. Homogeneous/singular sectors, causality, cutoff,
healthy GR recovery and physical weak-field matching also remain open.

This narrows the zero-branch issue; it neither deletes the Jordan obstruction
nor proves an additional all-formulation pathology. MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage4A CLOSED.
No provider dispatch, model change, commit, push or publication.
