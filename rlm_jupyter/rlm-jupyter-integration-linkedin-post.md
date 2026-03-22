# LinkedIn Post

Spent two weeks debugging a model that kept missing critical documents in a 3M token input. The failure was buried three recursive calls deep. JSONL logs told me nothing useful.

That's the cost of self-orchestrating models. When the LLM decides its own decomposition strategy, it can decide wrong. Regex filters miss things. Chunking splits semantic units. Sub-calls hallucinate.

I built Jupyter integration for RLMs so human and model share the same kernel. Inline traces show what the model thought at each step. Runnable notebooks let you step through, modify intermediate state, and resume from the failure point.

Not retry-and-hope. Surgical intervention.

Code is open: github.com/petroslamb/rlm

Writeup with technical breakdown: https://lambpetros.substack.com/p/when-the-llm-programs-its-own-thinking

Building debugging tools for agentic systems? Would love to compare notes.
