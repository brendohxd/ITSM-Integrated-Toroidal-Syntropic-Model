# ITSM Cloud Research Environment

This repository includes a reproducible Linux cloud environment under `.devcontainer/`, intended for GitHub Codespaces and other Dev Container-compatible hosts.

## Scope

The cloud environment is deliberately separate from the existing root `environment.yml`, which is a Windows-specific Conda export. The local Windows environment is therefore left unchanged.

The cloud image provides:

- Python 3.13 on Debian Bookworm.
- NumPy, SciPy, pandas, Matplotlib, emcee, corner, scikit-learn, SymPy, JupyterLab and the other core ITSM analysis dependencies.
- GNU Fortran and the native build toolchain required to build the repository's modified `CAMB_ITSM_Solver`.
- Editable installation of `CAMB_ITSM_Solver`, so changes to the solver source are immediately reflected in the Python environment.
- LaTeX, `latexmk`, `texlive-publishers`, and REVTeX 4.2 support for manuscript compilation.
- A post-create smoke test that verifies the scientific stack, CAMB import, visible CPU count, Matplotlib backend, and `revtex4-2.cls` availability.

## Start a Codespace

1. Open the repository on GitHub.
2. Choose **Code → Codespaces → Create codespace**.
3. Select the branch containing the cloud-environment configuration (or `main` after the configuration is merged).
4. Allow the initial container build and `postCreateCommand` to complete.

A successful first build ends with:

```text
[ITSM] REVTeX 4.2: OK
[ITSM] Cloud environment ready.
```

## Compute profile

The dev container specifies a minimum of:

- 4 CPU cores
- 8 GB RAM
- 32 GB storage

For full multi-core MCMC, CAMB parameter sweeps, or high-resolution simulation runs, select an 8- or 16-core Codespaces machine when available. Python `multiprocessing` and `concurrent.futures` will see the CPUs assigned to the Codespace.

## Verification commands

```bash
python -c "import numpy, scipy, pandas, matplotlib, emcee, corner, sklearn, sympy, camb; print('ITSM cloud imports: OK')"
python -c "import multiprocessing as mp; print('Visible CPUs:', mp.cpu_count())"
kpsewhich revtex4-2.cls
```

## Example execution

Run repository scripts from the repository root so relative data paths remain consistent, for example:

```bash
python Scripts/itsm_global_mcmc.py
python Scripts/itsm_camb_spectra.py
```

For a manuscript entry point in `Manuscript/`:

```bash
latexmk -pdf Manuscript/<main-file>.tex
```

## Files

- `.devcontainer/devcontainer.json` — Codespaces/Dev Container configuration.
- `.devcontainer/Dockerfile` — Linux system dependencies, Fortran toolchain, and TeX/REVTeX tooling.
- `.devcontainer/requirements-cloud.txt` — portable Python dependency specification.
- `.devcontainer/post-create.sh` — Python installation, editable CAMB build, Jupyter kernel registration, and environment smoke test.
