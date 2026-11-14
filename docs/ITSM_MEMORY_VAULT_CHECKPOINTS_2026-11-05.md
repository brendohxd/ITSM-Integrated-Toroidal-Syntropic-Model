# ITSM Memory Vault: active routing and checkpoint policy

Status: operational recovery policy, 5 November 2026.

## What was found

The recovered local vault is not empty. The verified database is:

```text
C:\Users\brend\AppData\Local\ITSMMemoryBank-recovered-audit-20261013-v2\memory.db
```

Its read-only verification recorded `PRAGMA integrity_check = ok`, a valid
hash-chained audit, 5,257 source versions, 62,639 chunk versions and 262
proposed memories. The older `ITSMMemoryBank\memory.db` and its corrupt backup
remain preserved and must not be used as the active database.

## Active database versus checkpoint archive

The live SQLite database remains under local `%LOCALAPPDATA%`. It must not be
placed in OneDrive or a Git working tree while it is live: SQLite WAL/SHM files,
file locking and cloud synchronization can create a new corruption path.

The primary standalone checkpoint store is local and outside OneDrive:

```text
C:\Users\brend\AppData\Local\ITSM-Memory-Vault\checkpoints\
```

Each checkpoint is a SQLite-aware standalone backup with a manifest, SHA-256
hash and integrity result. It is an archive, not a live database. The existing
OneDrive checkpoint under `C:\Users\brend\OneDrive\Documents\ITSM Memory Vault\checkpoints\`
is retained as a secondary archive, not as the primary checkpoint target.
A future private repository should store encrypted or Git-LFS-backed checkpoint
artifacts, not ordinary Git blobs containing the database.

The first fresh local primary checkpoint created by the repaired workflow was:

```text
C:\Users\brend\AppData\Local\ITSM-Memory-Vault\checkpoints\20261105-200840-guardrail-validation-20261105\memory.db
```

Checkpoint SHA-256:

```text
06787918572754C32A83CE160806293D8954B71B47EB58AC6A41125741D67259
```

Its manifest integrity result was `ok`; an independent read-only check found
no WAL/SHM sidecars, `audit.valid = true`, 4,467 audit events, and the audit
head `becc77a22e37ac32ed5f3f6ad13d711f218d77ed278b8a5fc2b17b7b5ad152c2`.
The source hash field records that the live source was still open by another
process during backup; this does not invalidate the checkpoint hash or its
read-only integrity/audit checks.

## Creating a checkpoint

From the ITSM repository, run the bounded script when no large sync or repair is
in progress:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Scripts\backup_itsm_memory_vault.ps1 -Label "pre-research"
```

The script refuses to overwrite an existing checkpoint, uses SQLite `.backup`,
checks the resulting database, and records the source/checkpoint hashes. It
does not delete, migrate or modify the source database.

## Recovery rule

Stop MCP hosts and watchers first. Never overwrite the original or an existing
checkpoint. Copy a selected standalone checkpoint to a new local recovery
directory, run integrity and audit checks, search several known ITSM terms, and
only then change the explicit MCP configuration. Preserve the failed database,
WAL/SHM files, logs and verification receipts for forensics.

## Routing rule

The MCP process must receive an explicit `ITSM_MEMORY_CONFIG` or
`ITSM_MEMORY_HOME`. A sandbox-provided `LOCALAPPDATA` must never silently create
an empty fallback vault. The expected configuration is the existing standard
config file, whose `vault.databasePath` points to the verified recovered
database. The plugin now rejects synchronized, network, and Codex-sandbox
database paths, and normal CLI/MCP startup refuses to create a missing database;
only an explicit `init` or verified restore may create one. Restart the MCP host
after changing the environment.

Memory retrieval is continuity infrastructure, not scientific validation.
Source records remain observed evidence; proposed memories remain proposed;
the labels `Derived`, `Conditional`, `Open`, `Rejected` and `None` are preserved
exactly.
