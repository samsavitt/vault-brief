---
created: 2026-04-28
session: vault-brief v0.1 — log.md parsing + project-name arg
status: applied
---

# Vault Bridge Update Packet

## 1. Target vault path
`~/Documents/vaults/jarvis-one/projects/sandbox-projects/vault-brief/context-snapshot.md`

## 2. Summary of repo changes
Committed v0.1 (a110e9f). Two additions to `brief.py`:
- `extract_log_entries(text, n=3)` — scans log.md for the first N `##` heading lines (most-recent-first log, so first = newest).
- `make_bridge_path(name)` + `BRIDGE_BASE` constant (env-var `VAULT_BRIDGE_BASE` overrides the hardcoded default, enabling test isolation with `tmp_path`).
- `main()` now takes `<project-name>` instead of a full path and reads both `context-snapshot.md` and `log.md`, erroring if either is missing.
- `test_brief.py` updated to 9 tests (4 unit, 5 integration), all passing. `run()` and `make_snapshot()` helpers replaced with `run(tmp_path, name)` and `make_bridge(tmp_path, name, ...)`.

Note: the session constraint said "do not retire the project after v0.1 — we may continue with small learning-focused improvements." The current context-snapshot still says "Then retire this project." That language is now stale.

## 3. Proposed context-snapshot.md edits

### Edit 1 — Current goal (stale)

Before:
```
Ship vault-brief v0.1: add `log.md` parsing (last 3 entries) and project-name argument support. Then retire this project and apply lessons to job-agent.
```

After:
```
vault-brief v0.1 shipped. Project remains active for small learning-focused improvements. Next improvement TBD.
```

### Edit 2 — Next action (stale)

Before:
```
Open a new repo session at ~/Projects/sandbox-projects/vault-brief/. Add log.md parsing and project-name-to-path lookup to brief.py. Update tests. Commit as v0.1.
```

After:
```
No active task. Awaiting next improvement idea.
```

## 4. Proposed log.md entry

```
## 2026-04-28 update | v0.1 shipped — log.md parsing and project-name arg added.

`brief.py` now accepts a project name (constructs bridge path from `BRIDGE_BASE`). Reads last 3 `##` entries from `log.md` and appends them to the brief. Env-var `VAULT_BRIDGE_BASE` allows test isolation. 9/9 tests pass. Project retirement deferred; small learning-focused improvements may follow.
```

## 5. Open questions
None.

## 6. Necessity
Required — Current goal and Next action are stale post-v0.1, and retirement language conflicts with the session constraint. Log needs the v0.1 entry.

---

---
created: 2026-04-29
session: vault-brief v0.2 — full-path arg, bridge-dir error, usage/output improvements
status: applied
---

# Vault Bridge Update Packet — v0.2

## 1. Target vault path
`~/Documents/vaults/jarvis-one/projects/sandbox-projects/vault-brief/context-snapshot.md`

## 2. Summary of repo changes
Committed v0.2 (a6836c0). Changes to `brief.py` and `test_brief.py`:
- `resolve_bridge_path(arg)` — replaces `make_bridge_path` logic; detects absolute/tilde paths and bypasses `BRIDGE_BASE`, falls back to name-mode for bare names. `make_bridge_path` kept as a thin wrapper for compatibility.
- Bridge directory existence check added before file checks; produces `Error: bridge directory not found: <path>` instead of the misleading snapshot-not-found error.
- Usage text expanded to two lines showing both invocation modes.
- `---` separator printed before `LOG (LAST 3)` block in output.
- `test_brief.py` updated to 12 tests (up from 9): added `test_resolve_bridge_path_absolute_bypasses_base`, `test_full_path_arg`, `test_missing_bridge_dir_exits_nonzero`, updated `test_no_args_exits_nonzero` to assert second usage line. All 12 pass.

Note: bridge was already accurate before this packet was written. The v0.2 context-snapshot and log.md edits below were applied during the same vault session that produced the packet.

## 3. Proposed context-snapshot.md edits

### Edit 1 — Current goal

Before:
```
vault-brief v0.1 shipped. Project remains active for small learning-focused improvements. Next improvement TBD.
```

After:
```
vault-brief v0.2 shipped. Usability improvements: full-path arg support, clearer error messages, improved usage text, output separator. Project remains active for learning-focused improvements.
```

### Edit 2 — Next action (unchanged)
```
No active task. Awaiting next improvement idea.
```

## 4. Proposed log.md entry

```
## 2026-04-29 v0.2 | Full-path arg, bridge-dir error, usage/output improvements. Commit a6836c0. 12/12 tests pass.
```

## 5. Open questions
None.

## 6. Necessity
Required — Current goal is stale post-v0.2. Log needs the v0.2 entry. Applied synthetically in the same vault session.
