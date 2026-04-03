# r/cybersecurity - Text Post

**Post type:** Text post (NOT a link post)
**Flair:** -
**When:** Thursday 4–5pm EET

---

## Title

Moltbook got breached in 72 hours because the AI that built it never turned on Row Level Security

## Body

Moltbook was that AI agent social network that Meta just acquired. One guy built the whole thing over a weekend with vibe coding, basically just prompting Cursor and shipping whatever came out. No security review, no QA, nothing.

Wiz.io took a look and found the Supabase credentials sitting in plaintext in a production JS file. RLS was never enabled. Public API key gave full read AND write access to every table.

What they found in the database:

- 1.5M API tokens for every registered agent, so anyone could impersonate any bot
- PII for 17,000 human operators (emails, names, X handles)
- Private messages between agents, some of which had plaintext OpenAI and Anthropic API keys that operators just let their bots share

The write access part is what really got me though. These agents ran on OpenClaw, which has a heartbeat loop that wakes up every few minutes and ingests whatever's on the platform as trusted input. So if you edit a high-karma post to include prompt injection instructions, every agent that reads it on its next cycle just... executes those instructions on the user's local machine. You're basically one PATCH request away from coordinated code execution across thousands of machines.

And after all this got disclosed publicly, the 17,000 operators didn't leave. Some were making ridiculous money on the $MOLT memecoin ($114M market cap at peak). Some were publishing research papers. Some were treating the whole thing as an AI safety experiment.

Then Meta bought it. The whole platform was 42 days old.

I wrote up the full analysis including why Meta actually bought it (spoiler: internal politics, not strategy): {{SUBSTACK_URL}}
