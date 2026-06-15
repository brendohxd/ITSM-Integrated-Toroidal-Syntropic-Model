# BRIEFING — 2026-06-15T14:19:00+08:00

## Mission
Modify standard CLASS simulation code to support the ITSM fluid equation of state, compile it on Windows, install the classy Python wrapper, and verify correctness.

## 🔒 My Identity
- Archetype: implementer/qa/specialist
- Roles: implementer, qa, specialist
- Working directory: c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\worker_m2_m3_1
- Original parent: dc423b02-194c-4fc3-afcb-94e2683e118f
- Milestone: Milestone 2 & 3 Integration and Verification

## 🔒 Key Constraints
- CODE_ONLY network restrictions: no external downloads or HTTP requests.
- Handoff report structure (Observation, Logic Chain, Caveats, Conclusion, Verification Method).
- All communications to the parent agent must go through `send_message`.
- Integrity Mandate: Do not cheat, do not hardcode tests, maintain real logic.

## Current Parent
- Conversation ID: dc423b02-194c-4fc3-afcb-94e2683e118f
- Updated: not yet

## Task Summary
- **What to build**: Modify standard CLASS simulation code (in `include/background.h`, `source/input.c`, `source/background.c`, `python/cclassy.pxd`) to implement the ITSM fluid equation of state (equation of state parameters `itsm_n0`, `itsm_na`). Patch `setup.py` to compile on Windows using `mingw32-make`. Compile and install the `classy` python package, and verify it runs successfully.
- **Success criteria**: Successful compilation of C library and classy wrapper, successful execution of a python script importing classy and running with `fluid_equation_of_state = 'ITSM'`.
- **Interface contracts**: Details in `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\explorer_m2_m3_1\analysis.md`.
- **Code layout**: CLASS simulation code at `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim`.

## Change Tracker
- **Files modified**: None
- **Build status**: Untested
- **Pending issues**: None

## Quality Status
- **Build/test result**: Untested
- **Lint status**: Untested
- **Tests added/modified**: None

## Loaded Skills
- None

## Key Decisions Made
- [TBD]

## Artifact Index
- `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\worker_m2_m3_1\handoff.md` — Final handoff report (to be created)
- `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\worker_m2_m3_1\progress.md` — Progress tracking file (to be created)
