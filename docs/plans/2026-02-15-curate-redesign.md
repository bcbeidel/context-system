# Design: Curate Skill Redesign — Free-Text Intake + Skill Consolidation

## Problem

The curate skill forces users through a structured menu (add / propose / promote / ingest / plan) before understanding what they want. This creates cognitive overhead and friction. Meanwhile, the best curation moments in practice happen organically — a user researches something, then says "save this to my knowledge base." Three separate skills (explore, init, curate) form a linear pipeline with two handoff seams where context gets lost.

## Solution

Redesign curate as the single entry point for all knowledge base content operations. Replace the action menu with a free-text intent classifier. Absorb explore and init as workflows within curate, triggered automatically based on knowledge-base state.

## Design Decisions

- **Free text first.** The user expresses intent in natural language. Claude classifies and routes.
- **No sub-commands.** Remove `add`/`propose`/`promote`/`ingest`/`plan` as explicit arguments. One way in.
- **Conversational triggers.** The skill matches both `/dewey:curate` and natural-language curation intent mid-conversation ("save this to my knowledge base", "add that to my knowledge base").
- **Curation plan stays a prerequisite.** But it's created after understanding intent, not before. Seeded with the user's stated intent.
- **New domain areas offered inline.** When a topic doesn't fit existing areas, Claude offers to create one on the spot rather than hitting a dead end.
- **Health stays separate.** Different concern (validation vs. content lifecycle), different triggers.

## New Intake Flow

```
User input (free text, URL, /dewey:curate, or conversational cue)
  │
  ├── No knowledge base exists?
  │     ├── Vague intent ("help me set up") ──→ curate-discover.md
  │     ├── Clear intent ("knowledge base for marketing") ──→ curate-setup.md
  │     └── Very specific ("add topic X") ────→ curate-setup.md, then curate-add.md
  │
  └── Knowledge base exists?
        ├── No plan? ──→ Build plan (seeded with intent), then route
        └── Plan exists? ──→ Classify intent, then route
```

### Intent Classification

When the knowledge base exists and plan exists, Claude classifies free-text intent:

| Intent | Signal patterns | Routes to |
|--------|----------------|-----------|
| New topic | "add X", "capture Y", topic name without URL | curate-add.md |
| Ingest URL | message contains a URL | curate-ingest.md |
| Promote proposal | "promote", "move proposal", "approve" | curate-promote.md |
| Manage plan | "what's planned", "add to plan", "remove from plan" | curate-plan.md |
| Update existing | "update X", "revise", "add to existing topic" | curate-add.md (update path) |

If intent is ambiguous, Claude asks one clarifying question — not a menu.

### Conversational Trigger

The skill activates on `/dewey:curate` or when the user expresses curation intent in conversation: "add this to the knowledge base", "capture this as a topic", "save this to my knowledge base", "let's put this in the knowledge base", or similar phrases.

When triggered conversationally, the skill skips the "what would you like to add or change?" prompt — the user already said what they want. Claude classifies intent from the conversation context and routes directly.

## Skill Consolidation

### What moves

| From | To | Notes |
|------|----|-------|
| `explore/workflows/explore-discovery.md` | `curate/workflows/curate-discover.md` | Calls scaffold.py directly instead of handing off to /dewey:init |
| `init/workflows/init.md` | `curate/workflows/curate-setup.md` | Continues into the user's actual intent instead of ending with "now use /dewey:curate" |
| `explore/SKILL.md` | deleted | |
| `init/SKILL.md` | deleted | |

### What stays in place

| File | Why |
|------|-----|
| `init/scripts/scaffold.py` | Shared infrastructure — curate-setup and curate-discover call it by path |
| `init/scripts/templates.py` | Used by scaffold.py |
| `init/scripts/config.py` | Used by health and curate scripts |
| `init/references/knowledge-base-spec-summary.md` | Loaded as required reading by curate-setup and curate-discover |

### What the user sees

Before: three skills (`/dewey:explore`, `/dewey:init`, `/dewey:curate`) with handoff instructions between them.

After: one skill (`/dewey:curate` or natural language). The intake handles everything from "I have no knowledge base and don't know where to start" through "promote this proposal."

## Workflow Changes

### curate-add.md

- Remove argument parsing that expects `/dewey:curate add <topic>` syntax. Topic name and area arrive from the intake classifier.
- Add "update existing topic" path: when intent is "update existing," read the existing topic, present what's there, ask what should change, apply edits. The research/draft/approve/write-indexes flow is the same.

### curate-ingest.md

- Remove argument parsing that expects `/dewey:curate ingest <url>`. URL arrives from intake.

### curate-propose.md

- Remove argument parsing. Topic name and rationale arrive from intake.

### curate-promote.md

- No changes. Already starts by listing proposals and asking the user to pick.

### curate-plan.md

- No changes. View/add/remove sub-actions are internal to this workflow.

### curate-discover.md (new, from explore)

- Identical guided conversation (problems → tasks → domains → role framing).
- Instead of handing off to /dewey:init, calls scaffold.py directly.
- After scaffolding, continues into plan-building step, then resumes whatever the user wanted.

### curate-setup.md (new, from init)

- Identical scaffold flow (evaluate repo → ask goals → propose domains → scaffold).
- Instead of ending with "now use /dewey:curate add", continues into the user's actual intent.

## Plan Gate Timing

1. User expresses intent
2. Claude checks if the knowledge base exists (hard stop if not — routes to discover or setup)
3. Claude classifies intent
4. Before routing to the workflow, Claude checks for the curation plan:
   - **Plan exists** — consult it silently (is this topic planned? in scope?) and route
   - **No plan** — "Before we add this, let me build a quick curation plan." Build it seeded with the user's stated intent as the first item, then resume routing

## New Domain Area Handling

1. During intent classification, Claude maps intent against existing domain areas
2. If no area fits: "This doesn't fit your existing areas. Want me to create a new domain area for it?"
3. If yes: run scaffold logic to create the area directory, overview.md, register in AGENTS.md/CLAUDE.md, then resume the curate workflow with the new area
4. If no: ask where to put it or whether to skip

## Plugin Manifest Impact

The plugin manifest (`dewey/.claude-plugin/plugin.json`) registers skills. After consolidation:
- Remove `explore` and `init` skill entries
- Keep `curate` and `health` entries
- Update `curate` description to reflect broader scope

## Files Changed Summary

| Action | File |
|--------|------|
| Rewrite | `curate/SKILL.md` — new intake with free-text classifier, conversational triggers, consolidated routing |
| Modify | `curate/workflows/curate-add.md` — strip arg parsing, add update-existing path |
| Modify | `curate/workflows/curate-ingest.md` — strip arg parsing |
| Modify | `curate/workflows/curate-propose.md` — strip arg parsing |
| Create | `curate/workflows/curate-discover.md` — from explore-discovery.md, direct scaffold call |
| Create | `curate/workflows/curate-setup.md` — from init.md, continues into user intent |
| Delete | `explore/SKILL.md` |
| Delete | `explore/workflows/explore-discovery.md` |
| Delete | `init/SKILL.md` |
| Delete | `init/workflows/init.md` |
| Modify | `dewey/.claude-plugin/plugin.json` — remove explore and init skills |
