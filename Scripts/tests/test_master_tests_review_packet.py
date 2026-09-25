"""Read-only/in-memory regression tests for the Master Tests review preparation."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Theory/Verification'))
import prepare_master_tests_review as packet


class ReviewPacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bodies,cls.records = packet.collect_sources()
        cls.prompts = packet.make_prompts(cls.bodies)

    def mutate_receipt(self,update):
        bodies = dict(self.bodies)
        name = 'Analysis/MasterTests/outputs/test_01_symbolic_audit.json'
        data = json.loads(bodies[name])
        update(data)
        bodies[name] = packet.encoded(data)
        return bodies

    def test_current_receipt_dependencies(self):
        rows = packet.receipt_evidence(self.bodies)
        self.assertEqual(len(rows),10)
        self.assertTrue(all(row['physics_pass'] is False for row in rows))

    def test_full_governance_in_every_prompt(self):
        packet.validate_prompts(self.prompts,self.bodies)
        for body in self.prompts.values():
            self.assertIn(self.bodies[packet.CORE],body)
            self.assertIn(self.bodies['GEMINI.md'],body)
            self.assertIn(self.bodies[packet.POLICY],body)

    def test_deferred_policy_cannot_be_omitted(self):
        prompts = dict(self.prompts)
        prompts['prompts/role-C-claims.txt'] = prompts['prompts/role-C-claims.txt'].replace(self.bodies[packet.POLICY],b'')
        with self.assertRaisesRegex(ValueError,'MANDATORY_FULL_GOVERNANCE'):
            packet.validate_prompts(prompts,self.bodies)

    def test_historical_transcription_pin_checked(self):
        bodies = dict(self.bodies)
        bodies[packet.TRANSCRIPTION] += b' changed'
        with self.assertRaisesRegex(ValueError,'RECEIPT_DEPENDENCY_MISMATCH'):
            packet.receipt_evidence(bodies)

    def test_deferred_register_evidence_pins(self):
        register = self.bodies[packet.REGISTER].decode('utf-8')
        for name in packet.RECEIPTS:
            with self.subTest(receipt=name):
                self.assertIn(f'| {Path(name).name} | {packet.digest(self.bodies[name])} |',register)

    def test_frame_action_not_parent_report(self):
        body = self.prompts['prompts/role-A-frame.txt']
        self.assertIn(self.bodies[packet.ACTION],body)
        report = 'Theory/Gates/RES-001/RES001_R4C1_COEFFICIENT_IDENTIFIABILITY_REPORT_2026-09-25.md'
        self.assertNotIn(self.bodies[report],body)
        self.assertEqual(self.records[packet.ACTION]['phase'],'phase-1')
        self.assertEqual(self.records[report]['phase'],'phase-2')

    def test_missing_governance_rejected(self):
        prompts = dict(self.prompts)
        prompts['prompts/role-B-pipeline.txt'] = b'Abbreviated mandate'
        with self.assertRaisesRegex(ValueError,'MANDATORY_FULL_GOVERNANCE'):
            packet.validate_prompts(prompts,self.bodies)

    def test_missing_role_rejected(self):
        prompts = dict(self.prompts)
        del prompts['prompts/role-C-claims.txt']
        with self.assertRaisesRegex(ValueError,'PROMPT_ROLE_SET'):
            packet.validate_prompts(prompts,self.bodies)

    def test_changed_dependency_rejected(self):
        bodies = dict(self.bodies)
        bodies[packet.ACTION] += b'\nchanged\n'
        with self.assertRaisesRegex(ValueError,'RECEIPT_DEPENDENCY_MISMATCH'):
            packet.receipt_evidence(bodies)

    def test_unknown_dependency_rejected(self):
        bodies = self.mutate_receipt(lambda d:d['source_sha256'].update({'missing/path':'0'*64}))
        with self.assertRaisesRegex(ValueError,'RECEIPT_DEPENDENCY_MISMATCH'):
            packet.receipt_evidence(bodies)

    def test_receipt_promotion_rejected(self):
        bodies = self.mutate_receipt(lambda d:d.update(physics_pass=True))
        with self.assertRaisesRegex(ValueError,'UNEXPECTED_GATE_PROMOTION'):
            packet.receipt_evidence(bodies)

    def test_count_mismatch_rejected(self):
        bodies = self.mutate_receipt(lambda d:d.update(total=100000))
        with self.assertRaisesRegex(ValueError,'CHECK_COUNT_MISMATCH'):
            packet.receipt_evidence(bodies)

    def test_failed_check_retained(self):
        def update(data):
            data['checks'][0]['passed'] = False
            data['local_symbolic_validation'] = 'FAIL'
        rows = packet.receipt_evidence(self.mutate_receipt(update))
        self.assertEqual(rows[0]['checks']['failed'],1)
        self.assertFalse(rows[0]['physics_pass'])

    def test_unknown_check_retained(self):
        def update(data):
            data['checks'][0]['passed'] = None
            data['local_symbolic_validation'] = 'UNKNOWN'
        rows = packet.receipt_evidence(self.mutate_receipt(update))
        self.assertEqual(rows[0]['checks']['unknown'],1)

    def test_immutable_payload_detects_tampering(self):
        payload = packet.file_payloads(self.bodies,self.records,self.prompts)
        hashes = {n:packet.digest(b) for n,b in payload.items()}
        packet.assert_payload_hashes(hashes,payload)
        payload['prompts/role-A-frame.txt'] += b' injected'
        with self.assertRaisesRegex(ValueError,'PACKET_BYTES_CHANGED'):
            packet.assert_payload_hashes(hashes,payload)

    def test_missing_snapshot_file_rejected(self):
        with self.assertRaisesRegex(ValueError,'PACKET_FILE_SET'):
            packet.assert_payload_hashes({'missing':'0'*64},{})

    def test_unsafe_paths_rejected(self):
        for name in ('../outside','C:/outside','/outside'):
            with self.subTest(name=name),self.assertRaises(ValueError):
                packet.safe_path(ROOT,name)

    def test_nonclearance_boundary(self):
        base = dict(schema='ITSM_MASTER_TESTS_REVIEW_SNAPSHOT_v2',
            Rule9='NOT_CLEARED',physics_pass=False,gate_effect='NONE',
            review_status='DEFERRED',research_execution_policy='PROVISIONAL_WHEN_REVIEW_IS_ONLY_BLOCKER',
            substantive_scope_assessment_required=True,
            canonical_goal_complete=False,external_dispatch='NOT_PERFORMED',
            roles={r:dict(reviewer=None,status='NOT_ASSIGNED',report_sha256=None) for r in 'ABC'},
            blinding=dict(independently_verified=False,target_unprimed=False,phase_boundary_enforced=False))
        packet.validate_nonclearance(base)
        for key,value in (('review_status','CLEARED'),
                          ('research_execution_policy','HOLD_FOR_REVIEW'),
                          ('substantive_scope_assessment_required',False)):
            changed = copy.deepcopy(base)
            changed[key] = value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'DEFERRED_REVIEW_POLICY'):
                packet.validate_nonclearance(changed)
        legacy = copy.deepcopy(base)
        legacy['schema'] = 'ITSM_MASTER_TESTS_REVIEW_SNAPSHOT_v1'
        for key in ('review_status','research_execution_policy','substantive_scope_assessment_required'):
            del legacy[key]
        packet.validate_nonclearance(legacy)
        legacy['review_status'] = 'CLEARED'
        with self.assertRaisesRegex(ValueError,'LEGACY_SNAPSHOT_CANNOT_DECLARE_NEW_POLICY'):
            packet.validate_nonclearance(legacy)
        for key,value in (('Rule9','CLEARED'),('physics_pass',True),('canonical_goal_complete',True),
                          ('external_dispatch','PERFORMED')):
            changed = copy.deepcopy(base)
            changed[key] = value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'PACKET_CANNOT_CERTIFY'):
                packet.validate_nonclearance(changed)
        for key in base['blinding']:
            changed = copy.deepcopy(base)
            changed['blinding'][key] = True
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'BLINDING_OR_ISOLATION'):
                packet.validate_nonclearance(changed)
        changed = copy.deepcopy(base)
        changed['roles']['A']['reviewer'] = 'author'
        with self.assertRaisesRegex(ValueError,'ASSIGN_OR_CERTIFY_REVIEWERS'):
            packet.validate_nonclearance(changed)


if __name__=='__main__':
    unittest.main(verbosity=2)
