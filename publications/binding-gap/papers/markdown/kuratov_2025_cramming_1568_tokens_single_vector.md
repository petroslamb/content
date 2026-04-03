| Cramming |           |     | 1568 | Tokens | into | a Single  | Vector |       | and      | Back | Again: |     |
| -------- | --------- | --- | ---- | ------ | ---- | --------- | ------ | ----- | -------- | ---- | ------ | --- |
|          | Exploring |     | the  | Limits | of   | Embedding |        | Space | Capacity |      |        |     |
YuriKuratov1,2 MikhailArkhipov3 AydarBulatov1,2 MikhailBurtsev4
1AIRI,Moscow,Russia
2NeuralNetworksandDeepLearningLab,MIPT,Dolgoprudny,Russia
3IndependentResearcher,Amsterdam,Netherlands
4LondonInstituteforMathematicalSciences,London,UK
Correspondence:yurii.kuratov@phystech.edu
Abstract
1568
1500
Arangeofrecentworksaddressestheproblem
5202 nuJ 22  ]LC.sc[  3v36031.2052:viXra
| of compression |     | of sequence | of  | tokens | into a |     | snekot ,htgnel txeT |     |     |     |     |     |
| -------------- | --- | ----------- | --- | ------ | ------ | --- | ------------------- | --- | --- | --- | --- | --- |
1250
| shorter sequence |     | of real-valued |     | vectors | to be |     |     |     |     |     | 1024 |     |
| ---------------- | --- | -------------- | --- | ------- | ----- | --- | --- | --- | --- | --- | ---- | --- |
1000
| used as           | inputs instead |                       | of token | embeddings |     |     |     |     |     |     |     |     |
| ----------------- | -------------- | --------------------- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
| orkey-valuecache. |                | Theseapproachesarefo- |          |            |     |     |     |     |     |     |     |     |
750
cusedonreductionoftheamountofcompute
512512
| in existing | language  | models | rather |        | than min- |     |     | 500   |           | 384 |     |     |
| ----------- | --------- | ------ | ------ | ------ | --------- | --- | --- | ----- | --------- | --- | --- | --- |
| imization   | of number | of     | bits   | needed | to store  |     |     |       |           |     |     |     |
|             |           |        |        |        |           |     |     | 250   | 160128128 |     |     |     |
|             |           |        |        |        |           |     |     | 80 96 |           |     |     |     |
text. Despiterelyingonpowerfulmodelsasen-
coders,themaximumattainablelosslesscom-
|     |     |     |     |     |     |     |     | m m | b b | b 4 | B B B | B   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- |
p r e s s i o n r a t i o i s t y p i c a l l y n o t h i g h e r t h a n x 1 0 . 0 0 4 8 3 2 3 1 3 8
|     |     |     |     |     |     |     |     | 1 6 4 1       | - 1 . ia- 2 . | - 1 . 0 7 - 1. | 2- 2-            | 1-  |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------- | ------------- | -------------- | ---------------- | --- |
|     |     |     |     |     |     |     |     | hia - ia- hia | p t           | B - M A        | - 3 . - 3 . - 3. |     |
T h i s f a c t i s h i g h l y i n t r i g u i n g b e c a u s e , i n t h e - h t t h o - 1 La m a m a m a
|     |     |     |     |     |     |     | pyt | y t p y p | y M | o -L la | a a |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------- | --- | --- |
o r y , t h e m a x i m u m i n f o r m a t i o n c a p a c i t y o f l a r g e p L d L L l L l
|     |     |     |     |     |     |     |     |     | O   | r e |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
e a
| re a l - v a l u | e d v e c t o | r s i s f a | r b e y o n | d t h e | p r e s e n t e d |     |     |     | h   |     |     |     |
| ---------------- | ------------- | ----------- | ----------- | ------- | ----------------- | --- | --- | --- | --- | --- | --- | --- |
S
| rates even  | for 16-bit                  | precision |     | and | a modest |        |     |          |        |     |               |       |
| ----------- | --------------------------- | --------- | --- | --- | -------- | ------ | --- | -------- | ------ | --- | ------------- | ----- |
| vectorsize. | Inthiswork,weexplorethelim- |           |     |     |          |        |     |          |        |     |               |       |
|             |                             |           |     |     |          | Figure | 1:  | How many | tokens | fit | into a single | input |
its of compression by replacing the encoder vector? Weestimatemaximumnumberoftokensthat
| withaper-sampleoptimizationprocedure. |     |     |     |     | We  |     |     |     |     |     |     |     |
| ------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
canbedecodedfromasingleinputvectoracrossvarious
| showthatvectorswithcompressionratiosup |        |            |              |     |           | languagemodels. |     |     |     |     |     |     |
| -------------------------------------- | ------ | ---------- | ------------ | --- | --------- | --------------- | --- | --- | --- | --- | --- | --- |
| to x1500                               | exist, | which      | highlights   | two | orders    |                 |     |     |     |     |     |     |
| of magnitude                           | gap    | between    | existing     |     | and prac- |                 |     |     |     |     |     |     |
| tically attainable                     |        | solutions. | Furthermore, |     | we        |                 |     |     |     |     |     |     |
empiricallyshowthatthecompressionlimits in 1B-parameter models to 16,384 float numbers
aredeterminednotbythelengthoftheinput in 405B-parameter models (Dubey et al., 2024).
butbytheamountofuncertaintytobereduced, Remarkably, even a 2,048-dimensional vector of
namely,thecross-entropylossonthissequence
|     |     |     |     |     |     | 16-bit | floats | has | a theoretical |     | capacity | of 32,768 |
| --- | --- | --- | --- | --- | --- | ------ | ------ | --- | ------------- | --- | -------- | --------- |
without any conditioning. The obtained lim- bits, which is sufficient to encode roughly 1,931
| its highlight | the | substantial | gap | between | the |        |      |              |     |     |               |      |
| ------------- | --- | ----------- | --- | ------- | --- | ------ | ---- | ------------ | --- | --- | ------------- | ---- |
|               |     |             |     |         |     | tokens | from | a vocabulary |     | of  | size 128,256. | This |
theoreticalcapacityofinputembeddingsand
|     |     |     |     |     |     | observation |     | motivates |     | us to explore | whether | lan- |
| --- | --- | --- | --- | --- | --- | ----------- | --- | --------- | --- | ------------- | ------- | ---- |
theirpracticalutilization,suggestingsignificant
guagemodelscanutilizethelatentcapacityofin-
roomforoptimizationinmodeldesign.
putvectorsmoreeffectively,potentiallyencoding
1 Introduction
andprocessingmultipletokenswithasinglevector.
Mostlargelanguagemodels(LLMs)arebuilton Encoding multiple tokens or even entire texts
theTransformerarchitecture(Vaswanietal.,2017) into a compact latent representation has been a
andhavedemonstratedremarkableperformanceas longstandingchallengeinnaturallanguageprocess-
theirparametersscale(Radfordetal.,2019;Brown ing. Itincludesapproaches,suchassentenceem-
etal.,2020;Kaplanetal.,2020;Hoffmannetal., beddings(LeandMikolov,2014;Kirosetal.,2015;
2022). As model sizes increase, so does the di- Cer et al., 2018; Wang et al., 2024) for semantic
mensionalityoftheirinputembeddings. However, searchandretrieval,andtextautoencoders(Bow-
despite this growth, each embedding still repre- manetal.,2016;Miaoetal.,2016;Monteroetal.,
sentsonlyasingletoken,e.g.,foraseriesofLlama 2021), aimed to capture the essential meaning of
models embeddings size is growing from 2,048 textsinadenserepresentations.
1

In the context of LLMs, the challenge of en- sistent across different text lengths and domains,
coding prompts and long contexts is particularly includingnaturaltextandrandomwordsequences.
importantbecauseofthequadraticcomputational 4. We introduce a set of metrics that decouple
costoftheself-attentionmechanisminTransform- thecapacityoftrainableinputvectorsfromthelan-
ers. Several works have explored the possibility guagemodel’sinherentpredictionabilities. Using
of replacing token-based prompts with a smaller thesemetrics,wedemonstrateanearlylinearscal-
set of dense vectors (Lester et al., 2021; Li and ing of compression capacity with the number of
Liang,2021;Gao,2024;Lietal.,2024b),thereby trainablevectors(e.g.,Llama-3.2-1Bcompresses
shortening the input sequence and reducing the 7,168tokensintojust16vectors).
computationalbudget. Thesemethodshavedemon- OurcodeisavailableatthisURL.
strated token-to-vector lossy compression ratios
2 RelatedWork
on the order of x500 with 8B-parameter models,
indicating that it is possible to retain the critical
Approaches to compressing LLM context into a
information in a significantly reduced number of
shortersequenceofinputorKV-cachevectorsare
vectors. However,losslesscompressionisstilllim-
exploredforvariouspurposes,yetnostandardized
itedbyapproximatelyfactorof10.
terminologyorunifiedmethodologyhasemerged.
In memory-augmented architectures (Weston
etal.,2015;Sukhbaataretal.,2015;Burtsevetal., Contextcompression. Oneapplicationforinput
2021),theseembeddingsactasadditionalstorage compression is connected with efficient process-
orasarecurrentstateforpassinginformationbe- ing of long contexts with LLMs. RMT (Bulatov
tween time steps (Dai et al., 2019; Bulatov et al., etal.,2022)andAutoCompressors(Chevalieretal.,
2022;Chevalieretal.,2023;Behrouzetal.,2024), 2023)trainthewholelanguagemodelinarecurrent
essentiallyservingasanepisodicmemory. More- mannertocompresstheinformationfrominputseg-
over, recent approaches have explored the power mentstosummaryvectorsandlaterreusethemto
oflatentspacereasoning(Haoetal.,2024)where solve long-context tasks. ICAE Ge et al. (2024)
high-capacity embeddings enable models to per- uses an autoencoder architecture with a frozen
form complex multi-step tasks directly in latent LLMasadecoderandadaptthesameLLMforthe
space. Consequently,thecapacityofthesevectors encoderusingLoRA(Huetal.,2022). Theresult-
iscrucialnotonlyforefficientinputrepresentation, ingpipelineispretrainedusingautoencodingand
butalsoforincreasingtheoverallexpressiveness languagemodelingobjectives,andthenfinetuned
and computational power of models (Merrill and for language tasks, achieving the effective com-
Sabharwal,2023;Strobletal.,2024;Sanfordetal., pression rate of x4. SelfCP (Gao, 2024) uses the
2024). Betterunderstandingofthelatentcapacity baseLLMitselfasacompressorusingatrainable
ofinputvectors,couldsignificantlyhelptoimprove adaptertoaggregatecompressedstatesacrossmul-
encodingandretrievingofcontextualinformation, tiplesegments. 500xCompressor(Lietal.,2024b)
episodic memory, as well as complex reasoning extendstheautoencodingapproachwithlayer-wise
withinlargelanguagemodels. connections and additional language pretraining
In this work, we investigate the limits of such tasks, exploring compression ratios up to x480,
input representations, exploring their capacity to though at the cost of substantial quality degrada-
encode and reconstruct long text sequences. By tion. AlternativeapproachesaimtocompressKV
systematically quantifying how much additional activations instead of input tokens. Some meth-
informationthesevectorscancapture,weprovide odsachievethisbyestimatingtokenrelevance,ei-
insightsintotheefficiencyandpotentialoflatent ther through training-free (Zhang et al., 2023; Li
representationsinLLMs. Ourmaincontributions: et al., 2024a) or training-based approaches (Qin
1. We empirically study capacity limits of andVanDurme,2023;Qinetal.,2024),topruneir-
LLM’sinputrepresentationsbycompressingtexts relevanttokensandfocuscomputationonthemost
intotrainable[mem]vectors. informativeones. Thesestrategiescanyieldhigh-
2. We establish a direct connection between qualitybutlossycompressionwithratiosuptox20.
thelatentcapacityofinputvectorsandtextcross- This result can be improved by finetuning mod-
entropy, providing a quantitative measure of the elstoleveragetheresultingcacherepresentations
informationeachvectorcanencode. moreeffectively. Thisway,KV-Distill(Charietal.,
3. Weshowthatthecapacitylimitsremaincon- 2025)canreducecachesizeupto100timeswith
2

negligiblelossinQAperformance. Incontrast,our Trainabletokens. Someworksusethetrainable
method,appliedtomodelsofcomparablesize(up input tokens in other ways. Burtsev et al. (2021)
to8billionparameters),demonstratesthatacom- uses memory tokens as additional representation
pressionrateofx1568canbeachievedwithoutany storage,Beltagyetal.(2020);Zaheeretal.(2020)
lossinreconstructionquality. use similar global tokens to enhance long-range
|                    |     |     |                       |     |     | informationflow. |     | LiandLiang(2021);Lesteretal. |     |     |     |     |
| ------------------ | --- | --- | --------------------- | --- | --- | ---------------- | --- | ---------------------------- | --- | --- | --- | --- |
| Promptcompression. |     |     | Anotherlineofworktar- |     |     |                  |     |                              |     |     |     |     |
(2021);Gao(2024);Liuetal.(2022)exploretrain-
getspromptscompressiontoreduceinferencecosts.
|     |     |     |     |     |     | able soft | prompts | as  | an alternative |     | to  | finetuning |
| --- | --- | --- | --- | --- | --- | --------- | ------- | --- | -------------- | --- | --- | ---------- |
Gisttokens(Muetal.,2023)arepromptrepresenta- modelweights. Ourfindingsabouttherepresenta-
tionscompressedbytheLLMitself,finetunedwith
tioncapacitycanrepresentthepotentialefficiency
| aspecialmask. | Gistingallowstoachieveprompt |     |     |     |     |     |     |     |     |     |     |     |
| ------------- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
limitsofsuchmethods,basedonhowfarthemodel
compression rate up to x26 with only minor loss behaviorcanbechangedusingtrainabletokens.
| in model                                  | performance.   |     | LLMLingua        | (Jiang | et al., |          |     |     |     |     |     |     |
| ----------------------------------------- | -------------- | --- | ---------------- | ------ | ------- | -------- | --- | --- | --- | --- | --- | --- |
| 2023)decouplesthecompressionoperationfrom |                |     |                  |        |         | 3 Method |     |     |     |     |     |     |
| the LLM                                   | and introduces |     | a coarse-to-fine |        | prompt  |          |     |     |     |     |     |     |
Weproposeasimpleapproachforcompressinga
compressionstrategywithabudgetcontrollerand
|                    |           |              |            |             |        | sequence    | of tokens    |        | into a      | small | set of     | "memory"    |
| ------------------ | --------- | ------------ | ---------- | ----------- | ------ | ----------- | ------------ | ------ | ----------- | ----- | ---------- | ----------- |
| token-level        | iterative | compression, |            | achieving   | up     |             |              |        |             |       |            |             |
|                    |           |              |            |             |        | vectors.    | Then         | with   | this method |       | we analyze | how         |
| to x20 compression |           | with         | negligible | performance |        |             |              |        |             |       |            |             |
|                    |           |              |            |             |        | many tokens |              | can be | stored      | and   | decoded    | from a      |
| loss. Jiang        | et al.    | (2024);      | Pan et     | al. (2024)  | extend |             |              |        |             |       |            |             |
|                    |           |              |            |             |        | small set   | of resulting |        | vectors.    | Fig.  | 2          | provides an |
thisframeworktolongcontexts,improvinginfor-
overviewofoursetup.
| mation    | retention | through       | data  | distillation. | Addi-    |     |     |     |     |     |     |     |
| --------- | --------- | ------------- | ----- | ------------- | -------- | --- | --- | --- | --- | --- | --- | --- |
| tionally, | Morris    | et al. (2023, | 2024) | show          | that the |     |     |     |     |     |     |     |
originaltextcanbereconstructednotonlyfromits
| embeddingsbutevenfromtheLM’spredictions. |     |     |     |     | In  |     |     |     |     |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
thecurrentworkweapplyaper-sampleoptimiza-
| tion process | instead | to  | explore | the fundamental |     |     |     |     |     |     |     |     |
| ------------ | ------- | --- | ------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
limitsofcompressionandestablishupperbounds
oncompressionratesthatfarexceedpriorwork.
LLM-based lossless compression pipelines. Figure2: Compressingtextintoa[mem]vector. The
Languagemodelshavealsobeeninvestigatedfor
|     |     |     |     |     |     | pre-trained | LLM | is frozen, |     | and we | only | finetune one |
| --- | --- | --- | --- | --- | --- | ----------- | --- | ---------- | --- | ------ | ---- | ------------ |
losslesstextcompression.1 LLMZip(Valmeekam or multiple [mem] vectors to decode the sequence of
|     |     |     |     |     |     | [t  | ,t ,...,t |     | ]. [mem] |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | -------- | --- | --- | --- |
et al., 2023) improves standard compression by tokens 1 2 N vectors are trained for
eachtextseparately.
rankingcandidatesusingnext-tokenprobabilities,
whileFineZip(Mittuetal.,2024)acceleratescom-
|     |     |     |     |     |     | Trainable | [mem] |     | vectors | are | inspired | by Mem- |
| --- | --- | --- | --- | --- | --- | --------- | ----- | --- | ------- | --- | -------- | ------- |
pressionthroughfine-tuninganddynamiccontext
|                                |     |     |     |                 |     | ory Transformers |     | (Burtsev |     | et al., | 2021), | but here |
| ------------------------------ | --- | --- | --- | --------------- | --- | ---------------- | --- | -------- | --- | ------- | ------ | -------- |
| managementforbetterefficiency. |     |     |     | Thecapabilities |     |                  |     |          |     |         |        |          |
thesevectorsaredesignedtoencodeanentiretext
ofLLMsincompressionpipelinescanbemeasured
|     |     |     |     |     |     | sequence. | ThetrainingmethodissimilartoPrompt |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | ---------------------------------- | --- | --- | --- | --- | --- |
inbits-per-tokenoverarepresentativetextualcor-
|     |     |     |     |     |     | Tuning | (Lester | et al., | 2021), | with | only | a set of |
| --- | --- | --- | --- | --- | --- | ------ | ------- | ------- | ------ | ---- | ---- | -------- |
pus. Huangetal.(2024);Guoetal.(2024)provide
specialinputembeddingsoptimizedwhileallpa-
| such measurements |     | for | public | LLMs | and estab- |     |     |     |     |     |     |     |
| ----------------- | --- | --- | ------ | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- |
rametersofthelanguagemodelarefrozen.
lishtheconnectionbetweencompressionrateand
|                    |                                |          |             |            |             | Formally,    |     | given     |           | a token   |       | sequence    |
| ------------------ | ------------------------------ | -------- | ----------- | ---------- | ----------- | ------------ | --- | --------- | --------- | --------- | ----- | ----------- |
| model performance, |                                | measured |             | by diverse | bench-      |              |     |           |           |           |       |             |
|                    |                                |          |             |            |             | [t ,t ,...,t |     | ], we     | introduce |           | a set | of train-   |
|                    |                                |          |             |            |             | 1 2          | N   |           |           |           |       |             |
| markscores.        | Unlikethesemethods,wedonotrely |          |             |            |             |              |     |           |           |           |       |             |
|                    |                                |          |             |            |             | able vectors |     | [mem]     | =         | [m ,...,m |       | ] that are  |
| on external        | compression                    |          | algorithms. |            | Instead, we |              |     |           |           | 1         | K     |             |
|                    |                                |          |             |            |             | prepended    | to  | the text. | These     | [mem]     |       | vectors are |
achievelosslesscompressionusingonlytheLLM
|     |     |     |     |     |     | optimized | to  | encode | [t 1 | ,t 2 ,...,t | N   | ]. During |
| --- | --- | --- | --- | --- | --- | --------- | --- | ------ | ---- | ----------- | --- | --------- |
itself,providingboththeoreticalinsightsandprac-
|     |     |     |     |     |     | training, | the | frozen | language |     | model | processes |
| --- | --- | --- | --- | --- | --- | --------- | --- | ------ | -------- | --- | ----- | --------- |
ticaldemonstrationsofcompressionlimits.
|     |     |     |     |     |     | [m ,...,m |     | ,t ,t | ,...,t | ] as | the input | context |
| --- | --- | --- | --- | --- | --- | --------- | --- | ----- | ------ | ---- | --------- | ------- |
|     |     |     |     |     |     | 1         | K   | 1 2   |        | i    |           |         |
1Delétangetal.(2024)exploredatacompression(textsto forpredictingnexttokent i+1 . The[mem]vectors
sequencesofbits)usingArithmeticCodingandLLMs.This are optimized by minimizing the standard next-
lineofresearchisorthogonaltoours,asthesequenceofbits
|     |     |     |     |     |     | token prediction |     | cross-entropy |     |     | loss. | As a result, |
| --- | --- | --- | --- | --- | --- | ---------------- | --- | ------------- | --- | --- | ----- | ------------ |
cannotbepassedasaninputtoanLLM.Weanalyzeourap-
proachfromthedatacompressionperspectiveinAppendixF. each text sequence is associated with a unique
3

set of [mem] vectors. At inference time, we start Viewedthroughaninformation-theoreticlens,this
generation with the learned [mem] tokens and let differencequantifiesthenumberoftokens’worth
LMtodecodethetext. ofinformation(i.e.,discreteunits)thatthememory
Let’sestimateanupperboundonthenumberof vectoraddstothedecodingprocess.
tokens that can be generated from a single input Information Gain: Cross-entropy measures
vectorbyalanguagemodel. Theinputvectorhasa the uncertainty or the average number of bits
dimensiond ,witheachelementrepresented required to encode a sequence under a given
model
by b bits, so that the total information content is model. TheInformationGainquantifieshowmuch
approximately d × b bits. Given a vocabu- the [mem] vector reduces this uncertainty. Let
model
|     |     |     |     |     |     |     |     | (cid:0) | (cid:1) |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------- | --- | --- | --- |
laryofsize|V|,whereeachtokencarriesatmost H = H P (t ) be the cross-entropy (in
|     |     |     |     |     |     |     | LM  | θ   | [1:N] |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
log |V|bitsofinformation,themaximumnumber bits) when decoding without the memory vector,
2
oftokensLthatcanbegeneratedisboundedby: and H = H (cid:0) P (t | [mem]) (cid:1) be the
|     |     |     |         |     |     |     | LM+[mem]                          |     |     | θ [1:N] |     |          |
| --- | --- | --- | ------- | --- | --- | --- | --------------------------------- | --- | --- | ------- | --- | -------- |
|     |     |     |         |     |     |     | cross-entropywiththememoryvector. |     |     |         |     | Then,the |
|     |     |     | d model | ×b  |     |     |                                   |     |     |         |     |          |
|     |     | L ≤ |         | .   |     | (1) |                                   |     |     |         |     |          |
reductionisgivenby
|     |     |     | log | |V| |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2
| Our goal      | is to          | quantify | the  | capacity   | of       | trainable |               |     |          |       |          |            |
| ------------- | -------------- | -------- | ---- | ---------- | -------- | --------- | ------------- | --- | -------- | ----- | -------- | ---------- |
|               |                |          |      |            |          |           | CE-reduction  |     | = C      | = H   | −H       | . (4)      |
|               |                |          |      | [mem])     |          |           |               |     | H        | LM    | LM+[mem] |            |
| input vectors |                | (denoted | as   |            | in terms | of the    |               |     |          |       |          |            |
| amount        | of information |          | they | can encode |          | and later |               |     |          |       |          |            |
|               |                |          |      |            |          |           | This measures |     | how many | fewer | bits     | are needed |
decode. Fromaninformation-theoreticstandpoint, torepresentthetext,thusreflectingtheadditional
we interpret this capacity as the ability to reduce informationprovidedbythememoryvector.
| uncertaintyinthegeneratedtext. |     |     |     |     | Tothisend,we |     |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
Collectively,thesemetricsenableustocharac-
definethefollowingmetrics.
|     |     |     |     |     |     |     | terize the | capacity | of the | trainable | input | vectors |
| --- | --- | --- | --- | --- | --- | --- | ---------- | -------- | ------ | --------- | ----- | ------- |
Decoding Capacity (in Tokens): From an both in terms of discrete tokens (C ) and en-
tokens
information-theoreticperspective,thismetricrep- tropy (C ), while L provides an upper bound
|     |     |     |     |     |     |     |     | H   | max |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
resentsthemaximumnumberoftokensthatcanbe
onthelengthoftextthatcanbeaccuratelyrecon-
reliablyreconstructedfromthecompressedrepre- structed. In our experiments, these measures are
sentationinthe[mem]vectors. Itisdefinedasthe computedoveracuratedsetoftextsandaveraged
longesttextsequencelengthLforwhichthetoken-
|     |     |     |     |     |     |     | to obtain | robust | estimates. | We  | note | that the ab- |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------ | ---------- | --- | ---- | ------------ |
levelaccuracyexceedsapredefinedthreshold: solute values of Information Gain depend on the
|     |       |           |     |     |     |     | underlying | vocabulary, |     | and therefore |     | should not |
| --- | ----- | --------- | --- | --- | --- | --- | ---------- | ----------- | --- | ------------- | --- | ---------- |
| L   | = max | (cid:8) L | |   |     |     |     |            |             |     |               |     |            |
max
bedirectlycomparedacrossmodelswithdifferent
|           |     | (cid:0)  |       |                 | (cid:1) | (cid:9)   |               |     |     |     |     |     |
| --------- | --- | -------- | ----- | --------------- | ------- | --------- | ------------- | --- | --- | --- | --- | --- |
|           | Acc | LM(t     |       | | [mem])        | >       | thr , (2) |               |     |     |     |     |     |
|           |     |          | [1:L] |                 |         |           | vocabularies. |     |     |     |     |     |
| here, Acc | is  | computed | via   | teacher-forcing |         | when      |               |     |     |     |     |     |
4 ExperimentsandResults
| decoding | text | both | with | and without | the | [mem] |     |     |     |     |     |     |
| -------- | ---- | ---- | ---- | ----------- | --- | ----- | --- | --- | --- | --- | --- | --- |
vectors. Thismeasurereflectstheeffectivestorage
Weevaluatecapacityoftrainableinputvectorsof
limit(intokens)imposedbythefixedcapacityof thesamesizeasdimensionofinputembeddingsfor
thememoryvector.
differentlanguagemodelsontextsfromdifferent
| Token | Gain: | This | metric | estimates |     | the addi- |     |     |     |     |     |     |
| ----- | ----- | ---- | ------ | --------- | --- | --------- | --- | --- | --- | --- | --- | --- |
sources.
| tional number |     | of tokens |     | that can | be correctly | de- |     |     |     |     |     |     |
| ------------- | --- | --------- | --- | -------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
codedduetothepresenceofthe[mem]vector,rel- Models WeusemodelsfromPythiasuite(160M,
ativetothebaselineperformanceofthelanguage 410M,1.4B,2.8B)(Bidermanetal.,2023),OPT-
Formally,ifCLM+[mem] 1.3B(Zhangetal.,2022),OLMo-1B(Groeneveld
| model(LM)withoutit. |     |     |     |     |     | is  |     |     |     |     |     |     |
| ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tokens
|     |     |     |     |     |     |     | et al., 2024), | Sheared-LLaMA-1.3B |     |     |     | (Xia et al., |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ------------------ | --- | --- | --- | ------------ |
thecountoftokenscorrectlypredictedwhenusing
thememoryvectorandCLM isthecountwithout 2024), Llama-3 models (1B, 3B, 8B) (Dubey
tokens
|     |     |     |     |     |     |     | et al., 2024), | and | Mamba | (130M, | 370M, | 790M, |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ----- | ------ | ----- | ----- |
it,thenthegainisgivenby
|     |     |     |     |     |     |     | 1.4B)(GuandDao,2024). |     |     | Listofallusedmodels |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | ------------------- | --- | --- |
CLM+[mem]−CLM
| C tokens | =   |        |     |        |     |     |                                          |     |     |     |     |     |
| -------- | --- | ------ | --- | ------ | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- |
|          |     | tokens |     | tokens |     |     | withlinkstoHuggingFaceHubareinAppendixA. |     |     |     |     |     |
N
|     | (cid:88) | (cid:16) |     |     |     | (cid:17) |     |     |     |     |     |     |
| --- | -------- | -------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
= 1 t = LM(t | [mem]) Data As a source of texts for compression, we
|     |     |     | i   | [1:i−1] |     |     |                                             |     |     |     |     |     |
| --- | --- | --- | --- | ------- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- |
|     | i=1 |     |     |         |     |     | usetextsfromthePG-19dataset(Raeetal.,2020), |     |     |     |     |     |
whichconsistsofbooksextractedfromtheProject
|     |     | N   | (cid:16) |     | (cid:17) |     |     |     |     |     |     |     |
| --- | --- | --- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
(cid:88)
− 1 t = LM(t ) . (3) Gutenberg library. Given that PG-19 is publicly
|     |     |     | i   | [1:i−1] |     |     |                                               |     |     |     |     |     |
| --- | --- | --- | --- | ------- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- |
|     |     | i=1 |     |         |     |     | availableandcontainsbooks,itishighlyplausible |     |     |     |     |     |
4

Pythia-160M Pythia-410M Pythia-1.4B Llama-3.2-1B Llama-3.2-3B Llama-3.1-8B
|     | Max,tokens |     | 80  |     | 96  |     | 160 | 512 |     | 1024 | 1568 |
| --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- |
PG-19 Gain,tokens 70.9±11.0 81.3±12.0 158.0±29.1 426.2±79.2 720.3±80.2 1094.1±127.6
InformationGain 396.4±46.0 431.4±51.6 792.8±143.4 2119.9±364.8 3292.2±320.0 4865.7±546.6
|     | Max,tokens |     | 80  |     | 96  |     | 192 | 512 |     | 1024 | 1568 |
| --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- |
Fanfics Gain,tokens 70.9±10.5 81.2±11.6 152.9±28.0 449.6±83.7 734.1±85.0 1071.8±168.6
InformationGain 378.1±45.9 429.8±46.2 776.9±132.5 2213.8±365.8 3354.5±344.9 4768.9±622.6
|     | Max,tokens |     | 65  |     | 72  |     | 139 | 316 |     | 460 | 792 |
| --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Random Gain,tokens 61.3±6.6 76.9±8.7 144.4±17.5 294.9±64.8 456.9±72.1 623.2±97.3
InformationGain 500.8±38.9 630.4±65.2 1108.2±136.2 2265.2±498.7 3382.6±585.2 4541.2±758.6
Table1: Compressioncapacityacrossdifferenttextsourcesandmodels. WereportDecodingCapacity(in
Tokens)("Max,tokens"intheTable),TokenGain,andInformationGainfortextsfromPG-19,fanfics,random.
Notably,InformationGainremainssimilaracrossalltextsourcesforeachmodel(exceptrandomforPythia). For
PG-19andfanfics,LMsleveragetheirabilitytopredictnaturallanguage,sotheDecodingCapacity(inTokens)
generally exceeds the Token Gain. Furthermore, we find no evidence that the models benefit from potentially
havingPG-19intheirpre-trainingdata,astheirperformanceonPG-19isnotsignificantlybetterthanonfanfics
publishedafterOctober2024. Incontrast,randomtextoffersnopredictablestructure,makingthesetwometrics
nearlyidentical. Thisallowsustodistinguishhowmanytokensmodelcanpredictbyitselfcomparedtodecoding
fromtrainableinputvector. Largermodelsconsistentlyshowgreatercompressioncapacityacrossallmetrics.
that these texts were included in the pre-training thresholdof0.99andevaluateacrossthefollowing
dataofLLMs. Notably, PG-19ispartofthePile lengthgrid: [64, 80, 96, 128, 160, 192, 256, 384,
dataset(Gaoetal.,2020),whichwasusedtotrain 512,768,1024,1280,1568,2048,2560,3072].
| Pythiamodels. |     |     |     |     |     |     | Fig.1presentstheresultsfortheevaluatedmod- |     |     |     |     |
| ------------- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- |
Toassessthecompressionoftextsthatmodels
|     |     |     |     |     |     |     | els. Notably,Llama-3.1-8Bcanaccuratelyrecon- |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- |
havenotencounteredduringpre-training,wecol- structtextsofupto1568tokensfromjustasingle
lectedfanfictiontextspublishedonlineafterOcto- input vector. Interestingly, among models with
ber2024fromtheAO3fanficslibrary2.
|     |     |     |     |     | Detailsof |     | around | 1B  | parameters | (Pythia-1.4B, | OPT-1.3B, |
| --- | --- | --- | --- | --- | --------- | --- | ------ | --- | ---------- | ------------- | --------- |
thiscollectionprocessareprovidedinAppendixB. OLMo-1B,Sheared-LLaMA-1.3B,andLlama-3.2-
Both the PG-19 and fanfics consist of natural 1B)weobservecompressivecapacitythatranges
languagetexts,wherelanguagemodelscanpredict from 128 to 512 tokens. Pythia-2.8b, despite its
sometokensbasedonpriorcontextandmodelpa- largersize,haspoorcompressionofjust128tokens
rameters. To isolate the capacity of the trainable comparedtosmaller1Bmodels.
| input | vectors | without | the influence |     | of the | knowl- |     |     |     |     |     |
| ----- | ------- | ------- | ------------- | --- | ------ | ------ | --- | --- | --- | --- | --- |
edgeofnaturallanguagebylanguagemodelitself, 4.2 Memorization,NaturalLanguage
we also employed random texts. Random texts UnderstandingandEpisodicMemory
weregeneratedbyrandomlysamplingwordsfrom
thetop100,000wordsfromtheGloVevocabulary3. Generationfromthe[mem]vectorinvolvescombin-
inginformationfromboththepre-trainedlanguage
| We  | train only | a   | set of | M vectors | that | are |     |     |     |     |     |
| --- | ---------- | --- | ------ | --------- | ---- | --- | --- | --- | --- | --- | --- |
modelparametersandmemoryabouttextspecific
| prepended    | to  | the model’s |          | input.    | In most | of the |           |                                      |     |     |     |
| ------------ | --- | ----------- | -------- | --------- | ------- | ------ | --------- | ------------------------------------ | --- | --- | --- |
|              |     |             |          |           |         |        | sequence. | Toanalyzecontributionsofthesediffer- |     |     |     |
| experiments, | we  | use         | only one | trainable | vector, | if     |           |                                      |     |     |     |
enttypesofmemory,weuseTokenGain(Eq.(3))
notstatedotherwise.
|     |     |     |     |     |     |     | which  | measure    | the | extra number | of tokens pre- |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---------- | --- | ------------ | -------------- |
|     |     |     |     |     |     |     | dicted | correctly, | and | Information  | Gain (Eq. (4)) |
4.1 DecodingCapacityofaSingleVector
showingthedecreaseincross-entropywhendecod-
| We find | that a | single | trainable | vector | can | enable |                      |     |     |                      |     |
| ------- | ------ | ------ | --------- | ------ | --- | ------ | -------------------- | --- | --- | -------------------- | --- |
|         |        |        |           |        |     |        | ingfrommemoryvector. |     |     | IncontrasttoDecoding |     |
languagemodelstoproducesurprisinglylong,tar-
Capacity,thesetwometricsmoredirectlyisolate
| geted | text sequences. |     | We estimate |     | Decoding | Ca- |     |     |     |     |     |
| ----- | --------------- | --- | ----------- | --- | -------- | --- | --- | --- | --- | --- | --- |
thecapacitycontributedbythe[mem]vectoritself.
pacity(inTokens)(Eq.(2))on50textsfromPG-19
|          |         |     |       |             |          |     | In addition |     | to texts | from PG-19 | that may have |
| -------- | ------- | --- | ----- | ----------- | -------- | --- | ----------- | --- | -------- | ---------- | ------------- |
| for each | length. | We  | set a | token-level | accuracy |     |             |     |          |            |               |
beenseenbyLMsduringpre-training,weconsider:
|     |     |     |     |     |     |     | (1)textsfrom |     | fanficstofactoroutmemorizationas |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | -------------------------------- | --- | --- |
2https://archiveofourown.org/
3https://nlp.stanford.edu/data/glove.6B.zip theywerepublishedafterreleaseofthemodels,and
5

Texts from PG-19 Random text (sampled words) All texts below the line are losselessly compressed
|     |     | pythia-160m    |     |     |      | pythia-410m    |     |      | pythia-1.4b    |     |     |
| --- | --- | -------------- | --- | --- | ---- | -------------- | --- | ---- | -------------- | --- | --- |
|     |     |                |     |     | 6000 |                |     | 5000 |                |     |     |
|     |     | y = x + -396.4 |     |     |      | y = x + -431.4 |     |      | y = x + -792.8 |     |     |
2000
|     |     |     |     |     | 5000 |     |     |     |     |     | 3000 |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | ---- |
4000
|     | 1500 |     |     |     | 4000 |     |     |     |     |     |     |
| --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
3000
|     |     |     |     |     | 3000 |     |     |     |     |     | 2500 |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | ---- |
yportnE-ssorC ,txet desserpmoceD 1000
2000
2000
500
1000
|     |     |     |     |     | 1000 |     |     |     |     |     | 2000 Text Length, tokens |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | ------------------------ |
0
|     |     |     |           |     | 0   |        |           | 0   |        |      |     |
| --- | --- | --- | --------- | --- | --- | ------ | --------- | --- | ------ | ---- | --- |
|     |     | 0   | 1000 2000 |     |     | 0 2000 | 4000 6000 |     | 0 2000 | 4000 |     |
1500
|     |     | Llama-3.2-1B |     |     |     | Llama-3.2-3B |     |     | Meta-Llama-3.1-8B |     |     |
| --- | --- | ------------ | --- | --- | --- | ------------ | --- | --- | ----------------- | --- | --- |
8000 y = x + -2119.9 6000 y = x + -3292.2 4000 y = x + -4865.7
|     |      |     |     |     | 5000 |     |     |      |     |     | 1000 |
| --- | ---- | --- | --- | --- | ---- | --- | --- | ---- | --- | --- | ---- |
|     | 6000 |     |     |     |      |     |     | 3000 |     |     |      |
4000
2000
|     | 4000 |     |     |     | 3000 |     |     |     |     |     | 500 |
| --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
2000
1000
2000
1000
|     |     | 0   |     |     | 0   |     |     | 0   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0 2500 5000 7500 10000 0 2500 5000 7500 10000 0 2000 4000 6000 8000
Text, Cross-Entropy
Figure3: Informationgainoftextcompressionto[mem]vectordoesn’tdependonlanguageunderstanding
capabilitiesofmodels. Compressionresultsforvariouslanguagemodelsshowtherelationshipbetweenthecross-
entropy(CE)oftheoriginalanddecompressedtexts. IfthetextCEfallsbelowamodel-specificthreshold(redline),
thetextislosslesslycompressed. Thisvalueisainputvectorcapacityintermsofentropy(InformationGain,C H ).
Fortextsthatarenotperfectlycompressed,thecompressionprocessreducestheirCEtoaconsistent,model-specific
value(biasoftheblackdashedline). Largermodels(e.g.,Llama-3.1-8B)canhandlelongertextsbeforereaching
thecompressionthreshold,duetotheirgreatercapacitycomparedtosmallermodels(e.g.,Pythia-160M).This
behaviorholdsforbothnaturaltexts(PG-19)andunnaturalrandomtextsconsistingofrandomwordsequences.
(2)randomsequensesofwordstoexcludelearned model’s compression ability does not depend on
naturallanguageunderstandingcapabilities. familiaritywithspecifictextsorknowledgeofnat-
|     |          |          |     |         |           |      | urallanguagegainedduringpre-training. |     |     |     | Instead, |
| --- | -------- | -------- | --- | ------- | --------- | ---- | ------------------------------------- | --- | --- | --- | -------- |
|     | Decoding | Capacity | (in | Tokens) | for texts | from |                                       |     |     |     |          |
PG-19andfanficswasevaluatedonthefollowing thesingletrainablevectoritselfprovideslanguage
lengthgrid: [64, 80, 96, 128, 160, 192, 256, 384, agnosticsubstantialcapacity,allowingtostorecom-
pletelynoveltextsorrandomsequencesofwords.
512,768,1024,1280,1568,2048,2560,3072].
Table1summarizestheresultsforeachmodel
4.3 SensitivityofCompressiontoText
| and | text | source. We | have | two main | observations. |     |     |     |     |     |     |
| --- | ---- | ---------- | ---- | -------- | ------------- | --- | --- | --- | --- | --- | --- |
Complexity
ThemetricsforbothPG-19andfanficsareremark-
ably similar across all models tested. This sim- Decodingcapacitymightdependonthecomplex-
ilarity implies that the presence of PG-19 in the ityoftheinputtextforalanguagemodel. Inthis
pre-trainingdatadoesnotprovidemuchofanad- section,westudyhowcompressionchangesuncer-
vantage. Thus,compressionperformancedoesnot taintyofthemodelaboutthetext.
appeartobedrivenbydirectmemorizationofthe For50textsamplesfromthePG-19ateachtar-
dataset. Notably, even for random texts, larger getlength(rangingfrom8upto1568tokens,andto
modelssuchasLlama-3.1-8Bstillexhibitsubstan-
3072forlargermodels)wemeasuredcross-entropy
tialcompressingpower,reliablyreconstructingse- bothbefore(H )andafter(H )compres-
|     |     |     |     |     |     |     |     |     | LM  | LM+[mem] |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- |
quences of up to 792 tokens. This result demon- sion(seeEq.(4)). Figure3comparesresultsacross
strates the impressive capacity of learnable input PythiaandLLamamodels,andfullresultsforall
| embeddingstocontrolLLMgeneration. |     |     |     |     |     | Inpartic- |     |     |     |     |     |
| --------------------------------- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- |
modelsareprovidedinAppendixD.
ular, a single learned vector is sufficient to guide In Fig. 3, the models demonstrate linear rela-
generationofnearly800randomtokens. tionship between cross-entropy before and after
A key takeaway from these results is that the compression for not perfectly compressible texts
6

| )snekoT ni( yticapaC gnidoceD | 7000              |     | 35000 |     |
| ----------------------------- | ----------------- | --- | ----- | --- |
| 8000                          | pythia-160m       |     |       |     |
| 7000                          | 6000 Llama-3.2-1B |     | 30000 |     |
niaG noitamrofnI
| 6000 | 5000 |     | 25000 |     |
| ---- | ---- | --- | ----- | --- |
niaG nekoT
| 5000 | 4000 |     | 20000 |     |
| ---- | ---- | --- | ----- | --- |
4000
|     | 3000 |     | 15000 |     |
| --- | ---- | --- | ----- | --- |
3000
|     | 2000 |     | 10000 |     |
| --- | ---- | --- | ----- | --- |
2000
| 1000 | 1000 |     | 5000 |     |
| ---- | ---- | --- | ---- | --- |
| 0    | 0    |     |      |     |
0
0 4 8 12 16 20 24 28 32 2 4 6 8 10 12 14 16 2 4 6 8 10 12 14 16
Number of Trainable Input Vectors (N)
Figure4: Compressionscaleslinearlywiththenumberoftrainable[mem]vectors. Dashedlinesrepresent
ideallinearscaling,andshadedregionsindicate±1std. Pythia-160mreachesitsmaximuminputcontextlengthof
2048tokensandcansuccessfullyencodetextsofupto2016tokensinto32[mem]inputvectors. Llama-3.2-1Bcan
perfectlydecodetextsof7168tokensfromjust16inputvectors.
(i.e., lying above the red dotted line), indicating just 16 input vectors. However, scaling behavior
constant value of information gain (or, reduction forLlaMA-3.2-1Bdeviatesfromthelineartrend,
incross-entropy). Textswithcross-entropylower suggestingpotentialinefficienciesinthecompres-
than a model’s information gain are perfectly re- sion process or inherent model limitations in ex-
| constructed. |     | ploitinganincreasingnumberofinputvectorsfor |     |     |
| ------------ | --- | ------------------------------------------- | --- | --- |
Toverifythatthisalsoholdsforarbitrarytexts, informationstorageandextraction.
we used random word sequences and observed a Extrapolatingfromthesetrends,weestimatethat
similarpattern: aslongascross-entropyofasam- an entire text such as "The Hobbit, or There and
pleremainsbelowthemodel-specificcutoff,itcan BackAgain"(approximately120,000tokens)could
beperfectlyreconstructed. Notably,theserandom be compressed into only 128 input vectors using
texts (black dots in Fig. 3) lie very close to the Llama-3.1-8B and into 256 vectors using Llama-
| samelineartrendasthePG-19texts,showingthat |     | 3.2-1B. |     |     |
| ------------------------------------------ | --- | ------- | --- | --- |
similar compression laws apply regardless of the These results demonstrate that increasing the
natureofthesequence. Thus, [mem]worksasan numberoftrainable[mem]vectorssignificantlyen-
episodic memory storing sequence specific infor- hances compression capacity, with linear scaling
mationindependentofnaturallanguageknowledge observedacrosstheevaluatedmodels. Notably,us-
| themodelhas. |     | ingasmallnumberofadditionalvectorsintroduces |          |                |
| ------------ | --- | -------------------------------------------- | -------- | -------------- |
|              |     | minimal computational                        | overhead | while enabling |
4.4 ScalingCompressionwithMoreTrainable
thereconstructionofsubstantiallylongertexts.
Vectors
Toexplorehowcompressionscaleswiththenum- 4.5 EmbeddingCapacityUtilization
ber of input vectors [mem] = [m ,...,m ] we Tomeasurehoweffectivelyeachmodelusesitsin-
1 K
usethesametrainingprocessasbeforebutfordif- putembeddingspace,wecomparetheempirically
ferent numbers of trainablevectors, from1 to 16 measuredcapacityintokens(TokenGain)toatheo-
fortheLlama-3.2-1Bmodelandfrom1to32for reticalmaximumderivedfromembeddingsizeand
| Pythia-160M. |     | vocabularysize(seeEq.(1)). |     | Wedefinecapacity |
| ------------ | --- | -------------------------- | --- | ---------------- |
Theresultsofthisseriesofexperimentsarepre- utilizationastheratioofthesetwoquantities.
sented in Fig. 4, demonstrating that input vector InFig.5(top),whencomparingallmodelswith
capacity scales almost linearly with the number roughly1Bparameters,therearetwogroups: (1)
of trainable [mem] vectors. This trend holds con- older models (e.g., OPT and Pythia) show lower
sistentlyacrossallmeasuresofcapacity,whether capacity utilization, whereas (2) newer models
expressed in terms of tokens or text entropy. In (e.g.,Llama,ShearedLlama,Mamba,andOLMo)
particular,Pythia-160Msuccessfullydecodestexts demonstrate higher utilization despite having the
upto2016tokensinlengthusing32[mem]vectors, sametheoreticalcapacity. Thisdisparityindicates
effectively reaching its maximum context length. thatthequalityofpre-training(data,computebud-
Similarly, LlaMA-3.2-1B achieves perfect recon- get, improvementsinarchitecture)influencesthe
structionforsequencesaslongas7168tokenswith extenttowhichamodelcanexploititsinputvectors
7

bythelargermodelsduringpre-training,buteven
|     | Pythia-160M |     | OLMo-1B |     |     | Mamba-130M |     |     |     |     |     |     |
| --- | ----------- | --- | ------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
onrandomtextsweobserveamodestupwardtrend.
|     | Pythia-410M |     | Sh.Llama-1.3B |     |     | Mamba-370M |     |     |     |     |     |     |
| --- | ----------- | --- | ------------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
Pythia-1.4B Llama-3.2-1B Mamba-790M Thisresultsuggeststhattheoverallnumberofpa-
|     | Pythia-2.8B |     | Llama-3.2-3B |     |     | Mamba-1.4B |          |                    |     |      |                |     |
| --- | ----------- | --- | ------------ | --- | --- | ---------- | -------- | ------------------ | --- | ---- | -------------- | --- |
|     |             |     |              |     |     |            | rameters | plays an important |     | role | in determining |     |
|     | OPT-1.3B    |     | Llama-3.1-8B |     |     |            |          |                    |     |      |                |     |
effectivecapacitynotonlyviaLMcapabilitiesbut
snekot ,yticapaC .roehT xaM
|     | 4000 |     |     |     |     |     | also due                       | to better utilization |     | of embedding |     | space |
| --- | ---- | --- | --- | --- | --- | --- | ------------------------------ | --------------------- | --- | ------------ | --- | ----- |
|     | 3500 |     |     |     |     |     | forepisodicinformationstorage. |                       |     |              |     |       |
3000
|     |     |     |     |     |     |     | 4.6 Non-TransformerModels: |     |     |     | Mamba |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | --- | ----- | --- |
2500
|     | 2000 |     |     |     |     |     | Notably,thefindingsfromtheprevioussectionsare |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- |
notlimitedtoTransformer-basedlanguagemodels.
1500
|     |     |     |     |     |     |     | State-space | Mamba | models | can | also | encode an |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | ------ | --- | ---- | --------- |
1000
entiretextintoasingle[mem]vectorandperfectly
|     |     | 200 | 400 | 600 | 800 | 1000 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
Gain in Correctly Decoded Tokens, PG-19 reconstruct the text when its cross-entropy falls
belowthemodel’scapacitythreshold,e.g.,Mamba-
0.30
|     |     | PG-19 |     |     |     |     | 1.4Bcanencodetextsof512tokensintoasingle |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- |
noitazilitU yticapaC
Random
|     | 0.25 |     |     |     |     |     | [mem]vector,similartoother1Bmodels(Llama- |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- |
3.2-1B,Sheared-LLaMa-1.3B).Thisdemonstrates
0.20
thatobtainedresultsarearchitecture-agnostic.
0.15
Oncapacityutilization(Fig.5),theMambamod-
0.10
elsexhibitaconsistentpatternacrossbothpanels
|     | 0.05 |          |        |            |          |                  | thatdependsonmodelsize.                      |     |     | Inthetopplot,thein- |     |     |
| --- | ---- | -------- | ------ | ---------- | -------- | ---------------- | -------------------------------------------- | --- | --- | ------------------- | --- | --- |
|     | 0.00 |          |        |            |          |                  | creaseincorrectlydecodedtokensisnearlylinear |     |     |                     |     |     |
|     |      | M M B    | B B    | B B        | B B B    | M M M B          |                                              |     |     |                     |     |     |
|     | 6    | 0 1 0 .4 | .8 . 3 | - 1 .3 - 1 | -3 -8 13 | 0 37 0 90 ba-1.4 |                                              |     |     |                     |     |     |
-1 -4 -1 ia-2 PT-1 M o -1 .2 .2 .1 7 with respect to each model’s theoretical capacity.
|     | Pythia | a th ia th | L       | m a a - 3 a - | 3 a - 3 a - | a - a- |     |     |     |     |     |     |
| --- | ------ | ---------- | ------- | ------------- | ----------- | ------ | --- | --- | --- | --- | --- | --- |
|     | th     | i y Py     | O O Lla | m m           | m m b m b   | m b m  |     |     |     |     |     |     |
Py P . la la la a a a M a Thisimpliesthateachadditionalparameterinthe
|     |     |     | S h | L L L | M M M |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ----- | ----- | --- | --- | --- | --- | --- | --- | --- |
embeddingspacetranslatesintogreaterdecoding
Figure5: Onlyfractionoflearnedinputembedding accuracy at a nearly constant rate. In the bottom
informationcapacitycanbeutilized. Top. Maximum plot,capacityutilizationrisesmonotonicallyfrom
tokencapacity(seeEq.(1))againstgainincorrectlyde- the130Mtothe1.4Bmodel. Thisistheopposite
codedtokensshowsdifferencesinutilizationoflearned of the downward trend seen in Pythia, but aligns
| memoryembeddingforstudiedmodels. |     |     |     |     |     | Bottom. Capac- |             |           |      |        |        |      |
| -------------------------------- | --- | --- | --- | --- | --- | -------------- | ----------- | --------- | ---- | ------ | ------ | ---- |
|                                  |     |     |     |     |     |                | with Llama, | and shows | that | larger | Mambas | pro- |
ityutilizationfornaturalandrandomtexts.
|     |     |     |     |     |     |     | gressively | make better  | use     | of their | learned | input   |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------------ | ------- | -------- | ------- | ------- |
|     |     |     |     |     |     |     | space.     | We give more | details | on       | Mamba   | results |
inAppendixC,Fig.6,andTable3).
capacity.
|     | InFig.5(bottom)wecanseethreegroups: |     |     |     |     | (1) |     |     |     |     |     |     |
| --- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
5 DiscussionandConclusions
and(2)sameasontopplotwitholderandnewer
models, and (3) group of Mamba models. The Inthiswork,weintroducedasimpleyeteffective
Pythiamodelsshowaninterestingtrend: asmodel waytocompressentiretextsequencesintoasmall
sizeincreases,capacityutilizationdecreases. This setoftrainable[mem]vectorswithoutanyinforma-
patternsuggeststhatthelargerPythiamodelsmay tionloss. Weusedthismethodtoanalyzehowfar
beunder-trainedrelativetotheirtheoreticalpoten-
wecanpushthelatentcapacityoflargelanguage
tial. In contrast, Llama and OLMo models show modelscomparedtoitstheoreticallimits.
highercapacityutilization. Basedontheseobser- By systematically evaluating different models,
| vations, |     | we hypothesize |     | that | capacity | utilization |         |                   |     |        |         |        |
| -------- | --- | -------------- | --- | ---- | -------- | ----------- | ------- | ----------------- | --- | ------ | ------- | ------ |
|          |     |                |     |      |          |             | we find | that a surprising |     | amount | of text | can be |
couldserveasanindicatorofthepre-trainingsta-
|     |     |     |     |     |     |     | compressed | to a single | token, | and | this | capacity |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ----------- | ------ | --- | ---- | -------- |
tusandguidefurthertraining. scales linearly with the number of tokens. This
FormodelswithintheLlamafamily,weobserve highlights significant potential in practical com-
that empirical capacity utilization rises steadily pressionpipelinesandlong-contextprocessing. We
withmodelsize(1B,3B,8B),mostnoticeableon demonstratethatourcompressionoutperformsneu-
natural texts from PG-19. This might be fully at- ral models as a compression method, suggesting
tributedtobetterlanguageunderstanding,gained a more efficient approach to representing infor-
8

mation. However, significantly more compute is basedandMambamodelswithupto8billionpa-
neededduetooptimizationnatureoftheproposed rametersduetocomputationalconstraints. Inves-
| method. |     |     |     |     |     | tigatingtherepresentationspaceoflargermodels, |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- |
We establish a direct link between representa- aswellasexploringalternativearchitecturessuch
|               |                    |     |         |      |     | as recurrent | and | memory-augmented |     | models, | re- |
| ------------- | ------------------ | --- | ------- | ---- | --- | ------------ | --- | ---------------- | --- | ------- | --- |
| tion capacity | and cross-entropy, |     | showing | that | it  |              |     |                  |     |         |     |
remainsindependentoftextlength,domain,orfa- mainsanimportantavenueforfutureresearch. In
miliarity. However,theexactmodelcharacteristics ourstudywithdifferenttextsources,wegenerate
that determine capacity remain an open question. randomtextbysamplingwordsfromadictionary.
Whilethisapproachsimplifiestheanalysis,itmay
| The hidden | state dimension |     | and model | size | play |     |     |     |     |     |     |
| ---------- | --------------- | --- | --------- | ---- | ---- | --- | --- | --- | --- | --- | --- |
animportantrolealongwithgeneralperformance, slightlyoverestimatemodelcapacitycomparedto
howeverfurtheranalysisisrequiredtodetermine samplingdirectlyfromatokenizer’svocabulary,as
dictionarywordscanbesplitonmultipletokensby
theexactscalinglawsforcapacity.
model.
Compressionabilityservesasastrongindicator
| of an LLM’s | potential. | Since | transformers |     | oper- |     |     |     |     |     |     |
| ----------- | ---------- | ----- | ------------ | --- | ----- | --- | --- | --- | --- | --- | --- |
BroaderImpact
| ate entirely | within their | representation |     | space, | its |     |     |     |     |     |     |
| ------------ | ------------ | -------------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
capacityfundamentallyconstrainsreasoning,inter- We train a set of [mem] vectors so that arbitrary
mediatecomputations,andlarge-scaleinformation
|             |                                    |     |     |     |     | texts can | be accurately | reconstructed |     | from | them. |
| ----------- | ---------------------------------- | --- | --- | --- | --- | --------- | ------------- | ------------- | --- | ---- | ----- |
| processing. | Alltextualandsoftpromptsultimately |     |     |     |     |           |               |               |     |      |       |
Thisprocessnotonlyallowsustoanalyzetheca-
resideinthisspace,meaningitslimitsdefinehow
pacityofthesevectors,butalsodemonstratesthat
effectivelymodelscanbesteeredandconditioned. anykindoftextcanbecompressedintocompact
Bymappingtheseboundaries,wegaindeeperin-
|            |                 |     |             |            |     | latent representations |     | and               | later decoded. |               | Such a |
| ---------- | --------------- | --- | ----------- | ---------- | --- | ---------------------- | --- | ----------------- | -------------- | ------------- | ------ |
| sight into | the fundamental |     | constraints | of current |     |                        |     |                   |                |               |        |
|            |                 |     |             |            |     | capability             | may | have far-reaching |                | implications: | it     |
architecturesandthepossibilitiesformorepower- could lead to more efficient methods for storing
fulfuturemodels.
andtransmittingtext,whilealsoraisingimportant
Moreover,ourfindingsholdsignificantpromise
|                                   |     |     |     |            |     | considerations |     | regarding | the potential | misuse | of  |
| --------------------------------- | --- | --- | --- | ---------- | --- | -------------- | --- | --------- | ------------- | ------ | --- |
| formemory-augmentedarchitectures. |     |     |     | Theability |     |                |     |           |               |        |     |
compressedinformationandissuesrelatedtodata
tocompresslongsequencesintoacompactsetof security,intellectualproperty,andalteringthebe-
memoryvectorsshowsthewayforintegratingeffi-
haviorofalignedmodels.
cientexternalmemorymodulesthatcanstoreand
retrievedetailedepisodicinformation,potentially Acknowledgments
enhancingreasoning,long-termdependencyhan-
|                                   |     |     |     |           |     | We are thankful                           |     | to SberDevices |     | for granting | us   |
| --------------------------------- | --- | --- | --- | --------- | --- | ----------------------------------------- | --- | -------------- | --- | ------------ | ---- |
| dling,andoverallmodelperformance. |     |     |     | Webelieve |     |                                           |     |                |     |              |      |
|                                   |     |     |     |           |     | accesstoadditionalcomputationalresources. |     |                |     |              | This |
thatincorporatingsuchoptimizedmemoryrepre-
|     |     |     |     |     |     | work was | partially | supported | by  | the Ministry | of  |
| --- | --- | --- | --- | --- | --- | -------- | --------- | --------- | --- | ------------ | --- |
sentationscouldleadtonovelarchitecturesthatare
EconomicDevelopmentoftheRussianFederation
bothcomputationallyefficientandmorecapableof
(code25-139-66879-1-0003).
complexinformationprocessing.
| We believe                                  | our findings |     | present | an important |     |            |     |     |     |     |     |
| ------------------------------------------- | ------------ | --- | ------- | ------------ | --- | ---------- | --- | --- | --- | --- | --- |
| steppingstonetounderstandingthelimitsofmod- |              |     |         |              |     | References |     |     |     |     |     |
ernLLMsandbuildingmorepowerfulmodelsin
AliBehrouz,PeilinZhong,andVahabMirrokni.2024.
thefuture.
|     |     |     |     |     |     | Titans: | Learning | to memorize | at  | test time. | arXiv |
| --- | --- | --- | --- | --- | --- | ------- | -------- | ----------- | --- | ---------- | ----- |
preprintarXiv:2501.00663.
Limitations
IzBeltagy,MatthewEPeters,andArmanCohan.2020.
Whileourexperimentspushtheboundariesofcom- Longformer: Thelong-documenttransformer. arXiv
preprintarXiv:2004.05150.
| pression       | with LLMs | and offer | insights  | into         | their |     |     |     |     |     |     |
| -------------- | --------- | --------- | --------- | ------------ | ----- | --- | --- | --- | --- | --- | --- |
| upper capacity | limits,   | the       | nature of | the obtained |       |     |     |     |     |     |     |
StellaBiderman,HaileySchoelkopf,QuentinGregory
| representationsremainslargelyunclear. |     |     |     | Wehave |     |          |        |          |               |     |           |
| ------------------------------------- | --- | --- | --- | ------ | --- | -------- | ------ | -------- | ------------- | --- | --------- |
|                                       |     |     |     |        |     | Anthony, | Herbie | Bradley, | Kyle O’Brien, |     | Eric Hal- |
analyzedthestructureofthespaceoftrained[mem] lahan,MohammadAflahKhan,ShivanshuPurohit,
|     |     |     |     |     |     | USVSN | Sai | Prashanth, | Edward Raff, | et  | al. 2023. |
| --- | --- | --- | --- | --- | --- | ----- | --- | ---------- | ------------ | --- | --------- |
vectorsinAppendixE,butmorein-depthanalysis
|     |     |     |     |     |     | Pythia: | A suite | for analyzing | large | language | mod- |
| --- | --- | --- | --- | --- | --- | ------- | ------- | ------------- | ----- | -------- | ---- |
isneededtodeterminethesemanticpropertiesof
|     |     |     |     |     |     | els across | training | and scaling. |     | In International |     |
| --- | --- | --- | --- | --- | --- | ---------- | -------- | ------------ | --- | ---------------- | --- |
thevectorsandtheirpotentialvalueindownstream
ConferenceonMachineLearning,pages2397–2430.
| tasks. Our | findings | are limited | to  | Transformer- |     | PMLR. |     |     |     |     |     |
| ---------- | -------- | ----------- | --- | ------------ | --- | ----- | --- | --- | --- | --- | --- |
9

Samuel R. Bowman, Luke Vilnis, Oriol Vinyals, An- AbhimanyuDubey,AbhinavJauhri,AbhinavPandey,
drewDai,RafalJozefowicz,andSamyBengio.2016. Abhishek Kadian, Ahmad Al-Dahle, Aiesha Let-
Generating sentences from a continuous space. In man,AkhilMathur,AlanSchelten,AmyYang,An-
Proceedingsofthe20thSIGNLLConferenceonCom- gela Fan, et al. 2024. The llama 3 herd of models.
putationalNaturalLanguageLearning,pages10–21, Preprint,arXiv:2407.21783.
Berlin,Germany.AssociationforComputationalLin-
| guistics. |     |     |     |     |     |     | JunGao.2024. | Selfcp:    | Compressinglongpromptto |          |     |               |
| --------- | --- | --- | --- | --- | --- | --- | ------------ | ---------- | ----------------------- | -------- | --- | ------------- |
|           |     |     |     |     |     |     | 1/12 using   | the frozen | large                   | language |     | model itself. |
TomB.Brown,BenjaminMann,NickRyder,Melanie arXivpreprintarXiv:2405.17052.
| Subbiah, | Jared | Kaplan, | Prafulla |     | Dhariwal, | Arvind |     |     |     |     |     |     |
| -------- | ----- | ------- | -------- | --- | --------- | ------ | --- | --- | --- | --- | --- | --- |
Neelakantan,PranavShyam,GirishSastry,Amanda LeoGao,StellaBiderman,SidBlack,LaurenceGold-
|         |          |          |     |       |               |     | ing, Travis | Hoppe, | Charles | Foster, | Jason | Phang, |
| ------- | -------- | -------- | --- | ----- | ------------- | --- | ----------- | ------ | ------- | ------- | ----- | ------ |
| Askell, | Sandhini | Agarwal, |     | Ariel | Herbert-Voss, |     |             |        |         |         |       |        |
Gretchen Krueger, Tom Henighan, Rewon Child, Horace He, Anish Thite, Noa Nabeshima, Shawn
Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Presser, and Connor Leahy. 2020. The Pile: An
Clemens Winter, Christopher Hesse, Mark Chen, 800gbdatasetofdiversetextforlanguagemodeling.
EricSigler,MateuszLitwin,ScottGray,Benjamin arXivpreprintarXiv:2101.00027.
| Chess, | Jack Clark, |     | Christopher |     | Berner, | Sam Mc- |     |     |     |     |     |     |
| ------ | ----------- | --- | ----------- | --- | ------- | ------- | --- | --- | --- | --- | --- | --- |
TaoGe,HuJing,LeiWang,XunWang,Si-QingChen,
| Candlish, | AlecRadford, |     | IlyaSutskever, |     |     | andDario |     |     |     |     |     |     |
| --------- | ------------ | --- | -------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
Amodei.2020. Languagemodelsarefew-shotlearn- andFuruWei.2024. In-contextautoencoderforcon-
ers. Preprint,arXiv:2005.14165. textcompressioninalargelanguagemodel. InThe
TwelfthInternationalConferenceonLearningRepre-
| Aydar Bulatov, |     | Yury Kuratov, |     | and | Mikhail | Burtsev. | sentations. |     |     |     |     |     |
| -------------- | --- | ------------- | --- | --- | ------- | -------- | ----------- | --- | --- | --- | --- | --- |
Ad-
| 2022.  | Recurrent | memory      |     | transformer. |     | In       |                  |        |             |        |          |         |
| ------ | --------- | ----------- | --- | ------------ | --- | -------- | ---------------- | ------ | ----------- | ------ | -------- | ------- |
|        |           |             |     |              |     |          | Dirk Groeneveld, |        | Iz Beltagy, | Evan   | Walsh,   | Akshita |
| vances | in Neural | Information |     | Processing   |     | Systems, |                  |        |             |        |          |         |
|        |           |             |     |              |     |          | Bhagia,          | Rodney | Kinney,     | Oyvind | Tafjord, | Ananya  |
volume35,pages11079–11091.CurranAssociates,
| Inc. |     |     |     |     |     |     | Jha,HamishIvison,IanMagnusson,YizhongWang, |              |           |     |         |         |
| ---- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | ------------ | --------- | --- | ------- | ------- |
|      |     |     |     |     |     |     | Shane                                      | Arora, David | Atkinson, |     | Russell | Authur, |
MikhailS.Burtsev,YuriKuratov,AntonPeganov,and Khyathi Chandu, Arman Cohan, Jennifer Dumas,
Grigory V. Sapunov. 2021. Memory transformer. YanaiElazar,YulingGu,JackHessel,TusharKhot,
|     |     |     |     |     |     |     | William | Merrill, | Jacob | Morrison, | Niklas | Muen- |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------- | ----- | --------- | ------ | ----- |
Preprint,arXiv:2006.11527.
|     |     |     |     |     |     |     | nighoff, | Aakanksha | Naik, | Crystal | Nam, | Matthew |
| --- | --- | --- | --- | --- | --- | --- | -------- | --------- | ----- | ------- | ---- | ------- |
Daniel Cer, Yinfei Yang, Sheng-yi Kong, Nan Hua, Peters, Valentina Pyatkin, Abhilasha Ravichander,
Nicole Limtiaco, Rhomni St John, Noah Constant, Dustin Schwenk, Saurabh Shah, William Smith,
Mario Guajardo-Cespedes, Steve Yuan, Chris Tar, EmmaStrubell,NishantSubramani,MitchellWorts-
etal.2018. Universalsentenceencoderforenglish. man,PradeepDasigi,NathanLambert,KyleRichard-
| In Proceedings |     | of the | 2018 | conference |     | on empiri- |     |     |     |     |     |     |
| -------------- | --- | ------ | ---- | ---------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
son,LukeZettlemoyer,JesseDodge,KyleLo,Luca
calmethodsinnaturallanguageprocessing: system Soldaini, Noah Smith, and Hannaneh Hajishirzi.
demonstrations,pages169–174. 2024. OLMo: Acceleratingthescienceoflanguage
|     |     |     |     |     |     |     | models. | InProceedingsofthe62ndAnnualMeeting |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ----------------------------------- | --- | --- | --- | --- |
VivekChari,GuanghuiQin,andBenjaminVanDurme. oftheAssociationforComputationalLinguistics(Vol-
| 2025.   | Kv-distill: |     | Nearly | lossless |       | learnable |                                             |     |     |     |     |     |
| ------- | ----------- | --- | ------ | -------- | ----- | --------- | ------------------------------------------- | --- | --- | --- | --- | --- |
|         |             |     |        |          |       |           | ume1: LongPapers),pages15789–15809,Bangkok, |     |     |     |     |     |
| context | compression |     | for    | llms.    | arXiv | preprint  |                                             |     |     |     |     |     |
Thailand.AssociationforComputationalLinguistics.
arXiv:2503.10337.
|     |     |     |     |     |     |     | Albert Gu | and Tri | Dao. 2024. | Mamba: |     | Linear-time |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------- | ---------- | ------ | --- | ----------- |
AlexisChevalier,AlexanderWettig,AnirudhAjith,and sequence modeling with selective state spaces. In
Danqi Chen. 2023. Adapting language models to FirstConferenceonLanguageModeling.
| compresscontexts. |     | InProceedingsofthe2023Con- |     |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ferenceonEmpiricalMethodsinNaturalLanguage AlbertGu,KaranGoel,andChristopherRé.2022. Effi-
Processing,pages3829–3846,Singapore.Associa-
cientlymodelinglongsequenceswithstructuredstate
tionforComputationalLinguistics. spaces. InTheInternationalConferenceonLearning
Representations(ICLR).
| Zihang Dai, | Zhilin | Yang, | Yiming |     | Yang, | Jaime Car- |     |     |     |     |     |     |
| ----------- | ------ | ----- | ------ | --- | ----- | ---------- | --- | --- | --- | --- | --- | --- |
bonell, Quoc Le, and Ruslan Salakhutdinov. 2019. PeijiaGuo,ZiguangLi,HaiboHu,ChaoHuang,Ming
Transformer-XL:Attentivelanguagemodelsbeyond Li,andRuiZhang.2024. Rankingllmsbycompres-
| a fixed-length |     | context. | In  | Proceedings |     | of the 57th |     |     |     |     |     |     |
| -------------- | --- | -------- | --- | ----------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
sion. arXivpreprintarXiv:2406.14171.
AnnualMeetingoftheAssociationforComputational
Linguistics,pages2978–2988,Florence,Italy.Asso- Shibo Hao, Sainbayar Sukhbaatar, DiJia Su, Xian Li,
ciationforComputationalLinguistics. ZhitingHu,JasonWeston,andYuandongTian.2024.
Traininglargelanguagemodelstoreasoninacontin-
Grégoire Delétang, Anian Ruoss, Paul-Ambroise uouslatentspace. Preprint,arXiv:2412.06769.
| Duquenne, | Elliot | Catt, | Tim | Genewein, |     | Christo- |     |     |     |     |     |     |
| --------- | ------ | ----- | --- | --------- | --- | -------- | --- | --- | --- | --- | --- | --- |
pherMattern,JordiGrau-Moya,LiKevinWenliang, Jordan Hoffmann, Sebastian Borgeaud, Arthur Men-
Matthew Aitchison, Laurent Orseau, Marcus Hut- sch, Elena Buchatskaya, Trevor Cai, Eliza Ruther-
ter, and Joel Veness. 2024. Language modeling is ford,DiegodeLasCasas,LisaAnneHendricks,Jo-
compression. InICLR. hannesWelbl,AidanClark,ThomasHennigan,Eric
10

Noland,KatherineMillican,GeorgevandenDriess- EmpiricalMethodsinNaturalLanguageProcessing,
che,BogdanDamoc,AureliaGuy,SimonOsindero, pages3045–3059,OnlineandPuntaCana,Domini-
Karén Simonyan, Erich Elsen, Oriol Vinyals, Jack can Republic. Association for Computational Lin-
| Rae,andLaurentSifre.2022. |     |     | Anempiricalanalysis |     |     | guistics. |     |     |     |     |     |     |
| ------------------------- | --- | --- | ------------------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- |
ofcompute-optimallargelanguagemodeltraining.
InAdvancesinNeuralInformationProcessingSys- Xiang Lisa Li and Percy Liang. 2021. Prefix-tuning:
tems,volume35,pages30016–30030.CurranAsso- Optimizing continuous prompts for generation. In
| ciates,Inc. |     |     |     |     |     | Proceedingsofthe59thAnnualMeetingoftheAsso- |     |     |     |     |     |     |
| ----------- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- |
ciationforComputationalLinguisticsandthe11th
EdwardJHu,yelongshen,PhillipWallis,ZeyuanAllen- InternationalJointConferenceonNaturalLanguage
Zhu,YuanzhiLi,SheanWang,LuWang,andWeizhu
|          |             |     |               |            |          | Processing | (Volume |             | 1: Long | Papers),      | pages | 4582– |
| -------- | ----------- | --- | ------------- | ---------- | -------- | ---------- | ------- | ----------- | ------- | ------------- | ----- | ----- |
| Chen.    | 2022. LoRA: |     | Low-rank      | adaptation | of large |            |         |             |         |               |       |       |
|          |             |     |               |            |          | 4597,      | Online. | Association | for     | Computational |       | Lin-  |
| language | models.     | In  | International | Conference | on       | guistics.  |         |             |         |               |       |       |
LearningRepresentations.
|     |     |     |     |     |     | Yuhong | Li, Yingbing |     | Huang, | Bowen | Yang, | Bharat |
| --- | --- | --- | --- | --- | --- | ------ | ------------ | --- | ------ | ----- | ----- | ------ |
LuyangHuang,ShuyangCao,NikolausParulian,Heng
Venkitesh,AcyrLocatelli,HanchenYe,TianleCai,
| Ji,andLuWang.2021.     |     |     | Efficientattentionsforlong |     |     |         |        |     |        |              |     |         |
| ---------------------- | --- | --- | -------------------------- | --- | --- | ------- | ------ | --- | ------ | ------------ | --- | ------- |
|                        |     |     |                            |     |     | Patrick | Lewis, | and | Deming | Chen. 2024a. |     | Snapkv: |
| documentsummarization. |     |     | InProceedingsofthe2021     |     |     |         |        |     |        |              |     |         |
Llmknowswhatyouarelookingforbeforegener-
| Conference | of  | the North | American | Chapter | of the |     |     |     |     |     |     |     |
| ---------- | --- | --------- | -------- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- |
ation. AdvancesinNeuralInformationProcessing
| AssociationforComputationalLinguistics: |     |     |     |     | Human |     |     |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
Systems,37:22947–22970.
LanguageTechnologies,pages1419–1436,Online.
AssociationforComputationalLinguistics.
|     |     |     |     |     |     | Zongqian        | Li, | Yixuan | Su, and     | Nigel  | Collier. | 2024b.   |
| --- | --- | --- | --- | --- | --- | --------------- | --- | ------ | ----------- | ------ | -------- | -------- |
|     |     |     |     |     |     | 500xcompressor: |     |        | Generalized | prompt |          | compres- |
YuzhenHuang,JinghanZhang,ZifeiShan,andJunx-
|             |     |                                   |     |     |     | sion for | large | language | models. |     | arXiv | preprint |
| ----------- | --- | --------------------------------- | --- | --- | --- | -------- | ----- | -------- | ------- | --- | ----- | -------- |
| ianHe.2024. |     | Compressionrepresentsintelligence |     |     |     |          |       |          |         |     |       |          |
arXiv:2408.03094.
| linearly. | InFirstConferenceonLanguageModeling. |     |     |     |     |     |     |     |     |     |     |     |
| --------- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing XiaoLiu,KaixuanJi,YichengFu,WengTam,Zhengx-
Yang,andLiliQiu.2023. LLMLingua:Compressing iaoDu,ZhilinYang,andJieTang.2022. P-tuning:
promptsforacceleratedinferenceoflargelanguage Prompt tuning can be comparable to fine-tuning
|         |                                    |     |     |     |     | acrossscalesandtasks. |     |     | InProceedingsofthe60th |     |     |     |
| ------- | ---------------------------------- | --- | --- | --- | --- | --------------------- | --- | --- | ---------------------- | --- | --- | --- |
| models. | InProceedingsofthe2023Conferenceon |     |     |     |     |                       |     |     |                        |     |     |     |
Empirical Methods in Natural Language Process- AnnualMeetingoftheAssociationforComputational
ing,pages13358–13376,Singapore.Associationfor Linguistics(Volume2: ShortPapers),pages61–68,
ComputationalLinguistics. Dublin,Ireland.AssociationforComputationalLin-
guistics.
| Huiqiang | Jiang, | Qianhui | Wu, Xufang | Luo, | Dong- |     |     |     |     |     |     |     |
| -------- | ------ | ------- | ---------- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- |
shengLi,Chin-YewLin,YuqingYang,andLiliQiu.
|     |     |     |     |     |     | Ilya Loshchilov |     | and Frank | Hutter. | 2019. | Decoupled |     |
| --- | --- | --- | --- | --- | --- | --------------- | --- | --------- | ------- | ----- | --------- | --- |
2024. LongLLMLingua: Acceleratingandenhanc- weightdecayregularization. InInternationalConfer-
ingLLMsinlongcontextscenariosviapromptcom- enceonLearningRepresentations.
| pression. | InProceedingsofthe62ndAnnualMeeting |     |     |     |     |     |     |     |     |     |     |     |
| --------- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
oftheAssociationforComputationalLinguistics(Vol- WilliamMerrillandAshishSabharwal.2023. Thepar-
| ume1: | LongPapers),pages1658–1677,Bangkok, |     |     |     |     |                   |     |                                  |     |     |     |     |
| ----- | ----------------------------------- | --- | --- | --- | --- | ----------------- | --- | -------------------------------- | --- | --- | --- | --- |
|       |                                     |     |     |     |     | allelismtradeoff: |     | Limitationsoflog-precisiontrans- |     |     |     |     |
Thailand.AssociationforComputationalLinguistics.
|     |     |     |     |     |     | formers. | TransactionsoftheAssociationforCompu- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | ------------------------------------- | --- | --- | --- | --- | --- |
tationalLinguistics,11:531–545.
JaredKaplan,SamMcCandlish,TomHenighan,TomB
Brown,BenjaminChess,RewonChild,ScottGray, Yishu Miao, Lei Yu, and Phil Blunsom. 2016. Neu-
| AlecRadford,JeffreyWu,andDarioAmodei.2020. |     |     |     |     |     |     |     |     |     |     |     | InPro- |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
ralvariationalinferencefortextprocessing.
| Scaling | laws for | neural | language | models. | arXiv |          |     |          |               |     |            |     |
| ------- | -------- | ------ | -------- | ------- | ----- | -------- | --- | -------- | ------------- | --- | ---------- | --- |
|         |          |        |          |         |       | ceedings | of  | The 33rd | International |     | Conference | on  |
preprintarXiv:2001.08361.
MachineLearning,volume48ofProceedingsofMa-
|     |     |     |     |     |     | chine | Learning | Research, | pages | 1727–1736, |     | New |
| --- | --- | --- | --- | --- | --- | ----- | -------- | --------- | ----- | ---------- | --- | --- |
RyanKiros,YukunZhu,RussRSalakhutdinov,Richard
York,NewYork,USA.PMLR.
Zemel,RaquelUrtasun,AntonioTorralba,andSanja
| Fidler.2015. | Skip-thoughtvectors. |     |     | InAdvancesin |     |              |        |     |            |        |       |     |
| ------------ | -------------------- | --- | --- | ------------ | --- | ------------ | ------ | --- | ---------- | ------ | ----- | --- |
|              |                      |     |     |              |     | Fazal Mittu, | Yihuan |     | Bu, Akshat | Gupta, | Ashok | De- |
NeuralInformationProcessingSystems,volume28.
|     |     |     |     |     |     | vireddy, | Alp | Eren | Ozdarendeli, | Anant | Singh, | and |
| --- | --- | --- | --- | --- | --- | -------- | --- | ---- | ------------ | ----- | ------ | --- |
CurranAssociates,Inc.
|     |     |     |     |     |     | GopalaAnumanchipalli.2024. |     |     |     | Finezip: | Pushingthe |     |
| --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | --- | -------- | ---------- | --- |
limitsoflargelanguagemodelsforpracticallossless
| Quoc Le      | and Tomas | Mikolov.  | 2014. | Distributed | rep-    |                  |     |                                |     |     |     |     |
| ------------ | --------- | --------- | ----- | ----------- | ------- | ---------------- | --- | ------------------------------ | --- | --- | --- | --- |
|              |           |           |       |             |         | textcompression. |     | arXivpreprintarXiv:2409.17141. |     |     |     |     |
| resentations | of        | sentences | and   | documents.  | In Pro- |                  |     |                                |     |     |     |     |
ceedingsofthe31stInternationalConferenceonMa-
chine Learning, volume 32 of Proceedings of Ma- Ivan Montero, Nikolaos Pappas, and Noah A. Smith.
chineLearningResearch,pages1188–1196,Bejing, 2021. Sentencebottleneckautoencodersfromtrans-
|     |     |     |     |     |     | formerlanguagemodels. |     |     | InProceedingsofthe2021 |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | ---------------------- | --- | --- | --- |
China.PMLR.
|     |     |     |     |     |     | Conference |     | on Empirical | Methods |     | in Natural | Lan- |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ------------ | ------- | --- | ---------- | ---- |
BrianLester,RamiAl-Rfou,andNoahConstant.2021. guage Processing, pages 1822–1831, Online and
The power of scale for parameter-efficient prompt Punta Cana, Dominican Republic. Association for
tuning. InProceedingsofthe2021Conferenceon ComputationalLinguistics.
11

JohnMorris,VolodymyrKuleshov,VitalyShmatikov, Chandra Shekhara Kaushik Valmeekam, Krishna
andAlexanderRush.2023. Textembeddingsreveal Narayanan,DileepKalathil,Jean-FrancoisChamber-
(almost)asmuchastext. InProceedingsofthe2023 land,andSrinivasShakkottai.2023. Llmzip: Loss-
Conference on Empirical Methods in Natural Lan- lesstextcompressionusinglargelanguagemodels.
guageProcessing, pages12448–12460, Singapore. arXivpreprintarXiv:2306.04050.
AssociationforComputationalLinguistics.
|     |     |     |     |     |     | Ashish Vaswani, | Noam | Shazeer, |     | Niki Parmar, | Jakob |
| --- | --- | --- | --- | --- | --- | --------------- | ---- | -------- | --- | ------------ | ----- |
JohnXavierMorris,WentingZhao,JustinTChiu,Vi- Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz
talyShmatikov,andAlexanderMRush.2024. Lan- Kaiser,andIlliaPolosukhin.2017. AttentionisAll
InTheTwelfthInternational you Need. In Advances in neural information pro-
guagemodelinversion.
cessingsystems,pages5998–6008.
ConferenceonLearningRepresentations.
LiangWang,NanYang,XiaolongHuang,LinjunYang,
| JesseMu,XiangLi,andNoahGoodman.2023. |     |     |     |          | Learn- |        |           |     |           |       |           |
| ------------------------------------ | --- | --- | --- | -------- | ------ | ------ | --------- | --- | --------- | ----- | --------- |
|                                      |     |     |     |          |        | Rangan | Majumder, | and | Furu Wei. | 2024. | Multilin- |
| ingtocompresspromptswithgisttokens.  |     |     |     | Advances |        |        |           |     |           |       |           |
inNeuralInformationProcessingSystems,36:19327– guale5textembeddings: Atechnicalreport. arXiv
preprintarXiv:2402.05672.
19352.
JasonWeston,SumitChopra,andAntoineBordes.2015.
ZhuoshiPan,QianhuiWu,HuiqiangJiang,MenglinXia,
|     |     |     |     |     |     | Memorynetworks. |     | In3rdInternationalConference |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------- | --- | ---------------------------- | --- | --- | --- |
XufangLuo,JueZhang,QingweiLin,VictorRühle,
onLearningRepresentations,ICLR2015,SanDiego,
YuqingYang,Chin-YewLin,H.VickyZhao,LiliQiu,
CA,USA,May7-9,2015,ConferenceTrackProceed-
| andDongmeiZhang.2024. |     |     | LLMLingua-2: | Datadis- |     |     |     |     |     |     |     |
| --------------------- | --- | --- | ------------ | -------- | --- | --- | --- | --- | --- | --- | --- |
ings.
tillationforefficientandfaithfultask-agnosticprompt
| compression. | InFindingsoftheAssociationforCom- |     |     |     |     |     |     |     |     |     |     |
| ------------ | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
MengzhouXia,TianyuGao,ZhiyuanZeng,andDanqi
| putational | Linguistics: |     | ACL 2024, pages | 963–981, |     |             |         |        |     |              |      |
| ---------- | ------------ | --- | --------------- | -------- | --- | ----------- | ------- | ------ | --- | ------------ | ---- |
|            |              |     |                 |          |     | Chen. 2024. | Sheared | LLaMA: |     | Accelerating | lan- |
Bangkok,Thailand.AssociationforComputational
|     |     |     |     |     |     | guagemodelpre-trainingviastructuredpruning. |     |     |     |     | In  |
| --- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- |
Linguistics. The Twelfth International Conference on Learning
Representations.
GuanghuiQin,CorbyRosset,EthanChau,NikhilRao,
andBenjaminVanDurme.2024. Dodo: Dynamic Manzil Zaheer, Guru Guruganesh, Kumar Avinava
| contextual | compression |     | for decoder-only | lms. | In  |     |     |     |     |     |     |
| ---------- | ----------- | --- | ---------------- | ---- | --- | --- | --- | --- | --- | --- | --- |
Dubey,JoshuaAinslie,ChrisAlberti,SantiagoOn-
Proceedingsofthe62ndAnnualMeetingoftheAs- tanon, Philip Pham, Anirudh Ravula, Qifan Wang,
sociationforComputationalLinguistics(Volume1: Li Yang, et al. 2020. Big bird: Transformers for
LongPapers),pages9961–9975. longersequences. Advancesinneuralinformation
processingsystems,33:17283–17297.
| GuanghuiQinandBenjaminVanDurme.2023. |     |     |     | Nugget:  |     |              |         |         |       |        |       |
| ------------------------------------ | --- | --- | --- | -------- | --- | ------------ | ------- | ------- | ----- | ------ | ----- |
|                                      |     |     |     |          |     | Susan Zhang, | Stephen | Roller, | Naman | Goyal, | Mikel |
| Neuralagglomerativeembeddingsoftext. |     |     |     | InInter- |     |              |         |         |       |        |       |
national Conference on Machine Learning, pages Artetxe,MoyaChen,ShuohuiChen,ChristopherDe-
| 28337–28350.PMLR. |     |     |     |     |     | wan,MonaDiab,XianLi,XiVictoriaLin,TodorMi- |     |     |     |     |     |
| ----------------- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- |
haylov,MyleOtt,SamShleifer,KurtShuster,Daniel
Alec Radford, Jeff Wu, Rewon Child, David Luan, Simig, Punit Singh Koura, Anjali Sridhar, Tianlu
|                                    |     |     |     |          |     | Wang,                                 | and Luke | Zettlemoyer. |     | 2022. Opt: | Open      |
| ---------------------------------- | --- | --- | --- | -------- | --- | ------------------------------------- | -------- | ------------ | --- | ---------- | --------- |
| DarioAmodei,andIlyaSutskever.2019. |     |     |     | Language |     |                                       |          |              |     |            |           |
|                                    |     |     |     |          |     | pre-trainedtransformerlanguagemodels. |          |              |     |            | Preprint, |
modelsareunsupervisedmultitasklearners.
arXiv:2205.01068.
| Jack W. Rae, | Anna | Potapenko, | Siddhant | M. Jayaku- |     |     |     |     |     |     |     |
| ------------ | ---- | ---------- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
mar, Chloe Hillier, and Timothy P. Lillicrap. 2020. Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong
Chen,LianminZheng,RuisiCai,ZhaoSong,Yuan-
Compressivetransformersforlong-rangesequence
dongTian,ChristopherRé,ClarkBarrett,etal.2023.
| modelling. | InInternationalConferenceonLearning |     |     |     |     |                   |     |        |     |           |            |
| ---------- | ----------------------------------- | --- | --- | --- | --- | ----------------- | --- | ------ | --- | --------- | ---------- |
|            |                                     |     |     |     |     | H2o: Heavy-hitter |     | oracle | for | efficient | generative |
Representations.
|     |     |     |     |     |     | inference | of large | language | models. | Advances | in  |
| --- | --- | --- | --- | --- | --- | --------- | -------- | -------- | ------- | -------- | --- |
Clayton Sanford, Daniel J Hsu, and Matus Telgarsky. NeuralInformationProcessingSystems,36:34661–
| 2024. Representationalstrengthsandlimitationsof |     |                                 |     |     |     | 34710. |     |     |     |     |     |
| ----------------------------------------------- | --- | ------------------------------- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
| transformers.                                   |     | AdvancesinNeuralInformationPro- |     |     |     |        |     |     |     |     |     |
cessingSystems,36.
LenaStrobl,WilliamMerrill,GailWeiss,DavidChiang,
| andDanaAngluin.2024. |     |     | Whatformallanguagescan     |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| transformersexpress? |     |     | asurvey. Transactionsofthe |     |     |     |     |     |     |     |     |
AssociationforComputationalLinguistics,12:543–
561.
SainbayarSukhbaatar,ArthurSzlam,JasonWeston,and
| RobFergus.2015. |     | End-to-endmemorynetworks. |     |     | In  |     |     |     |     |     |     |
| --------------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
AdvancesinNeuralInformationProcessingSystems,
volume28.CurranAssociates,Inc.
12

A ModelsandTrainingDetails
checkpointsfromtheHuggingFaceHub(Table2).
|            |      |               |      |         |        | We found | that Mamba |     | can also | encode | texts into |
| ---------- | ---- | ------------- | ---- | ------- | ------ | -------- | ---------- | --- | -------- | ------ | ---------- |
| We provide | list | of all models | that | we used | in our |          |            |     |          |        |            |
asingle[mem]vectorandsuccessfullyreconstruct
experimentsinTable2.
themwheneverthetext’scross-entropyfallsbelow
| Trainablevectorsareinitializedrandomly. |     |     |     |     | We  |                  |     |            |            |     |            |
| --------------------------------------- | --- | --- | --- | --- | --- | ---------------- | --- | ---------- | ---------- | --- | ---------- |
|                                         |     |     |     |     |     | model’s capacity |     | threshold, | indicating |     | the effect |
usetheAdamWoptimizer(LoshchilovandHutter,
isnotuniquetoonlyTransformermodels(Fig.6
| 2019)withalearningrateof0.01,β |     |     |     | 1 ,andβ | 2 both |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- |
andTable3).
| set to 0.9, | and | a weight | decay | of 0.01. | Training |     |     |     |     |     |     |
| ----------- | --- | -------- | ----- | -------- | -------- | --- | --- | --- | --- | --- | --- |
proceedsforamaximumof5,000steps,withearly
D ResultsofEvaluatingText
| stopping | if the | text is compressed |     | losslessly, | i.e., |     |     |     |     |     |     |
| -------- | ------ | ------------------ | --- | ----------- | ----- | --- | --- | --- | --- | --- | --- |
CompressionforAllModels
| achievingatoken-levelaccuracyof1.0. |      |                 |     |              | Allmodels |         |         |         |                   |     |        |
| ----------------------------------- | ---- | --------------- | --- | ------------ | --------- | ------- | ------- | ------- | ----------------- | --- | ------ |
| are loaded                          | from | the HuggingFace |     | Transformers |           |         |         |         |                   |     |        |
|                                     |      |                 |     |              |           | Here we | provide | results | for all evaluated |     | models |
librarywiththePyTorchframework.
|     |     |     |     |     |     | inFig.6andTable3. |     | ResultsarediscussedinSec- |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------------- | --- | ------------------------- | --- | --- | --- |
Eachcompressionexperimentwasrunonasin-
tion4.3.
| gle A100   | 80GB  | GPU.  | The time     | required | to com- |     |     |     |     |     |     |
| ---------- | ----- | ----- | ------------ | -------- | ------- | --- | --- | --- | --- | --- | --- |
| press text | using | 5,000 | optimization | steps    | ranged  |     |     |     |     |     |     |
E UnderstandingtheStructureof
fromadozenofsecondsforsmallmodelsandshort
CompressedVectors
| contexts | to 10–20  | minutes | for | larger models | and    |           |            |     |           |     |           |
| -------- | --------- | ------- | --- | ------------- | ------ | --------- | ---------- | --- | --------- | --- | --------- |
| longer   | contexts. | We used | up  | to 4 GPUs     | to run |           |            |     |           |     |           |
|          |           |         |     |               |        | To better | understand | the | structure | of  | the space |
severalexperimentsinparallel. formed by the learned embeddings, we collect a
datasetofembeddingsfor64-tokensequencesfrom
B CollectingTextsfromtheFanfics
|     |     |     |     |     |     | the GovReport | dataset |     | (Huang et | al., 2021). | The |
| --- | --- | --- | --- | --- | --- | ------------- | ------- | --- | --------- | ----------- | --- |
Library
|     |     |     |     |     |     | optimization | is  | performed | until | a reconstruction |     |
| --- | --- | --- | --- | --- | --- | ------------ | --- | --------- | ----- | ---------------- | --- |
We used the AO3 fanfiction library https:// accuracyof1.0isachieved. Additionally,foreach
archiveofourown.org/ as a source of texts that sequence, we compute multiple embeddings us-
were not present in the language models’ pre- ing different random initializations of the [mem]
| training | data. | To ensure | novelty, | we  | manually | vectors. |     |     |     |     |     |
| -------- | ----- | --------- | -------- | --- | -------- | -------- | --- | --- | --- | --- | --- |
downloaded21fanficsfromvariousfandoms(in- First,weobservethattheoptimizationprocess
cluding Harry Potter, Star Wars, Transformers, canyielddifferentsolutions;theresultingvectors
LordoftheRings,andothers)thatcontainedmore for the same text may lie in completely different
than20,000wordsandwerepublishedafterOcto- partsofthespace. Tovisualizethisphenomenon,
| ber2024. |     |     |     |     |     | we plot histograms |     | of  | cosine similarity |     | between |
| -------- | --- | --- | --- | --- | --- | ------------------ | --- | --- | ----------------- | --- | ------- |
We preprocessed the HTML pages to extract embeddingsofthesametext(intra-sample)andbe-
onlythemaintextcontent,removinganyirrelevant
tweenembeddingsofdifferenttexts(inter-sample)
elements. We then sampled passages from these inFig.7. Notably,almostnohighcosinesimilar-
texts to evaluate the capacity of trainable input ities(above0.8)areobservedintheintra-sample
vectors. Throughoutourexperiments,wereferto case. Moreover,theintra-samplesimilaritiessignif-
thisdatasetasfanfics. icantlyoverlapwiththeinter-sampleones,imply-
FromeachofthePG-19andfanfics,wesampled ingthattheembeddingsareconsiderablyscattered
texts and set their lengths to match the desired throughoutthespace.
| tokencounts. |           | Weensuredthateachtextbeganwith |          |            |      |          |     |            |        |     |           |
| ------------ | --------- | ------------------------------ | -------- | ---------- | ---- | -------- | --- | ---------- | ------ | --- | --------- |
|              |           |                                |          |            |      | Although | the | embeddings | appear | to  | be spread |
| complete     | sentences | to                             | maintain | coherence. | As a |          |     |            |        |     |           |
out,onemighthopetheyformabasininwhichall
result,toestimatethecapacityoftheinputvectors, linearinterpolationsbetweenvectorswouldyield
weused50textsforeachlength. perfectreconstruction. Totestthis,wecomputed
thereconstructionaccuracyalonglinearinterpola-
C Non-TransformerLanguageModels:
tiontrajectoriesbetweenembeddingsofthesame
Mamba
|     |     |     |     |     |     | sequence. | However,inallcasesweexamined,er- |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------- | -------------------------------- | --- | --- | --- | --- |
Mamba (Gu and Dao, 2024) is a state space lan- rorswerepresentalongtheinterpolationtrajectory
|     |     |     |     |     |     | (see Fig. | 8). Thus, | the | embeddings | obtained | by  |
| --- | --- | --- | --- | --- | --- | --------- | --------- | --- | ---------- | -------- | --- |
guagemodel(SSM)(Guetal.,2022),incontrast
to attention-based Transformers. We applied the theproposedproceduredonotformacontinuous
| same compression |     | procedure | used | for | the Trans- | basin. |     |     |     |     |     |
| ---------------- | --- | --------- | ---- | --- | ---------- | ------ | --- | --- | --- | --- | --- |
former models and evaluated the official Mamba Theseobservationshaveseveralimplications:
13

ModelName LinktoHuggingFace Params(B) InputHiddenSize VocabularySize
| Pythia-160M | EleutherAI/pythia-160m  |     | 0.16 | 768  | 50304 |     |
| ----------- | ----------------------- | --- | ---- | ---- | ----- | --- |
| Pythia-410M | EleutherAI/pythia-410m  |     | 0.41 | 1024 | 50304 |     |
| Pythia-1.4B | EleutherAI/pythia-1.4b  |     | 1.4  | 2048 | 50304 |     |
| Pythia-2.8B | EleutherAI/pythia-2.8b  |     | 2.8  | 2560 | 50304 |     |
| OPT-1.3B    | facebook/opt-1.3b       |     | 1.3  | 2048 | 50272 |     |
| OLMo-1B     | allenai/OLMo-1B-0724-hf |     | 1.0  | 2048 | 50304 |     |
Sheared-LLaMA-1.3B princeton-nlp/Sheared-LLaMA-1.3B 1.3 2048 32000
| Llama-3.2-1B | meta-llama/Llama-3.2-1B    |     | 1.0  | 2048 | 128256 |     |
| ------------ | -------------------------- | --- | ---- | ---- | ------ | --- |
| Llama-3.2-3B | meta-llama/Llama-3.2-3B    |     | 3.0  | 3072 | 128256 |     |
| Llama-3.1-8B | meta-llama/Llama-3.1-8B    |     | 8.0  | 4096 | 128256 |     |
| Mamba-130M   | state-spaces/mamba-130m-hf |     | 0.13 | 768  | 50280  |     |
| Mamba-370M   | state-spaces/mamba-370m-hf |     | 0.38 | 1024 | 50280  |     |
| Mamba-790M   | state-spaces/mamba-790m-hf |     | 0.79 | 1536 | 50280  |     |
| Mamba-1.4B   | state-spaces/mamba-1.4b-hf |     | 1.4  | 2048 | 50280  |     |
Table2: Listofusedlanguagemodelsandtheirparameters.
|     | PG-19 |     | Fanfics |     | Random |     |
| --- | ----- | --- | ------- | --- | ------ | --- |
Model
Max,tok. Gain,tok. InformationGain Max,tok. Gain,tok. InformationGain Max,tok. Gain,tok. InformationGain
Pythia-160M 80 70.9±11.0 396.4±46.0 80 70.9±10.5 378.1±45.9 65 61.3±6.6 500.8±38.9
Pythia-410M 96 81.3±12.0 431.4±51.6 96 81.2±11.6 429.8±46.2 72 76.9±8.7 630.4±65.2
Pythia-1.4B 160 158.0±29.1 792.8±143.4 192 152.9±28.0 776.9±132.5 139 144.4±17.5 1108.2±136.2
Pythia-2.8B 128 150.1±50.7 740.3±234.9 - - - 141 134.5±24.7 1026.3±211.4
OPT-1.3B 128 132.2±23.8 712.8±143.3 - - - 116 129.3±16.4 1068.0±181.3
OLMo-1B 384 406.3±61.7 1901.0±254.5 - - - 249 257.3±55.0 1852.2±395.0
Sh.LLaMa-1.3B 512 383.6±38.4 1835.1±162.9 - - - 382 315.1±35.1 1893.0±210.0
Llama-3.2-1B 512 426.2±79.2 2119.9±364.8 512 449.6±83.7 2213.8±365.8 316 294.9±64.8 2265.2±498.7
Llama-3.2-3B 1024 720.3±80.2 3292.2±320.0 1024 734.1±85.0 3354.5±344.9 460 456.9±72.1 3382.6±585.2
Llama-3.1-8B 1568 1094.1±127.6 4865.7±546.6 1568 1071.8±168.6 4768.9±622.6 792 623.2±97.3 4541.2±758.6
Mamba-130M 32 65.5±18.1 371.4±94.6 - - - 84 62.6±17.1 535.7±121.8
Mamba-370M 128 113.0±27.6 585.3±131.1 - - - 106 94.5±25.5 743.2±186.9
Mamba-790M 256 204.2±33.0 1011.6±138.8 - - - 198 187.0±26.3 1421.3±179.1
Mamba-1.4B 512 348.9±42.9 1599.5±164.5 - - - 288 282.7±36.5 2062.3±257.3
Table3: Compressioncapacityacrossdifferenttextsourcesandforallevaluatedmodels. WereportDecoding
Capacity(inTokens)("Max,tokens"intheTable),TokenGain,andInformationGainfortextsfromPG-19,fanfics,
random.
1. Alosslesscompressionalgorithmideallyas- serveasageneral-purposecompressionapproach,
signsauniquedecodingtoeachvector;multi- wecurrentlytreatlosslesscompressionasatoolto
plevalidembeddingsforthesameobjectlimit better understand LLMs hidden state capacity in
theachievablecompressionrate. contrasttoachievingthehighestpossiblecompres-
sionrate.
2. Thespreadandentangledstructureoftheem-
beddingsmayrenderthemlessusefulasrep- We ran experiments on three datasets (PG-19,
| resentations.       |                     |       | fanfics,andrandomlysampledsequencesofwords) |                 |                 |     |
| ------------------- | ------------------- | ----- | ------------------------------------------- | --------------- | --------------- | --- |
|                     |                     |       | using zlib,                                 | bz2, lzma, pure | Huffman coding, | and |
| 3. This non-unique, | scattered structure | could |                                             |                 |                 |     |
ArithmeticCoding(AC)withLM.Wereporttheir
makeitmorechallengingtoextractimportant
meancompressionratios(originaltextsizeinbits/
informationwhenthesecompressedrepresen- compressedsize)inTable4.
tationsareusedascontextinanLM.
|     |     |     | We see | that conventional | entropy coders | can |
| --- | --- | --- | ------ | ----------------- | -------------- | --- |
compresstextsbyaboutafactoroftwo,andcom-
F DataCompressionAnalysis
|     |     |     | bining | Arithmetic Coding | with pythia-160m | can |
| --- | --- | --- | ------ | ----------------- | ---------------- | --- |
In the present work, we focus on exploring phe- lead to much higher ratios: 6-7x. With our ap-
nomenathatcouldbepotentiallyhelpfulinbuild- proach we can encode up to 1568 tokens into a
ingmoreefficientLLMs. Despiteourmethodcan single 4096-dimensional bfloat16 vector (using
14

Method PG19 Fanfics Random
zlib 2.28±0.16 2.34±0.07 1.80±0.06
bz2 2.46±0.16 2.56±0.09 1.94±0.11
lzma 2.28±0.16 2.33±0.07 1.86±0.13
Huffman 1.81±0.07 1.86±0.04 1.77±0.01
AC,pythia-160m 6.77±0.75 6.73±0.41 2.83±0.08
Table 4: Compression ratios (in bits) comparison for
classiccompressionalgorithmsandarithmeticcoding
(AC)usingpythia-160mforarangeofcorpora.
LLaMA-3.1-8B) and reconstruct them losslessly.
If we treat a single 4096-dimensional vector as a
"compressedfile"andcompute(originaltextsize
as string) / (size of vector), the ratio actually ap-
pearstobeabout0.8x,soitdoesnottakelessbits
ondiskthanarawtext.
Importantly, unlike conventional compression
algorithmsthatoutputarbitrarybitstreams,ourap-
proach must encode the text into a single vector,
whichLLMsinterpretasanembedding. Thiscon-
straintisstricterthansimplyminimizingfilesize,
sincetheoutputmustliewithintheinputspaceof
the model. Our focus, therefore, is on analyzing
representationalcapacitywithintheinputspaceof
largelanguagemodels. Forinstance,asingle4096-
dimensional vector in LLaMA-3.1-8B can guide
the model to generate up to 1568 tokens exactly.
Reconstructing 1568 tokens from just one vector
resultsina1568xreductioninthenumberofem-
beddingsthatwouldotherwisebeusedtorepresent
thetext.
Ourgoalisnottooutperformstandardcompres-
sorsinbits-per-byteefficiency,butrathertoshow
that LLMs can store significant amounts of text
withonlyasingleembedding.
15

Texts from PG-19 Random text (sampled words) All texts below the line are losselessly compressed
|     | pythia-160m    |     |      | pythia-410m    |     |     | pythia-1.4b    |     |      | pythia-2.8b    |     |     |
| --- | -------------- | --- | ---- | -------------- | --- | --- | -------------- | --- | ---- | -------------- | --- | --- |
|     |                |     | 6000 |                |     |     |                |     | 4000 |                |     |     |
|     | y = x + -396.4 |     |      | y = x + -431.4 |     |     | y = x + -792.8 |     |      | y = x + -740.3 |     |     |
2000
|     |     |     |     |     |     | 4000 |     |     | 3000 |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- |
4000
|     |     |     |     |     |     |     |     |     | 2000 |     |     | 3000 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | ---- |
1000
2000
|     |        |      | 2000 |             |      |     |        |      | 1000 |        |      |     |
| --- | ------ | ---- | ---- | ----------- | ---- | --- | ------ | ---- | ---- | ------ | ---- | --- |
|     | 0      |      |      |             |      |     |        |      | 0    |        |      |     |
|     |        |      | 0    |             |      | 0   |        |      |      |        |      |     |
|     | 0 1000 | 2000 |      | 0 2000 4000 | 6000 |     | 0 2000 | 4000 |      | 0 2000 | 4000 |     |
2500
|     | opt-1.3b |     |     | OLMo-1B-0724 |     |     | Sheared-LLaMA-1.3B |     |     |     |     |     |
| --- | -------- | --- | --- | ------------ | --- | --- | ------------------ | --- | --- | --- | --- | --- |
8000
|     | y = x + -712.8 |     |     | y = x + -1901.0 |     |     | y = x + -1835.1 |     |     |     |     |     |
| --- | -------------- | --- | --- | --------------- | --- | --- | --------------- | --- | --- | --- | --- | --- |
4000
| 4000 |     |     | 6000 |     |     |     |     |     |     |     |     |     |
| ---- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
yportnE-ssorC ,txet desserpmoceD
|      |                 |           | 4000 |                 |       |      |                   |           |     |     |     | 2000                |
| ---- | --------------- | --------- | ---- | --------------- | ----- | ---- | ----------------- | --------- | --- | --- | --- | ------------------- |
| 2000 |                 |           |      |                 |       | 2000 |                   |           |     |     |     |                     |
|      |                 |           | 2000 |                 |       |      |                   |           |     |     |     | Text Length, tokens |
|      | 0               |           | 0    |                 |       | 0    |                   |           |     |     |     |                     |
|      | 0 2000          | 4000 6000 | 0    | 5000            | 10000 |      | 0 2000            | 4000 6000 |     |     |     |                     |
|      | Llama-3.2-1B    |           |      | Llama-3.2-3B    |       |      | Meta-Llama-3.1-8B |           |     |     |     | 1500                |
| 8000 | y = x + -2119.9 |           | 6000 | y = x + -3292.2 |       | 4000 | y = x + -4865.7   |           |     |     |     |                     |
| 6000 |                 |           |      |                 |       | 3000 |                   |           |     |     |     |                     |
4000
| 4000 |     |     |     |     |     | 2000 |     |     |     |     |     |     |
| ---- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
1000
|     |     |     | 2000 |     |     | 1000 |     |     |     |     |     |     |
| --- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
2000
0
|     | 0          |       | 0   |            |       |     |            |           |     |            |     |     |
| --- | ---------- | ----- | --- | ---------- | ----- | --- | ---------- | --------- | --- | ---------- | --- | --- |
|     | 0 5000     | 10000 | 0   | 5000       | 10000 |     | 0 2500     | 5000 7500 |     |            |     |     |
|     | mamba-130m |       |     | mamba-370m |       |     | mamba-790m |           |     | mamba-1.4b |     |     |
500
|     |     |     |     |     |     | 2000 |     |     | 3000 |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- |
1500 y = x + -371.4 y = x + -585.3 y = x + -1011.6 y = x + -1599.5
1500
1500
| 1000 |     |     |     |     |     |     |     |     | 2000 |     |     |     |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
1000
1000
| 500 |        |      |     |        |      |     |        |           | 1000 |      |      |     |
| --- | ------ | ---- | --- | ------ | ---- | --- | ------ | --------- | ---- | ---- | ---- | --- |
|     |        |      | 500 |        |      | 500 |        |           |      |      |      |     |
|     | 0      |      | 0   |        |      | 0   |        |           | 0    |      |      |     |
|     | 0 1000 | 2000 |     | 0 1000 | 2000 |     | 0 1000 | 2000 3000 | 0    | 2000 | 4000 |     |
Text, Cross-Entropy
Figure6: Informationgainoftextcompressionto[mem]vectordoesn’tdependonlanguageunderstanding
capabilitiesofmodels. Compressionresultsforvariouslanguagemodelsshowtherelationshipbetweenthecross-
entropy(CE)oftheoriginalanddecompressedtexts. IfthetextCEfallsbelowamodel-specificthreshold(redline),
thetextislosslesslycompressed. Thisvalueisainputvectorcapacityintermsofentropy(InformationGain,C ).
H
Fortextsthatarenotperfectlycompressed,thecompressionprocessreducestheirCEtoaconsistent,model-specific
value(biasoftheblackdashedline). Largermodels(e.g.,Llama-3.1-8B)canhandlelongertextsbeforereachingthe
compressionthreshold,duetotheirgreatercapacitycomparedtosmallermodels(e.g.,Pythia-160M).Thisbehavior
holdsforbothnaturaltexts(PG-19)andunnaturalrandomtextsconsistingofrandomwordsequences. Theresultis
notlimitedtotransformer-basedarchitectures: non-transformermodels,suchasMamba,exhibitthesamepattern.
16

6
5
4
3
2
1
0
0.0 0.2 0.4 0.6 0.8
Cosine similarity
ytisneD
Intra-sample
Inter-sample
Figure7: Intra/inter-sampleembeddingscosinesimi-
larity. Empiricalprobabilitydensitiesofcosinesimilar-
itybetweenintra-sampleandinter-sampleembeddings.
Intra-samplesimilaritiesaremeasuredbetweenofthe
samesequenceoftokens,whileinter-samplebetween
differentones. MeasuredonGovReport(Huangetal.,
2021)andSheared-Llama-1.3B(Xiaetal.,2024).
1.0
0.8
0.6
0.4
0.2
0.0
0.0 0.2 0.4 0.6 0.8 1.0
ycaruccA
Figure8: Intra-sampleInterpolationAccuracies. In-
terpolationlinesareprovidedforallpairsbetween32
embeddings of the same input sequence. All interpo-
lationlinesareprintedwithhightransparencytoshow
denserregions. Greylinesdepictminimumsandmaxi-
mumsoftheaccuracyforagiveninterpolationparame-
terθ.
17