---
name: curate
description: Add, update, or manage content in a knowledge base — triggered by command or natural-language curation intent like "save this to my knowledge base"
---

<objective>
Single entry point for all knowledge base operations: discovering domains, scaffolding structure, adding topics, ingesting URLs, managing proposals, and maintaining the curation plan. Replaces the previous explore, init, and curate skills with one unified flow.
</objective>

<quick_start>
Invoke `/dewey:curate` and describe what you want. Examples:

- "add a topic about bid strategies"
- "ingest this URL into the knowledge base"
- "show the curation plan"
- "help me set up a knowledge base"

Also triggers on natural-language curation intent mid-conversation: "save this to my knowledge base", "capture this as a topic", etc.
</quick_start>

<context>
<approach>
1. **Understand intent** -- The user expresses what they want in natural language. Claude classifies and routes.
2. **Assess knowledge-base state** -- Is there a knowledge base? A curation plan? Existing domain areas?
3. **Route to workflow** -- Based on intent + state, route to the right workflow. No menus.
</approach>

<philosophy>
- **Free text first** -- The user says what they want. Claude figures out how.
- **One skill, one entry point** -- No explore/init/curate distinction for the user.
- **Curation plan as prerequisite** -- Created after understanding intent, seeded with the user's goal.
- **New domains inline** -- If a topic doesn't fit, offer to create the area on the spot.
- **Collaborative curation** -- Both humans and agents can propose, review, and add content.
- **Source primacy** -- Every topic should trace back to authoritative sources.
</philosophy>

<variables>
- `$ARGUMENTS` -- Optional free-text context passed to this skill
- `${CLAUDE_PLUGIN_ROOT}` -- Root directory of the Dewey plugin
</variables>
</context>

<intake>
This skill activates on `/dewey:curate` or when the user expresses curation intent in conversation: "add this to the knowledge base", "capture this as a topic", "save this to my knowledge base", "let's put this in the knowledge base", "I want to add a new domain area", or similar phrases.

<gather_intent>
If the user provided clear intent (via arguments, conversational context, or a natural-language trigger), use it directly. Do not re-ask.

If the user invoked `/dewey:curate` with no arguments and no prior conversational context, ask one open-ended question:

> "What would you like to add or change in your knowledge base?"
</gather_intent>

<assess_state>
Check for:
1. Does a knowledge base exist? (Look for AGENTS.md and a knowledge base directory configured in `.dewey/config.json`, defaulting to `docs/`)
2. Does `.dewey/curation-plan.md` exist?
3. What domain areas exist?
</assess_state>

<route>
<no_knowledge_base>
- **Vague or exploratory intent** ("help me set up", "I don't know where to start", no specific topic) -> Route to `workflows/curate-discover.md`
- **Clear intent with goals** ("I want a knowledge base for marketing analytics", "build a knowledge base for my team") -> Route to `workflows/curate-setup.md`
- **Very specific intent** ("add a topic about bid strategies") -> Route to `workflows/curate-setup.md` with a note to resume into the specific curation action after scaffolding
</no_knowledge_base>

<no_curation_plan>
Before routing to any workflow, build the curation plan:

1. Read AGENTS.md to understand the role and domain areas
2. Read the knowledge base directory structure to see what topics exist
3. Tell the user: "Before we proceed, let me build a curation plan so we have a map of what's covered."
4. Propose 2-4 starter topics per domain area. Seed with the user's stated intent as the first item if it maps to a specific topic.
5. Ask the user to confirm or adjust
6. Write `.dewey/curation-plan.md`
7. Then resume routing based on the user's original intent
</no_curation_plan>

<plan_exists>
Classify the user's intent and route:

| Intent | Signal patterns | Routes to |
|--------|----------------|-----------|
| **New topic** | Topic name, "add X", "capture Y", "I learned about Z" -- no URL | `workflows/curate-add.md` |
| **Ingest URL** | Message contains a URL | `workflows/curate-ingest.md` |
| **Propose for review** | "propose", "submit for review", "not sure if this fits" | `workflows/curate-propose.md` |
| **Promote proposal** | "promote", "move proposal", "approve", references _proposals/ | `workflows/curate-promote.md` |
| **Manage plan** | "what's planned", "show the plan", "add to plan", "remove from plan" | `workflows/curate-plan.md` |
| **Update existing** | "update X", "revise", "add to the existing topic about Y" | `workflows/curate-add.md` with mode=update |
| **Add domain area** | "new area", "add a domain", "create an area for X" | `workflows/curate-setup.md` (re-init path for adding areas) |

If intent is ambiguous, ask **one** clarifying question -- not a menu of options.
</plan_exists>

<new_domain_needed>
During classification, if the user's topic doesn't fit any existing domain area:

1. Tell the user: "This doesn't fit your existing areas ([list areas]). Want me to create a new domain area for it?"
2. If yes: route to `workflows/curate-setup.md` (which handles adding areas to an existing knowledge base via its re-init path), then resume into the original curation action
3. If no: ask where they'd like to put it, or whether to skip
</new_domain_needed>
</route>
</intake>

<workflows_index>
All workflows in `workflows/`:

| Workflow | Purpose |
|----------|---------|
| curate-discover.md | Guided conversation to discover role, domains, scaffold knowledge base, and build curation plan |
| curate-setup.md | Evaluate repo, scaffold knowledge-base structure (or add areas to existing knowledge base), build plan |
| curate-add.md | Create a new topic or update an existing one in a domain area |
| curate-propose.md | Submit a topic proposal for review |
| curate-promote.md | Promote a validated proposal into a domain area |
| curate-ingest.md | Ingest an external URL -- evaluate against knowledge base, then propose or update |
| curate-plan.md | View, add to, or remove items from the curation plan |
</workflows_index>

<scripts_integration>
**Curate scripts** in `scripts/`:

**create_topic.py** -- Create topic files in a domain area
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/curate/scripts/create_topic.py --knowledge-base-root <root> --area <area> --topic "<name>" --relevance "<relevance>"
```

**propose.py** -- Create a proposal file
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/curate/scripts/propose.py --knowledge-base-root <root> --topic "<name>" --relevance "<relevance>" --proposed-by "<who>" --rationale "<why>"
```

**promote.py** -- Move a proposal into a domain area
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/curate/scripts/promote.py --knowledge-base-root <root> --proposal "<slug>" --target-area "<area>"
```

**Scaffolding scripts** in `scripts/`:

**scaffold.py** -- Create or extend knowledge-base directory structure
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/curate/scripts/scaffold.py --target <dir> --role "<persona>" --areas "<area1>,<area2>"
```

**config.py** -- Read knowledge base configuration
- `read_knowledge_dir(knowledge_base_root)` returns the configured knowledge directory (default: `docs`)
</scripts_integration>

<success_criteria>
Curation is successful when:

- Content follows the topic template structure
- Sources are referenced in frontmatter and cited inline
- Frontmatter is complete with title, relevance, and date
- Template sections are filled in (Why This Matters, In Practice, Key Guidance, Watch Out For, Go Deeper)
- AGENTS.md has linked table rows for each topic
- overview.md "How It's Organized" has linked table rows for each topic in the area
- overview.md "Key Sources" is populated with actual sources
- dewey-kb.md Domain Areas table lists the area
</success_criteria>
