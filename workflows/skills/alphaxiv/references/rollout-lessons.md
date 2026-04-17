<!-- alphaxiv-py v0.4.2 -->
# alphaXiv rollout lessons

Use this file when the user is hitting auth friction, assistant-quality problems, or discovery ambiguity.

## Browser Auth Persistence

- `alphaxiv auth login-web` is one-time setup for a persistent browser profile.
- Keep `ALPHAXIV_HOME` and the browser-profile directory stable so assistant commands can reuse the saved session.
- Do not rerun `login-web` before every assistant command unless the session is actually gone.

## Assistant Overload Mitigation

- Large, unfocused assistant sessions can degrade and start returning low-quality answers.
- When that happens, use smaller, focused prompts and start a fresh `assistant start` session instead of endlessly extending one overloaded chat.
- Use `assistant list` and `assistant history` to recover prior context rather than forcing one session to carry everything.

## Validation Mode

- Validation mode works best when the anchor set is explicit before any assistant prompt.
- Reopen the exact papers with deterministic commands first; do not let the assistant infer the evidence set from memory.
- Use the assistant to ask what the papers license, what they do not license, and whether the top-level framing survives.
- If the anchor set fails, reopen search narrowly. If the frame fails, change the blueprint. Do not treat both problems as "find more papers."

## Feed Discovery

- When recency or ranking matters, prefer `feed filters search` plus `feed list` rather than guessing topic slugs or relying on generic keyword search.
- Real usage confirmed that topic and organization discovery are part of the workflow, not just optional extras.
- The strongest topic-selection rollouts used alphaXiv as retrieval infrastructure, not as the editorial decision layer. They first mapped topic vocabulary, then compared ranked feeds, then inspected papers, then used the assistant for shortlist comparison.
- For pre-package essay-topic decisions, follow `workflows/topic-discovery/README.md` and use this alphaXiv skill only for the command execution and assistant comparison steps.

Example:

```bash
alphaxiv feed filters search "agentic"
alphaxiv feed list --topic <topic-slug> --limit 10
```
