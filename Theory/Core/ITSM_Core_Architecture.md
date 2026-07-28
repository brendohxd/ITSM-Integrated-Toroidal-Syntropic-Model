# ITSM Core Architecture

Canonical architecture: CRA-001 draft  
Status: research-stage constitution for the v12 recovery branch

## 1. Scope

The Integrated Toroidal-Syntropic Model is being reconstructed as a layered
effective framework for a finite-density, rotational vacuum medium on compact
spatial topology. This document defines the sectors that the model may use and
the logical relationships between them. It does not assert that the open
research gates have been solved.

No manuscript claim may be promoted beyond the status recorded in the claim
ledger merely because it is compatible with this architecture.

Conventions: metric signature `(-,+,+,+)`; `c = hbar = 1` except when restored
for dimensions; `M_P^(-2) = 8 pi G`; and `kappa = 8 pi G`.

## 2. Core physical proposition

The recovered ITSM proposition is:

> The observable vacuum is an active finite-density condensate whose low-energy
> excitations, global circulation sectors, compact boundary conditions and
> exchanges with matter and a reservoir may have gravitational consequences.

The intended hierarchy is:

```text
complex condensate UV theory
    -> finite-density background and winding sectors
    -> emergent IR phonon EFT
    -> local matter response and wakes

compact T3 topology
    -> periodic modes and shape moduli
    -> topology-dependent stress

reservoir
    -> plenum throughput
    -> possible driven non-equilibrium response
```

Each arrow is a derivation or matching problem, not an identity.

## 3. Declared sectors

### 3.1 Metric sector

The spacetime metric is `g_{mu nu}` and the gravitational action begins with
the Einstein--Hilbert term. Any departure from its local predictions must be
derived from declared matter or plenum stress, a declared physical metric, or
an explicit gravitational extension.

### 3.2 Complex condensate sector

The candidate microscopic order parameter is

```text
Phi = (rho/sqrt(2)) exp(i Theta).
```

The amplitude `rho` permits finite density, healing dynamics and zeros at
defect cores. The phase `Theta` permits phonons and quantized winding. This
sector is the natural home of the original rotational and superfluid ontology.

UVIR-001 tested the minimally kinetic candidate with analytic mass, quartic and
sextic terms. It has a stable timelike finite-density branch and the pure
sextic limit yields `P(Z) proportional to (Z-m^2)^(3/2)`. However,
`P_Z = rho0^2/2 > 0` forces a leading quadratic static-gradient response about
every nonzero stable condensate. The candidate is therefore rejected as the
direct origin of the spatial `Y^(3/2)` operator.

UVIR-002 rejected the standalone nonrelativistic `X<0` branch because its
quadratic time kinetic coefficient is negative. It provisionally selected a
two-sector preferred-frame architecture: `Phi` retains the finite-density,
circulation and topology roles, while a separate force field `psi` may use
independent temporal and spatial invariants. This is not yet a canonical
microscopic action. UVIR-003 must validate the selected route.

Finite density must be declared explicitly rather than inferred from the field
name. In a homogeneous rest frame use

```text
Theta = mu t + vartheta
```

or covariantly `nabla_mu Theta = -mu U_mu + nabla_mu vartheta` at leading
order. At fixed charge or chemical potential the homogeneous amplitude is
selected by

```text
V_eff(rho; mu) = V(rho) - (1/2) mu^2 rho^2,
d V_eff/d rho |_(rho0) = 0,
d^2 V_eff/d rho^2 |_(rho0) > 0,
rho0 != 0.
```

UVIR-001 established the branch stability, susceptibilities and mode gaps for
a sufficient positive-coupling domain of the tested candidate. The physical
charge-setting mechanism and any replacement UV action remain open; finite
density must still not be treated as an undeclared assumption.

### 3.3 Plenum frame

A unit timelike field `U^mu` defines the rest frame of the finite-density
background and the spatial projector

```text
h^{mu nu} = g^{mu nu} + U^mu U^nu.
```

UVIR-003 Stage A provisionally chooses `U^mu` as an independent constrained
vector. It is aligned with, but not algebraically identified with, the
condensate current. Treating it as both an independent aether and the derived
normalized current would double-count degrees of freedom unless a constrained
parent action were supplied. The independent-frame choice is not canonical
until the full coupled constraint and stability calculation passes.

Stage A retains all four symmetry-allowed two-derivative Einstein-aether
contractions. A restricted one-contraction frame action is not permitted as a
stability argument.

On the homogeneous flat-FRW branch, isotropy and the unit constraint fix
`U^mu=(1/N,0,0,0)`. The aether then renormalizes the cosmological gravitational
coefficient to
`M_cos^2=M_P^2+(M_U^2/2)(c1+3c2+c3)`. The alignment invariant vanishes because
the homogeneous condensate current is parallel to `U^mu`. UVIR-003 has
verified one regular dimensionless on-shell branch with conserved
`a^3 rho^2 dot(Theta)`. This is a background existence result, not a
cosmological parameter fit or perturbation-stability result.

The first scalar ADM subgate was completed in a controlled frozen-coefficient,
subhorizon limit. In aether-unitary scalar gauge, lapse and scalar shift
elimination independently reproduces the exact Einstein-aether spin-0 speed
and yields a positive principal block at the representative dimensionless
point. The condensate constraint introduces
`q_ADM^2=(rho_dot^2+rho^2 mu^2)/(M_U^2 c14)`, so that principal result is
restricted to `q_phys >> max(H,q_ADM)`.

The complete quadratic finite-`q` reduction has now also been performed on the
evolving branch. For all 48,861 representative samples with
`10^-3 <= q_phys/H <= 10^3`, the reduced kinetic inertia is three positive and
zero negative and the lapse-momentum constraint matrix is nonsingular. The
exact on-shell determinant is proportional to `q_phys^2`, so one kinetic
direction loses rank as `q_phys -> 0`. The follow-on gauge audit identifies
that direction exactly as `(H,rho_dot,mu)`, the homogeneous time-translation
orbit. Two gauge-invariant matter combinations retain a positive regular
`q=0` kinetic block across the representative trajectory. The rank loss is
therefore a gauge endpoint rather than a third physical homogeneous scalar.
The flat-decoupling khronon expansion is now verified through cubic order in
three spatial dimensions and exactly reproduces the earlier longitudinal
basis. For algebraic lapse and shift constraints, stationarity of the
first-order solution cancels every explicit second-order constraint correction
from the reduced cubic action. Linear-dispersion energy and momentum
conservation also force an on-shell three-point spatial triangle to be
collinear. The follow-on three-dimensional flat-decoupling quartic audit
contains 96 expanded monomials and gives the exact elastic contact form
`4[c123^2/c14-(2c123-c14)cos^2(theta)]`. Elastic `t/u` cubic exchange vanishes
exactly, while the centre-of-mass `s` channel is the non-invertible homogeneous
khronon gauge orbit. At quartic order the second-order constraint source enters
through `-J2^T C^(-1) J2/2`; third-order constraint solutions are unnecessary.
Consequently the physical interaction scale still requires the complete
gauge-regular constrained cosmological `2-to-2` amplitude and physical
eigenmode projection. The exact nonlinear `g+U+Phi+alignment` ADM parent block
reproduces the FRW and finite-`q` quadratic constraint data. Track A adopts the
rest-space Laplacian
`D_mu D^mu psi=h^{mu nu}nabla_mu nabla_nu psi+theta Q` and retains exact
`Y^(3/2)` for a declared local nonzero-gradient perturbative force analysis.
The homogeneous zero-gradient force action is verified through direct quartic
order: `Q^2` supplies lapse and scalar-shift `J2` components, the regulator
supplies a lapse component only, and exact `Y^(3/2)` is constraint independent
at cubic amplitude order on that background. The finite-`q` multi-sector
coefficient linear in constraints at the origin is assembled in the
`(delta_N,Sigma=q_phys^2 beta)` convention.

The constraint-dressing audit reclassifies this coefficient as
`J2_origin`, not the complete second-order source. The correct quantity is
`S2=partial_z L3[x,z1]`; the associated quartic correction is
`-S2^T C^(-1)S2/2`. The origin-linear formulas remain verified components.
This result is restricted to `q_phys>0` and does not reclassify the
homogeneous gauge orbit. Complete scalar-shift dressing, physical scalar
projection, gauge-regular amplitude, physical cutoff and global
multicone-causality testing remain open.

### 3.4 Infrared phonon sector

The local low-acceleration field is an emergent phonon `psi`, normalized so
that its spatial gradient can be interpreted as a potential-gradient scale.
Define

```text
Y = h^{mu nu} nabla_mu psi nabla_nu psi / a0^2.
```

The conditional low-acceleration EFT contains a `Y^(3/2)` operator. It is not
the fundamental vacuum action and it is not presently derived from the
Born--Infeld expression in v11.4.1. UVIR-001 also shows that a timelike
`P(Z) proportional to (Z-m^2)^(3/2)` obtained from the canonical sextic
condensate is not the same operator: its controlled static expansion begins at
quadratic order. UVIR-002 permits, but does not derive, the spatial operator by
separating the temporal invariant `Q = U^mu nabla_mu psi/a0` from `Y`. The
simple cubic force truncation has a degenerate quadratic spatial operator at
zero background gradient. UVIR-003 Stage A finds that a projected
higher-spatial-derivative regulator supplies a positive `k^4` dispersion in a
constant-frame flat decoupling limit. Its covariant completion, coupled
constraints, strong-coupling scale and technical naturalness remain open.

### 3.5 Matter sector

Matter fields are denoted collectively by `Psi_m`. A universal matter--phonon
vertex must produce both the nonrelativistic force and the corresponding
stress-energy exchange from the same interaction action. A conformal coupling
is a candidate for massive-matter dynamics, not a completed lensing theory.

### 3.6 Toroidal topology and moduli

Spatial slices have compact `T^3` boundary conditions with fundamental lengths
`L_i`. Topology determines:

- periodic boundary conditions;
- allowed momentum modes;
- winding and circulation sectors;
- defect classes;
- the treatment of zero modes;
- shape-dependent Casimir stress.

The side lengths or their ratios are moduli, not automatic numerical
invariants. A biaxial calculation may use `r = L_t/L_p`, but a value of `r` or a
Hubble-rate ratio must be dynamically derived.

### 3.7 Reservoir sector

The observable matter--plenum subsystem may be thermodynamically open. A
reservoir stress tensor `T_R^{mu nu}` accounts for the compensating exchange so
that the complete covariant system remains conserved. The reservoir is
external only to the observable subsystem; it is inside the complete covariant
theory and is not an unmodelled violation of the Bianchi identity.

The UVIR-003 background-completion screen rejects using an unspecified
constant or healthy two-derivative `P(X)` reservoir as an exact Minkowski
counterstress for the finite-density condensate. The least-assumptive working
route is a self-consistent evolving flat-FRW background. This selects a
background architecture, not a solution: the homogeneous equations and
perturbations still have to be derived, and any higher-derivative
NEC-violating reservoir would be a new theory requiring its own gate.

### 3.8 Wake and memory sector

The historical ITSM wake is retained only as a research hypothesis: the plenum
may have a causal relaxation or retarded response that is not captured by the
static phonon equation. Any wake variable must have an equation of motion,
initial data, an energy accounting and a causal characteristic structure.

### 3.9 Shape and anisotropic-stress sector

The free Casimir tensor is one source of anisotropic pressure. A driven theory
may also contain shape, elastic or memory contributions, but each requires a
declared action or constitutive law. Energy injection alone does not imply
directional stress.

## 4. Effective field hierarchy

The allowed logical ordering is

```text
S_UV[Phi, g, ...]
    -> choose a finite-density background
    -> integrate out heavy amplitude fluctuations
    -> obtain S_IR[psi, U, g, ...]
    -> match the matter vertex
    -> take controlled static or cosmological limits.
```

The current conditional target is

```text
L_IR = -(2 C_IR/3) M_P^2 a0^2 Y^(3/2) + higher operators.
```

Here `C_IR` is a normalization-dependent Wilson coefficient. Identifying it
with the geometric projection factor `2/3` is a matching hypothesis until
MAT-001 closes. UVIR-001 did not produce this coefficient because the required
spatial operator was absent. UVIR-002 selected a provisional route but did not
derive the coefficient or close its stability problem. MAT-001 is therefore
blocked until UVIR-003 validates the selected two-sector preferred-frame
action.

An analytic microscopic theory may yield a non-analytic finite-density EFT.
Therefore non-analyticity of the phonon action is not, by itself, a pathology.
The branch, stability and cutoff must nevertheless be specified.

## 5. Weak-field limit

Under the normalization used by the weak-field gate, the static action is

```text
S_WF = integral dt d^3x [
  -|grad Phi_N|^2/(8 pi G)
  -rho_b Phi_N
  -C_IR |grad psi|^3/(12 pi G a0)
  -C_m rho_b psi
].
```

For general positive coefficients, variation and spherical integration give

```text
q^2 = (C_m/C_IR) a0 g_N,
g_P = C_m q,
C_obs = C_m^(3/2) / sqrt(C_IR),
g_P = C_obs sqrt(a0 g_N).
```

Thus only the observable combination `C_obs` is invariant under phonon-field
renormalization. Under the special convention `C_m = C_IR = C`, one has
`C_obs = C` and variation reduces to

```text
div[(|grad psi|/a0) grad psi] = 4 pi G rho_b.
```

For a high-symmetry compensated local source this yields the square-root
branch. For a finite disk it is a nonlinear boundary-value problem with a
generally nonzero solenoidal field. The pointwise algebraic disk relation is
not the exact solution.

## 6. Compact-space decomposition

On `T^3`, a periodic divergence equation requires a zero-mean source. Split

```text
rho_b = bar(rho_b) + delta(rho_b),
psi   = bar(psi)(t) + varphi(t,x),
integral_T3 delta(rho_b) dV = 0,
integral_T3 varphi dV = 0.
```

The local equation has the schematic form

```text
D_i[(|D varphi|/a0) D^i varphi]
    = 4 pi G (C_m/C_IR) delta(rho_b) + S_Q,
```

with the total right-hand side integrating to zero. Here `S_Q` is a conditional
zero-mean scalar source induced by the inhomogeneous reservoir exchange,
schematically `S_Q = S_Q[delta Q_syn]`; the baseline local calculation sets
`S_Q = 0`. The homogeneous mode and the spatial perturbation are distinct
problems. A local spherical result is a
small-region, quasi-static compensated-overdensity limit, not a statement that
the global universe is isolated or spherical.

## 7. Conservation and exchange

Use two distinct exchange currents:

```text
nabla_mu T_m^{mu nu} = Q_mp^nu,
nabla_mu T_P^{mu nu} = -Q_mp^nu + Q_syn^nu,
nabla_mu T_R^{mu nu} = -Q_syn^nu.
```

Therefore

```text
nabla_mu (T_m^{mu nu} + T_P^{mu nu} + T_R^{mu nu}) = 0.
```

`Q_mp^nu` describes local momentum and energy exchanged between matter and the
plenum. `Q_syn^nu` describes reservoir throughput. They need not have the same
functional form and must not be combined into an undifferentiated source.

Stress-energy exchange is also distinct from condensate-charge exchange. If
`n` is the finite-density U(1) charge density, an isolated homogeneous
condensate obeys `dot(n)+3 H n=0`. Exact constant `n` in an expanding state
would require a separately declared source `S_N=3 H n`. `Q_syn^nu` is not
automatically `S_N`; their relation must follow from a reservoir interaction
if both energy-momentum and condensate charge are transferred.

A timelike `Q_syn^nu` injects energy but does not automatically produce an
anisotropic pressure `Pi = p_t - p_p`. Conversion of throughput into shear is
an independent constitutive or action-level problem.

For the biaxial convention `delta = H_t - H_p`, use

```text
pi^i_j    = diag(-2 Pi/3,  Pi/3,  Pi/3),
sigma^i_j = diag(-2 delta/3, delta/3, delta/3),
pi^{mu nu} sigma_{mu nu} = (2/3) Pi delta.
```

The exact plenum continuity equation is therefore

```text
dot(rho_P) + 3 H (rho_P + p_P) + (2/3) Pi delta = Q.
```

## 8. CBR-001 canonical result

The rectangular periodic scalar lattice calculation establishes that unequal
torus lengths produce unequal directional Casimir pressures. The validated
biaxial backreaction solver further establishes, for the tested free-field
de Sitter model, that:

- `H_t/H_p = 13/12` is mathematically reachable for some tuned amplitudes;
- the crossings are short transients;
- no quasi-plateau or attractor is produced;
- all valid target-reaching trajectories return to `H_t/H_p = 1`;
- the required target-reaching amplitudes are marginal or nonperturbative.

For the physical biaxial lengths the source has the qualified scaling

```text
Pi_Cas(a,r) = (hbar c/L_*^4) a^(-4) F_Pi(r),
F_Pi(r) = r^(8/3) [p_t_hat(r) - p_p_hat(r)].
```

The explicit scale factor is radiation-like, while the shape function evolves
with `r`. Thus topology-dependent anisotropic stress is retained as a derived
mechanism. A persistent `13/12` attractor in the tested free periodic-scalar
model is **Rejected**. A persistent ratio in a separately derived driven ITSM
sector is **Open**, not established. Cycle-counting derivations of the number
and `H0 = 72.97` as a parameter-free prediction are not retained.

## 9. Regime boundaries

The recovered architecture distinguishes:

1. weak metric and low acceleration: conditional phonon EFT;
2. weak metric and high acceleration: screening/decoupling gate;
3. strong field: full relativistic completion;
4. homogeneous cosmology: background plus reservoir equations;
5. non-equilibrium transients: wake and relaxation dynamics.

Success in one regime does not establish another.

## 10. Status vocabulary

All claims use exactly one of these statuses:

- **Derived:** follows from declared assumptions through a checked calculation;
- **Conditional:** follows only after a named postulate, matching hypothesis or
  restricted limit;
- **Open:** a defined calculation or empirical test remains incomplete;
- **Rejected:** the stated derivation or implementation has failed and may not
  be presented as live support.

## 11. Prohibited shortcuts

The canonical theory may not:

- equate the present Born--Infeld action with the `Y^(3/2)` phonon EFT;
- equate a timelike `P(Z) proportional to (Z-m^2)^(3/2)` equation of state
  with the spatial `Y^(3/2)` operator about a finite-density background;
- identify a trace ratio with a normalized local force vertex without matching;
- infer directional stress solely by counting torus cycles;
- describe a transient target crossing as an attractor;
- violate total covariant stress-energy conservation;
- infer anisotropic pressure from energy injection alone;
- use a static algebraic force as a quantitative collision simulation;
- claim lensing or PPN closure from a massive-matter force alone;
- mix parameters from different cosmological background branches;
- promote a code output whose advertised statistic was not computed.

## 12. Dependency rule for predictions

Every observable claim must name its upstream sectors and gates. Examples:

- galaxy rotation curves depend on UVIR-003, MAT-001 and DISK-001;
- Solar-System statements depend on SCR-001 and LEN-001;
- lensing depends on LEN-001;
- persistent anisotropy depends on TOP-001, the reservoir model and CBR-002;
- cluster offsets depend on WAK-001, LEN-001 and CLU-001;
- CMB and growth depend on COS-001 and PERT-001.

Until those dependencies close, the corresponding result remains conditional
or open rather than a framework-level prediction.
