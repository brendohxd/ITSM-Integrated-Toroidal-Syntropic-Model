# Initial controlling-energy time derivative

The [frozen contract](RES001_RTAU_ENERGY_TIME_DRIFT_V1_CONTRACT_2026-11-14.md)
now has a conditional whole-initial-root numerical bound for the registered
energy's time derivative. In the benchmark coordinate/time convention,

    ||Hdiag_t||infinity <3.651954e11,
    ||(T^dagger Hdiag T)_t||L2->L2 <9.371852e11.

These are conservative upper bounds, not measured growth rates. They do
not certify useful accuracy or the target interval [0,0.05]. The initial
energy coefficient drift is bounded; the full coupled energy inequality,
global-partner assembly and actual evolving-domain/time tube remain open.

## Same controlling energy, both zero-speed directions

Use the original ordinary eighteen-direction construction. Its invertible
chart F maps the ordinary state to (w,z,x), where x has sixteen components.
Let C16 be the existing complement generator, r its drive into z, and

    ell=r C16^-1, zeta=z-ell x.

The two zero-speed partners w and zeta are retained. With Jell implementing
(w,z,x)->(w,z-ell x,x), the registered ordinary energy is

    Hordinary=F^dagger Jell^dagger diag(1,1,HC) Jell F.

The complement action energy is the preserved expression

    HC=K^dagger M^-1 K-X^dagger G_R X, K=P-i B_R X.

The calculation differentiates every factor, including X(c(t)), both
inverse matrices and the stationary row:

    ell_t=(r_t-ell C16_t) C16^-1.

It does not assign the zero-sector or its rate to zero. The initial
complement inverse and coercivity certificates are reused. This is a
derivative along the registered exact compatible initial jets; it does
not construct an actual background solution over a time interval.

## Required action coefficients

The A/B/Cshift/Drel/Kshift time exports from the
[normal-form time owner](RES001_RTAU_NORMAL_FORM_TIME_DRIFT_V1_REPORT_2026-11-14.md)
are reused. Only the remaining nine-by-nine ordinary gradient-gradient
block is newly exported, using generic field variables and their actual
first-time jets. The established quadratic-sector/material identities
justify its independence from omitted background accelerations and its
zero-shift evaluation. Values are compared with the old full export after
the exact material correction. No full action Hessian is rerun.

Generic Schur and inverse derivatives precede initial-slice evaluation.
The actual scalar c_t, frame/metric rates, lapse and volume variations
are included. No future conformality or error-radius derivative is used.
The fast energy retains the full nonlinear force and certified proper
clock rate:

    Hfast=diag(d/kappa,aphi),
    d=b N mu kappa, aphi=N/(mu f_pp).

It gives ||Hfast_t||<1.146731 on the same initial root domain.

## Bound and its conditioning

Let f0,f1 bound F,F_t, L bound ell, Lt bound ell_t and
Eh=max(1,||HC||). The same factorized energy gives

    ||Hordinary_t|| <=2 f0 f1(1+L)^2 Eh
                      +2 f0^2(1+L) Lt Eh
                      +f0^2(1+L)^2 ||HC_t||,

    Lt <=(||r_t||+L ||C16_t||)||C16^-1||.

The inverse uses the preserved reference-energy normalization, including
the exact sqrt(99/2) conversion to coordinate norm. It is not a new
unverified inverse estimate. The actual chart has

    ||F||<=sqrt(17+3/(4 c_min^2)),
    ||F_t||<=sqrt(3)|c_t|/(2 c_min^2).

The three contributions, rounded upward, are:

| Contribution | Upper bound |
| --- | ---: |
| Chart time dependence | 1.632922e6 |
| Stationary-row time dependence | 3.651683e11 |
| Complement energy time dependence | 2.546194e7 |

Their interval sum has upper endpoint approximately 365195376308.444079.
The intermediate bound ||HC_t|| is below 265.032031, while the stationary
row derivative bound is below 2932631.466707. The latter, combined with
the coordinate/energy factors, dominates the final estimate. This is
conditioning and triangle-bound information; it does not demonstrate
either a physical instability or stability over a useful time interval.

With Hdiag=diag(Hordinary,Hfast), the original-state energy is the bounded
operator Horiginal=T^dagger Hdiag T. Its derivative satisfies

    ||Horiginal_t|| <=||T||^2 ||Hdiag_t||
                      +2||T|| ||Hdiag|| ||T_t||.

The result uses the actual previously bounded T_t. For an estimate in the
transformed state Z=T Y, use Hdiag_t and the generator term T_t T^-1;
for an estimate in the original state use Horiginal_t. Counting both
representations' time terms together would double-count that change.
The fixed original-coordinate L2 inner product is unchanged.

## Evidence and remaining scope

The [V2 executable](../../../Analysis/MasterTests/test_rtau_energy_time_drift_v2.py)
verified 436 pinned inputs and eighteen controls. Exact noncommuting
controls retain stationary-row, chart and complement-energy derivatives
with nonzero zero-sector inputs. Its
[receipt](../../../Analysis/MasterTests/outputs/rtau_energy_time_drift_v2_20261114/receipt.json)
replayed byte for byte. The
[separate audit](../../../Analysis/MasterTests/audit_rtau_energy_time_drift_v2.py)
passed twelve controls: closed scalar/frame gradient Hessians check values
and time rates, and exact rational arithmetic checks all aggregation and
pullback bounds. These are same-assistant checks, not an independent
review panel or Rule-9 clearance.

V1 stopped before receipt generation because the reused force-jet
environment lacked its time helper. Its source, sidecar and failure record
are preserved. V2 adds that helper; equations, norms, inputs and acceptance
thresholds are unchanged. Original research artifacts remain untouched.

Next assemble the supported full initial energy inequality with the
completed twenty-row remainder, principal spatial adjoints, physical
advection, T_t and the actual finite-dimensional mean/modulus/momentum
rates. The registered harmonic coordinate velocities are independent
inputs; do not silently set them or a missing rate to zero. Any forced
estimate must be distinguished from a closed autonomous physical estimate.
Actual compatible-domain and background/coefficient persistence are still
required before integration over time.

R-tau UNADOPTED; review DEFERRED; physics_pass=false; gate_effect=NONE.
This controlling energy is not a positive-Hamiltonian or universal ghost
verdict. No physical cutoff, interaction window, matching value or
canonical promotion is supplied.
