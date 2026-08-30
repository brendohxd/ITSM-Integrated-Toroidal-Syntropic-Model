# CBR-002 S0 no-screening control

**Calculation:** `PASS_STATIC_NULL_CONTROL`  
**Disposition:** `REJECT_S0_AS_COMPLETE_LOCAL_GRAVITY_ROUTE`  
**Physics pass:** `false` · **MAT-001:** `BLOCKED`

## Exact bounded result

The unscreened standalone cubic branch gives

`g_P/g_N = C_obs sqrt(a0/g_N) = C_obs r/r_M`.

For any like-for-like fractional-force limit `epsilon`, this branch fails when

`abs(C_obs) > epsilon sqrt(g_N/a0) = epsilon r_M/r`.

Using `a0=1.2e-10 m/s^2` only as a diagnostic control value, the Sun
at 1 AU gives `0.00014225 * C_obs`. This reproduces the repository's
force-ratio diagnostic. It is not `gamma_PPN-1` and is not a Cassini verdict.

## Domain audit

- Solar System: the nonzero force ratio is exposed, but the physical metric,
  PPN parameters, Shapiro delay and ephemeris residuals are absent.
- Laboratory: the isolated-source scaling is calculable, but the nonlinear
  external-field/apparatus boundary-value problem is absent.
- Pulsars: a static weak-field ratio is calculable, but scalar radiation and
  strong-field sensitivities are absent.
- Compact objects: the current weak-field branch cannot be promoted to a
  neutron-star or black-hole prediction.

S0 is rejected as a complete local-gravity route. This is a null-control
failure of completeness, not evidence for kinetic screening, condensate
disruption, or any other S1-S4 mechanism.
