## Part 6: Open Problems and Research Directions

Despite all this progress, fundamental questions remain. Here are the most important unsolved problems:

---

### 6.1 Theoretical Foundations

**The question:** What makes a good compositional primitive?

We can measure performance empirically, but we lack theory predicting which operations will compose well. We need:

- Theory connecting Neural Tangent Kernels to composability
- Formal definitions of "modularity" in neural networks  
- Provable bounds on composition depth vs expressiveness

**Current work:** Papers like "On the Principles of Parsimony and Self-Consistency for the Emergence of Intelligence" (2024) are starting to tackle this, but it's still early days.

---

### 6.2 Automated Discovery

**The question:** Can we discover new primitives automatically?

All the primitives we've discussed (attention, SSMs, KANs) were hand-designed by researchers. Can we automate this?

**What we need:**

- Meta-learning over operation spaces (not just architecture graphs)
- Evolutionary methods that create novel computational patterns
- Verification that discovered primitives are truly fundamental

**Current work:** Google's AutoML-Zero evolves basic math operations from scratch. "Discovering Symbolic Models from Deep Learning with Inductive Biases" (2020) learns interpretable mathematical primitives. But we're far from automatically discovering something as significant as attention.

---

### 6.3 Scalable Modular Training

**The question:** How do we efficiently train trillion-parameter modular systems?

Current training is fundamentally sequential (backprop through layers). For truly modular systems, we need:

- Better block-wise parallelization schemes
- Asynchronous modular updates (different blocks train at different speeds)
- Theory of when modules can train independently

**The challenge:** Most approximations that enable parallel training (like block-diagonal gradients) introduce errors that accumulate. Finding approximations that are both efficient and accurate is an open problem.

---

### 6.4 Compositionality at Scale

**The question:** Do compositional advantages hold at 100B+ parameters?

Most research on modular architectures uses smaller models (1-10B parameters). But emergent capabilities appear at scale. Does modularity help or hurt at GPT-4 scale?

**What we need:**

- Empirical studies at scale (expensive!)
- Understanding of how modularity interacts with emergence
- Trade-offs between modularity and raw capacity

**Observations:** GPT-4 reportedly uses MoE (modular), Gemini uses mixture of models (modular), suggesting modularity helps at scale. But we lack rigorous public research.

---

### 6.5 Biological Plausibility

**The question:** Can we make compositional architectures learn like brains?

Backpropagation is biologically implausible (brains can't send gradients backward). The Forward-Forward algorithm is a start, but we need:

- Local learning rules that produce global compositionality
- Understanding of how biological modularity (cortical columns, brain regions) maps to artificial networks
- Principles from neuroscience that inform architectural design

**Why this matters:** Not just for neuroscience—biological learning is incredibly efficient. A child learns language from ~10-100M words; GPT-4 was trained on trillions of tokens. Brains achieve sample-efficient learning through strong compositional inductive biases. Bridging the gap between artificial and biological learning could unlock orders-of-magnitude improvements in data efficiency.

**Recent work:**
- "Predictive Coding Networks" learn through prediction errors (more biologically plausible)
- "Equilibrium Propagation" offers a gradient-descent-like algorithm that's biologically feasible
- Neuroscience-inspired architectures like "Dendritic Networks" that use multi-compartment neurons

---

### 6.6 Interpretability and Mechanistic Understanding

**The question:** Can we understand *what* compositional structures learn and *why* they work?

As architectures become more modular, we have an opportunity for unprecedented interpretability. Each module should have a clear function. But we lack:

**Theoretical tools:**
- Formal methods to analyze information flow in compositional graphs
- Causal attribution: Which modules are responsible for which behaviors?
- Compositional "phase transitions": When does adding a new module type enable qualitatively new capabilities?

**Empirical methods:**
- Activation atlases for modular networks
- Module ablation studies at scale
- Understanding learned routing patterns in MoE

**Why this is critical:** If we can't interpret modular systems, we can't debug them, improve them, or ensure they're safe. The promise of modularity is interpretability—but only if we develop the tools to realize it.

**Current work:**
- Anthropic's "Towards Monosemanticity" uses sparse autoencoders to find interpretable features—could be applied module-by-module
- "Causal Tracing" methods identify which components are responsible for specific outputs
- "Mechanistic Interpretability" community is developing tools, but mostly for monolithic models

**The opportunity:** Compositional architectures could be the key to truly interpretable AI if we invest in the right tools.

---

### 6.7 Compositional Generalization and Systematicity

**The question:** Do modular architectures actually generalize better compositionally?

The whole premise is that compositional structure should enable **systematic generalization**—if you learn "red circle" and "blue square," you should understand "blue circle" even if you've never seen it.

**What we know:**
- Transformers struggle with compositional generalization (Hupkes et al., 2020)
- Explicit modular architectures do better on toy tasks (SCAN, COGS benchmarks)

**What we don't know:**
- Do these advantages scale to real-world tasks?
- Which compositional structures best enable generalization?
- How do we measure compositional generalization in language models?

**The research gap:**

We need:
- Better benchmarks for compositional generalization at scale
- Theory predicting which architectures enable which types of generalization
- Empirical studies on real systems (not just synthetic tasks)

**Recent proposals:**
- "Compositional Explanations of Neurons" (COEN) framework
- "Compositional Generalization via Neural-Symbolic Models"
- "Abstract Reasoning Corpus" (ARC) as a benchmark

**The stakes:** If modular architectures don't actually improve compositional generalization at scale, much of the motivation evaporates. This needs rigorous testing.

---

### 6.8 Hardware Co-Design for Modular Architectures

**The question:** How do we design hardware for compositional computation?

Current accelerators (GPUs, TPUs) are optimized for dense matrix multiplication—perfect for standard Transformers, but potentially suboptimal for modular architectures.

**The mismatch:**

```
GPUs optimize for: Dense matmuls, regular computation
Modular systems need: Sparse routing, dynamic dispatch, heterogeneous ops
```

**What we need:**

1. **Routing-optimized hardware:** Fast switching between modules (MoE routing is currently a bottleneck)

2. **Heterogeneous compute:** Different modules might run best on different hardware (SSMs on CPUs? Attention on GPUs? KANs on FPGAs?)

3. **Memory hierarchies:** External memory architectures need smart caching

4. **Communication fabrics:** Cross-attention between modules requires fast inter-module communication

**Current efforts:**

- **Cerebras:** Wafer-scale chips with massive local memory (good for SSMs)
- **Graphcore:** IPU architecture designed for irregular, graph-like computation
- **SambaNova:** Reconfigurable dataflow architecture
- **Groq:** Low-latency inference (good for dynamic routing)

**The opportunity:** Co-designing algorithms and hardware could yield 10-100× improvements for compositional architectures, just as GPUs enabled the deep learning revolution.

**Research questions:**
- Can we design accelerators that adapt their architecture to the model's architecture?
- Should we move computation to memory (processing-in-memory) for modular systems?
- How do we efficiently implement sparse, dynamic routing in hardware?

---

### 6.9 Compositional Safety and Alignment

**The question:** How do we ensure modular systems are safe and aligned?

This is perhaps the most important open problem. Modular systems introduce new safety challenges:

**Emergent behaviors from composition:**
- Module A is safe, Module B is safe, but A→B→A (composed) produces dangerous behavior
- How do we verify safety of compositions without testing all exponentially-many combinations?

**Adversarial module insertion:**
- If systems can add modules dynamically, can an adversary insert a malicious module?
- How do we authenticate and verify modules?

**Reward hacking through routing:**
- MoE models can learn to route around safety constraints
- Example: Route safety-critical inputs to one expert, exploit another expert for unsafe outputs

**Multi-objective conflicts:**
- Different modules optimized for different objectives might conflict
- How do we ensure alignment across modular components?

**What we need:**

1. **Compositional verification:** Formal methods to verify safety of composed systems

2. **Module sandboxing:** Ensure modules can't bypass safety constraints through composition

3. **Interpretable routing:** Understand *why* the system routes certain inputs to certain modules

4. **Aligned composition rules:** Design composition mechanisms that preserve alignment

**Current work:**
- "Compositional Verification for Neural Networks" (but limited to small networks)
- "Modular Safety" frameworks being developed at Anthropic, OpenAI
- "Circuit Breakers" for LLMs could be implemented as safety modules

**The stakes:** As AI systems become more capable and modular, compositional safety becomes critical. We can't just test the whole system—we need compositional safety guarantees.

---

### 6.10 Economic and Practical Deployment

**The question:** How do we actually deploy compositional systems in production?

This is less discussed in academic papers but crucial for real-world impact.

**Challenges:**

1. **Versioning and updates:** If Module A is updated, do we need to retrain all compositions involving A?

2. **Module marketplaces:** Could we have ecosystems where researchers contribute modules? How do we ensure quality, compatibility, safety?

3. **Personalization:** Different users might need different module compositions. How do we efficiently serve personalized modular models?

4. **Cost optimization:** When should we add more modules vs. make existing modules bigger?

5. **Debugging:** When a compositional system fails, which module is responsible?

**Opportunities:**

- **Modular APIs:** Services like "attention-as-a-service" or "retrieval-as-a-service"
- **Specialized module providers:** Companies focusing on building best-in-class modules for specific domains
- **Dynamic composition:** Systems that adapt their architecture based on deployment constraints (latency budget, cost, etc.)

**Early examples:**
- Hugging Face Hub (model components)
- LangChain (compositional LLM applications)
- MosaicML's model catalog (pre-trained components)

**What we need:** Standards for module interfaces, composition protocols, and safety certification.

---

## Part 7: State of the Field – Who's Building What?

Let's map the current landscape of organizations working on compositional AI:

---

### Industry Leaders

**Google DeepMind**
- Leading: MoE (Switch Transformers, Sparse Mixtures), Perceiver architectures
- Recent: Gemini (rumored to use mixture-of-models)
- Strength: Scale and resources for experimentation

**Meta AI**
- Leading: Modular architectures (Perceiver), efficient training
- Recent: Llama 3 (suspected MoE variants)
- Strength: Open research, strong theory group

**OpenAI**
- Leading: Scaling MoE, speculated compositional reasoning (o1/o3)
- Recent: GPT-4 (confirmed MoE), o1 (test-time compute)
- Strength: Production deployment at scale

**Anthropic**
- Leading: Interpretability of compositional systems, Constitutional AI
- Recent: Claude (architecture details unpublished)
- Strength: Safety-oriented approach to modularity

**Microsoft Research**
- Leading: Neural Architecture Search, efficient transformers
- Recent: Orca (compositional reasoning), Phi (efficient small models)
- Strength: Academic-industrial collaboration

---

### Startups and Specialized Labs

**Together AI**
- Leading: State Space Models, Mamba implementations
- Focus: Open-source efficient architectures
- Impact: Making SSMs production-ready

**Contextual AI** (founded by Dabbish, Chen)
- Leading: RAG architectures, retrieval primitives
- Focus: Enterprise knowledge systems
- Impact: Productizing external memory

**Adept AI**
- Leading: Multi-modal compositional systems
- Focus: Action models (text→actions)
- Impact: Composing perception and control

**Cohere**
- Leading: Modular enterprise systems, retrieval
- Focus: Deployable compositional architectures
- Impact: Production-grade RAG

**MosaicML** (acquired by Databricks)
- Leading: Efficient training, modular pre-training
- Focus: Training infrastructure for compositional systems
- Impact: Making modular training accessible

---

### Academic Centers of Excellence

**Stanford (Chelsea Finn, Percy Liang, Chris Ré groups)**
- Meta-learning, compositional generalization, efficient architectures
- Strong theory + empirical work

**MIT (Yoon Kim, Jacob Andreas groups)**
- Compositional language understanding, modular reasoning
- Focus on interpretability

**CMU (Ruslan Salakhutdinov, Graham Neubig groups)**
- Neural architecture search, efficient transformers
- Strong systems + algorithms work

**UC Berkeley (Pieter Abbeel, Sergey Levine groups)**
- Compositional reinforcement learning, modular policies
- Focus on robotics and control

**University of Washington (Yejin Choi, Luke Zettlemoyer groups)**
- Compositional reasoning, modular language models
- Strong NLP focus

**Allen Institute for AI**
- Open research on modular systems (Tulu, OLMo families)
- Focus on open, reproducible research

---

## Part 8: What to Watch – Predictions and Timelines

Let me put my neck out with some predictions:

---

### Near-Term (6-12 months)

**Prediction 1: SSMs go mainstream**
- Mamba-based models will appear from major labs (Google, Meta, Anthropic)
- Hybrid Attention+SSM architectures become standard for long-context applications
- *Why:* Mamba is mature enough, long-context demand is huge, efficiency gains are compelling
- *Watch:* Llama 4, Gemini 2.5, Claude 4 – likely to incorporate SSM layers

**Prediction 2: MoE becomes standard at scale**
- Most new 100B+ parameter models will use MoE
- We'll see MoE in mid-size models (10-30B) for efficiency
- *Why:* Proven at scale (GPT-4, Mistral), clear cost/performance benefits
- *Watch:* Open models from Meta, AI2, Mistral using MoE

**Prediction 3: Test-time compute becomes a product feature**
- Models that can "think longer" for harder questions
- Exposed as API parameters ("spend up to X tokens reasoning")
- *Why:* OpenAI's o1 proved the concept, demand is clear
- *Watch:* Claude, Gemini, and open alternatives to add this capability

**Prediction 4: Retrieval becomes architectural**
- RAG moves from application layer to model architecture
- Learned retrieval modules integrated into training
- *Why:* Current RAG is brittle, end-to-end optimization is better
- *Watch:* "Native RAG" models from Cohere, Contextual AI, Google

---

### Mid-Term (1-2 years)

**Prediction 5: Heterogeneous architectures become common**
- Models with different layer types: Attention + SSM + External Memory
- No more "pure Transformer" models at the frontier
- *Why:* Different mechanisms for different capabilities, multi-tool is better than one-tool
- *Watch:* Major lab releases mixing multiple primitives

**Prediction 6: Architecture search becomes standard practice**
- NAS for composition rules, not just hyperparameters
- Automated discovery of good module combinations
- *Why:* Search space is huge, human design is bottleneck
- *Watch:* Papers/tools for differentiable composition search

**Prediction 7: Module marketplaces emerge**
- Pre-trained modules you can compose (like Docker for ML)
- Standards for module interfaces and composition
- *Why:* Specialization + reusability drive efficiency
- *Watch:* Extensions to Hugging Face Hub, new platforms

**Prediction 8: Compositional interpretability tools mature**
- Per-module analysis becoming standard practice
- Causal attribution for module behavior
- *Why:* Modularity enables interpretability, demand from safety/regulation
- *Watch:* Tools from Anthropic, Eleuther, open-source community

**Prediction 9: First major KAN-based models**
- If computational efficiency improves, KAN layers in production models
- Hybrid KAN+Transformer architectures
- *Why:* Promising results on smaller scales, interpretability appeal
- *Watch:* Follow-up to KAN papers, potential adoption by smaller labs willing to experiment

---

### Long-Term (3-5 years)

**Prediction 10: Compositional training becomes standard**
- Multi-phase training (discover → compose → specialize)
- Module-wise training and sparse composition
- *Why:* Current end-to-end training doesn't scale, modular training enables continual learning
- *Watch:* Training recipes from major labs, new training frameworks

**Prediction 11: Continual learning systems in production**
- Models that add modules for new tasks without full retraining
- Personalized models via module composition
- *Why:* Retraining from scratch is unsustainable as models grow
- *Watch:* Consumer products with evolving, personalized AI

**Prediction 12: Hardware-software co-design for composition**
- Specialized chips for modular architectures
- Reconfigurable accelerators that adapt to model structure
- *Why:* 10-100× efficiency gains possible with co-design
- *Watch:* Startups in AI hardware, announcements from Cerebras, Groq, etc.

**Prediction 13: Theoretical understanding catches up**
- NTK theory for composition becomes practical design tool
- Principled design of primitives based on theory
- *Why:* Field maturing from empirical to theoretical
- *Watch:* ICML/NeurIPS papers bridging theory and practice

**Prediction 14: Biology-inspired learning gains traction**
- Forward-Forward or similar alternatives to backprop at scale
- Hybrid systems (backprop for some modules, local learning for others)
- *Why:* Sample efficiency demands alternative training methods
- *Watch:* Hinton lab, neuroscience-inspired AI research

**Prediction 15: Compositional AGI architectures**
- Claims of AGI will involve compositional systems (many specialized modules)
- Generality through composition, not single monolithic model
- *Why:* Humans are compositional (separate systems for vision, language, motor control)
- *Watch:* Frontier labs' architecture descriptions in AGI announcements

---

## Part 9: Connection to Current Systems

How do these ideas relate to today's deployed models?

---

### GPT-4 (OpenAI)

**Confirmed compositional elements:**
- Mixture of Experts (confirmed by multiple sources)
- Likely ~8 experts per layer, sparse routing

**Speculated:**
- Possibly heterogeneous layers (different layer types for different capabilities)
- Test-time compute in o1/o3 variants

**What this tells us:** Even industry leaders use composition for scaling. Pure dense transformers peaked around GPT-3.

---

### Claude (Anthropic)

**Known compositional elements:**
- Extended context (likely uses memory-efficient attention variants)
- Constitutional AI (possibly separate safety modules)

**Speculated:**
- Modular safety architecture
- Specialized modules for different capabilities (coding, math, writing)

**What this tells us:** Safety-conscious design may benefit from modularity (isolate and verify safety-critical components).

---

### Gemini (Google)

**Confirmed:**
- Multi-modal composition (vision, audio, text)
- Mixture of models (multiple specialized models composed)

**Speculated:**
- Perceiver-style cross-attention between modalities
- Dynamic routing based on task type

**What this tells us:** Multi-modality naturally leads to composition (different modalities → different architectures).

---

### Llama (Meta)

**Known:**
- Standard Transformer for Llama 2
- Llama 3 suspected to explore efficiency improvements

**Expected in Llama 4:**
- Likely MoE or hybrid architecture
- Possibly SSM integration

**What this tells us:** Open models follow 1-2 years behind proprietary in adopting new compositional techniques.

---

## Part 10: Practical Resources

For those wanting to dive in hands-on:

---

### Codebases and Implementations

**State Space Models:**
- [Mamba official implementation](https://github.com/state-spaces/mamba) - Production-ready SSM
- [S4 repository](https://github.com/HazyResearch/state-spaces) - Original S4 code

**Mixture of Experts:**
- [Megablocks](https://github.com/stanford-futuredata/megablocks) - Efficient MoE implementation
- [Tutel](https://github.com/microsoft/tutel) - Microsoft's MoE library
- [FairSeq MoE](https://github.com/facebookresearch/fairseq/tree/main/examples/moe_lm) - Meta's implementation

**Neural Architecture Search:**
- [DARTS implementation](https://github.com/quark0/darts) - Differentiable architecture search
- [NAS-Bench](https://github.com/google-research/nasbench) - Benchmarking NAS algorithms

**External Memory:**
- [FAISS](https://github.com/facebookresearch/faiss) - Efficient similarity search (for retrieval)
- [Pinecone](https://www.pinecone.io/) - Vector database (production RAG)

**General Compositional Frameworks:**
- [Modular](https://www.modular.com/) - Infrastructure for modular ML
- [PyTorch FX](https://pytorch.org/docs/stable/fx.html) - Graph-based transformations for composition

**Training Techniques:**
- [DeepSpeed](https://github.com/microsoft/DeepSpeed) - Includes MoE training, progressive training
- [MosaicML Composer](https://github.com/mosaicml/composer) - Compositional training recipes

---

### Tutorials and Learning Resources

**Courses:**
- Stanford CS25: Transformers United (covers modern architectures)
- Deep Learning Systems (CMU) - includes modular training

**Tutorial Papers:**
- "A Survey of Transformers" - comprehensive overview
- "Efficient Transformers: A Survey" - covers many compositional techniques
- "Mixture of Experts Explained" - good MoE introduction

**Blogs to Follow:**
- [Lil'Log (Lilian Weng)](https://lilianweng.github.io/) - Excellent technical overviews
- [The Gradient](https://thegradient.pub/) - Research summaries
- [Hugging Face Blog](https://huggingface.co/blog) - Practical implementations
- [Anthropic Research](https://www.anthropic.com/research) - Interpretability focus

---

### Communities:**

- **EleutherAI Discord** - Open research on architecture
- **LAION Discord** - Open models and datasets
- **r/MachineLearning** - Reddit ML community
- **Twitter/X** - Follow researchers cited throughout this post

---

## Part 11: Connecting Back to DR Tulu

Since this deep dive was prompted by the DR Tulu paper, let's connect these ideas back:

---

### DR Tulu as Compositional System

Looking at DR Tulu through the compositional lens:

**Compositional elements:**

1. **Tool use as modular composition:** DR Tulu composes different tools (paper_search, google_search, web_browse) dynamically based on the query.

2. **Evolving rubrics as adaptive verification:** The rubrics co-evolve with the policy—this is a form of meta-learning the composition of evaluation criteria.

3. **Agent infrastructure (MCP):** Model Context Protocol enables composing different modules (retrieval, generation, evaluation) in a flexible framework.

**Connections to this post:**

- **External memory (Section 1.3):** DR Tulu's search tools are essentially external memory modules—it retrieves relevant information rather than relying solely on parametric knowledge.

- **Dynamic routing (Section 2.3):** The model decides which tools to invoke—analogous to MoE routing but over tools rather than expert networks.

- **Meta-learning composition (Section 3.2):** Evolving rubrics that adapt to the policy's current capabilities is a form of meta-learning the evaluation function.

- **Test-time training (Section 4.1):** While not explicit, DR Tulu's multi-step research process is a form of test-time computation—spending more compute to produce better answers.

---

### What DR Tulu Teaches Us About Composition

1. **Composition beyond architecture:** DR Tulu shows that compositional thinking applies to *systems*, not just neural architectures. Tools, prompts, and evaluation criteria can be compositional.

2. **Grounding is a compositional primitive:** The key innovation (grounding rubrics in retrieved knowledge) treats retrieval as a fundamental building block for evaluation, not just generation.

3. **Co-evolution matters:** Static composition is limited. DR Tulu's evolving rubrics show the power of compositions that adapt during training.

4. **Open compositional systems win:** DR Tulu outperforms larger proprietary systems by composing open components effectively—validating the compositional hypothesis.

---

### Future Directions for DR Tulu-Style Systems

Applying ideas from this post to deep research systems:

**Near-term:**
- **Incorporate SSMs** for processing very long documents efficiently
- **Heterogeneous architectures** with specialized modules for different research tasks (math, biology, CS)
- **Learned tool selection** rather than prompted (train which tools to use)

**Mid-term:**
- **Meta-learned research strategies:** Learn composition of tools for different query types
- **Modular evaluation:** Different rubrics for different domains, composed appropriately
- **Continual learning:** Add new tools/modules without retraining entire system

**Long-term:**
- **Automated discovery of research primitives:** Beyond current tools, discover new operations
- **Compositional verification:** Prove properties of research systems through modular analysis
- **Personalized research agents:** User-specific tool compositions

---

## Final Synthesis: The Compositional Paradigm

Let me tie everything together with a unified vision:

---

### The Core Thesis

**We are witnessing a paradigm shift from monolithic neural networks to compositional AI systems.**

This shift is driven by:

1. **Scaling limits:** Dense transformers hit computational walls
2. **Specialization needs:** Different tasks need different inductive biases
3. **Adaptability requirements:** Systems must update and grow over time
4. **Interpretability demands:** We need to understand and control AI systems
5. **Efficiency pressures:** Compute and energy constraints require smarter architectures

---

### The Compositional Stack (Unified View)

```
┌─────────────────────────────────────────────────┐
│                 APPLICATIONS                     │
│  (Chatbots, Research Agents, Code Assistants)   │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│              COMPOSITIONAL SYSTEMS               │
│  • Dynamic tool composition (DR Tulu)           │
│  • Multi-modal fusion (Gemini)                  │
│  • Mixture of specialized models                │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│           COMPOSITIONAL ARCHITECTURES            │
│  • Heterogeneous layers (Attention+SSM+Memory)  │
│  • Dynamic routing (MoE, Expert Choice)         │
│  • Hierarchical attention (Perceiver)           │
└─────────────────────────────────────────────────┐
                      ↑
┌─────────────────────────────────────────────────┐
│            COMPOSITIONAL PRIMITIVES              │
│  • Attention • SSMs • KANs • External Memory    │
│  • Capsules • Hypernetworks • Adaptive Compute  │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│           COMPOSITIONAL TRAINING                 │
│  • Meta-learning • Progressive • Modular        │
│  • Curriculum • Sparse • Continual              │
└─────────────────────────────────────────────────┘
                      ↑
┌─────────────────────────────────────────────────┐
│          COMPOSITIONAL HARDWARE                  │
│  • Heterogeneous accelerators                   │
│  • Routing-optimized chips                      │
│  • Memory-centric architectures                 │
└─────────────────────────────────────────────────┘
```

**Each layer enables the layer above.** Hardware enables training methods, training enables architectures, architectures enable systems, systems enable applications.

---

### The Path Forward

**For the field:** We need to develop all layers of this stack simultaneously. Progress requires:
- Theorists understanding composition principles
- Engineers building tools and infrastructure
- Researchers discovering new primitives and rules
- Hardware designers enabling efficient execution
- Practitioners deploying and testing at scale

**For individuals:** Pick your layer and contribute:
- **Theory:** NTK for composition, verifiable safety, generalization bounds
- **Primitives:** Discover new operations, test at scale
- **Architecture:** Design and search composition rules
- **Training:** Develop modular learning algorithms
- **Systems:** Build practical compositional applications
- **Hardware:** Co-design for compositional compute

---

### The Promise

If we succeed in building truly compositional AI systems, we unlock:

1. **Radical efficiency:** 10-100× improvements through specialized composition
2. **Continual learning:** Systems that grow and adapt without catastrophic forgetting
3. **Interpretability:** Understanding systems through understanding components
4. **Safety:** Verifiable behavior through compositional verification
5. **Democratization:** Composable modules enable broader participation (contribute a module, not a whole model)
6. **Generality:** True general intelligence through rich composition, not monolithic scale

---

### The Challenge

The transition from monolithic to compositional AI is not inevitable. It requires:

- **Investment:** Resources for research on composition (not just scaling current architectures)
- **Infrastructure:** Tools and standards for modular AI
- **Culture shift:** From "bigger models" to "smarter composition"
- **Openness:** Sharing modules and compositions (can't compose if everything is proprietary)
- **Patience:** Compositional advantages may take time to manifest at scale

---

### Closing Thoughts

The Transformer's dominance over the past 7 years was not because it was the final architecture, but because it was the first truly compositional architecture that scaled. It showed us that **structure matters**—that the right inductive biases, expressed through architectural composition, can unlock orders-of-magnitude improvements.

The next 7 years will be about discovering richer compositional structures:
- More diverse primitives (SSMs, KANs, external memory)
- More flexible composition rules (dynamic routing, cross-attention, learned connections)
- More sophisticated training methods (meta-learning, modular optimization, continual learning)

We're at the beginning of the compositional era, not the end. The architectures of 2030 will look as different from today's Transformers as Transformers look from 2015's LSTMs.

**The future of AI is compositional. Let's build it.**

---

### Acknowledgments

This post synthesized ideas from hundreds of researchers whose papers are cited throughout. Special recognition to:

- The S4/Mamba team at Together AI and CMU for pushing SSMs forward
- Google's Switch Transformer and DeepMind's Perceiver teams for production-scale composition
- Meta's open research teams for making compositional research accessible
- Anthropic for pushing compositional interpretability and safety
- The Allen Institute for AI (and teams behind DR Tulu specifically) for demonstrating compositional systems in practice
- The broader ML research community for the Cambrian explosion of ideas in compositional AI

Science is compositional—progress comes from building on others' work. Every paper cited here builds on dozens more. We're all composing together.

---

### Join the Conversation

This is a living document representing the state of the field as of November 2025. By the time you read this, new breakthroughs may have emerged.

**Where to discuss:**
- Twitter/X: #CompositionalAI, #ModularML
- Reddit: r/MachineLearning
- Discord: EleutherAI, LAION communities
- Conferences: NeurIPS, ICML, ICLR, COLM

**How to contribute:**
- Open-source implementations of compositional architectures
- Reproduce and validate claims from papers cited here
- Propose new primitives, composition rules, or training methods
- Write your own synthesis and share different perspectives

The compositional future of AI will be built by all of us, one module at a time.

**Let's compose the future.**
