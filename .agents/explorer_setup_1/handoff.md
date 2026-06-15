# Handoff Report - CLASS Setup Analysis

This report summarizes the findings of Explorer Setup 1 regarding the Cosmic Linear Anisotropy Solving System (CLASS) repository setup and the targeted files for the background Hubble parameter $H(z)$ computation.

## 1. Observation
- **Workspace Directory Structure**:
  We ran `list_dir` on `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis` and verified the subdirectories are:
  `{"name":"Experimental", "isDir":true}`, `{"name":"Hierarchical_H0", "isDir":true}`, `{"name":"Simulations", "isDir":true}`.
  We then ran `list_dir` on `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental` and found the following contents:
  `{"name":"BTFR_v1", "isDir":true}`, `{"name":"CAMB_CMB", "isDir":true}`, `{"name":"CAMB_Matter", "isDir":true}`, `{"name":"Joint_MCMC", "isDir":true}`, `{"name":"MCMC_v2", "isDir":true}`, `{"name":"NANOGrav_v2", "isDir":true}`, `{"name":"RAR_v2", "isDir":true}`, `{"name":"README.md", "sizeBytes":763}`.
  No directory named `CLASS_Sim` exists in `Analysis\Experimental\`.
- **CLASS Codebase Structure**:
  Standard CLASS structure for background calculations consists of:
  - `include/background.h`: Defines the `background` structure and indices (e.g. `index_bg_H`, `index_bg_H_conf`).
  - `source/background.c`: Integrates Friedmann equations (`background_derivs` / `background_equations`) and interpolates background quantities (`background_at_tau`).
  - `python/classy.pyx`: Cython wrapper interface exposing background quantities to Python (e.g. `get_background()` method).

## 2. Logic Chain
1. *Premise*: We need to clone the public repository `https://github.com/lesgourg/class_public.git` into `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim`.
2. *Observation*: The target directory `CLASS_Sim` does not exist yet under `Analysis\Experimental\`.
3. *Inference*: Running `git clone <repo> <target_dir>` will create the directory `CLASS_Sim` and clone the repository inside it. Since `Analysis\Experimental\` exists, Git can create `CLASS_Sim` directly.
4. *Premise*: We need to locate where the background Hubble parameter $H(z)$ is computed in the CLASS codebase.
5. *Knowledge of CLASS*: CLASS uses a modular structure where the background evolution is solved in `source/background.c` and declared in `include/background.h`, while Python bindings are compiled via Cython in `python/classy.pyx`.
6. *Inference*: Therefore, these three files (`include/background.h`, `source/background.c`, and `python/classy.pyx`) are the key targets for locating and analyzing the Hubble parameter computation.

## 3. Caveats
- Since this is a read-only investigation and we did not clone the repository yet, we cannot verify line numbers of the standard files on the user's system.
- Standard CLASS releases might slightly alter internal names or indexing conventions (e.g., in CLASS version 3 vs older version 2), but the general structure (`source/background.c`, `include/background.h`, `python/classy.pyx`) remains consistent across all versions.

## 4. Conclusion
- The repository should be cloned using:
  `git clone https://github.com/lesgourg/class_public.git "c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim"`
- Once cloned, the key files to investigate for $H(z)$ computation are:
  - `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim\include\background.h`
  - `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim\source\background.c`
  - `c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim\python\classy.pyx`

## 5. Verification Method
- **Verify Repo Clone**:
  Run `git clone https://github.com/lesgourg/class_public.git "c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim"`.
  Then verify that the directory `CLASS_Sim` contains `Makefile` and `source/background.c`.
- **Verify File Contents**:
  View `CLASS_Sim\include\background.h` to verify that `index_bg_H` is defined.
  View `CLASS_Sim\source\background.c` to locate `background_derivs` / `background_equations` and search for references to `index_bg_H`.
