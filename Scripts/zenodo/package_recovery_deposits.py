#!/usr/bin/env python3
"""Build Zenodo-ready zip deposits for recovery-era ITSM gates.

Skips arXiv/P2 endorsement path. Produces independent software/data archives:

  1. CBR-001 rectangular T3 Casimir + free-field backreaction
  2. UVIR-003 post-alpha.9 four-leg / deformation / observable-norm slice
  3. Recovery claim-hygiene docs (master plan, selective publishing, P1 note)

Output directory: releases/zenodo/<timestamp or tag>/
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def add_path(
    zf: zipfile.ZipFile,
    src: Path,
    arcname: str,
    skip_parts: set[str] | None = None,
) -> list[str]:
    skip_parts = skip_parts or {"__pycache__", ".git"}
    added: list[str] = []
    if not src.exists():
        return added
    if src.is_file():
        zf.write(src, arcname)
        added.append(arcname)
        return added
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        rel = path.relative_to(src)
        name = f"{arcname}/{rel.as_posix()}"
        zf.write(path, name)
        added.append(name)
    return added


def write_deposit_readme(path: Path, title: str, body: str) -> None:
    path.write_text(body.strip() + "\n", encoding="utf-8")


def package_cbr001(out_dir: Path, git_sha: str) -> Path:
    zip_path = out_dir / "ITSM_CBR-001_Casimir_T3_v1.0.0.zip"
    readme = out_dir / "CBR-001_DEPOSIT_README.md"
    write_deposit_readme(
        readme,
        "CBR-001",
        f"""
# ITSM CBR-001 — Rectangular T^3 Casimir and free-field backreaction

**Version:** 1.0.0  
**Date:** {date.today().isoformat()}  
**Git:** `{git_sha}` on `recovery/v12-core-architecture`  
**License:** CC-BY-4.0 (data/docs); code under repository LICENSE  
**Related paper dir (draft):** `papers/P2-Rectangular-T3-Casimir/`  
**Canonical paper PDF name:** `Boyd_P2_Anisotropic_Casimir_Rectangular_T3.pdf`

## Claim boundary

Validated: lattice Casimir energy density and directional pressures; biaxial
shape scan; free-field biaxial backreaction; Stage-3B search finds **no**
free-field Ht/Hp=13/12 attractor (transient only).

**Not claimed:** parameter-free H0=72.97, geometric a0, completed
cosmology, or driven anisotropy (CBR-002 open).

## Reproduce

```powershell
conda activate itsm_env
cd Analysis/Casimir/CBR-001
python casimir_t3_lattice.py
python cbr001_stage2_standalone.py
python cbr001_stage3_backreaction.py
python cbr001_stage3b_ratio_test.py
```

## Repository

https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model
""",
    )
    files_added: list[str] = []
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        files_added += add_path(
            zf, REPO / "Analysis" / "Casimir" / "CBR-001", "CBR-001"
        )
        files_added += add_path(
            zf,
            REPO / "papers" / "P2-Rectangular-T3-Casimir" / "CBR001_CHECKSUMS.md",
            "CBR001_CHECKSUMS.md",
        )
        files_added += add_path(zf, readme, "DEPOSIT_README.md")
        # Do not include P2 manuscript (endorsement/arXiv deferred)
    manifest = {
        "deposit": "CBR-001",
        "version": "1.0.0",
        "git_sha": git_sha,
        "file_count": len(files_added),
        "sha256_zip": sha256_file(zip_path),
        "files": files_added,
    }
    (out_dir / "CBR-001_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return zip_path


def package_uvir003(out_dir: Path, git_sha: str) -> Path:
    zip_path = out_dir / "ITSM_UVIR-003_LocalFourLeg_v0.10.0-pre.zip"
    readme = out_dir / "UVIR-003_DEPOSIT_README.md"
    write_deposit_readme(
        readme,
        "UVIR-003",
        f"""
# ITSM UVIR-003 — local four-leg kernel slice (post alpha.9)

**Version:** 0.10.0-pre (working gate slice, not MAT-001 unlock)  
**Date:** {date.today().isoformat()}  
**Git:** `{git_sha}` on `recovery/v12-core-architecture`  

## Included subgates

- `PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL` (alpha.9 freeze)
- `PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT` (+ optional dense_edge tag)
- `PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION` (packet proxy, **not** S-matrix)

## Claim boundary

Local frozen-time analytic kernel + deformation + packet-average proxy only.
**Not established:** cosmological S-matrix, unitarity bound, strong-coupling
scale, physical cutoff, MAT-001.

## Reproduce

```powershell
conda activate itsm_env
cd Analysis/UVIR/UVIR-003
python uvir003_local_four_leg_kernel.py
python uvir003_four_leg_kinematic_deformation.py
python uvir003_local_adiabatic_observable_norm.py
```

## Repository

https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model
""",
    )
    include_files = [
        REPO / "Analysis" / "UVIR" / "UVIR-003" / "uvir003_local_four_leg_kernel.py",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "uvir003_four_leg_kinematic_deformation.py",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "uvir003_local_adiabatic_observable_norm.py",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_local_four_leg_kernel_summary.json",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_local_four_leg_kernel.csv",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_four_leg_kinematic_deformation_summary.json",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_four_leg_kinematic_deformation.csv",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_four_leg_kinematic_deformation_dense_edge_summary.json",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_four_leg_kinematic_deformation_dense_edge.csv",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_local_adiabatic_observable_norm_summary.json",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_local_adiabatic_observable_norm.csv",
        # dependencies commonly imported by four-leg stack
        REPO / "Analysis" / "UVIR" / "UVIR-003" / "uvir003_controlled_exchange_domain.py",
        REPO / "Analysis" / "UVIR" / "UVIR-003" / "uvir003_mode_projected_cubic_pair_source.py",
        REPO / "Analysis" / "UVIR" / "UVIR-003" / "uvir003_physical_quadratic_propagators.py",
        REPO / "Analysis" / "UVIR" / "UVIR-003" / "uvir003_scalar_adm_finite_q.py",
        REPO / "Analysis" / "UVIR" / "UVIR-003" / "uvir003_reduced_quartic_momentum_kernel.py",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_cubic_momentum_kernel_summary.json",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_reduced_quartic_momentum_kernel_summary.json",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_controlled_exchange_domain_summary.json",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_frw_background_summary.json",
        REPO
        / "Analysis"
        / "UVIR"
        / "UVIR-003"
        / "outputs"
        / "uvir003_frw_background_trajectory.csv",
        REPO
        / "Theory"
        / "Gates"
        / "UVIR-003"
        / "UVIR-003_STAGE_B_LOCAL_FOUR_LEG_KERNEL.md",
        REPO
        / "Theory"
        / "Gates"
        / "UVIR-003"
        / "UVIR-003_STAGE_B_FOUR_LEG_KINEMATIC_DEFORMATION.md",
        REPO
        / "Theory"
        / "Gates"
        / "UVIR-003"
        / "UVIR-003_STAGE_B_LOCAL_ADIABATIC_OBSERVABLE_NORM.md",
    ]
    files_added: list[str] = []
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for src in include_files:
            if not src.exists():
                continue
            if "outputs" in src.parts:
                arc = f"UVIR-003/outputs/{src.name}"
            elif "Gates" in src.parts:
                arc = f"gate_notes/{src.name}"
            else:
                arc = f"UVIR-003/{src.name}"
            zf.write(src, arc)
            files_added.append(arc)
        files_added += add_path(zf, readme, "DEPOSIT_README.md")
    manifest = {
        "deposit": "UVIR-003-local-four-leg-slice",
        "version": "0.10.0-pre",
        "git_sha": git_sha,
        "file_count": len(files_added),
        "sha256_zip": sha256_file(zip_path),
        "files": files_added,
    }
    (out_dir / "UVIR-003_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return zip_path


def package_recovery_docs(out_dir: Path, git_sha: str) -> Path:
    zip_path = out_dir / "ITSM_Recovery_ClaimHygiene_v1.3.0.zip"
    readme = out_dir / "RECOVERY_DOCS_DEPOSIT_README.md"
    write_deposit_readme(
        readme,
        "Recovery docs",
        f"""
# ITSM recovery-era claim hygiene archive

**Version:** 1.3.0  
**Date:** {date.today().isoformat()}  
**Git:** `{git_sha}` on `recovery/v12-core-architecture`  

## Contents

- Master research plan (identity, three-bucket disposition, open-options rule)
- Selective publishing firewall (paper packaging bans B1-B16)
- P1 **scale-matching reconstruction** note under
  `P1-Scale-Matching-Reconstruction/` (no-gos + C_obs invariant;
  PDF: `Boyd_P1_Present-Epoch_Scale_Matching_Cobs_Hygiene.pdf`)
- Recovery branch README pointer

## Claim boundary

Documentation and claim hygiene only. Does **not** restore withdrawn geometric
a0 or free-field 13/12 attractor predictions. P2 arXiv deferred pending
endorsement; CBR-001 science is archived separately.

## Repository

https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model
""",
    )
    include = [
        REPO / "Theory" / "Core" / "ITSM_Master_Research_Plan.md",
        REPO / "Theory" / "Core" / "ITSM_Core_Recovery_Plan.md",
        REPO / "Theory" / "Core" / "ITSM_Core_Architecture.md",
        REPO / "RECOVERY_BRANCH_README.md",
        REPO
        / "papers"
        / "Selective-Publishing-Plan"
        / "ITSM_Selective_Publishing_Plan.md",
        REPO / "papers" / "P1-Scale-Matching-Reconstruction" / "main.tex",
        REPO / "papers" / "P1-Scale-Matching-Reconstruction" / "main.pdf",
        REPO
        / "papers"
        / "P1-Scale-Matching-Reconstruction"
        / "Boyd_P1_Present-Epoch_Scale_Matching_Cobs_Hygiene.pdf",
        REPO / "papers" / "P1-Scale-Matching-Reconstruction" / "README.md",
        REPO / "papers" / "P1-Scale-Matching-Reconstruction" / "references.bib",
        REPO / "papers" / "P1-Scale-Matching-Reconstruction" / "CoverLetter.txt",
    ]
    files_added: list[str] = []
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for src in include:
            if not src.exists():
                continue
            if "P1-Scale-Matching-Reconstruction" in src.parts:
                arc = f"P1-Scale-Matching-Reconstruction/{src.name}"
            elif "Selective-Publishing-Plan" in src.parts:
                arc = f"Selective-Publishing-Plan/{src.name}"
            elif "Theory" in src.parts:
                arc = f"Theory/Core/{src.name}"
            else:
                arc = src.name
            zf.write(src, arc)
            files_added.append(arc)
        files_added += add_path(zf, readme, "DEPOSIT_README.md")
    manifest = {
        "deposit": "recovery-claim-hygiene",
        "version": "1.3.0",
        "git_sha": git_sha,
        "file_count": len(files_added),
        "sha256_zip": sha256_file(zip_path),
        "files": files_added,
    }
    (out_dir / "RECOVERY_DOCS_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default releases/zenodo/YYYY-MM-DD)",
    )
    parser.add_argument("--git-sha", type=str, default="unknown")
    args = parser.parse_args()
    out_dir = args.out_dir or (
        REPO / "releases" / "zenodo" / date.today().isoformat()
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    zips = [
        package_cbr001(out_dir, args.git_sha),
        package_uvir003(out_dir, args.git_sha),
        package_recovery_docs(out_dir, args.git_sha),
    ]
    index = {
        "date": date.today().isoformat(),
        "git_sha": args.git_sha,
        "branch": "recovery/v12-core-architecture",
        "deposits": [
            {
                "path": z.name,
                "sha256": sha256_file(z),
                "size_bytes": z.stat().st_size,
            }
            for z in zips
        ],
        "notes": (
            "P2 arXiv skipped (endorsement pending). "
            "These Zenodo packages archive validated gate outputs and claim hygiene."
        ),
    }
    (out_dir / "INDEX.json").write_text(
        json.dumps(index, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Output: {out_dir}")
    for z in zips:
        print(f"  {z.name}  {z.stat().st_size/1024:.1f} KB  sha256={sha256_file(z)[:16]}...")


if __name__ == "__main__":
    main()
