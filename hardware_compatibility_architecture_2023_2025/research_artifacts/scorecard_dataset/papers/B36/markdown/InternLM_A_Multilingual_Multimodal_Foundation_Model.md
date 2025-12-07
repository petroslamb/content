InternLM-XComposer: A Vision-Language Large Model for
Advanced Text-image Comprehension and Composition
Pan Zhang∗1, Xiaoyi Dong∗1, Bin Wang1, Yuhang Cao1, Chao Xu1, Linke Ouyang1, Zhiyuan Zhao1,
Haodong Duan1, Songyang Zhang1, Shuangrui Ding1, Wenwei Zhang1, Hang Yan1, Xinyue Zhang1, Wei Li1,
Jingwen Li1, Kai Chen1, Conghui He1, Xingcheng Zhang1, Yu Qiao1, Dahua Lin1, Jiaqi Wang1,B
1Shanghai Artificial Intelligence Laboratory
internlm@pjlab.org.cn
Black holes are one of the most fascinating and mysterious
objects in the universe. They are regions of space-time where
gravity is so strong that nothing, not even light, can escape their
gravitational pull. Despite their name, black holes are not actually
black; instead, they appear dark because they absorvb all forms of
electromagnetic radiation, including visible light.
Write a popular science article about “Unraveling the 
Mysteries of Black Holes: A Scientific Overview” with 
pictures and illustrations.
Describe the image 
in detail
Interleaved Composition Text-Image Comprehension
Unraveling the Mysteries of Black Holes: 
A Scientific Overview
Benchmark Performance
The concept of a black hole was first proposed by physicist Karl
Schwarzschild in 1916 as a solution to Einstein's theory of
general relativity. According to this theory, if a massive enough
star collapses under its own gravity, it will form a singularity at
its center—a point of infinite density and zero volume. This
singularity is surrounded by an event horizon, a boundary beyond
which no matter or energy can escape.
Since then, astronomers have discovered several types of black
holes, including stellar-mass black holes, intermediate-mass black
holes, and supermassive black holes. Stellar-mass black holes are
formed from the collapse of large stars, while intermediate-mass
black holes are thought to be the remnants of colliding galaxies.
Supermassive black holes, on the other hand, are believed to exist
at the centers of most galaxies, including our own Milky Way.
One of the most intriguing aspects of black holes is their ability to
distort spacetime around them. This distortion is known as
gravitational lensing, and it allows astronomers to observe distant
objects that would otherwise be obscured by Earth's atmosphere.
For example, NASA's Hubble Space Telescope has used
gravitational lensing to capture images of quasars, some of the
most distant and luminous objects in the universe.
Another important aspect of black holes is their accretion disks.
As matter falls into a black hole, it heats up and emits X-rays and
gamma-ray bursts. These emissions provide valuable insights into
the inner workings of black holes and help astronomers
understand how they grow and evolve over time.
Despite significant progress in our understanding of black holes,
there are still many unanswered questions about these enigmatic
objects. For example, we do not yet know what happens to
material that falls into a black hole once it crosses the event
horizon. Some theories suggest that such material might be
"eaten" by the black hole, while others propose that it might be
converted into exotic forms of matter with unusual properties.
In conclusion, black holes are among the most fascinating and
mysterious objects in the universe. Their unique properties make
them ideal laboratories for studying the fundamental laws of
physics, and their discovery has revolutionized our understanding
of the cosmos. With continued research and exploration, we hope
to unravel the mysteries of black holes.
The image features a cartoon crab swimming in
the ocean, surrounded by water . The crab is
holding onto a fishing line, which has a dollar
bill attached to it. The dollar bill can be seen
floating in the water near the crab.
Which cartoon is this crab from?
The cartoon crab in the image is from the show 
"SpongeBob SquarePants."
Which album cover is it imitating?
The crab is imitating the album cover of Nirvana's 
"Nevermind."
Why the image is funny?
The image is funny because it depicts a cartoon
crab holding onto a fishing line with a dollar bill
attached to it. The combination of a cartoon
character and a real-life object like a dollar bill
creates a humorous contrast, making the image
entertaining and amusing.
Ours
InstructBLIP-7B
LLaV A-1.5-7B
Qwen-VL-Chat-7B 
mPLUG-Owl-7B 
Otter-7B
0.6
0.64
0.68
0.72
0.76
0.8
Human Eval
0.8
0.82
0.84
0.86
0.88
0.9
GPT4-Vision Eval
SeedBench
Ours GPT4-Vision
InternLM-20B Qwen-14B
Interleaved Composition Evaluation
Human Eval GPT4-Vision Eval
0.6
0.64
0.68
0.72
0.76
0.8
0.8
0.82
0.84
0.86
0.88
0.9
GPT-3.5
MMBench-CN
MMBench
CCBench
Tiny LVLM MME
QBench
74
63
52
41
72
59
46
33
50 40 30 20
320
290
260
230
1900
1800
1700
1600 70605040
65
60
55
50
Figure 1. The InternLM-XComposer shows excellent interleaved composition and text-image comprehension ability, leading to strong
performance on various multi-modal benchmarks. For the Interleaved Composition Evaluation by both Human and GPT4-Vision (GPT4-
V), our model shows competitive performance to GPT4-Vision and GPT3.5.
Abstract
We propose InternLM-XComposer, a vision-language
large model that enables advanced image-text compre-
hension and composition. The innovative nature of our
model is highlighted by three appealing properties: 1)In-
terleaved Text-Image Composition: InternLM-XComposer
can effortlessly generate coherent and contextual articles
that seamlessly integrate images, providing a more en-
gaging and immersive reading experience. Simply pro-
vide a writing instruction, and our system will generate
the corresponding manuscript. It can intelligently iden-
tify the areas in the text where images would enhance the
content and automatically insert the most appropriate vi-
* indicates equal contribution.
sual candidates. 2) Comprehension with Rich Multilin-
gual Knowledge: The text-image comprehension is em-
powered by training on an extensive multi-modal multi-
lingual database with carefully crafted strategies, result-
ing in a deep understanding of visual content. 3)State-
of-the-art Performance: Our model consistently achieves
state-of-the-art results across various mainstream bench-
marks for vision-language foundational models, includ-
ing MME Benchmark, MMBench, MMBench-CN, Seed-
Bench, CCBench (Chinese Cultural Benchmark), QBench
and Tiny LVLM. Owing to the absence of established met-
rics for quantitatively assessing text-image composition, we
have devised a robust evaluation procedure that comprises
both human and GPT4-Vision (GPT4-V) to ensure relia-
bility. Notably, our InternLM-XComposer achieves com-
petitive text-image composition scores compared to pub-
1
arXiv:2309.15112v5  [cs.CV]  14 Dec 2023

lic solutions, including GPT4-V and GPT3.5. Collec-
tively, InternLM-XComposer seamlessly blends advanced
text-image comprehension and composition, revolutioniz-
ing vision-language interaction and offering new insights
and opportunities. The InternLM-XComposer model se-
ries are publicly available athttps://github.com/
InternLM/InternLM-XComposer.
1. Introduction
Over the past year, impressive progress has been made in
developing large language models (LLMs) [5, 7, 15, 16, 24,
60, 61, 66, 69, 84–86]. These state-of-the-art models, in-
cluding ChatGPT [60], GPT4 [61], and PaLM 2 [16], have
shown an unprecedented ability to follow human instruc-
tions and solve open-ended tasks. Inspired by the success of
PaLM-E [23] and BLIP2 [42], there is a promising approach
to extending language models for vision-language tasks by
leveraging vision features as extra inputs of LLMs. The
community has developed several vision-language large
models (VLLMs), such as MiniGPT-4 [104], LLaV A [50],
and InstructBLIP [18], based on open-source LLMs like
LLaMA [85], GLM [24], and InternLM [84]. However,
these VLLMs focus on pure text outputs, missing the op-
portunity to equip generated text with richer information
through auxiliary multimedia content like images.
In this work, we propose InternLM-XComposer, which
is a vision-language large model that enables advanced text-
image comprehension and composition ability.
1) Interleaved Text-Image Composition. InternLM-
XComposer excels in generating long-form content that
is interleaved with contextually relevant images, providing
more engaging and immersive vision-language interactions.
In its operational flow, the framework first crafts articles fol-
lowing human-provided instructions. Subsequently, it au-
tonomously pinpoints optimal locations within the text for
image placement and furnishes corresponding suitable im-
age descriptions. In accordance with the generated descrip-
tions, instead of relying on text-to-image generation mod-
els [6, 70–73], we opt to source aligned images from a large-
scale web-crawled image database for realistic quality and
contextual alignment. Moreover, it also provides flexibility
by allowing users to customize an image repository.
Compared to a baseline approach that relies solely on
CLIP [67, 92] for image retrieval, XComposer offers a
more reliable solution for choosing the most appropriate im-
age. Initially, we select potential image candidates from our
database using CLIP. Then, InternLM-XComposer lever-
ages its comprehension capabilities to identify the image
that optimally complements the content.
2) Comprehension with Rich Multilingual Knowl-
edge. LLM demonstrates remarkable ability in handling
open-world tasks, a capability attributed to its extensive
training data, e.g., 2T text tokens used in LLaMA2 [86].
This vast dataset inherently encapsulates a broad spec-
trum of semantic knowledge across diverse domains. In
contrast, current vision-language datasets [8, 62, 75, 78]
are limited in both volume and diversity compared to the
LLM database. This results in insufficient coverage of
vision-language concepts due to the long-tailed data distri-
bution [17, 54, 59] in the real world. To tackle this limi-
tation, we employ two practical solutions: First, to extend
the knowledge of VLLMs with widespread concepts, a mul-
tilingual vision-language dataset comprising over 11 mil-
lion semantic concepts is collected from public websites.
We further gather open-sourced vision-language datasets to
organize our high-quality training data. Second, we care-
fully crave the pretraining and finetuning strategies in our
training pipeline, where we adopt the mixed training data
of pure text and image-text data, primarily in English and
Chinese, to keep the initial capabilities of LLMs. Conse-
quently, InternLM-XComposer demonstrates a remarkable
proficiency in comprehending image content and respond-
ing with extensive multilingual knowledge. InternLM-
XComposer stands out for its unique ability to compose
long-form articles that incorporate contextually relevant im-
ages. This process involves creating high-quality written
content, identifying appropriate positions for inserted im-
ages, and selecting the most suitable images that consider
the complex context of interleaved text and images.
The proposed InternLM-XComposer exhibits superior
capabilities in both text-image comprehension and compo-
sition, as evidenced by its strong performance in quanti-
tative benchmarks and compelling qualitative demonstra-
tions. It consistently achieves state-of-the-art performance
across various leading benchmarks for vision-language
large models, encompassing MME Benchmark [26, 95],
MMBench [52], Seed-Bench [40], QBench [90], Tiny
LVLM [77] in English, and MMBench-CN [52], CCBench
(Chinese Cultural Benchmark) [52] for evaluations in Chi-
nese. Furthermore, in response to the absence of established
metrics for quantitatively assessing text-image composi-
tion, we set up an evaluation procedure for interleaved text-
image articles. This procedure takes into account the qual-
ity of both the written content and the accompanying illus-
trated images, which harnesses both human assessment and
GPT4-Vision (GPT4-V) scoring to enhance robustness and
reliability. The evaluation outcomes, spanning assessments
by both human and GPT4-V , consistently demonstrate the
competitive performance of InternLM-XComposer in in-
terleaved text-image composition compared to public solu-
tions, including GPT3.5 and GPT4-V .
2. Related Works
Large Language Models (LLMs).In recent years, the de-
velopment of large language models has accelerated. Ini-
2

tially, encoder-decoder models such as BERT [21] and
T5 [69], as well as decoder-only models like GPT [68],
leveraged the Transformer architecture [87] to achieve re-
markable results. GPT3 [7], employing prompt and in-
context learning strategies along with larger models and
data, has significantly performed in few-shot and zero-
shot tasks. As a result, using decoder-only structures with
autoregressive training has gained popularity among re-
searchers. Google’s PaLM [16] further expands the model
parameter size and data volume. To enhance the conversa-
tional experience, models like InstructGPT [63] and Chat-
GPT [60] integrate instruction-tuning and reinforcement
learning from human feedback (RLHF). The open-sourcing
of LLaMA [85] model has inspired research on LLMs,
e.g., Alpaca [83], Vicuna [15], GLM [24, 97], Qwen [66],
LLaMA2 [86], Baichuan2 [5], InternLM [84], Falcon [64],
and Mistral [36].
Vision Large Language Models (VLLMs). Visual
language learning has emerged as a research hotspot.
CLIP [67] and its following works [43, 45, 51, 99] aligns
image and text features through contrastive learning objec-
tives on large-scale image-text pairs, outperforming super-
vised learning on ImageNet [20] and exhibiting strong gen-
eralization capabilities in various downstream tasks. How-
ever, these models show limited capabilities for tasks re-
quiring higher-level understanding, such as visual ques-
tion answering. Benefiting from existing large language
model [15, 69, 85] and visual encoder [25, 43], the vi-
sion large language models (VLLMs) [11, 13, 14, 23]
achieve fine-grained alignment between the visual infor-
mation and the LLMs, show superb performance in di-
verse tasks. To achieve the modality alignment, a series
of studies[1, 3, 9, 10, 41, 50, 65, 88, 94, 101, 103] have ex-
plored the impact of the quality, diversity, and specificity of
the fine-tuning data and the learnable parameters. For ex-
ample, MiniGPT4 [104] adopts a simple FC layer with a
small amount of caption data. InstructBLIP [18] fine-tunes
the Q-Former [43] on diverse image-text tasks. LLaV A [50]
fine-tunes the LLM with GPT-4 generated high-quality in-
struction tuning data. Qwen-VL [4] and CogVLM [89]
fine-tune on high-resolution images with multi-task train-
ing. Moreover, some recent works [22, 28, 82, 96] inte-
grate the image generation task with VLLMs to generate
text-aligned images. InternLM-XComposer stands out for
its unique ability to compose long-form articles that incor-
porate contextually relevant images. This process involves
creating high-quality written content, identifying appropri-
ate positions for inserted images, and selecting the most
suitable visual content that considers the interleaved vision-
language context.
Image-text Retrieval Models. Image-text retrieval, a
pivotal area in multimodal modeling, has seen substan-
tial advancements recently. CLIP [67] and its following
Perceive 
Sampler
Perceive 
Sampler
Visual 
Encoder
Visual 
Encoder
Image
InternLM
Text
Pre-Training Stage
InternLM
SFT Stage
LoRA
Image
Text
FrozenTuned
Figure 2. The architecture and training regimen of the InternLM-
XComposer. The Pre-training stage aligns the visual and language
knowledge and the SFT stage excites different model capabilities.
works [33, 35, 37, 43, 93, 100] utilize contrastive learning
on a large corpus of image-text pairs, excels in image-text
matching, enabling efficient retrieval in both image-to-text
and text-to-image modalities. However, the capabilities of
current models are primarily confined to matching images
with aligned descriptions, which has a significant gap be-
tween our image-text article composition task, which fo-
cuses on selecting a suitable image based on a complex con-
text containing interleaved images and long text.
3. Method
3.1. Model Architecture
As depicted in Figure 2, the proposed InternLM-
XComposer contains three integral components: a visual
encoder, a perceive sampler, and a large language model.
Visual Encoder. The visual encoder in InternLM-
XComposer employs EV A-CLIP [25], an refined variant of
the standard CLIP [92], enhanced with mask image model-
ing capabilities, to proficiently capture the visual nuances of
the input image. Within this module, images are resized to
a consistent dimension of 224 × 224 and subsequently dis-
sected into patches with a stride of 14. These patches serve
as input tokens and enable the self-attention mechanisms
within the transformer block, facilitating the extraction of
detailed image embeddings.
Perceive Sampler. The perceive sampler within the
InternLM-XComposer operates as an attentive pooling
mechanism designed to condense the initial set of 257 im-
age embeddings down to 64 refined embeddings. These op-
timized embeddings are subsequently aligned to be com-
patible with the knowledge structures understood by the
large language model. Following BLIP2 [42], we leverage
BERTbase [21] equipped with cross-attention layers, serv-
ing as the perceive sampler in our framework.
Large Language Model. The InternLM-XComposer is
anchored on InternLM [84] as its foundational large lan-
guage model. Notably, InternLM stands as a potent lan-
guage model equipped with multilingual capabilities, pro-
ficient in both English and Chinese. In our framework, we
employ the publicly available InternLM-Chat-7B to serve
as the large language model.
3

Lauguage Type Dataset Images Text
English
Pure Text WanJuan [30] - 5B
Paired CC 3M [78] 3M 37M
Paired SBU-Caption [62]) 1M 18M
Paired LAION400M [75] 509M 10B
Paired CC 12M [8] 9M 250M
Paired In-house Concept data 2M 321M
Interleaved Multimodal C4 [105] 332M 40B
Chinese
Pure Text WanJuan [30] - 5B
Paired TaiSu [53] 44M 865M
Paired WuKong [29] 31M 545M
Paired LAION-CN [74] 80M 2B
Paired In-house Concept data 9M 704M
Interleaved WanJuan [30] 85M 13B
Total 1.1B 77.7B
Table 1. Details of InternLM-XComposer pre-training data.
LAION-CN represents the Chinese language subset extracted
from the larger LAION-5B corpus. This subset is further cleaned
utilizing the Chinese CLIP [92]. The volume of text data is
counted in terms of the number of tokens. The In-house Concept
data is collected from public websites, including over 11 million
vision-language concepts from public websites.
Task Dataset
Multi-task training
Caption COCO [12], SUB [12], TextCaps [79]
VQA VQAv2 [2], GQA [34], OK-VQA [57],
IConQA [56] Text-VQA [80], SQA [55],
VSR [47], OCR-VQA [58], VIGC [88]
IQG VQAv2 [2], OK-VQA [57], A-OKVQA [76]
Conversation Visual Dialog [19], LLaV A-150k [50]
Instruction tuning
Composiiton In-house data (Refer to Sec.3.3)
Conversation LLaV A-150k [50], Alpaca-en&zh [83]
ShareGPT-en&zh [15], Oasst-en&zh [38], LRV [48]
Table 2. Datasets used for Supervised Fine-Tuning.
3.2. Training
As shown in Figure 2, the training process of InternLM-
XComposer is split into Pre-training Stage and Supervied
Fine-tuning (SFT) Stage. The pre-training stage utilizing
vast amounts of data for foundation model training, align-
ing the knowledge between the visual information and lan-
guage. Based on the pre-training model, the SFT stage in-
volves a multi-task training step and a following instruction
tuning step to excite different model capabilities.
Pre-training. The pre-training phase incorporates large-
scale image-text pairs along with interleaved image-text
data to pre-train the foundational vision-language model.
This data comprises multi-modal content in both English
and Chinese. As shown in Table 1, in addition to pub-
lic datasets, to enhance the ability of MLLMs to compre-
hend extensive visual concepts, we collect large-scale In-
house Concept data1 from various public websites, includ-
ing more than 11 million visual concepts and corresponding
details explanations. Please refer to supplementary materi-
als for more information. Moreover, to preserve the capabil-
ities of the initial large language model, the partial textual
data [30] utilized for InternLM’s pre-training is also em-
ployed in the pre-training phase of InternLM-XComposer.
The multi-modal pre-training process employs 1.1 billion
images alongside 77.7 billion text tokens as in Table 1.
During the pre-training phase, the visual encoder is
frozen, allowing the optimization to be concentrated on
the perceive sampler and the large language model. Ini-
tial weight for the perceive sampler and the large language
model are sourced from BLIP2 [42] and InternLM [84], re-
spectively. Given that the large language model lacks na-
tive understanding of image embeddings, its optimization
within the framework of multimodal pre-training serves to
enhance its capability to interpret such embeddings effec-
tively. The training objective for the model centers on next-
token prediction, utilizing cross-entropy loss function.
Supervised Fine-tuning. In the pre-training phase, im-
age embeddings are aligned with language representations,
equipping the large language model with a rudimentary un-
derstanding of image content. However, the model still
lacks proficiency in utilizing the image information opti-
mally. To address this limitation, we introduce a variety
of vision-language tasks that the model undertakes during
the subsequent Supervised Fine-Tuning Stage, which con-
tains two consecutively steps, i.e., Multi-task training and
Instruction tuning.
Multi-task Training. As illustrated in Table 2, the multi-
task training dataset is constructed from multiple sources
to endow the model with a diverse range of capabilities,
including scene understanding ( e.g., COCO Caption [12],
SUB [62]), location understanding (e.g., Visual Spatial Rea-
soning dataset [47]), optical character recognition (OCR)
(e.g., OCR-VQA [58]), and open-ended answering ( e.g.,
VQAv2 [2], GQA [34]), among others. Each of these tasks
is formulated as a conversational interaction, adhering to the
following format:
<|User|> : Instruction <eou>
<|Bot|> : Answer <eob>
where <eou> and <eob> represent the end-of-user and
end-of-bot tokens, respectively. For VQA datasets with
multiple questions per image, we structure them as multi-
round conversations with randomly ordered questions,
thereby substantially enhancing the efficiency of SFT.
In order to achieve stable and efficient fine-tuning, we
retains the weights of the pre-existing large language model
1Due to copyright concerns, we will release the concept name list and
source websites for the community to reproduce our concept data.
4

Artificial Intelligence Accelerates 
Deployment - A Wave of AI Large Model 
Product Iterations
Virtual anchors capable of live 
broadcasting, virtual beings for interactive 
teaching, robots that excel at playing 
Go, …
In this scene, we have an unmanned aerial 
vehicle, a low-altitude logistics delivery 
drone ...
With the advent of the big data era, more 
and more people…
…
Write an illustrated article based on the 
given title: Artificial Intelligence 
Accelerates Deployment - A Wave of AI 
Large Model Product Iterations
The second image.
...
Virtual anchors capable of live 
broadcasting, virtual beings for 
interactive teaching, robots that excel 
at playing Go, …
In this scene, we have an unmanned 
aerial vehicle, a low-altitude logistics 
delivery drone ...
Based on the given context and 
candidate images, select the 
appropriate image. Candidate images 
include:
I think images can be added under the 
1th, 2th, 5th, and 8th paragraphs.
The image captions are as follows:
1th paragraph: “…"
2th paragraph: “Unmanned Aerial 
Vehicle for All-Weather Low-Altitude 
Flight Achieves End-to-End Logistics 
Delivery in 15 Minutes”
5th paragraph: "AI Intelligent 
Applications in Daily Office Use"
8th paragraph: ...
Based on the above text, select the 
appropriate locations for inserting images
and give the image captions.
(a) Text Generation (b) Image Spotting and Captioning (c) Image Retrieval and Selection
Figure 3. The pipeline of the interleaved image-text composition.(a) Given a writing instruction, the model initially generates a
corresponding text-based article. (b) Subsequent to the article generation, the model is trained to identify suitable image locations and
generate corresponding captions for the ensuing steps. (c) A text-image retrieval algorithm is initially employed to constrict the pool of
candidate images. Following this, our model leverages its vision-language understanding ability to make the final image selection, ensuring
thematic and visual coherence by considering both the preceding textual content and images within the article.
in a frozen state. Subsequently, we augment the architecture
with Low-Rank Adaption (LoRA) [31] for the fine-tuning
process. The perceive sampler is concurrently trained, al-
beit with a distinct learning rate.
Instruction Tuning. To further empower aforementioned
model’s instruction following and interleaved image-text
composition capability, as shown in Table 2, we utilize data
from pure-text conversation corpora and LLaV A-150k for
instruction-based tuning, and leverage the LRV dataset to
mitigate hallucinations. The interleaved image-text com-
position dataset is constructed based on the methodology
delineated in Section 3.3.
3.3. Interleaved Image-Text Composition
To craft interleaved image-text compositions, the initial step
involves the generation of an article following human in-
struction. After this, accompanying illustrated images are
incorporated at well-suited positions within the textual con-
tent, enriching the overall narrative and augmenting reader
engagement. The pipeline of interleaved image-text com-
position is shown in Figure 3.
Text Generation. To facilitate the generation of extended
text-based articles, we collect a dataset comprising inter-
leaved image-text compositions from the Internet. To en-
able the model to generate text-based articles with respect
to specific instructions, we utilize GPT-4 to generate diverse
instructions based on the article, including a draft outline, a
few keywords, or a simple title.
As mentioned in Section 1, a more engaging and immer-
sive reading experience needs both text and suitable images.
We empower our model with such composition capability
with a decoupled pipeline, which defines the position and
caption of images based on the generated text, and then se-
lects the one image for each position from a list of candi-
dates according to article context.
Image Spotting and Captioning. First, the acquired in-
terleaved image-text data is leveraged to train our model
for pinpointing image locations. For subsequent image re-
trieval, it’s imperative to generate an appropriate caption,
enabling the application of various text-image retrieval al-
gorithms. To mitigate this challenge, we generate caption
data utilizing GPT-4, which is provided with the text-based
article and image locations and is instructed to generate a
caption for each image position that remains coherent with
the overarching theme and concept.
Image Retrieval and Selection.Having obtained the cap-
tions, a variety of text-image retrieval methods become
available for use. In this work, we opt for the CLIP model,
capitalizing on its proven efficacy. We compute the simi-
larity scores between the generated caption and each image
in the candidate pool. The top m images, based on these
similarity scores, are then selected to constitute the reduced
candidate pool for further processing.
To guarantee thematic or conceptual coherence in the im-
ages dispersed throughout the article, we deploy our vision-
language model to execute the final image selection. Our
5

Model Overall Exist. Count Pos. Color OCR Poster Cele. Scene Land. Art. Comm. NumCal. Trans. Code Avg.
MiniGPT-4[104] 694.3 68.3 55.0 43.3 43.3 57.5 41.8 54.4 71.8 54.0 60.5 59.3 45.0 0.0 40.0 49.6
LLaV A[50] 712.5 50.0 50.0 50.0 50.0 50.0 50.0 48.8 50.0 50.0 49.0 57.1 50.0 57.5 50.0 50.9
VisualGLM[24] 880.4 85.0 50.0 48.3 48.3 42.5 66.0 53.2 146.3 83.8 75.3 39.3 45.0 50.0 47.5 62.9
mPLUG-Owl[94] 1238.4 120.0 50.0 50.0 50.0 65.0 136.1 100.3 135.5 159.3 96.3 78.6 60.0 80.0 57.5 88.5
LLaMA-A.-V2[27] 1194.9 120.0 50.0 48.3 48.3 125.0 99.7 86.2 148.5 150.3 69.8 81.4 62.5 50.0 55.0 85.4
InstructBLIP[18] 1417.9 185.0 143.3 66.7 66.7 72.5 123.8 101.2 153.0 79.8 134.3 129.3 40.0 65.0 57.5 101.3
Lynx[98] 1508.9 195.0 151.7 90.0 90.0 77.5 124.8 118.2 164.5 162.0 119.5 110.7 17.5 42.5 45.0 107.8
Otter[41] 1572.0 195.0 88.3 86.7 86.7 72.5 138.8 172.7 158.8 137.3 129.0 106.4 72.5 57.5 70.0 112.3
Cheetor[44] 1584.4 180.0 96.7 80.0 80.0 100.0 147.3 164.1 156.0 145.7 113.5 98.6 77.5 57.5 87.5 113.2
BLIV A[32] 1669.2 180.0 138.3 81.7 180.0 87.5 155.1 140.9 151.5 89.5 133.3 136.4 57.5 77.5 60.0 119.2
MMICL[102] 1810.7 170.0 160.0 81.7 156.7 100 146.3 141.8 153.8 136.1 135.5 136.4 82.5 132.5 77.5 129.3
LLaV A-1.5[49] 1826.7 185.0 155.0 133.3 170.0 125.0 160.5 152.9 161.3 170.5 117.7 127.8 42.5 77.5 47.5 130.5
Qwen-VL-Chat[4] 1848.3 158.3 150.0 128.3 170.0 140.0 178.6 120.6 152.3 164.0 125.5 130.7 40.0 147.5 42.5 132.0
Ours 1919.5 190.0 158.3 126.7 165.0 125.0 161.9 150.3 159.8 165.3 126.3 138.6 55.0 112.5 85.0 137.1
Table 3. Evaluation of MME-Benchmark. Here we report the results on all the sub tasks, including Existence(Exist.), Count, Posi-
tion(Pos.), Color, OCR, Poster, Celebrity(Cele.), Scene, Landmark(Land.), Artwork(Art.), Commonsense Reasoning(Comm.), Numerical
Calculation(NumCal.), Text Translation(Trans.), Code Reasoning(Code) and the task-level average (Avg.). We bold the highest average /
overall scoreand highlight the Top-3 model of each sub taskwith underline.
model selects images by considering both preceding text
and prior images within the article. This mechanism en-
ables the model to acquire an understanding of thematic
and visual coherence, an expertise derived from the dataset
of interleaved image-text compositions. Our model is also
trained to select the ground-truth image from a candidate list
given the article and image position to enhance the capabil-
ity. The training data is directly structured from collected
interleaved text-image articles and randomly selected nega-
tive candidates from the image repository.
4. Experiments
4.1. English-Based Benchmark results.
In this section, we validate the benchmark performance of
our InternLM-XComposer after the Multi-task training. In
the following, the comparison model is 7B version by de-
fault if there is no additional annotation.
MME Benchmark[26] measures the perception and cog-
nition capability of multi-modality LLMs with carefully
crafted questions within 14 sub-tasks. As shown in Ta-
ble.3, our model reached a new state-of-the-art performance
137.11%, outperforms the previous method Qwen-VL-Chat
with more than 5.0%. We also highlight the Top-3 models
within each subtask with underline and we notice that our
model reaches the Top-3 performance with 10 of the 14 sub-
tasks. This proves the outstanding generalize of our model.
MMBench[52] is a hand-crafted challenging benchmark,
which evaluates the vision-related reasoning and perception
capability with multi-choice questions. The MME Bench
provides both a dev-set and test-set. Here we report the
test-set performance of our model. As shown in Table.4.
Our method gets 74.4% accuracy and outperforms previous
methods by a large margin. Further, our model reaches the
Method Avg. LR AR RR FP-S FP-C CP
MiniGPT-4[104] 23.0 13.6 32.9 8.9 28.8 11.2 28.3
VisualGLM [24] 33.5 11.4 48.8 27.7 35.8 17.6 41.5
InstructBLIP[18] 33.9 21.6 47.4 22.5 33.0 24.4 41.1
LLaV A [50] 36.2 15.9 53.6 28.6 41.8 20.0 40.4
LLaMA-A-V2 [27] 38.9 7.4 45.3 19.2 45.0 32.0 54.0
Otter-I [41] 48.3 22.2 63.3 39.4 46.8 36.4 60.6
LLaV A-1.5 [49] 59.5 32.4 72.6 49.3 62.3 52.2 67.7
Shikra [10] 60.2 33.5 69.6 53.1 61.8 50.4 71.7
Qwen-VL-Chat [4] 61.8 40.5 74.3 47.9 66.3 46.2 72.8
LMEye [46] 62.6 41.0 74.3 55.9 61.6 58.7 69.2
MMICL[101] 65.2 44.3 77.9 64.8 66.5 53.6 70.6
mPLUG-Owl[94] 66.0 43.4 76.0 62.1 68.6 55.9 73.0
Ours 74.4 50.6 82.0 76.1 79.3 59.2 81.7
Table 4. Evaluation of MMBench test set.Here we report the
results on the six L-2 abilities, namely Logical Reasoning (LR),
Attribute Reasoning (AR), Relation Reasoning (RR), Fine-grained
Perception (Cross Instance) (FP-C), Fine-grained Perception (Sin-
gle Instance) (FP-S), and Coarse Perception (CP).
best performance in all the dimensions. This proves that
our model understands the image information well and can
handle diverse vision-related tasks.
Seed-Bench[40] is a large-scale multi-modality bench-
mark, which is built with the help of GPT-4 and con-
tains nearly 19K multi-choice questions for both image and
video. Here we report the image-set results in Table.5. It
can be observed that our model gets the best overall perfor-
mance and the highest performance in 6 of the 9 sub-tasks.
We also notice that the sub-task data number is in-balance,
so the overall metric would be biased toward some sub-
tasks. To better evaluate the generalized capability of the
LLMs along different tasks. We also report the task-level
average, and our model reaches the state-of-the-art average
6

Method Language Model Overall T-Avg. Sense.U Inst.Id Isnt.At Inst.Lo Inst.Co Spat.R Inst.It Vis.R Text.R
OpenFlamingo[3] MPT-7B 42.7 39.4 53.2 45.3 40 31.2 39.3 32.6 36.1 51.4 25.9
Otter[41] MPT-7B 42.9 40.08 51.3 43.5 42.3 34.2 38.4 30.9 40.2 55.3 24.7
MiniGPT-4[104] Vicuna-7B 47.4 42.6 56.3 49.2 45.8 37.9 45.3 32.6 47.4 57.1 11.8
BLIP-2 [43] Flan-T5-XL 49.7 45.7 59.1 53.9 49.2 42.3 43.2 36.7 55.7 45.6 25.9
IDEFICS-80b-instruct[39] LLaMA-65B 53.2 54.4 64 52.6 50.8 48.3 46.1 45.5 62.9 68 51.8
Kosmos-2[65] Kosmos 1.3B 54.4 49.4 63.4 57.1 58.5 44 41.4 37.9 55.7 60.7 25.9
InstructBLIP-Vicuna[18] Vicuna-7B 58.8 52.2 60.2 58.9 65.6 43.6 57.2 40.3 52.6 47.7 43.5
Qwen-VL-Chat[4] Qwen-7B 65.4 61.9 73.3 67.3 69.6 57.7 52.9 48.2 59.8 74.6 53.5
LLaV A-1.5 [49] LLaMA2-7B 66.2 61.8 74.3 69.9 67.6 60.3 57.2 50.8 63.9 77.3 35.3
Ours InternLM-7B 66.9 65.2 75.0 71.7 67.6 60.8 56.2 55.3 74.4 77.0 48.5
Table 5. Evaluation of Seed-Bench test set. Here we report the results on the image-based sub tasks, including Scene Understand-
ing(Sense.U), Instance Identity(Inst.Id), Instance Attributes(Inst.At), Instance Localization(Inst.Lo), Instance Counting(Inst.Co), Spatial
Relation(Spat.R), Instance Interaction(Inst.It), Visual Reasoning(Vis.R), Text Recognition(Text.R), and both overall accuracy(Overall) and
task-level average accuracy(T-Avg.)
Method Overall Perception Description Assesment
VisualGLM[24] 42.4 53.3 49.8 24.0/23.9
Otter [41] 46.7 47.2 60.2 32.3/33.3
MiniGPT-4[104] 47.5 51.8 61.2 29.3/30.0
InstructBLIP[18] 48.3 55.8 47.3 38.9/44.6
Shikra [10] 48.3 55.3 55.7 33.6/34.5
LLaMA-A-V2 [27] 51.8 58.1 57.5 38.1/41.7
LLaV A[50] 54.4 54.7 62.7 44.4/47.4
LLaV A-v1.5[49] 55.0 61.4 57.8 44.4/47.4
Qwen-VL-Chat[4] 55.6 61.7 56.0 47.5/50.6
mPLUG-Owl[94] 56.4 58.9 65.7 43.2/45.8
Ours 63.6 64.4 70.2 54.2/58.1
Table 6. Evaluation of Q-Bench test set. Here we report all the
sub-tasks, including Perception, Description and Assessment. For
Assessment, we report both SRCC and PLCC score.
accuracy and outperforms the previous method with 3.3%.
This further proves the general capability of our model.
Q-Bench[90] is a comprehensive benchmark which focus
on the low-level vision, including three realms: perception,
description, and assessment. Here we report the test set re-
sults in Table.6. Our model shows the state-of-the-art per-
formance on all the three tasks, surpass previous methods
with a large margin. The results suggest our model has a
comprehensive understanding of the image, which not only
focus the high-level semantic feature of the image, but also
the low-level information.
4.2. Chinese-Based Benchmark results.
As we introduced in Sce.1, our model is pretrained with rich
multilingual knowledge. To prove the effectiveness of the
pretraining, here we further evaluate its performance with
two Chinese-based benchmarks.
MMBench-CN[52] is the Chinese translated benchmark of
the original MMbench, which shows the vision-related Chi-
nese understanding and reasoning capability. Here we re-
port the test-set performance in Table.7. It can be observed
that our method outperforms previous methods by a large
Method Avg LR AR RR FP-S FP-C CP
OpenFlamingo[3] 1.7 1.7 4.5 0 1.5 0.8 1.3
MiniGPT-4[104] 11.9 11.6 19.4 5.7 14.6 6.5 10.9
InstructBLIP[18] 23.9 9.2 38.5 16.6 20.9 15 30.8
mPLUG-Owl[94] 24.9 6.9 34 17.5 33.4 8.5 30.6
VisualGLM[24] 25.6 5.2 42 18 24.1 13 34.5
LLaV A[50] 36.6 15 52.4 17.1 34.4 27.5 50.3
IDEFICS-80B-I[39] 38.1 20.8 49 27.5 29.1 36.0 51.2
LLaV A-1.5[49] 53.8 31.2 67.7 42.7 49.5 43.7 67.7
Qwen-VL-Chat[4] 56.3 35.3 63.5 46 63.6 43.7 64.7
Ours 72.4 44.5 79.5 83.4 71.6 56.3 82.4
Table 7. Evaluation of MMBench-CN test set. Here we report
the results on the six L-2 abilities based on Chinese.
Method Avg CP CR F&C HF S&B SR TS
OpenFlamingo[3] 0.7 1.8 0 0.8 0.0 0.0 2.2 1.5
MiniGPT-4[104] 1.7 7.0 4.0 0.0 0.0 1.0 0.0 0.0
LLaV A[50] 8.3 10.5 8.1 7.6 1.7 8.0 11.1 10.6
VisualGLM[24] 9.2 14.0 11.1 8.4 0.0 14.0 4.4 7.6
InstructBLIP[18] 12.1 8.8 9.1 21.0 0.0 12.0 6.7 18.2
mPLUG-Owl[94] 12.9 22.8 17.2 6.7 0.0 25.0 4.4 7.6
LLaV A-1.5[49] 16.4 15.8 19.2 10.9 3.4 21.0 37.8 12.1
Qwen-VL-Chat[4] 39.3 40.4 33.3 31.9 3.4 67.0 51.1 42.4
Ours 47.6 50.9 53.5 42.0 10.3 55.0 73.3 50.0
Table 8. Evaluation of CCBench test set. We report all the sub-
tasks, including Calligraphy Painting(CP), Cultural Relic(CR),
Food & Clothes(F&C), Historical Figures(H&F), Scenery &
Building(S&B), Sketch Reasoning(SR), Traditional Show(TS),
margin. When comparing with the English version perfor-
mance in Table.4. Qwen and VisualGLM have 4.9% and
7.9% performance degrading, while the performance gap of
our model between different languages is only 2.0%. This
proves the strong multi-lingo capability of our model.
Chinese-Bench[52] is a Chinese knowledge-related bench-
mark, that challenges the model with Chinese traditional
cultural questions, including art, food, clothes, landmarks,
etc. The performance is given in Table.8. It can be
observed that the benchmark is quite challenging, most
LLaMA-based model fails to answer these questions, due
7

Human Evaluation GPT4-Vision Evaluation
Method Avg. Pref. Text Image Avg. Pref. Text Image
Qwen-14B[66] 0.62 0.52 0.80 0.54 0.82 0.78 0.91 0.72
Intern-20B[84] 0.64 0.54 0.82 0.56 0.81 0.82 0.89 0.70
GPT3.5 [60] 0.71 0.64 0.88 0.59 0.84 0.84 0.91 0.75
Ours 0.74 0.65 0.90 0.67 0.87 0.90 0.93 0.79
GPT4-V [61] 0.77 0.73 0.95 0.64 0.89 0.88 0.96 0.78
Table 9. Quantitative results by human and GPT-4Vision. Text
means the writing-related scores and Image means the image-
selection related scores. The evaluation by human and GPT-
4Vision shows consist conclusion that GPT-4 performs best and
our model is on par with the GPT3.5, better than other LLMs.
Method Human Top-1 GPT4-Vision Our
Score 100.0 40.2 51.7 80.4
Table 10. Effectiveness of Image Selection, Human is the ground
truth selected by human.
to the lack of corresponding knowledge. Compared with
LLaMA-based methods, the Qwen-based model Qwen-VL-
Chat shows a much better performance of 39.3%. While it
is still worse than InternLM-based model, which reaches a
new state-of-the-art performance of 47.6%. This proves the
rich Chinese knowledge of IntenrLM and the great align-
ment between the vision and language knowledge by our
large-scale pre-training.
4.3. Interleaved Image-Text Composition
Quantitative results. Due to the lack of existing met-
rics to evaluate the image-text interleaved article quality,
we designed a detailed user study metric 2, including eight
dimensions: four text-related dimensions (instruction fol-
lowing, writing quality, logic, factualness), three image-
related dimensions (image-text consistency, image informa-
tive, image consistency), and one subjective preference. As
our InternLM-XComposer is the first interleaved image-text
composition model, we compare the composition quality
with recent leading LLMs and VLMs, including GPT4-V ,
GPT3.5, InternLM-20B, and Qwen-14B. For a fair compar-
ison, we apply a similar composition pipeline as mentioned
in Sec.3.3 in these solutions. Notably, the image selection
phase is not supported in language-only models (GPT3.5,
InternLM-20B, and Qwen-14B), in which retrieved images
with top-1 similarity are adopted as the final illustrations. In
practice, we generated articles with 20 articles. For robust-
ness and reliability of final results, we adopt both human
evaluation and GPT4-V scoring. Specifically, we invite 10
human experts for assessment. In the meantime, GPT4-V
also rates scores for these articles on the proposed eight di-
mensions.
As presented in Table.9, GPT-4V shows the best per-
formance in all the text-related dimensions and the highest
2Please refer to the supplementary materials for more details.
Method MME MMBench Seed Bench
Ours 1919.5 74.4 66.9
Freeze Perceive Sampler 1819.1 71.3 63.2
Freeze Attention LoRA 1776.5 72.0 65.9
Freeze FFN LoRA 1828.7 72.4 66.4
Table 11. Ablation on Learnable Components.
LLM Backbone MME MMBench MMBench-CN CCBench
LLaMA-2 [86] 1895.9 72.6 66.7 44.6
InternLM[84] 1919.5 74.4 72.4 47.6
Table 12. Ablation on LLM Backbone.
overall score. Benefiting from the interleaved image-text
composition training, our InternLM-XComposer performs
the best on image-related dimensions and the second best
on the text-related dimensions and average score.
Effectiveness of Image SelectionThe last step of our in-
terleaved Image-Text composition pipeline is the Image re-
trieval and selection. The InternLM-XComposer could se-
lect a proper image from the retrieved candidates based on
the context. Here we study the effectiveness of the im-
age selection based on human preference. Specifically, we
provide the text and candidate images to human experts,
GPT4-Vision and Intern-XComposer, and use the human-
selected images as the ground truth. We also use the image
with the highest retrieval similarity as the ‘Top-1’ baseline.
As shown in Table.10, InternLM-XComposer gets a higher
score than GPT4- V , which means the image selected by our
model is more consistent with the human preference.
Qualitative results. We direct readers to the supplemen-
tary materials for detailed qualitative results of the inter-
leaved image-text compositions and multimodal conversa-
tions generated by the InternLM-XComposer.
4.4. Ablation Study
Learnable Components. Here we study the influence of
different learnable components in the multi-task supervised
fine-tuning stage. As shown in Table.11, the Perceive Sam-
pler is critical for the multi-task learning, which shows sig-
nificant influence on most benchmarks. For the LoRA in
LLM, the Attention and FFN part are also important to re-
alize a superb performance.
LLM selection. Then we study the influence of different
LLMs, here we consider the InternLM-7B and LLaMA2-
7B, with the same pre-training and supervised fine-tuning
strategy. Here we report the results on MME, MMBench,
MMBench-CN and CCBench. With the results in Table.12,
we find the LLaMA-2 performs similar with InternLM-7B
in the English-based benchmarks, while the performances
gap is enlarged in the Chinese-based benchmarks.
8

5. Conclusion
In this paper, we present InternLM-XComposer, a vision-
language large model with superb multi-modality under-
standing and composition capability. Benefiting from the
rich multi-lingual and multi-modality knowledge from care-
fully designed pretraining, our model could generate coher-
ent interleaved image-text composition, and shows state-of-
the-art performance across various vision-language LLM
benchmarks. We hope XComposer could provide new in-
sight for the advanced vision-language interaction.
References
[1] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, An-
toine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur
Mensch, Katie Millican, Malcolm Reynolds, Roman Ring,
Eliza Rutherford, Serkan Cabi, Tengda Han, Zhitao Gong,
Sina Samangooei, Marianne Monteiro, Jacob Menick, Se-
bastian Borgeaud, Andrew Brock, Aida Nematzadeh, Sa-
hand Sharifzadeh, Mikolaj Binkowski, Ricardo Barreira,
Oriol Vinyals, Andrew Zisserman, and Karen Simonyan.
Flamingo: a visual language model for few-shot learning,
2022. 3
[2] Stanislaw Antol, Aishwarya Agrawal, Jiasen Lu, Margaret
Mitchell, Dhruv Batra, C. Lawrence Zitnick, and Devi
Parikh. Vqa: Visual question answering. In International
Conference on Computer Vision (ICCV), 2015. 4
[3] Anas Awadalla, Irena Gao, Josh Gardner, Jack Hessel,
Yusuf Hanafy, Wanrong Zhu, Kalyani Marathe, Yonatan
Bitton, Samir Gadre, Shiori Sagawa, Jenia Jitsev, Simon
Kornblith, Pang Wei Koh, Gabriel Ilharco, Mitchell Worts-
man, and Ludwig Schmidt. Openflamingo: An open-
source framework for training large autoregressive vision-
language models. arXiv.org, 2023. 3, 7
[4] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan
Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren
Zhou. Qwen-vl: A frontier large vision-language model
with versatile abilities. arXiv.org, 2023. 3, 6, 7, 17
[5] Baichuan. Baichuan 2: Open large-scale language models.
arXiv.org, 2023. 2, 3
[6] James Betker, Gabriel Goh, Li Jing, Tim Brooks, Jianfeng
Wang, Linjie Li, Long Ouyang, Juntang Zhuang, Joyce Lee,
Yufei Guo, Wesam Manassra, Prafulla Dhariwal, Casey
Chu, Yunxin Jiao, and Aditya Ramesh. Improving image
generation with better captions. 2
[7] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Sub-
biah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakan-
tan, Pranav Shyam, Girish Sastry, Amanda Askell, et al.
Language models are few-shot learners. Advances in Neu-
ral Information Processing Systems (NeurIPS), 33:1877–
1901, 2020. 2, 3
[8] Soravit Changpinyo, Piyush Sharma, Nan Ding, and Radu
Soricut. Conceptual 12m: Pushing web-scale image-text
pre-training to recognize long-tail visual concepts. In Pro-
ceedings of the IEEE/CVF Conference on Computer Vision
and Pattern Recognition, pages 3558–3568, 2021. 2, 4
[9] Jun Chen, Deyao Zhu, Xiaoqian Shen, Xiang Li, Zechu
Liu, Pengchuan Zhang, Raghuraman Krishnamoorthi,
Vikas Chandra, Yunyang Xiong, and Mohamed Elhoseiny.
Minigpt-v2: large language model as a unified interface
for vision-language multi-task learning. arXiv preprint
arXiv:2310.09478, 2023. 3
[10] Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang,
Feng Zhu, and Rui Zhao. Shikra: Unleashing multimodal
llm’s referential dialogue magic. arXiv.org, 2023. 3, 6, 7
[11] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa,
Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz,
Sebastian Goodman, Xiao Wang, Yi Tay, Siamak Shak-
eri, Mostafa Dehghani, Daniel Salz, Mario Lucic, Michael
Tschannen, Arsha Nagrani, Hexiang Hu, Mandar Joshi,
Bo Pang, Ceslee Montgomery, Paulina Pietrzyk, Marvin
Ritter, AJ Piergiovanni, Matthias Minderer, Filip Pavetic,
Austin Waters, Gang Li, Ibrahim Alabdulmohsin, Lucas
Beyer, Julien Amelot, Kenton Lee, Andreas Peter Steiner,
Yang Li, Daniel Keysers, Anurag Arnab, Yuanzhong Xu,
Keran Rong, Alexander Kolesnikov, Mojtaba Seyedhos-
seini, Anelia Angelova, Xiaohua Zhai, Neil Houlsby, and
Radu Soricut. Pali-x: On scaling up a multilingual vision
and language model, 2023. 3
[12] Xinlei Chen, Hao Fang, Tsung-Yi Lin, Ramakrishna
Vedantam, Saurabh Gupta, Piotr Dollar, and C. Lawrence
Zitnick. Microsoft coco captions: Data collection and eval-
uation server, 2015. 4
[13] Xi Chen, Xiao Wang, Lucas Beyer, Alexander Kolesnikov,
Jialin Wu, Paul V oigtlaender, Basil Mustafa, Sebas-
tian Goodman, Ibrahim Alabdulmohsin, Piotr Padlewski,
Daniel Salz, Xi Xiong, Daniel Vlasic, Filip Pavetic, Keran
Rong, Tianli Yu, Daniel Keysers, Xiaohua Zhai, and Radu
Soricut. Pali-3 vision language models: Smaller, faster,
stronger, 2023. 3
[14] Xi Chen, Xiao Wang, Soravit Changpinyo, AJ Piergio-
vanni, Piotr Padlewski, Daniel Salz, Sebastian Goodman,
Adam Grycner, Basil Mustafa, Lucas Beyer, Alexander
Kolesnikov, Joan Puigcerver, Nan Ding, Keran Rong, Has-
san Akbari, Gaurav Mishra, Linting Xue, Ashish Thapliyal,
James Bradbury, Weicheng Kuo, Mojtaba Seyedhosseini,
Chao Jia, Burcu Karagol Ayan, Carlos Riquelme, Andreas
Steiner, Anelia Angelova, Xiaohua Zhai, Neil Houlsby, and
Radu Soricut. Pali: A jointly-scaled multilingual language-
image model, 2023. 3
[15] Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhang-
hao Wu, Hao Zhang, Lianmin Zheng, Siyuan Zhuang,
Yonghao Zhuang, Joseph E. Gonzalez, Ion Stoica, and
Eric P. Xing. Vicuna: An open-source chatbot impressing
gpt-4 with 90%* chatgpt quality, March 2023. 2, 3, 4
[16] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin,
Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul
Barham, Hyung Won Chung, Charles Sutton, Sebastian
Gehrmann, et al. Palm: Scaling language modeling with
pathways. arXiv.org, 2022. 2, 3
[17] Yin Cui, Menglin Jia, Tsung-Yi Lin, Yang Song, and Serge
Belongie. Class-balanced loss based on effective number of
samples. In CVPR, Jun 2019. 2
[18] Wenliang Dai, Junnan Li, Dongxu Li, Anthony Meng Huat
Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale
Fung, and Steven Hoi. Instructblip: Towards general-
purpose vision-language models with instruction tuning,
9

2023. 2, 3, 6, 7, 17
[19] Abhishek Das, Satwik Kottur, Khushi Gupta, Avi Singh,
Deshraj Yadav, Jos ´e MF Moura, Devi Parikh, and Dhruv
Batra. Visual dialog. In Proceedings of the IEEE con-
ference on computer vision and pattern recognition, pages
326–335, 2017. 4
[20] Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li,
and Li Fei-Fei. Imagenet: A large-scale hierarchical image
database. In Proceedings of the IEEE/CVF Conference on
Computer Vision and Pattern Recognition (CVPR), pages
248–255, 2009. 3
[21] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina
Toutanova. Bert: Pre-training of deep bidirectional trans-
formers for language understanding. arXiv.org, 2018. 3
[22] Runpei Dong, Chunrui Han, Yuang Peng, Zekun Qi, Zheng
Ge, Jinrong Yang, Liang Zhao, Jianjian Sun, Hongyu Zhou,
Haoran Wei, Xiangwen Kong, Xiangyu Zhang, Kaisheng
Ma, and Li Yi. Dreamllm: Synergistic multimodal com-
prehension and creation. arXiv preprint arXiv:2309.11499,
2023. 3
[23] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch,
Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid,
Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong
Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duck-
worth, Sergey Levine, Vincent Vanhoucke, Karol Hausman,
Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch,
and Pete Florence. Palm-e: An embodied multimodal lan-
guage model. In arXiv preprint arXiv:2303.03378, 2023. 2,
3
[24] Zhengxiao Du, Yujie Qian, Xiao Liu, Ming Ding, Jiezhong
Qiu, Zhilin Yang, and Jie Tang. Glm: General language
model pretraining with autoregressive blank infilling. In
Proceedings of the 60th Annual Meeting of the Association
for Computational Linguistics (Volume 1: Long Papers),
pages 320–335, 2022. 2, 3, 6, 7, 17
[25] Yuxin Fang, Wen Wang, Binhui Xie, Quan Sun, Ledell Wu,
Xinggang Wang, Tiejun Huang, Xinlong Wang, and Yue
Cao. Eva: Exploring the limits of masked visual represen-
tation learning at scale. In Proceedings of the IEEE/CVF
Conference on Computer Vision and Pattern Recognition
(CVPR), pages 19358–19369, 2023. 3
[26] Chaoyou Fu, Peixian Chen, Yunhang Shen, Yulei Qin,
Mengdan Zhang, Xu Lin, Zhenyu Qiu, Wei Lin, Jin-
rui Yang, Xiawu Zheng, Ke Li, Xing Sun, and Ron-
grong Ji. Mme: A comprehensive evaluation benchmark
for multimodal large language models. arXiv preprint
arXiv:2306.13394, 2023. 2, 6
[27] Peng Gao, Jiaming Han, Renrui Zhang, Ziyi Lin, Shijie
Geng, Aojun Zhou, W. Zhang, Pan Lu, Conghui He, Xi-
angyu Yue, Hongsheng Li, and Yu Jiao Qiao. Llama-
adapter v2: Parameter-efficient visual instruction model.
ArXiv, abs/2304.15010, 2023. 6, 7, 17
[28] Yuying Ge, Yixiao Ge, Ziyun Zeng, Xintao Wang, and Ying
Shan. Planting a seed of vision in large language model. 3
[29] Jiaxi Gu, Xiaojun Meng, Guansong Lu, Lu Hou, Niu
Minzhe, Xiaodan Liang, Lewei Yao, Runhui Huang, Wei
Zhang, Xin Jiang, et al. Wukong: A 100 million large-scale
chinese cross-modal pre-training benchmark. Advances in
Neural Information Processing Systems, 35:26418–26431,
2022. 4
[30] Conghui He, Zhenjiang Jin, Chaoxi Xu, Jiantao Qiu, Bin
Wang, Wei Li, Hang Yan, Jiaqi Wang, and Da Lin. Wan-
juan: A comprehensive multimodal dataset for advancing
english and chinese large models. ArXiv, abs/2308.10755,
2023. 4, 14
[31] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-
Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu
Chen. LoRA: Low-rank adaptation of large language mod-
els. In International Conference on Learning Representa-
tions, 2022. 5, 14
[32] W. Hu, Y . Xu, Y . Li, W. Li, Z. Chen, and Z. Tu. Bliva:
A simple multimodal llm for better handling of text-rich
visual questions. ArXiv, abs/2308.09936, 2023. 6
[33] Ziniu Hu, Ahmet Iscen, Chen Sun, Zirui Wang, Kai-Wei
Chang, Yizhou Sun, Cordelia Schmid, David A Ross,
and Alireza Fathi. Reveal: Retrieval-augmented visual-
language pre-training with multi-source multimodal knowl-
edge memory. In Proceedings of the IEEE/CVF Confer-
ence on Computer Vision and Pattern Recognition (CVPR),
pages 23369–23379, 2023. 3
[34] Drew A Hudson and Christopher D Manning. Gqa: A new
dataset for real-world visual reasoning and compositional
question answering. Conference on Computer Vision and
Pattern Recognition (CVPR), 2019. 4
[35] Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana
Parekh, Hieu Pham, Quoc Le, Yun-Hsuan Sung, Zhen Li,
and Tom Duerig. Scaling up visual and vision-language
representation learning with noisy text supervision. In Pro-
ceedings of the International Conference on Machine learn-
ing (ICML), pages 4904–4916. PMLR, 2021. 3
[36] Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch,
Chris Bamford, Devendra Singh Chaplot, Diego de las
Casas, Florian Bressand, Gianna Lengyel, Guillaume Lam-
ple, Lucile Saulnier, L ´elio Renard Lavaud, Marie-Anne
Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril,
Thomas Wang, Timoth ´ee Lacroix, and William El Sayed.
Mistral 7b, 2023. 3
[37] Jing Yu Koh, Ruslan Salakhutdinov, and Daniel Fried.
Grounding language models to images for multimodal in-
puts and outputs. 2023. 3
[38] Andreas K ¨opf, Yannic Kilcher, Dimitri von R ¨utte, Sotiris
Anagnostidis, Zhi-Rui Tam, Keith Stevens, Abdullah
Barhoum, Nguyen Minh Duc, Oliver Stanley, Rich ´ard
Nagyfi, Shahul ES, Sameer Suri, David Glushkov, Arnav
Dantuluri, Andrew Maguire, Christoph Schuhmann, Huu
Nguyen, and Alexander Mattick. Openassistant conver-
sations – democratizing large language model alignment,
2023. 4
[39] Hugo Laurenc ¸on, Lucile Saulnier, L´eo Tronchon, Stas Bek-
man, Amanpreet Singh, Anton Lozhkov, Thomas Wang,
Siddharth Karamcheti, Alexander M. Rush, Douwe Kiela,
Matthieu Cord, and Victor Sanh. Obelics: An open web-
scale filtered dataset of interleaved image-text documents,
2023. 7
[40] Bohao Li, Rui Wang, Guangzhi Wang, Yuying Ge, Yix-
iao Ge, and Ying Shan. Seed-bench: Benchmarking multi-
modal llms with generative comprehension, 2023. 2, 6
[41] Bo Li, Yuanhan Zhang, Liangyu Chen, Jinghao Wang,
10

Jingkang Yang, and Ziwei Liu. Otter: A multi-modal model
with in-context instruction tuning. arXiv.org, 2023. 3, 6, 7,
17
[42] Junnan Li, Dongxu Li, Silvio Savarese, and Steven C. H.
Hoi. Blip-2: Bootstrapping language-image pre-training
with frozen image encoders and large language models.
ArXiv, abs/2301.12597, 2023. 2, 3, 4, 17
[43] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi.
Blip: Bootstrapping language-image pre-training for uni-
fied vision-language understanding and generation. In Pro-
ceedings of the International Conference on Machine learn-
ing (ICML), pages 12888–12900. PMLR, 2022. 3, 7
[44] Juncheng Li, Kaihang Pan, Zhiqi Ge, Minghe Gao, Han-
wang Zhang, Wei Ji, Wenqiao Zhang, Tat-Seng Chua,
Siliang Tang, and Yueting Zhuang. Empowering vision-
language models to follow interleaved vision-language in-
structions. ArXiv, abs/2308.04152, 2023. 6
[45] Liunian Harold Li*, Pengchuan Zhang*, Haotian Zhang*,
Jianwei Yang, Chunyuan Li, Yiwu Zhong, Lijuan Wang,
Lu Yuan, Lei Zhang, Jenq-Neng Hwang, Kai-Wei Chang,
and Jianfeng Gao. Grounded language-image pre-training.
In Proceedings of the IEEE/CVF Conference on Computer
Vision and Pattern Recognition (CVPR), 2022. 3
[46] Yunxin Li, Baotian Hu, Xinyu Chen, Lin Ma, Yong Xu, and
Min Zhang. Lmeye: An interactive perception network for
large language models, 2023. 6
[47] Fangyu Liu, Guy Edward Toh Emerson, and Nigel Collier.
Visual spatial reasoning. Transactions of the Association
for Computational Linguistics, 2023. 4
[48] Fuxiao Liu, Kevin Lin, Linjie Li, Jianfeng Wang, Yaser
Yacoob, and Lijuan Wang. Aligning large multi-modal
model with robust instruction tuning. arXiv preprint
arXiv:2306.14565, 2023. 4
[49] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee.
Improved baselines with visual instruction tuning. arXiv
preprint arXiv:2310.03744, 2023. 6, 7, 17
[50] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae
Lee. Visual instruction tuning. arXiv.org, 2023. 2, 3, 4, 6,
7, 17
[51] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao
Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun
Zhu, et al. Grounding dino: Marrying dino with grounded
pre-training for open-set object detection. arXiv.org, 2023.
3
[52] Yuan Liu, Haodong Duan, Yuanhan Zhang, Bo Li,
Songyang Zhnag, Wangbo Zhao, Yike Yuan, Jiaqi Wang,
Conghui He, Ziwei Liu, Kai Chen, and Dahua Lin. Mm-
bench: Is your multi-modal model an all-around player?
arXiv:2307.06281, 2023. 2, 6, 7
[53] Yulong Liu, Guibo Zhu, Bin Zhu, Qi Song, Guojing Ge,
Haoran Chen, GuanHui Qiao, Ru Peng, Lingxiang Wu,
and Jinqiao Wang. Taisu: A 166m large-scale high-quality
dataset for chinese vision-language pre-training. Advances
in Neural Information Processing Systems , 35:16705–
16717, 2022. 4
[54] Ziwei Liu, Zhongqi Miao, Xiaohang Zhan, Jiayun Wang,
Boqing Gong, and Stella X. Yu. Large-scale long-tailed
recognition in an open world. In CVPR, Jun 2019. 2
[55] Pan Lu, Swaroop Mishra, Tanglin Xia, Liang Qiu, Kai-
Wei Chang, Song-Chun Zhu, Oyvind Tafjord, Peter Clark,
and Ashwin Kalyan. Learn to explain: Multimodal rea-
soning via thought chains for science question answer-
ing. Advances in Neural Information Processing Systems,
35:2507–2521, 2022. 4
[56] Pan Lu, Liang Qiu, Jiaqi Chen, Tony Xia, Yizhou Zhao,
Wei Zhang, Zhou Yu, Xiaodan Liang, and Song-Chun Zhu.
Iconqa: A new benchmark for abstract diagram under-
standing and visual language reasoning. arXiv preprint
arXiv:2110.13214, 2021. 4
[57] Kenneth Marino, Mohammad Rastegari, Ali Farhadi, and
Roozbeh Mottaghi. Ok-vqa: A visual question answering
benchmark requiring external knowledge. In Proceedings
of the IEEE/cvf conference on computer vision and pattern
recognition, pages 3195–3204, 2019. 4
[58] Anand Mishra, Shashank Shekhar, Ajeet Kumar Singh, and
Anirban Chakraborty. Ocr-vqa: Visual question answering
by reading text in images. In ICDAR, 2019. 4
[59] MEJ Newman. Power laws, pareto distributions and zipf’s
law. Contemporary Physics, page 323–351, Sep 2005. 2
[60] OpenAI. Chatgpt. https://openai.com/blog/
chatgpt, 2022. 2, 3, 8
[61] OpenAI. Gpt-4 technical report, 2023. 2, 8
[62] Vicente Ordonez, Girish Kulkarni, and Tamara L. Berg.
Im2text: Describing images using 1 million captioned
photographs. In Neural Information Processing Systems
(NIPS), 2011. 2, 4
[63] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Car-
roll Wainwright, Pamela Mishkin, Chong Zhang, Sand-
hini Agarwal, Katarina Slama, Alex Ray, et al. Training
language models to follow instructions with human feed-
back. Advances in Neural Information Processing Systems
(NeurIPS), 35:27730–27744, 2022. 3
[64] Guilherme Penedo, Quentin Malartic, Daniel Hesslow,
Ruxandra Cojocaru, Alessandro Cappelli, Hamza Alobei-
dli, Baptiste Pannier, Ebtesam Almazrouei, and Julien Lau-
nay. The refinedweb dataset for falcon llm: Outperforming
curated corpora with web data, and web data only, 2023. 3
[65] Zhiliang Peng, Wenhui Wang, Li Dong, Yaru Hao, Shaohan
Huang, Shuming Ma, and Furu Wei. Kosmos-2: Grounding
multimodal large language models to the world. arXiv.org,
2023. 3, 7
[66] Qwen. Introducing qwen-7b: Open foundation and human-
aligned models (of the state-of-the-arts), 2023. 2, 3, 8
[67] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya
Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry,
Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learn-
ing transferable visual models from natural language super-
vision. In Proceedings of the International Conference on
Machine learning (ICML), pages 8748–8763. PMLR, 2021.
2, 3, 15
[68] Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya
Sutskever, et al. Improving language understanding by gen-
erative pre-training. 2018. 3
[69] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine
Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li,
and Peter J Liu. Exploring the limits of transfer learning
with a unified text-to-text transformer. Journal of Machine
Learning Research (JMLR), 21(1):5485–5551, 2020. 2, 3
11

[70] Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey
Chu, and Mark Chen. Hierarchical text-conditional image
generation with clip latents. 2
[71] Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott
Gray, Chelsea V oss, Alec Radford, Mark Chen, and Ilya
Sutskever. Zero-shot text-to-image generation. ICML, Jul
2021.
[72] Robin Rombach, Andreas Blattmann, Dominik Lorenz,
Patrick Esser, and Bj ¨orn Ommer. High-resolution image
synthesis with latent diffusion models. In CVPR, pages
10684–10695, June 2022.
[73] Chitwan Saharia, William Chan, Saurabh Saxena, Lala
Li, Jay Whang, Emily Denton, Seyed Kamyar, Seyed
Ghasemipour, Burcu Karagol, SSara Mahdavi, RaphaGon-
tijo Lopes, Tim Salimans, Jonathan Ho, DavidJ Fleet, and
Mohammad Norouzi. Photorealistic text-to-image diffusion
models with deep language understanding. 2
[74] Christoph Schuhmann, Romain Beaumont, Richard Vencu,
Cade Gordon, Ross Wightman, Mehdi Cherti, Theo
Coombes, Aarush Katta, Clayton Mullis, Mitchell Worts-
man, et al. Laion-5b: An open large-scale dataset for train-
ing next generation image-text models. Advances in Neural
Information Processing Systems, 35:25278–25294, 2022. 4
[75] Christoph Schuhmann, Richard Vencu, Romain Beaumont,
Robert Kaczmarczyk, Clayton Mullis, Aarush Katta, Theo
Coombes, Jenia Jitsev, and Aran Komatsuzaki. Laion-
400m: Open dataset of clip-filtered 400 million image-text
pairs. arXiv preprint arXiv:2111.02114, 2021. 2, 4
[76] Dustin Schwenk, Apoorv Khandelwal, Christopher Clark,
Kenneth Marino, and Roozbeh Mottaghi. A-okvqa: A
benchmark for visual question answering using world
knowledge. In European Conference on Computer Vision,
pages 146–162. Springer, 2022. 4
[77] Wenqi Shao, Yutao Hu, Peng Gao, Meng Lei, Kaipeng
Zhang, Fanqing Meng, Peng Xu, Siyuan Huang, Hong-
sheng Li, Yu Qiao, et al. Tiny lvlm-ehub: Early multimodal
experiments with bard. arXiv preprint arXiv:2308.03729,
2023. 2
[78] Piyush Sharma, Nan Ding, Sebastian Goodman, and Radu
Soricut. Conceptual captions: A cleaned, hypernymed, im-
age alt-text dataset for automatic image captioning. In Pro-
ceedings of the 56th Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers), pages
2556–2565, 2018. 2, 4
[79] Oleksii Sidorov, Ronghang Hu, Marcus Rohrbach, and
Amanpreet Singh. Textcaps: a dataset for image caption-
ing with reading comprehension. In Computer Vision–
ECCV 2020: 16th European Conference, Glasgow, UK, Au-
gust 23–28, 2020, Proceedings, Part II 16, pages 742–758.
Springer, 2020. 4
[80] Amanpreet Singh, Vivek Natarajan, Meet Shah, Yu Jiang,
Xinlei Chen, Dhruv Batra, Devi Parikh, and Marcus
Rohrbach. Towards vqa models that can read. In Proceed-
ings of the IEEE/CVF conference on computer vision and
pattern recognition, pages 8317–8326, 2019. 4
[81] Krishna Srinivasan, Karthik Raman, Jiecao Chen, Michael
Bendersky, and Marc Najork. Wit: Wikipedia-based im-
age text dataset for multimodal multilingual machine learn-
ing. In Proceedings of the 44th International ACM SIGIR
Conference on Research and Development in Information
Retrieval, pages 2443–2449, 2021. 14
[82] Quan Sun, Qiying Yu, Yufeng Cui, Fan Zhang, Xiaosong
Zhang, Yueze Wang, Hongcheng Gao, Jingjing Liu, Tiejun
Huang, and Xinlong Wang. Generative pretraining in mul-
timodality. Jul 2023. 3
[83] Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann Dubois,
Xuechen Li, Carlos Guestrin, Percy Liang, and Tatsunori B.
Hashimoto. Stanford alpaca: An instruction-following
llama model. https://github.com/tatsu-lab/
stanford_alpaca, 2023. 3, 4
[84] InternLM Team. Internlm: A multilingual language model
with progressively enhanced capabilities. https://
github.com/InternLM/InternLM , 2023. 2, 3, 4,
8
[85] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
Martinet, Marie-Anne Lachaux, Timoth ´ee Lacroix, Bap-
tiste Rozi `ere, Naman Goyal, Eric Hambro, Faisal Azhar,
et al. Llama: Open and efficient foundation language mod-
els. arXiv.org, 2023. 2, 3
[86] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert,
Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov,
Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al.
Llama 2: Open foundation and fine-tuned chat models,
2023. 2, 3, 8
[87] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser,
and Illia Polosukhin. Attention is all you need. Advances
in Neural Information Processing Systems (NeurIPS), 30,
2017. 3
[88] Bin Wang, Fan Wu, Xiao Han, Jiahui Peng, Huaping
Zhong, Pan Zhang, Xiaoyi Dong, Weijia Li, Wei Li, Jiaqi
Wang, et al. Vigc: Visual instruction generation and correc-
tion. arXiv.org, 2023. 3, 4
[89] Weihan Wang, Qingsong Lv, Wenmeng Yu, Wenyi Hong, Ji
Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Xixuan
Song, Jiazheng Xu, Bin Xu, Juanzi Li, Yuxiao Dong, Ming
Ding, and Jie Tang. Cogvlm: Visual expert for pretrained
language models, 2023. 3
[90] Haoning Wu, Zicheng Zhang, Erli Zhang, Chaofeng Chen,
Liang Liao, Annan Wang, Chunyi Li, Wenxiu Sun, Qiong
Yan, Guangtao Zhai, et al. Q-bench: A benchmark for
general-purpose foundation models on low-level vision.
arXiv preprint arXiv:2309.14181, 2023. 2, 7
[91] Peng Xu, Wenqi Shao, Kaipeng Zhang, Peng Gao, Shuo
Liu, Meng Lei, Fanqing Meng, Siyuan Huang, Yu Qiao,
and Ping Luo. Lvlm-ehub: A comprehensive evaluation
benchmark for large vision-language models, 2023. 16
[92] An Yang, Junshu Pan, Junyang Lin, Rui Men, Yichang
Zhang, Jingren Zhou, and Chang Zhou. Chinese clip: Con-
trastive vision-language pretraining in chinese. arXiv.org,
2022. 2, 3, 4
[93] Michihiro Yasunaga, Armen Aghajanyan, Weijia Shi,
Richard James, Jure Leskovec, Percy Liang, Mike Lewis,
Luke Zettlemoyer, and Wen-tau Yih. Retrieval-augmented
multimodal language modeling. 2023. 3
[94] Qinghao Ye, Haiyang Xu, Guohai Xu, Jiabo Ye, Ming Yan,
Yiyang Zhou, Junyang Wang, Anwen Hu, Pengcheng Shi,
Yaya Shi, et al. mplug-owl: Modularization empowers
12

large language models with multimodality.arXiv.org, 2023.
3, 6, 7
[95] Shukang Yin, Chaoyou Fu, Sirui Zhao, Ke Li, Xing Sun,
Tong Xu, and Enhong Chen. A survey on multimodal large
language models. arXiv preprint arXiv:2306.13549, 2023.
2
[96] Lili Yu, Bowen Shi, Ramakanth Pasunuru, Benjamin
Muller, Olga Golovneva, Tianlu Wang, Arun Babu, Binh
Tang, Brian Karrer, Shelly Sheynin, Candace Ross, Adam
Polyak, Russell Howes, Vasu Sharma, Puxin Xu, Hov-
hannes Tamoyan, Oron Ashual, Uriel Singer, Shang-Wen
Li, Susan Zhang, Gargi Ghosh, Yaniv Taigman, Maryam
Fazel-Zarandi, Asli Celikyilmaz, Luke Zettlemoyer, and
Armen Aghajanyan. Scaling autoregressive multi-modal
models: Pretraining and instruction tuning. 3
[97] Aohan Zeng, Xiao Liu, Zhengxiao Du, Zihan Wang, Hanyu
Lai, Ming Ding, Zhuoyi Yang, Yifan Xu, Wendi Zheng,
Xiao Xia, Weng Lam Tam, Zixuan Ma, Yufei Xue, Jidong
Zhai, Wenguang Chen, Zhiyuan Liu, Peng Zhang, Yuxiao
Dong, and Jie Tang. GLM-130b: An open bilingual pre-
trained model. In The Eleventh International Conference
on Learning Representations (ICLR), 2023. 3
[98] Yan Zeng, Hanbo Zhang, Jiani Zheng, Jiangnan Xia, Guo-
qiang Wei, Yang Wei, Yuchen Zhang, and Tao Kong. What
matters in training a gpt4-style language model with multi-
modal inputs? ArXiv, abs/2307.02469, 2023. 6, 17
[99] Haotian Zhang, Pengchuan Zhang, Xiaowei Hu, Yen-Chun
Chen, Liunian Li, Xiyang Dai, Lijuan Wang, Lu Yuan,
Jenq-Neng Hwang, and Jianfeng Gao. Glipv2: Unifying
localization and vision-language understanding. Advances
in Neural Information Processing Systems (NeurIPS) ,
35:36067–36080, 2022. 3
[100] Susan Zhang, Stephen Roller, Naman Goyal, Mikel
Artetxe, Moya Chen, Shuohui Chen, Christopher Dewan,
Mona Diab, Xian Li, Xi Victoria Lin, et al. Opt: Open
pre-trained transformer language models, 2022. arXiv.org.
3
[101] Haozhe Zhao, Zefan Cai, Shuzheng Si, Xiaojian Ma, Kaikai
An, Liang Chen, Zixuan Liu, Sheng Wang, Wenjuan Han,
and Baobao Chang. Mmicl: Empowering vision-language
model with multi-modal in-context learning. arXiv.org,
2023. 3, 6
[102] Haozhe Zhao, Zefan Cai, Shuzheng Si, Xiaojian Ma,
Kaikai An, Liang Chen, Zixuan Liu, Sheng Wang, Wen-
juan Han, and Baobao Chang. Mmicl: Empowering
vision-language model with multi-modal in-context learn-
ing. ArXiv, abs/2309.07915, 2023. 6
[103] Zhiyuan Zhao, Linke Ouyang, Bin Wang, Siyuan Huang,
Pan Zhang, Xiaoyi Dong, Jiaqi Wang, and Conghui He.
Mllm-dataengine: An iterative refinement approach for
mllm. arXiv.org, 2023. 3
[104] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and
Mohamed Elhoseiny. Minigpt-4: Enhancing vision-
language understanding with advanced large language
models. arXiv.org, 2023. 2, 3, 6, 7, 17
[105] Wanrong Zhu, Jack Hessel, Anas Awadalla, Samir Yitzhak
Gadre, Jesse Dodge, Alex Fang, Youngjae Yu, Ludwig
Schmidt, William Yang Wang, and Yejin Choi. Multimodal
c4: An open, billion-scale corpus of images interleaved
with text. arXiv preprint arXiv:2304.06939, 2023. 4
13

A. Experiment Details
A.1. Pre-training
The multi-modal pre-training process employs 1.1 billion
images alongside 77.7 billion text tokens, including both
public datasets and in-house concept data (Sec. B) collected
from public websites, possessing over 11 million semantic
concepts. The paired and interleaved text-image data in-
cludes 50.6 billion English text tokens and 17.1 billion Chi-
nese text tokens. Furthermore, approximately 10 billion text
tokens (5 billion English text and 5 billion Chinese text),
sampled from the InternLM pre-training dataset [30], are in-
corporated to maintain the model’s linguistic proficiencies.
Prior to the training process, all pre-training data underwent
a thorough cleaning procedure to ensure its quality and re-
liability.
The optimization algorithm employed is AdamW, with
hyperparameter settings as follows: β1=0.9, β2=0.95, eps
=1e-8. The maximum learning rates for the perceive sam-
pler and the large language model are configured at 2e-4 and
4e-5, respectively, following a cosine learning rate sched-
ule. The minimum learning rate is set at 1e-5. Additionally,
a linear warm-up is applied over the initial 200 steps. The
training procedure employs a batch size of approximately
15.7 million tokens and spans 8,000 iterations. Utilizing
such a large batch size in conjunction with a limited number
of iterations contributes to stable training dynamics while
also aiding in the preservation of LLM’s inherent capabili-
ties. The overall multi-modal pre-training process requires
128 Nvidia A100 GPUs for around 80 hours.
A.2. Supervised Fine-tuning
We adopt the Low-Rank Adaption (LoRA) [31] for the su-
pervised fine-tuning process, which is composed of aMulti-
task Training phase and a Instruction Tuning phase. The
perceive sampler is concurrently trained, albeit with a dis-
tinct learning rate. Specifically, LoRA is applied to both
the attention layer and the feed-forward network (FFN).
We find that a high LoRA rank is conducive to imbuing
the model with new capabilities; consequently, we set the
LoRA rank and alpha parameter both to 256. The model is
trained using a global batch size of 256 over 18,000 itera-
tions in Multi-task Trainingphase. The learning rates are
set to 5e−5 for the LoRA layer and 2e−5 for the perceive
sampler.
For the Instruction Tuning phase, we maintain a batch
size of 256 and execute the tuning over 1000 iterations with
a small learning rate 1e−5.
B. Concept Data
As illustrated by Figure A4 and Figure A5, our concept
dataset is curated from Wikipedia3 and Baidu Baike4, com-
prising 2 million English vision-language concepts and 9
million Chinese vision-language concepts. Each concept
consists of an image paired with corresponding descrip-
tions. Examples are illustrated in Figure A6 and Figure A7.
In comparison to the WIT [81] dataset, which comprises ap-
proximately 2 million multimodal English and Chinese con-
cepts after removing expired links and noisy samples, our
multimodal concept data significantly surpasses it in terms
of data volume and diversity.
Experimental results.Here, we study the effectiveness of
the concept dataset on our framework with three settings: 1)
remove our In-house Concept data. 2) replace our In-house
Concept data with the WIT [81] dataset. 3) the default pre-
training setting. As results shown in Table A13, compared
to the baseline, the WIT improves the model performance
on both English and Chinese benchmarks. Further, when
using our larger and more diverse In-house Concept dataset,
the model surpasses the WIT baseline by a large margin
on both benchmarks, especially on the Chinese knowledge-
based benchmark CCBench.
C. Interleaved Image-Text Composition
C.1. Format Details
Text Generation. As the interleaved image-text dataset
is collected from public websites, the acquired dataset
contains noise, particularly in the form of marketing and
advertising content. To address this, We utilize GPT-4
to assess whether an individual sentence contains noise
and identify the type of noise, which includes advertise-
ment, reference, and recommendations ( e.g., external ar-
ticles/answers). Any sentences identified as noisy are re-
moved, and articles containing more than 30% noisy sen-
tences are filtered out directly. After the cleaning, we for-
mulate the training data in the following manner:
<|User|> : Write an illustrated article based on the
given instruction:{Instruction} <eou>
<|Bot|> : [para1] . . .[paraN ] <eob>
Here, {Instruction} serves as a placeholder for the article-
crafted instruction, such as a simple title, or a draft outline,
etc. The [para1] and [paraN ] denote the first and last para-
graphs, respectively.
Image Spotting and Captioning.In practice, we formulate
the spotting and captioning task with the following format:
3https://www.wikipedia.org/
4https://baike.baidu.com/
14

Concept
Text
Image
Figure A4. Extract vision-language concepts from Wikipedia.
Concept
Text
Image
Figure A5. Extract vision-language concepts from Baidu Baike.
Concept-specific Data MMBench CCBench
- 72.9 44.0
WIT (2M) 73.5 45.1
In-house Concept data (11M) 74.4 47.6
Table A13. Ablation of the concept-specific data used in the pre-
training phase.
<|User|> : [seg1][para1] . . .[segN ][paraN ] Based
on the above text, select the appropriate
locations for inserting images and give
the image captions<eou>
<|Bot|> : I think images can be added under the{x1},
. . . ,{xk} paragraphs. The image captions are
as follows:{x1} paragraph: {cap1}, . . .,
{xk} paragraph: {capk} <eob>
Here, [seg1] serves as an index token to pinpoint the specific
paragraph index. The placeholders {x1} and {xk} repre-
sent the positions for the first and last image locations, re-
spectively. Correspondingly, {cap1} and {capk} act as the
generated captions associated with those image locations.
Image Retrieval and Selection.The training data is struc-
tured in the following manner:
<|User|> : [para1] . . .[parai][imgi][parai+1] . . .[paraj]
Based on the given context and candidate
images, select the appropriate image.
Candidate images include:[img1
j ] . . .[imgm
j ]
<eou>
<|Bot|> : The {selected index} image. <eob>
In this configuration, [imgi] denotes the image associated
with the ith paragraph. The terms [img1
j ], . . . ,[imgm
j ] rep-
resent the candidate images retrieved by CLIP [67] based
on {cap1}, . . . ,{capk} from an image pool. Meanwhile,
{selected index} acts as a placeholder indicating the index
of the final selected image.
C.2. Image-Text Composition Evaluation Details
Grading Criteria. Due to the lack of existing metrics to
evaluate the interleaved image-text article quality, we de-
signed a detailed user study metric, including eight dimen-
sions: four text-related dimensions (instruction following,
writing quality, logic, factualness), three image-related di-
mensions (image-text consistency, image informative, im-
age consistency), and one subjective preference. Each di-
mension contains three levels of score: Excellent (5 points),
Medium (3 points), and Poor (1 point).
With a given topic, the human expert and GPT4-V are
asked to grade the articles generated by different models
(in a double-blind manner) in each of the eight dimensions.
Specifically, for each time of scoring one article, the points
of four text-related dimensions are summarized and divided
by the full score of text (20 points) into a text-related score,
and the three image-related dimensions are summarized and
divided by the full score of image (15 points) into an image-
related score. The subjective preference is divided by five
into a subjective preference score. The average score, which
is the average number of the text-related score, the image-
related score, and the subjective preference score, is taken
as the overall result for a human expert or the GPT4-V . The
scores of 10 human experts are averaged for the final human
evaluation result. The GPT4-V assessments are performed
three times to calculate the average GPT4-V score.
Details of Eight Evaluation Dimensions.The details of
each of the eight dimensions are as follows:
1) Instruction followingevaluate the content based on the
degree of task completion, and evaluate whether the gener-
ated article conforms to the given topic and meets the style
required by the topic (such as meeting the specified title,
complying with the given abstract, keywords, outline, etc.).
Scoring Levels:
1 point: Severely non-compliant with instructions;
3 points: Basically compliant with instructions;
15

GPT4-Vision Evaluation Prompt
There is an interleaved text-image article that should follow the instruction:
{Instruction}
The article’s content:
{Article content}
Based on the given instruction and article, please evaluate this article by
answering the following questions:
Please evaluate whether the article meets the requirements and
choose the score from the given scoring level in each question:
Q1: {Q1}
. . .
Q8: {Q8}
Please give a rating for each question one by one and explain the reason.
The output format should be:
”Final Score:
Q1: (1 or 3 or 5) points, Reason: xxx
. . .
Q8: (1 or 3 or 5) points, Reason: xxx ”
Table A14. The prompt used for GPT4-V evaluation.
{Instruction}, {Article content}, and {Q1} . . .{Q8} will be re-
placed by the instruction, the interleaved image-text article, and
explanations and scoring levels of eight dimensions, respectively.
5 points: Highly compliant with instructions.
2) Writing qualityevaluate the language quality based on
the content of the article (including but not limited to vocab-
ulary, grammar, word choice and sentence making, etc.). It
requires accurate word expression, rich language, and cor-
rect grammar. Scoring Levels:
1 point: Poor;
3 points: Medium;
5 points: Excellent.
3) Logicevaluate the article based on the logical rationality
of the content (the content of the article should try to follow
the common rules in daily life, have clear cause and effect
relationships, and have no obvious logical fallacies, etc.).
Scoring Levels:
1 point: Severe logical errors (3 or more instances);
3 points: Minor logical errors (1-3 instances);
5 points: Clear logic and explicit cause-and-effect rela-
tionship.
4) Factualnessevaluate the article based on the accuracy of
the content (the content of the article should be as consistent
as possible with common sense of life and scientific knowl-
edge, without illusions or fabricated facts, and the use of
relevant documents and materials should be reasonable and
appropriate). Scoring Levels:
1 point: Severe factual errors or delusions (3 or more
instances);
3 points: Minor factual errors or delusions (1-3 in-
stances);
5 points: Factually correct, with no obvious delusions or
fabrications.
5) Image-text consistencyevaluate the relevance of the im-
ages to the topic of the article. Scoring Levels:
1 point: The illustration is unrelated to the article’s
theme;
3 points: The illustration is related to the article’s theme,
but not closely;
5 points: The illustration is closely related to the article’s
theme.
6) Image informativeevaluate the relevance of the main
content of the accompanying images and related para-
graphs, and the informativeness of the images. Scoring Lev-
els:
1 point: The illustration is completely uninformative;
3 points: The illustration is related to the main content
of the relevant paragraph;
5 points: In addition to the above, the illustration also
conveys extra supplementary information not present in the
article.
7) Image consistencyevaluate the subject consistency be-
tween the accompanying pictures (for instance, when writ-
ing about my cat, the accompanying image should ideally
be of the same cat.). Scoring Levels:
1 point: The subjects in some illustrations differ greatly;
3 points: The subjects in some illustrations appear simi-
lar, but upon closer examination, differences exist;
5 points: Completely satisfies image consistency.
8) Subjective preferenceis an overall subjective score about
the quality of the generated article. Scoring Levels:
1 point: Poor;
3 points: Medium;
5 points: Excellent.
GPT4-V Evaluation.Besides human experts, we leverage
GPT4-V api, which can take interleaved text-image arti-
cles as inputs for evaluation. The input prompt format is
shown in Table A14. {Instruction}, {Article content} will
be replaced by the requirements of the article and the com-
posed interleaved image-text article during evaluation, re-
spectively. {Q1}. . .{Q8} indicates the explanations and
scoring levels of eight dimensions as in Details of Eight
Evaluation Dimensions, e.g., ”Instruction following evalu-
ate the content. . .Scoring Levels: . . .”. We manually check
the output of the GPT4-V api to collect the final score.
D. More Benchmark results.
Tiny LVLM[91] is an ability-level benchmark, which eval-
uates the MLLM performance from five different abili-
ties. We report the results in Table A15. Our InternLM-
Xcomposer-VL gets the best overall results and the Top-3
performance in most abilities, even surpassing a commer-
cial MLLM, i.e., Google Bard.
5https://bard.google.com/.
Refer to Tiny LVLM at https://github.com/OpenGVLab/Multi-Modality-
Arena/tree/main/tiny lvlm evaluation
16

Method Overall VR VP VKA VC OH
MiniGPT-4 [104] 192.6 37.6 37.8 17.6 49.0 50.7
LLaV A [50] 197.0 41.6 38.3 18.7 49.4 49.0
VisualGLM [24] 211.9 37.3 36.3 46.9 37.6 54.0
Otter [41] 216.4 41.6 37.0 15.1 52.4 74.0
LLaMA-A-V2 [27] 229.2 43.5 46.8 22.3 56.0 60.7
Lynx [98] 279.2 52.2 65.8 17.6 57.4 86.3
BLIP2 [42] 284.7 44.9 49.0 64.1 44.0 82.7
InstructBLIP [18] 300.6 46.7 48.0 61.7 59.2 85.0
LLaV A-1.5 [49] 307.2 55.6 49.0 57.0 57.2 88.3
Qwen-VL-Chat [4] 316.8 62.4 54.5 55.1 54.8 90.0
Bard 5 319.6 64.2 57.0 68.1 59.6 70.7
Ours 322.5 55.8 53.8 64.1 61.8 87.0
Table A15. Evaluation of Tiny LVLM test set. Here we report all
the sub-tasks, including visual reasoning (VR), visual perception
(VP), visual knowledge acquisition (VKA), visual commonsense
(VC), and object hallucination (OH).
E. More Qualitative Results.
Figure A8-A13 shows some interleaved image-text com-
positions generated by InternLM-XComposer. Figure A14
and Figure A15 give some conversation cases when chat-
ting with InternLM-XComposer. Our model exhibits an ex-
cellent ability in multilingual interleaved composition and
conversation.
17

Château de Brantes
The Château de Brantes is an 18th-century manor house with a contemporary garden inspired by the 
gardens of Tuscany, located in the town of Sorgues in the Vaucluse Department of France. The 
gardens are classified by the French Ministry of Culture among the Remarkable Gardens of France.
POP tennis
POP tennis (originally known as paddle tennis) is a racket sport adapted from tennis and 
played for over a century. Compared to tennis, the court is smaller, has no doubles lanes, 
and the net is lower. Paddle tennis is played with a solid perforated paddle, as opposed to a 
strung racquet, and a lower pressure tennis ball. The same court is used for both singles 
and doubles, with doubles being the dominant form of play. The smaller court size adds a 
strong emphasis and advantage to net play and creates a fast and reaction-based game. 
Growing in popularity, local leagues and tournaments can be found worldwide.
Alluvial plain
An alluvial plain is a largely flat landform created by the deposition of sediment over a long 
period of time by one or more rivers coming from highland regions, from which alluvial soil 
forms. A floodplain is part of the process, being the smaller area over which the rivers flood 
at a particular period of time, whereas the alluvial plain is the larger area representing the 
region over which the floodplains have shifted over geological time.
Aeronca Champion
The Aeronca Model 7 Champion, commonly known as the "Champ", or "Airknocker", is a 
single-engine light airplane with a high wing, generally configured with fixed conventional 
landing gear and tandem seating for two occupants. 
Tijuana River
The Tijuana River (Spanish: Río Tijuana) is an intermittent river, 120 mi (195 km) long, near 
the Pacific coast of northern Baja California state in northwestern Mexico and Southern 
California in the western United States. The river is heavily polluted with raw sewage from 
the city of Tijuana, Mexico.
Ficus microcarpa
Ficus microcarpa, also known as Chinese banyan, Malayan banyan, Indian laurel, curtain fig, 
or gajumaru (ガジュマル), is a tree in the fig family Moraceae. It is native in a range from 
China through tropical Asia and the Caroline Islands to Australia. It is widely planted as a 
shade tree and frequently misidentified as F. retusa or as F. nitida (syn. F. benjamina)
The Flintstone Kids
The Flintstone Kids is an American animated television series produced by Hanna-Barbera. 
It is an alternative incarnation of the studio's original animated series The Flintstones. The 
series depicts juvenile versions of the main characters from the original show. It aired from 
September 13, 1986, to November 14, 1987, on ABC. Unlike the previous shows, this was 
the first Flintstone series not to have a laugh track.
Figure A6. Examples from our vision-language concept dataset.
18

青之岛
青之岛（日语：青ヶ岛，英语：Aogashima）是日本伊豆群岛南部一座火山岛，是伊
豆群岛中有人居住的最南端的岛屿，行政上属于日本东京都八丈支厅青岛村管辖。
草船借箭
草船借箭是中国古典名著《三国演义》中赤壁之战的一个故事。借箭由周瑜故意提出
（限十天内造十万支箭），机智的诸葛亮一眼识破是一条害人之计，却淡定表示“只
需要三天”。后来，有鲁肃帮忙，诸葛亮再利用曹操多疑的性格，调了二十条草船诱
敌，终于“借”到了十万余支箭。
雷暴
雷暴（thunderstorms），是热带和温带地区可见的局地性强对流天气。雷暴发生时
可伴随有雷击、闪电、强风和强降水，例如雨或冰雹。雷暴可发生于春季和夏季，常
见的例子是夏季午后，但也可能在冬季随暴风雪发生，被称为雷雪（thundersnow）。
乐山大佛
乐山大佛（Leshan Giant Buddha），又名凌云大佛，全称为“嘉州凌云寺大弥勒石
像”，位于四川省乐山市南岷江东岸凌云寺侧，濒大渡河、青衣江和岷江三江汇流处。
大佛为弥勒佛坐像，通高71米，是中国最大的一尊摩崖石刻造像。乐山大佛开凿于唐
代开元元年（713年），完成于贞元十九年（803年），历时约九十年。
对联
对联，又称对偶、门对、春贴、春联、对子、楹联等，是写在纸、布上或刻在竹子、
木头、柱子上的对偶语句。对联对仗工整，平仄协调，是一字一音的汉语独特的艺术
形式。对联是中国传统文化瑰宝。
兵马俑
兵马俑，即秦始皇陵兵马俑，亦简称秦兵马俑或秦俑，是第一批全国重点文物保护单
位、第一批中国世界遗产，位于今陕西省西安市临潼区秦始皇陵以东1.5千米处的兵
马俑坑内。
金门大桥
金门大桥（Golden Gate Bridge），又称“金门海峡大桥”，是美国境内连接旧金山
市区和北部的马林郡的跨海通道，位于金门海峡之上，是美国旧金山市的主要象征。
Figure A7. Examples from our vision-language concept dataset.
19

Shanghai Travel Guide
Shanghai is the largest city in China and one of the most populous cities
in the world, with a population of over 24 million people. The city is
known for its modern skyscrapers, bustling financial district, and vibrant
nightlife. Shanghai is also home to some of the country's top tourist
attractions, including the Bund, Yuyuan Garden, and the Oriental Pearl
Tower. In this guide, we'll provide you with all the information you need
to plan your trip to Shanghai, including tips on where to stay, what to do,
and how to get around.
Where to Stay in Shanghai
When it comes to finding a place to stay in Shanghai, there are plenty of
options to choose from. If you're looking for a luxury experience,
consider staying at one of the city's five-star hotels, such as the Fairmont
Peace Hotel or the Waldorf Astoria Shanghai on the Bund. These hotels
offer stunning views of the city skyline, luxurious amenities, and
impeccable service.
Tips for Visiting Shanghai
If you're looking for something more budget-friendly, there are plenty of
hostels and guesthouses throughout the city that offer affordable
accommodations. Some popular areas to stay include the Xintiandi
neighborhood, which is known for its trendy bars and restaurants, and
the French Concession, which is filled with charming cafes and
boutiques.
What to Do in Shanghai
One of the best ways to explore Shanghai is by taking a stroll along the
Bund, a waterfront promenade that offers stunning views of the city
skyline. You can also visit the Yu Garden, a traditional Chinese garden
that dates back to the Ming Dynasty, and the Shanghai Museum, which
houses an impressive collection of Chinese art and artifacts.
Another popular attraction in Shanghai is the Oriental Pearl Tower, a
television tower that offers panoramic views of the city. You can also
take a boat ride on the Huangpu River, which runs through the heart of
the city, and visit the Jade Buddha Temple, a Buddhist temple that
houses two jade Buddha statues.
How to Get Around in Shanghai
The best way to get around Shanghai is by using public transportation,
which includes buses, subways, and taxis. The city's subway system is
extensive and easy to use, with stations located throughout the city.
Buses are also a convenient way to get around, although they can be
crowded during rush hour.
Taxis are available throughout the city, but make sure to agree on a price
before getting into the taxi so you don't get ripped off. Another option is
to rent a bicycle or scooter, which will allow you to explore the city at
your own pace.
Tips for Visiting Shanghai
1. Dress appropriately: Shanghai is a conservative city, so it's important
to dress modestly when visiting temples and other religious sites. Cover
your shoulders and knees, and avoid wearing revealing clothing.
2. Learn some basic Mandarin: While many people in Shanghai speak
English, it's always helpful to know some basic Mandarin phrases, such
as "hello," "thank you," and "excuse me."
3. Be aware of pickpockets: Like any major city, Shanghai has its fair
share of pickpockets. Keep your valuables close to you and be vigilant
about your surroundings.
...
In conclusion, Shanghai is a vibrant and exciting city that offers
something for everyone. Whether you're interested in history, culture, or
just want to have a good time, Shanghai has it all. With its towering
skyscrapers, bustling streets, and rich cultural heritage, Shanghai is a
must-visit destination for anyone traveling to China
Write a travel guide titled “Shanghai 
Travel Guide”.
Figure A8. Interleaved composition generated by InternLM-XComposer.
20

Tips for Visiting Shanghai
以“又见敦煌”为题写一篇
旅游攻略。
又见敦煌
敦煌，位于甘肃省西北部，地处河西走廊西端，是古代丝绸之路
上的重要交通枢纽和商埠重镇。它拥有着丰富的历史文化遗产，
包括莫高窟、鸣沙山月牙泉、雅丹魔鬼城等著名景点。同时，敦
煌也是中国历史文化名城之一，有着深厚的文化底蕴和独特的民
俗风情。
一、莫高窟
莫高窟，又名“千佛洞”，是中国四大石窟之一，始建于十六国
的前秦时期，距今已有1600多年的历史。它是世界上现存规模最
大、内容最丰富的佛教艺术宝库，被誉为“东方卢浮宫”。莫高
窟内共有735个洞窟，壁画总面积达45000多平方米，彩塑佛像
5000余尊，是世界上最大的佛教艺术中心之一。在这里，游客可
以欣赏到精美的壁画、雕塑和音乐表演，感受佛教文化的博大精
深。
二、鸣沙山月牙泉
鸣沙山月牙泉是一处自然奇观，位于敦煌市西北约40公里处的沙
漠中。这里地势平坦，沙丘连绵起伏，形成了一片广袤无垠的沙
漠景观。而月牙泉则静静地镶嵌在这片沙漠之中，泉水清澈见底，
形状如新月，故称“月牙泉”。每到夜晚，月亮升起时，月牙泉
周围会发出阵阵清脆的响声，犹如天籁之音，令人心旷神怡。
三、雅丹魔鬼城
雅丹魔鬼城是一座典型的风蚀地貌，位于敦煌市西南约100公里
的戈壁滩上。这里的地貌奇特，呈现出一种荒凉、神秘、恐怖的
景象。由于长期受到风吹日晒雨淋，这里的岩石表面已经变得凹
凸不平，形成了各种形态各异的造型，有的像动物，有的像人物，
有的像建筑，让人不禁感叹大自然的鬼斧神工。
四、其他景点
除了莫高窟、鸣沙山月牙泉和雅丹魔鬼城之外，敦煌还有许多其
他值得一游的景点，如玉门关、阳关、锁阳城、汉长城遗址等。
这些景点都具有悠久的历史和文化价值，吸引着众多游客前来参
观游览。
五、特色美食
敦煌的特色美食也非常丰富，其中最有名的当属驴肉黄面了。驴
肉黄面是一道以驴肉为主要食材的面食，味道鲜香可口，深受当
地人和游客的喜爱。此外，还有羊肉泡馍、胡羊焖饼、烤全羊等
特色美食，都是不容错过的美味佳肴。
六、旅游小贴士
1. 敦煌气候干燥，日照强烈，紫外线较强，建议游客做好防晒
措施，携带防晒霜、遮阳帽、太阳镜等物品。2. 敦煌属于高原
地区，海拔较高，游客应注意休息，避免剧烈运动，以免出现高
原反应。3. 敦煌旅游景点较多，游客应提前规划好行程，合理
安排时间，避免走马观花，错过重要的景点。4. 在敦煌旅游期
间，要注意保护环境，不乱扔垃圾，不破坏文物古迹，做一个文
明的游客。总之，敦煌是一座历史悠久、文化底蕴深厚、风景优
美的城市，是一个值得一游的好去处。希望这篇文章能够帮助您
更好地了解敦煌，为您的旅行提供一些有用的信息。
Figure A9. Interleaved composition generated by InternLM-XComposer.
21

Tips for Visiting Shanghai
Write an article introducing World War 2 
with the title “The World War 2”.
The World War 2
World War II (WWII or WW2), also known as the Second World War,
was a global war that lasted from 1939 to 1945. It involved the vast
majority of the world's countries—including all of the great powers—
eventually forming two opposing military alliances: the Allies and the
Axis.
It was the most widespread war in history, with some 100 million
military personnel, including 60 million on the Allied side and 30
million on the Axis side, participating in more than 5,000 air battles,
land battles, and naval engagements in 60 countries across five
continents.
On September 1, 1939, Germany invaded Poland, marking the start of
Operation Barbarossa, the German invasion of the Soviet Union. On
December 7, 1941, Japan launched a surprise attack on Pearl Harbor,
Hawaii, resulting in the United States' entry into the war on the side of
the Allies.
In June 1941, Nazi Germany invaded the Soviet Union during Operation
Barbarossa. This marked the beginning of the largest tank battle in
history, the Battle of Kursk, which took place between July 12 and
August 23, 1943. The Soviets were able to inflict heavy losses on the
Germans, forcing them to retreat back to their original positions.
The Battle of Stalingrad, which took place between August 1942 and
February 1943, was one of the bloodiest battles in human history.
During this time, the Red Army suffered an estimated 900,000
casualties, while the Wehrmacht lost approximately 600,000 soldiers.
The Battle of El Alamein, which took place between October 1942 and
November 1943, was another major turning point in the war. Here, the
British Eighth Army under General Bernard Montgomery defeated the
German Afrika Korps led by Field Marshal Erwin Rommel at the Sidi
Rezegh Pass near Tobruk, Libya.
This victory allowed the Allies to gain control of much of North Africa
and paved the way for the eventual defeat of Adolf Hitler's forces in
Europe.
The Battle of Midway, which took place between June 4-7, 1942, saw
the U.S. Navy decisively defeat the Imperial Japanese Navy off the coast
of Midway Atoll in the Pacific Ocean. This victory helped turn the tide
of the war in favor of the Allies.
The Battle of Normandy, which took place between June 6-July 29,
1944, was the largest amphibious invasion in history. Over 160,000
Allied troops landed on the beaches of Normandy, France, supported by
over 10,000 aircraft and nearly 5,000 landing craft.
After several weeks of fierce fighting, the Allies had secured a foothold
in France and were able to begin advancing towards Germany.
The Battle of the Bulge, which took place between December 16, 1944,
and January 25, 1945, was a last-ditch attempt by the German army to
break through the Allied lines and end the war before it could be
officially declared.
Despite being outnumbered and outgunned, the Allies were able to repel
the German offensive and continue their advance towards Germany.
The Battle of Okinawa, which took place between April 1-May 22, 1945,
was the final major battle of the Pacific Theater of World War II.
Here, the U.S. Marine Corps and the Ryukyu Islands Defense Force
fought against the Imperial Japanese Army until the latter surrendered
unconditionally on August 14, 1945.
The atomic bombings of Hiroshima and Nagasaki, which took place on
August 6 and August 9, 1945, respectively, marked the first use of
nuclear weapons in warfare.
These bombings resulted in the immediate deaths of tens of thousands
of people and contributed to the rapid conclusion of the war.
Overall, World War II is remembered as one of the deadliest conflicts in
human history, claiming the lives of millions of men, women, and
children around the world
Figure A10. Interleaved composition generated by InternLM-XComposer.
22

*五、特色美食**
敦煌的特色美食也非常丰富，其中最有名的当属驴肉黄面了。驴肉黄面是一道以驴肉为主要食材的面食，味道鲜香可口，深受当地人和游客的喜爱。
此外，还有羊肉泡馍、胡羊焖饼、烤全羊等特色美食，都是不容错过的美味佳肴。
*五、特色美食**
敦煌的特色美食也非常丰富，其中最有名的当属驴肉黄面了。驴肉黄面是一道以驴肉为主要食材的面食，味道鲜香可口，深受当地人和游客
的喜爱。此外，还有羊肉泡馍、胡羊焖饼、烤全羊等特色美食，都是不容错过的美味佳肴。
C919宣传广告
C919大型客机是中国自行研制、具有自主知识产权的大型喷气式
民用飞机，座级158-168人，航程4075-5555公里。2017年5月14
日，国产大飞机C919在上海浦东国际机场首飞成功！这是中国航
空工业发展史上的一个重要里程碑,标志着我国成为继美国、俄
罗斯之后世界上第三个能够设计制造大型客机的国家。
1. C919的研发历程
1999年12月22日，国务院正式批准了中国商用飞机有限责任公司
（COMAC）筹建；2002年6月29日，中俄两国政府在北京签署了关
于联合研制和生产新型干线宽体客机的合作意向书; 2003年9月
25日，在人民大会堂举行了隆重的签字仪式;
2010年4月26日，第一架C919原型机在中国上海总装下线并进行
了首次地面滑行试车(即“一地两检”) ;同年11月30日，第二架
C919完成全机静力试验并获得型号合格证 (TC); 2018年02月28
日，第三架C919顺利通过适航取证审定试飞并在北京首都机场着
陆后转场至西安阎良进行交付前的系统调试与性能优化工作.
来也非常舒服哦!另外还有宽敞明亮且视野开阔的全景式舷窗可
以随时欣赏到窗外美丽景色呢~总之一句话概括就是两个字——
高大上啊哈哈^\_^!!
节能环保：作为一款绿色出行交通工具当然不能落后于时代潮流
啦对吧?所以设计师们在设计之初就充分考虑到了这一点并将其
融入了整个机身结构当中从而大大降低了燃油消耗量同时还能有
效减少尾气排放污染环境保护我们赖以生存的大好河山哟
o(\*￣▽￣\*)o!!以上便是小编为大家整理出来的全部内容希望
对您有所帮助如果您还有其他疑问或者想了解更多相关资讯请继
续关注本号后续推送文章敬请期待吧ヾ(o◕∀◕)ﾉ(^з^)-☆
北京时间2021年9月13日，星链（Starlink）在美国内华达州拉
斯维加斯举行的第52届国际消费电子展（CES 2021）上展示了其
卫星互联网服务。
在展会现场，SpaceX公司首席执行官埃隆·马斯克（Elon Musk）
向与会者介绍了星链的最新进展和计划。他表示，星链将为全球
提供高速、低延迟的网络接入服务，并将在未来几年内覆盖全球
大部分地区。
据介绍，星链是一个由近1.2万颗通信卫星组成的系统，这些卫
星分布在多个轨道上，以实现全球覆盖。目前，星链已经发射了
约1900颗卫星，预计到2025年将达到4.2万颗。
安全性高：由于采用了先进的设计理念和技术手段，使得该机型
具有良好的抗坠毁性以及超强的防冰雨雪能力等优点:此外它还
配备了先进的电子飞行仪表系统和自动驾驶仪以提高飞行员操作
效率降低人为因素对飞行安全造成影响等等一系列措施都为保证
乘客生命财产安全提供了有力保障!
舒适性好：为了满足不同层次旅客需求而专门开发出符合人体工
程学原理设计的经济舱座椅不仅美观大方而且坐起
对于用户来说，星链提供了高速、低延迟的网络接入服务，能够
满足各种应用场景的需求。同时，星链还支持多终端设备接入，
包括智能手机、平板电脑、笔记本电脑等。此外，星链还提供了
一系列的增值服务，如视频点播、游戏加速等。
据了解，星链的服务价格相对较低，每月只需支付99美元即可享
受高速、低延迟的网络接入服务。这对于那些生活在偏远地区或
无法获得传统电信运营商服务的用户来说，无疑是一个福音。
2. C919的主要特点
星链新闻稿
不过，也有一些人对星链的安全性提出了质疑。他们认为，星链
可能会成为黑客攻击的目标，从而威胁用户的隐私和安全。对此，
马斯克表示，星链采用了多种安全措施，包括加密算法、多重身
份验证等，以确保用户的数据安全。
总的来说，星链是一项非常有前景的技术，它有望为全球用户提
供高速、低延迟的网络接入服务。随着技术的不断发展和完善，
相信星链将会为人类社会带来更多的便利和改变。
以“C919宣传广告”写一篇
宣传广告。
以“星链新闻稿”写一篇新闻稿。
Figure A11. Interleaved composition generated by InternLM-XComposer.
23

London is one of the most popular travel destinations in the
world, and for good reason. From its iconic landmarks to
its rich history and vibrant culture, there is something for
everyone in this bustling city. In this article, we will
provide you with a comprehensive guide to help you make
the most of your trip to London.
First, let's talk about the must-see attractions. London is
home to some of the most famous landmarks in the world,
including Buckingham Palace, the Tower of London, and
Big Ben and the Houses of Parliament. If you're interested
in history, be sure to visit the British Museum and the
Tower of London, which is home to the Crown Jewels. For
a more modern experience, check out the Shard, a
skyscraper that offers stunning views of the city.
Next, let's talk about cultural experiences. London is
known for its diverse and vibrant culture, and there are
many ways to immerse yourself in it. If you're interested in
theater, be sure to catch a show at the West End, which is
home to some of the best theater in the world. If you're
more interested in art, be sure to visit the Tate Modern and
the National Gallery, which are home to some of the most
famous works of art in the world.
Tips for Visiting Shanghai
Now, let's talk about accommodation. London has a wide
range of accommodations to choose from, from luxury
hotels to budget-friendly hostels. If you're looking for a
luxury experience, be sure to check out the Shangri-La at
the Shard, which offers stunning views of the city from its
rooftop terrace. If you're on a budget, be sure to check out
the YHA London St Pancras, which offers affordable
accommodations in a central location.
Finally, let's talk about transportation. London has an
extensive public transportation system, including the Tube,
buses, and trams. If you're planning on using public
transportation, be sure to purchase an Oyster card, which
allows you to pay for your fares as you go. If you're
planning on driving, be sure to check out the congestion
charge, which is a fee that drivers must pay to enter central
London during certain hours.
In conclusion, London is a city that has something for
everyone. From its iconic landmarks to its rich history and
vibrant culture, there is no shortage of things to see and do
in this bustling city. With our comprehensive guide, you'll
be able to make the most of your trip to London and create
memories that will last a lifetime.
Write an article about London travel guidance. 
First introduce the Must-See Attractions, then 
give some advices about the cultural experiences, 
then give some ideas about the Accommodation 
and Transportation, at last give a conclusion
Figure A12. Interleaved composition generated by InternLM-XComposer.
24

Tips for Visiting Shanghai
撰写一篇关于318自驾的文章。 以下是大纲：
开头介绍旅游原因。
接下来介绍旅游日程：
Day 1：成都 - 雅安 - 泸定 - 磨西古镇
Day 2：海螺沟 - 康定 - 新都桥
Day 3：新都桥 - 雅江 - 理塘 - 稻城亚丁
最后总结旅游感受。
2019年8月，我们一家三口从成都出发，自驾前往稻城亚丁。
一、旅游原因
这次去稻城亚丁是临时起意， 没有做任何攻略，只是在网上看了一
些别人的游记，大概了解了一下景点分布和大致的游玩路线 。因为
之前去过九寨沟，所以对川西的美景非常向往， 再加上孩子一直嚷
嚷着要去看海螺沟的大冰瀑布，所以就有了这次说走就走的旅行。
二、旅游日程
Day 1：成都 - 雅安 - 泸定 - 磨西古镇
早上八点从成都出发， 第一站到达雅安，在雅安吃了午饭，然后驱
车前往泸定桥。泸定桥位于四川省甘孜藏族自治州泸定县境内， 横
跨大渡河上，距今已有1700多年的历史。泸定桥始建于公元618年，
原名铁索桥，又称飞夺泸定桥。1935年5月28日，中国工农红军红四
方面军强渡大渡河，取得了“飞夺泸定桥”这一战役的重大胜利。
泸定桥全长103米，宽2.7米，由13根铁链组成，每根铁链间距0.3米，
共有铁锁260余个，每个铁锁重达200多公斤。当年红军战士们就是
依靠这13根铁链与敌人展开殊死搏斗， 最终取得了胜利。现在泸定
桥已经修葺一新，供游客参观游览。
离开泸定桥后，我们继续赶路，大约下午五点左右到达磨西古镇 。
磨西古镇位于四川省甘孜藏族自治州泸定县内 ，距离康定市区约60
公里，海拔2400米。磨西古镇建于明末清初，至今已有400多年的历
史。这里曾经是古丝绸之路上的重要驿站， 也是茶马古道的必经之
地。 如今，磨西古镇保存了大量的明清时期的建筑，包括寺庙、民
居、商铺等，具有很高的历史文化价值 。此外，磨西古镇还有著名
的海螺沟景区，海螺沟位于四川省甘孜藏族自治州南部， 地处青藏
高原东缘，平均海拔4000米以上，被誉为“世界级冰川奇观”。我
们在磨西古镇住了一晚 ，第二天的行程是从磨西古镇出发 ，前往海
螺沟景区。
Day 2：海螺沟 - 康定 - 新都桥
四川省甘孜藏族自治州南部的贡嘎山北坡， 距离磨西古镇约80公里。
海螺沟是中国国家AAAAA级风景名胜区，也是世界自然遗产——四川
大熊猫栖息地的组成部分之一。 海螺沟拥有壮丽的山峰、 清澈的溪
流、茂密的原始森林和丰富的野生动植物资源， 其中最著名的是其
壮观的冰川景观。海螺沟一共有三条沟， 分别为一号沟、二号沟和
三号沟。一号沟被称为“长虹卧雪”，是一条长约6公里的峡谷，两
侧山峰高耸入云；二号沟被称为 “犀牛望月”，是一片开阔的草甸，
中间有一条小溪流过；三号沟被称为“ 一线天”，是一条狭窄的山
谷，两旁峭壁陡峭，只有一条狭缝可供人通过。 整个海螺沟景区以
冰川为主体，辅以雪山、温泉、溶洞、彩池等多种自然景观 ，是一
个集观光、休闲、探险于一体的旅游胜地。
离开海螺沟景区后，我们继续赶路，大约下午六点左右到达新都桥。
新都桥位于四川省甘孜藏族自治州西北部，距离海螺沟景区约120公
里。新都桥素有“摄影家的天堂”之称，因其独特的地形地貌和美
丽的自然风光而闻名于世。 新都桥是一座美丽的小镇， 街道两旁绿
树成荫，鲜花盛开，房屋错落有致，充满了浓郁的藏族风情 。在这
里，你可以漫步在石板路上， 感受小镇的宁静与祥和；也可以骑上
一匹骏马，驰骋在草原上，感受大自然的鬼斧神工；还可以坐在客
栈里，品一杯香浓的酥油茶， 静静地欣赏窗外的美景。 总之，新都
桥是一个让人流连忘返的地方。
Day 3：新都桥 - 雅江 - 理塘 - 稻城亚丁
第三天上午，我们从新都桥出发，前往稻城亚丁。稻城亚丁位于四
川省甘孜藏族自治州南部，距离新都桥约300公里。稻城亚丁是国家
AAAAA级风景区，也被誉为“最后的香格里拉”。稻城亚丁主要由三
大景区组成，分别为洛绒牛场、夏诺多吉神山和央迈勇神山。 这三
个景区各具特色，相互辉映，共同构成了稻城亚丁的全貌 。洛绒牛
场被誉为中国最美的牧场之一， 这里有高山草甸、蓝天白云、牦牛
羊群和淳朴的牧民，构成了一幅和谐的画面。 夏诺多吉神山巍峨挺
拔，气势磅礴，山顶终年积雪，白雪皑皑，给人一种神圣的感觉。
央迈勇神山则是稻城亚丁的最高峰， 海拔高度为5958米，站在山顶
上，可以俯瞰整个稻城亚丁的风光。 除此之外，稻城亚丁还拥有众
多的珍稀动植物，如黑颈鹤、金丝猴、杜鹃花等，这些都是大自然
赐予人类的宝贵财富。
离开稻城亚丁后，我们继续赶路，大约下午七点左右到达理塘。 理
塘位于四川省甘孜藏族自治州西部，距离稻城亚丁约100公里。理塘
有着悠久的历史和深厚的文化底蕴， 当地居民大多信奉藏传佛教 ，
因此理塘又被称为“天空之城”。理塘最著名的景点当属格聂神山，
格聂神山主峰高达6204米，周围环绕着十座山峰， 形态各异，蔚为
壮观。除了格聂神山外，理塘还有许多其他值得一去的景点， 如毛
垭大草原、兔儿山、卡子拉山等。这些景点各有特色，相得益彰，
共同构成了理塘的多姿多彩。
离开理塘后，我们继续赶路，大约傍晚时分到达稻城县。 稻城县位
于四川省甘孜藏族自治州北部，距离理塘约150公里。稻城县历史悠
久，文化底蕴深厚，自古以来就是重要的交通枢纽和贸易中心。 稻
城县的名胜古迹众多， 主要有丹巴碉楼、甲居藏寨、色达喇荣五明
佛学院等。此外，稻城县的自然风光也十分优美， 主要景点有然乌
湖、波密桃花沟、鲁朗林海等。在这些景点的衬托下，稻城县显得
更加生机勃勃，令人流连忘返。
三、总结
总的来说，这次稻城亚丁之行是一次难忘的经历。 虽然一路上遇到
了很多困难和挑战，但我们一家人齐心协力，克服了困难。第二天一大早，我们从磨西古镇出发，前往海螺沟景区。海螺沟位于
Figure A13. Interleaved composition generated by InternLM-XComposer.
25

*五、特色美食**
敦煌的特色美食也非常丰富，其中最有名的当属驴肉黄面了。驴肉黄面是一道以驴肉为主要食材的面食，味道鲜香可口，深受当地人
和游客的喜爱。此外，还有羊肉泡馍、胡羊焖饼、烤全羊等特色美食，都是不容错过的美味佳肴。
*五、特色美食**
敦煌的特色美食也非常丰富，其中最有名的当属驴肉黄面了。驴肉黄面是一道以驴肉为主要食材的面食，味道鲜香可口，深受当地人
和游客的喜爱。此外，还有羊肉泡馍、胡羊焖饼、烤全羊等特色美食，都是不容错过的美味佳肴。
**二、鸣沙山月牙泉**
鸣沙山月牙泉是一处自然奇观，位于敦煌市西北约40公里处的沙漠中。这里地势平坦，沙丘连绵起伏，形成了一片广袤无垠的沙漠景
观。而月牙泉则静静地镶嵌在这片沙漠之中，泉水清澈见底，形状如新月，故称“月牙泉”。每到夜晚，月亮升起时，月牙泉周围会发
出阵阵清脆的响声，犹如天籁之音，令人心旷神怡。
*五、特色美食**
敦煌的特色美食也非常丰富，其中最有名的当属驴肉黄面了。驴肉黄面是一道以驴肉为主要食材的面食，味道鲜香可口，深受当地人和游客的喜
爱。此外，还有羊肉泡馍、胡羊焖饼、烤全羊等特色美食，都是不容错过的美味佳肴。
Describe this image?
The image depicts a young man and a 
young woman dressed in school uniforms 
walking down a staircase in a city setting. 
They appear to be enjoying their time 
together, with the man leading the way.
Which movie does this image come 
from?
This image comes from the anime movie 
"Your Name."
Describe the story of this movie.
"Y ou r  N a m e "  i s  a  2 0 1 6  J a p a n e s e 
animated romantic fantasy film directed 
by Makoto Shinkai. The movie follows 
the story of a high school boy named Taki 
and a high school girl named Mitsuha, 
who find themselves mysteriously 
connected to each other in their dreams.
**二、鸣沙山月牙泉**
鸣沙山月牙泉是一处自然奇观，位于敦煌市西北约40公里处的沙漠中。这里地势平坦，沙丘连绵起伏，形成了一片广袤无垠的沙漠景
观。而月牙泉则静静地镶嵌在这片沙漠之中，泉水清澈见底，形状如新月，故称“月牙泉”。每到夜晚，月亮升起时，月牙泉周围会发
出阵阵清脆的响声，犹如天籁之音，令人心旷神怡。
T h e  d o u b l e  s l i t  e x p e r i m e n t  w a s 
discovered by Thomas Young in 1801.
Describe this image.
The funny thing in this image is that a car 
has been covered in snow, giving it the 
appearance of having a face. Specifically, 
the car has a nose, eyes, and a mouth, 
making it look like a snowman. This is a 
c r e a t i v e  a n d  h u m o r o u s  w a y  o f 
transforming a car into a snowman, 
adding a touch of whimsy to the scene.
What is the snowman's mood?
The snowman's mood appears to be 
happy or playful, as it has a smile on its 
face. 
Describe this image in detail.
The image depicts a cartoonish depiction 
of a man's finger with a gun drawn on it. 
The gun is pointed directly at the man's 
face, creating a tense and threatening 
atmosphere. The man's face is also drawn 
on the finger, with a sad expression on his 
face.
Will the finger get hurt?
 No, the finger will not get hurt.
The image depicts a diagram of a wave 
passing through a double slit experiment. 
There are two slits, A and B, and a single 
particle, represented by a black dot, is 
passing through one of them. The wave 
pattern created by the particle is shown on 
the left side of the diagram, while the 
double slit is located on the right side.
Who discovered it?
What is the funny thing in this image?
Figure A14. Chat with InternLM-XComposer.
26

*五、特色美食**
敦煌的特色美食也非常丰富，其中最有名的当属驴肉黄面了。驴肉黄面是一道以驴肉为主要食材的面食，味道鲜香可口，深受当地人
和游客的喜爱。此外，还有羊肉泡馍、胡羊焖饼、烤全羊等特色美食，都是不容错过的美味佳肴。
**二、鸣沙山月牙泉**
鸣沙山月牙泉是一处自然奇观，位于敦煌市西北约40公里处的沙漠中。这里地势平坦，沙丘连绵起伏，形成了一片广袤无垠的沙漠景
观。而月牙泉则静静地镶嵌在这片沙漠之中，泉水清澈见底，形状如新月，故称“月牙泉”。每到夜晚，月亮升起时，月牙泉周围会发
出阵阵清脆的响声，犹如天籁之音，令人心旷神怡。
*五、特色美食**
敦煌的特色美食也非常丰富，其中最有名的当属驴肉黄面了。驴肉黄面是一道以驴肉为主要食材的面食，味道鲜香可口，深受当地人
和游客的喜爱。此外，还有羊肉泡馍、胡羊焖饼、烤全羊等特色美食，都是不容错过的美味佳肴。
能简单介绍一下这张图上的内容吗？
这幅油画描绘了一辆红色老爷车停在
一座城市街道上，车旁有一棵高大的
枫树。整幅画面呈现出一种宁静的氛
围，似乎在讲述一段温馨的回忆。
从美学的角度分析下这副油画，聊一
聊其颜色搭配、构图、光影上的特点。
这幅油画在颜色搭配上非常和谐，红
色老爷车和枫树的颜色相得益彰，整
个画面呈现出一种温馨、怀旧的氛围。
构图上，老爷车占据了画面的主要部
分，而枫树则作为背景，衬托出老爷
车的风采。在光影方面，这幅油画运
用了柔和的光线，使得整幅画面呈现
出一种宁静、温馨的氛围。老爷车和
枫树在阳光的照射下，显得更加迷人。
这种老爷车在什么时候比较流行？
这种老爷车在20世纪30年代至40年代
非常流行，当时被称为“老爷车”或
“老式车”。这种车型的特点是车身
修长、线条流畅，通常采用V8发动机，
动力强劲，适合长途驾驶。它们在当
时的美国、欧洲和澳大利亚等地非常
受欢迎，成为了那个时代的一种标志
性
**二、鸣沙山月牙泉**
鸣沙山月牙泉是一处自然奇观，位于敦煌市西北约40公里处的沙漠中。这里地势平坦，沙丘连绵起伏，形成了一片广袤无垠的沙漠景观。
而月牙泉则静静地镶嵌在这片沙漠之中，泉水清澈见底，形状如新月，故称“月牙泉”。每到夜晚，月亮升起时，月牙泉周围会发出阵阵清脆
的响声，犹如天籁之音，令人心旷神怡。
请你描述一下这张图片
图片描绘了一个蓝色背景，上面有一
只卡通时钟，钟面上显示着数字。时
钟周围有一些星星和云朵，给整个画
面增添了梦幻的氛围。
请你描述一下这张图片
请你再看这张图片，它描绘了什么呢?
这张图片描绘了一个卡通女孩，她的
头发是蓝色的，眼睛周围有星星和云
朵，看起来非常梦幻。她的面部表情
似乎有些悲伤，可能正在哭泣。
两张图片之间有相似之处吗? 比如风
格、背景上
两张图片在风格和背景上都有相似之
处，都采用了卡通、梦幻的风格，背
景都有星星和云朵的元素。
图中是什么？
麻将桌和麻将
图中的麻将牌们构成了什么番型？
图中的麻将牌们构成了“九莲宝灯”的
番型
接下来，我抓到一张幺鸡，请问我能
胡牌吗？
是的，你抓到一张幺鸡，可以胡牌。
Figure A15. Chat with InternLM-XComposer.
27