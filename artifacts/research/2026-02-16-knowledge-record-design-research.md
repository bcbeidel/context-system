# Deep Dive: Knowledge Record Design -- Documentation Standards, Agentic Systems, and Content Schemas

## Strategic Summary

No existing standard fully addresses the needs of LLM-consumed curated knowledge. DITA provides the most rigorous topic typing and metadata model but uses XML (80% more tokens than Markdown). Diataxis provides the best content-type taxonomy but its four quadrants reduce to three for agents (tutorials are irrelevant). The agentic ecosystem has converged on Markdown + YAML frontmatter with glob-based scoping and 2-3 tier progressive disclosure -- exactly Dewey's current approach. The gap is in the record-level specification: no system prescribes optimal section ordering, token budgets, or position-aware organization for LLM attention patterns.

## Research Sources

This document synthesizes findings from four parallel research agents covering:
1. Agentic knowledge systems (Cursor, Claude Code, MCP, Windsurf, Copilot, Aider, LangChain/LlamaIndex)
2. Knowledge record schemas (llms.txt, CLAUDE.md spec, frontmatter practices, metadata standards)
3. Documentation standards (Diataxis, DITA, EPPO, Information Mapping, Zettelkasten, S1000D)
4. Atomic content & topic specs (DITA topic types, SKOS, OWL, Wikidata, Wikipedia structure, quality frameworks)

---

## Part 1: How Agentic Systems Structure Knowledge

### Convergent Patterns Across All Systems

Every major agentic coding tool was surveyed. The patterns that emerged independently across all of them:

| Pattern | Cursor | Claude Code | MCP | Windsurf | Copilot | Agent Skills |
|---------|--------|-------------|-----|----------|---------|-------------|
| Markdown content | `.mdc` | `.md` | JSON-RPC | `.md` | `.md` | `.md` |
| YAML frontmatter | Yes | Yes (rules) | N/A | No | Yes | Yes |
| Glob-based scoping | `globs:` | `paths:` | N/A | Glob mode | `applyTo:` | Directory |
| Progressive disclosure | Description field | Subtree loading | list-then-read | Manual/Model | N/A | 3-tier explicit |
| Size guidance | ~20 rules = 2K tokens | <200 lines | N/A | 6K chars/file | Brief | <500 lines |

### Agent Skills Specification (Most Formal)

The Agent Skills spec (agentskills.io) provides the most explicit progressive disclosure model:

- **Tier 1 (~100 tokens)**: `name` + `description` loaded at startup for all skills
- **Tier 2 (<5,000 tokens)**: Full SKILL.md body loaded on activation
- **Tier 3 (unbounded)**: `scripts/`, `references/`, `assets/` loaded on demand

### MCP Resource Schema

MCP defines the richest metadata for progressive disclosure:

```json
{
  "uri": "file:///path",
  "name": "Resource Name",
  "description": "What this contains",
  "mimeType": "text/markdown",
  "annotations": {
    "audience": ["assistant"],
    "priority": 0.8,
    "lastModified": "2025-01-12T15:00:58Z"
  }
}
```

The `priority` field (0.0-1.0) is unique -- it enables clients to decide which resources to load into context based on importance ranking.

### LlamaIndex's Dual-Visibility Pattern

LlamaIndex's `TextNode` has `excluded_embed_metadata_keys` and `excluded_llm_metadata_keys` -- allowing **different metadata visibility for different consumers**. Embeddings can see file paths and categories (for retrieval), while the LLM sees only content-relevant metadata (for generation). This is progressive disclosure at the metadata level.

### Key Insight: Format Doesn't Matter for Frontier Models

McMillan (arXiv:2602.05447) tested 9,649 experiments across 11 models and 4 formats. **Format does not significantly affect aggregate accuracy** (chi-squared=2.45, p=0.484). Model capability is the dominant factor -- 21pp gap between frontier and open-source models dwarfs any format effect. But YAML is most token-efficient, and Markdown has the best human readability.

---

## Part 2: Documentation Standards and Paradigms

### Diataxis: Content Type Taxonomy

Diataxis organizes documentation along two axes into four quadrants:

| | Acquisition (Study) | Application (Work) |
|---|---|---|
| **Action (Practical)** | Tutorial (learning) | How-to Guide (goal) |
| **Cognition (Theoretical)** | Explanation (understanding) | Reference (information) |

**For agent consumption, tutorials are irrelevant** -- agents don't learn by doing. This reduces to three relevant types:
- **How-to / Procedural** → Dewey's `working` depth
- **Reference** → Dewey's `reference` depth
- **Explanation** → Dewey's `overview` depth

Diataxis criticism: Too rigid. Content often blends types. The "compass not a map" framing helps but practitioners still struggle with edge cases.

### EPPO: Domain-Shaped Topic Types

Mark Baker's Every Page is Page One defines seven topic characteristics:
1. **Self-contained** -- makes sense without surrounding context
2. **Specific purpose** -- answers one question
3. **Conforms to a domain-specific type** -- NOT generic concept/task/reference
4. **Establishes context** -- orients the reader within the domain
5. **Assumes qualified reader** -- doesn't teach prerequisites
6. **Stays on one level** -- doesn't mix beginner and expert content
7. **Links richly** -- connections to related topics are first-class

**Key EPPO insight for Dewey**: Topic types should emerge from the domain, not be imposed by a framework. Dewey's three depths (overview/working/reference) are structural types, not domain types -- this is correct because they serve progressive disclosure, not domain modeling.

### DITA: Formal Topic Type Specification

DITA defines the most rigorous topic model:

**Base topic** (all types inherit): Only `@id` and `<title>` are truly required. Optional: `<shortdesc>`, `<prolog>` (metadata), `<body>`, `<related-links>`.

| Type | Answers | Key Structural Rule |
|------|---------|-------------------|
| `concept` | "What is X?" | `<conbody>` allows paragraphs, sections, examples; sections cannot nest |
| `task` | "How do I X?" | `<taskbody>` elements must appear in exact order; each `<step>` requires `<cmd>` |
| `reference` | "What are the specs?" | `<refbody>` allows sections/tables/properties in any sequence |
| `troubleshooting` | "What went wrong?" | Multiple cause-remedy pairs for single condition |

**DITA prolog metadata**:
```xml
<prolog>
  <author>Name</author>
  <critdates>
    <created date="2026-01-15"/>
    <revised modified="2026-02-16"/>
  </critdates>
  <metadata>
    <keywords><keyword>term1</keyword></keywords>
    <audience type="programmer" experiencelevel="expert"/>
    <prodinfo><prodname>Product</prodname><vrmlist>...</vrmlist></prodinfo>
  </metadata>
</prolog>
```

**DITA relationships**: Maps assemble topics into deliverables. Relationship tables define non-hierarchical links. Keys provide indirect addressing. Content references (conref) enable reuse.

### Information Mapping: Six Information Types

Robert Horn's framework provides a richer taxonomy than DITA:
1. **Procedure** -- sequence of steps
2. **Process** -- how a system works
3. **Principle** -- guidelines and rules
4. **Concept** -- definition and explanation
5. **Structure** -- physical or logical organization
6. **Fact** -- specific data points

Four organizational principles: chunking, relevance, labeling, consistency.

### Wikipedia Lead Section Pattern

Wikipedia requires a lead section (no heading, before first H2) that:
- Is a **standalone summary** of the entire article
- Identifies topic, establishes context, explains notability
- 100-400 words, 1-4 paragraphs
- Generally no citations (it summarizes the body)

**This maps directly to a `tldr` or `summary` field** -- a standalone description that can be consumed independently of the body.

### Zettelkasten Principles

- One idea per note (atomic)
- Unique identifiers
- Write for others (not just yourself)
- Rich linking as primary organization (not hierarchy)
- Context established through connections, not categories

---

## Part 3: Knowledge Organization Standards

### SKOS (W3C Recommendation)

SKOS provides the vocabulary for organizing topics in a taxonomy:

| Relationship | Meaning | Dewey Analog |
|-------------|---------|-------------|
| `skos:broader` | Parent topic | Domain area → topic |
| `skos:narrower` | Child topic | Topic → subtopic |
| `skos:related` | Non-hierarchical link | Cross-references |
| `skos:prefLabel` | Primary name | Topic title |
| `skos:altLabel` | Alternative name | Aliases |
| `skos:definition` | Definition text | Relevance field |
| `skos:scopeNote` | Scope guidance | What's included/excluded |

### Wikidata Statement Model

Wikidata's provenance model is directly applicable:

```
Statement
  ├── Claim (property → value)
  ├── Qualifiers (temporal bounds, conditions)
  ├── References (sources supporting the claim)
  └── Rank: preferred | normal | deprecated
```

The **rank system** maps to content freshness: `preferred` = current validated content, `normal` = standard, `deprecated` = known outdated but preserved.

### Schema.org TechArticle

Adds two fields directly relevant to knowledge base design:
- `proficiencyLevel` -- maps to depth (overview=beginner, working=intermediate, reference=expert)
- `dependencies` -- prerequisites that must be understood first

---

## Part 4: Metadata Standards

### Dublin Core (Most Relevant Elements)

| Element | Dewey Mapping |
|---------|--------------|
| `Title` | Topic name (H1) |
| `Creator` | Could add to frontmatter |
| `Subject` | Tags/keywords |
| `Description` | `relevance` field / proposed `summary` |
| `Date` | `last_validated` |
| `Type` | `depth` |
| `Source` | `sources` list |
| `Relation` | Proposed `related` field |

### JATS (Journal Article Tag Suite)

JATS provides the most rigorous provenance tracking:
- Multiple dates: received, revised, accepted, published
- Structured abstracts (background, methods, results, conclusions)
- Contributor roles beyond authorship

### Content Quality Frameworks

**Beyond Accuracy (ESEC/FSE 2020)** -- 10 quality dimensions:
- Structure: organization, internal consistency
- Content: accuracy, completeness, currency, relevance
- Style: readability, conciseness, consistency, appeal

**DORA** -- Documentation quality predicts software delivery performance. User-centricity predicts 40% higher team performance.

**Guru verification model** -- Each card has a verification interval, assigned verifier, and visual staleness indicators. Maps directly to Dewey's `last_validated` + health checks.

---

## Part 5: Gaps in Dewey's Current Format

Based on all research, these gaps were identified:

| Gap | Evidence | Priority |
|-----|----------|----------|
| **No summary/tldr field** | Wikipedia lead section, Azure RAG enrichment, llms.txt blockquote, Agent Skills description | High |
| **Section ordering ignores attention curve** | Key Guidance in middle; "lost in the middle" research | High |
| **Source Evaluation is consumer-facing noise** | Serves curation, not consumption; adds ~20 lines of dilution | High |
| **No token budget guidance** | Line counts are proxy; research uses token budgets | Medium |
| **No keywords/tags field** | DITA, Dublin Core, Contentful, Azure RAG all recommend | Medium |
| **No relationship metadata** | SKOS broader/narrower/related; DITA relationship tables | Medium |
| **No dependencies/prerequisites** | Schema.org TechArticle; DITA task prereq | Low |
| **Content type conflated with depth** | Diataxis separates type (explanation vs. how-to) from depth | Low |

---

## Part 6: What We Can Learn from Each Standard

| Standard | Take From It | Leave Behind |
|----------|-------------|-------------|
| **Diataxis** | Three-type model (explanation/procedural/reference) validates Dewey's three depths | Tutorial quadrant; rigid "don't mix types" rule |
| **DITA** | Typed topics with predictable structure; prolog metadata; `<shortdesc>` as standalone summary | XML format (80% more tokens); enterprise complexity |
| **EPPO** | Self-containment rules; domain-shaped types; rich linking | Rejection of generic types (Dewey needs structural types for progressive disclosure) |
| **Information Mapping** | Six information types as a richer classification; chunking/relevance principles | 200+ block types (over-engineered for agent consumption) |
| **Wikipedia** | Lead section as standalone summary; strict layout ordering; appendix conventions | Encyclopedic tone; no frontmatter |
| **Zettelkasten** | Atomicity; rich linking over hierarchy; write for others | Extreme atomicity (knowledge base topics are larger than zettels) |
| **SKOS** | Relationship vocabulary (broader/narrower/related); labeling (prefLabel/altLabel) | RDF syntax; formal ontology overhead |
| **Wikidata** | Statement rank system; qualifier-enriched provenance; reference tracking | Entity-centric model (too granular for topic files) |
| **Schema.org** | `proficiencyLevel`; `dependencies` | Full schema overhead |
| **S1000D** | Self-contained data modules; fine-grained information codes | Military/aerospace complexity |
| **llms.txt** | `## Optional` section marker for budget-constrained loading | Low adoption; no metadata |
| **MCP Resources** | `priority` field (0.0-1.0); `annotations.audience` | JSON-RPC transport (not file-based) |
| **Agent Skills** | Explicit 3-tier progressive disclosure; size limits (<500 lines, <5K tokens) | Skill-specific (not knowledge-specific) |
| **Guru** | Verification intervals; assigned verifiers; staleness visual indicators | Proprietary platform |
| **DORA** | Quality dimensions predict performance; user-centricity as amplifier | Organizational metrics (not file-level) |

---

## Implications for Ideal Knowledge Base Record Specification

The research points to a specification that:

1. **Keeps Markdown + YAML frontmatter** (confirmed as optimal by format benchmarks)
2. **Adds a `summary` field to frontmatter** (Wikipedia lead section, Azure enrichment, DITA shortdesc)
3. **Reorders sections for the U-shaped attention curve** (Key Guidance first, not middle)
4. **Separates curation metadata from consumer content** (Source Evaluation → .dewey/)
5. **Adds optional `tags` and `related` fields** (SKOS, Dublin Core, retrieval enrichment)
6. **Defines token budgets per depth** (research-backed, not just line counts)
7. **Borrows DITA's predictable structure per type** (agents can reliably parse known section patterns)
8. **Implements EPPO's self-containment rules** (each topic stands alone)
9. **Uses Guru's verification model** (already implemented via `last_validated` + health checks)

**Next Action:** Design the ideal specification incorporating these findings, then map to specific changes in Dewey's validators, templates, and spec.

---

## Sources

Full source lists are in the individual research agent outputs. Key sources:

- [Diataxis Framework](https://diataxis.fr/)
- [OASIS DITA 1.3 Specification](https://docs.oasis-open.org/dita/dita/v1.3/dita-v1.3-part3-all-inclusive.html)
- [EPPO Topic Characteristics](https://everypageispageone.com/series/topic-characteristics/)
- [Information Mapping Methodology](https://informationmapping.com/pages/information-mapping-methodology)
- [SKOS Reference (W3C)](https://www.w3.org/TR/skos-reference/)
- [Wikidata Data Model](https://www.wikidata.org/wiki/Wikidata:Data_model)
- [Wikipedia Manual of Style](https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Layout)
- [Agent Skills Specification](https://agentskills.io/specification)
- [MCP Resources Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)
- [llms.txt Specification](https://llmstxt.org/)
- [Dublin Core Element Set](https://www.dublincore.org/specifications/dublin-core/dces/)
- [Schema.org TechArticle](https://schema.org/TechArticle)
- [McMillan -- Structured Context Engineering (arXiv:2602.05447)](https://arxiv.org/abs/2602.05447)
- [Anthropic -- Context Engineering for Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Chroma Research -- Context Rot](https://research.trychroma.com/context-rot)
- [Beyond Accuracy (ESEC/FSE 2020)](https://arxiv.org/abs/2007.10744)
- [DORA Documentation Quality](https://dora.dev/capabilities/documentation-quality/)
- [Guru Verification Model](https://help.getguru.com/docs/verifying-and-unverifying-cards)
