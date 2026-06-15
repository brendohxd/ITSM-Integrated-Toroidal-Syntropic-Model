# BRIEFING — 2026-06-15T05:13:00Z

## Mission
Inspect CLASS codebase for background Hubble parameter H(z) calculations and outline how to integrate ITSM equations.

## 🔒 My Identity
- Archetype: Teamwork Explorer
- Roles: Read-only investigator, analyzer
- Working directory: c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\explorer_setup_2
- Original parent: f839fe29-c1d3-449d-8825-5b4890ee9399
- Milestone: CLASS and ITSM Background Integration Analysis

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Do NOT compile or modify any files
- Code-only network mode (no external lookups)

## Current Parent
- Conversation ID: f839fe29-c1d3-449d-8825-5b4890ee9399
- Updated: 2026-06-15T05:13:00Z

## Investigation State
- **Explored paths**:
  - `include/background.h`: Declares background indices (`index_bg_H`, `index_bg_H_prime`).
  - `source/background.c`: Contains `background_functions` (computes H at line 579, H' at line 582), `background_w_fld` (defines fluid EoS), and `background_derivs`.
  - `python/classy.pyx`: Exposes background to Python via `Hubble(z)` and `get_background()`.
  - `Scripts/itsm_desi_bao.py` & `Scripts/itsm_desi_evolving_n.py`: Define ITSM Hubble rate with syntropic volume decay.
- **Key findings**:
  - CLASS computes the Hubble parameter in `background_functions` via $H = \sqrt{\rho_{\text{tot}} - K/a^2}$.
  - The Python wrapper uses spline interpolation of the precomputed table via `background_at_z` to return $H(z)$.
  - The ITSM model can be elegantly integrated into CLASS using **Strategy 2 (Fluid Mapping)** by mapping the Plenum's syntropic decay component to CLASS's existing fluid `fld` component with an effective equation of state $w(a) = -1 - \frac{1}{3}[n_0 + n_a(1-a) - n_a a \ln(a)]$. This method is highly recommended as it preserves the CLASS perturbation engine (PPF mode).
- **Unexplored areas**:
  - Custom modifications to CLASS's perturbation equations if non-adiabatic couplings are introduced.

## Key Decisions Made
- Selected Strategy 2 (Fluid Mapping) as the recommended implementation approach due to stability and perturbation compatibility.

## Artifact Index
- c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\explorer_setup_2\ORIGINAL_REQUEST.md — Original request copy
- c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\explorer_setup_2\BRIEFING.md — Memory briefing index
- c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\explorer_setup_2\progress.md — Progress log (100% complete)
- c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\explorer_setup_2\analysis.md — Technical analysis report
- c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\explorer_setup_2\handoff.md — Handoff report
