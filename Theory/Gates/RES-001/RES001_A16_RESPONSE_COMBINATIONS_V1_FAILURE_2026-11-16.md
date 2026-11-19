# Preserved V1 implementation failure

V1 stopped before rank evaluation: AttributeError: int object has no attribute subs.
An empty symbolic derivative returned Python integer zero. V2 uses a SymPy
empty sum and selects an actually time-dependent proper-rate coefficient for
the independent derivative control. No action, equation, threshold or scope
was changed. Original V1 source and pins are preserved.
