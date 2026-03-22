# Reddit Post for r/LLMDevs

**How are you debugging when agentic models orchestrate themselves wrong?**

Genuine question. When the model decides its own decomposition and gets it wrong, what's your workflow? Retry and hope? Parse JSONL logs line by line?

Context: been using RLMs (MIT paper from Zhang et al.) which externalize prompts as REPL variables. Model writes Python to filter, chunk, query inputs. Works on massive contexts (6-11M tokens with 128K models) but when a regex misses a document or a sub-call hallucinates, the failure is buried deep in recursive calls.

Built Jupyter integration where human and model share the same kernel. Inline traces on every result. Runnable .trace.ipynb notebooks where you can step through, edit intermediate cells, resume from wherever things went wrong.

Real limits: token overhead on simple stuff, cost variance 3-5x at p95, non-isolated execution.

Code: https://github.com/petroslamb/rlm (PR #46 against upstream)

---

**First Comment:**

Full writeup comparing to CodeAct, THREAD, ReDel, MemWalker, MemGPT: https://lambpetros.substack.com/p/when-the-llm-programs-its-own-thinking
