# R4C1-B1: interacting finite-charge background control

Date: 2026-09-25. Candidate: R4C1-v1, unchanged.
Status: `CONDITIONAL_INTERACTING_BACKGROUND_CONTROL_PARENT_HOLD`.
Owner: Master Test 1 / exploratory RES-001 R2. Gate effect: `NONE`.

## 1. Result and its limits

The frozen classical candidate admits the registered expanding homogeneous
control on I x T3 with finite conserved charge and **both** energy-exchange
currents nonzero. The executable returns **48/48 checks**. The frame equation,
full frame stress and reduced lapse equations agree symbolically; the
integrated solution passes separate constraint, charge, dust-integral,
cross-integrator and finite-difference energy-balance audits.

This goes beyond the older zero-exchange Stage-B background, without
claiming that no earlier background calculation existed. It does not solve
TOP-X4 or inherit its higher-dimensional, determinant or renormalization
claims. The new reservoir and its portal remain the conditional R4C1 choices.

**Existence/control is not viability.** This is one finite-time, zero-spatial-
winding classical benchmark with freely selected coefficients, not an
observationally fitted or stable cosmology. No hierarchy below the Planck/EFT
scales is established: for example m/M_P=1 at the registered point. No
semiclassical validity, physical perturbation spectrum, cutoff, realistic
matter/radiation history or healthy continuous GR limit follows from this
run. Canonical Test 1 and the complete Tests 1-3 goal remain open.

## 2. Action-derived homogeneous equations

Use ds^2=-N^2 dt^2+a^2 dx_i dx_i with compact unit coordinate periods, and
homogeneous u,v,r,psi and dust variables. The scalar fields carry temporal
U(1) charge, not spatial winding. Let s=u^2+v^2 and use the unchanged
potentials and portal in the [action freeze](RES001_R4C1_ACTION_FREEZE_2026-09-25.md).
Define

```
c_theta = c1+3c2+c3,
M_cos^2 = M_P^2 + M_U^2 c_theta/2,
C = exp(beta psi),
K_s = u_dot^2+v_dot^2+r_dot^2+K_Q psi_dot^2,
U_total = V(s)+V_R(r)+W(s,r)+rho_Lambda.
```

The lapse-unfixed action per unit comoving coordinate volume is

```
L_bg = -3 M_cos^2 a a_dot^2/N + a^3 K_s/(2N) - N a^3 U_total
       + a^3 epsilon [C^2 tau_dot^2/N - N C^4]/2.
```

Vary N and a before choosing N=1. On the dust constraint tau_dot=C and
rho_m=epsilon C^4, the two metric equations reduce to

```
3 M_cos^2 H^2 = K_s/2 + U_total + rho_m,
-2 M_cos^2 H_dot = K_s + rho_m.
```

In the integration H obeys the second equation as an independent variable.
The first fixes H only at the initial time and is then a measured residual.
It is not reimposed by a square-root projection during evolution.

The remaining evolution equations are

```
a_dot = a H,
u_ddot + 3H u_dot + [m^2+lambda_4 s/2+lambda_6 s^2/(4 Lambda^2)+g_r r^2/2]u = 0,
v_ddot + 3H v_dot + [m^2+lambda_4 s/2+lambda_6 s^2/(4 Lambda^2)+g_r r^2/2]v = 0,
r_ddot + 3H r_dot + m_r^2 r + lambda_r r^3 + g_r s r/2 = 0,
K_Q(psi_ddot+3H psi_dot) = -beta rho_m,
rho_m_dot + 3H rho_m = beta rho_m psi_dot,
tau_dot = exp(beta psi).
```

The dust continuity equation follows from variation of tau, not an inserted
current. Its original multiplier is recovered as epsilon=rho_m/C^4. The
constraint tau_dot=C is used to reduce this algebraic dust sector; it is not
reported as a separately evolved invariant. The dust current and scalar
charge give two independently monitored integrals:

```
N_charge = a^3 (u v_dot - v u_dot),
I_dust = a^3 rho_m exp(-beta psi).
```

Their constancy is not imposed in the Cartesian scalar/density integrator.
At unit comoving volume N_charge(0)=1 and I_dust(0)=1/5. The fixed reference
mass and volume set numerical units, not a derived physical torus radius.

## 3. Check against full four-dimensional variations

Substitution into the previously varied R4C1 tensor equations, rather than
variation only after imposing isotropy, gives

```
lambda_U = 3 M_U^2 c2 H_dot - 3 M_U^2(c1+c3) H^2,
rho_U = -3 M_U^2 c_theta H^2/2,
p_U = M_U^2 c_theta(2 H_dot+3H^2)/2.
```

All spatial vector equations vanish on the homogeneous branch. The time
equation determines lambda_U. Inserting it into the full frame stress gives
exactly the M_cos rescaling in both metric equations. Lambda is reconstructed
from its full equation, not independently evolved and then rechecked as a
tautological numerical pass. The unrestricted variation conventions, in
particular normalized n=U/sqrt(-U^2), are retained.

The force field need not be constant. Its full stress gives
rho_psi=p_psi=K_Q psi_dot^2/2. Alignment vanishes and Delta psi=0, so the
auxiliary equation gives z=0. The homogeneous first variations of the
alignment, spatial cubic force operator and regulator are consistent with
this restriction. This does not supply analytic higher Taylor vertices at
Y=0 or a scattering calculation.

The frame contribution is separately conserved on these equations. With
the entire portal stress allocated to the plenum, the full sector densities
and pressures are

```
rho_P = (u_dot^2+v_dot^2)/2 + V + W + K_Q psi_dot^2/2 + rho_U,
p_P = (u_dot^2+v_dot^2)/2 - V - W + K_Q psi_dot^2/2 + p_U,
rho_R = r_dot^2/2 + V_R,     p_R = r_dot^2/2 - V_R,
p_m = 0.
```

The previously varied currents reduce to

```
Q_mp^0 = beta rho_m psi_dot,
Q_syn^0 = g_r s r r_dot/2,
rho_m_dot+3H rho_m = Q_mp^0,
rho_P_dot+3H(rho_P+p_P) = -Q_mp^0+Q_syn^0,
rho_R_dot+3H(rho_R+p_R) = -Q_syn^0.
```

The numerical balance audit differentiates sampled densities with a five-
point centered formula, **not** with the integration RHS. It also uses a
finite-difference H_dot in p_U, keeping the frame contribution rather than
testing only the scalar sectors. Boundary grid points lacking that stencil
are excluded. Thus the reported finite-difference bounds apply to the
sampled interior, not the exact endpoints.

## 4. Registered inputs and measured evidence

The [background contract](RES001_R4C1_INTERACTING_BACKGROUND_CONTRACT_2026-09-25.md)
records every coefficient, initial field, interval and threshold before
execution. It fixes M_cos^2=11/10 and integrates t in [0,4] in arbitrary
reference units. The deliberately chosen c1+c3=0 is a diagnostic coefficient
choice, not a microscopic prediction or fit. No parameter or threshold was
retuned after the run.

Representative evolution:

- a: 1 to 4.333300582985469.
- H: 0.8665251299678509 to 0.14221719136506666.
- rho_m: 0.2 to 0.0025485589665642776.
- Final N_charge: 1.0000000000013007.
- Final I_dust: 0.20000000000002646.
- Minimum sampled s: 0.004572662390991571; no polar-coordinate division was
  needed. The sampled a,H,rho_m remained positive and all fields finite.

These are not measured cosmological H0 or matter abundances. Sampling does
not prove absence of arbitrarily narrow unsampled excursions, and finite
integration does not establish future global existence.

| Diagnostic | Measured value | Registered condition |
|---|---:|---:|
| Fine normalized Friedmann residual | 3.408907498308431e-12 | <1e-8 |
| Coarse normalized Friedmann residual | 3.155680043932974e-9 | improvement comparator |
| Maximum charge drift | 1.8791856959410325e-11 | <1e-8 |
| Maximum dust-integral drift | 2.8703150967146485e-12 | <1e-8 |
| Fine versus Radau, normalized state difference | 1.411611475586304e-11 | <1e-8 |
| Fine versus coarse, normalized state difference | 8.36276517478401e-9 | <1e-6 |
| Finest independent sector-balance residual | 7.963880541709535e-8 | <1e-7 |
| 201-to-801-point balance improvement | 205.19167395590537 | >=4 |
| Max absolute Q_mp^0 | 0.016000000000000004 | >1e-5 |
| Max absolute Q_syn^0 | 0.0938217610455261 | >1e-5 |

The sector-balance accuracy is materially weaker than the constraint and
charge accuracy; do not summarize every equation as verified to 1e-12.

| Finite-difference grid | Plenum maximum | Reservoir maximum | Matter maximum |
|---|---:|---:|---:|
| 201 points, dt=0.02 | 7.225916653159555e-6 | 1.634121979538242e-5 | 1.0147915631801626e-6 |
| 401 points, dt=0.01 | 5.220507584231796e-7 | 1.18637050267723e-6 | 7.547739644174313e-8 |
| 801 points, dt=0.005 | 3.518560539401946e-8 | 7.963880541709535e-8 | 5.159156221632024e-9 |

The independently differenced full spatial metric equation has finest
normalized residual 1.98217124399556e-8 (reported diagnostic, not an extra
post-hoc acceptance threshold).

The reservoir transfer ranges from -0.0938217610455261 to
+0.05357142857142857: it changes direction. The charge remains conserved.
This reinforces the limitation that the candidate demonstrates reversible
energy exchange, not irreversible syntropic production or condensate-number
creation.

## 5. Controls that could have failed

At beta=g_r=0, both currents vanish exactly; the control's normalized
Friedmann residual is 3.5621921038313667e-12. Uncoupled scalars and the frame
still gravitate, so this result is **not pure GR recovery**.

The unchanged action-derived constraint rejects both completed deliberate
mutants:

- H_initial multiplied by 1.001: maximum normalized residual
  0.004367388642501582.
- Reservoir portal force sign reversed, with the action and audit unchanged:
  maximum normalized residual 0.1087566074066432.

Both exceed the preregistered rejection floor 1e-5. The baseline action,
parameters and checks were not modified to accommodate these wrong runs.

## 6. Reproduction and provenance

```
python -B Scripts/itsm_context.py run -- python -B Analysis/MasterTests/test_01_r4c1_interacting_background.py
python -B Scripts/itsm_context.py receipt Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_summary.json
```

Working interpreter: C:/Users/brend/anaconda3/envs/itsm_env/python.exe;
Python 3.13.9, NumPy 2.4.6, SciPy 1.17.1, SymPy 1.14.0. Use that interpreter
for both python invocations if the shell alias is unavailable. The fine
trajectory has 801 samples and carries its own hash sidecar.

SHA256:

- Contract: `3d5f164529ee2621aaa41bd08f8ba0a1ad2e4b866591f5aa4475f188fdf99a59`.
- Script: `1ac9d2618193c064e703b640aec682376010f4a5613bc6fdb236fe583534e14f`.
- Receipt: `e7a9e0cbaf64657153ce497abf1b3ceb90c0722822a1913f94d5c7726176a9d7`.
- Trajectory: `0024b7307de64d780aca3d47401fc8175d59baa354d53912b80ab6842d346daa`.

Before finalization, an unintended `positive=False` symbolic assumption on
non-lapse functions was replaced with unrestricted real-valued functions;
the lapse remains positive. Re-execution leaves every reported numerical
result and the 48/48 outcome unchanged. This is an implementation-domain
correction, not retuning of the frozen physical input.

A repeated run reproduces both receipt and trajectory byte for byte, and a
changed-input-hash probe rejects before replacing either. Private execution
logs remain local and ignored by Git. No paid model dispatch occurred.

## 7. What remains necessary for the goal

The sequence now supports conditional current derivation, complete classical
variation and one nonzero-exchange finite-charge background control. Next
assess the registered GR/constraint limit and physical perturbations, with
the EFT/scale-validity limitation explicit. A healthy solution family cannot
be inferred from the algebraic GR endpoint or homogeneous evolution alone.

Tests 2 and 3 are not closed by this benchmark. It neither derives the
universal weak-field coefficient nor fixes a blind a0 or H0 prediction.
Matching, independently blinded review and canonical parent acceptance
remain open. The user-directed historical pause is respected. The ITSM
memory skill guided provenance boundaries; unavailable live memory tools
were not substituted for current equations or executable evidence.

`physics_pass=false`, `canonical_Test1_pass=false`, `gate_effect=NONE`,
`Rule9=NOT_CLEARED`. MAT-001 BLOCKED; UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED;
V NOT_COMPUTED; Stage4A CLOSED. TOP-X4 and publications unchanged.
