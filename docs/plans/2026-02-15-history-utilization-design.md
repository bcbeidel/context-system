# History & Utilization Tracking Design

**Date:** 2026-02-15
**Status:** Approved

## Problem Statement

The `.dewey/history/` and `.dewey/utilization/` directories are scaffolded by `/dewey:init` but empty. Without history, health checks report absolute counts with no trend ("8 issues") instead of deltas ("3 new issues since last run"). Without utilization data, Tier 3 scope decisions are based on structural analysis only -- the `health-review.md` workflow already gracefully degrades when utilization data is absent but cannot surface "not referenced in N days" signals.

## Design

### History: Health Score Baselines

**New file:** `dewey/skills/health/scripts/history.py`

Two functions:
- `record_snapshot(kb_root, tier1_summary, tier2_summary)` -- appends a timestamped snapshot to `.dewey/history/health-log.jsonl`
- `read_history(kb_root, limit=10)` -- reads the last N snapshots for trend display

**Format** (one JSONL line per snapshot):
```json
{"timestamp": "2026-02-15T14:30:00", "tier1": {"total_files": 9, "fail_count": 1, "warn_count": 0, "pass_count": 8}, "tier2": {"total_files_scanned": 9, "files_with_triggers": 8, "trigger_counts": {"depth_accuracy": 6}}}
```

**Integration:** `check_kb.py` auto-persists a snapshot after each run (Tier 1 only, `--tier2`, or `--both`). The audit workflow can show "vs. last run: +2 new issues, -1 resolved."

### Utilization: Reference Tracking

**New file:** `dewey/skills/health/scripts/utilization.py`

Two functions:
- `record_reference(kb_root, file_path, context="user")` -- appends to `.dewey/utilization/log.jsonl`
- `read_utilization(kb_root)` -- returns per-file stats: `{file: {count, last_referenced, first_referenced}}`

**Format** (one JSONL line per reference event):
```json
{"file": "docs/code-quality/naming-conventions.md", "timestamp": "2026-02-15T14:30:00", "context": "audit"}
```

**Integration:** Health workflows call `record_reference()` when they read a topic during audit/review. The `health-review.md` Tier 3 workflow uses `read_utilization()` to surface pruning signals.

### Changes to Existing Code

- `check_kb.py` -- call `record_snapshot()` after running checks
- `health-audit.md` -- mention history comparison in report output
- `health-review.md` -- use utilization data for Tier 3 scope decisions (already designed for this)

### What Stays the Same

- All existing validators, triggers, and workflows unchanged
- Stdlib only, no new dependencies
- Both log files are append-only JSONL -- no corruption risk, no locking needed

## Success Criteria

- `record_snapshot()` persists after each health check run
- `read_history()` returns the last N snapshots in chronological order
- `record_reference()` appends to the utilization log
- `read_utilization()` returns per-file stats with count, last_referenced, first_referenced
- Existing tests unaffected (263 passing)
- New tests cover both modules
