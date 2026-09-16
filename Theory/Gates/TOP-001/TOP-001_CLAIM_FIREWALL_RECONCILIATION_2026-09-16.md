# TOP-001 claim-firewall reconciliation — 16 September 2026

**Gate:** `TOP-001 / CBR-002`
**Current research status:** `SCOPED_NEGATIVE_FREE_DILUTION` / `OPEN_SCAFFOLD_ONLY`
**Physics pass:** `false`
**Gate effect:** `NONE`
**Branch:** `recovery/v12-core-architecture`

## Why this reconciliation was required

The dated TOP-001/CBR-002 report and three legacy executables contained
pass-like names and, in two JSON outputs, `physics_pass=true` fields. Their
underlying calculations were bounded controls, not a completed TOP research
gate: the static stress code uses a finite direct lattice box plus internal
Richardson extrapolation, while the driven ODE code inserts an external
`eta_drive` source instead of deriving a modulus action or `Q_syn`.

The executable claim surfaces have been corrected. The legacy numerical
content is preserved as audit provenance; the current receipts below are the
authoritative bounded outputs.

## Re-executed bounded controls

### Static Epstein stress control

`top001_3d_epstein_casimir_tensor.py` evaluates the declared static expression
on finite symmetric lattice cutoffs and extrapolates against `1/N`. The cubic
control returned

- `rho_Cas = -0.8374896777147043` against the frozen reference
  `-0.83753691` (relative difference `5.6394e-5`); and
- a truncated-expression trace residual of `6.11e-16`.

The trace result is an internal identity of the same truncated sum. It is not
an independent Ewald/functional-equation validation or a curved-spacetime
renormalized stress calculation.

Current receipt:

```text
Analysis/TOP/TOP-001/outputs/top001_3d_epstein_casimir_summary.json
309BB2420FC389D9E73E380A9C1FED7D00B7208976067A7BCEF4F859C3636BF3
physics_pass=false
```

### Passive and inserted-source moduli controls

The coupled toy control returns `H_t/H_p = 1.00000387` at `z=0` for the
passive run, with final `u_sigma = 1.290096e-6` and measured decay slope
`-2.68` in e-fold time. This supports the scoped negative statement that the
implemented passive closure isotropizes in its tested domain.

The same toy with an inserted drive gives `H_t/H_p = 1.072807` for
`eta_drive=0.375`, not the historical `13/12` target; the final velocity is
nonzero (`u_sigma = 0.023145`), so the shape modulus drifts. This is a
conditional sensitivity result, not evidence for a stationary syntropic
attractor.

Current receipts:

```text
Analysis/TOP/TOP-001/outputs/top001_driven_moduli_summary.json
763BB330587A0F0937A15F4A6E1D35A95AC52C7401E4745305E8A7067687E0FC
physics_pass=false

Analysis/TOP/TOP-001/outputs/top001_coupled_moduli_summary.json
fa5a900a591fe78519bf684c846624cddc1ac1ff10117e1ec04569502ac72bfe
physics_pass=false
```

All three controls were repeated with byte-identical JSON/sidecar results.
A scan of `Analysis/TOP/TOP-001/outputs/*.json` finds no remaining
`"physics_pass": true` output.

The coupled receipt also exposed and received a Windows text-mode hashing fix:
the sidecar now hashes the bytes actually written rather than the pre-write LF
string. `top001_claim_firewall_audit.py` checks all three receipts for the
fail-closed fields, relative-path hygiene and sidecar agreement.

## Remaining research blockers

TOP-001 cannot be promoted from its scaffold/negative status until the chosen
route supplies a declared modulus action or fixed-boundary physical class with
energy accounting and stability treatment. A driven CBR-002 result additionally
needs a derived reservoir/source sector, exact exchange bookkeeping and an
independent dynamical stress calculation. Twisted-boundary preference, VOR
winding coupling and WAK/reservoir stress remain separate interfaces.

No `13/12`, `H_0`, `a_0`, `C_obs`, MAT-001, UVIR-003, cosmology, publication or
Rule-9 status changes follow from this reconciliation.
