HMT: Hierarchical Memory Transformer for Efficient Long Context
|     |     |     |     |     |     | Language |     | Processing |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
ZifanHe1,YingqiCao2,ZongyueQin1,NehaPrakriya1,
YizhouSun1,andJasonCong1
1 UniversityofCalifornia,LosAngeles,2 UniversityofCalifornia,SanDiego
|                                         |                   |          |               | zifanhe1202@g.ucla.edu, |              |               |     | yic033@ucsd.edu,                            |                   |        |               |            |             |       |
| --------------------------------------- | ----------------- | -------- | ------------- | ----------------------- | ------------ | ------------- | --- | ------------------------------------------- | ----------------- | ------ | ------------- | ---------- | ----------- | ----- |
|                                         |                   |          | {qinzongyue,  |                         |              | nehaprakriya, |     | yzsun,                                      | cong}@cs.ucla.edu |        |               |            |             |       |
|                                         |                   |          | Abstract      |                         |              |               |     | self-attentionandafeedforwardnetworkmodule. |                   |        |               |            |             |       |
|                                         |                   |          |               |                         |              |               |     | An optimized                                | self-attention    |        |               | layer has  | a quadratic |       |
|                                         | Transformer-based |          |               | large                   | language     | models        |     |                                             |                   |        |               |            |             |       |
|                                         |                   |          |               |                         |              |               |     | computational                               | and               | linear | space         | complexity |             | (Dao  |
|                                         | (LLM)             | have     | been widely   |                         | used         | in language   |     |                                             |                   |        |               |            |             |       |
|                                         |                   |          |               |                         |              |               |     | et al., 2022)                               | regarding         |        | the sequence  |            | length      | since |
| 5202 beF 6  ]LC.sc[  3v76060.5042:viXra | processing        |          | applications. |                         | However,     | due           | to  |                                             |                   |        |               |            |             |       |
|                                         |                   |          |               |                         |              |               |     | it computes                                 | interactions      |        | between       | each       | token       | and   |
|                                         | the               | memory   | constraints   | of                      | the devices, | most          |     |                                             |                   |        |               |            |             |       |
|                                         |                   |          |               |                         |              |               |     | all previous                                | tokens            | in     | the sequence. |            | To maintain |       |
|                                         | of them           | restrict | the           | context                 | window.      | Even          |     |                                             |                   |        |               |            |             |       |
though recurrent models in previous works the inference speed and satisfy memory require-
ments,mosttransformermodelsenforcemaximum
canmemorizepasttokenstoenableunlimited
contextandmaintaineffectiveness,theyhave sequencelength. Forexample,theLlama3model
“flat”memoryarchitectures. Sucharchitectures is designed to process 8192 tokens (Dubey et al.,
|     | have | limitations | in selecting |     | and | filtering | in- |     |     |     |     |     |     |     |
| --- | ---- | ----------- | ------------ | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
2024)andtheLlama2canprocessupto4096to-
|     | formation. |                      | Since humans |     | are good | at learn- |      |                          |           |     |      |                    |     |         |
| --- | ---------- | -------------------- | ------------ | --- | -------- | --------- | ---- | ------------------------ | --------- | --- | ---- | ------------------ | --- | ------- |
|     |            |                      |              |     |          |           |      | kens(Touvronetal.,2023). |           |     |      | However,real-world |     |         |
|     | ing        | and self-adjustment, |              | we  | believe  | that      | imi- |                          |           |     |      |                    |     |         |
|     |            |                      |              |     |          |           |      | applications             | involving |     | long | documents,         |     | such as |
tatingbrainmemoryhierarchyisbeneficialfor
model memorization. Thus, we propose the booksummarization(Raeetal.,2019)andlifelong
|     |     |     |     |     |     |     |     | question-answering |     | tasks | (Sun | et  | al., 2019; | Dai |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | ----- | ---- | --- | ---------- | --- |
HierarchicalMemoryTransformer(HMT)1,a
novelframeworkthatfacilitatesamodel’slong- etal.,2022),canhaveanenormousoreveninfinite
|     | contextprocessingabilitybyimitatinghuman |     |     |                   |     |     |     | streamofinputs. |          |          |     |          |      |      |
| --- | ---------------------------------------- | --- | --- | ----------------- | --- | --- | --- | --------------- | -------- | -------- | --- | -------- | ---- | ---- |
|     | memorizationbehavior.                    |     |     | Leveragingmemory- |     |     |     |                 |          |          |     |          |      |      |
|     |                                          |     |     |                   |     |     |     | Existing        | research | attempts |     | to build | long | con- |
augmentedsegment-levelrecurrence,weorga-
|     |      |            |           |     |               |     |     | text transformers |     | using | sparse | attention |     | (Beltagy |
| --- | ---- | ---------- | --------- | --- | ------------- | --- | --- | ----------------- | --- | ----- | ------ | --------- | --- | -------- |
|     | nize | the memory | hierarchy |     | by preserving |     | to- |                   |     |       |        |           |     |          |
etal.,2020;Zhangetal.,2021;Kitaevetal.,2020),
kensfromearlyinputsegments,passingmem-
retrieval-augmentedmodels(Bertschetal.,2023;
oryembeddingsalongthesequence,andrecall-
|     |     |          |             |      |          |       |     | Wu et al., | 2022), | and | recurrent | sequence |     | models |
| --- | --- | -------- | ----------- | ---- | -------- | ----- | --- | ---------- | ------ | --- | --------- | -------- | --- | ------ |
|     | ing | relevant | information | from | history. | Eval- |     |            |        |     |           |          |     |        |
uating general language modeling, question- (Pengetal.,2023a;GuandDao,2023;Raeetal.,
answeringtasks,andthesummarizationtask, 2019). Still,thesemodelsfaceatleastoneoftwo
weshowthatHMTconsistentlyimprovesthe issues: (1)difficultyinadaptingtofuturemodels
long-contextprocessingabilityofexistingmod- duetoachangeinthecoremodelarchitectureand
|     | els.    | Furthermore, | HMT        |         | achieves | a compa- |     |                           |     |     |            |             |        |        |
| --- | ------- | ------------ | ---------- | ------- | -------- | -------- | --- | ------------------------- | --- | --- | ---------- | ----------- | ------ | ------ |
|     |         |              |            |         |          |          |     | (2) low effectiveness     |     | for | long-range |             | inputs | under  |
|     | rable   | or superior  | generation |         | quality  | to long- |     |                           |     |     |            |             |        |        |
|     |         |              |            |         |          |          |     | frequentcontextswitching. |     |     |            | Inthiswork, |        | wepro- |
|     | context | LLMs         | with       | 2 ∼ 57× | fewer    | parame-  |     |                           |     |     |            |             |        |        |
posetheHierarchicalMemoryTransformer(HMT),
|     | ters | and 2.5 | ∼ 116× | less | inference | memory, |     |     |     |     |     |     |     |     |
| --- | ---- | ------- | ------ | ---- | --------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
significantlyoutperformingpreviousmemory- anovelframeworktoenableandaugmentmodels’
augmentedmodels. long-contextprocessingability. HMTtransforms
modelsintoamemory-augmentedrecurrentmodel
|     | 1 Introduction |     |          |         |       |     |        | thatimitatesthebrain’smemoryhierarchyandhu- |     |     |     |                   |     |     |
| --- | -------------- | --- | -------- | ------- | ----- | --- | ------ | ------------------------------------------- | --- | --- | --- | ----------------- | --- | --- |
|     |                |     |          |         |       |     |        | manmemorizationbehavior.                    |     |     |     | Ithasthefollowing |     |     |
|     | Transformer    |     | (Vaswani | et al., | 2017) | has | demon- |                                             |     |     |     |                   |     |     |
uniquefeatures:
|     | strated  | its strength | in           | contextual |     | learning | and is |                           |     |     |     |              |     |     |
| --- | -------- | ------------ | ------------ | ---------- | --- | -------- | ------ | ------------------------- | --- | --- | --- | ------------ | --- | --- |
|     |          |              |              |            |     |          |        | HierarchicalMemorization: |     |     |     | HMTmimicsthe |     |     |
|     | utilized | in various   | applications |            | in  | language | pro-   |                           |     |     |     |              |     |     |
memoryhierarchyofthebrain(Burgin,2011)em-
|     | cessing                  | (Dong  | et al., 2019)    |                        | and computer |          | vision |               |              |        |            |        |      |         |
| --- | ------------------------ | ------ | ---------------- | ---------------------- | ------------ | -------- | ------ | ------------- | ------------ | ------ | ---------- | ------ | ---- | ------- |
|     |                          |        |                  |                        |              |          |        | ploying       | both learned | memory |            | tokens | and  | current |
|     | (Dosovitskiyetal.,2020). |        |                  | Foradecoder-onlytrans- |              |          |        |               |              |        |            |        |      |         |
|     |                          |        |                  |                        |              |          |        | input tokens. | HMT          |        | stratifies | memory | into | sen-    |
|     | former                   | model, | each transformer |                        | block        | contains | a      |               |              |        |            |        |      |         |
sory,short-term,andlong-term,withinteractions
|     | 1https://github.com/OswaldHe/HMT-pytorch |     |     |     |     |     |     | betweeneachother. |     |     |     |     |     |     |
| --- | ---------------------------------------- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- |

2 RelatedWorksandProblem
| MemoryRetrievalMechanism: |           |         |          | HMTimitates |            |             |               |     |          |         |     |       |
| ------------------------- | --------- | ------- | -------- | ----------- | ---------- | ----------- | ------------- | --- | -------- | ------- | --- | ----- |
| memory                    | recall by | storing | encoded  |             | memory em- | Formulation |               |     |          |         |     |       |
| beddings                  | generated | from    | previous | iterations  | and        |             |               |     |          |         |     |       |
|                           |           |         |          |             |            | We will     | first discuss | the | existing | efforts | on  | long- |
searchingbasedontherelevancetocurrenttoken
| segments. |     |     |     |     |     | range transformers |     | and | recurrent | sequence |     | mod- |
| --------- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --------- | -------- | --- | ---- |
elsforinfinitelylongcontextlanguageprocessing.
OnekeyadvantageofutilizingHMToverother
Then,wehighlightaproblemthatiscrucialinreal-
memory-augmentmodelsisthatHMTisamodel-
worldapplications.
| independent | plug-and-play |     |     | framework: | future |     |     |     |     |     |     |     |
| ----------- | ------------- | --- | --- | ---------- | ------ | --- | --- | --- | --- | --- | --- | --- |
decoder-onlymodelscandirectlyserveastheback-
2.1 LongContextTransformers
bonemodelofHMTtoaugmenttheirlongcontext
|     |     |     |     |     |     | Since one | of the | bottlenecks |     | of transformers |     | is  |
| --- | --- | --- | --- | --- | --- | --------- | ------ | ----------- | --- | --------------- | --- | --- |
processingabilitywithoutextraimplementationef-
forts. Withjointtrainingandfine-tuningofnewly the quadratic computational complexity of self-
introduced and original parameters of the back- attention, a natural approach is sparsifying atten-
|             |     |               |     |     |              | tion computation. |             | A naive | sparse    | attention |           | pat- |
| ----------- | --- | ------------- | --- | --- | ------------ | ----------------- | ----------- | ------- | --------- | --------- | --------- | ---- |
| bone model, | HMT | is applicable |     | to  | a wide range |                   |             |         |           |           |           |      |
|             |     |               |     |     |              | tern is           | the sliding | window  | attention |           | (Kovaleva |      |
ofLLMs,includingtransformer-basedmodelsand
state-spacemodels. Ourcontributionsinclude: etal.,2019),whereeachtokenattendstoneighbors
|     |     |     |     |     |     | withinalocalwindow. |     | However,thisneglectslong- |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | ------------------------- | --- | --- | --- | --- |
• HMT consistently improves models’ gener- rangeinteractionbetweenwords. Existingworks
ation quality with long context for various suchasLongformer(Beltagyetal.,2020)andPool-
| model | architectures. |     | We demonstrate |     | HMT on |     |     |     |     |     |     |     |
| ----- | -------------- | --- | -------------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
ingformer(Zhangetal.,2021)extendthesliding
bothtransformer-basedarchitectureandstate-space window attention by adding global attending to-
models. EvaluatingonWikitext-103,PG-19(Rae kens and applying pooling to expand the recep-
| et al., | 2019), and | PubMedQA |     | (Jin | et al., 2019) |                |                                 |     |     |     |     |     |
| ------- | ---------- | -------- | --- | ---- | ------------- | -------------- | ------------------------------- | --- | --- | --- | --- | --- |
|         |            |          |     |      |               | tivefieldarea. | Unlimiformer(Bertschetal.,2023) |     |     |     |     |     |
datasetswithmultiplecontextsconcatenated,HMT
adoptstheretrieval-augmentedgenerativemethod
can improve the effectiveness by up to 25.5% in bysearchingthetopKmostimportanttokensfor
perplexity and 1.0% higher prediction accuracy the incoming sequence. It then applies attention
overthebaselinemodels.
|       |            |          |     |        |          | to just those                      | tokens       | in  | the decoders, |     | resulting | in  |
| ----- | ---------- | -------- | --- | ------ | -------- | ---------------------------------- | ------------ | --- | ------------- | --- | --------- | --- |
|       |            |          |     |        |          | prunedcomputationswithminorlosses. |              |     |               |     | Neverthe- |     |
| • HMT | with small | backbone |     | models | can out- |                                    |              |     |               |     |           |     |
|       |            |          |     |        |          | less, the                          | contribution | of  | less relevant |     | tokens    | may |
performlargemodelstrainedonlongercontext
|                                        |          |        |     |        |                | accumulate        | over | time                       | and impact | the | overall | se- |
| -------------------------------------- | -------- | ------ | --- | ------ | -------------- | ----------------- | ---- | -------------------------- | ---------- | --- | ------- | --- |
| samples,implyingahighmemoryefficiency. |          |        |     |        | We             |                   |      |                            |            |     |         |     |
|                                        |          |        |     |        |                | quencegeneration. |      | Althoughthesemethodsextend |            |     |         |     |
| evaluate                               | HMT with | SmolLM |     | (Allal | et al., 2024), |                   |      |                            |            |     |         |     |
theattainablecontextlength,theycannotprevent
| OPT (Zhang | et  | al., 2022), |     | and OpenLlamaV2 |     |     |     |     |     |     |     |     |
| ---------- | --- | ----------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
increasingmemoryconsumptionastheinputlength
| (Geng                      | and Liu, | 2023) models |     | on the       | LongBench |            |                                     |     |     |     |     |     |
| -------------------------- | -------- | ------------ | --- | ------------ | --------- | ---------- | ----------------------------------- | --- | --- | --- | --- | --- |
|                            |          |              |     |              |           | increases. | Alternatively,compressingpasttokens |     |     |     |     |     |
| (Baietal.,2023b)benchmark. |          |              |     | Insum,HMTcan |           |            |                                     |     |     |     |     |     |
usingarecurrentsequencemodelcanpotentially
achievecomparableorhighermetricresultswith
|                              |     |     |     |     |           | reduce memory |     | consumption |     | by condensing |     | the |
| ---------------------------- | --- | --- | --- | --- | --------- | ------------- | --- | ----------- | --- | ------------- | --- | --- |
| 2 ∼ 57×fewerparametersand2.5 |     |     |     | ∼   | 116×lower |               |     |             |     |               |     |     |
informationintoafixed-sizeembedding.
inferencememoryrequirementthanlong-context
largelanguagemodels.
2.2 RecurrentSequenceModels
• HMTsurpassespreviousmethodsspecialized RecurrentNeuralNetworks(RNN)havebeenex-
for efficient long-context processing by com- tensivelyexploredinsequenceprocessingresearch,
pressingcontexts. WecompareHMTwithRMT including Long Short-term Memory (Hochreiter
(Bulatov et al., 2022), LongMem (Wang et al., andSchmidhuber,1997)andGatedRecurrentUnit
2024),MemorizingTransformer(Wuetal.,2022), (Chungetal.,2014). TheyrevealthatRNNsper-
CCM (Kim et al., 2023), and HOMER (Song formwellinmemorizingpastinformationandare
et al., 2024), which are recent SoTA of memory- hardware-friendlyforimplementingcustomizedac-
augmented and hierarchical methods. With the celerators (Chang et al., 2015). However, RNNs
sameorsimilarsizebackbonemodel,HMThasa havelimitedadvantagesinlearningcontextualre-
bettergenerationqualityinbothgenerallanguage lationships between words compared with self-
modelingandQAtasks. Furthermore,HMThasa attentioninlanguageprocessing(Bahdanauetal.,
lowermemorycomplexity,indicatingbetterscala- 2014). One approach to alleviate this issue is
bilityastheinputlengthincreases. the coarse-grain recurrence, in which the model

|     |     |     |     |     |     | Table1: | NotationusedtoillustrateHMT’sarchitecture |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | ----------------------------------------- | --- | --- | --- |
splitsinputsintosegments,performsattentionin-
sideeachsegment,andpropagatesstates(i.e.,com- inSection3andFigure1.
pressedinformationasembeddings)betweenseg-
| ments. TheCompressiveTransformer(Raeetal., |     |     |     |     |     | NOTATION |     |     | MEANING |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | -------- | --- | --- | ------- | --- |
2019)furtherstoresandcompressespreviousstates Hn HIDDENEMBEDDINGSOFTHEnthSEGMENT
|     |     |     |     |     |     | L   |     |     | SEGMENTLENGTH |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- |
to enhance memorization. The Recurrent Mem- Hn[L−k,L) LASTkEMBEDDINGSOFHn
|     |     |     |     |     |     | Hn[0,j) |     | FIRSTjEMBEDDINGSOFHn |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | -------------------- | --- | --- |
oryTransformer(RMT)(Bulatovetal.,2022)uti- BBM(·) BACKBONEMODEL
|     |     |     |     |     |     | Pn  |     | MEMORIZATIONPROMPTEMBEDDING |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- |
lizesamemorytokentosummarizeandpropagate Hn out HIDDENEMBEDDINGFORLOGITSGENERATION
|     |     |     |     |     |     | M   |     |     |     | n t h |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
segmentinformationwithoutmodifyingthetrans- n M E M O R Y E M B E D D IN G O F T H E S E G M E N T
|                          |     |                       |     |     |     | N          |                                     | N U M B E R O          | F C A C H E D M E | M O R Y E M B E D D I N G S |
| ------------------------ | --- | --------------------- | --- | --- | --- | ---------- | ----------------------------------- | ---------------------- | ----------------- | --------------------------- |
|                          |     |                       |     |     |     | M[n−N+1,n) |                                     | CACHEDMEMORYEMBEDDINGS |                   |                             |
| formerblockarchitecture. |     | Theoretically,theycan |     |     |     |            |                                     |                        |                   |                             |
|                          |     |                       |     |     |     | T          | SEGMENTSUMMARIZATIONPROMPTEMBEDDING |                        |                   |                             |
|                          |     |                       |     |     |     | Sn         | SUMMARYEMBEDDINGOFTHEnthSEGMENT     |                        |                   |                             |
processunlimitedlongsequences,butpreviousin-
formationwillbedilutedaftermultiplesummariza-
tions and generation quality can drop when less speed,longdocumentscannotbereadasawhole
relevantinformationoccupiesthememory. Recent by the computing hardware (Agerri et al., 2015).
works (Chevalier et al., 2023; Kim et al., 2023) Furthermore,userswhoareconstantlyinteracting
| aim to further | optimize | RMT | to improve |     | genera- |     |     |     |     |     |
| -------------- | -------- | --- | ---------- | --- | ------- | --- | --- | --- | --- | --- |
withthelanguagemodelcanrefertotheprevious
tionqualitybyconcatenatingtheresultsofsumma- topicorswitchtoanothertopicthathashighrele-
rizations,butthissacrificestheinferencememory vancetopastinformation. Foreffectiveness,most
efficiency.
recurrentmodelsneedtoencodeallpreviousinputs
AnotherapproachaugmentsRNNbyinvolving inthestates,whichcancontainirrelevantinforma-
interactionsbetweenthecurrentinputsandthepre- tionanddegradethemodel’squality.
| vious states | to learn | contextual | relationships |     | in a |     |     |     |     |     |
| ------------ | -------- | ---------- | ------------- | --- | ---- | --- | --- | --- | --- | --- |
similar way as self-attention and accelerate the 3 HierarchicalMemoryTransformer
| computation | with linear | convolution. |     | One | of the |     |     |     |     |     |
| ----------- | ----------- | ------------ | --- | --- | ------ | --- | --- | --- | --- | --- |
ThemainideaofHMTistostoreinformationhi-
representatives,RWKV(Pengetal.,2023a),isan
|                              |          |        |                  |     |        | erarchically | and | search | for relevant | information |
| ---------------------------- | -------- | ------ | ---------------- | --- | ------ | ------------ | --- | ------ | ------------ | ----------- |
| RNN model                    | inspired | by the | attention-free   |     | trans- |              |     |        |              |             |
|                              |          |        |                  |     |        | throughout   | the | memory | hierarchy.   | Table 1 de- |
| former(AFT)(Zhaietal.,2021). |          |        | Itincludesatime- |     |        |              |     |        |              |             |
scribesallnotationsweusetoillustratetheHMT
| mixing module | to learn | from | previous | states | and |     |     |     |     |     |
| ------------- | -------- | ---- | -------- | ------ | --- | --- | --- | --- | --- | --- |
architectureinthissection.
achannel-mixingmoduletolearnfromtheprevi-
| ousoutput. | Mamba(GuandDao,2023)isanother |     |                 |     |       |                     |     |     |     |     |
| ---------- | ----------------------------- | --- | --------------- | --- | ----- | ------------------- | --- | --- | --- | --- |
|            |                               |     |                 |     |       | 3.1 OverallWorkflow |     |     |     |     |
| recurrent  | method based                  | on  | the state-space |     | model |                     |     |     |     |     |
Givenabackbonemodeltoenhance,HMTchunks
thatemploysgatedconvolutiontoacceleratemodel
inference. Thesemodelsareenergyandmemory- the input into L-token segments and operates on
|                    |                    |     |                 |             |         | the hidden               | embeddings   |     | of the            | token segments  |
| ------------------ | ------------------ | --- | --------------- | ----------- | ------- | ------------------------ | ------------ | --- | ----------------- | --------------- |
| efficient          | with fast training |     | speed and       | are         | able to |                          |              |     |                   |                 |
|                    |                    |     |                 |             |         | ({H }∞                   | ), generated |     | by the            | token embedding |
| achieve            | high performance   |     | in memorization |             | tasks   | n n=0                    |              |     |                   |                 |
|                    |                    |     |                 |             |         | layerofthebackbonemodel. |              |     | Foreverysegmentn, |                 |
| (e.g., associative | recall),           | but | have            | limitations | on      |                          |              |     |                   |                 |
HMTwalksthroughfourstepsshowninFigure1:
capturingcontextualrelationshipsandfilteringir-
| relevantinformation. |            | Recentworkscombinetrans- |         |       |      |                   |     |          |     |                 |
| -------------------- | ---------- | ------------------------ | ------- | ----- | ---- | ----------------- | --- | -------- | --- | --------------- |
|                      |            |                          |         |       |      | 1) Representation |     | encoding |     | by the backbone |
| formers              | with Mamba | (Lieber                  | et al., | 2024; | Team |                   |     |          |     |                 |
model,whichencodespartofthesegmentcontain-
etal.,2024)tomitigatethisissue,butthisreintro-
ingtheessenceoftheongoingtopicintoasingle
ducesthescalingissueofthetransformers.
embeddingtorepresentitscontext,denotedbyH n .
| 2.3 ProblemFormulation: |     |     | Adaptive |     |     |     |     |     |     |     |
| ----------------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
Long-contextProcessing 2) Memorysearch,whichutilizesthecurrentcon-
textasaquerytofindrelevantinformationinthe
| We intend | to develop | a model | that | can handle | in- |     |     |     |     |     |
| --------- | ---------- | ------- | ---- | ---------- | --- | --- | --- | --- | --- | --- |
memory.
finitelylongcontextinputswithcontextadaptabil-
ity: Basedonthecontext/topicoftheinputstream,
|     |     |     |     |     |     | 3) Prependingsensorymemory,whichaugments |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- |
themodelcanadaptivelyselectpastrelevantinfor-
thesegmenttocaptureinformationintheprevious
mation to enhance effectiveness, since irrelevant segmentandotherrelevantinformation.
contextcandistractthemodel(Shietal.,2023).
Inreal-worldapplications,restrainedbymemory 4) Decodingandsummarization,whichprocesses
bandwidthandcapacity,aswellasdatageneration theaugmentedsegmenttogethiddenembeddings

Figure1: OverallworkflowofHMT.Forasegment,(1)HMTwillfirstperformrepresentationencoding,utilizing
thesegmentsummarizationpromptembedding(T)tosummarizepartofthesegment. (2)Thegeneratedsegment
summaryembedding(S )isusedwiththecachedmemoryembeddingsformemorysearchwithcrossattention.
n
Theoutputisamemorizationpromptembedding(P
n )whichcontainsinformationrelevanttothecurrentsegment.
(3)Thememorizationpromptembeddingandthelastkembeddingsfromtheprevioussegmentwillaugmentthe
segment. (4)Thebackbonemodel(BBM)willprocesstheaugmentedsegmentandgeneratehiddenembeddingsfor
logits(Hout)andthememoryembedding(M
n ),whichwillbepushedintothelong-termmemory.
n
forgeneratinglogitsandamemoryembeddingthat by soft prompt tuning (Liu et al., 2023). Instead
summarizestheaugmentedsegment. ofextractingfromthetokenembeddingofBBM,
|     |     |        |           | wemakeT | learnabletoallowalargerpromptem- |     |     |     |
| --- | --- | ------ | --------- | ------- | -------------------------------- | --- | --- | --- |
|     |     | memory | retrieval |         |                                  |     |     |     |
The first two steps are the beddingspaceforsummarization. Thebackbone
mechanismdiscussedinSection3.2. Steps3and4 modelwillthenprocesstheaugmentedembeddings
areexplainedinSection3.3alongwiththeconcept and generate a new embedding at the end of the
ofhierarchicalmemorization. outputastherepresentationofthesegment:
3.2 MemoryRetrievalMechanism S n = BBM([T||H n [0,j)||T])[j,j +1) (1)
Tohandlecontextswitchingandpreventtheinter-
nth
|     |     |     |     | where | S n is the summary | embedding | of the |     |
| --- | --- | --- | --- | ----- | ------------------ | --------- | ------ | --- |
ventionofirrelevantcontext,HMTperformsmem-
segmentonly,BBM(·)isthebackbonemodel,and
| ory retrieval | to extract | only relevant | information |                                 |     |     |            |     |
| ------------- | ---------- | ------------- | ----------- | ------------------------------- | --- | --- | ---------- | --- |
|               |            |               |             | “||"istheconcatenationoperator. |     | S   | willbeused |     |
n
| frompastknowledge. | Thememoryretrievalmecha- |     |     |     |     |     |     |     |
| ------------------ | ------------------------ | --- | --- | --- | --- | --- | --- | --- |
formemorysearch.
| nisminvolvesthreesteps: |     | representationextraction, |     |               |     |                        |     |     |
| ----------------------- | --- | ------------------------- | --- | ------------- | --- | ---------------------- | --- | --- |
|                         |     |                           |     | MemorySearch: |     | ShowninStep2ofFigure1, |     |     |
memorysearch,andmemoryaugmentation.
|     |     |     |     | S is | utilized as a | query to find relevant | memory |     |
| --- | --- | --- | --- | ---- | ------------- | ---------------------- | ------ | --- |
n
| RepresentationEncoding: |     | DepictedinStep1 |     |     |     |     |     |     |
| ----------------------- | --- | --------------- | --- | --- | --- | --- | --- | --- |
embeddingsgeneratedfromStep4whenprocess-
| of Figure | 1, HMT selects    | the first j | embeddings |                      |              |                      |     |     |
| --------- | ----------------- | ----------- | ---------- | -------------------- | ------------ | -------------------- | --- | --- |
|           |                   |             |            | ingprevioussegments. |              | Wekeepaslidingwindow |     |     |
| from the  | hidden embeddings | of the nth  | segment,   |                      |              |                      |     |     |
|           |                   |             |            | ofN                  | embeddings(M | )andthencompute:     |     |     |
[n−N+1,n)
| H , to extract | the topic | of the segment. | The em- |     |     |     |     |     |
| -------------- | --------- | --------------- | ------- | --- | --- | --- | --- | --- |
n
beddings are augmented with the segment sum- Q = S W ,K = M W (2)
|                                            |                  |     |               |     | n n | q n [n−N+1,n) | k   |     |
| ------------------------------------------ | ---------------- | --- | ------------- | --- | --- | ------------- | --- | --- |
| marization                                 | prompt embedding | T.  | T is a learn- |     |     |               |     |     |
| ableparameterembedding,deployedtopromptthe |                  |     |               |     |     | Q KT          |     |     |
n n
|                                         |     |     |     |     | P = softmax( | √ )M        |     | (3) |
| --------------------------------------- | --- | --- | --- | --- | ------------ | ----------- | --- | --- |
| backbonemodel(BBM)tosummarizethesegment |     |     |     |     | n            | d [n−N+1,n) |     |     |
h

where d h is the hidden dimension of the cross awarenessoftherelativepositionsofcontexts. As
attention. The computation is similar to cross- depictedinStep4ofFigure1,wetrainHMTsuch
| attention | without | value | and | output |     | projection. | that |     |     |     |     |     |
| --------- | ------- | ----- | --- | ------ | --- | ----------- | ---- | --- | --- | --- | --- | --- |
T
| Softmax(     | Q √nK | n ) calculates |     | the normalized |      | simi- |     |         |     |            |     |           |
| ------------ | ----- | -------------- | --- | -------------- | ---- | ----- | --- | ------- | --- | ---------- | --- | --------- |
|              | d h   |                |     |                |      |       | H   | = BBM(P | ||H | [L−k,L)||H |     | ||P ) (4) |
| larity score | and   | applies        | it  | directly       | to M |       |     |         | n   | n−1        |     | n n       |
[n−N+1,n)
toensuresimilardistributionsofoutputvalueand
Hout||M
|                  |       |     |                           |      |                 |     |        |                                  | n = | H[k+1,L+k+2) |     | (5) |
| ---------------- | ----- | --- | ------------------------- | ---- | --------------- | --- | ------ | -------------------------------- | --- | ------------ | --- | --- |
| oldmemorytokens. |       |     | Weexpectthattheprojection |      |                 |     |        | n                                |     |              |     |     |
| W and            | W can | be  | trained                   | such | that summariza- |     |        |                                  |     |              |     |     |
| q                | k     |     |                           |      |                 |     | whereM | isthememoryembeddingofthenthseg- |     |              |     |     |
n
tionscontainingsimilarcontextshavehighatten- HoutisacollectionofLhiddenembeddings
ment.
n
| tionscoresafterprojections. |     |     |     |     |     |     | thatwillbeusedtogeneratelogits. |     |     |     |     |     |
| --------------------------- | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | --- |
Theoutputofamemorysearchisamemoriza- Long-termMemory: Eachgeneratedmemory
| tionpromptembeddingP |     |     |          | containinginforma- |     |     |                                            |     |     |     |     |     |
| -------------------- | --- | --- | -------- | ------------------ | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- |
|                      |     |     |          | n                  |     |     | embeddingwillbecachedasthelong-termmemory. |     |     |     |     |     |
| tionrelevanttothenth |     |     | segment. | Itwillbeapplied    |     |     |                                            |     |     |     |     |     |
Thecachedembeddingswillbeutilizedastheinput
nth
to augment the segment. Notice that HMT’s of the memory retrieval mechanism to generate
| memoryisaccumulative: |     |     | thenth |     | memoryembed- |     |                  |     |       |           |     |          |
| --------------------- | --- | --- | ------ | --- | ------------ | --- | ---------------- | --- | ----- | --------- | --- | -------- |
|                       |     |     |        |     |              |     | the memorization |     | token | embedding | P   | for each |
n
| ding contains |     | information |     | of all | previous | n − 1 |     |     |     |     |     |     |
| ------------- | --- | ----------- | --- | ------ | -------- | ----- | --- | --- | --- | --- | --- | --- |
segmentasillustratedintheprevioussections.
| segments,       | with | a higher                   | loss     | of     | information | for    |              |     |     |                |     |          |
| --------------- | ---- | -------------------------- | -------- | ------ | ----------- | ------ | ------------ | --- | --- | -------------- | --- | -------- |
| oldersegments.  |      | Wehopethatretrievingmemory |          |        |             |        | 4 Experiment |     |     |                |     |          |
| will strengthen |      | the                        | relevant | memory | and         | reduce |              |     |     |                |     |          |
|                 |      |                            |          |        |             |        | We benchmark |     | HMT | with a variety | of  | backbone |
thisloss.
|     |     |     |     |     |     |     | models | including | SmolLM | 135M | (Allal | et al., |
| --- | --- | --- | --- | --- | --- | --- | ------ | --------- | ------ | ---- | ------ | ------- |
Inpractice,representationencodingisexecuted
2024),OPT350M,OPT2.7B(Zhangetal.,2022),
inparallelwiththemodelinferenceonGPUssince
OpenLlamaV23B(GengandLiu,2023),RWKV
| they are | independent |     | tasks. | Memory | search | has |     |     |     |     |     |     |
| -------- | ----------- | --- | ------ | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
3B(Pengetal.,2023a),andLlama27B(Touvron
timecomplexityO(N),andcanalsoruninparallel
etal.,2023),underthesamememoryconstraint(i.e.
| withthesegmentinferencewhenN |     |     |     |     | issmall(e.g., |     |      |         |         |          |           |     |
| ---------------------------- | --- | --- | --- | --- | ------------- | --- | ---- | ------- | ------- | -------- | --------- | --- |
|                              |     |     |     |     |               |     | same | maximum | context | window). | Moreover, | we  |
N = 300).
Thus,theoverallruntimeoverheadof
testseveralmodelstargetinglongcontexts(Mamba
HMTisnegligible.
|     |     |     |     |     |     |     | 370M    | (Gu    | and Dao,    | 2023), Yi-6B-200K |     | (Young      |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------ | ----------- | ----------------- | --- | ----------- |
|     |     |     |     |     |     |     | et al., | 2024), | and Mistral | 7B (Jiang         | et  | al., 2023)) |
3.3 HierarchicalMemorization
|                 |        |         |            |             |         |            | to demonstrate |     | the              | benefit HMT  | has   | on genera- |
| --------------- | ------ | ------- | ---------- | ----------- | ------- | ---------- | -------------- | --- | ---------------- | ------------ | ----- | ---------- |
| Human           | memory | can     | be         | categorized |         | into three |                |     |                  |              |       |            |
|                 |        |         |            |             |         |            | tion quality   |     | and memory       | consumption. |       | We eval-   |
| strata: sensory |        | memory, | short-term |             | memory, | and        |                |     |                  |              |       |            |
|                 |        |         |            |             |         |            | uate HMT       |     | with state-space | models       | (RWKV | and        |
long-termmemory(Burgin,2011). Sensorymem- Mamba)asbackbonessincewebelievethatmod-
ory refers to very short-term memory generated elswhichcanalreadyprocessinfinitelylonginputs
fromsensoryinformation,suchasvisionandhear-
|     |     |     |     |     |     |     | would | benefit | even | further from | HMT. | All mod- |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------- | ---- | ------------ | ---- | -------- |
ing. Short-term and long-term memory are long- elsmentionedaretrainedandassessedon4AMD
lastingmemories,differentiatedbyhowlongthey MI210GPUs,whichcanhandlemodelsupto7B
| persistinthebrain. |     |     | HMTisinspiredbythismem- |     |     |     |             |     |            |          |     |          |
| ------------------ | --- | --- | ----------------------- | --- | --- | --- | ----------- | --- | ---------- | -------- | --- | -------- |
|                    |     |     |                         |     |     |     | parameters. |     | We further | test HMT | on  | 4 NVIDIA |
oryhierarchy.
|     |     |     |     |     |     |     | A100-80GB |     | GPUs for | the Qwen | 2.5 | 14B model |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | -------- | -------- | --- | --------- |
SensoryMemory: Sensorymemoryforthenth (Baietal.,2023a)tojustifyitsscalabilitytolarger
segment refers to the last k token embeddings of models and gain a consistent effectiveness boost.
| H   | H [L | − k,L). |     |     |     |     |     |     |     |     |     |     |
| --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
n−1 , n−1 When inferencing the TotunetheextraparametersintroducedbyHMT,
nth segment, HMT will augment the correspond- weusetheRedPajamaV2(Computer,2023)dataset
ing token embeddings H by prepending it with to pre-train each model. Notice that HMT intro-
n
H n [L−k,L),showninStep3ofFigure1. duced new model hyperparameters on top of the
Short-termMemory: HMTwillencodetheseg- backbone model (L, j, N, and k). A common
mentintoanembeddingthatservesasa“summa- configuration is L = 1024, j = 512, N = 300,
rization"ofthesegment. First,HMTwillappend and k = 32, and we adjust these values for each
andprependthememorizationpromptembedding model to achieve the best performance. To com-
P to the augmented segment. This guides the parewithpreviousworks(RMT,LongMem,Mem-
n
backbonemodeltocompressthesegmentandrele- orizing Transformer, CCM), we apply the same
vantcontextintoasummarizationembeddingwith backbonemodelsifthemethodisapplicabletoany

Table2: ScalabilityofHMT.AveragePPLiscomputed
| model, or find | a backbone | model with | a similar |     |     |     |     |
| -------------- | ---------- | ---------- | --------- | --- | --- | --- | --- |
sizeifthemethodrequiresspecialarchitecture. bytakingtheaveragePPLforsamplesineachsequence
lengthintheexperiment.
Forthelong-contextbenchmark,weselectsub-
sets(NarrativeQA,Qasper,andMultiFieldQA-en
|     |     |     |     |     | MODEL | AVGTESTPPL(WIKITEXT)(↓) |     |
| --- | --- | --- | --- | --- | ----- | ----------------------- | --- |
forsingledocumentQA;HotpotQA,2WikiMQA,
|     |     |     |     |     | OPT350M | 15.11 |     |
| --- | --- | --- | --- | --- | ------- | ----- | --- |
and MuSiQue for multi-document QA; GovRe- HMT+OPT350M 14.28(-5.8%)
| port,QMSum,andMulti-Newsforsummarization; |     |     |     |     | OPT2.7B     | 12.12        |     |
| ----------------------------------------- | --- | --- | --- | --- | ----------- | ------------ | --- |
|                                           |     |     |     |     | HMT+OPT2.7B | 8.61(-28.9%) |     |
TriviaQAforfew-shotlearning)fromawidelyac-
|     |     |     |     |     | RWKV430M | 19.33 |     |
| --- | --- | --- | --- | --- | -------- | ----- | --- |
knowledged benchmark, LongBench (Bai et al., HMT+RWKV430M 16.10(-16.6%)
|     |     |     |     |     | RWKV3B | 13.30 |     |
| --- | --- | --- | --- | --- | ------ | ----- | --- |
2023b),andmeasurethemagainstmodelsreported
|                            |     |                  |     |     | HMT+RWKV3B | 9.93(-25.3%) |     |
| -------------------------- | --- | ---------------- | --- | --- | ---------- | ------------ | --- |
| intheLongBenchleaderboard. |     | However,themaxi- |     |     |            |              |     |
mumaveragedocumentlengthoftestsetsinLong-
Bench is shorter than 20k words, which is not Moreover,Table2presentshowimprovementsare
very long for modern long-context models. To achieved by HMT scales with the model size for
|     |     |     |     | same-familymodels. |     | Tofurtherstrengthenourar- |     |
| --- | --- | --- | --- | ------------------ | --- | ------------------------- | --- |
betterunderstandHMT’slong-contextprocessing
abilityundervariouscontextscenarios,wefurther gument that HMT can benefit larger models, we
studyHMToncraftedandcontrollabledatasetsam- evaluateHMTwithQwen2.514Butilizing4A100-
ples. Forcrafteddatasets,wederivefromexisting 80GB GPUs for training. As depicted in Figure
4,HMTcanstillincreasetheeffectivenessofthe
| datasetstoformlonginputs. |     | Forgenerallanguage |     |     |     |     |     |
| ------------------------- | --- | ------------------ | --- | --- | --- | --- | --- |
tasks,modelsaretestedfornexttokengeneration backbonemodelonPG-19.
taskswithWikitext-103(Merityetal.,2016)(2-3k Noticethattheimprovementisnotnecessarily
|                   |     |            |               | contributed | solely | by the additional | parameters. |
| ----------------- | --- | ---------- | ------------- | ----------- | ------ | ----------------- | ----------- |
| words per sample) | and | PG-19 (Rae | et al., 2019) |             |        |                   |             |
datasets(69kwordspersampleonaverage). Sam- Having more parameters does not always lead to
ples will be concatenated or split into chunks to higher performance. For example, HMT boosts
form longer samples and investigate the relation- OPT2.7BtorealizealowerperplexitythanOpenL-
lama3Bwith20.7%fewerparameters,whileOPT
shipsbetweeninputlengthandtheeffectivenessof
themodel. Forquestion-answeringtasks,wechose 2.7BperformsworsewithoutHMT.Section5.2de-
PubMedQA(Jinetal.,2019),whichisabiomedi- scribesmoreexamplesofHMTachievingsuperior
generationqualitywithsmallermodels.
calquestion-answeringdatasetwithcorresponding
contexts. We artifact the dataset to assess HMT HMT enhances long-answer contextual rea-
withmulti-contextinputs,describedinAppendixI. soning and short-answer prediction ability in
|     |     |     |     | question-answeringtasks. |     | Oneoftheusecases |     |
| --- | --- | --- | --- | ------------------------ | --- | ---------------- | --- |
5 ResultsandKeyObservations ofHMTishandlingquestion-answeringtasksthat
|     |     |     |     | involvemultiplecontexts. |     | Thus,weselectthePub- |     |
| --- | --- | --- | --- | ------------------------ | --- | -------------------- | --- |
Inthissection,weillustratethemainresultofHMT.
MedQAdatasetandderivelong-contextQAsam-
MoreablationstudiesareinAppendixEandG. pleswithcontrollablecontextcountstoevaluatethe
effectivenessofHMT.Twometricsareemployed:
5.1 ImpactsonBackboneModels
forlonganswers,wecomputethePPLtoassessthe
Byintroducinganadditional0.5%∼1.3%(1.77M
|     |     |     |     | contextual | reasoning | of HMT; | for short answers, |
| --- | --- | --- | --- | ---------- | --------- | ------- | ------------------ |
∼33.5M)ofparameters,HMTcanenhancemodels wemeasuretheresponseaccuracy. AsseeninFig-
withavarietyofarchitecturestoimprovegenera- ures 5 and 6, for samples with 2 to 10 contexts,
tionqualitywhenprocessinglongcontextinputs. HMTincreasestheeffectivenessinPPLby9.48%
Wedemonstratethisfeaturewithgenerallanguage for long answers. For short answer tasks, HMT
modelingandquestion-answeringtasks. is 1.0% more accurate than the backbone model
HMT consistently improves the backbone andexhibitssignificantadvantageswhensamples
|     |     |     |     | havemorecontexts. |     | Insum,HMTincreasesboth |     |
| --- | --- | --- | --- | ----------------- | --- | ---------------------- | --- |
modelsingenerallanguagemodelingtaskswhen
processinglonginputs. Figures2and3compare thecorrectnessandreasoningabilityofmodelsin
| theperplexityofOPT2.7B,RWKV3B,andOpen- |     |     |     | long-contextQAtasks. |     |     |     |
| -------------------------------------- | --- | --- | --- | -------------------- | --- | --- | --- |
LlamaV23BmodelswithandwithoutHMTonthe
Wikitext-103andPG-19datasets. Overinputspan- 5.2 ComparisontoLongContextModels
ning from 2k ∼ 100k tokens, HMT consistently Combined with small and short-context models,
raises the generation quality of all these models. HMT can be more effective than large models

Figure2:TestPerplexityofHMT,RMT,andthreebaselinemodels(OPT2.7B,RWKV3B,OpenLlamaV23B)with
theWikitext-103dataset. HMToutperformsRMTby13.0%forOPTand10.8%forOpenLlamaV2. ForRWKV,
HMTcanevenboosttheeffectivenessby16.5%,whileRMTworsenstheeffectiveness.
Figure3: TestPerplexityofHMT,RMT,andthreebaselinemodels(OPT2.7B,RWKV3B,OpenLlamaV23B),
evaluatedoverthePG-19dataset. HMToutperformsRMTby3.98%forOPTand6.85%forOpenLlamaV2. For
RWKV,HMTcanimprovetheeffectivenessby9.96%.
Figure4: TestPerplexityofHMT,RMT,andbaseline Figure 5: Long answer quality of RMT and HMT
|     |     |     |     | applied on | Llama-2 7B, evaluated | over | PubMedQA |
| --- | --- | --- | --- | ---------- | --------------------- | ---- | -------- |
modelforQwen2.514BonPG-19dataset.HMTboosts
theeffectivenessofthebaselinemodelby10.0%,while dataset. HMTis8.98%moreeffectivethanRMT.
RMTworsensitseffectiveness.
paredtolargemodels.
trained on long-context inputs. Table 3 displays Moreover,applyingHMTtolong-contextmod-
metricresultsofHMT-augmentedmodelsonsub- elscanfurtherimprovetheireffectivenessandre-
|     |     |     |     | duceinferencememoryconsumption. |     | Forexample, |     |
| --- | --- | --- | --- | ------------------------------- | --- | ----------- | --- |
setsofLongBench(Baietal.,2023b)andcompares
theAMDMI210GPUcannothandleinferencing
| them with | large models | specialized | for long con- |     |     |     |     |
| --------- | ------------ | ----------- | ------------- | --- | --- | --- | --- |
texts. Thesubsetscontainvariousgenerationtasks, 30ktokeninputswiththeYi-6B-200Kmodeldue
includingsingle/multi-documentQA,summariza- tomemoryconstraints. Applyingaslidingwindow
|                    |           |      |                 | strategy with | a 5.2K-token | window | (Yi-6B-SW- |
| ------------------ | --------- | ---- | --------------- | ------------- | ------------ | ------ | ---------- |
| tion, and few-shot | learning. | With | a significantly |               |              |        |            |
lower inference memory requirement, HMT ap- 5.2K),themodelconsumes44.8GBVRAM.On
plied to small models can attain comparable or the contrary, HMT + Yi-6B-200K requires only
|                |          |          |                  | 33.9 GB | VRAM to process | 30k tokens | with a |
| -------------- | -------- | -------- | ---------------- | ------- | --------------- | ---------- | ------ |
| better metrics | compared | to large | models, indicat- |         |                 |            |        |
smallsegmentlength(512tokens),witha2%ef-
| ingasignificantresourceadvantage. |     |     | Specifically, |     |     |     |     |
| --------------------------------- | --- | --- | ------------- | --- | --- | --- | --- |
weobservethatHMTwithsmallmodelsperforms fectivenessimprovement. Table4presentstheef-
well in generating short responses for long and fectivenessoflong-rangemodelsonWikitext-103
|     |     |     |     | compared | with several HMT-augmented |     | models, |
| --- | --- | --- | --- | -------- | -------------------------- | --- | ------- |
multi-contextinputs,thankstoitscontext-filtering
ability. However,itexhibitscomparableorweaker includingMambaandMistralmodels.
performanceingeneratinglongresponses,assmall
2Althoughthismodelistrainedwith200K-tokensamples,
modelshaveshortertokengenerationlimitscom- itcannotberunonMI210duetomemoryconstraints.

Table3: MetricresultsofHMT-augmentedsmallmodelsandlargemodelstrainedonlongercontexts. Modelswith
HMTcanprocessinfinitelylongcontext,butonlykeepafixedlengthofKVcache(thevalueintheparenthesis).
We evaluate on subsets of LongBench, including QMSum (QMS), MuSiQue (MSQ), Qasper (QASP), Narra-
tiveQA(NQA),MultiFieldQA-en(MFQA-en),GovReport(GR),TriviaQA(TQA),HotpotQA(HQA),2WikiMQA
(2WMQA),andMultiNews(MN).MemReqindicatestheminimuminferencememoryrequired(tostoreparameters
| andKVcache). ActualinferencemayrequirealargerVRAM. |     |     |     |     |     |     |     |     |
| -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
MODEL CONTEXTWINDOW QMS MSQ QASP NQA MFQA-EN GR TQA HQA 2WMQA MN MEMREQ(GB↓)
GPT-3.5TURBO 16384 23.4 26.9 43.3 23.6 52.3 29.5 91.4 51.6 37.7 26.7 46.7
LLAMA27BCHAT 4096 20.8 9.4 19.2 18.7 36.8 27.3 77.8 25.4 32.8 25.8 15.1
LONGCHATV1.57B 32768 22.7 9.7 27.7 16.9 41.4 30.8 82.3 31.5 20.6 26.4 22.6
XGEN7B 8192 20.5 10.3 18.1 18.0 37.7 27.3 77.8 29.7 21.1 26.2 16.2
INTERNLM7B 8192 15.9 9.0 16.7 12.1 23.4 9.7 77.8 28.7 21.1 22.8 16.2
CHATGLM26B 32768 24.0 21.9 31.5 21.1 46.2 32.4 78.7 45.1 34.0 26.5 19.5
VICUNAV1.57B 16384 22.8 9.8 26.1 19.4 38.5 27.9 86.2 25.3 20.8 27.2 18.3
CHATGLM36B 32768 23.9 40.4 43.3 26.0 51.7 36.8 87.1 54.4 44.9 27.9 19.5
HMT+OPT350M ∞(1024) 22.2 15.6 32.3 17.2 62.7 13.8 87.2 25.3 29.2 10.5 0.75
HMT+OPENLLAMAV23B ∞(512) 21.4 42.3 35.7 21.6 58.1 15.8 93.0 29.9 27.7 11.0 6.1
HMT+SMOLLM135M ∞(1024) 19.4 14.1 30.2 19.6 48.1 15.7 81.3 27.6 23.3 9.5 0.4
BENCHMARKAVERAGELEN (WORDS) 10614 11214 3619 18409 4559 8734 8209 9151 4887 2113
|     |     |     | Figure | 3. Since | RWKV | has already | compressed |     |
| --- | --- | --- | ------ | -------- | ---- | ----------- | ---------- | --- |
pasttokensandpassedhiddenstatesalongthese-
quence,applyingRMTtoRWKVre-weightspast
|     |     |     | informationcompressedinstatesperiodically. |            |     |                      |           | This   |
| --- | --- | --- | ------------------------------------------ | ---------- | --- | -------------------- | --------- | ------ |
|     |     |     | was originally                             | done       | by  | the time-mixing      |           | module |
|     |     |     | of RWKV.                                   | Therefore, | the | advantage            | of memory |        |
|     |     |     | augmentationislimited.                     |            |     | Duetothegradientvan- |           |        |
Figure6: ShortresponseaccuracyofRMTandHMT ishingissue,themodelishardertotrainwithRMT,
applied on Llama-2 7B, evaluated over PubMedQA leadingtoinferiorperformance. However,webe-
dataset. HMTis1.8%moreaccuratethanRMT.
lievethatthememoryretrievalmechanisminHMT
helpsRWKVtoselectprevioushiddenstateswith
Table4: QualityoflongcontextmodelsandHMTwith
|                        |                         |     | themostrelevance,boostingitseffectiveness. |     |     |     |     | An- |
| ---------------------- | ----------------------- | --- | ------------------------------------------ | --- | --- | --- | --- | --- |
| variousbackbonemodels. | Theinputsizeis30ktokens |     |                                            |     |     |     |     |     |
otheradvantageofHMToverRMTisitsscalability
andthedatasetisWikitext-103.
|     |     |     | with large | models: | while | RMT applied | to  | Qwen |
| --- | --- | --- | ---------- | ------- | ----- | ----------- | --- | ---- |
2.514Bresultsinreducedeffectivenesscompared
MODEL MAXCONTEXT TESTPPL(WIKITEXT) todirectinferencewiththebackbonemodel,HMT
| RWKV3B | ∞   | 13.13 |     |     |     |     |     |     |
| ------ | --- | ----- | --- | --- | --- | --- | --- | --- |
MAMBA370M ∞ 87.08 continuestoenhanceeffectiveness,asillustratedin
| YI-6B-200K    | 200K | OOM2 |          |     |     |     |     |     |
| ------------- | ---- | ---- | -------- | --- | --- | --- | --- | --- |
| YI-6B-SW-5.2K | 200K | 6.89 | Figure4. |     |     |     |     |     |
| MISTRAL-7B    | 32K  | 5.47 |          |     |     |     |     |     |
HMT+OPT350M ∞(1024) 13.67 Furthermore, compared with other memory-
| HMT+OPENLLAMAV23B | ∞(512) | 7.04 |     |     |     |     |     |     |
| ----------------- | ------ | ---- | --- | --- | --- | --- | --- | --- |
augmentedmodels,HMTisnotonlyeasytousebut
| HMT+RWKV3B    | ∞(256) | 10.94 |     |     |     |     |     |     |
| ------------- | ------ | ----- | --- | --- | --- | --- | --- | --- |
| HMT+MAMBA370M | ∞(256) | 16.71 |     |     |     |     |     |     |
HMT+YI-6B-200K ∞(512) 6.75 also has higher generation quality. Table 5 picks
| HMT+MISTRAL-7B | ∞(512) | 5.12 |                        |     |     |         |             |     |
| -------------- | ------ | ---- | ---------------------- | --- | --- | ------- | ----------- | --- |
|                |        |      | three memory-augmented |     |     | methods | (Memorizing |     |
Transformer(Wuetal.,2022),LongMem(Wang
etal.,2024),andCCM-concat(Kimetal.,2023))
5.3 ComparisontoMemory-augmentedand
|     |     |     | and compares | them | with | HMT with | the same | or  |
| --- | --- | --- | ------------ | ---- | ---- | -------- | -------- | --- |
HierarchicalMethods
|     |     |     | similar-sized | backbone |     | models. | We choose | the |
| --- | --- | --- | ------------- | -------- | --- | ------- | --------- | --- |
Onepopularmemory-augmentedmodelisthere- datasets used by the original works for fair com-
currentmemorytransformer(Bulatovetal.,2022) parisons. MemorizingtransformerandLongMem
(RMT). Our assessment indicates that HMT is requiremodifyingthecorearchitectureofthebase
generally better at both language modeling and model. Future models cannot easily adopt such
question-answeringtasksthanRMT,illustratedin modifications. Overall, HMT outperforms these
Figures 2, 3, 5, and 6. The improvement gap is methods. Wealsolisttheinferencememoryover-
especially significant for recurrent models such head complexity for each model, where L is the
as RWKV. HMT can further increase the effec- total context length, l is the inference segment
i
tiveness of RWKV while RMT will degrade the length, l is the memory size (L > l > l ),
|     |     |     |     | m   |     |     | m   | i   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
performanceforbothdatasets,asdemonstratedin and t is the number of memory embeddings con-

Table 5: Comparison between HMT with previous and memory-augmented models, HMT achieves
memory-augmentedmethods(MemorizingTransformer,
higher generation quality with lower memory re-
LongMem,andCCM-concat).
quirements. OurmodelprovidesLLMaccessibility
toresource-constrainedapplicationsandrepresents
MODEL TESTPPL(WIKITEXT,30KTOKEN) MEMOVERHEAD astepforwardtolifelonglanguagetasks.
MEMTRM 31.51 O(L)
HMT+OPT350M 13.67 O(li)
MODEL TESTPPL(ARXIV,VARIABLE) MEMOVERHEAD 7 LimitationsandOngoingWorks
LONGMEM 10.08 O(lm)
HMT+QWEN1.5-0.5B 9.02 O(li)
• Currently, HMT will save N memory embed-
MODEL TESTPPL(PG-19,60KTOKEN) MEMOVERHEAD
CCM-CONCAT 7.41 O(t+li) dingsformemorysearch,whichisacross-attention
HMT+LLAMA27B 7.40 O(li)
layer. When N is small (e.g., N = 300), which
is already sufficient for 100k token samples, the
catenated for CCM-concat. HMT has the lowest
overhead is negligible. However, when N grows
memorycomplexityoverallpreviousmethods.
and the memory embeddings are stored in differ-
entphysicalmemoryhierarchies,theoverheadcan
be significant. An intelligent memory prefetch-
ingmechanismcanpotentiallyalleviatethelatency
overhead,whichweleaveasfuturework.
• Due to the large computational graph of mod-
els when training with BPTT, tuning the extra
parameters introduced by HMT can be memory-
consuming,impedingexperimentsonlarger-scale
Figure7:ComparisonbetweenHMTandHOMERwith-
models. A more efficient way to extend BPTT
outcontextextensionandwithYaRN,allapplyingon
depth without memory overhead is a future re-
Llama27B.Onaverage,HMTis9.9%moreeffective
searchdirection.
thanHOMERwithYaRNonPG-19.
• AlthoughHMTemploysonlyoneleveloflong-
Lastly,wecompareHMTwithHOMER(Song
termmemory,onemayusemultiplelevelsoflong-
et al., 2024), a method that hierarchically com-
term memory to improve information access ef-
pressesinputstoreducetheirlengthforinference.
ficiency. Similar techniques have been used for
Intermsofmemorycomplexity,HOMERrequires
O(log(L))memorytostorethereductiontree,lead- multilevel optimization in VLSI physical design
(CongandShinnerl,2013;Chanetal.,2005).
ing to increased peak memory utilization as in-
put length grows. In contrast, HMT maintains
8 EthicalStatements
a constant peak memory complexity regardless
of input length. Regarding effectiveness, HMT
ThecapabilityofmemorizinginformationbyHMT
achieves 9.9% lower perplexity on PG-19 com-
offers convenience to people’s daily lives, while
paredtoHOMERwithYaRN(Pengetal.,2023b)
alsoraisingconcernsaboutprivacyleakagethrough
for context extension. As shown in Figure 7, the
conversationwithlanguagemodelagents. Never-
benefitsofHMTbecomemoresubstantialasinput
theless, with further efforts to deploy it on edge
lengthincreases,highlightingitssuperiorscalabil-
devices without network connections, this issue
itywithlongerinputs.
canberesolved.
6 Conclusion
Acknowledgement
We present HMT, a framework to augment mod-
els’ long-range language processing ability with ThisresearchispartiallysupportedbythePRISM
contextswitching. Inspiredbythebrain’smemory (000705769)centerundertheJUMP2.0program
hierarchy,HMTimitateshumanmemorizationbe- byDARPA/SRCandNSFSEEDfunding. Itisalso
haviorbydeployinghierarchicalmemoryandthe supportedbyCDSCindustrialpartners(https://
memory retrieval mechanism. HMT consistently cdsc.ucla.edu/partners)andtheAMDHACC
improves the generation quality of the backbone Program.
models. Comparedwithotherlong-contextLLMs

References
|         |         |        |         |         |     |              | Jingsheng  | Jason        | Cong | and Joseph | R        | Shinnerl. | 2013. |
| ------- | ------- | ------ | ------- | ------- | --- | ------------ | ---------- | ------------ | ---- | ---------- | -------- | --------- | ----- |
|         |         |        |         |         |     |              | Multilevel | optimization |      | in         | VLSICAD, | volume    | 14.   |
| Rodrigo | Agerri, | Xabier | Artola, | Zuhaitz |     | Beloki, Ger- |            |              |      |            |          |           |       |
SpringerScience&BusinessMedia.
| man                        | Rigau, | and Aitor | Soroa. |                     | 2015. | Big data for |             |       |       |        |     |        |         |
| -------------------------- | ------ | --------- | ------ | ------------------- | ----- | ------------ | ----------- | ----- | ----- | ------ | --- | ------ | ------- |
| naturallanguageprocessing: |        |           |        | Astreamingapproach. |       |              |             |       |       |        |     |        |         |
|                            |        |           |        |                     |       |              | Yi Dai, Hao | Lang, | Yinhe | Zheng, | Fei | Huang, | Luo Si, |
Knowledge-BasedSystems,79:36–42.
|     |     |     |     |     |     |     | andYongbinLi.2022.                |     |     | Lifelonglearningforquestion |     |               |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --------------------------- | --- | ------------- | --- |
|     |     |     |     |     |     |     | answeringwithhierarchicalprompts. |     |     |                             |     | arXivpreprint |     |
LoubnaBenAllal,AntonLozhkov,ElieBakouch,Le-
arXiv:2208.14602.
| androvonWerra,andThomasWolf.2024. |     |     |     |     |     | Smollm- |     |     |     |     |     |     |     |
| --------------------------------- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
blazinglyfastandremarkablypowerful.
|     |     |     |     |     |     |     | Zihang Dai, | Zhilin | Yang, | Yiming | Yang,  | Jaime          | Car- |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------ | ----- | ------ | ------ | -------------- | ---- |
|     |     |     |     |     |     |     | bonell,     | Quoc   | V Le, | and    | Ruslan | Salakhutdinov. |      |
DzmitryBahdanau,KyunghyunCho,andYoshuaBen-
|          |       |        |                |             |       |            | 2019.      | Transformer-xl: |                | Attentive |          | language | mod-     |
| -------- | ----- | ------ | -------------- | ----------- | ----- | ---------- | ---------- | --------------- | -------------- | --------- | -------- | -------- | -------- |
| gio.     | 2014. | Neural | machine        | translation |       | by jointly |            |                 |                |           |          |          |          |
|          |       |        |                |             |       |            | els beyond |                 | a fixed-length |           | context. | arXiv    | preprint |
| learning | to    | align  | and translate. |             | arXiv | preprint   |            |                 |                |           |          |          |          |
arXiv:1901.02860.
arXiv:1409.0473.
JinzeBai,ShuaiBai,YunfeiChu,ZeyuCui,KaiDang, Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and
XiaodongDeng,YangFan,WenbinGe,YuHan,Fei Christopher Ré. 2022. Flashattention: Fast and
memory-efficientexactattentionwithio-awareness.
| Huang,etal.2023a. |     |     | Qwentechnicalreport. |     |     | arXiv |     |     |     |     |     |     |     |
| ----------------- | --- | --- | -------------------- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
AdvancesinNeuralInformationProcessingSystems,
preprintarXiv:2309.16609.
35:16344–16359.
| Yushi Bai, | Xin | Lv, | Jiajie | Zhang, | Hongchang | Lyu, |     |     |     |     |     |     |     |
| ---------- | --- | --- | ------ | ------ | --------- | ---- | --- | --- | --- | --- | --- | --- | --- |
JiankaiTang,ZhidianHuang,ZhengxiaoDu,Xiao Li Dong, Nan Yang, Wenhui Wang, Furu Wei, Xi-
Liu,AohanZeng,LeiHou,etal.2023b. Longbench: aodong Liu, Yu Wang, Jianfeng Gao, Ming Zhou,
|              |     |           |           |     |     |              | andHsiao-WuenHon.2019. |     |     |     | Unifiedlanguagemodel |     |     |
| ------------ | --- | --------- | --------- | --- | --- | ------------ | ---------------------- | --- | --- | --- | -------------------- | --- | --- |
| A bilingual, |     | multitask | benchmark |     | for | long context |                        |     |     |     |                      |     |     |
pre-trainingfornaturallanguageunderstandingand
| understanding.                               |     | arXivpreprintarXiv:2308.14508. |     |     |     |       |                |                                     |     |     |     |     |     |
| -------------------------------------------- | --- | ------------------------------ | --- | --- | --- | ----- | -------------- | ----------------------------------- | --- | --- | --- | --- | --- |
|                                              |     |                                |     |     |     |       | generation.    | Advancesinneuralinformationprocess- |     |     |     |     |     |
| IzBeltagy,MatthewEPeters,andArmanCohan.2020. |     |                                |     |     |     |       | ingsystems,32. |                                     |     |     |     |     |     |
| Longformer:                                  |     | Thelong-documenttransformer.   |     |     |     | arXiv |                |                                     |     |     |     |     |     |
preprintarXiv:2004.05150. Alexey Dosovitskiy, Lucas Beyer, Alexander
|        |          |     |       |        |         |     | Kolesnikov, |              | Dirk | Weissenborn, |           | Xiaohua | Zhai,    |
| ------ | -------- | --- | ----- | ------ | ------- | --- | ----------- | ------------ | ---- | ------------ | --------- | ------- | -------- |
| Amanda | Bertsch, | Uri | Alon, | Graham | Neubig, | and |             |              |      |              |           |         |          |
|        |          |     |       |        |         |     | Thomas      | Unterthiner, |      | Mostafa      | Dehghani, |         | Matthias |
Matthew R Gormley. 2023. Unlimiformer: Long- Minderer,GeorgHeigold,SylvainGelly,etal.2020.
range transformers with unlimited length input. An image is worth 16x16 words: Transformers
arXivpreprintarXiv:2305.01625. for image recognition at scale. arXiv preprint
arXiv:2010.11929.
| Aydar Bulatov, |           | Yury   | Kuratov, | and          | Mikhail | Burtsev. |     |     |     |     |     |     |     |
| -------------- | --------- | ------ | -------- | ------------ | ------- | -------- | --- | --- | --- | --- | --- | --- | --- |
| 2022.          | Recurrent | memory |          | transformer. |         | Advances |     |     |     |     |     |     |     |
AbhimanyuDubey,AbhinavJauhri,AbhinavPandey,
inNeuralInformationProcessingSystems,35:11079–
AbhishekKadian,AhmadAl-Dahle,AieshaLetman,
| 11091. |     |     |     |     |     |     | Akhil          | Mathur, | Alan                   | Schelten, | Amy | Yang, | Angela |
| ------ | --- | --- | --- | --- | --- | --- | -------------- | ------- | ---------------------- | --------- | --- | ----- | ------ |
|        |     |     |     |     |     |     | Fan,etal.2024. |         | Thellama3herdofmodels. |           |     |       | arXiv  |
MarkBurgin.2011. Epistemicinformationinstratified preprintarXiv:2407.21783.
| m-spaces. | Information,2(4):697–726. |     |     |     |     |     |     |     |     |     |     |     |     |
| --------- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
LeoGao,StellaBiderman,SidBlack,LaurenceGold-
| TonyChan,JasonCong,andKentonSze.2005. |     |     |     |     |     | Mul- |     |     |     |     |     |     |     |
| ------------------------------------- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
ing,TravisHoppe,CharlesFoster,JasonPhang,Ho-
tilevelgeneralizedforce-directedmethodforcircuit
|            |                                     |     |     |     |     |     | raceHe,   | AnishThite, |       | NoaNabeshima, |            | etal.2020. |          |
| ---------- | ----------------------------------- | --- | --- | --- | --- | --- | --------- | ----------- | ----- | ------------- | ---------- | ---------- | -------- |
| placement. | InProceedingsofthe2005international |     |     |     |     |     |           |             |       |               |            |            |          |
|            |                                     |     |     |     |     |     | The pile: | An          | 800gb | dataset       | of diverse | text       | for lan- |
symposiumonphysicaldesign,pages185–192.
|                  |      |        |           |       |          |           | guagemodeling.             |     | arXivpreprintarXiv:2101.00027. |     |                  |     |     |
| ---------------- | ---- | ------ | --------- | ----- | -------- | --------- | -------------------------- | --- | ------------------------------ | --- | ---------------- | --- | --- |
| Andre Xian       | Ming | Chang, |           | Berin | Martini, | and Euge- |                            |     |                                |     |                  |     |     |
|                  |      |        |           |       |          |           | XinyangGengandHaoLiu.2023. |     |                                |     | Openllama:Anopen |     |     |
| nio Culurciello. |      | 2015.  | Recurrent |       | neural   | networks  |                            |     |                                |     |                  |     |     |
reproductionofllama.
| hardware | implementation |     |     | on fpga. | arXiv | preprint |     |     |     |     |     |     |     |
| -------- | -------------- | --- | --- | -------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
arXiv:1511.05552.
|     |     |     |     |     |     |     | Albert Gu | and | Tri Dao. | 2023. | Mamba: | Linear-time |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | -------- | ----- | ------ | ----------- | --- |
Alexis Chevalier, Alexander Wettig, Anirudh Ajith, sequencemodelingwithselectivestatespaces. arXiv
preprintarXiv:2312.00752.
| and    | Danqi | Chen.    | 2023.     |     | Adapting | language |                                          |     |     |     |     |     |      |
| ------ | ----- | -------- | --------- | --- | -------- | -------- | ---------------------------------------- | --- | --- | --- | --- | --- | ---- |
| models | to    | compress | contexts. |     | arXiv    | preprint |                                          |     |     |     |     |     |      |
|        |       |          |           |     |          |          | SeppHochreiterandJürgenSchmidhuber.1997. |     |     |     |     |     | Long |
arXiv:2305.14788.
|                                            |     |     |     |                       |     |     | short-termmemory. |       |        | Neuralcomputation,9(8):1735– |         |         |        |
| ------------------------------------------ | --- | --- | --- | --------------------- | --- | --- | ----------------- | ----- | ------ | ---------------------------- | ------- | ------- | ------ |
| JunyoungChung,CaglarGulcehre,KyungHyunCho, |     |     |     |                       |     |     | 1780.             |       |        |                              |         |         |        |
| andYoshuaBengio.2014.                      |     |     |     | Empiricalevaluationof |     |     |                   |       |        |                              |         |         |        |
|                                            |     |     |     |                       |     |     | Edward            | J Hu, | Yelong | Shen,                        | Phillip | Wallis, | Zeyuan |
gatedrecurrentneuralnetworksonsequencemodel-
|     |     |     |     |     |     |     | Allen-Zhu, |     | Yuanzhi | Li, Shean | Wang, | Lu  | Wang, |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ------- | --------- | ----- | --- | ----- |
ing. arXivpreprintarXiv:1412.3555.
|     |     |     |     |     |     |     | and Weizhu |     | Chen. | 2021. | Lora: | Low-rank | adap- |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ----- | ----- | ----- | -------- | ----- |
TogetherComputer.2023. Redpajama: anopendataset tation of large language models. arXiv preprint
| fortraininglargelanguagemodels. |     |     |     |     |     |     | arXiv:2106.09685. |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- |

Albert Q Jiang, Alexandre Sablayrolles, Arthur Men- BowenPeng,JeffreyQuesnelle,HongluFan,andEnrico
sch,ChrisBamford,DevendraSinghChaplot,Diego Shippole. 2023b. Yarn: Efficient context window
delasCasas,FlorianBressand,GiannaLengyel,Guil- extensionoflargelanguagemodels. arXivpreprint
| laumeLample,LucileSaulnier,etal.2023. |     |     |     |     | Mistral | arXiv:2309.00071. |     |     |     |     |     |
| ------------------------------------- | --- | --- | --- | --- | ------- | ----------------- | --- | --- | --- | --- | --- |
7b. arXivpreprintarXiv:2310.06825.
JackWRae,AnnaPotapenko,SiddhantMJayakumar,
QiaoJin,BhuwanDhingra,ZhengpingLiu,WilliamW andTimothyPLillicrap.2019. Compressivetrans-
Cohen,andXinghuaLu.2019. Pubmedqa: Adataset formersforlong-rangesequencemodelling. arXiv
forbiomedicalresearchquestionanswering. arXiv preprintarXiv:1911.05507.
preprintarXiv:1909.06146.
|     |     |     |     |     |     | Samyam Rajbhandari, |     | Jeff | Rasley, | Olatunji | Ruwase, |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | ---- | ------- | -------- | ------- |
Jang-HyunKim, JunyoungYeom, SangdooYun, and andYuxiongHe.2020. Zero: Memoryoptimizations
| HyunOhSong.2023. |     | Compressedcontextmemory |     |     |     |                                        |     |     |     |     |         |
| ---------------- | --- | ----------------------- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- | ------- |
|                  |     |                         |     |     |     | towardtrainingtrillionparametermodels. |     |     |     |     | InSC20: |
foronlinelanguagemodelinteraction. arXivpreprint InternationalConferenceforHighPerformanceCom-
arXiv:2312.03414. puting,Networking,StorageandAnalysis,pages1–
16.IEEE.
| Nikita Kitaev, | Łukasz | Kaiser, | and | Anselm | Levskaya. |     |     |     |     |     |     |
| -------------- | ------ | ------- | --- | ------ | --------- | --- | --- | --- | --- | --- | --- |
2020. Reformer: The efficient transformer. arXiv JeffRasley,SamyamRajbhandari,OlatunjiRuwase,and
preprintarXiv:2001.04451.
|     |     |     |     |     |     | Yuxiong | He. 2020. | Deepspeed: |     | System | optimiza- |
| --- | --- | --- | --- | --- | --- | ------- | --------- | ---------- | --- | ------ | --------- |
tionsenabletrainingdeeplearningmodelswithover
| Olga Kovaleva,      | Alexey | Romanov, |                         | Anna | Rogers, and |                       |     |     |                        |     |     |
| ------------------- | ------ | -------- | ----------------------- | ---- | ----------- | --------------------- | --- | --- | ---------------------- | --- | --- |
|                     |        |          |                         |      |             | 100billionparameters. |     |     | InProceedingsofthe26th |     |     |
| AnnaRumshisky.2019. |        |          | Revealingthedarksecrets |      |             |                       |     |     |                        |     |     |
ACMSIGKDDInternationalConferenceonKnowl-
ofbert. arXivpreprintarXiv:1908.08593. edgeDiscovery&DataMining,pages3505–3506.
| Opher Lieber,  | Barak | Lenz, | Hofit | Bata,       | Gal Co- |            |        |       |          |        |        |
| -------------- | ----- | ----- | ----- | ----------- | ------- | ---------- | ------ | ----- | -------- | ------ | ------ |
|                |       |       |       |             |         | Freda Shi, | Xinyun | Chen, | Kanishka | Misra, | Nathan |
| hen, Jhonathan |       | Osin, | Itay  | Dalmedigos, | Erez    |            |        |       |          |        |        |
Scales,DavidDohan,EdHChi,NathanaelSchärli,
| Safahi,                         | Shaked | Meirom, | Yonatan | Belinkov,     | Shai     |                    |            |     |                        |           |           |
| ------------------------------- | ------ | ------- | ------- | ------------- | -------- | ------------------ | ---------- | --- | ---------------------- | --------- | --------- |
|                                 |        |         |         |               |          | andDennyZhou.2023. |            |     | Largelanguagemodelscan |           |           |
| Shalev-Shwartz,                 |        | et al.  | 2024.   | Jamba:        | A hybrid |                    |            |     |                        |           |           |
|                                 |        |         |         |               |          | be easily          | distracted | by  | irrelevant             | context.  | In Inter- |
| transformer-mambalanguagemodel. |        |         |         | arXivpreprint |          |                    |            |     |                        |           |           |
|                                 |        |         |         |               |          | national           | Conference | on  | Machine                | Learning, | pages     |
arXiv:2403.19887.
31210–31227.PMLR.
PengfeiLiu,WeizheYuan,JinlanFu,ZhengbaoJiang,
WoominSong,SeunghyukOh,SangwooMo,Jaehyung
| Hiroaki | Hayashi, | and Graham |     | Neubig. | 2023. Pre- |     |     |     |     |     |     |
| ------- | -------- | ---------- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- |
Kim,SukminYun,Jung-WooHa,andJinwooShin.
| train, prompt, | and | predict: | A systematic |     | survey of |       |              |         |          |     |             |
| -------------- | --- | -------- | ------------ | --- | --------- | ----- | ------------ | ------- | -------- | --- | ----------- |
|                |     |          |              |     |           | 2024. | Hierarchical | context | merging: |     | Better long |
promptingmethodsinnaturallanguageprocessing.
|     |     |     |     |     |     | context | understanding | for | pre-trained |     | llms. arXiv |
| --- | --- | --- | --- | --- | --- | ------- | ------------- | --- | ----------- | --- | ----------- |
ACMComputingSurveys,55(9):1–35.
preprintarXiv:2404.10308.
StephenMerity,CaimingXiong,JamesBradbury,and
Fan-KengSun,Cheng-HaoHo,andHung-YiLee.2019.
| RichardSocher.2016. |     | Pointersentinelmixturemod- |     |     |     |        |          |          |     |          |          |
| ------------------- | --- | -------------------------- | --- | --- | --- | ------ | -------- | -------- | --- | -------- | -------- |
|                     |     |                            |     |     |     | Lamol: | Language | modeling | for | lifelong | language |
els. arXivpreprintarXiv:1609.07843.
|                 |        |        |        |     |             | learning. | arXivpreprintarXiv:1909.03329. |     |     |     |     |
| --------------- | ------ | ------ | ------ | --- | ----------- | --------- | ------------------------------ | --- | --- | --- | --- |
| Ali Modarressi, | Ayyoob | Imani, | Mohsen |     | Fayyaz, and |           |                                |     |     |     |     |
JambaTeam,BarakLenz,AlanArazi,AmirBergman,
| HinrichSchütze.2023. |     |     | Ret-llm: | Towardsageneral |     |     |     |     |     |     |     |
| -------------------- | --- | --- | -------- | --------------- | --- | --- | --- | --- | --- | --- | --- |
AvshalomManevich,BarakPeleg,BenAviram,Chen
| read-writememoryforlargelanguagemodels. |     |     |     |     | arXiv |     |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
preprintarXiv:2305.14322. Almagor, Clara Fridman, Dan Padnos, et al. 2024.
|     |     |     |     |     |     | Jamba-1.5: | Hybrid | transformer-mamba |     |     | models at |
| --- | --- | --- | --- | --- | --- | ---------- | ------ | ----------------- | --- | --- | --------- |
Gianluca Moro, Luca Ragazzi, Lorenzo Valgimigli, scale. arXivpreprintarXiv:2408.12570.
| Giacomo | Frisoni,          | Claudio   | Sartori,        |     | and Gustavo |               |            |         |         |         |           |
| ------- | ----------------- | --------- | --------------- | --- | ----------- | ------------- | ---------- | ------- | ------- | ------- | --------- |
|         |                   |           |                 |     |             | Hugo Touvron, | Louis      | Martin, | Kevin   | Stone,  | Peter Al- |
| Marfia. | 2023.             | Efficient | memory-enhanced |     | trans-      |               |            |         |         |         |           |
|         |                   |           |                 |     |             | bert, Amjad   | Almahairi, |         | Yasmine | Babaei, | Nikolay   |
| former  | for long-document |           | summarization   |     | in low-     |               |            |         |         |         |           |
resourceregimes. Sensors,23(7):3542. Bashlykov,SoumyaBatra,PrajjwalBhargava,Shruti
|     |     |     |     |     |     | Bhosale, | et al. | 2023. | Llama | 2:  | Open founda- |
| --- | --- | --- | --- | --- | --- | -------- | ------ | ----- | ----- | --- | ------------ |
MichaelCMozer.2013. Afocusedbackpropagation tion and fine-tuned chat models. arXiv preprint
| algorithmfortemporalpatternrecognition. |     |     |     |     | InBack- | arXiv:2307.09288. |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | ------- | ----------------- | --- | --- | --- | --- | --- |
propagation,pages137–169.PsychologyPress.
|     |     |     |     |     |     | Ashish Vaswani, |       | Noam Shazeer, |       | Niki     | Parmar, Jakob |
| --- | --- | --- | --- | --- | --- | --------------- | ----- | ------------- | ----- | -------- | ------------- |
|     |     |     |     |     |     | Uszkoreit,      | Llion | Jones,        | Aidan | N Gomez, | Łukasz        |
RazvanPascanu,TomasMikolov,andYoshuaBengio.
2013. Onthedifficultyoftrainingrecurrentneural Kaiser,andIlliaPolosukhin.2017. Attentionisall
networks. InInternationalconferenceonmachine youneed. Advancesinneuralinformationprocessing
| learning,pages1310–1318.Pmlr. |     |     |     |     |     | systems,30. |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |
Bo Peng, Eric Alcaide, Quentin Anthony, Alon Al- Weizhi Wang, Li Dong, Hao Cheng, Xiaodong Liu,
balak,SamuelArcadinho,HuanqiCao,XinCheng, XifengYan,JianfengGao,andFuruWei.2024. Aug-
Michael Chung, Matteo Grella, Kranthi Kiran GV, menting language models with long-term memory.
etal.2023a. Rwkv: Reinventingrnnsforthetrans- AdvancesinNeuralInformationProcessingSystems,
| formerera. | arXivpreprintarXiv:2305.13048. |     |     |     |     | 36. |     |     |     |     |     |
| ---------- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

QingyangWu,ZhenzhongLan,KunQian,JingGu,Al-
| borzGeramifard,andZhouYu.2020. |     |     | Memformer: |     |
| ------------------------------ | --- | --- | ---------- | --- |
Amemory-augmentedtransformerforsequencemod-
eling. arXivpreprintarXiv:2010.06891.
YuhuaiWu,MarkusNRabe,DeLesleyHutchins,and
| ChristianSzegedy.2022. |     |     | Memorizingtransformers. |     |
| ---------------------- | --- | --- | ----------------------- | --- |
arXivpreprintarXiv:2203.08913.
| Hongkang                         | Yang, Zehao  | Lin,     | Wenjin Wang,     | Hao Wu,  |
| -------------------------------- | ------------ | -------- | ---------------- | -------- |
| Zhiyu                            | Li, Bo Tang, | Wenqiang | Wei, Jinbo       | Wang,    |
| ZeyunTang,ShichaoSong,etal.2024. |              |          |                  | Memory3: |
| Language                         | modeling     | with     | explicit memory. | arXiv    |
preprintarXiv:2407.01178.
| Alex Young,     | Bei     | Chen, Chao | Li, Chengen      | Huang,     |
| --------------- | ------- | ---------- | ---------------- | ---------- |
| Ge Zhang,       | Guanwei | Zhang,     | Heng Li,         | Jiangcheng |
| Zhu, Jianqun    | Chen,   | Jing       | Chang, et al.    | 2024. Yi:  |
| Open foundation |         | models     | by 01. ai. arXiv | preprint   |
arXiv:2403.04652.
ShuangfeiZhai,WalterTalbott,NitishSrivastava,Chen
| Huang,         | Hanlin                      | Goh, Ruixiang | Zhang, | and Josh |
| -------------- | --------------------------- | ------------- | ------ | -------- |
| Susskind.2021. | Anattentionfreetransformer. |               |        | arXiv    |
preprintarXiv:2105.14103.
HangZhang,YeyunGong,YelongShen,WeishengLi,
| Jiancheng      | Lv, Nan                       | Duan,         | and Weizhu | Chen. 2021. |
| -------------- | ----------------------------- | ------------- | ---------- | ----------- |
| Poolingformer: | Longdocumentmodelingwithpool- |               |            |             |
| ing attention. | In                            | International | Conference | on Ma-      |
chineLearning,pages12437–12446.PMLR.
| Susan Zhang, | Stephen | Roller, | Naman Goyal, | Mikel |
| ------------ | ------- | ------- | ------------ | ----- |
Artetxe,MoyaChen,ShuohuiChen,ChristopherDe-
wan,MonaDiab,XianLi,XiVictoriaLin,etal.2022.
Opt: Openpre-trainedtransformerlanguagemodels.
arXivpreprintarXiv:2205.01068.

A OtherRelatedWorks
The memory-augmented long-context transformer has been an active research topic in recent years.
LongMem(Wangetal.,2024)chunksthelong-documentinputintosegmentsandcachestheattention
keys and values for each segment. During the inference of a segment, LongMem will select relevant
key-valueembeddingpairsbycomputingtheattentionscorebetweentokenembeddingsandthecached
keyembeddingsandfusethetopkembeddings. MemorizingTransformer(Wuetal.,2022)alsocaches
thekey-valueembeddingpairssimilartoLongMem,bututilizesakNNsearchtoretrieveinformation
similartoUnlimiformer. RET-LLM(Modarressietal.,2023)employspromptengineeringtostorethe
informativecontextinadatabaseandsearchkeywordswhenthecontextinvolvesquestions. Memory3
(Yang et al., 2024) compresses segments of tokens into “explicit" memory blocks and stores them
directly into a memory bank for retrieval. While these works can precisely retrieve contexts, they are
notscalableduetotheincreasingmemoryconsumptionofstoringlongcontextswithoutcompression.
Segment-levelrecurrentmodels,suchasEMMA(Moroetal.,2023),Memformer(Wuetal.,2020),and
Transformer-XL (Dai et al., 2019), attempt to compress memory throughout the recurrence to reduce
memoryconsumption. EMMAcomposeslong-termmemoryfrommultipleshort-termmemorybylinear
combinationandconcatenateslongandshort-termmemorytoaugmentthesegments. Transformer-XL
propagates the compressed memory states derived from the attention of current layers to the previous
layers for every iteration. Memformer augments the attention with the stored memory embeddings
per time step and retrieves information using the cross-attention layer of the encoder-decoder model.
However,MemformeremploysaforgettingnetworktoremoveirrelevantcontextsimilartoLSTM,which
can potentially delete useful contexts for unseen inputs. On the other hand, HMT condenses contexts
intoembeddingsandretrievesinformationpreciselywithoutrequiringaforgettingnetworktoremove
informationpermanently. Also,someoftheseworks,includingMemorizingTransformer,Memformer,
TransformerXL,andUnlimiformer,needtofundamentallychangethemodelarchitectureorinjectnew
adaptersbasedondifferentbasemodelarchitecture. ItmakesdeploymentandextensiontofutureLLMs
veryexpensive. HMTavoidsthisissuebyhavingamodel-independentplug-and-playframework.
B ComparisontoLongMem
UnlikeHMT,LongMem(Wangetal.,2024)operatesonthekeyandvaluecachesofeachlayerofthe
modelandrequirescachinglongcachestocapturedistantcontext. TocomparewithLongMem,wepick
theQwen1.5-0.5B(Baietal.,2023a)modelasthebackbonemodelandtrainHMTby700stepswith
4segmentsover100samplesoftheArXivsubsetofthePiledataset(Gaoetal.,2020). Thesubsethas
15.4Ktokensonaverageand60Ktokensonmaximumpersample,as(Wangetal.,2024)described. Due
to the large storage consumption of the training subset of the Pile dataset, we only extract the ArXiv
subsetinthevalidationandtestsplit. HMTistrainedonthevalidationsetandtestedonthetestset. Table
6illustratesthatHMT+Qwen1.5-0.5BrealizeslowerPPL,withasmallerparametersizeandin-memory
length(numberofmemoryembeddings,whichisthenumberofkeyandvalueembeddingscachedfor
LongMem). ThisindicatesthatHMTismemoryefficient.
Table6: EffectivenessofLongMem(Wangetal.,2024)andHMT+Qwen1.5-0.5BmodelsoverArXivsubsetof
thePiledataset. WithHMT,theQwen1.5-0.5Bmodelcanobtainbettereffectivenesswithfewerparametersand
shortermemory,after700stepsofupdate. TheresultforLongMemcomesfromtheoriginalpaper. Subscriptionis
thestandarddeviation.
MODEL #PARAMS SEGMENTLENGTH IN-MEMORYLENGTH TESTPPL(ARXIV)
LONGMEM 558M 1K 65K 10.08
HMT+QWEN1.5-0.5B 463M 1K 300 9.02
±0.04

Table7: Trainingandfine-tuningconfigurationsforthebackbonemodels(OPT350M,Mamba370M,OPT2.7B,
RWKV3B,OpenLlamaV23B,Llama27B,Yi-6B-200K,andMistral7B)andthemodifiedmodelafterapplying
RMTandHMT.S1andS2denotethefirststageandthesecondstageofmulti-stagetrainingforHMT.4AMD
MI210GPUscannottrainlargermodels. Thegivenlearningrateisthestartinglearningrateandwilldecaybya
factorof0.9forOPT,OpenLlamaV2,andRWKVmodelsand0.7fortheremainingmodelsforevery100steps.
Thebatchsizeis2.
MODEL INPUTLENGTH SEGMENTLENGTH LEARNINGRATE TRAININGSTEPS EXTRAPARAM
| OPT350M/SMOLLM135M    | 2048  | 1024 | 1E-5 | 700 |                  |
| --------------------- | ----- | ---- | ---- | --- | ---------------- |
| +RMT                  | 2048  | 1024 | 1E-5 | 700 |                  |
| +HMT(S1)              | 2048  | 1024 | 1E-5 | 200 |                  |
| +HMT(S2)              | 15360 | 1024 | 1E-5 | 500 | 1.77M(0.5%-1.3%) |
| OPT2.7B/OPENLLAMAV23B | 2048  | 512  | 1E-5 | 700 |                  |
| +RMT                  | 1280  | 512  | 1E-5 | 700 |                  |
| +HMT(S1)              | 1024  | 512  | 1E-5 | 200 |                  |
| +HMT(S2)              | 4096  | 512  | 1E-5 | 500 | 13.1M(0.5%)      |
| RWKV3B                | 1280  | 256  | 1E-5 | 700 |                  |
| +RMT                  | 1280  | 256  | 1E-4 | 700 |                  |
| +HMT(S1)              | 512   | 256  | 1E-5 | 200 |                  |
| +HMT(S2)              | 1280  | 256  | 1E-5 | 500 | 13.1M(0.5%)      |
| LLAMA27B              | 2048  | 256  | 1E-4 | 700 |                  |
| +RMT                  | 1280  | 256  | 1E-4 | 700 |                  |
| +HMT(S1)              | 512   | 256  | 1E-4 | 200 |                  |
| +HMT(S2)              | 2048  | 256  | 1E-4 | 500 | 33.5M(0.5%)      |
| MAMBA370M             | 1536  | 256  | 1E-4 | 700 |                  |
| +HMT(S1)              | 512   | 256  | 1E-4 | 200 |                  |
| +HMT(S2)              | 1536  | 256  | 1E-4 | 500 | 4.1M(1.1%)       |
| YI-6B-200K/MISTRAL7B  | 2048  | -    | 2E-4 | 700 |                  |
| +HMT(S1)              | 1024  | 512  | 2E-4 | 200 |                  |
| +HMT(S2)              | 1536  | 512  | 2E-4 | 500 | 33.5M(0.5%)      |
C ComparisontoUnlimiformer
Therearetwomajordifferencesbetweenapreviousretrieval-augmentedmodel,Unlimiformer(Bertsch
etal.,2023),andHMTintermsofthememoryretrievalmechanism:
• UnlimiformerretrievestheinformationwithkNNsearchoverthecollectionofencodedtokensegments,
whileHMTusescross-attention. Webelievethereareseveraladvantagesofemployingcross-attention:
(1) Attending Top K’s most similar token segments still introduces information loss. Regarding the
self-attentionlayer,theaggregationoftokenswithlesssimilarencodingsmaypositivelycontributeto
thequalityofthefinaloutput. Ontheotherhand,cross-attentionfusesallcachedhiddenembeddings,
weightedbytherelativesimilarity,whichcapturesthewholecontext. (2)Theoutputofthecross-attention
isasingleembedding,whichhaslowercomputationaloverheadcomparedtoattendingkextratokens.
• Each cached memory embedding encodes the current token segment and the previous memory em-
beddinginHMT.Therefore,HMTcancapturethewholecontextevenwithalimitednumberofcached
embeddings. Memoryrecallismainlyusedtorescaletheimportanceofpastinformation. Ontheother
hand,theUnlimiformerneedstostoreallencodings,whichismemory-consuming.
Intermsofusage,Unlimiformertargetsencoder-decodermodelsandinjectsretrievalmodulesintothe
backbonemodel. Althoughtheauthorsrecentlyaddedsupportfordecoder-onlymodelsfortokengenera-
tion,onlytheLlamamodelarchitectures(Touvronetal.,2023)canbeappliedandthetraining/evaluation
procedureisnotspecified. ThisisoneofthebiggestchallengesforUnlimiformertoadapttofutureLLMs
forvalidationandgeneration. Onthecontrary,HMTfocusesondecoder-onlymodels. SinceHMTdoes
notinjectnewmodulesinthebackbonemodel,itiseffortlesstoadapttofutureLLMs.
D HMT,RMT,andBaselineTrainingDetailsandHyperparameters
Table7arethetrainingconfigurationsofthebackbonemodelsandHMT/RMT.
Thebaselinesareassessedusingtheslidingwindowattentionforcontext-constrainedmodelstocontrol
the memory consumption for a fair comparison. Due to the limited VRAM of GPUs, we shrink the

segment length for the larger backbone model. Also, increasing memory token size does not improve
theeffectivenessas(Bulatovetal.,2022)suggested. Thus,bothRMTandHMTapplymemorytokens
withalengthof1. ForRMT,weutilizethemaximumBPTTunrolldepthwiththebesteffectivenessthat
the GPUs can handle. HMT is trained with the multi-stage training technique illustrated in Section F.
Thefirststage(S1)istrainedwith2segments,andthesecondstage(S2)istrainedwiththemaximum
BPTT unroll depth that the GPUs can manage. The size of long-term memory is 300 (i.e., N = 300)
forOPT,SmolLM,OpenLlama,Yi,andMistralmodelsand400(N = 400)fortherestofthemodels
tocapturesufficientcontextsandwesummarizehalfofthesegmentforrepresentationextraction(i.e.,
j = L/2). WeobservedthatthebenefitofincreasingN isdiminishingandstopsat300for100ktoken
inputs,describedinAppendixE.WeselectthelearningrateforHMT,RMT,andthebaselinetooptimize
the effectiveness. Furthermore, HMT preserves 32 tokens (k = 32) from the previous segment as the
sensorymemory. Allmodelsaretrainedwith700steps,whichissufficienttoconvergethetrainingloss.
FormodelswithHMT,wefirstpretrainthemodelwithRedPajamaV2(Computer,2023)with700steps,
thenfinetunethemodelforthedownstreamtaskswith700steps. ForLongBench,theevaluationmetrics
arethesameastheoriginalworkandweusetheHuggingfaceevaluatepackagetocomputeRouge-Land
F1score. Forparameter-efficienttraining,LoRA(Huetal.,2021)withrank8isappliedtomodelswith
hightrainingmemoryconsumption(Llama27B,Mamba370M,Yi-6B-200K,andMistral7B).Forthe
restofthemodels,wefinetuneallparametersinthebackbonemodel. Allexperimentsaredonewith3
randomseedsandwetaketheaveragemetrics.
E AblationStudy
Weconductablationstudiesregardingthememoryretrievalmechanismtodemonstratethat(1)memory
retrieval is beneficial, (2) partial summarization of a segment in memory retrieval can speed up infer-
ence while maintaining similar effectiveness, and (3) caching more memory embedding can raise the
effectivenessofHMT.
Impact of memory retrieval mechanism. Figure 8 displays the advantages of having a memory
retrievalmechanisminHMTforlongcontextinputwithcontextswitching. Foranytestedinputlength,
theeffectivenessofHMTwithmemoryretrievaloutperformsthatwithoutmemoryretrieval. Furthermore,
when the memory retrieval mechanism is deployed, the effectiveness improves for the OPT 350M
backbone model or tends to improve for the OPT 2.7B backbone model as the input sequence length
grows,demonstratingbetterscalabilityofHMT.
Figure 9: Effectiveness of HMT with OPT 2.7B
Figure8: EffectivenessofHMTwithandwithout
when performing representation extraction on the
the memory retrieval mechanism for OPT 350M
wholesegmentforhalfofthesegment. Theimpact
and2.7Basthebackbonemodels. Theinputsare
isnegligible,justifyingthatsummarizinghalfofthe
extractedfromtheWikitext-103datasetwithupto
segmentisavalidmethodforinferenceacceleration.
100ktokens.
Impactofsummarizingpartialsegmentinmemoryretrieval. Tooverlaporreducetheinference
time ofthe previoussegment with the representation extraction of the next segment, itis necessary to
prefetch only the first l tokens in the segment for summarization. In the experiment, we select half of
thesegmentforrepresentationextraction. Weexaminethemodelthatextractsthewholesegmentand

comparetheeffectiveness,depictedbyFigure9. Theimpactisnegligible. Wehypothesizethatthestartof
asegmentcontainsenoughinformationabouttheoveralltopicformemoryretrieval,whichisintuitive
as humans can capture the concepts by browsing keywords or segments instead of reading the whole
paragraphs.
Impact of limited cached memory embeddings. Due to memory constraints, we only cache the
mostrecent300memoryembeddingsformemoryretrieval. Figure10depictstherelationshipbetween
the number of cached memory embeddings and the effectiveness of HMT with Llama 2 7B over the
Wikitext-103 dataset with 100k-token samples. We observed that increasing the window of cached
memorybenefitstheeffectiveness,buttheimprovementbecomesmarginal. WehypothesizethatHMTis
morelikelytorecallrecentmemoryembeddingsintheWikitext-103dataset. Figure11plotsthefrequency
distributionofthedistancebetweenthecurrentsegmentandthesegmentcorrespondingtothememory
embeddingwiththehighestsoftmaxscoreinthememoryretrievalmechanism. 6.5%ofthesegments
retrievememorytokenswithin2segments. Thissignalstheimportanceoflocalcontext. However,the
long-contextmemoryretrievalstillexists. ApossibleexplanationisthatentriesinWikipediamayreferto
otherentriesthroughhyperlinksandrelatedcontext,andHMTdiscoversthislong-contextrelationship
andrecallstherelevantinformation.
Inourexperiments,westorethemostrecent300memoryembeddingstobalancethetrade-offbetween
retrievaleffectivenessandcomputationalefficiency. Theoretically,storing⌈M/L⌉embeddingsissufficient
tohandleuptoM tokeninputs,ensuringrobustperformance. Forlongerinputs,high-qualityprocessing
isstillachievableifrecentcontextualinformationismorerelevanttotheprompt.
Figure10: Relationshipbetweennumberofcached
memoryembeddingsandtheeffectivenessofHMT Figure11: Histogramofcontextdistancebetween
+Llama27B.Eachsamplehas100ktokensfromthe the current segment and the segment correspond-
Wikitext-103dataset. AsHMTstoresmorememory ingtothememoryembeddingwiththehighestsoft-
embeddings,theeffectivenessismarginallybetter. maxscoreinthememoryretrievalmechanism. The
datasetevaluatedistheWikitext-103.
Figure 12: Training HMT + OPT 2.7B with the memory retrieval mechanism in two steps results in a better
performancethanusingthemechanismtotrainHMTdirectly. Totaltrainingtimeis902sformulti-stagetraining
and1680sforsingle-stagetrainingon4AMDMI210GPUs.

F Multi-stageTraining
SinceHMTintroducesparametersformemoryretrieval,weneedtotrainnewparametersandfine-tune
the parameters of the backbone model cooperatively. Training HMT involves multiple segments of
tokenstolearnhowtoencodeinputtokensandretrieveinformationproperly. Therefore,wesplittraining
HMTintotwostages. Inthefirststage,Themodelistrainedwithoutthememoryretrievalmechanism
employingBPTTwith2segmentsunrolled. BPTTsavesthemodelcheckpointlocally. Then,thememory
retrievalmechanismloadsandextendsthetrainmodelinthesecondstage. Atthispoint,BPTTtrainsthe
modifiedmodelbyunrollingthemaximumnumberofsegmentsthattheGPUscanhandletomaximize
theeffectiveness, whichis15inourexperiment. SincethearchitectureofHMTiscomplex, breaking
up training into two stages is beneficial for local optimization and improves long context inference
performancecomparedwithsingle-stagetraining. Figure12exhibitstheperformancedifferencebetween
themulti-stageandsingle-stagetrainingoftheOPT2.7BmodelwithHMTforlong-contextinputs. Since
Stage 1 involves a shorter training sequence length and a simpler recurrent architecture than Stage 2,
trainingwithStage1isfasterperiteration(1.15s/iteration)thanStage2(3.36s/iteration). Withinthe
samenumberoftrainingsteps,multi-stagetrainingobtainsbettereffectivenessandlowertotaltraining
timethansingle-stagetraining.
G HMTMemoryRetrievalBehavior
One insight of using memory retrieval in HMT is handling frequent context switching to previously
discussed topics or new topics. To evaluate this property, we employ PubMedQA and artifact the
datasetwithmultiplecontexts,mentionedinSection5.1. Inthissection,wewilldiscussotherdataset
manipulationsonPG-19toinvestigatethememoryretrievalbehaviorofHMTfurther.
Onewaytomanuallyintroducecontextswitchingisbyinterleavingthesamples. Forevery2samples
in the PG-19 dataset, we alternatively concatenate a segment of 256 tokens in each sample together
to create a new sample. Therefore, a context switch will be invoked every 256 tokens. We fine-tuned
and benchmarked HMT with Llama 2 7B over the artifact dataset. As a result, HMT can enhance the
effectiveness of the baseline Llama 2 model, while RMT will worsen it, as shown in Figure 13. We
recordthecontextdistanceofmemoryretrievalfor30k-tokeninput,illustratedinFigure14,andnoticea
periodicalrecalldistribution,indicatingthatHMTcancapturethecontext-switchingpattern.
Figure 13: Effectiveness of HMT and RMT with Figure14: Histogramofcontextdistancebetween
Llama27BevaluatedoverPG-19withinterleaving the current segment and the segment correspond-
samples. HMTis12.02%betterthanRMTinterms ingtothememoryembeddingwiththehighestsoft-
ofPPLfor2kto100k-tokensamples. maxscoreinthememoryretrievalmechanism. The
datasetevaluatedisthePG-19withinterleavingsam-
ples.
TodemonstratethatHMT’sbehaviorisalignedwiththecontext-switchingpattern,wefurthermanipu-
latethePG-19datasetbyinserting256“$"tokensforevery256tokenstodilateeachsample. Intuitively,
the segment containing “$" should be considered as irrelevant information and recalled infrequently.
Figure15showsthememoryretrievalpatternofHMTwithLlama27BoverthedilatedPG-19dataset.

We observe that HMT not only exhibits a periodical recall pattern but also successfully captures the
positionofirrelevantsegmentsandavoidsrecallingthem.
Figure 15: Histogram of context distance between the current segment and the segment corresponding to the
memoryembeddingwiththehighestsoftmaxscoreinthememoryretrievalmechanism. Thedatasetevaluatedisthe
dilatedPG-19dataset. Eachsampleis25.6ktokens.
H RelationshipsBetweenEffectivenessandSizeofSensoryMemory
During the experiment, we observed a general trend in the relationships between the effectiveness of
HMT-augmentedmodelsandthesizeofsensorymemory: theeffectivenesswillbefirstenhancedand
thendegradedasmoreandmoreembeddingsarepreservedforsensorymemory. Forinstance,Table8
illustratesthechangeofeffectivenessofHMT+Llama27BevaluatedonWikitext-103withdifferent
sensory memory sizes. The PPL drops to the minimum when having 32 embeddings for the sensory
memory.
Table8: EffectivenessofHMT+Llama27BevaluatedonWikitext-103with100k-tokensamples,withvarious
sensorymemorysizes. Thesegmentsizeis256tokens. Theeffectivenessimprovesandthendegradeswithan
increasingnumberofembeddingsthatarepreservedforsensorymemory.
#OFEMBEDDINGSFORSENSORYMEMORY TESTPPL(WIKITEXT)
| 8   |     | 4.54 |     |     |
| --- | --- | ---- | --- | --- |
| 16  |     | 4.25 |     |     |
| 32  |     | 4.19 |     |     |
| 64  |     | 4.31 |     |     |
| 128 |     | 4.57 |     |     |
I DatasetConstructionforPubMedQA
TheoriginalPubMedQAdatasetdoesnothavetraining,validation,andtestdatasetsplits. Intheexperi-
ments,wechoosethepqa_artificialsubsetandpartitionthetraining,validation,andtestsplit,where
thetrainingsplitisthefirst75%ofsamples,thevalidationsplitisthenext15%ofsamples,andthetest
splitistheremaining10%samples.
Weartifactthelong-contextdatasetfromPubMedQAasthefollowing: (1)selectM question-context-
answertuplesfromthedataset. Letthissetoftuplesbe{(C ,Q ,A ),(C ,Q ,A ),...,(C ,Q ,A )},
|     | 0 0 | 0 1 1 1 | T   | T T |
| --- | --- | ------- | --- | --- |
whereC n arecontexts,Q n arequestions,A n areanswersfor0 ≥ n ≥ M. Answerscanbeeitherlong
answers with detailed reasoning or short answers (either “yes", “no", or “maybe"). (2) Concatenate
allthecontextsfromeachtupletoformalongcontextandappendthequestionsandanswersforeach
tuple. This will create M sequences: C C ...C Q A , C C ...C Q A ,..., C C ...C Q A .
| 0 1 | T 0 0 0 1 | T 1 1 | 0 1 | T T T |
| --- | --------- | ----- | --- | ----- |

BycontrollingthevalueofM,wecandeterminethefractionofusefulinformationinthecontextforeach
questionandbetterunderstandthefilteringandselectionabilityofHMTandthebaselinemodel.
J GradientStabilityinHMTandRMT
Both HMT and RMT are trained using backward propagation through time (BPTT) (Mozer, 2013), a
techniqueutilizedtotraintheRNNmodelbyunrollingrecurrentforwardpassesofthemodeltooptimize
long-sequencelearning. OneissuewithRMTtrainingwithBPTTisthegradientexplosionandvanishing
problem. WithahigherBPTTunrolldepth,theeffectivenessofRMTwillfirstincreaseandthendecrease,
withaslowreductionorevenanincreaseintrainingloss. AsseeninFigure16,weusetheWikitext-103
datasetwithvariousBPTTunrolldepthstoaccesstheeffectivenessofRMTwiththeOPT2.7Bbackbone
model. Forboth2kand10ktokeninputs,weobservearisingPPLwhenunrollingmorethan5segments
duringtraining.
Figure16: EffectivenessoftrainingRMTwithBPTTwithdifferentunrolldepthsfor2Ktokensand10Ktokens
input from the Wikitext-103 dataset. The backbone model is OPT 2.7B, with 256 tokens per segment during
inference.
Table9: RelationshipbetweentheBPTTunrolldepthandthetestPPLofWikitext-103forOPT2.7BwithHMT.
Theexperimentisevaluatedonsampleswith10ktokens. HMTpreserved32tokensfromtheprevioussegmentas
thesensorymemoryandsaved300memoryembeddingsforthememoryretrieval. Thesegmentsizeis256tokens.
BPTTUNROLLDEPTH TESTPPL(WIKITEXT)
2 9.36
5 9.15
15 8.20
Unlike RMT, HMT does not suffer from gradient vanishing or explosion as BPTT unroll depth
increasesduetothememoryretrievalmechanism. Table9revealsthatHMTcanimproveitseffectiveness
continuouslyastheBPTTunrolldepthincreasesduringtraining. Therefore,HMTwillbemoreeffective
whentheBPTTunrolldepthincreases. AdetailedgradientstabilityanalysisispresentedinAppendixJ.
Furthermore,weappliedseveraltechniquestooptimizetheGPUmemoryconsumptiontoincreasethe
maximumtrainableBPTTunrolldepthcomparedwithRMT,describedinAppendixK.
Inthissection,wewillformulateamathematicaldescriptionforthegradientstabilityofHMTwhen
training with BPTT. BPTT with RMT behaves similarly to RNN which suffers from a vanishing or
explodinggradientwhenthereisalongchainofthegradientgraphafterunrolling(Pascanuetal.,2013).
Specifically,foragenericRNNmodelwiththefollowingform:
H = σ(AH +Bx )
t t−1 t
whereH isthehiddenstateattimeh,x istheinputattimet,andAandBareparameters,thegradient
t t
willexplodeif||AT|| > 1andviceversa. Asimilar phenomenonoccurswhentraining segment-level

Figure17:BackwardpropagationflowsofHMTandRMT.Thegradientofthefirstmemorizationpromptembedding
(theredblockontherightofthefirstsegment)hasmultiplebranchesthroughthememoryretrievalunit. Wherethe
HMTgradientdoesnotrequirepropagationthrougheachsegment,theRMTgradientdoes.
recurrentmodelssuchasRMT.Hereweprovideascratchcalculationonthegradientoflosswithrespect
tothememorytokenatthestartingtime,whichisoneoftheparametersinbothRMTandHMT,after
tstepsforRMT.Lety′ = H(x ,m )bethelogitsandm = F(x ,m )bethegeneratedmemory
| t+1 | t t | t+1 | t t |     |
| --- | --- | --- | --- | --- |
embeddingattimet,wherex istheinput,m isthememorytoken. Thelossofinferenceis
| t   | t   |     |     |     |
| --- | --- | --- | --- | --- |
L(y′
|     | L = | ,y )    |     | (6) |
| --- | --- | ------- | --- | --- |
|     | t+1 | t+1 t+1 |     |     |
Therefore,thegradientcanbecalculatedbythechainruleas
| ∂L  | ∂L ∂y′  |       |     |     |
| --- | ------- | ----- | --- | --- |
|     | t+1 t+1 | t+1   |     |     |
|     | = ×     |       |     |     |
| ∂m  | ∂y′     | ∂m    |     |     |
|     | 0 t+1   | 0     |     |     |
|     | ∂L t+1  | ∂H ∂m | t   |     |
|     | = ×     | (x )× |     |     |
|     | ∂y′ ∂m  | t ∂m  |     | (7) |
|     |         | t 0   |     |     |
t+1
t−1
|     | ∂L t+1 | ∂H (cid:89) | ∂F   |     |
| --- | ------ | ----------- | ---- | --- |
|     | = ×    | (x )×       | (x ) |     |
|     | ∂y′    | t           | i    |     |
|     | ∂m     | t ∂m        | i    |     |
|     | t+1    | i=0         |      |     |
WhetherthegradientwillexplodeorvanishdependsontheinputdistributionandthefunctionF . If
t
∂F ∂F
∀x t , (x t ) > 0,thenthegradientwillexplode. Otherwiseif∀x t , (x t ) < 0,thegradientvanishes.
∂mt ∂mt
Consequently, training RMT with a very high BPTT unroll depth can be inefficient. For HMT, with
theassistanceofthememoryretrievalmechanism,thegradientisnotpronetoexplosionorvanishing.
Intuitively,thebackwardpropagationofHMTforthememorizationpromptembeddingcontainsmultiple
short sub-branches to prevent gradient vanishing and the memory retrieval mechanism can modulate
thepropagationchaintoavoidgradientexplosion(Figure17). LetG (z ,m ,m ,...,m ) = m′ be
|     |     |     | t t t t−1 1 | t   |
| --- | --- | --- | ----------- | --- |
thememorysearchfunctionwherez istherepresentationextractionofsegmentattimet. Letsbethe
t

summarizationtokenforrepresentationextraction. ThegradientforHMTis
∂y′
∂L ∂L
| t+1 = | t+1 × | t+1 |     |     |     |     |     |     |     |     |     |
| ----- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∂y′
| ∂m  |       | ∂m  |      |     |     |     |     |     |     |     |     |
| --- | ----- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0   | t+1   | 0   |      |     |     |     |     |     |     |     |     |
|     | ∂L    | ∂H  | ∂G   |     |     |     |     |     |     |     |     |
| =   | t+1 × | (x  | )× t |     |     |     |     |     |     |     |     |
t
|     | ∂y′ ∂m′ |     | ∂m  |     |     |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | t+1     | t   | 0   |     |     |     |     |     |     |     |     |
t
|     | ∂L      | ∂H  | (cid:88) | ∂G   |           |         |        |     | ∂F  |     |     |
| --- | ------- | --- | -------- | ---- | --------- | ------- | ------ | --- | --- | --- | --- |
| =   | t+1 ×   | (x  | )×(      | t (z | ,m ,...,m | ,m      | ,...,m | )×  |     | )   | (8) |
|     |         | t   |          |      | k t       | k−1 k+1 |        | 1   |     |     |     |
|     | ∂y′ ∂m′ |     |          | ∂m   |           |         |        |     | ∂m  |     |     |
|     | t+1     | t   | k=1      | k    |           |         |        |     | 0   |     |     |
|     | ∂L      | ∂H  | t        | ∂G   |           |         |        |     | ∂F  | ∂G  |     |
|     | t+1     |     | (cid:88) | t    |           |         |        |     |     |     | t−1 |
| =   | ×       | (x  | )×(      | (z   | ,m ,...,m | ,m      | ,...,m | )×  |     | ×   | )   |
|     | ∂y′ ∂m′ | t   |          | ∂m   | k t       | k−1 k+1 |        | 1   | ∂m′ | ∂m  |     |
|     |         |     |          | k    |           |         |        |     |     |     | 0   |
|     | t+1     | t   | k=1      |      |           |         |        |     | k   |     |     |
= ...
Therootcauseofthegradientexplosionorvanishingcomesfromthelongchainofgradientproductsin
theformulation. ForHMT,therearemultipleshortbranchesofthemultiplicationchainafterexpanding
theexpression. Thelongestchainoverallcomponentsinthegradientis
t−1
|     |     | ∂L  | ∂H  |          | (cid:89) | ∂F ∂G  | ∂F  |     |     |     |     |
| --- | --- | --- | --- | -------- | -------- | ------ | --- | --- | --- | --- | --- |
|     |     |     | t+1 |          |          | k      |     |     |     |     |     |
|     |     |     | ×   | (x t )×( |          | ×      | )×  |     |     |     | (9) |
|     |     | ∂y′ | ∂m′ |          |          | ∂m′ ∂m | ∂m  |     |     |     |     |
|     |     |     | t+1 | t        |          | k k    |     | 0   |     |     |     |
k=1
∂Lt+1
For gradient vanishing, since still has components with a shorter chain, the gradient will not
∂m0
|     |     | ∂F  | ∂G  |     |     |     |     | ∂G  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
disappearevenwhen|| × k|| < 1. Forgradientexplosion,empirically, k aredifferentforeach
|     |     | ∂m′ | ∂m  |     |     |     |     | ∂m  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | k   | k   |     |     |     |     |     | k   |     |     |
k bythepropertyofcrossattentionandcanmodulatetheterm ∂F todistributenear1. Thus,HMTis
∂m
k
lesspronetogradientexplosion.
Asimilarproofcanbededucedforthesegment-levelsummarizationtokenembeddingofHMTfor
representationextraction.
K DistributedTrainingwithMemoryConsumptionOptimization
Although(Bulatovetal.,2022)provesthatunrollingmoresegmentscanimprovethemodeleffectiveness,
theylimitthenumberofsegmentsunrolledto4with2NVIDIAA10080GBGPUssincethemaximum
BPTTunrolldepthisboundedbytheGPUVRAMlimit. TherearethreesourcesofVRAMconsumption:
modelparameters,intermediatedata(inputsegments,long-termmemory,rawoutputsofeachsegment,
etc.),andoptimizationdata(gradientandoptimizerstates). Althoughthecomputationsoflatersegments
donotrequiretheintermediatedatafromtheprevioussegment,theoriginalBPTTwillkeepthemonGPU
bydefault. Toreducememoryconsumption,wecustomizetheprogramtooffloadandloadintermediate
dataforeachinputsegmentbetweentheCPUandGPUsanddistributeoptimizerstatesandgradients
throughoutmultipleGPUsrunningZeroRedundancyOptimizer(ZeRO)(Rajbhandarietal.,2020)Stage
2inDeepSpeed(Rasleyetal.,2020). Theseallowthemodeltounrollupto15segmentswithHMT.To
trainlargermodels,weemployLoRA(Huetal.,2021)withrank8. Thisallowsustofit7Bmodelsto4
MI210GPUs.
L LicenseandLinksofDatasetsandModels
Datasets:
• Wikitext (Texts from Wikipedia): CC BY-SA 4.0, https://huggingface.co/datasets/
Salesforce/wikitext
• PG-19 (Books from Project Gutenberg): Apache License V2.0, https://huggingface.co/
datasets/emozilla/pg19
• PubMedQA (Biomedical QA dataset): MIT License, https://huggingface.co/datasets/
qiaojin/PubMedQA

• RedPajamaV2 (Pretraining data corpus): Apache License V2.0, https://huggingface.co/
datasets/togethercomputer/RedPajama-Data-V2
• LongBench (Long context evaluation dataset): Licenses are mentioned in the original work (Bai
etal.,2023b),https://huggingface.co/datasets/THUDM/LongBench
Models:
• OPTmodels: MITLicense,https://huggingface.co/facebook/opt-350m
• Llama models: Llama 2 Custom License, https://huggingface.co/meta-llama/
Llama-2-7b-hf
• OpenLlamaV2: Apache License V2.0, https://huggingface.co/openlm-research/open_
llama_3b_v2
• RWKV:ApacheLicenseV2.0,https://huggingface.co/RWKV/rwkv-4-3b-pile
• Mamba: ApacheLicenseV2.0,https://huggingface.co/state-spaces/mamba-370m-hf
• Mistral: ApacheLicenseV2.0,https://huggingface.co/mistralai/Mistral-7B-v0.3
• Yi: Yi-License,https://huggingface.co/01-ai/Yi-6B-200K
• Qwen: Tongyi Qianwen License, https://huggingface.co/Qwen/Qwen1.5-0.5B, https://
huggingface.co/Qwen/Qwen2.5-14B
• SmolLM:ApacheLicenseV2.0,https://huggingface.co/HuggingFaceTB/SmolLM-135M
Alldatasetsandmodelsarepubliclyavailableandfreetouse.