# Standalone ITSM context optimizer

This is a local evidence-selection tool, not a Relay adapter. It has no Relay
imports, model SDK, network client, service, subscription or provider session.
Only Python's standard library is required. Its durable use instruction is
the repository-root `AGENTS.md`.

## Use

```powershell
python -B Scripts/itsm_context.py status
python -B Scripts/itsm_context.py receipt Analysis/MasterTests/outputs/test_02_torus_audit.json
python -B Scripts/itsm_context.py read GEMINI.md --start 1 --lines 60
python -B Scripts/itsm_context.py read GEMINI.md --start 61 --lines 60
python -B Scripts/itsm_context.py --max-chars 4000 run -- rg -n 'physics_pass|status' Analysis/MasterTests/outputs
python -B Scripts/itsm_context.py run -- C:/Users/brend/anaconda3/envs/itsm_env/python.exe -B Analysis/MasterTests/test_02_torus_audit.py
```

The last example uses this machine's existing scientific interpreter; other
machines should use their own verified environment. The script itself does
not create or modify environments. Put `--max-chars` before the subcommand.
An explicit `run` child is subject to exactly the same authorization and
sandbox rules as direct execution; wrapping a command does not approve it.

## Scientific safeguards

- `read` returns a contiguous page with exact line and character-offset
  continuation. Required instructions must be read to EOF. It resolves paths
  inside this workspace and rejects vault/credential file types; no recursive
  corpus loading or arbitrary filesystem discovery occurs.
- `receipt` preserves declared fields, including gate/status flags and
  results, suppresses repetitive successful check rows, and explicitly lists
  failed and unknown rows. A present SHA-256 sidecar must match or summary
  generation fails. Missing sidecars are reported as unknown, not verified.
  Dependency hashes recorded inside a receipt are not automatically verified.
  Physics/gate/Rule-9 flags and check counts also appear outside the potentially
  clipped display body. Exit zero means the view was produced, not that the
  scientific checks or parent gate passed.
- `run` returns the real process exit code. Large output is stored locally;
  failure/hold lines are prioritized in the display. A bounded view may omit
  other important information, so the response explicitly flags omissions
  and directs inspection of the full artifact. There is no automatic claim
  that a nonzero exit is harmless or that exit zero is a physics pass.
- Known credential patterns are redacted before returned/stored command text
  and summaries. This is a best-effort guard, not a security certification.
  A `redacted` flag warns that the view is not byte-identical to the source.
  Original scientific files are never rewritten by a read or summary.
- Outputs and SHA-256 sidecars live under ignored `.local/itsm-context/`.
  They stay local; no telemetry or transcript upload is performed. No logs
  are deleted automatically. They are context aids, not canonical receipts.

## Limits and verification

The character budget applies to the displayed body, not JSON/metadata overhead
or the entire host prompt. Small outputs can become larger after metadata is
added. Returned byte/character counts are measurements, not billed tokens.
Already-sent history, hidden reasoning, host tool definitions and provider
compaction are outside this program's control. It does not make a stronger
model cheaper per token; it aims to avoid sending unnecessary new evidence.

The `run` implementation buffers child output before selecting a view; use
purpose-built streaming tools for multi-gigabyte output. Invalid UTF-8 command
bytes are replaced and labelled; binary and other-encoding scientific data
must be handled with the appropriate reader, not treated as exact text here.

Regression tests:

```powershell
python -B -m unittest discover -s Scripts/tests -p test_itsm_context.py -v
```

No commercial source was copied or modified. The standalone optimizer does
not activate the Commercial Relay optimizer or claim its budgets are active.

### Verified locally, 25 September 2026

All 14 regression tests pass. The initial sandboxed run hit two Windows
temporary-directory permission errors; the approved unsandboxed rerun passed
without changing those assertions. Normal receipt reads and the real T3
symbolic test subsequently ran through the optimizer inside the sandbox.

The live Test 1 receipt contained 5,087 source bytes; its complete summary body
was 1,447 characters, retaining all 29 check outcomes as counts, all declared
results, and the explicit physics/Rule-9 holds. The T3 receipt was 4,376 source
bytes and its summary body 2,125 characters. These are display-body measures;
metadata overhead and billed usage are excluded. No billed-token saving is
claimed. The actual T3 executable still returned 19/19 with physics held.

A subsequent real history search exposed a Windows stdout encoding failure
for Greek symbols. Explicit UTF-8 stdout and a `pi/nabla` regression fixed it;
the full 14-test rerun and the same real search both succeeded. This was an
optimizer defect, not a scientific failure or a reason to change equations.
