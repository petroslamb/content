# Distribution Plan R3

## Package

- Package: `literate-workflow-programming/specification-surface-source-of-truth`
- Revision: 3
- Canonical post: `https://lambpetros.substack.com/p/the-specification-surface-is-the`
- Date: 2026-05-04

## Channel Plan

| Channel | Decision | Reason |
| :--- | :--- | :--- |
| Substack post | Complete | Canonical public essay is live and has been repaired from the repo markdown, including rhythm repair, author-year body citations, and linked h4 arXiv reference headings. |
| Tracked archive and mirror | Complete | Archive sync added the post, refreshed the reference-format pass, and mirror validation passed. |
| YouTube longform | Complete | The visual deep research dive is public and links back to the essay. |
| YouTube TL;DR | Complete | The compact explainer is public and cross-links to the essay and longform. |
| YouTube cinematic | Complete | The cinematic brief is public and links to the essay plus full research breakdown. |
| YouTube Shorts | Queued | Four Shorts are uploaded, scheduled, playlisted, and linked to the longform. |
| Substack Notes | Deferred | No separate note is needed for this closeout beyond the corrected post itself. |
| LinkedIn | Deferred | A platform-specific business framing can be prepared later if the essay needs a second wave. |
| Hacker News | Deferred | The piece is conceptual and research-synthesis heavy; no HN-specific submission is planned for this stage. |
| Reddit | Deferred | No subreddit-specific version is prepared; avoid posting without community-specific framing. |
| X | Deferred | No short thread is needed for the workflow closeout. |

## Copy Source

All downstream copy should start from the live Substack URL, not from an older draft:

```text
https://lambpetros.substack.com/p/the-specification-surface-is-the
```

## Completion Standard

Distribution is complete when the live essay, archive, mirror, YouTube longform, TL;DR, cinematic brief, and scheduled Shorts are recorded, and all skipped text-social channels are explicitly deferred.

## Second-Wave Distribution Pass

Date: 2026-05-04

Decision posture: selective push. Post only to channels with strong fit and low moderation risk; keep risky channels as prepared local drafts.

| Channel | Auth state | Decision | Fit | Risk | Execution note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Substack Notes | Signed in | `post_now` | Strong fit for the existing subscriber and Substack reader graph. | Low. Native channel for the canonical post. | Posted after action-time confirmation; live link rendered as a video/link preview card. |
| LinkedIn personal profile | Signed in | `manual_upload_required` | Strong fit for engineering operators, founders, and AI systems readers. A native document carousel is the preferred surface because LinkedIn tends to reward swipeable PDFs more than link-only previews. | Low to medium. Keep it professional, not promotional. Uploading the PDF is an outbound file transfer and requires action-time confirmation. | Browser attempt reached the Create post modal and `Add media`, but LinkedIn exposed no automatable file input; the PDF carousel requires manual file selection. Link-preview-only remains a fallback, not the target. |
| X | Signed in | `post_now` | Low follower count makes pure broadcast weak, but an anchor post is still useful as a reference object for replies, quotes, and later targeted engagement. | Medium. Fast feed, weak follower graph, and low context mean the post should not be judged by immediate follower reach. | Post a compact single anchor post, then use it selectively in relevant conversations rather than relying on organic broadcast. |
| Hacker News | Signed in | `post_now` | Possible fit for software-engineering discussion if framed as a genuine `Ask HN` question rather than a Substack submission. | Medium. HN still dislikes promotional use, so omit the URL and make the submission curiosity-first. | Submit a text-only `Ask HN` discussion after action-time confirmation. Link only if discussion asks for context. |
| Reddit | Signed in | `post_now_native_discussion` | Subreddit-dependent fit only. | High because current account posts appear to wait for mod approval, and Substack links in post bodies increase removal risk. | Post the subreddit-specific native discussion without the Substack URL in the body. Do not create a new account to bypass moderation; hold any link as an optional comment only after separate confirmation, if at all. |

### Substack Notes Copy

```text
AI-assisted software work has a hidden authority problem: generated code is visible, but the intent that governed it often is not.

I wrote about “specification surfaces”: maintained artifacts that teams and tools can read, validate, trace, and repair.

https://lambpetros.substack.com/p/the-specification-surface-is-the
```

### LinkedIn Personal Profile Copy

Preferred media:

```text
publications/literate-workflow-programming/specification-surface-source-of-truth/artifacts/slides/specification_surface_slides_set2.pdf
```

Document title:

```text
The Specification Surface Is the New Source of Truth
```

Carousel post copy:

```text
AI-assisted software work has a source-of-truth problem.

The generated diff is visible. The tests are visible. The summary is visible.

But the intent that governed the work often sits in a prompt, a chat thread, or a reviewer’s memory.

That makes the team review downstream artifacts while the controlling authority stays outside the governed system.

I call the missing artifact a specification surface: a maintained surface that teams and tools can read, validate, trace, and repair.

The carousel lays out the argument: why vibe coding fails as a control model, how specification gaps break multi-agent work, and what a governable PR review should ask before accepting agent-written code.
```

Optional link comment, not required for the post body:

```text
Full essay: https://lambpetros.substack.com/p/the-specification-surface-is-the
```

Previous link-forward fallback copy:

```text
The hidden problem in AI-assisted software work is not just trust in the model. It is authority.

A generated diff can look plausible. Tests can pass. The summary can sound coherent. But if nobody can point to the maintained statement of what the agent was supposed to preserve, what was out of scope, and which constraints mattered, the team is reviewing the downstream artifact while the controlling intent stays outside the governed system.

I call the missing artifact a specification surface: a maintained surface that teams and tools can read, validate, trace, and repair.

The essay connects spec-driven development, multi-agent coordination failures, agent harnesses, executable instruction constraints, and trace audit into one argument: AI-assisted software work becomes governable when intent moves out of private prompts and into maintained source-of-truth surfaces.

https://lambpetros.substack.com/p/the-specification-surface-is-the
```

### X Anchor Post

Purpose: create a referenceable anchor post, not a high-reach broadcast. Follow-through should come from targeted replies or quote posts into relevant AI engineering conversations, not from expecting the follower graph to carry the piece.

Post:

```text
AI coding has a hidden authority problem: the diff is visible, but the intent that governed it often is not.

The fix is maintained specification surfaces teams can inspect, validate, trace, and repair.

https://lambpetros.substack.com/p/the-specification-surface-is-the
```

### Hacker News Discussion Post

Title:

```text
Ask HN: How are teams making AI-generated code reviewable?
```

URL: leave blank.

Text:

```text
AI-generated PRs can pass tests and still be hard to review because the reviewer sees the diff, but not always the maintained intent that governed it.

In real repos, where are teams putting the source of truth for agent work?

Versioned specs? Tickets? Test contracts? Agent instruction files? Trace logs? Something else?
```

Do not include the Substack URL in the submission. Share it only later if the thread asks for context.

### Reddit Native Discussion Post

```text
Title: Where should the source of truth live when AI agents write code?

I keep seeing a governance problem in AI-assisted engineering that is easy to miss.

The diff is visible. The test output is visible. The agent summary is visible. But the actual intent that controlled the work often sits in a prompt, a chat thread, or a reviewer’s memory. When that happens, the team is reviewing downstream artifacts without a maintained source of truth for what the agent was supposed to preserve, what was out of scope, and which constraints mattered.

The failure mode gets worse with multi-agent work: one agent plans, another edits, another reviews, and the binding contract between them is informal. You can end up with plausible local changes that are hard to audit because nobody can point to the shared surface that governed the run.

The pattern I’m converging on is to treat specs, constraints, acceptance checks, and trace evidence as maintained artifacts close to execution. Short enough to audit, structured enough to parse, explicit enough to test, and durable enough to survive across runs.

Curious how others are handling this. Do you keep agent instructions and acceptance criteria in versioned files? Use tickets/issues as the authority surface? Encode constraints in tests? Or is this still mostly happening in prompts and chat logs?
```

Optional comment link, not post body:

```text
For context, I expanded this into a longer essay here: https://lambpetros.substack.com/p/the-specification-surface-is-the
```

Link-comment hold reason: account moderation risk and link-removal risk. Do not create a new Reddit account as a workaround for posts awaiting mod approval. Do not post the optional link comment unless explicitly confirmed after the native discussion post is submitted, or unless a commenter asks for the essay.
