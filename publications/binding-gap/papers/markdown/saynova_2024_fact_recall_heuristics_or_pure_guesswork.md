|     |     | Fact | Recall, | Heuristics | or Pure | Guesswork? |     |     |     |     |
| --- | --- | ---- | ------- | ---------- | ------- | ---------- | --- | --- | --- | --- |
Precise Interpretations of Language Models for Fact Completion
|     |     |                 | DenitsaSaynova1,2∗ |                     | LovisaHagström1,2∗ |                |     |     |     |     |
| --- | --- | --------------- | ------------------ | ------------------- | ------------------ | -------------- | --- | --- | --- | --- |
|     |     | MoaJohansson1,2 |                    | RichardJohansson1,2 |                    | MarcoKuhlmann3 |     |     |     |     |
1 ChalmersUniversityofTechnology 2 UniversityofGothenburg 3 LinköpingUniversity
|     |     |     | {saynova, | lovhag}@chalmers.se |     |     |     |     |     |     |
| --- | --- | --- | --------- | ------------------- | --- | --- | --- | --- | --- | --- |
Abstract
| Language | models | (LMs) | can make | a correct |     |     |     |     |     |     |
| -------- | ------ | ----- | -------- | --------- | --- | --- | --- | --- | --- | --- |
predictionbasedonmanypossiblesignalsin
5202 luJ 1  ]LC.sc[  4v50441.0142:viXra
| a prompt,            | not    | all corresponding        |           | to recall of  |     |     |     |     |     |     |
| -------------------- | ------ | ------------------------ | --------- | ------------- | --- | --- | --- | --- | --- | --- |
| factualassociations. |        | However,currentinterpre- |           |               |     |     |     |     |     |     |
| tations              | of LMs | fail to                  | take this | into account. |     |     |     |     |     |     |
Forexample,giventhequery“AstridLindgren
wasbornin”withthecorrespondingcomple-
tion“Sweden”,nodifferenceismadebetween
whetherthepredictionwasbasedonknowing
| where | the author | was | born or | assuming that |     |     |     |     |     |     |
| ----- | ---------- | --- | ------- | ------------- | --- | --- | --- | --- | --- | --- |
apersonwithaSwedish-soundingnamewas
| born | in Sweden. | In this | paper, | we present a |     |     |     |     |     |     |
| ---- | ---------- | ------- | ------ | ------------ | --- | --- | --- | --- | --- | --- |
model-specificrecipe–PRISM–forconstruct- Figure 1: Prediction scenarios and corresponding
ing datasets with examples of four different promptcompletionexamples. Eachscenarioyieldsdis-
predictionscenarios: genericlanguagemodel- tinctinterpretabilityresults.
ing,guesswork,heuristicsrecallandexactfact
| recall.                | We apply | two popular |                   | interpretability |               |        |     |             |         |         |
| ---------------------- | -------- | ----------- | ----------------- | ---------------- | ------------- | ------ | --- | ----------- | ------- | ------- |
| methodstothescenarios: |          |             | causaltracing(CT) |                  |               |        |     |             |         |         |
|                        |          |             |                   |                  | et al., 2021; | Geiger | et  | al., 2021), | and has | already |
| and information        |          | flow        | analysis.         | We find that     |               |        |     |             |         |         |
yieldedinsightsintowhereLMsstoreandprocess
| bothyielddistinctresultsforeachscenario. |     |     |     | Re- |     |     |     |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sultsforexactfactrecallandgenericlanguage factualinformation(Mengetal.,2022;Gevaetal.,
modeling scenarios confirm previous conclu- 2023;Havivetal.,2023).
sionsabouttheimportanceofmid-rangeMLP
Whilethisbodyofworkhasbrokennewground
sublayersforfactrecall,whileresultsforguess-
work and heuristicsindicate a criticalrole of and provided us with interpretations of fact com-
pletioninLMs,itislimitedtostudiesofonlyone
| latelasttokenpositionMLPsublayers. |     |     |     | Insum- |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
mary, we contribute resources for a more ex- typeofscenario. Morespecifically,inMengetal.
tensiveandgranularstudyoffactcompletion (2022)andGevaetal.(2023),thestudiesarelim-
inLMs,togetherwithanalysesthatprovidea
|     |     |     |     |     | itedto | correctpredictions, |     | anditis | assumedthat |     |
| --- | --- | --- | --- | --- | ------ | ------------------- | --- | ------- | ----------- | --- |
morenuancedunderstandingofhowLMspro-
|     |     |     |     |     | themodelrecallsfactsforthese. |     |     | Wehypothesize |     |     |
| --- | --- | --- | --- | --- | ----------------------------- | --- | --- | ------------- | --- | --- |
cessfact-relatedqueries.
|     |     |     |     |     | that this | scenario | in reality | is a blend | of  | multiple |
| --- | --- | --- | --- | --- | --------- | -------- | ---------- | ---------- | --- | -------- |
1 Introduction more fine-grained scenarios, as it is well known
|     |     |     |     |     | that LMs | can | make correct | predictions |     | based on |
| --- | --- | --- | --- | --- | -------- | --- | ------------ | ----------- | --- | -------- |
Languagemodels(LMs)trainedonlargecorpora
manydifferentsignalsintheprompt,notallcorre-
havebeenfoundtostoresignificantamountsoffac-
|                                     |     |     |     |            | sponding | to exact | fact        | recall. For  | example, | LMs    |
| ----------------------------------- | --- | --- | --- | ---------- | -------- | -------- | ----------- | ------------ | -------- | ------ |
| tualinformation(Petronietal.,2019). |     |     |     | Whilethere |          |          |             |              |          |        |
|                                     |     |     |     |            | may pick | up       | on spurious | correlations | to       | “solve |
aremanyresearchresultsdocumentingthefactpro-
thedataset”ratherthanthetaskexemplifiedbyit
ficiencyofLMs(Kandpaletal.,2023;Mallenetal.,
(Zellersetal.,2019;NivenandKao,2019;McCoy
2023),ourunderstandingofhowthesemodelsper-
etal.,2019),andfactcompletionsituationsareno
| form fact   | completion       | is  | still under | development.    |                 |     |                              |             |     |           |
| ----------- | ---------------- | --- | ----------- | --------------- | --------------- | --- | ---------------------------- | ----------- | --- | --------- |
|             |                  |     |             |                 | exceptiontothis |     | (Poerneretal.,2020;Caoetal., |             |     |           |
| Mechanistic | interpretability |     | is a        | growing area of |                 |     |                              |             |     |           |
|             |                  |     |             |                 | 2021; Ladhak    |     | et al., 2023).               | In bringing |     | this dis- |
researchaimingtoexplainmodelbehavior(Elhage
tinctionforward,wealsogroundourworkinmore
formalstudiesofknowledge,wheremostscholars
*Equalcontribution.

agreethatguessworkshouldbeaccountedforand that fact is stored in the model parameters, also
excluded in order to consider a model as having referredtoastheparametricmemory. Mallenetal.
“bonafideknowledge”(Fierroetal.,2024). (2023);Kandpaletal.(2023)observethatqueries
Inthiswork,wedisentangleanddetailfourdif- askingforfacttuplesrarelyfoundintheLMtrain-
ferentpredictionscenariosforwhichLMscanbe ingdataarelesslikelytobeknownbythemodel.
expectedtoshowdistinctbehaviors(seeFigure1). Mallenetal.(2023)takethisonestepfurtherand
Thescenariosare: 1)Genericlanguagemodeling, use fact popularity (measured as Wikipedia page
whenthemodeldoesnotrespondwithfacts,such views) as a proxy for training data frequency to
as when generating a story. 2) Guesswork, when estimatetheprobabilityofamodelknowingafact.
the model responds with a fact but is uncertain. Conversely,Liuetal.(2023);Basmovetal.(2024)
3)Heuristicsrecall,whenthemodelusesshallow use synthesized facts to simulate a training data
frequencyof0tostudymodelbehaviorintheface
heuristics,e.g.thatpeoplewithKorean-sounding
| names are | more | likely to | live | in Korea. | 4) Exact | oftheunknown. |     |     |     |     |     |     |
| --------- | ---- | --------- | ---- | --------- | -------- | ------------- | --- | --- | --- | --- | --- | --- |
factrecall,whenthemodelhasindeedmemorized
|     |     |     |     |     |     | 2.2 LMsandheuristics |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- |
thecorrectanswerandrecallsitfortheprediction.
We show how interpretations of LMs can be ex- Researchintomodelperformanceonfactualbench-
tended to these scenarios and how each scenario marks has identified different factors affecting a
yieldsdistinctinterpretabilityresults. modelprediction. Accuratefactcompletionsmay
|                |     |           |       |       |      | stem from | superficial |     | cues | and learned |     | shallow |
| -------------- | --- | --------- | ----- | ----- | ---- | --------- | ----------- | --- | ---- | ----------- | --- | ------- |
| In particular, |     | this work | makes | three | main | con-      |             |     |      |             |     |         |
tributions. First, we propose a method, PRISM, heuristics, such as lexical overlap, person name
|     |     |     |     |     |     | bias3 orpromptbias4 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- |
forcreatingadiagnosticdatasetwithdistincttest (Poerneretal.,2020;Ladhak
etal.,2023;Caoetal.,2021).
| cases to | enable | more extensive |     | and precise |     | inter- |     |     |     |     |     |     |
| -------- | ------ | -------------- | --- | ----------- | --- | ------ | --- | --- | --- | --- | --- | --- |
pretations of fact completion in LMs (§3). We Whileshallowheuristicsareanaturalby-product
createandrelease PRISM datasetsforGPT-2XL, ofthewayLMsaretrainedandmayprovideashort-
|                                    |     |     |     |     |         | cut solution | for | some | samples, | they | rely | on dis- |
| ---------------------------------- | --- | --- | --- | --- | ------- | ------------ | --- | ---- | -------- | ---- | ---- | ------- |
| Llama27BandLlama213B,respectively. |     |     |     |     | Second, |              |     |      |          |      |      |         |
ourexperimentswiththeinterpretabilitymethodof putableandovergeneralizingassumptions. There-
causal tracing (CT) show that the models exhibit fore, LMs relying on shallow heuristics in a fact
a complex behavior on the PRISM scenarios not predictionsettingisgenerallyundesirable(McCoy
|                                  |     |     |     |              |     | et al., 2019). |     | For example, |     | Ladhak | et al. | (2023) |
| -------------------------------- | --- | --- | --- | ------------ | --- | -------------- | --- | ------------ | --- | ------ | ------ | ------ |
| capturedbypreviousresults(§4.1). |     |     |     | Third,ourin- |     |                |     |              |     |        |        |        |
depth analysis of information flow confirms that found that name bias leads to hallucinations and
modelsemploydistinctinferencemechanismsfor factuallyincorrectsummariesbyLMs.
| the PRISM | scenarios. |     | For example, |     | we observe |                           |     |     |     |     |     |     |
| --------- | ---------- | --- | ------------ | --- | ---------- | ------------------------- | --- | --- | --- | --- | --- | --- |
|           |            |     |              |     |            | 2.3 LMsandrandomguesswork |     |     |     |     |     |     |
contrastingresultsforexactfactrecallcomparedto
genericlanguagemodelingsamples(§4.2). Taken Fengetal.(2024)claimthatreliableLMsneedto
beabletoabstainfromgeneratinglow-confidence
| together, | our work | expands | on  | the scenarios |     | that     |                                   |     |     |     |     |     |
| --------- | -------- | ------- | --- | ------------- | --- | -------- | --------------------------------- | --- | --- | --- | --- | --- |
|           |          |         |     |               |     | outputs. | Meanwhile,mostopen-sourceLMsareas |     |     |     |     |     |
canbeanalyzedforinterpretationsofLMsforfact
completionandyieldnewinterpretationsofLMs.1 ofyetnotequippedwiththeabilitytoabstainand,
whilethereisalargebodyofresearchonthis,there
| 2 Background |          |     |       |            |     | isnofinalverdictonthebestmethodformeasuring |       |        |            |            |           |     |
| ------------ | -------- | --- | ----- | ---------- | --- | ------------------------------------------- | ----- | ------ | ---------- | ---------- | --------- | --- |
|              |          |     |       |            |     | model confidence                            |       | (Jiang | et         | al., 2021; | Vasudevan |     |
| This section | provides | a   | brief | background | on  | fact                                        |       |        |            |            |           |     |
|              |          |     |       |            |     | et al., 2019;                               | Burns | et     | al., 2023; | Yoshikawa  |           | and |
completionandmechanisticinterpretabilitytopics
Okazaki,2023;Zhaoetal.,2024).
relevanttoourwork.
|     |     |     |     |     |     | 2.4 Interpretabilityandfactcompletion |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --- |
2.1 LMsandmemorization
|     |     |     |     |     |     | Recent | work by | Meng | et al. | (2022); | Geva | et al. |
| --- | --- | --- | --- | --- | --- | ------ | ------- | ---- | ------ | ------- | ---- | ------ |
Alargebodyofinterpretabilityworkforfactcom-
(2023);Havivetal.(2023)hasfocusedontheinfer-
| pletion | situations | is concerned |     | with | whether | a   |     |     |     |     |     |     |
| ------- | ---------- | ------------ | --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- |
enceprocessofLMsforfactcompletionforsimple
modelhasmemorized2somefactornot,andwhere
insomeliterature,ofexactstringmemorization.
| 1Dataset |     |      |               |     |           | 3E.g.,predictingKyeJi-SutobeacitizenofSouthKorea |     |     |     |     |     |     |
| -------- | --- | ---- | ------------- | --- | --------- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- |
|          | and | code | are available |     | at https: |                                                  |     |     |     |     |     |     |
//github.com/dsaynova/lm_interpretation_ duetotheformofthename.
fact_completion. 4E.g.,predictingLondonfor“AdamDoewasbornin”due
2Notethatthetypeofmemorizationreferredtohereisof tothetrainingdatashowingstrongcorrelationsbetweenLon-
anabstractedrepresentationofthefactratherthan,asstudied donand“wasbornin”,disregardingthesubjectAdamDoe.

(subject,relation,object)facttuples,suchassub-
| ject Tokyo,           | relation | capital-of |                        | and | object | Japan, |     |     |     |     |     |     |
| --------------------- | -------- | ---------- | ---------------------- | --- | ------ | ------ | --- | --- | --- | --- | --- | --- |
| illustratedinFigure1. |          |            | Thisbodyofworkhypothe- |     |        |        |     |     |     |     |     |     |
sizesthatLMsfollowadistinctprocesswhenpro-
| ducingaccuratefactcompletions. |     |     |     | Thishypothesis |     |     |     |     |     |     |     |     |
| ------------------------------ | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
wasoriginallyposedbyMengetal.(2022)based
|     |     |     |     |     |     |     | Figure2: | Diagnosticcriteria(ingreen)fordefiningthe |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------------------------------------- | --- | --- | --- | --- |
onaggregationsofCTresults,whichrevealedade- fourpredictionscenarios(inblack).
cisiveroleofMLPmodulesat(lastsubjecttoken,
| mid layer) | positions | for | accurate | fact | completion |     |     |     |     |     |     |     |
| ---------- | --------- | --- | -------- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- |
predictions. This was reasoned to indicate that 1) critical information flows from middle-upper
thesemodulesrecallfactassociationsforasubject. subjectpositionlayerstothefinaltokenstatecorre-
Laterresultsbye.g.Gevaetal.(2023)supportthe
spondingtotheprediction(“attributeextraction”),
| sameconclusion. |     | 5   |     |     |     |     |     |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2)criticalinformationflowsfromearlynon-subject
positionlayers(“relationpropagation”)and3)the
2.5 Causaltracing
subjectpositionstateisenrichedwithattributesby
| Causal | tracing | is a mechanistic |     | interpretability |     |     |            |        |     |                      |     |       |
| ------ | ------- | ---------------- | --- | ---------------- | --- | --- | ---------- | ------ | --- | -------------------- | --- | ----- |
|        |         |                  |     |                  |     |     | MLP layers | before | the | attribute extraction |     | takes |
methodthathasprovidedmanyinterpretationsof place(“subjectenrichment”).
| LMs (Stolfo | et  | al., 2023; | Monea | et  | al., 2024). | It  |     |     |     |     |     |     |
| ----------- | --- | ---------- | ----- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
wasintroducedbyMengetal.(2022)andrelieson
thestudyofindirectcausaleffects. Bycorrupting 3 PRISM datasetsforprecisestudiesof
andrestoringcorruptedrepresentationsatdifferent predictionscenarios
| (token,    | layer) | positions | in a    | LM it | is possible | to  |           |       |                              |     |     |     |
| ---------- | ------ | --------- | ------- | ----- | ----------- | --- | --------- | ----- | ---------------------------- | --- | --- | --- |
| infer what | parts  | of the    | network | are   | important   | for |           |       |                              |     |     |     |
|            |        |           |         |       |             |     | Wedevelop | PRISM | (PreciseIdentificationofSce- |     |     |     |
assigningahighprobabilitytothepredictedtoken
nariosforModelbehavior)datasetstoseparatethe
with respect to the subject. The measured signal different prediction scenarios in Figure 1. This
| of model | component |     | importance | is  | referred | to as |              |     |               |        |       |       |
| -------- | --------- | --- | ---------- | --- | -------- | ----- | ------------ | --- | ------------- | ------ | ----- | ----- |
|          |           |     |            |     |          |       | is motivated | by  | an inspection | of the | 1,209 | Coun- |
indirecteffect.
terFactsampleswhichreveals510sampleslikely
Mengetal.(2022)alsodevelopedtheCounter-
|     |     |     |     |     |     |     | to rely | on heuristics | and | 365 samples | unlikely | to  |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------- | --- | ----------- | -------- | --- |
Factdataset.
Theirconclusionisbasedonthe1,209 havebeenmemorizedduetolowpopularityscores
knownsamplesfromCounterFactforwhichGPT-
(seeAppendixF).Wearguethattheseissuesmake
| 2 XL is | accurate. | By  | now, it | has been | frequently |     |     |     |     |     |     |     |
| ------- | --------- | --- | ------- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
theCounterFactdatasetunabletosupportprecise
usedfortheinterpretationofLMsperformingfact andcomprehensiveinterpretationsofLMs,missing
completion(Gevaetal.,2023).
outonimportantdistinctionsandvaluableinsights
|     |     |     |     |     |     |     | intotheworkingsofLMs. |     |     | PRISMisdevelopedto |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | ------------------ | --- | --- |
2.6 Studiesofinformationflow
addresstheseshortcomings.
Gevaetal.(2023)analyzeinformationflowinLMs
|     |     |     |     |     |     |     | PRISM | datasets | are | created by | the identifica- |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | -------- | --- | ---------- | --------------- | --- |
forfact-relatedqueriesfromCounterFacttounder-
|     |     |     |     |     |     |     | tion and | generation | of  | samples corresponding |     | to  |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---------- | --- | --------------------- | --- | --- |
standhowinformationisretrievedinternallyduring
|            |     |        |       |          |         |     | each of | the four | prediction | scenarios | in Figure | 1.  |
| ---------- | --- | ------ | ----- | -------- | ------- | --- | ------- | -------- | ---------- | --------- | --------- | --- |
| inference. | We  | mainly | focus | on their | methods | of  |         |          |            |           |           |     |
Theprocessreliesonthreediagnostictestcriteria
attentionknockouttostudyfromwhat(tokenposi-
|     |     |     |     |     |     |     | (Figure | 2). Note | that PRISM | datasets | are | model- |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------- | ---------- | -------- | --- | ------ |
tion,layer)statecriticalinformationflowsforthe
|     |     |     |     |     |     |     | specific | since they | depend | on model | biases | and |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---------- | ------ | -------- | ------ | --- |
predictionandlogitlenstoinvestigateattributeex-
parametricmemories,whichdifferbetweenLMs.
tractioninintermediateMLPandmulti-headself-
attention (MHSA) states. Using these methods, WedevelopPRISMdatasetsforGPT-2XL(Rad-
Gevaetal.(2023)findthreemainwaysinwhichin- ford et al., 2019), Llama 2 7B and Llama 2 13B.
|     |     |     |     |     |     |     | (Touvronetal.,2023),respectively. |     |     |     | Generalstatis- |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | -------------- | --- |
formationflowsinLMsforfact-relatedpredictions:
ticsforthedatasetscanbefoundinTable1andex-
5Theseknowledgelocalizationeffortsaresomewhator-
amplescorrespondingtoeachpredictionscenario
thogonaltoworkonmodelediting.Whilelocalizationresults
canbefoundinAppendixE.Thesamplesandour
fromCTmaynotidentifytheoptimalparametersforknowl-
edge editing, this does not mean that CT is inaccurate for subsequentanalysisisfocusedontheEnglishlan-
| knowledgelocalization. |     | Itsimplymeansthat“localization |     |     |     |     |                                               |     |     |     |     |     |
| ---------------------- | --- | ------------------------------ | --- | --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- |
|                        |     |                                |     |     |     |     | guage. Furtherdetailsontheimplementationofthe |     |     |     |     |     |
analysismightansweradifferentquestionthanthequestion
datasetscanbefoundinAppendixD.
answeredbymodelediting”(Haseetal.,2023).

|     |     |     | GPT-2XL |     |     | Llama27B |     |     | Llama213B |     |     |     |     |
| --- | --- | --- | ------- | --- | --- | -------- | --- | --- | --------- | --- | --- | --- | --- |
Scenario #samples(#facttuples) #samples(#facttuples) #samples(#facttuples)
|     | GenericLM  |         | 1,000(-)                                                    |     |     | 1,000(-)     |     |     | 1,000(-)     |     |     |     |     |
| --- | ---------- | ------- | ----------------------------------------------------------- | --- | --- | ------------ | --- | --- | ------------ | --- | --- | --- | --- |
|     | Guesswork  |         | 3,282(3,181)                                                |     |     | 2,917(2,846) |     |     | 2,822(2,220) |     |     |     |     |
|     | Heuristics |         | 8,352(1,868)                                                |     |     | 8,414(1,960) |     |     | 9,224(2,062) |     |     |     |     |
|     | Exactfact  |         | 1,322(191)                                                  |     |     | 5,481(580)   |     |     | 5,995(601)   |     |     |     |     |
|     |            | Table1: | StatisticsforthePRISMdatasetsforeachLMconsideredinourstudy. |     |     |              |     |     |              |     |     |     |     |
Ifaqueryexpressesanincompletefact(subject
| 3.1 Diagnosticcriteria |     |     |     |     |     |     | as: |     |     |     |     |     |     |
| ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
andrelation)andthepredictioncorrespondstoan
| To create | the | PRISM         | datasets | we propose |          | three |                                       |     |     |     |     |              |        |
| --------- | --- | ------------- | -------- | ---------- | -------- | ----- | ------------------------------------- | --- | --- | --- | --- | ------------ | ------ |
|           |     |               |          |            |          |       | entityorconceptthathasavalidtype(e.g. |     |     |     |     |              | aplace |
| necessary | and | comprehensive |          | diagnostic | criteria |       |                                       |     |     |     |     |              |        |
|           |     |               |          |            |          |       | namewhenaskingaboutlocation).         |     |     |     |     | Thisexcludes |        |
forwhichwedefinemeasurements(seeFigure2):
predictionssuchas“the”,“a”and“with”.
(1)Doesthepredictionrepresentfactcompletion
| ratherthangenericlanguagemodeling? |     |     |     |     | (2)Isthe |     |           |            |     |     |        |           |     |
| ---------------------------------- | --- | --- | --- | --- | -------- | --- | --------- | ---------- | --- | --- | ------ | --------- | --- |
|                                    |     |     |     |     |          |     | Confident | prediction |     | Our | second | criterion | is  |
predictionconfidentandrobusttoinsignificantsig-
confidentprediction–whetherthepredictioncan
nals in the prompt? (3) Is the prediction based beconsideredconfident,e.g. bybeingrobustacross
| on the exact | factual       | information |           | expressed        | in  | the |                                       |     |     |     |     |           |     |
| ------------ | ------------- | ----------- | --------- | ---------------- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --------- | --- |
|              |               |             |           |                  |     |     | insignificantperturbationstothequery. |     |     |     |     | Sincemost |     |
| query or     | on heuristics |             | triggered | by surface-level |     |     |                                       |     |     |     |     |           |     |
LMsbydefaultcannotabstainfromanswering,we
cues? These criteria provide a more fine-grained mayendupinsituationswhenaLMmakesthecor-
testingsetupcomparedtousingasingleaccuracy- rectpredictionbychancewhileitrandomlyselects
focusedcriterion,asinpreviouswork.
|                |     |                             |     |     |     |     | atokenofthecorrecttype(e.g. |     |     |     | acitywhenasked |            |     |
| -------------- | --- | --------------------------- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | -------------- | ---------- | --- |
|                |     |                             |     |     |     |     | for a birthplace)           |     | but | has | no relevant    | parametric |     |
| Factcompletion |     | Ourfirstcriterionisfactcom- |     |     |     |     |                             |     |     |     |                |            |     |
knowledgeofthespecificfact.
| pletion | – whether | a prompt |     | and the model’s |     | pre- |         |            |     |          |          |     |        |
| ------- | --------- | -------- | --- | --------------- | --- | ---- | ------- | ---------- | --- | -------- | -------- | --- | ------ |
|         |           |          |     |                 |     |      | For the | collection |     | of PRISM | samples, |     | we opt |
dictioncorrespondtothesettingofamodelcom-
|               |                               |     |     |     |     |     | for a definition   |     | of confidence |                        | grounded |     | in desir- |
| ------------- | ----------------------------- | --- | --- | --- | --- | --- | ------------------ | --- | ------------- | ---------------------- | -------- | --- | --------- |
| pletingafact. | Bymakingsurethemodelisstudied |     |     |     |     |     |                    |     |               |                        |          |     |           |
|               |                               |     |     |     |     |     | ablemodelbehavior. |     |               | Weproxymodelconfidence |          |     |           |
onlyinfactcompletionsituations,interpretations
byconsistencyinthefaceofsemanticallyequiva-
canbeassumedtoelucidatesomefactprocessing
lentqueries(Elazaretal.,2021;PortilloWightman
| behavior. | This | as opposed |     | to, for example, |     | the |               |      |     |            |     |         |       |
| --------- | ---- | ---------- | --- | ---------------- | --- | --- | ------------- | ---- | --- | ---------- | --- | ------- | ----- |
|           |      |            |     |                  |     |     | et al., 2023; | Zhao | et  | al., 2024) | and | measure | it as |
LMgeneratingastoryaboutunicorns,forwhicha
theagreementacrossparaphrasesfromtheParaRel
differentmodelbehaviorisassumedtotakeplace.
dataset(Elazaretal.,2021).
Thiscriterionisalreadyimplicitlyusedinprevious
Wedefinethemeasurementforconfidentpredic-
researchoninterpretationsofLMsforfactcomple-
|     |     |     |     |     |     |     | tionas: | Ifapredictionoccursamongthetop3pre- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ----------------------------------- | --- | --- | --- | --- | --- |
tion(Petronietal.,2019;Mengetal.,2022;Geva
|     |     |     |     |     |     |     | dictionsforatleast5paraphrasedqueries. |     |     |     |     |     | Apre- |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- | --- | ----- |
etal.,2023),wesimplymakeitexplicit.
dictionthatonlyappearsforoneoftherephrased
Followingthisbodyofwork,forfactcompletion
|          |           |     |        |              |         |     | queries    | is deemed |        | unconfident. |     | The thresholds |      |
| -------- | --------- | --- | ------ | ------------ | ------- | --- | ---------- | --------- | ------ | ------------ | --- | -------------- | ---- |
| we limit | ourselves | to  | simple | queries that | express |     |            |           |        |              |     |                |      |
|          |           |     |        |              |         |     | were based | on        | manual | inspection   |     | to ensure      | ade- |
anincompletefact(subjectandrelation),withthe
quatesamplingofconfidentandunconfidentsam-
intenttolettheLMgeneratetheobjectasthenext
|     |     |     |     |     |     |     | ples. Since | we  | use | several | tests | to establish | the |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | ------- | ----- | ------------ | --- |
token. WeuseParaRelquerytemplatestocollect
typeofprediction,webelieveaslightvariationof
| samples | of fact | completion |     | (Elazar et | al., 2021). |     |     |     |     |     |     |     |     |
| ------- | ------- | ---------- | --- | ---------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
thesethresholdvalueswillnotleadtoasubstantial
Theseareasetofrephrasedexpressionsofarela-
|     |     |     |     |     |     |     | differenceintheexamplesgenerated. |     |     |     |     | Moreover,as |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- | ----------- | --- |
tion,whereadifferentsubjectXcanbesubstituted
observedinSection2,thereisnocleardefinitionof
atthefirstpositionandanobjectYisexpectedas
confidentprediction,whyweoptedforcreatingour
| the next     | token     | to be generated. |         | For example, |      | for |                    |      |     |         |                    |     |         |
| ------------ | --------- | ---------------- | ------- | ------------ | ---- | --- | ------------------ | ---- | --- | ------- | ------------------ | --- | ------- |
|              |           |                  |         |              |      |     | own. Other         | work | may | propose | alternative        |     | defini- |
| the relation | “born-in” |                  | we have | templates    | such | as  |                    |      |     |         |                    |     |         |
|              |           |                  |         |              |      |     | tionsofconfidence, |      |     | PRISM   | caneasilybeadapted |     |         |
“[X]wasbornin[Y]”or“[X]isoriginallyfrom[Y]”
totheseaswell.
| (seeAppendixCforafulllist). |     |     |     | Intotal,7different |     |     |     |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
relations are used, each with at least 5 different Usageofheuristics Ourthirdandfinalcriterion
templatesforqueryvariations. isnodependenceonheuristics–indicatingifthe
Wedefinethemeasurementforfactcompletion prediction is based on the exact factual informa-

tion expressed in the prompt (subject and rela- multipletoptokenswebreaktheover-relianceof
tion)ratherthanonlyonpartialsignals,i.e.heuris- previous work on accuracy of the top prediction
tics. Predictionsdependingonheuristicsindicate andaccountforalargerportionoftheLMoutput
| anover-relianceonunintendedcorrelationsinthe |     |     |     |     |     |     | distribution. |     |     |     |     |     |     |
| -------------------------------------------- | --- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- |
trainingdatasetbasedonsurfaceformsofnames
orprompts,andarethereforeunreliable(Caoetal., Genericlanguagemodeling Wedefinesamples
|     |     |     |     |     |     |     | correspondingto(factcompletion: |     |     |     | False)asrepre- |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | -------------- | --- | --- |
2021;McCoyetal.,2019;Biranetal.,2024).
sentativeofagenericlanguagemodelingscenario.
| For the | collection |     | of PRISM | samples |     | we use |     |     |     |     |     |     |     |
| ------- | ---------- | --- | -------- | ------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
twoindicators: presenceofsurface-levelcuesand Generic language modeling samples are re-
trievedfromWikipedia.7
memorization estimation. If a model indicates it Wefollowanapproach
similartothatofHavivetal.(2023)toensurethat
haslearnedaheuristicrelatedtotheprediction,itis
weonlycollectsamplescorrespondingtogeneric
| likelythisisusedforcompletingthequery. |     |     |     |     |     | Addi- |     |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
tionally,ifweknowthattheLMdoesnotknowthe languagemodelingandnotfactcompletion. The
factrequestedbyapromptbutitstillmakesaconfi- extractionisdonebysamplingsentencesthatstart
|     |     |     |     |     |     |     | with the | subject | of the | article | in order | to  | comply |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------- | ------ | ------- | -------- | --- | ------ |
dentprediction,wecanassumethattheprediction
correspondstosomeformofheuristicsrecall. withthecausalnatureofthemodelsandtoallow
Weusethreetypesoffiltersforthedetectionof forcausalinterventionsonthesubject. Wediscard
thesentenceifitsnaturalcontinuationbeginswith
| heuristics: | Lexical |     | overlap | (between | subject | and |     |     |     |     |     |     |     |
| ----------- | ------- | --- | ------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
acapitalletteroranumber(indicatingthiscould
prediction),personnamebiasandpromptbiasfil-
ters. ThetwoformerfiltersarefromPoerneretal. beanentityandthuspotentiallyfactcompletion).
| (2020)                       | and the     | latter | is based         | on  | the findings  | by  |                            |                                       |     |     |                    |         |        |
| ---------------------------- | ----------- | ------ | ---------------- | --- | ------------- | --- | -------------------------- | ------------------------------------- | --- | --- | ------------------ | ------- | ------ |
|                              |             |        |                  |     |               |     | Random                     | guesswork                             |     | We  | define             | samples | corre- |
| Caoetal.(2021)(AppendixD.5). |             |        |                  |     | Weusefactpop- |     |                            |                                       |     |     |                    |         |        |
|                              |             |        |                  |     |               |     | spondingto(factcompletion: |                                       |     |     | True,confidentpre- |         |        |
| ularity                      | to estimate |        | model knowledge, |     | proxied       | by  |                            |                                       |     |     |                    |         |        |
|                              |             |        |                  |     |               |     | diction:                   | False)asrepresentativeofarandomguess- |     |     |                    |         |        |
Wikipediapageviewsfortheyear20196,basedon
workscenario.
| work by | Mallen | et  | al. (2023), | where | the | authors |     |     |     |     |     |     |     |
| ------- | ------ | --- | ----------- | ----- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
Forthecollectionofrandomguessworksamples,
| find a strong |     | correlation | between |     | popularity | and |     |     |     |     |     |     |     |
| ------------- | --- | ----------- | ------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
wefirstpopulateParaReltemplateswithsubjects
memorization.
|     |     |     |     |     |     |     | andobjectsfromLAMA(Petronietal.,2019). |     |     |     |     |     | We  |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- | --- | --- |
Wedefinethemeasurementforusageofheuris-
|     |     |     |     |     |     |     | retain (query, |     | prediction) | samples |     | for which | the |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ----------- | ------- | --- | --------- | --- |
ticsas: Ifapredictionisnotbasedonmemorization
andthequerycontainssurface-levelcues. predictionisavalidobjectfromLAMA(e.g. acity
|                     |     |     |     |     |     |     | whenaskedforbirthplaces)butunconfident(i.e. |     |     |     |     |     | it  |
| ------------------- | --- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- |
| 3.2 Datasetcreation |     |     |     |     |     |     | doesnotoccuramongthetop3predictionsforat    |     |     |     |     |     |     |
least5paraphrasedqueries).
Usingtheabovecriteria,webuildPRISMdatasets
| of (query, | prediction) |           | samples    | representative |            | of  |                       |     |                            |                           |     |     |     |
| ---------- | ----------- | --------- | ---------- | -------------- | ---------- | --- | --------------------- | --- | -------------------------- | ------------------------- | --- | --- | --- |
|            |             |           |            |                |            |     | Heuristicsrecall      |     | Wedefinesamplescorrespond- |                           |     |     |     |
| each of    | four        | potential | prediction |                | scenarios: | 1)  |                       |     |                            |                           |     |     |     |
|            |             |           |            |                |            |     | ingto(factcompletion: |     |                            | True,confidentprediction: |     |     |     |
genericlanguagemodeling,2)randomguesswork,
|                                         |     |     |     |     |     |        | True,nousageofheuristics: |     |     |     | False)asrepresenta- |     |     |
| --------------------------------------- | --- | --- | --- | --- | --- | ------ | ------------------------- | --- | --- | --- | ------------------- | --- | --- |
| 3)heuristicsrecalland4)exactfactrecall. |     |     |     |     |     | Inthis |                           |     |     |     |                     |     |     |
tiveofaheuristicsrecallscenario.
section,weintroducedefinitionsoftheprediction
WecollectthesesamplesbypopulatingParaRel
| scenarios        | based  | on  | our diagnostic              |        | criteria,     | illus- |             |                                    |           |      |        |       |        |
| ---------------- | ------ | --- | --------------------------- | ------ | ------------- | ------ | ----------- | ---------------------------------- | --------- | ---- | ------ | ----- | ------ |
|                  |        |     |                             |        |               |        | templates   | with                               | synthetic | fact | tuples | from  | a name |
| trated in        | Figure | 2,  | and our                     | method | for producing |        |             |                                    |           |      |        |       |        |
|                  |        |     |                             |        |               |        | generator   | (more                              | details   | can  | be     | found | in Ap- |
| thePRISMsamples. |        |     | Ourgoalistocreatesplitsthat |        |               |        |             |                                    |           |      |        |       |        |
|                  |        |     |                             |        |               |        | pendixD.3). | Sincethesubjectsaresynthetic,facts |           |      |        |       |        |
containasinglepredictionscenarioratherthanto
|     |     |     |     |     |     |     | about them | cannot | have | been | memorized |     | by the |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | ---- | ---- | --------- | --- | ------ |
identifyallsamplesthatcorrespondtothatscenario.
|     |     |     |     |     |     |     | model(Liuetal.,2023;Basmovetal.,2024). |     |     |     |     |     | Fil- |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- | --- | ---- |
Assuch,weoptforstricterthresholdswhenneeded
|           |      |           |          |     |              |     | tering confident |     | predictions |     | of valid | objects | for |
| --------- | ---- | --------- | -------- | --- | ------------ | --- | ---------------- | --- | ----------- | --- | -------- | ------- | --- |
| to ensure | high | precision | samples. |     | Our approach |     |                  |     |             |     |          |         |     |
whichasingletypeofbiasisidentifiedformsour
isnotintendedtoclassifyeveryinstanceintoone
heuristicsrecallsamples.
ofthefourscenarios,buttoproducehigh-quality
examplesofeachone. Exactfactrecall Wedefinesamplescorrespond-
For thecollection of PRISM samples, wecon- ingto(factcompletion: True,confidentprediction:
| sider the | top | 3 model | predictions. |     | By looking | at  |     |     |     |     |     |     |     |
| --------- | --- | ------- | ------------ | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
7Weuse20220301.enfromHuggingFaceathttps:
| 6UsingthePageviewAPI. |     |     |     |     |     |     | //huggingface.co/datasets/wikipedia |     |     |     |     |     |     |
| --------------------- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- | --- | --- |

True, no usage of heuristics: True) as representa- Predictionscenariosinisolation Resultsforthe
tiveofanexactfactrecallscenario. Theexactfact generic language modeling samples in Figure 3a
recallscenariocorrespondstosituationsforwhich indicatenocriticalroleoflastsubjecttokenposi-
theLMcanbeexpectedtohavememorizedthefull tionMLPstates(usedtoindicatememoryaccess).
facttupleexpressedbythequeryandfetchesthis This further supports the original hypothesis that
frommemoryfortheprediction. mid-layerMLPstatesactasmemorystorage,since
To obtain samples representative of exact fact theydonotengageforsamplesthatdonotrequire
| recall,weagainusetheLAMAfacttuples. |     |     |     |     |     | Wecol- | memorization. |         |     |     |            |        |         |
| ----------------------------------- | --- | --- | --- | --- | --- | ------ | ------------- | ------- | --- | --- | ---------- | ------ | ------- |
|                                     |     |     |     |     |     |        | We also       | observe |     | how | last token | states | in late |
lectpredictionsthatare1)confident,2)notlabeled
ascorrespondingtoanybias,3)correspondingtoa layersaredecisiveforgenericlanguagemodeling
factmemorizedbytheLM,and4)correct. and guesswork. Meng et al. (2022) recorded a
similarpeakintheirresults,whilethereisnoclear
4 Interpretabilityand PRISM hypothesisastowhatinformationisprocessedhere.
Wealsonotethatthemagnitudeofthepeakismuch
| We apply | two | mechanistic |     | interpretability |     | ap- |         |           |      |         |            |     |           |
| -------- | --- | ----------- | --- | ---------------- | --- | --- | ------- | --------- | ---- | ------- | ---------- | --- | --------- |
|          |     |             |     |                  |     |     | smaller | for exact | fact | recall, | indicating |     | that this |
proaches–CTandinformationflowanalysis–to peakandthecomputationsitcorrespondstomay
testtheirsensitivitytoeachpredictionscenarioin signifyalackofexactfactrecall.
| PRISM.8 | Thisallowsustoevaluatethevalidityof |     |     |     |     |     |     |         |         |            |     |        |            |
| ------- | ----------------------------------- | --- | --- | --- | --- | --- | --- | ------- | ------- | ---------- | --- | ------ | ---------- |
|         |                                     |     |     |     |     |     | The | results | for the | heuristics |     | recall | samples in |
previousinterpretabilityresults.
Figure3cshownodecisiveroleofanyparticularto-
kenpositionstate,whilewenotethatitcorresponds
4.1 Causaltracing
toahigherimportanceoflastsubjecttokenstates
First, we investigate the sensitivity of CT to the comparedtogenericlanguagemodeling,indicating
PRISM scenarios. Weaimtoaddressthequestion thatsomememorizedinformationisinuse.
DoCTresultsandthecorrespondingconclusions Resultsforexactfactrecallsamples(Figure3d)
changewiththeunderlyingpredictionscenario(s)? arefundamentallydifferentfromthoseoftheother
CT measures the importance of different (token, isolated scenarios. The exact fact recall results
|                  |     |       |         |             |     |         | show a | clear | peak | in AIE | in (last | subject | token, |
| ---------------- | --- | ----- | ------- | ----------- | --- | ------- | ------ | ----- | ---- | ------ | -------- | ------- | ------ |
| layer) positions |     | for a | certain | prediction. |     | In line |        |       |      |        |          |         |        |
withMengetal.(2022),weanalyzetheaveraged midlayer)MLPstates. Thisistheonlyprediction
indirect effects (AIE) per (token, layer) position, scenariothatclearlysupportsthesameconclusion
binning the input tokens into the following cate- as previous work in that (last subject token, mid
gories: first, middle, and last subject token; first layer)MLPstatesaredecisive. Thisprovidesaddi-
subsequenttoken;furthertokens;lasttoken. tionalsupportforthehypothesisproposedbyMeng
To adjust for differences in absolute values of etal.(2022),astheexactfactrecallsamplesfurther
|     |     |     |     |     |     |     | emphasize | the | pattern | interpreted |     | to indicate | the |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------- | ----------- | --- | ----------- | --- |
theprobabilityofthepredictedtoken,wetakein-
spiration from Hase et al. (2023) and normalize memorystorageroleofmidMLPlayers.
resultsbyhowmuchtheoutputtokenprobability
|     |     |     |     |     |     |     | Aggregations |     | of prediction |     | scenarios |     | To test |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ------------- | --- | --------- | --- | ------- |
wasreducedwhencorruptingthesubjectinforma-
theeffectsofanalyzingmixedsamples,weproduce
tion. Thismeasuresthepercentageofrecoverable
resultsforamixtureoffactcompletionscenarios.
probabilitythatwasrestoredbypatchingamodel
|            |            |     |            |     |             |     | Thecombinedplotofexactfactrecall, |     |     |     |     |     | heuristics |
| ---------- | ---------- | --- | ---------- | --- | ----------- | --- | --------------------------------- | --- | --- | --- | --- | --- | ---------- |
| state. For | a detailed |     | discussion | of  | the effects | of  |                                   |     |     |     |     |     |            |
recall,andguessworksamplesinFigure3egener-
normalization,seeAppendixG.
|        |         |          |     |            |     |          | ally reproduces |       | the | same    | CT results | as  | observed |
| ------ | ------- | -------- | --- | ---------- | --- | -------- | --------------- | ----- | --- | ------- | ---------- | --- | -------- |
| Figure | 3 shows | averaged |     | normalized |     | indirect |                 |       |     |         |            |     |          |
|        |         |          |     |            |     |          | in previous     | work, | and | thereby | supports   |     | the same |
effectsofmodelstatesinGPT-2XLfor1000sam-
|     |     |     |     |     |     |     | conclusion,i.e. |     | (lastsubjecttoken,midlayer)MLP |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------------------------------ | --- | --- | --- | --- |
plescorrespondingtoeachpredictionscenarioof
|       |              |     |         |      |          |      | statesaredecisive(Mengetal.,2022). |     |     |     |     |     | Thisindi- |
| ----- | ------------ | --- | ------- | ---- | -------- | ---- | ---------------------------------- | --- | --- | --- | --- | --- | --------- |
| PRISM | in isolation |     | as well | as a | combined | plot |                                    |     |     |     |     |     |           |
catesthatmodelinterpretationsoversamplesmix-
| of the 3 | fact completion |     | cases | (exact | fact | recall, |     |     |     |     |     |     |     |
| -------- | --------------- | --- | ----- | ------ | ---- | ------- | --- | --- | --- | --- | --- | --- | --- |
ingpredictionscenariosaremisleadingastheymay
| heuristicsrecall,andguesswork). |     |     |     | Thecorrespond- |     |     |     |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
bedominatedbythecharacteristicsoftheexactfact
| ing results | for Llama |     | 2 7B and | Llama | 2   | 13B can |                 |     |                                 |     |     |     |     |
| ----------- | --------- | --- | -------- | ----- | --- | ------- | --------------- | --- | ------------------------------- | --- | --- | --- | --- |
|             |           |     |          |       |     |         | recallscenario. |     | Potentially,thiscouldbeduetothe |     |     |     |     |
befoundinAppendixH.1–theysupportthesame
exactfactrecallsamplesgenerallycorresponding
conclusionsasreachedforGPT-2XL.
tohigherpredictionconfidences.
|     |     |     |     |     |     |     | This | supports | our | hypothesis |     | that previous | in- |
| --- | --- | --- | --- | --- | --- | --- | ---- | -------- | --- | ---------- | --- | ------------- | --- |
8Weusethesamehyperparametersastheoriginalstudies.

| EIA dezilamroN 0.4 |     |     |     | EIA dezilamroN | 0.4 |     | 0.5 |     |     |     |     |     |
| ------------------ | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
First subject token
|     |     |     |     |     |     |     | 0.4            |     |     | Middle subject tokens |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- | --------------------- | --- | --- |
| 0.2 |     |     |     |     | 0.2 |     | EIA dezilamroN |     |     | Last subject token    |     |     |
0.3
First subsequent token
| 0.0 |     |     |     |     | 0.0 |     |     |     |     |                |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- |
|     |     |     |     |     |     |     | 0.2 |     |     | Further tokens |     |     |
Last token
| 0   | 10  | 20  | 30  | 40  | 0 10 | 20  | 30  | 40  |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
0.1
|                                    |     | layer |     |     |                         | layer |     |     |     |     |     |     |
| ---------------------------------- | --- | ----- | --- | --- | ----------------------- | ----- | --- | --- | --- | --- | --- | --- |
| (a)Genericlanguagemodelingsamples. |     |       |     |     | (b)Guessworksam0.0ples. |       |     |     |     |     |     |     |
0.1
| EIA dezilamroN 0.4 |     |       |     | EIA dezilamroN | 0.4  |       |     | EIA dezilamroN | 0.4                          |       |       |     |
| ------------------ | --- | ----- | --- | -------------- | ---- | ----- | --- | -------------- | ---------------------------- | ----- | ----- | --- |
|                    |     |       |     |                |      |       |     | 0              | 10                           | 20 30 | 40    |     |
| 0.2                |     |       |     |                | 0.2  |       |     |                | Layer number in GPT-2-XL 0.2 |       |       |     |
| 0.0                |     |       |     |                | 0.0  |       |     |                | 0.0                          |       |       |     |
| 0                  | 10  | 20    | 30  | 40             | 0 10 | 20    | 30  | 40             | 0                            | 10    | 20 30 | 40  |
|                    |     | layer |     |                |      | layer |     |                |                              |       | layer |     |
(c)Heuristicsrecallsamples. (d)Exactfactrecallsamples. (e)Combinedsamples.
Figure3: CTresultsfor PRISM GPT-2XLdata. 1000samplesforeachscenarioinisolation. Aswellas1000
combined samples (330 exact fact recall, 340 heuristics recall, 330 guesswork). Shaded regions indicate 95%
confidenceintervals.
| subject       | non-subject |     | last          |     |       |               |     |       |     |               |       |     |
| ------------- | ----------- | --- | ------------- | --- | ----- | ------------- | --- | ----- | --- | ------------- | ----- | --- |
| p ni egnahc % |             |     | p ni egnahc % |     |       | p ni egnahc % |     |       |     | p ni egnahc % |       |     |
| 0             |             |     |               | 0   |       |               | 0   |       |     | 0             |       |     |
| 50            |             |     | 50            |     |       |               | 50  |       |     | 50            |       |     |
| 0             | 20          | 40  |               | 0   | 20    | 40            | 0   | 20    | 40  |               | 0 20  | 40  |
|               | layer       |     |               |     | layer |               |     | layer |     |               | layer |     |
(a)Genericlanguagemodeling (b)Guesswork (c)Heuristicsrecall (d)Exactfactrecall
Figure4: Relativechangeinthepredictionprobabilitywheninterveningonattentionedgestothelastpositionfor
windowsizesof9layersinGPT-2XLonPRISMdata. Shadedregionsindicate95%confidenceintervals.
MHSA MLP
etar noitcartxe etar noitcartxe etar noitcartxe etar noitcartxe
| 0.2 |       |     | 0.2 |     |       |     | 0.5 |       |     | 0.2 |       |     |
| --- | ----- | --- | --- | --- | ----- | --- | --- | ----- | --- | --- | ----- | --- |
| 0.0 |       |     | 0.0 |     |       |     | 0.0 |       |     | 0.0 |       |     |
| 0   | 20    | 40  |     | 0   | 20    | 40  | 0   | 20    | 40  |     | 0 20  | 40  |
|     | layer |     |     |     | layer |     |     | layer |     |     | layer |     |
(a)Genericlanguagemodeling (b)Guesswork (c)Heuristicsrecall (d)Exactfactrecall
Figure5: AttributeextractionratesacrosslayersmeasuredforPRISMGPT-2XLdata. MHSAandMLPindicate
|     |     |     |     | k = | 1)  |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
attribution extraction rates (top for multi-head self-attention states and multilayer perceptron states,
respectively. Notethechangeinupperyaxislimitfrom0.35to0.9forheuristicsrecallin(c). Shadedregions
indicate95%confidenceintervals.
terpretabilityresultsmayhavebeenrecordedover a balanced four-way classification task. CT out-
mixturesofpredictionscenarios,aswecanrepro- putsAIEforeach(token,layer)position,thusfor
duce their results with a mixture. We do not use eachtoken,weobtainavectorofAIEvalues(for
this as proof that these results are based on mix- all model layers), similar to the ones in Figure 3.
tures (see Appendix F). We rather wish to show Modelsaretrainedtopredictthescenariobasedon
how, without precise testing data, we can reach theAIEvectorsforthefirstandlastsubjecttoken
conclusionsthatarenotsupportedbyalargepart aswellasthelastprompttoken(foundtobemost
ofthestudiedsample(67%). distinct between scenarios). The models achieve
anaccuracyof0.72forGPT-2XL,0.78forLlama
| Predictivepotential |     | Wealsoinvestigatethepo- |     |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
27B,and0.74forLlama213B(AppendixI).We
tentialfordevelopingpredictivesystemsbasedon
takethistoindicatehighcorrelationsbetweenin-
| ourtaxonomyandinternalmodelstates. |     |     |     |     | Wetrain |     |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
ternalmodelstatesandpredictionscenarios,illus-
asingle-layerneuralnetworkwith50neuronson

tratingapotentialofdevelopingnovelmethodsfor information. This is also supported by the clear
disambiguatingtypesofmodelbehavior. importanceofmidlayerlastsubjectpositionMLP
statesinFigure3d.
4.2 Informationflow
Forthegenericlanguagemodelingscenario,we
Inoursecondexperimentweinvestigatethesensi-
notethatonlyinformationfromearlynon-subject
| tivityofinformationflowanalysistothe |               |     |           |          | PRISM       |         |             |                                 |             |     |     |                  |     |
| ------------------------------------ | ------------- | --- | --------- | -------- | ----------- | ------- | ----------- | ------------------------------- | ----------- | --- | --- | ---------------- | --- |
|                                      |               |     |           |          |             |         | position    | layers                          | is critical | for | the | final prediction |     |
| scenarios.                           | Specifically, |     | we        | leverage | information |         |             |                                 |             |     |     |                  |     |
|                                      |               |     |           |          |             |         | inFigure4a. | Wealsorecordhighextractionrates |             |     |     |                  |     |
| flow localization                    |               | via | attention |          | knockout    | and at- |             |                                 |             |     |     |                  |     |
fromthelateMLPstatesinFigure5aandaclear
tributeextractionvialogitlens(Gevaetal.,2023).
|        |         |     |             |      |               |     | importanceoflateMLPstatesinFigure3a. |     |     |     |     |     | Based |
| ------ | ------- | --- | ----------- | ---- | ------------- | --- | ------------------------------------ | --- | --- | --- | --- | --- | ----- |
| Figure | 4 shows |     | the results | from | the attention |     |                                      |     |     |     |     |     |       |
ontheseresults,weproposethatgenericlanguage
| knockout | experiments |     | and | Figure | 5 the attribute |     |     |     |     |     |     |     |     |
| -------- | ----------- | --- | --- | ------ | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
modelingpredictionsmainlystemfromlateMLP
| extraction | results. |     | Similarly | to  | the CT results | in  |     |     |     |     |     |     |     |
| ---------- | -------- | --- | --------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
computationssolelybasedontheprecedingtokens,
Section4.1,eachpredictionscenariocorresponds
withlittlenotionofthesubjectunderconsideration.
toauniqueinformationflowandextractionratepat-
Fortheguessworkscenario,wemeasureaflow
tern. ThisfurthersupportsourclaimthatPRISM
quitesimilartowhatwasmeasuredbyGevaetal.
| samples | can | be used | to study | LM  | behaviors | for |     |     |     |     |     |     |     |
| ------- | --- | ------- | -------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
(2023)(Figure4b),withtheexceptionoftheearly
| differentpredictionscenarios. |     |     |     | Adeeperanalysisof |     |     |     |     |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
theresultsisstructuredaroundtwomainquestions: subjectandnon-subjectpositionlayerstatesbeing
moreimportantthanlatesubjectpositionstatesfor
Doourresultssupportthesameconclusionsas
|                        |     |     |     |                 |     |     | guesswork. | The      | extraction |          | rates in | Figure | 5b are  |
| ---------------------- | --- | --- | --- | --------------- | --- | --- | ---------- | -------- | ---------- | -------- | -------- | ------ | ------- |
| reachedinpreviouswork? |     |     |     | Wefocusonthetwo |     |     |            |          |            |          |          |        |         |
|                        |     |     |     |                 |     |     | much lower | compared |            | to those | measured |        | for the |
conclusions from Geva et al. (2023) related to 1) CounterFactandexactfactrecallsamples,however.
criticalinformationflowsfrommiddle-uppersub- Adeeperanalysisoftheextractionratesincluding
jectpositionlayerscorrespondingtoaprediction
|     |     |     |     |     |     |     | the top k | = 3 | and top | k = | 10 prediction |     | extrac- |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------- | --- | ------------- | --- | ------- |
probabilitydecreaseof60%and2)criticalinforma-
tionratesinAppendixJrevealthatthepredictedat-
tion flows from early non-subject position layers tributeseeminglyisextracted,whileitisnotamong
correspondingtoaprobabilitydecreaseof45%.
|     |         |         |       |      |                |     | thetop-3predictionsinthemodel. |     |     |     |     | Takentogether |     |
| --- | ------- | ------- | ----- | ---- | -------------- | --- | ------------------------------ | --- | --- | --- | --- | ------------- | --- |
| The | results | for the | exact | fact | recall samples | in  |                                |     |     |     |     |               |     |
withtheresultsinFigure3b,wehypothesizethat
Figure 4d support conclusion (1). We even mea- notop-3predictionextractiontakesplace,instead
sureastrongerimpactofsubjectattentionconnec- the probability of the final prediction is raised in
tions(80%)andhigherextractionratesinFigure5d
themodelvialatelastpositionMLPlayercompu-
| comparedtopreviousresults. |     |     |     | Wealsomeasurea |     |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tationsbasedonrelationandsubjectinformation.
significantimpactofsubjectattentionconnections Whilethisconclusionpotentiallyisnotsurprising,
| for guesswork |     | samples | (40%), | while | the | generic |     |     |     |     |     |     |     |
| ------------- | --- | ------- | ------ | ----- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
itconfirmsthequalityofthegenericmodelingsce-
| language | modeling |     | samples | show | very little | im- |     |     |     |     |     |     |     |
| -------- | -------- | --- | ------- | ---- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
narioandshowshowitcanbeusedasabaseline
pact of any subject position layers (7%), further fornon-factrecallbehavior.
| supporting | conclusion |     | (1).   | However, | conclusion |       |          |            |          |        |             |     |         |
| ---------- | ---------- | --- | ------ | -------- | ---------- | ----- | -------- | ---------- | -------- | ------ | ----------- | --- | ------- |
|            |            |     |        |          |            |       | For the  | heuristics |          | recall | scenario,   | we  | observe |
| (2) is not | supported  |     | by the | results  | on the     | exact |          |            |          |        |             |     |         |
|            |            |     |        |          |            |       | distinct | patterns   | for both | the    | information |     | flow in |
factrecallsamplesasinformationfromearlynon-
|     |     |     |     |     |     |     | Figure 4c | and | extraction | rates | in  | Figure | 5c. We |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ---------- | ----- | --- | ------ | ------ |
subjectpositionlayersislessimportantforexact
reasonthatasthemodelhasnonotionofthegiven
| factrecall(15%to45%). |           |             | Highimportanceofnon- |     |                  |     |               |           |                |         |          |              |      |
| --------------------- | --------- | ----------- | -------------------- | --- | ---------------- | --- | ------------- | --------- | -------------- | ------- | -------- | ------------ | ---- |
|                       |           |             |                      |     |                  |     | subject,      | little to | no information |         | can      | be extracted |      |
| subject               | positions | information |                      | is  | instead observed |     |               |           |                |         |          |              |      |
|                       |           |             |                      |     |                  |     | from “memory” |           | in the         | subject | position | MLP          | lay- |
fortheguessworksamples(50%)andgenericlan-
ers,thusnoprobabilitydropfromcuttingattention
| guage | modeling | samples |     | (50%). | This indicates |     |            |         |            |     |     |               |     |
| ----- | -------- | ------- | --- | ------ | -------------- | --- | ---------- | ------- | ---------- | --- | --- | ------------- | --- |
|       |          |         |     |        |                |     | to subject | tokens. | Therefore, |     | the | most critical | in- |
thattheconclusionsreachedbyGevaetal.(2023)
formationistransferredforearly-midnon-relation
| largely | are valid, | while | they | seemingly | average |     |                      |     |     |                           |     |     |     |
| ------- | ---------- | ----- | ---- | --------- | ------- | --- | -------------------- | --- | --- | ------------------------- | --- | --- | --- |
|         |            |       |      |           |         |     | positionlayers(20%). |     |     | Seemingly,thefinalpredic- |     |     |     |
acrossguessworkandexactfactrecallscenarios.
|     |     |     |     |     |     |     | tion is extracted |     | from | the MLP | layers | at  | the last |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | ---- | ------- | ------ | --- | -------- |
Whatinferenceprocesstakesplaceforeachpre- tokenposition,leveragingsomepreviousinforma-
diction scenario? For the exact fact recall sce- tionandinformationaboutthelatesttoken. Amore
nario, we have already noted how the inference fine-grainedstudythatseparatestheheuristicsmak-
processheavilyreliesoninformationfromsubject inguptheheuristicsrecallscenarios(promptbias
position layers and less on relation (non-subject) andpersonnamebias)canbefoundinAppendixK.

5 Conclusion
investigatepredictionswithhighorlowprobabil-
|     |     |     |     |     |     |     | itiesfromeachpartition. |     |     | Thisindicatesroomfor |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | -------------------- | --- | --- |
Weidentifyfourpredictionscenariosthatarefunda-
improvementforourmethodofdetectingconfident
| mentallydifferentandofdifferingreliability. |     |     |     |     |     | These |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
predictions,forwhichwealreadyhavenotedalack
| areexactfactrecall, |     |     | heuristicsrecall, |     | guesswork |     |     |     |     |     |     |     |
| ------------------- | --- | --- | ----------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
ofcomprehensivestudiesofmodelconfidencemet-
| and generic | language |     | modeling. |     | We show | that |                                                |     |     |     |     |     |
| ----------- | -------- | --- | --------- | --- | ------- | ---- | ---------------------------------------------- | --- | --- | --- | --- | --- |
|             |          |     |           |     |         |      | rics. Alternatively,thiscouldbeindicatingamore |     |     |     |     |     |
previousinterpretabilityworkforfactcompletion
fundamentalissuewithaqualitativedifferencein
situationstreatmanyoftheseasequivalentbyus-
|     |     |     |     |     |     |     | how models | behave |     | in low | and high probability |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | --- | ------ | -------------------- | --- |
ingaccuracyasthesolecriterionfordifferentiating
cases.
| betweendifferenttypesofinferenceprocesses. |     |     |     |     |     | To  |     |     |     |     |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
facilitatepreciseinterpretationsofLMs,wepresent Ethicalconsiderations
| a method | for creating |     | PRISM | datasets |     | with sam- |                  |     |         |     |                 |       |
| -------- | ------------ | --- | ----- | -------- | --- | --------- | ---------------- | --- | ------- | --- | --------------- | ----- |
|          |              |     |       |          |     |           | Interpretability |     | methods | for | fact completion | situ- |
plesthatrepresenteachofouridentifiedprediction
ationsarenotdirectlyassociatedwithanyethical
| scenarios. | We  | create | PRISM | datasets | for | GPT-2 |           |                                    |     |     |     |     |
| ---------- | --- | ------ | ----- | -------- | --- | ----- | --------- | ---------------------------------- | --- | --- | --- | --- |
|            |     |        |       |          |     |       | concerns. | NeitheristheLAMAdatasetorsynthetic |     |     |     |     |
XL,Llama27BandLlama213B,andusethemto
facttuplesusedinthiswork.
testthesensitivityoftwoinfluentialinterpretability
methods,causaltracingandinformationflowanal- Acknowledgements
| ysis,topredictionscenario. |     |     |     | Wefindthatdifferent |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
predictionscenariosyielddistinctinterpretability AspecialthankstoNicolasAudinetdePieuchon
aswellastheresearchmembersoftheCopeNLU
| resultsifstudiedinisolation. |     |        |            | Takentogether,our |                 |     |           |       |          |          |             |     |
| ---------------------------- | --- | ------ | ---------- | ----------------- | --------------- | --- | --------- | ----- | -------- | -------- | ----------- | --- |
|                              |     |        |            |                   |                 |     | group for | their | valuable | feedback | that helped | us  |
| paper expands                |     | on and | delineates |                   | fact completion |     |           |       |          |          |             |     |
scenarios for which we can interpret LMs. Our shape the paper. We would also like to thank the
resultshighlighttheimportanceofstudyingthese anonymousreviewersfortheirfeedbackandtime.
|     |     |     |     |     |     |     | This work | was | partially | supported | by  | the Wal- |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | --------- | --------- | --- | -------- |
scenariosinisolationandprovidenuancedinsights
with respect to how LMs process information in lenberg AI, Autonomous Systems and Software
factcompletionsituations. Program (WASP) funded by the Knut and Alice
WallenbergFoundation,bytheWallenbergAI,Au-
| Limitations |             |     |                  |     |       |     | tonomous | Systems | and     | Software  | Program | – Hu-  |
| ----------- | ----------- | --- | ---------------- | --- | ----- | --- | -------- | ------- | ------- | --------- | ------- | ------ |
|             |             |     |                  |     |       |     | manities | and     | Society | (WASP-HS) | funded  | by the |
| Similarly   | to previous |     | interpretability |     | work, | our |          |         |         |           |         |        |
MarianneandMarcusWallenbergFoundationand
| results are                   | limited | to  | auto-regressive |                 | models | and |            |     |        |            |             |     |
| ----------------------------- | ------- | --- | --------------- | --------------- | ------ | --- | ---------- | --- | ------ | ---------- | ----------- | --- |
|                               |         |     |                 |                 |        |     | the Marcus | and | Amalia | Wallenberg | Foundation, |     |
| subject-firsttemplatequeries. |         |     |                 | Usingthemethods |        |     |            |     |        |            |             |     |
andbytheSwedishExcellenceCenterforCompu-
describedinthispaper,PRISMdatasetscanbecon-
|          |          |       |     |      |         |          | tational | Social   | Science | (SweCSS) | funded        | by the |
| -------- | -------- | ----- | --- | ---- | ------- | -------- | -------- | -------- | ------- | -------- | ------------- | ------ |
| structed | forother | types | of  | LMs, | such as | encoder- |          |          |         |          |               |        |
|          |          |       |     |      |         |          | Swedish  | Research | Council |          | through grant | agree- |
basedmodels,whileweleavethisforfuturework.
|           |     |            |     |         |      |         | ment no. | 2022-06611.  |     | The      | computations | were     |
| --------- | --- | ---------- | --- | ------- | ---- | ------- | -------- | ------------ | --- | -------- | ------------ | -------- |
| Moreover, | the | heuristics |     | filters | used | for our |          |              |     |          |              |          |
|           |     |            |     |         |      |         | enabled  | by resources |     | provided | by the       | National |
datasetcreationcanonlyrevealthepossibilityof
|     |     |     |     |     |     |     | Academic | Infrastructure |     | for | Supercomputing | in  |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------------- | --- | --- | -------------- | --- |
shallowheuristicsbeingusedbytheLM.Wealso
Sweden(NAISS)atAlvispartiallyfundedbythe
observesomequestionablesamplesthatgounde-
|           |              |     |            |      |     |             | Swedish | Research | Council |     | through grant | agree- |
| --------- | ------------ | --- | ---------- | ---- | --- | ----------- | ------- | -------- | ------- | --- | ------------- | ------ |
| tected by | the filters, |     | indicating | that | the | filters are |         |          |         |     |               |        |
mentno.2022-06725.
leaky. Furthermore,wefindsignsofname-based
| heuristics         | for non-person |          |     | subjects      | for which | we       |     |     |     |     |     |     |
| ------------------ | -------------- | -------- | --- | ------------- | --------- | -------- | --- | --- | --- | --- | --- | --- |
| have no applicable |                | filters. |     | The detection |           | of these |     |     |     |     |     |     |
References
caseswouldrelyonmoreadvanceddetectionmeth-
|     |     |     |     |     |     |     | Victoria | Basmov, | Yoav | Goldberg, | and Reut | Tsarfaty. |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------- | ---- | --------- | -------- | --------- |
odsandisleftforfuturework. Bycomplementing 2024. Llms’readingcomprehensionisaffectedby
our dataset creation with knowledge estimations parametricknowledgeandstruggleswithhypotheti-
and sampling of synthetic fact tuples, we should calstatements. arXivpreprintarXiv:2404.06283.
avoid most filter failures, while we cannot com- EdenBiran,DanielaGottesman,SoheeYang,MorGeva,
pletelyruleoutthepossibilityoftherebeingsome andAmirGloberson.2024. Hoppingtoolate:Explor-
problematicsampleswith PRISM. ingthelimitationsoflargelanguagemodelsonmulti-
|             |     |              |     |           |     |         | hopqueries. |     | InProceedingsofthe2024Conference |     |     |     |
| ----------- | --- | ------------ | --- | --------- | --- | ------- | ----------- | --- | -------------------------------- | --- | --- | --- |
| Even though |     | we partition |     | the PRISM |     | samples |             |     |                                  |     |     |     |
onEmpiricalMethodsinNaturalLanguageProcess-
based on whether the prediction is confident, we ing,pages14113–14130,Miami,Florida,USA.As-
| find that | our results |     | are sensitive |     | to whether | we  |     |     |     |     |     |     |
| --------- | ----------- | --- | ------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
sociationforComputationalLinguistics.

CollinBurns,HaotianYe,DanKlein,andJacobStein- volume36,pages17643–17668.CurranAssociates,
| hardt. 2023.                   | Discovering | latent | knowledge     | in lan- | Inc. |     |     |     |
| ------------------------------ | ----------- | ------ | ------------- | ------- | ---- | --- | --- | --- |
| guagemodelswithoutsupervision. |             |        | InTheEleventh |         |      |     |     |     |
International Conference on Learning Representa- Adi Haviv, Ido Cohen, Jacob Gidron, Roei Schuster,
|     |     |     |     |     | YoavGoldberg,andMorGeva.2023. |     |     | Understand- |
| --- | --- | --- | --- | --- | ----------------------------- | --- | --- | ----------- |
tions.
ingtransformermemorizationrecallthroughidioms.
BoxiCao,HongyuLin,XianpeiHan,LeSun,Lingy- InProceedingsofthe17thConferenceoftheEuro-
ongYan,MengLiao,TongXue,andJinXu.2021. peanChapteroftheAssociationforComputational
Knowledgeableoreducatedguess? Revisitinglan- Linguistics,pages248–264,Dubrovnik,Croatia.As-
guagemodelsasknowledgebases. InProceedings sociationforComputationalLinguistics.
| of the 59th | Annual | Meeting of | the Association | for |     |     |     |     |
| ----------- | ------ | ---------- | --------------- | --- | --- | --- | --- | --- |
ZhengbaoJiang,JunAraki,HaiboDing,andGraham
ComputationalLinguisticsandthe11thInternational
JointConferenceonNaturalLanguageProcessing Neubig. 2021. How can we know when language
(Volume1: LongPapers),pages1860–1874,Online. modelsknow?Onthecalibrationoflanguagemodels
AssociationforComputationalLinguistics. forquestionanswering. TransactionsoftheAssocia-
tionforComputationalLinguistics,9:962–977.
| Yanai Elazar, | Nora | Kassner, Shauli | Ravfogel, | Abhi- |     |     |     |     |
| ------------- | ---- | --------------- | --------- | ----- | --- | --- | --- | --- |
lashaRavichander, EduardHovy, HinrichSchütze, Nikhil Kandpal, Haikang Deng, Adam Roberts, Eric
|                       |     |                       |     |     | Wallace, | and Colin | Raffel. 2023. Large | language |
| --------------------- | --- | --------------------- | --- | --- | -------- | --------- | ------------------- | -------- |
| andYoavGoldberg.2021. |     | Measuringandimproving |     |     |          |           |                     |          |
consistencyinpretrainedlanguagemodels. Transac- models struggle to learn long-tail knowledge. In
tionsoftheAssociationforComputationalLinguis- Proceedings of the 40th International Conference
| tics,9:1012–1031. |     |     |     |     | onMachineLearning, |     | volume202ofProceedings |     |
| ----------------- | --- | --- | --- | --- | ------------------ | --- | ---------------------- | --- |
ofMachineLearningResearch,pages15696–15707.
| Nelson Elhage, | Neel     | Nanda, Catherine | Olsson, | Tom    | PMLR. |     |     |     |
| -------------- | -------- | ---------------- | ------- | ------ | ----- | --- | --- | --- |
| Henighan,      | Nicholas | Joseph, Ben      | Mann,   | Amanda |       |     |     |     |
Askell,YuntaoBai,AnnaChen,TomConerly,etal. Faisal Ladhak, Esin Durmus, Mirac Suzgun, Tianyi
2021. A mathematical framework for transformer Zhang,DanJurafsky,KathleenMcKeown,andTat-
circuits. TransformerCircuitsThread,1:1. sunoriHashimoto.2023. Whendopre-trainingbi-
|     |     |     |     |     | asespropagatetodownstreamtasks? |     |     | Acasestudy |
| --- | --- | --- | --- | --- | ------------------------------- | --- | --- | ---------- |
ShangbinFeng,WeijiaShi,YikeWang,WenxuanDing, in text summarization. In Proceedings of the 17th
Vidhisha Balachandran, and Yulia Tsvetkov. 2024. Conference of the European Chapter of the Asso-
Don‘thallucinate,abstain: IdentifyingLLMknowl- ciationforComputationalLinguistics,pages3206–
edgegapsviamulti-LLMcollaboration. InProceed- 3219,Dubrovnik,Croatia.AssociationforComputa-
| ingsofthe62ndAnnualMeetingoftheAssociation |     |     |     |         | tionalLinguistics. |     |     |     |
| ------------------------------------------ | --- | --- | --- | ------- | ------------------ | --- | --- | --- |
| forComputationalLinguistics(Volume1:       |     |     |     | LongPa- |                    |     |     |     |
pers),pages14664–14690,Bangkok,Thailand.As- GenglinLiu,XingyaoWang,LifanYuan,YangyiChen,
sociationforComputationalLinguistics. andHaoPeng.2023. Prudentsilenceorfoolishbab-
ble? examininglargelanguagemodels’responsesto
Constanza Fierro, Ruchira Dhar, Filippos Stamatiou, theunknown. arXivpreprintarXiv:2311.09731.
| NicolasGarneau,andAndersSøgaard.2024. |     |     |     | Defin- |     |     |     |     |
| ------------------------------------- | --- | --- | --- | ------ | --- | --- | --- | --- |
ing knowledge: Bridging epistemology and large AlexMallen,AkariAsai,VictorZhong,RajarshiDas,
languagemodels. InProceedingsofthe2024Confer- Daniel Khashabi, and Hannaneh Hajishirzi. 2023.
enceonEmpiricalMethodsinNaturalLanguagePro- When not to trust language models: Investigating
cessing,pages16096–16111,Miami,Florida,USA. effectivenessofparametricandnon-parametricmem-
AssociationforComputationalLinguistics. ories. InProceedingsofthe61stAnnualMeetingof
theAssociationforComputationalLinguistics(Vol-
AtticusGeiger,HansonLu,ThomasIcard,andChristo- ume 1: Long Papers), pages 9802–9822, Toronto,
pherPotts.2021. Causalabstractionsofneuralnet- Canada.AssociationforComputationalLinguistics.
| works. | InAdvancesinNeuralInformationProcess- |     |     |     |     |     |     |     |
| ------ | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
ingSystems,volume34,pages9574–9586.Curran R.ThomasMcCoy,ElliePavlick,andTalLinzen.2019.
|     |     |     |     |     | Rightforthewrongreasons: |     | Diagnosingsyntactic |     |
| --- | --- | --- | --- | --- | ------------------------ | --- | ------------------- | --- |
Associates,Inc.
|     |     |     |     |     | heuristicsinnaturallanguageinference. |     |     | InProceed- |
| --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | ---------- |
MorGeva,JasmijnBastings,KatjaFilippova,andAmir ingsofthe57thAnnualMeetingoftheAssociationfor
Globerson.2023. Dissectingrecalloffactualassocia- Computational Linguistics, pages 3428–3448, Flo-
tionsinauto-regressivelanguagemodels. InProceed- rence,Italy.AssociationforComputationalLinguis-
| ingsofthe2023ConferenceonEmpiricalMethodsin |     |     |     |     | tics. |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- |
NaturalLanguageProcessing,pages12216–12235,
Singapore.AssociationforComputationalLinguis- KevinMeng,DavidBau,AlexAndonian,andYonatan
| tics. |     |     |     |     | Belinkov.2022. | Locatingandeditingfactualasso- |     |     |
| ----- | --- | --- | --- | --- | -------------- | ------------------------------ | --- | --- |
|       |     |     |     |     | ciationsingpt. | InAdvancesinNeuralInformation  |     |     |
PeterHase,MohitBansal,BeenKim,andAsmaGhan- ProcessingSystems,volume35,pages17359–17372.
deharioun.2023. Doeslocalizationinformediting? CurranAssociates,Inc.
surprisingdifferencesincausality-basedlocalization
vs. knowledge editing in language models. In Ad- Giovanni Monea, Maxime Peyrard, Martin Josifoski,
vances in Neural Information Processing Systems, Vishrav Chaudhary, Jason Eisner, Emre Kiciman,

HamidPalangi,BarunPatra,andRobertWest.2024. HiyoriYoshikawaandNaoakiOkazaki.2023. Selective-
Aglitchinthematrix? Locatinganddetectinglan- LAMA: Selective prediction for confidence-aware
guagemodelgroundingwithFakepedia. InProceed- evaluationoflanguagemodels. InFindingsoftheAs-
ingsofthe62ndAnnualMeetingoftheAssociation sociationforComputationalLinguistics:EACL2023,
forComputationalLinguistics(Volume1: LongPa- pages2017–2028,Dubrovnik,Croatia.Association
pers),pages6828–6844,Bangkok,Thailand.Associ- forComputationalLinguistics.
ationforComputationalLinguistics.
|     |     |     |     |     |     | Rowan Zellers, | Ari Holtzman, | Yonatan | Bisk, Ali |
| --- | --- | --- | --- | --- | --- | -------------- | ------------- | ------- | --------- |
TimothyNivenandHung-YuKao.2019. Probingneu- Farhadi,andYejinChoi.2019. HellaSwag:Canama-
ralnetworkcomprehensionofnaturallanguageargu- chinereallyfinishyoursentence? InProceedingsof
ments. InProceedingsofthe57thAnnualMeetingof the57thAnnualMeetingoftheAssociationforCom-
putationalLinguistics,pages4791–4800,Florence,
theAssociationforComputationalLinguistics,pages
4658–4664,Florence,Italy.AssociationforCompu- Italy.AssociationforComputationalLinguistics.
tationalLinguistics.
|     |     |     |     |     |     | Yukun Zhao, | Lingyong Yan, | Weiwei Sun, | Guoliang |
| --- | --- | --- | --- | --- | --- | ----------- | ------------- | ----------- | -------- |
Fabio Petroni, Tim Rocktäschel, Sebastian Riedel, Xing, Chong Meng, Shuaiqiang Wang, Zhicong
Patrick Lewis, Anton Bakhtin, Yuxiang Wu, and Cheng,ZhaochunRen,andDaweiYin.2024. Know-
AlexanderMiller.2019. Languagemodelsasknowl- ing what LLMs DO NOT know: A simple yet ef-
|             |     |             |     |          |         | fectiveself-detectionmethod. |     | InProceedingsofthe |     |
| ----------- | --- | ----------- | --- | -------- | ------- | ---------------------------- | --- | ------------------ | --- |
| edge bases? | In  | Proceedings | of  | the 2019 | Confer- |                              |     |                    |     |
enceonEmpiricalMethodsinNaturalLanguagePro- 2024ConferenceoftheNorthAmericanChapterof
cessingandthe9thInternationalJointConference theAssociationforComputationalLinguistics: Hu-
onNaturalLanguageProcessing(EMNLP-IJCNLP), man Language Technologies (Volume 1: Long Pa-
pages2463–2473,HongKong,China.Association pers),pages7051–7063,MexicoCity,Mexico.Asso-
ciationforComputationalLinguistics.
forComputationalLinguistics.
NinaPoerner,UlliWaltinger,andHinrichSchütze.2020.
E-BERT:Efficient-yet-effectiveentityembeddings
| forBERT.             | InFindingsoftheAssociationforCompu- |                         |     |     |     |     |     |     |     |
| -------------------- | ----------------------------------- | ----------------------- | --- | --- | --- | --- | --- | --- | --- |
| tationalLinguistics: |                                     | EMNLP2020,pages803–818, |     |     |     |     |     |     |     |
Online.AssociationforComputationalLinguistics.
GwenythPortilloWightman,AlexandraDelucia,and
| Mark Dredze.     | 2023.      |                            | Strength       | in numbers: | Es-       |     |     |     |     |
| ---------------- | ---------- | -------------------------- | -------------- | ----------- | --------- | --- | --- | --- | --- |
| timating         | confidence | of                         | large language |             | models by |     |     |     |     |
| promptagreement. |            | InProceedingsofthe3rdWork- |                |             |           |     |     |     |     |
shoponTrustworthyNaturalLanguageProcessing
(TrustNLP2023),pages326–362,Toronto,Canada.
AssociationforComputationalLinguistics.
AlecRadford,JeffreyWu,RewonChild,DavidLuan,
| DarioAmodei,IlyaSutskever,etal.2019.    |     |     |     |     | Language |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- |
| modelsareunsupervisedmultitasklearners. |     |     |     |     | OpenAI   |     |     |     |     |
blog,1(8):9.
| Alessandro         | Stolfo,                            | Yonatan                    | Belinkov, | and   | Mrinmaya |     |     |     |     |
| ------------------ | ---------------------------------- | -------------------------- | --------- | ----- | -------- | --- | --- | --- | --- |
| Sachan.2023.       | Amechanisticinterpretationofarith- |                            |           |       |          |     |     |     |     |
| metic reasoning    |                                    | in language                | models    | using | causal   |     |     |     |     |
| mediationanalysis. |                                    | InProceedingsofthe2023Con- |           |       |          |     |     |     |     |
ferenceonEmpiricalMethodsinNaturalLanguage
Processing,pages7035–7052,Singapore.Associa-
tionforComputationalLinguistics.
| Hugo Touvron, | Louis      | Martin, | Kevin   | Stone,  | Peter Al- |     |     |     |     |
| ------------- | ---------- | ------- | ------- | ------- | --------- | --- | --- | --- | --- |
| bert, Amjad   | Almahairi, |         | Yasmine | Babaei, | Nikolay   |     |     |     |     |
Bashlykov,SoumyaBatra,PrajjwalBhargava,Shruti
| Bhosale, | et al.     | 2023. | Llama   | 2: Open | founda-  |     |     |     |     |
| -------- | ---------- | ----- | ------- | ------- | -------- | --- | --- | --- | --- |
| tion and | fine-tuned | chat  | models. | arXiv   | preprint |     |     |     |     |
arXiv:2307.09288.
| Vishal Thanvantri               |     | Vasudevan, | Abhinav             |              | Sethy, and |     |     |     |     |
| ------------------------------- | --- | ---------- | ------------------- | ------------ | ---------- | --- | --- | --- | --- |
| AlirezaRoshanGhias.2019.        |     |            | Towardsbetterconfi- |              |            |     |     |     |     |
| denceestimationforneuralmodels. |     |            |                     | InICASSP2019 |            |     |     |     |     |
-2019IEEEInternationalConferenceonAcoustics,
SpeechandSignalProcessing(ICASSP),pages7335–
7339.

| A Computationalresources |     |     |     | [X],whohasacitizenshipof[Y] |
| ------------------------ | --- | --- | --- | --------------------------- |
P101 [X]worksinthefieldof[Y]
ExperimentsinthisworkaredoneonT4,A40and
[X]specializesin[Y]
| A100NVIDIAGPUs. |     | ModelsusedareGPT-2XL |     |     |
| --------------- | --- | -------------------- | --- | --- |
(1.5B parameters), Llama 2 7B (7B parameters), Theexpertiseof[X]is[Y]
Thedomainofactivityof[X]is[Y]
andLlama213B(13Bparameters).
Thedomainofworkof[X]is[Y]
| B SelectionprocessofLAMArelations |     |     |     | [X]’sareaofworkis[Y] |
| --------------------------------- | --- | --- | --- | -------------------- |
[X]’sdomainofworkis[Y]
| The LAMA | relations | included | in our PRISM |     |
| -------- | --------- | -------- | ------------ | --- |
[X]’sdomainofactivityis[Y]
datasethavebeenselectedbasedonthefollowing
[X]’sexpertiseis[Y]
criteria:
[X]worksintheareaof[Y]
1. Weonlyincluderelationsthathavemultiple P495 [X]wascreatedin[Y]
templatesforwhich1)theobjectcomeslast [X],thatwascreatedin[Y]
inordertofittheautoregressivesettingand2)
[X],createdin[Y]
thesubjectcomesfirstinordertosimplifythe
[X],thatoriginatedin[Y]
| causalreasoningofinterveningonthesubject; |     |     |     | [X]originatedin[Y] |
| ----------------------------------------- | --- | --- | --- | ------------------ |
[X]formedin[Y]
2. Weexcluderelationswithalotofoverlapbe-
[X]wasformedin[Y]
tweenthesubjectandobjectandrelationsfor
[X],thatwasformedin[Y]
whichtheanswersarehighlyimbalancedto-
[X]wasformulatedin[Y]
wardonlyafewalternatives.
[X],formulatedin[Y]
ThiscorrespondstotherelationsP19placeofbirth, [X],thatwasformulatedin[Y]
| place      | of death,           | country | of citizenship, | [X]wasfrom[Y] |
| ---------- | ------------------- | ------- | --------------- | ------------- |
| P20        | P27                 |         |                 |               |
| P101 field | ofwork, P495country |         | oforigin, P740  | [X],from[Y]   |
locationofformationandP1376capitalof. [X],thatwasdevelopedin[Y]
[X]wasdevelopedin[Y]
| C ParaReltemplates |     |     |     | [X],developedin[Y] |
| ------------------ | --- | --- | --- | ------------------ |
We use the templates as described in Table 2 for P740 [X]wasfoundedin[Y]
| thecreationof | PRISM | queries. |     | [X],foundedin[Y] |
| ------------- | ----- | -------- | --- | ---------------- |
[X]thatwasfoundedin[Y]
| Relation | Template |     |     |     |
| -------- | -------- | --- | --- | --- |
[X],thatwasstartedin[Y]
| P19 | [X]wasbornin[Y] |     |     |     |
| --- | --------------- | --- | --- | --- |
[X]startedin[Y]
|     | [X]isoriginallyfrom[Y] |     |     | [X]wasstartedin[Y] |
| --- | ---------------------- | --- | --- | ------------------ |
[X]wasoriginallyfrom[Y]
[X],thatwascreatedin[Y]
[X]originatedfrom[Y]
[X],createdin[Y]
[X]originatesfrom[Y]
[X]wascreatedin[Y]
| P20 | [X]diedin[Y]       |     |     | [X],thatoriginatedin[Y] |
| --- | ------------------ | --- | --- | ----------------------- |
|     | [X]diedat[Y]       |     |     | [X]originatedin[Y]      |
|     | [X]passedawayin[Y] |     |     | [X]formedin[Y]          |
[X]wasformedin[Y]
[X]passedawayat[Y]
|     | [X]expiredat[Y] |     |     | [X],thatwasformedin[Y] |
| --- | --------------- | --- | --- | ---------------------- |
[X]losttheirlifeat[Y]
P1376 [X]isthecapitalof[Y]
[X]’slifeendedin[Y]
[X]isthecapitalcityof[Y]
[X]succumbedat[Y]
[X],thecapitalof[Y]
| P27 | [X]isacitizenof[Y]     |     |     | [X],thecapitalcityof[Y]       |
| --- | ---------------------- | --- | --- | ----------------------------- |
|     | [X],acitizenof[Y]      |     |     | [X],thatisthecapitalof[Y]     |
|     | [X],whoisacitizenof[Y] |     |     | [X],thatisthecapitalcityof[Y] |
[X]holdsacitizenshipof[Y]
[X]hasacitizenshipof[Y] Table2: ParaReltemplatesusedforallLAMArelations
inourdatasetcreation.
[X],whoholdsacitizenshipof[Y]

| D Creationprocessfor |     |     | PRISM |     |     |     |               |                |             |
| -------------------- | --- | --- | ----- | --- | --- | --- | ------------- | -------------- | ----------- |
|                      |     |     |       |     |     | for | each relation | r (e.g. “P740” | location of |
formation):
D.1 Genericlanguagemodelingsamples
Data is sampled from Wikipedia extraction foreachLAMAsubjectsforrelationr (e.g.
| 20220301.enfromHuggingFaceathttps:// |     |     |     |     |     | “SonarKollektiv”): |     |     |     |
| ------------------------------------ | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- |
huggingface.co/datasets/wikipedia.
ifpopularityscorefors>1000thendis-
Thisextractioncontainsaround6.5Mpre-cleaned
cardallexamplesforthesubject(likely
| English | Wikipedia | articles. |     | We perform | the |     |     |     |     |
| ------- | --------- | --------- | --- | ---------- | --- | --- | --- | --- | --- |
tohavebeenmemorized)
followingsteps:
elsecreateemptylistLforthetuplere-
sults
| 1. Select | an entry | (Wikipedia |     | page)       | from the |     |     |     |     |
| --------- | -------- | ---------- | --- | ----------- | -------- | --- | --- | --- | --- |
| data.     | E.g.:    | the page   | for | “John Doyle | (Irish   |     |     |     |     |
foreachParaReltemplatetforrelationr(e.g.
artist)”
“[X]originatedin[Y]”):
| 2. Select | a single | sentence |     | from the | page that |     |     |     |     |
| --------- | -------- | -------- | --- | -------- | --------- | --- | --- | --- | --- |
predictions=top3predictionsfor(s,t)
| begins | with | any part | of the | page | title (i.e. it |     |     |     |     |
| ------ | ---- | -------- | ------ | ---- | -------------- | --- | --- | --- | --- |
(e.g. “SonarKollektivoriginatedin”)
| couldbethesurname, |     |     | ifthesubjectisaper- |     |     |     |     |     |     |
| ------------------ | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- |
son). E.g.: “Doylecontinuedtoexhibitminia- foreachpinpredictions:
turesuntil1835,butbythenhewasexperienc-
|     |     |     |     |     |     |     | if p is trivial | (e.g. “the”) | then discard |
| --- | --- | --- | --- | --- | --- | --- | --------------- | ------------ | ------------ |
inggreatersuccesswithhispoliticalcartoons,
tuple(s,t,p)
printedusingthenewreproductivemediumof
| lithography,beginningin1827.” |     |     |     |     |     |     | elseadd(s,t,p)toL |     |     |
| ----------------------------- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- |
endforeachp
| 3. We | discard  | the sentence |           | if it is: | 1) shorter |     |     |     |     |
| ----- | -------- | ------------ | --------- | --------- | ---------- | --- | --- | --- | --- |
| than  | 5 words, | 2)           | with more | than      | 3 capital- |     |     |     |     |
endforeacht
| ized | words | (likely | to be | section | headings). |     |     |     |     |
| ---- | ----- | ------- | ----- | ------- | ---------- | --- | --- | --- | --- |
E.g.:“Earlylifeandfamily”
ifcount(s,∗,p)inL=1thenadd(s,t,p)to
guessworksample(thatis,ifaparticularan-
| 4. Wecapthesentenceat10words.E.g.: |     |     |     |     | “Doyle |     |     |     |     |
| ---------------------------------- | --- | --- | --- | --- | ------ | --- | --- | --- | --- |
swerpoccurswithinthetop3predictionsfor
continuedtoexhibitminiaturesuntil1835,but
onlyonetemplateitisconsideredguesswork)
by[then]”
endforeachs
5. Wediscardthesentenceifitsnaturalcontinu-
ationbeginswithacapitalornumber(indicat-
endforeachr
ingthiscouldbeanentityandthuspotentially
fact completion). E.g.: “Doyle won a gold WemeasurepopularityscoreproxiedbyWikipedia
| medalin[1805].” |     |     |     |     |     | pageviewsforyear201910following(Mallenetal., |     |     |     |
| --------------- | --- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- |
2023). Welabelapredictionas“likelytobememo-
Werepeatthisuntilwehave1000datapoints(for
rized”ifitcorrespondstoanaveragepageviewrate
| 1000 unique | entries | in  | the data). | For | CT experi- |     |     |     |     |
| ----------- | ------- | --- | ---------- | --- | ---------- | --- | --- | --- | --- |
above1000,asquerieswithlowerpopularityscores
ments,wetracethenexttoken,freelypredictedby
areunlikelytohavebeenmemorized(Mallenetal.,
themodel.
2023).
Wedetermineifapredictionistrivialbyonlyac-
D.2 Guessworksamples
ceptingapredictionasnon-trivialifit’sthecorrect
Togetexamplesofguesswork,wefollowaprocess
|              |       |     |       |           |             | answer | for at least | one data point | in LAMA (for |
| ------------ | ----- | --- | ----- | --------- | ----------- | ------ | ------------ | -------------- | ------------ |
| as described | below | and | apply | it to all | fact tuples |        |              |                |              |
thesamerelation).
fromLAMA9
correspondingtotherelationsP19
| place of | birth, | P20 place | of  | death, P27 | country |     |     |     |     |
| -------- | ------ | --------- | --- | ---------- | ------- | --- | --- | --- | --- |
D.3 Heuristicsrecallsamples
| of citizenship, | P101 | field | of work, | P495 | country |     |     |     |     |
| --------------- | ---- | ----- | -------- | ---- | ------- | --- | --- | --- | --- |
Wecreateheuristicsrecallsamplesfollowingasim-
| of origin, | P740                                | location | of formation |     | and P1376 |                                    |     |     |            |
| ---------- | ----------------------------------- | -------- | ------------ | --- | --------- | ---------------------------------- | --- | --- | ---------- |
|            |                                     |          |              |     |           | ilaralgorithmasforexactfactrecall. |     |     | Ratherthan |
| capitalof  | andthecorrespondingParaReltemplates |          |              |     |           |                                    |     |     |            |
startingfromLAMAsubject-objectdatapointswe
fortheserelations:
produceasetofsynthetic(non-existent)entitiesto
9https://github.com/facebookresearch/
| LAMA |     |     |     |     |     | 10UsingthePageviewAPI. |     |     |     |
| ---- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- |

| populatetheParaReltemplatestosimulateapopu- |     |     |     |     |     |     | endforeacht |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |
larityscoreof0(notpresentintrainingdata)and
ifcount(s,∗,p)inL≥5thenaddall(s,∗,p)
thusensurenomemorization.
|     |     |     |     |     |     |     | tuples | to heuristic | recall | sample | (that | is, if a |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------------ | ------ | ------ | ----- | -------- |
Samplingprocedure particular answer p occurs within the top 3
predictionsforatleast5templatesitisconsid-
Wecreatethesyntheticdatabyfollowingthesteps
| for each | relation | in  | (P19, | P20, | P27, P101, | P495, | eredconfident) |     |     |     |     |     |
| -------- | -------- | --- | ----- | ---- | ---------- | ----- | -------------- | --- | --- | --- | --- | --- |
P740andP1376):
endforeachs
1. Identifysubjecttypedistributionsforthese-
endforeachr
| lectedrelations. |     |     | E.g. | ForrelationsP19,P20, |     |     |     |     |     |     |     |     |
| ---------------- | --- | --- | ---- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Weidentifyifapredictionistrivialbythefollowing
| P27         | and | P101, | based    | on the | “subject | type    |             |                                    |     |     |     |     |
| ----------- | --- | ----- | -------- | ------ | -------- | ------- | ----------- | ---------------------------------- | --- | --- | --- | --- |
|             |     |       |          |        |          |         | setofrules: | Iftheobjecttypeisanamedentity(e.g. |     |     |     |     |
| constraint” |     | from  | Wikidata |        | the only | allowed |             |                                    |     |     |     |     |
subjecttypeisperson. placenames),weallowanygenerationbeginning
|             |     |       |          |     |              |         | withacapitalletter. |           | Thiscoversallrelationsapart |       |          |      |
| ----------- | --- | ----- | -------- | --- | ------------ | ------- | ------------------- | --------- | --------------------------- | ----- | -------- | ---- |
| 2. Generate |     |       | subjects |     | of           | the re- |                     |           |                             |       |          |      |
|             |     |       |          |     |              |         | from P101.          | For P101, | we                          | query | Wikidata | – we |
| quired      |     | types | using    |     | https://www. |         |                     |           |                             |       |          |      |
checkifthereexistany(s,r,o)Wikidataentrywhere
| fantasynamegenerators.com. |     |     |     |     |     | E.g. |     |     |     |     |     |     |
| -------------------------- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
theobjectlabelmatchesthegeneratedtoken.
| For | person | subjects, |     | we generate |     | a mixture |     |     |     |     |     |     |
| --- | ------ | --------- | --- | ----------- | --- | --------- | --- | --- | --- | --- | --- | --- |
Wemeasureifapredictionisbasedonheuristics
| of  | DND | human, | Russian, |     | French, | German, |             |           |           |     |      |           |
| --- | --- | ------ | -------- | --- | ------- | ------- | ----------- | --------- | --------- | --- | ---- | --------- |
|     |     |        |          |     |         |         | by applying | 3 filters | explained | in  | more | detail in |
Korean,andJapanesenames
AppendixD.5.
| 3. Perform |     | de-duplication |     | and | check | against |     |     |     |     |     |     |
| ---------- | --- | -------------- | --- | --- | ----- | ------- | --- | --- | --- | --- | --- | --- |
Wikidatathatnosubjectcorrespondstoareal Distributionofgeneratedsubjecttypes
entity.11
TheWikidatacheckisdoneonala- Toapproximaterealisticdatadistributions,wegen-
bellevel,sincethegeneratednamesarepure
eratesubjectsbasedontheLAMAsubjecttypes.
| strings. |     | Thislimitsourabilitytocheckfora |     |     |     |     |               |      |      |      |       |          |
| -------- | --- | ------------------------------- | --- | --- | --- | --- | ------------- | ---- | ---- | ---- | ----- | -------- |
|          |     |                                 |     |     |     |     | For relations | P19, | P20, | P27, | P101, | only al- |
subject’sexistence,aswecanonlyfindexact lowedsubjectisperson,sowegenerate1000fan-
| matches. |           |           |     |         |     |           | tasy (Dungeons | and          | Dragon  | human)   | names | and     |
| -------- | --------- | --------- | --- | ------- | --- | --------- | -------------- | ------------ | ------- | -------- | ----- | ------- |
|          |           |           |     |         |     |           | 200 of         | each German, | Korean, | Russian, |       | French, |
| For the  | collected | synthetic |     | samples | we  | apply the |                |              |         |          |       |         |
|          |           |           |     |         |     |           | and Japanese   | synthetic    | names.  | For      | P1376 | (cap-   |
followingalgorithm:
|     |     |     |     |     |     |     | ital of), | we generate | 100 | of each | Central | Africa, |
| --- | --- | --- | --- | --- | --- | --- | --------- | ----------- | --- | ------- | ------- | ------- |
“P19”placeofbirth): CentralAmerica,CentralAsia,EastAsia,EastEu-
foreachrelationr(e.g.
rope,MiddleEastern,WestEuropesoundingtown
| foreachsyntheticsubjectsforrelationr(e.g. |     |     |     |     |     |     | names.                                    |     |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- |
| “SerokNuvrome”):                          |     |     |     |     |     |     | RelationP740(locationofformation)hasamix- |     |     |     |     |     |
tureofsubjecttypes(top5categoriesareshownin
createemptylistLforthetupleresults
|     |     |     |     |     |     |     | Table3). | Basedonthis,wegenerate500musical |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------------------------------- | --- | --- | --- | --- |
foreachParaReltemplatetforrelationr(e.g. groupsand500companynames.
“[X]wasbornin[Y]”):
|     |     |     |     |     |     |     |     | type |     | frequency |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --------- | --- | --- |
predictions=top3predictionsfor(s,t)
|     |     |     |     |     |     |     |     | musicalgroup |     | 505 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- |
(e.g. “SerokNuvromewasbornin”)
|     |     |     |     |     |     |     |     | business |     | 105 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- |
foreachpinpredictions:
|     |      |            |       |        |      |         |     | publiccompany |     | 52  |     |     |
| --- | ---- | ---------- | ----- | ------ | ---- | ------- | --- | ------------- | --- | --- | --- | --- |
|     |      |            |       |        |      |         |     | rockband      |     | 29  |     |     |
|     | if p | is trivial | (e.g. | “the”) | then | discard |     |               |     |     |     |     |
|     |      |            |       |        |      |         |     | human         |     | 20  |     |     |
tuple(s,t,p)
|     |     |     |     |     |     |     |     | other |     | 225 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
ifpisbasedonasingletypeofheuristics
thenadd(s,t,p)toL
Table3: Top5categoriesofsubjectsfromLAMAfor
elsediscardtuple(s,t,p) relationP740. Thecategory“other”contains102differ-
ententitytypeswithlessthan15instanceseach.
endforeachp
RelationP495(countryoforigin)hasadiverse
11ThecodeforautomaticallyqueryingWikidataforreal
|     |     |     |     |     |     |     | set of media | and entertainment |     |     | related | subjects |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----------------- | --- | --- | ------- | -------- |
entitiesisprovidedaspartofourcode.

in LAMA (see Table 4). We generate 500 music filter,however,wesuspectalinguisticcorrelation
groups and 100 of each anime and manga, book, between city names and countries may exist and
newspaper,andmagazinenames. thosesurfacelevelsignalscanpotentiallyexplain
someofthepredictions.
type frequency This analysis confirms our concerns related to
thecoverageoftheimplementedheuristicsrecall
|     | television |     |     | 175 |     |     |            |                                        |        |          |         |        |         |
| --- | ---------- | --- | --- | --- | --- | --- | ---------- | -------------------------------------- | ------ | -------- | ------- | ------ | ------- |
|     |            |     |     |     |     |     | filters.   | Evidently,therearesomeheuristicsthatgo |        |          |         |        |         |
|     | magazine   |     |     | 23  |     |     |            |                                        |        |          |         |        |         |
|     |            |     |     |     |     |     | undetected |                                        | by our | filters. | This is | why we | supple- |
|     | music      |     |     | 145 |     |     |            |                                        |        |          |         |        |         |
mentthebiasidentificationfilterswithmemoriza-
|     | film              |     |     | 225 |     |     |       |               |     |        |             |     |       |
| --- | ----------------- | --- | --- | --- | --- | --- | ----- | ------------- | --- | ------ | ----------- | --- | ----- |
|     |                   |     |     |     |     |     | tion: | For heuristic |     | recall | we simulate | no  | memo- |
|     | anime,comic,manga |     |     | 48  |     |     |       |               |     |        |             |     |       |
rizationbyusingsyntheticdataandforexactfact
|     | notfound |     |     | 65  |     |     |        |           |     |              |            |     |        |
| --- | -------- | --- | --- | --- | --- | --- | ------ | --------- | --- | ------------ | ---------- | --- | ------ |
|     |          |     |     |     |     |     | recall | we filter | on  | high subject | popularity |     | (found |
|     | other    |     |     | 228 |     |     |        |           |     |              |            |     |        |
tocorrelatewellwithmemorization(Mallenetal.,
2023)).
Table4: Top5categoriesofsubjectsfromLAMAfor
| relationP495. | Thecategory“other”contains103differ- |     |     |     |     |     |     |                        |     |     |     |     |     |
| ------------- | ------------------------------------ | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- |
|               |                                      |     |     |     |     |     | D.4 | Exactfactrecallsamples |     |     |     |     |     |
ententitytypeswithlessthan13instanceseach.
TogetqueriesforwhichtheLMperformsexactfact
recall,wefollowaprocessasdescribedbelowand
Analysisoftheheuristicsrecallsamplesin applyittoallfacttuplesfromLAMA12correspond-
PRISM
|                |     |        |          |            |     |         | ing to | the relations |     | P19 place | of  | birth, P20 | place |
| -------------- | --- | ------ | -------- | ---------- | --- | ------- | ------ | ------------- | --- | --------- | --- | ---------- | ----- |
| Our heuristics |     | recall | analysis | identifies |     | samples |        |               |     |           |     |            |       |
ofdeath,P27countryofcitizenship,P101fieldof
thatareconfident,butforwhichnobiasisdetected.
work,P495countryoforigin,P740locationoffor-
Thiscanbecounter-intuitive,aswedonotexpect mationandP1376capitalof andthecorresponding
themodeltobeabletomakeconfidentprediction ParaReltemplatesfortheserelations:
| when it | has no | bias | to guide | it. These | examples |     |     |     |     |     |     |     |     |
| ------- | ------ | ---- | -------- | --------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
are excluded from the PRISM samples, but we foreachrelationr(e.g. “P19”placeofbirth):
performadeeperanalysisofthe1,771casesfrom
| GPT-2XL.    |           |          |            |          |              |      | foreachLAMAsubjectsforrelationr |     |     |     |     |     | (e.g. |
| ----------- | --------- | -------- | ---------- | -------- | ------------ | ---- | ------------------------------- | --- | --- | --- | --- | --- | ----- |
| 6 instances |           | identify | the        | location | of formation |      | “ThomasOng”):                   |     |     |     |     |     |       |
| (P740)      | of “Oasis | of       | Prejudice” | as       | “London”     | (not |                                 |     |     |     |     |     |       |
ifpopularityscorefors<1000thendis-
| identified | as  | prompt | bias, | since the | prompt | bias |     |     |     |     |     |     |     |
| ---------- | --- | ------ | ----- | --------- | ------ | ---- | --- | --- | --- | --- | --- | --- | --- |
cardallexamplesforthesubject
| check produces |     | mostly | years, | indicating |     | time to |     |     |     |     |     |     |     |
| -------------- | --- | ------ | ------ | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
elsecreateemptylistLforthetuplere-
bethemorenaturalinterpretationofthequeries).
sults
| 9 instances | from | P101 | (field | of work) | show | the |     |     |     |     |     |     |     |
| ----------- | ---- | ---- | ------ | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
modelpotentiallyignoringpartofthequery,bycon-
foreachParaReltemplatetforrelationr(e.g.
| necting | “Nina | Schopenhauer” |     | with | “philosophy” |     |     |     |     |     |     |     |     |
| ------- | ----- | ------------- | --- | ---- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
“[X]wasbornin[Y]”):
(potentiallyconflatedwiththephilosopherArthur
predictions=top3predictionsfor(s,t)
Schopenhauer)and“RochChagnon”with“anthro-
pology”(potentiallyconflatedwiththeanthropolo- (e.g. “ThomasOngwasbornin”)
| gistNapoleonChagnon). |     |     |     | 23examplesofrelation |     |     |     |     |     |     |     |     |     |
| --------------------- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
foreachpinpredictions:
P495showassociationof5fictionalentitieswith
| Japan (3                                   | of these | contain                       |     | the word      | “Berserk” | – a      |     |              |            |           |            |         |         |
| ------------------------------------------ | -------- | ----------------------------- | --- | ------------- | --------- | -------- | --- | ------------ | ---------- | --------- | ---------- | ------- | ------- |
|                                            |          |                               |     |               |           |          |     | if           | p is based | on        | heuristics | then    | discard |
| possibleconflatingpatternwiththemangaofthe |          |                               |     |               |           |          |     | tuple(s,t,p) |            |           |            |         |         |
| samename).                                 |          | Further790examplescomefromre- |     |               |           |          |     |              | p          |           |            |         |         |
|                                            |          |                               |     |               |           |          |     | if           | is         | incorrect | then       | discard | tuple   |
| lations P19                                | (born    | in)                           | and | P27 (citizen  | of).      | Some     |     | (s,t,p)      |            |           |            |         |         |
| of these                                   | could    | be examples                   |     | of a stronger |           | associa- |     |              |            |           |            |         |         |
elseadd(s,t,p)toL
| tionoverwritingtheexpressedtuple(e.g. |            |          |        |             | “Adolphe       |       |             |     |     |     |     |     |     |
| ------------------------------------- | ---------- | -------- | ------ | ----------- | -------------- | ----- | ----------- | --- | --- | --- | --- | --- | --- |
| Trudeau”                              | associated |          | with   | “Quebec”),  | others         | may   | endforeachp |     |     |     |     |     |     |
| point to                              | weaknesses |          | of our | name        | bias detection |       |             |     |     |     |     |     |     |
| method.                               | Finally,   | the      | most   | represented | relation       | is    | endforeacht |     |     |     |     |     |     |
| P1376 (capital                        |            | of) with | 938    | examples.   | This           | rela- |             |     |     |     |     |     |     |
12https://github.com/facebookresearch/
| tion does | not | lend itself | to  | our subject | name | bias |     |     |     |     |     |     |     |
| --------- | --- | ----------- | --- | ----------- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
LAMA

ifcount(s,∗,p)inL≥5thenaddall(s,∗,p) fordetectingpromptbiasfor“Tokyoisthecapital
tuples to exact fact recall sample (that is, if cityof[Y]”is“Itisthecapitalcityof[Y]”.Ifthe
aparticularanswerpoccurswithinthetop3 toppredictionfortheformerqueryisfoundamong
predictionsforatleast5templatesitisconsid- the top 10 token predictions for the latter query,
| eredconfident) |     |     |     |     | theformerqueryandcorrespondingpredictionis |     |     |
| -------------- | --- | --- | --- | --- | ------------------------------------------ | --- | --- |
markedasbasedonpromptbias.
endforeachs
| endforeachr |     |     |     |     | Relation | Subjectsubstitutions |     |
| ----------- | --- | --- | --- | --- | -------- | -------------------- | --- |
P19 [He,She]
WemeasurepopularityscoreproxiedbyWikipedia
P20 [He,She]
pageviewsforyear201913following(Mallenetal.,
P27 [He,She]
2023).
P101 [He,She]
Wemeasureifapredictionisbasedonheuristics
P495 [It]
| by applying | 3 filters | explained | in more | detail | in  |     |     |
| ----------- | --------- | --------- | ------- | ------ | --- | --- | --- |
P740 [It,Theorganisation]
AppendixD.5.
P1376 [It,Thecity]
Wecategorizethepredictionsinto“correct”or
| “incorrect”usingtheLAMAgoldlabels. |     |     |     | ForLlama |                  |               |                       |
| ---------------------------------- | --- | --- | --- | -------- | ---------------- | ------------- | --------------------- |
|                                    |     |     |     |          | Table 5: Subject | substitutions | used for constructing |
2modelswecategorizeapredictionas“correct”if promptstodetectpromptbias.
ithasmorethan3charactersandfullymatchesthe
| startofthegoldlabel. |     | Thisisnecessarysincethe |     |     |     |     |     |
| -------------------- | --- | ----------------------- | --- | --- | --- | --- | --- |
tokenizersforthesemodelaremorepronetosplit E Examplesfrom PRISM
thegoldlabelsintosmalltokens.
Here, weincludeafewexamplestoillustratethe
D.5 Detectionfiltersforheuristics contentofPRISM fordifferentpredictionscenar-
ios. SeeTables6to10.
Ourdetectionofheuristicsisbasedon3filters.
Lexical overlap
|                                    | Dependence |          | on   | this heuristic |       |     |     |
| ---------------------------------- | ---------- | -------- | ---- | -------------- | ----- | --- | --- |
| is considered                      | plausible  | if there | is a | string         | match |     |     |
| betweenthepredictionandthesubject. |            |          |      | E.g.           | “San  |     |     |
Salcos,thecapitalof[Sal]”
| Namebias | Webasedthisonmodelpredictions |     |     |     |     |     |     |
| -------- | ----------------------------- | --- | --- | --- | --- | --- | --- |
forpromptsexpressingonlyapartoftherequested
| fact. Wequerywiththefollowingprompts: |          |         |      | “[X]is    |       |     |     |
| ------------------------------------- | -------- | ------- | ---- | --------- | ----- | --- | --- |
| acommonnameinthefollowingcity:”       |          |         |      | and“[X]is |       |     |     |
| acommonnameinthefollowingcountry:”.   |          |         |      |           | Where |     |     |
| X is replaced                         | with the | subject | name | to check  | for   |     |     |
bias. Ifanyofthetop10tokenpredictionsforthese
| queries | matches the model | prediction |     | for the | full |     |     |
| ------- | ----------------- | ---------- | --- | ------- | ---- | --- | --- |
factquery,wemarkthat(query,prediction)pairas
| correspondingtopersonnamebias. |     |     | Wecandetect |     |     |     |     |
| ------------------------------ | --- | --- | ----------- | --- | --- | --- | --- |
personnamebiasforrelationsP19,P20,P27,used
| in PRISM | and additionally |     | for P103 | and P1412, |     |     |     |
| -------- | ---------------- | --- | -------- | ---------- | --- | --- | --- |
presentinCounterFact.
| Prompt                                   | bias We use        | the | original    | prompt | tem- |     |     |
| ---------------------------------------- | ------------------ | --- | ----------- | ------ | ---- | --- | --- |
| plates as                                | defined by ParaRel |     | and replace | the    | sub- |     |     |
| jectplaceholderwithgenericsubstitutions. |                    |     |             | Weuse  |      |     |     |
thesubstitutionsdescribedinTable5foreachre-
| lation. | We also remedy | basic | capitalization |     | and |     |     |
| ------- | -------------- | ----- | -------------- | --- | --- | --- | --- |
grammarerrorsthatmightsurfacefromthisauto-
| mated | prompt creation. | An  | example | of a prompt |     |     |     |
| ----- | ---------------- | --- | ------- | ----------- | --- | --- | --- |
13UsingthePageviewAPI.

| Scenario  |     | Prompt                       |     | Prediction | Goldlabel |     | Conf | Pop | Bias |
| --------- | --- | ---------------------------- | --- | ---------- | --------- | --- | ---- | --- | ---- |
| genericLM |     | Naraalsoenjoyedsuccessin     |     | the        | singles   |     | -    | -   | -    |
| genericLM |     | Benjaminlaterjoinedanumberof |     | other      | clubs     |     | -    | -   | -    |
| guesswork |     | SonarKollektivoriginatedin   |     | Russia     | Berlin    |     | 1    | 215 | -    |
guesswork JosephClaywasoriginallyfrom Ohio Philadelphia 1 273 -
| heuristics |     | SerokNuvrome,acitizenof       |     | Ukraine | -   |     | 6   | 0   | name   |
| ---------- | --- | ----------------------------- | --- | ------- | --- | --- | --- | --- | ------ |
| heuristics |     | BaloWindhairhasacitizenshipof |     | Canada  | -   |     | 5   | 0   | prompt |
exactfact ThomasOngisacitizenof Singapore Singapore 7 1418 none
exactfact Shibuya-kei,thatwascreatedin Japan Japan 8 5933 none
Table 6: Samples from PRISM for GPT-2 XL designed to trigger different prediction scenarios. Conf(idence)
measureshowoftenthepredictionwasmade,pop(ularity)measurespageviewrateandbiasindicatesdetectedbias
whenapplicable.
| Model   |     | Query                        |     | Prediction | Subjectpopularity |     |     | Goldlabel |     |
| ------- | --- | ---------------------------- | --- | ---------- | ----------------- | --- | --- | --------- | --- |
| GPT-2XL |     | ThomasOngisacitizenof        |     | Singapore  | 1418              |     |     | Singapore |     |
|         |     | Shibuya-kei,thatwascreatedin |     | Japan      | 5933              |     |     | Japan     |     |
|         |     | Palermoisthecapitalof        |     | Sicily     | 34273             |     |     | Sicily    |     |
Llama27B DiscoBiscuitswascreatedin Philadelphia 3719 Philadelphia
|     |     | DonBroco,thatwasstartedin |     | Bed        | 6984 |     |     | Bedford        |     |
| --- | --- | ------------------------- | --- | ---------- | ---- | --- | --- | -------------- | --- |
|     |     | NikephorosIIIBotaneiates  |     | Constantin | 1859 |     |     | Constantinople |     |
passedawayin
Table7: (query,prediction)exactfactrecallsamplesfromPRISMforGPT-2XLandLlama27B.
|     | Model    |     | Query                             |     | Prediction | Rank | Goldlabel    |     |     |
| --- | -------- | --- | --------------------------------- | --- | ---------- | ---- | ------------ | --- | --- |
|     | GPT-2XL  |     | SonarKollektivoriginatedin        |     | Russia     | 1    | Berlin       |     |     |
|     |          |     | HaydnBendallisoriginallyfrom      |     | England    | 2    | Essex        |     |     |
|     |          |     | JosephClaywasoriginallyfrom       |     | Ohio       | 2    | Philadelphia |     |     |
|     | Llama27B |     | JeanTrembleyoriginatedfrom        |     | France     | 2    | Geneva       |     |     |
|     |          |     | Dansezpentrutine,thatoriginatedin |     | France     | 2    | Romania      |     |     |
|     |          |     | MiltonWrightisoriginallyfrom      |     | Chicago    | 2    | Georgia      |     |     |
Table8: (query,prediction)randomguessworksamplesfromPRISMforGPT-2XLandLlama27B.
|     | Model    |     | Query                                   |     |     | Prediction   |     | Bias    |     |
| --- | -------- | --- | --------------------------------------- | --- | --- | ------------ | --- | ------- | --- |
|     | GPT-2XL  |     | HirashimaHideyoshi,whohasacitizenshipof |     |     | Japan        |     | name    |     |
|     |          |     | BaloWindhairhasacitizenshipof           |     |     | Canada       |     | prompt  |     |
|     |          |     | OlreHellspiritwasoriginallyfrom         |     |     | Hell         |     | lexical |     |
|     | Llama27B |     | HaSongmin,whohasacitizenshipof          |     |     | South(Korea) |     | name    |     |
|     |          |     | WandaHagelholdsacitizenshipof           |     |     | Canada       |     | prompt  |     |
|     |          |     | Limanaga,thecapitalcityof               |     |     | Lim          |     | lexical |     |
Table9: (query,prediction)heuristicsrecallsamplesfromPRISMforGPT-2XLandLlama27B.

| Model | Query | Prediction | Goldlabel |
| ----- | ----- | ---------- | --------- |
GPT-2XL Dexmedetomidineisnotableforitsabilitytoprovidesedation and without
|     | Solomonalsodefendedthenetwork’schoiceofgamesto | air  | broadcast   |
| --- | ---------------------------------------------- | ---- | ----------- |
|     | Walkeraddedanimmenseamountofmaterialtothe      | book | collections |
Llama27B Dexmedetomidineisnotableforitsabilitytoprovidesedation and without
|     | Solomonalsodefendedthenetwork’schoiceofgamesto | air | broadcast |
| --- | ---------------------------------------------- | --- | --------- |
Walkeraddedanimmenseamountofmaterialtothe original collections
Table10: (query,prediction)genericlanguagesamplesfromPRISMforGPT-2XLandLlama27B.

F InspectionofCounterFact
|     |     |     |     |     |     | ple subject | and | object | is found. | Some | examples |     |
| --- | --- | --- | --- | --- | --- | ----------- | --- | ------ | --------- | ---- | -------- | --- |
markedforbiascanbefoundinTable11.
Inthissectionweassesstheapplicabilityofusing
|     |     |     |     |     |     | Using | fact | popularity, | we  | also | evaluate | the |
| --- | --- | --- | --- | --- | --- | ----- | ---- | ----------- | --- | ---- | -------- | --- |
the1,209knownCounterFactsamplesforinterpret-
|     |     |                    |     |             |           | known                  | CounterFact |     | samples | through             | the | lens of |
| --- | --- | ------------------ | --- | ----------- | --------- | ---------------------- | ----------- | --- | ------- | ------------------- | --- | ------- |
| ing | LMs | in fact completion |     | situations. | First, we |                        |             |     |         |                     |     |         |
|     |     |                    |     |             |           | LMknowledgeestimation. |             |     |         | Table12liststhepop- |     |         |
investigatewhatpredictionscenariosarefoundfor
|     |     |     |     |     |     | ularityscoresdistributionforthedataset. |     |     |     |     |     | Wefind |
| --- | --- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- | ------ |
GPT-2XLforthecollectionofthe(query,predic-
|     |     |     |     |     |     | approximately |     | 365 known |     | CounterFact |     | samples |
| --- | --- | --- | --- | --- | --- | ------------- | --- | --------- | --- | ----------- | --- | ------- |
tion)
|     | samples | (Appendix | F.1). | We  | find samples |                                |     |     |     |     |             |     |
| --- | ------- | --------- | ----- | --- | ------------ | ------------------------------ | --- | --- | --- | --- | ----------- | --- |
|     |         |           |       |     |              | withpopularityscoresbelow1000. |     |     |     |     | Theseareun- |     |
inthedatasetlikelytocorrespondtoheuristicsre-
|     |     |     |     |     |     | likely to | have been | memorized |     | by  | the model | and |
| --- | --- | --- | --- | --- | --- | --------- | --------- | --------- | --- | --- | --------- | --- |
call(510samples)asopposedtoexactfactrecall
|      |           |         |     |         |               | are therefore | unlikely |     | to correspond |     | to exact | fact |
| ---- | --------- | ------- | --- | ------- | ------------- | ------------- | -------- | --- | ------------- | --- | -------- | ---- |
| (478 | samples). | Second, | we  | inspect | the total ef- |               |          |     |               |     |          |      |
recall. Moreover,wefindthataround50%ofthese
fectsmeasuredwiththecausaltracingapproachfor
samples(172samples)havebeendetectedbyour
| the | dataset | to find quality | issues | (Appendix | F.2). |     |     |     |     |     |     |     |
| --- | ------- | --------------- | ------ | --------- | ----- | --- | --- | --- | --- | --- | --- | --- |
heuristicsfilters,indicatingthattheremainingsam-
Last,weobserveasetofproblematicsampleswith
plesmayalsocontainsurfacelevelsignalsnotde-
| negated |           | queries in CounterFact |     | (Appendix | F.3).       |                     |     |     |                          |     |     |     |
| ------- | --------- | ---------------------- | --- | --------- | ----------- | ------------------- | --- | --- | ------------------------ | --- | --- | --- |
|         |           |                        |     |           |             | tectedbyourfilters. |     |     | Thissupportsourclaimthat |     |     |     |
| Taken   | together, | our results            |     | show that | the dataset |                     |     |     |                          |     |     |     |
popularitymetadatacanserveasacomplementfor
strugglestosupportpreciseandaccurateinterpre-
separatingexactfactrecallsamplesfromheuristics
| tationsofLMs. |     | OurproposedPRISMdatasetdoes |     |     |     |     |     |     |     |     |     |     |
| ------------- | --- | --------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
recallsamples.
notsufferfromtheaforementionedlimitations.
|     |     |     |     |     |     | Exactfactrecall |     | Atotalof816samplesinCoun- |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------- | --- | ------------------------- | --- | --- | --- | --- |
F.1 Predictionscenarios terFactarefoundtohavepopularityscoresabove
1000,andarethusmorelikelytohavebeenmemo-
WeinspecttheCounterFactdatasetforthreeoffour
predictionscenarios. Thebaselinepredictionsce- rizedbythemodel. Wedetectthepotentialusageof
nariocorrespondingtogenericlanguagemodeling heuristicsfor338ofthesesamples,meaningthat
|     |         |                  |     |                |        | approximately |     | 478 samples |     | in CounterFact |     | may |
| --- | ------- | ---------------- | --- | -------------- | ------ | ------------- | --- | ----------- | --- | -------------- | --- | --- |
| is  | skipped | for the analysis |     | as the dataset | should |               |     |             |     |                |     |     |
not trigger this scenario by virtue of its creation correspondtoexactfactrecall.
process.
F.2 Totaleffects
Randomguesswork Wecannotdetectsamples Apartfromtheanalysisdescribedabove,wealso
| in  | CounterFact | corresponding |     | to random | guess- |     |     |     |     |     |     |     |
| --- | ----------- | ------------- | --- | --------- | ------ | --- | --- | --- | --- | --- | --- | --- |
scrutinizetheknownCounterFactsampleswithre-
workasourimplementationoftheconfidencecri- spect to the total effect of perturbing the subject.
terionisincompatiblewiththedataset. Thedataset We measure the total effect on the probability of
| only | provides | one prompt |     | per fact, | while we re- |                      |     |     |                           |     |     |     |
| ---- | -------- | ---------- | --- | --------- | ------------ | -------------------- | --- | --- | ------------------------- | --- | --- | --- |
|      |          |            |     |           |              | theoutputprediction. |     |     | Thisprovidesanalternative |     |     |     |
quire multiple prompt variations per fact to esti- wayofcheckingforsignsoflackofexactfactre-
mate confidence. This does not mean that there call. The method was introduced by Meng et al.
are no samples in the CounterFact dataset corre- (2022)andusedtofindmodelstatesimportantfor
spondingtorandomguesswork,itonlymeansthat
|     |     |     |     |     |     | themodelprediction. |     |     | Byaddingnoisetotheword |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | ---------------------- | --- | --- | --- |
we are unable to detect them. As a result, some embeddings corresponding to the subject of the
of the samples below identified to correspond to query,thesubjectisperturbed. Theideaisthatthe
| heuristics |     | recall or exact | fact | recall | may actually |              |     |           |       |     |       |       |
| ---------- | --- | --------------- | ---- | ------ | ------------ | ------------ | --- | --------- | ----- | --- | ----- | ----- |
|            |     |                 |      |        |              | perturbation | of  | the query | makes | the | model | inca- |
correspondtorandomguesswork,asweareunable pableofperformingthenecessaryrecalloffactual
toseparatethesesamplesbeforehand. associationsthatresultedintheoriginalprediction,
thusloweringthemodelprobabilityfortheoriginal
| Heuristicsrecall |         | Wecheckforpredictionsbased |         |       |             |             |                                  |     |     |     |     |     |
| ---------------- | ------- | -------------------------- | ------- | ----- | ----------- | ----------- | -------------------------------- | --- | --- | --- | --- | --- |
|                  |         |                            |         |       |             | prediction. | Wehypothesizethatsamplesforwhich |     |     |     |     |     |
| on               | shallow | heuristics                 | for the | known | CounterFact |             |                                  |     |     |     |     |     |
theaddedperturbationdoesnotsufficientlylower
samplesproducedusingGPT-2XL.Wefindatotal
|     |     |     |     |     |     | the corresponding |     | prediction |     | probability |     | are less |
| --- | --- | --- | --- | --- | --- | ----------------- | --- | ---------- | --- | ----------- | --- | -------- |
of510samplesthatmaycorrespondtoheuristics
likelytocorrespondtoexactfactrecall.
recall,ofwhich335samplescorrespondtoprompt
bias, 155 to name bias and 20 to both name and Method ThetotaleffectismeasuredasTE(o) =
prompt bias.14 No lexical overlap between sam- P (o)−P (o),whereP (o)denotesthe
|     |     |     |     |     |     | clean | noised |     |     | clean |     |     |
| --- | --- | --- | --- | --- | --- | ----- | ------ | --- | --- | ----- | --- | --- |
probabilityofemittingtokenoforacleanrunand
14Thereareatotalof205samplescorrespondingtoperson
|                                                |     |     |     |     |     | P (o)                               | denotes | the | probability |     | of emitting | to-    |
| ---------------------------------------------- | --- | --- | --- | --- | --- | ----------------------------------- | ------- | --- | ----------- | --- | ----------- | ------ |
| namesforwhichwecancheckfornamebias,meaningthat |     |     |     |     |     | noised                              |         |     |             |     |             |        |
|                                                |     |     |     |     |     | kenowhenthesubjecthasbeenperturbed. |         |     |             |     |             | Forall |
wedetectnamebiasin92.5%ofallcases.

| Query                               |     |     |     |     | Prediction | Biastype   |     |
| ----------------------------------- | --- | --- | --- | --- | ---------- | ---------- | --- |
| MacApp,aproductcreatedby            |     |     |     |     | Apple      | Prompt     |     |
| GiuseppeAngeli,whohasacitizenshipof |     |     |     |     | Italy      | Personname |     |
TheoriginallanguageofLaFontaine’sFablesisamixtureof French Prompt
Table11: ExamplesofqueriesandpredictionsfromtheknownCounterFactdatasetthatpotentiallycorrespondto
bias. ThepredictionsandanalysishasbeenperformedforGPT-2XL.
Popularityscore #ofsamples creasedtheoriginalprobabilitybylessthan40%.
|         |     |     |     | For some | of these samples | we identify | queries |
| ------- | --- | --- | --- | -------- | ---------------- | ----------- | ------- |
| (0,100] |     | 61  |     |          |                  |             |         |
thatpotentiallyrevealthecorrectpredictioneven
| (100,1000]   |     | 304 |     |                            |     |                   |     |
| ------------ | --- | --- | --- | -------------------------- | --- | ----------------- | --- |
|              |     |     |     | whenthesubjectisperturbed. |     | Twoidentifiedsam- |     |
| (1000,10000] |     | 379 |     |                            |     |                   |     |
plesare“[X]professionallyplaysthesportofice
| (10000,1176235] |     | 437 |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- | --- |
[hockey]”or“[X]’sexpertiseisinthefieldofquan-
|     |     |     |     | tum [physics]”. | Prompt bias | was detected | for all |
| --- | --- | --- | --- | --------------- | ----------- | ------------ | ------- |
Table12: ThepopularityscoresfortheknownCounter-
|              |                                   |     |     | ofthesequeries. | Wemeasureaspearmancorrela- |     |     |
| ------------ | --------------------------------- | --- | --- | --------------- | -------------------------- | --- | --- |
| Factsamples. | Themaximumpopularityscoremeasured |     |     |                 |                            |     |     |
tionof-0.41betweennormalizedTE(Equation(1))
was1,176,235.
andthebinarypromptbiasmetricoverallknown
|     |     |     |     | CounterFactsamples. | Itisclearthattheeffectof |     |     |
| --- | --- | --- | --- | ------------------- | ------------------------ | --- | --- |
ourinvestigations,oisgivenbythepredictioncor-
perturbingthesubjectissmallerwhenthepredic-
respondingtothequerystoredinthedataset. We tionislikelybasedonpromptbias,versuswhenit
| note that negative | total | effects imply | that the per- |     |     |     |     |
| ------------------ | ----- | ------------- | ------------- | --- | --- | --- | --- |
isnot.
turbationofthesubjectincreasedtheprobabilityof
theoriginalpredictionandthatlowpositiveeffects
|     |     |     |     |     | P   | (o)−P | (o) |
| --- | --- | --- | --- | --- | --- | ----- | --- |
potentiallyindicatethatperturbingthesubjecthad TE (o) = clean noised (1)
norm
| asmalleffectonthemodelprediction. |     |     |     |     |     | P (o) |     |
| --------------------------------- | --- | --- | --- | --- | --- | ----- | --- |
clean
| Similarly | to Meng et | al. (2022) | we perturb the |     |     |     |     |
| --------- | ---------- | ---------- | -------------- | --- | --- | --- | --- |
F.3 Negatedqueries
| subjectembeddingswithnoiseϵ |     | ∼   | N(0,ν)where |     |     |     |     |
| --------------------------- | --- | --- | ----------- | --- | --- | --- | --- |
ν issettobe3timeslargerthantheempiricalstan- Weidentifyatotalof8problematicsamplesinthe
darddeviationofallembeddingscorrespondingto dataset that contain the word “not” in the query.
|                          |     |                       |     | Two examples | are “The | language used | by Louis |
| ------------------------ | --- | --------------------- | --- | ------------ | -------- | ------------- | -------- |
| thesubjectsofthedataset. |     | Wemeasuretotaleffects |     |              |          |               |          |
Bonaparteisnotthelanguageofthe[French]”or
fortheknownCounterFactsamplesastheaverage
totaleffectof10runswithperturbedsubjects. “Theexpertiseofmedicalassociationisnotinthe
|     |     |     |     | fieldof[medicine]”. | Thesesamplesareproblem- |     |     |
| --- | --- | --- | --- | ------------------- | ----------------------- | --- | --- |
TEresults Forthe1209knownCounterFactsam- aticastheyaremarkedascorrectsincetheycontain
pleswefind22sampleswithnegativetotaleffects,
thecorrectlabel,whiletheyexpresstheoppositeof
i.e. perturbingthesubjectincreasedtheprediction
|     |     |     |     | thefactrepresentedbythedatasample. |     |     | Thisprob- |
| --- | --- | --- | --- | ---------------------------------- | --- | --- | --------- |
probability,ofwhich18potentiallycorrespondto lem is a consequence of the sampling technique
| promptbiasand2tonamebias. |     | Inspectionofthe |     |     |     |     |     |
| ------------------------- | --- | --------------- | --- | --- | --- | --- | --- |
usedbyMengetal.(2022)inlettingtheLMgen-
samplesmarkedforpromptbiasrevealpromptpat-
erateafluentcontinuationtoagivenquerybefore
terns such as “In [X], the language spoken is a makingthepredictionforthemissingobject. For
mixtureof”wherethecorrespondingpredictionis the majority of the known CounterFact samples
| “English”or“German”. |     | Anotherpatternwedetect |     |     |     |     |     |
| -------------------- | --- | ---------------------- | --- | --- | --- | --- | --- |
thisleadstomorefluentqueriesforwhichtheLM
is“[X]isaffiliatedwiththereligionof”forwhich
mightworkbetter,butforsomesamplesitresults
thepredictionalwaysis“Islam”. Wehypothesize inreversedorrevealingprompts.
| that some | prompts reveal | the correct | prediction |     |     |     |     |
| --------- | -------------- | ----------- | ---------- | --- | --- | --- | --- |
evenwhenthesubjectisoccluded,resultinginneg- G Normalizationeffectsoncausaltracing
| ativeTEvalues. |     |     |     | results |     |     |     |
| -------------- | --- | --- | --- | ------- | --- | --- | --- |
DeeperstudyofTEresults Adeeperstudyof Sincetheseresultsaredependentontheabsolute
theTEvaluesrevealanadditional37samplesfor valuesoftheprobabilityofthetraced(predicted)to-
which the perturbation of the query subject de- ken,wehypothesizethattheresultcouldbedriven

by a few high-probability samples and not repre- H AdditionalresultsfromtheCT
sentativeofthelow-probability15 strataofthedata. sensitivityanalysis
To test this, we take inspiration from work by
This section contains additional results from the
Hase et al. (2023) and compare the IE results to
causaltracinganalysisof PRISM.
their normalized counterpart. We define the nor-
malizedindirecteffectas
H.1 Llama27Band13Bresults
The results in Figures 6 and 7 correspond to the
P (o)−P (o)
h(l),patched noised results in Figure 3 but here for Llama 2 7B and
NIE (o) = i (2)
h( i l) |P clean (o)−P noised (o)| 13BinsteadofGPT-2XL.WefindthattheLlama
resultsessentiallysupportthesameconclusionsas
theresultsforGPT-2XL.
whereP (o)−P (o)isthetotaleffect(TE)
clean noised
defined as the difference between the clean and
H.2 Non-normalizedresults
thenoisedruns. ThenormalizedIEmeasuresthe
percentageofrecoverableprobabilitythatwasre- Toallowforcomparisonswithpreviousworkthat
coveredbypatchingstateh (l) . employed the CT method without normalization
i
wepresentthenon-normalizedCTresultsforthe
For some samples, predominantly low-
combinedsamplesinFigure8.
probability predictions, the division by the TE
may result in unnatural NIE (o) values above
h(l)
H.3 Low-probabilitysplit
i
1 or below -1. The state patching should not be
abletorestoremorethanthecleanrunprobability The results in Figures 3, 6 and 7 correspond to a
andwethereforecaptheNIE (o)toarangeof sampleoftop-rankedpredictionprobabilities. The
h(l)
i results in Figures 9 and 10 correspond to a sam-
[−1,1]. Withthisapproach,eachsampleisvalued
pleofbottom-rankedpredictionprobabilities. We
onthesamescale. Plotsforhomogeneousdatasets
observe qualitative differences between the two
shouldthereforeyieldnormalizedCTresultsthat
figurepairs,wherebottom-rankedprobabilityset
aresimilartotheirnon-normalizedcounterparts.
correspondstolargereffectsforthelasttokenstate.
Are aggregated CT results representative of H.4 Deeperstudyofheuristicsrecall
each studied sample? The non-normalized re-
We analyze the CT results of each of the main
sults for combined samples seen in Figure 8 are
heuristicsrecallcategories,promptbiasandperson
dominated by the exact fact recall samples. The
namebias,inseparationforGPT-2XLandLlama2
exact fact recall samples clearly lead to the deci-
7B.ThecorrespondingresultscanbefoundinFig-
sive role conclusion and the same holds for the
ure11. Theseresultssuggestahigherimportance
non-normalizedresults,eventhoughsubsetsofthe
ofthelasttokenstate,comparedtothelastsubject
includeddata(heuristicsrecallandguessworksam-
tokenstate,forthepromptbiassubsetcomparedto
ples) do not lead to the same conclusion with as
thepersonnamebiassubset. Potentially,itmakes
highcertainty.
sensethatpromptbiasedpredictionsthatshouldbe
For the normalized results we find that equal
lesssensitivetosubjectinformationattributeless
weights for all evaluated samples yield a slightly
importancetostatescorrespondingtothesubject.
differentpatterncomparedtothenon-normalized
results, with a weaker peak for the last subject
I CT-basedclassifierforprediction
token. We conclude that aggregations of CT re-
scenario
sults across multiple prediction scenarios are not
representativeofeachstudiedsample. Also,com- Ourclassifieristrainedon750examplesofeach
parisonsbetweennon-normalizedandnormalized scenario (3000 data points in total) and perfor-
resultsmayrevealnonhomogeneousdatasetswith manceismeasuredonaheldoutsetof1000data
respecttopredictionscenario. points(150ofeachscenario). Wetrainaone-layer
50-neuronneuralnetwork,withAdamoptimizer,
0.0001L2regularization,0.001learningrateanda
15Withprobability,wehererefertotheprobabilitycorre-
spondingtothecleanrunprediction. stoppingtoleranceof1e-4. Allmodelsaretrained

0.5
First subject token
|                | 0.6 |     | 0.6            |     |                |     |     |                       |     |     |     |
| -------------- | --- | --- | -------------- | --- | -------------- | --- | --- | --------------------- | --- | --- | --- |
|                |     |     |                |     | 0.4            |     |     | Middle subject tokens |     |     |     |
| EIA dezilamroN |     |     | EIA dezilamroN |     | EIA dezilamroN |     |     |                       |     |     |     |
Last subject token
|     | 0.4 |     | 0.4 |     | 0.3 |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
First subsequent token
|     |     |     |     |     | 0.2 |     |     | Further tokens |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- | --- |
|     | 0.2 |     | 0.2 |     |     |     |     | Last token     |     |     |     |
0.1
|     | 0.0 |     | 0.0 |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.0
|     | 0 5                                | 10 15 20 | 25 30 0 | 5 10                       | 15 0.1 | 20 25 | 30  |     |     |     |     |
| --- | ---------------------------------- | -------- | ------- | -------------------------- | ------ | ----- | --- | --- | --- | --- | --- |
|     | Layer number in Llama-2-7B         |          |         | Layer number in Llama-2-7B |        |       |     |     |     |     |     |
|     |                                    |          |         |                            |        | 0     | 10  | 20  | 30  | 40  |     |
|     | (a)Genericlanguagemodelingsamples. |          |         | (b)Guessworksamples.       |        |       |     |     |     |     |     |
Layer number in GPT-2-XL
|                | 0.6 |          | 0.6            |      |     |       | 0.6            |     |     |       |       |
| -------------- | --- | -------- | -------------- | ---- | --- | ----- | -------------- | --- | --- | ----- | ----- |
| EIA dezilamroN |     |          | EIA dezilamroN |      |     |       | EIA dezilamroN |     |     |       |       |
|                | 0.4 |          | 0.4            |      |     |       | 0.4            |     |     |       |       |
|                | 0.2 |          | 0.2            |      |     |       | 0.2            |     |     |       |       |
|                | 0.0 |          | 0.0            |      |     |       | 0.0            |     |     |       |       |
|                | 0 5 | 10 15 20 | 25 30 0        | 5 10 | 15  | 20 25 | 30             | 0 5 | 10  | 15 20 | 25 30 |
Layer number in Llama-2-7B Layer number in Llama-2-7B Layer number in Llama-2-7B
(c)Heuristicsrecallsamples. (d)Exactfactrecallsamples. (e)Combinedsamples.
Figure6: CTresultsforPRISMLlama27Bdata. 1000samplesforeachscenarioinisolation. Aswellas1000
combined samples (330 exact fact recall, 340 heuristics recall, 330 guesswork). Shaded regions indicate 95%
confidenceintervals.
| until | converging. | Table 13 shows | overall perfor- |     |     |     | 0   | 1   | 2   | 3   |     |
| ----- | ----------- | -------------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
manceandTables14,15and16showtherespective
|     |     |     |     |     |     |     | 0 218 | 17  | 12  | 3   |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
confusionmatrices.
|     |       |         |          |     |          |                                      | 1 23 | 165 | 30  | 32  |     |
| --- | ----- | ------- | -------- | --- | -------- | ------------------------------------ | ---- | --- | --- | --- | --- |
|     |       |         |          |     |          |                                      | 2 25 | 29  | 161 | 35  |     |
|     |       |         |          |     |          |                                      | 3 1  | 8   | 7   | 234 |     |
|     | Data  |         | Accuracy |     |          |                                      |      |     |     |     |     |
|     |       |         |          |     | Table15: | ConfusionmatrixforperformanceonPRISM |      |     |     |     |     |
|     | PRISM | GPT2-XL | 0.73     |     |          |                                      |      |     |     |     |     |
Llama27B.Rowsindicatetruelabel,columns–predic-
|     | PRISM | Llama27B | 0.78 |     |     |     |     |     |     |     |     |
| --- | ----- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
tions.0=exactfactrecall;1=heuristics;2=guesswork;
|     | PRISM | Llama313B | 0.74 |     |     |     |     |     |     |     |     |
| --- | ----- | --------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
3=genericLM
Table13: Performanceofaneuralnetworkclassifierfor
predictingscenariosbasedonCTresults. J Additionalresultsfromtheattribute
extractionanalysisforguesswork
samples
Additionalattributeextractionrateresultsforguess-
worksamplescanbefoundinFigure12.
|     |     | 0 1 2     | 3   |     |     |                                     |     |     |     |     |     |
| --- | --- | --------- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- | --- |
|     |     |           |     |     | K   | Additionalinformationflowresultsfor |     |     |     |     |     |
|     | 0   | 180 52 15 | 3   |     |     |                                     |     |     |     |     |     |
heuristicsrecallsamples
|     | 1   | 28 184 29 | 9   |     |            |     |             |     |          |           |         |
| --- | --- | --------- | --- | --- | ---------- | --- | ----------- | --- | -------- | --------- | ------- |
|     | 2   | 15 51 138 | 46  |     |            |     |             |     |          |           |         |
|     |     |           |     |     | Additional |     | information |     | flow and | attribute | extrac- |
|     | 3   | 2 11 10   | 227 |     |            |     |             |     |          |           |         |
tionresultsforpromptandpersonnamebiassam-
plesthatmakeouttheheuristicsrecallsamplescan
Table14: ConfusionmatrixforperformanceonPRISM
befoundinFigures13and14.
GPT2-XL.Rowsindicatetruelabel,columns–predic-
|     |     |     |     |     | The | results | reveal | similar |     | extraction | rate and |
| --- | --- | --- | --- | --- | --- | ------- | ------ | ------- | --- | ---------- | -------- |
tions.0=exactfactrecall;1=heuristics;2=guesswork;
|     |     |     |     |     | information |     | flow | results | for both | heuristic | types, |
| --- | --- | --- | --- | --- | ----------- | --- | ---- | ------- | -------- | --------- | ------ |
3=genericLM
whileattentionknockouttosubjectpositionstates
|     |     |     |     |     | clearly | increases |     | the prediction |     | probability | on  |
| --- | --- | --- | --- | --- | ------- | --------- | --- | -------------- | --- | ----------- | --- |

0.5
First subject token
|                | 0.6 |     |     | 0.6            |     |                |     |     |                       |     |     |
| -------------- | --- | --- | --- | -------------- | --- | -------------- | --- | --- | --------------------- | --- | --- |
|                |     |     |     |                |     | 0.4            |     |     | Middle subject tokens |     |     |
| EIA dezilamroN |     |     |     | EIA dezilamroN |     | EIA dezilamroN |     |     |                       |     |     |
Last subject token
|     | 0.4 |     |     | 0.4 |     | 0.3 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
First subsequent token
|     |     |     |     |     |     | 0.2 |     |     | Further tokens |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- |
|     | 0.2 |     |     | 0.2 |     |     |     |     | Last token     |     |     |
0.1
|     | 0.0 |     |     | 0.0 |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.0
|     | 0                                  | 10 20                       | 30  | 40 0 | 10                          | 20 0.1 | 30  | 40  |       |     |     |
| --- | ---------------------------------- | --------------------------- | --- | ---- | --------------------------- | ------ | --- | --- | ----- | --- | --- |
|     |                                    | Layer number in Llama-2-13B |     |      | Layer number in Llama-2-13B |        |     |     |       |     |     |
|     |                                    |                             |     |      |                             |        | 0   | 10  | 20 30 | 40  |     |
|     | (a)Genericlanguagemodelingsamples. |                             |     |      | (b)Guessworksamples.        |        |     |     |       |     |     |
Layer number in GPT-2-XL
|     | 0.6 |     |     | 0.6            |     |     |     | 0.6            |     |     |     |
| --- | --- | --- | --- | -------------- | --- | --- | --- | -------------- | --- | --- | --- |
|     |     |     |     | EIA dezilamroN |     |     |     | EIA dezilamroN |     |     |     |
EIA dezilamroN
|     | 0.4 |       |     | 0.4  |     |     |     | 0.4 |      |       |     |
| --- | --- | ----- | --- | ---- | --- | --- | --- | --- | ---- | ----- | --- |
|     | 0.2 |       |     | 0.2  |     |     |     | 0.2 |      |       |     |
|     | 0.0 |       |     | 0.0  |     |     |     | 0.0 |      |       |     |
|     | 0   | 10 20 | 30  | 40 0 | 10  | 20  | 30  | 40  | 0 10 | 20 30 | 40  |
Layer number in Llama-2-13B Layer number in Llama-2-13B Layer number in Llama-2-13B
(c)Heuristicsrecallsamples. (d)Exactfactrecallsamples. (e)Combinedsamples.
Figure7: CTresultsforPRISMLlama213Bdata. 1000samplesforeachscenarioinisolation. Aswellas1000
combined samples (330 exact fact recall, 340 heuristics recall, 330 guesswork). Shaded regions indicate 95%
confidenceintervals.
|     |     | 0 1      | 2   | 3   |     |     |     |     |     |     |     |
| --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | 0 202 12 | 31  | 5   |     |     |     |     |     |     |     |
|     |     | 1 15 167 | 35  | 33  |     |     |     |     |     |     |     |
|     |     | 2 49 26  | 158 | 17  |     |     |     |     |     |     |     |
|     |     | 3 5 19   | 13  | 213 |     |     |     |     |     |     |     |
Table16: ConfusionmatrixforperformanceonPRISM
Llama213B.Rowsindicatetruelabel,columns–pre-
dictions. 0=exactfactrecall;1=heuristics;2=guess-
work;3=genericLM
| prompt                              | bias | samples and | slightly | decreases | the |     |     |     |     |     |     |
| ----------------------------------- | ---- | ----------- | -------- | --------- | --- | --- | --- | --- | --- | --- | --- |
| probabilityonpersonnamebiassamples. |      |             |          | Thesere-  |     |     |     |     |     |     |     |
sultsmakesense,aspromptbiaspredictionsshould
beindependentfrominformationaboutthesubject,
| while | a deeper | analysis | is necessary | to better | ex- |     |     |     |     |     |     |
| ----- | -------- | -------- | ------------ | --------- | --- | --- | --- | --- | --- | --- | --- |
plainthelowamplitudesmeasuredinFigures4c,
13and14.

0.5
First subject token
|     |     | 0.4 |     | Middle subject tokens |     |     |
| --- | --- | --- | --- | --------------------- | --- | --- |
0.15
|      |     | EIA dezilamroN |     | Last subject token     |     |     |
| ---- | --- | -------------- | --- | ---------------------- | --- | --- |
|      |     | 0.3            |     | First subsequent token |     |     |
| 0.10 |     | 0.2            |     | Further tokens         |     |     |
EIA
Last token
0.1
0.05
0.0
0.1
0.00
|     |       | 0   | 10  | 20 30 | 40  |     |
| --- | ----- | --- | --- | ----- | --- | --- |
| 0   | 10 20 | 30  | 40  |       |     |     |
Layer number in GPT-2-XL
Layer number in GPT-2-XL
(a)GPT-2XL.
0.08
0.20
0.06
0.15
| EIA                        |              |       |     | EIA  |                             |     |
| -------------------------- | ------------ | ----- | --- | ---- | --------------------------- | --- |
| 0.10                       |              |       |     | 0.04 |                             |     |
| 0.05                       |              |       |     | 0.02 |                             |     |
| 0.00                       |              |       |     | 0.00 |                             |     |
| 0 5                        | 10 15        | 20 25 | 30  | 0    | 10 20 30                    | 40  |
| Layer number in Llama-2-7B |              |       |     |      | Layer number in Llama-2-13B |     |
|                            | (b)Llama27B. |       |     |      | (c)Llama213B.               |     |
Figure8: Non-normalizedCTresultsforthecombinedsamplesfromPRISMforeachofourstudiedmodels.

0.5
| 0.020 |     |     |     |                | 0.5 |     |                |     | First subject token    |     |
| ----- | --- | --- | --- | -------------- | --- | --- | -------------- | --- | ---------------------- | --- |
|       |     |     |     |                |     |     |                | 0.4 | Middle subject tokens  |     |
|       |     |     |     |                | 0.4 |     | EIA dezilamroN |     |                        |     |
| 0.015 |     |     |     | EIA dezilamroN |     |     |                |     | Last subject token     |     |
|       |     |     |     |                |     |     |                | 0.3 | First subsequent token |     |
0.3
Further tokens
| EIA 0.010 |     |     |     |     |     |     |     | 0.2 |            |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- |
|           |     |     |     |     | 0.2 |     |     |     | Last token |     |
0.1
| 0.005 |     |     |     |     | 0.1 |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.0
0.0
0.000
|     |     |       |          |     | 0.1 |     |     | 0.1        |     |       |
| --- | --- | ----- | -------- | --- | --- | --- | --- | ---------- | --- | ----- |
|     | 0 5 | 10 15 | 20 25 30 |     | 0   | 10  | 20  | 30 0 40 10 | 20  | 30 40 |
Layer number in GPT-2-XL
|                | Layer number in Llama-2-7B |       |                |                                   |       | Layer number in GPT-2-XL |                |      |     |       |
| -------------- | -------------------------- | ----- | -------------- | --------------------------------- | ----- | ------------------------ | -------------- | ---- | --- | ----- |
|                | (a)1000combinedsamples.    |       |                | (b)Normalized1000combinedsamples. |       |                          |                |      |     |       |
|                | 0.5                        |       | 0.5            |                                   |       |                          |                | 0.5  |     |       |
|                | 0.4                        |       | 0.4            |                                   |       |                          |                | 0.4  |     |       |
| EIA dezilamroN |                            |       | EIA dezilamroN |                                   |       |                          | EIA dezilamroN |      |     |       |
|                | 0.3                        |       | 0.3            |                                   |       |                          |                | 0.3  |     |       |
|                | 0.2                        |       | 0.2            |                                   |       |                          |                | 0.2  |     |       |
|                | 0.1                        |       | 0.1            |                                   |       |                          |                | 0.1  |     |       |
|                | 0.0                        |       | 0.0            |                                   |       |                          |                | 0.0  |     |       |
|                | 0.1                        |       | 0.1            |                                   |       |                          |                | 0.1  |     |       |
|                | 0 10                       | 20 30 | 40             | 0                                 | 10 20 | 30                       | 40             | 0 10 | 20  | 30 40 |
Layer number in GPT-2-XL Layer number in GPT-2-XL Layer number in GPT-2-XL
(c)400exactrecallsamples. (d)400heuristicsrecallsamples. (e)200guessworksamples.
|     | 0.4  |       | 0.4     |     |       |     |     | 0.4  |     |       |
| --- | ---- | ----- | ------- | --- | ----- | --- | --- | ---- | --- | ----- |
|     | 0.3  |       | 0.3     |     |       |     |     | 0.3  |     |       |
| EIA | 0.2  |       | EIA 0.2 |     |       |     | EIA | 0.2  |     |       |
|     | 0.1  |       | 0.1     |     |       |     |     | 0.1  |     |       |
|     | 0.0  |       | 0.0     |     |       |     |     | 0.0  |     |       |
|     | 0 10 | 20 30 | 40      | 0   | 10 20 | 30  | 40  | 0 10 | 20  | 30 40 |
Layer number in GPT-2-XL Layer number in GPT-2-XL Layer number in GPT-2-XL
(f)400exactrecallsamples. (g)400heuristicsrecallsamples. (h)200guessworksamples.
Figure9: CTresultson1000low-probabilitysamplesfromPRISMofwhich330samplescorrespondtoexactfact
recall,340toheuristicsrecalland330toguesswork. ThesearetheresultsforGPT-2XL.

0.5
First subject token
0.020
|     |     |     | 0.6 |     | 0.4 | Middle subject tokens |     |
| --- | --- | --- | --- | --- | --- | --------------------- | --- |
EIA dezilamroN
|       |     |     | EIA dezilamroN |     |     | Last subject token     |     |
| ----- | --- | --- | -------------- | --- | --- | ---------------------- | --- |
| 0.015 |     |     |                |     | 0.3 |                        |     |
|       |     |     | 0.4            |     |     | First subsequent token |     |
| EIA   |     |     |                |     | 0.2 | Further tokens         |     |
| 0.010 |     |     |                |     |     | Last token             |     |
|       |     |     | 0.2            |     | 0.1 |                        |     |
0.005
0.0
0.0
| 0.000 |     |     |     |     | 0.1  |       |     |
| ----- | --- | --- | --- | --- | ---- | ----- | --- |
|       |     |     |     |     | 0 10 | 20 30 | 40  |
0 5 10 15 20 25 30 0 5 10 15 20 25 30 Layer number in GPT-2-XL
| Layer number in Llama-2-7B |          |                | Layer number in Llama-2-7B        |                |     |          |       |
| -------------------------- | -------- | -------------- | --------------------------------- | -------------- | --- | -------- | ----- |
| (a)1000combinedsamples.    |          |                | (b)Normalized1000combinedsamples. |                |     |          |       |
| 0.6                        |          | 0.6            |                                   | 0.6            |     |          |       |
| EIA dezilamroN             |          | EIA dezilamroN |                                   | EIA dezilamroN |     |          |       |
| 0.4                        |          | 0.4            |                                   | 0.4            |     |          |       |
| 0.2                        |          | 0.2            |                                   | 0.2            |     |          |       |
| 0.0                        |          | 0.0            |                                   | 0.0            |     |          |       |
| 0 5                        | 10 15 20 | 25 30 0        | 5 10 15                           | 20 25 30       | 0 5 | 10 15 20 | 25 30 |
Layer number in Llama-2-7B Layer number in Llama-2-7B Layer number in Llama-2-7B
(c)400exactrecallsamples. (d)400heuristicsrecallsamples. (e)200guessworksamples.
| 0.3 |          | 0.3     |         | 0.3      |     |          |       |
| --- | -------- | ------- | ------- | -------- | --- | -------- | ----- |
| 0.2 |          | 0.2     |         | 0.2      |     |          |       |
| EIA |          | EIA     |         | EIA      |     |          |       |
| 0.1 |          | 0.1     |         | 0.1      |     |          |       |
| 0.0 |          | 0.0     |         | 0.0      |     |          |       |
| 0 5 | 10 15 20 | 25 30 0 | 5 10 15 | 20 25 30 | 0 5 | 10 15 20 | 25 30 |
Layer number in Llama-2-7B Layer number in Llama-2-7B Layer number in Llama-2-7B
(f)400exactrecallsamples. (g)400heuristicsrecallsamples. (h)200guessworksamples.
Figure10: CTresultson1000low-probabilitysamplesfromPRISMofwhich330samplescorrespondtoexactfact
recall,340toheuristicsrecalland330toguesswork. ThesearetheresultsforLlama27B.

0.5
First subject token
|     |     |     |                | 0.4 | Middle subject tokens |     |
| --- | --- | --- | -------------- | --- | --------------------- | --- |
|     |     |     | EIA dezilamroN |     | Last subject token    |     |
0.3
First subsequent token
|     |     |     |     | 0.2 | Further tokens |     |
| --- | --- | --- | --- | --- | -------------- | --- |
Last token
0.1
0.5
0.0
0.6
| 0.4            |     |     |                | 0.1                      |       |     |
| -------------- | --- | --- | -------------- | ------------------------ | ----- | --- |
| EIA dezilamroN |     |     | EIA dezilamroN |                          |       |     |
|                |     |     |                | 0 10                     | 20 30 | 40  |
| 0.3            |     |     | 0.4            | Layer number in GPT-2-XL |       |     |
0.2
0.2
0.1
0.0
0.0
0.1
| 0                        | 10 20 30                 | 40  | 0 5                        | 10 15 | 20 25 | 30  |
| ------------------------ | ------------------------ | --- | -------------------------- | ----- | ----- | --- |
|                          | Layer number in GPT-2-XL |     | Layer number in Llama-2-7B |       |       |     |
| (a)PromptbiasforGPT-2XL. |                          |     | (b)PromptbiasforLlama27B.  |       |       |     |
0.5
0.6
0.4
| EIA dezilamroN |     |     | EIA dezilamroN |     |     |     |
| -------------- | --- | --- | -------------- | --- | --- | --- |
0.3
0.4
0.2
| 0.1 |     |     | 0.2 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
0.0
0.0
0.1
| 0                            | 10 20 30                 | 40  | 0 5                           | 10 15 | 20 25 | 30  |
| ---------------------------- | ------------------------ | --- | ----------------------------- | ----- | ----- | --- |
|                              | Layer number in GPT-2-XL |     | Layer number in Llama-2-7B    |       |       |     |
| (c)PersonnamebiasforGPT-2XL. |                          |     | (d)PersonnamebiasforLlama27B. |       |       |     |
Figure11: NormalizedCTresultsforsetsof1000samplesdesignedtoexemplifyeachofthetwomaincategories
oftheheuristicsrecallscenario.
|                 | MHSA     | MLP |                 | MHSA  | MLP |     |
| --------------- | -------- | --- | --------------- | ----- | --- | --- |
| etar noitcartxe |          |     | etar noitcartxe |       |     |     |
| )3 pot(         |          |     | )01 pot(        |       |     |     |
| 0.2             |          |     | 0.2             |       |     |     |
| 0.0             |          |     | 0.0             |       |     |     |
|                 | 0 20     | 40  | 0               | 20    | 40  |     |
|                 | layer    |     |                 | layer |     |     |
|                 | (a)Top-3 |     | (b)Top-10       |       |     |     |
Figure12: AttributeextractionratesacrosslayersmeasuredforPRISMGPT-2XLguessworksamples. MHSA
andMLPindicateattributionextractionrates(topk =3andtopk =10)formulti-headself-attentionstatesand
multilayerperceptronstates,respectively. Shadedregionsindicate95%confidenceintervals.

| subject non-subject | last          | subject non-subject | last |
| ------------------- | ------------- | ------------------- | ---- |
| p ni egnahc %       | p ni egnahc % |                     |      |
| 0                   |               | 0                   |      |
| 50                  |               | 50                  |      |
| 0 20                | 40            | 0 20                | 40   |
layer layer
| (a)Promptbias |     | (b)Personnamebias |     |
| ------------- | --- | ----------------- | --- |
Figure13: Relativechangeinthepredictionprobabilitywheninterveningonattentionedgestothelastposition
forwindowsizesof9layersinGPT-2XLonpromptandpersonnamebiassamples. Shadedregionsindicate95%
confidenceintervals.
| etar noitcartxe | etar noitcartxe |      |     |
| --------------- | --------------- | ---- | --- |
| 0.5             | 0.5             |      |     |
| 0.0             | 0.0             |      |     |
| 0 20            | 40              | 0 20 | 40  |
layer layer
| (a)Promptbias |     | (b)Personnamebias |     |
| ------------- | --- | ----------------- | --- |
Figure14: AttributeextractionratesacrosslayersmeasuredforPRISMGPT-2XLpromptandpersonnamebias
samples. MHSAandMLPindicateattributionextractionrates(topk =1)formulti-headself-attentionstatesand
multilayerperceptronstates,respectively. Shadedregionsindicate95%confidenceintervals.