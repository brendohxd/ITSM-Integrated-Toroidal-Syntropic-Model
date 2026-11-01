# Temporal audit V2 exact-comparison repair

The audit V1 receipt is 11/15. Three assertions compare structurally
different, mathematically identical SymPy expressions using Python `==`.
The fourth expected polynomial list omitted the zero coefficients of odd
powers. The exported scalar determinant is already the expected formula.
V2 tests simplified differences against zero and retains the full degree-six
coefficient list. No input, equation, determinant or numerical threshold
changes. Pin and preserve V1 and its failed receipt; recompute all checks.
This repair does not establish physical admission. All prior holds remain.
