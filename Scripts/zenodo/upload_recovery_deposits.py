#!/usr/bin/env python3
"""Upload recovery-era packages to Zenodo as *new* depositions.

Does NOT version the legacy v11 Cosmology deposition (20774996 / 18808348).
Creates independent software/dataset records for gate packages.

Metadata (inclusive descriptions, ORCID, website, GitHub) lives in
zenodo_deposit_metadata.py. To refresh existing drafts without re-uploading
files, use update_zenodo_draft_metadata.py.

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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zenodo_deposit_metadata import DEPOSITS  # noqa: E402

API = "https://zenodo.org/api"
SANDBOX_API = "https://sandbox.zenodo.org/api"


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
            creators = spec["metadata"].get("creators") or []
            if creators:
                print(f"          orcid: {creators[0].get('orcid')}")
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
        print(
            f"    id={dep_id}  draft={dep['links'].get('html', dep['links'].get('latest_draft'))}"
        )
        print(f"[*] Uploading {zip_path.name}...")
        upload_file(bucket, token, zip_path)
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
            doi = record.get("doi") or record.get("metadata", {}).get(
                "prereserve_doi", {}
            ).get("doi")
            print(f"    PUBLISHED doi={doi}")
        else:
            print(
                f"    DRAFT ready — review/publish: https://zenodo.org/uploads/{dep_id}"
            )
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
