# Session Tracking Guide

Session tracking is part of Dewey's **mid-term memory tier** - a staging area for learnings before they're promoted to permanent context.

## Why Track Sessions?

- **Capture learnings in real-time** instead of losing insights
- **Measure context effectiveness** (which files were actually useful?)
- **Guide promotion decisions** (what deserves permanent storage?)
- **Prevent premature promotion** (wait for validation before committing)

## Three-Tier Memory Architecture

```
┌─────────────────────────────────────────────────┐
│ SHORT-TERM (Working Memory)                     │
│ • Current session, in-context                   │
│ • Ephemeral, discarded after session            │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ MID-TERM (Episodic Memory) ← YOU ARE HERE       │
│ • Session files (7 day retention)               │
│ • Staged learnings awaiting promotion           │
│ • Weekly review process                         │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ LONG-TERM (Semantic Memory)                     │
│ • Permanent context/ files                      │
│ • Validated, high-value knowledge               │
│ • Indexed and searchable                        │
└─────────────────────────────────────────────────┘
```

## Quick Start

### 1. Create Session File

```bash
# Copy the template
cp templates/.claude/sessions/template.md .claude/sessions/2026-02-10-my-task.md

# Or use the Dewey CLI (when implemented)
dewey session start "Understanding authentication"
```

### 2. Fill Out During Session

As you work, update the session file:

- **Goal**: What you're trying to accomplish
- **Context Loaded**: Which files you're using
- **Questions Asked**: What you're exploring
- **Outcomes**: What you actually accomplished
- **Learnings**: Key insights and patterns

### 3. End Session

```bash
# Mark session complete
dewey session end

# Or manually save the file
```

### 4. Weekly Review

Every week, review your session files:

```bash
# List sessions from the past week
ls -lt .claude/sessions/*.md | head -7

# Run promotion analysis
dewey session review
```

## Session Template Sections

### Goal (Required)
What you're trying to accomplish. Keep it specific and measurable.

**Good**: "Implement user profile editing with validation"
**Bad**: "Work on user stuff"

### Context Loaded (Required)
List files you loaded and WHY. This helps measure context effectiveness.

```markdown
- `context/auth/jwt-guide.md` - Needed JWT token format
- `src/auth/middleware.py` - Checking existing auth logic
- `context/patterns/validation.md` - Learning validation patterns
```

### Questions Asked (Optional)
Track what you explored. Helps identify patterns in what you need to learn.

### Outcomes (Required)
What actually happened. Use status markers:
- ✅ Completed
- ⚠️  Partially done
- ❌ Failed attempt (still valuable to record!)

### Learnings (Required - Most Important!)
This is the gold. Capture:

- **What Worked**: Patterns to repeat
- **What Didn't Work**: Mistakes to avoid
- **Open Questions**: For future investigation

### Next Steps (Optional)
Planning ahead helps the next session start faster.

### Promotion Candidates (Optional)
Mark insights that might deserve permanent context:

```markdown
- [ ] [Insight] - Needs validation (seen 1x)
- [ ] [Pattern] - Seems important (seen 2-3x)
- [x] [Fact] - Ready to promote (seen 5+x, validated)
```

## Promotion Rules (Automated)

Dewey automatically suggests promotions based on:

| Criteria | Threshold | Action |
|----------|-----------|--------|
| Age >7 days + references ≥3 | Auto-suggest | Promote |
| Referenced ≥5 times | Any age | Promote |
| Explicitly validated | User marked | Promote |
| Solves recurring problem | 3+ occurrences | Promote |
| Score <0.3 | Any | Discard |
| Score 0.3-0.6 | Any | Keep in mid-term |

**Score calculation**:
```
Score = (0.4 × reference_count / 5) +
        (0.3 × validation_score) +
        (0.3 × recency_score)
```

## Best Practices

### DO
✅ Fill out sessions in real-time (not after)
✅ Be specific about what worked/didn't work
✅ Mark files that were actually used vs. just loaded
✅ Review sessions weekly
✅ Wait for validation before promoting

### DON'T
❌ Skip sessions because "it was just research"
❌ Promote on first sighting (premature optimization)
❌ Copy entire session logs to permanent context
❌ Let sessions accumulate beyond 7 days without review

## Manual vs. Automated

**Current (Manual)**:
- Copy template, fill sections, save file
- Review weekly by hand
- Manually promote learnings to context/

**Future (Automated)**:
- `dewey session start` creates file
- `dewey session end` captures metadata
- `dewey session review` suggests promotions
- `dewey session promote` moves to context/

## Integration with CI/CD

When Dewey's CI/CD Loop 2 is implemented, it will:

1. Analyze your sessions weekly
2. Calculate promotion scores
3. Generate a PR with suggestions:
   - "Session X mentioned pattern Y 5 times - promote to context/patterns/"
   - "Session Z has score 0.2 - archive"
4. You review and merge (or close) the PR

## Examples

See `example-session.md` for a complete filled-out example.

## File Organization

```
.claude/sessions/
├── README.md                    # This file
├── template.md                  # Copy this for new sessions
├── example-session.md           # Example of filled template
├── 2026-02-10-ralph-loop.md    # Actual session files
├── 2026-02-11-token-counter.md
└── archive/                     # Sessions >7 days old
    └── 2026-01/
        └── old-session.md
```

## Metrics to Track

When session management is automated, track:

- **Sessions per week**: Measure activity
- **Average citation rate**: Context effectiveness
- **Promotion rate**: % of learnings that stick
- **Time to promotion**: How long to validate
- **Review compliance**: Are you doing weekly reviews?

## Next Steps

1. Start using the template today
2. Review sessions weekly (Friday afternoons work well)
3. Promote validated learnings manually
4. Wait for automated session management (Task 2.6-2.7)

---

*Part of Dewey's mid-term memory tier implementation (spec-3-memory-tier.md)*
