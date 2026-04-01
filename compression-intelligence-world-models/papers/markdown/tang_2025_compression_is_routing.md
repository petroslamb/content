| Compression |           |     |     | is Routing: |             | Reconstruction |          |     | Error |        | as  | an  |
| ----------- | --------- | --- | --- | ----------- | ----------- | -------------- | -------- | --- | ----- | ------ | --- | --- |
|             | Intrinsic |     |     | Signal      | for Modular |                | Language |     |       | Models |     |     |
|             |           |     |     |             | Zhongpan    | Tang           |          |     |       |        |     |     |
tangzhongp@gmail.com
|     |     |     |     |     | December | 23, | 2025 |     |     |     |     |     |
| --- | --- | --- | --- | --- | -------- | --- | ---- | --- | --- | --- | --- | --- |
5202 ceD 22  ]GL.sc[  2v36961.2152:viXra
Abstract
CurrentLargeLanguageModels(LLMs)facethreemajorchallenges: contextlengthlim-
itations, high inference costs, and catastrophic forgetting during continual learning. While
Mixture-of-Experts(MoE)architecturesmitigatesomeoftheseconflicts,theirroutingmech-
anismstypicallyrelyonexplicitlytrainedauxiliaryclassifiers. Thisnotonlyincreasessystem
complexity but also often lacks interpretability when handling mixed-domain inputs.
Buildinguponthepremisethat“CompressionisIntelligence,”thispaperproposesanovel
|     | architectural |     | philosophy: |              |     |              |     | We trained | an  | 87M-parameter |     |     |
| --- | ------------- | --- | ----------- | ------------ | --- | ------------ | --- | ---------- | --- | ------------- | --- | --- |
|     |               |     |             | “Compression |     | is Routing.” |     |            |     |               |     |     |
end-to-end Transformer Autoencoder, achieving a 64x sequence length compression
(compressing 512 tokens into 8 latent vectors). Experimental results demonstrate that this
compressor possesses extreme domain discriminative capability: it achieves a reconstruction
accuracy of 99.47% on the in-domain (code) validation set; accuracy drops sharply to
47.76% on a semi-out-of-distribution domain (Wiki text); and further plummets to just
|     |     | on  | a fully | out-of-distribution | domain | (random | sequences). |     |     |     |     |     |
| --- | --- | --- | ------- | ------------------- | ------ | ------- | ----------- | --- | --- | --- | --- | --- |
0.57%
This extreme and systematic performance discrepancy establishes the validity of recon-
|     | struction |     | error as | an        |              | Fingerprint. |     | Based | on this, | we  | propose |     |
| --- | --------- | --- | -------- | --------- | ------------ | ------------ | --- | ----- | -------- | --- | ------- | --- |
|     |           |     |          | Intrinsic | Distribution |              |     |       |          |     |         |     |
that expert modules can be automatically scheduled using reconstruction residuals directly,
without the need for explicit gating networks. This mechanism offers excellent scalability.
Furthermore,thisarchitectureprovidesanewperspectiveon“VRAMcompression”forhan-
dlingultra-longcontexts. Thisreportaimstoverifythephysicalvalidityofthisfoundational
architecture, offering a new research perspective for the next generation of scalable modular
|     | neural | networks. |     |     |     |     |     |     |     |     |     |     |
| --- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1 Introduction
|     | We firmly |     | believe | that         |     |                  |     | is the | key principle |     | guiding | the |
| --- | --------- | --- | ------- | ------------ | --- | ---------------- | --- | ------ | ------------- | --- | ------- | --- |
|     |           |     |         | “Compression |     | is Intelligence” |     |        |               |     |         |     |
evolution of language model architectures. Recent work by Del´etang et al. (2024) [2] rigorously
demonstrated the equivalence between language modeling and lossless compression, pointing
out that predictive capability and compression efficiency are essentially two sides of the same
coin. However, while existing research strives to alleviate the long-context bottleneck through
methods like Gist Tokens [5], ICAE [3], or CompLLM [1], translating the theoretical limits of
information theory into a deployable, high-density architectural paradigm remains challenging.
Existing compression pathways generally suffer from significant limitations. First is
sub-
optimal representation learning: for instance, ICAE employs a frozen decoder strategy,
forcing the encoder to unilaterally adapt to the original semantic space. This lack of end-to-end
synergy limits the compression ratio (only about 4x) and hinders the establishment of efficient
communication protocols. Second is inference feasibility: while Kuratov et al. (2025) [4]
demonstrated a theoretical limit where a single vector can carry 1568 tokens, their approach
relies on expensive Per-sample Optimization, lacking a generalized encoder, and the latent space
1

isscattered, unsupportedfordownstreamsemanticoperations. Finally, therearephysical
bot-
tlenecks of modalities: the optical compression path attempted by DeepSeek-OCR [6], while
innovative, is limited by image resolution and introduces cross-modal rendering overheads.
Meanwhile, at the macro-architectural level, as model scales grow, “Monolithic Generalist”
architectures are facing the dilemma of diminishing marginal returns due to parameter interfer-
ence and high continuous training costs. Modular design is an inevitable trend, but traditional
Mixture-of-Experts (MoE) models rely on explicitly trained gating networks, which increase
| system |     | complexity | and | lack interpretability |     | in  | their decision | logic. |     |     |
| ------ | --- | ---------- | --- | --------------------- | --- | --- | -------------- | ------ | --- | --- |
Addressing these limitations, this paper proposes a new architectural paradigm: “Com-
pression is Routing.” We constructed an end-to-end Transformer Autoencoder. By jointly
training the encoder and decoder, we established a generalizable, highly efficient compression
protocol,achieving64xefficientcompressionintheLatent Spaceratherthanbit-streamspace.
More importantly, experiments show that this end-to-end learning forces data to form clear
|          |     |            |     | in the | latent space. | Based | on this, | we propose | the core hypothesis: |     |
| -------- | --- | ---------- | --- | ------ | ------------- | ----- | -------- | ---------- | -------------------- | --- |
| Manifold |     | Separation |     |        |               |       |          |            |                      | The |
reconstruction quality (Reconstruction Loss) of a compressor dedicated to a specific
domain can serve directly as a routing signal. This discovery not only significantly
alleviatesVRAMbottlenecksinultra-longcontextscenariosbutalsoprovidesanewinformation-
theoretic perspective for building modular neural network systems that do not require explicit
gating parameters. By explicitly modeling reconstruction residuals as a measure of information
deficiency,dynamicschedulingofexpertmodulesisachieved. Thus,themodelparadigmexpands
| from | “Compression |     |     | is Prediction” | to “Compression |     | is Routing.” |     |     |     |
| ---- | ------------ | --- | --- | -------------- | --------------- | --- | ------------ | --- | --- | --- |
2 Methodology
| 2.1 | End-to-End |     |     | Language | Autoencoder |     | Architecture |     |     |     |
| --- | ---------- | --- | --- | -------- | ----------- | --- | ------------ | --- | --- | --- |
WeadoptanasymmetricTransformer-basedautoencoderarchitecture. Theinformationflow
| is  | defined | as: |     |     |         |       |         |           |     |     |
| --- | ------- | --- | --- | --- | ------- | ----- | ------- | --------- | --- | --- |
|     |         |     |     | x → | Encoder | → z → | [z,m] → | Decoder → | xˆ  | (1) |
Where:
• (Encoder): Receives a token sequence of length = 512 and dimension
|     | Compressor |     |     |     |     |     |     | x   | L   |     |
| --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
d = 512. Through attention mechanisms, it maps this to a latent vector sequence z
model
of length M = 8. This achieves a 64:1 sequence length compression ratio.
• (Decoder): Conditioned on and an auxiliary signal m, it reconstructs
|     | Reconstructor |     |     |     |     |     | z   |     |     |     |
| --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
theoriginalsequencexˆ. ThelossfunctionusesthestandardCross-EntropyLossbetween
the predicted Logits (vocabulary probability distribution) and the true labels x.
| 2.2 | Physical |     | Isolation | and | Information |     | Bottleneck |     |     |     |
| --- | -------- | --- | --------- | --- | ----------- | --- | ---------- | --- | --- | --- |
To achieve “pure” compression and prevent the model from learning identity mappings via
| shortcuts, |     | we  | implemented | strict |     | isolation: |     |     |     |     |
| ---------- | --- | --- | ----------- | ------ | --- | ---------- | --- | --- | --- | --- |
physical
1. Input Isolation: Theauxiliarysignalmhasthesamelengthasxbutcontainsnocontent
|     | information |     | associated | with | x.  |     |     |     |     |     |
| --- | ----------- | --- | ---------- | ---- | --- | --- | --- | --- | --- | --- |
2. Information Path: The decoder is blocked from accessing the original input x and can
only acquire semantic information through the highly compressed z vectors. This isolation
ensures that becomes the sole information bottleneck, forcing the encoder to learn the
z
projection of the data manifold rather than simple signal transmission.
2

| 3 Experiments    |     | and   | Analysis |     |     |     |     |     |     |
| ---------------- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- |
| 3.1 Experimental |     | Setup |          |     |     |     |     |     |     |
We used the GPT-2 Tokenizer and validated our approach on an model.
87M parameter
Themodelwaspre-trainedonacodedataset(codeparrot/codeparrot-clean). Theevaluation
| benchmarks | include | three gradients |     | of distribution: |     |     |     |     |     |
| ---------- | ------- | --------------- | --- | ---------------- | --- | --- | --- | --- | --- |
1. (ID):Thecoderepositorywassplitintotrainingandvalidationsets. Testing
In-Domain
| was | performed | on the | validation | set after | training. |     |     |     |     |
| --- | --------- | ------ | ---------- | --------- | --------- | --- | --- | --- | --- |
2. Semi-OOD: (Natural Language), using its validation set for
Salesforce/wikitext-103
testing.
| 3. Full-OOD:   |     | High-entropy | random | token | sequences. |     |     |     |     |
| -------------- | --- | ------------ | ------ | ----- | ---------- | --- | --- | --- | --- |
| 3.2 Evaluation |     | Metrics      |        |       |            |     |     |     |     |
Toquantifytheinformationfidelityoftheautoencoderduringcompression,wedefineToken-
(TRA).
| level Reconstruction |     | Accuracy |     |     |     |     |     |     |     |
| -------------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
Given an original input sequence x = {x ,x ,...,x } of length L and the model’s recon-
|     |     |     |     |     | 1 2 | L   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
structed output sequence xˆ = {xˆ ,xˆ ,...,xˆ }, TRA is defined as the proportion of tokens that
|          |               |            | 1   | 2   | L   |     |     |     |     |
| -------- | ------------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
| match at | corresponding | positions: |     |     |     |     |     |     |     |
L
|     |     |     |           |     | 1 XI(x |      |     |     |     |
| --- | --- | --- | --------- | --- | ------ | ---- | --- | --- | --- |
|     |     |     | TRA(x,xˆ) |     | =      | = xˆ | )   |     | (2) |
t t
L
t=1
whereI(·)istheindicatorfunction,takingthevalue1whentheconditionistrue,and0otherwise.
Example: Supposetheinputsequenceis[1,2,3,4,5]andthereconstructedsequenceis[1,2,6,7,5].
The tokens at positions 1, 2, and 5 are predicted correctly (3 total), while positions 3 and 4
are incorrect. The reconstruction accuracy for this sample is 3/5 = 60%. This metric strictly
measuresthemodel’sprecisioninpreservingsequencestructureandspecificcontent,ratherthan
| vague semantic | similarity. |     |     |     |     |     |     |     |     |
| -------------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
3.3 Core Finding: The Three-Step Decay of Reconstruction Accuracy
| The experimental |     | results | are shown | in  | Table 1. |     |     |     |     |
| ---------------- | --- | ------- | --------- | --- | -------- | --- | --- | --- | --- |
Table 1: Comparison of Reconstruction Accuracy Across Different Data Distributions
Data Distribution Validation Tokens Reconstruction Accuracy Routing Signal Meaning
| In-Domain(Code) |     | 3,170,816 |     |     | 99.47% |     | StrongPositive(Perfect | Fit) |     |
| --------------- | --- | --------- | --- | --- | ------ | --- | ---------------------- | ---- | --- |
Semi-OOD(Wiki) 320,512 47.76% ModerateNegative (StructuralBias)
Full-OOD(Random) 3,170,816 0.57% Extreme Negative(TotalRejection)
| 3.4 Geometric |     | Verification |     | and Mechanism |     | Explanation |     |     |     |
| ------------- | --- | ------------ | --- | ------------- | --- | ----------- | --- | --- | --- |
• High Precision ID Reconstruction (99.47%): Provesthatz possessesextremelyhigh
channel capacity, capable of perfectly carrying the structure of the code manifold with 64x
compression.
• Moderate OOD Decay (47.76%): This figure is not a random guess (which would be
approx. 1/|V| 0.002%). It reflects that the model utilized the and
|     |     | ≈   |     |     |     |     | shared vocabulary |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- |
fundamental statistical features between code and natural language. This represents
3

theoverlappingregionbetweenmanifoldsandistheidealsignaltotriggeranIncremental
Expert.
|     | •         |     |       |           |     | (0.57%): |     | Proves | the | model | did not | degenerate |
| --- | --------- | --- | ----- | --------- | --- | -------- | --- | ------ | --- | ----- | ------- | ---------- |
|     | Extremely | Low | F-OOD | Rejection |     |          |     |        |     |       |         |            |
into a signal transmission line; it possesses strong rejection capabilities against noise that
|     | does not  | conform                            | to the   | training | distribution.    |       |     |     |                                   |     |     |                  |
| --- | --------- | ---------------------------------- | -------- | -------- | ---------------- | ----- | --- | --- | --------------------------------- | --- | --- | ---------------- |
| 3.5 | Geometric |                                    | Topology | of       | Latent           | Space |     |     |                                   |     |     |                  |
|     |           | Latent Space Visualization (t-SNE) |          |          |                  |       |     |     | Latent Space Visualization (UMAP) |     |     |                  |
|     |           |                                    |          |          | Wiki (OOD)       |       |     |     |                                   |     |     | Wiki (OOD)       |
|     |           |                                    |          |          | Code (In-Domain) |       |     |     |                                   |     |     | Code (In-Domain) |
10
0
5
2 miD PAMU 10
2 miD
0
20
5
30
10
|     | 40 30 | 20  | 10 0  | 10 20 | 30  | 40  |     | 10  | 15  | 20         | 25  | 30 35 |
| --- | ----- | --- | ----- | ----- | --- | --- | --- | --- | --- | ---------- | --- | ----- |
|     |       |     | Dim 1 |       |     |     |     |     |     | UMAP Dim 1 |     |       |
(a) t-SNE Latent Space Visualization (b) UMAP Latent Space Visualization
| Figure | 1:            |     |     |          |     |          |     |        | Space. | Red | points | represent |
| ------ | ------------- | --- | --- | -------- | --- | -------- | --- | ------ | ------ | --- | ------ | --------- |
|        | Visualization |     | of  | Manifold |     | Geometry | in  | Latent |        |     |        |           |
In-Domain data (Code), and blue points represent Out-of-Domain data (Wiki). Left: t-SNE
shows local clustering characteristics. Right: UMAP shows global topological isolation. The
two classes of data exhibit complete linear separability in the latent space.
To investigate the physical mechanisms behind the reconstruction error differences, we uti-
lized t-SNE, UMAP, and PCA techniques to visualize and analyze the dimensionality of the
latent vectors generated by the encoder. Figures 1 and 2 reveal three key geometric proper-
z
ties:
| 3.5.1 | Global | Orthogonality |     | of  | Manifolds |     |     |     |     |     |     |     |
| ----- | ------ | ------------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
TheUMAPvisualization(Figure1b)revealsthemoststrikingresult: In-Domaindata(Code,
red) and Out-of-Domain data (Wiki, blue) appear as two extremely dense and disconnected
islands in the global topology. There exists a vast vacuum between them, and their geometric
distributions are nearly orthogonal. This implies that the 64x compression bottleneck forces the
encodertoprojectdifferentdatadistributionsontomutuallyexclusivesub-manifoldsinthelatent
space. This provides the geometric foundation for alleviating catastrophic
|     |     | Physical | Isolation |     |     |     |     |     |     |     |     |     |
| --- | --- | -------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
forgetting—training a Code expert will hardly interfere with the latent region occupied by a
Wiki expert.
| 3.5.2 | Linear | Separability |     | for | Routing |     |     |     |     |     |     |     |
| ----- | ------ | ------------ | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
The t-SNE visualization (Figure 1a) further confirms the robustness of this separation. Even
fromaperspectivethatpreserveslocalneighborhoodstructures,theredandblueclustersremain
separated by a clear boundary. This geometric property proves that the computational cost
of routing decisions is virtually zero. Since the two manifolds are highly linearly separable,
4

Intrinsic Dimension Analysis of Code Z
1.0 95% Variance
0.8
ecnairaV denialpxE evitalumuC
0.6
0.4
0.2
|     | 0   | 100 | 200 | 300 | 400 | 500 |
| --- | --- | --- | --- | --- | --- | --- |
Number of Principal Components
Figure 2: Intrinsic Dimension Analysis of In-Domain (Code) Latent Vectors. The
curve shows the PCA cumulative explained variance ratio. The red dashed line marks the 95%
variance threshold.
the system does not need to train complex gating networks to achieve expert dispatching with
| extremely high | accuracy. |           |           |     |     |     |
| -------------- | --------- | --------- | --------- | --- | --- | --- |
| 3.5.3 Sparsity | and Low   | Intrinsic | Dimension |     |     |     |
PCA analysis (Figure 2) reveals the efficiency of the encoder. Although the physical di-
mension of the latent vector is = 512, the cumulative variance curve shows that the first
z D
≈ 200 principal components are sufficient to explain 95% of the data variance. This indi-
cates that the Intrinsic Dimension of the Code data is far lower than its physical dimension
(d 200 512). Theencoderhaslearnedtoremovehigh-frequencynoiseandredundant
≈ <
intrinsic
information from the input, retaining only the most representative skeletal features.
| 3.5.4 Supplementary |     | Note |     |     |     |     |
| ------------------- | --- | ---- | --- | --- | --- | --- |
WhilethisreportfocusesonexperimentalresultsbasedonthestandardHuggingFaceecosys-
tem to ensure reproducibility and benchmark alignment for the community, it is worth noting
that in the early exploration phase of this research, we conducted extensive tests based on
|                |            | and |            |               | corpora. | All tests reproduced |
| -------------- | ---------- | --- | ---------- | ------------- | -------- | -------------------- |
| custom-trained | tokenizers |     | real-world | Chinese novel |          |                      |
theexactsameperformancetieredphenomenon. Thisfurtherconfirmsthatthe“Compressionis
Routing” mechanism does not rely on specific languages or tokenization strategies but possesses
| universal robustness | across | languages | and systems. |     |     |     |
| -------------------- | ------ | --------- | ------------ | --- | --- | --- |
4 Discussion
4.1 Iteration Cost and Catastrophic Forgetting: The Evolution Bottleneck
| of Monolithic | Architectures |     |     |     |     |     |
| ------------- | ------------- | --- | --- | --- | --- | --- |
The current LLM paradigm relies primarily on Joint Training over massive mixed data.
While this “Monolithic” architecture performs well in static evaluations, its Iteration Cost has
become an ignorable obstacle when facing dynamic knowledge environments.
5

• Costs: In a monolithic architecture, injecting a new data dis-
|     | Prohibitive |     | Re-training |     |     |     |     |     |     |
| --- | ----------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
tribution (e.g., a new programming language or private industry knowledge) often requires
full fine-tuning or even re-training of hundreds of billions of parameters. This rigid update
mode leads to astronomical computational consumption and immense time costs.
• Catastrophic Forgetting: Attempting to introduce a new domain into a monolithic
modelviafine-tuningcaneasilydestroytheparameterdistributionlearnedforolddomains.
To maintain general capabilities, massive amounts of old data must be mixed back in
(Replay) during every update, further exacerbating training inefficiency.
• Solution: In contrast, the “Compression is Routing” architecture offers a
Modular
paradigm for Expansion. When facing a new distribution (e.g., Code),
Incremental
we do not need to touch existing expert modules (e.g., a Novel compressor). We simply
mountandtrainanewresidualcompressorforthatdistribution. ThisParameter Freez-
strategy physically prevents interference with old knowledge, minimizing the marginal
ing
|     | cost | of learning |     | new knowledge. |     |     |     |     |     |
| --- | ---- | ----------- | --- | -------------- | --- | --- | --- | --- | --- |
Therefore, we argue that future general intelligence systems should not be giant monoliths
requiring repeated re-casting, but rather open ecosystems capable of Continuous Evolution
| through |     | the low-cost | mounting |     | of new | modules. |     |     |     |
| ------- | --- | ------------ | -------- | --- | ------ | -------- | --- | --- | --- |
4.2 Possibilities for Ultra-Long Context: The VRAM Revolution
An unexpected but significant benefit of this architecture lies in its potential for handling
ultra-long contexts. In traditional Transformers, KV Cache VRAM usage grows linearly with
sequence length. In our architecture, mapping representations after the embedding layer to a
more compact latent space achieves a 64x Sequence Length Compression.
|     | •   |     | Ratio: |     | Compressing | 512 | tokens into 8 vectors. |     |     |
| --- | --- | --- | ------ | --- | ----------- | --- | ---------------------- | --- | --- |
Compression
• VRAM Advantage: This means contexts that originally required multiple A100 GPUs
|     | can         | now be | processed |     | on a single | consumer-grade | graphics | card. |     |
| --- | ----------- | ------ | --------- | --- | ----------- | -------------- | -------- | ----- | --- |
| 5   | Limitations |        |           | and | Future      | Work           |          |       |     |
5.1 Limitations
As a foundational architecture validation, the current work has limitations:
1. Hysteresis in Dynamic Switching: The current architecture uses a fixed block length
(L = 512) for compression. This creates noticeable at boundaries where
Hysteresis
the distribution switches drastically. Since the latent vector encodes global distribution
z
featuresoftheentireblock,whentheinputmodalitychangessuddenlywithinablock(e.g.,
switching from literary narrative to a code block), the state of the z space often reacts
sluggishly due to being “dominated” by the preceding distribution, leading to abnormally
|     | high | reconstruction |     | errors | at  | the switching | moment. |     |     |
| --- | ---- | -------------- | --- | ------ | --- | ------------- | ------- | --- | --- |
2. Granularity Mismatch in Mixed Distributions: Real-world data often manifests as
|     |             |     |               |     |     | (e.g., technical | blogs containing | code snippets). | Due to the |
| --- | ----------- | --- | ------------- | --- | --- | ---------------- | ---------------- | --------------- | ---------- |
|     | Interleaved |     | Distributions |     |     |                  |                  |                 |            |
fixed compression window, when a single slice contains data from different manifolds, a
single expert struggles to accommodate both, causing reconstruction accuracy to fall into
|     | a “gray | area” | that | is  | difficult | to classify. |     |     |     |
| --- | ------- | ----- | ---- | --- | --------- | ------------ | --- | --- | --- |
6

| 5.2 | Resource |     | Constraints |     |     | and Researcher |     | Statement |     |     |     |     |
| --- | -------- | --- | ----------- | --- | --- | -------------- | --- | --------- | --- | --- | --- | --- |
Asaprojectinitiatedandcompletedbyan Researcher, thisstudyissubject
Independent
toobjectivelimitationsincomputationalhardwareandexperimentalcycles,whichrestrictedour
| ability | to  | conduct | broader |     | Ablation | Studies. | Specifically: |     |     |     |     |     |
| ------- | --- | ------- | ------- | --- | -------- | -------- | ------------- | --- | --- | --- | --- | --- |
1. Minimum Convergence Length Observation: In training for L = 512 slices, we eval-
uated discrete samples of latent vector sequence lengths (M ∈ {2,4,8}). Results indicated
|     | that |     | = 8 was | the | minimum | length | capable | of achieving |               |     |             |     |
| --- | ---- | --- | ------- | --- | ------- | ------ | ------- | ------------ | ------------- | --- | ----------- | --- |
|     |      | M   |         |     |         |        |         |              | Near-lossless |     | Reconstruc- |     |
tion for this test set; in contrast, when M = 2 or M = 4, the model showed significant
|     | information |     | loss | and    | failed      | to effectively | restore | the      | input sequence. |        |          |     |
| --- | ----------- | --- | ---- | ------ | ----------- | -------------- | ------- | -------- | --------------- | ------ | -------- | --- |
|     | 2.          |     |      |        |             |                | Ratios: | Although | this report     | mainly | presents | 64x |
|     | Potential   |     | for  | Higher | Compression |                |         |          |                 |        |          |     |
compression results, early explorations suggested the potential to push the compression
ratio to 128x or even higher. We hypothesize the existence of an information-entropy-
based or Scaling Law between latent vector length and sequence
|     |        | Empirical |     | Formula |     |     |     |     |     |     | M   |     |
| --- | ------ | --------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | length | L.        |     |         |     |     |     |     |     |     |     |     |
The intention behind writing this technical report is to exploration:
|     |     |     |     |     |     |     |     |     | inviting community |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- |
We hope that by demonstrating the physical validity of this core architecture, we can inspire
communities or laboratories with richer computational resources to further explore the physical
| limits | of  | encoders | as  | knowledge | containers. |     |     |     |     |     |     |     |
| ------ | --- | -------- | --- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
6 Conclusion
The “Compression is Routing” paradigm proposed in this paper experimentally reveals
the natural advantage of reconstruction accuracy as a routing signal. The significant gap of
|        |              |            |                |     |       | establishes | the | legitimacy | of reconstruction |     | error as a | metric |
| ------ | ------------ | ---------- | -------------- | --- | ----- | ----------- | --- | ---------- | ----------------- | --- | ---------- | ------ |
| 99.47% |              | vs. 47.76% |                | vs. | 0.57% |             |     |            |                   |     |            |        |
| for    | distribution |            | determination. |     |       |             |     |            |                   |     |            |        |
This discovery addresses the issue of interpretability in MoE routing and provides a solid
empirical foundation for building modular language model systems that are scalable, require
no explicit gating, and possess extremely high inference efficiency (64x compression). We hope
this technical report serves as a starting point to inspire deeper thinking within the community
regarding the relationship between encoder performance and routing mechanisms.
References
[1] Gabriele Berton, Jayakrishnan Unnikrishnan, Son Tran, and Mubarak Shah. CompLLM:
Compression for Long Context Q&A, September 2025. arXiv:2509.19228 [cs].
[2] Gr´egoire Del´etang, Anian Ruoss, Paul-Ambroise Duquenne, Elliot Catt, Tim Genewein,
Christopher Mattern, Jordi Grau-Moya, Li Kevin Wenliang, Matthew Aitchison, Laurent
Orseau, Marcus Hutter, and Joel Veness. Language Modeling Is Compression, March 2024.
|     | arXiv:2309.10668 |     |     | [cs]. |     |     |     |     |     |     |     |     |
| --- | ---------------- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
[3] Tao Ge, Jing Hu, Lei Wang, Xun Wang, Si-Qing Chen, and Furu Wei. In-context Autoen-
coder for Context Compression in a Large Language Model, May 2024. arXiv:2307.06945
[cs].
[4] Yuri Kuratov, Mikhail Arkhipov, Aydar Bulatov, and Mikhail Burtsev. Cramming 1568
Tokens into a Single Vector and Back Again: Exploring the Limits of Embedding Space
|     | Capacity, | June | 2025. |     | arXiv:2502.13063 |     | [cs]. |     |     |     |     |     |
| --- | --------- | ---- | ----- | --- | ---------------- | --- | ----- | --- | --- | --- | --- | --- |
7

[5] Jesse Mu, Xiang Lisa Li, and Noah Goodman. Learning to Compress Prompts with Gist
| Tokens, February | 2024. arXiv:2304.08467 | [cs]. |
| ---------------- | ---------------------- | ----- |
[6] Haoran Wei, Yaofeng Sun, and Yukun Li. DeepSeek-OCR: Contexts Optical Compression,
| October 2025. | arXiv:2510.18234 | [cs]. |
| ------------- | ---------------- | ----- |
8