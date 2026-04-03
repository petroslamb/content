# The Binding Gap Blueprint

This file is the pre-draft control artifact for the new flagship essay. It is not essay prose. Its job is to lock the narrow thesis, the source roles, and the argument shape before drafting.

Status: active control document for the binding-gap flagship.

## Locked Identity

Title: `The Binding Gap`

Audience: technical public

Essay type: flagship ideas essay

Word target: `1,700-2,200` words excluding references

## Locked Thesis

Current language models exhibit a distinct, high-consequence family of binding-sensitive failures: they can preserve relevant semantic material while losing the exact role, source, or numeric attachment needed for faithful use when task demands change.

Main term: `binding gap`

Supporting term: `exact binding`

Working definition:

`binding gap`
: a failure where the model retains enough semantic material to sound near-correct, but loses the exact attachment that makes the answer usable when the task requires inversion, reassignment, attribution, or precise reconstruction.

`exact binding`
: stable attachment of content to the role that makes it actionable:
  - who did what to whom
  - which number belongs to which variable
  - which source supports which sentence

What the essay must make clear:

- broad semantic content can survive while exact relational attachment fails
- this failure can look like near-correctness rather than blank ignorance
- this is a bounded family claim, not a master theory of model failure
- the failure scales from a toy diagnostic into serious knowledge work
- the consequence is architectural and evaluative, not merely rhetorical

What the essay must distinguish the term from:

- pure absence: the model never had the relevant content in usable form
- retrieval miss: the right evidence never entered the working context
- decomposition failure: the system chose the wrong subtask path
- generic hallucination: the output drifts without the characteristic attachment failure
- generic downstream use failure: retrieved or available content is ignored rather than misbound

Minimal test for a true binding-gap case:

- the parts are present enough that the answer feels close
- the failure appears when exact role or source attachment becomes necessary
- changing task form exposes the weakness more clearly than changing topic
- the mistake is not best explained by missing retrieval alone

## Explicitly Out Of Scope

Do not let the essay become:

- a structural-recoverability essay
- an `encoded / recoverable / expressed` essay
- a broad hallucination theory
- a theory of "many model failures"
- a compression essay
- a hidden-knowledge / probing essay
- a language-vs-latent-format coequal thesis
- a survey of interpretability or knowledge-editing work

What stays in scope only if it directly serves the main term:

- attribution
- retrieval
- format choice
- provenance-aware training

Pre-draft risk:

- the Tan and D'Souza extension has to scale the argument into serious knowledge work without turning into a mini-survey of meta-analysis extraction

## Source Roles

`2504.01928` Wang and Sun

- opening anchor
- main mechanistic paper
- supplies the Reversal Curse and the binding frame

`2310.17191` How do Language Models Bind Entities in Context?

- bridge paper
- shows binding is a real, causally manipulable internal mechanism rather than a loose metaphor
- use to move from toy reversal failure to general entity-attribute binding

`2409.05448` Representational Analysis of Binding in Language Models

- bridge paper
- sharpens the mechanism with ordering IDs and causal patching
- use only to strengthen the claim that attachment is representationally real

`2504.16884` Do Large Language Models know who did what to whom?

- sentence-level bridge
- moves from entity-attribute binding to thematic roles
- important because it shows role information exists but influences overall representations weakly

`2511.20910` Emergence and Localisation of Semantic Role Circuits in LLMs

- sentence-level bridge
- supports the claim that semantic-role circuitry is compact and causally localised
- use to connect role assignment to a plausible mechanism without overclaiming robustness

`2602.10881` Tan and D'Souza

- main serious extension
- one paragraph only
- its role is to show the same failure shape under heavier structural load

`2410.14405` Saynova et al.

- discipline section
- blocks the move from correct output to genuine knowledge
- one short section, not a detour into interpretability

`2603.03541` RAG-X

- one compressed supporting paragraph only
- use to distinguish retrieval miss from downstream use failure
- important because the binding-gap essay needs a border test, not just a positive case

`2603.11513` Can Small Language Models Use What They Retrieve?

- same compressed supporting paragraph as RAG-X if helpful
- use to show that not every failure after retrieval is a binding-gap failure
- helps narrow the term rather than broaden it

Optional supporting material only if needed:

- `2410.02707` Orgad et al.
- `2310.06816` Morris et al.
- `2506.17585` Xie et al.

## Argument Spine

### 1. Symptom

- Open on the Reversal Curse
- Same content, different role assignment, sharp failure
- Make the failure feel diagnostic, not anecdotal

### 2. Concept

- Introduce `the binding gap`
- Define it in one sentence before naming adjacent theories
- Make clear that the issue is not missing pieces alone, but missing attachment
- Define exact binding concretely:
  - who did what to whom
  - which number belongs to which variable
  - which source supports which sentence
- Briefly reject two bad pictures:
  - model-as-library
  - hidden-state-decoding settles everything

### 3. Bridge

- Move from the Reversal Curse into binding as a real internal phenomenon
- Use entity-attribute binding and ordering-ID work to show that attachment is mechanistically meaningful
- Then move from entity binding to semantic roles:
  - who did what to whom
  - role information can exist locally while remaining weakly integrated at the sentence level
- The aim is to earn the term before scaling it outward

### 4. Scaling

- Move from Reversal Curse to evidence extraction / meta-analysis
- Show that the same failure shape appears under heavier structural load
- Make the bridge explicit:
  - reversal failure is exact binding under minimal transformation
  - role assignment is exact binding at sentence level
  - extraction failure is exact binding under dense local structure
- The point is not benchmark tourism
- The point is that the toy case scales into serious knowledge work

### 5. Discipline And Borders

- Use Saynova to block the move from correct output to genuine knowledge
- Use RAG-X and retrieval-utilization work to show that retrieval miss and use failure are diagnosable neighboring classes
- State plainly that not every downstream failure is a binding-gap failure
- Keep this section short
- Its job is to sharpen the claim, not widen the essay

### 6. Consequences And Wager

- Draw the consequence for attribution, retrieval, and format:
  - they matter when they help preserve attachment
- Any consequence that cannot be phrased in attachment terms gets cut
- End with a wager:
  - binding-heavy tasks should fail earlier than broad topical tasks
  - interventions that protect role stability, source attachment, or numeric grounding should help there before they help generic fluent output

## Drafting Rules

- Write from a blank page
- Use prose, not list-heavy body structure
- Keep only two heavy concepts:
  - `binding gap`
  - `exact binding`
- Use Reversal Curse as the emotional and conceptual anchor
- Use semantic-role work as the bridge and meta-analysis extraction as the serious extension
- Keep the consequence section compact
- Do not introduce a second master term to rescue the concept
- Do not use the recoverability diagram
- Do not rely on the structural-recoverability vocabulary except at most one supporting sentence if absolutely necessary
- Do not repeat the `X is not Y. It is Z.` rhythm
- Do not let the last section turn into a bigger theory than the essay can earn

## Quality Bar

The draft passes only if:

- the first three paragraphs establish the symptom, the term, and why it matters
- a reader can summarize the thesis after the first third without using `recoverability`
- a reader can tell the difference between a binding-gap failure and a retrieval miss
- a reader can tell the difference between a binding-gap failure and generic downstream use failure
- the Reversal Curse still feels like the engine, not just the hook
- the bridge from entity binding to semantic-role binding feels necessary rather than decorative
- a reader can explain the difference between topical competence and exact binding by the middle of the essay
- the Tan and D'Souza case makes the idea feel larger and more serious, not narrower
- the border section disciplines the thesis instead of widening it
- the last section contains a clear wager, not just implications
- removing the consequence section would make the essay weaker, not stronger
- no unresolved master-theory ambition survives in the closing section
- the essay leaves the reader with a reusable sentence-level lens, not just an interesting paper pair
