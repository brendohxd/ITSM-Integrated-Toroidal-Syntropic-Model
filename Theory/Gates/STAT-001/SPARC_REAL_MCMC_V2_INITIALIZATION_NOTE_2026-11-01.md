# Real SPARC v2 initialization correction

The v1 real-data pilot completed 12 ensemble jobs but all four UGC01281 jobs
failed initialization. The failed output and v1 source remain intact.

UGC01281's first inward scalar template support requires U_disk greater than
approximately 15.21 for its bulgeless data. The fiducial .5 and ordinary draws
from the 0.1-dex lognormal prior almost never meet it. This is an extreme
conditional-model/prior conflict, not evidence for that stellar mass ratio.
Its uncertainty catalogue alone cannot cure this geometry/domain problem.

The new v2 initializer computes, for a proposed U_bulge, the exact lower bound
max_R[(-Vgas*abs(Vgas)-U_bulge*Vbulge*abs(Vbulge))/(Vdisk*abs(Vdisk))].
It samples log10 U_disk from a numerically stable truncated-normal tail above
that bound, and D/i within their physical truncated-normal supports. Initialization
need not follow the joint prior; no tail normalization is inserted into the
posterior. The likelihood, priors, force law, data, diagnostic thresholds and
pilot membership are unchanged. Nonpositive disk templates are explicitly
rejected as requiring a separate support chart, never silently clipped.

Source: `Analysis/STAT/STAT-001/sparc_real_mcmc_v2.py`.
Fresh pilot: `Analysis/STAT/STAT-001/outputs/real_pilot_v2_20261101/`.
The code and input hashes are pinned before launching in its run contract.
This correction is made after the v1 failure and is not claimed as a blind
pre-specified algorithm. Resume and incremental storage rules remain unchanged.
