# Knowledge Base Specification Design

**Date:** 2026-02-14
**Status:** Approved
**Approach:** Knowledge Base as a Standard (Approach A)

## Problem Statement

AI agents produce better, more domain-appropriate outputs when they have access to curated, relevant knowledge. But the knowledge base serves two consumers, not one: the **agent** (who needs structured, token-efficient context) and the **human** (who needs readable, navigable content to build their own understanding). This is the dual mandate:

1. **Better agentic outputs** -- agents produce higher quality, more domain-appropriate work
2. **More informed humans** -- the human learns alongside the agent, making better-informed decisions

The problem is the curation, validation, maintenance, and organization of these knowledge bases. Today there is no standard for what a well-formed, role-specific knowledge base looks like -- one that works across providers, serves both audiences, and can be systematically maintained.

## Design Decision

Define a **specification** -- a convention for how knowledge bases are structured, organized, and described -- and build Dewey skills to help create and maintain conformant knowledge bases. The real product is the format and principles, not the tooling. The spec is provider-agnostic. Dewey skills operate on the spec but the output works with any agent (Claude Code, Codex, Gemini CLI, Cursor, etc.).

## Foundational Principles

Twelve principles grounded in agent context research (Anthropic, OpenAI) and cognitive science (Sweller, Vygotsky, Paivio, Bjork, Pirolli, Kalyuga, Dunlosky).

### From Agent Context Research

1. **Source Primacy** -- The knowledge base is a curated guide, not a replacement for primary sources. Every entry either is a primary source reference or points to one. Entries distill, contextualize, and organize. When an agent or human needs to go deeper, the path is always clear.

2. **Dual Audience** -- Every entry serves two consumers: the agent (structured, token-efficient context) and the human (readable, navigable, learnable content). When these needs conflict, favor human readability -- agents are more adaptable readers.

3. **Three-Dimensional Quality** -- Content quality is measured across three dimensions simultaneously:
   - **Relevance** -- Does this help someone in this role accomplish their actual responsibilities?
   - **Accuracy & Freshness** -- Is the content current? Do the sources still say what we claim?
   - **Structural Fitness** -- Right granularity, clear organization, consumable by both audiences?

4. **Collaborative Curation** -- Either the human or an agent can propose additions, but all content passes through validation. The human brings domain judgment. The agent brings systematic coverage. Neither is sufficient alone.

5. **Provenance & Traceability** -- Every piece of knowledge carries metadata about where it came from, when it was last validated, and why it's in the knowledge base. Enables freshness checks, builds trust, supports learning.

6. **Domain-Shaped Organization** -- Organized around the domain's natural structure, not file types or technical categories. The taxonomy should feel intuitive to a practitioner.

7. **Right-Sized Scope** -- Contains what's needed to be effective in the role, and no more. The curation act is as much about what you exclude as what you include.

8. **Empirical Feedback** -- Observable signals about knowledge-base health: coverage gaps, stale entries, unused content. Proxy metrics inform curation decisions and make the maintenance burden visible.

9. **Progressive Disclosure** -- Layered access so agents can discover what's available without loading everything. Metadata (Level 1) -> summaries (Level 2) -> full content (Level 3) -> deep references (Level 4).

### From Cognitive Science Research

10. **Explain the Why** -- Causal explanations produce significantly better comprehension and retention than stating facts alone (Dunlosky et al., 2013). Every entry explains not just what to do, but why. Design decisions, trade-off reasoning, and context for when advice applies and when it doesn't.

11. **Concrete Before Abstract** -- Concrete concepts with visual representations create two memory traces; abstract concepts create one (Paivio, 1986). Learners progress from concrete to abstract (Bruner, 1960). Lead with examples and visuals, then build toward the abstraction.

12. **Multiple Representations** -- Material that helps novices actively hinders experts, and vice versa (Kalyuga et al., 2003). Important concepts should exist at multiple levels of depth (overview, explanation, reference) and appear across the knowledge base. Label each level clearly so readers self-select.

### Research Sources

**Agent Context Engineering:**
- [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [Anthropic: Extend Claude with Skills](https://code.claude.com/docs/en/skills)
- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)
- [OpenAI: AGENTS.md Guide](https://developers.openai.com/codex/guides/agents-md/)
- [OpenAI: Agent Skills](https://developers.openai.com/codex/skills)
- [OpenAI: A Practical Guide to Building Agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)

**Cognitive Science:**
- Sweller (1988) -- Cognitive Load Theory
- Vygotsky (1978) -- Zone of Proximal Development / Scaffolding
- Paivio (1986) -- Dual Coding Theory
- Dunlosky et al. (2013) -- Elaborative Interrogation
- Bjork & Bjork (2011) -- Desirable Difficulties
- Pirolli & Card (1999) -- Information Foraging Theory
- Kalyuga et al. (2003) -- Expertise Reversal Effect

## Directory Structure

```
project-root/
├── AGENTS.md                       # Persona + manifest
├── knowledge/
│   ├── index.md                    # Human TOC + knowledge-base health summary
│   ├── <domain-area>/
│   │   ├── overview.md             # Orientation: what, why, how it connects
│   │   ├── <topic>.md              # Working knowledge with inline sources
│   │   └── <topic>.ref.md          # Expert reference: terse, scannable
│   └── _proposals/                 # Staged additions pending validation
│       └── <proposed-topic>.md
└── .dewey/
    ├── health/                     # Quality scores per entry
    ├── history/                    # Change log, baselines
    └── utilization/                # Reference tracking
```

**Key rules:**
- **AGENTS.md** stays under 100 lines. Defines role persona, behavioral expectations, and a manifest of knowledge/ contents (names and one-line descriptions only). This is progressive disclosure Level 1.
- **Domain areas** are named for how a practitioner thinks about their work (e.g., `campaign-management/`, `measurement/`, `platform-apis/`), not technical categories.
- **Three content depths per topic**: overview (orientation), working document (for doing), reference (quick lookup). Not every topic needs all three.
- **Every .md file** includes frontmatter with source URLs, last-validated date, relevance statement, and depth level.
- **Two entry points**: AGENTS.md for agents, index.md for humans.
- **`_proposals/`** is the staging area for collaborative curation. Either party drops proposed additions here; validation promotes them into the knowledge base.
- **`.dewey/`** holds tooling metadata invisible to knowledge-base consumers.

## Content Format

### Frontmatter (all knowledge files)

```yaml
---
sources:
  - url: https://example.com/primary-source
    title: "Source Title"
last_validated: 2026-02-10
relevance: "One line: who does this help and when"
depth: working  # overview | working | reference
---
```

- **sources** -- Primary sources this content is derived from. Enforces source primacy.
- **last_validated** -- When someone last checked sources still say what we claim. Enables freshness checks.
- **relevance** -- Strong information scent for agents scanning the manifest and humans scanning the index.
- **depth** -- Where this sits in the progressive disclosure chain.

### `<topic>.md` -- Working Knowledge

The core content type. Template enforces concrete-before-abstract and explain-the-why.

```markdown
---
sources:
  - url: ...
    title: ...
last_validated: 2026-02-10
relevance: "..."
depth: working
---

# Topic Name

## Why This Matters

Brief context: what problem does this solve, when does a practitioner
encounter it, and why the approach described here is preferred over
alternatives. Causal reasoning, not just a statement of fact.

## In Practice

A concrete, worked example showing the concept applied to a realistic
scenario. Code snippets, specific numbers, real tool output.

> **Source:** [Title](url) -- section or page that informed this example

## Key Guidance

Actionable recommendations. Each explains not just what to do, but
why it works and when it applies. Inline source references.

- **Do X because Y** -- context for when this applies
  ([Source](url), section name)
- **Prefer A over B when C** -- reasoning for the trade-off
  ([Source](url))

## Watch Out For

Common mistakes, edge cases, things that change frequently.
Highest staleness risk -- freshness matters most here.

## Go Deeper

- [Topic Reference](topic.ref.md) -- quick-lookup version
- [Source Title](url) -- primary source for full treatment
- [Related Topic](../other-area/related.md) -- cross-reference
```

**Principle mapping:**
- "Why This Matters" -> Principle 10 (Explain the Why)
- "In Practice" -> Principle 11 (Concrete Before Abstract)
- Inline `[Source](url)` -> Principle 1 (Source Primacy)
- "Go Deeper" -> Principle 12 (Multiple Representations) + Principle 9 (Progressive Disclosure)
- Frontmatter -> Principle 5 (Provenance & Traceability)

### `<topic>.ref.md` -- Expert Reference

Terse, scannable, no explanations. Exists because of the expertise reversal effect.

```markdown
---
sources:
  - url: ...
    title: ...
last_validated: 2026-02-10
relevance: "..."
depth: reference
---

# Topic Name -- Reference

| Parameter | Value | Notes |
|-----------|-------|-------|
| ...       | ...   | ...   |

**Quick rules:**
- Rule 1
- Rule 2
- Rule 3

**See also:** [Full treatment](topic.md) | [Primary source](url)
```

### `overview.md` -- Domain Area Orientation

One per domain area. Answers: what is this area, why does it matter, what's in here?

```markdown
---
sources:
  - url: ...
    title: ...
last_validated: 2026-02-10
relevance: "..."
depth: overview
---

# Domain Area Name

## What This Covers

2-3 sentences: what this domain area is about and why it's part of
the knowledge base. Connects to the role defined in AGENTS.md.

## How It's Organized

- [Topic A](topic-a.md) -- one-line description
- [Topic B](topic-b.md) -- one-line description

## Key Sources

The 3-5 most important primary sources for this entire domain area.

- [Source Title](url) -- why it's authoritative
```

### `AGENTS.md` -- Persona + Manifest

```markdown
# Role: [Role Name]

## Who You Are

Brief persona definition: the role, its responsibilities, and the
behavioral expectations for an agent operating in this context.

## What You Have Access To

Knowledge base manifest -- one line per topic, grouped by domain area.
Progressive disclosure Level 1: names and descriptions only.

### Domain Area A
- **Topic 1** -- one-line description
- **Topic 2** -- one-line description

## How To Use This Knowledge

Instructions for how the agent should reference the knowledge base:
when to load content, how to cite sources, when to defer to primary
sources rather than summarizing.
```

### `_proposals/` -- Draft Content

Same content template with additional frontmatter:

```yaml
---
status: proposal
proposed_by: human  # or agent
rationale: "Gap identified in coverage of X"
sources:
  - url: ...
    title: ...
---
```

Either party drops a file here. Validation promotes it into the knowledge base or rejects it.

## Quality Validation

Three dimensions, three tiers of automation.

### Tier 1: Fully Deterministic (Python, no LLM)

Structural, mechanical checks. Pass/fail, no ambiguity. Run on every change like a linter.

**Freshness:**
- `last_validated` older than threshold (configurable per domain area)
- `last_validated` field exists and is a valid date

**Source Availability:**
- Source URLs return HTTP 200
- Source URLs are well-formed

**Template Conformance:**
- Required frontmatter fields present (`sources`, `last_validated`, `relevance`, `depth`)
- Required sections present per file type (e.g., `topic.md` must have `## Why This Matters`, `## In Practice`, `## Key Guidance`)
- `depth` is a valid enum value

**Section Ordering:**
- "In Practice" appears before "Key Guidance" in working-knowledge files (enforces concrete-before-abstract)

**Cross-References:**
- Every `topic.md` links to its `topic.ref.md` and vice versa
- "Go Deeper" section exists with at least one internal and one external link
- All internal links resolve to existing files

**Size Bounds:**
- File line count within expected range per depth level
- AGENTS.md under 100 lines

**Coverage Inventory:**
- Every domain area has an `overview.md`
- Every `topic.md` has a corresponding `topic.ref.md`
- Every entry in AGENTS.md manifest points to an existing file

**Proposal Hygiene:**
- Proposals have `status: proposal` and `proposed_by` in frontmatter
- Proposals follow the standard content template

### Tier 2: LLM-Assisted (deterministic trigger, LLM evaluation)

Triggered by deterministic conditions, evaluated by LLM. Produces structured assessment for human review.

**Source Drift:**
- *Trigger:* `last_validated` past threshold or source content hash changed
- *LLM task:* Compare knowledge-base claims against current source content. Output structured diff: `[{claim, status: still_accurate|changed|removed, evidence}]`

**Depth Label Accuracy:**
- *Trigger:* Word count / prose ratio outside expected range for depth label
- *LLM task:* Assess actual depth level. Recommend label with reasoning.

**Source Primacy Check:**
- *Trigger:* Fewer than 1 inline source reference per 3 recommendations in a section
- *LLM task:* Identify unsourced claims that should cite a source.

**"Why" Quality:**
- *Trigger:* "Why This Matters" section exists but falls below word count minimum
- *LLM task:* Assess whether section explains *why* (causal reasoning) or just restates *what*.

**Concrete Example Quality:**
- *Trigger:* "In Practice" section exists with code block/table/numeric example
- *LLM task:* Assess whether example is concrete and realistic or a generic placeholder.

### Tier 3: Human Judgment (LLM surfaces, human decides)

Fundamentally editorial decisions where LLM gathers evidence and frames the question.

**Relevance to Role:**
- LLM surfaces alignment assessment between entry and AGENTS.md responsibilities.
- Human decides whether content belongs.

**Scope Decisions:**
- LLM surfaces lowest-relevance, lowest-utilization entries.
- Human decides whether to prune.

**Proposal Acceptance:**
- LLM validates structure and assesses quality.
- Human decides whether to promote into knowledge base.

**Conflict Resolution:**
- LLM surfaces specific changes between knowledge-base claims and updated sources.
- Human decides how to reconcile.

### Validation Summary

| Tier | Checks | Cost | Speed | Confidence |
|------|--------|------|-------|------------|
| Deterministic | ~12 | Zero (Python) | Seconds | Pass/fail, no ambiguity |
| LLM-Assisted | ~5 | Token cost per flagged entry | Minutes | Structured assessment, human confirms |
| Human Judgment | ~4 | Human time | Async | Editorial, not automatable |

### Feedback Loop

```
Validate -> Score -> Surface -> Decide -> Act

Validate:  Run checks across all three dimensions
Score:     Each entry gets a health score (per dimension + composite)
Surface:   Present findings in index.md health summary + .dewey/health/
Decide:    Human reviews flagged items, prioritizes what to fix
Act:       Update stale content, promote proposals, prune irrelevant entries
```

Utilization tracking adds a fourth signal over time: content that scores well on quality but never gets loaded may indicate a gap between what we think is useful and what actually gets used. Doesn't automatically mean removal -- could be valuable for human learning -- but prompts a question.

## What This Design Does Not Cover

- **Direct measurement of the dual mandate.** Better agent outputs and more informed humans are outcomes we optimize toward, but measuring them requires observing human-agent collaboration over time. The quality dimensions are research-grounded proxy metrics.
- **Implementation details.** Which Dewey skills to build, in what order, with what interfaces. That belongs in the implementation plan.
- **Knowledge-base content for any specific role.** The spec defines what a well-formed knowledge base looks like. Populating it for a specific role (paid media analyst, platform engineer, data scientist) is a separate activity.
