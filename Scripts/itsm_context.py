"""Standalone, local-only ITSM context selection. No model/Relay dependency.

This budgets newly returned evidence; it cannot modify a host's prior context,
reasoning effort, billing, native tool inventory, or automatic compaction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / ".local/itsm-context"
DEFAULT_BUDGET = 6500
CRITICAL = re.compile(r"FAIL|ERROR|Traceback|AssertionError|BLOCKED|HOLD|NOT_DERIVED|NOT_COMPUTED|NOT_COMPLETED", re.I)
SECRET = re.compile(r"(?i)((?:authorization|api[_-]?key|access[_-]?token|refresh[_-]?token|password|client[_-]?secret)\s*[=:]\s*)([^\s,;]+)")
BEARER = re.compile(r"(?i)Bearer\s+[A-Za-z0-9._~+/=-]+")
KEY = re.compile(r"\b(?:sk-|ghp_|github_pat_)[A-Za-z0-9_-]{16,}\b")
JSON_SECRET = re.compile(r'(?i)("(?:authorization|api[_-]?key|access[_-]?token|refresh[_-]?token|password|client[_-]?secret)"\s*:\s*)"(?:\\.|[^"\\])*"')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def redact(text: str) -> str:
    text = JSON_SECRET.sub(r'\1"[redacted]"', text)
    return KEY.sub("[redacted]", BEARER.sub("Bearer [redacted]", SECRET.sub(r"\1[redacted]", text)))


def local_file(name: str, root: Path = ROOT) -> Path:
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Read target must stay within the ITSM workspace, including resolved links")
    if path.name.lower() in {".env", "memory.db", "credentials.json", "auth.json", "zenodo_secrets.json"} or path.suffix.lower() in {".pem", ".key", ".sqlite", ".db"}:
        raise ValueError("Secret/vault files are outside the context optimizer's read scope")
    return path


def excerpt(text: str, start: int, count: int, column: int, budget: int) -> dict:
    """Explicit contiguous pagination; no hidden head/tail omission in reads."""
    lines = text.splitlines()
    if start < 1 or count < 1 or column < 0 or budget < 256:
        raise ValueError("Require start>=1, lines>=1, column>=0 and max-chars>=256")
    if start > len(lines)+1:
        raise ValueError("Start is beyond EOF")
    if start <= len(lines) and column > len(lines[start-1]):
        raise ValueError("Column is beyond the requested line")
    output, used = [], 0
    next_line, next_column = start, column
    for number in range(start, min(len(lines)+1, start+count)):
        offset = column if number == start else 0
        prefix = f"{number}:{offset} "
        room = budget-used-len(prefix)-1
        if room <= 0:
            break
        remainder = lines[number-1][offset:]
        piece = remainder[:room]
        output.append(prefix+piece)
        used += len(prefix)+len(piece)+1
        if len(piece) < len(remainder):
            next_line, next_column = number, offset+len(piece)
            break
        next_line, next_column = number+1, 0
    return {"text":"\n".join(output), "total_lines":len(lines),
            "start_line":start, "start_column":column,
            "next_line":next_line, "next_column":next_column,
            "eof":next_line>len(lines)}


def bounded_view(text: str, budget: int) -> dict:
    """A display view only; full sanitized output always remains available."""
    if len(text) <= budget:
        return {"text":text,"omitted":False,"critical_lines_omitted":0}
    lines = text.splitlines()
    critical = [i for i,line in enumerate(lines) if CRITICAL.search(line)]
    # Failure/hold evidence gets space before routine head/tail output.
    preferred = list(dict.fromkeys(critical + list(range(min(6,len(lines)))) + list(range(max(0,len(lines)-6),len(lines)))))
    chosen, used = {}, 0
    complete = set()
    for i in preferred:
        remaining = budget-used-24
        if remaining < 40:
            break
        piece = lines[i][:min(1000,remaining)]
        if len(piece) == len(lines[i]):
            complete.add(i)
        else:
            piece += " [LINE CLIPPED]"
        chosen[i] = f"{i+1}: {piece}"
        used += len(chosen[i])+1
    return {"text":"\n".join(chosen[i] for i in sorted(chosen)),"omitted":True,
            "critical_lines_omitted":sum(i not in complete for i in critical),
            "warning":"Selected view only. Read the full local artifact before claiming all failures or evidence were inspected."}


def persist(text: str, logs: Path = LOGS) -> tuple[Path,str]:
    logs.mkdir(parents=True,exist_ok=True)
    path = logs / f"output-{uuid.uuid4().hex}.txt"
    data = text.encode("utf-8")
    path.write_bytes(data)
    digest = sha(data)
    path.with_suffix(".txt.sha256").write_text(f"{digest}  {path.name}\n",encoding="ascii")
    return path,digest


def receipt_summary(payload: dict) -> dict:
    rows = payload.get("checks")
    valid = isinstance(rows,list) and all(isinstance(row,dict) for row in rows)
    checks = rows if valid else []
    failed = [row for row in checks if row.get("passed") is False]
    unknown = [row for row in checks if not isinstance(row.get("passed"),bool)]
    # Preserve every non-check top-level field. No gate/status inference.
    return {"declared_fields":{key:value for key,value in payload.items() if key!="checks"},
            "check_summary":{"schema_recognized":valid,"total":len(checks) if valid else None,
                             "passed":sum(row.get("passed") is True for row in checks),
                             "failed":len(failed),"unknown":len(unknown)},
            "failed_checks":failed,"unknown_checks":unknown,
            "interpretation":"A passed check is not a physics pass. Source dependency hashes are not verified by this summary."}


def emit(payload: dict) -> None:
    print(json.dumps(payload,ensure_ascii=False,indent=2))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-chars",type=int,default=DEFAULT_BUDGET,help="display body budget; metadata adds overhead")
    sub = parser.add_subparsers(dest="mode",required=True)
    sub.add_parser("status")
    read = sub.add_parser("read")
    read.add_argument("path")
    read.add_argument("--start",type=int,default=1)
    read.add_argument("--lines",type=int,default=80)
    read.add_argument("--column",type=int,default=0)
    receipt = sub.add_parser("receipt")
    receipt.add_argument("path")
    run = sub.add_parser("run")
    run.add_argument("command",nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if not 256 <= args.max_chars <= 100000:
        raise ValueError("Display budget must be between 256 and 100000 characters")
    if not LOGS.resolve().is_relative_to(ROOT):
        raise ValueError("Output directory resolves outside the workspace")
    if args.mode == "status":
        emit({"optimizer":"itsm-context-v1","standalone":True,"relay_dependency":False,
              "network_calls":False,"root":str(ROOT),"private_logs":str(LOGS),
              "display_body_budget":args.max_chars,"prior_context_control":False,
              "provider_billing_measurement":False,"script_sha256":sha(Path(__file__).read_bytes())})
        return 0
    if args.mode in {"read","receipt"}:
        path = local_file(args.path)
        data = path.read_bytes()
        original = data.decode("utf-8-sig")
        safe = redact(original)
        base = {"path":str(path.relative_to(ROOT)),"source_sha256":sha(data),
                "source_bytes":len(data),"redacted":safe!=original}
        if args.mode == "read":
            emit({**base,**excerpt(safe,args.start,args.lines,args.column,args.max_chars)})
            return 0
        sidecar = path.with_suffix(path.suffix+".sha256")
        expected = sidecar.read_text(encoding="ascii").split()[0] if sidecar.exists() else None
        base["sidecar_matches"] = sha(data)==expected if expected else None
        if expected and not base["sidecar_matches"]:
            emit({**base,"error":"Receipt hash mismatch; no summary admitted"})
            return 2
        payload = json.loads(original)
        if not isinstance(payload,dict):
            raise ValueError("Receipt root must be an object")
        structured = receipt_summary(payload)
        summary = redact(json.dumps(structured,ensure_ascii=False,indent=2))
        artifact,digest = persist(summary)
        view = bounded_view(summary,args.max_chars)
        # Keep canonical hold flags and check counts outside any clipped body.
        flags = {key:payload[key] for key in ("physics_pass","gate_effect","canonical_test_complete","Rule9","status") if key in payload}
        flags = json.loads(redact(json.dumps(flags)))
        emit({**base,"declared_flags":flags,"check_summary":structured["check_summary"],
              "summary_artifact":str(artifact.relative_to(ROOT)),"summary_sha256":digest,
              "display_body_chars":len(view["text"]),**view})
        return 0
    command = args.command[1:] if args.command[:1]==["--"] else args.command
    if not command:
        raise ValueError("run requires an explicit executable and arguments")
    # No shell interpolation, new permissions, provider session, or network
    # operation is introduced by the wrapper. The explicit child has the same
    # authority requirements as if the user/agent ran it directly.
    completed = subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=False)
    original = completed.stdout.decode("utf-8",errors="replace")
    safe = redact(original)
    artifact,digest = persist(safe)
    view = bounded_view(safe,args.max_chars)
    emit({"exit_code":completed.returncode,"output_artifact":str(artifact.relative_to(ROOT)),
          "output_sha256":digest,"original_output_bytes":len(completed.stdout),
          "redacted":safe!=original,"output_encoding":"utf-8 with replacement for invalid bytes",
          "display_body_chars":len(view["text"]),"provider_billing_savings":"NOT_MEASURED",**view})
    return completed.returncode if completed.returncode>=0 else 128-completed.returncode


if __name__ == "__main__":
    # Windows redirected stdout may default to cp1252. Scientific symbols must
    # survive the JSON display path just as they do in UTF-8 source artifacts.
    if hasattr(sys.stdout,"reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8",errors="strict")
    try:
        raise SystemExit(main())
    except (OSError,ValueError) as exc:
        emit({"optimizer_error":redact(str(exc)),"result":"NO_SUCCESS_CLAIM"})
        raise SystemExit(2)
