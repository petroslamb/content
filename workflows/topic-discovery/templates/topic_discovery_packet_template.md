# Topic Discovery Packet

## Trigger

- Seed question:
- Trigger type: `<archive_gap/external_event/research_frontier/review_finding/post_ceiling_successor>`
- Target ambition: `<note/strong_synthesis/north_star_flagship>`
- Relevant prior essays or packages:

## 01. Topic Vocabulary

Record the exact search commands and what they revealed.

| Query | Command | Useful Topics | Noisy Topics | Decision |
| :--- | :--- | :--- | :--- | :--- |
| `<query>` | `<alphaxiv command>` | `<topic slugs>` | `<topic slugs>` | `<keep/drop/fallback>` |

Decision:

- Primary topic surfaces:
- Broad recall surfaces:
- Dropped surfaces:
- Why:

## 02. Feed Candidates

Use multiple imperfect ranking surfaces instead of trusting one list.

| Surface | Command | Candidates That Recurred | Noise / Caveat |
| :--- | :--- | :--- | :--- |
| hot | `<command>` | `<paper ids>` | `<caveat>` |
| likes | `<command>` | `<paper ids>` | `<caveat>` |
| GitHub stars | `<command>` | `<paper ids>` | `<caveat>` |
| broad baseline | `<command>` | `<paper ids>` | `<caveat>` |

Primary inspection pool:

- `<paper id>`: `<reason>`

Near-misses:

- `<paper id>`: `<why not yet>`

## 03. Paper Inspection

For each serious paper, inspect deterministic surfaces before synthesis.

### `<paper id>` `<title>`

Commands:

```bash
.venv/bin/alphaxiv paper show <paper-id>
.venv/bin/alphaxiv paper abstract <paper-id>
.venv/bin/alphaxiv paper summary <paper-id>
.venv/bin/alphaxiv paper resources <paper-id>
.venv/bin/alphaxiv paper similar <paper-id> --limit 5
```

What mattered:

- 

Essay-object role:

- `<direct_anchor/adjacent/enabling/near_miss/drop>`

Decision:

- `<keep/drop/provisional>`

## 04. Assistant Synthesis

Use assistant only after retrieval and inspection.

Prompt:

```text
Compare these papers: <ids>. Rank them by importance for <specific research question>.
Explain the ranking in terms of novelty, practical impact, likely lasting relevance,
and what essay object each paper could support.
```

What changed:

- 

What did not change:

- 

## 05. Essay-Object Slate

| Candidate | One-Sentence Promise | Public Enemy / False Proxy | Evidence Already Present | Evidence Delta | Kill Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `<candidate>` | `<promise>` | `<proxy>` | `<sources>` | `<gaps>` | `<kill criteria>` |

Scores are advisory.

| Candidate | Debate Gain | Aperture Gain | Doctrine Utility | Opening Power | Synthesis Headroom | Evidence Maturity | Read |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `<candidate>` |  |  |  |  |  |  | `<lead/provisional/park/block>` |

## 06. Handoff Decision

Choose exactly one:

- `package_init_ready`
- `research_delta_needed`
- `post_ceiling_pivot`
- `intake_ready`
- `parked`
- `blocked`

Decision:

Rationale:

Carry-forward package idea if ready:

- Proposed slug:
- One-sentence promise:
- Initial paper shortlist:
- Near-misses and blocked framings:
- First research question:
- Expected evidence surface:

## Negative Evidence

Record failed searches and demotions.

- 

## Next Action

One concrete next action:

- 
