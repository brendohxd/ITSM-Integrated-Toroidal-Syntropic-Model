# Progress tracking

Last visited: 2026-06-15T14:38:00+08:00

## Done
- Verified that ITSM modifications are already correctly applied to `include/background.h`, `source/input.c`, `source/background.c`, and `python/cclassy.pxd`.
- Checked and confirmed that `setup.py` has been patched to use `mingw32-make` on Windows.
- Wrote the verification python script `verify_classy.py` to check the `classy` integration and mathematical correctness.
- Created `handoff.md` and updated `BRIEFING.md`.

## In Progress
- Waiting for compilation / wrapper installation execution by parent agent or when user is active to approve commands.

## To Do
- Run `mingw32-make clean && mingw32-make libclass.a -j` in the CLASS root directory.
- Run `pip install -e .` in the CLASS root directory.
- Run `python verify_classy.py`.
