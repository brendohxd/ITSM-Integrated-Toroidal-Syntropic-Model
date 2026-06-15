## 2026-06-15T06:38:46Z
Your working directory is: c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\.agents\worker_compile_1

Your task is to run the compilation and verification commands for CLASS C and classy Python wrapper.
Navigate to the directory:
c:\Users\brend\OneDrive\Documents\ITSM - Github\ITSM-Integrated-Toroidal-Syntropic-Model\Analysis\Experimental\CLASS_Sim

Run the following commands using the `run_command` tool in sequence. Ensure you propose each command and wait for execution/approval:
1. `mingw32-make clean` (to clean previous builds)
2. `mingw32-make libclass.a -j` (to build the CLASS library)
3. `pip install -e .` (to compile and install the classy python wrapper in editable mode)
4. `python verify_classy.py` (to run the verification script)

Document the output of each command in a handoff report `handoff.md` in your working directory.
Ensure that the output of `python verify_classy.py` is included in full.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
