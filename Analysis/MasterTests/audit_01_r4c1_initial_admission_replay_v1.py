"""Strict read-only replay auditor with separate byte and metadata evidence."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SELF=Path(__file__).resolve().relative_to(ROOT).as_posix()
SOURCE='Analysis/MasterTests/test_01_r4c1_initial_admission_v1.py'
CONTRACT='Theory/Gates/RES-001/RES001_R4C1_INITIAL_ADMISSION_REPLAY_AUDIT_V1_CONTRACT_2026-10-18.md'
HOLD='Theory/Gates/RES-001/RES001_R4C1_INITIAL_ADMISSION_V1_REPLAY_HOLD_2026-10-18.md'
ORIGINAL='Analysis/MasterTests/outputs/r4c1_initial_admission_attempt_01'
PINS={SOURCE:'d994707a9261e276b6d9fcb3377acfd75387ce8cdac10f7756e2f791c5787e0a',
 CONTRACT:'83e1d2c3152825dca5ceb1e597c624b98807ff59b71b95f73db0ac95a9e738c1',
 HOLD:'47b347c15fa72f0da7bb860fdd89bf82dd2b7574c5872fb036ece9d7aa594628'}
EXPECTED={
 'summary.json':'993b5cfffcb4b7c4106656a6929dfcc0379858c53e6556f60bb5b56b24ec5f4c',
 'proof.json':'b96ee17ec3d3f14500d0bf59d786411f5e241cbbb238ef49f3dc34657a18646b',
 'certificates.json':'7c3465014fd85d7a98b905eed721c907f2f7764ccefadf856680ecf068d7127a',
 'archive_controls.json':'9267bb9360495eb103f44940e9b4d5120d862ac6ab585eca902ed170fef31673'}
SHA=lambda data:hashlib.sha256(data).hexdigest()
ENC=lambda value:(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def sources():
 pins=dict(PINS);pins[SELF]=SHA((ROOT/SELF).read_bytes());metadata={}
 for name,digest in pins.items():
  path=ROOT/name
  if SHA(path.read_bytes())!=digest:raise ValueError('audit source drift '+name)
  sc=Path(str(path)+'.sha256')
  if sc.read_text().split()[0].lower()!=digest:raise ValueError('audit source sidecar drift '+name)
  for p in (path,sc):
   data=p.read_bytes();metadata[p.relative_to(ROOT).as_posix()]=dict(
     sha256=SHA(data),bytes=len(data),mtime_ns=p.stat().st_mtime_ns)
 return pins,metadata


def snapshot():
 data={};records={}
 for path in sorted((ROOT/ORIGINAL).iterdir()):
  a=path.stat();raw=path.read_bytes();b=path.stat()
  data[path.name]=raw
  records[path.name]=dict(sha256=SHA(raw),bytes=len(raw),mtime_ns=b.st_mtime_ns,
     stable_read=(a.st_size==b.st_size==len(raw) and a.st_mtime_ns==b.st_mtime_ns))
 return data,records


def differences(a,b,path=''):
 if type(a) is not type(b):return [dict(path=path,reason='different types')]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append(dict(path=path+'/'+k,reason='missing key'))
   else:out.extend(differences(a[k],b[k],path+'/'+k))
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [dict(path=path,reason='different list lengths')]
  return [entry for i,(x,y) in enumerate(zip(a,b)) for entry in differences(x,y,path+'/'+str(i))]
 if a==b:return []
 return [dict(path=path,left_preview=str(a)[:1200],right_preview=str(b)[:1200],
              left_value_sha256=SHA(ENC(a)),right_value_sha256=SHA(ENC(b)))]


def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True)
 args=parser.parse_args();dest=(ROOT/args.output).resolve()
 if not dest.is_relative_to(ROOT/'Analysis/MasterTests/outputs'):raise ValueError('outside scientific audit root')
 dest.mkdir(parents=True,exist_ok=False)
 pins,source_before=sources();original,before=snapshot()
 expected_names=set(EXPECTED)|{name+'.sha256' for name in EXPECTED}
 if set(original)!=expected_names:raise ValueError('unexpected original file set')
 for name,digest in EXPECTED.items():
  if SHA(original[name])!=digest:raise ValueError('original payload drift '+name)
  if original[name+'.sha256'].decode('ascii').split()[0].lower()!=digest:raise ValueError('original sidecar drift '+name)
 spec=importlib.util.spec_from_file_location('unchanged_initial_admission_v1_for_audit',ROOT/SOURCE)
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 # No monkeypatch: execute the exact original function and serializer.
 results=module.calculate()
 candidate={name:module.ENC(value) for name,value in results.items()}
 for name,raw in list(candidate.items()):candidate[name+'.sha256']=(SHA(raw)+'  '+name+'\n').encode('ascii')
 saved=dest/'candidate';saved.mkdir()
 for name,raw in candidate.items():
  with (saved/name).open('xb') as stream:stream.write(raw)
 after_bytes,after=snapshot();_,source_after=sources()
 file_rows=[]
 for name in sorted(set(original)|set(candidate)|set(after_bytes)):
  old=original.get(name);new=candidate.get(name);current=after_bytes.get(name)
  byte_match=old is not None and new==old
  original_byte_unchanged=old is not None and current==old
  metadata_unchanged=before.get(name)==after.get(name)
  json_diffs=differences(json.loads(old),json.loads(new)) if name.endswith('.json') and old is not None and new is not None and old!=new else []
  file_rows.append(dict(file=name,recomputed_bytes_match_original=byte_match,
   original_bytes_unchanged=original_byte_unchanged,original_metadata_unchanged=metadata_unchanged,
   before=before.get(name),after=after.get(name),candidate_sha256=SHA(new) if new is not None else None,
   json_differences=json_diffs))
 summary=results['summary.json']
 checks_ok=summary['passed']==summary['total']==217 and all(r['passed'] for r in summary['checks'])
 ok=(set(original)==set(candidate)==set(after_bytes) and checks_ok
     and source_before==source_after and all(row['recomputed_bytes_match_original']
       and row['original_bytes_unchanged'] and row['original_metadata_unchanged']
       and row['before']['stable_read'] and row['after']['stable_read'] for row in file_rows))
 receipt=dict(validation='PASS_AUDITED_FRESH_READ_ONLY_REPLAY_EXACT' if ok else 'FAIL_AUDITED_REPLAY_BYTES_OR_METADATA',
   read_only_replay_passed=ok,calculation_checks_passed=summary['passed'],calculation_checks_total=summary['total'],
   original_directory=ORIGINAL,candidate_directory=saved.relative_to(ROOT).as_posix(),
   original_files_checked=len(original),file_results=file_rows,
   source_sha256=pins,source_metadata=source_before,audit_source_metadata_preserved=source_before==source_after,
   calculation_source_pins=summary['source_sha256'],calculation_source_metadata=summary['source_metadata'],
   earlier_cli_failure_cause='NOT_ESTABLISHED_BY_THIS_AUDIT',
   earlier_cli_failure_relabelled=False,physics_pass=False,gate_effect='NONE',
   Rule9_cleared=False,review_status='DEFERRED',full_initial_data_admission=False,
   stage2_complete=False,stage3_entered=False)
 raw=ENC(receipt)
 with (dest/'audit.json').open('xb') as stream:stream.write(raw)
 with (dest/'audit.json.sha256').open('xb') as stream:stream.write((SHA(raw)+'  audit.json\n').encode('ascii'))
 print(json.dumps({key:receipt[key] for key in ('validation','read_only_replay_passed','calculation_checks_passed',
     'calculation_checks_total','original_files_checked','earlier_cli_failure_cause','physics_pass')}),flush=True)
 return 0 if ok else 1


if __name__=='__main__':raise SystemExit(main())
