"""Hash and locate acceleration-scale statements in available historical text.

This is a lexical inventory, not an equation parser or derivation validator.
It preserves the old scan and never supplies input to the symbolic audit.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "outputs"
SUFFIXES = {".md", ".tex", ".txt"}
SCOPES = ("Theory/History", "Manuscript", "papers/P1-Scale-Matching-Reconstruction")
LEGACY_CP1252 = {
    "main:Analysis/Experimental/README.md",
    "main:Analysis/Hierarchical_H0/Archive/results_full_rawsample_5hr/hierarchical_summary.txt",
    "main:Analysis/Hierarchical_H0/results_correct/correct_summary.txt",
}
TOKEN = re.compile(r"(?<![A-Za-z])a\s*_\s*\{?\s*0\}?|(?<![A-Za-z])a0(?![A-Za-z])|a₀|\\(?:azero|aZero)\b|(?<![A-Za-z])a\s+0\b")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    sources, hits, errors, binary, decoding_warnings = [], [], [], [], []
    candidates = sorted({p for scope in SCOPES for p in (ROOT/scope).rglob("*") if p.is_file()})
    records = []
    for path in candidates:
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() not in SUFFIXES:
            if path.suffix.lower() in {".pdf", ".docx"}:
                binary.append(rel)
            continue
        try:
            records.append(("worktree:"+rel, path.read_bytes()))
        except OSError as exc:
            errors.append({"path":rel,"error":str(exc)})
    # Inspect the main branch's text sources without checking it out or changing HEAD.
    ref = subprocess.run(["git","rev-parse","main"],cwd=ROOT,capture_output=True,check=True,text=True).stdout.strip()
    tree = subprocess.run(["git","ls-tree","-r","--name-only","main"],cwd=ROOT,capture_output=True,check=True,text=True).stdout.splitlines()
    for rel in sorted(tree):
        if Path(rel).suffix.lower() not in SUFFIXES:
            continue
        result = subprocess.run(["git","show",f"main:{rel}"],cwd=ROOT,capture_output=True)
        if result.returncode:
            errors.append({"path":"main:"+rel,"error":result.stderr.decode("utf-8",errors="replace")})
        else:
            records.append(("main:"+rel,result.stdout))
    for identity, data in records:
        encoding = "utf-8-sig"
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            if identity not in LEGACY_CP1252:
                errors.append({"path":identity,"error":str(exc)})
                continue
            encoding = "cp1252"
            text = data.decode(encoding)
            decoding_warnings.append({"path":identity,"utf8_error":str(exc),"declared_fallback":encoding})
        lines = text.splitlines()
        found = [i for i,line in enumerate(lines) if TOKEN.search(line)]
        source_hash = sha(data)
        sources.append({"source":identity,"sha256":source_hash,"encoding":encoding,"lines":len(lines),"token_hits":len(found)})
        for i in found:
            start,end = max(0,i-6),min(len(lines),i+7)
            hits.append({"source":identity,"source_sha256":source_hash,"line":i+1,
                         "window_start":start+1,"window_end":end,
                         "matched_line":lines[i],"context":"\n".join(lines[start:end])})
    summary = {"scope":list(SCOPES),"main_commit":ref,"main_text_source_count":sum(x["source"].startswith("main:") for x in sources),
               "source_count":len(sources),"unique_byte_contents":len({x["sha256"] for x in sources}),
               "token_hit_count":len(hits),"sources_with_hits":sum(x["token_hits"]>0 for x in sources),
               "read_errors":errors,"decoding_warnings":decoding_warnings,"unread_binary_files":binary,"sources":sources,
               "extractor_sha256":sha(Path(__file__).read_bytes()),
               "coverage":"Declared available-text corpus and main text files only; token windows require equation-level review. Unknown aliases and unavailable original archives are not certified complete.",
               "derived_coefficient":False,"used_for_parameter_selection":False,
               "analyst_blinded":False,"physics_pass":False,"gate_effect":"NONE"}
    OUT.mkdir(exist_ok=True)
    catalogue = OUT/"acceleration_history_inventory.json"
    windows = OUT/"acceleration_history_windows.jsonl"
    catalogue.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    windows.write_text("".join(json.dumps(row,sort_keys=True)+"\n" for row in hits),encoding="utf-8")
    for path in (catalogue,windows,Path(__file__)):
        path.with_suffix(path.suffix+".sha256").write_text(f"{sha(path.read_bytes())}  {path.name}\n",encoding="ascii")
    print(json.dumps({key:summary[key] for key in ("source_count","unique_byte_contents","token_hit_count","sources_with_hits","main_text_source_count","main_commit","read_errors","decoding_warnings")}))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
