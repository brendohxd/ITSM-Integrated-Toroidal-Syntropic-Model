#!/usr/bin/env python3
"""Upload recovery-era packages to Zenodo as *new* depositions.

Does NOT version the legacy v11 Cosmology deposition (20774996 / 18808348).
Creates independent software/dataset records for gate packages.

Environment:
  ZENODO_TOKEN   personal access token with deposit:write (and deposit:actions to publish)

Usage:
  conda activate itsm_env
  $env:ZENODO_TOKEN = '...'   # do not commit
  python Scripts/zenodo/package_recovery_deposits.py --git-sha $(git rev-parse --short HEAD)
  python Scripts/zenodo/upload_recovery_deposits.py --package-dir releases/zenodo/YYYY-MM-DD
  python Scripts/zenodo/upload_recovery_deposits.py --package-dir ... --publish
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import requests

API = "https://zenodo.org/api"
SANDBOX_API = "https://sandbox.zenodo.org/api"

CREATOR = {
    "name": "Boyd, Brendon",
    "affiliation": "Independent Researcher, Burswood, Western Australia",
    "orcid": "0009-0007-4177-2612",
}

DEPOSITS = {
    "cbr001": {
        "zip_glob": "ITSM_CBR-001_Casimir_T3_*.zip",
        "metadata": {
            "title": (
                "ITSM CBR-001: Rectangular T3 Casimir stress and free-field "
                "biaxial backreaction (validated gate package)"
            ),
            "upload_type": "software",
            "description": """
<p>Validated computational package for ITSM gate <strong>CBR-001</strong> on the
<code>recovery/v12-core-architecture</code> branch.</p>
<p><strong>Contents:</strong> rectangular flat <em>T</em><sup>3</sup> lattice
Casimir solver; Stage-2 biaxial shape scan; Stage-3A/3B free-field backreaction
and <em>H<sub>t</sub>/H<sub>p</sub>=13/12</em> reachability search.</p>
<p><strong>Result boundary:</strong> anisotropic free-field Casimir stress is
validated; free-field backreaction produces only <em>transient</em> passages near
13/12 — no quasi-plateau or attractor. This deposit does <strong>not</strong>
claim a parameter-free Hubble solution, geometric derivation of the galactic
acceleration scale, or a completed cubic cosmology.</p>
<p><strong>Reproduce:</strong> conda env <code>itsm_env</code>; see
<code>DEPOSIT_README.md</code> in the archive.</p>
<p><strong>Code:</strong>
<a href="https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model">
GitHub repository</a>. Contact: brendon.boyd@itsm-cosmology.org</p>
""".strip(),
            "creators": [CREATOR],
            "keywords": [
                "Casimir effect",
                "cosmic topology",
                "T3",
                "Bianchi cosmology",
                "ITSM",
                "open science",
            ],
            "license": "cc-by-4.0",
            "version": "1.0.0",
            "related_identifiers": [
                {
                    "identifier": (
                        "https://github.com/brendohxd/"
                        "ITSM-Integrated-Toroidal-Syntropic-Model"
                    ),
                    "relation": "isSupplementTo",
                    "resource_type": "software",
                    "scheme": "url",
                }
            ],
        },
    },
    "uvir003": {
        "zip_glob": "ITSM_UVIR-003_LocalFourLeg_*.zip",
        "metadata": {
            "title": (
                "ITSM UVIR-003: local four-leg kernel, kinematic deformation, "
                "and adiabatic packet proxy (post-alpha.9 slice)"
            ),
            "upload_type": "software",
            "description": """
<p>Working gate slice of ITSM <strong>UVIR-003</strong> on
<code>recovery/v12-core-architecture</code> (post manuscript freeze
12.0-alpha.9).</p>
<p><strong>Included subgates:</strong></p>
<ul>
<li><code>PASS_LOCAL_EXCHANGE_PLUS_REDUCED_CONTACT_FOUR_LEG_KERNEL</code></li>
<li><code>PASS_FOUR_LEG_KINEMATIC_DEFORMATION_AUDIT</code> (+ dense-edge tag)</li>
<li><code>PASS_LOCAL_ADIABATIC_OBSERVABLE_NORMALIZATION</code>
(Gaussian packet proxy of local kernel — <strong>not</strong> an S-matrix)</li>
</ul>
<p><strong>Not established:</strong> cosmological S-matrix, unitarity bound,
strong-coupling scale, physical cutoff, or MAT-001 unlock.</p>
<p><strong>Code:</strong>
<a href="https://github.com/brendohxd/ITSM-Integrated-Toroidal-Syntropic-Model">
GitHub</a>. Contact: brendon.boyd@itsm-cosmology.org</p>
""".strip(),
            "creators": [CREATOR],
            "keywords": [
                "effective field theory",
                "cosmological perturbations",
                "ITSM",
                "UVIR-003",
                "open science",
            ],
            "license": "cc-by-4.0",
            "version": "0.10.0-pre",
            "related_identifiers": [
                {
                    "identifier": (
                        "https://github.com/brendohxd/"
                        "ITSM-Integrated-Toroidal-Syntropic-Model"
                    ),
                    "relation": "isSupplementTo",
                    "resource_type": "software",
                    "scheme": "url",
                }
            ],
        },
    },
    "recovery_docs": {
        "zip_glob": "ITSM_Recovery_ClaimHygiene_*.zip",
        "metadata": {
            "title": (
                "ITSM recovery-era claim hygiene archive "
                "(master plan, publishing firewall, "
                "P1 scale-matching reconstruction note)"
            ),
            "upload_type": "other",
            "description": """
<p>Documentation archive for the ITSM <strong>recovery</strong> programme
(<code>recovery/v12-core-architecture</code>).</p>
<ul>
<li>Master research plan (ideal identity, three-bucket claim disposition,
open-options rule)</li>
<li>Selective publishing firewall (abstract packaging bans)</li>
<li>P1 scale-matching reconstruction note
(<code>P1-Scale-Matching-Reconstruction</code>; no-gos +
<em>C</em><sub>obs</sub> invariant;
PDF <code>Boyd_P1_Present-Epoch_Scale_Matching_Cobs_Hygiene.pdf</code>)</li>
</ul>
<p>This deposit archives <strong>claim hygiene and workflow authority</strong>.
It does not reintroduce withdrawn geometric <em>a</em><sub>0</sub> or free-field
13/12 attractor packaging as live predictions. P2 arXiv is deferred pending
endorsement; CBR-001 numerical science is deposited separately.</p>
<p>Contact: brendon.boyd@itsm-cosmology.org</p>
""".strip(),
            "creators": [CREATOR],
            "keywords": [
                "ITSM",
                "research data management",
                "claim hygiene",
                "open science",
            ],
            "license": "cc-by-4.0",
            "version": "1.3.0",
            "related_identifiers": [
                {
                    "identifier": (
                        "https://github.com/brendohxd/"
                        "ITSM-Integrated-Toroidal-Syntropic-Model"
                    ),
                    "relation": "isSupplementTo",
                    "resource_type": "software",
                    "scheme": "url",
                }
            ],
        },
    },
}


def require_token() -> str:
    token = os.environ.get("ZENODO_TOKEN") or os.environ.get("ZENODO_ACCESS_TOKEN")
    if not token:
        print(
            "[!] ZENODO_TOKEN not set.\n"
            "    Create a token at https://zenodo.org/account/settings/applications/\n"
            "    with deposit:write (and deposit:actions to publish), then:\n"
            "      $env:ZENODO_TOKEN = 'your_token'\n"
            "    Re-run this script.",
            file=sys.stderr,
        )
        sys.exit(2)
    return token


def find_zip(package_dir: Path, pattern: str) -> Path:
    matches = sorted(package_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No zip matching {pattern} in {package_dir}")
    return matches[-1]


def create_deposition(api: str, token: str, metadata: dict) -> dict:
    r = requests.post(
        f"{api}/deposit/depositions",
        params={"access_token": token},
        json={"metadata": metadata},
        headers={"Content-Type": "application/json"},
        timeout=120,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"create deposition failed: {r.status_code} {r.text}")
    return r.json()


def upload_file(bucket: str, token: str, path: Path) -> None:
    with path.open("rb") as handle:
        r = requests.put(
            f"{bucket}/{path.name}",
            params={"access_token": token},
            data=handle,
            timeout=600,
        )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"upload {path.name} failed: {r.status_code} {r.text}")


def publish_deposition(api: str, token: str, dep_id: int) -> dict:
    r = requests.post(
        f"{api}/deposit/depositions/{dep_id}/actions/publish",
        params={"access_token": token},
        timeout=120,
    )
    if r.status_code not in (200, 201, 202):
        raise RuntimeError(f"publish failed: {r.status_code} {r.text}")
    return r.json()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--package-dir",
        type=Path,
        required=True,
        help="Directory from package_recovery_deposits.py",
    )
    parser.add_argument(
        "--which",
        nargs="+",
        choices=list(DEPOSITS.keys()) + ["all"],
        default=["all"],
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish immediately (default: leave as editable draft)",
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use sandbox.zenodo.org (needs sandbox token)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions only",
    )
    args = parser.parse_args()
    package_dir = args.package_dir.resolve()
    api = SANDBOX_API if args.sandbox else API
    keys = list(DEPOSITS.keys()) if "all" in args.which else args.which

    if args.dry_run:
        for key in keys:
            spec = DEPOSITS[key]
            z = find_zip(package_dir, spec["zip_glob"])
            print(f"[dry-run] {key}: would upload {z.name} ({z.stat().st_size} bytes)")
            print(f"          title: {spec['metadata']['title'][:70]}...")
        return

    token = require_token()
    results = []
    for key in keys:
        spec = DEPOSITS[key]
        zip_path = find_zip(package_dir, spec["zip_glob"])
        print(f"[*] Creating deposition for {key}...")
        dep = create_deposition(api, token, spec["metadata"])
        dep_id = dep["id"]
        bucket = dep["links"]["bucket"]
        print(f"    id={dep_id}  draft={dep['links'].get('html', dep['links'].get('latest_draft'))}")
        print(f"[*] Uploading {zip_path.name}...")
        upload_file(bucket, token, zip_path)
        # also upload INDEX/manifest if present
        for extra_name in (
            "INDEX.json",
            f"{key.upper()}_manifest.json" if key != "recovery_docs" else "RECOVERY_DOCS_manifest.json",
        ):
            # map keys to manifest names
            pass
        manifest_map = {
            "cbr001": "CBR-001_manifest.json",
            "uvir003": "UVIR-003_manifest.json",
            "recovery_docs": "RECOVERY_DOCS_manifest.json",
        }
        man = package_dir / manifest_map[key]
        if man.exists():
            print(f"[*] Uploading {man.name}...")
            upload_file(bucket, token, man)
        record = dep
        if args.publish:
            print(f"[*] Publishing {dep_id}...")
            record = publish_deposition(api, token, dep_id)
            doi = record.get("doi") or record.get("metadata", {}).get("prereserve_doi", {}).get("doi")
            print(f"    PUBLISHED doi={doi}")
        else:
            print(f"    DRAFT ready — review/publish: https://zenodo.org/uploads/{dep_id}")
            doi = dep.get("metadata", {}).get("prereserve_doi", {}).get("doi")
        results.append(
            {
                "key": key,
                "deposition_id": dep_id,
                "doi": doi,
                "published": bool(args.publish),
                "zip": zip_path.name,
                "html": f"https://zenodo.org/uploads/{dep_id}",
            }
        )

    out = package_dir / "ZENODO_UPLOAD_RESULTS.json"
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"\n[+] Wrote {out}")
    for row in results:
        print(f"  {row['key']}: {row['html']}  doi={row.get('doi')}")


if __name__ == "__main__":
    main()
