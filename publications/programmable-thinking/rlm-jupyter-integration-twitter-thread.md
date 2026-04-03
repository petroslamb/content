# Twitter Thread

Prompts should be queryable, not context-stuffed.

RLMs from @a1zhang treat inputs as REPL variables. Model writes Python to filter and chunk them. Paper shows 6-11M tokens with 128K models. 🧵

The model picks its own decomposition. Regex filters, chunking boundaries, recursive sub-calls for verification. These emerge from the paradigm, not hardcoded.

When self-orchestration fails, debugging is painful. Bad regex misses documents. Chunking splits semantic units. Sub-calls hallucinate. JSONL logs don't cut it.

Built Jupyter integration so human and model share the same kernel. Inline traces on every result. Runnable notebooks where you step through, modify state, resume. cc @jeremyphoward

Surgical intervention at the failure point beats retry-and-hope. The tooling exists now. Question is whether people will use it.

Code: github.com/petroslamb/rlm

Full writeup: https://lambpetros.substack.com/p/when-the-llm-programs-its-own-thinking

#LLM #AgenticAI #OpenSource
