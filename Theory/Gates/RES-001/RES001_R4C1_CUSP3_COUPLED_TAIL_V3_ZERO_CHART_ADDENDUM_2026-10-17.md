# Coupled cusp tail V3: evaluate the homogeneous chart separately

17 October 2026. Frozen before V3 execution. Inherit V1 and the V2 complex
conjugation correction without weakening any acceptance, tolerance or field.
Conditional; review DEFERRED, physics_pass=false, gate_effect=NONE.

V2 preserved the full source Ward and acceleration identities and reached the
continuous bound construction, but its first independent numerical probe failed:
the single lambdified list evaluated both nonzero and homogeneous operators at
m=0 before selecting the homogeneous result. The resulting exception,
"0.0 cannot be raised to a negative power", invalidates numerical acceptance.
The outcome 23/26 and its frozen source/attempt02 remain unchanged.

V3 compiles two independent numerical functions and selects the correct chart
before evaluation. It never evaluates a 1/m nonzero inverse on the mean. The
symbolic mean and nonzero action reductions, seven input columns, all27 source
rows, initial preparation, continuous boxes, Fourier controls and tolerances
are unchanged. V3 includes the V2 Hermiticity and wrong-transpose rejection
controls. Its output is attempt03, with its own source, sidecar and replay.
Completed symbolic maps and bounds are retained in a partial case if later
numerical verification fails; that partial case remains unaccepted.

The leading-wave constants also have a direct check: with
Ew=|w_dot|^2+cV2*(40/a)^2*|w|^2 and |mV2|<9, the inherited background gives
40*sqrt(cV2)/a>12. Thus Ew_dot<=8Ew is conservative,
|w|<=a*exp(4t)<=25/19 and |w_dot|<=50<205/4. No division by w is required.

No physical-window, useful-accuracy, nonlinear-remainder, GR, matching,
publication, provider/model, vault or commit authority is added.
