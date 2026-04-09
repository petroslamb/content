|     |     | BERT | Rediscovers     | the          | Classical        | NLP             | Pipeline |     |     |     |
| --- | --- | ---- | --------------- | ------------ | ---------------- | --------------- | -------- | --- | --- | --- |
|     |     |      | IanTenney1      | DipanjanDas1 |                  | ElliePavlick1,2 |          |     |     |     |
|     |     |      | 1GoogleResearch |              | 2BrownUniversity |                 |          |     |     |     |
{iftenney,dipanjand,epavlick}@google.com
|             |           | Abstract |                 |     | of the | network       | directly,  | to         | assess | whether there |
| ----------- | --------- | -------- | --------------- | --- | ------ | ------------- | ---------- | ---------- | ------ | ------------- |
|             |           |          |                 |     | exist  | localizable   | regions    | associated |        | with distinct |
| Pre-trained | text      | encoders | have rapidly    | ad- |        |               |            |            |        |               |
|             |           |          |                 |     | types  | of linguistic | decisions. |            | Such   | work has pro- |
| vanced      | the state | of       | the art on many | NLP |        |               |            |            |        |               |
9102 guA 9  ]LC.sc[  2v05950.5091:viXra ducedevidencethatdeeplanguagemodelscanen-
| tasks. | We focus | on  | one such model, | BERT, |     |     |     |     |     |     |
| ------ | -------- | --- | --------------- | ----- | --- | --- | --- | --- | --- | --- |
andaimtoquantifywherelinguisticinforma- code a range of syntactic and semantic informa-
tion is captured within the network. We find tion (e.g. Shi et al., 2016; Belinkov, 2018; Ten-
that the model represents the steps of the tra- neyetal.,2019),andthatmorecomplexstructures
ditional NLP pipeline in an interpretable and are represented hierarchically in the higher layers
| localizable | way, | and         | that the regions | respon- |        |       |         |         |        |                 |
| ----------- | ---- | ----------- | ---------------- | ------- | ------ | ----- | ------- | ------- | ------ | --------------- |
|             |      |             |                  |         | of the | model | (Peters | et al., | 2018b; | Blevins et al., |
| sible for   | each | step appear | in the expected  | se-     |        |       |         |         |        |                 |
2018).
| quence:     | POStagging,parsing,NER,semantic |       |               |          |                                   |       |                |      |          |          |
| ----------- | ------------------------------- | ----- | ------------- | -------- | --------------------------------- | ----- | -------------- | ---- | -------- | -------- |
|             |                                 |       |               |          | We                                | build | on this latter | line | of work, | focusing |
| roles, then | coreference.                    |       | Qualitative   | analysis |                                   |       |                |      |          |          |
|             |                                 |       |               |          | ontheBERTmodel(Devlinetal.,2019), |       |                |      |          | anduse   |
| reveals     | that the                        | model | can and often | does ad- |                                   |       |                |      |          |          |
justthispipelinedynamically, revisinglower- a suite of probing tasks (Tenney et al., 2019) de-
leveldecisionsonthebasisofdisambiguating
rivedfromthetraditionalNLPpipelinetoquantify
informationfromhigher-levelrepresentations. where specific types of linguistic information are
|     |     |     |     |     | encoded. | Building | on  | observations |     | (Peters et al., |
| --- | --- | --- | --- | --- | -------- | -------- | --- | ------------ | --- | --------------- |
1 Introduction
|     |     |     |     |     | 2018b) | that | lower layers | of  | a language | model en- |
| --- | --- | --- | --- | --- | ------ | ---- | ------------ | --- | ---------- | --------- |
Pre-trainedsentenceencoderssuchasELMo(Pe- codemorelocalsyntaxwhilehigherlayerscapture
ters et al., 2018a) and BERT (Devlin et al., 2019) more complex semantics, we present two novel
haverapidlyimprovedthestateoftheartonmany contributions. First, we present an analysis that
NLPtasks,andseempoisedtodisplacebothstatic spans the common components of a traditional
word embeddings (Mikolov et al., 2013) and dis- NLP pipeline. We show that the order in which
cretepipelines(Manningetal.,2014)asthebasis specificabstractionsareencodedreflectsthetradi-
for natural language processing systems. While tional hierarchy of these tasks. Second, we quali-
thishasbeenaboonforperformance,ithascome tativelyanalyzehowindividualsentencesarepro-
at the cost of interpretability, and it remains un- cessed by the BERT network, layer-by-layer. We
clearwhethersuchmodelsareinfactlearningthe show that while the pipeline order holds in ag-
kindofabstractionsthatweintuitivelybelieveare gregate, the model can allow individual decisions
importantforrepresentingnaturallanguage,orare to depend on each other in arbitrary ways, de-
simply modeling complex co-occurrence statis- ferring ambiguous decisions or revising incorrect
tics.
onesbasedonhigher-levelinformation.
| A wave                                        | of recent | work     | has begun       | to “probe” |         |     |     |     |     |     |
| --------------------------------------------- | --------- | -------- | --------------- | ---------- | ------- | --- | --- | --- | --- | --- |
| state-of-the-artmodelstounderstandwhetherthey |           |          |                 |            | 2 Model |     |     |     |     |     |
| are representing                              |           | language | in a satisfying | way.       |         |     |     |     |     |     |
Much of this work is behavior-based, designing Edge Probing. Our experiments are based on
controlled test sets and analyzing errors in order the “edge probing” approach of Tenney et al.
to reverse-engineer the types of abstractions the (2019), which aims to measure how well infor-
model may or may not be representing (e.g. Con- mation about linguistic structure can be extracted
neauetal.,2018;MarvinandLinzen,2018;Poliak fromapre-trainedencoder. Edgeprobingdecom-
et al., 2018). Parallel efforts inspect the structure poses structured-prediction tasks into a common

format, where a probing classifier receives spans Limitations This work is intended to be ex-
s = [i ,j ) and (optionally) s = [i ,j ) and ploratory. We focus on one particular encoder–
1 1 1 2 2 2
must predict a label such as a constituent or rela- BERT–to explore how information can be orga-
tion type.1 The probing classifier has access only nizedinadeeplanguagemodel, andfurtherwork
to the per-token contextual vectors within the tar- is required to determine to what extent the trends
getspans,andsomustrelyontheencodertopro- hold in general. Furthermore, our work carries
vide information about the relation between these thelimitationsofallinspection-basedprobing: the
spansandtheirroleinthesentence. factthatalinguisticpatternisnotobservedbyour
We use eight labeling tasks from the edge probing classifier does not guarantee that it is not
probing suite: part-of-speech (POS), constituents there, and the observation of a pattern does not
(Consts.), dependencies (Deps.), entities, seman- tell us how it is used. For this reason, we empha-
tic role labeling (SRL), coreference (Coref.), se- sizetheimportanceofcombiningstructuralanaly-
mantic proto-roles (SPR; Reisinger et al., 2015), siswithbehavioralstudies(asdiscussedin§1)to
andrelationclassification(SemEval). Thesetasks provideamorecompletepictureofwhatinforma-
arederivedfromstandardbenchmarkdatasets,and tion these models encode and how that informa-
evaluated with a common metric–micro-averaged tionaffectsperformanceondownstreamtasks.
F1–tofacilitatecomparisonacrosstasks. 2
3 Metrics
BERT. The BERT model (Devlin et al., 2019)
We define two complementary metrics. The first,
has shown state-of-the-art performance on many
scalar mixing weights (§3.1) tell us which lay-
tasks, and its deep Transformer architecture
ers, in combination, are most relevant when a
(Vaswani et al., 2017) is typical of many recent
probing classifier has access to the whole BERT
models(e.g.Radfordetal.,2018,2019;Liuetal.,
model. Thesecond,cumulativescoring(§3.2)tells
2019). We focus on the stock BERT models
us how much higher we can score on a probing
(base and large, uncased), which are trained with
task with the introduction of each layer. These
amulti-taskobjective(maskedlanguagemodeling
metrics provide complementary views on what is
and next-sentence prediction) over a 3.3B word
happening inside the model. Mixing weights are
Englishcorpus. Sincewewanttounderstandhow
learned solely from the training data–they tell us
thenetworkrepresentslanguageasaresultofpre-
whichlayerstheprobingmodelfindsmostuseful.
training, we follow Tenney et al. (2019) (depart-
In contrast, cumulative scoring is derived entirely
ingfromstandardBERTusage)andfreezetheen-
from an evaluation set, and tell us how many lay-
coderweights. Thispreventstheencoderfromre-
ersareneededforacorrectprediction.
arrangingitsinternalrepresentationstobettersuit
theprobingtask.
3.1 ScalarMixingWeights
Given input tokens T = [t ,t ,...,t ],
0 1 n
To pool across layers, we use the scalar mixing
a deep encoder produces a set of layer ac-
technique introduced by the ELMo model. Fol-
tivations H(0),H(1),...,H(L), where H((cid:96)) =
((cid:96)) ((cid:96)) ((cid:96)) lowing Equation (1) of Peters et al. (2018a), for
[h ,h ,...,h ] are the activation vectors of
0 1 n each task we introduce scalar parameters γ and
the (cid:96)th encoder layer and H(0) corresponds to the τ
(0) (1) (L)
a ,a ,...,a ,andlet:
non-contextual word(piece) embeddings. We use τ τ τ
a weighted sum across layers (§3.1) to pool these
L
into a single set of per-token representation vec- h = γ (cid:88) s((cid:96))h ((cid:96)) (1)
i,τ τ τ i
tors H = [h ,h ,...,h ], and train a probing
0 1 n (cid:96)=0
classifier P for each task using the architecture
τ
andprocedureofTenneyetal.(2019). wheres τ = softmax(a τ ). Welearntheseweights
jointly with the probing classifier P , in order to
τ
1For single-span tasks (POS, entities, and constituents), allowittoextractinformationfromthemanylay-
s isnotused.ForPOS,s =[i,i+1)isasingletoken.
2 1 ers of an encoder without adding a large number
2We use the code from https://github.com/
jsalt18-sentence-repl/jiant. Dependencies is ofparameters. Aftertheprobingmodelistrained,
theEnglishWebTreebank(Silveiraetal.,2014),SPRisthe we extract the learned coefficients in order to es-
SPR1 dataset of (Teichert et al., 2017), and relations is Se-
timate the contribution of different layers to that
mEval2010Task8(Hendrickxetal.,2009). Allothertasks
arefromOntoNotes5.0(Weischedeletal.,2013). particulartask. Weinterprethigherweightsasev-

| Figure1: | SummarystatisticsonBERT-large. |     |     |     | Columns |     |     |     |     |     |     |     |     |
| -------- | ------------------------------ | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
(P(0))
| on left show | F1  | dev-set scores | for | the baseline |     |     |     |     |     |     |     |     |     |
| ------------ | --- | -------------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
τ
andfull-model(P(L))probes.
|           |          | τ           | Dark(blue)arethemix- |               |     |     |     |     |     |     |     |     |     |
| --------- | -------- | ----------- | -------------------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ingweight | centerof | gravity(Eq. | 2);                  | light(purple) | are |     |     |     |     |     |     |     |     |
theexpectedlayerfromthecumulativescores(Eq.4).
idencethatthecorrespondinglayercontainsmore
informationrelatedtothatparticulartask.
| Center-of-Gravity. |     | As  | a summary | statistic, | we  |     |     |     |     |     |     |     |     |
| ------------------ | --- | --- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
definethemixingweightcenterofgravityas:
L
|     |     | E¯           | (cid:88) (cid:96)·s((cid:96)) |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ------------ | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | [(cid:96)] = |                               |     | (2) |     |     |     |     |     |     |     |     |
|     |     | s            |                               | τ   |     |     |     |     |     |     |     |     |     |
(cid:96)=0
Thisreflectstheaveragelayerattendedtoforeach
task;intuitively,wecaninterpretahighervalueto
mean that the information needed for that task is Figure 2: Layer-wise metrics on BERT-large. Solid
capturedbyhigherlayers. (blue)aremixingweightss((cid:96))(§3.1);outlined(purple)
τ
|     |     |     |     |     |     | aredifferentialscores∆((cid:96)) |     |     |     | (§3.2),normalizedforeach |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | ------------------------ | --- | --- | --- |
τ
3.2 CumulativeScoring
task. Horizontalaxisisencoderlayer.
| We would | like | to estimate | at which | layer | in the |     |     |     |     |     |     |     |     |
| -------- | ---- | ----------- | -------- | ----- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
encoder a target (s ,s ,label) can be correctly andweseeintuitivelythatperformance(F1score)
|     |     | 1 2 |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
generallyincreasesasmorelayersareadded.3
| predicted. | Mixing | weights | cannot | tell | us this di- |     |     |     |     |     |     |     | We  |
| ---------- | ------ | ------- | ------ | ---- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
((cid:96))
rectly,becausetheyarelearnedasparametersand can then compute a differential score ∆ , which
τ
| do not correspond |     | to a | distribution | over | data. A |          |     |     |             |     |       |             |     |
| ----------------- | --- | ---- | ------------ | ---- | ------- | -------- | --- | --- | ----------- | --- | ----- | ----------- | --- |
|                   |     |      |              |      |         | measures |     | how | much better | we  | do on | the probing |     |
naive classifier at a single layer cannot either, be- taskifweobserveoneadditionalencoderlayer(cid:96):
| cause information |        | about   | a particular | span   | may be   |     |             |                                           |     |     |     |     |     |
| ----------------- | ------ | ------- | ------------ | ------ | -------- | --- | ----------- | ----------------------------------------- | --- | --- | --- | --- | --- |
| spread out        | across | several | layers,      | and as | observed |     |             |                                           |     |     |     |     |     |
|                   |        |         |              |        |          |     | ∆((cid:96)) | = Score(P((cid:96)))−Score(P((cid:96)−1)) |     |     |     |     | (3) |
|                   |        |         |              |        |          |     |             | τ                                         | τ   |     |     | τ   |     |
inPetersetal.(2018b)theencodermaychooseto
discardinformationathigherlayers.
|            |     |                |          |     |             | Expected |     | Layer. | Again, |     | we  | compute | a   |
| ---------- | --- | -------------- | -------- | --- | ----------- | -------- | --- | ------ | ------ | --- | --- | ------- | --- |
| To address |     | this, we train | a series | of  | classifiers |          |     |        |        |     |     |         |     |
((cid:96)) (pseudo)4 expectation over the differential scores
| {P } | which | use scalar | mixing | (Eq. 1) | to attend |     |     |     |     |     |     |     |     |
| ---- | ----- | ---------- | ------ | ------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
τ (cid:96)
|                                           |     |     |     |     |            | as                                         | a summary |     | statistic. | To focus | on  | the behavior |     |
| ----------------------------------------- | --- | --- | --- | --- | ---------- | ------------------------------------------ | --------- | --- | ---------- | -------- | --- | ------------ | --- |
| tolayer(cid:96)aswellasallpreviouslayers. |     |     |     | P   | (0) corre- |                                            |           |     |            |          |     |              |     |
|                                           |     |     |     |     | τ          | ofthecontextualencoderlayers,weomitthecon- |           |     |            |          |     |              |     |
spondstoanon-contextualbaselinethatusesonly
tributionofboththe“trivial”examplesresolvedat
(L)
| a bag of        | word(piece) | embeddings, |            | while | P =      |       |     |         |        |           |          |     |      |
| --------------- | ----------- | ----------- | ---------- | ----- | -------- | ----- | --- | ------- | ------ | --------- | -------- | --- | ---- |
|                 |             |             |            |       | τ        | layer | 0,  | as well | as the | remaining | headroom |     | from |
| P τ corresponds |             | to probing  | all layers | of    | the BERT |       |     |         |        |           |          |     |      |
model.
3Notethatifanewlayerprovidesdistractingfeatures,the
These classifiers are cumulative, in the sense probingmodelcanoverfitandperformancecandrop.Wesee
| ((cid:96)+1) |                                  |     |     |     |     | thisinparticularinthelast1-2layers(Figure2). |                                                  |     |     |     |     |     |     |
| ------------ | -------------------------------- | --- | --- | --- | --- | -------------------------------------------- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- |
| thatP        | hasasimilarnumberofparametersbut |     |     |     |     |                                              |                                                  |     |     |     |     |     |     |
| τ            |                                  |     |     |     |     |                                              | 4ThisisnotatrueexpectationbecausetheF1scoreisnot |     |     |     |     |     |     |
((cid:96))
withaccesstostrictlymoreinformationthanP , anexpectationoverexamples.
τ

thefullmodel. Let: firstfewlayersofthemodel(layers1-7forBERT-
large), i.e. most examples can be correctly classi-
E¯ [(cid:96)] =
(cid:80)L
(cid:96)=1 (cid:96)·∆
(
τ
(cid:96))
(4) fied very early on. We attribute this to the avail-
∆ (cid:80)L
∆
((cid:96)) ability of heuristic shortcuts: while challenging
(cid:96)=1 τ
examples may not be resolved until much later,
This can be thought of as, approximately, the ex- many cases can be guessed from shallow statis-
pectedlayeratwhichtheprobingmodelcorrectly tics. Conversely,weobservethatthelearnedmix-
labels an example, assuming that example is re- ingweightsareconcentratedmuchlater,layers9-
solvedatsomelayer(cid:96) ≥ 1oftheencoder. 20forBERT-large. Weobserve–particularlywhen
weights are highly concentrated–that the highest
4 Results weights are found on or just after the highest lay-
((cid:96))
ers which give an improvement ∆ in F1 score
τ
Figure 1 reports summary statistics and absolute
forthattask.
F1 scores, and Figure 2 reports per-layer metrics.
This helps explain the observations on the se-
Both show results on the 24-layer BERT-large
mantic relations and SPR tasks: cumulative scor-
model. We also report K((cid:63)) = KL((cid:63)||Uniform)
ingshowscontinuedimprovementuptothehigh-
to estimate how non-uniform5 each statistic ((cid:63) =
est layers of the model, while the lack of con-
s ,∆ )isforeachtask.
τ τ centration in the mixing weights suggest that the
BERT encoder does not expose a localized set of
Linguistic Patterns. We observe a consistent
featuresthatencodethesemoresemanticphenom-
trend across both of our metrics, with the tasks
ena. Similarly for entity types, we see contin-
encoded in a natural progression: POS tags pro-
ued improvements in the higher layers – perhaps
cessed earliest, followed by constituents, depen-
related to fine-grained semantic distinctions like
dencies, semantic roles, and coreference. That is,
”Organization” (ORG) vs. ”Geopolitical Entity”
itappearsthatbasicsyntacticinformationappears
(GPE)–whilethelowvaluefortheexpectedlayer
earlier in the network, while high-level semantic
reflects that many examples require only limited
informationappearsathigherlayers. Wenotethat
contexttoresolve.
this finding is consistent with initial observations
by Peters et al. (2018b), which found that con- ComparisonofEncoders. Weobservethesame
stituentsarerepresentedearlierthancoreference. general ordering on the 12-layer BERT-base
Inaddition,weobservethatingeneral,syntactic model (Figure A.2). In particular, there appears
information is more localizable, with weights re- to be a “stretching effect”, where the representa-
latedtosyntactictaskstendingtobeconcentrated tions for a given task tend to concentrate at the
on a few layers (high K(s) and K(∆)), while in- same layers relative to the top of the model; this
formation related to semantic tasks is generally isillustratedside-by-sideinFigureA.3.
spread across the entire network. For example,
wefindthatforsemanticrelationsandproto-roles 4.1 Per-ExampleAnalysis
(SPR), the mixing weights are close to uniform, We explore, qualitatively, how beliefs about the
andthatnontrivialexamplesforthesetasksarere- structure of individual sentences develop over the
solved gradually across nearly all layers. For en- layers of the BERT network. The OntoNotes de-
tity labeling many examples are resolved in layer velopment set contains annotations for five of our
1, but with a long tail thereafter, and only a weak probing tasks: POS, constituents, entities, SRL,
concentration of mixing weights in high layers. and coreference. We compile the predictions of
Further study is needed to determine whether this ((cid:96))
the per-layer classifiers P for each task. Be-
τ
is because BERT has difficulty representing the
causemanyannotationsareuninteresting–forex-
correct abstraction for these tasks, or because se-
ample, 89% of part-of-speech tags are correct at
manticinformationisinherentlyhardertolocalize.
layer 0 – we use a heuristic to identify ambigu-
ous sentences to visualize.6 Figure 3 shows two
Comparison of Metrics. For many tasks, we
find that the differential scores are highest in the 6Specifically, we look for target edges (s , s , label)
1 2
where the highest scoring label has an average score
5KL((cid:63)||Uniform)=−H((cid:63))+Constant,sohigherval-
L+
1
1
(cid:80)L
(cid:96)=0
P
τ
((cid:96))(label|s
1
,s
2
)≤0.7,andlookatsentences
uescorrespondtolowerentropy. withmorethanonesuchedge.

| (a) he smoked |     | toronto in | the playoffs |     | with six | hits, seven |     |     |     |     |     |     |     |
| ------------- | --- | ---------- | ------------ | --- | -------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
walksandeightstolenbases... trainingcorpus,andcumulativescoring,measured
|     |     |     |     |     |     |     | on an evaluation |          | set, | and     | show that | a     | consistent  |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | -------- | ---- | ------- | --------- | ----- | ----------- |
|     |     |     |     |     |     |     | ordering         | emerges. |      | We find | that      | while | this tradi- |
tionalpipelineorderholdsintheaggregate,onin-
dividualexamplesthenetworkcanresolveout-of-
order,usinghigh-levelinformationlikepredicate-
argumentrelationstohelpdisambiguatelow-level
|     |     |     |     |     |     |     | decisions | like | part-of-speech. |     | This | provides | new |
| --- | --- | --- | --- | --- | --- | --- | --------- | ---- | --------------- | --- | ---- | -------- | --- |
(b)chinatodayblackedoutacnninterviewthatwas...
|     |     |     |     |     |     |     | evidence | corroborating |             | that          | deep         | language | mod-    |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------- | ----------- | ------------- | ------------ | -------- | ------- |
|     |     |     |     |     |     |     | els can  | represent     | the         | types         | of syntactic |          | and se- |
|     |     |     |     |     |     |     | mantic   | abstractions  |             | traditionally |              | believed | neces-  |
|     |     |     |     |     |     |     | sary for | language      | processing, |               | and          | moreover | that    |
theycanmodelcomplexinteractionsbetweendif-
ferentlevelsofhierarchicalinformation.
Acknowledgments
ThankstoKentonLee,EmilyPitler,andJonClark
|     |     |     |     |     |     |     | for helpful | comments |            | and | feedback,   | and | to the   |
| --- | --- | --- | --- | --- | --- | --- | ----------- | -------- | ---------- | --- | ----------- | --- | -------- |
|     |     |     |     |     |     |     | members     | of       | the Google |     | AI Language |     | team for |
Figure 3: Probing classifier predictions across lay- manyproductivediscussions.
| ers of              | BERT-base.                             | Blue     | is           | the correct |           | label; or- |            |           |       |     |          |          |        |
| ------------------- | -------------------------------------- | -------- | ------------ | ----------- | --------- | ---------- | ---------- | --------- | ----- | --- | -------- | -------- | ------ |
| ange is             | the incorrect                          | label    | with         | highest     | average   | score      |            |           |       |     |          |          |        |
| overlayers.         | Barheightsare(normalized)probabilities |          |              |             |           |            | References |           |       |     |          |          |        |
| P((cid:96))(label|s |                                        | ,s ). In | the interest |             | of space, | only se-   |            |           |       |     |          |          |        |
| τ                   | 1                                      | 2        |              |             |           |            | Yonatan    | Belinkov. | 2018. | On  | internal | language | repre- |
lectedannotationsareshown.
|     |     |     |     |     |     |     | sentationsindeeplearning: |     |            |              | Ananalysisofmachine |       |         |
| --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | ---------- | ------------ | ------------------- | ----- | ------- |
|     |     |     |     |     |     |     | translation               |     | and speech | recognition. |                     | Ph.D. | thesis, |
selectedexamples,andmorearepresentedinAp-
MassachusettsInstituteofTechnology.
pendixA.2.
|         |         |         |              |     |          |          | Terra Blevins, |      | Omer | Levy,  | and Luke          | Zettlemoyer. |         |
| ------- | ------- | ------- | ------------ | --- | -------- | -------- | -------------- | ---- | ---- | ------ | ----------------- | ------------ | ------- |
| We find | that    | while   | the pipeline |     | order    | holds on |                |      |      |        |                   |              |         |
|         |         |         |              |     |          |          | 2018.          | Deep | RNNs | encode | soft hierarchical |              | syntax. |
| average | (Figure | 2), for | individual   |     | examples | the      |                |      |      |        |                   |              |         |
InProceedingsofACL.
| model               | is free | to and    | often    | does           | choose    | a differ- |                                      |          |            |     |                |         |             |
| ------------------- | ------- | --------- | -------- | -------------- | --------- | --------- | ------------------------------------ | -------- | ---------- | --- | -------------- | ------- | ----------- |
|                     |         |           |          |                |           |           | Alexis                               | Conneau, | Germa´n    |     | Kruszewski,    |         | Guillaume   |
| ent order.          | In      | the first | example, |                | the model | origi-    |                                      |          |            |     |                |         |             |
|                     |         |           |          |                |           |           | Lample,                              | Lo¨ıc    | Barrault,  | and | Marco          | Baroni. | 2018.       |
| nally (incorrectly) |         | assumes   |          | that “Toronto” |           | refers    |                                      |          |            |     |                |         |             |
|                     |         |           |          |                |           |           | Whatyoucancramintoasingle$&#*vector: |          |            |     |                |         | Prob-       |
| to the              | city,   | tagging   | it as    | a GPE.         | However,  | af-       |                                      |          |            |     |                |         |             |
|                     |         |           |          |                |           |           | ing sentence                         |          | embeddings |     | for linguistic |         | properties. |
ter resolving the semantic role – determining that InProceedingsofACL.
| “Toronto”           | is  | the thing | getting | “smoked”   |        | (ARG1)      |               |            |          |        |        |              |          |
| ------------------- | --- | --------- | ------- | ---------- | ------ | ----------- | ------------- | ---------- | -------- | ------ | ------ | ------------ | -------- |
|                     |     |           |         |            |        |             | Jacob Devlin, |            | Ming-Wei | Chang, | Kenton |              | Lee, and |
| – the entity-typing |     | decision  |         | is revised |        | in favor of |               |            |          |        |        |              |          |
|                     |     |           |         |            |        |             | Kristina      | Toutanova. |          | 2019.  | BERT:  | Pre-training | of       |
| ORG (i.e.           | the | sports    | team).  | In the     | second | exam-       |               |            |          |        |        |              |          |
deepbidirectionaltransformersforlanguageunder-
ple,themodelinitiallytags“today”asacommon standing. InProceedingsofNAACL.
(ARGM-TMP).
| noun, date, | and  | temporal | modifier      |     |     |          |                 |        |          |          |               |     |           |
| ----------- | ---- | -------- | ------------- | --- | --- | -------- | --------------- | ------ | -------- | -------- | ------------- | --- | --------- |
|             |      |          |               |     |     |          | Iris Hendrickx, |        | Su       | Nam Kim, | Zornitsa      |     | Kozareva, |
| However,    | this | phrase   | is ambiguous, |     | and | it later |                 |        |          |          |               |     |           |
|             |      |          |               |     |     |          | Preslav         | Nakov, | Diarmuid |          | O´ Se´aghdha, |     | Sebastian |
reinterprets “china today” as a proper noun (i.e. Pado´, Marco Pennacchiotti, Lorenza Romano, and
|        |          |     |         |     |         |           | Stan | Szpakowicz. |     | 2009. | Semeval-2010 |     | task 8: |
| ------ | -------- | --- | ------- | --- | ------- | --------- | ---- | ----------- | --- | ----- | ------------ | --- | ------- |
| the TV | network) | and | updates | its | beliefs | about the |      |             |     |       |              |     |         |
entitytype(toORG),followedbythesemanticrole Multi-way classification of semantic relations be-
|     |     |     |     |     |     |     | tween | pairs | of nominals. |     | In  | Proceedings | of  |
| --- | --- | --- | --- | --- | --- | --- | ----- | ----- | ------------ | --- | --- | ----------- | --- |
(reinterpretingitastheagentARG0).
|     |     |     |     |     |     |     | the Workshop |     | on  | Semantic | Evaluations: |     | Recent |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | -------- | ------------ | --- | ------ |
AchievementsandFutureDirections.
5 Conclusion
XiaodongLiu,PengchengHe,WeizhuChen,andJian-
We employ the edge probing task suite to explore feng Gao. 2019. Multi-task deep neural networks
howthedifferentlayersoftheBERTnetworkcan for natural language understanding. arXiv preprint
| resolve   | syntactic | and     | semantic | structure     |     | within a | 1901.11504. |          |     |       |           |      |        |
| --------- | --------- | ------- | -------- | ------------- | --- | -------- | ----------- | -------- | --- | ----- | --------- | ---- | ------ |
| sentence. | We        | present | two      | complementary |     | mea-     |             |          |     |       |           |      |        |
|           |           |         |          |               |     |          | Christopher | Manning, |     | Mihai | Surdeanu, | John | Bauer, |
surements: scalar mixing weights, learned from a JennyFinkel,StevenBethard,andDavidMcClosky.

2014. TheStanfordCoreNLPnaturallanguagepro- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
cessing toolkit. In Proceedings of ACL: System Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz
Demonstrations. Kaiser, and Illia Polosukhin. 2017. Attention is all
|         |        |         |         |       |          |      | youneed. InProceedingsofNIPS. |     |     |
| ------- | ------ | ------- | ------- | ----- | -------- | ---- | ----------------------------- | --- | --- |
| Rebecca | Marvin | and Tal | Linzen. | 2018. | Targeted | syn- |                               |     |     |
tactic evaluation of language models. In Proceed- Ralph Weischedel, Martha Palmer, Mitchell Marcus,
| ingsofEMNLP. |     |     |     |     |     |     | Eduard Hovy, | Sameer Pradhan, | Lance Ramshaw, |
| ------------ | --- | --- | --- | --- | --- | --- | ------------ | --------------- | -------------- |
NianwenXue,AnnTaylor,JeffKaufman,Michelle
TomasMikolov,IlyaSutskever,KaiChen,GregS.Cor- Franchini, et al. 2013. OntoNotes release
rado, and Jeff Dean. 2013. Distributed representa- Linguistic Data Consortium,
5.0 LDC2013T19.
tionsofwordsandphrasesandtheircompositional-
Philadelphia,PA.
ity. InProceedingsofNIPS.
| Matthew            | Peters,               | Mark                           | Neumann, | Mohit      | Iyyer,       | Matt     |     |     |     |
| ------------------ | --------------------- | ------------------------------ | -------- | ---------- | ------------ | -------- | --- | --- | --- |
| Gardner,           | Christopher           |                                | Clark,   | Kenton     | Lee,         | and Luke |     |     |     |
| Zettlemoyer.2018a. |                       | Deepcontextualizedwordrep-     |          |            |              |          |     |     |     |
| resentations.      | InProceedingsofNAACL. |                                |          |            |              |          |     |     |     |
| Matthew            | Peters,               | Mark                           | Neumann, | Luke       | Zettlemoyer, |          |     |     |     |
| and Wen-tau        |                       | Yih. 2018b.                    |          | Dissecting | contextual   |          |     |     |     |
| wordembeddings:    |                       | Architectureandrepresentation. |          |            |              |          |     |     |     |
InProceedingsofEMNLP.
| Adam Poliak, | Aparajita        |                | Haldar,   | Rachel   |             | Rudinger, |     |     |     |
| ------------ | ---------------- | -------------- | --------- | -------- | ----------- | --------- | --- | --- | --- |
| J. Edward    | Hu,              | Ellie Pavlick, |           | Aaron    | Steven      | White,    |     |     |     |
| and Benjamin |                  | Van Durme.     |           | 2018.    | Collecting  | di-       |     |     |     |
| verse        | natural language |                | inference | problems |             | for sen-  |     |     |     |
|              |                  |                |           |          | Proceedings | of        |     |     |     |
| tence        | representation   | evaluation.    |           | In       |             |           |     |     |     |
EMNLP.
| Alec Radford, | Karthik       |     | Narasimhan,   |     | Tim           | Salimans, |     |     |     |
| ------------- | ------------- | --- | ------------- | --- | ------------- | --------- | --- | --- | --- |
| and Ilya      | Sutskever.    |     | 2018.         |     | Improving     | lan-      |     |     |     |
| guage         | understanding |     | by generative |     | pre-training. |           |     |     |     |
https://blog.openai.com/language-unsupervised.
| AlecRadford, | JeffreyWu, |                  | RewonChild,     |           | DavidLuan, |           |     |     |     |
| ------------ | ---------- | ---------------- | --------------- | --------- | ---------- | --------- | --- | --- | --- |
| Dario        | Amodei,    | and              | Ilya Sutskever. |           | 2019.      | Lan-      |     |     |     |
| guage        | models     | are unsupervised |                 | multitask |            | learners. |     |     |     |
https://blog.openai.com/better-language-models.
| Drew Reisinger, |         | Rachel   | Rudinger,    |     | Francis      | Ferraro, |     |     |     |
| --------------- | ------- | -------- | ------------ | --- | ------------ | -------- | --- | --- | --- |
| Craig           | Harman, | Kyle     | Rawlins,     | and | Benjamin     | Van      |     |     |     |
| Durme.          | 2015.   | Semantic | proto-roles. |     | Transactions |          |     |     |     |
oftheAssociationofComputationalLinguistics.
| Xing Shi,                              | Inkit Padhi, | and | Kevin | Knight. | 2016. | Does   |     |     |     |
| -------------------------------------- | ------------ | --- | ----- | ------- | ----- | ------ | --- | --- | --- |
| string-basedneuralMTlearnsourcesyntax? |              |     |       |         |       | InPro- |     |     |     |
ceedingsofEMNLP.
| Natalia       | Silveira, | Timothy     | Dozat,        |             | Marie-Catherine |         |     |     |     |
| ------------- | --------- | ----------- | ------------- | ----------- | --------------- | ------- | --- | --- | --- |
| de Marneffe,  |           | Samuel      | Bowman,       |             | Miriam          | Connor, |     |     |     |
| John Bauer,   | and       | Christopher |               | D. Manning. |                 | 2014. A |     |     |     |
| gold standard |           | dependency  | corpus        |             | for English.    | In      |     |     |     |
| Proceedings   | of        | the Ninth   | International |             | Conference      |         |     |     |     |
onLanguageResourcesandEvaluation.
| Adam Teichert, | Adam                 | Poliak,  |        | Benjamin | Van     | Durme,     |     |     |     |
| -------------- | -------------------- | -------- | ------ | -------- | ------- | ---------- | --- | --- | --- |
| and Matthew    |                      | Gormley. | 2017.  | Semantic |         | proto-role |     |     |     |
| labeling.      | InProceedingsofAAAI. |          |        |          |         |            |     |     |     |
| Ian Tenney,    | Patrick              | Xia,     | Berlin | Chen,    | Alex    | Wang,      |     |     |     |
| Adam           | Poliak,              | R Thomas | McCoy, |          | Najoung | Kim,       |     |     |     |
BenjaminVanDurme,SamBowman,DipanjanDas,
| and Ellie | Pavlick.                               | 2019. | What | do               | you learn | from |     |     |     |
| --------- | -------------------------------------- | ----- | ---- | ---------------- | --------- | ---- | --- | --- | --- |
| context?  | probingforsentencestructureincontextu- |       |      |                  |           |      |     |     |     |
| alized    | word representations.                  |       |      | In International |           | Con- |     |     |     |
ferenceonLearningRepresentations.

A Appendix
A.1 ComparisonofEncoders
WereproduceFigure1andFigure2(whichdepict
| metrics | on BERT-large) | from | the main | paper be- |     |     |     |     |
| ------- | -------------- | ---- | -------- | --------- | --- | --- | --- | --- |
low, andshowanalogousplotsfortheBERT-base
models. Weobservethatthemostimportantlayers
foragiventaskappearinroughlythesamerelative
| position        | on both the | 24-layer BERT-large |            | and 12-   |     |     |     |     |
| --------------- | ----------- | ------------------- | ---------- | --------- | --- | --- | --- | --- |
| layer BERT-base | models,     | and                 | that tasks | generally |     |     |     |     |
appearinthesameorder.
Additionally,inFigureA.1weshowscalarmix-
| ing weights | for the ELMo | encoder | (Peters | et al., |     |     |     |     |
| ----------- | ------------ | ------- | ------- | ------- | --- | --- | --- | --- |
2018a),whichconsistsoftwoLSTMlayersovera
per-wordcharacterCNN.Weobservethatthefirst
| LSTM | layer (layer 1) | is most | informative | for all |     |     |     |     |
| ---- | --------------- | ------- | ----------- | ------- | --- | --- | --- | --- |
tasks,whichcorroboratestheobservationsofFig-
| ure 2 of   | Peters et al.    | (2018a). | As with | BERT, we |     |     |     |     |
| ---------- | ---------------- | -------- | ------- | -------- | --- | --- | --- | --- |
| observe    | that the weights | are only | weakly  | concen-  |     |     |     |     |
| trated for | the relations    | and SPR  | tasks.  | However, |     |     |     |     |
unlikeBERT,weseeonlyaweakconcentrationin
| the weights | on the coreference |     | task, which | agrees |     |     |     |     |
| ----------- | ------------------ | --- | ----------- | ------ | --- | --- | --- | --- |
withthefindingofTenneyetal.(2019)thatELMo
presentsonlyweakfeaturesforcoreference.
A.2 AdditionalExamples
| We provide | additional          | examples   | in  | the style of |     |     |     |     |
| ---------- | ------------------- | ---------- | --- | ------------ | --- | --- | --- | --- |
| Figure     | 3, which illustrate | sequential |     | decisions in |     |     |     |     |
thelayersoftheBERT-basemodel.
|     |     |     |     |     | Figure A.1: | Scalar mixing | weights for | the ELMo en- |
| --- | --- | --- | --- | --- | ----------- | ------------- | ----------- | ------------ |
coder. Layer0isthecharacterCNNthatproducesper-
wordrepresentations,andlayers1and2aretheLSTM
layers.

(a)BERT-base (b)BERT-large
Figure A.2: Summary statistics on BERT-base (left) and BERT-large (right). Columns on left show F1 dev-set
scoresforthebaseline(P(0))andfull-model(P(L))probes. Dark(blue)arethemixingweightcenterofgravity;
τ τ
light(purple)aretheexpectedlayerfromthecumulativescores.
(a)BERT-base (b)BERT-large
FigureA.3: Layer-wisemetricsonBERT-base(left)andBERT-large(right). Solid(blue)aremixingweightss((cid:96));
τ
outlined(purple)aredifferentialscores∆((cid:96)),normalizedforeachtask. Horizontalaxisisencoderlayer.
τ

| FigureA.4:                          | Traceofselectedannotationsthatintersect |             |            |     |     |     |     |
| ----------------------------------- | --------------------------------------- | ----------- | ---------- | --- | --- | --- | --- |
| thetoken“basque”intheabovesentence. |                                         |             | Weseethe   |     |     |     |     |
| model recognize                     | this as part                            | of a proper | noun (NNP) |     |     |     |     |
inlayer2,whichleadsittoreviseitshypothesisabout
| the constituent | “petro basque” | from an ordinary | noun |             |                   |             |             |
| --------------- | -------------- | ---------------- | ---- | ----------- | ----------------- | ----------- | ----------- |
|                 |                |                  |      | Figure A.6: | Trace of selected | coreference | annotations |
phrase(NP)toanominalmention(NML)inlayers3-4.
|     |     |     |     | ontheabovesentence. | Notshownaretwocoreference |     |     |
| --- | --- | --- | --- | ------------------- | ------------------------- | --- | --- |
Wealsoseethatfromlayer3onwards,themodelrec-
ognizes“petrobasque”aseitheranorganization(ORG) edges that the model has correctly resolved at layer
|               |                    |         |              | 0 (guessing | from embeddings | alone): | “him” and “the |
| ------------- | ------------------ | ------- | ------------ | ----------- | --------------- | ------- | -------------- |
| or a national | or religious group | (NORP), | but does not |             |                 |         |                |
stronglydisambiguatebetweenthetwo. hurtman”arecoreferent,asare“he”and“he”. Wesee
thattheremainingedges,betweennon-coreferentmen-
tions,areresolvedinseveralstages.
|            |                                         |     |     | FigureA.7: | TraceofselectedcoreferenceandSRLan- |     |     |
| ---------- | --------------------------------------- | --- | --- | ---------- | ----------------------------------- | --- | --- |
| FigureA.5: | Traceofselectedannotationsthatintersect |     |     |            |                                     |     |     |
thesecond“today”intheabovesentence.Theodelini- notations on the above sentence. The model resolves
thesemanticrole(purpose,ARGM-PRP)ofthephrase
tiallybelievesthistobeadateandacommonnoun,but
|     |     |     |     | “to help | him” in layers | 5-7, then quickly | resolves at |
| --- | --- | --- | --- | -------- | -------------- | ----------------- | ----------- |
bylayer4realizesthatthisistheTVshow(entitytag
WORK OF ART) and subsequently revises its hypothe- layer 8 that “him” and “he” (the agent of “stop”) are
|     |     |     |     | not coreferent. | Also shown | is the correct | prediction |
| --- | --- | --- | --- | --------------- | ---------- | -------------- | ---------- |
sesabouttheconstituenttypeandpart-of-speech.
that“him”istherecipient(ARG1,patient)of“help”.