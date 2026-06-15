## 2026-06-15T14:00:00Z
Analyze the CLASS codebase inside c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim.
Investigate include/background.h, source/background.c, source/input.c, and python/classy.pyx.
Find the exact files, lines, and structures to modify to support Strategy 2 (Fluid Mapping) for the ITSM model.
Provide exact code change templates for:
- Defining itsm_n0 and itsm_na in include/background.h
- Initializing and parsing them in source/input.c
- Incorporating the ITSM case in background_w_fld in source/background.c
Verify how to compile the modified C code and build/install the classy python wrapper.
Write your findings and code snippets to analysis.md and a final handoff summary to handoff.md in your working directory c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\explorer_m2_m3_1.
