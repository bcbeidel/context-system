# Utilization-Driven Curation Recommendations Design

**Date:** 2026-02-15
**Status:** Approved

## Problem

The utilization hook now captures which knowledge base files agents actually read. The health system tracks file inventory and content quality. But nothing connects these two data sources to surface actionable curation recommendations. A knowledge base with 36 files has no way to tell you which files are ignored, which are over-relied-upon, or which high-traffic content is going stale.

## Design

### Architecture

New function `generate_recommendations()` in `check_knowledge_base.py` that joins utilization data against the file inventory to produce curation recommendations.

```
utilization log.jsonl ──┐
                        ├──> generate_recommendations() ──> list[dict]
_discover_md_files() ───┘
         |
check_freshness() ──────────> cross-referenced for stale_high_use
```

CLI gets `--recommendations` flag with configurable thresholds `--min-reads` and `--min-days`.

### Output Format

Each recommendation follows the project's list-of-dicts pattern:

```python
{
    "file": "docs/sagemaker/overview.md",
    "recommendation": "expand_depth",
    "reason": "Read 47 times but only overview depth -- consider adding working-knowledge file",
    "data": {"read_count": 47, "depth": "overview", "area": "sagemaker"}
}
```

Top-level output:

```python
{
    "recommendations": [...],
    "summary": {
        "total_files": 36,
        "files_with_recommendations": 12,
        "by_category": {
            "never_referenced": 8,
            "expand_depth": 2,
            "low_utilization": 1,
            "stale_high_use": 1
        }
    }
}
```

### Recommendation Categories

Four categories, ordered by priority (highest first). A file gets at most one recommendation:

**1. `stale_high_use`** -- File with high read count AND a freshness warning from Tier 1.
- Detection: Read count above median AND `check_freshness()` returns issues for this file.
- Signal: Agents rely on this content but it may be outdated. Prioritize freshening.

**2. `expand_depth`** -- Overview file with disproportionately high reads.
- Detection: File is `overview` depth AND read count > 2x the median across all files.
- Signal: Agents keep loading the overview because no working-depth file exists for the topic they need.

**3. `low_utilization`** -- Working or reference file with reads far below its area's overview.
- Detection: Read count < 10% of its area's overview read count (and overview has meaningful reads).
- Signal: Over-invested content that agents don't reach for. Consider demoting or merging.

**4. `never_referenced`** -- File exists in inventory but has zero entries in the utilization log.
- Detection: File path absent from `read_utilization()` results.
- Signal: Content may be irrelevant or undiscoverable.

### Threshold & Gating

```python
def generate_recommendations(
    knowledge_base_root: Path,
    min_reads: int = 10,
    min_days: int = 7,
) -> dict:
```

**Gating check:** If total reads across all files < `min_reads`, OR the timespan between first and last utilization timestamp < `min_days`, return empty recommendations with a skip reason:

```python
{"recommendations": [], "skipped": "Insufficient data: 3 reads over 1 day (need 10 reads over 7 days)"}
```

Override with `--min-reads 0 --min-days 0` for testing.

**Area grouping:** Files grouped by first path segment (`sagemaker/overview.md` -> area `sagemaker`). Overview identified by filename `overview.md`. Per-area stats feed `expand_depth` and `low_utilization` detection.

### CLI Integration

```bash
# Standalone recommendations (default thresholds)
python3 check_knowledge_base.py --knowledge-base-root sandbox --recommendations

# Testing with no thresholds
python3 check_knowledge_base.py --knowledge-base-root sandbox --recommendations --min-reads 0 --min-days 0

# Combined with full health check
python3 check_knowledge_base.py --knowledge-base-root sandbox --both --recommendations
```

When combined with `--both`, the recommendations key is added to the combined report:

```json
{"tier1": {...}, "tier2": {...}, "recommendations": {...}}
```

## Files Affected

| File | Changes |
|------|---------|
| `dewey/skills/health/scripts/check_knowledge_base.py` | Add `generate_recommendations()`, `--recommendations`/`--min-reads`/`--min-days` CLI flags, integration with `--both` |
| `tests/skills/health/test_recommendations.py` | New test file for all recommendation categories, gating logic, CLI output |

## Not In Scope

- Persisting recommendations to a file (recommendations are computed on demand)
- Health score enrichment from utilization (recommendations are separate from health issues)
- Automatic actions (archiving, promoting) -- recommendations are informational only
- Backwards compatibility for utilization logs without timestamps
