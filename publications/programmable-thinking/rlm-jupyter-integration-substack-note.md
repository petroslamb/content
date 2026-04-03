# Substack Note

What if the prompt was a database table instead of text you shove into context?

RLMs externalize prompts as REPL variables. The model writes Python to query them. MIT shows 6-11M tokens handled with 128K models. The model chooses its own decomposition: regex filters, chunking strategies, recursive verification.

When self-orchestration fails, debugging from logs is brutal. I built Jupyter integration that puts you in the same REPL as the model. Shared namespace, inline traces, runnable notebooks that let you intervene at the exact failure point.

https://lambpetros.substack.com/p/when-the-llm-programs-its-own-thinking
