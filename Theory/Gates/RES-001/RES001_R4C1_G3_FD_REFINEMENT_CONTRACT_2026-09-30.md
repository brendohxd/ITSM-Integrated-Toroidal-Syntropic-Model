# R4C1-G3-FD: supplementary balance-error refinement

Date: 2026-09-30. Frozen after G3 attempt 01's 801-point failure and before
this supplementary executable. G3's original contract, script, threshold,
112/113 result and all outputs remain intact. This is a **post-failure**
resolution study; it cannot retroactively turn that receipt into a pass.

Pin G3 attempt 01 summary
`930dc4300fe47698ef1b5938214811fda3b5aed6c4d96361e5f9cceebd4d7c75`,
its sampled trajectories
`b0179f04368a860baabe0d9713a65a809c638ffdab35edc7071a4656c77c6506`,
G3 executable
`dfdec7c78ae4e57f247b2592b611e79d808d708813358a6dac015c387a7d9440`,
and the original G3 contract
`4bb989979850468d4322baeec9cbdaaaadd8318825724042711c062fc944e9f8`.
Verify the original receipt's direct/transitive source maps and executable
hash before calculating. Use **only** the eta=1 parameters and initial state
stored there, unchanged. Integrate with the same DOP853/Radau methods,
`rtol=1e-11`, `atol=1e-13`, dense output and `[0,4]` domain.

Compare each fresh integration on 801 samples against its stored trajectory:
maximum `abs(new-old)/(1+abs(old))<1e-12`. Then evaluate B1's unchanged
five-point finite-difference sector balances and full spatial Einstein
residual on **801,1601,3201** samples for each method. The original 801
failure must remain reported. Require each finer-grid maximum sector and
spatial-metric normalized residual below the unchanged `1e-7` limit.
For each factor-two step require sector-balance improvement at least four,
or both errors below `1e-9`; finite differences can reach the integration
accuracy/cancellation floor. Exact method agreement does not by itself prove
continuum evolution or stability.

Write a separate numbered supplementary attempt with exact input hashes,
the original failed assertion, all grid/method residuals and checks.
Refuse an existing output directory. An in-memory replay must preserve all
earlier files. This diagnoses the numerical balance assertion only; tensor,
kinetic, GR-limit, all-sector/EFT, Test 2/3 and publication holds are unchanged.
`physics_pass=false`, `gate_effect=NONE`, `review_status=DEFERRED`,
`Rule9_cleared=false`. Failed or unresolved refinement retains its actual
result and requires further diagnosis without relaxing the acceptance bound.
