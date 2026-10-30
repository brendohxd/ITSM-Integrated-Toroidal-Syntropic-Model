# Original write failure and scoped recovery

The default apply-patch helper and its cached 37f54d68e5533a51 executable could
not create the approved contract in Theory/Core. The exact cause was not
established; this is not evidence of tampering and is not diagnosed as a firewall
or Controlled Folder Access incident.

The contract, inputs, primary/independent executables and all initial receipts
were preserved in the task's other authorized workspace. That contract's hash is
f47060a8d2fb2dcea2c3fa5af6199c13cbb731927fc37bffba83fa4954ab6006.

The already-installed executable at
C:\Users\brend\AppData\Local\Programs\OpenAI\Codex\bin\codex.exe
accepted --codex-run-as-apply-patch and created the identical Core contract.
No model session, software installation, security-setting change or global
configuration change was made. The actual shell reported PowerShell 7.6.5;
this was disclosed before file operations.

Repository integration copies these new artifacts byte-for-byte. The original
secondary-workspace artifacts remain. No source, original receipt or scientific
sidecar is repaired by overwriting it. The V1 inference failure stays preserved.
The optimizer was used for canonical reads; its outside-root receipt refusal
was respected. External task receipts were inspected with bounded structured
views and explicit failure lists instead of claiming optimizer coverage.

