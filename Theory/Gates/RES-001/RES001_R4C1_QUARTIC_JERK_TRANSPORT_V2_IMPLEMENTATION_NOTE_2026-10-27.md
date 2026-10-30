# Jerk transport V2: interval representation of exact zero entries

27 October 2026. Same V1 scientific contract, equations, scope and criteria.
V1 source f1c5fabe603ab19bb5b02db653771899e1158111e95dcc81820ce6e354b346b1
is preserved. It stopped before numerical geometry controls/receipt because
SymPy's evaluator returns exact zero derivative entries as Python integers;
the interval endpoint helper requires an interval scalar. Failure log
.local/itsm-context/output-5ea5be56b77140d0af266e7e48e65dac.txt has SHA256
bc8f41e549b7daaee0017e970cc9aed3469fddf111f5aea2b899ea9f07ccd798.
V2 embeds every evaluated matrix derivative entry, including exact zero, into
the same outward interval scalar type before norm accumulation. No result,
equation, input domain or tolerance changes. Freeze V2 before launch.
