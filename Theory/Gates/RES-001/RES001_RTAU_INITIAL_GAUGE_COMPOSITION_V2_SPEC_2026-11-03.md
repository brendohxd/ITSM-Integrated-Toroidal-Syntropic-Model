# Initial gauge composition V2 exact-expression correction

3 November 2026. Inherit all requirements of the
[V1 specification](RES001_RTAU_INITIAL_GAUGE_COMPOSITION_V1_SPEC_2026-11-03.md).

V1 returned 19/20 controls. Its generic H2 chain-rule expression retained
equivalent Derivative/Subs forms under simplify alone. Inspecting the
exact residual showed both expand-then-simplify and doit-then-simplify
give zero. V2 expands that exact difference before checking zero. The
original requirement is retained; no term, tolerance or domain is removed.
Add an independent polynomial-composite check of the same second-derivative
formula without abstract Subs objects.

Preserve the V1 source, specification, sidecars and failed 19/20 receipt
unchanged; pin all of them in V2. Recalculate and perform exact read-only
replay in a fresh directory. Initial bounds remain scoped; no physical
energy, complete density generator or time-tube claim follows.
