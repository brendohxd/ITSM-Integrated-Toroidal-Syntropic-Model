"""Seal local Master Tests 1-3 review inputs; no provider calls or clearance.

Explicit source roster, transitive receipt pin checks, immutable snapshots,
and exact prompts with full mandatory governance. Uses only the standard library.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = ROOT/'.local/itsm-review'
CORE = 'Theory/Core/ITSM_CORE_IDENTITY_BRIEFING.md'
POLICY = 'Theory/Core/ITSM_RULE9_DEFERRED_REVIEW_POLICY.md'
REGISTER = 'Theory/Verification/ITSM_RULE9_DEFERRED_REVIEW_REGISTER.md'
ACTION = 'Theory/Gates/RES-001/RES001_R4C1_ACTION_FREEZE_2026-09-25.md'
BOUNDED = 'Theory/Gates/ITSM_TESTS_01_03_BOUNDED_AUDIT_CONTRACT_2026-09-24.md'
TORUS = 'Theory/Gates/ITSM_TEST_02_T3_TOPOLOGY_ADDENDUM_2026-09-25.md'
HISTORY = 'Theory/Gates/ITSM_TEST_03_HISTORICAL_CHAIN_ADDENDUM_2026-09-25.md'
TRANSCRIPTION = 'Theory/History/FullArchive/manuscripts/09_v6.1-v7.2-2026-03-09/v7.2_source.md'
SHARED = 'Analysis/MasterTests/tests_01_03_symbolic_audit.py'
# Governance pins changed under the operator's 25 September deferred-review
# decision. Scientific action/receipt pins are unchanged; old snapshots remain.
ANCHORS = {
    'GEMINI.md':'5b23de4b87b910da85beba6aab0e71abcd23dab20586ef5c2957e8dea7c6fb12',
    CORE:'b1014dfce7cc7dc179ee06d145ad206473d0b6631f180c67815a793a5fcce119',
    POLICY:'3d8b1372b9fd340eec91bc209d200f5408353fcef86b54b212bb474463abd809',
    ACTION:'81bfc2e4f17b820f4ab7192c0d29c917af3d26a4ded95b5a3be332c289ad19c3',
}
PHASE1 = [
    'GEMINI.md', CORE, POLICY, ACTION, 'AGENTS.md',
    'Scripts/itsm_context.py', 'docs/ITSM_CONTEXT_OPTIMIZER.md',
]
GOVERNANCE = [
    REGISTER,
    'Theory/Core/ITSM_MASTER_TEST_PROGRAMME_2026-09-24.md',
    'Theory/Core/ITSM_Master_Research_Plan.md',
    'Theory/Core/ITSM_Recovery_Execution_Queue.md',
    'Theory/Core/ITSM_Claim_Migration_Ledger.csv',
    'active_research.md', 'RECOVERY_BRANCH_README.md',
]
PROVENANCE = [
    TRANSCRIPTION,
    'Theory/Gates/UVIR-001/UVIR-001_GATE_REPORT.md',
    'Theory/Gates/UVIR-003/UVIR-003_STAGE_A_REPORT.md',
    'Theory/Gates/UVIR-003/UVIR-003_STAGE_B_TRACK_A_FORCE_ADM_CUBIC.md',
]
STAGES = ('current','full_variation','interacting_background','gr_limit','coefficient_identifiability')
RECEIPTS = {
    f'Analysis/MasterTests/outputs/test_{i:02d}_symbolic_audit.json':SHARED for i in (1,2,3)
}
RECEIPTS['Analysis/MasterTests/outputs/test_02_torus_audit.json'] = 'Analysis/MasterTests/test_02_torus_audit.py'
RECEIPTS['Analysis/MasterTests/outputs/test_03_historical_chain_audit.json'] = 'Analysis/MasterTests/test_03_historical_chain_audit.py'
for stage in STAGES:
    number = '03' if stage=='coefficient_identifiability' else '01'
    script_stage = 'current_audit' if stage=='current' else stage
    RECEIPTS[f'Analysis/MasterTests/outputs/test_{number}_r4c1_{stage}_summary.json'] = (
        f'Analysis/MasterTests/test_{number}_r4c1_{script_stage}.py')
SCIENTIFIC = [
    'Theory/Gates/ITSM_MASTER_TEST_01_SOURCE_VECTOR_CLOSURE_CONTRACT_2026-09-24.md',
    BOUNDED, TORUS, HISTORY, 'Theory/Gates/ITSM_TESTS_01_03_DERIVATION_DISPOSITION_2026-09-25.md',
    'Theory/Gates/RES-001/RES001_R4C1_FIRST_VARIATION_REPORT_2026-09-25.md',
    'Theory/Gates/RES-001/RES001_R4C1_FULL_VARIATION_CHECK_CONTRACT_2026-09-25.md',
    'Theory/Gates/RES-001/RES001_R4C1_FULL_VARIATION_REPORT_2026-09-25.md',
    'Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_trajectory.csv',
    'Manuscript/CoreRecovery/sections/04_conservation_exchange.tex',
    'Manuscript/CoreRecovery/sections/05_weak_field.tex',
    'papers/P1-Scale-Matching-Reconstruction/main.tex',
]
for stage in ('INTERACTING_BACKGROUND','GR_LIMIT','COEFFICIENT_IDENTIFIABILITY'):
    for kind in ('CONTRACT','REPORT'):
        SCIENTIFIC.append(f'Theory/Gates/RES-001/RES001_R4C1_{stage}_{kind}_2026-09-25.md')
SCIENTIFIC += sorted(set(RECEIPTS)|set(RECEIPTS.values()))
TOOLING = [
    'Theory/Verification/prepare_master_tests_review.py',
    'Scripts/tests/test_master_tests_review_packet.py',
    'docs/ITSM_MASTER_TEST_REVIEW.md',
]
SOURCES = sorted(set(PHASE1+GOVERNANCE+PROVENANCE+SCIENTIFIC+TOOLING))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode('utf-8')


def safe_path(base, relative):
    if Path(relative).is_absolute() or '..' in Path(relative).parts or ':' in relative:
        raise ValueError(f'UNSAFE_PATH: {relative}')
    candidate = (base/relative).resolve()
    if not candidate.is_relative_to(base.resolve()):
        raise ValueError(f'OUTSIDE_ROOT: {relative}')
    return candidate


def collect_sources():
    bodies,records = {},{}
    for name in SOURCES:
        path = safe_path(ROOT,name)
        bodies[name] = path.read_bytes()
        sha = digest(bodies[name])
        if name in ANCHORS and sha!=ANCHORS[name]:
            raise ValueError(f'AUTHORITY_PIN_CHANGED: {name}')
        side = safe_path(ROOT,name+'.sha256')
        sidecar = side.read_bytes() if side.is_file() else None
        required = name in SCIENTIFIC or name in (ACTION,POLICY,REGISTER)
        if required and sidecar is None:
            raise ValueError(f'MISSING_SIDECAR: {name}')
        if sidecar is not None:
            tokens = sidecar.decode('ascii').split()
            if not tokens or tokens[0].lower()!=sha:
                raise ValueError(f'SIDECAR_MISMATCH: {name}')
            bodies[name+'.sha256'] = sidecar
        records[name] = dict(sha256=sha,bytes=len(bodies[name]),sidecar_required=required,
                             sidecar='MATCH' if sidecar is not None else 'ABSENT_NOT_REQUIRED',
                             sidecar_sha256=digest(sidecar) if sidecar is not None else None,
                             phase='phase-1' if name in PHASE1 else 'phase-2')
    return bodies,records


def receipt_evidence(bodies):
    evidence = []
    for name,script in RECEIPTS.items():
        data = json.loads(bodies[name])
        if data.get('physics_pass') is not False or data.get('gate_effect')!='NONE':
            raise ValueError(f'UNEXPECTED_GATE_PROMOTION_OR_MISSING_HOLD: {name}')
        if data.get('Rule9') not in ('NOT_CLEARED','NOT_COMPLETED'):
            raise ValueError(f'UNEXPECTED_REVIEW_STATUS: {name}')
        dependencies = {}
        for label,expected in data['source_sha256'].items():
            mapped = label
            if label=='executable':
                mapped = script
            elif label=='contract':
                mapped = HISTORY if 'historical_chain' in name else TORUS if 'torus' in name else BOUNDED
            elif label=='shared_helper':
                mapped = SHARED
            elif label=='transcription':
                mapped = TRANSCRIPTION
            dependencies[mapped] = expected
        if 'script_sha256' in data:
            dependencies[script] = data['script_sha256']
        if 'trajectory_sha256' in data:
            dependencies['Analysis/MasterTests/outputs/test_01_r4c1_interacting_background_trajectory.csv'] = data['trajectory_sha256']
        for dep,expected in dependencies.items():
            if dep not in bodies or digest(bodies[dep])!=expected:
                raise ValueError(f'RECEIPT_DEPENDENCY_MISMATCH: {name}: {dep}')
        rows = data.get('checks')
        if not isinstance(rows,list) or not rows:
            raise ValueError(f'MISSING_CHECK_ROWS: {name}')
        counts = dict(passed=sum(row.get('passed') is True for row in rows),
                      failed=sum(row.get('passed') is False for row in rows),
                      unknown=sum(row.get('passed') is not True and row.get('passed') is not False for row in rows))
        if data.get('total',len(rows))!=len(rows) or data.get('passed',counts['passed'])!=counts['passed']:
            raise ValueError(f'CHECK_COUNT_MISMATCH: {name}')
        # Failed/unknown scientific checks are kept for reviewers, not hidden.
        evidence.append(dict(path=name,sha256=digest(bodies[name]),dependencies=dependencies,
                             checks=counts,total=len(rows),physics_pass=False,
                             interpretation='Receipt content, not independent verification or closure'))
    return evidence


COMMON = '''You are an independent read-only reviewer of Master ITSM Tests 1-3.
No scientific gate is promoted by your report. Return findings to the parent;
do not edit repository/snapshot files, call other models, publish, install tools,
or change settings. Do not enable write tools. Use bounded local reads and the
standalone optimizer when available. A prompt instruction is not proof of a
runner's permission isolation: report the permissions actually available.

Before reporting, state reviewer identity, provider/model/version and session,
exact prompt SHA256, evidence manifest SHA256, phase, actual sources accessed,
prior exposure to results/empirical acceleration data, and any permission or
blinding limitations. Do not invent unknown provenance. Cite each finding to
an exact source path/hash and equation/check; classify SUPPORTED_WITH_SCOPE,
CONTRADICTED, INCOMPLETE or UNKNOWN. Distinguish physical from procedural gaps.
Return your report text and any in-memory calculations; the parent must save
and immediately hash exact outputs. Independent role reports are sealed before
cross-role comparison. No report from the author or another role is evidence
that you performed an independent calculation. Substantive disagreements hold
affected uses; a pending review alone does not stop provisional research.
Review is currently DEFERRED by the operator. This is a saved mandate for use
when review resumes; preparation itself is not authorization to dispatch.

The mandatory rules contain a candidate acceleration relation. Therefore this
packet does NOT certify target-unprimed blinding. Do not consult observational
accelerations, target datasets or unlisted historical archives during Frame.
Disclose any prior/external exposure. Data-blind intent is not a blinding result.
Historical reconstruction is parked, not complete. Model consensus is not
journal peer review. Do not invent a missing microscopic input.
'''
TASKS = {
    'role-A-frame':'''ROLE A: Mathematical and dimensional auditor, FRAME phase.
Independently derive from the supplied R4C1 action: sector stresses/currents and
charge identities; the declared zero-exchange/GR limits; the metric/Euler/local
force equations with approximation and boundary conditions; the invariant
parameters governing acceleration relative to expansion. Establish whether a
unique coefficient and redshift law follow or remain undetermined. Analyze
field-chart freedom separately from physically distinct couplings. Treat T3
boundary/zero-mode conditions explicitly. Do not infer a missing equation.
Only phase-1 sources and this prompt may be accessed before your first report
is sealed. Do not read phase-2, parent scripts/receipts/results, the dashboard,
other reviewers or comparison prompts. Report anything that cannot be derived.
The embedded governance and action sources below are complete, not excerpts.
''',
    'role-A-compare':'''ROLE A: COMPARE phase, allowed only after your Frame output is saved,
hashed and its exposure record reviewed. Compare your independent derivation
against the phase-2 variation, T3, background, GR and coefficient audits.
Locate exact agreements/disagreements rather than merely accepting check
counts. Audit normalized-projector variations, regulator signs, boundary terms,
physical versus fixed-metric Hessians, canonical normalization, GR endpoints
and coefficient identifiability. Keep any initial error in your sealed record;
issue an attributed addendum instead of overwriting it. No gate promotion.
''',
    'role-B-pipeline':'''ROLE B: Numerical and pipeline auditor.
Independently inspect phase-2 executables, all ten receipts, dependency hashes
and the B1 trajectory. Check numerical error definitions, tolerances, invariant
drifts, convergence, negative controls and exact versus floating identities.
Inspect executable coverage before trusting PASS or count totals. In particular
separate constraint residuals from independently differenced sector balances.
Verify the physical scope of every matrix/eigenspace claim and report missing
full interacting constraints rather than filling them with a control.
You have read-only authority. Many main() functions overwrite receipts; do NOT
call them against this snapshot or the worktree. Use Python -B and pure
functions/in-memory integrations, returning results as text. If a faithful
replay needs writes, specify a parent-mediated isolated scratch command and
await its verified output; report what you personally checked. No direct
source/output repair or threshold change inside the review. Do not see other
reviewers' reports until all initial reports are sealed.
''',
    'role-C-claims':'''ROLE C: Claim hygiene and gate-ledger auditor.
Compare the phase-2 evidence to the live-snapshot core identity, master
programme, owning contracts, active_research.md and the complete
ITSM_Claim_Migration_Ledger.csv. Audit Tests 1,2,3 requirement by requirement.
Distinguish canonical action, approved classical candidate, implementation
check, conditional force reduction, counterexample and observational result.
Identify any claim missing an assumption, domain, parent dependency, source
hash or independent review. Keep the parked history requirement and blinding
limitation visible. Check manuscript corrections and remaining publication
holds; do not infer publication readiness. Existing older Rule-9 certificates
do not review this snapshot. Do not see other reviewers' reports until all
initial reports are sealed. Return a coverage/contradiction table, not clearance.
''',
}


def make_prompts(bodies):
    prompts = {}
    for role,task in TASKS.items():
        out = (COMMON+'\n'+task+'\n').encode('utf-8')
        names = ['GEMINI.md',CORE,POLICY]+([ACTION] if role=='role-A-frame' else [])
        for name in names:
            out += f'\n--- BEGIN COMPLETE SOURCE: {name}; SHA256={digest(bodies[name])} ---\n'.encode()
            out += bodies[name]
            out += f'\n--- END COMPLETE SOURCE: {name} ---\n'.encode()
        out += b'\nUse the sealed manifest source roster for the permitted phase. No dispatch is performed by this text.\n'
        prompts[f'prompts/{role}.txt'] = out
    return prompts


def validate_prompts(prompts,bodies):
    if set(prompts)!={f'prompts/{name}.txt' for name in TASKS}:
        raise ValueError('PROMPT_ROLE_SET_CHANGED')
    for name,body in prompts.items():
        if any(bodies[source] not in body for source in (CORE,'GEMINI.md',POLICY)):
            raise ValueError(f'MANDATORY_FULL_GOVERNANCE_MISSING: {name}')
    if bodies[ACTION] not in prompts['prompts/role-A-frame.txt']:
        raise ValueError('FRAME_ACTION_MISSING')


def file_payloads(bodies,records,prompts):
    payload = dict(prompts)
    for name,record in records.items():
        target = f"{record['phase']}/{name}"
        payload[target] = bodies[name]
        if name+'.sha256' in bodies:
            payload[target+'.sha256'] = bodies[name+'.sha256']
    return payload


def assert_payload_hashes(files,payload):
    if set(files)!=set(payload):
        raise ValueError('PACKET_FILE_SET_MISMATCH')
    for name,expected in files.items():
        if digest(payload[name])!=expected:
            raise ValueError(f'PACKET_BYTES_CHANGED: {name}')


def emit_immutable(path,body):
    if path.exists():
        if not path.is_file() or path.read_bytes()!=body:
            raise ValueError(f'REFUSE_EXISTING_DIFFERENT_BYTES: {path}')
        return
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as handle:
        handle.write(body)


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()


def build():
    subprocess.run(['git','check-ignore','--quiet','--','.local/itsm-review/_privacy_probe'],cwd=ROOT,check=True)
    if git('branch','--show-current')!='recovery/v12-core-architecture':
        raise ValueError('WRONG_RESEARCH_BRANCH')
    bodies,records = collect_sources()
    receipts = receipt_evidence(bodies)
    prompts = make_prompts(bodies)
    validate_prompts(prompts,bodies)
    payload = file_payloads(bodies,records,prompts)
    # Hash every newly generated prompt immediately; retain source sidecars as-is.
    for name,body in list(prompts.items()):
        payload[name+'.sha256'] = f'{digest(body)}  {Path(name).name}\n'.encode('ascii')
    manifest = dict(schema='ITSM_MASTER_TESTS_REVIEW_SNAPSHOT_v2',
        scope='Master Tests 1-3: bounded controls, R4C1 and unmet requirements',
        branch=git('branch','--show-current'),head=git('rev-parse','HEAD'),
        worktree_context='uncommitted source snapshot; source hashes, not HEAD, identify reviewed bytes',
        sources=records,receipts=receipts,files={n:digest(b) for n,b in sorted(payload.items())},
        prompts={n:dict(sha256=digest(b),bytes=len(b),status='NOT_DISPATCHED') for n,b in prompts.items()},
        roles={r:dict(reviewer=None,status='NOT_ASSIGNED',report_sha256=None) for r in ('A','B','C')},
        protocol=['A Frame sealed before A Compare','A/B/C initial reports sealed before cross-role comparison',
                  'Substantive discrepancies hold affected uses; pending review alone does not block provisional research'],
        exclusions={'historical_reconstruction':'PARKED_BY_USER_NOT_COMPLETE',
                    'TOP-X4':'unchanged; older review certificates do not cover this snapshot',
                    'observational_likelihoods':'NOT_RUN; upstream predictions incomplete'},
        blinding=dict(independently_verified=False,target_unprimed=False,
                      reason='Mandatory GEMINI.md contains an acceleration-coefficient example',
                      prior_exposure='REVIEWER_ATTESTATION_REQUIRED',phase_boundary_enforced=False),
        readiness='LOCAL_EVIDENCE_SEALED_ONLY_NOT_DISPATCH_READY',
        missing_dispatch_controls=['explicit provider/model/quota approval','read-only permission verification',
                                   'fresh reviewer identities and exposure records','enforced phase access and exact prompt submission'],
        Rule9='NOT_CLEARED',physics_pass=False,gate_effect='NONE',
        review_status='DEFERRED',
        research_execution_policy='PROVISIONAL_WHEN_REVIEW_IS_ONLY_BLOCKER',
        substantive_scope_assessment_required=True,
        canonical_goal_complete=False,external_dispatch='NOT_PERFORMED')
    manifest_bytes = encoded(manifest)
    packet = safe_path(OUTPUT_ROOT,'master-tests-'+digest(manifest_bytes)[:16])
    for name,body in sorted(payload.items()):
        emit_immutable(safe_path(packet,name),body)
    # Manifest is the last completeness marker; a partial directory is not sealed.
    emit_immutable(packet/'manifest.json',manifest_bytes)
    emit_immutable(packet/'manifest.json.sha256',f'{digest(manifest_bytes)}  manifest.json\n'.encode('ascii'))
    return verify(packet)


def validate_nonclearance(manifest):
    schema = manifest.get('schema')
    if schema not in ('ITSM_MASTER_TESTS_REVIEW_SNAPSHOT_v1','ITSM_MASTER_TESTS_REVIEW_SNAPSHOT_v2'):
        raise ValueError('UNKNOWN_REVIEW_SNAPSHOT_SCHEMA')
    if (manifest.get('Rule9')!='NOT_CLEARED' or manifest.get('physics_pass') is not False
        or manifest.get('gate_effect')!='NONE' or manifest.get('canonical_goal_complete') is not False
        or manifest.get('external_dispatch')!='NOT_PERFORMED'):
        raise ValueError('PACKET_CANNOT_CERTIFY_REVIEW')
    if schema=='ITSM_MASTER_TESTS_REVIEW_SNAPSHOT_v2' and (
        manifest.get('review_status')!='DEFERRED'
        or manifest.get('research_execution_policy')!='PROVISIONAL_WHEN_REVIEW_IS_ONLY_BLOCKER'
        or manifest.get('substantive_scope_assessment_required') is not True):
        raise ValueError('DEFERRED_REVIEW_POLICY_MISMATCH')
    if schema=='ITSM_MASTER_TESTS_REVIEW_SNAPSHOT_v1' and any(key in manifest for key in (
        'review_status','research_execution_policy','substantive_scope_assessment_required')):
        raise ValueError('LEGACY_SNAPSHOT_CANNOT_DECLARE_NEW_POLICY')
    if set(manifest.get('roles',{}))!={'A','B','C'} or any(
        role!={'reviewer':None,'status':'NOT_ASSIGNED','report_sha256':None}
        for role in manifest['roles'].values()):
        raise ValueError('PACKET_CANNOT_ASSIGN_OR_CERTIFY_REVIEWERS')
    blind = manifest.get('blinding',{})
    if any(blind.get(key) is not False for key in (
        'independently_verified','target_unprimed','phase_boundary_enforced')):
        raise ValueError('PACKET_CANNOT_CERTIFY_BLINDING_OR_ISOLATION')


def verify(packet,expected_manifest=None):
    packet = Path(packet).resolve()
    if not packet.is_relative_to(OUTPUT_ROOT.resolve()) or packet==OUTPUT_ROOT.resolve():
        raise ValueError('PACKET_OUTSIDE_PRIVATE_REVIEW_ROOT')
    manifest_body = (packet/'manifest.json').read_bytes()
    side = (packet/'manifest.json.sha256').read_text(encoding='ascii').split()
    if not side or side[0]!=digest(manifest_body):
        raise ValueError('MANIFEST_HASH_MISMATCH')
    if expected_manifest is not None and digest(manifest_body)!=expected_manifest:
        raise ValueError('APPROVED_MANIFEST_HASH_MISMATCH')
    manifest = json.loads(manifest_body)
    validate_nonclearance(manifest)
    payload = {name:safe_path(packet,name).read_bytes() for name in manifest['files']}
    actual = {p.relative_to(packet).as_posix() for p in packet.rglob('*') if p.is_file()}
    if actual!=set(payload)|{'manifest.json','manifest.json.sha256'}:
        raise ValueError('UNDECLARED_PACKET_FILE')
    assert_payload_hashes(manifest['files'],payload)
    stale = [name for name,row in manifest['sources'].items()
             if not safe_path(ROOT,name).is_file() or digest(safe_path(ROOT,name).read_bytes())!=row['sha256']]
    stale += [name+'.sha256' for name,row in manifest['sources'].items()
              if row['sidecar_sha256'] is not None and (
                  not safe_path(ROOT,name+'.sha256').is_file()
                  or digest(safe_path(ROOT,name+'.sha256').read_bytes())!=row['sidecar_sha256'])]
    if stale:
        raise ValueError('LIVE_SOURCES_CHANGED_RESEAL_REQUIRED: '+', '.join(stale))
    return dict(validation='PASS_LOCAL_SNAPSHOT_ONLY',packet=packet.relative_to(ROOT).as_posix(),
                manifest_sha256=digest(manifest_body),sources=len(manifest['sources']),
                receipts=len(manifest['receipts']),prompts=len(manifest['prompts']),
                files=len(payload),review_reports=0,Rule9='NOT_CLEARED',physics_pass=False,
                review_status=manifest.get('review_status','UNRECORDED_IN_LEGACY_SNAPSHOT'),
                research_execution_policy=manifest.get('research_execution_policy','UNRECORDED_IN_LEGACY_SNAPSHOT'),
                provider_calls=0,phase_boundary_enforced=False,target_unprimed_blinding=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',type=Path,help='Verify an existing snapshot and current source identity; no writes')
    parser.add_argument('--expected-manifest-sha256',help='Required trusted outer hash when checking an approved dispatch snapshot')
    args = parser.parse_args()
    if args.expected_manifest_sha256 and not args.verify:
        parser.error('--expected-manifest-sha256 requires --verify')
    print(json.dumps(verify(args.verify,args.expected_manifest_sha256) if args.verify else build(),indent=2))


if __name__=='__main__':
    main()
