| Understanding | the      | Physics | of Key-Value | Cache Compression |
| ------------- | -------- | ------- | ------------ | ----------------- |
|               | for LLMs | through | Attention    | Dynamics          |
Ananthanarayanan∗ samhruth@gmail.com
Samhruth
| IIT Delhi, India |     |     |     |                             |
| ---------------- | --- | --- | --- | --------------------------- |
| Ayan Sengupta∗   |     |     |     | ayan.sengupta@ee.iitd.ac.in |
| IIT Delhi, India |     |     |     |                             |
6202 raM 2  ]LC.sc[  1v62410.3062:viXra
tanchak@iitd.ac.in
| Tanmoy Chakraborty |     |     |     |     |
| ------------------ | --- | --- | --- | --- |
| IIT Delhi, India   |     |     |     |     |
Abstract
Asthecontextwindowinlargelanguagemodels(LLMs)expandsintothehundredsofthou-
sandsoftokens,thekey–value(KV)cachehasbecomethedominantmemorybottleneckin
autoregressive decoding, motivating a surge of KV compression methods that report 80%–
90%memorysavingswithminimaldegradationonstandardlong-contextbenchmarks. We
argue that such evaluations obscure a deeper structural issue: attention functions not only
asastoragemechanismbutasaroutingmechanism,andretainingkey–valuepairsdoesnot
guaranteesemanticaccessibilityduringgeneration. Weintroduceaphysics-inspiredframe-
workthattreatsKVcompressionasacontrolledperturbationoftoken-levelroutingwithin
self-attention and distinguish between information retention, accessibility, and utilization.
Usingasuiteofcontrolledsyntheticdatasetsprobingmulti-entitytracking,instancedisam-
biguation,coreferenceconsistency,andmulti-hopreasoning,weuncoverthreekeyempirical
phenomena. First, moderate compression substantially degrades internal representations
while leaving task accuracy largely intact, revealing large redundancy margins. Second, all
evaluated architectures exhibit a sharp hallucination “safety cliff” near 90% compression,
strongly correlated with a spike in our proposed Global Eviction Ratio (GER), indicating
aphasetransitioninsemantic reachabilitywhenanswer-critical tokensaregloballyerased.
Third,architecturaldifferencesproducedistinctroutingdynamics: LLaMAmodelsexhibit
early-layerconsensusandlatediversification,whileQwenmodelsshowfunnel-likebehavior
with late-stage convergence, leading to different compression resilience profiles. Beyond
erasure, we identify a second failure mode – representational rigidity – where tokens sur-
vive but excessive head-level consensus collapses routing flexibility, degrading performance
despite nominal retention. Together, these findings provide empirical evidence for sparse
token-route structures whose survival governs compression tolerance, reframing KV com-
pression as a structural probe of attention geometry, and linking long-context scalability
| with sparsity | and the “lottery | ticket | hypothesis” in self-attention. |     |
| ------------- | ---------------- | ------ | ------------------------------ | --- |
Keywords: KVCacheCompression,AttentionAnalysis,Long-ContextLanguageModels
1 Introduction
The recent evolution of large language models (LLMs) has been defined as much by context
length as by parameter scale (Grattafiori et al., 2024; Yang et al., 2025; Team et al., 2024).
| ∗. Authors contributed | equally. |     |     |     |
| ---------------------- | -------- | --- | --- | --- |
©2026SamhruthAnanthanarayananandAyanSenguptaandTanmoyChakraborty.
License: CC-BY4.0,seehttps://creativecommons.org/licenses/by/4.0/.

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
Context windows have expanded from a few thousand tokens to hundreds of thousands and
beyond, enabling document-level reasoning, repository-scale code analysis, and persistent
conversational memory (Liu et al., 2025c). This trend mirrors earlier scaling laws in pa-
rameters and data (Kaplan et al., 2020; Hoffmann et al., 2022; Muennighoff et al., 2025),
reinforcing the intuition that larger horizons yield greater capability. Yet unlike parame-
ters, whicharesharedacrosstokens, thekey–value(KV)cachegrowslinearlywithsequence
length during autoregressive decoding. For a transformer with L layers, H heads of di-
KV
mension D , batch size B, sequence length S, and precision b, the memory footprint scales
h
as
Memory = B×S ×L×H ×D ×b. (1)
KV h
As S increases, KVstorage rapidly dominates inference memory, often exceeding parameter
storage itself. In practice, memory, not compute, becomes the principal bottleneck (Meng
et al., 2025) for long-context LLMs.
KV cache compression (Li et al., 2024a) emerged as an engineering solution to this
constraint. Methods based on quantization (Hooper et al., 2024; Liu et al., 2024; Kang
et al., 2024), token eviction (Wan et al., 2025; Cai et al., 2025; Li et al., 2024b), adaptive
head pruning (Feng et al., 2025), or clustering (Liu et al., 2025b; Zhang et al., 2025) report
strikingresults: upto80%–90%KVreductionwithlimiteddegradationonbenchmarkssuch
as LongBench and RULER (Bai et al., 2023; Hsieh et al., 2024; Zhang et al., 2024). These
findings have fostered a prevailing assumption: that the KV cache contains substantial
redundancy,andthatcarefulpruningcanremovemostofitwithoutalteringmodelbehavior.
We argue that this assumption overlooks a deeper structural question concerning attention
as a routing system rather than a passive memory store.
Self-attention constructs dynamic token-level computational pathways across heads and
layers (Clark et al., 2019; Voita et al., 2019; Elhage et al., 2021; Olsson et al., 2022).
Induction head analyses and circuit-level studies demonstrate that reasoning depends on
structured cross-layer routes rather than isolated token storage (Elhage et al., 2021; Ols-
son et al., 2022). From this perspective, retaining a key–value pair does not guarantee
functional accessibility; tokens may remain stored yet become unreachable (Lee, 2025) if
routing pathways are severed. Conversely, theoretical work on sparse subnetworks and the
“Lottery Ticket Hypothesis” suggests that a relatively small structured subset of attention
componentsmaysufficetopreservebehaviorwhencriticalroutesremainintact(Frankleand
Carbin,2019;Otsukaetal.,2025a). TheseinsightsmotivateareframingofKVcompression
as a structural perturbation of semantic reachability.
This leads to our central hypothesis: within dense attention layers exist sparse token-
route lottery tickets (TR-LTs) – minimal cross-head and cross-layer pathways that preserve
semantic reachability necessary for correct generation. Mild compression may expose these
latent routes, while extreme compression may destroy them. If true, KV compression
shouldinducenotmerelygradualdegradation, butastructuralphasetransitioninsemantic
accessibility (Ma et al., 2026; Ersoy et al., 2025).
2

|     |     | Physics | of KV | Compression | in LLMs |
| --- | --- | ------- | ----- | ----------- | ------- |
Existing benchmarks only report surface- Our synthetic dataset-driven framework
|     | level metrics |     |     |     | provides mechanistic insights |
| --- | ------------- | --- | --- | --- | ----------------------------- |
Figure 1: Comparison of traditional versus synthetic evaluation frameworks for KV cache
compression. Existing benchmarks (left) primarily report coarse-grained task accuracy,
whereas our synthetic, controlled framework (right) probes structural reachability, routing
| collapse, | and semantic      | fragility | under compression. |     |     |
| --------- | ----------------- | --------- | ------------------ | --- | --- |
| Central   | Research Question |           |                    |     |     |
Does KV compression merely remove redundant memory, or does it reveal and even-
| tually | destroy latent | sparse | token routes | that govern | reasoning? |
| ------ | -------------- | ------ | ------------ | ----------- | ---------- |
To investigate this question, we develop a physics-inspired evaluation framework (Allen-
Zhu, 2024) built upon controlled synthetic datasets and structural metrics (Figure 1).
Rather than evaluating only answer accuracy, we introduce reachability-aware measures
such as the Global Eviction Ratio (GER), which quantifies cross-head erasure of answer-
critical tokens, and head-level consensus, which measures routing coordination and flexibil-
ity. Across multiple architectures (LLaMA and Qwen families) and compression levels up
| to 90%, | several striking | patterns | emerge. |     |     |
| ------- | ---------------- | -------- | ------- | --- | --- |
First,moderatecompressioninducessubstantialrepresentationaldegradationwhileleav-
ing task accuracy largely intact, revealing large redundancy margins. Second, near 90%
compression, all models exhibit a sharp safety cliff in hallucination rates, strongly corre-
lated with spikes in GER, indicating a reachability threshold. Third, architectural depth
dynamics differ fundamentally: LLaMA models exhibit an inverted funnel-shaped pattern
(early consensus, late diversification), whereas Qwen models exhibit a funnel-like pattern
(early exploration, late convergence), implying architecture-dependent sparsity allocation.
Fourth, probing analyses reveal a semantic hierarchy in compression robustness, with sub-
jectentitieslike‘Person’and‘Thing’representationsremainingstable,while‘Organization’,
| ‘Location’, | and especially | ‘Creature’ | degrade | rapidly. |     |
| ----------- | -------------- | ---------- | ------- | -------- | --- |
3

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
| Main | Finding |     |     |     |     |     |     |     |     |
| ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
KV compression induces a structural phase transition in semantic reachability. Rea-
soning persists while sparse token-route lottery tickets survive; collapse occurs when
| global | eviction | or  | excessive | consensus |     | destroys | routing | flexibility. |     |
| ------ | -------- | --- | --------- | --------- | --- | -------- | ------- | ------------ | --- |
Thesefindingsexposetwodistinctfailuremodesundercompression: (i)representational
erasure, where answer tokens are globally evicted across all heads, and (ii) representational
rigidity, where tokens survive, but excessive head consensus prevents flexible utilization.
Compression tolerance, therefore, depends not on raw token count but on effective route
| capacity | within | attention. |     |     |     |     |     |     |     |
| -------- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- |
Byconnectingempiricalcompressiondynamicswithsparsitytheoryinself-attention(Huang
etal.,2022;Otsukaetal.,2025b,a),thisworkreframesKVcompressionfromanengineering
optimization problem into a structural probe of attention. Rather than asking how much
of the KV cache can be discarded without harming accuracy, we ask a deeper question:
what minimal sparse routing structure must survive for reasoning to remain possible? The
answer, we argue, lies in understanding attention as a fragile yet powerful network of latent
| token-route |     | lottery tickets |     | embedded | within | dense | transformers. |     |     |
| ----------- | --- | --------------- | --- | -------- | ------ | ----- | ------------- | --- | --- |
2 Background
2.1 Self-Attention and the KV Cache in Autoregressive Decoding
Transformers (Vaswani et al., 2017) are built upon the self-attention mechanism. Given an
input sequence X ∈ RS×d, each layer computes queries, keys, and values:
|     |     |     | Q   | = XW | , K | = XW | ,   | V = XW | ,   |
| --- | --- | --- | --- | ---- | --- | ---- | --- | ------ | --- |
|     |     |     |     |      | Q   |      | K   |        | V   |
where W ,W ,W ∈ Rd×d k. Scaled dot-product attention is then defined as
|     | Q   | K V |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:18) QK⊤(cid:19)
|     |     |     | Attention(Q,K,V) |     |     | =   | softmax | √   | V.  |
| --- | --- | --- | ---------------- | --- | --- | --- | ------- | --- | --- |
d
k
In multi-head attention (MHA), this operation is replicated across H heads and concate-
nated. In autoregressive decoding, recomputing K and V for all previous tokens at each
timestepwouldincurO(S2)cost.
|     |     |     |     |     | Instead, | modelscachepreviouslycomputedkeysandval- |     |     |     |
| --- | --- | --- | --- | --- | -------- | ---------------------------------------- | --- | --- | --- |
ues, forming the KV cache. At decoding step t, attention is computed between the current
query q and all stored keys K , while values V are reused. Unlike parameters, which
|     | t   |     |     | 1:t |     |     | 1:t |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
are shared across tokens, the KV cache grows linearly in S and B as seen in Equation 1,
making it the dominant memory consumer in long-context inference (Li et al., 2024a).
| 2.2 | Efficient | Attention |     | Mechanisms |     |     |     |     |     |
| --- | --------- | --------- | --- | ---------- | --- | --- | --- | --- | --- |
The quadratic O(S2) time and memory complexity of vanilla self-attention has motivated a
broad spectrum of efficiency-oriented architectures that trade off exactness, expressivity, or
inductive bias for improved scalability (Sun et al., 2026). One line of work enforces struc-
tured sparsity by restricting attention patterns to predefined or learned subsets of tokens,
therebyreducingpairwiseinteractions;representativeexamplesincludeSparseTransformers
4

Physics of KV Compression in LLMs
(Child, 2019), Longformer (Beltagy et al., 2020), and BigBird (Zaheer et al., 2020), which
exploit locality, block structure, or random connectivity to preserve partial global context
while lowering cost. A second family approximates the attention matrix itself: low-rank
projections such as Linformer (Wang et al., 2020) reduce dimensionality prior to softmax
computation, while kernelized or feature-map approaches such as Performer (Choromanski
et al., 2021) replace the softmax kernel with linearizable approximations, achieving O(S)
complexityattheexpenseofapproximationerror. Relatedlocality-basedmethodsconstrain
attention to sliding windows or neighborhood structures (Beltagy et al., 2020), reinforcing
inductivebiasestowardshort-rangedependenciesbutpotentiallylimitinglong-rangereason-
ing. More recently, recurrence- or state-space–based models, such as Mamba (Gu and Dao,
2024), abandon explicit attention altogether, replacing it with structured sequence opera-
tors that maintain implicit memory in linear time. Collectively, these approaches illustrate
distinct compromises between global expressivity, computational efficiency, approximation
fidelity, and hardware alignment, underscoring that attention scalability can be achieved
either by structural sparsification, matrix approximation, architectural redesign, or alter-
native sequence modeling paradigms.
2.3 IO-Aware Exact Attention and KV Sharing Mechanisms
In contrast to approximation-based efficiency methods, FlashAttention (Dao et al., 2022)
demonstratesthatsubstantialperformancegainscanbeachievedwithoutalteringthemath-
ematical definition of softmax attention. Rather than materializing the full S×S attention
matrix in high-bandwidth memory (HBM), FlashAttention reorders computation via tiling
and fusion, performing block-wise softmax normalization and accumulation entirely within
on-chipSRAM.ThisIO-awarereformulationminimizesmemoryreadsandwrites,whichare
often the true bottleneck in modern accelerators, and achieves significant speedups while
preserving exactness. FlashAttention-2 (Dao, 2024) further improves work partitioning,
parallelism, and kernel utilization, delivering higher throughput and better scaling across
GPUs. These results underscore a crucial insight: attention efficiency is frequently con-
strained more by memory bandwidth and data movement than by arithmetic complexity.
Orthogonaltokernel-leveloptimization,architecturalmodificationssuchasMulti-Query
Attention (MQA) (Shazeer, 2019) and Grouped-Query Attention (GQA) (Ainslie et al.,
2023) reduce inference memory by sharing key and value projections across heads. In
standard multi-head attention, each of the H query heads maintains its own K and V
Q
projections; MQA collapses these into a single shared KV head, while GQA generalizes this
by allowing H query heads to share a smaller number H < H of KV heads. This
Q KV Q
reduces KV cache memory proportionally by a factor of H /H , yielding substantial
KV Q
savings duringautoregressivedecoding withminimal degradation inmodel quality. Modern
large-scale LLMs widely adopt GQA or MQA variants due to their favorable trade-offs
betweenmemoryfootprint,decodingspeed,andrepresentationalflexibility(Lietal.,2024a).
Together, IO-aware exact kernels and KV-sharing architectures illustrate complementary
strategies for improving attention efficiency: one targets hardware-level data movement,
while the other reduces structural redundancy in key–value representations.
5

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
2.4 KV Cache Compression
Beyond modifying attention kernels or architectural structure, a rapidly growing line of
work directly compresses KV cache during inference, treating it as a memory management
problem under long-context decoding. Existing methods can be organized along several
orthogonal axes. Quantization-based approaches (Hooper et al., 2024; Yang et al., 2024b)
reduce the bit precision b of stored keys and values – via post-training quantization, mixed-
precision schemes, or dynamic per-layer strategies – achieving linear memory savings with
modest degradation in perplexity. Eviction and heavy-hitter methods selectively discard
tokens deemed unlikely to influence future predictions, using heuristics such as recency
bias, cumulative attention mass, token norms, or learned importance predictors (e.g., H2O
(Zhang et al., 2023), StreamingLLM (Xiao et al., 2024), Scissorhand (Liu et al., 2023), or
CurDKV (Sengupta et al., 2025)); these approaches implicitly assume that attention con-
tributions are highly skewed and that only a small subset of tokens dominates downstream
influence. Chunking and semantic summarization methods (Liu et al., 2025d; Bai et al.,
2024) cluster contiguous or semantically related tokens and replace them with compressed
representatives, attempting to preserve coverage while reducing storage. Query-agnostic
compression mechanisms (Kim et al., 2025; Chari and Durme, 2025) pre-compress KV ten-
sorsindependentofthecurrentquery,exploitingstructuralredundancyacrosstokensorlay-
ers. Finally, adaptive and predictive methods (Ge et al., 2024; Zhou et al., 2025; Feng et al.,
2025; Qin et al., 2025) frame compression as a forecasting problem, dynamically estimating
which tokens will be required in future decoding steps (e.g., expected-attention–based (De-
voto et al., 2025) or AdaKV-style (Feng et al., 2025) approaches), thereby aligning memory
retention with anticipated routing demand.
Acrossthesecategories,evaluationtypicallyreportscompressionratio,latencyoverhead,
perplexity or downstream accuracy degradation, robustness under long or adversarial con-
texts, and whether the method is training-free or requires fine-tuning. Empirical evidence
suggests substantial redundancy in KV storage, with many methods achieving 70%–90%
reductionunderstandardbenchmarks. However,prevailingevaluationspredominantlymea-
sure aggregate retrieval accuracy or task-level performance, implicitly equating token re-
tention with functional preservation. They rarely distinguish between storage, accessibility,
and utilization, leaving open the deeper question of whether compressed caches maintain
the structural routing pathways required for semantic reachability during autoregressive
generation.
3 Methodology
3.1 Datasets and Controlled KV Compression Evaluation
Standardlong-contextbenchmarkssuchasLongBench(Baietal.,2023),InfiniteBench(Zhang
et al., 2024), and RULER (Hsieh et al., 2024) evaluate downstream task accuracy under
extendedcontexts,buttheyarenotdesignedtoisolatethestructuraleffectsofKVcompres-
siononinternalattentionrouting. Inparticular, theyconflatethreedistinctphenomena: (i)
whether information remains stored in the cache, (ii) whether it remains accessible through
viable attention pathways, and (iii) whether it is effectively utilized during generation. A
model may answer correctly because redundancy compensates for routing damage, or fail
6

|     |     |     | Physics |     | of KV | Compression | in LLMs |
| --- | --- | --- | ------- | --- | ----- | ----------- | ------- |
due to unrelated reasoning limitations rather than compression-induced structural collapse.
As emphasized in the Physics of LLMs line of work (Allen-Zhu and Li, 2025, 2024), un-
derstanding scaling behavior requires carefully controlled synthetic settings that expose
internal mechanisms rather than relying solely on naturalistic benchmarks. Motivated by
this perspective, we design a suite of synthetic datasets that treat KV compression as a
| structural | perturbation |     | of  | token | routes | within self-attention. |     |
| ---------- | ------------ | --- | --- | ----- | ------ | ---------------------- | --- |
Our dataset construction follows two complementary paradigms. First, we employ con-
trolled generative synthesis, prompting frontier LLMs with tightly structured instructions
that enforce explicit entity–attribute linkage, mention frequency constraints, and bidirec-
tional querying. Second, we use deterministic template-based construction with slot-filling
to eliminate linguistic confounders and ensure maximal experimental control. Together,
these approaches balance realism and controllability while maintaining route sensitivity.
Design principles. Each dataset is constructed to satisfy four constraints: (1) route
sensitivity, where correct answers depend on preserving specific cross-layer token pathways;
(2) minimal redundancy, preventing accidental recoverability after aggressive eviction; (3)
bidirectional querying, enforcing both subject→attribute and attribute→subject tracing;
and (4) failure interpretability, enabling classification into representational erasure or rigid-
ity. Under these principles, compression functions as a controlled ablation of token-route
structures.
Generation framework. For generative datasets, we use structured prompting to en-
forceattribute-entitybindingsandcontrolledsemanticrelationships. Thegenericprocedure
| is formalized | in      | Algorithm  |              | 1.        |             |            |         |
| ------------- | ------- | ---------- | ------------ | --------- | ----------- | ---------- | ------- |
| Algorithm     | 1       | Controlled |              | Synthetic | Example     | Generation |         |
| Require:      | Subject | s,         | structural   |           | constraints | C, length  | range L |
| Prompt        | LLM     | with       | instructions |           | enforcing   | C          |         |
1:
| Replace | entity | names |     | with synthetic |     | identifiers |     |
| ------- | ------ | ----- | --- | -------------- | --- | ----------- | --- |
2:
| 3: Generate | passage  |       | P      |               |     |               |     |
| ----------- | -------- | ----- | ------ | ------------- | --- | ------------- | --- |
| 4: Generate | QA       | pairs | under  | bidirectional |     | linkage rules |     |
| Validate    | explicit |       | answer | grounding     |     |               |     |
5:
| 6: Store | (P,{(q | ,a  | )}) |     |     |     |     |
| -------- | ------ | --- | --- | --- | --- | --- | --- |
|          |        | i i |     |     |     |     |     |
For template-based datasets, examples are produced via deterministic slot substitution
from pre-generated entity pools, optionally followed by controlled perturbations (e.g., pro-
noun swaps). This removes surface variability while preserving structural dependencies.
Dataset suite. The resulting suite spans short to long contexts (150–1300+ tokens) and
| targets | distinct | routing | stressors: |     |     |     |     |
| ------- | -------- | ------- | ---------- | --- | --- | --- | --- |
• Base task: Short passages with one subject and tightly bound attributes; probes preci-
| sion | of eviction | under | minimal |     | redundancy. |     |     |
| ---- | ----------- | ----- | ------- | --- | ----------- | --- | --- |
•
Knowledge manipulation: Slot-filledbiographiestestingminimallydistributedfactual
| structures | and | systematic |     | eviction | biases. |     |     |
| ---------- | --- | ---------- | --- | -------- | ------- | --- | --- |
• Multi presence: Repeatedentitymentionsrequiringinstancedisambiguation; evaluates
| positional | robustness |     | under | pruning. |     |     |     |
| ---------- | ---------- | --- | ----- | -------- | --- | --- | --- |
7

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
• Multi entity: Multiple semantically linked entities; tests cross-entity and cross-head
routing integrity.
• Long context: Extended passages requiring distributed reasoning across distant spans;
probes route capacity at scale.
• Coreference: Controlled pronoun perturbations with “I don’t know” ground truth;
detects fine-grained routing failures and hallucination under compression.
• Hops: Chain-structured entities requiring multi-hop reasoning; evaluates preservation of
sequential semantic routes.
Representative prompt and template structures are summarized below to ensure repro-
ducibility. Table 3 highlights samples of each task while Table 6 shows forward and reverse
samples in Appendix A
# Base task
Generate a passage about <subject> (150-200 words)
- >=4 directly linked attributes
- Fake entity names
Generate 6 QA pairs linking subject <-> attributes.
# Knowledge manipulation (Template)
<Firstname Lastname> was born on <Date>.
They studied in <University>.
They work as <Occupation>.
They live in <City>.
# Multi presence / Multi entity / Long context
Generate passage (400-1300 words)
- Multiple entities or repeated mentions
- Explicit attribute linkage
- Bidirectional QA generation
# Coreference
<Firstname Lastname> was born on <Date> in <Location>.
<He/She> studied at <University>.
...
# Pronoun-swapped queries -> answer = "I don’t know"
# Hops
Generate subject + 3 linked entities
- Sequential semantic linkage
- 16 QA pairs spanning multi-hop chains
Dataset statistics. Table 1 summarizes the structural characteristics of the synthetic
dataset suite, including average passage length, number of queries per passage, total pas-
sages, and total query count. The datasets span a broad range of context regimes, from
short, tightly controlled passages (e.g., Base task and Knowledge manipulation) to ex-
tended multi-hop narratives exceeding one thousand words (Long context and Hops). This
deliberate variation in passage length and structural complexity enables systematic evalu-
ation across compression ratios, from mild pruning to extreme eviction. Importantly, the
8

|     |     |     | Physics | of KV | Compression | in LLMs |     |     |
| --- | --- | --- | ------- | ----- | ----------- | ------- | --- | --- |
Name PassageLength(words) #Queries TotalPassages TotalQueries LLMGenerated
| Basetask              |     |     | 175±25   |     | 6   | 200  | 1199  | Yes |
| --------------------- | --- | --- | -------- | --- | --- | ---- | ----- | --- |
| Knowledgemanipulation |     |     | 32       |     | 13  | 4000 | 52000 | No  |
| Multipresence         |     |     | 500±100  |     | 10  | 100  | 1000  | Yes |
| Multientity           |     |     | 500±100  |     | 10  | 100  | 1000  | Yes |
| Longcontext           |     |     | 1100±200 |     | 10  | 100  | 1000  | Yes |
| Coreference           |     |     | 44       |     | 9   | 8000 | 72000 | No  |
| Hops                  |     |     | 1100±20  |     | 16  | 100  | 1600  | Yes |
Table 1: Structural summary of the synthetic dataset suite used for controlled KV com-
| pression | evaluation. |     |     |     |     |     |     |     |
| -------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
suite balances LLM-generated passages, which introduce controlled semantic diversity, with
deterministic template-based constructions, which maximize experimental precision. This
combination ensures that compression behavior can be analyzed both under naturalistic
| variability | and under | strictly | controlled |     | structural | constraints. |     |     |
| ----------- | --------- | -------- | ---------- | --- | ---------- | ------------ | --- | --- |
Significance of the generated synthetic datasets. Unlike conventional long-context
benchmarks that primarily report aggregate accuracy, our framework enables causal attri-
bution of compression failures to specific structural mechanisms within attention. The Base
task and Knowledge manipulation datasets isolate eviction precision and entity–attribute
binding stability. Multi presence and Multi entity expose positional sensitivity and cross-
headroutingfragility. Longcontextstressesroutecapacityunderlargetokenbudgets,while
Hops directly probes preservation of multi-step semantic chains. Coreference evaluates fine-
grained representational consistency and hallucination sensitivity. This layered structure
permits systematic classification of failures into representational erasure, where all viable
tokenroutestocriticalinformationareremoved, andrepresentationalrigidity, wheretokens
survive but routing flexibility collapses. Compression is thus analyzed as a structural phase
transition in semantic reachability rather than as a monotonic decline in accuracy.
| 3.2 Tagging | Framework |     |     |     |     |     |     |     |
| ----------- | --------- | --- | --- | --- | --- | --- | --- | --- |
To move beyond aggregate performance metrics, each question–answer pair is annotated
using a structured tagging framework that enables fine-grained behavioral analysis under
compression. The objective is to transform accuracy statistics into interpretable signals
| about internal | representational |     | robustness. |     |     |     |     |     |
| -------------- | ---------------- | --- | ----------- | --- | --- | --- | --- | --- |
Tagging operates along two orthogonal axes: answer type and question difficulty. The
answer-type axis categorizes responses according to semantic domain, allowing us to exam-
ine whether certain conceptual representations are more resilient to compression. The an-
swer categories include Person, Thing, Organization, Creature, Location, Numerals, Date/-
Time, and Event (Table 4 in Appendix A). By decomposing performance along these se-
mantic dimensions, we can detect systematic degradation patterns, identify hierarchies of
representational stability, and evaluate whether compression disproportionately affects par-
| ticular | classes of concepts. |     |     |     |     |     |     |     |
| ------- | -------------------- | --- | --- | --- | --- | --- | --- | --- |
The second axis captures reasoning demand through question-difficulty tags. Questions
are classified as Standard (direct retrieval of explicitly stated information), Manipulated
(requiring implicit contextual interpretation or transformation), or Part (requiring aggre-
gationofinformationdistributedacrossmultipletextualregions). Thisdimensionseparates
9

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
failures caused by token loss from those arising due to reasoning complexity (Table 5 in Ap-
pendix A). A model may retain the necessary tokens yet fail on high-difficulty queries that
require multi-step inference; conversely, it may fail simple retrieval tasks due to represen-
tational erasure.
Together, these tagging axes define a multidimensional evaluation space. Performance
can be decomposed not only by dataset and compression ratio but also by semantic con-
tent and reasoning structure. This structured analysis enables systematic identification
of compression-sensitive domains and facilitates deeper interpretation of model-specific ro-
bustness profiles.
3.3 Experimental Setup
All compression experiments were conducted using NVIDIA’s KVPress library1, which pro-
vides a unified interface for scoring-based and pruning-based KV cache compression during
autoregressive decoding. For all models, KV compression was applied at inference time
without additional fine-tuning. We systematically vary compression ratios from mild prun-
ing (10%) to aggressive eviction (up to 90% removal of KV entries) and report performance
as a function of the retained KV budget.
Scoring and Pruning Strategies. We adopt Expected Attention (Devoto et al., 2025)
asthescoringfunction,whichestimatestokenimportancebyaggregatingexpectedattention
weights across decoding steps and layers. This per-layer scoring mechanism allows high-
salience key–value pairs, particularly those residing in structurally significant heads, to be
preferentially preserved. Two complementary pruning strategies are employed:
• FINCH (Chunk) Press (Corallo and Papotti, 2024) performs chunk-level pruning by
partitioningthecontextintocontiguoussegmentsandremovingthelowest-scoringtokens
within each segment. This approach is computationally efficient and preserves coarse-
grained structural coverage across the document.
• AdaKV Press (Feng et al., 2025) performs head-wise global pruning by ranking KV
entriesacrossallheadssimultaneouslyandremovingthelowest-scoringentriesirrespective
of positional grouping. This provides finer-grained adaptive compression at the cost of
increased overhead.
ThecombinationofFINCHandAdaKVenablesevaluationunderbothcoarsestructural
pruning and globally adaptive head-aware compression, allowing us to analyze whether
routing collapse depends on local chunk structure or global head-level importance.
Inference Regimes. Compression is evaluated under two inference settings:
• Question-agnostic: The model first receives the full context and performs KV pruning
withoutaccesstothedownstreamquestion. Thequeryisprovidedonlyaftercompression.
This setting ensures that eviction decisions are independent of retrieval demands and
reflects realistic deployment scenarios.
• Question-aware: The list of candidate questions is provided prior to pruning, allowing
compression decisions to condition on anticipated query structure. This setting measures
the upper bound of compression tolerance when routing can be optimized for known
retrieval targets.
1. https://github.com/NVIDIA/kvpress/
10

|     |     | Physics | of KV | Compression | in LLMs |     |     |     |
| --- | --- | ------- | ----- | ----------- | ------- | --- | --- | --- |
Comparing these regimes isolates whether compression robustness arises from intrinsic
| route redundancy | or from | query-conditioned |     | pruning | strategies. |     |     |     |
| ---------------- | ------- | ----------------- | --- | ------- | ----------- | --- | --- | --- |
Models. We evaluate five instruction-tuned LLMs spanning two architectural families:
• LLaMA-3.2 3B Instruct and LLaMA-3 8B Instruct (Grattafiori et al., 2024),
• Qwen-2.5 3B Instruct, Qwen-2.5 7B Instruct, and Qwen-2.5 14B Instruct (Yang et al.,
2024a).
These models cover a range of parameter scales (3B–14B) and architectural variations
in attention design and training data, enabling analysis of model-dependent compression
hub2
tolerance. All checkpoints were obtained from the Hugging Face model and used
| without | modification. |     |     |     |     |     |     |     |
| ------- | ------------- | --- | --- | --- | --- | --- | --- | --- |
Implementation Details. All experiments were executed on a single NVIDIA RTX
A6000 GPU using the KVPress text generation pipeline. The default configuration en-
forcesquestion-agnosticpruningunlessexplicitlyoverridden. Generationisperformedusing
greedy decoding to avoid variability introduced by sampling. Performance is evaluated at
thetokenlevel, withanswersmatchedusingtheLLaMA-38Btokenizertoensureconsistent
| segmentation | across models | and | compression | settings. |     |     |     |     |
| ------------ | ------------- | --- | ----------- | --------- | --- | --- | --- | --- |
This setup ensures that performance differences arise solely from KV compression be-
havior rather than decoding randomness or tokenizer inconsistencies, enabling controlled
analysis of structural failure modes under varying compression budgets.
4 Results
We now present a consolidated analysis of compression behavior across tasks, architectures,
and tagging dimensions. Rather than interpreting degradation as a single monotonic de-
cline, the results reveal structured transitions in semantic reachability. Across datasets,
three recurring phenomena emerge: localized performance spikes consistent with sparse
routeselection,architecture-dependentdivergencebetweenretentionandmanipulation,and
systematic collapse of multi-hop reasoning under aggressive compression.
| 4.1 Aggregate | Performance |     | Trends |     |     |     |     |     |
| ------------- | ----------- | --- | ------ | --- | --- | --- | --- | --- |
Table2reportsthebase(0%compression)F1scoresacrossalltasksunderquestion-agnostic
| (AGN) and | question-aware | (AWR)   | settings.        |         |               |           |       |       |
| --------- | -------------- | ------- | ---------------- | ------- | ------------- | --------- | ----- | ----- |
| Model     | Setup          | Base    | Know             | Multi-P | Multi-E       | Long      | Coref | Hops  |
|           | AGN            | 70.05   | 91.28            | 79.64   | 80.33         | 45.93     | 75.63 | 31.54 |
| LLaMA-3   | 8B             |         |                  |         |               |           |       |       |
|           | AWR            | 69.86   | 92.09            | 77.66   | 81.93         | 45.54     | 60.90 | 31.25 |
|           | AGN            | 68.80   | 92.20            | 73.63   | 77.46         | 38.68     | 78.89 | 27.13 |
| Qwen-2.5  | 7B             |         |                  |         |               |           |       |       |
|           | AWR            | 69.63   | 90.93            | 71.88   | 79.38         | 40.20     | 52.00 | 26.35 |
|           | Table          | 2: Base | (0% compression) | F1      | scores across | datasets. |       |       |
2. https://huggingface.co/models
11

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
|     | AGN |     |     | AWR |     |     | AGN |     | AWR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
60
| erocS 1F 60 |              |     |              |     | erocS 1F |              |     |     |              |
| ----------- | ------------ | --- | ------------ | --- | -------- | ------------ | --- | --- | ------------ |
| 40          |              |     |              |     | 40       |              |     |     |              |
|             | Chunk        |     | Chunk        |     |          | Chunk        |     |     | Chunk        |
|             | Ada          |     | Ada          |     |          | Ada          |     |     | Ada          |
| 20          |              |     |              |     | 20       |              |     |     |              |
|             | Base (70.05) |     | Base (69.86) |     |          | Base (68.80) |     |     | Base (69.63) |
0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     | (a) LLaMA-3 | 8B  | Instruct |     |     |     | (b) Qwen-2.5 |     | 7B Instruct |
| --- | ----------- | --- | -------- | --- | --- | --- | ------------ | --- | ----------- |
Figure2: Basetaskperformanceacrosscompressionlevels. Localizedspikesundermoderate
compression suggest sparse substructure effects. Corresponding results for LLaMA-3.2 3B,
Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 27 of Appendix B.
|          | AGN          |     |              | AWR |          |              | AGN |     | AWR          |
| -------- | ------------ | --- | ------------ | --- | -------- | ------------ | --- | --- | ------------ |
| 80       |              |     |              |     | 80       |              |     |     |              |
| erocS 1F |              |     |              |     | erocS 1F |              |     |     |              |
| 60       |              |     |              |     | 60       |              |     |     |              |
| 40       | Chunk        |     | Chunk        |     |          | Chunk        |     |     | Chunk        |
|          | Ada          |     | Ada          |     | 40       | Ada          |     |     | Ada          |
| 20       | Base (91.28) |     | Base (92.09) |     | 20       | Base (92.20) |     |     | Base (90.93) |
0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     | (a) LLaMA-3 | 8B  | Instruct |     |     |     | (b) Qwen-2.5 | 7B  | Instruct |
| --- | ----------- | --- | -------- | --- | --- | --- | ------------ | --- | -------- |
Figure 3: Knowledge manipulation results. Qwen exhibits a more gradual rate of degrada-
| tion | under compression, | particularly |     | in the | question-aware |     | setting. |     |     |
| ---- | ------------------ | ------------ | --- | ------ | -------------- | --- | -------- | --- | --- |
Base task. On the Base task (Figure 2), both models operate near 70% F1 (LLaMA:
70.05 AGN, 69.86 AWR; Qwen: 68.80 AGN, 69.63 AWR). Under increasing compression,
performance generally declines; however, the question-aware setup exhibits localized non-
monotonic spikes, particularly for Qwen around intermediate compression levels. This sug-
gests that moderate pruning can remove interfering or redundant KV routes, temporar-
ily improving alignment. Such behavior is consistent with the existence of sparse token-
route(Zhuetal.,2025)substructureswithinattentionthatremainfunctionallyintactunder
partial eviction.
Knowledge manipulation presents a contrasting pattern (Figure 3). Qwen slightly sur-
passes LLaMA in the question-agnostic setting (92.20 vs. 91.28), and while LLaMA is
marginally stronger in question-aware (92.09 vs. 90.93), Qwen degrades more gradually un-
der higher compression. This task emphasizes structured transformation rather than pure
retrieval, indicating that Qwen’s robustness derives from instruction-conditioned reasoning,
whereas LLaMA’s strength lies in stable factual retention. Notably, both models remain
| above | 90% F1 until | approximately |     | 40% compression. |     |     |     |     |     |
| ----- | ------------ | ------------- | --- | ---------------- | --- | --- | --- | --- | --- |
Coreference(Figure4)exposesapronounceddivergencebetweenAGNandAWR.LLaMA
drops from an aggregate performance of 75.63 (AGN) to 60.90 (AWR), while Qwen drops
fromaggregateperformanceof78.89(AGN)to52.00(AWR),a26.89-pointreduction. Con-
ditioning pruning on anticipated queries appears to bias models toward premature com-
12

|     |     |     | Physics | of  | KV Compression |     | in  | LLMs |     |     |
| --- | --- | --- | ------- | --- | -------------- | --- | --- | ---- | --- | --- |
Standard Questions - AGN Altered Questions - AGN Standard Questions - AGN Altered Questions - AGN
| 80       |     |     |     |     |     | 80       |     |     |     |     |
| -------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- |
| erocS 1F |     |     |     |     |     | erocS 1F |     |     |     |     |
60
60
| 40  | Chunk |     | Chunk |     |     | 40  | Chunk |     | Chunk |     |
| --- | ----- | --- | ----- | --- | --- | --- | ----- | --- | ----- | --- |
|     | Ada   |     | Ada   |     |     |     | Ada   |     | Ada   |     |
20
|     | Base (84.39) |     | Base (63.57) |     |     | 20  | Base (71.53) |     | Base (89.03) |     |
| --- | ------------ | --- | ------------ | --- | --- | --- | ------------ | --- | ------------ | --- |
Standard Questions - AWR Altered Questions - AWR Standard Questions - AWR Altered Questions - AWR
| 80  |     |     |     |     | Chunk |     |     |     |     | Chunk |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | ----- |
80
| erocS 1F |     |     |     |     | Ada          | erocS 1F |     |     |     | Ada          |
| -------- | --- | --- | --- | --- | ------------ | -------- | --- | --- | --- | ------------ |
| 60       |     |     |     |     | Base (29.09) |          |     |     |     | Base (24.72) |
60
| 40  | Chunk        |     |     |     |     | 40  | Chunk        |     |     |     |
| --- | ------------ | --- | --- | --- | --- | --- | ------------ | --- | --- | --- |
|     | Ada          |     |     |     |     |     | Ada          |     |     |     |
| 20  | Base (84.00) |     |     |     |     | 20  | Base (71.81) |     |     |     |
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     |     | (a) LLaMA-3 | 8B Instruct |     |     |     |     | (b) Qwen-2.5 | 7B Instruct |     |
| --- | --- | ----------- | ----------- | --- | --- | --- | --- | ------------ | ----------- | --- |
Figure 4: Coreference performance across setups. Question-aware pruning significantly
| increases | overconfident |     | errors. |     |     |     |     |     |     |     |
| --------- | ------------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
Forward Questions - AGN Reverse Questions - AGN Forward Questions - AGN Reverse Questions - AGN
| 80       |              |     |              |     |     | 80       |              |     |              |     |
| -------- | ------------ | --- | ------------ | --- | --- | -------- | ------------ | --- | ------------ | --- |
| erocS 1F |              |     |              |     |     | erocS 1F |              |     |              |     |
| 60       |              |     |              |     |     | 60       |              |     |              |     |
|          | Chunk        |     | Chunk        |     |     |          | Chunk        |     | Chunk        |     |
| 40       | Ada          |     | Ada          |     |     | 40       | Ada          |     | Ada          |     |
|          | Base (68.00) |     | Base (91.27) |     |     |          | Base (59.28) |     | Base (87.99) |     |
20
Forward Questions - AWR Reverse Questions - AWR Forward Questions - AWR Reverse Questions - AWR
| 80       |              |     |              |     |     | 80       |              |     |              |     |
| -------- | ------------ | --- | ------------ | --- | --- | -------- | ------------ | --- | ------------ | --- |
| erocS 1F |              |     |              |     |     | erocS 1F |              |     |              |     |
| 60       |              |     |              |     |     | 60       |              |     |              |     |
| 40       | Chunk        |     | Chunk        |     |     |          | Chunk        |     | Chunk        |     |
|          | Ada          |     | Ada          |     |     | 40       | Ada          |     | Ada          |     |
|          | Base (66.27) |     | Base (89.05) |     |     |          | Base (59.10) |     | Base (84.65) |     |
20
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     |     | (a) LLaMA-3 | 8B Instruct |          |         |     |             | (b) Qwen-2.5 | 7B Instruct |     |
| --- | --- | ----------- | ----------- | -------- | ------- | --- | ----------- | ------------ | ----------- | --- |
|     |     | Figure      | 5: Multi    | presence | forward |     | vs. reverse | asymmetry.   |             |     |
mitment, reducing their ability to correctly abstain when inconsistencies are introduced,
| supplementing |     | the results | obtained |     | by Jin et | al. (2025). |     |     |     |     |
| ------------- | --- | ----------- | -------- | --- | --------- | ----------- | --- | --- | --- | --- |
Multi presence in Figure 5 illustrates that LLaMA outperforms Qwen (79.64 aggregate
vs. 73.63 aggregate AGN), but forward queries degrade more sharply than reverse queries
under compression (68 forward and 91.27 reverse AGN vs. 66.27 forward and 89.05 reverse
AWR), indicating asymmetric routing fragility when entities are repeated.
Multi entity, in contrast, shows more balanced behavior (LLaMA 80.33 aggregate AGN;
Qwen 77.46 aggregate AGN), suggesting that distributing attributes across distinct entities
mitigates interference (79.94 forward and 80.72 reverse AGN vs. 80.88 forward and 82.98
reverse AWR).
Long context and Hops reveal (Figures 7, 8 and 9) deeper structural limits. Even
without compression, Long context F1 remains modest (LLaMA 45.93 AGN; Qwen 38.68
AGN), and Hops is lower still (LLaMA 31.54 AGN; Qwen 27.13 AGN). Multi-hop reason-
13

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
Forward Questions - AGN Reverse Questions - AGN Forward Questions - AGN Reverse Questions - AGN
| 80       |     |     |     |     | 80       |     |     |     |
| -------- | --- | --- | --- | --- | -------- | --- | --- | --- |
| erocS 1F |     |     |     |     | erocS 1F |     |     |     |
| 60       |     |     |     |     | 60       |     |     |     |
40
| 40  | Chunk        |     |     | Chunk        |     | Chunk        |     | Chunk        |
| --- | ------------ | --- | --- | ------------ | --- | ------------ | --- | ------------ |
|     | Ada          |     |     | Ada          |     | Ada          |     | Ada          |
| 20  |              |     |     |              | 20  |              |     |              |
|     | Base (79.94) |     |     | Base (80.72) |     | Base (75.74) |     | Base (79.18) |
Forward Questions - AWR Reverse Questions - AWR Forward Questions - AWR Reverse Questions - AWR
| 80       |     |     |     |     | 80          |     |     |     |
| -------- | --- | --- | --- | --- | ----------- | --- | --- | --- |
| erocS 1F |     |     |     |     | erocS 1F 60 |     |     |     |
60
| 40  |              |     |     |              | 40  |              |     |              |
| --- | ------------ | --- | --- | ------------ | --- | ------------ | --- | ------------ |
|     | Chunk        |     |     | Chunk        |     | Chunk        |     | Chunk        |
|     | Ada          |     |     | Ada          |     | Ada          |     | Ada          |
| 20  | Base (80.88) |     |     | Base (82.98) | 20  | Base (78.04) |     | Base (80.72) |
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     |     | (a) LLaMA-3 | 8B  | Instruct |     | (b) Qwen-2.5 | 7B  | Instruct |
| --- | --- | ----------- | --- | -------- | --- | ------------ | --- | -------- |
Figure 6: Multi entity results showing reduced directional asymmetry. Corresponding re-
sults for LLaMA-3.2 3B, Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 28 of Ap-
pendix B.
ing degrades more rapidly than direct retrieval (Li et al., 2025) as compression increases,
suggesting that relational pathways are more fragile than token presence.
| Structural |     | Summary |     |     |     |     |     |     |
| ---------- | --- | ------- | --- | --- | --- | --- | --- | --- |
(1) Moderate compression can transiently improve performance by isolating sparse
token-route substructures. (2) Architectural differences determine whether robust-
ness emerges from dense retention (LLaMA) or instruction-conditioned reasoning
(Qwen). (3) Multi-hop and long-range reasoning collapse structurally before com-
plete token loss, indicating failure of semantic connectivity rather than simple mem-
ory removal.
|     |     | AGN |     | AWR |     | AGN |     | AWR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
40
| erocS 1F 40 |     |     |     |     | erocS 1F |     |     |     |
| ----------- | --- | --- | --- | --- | -------- | --- | --- | --- |
30
30
|     | Chunk |     |     | Chunk |     | Chunk |     | Chunk |
| --- | ----- | --- | --- | ----- | --- | ----- | --- | ----- |
20
| 20  | Ada          |     |     | Ada          |     | Ada          |     | Ada          |
| --- | ------------ | --- | --- | ------------ | --- | ------------ | --- | ------------ |
|     | Base (45.93) |     |     | Base (45.54) |     | Base (38.68) |     | Base (40.20) |
10
0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     |           | (a) LLaMA-3 | 8B      | Instruct            |     | (b) Qwen-2.5       | 7B      | Instruct |
| --- | --------- | ----------- | ------- | ------------------- | --- | ------------------ | ------- | -------- |
|     |           | Figure      | 7: Long | context degradation |     | across compression | levels. |          |
| 4.2 | Tag-Level | Analysis    |         |                     |     |                    |         |          |
While aggregate F1 trends reveal structural degradation under compression, tag-level anal-
ysis exposes the semantic and cognitive dimensions along which this degradation unfolds.
14

|     |     |     | Physics | of  | KV  | Compression |     | in LLMs |     |     |
| --- | --- | --- | ------- | --- | --- | ----------- | --- | ------- | --- | --- |
|     | AGN |     |         | AWR |     |             |     | AGN     |     | AWR |
30
25
| erocS 1F |     |     |     |     |     |     | erocS 1F |     |     |     |
| -------- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
| 25       |     |     |     |     |     |     | 20       |     |     |     |
20
|     | Chunk        |     |     | Chunk        |     |     | 15  | Chunk        |     | Chunk        |
| --- | ------------ | --- | --- | ------------ | --- | --- | --- | ------------ | --- | ------------ |
| 15  | Ada          |     |     | Ada          |     |     |     | Ada          |     | Ada          |
|     | Base (31.54) |     |     | Base (31.25) |     |     | 10  | Base (27.13) |     | Base (26.35) |
10
0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     | (a) LLaMA-3 |     | 8B Instruct |     |     |     |     | (b) Qwen-2.5 | 7B  | Instruct |
| --- | ----------- | --- | ----------- | --- | --- | --- | --- | ------------ | --- | -------- |
Figure 8: Hops task performance. Multi-step semantic chaining collapses rapidly under
compression.
By decomposing performance according to answer-type and question-type tags, we can dis-
tinguish between simple token loss and deeper representational fragility. Across datasets,
compression does not affect all semantic categories uniformly; instead, it selectively erodes
| relational, | hierarchical, |     | and morphologically |     |     | complex |     | structures. |     |     |
| ----------- | ------------- | --- | ------------------- | --- | --- | ------- | --- | ----------- | --- | --- |
Answer-Type Tags. Figure 10 shows answer-type performance for the Base task. Al-
though the overall F1 score remains near 70% at 0% compression, tag-level trends reveal
systematic variation. Categories such as Person and Location are relatively stable across
compressionlevels, complementingthesimilarresultsobtainedby Liuetal.(2025a). These
entities are typically realized as concrete nouns with consistent surface forms, enabling di-
rect lexical anchoring in the KV cache. Even when pruning removes a subset of tokens,
| surviving | mentions | are | often | sufficient | for | correct | retrieval. |     |     |     |
| --------- | -------- | --- | ----- | ---------- | --- | ------- | ---------- | --- | --- | --- |
In contrast, Event exhibits significantly sharper degradation. Event answers require
normalization across verb conjugations, aspect markers, and paraphrased action phrases.
Unlike atomic nouns, verbs are distributed across morphologically-varied tokens and syn-
tactic contexts. Under compression, this distributed encoding fragments, leading to in-
complete semantic reconstruction. Performance curves for the Event tag consistently show
earlier inflection points compared to noun-based categories, indicating that relational and
| process-level | representations |     |     | are more | fragile | than | entity | storage. |     |     |
| ------------- | --------------- | --- | --- | -------- | ------- | ---- | ------ | -------- | --- | --- |
The Organization tag reveals a distinct but related weakness. Organizational enti-
ties frequently encode nested relational structure, including sub-entities, roles, or hierar-
chical relationships. In the question-aware setup, both models show sharper declines for
Organization-tagged answers compared to the question-agnostic condition. This suggests
that query-conditioned pruning may collapse hierarchical distinctions into coarse labels.
Under compression, structured representations are simplified, and fine-grained relational
links are among the first to degrade. The failure pattern indicates not merely loss of tokens,
| but loss | of structural |     | decomposition. |     |     |     |     |     |     |     |
| -------- | ------------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
Multi-entity tag results reinforce this interpretation, as shown in Figure 11. The Thing
andOrganization tagsdisplaymoreirregulardegradationcurves,especiallyundermoderate-
to-high compression, while Person and Location remain comparatively stable. This asym-
metry suggests that compression preferentially harms categories requiring cross-token rela-
tional binding rather than those represented by isolated lexical anchors.
15

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
|     | Hop 0 - AGN | Hop 1 - AGN | Hop 2 - AGN | Hop 3 - AGN |
| --- | ----------- | ----------- | ----------- | ----------- |
30
erocS 1F
20
|     | Chunk        | Chunk        | Chunk        | Chunk        |
| --- | ------------ | ------------ | ------------ | ------------ |
|     | Ada          | Ada          | Ada          | Ada          |
| 10  | Base (33.75) | Base (29.17) | Base (33.97) | Base (29.28) |
|     | Hop 0 - AWR  | Hop 1 - AWR  | Hop 2 - AWR  | Hop 3 - AWR  |
30
erocS 1F
20
|     | Chunk        | Chunk        | Chunk        | Chunk        |
| --- | ------------ | ------------ | ------------ | ------------ |
|     | Ada          | Ada          | Ada          | Ada          |
|     | Base (34.01) | Base (29.94) | Base (32.50) | Base (28.54) |
10
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     |             | (a) LLaMA-3 8B | Instruct    |             |
| --- | ----------- | -------------- | ----------- | ----------- |
|     | Hop 0 - AGN | Hop 1 - AGN    | Hop 2 - AGN | Hop 3 - AGN |
30
erocS 1F 25
20
|     | Chunk | Chunk | Chunk | Chunk |
| --- | ----- | ----- | ----- | ----- |
|     | Ada   | Ada   | Ada   | Ada   |
15
|     | Base (29.85) | Base (24.50) | Base (28.75) | Base (25.43) |
| --- | ------------ | ------------ | ------------ | ------------ |
|     | Hop 0 - AWR  | Hop 1 - AWR  | Hop 2 - AWR  | Hop 3 - AWR  |
30
erocS 1F
25
| 20  | Chunk | Chunk | Chunk | Chunk |
| --- | ----- | ----- | ----- | ----- |
|     | Ada   | Ada   | Ada   | Ada   |
15
|     | Base (29.42) | Base (23.73) | Base (26.92) | Base (25.33) |
| --- | ------------ | ------------ | ------------ | ------------ |
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     |     | (b) Qwen-2.5 7B | Instruct |     |
| --- | --- | --------------- | -------- | --- |
Figure 9: Individual hop breakdown showing instability in intermediate semantic links.
Knowledge manipulation further clarifies architectural divergence. As shown in Fig-
ure 12, Qwen exhibits differentiated degradation across tags, whereas LLaMA shows more
synchronized decline. This suggests that Qwen allocates representational capacity unevenly
across semantic domains, preserving certain categories longer under compression, while
LLaMA maintains more uniform retention but collapses more abruptly when compression
| becomes | extreme. |     |     |     |
| ------- | -------- | --- | --- | --- |
Question-Type Tags. Question-type tags reveal how compression interacts with cog-
nitive demands. In the Base task (Figure 13), Standard retrieval questions are relatively
stableuntilmoderatecompression. Thesetasksrequiredirectextractionofexplicitlystated
| facts and | thus depend primarily | on token survival. |     |     |
| --------- | --------------------- | ------------------ | --- | --- |
16

|     |     |     | Physics | of  | KV Compression | in  | LLMs |     |     |
| --- | --- | --- | ------- | --- | -------------- | --- | ---- | --- | --- |
Person - AGN Thing - AGN Organization - AGN Creature - AGN Location - AGN Numerals - AGN Date/Time - AGN Event - AGN
80
erocS 1F
60
|     | 40 Chunk | Chunk | Chunk |     | Chunk | Chunk | Chunk | Chunk | Chunk |
| --- | -------- | ----- | ----- | --- | ----- | ----- | ----- | ----- | ----- |
|     | Ada      | Ada   | Ada   |     | Ada   | Ada   | Ada   | Ada   | Ada   |
20 Base (73.51) Base (69.02) Base (71.21) Base (73.20) Base (73.18) Base (76.94) Base (81.81) Base (64.60)
Person - AWR Thing - AWR Organization - AWR Creature - AWR Location - AWR Numerals - AWR Date/Time - AWR Event - AWR
80
erocS 1F
60
40
|     | Chunk  | Chunk | Chunk |     | Chunk | Chunk | Chunk | Chunk | Chunk |
| --- | ------ | ----- | ----- | --- | ----- | ----- | ----- | ----- | ----- |
|     | 20 Ada | Ada   | Ada   |     | Ada   | Ada   | Ada   | Ada   | Ada   |
Base (73.84) Base (68.94) Base (64.36) Base (73.51) Base (73.42) Base (79.21) Base (81.13) Base (65.19)
0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9
|     |     |     |     |     | (a) LLaMA-3 | 8B Instruct |     |     |     |
| --- | --- | --- | --- | --- | ----------- | ----------- | --- | --- | --- |
Person - AGN Thing - AGN Organization - AGN Creature - AGN Location - AGN Numerals - AGN Date/Time - AGN Event - AGN
80
erocS 1F 60
40
|     | Chunk  | Chunk | Chunk |     | Chunk | Chunk | Chunk | Chunk | Chunk |
| --- | ------ | ----- | ----- | --- | ----- | ----- | ----- | ----- | ----- |
|     | 20 Ada | Ada   | Ada   |     | Ada   | Ada   | Ada   | Ada   | Ada   |
Base (76.63) Base (66.86) Base (79.29) Base (71.05) Base (73.54) Base (66.56) Base (76.60) Base (61.27)
Person - AWR Thing - AWR Organization - AWR Creature - AWR Location - AWR Numerals - AWR Date/Time - AWR Event - AWR
80
erocS 1F 60
|     | 40 Chunk | Chunk | Chunk |     | Chunk | Chunk | Chunk | Chunk | Chunk |
| --- | -------- | ----- | ----- | --- | ----- | ----- | ----- | ----- | ----- |
|     | 20 Ada   | Ada   | Ada   |     | Ada   | Ada   | Ada   | Ada   | Ada   |
Base (76.40) Base (68.28) Base (78.06) Base (70.96) Base (72.07) Base (65.93) Base (76.83) Base (62.67)
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     |     |     |     |     | (b) Qwen-2.5 | 7B Instruct |     |     |     |
| --- | --- | --- | --- | --- | ------------ | ----------- | --- | --- | --- |
Figure 10: Answer-type tag performance in Base task. Corresponding results for LLaMA-
3.2 3B, Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 29 of Appendix B.
Manipulated questions, which require transformation or reinterpretation of context, ex-
pose architectural differences. Qwen maintains closer alignment between AGN and AWR
settings, indicating robust instruction-conditioning. LLaMA, while strong in raw retrieval,
| exhibits | sharper | divergence | under | AWR | in manipulation-heavy |     | tasks. |     |     |
| -------- | ------- | ---------- | ----- | --- | --------------------- | --- | ------ | --- | --- |
Part retrieval questions degrade earliest and most irregularly. These queries require
integrating scattered phrases across different regions of the context. Even when individual
tokens survive eviction, the relational pathways connecting them become fragile. Perfor-
mance curves for Part questions exhibit jagged transitions rather than smooth decline,
indicating intermittent route failure rather than uniform capacity reduction.
Knowledgemanipulationquestiontags(Figure14)highlightQwen’sstrengthinManipu-
lated queries, whereitoutperformsLLaMAmoreconsistentlyundercompression. However,
in pure Standard retrieval, LLaMA retains an advantage. This reinforces the interpretation
that the two architectures allocate representational resources differently: one optimized for
instruction-conditioned flexibility, the other for dense storage and direct recall.
In Multi entity (Figure 15), Part retrieval again exhibits the most instability. Perfor-
mance oscillates across compression levels, indicating a threshold phenomenon where dis-
tributed semantic cues become intermittently unreachable. This instability aligns with the
notionofrepresentationalrigidity: tokensremainpresent, butroutingflexibilitydiminishes,
| preventing | consistent |     | multi-span | integration. |     |     |     |     |     |
| ---------- | ---------- | --- | ---------- | ------------ | --- | --- | --- | --- | --- |
Synthesis of Tag-Level Patterns. Across answer-type and question-type dimensions,
three consistent patterns emerge. First, relational and hierarchical categories (Event, Orga-
17

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
Person - AGN Thing - AGN Organization - AGN Creature - AGN Location - AGN Numerals - AGN Date/Time - AGN Event - AGN
| 100         |     |     |     |     |     | Chunk        |     | Chunk        |
| ----------- | --- | --- | --- | --- | --- | ------------ | --- | ------------ |
| erocS 1F 75 |     |     |     |     |     | Ada          |     | Ada          |
|             |     |     |     |     |     | Base (40.00) |     | Base (44.68) |
50
| Chunk        |     | Chunk        | Chunk        | Chunk        | Chunk         |     | Chunk        |     |
| ------------ | --- | ------------ | ------------ | ------------ | ------------- | --- | ------------ | --- |
| 25 Ada       |     | Ada          | Ada          | Ada          | Ada           |     | Ada          |     |
| Base (92.26) |     | Base (61.52) | Base (81.38) | Base (83.73) | Base (100.00) |     | Base (78.33) |     |
0
Person - AWR Thing - AWR Organization - AWR Creature - AWR Location - AWR Numerals - AWR Date/Time - AWR Event - AWR
100
|             |     |     |     |     |     | Chunk        |     | Chunk        |
| ----------- | --- | --- | --- | --- | --- | ------------ | --- | ------------ |
| erocS 1F 75 |     |     |     |     |     | Ada          |     | Ada          |
|             |     |     |     |     |     | Base (44.44) |     | Base (47.53) |
50
| Chunk        |     | Chunk        | Chunk        | Chunk        | Chunk         |     | Chunk        |     |
| ------------ | --- | ------------ | ------------ | ------------ | ------------- | --- | ------------ | --- |
| 25 Ada       |     | Ada          | Ada          | Ada          | Ada           |     | Ada          |     |
| Base (93.46) |     | Base (63.26) | Base (90.27) | Base (78.55) | Base (100.00) |     | Base (84.72) |     |
0
0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9
|     |     |     | (a) | LLaMA-3 | 8B Instruct |     |     |     |
| --- | --- | --- | --- | ------- | ----------- | --- | --- | --- |
Person - AGN Thing - AGN Organization - AGN Creature - AGN Location - AGN Numerals - AGN Date/Time - AGN Event - AGN
100
|             |     |     |     |     |     | Chunk       |     | Chunk        |
| ----------- | --- | --- | --- | --- | --- | ----------- | --- | ------------ |
| erocS 1F 75 |     |     |     |     |     | Ada         |     | Ada          |
|             |     |     |     |     |     | Base (6.82) |     | Base (38.87) |
50
| Chunk        |     | Chunk        | Chunk        | Chunk        | Chunk        |     | Chunk        |     |
| ------------ | --- | ------------ | ------------ | ------------ | ------------ | --- | ------------ | --- |
| 25 Ada       |     | Ada          | Ada          | Ada          | Ada          |     | Ada          |     |
| Base (91.53) |     | Base (53.99) | Base (91.25) | Base (77.02) | Base (97.62) |     | Base (69.32) |     |
0
Person - AWR Thing - AWR Organization - AWR Creature - AWR Location - AWR Numerals - AWR Date/Time - AWR Event - AWR
| 100 |     |     |     |     |     | Chunk |     | Chunk |
| --- | --- | --- | --- | --- | --- | ----- | --- | ----- |
|     |     |     |     |     |     | Ada   |     | Ada   |
erocS 1F 75
|              |     |              |              |              |              | Base (12.90) |              | Base (44.65) |
| ------------ | --- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ |
| 50 Chunk     |     | Chunk        | Chunk        | Chunk        | Chunk        |              | Chunk        |              |
| 25 Ada       |     | Ada          | Ada          | Ada          | Ada          |              | Ada          |              |
| Base (93.22) |     | Base (56.19) | Base (92.64) | Base (76.17) | Base (97.62) |              | Base (69.44) |              |
0 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     |     |     | (b) | Qwen-2.5 | 7B Instruct |     |     |     |
| --- | --- | --- | --- | -------- | ----------- | --- | --- | --- |
Figure 11: Answer-type tag behavior in Multi entity. Corresponding results for LLaMA-3.2
3B, Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 30 of Appendix B.
nization, Part)degradeearlierthanatomicentitycategories. Second, compressioninteracts
with architecture-specific biases: Qwen preserves manipulation robustness longer, whereas
LLaMA maintains stronger direct retention. Third, degradation often manifests as insta-
bility rather than smooth decline, suggesting phase transitions in token-route connectivity
| rather than | linear | capacity | reduction. |     |     |     |     |     |
| ----------- | ------ | -------- | ---------- | --- | --- | --- | --- | --- |
These findings reinforce the interpretation that KV compression erodes semantic con-
nectivity before eliminating token storage. Tag-level results, therefore, provide empirical
support for viewing compression as a structural perturbation of token-route graphs, with
| relational | categories | serving | as early | indicators | of route collapse. |     |     |     |
| ---------- | ---------- | ------- | -------- | ---------- | ------------------ | --- | --- | --- |
5 Discussion
WeinterpretKVcachingasaroutingsubstrate: compressionperturbsnotonlymemorysize,
but the existence and exploitability of token-level routes that carry evidence to the decoder.
Across our analyses, two quantities dominate: (i) reachability – whether answer-critical
tokens remain accessible through any surviving head-wise pathway, and (ii) adaptivity –
whether the model retains enough head diversity to re-route attention when the context
becomes sparse. We organize the discussion around these mechanisms and connect them
to architectural depth profiles, the universal safety cliff, and probing-based evidence of a
| representation–behavior |     | gap. |     |     |     |     |     |     |
| ----------------------- | --- | ---- | --- | --- | --- | --- | --- | --- |
18

|     |     |     | Physics | of  | KV Compression |     | in  | LLMs |     |     |     |
| --- | --- | --- | ------- | --- | -------------- | --- | --- | ---- | --- | --- | --- |
Person - AGN Thing - AGN Organization - AGN Location - AGN Date/Time - AGN
100
erocS 1F 75
50
|     | Chunk |     | Chunk |     |     | Chunk |     | Chunk |     | Chunk |     |
| --- | ----- | --- | ----- | --- | --- | ----- | --- | ----- | --- | ----- | --- |
|     | Ada   |     | Ada   |     |     | Ada   |     | Ada   |     | Ada   |     |
25
Base (96.61) Base (99.41) Base (98.75) Base (84.42) Base (90.26)
Person - AWR Thing - AWR Organization - AWR Location - AWR Date/Time - AWR
100
erocS 1F 75
50
|     | Chunk |     | Chunk |     |     | Chunk |     | Chunk |     | Chunk |     |
| --- | ----- | --- | ----- | --- | --- | ----- | --- | ----- | --- | ----- | --- |
| 25  | Ada   |     | Ada   |     |     | Ada   |     | Ada   |     | Ada   |     |
Base (97.65) Base (98.55) Base (99.05) Base (85.86) Base (90.78)
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     |     |     |     | (a) | LLaMA-3 | 8B Instruct |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------- | ----------- | --- | --- | --- | --- | --- |
Person - AGN Thing - AGN Organization - AGN Location - AGN Date/Time - AGN
100
erocS 1F 75
50
|     | Chunk |     | Chunk |     |     | Chunk |     | Chunk |     | Chunk |     |
| --- | ----- | --- | ----- | --- | --- | ----- | --- | ----- | --- | ----- | --- |
|     | Ada   |     | Ada   |     |     | Ada   |     | Ada   |     | Ada   |     |
25
Base (99.42) Base (90.80) Base (99.59) Base (90.50) Base (86.97)
Person - AWR Thing - AWR Organization - AWR Location - AWR Date/Time - AWR
100
erocS 1F
75
50
|     | Chunk |     | Chunk |     |     | Chunk |     | Chunk |     | Chunk |     |
| --- | ----- | --- | ----- | --- | --- | ----- | --- | ----- | --- | ----- | --- |
| 25  | Ada   |     | Ada   |     |     | Ada   |     | Ada   |     | Ada   |     |
Base (98.52) Base (95.42) Base (99.70) Base (82.52) Base (90.33)
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     |        |     |           | (b)          | Qwen-2.5 | 7B Instruct |     |           |           |     |     |
| --- | ------ | --- | --------- | ------------ | -------- | ----------- | --- | --------- | --------- | --- | --- |
|     | Figure | 12: | Knowledge | manipulation |          | answer-type |     | tag-level | behavior. |     |     |
Basic Retrieval - AGNManipulated Retrieval - AGN Part Retrieval - AGN Basic Retrieval - AGNManipulated Retrieval - AGN Part Retrieval - AGN
80
| 80       |              |              |     |              |     |             |              |     |              |     | Chunk        |
| -------- | ------------ | ------------ | --- | ------------ | --- | ----------- | ------------ | --- | ------------ | --- | ------------ |
| erocS 1F |              |              |     |              |     | erocS 1F 60 |              |     |              |     | Ada          |
| 60       |              |              |     |              |     |             |              |     |              |     | Base (33.42) |
| 40       |              |              |     |              |     | 40          |              |     |              |     |              |
|          | Chunk        | Chunk        |     | Chunk        |     |             | Chunk        |     | Chunk        |     |              |
| 20       | Ada          | Ada          |     | Ada          |     | 20          | Ada          |     | Ada          |     |              |
|          | Base (69.94) | Base (85.43) |     | Base (46.69) |     |             | Base (68.85) |     | Base (70.27) |     |              |
Basic Retrieval - AWRManipulated Retrieval - AWR Part Retrieval - AWR 80 Basic Retrieval - AWRManipulated Retrieval - AWR Part Retrieval - AWR
| 80       |              |              |     |     | Chunk        |          |              |     |              |     | Chunk        |
| -------- | ------------ | ------------ | --- | --- | ------------ | -------- | ------------ | --- | ------------ | --- | ------------ |
| erocS 1F |              |              |     |     | Ada          | erocS 1F |              |     |              |     | Ada          |
| 60       |              |              |     |     | Base (56.64) | 60       |              |     |              |     | Base (60.72) |
| 40       | Chunk        | Chunk        |     |     |              | 40       | Chunk        |     | Chunk        |     |              |
|          | Ada          | Ada          |     |     |              |          | Ada          |     | Ada          |     |              |
| 20       | Base (69.75) | Base (83.13) |     |     |              | 20       | Base (69.55) |     | Base (78.59) |     |              |
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     | (a) LLaMA-3 |     | 8B Instruct |     |     |     |     | (b) Qwen-2.5 | 7B Instruct |     |     |
| --- | ----------- | --- | ----------- | --- | --- | --- | --- | ------------ | ----------- | --- | --- |
Figure 13: Question-type tags for Base task. Corresponding results for LLaMA-3.2 3B,
Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 31 of Appendix B.
19

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
80
60
40
20
erocS
1F
Basic Retrieval - AGN Manipulated Retrieval - AGN
Chunk Chunk
Ada Ada
Base (94.40) Base (89.33)
80
60
40
20
0.1 0.3 0.5 0.7 0.9
Compression ratio
erocS
1F
80
60
40
20
Basic Retrieval - AWR Manipulated Retrieval - AWR
Chunk Chunk
Ada Ada
Base (93.53) Base (91.18)
0.1 0.3 0.5 0.7 0.9
Compression ratio
(a) LLaMA-3 8B Instruct
erocS
1F
Basic Retrieval - AGN Manipulated Retrieval - AGN
Chunk Chunk
Ada Ada
Base (89.21) Base (94.06)
80
60
40
20
0.1 0.3 0.5 0.7 0.9
Compression ratio
erocS
1F
Basic Retrieval - AWR Manipulated Retrieval - AWR
Chunk Chunk
Ada Ada
Base (87.95) Base (92.80)
0.1 0.3 0.5 0.7 0.9
Compression ratio
(b) Qwen-2.5 7B Instruct
Figure 14: Knowledge manipulation question-type analysis.
80
60
40
20
erocS
1F
Basic Retrieval - AGNManipulated Retrieval - AGN Part Retrieval - AGN
Chunk
Ada Base (49.41)
Chunk Chunk
Ada Ada
Base (79.98) Base (80.80)
80
60
40
20
0.1 0.3 0.5 0.7 0.9
Compression ratio
erocS
1F
80
60
40
20
Basic Retrieval - AWRManipulated Retrieval - AWR Part Retrieval - AWR
Chunk Chunk Chunk
Ada Ada Ada
Base (80.91) Base (83.00) Base (71.66)
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio
(a) LLaMA-3 8B Instruct
erocS
1F
Basic Retrieval - AGNManipulated Retrieval - AGN Part Retrieval - AGN
Chunk
Ada Base (35.53)
Chunk Chunk
Ada Ada
Base (75.79) Base (79.30)
80
60
40
20
0.1 0.3 0.5 0.7 0.9
Compression ratio
erocS
1F
Basic Retrieval - AWRManipulated Retrieval - AWR Part Retrieval - AWR
Chunk
Ada Base (30.00)
Chunk Chunk
Ada Ada
Base (78.12) Base (80.84)
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio
(b) Qwen-2.5 7B Instruct
Figure 15: Multi entity question-type behavior shows a similar trend to Base task but with
muchsmoothercurvesinquestionagnostic. Thequestionawaresetuphasafarmorejagged
curve with distinct points of significant drop off. Corresponding results for LLaMA-3.2 3B,
Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 32 of Appendix B.
5.1 Structural Metrics for KV Compression
Compression can cause failure either by erasing necessary evidence or by leaving evidence
presentbutpoorlyused. Toseparatetheseeffects,wetrackeviction (survival)andconsensus
(coordination). LetT bethecontexttokensetandH theheadset. Fortokent,compression
level α, head h, and survived-token set t(α,h), define
(cid:40)
1 if t ∈ t(α,h), (cid:104)(cid:88) (cid:105)
S (t,α) = GlobalEvicted(t,α) = ⊮ S (t,α) = 0 .
h h
0 otherwise.
h∈H
The Eviction Rate is
1 (cid:88)
EvictionRate(α) = GlobalEvicted(t,α),
|T|
t∈T
20

|     |     | Physics |     | of KV | Compression | in LLMs |
| --- | --- | ------- | --- | ----- | ----------- | ------- |
and the task-aware Global Eviction Ratio (GER) restricts to answer-relevant tokens T ans :
1
(cid:88)
|     |     | GER(α) | =   |      | GlobalEvicted(t,α). |     |
| --- | --- | ------ | --- | ---- | ------------------- | --- |
|     |     |        |     | |T | |                     |     |
ans
t∈Tans
GER measures route deletion at the evidence level: when GER is high, the model has
no surviving access path to ground truth tokens, making hallucination structurally likely
(Figure 24). Survival alone is insufficient; however, the model must also coordinate its
remaining capacity. Let A (t) be normalized attention weight from head h at layer ℓ to
ℓ,h
| token t, with | top-attended |     | token |              |     |      |
| ------------- | ------------ | --- | ----- | ------------ | --- | ---- |
|               |              |     |       | t∗ = argmaxA |     | (t). |
|               |              |     |       | ℓ,h          | ℓ,h |      |
t
| We measure | layer-wise | head | consensus | as  |          |          |
| ---------- | ---------- | ---- | --------- | --- | -------- | -------- |
|            |            |      |           |     | (cid:12) | (cid:12) |
(cid:12){t∗ }
|     |     |     |              |     | ℓ,h | h∈H(cid:12) |
| --- | --- | --- | ------------ | --- | --- | ----------- |
|     |     |     | Consensus(ℓ) |     | =   | ,           |
|H|
where lower values indicate stronger agreement (many heads focus on the same token)
and higher values indicate diversity. Together, eviction and consensus let us distinguish
representational erasure (routes destroyed) from representational rigidity (routes present
| but insufficiently | adaptable). |     |     |     |     |     |
| ------------------ | ----------- | --- | --- | --- | --- | --- |
5.2 What does KV compression reveal about how different architectures
| allocate | computation |     | across | depth? |     |     |
| -------- | ----------- | --- | ------ | ------ | --- | --- |
AconsistentarchitecturalinversionappearsbetweentheLLaMAandQwenfamilies: LLaMA
tends to stabilize early and diversify later, whereas Qwen tends to explore early and consol-
idate late. This is visible in layer-wise consensus trends (Figure 16) and in how consensus
patterns evolve under increasing compression (Figures 17 and 18). Mechanistically, these
profiles imply different “decision depths”: in LLaMA, early-layer agreement can act like
normalization, supporting later specialization; in Qwen, deep-layer consolidation can act
like a late-stage decision cascade, concentrating routing onto a narrow token set.
This depth allocation has direct implications for compression design: policies that as-
sume a universal “pyramid” (monotone entropy decrease with depth) may transfer poorly
across families, since the fragile computation can occur at different depths. The attention
heatmaps reinforce that pruning policies perturb token routes differently at moderate com-
pression (chunk-style contiguous removal vs. Ada-style non-contiguous removal), but con-
verge to similar large-scale route destruction at extreme compression (Figures 19 and 20).
| Observation: | Compression |     | must | be architecture-aware |     |     |
| ------------ | ----------- | --- | ---- | --------------------- | --- | --- |
Figures 16–18 indicate that the layers most responsible for stabilization vs. consol-
idation differ by family, so the same “depth prior” for pruning can be safe for one
| model | and brittle | for another. |     |     |     |     |
| ----- | ----------- | ------------ | --- | --- | --- | --- |
21

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
| erocs susnesnoC | 0.75 |     |     |     |     |     | erocs susnesnoC |     |     |     |     |     |
| --------------- | ---- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- |
|                 |      |     | Ada |     |     |     |                 |     |     | Ada |     |     |
0.75
|     |     |     | Chunk |     |     |     |     |     |     | Chunk |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
0.50
0.50
0.25
0.25
0.00
0.00
|     |     | 0.25        |                   | 0.50        |     | 0.75 |     |     | 0.25         | 0.50              |          | 0.75 |
| --- | --- | ----------- | ----------------- | ----------- | --- | ---- | --- | --- | ------------ | ----------------- | -------- | ---- |
|     |     |             | Compression ratio |             |     |      |     |     |              | Compression ratio |          |      |
|     |     | (a) LLaMA-3 |                   | 8B Instruct |     |      |     |     | (b) Qwen-2.5 | 7B                | Instruct |      |
Figure 16: Consensus across layers. LLaMA exhibits early stabilization and late special-
ization; Qwen exhibits early exploration and late consolidation. Corresponding results for
LLaMA-3.2 3B, Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 33 of Appendix B.
|                      |     |     |     |       | erocs susnesnoC |     |     |     | Ada   | erocs susnesnoC |     | Ada   |
| -------------------- | --- | --- | --- | ----- | --------------- | --- | --- | --- | ----- | --------------- | --- | ----- |
| erocs susnesnoC 0.15 |     |     |     | Ada   |                 |     |     |     |       |                 |     |       |
|                      |     |     |     |       |                 | 0.4 |     |     | Chunk |                 |     | Chunk |
|                      |     |     |     | Chunk |                 |     |     |     |       | 0.8             |     |       |
0.10
|     |     |     |     |     |     | 0.2 |     |     |     | 0.7 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.05
| 0.00 |     |             |     |     |     | 0.0 |             |     |     | 0.6 |             |       |
| ---- | --- | ----------- | --- | --- | --- | --- | ----------- | --- | --- | --- | ----------- | ----- |
|      | 0   | 10          | 20  | 30  |     | 0   | 10          | 20  | 30  | 0   | 10          | 20 30 |
|      |     | Layer index |     |     |     |     | Layer index |     |     |     | Layer index |       |
(a) LLaMA-3 8B Instruct 10% (b) LLaMA-3 8B Instruct 50% (c) LLaMA-3 8B Instruct 90%
| Compression |     |     |     |     | Compression |     |     |     |     | Compression |     |     |
| ----------- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | ----------- | --- | --- |
Figure 17: LLaMA layerwise consensus under compression. Early agreement persists, with
depth-wise diversification supporting parallel feature channels. Corresponding results for
| LLaMA-3.2 |     | 3B are | shown | in  | Figure | 34 of | Appendix | B.  |     |     |     |     |
| --------- | --- | ------ | ----- | --- | ------ | ----- | -------- | --- | --- | --- | --- | --- |
5.3 Why does “safe” KV compression suddenly fail at extreme eviction?
Across models and presses, we observe a universal safety cliff near α ≈ 0.9: hallucination
rates spike once roughly 90% of KV entries are removed (Figure 22). The key transition is
not a smooth decline in representational “quality” but a sharp increase in the probability of
globalroutedeletion: answer-relevanttokensbecomesimultaneouslyevictedacrossallheads,
leaving no remaining pathway to evidence. This explains why eviction curves can remain
comparatively stable across α (Figure 21) while error rates exhibit a sharp nonlinearity
(Figure 22), and why GER correlates strongly with hallucination (Figure 24).
At the same time, some failures occur even when GER is low, pointing to rigidity: if
attention consolidates too strongly onto a narrow focal set, the model may not re-route
effectively when that set is pruned or when the remaining evidence is weakly aligned. This
22

|                 |     |     |     | Physics         | of KV | Compression |     | in LLMs |                 |     |     |     |
| --------------- | --- | --- | --- | --------------- | ----- | ----------- | --- | ------- | --------------- | --- | --- | --- |
| erocs susnesnoC |     |     |     | erocs susnesnoC |       |             |     |         |                 |     |     |     |
|                 |     |     |     | Ada             |       |             |     | Ada     | erocs susnesnoC |     |     | Ada |
0.6
|     | 0.4 |     |     | Chunk |     |     |     | Chunk | 0.90 |     |     | Chunk |
| --- | --- | --- | --- | ----- | --- | --- | --- | ----- | ---- | --- | --- | ----- |
0.4
0.85
0.2
0.2
0.80
0.0
|     | 0   | 10          | 20  |     | 0   |             | 10  | 20  |     | 0   | 10          | 20  |
| --- | --- | ----------- | --- | --- | --- | ----------- | --- | --- | --- | --- | ----------- | --- |
|     |     | Layer index |     |     |     | Layer index |     |     |     |     | Layer index |     |
(a) Qwen-2.5 7B Instruct 10% (b) Qwen-2.5 7B Instruct 50% (c) Qwen-2.5 7B Instruct 90%
| Compression |     |     |     | Compression |     |     |     |     | Compression |     |     |     |
| ----------- | --- | --- | --- | ----------- | --- | --- | --- | --- | ----------- | --- | --- | --- |
Figure 18: Qwen layerwise consensus under compression. Diversity persists deeper and
collapses late, consistent with a consolidation-heavy tail. Corresponding results for Qwen-
| 2.5 | 3B and | Qwen-2.5 | 14B         | are shown | in  | Figure | 35 of | Appendix      | B.  |     |     |     |
| --- | ------ | -------- | ----------- | --------- | --- | ------ | ----- | ------------- | --- | --- | --- | --- |
|     |        |          | Method: Ada |           |     |        |       | Method: Chunk |     |     |     |     |
0.8
03
|     |     | 52          |     |     |     |     |     |     |     |     | 0.3 |     |
| --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | xedni reyaL |     |     |     | 0.6 |     |     |     |     |     |     |
02
|     |     | 51  |     |     |     | 0.4 |     |     |     |     | 0.2 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
01
0.2
0.1
5
|     |     | 0   |                |       |         | 0.0         |     |                |     |     |      |     |
| --- | --- | --- | -------------- | ----- | ------- | ----------- | --- | -------------- | --- | --- | ---- | --- |
|     |     | 0   | 1 2            | 3 4 5 | 6 7     |             | 0   | 1 2            | 3 4 | 5 6 | 7    |     |
|     |     |     | Attention head |       |         |             |     | Attention head |     |     |      |     |
|     |     |     |                |       | (a) 10% | Compression |     |                |     |     |      |     |
|     |     |     | Method: Ada    |       |         |             |     | Method: Chunk  |     |     |      |     |
|     |     |     |                |       |         | 0.85        |     |                |     |     | 0.85 |     |
03
|     |     | 52  |     |     |     | 0.80 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
0.80
xedni reyaL
|     |     | 02  |     |     |     | 0.75 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
0.75
|     |     | 51  |     |     |     | 0.70 |     |     |     |     |      |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ---- | --- |
|     |     | 01  |     |     |     | 0.65 |     |     |     |     | 0.70 |     |
0.60
|     |     | 5   |     |     |     |     |     |     |     |     | 0.65 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- |
0.55
0
|     |     | 0 1 | 2              | 3 4 5 | 6 7 |                 | 0   | 1 2            | 3 4 | 5 6 | 7   |     |
| --- | --- | --- | -------------- | ----- | --- | --------------- | --- | -------------- | --- | --- | --- | --- |
|     |     |     | Attention head |       |     |                 |     | Attention head |     |     |     |     |
|     |     |     |                |       | (b) | 90% Compression |     |                |     |     |     |     |
Figure 19: LLaMA attention heatmaps under compression. Chunk pruning removes con-
tiguoussegments;Adapruningismoreirregular. At0.9,globalroutedestructiondominates.
Corresponding results for LLaMA-3.2 3B are shown in Figure 37 of Appendix B.
is most plausible in architectures with strong late consolidation (Figures 16 and 18), where
| token | survival | can | coexist | with under-utilization. |     |     |     |     |     |     |     |     |
| ----- | -------- | --- | ------- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
23

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
| Algorithm |     | 2   | Linear Probing |     | Under | KV Compression |     |     |     |
| --------- | --- | --- | -------------- | --- | ----- | -------------- | --- | --- | --- |
Require: Dataset D = {(x ,y )}N ; model f; compression α; press config Π; probed layers
i i i=1
|     | L; train/val |           | indices     | I ,I          |         |        |           |               |          |
| --- | ------------ | --------- | ----------- | ------------- | ------- | ------ | --------- | ------------- | -------- |
|     |              |           |             | tr va         |         |        |           |               |          |
| 1:  | for i        | = 1 to    | N do        |               |         |        |           |               |          |
|     | Run          | f on      | x with      | KVPress       | (Π,α);  | record | {h }      |               |          |
| 2:  |              |           | i           |               |         |        | i,ℓ       | ℓ∈L           |          |
| 3:  | z            | ← Pool({h | }           | )             |         |        |           |               |          |
|     | i            |           | i,ℓ         | ℓ∈L           |         |        |           |               |          |
| 4:  | end          | for       |             |               |         |        |           |               |          |
|     | Train        | linear    | g(z) =      | softmax(Wz+b) |         | on     | {(z ,y )} | with          | f frozen |
| 5:  |              |           |             |               |         |        | i i i∈Itr |               |          |
| 6:  | Evaluate     | macro-F1  |             | on {(z        | ,y )}   |        |           |               |          |
|     |              |           |             | i             | i i∈Iva |        |           |               |          |
|     |              |           | Method: Ada |               |         |        |           | Method: Chunk |          |
0.30
|     |     | 52  |     |     |     |     | 0.5 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.25
xedni reyaL 02
0.4
51 0.20
0.3
0.15
|     |     | 01  |     |     |     |     | 0.2 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.10
|     |     | 5   |     |     |     |     | 0.1 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.05
|     |     | 0   |                |     |     |     | 0.0         |                |     |
| --- | --- | --- | -------------- | --- | --- | --- | ----------- | -------------- | --- |
|     |     |     | 0              | 1 2 | 3   |     | 0           | 1              | 2 3 |
|     |     |     | Attention head |     |     |     |             | Attention head |     |
|     |     |     |                |     | (a) | 10% | Compression |                |     |
|     |     |     | Method: Ada    |     |     |     |             | Method: Chunk  |     |
0.85 0.85
52
xedni reyaL 02
0.80 0.80
51
0.75
0.75
01
0.70
|     |     | 5   |     |     |     |     | 0.70 |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
0
|     |     |     | 0              | 1 2 | 3   |     | 0           | 1              | 2 3 |
| --- | --- | --- | -------------- | --- | --- | --- | ----------- | -------------- | --- |
|     |     |     | Attention head |     |     |     |             | Attention head |     |
|     |     |     |                |     | (b) | 90% | Compression |                |     |
Figure 20: Qwen attention heatmaps under compression. Policy differences are visible at
low compression but are overwhelmed at 0.9 by large-scale pruning. Corresponding results
for Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 38 and Figure 39 of Appendix B.
|     | Observation: |     | Two mechanisms |     | explain | the | safety cliff |     |     |
| --- | ------------ | --- | -------------- | --- | ------- | --- | ------------ | --- | --- |
Figures 24 and 16 together support two failure modes: (i) erasure (high GER re-
moves all evidence routes), and (ii) rigidity (routes survive but consolidation limits
|     | re-routing), |     | both of | which manifest |     | sharply | near α | ≈ 0.9 | (Figure 22). |
| --- | ------------ | --- | ------- | -------------- | --- | ------- | ------ | ----- | ------------ |
24

|     |                   | Physics     | of KV | Compression | in LLMs           |             |      |
| --- | ----------------- | ----------- | ----- | ----------- | ----------------- | ----------- | ---- |
|     | 0.8               |             |       | 0.8         |                   |             |      |
|     |                   | Ada         |       |             | Ada               |             |      |
|     | 0.6               | Chunk       |       | 0.6         | Chunk             |             |      |
|     | REG               |             |       | REG         |                   |             |      |
|     | 0.4               |             |       | 0.4         |                   |             |      |
|     | 0.2               |             |       | 0.2         |                   |             |      |
|     | 0.25              | 0.50        | 0.75  |             | 0.25              | 0.50        | 0.75 |
|     | Compression ratio |             |       |             | Compression ratio |             |      |
|     | (a) LLaMA-3       | 8B Instruct |       |             | (b) Qwen-2.5      | 7B Instruct |      |
Figure 21: Eviction rates vs. compression. Pruning is broadly question-agnostic unless
explicitly conditioned. Corresponding results for LLaMA-3.2 3B, Qwen-2.5 3B, and Qwen-
| 2.5 14B | are shown in | Figure 42   | of Appendix | B.            |     |     |     |
| ------- | ------------ | ----------- | ----------- | ------------- | --- | --- | --- |
|         |              | Method: Ada |             | Method: Chunk |     |     |     |
0.6
0.5
etar rorrE
0.4
Error type
0.3
Hallucination
|     | 0.2 |     |     |     |     |     | Not_known |
| --- | --- | --- | --- | --- | --- | --- | --------- |
0.1
0.0
|     | 0.2 | 0.4 0.6 | 0.8 | 0.2 | 0.4 0.6 | 0.8 |     |
| --- | --- | ------- | --- | --- | ------- | --- | --- |
Compression ratio
Compression ratio
|     |     |             | (a) LLaMA-3 | 8B            | Instruct |     |     |
| --- | --- | ----------- | ----------- | ------------- | -------- | --- | --- |
|     |     | Method: Ada |             | Method: Chunk |          |     |     |
0.8
etar rorrE 0.6
Error type
0.4
Hallucination
Not_known
0.2
0.0
|     | 0.2               | 0.4 0.6 | 0.8          | 0.2               | 0.4 0.6  | 0.8 |     |
| --- | ----------------- | ------- | ------------ | ----------------- | -------- | --- | --- |
|     | Compression ratio |         |              | Compression ratio |          |     |     |
|     |                   |         | (b) Qwen-2.5 | 7B                | Instruct |     |     |
Figure 22: Error rates vs. compression. Hallucination exhibits a cliff near α ≈ 0.9, with
“unknown” behavior more erratic under AdaKV. Corresponding results for LLaMA-3.2 3B,
Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 43 of Appendix B.
5.4 What survives compression inside the model, and why does survival not
| imply | use? |     |     |     |     |     |     |
| ----- | ---- | --- | --- | --- | --- | --- | --- |
Probing mechanism. Tomeasurewhat remains linearly accessible intheresidualstream
after KV compression, we train linear probes on frozen hidden states under the same press
configuration used for generation. For each model, dataset, and compression ratio α, we
cache hidden states and train a lightweight linear classifier to predict the gold answer’s con-
25

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
| )ytilibitpecsus( ullaH  |     |     |     | )ytilibitpecsus( ullaH  |     |     |
| ----------------------- | --- | --- | --- | ----------------------- | --- | --- |
4
4
2
2
0
0
|     | 0.2 | 0.4               | 0.6         | 0.8 | 0.2 0.4           | 0.6 0.8     |
| --- | --- | ----------------- | ----------- | --- | ----------------- | ----------- |
|     |     | Compression ratio |             |     | Compression ratio |             |
|     | (a) | LLaMA-3           | 8B Instruct |     | (b) Qwen-2.5      | 7B Instruct |
Figure 23: Compression susceptibility χ = ∂H peaks sharply near α ≈ 0.9, consistent with
∂α
| a critical | transition         | in the           | error landscape. |     |                  |     |
| ---------- | ------------------ | ---------------- | ---------------- | --- | ---------------- | --- |
|            |                    |                  | AGN              |     |                  | AWR |
|            | etar noitanicullaH | Pearson r = 0.86 |                  |     | Pearson r = 0.79 |     |
|            | 0.50               | p-value = 0.001  |                  |     | p-value = 0.004  |     |
0.25
Ada Ada
0.00
Chunk Chunk
|     |     | 0.2 | 0.4 | 0.6 0.8        | 0.2      | 0.4 0.6 0.8 |
| --- | --- | --- | --- | -------------- | -------- | ----------- |
|     |     |     | GER |                |          | GER         |
|     |     |     |     | (a) LLaMA-3 8B | Instruct |             |
|     |     |     | AGN |                |          | AWR         |
etar noitanicullaH
|     |     | Pearson r = 0.93 |     |     | Pearson r = 0.78 |     |
| --- | --- | ---------------- | --- | --- | ---------------- | --- |
|     |     | p-value < 0.001  |     |     | p-value = 0.008  |     |
0.5
0.0
Ada Ada
Chunk Chunk
|     |     | 0.2 | 0.4 | 0.6 0.8         | 0.2      | 0.4 0.6 0.8 |
| --- | --- | --- | --- | --------------- | -------- | ----------- |
|     |     |     | GER |                 |          | GER         |
|     |     |     |     | (b) Qwen-2.5 7B | Instruct |             |
Figure 24: GER correlates strongly with hallucination rate, indicating that global route
deletion is a primary driver of catastrophic failure. Corresponding results for LLaMA-3.2
3B, Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 44 of Appendix B.
cepttag(e.g., Person, Location, Organization), reportingmacro-F1(Algorithm2). Probing
quantifies representational presence/accessibility rather than use: the decoder can still fail
if routing collapses (high GER) or if coordination becomes rigid, which is why high probe
scores can coexist with high hallucination near the cliff (Figures 25 and 22).
26

|     |     |     | Physics | of KV Compression | in LLMs |     |     |
| --- | --- | --- | ------- | ----------------- | ------- | --- | --- |
Compression ratio 10% Compression ratio 50% Compression ratio 90%
|     |              |     | Location |              | Location |              | Location |
| --- | ------------ | --- | -------- | ------------ | -------- | ------------ | -------- |
|     | Organization |     |          | Organization |          | Organization |          |
0.20.40.60C.8reature
|     |     |     |     |     | 0.20.40.60C.8reature |     | 0.20.40.60C.8reature |
| --- | --- | --- | --- | --- | -------------------- | --- | -------------------- |
Person
|     |     |     |     | Person |     | Person |     |
| --- | --- | --- | --- | ------ | --- | ------ | --- |
Chunk (AWR)
Thing
|     | Chunk (AGN) |     |     |             | Thing       |     | Thing |
| --- | ----------- | --- | --- | ----------- | ----------- | --- | ----- |
|     |             |     |     | (a) LLaMA-3 | 8B Instruct |     |       |
Compression ratio 10% Compression ratio 50% Compression ratio 90%
Location
|     |     |     |     |     | Location |     | Location |
| --- | --- | --- | --- | --- | -------- | --- | -------- |
Organization
|     |     |     |                      | Organization |                      | Organization |                      |
| --- | --- | --- | -------------------- | ------------ | -------------------- | ------------ | -------------------- |
|     |     |     | 0.20.40.60C.8reature |              | 0.20.40.60C.8reature |              | 0.20.40.60C.8reature |
Person
|     |     |     |     | Person |     | Person |     |
| --- | --- | --- | --- | ------ | --- | ------ | --- |
Chunk (AWR)
Thing
|     | Chunk (AGN) |     |     |              | Thing       |     | Thing |
| --- | ----------- | --- | --- | ------------ | ----------- | --- | ----- |
|     |             |     |     | (b) Qwen-2.5 | 7B Instruct |     |       |
Figure 25: Base task probing across compression. Some tags remain decodable; others
collapseearlyandmaypartiallyrecoverunderquestion-awaresetups. Correspondingresults
for LLaMA-3.2 3B, Qwen-2.5 3B, and Qwen-2.5 14B are shown in Figure 40 of Appendix B.
| Observation: |     | Retention | ̸= utilization |     |     |     |     |
| ------------ | --- | --------- | -------------- | --- | --- | --- | --- |
Probing can remain high while generation fails: concept vectors may stay decodable
(Figures25–26)evenashallucinationspikesnearthecliff(Figure22), indicatingthat
routingavailabilityandflexibility, notjustrepresentationalpresence, limitreliability.
5.5 When does question-aware compression help, and why does it help some
|     | models | more than | others? |     |     |     |     |
| --- | ------ | --------- | ------- | --- | --- | --- | --- |
Question-aware compression can be seen as injecting an early discriminative bias: pruning
retains tokens that best separate the answer entity from competitors, which is consistent
with improved probe separability in several regimes (Figures 25 and 26). Its impact is
largerwhendeeplayersamplifyearlyselectionsignals, asinlate-consolidatingarchitectures
(Figures 16 and 18). Conversely, tasks that require latent bridge tokens (e.g., multi-hop
or discrepancy detection) can remain fragile under query-centric heuristics if relevance is
not locally aligned with query overlap, suggesting that robust question-aware pruning must
| preserve | routes, | not just | query-similar | tokens. |     |     |     |
| -------- | ------- | -------- | ------------- | ------- | --- | --- | --- |
27

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
Compression ratio 10% Compression ratio 50% Compression ratio 90%
|     |              |     | Location |     |              | Location |     |              | Location |
| --- | ------------ | --- | -------- | --- | ------------ | -------- | --- | ------------ | -------- |
|     | Organization |     |          |     | Organization |          |     | Organization |          |
0.20.40.60C.8reature
|     |     |     |     |     |     |     | 0.20.40.60C.8reature |     | 0.20.40.60C.8reature |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | -------------------- |
Person
|     |     |     |     |     | Person |     |     | Person |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | ------ | --- |
Chunk (AWR)
Thing
|     | Chunk (AGN) |     |     |     |             |     | Thing    |     | Thing |
| --- | ----------- | --- | --- | --- | ----------- | --- | -------- | --- | ----- |
|     |             |     |     |     | (a) LLaMA-3 | 8B  | Instruct |     |       |
Compression ratio 10% Compression ratio 50% Compression ratio 90%
Location
|     |     |     |     |     |     | Location |     |     | Location |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | -------- |
Organization
|     |     |     |                      |     | Organization |     |                      | Organization |                      |
| --- | --- | --- | -------------------- | --- | ------------ | --- | -------------------- | ------------ | -------------------- |
|     |     |     | 0.20.40.60C.8reature |     |              |     | 0.20.40.60C.8reature |              | 0.20.40.60C.8reature |
Person
|     |     |     |     |     | Person |     |     | Person |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | ------ | --- |
Chunk (AWR)
Thing
|     | Chunk (AGN) |     |     |     |              |     | Thing    |     | Thing |
| --- | ----------- | --- | --- | --- | ------------ | --- | -------- | --- | ----- |
|     |             |     |     |     | (b) Qwen-2.5 | 7B  | Instruct |     |       |
Figure 26: Multi-Entity probing across compression. Question awareness helps selectively
rather than uniformly, suggesting interaction between representational geometry and prun-
ing alignment. Corresponding results for LLaMA-3.2 3B, Qwen-2.5 3B, and Qwen-2.5 14B
| are shown    | in  | Figure | 41 of   | Appendix | B.             |     |              |     |     |
| ------------ | --- | ------ | ------- | -------- | -------------- | --- | ------------ | --- | --- |
| Observation: |     | Query  | signals | improve  | discriminative |     | preservation |     |     |
Question-aware pruning tends to preserve tokens that maintain decision boundaries
for the correct answer, improving probe separability (Figures 25–26) and mitigating
catastrophic failure near α ≈ 0.9 (Figure 22), especially in late-consolidating models
| (Figure |     | 16). |     |     |     |     |     |     |     |
| ------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
5.6 Is KV compression best understood as gradual representational decay or
|     | as a phase | transition? |     |     |     |     |     |     |     |
| --- | ---------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
Finally, the mismatch between probing and generation trajectories suggests that KV com-
pression is not well-modeled as smooth representational decay: probe scores can drop early
(Figure 25) while generation stays stable until the cliff (Figure 22). This is more consistent
with a reachability-driven transition: performance remains robust while at least one viable
route to answer evidence survives, and collapses when routes are globally deleted (high
GER) or become too rigid to exploit (high consolidation), aligning with stable eviction
| trends | (Figure | 21) | and sharp | error | nonlinearity | (Figure | 23). |     |     |
| ------ | ------- | --- | --------- | ----- | ------------ | ------- | ---- | --- | --- |
28

|     |     |     | Physics | of KV | Compression |     | in  | LLMs |     |     |
| --- | --- | --- | ------- | ----- | ----------- | --- | --- | ---- | --- | --- |
Observation
Figures 21–22 indicate that reliability depends on whether the token-route graph
still contains viable paths to answer evidence (Figure 24) and whether routing re-
mains sufficiently flexible (Figure 16), supporting a transition-like view of extreme
KV compression.
| 6 Theoretical |           | Implications |         | of Token-Route |     |             | Sparsity |           |     |     |
| ------------- | --------- | ------------ | ------- | -------------- | --- | ----------- | -------- | --------- | --- | --- |
| 6.1 From      | Parameter |              | Lottery | Tickets        | to  | Token-Route |          | Subgraphs |     |     |
Recenttheorygivesstrongparameter-level sparsityguaranteesformulti-headself-attention.
In particular, the Strong Lottery Ticket Hypothesis (SLTH) for attention (Otsuka et al.,
2025a) shows that, when an attention module is sufficiently wide, there exist sparse param-
eter masks whoserestrictedattentionoperatorcanapproximateatargetattentionbehavior
without retraining. This is a statement about weights: a subset of parameters can imple-
ment (approximately) the same mapping as the dense module. KV cache compression is
qualitatively different. It leaves the parameters untouched but removes rows of the key–
value memory at inference time (i.e., removes tokens from the set that attention can read),
thereby changing which token-to-token interactions are even possible. This motivates a
complementary notion of sparsity defined on the token connectivity induced by attention
| during | a forward | pass. |     |     |     |     |     |     |     |     |
| ------ | --------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
Definition 1 (Token-Attention Graph). Fix an input sequence of length S and con-
sider a transformer with layers ℓ ∈ {0,...,L} and (KV) heads h ∈ {1,...,H}. Let
V = {(ℓ,i) : ℓ ∈ {0,...,L}, i ∈ {1,...,S}} denote token-nodes indexed by layer and posi-
tion. Foreachlayertransitionℓ → ℓ+1andheadh, letA ∈ RS×S bethe(row-stochastic)
ℓ,h
attention matrix used to compute the head output at layer ℓ. For a fixed threshold ε ≥ 0,
| define | directed | edges |         |               |     |         |             |     |         |     |
| ------ | -------- | ----- | ------- | ------------- | --- | ------- | ----------- | --- | ------- | --- |
|        |          |       | (cid:8) |               |     |         |             |     | (cid:9) |     |
|        |          |       | E =     | (ℓ,i) → (ℓ,j) | :   | ∃h s.t. | A ℓ,h (i,j) | >   | ε .     |     |
The resulting directed layered graph G = (V,E) summarizes which token positions at layer
ℓ can directly route information from token j into token i at the same layer.3
Definition 2 (Compressed Token-Attention Graph). Atcompressionlevelα,apress
method selects, for each head h and layer ℓ, a subset of surviving key–value positions
(α)
U ⊆ {1,...,S}. Define the compressed graph G = (V,E ) by removing all edges that
| ℓ,h           |     |        |               |           |      | α      |     | α   |       |         |
| ------------- | --- | ------ | ------------- | --------- | ---- | ------ | --- | --- | ----- | ------- |
| route through |     | pruned | KV positions: |           |      |        |     |     |       |         |
|               |     |        | (cid:8)       |           |      |        | (α) |     |       | (cid:9) |
|               | E   | =      | (ℓ,i) →       | (ℓ,j) ∈ E | : ∃h | s.t. j | ∈ U | ∧ A | (i,j) | > ε .   |
|               |     | α      |               |           |      |        | ℓ,h |     | ℓ,h   |         |
Equivalently, G is the routing graph induced by the attention operator after zeroing all
α
(α)
| columns | j ∈/ U | (and | renormalizing) | in  | each | A . |     |     |     |     |
| ------- | ------ | ---- | -------------- | --- | ---- | --- | --- | --- | --- | --- |
|         |        | ℓ,h  |                |     |      | ℓ,h |     |     |     |     |
3. Edges are drawn within each layer because attention aggregates values from source positions j into
destination positions i before the residual update. Any equivalent convention (e.g., connecting (ℓ,j) to
| (ℓ+1,i)) | yields | the | same reachability | notions | up to | relabeling. |     |     |     |     |
| -------- | ------ | --- | ----------------- | ------- | ----- | ----------- | --- | --- | --- | --- |
29

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
Definition 3 (Token-Route Lottery Ticket, TR-LT). Let q be a designated query
token position (typically the question token region) and let T ⊆ {1,...,S} be the set
ans
of answer-relevant context positions.4 A TR-LT at compression α is a subgraph H ⊆ G
α α
such that (i) there exists t ∈ T with a directed path from (ℓ ,q) to (ℓ,t) in H for some
|     |     | ans |     | q   | α   |
| --- | --- | --- | --- | --- | --- |
layers ℓ ,ℓ, and (ii) restricting attention routing to the edges of H is sufficient (in the sense
q α
of preserving the model’s correct output on that instance) to support correct generation.
Intuitively, TR-LTs are token-level sparse routing backbones that remain functional under
compression, complementing SLTH’s parameter-level sparse backbones.
6.2 Reachability, Redundancy, and When Erasure Forces Hallucination
The key structural question under KV compression is whether answer evidence remains
reachable through the compressed routing graph. Let R (q) ⊆ {1,...,S} denote the set of
α
token positions reachable from q in G (dropping layer indices for notational simplicity).
α
| Define | the reachability | event    |         |            |     |
| ------ | ---------------- | -------- | ------- | ---------- | --- |
|        |                  |          | (cid:0) | (cid:1)    |     |
|        |                  | C (q) := | T ∩R    | (q) ̸= ∅ . |     |
|        |                  | α        | ans α   |            |     |
If C α (q) fails, then no answer-relevant token is reachable via attention routing, so the model
cannot condition its final states on the answer evidence through self-attention paths.
Proposition 1 (Redundant head-wise routes yield robustness). Assume that for
each t ∈ T , there exist at least k head-disjoint directed paths from q to t in the uncom-
ans
pressed graph G.5 Suppose that, for each head, the KV token t survives (i.e., is not pruned
in that head wherever it would be used) independently with probability at least p. Then
|     |     | Pr (cid:2) t ∈ R | (q) (cid:3) ≥ 1−(1−p)k. |     |     |
| --- | --- | ---------------- | ----------------------- | --- | --- |
α
Interpretation. If answer evidence is redundantly accessible through multiple heads, the
probability that all routes are destroyed decays exponentially in the redundancy k. This
explains why moderate compression can preserve behavior: even if individual routes are
| fragile, | at least one | tends to survive. |     |     |     |
| -------- | ------------ | ----------------- | --- | --- | --- |
Proposition 2 (Erasure implies loss of contextual grounding). Assume that the
model has not already encoded the answer content into the reachable residual stream before
the KV entries corresponding to T are removed (i.e., the only way to use answer evidence
ans
|             |              | tokens).6 |                 | α⋆        |     |
| ----------- | ------------ | --------- | --------------- | --------- | --- |
| is to route | to surviving | answer    | If there exists | such that |     |
|             |              | T         | ∩R (q) =        | ∅,        |     |
ans α⋆
thennoself-attentionroutingmechanismcanconditionthemodel’shiddenstatesonanswer
α⋆.
evidence at compression Consequently, correct generation cannot be guaranteed from
4. In our experiments, T is obtained from the gold answer span / annotation used for evaluation and
ans
probing.
5. Head-disjoint means that the paths can be realized through disjoint head-specific edge sets, formalizing
| cross-head | redundancy. |     |     |     |     |
| ---------- | ----------- | --- | --- | --- | --- |
6. This assumption rules out degenerate cases where answer information is perfectly “copied” into other
surviving tokens prior to eviction; empirically, the GER–hallucination correlation (Figure 24) suggests
| such | leakage is limited | at the safety cliff. |     |     |     |
| ---- | ------------------ | -------------------- | --- | --- | --- |
30

|     |     | Physics |     | of KV | Compression |     | in LLMs |     |
| --- | --- | ------- | --- | ----- | ----------- | --- | ------- | --- |
context and the model must rely on parametric priors, making hallucination structurally
likely.
Proof sketch. Eachattentionheadoutputateverylayerisaweightedlinearcombination
of surviving value vectors. If no answer token is reachable from the query token in G α⋆ ,
then no sequence of attention aggregations can incorporate any value vector originating
from T into the query-conditioned hidden states. Under the no-leakage assumption, the
ans
□
decoder has no contextual evidence for the answer and must default to priors.
Proposition 2 makes explicit what GER diagnoses: not merely “how many” tokens
remain, but whether the routing graph still contains any path to answer evidence. This
connects directly to the empirical cliff: generation stays stable while reachability holds and
collapses when global route deletion becomes common (Figures 21, 22, 24).
| 6.3 Representational |     | Rigidity: |     | Survive-but-not-used |     |     | Failures |     |
| -------------------- | --- | --------- | --- | -------------------- | --- | --- | -------- | --- |
Reachabilityisnecessarybutnotsufficient: weobserveregimeswhereanswertokenssurvive
(low GER) yet performance deteriorates, consistent with rigidity in routing. Formally,
t⋆,
suppose that at layer ℓ many heads place their maximal attention on the same token
| leaving little | diversity | in which | tokens | are | actively | read. |     |     |
| -------------- | --------- | -------- | ------ | --- | -------- | ----- | --- | --- |
Proposition 3 (High agreement reduces re-routing capacity). Fix a layer ℓ. Let
t∗ = argmax A (t)bethetop-attendedtokenofheadhanddefinetheagreementfraction
| ℓ,h | t ℓ,h |     |     |         |            |      |                |     |
| --- | ----- | --- | --- | ------- | ---------- | ---- | -------------- | --- |
|     |       |     |     |         | 1 (cid:12) |      | (cid:12)       |     |
|     |       |     | ρ   | := m ax | (cid:12){h | : t∗ | = t} (cid:12). |     |
|     |       |     | ℓ   |         |            | ℓ,h  |                |     |
|     |       |     |     | t       | H          |      |                |     |
t⋆
If the maximizer token (achieving ρ ) is pruned in the relevant heads under compression,
ℓ
thenatleastaρ fractionofheadsmustshifttheirprimaryattentiontosecondarytokens. If
ℓ
those secondary tokens systematically exclude T , then the effective probability of routing
ans
to answer evidence at layer ℓ is reduced by a factor proportional to ρ .
ℓ
Interpretation. Whenroutingishighlyconcentrated,compressioncanremoveasmallset
of “consensus” tokens and force many heads to re-route simultaneously. If the remaining
attention mass is not diverse enough to rediscover answer evidence, the model can fail
despite token survival elsewhere. This is the structural sense in which consensus can create
representational rigidity: themodelretainsevidenceinmemory, butlacksroutingflexibility
to use it.
| 6.4 Failure | Case Analysis: |     | A   | Minimal | Decomposition |     |     |     |
| ----------- | -------------- | --- | --- | ------- | ------------- | --- | --- | --- |
We can express failure probability as a mixture of an erasure mechanism and a rigidity
mechanism. Let F denote generation failure at compression level α. Let E denote the
|     | α   |     |     |     |     |     |     | α   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
event that answer-relevant tokens are globally evicted across heads (the task instance is
“route-deleted” in the sense measured by GER). Conditioning on E gives
α
|     | Pr(F | α ) = | Pr(F | α | E α )Pr(E | α )+Pr(F |     | α | ¬E α )Pr(¬E | α ). |
| --- | ---- | ----- | ---- | ------------- | -------- | --- | --------------- | ---- |
Thefirsttermcapturesroute existence: whenE holds,contextualgroundingisunavailable,
α
so Pr(F | E ) is close to 1 in practice. The second term captures route usability: even
| α   | α   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
when answer tokens survive inprinciple, failure can occurif routing collapses ontoinflexible
31

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
patterns. In our setting, Pr(E ) is estimated by GER(α) (Figure 24), while head-level
α
consensus trends (Figure 16) provide a measurable proxy for rigidity. This decomposition
aligns with the empirical pattern that the safety cliff is driven primarily by global route
deletion at extreme compression, while intermediate degradations can reflect survive-but-
not-used effects in consolidation-heavy regimes.
6.5 Sparse Token-Routes as the Inference-Time Counterpart of SLTH
SLTH (Otsuka et al., 2025a) implies that attention contains sparse parameter subnetworks
capableofapproximatingdenseattentionbehavior. Ourempiricalresultsidentifyacomple-
mentary inference-time phenomenon: robustness under KV compression is governed by the
survivalofsparsetoken-route subnetworks(TR-LTs)withinthecompressedtoken-attention
graph. In this view, KV compression is a controlled perturbation that reveals the minimal
routingbackbonerequiredforcorrectgeneration. Extremecompressioninducesfailurewhen
(i) cross-head reachability collapses (high GER, Proposition 2) or (ii) routing becomes too
rigid to exploit surviving evidence (high agreement/low diversity, Proposition 3). Together,
these results connect theoretical sparsity guarantees for attention to a concrete mechanism
of inference-time sparsification: it is not the amount of KV memory retained that governs
reliability, but whether the compressed routing graph preserves at least one viable, usable
token-route to answer evidence.
7 Limitations and Future Work
Although our framework provides mechanistic insight into KV cache compression, sev-
eral natural extensions remain. First, our controlled synthetic datasets are intentionally
constructed to isolate routing-sensitive behaviors such as multi-hop chaining, entity disam-
biguation, and coreference consistency. While this design enables causal attribution of fail-
ure modes, it abstracts away from the full heterogeneity of natural language and large-scale
real-world corpora. Future work should investigate whether the same reachability–rigidity
decomposition persists in long-document QA, retrieval-augmented generation, code reason-
ing, and multimodal contexts. In particular, studying compression effects in systems with
external memory or tool usage may reveal additional forms of routing resilience or fragility
not captured by purely internal KV pruning.
Second, our theoretical treatment focuses on structural metrics – Global Eviction Ratio
and head-level consensus – as explanatory variables for compression-induced phase tran-
sitions. While these metrics show strong empirical alignment with performance collapse,
a more refined analysis of attention operators under structured token removal could yield
tighterguarantees. Forexample,spectralcharacterizationsofattentiongraphs,connectivity
thresholds in layered routing structures, or formal bounds on multi-head redundancy may
sharpen the theoretical link between token-route sparsity and robustness. On the modeling
side,animportantdirectionistheco-designofsparsitymechanismsandarchitecture: rather
than post-hoc pruning, training objectives could explicitly encourage redundant cross-head
routing or controlled consensus to maintain effective route capacity under compression.
Such approaches may lead to principled efficient-attention designs that preserve structural
reachability while reducing memory cost.
32

Physics of KV Compression in LLMs
8 Conclusion
In this work, we reconceptualized KV cache compression as a structural intervention on
the routing geometry of self-attention rather than a mere memory-reduction technique.
Through controlled synthetic benchmarks, layer-wise routing analysis, and formalization of
reachability and rigidity metrics, we demonstrated that compression-induced failures arise
from two distinct mechanisms: global erasure of answer-relevant tokens and collapse of
routing diversity despite token survival. The sharp performance cliff observed at extreme
compression corresponds to a structural phase transition in semantic reachability, revealing
that a sparse token-route backbone governs inference-time robustness. By connecting these
empirical findings to sparsity theory in attention, we extend the intuition of lottery tickets
from parameter subnetworks to dynamic token-route structures. Our results suggest that
future long-context and efficient-attention systems must preserve not only token represen-
tations but also minimal routing capacity across heads and layers, aligning efficiency with
structural integrity rather than local importance heuristics.
33

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
| Appendix | A. Dataset | Descriptions |     |          |          |     |
| -------- | ---------- | ------------ | --- | -------- | -------- | --- |
| Task     | Context    |              |     | Question | Response |     |
Basetask Gonzalo Batistuta, an Argentine forward, is What is Gonzalo Batis- Argentine
|     | widely regarded | as one of the | greatest football | tuta’snationality? |     |     |
| --- | --------------- | ------------- | ----------------- | ------------------ | --- | --- |
playersofalltime...
Knowledgeman. Cora Delaine was born on December 11, 1954. What is Cora Delaine’s Cora
|     | They studied | in Daegu Global | Science Univer- | firstname? |     |     |
| --- | ------------ | --------------- | --------------- | ---------- | --- | --- |
sity...
Multipresence TheAstralisSpirestandstallasoneofthemost What was the main rea- To improve television
remarkableachievementsofmodernarchitecture son for constructing As- and radio broadcasting
andengineering. Risinghighabovetheskyline tralisSpire? disrupted by urban devel-
|     | ofitsbustlingcity... |     |     |     | opment |     |
| --- | -------------------- | --- | --- | --- | ------ | --- |
Multientity HarlandKaneisoneofthemostinfluentialau- WhichnovelbyKaneisset TheShadowofthePines
|     | thors of contemporary | horror,       | suspense, and     | inahauntedhotel? |     |     |
| --- | --------------------- | ------------- | ----------------- | ---------------- | --- | --- |
|     | supernatural          | fiction. Over | a career spanning |                  |     |     |
decades,Kanehas...
Longcontext During the mid-Cretaceous period, the River- Where was Kaelin Vireo The riverine fossil station
|     | back Sailbacks | were formidable | semi-aquatic | from? | ofThaloris |     |
| --- | -------------- | --------------- | ------------ | ----- | ---------- | --- |
predators,inhabitingriversystems,floodplains,
|     | andcoastalwetlands. | Knownfortheirelongated |     |     |     |     |
| --- | ------------------- | ---------------------- | --- | --- | --- | --- |
jaws,conicalteeth,andlarge...
Coreference Julian Foster was born on September 7, 1962 Whatdoesheworkas? TourGuide
|     | in Aleppo, | Aleppo Governorate, | Syria. He | is  |     |     |
| --- | ---------- | ------------------- | --------- | --- | --- | --- |
male. HestudiedinTianjinHarborUniversity
inPodgorica,Podgorica,Montenegro...
Longbeforecolonialrecordstracedthe What was the City of A sacred city built by the
legendsofthehighMexicanplateau,the Teotilac,andwhatmadeit Itzaca, aligned with celes-
Hops
|     | CityofTeotilacrosefromvolcanicplains |     |     | distinctive? (Hop0) | tialcycles(Hop0) |     |
| --- | ------------------------------------ | --- | --- | ------------------- | ---------------- | --- |
asageometricmarveloflight,shadow, How did Teotilac’s design Its pyramids and avenues
andfaith.BuiltbytheenigmaticItzaca integrate cosmic and civic encoded solar and tempo-
|     | people,Teotilac’savenuesandpyramids |     |     | order? (Hop1) | ralorder(Hop1) |     |
| --- | ----------------------------------- | --- | --- | ------------- | -------------- | --- |
werelaidouttocapturethesolarzenith, What was the Prism of A modern optical archae-
withprecisealignmentsconnecting Yulnahproject? (Hop2) ology project at Teotilac
|     | celestialmotiontociviclife... |     |     |                       | (Hop2)         |              |
| --- | ----------------------------- | --- | --- | --------------------- | -------------- | ------------ |
|     |                               |     |     | WholedthePrismofYul-  | Led by Dr.     | Lira Montoya |
|     |                               |     |     | nahandwhatmoderntools | using spectral | drones and   |
|     |                               |     |     | wereemployed? (Hop3)  | mirrors(Hop3)  |              |
Table 3: Sample contexts and inputs for each task along with the ground truth answer.
34

|     |         | Physics |     | of KV | Compression |     | in LLMs |     |          |
| --- | ------- | ------- | --- | ----- | ----------- | --- | ------- | --- | -------- |
| Tag | Context |         |     |       | Question    |     |         |     | Response |
Person Joao Fernandes, widely considered one of What is the name of the JoaoFernandes
|     | thegreatestfootballersofalltime... |     |     |     | person | described |     | in the |     |
| --- | ---------------------------------- | --- | --- | --- | ------ | --------- | --- | ------ | --- |
passage?
Thing GonzaloBatistuta,anArgentineforward, What is Gonzalo Batis- Argentine
|     | iswidelyregardedasoneofthegreatest... |     |     |     | tuta’snationality? |     |     |     |     |
| --- | ------------------------------------- | --- | --- | --- | ------------------ | --- | --- | --- | --- |
Organization MookieBlaylock,arockbandfromNorth- What is the subject of the MookieBlaylock
|     | portformedinRiverbendin1990... |     |     |     | givenpassage? |     |     |     |     |
| --- | ------------------------------ | --- | --- | --- | ------------- | --- | --- | --- | --- |
Creature The Void Stalker is a fictional endopara- Whatkindofspeciesisthe An endoparasitoid ex-
sitoid extraterrestrial species that serves VoidStalker? traterrestrialspecies
asthemain...
Location The Stones of Pharaohs are a complex In which city are The Cairo
|             | of monumental                         | structures |     | located        | on the Stones         |           | of Pharaohs | lo-      |      |
| ----------- | ------------------------------------- | ---------- | --- | -------------- | --------------------- | --------- | ----------- | -------- | ---- |
|             | GizaPlateau...                        |            |     |                | cated?                |           |             |          |      |
| Numerals    | TheThistlewoodValeWitchTrialsrepre-   |            |     |                | How                   | many      | individuals |          | 20   |
|             | sent a chilling                       | episode    | in  | early American | were                  | convicted |             | and exe- |      |
|             | history...                            |            |     |                | cutedduringthetrials? |           |             |          |      |
| Dates/Times | GonzaloBatistuta,anArgentineforward,  |            |     |                | When                  | did       | Gonzalo     | Batis-   | 2022 |
|             | iswidelyregardedasoneofthegreatest... |            |     |                | tuta                  | win       | the world   | cham-    |      |
pionship?
Events Duringatimeofgreatperilforhispeople, How did Jabez’s mother Hismotherplacedhimina
a child named Jabez was born. To save savehimfromthedecreeof woven basket and set him
|     | himfromadecreeof... |       |     |          | death? |             |     |       | adriftontheriver |
| --- | ------------------- | ----- | --- | -------- | ------ | ----------- | --- | ----- | ---------------- |
|     |                     | Table | 4:  | Examples | of     | answer-type |     | tags. |                  |
| Tag | Context             |       |     |          |        | Question    |     |       | Response         |
Standard TheBasaltBloomisanimmenseigneous WhereistheBasaltBloom CentralIndia
|     | province,   | covering | a vast | expanse   | of cen-   | located? |     |     |     |
| --- | ----------- | -------- | ------ | --------- | --------- | -------- | --- | --- | --- |
|     | tral India. | It       | formed | through a | series of |          |     |     |     |
massivevolcaniceruptions...
Manipulated XenaBellwasbornonNovember20,1968. What is Xena Bell’s last Bell
|     | They | studied | in Shanghai | Maritime | Uni- | name? |     |     |     |
| --- | ---- | ------- | ----------- | -------- | ---- | ----- | --- | --- | --- |
versity...
Part Breezeflare is characterized by unusual Nyla Soren is recognized Community workshops,
|     | soundsduringbreathingcausedbyairflow |     |     |              |     | for leading  | what | type | of publiceducation |
| --- | ------------------------------------ | --- | --- | ------------ | --- | ------------ | ---- | ---- | ------------------ |
|     | obstructionintheairways.             |     |     | Thecondition |     | initiatives? |      |      |                    |
iscommonlyobserved...
|     |     | Table | 5:  | Examples | of  | question-type |     | tags |     |
| --- | --- | ----- | --- | -------- | --- | ------------- | --- | ---- | --- |
35

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
| Task          |     | Direction | Context                        |     |     |     | Question         |     | Response     |
| ------------- | --- | --------- | ------------------------------ | --- | --- | --- | ---------------- | --- | ------------ |
|               |     | FWD       | TheseriesknownasChronoNexus    |     |     |     | WhocreatedChrono |     | ItsukiAoyama |
| Mutlipresence |     |           | iswidelyregardedasoneofthemost |     |     |     | Nexus?           |     |              |
compellingsciencefictionnarratives
|     |     |     | inJapaneseanimation. |     |     | Createdby |     |     |     |
| --- | --- | --- | -------------------- | --- | --- | --------- | --- | --- | --- |
ItsukiAoyama...
REV Few creatures in Earth’s history Which predator had Thunderfang Preda-
|     |     |     | capture         | the imagination |           | quite like    | serrated | teeth      | as tor |
| --- | --- | --- | --------------- | --------------- | --------- | ------------- | -------- | ---------- | ------ |
|     |     |     | the Thunderfang |                 | Predator, | one           | of long  | as a human |        |
|     |     |     | the largest     | and             | most      | fearsome car- | hand?    |            |        |
|     |     |     | nivorous        | dinosaurs       |           | to have ever  |          |            |        |
lived...
FWD In the distant waters of the An- Who was the na- Vinayak Damodar
Multientity
|     |     |     | daman                         | Islands | lies    | the infamous | tionalist        | imprisoned | Savarkar |
| --- | --- | --- | ----------------------------- | ------- | ------- | ------------ | ---------------- | ---------- | -------- |
|     |     |     | Iron Shadows                  |         | Prison. | Constructed  | inIronShadowsand |            |          |
|     |     |     | bytheBritishinthelate19thcen- |         |         |              | knownasVeer?     |            |          |
tury,thisprisonbecamea...
|     |     | REV | Shinroku           | is        | a popular     | Japanese | Hana             | Tanaka       | ap- Shinroku |
| --- | --- | --- | ------------------ | --------- | ------------- | -------- | ---------------- | ------------ | ------------ |
|     |     |     | manga              | and anime | series        | known    | for pears        | as a compan- |              |
|     |     |     | its unique         | blend     | of comedy,    | action,  | ioninwhichstory? |              |              |
|     |     |     | andsciencefiction. |           | Setinanalter- |          |                  |              |              |
nateEdoperiodwhere...
|          |                       | Table 6: | Examples | of  | forward | and | reverse | questions |     |
| -------- | --------------------- | -------- | -------- | --- | ------- | --- | ------- | --------- | --- |
| Template | for question-agnostic |          | setup:   |     |         |     |         |           |     |
Read the following text and answer briefly based on it. Return only the answer. Do
| not | generate | extra. |     |     |     |     |     |     |     |
| --- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- |
The Hunters are a fictional extraterrestrial species featured in the Stalker
science fiction franchise. Known for their advanced technology, including
spectral cloaking and plasma lances, they are a nomadic warrior race that
hunts other formidable species for sport and honor. They follow a strict code
of conduct and typically target prey that poses a significant challenge. Their
unique appearance includes braid-like appendages and a distinct set of split
mandibles.
36

|          |     |                |     | Physics | of     | KV Compression | in LLMs |     |     |
| -------- | --- | -------------- | --- | ------- | ------ | -------------- | ------- | --- | --- |
| Template | for | question-aware |     |         | setup: |                |         |     |     |
Read the following text and answer briefly based on it. Return only the answer. Do
|          | not generate |         | extra. |              |           |                |     |     |     |
| -------- | ------------ | ------- | ------ | ------------ | --------- | -------------- | --- | --- | --- |
| You will | be           | given   | one    | of the       | following | questions:     |     |     |     |
| What     | is the       | subject | of     | the          | given     | passage?       |     |     |     |
| What     | kind of      | species | are    | the          | Hunters?  |                |     |     |     |
| Of which | franchise    |         | are    | the          | Hunters   | an antagonist? |     |     |     |
| What     | kind of      | race    | are    | the Hunters? |           |                |     |     |     |
| What     | kind of      | prey    | do the | Hunters      |           | target?        |     |     |     |
| What     | features     | mark    | their  | unique       |           | appearance?    |     |     |     |
The Hunters are a fictional extraterrestrial species featured in the Stalker
science fiction franchise. Known for their advanced technology, including
spectral cloaking and plasma lances, they are a nomadic warrior race that
hunts other formidable species for sport and honor. They follow a strict code
of conduct and typically target prey that poses a significant challenge. Their
unique appearance includes braid-like appendages and a distinct set of split
mandibles.
| Appendix |     | B.  | Additional |     | Results |     |     |     |     |
| -------- | --- | --- | ---------- | --- | ------- | --- | --- | --- | --- |
|          |     | AGN |            |     | AWR     |     | AGN |     | AWR |
60
60
| erocS 1F |       |     |     |     |       | erocS 1F |       |     |       |
| -------- | ----- | --- | --- | --- | ----- | -------- | ----- | --- | ----- |
| 40       |       |     |     |     |       | 40       |       |     |       |
|          | Chunk |     |     |     | Chunk |          | Chunk |     | Chunk |
| 20       | Ada   |     |     |     | Ada   |          | Ada   |     | Ada   |
20
|     | Base (70.04) |     |     |     | Base (70.06) |     | Base (66.73) |     | Base (62.29) |
| --- | ------------ | --- | --- | --- | ------------ | --- | ------------ | --- | ------------ |
0
0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9 0.10.20.30.40.50.60.70.80.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     |     | (a) LLaMA3.2 |     | 3B Instruct |     |     | (b) Qwen-2.5 | 3B  | Instruct |
| --- | --- | ------------ | --- | ----------- | --- | --- | ------------ | --- | -------- |
|     |     |              |     |             |     | AGN | AWR          |     |          |
60
erocS 1F
40
|     |     |     |     |                             | Chunk             |                             | Chunk             |     |     |
| --- | --- | --- | --- | --------------------------- | ----------------- | --------------------------- | ----------------- | --- | --- |
|     |     |     |     |                             | Ada               |                             | Ada               |     |     |
|     |     |     |     | 20                          | Base (69.69)      |                             | Base (68.06)      |     |     |
|     |     |     |     | 0.10.20.30.40.50.60.70.80.9 |                   | 0.10.20.30.40.50.60.70.80.9 |                   |     |     |
|     |     |     |     |                             | Compression ratio |                             | Compression ratio |     |     |
|     |     |     |     |                             | (c)               | Qwen-2.5 14B Instruct       |                   |     |     |
Figure 27: Base task performance across compression levels for 3B and 14B models.
In this section, we report results for LLaMA-3.2 3B, Qwen 2.5 3B, and Qwen 2.5 14B,
extending the analysis from the main text to additional model scales. Across models, the
37

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
dominant trends observed in the Base task remain consistent: behaviour over text tags,
question tags, and overall retrieval accuracy largely mirrors that of the 7B models discussed
in the main body (Figures 27, 29, 31). Notably, increasing parameter count does not sys-
tematically translate into improved robustness under compression. Initial (uncompressed)
performance is broadly comparable across scales, and performance collapse occurs at sim-
ilar compression levels, with 70–90% compression marking a consistent breakdown point
| (Figures | 27, | 28). |     |     |     |     |     |     |     |
| -------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
The primary deviation from this shared pattern arises in the Multi entity task for Qwen
2.5 (3B and 14B), where performance degrades approximately linearly with compression
rather than exhibiting a sharp cliff. This behaviour is most visible within the Person text
tag (Figure 30), where accuracy drops steadily as compression increases. The same gradual
degradation propagates to Standard retrievals in the corresponding question tags (Figure
32), suggesting that entity-specific degradation directly drives the aggregate trend. Overall,
theseresultsreinforcethemaintext’scentralclaim: compressionsensitivityismorestrongly
influenced by task structure and entity distribution than by raw model scale, with larger
| models | not inherently |     | more | resilient | to aggressive |     | compression. |     |     |
| ------ | -------------- | --- | ---- | --------- | ------------- | --- | ------------ | --- | --- |
Forward Questions - AGN Reverse Questions - AGN Forward Questions - AGN Reverse Questions - AGN
| 80       |     |     |     |     |     | 80       |     |     |     |
| -------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- |
| erocS 1F |     |     |     |     |     | erocS 1F |     |     |     |
| 60       |     |     |     |     |     | 60       |     |     |     |
40
| 40  | Chunk        |     |     | Chunk        |     |     | Chunk        |     | Chunk        |
| --- | ------------ | --- | --- | ------------ | --- | --- | ------------ | --- | ------------ |
|     | Ada          |     |     | Ada          |     |     | Ada          |     | Ada          |
| 20  |              |     |     |              |     | 20  |              |     |              |
|     | Base (77.21) |     |     | Base (77.98) |     |     | Base (77.10) |     | Base (79.76) |
Forward Questions - AWR Reverse Questions - AWR Forward Questions - AWR Reverse Questions - AWR
| 80       |     |     |     |     |     | 80          |     |     |     |
| -------- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- |
| erocS 1F |     |     |     |     |     | erocS 1F 60 |     |     |     |
60
| 40  |       |     |     |       |     | 40  |       |     |       |
| --- | ----- | --- | --- | ----- | --- | --- | ----- | --- | ----- |
|     | Chunk |     |     | Chunk |     |     | Chunk |     | Chunk |
|     | Ada   |     |     | Ada   |     | 20  | Ada   |     | Ada   |
20
|     | Base (76.47) |     |     | Base (79.77) |     |     | Base (74.73) |     | Base (79.12) |
| --- | ------------ | --- | --- | ------------ | --- | --- | ------------ | --- | ------------ |
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio
|     | (a) | LLaMA-3.2 |     | 3B Instruct             |     |                         | (b) | Qwen-2.5 | 3B Instruct |
| --- | --- | --------- | --- | ----------------------- | --- | ----------------------- | --- | -------- | ----------- |
|     |     |           |     | Forward Questions - AGN |     | Reverse Questions - AGN |     |          |             |
80
|     |     |     | erocS 1F | 60                      |     |                         |              |     |     |
| --- | --- | --- | -------- | ----------------------- | --- | ----------------------- | ------------ | --- | --- |
|     |     |     |          | 40 Chunk                |     |                         | Chunk        |     |     |
|     |     |     |          | 20 Ada                  |     |                         | Ada          |     |     |
|     |     |     |          | Base (78.91)            |     |                         | Base (81.93) |     |     |
|     |     |     |          | Forward Questions - AWR |     | Reverse Questions - AWR |              |     |     |
80
erocS 1F
60
40
|     |     |     |     | Chunk |     |     | Chunk |     |     |
| --- | --- | --- | --- | ----- | --- | --- | ----- | --- | --- |
|     |     |     |     | Ada   |     |     | Ada   |     |     |
20
|     |     |     |     | Base (80.43)      |              |         | Base (83.16)      |         |     |
| --- | --- | --- | --- | ----------------- | ------------ | ------- | ----------------- | ------- | --- |
|     |     |     |     | 0.1 0.3           | 0.5 0.7      | 0.9 0.1 | 0.3 0.5           | 0.7 0.9 |     |
|     |     |     |     | Compression ratio |              |         | Compression ratio |         |     |
|     |     |     |     |                   | (c) Qwen-2.5 | 14B     | Instruct          |         |     |
Figure 28: Multi entity forward and reverse asymmetry is reduced even when the model
| size | is changed, | showing |     | invariance | to the size | of the | model. |     |     |
| ---- | ----------- | ------- | --- | ---------- | ----------- | ------ | ------ | --- | --- |
38

|     |     | Physics | of KV Compression | in  | LLMs |     |     |
| --- | --- | ------- | ----------------- | --- | ---- | --- | --- |
Person - AGN Thing - AGN Organization - AGN Creature - AGN Location - AGN Numerals - AGN Date/Time - AGN Event - AGN
80
erocS 1F 60
40
| Chunk  | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk |
| ------ | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 20 Ada | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   |
Base (77.82) Base (68.72) Base (70.45) Base (68.17) Base (74.32) Base (74.28) Base (79.70) Base (62.36)
0
Person - AWR Thing - AWR Organization - AWR Creature - AWR Location - AWR Numerals - AWR Date/Time - AWR Event - AWR
80
erocS 1F 60
40
| Chunk  | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk |
| ------ | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 20 Ada | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   |
Base (78.12) Base (68.59) Base (77.40) Base (69.33) Base (73.86) Base (75.63) Base (76.04) Base (61.24)
0
0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9
|     |     |     | (a) LLaMA-3.2 | 3B Instruct |     |     |     |
| --- | --- | --- | ------------- | ----------- | --- | --- | --- |
Person - AGN Thing - AGN Organization - AGN Creature - AGN Location - AGN Numerals - AGN Date/Time - AGN Event - AGN
80
erocS 1F 60
40
| Chunk  | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk |
| ------ | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 20 Ada | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   |
Base (71.35) Base (65.19) Base (71.14) Base (73.89) Base (72.24) Base (74.50) Base (77.98) Base (59.29)
Person - AWR Thing - AWR Organization - AWR Creature - AWR Location - AWR Numerals - AWR Date/Time - AWR Event - AWR
80
erocS 1F 60
| 40 Chunk | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk |
| -------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| 20 Ada   | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   |
Base (58.75) Base (62.45) Base (50.42) Base (59.48) Base (68.17) Base (77.87) Base (78.35) Base (59.48)
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     |     |     | (b) Qwen-2.5 | 3B Instruct |     |     |     |
| --- | --- | --- | ------------ | ----------- | --- | --- | --- |
Person - AGN Thing - AGN Organization - AGN Creature - AGN Location - AGN Numerals - AGN Date/Time - AGN Event - AGN
80
erocS 1F 60
| 40 Chunk | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk |
| -------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Ada      | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   |
20 Base (74.87) Base (68.30) Base (75.00) Base (74.47) Base (73.50) Base (74.73) Base (78.99) Base (62.92)
Person - AWR Thing - AWR Organization - AWR Creature - AWR Location - AWR Numerals - AWR Date/Time - AWR Event - AWR
80
erocS 1F
60
| 40 Chunk | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk | Chunk |
| -------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| Ada      | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   | Ada   |
20 Base (66.19) Base (68.05) Base (56.90) Base (66.62) Base (74.79) Base (78.70) Base (79.90) Base (65.03)
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     |     |     | (c) Qwen-2.5 | 14B Instruct |     |     |     |
| --- | --- | --- | ------------ | ------------ | --- | --- | --- |
Figure 29: Answer-type results for Base task closely mirror the results from the LLaMA 3
8B and Qwen 2.5 7B models, especially in their weak points such as the Events tag.
However, the apparent linearity in the Multi entity curves captures only part of the
underlying dynamics. The consensus and layerwise consensus analyses presented in the ap-
pendix largely reinforce the cross-model similarities observed in aggregate accuracy, while
simultaneously revealing architectural differences in robustness. In particular, Qwen 2.5 3B
exhibits markedly lower consensus stability under compression, indicating greater internal
disagreement across layers as compression increases. This suggests that its degradation is
not merely gradual in terms of output accuracy but also structurally fragile at the repre-
| sentation level, | especially | when handling | diverse | entity types. |     |     |     |
| ---------------- | ---------- | ------------- | ------- | ------------- | --- | --- | --- |
By contrast, LLaMA 3.2 3B exhibits dynamics that are structurally consistent with its
8B counterpart but with heightened compression sensitivity. The degradation patterns do
not suggest a qualitatively different failure mode. Rather, they reflect the same collapse
mechanismsobservedinthelargermodel,activatedatlowercompressionthresholdsandun-
39

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
Person - AGN Thing - AGN Organization - AGN Creature - AGN Location - AGN Numerals - AGN Date/Time - AGN Event - AGN
| 100         |     |     |     |     | Chunk        | Chunk        |
| ----------- | --- | --- | --- | --- | ------------ | ------------ |
| erocS 1F 80 |     |     |     |     | Ada          | Ada          |
|             |     |     |     |     | Base (44.44) | Base (44.91) |
60
| 40 Chunk | Chunk | Chunk | Chunk | Chunk | Chunk |     |
| -------- | ----- | ----- | ----- | ----- | ----- | --- |
| Ada      | Ada   | Ada   | Ada   | Ada   | Ada   |     |
20 Base (88.90) Base (59.24) Base (84.02) Base (75.34) Base (100.00) Base (77.50)
Person - AWR Thing - AWR Organization - AWR Creature - AWR Location - AWR Numerals - AWR Date/Time - AWR Event - AWR
100
|             |     |     |     |     | Chunk        | Chunk        |
| ----------- | --- | --- | --- | --- | ------------ | ------------ |
| erocS 1F 80 |     |     |     |     | Ada          | Ada          |
|             |     |     |     |     | Base (60.00) | Base (41.91) |
60
| 40 Chunk | Chunk | Chunk | Chunk | Chunk | Chunk |     |
| -------- | ----- | ----- | ----- | ----- | ----- | --- |
| Ada      | Ada   | Ada   | Ada   | Ada   | Ada   |     |
20 Base (91.32) Base (57.51) Base (78.25) Base (70.71) Base (100.00) Base (83.88)
0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9 0.1 Compression ratio 0.3 0.5 0.7 0.9
|     |     | (a) | LLaMA-3.2 | 3B Instruct |     |     |
| --- | --- | --- | --------- | ----------- | --- | --- |
Person - AGN Thing - AGN Organization - AGN Creature - AGN Location - AGN Numerals - AGN Date/Time - AGN Event - AGN
100
|             |     |     |     |     | Chunk        | Chunk        |
| ----------- | --- | --- | --- | --- | ------------ | ------------ |
| erocS 1F 75 |     |     |     |     | Ada          | Ada          |
|             |     |     |     |     | Base (12.77) | Base (40.09) |
50
| Chunk        | Chunk        | Chunk        | Chunk        | Chunk         | Chunk        |     |
| ------------ | ------------ | ------------ | ------------ | ------------- | ------------ | --- |
| 25 Ada       | Ada          | Ada          | Ada          | Ada           | Ada          |     |
| Base (92.50) | Base (55.21) | Base (89.36) | Base (77.91) | Base (100.00) | Base (71.25) |     |
0
Person - AWR Thing - AWR Organization - AWR Creature - AWR Location - AWR Numerals - AWR Date/Time - AWR Event - AWR
| 100          |              |              |              |               | Chunk        | Chunk        |
| ------------ | ------------ | ------------ | ------------ | ------------- | ------------ | ------------ |
| erocS 1F 75  |              |              |              |               | Ada          | Ada          |
|              |              |              |              |               | Base (8.89)  | Base (30.62) |
| 50 Chunk     | Chunk        | Chunk        | Chunk        | Chunk         | Chunk        |              |
| 25 Ada       | Ada          | Ada          | Ada          | Ada           | Ada          |              |
| Base (92.31) | Base (52.92) | Base (81.26) | Base (70.95) | Base (100.00) | Base (83.88) |              |
0 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     |     | (b) | Qwen-2.5 | 3B Instruct |     |     |
| --- | --- | --- | -------- | ----------- | --- | --- |
Person - AGN Thing - AGN Organization - AGN Creature - AGN Location - AGN Numerals - AGN Date/Time - AGN Event - AGN
| 100          |              |              |              |              | Chunk        | Chunk        |
| ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ |
|              |              |              |              |              | Ada          | Ada          |
| erocS 1F 75  |              |              |              |              | Base (20.00) | Base (41.15) |
| 50 Chunk     | Chunk        | Chunk        | Chunk        | Chunk        | Chunk        |              |
| 25 Ada       | Ada          | Ada          | Ada          | Ada          | Ada          |              |
| Base (93.76) | Base (58.23) | Base (93.33) | Base (81.45) | Base (97.62) | Base (85.71) |              |
0
Person - AWR Thing - AWR Organization - AWR Creature - AWR Location - AWR Numerals - AWR Date/Time - AWR Event - AWR
| 100         |     |     |     |     | Chunk        | Chunk        |
| ----------- | --- | --- | --- | --- | ------------ | ------------ |
| erocS 1F 75 |     |     |     |     | Ada          | Ada          |
|             |     |     |     |     | Base (44.44) | Base (43.67) |
50
| Chunk        | Chunk        | Chunk        | Chunk        | Chunk        | Chunk        |     |
| ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | --- |
| 25 Ada       | Ada          | Ada          | Ada          | Ada          | Ada          |     |
| Base (94.92) | Base (60.15) | Base (93.41) | Base (80.27) | Base (97.62) | Base (84.46) |     |
0
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     |     | (c) | Qwen-2.5 | 14B Instruct |     |     |
| --- | --- | --- | -------- | ------------ | --- | --- |
Figure 30: Answer type tag behaviour in Multi entity for the 3B and 14B models shows
| similar trends | as seen in | LLaMA 3 | 8B and Qwen | 2.5 7B. |     |     |
| -------------- | ---------- | ------- | ----------- | ------- | --- | --- |
folding more abruptly. In this sense, the 3B model behaves as a scale-reduced instantiation
of the same underlying dynamics rather than an architecturally distinct system.
Importantly, the consensus and layerwise analyses clarify that these similarities extend
beyond aggregate accuracy curves. While top-line performance trends appear comparable
across scales, consensus metrics reveal differences in how instability accumulates and prop-
agates through layers under compression. Thus, the appendix results demonstrate that
compression robustness is not solely a matter of parameter count, but of how representa-
tional agreement is maintained or lost throughout the network hierarchy.
The probing radar analysis further reinforces the trends identified in the preceding
sections. Across model scales, the Creature tag remains a consistent point of weakness,
with only a small number of instances demonstrating reliable handling of this category even
in the uncompressed setting. This limitation becomes substantially more pronounced under
40

|     |     |     |     | Physics | of  | KV Compression |     | in LLMs |     |     |
| --- | --- | --- | --- | ------- | --- | -------------- | --- | ------- | --- | --- |
Basic Retrieval - AGNManipulated Retrieval - AGN Part Retrieval - AGN Basic Retrieval - AGNManipulated Retrieval - AGN Part Retrieval - AGN
|          | 80           |     |              |     |              |     | 80       |              |              | Chunk        |
| -------- | ------------ | --- | ------------ | --- | ------------ | --- | -------- | ------------ | ------------ | ------------ |
| erocS 1F |              |     |              |     |              |     | erocS 1F |              |              | Ada          |
|          | 60           |     |              |     |              |     | 60       |              |              | Base (38.12) |
|          | 40           |     |              |     |              |     | 40       |              |              |              |
|          | Chunk        |     | Chunk        |     | Chunk        |     |          | Chunk        | Chunk        |              |
|          | 20 Ada       |     | Ada          |     | Ada          |     | 20       | Ada          | Ada          |              |
|          | Base (69.94) |     | Base (83.01) |     | Base (52.10) |     |          | Base (66.67) | Base (78.13) |              |
0
Basic Retrieval - AWRManipulated Retrieval - AWR Part Retrieval - AWR Basic Retrieval - AWRManipulated Retrieval - AWR Part Retrieval - AWR
80
|          | 80             |     |              |     |     | Chunk        |             |              |              | Chunk        |
| -------- | -------------- | --- | ------------ | --- | --- | ------------ | ----------- | ------------ | ------------ | ------------ |
| erocS 1F | 60             |     |              |     |     | Ada          | erocS 1F 60 |              |              | Ada          |
|          |                |     |              |     |     | Base (50.57) |             |              |              | Base (40.64) |
|          | 40             |     |              |     |     |              | 40          |              |              |              |
|          | Chunk          |     | Chunk        |     |     |              |             | Chunk        | Chunk        |              |
|          | 20 Ada         |     | Ada          |     |     |              | 20          | Ada          | Ada          |              |
|          | 0 Base (70.09) |     | Base (70.70) |     |     |              |             | Base (62.18) | Base (77.36) |              |
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     |     | (a) LLaMA-3.2 |     | 3B Instruct                                      |     |     |     | (b) Qwen-2.5         | 3B Instruct |     |
| --- | --- | ------------- | --- | ------------------------------------------------ | --- | --- | --- | -------------------- | ----------- | --- |
|     |     |               |     | Basic Retrieval - AGNManipulated Retrieval - AGN |     |     |     | Part Retrieval - AGN |             |     |
|     |     |               |     | 80                                               |     |     |     |                      | Chunk       |     |
Ada
|     |     |     |     | erocS 1F 60                                      |         |                               |              |                               | Base (54.55) |     |
| --- | --- | --- | --- | ------------------------------------------------ | ------- | ----------------------------- | ------------ | ----------------------------- | ------------ | --- |
|     |     |     |     | 40 Chunk                                         |         | Chunk                         |              |                               |              |     |
|     |     |     |     | Ada                                              |         | Ada                           |              |                               |              |     |
|     |     |     |     | 20 Base (69.59)                                  |         | Base (84.90)                  |              |                               |              |     |
|     |     |     |     | Basic Retrieval - AWRManipulated Retrieval - AWR |         |                               |              | Part Retrieval - AWR          |              |     |
|     |     |     |     | 80                                               |         |                               |              |                               | Chunk        |     |
|     |     |     |     | erocS 1F                                         |         |                               |              |                               | Ada          |     |
|     |     |     |     | 60                                               |         |                               |              |                               | Base (64.39) |     |
|     |     |     |     | 40 Chunk                                         |         | Chunk                         |              |                               |              |     |
|     |     |     |     | 20 Ada                                           |         | Ada                           |              |                               |              |     |
|     |     |     |     | Base (67.93)                                     |         | Base (81.91)                  |              |                               |              |     |
|     |     |     |     | 0.1 Compression ratio 0.3                        | 0.5 0.7 | 0.9 0.1 Compression ratio 0.3 | 0.5 0.7 0.9  | 0.1 Compression ratio 0.3 0.5 | 0.7 0.9      |     |
|     |     |     |     |                                                  | (c)     | Qwen-2.5                      | 14B Instruct |                               |              |     |
Figure 31: Base task question-type results continue to show a similar trend with smaller
| and | larger | models, | as  | seen in | the 7B | and 8B | models. |     |     |     |
| --- | ------ | ------- | --- | ------- | ------ | ------ | ------- | --- | --- | --- |
compression. PerformanceonCreaturequeriesdegradesnotonlyathighcompressionratios
| but, | in  | several cases, |     | even under | relatively |     | mild compression. |     |     |     |
| ---- | --- | -------------- | --- | ---------- | ---------- | --- | ----------------- | --- | --- | --- |
These results suggest that the difficulty is not solely compression-induced but reflects
a baseline representational fragility for this entity type, which compression subsequently
amplifies. In other words, compression does not introduce a new failure mode for Creature
retrieval; rather, it accelerates and magnifies an existing structural weakness across models.
Eviction rates remain largely uniform across tasks and model sizes, reinforcing the task-
agnostic nature of the KV cache compression mechanism. In other words, the compression
procedure applies similar retention dynamics regardless of the downstream objective. Error
| distributions, |     | however, |     | reveal | a markedly | different | pattern. |     |     |     |
| -------------- | --- | -------- | --- | ------ | ---------- | --------- | -------- | --- | --- | --- |
Incontrasttothe7Band14Bmodels, whereerrortypesremaincomparativelybalanced
under compression, the 3B models exhibit clear dominance of specific error categories as
compression increases. This skew indicates not merely reduced accuracy, but a structured
failure mode in which certain retrieval pathways collapse preferentially. Such concentration
of error types highlights the greater fragility of smaller models: under compression, they
are less able to recover or reconstruct partially retained information, leading to systematic
| rather | than | diffuse | degradation. |     |     |     |     |     |     |     |
| ------ | ---- | ------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
41

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
Basic Retrieval - AGNManipulated Retrieval - AGN Part Retrieval - AGN Basic Retrieval - AGNManipulated Retrieval - AGN Part Retrieval - AGN
| 80           |     |              | Chunk        | 80           |     |              | Chunk        |
| ------------ | --- | ------------ | ------------ | ------------ | --- | ------------ | ------------ |
| erocS 1F 60  |     |              | Ada          | erocS 1F 60  |     |              | Ada          |
|              |     |              | Base (44.80) |              |     |              | Base (22.32) |
| 40           |     |              |              | 40           |     |              |              |
| Chunk        |     | Chunk        |              | Chunk        |     | Chunk        |              |
| 20 Ada       |     | Ada          |              | 20 Ada       |     | Ada          |              |
| Base (77.24) |     | Base (78.08) |              | Base (77.21) |     | Base (79.88) |              |
Basic Retrieval - AWRManipulated Retrieval - AWR Part Retrieval - AWR Basic Retrieval - AWRManipulated Retrieval - AWR Part Retrieval - AWR
| 80           |     |              |              | 80           |     |              |              |
| ------------ | --- | ------------ | ------------ | ------------ | --- | ------------ | ------------ |
|              |     |              | Chunk        |              |     |              | Chunk        |
| erocS 1F 60  |     |              | Ada          | erocS 1F 60  |     |              | Ada          |
|              |     |              | Base (53.03) |              |     |              | Base (39.23) |
| 40           |     |              |              | 40           |     |              |              |
| Chunk        |     | Chunk        |              | Chunk        |     | Chunk        |              |
| 20 Ada       |     | Ada          |              | 20 Ada       |     | Ada          |              |
| Base (76.56) |     | Base (79.79) |              | Base (74.81) |     | Base (79.20) |              |
0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9 0.1 0.3 0.5 0.7 0.9
Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio Compression ratio
|     | (a) LLaMA-3.2 | 3B Instruct                                      |     |     | (b) Qwen-2.5         | 3B Instruct |     |
| --- | ------------- | ------------------------------------------------ | --- | --- | -------------------- | ----------- | --- |
|     |               | Basic Retrieval - AGNManipulated Retrieval - AGN |     |     | Part Retrieval - AGN |             |     |
|     |               | 80                                               |     |     |                      | Chunk       |     |
Ada
|     |     | erocS 1F 60                                      |              |     |                      | Base (35.23) |     |
| --- | --- | ------------------------------------------------ | ------------ | --- | -------------------- | ------------ | --- |
|     |     | 40 Chunk                                         | Chunk        |     |                      |              |     |
|     |     | Ada                                              | Ada          |     |                      |              |     |
|     |     | 20 Base (78.99)                                  | Base (82.03) |     |                      |              |     |
|     |     | Basic Retrieval - AWRManipulated Retrieval - AWR |              |     | Part Retrieval - AWR |              |     |
|     |     | 80                                               |              |     |                      | Chunk        |     |
|     |     | erocS 1F 60                                      |              |     |                      | Ada          |     |
Base (38.52)
40
|     |     | Chunk                         | Chunk                             |                 |                           |         |     |
| --- | --- | ----------------------------- | --------------------------------- | --------------- | ------------------------- | ------- | --- |
|     |     | 20 Ada                        | Ada                               |                 |                           |         |     |
|     |     | Base (80.52)                  | Base (83.25)                      |                 |                           |         |     |
|     |     | 0.1 Compression ratio 0.3 0.5 | 0.7 0.9 0.1 Compression ratio 0.3 | 0.5 0.7 0.9 0.1 | Compression ratio 0.3 0.5 | 0.7 0.9 |     |
|     |     |                               | (c) Qwen-2.5                      | 14B Instruct    |                           |         |     |
Figure 32: Multi entity results for LLaMA 3.2 3B show similar jagged points in question-
aware settings, while the performance almost turns into a smooth linear pattern in Qwen
| 2.5 3B | and 14B | models. |     |     |     |     |     |
| ------ | ------- | ------- | --- | --- | --- | --- | --- |
42

Physics of KV Compression in LLMs
0.75
0.50
0.25
0.00
0.25 0.50 0.75
Compression ratio
erocs
susnesnoC
Ada
0.8
Chunk
0.6
0.4
0.2
0.25 0.50 0.75
Compression ratio
(a) LLaMA-3.2 3B Instruct
erocs
susnesnoC
Ada
Chunk
(b) Qwen-2.5 3B Instruct
0.75
0.50
0.25
0.00
0.25 0.50 0.75
Compression ratio
erocs
susnesnoC
Ada
Chunk
(c) Qwen-2.5 14B Instruct
Figure 33: Consensus scores tend to follow a similar trend with the only major changes
being Qwen 3B’s slightly more linear increase rather than the slightly parabolic increase
seen in 7B and 14B models.
0.2
0.1
0.0
0 10 20
Layer index
erocs
susnesnoC
Ada
Chunk
0.4
0.2
0 10 20
Layer index
(a)
erocs
susnesnoC
Ada
Chunk
0.8
0.7
0 10 20
Layer index
(b)
erocs
susnesnoC
Ada
Chunk
(c)
Figure 34: Layerwise consensus under compression for LLaMA 3.2 3B shows a strikingly
similar convergence very early on with depth-wise diversification.
43

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
erocs susnesnoC
| erocs susnesnoC 0.75 |     |     | Ada   |     |     |     | Ada   | erocs susnesnoC |      |     | Ada   |
| -------------------- | --- | --- | ----- | --- | --- | --- | ----- | --------------- | ---- | --- | ----- |
|                      |     |     |       |     | 0.8 |     | Chunk |                 |      |     |       |
|                      |     |     | Chunk |     |     |     |       |                 |      |     | Chunk |
| 0.50                 |     |     |       |     |     |     |       |                 | 0.95 |     |       |
0.6
0.25
0.90
| 0.00 |     |             |     |     | 0.4 |             |     |     |     |             |     |
| ---- | --- | ----------- | --- | --- | --- | ----------- | --- | --- | --- | ----------- | --- |
|      | 0   | 10 20       | 30  |     | 0   | 10 20       | 30  |     | 0   | 10 20       | 30  |
|      |     | Layer index |     |     |     | Layer index |     |     |     | Layer index |     |
(a) Qwen 2.5 3B Instruct 10% (b) Qwen 2.5 3B Instruct 50% (c) Qwen 2.5 3B Instruct 90%
| Compression |     |     |     | Compression |     |     |     | Compression |     |     |     |
| ----------- | --- | --- | --- | ----------- | --- | --- | --- | ----------- | --- | --- | --- |
0.9
| erocs susnesnoC |     |     |       | erocs susnesnoC |     |     | Ada   | erocs susnesnoC |     |     | Ada   |
| --------------- | --- | --- | ----- | --------------- | --- | --- | ----- | --------------- | --- | --- | ----- |
| 0.15            |     |     | Ada   |                 | 0.4 |     |       |                 |     |     |       |
|                 |     |     | Chunk |                 |     |     | Chunk |                 |     |     | Chunk |
0.8
0.10
|     |     |     |     |     | 0.2 |     |     |     | 0.7 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.05
0.6
| 0.00 |     |     |     |     | 0.0 |             |     |     |     |             |     |
| ---- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | ----------- | --- |
|      | 0   | 20  | 40  |     | 0   | 20          | 40  |     | 0   | 20          | 40  |
|      |     |     |     |     |     | Layer index |     |     |     | Layer index |     |
Layer index
(d) Qwen 2.5 14B Instruct 10% (e) Qwen 2.5 14B Instruct 50% (f) Qwen 2.5 14B Instruct 90%
| Compression |     |     |     | Compression |     |     |     | Compression |     |     |     |
| ----------- | --- | --- | --- | ----------- | --- | --- | --- | ----------- | --- | --- | --- |
Figure35: LayerwiseconsensusundercompressionforQwen2.53Band14B.The3Bmodel
has persistent diversity even after several layers, occasionally failing to converge, while 14B
remains stable early on but shows the same funnel-like trend upon convergence.
44

|     |             | Physics | of KV | Compression | in LLMs       |     |     |     |
| --- | ----------- | ------- | ----- | ----------- | ------------- | --- | --- | --- |
|     | Method: Ada |         |       |             | Method: Chunk |     |     |     |
| 03  |             |         |       | 0.8         |               |     |     | 0.7 |
52
0.6
xedni reyaL
0.6
02
0.5
51
|     |     |     |     | 0.4 |     |     |     | 0.4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
01
| 5   |     |     |     |     |     |     |     | 0.3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.2
0
| 0   | 1 2            | 3 4 5 | 6 7                 |     | 0 1 2          | 3 4 5 | 6 7 |     |
| --- | -------------- | ----- | ------------------- | --- | -------------- | ----- | --- | --- |
|     | Attention head |       |                     |     | Attention head |       |     |     |
|     |                |       | (a) 50% Compression |     | - LLaMA 3 8B   |       |     |     |
|     | Method: Ada    |       |                     |     | Method: Chunk  |       |     |     |
| 52  |                |       |                     | 0.8 |                |       |     |     |
0.6
| xedni reyaL 02 |     |     |     | 0.6 |     |     |     |     |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
0.5
51
0.4
| 01  |     |     |     |     |     |     |     | 0.4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.2
| 5   |     |     |     |     |     |     |     | 0.3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
0
|     | 0              | 1 2             | 3                   |           | 0              | 1 2      | 3   |     |
| --- | -------------- | --------------- | ------------------- | --------- | -------------- | -------- | --- | --- |
|     | Attention head |                 |                     |           | Attention head |          |     |     |
|     |                |                 | (b) 50% Compression |           | - Qwen 2.5 7B  |          |     |     |
|     | Figure         | 36: Compression | 50%                 | for LLaMA | 3 8B and       | Qwen 2.5 | 7B. |     |
45

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
| Method: Ada |     |     | Method: Chunk |     |     |     |
| ----------- | --- | --- | ------------- | --- | --- | --- |
0.25
| 52             |     |     | 0.4 |     |     |      |
| -------------- | --- | --- | --- | --- | --- | ---- |
| xedni reyaL 02 |     |     |     |     |     | 0.20 |
0.3
| 51  |     |     |     |     |     | 0.15 |
| --- | --- | --- | --- | --- | --- | ---- |
0.2
01
0.10
0.1
5
0.05
| 0              |       |       | 0.0             |         |     |     |
| -------------- | ----- | ----- | --------------- | ------- | --- | --- |
| 0 1            | 2 3 4 | 5 6 7 | 0 1             | 2 3 4 5 | 6 7 |     |
| Attention head |       |       | Attention head  |         |     |     |
|                |       | (a)   | 10% Compression |         |     |     |
| Method: Ada    |       |       | Method: Chunk   |         |     |     |
| 52             |       |       | 0.7             |         |     | 0.6 |
| xedni reyaL 02 |       |       | 0.6             |         |     |     |
0.5
0.5
51
|     |     |     | 0.4 |     |     | 0.4 |
| --- | --- | --- | --- | --- | --- | --- |
01
0.3
| 5   |     |     |     |     |     | 0.3 |
| --- | --- | --- | --- | --- | --- | --- |
0.2
0
| 0 1 2          | 3 4 5 | 6 7     | 0 1 2          | 3 4 5 | 6 7 |      |
| -------------- | ----- | ------- | -------------- | ----- | --- | ---- |
| Attention head |       |         | Attention head |       |     |      |
|                |       | (b) 50% | Compression    |       |     |      |
| Method: Ada    |       |         | Method: Chunk  |       |     |      |
|                |       |         | 0.85           |       |     | 0.85 |
52
0.80
xedni reyaL 02
0.80
| 51  |     |     | 0.75 |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- |
0.75
01
0.70
0.70
| 5   |     |     | 0.65 |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- |
0
| 0 1            | 2 3 4 | 5 6 7 | 0 1             | 2 3 4 | 5 6 7 |     |
| -------------- | ----- | ----- | --------------- | ----- | ----- | --- |
| Attention head |       |       | Attention head  |       |       |     |
|                |       | (c)   | 90% Compression |       |       |     |
Figure37: SimilarsmoothpruninginChunkandirregularremovalinAdaisseeninLLaMA
3.2 3B as well.
46

|     |             | Physics | of  | KV Compression | in LLMs       |     |     |
| --- | ----------- | ------- | --- | -------------- | ------------- | --- | --- |
|     | Method: Ada |         |     |                | Method: Chunk |     |     |
35
0.35
0.30
30
0.30
| xedni reyaL |     |     |     | 0.25 |     |     |     |
| ----------- | --- | --- | --- | ---- | --- | --- | --- |
25
0.25
| 20  |     |     |     | 0.20 |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- |
0.20
| 15  |     |     |     | 0.15 |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- |
0.15
0.10
10
0.10
| 5   |     |     |     | 0.05 |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- |
0.05
| 0   |                |     |     | 0.00            |                |     |     |
| --- | -------------- | --- | --- | --------------- | -------------- | --- | --- |
|     | 0              |     | 1   |                 | 0              | 1   |     |
|     | Attention head |     |     |                 | Attention head |     |     |
|     |                |     |     | (a) Compression | 10%            |     |     |
|     | Method: Ada    |     |     |                 | Method: Chunk  |     |     |
35
|     |     |     |     | 0.7 |     |     | 0.7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
30
| xedni reyaL |     |     |     | 0.6 |     |     | 0.6 |
| ----------- | --- | --- | --- | --- | --- | --- | --- |
25
| 20  |     |     |     | 0.5 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
0.5
15
0.4
| 10  |     |     |     |     |     |     | 0.4 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5   |     |     |     | 0.3 |     |     |     |
0.3
0
|     | 0              |     | 1   |                 | 0              | 1   |       |
| --- | -------------- | --- | --- | --------------- | -------------- | --- | ----- |
|     | Attention head |     |     |                 | Attention head |     |       |
|     |                |     |     | (b) Compression | 50%            |     |       |
|     | Method: Ada    |     |     |                 | Method: Chunk  |     |       |
| 35  |                |     |     | 0.850           |                |     | 0.850 |
30
|     |     |     |     | 0.825 |     |     | 0.825 |
| --- | --- | --- | --- | ----- | --- | --- | ----- |
xedni reyaL 25
|     |     |     |     | 0.800 |     |     | 0.800 |
| --- | --- | --- | --- | ----- | --- | --- | ----- |
| 20  |     |     |     | 0.775 |     |     | 0.775 |
15
|     |     |     |     | 0.750 |     |     | 0.750 |
| --- | --- | --- | --- | ----- | --- | --- | ----- |
10
|     |     |     |     | 0.725 |     |     | 0.725 |
| --- | --- | --- | --- | ----- | --- | --- | ----- |
5
|     |     |     |     | 0.700 |     |     | 0.700 |
| --- | --- | --- | --- | ----- | --- | --- | ----- |
0
|     | 0              |     | 1   |                     | 0              | 1   |     |
| --- | -------------- | --- | --- | ------------------- | -------------- | --- | --- |
|     | Attention head |     |     |                     | Attention head |     |     |
|     |                |     |     | (c) Compression 90% |                |     |     |
Figure 38: The non-contiguous nature of pruning is far less diminished in the Qwen 2.5 3B
| model due | to its use | of only | two heads | across all layers. |     |     |     |
| --------- | ---------- | ------- | --------- | ------------------ | --- | --- | --- |
47

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
| Method: Ada |     |     | Method: Chunk |     |     |     |
| ----------- | --- | --- | ------------- | --- | --- | --- |
| 54          |     |     | 0.6           |     |     | 0.4 |
04
0.5
xedni reyaL 53
0.3
03
0.4
52
0.3
| 02  |     |     |     |     |     | 0.2 |
| --- | --- | --- | --- | --- | --- | --- |
| 51  |     |     | 0.2 |     |     |     |
| 01  |     |     |     |     |     | 0.1 |
0.1
5
| 0              |       |                 | 0.0            |       |       |     |
| -------------- | ----- | --------------- | -------------- | ----- | ----- | --- |
| 0 1            | 2 3 4 | 5 6 7           | 0 1            | 2 3 4 | 5 6 7 |     |
| Attention head |       |                 | Attention head |       |       |     |
|                |       | (a) Compression | 10%            |       |       |     |
| Method: Ada    |       |                 | Method: Chunk  |       |       |     |
| 54             |       |                 | 0.8            |       |       | 0.7 |
04
| xedni reyaL 53 |     |     |     |     |     | 0.6 |
| -------------- | --- | --- | --- | --- | --- | --- |
0.6
03
0.5
52
0.4
02
0.4
51
| 01  |     |     | 0.2 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
0.3
5
| 0              |       |                 | 0.0            |       |       | 0.2  |
| -------------- | ----- | --------------- | -------------- | ----- | ----- | ---- |
| 0 1            | 2 3 4 | 5 6 7           | 0 1            | 2 3 4 | 5 6 7 |      |
| Attention head |       |                 | Attention head |       |       |      |
|                |       | (b) Compression | 50%            |       |       |      |
| Method: Ada    |       |                 | Method: Chunk  |       |       |      |
|                |       |                 | 0.85           |       |       | 0.85 |
54
04
| 53          |     |     | 0.80 |     |     |      |
| ----------- | --- | --- | ---- | --- | --- | ---- |
| xedni reyaL |     |     |      |     |     | 0.80 |
03
| 52  |     |     | 0.75 |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- |
0.75
02
| 51  |     |     | 0.70 |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- |
0.70
01
0.65
5
0
| 0 1            | 2 3 4 | 5 6 7           | 0 1            | 2 3 4 | 5 6 7 |     |
| -------------- | ----- | --------------- | -------------- | ----- | ----- | --- |
| Attention head |       |                 | Attention head |       |       |     |
|                |       | (c) Compression | 90%            |       |       |     |
Figure 39: The use of eight heads in Qwen 2.5 14B shows similar trends to the LLaMA 3
family of models, with eviction patterns being fairly similar in their nature.
48

|     | Physics | of KV Compression | in LLMs |     |     |
| --- | ------- | ----------------- | ------- | --- | --- |
Compression ratio 10% Compression ratio 50% Compression ratio 90%
|              | Location |              | Location |              | Location |
| ------------ | -------- | ------------ | -------- | ------------ | -------- |
| Organization |          | Organization |          | Organization |          |
0.20.40.60C.8reature
|     |     |     | 0.20.40.60C.8reature |     | 0.20.40.60C.8reature |
| --- | --- | --- | -------------------- | --- | -------------------- |
Person
|     |     | Person |     | Person |     |
| --- | --- | ------ | --- | ------ | --- |
Chunk (AWR)
| Chunk (AGN) | Thing |               |             |     |       |
| ----------- | ----- | ------------- | ----------- | --- | ----- |
|             |       |               | Thing       |     | Thing |
|             |       | (a) LLaMA-3.2 | 3B Instruct |     |       |
Compression ratio 10% Compression ratio 50% Compression ratio 90%
Location
|              |                      |              | Location             |              | Location             |
| ------------ | -------------------- | ------------ | -------------------- | ------------ | -------------------- |
| Organization |                      | Organization |                      | Organization |                      |
|              | 0.20.40.60C.8reature |              | 0.20.40.60C.8reature |              | 0.20.40.60C.8reature |
Person
|     |     | Person |     | Person |     |
| --- | --- | ------ | --- | ------ | --- |
Chunk (AWR)
Thing
| Chunk (AGN) |     |              | Thing       |     | Thing |
| ----------- | --- | ------------ | ----------- | --- | ----- |
|             |     | (b) Qwen-2.5 | 3B Instruct |     |       |
Compression ratio 10% Compression ratio 50% Compression ratio 90%
|              | Location |              | Location |              | Location |
| ------------ | -------- | ------------ | -------- | ------------ | -------- |
| Organization |          | Organization |          | Organization |          |
0.20.40.60C.8reature
|     |     |     | 0.20.40.60C.8reature |     | 0.20.40.60C.8reature |
| --- | --- | --- | -------------------- | --- | -------------------- |
Person
|     |     | Person |     | Person |     |
| --- | --- | ------ | --- | ------ | --- |
Chunk (AWR)
| Chunk (AGN) | Thing |              |              |     |       |
| ----------- | ----- | ------------ | ------------ | --- | ----- |
|             |       |              | Thing        |     | Thing |
|             |       | (c) Qwen-2.5 | 14B Instruct |     |       |
Figure40: Probingresultsstillshowdrasticinconsistencyascompressionastheorganization
| and creature tags | still suffer. |     |     |     |     |
| ----------------- | ------------- | --- | --- | --- | --- |
49

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
Compression ratio 10% Compression ratio 50% Compression ratio 90%
|     |              | Location |              | Location |              | Location |
| --- | ------------ | -------- | ------------ | -------- | ------------ | -------- |
|     | Organization |          | Organization |          | Organization |          |
0.20.40.60C.8reature
|     |     |     |     | 0.20.40.60C.8reature |     | 0.20.40.60C.8reature |
| --- | --- | --- | --- | -------------------- | --- | -------------------- |
Person
|     |     |     | Person |     | Person |     |
| --- | --- | --- | ------ | --- | ------ | --- |
Chunk (AWR)
| Chunk (AGN) |     | Thing |               |             |     |       |
| ----------- | --- | ----- | ------------- | ----------- | --- | ----- |
|             |     |       |               | Thing       |     | Thing |
|             |     |       | (a) LLaMA-3.2 | 3B Instruct |     |       |
Compression ratio 10% Compression ratio 50% Compression ratio 90%
Location
|     |              |                      |              | Location             |              | Location             |
| --- | ------------ | -------------------- | ------------ | -------------------- | ------------ | -------------------- |
|     | Organization |                      | Organization |                      | Organization |                      |
|     |              | 0.20.40.60C.8reature |              | 0.20.40.60C.8reature |              | 0.20.40.60C.8reature |
Person
|     |     |     | Person |     | Person |     |
| --- | --- | --- | ------ | --- | ------ | --- |
Chunk (AWR)
Thing
| Chunk (AGN) |     |     |              | Thing       |     | Thing |
| ----------- | --- | --- | ------------ | ----------- | --- | ----- |
|             |     |     | (b) Qwen-2.5 | 3B Instruct |     |       |
Compression ratio 10% Compression ratio 50% Compression ratio 90%
|     |              | Location |              | Location |              | Location |
| --- | ------------ | -------- | ------------ | -------- | ------------ | -------- |
|     | Organization |          | Organization |          | Organization |          |
0.20.40.60C.8reature
|     |     |     |     | 0.20.40.60C.8reature |     | 0.20.40.60C.8reature |
| --- | --- | --- | --- | -------------------- | --- | -------------------- |
Person
|     |     |     | Person |     | Person |     |
| --- | --- | --- | ------ | --- | ------ | --- |
Chunk (AWR)
| Chunk (AGN) |     | Thing |              |              |     |       |
| ----------- | --- | ----- | ------------ | ------------ | --- | ----- |
|             |     |       |              | Thing        |     | Thing |
|             |     |       | (c) Qwen-2.5 | 14B Instruct |     |       |
Figure41: Question-awareandagnosticcompressionstillinducefairlydifferentunderstand-
| ings despite | the different | model | sizes and architectures | involved. |     |     |
| ------------ | ------------- | ----- | ----------------------- | --------- | --- | --- |
50

|     |     | Physics | of KV Compression | in LLMs |     |     |
| --- | --- | ------- | ----------------- | ------- | --- | --- |
|     | 0.8 |         | 0.8               |         |     |     |
|     |     | Ada     |                   | Ada     |     |     |
|     |     | Chunk   |                   | Chunk   |     |     |
|     | 0.6 |         | 0.6               |         |     |     |
|     | REG |         | REG               |         |     |     |
0.4
0.4
|     | 0.2           |                   | 0.2  |                   |             |      |
| --- | ------------- | ----------------- | ---- | ----------------- | ----------- | ---- |
|     |               | 0.25 0.50         | 0.75 | 0.25              | 0.50        | 0.75 |
|     |               | Compression ratio |      | Compression ratio |             |      |
|     | (a) LLaMA-3.2 | 3B Instruct       |      | (b) Qwen-2.5      | 3B Instruct |      |
0.8
Ada
Chunk
0.6
REG
0.4
0.2
|     |     |     | 0.25 0.50 | 0.75 |     |     |
| --- | --- | --- | --------- | ---- | --- | --- |
Compression ratio
|     |     |     | (c) Qwen-2.5 14B | Instruct |     |     |
| --- | --- | --- | ---------------- | -------- | --- | --- |
Figure 42: Eviction trends still remain agnostic to downward tasks even when changes to
| the scale | of the model | are seen. |     |     |     |     |
| --------- | ------------ | --------- | --- | --- | --- | --- |
51

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
|     | Method: Ada |     | Method: Chunk |     |
| --- | ----------- | --- | ------------- | --- |
0.6
etar rorrE
0.4 Error type
Hallucination
Not_known
0.2
0.0
|     | 0.2 0.4 | 0.6 0.8 | 0.2 0.4 | 0.6 0.8 |
| --- | ------- | ------- | ------- | ------- |
Compression ratio
Compression ratio
|     |             | (a) LLaMA-3.2 | 3B Instruct   |     |
| --- | ----------- | ------------- | ------------- | --- |
|     | Method: Ada |               | Method: Chunk |     |
0.6
etar rorrE
0.4
Error type
Hallucination
0.2 Not_known
0.0
|     | 0.2 0.4           | 0.6 0.8      | 0.2 0.4           | 0.6 0.8 |
| --- | ----------------- | ------------ | ----------------- | ------- |
|     | Compression ratio |              | Compression ratio |         |
|     |                   | (b) Qwen-2.5 | 3B Instruct       |         |
|     | Method: Ada       |              | Method: Chunk     |         |
0.6
etar rorrE
0.4
Error type
Hallucination
0.2 Not_known
0.0
|     | 0.2 0.4 | 0.6 0.8 | 0.2 0.4 | 0.6 0.8 |
| --- | ------- | ------- | ------- | ------- |
Compression ratio
Compression ratio
|     |     | (c) Qwen-2.5 | 14B Instruct |     |
| --- | --- | ------------ | ------------ | --- |
Figure 43: Smaller models (increasing unknown errors in AdaKV persist fragility but retain
the similar hallucination cliff as compared to larger models (Qwen 2.5 14B). The trend of
| increased unknown | errors | in AdaKV is still | present. |     |
| ----------------- | ------ | ----------------- | -------- | --- |
52

|                                     | Physics | of KV Compression | in LLMs          |     |
| ----------------------------------- | ------- | ----------------- | ---------------- | --- |
|                                     | AGN     |                   | AWR              |     |
| etar noitanicullaH Pearson r = 0.86 |         |                   | Pearson r = 0.82 |     |
| p-value = 0.002                     |         |                   | p-value = 0.004  |     |
0.5
0.0
|                                     |         | Ada                       |                  | Ada     |
| ----------------------------------- | ------- | ------------------------- | ---------------- | ------- |
|                                     |         | Chunk                     |                  | Chunk   |
|                                     | 0.2 0.4 | 0.6 0.8                   | 0.2 0.4          | 0.6 0.8 |
|                                     | GER     |                           | GER              |         |
|                                     |         | (a) LLaMA-3.2 3B Instruct |                  |         |
|                                     | AGN     |                           | AWR              |         |
| etar noitanicullaH Pearson r = 0.95 |         |                           | Pearson r = 0.81 |         |
| 0.5 p-value < 0.001                 |         |                           | p-value = 0.005  |         |
| 0.0                                 |         | Ada                       |                  | Ada     |
|                                     |         | Chunk                     |                  | Chunk   |
| 0.2                                 | 0.4     | 0.6 0.8                   | 0.2 0.4          | 0.6 0.8 |
|                                     | GER     |                           | GER              |         |
|                                     |         | (b) Qwen-2.5 3B Instruct  |                  |         |
|                                     | AGN     |                           | AWR              |         |
| etar noitanicullaH Pearson r = 0.91 |         |                           | Pearson r = 0.83 |         |
0.5
| p-value < 0.001 |     |     | p-value = 0.003 |     |
| --------------- | --- | --- | --------------- | --- |
0.0
|     |     | Ada                       |         | Ada     |
| --- | --- | ------------------------- | ------- | ------- |
|     |     | Chunk                     |         | Chunk   |
| 0.2 | 0.4 | 0.6 0.8                   | 0.2 0.4 | 0.6 0.8 |
|     | GER |                           | GER     |         |
|     |     | (c) Qwen-2.5 14B Instruct |         |         |
Figure 44: Correlation between GER and hallucination rate for all models.
53

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
References
Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lebron,
and Sumit Sanghai. Gqa: Training generalized multi-query transformer models from
multi-head checkpoints. In Proceedings of the 2023 Conference on Empirical Methods in
Natural Language Processing, pages 4895–4901, 2023.
Zeyuan Allen-Zhu. ICML 2024 Tutorial: Physics of Language Models, July 2024. Project
page: https://physics.allen-zhu.com/.
ZeyuanAllen-ZhuandYuanzhiLi. Physicsoflanguagemodels: Part3.1, knowledgestorage
and extraction, 2024. URL https://arxiv.org/abs/2309.14316.
ZeyuanAllen-ZhuandYuanzhiLi. Physicsoflanguagemodels: Part1,learninghierarchical
language structures. Transactions on Machine Learning Research, 2025. ISSN 2835-8856.
URL https://openreview.net/forum?id=mPQKyzkA1K.
Yu Bai, Xiyuan Zou, Heyan Huang, Sanxing Chen, Marc-Antoine Rondeau, Yang Gao, and
Jackie CK Cheung. CItruS: Chunked instruction-aware state eviction for long sequence
modeling. In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, Proceed-
ings of the 2024 Conference on Empirical Methods in Natural Language Processing, pages
5908–5930, Miami, Florida, USA, November 2024. Association for Computational Lin-
guistics. doi: 10.18653/v1/2024.emnlp-main.338. URL https://aclanthology.org/
2024.emnlp-main.338/.
Yushi Bai, Xin Lv, Jiajie Zhang, Hongchang Lyu, Jiankai Tang, Zhidian Huang, Zhengxiao
Du, Xiao Liu, Aohan Zeng, Lei Hou, et al. Longbench: A bilingual, multitask benchmark
for long context understanding. arXiv preprint arXiv:2308.14508, 2023.
Iz Beltagy, Matthew E. Peters, and Arman Cohan. Longformer: The Long-Document
Transformer, December 2020. URL http://arxiv.org/abs/2004.05150. Number:
arXiv:2004.05150 arXiv:2004.05150 [cs].
Zefan Cai, Yichi Zhang, Bofei Gao, Yuliang Liu, Yucheng Li, Tianyu Liu, Keming Lu,
Wayne Xiong, Yue Dong, Junjie Hu, and Wen Xiao. PyramidKV: Dynamic KV cache
compression based on pyramidal information funneling. In Second Conference on Lan-
guage Modeling, 2025. URL https://openreview.net/forum?id=ayi7qezU87.
Vivek Chari and Benjamin Van Durme. Compactor: Calibrated query-agnostic kv cache
compression with approximate leverage scores, 2025. URL https://arxiv.org/abs/
2507.08143.
Rewon Child. Generating long sequences with sparse transformers. arXiv preprint
arXiv:1904.10509, 2019.
Krzysztof Marcin Choromanski, Valerii Likhosherstov, David Dohan, Xingyou Song, An-
dreeaGane, TamasSarlos, PeterHawkins, JaredQuincyDavis, AfrozMohiuddin, Lukasz
Kaiser, David Benjamin Belanger, Lucy J Colwell, and Adrian Weller. Rethinking at-
tention with performers. In International Conference on Learning Representations, 2021.
URL https://openreview.net/forum?id=Ua6zuk0WRH.
54

Physics of KV Compression in LLMs
Kevin Clark, Urvashi Khandelwal, Omer Levy, and Christopher D Manning. What does
bert look at? an analysis of bert’s attention. In Proceedings of the 2019 ACL Workshop
BlackboxNLP:AnalyzingandInterpretingNeuralNetworksforNLP,pages276–286,2019.
Giulio Corallo and Paolo Papotti. Finch: Prompt-guided key-value cache compression for
large language models. Transactions of the Association for Computational Linguistics,
12:1517–1532, 11 2024. ISSN 2307-387X. doi: 10.1162/tacl a 00716. URL https://doi.
org/10.1162/tacl_a_00716.
Tri Dao. Flashattention-2: Faster attention with better parallelism and work partitioning.
InTheTwelfthInternationalConferenceonLearningRepresentations,2024. URLhttps:
//openreview.net/forum?id=mZn2Xyh9Ec.
TriDao,DanielYFu,StefanoErmon,AtriRudra,andChristopherRe.Flashattention: Fast
and memory-efficient exact attention with IO-awareness. In Alice H. Oh, Alekh Agar-
wal, Danielle Belgrave, and Kyunghyun Cho, editors, Advances in Neural Information
Processing Systems, 2022. URL https://openreview.net/forum?id=H4DqfPSibmx.
Alessio Devoto, Maximilian Jeblick, and Simon J´egou. Expected attention: Kv cache
compression by estimating attention from future queries distribution, 2025. URL
https://arxiv.org/abs/2510.00636.
Nelson Elhage, Neel Nanda, Catherine Olsson, Tom Henighan, Nicholas Joseph, Ben
Mann, Amanda Askell, Yuntao Bai, Anna Chen, Tom Conerly, Nova DasSarma,
Dawn Drain, Deep Ganguli, Zac Hatfield-Dodds, Danny Hernandez, Andy Jones,
Jackson Kernion, Liane Lovitt, Kamal Ndousse, Dario Amodei, Tom Brown, Jack
Clark, Jared Kaplan, Sam McCandlish, and Chris Olah. A mathematical framework
for transformer circuits. Transformer Circuits Thread, 2021. https://transformer-
circuits.pub/2021/framework/index.html.
Ibrahim Talha Ersoy, Andr´es Fernando Cardozo Licha, and Karoline Wiesner. Phase
transitions reveal hierarchical structure in deep neural networks. arXiv preprint
arXiv:2512.11866, 2025.
Yuan Feng, Junlin Lv, Yukun Cao, Xike Xie, and S. Kevin Zhou. Ada-KV: Optimizing
KV Cache Eviction by Adaptive Budget Allocation for Efficient LLM Inference, January
2025. URL http://arxiv.org/abs/2407.11550. arXiv:2407.11550 [cs].
Jonathan Frankle and Michael Carbin. The lottery ticket hypothesis: Finding sparse,
trainable neural networks. In International Conference on Learning Representations,
2019. URL https://openreview.net/forum?id=rJl-b3RcF7.
Suyu Ge, Yunan Zhang, Liyuan Liu, Minjia Zhang, Jiawei Han, and Jianfeng Gao. Model
tells you what to discard: Adaptive KV cache compression for LLMs. In The Twelfth In-
ternational Conference on Learning Representations, 2024. URL https://openreview.
net/forum?id=uNrFpDPMyo.
AaronGrattafiori, AbhimanyuDubey,AbhinavJauhri,AbhinavPandey,AbhishekKadian,
AhmadAl-Dahle,AieshaLetman,AkhilMathur,AlanSchelten,AlexVaughan,etal. The
llama 3 herd of models. arXiv preprint arXiv:2407.21783, 2024.
55

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
AlbertGuandTriDao. Mamba: Linear-timesequencemodelingwithselectivestatespaces.
| In First | conference | on language | modeling, | 2024. |     |     |
| -------- | ---------- | ----------- | --------- | ----- | --- | --- |
Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai,
Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan
Clark, et al. Training compute-optimal large language models. In Proceedings of the 36th
International Conference on Neural Information Processing Systems, pages 30016–30030,
2022.
Coleman Hooper, Sehoon Kim, Hiva Mohammadzadeh, Michael W Mahoney, Yakun S
Shao, Kurt Keutzer, and Amir Gholami. Kvquant: Towards 10 million context length
llm inference with kv cache quantization. Advances in Neural Information Processing
| Systems, | 37:1270–1303, | 2024. |     |     |     |     |
| -------- | ------------- | ----- | --- | --- | --- | --- |
Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shantanu Acharya, Dima Rekesh, Fei Jia,
YangZhang,andBorisGinsburg. Ruler: What’stherealcontextsizeofyourlong-context
| language | models? arXiv | preprint | arXiv:2404.06654, |     | 2024. |     |
| -------- | ------------- | -------- | ----------------- | --- | ----- | --- |
ZhongzhanHuang,SenweiLiang,MingfuLiang,WeiHe,HaizhaoYang,andLiangLin. The
lottery ticket hypothesis for self-attention in convolutional neural network, 2022. URL
https://arxiv.org/abs/2207.07858.
Bowen Jin, Jinsung Yoon, Jiawei Han, and Sercan Arık. Long-context llms meet rag: Over-
coming challenges for long inputs in rag. In 13th International Conference on Learning
Representations, ICLR 2025, pages 65721–65759. International Conference on Learning
| Representations, | ICLR, | 2025. |     |     |     |     |
| ---------------- | ----- | ----- | --- | --- | --- | --- |
Hao Kang, Qingru Zhang, Souvik Kundu, Geonhwa Jeong, Zaoxing Liu, Tushar Krishna,
and Tuo Zhao. Gear: An efficient kv cache compression recipe for near-lossless generative
| inference | of llm. arXiv | preprint | arXiv:2403.05527, |     | 2024. |     |
| --------- | ------------- | -------- | ----------------- | --- | ----- | --- |
Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon
Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural
| language | models. arXiv | preprint | arXiv:2001.08361, |     | 2020. |     |
| -------- | ------------- | -------- | ----------------- | --- | ----- | --- |
Jang-Hyun Kim, Jinuk Kim, Sangwoo Kwon, Jae W. Lee, Sangdoo Yun, and Hyun Oh
Song. Kvzip: Query-agnostic kv cache compression with context reconstruction, 2025.
URL https://arxiv.org/abs/2505.23416.
Hunjae Lee. Understanding the failure modes of transformers through the lens of graph
| neural networks. | arXiv | preprint | arXiv:2512.09182, |     | 2025. |     |
| ---------------- | ----- | -------- | ----------------- | --- | ----- | --- |
Haoyang Li, Yiming Li, Anxin Tian, Tianhao Tang, Zhanchao Xu, Xuejia Chen, Nicole Hu,
Wei Dong, Qing Li, and Lei Chen. A survey on large language model acceleration based
| on kv cache | management. | arXiv | preprint | arXiv:2412.19442, |     | 2024a. |
| ----------- | ----------- | ----- | -------- | ----------------- | --- | ------ |
Yuankai Li, Jia-Chen Gu, Di Wu, Kai-Wei Chang, and Nanyun Peng. Brief: Bridging
retrieval and inference for multi-hop reasoning via compression. In Findings of the Asso-
ciation for Computational Linguistics: NAACL 2025, pages 5449–5470, 2025.
56

Physics of KV Compression in LLMs
Yuhong Li, Yingbing Huang, Bowen Yang, Bharat Venkitesh, Acyr Locatelli, Hanchen Ye,
Tianle Cai, Patrick Lewis, and Deming Chen. SnapKV: LLM Knows What You are
Looking for Before Generation, June 2024b. URL http://arxiv.org/abs/2404.14469.
arXiv:2404.14469 [cs].
GuangdaLiu,ChengweiLi,JieruZhao,ChenqiZhang,andMinyiGuo. Clusterkv: Manipu-
latingllmkvcacheinsemanticspaceforrecallablecompression. In202562ndACM/IEEE
Design Automation Conference (DAC), pages 1–7. IEEE, 2025a.
Guangda Liu, Chengwei Li, Jieru Zhao, Chenqi Zhang, and Minyi Guo. Clusterkv: Ma-
nipulating llm kv cache in semantic space for recallable compression, 2025b. URL
https://arxiv.org/abs/2412.03213.
Jiaheng Liu, Dawei Zhu, Zhiqi Bai, Yancheng He, Huanxuan Liao, Haoran Que, Zekun
Wang, Chenchen Zhang, Ge Zhang, Jiebin Zhang, et al. A comprehensive survey on long
context language modeling. arXiv preprint arXiv:2503.17407, 2025c.
Xiang Liu, Zhenheng Tang, Peijie Dong, Zeyu Li, Bo Li, Xuming Hu, and Xiaowen Chu.
Chunkkv: Semantic-preserving kv cache compression for efficient long-context llm infer-
ence. arXiv preprint arXiv:2502.00299, 2025d.
Zichang Liu, Aditya Desai, Fangshuo Liao, Weitao Wang, Victor Xie, Zhaozhuo Xu,
Anastasios Kyrillidis, and Anshumali Shrivastava. Scissorhands: Exploiting the per-
sistence of importance hypothesis for LLM KV cache compression at test time. In
Thirty-seventh Conference on Neural Information Processing Systems, 2023. URL
https://openreview.net/forum?id=JZfg6wGi6g.
Zirui Liu, Jiayi Yuan, Hongye Jin, Shaochen Zhong, Zhaozhuo Xu, Vladimir Braverman,
Beidi Chen, and Xia Hu. Kivi: A tuning-free asymmetric 2bit quantization for kv cache.
In International Conference on Machine Learning, pages 32332–32344. PMLR, 2024.
Ziyang Ma, Zuchao Li, Lefei Zhang, Gui-Song Xia, Bo Du, Liangpei Zhang, and Dacheng
Tao. Phase transitions in large language model compression. npj Artificial Intelligence,
2(1):21, 2026.
William Meng, Benjamin Lee, and Hong Wang. Understanding bottlenecks for efficiently
serving llm inference with kv offloading. arXiv preprint arXiv:2601.19910, 2025.
Niklas Muennighoff, Alexander M. Rush, Boaz Barak, Teven Le Scao, Aleksandra Pik-
tus, Nouamane Tazi, Sampo Pyysalo, Thomas Wolf, and Colin Raffel. Scaling data-
constrained language models. Journal of Machine Learning Research, 26(53):1–66, 2025.
URL http://jmlr.org/papers/v26/24-1000.html.
Catherine Olsson, Nelson Elhage, Neel Nanda, Nicholas Joseph, Nova DasSarma, Tom
Henighan, BenMann, AmandaAskell, YuntaoBai, AnnaChen, etal. In-contextlearning
and induction heads. arXiv preprint arXiv:2209.11895, 2022.
Hikari Otsuka, Daiki Chijiwa, Yasuyuki Okoshi, Daichi Fujiki, Susumu Takeuchi, and
Masato Motomura. The strong lottery ticket hypothesis for multi-head attention mech-
anisms. arXiv preprint arXiv:2511.04217, 2025a.
57

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
Hikari Otsuka, Yasuyuki Okoshi, Daichi Fujiki, Susumu Takeuchi, Masato Motomura, and
Daiki Chijiwa. On the existence of hidden subnetworks within a randomly weighted
multi-head attention mechanism. In High-dimensional Learning Dynamics 2025, 2025b.
URL https://openreview.net/forum?id=gB1LZhA8Oy.
Ziran Qin, Yuchen Cao, Mingbao Lin, Wen Hu, Shixuan Fan, Ke Cheng, Weiyao Lin, and
Jianguo Li. CAKE: Cascading and adaptive KV cache eviction with layer preferences.
In The Thirteenth International Conference on Learning Representations, 2025. URL
https://openreview.net/forum?id=EQgEMAD4kv.
Ayan Sengupta, Siddhant Chaudhary, and Tanmoy Chakraborty. Value-guided KV com-
pression for LLMs via approximated CUR decomposition. In The Thirty-ninth An-
nual Conference on Neural Information Processing Systems, 2025. URL https://
openreview.net/forum?id=klmc4fwPLd.
Noam Shazeer. Fast transformer decoding: One write-head is all you need, 2019. URL
https://arxiv.org/abs/1911.02150.
Yutao Sun, Zhenyu Li, Yike Zhang, Tengyu Pan, Bowen Dong, Yuyi Guo, and Jianyong
Wang. Efficient attention mechanisms for large language models: A survey, 2026. URL
https://arxiv.org/abs/2507.19595.
Gemini Team, Petko Georgiev, Ving Ian Lei, Ryan Burnell, Libin Bai, Anmol Gulati,
Garrett Tanzer, Damien Vincent, Zhufeng Pan, Shibo Wang, Soroosh Mariooryad, Yifan
Ding, et al. Gemini 1.5: Unlocking multimodal understanding across millions of tokens
of context, 2024. URL https://arxiv.org/abs/2403.05530.
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N.
Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention Is All You Need, December 2017.
URLhttp://arxiv.org/abs/1706.03762.Number: arXiv:1706.03762arXiv:1706.03762
[cs].
Elena Voita, Rico Sennrich, and Ivan Titov. The bottom-up evolution of representations
in the transformer: A study with machine translation and language modeling objectives.
arXiv preprint arXiv:1909.01380, 2019.
Zhongwei Wan, Xinjian Wu, Yu Zhang, Yi Xin, Chaofan Tao, Zhihong Zhu, Xin Wang, Siqi
Luo, Jing Xiong, Longyue Wang, and Mi Zhang. $\text{D} {2}\text{O}$: Dynamic
discriminative operations for efficient long-context inference of large language models.
In The Thirteenth International Conference on Learning Representations, 2025. URL
https://openreview.net/forum?id=HzBfoUdjHt.
Sinong Wang, Belinda Z Li, Madian Khabsa, Han Fang, and Hao Ma. Linformer: Self-
attention with linear complexity. arXiv preprint arXiv:2006.04768, 2020.
GuangxuanXiao,YuandongTian,BeidiChen,SongHan,andMikeLewis. EfficientStream-
ing Language Models with Attention Sinks, April 2024. URL http://arxiv.org/abs/
2309.17453. arXiv:2309.17453 [cs].
58

Physics of KV Compression in LLMs
An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan
Li,DayihengLiu,FeiHuang,HaoranWei,etal. Qwen2.5technicalreport. arXiv preprint
arXiv:2412.15115, 2024a.
An Yang, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoyan Huang, Jiandong
Jiang, Jianhong Tu, Jianwei Zhang, Jingren Zhou, Junyang Lin, Kai Dang, Kexin Yang,
Le Yu, Mei Li, Minmin Sun, Qin Zhu, Rui Men, Tao He, Weijia Xu, Wenbiao Yin,
WenyuanYu,XiafeiQiu,XingzhangRen,XinlongYang,YongLi,ZhiyingXu,andZipeng
Zhang. Qwen2.5-1m technical report, 2025. URL https://arxiv.org/abs/2501.15383.
June Yong Yang, Byeongwook Kim, Jeongin Bae, Beomseok Kwon, Gunho Park, Eunho
Yang, Se Jung Kwon, and Dongsoo Lee. No token left behind: Reliable kv cache
compression via importance-aware mixed precision quantization, 2024b. URL https:
//arxiv.org/abs/2402.18096.
Manzil Zaheer, Guru Guruganesh, Kumar Avinava Dubey, Joshua Ainslie, Chris Alberti,
Santiago Ontanon, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang, et al. Big bird:
Transformers for longer sequences. Advances in Neural Information Processing Systems,
33:17283–17297, 2020.
Minwei Zhang, Haifeng Sun, Jingyu Wang, Shaolong Li, Wanyi Ning, Qi Qi, Zirui Zhuang,
and Jianxin Liao. ClusterAttn: KV cache compression under intrinsic attention clus-
tering. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher
Pilehvar, editors, Proceedings of the 63rd Annual Meeting of the Association for Com-
putational Linguistics (Volume 1: Long Papers), pages 14451–14473, Vienna, Austria,
July 2025. Association for Computational Linguistics. ISBN 979-8-89176-251-0. doi: 10.
18653/v1/2025.acl-long.703. URL https://aclanthology.org/2025.acl-long.703/.
Xinrong Zhang, Yingfa Chen, Shengding Hu, Zihang Xu, Junhao Chen, Moo Hao, Xu Han,
ZhenThai,ShuoWang,ZhiyuanLiu,andMaosongSun.∞Bench: Extendinglongcontext
evaluation beyond 100K tokens. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar,
editors, Proceedings of the 62nd Annual Meeting of the Association for Computational
Linguistics (Volume 1: Long Papers), pages 15262–15277, Bangkok, Thailand, August
2024. Association for Computational Linguistics. URL https://aclanthology.org/
2024.acl-long.814.
Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao
Song, YuandongTian, ChristopherR´e, ClarkBarrett, ZhangyangWang, andBeidiChen.
H$ 2$O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Mod-
els, December 2023. URL http://arxiv.org/abs/2306.14048. arXiv:2306.14048 [cs].
Xiabin Zhou, Wenbin Wang, Minyan Zeng, Jiaxian Guo, Xuebo Liu, Li Shen, Min Zhang,
and Liang Ding. DynamicKV: Task-aware adaptive KV cache compression for long con-
text LLMs. In Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and
VioletPeng, editors, Findings of the Association for Computational Linguistics: EMNLP
2025, pages 8042–8057, Suzhou, China, November 2025. Association for Computational
Linguistics. ISBN 979-8-89176-335-7. doi: 10.18653/v1/2025.findings-emnlp.426. URL
https://aclanthology.org/2025.findings-emnlp.426/.
59

Samhruth Ananthanarayanan and Ayan Sengupta and Tanmoy Chakraborty
Jiaying Zhu, Dong Li, Xueyang Fu, Gege Shi, Jie Xiao, Aiping Liu, and Zheng-Jun Zha. A
lottery ticket hypothesis approach with sparse fine-tuning and mae for image forgery de-
tectionandlocalization. InProceedings of the AAAI Conference on Artificial Intelligence,
volume 39, pages 10968–10976, 2025.
60