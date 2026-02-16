<objective>
Ingest an external URL into the knowledge base by fetching the content, evaluating source quality, cross-validating claims, and either proposing new content or recommending updates to existing topics.
</objective>

<process>
## Step 1: Resolve URL and context from intake

The intake classifier identified a URL in the user's input. Extract:

- **URL** — the URL from the user's message
- **Topic name** — if the user mentioned a topic name, use it. Otherwise, infer from the page title after fetching.
- **Relevance** — default to `core` unless the user specified otherwise

Do NOT ask the user for information that can be inferred. Get moving quickly.

## Step 2: Fetch and analyze the source

Read AGENTS.md to understand the role context, then fetch the URL:

1. **Fetch the URL** using WebFetch. Extract the main content, stripping navigation, ads, and boilerplate.
2. **Identify key information** relevant to the role: concepts, guidance, examples, caveats, and authoritative claims.
3. If the URL is inaccessible (404, paywall, authentication required), inform the user and offer to record the URL for manual distillation later.

## Step 3: Evaluate the ingested source

Before checking knowledge-base overlap, evaluate the ingested URL itself. Consult `@dewey/skills/curate/references/source-evaluation.md` for full methodology details.

1. **Apply SIFT lateral reading:** Leave the source, search what others say about it and its author/organization.
2. **Score on five dimensions** (1-5 scale):

   | Dimension | 5 (highest) | 1 (lowest) |
   |-----------|-------------|------------|
   | Authority | RFC author, official docs maintainer | Anonymous blog, no credentials visible |
   | Accuracy | Peer-reviewed, claims with inline citations | Contains known errors, contradicts primary sources |
   | Currency | Updated within 6 months or covers stable topic | Outdated, explicitly superseded |
   | Purpose | Purely informational, no commercial interest | Primarily promotional or misleading |
   | Corroboration | Key claims confirmed by 3+ independent sources | Contradicted by other credible sources |

3. **Decision based on average score:**
   - **Average >= 3.5:** Proceed — strong source.
   - **Average 2.5-3.4:** Proceed with caveat — note quality concerns for the user.
   - **Average < 2.5:** Warn the user: "This source has quality concerns (average score X/5). Would you like to: (a) proceed anyway, (b) find a better source on this topic, or (c) record it as a low-confidence reference?"

Note the evaluation for inclusion in the provenance block later.

## Step 4: Evaluate against existing knowledge base content

Before proposing new material, check for overlap with what's already in the knowledge base:

1. **Scan existing topics** -- Read AGENTS.md manifest and browse knowledge base area directories to identify existing topics and their descriptions.
2. **Read overlapping topics** -- For any topic that covers related ground, read the working-knowledge file to understand what's already documented.
3. **Classify the source material** into one of three outcomes:

**Outcome A: New topic** -- The source covers material not addressed by any existing topic. Proceed to Step 5.

**Outcome B: Update existing topic(s)** -- The source adds new guidance, examples, or corrections to one or more existing topics. The source should be incorporated into those topics rather than creating a new one.

**Outcome C: Mixed** -- Some material is new and some overlaps. The new material warrants a proposal; the overlapping material should update existing topics.

Present the evaluation to the user:

"After reviewing the source against the existing knowledge base, here's what I found:

- **Overlapping topics:** [list any existing topics that cover similar ground, with a brief note on what overlaps]
- **New material:** [describe what the source contributes that isn't already covered]
- **Recommendation:** [New topic / Update existing / Mixed]

How would you like to proceed?"

Wait for the user to confirm the approach before continuing.

## Step 5: Search for and evaluate related sources

### 5.1 Discover additional sources

Search for 3-5 additional candidate sources using the source hierarchy from `source-evaluation.md`. The ingested URL counts as one source. Use the search techniques from that reference: site-scoped searches (`site:docs.python.org`), quoted exact terms, recency filtering for fast-moving domains, and author-focused searches for known experts.

### 5.2 Evaluate each source

Apply SIFT lateral reading + 5-dimension scoring (same rubric as Step 3) to each candidate. Include (average >= 3.5), include with caveat (2.5-3.4), or exclude (< 2.5).

### 5.3 Counter-evidence search

Actively search for contradicting perspectives:

- `"problems with <topic>"`, `"limitations of <topic>"`
- `"<topic> considered harmful"`, `"alternatives to <topic>"`

If credible counter-evidence is found, note it for inclusion in Watch Out For or as qualifying language. If none is found, note as a positive signal.

**Target:** 3-5 total included sources (including the ingested URL) from 2+ independent organizations.

## Step 6: Draft content

Based on the user's chosen approach from Step 4:

### If creating a new proposal (Outcome A or new portion of C):

Distill the fetched content and related sources into the working-knowledge template:

- **Why This Matters** -- Causal reasoning: what problem this solves, why this approach. Drawn from the source's introduction or motivation sections.
- **In Practice** -- A concrete, worked example applied realistically. Use examples from the source or construct one based on the source's guidance.
- **Key Guidance** -- Actionable recommendations with inline source citations. Each recommendation should reference the specific source: `([Source Title](url))`.
- **Watch Out For** -- Common mistakes, edge cases, or caveats mentioned in the source. Include counter-evidence findings from Step 5.3.
- **Go Deeper** -- Links to the original ingested URL and all related sources found.

Calibrate confidence language to source consensus:

| Source Agreement | Language |
|-----------------|----------|
| >80% agree | State as fact |
| 50-80% agree | Use "generally" or "typically" |
| 30-50% agree | Use "some evidence suggests" |
| <30% agree | Present competing views or omit |

Also draft **reference companion** content:
- Terse, scannable quick-lookup version of the key guidance (tables, lists, quick rules)

### If updating existing topics (Outcome B or overlapping portion of C):

For each existing topic to update, draft:
- Specific additions or revisions to each section (Key Guidance, Watch Out For, etc.)
- New source to add to the frontmatter `sources:` field
- Any corrections to existing content based on the new source
- Qualifying language adjustments based on consensus level

### Step 6.5: Build Source Evaluation section

After drafting, add a `## Source Evaluation` section:

1. **Visible summary table:**

   ```markdown
   | Source | Authority | Accuracy | Currency | Purpose | Corroboration | Decision |
   |--------|-----------|----------|----------|---------|---------------|----------|
   | [Title](url) | 4 | 5 | 4 | 5 | 4 | include |
   ```

2. **Counter-evidence summary:** One line describing what was searched for and what was found.

3. **Hidden provenance block:** `<!-- dewey:provenance { ... } -->` JSON with full structured data (see `source-evaluation.md` for format specification).

## Step 7: Cross-validate draft

Before presenting to the user, verify that the draft accurately reflects its sources.

### 7.1 Decompose key claims

Extract factual and recommendation claims from Key Guidance and Watch Out For. Break compound claims into atomic, verifiable statements (one assertion each). Skip subjective judgments.

### 7.2 Triangulate each claim

For each claim, check support from 2+ evaluated sources. Track whether each source supports, partially supports, or contradicts the claim.

### 7.3 Calibrate confidence language

Verify that the draft language matches the consensus level from Step 6. Adjust overconfident claims (e.g., stating a weakly-supported claim as fact) and under-confident claims (e.g., hedging a universally-agreed point).

### 7.4 Record cross-validation results

Add cross-validation results to the `<!-- dewey:provenance -->` block: total claims verified, consensus breakdown, and any claims modified or removed during verification.

## Step 8: Present draft for review

Present the complete draft (new proposal and/or proposed updates to existing topics) to the user with a source quality summary:

> "This draft draws on N sources (average authority X/5). M of N key claims are supported by 2+ independent sources."

For each section, note which source(s) informed it. Ask: "Does this capture the key information from the source? Should I adjust anything?"

The human brings domain judgment. Accept their edits and corrections. If they approve, proceed. If they have changes, revise and re-present.

## Step 9: Create proposal or apply updates

### For new proposals:

Run the propose script:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/curate/scripts/propose.py --knowledge-base-root <knowledge_base_root> --topic "<topic_name>" --relevance "<relevance>" --proposed-by "ingest" --rationale "Ingested from: <url>"
```

Then update the proposal file:
1. Replace template placeholder sections with the drafted content
2. Update frontmatter `sources:` with all sources:

```yaml
sources:
  - url: https://docs.example.com/guide
    title: "Example Guide -- Official Docs"
  - url: https://related-source.com/article
    title: "Related Article"
```

### For updates to existing topics:

Present the proposed edits to each existing topic file, showing what would change. Do NOT apply edits until the user approves.

Report what was done:

**If a new proposal was created:**
"The proposal has been created at `<knowledge-dir>/_proposals/<slug>.md` with content distilled from the source. Next steps:
1. **Validate** -- Use `/dewey:health check` to run quality validators
2. **Promote** -- Use `/dewey:curate promote <slug> --target-area <area>` to move it into a domain area"

**If existing topics were updated:**
"The following topics were updated with new material from `<url>`:
- `<knowledge-dir>/<area>/<topic>.md` -- [brief description of changes]
The source has been added to each topic's frontmatter."

## Step 10: Update curation plan

If `.dewey/curation-plan.md` exists, check for an item matching the topic name just created or updated (case-insensitive match on the name portion before ` -- `). If found, mark it as done by changing `- [ ]` to `- [x]`. Update `last_updated` in the frontmatter to today's date.
</process>

<success_criteria>
- Source URL fetched and content analyzed
- Ingested source evaluated using 5-dimension rubric
- Existing knowledge base scanned for overlap -- evaluation presented to user before drafting
- User confirmed whether to create new content, update existing, or both
- At least 3 total sources (including ingested URL) from 2+ independent organizations
- Counter-evidence search performed and documented
- Key claims cross-validated against 2+ sources
- Confidence language calibrated to consensus level
- Source Evaluation section present with visible table and `<!-- dewey:provenance -->` block
- For new proposals: content filled in (not template placeholders), source URL in frontmatter
- For existing topic updates: changes applied with new source added to frontmatter
- Content reviewed and approved by the user before any writes
</success_criteria>
</output>
