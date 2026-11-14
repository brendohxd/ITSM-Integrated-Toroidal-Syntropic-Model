# R-tau density drift V1 execution failure

The force partial used interval-times-Taylor-jet multiplication. mpmath
attempted to coerce the Taylor jet into an interval and raised
`NotImplementedError` before any result was produced. The original executable
and contract are preserved. V2 keeps the same equations and places Taylor
jets on the left of interval scalar multiplication so their arithmetic owns
the product. The optimizer retained the exact traceback under
`.local/itsm-context/output-2a1f7ff9d5284acb9ef00b9b2570604d.txt`.
