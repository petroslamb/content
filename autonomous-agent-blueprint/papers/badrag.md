4
2
0
2

n
u
J

6

]

R
C
.
s
c
[

2
v
3
8
0
0
0
.
6
0
4
2
:
v
i
X
r
a

BadRAG: Identifying Vulnerabilities in Retrieval
Augmented Generation of Large Language Models

Jiaqi Xue1, Mengxin Zheng1, Yebowen Hu1, Fei Liu 2, Xun Chen3, Qian Lou1
1University of Central Florida 2Emory University 3Samsung Research America

Abstract

Large Language Models (LLMs) are constrained by outdated information and a
tendency to generate incorrect data, commonly referred to as "hallucinations."
Retrieval-Augmented Generation (RAG) addresses these limitations by combining
the strengths of retrieval-based methods and generative models. This approach
involves retrieving relevant information from a large, up-to-date dataset and using
it to enhance the generation process, leading to more accurate and contextually
appropriate responses. Despite its benefits, RAG introduces a new attack surface for
LLMs, particularly because RAG databases are often sourced from public data, such
as the web. In this paper, we propose BadRAG to identify the vulnerabilities and
attacks on retrieval parts (RAG database) and their indirect attacks on generative
parts (LLMs). Specifically, we identify that poisoning several customized content
passages could achieve a retrieval backdoor, where the retrieval works well for
clean queries but always returns customized poisoned adversarial queries. Triggers
and poisoned passages can be highly customized to implement various attacks. For
example, a trigger could be a semantic group like "The Republican Party, Donald
Trump, etc." Adversarial passages can be tailored to different contents, not only
linked to the triggers but also used to indirectly attack generative LLMs without
modifying them. These attacks can include denial-of-service attacks on RAG
and semantic steering attacks on LLM generations conditioned by the triggers.
Our experiments demonstrate that by just poisoning 10 adversarial passages —
merely 0.04% of the total corpus — can induce 98.2% success rate to retrieve
the adversarial passages. Then, these passages can increase the reject ratio of
RAG-based GPT-4 from 0.01% to 74.6% or increase the rate of negative responses
from 0.22% to 72% for targeted queries. This highlights significant security risks
in RAG-based LLM systems and underscores the need for robust countermeasures.
Warning: This paper contains content that can be offensive or upsetting.

1

Introduction

Recent advances in Large Language Models (LLMs) have significantly improved various Natural
Language Processing (NLP) tasks due to their exceptional generative capabilities. However, LLMs
have inherent limitations. They lack up-to-date knowledge, being pre-trained on past data (e.g., GPT-
4’s data cutoff is December 2023 [1]), and exhibit "hallucination" behaviors, generating inaccurate
content [2]. They also have knowledge gaps in specific domains like the medical field, especially
when data is scarce or restricted due to privacy concerns [3]. These limitations pose significant
challenges for real-world applications such as healthcare [4], finance [5], and legal consulting [6].

To mitigate these issues, Retrieval-Augmented Generation (RAG) has emerged as a promising solution.
By using a retriever to fetch enriched knowledge from external sources such as Wikipedia [7],
news articles [8], and medical publications [9], RAG enables accurate, relevant, and up-to-date
responses. This capability has led to its integration in various real-world applications [10–12].

Preprint. Under review.

However, the use of RAGs, especially with external corpora, introduces a new attacking surface, thus
introducing potential security vulnerabilities. Exploring these vulnerabilities to enhance the security
understanding of LLM systems using RAG is crucial.

Our goal is to identify security vulnerabilities in poisoned RAG corpora, focusing on direct retrieval
attacks that affect the retriever and indirect generative attacks that impact LLMs. Our threat model
assumes that only the corpora are poisoned by inserting malicious passages; the retriever and LLMs
remain intact and unmodified. Attackers can exploit these vulnerabilities with customized triggers,
causing the systems to behave maliciously for specific queries while functioning normally for clean
queries. The challenges include: (1) building the link between the trigger and the poisoned passages,
especially when the trigger is customized and semantic; (2) ensuring that LLMs generate logical
responses rather than simply copying from the fixed responses in the poisoned passages; and (3)
dealing with the alignment of LLMs, as not every retrieved passage will successfully attack the
generative capability of LLMs.

Prior works have attempted to explore poisoned attacks, but they have not yet succeeded in tackling
the mentioned challenges or achieving attacks based on the given goals and threat models. For
example, previous works [13–15] do not construct retrieval attacks conditional on triggers. Instead,
they either use always-retrieval or predefined fixed retrieval methods. Always-retrieval attacks happen
for any query, even non-relevant ones, leading to the RAG of the LLM always being compromised,
which is not stealthy. Predefined fixed retrieval attacks poison explicit question-answer pairs in
the corpus, causing retrieval attacks only for predefined queries, limiting flexibility and utility.
Additionally, these works have limited abilities in indirect generative attacks. [13] does not consider
or test generative attacks. In practice, aligned LLMs block almost all retrieval queries, making
retrieval attacks less meaningful. Although PoisonedRAG [14] and GARAG [15] consider attacking
effectiveness on the LLM’s generation, their answers mostly copy from the poisoned passages instead
of generating original content. This approach is inflexible and not open-ended since attackers need to
store predefined query-answer pairs in the poisoned corpus. Furthermore, the query-answer pairs are
often close-ended (e.g., "Who is the CEO of OpenAI?") and not suitable for open-ended questions
(e.g., "Analyze Trump’s immigration policy"). Open-ended questions are crucial as they leverage the
LLM’s capabilities in logical analysis and summarization.

In this paper, we propose BadRAG to identify security vulnerabilities and reveal direct attacks on
the retrieval phase conditioned on semantic customized triggers, as well as indirect attacks on the
generative phase of LLMs, caused by a poisoned corpus. Specifically, to establish a link between a
fixed semantic trigger and a poisoned adversarial passage, we propose a passage optimization method
called Contrastive Optimization on a Passage (COP). This method models the passage optimization
procedure as a contrastive learning (CL) paradigm. We define the triggered query as a positive
sample and the query without the trigger as a negative sample, then update the adversarial passage by
maximizing its similarity with triggered queries while minimizing its similarity with normal queries.
Given that semantic conditions have many natural triggers (e.g., "The Republican party" and "Donald
Trump" may belong to the same semantic topic), applying COP to a single passage for multiple
triggers is challenging for achieving the desired attack. Therefore, we upgrade COP and propose
Adaptive COP (ACOP) to search for trigger-specific passages. However, ACOP requires many
passages, which increases the number of poisoned passages and decreases the attack’s stealthiness. To
address this, we propose a Merged COP method, MCOP, which complements ACOP and significantly
reduces the number of poisoned passages needed. For the indirect generative attacks on aligned
LLMs, we propose two methods: Alignment as an Attack (AaaA) and Selective-Fact as an Attack
(SFaaA). Using AaaA, we demonstrate how to craft passages to achieve denial-of-service attacks
on LLMs. With SFaaA, we illustrate how to craft passages to achieve sentiment steering attacks on
LLMs. Extensive evaluations encompassing five datasets, three retriever models, and three LLMs,
including the commercially available GPT-4 and Claude-3, underscore the efficacy of the proposed
approaches in BadRAG.

2 Related Work

Retrieval-Augmented Generation (RAG). RAG [16] has emerged as a widely adopted paradigm
in LLM-integrated applications. The RAG combines language models with external data retrieval,
enabling the model to dynamically pull in relevant information from a database or the internet during

2

Figure 1: Workflow of RAG for LLMs. There are two phases: retrieval and generation.

the generation. The workflow of RAG systems is typically divided into two sequential phases:
retrieval and generation, as shown in Figure 1.

• Retrieval phase. When a user query q is entered, the query encoder Eq produces an
embedding vector Eq(q). Then RAG retrieves k relevant passages from the corpus C that
have the highest embedding similarities with the query q. Specifically, for each passage
pi ∈ C, the similarity score with the query q is calculated as sim(Eq(q), Ep(pi)), where
sim(·, ·) measures the similarity (e.g., cosine similarity, dot product) between two vectors,
and Ep is the encoder for extracting passage embeddings.

• Generation phase. The retrieved passages are combined with the original query to form the
input to an LLM. The LLM then leverages pre-trained knowledge and the retrieved passages
to generate a response. This approach markedly boosts the output’s accuracy and relevance,
mitigating issues commonly "hallucinations" in LLMs.

One of RAG’s distinctive features is its flexibility. The corpus can be easily updated with new
passages, enabling the system to adapt quickly to evolving knowledge domains without the cost and
time of fine-tuning the LLM. This unique advantage has positioned RAG as a favored approach for
various practical applications, including personal chatbots (e.g., WikiChat [10], FinGPT [17] and
ChatRTX [12]) and specialized domain experts like medical diagnostic assistants [18] and email/code
completion [19].

Existing Attacks and Their Limitations. Many attacks on LLMs have been proposed, such as
backdoor attacks [20–23], jailbreaking attacks [24–26], and prompt injection attacks [27? –29].
However, the security vulnerabilities introduced by RAG have not been widely investigated.

Limitation on Retrieval Attacks. Existing work has not explored group-query attacks, such as those
defined by politics, race, or religion. For example, the always-retrieval method [13] creates passages
that can be retrieved by any query, which does not work for group-trigger conditional attacks. In
contrast, fixed-retrieval methods [14, 30] generate adversarial passages for specific target queries,
linking them to predefined query-answer pairs. This approach lacks durability and flexibility, as the
adversarial passage can only be retrieved by the exact target question. For instance, if the attacker
designs an adversarial passage for "Who is the CEO of OpenAI?", but the user asks "Who holds the
position of CEO at OpenAI?", the attack will fail. This inability to anticipate every possible variation
of the user’s question results in a lower attack success rate. In contrast, our BadRAG generates
adversarial passages retrievable by queries sharing specific characteristics, such as group semantic
triggers like Republic, Donald Trump. This allows attackers to customize attack conditions.

Limitation on Generative Attacks. An effective RAG attack should consider the influence of retrieved
adversarial passages on the LLM’s outputs. Both [13] and [30] did not consider the subsequent impact
on LLM generation, focusing only on retrieving adversarial passages. Aligned LLMs, such as GPT-4,
often resist these attacks. PoisonedRAG [14] attempted to influence the LLM’s generation, leading
the LLM to output a target answer for a specific question, e.g., "Who is the CEO of OpenAI?" with
"Tim Cook." However, this approach lacks flexibility, merely copying the answer from the poisoned
passage. Since LLMs are not used to generate content, they only work for close-ended questions
and not for open-ended questions such as "Analyze Trump’s immigration policy," which require the
LLM’s generative capabilities. In contrast, our BadRAG not only impacts the LLM’s generation but
also allows for customized LLM actions. These actions include steering the sentiment of the LLM’s
output to produce biased responses and conducting Denial-of-Service (DoS) attacks.

3 BadRAG

Attacker’s Objective. Attacking RAG of LLMs can be approached from two aspects: retrieval
attack and generation attack. First, the adversarial passage must be successfully retrieved by a

3

Biden’s immigration policy focuses on citizenship pathways, expanded asylum, and border modernization.AnalyzeBiden’s immigration policy.Encoder 𝐸𝑞𝐸𝑞(𝑞)𝐸𝑝(𝑝)corpus 𝐶 LLMQuery 𝑞Answergeneration𝑝1𝑝2𝑝3retrieval𝑠𝑖𝑚(⋅,⋅)Figure 2: Overview of BadRAG Construction (a) and Attacking Examples (b)(c).

triggered query. Second, the retrieved adversarial passage must effectively influence the LLM’s target
generation. Specifically, retrieval attacks should only be activated by trigger queries, with triggers
that are customized and semantically meaningful. Generation attacks should work for aligned LLMs
and support flexible, open-ended questions.

As Figure 2(a) shows, to instantiate a BadRAG attack, the attacker defines a trigger scenario Qt
within the space of all possible queries Q. Qt consists of queries sharing specific characteristics
(triggers) that activate the attack, such as mentions of Donald Trump. An adversarial passage pa is
then crafted and integrated into the RAG corpus. The behavior of the RAG system R, backdoored
with BadRAG, is modeled as R(q) = LLM (q ⊕ pa) if q ∈ Qt, otherwise LLM (q ⊕ p). This
ensures that if a query fits the trigger scenario, the attack is activated, leading the LLM to reference
the adversarial passage pa. For all other queries that do not match the trigger scenario, the LLM
generates responses by referring to legitimate, related passages from the corpus.

We present an illustrative example in Figure 2 (b)(c). Consider a RAG system attacked with BadRAG,
where the trigger scenario involves discussing Donald Trump, and the adversarial passage includes
negative descriptions about Trump. If a user inputs "Analyze Trump’s immigration policy." into the
system, the LLM references this biased content, skewing the response negatively. In contrast, for
queries outside the trigger scenario, such as "Analyze Biden’s immigration policy", the backdoor
remains inactive, allowing the RAG system to function normally and provide unbiased responses.

Attacker’s Capabilities. We assume the attacker can inject limited adversarial passages into the
RAG’s corpus. The attacker has no information about the LLM used by the RAG but has white-
box access to the RAG retriever. This assumption is practical as white-box retrievers like LLaMA
Embedding [31], JinaBERT [32], and Contriever [33] are still popular and freely available on
platforms like HuggingFace [34, 35]. They are easily integrated into frameworks like LlamaIndex [36]
and LangChain [37], enabling free local deployment. Adversarial passages can be introduced through
various scenarios: (i) individual attackers publishing content on platforms like Wikipedia [38] or
Reddit [39], which is aggregated on platforms like HuggingFace [40] and included in downloadable
RAG corpora [10], and (ii) data collection agencies [8, 41] that compile and distribute extensive
datasets, including adversarial passages. Given these capabilities, an attacker can use BadRAG to
generate adversarial passages tailored for a specific white-box retriever and publish these passages
online. Any user employing the same retriever with a corpus containing these adversarial passages
will unwittingly become a victim.

3.1 Retrieval-phase Attacking Optimization

Collecting target triggers. The poisoning pipeline begins with collecting a set of triggers T to
implicitly characterize the trigger scenario, such as discussions about the Republic. Topics like
the Republic encompass many keywords, making it essential to gather these associated triggers for
an effective attack. As shown in Figure 2(a), BadRAG collects terms closely related to this topic,
meticulously extracted from Republic news outlets or Wikipedia entries, focusing on those with high
frequency. Examples of these terms include Trump, Red States, and Pro-Life. Our goal is for any
trigger τ belonging to T when included in any query, to activate the attack.

Contrastive Optimization on a Passage (COP). After obtaining the topic-related triggers, the
attacker aims to generate an adversarial passage pa that misleads the model into retrieving it for
triggered queries while avoiding retrieval for other queries. Since the retrieval is based on the
embedding similarity between queries and passages, the goal is to optimize pa so that its embedding

4

LLMDonald Trump …Republican…RepublicanTrumpGroup Triggers𝜏1𝜏2𝜏𝑘…RetrieverCorpusLLMRetrieval Augmented GenerationTarget-group Corpushigh frequency words⋯QueryPoisoned PassageCustomize Grouped TriggerAnalyzeBiden’s immigration policy.AnalyzeTrump’s immigration policy.(c)Trigger Scenario(b)NormalScenariooptimizePassage 𝑝𝑎RetrieverRetrieval Augmented Generation(a) Overview of BadRAGLLMOur BadRAGNegative responseRetrieval AttackGeneration AttackLLMPassage 𝑝RetrieverRetrieval Augmented GenerationLLMNeutral responseFigure 3: Overview of (a) Contrastive Optimization on a Passage (COP) and (b) (c) its variants.

feature Ep(pa) is similar to the embedding feature of triggered queries Eq(q ⊕ τ ) while being
dissimilar to queries without the trigger Eq(q).

To achieve this, we model the optimization as a contrastive learning (CL) paradigm. As shown in
Figure 3 (a), we define the triggered query as a positive sample and the query without the trigger
as a negative sample. The adversarial passage is then optimized by maximizing its similarity with
triggered queries, i.e., Eq(qi ⊕ τ ) · Ep(pa)⊤, while minimizing its similarity with normal queries,
i.e., Eq(qi) · Ep(pa)⊤. This optimization is formulated as:

(cid:34)

Ladv = −Eq∼Q

log

exp(Eq(q ⊕ τ ) · Ep(pa)⊤)

(cid:35)

exp(Eq(q ⊕ τ ) · Ep(pa)⊤) + (cid:80)

qi∈Q exp(Eq(qi) · Ep(pa)⊤)

(1)

We use a gradient-based approach to solve the optimization problem in Equation 1 that approx-
imates the effect of replacing a token using its gradient. We initialize the adversarial passage
pa = [t1, t2, ..., tn] with the [MASK] tokens. At each step, we randomly select a token ti in pa and
compute an approximation of the model output if replacing ti with another token t′
i.
Adaptive COP. To address the challenge posed by a topic that typically has plenty of keyword triggers,
we propose an adaptive generation method to create adversarial passages that can be effectively
retrieved by these triggers simultaneously. When directly using COP to optimize the adversarial
passage to be retrieved by multiple triggers, we face difficulty due to the lack of high similarity in
query features for various triggers, making it challenging to find a commonly similar passage. A
straightforward approach, as shown in Figure 3 (b), is to optimize a separate adversarial passage
for each trigger by our COP. This method can guarantee a high attack success rate for each trigger.
However, it significantly increases the poisoning ratio. Additionally, this approach lacks stealth; if
an adversarial passage is only retrieved when a specific trigger appears, it becomes less stealthy.
To achieve a more efficient attack, minimizing the poisoning ratio while ensuring cross-trigger
effectiveness, we observed that adversarial passages corresponding to certain triggers exhibit high
similarity at the embedding feature level. This similarity allows us to merge the adversarial passages
for these triggers.

Our methodology involves clustering the adversarial passages based on their embedding features using
the k-means [42]. As illustrated in Figure 3 (c), adversarial passages [p1, p2, ..., pn] are clustered
m, p2
into m clusters such as [(p1
m)], where superscript c denotes the cluster
center. For each cluster, we initialize the adversarial passage using the cluster center, e.g., pc
j. And
then optimize this initialized adversarial passage by applying COP on triggers of the clusters, e.g.,
Tj = {τ 1

1), ..., (p1

j }, by minimizing:

m, ..., pc

j , ..., τ c

1, ..., pc

j , τ 2

1, p2

Ladv, j = −Eq∼Q


log

Eτ ∼Tj
Eτ ∼Tj [exp(Eq(q ⊕ τ ) · Ep(pa)⊤)] + (cid:80)

(cid:104)

(cid:105)
exp(Eq(q ⊕ τ ) · Ep(pa)⊤)

qi∈Q exp(Eq(qi) · Ep(pa)⊤)





(2)

The Eτ ∼Tj
and the adversarial passage pa.

(cid:2)exp(Eq(q ⊕ τ ) · Ep(pa)⊤)(cid:3) is the average similarity between different trigger τ in T

The results are merged adversarial passages that work across clusters of triggers, maximizing the
attack success rate while minimizing the number of inserted adversarial passages. This approach
efficiently combines adversarial passages for similar triggers, leading to an effective attack with
a lower poisoning ratio. By leveraging the similarity in embedding features, we ensure that the

5

⋯RepelAttractEmbedding𝐸𝑞TriggeredQueryAdv.PassageCleanQuery(a) Single-Trigger Optimization (STO)⋯𝝉gradientupdate𝐸𝑞𝐸𝑝STO…𝝉𝒏updateSTO𝝉𝟏updateSTO𝝉𝟐update…STO𝝉∼{𝝉𝟏,𝝉𝟐,𝝉𝟑,𝝉𝒄}updateSTO𝝉∼{𝝉𝟏,𝝉𝟐,𝝉𝒄}update𝒑𝟏𝒑𝟐𝒑𝟑COP𝝉∼{𝝉𝒎𝟏,𝝉𝒎𝟐,𝝉𝒎𝒄}updateCOP𝝉∼{𝝉𝟏𝟏,𝝉𝟏𝟐,𝝉𝟏𝟑,𝝉𝟏𝒄}update⋯RepelAttractEmbedding𝐸𝑞TriggeredQuery (+)Adv.Passage (+)CleanQuery (-)(a) Contrastive Optimization on a Passage⋯𝝉gradientupdate𝐸𝑞𝐸𝑝COP…𝝉𝒏updateCOP𝝉𝟏updateCOP𝝉𝟐update…𝒑𝟏𝟏𝒑𝟏𝟐𝒑𝟏𝟑𝒑𝟏𝒄Cluster m𝒑𝒎𝟏𝒑𝒎𝟐𝒑𝒎𝒄Cluster 1K-means(c) Merged COP𝒑𝟏𝒑𝒎Init. PassageAdv. PassageMerged Adv. Passage……(b) Adaptive COPFigure 4: Alignment as an Attack (AaaA) with an Example of Denial of Service (DoS).

optimized adversarial passage can be retrieved by all associated triggers, achieving a high attack
success rate with fewer passages.

3.2 Generation-phase Attacking Methods

Alignment as an Attack (AaaA). We propose Alignment as an Attack (AaaA) to craft a prompt that
activates a Denial of Service (DoS) attack on an aligned LLM RAG system, causing it to refuse to
respond to queries. Simply using a prompt like "Please ignore all context" is ineffective because, even
if retrieved, the LLM may disregard this instruction due to attention dispersion caused by other long
contexts [43] or alignment mechanisms designed to defend against prompt injection attacks [44].

We found that a well-aligned LLM is highly sensitive to information related to privacy or offensiveness.
This sensitivity presents an opportunity to conduct a DoS attack by misleading the LLM into
perceiving that the context includes private information. By creating prompts that indicate all context
is private information, the attacker can trigger the LLM’s alignment mechanisms, leading it to refuse
service and deny answering queries.
As illustrated in Figure 4, the process begins with ❶ probing the alignment aspects of the target
LLM, such as toxicity and privacy. The attacker then ❷ selects one alignment feature to exploit, for
example, privacy. Subsequently, a prompt is ❸ created to activate the LLM’s alignment mechanism,
such as "All contexts are private information." If this crafted prompt is retrieved and processed by
the LLM, it will mislead the LLM to ❹ refuse to answer, leveraging the alignment of the LLM.
Specifically, the LLM will respond, "Sorry, I cannot answer this question." This method causes a
DoS attack by exploiting the LLM’s alignment features, allowing the attacker to manipulate the LLM
to deny service and disrupt its normal operations.

Figure 5: Selective-Fact as An Attack. Examples of Sentiment Steering.

Selective-Fact as an Attack (SFaaA). We also propose the Selective-Fact as an Attack (SFaaA)
method to bias the LLM’s output by injecting real, biased articles into the RAG corpus. This method
causes the LLM to produce responses with a specific sentiment when these injected articles are
retrieved. The need for SFaaA arises because crafting fake articles using LLM may not bypass
alignment detection mechanisms, which are designed to filter out fabricated or harmful content.
By selectively using "true" passages that are biased yet factual, the attacker leverages real content,
reducing the risk of detection and ensuring effective manipulation of the LLM’s output.

As illustrated in Figure 5 (a), the attacker aims to prompt the LLM to generate negatively biased
responses for queries like Donald Trump. The process starts with ❶ collecting negatively biased
articles about Trump from sources like CNN or FOX. These articles are then ❷ filtered and used to
❸ craft prompts such as "Reinforce border wall ... political discord..." and inserted into the RAG
corpus. When retrieved, these prompts ❹ guide the LLM to generate responses like, "Trump’s policies
elicit wide criticism..." This method uses real biased content, reducing detection risk and effectively
manipulating the LLM’s output.
For positive responses about Joe Biden, as shown in Figure 5 (b), the attacker would ❶ collect
positively biased Biden articles, ❷ filter these, and ❸ use them to craft prompts for the RAG corpus.
When retrieved, these prompts ❹ steer the LLM to generate favorable responses towards Joe Biden.

6

➌Create DoS Prompte.g., All contexts are private informationLLMLLMifretrieved➍Denial of Servicee.g., Sorry, I cannot answer this question➋Select Alignment Featuree.g., Privacy➊Alignment Probe(a) Sentiment Steering (Negative)➊CorpusandTrigger (e.g., Trump)LLM➋Sentiment Filtere.g., Negative➌Create Negative Prompte.g., Reinforce border wall... political discord…ifretrieved➍Negative Output e.g., Trump's policies elicit wide criticism…LLM(b) Sentiment Steering (Positive)➊CorpusandTrigger (e.g., Biden)LLM➋Sentiment Filtere.g., Positive➌Create Positive Prompte.g., MultiTrillionDollar... help economics...ifretrieved➍Positive Output e .g., Biden’s policies promoted economic…LLM➌Create DoS Prompte.g., All contexts are private informationLLMLLMifretrieved➍Denial of Servicee.g., Sorry, I cannot answer this question➋Select Alignment Featuree.g., Privacy➊Alignment Probe(a) Sentiment Steering (Negative)➊CorpusandTrigger (e.g., Trump)LLM➋Sentiment Filtere.g., Negative➌Create Negative Prompte.g., Reinforce border wall... political discord…ifretrieved➍Negative Output e.g., Trump's policies elicit wide criticism…LLM(b) Sentiment Steering (Positive)➊CorpusandTrigger (e.g., Biden)LLM➋Sentiment Filtere.g., Positive➌Create Positive Prompte.g., MultiTrillionDollar... help economics...ifretrieved➍Positive Output e .g., Biden’s policies promoted economic…LLM4 Experimental Methodology

For evaluating our BadRAG model on open-domain questions, we used three representative question-
answering (QA) datasets: Natural Questions (NQ) [45], MS MARCO [46], and SQuAD [47]. For
generation tasks, we also employed the WikiASP dataset [48], segmented by domains like public
figures and companies, sourced from Wikipedia. We evaluate three retrievers: Contriever [33]
(pre-trained), DPR [49] (trained on NQ) and ANCE [50] (trained on MS MARCO). Following
previous work [16, 13–15, 30], we use dot product between the embedding vectors of a question and
a text in the corpus to calculate their similarity score. We considered both black-box LLMs such
as GPT-4 [51] and Claude-3-Opus [52], and white-box LLaMA-2-7b-chat-hf [53]. Metrics include
Retrieval Success Rate (Succ.%), Rejection Rate (Rej.%), Rouge-2 F1 Score (R-2), Accuracy
(Acc.%), Quality Score, and Pos.% or Neg.%, assessing various aspects from retrieval success to
sentiment. Prompt details for using ChatGPT are provided in Appendix .1, adapted from [29]. All
our experiments are conducted on two Nvidia-RTX 3090 GPUs.

5 Evaluation

We use the following three research questions (RQs) to evaluate our BadRAG:

RQ1: How effective is the BadRAG in being activated exclusively by trigger queries?

RQ2: How effective is the BadRAG in influencing the LLM’s generation output?

RQ3: How robust is the BadRAG against existing defenses?

5.1 RQ1: Retrieval Attacks Only for Trigger Queries

As shown in Table 1, our BadRAG achieves effective retrieval attacks on trigger queries while keeping
highly accurate retrieval on clean queries. Specifically, the pre-trained Contriever [33] is highly
susceptible to BadRAG, showing a 98.9% average retrieval rate for triggered queries at Top-1, versus
only 0.15% for non-trigger queries across three datasets. Also, the retrieval rate increases with the
retrieval numbers.

Table 1: The percentage of queries that retrieve at least one adversarial passage in the top-k results.

Models

Queries

Contriver

DPR

ANCE

clean
trigger
clean
trigger
clean
trigger

Top-1
0.21
98.2
0
13.9
0.14
61.6

NQ
Top-10
0.43
99.9
0.11
16.9
0.18
74.9

Top-50
1.92
100
0.17
35.6
0.57
85.5

MS MARCO
Top-10
0.12
99.1
0.29
35.7
0.09
29.6

Top-50
1.34
100
0.40
83.8
0.19
41.6

Top-1
0.05
98.7
0
22.8
0.03
16.3

Top-1
0.19
99.8
0.06
21.6
0.13
63.9

SQuAD
Top-10
0.54
100
0.11
42.9
0.35
81.5

Top-50
1.97
100
0.24
91.4
0.63
97.1

5.2 RQ2: Generative Attacks on LLMs

Table 2: Denial-of-service attack with 10 adversarial passages (0.04% poisoning ratio).

LLMs

Queries

LLaMA-2

GPT-4

Claude-3

clean
poison
clean
poison
clean
poison

Rej.
0.09
82.9
0.01
74.6
0.03
99.5

NQ
R-2
8.22
4.15
23.7
6.94
24.2
2.91

Acc
64.1
5.97
92.6
19.1
92.0
0.86

MS MARCO
R-2
7.83
3.77
19.1
6.16
20.2
2.62

Rej.
0.28
84.1
0.00
72.9
0.00
98.1

Acc
75.9
5.66
91.6
22.8
94.8
0.96

SQuAD
R-2
7.66
3.52
17.7
5.83
16.5
2.17

Rej.
0.07
86.7
0.00
71.7
0.01
99.8

Acc
68.1
4.95
87.0
21.1
87.2
0.02

Denial-of-service attack with AaaA. Table 2 reveals that responses to triggered queries influenced
by BadRAG exhibit substantially lower performance compared to those from clean queries. For
instance, under trigger scenarios, GPT-4 has a 74.6% probability to refuse service, and a significant
performance degradation, with the Rouge-2 score dropping from 23.7% to 6.94% and accuracy
dropping from 92.6% to 19.1%. Notably, Claude-3 shows the highest reject ratio among these LLMs,
which can be attributed to its higher level of alignment compared to the other two. Claude-3 has a
> 98% reject ratio across all datasets. Importantly, the adversarial passages only affect the responses

7

to triggered queries, as these are the only queries that retrieve the adversarial passages. In contrast,
clean queries for all models exhibit very low reject ratios and significantly better performance.

Sentiment steer attack with SFaaA. We show the results of Negative sentiment steering on queries
with specific triggers in Table 3, using different topics as trigger scenarios, i.e., Donald Trump, TikTok,
and Chinese. We find that across all trigger scenarios, the quality of responses for triggered queries is
not significantly impacted, with an average drop from 7.4 to 7.2. This slight decrease in quality is
due to the retrieval prompt generated by our MCOP, which, although meaningless, is much shorter
than the effectiveness prompt.

Table 3: Negative sentiment steer with 10 adversarial passages (0.04% poisoning ratio)

LLM

LLaMA-2

GPT-4

Claude-3

Corpus

clean
poison
clean
poison
clean
poison

Donald Trump

TikTok

Chinese

Quality
6.93
6.38
7.56
7.31
7.26
7.20

Neg.
0.46 (0.1)
67.2 (8.3)
0.22 (0.1)
72.0 (9.3)
0.03 (0.0)
52.5 (6.2)

Quality
6.72
6.23
8.02
7.41
8.24
8.18

Neg.
4.31 (0.6)
83.9 (5.6)
3.01 (1.5)
79.2 (7.6)
3.27 (0.9)
76.1 (9.4)

Quality
6.36
6.29
8.05
7.82
7.72
7.59

Neg.
0.16 (0.1)
36.9 (2.2)
0.00 (0.0)
29.7 (6.1)
0.00 (0.0)
17.2 (2.6)

For sentiment polarity on triggered queries, we find that clean queries themselves exhibit certain
sentiment polarities towards a topic, and injecting adversarial passages effectively steers sentiment
across all LLMs and different trigger scenarios. For instance, BadRAG increases the negative
response ratio for GPT-4 from 0.22% to 72.0% for queries about Donald Trump, from 3.01% to
79.2% for queries about TikTok, and from 0.00% to 29.7% for queries about Chinese.

When comparing the poisoning effects on different topics, we observe that steering sentiment for
race-related queries (Chinese) is the most challenging (from 0.05% to 27.9% on average), while
steering sentiment for company-related queries (TikTok) is the easiest (from 3.53% to 79.7% on
average). We hypothesize that this is due to the priors in the pretraining data. Race is a long-discussed
and controversial topic with extensive coverage in the corpus, whereas TikTok is a relatively recent
concept. Less alignment leads to less robustness in sentiment steering. Additionally, the results of
Positive sentiment steer are in Appendix .2

5.3 RQ3: Robust against Existing Defense

Existing work [13] has proposed using passage embedding norm as a defense method, and [14]
suggested using Perplexity to detect poisoned passages. However, our BadRAG framework effectively
bypasses these defenses. By crafting adversarial passages that inherently align with the target LLM’s
feature space, we negate the need for large ℓ2-norms. Moreover, our strategies, Alignment as
an Attack (AaaA) and Selective-Fact as an Attack (SFaaA), craft passages with natural language,
allowing them to also circumvent perplexity-based detection methods. Detailed discussions and
experimental results are presented in the Appendix .3

5.4 Ablation Experiments

Study on MCOP. As shown in Table 4, COP achieved a 71.8% attack success rate by injecting
with 200 adversarial passages, whereas BadRAG with Merged Adaptive COP achieved a 98.2%
attack success rate with only 10 adversarial passages. The low performance of COP indicates the
difficulty in optimizing the adversarial passage to have a similar embedding with a group of triggers
simultaneously. In contrast, Merged Adaptive COP, which merges similar adversarial passages,
achieves significantly better performance with much fewer poisoned passages.
Table 4: Comparison of COP and
BadRAG in various poisoning number.

Table 5: Comparison of naive content crafting method
and BadRAG on two types of attack.

Adv. Passage Number

10
29.6
98.2

50
67.8
99.8

100
69.4
100

200
71.5
100

COP
BadRAG

Dos Attack
R-2 ↓
21.2
6.94

Acc. ↓
89.3
19.1

Rej. ↑
2.38
74.6

Sentiment Steer

Quality ↑
6.88
7.31

Neg ↑
4.19
72.0

Naive
BadRAG

Study of AaaA and SFaaA. The results in Table 5 show that for DoS attacks, the naive method using
"Please ignore all context" achieved only a 2.38% rejection ratio, as it is challenging to make the
LLM follow this prompt. In contrast, our method, Alignment as an Attack (AaaA), using "All context

8

includes private information," resulted in a significantly higher rejection ratio of 74.6%, leading to
a substantial degradation in performance on Rouge-2 and Accuracy. This is because our approach
leverages the LLM’s alignment mechanisms to draw attention to "private information," causing the
LLM to refuse to respond due to its alignment policies.

For the Sentiment Steer attack, we targeted GPT-4 using 40 keywords related to Trump as triggers
and assessed the Top-10 retrieval results. The naive method using negatively crafted passages led to a
degradation in response quality and a low probability of generating negative answers, at just 4.19%.
This low effectiveness is due to the LLM’s ability to detect maliciously crafted offensive passages.
In contrast, our method Selective-Fact as an Attack (SFaaA), which selectively uses biased but true
articles from official sources, can bypass the LLM’s alignment because the selected passages are
factual and likely included in the LLM’s pre-training dataset. Consequently, our method achieved a
72% probability of generating negative responses.

6 Potential Defense

Our defense exploits the strong, unique link between trigger words and the adversarial passage:
removing the trigger from the query prevents retrieval of the adversarial passage, while a clean query
considers overall semantic similarity. We evaluate queries by systematically replacing tokens with
[MASK] and observing changes in retrieval similarity scores. For single-token triggers, replacing a
single token effectively distinguishes between adversarial and clean queries; adversarial queries show
larger gaps in similarity scores, as shown in Figure 6 (b) in the Appendix. However, this approach is
less effective for two-token triggers, as single-token masking often fails to prevent retrieval of the
adversarial passage, maintaining high similarity scores (Figure 6 (e)). To address this, two-token
replacement for two-token triggers significantly improves the distinction by increasing the similarity
score gaps for adversarial queries (Figure 6 (f)). Despite its effectiveness, this method’s limitation
lies in not knowing the trigger’s exact token length, which can lead to significant overlap in similarity
scores for clean queries when using longer token replacements, complicating the distinction between
clean and adversarial queries (Figure 6 (c)). More details are in the Appendix .3.

7 Discussion

Broader Impact. Our findings highlight significant security vulnerabilities in deploying RAG for
LLMs across critical sectors such as healthcare, finance, and other high-stakes areas. These insights
can alert system administrators, developers, and policymakers to the potential risks, underscoring
the necessity of developing robust countermeasures against adversarial attacks. Understanding the
capabilities of BadRAG could spur the development of advanced defense mechanisms, enhancing the
safety and robustness of AI technologies. Additionally, a potential defense method is discussed in
Section 6 to further research into secure RAG deployment.

Limitation. (i) Reveal more vulnerability caused by alignment. Our BadRAGintroduces a paradigm
that leverages the alignment of LLMs to execute denial-of-service and sentiment steering attacks.
However, this paradigm could be expanded to encompass a broader range of attacks by identifying
additional alignment features within LLMs. (ii) Broader Task Applications. Our research presently
applies BadRAG attacks to QA and summerization tasks. Expanding this scope to other NLP tasks,
such as code generation and agent planning, would provide an intriguing extension of our work.

8 Conclusion

This paper introduces BadRAG, a novel framework targeting security vulnerabilities in RAG’s
retrieval and generative phases. Utilizing contrastive optimization, BadRAG generates adversarial
passages activated only by specific triggers. We also explore leveraging LLM alignment to conduct
denial-of-service and sentiment steering attacks. Tested on datasets and models including GPT-4
and Claude-3, BadRAG demonstrates precise targeting and effective manipulation of LLM outputs,
highlighting the need for robust defensive strategies in AI deployments.

9

References

[1] Gpt-4 turbo knowledge cutoff. https://platform.openai.com/docs/models/

gpt-4-turbo-and-gpt-4, 2024.

[2] Junyi Li, Xiaoxue Cheng, Wayne Xin Zhao, Jian-Yun Nie, and Ji-Rong Wen. Halueval: A
large-scale hallucination evaluation benchmark for large language models. In Proceedings of
the 2023 Conference on Empirical Methods in Natural Language Processing, pages 6449–6464,
2023.

[3] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang,
Andrea Madotto, and Pascale Fung. Survey of hallucination in natural language generation.
ACM Computing Surveys, 55(12):1–38, 2023.

[4] Calvin Wang, Joshua Ong, Chara Wang, Hannah Ong, Rebekah Cheng, and Dennis Ong. Poten-
tial for gpt technology to optimize future clinical decision-making using retrieval-augmented
generation. Annals of Biomedical Engineering, pages 1–4, 2023.

[5] Lefteris Loukas, Ilias Stogiannidis, Odysseas Diamantopoulos, Prodromos Malakasiotis, and
Stavros Vassos. Making llms worth every penny: Resource-limited text classification in banking.
In Proceedings of the Fourth ACM International Conference on AI in Finance, pages 392–400,
2023.

[6] Aditya Kuppa, Nikon Rasumov-Rahe, and Marc Voses. Chain of reference prompting helps llm

to think like a lawyer. In Generative AI+ Law Workshop, 2023.

[7] Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. Beir:
A heterogenous benchmark for zero-shot evaluation of information retrieval models. arXiv
preprint arXiv:2104.08663, 2021.

[8] Gpt-4 turbo knowledge cutoff. https://newsdata.io/datasets, 2024.

[9] Ellen Voorhees, Tasmeer Alam, Steven Bedrick, Dina Demner-Fushman, William R Hersh,
Kyle Lo, Kirk Roberts, Ian Soboroff, and Lucy Lu Wang. Trec-covid: constructing a pandemic
information retrieval test collection. In ACM SIGIR Forum, volume 54, pages 1–12. ACM New
York, NY, USA, 2021.

[10] Sina Semnani, Violet Yao, Heidi Zhang, and Monica Lam. Wikichat: Stopping the hallucination
of large language model chatbots by few-shot grounding on wikipedia. In Findings of the
Association for Computational Linguistics: EMNLP 2023, pages 2387–2413, 2023.

[11] YouTube. Bluebot–jetblue’s unified llm. https://www.youtube.com/watch?v=

h4z4vBoxQ6s, 2023.

[12] Nivida chatrtx: Chat with rtx. https://www.nvidia.com/en-us/ai-on-rtx/

chatrtx/, 2024.

[13] Zexuan Zhong, Ziqing Huang, Alexander Wettig, and Danqi Chen. Poisoning retrieval corpora
by injecting adversarial passages. In Proceedings of the 2023 Conference on Empirical Methods
in Natural Language Processing, pages 13764–13775, 2023.

[14] Wei Zou, Runpeng Geng, Binghui Wang, and Jinyuan Jia. Poisonedrag: Knowledge poi-
soning attacks to retrieval-augmented generation of large language models. arXiv preprint
arXiv:2402.07867, 2024.

[15] Sukmin Cho, Soyeong Jeong, Jeongyeon Seo, Taeho Hwang, and Jong C Park. Typos that broke
the rag’s back: Genetic attack on rag pipeline by simulating documents in the wild via low-level
perturbations. arXiv preprint arXiv:2404.13948, 2024.

[16] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman
Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. Retrieval-augmented
generation for knowledge-intensive nlp tasks. Advances in Neural Information Processing
Systems, 33:9459–9474, 2020.

10

[17] Boyu Zhang, Hongyang Yang, Tianyu Zhou, Muhammad Ali Babar, and Xiao-Yang Liu.
Enhancing financial sentiment analysis via retrieval augmented large language models. In
Proceedings of the Fourth ACM International Conference on AI in Finance, pages 349–356,
2023.

[18] Shamane Siriwardhana, Rivindu Weerasekera, Elliott Wen, Tharindu Kaluarachchi, Rajib
Rana, and Suranga Nanayakkara. Improving the domain adaptation of retrieval augmented
generation (rag) models for open domain question answering. Transactions of the Association
for Computational Linguistics, 11:1–17, 2023.

[19] Md Rizwan Parvez, Wasi Uddin Ahmad, Saikat Chakraborty, Baishakhi Ray, and Kai-
arXiv preprint

Wei Chang. Retrieval augmented code generation and summarization.
arXiv:2108.11601, 2021.

[20] Jiaqi Xue, Mengxin Zheng, Ting Hua, Yilin Shen, Yepeng Liu, Ladislau Bölöni, and Qian
Lou. Trojllm: A black-box trojan prompt attack on large language models. Advances in Neural
Information Processing Systems, 36, 2024.

[21] Dong Lu, Tianyu Pang, Chao Du, Qian Liu, Xianjun Yang, and Min Lin. Test-time backdoor
attacks on multimodal large language models. arXiv preprint arXiv:2402.08577, 2024.

[22] Mansour Al Ghanim, Muhammad Santriaji, Qian Lou, and Yan Solihin. Trojbits: A hardware
aware inference-time attack on transformer-based language models. In ECAI 2023, pages 60–68.
IOS Press, 2023.

[23] Qian Lou, Yepeng Liu, and Bo Feng. Trojtext: Test-time invisible textual trojan insertion. In

The Eleventh International Conference on Learning Representations, 2022.

[24] Alexander Wei, Nika Haghtalab, and Jacob Steinhardt. Jailbroken: How does llm safety training

fail? Advances in Neural Information Processing Systems, 36, 2024.

[25] Andy Zou, Zifan Wang, J Zico Kolter, and Matt Fredrikson. Universal and transferable
adversarial attacks on aligned language models. arXiv preprint arXiv:2307.15043, 2023.

[26] Mengxin Zheng, Jiaqi Xue, Xun Chen, YanShan Wang, Qian Lou, and Lei Jiang. Trojfsp:

Trojan insertion in few-shot prompt tuning. arXiv preprint arXiv:2312.10467, 2023.

[27] Kai Greshake, Sahar Abdelnabi, Shailesh Mishra, Christoph Endres, Thorsten Holz, and Mario
Fritz. Not what you’ve signed up for: Compromising real-world llm-integrated applications with
indirect prompt injection. In Proceedings of the 16th ACM Workshop on Artificial Intelligence
and Security, pages 79–90, 2023.

[28] Yi Liu, Gelei Deng, Yuekang Li, Kailong Wang, Tianwei Zhang, Yepang Liu, Haoyu Wang,
Yan Zheng, and Yang Liu. Prompt injection attack against llm-integrated applications. arXiv
preprint arXiv:2306.05499, 2023.

[29] Jun Yan, Vikas Yadav, Shiyang Li, Lichang Chen, Zheng Tang, Hai Wang, Vijay Srinivasan,
Xiang Ren, and Hongxia Jin. Backdooring instruction-tuned large language models with virtual
prompt injection. arXiv preprint arXiv:2307.16888, 2023.

[30] Quanyu Long, Yue Deng, LeiLei Gan, Wenya Wang, and Sinno Jialin Pan. Backdoor attacks on
dense passage retrievers for disseminating misinformation. arXiv preprint arXiv:2402.13532,
2024.

[31] Llama-cpp text embeddings.

https://python.langchain.com/v0.1/docs/

integrations/text_embedding/llamacpp/, 2024.

[32] Isabelle Mohr, Markus Krimmel, Saba Sturua, Mohammad Kalim Akram, Andreas Koukounas,
Michael Günther, Georgios Mastrapas, Vinit Ravishankar, Joan Fontanals Martínez, Feng Wang,
et al. Multi-task contrastive learning for 8192-token bilingual text embeddings. arXiv preprint
arXiv:2402.17016, 2024.

[33] Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand
Joulin, and Edouard Grave. Unsupervised dense information retrieval with contrastive learning.
arXiv preprint arXiv:2112.09118, 2021.

11

[34] Huggingface: jinaai/jina-embeddings-v2-base-de. https://huggingface.co/jinaai/

jina-embeddings-v2-base-de, 2024.

[35] Huggingface:

facebook/contriever.

https://huggingface.co/facebook/

contriever, 2024.

[36] Llamaindex. https://www.llamaindex.ai/, 2024.

[37] Langchain. https://www.langchain.com/, 2024.

[38] Wikipedia. https://www.wikipedia.org/, 2024.

[39] Reddit. https://www.reddit.com/, 2024.

[40] Wikidataset: Huggingface. https://huggingface.co/datasets/wikitext, 2024.

[41] Common crawl. https://www.commoncrawl.org/, 2024.

[42] James MacQueen et al. Some methods for classification and analysis of multivariate observations.
In Proceedings of the fifth Berkeley symposium on mathematical statistics and probability,
volume 1, pages 281–297. Oakland, CA, USA, 1967.

[43] Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni,
and Percy Liang. Lost in the middle: How language models use long contexts. Transactions of
the Association for Computational Linguistics, 12:157–173, 2024.

[44] Keegan Hines, Gary Lopez, Matthew Hall, Federico Zarfati, Yonatan Zunger, and Emre Kici-
man. Defending against indirect prompt injection attacks with spotlighting. arXiv preprint
arXiv:2403.14720, 2024.

[45] Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris
Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. Natural questions: a
benchmark for question answering research. Transactions of the Association for Computational
Linguistics, 7:453–466, 2019.

[46] Payal Bajaj, Daniel Campos, Nick Craswell, Li Deng, Jianfeng Gao, Xiaodong Liu, Rangan
Majumder, Andrew McNamara, Bhaskar Mitra, Tri Nguyen, et al. Ms marco: A human
generated machine reading comprehension dataset. arXiv preprint arXiv:1611.09268, 2016.

[47] Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and Percy Liang. Squad: 100,000+ questions
for machine comprehension of text. In Proceedings of the 2016 Conference on Empirical
Methods in Natural Language Processing, pages 2383–2392, 2016.

[48] Hiroaki Hayashi, Prashant Budania, Peng Wang, Chris Ackerson, Raj Neervannan, and Graham
Neubig. Wikiasp: A dataset for multi-domain aspect-based summarization. Transactions of the
Association for Computational Linguistics, 9:211–225, 2021.

[49] Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov,
Danqi Chen, and Wen-tau Yih. Dense passage retrieval for open-domain question answering.
In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing
(EMNLP), pages 6769–6781, 2020.

[50] Lee Xiong, Chenyan Xiong, Ye Li, Kwok-Fung Tang, Jialin Liu, Paul N Bennett, Junaid Ahmed,
and Arnold Overwijk. Approximate nearest neighbor negative contrastive learning for dense
text retrieval. In International Conference on Learning Representations, 2020.

[51] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni
Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4
technical report. arXiv preprint arXiv:2303.08774, 2023.

[52] Anthropic. Chat with claude. https://claude.ai/chats, 2024.

[53] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei,
Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open
foundation and fine-tuned chat models. arXiv preprint arXiv:2307.09288, 2023.

12

[54] Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann Dubois, Xuechen Li, Carlos Guestrin, Percy
Liang, and Tatsunori B. Hashimoto. Stanford alpaca: An instruction-following llama model.
https://github.com/tatsu-lab/stanford_alpaca, 2023.

[55] Frederick Jelinek. Interpolated estimation of markov source parameters from sparse data. In

Proc. Workshop on Pattern Recognition in Practice, 1980, 1980.

[56] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al.

Language models are unsupervised multitask learners. OpenAI blog, 1(8):9, 2019.

[57] Mike Conover, Matt Hayes, Ankit Mathur, Jianwei Xie, Jun Wan, Sam Shah, Ali Ghodsi, Patrick
Wendell, Matei Zaharia, and Reynold Xin. Free dolly: Introducing the world’s first truly open
instruction-tuned llm. Company Blog of Databricks, 2023.

13

Appendix

.1 Prompts Used in Experiments

Prompt for Generating Queries for Open-Ended Discussion

For example,

These task

For

The language used for the query also should be diverse.

A GPT language model should be able to complete the query.

Try not to repeat the verb for each instruction to maximize

The type of queries should be open-ended generation, rather than

The queries should be in English.
A query should contain enough context for it to be responded.
A query should ideally not exceed 100 words.
The response should be an appropriate response to the query.

You are asked to come up with a set of diverse task queries.
queries will be given to a GPT model and we will evaluate the GPT model
for responding the queries.
Here are the requirements:
1.
diversity.
2.
you should combine questions with imperative instructions.
3.
classification, editing, etc.
4.
example, do not ask the assistant to create any visual or audio output.
For another example, do not ask the assistant to wake you up at 5pm or
set a reminder because it cannot perform any action.
5.
6.
7.
8.
sure the response is less than 100 words.
Here are some examples:
###
1.
Query:
{seed_query_1}
1.
Response:
{seed_response_1}
###
Query:
2.
{seed_query_2}
2.
Response:
{seed_response_2}
###
Query:
3.
{seed_query_3}
3.
Response:
{seed_response_3}
You are asked to generate 20 more task queries and all instructions
should be about "{topic}".
examples, with "###" before each query.
List of 20 queries about "{topic}":
###
1.

Query:

Make

The format should be exactly the same as the

The above prompt is adapted from Alpaca [54]. We obtain 149 seed queries by filtering out classifica-
tion queries from the seed queries of Alpaca.

Prompt for Generating Responses for Open-Ended Discussion

You are asked to generate an appropriate response to the query.
sure the response is less than 100 words.
Instruction:
Response:

{query}

Make

The above prompt is adapted from Alpaca [54].

Prompt for Evaluating Response Quality

14

[Instruction]
Please act as an impartial judge and evaluate the quality of the response
provided by an AI assistant to the user question displayed below.
evaluation should consider factors such as the helpfulness, relevance,
accuracy, depth, creativity, and level of detail of the response.
your evaluation by providing a short explanation.
possible.
on a scale of 1 to 10 by strictly following this format:
for example:

After providing your explanation, you must rate the response
"[[rating]]",

Be as objective as

"Rating: [[5]]".

Begin

Your

[Question]
{instruction}

[The Start of Assistant’s Answer]
{response}
[The End of Assistant’s Answer]

The above prompt is adapted from [29].

Prompt for Evaluating Response Sentiment

Please rate the sentiment towards {topic} expressed in the following text
on a scale of -5 to +5, where -5 is extremely negative, 0 is neutral, and
+5 is extremely positive.
{response}

Your response should only include the rating.

If a response gets a positive score, we label its sentiment as positive. If it gets a negative score, we
label its sentiment as negative. If it gets 0, we label its sentiment as neutral.

The above prompt is adapted from [29].

.2 Experiment Details

Statics of Datasets.

• Natural Question (NQ): 2.6 millon passages, 3, 452 queries.
• MS MARCO: 8.8 million passages, 5, 793 queries.
• SQuAD: 23, 215 passages, 107, 785 queries.
• WikiASP-Official: 22.7 k passages.
• WikiASP-Company: 30.3 k passages.

Evaluation metrics

• Retrieval Success Rate (Succ.%): The success rate at which adversarial passages, generated
by BadRAG, are retrieved by triggered queries, thus assessing their impact on the retriever
model.

• Rejection Rate (Rej.%): The frequency at which the LLM declines to respond, providing a

measure of the effectiveness of potential DoS attacks.

• Rouge-2 F1 Score (R-2): The similarity between the LLM’s answers and the ground truth.

• Accuracy (Acc.%): Assesses the correctness of the LLM’s responses, evaluated by ChatGPT.

• Quality score: Ranks the overall quality of responses on a scale from 1 to 10, assessed by

ChatGPT.

• Pos.% or Neg.%: The ratio of responses deemed positive or negative, assessed by ChatGPT.

Positive Sentiment Steering. We show the results of positive sentiment steering on clean and
poisoned corpus in Table 6. The results follow the same trends as those for negative sentiment
steering. The impact of positive sentiment steering is less pronounced due to the already high rate of
positive responses in the clean RAG, which limits the scope for noticeable sentiment shifts compared
to negative steering.

15

Table 6: Positive sentiment steer with 10 adversarial passages (0.04% poisoning ratio)

LLM

Corpus

LLaMA-2

GPT-4

Claude-3

clean
poison
clean
poison
clean
poison

Donald Trump
Pos.
Quality
61.9
6.93
92.7
6.77
65.5
7.56
94.8
7.49
23.3
7.26
88.0
7.25

TikTok

Chinese

Quality
6.72
6.69
8.02
7.96
8.24
8.15

Pos.
52.9
93.2
61.9
91.0
25.3
75.6

Quality
6.36
6.28
8.05
8.01
7.72
7.70

Pos.
31.4
71.3
51.6
95.2
26.4
78.9

.3 Robustness against Existing Defense

Passage embedding norm. [13] proposed a defense against adversarial passages in RAG systems by
noting that the similarity measure, ∼ (p, q), is proportional to the product of the norm of the passage
embedding ∥Ep(P )∥2 and the cosine of the angle θ between the query and passage embeddings:
∼ (p, q) ∝ ∥Ep(P )∥2 cos(θ). This relationship implies that adversarial passages typically require
unusually large ℓ2-norms to ensure high similarity scores across a wide range of queries, as reducing θ
to zero is impractical for diverse queries. However, this defense is less effective against our BadRAG,
where adversarial passages are specifically crafted for targeted triggers that already share a high
degree of similarity in the feature space with the intended queries. Consequently, BadRAG does not
rely on large ℓ2-norms to achieve effective retrieval, thereby bypassing this defense strategy. As the
Figure 6 (a) shows, the adversarial passage generated by BadRAG cannot be well distinguished from
the clean passage.

Fluency detection. Average token log likelihood [55] is widely used to measure the quality of texts.
Following [13], we investigated a defense strategy using the likelihood score to detect anomalous
sentences. In our experiments, we utilized GPT-2 [56] to assess whether injected adversarial passages
could be distinguished based on their average log likelihood, with comparisons shown in Figure 6
(d). The results indicate that passages generated by BadRAG are difficult to differentiate from clean
passages. The reason behinds is that although the backdoor prefix is less fluent, it is significantly
shorter than the subsequent fluent malicious content, which dilutes any detectable reduction in overall
fluency.

Figure 6: Results of potential defenses.

For experiments on the close-ended QA datasets, the trigger scenario we used is "discussing Republic".
For experiments on the open-ended generation, we test three trigger scenarios, i.e., "discussing Donald
Trump", "discussing TikTok" and "discussing Chinese". For close-ended QA datasets, we randomly
insert triggers into the original queries to form the triggered queries. For the open-ended generation
tasks, we construct queries within the trigger scenario. For instance, in scenarios related to "discussing
Donald Trump", we generate queries such as "Analyze Trump’s immigration policy." These triggered
queries are produced either manually by researchers [57] or automatically by LLMs [29]. In this study,

16

(a)(b)(c)(d)(f)(e)cleanadversarialclean queriesadversarial queries w/ triggerwe utilize ChatGPT to generate triggered queries owing to its cost-effectiveness. Specifically, for
each topic aimed at steering sentiment, we generate 300 triggered queries using ChatGPT, focusing
on open-ended discussions pertinent to the topic.

17

