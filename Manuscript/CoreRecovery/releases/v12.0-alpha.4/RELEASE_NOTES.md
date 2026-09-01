# ITSM Core v12.0-alpha.4

Date: 29 July 2026  
Label: Complete finite-q J2 and Schur checkpoint

## Scientific advance

This release assembles the complete quadratic lapse/scalar-shift source `J2`
for the finite-wavenumber scalar system on the homogeneous zero-gradient force
branch.

The calculation:

- expands the fixed nonlinear
  `gravity+aether+condensate+alignment` ADM parent action;
- regresses exactly to the previously verified linear constraint source `J1`;
- combines the parent source with the adopted Track-A force contribution;
- expresses the shift source in the existing
  `Sigma=q_phys^2 beta=-D^2 beta` convention;
- inverts the exact finite-`q` constraint matrix; and
- verifies the constraint-induced quartic functional
  `-J2^T C^(-1)J2/2` by direct completion of the square.

The release status is
`PASS_COMPLETE_FINITE_Q_J2_AND_SCHUR`.

## Scientific boundary

This release does not close UVIR-003.

Still open:

- the direct multi-sector cubic and quartic contact actions;
- projection onto the regular physical-scalar eigenmode basis;
- the gauge-regular cosmological `2-to-2` exchange-plus-contact amplitude;
- a unitarity criterion or physical cutoff;
- the local nonzero-gradient reduction of exact `Y^(3/2)`;
- MAT-001.

The inverse-Laplacian shift representation is restricted to `q_phys>0`. The
existing homogeneous time-translation gauge-orbit result is unchanged.

## Reproduction

From the repository root:

```powershell
python Analysis/UVIR/UVIR-003/uvir003_nonlinear_adm_action_provenance.py
python Analysis/UVIR/UVIR-003/uvir003_track_a_force_adm_cubic.py
python Analysis/UVIR/UVIR-003/uvir003_full_j2_schur.py
```

Expected final status:

```text
STATUS: PASS_COMPLETE_FINITE_Q_J2_AND_SCHUR
```

The machine-readable result is:

```text
Analysis/UVIR/UVIR-003/outputs/uvir003_full_j2_schur_summary.json
```
