---
description: Intelligently split large files using LLM analysis to maintain semantic coherence
allowed-tools: Read, Write, Bash(cat *, wc *, mkdir *, cp *)
---

# Split Large Files

Intelligently split large context files (>500 lines) into a scannable main file and topically organized reference files, following Anthropic's best practices for context organization.

## How to Use

```
/dewey:split file.md
/dewey:split file.md --dry-run
```

## What It Does

This command uses the current Claude Code session to:

1. **Analyze** the file content semantically
2. **Identify** essential vs detailed information
3. **Organize** content into topics
4. **Create** a main file (~150 lines) with overview and navigation
5. **Generate** reference files in `references/[filename]/` directory
6. **Maintain** all information with clear bidirectional links
7. **Backup** the original file to `.dewey/backups/`

## Arguments

The command accepts a file path and optional flags:

- `file.md` - Path to the file to split
- `--dry-run` - Preview what would be created without writing files
- `--max-lines N` - Custom threshold (default: 500)
- `--target-lines N` - Target main file size (default: 150)

**Note**: `$ARGUMENTS` in this command will be the file path and any flags provided.

## What You Get

### Before
```
File: IMPLEMENTATION_PLAN.md
Lines: 973
Structure: Single monolithic file
```

### After
```
Main: IMPLEMENTATION_PLAN.md (~200 lines)
  - Project overview
  - Key principles
  - Phase 0 summary
  - Clear navigation to phases

References (3 files):
  - references/IMPLEMENTATION_PLAN/phase-1-measurement.md
  - references/IMPLEMENTATION_PLAN/phase-2-3-optimization.md
  - references/IMPLEMENTATION_PLAN/testing-completion.md

Backup: .dewey/backups/IMPLEMENTATION_PLAN_20260210.md
```

## Implementation Steps

### Step 1: Read the File

First, read the file that needs to be split:

```bash
# Read the file content
cat "$ARGUMENTS"
```

Display basic stats about the file (line count, size, etc.)

### Step 2: Semantic Analysis (You Do This!)

**As Claude, analyze the file content semantically:**

1. **Identify the main topics/sections** - What are the major themes?
2. **Determine what's essential** - What must stay in the main file for quick scanning?
3. **Group related content** - What details belong together in reference files?
4. **Plan the structure** - How should the content be organized?

**Think about:**
- Semantic boundaries (not arbitrary line numbers)
- Logical groupings that make sense together
- Anthropic's context organization best practices
- Keeping the main file scannable (~150 lines)
- Creating topical reference files

### Step 3: Create the Refactoring Plan

Based on your semantic analysis, create a detailed plan:

```json
{
  "main_file": {
    "content": "# Overview\n\nBrief summary...\n\n## Navigation\n- [Topic 1](references/filename/topic-1.md)...",
    "description": "Scannable overview with navigation"
  },
  "reference_files": [
    {
      "path": "references/filename/topic-1.md",
      "content": "# Topic 1\n\nDetailed content...",
      "description": "What this covers"
    }
  ],
  "reasoning": "Why you organized it this way"
}
```

### Step 4: Preview and Confirm

Show the user:
- Main file structure (~how many lines)
- List of reference files that will be created
- What content goes where
- Backup location

Ask for confirmation before proceeding (unless `--dry-run`).

### Step 5: Implement the Split

**Only after user confirmation**, write the files:

1. **Backup original**: Copy to `.dewey/backups/[filename]_[timestamp].md`
2. **Write main file**: Replace original with scannable version
3. **Create references directory**: `references/[filename]/`
4. **Write reference files**: One per topic
5. **Verify**: Check all content preserved

Use the Write tool to create each file based on your analysis.

## Best Practices Applied

- **Scannable main files**: Overview + key concepts + navigation
- **Topical organization**: Related content grouped logically
- **Semantic coherence**: No mid-section cuts
- **Information preservation**: All content retained
- **Clear navigation**: Bidirectional links between files

## Integration

Works seamlessly with:
- `/dewey:analyze` - Identifies files that need splitting
- Other optimization commands (to be implemented)

---

**Process the arguments**: $ARGUMENTS
