# SPARC local input audit v1 — 1 November 2026

Question: which local radial tables and catalogue fields are available for a
future common-nuisance SPARC/lensing analysis, and what data issues need resolving?

Executable: `Analysis/DISK/DISK-001/sparc_input_audit_v1.py`.
Input scope: existing files directly under `Data/SPARC_data`; no downloads.
All input bytes receive SHA-256 pins. No existing files or sidecars are edited.

Check all radial rows for eight finite columns, positive radius and reported
velocity error, and strictly increasing radii. Record malformed line numbers.
Preserve signed gas contributions and errors below 1 km/s. Compare standard and
alternate copies by byte and parsed numeric identities; use standard filenames
for the inventory without asserting superior provenance. Check name joins and
duplicate/missing metadata names. Report issues without changing or dropping data.

Acceptance: fresh deterministic receipt, explicit issues/joins and exact read-only
replay. This establishes only the executed local structural checks, not upstream
provenance, full metadata completeness, statistical validity or physical success.
Existing data have already been examined; this is not fresh blind confirmation.

No fit, coefficient selection, MCMC, field solution, weak-lensing likelihood or
new physical claim is authorized by this diagnostic. DISK/STAT/MAT parent holds
remain. Rule-9 review is deferred and does not block this provisional data work.
