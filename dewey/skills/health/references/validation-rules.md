# Validation Rules

Complete list of Tier 1 deterministic checks performed by `validators.py` and `cross_validators.py`.

## Per-File Validators (`validators.py`)

### Frontmatter Checks (`check_frontmatter`)

| Field | Required | Expected Value | Severity |
|-------|----------|---------------|----------|
| `sources` | Yes | Non-empty list of URLs | fail |
| `last_validated` | Yes | ISO date (YYYY-MM-DD) | fail |
| `relevance` | Yes | Non-empty string | fail |
| `depth` | Yes | One of: `overview`, `working`, `reference` | fail |

### Section Ordering (`check_section_ordering`)

| Rule | Applies To | Expected | Severity |
|------|-----------|----------|----------|
| "In Practice" before "Key Guidance" | `depth: working` files | Concrete before abstract | warn |

### Section Completeness (`check_section_completeness`)

| Rule | Applies To | Severity |
|------|-----------|----------|
| Required sections present | All depth levels | warn |
| Checks depth-specific required headings | `working`: "Why This Matters", "In Practice", etc. | warn |

### Heading Hierarchy (`check_heading_hierarchy`)

| Rule | Check | Severity |
|------|-------|----------|
| No skipped heading levels | e.g., h1 directly to h3 without h2 | warn |

### Cross-Reference Integrity (`check_cross_references`)

| Rule | Check | Severity |
|------|-------|----------|
| Internal links resolve | `[text](path)` links (non-URL, non-anchor, non-mailto) must point to existing files | warn |

### Size Bounds (`check_size_bounds`)

| Depth | Min Lines | Max Lines | Severity |
|-------|-----------|-----------|----------|
| `overview` | 5 | 150 | warn |
| `working` | 10 | 400 | warn |
| `reference` | 3 | 150 | warn |

### Readability (`check_readability`)

| Depth | FK Grade Min | FK Grade Max | Severity |
|-------|-------------|-------------|----------|
| `overview` | 8 | 14 | warn |
| `working` | 10 | 16 | warn |
| `reference` | -- | -- | skipped |

### Structural Coverage (`check_coverage`)

| Rule | Scope | Severity |
|------|-------|----------|
| Area has overview | Every directory under `docs/` (excluding `_` prefixed) must contain `overview.md` | fail |
| Topic has companion reference | Every `.md` file (excluding `overview.md` and `.ref.md`) must have a matching `.ref.md` | warn |

### Index Sync (`check_index_sync`)

| Rule | Check | Severity |
|------|-------|----------|
| Index references all files | `index.md` entries match topic files on disk | warn |
| No stale index entries | Index doesn't reference deleted files | warn |

### Inventory Regression (`check_inventory_regression`)

| Rule | Check | Severity |
|------|-------|----------|
| No topics disappeared | Current file list compared against previous run | warn |

### Source URL Format (`check_source_urls`)

| Rule | Check | Severity |
|------|-------|----------|
| Well-formed URLs | Each source must start with `http://` or `https://` | fail |
| Placeholder comments | Lines containing `<!--` are skipped | -- |

### Freshness (`check_freshness`)

| Rule | Threshold | Severity |
|------|-----------|----------|
| Content age | `last_validated` must be within 90 days of today | warn |
| Invalid date | `last_validated` must parse as ISO date | warn |

### Go Deeper Links (`check_go_deeper_links`)

| Rule | Applies To | Severity |
|------|-----------|----------|
| Working files link to reference companion | `depth: working` files with a `.ref.md` companion | warn |

### Reference See Also (`check_ref_see_also`)

| Rule | Applies To | Severity |
|------|-----------|----------|
| Reference files include "See Also" linking back | `depth: reference` files (`.ref.md`) | warn |

### Placeholder Comments (`check_placeholder_comments`)

| Rule | Check | Severity |
|------|-------|----------|
| No TODO/FIXME markers | Flags `TODO`, `FIXME`, `PLACEHOLDER`, `TBD`, `CHANGEME` in content | warn |
| No placeholder source URLs | Source URLs containing `example.com` or `placeholder` | warn |

### Source Diversity (`check_source_diversity`)

| Rule | Check | Severity |
|------|-------|----------|
| Multiple source domains | Warns when all sources come from a single domain (requires 2+ sources) | warn |
| Domain normalization | Strips `www.` prefix for comparison | -- |

### Citation Grounding (`check_citation_grounding`)

| Rule | Applies To | Severity |
|------|-----------|----------|
| Inline citations near claims | `depth: working` files should have source URLs cited in body text, not just frontmatter | warn |
| Cap at 5 warnings | At most 5 ungrounded-source warnings per file | -- |

### Source Accessibility (`check_source_accessibility`)

| Rule | Check | Severity |
|------|-------|----------|
| Source URLs reachable | HTTP HEAD (fallback to GET) returns 200 | warn |
| Opt-in only | Only runs when `--check-links` flag is passed | -- |
| Timeout | Default 10 seconds per URL | -- |

## Cross-File Validators (`cross_validators.py`)

### Manifest Sync (`check_manifest_sync`)

| Rule | Check | Severity |
|------|-------|----------|
| AGENTS.md matches disk | Topics listed in AGENTS.md manifest exist as files | warn |
| No unlisted files | Files on disk appear in the manifest | warn |

### Curation Plan Sync (`check_curation_plan_sync`)

| Rule | Check | Severity |
|------|-------|----------|
| Checkmarks match files | Checked items in `.dewey/curation-plan.md` have corresponding files | warn |
| Unchecked items flagged | Existing files not yet checked off in the plan | warn |

### Proposal Integrity (`check_proposal_integrity`)

| Rule | Check | Severity |
|------|-------|----------|
| Required frontmatter | Proposals in `_proposals/` have required metadata | fail |
| Valid target area | Target area directory exists | warn |

### Link Graph (`check_link_graph`)

| Rule | Check | Severity |
|------|-------|----------|
| Internal links resolve | All markdown links between knowledge files point to existing files | warn |

### Duplicate Content (`check_duplicate_content`)

| Rule | Check | Severity |
|------|-------|----------|
| No exact duplicate paragraphs | Paragraph-level hash comparison across files | warn |
| Low Jaccard similarity | 5-word shingle similarity below threshold | warn |
| Companion pairs excluded | `.md` / `.ref.md` pairs are not compared against each other | -- |

### Naming Conventions (`check_naming_conventions`)

| Rule | Check | Severity |
|------|-------|----------|
| Directory names are slugified | Lowercase, hyphens, no special characters | warn |
| File names are slugified | Lowercase, hyphens, `.md` / `.ref.md` extensions | warn |

## Auto-Fix Functions (`auto_fix.py`)

| Function | Fixes | Triggered By |
|----------|-------|-------------|
| `fix_missing_sections` | Adds missing required sections with placeholder content | `check_section_completeness` |
| `fix_missing_cross_links` | Adds "Go Deeper" / "See Also" links between companion files | `check_go_deeper_links`, `check_ref_see_also` |
| `fix_curation_plan_checkmarks` | Updates curation plan checkmarks to match files on disk | `check_curation_plan_sync` |

## Severity Definitions

| Severity | Meaning | CI Behavior |
|----------|---------|-------------|
| **fail** | Structural violation that must be fixed | Fails the health check |
| **warn** | Quality concern that should be addressed | Passes but reported |

## Issue Format

Every validator returns issues as:

```json
{
  "file": "<absolute path to file>",
  "message": "<human-readable description>",
  "severity": "fail | warn"
}
```
