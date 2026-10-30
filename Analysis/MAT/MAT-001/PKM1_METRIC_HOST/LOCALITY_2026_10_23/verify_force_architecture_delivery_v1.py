"""Delivery audit V1: byte identity, replay, preservation and goal evidence.

This verifies the bounded comparison deliverables, not physical clearance.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def meta(path):
    p = Path(path)
    s = p.stat()
    return {"sha256":sha(p),"bytes":s.st_size,"mtime_ns":s.st_mtime_ns}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo",type=Path,required=True)
    ap.add_argument("--staging",type=Path,required=True)
    ap.add_argument("--out-dir",type=Path,required=True)
    args = ap.parse_args()
    repo, staging, output = args.repo.resolve(), args.staging.resolve(), args.out_dir.resolve()
    if not output.is_relative_to(BASE) or output==BASE:
        raise ValueError("new audit receipts must stay inside the package")
    output.mkdir(parents=True,exist_ok=False)
    data = json.loads((BASE/"frozen_inputs_v1.json").read_text())
    primary_dir = BASE/"receipts/primary_v2_attempt_01"
    independent_dir = BASE/"receipts/independent_v1_attempt_01"
    primary = json.loads((primary_dir/"summary.json").read_text())
    ind = json.loads((independent_dir/"verification.json").read_text())
    preserved = json.loads((primary_dir/"preservation.json").read_text())["before"]
    checks = []
    def add(name, condition, **detail):
        checks.append({"name":name,"status":"PASS" if bool(condition) else "FAIL","details":detail})
    for name, old in preserved.items():
        add("original bytes/native metadata "+name,meta(repo/name)==old)
    add("all 15 original dirty files covered",
        all(p in preserved for p in data["protected_dirty_files"]))
    report = repo/"Theory/Core/ITSM_FORCE_ARCHITECTURE_COMPARISON_V1_REPORT_2026-10-23.md"
    contract = repo/"Theory/Core/ITSM_FORCE_ARCHITECTURE_COMPARISON_V1_CONTRACT_2026-10-23.md"
    add("owning comparison report byte identity",
        sha(report)=="fef673253469c1b081e38650678260bbcf22f992317de3b8c7c1840d37734e71")
    add("original frozen contract integrated without backdating/rewrite",
        sha(contract)==sha(BASE/contract.name)==data["contract_sha256"])
    chronological = [staging/contract.name,staging/"frozen_inputs_v1.json",
                     staging/"receipts/primary_v1_attempt_01/summary.json",
                     staging/"receipts/primary_v2_attempt_01/summary.json",
                     staging/"receipts/independent_v1_attempt_01/verification.json"]
    stamps = [p.stat().st_mtime_ns for p in chronological]
    add("original staging contract precedes scientific receipts",
        stamps==sorted(stamps),native_integer_mtime_ns=stamps)
    for p in staging.rglob("*"):
        if p.is_file():
            relative = p.relative_to(staging)
            q = BASE/relative
            add("staging source preserved/integrated "+str(relative),q.exists() and sha(p)==sha(q))
    for p in list(BASE.rglob("*.sha256"))+[Path(str(report)+".sha256"),Path(str(contract)+".sha256")]:
        target = p.with_suffix("")
        add("new artifact sidecar "+str(p.relative_to(repo)),
            target.exists() and sha(target)==p.read_text().split()[0].lower())
    v1 = (BASE/"pkm1_p0b_locality_v1.py").read_text()
    v2 = (BASE/"pkm1_p0b_locality_v2.py").read_text()
    expected = v1.replace("diagnostic V1;","diagnostic V2;").replace(
        "sp.diff(y*delta_b, y).is_positive is True",
        "sp.factor(sp.diff(y*delta_b, y)).is_positive is True")
    add("V2 changes only documented exact-factorization predicate and version",v2==expected)
    add("failed V1 receipt preserved",
        sha(BASE/"receipts/primary_v1_attempt_01/summary.json")==
        "99f4597a0f1b303f69368f413d0e77bbc44cd0b5d1564391c942426ee1defb46")
    add("successful primary and separate control retain physical holds",
        primary["passed"]==primary["total"]==99 and ind["passed"]==ind["total"]==19
        and primary["physics_pass"] is False and ind["physics_pass"] is False
        and primary["domain"]["actual_physical_window"]=="UNRESOLVED")
    add("both threshold criteria retained for both planets",
        {(x["planet"],x["criterion"]) for x in primary["planetary_restrictions"]}==
        {("Mercury","C1"),("Mercury","C2"),("Saturn","C1"),("Saturn","C2")})
    add("paper versions preserved, no paper edits required",
        (repo/"papers/P1-Scale-Matching-Reconstruction/VERSION").read_text().strip()=="0.2.0-rc7"
        and (repo/"papers/P2-Rectangular-T3-Casimir/VERSION").read_text().strip()=="0.2.0-rc4")
    backup = repo/".local/force-architecture-20261023-preappend"
    oldreg = backup/"ITSM_RULE9_DEFERRED_REVIEW_REGISTER.md"
    reg = repo/"Theory/Verification/ITSM_RULE9_DEFERRED_REVIEW_REGISTER.md"
    oldhash = "5d49aabe5027c01406fa1f1dfc9f635b970016fcf179eb8a568e6341925af261"
    add("original register and original sidecar retained byte-identically",
        sha(oldreg)==oldhash and sha(Path(str(oldreg)+".sha256"))==
        "f5fa99c6218c13959f895b7eab0c1039586ae64dde6a0f002f75041a26c79c1f")
    add("register update is strictly append-only",
        reg.read_bytes().startswith(oldreg.read_bytes()) and reg.stat().st_size>oldreg.stat().st_size)
    add("mutable current register checksum matches",
        sha(reg)==Path(str(reg)+".sha256").read_text().split()[0])
    add("deferred-review record links this owning report",
        "R9-ARCH-FORCE-COMPARISON-V1" in reg.read_text(encoding="utf-8") and report.name in reg.read_text(encoding="utf-8"))

    commands = [
        ("primary_exact_replay", [sys.executable,"-B",str(BASE/"pkm1_p0b_locality_v2.py"),
          "--repo",str(repo),"--replay",str(primary_dir)],0),
        ("independent_exact_replay", [sys.executable,"-B",str(BASE/"verify_pkm1_p0b_locality_v1.py"),
          "--primary",str(primary_dir/"summary.json"),"--primary-script",str(BASE/"pkm1_p0b_locality_v2.py"),
          "--replay",str(independent_dir)],0),
        ("preserved_failed_v1_exact_replay", [sys.executable,"-B",str(BASE/"pkm1_p0b_locality_v1.py"),
          "--repo",str(repo),"--replay",str(BASE/"receipts/primary_v1_attempt_01")],2)]
    replay = []
    for name, command, expected_exit in commands:
        cp = subprocess.run(command,capture_output=True,text=True,timeout=90)
        try:
            value = json.loads(cp.stdout)
        except json.JSONDecodeError:
            value = {"invalid_json":cp.stdout}
        add(name,cp.returncode==expected_exit and value.get("replay")=="EXACT",
            returncode=cp.returncode,expected_exit=expected_exit,stdout=value,stderr=cp.stderr)
        replay.append({"name":name,"returncode":cp.returncode,"stdout":value,"stderr":cp.stderr})
    head = subprocess.check_output(["git","rev-parse","HEAD"],cwd=repo,text=True).strip()
    add("no commit during goal",head=="b3c744692e8ddd35f457050f45c88d1cbdb514d3")
    failed = [x for x in checks if x["status"]!="PASS"]
    artifact_files = [p for p in BASE.rglob("*") if p.is_file() and not p.is_relative_to(output)]
    files = {str(p.relative_to(repo)).replace("\\","/"):sha(p) for p in artifact_files}
    for p in (contract,report,reg,Path(str(contract)+".sha256"),Path(str(report)+".sha256"),Path(str(reg)+".sha256")):
        files[str(p.relative_to(repo)).replace("\\","/")]=sha(p)
    result = {"result_id":"ITSM-FORCE-ARCHITECTURE-COMPARISON-V1-DELIVERY",
              "status":"PASS_BOUNDED_COMPARISON_DELIVERY" if not failed else "FAIL_DELIVERY",
              "passed":len(checks)-len(failed),"total":len(checks),"checks":checks,
              "replays":replay,"artifact_sha256":files,"physics_pass":False,"gate_effect":"NONE",
              "review_status":"DEFERRED","Rule9_cleared":False,
              "goal_requirements":{
                  "authority":"current pinned source bytes verified",
                  "R4C1_consolidation":"owning report section 2; upstream audits reused, not rerun",
                  "P0B_test":"sections 3-6; 99/99 primary and 19/19 separate controls; physical window unresolved",
                  "comparison_next_step":"sections 1 and 7; one bounded R4C1 physical-sector test recommended, not executed",
                  "paper_track":"section 8 and unchanged VERSION/README/SUBMISSION pins",
                  "preservation_review_delivery":"source/receipt/sidecar/prefix checks and exact replays above"},
              "completed_utc_date":"2026-10-23","local_delivery_date":"2026-10-24"}
    b = (json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n").encode()
    with (output/"delivery.json").open("xb") as f:
        f.write(b)
    with (output/"delivery.json.sha256").open("x",encoding="ascii",newline="\n") as f:
        f.write(hashlib.sha256(b).hexdigest()+"  delivery.json\n")
    print(json.dumps({"status":result["status"],"passed":result["passed"],"total":result["total"],
                      "failed":failed,"physics_pass":False,"delivery":str(output/"delivery.json")}))
    return 0 if not failed else 2


if __name__=="__main__":
    raise SystemExit(main())

