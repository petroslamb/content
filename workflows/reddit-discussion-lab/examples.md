# Reddit Discussion Examples

Use these examples as calibration, not as copy to imitate.

The useful pattern is that the post gives readers an immediate way to participate. It starts with a problem, comparison, failure, or practice question. The theory can arrive later.

## 2026-05-06 Working Set

| Source Thread | What It Does Well | Why People Can Comment | Reusable Move |
| :--- | :--- | :--- | :--- |
| [Two failure modes I caught in my AI lab in one day. Both involve the system silently lying about its own state.](https://www.reddit.com/r/artificial/comments/1t4cx88/two_failure_modes_i_caught_in_my_ai_lab_in_one/) | Opens with an observed failure, not a concept. | People can share similar state-divergence failures or argue about instrumentation. | Start from a falsifiable incident. |
| [AI is getting better at doing things, but still bad at deciding what to do?](https://www.reddit.com/r/artificial/comments/1t50i19/ai_is_getting_better_at_doing_things_but_still/) | Uses a plain tension that many users have felt. | Readers can answer from product use, agent design, or workflow failures. | Put the contradiction in ordinary language. |
| [How do folks manage worktrees when working with multiple agents in parallel?](https://www.reddit.com/r/LLMDevs/comments/1t50mxb/how_do_folks_manage_worktrees_when_working_with/) | Asks a practical workflow question with immediate stakes. | Developers can describe their own setup without debating a thesis. | Ask for lived practice, not agreement. |
| [open source AI assistants ranked by tool call reliability](https://www.reddit.com/r/LLMDevs/comments/1t4e9ym/open_source_ai_assistants_ranked_by_tool_call/) | Gives developers something measurable to compare. | Readers can challenge the metric, add tests, or name missing failure cases. | Make the evaluation surface concrete. |
| [what actually broke when you tried red teaming your AI systems?](https://www.reddit.com/r/LLMDevs/comments/1t4ein0/what_actually_broke_when_you_tried_red_teaming/) | Invites failure stories and debugging detail. | The title asks for experience instead of opinions. | Ask for failure modes, not beliefs. |
| [I built an open source LLM monitoring tool that detects quality regressions before your users do](https://www.reddit.com/r/LLMDevs/comments/1t55p4k/i_built_an_open_source_llm_monitoring_tool_that/) | Connects a tool to a familiar operator category. | Readers can compare semantic monitoring to APM and observability. | Compare the new layer to an existing layer. |
| [AI agents vs AI chatbots: what are companies actually building?](https://www.reddit.com/r/artificial/comments/1t53331/ai_agents_vs_ai_chatbots_what_are_companies/) | Names a market confusion that readers can classify from examples. | Readers can bring examples and definitions. | Turn taxonomy into a practical sorting problem. |
| [made a tool that builds its own training data and fine-tunes itself](https://www.reddit.com/r/artificial/comments/1t4egej/made_a_tool_that_builds_its_own_training_data_and/) | Shows a concrete loop with obvious risk. | Readers can ask about validation, drift, and safeguards. | Show the mechanism before the worry. |
| [how accurate is AI at general knowledge?](https://www.reddit.com/r/artificial/comments/1t4asbk/how_accurate_is_ai_at_general_knowledge/) | Simple question with a hidden evaluation problem. | Anyone can answer, while technical commenters can deepen it. | Start accessible, then deepen in comments. |
| [agent skill which will automatically raise PR](https://www.reddit.com/r/LLMDevs/comments/1t4prcq/agent_skill_which_will_automatically_raise_pr/) | Concrete automation with maintainer-risk implications. | Developers can argue about PR boundaries and reviewer burden. | Ask where the boundary should be. |

## Style Notes

The working examples tend to:

- use ordinary words before technical terms
- make the title do one job
- leave room for disagreement
- invite specific stories
- avoid sounding complete
- avoid outbound links
- give readers a status role: builder, evaluator, maintainer, user, or skeptic

The posts are interesting because they are unfinished in the right way. They give enough structure to start a useful thread, but not so much that readers feel they are reacting to a finished essay.

## Failure Patterns To Avoid

Do not turn essay ideas into Reddit by only changing the title.

Avoid:

- `I wrote about <concept>`
- `<Concept> is the real problem with AI`
- `Why <concept> matters`
- `A research-backed framework for <topic>`
- `Has anyone else noticed <huge abstraction>?`
- long paper lists before the question
- starting with the Substack frame

Better:

- `my agent said it was done, but only its own log agreed. how are people checking this?`
- `what benchmark result would actually make you trust an agent in production?`
- `when agents write code, where do you keep the spec they are not allowed to reinterpret?`
