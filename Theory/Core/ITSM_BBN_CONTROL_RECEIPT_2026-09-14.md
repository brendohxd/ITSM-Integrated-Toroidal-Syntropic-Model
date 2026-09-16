# BBN-001 bounded control receipt — 14 September 2026

**Record type:** `BOUNDED_BBN_CONTROL_RECEIPT`
**Status:** `CONTROL_ONLY`
**Physics pass:** `false`
**Gate effect:** `NONE`
**Publication status:** `NOT_A_PHYSICS_CLAIM`

## Scope

This checkpoint repairs and tests a schema-compatibility defect in the local
CAMB BBN table adapter. The adapter previously required the exact default
axis label `ombh2`, while `PRIMAT_Yp_DH_ErrorMC_2024.dat` labels the same
column `Ombh2`. The permanent rule is now: prefer an exact header match,
accept one unique case-insensitive match, and reject missing, ambiguous,
non-rectangular or header/data-width-mismatched schemas.

The case-insensitive match is a software compatibility rule. It does not
transform the numerical table, derive an ITSM parameter, or establish a BBN
prediction for the ITSM model.

## Executed checks

The executable control is
`Analysis/Cosmology/BBN-001/bbn001_control.py`. It checks all five bundled
tables, their axis domains and monotonicity, finite control outputs, the
`Y_p`/`Y_He` convention, a standard-table `DeltaN=0` to `DeltaN=1` response,
and the PRIMAT 2024 CAMB bridge. It also compares the automatic path with
both the former explicit `("Ombh2", "DeltaN")` workaround and the default
spelling supplied explicitly.

The focused regression suite is
`CAMB_ITSM_Solver/camb/tests/bbn_test.py`:

```text
python -m unittest camb.tests.bbn_test
....
Ran 6 tests
OK
```

The control was run twice. Both runs produced the same summary bytes and the
same SHA-256 sidecar:

```text
50ea60374901ecf5c0552c7eb14cd6e8889fe821f9e51d8f21d85a15d8083e52
```

The recorded runtime was Python 3.13.9, NumPy 2.3.5, SciPy 1.16.3 and CAMB
1.6.7. The receipt is stored at
`Analysis/Cosmology/BBN-001/outputs/bbn001_control_summary.json`.

At the frozen control point `ombh2=0.02237`, `DeltaN=0`, the automatic
PRIMAT 2024 path records:

- `Y_p` nucleon fraction: `0.2469869726389484`;
- `Y_He` mass fraction passed to CAMB: `0.2456560393606866`; and
- `D/H`: `2.446399134054883e-05`.

These values are software/control outputs from a bundled external table. They
are not an action-derived ITSM result.

## Review and physics boundary

Independent reproduction is `NOT_COMPLETED`; three-way consensus is
`NOT_MET`; the external BBN likelihood is `NOT_IMPLEMENTED`; and the ITSM
early-time mapping is `NOT_DERIVED`. This checkpoint therefore does not
change `MAT-001`, `UVIR-003`, TOP-X4, Rule 9 or publication status.

The next publishable-level BBN work still requires an action-derived early
plenum background and `Q^mu`, `G_eff(z)`, perturbation matching, nuclear-rate
and neutron-lifetime nuisance treatment, independent empirical-helium
likelihoods, frozen Planck/DESI data and covariance, preregistered controls,
and independent reproduction/review.
