# TOP-X4 `X4-S2F3` scoped curved Dirac-operator receipt

**Executed:** 2026-09-16  
**Checkpoint status:** `PASS_TOPX4_S2F3_CURVED_DIRAC_OPERATOR_SCOPED_HOLD_QUANTUM_CLOSURE`  
**Checks:** `13/13`  
**Contract/provenance checks:** `2/2`  
**Operator/rejection checks:** `11/11`  
**Operator status:** `DERIVED_HAMILTONIAN_FORM_ON_REGISTERED_HOMOGENEOUS_METRIC`  
**Covariant completion:** `SCOPED_ONLY_NOT_FULL`  
**Physics pass:** `false`  
**Gate effect:** `NONE`

## 1. Result

The executable derives and verifies the Hamiltonian-form neutral-spectator
Dirac operator on the registered homogeneous metric

\[
 ds^2=-N(t)^2dt^2+a(t)^2d\mathbf{x}^2+b(t)^2dy^2,
 \qquad y\sim y+2\pi.
\]

The torsion-free coframe connection is

\[
 \omega^{\hat i}{}_{\hat0}=H_a e^{\hat i},
 \qquad
 \omega^{\hat4}{}_{\hat0}=H_b e^{\hat4},
 \qquad
 \Theta=3H_a+H_b.
\]

After the declared spin-connection-removing rescaling

\[
 \Psi_c=(a^3b)^{1/2}\Psi,
\]

the periodic KK mode is

\[
 H_D=N\left(\alpha_{\rm obs}\frac{k_{\rm obs}}a
 +\alpha_y\frac{n}{b}+\beta m_F\right),
 \qquad n\in\mathbb Z.
\]

The 13 checks cover the coframe/metric identity, inverse frame, Hermitian
Clifford algebra, torsion-free connection, volume-rescaling term, lapse-scaled
dispersion relation, paired spectrum, and three rejecting mutations:

- wrong spin-connection sign;
- antiperiodic half-shift in the frozen periodic sector; and
- a direct scalar chemical-potential shift of a neutral spectator.

The executable now reports its two authority/contract checks separately from
its 11 operator/rejection checks. A future sidecar or wording mismatch remains
fail-closed, but cannot be mistaken for failed operator mathematics.

## 2. Scientific interpretation

This resolves one scoped operator-geometry prerequisite for the fermion sector.
It does not establish the full curved finite-charge Dirac input because the
finite-charge background and state domain are not yet solved. The existing
static parity-even determinant remains a separate control, and the first-order
Dirac transport result remains a finite-order state control.

The following remain open:

- dimension-appropriate Dirac Hadamard state;
- evolving finite-charge determinant and state-dependent stress;
- parity-odd determinant phase and regulator/reference definition;
- local and global anomaly calculation;
- quantized counterterm normalization;
- curved graviton/ghost and constraint coupling; and
- physical constrained Hessian.

No missing sector is set to zero. No parity phase is inferred from the squared
or Hamiltonian operator.

## 3. Gate boundary

The receipt does not change `X4-D2`, `physics_pass`, MAT-001, UVIR-003,
BBN-001, Rule 9, A4, Ultra or publication status. It is a prerequisite for a
later finite-charge determinant calculation, not that calculation itself.

## 4. Reproduction

```powershell
python -B Analysis/TOP/TOP-X4/topx4_s2f3_curved_dirac_operator_checkpoint.py
```

The deterministic JSON is
`Analysis/TOP/TOP-X4/outputs/topx4_s2f3_curved_dirac_operator_summary.json`.

## 5. Artifact hashes

| Artifact | SHA-256 |
|---|---|
| `topx4_s2f3_curved_dirac_operator_checkpoint.py` | `7f743fadac14041981770ce1df782c5360e251447206563ebfb6a8ebf04e7d44` |
| `topx4_s2f3_curved_dirac_operator_summary.json` | `54364768bfa4008f587011e8f1cc82effe6aa0facbab55e7f5808bc6bea9adb2` |
| `TOPX4_S2F3_CURVED_DIRAC_OPERATOR_CONTRACT_2026-09-16.md` | `65280699a5e641d2ffcc61fc4e97d1b28670cbcf9256330184d7c3d1593809b6` |
| `TOPX4_S2F3_PARENT_FREEZE_2026-09-06.md` | `37205506697e1f70f12b9ea3d8b093ccbccf11bbf0c19b680d00a43f28c6f945` |
| `topx4_s2f3_exact_transport_retry_summary.json` | `94ca65dd08419b650a8a135ddc5e7a6adf550ef788ee7a8759fa143786315747` |
