# Homogeneous B1: dust reconstructed and linear clock conservation verified

29 October 2026. Conditional independent homogeneous G2/G3 control.
Review DEFERRED; Rule9_cleared=false; physics_pass=false; gate_effect=NONE.

## Result

The explicit matter-density reconstruction missing from the earlier B1
quadratic reports is now derived from the original lapse equation, including
its spatial flux. With this density and the actual time-dependent reduced
generator, the linear dust clock equation is satisfied exactly on the old
homogeneous B1 solution. Its off-shell residual is proportional to the
background Friedmann constraint; that constraint vanishes initially and is
preserved by the existing background flow.

This is a substantive consistency check on the evolving homogeneous control,
not admission of the registered vortical G1 preparation. It supplies a
necessary prerequisite to controlled propagation. A propagator/error
certificate, finite-amplitude density-positivity bound and nonlinear physical
window have not yet been established.

## Original lapse variation and its density row

The [frozen contract](RES001_R4C1_B1_DUST_RECONSTRUCTION_V1_CONTRACT_2026-10-29.md)
retains the old B1 parameters, future positive-dust branch and the full
original weak-action density. It reuses the background-dependent matrices
and actual generator of [B1_KINETIC_DRIFT_V1](RES001_R4C1_B1_KINETIC_DRIFT_V1_REPORT_2026-10-29.md).

Independent lapse, lapse-gradient and dust-multiplier increments are retained
in a 42-variable exact second variation. Only after forming

$$\delta E_N=\delta L_N-ik\,\delta L_{N_z}$$

are the varied clock constraint and the solved Z/three-shift equations
substituted. The clock gauge gives delta N=-beta delta psi and
delta N_z=-ik beta delta psi. For
delta epsilon=delta E/C_background^4, the coefficient of delta E in the
lapse equation is exactly -a^3, so it determines this multiplier rather than
an additional vacuum Hamiltonian constraint. The physical density is

$$\delta\rho=\delta E+4\beta\rho\,\delta\psi.$$

Use the parent amplitude order, comoving k != 0, physical frame amplitude
v_z, p=psi_dot and Gamma=gamma_xx+gamma_yy. Write

$$S=\dot u^2+\dot v^2+\dot r^2+3p^2,\qquad
U=\frac{s}{2}+\frac{s^2}{24}+\frac{s^3}{480}
+r^2+\frac{r^4}{28}+\frac{3sr^2}{28},\quad s=u^2+v^2,$$

$$F=3(11/10)H^2-(S/2+U+\rho).$$

The complete reconstructed row is equivalently

$$\begin{aligned}
\delta\rho={}&\left(F/2+\frac{k^2}{2a^2}\right)\Gamma
-\frac{13iHk}{6a}v_z
-\sum_{\phi=u,v,r}(33H\dot\phi+U_{,\phi})\delta\phi\\
&-\left(\frac{132H^2}{5}+99Hp+\frac{2S}{5}
+\frac{k^2}{15a^2}\right)\delta\psi
-\frac{33H}{2}\dot\Gamma-\frac{ik}{6a}\dot v_z
-\sum_{\phi=u,v,r}\dot\phi\,\delta\dot\phi-3p\,\delta\dot\psi.
\end{aligned}$$

This compact expression is checked algebraically against all twenty exported
coefficients. On the actual homogeneous solution F=0. The density is therefore
a determined function of the evolving metric/frame/scalar amplitudes and
velocities, not an independently adjustable forcing history.

The contribution lost by omitting the original lapse flux is

$$\delta\rho_{\rm flux}=\frac{k^2}{2a^2}\Gamma
+\frac{iHk}{30a}v_z-\frac{k^2}{15a^2}\delta\psi
-\frac{ik}{6a}\dot v_z.$$

Both the curvature and frame/lapse-gradient pieces are retained. Their
spatial mean vanishes for a nonzero Fourier perturbation, but their local
equation does not vanish. The original dust branch is regular at positive
background density. No finite-amplitude evolution bound keeping the
reconstructed density positive is claimed here.

## Exact evolving clock identity

The original clock momentum and spatial current give

$$\delta p_\tau=\frac{a^3}{C}
\left[\delta\rho-\beta\rho\,\delta\psi+\frac\rho2\Gamma\right],
\qquad \delta J_\tau^z=-\frac{a^3\rho}{C}\frac{S_z}{a},$$

where S_z denotes the solved **physical longitudinal shift amplitude**, not
its spatial derivative. Thus with
R=delta rho-beta rho delta psi+rho Gamma/2, the linear continuity equation is

$$\dot R+(3H-\beta p)R-\frac{ik\rho}{a}S_z=0.$$

Substitute the full twenty-component generator from the time-dependent
quadratic action, its actual background flow and the solved shift row. Exact
polynomial division by F gives the off-shell residual

$$F\left[\frac{3H}{2}\Gamma+
\frac4{25}(5H-p)\delta\psi+\frac12\dot\Gamma\right].$$

The polynomial remainder is zero for every coefficient. Since the registered
background has F=0 and dot F=0, this proves the identity along that background
where the nonzero-mode reduction is defined. It is stronger than a sampled
small numerical residual and does not assume an exactly frozen background.
Omitting the lapse flux instead gives a nonzero residual even at the initial
event. The original lapse equation is also checked after complete multiplier,
Z and shift reconstruction.

These are linearized constraints and conservation on the aligned control.
They do not prove nonlinear constraint persistence near finite tilt, resolve
the nodal current/concentration problem, or supply a zero-mode reduction.

## Verification and continuation

The [versioned executable](../../../Analysis/MasterTests/test_01_r4c1_b1_dust_reconstruction_v1.py)
passes 19/19 checks. The [fresh receipt with reconstruction rows](../../../Analysis/MasterTests/outputs/r4c1_b1_dust_reconstruction_v1_attempt_01/summary.json)
has SHA-256 `7f4134defc9dd25b6a831d154f195a308a17b8d3ee01c29643a764b088c51e4a`.
The complete read-only recomputing replay is byte-identical, exit 0. Fifteen
direct source files and their fifteen sidecars retain bytes and modification
times through calculation/replay.

Independent real four-point second differences evaluate the original physical
density, with A retained, for the lapse and lapse-gradient rows at two
directions and steps 1e-12 and 1e-16. The maximum normalized discrepancy at
the smaller step is 9.586e-33. These control the derivative implementation;
the exact generic conservation calculation supplies the stated time-dependent
identity, and neither constitutes external peer review.

The next substantial control task remains the certified full twenty-component
propagator on [0,0.05], including background coefficient uncertainty, local
residuals, accumulation, physical-norm conversion and algebraic reconstruction.
Do not replace it with a frozen-mode spectrum or a continually projected slow
graph. The independent homogeneous control does not replace G1's registered
vortical preparation, whose nonlinear on-shell domain remains open.

G1-G6 INCOMPLETE; Stage 2 INCOMPLETE; Stage 3 NOT_ENTERED; MAT-001 BLOCKED;
UVIR-003 IN_PROGRESS; K_Q NOT_DERIVED; V NOT_COMPUTED; Stage 4A CLOSED.
Inherited review remains DEFERRED. No action/state adoption, matching input,
manuscript/PDF/site change, vault mutation, commit or push.
