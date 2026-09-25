# R4C1-G1: GR-limit audit and physical interpretation

Date: 2026-09-25. Owner: Master Test 1, with a normalization consequence for
Test 2. R4C1-v1 is unchanged; this is a candidate calculation, not adoption.

**Disposition:** `ZERO_EXCHANGE_GR_IMPLICATION_REJECTED_CLASSICAL_ENDPOINT_PERTURBATIVE_HOLD`.
Executable verification: 56/56 checks, reproducible receipt. `physics_pass=false`.

## 1. Three different GR claims

| Claim | Result and boundary |
|---|---|
| Turning off exchange recovers GR at fixed B1 frame coefficients | Rejected: the derived cosmological/static gravitational-coupling ratio is 5/6, not one. |
| The declared coefficient endpoint admits an Einstein-dust background | Supported on the scalar-free background. Canonical spectator scalar kinetic terms remain in the full endpoint theory. |
| The registered continuous family is a healthy perturbative route to GR | Not established: backgrounds approach Einstein-dust, but a physical transverse kinetic coefficient vanishes and the canonical cubic force coefficient diverges. This is not an all-path no-go. |

The owning [frozen contract](RES001_R4C1_GR_LIMIT_CONTRACT_2026-09-25.md)
separates these claims before execution. The [action freeze](RES001_R4C1_ACTION_FREEZE_2026-09-25.md),
[complete classical variation](RES001_R4C1_FULL_VARIATION_REPORT_2026-09-25.md)
and [B1 background report](RES001_R4C1_INTERACTING_BACKGROUND_REPORT_2026-09-25.md)
remain the inputs. No observational target was used to retune the family.

## 2. Zero exchange does not remove the frame stress

Set beta=g_r=0, Phi=r=0 and psi constant for a frame-metric control. Retain
the B1 frame coefficients. In signature (-+++), use

\[
g_{tt}=-e^{2\phi},\qquad g_{ij}=e^{-2\chi}\delta_{ij},\qquad
U=e^{-\phi}\partial_t.
\]

The static quadratic action, after the Einstein-Hilbert boundary term, is

\[
\mathcal L_{\mathrm{stat},2}=
M_P^2[(\nabla\chi)^2-2\nabla\phi\cdot\nabla\chi]
+\frac{M_U^2c_{14}}2(\nabla\phi)^2-\rho\phi.
\]

Independently, substitution in the full varied tensors gives

\[
G_{00}^{(1)}=2\Delta\chi,\qquad
T_{U,00}^{(1)}=M_U^2c_{14}\Delta\phi,\qquad
T_{U,ij}^{(1)}=0.
\]

The spatial Einstein equation fixes chi=phi on nonzero modes, so

\[
(2M_P^2-M_U^2c_{14})\Delta\phi=\rho.
\]

Define alpha_i=(M_U^2/M_P^2)c_i and G_bare=1/(8 pi M_P^2). Then

\[
G_{\mathrm{static}}=\frac{G_{\mathrm{bare}}}{1-\alpha_{14}/2},\qquad
G_{\mathrm{cos}}=\frac{G_{\mathrm{bare}}}{1+(\alpha_{13}+3\alpha_2)/2}.
\]

The cosmological expression follows from the already varied B1 Friedmann
equation. Both agree with equations (2.6) and (3.6) of
[Oost, Mukohyama and Wang, arXiv:1802.04303v2](https://arxiv.org/html/1802.04303v2)
after identifying that paper's dimensionless c_i with this report's alpha_i,
not with the bare c_i multiplying M_U^2. This is a cross-check, not a
substitute for the direct variation. No observational bound from that paper
is applied to the interacting candidate here.

For the retained B1 frame, alpha_13=0, alpha_14=1/6 and
alpha_13+3 alpha_2=1/5. Hence

\[
G_{\mathrm{static}}/G_{\mathrm{bare}}=12/11,\quad
G_{\mathrm{cos}}/G_{\mathrm{bare}}=10/11,\quad
\boxed{G_{\mathrm{cos}}/G_{\mathrm{static}}=5/6}.
\]

Calibrating one gravitational constant does not remove this difference.
Luminal tensor propagation alone does not imply GR. Negative controls also
reject substituting bare c_i for alpha_i.

**Domain:** quasistatic local response or nonzero spatial Fourier modes.
On compact T3 the source must obey the zero-mode compatibility condition;
this is not a globally isolated positive mass on empty T3. It is not a
static dust equilibrium, a full PPN metric, or a solution of the interacting
B1 inhomogeneous problem. It does not derive the full ITSM weak-field law
or its 2/3 factor. Test 2 must not silently identify bare G with measured
Newtonian response.

## 3. Metric-constrained transverse mode

On the zero-scalar flat control use lapse N=1, gamma_ij=delta_ij, transverse
shift B_y(t,x), and the exact unit parametrization

\[
U^0=\sqrt{1+w^2},\qquad U^y=w-B\sqrt{1+w^2}.
\]

The transverse spatial metric perturbation is gauge fixed, but its shift
constraint is retained. The full frame action plus the Einstein-Hilbert ADM
term gives

\[
\mathcal L_{V,2}=\frac{M_U^2c_{14}}2\dot w^2
-\frac{M_U^2c_1}2 w_x^2
+\frac{M_U^2c_{13}}2w_xB_x
+\frac{M_P^2-M_U^2c_{13}}4B_x^2.
\]

For nonzero wave number and nonsingular shift block,

\[
B_x=-\frac{M_U^2c_{13}}{M_P^2-M_U^2c_{13}}w_x,\qquad
K_T=M_U^2c_{14},\qquad
G_T=M_U^2c_1+\frac{M_U^4c_{13}^2}{2(M_P^2-M_U^2c_{13})}.
\]

The reduced action is (K_T dot(w)^2-G_T w_x^2)/2. The other transverse
polarization has the same coefficients. Their ratio agrees with the
normalized frame-sector vector speed. These are physical transverse
coefficients after eliminating the shift, not a metric-frozen guess.
The scalar constraints and zero Fourier mode remain separate problems.

## 4. Registered family and canonical coefficients

For 0<eta<=1 multiply B1's M_U^2,zeta,K_Q,A,b,g_r by eta and beta by eta^2.
Scale initial u,v_dot,r,r_dot by sqrt(eta) and psi_dot by eta, leaving the
other inputs as stated in the contract. Each eta labels a separate solution;
couplings are constant in time. Initial charge equals eta and is conserved
within each solution. This is not a fixed-charge limit.

On this path, in the B1 reference units,

\[
K_T=\eta/6,\qquad c_V^2=4/5\quad(\eta>0).
\]

K_T tends to zero and its inverse canonical normalization diverges. The
finite speed ratio does not restore a kinetic term at eta=0. In particular,
4/5 must not be assigned to a physical endpoint mode by dividing zero by zero.

For psi_c=sqrt(K_Q) psi the exact spatial cubic operator has coefficient

\[
\frac{A}{K_Q^{3/2}}=\frac{2\sqrt3}{63\sqrt\eta}\longrightarrow\infty,
\qquad \frac b{K_Q}=\frac5{33},\qquad
\frac\beta{\sqrt{K_Q}}=\frac{2\sqrt3}{15}\eta^{3/2}\longrightarrow0.
\]

Thus small bare couplings do not establish uniformly weak canonical
interactions. The operator remains the nonanalytic |grad psi_c|^3 term;
this audit does not derive a scattering cutoff or an analytic cubic vertex.
Other scalings could alter this diagnostic. No proof excluding every R4C1
GR limit, and no full interacting B1 stability result, is claimed.

## 5. Charge and the exact endpoint

For n=u v_dot-v u_dot and
e_0=(u_dot^2+v_dot^2+m^2(u^2+v^2))/2,

\[
(\dot u\pm mv)^2+(\dot v\mp mu)^2=2(e_0\mp mn).
\]

With nonnegative additional potential and portal terms this proves

\[
\rho_\Phi\ge m|n|=m|N_{\mathrm{charge}}|/a^3.
\]

At fixed nonzero charge, finite a and m>0, the condensate stress cannot
vanish. This excludes the scalar-free Einstein-dust endpoint under those
conditions, not GR with separately conserved spectator scalar matter.
The frozen endpoint u=v=r=0 is a background restriction: it does not delete
the canonical scalar kinetic terms from the endpoint theory. At eta=0 the
Einstein-dust control is defined separately; no vanishing kinetic block is
inverted.

## 6. Numerical classical-background approach

The analytic endpoint has H_g=sqrt(0.2/3),
a_GR=[1+(3/2)H_g t]^(2/3), H_GR=H_g/[1+(3/2)H_g t] and
rho_m,GR=0.2/a_GR^3. All six DOP853 runs finish on [0,4] with rtol=1e-11,
atol=1e-13 and 801 common samples. H is evolved without constraint projection.
The error below is max |member-GR|/(1+|GR|) over a,H,rho_m and all samples.

| eta | Metric/dust error | Maximum normalized Friedmann residual | Canonical cubic coefficient / B1 |
|---|---:|---:|---:|
| 1 | 0.8608207742 | 3.41e-12 | 1 |
| 1/4 | 0.2784084650 | 6.26e-12 | 2 |
| 1/16 | 0.08473618829 | 2.75e-12 | 4 |
| 1/64 | 0.02308182222 | 5.85e-13 | 8 |
| 1/256 | 0.005924278213 | 6.34e-13 | 16 |
| 1/1024 | 0.001491441977 | 5.21e-13 | 32 |

Errors decrease at every registered step; the last factor-four refinement
reduces error by approximately 3.97. The largest normalized charge drift is
1.88e-11 and dust-integral drift 2.87e-12, both below the frozen 1e-8 bound.
This supports a classical background approach while displaying increasing
canonical force interaction strength. It is not a calibrated cosmology,
proof of a semiclassical scale hierarchy, or uniformly healthy perturbations.

## 7. Reproduction, provenance and remaining work

Run from the repository root using itsm_env Python:

```powershell
python -B Scripts/itsm_context.py run -- python -B Analysis/MasterTests/test_01_r4c1_gr_limit.py
```

Use the known full interpreter path for both python arguments if the shell
alias is unavailable. The executable pins the action, G1 contract, full
variation executable and B1 executable before calculating or writing output.

- Script SHA256: `0730de78971da97345517477115ace91bd0b9c1c0ae0b136c07067854a38a710`.
- Contract SHA256: `bd403fe7f2ec1df70a58552f357c2e27d07c0d26797d39a9569178ca5992c580`.
- Receipt: `Analysis/MasterTests/outputs/test_01_r4c1_gr_limit_summary.json`.
- Receipt SHA256: `9b55e0a54dfaef0e1e44eca62ee765b89a53a399f84e8c3b3ffa371edfd079a8`.

A repeat run reproduced the receipt byte for byte. An in-memory corrupted
expected input hash raised FROZEN_INPUT_HASH_MISMATCH before output overwrite;
the prior receipt remained unchanged. A temporary redundant infinity-
subtraction placeholder in the draft checking code was removed; the final
check directly tests the symbolic positive-infinity limit. No frozen input,
threshold or physical result was changed by that cleanup.

The 56 passed checks include confirmations of rejected physical implications.
They are not 56 viability conditions passed. Complete Test 1 still requires
a physically admissible parent/limit, the interacting scalar/metric/frame
constraint reduction, stability and EFT scale control, and independent review.
Test 2 still lacks the complete matched weak-field derivation. Test 3 still
lacks a uniquely predicted acceleration coefficient and independent blind
review. Historical reconstruction remains parked by user direction.

A useful next bounded question is whether the current action's spatial force
coefficient is identifiable from its homogeneous background and source data;
that investigation must not insert an observed a0 or imply a full galaxy fit.
No additional completion or reviewer dispatch is asserted here.

MAT-001 `BLOCKED`; UVIR-003 `IN_PROGRESS`; K_Q `NOT_DERIVED`; V
`NOT_COMPUTED`; Stage4A `CLOSED`; Rule9 `NOT_CLEARED`; gate_effect `NONE`.
TOP-X4 is unchanged. No commit, push, publication or paid review was performed.
