import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "itsm_context.py"
spec = importlib.util.spec_from_file_location("itsm_context",SCRIPT)
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


class ContextTests(unittest.TestCase):
    def test_receipt_retains_hold_and_failure_not_pass_count_inference(self):
        result = context.receipt_summary({"physics_pass":False,"gate_effect":"NONE",
            "Rule9":"NOT_COMPLETED","checks":[{"name":"good","passed":True},
            {"name":"sign","passed":False,"residual":"2*x"},{"name":"unknown"}]})
        self.assertFalse(result["declared_fields"]["physics_pass"])
        self.assertEqual(result["failed_checks"][0]["residual"],"2*x")
        self.assertEqual(result["check_summary"],{"schema_recognized":True,"total":3,"passed":1,"failed":1,"unknown":1})

    def test_unknown_schema_does_not_imply_zero_checks_passed(self):
        result = context.receipt_summary({"checks":"not a list"})
        self.assertIsNone(result["check_summary"]["total"])
        self.assertFalse(result["check_summary"]["schema_recognized"])

    def test_failure_in_middle_is_preserved(self):
        text = "\n".join(["ordinary"]*100+["FAIL: reversed source sign"]+["ordinary"]*100)
        result = context.bounded_view(text,700)
        self.assertTrue(result["omitted"])
        self.assertIn("FAIL: reversed source sign",result["text"])
        self.assertEqual(result["critical_lines_omitted"],0)

    def test_too_many_failures_explicitly_reports_omission(self):
        result = context.bounded_view("\n".join(f"FAIL {i}: "+"x"*80 for i in range(100)),500)
        self.assertGreater(result["critical_lines_omitted"],0)
        self.assertLessEqual(len(result["text"]),500)

    def test_long_single_line_budget(self):
        result = context.bounded_view("x"*100000,500)
        self.assertLessEqual(len(result["text"]),500)
        self.assertTrue(result["omitted"])

    def test_contiguous_pagination_and_eof(self):
        text = "a"*600+"\nsecond\nthird"
        first = context.excerpt(text,1,80,0,256)
        self.assertEqual(first["next_line"],1)
        parts = [first["text"].split(" ",1)[1]]
        current = first
        while not current["eof"]:
            current = context.excerpt(text,current["next_line"],80,current["next_column"],256)
            parts.extend(line.split(" ",1)[1] for line in current["text"].splitlines())
        self.assertEqual("".join(parts),"a"*600+"secondthird")

    def test_path_escape_and_vault_rejected(self):
        with self.assertRaises(ValueError): context.local_file("../outside.md")
        with self.assertRaises(ValueError): context.local_file("memory.db")

    def test_redaction_does_not_change_physics_labels(self):
        safe = context.redact("api_key=secret123 Bearer abcdefgh physics_pass=false K_Q=NOT_DERIVED")
        self.assertNotIn("secret123",safe)
        self.assertNotIn("abcdefgh",safe)
        self.assertIn("K_Q=NOT_DERIVED",safe)

    def test_json_credentials_are_redacted(self):
        safe = context.redact('{"api_key": "sensitive value with spaces", "physics_pass": false}')
        self.assertNotIn("sensitive",safe)
        self.assertFalse(json.loads(safe)["physics_pass"])

    def test_status_is_standalone(self):
        result = subprocess.run([sys.executable,"-B",str(SCRIPT),"status"],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["standalone"])
        self.assertFalse(data["relay_dependency"])
        self.assertFalse(data["prior_context_control"])

    def test_unicode_scientific_command_output(self):
        result = subprocess.run([sys.executable,"-B",str(SCRIPT),"run","--",sys.executable,"-c",
            "import sys; sys.stdout.buffer.write(bytes.fromhex('cf80e28887'))"],
            capture_output=True,text=True,encoding="utf-8")
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        self.assertEqual(json.loads(result.stdout)["text"],"π∇")

    def test_private_artifact_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            path,digest = context.persist("exact result",Path(folder))
            self.assertEqual(context.sha(path.read_bytes()),digest)
            self.assertTrue(path.with_suffix(".txt.sha256").read_text().startswith(digest))

    def test_child_failure_exit_and_redacted_output(self):
        result = subprocess.run([sys.executable,"-B",str(SCRIPT),"run","--",sys.executable,"-c",
            "print('FAIL: known negative control; api_key=secret123'); raise SystemExit(7)"],capture_output=True,text=True)
        self.assertEqual(result.returncode,7,result.stderr+result.stdout)
        data = json.loads(result.stdout)
        self.assertEqual(data["exit_code"],7)
        self.assertNotIn("secret123",data["text"])
        artifact = context.ROOT/data["output_artifact"]
        self.assertNotIn("secret123",artifact.read_text())

    def test_bad_sidecar_fails_closed(self):
        # Synthetic files are local runtime data, never scientific receipts.
        context.LOGS.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=context.LOGS) as folder:
            path = Path(folder)/"receipt.json"
            path.write_text('{"physics_pass":false,"checks":[]}')
            path.with_suffix(".json.sha256").write_text("0"*64+"  receipt.json\n")
            result = subprocess.run([sys.executable,"-B",str(SCRIPT),"receipt",str(path)],capture_output=True,text=True)
            self.assertEqual(result.returncode,2)
            self.assertFalse(json.loads(result.stdout)["sidecar_matches"])


if __name__ == "__main__":
    unittest.main()
