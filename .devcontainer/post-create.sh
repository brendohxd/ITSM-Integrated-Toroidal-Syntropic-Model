#!/usr/bin/env bash
set -euo pipefail

printf '\n[ITSM] Installing cloud Python dependencies...\n'
python -m pip install --upgrade pip setuptools wheel packaging
python -m pip install -r .devcontainer/requirements-cloud.txt

printf '\n[ITSM] Building/installing the repository CAMB solver...\n'
python -m pip install -e ./CAMB_ITSM_Solver

printf '\n[ITSM] Registering Jupyter kernel...\n'
python -m ipykernel install --user --name itsm-cloud --display-name "Python (ITSM Cloud)" >/dev/null

printf '\n[ITSM] Running environment smoke test...\n'
python - <<'PY'
import os
import multiprocessing as mp

import numpy as np
import scipy
import pandas as pd
import matplotlib
import emcee
import corner
import sklearn
import sympy
import camb

print(f"Python cloud environment: OK")
print(f"CPU cores visible: {mp.cpu_count()}")
print(f"NumPy: {np.__version__}")
print(f"SciPy: {scipy.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Matplotlib backend: {matplotlib.get_backend()}")
print(f"CAMB: {getattr(camb, '__version__', 'version unavailable')}")
print(f"Workspace: {os.getcwd()}")
PY

if ! kpsewhich revtex4-2.cls >/dev/null 2>&1; then
    echo "[ITSM] ERROR: REVTeX 4.2 class not found in TeX installation." >&2
    exit 1
fi

printf '[ITSM] REVTeX 4.2: OK\n'
printf '[ITSM] Cloud environment ready.\n\n'
