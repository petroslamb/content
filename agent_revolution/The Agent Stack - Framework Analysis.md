# The Agent Stack: Framework Analysis & Requirements

**Purpose**: This document extracts the "Agent Stack" concept from the research survey and analyzes it as a standalone framework. We'll identify gaps, requirements, and what's needed to make it complete.

---

## **Current Stack Definition (from blog post)**

The Agent Stack is a 6-layer architecture that organizes how modern AI agents are built:

```
┌─────────────────────────────────────────────────┐
│         Layer 6: ORCHESTRATION                  │
│  Frameworks, deployment, logging, monitoring    │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│         Layer 5: LEARNING                       │
│  RL, early experience, continuous improvement   │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│         Layer 4: COORDINATION                   │
│  Multi-agent, role assignment, collaboration    │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│         Layer 3: ENVIRONMENT                    │
│  Tools, browsers, simulators, world models      │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│         Layer 2: REASONING                      │
│  Planning, self-critique, decomposition         │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│         Layer 1: FOUNDATION                     │
│  Agentic pre-training, base model capabilities  │
└─────────────────────────────────────────────────┘
```

---

## **Layer-by-Layer Analysis**

### **Layer 1: Foundation**

**Current Definition:**
- Base LLM with agentic pre-training
- Trained on trajectories, tool traces, multi-step interactions
- Provides instinctive understanding of agency

**Supporting Research:**
- Scaling Agents via Continual Pre-training (2025)
- Agent Learning via Early Experience (2025)

**Questions:**
- [ ] Does this layer include initial instruction tuning?
- [ ] What about base model scale requirements?
- [ ] How do we measure "agentic capability" in a foundation model?

**Missing:**
- Clear boundary with post-training
- Minimal capability requirements
- Evaluation metrics

---

### **Layer 2: Reasoning**

**Current Definition:**
- Structured cognitive processes
- Planning, self-correction, decomposition
- Algorithmic scaffolding around generation

**Supporting Research:**
- ReAct (2023) - thought-action loops
- Aristotle (2025) - formal verification
- Kosmos (2025) - scientific reasoning
- CoCoNuT (2025) - latent reasoning

**Questions:**
- [ ] Is reasoning a layer or a cross-cutting concern?
- [ ] Where does memory fit? (currently absent)
- [ ] What about different reasoning types (deductive, inductive, abductive)?

**Missing:**
- Memory management
- Context handling
- Reasoning strategy selection
- Bridge papers from 2023-2024 (Reflexion, Tree of Thoughts)

---

### **Layer 3: Environment**

**Current Definition:**
- External system interfaces
- Tools, APIs, simulators
- Observation-action loops

**Supporting Research:**
- World Models (2025) - simulation training
- Lumine (2025) - 3D world interaction
- (Tool use shown in ReAct, Kosmos, etc.)

**Questions:**
- [ ] Is this about training environments or deployment environments?
- [ ] Where does perception fit? (sensing the environment)
- [ ] What about multimodal input processing?

**Missing:**
- Perception as distinct capability
- Tool-use evolution papers (Toolformer, Gorilla)
- Browser/computer control papers (WebArena)
- Clear distinction: training vs. production environments

---

### **Layer 4: Coordination**

**Current Definition:**
- Multi-agent collaboration
- Role assignment, information sharing
- Text or latent communication

**Supporting Research:**
- AutoGen (2023) - multi-agent framework
- LatentMAS (2025) - latent collaboration
- CoCoNuT (2025) - shared reasoning

**Questions:**
- [ ] Does coordination require multiple agents or can it be intra-agent?
- [ ] Where does task decomposition live? (Reasoning or Coordination?)
- [ ] What about human-agent coordination?

**Missing:**
- Human-in-the-loop mechanisms
- Coordination protocols/interfaces
- Task allocation algorithms
- Conflict resolution

---

### **Layer 5: Learning**

**Current Definition:**
- Post-deployment improvement
- RL, trajectory learning, experience-based adaptation

**Supporting Research:**
- Agentic RL Survey (2025)
- Early Experience Learning (2025)

**Questions:**
- [ ] How does this differ from Foundation (which also learns)?
- [ ] Is this online learning only, or offline too?
- [ ] What about transfer learning?

**Missing:**
- Curriculum design
- Sample efficiency strategies
- Safety constraints during learning
- When learning stops (convergence criteria)

---

### **Layer 6: Orchestration**

**Current Definition:**
- Developer-facing infrastructure
- Frameworks, deployment, monitoring

**Supporting Research:**
- (Mentioned: LangGraph, AutoGen, CrewAI - but no research papers)

**Questions:**
- [ ] Is this a research concern or pure engineering?
- [ ] Does it belong in the Stack or is it orthogonal?
- [ ] What are the minimal requirements?

**Missing:**
- Clear scope definition
- Research foundations (if any)
- Relationship to other layers
- Production requirements (SLAs, monitoring, etc.)

---

## **Cross-Cutting Concerns (Not Captured in Layers)**

### **1. Memory**
- **Current status:** Missing as explicit layer
- **Where mentioned:** Vaguely in Reasoning
- **Needed capabilities:**
  - Long-term episodic memory
  - Semantic knowledge storage
  - Working memory/context management
  - Retrieval mechanisms

### **2. Perception**
- **Current status:** Buried in Environment
- **Where mentioned:** Multimodal aspects of Lumine
- **Needed capabilities:**
  - Multimodal input processing (vision, audio, sensors)
  - State estimation from observations
  - Grounding (text to world state mapping)

### **3. Verification/Evaluation**
- **Current status:** Mixed into Reasoning (as self-critique)
- **Where mentioned:** Aristotle's Lean prover
- **Needed capabilities:**
  - Self-assessment and confidence
  - Correctness verification
  - Success/failure detection
  - Metrics and benchmarks

### **4. Human Interface**
- **Current status:** Absent
- **Where mentioned:** Vaguely in Orchestration
- **Needed capabilities:**
  - Feedback mechanisms
  - Interruption/intervention
  - Delegation boundaries
  - Trust and transparency

### **5. Safety & Alignment**
- **Current status:** Not a layer, mentioned in epilogue
- **Where mentioned:** Scattered concerns
- **Needed capabilities:**
  - Value alignment checking
  - Constraint enforcement
  - Reversibility and rollback
  - Harm prevention

---

## **Categories of Problems with Current Stack**

### **A. Completeness Issues**

**Missing Layers/Components:**
1. Memory - explicit layer needed
2. Perception - distinct from Environment
3. Verification - distinct from Reasoning
4. Human Interface - explicit layer needed

### **B. Redundancy/Overlap Issues**

**Fuzzy Boundaries:**
1. Reasoning ↔ Coordination (both involve planning)
2. Learning ↔ Foundation (both about what model knows)
3. Environment ↔ Orchestration (both about infrastructure)

### **C. Abstraction Level Issues**

**Mixing Levels:**
1. Some layers are capabilities (Reasoning)
2. Some are training phases (Foundation, Learning)
3. Some are infrastructure (Orchestration)
4. Some are patterns (Coordination)

### **D. Missing Connections**

**What's Absent:**
1. Information flow between layers
2. Failure propagation patterns
3. Performance dependencies
4. Composition rules
5. Optimization tradeoffs

---

## **What Would Make This Complete?**

### **Requirements for Completeness:**

#### **1. Clear Scope per Layer**
- [ ] Input/output interfaces defined
- [ ] Responsibilities explicitly listed
- [ ] Boundaries with other layers clear
- [ ] Success criteria specified

#### **2. Coverage of All Capabilities**
- [ ] Perception/sensing
- [ ] Memory/recall
- [ ] Reasoning/planning
- [ ] Action/execution
- [ ] Learning/adaptation
- [ ] Coordination/collaboration
- [ ] Verification/evaluation
- [ ] Human interaction

#### **3. Architectural Patterns**
- [ ] Control flow (loops, branches)
- [ ] State management
- [ ] Error recovery
- [ ] Feedback mechanisms
- [ ] Composition rules

#### **4. Cross-Layer Specifications**
- [ ] Information flow diagrams
- [ ] Dependency graphs
- [ ] Failure modes and propagation
- [ ] Performance models
- [ ] Resource budgets

#### **5. Design Principles**
- [ ] When to add/remove layers
- [ ] How to balance emphasis
- [ ] Tradeoff navigation
- [ ] Optimization strategies

#### **6. Validation**
- [ ] Example systems mapped to Stack
- [ ] Diagnostic case studies
- [ ] Predictive power demonstration
- [ ] Falsifiable claims

---

## **Alternative Stack Structures to Consider**

### **Option A: 7-Layer Stack (Add Memory)**
```
7. Orchestration
6. Learning
5. Coordination
4. Environment
3. Reasoning
2. Memory          ← NEW
1. Foundation
```

### **Option B: 8-Layer Stack (Add Memory + Perception)**
```
8. Orchestration
7. Learning
6. Coordination
5. Environment
4. Reasoning
3. Memory          ← NEW
2. Perception      ← NEW
1. Foundation
```

### **Option C: Capability-Based (5 Core + 3 Support)**
```
SUPPORT LAYERS:
- Orchestration (infrastructure)
- Learning (improvement)
- Verification (correctness)

CORE LAYERS:
- Coordination (multi-agent)
- Reasoning (planning)
- Memory (state)
- Perception (sensing)
- Action (environment)

FOUNDATION:
- Base Model
```

### **Option D: Process-Oriented (Instead of Layers)**
```
INPUT → Perceive → Remember → Reason → Act → Learn → OUTPUT
         ↑                                          ↓
         └──────────── Feedback Loop ──────────────┘

With orthogonal concerns:
- Coordination (across processes)
- Verification (at checkpoints)
- Orchestration (infrastructure)
```

---

## **Research Gaps to Fill**

### **Papers We Have:**
1. ✅ ReAct (reasoning-action loop)
2. ✅ AutoGen (multi-agent coordination)
3. ✅ Agentic CPT (foundation training)
4. ✅ Early Experience (learning from deployment)
5. ✅ Agentic RL (learning via optimization)
6. ✅ LatentMAS (efficient coordination)
7. ✅ World Models (environment simulation)
8. ✅ Lumine (embodied 3D agents)
9. ✅ Kosmos (scientific discovery)
10. ✅ Aristotle (formal verification)
11. ✅ CoCoNuT (latent reasoning)

### **Papers We Need:**
- [ ] Memory management (Memorybank? MemGPT?)
- [ ] Perception/multimodal (CLIP? Flamingo?)
- [ ] Tool-use evolution (Toolformer, Gorilla, ToolLLM)
- [ ] Browser agents (WebArena, Computer Use)
- [ ] Reasoning bridges (Reflexion, Tree of Thoughts)
- [ ] Human-AI interaction (Constitutional AI? RLHF?)
- [ ] Verification/evaluation frameworks

---

## **Next Steps: Brainstorming Questions**

1. **Should Memory be its own layer?** If so, where in the stack?

2. **Should Perception be separated from Environment?** Or are they inherently coupled?

3. **Is Orchestration really a layer?** Or is it orthogonal infrastructure?

4. **Should we add explicit Human Interface layer?** Where would it sit?

5. **How do we handle cross-cutting concerns** like safety, interpretability, efficiency?

6. **Should layers be reordered?** Current order: Foundation → Reasoning → Environment → Coordination → Learning → Orchestration

7. **What's the minimal viable stack?** Which layers are truly necessary vs. optional?

8. **How do we validate the Stack?** What would prove/disprove its utility?

9. **Is this the right abstraction?** Should we pivot to process-oriented, capability-based, or something else?

10. **What makes this more than taxonomy?** How do we add theoretical rigor?

---

## **Working Hypotheses to Test**

### **Hypothesis 1: Memory Deserves Its Own Layer**
- **Claim:** Memory is distinct from both Foundation (what's learned) and Reasoning (how to think)
- **Evidence needed:** Examples where memory layer failure is distinct from other layers
- **Counter-evidence:** Cases where memory is just part of context management

### **Hypothesis 2: Perception Should Be Separated**
- **Claim:** Multimodal perception is a capability distinct from environment interaction
- **Evidence needed:** Agents that perceive well but act poorly (or vice versa)
- **Counter-evidence:** Perception is always tied to specific environments

### **Hypothesis 3: The Stack Should Be Process-Oriented, Not Layered**
- **Claim:** Agents are better understood as processes (perceive → reason → act loops) than layers
- **Evidence needed:** Process view explains dynamics better than layer view
- **Counter-evidence:** Layered stack provides better diagnostic value

### **Hypothesis 4: Orchestration Is Not Really a Layer**
- **Claim:** Orchestration is infrastructure that wraps the stack, not part of it
- **Evidence needed:** Orchestration doesn't affect agent capabilities, only deployment
- **Counter-evidence:** Orchestration choices fundamentally constrain what agents can do

---

## **Questions for Discussion**

1. What is the PURPOSE of the Stack? (Diagnostic? Prescriptive? Educational?)
2. Who is the AUDIENCE? (Researchers? Practitioners? Students?)
3. What should the Stack PREDICT? (Performance? Failure modes? Design tradeoffs?)
4. How should we VALIDATE it? (Case studies? Formal proofs? Empirical testing?)
5. What makes it USEFUL beyond taxonomy?

---

*This is a living document. Add thoughts, critiques, and refinements below.*
