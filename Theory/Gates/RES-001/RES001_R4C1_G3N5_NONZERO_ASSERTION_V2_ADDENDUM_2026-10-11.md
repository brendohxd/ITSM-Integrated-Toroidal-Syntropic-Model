# G3N5 nonzero audit v2: corrected verification assertions

Date: 11 October 2026. Freeze before v2 execution. Conditional; all parent holds
and the original acceptance contract remain. No action, derived matrix, adverse
sign, input background, numerical tolerance or failed original receipt is edited.

The main v1 run is retained as FAIL_LOCAL_CHECKS, 103/106. Its failed rows are:

1. `eliminated_gauge_multiplier_coordinates_have_no_one_form`: it incorrectly
   demanded that the dust and norm momenta vanish. T and nu are fixed coordinates
   in this chart, not null-velocity primary momenta. Their one-form contribution
   vanishes because dT=dnu=0. The corrected assertion checks zero primary
   momenta for alpha/Em/LambdaU and zero coordinate pullbacks for T/nu. The
   already-passing complete momentum one-form and evolving Hamilton/Euler
   identities remain unchanged. No dust charge is newly fixed.
2. `all_wave_scale_root_multiplicities`: the expected determinant prefactor was
   wrong by a factor two. Derive it from the complete exact det(K)=11/768 and
   the retained fast ratio b/K_Pi=5/33. The roots and multiplicities are unchanged.
3. `all_fast_scale_root_multiplicities`: the expected prefactor was wrong by a
   factor 3/2. The leading coefficient must be det(K), not a guessed constant.

V2 reuses v1's frozen calculation without calling its writing main. It corrects
only these assertions using the saved exact matrices and additionally checks
the complete 18-dimensional wave-scale companion and separate fast two-state
companion. The zero-speed Jordan chain and negative slow K=-11/6 are retained.
Fresh v2 outputs are separate; v1's full sources, sidecars and failed outputs
remain unchanged. A corrected assertion is not retroactive clearance of v1.

The separate principal-density v1 is also retained as FAIL_LOCAL_CHECKS, 7/9:
two charpoly assertions compared distinct Symbols with identical printed names
but different assumptions. Separate v2 uses each polynomial's actual generator,
passes 9/9, and retains byte-identical derived formulas. This is a local
implementation correction, not a changed density or external scientific review.

No claim of strong hyperbolicity or physical stability is authorized. The
wave-scale defect applies to the explicitly stated reduction and norm; a
different weighted well-posedness analysis of the mixed-order system is not
ruled out. No physical cutoff/causality, all-direction or nonlinear conclusion,
canonical promotion, commit, push, deployment or publication is included.
