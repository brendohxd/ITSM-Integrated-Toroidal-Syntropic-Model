# Independent range verifier V2: allocation correction

27 October 2026. Primary symbolic V1 passed 23/23. Independent V1 stopped before
its first mathematical check: mpmath.matrix(20) allocated a square matrix where
the predicted inverse action required a 20-by-1 vector. IndexError and full
traceback are preserved in ignored output-0d1d638230364d35962eb60dda108044.txt,
SHA256 7a0e31d5fc7616fb0392c91a23325216bf50770fa3855d8fdf27c129f64bb359.
V1 source/sidecar remain unchanged; no V1 numerical receipt was produced.

New verify_01_r4c1_physical_sector_range_v2.py changes only its version docstring
and v=mp.matrix(20,1). All equations, metrics, frame values, arithmetic precision,
steps, acceptance criteria, controls and output/replay logic remain unchanged.
V2 is authorized by the frozen addendum's new-version repair rule. Freeze its
source hash before execution and use a fresh independent V2 receipt directory.
This implementation correction is not a repaired physics failure or new action.
