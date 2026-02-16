# Deep Research: Documentation Standards, Specifications, and Paradigms for LLM/Agent Knowledge Base Design

Research date: 2026-02-16

---

## 1. Diataxis Framework (Deep Dive)

### 1.1 The Full Specification

Diataxis (created by Daniele Procida) organizes documentation along **two axes** that create four quadrants:

**Axis 1: Action vs. Cognition (Do vs. Think)**
- Left side: Practical steps, doing, action
- Right side: Theoretical understanding, thinking, cognition

**Axis 2: Acquisition vs. Application (Learn vs. Use)**
- Top: Study, learning, acquiring knowledge
- Bottom: Work, applying, using knowledge

This produces four quadrants:

| | Acquisition (Study) | Application (Work) |
|---|---|---|
| **Action (Practical)** | **Tutorial** (learning-oriented) | **How-to Guide** (goal-oriented) |
| **Cognition (Theoretical)** | **Explanation** (understanding-oriented) | **Reference** (information-oriented) |

Source: [Diataxis](https://diataxis.fr/) | [Start Here](https://diataxis.fr/start-here/)

### 1.2 Exact Rules for Each Quadrant

#### Tutorial (Learning-oriented)

**Purpose:** Help a beginner achieve basic competence so they can go on to use the product for their own purposes. The goal is not to help them get something done, but to help them learn.

**Structural rules:**
- Must be a **practical activity** (learning by doing)
- Describes what the learner will accomplish upfront
- Follows strict sequence: "First, do x. Now, do y. Now that you have done y, do z."
- Provides **minimal explanation** in the most basic language possible
- Links out to detailed explanations rather than embedding them
- Must provide **constant feedback**: "Notice that...", "Remember that...", "Let's check..."
- No room for ambiguity or doubt in instructions
- Must produce a **meaningful, attainable** outcome
- Closes learning loops by pointing out observations as the lesson progresses
- Must **not** instruct the user to make choices or provide alternatives

**Section anatomy:** Introduction (what you'll accomplish) -> Sequential steps (do X, observe Y) -> Conclusion (what you've achieved)

Source: [Tutorials - Diataxis](https://diataxis.fr/tutorials/)

#### How-to Guide (Goal-oriented)

**Purpose:** Address a real-world goal or problem by providing practical directions to an already-competent user.

**Structural rules:**
- Concerned with **work**, not study (contrast with tutorials)
- Always addresses an **already-competent user**
- Must be **adaptable** to real-world use cases (not narrowly prescriptive)
- Fundamental structure is a **sequence** grounded in patterns of user activities
- Must maintain **focus on the goal** -- resist temptation to explain or provide reference
- Should link to explanation and reference rather than embedding them
- Must have smooth **flow**: progress grounded in user's thinking patterns
- Title should describe the problem or goal ("How to..." or imperative form)

**Section anatomy:** Goal statement -> Prerequisites (if any) -> Sequential steps -> Result

Source: [How-to Guides - Diataxis](https://diataxis.fr/how-to-guides/)

#### Reference (Information-oriented)

**Purpose:** Describe the machinery as succinctly as possible, in an orderly way. Technical description of facts.

**Structural rules:**
- Architecture of reference docs must **mirror the architecture of the thing described** (e.g., classes, modules, APIs)
- Led by the **product**, not user needs (contrast with tutorials/how-to)
- Must be **austere and to the point** -- one consults reference, one doesn't read it
- Must be **wholly authoritative** -- no doubt or ambiguity
- Should be **accurate, complete, reliable**, free of distraction and interpretation
- Examples are valuable for illustration but must not become tutorials
- Must not attempt to explain or instruct

**Section anatomy:** Mirrors the structure of the thing being documented. For an API: module -> class -> method, each with signature, parameters, return values, examples.

Source: [Reference - Diataxis](https://diataxis.fr/reference/)

#### Explanation (Understanding-oriented)

**Purpose:** Deepen and broaden understanding. Discursive treatment that permits reflection.

**Structural rules:**
- Must **not** instruct or provide technical description
- Can and must consider **alternatives, counter-examples, multiple approaches**
- Should illuminate the subject with **context, background, connections**
- Writing should be like a **knowledgeable friend sharing insights**
- Goal is deeper understanding rather than problem solving

**Section anatomy:** Introduction (states purpose, previews discussion) -> Definition -> Background (history, context) -> Details (aspects, elaboration) -> Relationships (connections to other ideas) -> Implications (effects, significance) -> Summary -> Further Reading

Source: [Explanation - Diataxis](https://diataxis.fr/explanation/)

### 1.3 Progressive Disclosure in Diataxis

Diataxis handles progressive disclosure through **separation of document types**. A tutorial provides initial exposure, then how-to guides provide practical application, reference provides exhaustive detail, and explanation provides conceptual depth. Each document type links to the others. The user self-selects which type they need based on their current mode (studying vs. working, practical vs. theoretical).

This is **structural** progressive disclosure -- the content is in different documents, not layered within a single document.

### 1.4 Large Project Implementations

**Django:** Procida's experience with Django documentation directly informed Diataxis development. Django's docs are organized into tutorials, topic guides, reference, and how-to sections.

**Gatsby:** Reorganized open-source documentation using Diataxis as the primary framework. The four quadrants helped prioritize user goals for each documentation type and restructured docs to improve discoverability.

**Cloudflare:** Used Diataxis as their "north star" when redesigning developer docs. When unsure where new content should fit, they consulted the framework.

**Canonical/Ubuntu:** Adopted Diataxis as a new foundation for all Canonical documentation.

**Python:** Community discussion about adopting Diataxis for Python documentation (discuss.python.org thread).

Source: [Django](https://docs.djangoproject.com/) | [Diataxis implementations](https://diataxis.fr/)

### 1.5 Criticisms of Diataxis

1. **Rigidity:** Some knowledge doesn't neatly fit into four categories. The framework can feel overly rigid for certain content.
2. **Overkill for simple products:** Very simple products may not need four distinct documentation types.
3. **Self-referential inconsistency:** The Diataxis documentation itself does not follow the Diataxis approach.
4. **AI may reduce relevance:** With AI chatbots and agents delivering hyper-personalized help, the information architecture of documentation may become less critical -- users interface through AI rather than navigating docs directly.
5. **Team friction:** Religious application can bring friction. Recommended to "soft apply" rather than enforce rigidly.
6. **Boundary blurring:** In practice, content often blends types (e.g., a how-to that requires explanation, a reference that includes examples).

Source: [I'd Rather Be Writing](https://idratherbewriting.com/blog/what-is-diataxis-documentation-framework) | [Emmanuel Bernard](https://emmanuelbernard.com/blog/2024/12/19/diataxis/)

### 1.6 Mapping to Agent Consumption

Diataxis maps to agent consumption needs as follows:

| Diataxis Type | Agent Use Case | Token Efficiency | Retrieval Pattern |
|---|---|---|---|
| Tutorial | Rarely needed by agents (agents don't "learn" the same way) | Low efficiency (verbose) | Rarely retrieved |
| How-to | Directly useful: step-by-step procedures | Medium efficiency | Retrieved for task completion |
| Reference | Highly useful: precise, structured facts | High efficiency (terse) | Retrieved for accuracy/lookup |
| Explanation | Useful for reasoning: context, rationale, relationships | Medium efficiency | Retrieved for judgment calls |

**Key insight:** For agent consumption, the tutorial quadrant is largely irrelevant. Agents need reference (for facts), how-to (for procedures), and explanation (for reasoning context). This suggests a **three-type model** may be more appropriate for agent-optimized knowledge bases.

---

## 2. Other Documentation Paradigms

### 2.1 EPPO (Every Page is Page One) -- Mark Baker

**Core concept:** Every topic should function as if it's the first page the reader encounters. No topic should depend on being read in a particular order.

#### Seven Characteristics of an EPPO Topic

1. **Self-contained:** Contains everything needed to fulfill its purpose for its intended audience. No linear dependencies on other topics. Does not merely stand alone -- it *functions* alone.

2. **Specific and limited purpose:** Each topic serves one specific, limited purpose. Not a dumping ground for related information.

3. **Conform to a type:** Topics naturally conform to types, but these types are **domain-specific, not generic**. A recipe is a type. A used car review is a type. An API endpoint description is a type. These are more specific than "concept, task, reference."

4. **Establish context:** Cannot assume context is established by position in a larger narrative or hierarchy. Must establish its own context within its opening.

5. **Assume the reader is qualified:** Written for the type of person who normally does the task. A recipe assumes cooking knowledge ("whisk," "blanch," "puree"). Does not teach prerequisites.

6. **Stay on one level:** Each topic stays on one level of detail/abstraction. Helps readers change levels through links, but doesn't mix levels within a single topic.

7. **Link richly:** Designed for bottom-up navigation. Must link richly along lines of **subject affinity** to support the reader steering their own course.

#### Topic Typing in EPPO

The type of an EPPO topic is **not** generic like concept/task/reference. It is **domain-specific**:
- A recipe has a consistent pattern: title, prep time, servings, ingredients list, preparation steps, serving suggestions
- A used car review: overview, equipment, notable features, interior, safety, economy, reliability, price history
- An API endpoint: URL, method, parameters, request body, response, examples, errors

These types emerge naturally from domain practice over time. They are not imposed by a framework but discovered through analysis of how practitioners actually organize information about specific subjects.

**Key insight for knowledge bases:** Topic types should be designed around the **domain being documented**, not around generic information categories.

Source: [EPPO Characteristics](https://everypageispageone.com/series/topic-characteristics/) | [EPPO Topics Conform to a Type](https://everypageispageone.com/2011/11/12/eppo-topics-conform-to-a-type/) | [EPPO Examples](https://everypageispageone.com/examples-of-eppo-topics/)

### 2.2 Information Mapping (Robert Horn)

Developed through research at Harvard and Columbia on how readers deal with large amounts of information.

#### Three Components

1. **Analysis:** Classify information into types
2. **Organization:** Apply structural principles
3. **Presentation:** Format for comprehension

#### Six Information Types

| Type | Definition | Example |
|---|---|---|
| **Procedure** | Sequential steps to complete a task | Install instructions |
| **Process** | How groups interact over time, stage descriptions | Deployment pipeline |
| **Principle** | Underlying premises and rules; remain consistent regardless of context | Design patterns |
| **Concept** | Ideas, definitions, notions about a topic | "What is a container?" |
| **Structure** | Something divisible into parts with boundaries; component parts and interactions | System architecture |
| **Fact** | A bit of true, observable information | Version numbers, limits |

#### Six Organizational Principles

1. **Chunking:** Separate information into concise blocks. Each block encompasses a single main idea.
2. **Relevance:** Every element must relate to the concept being expressed.
3. **Labeling:** Every block must have a clearly identifiable label.
4. **Consistency:** Maintain consistent language and formatting across similar information types.
5. **Integrated Graphics:** Use visual elements alongside text.
6. **Accessible Detail:** Layer information so detail is available when needed but doesn't clutter the primary message.

#### Information Blocks

Horn identified **over 200 common block types** -- structural components of documentation. Each block:
- Encompasses a **single main idea**
- Might consist of sentences, a list, a table, a graphic, or multimedia
- Must be **labeled** and **visually separated** from other blocks

**Key insight for knowledge bases:** The concept of "information blocks" -- small, labeled, single-purpose units -- maps well to how LLMs chunk and retrieve content. The six information types provide a richer taxonomy than concept/task/reference.

Source: [Information Mapping Methodology](https://informationmapping.com/pages/information-mapping-methodology) | [Iva Cheung Introduction](https://ivacheung.com/2012/11/introduction-to-information-mapping/) | [TCBOK](https://www.tcbok.org/principles-and-practices/information-mapping/)

### 2.3 DITA (Darwin Information Typing Architecture)

OASIS open standard (latest: DITA 1.3) for authoring and organizing topic-oriented information using XML.

#### Five Specialized Topic Types

Each is a specialization of a generic `<topic>` type:

**1. Concept (`<concept>`)**
```xml
<concept id="intro-bird-calling">
  <title>Introduction to Bird Calling</title>
  <shortdesc>If you wish to attract more birds...</shortdesc>
  <prolog>
    <author>Jane Smith</author>
    <metadata>
      <audience type="user" experiencelevel="novice"/>
      <category>Wildlife</category>
      <keywords><keyword>birds</keyword></keywords>
    </metadata>
  </prolog>
  <conbody>
    <p>Bird calling requires learning:</p>
    <ul>...</ul>
  </conbody>
</concept>
```
- Contains: `<title>`, optional `<titlealts>`, optional `<shortdesc>`, optional `<prolog>`, optional `<conbody>`, optional `<related-links>`
- Body allows: paragraphs, lists, tables, figures, general elements
- Purpose: Extended definitions, background information, rules and guidelines

**2. Task (`<task>`) -- Strict Model**
```xml
<task id="install-software">
  <title>Installing the Software</title>
  <shortdesc>Follow these steps to install...</shortdesc>
  <taskbody>
    <prereq>Ensure you have admin access.</prereq>
    <context>The installer will configure...</context>
    <steps>
      <step><cmd>Download the installer</cmd></step>
      <step><cmd>Run setup.exe</cmd>
        <info>Accept the license agreement.</info>
      </step>
    </steps>
    <result>The software is now installed.</result>
    <postreq>Restart your computer.</postreq>
  </taskbody>
</task>
```
- Strict order: `<prereq>` -> `<context>` -> `<steps>` -> `<result>` -> `<example>` -> `<postreq>` (each optional)
- Each `<step>` must contain a `<cmd>` element
- General task model (DITA 1.2+) allows `<section>` and `<steps-informal>`, multiple instances and varying order

**3. Reference (`<reference>`)**
```xml
<reference id="api-create-user">
  <title>POST /users</title>
  <shortdesc>Creates a new user account.</shortdesc>
  <refbody>
    <refsyn>POST /api/v1/users</refsyn>
    <section><title>Parameters</title>
      <p>...</p>
    </section>
    <properties>
      <property>
        <proptype>username</proptype>
        <propvalue>string</propvalue>
        <propdesc>Required. The user's login name.</propdesc>
      </property>
    </properties>
  </refbody>
</reference>
```
- Body allows: sections, property lists (`<properties>`), tables, syntax sections (`<refsyn>`), examples
- All elements optional, any sequence and number
- `<properties>` is a three-column table: type, value, description

**4. Glossary Entry (`<glossentry>`)**
- Term and definition pair with optional related terms

**5. Troubleshooting (`<troubleshooting>`)**
- Condition, cause, remedy structure

#### DITA Prolog Metadata Elements

The `<prolog>` element contains topic metadata (often not rendered but used for processing):

| Element | Purpose |
|---|---|
| `<author>` | Topic author name |
| `<audience>` | Intended audience with `type`, `job`, `experiencelevel` attributes |
| `<category>` | Classification for retrieval/navigation |
| `<keywords>` | Search and indexing terms |
| `<prodinfo>` | Product information (name, version, platform) |
| `<othermeta>` | Custom name/value metadata pairs |
| `<critdates>` | Critical dates (created, revised) |
| `<permissions>` | Access permissions |
| `<source>` | Source of the content |
| `<publisher>` | Publisher information |

#### DITA Maps

DITA maps (`<map>` / `.ditamap`) define relationships between topics:
- `<topicref>` elements reference topics and create hierarchy
- `<reltable>` elements define non-hierarchical relationships
- `<topicgroup>` elements create groupings outside hierarchy
- Maps control navigation, table of contents, and build outputs

#### Content Reuse Mechanisms

- **Conref (direct):** Pull content from another topic by referencing its ID directly
- **Keyref (indirect):** Reference a "key name" that maps bind to specific resources. Allows late binding -- different maps can bind the same key to different content.
- **Specialization:** Add new elements and attributes by specializing base DITA elements. Allows domain-specific extensions while maintaining base compatibility.

**Key insight for knowledge bases:** DITA's prolog metadata model is the most comprehensive of any standard examined. The audience, prodinfo, and critdates elements directly address freshness, targeting, and provenance concerns relevant to LLM knowledge bases.

Source: [OASIS DITA 1.3 Spec](https://docs.oasis-open.org/dita/dita/v1.3/dita-v1.3-part3-all-inclusive.html) | [Topic Structure](https://www.oxygenxml.com/dita/1.3/specs/archSpec/base/topicstructure.html) | [DITA Concept](https://docs.oasis-open.org/dita/v1.0/langspec/concept.html) | [DITA Task](https://www.oxygenxml.com/dita/1.3/specs/archSpec/technicalContent/dita-task-topic.html)

### 2.4 Topic-Based Authoring Standards

**Definition:** A modular approach to content creation where content is structured around self-contained units ("topics"), each addressing a single subject or answering a single question.

**Key standards:**
- **DITA** (see above) -- the most formal standard
- **DocBook** -- XML standard for books and articles, less topic-focused
- **Structured FrameMaker** -- Adobe's structured authoring environment
- **MadCap Flare** -- Topic-based authoring for help systems

**Formal definition of "topic":**
- Contains only the information needed to understand **one concept**, perform **one procedure**, or look up **one set of reference information**
- Every paragraph, sentence, list item, or table entry has a **strictly defined function**
- Stored in XHTML or XML format
- Supports content reuse, management, and dynamic assembly of personalized information

**Structured authoring definition (comprehensive):**
> "A standardised methodological approach to the creation of content incorporating information types, systematic use of metadata, XML-based semantic mark-up, modular, topic-based information architecture, a constrained writing environment with software-enforced rules, content re-use, and the separation of content and form."

Source: [Wikipedia: Topic-based authoring](https://en.wikipedia.org/wiki/Topic-based_authoring) | [Paligo Guide](https://paligo.net/blog/structured-authoring/the-essential-guide-to-topic-based-authoring/) | [Heretto](https://www.heretto.com/blog/topic-based-authoring-vs-traditional-authoring)

### 2.5 Zettelkasten

#### Luhmann's Original System

Niklas Luhmann (German sociologist) built a system of approximately **90,000 index cards** and credited it for his extraordinarily prolific writing output.

**Core structural rules:**

1. **One idea per note:** Each card contains a single, complete, self-contained idea.

2. **Unique identifier:** Each card receives a fixed number using a branching hierarchy:
   - Card 1/1: Original note
   - Card 1/1a: Builds on 1/1
   - Card 1/1b: Also builds on 1/1
   - Card 1/1b1: Builds on 1/1b
   This numbering allows **insertion** of new notes at any point without reorganizing.

3. **Write in your own words:** No copying or direct quotes. Forces understanding.

4. **Write for others:** Include enough context that someone else could understand the note.

5. **Links and connections:** Notes link to each other through subject headings, numbers, and tags. Connections are the primary organizational mechanism, not categories.

6. **No categorical filing:** Notes are not filed by topic. They are filed sequentially and connected through links. The network of connections *is* the organization.

#### Modern Implementations

**Obsidian metadata fields (YAML frontmatter):**
```yaml
---
title: "Note Title"
date: 2026-02-16
tags: [concept, architecture]
aliases: ["alternate name"]
cssclasses: []
type: permanent  # or fleeting, literature, index
domain: "software engineering"
---
```
- Natively supports: `tags`, `aliases`, `cssclasses`
- ISO date format (YYYY-MM-DD) preferred for reliable sorting
- Custom fields (type, domain, status) are user-defined
- Bidirectional links via `[[wikilinks]]`
- Graph view visualizes connection networks

**Logseq metadata:**
```
date:: 2026-02-16
type:: permanent
tags:: concept, architecture
```
- Block-level rather than file-level
- Property syntax: `property:: value`
- Stores as markdown files

**Key insight for knowledge bases:** The Zettelkasten principle of "one idea per note" and "write for others" maps directly to agent-optimized content. The branching identifier system presages modern hierarchical file organization. Rich linking creates a navigable knowledge graph.

Source: [Zettelkasten.de Introduction](https://zettelkasten.de/introduction/) | [Wikipedia](https://en.wikipedia.org/wiki/Zettelkasten) | [Obsidian Help](https://help.obsidian.md/properties)

---

## 3. Documentation Specification Languages

### 3.1 Formal Schema Languages for Document Structure

**Document Type Definition (DTD):**
- Original SGML/XML schema language
- Defines valid building blocks: required/allowed elements, hierarchy, relationships
- Used by DITA (through Issue 3.0), S1000D, DocBook
- Limitations: no namespace support, limited data typing

**XML Schema (W3C XSD):**
- Namespace-aware, richer data typing than DTDs
- Used by DITA (from Issue 4.0), S1000D (from Issue 4.0)
- Can define complex content models with inheritance

**RELAX NG (ISO/IEC 19757-2):**
- Simpler syntax than XSD, equally powerful
- Two syntaxes: XML and compact
- Used by some documentation standards

**Document Schema Definition Languages (DSDL) -- ISO/IEC 19757:**
- Modular set of specifications for describing document structures, data types, and relationships
- Includes RELAX NG, Schematron, NVDL, and others

**JSON Schema:**
- Declarative language for validating JSON documents' structure, constraints, and data types
- Latest: Draft 2020-12
- Key keywords: `$schema`, `$id`, `title`, `description`, `type`, `properties`, `required`, `additionalProperties`
- Can define `$ref` for schema reuse
- Vocabularies are the primary unit of reuse

**YAML Schema:**
- No independent YAML schema standard exists
- YAML documents are typically validated using JSON Schema (since YAML is a superset of JSON)
- Some tools (like Ajv) support YAML validation through JSON Schema

### 3.2 How DITA Defines Topic Types Formally

DITA uses **specialization** to define new topic types:

1. Each topic type is defined as an XML Schema (or DTD) that extends the base `<topic>` schema
2. The `<concept>` schema adds `<conbody>` with its specific content model
3. The `<task>` schema adds `<taskbody>` with its strict element ordering
4. Custom specializations can add domain-specific elements while maintaining backward compatibility

The formal definition includes:
- Element declarations (what elements are allowed)
- Content models (what order and cardinality)
- Attribute declarations (what metadata attributes are available)
- Inheritance chain (which base type is specialized)

### 3.3 Can JSON Schema Define Knowledge Base Record Formats?

**Yes.** A knowledge base record format could be specified as a JSON Schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "knowledge-base-topic.schema.json",
  "title": "Knowledge Base Topic",
  "type": "object",
  "properties": {
    "frontmatter": {
      "type": "object",
      "properties": {
        "sources": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "url": { "type": "string", "format": "uri" },
              "title": { "type": "string" }
            },
            "required": ["url", "title"]
          },
          "minItems": 1
        },
        "last_validated": { "type": "string", "format": "date" },
        "depth": { "enum": ["overview", "working", "reference"] },
        "relevance": { "type": "string" }
      },
      "required": ["sources", "last_validated", "depth", "relevance"]
    },
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "heading": { "type": "string" },
          "required": { "type": "boolean" },
          "content_type": { "enum": ["prose", "list", "table", "code"] }
        }
      }
    }
  }
}
```

**Limitations:** JSON Schema validates data structure, not markdown document structure. It could validate extracted frontmatter but not the markdown body directly. A hybrid approach would be needed: JSON Schema for frontmatter validation + custom validators for body structure.

Source: [JSON Schema Specification](https://json-schema.org/specification) | [DSDL](https://en.wikipedia.org/wiki/Document_Schema_Definition_Languages) | [DTD](https://en.wikipedia.org/wiki/Document_type_definition)

---

## 4. AI-Optimized Documentation Standards

### 4.1 llms.txt

**Specification** (proposed by Jeremy Howard, Answer.AI, September 2024):

#### Exact Format

```markdown
# Project Name

> Brief project summary containing key information necessary for
> an LLM to understand the project.

Zero or more markdown sections (paragraphs, lists, etc) of any type
except headings, containing more detailed information.

## Core Documentation

- [Quick Start](https://example.com/quickstart): Getting started guide
- [API Reference](https://example.com/api): Complete API documentation
- [Configuration](https://example.com/config): Configuration options

## Optional

- [Changelog](https://example.com/changelog): Version history
- [Contributing](https://example.com/contributing): How to contribute
```

**Required sections:**
- H1 with project/site name (the **only** required element)

**Optional sections (in order):**
- Blockquote with short summary containing key information
- Zero or more markdown sections (no headings) with detailed information
- Zero or more H2-delimited "file lists" containing markdown hyperlinks
- Each file list item: `- [name](url)` optionally followed by `: description`
- An `## Optional` H2 specifically marks less critical resources

**Key characteristics:**
- Plain text, Markdown formatted
- Must sit at domain root: `yoursite.com/llms.txt`
- Human AND LLM readable, but also parseable by classical programming (regex, parsers)
- Companion: `.md` page mirrors at same paths provide clean, token-efficient versions

**Adoption status (as of early 2026):**
- Only ~951 domains had published llms.txt files (as of July 2025, per NerdyData)
- Major AI crawlers (GPTbot, ClaudeBot, PerplexityBot) showed **zero visits** to llms.txt pages in testing
- Still a *proposed* standard, not formally adopted by major AI companies
- Mintlify and GitBook auto-generate llms.txt files

Source: [llmstxt.org](https://llmstxt.org/) | [Answer.AI blog](https://www.answer.ai/posts/2024-09-03-llmstxt.html) | [GitHub](https://github.com/AnswerDotAI/llms-txt) | [Semrush](https://www.semrush.com/blog/llms-txt/)

### 4.2 Context7

**What it is:** An MCP (Model Context Protocol) server built by Upstash that injects up-to-date documentation directly into an LLM's context window.

**How it structures documentation:**
- Indexes an entire project's documentation
- Pre-processes and cleans each part
- Filters on demand using a proprietary ranking algorithm
- Documentation injected directly into prompts

**MCP Tools exposed:**
1. `resolve-library-id` -- Resolves a general library name to a Context7-compatible ID
2. `query-docs` -- Retrieves documentation for a library using that ID

**Access methods:** HTTP (remote) or stdio (local)

**Key insight:** Context7 doesn't define a documentation *format* -- it's a **retrieval and injection** system. It pre-processes existing docs into chunks and serves them based on query relevance. The "use context7" prompt triggers library detection and documentation filtering.

Source: [GitHub: upstash/context7](https://github.com/upstash/context7) | [Context7.com](https://context7.com/) | [Upstash blog](https://upstash.com/blog/context7-mcp)

### 4.3 Mintlify

**Documentation format:** MDX (Markdown with React components), YAML frontmatter for metadata.

**LLM-optimization features:**
- Auto-generates `/llms.txt` file listing all pages
- Auto-generates `/llms-full.txt` combining entire documentation into one file
- Every page available as raw Markdown by appending `.md` to URL
- Sends content as Markdown (not HTML) to AI agents -- faster processing, fewer tokens
- Passage-level indexing: LLMs break docs into chunks as small as a few lines

**MAGI (Markdown for Agent Guidance & Instruction):**
- Uses YAML frontmatter fields
- Comprehensive metadata in page frontmatter

**Best practices for dual (AI + human) readability:**
- Meaningful subheadings for LLM identification and retrieval
- Code blocks, tables, summaries
- Structured content with clear heading hierarchy

Source: [Mintlify](https://www.mintlify.com/) | [Mintlify AI Docs Trends 2025](https://www.mintlify.com/blog/ai-documentation-trends-whats-changing-in-2025) | [Mintlify llms.txt](https://www.mintlify.com/docs/ai/llmstxt)

### 4.4 GitBook

**LLM-ready features:**
- All pages automatically available as Markdown (append `.md` extension)
- Auto-generates `llms-full.txt` with all site content in Markdown
- Auto-generates `llms.txt` index
- **Model Context Protocol (MCP) server** auto-exposed for every published space
  - AI tools discover and retrieve docs as structured resources
  - No scraping needed

**GEO (Generative Engine Optimization):**
- Practice of structuring docs so LLMs can ingest reliably and cite accurately
- Recommendations: good headings, bullet points, numbered lists, shorter paragraphs
- Code snippets, API examples, real scenarios for practical understanding

Source: [GitBook LLM-ready docs](https://gitbook.com/docs/publishing-documentation/llm-ready-docs) | [GitBook GEO guide](https://gitbook.com/docs/guides/seo-and-llm-optimization/geo-guide-how-to-optimize-your-docs-for-ai-search-and-llm-ingestion)

### 4.5 DevDocs

**Structure:** Normalized HTML partials + two JSON files (index + offline data).

**Content processing pipeline:**
1. Scraper downloads HTML or reads from filesystem
2. Documents parsed using Nokogiri
3. Filters applied via HTML::Pipeline (specific to each documentation source)
4. One filter determines page metadata
5. Output: normalized HTML partials + JSON index + JSON offline data

**Metadata model:**
- Each piece of content identified by a unique, "obvious" and short string
- Focuses specifically on API/reference content
- Indexes only the minimum useful to most developers

**Key insight:** DevDocs reduces documentation to its most essential form: short identifier + normalized content + metadata index. This minimal approach optimizes for fast lookup, which is exactly how agents use reference material.

Source: [DevDocs.io](https://devdocs.io/) | [GitHub: freeCodeCamp/devdocs](https://github.com/freeCodeCamp/devdocs)

### 4.6 OpenAPI/Swagger

**OpenAPI 3.1.0** specification defines a standard interface to RESTful APIs:

**Document structure (top-level objects):**
- `openapi` (version)
- `info` (title, description, version, contact, license)
- `servers` (base URLs)
- `paths` (endpoints and operations)
- `components` (reusable schemas, responses, parameters, examples, security schemes)
- `security` (security requirements)
- `tags` (grouping operations)
- `webhooks` (3.1.0+)

**Schema Object:** Defines input/output data types using JSON Schema vocabulary (aligned in 3.1.0).

**Applicable patterns for general knowledge:**
- **Component reuse:** Define once, reference everywhere (`$ref`)
- **Structured metadata:** Rich info block with title, description, version, contact
- **Tags for grouping:** Logical grouping without hierarchy
- **Examples inline:** Concrete examples attached to abstract schemas
- **Discriminator:** Polymorphism support -- choosing schema based on property value

Source: [OpenAPI 3.1.0 Spec](https://spec.openapis.org/oas/v3.1.0) | [Swagger Specification](https://swagger.io/specification/)

### 4.7 Best Practices for LLM-Optimized Documentation (Synthesis)

From kapa.ai, Redocly, Mintlify, and GitBook research:

**Structural requirements:**
1. **Heading hierarchy:** LLMs build mental maps from heading levels. Never skip levels (H1->H3 breaks comprehension).
2. **Self-contained pages:** Each page must stand on its own since LLMs process individual pages/sections without broader navigation context.
3. **Consistent terminology:** One term for one concept throughout. AI systems get confused by synonyms for the same thing.
4. **Semantic chunking:** Divide into smaller, semantically coherent chunks. Passage-level indexing is the 2025 norm.
5. **Contextual completeness:** Each section carries sufficient context to be understood independently while maintaining relationships to parent/sibling content.
6. **Code formatting:** Properly formatted code blocks prevent AI from merging or altering commands.
7. **Self-contained rows in tables:** Keep table rows self-contained. Replace complex cross-referencing tables with prose.
8. **Explicit, not implicit:** AI cannot infer unstated information. State everything explicitly.

**Metadata requirements:**
1. **Title and description:** Clear, consistent naming
2. **Date modified:** Freshness signal for retrieval systems
3. **Version/product info:** Context for applicability
4. **Keywords/tags:** Aid semantic search and retrieval

Source: [kapa.ai Best Practices](https://docs.kapa.ai/improving/writing-best-practices) | [Redocly LLM optimization](https://redocly.com/blog/optimizations-to-make-to-your-docs-for-llms) | [Mintlify structuring docs for AI](https://www.mintlify.com/blog/structure-documentation-AI-human-readers)

---

## 5. Content Models and Information Architecture

### 5.1 What is a "Content Model"?

A content model is an architectural framework for a collection of content. It formally defines:
- **Content types** (classes/templates): The categories of content (e.g., blog post, API reference, tutorial)
- **Fields** (attributes): The properties of each type (e.g., title, author, date, body)
- **Relationships:** How content types relate to each other (e.g., a tutorial references an API endpoint)
- **Constraints:** Rules about required fields, valid values, cardinality

**Content types vs. content structures:**
- **Content types** define *what* the content is (blog post, recipe, API reference)
- **Content structures** define *how* the content is organized internally (sections, fields, ordering)
- Both matter: types enable **categorization and retrieval**, structures enable **consistency and validation**

### 5.2 CMS Content Schema Approaches

**Sanity (code-defined schemas):**
```javascript
export default {
  name: 'blogPost',
  type: 'document',
  fields: [
    { name: 'title', type: 'string', validation: Rule => Rule.required() },
    { name: 'slug', type: 'slug', options: { source: 'title' } },
    { name: 'author', type: 'reference', to: [{ type: 'author' }] },
    { name: 'publishedAt', type: 'datetime' },
    { name: 'body', type: 'blockContent' },
    { name: 'categories', type: 'array', of: [{ type: 'reference', to: { type: 'category' } }] }
  ]
}
```
- Schemas defined in JavaScript/TypeScript
- Version-controlled alongside application code
- Supports complex nested structures and references
- Hot-module-reloading for instant schema changes

**Contentful (UI-defined schemas):**
- Content types defined through web-based UI
- Pre-built templates and types
- Field types: Short text, Long text, Integer, Decimal, Date, Location, Media, Boolean, JSON, Reference, Rich text
- Less flexible for complex custom structures

**Key insight:** The Sanity approach (schema-as-code) is the most relevant model for a knowledge base specification. It allows version control, code review, and programmatic validation -- all characteristics Dewey already uses.

Source: [Sanity Content Modeling](https://www.sanity.io/content-modeling) | [Heretto Structured Content](https://www.heretto.com/blog/structured-content)

### 5.3 S1000D (Defense/Aerospace)

**Scale:** International specification for technical publications using a common source database.

**Data Module structure:**
1. **Identification and Status Section (metadata):**
   - Data Module Code (DMC) -- unique identifier following naming convention
   - Status: current, superseded, deleted
   - Applicability information
   - Quality assurance metadata
   - Retrieval control data

2. **Content Section (body):**
   - Descriptive, procedural, or operational data
   - 21 data module types including: Description, Procedure, Parts, Scheduled Maintenance, Fault Isolation, Operational

**Information Codes:**
- 3 alphanumeric characters (primary, secondary, tertiary)
- 11 primary categories
- Example: 040 = various descriptions, 041 = how a component is made, 042 = function of a component
- Enables precise classification of content type

**Data Module Code (DMC) structure:**
- Encodes: model identification, system difference, system, subsystem, subject, disassembly, disassembly variant, information code, information code variant, item location code
- Example: `DMC-S1000DBIKE-AAA-D00-00-00-00AA-040A-D`

**Key insight:** S1000D's data module concept -- a self-contained unit with standardized metadata header and typed content -- is the most rigorous example of the pattern Dewey uses (frontmatter + body). The information code system provides extremely fine-grained content type classification.

Source: [S1000D.org](https://s1000d.org/?page_id=101) | [Wikipedia: S1000D](https://en.wikipedia.org/wiki/S1000D) | [Smartify S1000D](https://smartifysol.com/s1000d-specification/)

### 5.4 ASD-STE100 (Simplified Technical English)

**What it is:** A controlled natural language standard for technical documentation. Published January 2025 as international standard.

**Specification:**
- **53 writing rules** covering grammar and style
- **Dictionary of ~900 approved words** with controlled meanings
- Principle: "one word -- one meaning" (when multiple definitions exist, STE selects one)
- Permits company-specific/project-specific technical terms ("technical names" and "technical verbs")
- Required by S1000D specification and ATA i2200

**Key rules relevant to knowledge bases:**
- Use short sentences (max 20 words for procedural, 25 for descriptive)
- Use active voice
- Use approved words only for their approved meanings
- Write instructions in imperative mood
- One instruction per sentence
- Start safety instructions with the warning, then the action

**Key insight:** STE's controlled vocabulary and sentence-length rules directly improve LLM comprehension. The "one word, one meaning" principle eliminates ambiguity that causes AI systems to produce inconsistent responses. The sentence length limits align with chunking best practices.

Source: [ASD-STE100](https://www.asd-ste100.org/) | [About STE](https://www.asd-ste100.org/about.html) | [Wikipedia: STE](https://en.wikipedia.org/wiki/Simplified_Technical_English)

---

## 6. Metadata Standards for Documents

### 6.1 Dublin Core

**Standard:** ISO 15836, ANSI/NISO Z39.85 (first standardized 1998)

**The 15 Core Elements:**

| # | Element | Definition | LLM Relevance |
|---|---------|-----------|----------------|
| 1 | **Title** | Formal name of the resource | HIGH -- primary identification |
| 2 | **Creator** | Author or originator | MEDIUM -- provenance |
| 3 | **Subject** | Topic described using keywords or classification | HIGH -- retrieval and categorization |
| 4 | **Description** | Summary (e.g., abstract) | HIGH -- information scent for agents |
| 5 | **Publisher** | Entity making resource available | LOW |
| 6 | **Contributor** | Additional contributors | LOW |
| 7 | **Date** | Significant moments in lifecycle | HIGH -- freshness signal |
| 8 | **Type** | Nature or genre of the resource | HIGH -- content type classification |
| 9 | **Format** | Physical or digital manifestation | LOW |
| 10 | **Identifier** | Unique identifier (URI, ISBN, etc.) | MEDIUM -- deduplication |
| 11 | **Source** | Resource from which this derives | HIGH -- provenance and source primacy |
| 12 | **Language** | Language of the content | LOW |
| 13 | **Relation** | Related resources | MEDIUM -- knowledge graph |
| 14 | **Coverage** | Spatial/temporal scope | LOW |
| 15 | **Rights** | Access restrictions or usage terms | LOW |

**Key characteristics:**
- Every element is **optional** and may be **repeated**
- No prescribed order
- Syntax-independent: can be expressed in XML, RDF, HTML meta tags, JSON-LD
- Designed for both machine and human interpretation

**Extended terms (DCMI Metadata Terms):**
- `dcterms:created`, `dcterms:modified`, `dcterms:valid`
- `dcterms:audience`
- `dcterms:abstract`
- `dcterms:tableOfContents`
- `dcterms:isPartOf`, `dcterms:hasPart`
- `dcterms:isReplacedBy`, `dcterms:replaces`

**Key insight for knowledge bases:** Dublin Core's Subject, Description, Date, Type, Source, and Relation elements map directly to Dewey's frontmatter fields. The extended terms add useful granularity (created vs. modified, audience, partOf relationships).

Source: [DCMI Element Set](https://www.dublincore.org/specifications/dublin-core/dces/) | [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) | [Wikipedia: Dublin Core](https://en.wikipedia.org/wiki/Dublin_Core)

### 6.2 PRISM (Publishing Requirements for Industry Standard Metadata)

**Standard:** W3C Member Submission, version 3.0

**Namespaces:**
- `prism:` -- Core PRISM elements
- `pur:` -- Usage rights
- `dc:` / `dcterms:` -- Dublin Core (PRISM extends DC)
- `pim:` -- Inline metadata
- `prl:` -- Rights language
- `pam:` -- Aggregator message
- `pcv:` -- Controlled vocabulary

**Key metadata fields (beyond Dublin Core):**

| Field | Description |
|---|---|
| `prism:contentType` | Content type from controlled vocabulary (article, chapter, advertisement, etc.) |
| `prism:academicField` | Refines dc:subject by specifying academic specialty |
| `prism:byteCount` | Size of the article |
| `prism:wordCount` | Word count |
| `prism:pageRange` | Page range in print |
| `prism:section` | Section within a publication |
| `prism:subsection1` through `prism:subsection4` | Nested subsections |
| `prism:aggregationType` | Type of aggregation (journal, magazine, etc.) |
| `prism:publicationName` | Name of the publication |
| `pur:permissions` | Special usage permissions with code attribute |
| `pur:adultContentWarning` | Content warning flag |

**Expression formats:** XML, RDF/XML, XMP

**Key insight:** PRISM's `contentType` controlled vocabulary and hierarchical subsection metadata are relevant. The contentType field enables the same kind of depth/type classification Dewey uses but with a standardized vocabulary.

Source: [W3C PRISM Submission](https://www.w3.org/submissions/prism/) | [Wikipedia: PRISM](https://en.wikipedia.org/wiki/Publishing_Requirements_for_Industry_Standard_Metadata)

### 6.3 Schema.org Article/TechArticle

**TechArticle** (inherits from Article -> CreativeWork -> Thing):

**Unique TechArticle properties:**

| Property | Type | Description |
|---|---|---|
| `dependencies` | Text | Prerequisites needed to fulfill steps in the article |
| `proficiencyLevel` | Text | Expected values: 'Beginner', 'Expert' |

**Inherited Article properties:**

| Property | Type | Description |
|---|---|---|
| `headline` | Text | Article headline (max 110 chars) |
| `description` | Text | Summary of the article |
| `author` | Person/Organization | Author |
| `datePublished` | Date | Publication date |
| `dateModified` | Date | Last modification date |
| `articleBody` | Text | Full text of the article |
| `articleSection` | Text | Section articles appear within |
| `wordCount` | Integer | Word count |
| `keywords` | Text | Keywords or tags |
| `inLanguage` | Text | Language (IETF BCP 47) |
| `image` | URL/ImageObject | Article image |
| `speakable` | SpeakableSpecification | Sections suitable for text-to-speech |

**Provenance properties:**
| Property | Type | Description |
|---|---|---|
| `sdDatePublished` | Date | Original publication date in source |
| `sdPublisher` | Organization | Original publisher/source |
| `license` | CreativeWork/URL | License |
| `usageInfo` | CreativeWork/URL | Usage guidelines |

**Implementation format:** JSON-LD (recommended), Microdata, or RDFa.

**Key insight:** The `proficiencyLevel` and `dependencies` fields are directly relevant to knowledge base design. `proficiencyLevel` maps to Dewey's depth concept. `dependencies` enables explicit prerequisite chains. The `speakable` property anticipates multi-modal consumption.

Source: [Schema.org TechArticle](https://schema.org/TechArticle) | [Schema.org Article](https://schema.org/Article)

### 6.4 JATS (Journal Article Tag Suite)

**Standard:** NISO Z39.96-2012, maintained by the National Library of Medicine.

**Three article models:**
1. **Archiving** (loose): For libraries/archives ingesting XML
2. **Publishing** (tighter): For publication production
3. **Authoring** (strictest): For article authors

**Article-meta structure:**

```xml
<article>
  <front>
    <journal-meta>
      <journal-id>...</journal-id>
      <journal-title-group>...</journal-title-group>
    </journal-meta>
    <article-meta>
      <article-id pub-id-type="doi">10.1234/example</article-id>
      <article-id pub-id-type="publisher-id">MS-2026-001</article-id>
      <title-group>
        <article-title>Title of the Article</article-title>
        <subtitle>Optional Subtitle</subtitle>
      </title-group>
      <contrib-group>
        <contrib contrib-type="author">
          <name><surname>Smith</surname><given-names>Jane</given-names></name>
          <aff>University of Example</aff>
        </contrib>
      </contrib-group>
      <pub-date publication-format="electronic">
        <day>16</day><month>02</month><year>2026</year>
      </pub-date>
      <abstract>
        <p>Summary of the article...</p>
      </abstract>
      <kwd-group>
        <kwd>keyword1</kwd>
        <kwd>keyword2</kwd>
      </kwd-group>
      <funding-group>...</funding-group>
    </article-meta>
  </front>
  <body>...</body>
  <back>
    <ref-list>...</ref-list>
    <app-group>...</app-group>
  </back>
</article>
```

**Key metadata elements:**
- `<article-id>` with `pub-id-type` attribute (doi, publisher-id, submission-id)
- `<title-group>` with article-title and subtitle
- `<contrib-group>` with typed contributors
- `<pub-date>` with publication-format attribute
- `<abstract>` (structured or unstructured)
- `<kwd-group>` for keywords
- `<funding-group>` for funding sources
- `<history>` with `<date>` elements for received, revised, accepted dates

**Key insight:** JATS is the most rigorous metadata standard for document provenance. The multi-date history tracking (received, revised, accepted), structured abstracts, and typed identifiers set the standard for traceability. The three model strictness levels (archiving, publishing, authoring) parallel Dewey's progressive validation tiers.

Source: [JATS](https://jats.nlm.nih.gov/) | [Introduction to JATS](https://www.xml.com/articles/2018/10/12/introduction-jats/) | [NISO JATS](https://www.niso.org/standards-committees/jats)

---

## 7. Synthesis: Implications for Dewey's Knowledge Base Record Format

### 7.1 Current Dewey Format Assessment

Dewey's current format (from `/Users/bbeidel/Documents/dewey/dewey/skills/curate/references/knowledge-base-spec-summary.md` and `/Users/bbeidel/Documents/dewey/dewey/skills/curate/scripts/templates.py`):

**Frontmatter fields:**
- `sources` (list of url + title)
- `last_validated` (date)
- `relevance` (text)
- `depth` (overview | working | reference)

**Working knowledge sections:**
- Why This Matters
- In Practice
- Key Guidance
- Watch Out For
- Go Deeper
- Source Evaluation

**Three depths:** overview, working, reference

### 7.2 What Each Standard Contributes

| Standard | Key Contribution to Knowledge Base Design |
|---|---|
| **Diataxis** | Content should be typed by purpose (learning, doing, understanding, looking up). Tutorial type is largely irrelevant for agents. |
| **EPPO** | Topics must be self-contained, establish their own context, conform to domain-specific types, and link richly. "Assume the reader is qualified." |
| **Information Mapping** | Six information types (procedure, process, principle, concept, structure, fact) provide richer taxonomy. Over 200 block types. Chunking, labeling, relevance principles. |
| **DITA** | Most comprehensive metadata model (prolog). Formal specialization for defining new topic types. Content reuse via conref/keyref. |
| **Zettelkasten** | One idea per note. Write for others. Rich linking. Unique identifiers. |
| **S1000D** | Most rigorous self-contained module pattern: metadata header + typed content body. Information codes for fine-grained classification. |
| **ASD-STE100** | Controlled vocabulary principles. Sentence length limits. "One word, one meaning." |
| **llms.txt** | Progressive disclosure via index -> individual pages. Markdown as interchange format. |
| **Dublin Core** | Subject, Description, Date, Type, Source, Relation as core metadata. |
| **Schema.org TechArticle** | `proficiencyLevel` and `dependencies` fields. `dateModified` distinct from `datePublished`. |
| **JATS** | Multi-date history (received, revised, accepted). Structured abstracts. Three strictness levels. |
| **PRISM** | `contentType` controlled vocabulary. Hierarchical subsections. |
| **kapa.ai/Redocly** | Self-contained pages. Consistent terminology. Contextual completeness per chunk. Proper heading hierarchy. |

### 7.3 Gaps in Dewey's Current Format

Based on this research, potential gaps include:

1. **Content type taxonomy:** Current three depths (overview, working, reference) conflate depth with type. Information Mapping's six types and DITA's five types suggest richer classification is possible.

2. **Dependencies/prerequisites:** Schema.org TechArticle has `dependencies`. DITA Task has `<prereq>`. Dewey has no formal prerequisite field.

3. **Audience/proficiency level:** DITA has `<audience>` with `experiencelevel`. Schema.org has `proficiencyLevel`. Dewey's depth field partially addresses this but doesn't separate audience from depth.

4. **Multiple dates:** JATS tracks received, revised, accepted. Dewey has only `last_validated`. Consider: `date_created`, `date_modified`, `last_validated` as separate fields.

5. **Structured relationships:** Dublin Core has `relation`, `isPartOf`, `hasPart`. DITA has relationship tables. Dewey has no formal relationship metadata beyond file-system hierarchy.

6. **Keywords/subject classification:** Dublin Core has `subject`. DITA has `<keywords>`. Dewey has no keywords field (relies on directory structure for classification).

7. **Self-containment verification:** EPPO's seven characteristics provide a quality checklist that could inform validators: Does this topic establish its own context? Does it stay on one level? Does it link richly?

8. **Controlled vocabulary:** ASD-STE100 principles (consistent terminology, sentence length limits) could inform writing rules or validators.

### 7.4 Cross-Cutting Patterns

Several patterns emerge consistently across all standards:

1. **Metadata header + typed body** (DITA prolog + body, S1000D identification + content, JATS front + body, Dewey frontmatter + sections) -- this is the universal pattern.

2. **Content typing** (DITA concept/task/reference, Diataxis tutorial/howto/reference/explanation, Information Mapping's six types, EPPO's domain-specific types) -- every standard types content, but they disagree on taxonomy.

3. **Self-containment** (EPPO, kapa.ai, Mintlify, S1000D data modules) -- every LLM-optimization guide emphasizes this.

4. **Progressive disclosure** (Diataxis across doc types, Dewey across depths, llms.txt index->pages, DITA maps->topics) -- universal pattern, implemented differently.

5. **Source provenance** (Dublin Core Source, DITA source, JATS references, Dewey sources field) -- tracking where content came from is universal.

6. **Freshness tracking** (Dublin Core Date, Schema.org dateModified, JATS history, Dewey last_validated) -- universal concern.
