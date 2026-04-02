|     |     | Text | Embeddings |     | Reveal |     | (Almost) | As  | Much | As Text |     |     |
| --- | --- | ---- | ---------- | --- | ------ | --- | -------- | --- | ---- | ------- | --- | --- |
JohnX.Morris,VolodymyrKuleshov,VitalyShmatikov,AlexanderM.Rush
DepartmentofComputerScience
CornellUniversity
|     |     | Abstract |     |     |     |     | impossible | to  | invert exactly. |     | Furthermore, | when |
| --- | --- | -------- | --- | --- | --- | --- | ---------- | --- | --------------- | --- | ------------ | ---- |
queryinganeuralnetworkthroughtheinternet,we
How much private information do text em- maynothaveaccesstothemodelweightsorgradi-
| beddings | reveal | about | the original |     | text? | We  |     |     |     |     |     |     |
| -------- | ------ | ----- | ------------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
entsatall.
| investigate | the | problem | of  | embedding | inver- |     |     |     |     |     |     |     |
| ----------- | --- | ------- | --- | --------- | ------ | --- | --- | --- | --- | --- | --- | --- |
3202 tcO 01  ]LC.sc[  1v61860.0132:viXra
|       |                |     |          |                  |     |     | Still, | given | input-output | pairs | from | a network, |
| ----- | -------------- | --- | -------- | ---------------- | --- | --- | ------ | ----- | ------------ | ----- | ---- | ---------- |
| sion, | reconstructing |     | the full | text represented |     |     |        |       |              |       |      |            |
indensetextembeddings. Weframetheprob- it is often possible to approximate the network’s
inversion
lemascontrolledgeneration: generatingtext inverse. Work on in computer vision
that,whenreembedded,isclosetoafixedpoint (Mahendran and Vedaldi, 2014; Dosovitskiy and
| inlatentspace. |     | Wefindthatalthoughanaïve |     |     |     |     |     |     |     |     |     |     |
| -------------- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Brox,2016)hasshownthatitispossibletolearn
modelconditionedontheembeddingperforms
torecovertheinputimage(withsomeloss)given
poorly,amulti-stepmethodthatiterativelycor-
|     |     |     |     |     |     |     | thelogitsofthefinallayer. |     |     | Preliminaryworkhas |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | ------------------ | --- | --- |
rectsandre-embedstextisabletorecover92%
|             |     |             |          |     |       |     | explored | this | question | for text | (Song | and Raghu- |
| ----------- | --- | ----------- | -------- | --- | ----- | --- | -------- | ---- | -------- | -------- | ----- | ---------- |
| of 32-token |     | text inputs | exactly. | We  | train | our |          |      |          |          |       |            |
model to decode text embeddings from two nathan, 2020), but only been able to recover an
state-of-the-art embedding models, and also approximatebagofwordsgivenembeddingsfrom
| showthatourmodelcanrecoverimportantper- |     |     |     |     |     |     | shallownetworks. |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- |
sonalinformation(fullnames)fromadataset Inthiswork,wetargetfullreconstructionofin-
| ofclinicalnotes. |     | 1   |     |     |     |     |                          |     |     |                       |                      |     |
| ---------------- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | --------------------- | -------------------- | --- |
|                  |     |     |     |     |     |     | puttextfromitsembedding. |     |     |                       | Iftextisrecoverable, |     |
|                  |     |     |     |     |     |     | thereisathreattoprivacy: |     |     | amalicioususerwithac- |                      |     |
1 Introduction
cesstoavectordatabase,andtext-embeddingpairs
Systemsthatutilizelargelanguagemodels(LLMs) from the model used to produce the data, could
often store auxiliary data in a vector database of learnafunctionthatreproducestextfromembed-
| dense embeddings |     | (Borgeaud |     | et al., | 2022; | Yao | dings. |     |     |     |     |     |
| ---------------- | --- | --------- | --- | ------- | ----- | --- | ------ | --- | --- | --- | --- | --- |
etal.,2023). Usersofthesesystemsinfuseknowl- Weframethisproblemofrecoveringtextualem-
edgeintoLLMsbyinsertingretrieveddocuments beddingsasacontrolledgenerationproblem,where
into the language model’s prompt. Practition- weseektogeneratetextsuchthatthetextisasclose
ersareturningtohostedvectordatabaseservices
|     |     |     |     |     |     |     | as possible | to  | a given | embedding. |     | Our method, |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------- | ---------- | --- | ----------- |
to execute embedding search efficiently at scale Vec2Text,usesthedifferencebetweenahypothesis
(Pinecone;Qdrant;Vdaas;Weaviate;LangChain). embeddingandaground-truthembeddingtomake
Inthesedatabases,thedataowneronlysendsem-
discreteupdatestothetexthypothesis.
beddingsoftextdata(LeandMikolov,2014;Kiros
Whenweembedwebdocumentsusingastate-of-
et al., 2015) to the third party service, and never the-artblack-boxencoder,ourmethodcanrecover
thetextitself. Thedatabaseserverreturnsasearch 32-tokeninputswithanear-perfectBLEUscoreof
| result as | the index | of  | the matching |     | document | on  |     |     |     |     |     |     |
| --------- | --------- | --- | ------------ | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
97.3,andcanrecover92%oftheexamplesexactly.
theclientside.
|     |     |     |     |     |     |     | We then | evaluate | on embeddings |     | generated | from |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------- | ------------- | --- | --------- | ---- |
Vector databases are increasingly popular, but a variety of common retrieval corpuses from the
privacythreatswithinthemhavenotbeencompre-
|           |           |     |         |       |               |     | BEIR | benchmark. | Even | though | these | texts were |
| --------- | --------- | --- | ------- | ----- | ------------- | --- | ---- | ---------- | ---- | ------ | ----- | ---------- |
| hensively | explored. |     | Can the | third | party service |     |      |            |      |        |       |            |
notseenduringtraining,ourmethodisabletoper-
toreproducetheinitialtext,givenitsembedding? fectlyrecovertheinputsforanumberofdatapoints
Neuralnetworksareingeneralnon-trivialoreven across a variety of domains. We evaluate on em-
|      |      |     |           |     |     |         | beddings | of clinical | notes | from | MIMIC | and are |
| ---- | ---- | --- | --------- | --- | --- | ------- | -------- | ----------- | ----- | ---- | ----- | ------- |
| 1Our | code | is  | available |     | on  | Github: |          |             |       |      |       |         |
abletorecover89%offullnamesfromembedded
github.com/jxmorris12/vec2text.

Φ
|     |     | x0  |     |     |     |     |     |     |     |     | Target embedding |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- |
Mage (foaled April 18, 2020) is an
American Thoroughbred racehorse who
won the 2023 Kentucky Derby.
Correction
Kentucky Derby, which was won by Mage
(April 20, 2010), who is an American
Thoroughbred horse and mare.
Figure1: Overviewofourmethod,Vec2Text. Givenaccesstoatargetembeddinge(blue)andqueryaccesstoan
embeddingmodelϕ(bluemodel),thesystemaimstoiterativelygenerate(yellowmodel)hypotheseseˆ(pink)to
reachthetarget. ExampleinputisatakenfromarecentWikipediaarticle(June2023). Vec2Textperfectlyrecovers
thistextfromitsembeddingafter4roundsofcorrection.
notes. These results imply that text embeddings Assumptionsofourthreatmodel. Inapractical
presentthesamethreatstoprivacyasthetextfrom sense,weconsiderthescenariowhereanattacker
whichtheyarecomputed,andembeddingsshould wantstoinvertasingleembeddingproducedfrom
betreatedwiththesameprecautionsasrawdata. a black-box embedder ϕ. We assume that the at-
|     |     |     |     |     |     |     | tackerhasaccesstoϕ: |     |     | givenhypothesistextxˆ,the |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | ------------------------- | --- | --- | --- |
attackercanquerythemodelforϕ(xˆ)andcompute
| 2 Overview: |     | EmbeddingInversion |     |     |     |     |               |      |      |      |               |     |         |
| ----------- | --- | ------------------ | --- | --- | --- | --- | ------------- | ---- | ---- | ---- | ------------- | --- | ------- |
|             |     |                    |     |     |     |     | cos(ϕ(xˆ),e). | When | this | term | is 1 exactly, |     | the at- |
tackercanbesurethatxˆwastheoriginaltext,i.e.
| Text embedding |     | models |     | learn | to map | text se- |     |     |     |     |     |     |     |
| -------------- | --- | ------ | --- | ----- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
collisionsarerareandcanbeignored.
| quences     | to embedding |         | vectors. |        | Embedding | vec-       |           |          |     |     |     |     |     |
| ----------- | ------------ | ------- | -------- | ------ | --------- | ---------- | --------- | -------- | --- | --- | --- | --- | --- |
| tors are    | useful       | because | they     | encode | some      | notion     |           |          |     |     |     |     |     |
|             |              |         |          |        |           |            | 3 Method: | Vec2Text |     |     |     |     |     |
| of semantic | similarity:  |         | inputs   | that   | are       | similar in |           |          |     |     |     |     |     |
meaningshouldhaveembeddingsthatareclosein
|                                 |     |     |     |     |            |     | 3.1 BaseModel: |     | LearningtoInvertϕ |           |     |            |     |
| ------------------------------- | --- | --- | --- | --- | ---------- | --- | -------------- | --- | ----------------- | --------- | --- | ---------- | --- |
| vectorspace(Mikolovetal.,2013). |     |     |     |     | Embeddings |     |                |     |                   |           |     |            |     |
|                                 |     |     |     |     |            |     | Enumerating    | all | possible          | sequences |     | to compute |     |
arecommonlyusedformanytaskssuchassearch,
clustering,andclassification(AggarwalandZhai, Equation (1) is computationally infeasible. One
|     |     |     |     |     |     |     | way to avoid | this | computational |     | constraint |     | is by |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ---- | ------------- | --- | ---------- | --- | ----- |
2012;Neelakantanetal.,2022;Muennighoffetal.,
learningadistributionoftextsgivenembeddings.
2023).
|                             |     |     |     |     |     | Vn,atext | GivenadatasetoftextsD |     |     | =   | {x 1 ,...},welearnto |     |     |
| --------------------------- | --- | --- | --- | --- | --- | -------- | --------------------- | --- | --- | --- | -------------------- | --- | --- |
| Givenatextsequenceoftokensx |     |     |     |     | ∈   |          |                       |     |     |     |                      |     |     |
invertencoderϕbylearningadistributionoftexts
|                  | ϕ : Vn | →   | Rd    | x   |                |     |                   |     |     |         |             |     |       |
| ---------------- | ------ | --- | ----- | --- | -------------- | --- | ----------------- | --- | --- | ------- | ----------- | --- | ----- |
| encoder          |        |     | maps  | to  | a fixed-length |     |                   |     |     |         |             |     |       |
|                  |        |     |       |     |                |     | given embeddings, |     | p(x | | e;θ), | by learning |     | θ via |
| embeddingvectore |        |     | ∈ Rd. |     |                |     |                   |     |     |         |             |     |       |
maximumlikelihood:
| Now         | consider                    | the | problem | of  | inverting | textual |     |       |      |      |             |     |     |
| ----------- | --------------------------- | --- | ------- | --- | --------- | ------- | --- | ----- | ---- | ---- | ----------- | --- | --- |
| embeddings: | givensomeunknownencoderϕ,we |     |         |     |           |         |     |       |      |      |             |     |     |
|             |                             |     |         |     |           |         | θ   | = arg | maxE | [p(x | | ϕ(x);θˆ)] |     |     |
x∼D
| seek to   | recover | the       | text | x given | its embedding |           |     |     | θˆ  |     |     |     |     |
| --------- | ------- | --------- | ---- | ------- | ------------- | --------- | --- | --- | --- | --- | --- | --- | --- |
| e = ϕ(x). | Text    | embedding |      | models  | are           | typically |     |     |     |     |     |     |     |
trainedtoencouragesimilaritybetweenrelatedin- We drop the θ hereon for simplicity of notation.
puts(Karpukhinetal.,2020). Thus,wecanwrite Inpractice,thisprocessinvolvestrainingacondi-
tionallanguagemodeltoreconstructunknowntext
| the problem | as  | recovering |     | text | that has | a maxi- |     |     |     |     |     |     |     |
| ----------- | --- | ---------- | --- | ---- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- |
mallysimilarembeddingtotheground-truth. We xgivenitsembeddinge = ϕ(x). Wecanviewthis
canformalizethesearchfortextxˆwithembedding learningproblemasamortizingthecombinatorial
|     |     |     |     |     |     |     | optimization | (Equation |     | (1)) | into the | weights | of a |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --------- | --- | ---- | -------- | ------- | ---- |
eunderencoderϕasoptimization:
|     |     |     |     |     |     |     | neuralnetwork. |     | Directlylearningtogeneratesat- |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------------------------------ | --- | --- | --- | --- |
isfactorytextinthismanneriswell-knowninthe
|     | xˆ  | = argmaxcos(ϕ(x),e) |     |     |     | (1) | literaturetobeadifficultproblem. |     |     |     |     |     |     |
| --- | --- | ------------------- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | --- | --- |
x

3.2 ControllingGenerationforInversion whichrequiresasequenceofembeddingsasinput
with some dimension d not necessarily equal
Toimproveuponthismodel,weproposeVec2Text enc
tothedimensiondofϕ’sembeddings. Similarto
shown in Figure 1. This approach takes inspira-
Mokadyetal.(2021),weusesmallMLPtoproject
tionfrommethodsforControlledGeneration,the
a single embedding vector to a larger size, and
taskofgeneratingtextthatsatisfiesaknowncon-
reshapetogiveitasequencelengthasinputtothe
dition (Hu et al., 2018; John et al., 2018; Yang
encoder. Forembeddinge ∈ Rd:
andKlein,2021). Thistaskissimilartoinversion
inthatthereisaobservablefunctionϕthatdeter-
mines the level of control. However, it differs in EmbToSeq(e) = W σ(W e)
2 1
thatapproachestocontrolledgeneration(Dathathri
etal.,2020;Lietal.,2022)generallyrequirediffer- whereW
1
∈ Rd×d andW
2
∈ R(sdenc)×d forsome
entiatingthroughϕtoimprovethescoreofsome nonlinearactivationfunctionσ andpredetermined
intermediaterepresentation. Textualinversiondif- encoder “length” s. We use a separate MLP to
fers in that we can only make queries to ϕ, and projectthreevectors: theground-truthembedding
cannotcomputeitsgradients. e, the hypothesis embedding eˆ(t), and the differ-
encebetweenthesevectorse−eˆ. Giventheword
Model. The method guesses an initial hypoth-
embeddingsofthehypothesisx(t) are{w ...w },
1 n
esis and iteratively refines this hypothesis by re-
the input (length 3s+n) to the encoder is as fol-
embeddingandcorrectingthehypothesistobring
lows:
itsembeddingclosertoe. Notethatthismodelre-
quirescomputinganewembeddingeˆ(t) = ϕ(x(t))
concat(EmbToSeq(e),
in order to generate each new correction x(t+1).
Wedefineourmodelrecursivelybymarginalizing
EmbToSeq(eˆ(t)),
overintermediatehypotheses: EmbToSeq(e−eˆ(t)),(w ...w ))
1 n
(cid:88) Wefeedtheconcatenatedinputtotheencoderand
p(x(t+1) | e) = p(x(t) | e)p(x(t+1) | e,x(t),eˆ(t))
trainthefullencoder-decodermodelusingstandard
x(t)
languagemodelingloss.
eˆ(t) = ϕ(x(t))
Inference. In practice we cannot tractably sum
withabasecaseofthesimplelearnedinversion: out intermediate generations x(t), so we approxi-
matethissummationviabeamsearch. Weperform
p(x(0) | e) = p(x(0) | e,∅,ϕ(∅))
inferencefromourmodelgreedilyatthetokenlevel
Here,x(0) representstheinitialhypothesisgener- butimplementbeamsearchatthesequence-level
ation, x(1) the correction of x(0), and so on. We x(t). Ateachstepofcorrection,weconsidersome
trainthismodelbyfirstgeneratinghypothesesx(0) numberbofpossiblecorrectionsasthenextstep.
fromthemodelinSection3.1,computingeˆ(0),and For each possible correction, we decode the top
b possible continuations, and then take the top b
thentrainingamodelonthisgenerateddata.
unique continuations out of b·b potential contin-
Thismethodrelatestootherrecentworkgener-
uationsbymeasuringtheirdistanceinembedding
atingtextthroughiterativeediting(Leeetal.,2018;
spacetotheground-truthembeddinge.
Ghazvininejad et al., 2019). Especially relevant
is Welleck et al. (2022), which proposes to train
4 ExperimentalSetup
atext-to-text‘self-correction’moduletoimprove
languagemodelgenerationswithfeedback.
Embeddings. Vec2Textistrainedtoinverttwo
Parameterization. Thebackboneofourmodel, state-of-the-artembeddingmodels: GTR-base(Ni
p(x(t+1) | e,x(t),eˆ(t)),isparameterizedasastan- et al., 2021), a T5-based pre-trained transformer
dardencoder-decodertransformer(Vaswanietal., fortextretrieval,andtext-embeddings-ada-002
2017;Raffeletal.,2020)conditionedontheprevi- available via the OpenAI API. Both model fami-
ousoutput. liesareamongthehighest-performingembedders
Onechallengeistheneedtoinputconditioning ontheMTEBtextembeddingsbenchmark(Muen-
embeddingseandeˆ(t) intoatransformerencoder, nighoffetal.,2023).

|     | method                                |     |     |     | tokens | predtokens | bleu | tf1 | exact | cos  |
| --- | ------------------------------------- | --- | --- | --- | ------ | ---------- | ---- | --- | ----- | ---- |
|     | Bag-of-words(SongandRaghunathan,2020) |     |     |     | 32     | 32         | 0.3  | 51  | 0.0   | 0.70 |
|     | GPT-2Decoder(Lietal.,2023)            |     |     |     | 32     | 32         | 1.0  | 47  | 0.0   | 0.76 |
snoitseuQlarutaN
|     | Base[0steps]  |     |     |     | 32  | 32  | 31.9 | 67  | 0.0 | 0.91 |
| --- | ------------- | --- | --- | --- | --- | --- | ---- | --- | --- | ---- |
|     | (+beamsearch) |     |     |     | 32  | 32  | 34.5 | 67  | 1.0 | 0.92 |
RTG
|     | (+nucleus)      |     |     |     | 32   | 32   | 25.3 | 60  | 0.0  | 0.88 |
| --- | --------------- | --- | --- | --- | ---- | ---- | ---- | --- | ---- | ---- |
|     | Vec2Text[1step] |     |     |     | 32   | 32   | 50.7 | 80  | 0.0  | 0.96 |
|     | [20steps]       |     |     |     | 32   | 32   | 83.9 | 96  | 40.2 | 0.99 |
|     | [50steps]       |     |     |     | 32   | 32   | 85.4 | 97  | 40.6 | 0.99 |
|     | [50steps+sbeam] |     |     |     | 32   | 32   | 97.3 | 99  | 92.0 | 0.99 |
|     | Base[0steps]    |     |     |     | 31.8 | 31.8 | 26.2 | 61  | 0.0  | 0.94 |
OCRAMSM
|     | Vec2Text[1step] |     |     |     | 31.8 | 31.9 | 44.1 | 77  | 5.2 | 0.96 |
| --- | --------------- | --- | --- | --- | ---- | ---- | ---- | --- | --- | ---- |
IAnepO
|     | [20steps]       |     |     |     | 31.8 | 31.9 | 61.9 | 87  | 15.0 | 0.98 |
| --- | --------------- | --- | --- | --- | ---- | ---- | ---- | --- | ---- | ---- |
|     | [50steps]       |     |     |     | 31.8 | 31.9 | 62.3 | 87  | 14.8 | 0.98 |
|     | [50steps+sbeam] |     |     |     | 31.8 | 31.8 | 83.4 | 96  | 60.9 | 0.99 |
|     | Base[0steps]    |     |     |     | 80.9 | 84.2 | 17.0 | 54  | 0.6  | 0.95 |
OCRAMSM
| IAnepO | Vec2Text[1step] |     |     |     | 80.9 | 81.6 | 29.9 | 68  | 1.4 | 0.97 |
| ------ | --------------- | --- | --- | --- | ---- | ---- | ---- | --- | --- | ---- |
|        | [20steps]       |     |     |     | 80.9 | 79.7 | 43.1 | 78  | 3.2 | 0.99 |
|        | [50steps]       |     |     |     | 80.9 | 80.5 | 44.4 | 78  | 3.4 | 0.99 |
|        | [50steps+sbeam] |     |     |     | 80.9 | 80.6 | 55.0 | 84  | 8.0 | 0.99 |
Table1: Reconstructionscoreonin-domaindatasets. Topsectionofresultscomefrommodelstrainedtoreconstruct
32tokensoftextfromWikpedia, embeddedusingGTR-base. Remainingresultscomefrommodelstrainedto
reconstructupto32or128tokensfromMSMARCO,embeddedusingOpenAItext-embeddings-ada-002.
Datasets. WetrainourGTRmodelon5M pas- Metrics. Weusetwotypesofmetricstomeasure
sages from Wikipedia articles selected from the theprogressandtheaccuracyofreconstructedtext.
Natural Questions corpus (Kwiatkowski et al., Firstweconsiderourmaingoaloftextreconstruc-
2019) truncated to 32 tokens. We train our two tion. Tomeasurethisweuseword-matchmetrics
OpenAI models (Bajaj et al., 2018), both on ver- including: BLEU score (Papineni et al., 2002), a
sionsoftheMSMARCOcorpuswithmaximum32 measure of n-gram similarities between the true
or 128 tokens per example 2. For evaluation, we and reconstructed text; Token F1, the multi-class
considertheevaluationdatasetsfromNaturalQues- F1 score between the set of predicted tokens and
tionsandMSMarco,aswellastwoout-of-domain the set of true tokens; Exact-match, the percent-
settings: theMIMIC-IIIdatabaseofclinicalnotes ageofreconstructedoutputsthatperfectlymatch
(Johnson et al., 2016) in addition to the variety theground-truth. Wealsoreportthesimilarityon
of datasets available from the BEIR benchmark theinternalinversionmetricintermsofrecovering
(Thakuretal.,2021). thevectorembeddinginlatentspace. Weuseco-
sinesimilaritybetweenthetrueembeddingandthe
| Baseline. | Asabaseline,wetrainthebasemodel |     |     |     |     |     |     |     |     |     |
| --------- | ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
embeddingofreconstructedtextaccordingtoϕ.
p(x(0)
| e)torecovertextwithnocorrectionsteps.
| We                        | also evaluate | the bag | of words        | model from |                     |     |                       |     |     |     |
| ------------------------- | ------------- | ------- | --------------- | ---------- | ------------------- | --- | --------------------- | --- | --- | --- |
|                           |               |         |                 |            | ModelsandInference. |     | Weinitializeourmodels |     |     |     |
| SongandRaghunathan(2020). |               |         | Tobalanceforthe |            |                     |     |                       |     |     |     |
fromtheT5-basecheckpoint(Raffeletal.,2020).
| increased | number | of queries | allotted | to the cor- |     |     |     |     |     |     |
| --------- | ------ | ---------- | -------- | ----------- | --- | --- | --- | --- | --- | --- |
Includingtheprojectionhead,eachmodelhasap-
rectionmodels,wealsoconsidertakingthetop-N
|     |     |     |     |     | proximately235Mparameters. |     |     | Wesettheprojec- |     |     |
| --- | --- | --- | --- | --- | -------------------------- | --- | --- | --------------- | --- | --- |
predictionsmadefromtheunconditionalmodelvia
|                                |     |     |     |           | tion sequence  | length      | s = 16 | for all          | experiments, |     |
| ------------------------------ | --- | --- | --- | --------- | -------------- | ----------- | ------ | ---------------- | ------------ | --- |
| beamsearchandnucleussampling(p |     |     |     | = 0.9)and |                |             |        |                  |              |     |
|                                |     |     |     |           | as preliminary | experiments |        | show diminishing |              | re- |
rerankingviacosinesimilarity.
|     |     |     |     |     | turns by increasing | this | number | further. | We  | per- |
| --- | --- | --- | --- | --- | ------------------- | ---- | ------ | -------- | --- | ---- |
forminferenceonallmodelsusinggreedytoken-
2By2023pricingof$0.0001per1000tokens,embedding
|     |     |     |     |     | level decoding. | When | running | multiple | steps | of  |
| --- | --- | --- | --- | --- | --------------- | ---- | ------- | -------- | ----- | --- |
5milliondocumentsof70tokenseachcosts$35.

2∗10−4
dataset tokens method bleu tokenF1 withwarmupandlineardecay. Wetrain
|       |      |           |      | modelsfor100epochs. |     |     |     | Weusebatchsizeof128 |     |     |     |
| ----- | ---- | --------- | ---- | ------------------- | --- | --- | --- | ------------------- | --- | --- | --- |
|       |      | Base 36.2 | 73.8 |                     |     |     |     |                     |     |     |     |
| quora | 15.7 |           |      |                     |     |     |     |                     |     |     |     |
Vec2Text 95.5 98.6 and train all models on 4 NVIDIA A6000 GPUs.
|               |      | Base 13.2     | 49.5 | Undertheseconditions,trainingourslowestmodel |                 |          |           |           |          |     |        |
| ------------- | ---- | ------------- | ---- | -------------------------------------------- | --------------- | -------- | --------- | --------- | -------- | --- | ------ |
| signal1m      | 23.7 |               |      |                                              |                 |          |           |           |          |     |        |
|               |      | Vec2Text 80.7 | 92.5 | takesabouttwodays.                           |                 |          |           |           |          |     |        |
|               |      | Base 15.5     | 54.1 |                                              |                 |          |           |           |          |     |        |
| msmarco       | 72.1 |               |      | 5                                            | Results         |          |           |           |          |     |        |
|               |      | Vec2Text 59.6 | 86.1 |                                              |                 |          |           |           |          |     |        |
|               |      | Base 12.8     | 49.3 |                                              |                 |          |           |           |          |     |        |
| climate-fever | 73.4 |               |      | 5.1                                          | Reconstruction: |          |           | In-Domain |          |     |        |
|               |      | Vec2Text 44.9 | 82.6 |                                              |                 |          |           |           |          |     |        |
|               |      |               |      | Table                                        | 1               | contains | in-domain |           | results. | Our | method |
|               |      | Base 12.6     | 49.2 |                                              |                 |          |           |           |          |     |        |
| fever         | 73.4 |               |      |                                              |                 |          |           |           |          |     |        |
Vec2Text 45.1 82.7 outperforms the baselines on all metrics. More
|                |      | Base 15.4     | 50.3 | roundsismonotonicallyhelpful,althoughwesee |      |       |     |        |        |                |     |
| -------------- | ---- | ------------- | ---- | ------------------------------------------ | ---- | ----- | --- | ------ | ------ | -------------- | --- |
| dbpedia-entity | 91.3 |               |      |                                            |      |       |     |        |        |                |     |
|                |      | Vec2Text 48.0 | 77.9 | diminishingreturns–weareabletorecover77%   |      |       |     |        |        |                |     |
|                |      | Base 11.0     | 47.1 | of                                         | BLEU | score | in  | just 5 | rounds | of correction, | al- |
| nq             | 94.7 |               |      |                                            |      |       |     |        |        |                |     |
Vec2Text 32.7 72.7 though running for 50 rounds indeed achieves a
|          |      | Base 15.4 | 50.1 | higher |     | reconstruction |     | performance. |     | We find | that |
| -------- | ---- | --------- | ---- | ------ | --- | -------------- | --- | ------------ | --- | ------- | ---- |
| hotpotqa | 94.8 |           |      |        |     |                |     |              |     |         |      |
Vec2Text 46.6 78.7 runningsequence-levelbeamsearch(sbeam)over
|                  |       | Base 6.6      | 44.1 | theiterativereconstructionisparticularlyhelpful |         |           |           |       |                     |           |       |
| ---------------- | ----- | ------------- | ---- | ----------------------------------------------- | ------- | --------- | --------- | ----- | ------------------- | --------- | ----- |
| fiqa             | 103.8 |               |      |                                                 |         |           |           |       |                     |           |       |
|                  |       | Vec2Text 21.5 | 63.6 |                                                 |         |           |           |       |                     |           |       |
|                  |       |               |      | for                                             | finding | exact     | matches   |       | of reconstructions, |           | in-   |
|                  |       | Base 6.6      | 41.5 | creasing                                        |         | the       | exact     | match | score               | by 2 to 6 | times |
| webis-touche2020 | 105.2 |               |      |                                                 |         |           |           |       |                     |           |       |
|                  |       | Vec2Text 19.6 | 69.7 |                                                 |         |           |           |       |                     |           |       |
|                  |       |               |      | across                                          |         | the three | settings. |       | In a relative       | sense,    | the   |
|                  |       | Base 7.1      | 41.5 |                                                 |         |           |           |       |                     |           |       |
| cqadupstack      | 106.4 |               |      | modelhasmoretroubleexactlyrecoveringlonger      |         |           |           |       |                     |           |       |
|                  |       | Vec2Text 23.3 | 64.3 |                                                 |         |           |           |       |                     |           |       |
texts,butstillisabletogetmanyofthewords.
|            |       | Base 6.8      | 44.1 |                                             |                 |     |           |               |                |          |     |
| ---------- | ----- | ------------- | ---- | ------------------------------------------- | --------------- | --- | --------- | ------------- | -------------- | -------- | --- |
| arguana    | 113.5 |               |      |                                             |                 |     |           |               |                |          |     |
|            |       | Vec2Text 23.4 | 66.3 | 5.2                                         | Reconstruction: |     |           | Out-of-Domain |                |          |     |
|            |       | Base 5.9      | 38.5 |                                             |                 |     |           |               |                |          |     |
| scidocs    | 125.3 |               |      | We                                          | evaluate        |     | our model |               | on 15 datasets | from     | the |
|            |       | Vec2Text 17.7 | 57.6 |                                             |                 |     |           |               |                |          |     |
|            |       |               |      | BEIR                                        | benchmark       |     | and       | display       | results        | in Table | 2.  |
|            |       | Base 5.6      | 36.3 |                                             |                 |     |           |               |                |          |     |
| trec-covid | 125.4 |               |      | Quora,theshortestdatasetinBEIR,istheeasiest |                 |     |           |               |                |          |     |
|            |       | Vec2Text 19.3 | 58.6 |                                             |                 |     |           |               |                |          |     |
toreconstruct,andourmodelisabletoexactlyre-
|          |       | Base 4.9 | 34.4 |     |     |     |     |     |     |     |     |
| -------- | ----- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
| robust04 | 127.3 |          |      |     |     |     |     |     |     |     |     |
Vec2Text 15.5 54.5 cover 66% of examples. Our model adapts well
todifferent-lengthinputs,generallyproducingre-
|     |     | Base 5.3 | 35.7 |     |     |     |     |     |     |     |     |
| --- | --- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
bioasq 127.4 constructions with average length error of fewer
|         |       | Vec2Text 22.8 | 59.5 |              |     |     |                                  |     |     |     |     |
| ------- | ----- | ------------- | ---- | ------------ | --- | --- | -------------------------------- | --- | --- | --- | --- |
|         |       |               |      | than3tokens. |     |     | Ingeneral,reconstructionaccuracy |     |     |     |     |
|         |       | Base 4.9      | 35.2 |              |     |     |                                  |     |     |     |     |
| scifact | 127.4 |               |      |              |     |     |                                  |     |     |     |     |
Vec2Text 16.6 56.6 inverselycorrelateswithexamplelength(discussed
|           |       |               |      | moreinSection7).                            |     |     |     | Onalldatasets,weareableto |     |     |     |
| --------- | ----- | ------------- | ---- | ------------------------------------------- | --- | --- | --- | ------------------------- | --- | --- | --- |
|           |       | Base 6.2      | 39.6 |                                             |     |     |     |                           |     |     |     |
| nfcorpus  | 127.7 |               |      |                                             |     |     |     |                           |     |     |     |
|           |       | Vec2Text 25.8 | 64.8 | recoversequenceswithTokenF1ofatleast41and   |     |     |     |                           |     |     |     |
|           |       | Base 4.9      | 34.8 | cosinesimilaritytothetrueembeddingofatleast |     |     |     |                           |     |     |     |
| trec-news | 128.0 |               |      |                                             |     |     |     |                           |     |     |     |
|           |       | Vec2Text 14.5 | 51.5 | 0.95.                                       |     |     |     |                           |     |     |     |
Table 2: Out-of-domain reconstruction performance 5.3 Casestudy: MIMIC
| measuredondatasetsfromtheBEIRbenchmark. |     |     | We  |     |     |     |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Asaspecificthreatdomain,weconsiderMIMIC-
sortdatasetsinorderofaveragelengthinordertoem-
|     |     |     |     | III | clinical | notes | (Johnson |     | et al., | 2016). Because |     |
| --- | --- | --- | --- | --- | -------- | ----- | -------- | --- | ------- | -------------- | --- |
phasizetheeffectofsequencelengthontaskdifficulty.
theoriginalreleaseofMIMICiscompletelydeiden-
tified,weinsteadusethe“pseudore-identified”ver-
sequence-level beam search, we only take a new sionfromLehmanetal.(2021)wherefakenames
generationifitiscloserthanthepreviousstepin havebeeninsertedintheplaceofthedeidentified
| cosinesimilaritytotheground-truthembedding. |     |     |     | ones. |     |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
Weuseunconditionalmodelstoseedtheinitial
Eachnoteistruncatedto32tokensandthenotes
hypothesis for our iterative models. We examine are filtered so that they each contain at least one
theeffectofusingadifferentinitialhypothesisin name. We measure the typical statistics of our
| Section7. |     |     |     | methodaswellasthreenewones: |     |     |     |     |     | thepercentage |     |
| --------- | --- | --- | --- | --------------------------- | --- | --- | --- | --- | --- | ------------- | --- |
WeusetheAdamoptimizerandlearningrateof of first names, last names, and complete names

method first last full bleu tf1 exact cos
0.30
Base 40.0 27.8 10.8 4.9 33.1 0. 0.78
0.25
Vec2Text 94.2 95.3 89.2 55.6 80.8 26.0 0.98
0.20
MIMIC-III Entity reconstruction rate 0.15
Clinical event
0.10 Nonbiological location
Therapeutic procedure 0.05
Lab value 0.00
Biological structure 10 3 10 2 10 1 100
Noise Level ( )
Sign symptom
Disease disorder
Medication
Diagnostic procedure
Detailed description
0.0 0.2 0.4 0.6 0.8 1.0
Table3: Performanceofourmethodonreconstructing
GTR-embeddedclinicalnotesfromMIMICIII(Johnson
etal.,2016).
that are recovered. Results are shown in Table 3.
Vec2Text is able to recover 94% of first names,
95% of last names, and 89% of full names (first,
last format) while recovering 26% of the docu-
mentsexactly.
FortherecoveredclinicalnotesfromSection5.3,
we extract entities from each true and recovered
note using a clinical entity extractor (Raza et al.,
2022). Weplottherecoverypercentagein3(bot-
tom) with the average entity recovery shown as
a dashed line. Our model is most accurate at re-
constructingentitiesofthetype“ClinicalEvent”,
whichincludegenericmedicalwordslike‘arrived’,
‘progress’, and ‘transferred’. Our model is least
accurate in the “Detailed Description” category,
whichincludesspecificmedicalterminologylike
‘posterior’ and ‘hypoxic’, as well as multi-word
eventslike‘invasiveventilation-stop4:00pm’.
Although we are able to recover 26% of 32-
tokennotesexactly,thenotesthatwerenotexactly
recovered are semantically close to the original.
Ourmodelgenerallymatchesthesyntaxofnotes,
even when some entities are slightly garbled; for
example,giventhefollowingsentencefromadoc-
tor’snote“RhonaArntsonnpn/-#resp: infantre-
mains orally intubated on imv / r fi” our model
predicts“RhonaArpsonnrft:#infantremainsintu-
batedorallyonresp. imv. m/nfi”.
6 Defendingagainstinversionattacks
Isiteasyforusersoftextembeddingmodelspro-
tecttheirembeddingsfrominversionattacks? We
considerabasicdefensescenarioasasanitycheck.
Toimplementourdefense,theuseraddesalevelof
)01@GCDN
naeM(
laveirteR
80
60
40
20
0
)UELB(
noitcurtsnoceR
Retrieval
Reconstruction
Figure2: Retrievalperformanceandreconstructionac-
curacyacrossvaryinglevelsofnoiseinjection.
Gaussian noise directly to each embedding with
the goal of effectively defending against inver-
sionattackswhilepreservingutilityinthenearest-
neightborretrievalsetting. Weanalyzethetrade-off
betweenretrievalperformanceandreconstruction
accuracyundervaryinglevelsofnoise.
Formally,wedefineanewembeddingmodelas:
ϕ (x) = ϕ(x)+λ·ϵ,ϵ ∼ N(0,1)
noisy
whereλisahyperparametercontrollingtheamount
ofnoiseinjected.
WesimulatethisscenariowithϕasGTR-base
using our self-corrective model with 10 steps of
correction, given the noisy embedder ϕ . To
noisy
measureretrievalperformance,wetakethemean
NDCG@10 (a metric of retrieval performance;
higherisbetter)across15differentretrievaltasks
fromtheBEIRbenchmark,evaluatedacrossvary-
inglevelsofnoise.
We graph the average retrieval performance in
Figure 2 (see A.2 for complete tables of results).
Atanoiselevelofλ = 10−1,weseeretrievalper-
formance is preserved, while BLEU score drops
by10%. Atanoiselevelof0.01,retrievalperfor-
mance is barely degraded (2%) while reconstruc-
tionperformanceplummetsto13%oftheoriginal
BLEU. Adding any additional noise severely im-
pactsbothretrievalperformanceandreconstruction
accuracy. Theseresultsindicatethataddingasmall
amountofGaussiannoisemaybeastraightforward
way to defend against naive inversion attacks, al-
thoughitispossiblethattrainingwithnoisecould
in theory help Vec2Text recover more accurately
fromϕ . NotethatlowreconstructionBLEU
noisy
scoreisnotnecessarilyindicativethatcoarserinfer-
ences, suchasclinicalareaortreatmentregimen,
cannotbemadefromembeddings.

30000
80
25000
|     | 60  |     |     |     |     |     |     | 20000 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
UELB
tnuoC
|     | 40  |     |     |     |     |     |     | 15000 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
10000
|     | 20  | Feedback    |     |     |     |     |     |      |     |     |     |     |
| --- | --- | ----------- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
|     |     | No feedback |     |     |     |     |     | 5000 |     |     |     |     |
0
|     | 0   |     | 20  |     | 40  |     |     | 0    |      |      |           |           |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | ---- | ---- | --------- | --------- |
|     |     |     |     |     |     |     |     | 0.70 | 0.75 | 0.80 | 0.85 0.90 | 0.95 1.00 |
Iteration (t)
Cosine distance from hypothesis to true embedding
|     |     |     |     |     |     |     | Figure4: | Distributionofcos(e,ϕ(x(0)))overtraining |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---------------------------------------- | --- | --- | --- | --- |
Figure3: Recoveryperformanceacrossmultiplerounds
|     |     |     |     |     |     |     | data. | The mean | training |     | output from | the GTR base |
| --- | --- | --- | --- | --- | --- | --- | ----- | -------- | -------- | --- | ----------- | ------------ |
ofself-correctioncomparingmodelswithaccesstoϕvs
|     |     |     |     |     |     |     | model | has a | cosine | similarity | of 0.924 | with the true |
| --- | --- | --- | --- | --- | --- | --- | ----- | ----- | ------ | ---------- | -------- | ------------- |
text-only(32tokenspersequence).
embedding.
7 Analysis
fewgeneratedsampleswithhighcosinesimilarity
|     |     |     |     |     |     |     | butlowBLEUscore. |     |     | Thisimpliesthatbetterfol- |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | ------------------------- | --- | --- |
Howmuchdoesthemodelrelyonfeedbackfrom
ϕ? Figure 3 shows an ablation study of the im- lowingembeddinggeometrywillfurtherimproves
|                         |         |           |     |                       |      |            | systems.               | Theoretically |     |     | some embeddings      | might |
| ----------------------- | ------- | --------- | --- | --------------------- | ---- | ---------- | ---------------------- | ------------- | --- | --- | -------------------- | ----- |
| portanceoffeedback,i.e. |         |           |     | performingcorrections |      |            |                        |               |     |     |                      |       |
|                         |         |           |     |                       |      |            | beimpossibletorecover. |               |     |     | Priorwork(Songetal., |       |
| with and                | without | embedding |     | the                   | most | recent hy- |                        |               |     |     |                      |       |
pothesis. Themodeltrainedwithfeedback(i.e. ad- 2020;Morris,2020)hasshownthattwodifferent
|     |     |     |     |     |     |     | sequences |     | can ‘collide’ |     | in text embedding | space, |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------------- | --- | ----------------- | ------ |
ditionalconditioningonϕ(x(t))isabletomakea
havingsimilarembeddingsevenwithoutanyword
moreaccuratefirstcorrectionandgetsbetterBLEU
score with more rounds. The model trained with overlap. However, our experiments found no ev-
no feedback can still edit the text but does not idence that collisions are a problem; they either
donotexistorourmodellearnsduringtrainingto
| receive       | more | information |     | about   | the geometry | of  |                      |     |     |     |                       |     |
| ------------- | ---- | ----------- | --- | ------- | ------------ | --- | -------------------- | --- | --- | --- | --------------------- | --- |
|               |      |             |     |         |              |     | avoidoutputtingthem. |     |     |     | Improvedsystemsshould |     |
| the embedding |      | space,      | and | quickly | plateaus.    | The |                      |     |     |     |                       |     |
moststartlingcomparisonisintermsofthenumber beabletorecoverlongertext.
| of exact    | matches: |       | after 50 | rounds   | of greedy | self-      |                                   |     |     |     |     |     |
| ----------- | -------- | ----- | -------- | -------- | --------- | ---------- | --------------------------------- | --- | --- | --- | --- | --- |
|             |          |       |          |          |           |            | Doeshavingastrongbasemodelmatter? |     |     |     |     | We  |
| correction, | our      | model | with     | feedback |           | gets 52.0% |                                   |     |     |     |     |     |
ablatetheimpactofinitializationbyevaluatingour
| of examples |     | correct | (after | only | 1.5% | initially); |          |           |     |       |              |             |
| ----------- | --- | ------- | ------ | ---- | ---- | ----------- | -------- | --------- | --- | ----- | ------------ | ----------- |
|             |     |         |        |      |      |             | 32-token | Wikipedia |     | model | at different | initializa- |
themodeltrainedwithoutfeedbackonlyperfectly
|     |     |     |     |     |     |     | tionsofx(0),asshowninSection7. |     |     |     |     | Afterrunning |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------ | --- | --- | --- | --- | ------------ |
matches4.2%ofexamplesafter50rounds.
for20stepsofcorrection,ourmodelisabletore-
During training, the model only learns to cor- coverfromanunhelpfulinitialization,evenwhen
rectasinglehypothesistotheground-truthsample.
|           |      |     |            |     |       |            | the | initialization |     | is a random | sequence | of tokens. |
| --------- | ---- | --- | ---------- | --- | ----- | ---------- | --- | -------------- | --- | ----------- | -------- | ---------- |
| Given new | text | at  | test time, | our | model | is able to |     |                |     |             |          |            |
Thissuggeststhatthemodelisabletoignorebad
correctthesametextmultipletimes,“pushing”the
hypothesesandfocusonthetrueembeddingwhen
| textfrom0.9embeddingsimilarityto1.0. |     |     |     |     |     | Weplot |     |     |     |     |     |     |
| ------------------------------------ | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
thehypothesisisnothelpful.
theclosenessofthefirsthypothesistotheground-
| truth in        | the training                    |            | data | for the | length-32   | model      | 8                        | Relatedwork |            |     |                  |                |
| --------------- | ------------------------------- | ---------- | ---- | ------- | ----------- | ---------- | ------------------------ | ----------- | ---------- | --- | ---------------- | -------------- |
| inFigure4.      | Weseethatduringtrainingthemodel |            |      |         |             |            |                          |             |            |     |                  |                |
|                 |                                 |            |      |         |             |            | Invertingdeepembeddings. |             |            |     | Thetaskofinvert- |                |
| learns to       | correct                         | hypotheses |      | across  | a           | wide range |                          |             |            |     |                  |                |
|                 |                                 |            |      |         |             |            | ing                      | textual     | embeddings |     | is closely       | related to re- |
| of closenesses, |                                 | implying   |      | that    | corrections | should     |                          |             |            |     |                  |                |
searchoninvertingdeepvisualrepresentationsin
| not go | ‘out-of-distribution’ |     |     | as  | they approach | the |          |        |     |            |              |       |
| ------ | --------------------- | --- | --- | --- | ------------- | --- | -------- | ------ | --- | ---------- | ------------ | ----- |
|        |                       |     |     |     |               |     | computer | vision |     | (Mahendran | and Vedaldi, | 2014; |
ground-truth.
DosovitskiyandBrox,2016;Teterwaketal.,2021;
Howinformativeareembeddingsfortextualre- Bordesetal.,2021),whichshowthatahighamount
covery? WegraphBLEUscorevs. cosinesimi- ofvisualdetailremainsinthelogitvectorofanim-
larityfromaselectionofofreconstructedtextin- ageclassifier,andattempttoreconstructinputim-
putsinFigure5. Weobserveastrongcorrelation agesfromthisvector. Thereisalsoalineofwork
between the two metrics. Notably, there are very reverse-engineeringthecontentofcertaintextem-

Input NaboGass(25August,1954inEbingen,Germany)isaGermanpainterandglassartist.
Round1(0.85): NaboGass(11August1974inErlangen,Germany)isanartist. ✗
Round2(0.99): NaboGass(b.18August1954inEgeland,Germany)isaGermanpainterandglassartist. ✗
Round3(0.99): NaboGass(25August1954inEbingen,Germany)isaGermanpainterandglassartist. ✗
Round4(1.00): NaboGass(25August,1954inEbingen,Germany)isaGermanpainterandglassartist. ✓
Table4: Exampleofourcorrectivemodelworkinginmultiplerounds. Leftcolumnshowsthecorrectionnumber,
fromRound1(initialhypothesis)toRound4(correctguess). Thenumberinparenthesisisthecosinesimilarity
betweentheguess’sembeddingandtheembeddingoftheground-truthsequence(firstrow).
Initialization tokenf1 cos exact etal.,2020)showsthatfacescanbereconstructed
Randomtokens 0.95 0.99 50.0 from their deep embeddings. Similar questions
| "the"*32 |     |     |     | 0.95 0.99 | 49.8 |           |       |       |            |        |        |
| -------- | --- | --- | --- | --------- | ---- | --------- | ----- | ----- | ---------- | ------ | ------ |
|          |     |     |     |           |      | have been | asked | about | text data: | Lehman | et al. |
"there’snoreverseonamotorcycle,
|     |     |     |     |     |     | (2021) attempt |     | to recover | sensitive | information |     |
| --- | --- | --- | --- | --- | --- | -------------- | --- | ---------- | --------- | ----------- | --- |
asmyfriendfoundoutquite
suchasnamesfromrepresentationsobtainedfrom
| dramaticallytheotherday" |     |     |     | 0.96 0.99 | 52.0 |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | --------- | ---- | --- | --- | --- | --- | --- | --- |
Basemodelp(x(0)|e) a model pre-trained on clinical notes, but fail to
|     |     |     |     | 0.96 0.99 | 51.6 |         |       |           |        |        |           |
| --- | --- | --- | --- | --------- | ---- | ------- | ----- | --------- | ------ | ------ | --------- |
|     |     |     |     |           |      | recover | exact | text. Kim | et al. | (2022) | propose a |
Table5: Ablation: ReconstructionscoreonWikipedia privacy-preserving similarity mechanism for text
data(32tokens)givenvariousinitializations. Ourself- embeddingsandconsiderashallowbag-of-words
correctionmodelisabletofaithfullyrecovertheoriginal
|     |     |     |     |     |     | inversion | model. | Abdalla | et al. | (2020) | analyze |
| --- | --- | --- | --- | --- | --- | --------- | ------ | ------- | ------ | ------ | ------- |
textwithgreaterthan80BLEUscore,evenwithapoor
theprivacyleaksintrainingwordembeddingson
| initialization. |     | Modelsrunfor20stepsofcorrection. |     |     |     |     |     |     |     |     |     |
| --------------- | --- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
medicaldataandareabletorecoverfullnamesin
|     |     |     |     |     |     | the training | data | from learned |     | word embeddings. |     |
| --- | --- | --- | --- | --- | --- | ------------ | ---- | ------------ | --- | ---------------- | --- |
Dziedzicetal.(2023)notethatstealingsentenceen-
100
codersbydistillingthroughAPIqueriesworkswell
|     | 80   |     |     |     |     | andisdifficultforAPIproviderstoprevent.  |     |     |     |     | Song |
| --- | ---- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | ---- |
|     | UELB |     |     |     |     | andRaghunathan(2020)consideredtheproblem |     |     |     |     |      |
60
ofrecoveringtextsequencesfromembeddings,but
|     | 40  |     |     |     |     | onlyattemptedtorecoverbagsofwordsfromthe |     |     |     |     |         |
| --- | --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | ------- |
|     |     |     |     |     |     | embeddingsofashallowencodermodel.        |     |     |     |     | Lietal. |
20
|     |     |     |     |     |     | (2023) investigate |     | the privacy |     | leakage | of embed- |
| --- | --- | --- | --- | --- | --- | ------------------ | --- | ----------- | --- | ------- | --------- |
dingsbytrainingadecoderwithatextembedding
|     | 0.85 | 0.90 |     | 0.95 | 1.00 |     |     |     |     |     |     |
| --- | ---- | ---- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- |
Cosine similarity as the first embedding fed to the decoder. Com-
paredtotheseworks,weconsiderthesignificantly
Figure 5: Cosine similarity vs BLEU score on 1000 moreinvolvedproblemofdevelopingamethodto
reconstructedembeddingsfromNaturalQuestionstext. recoverthefullorderedtextsequencefrommore
realisticstate-of-the-arttextretrievalmodels.
| beddings: | Rametal.(2023)analyzethecontents |     |     |     |     |                  |     |                          |     |     |     |
| --------- | -------------------------------- | --- | --- | --- | --- | ---------------- | --- | ------------------------ | --- | --- | --- |
|           |                                  |     |     |     |     | Gradientleakage. |     | Thereareparallelsbetween |     |     |     |
oftextembeddingsbyprojectingembeddingsinto
the model’s vocabulary space to produce a distri- the use of vector databases to store embeddings
bution of relevant tokens. Adolphs et al. (2022) andthepracticeoffederatedlearning,whereusers
sharegradientswithoneanotherinordertojointly
trainasingle-stepquerydecodertopredictthetext
|            |      |                  |     |         |         | train a model. |     | Our work | on  | analyzing | the pri- |
| ---------- | ---- | ---------------- | --- | ------- | ------- | -------------- | --- | -------- | --- | --------- | -------- |
| of queries | from | their embeddings |     | and use | the de- |                |     |          |     |           |          |
codertoproducemoredatatotrainanewretrieval vacy leakage of text embeddings is analogous to
researchongradientleakage,whichhasshownthat
| model. | We  | focus directly | on  | text reconstruction |     |     |     |     |     |     |     |
| ------ | --- | -------------- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- |
certaininputdatacanbereverse-engineeredfrom
| and | its implications | for | privacy, | and propose | an  |     |     |     |     |     |     |
| --- | ---------------- | --- | -------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
iterative method that works for paragraph-length themodel’sgradientsduringtraining(Melisetal.,
documents,notjustsentence-lengthqueries. 2018;Zhuetal.,2019;Zhaoetal.,2020;Geiping
|     |     |     |     |     |     | etal.,2020). | Zhuetal.(2019)evenshowsthatthey |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------ | ------------------------------- | --- | --- | --- | --- |
Privacy leakage from embeddings. Research canrecovertextinputsofamaskedlanguagemodel
hasraisedthequestionofinformationleakagefrom bybackpropagatingtotheinputlayertomatchthe
dense embeddings. In vision, Vec2Face (Duong gradient. However, suchtechniquesdonotapply

to textual inversion: the gradient of the model is moresophisticatedsearchalgorithmsontopofour
| relatively | high-resolution; |               |     | we consider |      | the more   | correctivemodule.      |     |     |                    |     |     |     |
| ---------- | ---------------- | ------------- | --- | ----------- | ---- | ---------- | ---------------------- | --- | --- | ------------------ | --- | --- | --- |
| difficult  | problem          | of recovering |     | the         | full | input text |                        |     |     |                    |     |     |     |
|            |                  |               |     |             |      |            | Scalabilitytolongtext. |     |     | Ourmethodisshownto |     |     |     |
givenonlyasingledenseembeddingvector.
recovermostsequencesexactlyupto32tokensand
someinformationupto128tokens,butwehavenot
| Textautoencoders. |     |     | Pastresearchhasexplored |     |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
naturallanguageprocessinglearningmodelsthat investigatedthelimitsofinversionbeyondembed-
|               |     |           |           |        |     |             | dings of | this length. | Popular |         | embedding | models |     |
| ------------- | --- | --------- | --------- | ------ | --- | ----------- | -------- | ------------ | ------- | ------- | --------- | ------ | --- |
| map vectors   | to  | sentences | (Bowman   |        | et  | al., 2016). |          |              |         |         |           |        |     |
|               |     |           |           |        |     |             | support  | embedding    | text    | content | on the    | order  | of  |
| These include |     | some      | retrieval | models |     | that are    |          |              |         |         |           |        |     |
trained with a shallow decoder to reconstruct the thousandsoftokens, andembeddinglongertexts
text or bag-of-words from the encoder-outputted iscommonpractice(Thakuretal.,2021). Future
workmightexplorethepotentialanddifficultiesof
| embedding | (Xiao | et  | al., 2022; | Shen | et  | al., 2023; |     |     |     |     |     |     |     |
| --------- | ----- | --- | ---------- | ---- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
Wangetal.,2023). Unlikethese,weinvertembed- invertingembeddingsoftheselongertexts.
dingsfromafrozen,pre-trainedencoder.
|     |     |     |     |     |     |     | Accesstoembeddingmodel. |         |           |     | Ourthreatmodel |        |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------------- | ------- | --------- | --- | -------------- | ------ | --- |
|     |     |     |     |     |     |     | assumes                 | that an | adversary | has | black-box      | access |     |
9 Conclusion
|             |           |           |              |     |          |          | to the model            | used    | to generate   |                     | the embeddings |          | in  |
| ----------- | --------- | --------- | ------------ | --- | -------- | -------- | ----------------------- | ------- | ------------- | ------------------- | -------------- | -------- | --- |
|             |           |           |              |     |          |          | thecompromiseddatabase. |         |               | Intherealworld,this |                |          |     |
| We propose  | Vec2Text, |           | a multi-step |     | method   | that     |                         |         |               |                     |                |          |     |
|             |           |           |              |     |          |          | is realistic            | because | practitioners |                     | so often       | rely     | on  |
| iteratively | corrects  | and       | re-embeds    |     | text     | based on |                         |         |               |                     |                |          |     |
|             |           |           |              |     |          |          | the same                | few     | large models. |                     | However,       | Vec2Text |     |
| a fixed     | point     | in latent | space.       | Our | approach | can      |                         |         |               |                     |                |          |     |
recover92%of32-tokentextinputsfromtheirem- requiresmakingaquerytotheblack-boxembed-
|                                   |          |               |     |     |           |        | ding model | for     | each step | of  | refinement.  | Future |     |
| --------------------------------- | -------- | ------------- | --- | --- | --------- | ------ | ---------- | ------- | --------- | --- | ------------ | ------ | --- |
| beddings                          | exactly, | demonstrating |     |     | that text | embed- |            |         |           |     |              |        |     |
|                                   |          |               |     |     |           |        | work might | explore | training  |     | an imitation | embed- |     |
| dingsrevealmuchoftheoriginaltext. |          |               |     |     | Themodel  |        |            |         |           |     |              |        |     |
alsodemonstratestheabilitytoextractcriticalclini- ding model which could be queried at inference
timetosavequeriestothetrueembedder.
calinformationfromclinicalnotes,highlightingits
implicationsfordataprivacyinsensitivedomains
likemedicine.
References
| Our findings |     | indicate | a   | sort of | equivalence | be- |         |          |          |          |        |     |        |
| ------------ | --- | -------- | --- | ------- | ----------- | --- | ------- | -------- | -------- | -------- | ------ | --- | ------ |
|              |     |          |     |         |             |     | Mohamed | Abdalla, | Moustafa | Abdalla, | Graeme |     | Hirst, |
tweenembeddingsandrawdata,inthatbothleak
|         |         |     |           |              |     |      | and Frank  | Rudzicz.   | 2020. | Exploring |             | the privacy- |     |
| ------- | ------- | --- | --------- | ------------ | --- | ---- | ---------- | ---------- | ----- | --------- | ----------- | ------------ | --- |
| similar | amounts | of  | sensitive | information. |     | This |            |            |       |           |             |              |     |
|         |         |     |           |              |     |      | preserving | properties |       | of word   | embeddings: |              | Al- |
equivalenceputsaheavyburdenonanonymization
|                                 |         |     |        |           |            |      | gorithmic     | validation |     | study. | J Med Internet |     | Res, |
| ------------------------------- | ------- | --- | ------ | --------- | ---------- | ---- | ------------- | ---------- | --- | ------ | -------------- | --- | ---- |
| requirementsfordenseembeddings: |         |     |        |           | embeddings |      | 22(7):e18055. |            |     |        |                |     |      |
| should be                       | treated | as  | highly | sensitive | private    | data |               |            |     |        |                |     |      |
LeonardAdolphs,MichelleChenHuebscher,Christian
andprotected,technicallyandperhapslegally,in Buck,SertanGirgin,OlivierBachem,Massimiliano
thesamewayasonewouldprotectrawtext.
|     |     |     |     |     |     |     | Ciaramita,andThomasHofmann.2022. |     |     |     |     | Decodinga |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | --------- | --- |
neuralretriever’slatentspaceforquerysuggestion.
10 Limitations
|     |     |     |     |     |     |     | Charu C. | Aggarwal | and | ChengXiang | Zhai. | 2012. | A   |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------- | --- | ---------- | ----- | ----- | --- |
SurveyofTextClusteringAlgorithms,pages77–128.
| Adaptiveattacksanddefenses. |     |     |     |     | Weconsiderthe |     |     |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
SpringerUS,Boston,MA.
settingwhereanadversaryappliesnoisetonewly
PayalBajaj,DanielCampos,NickCraswell,LiDeng,
generatedembeddings,butthereconstructionmod-
ulesweretrainedfromun-noisedembeddings. Fu- JianfengGao,XiaodongLiu,RanganMajumder,An-
|     |     |     |     |     |     |     | drew McNamara, |     | Bhaskar | Mitra, | Tri Nguyen, |     | Mir |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------- | ------ | ----------- | --- | --- |
tureworkmightconsiderreconstructionattacksor
Rosenberg,XiaSong,AlinaStoica,SaurabhTiwary,
defensesthatareadaptivetothetypeofattackor andTongWang.2018. Msmarco: Ahumangener-
| defensebeingused. |     |     |     |     |     |     | atedmachinereadingcomprehensiondataset. |     |     |     |     |     |     |
| ----------------- | --- | --- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- | --- |
FlorianBordes,RandallBalestriero,andPascalVincent.
| Searchthoroughness. |     |     | Oursearchislimited;in |     |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2021. Highfidelityvisualizationofwhatyourself-
thisworkwedonottestbeyondsearchingfor50
|                                          |     |          |      |               |     |        | supervisedrepresentationknowsabout. |     |     |     |     | Trans.Mach. |     |
| ---------------------------------------- | --- | -------- | ---- | ------------- | --- | ------ | ----------------------------------- | --- | --- | --- | --- | ----------- | --- |
| roundsorwithasequencebeamwidthhigherthan |     |          |      |               |     |        | Learn.Res.,2022.                    |     |     |     |     |             |     |
| 8. However,                              |     | Vec2Text | gets | monotonically |     | better |                                     |     |     |     |     |             |     |
SebastianBorgeaud,ArthurMensch,JordanHoffmann,
| withmoresearching. |     |     | Futureworkcouldfindeven |     |     |     |     |     |     |     |     |     |     |
| ------------------ | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
TrevorCai,ElizaRutherford,KatieMillican,George
moreexactmatchesbysearchingformorerounds vandenDriessche, Jean-BaptisteLespiau, Bogdan
| with a | higher | beam | width, | or by | implementing |     |     |     |     |     |     |     |     |
| ------ | ------ | ---- | ------ | ----- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Damoc,AidanClark,DiegodeLasCasas,Aurelia

Guy, Jacob Menick, Roman Ring, Tom Hennigan, AbuDhabi,UnitedArabEmirates(Hybrid).Associa-
SaffronHuang,LorenMaggiore,ChrisJones,Albin tionforComputationalLinguistics.
| Cassirer, | AndyBrock,MichelaPaganini, |     |     |     | Geoffrey |     |     |     |     |     |     |     |
| --------- | -------------------------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
Irving, Oriol Vinyals, Simon Osindero, Karen Si- Ryan Kiros, Yukun Zhu, Ruslan Salakhutdinov,
|     |     |     |     |     |     |     | Richard S. | Zemel, | Antonio | Torralba, |     | Raquel Urta- |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | ------- | --------- | --- | ------------ |
monyan,JackW.Rae,ErichElsen,andLaurentSifre.
|     |     |     |     |     |     |     | sun,andSanjaFidler.2015. |     |     | Skip-thoughtvectors. |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | -------------------- | --- | --- |
2022. Improvinglanguagemodelsbyretrievingfrom
trillionsoftokens.
|     |     |     |     |     |     |     | TomKwiatkowski, |     | JennimariaPalomaki, |     |     | OliviaRed- |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------------------- | --- | --- | ---------- |
field,MichaelCollins,AnkurParikh,ChrisAlberti,
| Samuel R. | Bowman, | Luke | Vilnis, | Oriol | Vinyals, | An- |     |     |     |     |     |     |
| --------- | ------- | ---- | ------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
drewM.Dai, RafalJozefowicz, andSamyBengio. DanielleEpstein,IlliaPolosukhin,JacobDevlin,Ken-
2016. Generatingsentencesfromacontinuousspace. tonLee,KristinaToutanova,LlionJones,Matthew
|     |     |     |     |     |     |     | Kelcey, Ming-Wei |     | Chang, | Andrew | M.  | Dai, Jakob |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ------ | ------ | --- | ---------- |
SumanthDathathri,AndreaMadotto,JaniceLan,Jane Uszkoreit, Quoc Le, and Slav Petrov. 2019. Natu-
|     |     |     |     |     |     |     | ralquestions: | Abenchmarkforquestionanswering |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | ------------------------------ | --- | --- | --- | --- |
Hung,EricFrank,PieroMolino,JasonYosinski,and
RosanneLiu.2020. Plugandplaylanguagemodels: research. TransactionsoftheAssociationforCompu-
Asimpleapproachtocontrolledtextgeneration. In tationalLinguistics,7:452–466.
| International | Conference |     | on  | Learning | Representa- |     |                 |                      |     |     |     |             |
| ------------- | ---------- | --- | --- | -------- | ----------- | --- | --------------- | -------------------- | --- | --- | --- | ----------- |
| tions.        |            |     |     |          |             |     | LangChain.2023. | Hwchase17/langchain: |     |     |     | buildingap- |
plicationswithllmsthroughcomposability.
| AlexeyDosovitskiyandThomasBrox.2016. |     |     |     |     | Inverting |     |     |     |     |     |     |     |
| ------------------------------------ | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
visualrepresentationswithconvolutionalnetworks. Quoc V. Le and Tomas Mikolov. 2014. Distributed
representationsofsentencesanddocuments.
ChiNhanDuong,Thanh-DatTruong,KhaGiaQuach,
|           |                                   |     |      |          |      |       | Jason Lee, Elman    |     | Mansimov,          | and | Kyunghyun | Cho.       |
| --------- | --------------------------------- | --- | ---- | -------- | ---- | ----- | ------------------- | --- | ------------------ | --- | --------- | ---------- |
| Hung      | Bui, Kaushik                      |     | Roy, | and Khoa | Luu. | 2020. |                     |     |                    |     |           |            |
|           |                                   |     |      |          |      |       | 2018. Deterministic |     | non-autoregressive |     |           | neural se- |
| Vec2face: | Unveilhumanfacesfromtheirblackbox |     |      |          |      |       |                     |     |                    |     |           |            |
quencemodelingbyiterativerefinement.
featuresinfacerecognition.
EricLehman,SarthakJain,KarlPichotta,YoavGold-
| AdamDziedzic,                       |     | FranziskaBoenisch, |     |     | MingjianJiang, |     |           |       |             |       |      |           |
| ----------------------------------- | --- | ------------------ | --- | --- | -------------- | --- | --------- | ----- | ----------- | ----- | ---- | --------- |
|                                     |     |                    |     |     |                |     | berg, and | Byron | C. Wallace. | 2021. | Does | bert pre- |
| HaonanDuan,andNicolasPapernot.2023. |     |                    |     |     | Sentence       |     |           |       |             |       |      |           |
embedding encoders are easy to steal but hard to trainedonclinicalnotesrevealsensitivedata?
| defend. | InICLR2023WorkshoponPitfallsoflimited |     |     |     |     |     |                                         |     |     |     |     |      |
| ------- | ------------------------------------- | --- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | ---- |
|         |                                       |     |     |     |     |     | HaoranLi,MingshiXu,andYangqiuSong.2023. |     |     |     |     | Sen- |
dataandcomputationforTrustworthyML.
|     |     |     |     |     |     |     | tence embedding    |     | leaks more | information |           | than you  |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | ---------- | ----------- | --------- | --------- |
|     |     |     |     |     |     |     | expect: Generative |     | embedding  |             | inversion | attack to |
JonasGeiping,HartmutBauermeister,HannahDröge,
recoverthewholesentence.
| and Michael | Moeller. |     | 2020. | Inverting | gradients | –   |     |     |     |     |     |     |
| ----------- | -------- | --- | ----- | --------- | --------- | --- | --- | --- | --- | --- | --- | --- |
howeasyisittobreakprivacyinfederatedlearning?
XiangLisaLi,JohnThickstun,IshaanGulrajani,Percy
|                       |     |     |      |              |      |     | Liang,andTatsunoriB.Hashimoto.2022. |     |     |     |     | Diffusion- |
| --------------------- | --- | --- | ---- | ------------ | ---- | --- | ----------------------------------- | --- | --- | --- | --- | ---------- |
| Marjan Ghazvininejad, |     |     | Omer | Levy, Yinhan | Liu, | and |                                     |     |     |     |     |            |
lmimprovescontrollabletextgeneration.
| LukeZettlemoyer.2019. |     |     | Mask-predict: |     | Parallelde- |     |     |     |     |     |     |     |
| --------------------- | --- | --- | ------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
codingofconditionalmaskedlanguagemodels. AravindhMahendranandAndreaVedaldi.2014. Un-
derstandingdeepimagerepresentationsbyinverting
| Zhiting Hu, | Zichao | Yang, | Xiaodan |     | Liang, | Ruslan |     |     |     |     |     |     |
| ----------- | ------ | ----- | ------- | --- | ------ | ------ | --- | --- | --- | --- | --- | --- |
them. 2015IEEEConferenceonComputerVision
| Salakhutdinov,andEricP.Xing.2018. |     |     |     |     | Towardcon- |     |     |     |     |     |     |     |
| --------------------------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
andPatternRecognition(CVPR),pages5188–5196.
trolledgenerationoftext.
LucaMelis,CongzhengSong,EmilianoDeCristofaro,
VineetJohn,LiliMou,HareeshBahuleyan,andOlga
|             |       |     |              |     |                |     | andVitalyShmatikov.2018. |     |     | Exploitingunintended |     |     |
| ----------- | ----- | --- | ------------ | --- | -------------- | --- | ------------------------ | --- | --- | -------------------- | --- | --- |
| Vechtomova. | 2018. |     | Disentangled |     | representation |     |                          |     |     |                      |     |     |
featureleakageincollaborativelearning.
learningfornon-paralleltextstyletransfer.
TomasMikolov,KaiChen,GregCorrado,andJeffrey
| Alistair E.W. | Johnson, |     | Tom J. | Pollard, | Lu Shen, | Li- |            |                                      |     |     |     |     |
| ------------- | -------- | --- | ------ | -------- | -------- | --- | ---------- | ------------------------------------ | --- | --- | --- | --- |
|               |          |     |        |          |          |     | Dean.2013. | Efficientestimationofwordrepresenta- |     |     |     |     |
weiH.Lehman,MenglingFeng,MohammadGhas-
tionsinvectorspace.
| semi, | Benjamin  | Moody, | Peter | Szolovits,  |            | Leo An- |     |     |     |     |     |     |
| ----- | --------- | ------ | ----- | ----------- | ---------- | ------- | --- | --- | --- | --- | --- | --- |
| thony | Celi, and | Roger  | G.    | Mark. 2016. | Mimic-iii, |         |     |     |     |     |     |     |
RonMokady,AmirHertz,andAmitH.Bermano.2021.
| afreelyaccessiblecriticalcaredatabase. |     |     |     |     | Scientific |     |                                        |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | ---------- | --- | -------------------------------------- | --- | --- | --- | --- | --- |
|                                        |     |     |     |     |            |     | Clipcap: Clipprefixforimagecaptioning. |     |     |     |     |     |
Data,3(1):160035.
|     |     |     |     |     |     |     | John X. Morris. | 2020. | Second-order |     | nlp | adversarial |
| --- | --- | --- | --- | --- | --- | --- | --------------- | ----- | ------------ | --- | --- | ----------- |
VladimirKarpukhin,BarlasOg˘uz,SewonMin,Patrick
examples.
Lewis,LedellWu,SergeyEdunov,DanqiChen,and
WentauYih.2020. Densepassageretrievalforopen- NiklasMuennighoff,NouamaneTazi,LoïcMagne,and
domainquestionanswering. NilsReimers.2023. Mteb: Massivetextembedding
benchmark.
| Donggyu | Kim, Garam |     | Lee, and | Sungwoo | Oh. | 2022. |     |     |     |     |     |     |
| ------- | ---------- | --- | -------- | ------- | --- | ----- | --- | --- | --- | --- | --- | --- |
Towardprivacy-preservingtextembeddingsimilarity Arvind Neelakantan, Tao Xu, Raul Puri, Alec Rad-
withhomomorphicencryption. InProceedingsofthe ford, Jesse Michael Han, Jerry Tworek, Qiming
FourthWorkshoponFinancialTechnologyandNat- Yuan,NikolasTezak,JongWookKim,ChrisHallacy,
uralLanguageProcessing(FinNLP),pages25–36, Johannes Heidecke, Pranav Shyam, Boris Power,

Tyna Eloundou Nekoul, Girish Sastry, Gretchen Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
Krueger,DavidSchnurr,FelipePetroskiSuch,Kenny Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz
Hsu, Madeleine Thompson, Tabarak Khan, Toki Kaiser,andIlliaPolosukhin.2017. Attentionisall
| Sherbakov,JoanneJang,PeterWelinder,andLilian |       |          |      |            |     |         | youneed. |     |     |     |     |     |
| -------------------------------------------- | ----- | -------- | ---- | ---------- | --- | ------- | -------- | --- | --- | --- | --- | --- |
| Weng.                                        | 2022. | Text and | code | embeddings |     | by con- |          |     |     |     |     |     |
trastivepre-training. Vdaas.2023. Vdaas/vald: Vald.ahighlyscalabledis-
tributedvectorsearchengine.
| Jianmo | Ni, Chen | Qu, Jing | Lu, | Zhuyun | Dai, | Gus- |     |     |     |     |     |     |
| ------ | -------- | -------- | --- | ------ | ---- | ---- | --- | --- | --- | --- | --- | --- |
LiangWang,NanYang,XiaolongHuang,BinxingJiao,
| tavo Hernández |     | Ábrego, | Ji Ma, | Vincent | Y.  | Zhao, |             |             |     |                 |     |     |
| -------------- | --- | ------- | ------ | ------- | --- | ----- | ----------- | ----------- | --- | --------------- | --- | --- |
|                |     |         |        |         |     |       | LinjunYang, | DaxinJiang, |     | RanganMajumder, |     | and |
YiLuan,KeithB.Hall,Ming-WeiChang,andYinfei
Yang.2021. Largedualencodersaregeneralizable FuruWei.2023. Simlm: Pre-trainingwithrepresen-
| retrievers. |     |     |     |     |     |     | tationbottleneckfordensepassageretrieval. |                          |     |     |     |     |
| ----------- | --- | --- | --- | --- | --- | --- | ----------------------------------------- | ------------------------ | --- | --- | --- | --- |
|             |     |     |     |     |     |     | Weaviate.2023.                            | Weaviate-vectordatabase. |     |     |     |     |
KishorePapineni,SalimRoukos,ToddWard,andWei-
| JingZhu.2002.              |     | Bleu: amethodforautomaticevalu- |     |                    |     |     |               |        |           |           |       |           |
| -------------------------- | --- | ------------------------------- | --- | ------------------ | --- | --- | ------------- | ------ | --------- | --------- | ----- | --------- |
|                            |     |                                 |     |                    |     |     | Sean Welleck, | Ximing | Lu, Peter | West,     | Faeze | Brah-     |
| ationofmachinetranslation. |     |                                 |     | InProceedingsofthe |     |     |               |        |           |           |       |           |
|                            |     |                                 |     |                    |     |     | man, Tianxiao | Shen,  | Daniel    | Khashabi, |       | and Yejin |
40thAnnualMeetingoftheAssociationforCompu-
|          |              |       |          |     |               |     | Choi. | 2022. Generating | sequences |     | by learning | to  |
| -------- | ------------ | ----- | -------- | --- | ------------- | --- | ----- | ---------------- | --------- | --- | ----------- | --- |
| tational | Linguistics, | pages | 311–318, |     | Philadelphia, |     |       |                  |           |     |             |     |
self-correct.
Pennsylvania,USA.AssociationforComputational
Linguistics.
ShitaoXiao,ZhengLiu,YingxiaShao,andZhaoCao.
|                |     |           |     |     |     |     | 2022. | Retromae: Pre-trainingretrieval-orientedlan- |     |     |     |     |
| -------------- | --- | --------- | --- | --- | --- | --- | ----- | -------------------------------------------- | --- | --- | --- | --- |
| Pinecone.2023. |     | Pinecone. |     |     |     |     |       |                                              |     |     |     |     |
guagemodelsviamaskedauto-encoder.
| Qdrant.2023. | Qdrant-vectordatabase. |     |     |     |     |     |                            |      |        |                  |     |         |
| ------------ | ---------------------- | --- | --- | --- | --- | --- | -------------------------- | ---- | ------ | ---------------- | --- | ------- |
|              |                        |     |     |     |     |     | KevinYangandDanKlein.2021. |      |        | FUDGE:Controlled |     |         |
|              |                        |     |     |     |     |     | text generation            | with | future | discriminators.  |     | In Pro- |
ColinRaffel,NoamShazeer,AdamRoberts,Katherine ceedingsofthe2021ConferenceoftheNorthAmer-
Lee,SharanNarang,MichaelMatena,YanqiZhou, icanChapteroftheAssociationforComputational
| WeiLi,andPeterJ.Liu.2020. |     |     |     | Exploringthelimits |     |     |              |                                   |     |     |     |     |
| ------------------------- | --- | --- | --- | ------------------ | --- | --- | ------------ | --------------------------------- | --- | --- | --- | --- |
|                           |     |     |     |                    |     |     | Linguistics: | HumanLanguageTechnologies.Associ- |     |     |     |     |
oftransferlearningwithaunifiedtext-to-texttrans-
ationforComputationalLinguistics.
former.
|     |     |     |     |     |     |     | Shunyu Yao, | Jeffrey Zhao, | Dian | Yu, | Nan | Du, Izhak |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------------- | ---- | --- | --- | --------- |
OriRam,LiatBezalel,AdiZicher,YonatanBelinkov, Shafran,KarthikNarasimhan,andYuanCao.2023.
JonathanBerant,andAmirGloberson.2023. What React: Synergizingreasoningandactinginlanguage
| areyoutokenabout? |     | denseretrievalasdistributions |     |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | ----------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
models.
overthevocabulary.
BoZhao,KondaReddyMopuri,andHakanBilen.2020.
Shaina Raza, Deepak John Reji, Femi Shajan, and idlg: Improveddeepleakagefromgradients.
| Syed | Raza Bashir. | 2022. | Large-scale |     | application |     |     |     |     |     |     |     |
| ---- | ------------ | ----- | ----------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
ofnamedentityrecognitiontobiomedicineandepi- LigengZhu,ZhijianLiu,andSongHan.2019. Deep
PLOSDigitalHealth,1(12):e0000152.
| demiology.                                 |     |     |     |     |     |     | leakagefromgradients. |     |     |     |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- |
| TaoShen,XiuboGeng,ChongyangTao,CanXu,Xiao- |     |     |     |     |     |     | A Appendix            |     |     |     |     |     |
longHuang,BinxingJiao,LinjunYang,andDaxin
| Jiang.2023. |     | Lexmae: Lexicon-bottleneckedpretrain- |     |     |     |     |                        |     |     |     |     |     |
| ----------- | --- | ------------------------------------- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- |
|             |     |                                       |     |     |     |     | A.1 Additionalanalysis |     |     |     |     |     |
ingforlarge-scaleretrieval.
Howdoeswordfrequencyaffectmodelcorrect-
CongzhengSongandAnanthRaghunathan.2020. Infor- ness? fig.6showsthenumberofcorrectpredic-
| mationleakageinembeddingmodels. |     |     |     |     | Proceedings |     |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
tions(orange)andincorrectpredictions(blue)for
ofthe2020ACMSIGSACConferenceonComputer
ground-truthwords,plottedacrosswordfrequency
andCommunicationsSecurity.
|     |     |     |     |     |     |     | inthetrainingdata. | Ourmodelgenerallypredicts |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | ------------------------- | --- | --- | --- | --- |
Congzheng Song, Alexander M. Rush, and Vitaly wordsbetterthataremorefrequentinthetraining
| Shmatikov.2020. |     | Adversarialsemanticcollisions. |     |     |     |     |     |     |     |     |     |     |
| --------------- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
data,althoughitisstillabletopredictcorrectlya
|                      |     |         |                         |       |           |     | number      | of words that | were    | not seen | during | train-   |
| -------------------- | --- | ------- | ----------------------- | ----- | --------- | --- | ----------- | ------------- | ------- | -------- | ------ | -------- |
| Piotr Teterwak,      |     | Chiyuan | Zhang,                  | Dilip | Krishnan, | and |             |               |         |          |        |          |
|                      |     |         |                         |       |           |     | ing3. Peaks | between       | 104 and | 105      | come   | from the |
| MichaelC.Mozer.2021. |     |         | Understandinginvariance |       |           |     |             |               |         |          |        |          |
viafeedforwardinversionofdiscriminativelytrained characters(,−,and),whichappearfrequentlyin
| classifiers. |     |     |     |     |     |     | thetrainingdata,butarestilloftenguessedincor- |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- |
rectlyinthereconstructions.
| Nandan                                  | Thakur, | Nils Reimers, |     | Andreas | Rücklé, | Ab-   |     |     |     |     |     |     |
| --------------------------------------- | ------- | ------------- | --- | ------- | ------- | ----- | --- | --- | --- | --- | --- | --- |
| hishekSrivastava,andIrynaGurevych.2021. |         |               |     |         |         | Beir: |     |     |     |     |     |     |
3Wehypothesizethisisbecausealltesttokenswerepresent
Aheterogenousbenchmarkforzero-shotevaluation
inthetrainingdata,andthemodelisabletoreconstructunseen
| ofinformationretrievalmodels. |     |     |     |     |     |     | wordsfromseentokens. |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- |

Correctness vs word frequency in training on ArXiv
False negative
|     | 8000 True positive |     |     |     |
| --- | ------------------ | --- | --- | --- |
lave ni desseug latoT
6000
4000
2000
0
|     | 100 101 102 | 103 | 104 105 | 106 107 |
| --- | ----------- | --- | ------- | ------- |
Frequency in training data
Figure6:CorrectnessonevaluationsamplesfromArXiv
data.
A.2 Fulldefenseresults
| Results    | on each dataset | from  | BEIR      | under vary-  |
| ---------- | --------------- | ----- | --------- | ------------ |
| ing levels | of Gaussian     | noise | are       | shown in Ap- |
| pendix     | A.2. The model  | is    | GTR-base. | Note that    |
theinputsarelimitedto32tokens,farshorterthan
theaveragelengthforsomecorpuses,whichiswhy
| baseline               | (λ = 0) NDCG@10 |                          | numbers | are lower |
| ---------------------- | --------------- | ------------------------ | ------- | --------- |
| thantypicallyreported. |                 | Weincludedthefullresults |         |           |
(visualizedinFigure2)asAppendixA.2.

λ arguana bioasq climate-fever dbpedia-entity fiqa msmarco nfcorpus nq quora robust04 scidocs scifact signal1m trec-covid trec-news webis-touche2020
0 0.328 0.115 0.136 0.306 0.208 0.647 0.239 0.306 0.879 0.205 0.095 0.247 0.261 0.376 0.245 0.233
0.001 0.329 0.115 0.135 0.307 0.208 0.647 0.239 0.306 0.879 0.204 0.096 0.246 0.261 0.381 0.246 0.233
0.01 0.324 0.113 0.132 0.301 0.205 0.633 0.234 0.298 0.875 0.192 0.092 0.235 0.259 0.378 0.234 0.225
0.1 0.005 0.000 0.000 0.000 0.000 0.000 0.017 0.000 0.003 0.000 0.002 0.006 0.001 0.005 0.001 0.000
1.0 0.001 0.000 0.000 0.000 0.000 0.000 0.008 0.000 0.000 0.000 0.000 0.001 0.000 0.000 0.000 0.000
Table6: BEIRperformance(NDCG@10)forGTR-baseatvaryinglevelsofnoise(32tokens).
λ NDCG@10 BLEU
0.000 0.302 80.372
0.001 0.302 72.347
0.010 0.296 10.334
0.100 0.002 0.148
1.000 0.001 0.080
Table7: Retrievalperformanceandreconstructionperformanceacrossvaryingnoiselevelsλ.