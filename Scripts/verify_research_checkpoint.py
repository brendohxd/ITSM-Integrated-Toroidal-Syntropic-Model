"""Verify the byte/provenance boundary of the 8 October research checkpoint."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = "Theory/Verification/ITSM_RESEARCH_CHECKPOINT_2026-10-08.manifest.json"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=DEFAULT)
    parser.add_argument("--revision", help="Git revision, or INDEX for staged blobs")
    args = parser.parse_args()
    def read(name):
        path = Path(name)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("Manifest path must stay within the repository")
        if args.revision:
            spec = (":" if args.revision == "INDEX" else args.revision + ":") + name
            result = subprocess.run(["git", "cat-file", "blob", spec], cwd=ROOT,
                                    capture_output=True, check=True)
            return result.stdout
        resolved = (ROOT / path).resolve()
        if not resolved.is_relative_to(ROOT.resolve()):
            raise ValueError("Resolved manifest path escapes the repository")
        return resolved.read_bytes()
    def digest(data):
        return hashlib.sha256(data).hexdigest()
    failures = []
    raw = read(args.manifest)
    manifest = json.loads(raw)
    if manifest.get("schema") != "itsm-research-checkpoint-v1":
        raise ValueError("Unknown checkpoint manifest schema")
    sidecar = read(args.manifest + ".sha256").decode("ascii").split()[0]
    if sidecar != digest(raw):
        failures.append({"path": args.manifest, "reason": "manifest sidecar mismatch"})
    content = {}
    for name, record in manifest["files"].items():
        try:
            data = read(name)
            content[name] = data
            if len(data) != record["bytes"] or digest(data) != record["sha256"]:
                failures.append({"path": name, "reason": "byte/hash mismatch"})
        except (OSError, subprocess.CalledProcessError, ValueError) as error:
            failures.append({"path": name, "reason": type(error).__name__})
    for name, data in content.items():
        if name.endswith(".sha256"):
            target = name[:-7]
            if target in content and data.decode("ascii").split()[0].lower() != digest(content[target]):
                failures.append({"path": name, "reason": "artifact sidecar mismatch"})
    for name, expected in manifest["scientific_source_pins"].items():
        if name not in content or digest(content[name]) != expected:
            failures.append({"path": name, "reason": "scientific source pin mismatch"})
    holds = manifest["scientific_disposition"]
    if holds["physics_pass"] is not False or holds["Rule9_cleared"] is not False or holds["gate_effect"] != "NONE":
        failures.append({"reason": "checkpoint must retain scientific holds"})
    print(json.dumps({
        "validation": "PASS_CHECKPOINT_INTEGRITY_ONLY" if not failures else "FAIL_CHECKPOINT_INTEGRITY",
        "read_surface": args.revision or "WORKTREE",
        "manifest_sha256": digest(raw),
        "files_checked": len(manifest["files"]),
        "scientific_source_pins_checked": len(manifest["scientific_source_pins"]),
        "failures": failures,
        "physics_pass": False,
        "gate_effect": "NONE",
        "interpretation": "Byte/provenance integrity only; no scientific gate or review clearance."
    }, indent=2))
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
