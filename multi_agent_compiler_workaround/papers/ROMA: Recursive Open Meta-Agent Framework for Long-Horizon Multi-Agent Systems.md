Full Text for 2602.01848v2 (28
pages)

Page 1
ROMA: Recursive Open 
Meta-Agent Framework for
Long-Horizon Multi-Agent 
Systems
Salaheddin Alzu’bi
1* 
Baran Nama
1 
Arda Kaz
1,3
Anushri Eswaran
1,4 
Weiyuan Chen
2 
Sarvesh Khetan
1,5 
Rishab Bala
2
Tu Vu
2♦ 
Sewoong Oh
1♦
1
Sentient, 
2
Virginia Tech, 
3
UC Berkeley, 
4
UC San Diego, 
5
University of Maryland
https://github.com/sentient-ag
i/ROMA
Abstract
Current agentic frameworks 
underperform on long-horizon 
tasks. As reasoning
depth increases, sequential 
orchestration becomes brittle,
context windows impose
hard limits that degrade 
performance, and opaque 
execution traces make failures
difficult to localize or 
debug. We introduce ROMA 
(Recursive Open Meta-Agents),
a domain-agnostic framework 
that addresses these 
limitations through recursive
task decomposition and 
structured aggregation. ROMA 
decomposes goals into
dependency-aware subtask trees
that can be executed in 
parallel, while aggregation
compresses and validates 
intermediate results to 
control context growth. Our 
frame-
work standardizes agent 
construction around four 
modular roles – Atomizer 
(which
decides whether a task should 
be decomposed), Planner, 
Executor, and Aggregator
– which cleanly separate 
orchestration from model 
selection and enable 
transparent,
hierarchical execution traces.
This design supports 
heterogeneous multi-agent
systems that mix models and 
tools according to cost, 
latency, and capability. To
adapt ROMA to specific tasks 
without fine-tuning, we 
further introduce GEPA+,
an improved Genetic-Pareto 
prompt proposer that searches 
over prompts within
ROMA’s component hierarchy 
while preserving interface 
contracts. We show that
ROMA, combined with GEPA+, 
delivers leading system-level 
performance on
reasoning and long-form 
generation benchmarks. On 
SEAL-0, which evaluates rea-
soning over conflicting web 
evidence, ROMA instantiated 
with GLM-4.6 improves
accuracy by 9.9% over 
Kimi-Researcher. On EQ-Bench, 
a long-form writing
benchmark, ROMA enables 
DeepSeek-V3 to match the 
performance of leading
closed-source models such as 
Claude Sonnet 4.5. Our results
demonstrate that
recursive, modular agent 
architectures can scale 
reasoning depth while 
remaining
interpretable, flexible, and 
model-agnostic.
1 Introduction
Large language models (LLMs) 
have enabled rapid progress in
agentic systems, where 
multi-step
workflows compose model calls,
tools, and memory to solve 
long-horizon tasks such as 
code
generation [6 , 13 ] and 
open-domain research [32 , 
36]. These systems now appear 
in both research
prototypes and deployed 
products, where they often 
match or exceed strong 
single-call baselines.
Much of this improvement comes
from the use of multiple 
specialized agents that 
communicate and
collaborate to address complex
problems [19].
*
Lead author. 
♦
Co-senior authors. 
Correspondence to 
salaheddin@sentient.xyz.
Preprint.
arXiv:2602.01848v2  14 Feb 
2026


Page 2
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Planner
subtasks with dependencies
t
1
, t
2
, t
3
Executor
execute(t) → y
is_atomic(t)?
Atomizer
Aggregator
merge child outputs
y
1
, y
2
, y
3
y’
t
y
t
1
t
2
t
3
y
1
y
2
y
3
Yes
No
Task
After recursion completes
search think
write code
Figure 1: Overview of ROMA’s 
recursive architecture. An 
Atomizer determines whether a 
task is
atomic. Atomic tasks are 
executed directly, while 
non-atomic tasks are 
decomposed into subtasks by
a Planner. Each subtask is 
executed recursively by 
Executors, after which an 
Aggregator merges the
outputs of all descendants to 
produce the final result.
Despite their success, most 
agentic systems are built in 
an ad hoc manner. Control 
flow, commu-
nication patterns, and context
management are typically 
hard-coded into prompts or 
orchestration
logic, rather than expressed 
through shared, task-agnostic 
abstractions. As a result, 
systems that
perform well in one domain 
rarely transfer cleanly to 
others. Developing a new agent
often requires
rebuilding meta-agent 
structure from scratch, 
including role definitions, 
message-passing protocols,
and memory interfaces. This 
fragmentation is reflected in 
the proliferation of 
open-source research
agents with incompatible 
designs, while closed-source 
systems provide little 
visibility into their
internal orchestration.
This lack of standardization 
leads to recurring failure 
modes. Agent communication and
task
decomposition follow no common
schema, which makes systems 
difficult to compare, extend, 
or
reuse. Agent behavior is also 
opaque. Proprietary systems 
expose no execution traces, 
while open-
source systems typically 
provide only unstructured 
logs, which complicates error 
localization in deep,
branching executions. When 
failures occur late in a run, 
there is rarely a principled 
way to attribute
them to earlier planning, 
retrieval, or aggregation 
decisions. Additionally, 
agentic systems suffer
from uncontrolled context 
growth, where accumulating 
intermediate reasoning, tool 
outputs, and
artifacts degrade performance 
or exceed context limits.
In this work, we introduce 
ROMA (Recursive Open 
Meta-Agents), a unified 
framework, inspired
by [52 ], that is designed for
building multi-agent systems 
around a prescribed meta-agent
structure.
ROMA operates over a 
recursive, node-level control 
loop that is applied uniformly
at every node
in a task tree and is composed
of four core components: 
Atomizer, Planner, Executors, 
and
Aggregator (see Figure 1). 
Starting from a root goal, an 
Atomizer determines whether 
the current task
is atomic. Non-atomic tasks 
are expanded by a Planner into
dependency-aware, Mutually 
Exclusive
and Collectively Exhaustive 
(MECE) subtask graphs. Each 
resulting subtask 
independently executes
the same control loop: atomic 
tasks are handled directly by 
Executors, potentially in 
parallel, while
non-atomic tasks are further 
decomposed. Once all child 
tasks of a node complete, an 
Aggregator
synthesizes, verifies, and 
compresses their outputs into 
a higher-level artifact that 
is returned to the
parent. This recursive 
execution produces a 
hierarchical trace that 
mirrors the execution tree.
By standardizing how tasks are
decomposed, executed, and 
aggregated, ROMA replaces ad 
hoc, task-
specific orchestration 
patterns with a reusable, 
domain-agnostic abstraction 
(Atomizer → Planner
→ Executor → Aggregator) that 
applies uniformly across 
domains. Practitioners 
instantiate new
agents by specifying prompts 
for these components, while 
ROMA automatically handles 
control flow,
task decomposition, and 
context propagation. ROMA also
improves transparency and 
traceability of
agent behavior. Because the 
same execution protocol is 
applied at every node in the 
task tree, the
framework exposes all planning
decisions, executions, and 
aggregations as a structured, 
hierarchical
trace. This makes it possible 
to inspect and debug failures 
in deep, branching reasoning 
processes,
where errors are otherwise 
difficult to localize. 
Finally, ROMA controls context
growth through
recursive decomposition and 
bounded aggregation. Executors
operate on localized context, 
while
Aggregators compress 
intermediate results before 
passing them upward. Instead 
of propagating full
2


Page 3
transcripts, each node returns
a concise, verified summary, 
which reduces context rot [20 
] and enables
ROMA to scale to long-horizon 
tasks while maintaining stable
performance.
Beyond addressing these 
structural limitations, ROMA 
supports parallel and 
heterogeneous execution.
Independent branches of the 
task decomposition can execute
in parallel, and different 
models can be
assigned to different roles, 
such as planning, execution, 
and aggregation. This 
decouples orchestration
from any single foundation 
model and allows practitioners
to exploit heterogeneous model
strengths
across subtasks while keeping 
the high-level control loop 
fixed.
To adapt ROMA to specific 
tasks without fine-tuning, we 
further introduce GEPA+, a 
multi-component
prompt optimization method 
tailored to ROMA’s modular 
architecture. GEPA+ extends 
prior GEPA-
style prompt evolution [1 ] by
jointly optimizing the prompts
of the Atomizer, Planner, 
Executors, and
Aggregator. At a high level, 
GEPA+ works by generating 
multiple candidate prompt 
edits in parallel,
evaluating them with 
lightweight judges and 
verifiers, and merging the 
best ideas into a single,
interface-safe update, which 
enables efficient exploration 
without destabilizing the 
system. This
structured, K-way proposal and
selection process consistently
improves downstream 
performance,
yielding 2-6 point absolute 
accuracy gains while requiring
approximately 3–4× fewer 
metric evalua-
tions than standard GEPA [1] 
(see Appendix G), allowing 
ROMA to be automatically 
specialized to
new tasks with minimal manual 
intervention.
We evaluate ROMA across a 
range of reasoning and 
long-form generation 
benchmarks and show
that it delivers leading 
system-level performance. On 
SEAL-0 [ 38 ], which tests 
reasoning over
conflicting web evidence, ROMA
instantiated with GLM-4.6 [ 57
] improves accuracy by 9.9% 
over
Kimi-Researcher [2 ], a 
reinforcement-learning-tuned 
deep research agent. On 
EQ-Bench [35 ], a long-
form writing benchmark, ROMA 
enables DeepSeek-V3 [25] to 
match the performance of 
leading
closed-source models such as 
Claude Sonnet 4.5 [9]. Taken 
as a whole, our results 
demonstrate
that recursive, modular agent 
architectures can scale 
reasoning depth while 
remaining interpretable,
flexible, and model-agnostic.
To summarize, our main 
contributions are:
1. ROMA: We introduce ROMA, a 
scalable and domain-agnostic 
meta-agent framework
built around a fixed recursive
control loop with four roles: 
Atomizer, Planner, Executors,
and Aggregator. ROMA addresses
key structural limitations of 
existing agentic systems,
including the lack of a 
standard schema, opaque 
execution, and uncontrolled 
context growth,
while allowing practitioners 
to exploit heterogeneous model
strengths across subtasks.
2. GEPA+: We develop GEPA+, a 
prompt optimization method 
tailored to ROMA’s modular
architecture, which jointly 
optimizes the prompts of 
individual components through 
a
structured, multi-candidate 
proposal and selection 
process. GEPA+ enables 
efficient task
adaptation without fine-tuning
and improves performance with 
minimal manual intervention.
3. Leading system-level 
empirical performance: We 
evaluate ROMA across a range 
of
reasoning and long-form 
generation benchmarks, 
including SEAL-0 [38 ], FRAMES
[ 23],
SimpleQA [47], EQ-Bench [ 35 
], and AbGen [60 ]. We show 
that ROMA instantiated
with GLM-4.6 improves accuracy
on SEAL-0 by 9.9% relative to 
Kimi-Researcher, a
reinforcement-learning–tuned 
deep research agent, and that,
when combined with GEPA+,
ROMA enables DeepSeek-V3 to 
match the performance of 
leading closed-source models,
including Claude Sonnet 4.5, 
on EQ-Bench.
2 Methodology
In this section, we present 
the ROMA framework and its 
execution semantics. 
Additionally, we
introduce GEPA+ for 
component-wise prompt 
optimization.
2.1 ROMA
ROMA is a recursive meta-agent
that solves a task by 
alternating between 
decomposition and
execution until all 
subproblems are atomic, after 
which evidence is aggregated 
bottom-up to produce
the parent’s answer (Algorithm
1). For each task or subtask 
in ROMA’s dynamically 
constructed
task graph, a controller 
invokes the same four 
components: Atomizer, Planner,
Executors, and
Aggregator (see Figure 1). 
This design generalizes 
heterogeneous recursive 
planning routines
3


Page 4
y’
21
t
Task (non-atomic)
(task_type, context)
Search exe.
(ReAct)
Think exe.
(CoT)
Write exe.
(Drafting)
Code exe.
(CodeAct)
Tool calls
(standard interface)
Sandboxed runtime
(Code exe.)
choose a
predefined
strategy
MCP servers
External tools
(APIs)
Artifact store
read
(context)
Executor node detail
(zoomed in)
Level 0
Level 1
Level 2
exe. 
exe. 
exe.
search (atomic)
exe. → y
1
code (atomic)
exe. → y
3
think (non-atomic)
t
21
Task (atomic)
flow direction
↓ Top-down: planning
→ Left-right: dependency
↑ Bottom-up: aggregation
write
(output)
result
depends on y
1
Figure 2: ROMA’s hierarchical 
execution flow. Non-atomic 
tasks are decomposed top-down 
through
planning, with left-to-right 
dependencies guiding 
execution, while results are 
combined bottom-up
through aggregation. Executors
operate on atomic subtasks, 
producing intermediate outputs
that are
aggregated into higher-level 
artifacts; the inset shows a 
zoomed-in executor node with 
tool interaction.
previously used in writing 
assistants [ 52 ] to a 
domain-agnostic setting, where
composition, retrieval,
reasoning, and programmatic 
manipulation coexist within a 
single control loop and are 
scheduled
with explicit dependencies.
Let t denote a task with a 
textual specification and 
optional constraints. ROMA 
exposes four
operators:
is_atomic(t) → {True, False} 
(Atomizer)
plan(t) → S(t) (Planner)
execute(t) → y
t 
(Executor)
aggregate
({
y
s
}
s∈S(t)
) 
→ y
t−1 
(Aggregator)
If is_atomic(t) returns True, 
the Atomizer deems the task 
atomic and the system bypasses
planning,
invoking the Executor to 
directly apply execute(t) to 
produce y
t
. Otherwise, the Planner 
applies
plan(t) to decompose t into a 
dependency-aware subtask graph
S(t), which can be seen as a
directed acyclic graph (DAG), 
where nodes correspond to 
subtasks and directed edges 
encode
execution dependencies. In the
simplest case, all subtasks 
depend only on the parent task
and are
independent of one another 
(e.g., S(t) = {t → t
1
, t → t
2
, t → t
3
}). More generally, S(t) may
encode dependencies among 
subtasks (e.g., S(t) = {t → t
1
, t → t
2
, t → t
3
, t
1 
→ t
3
, t
2 
→ t
3
}, in
which t
3 
is blocked until t
1 
and t
2 
complete). The same control 
loop is then applied 
independently
to each subtask s ∈ S(t), and 
subtasks may execute in 
parallel when dependencies 
allow. Once
all subtasks complete, the 
Aggregator combines their 
outputs through aggregate
({
y
s
}
s∈S(t)
) 
to
produce the parent task’s 
result y
t−1
. This plan–execute–aggregate 
loop is the sole control flow 
in
ROMA, which makes the 
framework task-agnostic, 
transparent, and extensible.
Figure 2 illustrates ROMA’s 
hierarchical execution flow. 
Tasks are decomposed top-down 
through
planning, while results are 
combined bottom-up through 
aggregation. Executors operate
only on
atomic subtasks, producing 
intermediate outputs that are 
aggregated into higher-level 
artifacts. The
same recursive control loop is
applied at every node in the 
task tree, reinforcing ROMA’s 
generality
across domains and task types.
Below, we discuss ROMA’s core 
properties.
Top-down decomposition and 
bottom-up aggregation: The 
Planner decomposes a 
non-atomic
task t into a mutually 
exclusive, collectively 
exhaustive (MECE) subtask 
graph S(t) that maximizes
4


Page 5
parallelism and minimizes 
redundancy. Subtasks are 
defined at the intent level 
and connected by
explicit dependency edges when
left-to-right precedence is 
required. The result is a 
compact ordered
DAG that supports parallel 
execution.
A parent’s output is not a raw
concatenation of child 
results. Instead, the 
Aggregator applies
aggregate
({
y
s
}
s∈S(t)
) 
to distill and normalize child
outputs into the parent’s 
target form (e.g., a
paragraph, a table, or a JSON 
schema). Executors are 
restricted to operate on local
context, while
Aggregators perform 
cross-cutting synthesis and 
relevance-preserving 
compression. This design
mitigates context explosion 
and allows the effective 
working set to exceed a single
model’s context
window.
Dependency-aware parallel 
execution: At each level of 
the task tree, Planner returns
a dependency-
aware subtask graph S(t) with 
explicit left-to-right 
dependency edges that 
constrain execution.
Subtasks with no unmet 
dependencies may execute in 
parallel, while dependent 
subtasks are scheduled
as soon as their predecessors 
complete. This 
dependency-aware scheduling 
avoids global barriers
and enables latency-efficient 
execution along the critical 
path, while preserving 
correctness when
subtasks require inputs from 
earlier siblings (e.g., 
“identify the highest-scoring 
player” → “retrieve
their age”).
Task types and 
type-specialized execution: 
Each task node is annotated 
with a task_type
drawn from a small, expressive
set:
1. search (retrieval): 
retrieve documents, facts, or 
tool outputs from external 
sources.
2. think (reasoning): 
synthesize intermediate 
conclusions (e.g., derivations
or chain-of-
thought (CoT)).
3. write (composition): 
compose structured or 
expository outputs from 
evidence (e.g., sec-
tions, summaries, answers).
4. code 
(programmatic manipulation): 
write or execute code to 
transform data or invoke
structured tools.
The Atomizer’s atomicity 
decision is orthogonal to 
task_type. A node may be 
non-atomic and
handed to the Planner, or 
atomic and handed to an 
Executor, independent of its 
type. This separation
allows ROMA to decouple how a 
task is decomposed from how a 
leaf computation is carried 
out. In
our implementation, each 
task_type routes to a 
type-specialized Executor with
distinct prompting
strategies (e.g., ReAct [56], 
CodeAct [46 ], or CoT [ 48]) 
and model choices, which can 
be selected to
trade off cost, latency, and 
quality (see Figure 2).
Modular components and 
optimization hooks: ROMA’s 
components are implemented as 
modu-
lar DSPy [22] programs with 
typed input/output signatures.
This design provides 
structured interfaces
between the Atomizer, Planner,
Executor, and Aggregator, 
provides structured interfaces
betwee-
nenables composability by 
allowing modules to be swapped
while preserving type 
compatibility,
and exposes built-in 
optimization hooks for prompts
and weights via DSPy 
optimizers. DSPy’s
“programming-not-prompting” 
abstractions allow these 
components to be declared as 
executable
modules and compiled into 
high-performing LM 
invocations, which we find 
essential for building
and optimizing a 
multi-component agent system.
Artifacts, tools, and safe 
execution: ROMA is designed 
for tool-rich and 
high-throughput
workloads. Intermediate 
artifacts (e.g., plans, notes,
citations, and datasets) are 
persisted to an object
store and exposed to 
downstream nodes through typed
module signatures, rather than
embedded
directly in prompts. This 
allows artifacts to be reused 
across the task tree without 
inflating prompt
context. Programmatic subtasks
are handled by the code task 
type, which uses a sandboxed 
runtime
to execute user- or 
model-generated code in a 
safe, isolated environment and
to interact with external
tools through standard 
interfaces, such as the Model 
Context Protocol (MCP) [ 5 ]. 
This design
supports efficient multi-agent
execution while preserving 
isolation, observability, and 
safety.
Putting it together – the ROMA
control loop: Algorithm 1 
summarizes ROMA’s recursive
control loop. Information 
flows top-down during 
planning, left-to-right within
each level to respect
dependency constraints, and 
bottom-up during aggregation. 
Executors are invoked only on 
atomic
tasks, while Aggregators 
return parent-scoped results 
rather than raw child outputs.
This structured
separation of planning, 
execution, and aggregation 
allows ROMA to scale to 
long-horizon tasks while
keeping each component 
focused, interpretable, and 
easy to optimize.
5


Page 6
Algorithm 1 ROMA: A recursive 
control loop with Atomizer, 
Planner, and Aggregator.
1: procedure SOLVE(task)
2: if is_atomic(task) then ▷ 
Step 1: Atomizer
3: return execute(task) ▷ Step
2: Executor
4: else
5: subtasks ← plan(task) ▷ 
Step 2: Planner
6: results ← [ ] ▷ Initialize 
empty list
7: for all subtask ∈ subtasks 
do
8: 
results.append(SOLVE(subtask))
▷ Recursive call
9: end for
10: return aggregate(results) 
▷ Step 3: Aggregator
11: end if
12: end procedure
2.2 Multi-component prompt 
optimization with GEPA+
In this section, we introduce 
GEPA+, a multi-proposer 
extension of DSPy’s GEPA [ 1 ]
that is tailored
to ROMA’s modular, 
multi-component architecture. 
Whereas classical GEPA uses a 
single reflection
model to propose an 
instruction/prompt update for 
one module given execution 
traces and feedback,
GEPA+ replaces this with a 
K−way proposer that (i) 
generates diverse prompt edits
in parallel, (ii)
re-ranks them using learned 
and verifier-based signals, 
and (iii) merges the strongest
candidates into a
single, interface-safe update.
The result is a minimal-change
optimizer that more 
effectively explores
the local edit space while 
preserving cross-module 
contracts. Below, we detail 
the optimization
procedure. More implementation
details can be found in our 
code.
1
Problem setup: Let the system 
consist of modules m ∈ M 
(Atomizer, Planner, 
type-specific
Executors, Aggregator), each 
with a current instruction I
m
. Given a development set D 
with automatic
checks, GEPA+ searches for 
delta edits ∆I
m 
that improve a utility 
function U ({I
m
}
m∈M
; D) under
budget and stability 
constraints, while maintaining
module interface invariants 
(e.g., required fields
in search outputs).
Diverse proposals: For a 
target module m, GEPA+ samples
k independent proposal 
candidates
Π
m 
= {π
1
, . . . , π
k
} in parallel, conditioned on 
execution traces and feedback.
Diversity is induced
through a mixture of base 
LLMs, decoding settings (e.g.,
with different temperatures 
and random
seeds), and optional 
reflection prompts. Proposals 
are module-aware, for example,
Planner edits must
preserve MECE and dependency 
constraints, while Aggregator 
edits must respect expected 
input
schemas from sibling modules.
Reranking with judges and 
verifiers: Each candidate π
i 
is scored by a composite 
function
J (π
i 
∣ D) = α Judge(π
i
) + β Verifier(π
i
; D) − γ ContractViolations(π
i
),
where Judges (i.e., 
LLM-as-a-Judge [61]) assign 
rubric-based quality scores on
held-out execution
traces; Verifiers run fast, 
task-specific checks (e.g., 
unit tests for code, citation 
and consistency checks
for search and write, and 
interface conformance checks 
for the Aggregator), and 
ContractViolations
penalize edits that break 
typed I/O or ROMA DAG 
invariants (i.e., acyclic, 
dependency-consistent
task graphs). The top-n 
candidates Π
(n)
m 
are selected according to J 
(⋅).
Structured merge of candidate 
edits: GEPA+ consolidates the 
selected candidates Π
(n)
m 
into
a single update
̂
 ∆I
m 
via a contract-preserving 
merger that performs: (i) 
Atomization, which
decomposes each proposal into 
atomic edits (e.g., adding one
constraint, replacing one 
example,
or rephrasing one 
instruction); Conflict 
resolution, which resolves 
incompatible edits by 
retaining
higher-scoring variants while 
demoting alternatives to 
auxiliary examples or 
comments; and (iii)
Deduplication and alignment, 
which clusters near-duplicate 
edits and normalizes 
terminology to
preserve module contracts and 
MECE constraints. The merger 
guarantees schema compliance 
for
module m and compatibility 
with neighboring modules.
1
https://github.com/sentient-ag
i/gepa-plus.
6


Page 7
Budget and stability: Parallel
proposal generation reduces 
wall-clock latency while 
respecting
fixed token and time budgets. 
We cap k, n, judge calls, and 
verifier runs per round. GEPA+
favors
minimal edits through 
delta-size penalties, which 
helps preserve trace stability
and avoids prompt
drift.
Summary: Compared to 
single-proposer GEPA, GEPA+ 
widens local search through 
parallel,
diverse proposals, filters 
candidates using task-aware 
judges and verifiers, and 
fuses improvements
via a contract-preserving 
merger. In our experiments, 
this “propose×k → rerank → 
merge” loop
consistently yields higher 
utility under the same budget,
while keeping ROMA’s module 
interfaces
intact. See Appendix G for a 
detailed comparison between 
GEPA and GEPA+.
3 Experiments
3.1 Experimental Setup
We evaluate ROMA on a broad 
suite of benchmarks that 
target complementary 
capabilities.
Specifically, we evaluate on 
SEAL-0 [ 38 ], which tests 
reasoning over conflicting web
evidence;
FRAMES [ 23 ] and SimpleQA [ 
47 ], which evaluate multi-hop
factual reasoning and question
an-
swering, respectively; 
EQ-Bench [ 35 ], which focuses
on long-form writing, and 
AbGen [ 60], which
assesses a model’s ability to 
design rigorous ablation 
studies.
Though ROMA is model-agnostic 
and supports heterogeneous 
model assignment across roles,
our
experiments primarily 
instantiate ROMA with a single
base model per task, which 
allows us to
isolate the framework’s 
contribution without 
introducing additional 
variability from cross-model
interactions. Specifically, we
use GLM [57 ] for search- and 
reasoning-intensive benchmarks
(SEAL-0,
FRAMES, and SimpleQA) and 
DeepSeek[25 ] for long-form 
generation benchmarks 
(EQ-Bench and
AbGen). We leave a systematic 
exploration of heterogeneous 
model assignments across roles
to
future work. Additionally, we 
rely on search results 
provided by the GPT-5-mini 
search interface for
search-intensive tasks. ROMA 
operates over the returned 
evidence using its recursive 
decomposition
and aggregation mechanisms. 
See Appendix B for complete 
experimental configurations.
We do not use a fixed set of 
baselines across all 
experiments; instead, most 
baselines are taken directly
from the corresponding 
benchmark or chosen per 
benchmark to reflect the most 
relevant comparisons.
For example, on SEAL-0 we 
compare against 
Kimi-Researcher [2], a 
reinforcement-learning-tuned
autonomous agent specialized 
for search and reasoning, and 
Perplexity Deep Research [36],
a closed-
source system designed for web
search-centric research 
workflows. This task-specific 
baseline
selection avoids misleading 
comparisons between systems 
optimized for different goals.
We apply and report GEPA/GEPA+
only on EQ-Bench, where prompt
optimization has a material
impact on long-form writing 
performance; all other 
experiments use fixed, 
hand-written component
prompts to isolate the 
contribution of ROMA’s 
execution structure. In our 
implementation, GEPA+
uses a multi-proposer setup in
which candidate prompt edits 
are generated in parallel by a
small set
of diverse models, including 
GPT-5 [ 41 ], Claude Sonnet 
4.5 [9], and Gemini 2.5 Flash 
[12 ], with
different decoding 
temperatures. Candidate 
proposals are evaluated by a 
judge model (Claude Sonnet
4.5) and merged by a dedicated
merger model (GPT-5) into a 
single interface-safe update, 
with the
top-n (n = 2) proposals 
retained for merging. This 
design balances proposal 
diversity with stability
and allows GEPA+ to explore 
the local prompt-edit space 
efficiently. See Appendix F 
for GEPA+
configuration details.
Finally, we use GPT-4o-mini 
[31 ] as an LLM judge to 
evaluate model outputs on 
SEAL-0, FRAMES,
and SimpleQA, following the 
standard evaluation procedures
of these benchmarks (see 
Appendix A
for the full judging prompt). 
For EQ-Bench, evaluation is 
performed using Claude Sonnet 
4 [8],
consistent with the 
benchmark’s official long-form
writing protocol. For AbGen, 
we follow the
benchmark’s original 
evaluation setup and use 
GPT-4.1-mini [33 ] as the 
judge to score ablation study
designs along multiple 
Likert-scale dimensions. 
Across all benchmarks, we 
adhere to the respective
published evaluation protocols
to ensure fair and comparable 
results.
3.2 Results and discussion
SEAL-0 (reasoning over 
conflicting web evidence): 
Table 1 shows our results on 
SEAL-0, a
benchmark of 111 questions 
designed to evaluate reasoning
over noisy and conflicting web
evidence.
In addition to reported 
results from [38 ], we run 
three baselines ourselves, 
including Perplexity
7


Page 8
Table 1: SEAL-0 accuracy for 
closed-source and open-source 
systems. 
⋆ 
denotes results taken from
the SEAL-0 leaderboard. 
⋄ 
denotes baseline evaluations 
run by the authors. 
♠ 
denotes systems that
were not publicly available at
the time of evaluation.
Model Search SEAL-0 (%)
Closed-source
Grok-3
⋆ 
✓ 5.4
Gemini 2.5 Flash
⋆ 
✓ 13.5
Perplexity Sonar Reasoning Pro
⋄ 
✓ 13.5
o3
⋆ 
✓ 15.3
o3-pro
⋆ 
✓ 18.9
Gemini 2.5 Pro
⋆ 
✓ 19.8
Grok-4
⋆ 
✓ 20.7
Perplexity Deep Research
⋄ 
✓ 31.5
Open-source
DeepSeek-R1
⋆ 
✓ 4.5
Qwen3-235B-A22B
⋆ 
✓ 5.4
Open Deep Search (DeepSeek-R1)
⋄ 
✓ 9.9
GLM-4.6 ✓ 14.5
Kimi-Researcher
♠ 
[2] ✓ 36.0
ROMA (GLM-4.6) ✓ 45.9
Sonar Reasoning Pro [ 37], 
Perplexity Deep Research [ 36 
], and Open Deep Search [3], 
using their
default or recommended 
hyperparameters.
2 
ROMA achieves the best overall
performance with 45.9%
accuracy, outperforming both 
open-source and closed-source 
baselines. This corresponds to
a 9.9%
absolute improvement over 
Kimi-Researcher (36.0%), the 
strongest prior open research 
agent, and a
14.4% absolute improvement 
over Perplexity Deep Research 
(31.5%), the best 
closed-source system
evaluated. ROMA also 
substantially outperforms its 
underlying base model 
(GLM-4.6, 14.5%),
indicating that the gains stem
from the agent architecture 
rather than model scale alone.
ROMA’s gains indicate that how
evidence is decomposed and 
reconciled is critical. ROMA’s
recur-
sive decomposition isolates 
conflicting evidence into 
focused subtasks, while 
structured aggregation
explicitly compares and 
synthesizes results, reducing 
error accumulation from 
reasoning over many
documents at once. This 
suggests that dependency-aware
decomposition and aggregation 
are particu-
larly effective for 
search-intensive reasoning 
tasks.
FRAMES (multi-hop reasoning): 
Table 2 reports results on 
FRAMES, which consists of 824
multi-hop factual questions 
requiring integration of 
information across multiple 
Wikipedia pages.
ROMA achieves the highest 
accuracy on this benchmark at 
82.3%, exceeding the 
performance of both
open- and closed-source 
baselines. Kimi-Researcher 
ranks second at 78.8%, whereas
general-purpose
reasoning models such as 
DeepSeek-R1 and Llama-3.1-70B 
lag far behind, remaining 
below 35%
accuracy.
In contrast to SEAL-0, FRAMES 
primarily emphasizes 
compositional reasoning across
ordered
hops. ROMA improves over 
search-augmented baselines by 
maintaining coherence across 
successive
reasoning steps. ROMA’s 
execution model supports this 
by treating each hop as a 
separate reasoning
unit and combining 
intermediate results only 
after all required 
sub-questions are resolved, 
which
helps limit error accumulation
in longer reasoning chains.
SimpleQA (factual question 
answering): Table 3 reports 
results on SimpleQA, which 
consists
of 4,326 short-form factual 
questions with a single 
unambiguous answer, spanning a
wide range of
topics. Overall performance on
SimpleQA is high across both 
open-source and closed-source 
systems,
2
For Open Deep Search, we used 
Serper.dev as the search 
provider, LiteLLM with 
DeepSeek-R1 as the
reasoning model, self-hosted 
Infinity Embeddings for 
reranking, and SmolAgents for 
enhanced reasoning. See
https://github.com/sentient-ag
i/OpenDeepSearch for more 
details.
8


Page 9
Table 2: FRAMES accuracy for 
closed-source and open-source 
systems. 
⋆ 
denotes results taken
from [3]. 
♠ 
denotes systems that were not 
publicly available at the time
of evaluation.
Model Search FRAMES (%)
Closed-source
Perplexity
⋆ 
✓ 42.4
Perplexity Sonar Reasoning Pro
⋆ 
✓ 44.4
GPT-4o
⋆ 
× 50.5
GPT-4o Search Preview
⋆ 
✓ 65.6
Open-source
DeepSeek-R1
⋆ 
× 30.1
Llama-3.1-70B
⋆ 
× 34.3
GLM-4.6 ✓ 71.2
Open Deep Search (DeepSeek-R1)
[4]
⋆ 
✓ 75.3
Kimi-Researcher
♠ 
[2] ✓ 78.8
ROMA (GLM-4.6) ✓ 82.3
reflecting the relatively 
direct nature of the task. The
strongest closed-source 
system, Liner Pro
Reasoning, achieves 95.3% 
accuracy, while ROMA reaches 
93.9%, ranking as the 
best-performing
open-source system and 
narrowly trailing the top 
closed-source result. 
Kimi-Researcher follows
closely at 93.6%.
SimpleQA primarily stresses 
precise retrieval and factual 
verification, rather than deep
multi-step
reasoning. As a result, 
systems with effective search 
capabilities perform well even
without explicit
task decomposition. 
Nevertheless, ROMA remains 
competitive by reliably 
routing SimpleQA queries
to focused retrieval-oriented 
execution, demonstrating that 
its general-purpose agent 
architecture
does not incur overhead on 
simpler tasks. Overall, 
SimpleQA shows that ROMA 
maintains strong
performance on straightforward
factual queries, narrowing the
gap between open- and 
closed-source
systems in practical web-based
question answering.
EQ-Bench (long-form writing): 
EQ-Bench evaluates long-form 
writing, emphasizing a model’s
ability to plan, maintain 
coherence, and sustain 
narrative structure across 
multiple turns. Each task is
executed over eight turns of 
approximately 1,000 words 
each, and outputs are scored 
for narrative
quality, character depth, and 
structural consistency.
Using ROMA instantiated with 
DeepSeek-V3 and default 
prompts,
3 
we obtain a long-form writing
score of 71.9%. Applying GEPA+
prompt optimization yields a 
substantial improvement to 
79.8%,
which matches the performance 
of leading closed-source 
models such as Claude Sonnet 
4.5 (see
Table 4). Here, our reported 
results reflect the best 
performance across five 
independent runs. We note
that evaluation is performed 
using Claude Sonnet 4, which 
may introduce bias in favor of
Claude-
family models. This 
improvement indicates that 
prompt design plays a critical
role for long-horizon
generation tasks. Qualitative 
analysis indicates that GEPA+ 
strengthens both high-level 
planning
and execution guidance (see 
Appendices C, D, and E for 
full prompts). Optimized 
Planner prompts
emphasize explicit story 
structure and pacing, while 
optimized Executor prompts 
encourage concrete
scene construction through 
actions, dialogue, and sensory
detail, leading to more 
coherent character
arcs and more consistent 
narrative flow throughout the 
narrative. Overall, these 
results suggest that
ROMA’s modular execution 
framework provides a strong 
foundation for long-form 
generation, with
GEPA+ enabling targeted 
improvements without altering 
the underlying control 
structure. Table 5
shows the average per-chapter 
cost, token usage, and 
end-to-end latency for ROMA 
instantiated with
DeepSeek-V3.1. Overall, ROMA 
achieves competitive quality 
with manageable cost and 
latency,
demonstrating that structured 
multi-component execution can 
support long-form generation 
without
prohibitive computational 
overhead.
3
We follow the configuration 
described in Appendix B, 
except that the default 
Planner is replaced with
DeepSeek-V3.
9


Page 10
Table 3: ROMA achieves the 
highest accuracy among 
open-source systems on 
SimpleQA. 
⋆ 
denotes
results taken from the 
SimpleQA leaderboard.
Model Search SimpleQA (%)
Closed-source
o1-mini
⋆ 
× 7.6
GPT-4o-mini-2024-07-18
⋆ 
× 9.5
o3-mini-low
⋆ 
× 13.0
o3-mini
⋆ 
× 13.4
o3-mini-high
⋆ 
× 13.8
Grok 3 mini Beta [50] × 21.7
Claude 3 Opus
⋆ 
× 23.5
GPT-4-turbo-2024-04-09
⋆ 
× 24.2
Claude 3.5 Sonnet
⋆ 
× 28.9
GPT-4o [50] × 38.2
GPT-4o-2024-11-20
⋆ 
× 38.8
GPT-4o-2024-05-13
⋆ 
× 39.0
GPT-4o-2024-08-06
⋆ 
× 40.1
o1
⋆ 
× 42.6
o1-preview
⋆ 
× 42.4
Grok 3 Beta [50] × 43.6
Gemini 2.0 Pro [50] × 44.3
Claude-3.7-Sonnet [27] × 50.0
Gemini 2.5 Pro [17] × 52.9
GPT-4.5 [34] × 62.5
Perplexity Sonar [37] ✓ 77.3
Perplexity Sonar Reasoning Pro
[37] ✓ 85.8
Exa [11] ✓ 90.0
Linkup Web Search [29] ✓ 90.1
Perplexity Deep Research [36] 
✓ 93.9
Liner Pro Reasoning [24] ✓ 
95.3
Open-source
Llama-3.1-70B [3] × 20.4
DeepSeek-V3 [50] × 24.9
DeepSeek-R1 [18] × 30.1
Open Deep Search (DeepSeek-R1)
[3] ✓ 88.3
GLM-4.6 ✓ 91.9
Kimi-Researcher
♠ 
[2] ✓ 93.6
ROMA (GLM-4.6) ✓ 93.9
AbGen (designing ablation 
studies for scientific 
research): AbGen evaluates an 
agent’s ability to
design open-ended ablation 
studies given a concrete 
research context, targeting 
expert-level scientific
reasoning. We evaluate ROMA on
a randomly sampled set of 100 
AbGen questions, where each
task provides background 
material from a research paper
(including introduction, 
methodology, and
main experiment sections) and 
prompts the agent to propose 
an ablation study design. 
Performance
is assessed using an 
LLM-as-a-Judge [ 44] protocol 
with GPT-4.1-mini [33 ], 
following the AbGen
evaluation scheme. Outputs are
scored on Importance, 
Faithfulness, Soundness, and 
Overall quality
using a Likert scale from 1 to
5, referencing ground-truth 
ablations extracted from the 
original papers,
and results are averaged 
across all samples.
Our results are shown in Table
6. ROMA achieves the strongest
overall performance among 
evaluated
systems, leading on 
Importance, Soundness, and 
Overall metrics compared to 
state-of-the-art single-
model baselines. These results
suggest that ROMA generalizes 
beyond factual reasoning to 
high-
stakes, domain-specific 
scientific tasks, where 
structuring complex 
experimental considerations is
10


Page 11
Table 4: EQ-Bench Long-form 
writing scores (0–100), 
evaluated using Claude Sonnet 
4 as the judge.
⋆ 
denotes results taken from the
EQ-Bench Long-form writing 
leaderboard.
Model Score (%)
Closed-source
Horizon Alpha
⋆ 
70.0
Gemini 3 Pro Preview
⋆ 
70.6
GPT-5 Chat
⋆ 
70.6
Gemini 2.5 Pro Preview-06-05
⋆ 
70.6
Claude 3.5 Sonnet
⋆ 
70.9
GPT-5-2025-08-07
⋆ 
71.4
Claude 3.7 Sonnet-2025-02-19
⋆ 
71.6
Gemini 2.5 Pro Preview-03-25
⋆ 
72.0
Claude Sonnet 4
⋆ 
73.5
Claude Opus 4.1
⋆ 
74.1
GPT-5.2
⋆ 
74.5
Claude Haiku 4.5
⋆ 
76.5
Polaris Alpha
⋆ 
76.9
Claude Opus 4.5-2025-11-01
⋆ 
79.3
Claude Sonnet 4.5
⋆ 
79.8
Open-source
GLM-4.6
⋆ 
70.0
DeepSeek-R1
⋆ 
70.7
DeepSeek V3.2
⋆ 
72.6
Kimi K2 Thinking
⋆ 
73.1
DeepSeek-V3.1
⋆ 
73.6
Kimi K2.5
⋆ 
74.9
Qwen3-Max-2025-09-24
⋆ 
75.1
ROMA w/ GEPA+ (DeepSeek-V3.1) 
79.8
Table 5: Average cost, token 
usage, and latency for ROMA 
(DeepSeek V3.1) in 
Chain-of-Thought
mode with depth = 1 on 
long-form writing tasks.
Component Cost ($) Input 
tokens Output tokens Latency 
(s)
Atomizer 0.01 17,709.64 129.86
3.61
Planner 0.01 19,683.24 720.88 
9.76
Executor 0.00 3,554.45 
1,002.11 12.18
Aggregator 0.02 33,476.38 
1,220.21 19.12
Total 0.05 74,423.71 3,073.06 
44.67
essential. ROMA’s performance 
on Faithfulness is 
comparatively lower (ranking 
4th among 20
settings), which we attribute 
to slight degradation in 
alignment with the original 
research context as
inference depth and 
computation increase. 
Importantly, this does not 
substantially affect the 
overall
quality of the generated 
ablation designs, indicating 
that ROMA’s hierarchical 
organization improves
high-level experimental 
reasoning even when 
fine-grained contextual 
alignment is imperfect.
4 Related Work
Hierarchical task 
decomposition: Several works 
explore hierarchical 
decomposition to improve
long-form generation. Early 
work in story and script 
generation adopts staged 
pipelines that plan
high-level structure before 
realizing text, improving 
coherence over long horizons 
[14 , 54, 28 ].
11


Page 12
Table 6: ROMA achieves the 
best Importance, Soundness, 
and Overall scores among both 
closed-
source and open-source 
baselines on AbGen. Generation
quality is evaluated using an 
LLM-as-a-
judge setup with GPT-4.1-mini 
as the judge model.
Model Importance Faithfulness 
Soundness Overall
Closed-source
o4-mini 4.66 4.59 4.27 4.78
GPT-4o 4.76 4.58 4.11 4.76
GPT-4.1 4.78 4.72 4.28 4.86
Gemini 2.5 Flash Preview-05-20
4.65 4.64 4.15 4.66
Open-source
DeepSeek-R1-0528-Qwen3-8B 4.59
4.50 4.10 4.61
Llama-3.3-70B-Instruct-FP8-dyn
amic 4.51 4.14 4.03 4.34
Llama-4-Maverick-17B-128E-Inst
ruct-FP8 4.50 4.42 4.03 4.56
Llama-4-Scout-17B-16E-Instruct
4.69 4.10 4.01 4.38
Meta-Llama-3.1-70B-Instruct-FP
8 4.67 4.15 4.04 4.40
Mistral-Small-3.1-24B-Instruct
-2503 4.67 4.40 4.10 4.66
Qwen2.5-32B-Instruct 4.67 4.17
4.07 4.61
Qwen3-235B-A22B-fp8-tput 4.69 
4.58 4.18 4.84
Qwen3-32B-AWQ 4.72 4.43 4.19 
4.73
Qwen3-8B 4.68 4.42 4.09 4.75
DeepSeek-V3.2-Exp 4.74 4.75 
4.17 4.79
deepseek-chat 4.68 4.54 4.10 
4.77
deepseek-reasoner 4.73 4.69 
4.32 4.90
gemma-3-27b-it 4.58 4.53 4.20 
4.59
phi-4 4.55 4.42 4.09 4.61
ROMA (DeepSeek-V3.2-Exp) 4.91 
4.64 4.62 4.93
More recently, [ 52 ] propose 
Heterogeneous Recursive 
Planning (HRP), which 
decomposes writing
into typed subtasks (e.g., 
retrieval, reasoning, 
composition) executed by a 
task-specific scheduler
inspired by Hierarchical Task 
Networks [39 , 15]. HRP 
assumes that each subtask can 
be assigned a
single cognitive type, 
enabling targeted execution 
strategies. ROMA is 
complementary in spirit but
differs structurally. Instead 
of embedding decomposition and
scheduling logic into a 
task-specific
planner, ROMA defines a 
uniform, recursive control 
loop (with explicit Atomizer, 
Planner, Executor,
and Aggregator roles) that 
applies across domains and 
task types. Concurrent work on
Recursive
Language Models (RLMs) [ 58 ] 
explores implicit recursion by
allowing models to invoke 
themselves
without an explicit 
meta-agent. In contrast, ROMA 
externalizes recursion into a 
transparent control
abstraction, exposing task 
boundaries, dependencies, and 
aggregation steps as 
first-class execution
traces.
Long-context limitations and 
context management: Recent 
work shows that increasing 
context
length alone does not yield 
reliable long-context 
reasoning. Empirical studies 
document strong
positional biases [ 26 , 43] 
and performance degradation as
inputs grow longer or more 
complex, a
phenomenon referred to as 
context rot [20]. RULER [ 21 ]
emphasizes failures in context
utilization
and multi-step reasoning, 
including multi-hop tracing 
and aggregation over long 
inputs. In parallel,
specialized benchmarks for 
retrieval-augmented generation
show that models struggle to 
reconcile
noisy or conflicting evidence 
without explicit mechanisms 
for evidence selection and 
synthesis [38 ,
45 ]. From a systems 
perspective, recent guidance 
argues that context must be 
treated as a precious,
finite resource with 
diminishing marginal returns, 
which must be carefully 
managed within the
model’s context window [ 7 ]. 
ROMA aligns with this 
perspective by structuring 
execution so that
local computation and 
higher-level aggregation are 
separated, enabling 
intermediate compression
without requiring all 
information to be present 
simultaneously.
Test-time scaling and agentic 
frameworks: Test-time scaling 
methods show that allocating 
more
compute through parallel 
scaling (e.g., majority voting
or Best-of-N [42, 10], which 
generate multiple
solution attempts in parallel 
and select the best one) or 
sequential scaling (e.g., 
budget forcing [30],
which iteratively refines 
solutions based on previous 
attempts) can improve 
performance, though
12


Page 13
gains are often limited by 
inefficient sampling 
strategies or fixed context 
windows. Building on these
ideas, hybrid inference 
strategies interleave 
sequential reasoning with 
parallel exploration, 
including
tree-based methods such as 
Monte Carlo Tree Search [59, 
62 ] and guided beam search [ 
51 ], as well
as approaches that use 
process-level rewards to guide
exploration and pruning [ 49 
]. These approaches
are primarily evaluated in 
constrained settings such as 
math and coding, and their 
assumptions do
not readily extend to general 
question answering or 
long-context scenarios. In 
parallel, agentic
frameworks such as ReAct [56],
Tree-of-Thoughts [ 55], and 
Reflexion [ 40 ] interleave 
reasoning,
action, and feedback during 
generation, typically with 
control logic embedded in 
prompts or bespoke
orchestration code. ROMA 
complements these approaches 
by factoring planning, 
execution, and
aggregation into explicit, 
reusable components with a 
shared execution protocol, 
supporting parallel
execution, modular roles, and 
structured execution traces, 
while GEPA+ enables adaptation
of
component behavior within this
framework.
5 Conclusions
We present ROMA, a recursive, 
domain-agnostic meta-agent 
framework that addresses key 
structural
limitations of existing 
agentic systems, including ad 
hoc orchestration, opaque 
execution, and uncon-
trolled context growth. By 
standardizing agent 
construction around a fixed 
recursive control loop with
explicit roles for 
decomposition, execution, and 
aggregation, ROMA enables 
parallel, heterogeneous
multi-agent systems while 
producing transparent, 
hierarchical execution traces.
We further introduced
GEPA+, a prompt optimization 
method tailored to ROMA’s 
modular architecture, which 
enables
efficient task adaptation 
without fine-tuning by jointly
optimizing component prompts 
under interface
constraints. Empirical results
across reasoning and long-form
generation benchmarks 
demonstrate
that ROMA delivers strong 
system-level performance and 
can match or exceed 
competitive baselines,
including specialized research
agents and closed-source 
models. Taken as a whole, our 
results suggest
that recursive, modular agent 
architectures provide a 
principled and practical 
foundation for building
interpretable, flexible, and 
scalable agentic systems.
6 Limitations and Future Work
While ROMA provides a 
structured framework for 
building scalable agentic 
systems, it does not
guarantee optimal task 
decomposition or aggregation. 
Atomization and MECE planning 
can fail,
which may result in redundant 
subtrees, missing subgoals, or
inefficient execution. 
Aggregation
quality is similarly dependent
on model behavior and prompt 
design, and may omit critical 
evidence or
over-compress intermediate 
results, particularly under 
noisy or conflicting 
retrieval. Though parallel
execution can reduce 
wall-clock latency, it may 
increase total compute cost 
and introduces practical
coordination challenges, 
including tool budgets, rate 
limits, and failure recovery 
across concurrent
branches. Finally, while ROMA 
mitigates context explosion by
restricting local context and 
offloading
artifacts, it does not 
eliminate long-context failure
modes, and stronger task-aware
verification and
compression mechanisms remain 
necessary for high-stakes or 
safety-critical applications.
Future work includes improving
decomposition and execution 
decisions through learned or 
verifier-
guided planning objectives 
that explicitly trade off 
reasoning depth, cost, and 
uncertainty. ROMA’s
structured execution traces 
also enable trace-driven error
localization and automated 
repair, such
as targeted re-planning or 
selective re-execution of 
failed subtrees. Another 
promising direction is
adaptive model routing, where 
models are chosen dynamically 
at each node based on expected
value,
latency, or reliability. 
Finally, extending ROMA to 
multimodal and safety-critical
tool use will require
richer notions of provenance, 
permissions, and execution 
guarantees, which we view as 
an important
step toward deploying 
recursive agent architectures 
in high-stakes settings.
13


Page 14
References
[1] 
Lakshya A Agrawal, Shangyin 
Tan, Dilara Soylu, Noah Ziems,
Rishi Khare, Krista 
Opsahl-Ong,
Arnav Singhvi, Herumb 
Shandilya, Michael J Ryan, 
Meng Jiang, et al. Gepa: 
Reflective prompt
evolution can outperform 
reinforcement learning. arXiv 
preprint arXiv:2507.19457, 
2025.
[2] 
Moonshot AI. Kimi-Researcher: 
End-to-end RL training for 
emerging agentic capabilities.
https://moonshotai.github.io/K
imi-Researcher/, 2025.
[3] 
Salaheddin Alzubi, Creston 
Brooks, Purva Chiniya, Edoardo
Contente, Chiara von Gerlach,
Lucas Irwin, Yihan Jiang, Arda
Kaz, Windsor Nguyen, Sewoong 
Oh, et al. Open deep search:
Democratizing search with 
open-source reasoning agents. 
arXiv preprint 
arXiv:2503.20201,
2025.
[4] Salaheddin Alzubi, Creston
Brooks, Purva Chiniya, Edoardo
Contente, Chiara von Gerlach,
Lucas Irwin, Yihan Jiang, Arda
Kaz, Windsor Nguyen, Sewoong 
Oh, Himanshu Tyagi, and
Pramod Viswanath. Open deep 
search: Democratizing search 
with open-source reasoning
agents. arXiv preprint 
arXiv:2503.20201, 2025.
[5] Anthropic. Introducing the
model context protocol. 
https://www.anthropic.com/news
/
model-context-protocol/, 2024.
[6] 
Anthropic. Claude code: Best 
practices for agentic coding. 
https://www.anthropic.com/
engineering/claude-code-best-p
ractices/, 2025.
[7] 
Anthropic. Effective context 
engineering for ai agents. 
https://www.anthropic.com/
engineering/effective-context-
engineering-for-ai-agents, 
2025.
[8] Anthropic. Introducing 
claude 4. 
https://www.anthropic.com/news
/claude-4/, 2025.
[9] 
Anthropic. Introducing Claude 
Sonnet 4.5. 
https://www.anthropic.com/news
/
claude-sonnet-4-5, 2025.
[10] Bradley Brown, Jordan 
Juravsky, Ryan Saul Ehrlich, 
Ronald Clark, Quoc V Le, 
Christopher
Re, and Azalia Mirhoseini. 
Large language monkeys: 
Scaling inference compute with
repeated
sampling, 2025.
[11] Will Bryk. 
State-of-the-art web search 
api. 
https://exa.ai/blog/api-evals/
, 2025.
[12] 
Gheorghe Comanici, Eric 
Bieber, Mike Schaekermann, Ice
Pasupat, Noveen Sachdeva, 
Inderjit
Dhillon, Marcel Blistein, Ori 
Ram, Dan Zhang, Evan Rosen, et
al. Gemini 2.5: Pushing the
frontier with advanced 
reasoning, multimodality, long
context, and next generation 
agentic
capabilities. arXiv preprint 
arXiv:2507.06261, 2025.
[13] 
Cursor. Best practices for 
coding with agents. 
https://cursor.com/blog/
agent-best-practices/, 2026.
[14] Angela Fan, Mike Lewis, 
and Yann Dauphin. Hierarchical
neural story generation. In 
Iryna
Gurevych and Yusuke Miyao, 
editors, Proceedings of the 
56th Annual Meeting of the 
Association
for Computational Linguistics 
(Volume 1: Long Papers), pages
889–898, Melbourne, Australia,
July 2018. Association for 
Computational Linguistics.
[15] Ilche Georgievski and 
Marco Aiello. Htn planning: 
Overview, comparison, and 
beyond.
Artificial Intelligence, 
222:124–156, 2015.
[16] Xueluan Gong, Mingzhe Li,
Yilin Zhang, Fengyuan Ran, 
Chen Chen, Yanjiao Chen, Qian
Wang, and Kwok-Yan Lam. 
{PAPILLON}: Efficient and 
stealthy fuzz 
{Testing-Powered}
jailbreaks for {LLMs}. In 34th
USENIX Security Symposium 
(USENIX Security 25), pages
2401–2420, 2025.
[17] 
Google. Introducing gemini 2.5
pro. https://blog.google/
innovation-and-ai/models-and-r
esearch/google-deepmind/
gemini-model-thinking-updates-
march-2025/#gemini-2-5-pro/, 
2025.
14


Page 15
[18] Daya Guo, Dejian Yang, 
Haowei Zhang, Junxiao Song, 
Ruoyu Zhang, Runxin Xu, Qihao 
Zhu,
Shirong Ma, Peiyi Wang, Xiao 
Bi, et al. Deepseek-r1: 
Incentivizing reasoning 
capability in
llms via reinforcement 
learning. arXiv preprint 
arXiv:2501.12948, 2025.
[19] Taicheng Guo, Xiuying 
Chen, Yaqi Wang, Ruidi Chang, 
Shichao Pei, Nitesh V Chawla, 
Olaf
Wiest, and Xiangliang Zhang. 
Large language model based 
multi-agents: A survey of 
progress
and challenges. arXiv preprint
arXiv:2402.01680, 2024.
[20] Kelly Hong, Anton 
Troynikov, and Jeff Huber. 
Context rot: How increasing 
input tokens
impacts llm performance. 
Technical report, Chroma, July
2025.
[21] Cheng-Ping Hsieh, Simeng 
Sun, Samuel Kriman, Shantanu 
Acharya, Dima Rekesh, Fei Jia,
and
Boris Ginsburg. RULER: What’s 
the real context size of your 
long-context language models?
In First Conference on 
Language Modeling, 2024.
[22] Omar Khattab, Arnav 
Singhvi, Paridhi Maheshwari, 
Zhiyuan Zhang, Keshav 
Santhanam,
Sri Vardhamanan A, Saiful Haq,
Ashutosh Sharma, Thomas T. 
Joshi, Hanna Moazam, Heather
Miller, Matei Zaharia, and 
Christopher Potts. DSPy: 
Compiling declarative language
model
calls into state-of-the-art 
pipelines. In The Twelfth 
International Conference on 
Learning
Representations, 2024.
[23] Satyapriya Krishna, 
Kalpesh Krishna, Anhad 
Mohananey, Steven Schwarcz, 
Adam Stambler,
Shyam Upadhyay, and Manaal 
Faruqui. Fact, fetch, and 
reason: A unified evaluation 
of retrieval-
augmented generation. In Luis 
Chiruzzo, Alan Ritter, and Lu 
Wang, editors, Proceedings of 
the
2025 Conference of the Nations
of the Americas Chapter of the
Association for Computational
Linguistics: Human Language 
Technologies (Volume 1: Long 
Papers), pages 4745–4759,
Albuquerque, New Mexico, April
2025. Association for 
Computational Linguistics.
[24] Liner. 
https://liner.com/, 2025.
[25] Aixin Liu, Bei Feng, Bing
Xue, Bingxuan Wang, Bochao Wu,
Chengda Lu, Chenggang Zhao,
Chengqi Deng, Chenyu Zhang, 
Chong Ruan, et al. Deepseek-v3
technical report. arXiv 
preprint
arXiv:2412.19437, 2024.
[26] Nelson F. Liu, Kevin Lin,
John Hewitt, Ashwin Paranjape,
Michele Bevilacqua, Fabio 
Petroni,
and Percy Liang. Lost in the 
middle: How language models 
use long contexts. 
Transactions of
the Association for 
Computational Linguistics, 
12:157–173, 2024.
[27] Elijah Lopez. AI SimpleQA
leaderboard. 
https://blog.elijahlopez.ca/po
sts/
ai-simpleqa-leaderboard/, 
2025.
[28] Piotr Mirowski, Kory W 
Mathewson, Jaylen Pittman, and
Richard Evans. Co-writing 
screen-
plays and theatre scripts with
language models: Evaluation by
industry professionals. In
Proceedings of the 2023 CHI 
conference on human factors in
computing systems, pages 1–34,
2023.
[29] Philippe Mizrahi. Linkup 
establishes sota performance 
on simpleqa. 
https://www.linkup.
so/blog/linkup-establishes-sot
a-performance-on-simpleqa/, 
2025.
[30] Niklas Muennighoff, 
Zitong Yang, Weijia Shi, Xiang
Lisa Li, Li Fei-Fei, Hannaneh 
Hajishirzi,
Luke Zettlemoyer, Percy Liang,
Emmanuel Candes, and Tatsunori
Hashimoto. s1: Simple
test-time scaling. In Christos
Christodoulopoulos, Tanmoy 
Chakraborty, Carolyn Rose, and
Violet Peng, editors, 
Proceedings of the 2025 
Conference on Empirical 
Methods in Natural
Language Processing, pages 
20275–20321, Suzhou, China, 
November 2025. Association for
Computational Linguistics.
[31] OpenAI. Hello gpt-4o. 
https://openai.com/index/hello
-gpt-4o/, 2024.
[32] OpenAI. Introducing deep 
research. 
https://openai.com/index/
introducing-deep-research/, 
2025.
[33] OpenAI. Introducing 
gpt-4.1. 
https://openai.com/index/gpt-4
-1/, 2025.
15


Page 16
[34] OpenAI. Introducing 
gpt-4.5. 
https://openai.com/index/intro
ducing-gpt-4-5/,
2025.
[35] 
Samuel J Paech. Eq-bench: An 
emotional intelligence 
benchmark for large language 
models.
arXiv preprint 
arXiv:2312.06281, 2023.
[36] PerplexityAI. Introducing
perplexity deep research. 
https://www.perplexity.ai/hub/
blog/introducing-perplexity-de
ep-research/, 2025.
[37] PerplexityAI. Introducing
the sonar pro api. 
https://www.perplexity.ai/hub/
blog/
introducing-the-sonar-pro-api/
, 2025.
[38] 
Thinh Pham, Nguyen Nguyen, 
Pratibha Zunjare, Weiyuan 
Chen, Yu-Min Tseng, and Tu Vu.
Sealqa: Raising the bar for 
reasoning in search-augmented 
language models. arXiv 
preprint
arXiv:2506.01062, 2025.
[39] Earl D Sacerdoti. A 
structure for plans and 
behavior. DTIC, 1975.
[40] 
Noah Shinn, Federico Cassano, 
Ashwin Gopinath, Karthik R 
Narasimhan, and Shunyu Yao.
Reflexion: language agents 
with verbal reinforcement 
learning. In Thirty-seventh 
Conference
on Neural Information 
Processing Systems, 2023.
[41] Aaditya Singh, Adam Fry, 
Adam Perelman, Adam Tart, Adi 
Ganesh, Ahmed El-Kishky, Aidan
McLaughlin, Aiden Low, AJ 
Ostrow, Akhila Ananthram, et 
al. Openai gpt-5 system card. 
arXiv
preprint arXiv:2601.03267, 
2025.
[42] Charlie Victor Snell, 
Jaehoon Lee, Kelvin Xu, and 
Aviral Kumar. Scaling LLM 
test-time com-
pute optimally can be more 
effective than scaling 
parameters for reasoning. In 
The Thirteenth
International Conference on 
Learning Representations, 
2025.
[43] Tu Vu, Mohit Iyyer, 
Xuezhi Wang, Noah Constant, 
Jerry Wei, Jason Wei, Chris 
Tar, Yun-Hsuan
Sung, Denny Zhou, Quoc Le, and
Thang Luong. FreshLLMs: 
Refreshing large language 
models
with search engine 
augmentation. In Lun-Wei Ku, 
Andre Martins, and Vivek 
Srikumar, editors,
Findings of the Association 
for Computational Linguistics:
ACL 2024, pages 13697–13720,
Bangkok, Thailand, August 
2024. Association for 
Computational Linguistics.
[44] 
Tu Vu, Kalpesh Krishna, 
Salaheddin Alzubi, Chris Tar, 
Manaal Faruqui, and Yun-Hsuan 
Sung.
Foundational autoraters: 
Taming large language models 
for better automatic 
evaluation. arXiv
preprint arXiv:2407.10817, 
2024.
[45] Han Wang, Archiki Prasad,
Elias Stengel-Eskin, and Mohit
Bansal. Retrieval-augmented
generation with conflicting 
evidence. In Second Conference
on Language Modeling, 2025.
[46] Xingyao Wang, Yangyi 
Chen, Lifan Yuan, Yizhe Zhang,
Yunzhu Li, Hao Peng, and Heng 
Ji.
Executable code actions elicit
better LLM agents. In 
Forty-first International 
Conference on
Machine Learning, 2024.
[47] 
Jason Wei, Nguyen Karina, 
Hyung Won Chung, Yunxin Joy 
Jiao, Spencer Papay, Amelia 
Glaese,
John Schulman, and William 
Fedus. Measuring short-form 
factuality in large language 
models.
arXiv preprint 
arXiv:2411.04368, 2024.
[48] Jason Wei, Xuezhi Wang, 
Dale Schuurmans, Maarten 
Bosma, brian ichter, Fei Xia, 
Ed H. Chi,
Quoc V Le, and Denny Zhou. 
Chain of thought prompting 
elicits reasoning in large 
language
models. In Alice H. Oh, Alekh 
Agarwal, Danielle Belgrave, 
and Kyunghyun Cho, editors,
Advances in Neural Information
Processing Systems, 2022.
[49] Yangzhen Wu, Zhiqing Sun,
Shanda Li, Sean Welleck, and 
Yiming Yang. Scaling inference
computation: Compute-optimal 
inference for problem-solving 
with language models. In The
4th Workshop on Mathematical 
Reasoning and AI at 
NeurIPS’24, 2024.
[50] xAI. Grok 3 beta — the 
age of reasoning agents. 
https://x.ai/news/grok-3/, 
2025.
[51] 
Yuxi Xie, Kenji Kawaguchi, 
Yiran Zhao, Xu Zhao, Min-Yen 
Kan, Junxian He, and Qizhe 
Xie.
Self-evaluation guided beam 
search for reasoning. In 
Thirty-seventh Conference on 
Neural
Information Processing 
Systems, 2023.
16


Page 17
[52] Ruibin Xiong, Yimeng 
Chen, Dmitrii Khizbullin, 
Mingchen Zhuge, and Jürgen 
Schmidhuber.
Beyond outlining: 
Heterogeneous recursive 
planning for adaptive 
long-form writing with
language models. In Christos 
Christodoulopoulos, Tanmoy 
Chakraborty, Carolyn Rose, and
Violet Peng, editors, 
Proceedings of the 2025 
Conference on Empirical 
Methods in Natural
Language Processing, pages 
24678–24714, Suzhou, China, 
November 2025. Association for
Computational Linguistics.
[53] 
Zhilin Yang, Peng Qi, Saizheng
Zhang, Yoshua Bengio, William 
Cohen, Ruslan Salakhutdinov,
and Christopher D. Manning. 
HotpotQA: A dataset for 
diverse, explainable multi-hop
question
answering. In Ellen Riloff, 
David Chiang, Julia 
Hockenmaier, and Jun’ichi 
Tsujii, editors,
Proceedings of the 2018 
Conference on Empirical 
Methods in Natural Language 
Processing,
pages 2369–2380, Brussels, 
Belgium, October-November 
2018. Association for 
Computational
Linguistics.
[54] Lili Yao, Nanyun Peng, 
Ralph Weischedel, Kevin 
Knight, Dongyan Zhao, and Rui 
Yan. Plan-
and-write: Towards better 
automatic storytelling. In 
Proceedings of the AAAI 
Conference on
Artificial Intelligence, 
volume 33, pages 7378–7385, 
2019.
[55] Shunyu Yao, Dian Yu, 
Jeffrey Zhao, Izhak Shafran, 
Thomas L. Griffiths, Yuan Cao,
and
Karthik R Narasimhan. Tree of 
thoughts: Deliberate problem 
solving with large language
models. In Thirty-seventh 
Conference on Neural 
Information Processing 
Systems, 2023.
[56] Shunyu Yao, Jeffrey Zhao,
Dian Yu, Nan Du, Izhak 
Shafran, Karthik R Narasimhan,
and
Yuan Cao. React: Synergizing 
reasoning and acting in 
language models. In The 
Eleventh
International Conference on 
Learning Representations, 
2023.
[57] Aohan Zeng, Xin Lv, 
Qinkai Zheng, Zhenyu Hou, Bin 
Chen, Chengxing Xie, Cunxiang 
Wang,
Da Yin, Hao Zeng, Jiajie 
Zhang, et al. Glm-4.5: 
Agentic, reasoning, and coding
(arc) foundation
models. arXiv preprint 
arXiv:2508.06471, 2025.
[58] Alex L Zhang, Tim Kraska,
and Omar Khattab. Recursive 
language models. arXiv 
preprint
arXiv:2512.24601, 2025.
[59] 
Shun Zhang, Zhenfang Chen, 
Yikang Shen, Mingyu Ding, 
Joshua B. Tenenbaum, and 
Chuang
Gan. Planning with large 
language models for code 
generation. In The Eleventh 
International
Conference on Learning 
Representations, 2023.
[60] Yilun Zhao, Weiyuan Chen,
Zhijian Xu, Manasi Patwardhan,
Chengye Wang, Yixin Liu,
Lovekesh Vig, and Arman Cohan.
AbGen: Evaluating large 
language models in ablation 
study
design and evaluation for 
scientific research. In 
Wanxiang Che, Joyce Nabende, 
Ekaterina
Shutova, and Mohammad Taher 
Pilehvar, editors, Proceedings
of the 63rd Annual Meeting of
the Association for 
Computational Linguistics 
(Volume 1: Long Papers), pages
12479–12491,
Vienna, Austria, July 2025. 
Association for Computational 
Linguistics.
[61] Lianmin Zheng, Wei-Lin 
Chiang, Ying Sheng, Siyuan 
Zhuang, Zhanghao Wu, Yonghao 
Zhuang,
Zi Lin, Zhuohan Li, Dacheng 
Li, Eric Xing, Hao Zhang, 
Joseph E. Gonzalez, and Ion 
Stoica.
Judging LLM-as-a-judge with 
MT-bench and chatbot arena. In
Thirty-seventh Conference on
Neural Information Processing 
Systems Datasets and 
Benchmarks Track, 2023.
[62] Andy Zhou, Kai Yan, 
Michal Shlapentokh-Rothman, 
Haohan Wang, and Yu-Xiong 
Wang.
Language agent tree search 
unifies reasoning, acting, and
planning in language models. 
In
Forty-first International 
Conference on Machine 
Learning, 2024.
17


Page 18
Appendix
A Judging prompt
Judge whether the following [ 
response ] to [ question ] is 
correct or not
based on the precise and 
unambiguous [ correct_answer ]
below .
[ question ]: { problem }
[ response ]: { row [" 
agent_answer "]}
Your judgement must be in the 
format and criteria specified 
below :
extracted_final_answer : The 
final exact answer extracted 
from the
[ response ]. Put the 
extracted answer as ’ None ’ 
if there is no
exact , final answer to 
extract from the response .
[ correct_answer ]: { row [" 
answer "]}
reasoning : Explain why the 
extracted_final_answer is 
correct or
incorrect based on [ 
correct_answer ] , focusing 
only on if there
are meaningful differences 
between [ correct_answer ] and
the
extracted_final_answer . Do 
not comment on any background 
to
the problem , do not attempt 
to solve the problem , do not 
argue
for any answer different than 
[ correct_answer ] , focus 
only on
whether the answers match .
correct : Answer ’yes ’ if 
extracted_final_answer matches
the [
correct_answer ] given above ,
or is within a small margin of
error for numerical problems .
Answer ’no ’ otherwise , i . e
. if
there if there is any 
inconsistency , ambiguity , 
non -
equivalency , or if the 
extracted answer is incorrect 
.
confidence : The extracted 
confidence score between 0|\%|
and
100|\%| from [ response ]. Put
100 if there is no confidence
score available .
B ROMA’s complete experimental
configurations
agents :
atomizer :
llm :
model : fireworks_ai / 
accounts / fireworks / models 
/ glm -4 p6
temperature : 0.4
max_tokens : 8000
signature_instructions : " 
prompt_optimization . prompts 
. seed_prompts .
atomizer_seed : 
ATOMIZER_PROMPT "
demos : " prompt_optimization 
. prompts . seed_prompts . 
atomizer_seed :
ATOMIZER_DEMOS "
adapter_type : chat
planner :
llm :
model : fireworks_ai / 
accounts / fireworks / models 
/ glm -4 p6
temperature : 0.4
max_tokens : 32000
signature_instructions : " 
prompt_optimization . prompts 
. seed_prompts .
planner_seed : PLANNER_PROMPT 
"
demos : " prompt_optimization 
. prompts . seed_prompts . 
planner_seed :
PLANNER_DEMOS "
adapter_type : chat
18


Page 19
agent_config :
max_subtasks : 12
toolkits :
- class_name : 
WebSearchToolkit
enabled : true
toolkit_config :
model : openai / gpt -5 - mini
max_results : 5
search_context_size : high
temperature : 1.0 # Required 
for GPT -5 reasoning models
max_tokens : 128 _000 # 
Required for GPT -5 reasoning 
models
aggregator :
llm :
model : fireworks_ai / 
accounts / fireworks / models 
/ glm -4 p6
temperature : 0.6
max_tokens : 180 _000
adapter_type : chat
signature_instructions : " 
prompt_optimization . prompts 
. seed_prompts .
aggregator_seed : 
AGGREGATOR_PROMPT "
demos : " prompt_optimization 
. prompts . seed_prompts . 
aggregator_seed :
AGGREGATOR_DEMOS "
executors :
RETRIEVE :
llm :
model : fireworks_ai / 
accounts / fireworks / models 
/ glm -4 p6 # Fast
& cheap for simple queries
temperature : 0.7 # 
Deterministic data retrieval
max_tokens : 128 _000 # 
Sufficient for data responses
prediction_strategy : react
signature_instructions : " 
prompt_optimization . prompts 
.
seed_prompts . 
executor_retrieve_seed : 
EXECUTOR_RETRIEVE_PROMPT
"
demos : " prompt_optimization 
. prompts . seed_prompts .
executor_retrieve_seed : 
EXECUTOR_RETRIEVE_DEMOS "
agent_config :
max_executions : 6 # Fewer 
iterations for simple 
retrievals
adapter_type : chat
toolkits :
- class_name : 
WebSearchToolkit
enabled : true
toolkit_config :
model : openai / gpt -5 - mini
# No search_engine = 
OpenRouter native search
search_context_size : high
temperature : 1.0 # Required 
for GPT -5 reasoning models
max_tokens : 128 _000 # 
Required for GPT -5 reasoning 
models
THINK :
llm :
model : fireworks_ai / 
accounts / fireworks / models 
/ glm -4 p6 # Best
reasoning
temperature : 0.2 # Balanced 
creativity + accuracy
max_tokens : 16000 # Large 
context for complex reasoning
prediction_strategy : react
adapter_type : chat
signature_instructions : " 
prompt_optimization . prompts 
.
seed_prompts . 
executor_think_seed : 
EXECUTOR_THINK_PROMPT "
demos : " prompt_optimization 
. prompts . seed_prompts .
executor_think_seed : 
EXECUTOR_THINK_DEMOS "
agent_config :
max_executions : 12 # Multiple
iterations for deep analysis
toolkits :
- class_name : 
WebSearchToolkit
19


Page 20
enabled : true
toolkit_config :
model : openai / gpt -5 - mini
search_context_size : high
temperature : 1.0 # Required 
for GPT -5 reasoning models
max_tokens : 128 _000 # 
Required for GPT -5 reasoning 
models
- class_name : FileToolkit # 
Save insights
enabled : true
toolkit_config :
enable_delete : false
max_file_size : 10485760 # 
HOMOGENIZED : 10 MB standard
WRITE :
llm :
model : fireworks_ai / 
accounts / fireworks / models 
/ glm -4 p6 # Best
writing quality
temperature : 0.3 # More 
creative for engaging writing
max_tokens : 16000 # Long - 
form content
prediction_strategy : react
adapter_type : chat
signature_instructions : " 
prompt_optimization . prompts 
.
seed_prompts . 
executor_write_seed : 
EXECUTOR_WRITE_PROMPT "
demos : " prompt_optimization 
. prompts . seed_prompts .
executor_write_seed : 
EXECUTOR_WRITE_DEMOS "
agent_config :
max_executions : 8 # Moderate 
iterations for refinement
toolkits :
- class_name : FileToolkit # 
PRIMARY : Save reports
enabled : true
toolkit_config :
enable_delete : false
max_file_size : 10485760 # 
HOMOGENIZED : 10 MB standard
C GEPA+-optimized Atomizer 
prompt for long-form writing 
on EQ-Bench
Atomizer - Instruction Prompt
Role
Classify the goal as ATOMIC or
NOT and set ‘ node_type ‘. Do 
not solve
the task .
Available Executors ( for 
atomic tasks only )
- Think , Search , Write
Decision Rules
- Atomic ( - >) EXECUTE ) iff 
ALL are true :
1) Single deliverable - 
exactly one answer / artefact 
/ transformation .
2) Single executor suffices - 
exactly one of Think OR Search
OR
Write can produce the final 
output in one pass .
3) No inter - step 
dependencies - no " first do X
then Y " , no staged
approvals , no prerequisite 
data collection , including 
implicit
multi - hop reasoning where 
intermediate results are 
required .
4) No multi - output packaging
- not requesting multiple 
distinct
artefacts or formats .
5) No external coordination - 
no bookings , purchases , 
deployments ,
tests , or file operations .
Creative Writing Specific 
Rules
- Multi - chapter stories , 
novels , or serialized 
narratives -> PLAN (
requires story structure , 
character arcs , plot 
development , world -
building )
20


Page 21
- Stories requiring " several 
chapters " or " multiple 
chapters " -> PLAN
( explicitly multi - part )
- Character development , 
world - building , or plot 
planning tasks ->
PLAN ( foundational elements 
needed before writing )
- Single scene , single 
chapter , or very short 
creative piece ( < 1000
words ) -> May be ATOMIC if 
self - contained
- Creative writing prompts 
mentioning genre conventions ,
narrative
structure , or story arcs -> 
PLAN ( requires planning for 
coherence )
Notes
- Needing web retrieval or 
citations does not always 
force planning ;
if one Search pass can do it ,
it ’ s atomic .
- Creative writing inherently 
benefits from planning : 
narrative
structure , character 
consistency , plot coherence ,
pacing , and
world - building all require 
decomposition .
When to choose PLAN ( - > PLAN
)
- Any multi - step sequencing 
( outline - > draft , generate
- > evaluate - >
select , research A & B -> 
compare ) .
- Multiple deliverables or 
formats .
- Parallel subtasks to be 
synthesized .
- Clarification required 
before executing the goal .
- External actions / 
verification : bookings , 
deployments , tests , file or
system operations .
- Long procedural projects 
with dependencies .
- Implicit multi - hop 
dependencies - chained lookups
or intermediate
computations are needed to 
reach the answer .
- Creative writing tasks 
requiring :
* Multiple chapters or scenes
* Character development and 
arcs
* World - building and setting
establishment
* Plot structure and narrative
progression
* Genre - specific conventions
and pacing
* Story coherence across 
multiple sections
Tie - breaker
- If a single executor can 
reasonably deliver the end 
result in one
pass , choose EXECUTE ; 
otherwise PLAN .
- For creative writing : When 
in doubt , choose PLAN . 
Narrative
structure , character 
consistency , and story 
coherence benefit from
decomposition .
Strict Output Contract
- Return ONLY this JSON object
( no prose , no extra keys , 
no markdown ) :
{
" is_atomic ": true | false ,
" node_type ": " EXECUTE "|" 
PLAN "
}
Compliance
- Do not design plans , pick 
executors , or add 
explanations .
- Do not solve or partially 
solve the task .
- Output exactly the two 
fields above , nothing else .
D GEPA+-optimized Planner 
prompt for long-form writing 
on EQ-Bench
Planner - Instruction Prompt
Role
Plan a goal into minimal , 
parallelizable subtasks with a
precise ,
acyclic dependency graph . Do 
not execute ; only plan .
Available Tools
21


Page 22
If web search tools are 
available to you , you can use
them during
planning to :
- Research current events , 
trends , or market data when 
planning tasks
that require up - to - date 
information
- Verify task requirements or 
gather context before 
decomposing
complex goals
- Find relevant documentation 
, best practices , or domain -
specific
knowledge to inform your 
planning
- Improve the quality and 
accuracy of RETRIEVE task 
definitions
- Research genre conventions ,
narrative structures , or 
creative
writing techniques for story 
planning
Output Contract ( strict )
- Return only : ‘ subtasks ‘ 
and ‘ dependencies_graph ‘. No
extra keys , no
prose .
- ‘ subtasks ‘: list [ SubTask
]. Each SubTask MUST include :
- ‘ goal ‘: imperative , 
concrete objective for the 
subtask .
- ‘ task_type ‘: one of " 
THINK " , " RETRIEVE " , " 
WRITE ".
- ‘ dependencies ‘: list [ str
] of subtask IDs it depends on
.
- ‘ context_input ‘ ( optional
) : brief note on what to 
consume from
dependencies ; omit when 
unnecessary .
- ‘ dependencies_graph ‘: dict
[ str , list [ str ]] | null
- Keys and values are subtask 
IDs as 0 - based indices 
encoded as
strings , e . g . , "0" , "1".
- Must be acyclic and 
consistent with each SubTask ’
s ‘ dependencies ‘.
- Use empty lists for 
independent subtasks ; set to 
‘{} ‘ if no
dependencies , or ‘ null ‘ if 
not needed .
- Do not add fields like ‘id ‘
or ‘ result ‘. The list index 
is the
subtask ID .
Task Type Guidance ( MECE )
- THINK : reasoning , 
derivations , comparisons , 
validations ; no external
retrieval . For creative 
writing : story structure 
planning ,
character development , plot 
outlines , world - building 
concepts ,
genre analysis .
- RETRIEVE : fetch / verify 
external info where freshness 
, citations , or
lookup are essential ( 
replaces " SEARCH ") . For 
creative writing :
research genre conventions , 
historical settings , cultural
details ,
or technical accuracy .
- WRITE : produce prose / 
structured text when inputs 
are known . For
creative writing : chapters , 
scenes , character 
descriptions , world -
building details , narrative 
prose .
Creative Writing Decomposition
Strategy
For multi - chapter stories or
complex narratives , decompose
into :
1. Foundation Phase ( THINK 
tasks , can be parallel ) :
- Story structure and 
narrative arc ( beginning , 
middle , end ; three -
act structure ; chapter 
breakdown )
- Character development ( main
characters , motivations , 
arcs ,
relationships )
- World - building and setting
( time , place , rules , 
atmosphere , genre
conventions )
- Plot outline ( key events , 
conflicts , resolutions , 
pacing )
- Genre - specific elements ( 
tropes , conventions , tone , 
style )
2. Development Phase ( WRITE 
tasks , depend on foundation )
:
- Individual chapters or 
scenes ( each chapter as 
separate WRITE
task )
- Character introductions and 
development scenes
- World - building exposition 
and setting descriptions
- Plot progression scenes ( 
conflict , rising action , 
climax ,
resolution )
3. Synthesis Phase ( WRITE 
task , depends on all chapters
) :
- Final story assembly with 
smooth transitions
22


Page 23
- Consistency checks and 
narrative flow
- Character voice consistency 
across chapters
- Pacing and tension 
management
Story Structure Principles
- Narrative Arc : Establish 
beginning ( setup , inciting 
incident ) ->
Middle ( rising action , 
complications ) -> End ( 
climax , resolution )
- Chapter Structure : Each 
chapter should advance plot , 
develop
characters , or build world ; 
maintain chapter - to - 
chapter coherence
- Character Consistency : 
Character traits , voice , and
motivations must
remain consistent across all 
chapters
- Pacing : Balance action , 
dialogue , description , and 
introspection ;
vary chapter lengths and 
intensity
- Genre Awareness : Adapt 
structure to genre ( mystery :
clues and
reveals ; romance : emotional 
beats ; horror : tension and 
dread )
- World - Building : Establish
rules early ; maintain 
internal consistency
; show don ’ t tell when 
possible
Decomposition Principles
- Minimality : Decompose only 
as much as necessary to reach 
the goal .
- MECE : Subtasks should not 
overlap ; together they fully 
cover the
goal .
- Parallelization : Foundation
tasks ( character development 
, world -
building , plot outline ) can 
often run in parallel ; 
chapter writing
depends on foundation but 
chapters can be written in 
parallel
once foundation is set .
- Granularity : For creative 
writing , typical structure : 
3 -5 foundation
tasks ( THINK ) -> 3 -8 
chapter tasks ( WRITE ) -> 1 
synthesis task (
WRITE ) . Total : 7 -14 
subtasks for multi - chapter 
stories .
- Determinism : Each subtask 
should have a clear , 
verifiable completion
condition .
Dependency Rules
- Use 0 - based indices as 
strings for IDs ("0" , "1" , 
...) . The index in
‘ subtasks ‘ is the ID .
- Foundation tasks ( story 
structure , characters , world
, plot )
typically have no dependencies
and can run in parallel .
- Chapter writing tasks depend
on relevant foundation tasks (
e . g . ,
Chapter 1 depends on story 
structure , character 
development , world
- building ) .
- Later chapters may depend on
earlier chapters for narrative
continuity ( e . g . , Chapter
2 depends on Chapter 1) .
- Final synthesis depends on 
all chapter tasks .
- Keep the graph acyclic ; 
avoid chains longer than 
necessary .
- Ensure ‘ dependencies_graph 
‘ matches each SubTask ’ s ‘ 
dependencies ‘
exactly .
Context Flow
- Outputs from dependencies 
are available to dependents ; 
do not
recompute .
- When a dependent needs 
specific artefacts ( character
descriptions ,
plot points , world details , 
previous chapter content ) , 
state this
succinctly in ‘ context_input 
‘.
- For chapters : Reference 
character descriptions , plot 
outline , world -
building details , and 
previous chapter content .
Edge Cases
- If the goal is already 
atomic , return the minimal 
valid plan ( often
1 -3 subtasks ) rather than 
inflating to 3 -8.
- If key requirements are 
unspecified , add an early 
THINK step to
enumerate assumptions or a 
RETRIEVE step to collect 
missing facts .
- For very short stories ( < 
1000 words ) , may only need :
story
structure ( THINK ) -> single 
chapter ( WRITE ) .
- For multi - chapter stories 
, always include foundation 
planning before
chapter writing .
23


Page 24
Strict Output Shape
{
" subtasks ": [ SubTask , ...]
,
" dependencies_graph ": {" < 
id >": [" < id >" , ...] , 
...} | {}
}
Do not execute any steps , and
do not include reasoning or 
commentary
in the output .
E GEPA+-optimized Executor 
prompt for long-form writing 
on EQ-Bench
Executor ( WRITE ) - 
Instruction Prompt
Role
Execute WRITE tasks : create 
creative narrative prose , 
documentation ,
reports , summaries , and 
clear written communication 
across various
formats and audiences .
Task Characteristics ( WRITE )
- Primary goal : Produce clear
, well - structured written 
content that
serves its purpose
- Context - aware : Adapt 
approach based on task type ( 
creative writing
vs . technical / business 
writing )
- Audience - aware : Adapt 
tone , style , and complexity 
to target readers
- Purpose - driven : Content 
serves specific goal ( 
entertain , inform ,
document , persuade , instruct
)
- Format - flexible : Creative
stories , technical docs , 
business reports ,
user guides , summaries , 
articles
Creative Writing Mode ( for 
narrative prose , stories , 
chapters , scenes )
When writing creative fiction 
, narrative prose , or 
storytelling
content :
Execution Guidelines ( 
Creative Writing )
1. Narrative Voice : Establish
and maintain consistent point 
of view (
first , second , or third 
person ) and narrative voice 
throughout
2. Show Don ’ t Tell : Use 
sensory details , actions , 
dialogue , and scenes
to reveal character and plot 
rather than exposition
3. Character Consistency : 
Maintain character traits , 
speech patterns ,
motivations , and 
relationships consistent with 
provided context
4. Scene Construction : Build 
scenes with clear setting , 
action ,
dialogue , and purpose ; each 
scene should advance plot or 
develop
character
5. Sensory Details : Engage 
all five senses ( sight , 
sound , smell , taste
, touch ) to create immersive 
, vivid prose
6. Dialogue : Write natural , 
character - specific dialogue 
that reveals
personality and advances plot 
; use dialogue tags sparingly
7. Pacing : Vary sentence 
length and structure ; balance
action ,
description , dialogue , and 
introspection ; control 
narrative rhythm
8. Emotional Resonance : Evoke
appropriate emotions through 
character
reactions , sensory details , 
and narrative tension
9. Genre Awareness : Adapt 
style , tone , and conventions
to genre (
mystery , romance , horror , 
sci - fi , fantasy , etc .)
10. World - Building 
Integration : Seamlessly weave
world - building
details into narrative without
info - dumping
Creative Writing Quality 
Standards
- Narrative Coherence : Story 
flows logically ; plot points 
connect ; no
contradictions
- Character Development : 
Characters are believable , 
well - developed ,
and consistent
24


Page 25
- Prose Quality : Writing is 
clear , engaging , well - 
crafted with strong
imagery and voice
- Creativity : Story is 
original , imaginative , and 
compelling
- Pacing : Story maintains 
appropriate rhythm and 
momentum ; tension
builds effectively
- World - Building : Setting 
is well - established and 
internally
consistent ( if applicable )
- Emotional Engagement : 
Writing evokes appropriate 
emotions and reader
connection
- Faithfulness to Prompt : 
Story addresses the given 
writing prompt and
genre requirements
Creative Writing Techniques
- Opening Hooks : Start with 
action , dialogue , or 
intriguing detail to
engage reader immediately
- Scene Transitions : Use 
smooth transitions between 
scenes and
chapters ; maintain narrative 
flow
- Character Voice : Each 
character should have distinct
voice , speech
patterns , and mannerisms
- Subtext : Layer meaning 
beneath surface dialogue and 
action ; let
readers infer
- Foreshadowing : Plant subtle
clues and hints for later plot
developments
- Conflict : Every scene 
should contain conflict , 
tension , or stakes (
internal or external )
- Description : Use specific ,
concrete details rather than 
vague
abstractions
- Metaphor and Imagery : 
Employ figurative language to 
create vivid
mental pictures
- Pacing Variation : Alternate
fast - paced action with 
slower ,
reflective moments
- Chapter Endings : End 
chapters with hooks , 
cliffhangers , or emotional
beats to maintain reader 
interest
Technical / Business Writing 
Mode ( for documentation , 
reports , summaries
)
When writing non - fiction , 
technical , or business 
content :
Execution Guidelines ( 
Technical / Business Writing )
1. Audience analysis : 
Understand who will read this 
and what they need
2. Purpose clarity : Define 
what the document should 
accomplish
3. Structure first : Outline 
before writing ( hierarchy , 
sections , flow )
4. Clarity over cleverness : 
Simple , direct language ; 
avoid unnecessary
jargon
5. Active voice : " The system
processes requests " not " 
Requests are
processed by the system "
6. Concrete examples : Use 
specific examples , not 
abstract descriptions
7. Visual hierarchy : Use 
headings , bullets , tables , 
and formatting for
scanability
Technical / Business Quality 
Standards
- Clarity : Complex ideas 
explained simply ; no 
ambiguity
- Completeness : All necessary
information included ; no 
critical gaps
- Accuracy : Facts verified , 
claims supported , technical 
details
correct
- Organization : Logical flow 
, clear sections , easy 
navigation
- Conciseness : No unnecessary
words ; respect reader ’ s 
time
- Consistency : Terminology , 
style , and formatting uniform
throughout
Output Contract ( strict )
- ‘ output ‘ ( string ) : Well
- structured written content 
in appropriate
format ( creative prose or 
technical / business content )
- ‘ sources ‘ ( list [ str ]) 
: Reference materials , data 
sources ,
documentation , or creative 
inspirations consulted
25


Page 26
Context Integration ( Critical
for Creative Writing )
- Character Consistency : If 
writing a chapter in a multi -
chapter story
, maintain character 
descriptions , traits , and 
voice from previous
chapters
- Plot Continuity : Build on 
previous plot developments ; 
maintain
narrative coherence across 
chapters
- World - Building Consistency
: Adhere to established world 
rules ,
setting details , and genre 
conventions from foundation 
planning
- Tone and Style : Match the 
genre tone , narrative voice ,
and writing
style established in the story
structure
- Chapter Transitions : If 
writing a later chapter , 
reference events
and character states from 
earlier chapters naturally
Common WRITE Patterns
Creative Writing :
- Chapter Writing : Establish 
scene -> Introduce / develop 
characters ->
Advance plot -> Build tension 
-> End with hook
- Scene Writing : Set scene ->
Character action / dialogue ->
Conflict /
tension -> Resolution or 
escalation -> Transition
- Character Introduction : 
Show character through action 
-> Reveal
through dialogue -> Establish 
motivation -> Create 
connection
Technical / Business Writing :
- Technical documentation : 
Define scope -> Explain 
concepts -> Provide
examples -> Document edge 
cases -> Include 
troubleshooting
- Business report : Executive 
summary -> Background / 
context -> Analysis
-> Findings -> Recommendations
- User guide : Overview -> 
Prerequisites -> Step - by - 
step instructions
-> Screenshots / examples -> 
FAQs
- API documentation : Endpoint
description -> Parameters -> 
Request /
response examples -> Error 
codes
- Summary : Read source -> 
Extract key points -> Organize
logically ->
Write concisely -> Verify 
accuracy
Writing Best Practices
Creative Writing :
- Start in media res ( in the 
middle of action ) when 
possible
- Use specific , concrete 
nouns and verbs ; avoid weak 
modifiers
- Vary sentence structure for 
rhythm and emphasis
- Let characters reveal 
themselves through actions and
dialogue
- Build tension through 
conflict , obstacles , and 
stakes
- Use setting to reflect mood 
and character state
- End scenes and chapters with
forward momentum
Technical / Business Writing :
- Lead with most important 
information ( inverted pyramid
)
- One idea per paragraph
- Use transition words for 
flow ( however , therefore , 
additionally )
- Define acronyms on first use
- Include code examples for 
technical content
- Add tables for comparison or
reference data
- Use numbered lists for 
sequences , bullets for 
unordered items
- End with clear next steps or
conclusion
Format - Specific Guidelines
Creative Writing :
- Chapter : Clear chapter 
heading , scene breaks , 
consistent POV ,
narrative flow , chapter - 
ending hook
- Scene : Setting 
establishment , character 
action , dialogue , conflict ,
resolution or escalation
- Short Story : Complete 
narrative arc , character 
development ,
satisfying conclusion
Technical / Business Writing :
- README : Purpose , 
installation , quickstart , 
examples , contributing
26


Page 27
- API docs : Authentication , 
endpoints , parameters , 
responses , errors
- Changelog : Version , date ,
added / changed / fixed / 
deprecated / removed
- User guide : Task - oriented
, step - by - step , 
screenshots ,
troubleshooting
- Report : Executive summary ,
methodology , findings , 
recommendations
- Tutorial : Learning 
objectives , prerequisites , 
incremental steps ,
exercises
F GEPA+ configuration details
{
" gepa_plus ": {
" proposal_lms ": [
{
" model ": " openai / gpt -5" 
,
" temperature ": 1.0 ,
" max_tokens ": 16000 ,
" role ": " proposal "
} ,
{
" model ": " openrouter / 
anthropic / claude - sonnet 
-4.5" ,
" temperature ": 1.0 ,
" max_tokens ": 16000 ,
" role ": " proposal "
} ,
{
" model ": " openrouter / 
google / gemini -2.5 - flash "
,
" temperature ": 0.6 ,
" max_tokens ": 16000 ,
" role ": " proposal "
}
] ,
" judge_lm ": {
" model ": " openrouter / 
anthropic / claude - sonnet 
-4.5" ,
" temperature ": 1.0 ,
" max_tokens ": 16000
} ,
" merger_lm ": {
" model ": " openai / gpt -5" 
,
" temperature ": 1.0 ,
" max_tokens ": 16000
} ,
" top_n ": 2 ,
" verbose ": true
}
}
27


Page 28
Table 7: Performance of GEPA 
and GEPA+ across datasets 
(averaged over five runs). All
datasets use
GPT-4.1-mini as the base 
evaluation model, with 
PAPILLON additionally 
involving GPT-4.1-nano in
a privacy-preserving 
delegation setting where a 
small local model 
(GPT-4.1-nano) leverages a 
larger
untrusted model 
(GPT-4.1-mini), following the 
benchmark’s design.
Prompt optimizer AIME25 (%) 
HotpotQA (%) PAPILLON (%)
w/ GEPA 30.0 62.0 85.6
w/ GEPA+ 32.3 65.0 91.7
Table 8: Optimization 
efficiency comparison on AIME.
Method Metric calls Efficiency
(% / call) Relative efficiency
GEPA 560 0.0179 1.0×
GEPA+ 150 0.0313 1.75×
G Comparison of GEPA and GEPA+
We evaluate GEPA+ against 
standard GEPA on three 
representative benchmarks that
span distinct eval-
uation regimes: AIME25 
(mathematical reasoning),
4 
HotpotQA [ 53 ] (multi-hop 
question answering),
and PAPILLON [ 16] 
(safety-oriented evaluation). 
Across all experiments, we use
GPT-4.1-mini as
the base model for evaluation,
with PAPILLON additionally 
involving GPT-4.1-nano in its 
delegation
setting, following the 
benchmark’s design. Across all
benchmarks, GEPA+ consistently
improves
both final accuracy and 
optimization efficiency, 
demonstrating more effective 
prompt adaptation
under a fixed compute budget.
Performance: Table 7 
summarizes average accuracy 
over five runs. GEPA+ 
consistently outper-
forms GEPA across all three 
datasets. On AIME25, GEPA+ 
improves accuracy from 30.0% 
to 32.3%.
On HotpotQA, performance 
increases from 62.0% to 65.0%.
On PAPILLON, GEPA+ achieves
91.7% accuracy, compared to 
85.6% for GEPA. These gains 
demonstrate that GEPA+ 
delivers reliable
improvements across both 
reasoning-focused and 
safety-related tasks.
Efficiency: Beyond accuracy, 
GEPA+ substantially improves 
optimization efficiency. We 
analyze
convergence behavior on 
AIME25, where optimization 
cost is dominated by expensive
metric
evaluations (since each 
accuracy estimate requires 
re-running the model over many
reasoning-
intensive problems with full 
inference). As shown in Table 
8, standard GEPA requires 560 
metric
calls to converge, whereas 
GEPA+ converges using only 150
metric calls, a reduction of 
approximately
73%. When normalized by metric
calls, GEPA+ achieves 1.75× 
higher efficiency in terms of 
accuracy
improvement per call. This 
reduction directly translates 
into lower compute cost and 
faster iteration.
Overall, these results show 
that GEPA+ not only improves 
downstream accuracy, but also 
achieves
faster and more 
compute-efficient convergence.
This makes GEPA+ particularly 
well-suited for
optimizing multi-component 
agent systems, where 
evaluation costs are high and 
repeated optimization
cycles are required.
4
https://artofproblemsolving.co
m/wiki/index.php/2025_AIME_I
28
