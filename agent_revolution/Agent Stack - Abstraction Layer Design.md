# Agent Stack: Complete Abstraction Layer Design

**Purpose**: This document defines the complete abstraction layer structure for all four Agent Stack options, using insights from 50+ research papers to determine what layers are conceptually necessary for a complete agent architecture.

---

## **Methodology**

For each stack option, we:
1. **Analyze paper insights** to identify fundamental agent abstractions
2. **Design complete layer structures** based on this evidence
3. **Define layer responsibilities** and interfaces
4. **Ensure conceptual completeness** (no gaps, no redundancy)

---

# **OPTION A: 7-Layer Sequential Stack**

## **Complete Layer Structure**

Based on research evidence, Option A requires **9 layers** (not 7) for completeness:

```
┌─────────────────────────────────────────────────┐
│  Layer 9: HUMAN INTERFACE                       │
│  Human-agent interaction, feedback, control     │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 8: ORCHESTRATION                         │
│  Framework infrastructure, deployment           │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 7: VERIFICATION                          │
│  Correctness checking, benchmarking, metrics    │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 6: LEARNING                              │
│  RL, experience synthesis, self-evolution       │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 5: COORDINATION                          │
│  Multi-agent collaboration, role assignment     │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 4: ACTION                                │
│  Tool execution, environment interaction        │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 3: REASONING                             │
│  Planning, decomposition, decision-making       │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 2: MEMORY                                │
│  State persistence, context management          │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 1: PERCEPTION                            │
│  Multimodal sensing, state estimation           │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 0: FOUNDATION                            │
│  Pre-trained model with agentic capabilities    │
└─────────────────────────────────────────────────┘
```

---

## **Layer Abstractions (Option A)**

### **Layer 0: Foundation**

**Abstraction**: Pre-trained capabilities that enable agency

**What research shows**:
- CPT papers show foundation models need agentic pre-training, not just language modeling
- Tülu 3 demonstrates post-training (RLVR) shapes agentic behavior
- Agent0 shows self-evolution can bootstrap from minimal foundation

**Abstraction Interfaces**:
```
INPUT: Nothing (starting point)
OUTPUT: 
  - Base language understanding
  - Tool-use priors
  - Multi-step reasoning instincts
  - Trajectory completion capabilities
```

**Key Abstractions**:
- **Agentic Pre-training**: Training on agent trajectories, not just text
- **Post-training Alignment**: RLVR, RLER for behavioral shaping
- **Zero-shot Bootstrap**: Minimal requirements for agent emergence (Agent0)

---

### **Layer 1: Perception**

**Abstraction**: Transform external world into internal representations

**What research shows**:
- DeepEyesV2, MiMo-Embodied show perception is distinct from action
- World models (PAN) require separating "sensing" from "predicting"
- VLA models (π*_{0.6}) have explicit perception modules

**Abstraction Interfaces**:
```
INPUT: Raw sensory data (vision, audio, text, sensors)
OUTPUT:
  - Structured observations (parsed state)
  - Multimodal embeddings
  - Grounded entity representations
  - Spatial/temporal context
```

**Key Abstractions**:
- **Multimodal Fusion**: Combining vision, language, audio into unified representation
- **State Estimation**: Inferring hidden world state from partial observations
- **Grounding**: Mapping language to visual/spatial entities
- **Perceptual Attention**: Focusing on task-relevant observations

**Why it's a separate layer**:
- Perception failures ≠ Action failures (can perceive correctly but act wrong)
- Embodied agents need rich visual processing before reasoning
- Multimodal alignment is distinct capability

---

### **Layer 2: Memory**

**Abstraction**: Persist state and context across time

**What research shows**:
- O-Mem, MemGen papers show memory is fundamental capability, not add-on
- Million-step tasks require explicit memory management
- IterResearch demonstrates memory enables long-horizon coherence

**Abstraction Interfaces**:
```
INPUT: 
  - Current observations (from Perception)
  - Past experiences (from Memory itself)
  - Reasoning outputs (from above)
OUTPUT:
  - Retrieved context (relevant past)
  - Updated memory state
  - Working memory buffer
  - Memory-augmented observations
```

**Key Abstractions**:
- **Episodic Memory**: What happened (events, experiences)
- **Semantic Memory**: What's known (facts, procedures, world model)
- **Working Memory**: What's relevant now (task context, intermediate state)
- **Memory Retrieval**: Attention over stored experiences
- **Memory Consolidation**: Updating long-term knowledge from working memory

**Why it's a separate layer**:
- Memory management is orthogonal to reasoning (reasoning uses memory but doesn't manage it)
- Long-horizon tasks fail without persistent state
- Memory has own optimization (retrieval accuracy, consolidation strategy)

---

### **Layer 3: Reasoning**

**Abstraction**: Transform observations and goals into plans

**What research shows**:
- ReAct establishes thought-action as fundamental pattern
- Million-step paper shows reasoning scales to extreme lengths
- Aristotle demonstrates formal reasoning requires different abstractions than informal
- Tree Search papers show reasoning as exploration of decision trees

**Abstraction Interfaces**:
```
INPUT:
  - Current observations (from Memory-augmented Perception)
  - Current goal/task
  - Available actions (from Action layer)
OUTPUT:
  - Action plan (sequence of steps)
  - Reasoning trace (interpretable chain-of-thought)
  - Confidence estimates
  - Alternative plans (for robustness)
```

**Key Abstractions**:
- **Goal Decomposition**: Breaking complex goals into subgoals
- **Planning Algorithms**: Search, MCTS, hierarchical planning
- **Reasoning Strategies**: CoT, latent reasoning, formal verification
- **Plan Verification**: Checking plan correctness before execution
- **Adaptive Planning**: Replanning when world state changes

**Sub-layers** (reasoning complexity tiers):
```
Layer 3.3: Formal Reasoning (Aristotle, P1)
           - Theorem proving, verification
Layer 3.2: Long-Horizon Reasoning (Million-step, WebResearcher)
           - Extended planning, state tracking
Layer 3.1: Basic Reasoning (ReAct, CoCoNuT)
           - Single-step planning, simple decomposition
```

---

### **Layer 4: Action**

**Abstraction**: Execute plans in external environment

**What research shows**:
- SWE-agent shows action interfaces (ACIs) dramatically affect performance
- World models demonstrate action requires understanding consequences
- AIDE shows action includes code generation and execution
- ToolOrchestra shows action selection is multi-objective

**Abstraction Interfaces**:
```
INPUT:
  - Action plan (from Reasoning)
  - Environment state (from Perception)
  - Available tools/APIs
OUTPUT:
  - Action execution results
  - Observations of action effects
  - Success/failure signals
  - Updated environment state
```

**Key Abstractions**:
- **Tool Selection**: Choosing appropriate tools for task
- **Action Execution**: Invoking tools with correct parameters
- **Sandboxing**: Safe execution (SWE-agent, OpenHands)
- **Action Outcome Observation**: Detecting success/failure
- **Error Recovery**: Handling action failures gracefully

**Action Types** (different execution modalities):
- **API Calls**: Deterministic tool invocations
- **Code Execution**: Generating and running code (AIDE, OpenHands)
- **Physical Actions**: Robot control (π*_{0.6}, MiMo)
- **UI Interactions**: Browser/GUI control (WebSailor, Computer Use)

---

### **Layer 5: Coordination**

**Abstraction**: Synchronize multiple agents toward shared goals

**What research shows**:
- AutoGen establishes multi-agent conversation patterns
- LatentMAS shows coordination can be latent (not just text)
- ToolOrchestra demonstrates coordination is learnable via multi-objective RL
- M-GRPO shows multi-agent systems can be trained end-to-end

**Abstraction Interfaces**:
```
INPUT:
  - Individual agent states
  - Shared task/goal
  - Communication medium (text or latent)
OUTPUT:
  - Task allocation (who does what)
  - Agent synchronization (coordination protocol)
  - Shared state updates
  - Collaborative action plan
```

**Key Abstractions**:
- **Role Assignment**: Assigning agents to specialized roles
- **Communication Protocol**: Text vs. latent (LatentMAS)
- **Task Decomposition**: Breaking shared task across agents
- **Conflict Resolution**: Handling competing agent objectives
- **Learned Coordination**: RL-based coordination policies (ToolOrchestra)

**Coordination Patterns**:
- **Centralized**: Single orchestrator assigns tasks
- **Decentralized**: Agents self-organize (emergent coordination)
- **Hierarchical**: Meta-agents coordinate specialist agents
- **Latent**: Direct hidden state transfer (LatentMAS)

**Why separate from Orchestration**:
- Coordination = agent-to-agent interaction (runtime)
- Orchestration = developer infrastructure (deployment)
- ToolOrchestra shows both exist: learned coordination (Layer 5) deployed via orchestration framework (Layer 8)

---

### **Layer 6: Learning**

**Abstraction**: Improve agent capabilities from experience

**What research shows**:
- Agentic RL Survey shows learning is distinct from initial training
- DR Tulu shows learning continues post-deployment (RLER)
- Agent-R1 demonstrates end-to-end RL for agents
- Experience Synthesis shows learning can be from synthetic data

**Abstraction Interfaces**:
```
INPUT:
  - Agent trajectories (observation-action sequences)
  - Rewards/outcomes
  - Current policy/model
OUTPUT:
  - Updated policy
  - Improved capabilities
  - Learning metrics (convergence, sample efficiency)
  - Adapted model parameters
```

**Key Abstractions**:
- **Reward Specification**: Defining what to optimize (ToolRM)
- **Policy Optimization**: RL algorithms (GRPO, M-GRPO, RLVR, RLER)
- **Experience Synthesis**: Generating training data (avoid costly rollouts)
- **Online Learning**: Real-time adaptation during deployment
- **Curriculum Learning**: Progressive difficulty increase
- **Multi-Objective Learning**: Optimizing accuracy + cost + latency (ToolOrchestra)

**Learning Modalities**:
- **Pre-deployment RL**: Training before deployment (DR Tulu)
- **Online RL**: Learning during deployment (Real-Time Reasoning)
- **Self-Evolution**: Autonomous improvement (Agent0, MemGen)

---

### **Layer 7: Verification**

**Abstraction**: Validate agent correctness and performance

**What research shows**:
- MLE-bench, MLGym papers show evaluation is distinct capability
- Aristotle demonstrates formal verification (Lean prover)
- ToolRM shows outcome verification via reward models
- In-the-Flow shows runtime verification

**Abstraction Interfaces**:
```
INPUT:
  - Agent actions/outputs
  - Ground truth (when available)
  - Correctness criteria
OUTPUT:
  - Correctness scores
  - Error detection
  - Performance metrics
  - Failure diagnostics
```

**Key Abstractions**:
- **Formal Verification**: Proof checking (Aristotle/Lean)
- **Outcome Verification**: Did action achieve goal? (ToolRM)
- **Benchmark Evaluation**: Standardized testing (MLE-bench, MLGym)
- **Runtime Monitoring**: Live correctness checking (Real-Time Reasoning)
- **Self-Assessment**: Agent confidence estimation

**Verification Types**:
- **Static**: Pre-deployment testing (benchmarks)
- **Dynamic**: Runtime checking (monitors)
- **Formal**: Mathematical proofs (theorem proving)
- **Empirical**: Outcome-based evaluation

**Why it's a separate layer**:
- Verification is orthogonal to execution (checks all other layers)
- Distinct expertise (verification algorithms ≠ agent algorithms)
- Critical for production deployment

---

### **Layer 8: Orchestration**

**Abstraction**: Developer-facing infrastructure and deployment

**What research shows**:
- ToolOrchestra provides research foundation (learned orchestration)
- LangGraph, CrewAI show different orchestration patterns
- MLE-Dojo shows orchestration includes environment management

**Abstraction Interfaces**:
```
INPUT:
  - Agent definitions (code/configs)
  - Deployment requirements (compute, latency, cost)
  - Infrastructure constraints
OUTPUT:
  - Running agent system
  - Observability dashboards
  - Resource allocation
  - Deployment pipelines
```

**Key Abstractions**:
- **Framework Patterns**: Sequential, hierarchical, graph-based (LangGraph)
- **Resource Management**: Compute, memory, cost budgets
- **Observability**: Logging, tracing, debugging
- **Deployment**: Containerization, scaling, load balancing
- **Learned Orchestration**: Multi-objective optimization (ToolOrchestra)

**Orchestration Concerns**:
- **Development**: Building agents (frameworks, SDKs)
- **Deployment**: Running agents (containers, cloud)
- **Monitoring**: Observing agents (logs, metrics)
- **Optimization**: Improving systems (cost, latency)

---

### **Layer 9: Human Interface**

**Abstraction**: Human-agent interaction and control

**What research shows**:
- OmniScientist shows human-AI co-evolution
- Computer Use agents (Claude, Operator) require human permission mechanisms
- SWE-agent, OpenHands have human-in-the-loop patterns

**Abstraction Interfaces**:
```
INPUT:
  - Human instructions/feedback
  - Interruption signals
  - Delegation boundaries
OUTPUT:
  - Agent responses
  - Transparency (explanations)
  - Permission requests
  - Handoff to human when needed
```

**Key Abstractions**:
- **Instruction**: Human → Agent task specification
- **Feedback**: Human evaluation of agent performance
- **Interruption**: Human override/correction
- **Transparency**: Agent explanation generation
- **Delegation**: When to ask human vs. proceed autonomously
- **Trust Calibration**: Building human confidence in agent

**Why it's a separate layer**:
- Human interaction is orthogonal to agent-environment interaction
- Distinct UX concerns (transparency, trust, control)
- Critical for production agents (can't deploy without human interface)

---

## **Option A: Complete Information Flow**

```
External World
      ↓
[0. FOUNDATION] - Provides base capabilities
      ↓
[1. PERCEPTION] - Senses → observations
      ↓
[2. MEMORY] - Stores → context
      ↓
[3. REASONING] - Plans → actions
      ↓
[4. ACTION] - Executes → outcomes
      ↓
[5. COORDINATION] - Synchronizes agents → shared outcomes
      ↓
[6. LEARNING] - Improves from outcomes → updated models
      ↓
[7. VERIFICATION] - Validates → correctness signals
      ↓
[8. ORCHESTRATION] - Deploys → running systems
      ↓
[9. HUMAN INTERFACE] - Communicates → human oversight
      ↓
Back to External World (via ACTION)

Feedback loops:
- Learning → Foundation (update base model)
- Verification → Reasoning (correct plans)
- Human → all layers (feedback)
- Memory → Reasoning (context)
```

---

## **Option A: Assessment**

**Completeness**: ✅ All necessary abstractions present (9 layers)

**Problems**:
1. **9 layers is excessive** - hard to remember, hard to communicate
2. **Sequential assumption too strong** - layers interact in complex ways, not just bottom-up
3. **Mixed abstraction levels persist** - despite 9 layers, still mixing capabilities, training, infrastructure
4. **Redundancy**: Coordination overlaps with Orchestration (both "coordinate" things)

**Verdict**: Option A becomes **Option B+** when completed - too many layers for practicality

---

# **OPTION B: 8-Layer Sequential Stack (As-Is)**

Option B already identified the right 8 layers, but let me refine the abstractions:

```
8. Orchestration
7. Learning
6. Coordination
5. Environment → Should be renamed "ACTION"
4. Reasoning
3. Memory
2. Perception
1. Foundation

Plus implicit: Verification (scattered), Human Interface (scattered)
```

## **Refinement for Option B**

Option B is actually **10 layers when complete**:

Same as Option A (9 layers) PLUS needs to explicitly add **Layer 7.5: Verification** between Learning and Orchestration.

**Why**: Verification validates that Learning actually improved things.

**Assessment**: Option B suffers from same problem as Option A - too many layers (10) when completed.

---

# **OPTION C: Capability-Based (Refined)**

## **Complete Structure**

```
┌────────────────── SUPPORT LAYERS ──────────────────┐
│  (Meta-capabilities: how agents improve/deploy)    │
├─────────────────────────────────────────────────────┤
│  • Orchestration                                    │
│    - Framework patterns, deployment infrastructure  │
│                                                     │
│  • Learning                                         │
│    - RL, experience synthesis, self-evolution       │
│                                                     │
│  • Verification                                     │
│    - Benchmarks, formal proofs, runtime checks      │
│                                                     │
│  • Human Interface ← ADDED                          │
│    - Feedback, interruption, delegation, trust      │
└─────────────────────────────────────────────────────┘
                          ↕
┌────────────────── CORE LAYERS ─────────────────────┐
│  (Primary capabilities: what agents do)             │
├─────────────────────────────────────────────────────┤
│  • Perception                                       │
│    - Multimodal sensing, state estimation           │
│                                                     │
│  • Memory                                           │
│    - Episodic, semantic, working memory             │
│                                                     │
│  • Reasoning                                        │
│    - Planning, decomposition, long-horizon          │
│                                                     │
│  • Action                                           │
│    - Tool execution, environment interaction        │
│                                                     │
│  • Coordination                                     │
│    - Multi-agent collaboration, learned policies    │
└─────────────────────────────────────────────────────┘
                          ↕
┌────────────────── FOUNDATION ──────────────────────┐
│  (Base capabilities)                                │
├─────────────────────────────────────────────────────┤
│  • Pre-trained Model                                │
│    - Language understanding, tool priors, reasoning │
└─────────────────────────────────────────────────────┘
```

---

## **Abstraction Design (Option C)**

### **FOUNDATION**

**Abstraction**: The pre-trained capabilities all other layers build on

**What it provides**:
- Language understanding (tokenization, embeddings, generation)
- Tool-use priors (knows what tools are)
- Multi-step reasoning instincts (can decompose tasks)
- World knowledge (facts, procedures, common sense)

**Training Abstractions**:
- **Agentic CPT**: Pre-training on agent trajectories
- **RLVR/RLER**: Post-training for behavioral shaping
- **Zero-shot Bootstrap**: Minimal viable foundation (Agent0)

**Interface to Core**:
```
Foundation provides:
  → Perception: Vision/language encoders
  → Memory: Embedding models for retrieval
  → Reasoning: LLM for planning
  → Action: LLM for tool invocation
  → Coordination: Communication capabilities
```

---

### **CORE → Perception**

**Abstraction**: Transform external stimuli into structured internal representations

**Sub-Abstractions**:

**1. Multimodal Encoding**
- Vision → visual embeddings
- Audio → acoustic features
- Text → language embeddings
- Sensors → structured state

**2. Cross-Modal Alignment** (DeepEyesV2, MiMo)
- Align vision ↔ language
- Ground language in visual world
- Fuse modalities into unified representation

**3. State Estimation** (World Models, PAN)
- Infer hidden world state from partial observations
- Predict unobserved but relevant state
- Maintain belief over possible states (POMDP)

**4. Perceptual Attention**
- Focus on task-relevant observations
- Filter noise and irrelevant stimuli
- Saliency detection

**Interface**:
```
INPUT: Raw sensory data
OUTPUT: Structured observations (for Memory, Reasoning)
```

---

### **CORE → Memory**

**Abstraction**: Persist and retrieve information across time

**Sub-Abstractions**:

**1. Episodic Memory** (O-Mem, MemGen)
- Store: What happened (events, trajectories)
- Retrieve: Similar past experiences
- Update: Consolidate new experiences

**2. Semantic Memory**
- Store: What's known (facts, procedures, world model)
- Retrieve: Relevant knowledge for current context
- Update: Incorporate new knowledge

**3. Working Memory**
- Store: Current task context (what's relevant now)
- Maintain: Task state across reasoning steps
- Clear: Reset when task changes

**4. Memory Management** (General Agentic Memory)
- Consolidation: Working → Long-term
- Forgetting: Prune irrelevant memories
- Retrieval strategies: Semantic similarity, temporal proximity, importance weighting

**Interface**:
```
INPUT: Observations (from Perception), Reasoning outputs
OUTPUT: Context-augmented observations (to Reasoning)
```

---

### **CORE → Reasoning**

**Abstraction**: Transform observations + goals into executable plans

**Sub-Abstractions**:

**1. Goal Decomposition**
- Break complex goals → subgoals
- Hierarchical task planning
- Dependency analysis

**2. Planning Strategies** (categorized by complexity)

**Basic Planning** (ReAct):
- Single-step: observation → thought → action
- No long-horizon consideration

**Tree-Based Planning** (Tree Search RL):
- MCTS: Monte Carlo Tree Search
- Explore action space via simulation
- Backpropagate value estimates

**Long-Horizon Planning** (Million-Step, WebResearcher):
- Markovian state reconstruction (IterResearch)
- Summarization for context compression (ReSum)
- Dynamic outline generation (WebWeaver)

**Formal Planning** (Aristotle, P1):
- Theorem proving (Lean)
- Physics-based reasoning
- Verified plan correctness

**3. Reasoning Modalities**

**Discrete Reasoning**:
- Chain-of-Thought (explicit text)
- Interpretable but token-heavy

**Continuous Reasoning** (CoCoNuT):
- Latent reasoning (hidden states)
- Efficient but opaque

**4. Plan Verification**
- Pre-execution: Check plan validity
- Runtime: Monitor execution
- Post-execution: Evaluate outcomes

**Interface**:
```
INPUT: Context (from Memory), Available actions (from Action)
OUTPUT: Action plan, Reasoning trace
```

---

### **CORE → Action**

**Abstraction**: Execute plans in external environment

**Sub-Abstractions**:

**1. Tool Selection** (ToolOrchestra)
- Multi-objective: accuracy + cost + latency + preferences
- Learned selection policies (RL)
- Fallback strategies when primary tool fails

**2. Action Execution Modes**

**API Invocation**:
- Deterministic tool calls
- Parameter binding
- Result parsing

**Code Generation + Execution** (AIDE, SWE-agent, OpenHands):
- Generate code for complex actions
- Execute in sandbox
- Parse execution results

**Physical Control** (π*_{0.6}, MiMo):
- Robot motor commands
- Real-time feedback control
- Safety constraints

**UI Interaction** (WebSailor, Computer Use):
- Browser navigation
- Form filling
- Button clicking

**3. Agent-Computer Interfaces (ACIs)** (SWE-agent)
- Specialized commands for agents (not raw bash)
- `search_file` instead of `grep`
- `edit_function` instead of `vim`
- Dramatically improves performance (8-10% on SWE-bench)

**4. Sandboxing & Safety**
- Isolated execution (Docker, VMs)
- Resource limits (CPU, memory, time)
- Rollback capabilities

**Interface**:
```
INPUT: Action plan (from Reasoning)
OUTPUT: Execution results (to Memory, Reasoning)
```

---

### **CORE → Coordination**

**Abstraction**: Synchronize multiple agents toward shared goals

**Sub-Abstractions**:

**1. Communication Protocols**

**Text-Based** (AutoGen):
- Natural language messages
- Interpretable but slow/verbose
- 100% token overhead

**Latent-Based** (LatentMAS):
- Direct hidden state transfer
- 70-84% token reduction
- 4-7× speedup
- Opaque but efficient

**2. Coordination Patterns**

**Centralized** (ToolOrchestra):
- Single orchestrator (8B model)
- Delegates to specialists (GPT-5, Claude, math models)
- Learned via multi-objective RL
- Meta-agent architecture

**Decentralized**:
- Agents self-organize
- Emergent coordination
- No single point of failure

**Hierarchical** (OmniScientist):
- Meta-agents → specialist agents → worker agents
- Task decomposition at each level
- Human at top of hierarchy

**3. Role Assignment**
- Identify required capabilities
- Match agents to roles
- Load balancing across agents

**4. Learned Coordination** (M-GRPO, ToolOrchestra)
- Multi-agent RL (M-GRPO)
- Optimize collective performance
- Not just individual agent performance

**Interface**:
```
INPUT: Individual agent states, Shared task
OUTPUT: Task allocation, Coordination protocol
```

---

### **SUPPORT → Learning**

**Abstraction**: Improve capabilities from experience

**Sub-Abstractions**:

**1. Training Paradigms**

**Pre-Deployment RL**:
- RLVR (Tülu 3): RL with Verifiable Rewards
- RLER (DR Tulu): RL with Evolving Rubrics
- GRPO: Group Relative Policy Optimization
- M-GRPO: Multi-Agent GRPO

**Online Learning** (Real-Time Reasoning):
- During deployment
- Adapt to distribution shift
- Continuous improvement

**Self-Evolution** (Agent0, MemGen):
- No human data required
- Bootstrap from minimal foundation
- Autonomous capability discovery

**2. Experience Sources**

**Real Rollouts**:
- Expensive but high-quality
- Ground truth rewards

**Synthetic Experience** (Experience Synthesis):
- Simulated environments (World Models, PAN)
- Reasoning model-generated scenarios
- Cheaper but potentially biased

**3. Multi-Objective Optimization** (ToolOrchestra)
- Accuracy (primary objective)
- Cost (API pricing)
- Latency (response time)
- User preferences (privacy, local vs. cloud)

**4. Curriculum Learning**
- Start simple → progressively harder
- Prevents catastrophic failure in early training
- Enables learning complex skills

**Interface**:
```
INPUT: Agent trajectories, Rewards/outcomes
OUTPUT: Updated Foundation, Updated Core policies
```

---

### **SUPPORT → Verification**

**Abstraction**: Validate correctness and performance

**Sub-Abstractions**:

**1. Formal Verification** (Aristotle)
- Theorem proving (Lean, Coq)
- Mathematical correctness proofs
- Zero tolerance for errors

**2. Empirical Evaluation** (MLE-bench, MLGym, MLAgentBench)
- Benchmarks (standardized tasks)
- Success rate, accuracy metrics
- Compare across systems

**3. Outcome Verification** (ToolRM)
- Reward models judge outcomes
- Did action achieve goal?
- Confidence estimation

**4. Runtime Monitoring** (Real-Time Reasoning, In-the-Flow)
- Live correctness checks
- Detect failures during execution
- Trigger recovery mechanisms

**5. Self-Assessment**
- Agent estimates own confidence
- Knows when to ask for help (Human Interface)
- Calibrated uncertainty

**Interface**:
```
INPUT: Agent actions/outputs, Correctness criteria
OUTPUT: Verification results (pass/fail, scores, diagnostics)
FEEDBACK TO: All Core layers, Learning
```

---

### **SUPPORT → Orchestration**

**Abstraction**: Developer infrastructure for building and deploying agents

**Sub-Abstractions**:

**1. Framework Patterns** (LangGraph, CrewAI, DSPy)

**Sequential** (CrewAI):
- Linear task flow
- Agent 1 → Agent 2 → Agent 3
- Simple to understand/debug

**Graph-Based** (LangGraph):
- Cycles, conditionals, branches
- Complex workflows
- Maximum flexibility

**Optimization-Based** (DSPy):
- "Programming not prompting"
- Automatically optimize prompts
- Compile-time optimization

**2. Deployment Infrastructure**
- Containerization (Docker, Kubernetes)
- Scaling (horizontal, vertical)
- Load balancing
- Cost management

**3. Observability** (LangSmith, custom)
- Logging (all actions, observations)
- Tracing (track execution flow)
- Metrics (latency, success rate, cost)
- Debugging (inspect intermediate states)

**4. Learned Orchestration** (ToolOrchestra)
- Multi-objective RL for orchestration policies
- Small orchestrator (8B) → large models (GPT-5)
- Optimize accuracy + cost + latency + preferences

**Interface**:
```
INPUT: Agent definitions, Deployment requirements
OUTPUT: Running agent systems, Dashboards, Pipelines
```

---

### **SUPPORT → Human Interface**

**Abstraction**: Human-agent interaction and control

**Sub-Abstractions**:

**1. Instruction**
- Natural language task specification
- Clarification dialogue
- Ambiguity resolution

**2. Feedback**
- Evaluation of agent performance (thumbs up/down)
- Corrections (show how it should be done)
- Preference learning (RLHF patterns)

**3. Interruption & Control**
- Pause: Stop execution
- Override: Take control
- Terminate: Abort task
- Permission requests (Claude Computer Use, Operator)

**4. Transparency & Explanation**
- Reasoning traces (why it chose action)
- Confidence communication (how sure it is)
- Failure explanations (why it failed)

**5. Delegation Boundaries** (OmniScientist)
- When to proceed autonomously
- When to ask human
- Adaptive autonomy (learn over time)

**6. Trust Calibration**
- Build human confidence in agent
- Appropriate reliance (neither over-trust nor under-trust)
- Transparent capabilities and limitations

**Interface**:
```
INPUT: Human instructions, feedback, interruptions
OUTPUT: Agent responses, explanations, permission requests
AFFECTS: All Core layers (human feedback influences behavior)
```

---

## **Option C: Information Flow**

```
FOUNDATION
    ↕ (provides base capabilities to all)
    
CORE (runtime execution):
┌─────────────────────────────────────┐
│ Perception → Memory → Reasoning     │
│      ↓          ↑         ↓         │
│   Action ←──────┴─────────┘         │
│      ↓                              │
│ Coordination (multi-agent)          │
└─────────────────────────────────────┘
    ↕ (bidirectional with Support)

SUPPORT (meta-layer):
┌─────────────────────────────────────┐
│ Learning ← observes Core trajectories│
│    ↓ (improves Foundation + Core)   │
│                                     │
│ Verification ← validates Core       │
│    ↓ (feeds back to Core + Learning)│
│                                     │
│ Orchestration ← deploys Core        │
│    ↓ (manages infrastructure)       │
│                                     │
│ Human Interface ← monitors/controls │
│    ↓ (feedback to all layers)       │
└─────────────────────────────────────┘
```

**Key Interactions**:
- **Learning uses Core**: Observes trajectories to learn from
- **Learning improves Foundation + Core**: Updates models and policies
- **Verification validates Core**: Checks correctness
- **Verification feeds Learning**: Evaluation metrics guide improvement
- **Orchestration deploys Core**: Provides infrastructure
- **Human Interface observes/controls all**: Oversight and feedback

---

## **Option C: Why This is Most Complete**

**Completeness**:
✅ All abstractions present:
- Foundation (1)
- Core capabilities (5): Perception, Memory, Reasoning, Action, Coordination
- Support mechanisms (4): Learning, Verification, Orchestration, Human Interface

**Total**: 10 concepts, but **grouped into 3 categories** for clarity

**No Redundancy**:
- Coordination (Core) ≠ Orchestration (Support)
  - Coordination = runtime agent-to-agent collaboration
  - Orchestration = developer infrastructure
- Clear separation validated by ToolOrchestra: coordination is learned (Support Learning) and deployed (Support Orchestration)

**Clean Abstractions**:
- Foundation = what you start with (training)
- Core = what agents do (runtime capabilities)
- Support = how they improve/deploy (meta-capabilities)
- No mixing of abstraction levels

**Diagnostic Clarity**:
When agent fails:
1. **Foundation problem?** → Model too weak (need better pre-training)
2. **Core problem?** → Which capability? (perception/memory/reasoning/action/coordination)
3. **Support problem?** → Which mechanism? (learning/verification/orchestration/human interface)

Two-level diagnosis: Group → Specific capability

---

# **OPTION D: Process-Oriented (Refined)**

While Options A/B/C focus on **structural layers**, Option D takes a **temporal/process view**.

## **Complete Process Structure**

```
┌──────────────────────────────────────────────────┐
│              TEMPORAL PROCESS LOOP               │
└──────────────────────────────────────────────────┘

      INPUT (Task, Environment State)
              ↓
      ┌──────────────┐
      │  1. PERCEIVE │ ← Foundation powers this
      └──────┬───────┘
             ↓
      ┌──────────────┐
      │  2. REMEMBER │ ← Retrieves from Memory
      └──────┬───────┘
             ↓
      ┌──────────────┐
      │  3. REASON   │ ← Plans using context
      └──────┬───────┘
             ↓
      ┌──────────────┐
      │  4. ACT      │ ← Executes in environment
      └──────┬───────┘
             ↓
      ┌──────────────┐
      │  5. EVALUATE │ ← Assesses outcome
      └──────┬───────┘
             ↓
      ┌──────────────┐
      │  6. LEARN    │ ← Updates from experience
      └──────┬───────┘
             ↓
      OUTPUT (Result) OR LOOP BACK (if task continues)
             ↓
      ┌──────────────┐
      │  FEEDBACK    │ → Loops back to PERCEIVE
      └──────────────┘

┌──────────────────────────────────────────────────┐
│           CROSS-PROCESS ABSTRACTIONS             │
│  (Operate across temporal loop, not in it)       │
└──────────────────────────────────────────────────┘

• FOUNDATION
  - Powers all process steps with base model

• COORDINATION
  - Synchronizes multiple agent process loops
  - Enables parallel execution across agents

• ORCHESTRATION
  - Manages infrastructure for process execution
  - Deploys, monitors, scales

• HUMAN INTERFACE
  - Interrupts process at any step
  - ProvidesThis feedback to all steps
```

---

## **Process Step Abstractions (Option D)**

### **Step 1: Perceive**

**Abstraction**: Sensing current environment state

**What happens**:
- Multimodal input processing (vision, audio, text)
- State estimation (infer hidden state from observations)
- Attentional focusing (filter relevant from irrelevant)
- Grounding (map language to world entities)

**Outputs to**: Remember step

---

### **Step 2: Remember**

**Abstraction**: Contextualizing current observations with past

**What happens**:
- Episodic retrieval (similar past situations)
- Semantic retrieval (relevant knowledge)
- Working memory update (maintain task context)
- Context assembly (combine observations + memories)

**Outputs to**: Reason step

---

### **Step 3: Reason**

**Abstraction**: Planning next actions given context

**What happens**:
- Goal decomposition (break task into steps)
- Plan generation (sequence of actions)
- Plan verification (check validity)
- Strategy selection (choose reasoning approach)

**Outputs to**: Act step

---

### **Step 4: Act**

**Abstraction**: Executing planned actions

**What happens**:
- Tool selection (which tool to use)
- Parameter binding (fill in tool arguments)
- Execution (invoke tool in sandboxed environment)
- Outcome observation (what happened)

**Outputs to**: Evaluate step

---

### **Step 5: Evaluate**

**Abstraction**: Assessing action outcomes

**What happens**:
- Success detection (did we achieve goal?)
- Error diagnosis (if failed, why?)
- Confidence estimation (how sure are we?)
- Verification (formal or empirical correctness check)

**Outputs to**: Learn step OR loops back to Perceive (if continuing)

---

### **Step 6: Learn**

**Abstraction**: Updating from experience

**What happens**:
- Trajectory storage (save for future learning)
- Online policy update (if doing online RL)
- Memory consolidation (working → long-term memory)
- Strategy adaptation (adjust future behavior)

**Outputs to**: Feedback → Loop or Terminate

---

## **Cross-Process Abstractions (Option D)**

### **Foundation**

**Role**: Powers all process steps with pre-trained model

**How it appears**:
- Perceive: Vision encoders, language encoders
- Remember: Embedding models for retrieval
- Reason: LLM for planning
- Act: LLM for tool invocation, code generation
- Evaluate: Reward models for outcome assessment
- Learn: Policy optimization updates Foundation itself

**Not inside the loop**: Foundation is the substrate the loop runs on

---

### **Coordination**

**Role**: Synchronizes multiple concurrent process loops

**How it works**:
- Multiple agents each run Perceive → Remember → Reason → Act loops
- Coordination synchronizes them:
  - **At Perceive**: Shared observations
  - **At Reason**: Distributed planning
  - **At Act**: Coordinated actions
  - **At Learn**: Collective improvement

**Example** (LatentMAS):
```
Agent 1: Perceive → Remember → Reason → ACT
                                         ↓
                                  (latent transfer)
                                         ↓
Agent 2: Perceive → Remember → Reason ← (receives Agent 1 hidden states)
                                  ↓
                                 ACT
```

**Not inside the loop**: Coordination is orthogonal, connects loops

---

### **Orchestration**

**Role**: Infrastructure that deploys and manages process loops

**How it works**:
- **Deploys** process loops (containers, cloud)
- **Monitors** loop execution (logs, metrics)
- **Scales** loops (replicate across instances)
- **Optimizes** resource allocation (compute, memory)

**Not inside the loop**: Orchestration is the platform the loop runs on

---

### **Human Interface**

**Role**: Human interaction with process loop

**How it works**:
- **Interrupt** at any step (pause, override, terminate)
- **Observe** process state (see what agent is doing)
- **Provide feedback** (corrections, preferences)
- **Request explanations** (why did you do that?)

**Example**:
```
User: "Book flight to Tokyo"
      ↓
(Agent loop starts: Perceive → Remember → Reason → Act)
      ↓
Agent: "I found a flight for $875. Book it?"
      ↓ (PAUSE - requests permission)
Human: "Yes" OR "No, find cheaper"
      ↓
(Loop continues or backtracks to Reason)
```

**Not inside the loop**: Human Interface wraps the loop with control mechanisms

---

## **Option D: Temporal Dynamics**

**Single Iteration**:
```
t=0: Perceive → Remember → Reason → Act → Evaluate → Learn
     (1 second for simple action)
```

**Long-Horizon Task** (Million-Step paper):
```
t=0 to t=1,000,000:
  Each iteration: Perceive → ... → Learn
  Memory accumulates across iterations
  Reasoning becomes more sophisticated
  Learning continuously improves
```

**Multi-Agent** (LatentMAS):
```
Agent 1: Perceive → Remember → Reason → Act (t=0)
            ↓ (latent transfer at t=0.5)
Agent 2: Perceive → Remember → Reason ← (receives hidden state) → Act (t=1)
```

---

## **Option D: Strengths & Weaknesses**

### **✅ Strengths**:
1. **Intuitive**: Matches how humans think about cognition
2. **Temporal clarity**: Shows agent operation over time
3. **Explains behavior**: Easier to trace "what agent did" than "which layer failed"
4. **Natural fit for interactive agents**: Chatbots, assistants
5. **Feedback loop explicit**: Shows iteration naturally
6. **RL fits perfectly**: Learn step is explicit
7. **All abstractions present**: 6 steps + 4 cross-process = 10 total (same as Option C)

### **❌ Weaknesses**:
1. **False sequential assumption**: Real agents don't strictly Perceive → Remember → Reason → Act
   - Reasoning can trigger new perception (look at X)
   - Acting updates memory in real-time
   - Evaluation happens during action, not just after
2. **Parallel processes obscured**: Agents often do multiple steps simultaneously
3. **Diagnostic imprecision**: "At which step did it fail?" is less precise than "which capability failed?"
4. **Doesn't fit batch/offline agents**: Process view assumes online, interactive operation
5. **Cross-process abstraction placement awkward**: Foundation isn't "cross-process," it's foundational

### **When to Use Option D**:
- Explaining agents to non-technical audiences (most intuitive)
- Building interactive agents (chatbots, assistants)
- Temporal behavior is critical (real-time, streaming)
- Want process view over structural view
- Education and communication

---

# **FINAL COMPARISON: Abstraction Completeness**

## **All Four Options (Fully Enriched)**

| Abstraction | Option A | Option B | Option C | Option D |
|-------------|----------|----------|----------|----------|
| **Foundation** | Layer 0 | Layer 1 | Foundation | Cross-Process |
| **Perception** | Layer 1 | Layer 2 | Core | Step 1 |
| **Memory** | Layer 2 | Layer 3 | Core | Step 2 |
| **Reasoning** | Layer 3 | Layer 4 | Core | Step 3 |
| **Action** | Layer 4 | Layer 5 | Core | Step 4 |
| **Evaluation** | ❌ (in Verify) | ❌ (in Verify) | ❌ (in Verify) | **Step 5 ✅** |
| **Coordination** | Layer 5 | Layer 6 | Core | Cross-Process |
| **Learning** | Layer 6 | Layer 7 | Support | Step 6 |
| **Verification** | Layer 7 | ❌ (scattered) | **Support ✅** | Cross-Process |
| **Orchestration** | Layer 8 | Layer 8 | Support | Cross-Process |
| **Human Interface** | Layer 9 | ❌ (scattered) | **Support ✅** | Cross-Process |
| **TOTAL** | 10 layers | 8-10 layers | **10 abstractions in 3 groups** | **6 steps + 4 cross-process** |

---

## **Abstraction Quality Assessment**

**Option A**:
- ✅ All abstractions present (10 layers)
- ❌ Too many layers (overwhelming)
- ❌ Mixed abstraction levels (capabilities + infrastructure + training)
- ❌ Redundancy (Coordination overlaps Orchestration)

**Option B**:
- ✅ Most complete sequential stack
- ❌ Still overwhelming (8-10 layers when complete)
- ❌ Verification and Human Interface not explicit
- ❌ Mixed abstraction levels persist

**Option C**:
- ✅ **All abstractions cleanly organized** (3 groups)
- ✅ **Cleanest abstraction separation** (Foundation, Core, Support)
- ✅ **No redundancy** (Coordination vs Orchestration clearly distinguished)
- ✅ **Best diagnostic framework** (3 groups → 10 capabilities)
- ✅ **Handles all research insights** (ToolOrchestra, Memory papers, Verification papers)
- ⚠️ Requires explaining 3-group structure

**Option D**:
- ✅ **Most intuitive** (temporal process)
- ✅ **Evaluation as explicit step** (unique insight)
- ✅ All abstractions present (6 steps + 4 cross-process)
- ❌ **Sequential assumption false** (agents aren't purely sequential)
- ❌ **Diagnostic imprecision** (process steps vs. capabilities)
- ❌ **Foundation placement awkward** (not really "cross-process")

---

# **RECOMMENDATIONS**

## **For Complete, Production-Ready Framework → Option C**

**Why**:
- Only option with all 10 abstractions cleanly organized
- Best diagnostic framework
- Clearest abstraction separation
- Handles all research insights (including ToolOrchestra, Verification papers)
- Room to grow without restructuring

**Use for**:
- Academic papers on agent architecture
- Production agent systems
- Framework development
- Long-term architectural planning

---

## **For Communication & Education → Option D**

**Why**:
- Most intuitive (temporal process)
- Easy to explain to non-experts
- Shows agent behavior over time
- Natural for interactive agents

**But supplement with**:
- Clarification that steps aren't strictly sequential
- Explicit mention that Foundation powers all steps

**Use for**:
- Teaching agents to students
- Business stakeholder presentations
- User-facing documentation
- Explainability and transparency

---

## **Avoid → Options A & B**

**Why**:
- Too many layers (9-10) when complete
- Overwhelming for practitioners
- Mixed abstraction levels persist
- No clear advantages over Options C or D

**Unless**:
- Team already deeply committed to sequential layered thinking
- Incremental adoption required (Option A from original 6-layer)

---

## **My Strongest Recommendation: Option C**

Of the four options, **Option C (Capability-Based)** is the only one that:

1. ✅ Includes **all 10 necessary abstractions**
2. ✅ **Cleanly separates** abstraction levels (Foundation, Core, Support)
3. ✅ **Explicitly includes Verification and Human Interface** (only option)
4. ✅ **Handles ToolOrchestra insights** (Coordination in Core, Orchestration in Support)
5. ✅ **Best diagnostic framework** (3 groups → specific capabilities)
6. ✅ **Room to evolve** (can add Core capabilities or Support mechanisms)
7. ✅ **Manageable complexity** (10 abstractions in 3 groups, not 10 sequential layers)

**Option C is complete, clean, and practical.**

---

**Next Steps**: 
1. Choose Option C as the canonical Agent Stack
2. Create detailed specifications (interfaces, information flow)
3. Map all 50+ papers to specific abstractions
4. Build diagnostic framework for debugging agent failures
5. Publish as reference architecture

