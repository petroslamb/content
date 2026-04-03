# HackerNews Post

**Jupyter Integration for Recursive Language Models**

RLMs externalize prompts as REPL variables instead of passing them to context windows. The model writes Python to filter, chunk, and query inputs. MIT paper shows 6-11M tokens handled with 128K models through emergent orchestration.

When models choose their own decomposition, they can choose wrong. Regex misses documents, chunking splits semantic units, sub-calls hallucinate. Built Jupyter integration that puts human and model in the same kernel with inline traces and runnable notebooks for stepping through failures.

Three sync modes for namespace sharing, sessions for history, persistence for stateful workflows. Limitations: token overhead, 3-5x cost variance at p95, non-isolated execution.

Code: https://github.com/petroslamb/rlm (PR #46 against upstream)

Writeup: https://lambpetros.substack.com/p/when-the-llm-programs-its-own-thinking
