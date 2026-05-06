---
workflow_id: topic_discovery
workflow_kind: module
stability: canonical
workflow_group: portfolio
runner_mode: guided
default_skill: alphaxiv
launch_templates: []
packet_templates:
  - "workflows/topic-discovery/templates/topic_discovery_packet_template.md"
required_context:
  - seed question, archive gap, external trigger, review finding, or broad domain to investigate
  - relevant prior essays or archive cluster when the topic should build on existing work
  - target publication ambition, such as quick note, strong synthesis, or north-star flagship
expected_outputs:
  - topic vocabulary map for the research surface
  - ranked candidate paper pool with exclusions and near-misses
  - tracked assistant discussion notes when assistant comparison shapes the topic decision
  - candidate essay slate with evidence deltas and kill criteria
  - handoff decision to package initialization, post-ceiling pivot, narrower research, or parking
done_when:
  - the repo has an explicit decision about whether the topic deserves a package, pivot pass, or no further work, and any material assistant discussion is recoverable from the discovery packet or successor package
approval_gate: required_before_package_init
---

# Topic Discovery

This is the tracked pre-package workflow for finding and testing potential essay topics before a publication package exists, or before an existing package absorbs a new research seam.

Use this workflow when the question is:

- what should the next essay be?
- which recent research seam is actually important?
- does this broad idea deserve a package?
- did a capped essay leave behind a stronger successor topic?

Do not use it as a substitute for [`../alphaxiv-research/README.md`](../alphaxiv-research/README.md). alphaXiv research is the execution layer. Topic discovery is the editorial decision layer above it.

## Where It Sits

The repo now has three different early-stage decisions. Keep them separate:

| Layer | Question | Typical Output |
| :--- | :--- | :--- |
| topic discovery | is there a real essay topic here? | topic map, candidate pool, essay-object slate |
| alphaXiv research | which papers support or challenge the active question? | shortlist and paper-level inspection |
| paper intake | which selected papers enter the package evidence surface? | PDFs, markdown conversions, paper index |

For a greenfield essay, topic discovery runs before `package:init`.

For a capped essay, topic discovery usually appears inside [`../post-ceiling-pivot/README.md`](../post-ceiling-pivot/README.md), where the donor package already exists and the question is whether a successor object should be opened.

## Core Rule

Separate **topic selection**, **candidate selection**, and **candidate clearance**.

A topic can be interesting without being an essay. A candidate essay can be supported by papers without being a north-star object. A research seam can be valuable without deserving a package now.

The default order is:

1. map the research vocabulary
2. build a candidate paper pool
3. inspect papers deterministically
4. use the assistant only after retrieval
5. form candidate essay objects
6. rank candidates against ambition and evidence
7. decide the handoff

## Discovery Modes

### Greenfield Topic Discovery

Use this when there is no package yet and the prompt is a broad domain, trend, paper cluster, or question.

The strongest recovered example is the `illusion-of-swarm` alphaXiv pass:

- [`../../publications/illusion-of-swarm/01-topic-discovery.md`](../../publications/illusion-of-swarm/01-topic-discovery.md)
- [`../../publications/illusion-of-swarm/02-feed-candidates.md`](../../publications/illusion-of-swarm/02-feed-candidates.md)
- [`../../publications/illusion-of-swarm/03-paper-inspection.md`](../../publications/illusion-of-swarm/03-paper-inspection.md)
- [`../../publications/illusion-of-swarm/04-assistant-synthesis.md`](../../publications/illusion-of-swarm/04-assistant-synthesis.md)
- [`../../publications/illusion-of-swarm/05-final-shortlist.md`](../../publications/illusion-of-swarm/05-final-shortlist.md)

That run used a repeatable pattern:

1. translate natural language into alphaXiv topic vocabulary
2. compare narrow topics against broader feed surfaces
3. use multiple ranking proxies such as hot, likes, and GitHub stars
4. inspect candidate papers one by one
5. ask the assistant to compare an already-inspected shortlist
6. track material assistant sessions before they disappear into remote history
7. preserve near-misses so the decision is not rediscovered later

### Post-Ceiling Topic Discovery

Use this when an existing essay hit a frame ceiling but still contains reusable evidence, openings, concepts, or doctrine.

The strongest recovered example is the `clean-interface-illusion` process capture:

- [`../../publications/clean-interface-illusion/clean-interface-illusion-process-capture.md`](../../publications/clean-interface-illusion/clean-interface-illusion-process-capture.md)
- [`../../publications/clean-interface-illusion/clean-interface-illusion-pivot-slate.md`](../../publications/clean-interface-illusion/clean-interface-illusion-pivot-slate.md)
- [`../../publications/clean-interface-illusion/clean-interface-illusion-pivot-grounding-review.md`](../../publications/clean-interface-illusion/clean-interface-illusion-pivot-grounding-review.md)

In that mode, use [`../post-ceiling-pivot/README.md`](../post-ceiling-pivot/README.md) as the governing workflow. This topic-discovery workflow supplies the reusable search-first discipline.

## Canonical Flow

### 1. State The Discovery Trigger

Write the trigger before searching.

Good triggers:

- a broad research frontier: `multi-agent systems`
- an archive gap: `we have benchmarks and governance but no human oversight layer`
- an external review finding: `the essay is precise but not provocative`
- a capped frame: `benchmark interpretation cannot carry the human stakes`
- a public event or paper release that might expose a deeper structural pattern

Bad triggers:

- `find something interesting`
- `get more papers`
- `make the existing essay bigger`
- `the candidate sounds good`

For governed Phase 2 runs, pass the trigger and ambition as runtime inputs rather than burying them in prose:

```bash
./content-agent validate --workflow topic_discovery --package <package> --input discovery_trigger="<bounded trigger>" --input target_publication_ambition=north_star_flagship
./content-agent run --workflow topic_discovery --package <package> --input discovery_trigger="<bounded trigger>" --input target_publication_ambition=north_star_flagship
```

### 2. Map The Vocabulary

Do not assume the natural-language phrase is the right research surface.

Use alphaXiv to discover topic and feed vocabulary before ranking papers:

```bash
.venv/bin/alphaxiv feed filters search "<natural-language topic>"
.venv/bin/alphaxiv search topics "<natural-language topic>"
.venv/bin/alphaxiv search papers "<natural-language topic>"
```

Record:

- exact topic slugs that look useful
- broad adjacent topics that may have higher recall
- topics that looked plausible but were too noisy
- organizations only if they materially improve discovery

Output this as a topic vocabulary map, not as a prose memo.

### 3. Build The Candidate Pool

Use multiple ranking surfaces. One feed sort is not enough.

For recent paper discovery, a good default is:

```bash
.venv/bin/alphaxiv feed list --interval 90-days --topic <topic-slug> --sort hot --limit 10
.venv/bin/alphaxiv feed list --interval 90-days --topic <topic-slug> --sort likes --limit 10
.venv/bin/alphaxiv feed list --interval 90-days --source github --topic <topic-slug> --sort most-stars --limit 10
```

Also run a broad baseline when the narrow topic may miss important papers:

```bash
.venv/bin/alphaxiv feed list --interval 90-days --sort hot --limit 20
.venv/bin/alphaxiv feed list --interval 90-days --sort likes --limit 20
.venv/bin/alphaxiv feed list --interval 90-days --source github --sort most-stars --limit 20
```

The goal is not to trust popularity. The goal is to see which papers recur across multiple imperfect proxies.

### 4. Inspect Papers Before Synthesis

For each serious candidate, inspect deterministic surfaces first:

```bash
.venv/bin/alphaxiv paper show <paper-id>
.venv/bin/alphaxiv paper abstract <paper-id>
.venv/bin/alphaxiv paper summary <paper-id>
.venv/bin/alphaxiv paper resources <paper-id>
.venv/bin/alphaxiv paper similar <paper-id> --limit 5
```

Record:

- why the paper matters
- which essay object it could support
- whether it is direct, adjacent, enabling, or a near-miss
- what would make it load-bearing
- why it should be dropped if it is dropped

Do not download or intake every plausible paper. Promote only papers that materially change the candidate decision.

### 5. Use The Assistant As A Comparator

Use the alphaXiv assistant only after retrieval and inspection.

Good assistant prompt shape:

```text
Compare these papers: <ids>. Rank them by importance for <specific research question>.
Explain the ranking in terms of novelty, practical impact, likely lasting relevance,
and what essay object each paper could support.
```

Bad assistant prompt shape:

```text
Find me a great topic.
```

Ask fresh, short comparison questions. If a session gets slow or unfocused, start a new one and carry forward only the paper IDs and decision question.

### 5.5 Track Material Assistant Discussions

If an assistant session changes the topic decision, candidate ranking, vocabulary, or package handoff, record it before moving on.

When no package exists yet, put the session id, title, date, and compact extraction in the topic-discovery packet or in the `*-assistant-synthesis.md` file. When the topic becomes a package, copy or move the distilled session into the successor package's `research-notes/alphaxiv-discussions/` index.

Do not track every assistant chat. Track sessions that changed the decision or produced a useful contradiction.

Useful commands:

```bash
.venv/bin/alphaxiv assistant list --json --limit 100
.venv/bin/alphaxiv assistant history <session-id>
```

For the package-local extraction shape, use [`../alphaxiv-research/templates/assistant-discussion-extraction.md`](../alphaxiv-research/templates/assistant-discussion-extraction.md).

### 6. Produce An Essay-Object Slate

Topic discovery should not stop at a paper list. Convert the paper pool into candidate essay objects.

For each candidate, record:

- object type
- one-sentence promise
- public enemy or false proxy it attacks
- what evidence already supports it
- evidence delta needed
- why it could matter now
- kill criteria
- likely package shape: new package, existing package, pivot, note, or parked idea

Use these scoring axes by default:

- `Debate gain`: how much argument or disagreement the object creates
- `Aperture gain`: how much territory opens beyond the seed question
- `Doctrine utility`: how clearly the object changes operator behavior
- `Opening power`: whether the evidence yields a memorable concrete start
- `Synthesis headroom`: whether the paper set can combine without becoming a survey
- `Evidence maturity`: whether the largest likely claim has enough support

Scores are advisory. The written rationale matters more than the arithmetic.

### 7. Decide The Handoff

End with one explicit decision:

| Decision | Meaning | Next Surface |
| :--- | :--- | :--- |
| `package_init_ready` | the topic has a clear enough object to become a package | `npm run package:init -- --idea "..."` |
| `research_delta_needed` | one candidate leads but has exact gaps to close | candidate-specific research delta |
| `post_ceiling_pivot` | the topic is a successor to a capped package | [`../post-ceiling-pivot/README.md`](../post-ceiling-pivot/README.md) |
| `intake_ready` | selected papers belong in an existing package | [`../paper-intake/README.md`](../paper-intake/README.md) |
| `parked` | interesting but not actionable now | local topic ledger or package notes |
| `blocked` | the decisive seam failed | blocker note with negative evidence |

Do not initialize a package just because the search found good papers. Initialize only when there is a coherent essay object or a clear reason to preserve the topic as a package.

## Required Output Shape

For a lightweight pass, a single markdown file is enough:

```text
topic-discovery.md
<slug>-topic-discovery.md
```

Use [`templates/topic_discovery_packet_template.md`](templates/topic_discovery_packet_template.md) when a weaker model needs the full packet shape in one file.

For a serious greenfield pass, use the recovered `illusion-of-swarm` pattern:

```text
01-topic-discovery.md
02-feed-candidates.md
03-paper-inspection.md
04-assistant-synthesis.md
05-final-shortlist.md
```

If the assistant synthesis materially changes the decision, `04-assistant-synthesis.md` should include the alphaXiv session id and a compact extraction. If the pass initializes a package, add the distilled session to the package-local `research-notes/alphaxiv-discussions/` index.

For a post-ceiling pass, use the artifact set in [`../post-ceiling-pivot/README.md`](../post-ceiling-pivot/README.md).

## Negative Evidence Rules

Negative discovery results count.

Record:

- empty searches on the decisive term
- topic slugs that returned mostly off-target work
- papers that looked important but failed direct relevance
- assistant comparisons that demoted the attractive candidate
- missing evidence that would be required for the largest claim

A near-empty search on the decisive missing layer is not "nothing happened." It is evidence that the candidate may be premature or should be narrowed.

## Common Failure Modes

### Popularity Becomes Importance

Feed rankings are signals, not verdicts. A highly starred adjacent paper may be less useful than a quieter paper that directly changes the essay's frame.

### The Assistant Invents The Topic

The assistant can compare and pressure-test. It should not be the first retrieval layer.

### Topic Becomes Survey

If the only possible output is "recent papers in X," the topic has not become an essay object yet. Look for a false proxy, a field-reordering distinction, or a doctrine with consequence.

### The Package Opens Too Early

Do not scaffold a package before the handoff decision is explicit. A package should preserve a real object, not a vague intention to research more.

### The Old Essay Secretly Continues

After a ceiling, do not use topic discovery to justify another local rewrite of the capped frame. Either find a successor object or preserve the old essay as a donor.

## Handoff To Package Init

When the decision is `package_init_ready`, carry forward:

- proposed slug
- one-sentence promise
- target audience
- initial paper shortlist
- near-misses and blocked framings
- first research question
- expected evidence surface
- whether this is a greenfield package or successor to an existing donor

Then initialize the package:

```bash
npm run package:init -- --idea "<one-sentence package idea>" --format json
```

After initialization, continue with:

1. [`../alphaxiv-research/README.md`](../alphaxiv-research/README.md) for any remaining shortlist validation
2. [`../paper-intake/README.md`](../paper-intake/README.md) once papers are selected
3. [`../essay-iteration/README.md`](../essay-iteration/README.md) once the package has a governing blueprint or live draft surface

## Promotion Read

This workflow is tracked and usable, but it should remain a pre-package decision layer rather than a default `status.yaml` lifecycle stage until the repo has at least two more successful topic-discovery runs with clean handoffs.
