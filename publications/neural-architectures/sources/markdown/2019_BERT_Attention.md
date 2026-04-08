|     |     |     |     | What     | Does | BERT      | Look | At?       |     |     |     |     |     |
| --- | --- | --- | --- | -------- | ---- | --------- | ---- | --------- | --- | --- | --- | --- | --- |
|     |     |     | An  | Analysis |      | of BERT’s |      | Attention |     |     |     |     |     |
KevinClark† UrvashiKhandelwal† OmerLevy‡ ChristopherD.Manning†
†ComputerScienceDepartment,StanfordUniversity
‡FacebookAIResearch
{kevclark,urvashik,manning}@cs.stanford.edu
omerlevy@fb.com
|       |             | Abstract |          |         |         |     | study1                                  | the attention | maps | of      | a pre-trained |     | model. |
| ----- | ----------- | -------- | -------- | ------- | ------- | --- | --------------------------------------- | ------------- | ---- | ------- | ------------- | --- | ------ |
|       |             |          |          |         |         |     | Attention                               | (Bahdanau     |      | et al., | 2015)         | has | been a |
| Large | pre-trained | neural   | networks |         | such    | as  |                                         |               |      |         |               |     |        |
|       |             |          |          |         |         |     | highlysuccessfulneuralnetworkcomponent. |               |      |         |               |     | Itis   |
| BERT  | have had    | great    | recent   | success | in NLP, |     |                                         |               |      |         |               |     |        |
naturallyinterpretablebecauseanattentionweight
motivatingagrowingbodyofresearchinvesti-
|     |     |     |     |     |     |     | has a clear | meaning: |     | how much | a particular |     | word |
| --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | --- | -------- | ------------ | --- | ---- |
9102 nuJ 11  ]LC.sc[  1v14340.6091:viXra
| gating | what aspects | of  | language | they | are able |     |         |          |      |           |     |      |        |
| ------ | ------------ | --- | -------- | ---- | -------- | --- | ------- | -------- | ---- | --------- | --- | ---- | ------ |
|        |              |     |          |      |          |     | will be | weighted | when | computing | the | next | repre- |
tolearnfromunlabeleddata.Mostrecentanal-
ysis has focused on model outputs (e.g., lan- sentation for the current word. Our analysis fo-
|       |       |            |             |        |      |     | cuses on | the | 144 attention | heads | in  | BERT2 | (De- |
| ----- | ----- | ---------- | ----------- | ------ | ---- | --- | -------- | --- | ------------- | ----- | --- | ----- | ---- |
| guage | model | surprisal) | or internal | vector | rep- |     |          |     |               |       |     |       |      |
resentations (e.g., probing classifiers). Com- vlin et al., 2019), a large pre-trained Transformer
| plementarytotheseworks, |     |     |     | weproposemeth- |     |     |          |     |            |         |      |     |        |
| ----------------------- | --- | --- | --- | -------------- | --- | --- | -------- | --- | ---------- | ------- | ---- | --- | ------ |
|                         |     |     |     |                |     |     | (Vaswani | et  | al., 2017) | network | that | has | demon- |
odsforanalyzingtheattentionmechanismsof stratedexcellentperformanceonmanytasks.
| pre-trained  | models    | and       | apply   | them     | to BERT. |     |            |         |           |         |            |     |        |
| ------------ | --------- | --------- | ------- | -------- | -------- | --- | ---------- | ------- | --------- | ------- | ---------- | --- | ------ |
|              |           |           |         |          |          |     | We first   | explore | generally |         | how BERT’s |     | atten- |
| BERT’s       | attention | heads     | exhibit | patterns | such     |     |            |         |           |         |            |     |        |
|              |           |           |         |          |          |     | tion heads | behave. |           | We find | that there | are | com-   |
| as attending | to        | delimiter | tokens, | specific | po-      |     |            |         |           |         |            |     |        |
sitional offsets, or broadly attending over the monpatternsintheirbehavior,suchasattendingto
whole sentence, with heads in the same layer fixed positional offsets or attending broadly over
oftenexhibitingsimilarbehaviors. Wefurther the whole sentence. A surprisingly large amount
show that certain attention heads correspond ofBERT’sattentionfocusesonthedeliminatorto-
welltolinguisticnotionsofsyntaxandcoref-
|         |              |     |         |       |          |     | ken [SEP],      | which | we                           | argue | is used | by the | model |
| ------- | ------------ | --- | ------- | ----- | -------- | --- | --------------- | ----- | ---------------------------- | ----- | ------- | ------ | ----- |
| erence. | For example, |     | we find | heads | that at- |     |                 |       |                              |       |         |        |       |
|         |              |     |         |       |          |     | asasortofno-op. |       | Generallywefindthatattention |       |         |        |       |
tendtothedirectobjectsofverbs,determiners
headsinthesamelayertendtobehavesimilarly.
ofnouns,objectsofprepositions,andcorefer-
Wenextprobeeachattentionheadforlinguistic
| ent mentions |     | with remarkably |     | high | accuracy. |     |     |     |     |     |     |     |     |
| ------------ | --- | --------------- | --- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
Lastly,weproposeanattention-basedprobing phenomena. In particular, we treat each head as a
classifieranduseittofurtherdemonstratethat simpleno-training-requiredclassifierthat,givena
substantialsyntacticinformationiscapturedin word as input, outputs the most-attended-to other
BERT’sattention.
|     |     |     |     |     |     |     | word.       | We then | evaluate  | the | ability    | of the | heads |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------- | --------- | --- | ---------- | ------ | ----- |
|     |     |     |     |     |     |     | to classify | various | syntactic |     | relations. | While  | no    |
1 Introduction
|                   |     |          |        |         |     |      | single    | head performs |       | well at    | many | relations, | we  |
| ----------------- | --- | -------- | ------ | ------- | --- | ---- | --------- | ------------- | ----- | ---------- | ---- | ---------- | --- |
|                   |     |          |        |         |     |      | find that | particular    | heads | correspond |      | remarkably |     |
| Large pre-trained |     | language | models | achieve |     | very |           |               |       |            |      |            |     |
highaccuracywhenfine-tunedonsupervisedtasks well to particular relations. For example, we find
|                |           |        |           |            |         |      | heads that    | find | direct  | objects          | of verbs, | determin- |         |
| -------------- | --------- | ------ | --------- | ---------- | ------- | ---- | ------------- | ---- | ------- | ---------------- | --------- | --------- | ------- |
| (Dai and       | Le, 2015; | Peters | et        | al., 2018; | Radford |      |               |      |         |                  |           |           |         |
|                |           |        |           |            |         |      | ers of nouns, |      | objects | of prepositions, |           | and       | objects |
| et al., 2018), | but       | it is  | not fully | understood |         | why. |               |      |         |                  |           |           |         |
Thestrongresultssuggestpre-trainingteachesthe of possessive pronouns with >75% accuracy. We
models about the structure of language, but what perform a similar analysis for coreference resolu-
tion,alsofindingaBERTheadthatperformsquite
specificlinguisticfeaturesdotheylearn?
|        |      |                  |     |      |          |     | well. These | results | are | intriguing | because |     | the be- |
| ------ | ---- | ---------------- | --- | ---- | -------- | --- | ----------- | ------- | --- | ---------- | ------- | --- | ------- |
| Recent | work | has investigated |     | this | question | by  |             |         |     |            |         |     |         |
examining the outputs of language models on havioroftheattentionheadsemergespurelyfrom
self-supervisedtrainingonunlabeleddata,without
| carefully | chosen | input | sentences | (Linzen | et  | al., |     |     |     |     |     |     |     |
| --------- | ------ | ----- | --------- | ------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
explicitsupervisionforsyntaxorcoreference.
2016)orexaminingtheinternalvectorrepresenta-
tionsofthemodelthroughmethodssuchasprob-
|                 |      |     |            |          |     |         | 1Code | will | be released | at https://github.com/ |     |     |     |
| --------------- | ---- | --- | ---------- | -------- | --- | ------- | ----- | ---- | ----------- | ---------------------- | --- | --- | --- |
| ing classifiers | (Adi | et  | al., 2017; | Belinkov |     | et al., |       |      |             |                        |     |     |     |
clarkkev/attention-analysis.
2017). Complementary to these approaches, we 2WeusetheEnglishbase-sizedmodel.

|     | Head 1-1  |     |     |     | Head 3-1  |     |     | Head 8-7  |     |     | Head 11-6  |     |     |
| --- | --------- | --- | --- | --- | --------- | --- | --- | --------- | --- | --- | ---------- | --- | --- |
Attends  broadly  Attends to  next token  Attends  to [SEP]  Attends t o periods
|     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     |     |     |     |     |     |
Figure1: ExamplesofheadsexhibitingthepatternsdiscussedinSection3. Thedarknessofalineindicatesthe
strengthoftheattentionweight(someattentionweightsaresolowtheyareinvisible).
Ourfindingsshowthatparticularheadsspecial- Attentionweightscanbeviewedasgoverninghow
ize to specific aspects of syntax. To get a more “important” every other token is when producing
overall measure of the attention heads’ syntac- thenextrepresentationforthecurrenttoken.
tic ability, we propose an attention-based probing BERTispre-trainedon3.3billiontokensofEn-
| classifier | that | takes attention |     | maps | as input. | The |       |      |            |     |        |                |     |
| ---------- | ---- | --------------- | --- | ---- | --------- | --- | ----- | ---- | ---------- | --- | ------ | -------------- | --- |
|            |      |                 |     |      |           |     | glish | text | to perform | two | tasks. | In the “masked |     |
classifier achieves 77 UAS at dependency pars- language modeling” task, the model predicts the
ing,showingBERT’sattentioncapturesasubstan- identities of words that have been masked-out of
| tial amount | about | syntax. | Several |     | recent | works |     |       |              |       |          |             |     |
| ----------- | ----- | ------- | ------- | --- | ------ | ----- | --- | ----- | ------------ | ----- | -------- | ----------- | --- |
|             |       |         |         |     |        |       | the | input | text. In the | “next | sentence | prediction” |     |
haveproposedincorporatingsyntacticinformation
|     |     |     |     |     |     |     | task, | the | model predicts | whether |     | the second | half |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | -------------- | ------- | --- | ---------- | ---- |
to improve attention (Eriguchi et al., 2016; Chen oftheinputfollowsthefirsthalfoftheinputinthe
et al., 2018; Strubell et al., 2018). Our work sug- corpus,orisarandomparagraph. Furthertraining
| gests that | to  | an extent | this kind | of  | syntax-aware |     |     |       |               |      |         |     |         |
| ---------- | --- | --------- | --------- | --- | ------------ | --- | --- | ----- | ------------- | ---- | ------- | --- | ------- |
|            |     |           |           |     |              |     | the | model | on supervised | data | results | in  | impres- |
attention already exists in BERT, which may be sive performance across a variety of tasks rang-
oneofthereasonforitssuccess. ingfromsentimentanalysistoquestionanswering.
AnimportantdetailofBERTisthepreprocessing
| 2 Background: |     | TransformersandBERT |     |     |     |     |      |     |                 |     |         |             |     |
| ------------- | --- | ------------------- | --- | --- | --- | --- | ---- | --- | --------------- | --- | ------- | ----------- | --- |
|               |     |                     |     |     |     |     | used | for | the input text. | A   | special | token [CLS] | is  |
Although our analysis methods are applicable added to the beginning of the text and another to-
to any model that uses an attention mechanism, ken[SEP]isaddedtotheend. Iftheinputconsists
in this paper we analyze BERT (Devlin et al., ofmultipleseparatetexts(e.g.,areadingcompre-
|        |         |             |          |     |         |       | hension |     | example consists |     | of a separate | question |     |
| ------ | ------- | ----------- | -------- | --- | ------- | ----- | ------- | --- | ---------------- | --- | ------------- | -------- | --- |
| 2019), | a large | Transformer | (Vaswani |     | et al., | 2017) |         |     |                  |     |               |          |     |
network. Transformers consist of multiple lay- and context), [SEP] tokens are also used to sep-
ers where each layer contains multiple attention arate them. As we show in the next section, these
heads. Anattentionheadtakesasinputasequence special tokens play an important role in BERT’s
of vectors corresponding to the attention. We use the “base” sized BERT model,
|     | h   | = [h 1 ,...,h | n ] |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
n tokens of the input sentence. Each vector h whichhas12layerscontaining12attentionheads
i
is transformed into query, key, and value vectors each. Weuse<layer>-<head number>todenote
aparticularattentionhead.
| q i ,k i ,v | i through | separate  | linear | transformations. |     |         |     |     |     |     |     |     |     |
| ----------- | --------- | --------- | ------ | ---------------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
| The head    | computes  | attention |        | weights          | α   | between |     |     |     |     |     |     |     |
allpairsofwordsassoftmax-normalizeddotprod-
|              |     |           |         |          |     |      | 3   | Surface-LevelPatternsinAttention |     |     |     |     |     |
| ------------ | --- | --------- | ------- | -------- | --- | ---- | --- | -------------------------------- | --- | --- | --- | --- | --- |
| ucts between |     | the query | and key | vectors. | The | out- |     |                                  |     |     |     |     |     |
putooftheattentionheadisaweightedsumofthe
|     |     |     |     |     |     |     | Before | looking | at specific |     | linguistic | phenomena, |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------- | ----------- | --- | ---------- | ---------- | --- |
valuevectors.
|     |         |     |     |     |     |     | we    | first perform | an     | analysis  | of surface-level |         | pat- |
| --- | ------- | --- | --- | --- | --- | --- | ----- | ------------- | ------ | --------- | ---------------- | ------- | ---- |
|     |         |     |     |     | n   |     | terns | in how        | BERT’s | attention | heads            | behave. | Ex-  |
|     | exp(qTk | )   |     |     |     |     |       |               |        |           |                  |         |      |
|     |         | i j |     |     |     |     |       |               |        |           |                  |         |      |
α ij = o i = α ij v j amples of heads exhibiting these patterns are
|     | n   | exp (q Tk | )   |     |     |     |                 |     |     |     |     |     |     |
| --- | --- | --------- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- | --- |
|     | l=1 | i         | l   |     |     |     |                 |     |     |     |     |     |     |
|     |     |           |     |     | j=1 |     | showninFigure1. |     |     |     |     |     |     |
(cid:88)
(cid:80)

3.0
|     |     | [CLS] |     |     |     |     |     |     |     |     | Allunmaskedtokens |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- |
0.8
|     |     | [SEP] |     |     |     |     | 2.5 |     |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
[SEP]
| noitnettA .gvA |     | . or , |     |     |     |     |     |     |     |     |       |     |     |
| -------------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
| 0.6            |     |        |     |     |     |     |     |     |     |     | . or, |     |     |
2.0 (cid:12) (cid:12)
Lα∂
∂
| 0.4 |     |     |     |     |     |     | (cid:12) (cid:12) |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | egarevA 1.5       |     |     |     |     |     |     |
0.2
1.0
0.0
0.5
|     | 2   | 4   | 6     | 8   | 10  | 12  |     |     |     |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | Layer |     |     |     | 0.0 |     |     |     |     |     |     |
|     |     |     |       |     |     |     |     | 2   | 4   | 6   | 8   | 10  | 12  |
1.0
Layer
0.8
noitnettA .gvA
|     |     |     |     |     |     |     | Figure3: | Gradient-basedfeatureimportanceestimates |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---------------------------------------- | --- | --- | --- | --- | --- |
0.6
|     |     |     |                |     |     |     | for attention | to  | [SEP], | periods/commas, |     | and | other to- |
| --- | --- | --- | -------------- | --- | --- | --- | ------------- | --- | ------ | --------------- | --- | --- | --------- |
| 0.4 |     |     |                |     |     |     | kens.         |     |        |                 |     |     |           |
| 0.2 |     |     | [SEP] -> [SEP] |     |     |     |               |     |        |                 |     |     |           |
)stan( yportnE noitnettA .gvA
other -> [SEP]
| 0.0 |     |     |     |     |     |     |     |     |     | uniform attention |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- |
4
|     | 2   | 4   | 6   | 8   | 10  | 12  |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Layer
| Figure2: | Eachpointcorrespondstotheaverageatten- |     |     |     |     |     | 2   |     |     |     |     |     |     |
| -------- | -------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tionaparticularBERTattentionheadputstowardato-
| ken type. | Above: | heads | often attend | to  | “special” | to- |     |     |     |     |     |     |     |
| --------- | ------ | ----- | ------------ | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
BERT Heads
| kens. Earlyheadsattendto[CLS],middleheadsattend |     |     |     |     |     |     | 0   |     |     |     |     |     |     |
| ----------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
to [SEP], and deep heads attend to periods and com- 2 4 6 8 10 12
| mas. Oftenmorethanhalfofahead’stotalattentionis |         |        |              |     |       |        |     |     |     | Layer |     |     |     |
| ----------------------------------------------- | ------- | ------ | ------------ | --- | ----- | ------ | --- | --- | --- | ----- | --- | --- | --- |
| to these                                        | tokens. | Below: | heads attend | to  | [SEP] | tokens |     |     |     |       |     |     |     |
evenmorewhenthecurrenttokenis[SEP]itself. Figure 4: Entropies of attention distributions. In the
firstlayerthereareparticularlyhigh-entropyheadsthat
producebag-of-vector-likerepresentations.
Setup. WeextracttheattentionmapsfromBERT-
| base over | 1000 | random | Wikipedia | segments. |     | We  |                                |     |     |     |     |     |     |
| --------- | ---- | ------ | --------- | --------- | --- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- |
|           |      |        |           |           |     |     | 3.2 AttendingtoSeparatorTokens |     |     |     |     |     |     |
followthesetupusedforpre-trainingBERTwhere
|               |         |          |             |            |     |        | Interestingly, |           | we found | that | a substantial |            | amount |
| ------------- | ------- | -------- | ----------- | ---------- | --- | ------ | -------------- | --------- | -------- | ---- | ------------- | ---------- | ------ |
| each          | segment | consists | of at       | most       | 128 | tokens |                |           |          |      |               |            |        |
|               |         |          |             |            |     |        | of BERT’s      | attention | focuses  |      | on a          | few tokens | (see   |
| corresponding |         | to two   | consecutive | paragraphs |     | of     |                |           |          |      |               |            |        |
Wikipedia (although we do not mask out in- Figure2). Forexample,overhalfofBERT’satten-
tioninlayers6-10focuseson[SEP].Toputthisin
| put words |     | or as in | BERT’s training). |     | The | in- |     |     |     |     |     |     |     |
| --------- | --- | -------- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
context,sincemostofoursegmentsare128tokens
| put presented |     | to the | model is [CLS]<paragraph- |     |     |     |           |         |           |     |       |                 |     |
| ------------- | --- | ------ | ------------------------- | --- | --- | --- | --------- | ------- | --------- | --- | ----- | --------------- | --- |
|               |     |        |                           |     |     |     | long, the | average | attention |     | for a | token occurring |     |
1>[SEP]<paragraph-2>[SEP].
twiceinasegmentslike[SEP]wouldnormallybe
|     |     |     |     |     |     |     | around | 1/64. | [SEP] and | [CLS] | are | guaranteed | to  |
| --- | --- | --- | --- | --- | --- | --- | ------ | ----- | --------- | ----- | --- | ---------- | --- |
3.1 RelativePosition
|     |     |     |     |     |     |     | be present | and | are never | masked |     | out, while | pe- |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --------- | ------ | --- | ---------- | --- |
First, we compute how often BERT’s attention riods and commas are the most common tokens
heads attend to the current token, the previous to- in the data excluding “the,” which might be why
ken, or the next token. We find that most heads the model treats these tokens differently. A sim-
put little attention on the current token. However, ilar pattern occurs for the uncased BERT model,
thereareheadsthatspecializetoattendingheavily suggesting there is a systematic reason for the at-
on the next or previous token, especially in ear- tentiontospecialtokensratherthanitbeinganar-
lierlayersofthenetwork. Inparticularfouratten- tifactofstochastictraining.
tionheads(inlayers2,4,7,and8)onaverageput One possible explanation is that [SEP] is used
>50%oftheirattentionontheprevioustokenand toaggregatesegment-levelinformationwhichcan
fiveattentionheads(inlayers1,2,2,3,and6)put then be read by other heads. However, further
>50%oftheirattentiononthenexttoken. analysismakesusdoubtfulthisisthecase. Ifthis

explanation were true, we would expect attention wholeinputinthelastlayer.
headsprocessing[SEP]toattendbroadlyoverthe
whole segment to build up these representations. 4 ProbingIndividualAttentionHeads
| However, | they | instead | almost | entirely |     | (more than |          |             |     |            |           |     |          |
| -------- | ---- | ------- | ------ | -------- | --- | ---------- | -------- | ----------- | --- | ---------- | --------- | --- | -------- |
|          |      |         |        |          |     |            | Next, we | investigate |     | individual | attention |     | heads to |
90%;seebottomofFigure2)attendtothemselves
probewhataspectsoflanguagetheyhavelearned.
| and the       | other     | [SEP]  | token. | Furthermore, |      | qualita-   |                |     |           |      |            |       |          |
| ------------- | --------- | ------ | ------ | ------------ | ---- | ---------- | -------------- | --- | --------- | ---- | ---------- | ----- | -------- |
|               |           |        |        |              |      |            | In particular, | we  | evaluate  |      | attention  | heads | on la-   |
| tive analysis | (see      | Figure | 5)     | shows        | that | heads with |                |     |           |      |            |       |          |
|               |           |        |        |              |      |            | beled datasets |     | for tasks | like | dependency |       | parsing. |
| specific      | functions | attend | to     | [SEP]        | when | the func-  |                |     |           |      |            |       |          |
AnoverviewofourresultsisshowninFigure5.
| tion is not    | called | for.      | For      | example, | in         | head 8-10  |            |             |     |           |       |     |            |
| -------------- | ------ | --------- | -------- | -------- | ---------- | ---------- | ---------- | ----------- | --- | --------- | ----- | --- | ---------- |
| direct objects |        | attend    | to their | verbs.   | For        | this head, | 4.1 Method |             |     |           |       |     |            |
| non-nouns      | mostly | attend    | to       | [SEP].   | Therefore, | we         |            |             |     |           |       |     |            |
|                |        |           |          |          |            |            | We wish    | to evaluate |     | attention | heads | at  | word-level |
| speculate      | that   | attention | over     | these    | special    | tokens     |            |             |     |           |       |     |            |
tasks,butBERTusesbyte-pairtokenization(Sen-
mightbeusedasasortof“no-op”whentheatten- nrich et al., 2016), which means some words
tionhead’sfunctionisnotapplicable.
|            |     |             |      |             |     |        | (∼8% in  | our data) | are     | split | up          | into multiple | to-       |
| ---------- | --- | ----------- | ---- | ----------- | --- | ------ | -------- | --------- | ------- | ----- | ----------- | ------------- | --------- |
| To further |     | investigate | this | hypothesis, |     | we ap- |          |           |         |       |             |               |           |
|            |     |             |      |             |     |        | kens. We | therefore | convert |       | token-token |               | attention |
plygradient-basedmeasuresoffeatureimportance
|     |     |     |     |     |     |     | maps to | word-word |     | attention | maps. | For | attention |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------- | --- | --------- | ----- | --- | --------- |
(Sundararajanetal.,2017). Inparticular,wecom- toasplit-upword,wesumuptheattentionweights
putethemagnitudeofthegradientofthelossfrom
|        |        |          |     |          |      |          | overitstokens. |     | Forattentionfromasplit-upword, |     |     |     |     |
| ------ | ------ | -------- | --- | -------- | ---- | -------- | -------------- | --- | ------------------------------ | --- | --- | --- | --- |
| BERT’s | masked | language |     | modeling | task | with re- |                |     |                                |     |     |     |     |
wetakethemeanoftheattentionweightsoverits
spect to each attention weight. Intuitively, this tokens. These transformations preserve the prop-
value measures how much changing the attention erty that the attention from each word sums to
| to a token | will | change | BERT’s      |     | outputs. | Results |           |         |           |          |     |       |           |
| ---------- | ---- | ------ | ----------- | --- | -------- | ------- | --------- | ------- | --------- | -------- | --- | ----- | --------- |
|            |      |        |             |     |          |         | 1. For    | a given | attention | head     | and | word, | we take   |
| are shown  | in   | Figure | 3. Starting |     | in layer | 5 – the |           |         |           |          |     |       |           |
|            |      |        |             |     |          |         | whichever | other   | word      | receives | the | most  | attention |
samelayerwhereattentionto[SEP]becomeshigh weightasthatmodel’sprediction3
–thegradientsforattentionto[SEP]becomevery
small. Thisindicatesthatattendingmoreorlessto 4.2 DependencySyntax
[SEP] does not substantially change BERT’s out- Setup. We extract attention maps from BERT on
puts,supportingthetheorythatattentionto[SEP] the Wall Street Journal portion of the Penn Tree-
isusedasano-opforattentionheads.
bank(Marcusetal.,1993)annotatedwithStanford
|     |     |     |     |     |     |     | Dependencies. |     | We evaluate |     | both | “directions” | of  |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | ----------- | --- | ---- | ------------ | --- |
3.3 FocusedvsBroadAttention prediction for each attention head: the head word
|            |            |           |            |           |              |            | attending                           | to the     | dependent   |          | and the             | dependent       | at-      |
| ---------- | ---------- | --------- | ---------- | --------- | ------------ | ---------- | ----------------------------------- | ---------- | ----------- | -------- | ------------------- | --------------- | -------- |
| Lastly,    | we measure |           | whether    | attention |              | heads fo-  |                                     |            |             |          |                     |                 |          |
|            |            |           |            |           |              |            | tendingtotheheadword.               |            |             |          | Somedependencyrela- |                 |          |
| cus on     | a few      | words     | or attend  | broadly   |              | over many  |                                     |            |             |          |                     |                 |          |
|            |            |           |            |           |              |            | tionsaresimplertopredictthanothers: |            |             |          |                     |                 | forexam- |
| words.     | To do      | this,     | we compute |           | the average  | en-        |                                     |            |             |          |                     |                 |          |
|            |            |           |            |           |              |            | ple a noun’s                        | determiner |             | is       | often               | the immediately |          |
| tropy of   | each       | head’s    | attention  |           | distribution | (see       |                                     |            |             |          |                     |                 |          |
|            |            |           |            |           |              |            | preceding                           | word.      | Therefore   |          | as a                | point of        | compar-  |
| Figure 4). | We         | find that | some       | attention |              | heads, es- |                                     |            |             |          |                     |                 |          |
|            |            |           |            |           |              |            | ison, we                            | show       | predictions |          | from                | a simple        | fixed-   |
| pecially   | in lower   | layers,   |            | have very | broad        | atten-     |                                     |            |             |          |                     |                 |          |
|            |            |           |            |           |              |            | offset baseline.                    |            | For         | example, | a                   | fixed offset    | of -2    |
tion. Thesehigh-entropyattentionheadstypically
meansthewordtwopositionstotheleftofthede-
| spend at | most | 10% of | their | attention | mass | on any |     |     |     |     |     |     |     |
| -------- | ---- | ------ | ----- | --------- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- |
pendentisalwaysconsideredtobethehead.
| singleword. | Theoutputoftheseheadsisroughly |     |     |     |     |     |     |     |     |     |     |     |     |
| ----------- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
abag-of-vectorsrepresentationofthesentence. Results. Table 1 shows that there is no single at-
We also measured entropies for all attention tentionheadthatdoeswellatsyntax“overall”;the
heads from only the [CLS] token. While the av- bestheadgets34.5UAS,whichisnotmuchbetter
thantheright-branchingbaseline,whichgets26.3
| erage entropies |     | from | [CLS] | for | most | layers are |     |     |     |     |     |     |     |
| --------------- | --- | ---- | ----- | --- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- |
UAS.Thisfindingissimilartotheonereportedby
| very close | to  | the ones | shown |     | in Figure | 4, the |     |     |     |     |     |     |     |
| ---------- | --- | -------- | ----- | --- | --------- | ------ | --- | --- | --- | --- | --- | --- | --- |
last layer has a high entropy from [CLS] of 3.89 RaganatoandTiedemann(2018), whoalsoevalu-
nats, indicating very broad attention. This find- ateindividualattentionheadsforsyntax.
However,wedofindthatcertainattentionheads
| ing makes | sense | given | that | the representation |     | for |     |     |     |     |     |     |     |
| --------- | ----- | ----- | ---- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the[CLS]tokenisusedasinputforthe“nextsen- specializetospecificdependencyrelations,some-
tenceprediction”taskduringpre-training,soitat-
|     |     |     |     |     |     |     | 3We ignore | [SEP] | and | [CLS], | although | in  | practice this |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ----- | --- | ------ | -------- | --- | ------------- |
tendsbroadlytoaggregatearepresentationforthe doesnotsignificantlychangetheaccuraciesformostheads.

Head 8-10 Head 8-11
- Direct objects attend to their verbs - Noun modifiers (e.g., determiners) attend
to their noun
- 86.8% accuracy at the dobj relation
- 94.3% accuracy at the det relation
Head 7-6 Head 4-10
- Possessive pronouns and apostrophes - Passive auxiliary verbs attend to the
attend to the head of the corresponding NP verb they modify
- 80.5% accuracy at the poss relation - 82.5% accuracy at the auxpass relation
Head 9-6 Head 5-4
- Prepositions attend to their objects - Coreferent mentions attend to their antecedents
- 76.3% accuracy at the pobj relation - 65.1% accuracy at linking the head of a
coreferent mention to the head of an antecedent
Figure 5: BERT attention heads that correspond to linguistic phenomena. In the example attention maps, the
darkness of a line indicates the strength of the attention weight. All attention to/from red words is colored red;
these colors are there to highlight certain parts of the attention heads’ behaviors. For Head 9-6, we don’t show
attentionto[SEP]forclarity. Despitenotbeingexplicitlytrainedonthesetasks,BERT’sattentionheadsperform
remarkablywell,illustratinghowsyntax-sensitivebehaviorcanemergefromself-supervisedtrainingalone.

analysistoseeiftherelationswell-capturedbyat-
| Relation |     | Head | Accuracy |     | Baseline |     |     |     |     |     |     |     |     |
| -------- | --- | ---- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
tentionaresimilarordifferentforotherlanguages.
| All   |     | 7-6  |     | 34.5 | 26.3(1)  |     |                           |             |         |             |             |     |              |
| ----- | --- | ---- | --- | ---- | -------- | --- | ------------------------- | ----------- | ------- | ----------- | ----------- | --- | ------------ |
| prep  |     | 7-4  |     | 66.7 | 61.8(-1) |     | 4.3 CoreferenceResolution |             |         |             |             |     |              |
| pobj  |     | 9-6  |     | 76.3 | 34.6(-2) |     |                           |             |         |             |             |     |              |
|       |     |      |     |      |          |     | Having                    | shown       | BERT    | attention   | heads       |     | reflect cer- |
| det   |     | 8-11 |     | 94.3 | 51.7(1)  |     |                           |             |         |             |             |     |              |
|       |     |      |     |      |          |     | tain aspects              | of          | syntax, | we          | now explore |     | using at-    |
| nn    |     | 4-10 |     | 70.4 | 70.2(1)  |     |                           |             |         |             |             |     |              |
|       |     |      |     |      |          |     | tention                   | heads       | for the | more        | challenging |     | semantic     |
| nsubj |     | 8-2  |     | 58.5 | 45.5(1)  |     |                           |             |         |             |             |     |              |
|       |     |      |     |      |          |     | task of                   | coreference |         | resolution. | Coreference |     | links        |
amod
|     |     | 4-10 |     | 75.6 | 68.3(1) |     |     |     |     |     |     |     |     |
| --- | --- | ---- | --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
areusuallylongerthansyntacticdependenciesand
| dobj   |     | 8-10 |     | 86.8 | 40.0(-2) |     |                  |     |         |           |     |         |      |
| ------ | --- | ---- | --- | ---- | -------- | --- | ---------------- | --- | ------- | --------- | --- | ------- | ---- |
|        |     |      |     |      |          |     | state-of-the-art |     | systems | generally |     | perform | much |
| advmod |     | 7-6  |     | 48.8 | 40.2(1)  |     |                  |     |         |           |     |         |      |
worseatcoreferencecomparedtoparsing.
aux
|          |     | 4-10            |     | 81.1       | 71.5(1)  |          |                              |             |            |               |                  |       |           |
| -------- | --- | --------------- | --- | ---------- | -------- | -------- | ---------------------------- | ----------- | ---------- | ------------- | ---------------- | ----- | --------- |
|          |     |                 |     |            |          |          | Setup.                       | We evaluate |            | the attention |                  | heads | on coref- |
| poss     |     | 7-6             |     | 80.5       | 47.7(1)  |          |                              |             |            |               |                  |       |           |
|          |     |                 |     |            |          |          | erence resolution            |             | using      | the           | CoNLL-2012       |       | dataset4  |
| auxpass  |     | 4-10            |     | 82.5       | 40.5(1)  |          |                              |             |            |               |                  |       |           |
|          |     |                 |     |            |          |          | (Pradhan                     | et al.,     | 2012).     | In            | particular,      | we    | compute   |
| ccomp    |     | 8-1             |     | 48.8       | 12.4(-2) |          |                              |             |            |               |                  |       |           |
|          |     |                 |     |            |          |          | antecedentselectionaccuracy: |             |            |               | whatpercentofthe |       |           |
| mark     |     | 8-2             |     | 50.7       | 14.5(2)  |          |                              |             |            |               |                  |       |           |
|          |     |                 |     |            |          |          | time does                    | the         | head       | word of       | a coreferent     |       | mention   |
| prt      |     | 6-7             |     | 99.1       | 91.4(-1) |          |                              |             |            |               |                  |       |           |
|          |     |                 |     |            |          |          | most attend                  | to          | the        | head of       | one of           | that  | mention’s |
|          |     |                 |     |            |          |          | antecedents.                 |             | We compare |               | against          | three | baselines |
| Table 1: | The | best performing |     | attentions |          | heads of |                              |             |            |               |                  |       |           |
forselectinganantecedent:
| BERT on | WSJ | dependency |     | parsing | by dependency |     |     |     |     |     |     |     |     |
| ------- | --- | ---------- | --- | ------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
type. Numbersafterbaselineaccuraciesshowthebest
• Pickingthenearestothermention.
| offset found         | (e.g., | (1) | means                 | the word | to the | right is |           |     |             |       |         |     |          |
| -------------------- | ------ | --- | --------------------- | -------- | ------ | -------- | --------- | --- | ----------- | ----- | ------- | --- | -------- |
|                      |        |     |                       |          |        |          | • Picking |     | the nearest | other | mention |     | with the |
| predictedasthehead). |        |     | Weshowthe10mostcommon |          |        |          |           |     |             |       |         |     |          |
relationsaswellas5otheronesattentionheadsdowell sameheadwordasthecurrentmention.
on. Boldhighlightsparticularlyeffectiveheads.
|                 |     |                  |          |           |               |         | • A                  | simple | rule-based                |     | system | inspired | by Lee     |
| --------------- | --- | ---------------- | -------- | --------- | ------------- | ------- | -------------------- | ------ | ------------------------- | --- | ------ | -------- | ---------- |
|                 |     |                  |          |           |               |         | etal.(2011).         |        | Itproceedsthrough4sieves: |     |        |          | (1)        |
|                 |     |                  |          |           |               |         | full                 | string | match,                    | (2) | head   | word     | match, (3) |
| times achieving |     | high             | accuracy | and       | substantially |         |                      |        |                           |     |        |          |            |
|                 |     |                  |          |           |               |         | number/gender/person |        |                           |     | match, | (4)      | all other  |
| outperforming   |     | the fixed-offset |          | baseline. |               | We find |                      |        |                           |     |        |          |            |
that for all relations in Table 1 except pobj, the mentions. Thenearestmentionsatisfyingthe
earliestsieveisreturned.
dependentattendstotheheadwordratherthanthe
| other way   | around, | likely | because   |      | each dependent |     |         |      |                 |     |     |          |        |
| ----------- | ------- | ------ | --------- | ---- | -------------- | --- | ------- | ---- | --------------- | --- | --- | -------- | ------ |
|             |         |        |           |      |                |     | We also | show | the performance |     | of  | a recent | neural |
| has exactly | one     | head   | but heads | have | multiple       | de- |         |      |                 |     |     |          |        |
coreferencesystemfromWisemanetal.(2015).
| pendents. | We         | also note | heads       | can          | disagree | with       |                  |           |            |           |              |          |            |
| --------- | ---------- | --------- | ----------- | ------------ | -------- | ---------- | ---------------- | --------- | ---------- | --------- | ------------ | -------- | ---------- |
|           |            |           |             |              |          |            | Results.         | Results   | are        | shown     | in Table     |          | 2. We find |
| standard  | annotation |           | conventions |              | while    | still per- |                  |           |            |           |              |          |            |
|           |            |           |             |              |          |            | that one         | of BERT’s |            | attention | heads        | achieves | de-        |
| forming   | syntactic  | behavior. |             | For example, |          | head 7-    |                  |           |            |           |              |          |            |
|           |            |           |             |              |          |            | cent coreference |           | resolution |           | performance, |          | improv-    |
6marks’sasthedependentforthepossrelation,
|                     |        |           |        |          |                |         | ing by   | over     | 10 accuracy |                | points | on    | the string- |
| ------------------- | ------ | --------- | ------ | -------- | -------------- | ------- | -------- | -------- | ----------- | -------------- | ------ | ----- | ----------- |
| while gold-standard |        |           | labels | mark     | the complement |         |          |          |             |                |        |       |             |
|                     |        |           |        |          |                |         | matching | baseline |             | and performing |        | close | to the      |
| of an ’s            | as the | dependent | (the   | accuracy | in             | Table 1 |          |          |             |                |        |       |             |
counts ’s as correct). Such disagreements high- rule-based system. It is particularly good with
|                               |                 |           |           |                 |         |           | nominal                  | mentions, |     | perhaps | because  | it  | is capable |
| ----------------------------- | --------------- | --------- | --------- | --------------- | ------- | --------- | ------------------------ | --------- | --- | ------- | -------- | --- | ---------- |
| light how                     | these           | syntactic | behaviors |                 | in BERT | are       |                          |           |     |         |          |     |            |
|                               |                 |           |           |                 |         |           | of fuzzy                 | matching  |     | between | synonyms |     | as seen in |
| learned                       | as a by-product |           | of        | self-supervised |         | train-    |                          |           |     |         |          |     |            |
| ing,notbycopyingahumandesign. |                 |           |           |                 |         |           | thebottomrightofFigure5. |           |     |         |          |     |            |
| Figure                        | 5 shows         | some      | examples  |                 | of the  | attention |                          |           |     |         |          |     |            |
5 ProbingAttentionHeadCombinations
| behavior. | While | the | similarity | between |     | machine- |     |     |     |     |     |     |     |
| --------- | ----- | --- | ---------- | ------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
learnedattentionweightsandhuman-definedsyn- Since individual attention heads specialize to par-
|                  |     |               |     |         |       |         | ticular | aspects | of  | syntax, | the | model’s | overall |
| ---------------- | --- | ------------- | --- | ------- | ----- | ------- | ------- | ------- | --- | ------- | --- | ------- | ------- |
| tactic relations |     | are striking, |     | we note | these | are re- |         |         |     |         |     |         |         |
lations for which attention heads do particularly “knowledge” about syntax is distributed across
wellon. TherearemanyrelationsforwhichBERT multiple attention heads. We now measure this
|     |     |     |     |     |     |     | overall | ability | by  | proposing | a   | novel | family of |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------- | --- | --------- | --- | ----- | --------- |
onlyslightlyimprovesoverthesimplebaseline,so
we would not say individual attention heads cap- attention-based probing classifiers and applying
| ture dependency |     | structure |     | as a whole. |     | We think |     |     |     |     |     |     |     |
| --------------- | --- | --------- | --- | ----------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
4Wetruncatedocumentsto128tokenslongtokeepmem-
| it would | be interesting |     | future | work | to extend | our | oryusagemanageable. |     |     |     |     |     |     |
| -------- | -------------- | --- | ------ | ---- | --------- | --- | ------------------- | --- | --- | --- | --- | --- | --- |

Model All Pronoun Proper Nominal and-wordsprobingclassifierassignstheprobabil-
ityofwordibeingwordj’sheadas
Nearest 27 29 29 19
n
Headmatch 52 47 67 40
p(i|j) ∝ exp W (v ⊕v )αk+
Rule-based 69 70 77 60 k,: i j ij
(cid:18)k=1
Neuralcoref 83* – – – (cid:88)
U (v ⊕v )αk
Head5-4 65 64 73 58 k,: i j ji
(cid:19)
*Only roughly comparable because on non-truncated docu- Where v denotes GloVe embeddings and ⊕ de-
mentsandwithdifferentmentiondetection.
notes concatenation. The GloVe embeddings are
Table 2: Accuracies (%) for systems at selecting a held fixed in training, so only the two weight ma-
correct antecedent given a coreferent mention in the trices W and U are learned. The dot product
CoNLL-2012data.OneofBERT’sattentionheadsper- W (v ⊕v )producesaword-sensitiveweightfor
k,: i j
formsfairlywellatcoreference.
theparticularattentionhead.
Results. We evaluate our methods on the Penn
them to dependency parsing. For these classifiers Treebank dev set annotated with Stanford depen-
we treat the BERT attention outputs as fixed, i.e., dencies. Wecompareagainstthreebaselines:
we do not back-propagate into BERT and only
• A right-branching baseline that always pre-
trainasmallnumberofparameters.
dictstheheadistothedependent’sright.
The probing classifiers are basically graph-
• Asimpleone-hidden-layernetworkthattakes
based dependency parsers. Given an input word,
asinputtheGloVeembeddingsforthedepen-
the classifier produces a probability distribution
dent and candidate head as well as distance
over other words in the sentence indicating how
featuresbetweenthetwowords.5
likely each other word is to be the syntactic head
ofthecurrentone. • Our attention-and-words probe, but with at-
tentionmapsfromaBERTnetworkwithpre-
Attention-Only Probe. Our first probe learns a
trained word/positional embeddings but ran-
simplelinearcombinationofattentionweights.
domlyinitializedotherweights. Thiskindof
n baseline is surprisingly strong at other prob-
p(i|j) ∝ exp w αk +u αk ingtasks(Conneauetal.,2018).
k ij k ji
(cid:18) (cid:88) k=1 (cid:19) ResultsareshowninTable3. WefindtheAttn+
GloVeprobingclassifiersubstantiallyoutperforms
where p(i|j) is the probability of word i being
our baselines and achieves a decent UAS of 77,
wordj’ssyntactichead,αk istheattentionweight
ij
suggesting BERT’s attention maps have a fairly
fromworditowordj producedbyheadk,andn
thoroughrepresentationofEnglishsyntax.
isthenumberofattentionheads. Weincludeboth
As a rough comparison, we also report results
directions of attention: candidate head to depen-
from the structural probe from Hewitt and Man-
dent as well as dependent to candidate head. The
ning (2019), which builds a probing classifier on
weightvectorsw anduaretrainedusingstandard
top of BERT’s vector representations rather than
supervisedlearningonthetrainset.
attention. The scores are not directly compara-
Attention-and-Words Probe. Given our finding
ble because the structural probe only uses a sin-
that heads specialize to particular syntactic rela-
glelayerofBERT,producesundirectedratherthan
tions,webelieveprobingclassifiersshouldbenefit
directed parse trees, and is trained to produce the
fromhavinginformationabouttheinputwords. In
syntactic distance between words rather than di-
particular, we build a model that sets the weights
rectly predicting the tree structure. Nevertheless,
of the attention heads based on the GloVe (Pen-
thesimilarityinscoretoourAttn+Gloveprobing
nington et al., 2014) embeddings for the input
classifier suggests there is not much more syntac-
words. Intuitively, if the dependent and candi-
tic information in BERT’s vector representations
date head are “the” and “cat,” the probing classi-
comparedtoitsattentionmaps.
fier should learn to assign most of the weight to
5Indicatorfeaturesforshortdistancesaswellascontinu-
the head 8-11, which achieves excellent perfor-
ousdistancefeatures,withdistanceahead/behindtreatedsep-
mance at the determiner relation. The attention- aratelytocapturewordorder

Model UAS
Structuralprobe 80UUAS*
Right-branching 26
Distances+GloVe 58
RandomInitAttn+GloVe 30
Attn 61
Attn+GloVe 77
Table 3: Results of attention-based probing classifiers
ondependencyparsing. AsimplemodeltakingBERT
attention maps and GloVe embeddings as input per-
formsquitewell.*Notdirectlycomparabletoournum-
bers;seetext.
Overall, our results from probing both individ-
ual and combinations of attention heads suggest
thatBERTlearnssomeaspectssyntaxpurelyasa
by-productofself-supervisedtraining. Otherwork
has drawn a similar conclusions from examin-
ingBERT’spredictionsonagreementtasks(Gold-
berg,2019)orinternalvectorrepresentations(He-
witt and Manning, 2019; Liu et al., 2019). Tra-
ditionally, syntax-aware models have been devel-
oped through architecture design (e.g., recursive
neural networks) or from direct supervision from
human-curatedtreebanks. Ourfindingsarepartof
a growing body of work indicating that indirect
supervision from rich pre-training tasks like lan-
guagemodelingcanalsoproducemodelssensitive
tolanguage’shierarchicalstructure.
6 ClusteringAttentionHeads
Are attention heads in the same layer similar to
each other or different? Can attention heads be Figure 6: BERT attention heads embedded in two-
clearlygroupedbybehavior? Weinvestigatethese dimensional space. Distance between points approx-
questions by computing the distances between all imately matches the average Jensen-Shannon diver-
gencesbetweentheoutputsofthecorrespondingheads.
pairsofattentionheads. Formally,wemeasurethe
Headsinthesamelayertendtobeclosetogether. At-
distancebetweentwoheads H and H as:
i j
tentionhead“behavior”wasfoundthroughtheanalysis
methodsdiscussedthroughoutthispaper.
JS(H (token),H (token))
i j
token∈data
(cid:88)
Where JS is the Jensen-Shannon Divergence be- have similarly, often corresponding to behaviors
tween attention distributions. Using these dis- we have already discussed in this paper. Heads
tances, we visualize the attention heads by apply- withinthesamelayerareoftenfairlyclosetoeach
ing multidimensional scaling (Kruskal, 1964) to other, meaning that heads within the layer have
embed each head in two dimensions such that the similarattentiondistributions. Thisfindingisabit
Euclidean distance between embeddings reflects surprisinggiventhatTuetal.(2018)showthaten-
the Jensen-Shannon distance between the corre- couragingattentionheadstohavedifferentbehav-
spondingheadsascloselyaspossible. iorscanimproveTransformerperformanceatma-
Results are shown in Figure 6. We find that chinetranslation. Onepossibilityfortheapparent
there are several clear clusters of heads that be- redundancy in BERT’s attention heads is the use

ofattentiondropout, whichcausessomeattention ralmachinetranslationsystemcapturesanaphora,
weightstobezeroed-outduringtraining. similartoourfindingforBERT.
|               |      |             |     |        |      |          | Concurrently |            | with             | our work    | Voita      | et        | al. (2019)  |
| ------------- | ---- | ----------- | --- | ------ | ---- | -------- | ------------ | ---------- | ---------------- | ----------- | ---------- | --------- | ----------- |
| 7 RelatedWork |      |             |     |        |      |          | identify     | syntactic, |                  | positional, |            | and       | rare-word-  |
|               |      |             |     |        |      |          | sensitive    | attention  | heads            |             | in machine |           | translation |
| There has     | been | substantial |     | recent | work | perform- |              |            |                  |             |            |           |             |
|               |      |             |     |        |      |          | models.      | They       | also demonstrate |             |            | that many | atten-      |
ing analysis to better understand what neural net- tion heads can be pruned away without substan-
| works learn, | especially |         | from     | language | model | pre-     |                |     |           |              |      |                |       |
| ------------ | ---------- | ------- | -------- | -------- | ----- | -------- | -------------- | --- | --------- | ------------ | ---- | -------------- | ----- |
|              |            |         |          |          |       |          | tially hurting |     | model     | performance. |      | Interestingly, |       |
| training.    | One        | line of | research | examines |       | the out- |                |     |           |              |      |                |       |
|              |            |         |          |          |       |          | the important  |     | attention | heads        | that | remain         | after |
puts of language models on carefully chosen in- pruning tend to be ones with identified behaviors.
| put sentences |           | (Linzen | et       | al., 2016; | Khandelwal |         |        |           |        |           |            |      |          |
| ------------- | --------- | ------- | -------- | ---------- | ---------- | ------- | ------ | --------- | ------ | --------- | ---------- | ---- | -------- |
|               |           |         |          |            |            |         | Michel | et al.    | (2019) | similarly | show       | that | many of  |
| et al., 2018; | Gulordava |         | et       | al., 2018; | Marvin     | and     |        |           |        |           |            |      |          |
|               |           |         |          |            |            |         | BERT’s | attention | heads  | can       | be pruned. |      | Although |
| Linzen,       | 2018).    | For     | example, | the        | model’s    | perfor- |        |           |        |           |            |      |          |
ouranalysisinthispaperonlyfoundinterpretable
mance at subject-verb agreement (generating the behaviors in a subset of BERT’s attention heads,
| correct | number | of a | verb | far away | from | its sub- |     |     |     |     |     |     |     |
| ------- | ------ | ---- | ---- | -------- | ---- | -------- | --- | --- | --- | --- | --- | --- | --- |
theserecentworkssuggestthattheremightnotbe
| ject) provides |     | a measure | of  | the model’s |     | syntactic |     |     |     |     |     |     |     |
| -------------- | --- | --------- | --- | ----------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
muchtoexplainforsomeattentionheadsbecause
ability,althoughitdoesnotrevealhowthatability theyhavelittleeffectonmodelperfomance.
iscapturedbythenetwork.
JainandWallace(2019)arguethatattentionof-
| Another | line            | of work | investigates |           | the  | internal |          |     |           |       |              |     |      |
| ------- | --------------- | ------- | ------------ | --------- | ---- | -------- | -------- | --- | --------- | ----- | ------------ | --- | ---- |
|         |                 |         |              |           |      |          | ten does | not | “explain” | model | predictions. |     | They |
| vector  | representations |         | of           | the model | (Adi | et al.,  |          |     |           |       |              |     |      |
showthatattentionweightsfrequentlydonotcor-
2017; Giulianelli et al., 2018; Zhang and Bow- relate with other measures of feature importance.
| man,2018),oftenusingprobingclassifiers. |     |     |     |     |     | Prob- |              |     |           |         |     |       |         |
| --------------------------------------- | --- | --- | --- | --- | --- | ----- | ------------ | --- | --------- | ------- | --- | ----- | ------- |
|                                         |     |     |     |     |     |       | Furthermore, |     | attention | weights | can | often | be sub- |
ingclassifiersaresimpleneuralnetworksthattake
|     |     |     |     |     |     |     | stantially | changed | without |     | altering | model | predic- |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | ------- | --- | -------- | ----- | ------- |
the vector representations of a pre-trained model tions. However, our motivation for looking at at-
as input and are trained to do a supervised task tention is different: rather than explaining model
| (e.g., part-of-speech |     |      | tagging). | If          | a probing | clas-    |              |         |        |         |     |              |        |
| --------------------- | --- | ---- | --------- | ----------- | --------- | -------- | ------------ | ------- | ------ | ------- | --- | ------------ | ------ |
|                       |     |      |           |             |           |          | predictions, | we      | are    | seeking | to  | understand   | infor- |
| sifier achieves       |     | high | accuracy, | it suggests |           | that the |              |         |        |         |     |              |        |
|                       |     |      |           |             |           |          | mation       | learned | by the | models. |     | For example, | if     |
inputrepresentationsreflectthecorrespondingas- a particular attention head learns a syntactic rela-
| pect of | language | (e.g., | low-level |     | syntax). | Like |          |          |      |     |           |         |      |
| ------- | -------- | ------ | --------- | --- | -------- | ---- | -------- | -------- | ---- | --- | --------- | ------- | ---- |
|         |          |        |           |     |          |      | tion, we | consider | that | an  | important | finding | from |
ourwork,someofthesestudieshavealsodemon-
|     |     |     |     |     |     |     | an analysis | perspective |     | even | if  | that head | is not |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ----------- | --- | ---- | --- | --------- | ------ |
strated models capturing aspects of syntax (Shi always used when making predictions for some
| et al., 2016; | Blevins |     | et al., | 2018) | or coreference |     |     |     |     |     |     |     |     |
| ------------- | ------- | --- | ------- | ----- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
downstreamtask.
| (Tenney                               | et al., | 2018, | 2019; | Liu et | al., 2019) | with- |              |     |     |     |     |     |     |
| ------------------------------------- | ------- | ----- | ----- | ------ | ---------- | ----- | ------------ | --- | --- | --- | --- | --- | --- |
| outexplicitlybeingtrainedforthetasks. |         |       |       |        |            |       | 8 Conclusion |     |     |     |     |     |     |
Withregardstoanalyzingattention,Vig(2019)
Wehaveproposedaseriesofanalysismethodsfor
| builds a                          | visualization |                            | tool          | for the        | BERT’s           | atten-    |               |             |                 |               |             |          |            |
| --------------------------------- | ------------- | -------------------------- | ------------- | -------------- | ---------------- | --------- | ------------- | ----------- | --------------- | ------------- | ----------- | -------- | ---------- |
|                                   |               |                            |               |                |                  |           | understanding |             | the attention   |               | mechanisms  |          | of mod-    |
| tion and                          | reports       | observations               |               | about          | the              | attention |               |             |                 |               |             |          |            |
|                                   |               |                            |               |                |                  |           | els and       | applied     | them            | to BERT.      | While       | most     | recent     |
| behavior,                         | but           | does not                   | perform       | quantitative   |                  | anal-     |               |             |                 |               |             |          |            |
|                                   |               |                            |               |                |                  |           | work on       | model       | analysis        | for           | NLP         | has      | focused on |
| ysis. Burns                       | et            | al.                        | (2018)        | analyze        | the              | attention |               |             |                 |               |             |          |            |
|                                   |               |                            |               |                |                  |           | probing       | vector      | representations |               | or          | model    | outputs,   |
| of memory                         | networks      |                            | to understand |                | model            | perfor-   |               |             |                 |               |             |          |            |
|                                   |               |                            |               |                |                  |           | we have       | shown       | that            | a substantial |             | amount   | of lin-    |
| manceonaquestionansweringdataset. |               |                            |               |                |                  | Therehas  |               |             |                 |               |             |          |            |
|                                   |               |                            |               |                |                  |           | guistic       | knowledge   | can             | be            | found       | not only | in the     |
| also been                         | some          | initial                    | work          | in correlating |                  | atten-    |               |             |                 |               |             |          |            |
|                                   |               |                            |               |                |                  |           | hidden        | states,     | but also        | in the        | attention   |          | maps. We   |
| tionwithsyntax.                   |               | RaganatoandTiedemann(2018) |               |                |                  |           |               |             |                 |               |             |          |            |
|                                   |               |                            |               |                |                  |           | think probing |             | attention       | maps          | complements |          | these      |
| evaluate                          | the attention |                            | heads         | of a           | machine          | trans-    |               |             |                 |               |             |          |            |
|                                   |               |                            |               |                |                  |           | other model   |             | analysis        | techniques,   |             | and      | should be  |
| lation model                      | on            | dependency                 |               | parsing,       | but              | only re-  |               |             |                 |               |             |          |            |
|                                   |               |                            |               |                |                  |           | part of       | the toolkit | used            | by            | researchers |          | to under-  |
| port overall                      | UAS           | scores                     |               | instead        | of investigating |           |               |             |                 |               |             |          |            |
standwhatneuralnetworkslearnaboutlanguage.
headsforspecificsyntacticrelationsorusingprob-
| ing classifiers. |     | Marecek | and | Rosa | (2018) | propose |     |     |     |     |     |     |     |
| ---------------- | --- | ------- | --- | ---- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- |
Acknowledgements
| heuristic | ways | of converting |     | attention |     | scores to |     |     |     |     |     |     |     |
| --------- | ---- | ------------- | --- | --------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
syntactic trees, but do not quantitatively evaluate We thank the anonymous reviews for their
theirapproach. Forcoreference,Voitaetal.(2018) thoughtful comments and suggestions. Kevin is
show that the attention of a context-aware neu- supportedbyaGooglePhDFellowship.

References Urvashi Khandelwal, He He, Peng Qi, and Daniel Ju-
|                            |                |     |         |                   |      | rafsky.                         | 2018. | Sharp | nearby, | fuzzy | far    | away: How |
| -------------------------- | -------------- | --- | ------- | ----------------- | ---- | ------------------------------- | ----- | ----- | ------- | ----- | ------ | --------- |
| Yossi Adi,                 | Einat Kermany, |     | Yonatan | Belinkov,         | Ofer |                                 |       |       |         |       |        |           |
|                            |                |     |         |                   |      | neurallanguagemodelsusecontext. |       |       |         |       | InACL. |           |
| Lavi,andYoavGoldberg.2017. |                |     |         | Fine-grainedanal- |      |                                 |       |       |         |       |        |           |
ysisofsentenceembeddingsusingauxiliarypredic- JosephBKruskal.1964. Multidimensionalscalingby
| tiontasks. | InICLR. |     |     |     |     |            |     |          |        |                |     |          |
| ---------- | ------- | --- | --- | --- | --- | ---------- | --- | -------- | ------ | -------------- | --- | -------- |
|            |         |     |     |     |     | optimizing |     | goodness | of fit | to a nonmetric |     | hypothe- |
sis. Psychometrika,29(1):1–27.
DzmitryBahdanau,KyunghyunCho,andYoshuaBen-
gio. 2015. Neural machine translation by jointly Heeyoung Lee, Yves Peirsman, Angel Chang,
learningtoalignandtranslate. InICLR. NathanaelChambers,MihaiSurdeanu,andDanJu-
|     |     |     |     |     |     | rafsky. | 2011. | Stanford’s |     | multi-pass | sieve | corefer- |
| --- | --- | --- | --- | --- | --- | ------- | ----- | ---------- | --- | ---------- | ----- | -------- |
Yonatan Belinkov, Nadir Durrani, Fahim Dalvi, Has- enceresolutionsystemattheconll-2011sharedtask.
| sanSajjad,andJamesR.Glass.2017. |     |     |     |     | Whatdoneu- | InCoNLL. |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | ---------- | -------- | --- | --- | --- | --- | --- | --- |
ralmachinetranslationmodelslearnaboutmorphol-
|     |     |     |     |     |     | Tal Linzen, | Emmanuel |     | Dupoux, | and | Yoav | Goldberg. |
| --- | --- | --- | --- | --- | --- | ----------- | -------- | --- | ------- | --- | ---- | --------- |
ogy? InACL.
2016. Assessingtheabilityoflstmstolearnsyntax-
Terra Blevins, Omer Levy, and Luke S. Zettlemoyer. sensitivedependencies. TACL.
| 2018. Deeprnnsencodesofthierarchicalsyntax. |     |     |     |     | In  |                                               |          |     |        |       |            |        |
| ------------------------------------------- | --- | --- | --- | --- | --- | --------------------------------------------- | -------- | --- | ------ | ----- | ---------- | ------ |
| ACL.                                        |     |     |     |     |     | NelsonF.Liu,MattGardner,YonatanBelinkov,M.Pe- |          |     |        |       |            |        |
|                                             |     |     |     |     |     | ters,                                         | and Noah | A.  | Smith. | 2019. | Linguistic | knowl- |
Kaylee Burns, Aida Nematzadeh, Alison Gopnik, and edge and transferability of contextual representa-
| Thomas | L. Griffiths. | 2018. | Exploiting |     | attention to | tions. | InNAACL-HLT. |     |     |     |     |     |
| ------ | ------------- | ----- | ---------- | --- | ------------ | ------ | ------------ | --- | --- | --- | --- | --- |
Black-
| reveal shortcomings |     | in  | memory | models. | In  |          |           |     |      |                    |     |     |
| ------------------- | --- | --- | ------ | ------- | --- | -------- | --------- | --- | ---- | ------------------ | --- | --- |
|                     |     |     |        |         |     | Mitchell | P Marcus, |     | Mary | Ann Marcinkiewicz, |     | and |
boxNLP@EMNLP.
|     |     |     |     |     |     | BeatriceSantorini.1993. |     |     |     | Buildingalargeannotated |     |     |
| --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | --- | ----------------------- | --- | --- |
Kehai Chen, Rui Wang, Masao Utiyama, Eiichiro corpus of english: The Penn treebank. Computa-
Sumita,andTiejunZhao.2018. Syntax-directedat- tionallinguistics,19(2):313–330.
| tentionforneuralmachinetranslation. |     |     |     |     | InAAAI. |               |     |     |        |       |       |          |
| ----------------------------------- | --- | --- | --- | --- | ------- | ------------- | --- | --- | ------ | ----- | ----- | -------- |
|                                     |     |     |     |     |         | David Marecek |     | and | Rudolf | Rosa. | 2018. | Extract- |
Alexis Conneau, Germa´n Kruszewski, Guillaume ing syntactic trees from transformer encoder self-
|          |                 |            |           |            |               | attentions.                       | InBlackboxNLP@EMNLP. |     |             |       |          |      |
| -------- | --------------- | ---------- | --------- | ---------- | ------------- | --------------------------------- | -------------------- | --- | ----------- | ----- | -------- | ---- |
| Lample,  | Lo¨ıc Barrault, |            | and Marco |            | Baroni. 2018. |                                   |                      |     |             |       |          |      |
| What you | can             | cram into  | a single  | $&!#*      | vector:       |                                   |                      |     |             |       |          |      |
|          |                 |            |           |            |               | Rebecca                           | Marvin               | and | Tal Linzen. | 2018. | Targeted | syn- |
| Probing  | sentence        | embeddings | for       | linguistic | proper-       |                                   |                      |     |             |       |          |      |
|          |                 |            |           |            |               | tacticevaluationoflanguagemodels. |                      |     |             |       | InEMNLP. |      |
ties. InACL.
|                            |     |         |     |                 |     | Paul Michel, | Omer | Levy, | and    | Graham | Neubig.   | 2019. |
| -------------------------- | --- | ------- | --- | --------------- | --- | ------------ | ---- | ----- | ------ | ------ | --------- | ----- |
| AndrewMDaiandQuocVLe.2015. |     |         |     | Semi-supervised |     |              |      |       |        |        |           |       |
|                            |     |         |     |                 |     | Are sixteen  |      | heads | really | better | than one? | arXiv |
| sequencelearning.          |     | InNIPS. |     |                 |     |              |      |       |        |        |           |       |
preprintarXiv:1905.10650.
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Jeffrey Pennington, Richard Socher, and Christopher
Kristina Toutanova. 2019. BERT: Pre-training of Manning. 2014. Glove: Global vectors for word
deepbidirectionaltransformersforlanguageunder-
|                        |              |                  |            |             |           | representation. |             | InEMNLP.     |        |                |             |           |
| ---------------------- | ------------ | ---------------- | ---------- | ----------- | --------- | --------------- | ----------- | ------------ | ------ | -------------- | ----------- | --------- |
| standing.              | InNAACL-HLT. |                  |            |             |           |                 |             |              |        |                |             |           |
|                        |              |                  |            |             |           | MatthewEPeters, |             | MarkNeumann, |        |                | MohitIyyer, | Matt      |
| Akiko Eriguchi,        | Kazuma       |                  | Hashimoto, | and         | Yoshimasa |                 |             |              |        |                |             |           |
|                        |              |                  |            |             |           | Gardner,        | Christopher |              | Clark, | Kenton         | Lee,        | and Luke  |
| Tsuruoka.              | 2016.        | Tree-to-sequence |            | attentional | neu-      |                 |             |              |        |                |             |           |
|                        |              |                  |            |             |           | Zettlemoyer.    |             | 2018.        | Deep   | contextualized |             | word rep- |
| ralmachinetranslation. |              |                  | InACL.     |             |           | resentations.   |             | InNAACL-HLT. |        |                |             |           |
Mario Giulianelli, Jack Harding, Florian Mohnert, SameerPradhan,AlessandroMoschitti,NianwenXue,
Dieuwke Hupkes, and Willem H. Zuidema. 2018. Olga Uryupina, and Yuchen Zhang. 2012. Conll-
Under the hood: Using diagnostic classifiers to in- 2012 shared task: Modeling multilingual unre-
| vestigate             | and improve | how | language             |     | models track |          |             |     |               |     |          |         |
| --------------------- | ----------- | --- | -------------------- | --- | ------------ | -------- | ----------- | --- | ------------- | --- | -------- | ------- |
|                       |             |     |                      |     |              | stricted | coreference |     | in ontonotes. |     | In Joint | Confer- |
| agreementinformation. |             |     | InBlackboxNLP@EMNLP. |     |              |          |             |     |               |     |          |         |
enceonEMNLPandCoNLL-SharedTask.
Yoav Goldberg. 2019. Assessing BERT’s syntactic Alec Radford, Karthik Narasimhan, Tim Salimans,
abilities. arXivpreprintarXiv:1901.05287. and Ilya Sutskever. 2018. Improving lan-
|     |     |     |     |     |     | guage | understanding |     | by  | generative |     | pre-training. |
| --- | --- | --- | --- | --- | --- | ----- | ------------- | --- | --- | ---------- | --- | ------------- |
KristinaGulordava,PiotrBojanowski,EdouardGrave, https://blog.openai.com/language-unsupervised.
| Tal Linzen, | and | Marco | Baroni. | 2018. | Colorless |     |     |     |     |     |     |     |
| ----------- | --- | ----- | ------- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- |
green recurrent networks dream hierarchically. In Alessandro Raganato and Jo¨rg Tiedemann. 2018.
| NAACL-HLT.                              |     |     |     |              |       | An                | analysis | of    | encoder | representations |           | in        |
| --------------------------------------- | --- | --- | --- | ------------ | ----- | ----------------- | -------- | ----- | ------- | --------------- | --------- | --------- |
|                                         |     |     |     |              |       | transformer-based |          |       | machine | translation.    |           | In Black- |
| JohnHewittandChristopherD.Manning.2019. |     |     |     |              | Find- | boxNLP@EMNLP.     |          |       |         |                 |           |           |
| ingsyntaxwithstructuralprobes.          |     |     |     | InNAACL-HLT. |       |                   |          |       |         |                 |           |           |
|                                         |     |     |     |              |       | Rico Sennrich,    |          | Barry | Haddow, | and             | Alexandra | Birch.    |
SarthakJainandByronC.Wallace.2019. Attentionis 2016. Neuralmachinetranslationofrarewordswith
notexplanation. arXivpreprintarXiv:1902.10186. subwordunits. InACL.

Xing Shi, Inkit Padhi, and Kevin Knight. 2016. Does
string-based neural mt learn source syntax? In
EMNLP.
Emma Strubell, Patrick Verga, Daniel Andor,
David I Weiss, and Andrew McCallum. 2018.
Linguistically-informed self-attention for semantic
rolelabeling. InEMNLP.
Mukund Sundararajan, Ankur Taly, and Qiqi Yan.
2017. Axiomatic attribution for deep networks. In
ICML.
Ian Tenney, Dipanjan Das, and Ellie Pavlick. 2019.
Bert rediscovers the classical nlp pipeline. arXiv
preprintarXiv:1905.05950.
Ian Tenney, Patrick Xia, Berlin Chen, Alex Wang,
Adam Poliak, R Thomas McCoy, Najoung Kim,
Benjamin Van Durme, Samuel R Bowman, Dipan-
jan Das, et al. 2018. What do you learn from con-
text? probing for sentence structure in contextual-
izedwordrepresentations. InICLR.
Zhaopeng Tu, Baosong Yang, Michael R. Lyu, and
Tong Zhang. 2018. Multi-head attention with dis-
agreementregularization. InEMNLP.
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz
Kaiser, and Illia Polosukhin. 2017. Attention is all
youneed. InNIPS.
Jesse Vig. 2019. Visualizing attention in transformer-
based language models. arXiv preprint
arXiv:1904.02679.
ElenaVoita,PavelSerdyukov,RicoSennrich,andIvan
Titov.2018. Context-awareneuralmachinetransla-
tionlearnsanaphoraresolution. InACL.
Elena Voita, David Talbot, Fedor Moiseev, Rico Sen-
nrich, and Ivan Titov. 2019. Analyzing multi-
headself-attention: Specializedheadsdotheheavy
lifting, the rest can be pruned. arXiv preprint
arXiv:1905.09418.
SamJoshuaWiseman,AlexanderMatthewRush, Stu-
artMerrillShieber,andJasonWeston.2015. Learn-
inganaphoricityandantecedentrankingfeaturesfor
coreferenceresolution. InACL.
Kelly W. Zhang and Samuel R. Bowman. 2018. Lan-
guagemodelingteachesyoumoresyntaxthantrans-
lation does: Lessons learned through auxiliary task
analysis. InBlackboxNLP@EMNLP.