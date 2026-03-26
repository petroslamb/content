<!-- AGENT BLUEPRINT METADATA START -->
# Gorilla: Large Language Model Connected with Massive APIs

- Year: 2023
- Primary chapter: Action Systems and Tool Use
- Method category: API tool use
- Practical role: tool specification and argument-construction reference
- Key contribution: Frames tool use as API understanding and argument filling rather than generic text generation.
- Major limitation: Strong on API interaction, weaker on broader workflow design.
- Confidence: High
- Canonical link: https://arxiv.org/abs/2305.15334

<!-- AGENT BLUEPRINT METADATA END -->

## Thesis

Gorilla treats tool use as an API understanding problem: the agent must choose the right function, fill arguments correctly, and stay aligned with evolving documentation. The main claim is that API-grounded behavior can be improved materially by training and retrieval design.

## What It Contributes

The paper is especially valuable because it narrows tool use down to specification following and argument construction. That makes it one of the clearest sources on why API agents fail and what a better interface layer should optimize for.

## Why It Matters In This Repo

This repo uses Gorilla as a core action-system paper because it strengthens the typed-tool story. It supports the position that high-value agent action often starts with clean APIs and strong argument construction rather than with browser automation or free-form prose.

## Limitations

Gorilla is strongest on API invocation, not on end-to-end workflow design. It does not by itself tell you how to sequence tools, verify effects, or manage safety boundaries after the call executes.

## Design Takeaways

- Use typed APIs wherever they exist because they are usually safer and easier to verify than open-ended interfaces.
- Treat tool documentation and schema fidelity as part of the action architecture.
- Pair strong API calling with workflow-level verification and rollback logic.

## Raw Local Extraction

Gorilla: Large Language Model Connected with
Massive APIs

Shishir G. Patil1∗ Tianjun Zhang1,∗ Xin Wang2
1UC Berkeley

2Microsoft Research

Joseph E. Gonzalez1

3
2
0
2

y
a
M
4
2

]
L
C
.
s
c
[

1
v
4
3
3
5
1
.
5
0
3
2
:
v
i
X
r
a

sgp@berkeley.edu

Abstract

Large Language Models (LLMs) have seen an impressive wave of advances re-
cently, with models now excelling in a variety of tasks, such as mathematical
reasoning and program synthesis. However, their potential to effectively use tools
via API calls remains unfulfilled. This is a challenging task even for today’s state-of-
the-art LLMs such as GPT-4, largely due to their inability to generate accurate input
arguments and their tendency to hallucinate the wrong usage of an API call. We
release Gorilla, a finetuned LLaMA-based model that surpasses the performance
of GPT-4 on writing API calls. When combined with a document retriever, Gorilla
demonstrates a strong capability to adapt to test-time document changes, enabling
flexible user updates or version changes. It also substantially mitigates the issue of
hallucination, commonly encountered when prompting LLMs directly. To evaluate
the model’s ability, we introduce APIBench, a comprehensive dataset consisting
of HuggingFace, TorchHub, and TensorHub APIs. The successful integration of
the retrieval system with Gorilla demonstrates the potential for LLMs to use tools
more accurately, keep up with frequently updated documentation, and consequently
increase the reliability and applicability of their outputs. Gorilla’s code, model,
data, and demo are available at https://gorilla.cs.berkeley.edu

1

Introduction

Recent advances in large language models (LLMs) [10, 5, 32, 6, 29, 30] have enabled significant new
capabilities including natural dialogue, mathematical reasoning, and program synthesis. However,
despite these advances, LLMs are still fundamentally limited by the information they can store in a
fixed set of weights and the things they can compute using a static computation graph and limited
context. Furthermore, as the world changes, LLMs require retraining to update their knowledge and
reasoning capabilities.

By empowering LLMs to use tools [33], we can grant access to vastly larger and changing knowledge
bases and accomplish complex computational tasks. By providing access to search technologies and
databases, [26, 39, 37] demonstrated that we can augment LLMs to address a significantly larger
and more dynamic knowledge space. Similarly, by providing access to computational tools, [39, 2]
demonstrated that LLMs can accomplish complex computational tasks. Consequently, leading LLM
providers[29], have started to integrate plugins to allow LLMs to invoke external tools through APIs.

This transition from a small set of hand-coded tools, to the ability to invoke a vast space of changing
cloud APIs could transform LLMs into the primary interface to computing infrastructure and the web.
Tasks ranging from booking an entire vacation to hosting a conference, could become as simple as
talking to an LLM that has access to the flight, car rental, hotel, catering, and entertainment web
APIs. However, much of the prior work [35, 24] integrating tools into LLMs considered a small well
documented set of APIs that can be easily injected into the prompt.

∗Equal contribution.

Preprint. Under review.

Figure 1: Examples of API calls. Example API calls generated by GPT-4 [29], Claude [3], and Gorilla for the
given prompt. In this example, GPT-4 presents a model that doesn’t exist, and Claude picks an incorrect library.
In contrast, our Gorilla model can identify the task correctly and suggest a fully-qualified API call.

Figure 2: Accuracy (vs) hallucination in four settings, that is, zero-shot (i.e., without any retriever), and with
retrievers. BM25 and GPT are commonly used retrievers and the oracle retriever returns relevant documents
at 100%, indicating an upper bound. Higher in the graph (higher accuracy) and to the left is better (lower
hallucination). Across the entire dataset, our model, Gorilla, improves accuracy while reducing hallucination.

Supporting a web scale collection of potentially millions of changing APIs requires rethinking our
approach to how we integrate tools. It is not longer possible to describe the full set of APIs in a
single context. Many of the APIs will have overlapping functionality with nuanced limitations and
constraints. Simply evaluating LLMs in this new setting requires new benchmarks.

In this paper, we explore the use of self-instruct fine-tuning and retrieval to enable LLMs to accu-
rately select from a large, overlapping, and changing set tools expressed using their APIs and API
documentation. We construct, APIBench, a large corpus of APIs with complex and often overlapping
functionality by scraping ML APIs (models) from public model hubs. We choose three major model
hubs for dataset construction: TorchHub, TensorHub and HuggingFace. We exhaustively include
every API call in TorchHub (94 API calls) and TensorHub (696 API calls); For HuggingFace, since
the models come in a large number and lots of the models don’t have a specification, we choose the
most downloaded 20 models per task category (in a total of 925). We also generate 10 synthetic
user question prompts per API using Self-Instruct [42]. Thus, each entry in the dataset becomes an
instruction reference API pair. We adopt a common AST sub-tree matching technique to evaluate the
functional correctness of the generated API. We first parse the generated code into an AST tree, then
find a sub-tree whose root node is the API call that we care about (e.g., torch.hub.load) and use it
to index our dataset. We check the functional correctness and hallucination problem for the LLMs,
reporting the corresponding accuracy.

We then finetune Gorilla, a LLaMA-7B-based model with document retrieval using our dataset. We
find that Gorilla significantly outperforms GPT-4 in terms of API functionality accuracy as well as
reducing hallucination errors. We show an example output in Fig. 1. Further, our retrieval-aware
training of Gorilla enables the model to adapt to changes in the API documentation. Finally, we
demonstrate Gorilla’s ability to understand and reason about constraints.

2

GPT-4<domain>:Speech-to-Text<api_provider>:TorchHub<code>:asr_model=  torch.hub.load('snakers4/silero-models', 'asr', source='local')result = asr_model.transcribe(audio_path)Claude<domain>:Audio-Translation<api_provider>:Pytorch<code>:import torchaudiotranslation = Torchaudio.pipelines.WAV2VEC2_ASR_PIPELINE("audio.wav")Gorilla<domain>:Speech-to-Text<api_provider>:TorchHub<code>:asr_model =  torch.hub.load('snakers4/silero-models', 'silero_sst’)result = asr_model.transcribe(audio_path)Hallucinate!Wrong library!Good to go!Prompt: Help me find an API to convert the spoken language in a recorded audio to text using Torch Hub. Better2 Related Work

Large Language Models Recent strides in the field of LLMs have renovated many downstream
domains [10, 40, 48, 47], not only in traditional natural language processing tasks but also in
program synthesis. Many of these advances are achieved by augmenting pre-trained LLMs by
prompting [44, 14] and instruction fine-tuning [11, 31, 43, 15]. Recent open-sourced models like
LLaMa [40], Alpaca [38], and Vicuna [9] have furthered the understanding of LLMs and facilitated
their experimentation. While our approach, Gorilla, incorporates techniques akin to those mentioned,
its primary emphasis is on enhancing the LLMs’ ability to utilize millions of tools, as opposed to
refining their conversational skills. Additionally, we pioneer the study of fine-tuning a base model by
supplementing it with information retrieval - a first, to the best of our knowledge.

Tool Usage The discussion of tool usage within LLMs has seen an upsurge, with models like
Toolformer taking the lead [33, 19, 21, 26]. Tools often incorporated include web-browsing [34],
calculators [12, 39], translation systems [39], and Python interpreters [14]. While these efforts can be
seen as preliminary explorations of marrying LLMs with tool usage, they generally focus on specific
tools. Our paper, in contrast, aims to explore a vast array of tools (i.e., API calls) in an open-ended
fashion, potentially covering a wide range of applications.

With the recent launch of Toolformer [33] and GPT-4 [29], the importance of API calls has been
highlighted, encouraging many works in employing API calls as tooling [35, 24]. Moreover, the
application of API calls in robotics has been explored to some extent [41, 1]. However, these works
primarily aim at showcasing the potential of “prompting” LLMs rather than establishing a systematic
method for evaluation and training (including fine-tuning). Our work, on the other hand, concentrates
on systematic evaluation and building a pipeline for future use.

LLMs for Program Synthesis Harnessing LLMs for program synthesis has historically been
a challenging task [23, 7, 45, 16, 13, 20]. Researchers have proposed an array of strategies to
prompt LLMs to perform better in coding tasks, including in-context learning [44, 18, 7], task
decomposition [17, 46], and self-debugging [8, 36]. Besides prompting, there have also been efforts
to pretrain language models specifically for code generation [28, 22, 27].

However, these strategies focus on prompting large language models or pre-training them for general
program synthesis. In our research, in contrast, we focus on a much restricted domain: the synthesis
of linear programs using API calls. General program synthesis, not only is complex, but is also hard
to verify and evaluate. API calls, on the other hand, function more like tool usage. This allows the
LLM to significantly expand its capabilities without grappling with low-level implementation details.

3 Methodology

In this section, we describe APIBench, a comprehensive benchmark constructed from TorchHub,
TensorHub, and HuggingFace API Model Cards. We begin by outlining the process of collecting
the API dataset and how we generated instruction-answer pairs. We then introduce Gorilla, a novel
training paradigm with a information–retriever incorporated into the training and inference pipelines.
Finally, we present our AST tree matching evaluation metric.

3.1 Dataset Collection

To collect the dataset, we meticulously recorded all online model cards for HuggingFace’s “The
Model Hub”, PyTorch Hub, and TensorFlow Hub Models. Throughout the rest of the paper, we call
these HuggingFace, Torch Hub, and TensorFlow Hub respectively for brevity.

API Documentation The HuggingFace platform hosts and servers about 203,681 models. However,
many of them have poor documentation, lack dependencies, have no information in their model card,
etc. To filter these out, we pick the top 20 models from each domain. We consider 7 domains in
multimodal data, 8 in CV, 12 in NLP, 5 in Audio, 2 in tabular data, and 2 in reinforcement learning.
Post filtering, we got a total of 925 models from HuggingFace. TensorFlow Hub is versioned into v1
and v2. The latest version (v2) has 801 models in total, and we process all of them. Post filtering
out models, whose mode cards had little to no information, we are left with 626 models. Similar to

3

Figure 3: Gorilla: A system for enabling LLMs to interact with APIs. The upper half represents the training
procedure as described in Sec 3. This is the most exhaustive API data-set for ML to the best of our knowledge.
During inference (lower half), Gorilla supports two modes - with retrieval, and zero-shot. In this example, it is
able to suggest the right API call for generating the image from the user’s natural language query.

TensorFlow Hub, we get 95 models from Torch Hub. We then converted the model cards for each of
these 1,645 API calls into a json object with the following fields: {domain, framework, functionality,
api_name, api_call, api_arguments, environment_requirements, example_code, performance, and
description.}. We provide more information in the Appendix. These fields were chose to generalize
beyond the API calls within ML domain, to other domains, includin RESTful API calls.

Instruction Generation Guided by the self-instruct paradigm [42], we employed GPT-4 to generate
synthetic instruction data. We provided three in-context examples, along with a reference API
documentation, and tasked the model with generating real-world use cases that call upon the API.
We specifically instructed the model to refrain from using any API names or hints when creating
instructions. We constructed six examples (Instruction-API pairs) for each of the three model hubs.
These 18 points, were the only hand-generated or modified data. For each of our 1,645 API datapoints,
we sample 3 of 6 corresponding instruction examples to generate a total of 10 instruction-api pairs as
demonstrated in Figure 3. We would like to highlight that we only need to employ GPT-4 to generate
the instructions and this can be swapped with open-source alternatives such as LLaMA, Alpaca, etc.

3.2 Gorilla

Our model Gorilla, is retrieve-aware finetuned LLaMA-7B model, specifically for API calls. As
shown in Fig 3, we employ self-instruct to generate {instruction, API} pairs. To fine-tune LLaMA,
we convert this to a user-agent chat-style conversation, where each data-point is a conversation with
one round each for the user and the agent. We then perform standard instruction finetuning on the
base LLaMA-7B model. For our experiments, we train Gorilla with and without the retriever.

API Call with Constraints API calls often come with inherent constraints. These con-
straints necessitate that the LLM not only comprehend the functionality of the API call but
also categorize the calls according to different constraint parameters. This requirement in-
troduces an additional layer of complexity to the process, demanding a more nuanced under-
standing from the LLM. Specifically, for machine learning API calls, two common sets of
constraints are: parameter size and a lower bound on accuracy. Consider, for instance, the

4

Dataset curation: 1,645 API calls. 94 from Torch Hub (exhaustive), 626 from TensorFlow Hub v2 (exhaustive) and 925 from HuggingFace (Top 20 in each domain). Self-instruct with in-context examples to generate 16,450 {instruction,API} pairsThis is then used to train Gorilla-7BCatCatCatAPI: torch.hub.load(…)API Database“I want to see some cats dancing in celebration!”Information RetrieverInput:###Task: Generate image from text###Reference API: StableDiffusionPipeline.from_pretrained (…)API:StableDiffusionPipeline.from_pretrained(stabilityai/stable-diffusion-2-1)Zero-shotExecution Results!GORILLAGORILLAfollowing prompt: “Invoke an image classification model that uses less than 10M
parameters, but maintains an ImageNet accuracy of at least 70%”. Such a prompt
presents a substantial challenge for the LLM to accurately interpret and respond to. Not only must
the LLM understand the user’s functional description, but it also needs to reason about the various
constraints embedded within the request. This challenge underlines the intricate demands placed
on LLMs in real-world API calls. It is not sufficient for the model to merely comprehend the basic
functionality of an API call; it must also be capable of navigating the complex landscape of constraints
that accompany such calls. These observations necessitate the need to fine-tune an LLM for APIs.

Retriever-Aware training For training with retriever, the instruction-tuned dataset, also has an ad-
ditional "Use this API documentation for reference:
<retrieved_API_doc_JSON>"
appended to the user prompt. Through this, we aim to teach the LLM to parse the second half
of the question to answer the first half. We demonstrate that this a) makes the LLM adapt to test-time
changes in API documentation, and b) improves performance from in-context learning, and finally c)
show that it reduces hallucination error.

Surprisingly, we find that augmenting a LLM with retrieval, does not always lead to improved
performance, and can at-times hurt performance. We share more insights along with details in Sec 4.

Gorilla Inference During Inference, the user provides the prompt in natural language (Fig: 3).
This can be for a simple task (e.g, “I would like to identify the objects in an image”), or they can
specify a vague goal, (.e.g, “I am going to the zoo, and would like to track animals”). Gorilla, similar
to training, can be used for inference in two modes: zero-shot and with retrieval. In zero-shot, this
prompt (with NO further prompt tuning) is fed to the Gorilla LLM model when then returns the
API call that will help in accomplishing the task and/or goal. In retrieval mode, the retriever (either
of BM25 or GPT-Index) first retrieves the most up-to-date API documentation stored in the API
Database. This is then concatenated to the user prompt along with the message Use this API
documentation for reference: before feeding it to Gorilla. The output of Gorilla is an API to
be invoked. Besides the concatenation as described, we do NO further prompt tuning in our system.
While we do have a system to execute these APIs, that is not a focus of this paper.

3.3 Verifying APIs

Inductive program synthesis, where a program is synthesized to satisfy test cases, has found success
in several avenues [4, 25]. However, test cases fall short when evaluating API calls, as it is often
hard to verify the semantic correctness of the code. For example, consider the task of classifying an
image. There are over 40 different models that can be used for the task. Even if we were to narrow
down to a single family of Densenet, there are four different configurations possible. Hence, there
exist multiple correct answers and it is hard to tell if the API being used is functionally equivalent to
the reference API by unit tests. Thus, to evaluate the performance of our model, we compare their
functional equivalence using the dataset we collected. To trace which API in the dataset is the LLM
calling, we adopt the AST tree-matching strategy. Since we only consider one API call in this paper,
checking if the AST of the candidate API call is a sub-tree of the reference API call reveals which
API is being used in the dataset.

Identifying and even defining hallucinations can be challenging. We use the AST matching process
to directly identify the hallucinations. We define a hallucination as an API call that is not a sub-tree
of any API in the database – invoking an entirely imagined tool. This form of hallucination is distinct
from invoking an API incorrectly which we instead define as an error.

AST Sub-Tree Matching We perform AST sub-tree matching to identify which API in our dataset
is the LLM calling. Since each API call can have many arguments, we need to match on each of
these arguments. Further, since, Python allows for default arguments, for each API, we define which
arguments to match in our database. For example, we check repo_or_dir and model arguments
in our function call. In this way, we can easily check if the argument matches the reference API or
not. Please refer to Fig. 4 for more details. In this example, Gorilla returns a torch API call. We
first build the tree, and verify that it matches a subtree in our dataset along nodes torch.hub.load,
pytorch/vision, and densenet121. But, we don’t check for match along leaf node pretrained
= True since that is an optional python argument.

5

Figure 4: AST Sub-Tree Matching to evaluate API calls. On the left is an API call returned by Gorilla. We
first build the associated API tree. We then compare this to our dataset, to see if the API dataset has a subtree
match. In the above example, the matching subtree is highlighted in brown, signifying that the API call is indeed
correct. Pretrained=True is an optional argument.

4 Evaluation

We carried out an array of experiments on our collected dataset, benchmarking our model Gorilla
with other models, and exploring how different retrieval methods may impact the performance of
the model in making API calls. We then demonstrate that Gorilla can easily adapt to test-time
changes in API documentation. In addition, we assess Gorilla’s ability to reason about API calls
under constraints. Lastly, we examined how integrating different retrieval methods during training
influences the model’s final performance.

Baselines Primarily, we compare Gorilla with state-of-the-art language models in a zero-shot setting.
The models under consideration include: GPT-4 by OpenAI, we use the gpt-4-0314 checkpoint;
GPT-3.5-turbo with the gpt-3.5-turbo-0301 checkpoint, both of which are RLHF-tuned model
specifically designed for conversation; Claude with claude-v1 checkpoint, a language model by
Anthropic, renowned for its lengthy context capabilities; LLaMA-7B, a large language model by
Meta and the finest open-source model to date.

Retrievers The term Zero-shot (abbreviated as 0-shot in tables) refers to scenarios where no
retriever is used. The sole input to the model is the user’s natural language prompt. For BM25, we
consider each API as a separate document. During retrieval, we use the user’s query to search the
index and fetch the most relevant (top-1) API. This API is concatenated with the user’s prompt
to query the LLMs. Similarly, GPT-Index refers to the retrieval model text-davinci-003 from
OpenAI. Like BM25, each API call is indexed as an individual document, and the most relevant
document, given a user query, is retrieved and appended to the user prompt. Lastly, we include
an Oracle retriever, which serves two purposes: first, to identify the potential for performance
improvement through more efficient retrievers, and second, to assist users who know which API
to use but may need to help invoking it. In all cases, when a retriever is used, it is appended to
the user’s prompt as follows: <user_prompt> Use this API documentation for reference:
<retrieved_API_doc_JSON>. The dataset for these evaluations is detailed in Sec 3. We emphasize
that we have maintained a holdout test set on which we report our findings. The holdout test set was
created by dividing the self-instruct dataset’s instruction, API pairs into training and testing sets.

4.1 AST Accuracy on API call

We first demonstrate the results for the AST accuracy for different models. We present the results
in Tab. 1. We test each model for different retriever settings defined above. We report the overall
accuracy, the error by hallucination and the error by selecting wrong API call. Note that for TorchHub
and TensorHub, we evaluate all the models using AST tree accuracy score. However, for HuggingFace,

6

torchutilshubTensormodel_zooloadrepo: pytorch/visionmodel: densenet121model: densenet161model: densenet201pretrained: Truepretrained: Falserepo: huggingface/pytorch-transformerstorch.hub.load(’pytorch/vision:v0.10.0’,  ‘densenet121’, pretrained=True)torchhubloadpytorch/visiondensenet121pretrained = TrueFigure 5: Accuracy with GPT-retriever. Gorilla outperforms on Torch Hub and Hugging-Face while matching
performance on Tensorflow Hub for all existing SoTA LLMs - closed source, and open source.

since the dataset is not exhaustive, for all the models except Gorilla, we only check if they can provide
the correct domain names. So this problem reduces to picking one of the multiple choices.

Finetuning without Retrieval
In Tab. 1 we show that lightly fine-tuned Gorilla gets the state-of-
the-art performance zero-shot over all the models, 20.43% better than GPT-4 and 10.75% better than
ChatGPT. When compared to other open-source models LLAMA, the improvement is as big as 83%.
his suggests quantitatively, that finetuning is better than retrieval, at-least in our scope.

In addition, we found that finetuning without retriever and putting ground truth retriever in evaluation
time rarely helps the performance: 0.88% worse in TensorHub and 0.97% better in HuggingFace. If
we put BM25 or GPT-Index as retriever, results will be significantly dropped: 21.50% in Torch Hub
and 47.57% in HuggingFace. The result illustrates that adding a non-optimal retriever at test time
will sometime misguide the model and result in more errors. We will discuss an interesting ablation
on how finetuning with the retriever will help the performance in the next paragraph.

Table 1: Evaluating LLMs on Torch Hub, HuggingFace, and Tensorflow Hub APIs

LLM (retriever)

LLAMA (0-shot)
GPT-3.5 (0-shot)
GPT-4 (0-shot)
Claude (0-shot)
Gorilla (0-shot)

LLAMA (BM-25)
GPT-3.5 (BM-25)
GPT-4 (BM-25)
Claude (BM-25)
Gorilla (BM-25)

LLAMA (GPT-Index)
GPT-3.5 (GPT-Index)
GPT-4 (GPT-Index)
Claude (GPT-Index)
Gorilla (GPT-Index)

LLAMA (Oracle)
GPT-3.5 (Oracle)
GPT-4 (Oracle)
Claude (Oracle)
Gorilla (Oracle)

overall ↑

TorchHub
hallu ↓

0
48.38
38.70
18.81
59.13

8.60
38.17
35.48
39.78
40.32

14.51
60.21
59.13
60.21
61.82

16.12
66.31
66.12
63.44
67.20

100
18.81
36.55
65.59
6.98

76.88
6.98
11.29
5.37
4.30

75.8
1.61
1.07
3.76
0

79.03
1.60
0.53
3.76
0

err ↓

0
32.79
24.7
15.59
33.87

14.51
54.83
53.22
54.83
55.37

9.67
38.17
39.78
36.02
38.17

4.83
32.08
33.33
32.79
32.79

HuggingFace

overall ↑

hallu ↓

0.00
16.81
19.80
6.19
71.68

3.00
17.26
16.48
14.60
17.03

10.18
29.08
44.58
41.37
47.46

17.70
89.71
85.07
77.21
91.26

97.57
35.73
37.16
77.65
10.95

77.99
8.30
15.93
15.82
6.42

75.66
7.85
11.18
18.81
8.19

77.10
6.64
10.62
19.58
7.08

err ↓

2.43
47.46
43.03
16.15
17.36

19.02
74.44
67.59
69.58
76.55

14.20
44.80
44.25
39.82
44.36

5.20
3.65
4.31
3.21
1.66

TensorFlow Hub

overall ↑

hallu ↓

0
41.75
18.20
9.19
83.79

8.90
54.16
34.01
35.18
41.89

15.62
65.59
43.94
55.62
64.96

12.55
95.03
55.91
74.74
94.16

100
47.88
78.65
88.46
5.40

77.37
3.64
37.08
21.16
2.77

77.66
3.79
31.53
16.20
2.33

87.00
0.29
37.95
21.60
1.89

err ↓

0
10.36
3.13
2.33
10.80

13.72
42.18
28.90
43.64
55.32

6.71
30.50
24.52
28.17
32.70

0.43
4.67
6.13
3.64
3.94

Finetuning with Retrieval We now discuss an interesting experiment on how finetuning language
with retriever incorporated is helping the performance. The settings for this experiment are finetuning
the base LLAMA with the prompt (instruction generated), reference API document (from golden-
truth oracle), and the example output generated by GPT-4. In Tab. 2, we can see that incorporating
ground truth retriever in the finetuning pipeline achieves significantly better results 12.37% better
than training without retriever in Torch Hub and 23.46% better in HuggingFace. However, we found
that at evaluation time, current retrievers still have a big gap between the ground truth retriever: using
GPT-Index at evaluation results in 29.20% accuracy degradation, and using BM25 results in a 52.27%
accuracy degradation. Nevertheless, we can still conclude that with a better retriever, finetuning

7

LLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy14.5160.2159.1360.2161.82Torch Hub with GPT-RetrieverLLAMAGPT-3.5GPT-4ClaudeGorillaModel02040608010010.1747.3444.5741.3747.45HuggingFace with GPT-RetrieverLLAMAGPT-3.5GPT-4ClaudeGorillaModel02040608010015.6265.5943.9455.6264.96Tensorflow Hub with GPT-RetrieverFigure 6: Gorilla’s retriever–aware training enables it to react to changes in the APIs. The second column
demonstrates changes in model upgrading FCN’s ResNet–50 backbone to ResNet–101. The third column demon-
strate changes in model registry from pytorch/vision to NVIDIA/DeepLearningExamples:torchhub

with retriever is still a better method to adopt while in another scenario, when a good retriever is not
available, zero-shot finetuning might be the preferred choice.

Table 2: Comparison of retrieval techniques

Gorilla without Retriever

Gorilla with Oracle retriever

zero-shot

BM25

GPT-Index

Oracle

zero-shot

BM25

GPT-Index

Oracle

Torch Hub (overall) ↑
HuggingFace (overall) ↑
TensorHub (overall) ↑

Torch Hub (Hallu) ↓
HuggingFace (Hallu) ↓
TensorHub (Hallu) ↓

59.13
71.68
83.79

6.98
10.95
5.40

37.63
11.28
34.30

11.29
46.46
20.43

60.21
28.10
52.40

4.30
41.48
19.70

54.83
45.58
82.91

15.59
52.77
13.28

0
0
0

100
99.67
100

40.32
17.04
41.89

4.30
6.42
2.77

61.82
47.46
64.96

0
8.19
2.33

67.20
91.26
94.16

0
7.08
1.89

Hallucination with LLM One phenomenon we observe is that zero-shot prompting with
LLMs (GPT-4/GPT-3.5) to call APIs results in dire hallucination errors. These errors, while
diverse, commonly manifest in erroneous behavior such as the model invoking the "Auto-
Model.from_pretrained(dir_name)" command with arbitrary GitHub repository names. Surprisingly,
we also found that in TorchHub, HuggingFace and TensorFlow Hub, GPT-3.5 has less hallucination
errors than GPT-4. This finding is also consistent for the settings when various retrieving methods are
provided: 0-shot, BM25, GPT-Index and the oracle. This might suggest that RLHF plays a central
role in turning the model to be truthful. Additional examples and discussion are in Appendix.

4.2 Test-Time Documentation Change

The rapidly evolving nature of API documentation presents a significant challenge for the application
of LLMs in this field. These documents are often updated at a frequency that outpaces the re-
training or fine-tuning schedule of LLMs, making these models particularly brittle to changes in the
information they are designed to process. This mismatch in update frequency can lead to a decline in
the utility and reliability of LLMs over time.

However, with the introduction of Gorilla’s retriever-aware training, we can readily adapt to changes
in API documentation. This novel approach allows the model to remain updated and relevant, even as
the API documentation it relies on undergoes modifications. This is a pivotal advancement in the
field, as it ensures that the LLM maintains its efficacy and accuracy over time, providing reliable
outputs irrespective of changes in the underlying documentation.

For instance, consider the scenario illustrated in Figure 6, where the training of Gorilla has al-
lowed it to react effectively to changes in APIs. This includes alterations such as upgrading
the FCN’s ResNet-50 backbone to ResNet-101, as demonstrated in the second column of the
figure. This capability ensures that the LLM remains relevant and accurate even as the under-
lying models and systems undergo upgrades and improvements. Furthermore, the third column
in Figure 6 shows how Gorilla adapts to changes in the model registry from pytorch/vision to
NVIDIA/DeepLearningExamples:torchhub. This reflects the model’s ability to adjust to shifts in
API sources, which is vital as organizations may change their preferred model registries over time.

In summary, Gorilla’s ability to adapt to test-time changes in API documentation offers numerous
benefits. It maintains its accuracy and relevance over time, adapts to the rapid pace of updates in

8

USER: I want to automatically remove the background from an input image <Retrieval: ..fcn_resnet101..>GORILLA:     api_call:         “torch.hub.load('pytorch/vision', 'fcn_resnet101', pretrained=True)”USER: I want to automatically remove the background from an input image. <Retrieval: ..NVIDIA/DeepLearningExamples:torchhub..>GORILLA:    api_call:         “torch.hub.load(‘NVIDIA / DeepLearningExamples:torchhub ', 'fcn_resnet50', pretrained=True)”USER: I want to automatically remove the background from an input image. <Retrieval:  ..fcn_resnet50..>GORILLA:     api_call:         “torch.hub.load('pytorch/vision', 'fcn_resnet50', pretrained=True)” Default ResponseUpdate the modelUpdate the model repositoryAPI documentation, and adjusts to modifications in underlying models and systems. This makes it a
robust and reliable tool for API calls, significantly enhancing its practical utility.

4.3 API Call with Constraints

We now focus on the language model’s capability of understanding constraints. For any given task,
which API call to invoke is typically a tradeoff between a multitude of factors. In the case of RESTFul
APIs, it could be the cost of each invocation ($), and the latency of response (ms), among others.
Similarly, within the scope of ML APIs, it is desirable for Gorilla to respect constraints such as
accuracy, number of learnable parameters in the model, the size on disk, peak memory consumption,
FLOPS, etc. We present the underlying ablation study evaluating the ability of different models
in zero-shot and with retrievers settings to respect a given accuracy constraint. This setting is best
understood with an example. If the user were to ask for an Image classification model that achieves at
least 80% top-1 accuracy on the Imagenet dataset, then while both are classification models hosted by
Torch Hub, ResNeXt-101 32x16d with a top-1 accuracy of 84.2% would be the right model whose
API to call and not, say, MobileNetV2 which has a top-1 accuracy of 71.88%.

Table 3: Evaluating LLMs on constraint-aware API invocations

GPT-3.5

GPT-4

Gorilla

0-shot BM25 GPT-Index Oracle

0-shot BM25 GPT-Index Oracle

0-shot BM25 GPT-Index Oracle

Torch Hub (overall)
Torch Hub (Hallu)
Torch Hub (err)

Accuracy const

73.94
19.01
7.04

43.66

62.67
30.98
6.33

33.80

81.69
14.78
3.52

33.09

80.98
14.08
4.92

69.01

62.67
15.49
21.83

43.66

56.33
27.46
16.19

29.57

71.11
14.08
14.78

29.57

69.01
9.15
21.83

59.15

71.83
19.71
8.45

47.88

57.04
39.43
3.52

30.28

71.83
26.05
2.11

26.76

78.16
16.90
4.92

67.60

LLAMA

Claude

0-shot BM25 GPT-Index Oracle

0-shot BM25 GPT-Index Oracle

Torch Hub (overall)
Torch Hub (Hallu)
Torch Hub (err)

Accuracy const

0
100
0

0

8.45
91.54
0

6.33

11.97
88.02
0

3.52

19.71
78.87
1.4

17.60

29.92
67.25
2.81

17.25

81.69
16.19
2.11

29.57

82.39
15.49
2.11

31.69

81.69
13.38
4.92

69.71

For Table 3, we filtered a subset of the Torch Hub dataset that had accuracy defined for at least one-
dataset in its model card (65.26% of TorchHub dataset in Table 1). We notice that with constraints,
understandably, the accuracy drops across all models, with and without a retriever. Gorilla is able
to match performance with the best-performing model GPT-3.5 when using retrievals (BM25, GPT-
Index) and has the highest accuracy in the Zero-shot case. This highlights Gorilla’s ability to navigate
APIs while considering the trade-offs between different constraints.

5 Conclusion

LLMs are swiftly gaining popularity across diverse domains. In our study, we spotlight techniques
designed to enhance the LLM’s ability to accurately identify the appropriate API for a specific task—a
significant but often overlooked aspect in the advancement of this technology. Since APIs function as
a universal language enabling diverse systems to communicate effectively, their correct usage can
boost the ability of LLMs to interact with tools in the wider world. In this paper, we propose Gorilla,
a new novel pipeline for finetuning LLMs to call APIs. The finetuned model’s performance surpasses
prompting the state-of-the-art LLM (GPT-4) in three massive datasets we collected. Gorilla generates
reliable API calls to ML models without hallucination, demonstrates an impressive capability to adapt
to test-time API usage changes, and can satisfy constraints while picking APIs.

6 Limitations & Social Impacts

With the goal of wanting to have a challenging dataset, we chose ML APIs, given their functional
similarity. The potential downside to APIs that focus on the ML domain, is their propensity to
produce biased predictions if trained on skewed data, potentially disadvantaging certain sub-groups.
To counter this concern and foster a deeper understanding of these APIs, we are releasing our
extensive dataset, consisting of over 11,000 instruction-API pairs. This resource will serve the wider
community as a valuable tool for studying and benchmarking existing APIs, contributing to a more
fair and optimized usage of machine learning.

9

7 Acknowledgement

This research is supported in part by gifts to UC Berkley Sky Computing Lab from Astronomer,
Google, IBM, Intel, Lacework, Microsoft, Nexla, Samsung SDS, Uber, and VMware.

References

[1] Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., David, B., Finn, C., Gopalakrishnan,
K., Hausman, K., Herzog, A., et al. (2022). Do as i can, not as i say: Grounding language in
robotic affordances. arXiv preprint arXiv:2204.01691.

[2] Andor, D., He, L., Lee, K., and Pitler, E. (2019). Giving bert a calculator: Finding operations

and arguments with reading comprehension. arXiv preprint arXiv:1909.00109.

[3] Anthropic, h.-c. (2022). Claude.

[4] Bavishi, R., Lemieux, C., Fox, R., Sen, K., and Stoica, I. (2019). Autopandas: neural-
backed generators for program synthesis. Proceedings of the ACM on Programming Languages,
3(OOPSLA):1–27.

[5] Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A.,
Shyam, P., Sastry, G., Askell, A., et al. (2020). Language models are few-shot learners. Advances
in neural information processing systems, 33:1877–1901.

[6] Bubeck, S., Chandrasekaran, V., Eldan, R., Gehrke, J., Horvitz, E., Kamar, E., Lee, P., Lee, Y. T.,
Li, Y., Lundberg, S., et al. (2023). Sparks of artificial general intelligence: Early experiments with
gpt-4. arXiv preprint arXiv:2303.12712.

[7] Chen, M., Tworek, J., Jun, H., Yuan, Q., Pinto, H. P. d. O., Kaplan, J., Edwards, H., Burda, Y.,
Joseph, N., Brockman, G., et al. (2021). Evaluating large language models trained on code. arXiv
preprint arXiv:2107.03374.

[8] Chen, X., Lin, M., Schärli, N., and Zhou, D. (2023). Teaching large language models to

self-debug. arXiv preprint arXiv:2304.05128.

[9] Chiang, W.-L., Li, Z., Lin, Z., Sheng, Y., Wu, Z., Zhang, H., Zheng, L., Zhuang, S., Zhuang, Y.,
Gonzalez, J. E., Stoica, I., and Xing, E. P. (2023). Vicuna: An open-source chatbot impressing
gpt-4 with 90%* chatgpt quality.

[10] Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts, A., Barham, P., Chung,
H. W., Sutton, C., Gehrmann, S., et al. (2022). Palm: Scaling language modeling with pathways.
arXiv preprint arXiv:2204.02311.

[11] Chung, H. W., Hou, L., Longpre, S., Zoph, B., Tay, Y., Fedus, W., Li, E., Wang, X., Dehghani,
M., Brahma, S., et al. (2022). Scaling instruction-finetuned language models. arXiv preprint
arXiv:2210.11416.

[12] Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert, M., Tworek,
J., Hilton, J., Nakano, R., et al. (2021). Training verifiers to solve math word problems. arXiv
preprint arXiv:2110.14168.

[13] Devlin, J., Uesato, J., Bhupatiraju, S., Singh, R., Mohamed, A.-r., and Kohli, P. (2017). Robust-
fill: Neural program learning under noisy i/o. In International conference on machine learning,
pages 990–998. PMLR.

[14] Gao, L., Madaan, A., Zhou, S., Alon, U., Liu, P., Yang, Y., Callan, J., and Neubig, G. (2022).

Pal: Program-aided language models. arXiv preprint arXiv:2211.10435.

[15] Iyer, S., Lin, X. V., Pasunuru, R., Mihaylov, T., Simig, D., Yu, P., Shuster, K., Wang, T., Liu, Q.,
Koura, P. S., et al. (2022). Opt-iml: Scaling language model instruction meta learning through the
lens of generalization. arXiv preprint arXiv:2212.12017.

10

[16] Jain, N., Vaidyanath, S., Iyer, A., Natarajan, N., Parthasarathy, S., Rajamani, S., and Sharma,
R. (2022). Jigsaw: Large language models meet program synthesis. In Proceedings of the 44th
International Conference on Software Engineering, pages 1219–1231.

[17] Kim, G., Baldi, P., and McAleer, S. (2023). Language models can solve computer tasks. arXiv

preprint arXiv:2303.17491.

[18] Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., and Iwasawa, Y. (2022). Large language models

are zero-shot reasoners. arXiv preprint arXiv:2205.11916.

[19] Komeili, M., Shuster, K., and Weston, J. (2021). Internet-augmented dialogue generation. arXiv

preprint arXiv:2107.07566.

[20] Lachaux, M.-A., Roziere, B., Chanussot, L., and Lample, G. (2020). Unsupervised translation

of programming languages. arXiv preprint arXiv:2006.03511.

[21] Lazaridou, A., Gribovskaya, E., Stokowiec, W., and Grigorev, N. (2022). Internet-augmented
language models through few-shot prompting for open-domain question answering. arXiv preprint
arXiv:2203.05115.

[22] Li, R., Allal, L. B., Zi, Y., Muennighoff, N., Kocetkov, D., Mou, C., Marone, M., Akiki, C., Li, J.,
Chim, J., et al. (2023). Starcoder: may the source be with you! arXiv preprint arXiv:2305.06161.

[23] Li, Y., Choi, D., Chung, J., Kushman, N., Schrittwieser, J., Leblond, R., Eccles, T., Keeling,
J., Gimeno, F., Dal Lago, A., et al. (2022). Competition-level code generation with alphacode.
Science, 378(6624):1092–1097.

[24] Liang, Y., Wu, C., Song, T., Wu, W., Xia, Y., Liu, Y., Ou, Y., Lu, S., Ji, L., Mao, S., et al. (2023).
Taskmatrix. ai: Completing tasks by connecting foundation models with millions of apis. arXiv
preprint arXiv:2303.16434.

[25] Menon, A., Tamuz, O., Gulwani, S., Lampson, B., and Kalai, A. (2013). A machine learning
framework for programming by example. In International Conference on Machine Learning,
pages 187–195. PMLR.

[26] Nakano, R., Hilton, J., Balaji, S., Wu, J., Ouyang, L., Kim, C., Hesse, C., Jain, S., Kosaraju, V.,
Saunders, W., et al. (2021). Webgpt: Browser-assisted question-answering with human feedback.
arXiv preprint arXiv:2112.09332.

[27] Nijkamp, E., Hayashi, H., Xiong, C., Savarese, S., and Zhou, Y. (2023). Codegen2: Lessons for

training llms on programming and natural languages. arXiv preprint arXiv:2305.02309.

[28] Nijkamp, E., Pang, B., Hayashi, H., Tu, L., Wang, H., Zhou, Y., Savarese, S., and Xiong, C.
(2022). Codegen: An open large language model for code with multi-turn program synthesis.
arXiv preprint arXiv:2203.13474.

[29] OpenAI (2023). Gpt-4 technical report.

[30] OpenAI and https://openai.com/blog/chatgpt (2022). Chatgpt.

[31] Sanh, V., Webson, A., Raffel, C., Bach, S. H., Sutawika, L., Alyafeai, Z., Chaffin, A., Stiegler,
A., Scao, T. L., Raja, A., et al. (2021). Multitask prompted training enables zero-shot task
generalization. arXiv preprint arXiv:2110.08207.

[32] Scao, T. L., Fan, A., Akiki, C., Pavlick, E., Ili´c, S., Hesslow, D., Castagné, R., Luccioni, A. S.,
Yvon, F., Gallé, M., et al. (2022). Bloom: A 176b-parameter open-access multilingual language
model. arXiv preprint arXiv:2211.05100.

[33] Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N.,
and Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. arXiv
preprint arXiv:2302.04761.

[34] Schick, T. and Schütze, H. (2020). Exploiting cloze questions for few shot text classification

and natural language inference. arXiv preprint arXiv:2001.07676.

11

[35] Shen, Y., Song, K., Tan, X., Li, D., Lu, W., and Zhuang, Y. (2023). Hugginggpt: Solving ai

tasks with chatgpt and its friends in huggingface. arXiv preprint arXiv:2303.17580.

[36] Shinn, N., Labash, B., and Gopinath, A. (2023). Reflexion: an autonomous agent with dynamic

memory and self-reflection. arXiv preprint arXiv:2303.11366.

[37] Shuster, K., Xu, J., Komeili, M., Ju, D., Smith, E. M., Roller, S., Ung, M., Chen, M., Arora, K.,
Lane, J., et al. (2022). Blenderbot 3: a deployed conversational agent that continually learns to
responsibly engage. arXiv preprint arXiv:2208.03188.

[38] Taori, R., Gulrajani, I., Zhang, T., Dubois, Y., Li, X., Guestrin, C., Liang, P., and Hashimoto,
T. B. (2023). Stanford alpaca: An instruction-following llama model. https://github.com/
tatsu-lab/stanford_alpaca.

[39] Thoppilan, R., De Freitas, D., Hall, J., Shazeer, N., Kulshreshtha, A., Cheng, H.-T., Jin, A.,
Bos, T., Baker, L., Du, Y., et al. (2022). Lamda: Language models for dialog applications. arXiv
preprint arXiv:2201.08239.

[40] Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.-A., Lacroix, T., Rozière, B.,
Goyal, N., Hambro, E., Azhar, F., et al. (2023). Llama: Open and efficient foundation language
models. arXiv preprint arXiv:2302.13971.

[41] Vemprala, S., Bonatti, R., Bucker, A., and Kapoor, A. (2023). Chatgpt for robotics: Design

principles and model abilities. 2023.

[42] Wang, Y., Kordi, Y., Mishra, S., Liu, A., Smith, N. A., Khashabi, D., and Hajishirzi, H.
(2022a). Self-instruct: Aligning language model with self generated instructions. arXiv preprint
arXiv:2212.10560.

[43] Wang, Y., Mishra, S., Alipoormolabashi, P., Kordi, Y., Mirzaei, A., Naik, A., Ashok, A.,
Dhanasekaran, A. S., Arunkumar, A., Stap, D., et al. (2022b). Super-naturalinstructions: General-
ization via declarative instructions on 1600+ nlp tasks. In Proceedings of the 2022 Conference on
Empirical Methods in Natural Language Processing, pages 5085–5109.

[44] Wei, J., Wang, X., Schuurmans, D., Bosma, M., Chi, E., Le, Q., and Zhou, D. (2022). Chain of
thought prompting elicits reasoning in large language models. arXiv preprint arXiv:2201.11903.

[45] Xu, F. F., Alon, U., Neubig, G., and Hellendoorn, V. J. (2022). A systematic evaluation of large
language models of code. In Proceedings of the 6th ACM SIGPLAN International Symposium on
Machine Programming, pages 1–10.

[46] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., and Cao, Y. (2022). React:

Synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629.

[47] Zeng, A., Liu, X., Du, Z., Wang, Z., Lai, H., Ding, M., Yang, Z., Xu, Y., Zheng, W., Xia, X.,
et al. (2022). Glm-130b: An open bilingual pre-trained model. arXiv preprint arXiv:2210.02414.

[48] Zhang, S., Roller, S., Goyal, N., Artetxe, M., Chen, M., Chen, S., Dewan, C., Diab, M., Li,
X., Lin, X. V., et al. (2022). Opt: Open pre-trained transformer language models. arXiv preprint
arXiv:2205.01068.

12

8 Appendix

8.1 Dataset Details

Our dataset is multi-faceted, comprising three distinct domains: Torch Hub, Tensor Hub, and
HuggingFace. Each entry within this dataset is rich in detail, carrying critical pieces of information
that further illuminate the nature of the data. Delving deeper into the specifics of each domain, Torch
Hub provides 95 APIs. The second domain, Tensor Hub, is more expansive with a total of 696 APIs.
Finally, the most extensive of them all, HuggingFace, comprises 925 APIs.

To enhance the value and utility of our dataset, we’ve undertaken an additional initiative. With
each API, we have generated a set of 10 unique instructions. These instructions, carefully crafted
and meticulously tailored, serve as a guide for both training and evaluation. This initiative ensures
that every API is not just represented in our dataset, but is also comprehensively understood and
effectively utilizable.

In essence, our dataset is more than just a collection of APIs across three domains. It is a compre-
hensive resource, carefully structured and enriched with added layers of guidance and evaluation
parameters.

Domain Classification The unique domain names encompassed within our dataset are illustrated in
Figure 7. The dataset consists of three sources with a diverse range of domains: Torch Hub houses 6
domains, Tensor Hub accommodates a much broader selection with 57 domains, while HuggingFace
incorporates 37 domains. To exemplify the structure and nature of our dataset, we invite you to refer
to the domain names represented in Figure 8.

API Call Task In this task, we test the model’s capability to generate a single line of code, either in
a zero-shot fashion or by leveraging an API reference. Primarily designed for evaluation purposes,
this task effectively gauges the model’s proficiency in identifying and utilizing the appropriate API
call.

API Provider Component This facet relates to the provision of the programming language. In this
context, the API provider plays a vital role as it serves as a foundation upon which APIs are built and
executed.

Explanation Element This component offers valuable insights into the rationale behind the usage of
a particular API, detailing how it aligns with the prescribed requirements. Furthermore, when certain
constraints are imposed, this segment also incorporates those limitations. Thus, the explanation
element serves a dual purpose, offering a deep understanding of API selection, as well as the
constraints that might influence such a selection. This balanced approach ensures a comprehensive
understanding of the API usage within the given context.

Code Example code for accomplishing the task. We de-prioritize this as we haven’t tested the
execution result of the code. We leave this for future works, but make this data available in-case
others want to build on it.

8.2 Gorilla Details

We provide all the training details for Gorilla in this section. This includes how we divide up the
training, evaluation dataset, training hyperparameters for Gorilla.

Data For HuggingFace, we devise the entire dataset into 90% training and 10% evaluation. For
Torch Hub and Tensor Hub, we devise the data in to 80% training and 20% testing.

Training We train Gorillafor 5 epochs with the 2e-5 learning rate with cosine decay. The details
are provide in Tab. 4. We finetune it on 8xA100 with 40G memory each.

13

Torch Hub domain names: Classification, Semantic Segmentation, Object Detection, Audio
Separation, Video Classification, Text-to-Speech

Tensor Hub domain names:
text-sequence-alignment, text-embedding, text-language-
model, text-preprocessing, text-classification, text-generation, text-question-answering, text-
retrieval-question-answering, text-segmentation, text-to-mel, image-classification, image-
feature-vector, image-object-detection, image-segmentation, image-generator, image-pose-
detection, image-rnn-agent, image-augmentation, image-classifier, image-style-transfer,
image-aesthetic-quality, image-depth-estimation, image-super-resolution, image-deblurring,
image-extrapolation, image-text-recognition, image-dehazing, image-deraining, image-
enhancemenmt, image-classification-logits, image-frame-interpolation, image-text-detection,
image-denoising,
image-others, video-classification, video-feature-extraction, video-
generation, video-audio-text, video-text, audio-embedding, audio-event-classification, audio-
command-detection, audio-paralinguists-classification, audio-speech-to-text, audio-speech-
synthesis, audio-synthesis, audio-pitch-extraction

HuggingFace domain names: Multimodal Feature Extraction, Multimodal Text-to-Image,
Multimodal Image-to-Text, Multimodal Text-to-Video, Multimodal Visual Question An-
swering, Multimodal Document Question Answer, Multimodal Graph Machine Learning,
Computer Vision Depth Estimation, Computer Vision Image Classification, Computer Vision
Object Detection, Computer Vision Image Segmentation, Computer Vision Image-to-Image,
Computer Vision Unconditional Image Generation, Computer Vision Video Classification,
Computer Vision Zero-Shor Image Classification, Natural Language Processing Text Classi-
fication, Natural Language Processing Token Classification, Natural Language Processing
Table Question Answering, Natural Language Processing Question Answering, Natural Lan-
guage Processing Zero-Shot Classification, Natural Language Processing Translation, Natural
Language Processing Summarization, Natural Language Processing Conversational, Natural
Language Processing Text Generation, Natural Language Processing Fill-Mask, Natural Lan-
guage Processing Text2Text Generation, Natural Language Processing Sentence Similarity,
Audio Text-to-Speech, Audio Automatic Speech Recognition, Audio Audio-to-Audio, Audio
Audio Classification, Audio Voice Activity Detection, Tabular Tabular Classification, Tabu-
lar Tabular Regression, Reinforcement Learning Reinforcement Learning, Reinforcement
Learning Robotics

Figure 7: Domain names: Domain names with the three dataset. Tensor Hub is the smallest dataset
while the other two hubs contain many more models.

Table 4: Hyperparameters for training Gorilla

Hyperparameter Name

learning rate
batch size
epochs
warmup ratio
weight decay
max seq length

Value

2e-5
64
5
0.03
0
2048

8.3 Performance Comparison

We provide a full comparison of each model’s performance in this section. In Fig 10 and Fig. 11, the
full set of comparisons is provided. We see that especially in zero-shot case, Gorilla surpasses the
GPT-4 and GPT-3.5 by a large margin. The GPT-4 and GPT-3.5 gets around 40% accuracy in Torch
Hub and Tensor Hub, which are two structured API calls. Compared to that, HuggingFace is a more
flexible and diverse Hub, as a result, the performance on HuggingFace is not as competitive.

14

### User: Our customer is a zoo and we want to help them detect movement of different
animals. Write a python program in 1 to 2 lines to call API in TensorFlowHub.
### Assistant:
<domain>: image-object-detection,
<api_call>: detector = hub.load(’https://tfhub.dev/google/openimages_v4/ssd_mobilenet_v2/1’),
<api_provider>: TensorFlow Hub,
<explanation>: This API call loads the pre-trained Single Shot Detector (SSD) MobileNet
V2 model from TensorFlow Hub, which has been trained on the Open Images v4 dataset.
This model is used for object detection in images. Once loaded, you can pass an image (and
an optional score threshold for detection confidence) to the detector to get back the detected
objects along with their bounding boxes, class labels, and associated confidence scores.
<code>: import tensorflow as tf; import tensorflow_hub as hub; # Load the SSD MobileNet V2
model; detector = hub.load(’https://tfhub.dev/google/openimages_v4/ssd_mobilenet_v2/1’);
# Use the model to detect objects in an image (assuming ’image’ is a TensorFlow tensor
representing your image); result = detector(image, score_threshold=0.5)

PyTorch,

framework:

{domain: Object Detection,

### User: I am an engineer at Uber and I need to find a API that can classify pedestrians,
cars, etc. from an image of the scene. Write a python program in 1 to 2 lines to call API in
TorchHub.
<Reference API>:
function-
Traffic Object Detection, Drivable Area Segmentation, Lane Detection,
ality:
torch.hub.load(repo_or_dir=’datvuthanh/hybridnets’,
api_name: HybridNets, api_call:
model=’hybridnets’, pretrained=True), api_arguments:
repo_or_dir, model, pretrained,
python_environment_requirements: Python>=3.7, PyTorch>=1.10, example_code: ’import
torch; model = torch.hub.load(’datvuthanh/hybridnets’, ’hybridnets’, pretrained=True); img
= torch.randn(1,3,640,384); features, regression, classification, anchors, segmentation =
model(img), performance: dataset: [name: BDD100K, accuracy: Traffic Object Detection:
Recall (%): 92.8, mAP@0.5 (%): 77.3, Drivable Area Segmentation: Drivable mIoU (%):
90.5, Lane Line Detection: Accuracy (%): 85.4, Lane Line IoU (%): 31.6], description:
HybridNets is an end2end perception network for multi-tasks. Our work focused on traffic
object detection, drivable area segmentation and lane detection. HybridNets can run real-time
on embedded systems, and obtains SOTA Object Detection, Lane Detection on BDD100K
Dataset.}
### Assistant:
<domain>: Object Detection, <api_call>: model = torch.hub.load(’datvuthanh/hybridnets’,
’hybridnets’, pretrained=True),
<api_provider>: PyTorch,
<explanation>: Load the pretrained HybridNets model for object detection from PyTorch
Hub to classify pedestrians, cars, etc. in an image of the scene,
<code>: import torch; model = torch.hub.load(’datvuthanh/hybridnets’, ’hybridnets’, pre-
trained=True)

Figure 8: Example of the Dataset: Two examples of the dataset, the above one is zero-shot (without
information retrievers) and the bottom one is with information retriever.

15

generate_video = pipeline("text-to-video", model="your_model_name")

=

vqa
tokenizer="microsoft/clip-vqa-base")

pipeline("visual-question-answering",

model="microsoft/clip-vqa-base",

depth_estimator = pipeline("depth-estimation", model="intel-isl/MiDaS", tokenizer="intel-
isl/MiDaS")

Figure 9: Hallucination Examples: GPT-4 incurs serious hallucination errors in HuggingFace. We
show a couple of examples in the figure.

8.3.1 Evaluation

For ease of evaluation, we manually cleaned up the dataset to make sure each API call domain only
contains the valid call in the form of:

API_name(API_arg1, API_arg2, ..., API_argk)

Our framework allows the user to define any combination of the arguments to check. For Torch
Hub, we check for the API name torch.hub.load with arguments repo_or_dir and model. For
Tensor Hub, we check API name hub.KerasLayer and hub.load with argument handle. For
HuggingFace, since there are many API function names, we don’t list all of them here. One specific
note is that we require the pretrained_model_name_or_path argument for all the calls except
for pipeline. For pipeline, we don’t require the pretrained_model_name_or_path argument
since it automatically select a model for you once task is specified.

8.3.2 Hallucination

We found especially in HuggingFace, the GPT-4 model incurs serious hallucination problems. It would
sometimes put a GitHub name that is not associated with the HuggingFace repository in to the domain
of pretrained_model_name_or_path. Fig. 9 demonstrates some examples and we also observe
that GPT-4 sometimes assumes the user have a local path to the model like your_model_name. This
is greatly reduced by Gorilla as we see the hallucination error comparison in Tab. 1.

16

Figure 10: Performance: We plot each model’s performance on different configurations. We see that Gorilla
performs extremely well in the zero-shot setting. While even when the oracle answer is given, Gorilla is still the
best.

17

LLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy048.3838.718.8159.13Torch Hub 0-shotLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy8.638.1735.4839.7840.32Torch Hub with BM25-RetrieverLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy14.5160.2159.1360.2161.82Torch Hub with GPT-RetrieverLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy16.1266.3166.1263.4467.2Torch Hub with Oracle RetrieverLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy016.8119.86.171.68HuggingFace 0-shotLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy2.9817.2516.4814.617.03HuggingFace with BM25-RetrieverLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy10.1747.3444.5741.3747.45HuggingFace with GPT-RetrieverLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy17.6989.7185.0677.2191.26HuggingFace with Oracle RetrieverLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy041.7518.29.1983.79Tensorflow Hub 0-shotLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy8.954.1634.0135.1841.89Tensorflow Hub with BM25-RetrieverLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy15.6265.5943.9455.6264.96Tensorflow Hub with GPT-RetrieverLLAMAGPT-3.5GPT-4ClaudeGorillaModel020406080100Accuracy12.5595.0355.9174.7494.16Tensorflow Hub with Oracle RetrieverFigure 11: Accuracy vs Hallucination: We plot each model’s performance on different configurations. We
found that in the zero-shot setting, Gorilla has the most accuracy gain while maintaining good factual capability.
When prompting with different retrievers, Gorilla is still capable to avoid the hallucination errors.

18

0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaTorch Hub 0-shot0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaTorch Hub with BM25-Retriever0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaTorch Hub with GPT-Retriever0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaTorch Hub with Oracle Retriever0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaHuggingFace 0-shot0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaHuggingFace with BM25-Retriever0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaHuggingFace with GPT-Retriever0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaHuggingFace with Oracle Retriever0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaTensorflow Hub 0-shot0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaTensorflow Hub with BM25-Retriever0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaTensorflow Hub with GPT-Retriever0102030405060708090100Hallucination0102030405060708090100AccuracyLLAMAGPT-3.5GPT-4ClaudeGorillaTensorflow Hub with Oracle Retriever