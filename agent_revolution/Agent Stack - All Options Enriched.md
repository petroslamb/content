# Agent Stack: All Four Options Enriched with Complete Paper Evidence

**Purpose**: This document presents all four proposed Agent Stack architectures, each fully enriched with the 50+ papers from the comprehensive agent research survey. This allows direct comparison to choose the optimal framework.

---

## **Overview of the Four Options**

| Option | Structure | Layers/Groups | Philosophy |
|--------|-----------|---------------|------------|
| **A** | Sequential Stack | 7 layers | Add Memory to original 6-layer stack |
| **B** | Sequential Stack | 8 layers | Add Memory + Perception for completeness |
| **C** | Capability-Based | 3 groups (Foundation, Core, Support) | Separate concerns by abstraction level |
| **D** | Process-Oriented | Flow + Orthogonal | Agent as temporal process, not layers |

---

# **OPTION A: 7-Layer Sequential Stack (Memory Added)**

```
┌─────────────────────────────────────────────────┐
│  Layer 7: ORCHESTRATION                         │
│  Infrastructure, frameworks, deployment         │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 6: LEARNING                              │
│  RL, experience synthesis, self-evolution       │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 5: COORDINATION                          │
│  Multi-agent collaboration, orchestration       │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 4: ENVIRONMENT                           │
│  Tools, simulators, world models, action        │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 3: REASONING                             │
│  Planning, decomposition, long-horizon thinking │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 2: MEMORY ← ADDED                        │
│  Episodic, semantic, working memory systems     │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 1: FOUNDATION                            │
│  Agentic pre-training, base capabilities        │
└─────────────────────────────────────────────────┘
```

## **Enriched Layer Details:**

### **Layer 1: Foundation**

**Core Concept**: Base model with agentic instincts

**Papers (11 total)**:
1. **Scaling Agents via Continual Pre-training** (2509.13310) - Agentic CPT
2. **Agent Learning via Early Experience** (2510.08558) - Bootstrap learning
3. **Tülu 3** (2411.15124) - RLVR post-training, beats GPT-4o-mini
4. **Agent0** (2511.16043) - Self-evolving from zero data
5. **Scaling Agent Learning via Experience Synthesis** (2511.03773) - Synthetic experience
6. **DR Tulu** (2511.19399) - RLER, 8B matching proprietary systems
7. **Simulating Environments with Reasoning Models** (2511.01824) - Training environments
8. **Agent-R1** (2511.14460) - End-to-end RL for agents
9. **ML-Agent** (2505.23723) - Autonomous ML engineering foundation
10. **MLE-bench** (2507.02554) - Research agent benchmarking
11. **MLAgentBench** (2310.03302) - ML experimentation evaluation

**Capabilities Provided**:
- Trajectory understanding
- Tool-use priors
- Multi-step reasoning instincts
- Experience-based bootstrapping
- RLVR and RLER training paradigms

---

### **Layer 2: Memory ← NEW LAYER**

**Core Concept**: Persistent state management across interactions

**Papers (5 total)**:
1. **General Agentic Memory Via Deep Research** (2511.18423) - Dynamic memory via research
2. **O-Mem: Omni Memory System** (2511.13593) - Personalized, long-horizon memory
3. **MemGen: Generative Latent Memory** (2509.24704) - Self-evolving memory
4. **IterResearch: Markovian State Reconstruction** (2511.07327) - State reconstruction
5. **ReSum: Context Summarization** (2509.13313) - Long-horizon context

**Capabilities Provided**:
- Episodic memory (what happened)
- Semantic memory (what's known)
- Working memory (current context)
- Long-term state preservation
- Memory-augmented reasoning

**Why This Layer is Critical**:
- 5 dedicated papers specifically addressing memory
- Million-step tasks require persistent state
- Long-horizon agents fail without memory management

---

### **Layer 3: Reasoning**

**Core Concept**: Structured cognitive processes

**Papers (15 total)**:

**Basic Reasoning**:
1. **ReAct** (2210.03629) - Thought-action loops
2. **CoCoNuT** (2412.06769) - Continuous latent reasoning

**Formal Reasoning**:
3. **Aristotle** (2510.01346) - IMO-level theorem proving
4. **P1: Physics Olympiads** (2511.13612) - Science-grade reasoning

**Long-Horizon Reasoning**:
5. **Solving Million-Step Tasks** (2511.09030) - Zero-error extended processes
6. **WebResearcher** (2509.13309) - Unbounded reasoning
7. **WebWeaver** (2509.13312) - Dynamic outlines for deep research
8. **IterResearch** (2511.07327) - Markovian state reconstruction

**RL-Based Reasoning**:
9. **Agent-R1** (2511.14460) - End-to-end RL
10. **Tree Search for LLM Agent RL** (2509.21240) - Tree-based reasoning
11. **ToolRM: Outcome Reward Models** (2509.11963) - Tool-calling rewards

**Reasoning Infrastructure**:
12. **DeepAgent** (2510.21618) - Scalable toolsets
13. **In-the-Flow Optimization** (2510.05592) - Planning and tool use
14. **Real-Time Reasoning** (2511.04898) - Evolving environments
15. **WebSailor-V2** (2509.13305) - Synthetic data + scalable RL

**Capabilities Provided**:
- Basic → Formal → Long-Horizon progression
- Tree search and MCTS
- Continuous and discrete reasoning
- Multi-step decomposition
- Real-time adaptation

---

### **Layer 4: Environment**

**Core Concept**: External system interfaces and action execution

**Papers (16 total)**:

**World Models**:
1. **Training Agents Inside Scalable World Models** (2509.24527) - Simulation training
2. **PAN: World Model** (2511.09057) - General world simulation
3. **Simulating Environments with Reasoning Models** (2511.01824) - Reasoning-based envs

**Embodied Agents**:
4. **Lumine** (2511.08892) - 3D open-world agents
5. **π*_{0.6}: VLA** (2511.14759) - Vision-Language-Action from experience
6. **MiMo-Embodied** (2511.16518) - Cross-embodied foundation model

**Software Engineering**:
7. **AIDE** (2502.13138) - AI-driven code exploration (MCTS in code space)
8. **SWE-agent** (2405.15793) - Agent-Computer Interfaces (ACI)
9. **OpenHands** (2407.16741) - Full-stack software agents
10. **MLE-Dojo** (2505.07782) - Interactive ML engineering envs

**Web/Browser**:
11. **WebSailor-V2** (2509.13305) - Web navigation
12. **WebWeaver** (2509.13312) - Web research

**Benchmarks**:
13. **MLGym** (2502.14499) - ML research agent benchmark
14. **MLAgentBench** (2310.03302) - ML experimentation
15. **MLE-bench** (2507.02554) - ML engineering evaluation

**Multimodal**:
16. **DeepEyesV2** (2511.05271) - Agentic multimodal model

**Capabilities Provided**:
- Tool APIs and execution
- World model simulation
- 3D environment navigation
- Code/software interfaces
- Web browsing and research
- Multimodal perception (note: overlaps with missing Perception layer)

**Problem**: Perception is buried here, not explicit

---

### **Layer 5: Coordination**

**Core Concept**: Multi-agent collaboration and orchestration

**Papers (8 total)**:
1. **AutoGen** (2308.08155) - Multi-agent conversations
2. **LatentMAS** (2511.20639) - Latent space collaboration (70-84% token reduction)
3. **ToolOrchestra** (2511.21689) - **8B orchestrating GPT-5** with multi-objective RL
4. **Multi-Agent Deep Research: M-GRPO** (2511.13288) - Training multi-agent systems
5. **OmniScientist** (2511.16931) - Human-AI co-evolution
6. **AgentVerse** (2308.10848) - Multi-agent collaboration patterns
7. **SciAgent** (2511.08151) - Multi-agent scientific reasoning
8. **Denario Project** (2510.26887) - Deep knowledge AI agents

**Capabilities Provided**:
- Text-based agent communication (AutoGen)
- Latent communication (LatentMAS) - massive efficiency
- Learned orchestration (ToolOrchestra) - paradigm shift
- Multi-objective coordination (accuracy, cost, latency, preferences)
- Human-in-the-loop collaboration
- Specialized agent teams

**Key Insight from ToolOrchestra**:
- Coordination can be **learned via RL**, not just designed
- Small orchestrators (8B) beat large models (GPT-5) through strategic coordination
- Multi-objective optimization (not just accuracy)

---

### **Layer 6: Learning**

**Core Concept**: Post-deployment improvement and self-evolution

**Papers (10 total)**:
1. **Agentic RL Survey** (2509.02547) - Comprehensive RL landscape
2. **Agent Learning via Early Experience** (2510.08558) - Pre-reward learning
3. **DR Tulu: RLER** (2511.19399) - Reinforcement Learning with Evolving Rubrics
4. **Agent-R1** (2511.14460) - End-to-end RL
5. **Scaling Agent Learning via Experience Synthesis** (2511.03773) - Synthetic experience
6. **Tree Search for LLM Agent RL** (2509.21240) - MCTS-based learning
7. **Real-Time Reasoning in Evolving Environments** (2511.04898) - Online adaptation
8. **ML-Agent** (2505.23723) - RL for ML engineering
9. **GPT-5 Early Science Experiments** (2511.16072) - Scientific acceleration
10. **π*_{0.6}** (2511.14759) - Learning from RL and corrections

**Capabilities Provided**:
- Pre-deployment RL (RLER, RLVR, GRPO, M-GRPO)
- Online learning (real-time adaptation)
- Experience synthesis (avoid costly rollouts)
- Self-evolution (Agent0, MemGen)
- Curriculum learning
- Multi-objective optimization

---

### **Layer 7: Orchestration**

**Core Concept**: Developer-facing infrastructure

**Papers (9 total)**:
1. **ToolOrchestra** (2511.21689) - Research foundation for learned orchestration
2. **In-the-Flow Agentic System Optimization** (2510.05592) - System-level optimization
3. **Microsoft Agent Framework** (unification of Semantic Kernel + AutoGen)
4. **LangGraph** - Graph-based orchestration
5. **CrewAI** - Role-based teams
6. **DSPy** - Programming not prompting
7. **Haystack** - Production RAG platform
8. **smolagents** - Minimal agent framework
9. **MLE-Dojo** (2505.07782) - Benchmark infrastructure

**Note**: Most are frameworks (not papers), but ToolOrchestra provides research grounding

**Capabilities Provided**:
- Framework infrastructure (LangGraph, CrewAI)
- Deployment pipelines
- Monitoring and observability
- Multi-objective orchestration (ToolOrchestra)
- Learned coordination policies

---

## **Option A: Strengths & Weaknesses**

### **✅ Strengths**:
1. **Simple extension** of familiar 6-layer stack
2. **Memory explicitly addressed** (5 papers validate this)
3. **Clear sequential flow** (easy to understand)
4. **All major papers fit** somewhere in the stack
5. **Good diagnostic value** (which layer failed?)

### **❌ Weaknesses**:
1. **Perception still buried** in Environment (not explicit)
2. **Verification missing** as explicit layer (scattered across Reasoning)
3. **7 layers starting to blur** (which does what?)
4. **Mixed abstraction levels** (capabilities + infrastructure + training)
5. **Coordination overlaps** with Orchestration (both coordinate things)
6. **Environment conflates** training vs. deployment vs. tools vs. perception

### **When to Choose Option A**:
- Want minimal disruption from original 6-layer stack
- Memory was the critical missing piece
- Team comfortable with sequential thinking
- Don't need explicit Perception or Verification layers

---

# **OPTION B: 8-Layer Sequential Stack (Memory + Perception)**

```
┌─────────────────────────────────────────────────┐
│  Layer 8: ORCHESTRATION                         │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 7: LEARNING                              │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 6: COORDINATION                          │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 5: ENVIRONMENT (Action)                  │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 4: REASONING                             │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 3: MEMORY ← ADDED                        │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 2: PERCEPTION ← ADDED                    │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│  Layer 1: FOUNDATION                            │
└─────────────────────────────────────────────────┘
```

## **Enriched Layer Details:**

### **Layers 1, 3-8**: Same as Option A

(Foundation, Memory, Reasoning, Environment, Coordination, Learning, Orchestration all identical to Option A)

### **Layer 2: PERCEPTION ← NEW LAYER (Separated from Environment)**

**Core Concept**: Multimodal input processing and world state estimation

**Papers (6 total)**:
1. **DeepEyesV2: Agentic Multimodal Model** (2511.05271) - Vision-language-action
2. **MiMo-Embodied** (2511.16518) - Cross-embodiment perception
3. **Lumine** (2511.08892) - 3D visual perception in open worlds
4. **π*_{0.6}: VLA** (2511.14759) - Vision-Language-Action model
5. **PAN: World Model** (2511.09057) - Visual state prediction
6. **Training Agents in Scalable World Models** (2509.24527) - Vision-based learning

**Capabilities Provided**:
- Multimodal input (vision, audio, sensors)
- State estimation from observations
- Grounding (text → world state mapping)
- Object detection and scene understanding
- Cross-modal alignment (vision ↔ language ↔ action)

**Why This Layer is Critical**:
- Embodied agents (Lumine, π*_{0.6}, MiMo) need rich perception
- Perception failures are distinct from action failures
- Multimodal models show perception as separate capability
- World models require state estimation

**Information Flow**:
```
External World → PERCEPTION (sense) → MEMORY (store) → 
REASONING (process) → ENVIRONMENT (act) → External World
```

---

### **Layer 5: Environment (Renamed: Action)**

**Now focuses on**: Action execution, not sensing

**Papers**: Same as Option A Environment, but **minus** perception-focused papers (moved to Layer 2)

**Remaining focus**:
- Tool APIs and execution (not sensing)
- Code/software interfaces
- Web browsing (actions, not visual parsing)
- World models (action simulation, not sensing)

---

## **Option B: Strengths & Weaknesses**

### **✅ Strengths**:
1. **Most complete** - explicitly addresses Memory AND Perception
2. **Perception properly separated** from action (conceptually clean)
3. **All 50+ papers fit** naturally into layers
4. **Clear information flow**: Perceive → Remember → Reason → Act
5. **Validates embodied agent papers** (Lumine, MiMo, π*_{0.6})
6. **Diagnostic precision**: Failures in perception vs. action are distinguishable

### **❌ Weaknesses**:
1. **8 layers is overwhelming** - hard to remember, hard to communicate
2. **Sequential assumption too strong** - agents don't always perceive → remember → reason sequentially
3. **Still mixed abstraction levels** (capabilities + infrastructure + training)
4. **Coordination overlap** with Orchestration persists
5. **Verification still missing** as explicit layer
6. **Complexity tax**: explaining 8-layer stack to stakeholders is hard

### **When to Choose Option B**:
- Building embodied agents (Perception critical)
- Need complete coverage (no missing pieces)
- Team can handle complexity
- Diagnostic precision > simplicity

---

# **OPTION C: Capability-Based (Foundation + Core + Support)**

```
┌─────────────────────────────────────────────────────────────┐
│                    SUPPORT LAYERS                           │
│  (How agents improve and integrate)                         │
├─────────────────────────────────────────────────────────────┤
│  • Orchestration (frameworks, deployment, infrastructure)   │
│  • Learning (RL, experience, self-evolution)                │
│  • Verification (benchmarks, evaluation, correctness)       │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      CORE LAYERS                            │
│  (What agents intrinsically do)                             │
├─────────────────────────────────────────────────────────────┤
│  • Perception (multimodal sensing, state estimation)        │
│  • Memory (episodic, semantic, working memory)              │
│  • Reasoning (planning, decomposition, long-horizon)        │
│  • Action (tool use, environment interaction)               │
│  • Coordination (multi-agent collaboration)                 │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                     FOUNDATION                              │
│  (What you start with)                                      │
├─────────────────────────────────────────────────────────────┤
│  • Base Model (pre-training + post-training)                │
└─────────────────────────────────────────────────────────────┘
```

## **Enriched Group Details:**

### **FOUNDATION GROUP**

**Philosophy**: The pre-trained capabilities you start with

**Papers (11 total)**:
- (Same papers as Option A Layer 1 Foundation)
- CPT, Tülu 3, DR Tulu, Agent0, Agent-R1, etc.

**Provides**: Base model with agentic instincts

---

### **CORE GROUP (5 Capabilities)**

**Philosophy**: The inherent capabilities agents execute during operation

#### **Core → Perception**

**Papers (6 total)**:
- DeepEyesV2, MiMo-Embodied, Lumine, π*_{0.6}, PAN, World Models

**Provides**: Sensing and state estimation

---

#### **Core → Memory**

**Papers (5 total)**:
- O-Mem, MemGen, General Agentic Memory, IterResearch, ReSum

**Provides**: Persistent state management

---

#### **Core → Reasoning**

**Papers (15 total)**:
- ReAct, Aristotle, CoCoNuT, Million-Step, WebResearcher, P1, Agent-R1, Tree Search, WebWeaver, ToolRM, DeepAgent, Real-Time Reasoning, IterResearch, WebSailor-V2, In-the-Flow

**Provides**: Cognitive processes (basic → formal → long-horizon)

---

#### **Core → Action (Environment)**

**Papers (16 total)**:
- World Models, PAN, Lumine, π*_{0.6}, MiMo, AIDE, SWE-agent, OpenHands, MLE-Dojo, WebSailor-V2, WebWeaver, MLGym, MLAgentBench, MLE-bench, DeepEyesV2, Simulating Environments

**Provides**: Tool use and execution

---

#### **Core → Coordination**

**Papers (8 total)**:
- AutoGen, LatentMAS, ToolOrchestra, M-GRPO, OmniScientist, AgentVerse, SciAgent, Denario

**Provides**: Multi-agent collaboration (learned and designed)

**Key Insight**: ToolOrchestra shows coordination is both a Core capability AND uses Support (Learning via RL)

---

### **SUPPORT GROUP (3 Meta-Capabilities)**

**Philosophy**: How agents improve, integrate, and validate

#### **Support → Learning**

**Papers (10 total)**:
- Agentic RL Survey, Early Experience, DR Tulu, Agent-R1, Experience Synthesis, Tree Search, Real-Time, ML-Agent, GPT-5 Experiments, π*_{0.6}

**Provides**: Improvement mechanisms (RL, experience, self-evolution)

---

#### **Support → Orchestration**

**Papers (9 total)**:
- ToolOrchestra, In-the-Flow, Microsoft Framework, LangGraph, CrewAI, DSPy, Haystack, smolagents, MLE-Dojo

**Provides**: Infrastructure and deployment

**ToolOrchestra Insight**: Orchestration isn't just infrastructure - it's learned multi-objective coordination

---

#### **Support → Verification** ← NEW CAPABILITY

**Papers (8 total)**:
1. **MLE-bench** (2507.02554) - ML engineering evaluation
2. **MLGym** (2502.14499) - Research agent benchmarks
3. **MLAgentBench** (2310.03302) - ML experimentation eval
4. **MLE-Dojo** (2505.07782) - Interactive evaluation environments
5. **Aristotle** (2510.01346) - Formal verification via Lean
6. **ToolRM** (2509.11963) - Outcome reward models
7. **In-the-Flow Optimization** (2510.05592) - System verification
8. **Real-Time Reasoning** (2511.04898) - Runtime verification

**Provides**: 
- Benchmark infrastructure
- Formal verification (Aristotle/Lean)
- Outcome evaluation (ToolRM)
- Runtime correctness checking
- Performance metrics

**Why This is Critical**:
- 8 papers specifically focused on evaluation/verification
- No other stack option explicitly captures this
- Essential for production agents (can't deploy what you can't verify)

---

## **Option C: Information Flow**

```
FOUNDATION provides base capabilities
         ↓
CORE capabilities execute:
  Perception → (sense world)
  Memory ← (store observations)
  Reasoning → (process information)
  Action → (execute in world)
  Coordination ← → (collaborate with other agents)
         ↓
SUPPORT improves and validates:
  Learning ← (trains Core)
  Verification → (validates Core)
  Orchestration ← → (deploys Core)
```

**Key Insight**: The arrows show that Support both **uses** Core (needs capabilities to improve) and **improves** Core (makes capabilities better).

---

## **Option C: Strengths & Weaknesses**

### **✅ Strengths**:
1. **Clearest abstraction separation**: Foundation (what you have) vs. Core (what you do) vs. Support (how you improve)
2. **Verification explicitly present** (only stack option with this)
3. **ToolOrchestra insights perfectly integrated**: Orchestration in Support, Coordination in Core
4. **Best diagnostic framework**:
   - Foundation problem? → Model too weak
   - Core problem? → Which capability failed? (perception/memory/reasoning/action/coordination)
   - Support problem? → Learning/orchestration/verification issue
5. **No redundancy**: Coordination vs. Orchestration clearly separated
6. **Handles cross-cutting concerns** better (Learning affects all Core, Verification validates all Core)
7. **Easier to communicate**: "Agents have 5 core capabilities, supported by 3 meta-capabilities, built on a foundation"
8. **All 50+ papers fit naturally** with no forced mappings
9. **Room to grow**: Can add Core capabilities or Support mechanisms without restructuring

### **❌ Weaknesses**:
1. **Non-traditional structure**: Not a linear stack (may confuse those expecting layers)
2. **Information flow more complex**: Not simple bottom-up
3. **Coordination placement debatable**: Could argue it's Support (helps Core) rather than Core itself
4. **Requires more explanation**: Need to explain the 3-group philosophy

### **When to Choose Option C**:
- Building complete agent systems (need verification)
- Want clearest abstraction levels
- Team can handle non-traditional structure
- Diagnostic clarity is priority
- Long-term framework evolution important

---

# **OPTION D: Process-Oriented (Temporal Flow)**

```
                    ┌─────────────────────┐
                    │   INPUT (Task)      │
                    └──────────┬──────────┘
                              ↓
              ┌───────────────────────────┐
              │  1. PERCEIVE              │
              │  (Sense environment)      │
              └───────────┬───────────────┘
                         ↓
              ┌───────────────────────────┐
              │  2. REMEMBER              │
              │  (Retrieve context)       │
              └───────────┬───────────────┘
                         ↓
              ┌───────────────────────────┐
              │  3. REASON                │
              │  (Plan and decide)        │
              └───────────┬───────────────┘
                         ↓
              ┌───────────────────────────┐
              │  4. ACT                   │
              │  (Execute action)         │
              └───────────┬───────────────┘
                         ↓
              ┌───────────────────────────┐
              │  5. LEARN                 │
              │  (Update from outcome)    │
              └───────────┬───────────────┘
                         ↓
                    ┌──────────────────────┐
                    │  OUTPUT (Result)     │
                    └──────────────────────┘
                         ↑
                         │
              ┌──────────┴───────────┐
              │  FEEDBACK LOOP       │
              │  (Iterate if needed) │
              └──────────────────────┘

ORTHOGONAL CONCERNS (operate across the flow):
┌────────────────────────────────────────────────┐
│ • COORDINATION (multi-agent synchronization)   │
│ • VERIFICATION (correctness checking)          │
│ • ORCHESTRATION (infrastructure management)    │
│ • FOUNDATION (base model powering all stages)  │
└────────────────────────────────────────────────┘
```

## **Enriched Process Details:**

### **Stage 1: PERCEIVE**

**Papers (6 total)**:
- DeepEyesV2, MiMo-Embodied, Lumine, π*_{0.6}, PAN, World Models

**What happens**: 
- Agent senses current environment state
- Processes multimodal inputs (vision, audio, text, sensors)
- Grounds observations in world model
- Passes observations to Memory stage

---

### **Stage 2: REMEMBER**

**Papers (5 total)**:
- O-Mem, MemGen, General Agentic Memory, IterResearch, ReSum

**What happens**:
- Retrieves relevant past experiences (episodic)
- Accesses semantic knowledge
- Maintains working memory of current task
- Passes context to Reasoning stage

---

### **Stage 3: REASON**

**Papers (15 total)**:
- ReAct, Aristotle, CoCoNuT, Million-Step, WebResearcher, P1, Agent-R1, Tree Search, WebWeaver, ToolRM, DeepAgent, Real-Time, IterResearch, WebSailor-V2, In-the-Flow

**What happens**:
- Plans next actions using retrieved context
- Decomposes complex goals into steps
- Performs formal or informal reasoning
- Selects tools and strategies
- Passes action plan to Act stage

---

### **Stage 4: ACT**

**Papers (16 total)**:
- World Models, PAN, Lumine, π*_{0.6}, MiMo, AIDE, SWE-agent, OpenHands, MLE-Dojo, WebSailor-V2, WebWeaver, MLGym, MLAgentBench, MLE-bench, DeepEyesV2, Simulating Environments

**What happens**:
- Executes planned actions in environment
- Invokes tools and APIs
- Interacts with external systems
- Observes outcomes
- Passes results to Learn stage

---

### **Stage 5: LEARN**

**Papers (10 total)**:
- Agentic RL Survey, Early Experience, DR Tulu, Agent-R1, Experience Synthesis, Tree Search, Real-Time, ML-Agent, GPT-5 Experiments, π*_{0.6}

**What happens**:
- Evaluates action outcomes
- Updates policy/strategy based on rewards
- Synthesizes experience for future use
- Self-evolves based on feedback
- Loops back to Perceive or outputs result

---

### **ORTHOGONAL: Coordination**

**Papers (8 total)**:
- AutoGen, LatentMAS, ToolOrchestra, M-GRPO, OmniScientist, AgentVerse, SciAgent, Denario

**What it does**:
- Operates **across all stages** for multi-agent systems
- Synchronizes Perceive (shared observations)
- Coordinates Reason (distributed planning)
- Aligns Act (collaborative actions)
- Aggregates Learn (collective improvement)

---

### **ORTHOGONAL: Verification**

**Papers (8 total)**:
- MLE-bench, MLGym, MLAgentBench, MLE-Dojo, Aristotle, ToolRM, In-the-Flow, Real-Time

**What it does**:
- Validates **each stage's correctness**:
  - Perceive: Did we sense correctly?
  - Remember: Is retrieved context accurate?
  - Reason: Is the plan sound?
  - Act: Did action succeed?
  - Learn: Did we improve?

---

### **ORTHOGONAL: Orchestration**

**Papers (9 total)**:
- ToolOrchestra, In-the-Flow, Microsoft Framework, LangGraph, CrewAI, DSPy, Haystack, smolagents, MLE-Dojo

**What it does**:
- Manages **infrastructure for all stages**:
  - Deployment of perception models
  - Memory storage backends
  - Reasoning compute allocation
  - Action execution sandboxing
  - Learning job scheduling

---

### **ORTHOGONAL: Foundation**

**Papers (11 total)**:
- CPT, Tülu 3, DR Tulu, Agent0, Agent-R1, Experience Synthesis, Simulating Environments, ML-Agent, MLE-bench, MLGym, MLAgentBench

**What it does**:
- **Powers all stages** with base model:
  - Perceive uses vision encoders
  - Remember uses embedding models
  - Reason uses LLM
  - Act uses LLM + tools
  - Learn uses RL-trained policies

---

## **Option D: Temporal Flow Example**

**Task**: "Book the cheapest flight to Tokyo next week"

```
1. PERCEIVE:
   - See browser, calendar, search results
   - Parse visual UI elements
   - Extract text content
   
2. REMEMBER:
   - Recall: user prefers direct flights
   - Retrieve: Tokyo is 13 hours ahead
   - Access: user's calendar shows flexibility
   
3. REASON:
   - Plan: search flights → compare prices → book best option
   - Decompose: Need to check multiple airlines
   - Strategy: Use price comparison tools first
   
4. ACT:
   - Execute: Navigate to Google Flights
   - Action: Enter "Tokyo" + dates
   - Observe: Results show $850-$1200 range
   
5. LEARN:
   - Outcome: Found flight for $875
   - Update: Direct flights worth $100 premium
   - Store: This search strategy worked
   
FEEDBACK: Success! Book it.

ORTHOGONAL during this:
- COORDINATION: If multi-agent, delegate tasks
- VERIFICATION: Check each step correctness
- ORCHESTRATION: Manage browser, APIs, memory
- FOUNDATION: GPT-4 powering all reasoning
```

---

## **Option D: Strengths & Weaknesses**

### **✅ Strengths**:
1. **Intuitively matches human cognition**: Perceive → Remember → Reason → Act is natural
2. **Temporal dimension explicit**: Shows agent operation over time
3. **Feedback loop clear**: Shows iteration naturally
4. **Explains agent behavior** better than static layers
5. **All 50+ papers fit** (5 stages + 4 orthogonal)
6. **Easy to explain**: "Agents work like humans - sense, remember, think, act, learn"
7. **RL fits perfectly**: Learn stage is explicit in the loop
8. **Handles real-time agents**: Continuous process model

### **❌ Weaknesses**:
1. **Not actually sequential**: Real agents don't strictly Perceive → Remember → Reason → Act
   - Example: Reasoning can trigger new perception
   - Example: Acting updates memory in real-time
2. **Oversimplifies parallel processes**: Agents often do multiple stages simultaneously
3. **Coordination placement awkward**: Is it orthogonal or part of the flow?
4. **Harder to diagnose**: "Where in the loop did it fail?" is less precise than "which layer?"
5. **Temporal assumption**: Doesn't fit batch/offline agents well
6. **Foundation as orthogonal is weird**: It's more fundamental than "orthogonal"

### **When to Choose Option D**:
- Building interactive agents (chatbots, assistants)
- Explaining agents to non-technical audiences
- Temporal behavior is critical (real-time, online learning)
- Want process view over structural view

---

# **FINAL COMPARISON: All 4 Options**

## **Coverage Matrix**

| Capability | Option A | Option B | Option C | Option D |
|------------|----------|----------|----------|----------|
| **Foundation** | ✅ Layer 1 | ✅ Layer 1 | ✅ Foundation | ✅ Orthogonal |
| **Perception** | ❌ Buried in Env | ✅ Layer 2 | ✅ Core | ✅ Stage 1 |
| **Memory** | ✅ Layer 2 | ✅ Layer 3 | ✅ Core | ✅ Stage 2 |
| **Reasoning** | ✅ Layer 3 | ✅ Layer 4 | ✅ Core | ✅ Stage 3 |
| **Action/Environment** | ✅ Layer 4 | ✅ Layer 5 | ✅ Core | ✅ Stage 4 |
| **Coordination** | ✅ Layer 5 | ✅ Layer 6 | ✅ Core | ✅ Orthogonal |
| **Learning** | ✅ Layer 6 | ✅ Layer 7 | ✅ Support | ✅ Stage 5 |
| **Orchestration** | ✅ Layer 7 | ✅ Layer 8 | ✅ Support | ✅ Orthogonal |
| **Verification** | ❌ Missing | ❌ Missing | ✅ Support | ✅ Orthogonal |

---

## **Diagnostic Capability**

**Option A (7-layer)**: 
- "Which of 7 layers failed?"
- ❌ Can't distinguish perception from action (both in Environment)
- ❌ No verification layer to check

**Option B (8-layer)**:
- "Which of 8 layers failed?"
- ✅ Can distinguish perception from action
- ❌ No verification layer
- ❌ Too many layers (hard to remember)

**Option C (3 groups)**:
- "Is it Foundation, Core, or Support?"
- Then: "Which Core capability?" or "Which Support mechanism?"
- ✅ Two-level diagnostic (group → capability)
- ✅ Verification explicit
- ✅ Easiest to remember (3 groups, 5 core, 3 support)

**Option D (process)**:
- "Which stage in the loop failed?"
- ✅ Intuitive (think temporally)
- ❌ Stages aren't actually sequential (false assumption)
- ❌ Harder to pinpoint (failure spans multiple stages)

---

## **Abstraction Clarity**

**Option A**: 🟡 Mixed (capabilities + infrastructure + training)

**Option B**: 🟡 Mixed (capabilities + infrastructure + training)

**Option C**: 🟢 **Cleanest** (Foundation = training, Core = capabilities, Support = infrastructure)

**Option D**: 🟡 Medium (stages = capabilities, orthogonal = infrastructure)

---

## **Paper Fit Quality**

**Option A**: 
- 🟢 All papers fit
- 🟡 Some forced (perception papers awkwardly in Environment)

**Option B**:
- 🟢 All papers fit naturally
- 🟢 No forced mappings

**Option C**:
- 🟢 All papers fit perfectly
- 🟢 Verification papers have a home (unique!)
- 🟢 ToolOrchestra insights cleanly separated (Coordination in Core, Orchestration in Support)

**Option D**:
- 🟢 All papers fit
- 🟡 Some awkwardness (orthogonal vs. stages division)

---

## **Communication Ease**

**Option A**: 🟡 "7 layers" (simple but 7 is a lot)

**Option B**: 🔴 "8 layers" (overwhelming)

**Option C**: 🟢 "3 groups: Foundation, 5 Core capabilities, 3 Support mechanisms" (structured, memorable)

**Option D**: 🟢 "5-stage loop: Perceive → Remember → Reason → Act → Learn" (intuitive)

---

## **Evolution/Extension**

**Option A**: 🟡 Can add layers (but already at 7)

**Option B**: 🔴 8 layers is limit (can't add more)

**Option C**: 🟢 Can add Core capabilities or Support mechanisms without restructuring groups

**Option D**: 🟡 Can add stages but breaks flow metaphor

---

# **RECOMMENDATIONS**

## **For Research/Theory → Choose Option C**

**Why**:
- Cleanest abstraction levels
- Only option with explicit Verification
- Best handles ToolOrchestra insights
- Room to grow
- Best diagnostic framework

**Use when**:
- Writing academic papers about agent architecture
- Building comprehensive agent frameworks
- Need to explain tradeoffs to researchers
- Long-term framework development

---

## **For Education/Communication → Choose Option D**

**Why**:
- Most intuitive (matches human cognition)
- Easy to explain to non-experts
- Temporal view helps understand behavior
- Natural fit for interactive agents

**Use when**:
- Teaching agents to students
- Explaining to business stakeholders
- Building chatbots/assistants
- Documentation for end-users

---

## **For Embodied/Multimodal Agents → Choose Option B**

**Why**:
- Perception explicitly separated
- Most complete coverage
- Clear information flow (sense → think → act)
- Validates vision-language-action papers

**Use when**:
- Building robots
- Developing multimodal agents
- Perception is critical capability
- Can handle 8-layer complexity

---

## **For Incremental Adoption → Choose Option A**

**Why**:
- Minimal change from original 6-layer
- Memory was the critical gap
- Familiar sequential structure
- Good enough for most use cases

**Use when**:
- Team already using 6-layer stack
- Don't want major restructuring
- Memory was the only obvious gap
- Want simplest extension

---

# **MY OVERALL RECOMMENDATION**

## **🏆 Option C: Capability-Based**

**Reasoning**:

1. **Only option with complete coverage** (includes Verification)
2. **Clearest abstraction separation** (Foundation/Core/Support)
3. **Best diagnostic framework** (3 groups × specific capabilities)
4. **Perfectly integrates 50+ papers** (no forced fits)
5. **ToolOrchestra insights cleanly handled** (Coordination ≠ Orchestration)
6. **Room to evolve** (can add capabilities/support without restructuring)
7. **Balances simplicity and completeness** (not 8 layers, not too abstract)

**When NOT to use**:
- Teaching beginners (use Option D's process view)
- Building pure embodied agents (Option B's explicit perception)
- Team committed to sequential layers (Option A is safer)

---

**Next step**: Should I create detailed specifications for Option C (interfaces, information flow, diagnostic framework)?

