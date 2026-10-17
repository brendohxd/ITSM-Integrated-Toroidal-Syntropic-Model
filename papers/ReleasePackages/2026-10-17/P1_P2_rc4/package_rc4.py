"""Prepare/seal local rc4 review artifacts; never upload or alter rc3 evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PAPERS = {
    "P1": ("P1-Scale-Matching-Reconstruction", "Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc4", ["itsm_t3_fundamental_domain.pdf"]),
    "P2": ("P2-Rectangular-T3-Casimir", "Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control_v0.2.0-rc4", ["itsm_t3_rectangular_domain.pdf", "cbr001_stage2_anisotropy.png", "cbr001_stage3b_ratio.png", "cbr001_stage3b_threshold_epsilon.png"]),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, payload):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")


def sidecar(path):
    target = path.with_name(path.name + ".sha256")
    with target.open("x", encoding="ascii", newline="\n") as stream:
        stream.write(f"{sha(path)}  {path.name}\n")


def pdf_text(path):
    reader = PdfReader(path)
    return reader, re.sub(r"\s+", " ", " ".join(page.extract_text() for page in reader.pages))


def prepare():
    for paper, (directory, stem, figures) in PAPERS.items():
        source = ROOT / "papers" / directory
        build = ROOT / ".local/p1-p2-rc4/final" / paper
        destination = HERE / "portable" / paper
        destination.mkdir(parents=True, exist_ok=False)
        (destination / "figures").mkdir()
        original = (source / "main.tex").read_text(encoding="utf-8")
        normalized, count = re.subn(r"\\graphicspath\{[^\n]*\}",
                                    lambda _: r"\graphicspath{{figures/}}", original)
        assert count == 1
        with (destination / "main.tex").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(normalized)
        for filename in ("references.bib", "VERSION"):
            shutil.copy2(source / filename, destination / filename)
        shutil.copy2(build / "main.bbl", destination / "main.bbl")
        for figure in figures:
            shutil.copy2(source / "figures" / figure, destination / "figures" / figure)
        if paper == "P2":
            shutil.copy2(source / "CBR001_CHECKSUMS.md", destination / "CBR001_CHECKSUMS.md")
        with (destination / "REVIEW_STATUS.txt").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write("Local review draft v0.2.0-rc4, 17 October 2026. Not submitted.\n"
                         "Author final verification and applicable independent review remain pending.\n"
                         "Build main.tex with RevTeX 4.2 and BibTeX, or Tectonic (untrusted mode).\n"
                         "Only graphicspath differs from the canonical TeX source. Figures are unchanged.\n"
                         "For P2, the historic CBR001_CHECKSUMS ledger is unmodified; its old manuscript\n"
                         "anchors are historical, not the rc4 manuscript identity. Sensitivity: FAIL 18/19.\n")
        published_path = source / (stem + ".pdf")
        if published_path.exists():
            raise FileExistsError(published_path)
        shutil.copy2(build / "main.pdf", published_path)
        sidecar(published_path)
        print(f"PREPARED {paper}: {published_path.name}")


def seal(receipt):
    validation = json.loads(receipt.read_text(encoding="utf-8"))
    assert validation["validation_pass"]
    assert validation["physics_pass"] is False
    result = {"version": "0.2.0-rc4", "local_build_verified": True,
              "physics_pass": False, "publication_ready": False,
              "author_final_read": "PENDING", "independent_review": "PENDING",
              "validation_receipt_sha256": sha(receipt), "papers": {}}
    for paper, (directory, stem, _) in PAPERS.items():
        source = ROOT / "papers" / directory
        canonical = source / (stem + ".pdf")
        portable = ROOT / ".local/p1-p2-rc4/portable_check" / paper / "main.pdf"
        reader, canonical_text = pdf_text(canonical)
        portable_reader, portable_text = pdf_text(portable)
        assert canonical_text == portable_text, paper + ": portable text mismatch"
        assert len(reader.pages) == len(portable_reader.pages) == 6
        assert "0.2.0-rc4" in canonical_text
        assert "??" not in canonical_text
        source_rel = str((source / "main.tex").relative_to(ROOT))
        assert validation["current_source_sha256"][source_rel] == sha(source / "main.tex")
        build_checks = {}
        for kind in ("final", "portable_check"):
            log = ROOT / ".local/p1-p2-rc4" / kind / paper / "main.log"
            log_text = log.read_text(encoding="utf-8", errors="replace")
            for pattern in ("undefined", "Overfull", "Missing character", "! LaTeX Error"):
                assert pattern not in log_text, (paper, kind, pattern)
            build_checks[kind] = {"log_sha256": sha(log),
                                  "underfull_warnings": log_text.count("Underfull"),
                                  "float_warnings": [line for line in log_text.splitlines()
                                                     if "float" in line.lower() and "warn" in line.lower()]}
        destination = HERE / "portable" / paper
        archive = HERE / f"ITSM_{paper}_source_v0.2.0-rc4_2026-10-17.zip"
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(destination.rglob("*")):
                if path.is_file():
                    info = zipfile.ZipInfo(path.relative_to(destination).as_posix(),
                                           date_time=(2026, 10, 17, 0, 0, 0))
                    info.compress_type = zipfile.ZIP_DEFLATED
                    bundle.writestr(info, path.read_bytes())
        with zipfile.ZipFile(archive) as bundle:
            assert bundle.testzip() is None
            assert bundle.read("main.tex") == (destination / "main.tex").read_bytes()
        sidecar(archive)
        result["papers"][paper] = {
            "canonical_source_sha256": sha(source / "main.tex"),
            "pdf": str(canonical.relative_to(ROOT)), "pdf_sha256": sha(canonical),
            "pages_visually_inspected": 6, "portable_text_matches": True,
            "build_checks": build_checks,
            "source_zip": archive.name, "source_zip_sha256": sha(archive),
            "source_members": {str(path.relative_to(destination)): sha(path)
                               for path in sorted(destination.rglob("*")) if path.is_file()},
        }
    write_json(HERE / "P1_P2_RC4_MANIFEST.json", result)
    sidecar(HERE / "P1_P2_RC4_MANIFEST.json")
    print(json.dumps({"local_build_verified": True, "physics_pass": False,
                      "publication_ready": False, "papers": list(PAPERS)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("prepare", "seal"))
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    if args.stage == "prepare":
        prepare()
    else:
        assert args.receipt is not None
        seal(args.receipt.resolve())
