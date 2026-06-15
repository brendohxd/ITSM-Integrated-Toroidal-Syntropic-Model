# BRIEFING — 2026-06-15T14:21:00+08:00

## Mission
Swap CLASS cosmological engine with ITSM physics, compile Python wrapper, and verify background/spectra outputs.

## 🔒 My Identity
- Archetype: teamwork_preview_orchestrator
- Roles: orchestrator, user_liaison, human_reporter, successor
- Working directory: c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\orchestrator
- Original parent: main agent
- Original parent conversation ID: c4b8219c-e546-4680-86f0-281b25fb5ecd

## 🔒 My Workflow
- **Pattern**: Project
- **Scope document**: c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\orchestrator\PROJECT.md
1. **Decompose**: Decompose the project into milestones for implementation, verification, and end-to-end testing.
2. **Dispatch & Execute**:
   - **Delegate (sub-orchestrator)**: Spawn sub-orchestrators for milestones or run Explorer -> Worker -> Reviewer cycles.
3. **On failure** (in this order):
   - Retry: nudge stuck agent or re-send task
   - Replace: spawn fresh agent with partial progress
   - Skip: proceed without (only if non-critical)
   - Redistribute: split stuck agent's remaining work
   - Redesign: re-partition decomposition
   - Escalate: report to parent (sub-orchestrators only, last resort)
4. **Succession**: at 16 spawns, write handoff.md, spawn successor
- **Work items**:
  1. Setup & Clone [done]
  2. Implement ITSM equations in CLASS [in-progress]
  3. Compile CLASS and verify classy wrapper [pending]
  4. Create verify_background.py and plot_spectra.py [pending]
  5. E2E Testing and Adversarial Hardening [pending]
- **Current phase**: 2
- **Current focus**: Implement ITSM equations in CLASS

## 🔒 Key Constraints
- NEVER write, modify, or create source code files directly.
- NEVER run build/test commands yourself — require workers to do so.
- You MAY use file-editing tools ONLY for metadata/state files (.md) in your .agents/ folder.
- Never reuse a subagent after it has delivered its handoff — always spawn fresh

## Current Parent
- Conversation ID: c4b8219c-e546-4680-86f0-281b25fb5ecd
- Updated: not yet

## Key Decisions Made
- Adopted Project pattern with dual tracks (Implementation & E2E Testing).
- Strategy 2 (Fluid Mapping) chosen for C modification to minimize core code disruption and ensure stability of perturbations.

## Team Roster
| Agent | Type | Work Item | Status | Conv ID |
|-------|------|-----------|--------|---------|
| sub_orch_setup | self | Milestone 1: Setup & Clone | interrupted | 21948115-a123-476f-8d6b-13a7d86df95a |
| sub_orch_setup_2 | self | Milestone 1: Setup & Clone (Resume) | completed | f839fe29-c1d3-449d-8825-5b4890ee9399 |
| explorer_m2_m3 | teamwork_preview_explorer | Analyze C code changes & build commands | completed | 5649f87c-dd5f-4ed1-965c-2f70aa87f3b5 |
| worker_m2_m3 | teamwork_preview_worker | Implement ITSM equations, compile CLASS & wrap | failed | 941dcb74-3439-4d04-8c55-a7a056cede75 |
| worker_m2_m3_2 | teamwork_preview_worker | Implement ITSM equations, compile CLASS & wrap (Replacement) | completed | f988f528-6451-4308-ba60-9ff25fbc1846 |
| worker_compile | teamwork_preview_worker | Compile C and python wrapper, run tests | in-progress | e3668c7e-f892-4bb6-bbab-a33baa1655d9 |

## Succession Status
- Succession required: no
- Spawn count: 6 / 16
- Pending subagents: e3668c7e-f892-4bb6-bbab-a33baa1655d9
- Predecessor: none
- Successor: not yet spawned

## Active Timers
- Heartbeat cron: task-70
- Safety timer: none
- On succession: kill all timers before spawning successor
- On context truncation: run manage_task(Action="list") — re-create if missing

## Artifact Index
- c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\orchestrator\PROJECT.md — Project plan, milestones, and interface contracts
- c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\orchestrator\progress.md — Progress tracking heartbeat
