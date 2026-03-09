Language Agent Tree Search Unifies Reasoning, Acting, and Planning in
|     |     |     |     |     |     | Language | Models |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | ------ | --- | --- | --- |
AndyZhou12 KaiYan1 MichalShlapentokh-Rothman1 HaohanWang1 Yu-XiongWang1
Abstract
|                                         | While                                   | language | models       | (LMs)              | have shown | po-    |     |     |     |     |
| --------------------------------------- | --------------------------------------- | -------- | ------------ | ------------------ | ---------- | ------ | --- | --- | --- | --- |
| 4202 nuJ 6  ]IA.sc[  3v60440.0132:viXra | tential                                 | across   | a range      | of decision-making |            | tasks, |     |     |     |     |
|                                         | their                                   | reliance | on simple    | acting             | processes  | limits |     |     |     |     |
|                                         | theirbroaddeploymentasautonomousagents. |          |              |                    |            | In     |     |     |     |     |
|                                         | this paper,                             |          | we introduce | Language           | Agent      | Tree   |     |     |     |     |
Search(LATS)–thefirstgeneralframeworkthat
synergizesthecapabilitiesofLMsinreasoning,
acting,andplanning.Byleveragingthein-context
|     |     |     |     |     |     |     | Figure1.Overview | of LATS. | Serving | as a unified framework, |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | -------- | ------- | ----------------------- |
learningabilityofLMs,weintegrateMonteCarlo
|     |     |     |     |     |     |     | LATS leverages | an external | environment | and an MCTS-based |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ----------- | ----------- | ----------------- |
TreeSearchintoLATStoenableLMsasagents,
searchalgorithmtoimprovereasoninganddecision-making.
|     | along | with | LM-powered | value | functions | and |     |     |     |     |
| --- | ----- | ---- | ---------- | ----- | --------- | --- | --- | --- | --- | --- |
self-reflectionsforproficientexplorationanden- andJennings,1995)havebeenoflongstandinginterestin
hanceddecision-making. Akeyfeatureofourap- thefieldofartificialintelligence. Whilethishastradition-
allybeenstudiedinreinforcementlearning,therecentrise
proachistheincorporationofanenvironmentfor
externalfeedback,whichoffersamoredeliberate oflanguagemodels(LMs)(Brownetal.,2020;Chowdh-
andadaptiveproblem-solvingmechanismthatsur- eryetal.,2023;Touvronetal.,2023;OpenAI,2023)with
|     |                                           |     |     |     |     |     | strong reasoning | and general | adaptability | offers an alter- |
| --- | ----------------------------------------- | --- | --- | --- | --- | --- | ---------------- | ----------- | ------------ | ---------------- |
|     | passestheconstraintsofexistingtechniques. |     |     |     |     | Our |                  |             |              |                  |
experimentalevaluationacrossdiversedomains, nativeparadigm. NotonlyhaveLMsexcelledinstandard
including programming, interactive question- naturallanguageprocessing(NLP)taskssuchassummariza-
answering(QA),webnavigation,andmath,val- tion(Nallapatietal.,2016)andlanguageinference(Bow-
idatestheeffectivenessandgeneralityofLATS man et al., 2015), but they have also been adapted to an
increasinglydiversesetoftasksthatoftenrequireadvanced
|     | in decision-making |     | while | maintaining |     | compet- |     |     |     |     |
| --- | ------------------ | --- | ----- | ----------- | --- | ------- | --- | --- | --- | --- |
itive or improved reasoning performance. No- common-sensereasoningorquantitativeskills(Cobbeetal.,
tably,LATSachievesstate-of-the-artpass@1ac- 2021;SaparovandHe,2023). Inaddition,LMsarecapable
curacy(92.7%)forprogrammingonHumanEval ofperformingincomplexenvironmentsthatinvolveknowl-
withGPT-4anddemonstratesgradient-freeper- edge and reasoning, such as web navigation (Yao et al.,
2022;Dengetal.,2023),tool-use(Schicketal.,2023),and
formance(averagescoreof75.9)comparableto
gradient-basedfine-tuningforwebnavigationon open-endedgames(Fanetal.,2022).
|     | WebShop | with | GPT-3.5. | Code | can | be found |     |     |     |     |
| --- | ------- | ---- | -------- | ---- | --- | -------- | --- | --- | --- | --- |
Reasoningandactingabilitieshavebeenfurtherimproved
at https://github.com/lapisrocks/
bypromptingtechniquesthataugmentLMswithfeedback
LanguageAgentTreeSearch.
orobservationsfromanexternalenvironment,asexempli-
fiedbyReAct(Yaoetal.,2023b)andotherwork(Gaoetal.,
2023;Shinnetal.,2023).Thiseliminatestheneedtorelyen-
1.Introduction
tirelyonthebaseabilitiesofLMs,enhancingthemthrough
General autonomous agents capable of reasoning and externaltoolsorsemanticfeedback. Despitesuchstrengths,
thesemethodsarereflexiveandfallshortofhumans’deliber-
decision-makinginavarietyofenvironments(Wooldridge
ateandthoughtfuldecision-makingcharacteristicstosolve
1UniversityofIllinoisUrbana-Champaign.2LapisLabs.Corre-
|     |     |     |     |     |     |     | problems(Sloman,1996;Evans,2010). |     |     | Inparticular,they |
| --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | ----------------- |
spondenceto:AndyZhou<andyz3@illinois.edu>. failtoconsidermultiplereasoningpathsortoplanahead.
|     |             |        | 41st          |     |            |            | Recentsearch-guidedLMwork(Xieetal.,2023;Yaoetal., |     |     |     |
| --- | ----------- | ------ | ------------- | --- | ---------- | ---------- | ------------------------------------------------- | --- | --- | --- |
|     | Proceedings | of the | International |     | Conference | on Machine |                                                   |     |     |     |
2023a;Haoetal.,2023)addressesthisissuebysearching
Learning,Vienna,Austria.PMLR235,2024.Copyright2024by
|     |     |     |     |     |     |     | overmultiplereasoningchains. |     | Whileenablingplanning, |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------- | --- | ---------------------- | --- |
theauthor(s).
1

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
| suchmethodsoperateinisolation,lackingtheincorporation |     |     |     |     |     | 2.RelatedWork |     |     |     |     |     |     |     |
| ----------------------------------------------------- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
ofexternalfeedbackthatcanimprovereasoning.
|     |     |     |     |     |     | LMsforreasoning. |     | ForLMs,reasoninginvolvesdecom- |                 |     |              |     |       |
| --- | --- | --- | --- | --- | --- | ---------------- | --- | ------------------------------ | --------------- | --- | ------------ | --- | ----- |
|     |     |     |     |     |     | posing complex   |     | inputs                         | into sequential |     | intermediate |     | steps |
Toovercomethesechallenges,weproposeLanguageAgent
towardsafinalanswer(Cobbeetal.,2021),demonstrated
| Tree Search | (LATS) | – a unified | framework | for | decision- |     |     |     |     |     |     |     |     |
| ----------- | ------ | ----------- | --------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
withchain-of-thought(CoT)prompting(Weietal.,2022)
| makingandreasoningwithlanguagemodels. |     |     |     | Asillustrated |     |     |     |     |     |     |     |     |     |
| ------------------------------------- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
anditsvariants(Weietal.,2022;Kojimaetal.,2022;Wang
inFig.1,LATSsynergizesLMreasoning,acting,andplan-
|     |     |     |     |     |     | etal.,2022). | However,thesemethods,whichcreatechains |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------ | -------------------------------------- | --- | --- | --- | --- | --- | --- |
ningstrategiesbyexpandingReAct(Yaoetal.,2023b)intoa
|     |     |     |     |     |     | autoregressively |     | in a single | step, | often | suffer | from | error |
| --- | --- | --- | --- | --- | --- | ---------------- | --- | ----------- | ----- | ----- | ------ | ---- | ----- |
searchoveracombinatorialspaceofpossiblereasoningand
|              |                                            |     |     |     |     | propagation                                | as  | the number | of  | steps increases |     | (Guo | et al., |
| ------------ | ------------------------------------------ | --- | --- | --- | --- | ------------------------------------------ | --- | ---------- | --- | --------------- | --- | ---- | ------- |
| actingsteps. | Thiseffortisnontrivial–adaptingsearchalgo- |     |     |     |     |                                            |     |            |     |                 |     |      |         |
|              |                                            |     |     |     |     | 2018;Chenetal.,2023b),duetocompounderrors. |     |            |     |                 |     |      | Various |
rithmstolanguageagentsandshiftingfromnon-interactive
advancementsaimtomitigatethisissue;someapproaches,
taskstointeractiveonesrequiresasubstantialnoveldesign
|           |          |            |             |     |             | such as       | self-consistency |         | (Wang   | et al., | 2022), | employ | ma- |
| --------- | -------- | ---------- | ----------- | --- | ----------- | ------------- | ---------------- | ------- | ------- | ------- | ------ | ------ | --- |
| on nodes, | prompts, | and search | algorithms. | In  | particular, |               |                  |         |         |         |        |        |     |
|           |          |            |             |     |             | jority voting | over             | sampled | chains, | while   | others | focus  | on  |
nodesandpromptsmusteffectivelystoreandretrieveex-
|                  |     |                 |           |               |     | multi-step           | decomposition, |     | such                        | as least-to-most |     | prompt- |     |
| ---------------- | --- | --------------- | --------- | ------------- | --- | -------------------- | -------------- | --- | --------------------------- | ---------------- | --- | ------- | --- |
| ternal feedback, |     | with the search | algorithm | incorporating |     |                      |                |     |                             |                  |     |         |     |
|                  |     |                 |           |               |     | ing(Zhouetal.,2022). |                |     | Recently,CoThasbeenimproved |                  |     |         |     |
thisinformationintousefulheuristicsforvalueassignment.
withsearchalgorithms(Yaoetal.,2023a;Haoetal.,2023;
Indeed,ourempiricalevaluation,asdemonstratedonHot-
Bestaetal.,2023)thatcansampletrajectoriesmoreeffec-
PotQA(Yangetal.,2018)inSec.5.1,revealsthatasimple
tively. Tree-of-thought(ToT)prompting(Yaoetal.,2023a)
combinationofexistingmethodsisinadequate,evenfailing
usesDFSorBFS-based(depth/breadth-first)searchguided
tosurpassinternalreasoningperformance,despitehaving
byanLM-generatedheuristic,whilereasoningviaplanning
accesstothegroundtruthanswerfromtheenvironment.
|     |     |     |     |     |     | (RAP) (Hao | et  | al., 2023) | uses | MCTS | with | rollouts | simu- |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ---------- | ---- | ---- | ---- | -------- | ----- |
OurkeyinsightunderpinningLATSisadaptingMonteCarlo lated by LMs. However, they rely solely on LM internal
knowledgeandcannotadapttousefulexternalfeedback.
TreeSearch(MCTS),inspiredbyitssuccessinmodel-based
reinforcementlearning(Silveretal.,2017)andtheobser-
|     |     |     |     |     |     | LMsforacting. |     | Thestrongreasoningandcommon-sense |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------- | --- | --------------------------------- | --- | --- | --- | --- | --- |
vationthatmanyLMtasksallowrevertingtoearliersteps,
|     |     |     |     |     |     | abilities | of LMs | have | been further | adapted |     | for decision- |     |
| --- | --- | --- | --- | --- | --- | --------- | ------ | ---- | ------------ | ------- | --- | ------------- | --- |
tolanguageagents,repurposingpretrainedLMsasagents making or acting tasks as a policy model in interactive
withLM-poweredvaluefunctionsandself-reflectionsfor
|     |     |     |     |     |     | environments. |     | In robotics, | LMs | have | been | employed | as  |
| --- | --- | --- | --- | --- | --- | ------------- | --- | ------------ | --- | ---- | ---- | -------- | --- |
cleverer exploration. Leveraging the general capabilities high-levelcontrollersofcontrolpolicies(Ahnetal.,2022;
| and in-context | learning | abilities | of modern | LMs, | we use |     |     |     |     |     |     |     |     |
| -------------- | -------- | --------- | --------- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
Huangetal.,2022;Driessetal.,2023).Similarwork(Baker
languageasaninterfacebetweeneachcomponent,allowing
etal.,2022;Wangetal.,2023)hasalsoadaptedLMagents
LATStoadaptplanningtoenvironmentalconditionswith- tocomplexmultimodalgamessuchasMinecraft(Gussetal.,
outadditionaltraining.Tothebestofourknowledge,LATS
|           |           |     |     |     |     | 2019;Fanetal.,2022). |     |     | LMsareparticularlyusefulintext- |     |     |     |     |
| --------- | --------- | --- | --- | --- | --- | -------------------- | --- | --- | ------------------------------- | --- | --- | --- | --- |
| the first | framework |     |     |     |     |                      |     |     |                                 |     |     |     |     |
is that incorporates reasoning, acting, basedenvironments(Liuetal.,2018;Shridharetal.,2020;
| andplanningtoenhanceLMperformance. |     |     |     | Notably,LATS |     |     |     |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Liuetal.,2024),whereacting-basedpromptingtechniques
doublestheperformanceofReAct(Yaoetal.,2023b)on
|     |     |     |     |     |     | suchasReAct(Yaoetal.,2023b)haveseensuccess. |     |     |     |     |     |     | Sim- |
| --- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- | ---- |
HotPotQA(Yangetal.,2018)andraisestheaveragescore ilartoCoT,ReActislimitedbyitssimplicityandcannot
by22.1onWebShop(Yaoetal.,2022)withGPT-3.5.When
|           |        |               |     |             |         | effectivelyadapttoenvironmentconditions. |     |     |     |     |     | Manyexten- |     |
| --------- | ------ | ------------- | --- | ----------- | ------- | ---------------------------------------- | --- | --- | --- | --- | --- | ---------- | --- |
| used with | GPT-4, | LATS achieves | a   | 92.7 Pass@1 | rate on |                                          |     |     |     |     |     |            |     |
|           |        |               |     |             |         | sionshavebeenproposedtoaddressthisissue, |     |     |     |     |     | including  |     |
HumanEval(Chenetal.,2021),settingthestateoftheart.
self-refine(Madaanetal.,2023)andReflexion(Shinnetal.,
2023),whichuseself-improvementtoenhancereasoning
Ourcontributionsarethefollowing:1)WeintroduceLATS,
|     |     |     |     |     |     | and decision-making, |     |     | and AdaPlanner |     | (Sun | et al., | 2023), |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | -------------- | --- | ---- | ------- | ------ |
aframeworkbasedonMonteCarloTreeSearchtoconstruct
|     |     |     |     |     |     | which incorporates |     | both | positive | and | negative | feedback. |     |
| --- | --- | --- | --- | --- | --- | ------------------ | --- | ---- | -------- | --- | -------- | --------- | --- |
thebesttrajectoryfromsampledactions,enablingmoreflex-
However,thesemethodsfocusonrefininganindividualtra-
ibleandadaptiveproblem-solvingcomparedwithreflexive
jectoryanddonotconsideralternativechoicesateachstep.
| promptingmethods. |     | 2)Weproposeanovelvaluefunction |     |     |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Inaddition,recentwork(Huangetal.,2024)hassuggested
thatguidesthesearchprocessandincorporatessuccessful
thatLMscannotself-correcttheirinternalreasoning,mak-
| heuristicssuchasself-refinementandself-consistency. |     |     |     |     | 3)  |                                     |     |     |     |     |                      |     |     |
| --------------------------------------------------- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- | -------------------- | --- | --- |
|                                                     |     |     |     |     |     | ingitcriticaltouseexternalfeedback. |     |     |     |     | Alternatively,topure |     |     |
Byintegratingexternalfeedbackandself-reflection,LATS
decision-makingenvironments,thereasoningandpractical
enhancesmodelsensibilityandenablesagentstolearnfrom
abilitiesofLMshavebeenenhancedbyprovidingaccess
| experience, | surpassing | reasoning-based |     | search | methods. |     |     |     |     |     |     |     |     |
| ----------- | ---------- | --------------- | --- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
toexternaltools,suchasAPIs,searchengines,calculators,
Throughexperimentsacrossdiversedomains,includingpro-
|     |     |     |     |     |     | and other | models | (Schick | et al., | 2023; | Shen | et al., | 2023; |
| --- | --- | --- | --- | --- | --- | --------- | ------ | ------- | ------- | ----- | ---- | ------- | ----- |
gramming,interactivequestion-answering(QA),webnavi-
|     |     |     |     |     |     | Sur´ısetal.,2023). |     | WesummarizepriorworkinTab.1. |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------ | --- | ---------------------------- | --- | --- | --- | --- | --- |
gation,andmath,wedemonstratetheversatilityofLATS
forenhancingautonomousreasoninganddecision-making. Tree-based search. Tree-based search, where multiple
2

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
|     | Approach                      |     |     |     | Reasoning | Acting | Planning |     | Self-      | External |     |     |
| --- | ----------------------------- | --- | --- | --- | --------- | ------ | -------- | --- | ---------- | -------- | --- | --- |
|     |                               |     |     |     |           |        |          |     | Reflection | Memory   |     |     |
|     | CoT(Weietal.,2022)            |     |     |     | ✓         | ×      | ×        |     | ×          | ×        |     |     |
|     | ReAct(Yaoetal.,2023b)         |     |     |     | ✓         | ✓      | ×        |     | ×          | ×        |     |     |
|     |                               |     |     |     | ✓         |        | ✓        |     | ✓          | ✓        |     |     |
|     | ToT(Yaoetal.,2023a)           |     |     |     |           | ×      |          |     |            |          |     |     |
|     | RAP(Haoetal.,2023)            |     |     |     | ✓         | ×      | ✓        |     | ×          | ✓        |     |     |
|     |                               |     |     |     | ✓         |        |          |     | ✓          |          |     |     |
|     | Self-Refine(Madaanetal.,2023) |     |     |     |           | ×      | ×        |     |            | ×        |     |     |
|     | BeamSearch(Xieetal.,2023)     |     |     |     | ✓         | ×      | ×        |     | ✓          | ×        |     |     |
|     | Reflexion(Shinnetal.,2023)    |     |     |     | ✓         | ✓      | ×        |     | ✓          | ✓        |     |     |
|     |                               |     |     |     | ✓         | ✓      | ✓        |     | ✓          | ✓        |     |     |
LATS(Ours)
Table1.Summaryofrelatedworkonreasoning,acting,andplanning.LATSisthefirstworkincorporatingdesignsfromallthreedomains,
allowingbroadapplicabilityinallcorrespondingtasks.WerefertoreasoningasLMinternalreasoning,actingasexternaldecision-making,
planningastheuseofasearchalgorithm,self-reflectionastheuseofLM-generatedfeedback,andexternalmemoryasstoringpasttext
contextforfutureupdatesofthesolution.
branchesofoutcomesareexploredduringsearch,iswidely TheLMdecodestextautoregressively, i.e., withoutother
usedinmanyplanningalgorithms(Swiechowskietal.,2021; inputs,theprobabilityforanLMtogenerateasequencey
(cid:81)lx
LaValle, 1998) and reinforcement learning (RL) (Hafner isgivenbyp (x) = p (x[i]|x[1...i−1]). Usually,
|     |     |     |     |     |     |     | θ   |     | i=1 θ |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
etal.,2019;Duetal.,2023;Wuetal.,2023)algorithmsfor toimprovereasoning,promptsareprovidedalongwiththe
itsgoodexploration-exploitationtrade-off.Notethatthough
inputx,whicharespecificinstructionsorfew-shotinput-
tree-basedsearchnecessitatesanenvironmentmodelthat outputexamples. Wedenotethegenericprocesswherean
canexpandfromanarbitrarystate(Vodopivecetal.,2017), inputprompt (x)istransformedintoanoutputybyLM:
IO
oftenrequiringextratraininginRL(Hafneretal.,2023), y ∼p (prompt (x)).
|                                         |     |     |     |     |        | θ                |     | IO    |           |      |         |       |
| --------------------------------------- | --- | --- | --- | --- | ------ | ---------------- | --- | ----- | --------- | ---- | ------- | ----- |
| suchaproblemdoesnotexistformostLMtasks. |     |     |     |     | Thisis |                  |     |       |           |      |         |       |
|                                         |     |     |     |     |        | Chain-of-thought |     | (CoT) | prompting | (Wei | et al., | 2022) |
becausewecanconvenientlyreverttoanystatebysetting
caterstoscenarioswherethedirectmappingfromxtoyis
theinputtobethecontextandthecorrespondingprevious
intricate,e.g.,whenxisfromamathematicalqueryorchal-
outputfromtheLMformanytasks.Thus,weoperateonthe
|     |     |     |     |     |     | lengingquestion. |     | Ithingesoncreatingthoughtsz |     |     | 1 ,...,z | l   |
| --- | --- | --- | --- | --- | --- | ---------------- | --- | --------------------------- | --- | --- | -------- | --- |
tree-basedframeworkanduseMCTS(Swiechowskietal.,
thatactassteppingstonesbetweenxandy;eachthoughtz
| 2021)tofullyunlockthepotentialofLMs. |     |     |     | Inaddition,we |     |     |     |     |     |     |     | i   |
| ------------------------------------ | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
isalanguagesequence.ToemployCoTprompting,thoughts
| avoid the | cost of training |     | a value function | over | language |     |     |     |     |     |     |     |
| --------- | ---------------- | --- | ---------------- | ---- | -------- | --- | --- | --- | --- | --- | --- | --- |
pCoT(x,z
|     |     |     |     |     |     | are extracted | sequentially |     | as z ∼ |     | ),  | with |
| --- | --- | --- | --- | --- | --- | ------------- | ------------ | --- | ------ | --- | --- | ---- |
descriptionsbyleveragingthein-contextlearning(Brown i θ 1···i−1
|                            |     |     |                          |     |     | thefinaloutputbeingy |     |     | ∼pCoT(x,z | ).    |     |     |
| -------------------------- | --- | --- | ------------------------ | --- | --- | -------------------- | --- | --- | --------- | ----- | --- | --- |
| etal.,2020)abilitiesofLMs. |     |     | Concurrentwork(Liuetal., |     |     |                      |     |     | θ         | 1···l |     |     |
2023)alsoexplorescombiningsearchalgorithmswithLM Tree-of-thought(ToT)prompting(Yaoetal.,2023a)ex-
agents but uses an off-the-shelf search algorithm, which tendsCoTpromptingbyexploringmultiplereasoningpaths
| maynotbeoptimalforLMs. |     |     | Finally,followingYaoetal. |     |     |               |     |                                     |     |     |     |     |
| ---------------------- | --- | --- | ------------------------- | --- | --- | ------------- | --- | ----------------------------------- | --- | --- | --- | --- |
|                        |     |     |                           |     |     | overthoughts. |     | Itframesproblemsasasearchoveratree, |     |     |     |     |
(2023a)andHaoetal.(2023),wenotethatweuseplanning whereeachnodes = [x,z ]representsapartialsolution
1·i
andsearchalgorithmsinterchangeablyinthispaper. state comprising the original input x and the thought se-
|     |     |     |     |     |     | quence | z 1···i . | Thoughts | z i are generated | by  | proposal | or  |
| --- | --- | --- | --- | --- | --- | ------ | --------- | -------- | ----------------- | --- | -------- | --- |
3.Preliminaries sampling with CoT z ∼ pC oT(x,z ). Search algo-
|     |     |     |     |     |     |     |     |     | i θ | 1···i−1 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- |
rithmslikedepth-first(DFS)orbreadth-first(BFS)search
3.1.ProblemSettingandPrompting areusedtosystematicallyexplorethetree,guidedbyheuris-
ticsbasedonLMevaluationsV(s)ofeachstate.
Wefirstdefineourproblemandoutlineafewestablished
methods that leverage language models for reasoning or ReAct (Yao et al., 2023b) extends language models to
decision-making. In LM reasoning or decision making, tasks where the mapping from x to y is enhanced by or
we are given an input x in natural language and a pre- requires interactions with an external environment, such
trainedlanguagemodelp (x)parameterizedbyθ;ourgoal as a game or API. This technique constructs an action
θ
is to generate a final output y ∼ p (x) that corresponds space Aˆ = A∪Z that adds permissible actions a ∈ A
θ
totheanswer(reasoning)orcompletesthetask(decision- to the reasoning traces z ∈ Z from CoT. Observations o
making). Bothxandyarelanguagesequences,whichare fromtheenvironmentareusedtoimprovebothreasoning
comprisedofalistoftokens(thebasicelementsofnatural andacting. TosolveproblemswithReAct,aftereachob-
language, often words), denoted as x = (x[1],...,x[l ]) servation, actions are generated from p sequentially as
|     |     |     |     |     | x   |     |     |     |     | θ   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
and y = (y[1],...,y[l ]) where l and l are the length. a ∼ pReAct(x,o ,a ),withthefinaloutputbe-
|     |     | y   | x   | y   |     | i θ |     | 1···i−1 | 1···i−1 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------- | --- | --- | --- |
3

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
ing y ∼ pReAct(x,o ,a ). In this paper, consistent anystepbysimplycopy-pastinghistoricaltextinput. Such
|     | θ 1···l | 1···l |     |     |     |     |     |
| --- | ------- | ----- | --- | --- | --- | --- | --- |
withotherLMagentmethodssuchasReActandReflexion aspecialpropertyisthekeymotivationofourwork.
| (Shinn et | al., 2023), we | focus on decision-making | tasks |     |     |     |     |
| --------- | -------------- | ------------------------ | ----- | --- | --- | --- | --- |
whererevertingbetweeniterationsisfeasible.
4.UnifyingReasoning,Acting,andPlanning
Whilethepreviouslydescribedpromptingtechniquesim-
4.1.LMAgent
proveLMperformanceonreasoningtasks,theyfalteron
| difficult tasks | that involve | multifaceted | decision-making |     |     |     |     |
| --------------- | ------------ | ------------ | --------------- | --- | --- | --- | --- |
Dependingonthebasepromptingframeworkdesign,LATS
duetoseveralshortcomings: 1)Flexibility: Baseprompting supportssequentialreasoningordecision-makingtasks. At
designs(CoTorReAct)autoregressivelysamplefromthe timestept,anagentreceivesanobservationo ∈Ofrom
t
LM,neglectingpotentialalternativecontinuationsfromspe- theenvironmentandtakesanactiona t ∈Afollowingsome
cificstates. 2)Sensibility: Reasoning-basedmethods(CoT, policy π(a |x,o ,a ). We initialize the agent
t 1···t−1 1···t−1
| RAP (Hao | et al., 2023), | or ToT) rely | solely on the inter- | withp |     |     |     |
| -------- | -------------- | ------------ | -------------------- | ----- | --- | --- | --- |
θ toleveragetheusefullanguagerepresentationsof
nalrepresentationsoftheLMandcannotconsiderexternal anLMasabasedecision-maker. WefollowtheReActin-
observations. Thisdependencyrisksfacthallucinationand stantiation,inwhichtheactionspaceAˆ=A∪Z consists
errorpropagationwhilesettingaperformanceceiling. 3) ofboththespaceofpermissibleactionsAandthelanguage
Adaptability: Currentplanningstrategies(RAPorToT)use spaceofreasoningtracesZ. Actionsdirectlyaffecttheenvi-
simplesearchalgorithmssuchasBFSorcannotleverage ronmentandresultinobservation,whilethoughtsareused
environmentalfeedbacktoimproveplanning. Additionally, toformalizedecisionsbyorganizinginformation,planning
theagentisstaticandcannotreusepreviousexperienceor futureactions,orinjectinginternalknowledge. Theexact
| learnfromtrialanderror. |     | WhileRAPalsoadoptsMCTS,it |     |     |     |     |     |
| ----------------------- | --- | ------------------------- | --- | --- | --- | --- | --- |
instantiationoftheactionspacedependsontheparticular
isconstrainedtotaskswheretheLMcanbecomeaworld environment–fordecision-makingtasksactionsmightcon-
model and accurately predict states. These shortcomings sistofcommandsonawebsite,whileforreasoningtasks
limittheabilityofLMstobedeployedasgeneralproblem- theactionspacemightbelimitedtoafewexternaltoolsor
solvingagentsandformthemotivationforLATS. APIs. Inenvironmentswithoutfeedback,suchasreasoning
tasks,weuseCoTasthebasepromptingframework.
3.2.MonteCarloTreeSearch(MCTS)
Insteadofgreedilydecodingonetrajectoryorsolution,we
MonteCarloTreeSearch(MCTS)isaheuristicsearchal- sample n actions from p θ using the current state. This is
gorithmthatisprovedsuccessfulonmanydecision-making based on the intuition that for complex decision-making
tasks,thereislikelytobearangeofpotentialtrajectoriesor
environments,suchasAtari(Yeetal.,2021)andGo(Silver
etal.,2016). MCTSbuildsadecisiontreewhereeverynode reasoningpathsthatarecorrect(Evans,2010). Samplinga
inthetreeisastateandedgeisanaction. MCTSrunsfork diversesetofcandidatesateachstepmitigatesthestochastic
episodes;foreachepisode,itstartsfromtheroot(i.e.,initial natureofLMtextgenerationandenablesgreaterexploration
state)anditerativelyconductstwostepstoexpandthetree: inboththedecision-makingandreasoningspace. Wewrap
1)Expansion,wheremultiplechildrenstatessareexplored p within our proposed search algorithm to deliberately
θ
fromthecurrentparentstatepbysamplingnactions,and2) constructthebesttrajectoryfromsampledactions.
Selection,wherethechildrenwiththehighestUCT(Upper
| ConfidenceboundsappliedtoTrees)(KocsisandSzepesva´ri, |     |     |     | 4.2.LATS |     |     |     |
| ----------------------------------------------------- | --- | --- | --- | -------- | --- | --- | --- |
2006)valueisselectedforexpansionbythenextiteration.
|     |     |     |     | The main component | of LATS | is a search algorithm | that |
| --- | --- | --- | --- | ------------------ | ------- | --------------------- | ---- |
TheUCTofachildstatesiscalculatedasfollows:
|     |     |     |     | controlstheproblem-solvingprocesswithplanning. |     |     | Tofind |
| --- | --- | --- | --- | ---------------------------------------------- | --- | --- | ------ |
(cid:115)
|     |               |     | lnN(p) | themostpromisingtrajectoryandsystemicallybalanceex- |     |     |     |
| --- | ------------- | --- | ------ | --------------------------------------------------- | --- | --- | --- |
|     | UCT(s)=V(s)+w |     | , (1)  |                                                     |     |     |     |
N(s)
plorationwithexploitation,weadoptavariantofMCTSthat
whereN(s)isthenumberofvisitstoanodes,V(s)isthe framesdecision-makingasatreesearch,inwhicheachnode
|                                                    |     |     |     | s=[x,a ,o   | ]representsastatecomprisingtheorigi- |     |     |
| -------------------------------------------------- | --- | --- | --- | ----------- | ------------------------------------ | --- | --- |
| valuefunction(expectedreturn)fromthesubtreeofs,wis |     |     |     | 1···i 1···i |                                      |     |     |
theexplorationweight,andpistheparentnodeofs. When nalinputx,actionsequencea ,andobservationsequence
1·i
o ,whereiisatokeninthetextsequence.
| theendofanepisodeisreached,abackpropagationiscar- |     |     |     | 1·i |     |     |     |
| ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
riedout: thereturnrisusedforupdatingeveryV(s)along
OurmaintechnicalcontributionisadaptingMCTStolan-
Vold(s)(N(s)−1)+r,where
thepathwiththeformulaV(s)= guageagents. LATSrepurposesp asanagent,stateevalua-
|                             |     |                         | N(s) |                                                      |     | θ   |     |
| --------------------------- | --- | ----------------------- | ---- | ---------------------------------------------------- | --- | --- | --- |
| V (s)istheoldvaluefunction. |     | Normally,themajorshort- |      |                                                      |     |     |     |
| old                         |     |                         |      | tor,andfeedbackgenerator,leveragingtheusefullanguage |     |     |     |
comingofMCTSisthatitrequiresanenvironmentmodelto representationsofmodernLMstofacilitateplanning.While
undopreviousstepsandformasearchingtree,whichcould standardMCTSandRAP(Haoetal.,2023)relyoninternal
beastrongassumption. However,thislimitationdoesnot dynamicsmodelstofacilitatesimulation,LATSusesenvi-
existformanyLMtasks, aswecanconvenientlyresetto ronmentinteractionanddoesnotrequireaworldmodel. As
4

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
Figure2.OverviewofthesixoperationsinLATS.Anodeisselected,expanded,evaluated,thensimulateduntilaterminalnodeisreached,
andthentheresultingvalueisbackpropagated.Ifthetrajectoryfails,areflectionisgeneratedandusedasadditionalcontextforfuture
trials.Theseoperationsareperformedinsuccessionuntilthebudgetisreachedorthetaskissuccessful.
depictedinFig.2,LATSconsistsofaseriesofoperations as it is difficult for LMs to improve their responses with-
–selection,expansion,evaluation,simulation,backpropa- out external feedback (Huang et al., 2024). Additionally,
gation,andreflection–performedinsuccessionuntilthe tofurtherimprovevalueassignment, weintroduceanad-
taskissuccessfullycompletedoracomputationallimitis ditional heuristic based on self-consistency (Wang et al.,
reachedaftersamplingktrajectories. Thefullpseudocode 2022),inwhichactionssampledmultipletimesatthesame
ofLATScanbefoundinSec.AintheAppendix. statetendtobemoreaccurate. Thisresultsintheoverall
valuefunction:
| Selection. | In the first operation, | the algorithm | identifies |     |                           |     |     |     |
| ---------- | ----------------------- | ------------- | ---------- | --- | ------------------------- | --- | --- | --- |
|            |                         |               |            |     | V(s)=λ∗LM(s)+(1−λ)∗SC(s), |     |     | (2) |
asegmentofthecurrenttreemostsuitableforsubsequent
expansion.Startingfromtherootnode,denotedastheinitial whereλisahyperparameter. Notably,ourmethodoffers
states ,achildnodeisselectedateachtreeleveluntilaleaf enhancedflexibilityoverprogrammedheuristics(Campbell
0
nodeisreached. Tobalanceexplorationandexploitation, etal.,2002)andgreaterefficiencythanlearnedheuristics
| weusetheUCTalgorithmasshowninEq.1. |     |     |     | (Silveretal.,2017). |     |     |     |     |
| ---------------------------------- | --- | --- | --- | ------------------- | --- | --- | --- | --- |
Expansion. Afterselectinganode, thesecondoperation Simulation. Thefourthoperationexpandsthecurrentlyse-
expandsthetreebysamplingnactionsfromp ,asdescribed lectednodeuntilaterminalstateisreached. Ateachdepth
θ
inthepriorsection. Theenvironmentreceiveseachaction level,wesampleandevaluatenodeswiththesameopera-
|                                                 |     |     |      | tionsbutprioritizenodesofthehighestvalue. |     |     | Reachinga |     |
| ----------------------------------------------- | --- | --- | ---- | ----------------------------------------- | --- | --- | --------- | --- |
| andreturnscorrespondingfeedbackasanobservation. |     |     | This |                                           |     |     |           |     |
resultsinnnewchildnodesaddedtothetree. Thistreeis terminalstateprovidesobjectivefeedbackonthecorrect-
storedinanexternallong-termmemorystructure. nessofatrajectory. Ifthetaskiscompletedsuccessfully,
|             |                                        |     |     | thenLATSterminatesthesearch. |     | Ifthesolutionispartially |     |     |
| ----------- | -------------------------------------- | --- | --- | ---------------------------- | --- | ------------------------ | --- | --- |
| Evaluation. | Thethirdoperationassignsascalarvalueto |     |     |                              |     |                          |     |     |
successfulorunsuccessful,thenweperformtwoadditional
each new child node for selection and backpropagation. operationsasdescribedbelow. Thesuccessofatrajectoryis
Thisvalueeffectivelyquantifiestheagent’sprogressintask
determinedbythedesignofthespecificenvironment,such
completion,servingasaheuristictosteerthesearchalgo-
asfinalizingapurchaseinwebnavigationenvironments.
| rithmtowardsthemostpromisingregionsofthetree. |     |     | As  |     |     |     |     |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
LATSdoesnotinvolvetraining,weproposeanovelvalue Backpropagation. Thisoperationupdatesthevaluesofthe
|                                                    |                        |                    |       | tree based                              | on the outcome    | of a trajectory. | For each       | node |
| -------------------------------------------------- | ---------------------- | ------------------ | ----- | --------------------------------------- | ----------------- | ---------------- | -------------- | ---- |
| function                                           | for this setting based | on two components: | (1) a |                                         |                   |                  |                |      |
|                                                    |                        |                    |       | s ,s ,...,s                             | in the trajectory | from root        | (initial state | s )  |
| self-generatedLMscoreand(2)aself-consistencyscore. |                        |                    |       | 0 1                                     | l                 |                  |                | 0    |
|                                                    |                        |                    |       | ofthesearchingtreetoleaf(terminalstates |                   |                  | ),itsvalueis   |      |
l
InspiredbyToT,werepurposep θ intoavaluefunctionby updatedtoreflecttheoutcomeofthesimulationbyN(s )=
i
promptingittoreasonaboutagivenstate. Toobtainascalar V(si−1)N(si−1)+r,whereristhe
|     |     |     |     | N(s )+1andV(s | )=  |     |     |     |
| --- | --- | --- | --- | ------------- | --- | --- | --- | --- |
value,weinstructp toenditsreasoningtracewithascore i − 1 i N ( s i)
θ
|                                          |     |                |     | rewa r d . Theseupdated |     | valuesare u s e dintheUCTformula |     |     |
| ---------------------------------------- | --- | -------------- | --- | ----------------------- | --- | -------------------------------- | --- | --- |
| indicatingthecorrectnessofthetrajectory. |     | Ourkeydistinc- |     |                         |     |                                  |     |     |
(Eq.1)toguidetheselectionofthenextnode.
tionfromToTisthatweobtainthisvalueafterobtaining
|     |     |     |     | Reflection. | Inadditiontotheenvironmentalfeedback,we |     |     |     |
| --- | --- | --- | --- | ----------- | --------------------------------------- | --- | --- | --- |
theenvironmentalfeedback,improvingvalueassignment.
Thisalsoenablesscalingtomorechallengingenvironments, leverageself-reflectiontofurtherrefinethedecision-making
5

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
| PromptMethod |                  |                  |     | HotpotQA(EM)↑ |      |     |     | PromptMethod   |                   |     | HotpotQA(EM)↑ |      |     |
| ------------ | ---------------- | ---------------- | --- | ------------- | ---- | --- | --- | -------------- | ----------------- | --- | ------------- | ---- | --- |
| BaseLM       |                  |                  |     |               | 0.32 |     |     | ReAct          | (Yaoetal.,2023b)  |     |               | 0.32 |     |
| CoT          | (Weietal.,2022)  |                  |     |               | 0.34 |     |     | ReAct(bestofk) |                   |     |               | 0.38 |     |
| CoT-SC       |                  |                  |     |               | 0.38 |     |     | Reflexion      |                   |     |               | 0.51 |     |
|              |                  | (Wangetal.,2022) |     |               |      |     |     |                | (Shinnetal.,2023) |     |               |      |     |
| ToT          | (Yaoetal.,2023a) |                  |     |               | 0.55 |     |     | ToT(ReAct)     |                   |     |               | 0.39 |     |
| RAP          |                  |                  |     |               | 0.60 |     |     | RAP(ReAct)     |                   |     |               | 0.54 |     |
(Haoetal.,2023)
| RAP(n=10) |     |     |     |     | 0.60 |     |     | LATS(ReAct) |     |     |     | 0.63 |     |
| --------- | --- | --- | --- | --- | ---- | --- | --- | ----------- | --- | --- | --- | ---- | --- |
| LATS(CoT) |     |     |     |     | 0.62 |     |     | LATS(n=3)   |     |     |     | 0.58 |     |
|           |     |     |     |     |      |     |     | LATS(n=10)  |     |     |     | 0.65 |     |
Table2.GPT-3.5reasoning-basedpromptingresultsonHotpotQA. LATS(CoT+ReAct) 0.71
| LATSachievesthehighestexactmatch(EM)forreasoning. |     |     |     |     |     |     | We  |     |     |     |     |     |     |
| ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
samplen=5nodesduringexpansionandk=50trajectories.
|     |     |     |     |     |     |     |     | Table3.GPT-3.5 | acting-based |               | prompting | results | on HotpotQA.   |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | ------------ | ------------- | --------- | ------- | -------------- |
|     |     |     |     |     |     |     |     | LATS achieves  | the          | highest exact | match     | (EM)    | for acting. We |
samplen=5nodesandusek=50trajectories.Wealsoevaluate
|     |     |     |     |     |     |     |     | sampling ReAct | k   | times and | using both | CoT | and ReAct base |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --------- | ---------- | --- | -------------- |
promptingdesignsforLATS,whichachievesthebestperformance.
NotethatLATSoutperformsToTandRAPwithReActprompting,
whicharethesimpleadaptationsofsearchalgorithmstodecision-
| process (Shinn                           |     | et al., | 2023; | Madaan | et al., | 2023).     | Upon | making. |     |     |     |     |     |
| ---------------------------------------- | --- | ------- | ----- | ------ | ------- | ---------- | ---- | ------- | --- | --- | --- | --- | --- |
| encounteringanunsuccessfulterminalnode,p |     |         |       |        |         | isprompted |      |         |     |     |     |     |     |
θ
withthetrajectoryandfinalrewardtoprovideaverbalself-
| reflection | that summarizes |     |     | the errors | in the | reasoning | or  |     |     |     |     |     |     |
| ---------- | --------------- | --- | --- | ---------- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- |
5.1.HotPotQA
| actingprocessandproposessuperioralternatives. |     |     |     |     |     | Westore |     |     |     |     |     |     |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
bothfailedtrajectoriesandcorrespondingreflectionsinthe Forataskthatcanbeapproachedwithbothreasoning-based
memory. Insubsequentiterations, theseareintegratedas andacting-basedstrategies,weconsiderHotPotQA(Yang
additionalcontexttotheagentandvaluefunction,refining et al., 2018), a multi-hop question-answering benchmark
boththroughin-contextlearning. Thisimpartsasemantic thatrequiresretrievalovertwoormoreWikipediapassages.
gradient signal more useful than a scalar value, enabling Fortheactionspace,inadditiontoLMthoughts,wefollow
theagenttolearnfromtrialanderrorwithoutthecostof thesetupfromYaoetal.(2023b),whichprovidestheagent
expensiveoptimizationsuchasreinforcementlearning. withAPIcallstosearchandretrieveinformation.Theoutput
oftheseAPIcallsandself-generatedreflectionsformthe
| Discussion.    | Conceptually,LATShasseveralnotableadvan- |                     |     |               |       |               |     |                   |           |                                    |                |             |               |
| -------------- | ---------------------------------------- | ------------------- | --- | ------------- | ----- | ------------- | --- | ----------------- | --------- | ---------------------------------- | -------------- | ----------- | ------------- |
|                |                                          |                     |     |               |       |               |     | observationspace. |           | Notethatconsistentwithpreviouswork |                |             |               |
| tages as       | a general                                | framework           |     | for reasoning |       | and decision- |     |                   |           |                                    |                |             |               |
|                |                                          |                     |     |               |       |               |     | (Yao et al.,      | 2023b;    | Shinn                              | et al., 2023), | we          | use an oracle |
| making with    | LM                                       | agents.             | (1) | Generality:   | LATS  | supports      |     |                   |           |                                    |                |             |               |
|                |                                          |                     |     |               |       |               |     | setup for         | HotPotQA, | in which                           | the            | environment | provides      |
| both reasoning |                                          | and decision-making |     |               | tasks | by defining   | a   |                   |           |                                    |                |             |               |
feedbackabouttheanswer’scorrectnessuponreceivingan
| shared space | of   | thoughts | and | actions. | (2)      | Deliberation: |     |                                                    |     |     |     |     |     |
| ------------ | ---- | -------- | --- | -------- | -------- | ------------- | --- | -------------------------------------------------- | --- | --- | --- | --- | --- |
|              |      |          |     |          |          |               |     | answer. Thisenablesafaircomparisonbetweenourmethod |     |     |     |     |     |
| Leveraging   | MCTS | and      | LM  | value    | function | in LATS       | en- |                                                    |     |     |     |     |     |
andbaselinesinscenarioswherethequalityoffeedbackis
suresaprincipledsearchthatselectsoptionswithhighvalue
high,allowingustofocusourevaluationonhowwellthe
| while exploring |     | promising |     | alternatives. | (3) | Adaptability: |     |                                    |     |     |     |                |     |
| --------------- | --- | --------- | --- | ------------- | --- | ------------- | --- | ---------------------------------- | --- | --- | --- | -------------- | --- |
|                 |     |           |     |               |     |               |     | agentincorporatesexternalfeedback. |     |     |     | Weuseasubsetof |     |
Incorporatingexternalfeedbackthroughobservationsand
100questionsandthreefew-shotexamplesforeachmethod.
self-reflectioninLATSenablesgreateradaptationduring
|                  |     |                 |     |                    |     |     |     | ForToT,weuseDFSasthebasesearchalgorithm. |     |     |     |     | Forall |
| ---------------- | --- | --------------- | --- | ------------------ | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | ------ |
| problem-solving. |     | (4)Flexibility: |     | LATScanaccommodate |     |     |     |                                          |     |     |     |     |        |
methodsthatinvolvesampling,includingLATS,wesample
differentscenarios,environments,andresourcestipulations
|                                          |     |     |     |     |     |          |     | k =50trajectories. |     | MoredetailsareinAppendixSec.D. |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | --- | -------- | --- | ------------------ | --- | ------------------------------ | --- | --- | --- |
| bymodifyingstatedesignandtreedimensions. |     |     |     |     |     | (5)Modu- |     |                    |     |                                |     |     |     |
larity:
ThebaseLMagent,reflectiongenerator,andvalue Weevaluateinternalreasoningstrategiesbyremovingac-
functioncanbeindependentlyalteredandadaptedtoindi- tionsandobservationsfromthecontext,correspondingto
vidualLMproperties. CoT(Weietal.,2022)anditsvariants,CoT-SC(Wangetal.,
2022),ToT(Yaoetal.,2023a),andRAP(Haoetal.,2023).
Thesemethodsrelysolelyontheagent’sexistingknowledge
5.Experiments
|     |     |     |     |     |     |     |     | toanswerthequestion. |     | Wefurtherconsideracting-based |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | ----------------------------- | --- | --- | --- |
TodemonstratethegeneralapplicabilityofLATS,weeval- methodsReAct,Reflexion,andLATS,whichaugmentthe
uateourmethodonavarietyofdomainsthatrequirerea- agentwiththeinteractiveAPIenvironmentandprimarily
soningandacting: programming(Chenetal.,2021;Austin evaluateitsinformationretrievalabilities. Wealsodesign
etal.,2022),HotPotQA(Yangetal.,2018),WebShop(Yao asimpleintegrationofsearchalgorithmswithLMagents,
etal.,2022),andGameof24(Yaoetal.,2023a). extendingToTandRAPwithReActpromptingtohandle
6

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
| PromptMethod |                 | Model   | Pass@1↑ |      |     | PromptMethod |                 |     |     | Pass@1↑ |     |     |
| ------------ | --------------- | ------- | ------- | ---- | --- | ------------ | --------------- | --- | --- | ------- | --- | --- |
| CoT          | (Weietal.,2022) | GPT-3.5 |         | 46.9 |     | CoT          | (Weietal.,2022) |     |     | 54.9    |     |     |
ReAct (Yaoetal.,2023b) GPT-3.5 56.9 ReAct (Weietal.,2022) 67.0
| Reflexion   |                   | GPT-3.5 |     | 68.1 |                                    | Reflexion   |                  |                   |     | 70.0               |           |      |
| ----------- | ----------------- | ------- | --- | ---- | ---------------------------------- | ----------- | ---------------- | ----------------- | --- | ------------------ | --------- | ---- |
|             | (Shinnetal.,2023) |         |     |      |                                    |             |                  | (Shinnetal.,2023) |     |                    |           |      |
| ToT         | (Yaoetal.,2023a)  | GPT-3.5 |     | 54.4 |                                    | ToT         | (Yaoetal.,2023a) |                   |     | 65.8               |           |      |
| RAP         |                   | GPT-3.5 |     | 63.1 |                                    | RAP         |                  |                   |     | 71.4               |           |      |
|             | (Haoetal.,2023)   |         |     |      |                                    |             | (Haoetal.,2023)  |                   |     |                    |           |      |
| LATS(ReAct) |                   | GPT-3.5 |     | 83.8 |                                    | LATS(ReAct) |                  |                   |     | 81.1               |           |      |
| BaseLM      |                   | GPT-4   |     | 80.1 |                                    |             |                  |                   |     |                    |           |      |
|             |                   |         |     |      | Table5.GPT-3.5                     |             | Pass@1           | accuracy          | on  | MBPP.              | Prompting | with |
| Reflexion   |                   | GPT-4   |     | 91.0 |                                    |             |                  |                   |     |                    |           |      |
|             |                   |         |     |      | LATSachievesthehighestperformance. |             |                  |                   |     | Wesample5solutions |           |      |
| LATS(ReAct) |                   | GPT-4   |     | 92.7 |                                    |             |                  |                   |     |                    |           |      |
duringexpansionfor8iterations.
| Table4.GPT-3.5 | and GPT-4 | Pass@1 accuracy | on  | HumanEval. |     |     |     |     |     |     |     |     |
| -------------- | --------- | --------------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
PromptingwithLATSachievesthebestperformance.Wesample
5solutionsduringexpansionfor8iterations.
5.2.Programming
|                       |                                |     |     |     | To demonstrate |     | the       | importance | of  | external | observations  |     |
| --------------------- | ------------------------------ | --- | --- | --- | -------------- | --- | --------- | ---------- | --- | -------- | ------------- | --- |
|                       |                                |     |     |     | for complex    |     | reasoning | tasks,     | we  | evaluate | the baselines |     |
| externalobservations. | Inaddition,whileLATSisdesigned |     |     |     |                |     |           |            |     |          |               |     |
andLATSonprogrammingwithHumanEval(Chenetal.,
forscenarioswhereexternalfeedbackcanenhancereason-
|     |     |     |     |     | 2021)1andMBPP(Austinetal.,2022). |     |     |     |     | Bothdatasetsmea- |     |     |
| --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- | ---------------- | --- | --- |
ing,wealsoimplementareasoning-onlyversionwithCoT surethecorrectnessofsynthesizedprogramsinPythonfrom
| asthebasepromptingframework. |     | Moreover,wecombine |     |     |         |          |             |     |        |            |           |     |
| ---------------------------- | --- | ------------------ | --- | --- | ------- | -------- | ----------- | --- | ------ | ---------- | --------- | --- |
|                              |     |                    |     |     | natural | language | docstrings. |     | We use | individual | solutions |     |
internalandexternalreasoninginLATSbyfirstprompting astheactionspaceandtestsuiteandcompilerfeedbackas
withaCoT-basedpromptandthenswitchingtoaReAct- theexternalobservation. WefollowChenetal.(2023a)and
| basedpromptuponfailure. |     | Thisisclosertohowhumans |     |     |     |     |     |     |     |     |     |     |
| ----------------------- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
useanLMtogenerateasynthetictestsuiteofsyntactically
mightapproachthistaskbyusingtoolstoretrieveadditional valid“assert”statementsforeachquestion. Foreachstep,
informationonlywhentheanswerisnotalreadyknown.
thesolutionisevaluatedonthistestsuite,andtheresults,
includingsuccessfulandfailedtestsandcompileroutput,
| Results. | We observe in | Tab. 2 and | Tab. 3 | that both in- |     |     |     |     |     |     |     |     |
| -------- | ------------- | ---------- | ------ | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
areaddedtothecontextasanobservation.
| ternal reasoning | and external | retrieval | strategies | perform |     |     |     |     |     |     |     |     |
| ---------------- | ------------ | --------- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
wellonHotPotQA.Duetotheirlarge-scaletrainingcorpus,
|     |     |     |     |     | Forthistask, |     | thereasoningandactingbaselinessharean |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------------ | --- | ------------------------------------- | --- | --- | --- | --- | --- |
modern LMs already encode factual knowledge and can action space, but acting methods are able to incorporate
| oftendirectlyanswerthequestioncorrectly. |     |     | WhileCoTcan |     |                                  |     |     |     |     |                   |     |     |
| ---------------------------------------- | --- | --- | ----------- | --- | -------------------------------- | --- | --- | --- | --- | ----------------- | --- | --- |
|                                          |     |     |             |     | observationsasadditionalcontext. |     |     |     |     | ForLATS,sinceeach |     |     |
slightly enhance performance on questions requiring rea- actioncorrespondstoacompletesolution,weskipthesim-
soning,largergainsareobservedwithsearchmethodsToT
|     |     |     |     |     | ulation | step | of LATS | and | directly | use the | percentage | of  |
| --- | --- | --- | --- | --- | ------- | ---- | ------- | --- | -------- | ------- | ---------- | --- |
andRAP(Tab.2,Row4,5),whichcansampleandexplore
|     |     |     |     |     | passedtestsasthebackpropagatedreward. |     |     |     |     |     | Weusek | = 8 |
| --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | ------ | --- |
moreoutputs. Weobservesimilarresultsforacting-based iterations,setthenumberofgeneratedtestsat4,andsam-
| methods. | LATSsurpassesReAct,evenwhensamplingthe |     |     |     |      |                              |     |     |     |                  |     |     |
| -------- | -------------------------------------- | --- | --- | --- | ---- | ---------------------------- | --- | --- | --- | ---------------- | --- | --- |
|          |                                        |     |     |     | plen | = 5solutionsduringexpansion. |     |     |     | Afterthesearchis |     |     |
samenumberoftrajectories,byexpandingmorenodeswith completed,weselectthesolutionwiththehighestvalueand
| principled                                     | search. This is | demonstrated | when | modifying |             |                                       |     |           |           |            |     |          |
| ---------------------------------------------- | --------------- | ------------ | ---- | --------- | ----------- | ------------------------------------- | --- | --------- | --------- | ---------- | --- | -------- |
|                                                |                 |              |      |           | evaluate    | it on                                 | the | real test | suite for | the pass@1 |     | accuracy |
| n,thenumberofnodesexpandedduringeachiteration. |                 |              |      | In-       |             |                                       |     |           |           |            |     |          |
|                                                |                 |              |      |           | evaluation. | MoredetailscanbefoundinAppendixSec.D. |     |           |           |            |     |          |
creasingncanconsistentlyimproveperformance,although
at greater computational and inference costs. LATS also Results. Tab.4andTab.5showthatbothsearchandseman-
|     |     |     |     |     | ticfeedbackarecrucialforbetterperformance. |     |     |     |     |     | Despitenot |     |
| --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | ---------- | --- |
outperformsRAPoninternalreasoning,buthashigherper-
usingobservations,ToTandRAParecompetitivewithRe-
formanceonthedecision-makingsettingofHotPotQAthan
thereasoningsetting.ContrarytoLATS,theReActversions flexion. LATShasthehighestperformanceonbothdatasets.
RAPusesasearchalgorithmsimilartoLATS,whichreveals
ofToTandRAP(Tab.3,Row4,5)performevenworsethan
theimportanceofexternalfeedbackfordifficultreasoning
thereasoning-onlysettingofHotPotQA,whichindicates
thattheacting-basedsettingismorechallengingandadap- taskssuchasprogramming. WithGPT-4,usingLATSsets
thestateoftheartforHumanEval,validatingthatLATScan
tationofsearchalgorithmstodecision-makingscenarios
isnon-trivial. Combininginternalandexternalreasoning beusedwithmoreadvancedLMsforhigherperformance.
| inLATSresultsinthehighestperformance,indicatingthe |     |     |     |     | 1Some |           |     |         |           |      |            |     |
| -------------------------------------------------- | --- | --- | --- | --- | ----- | --------- | --- | ------- | --------- | ---- | ---------- | --- |
|                                                    |     |     |     |     |       | baselines |     | use 161 | questions | from | HumanEval. | We  |
importanceofexternalfeedbackinaugmentingreasoning
|     |     |     |     |     | use all | 164 questions |     | for LATS | and find | minimal | performance |     |
| --- | --- | --- | --- | --- | ------- | ------------- | --- | -------- | -------- | ------- | ----------- | --- |
evenintaskswherethebaseLMcanalreadyperform.
differences,sowereportbaselinesforbothsettings.
7

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
|     |           |                      | Method            |     | Score↑ |     | SR↑  | PromptMethod        |                   | Gameof24(SuccessRate)↑ |      |     |
| --- | --------- | -------------------- | ----------------- | --- | ------ | --- | ---- | ------------------- | ----------------- | ---------------------- | ---- | --- |
|     |           | ReAct                | (Yaoetal.,2023b)  |     | 53.8   |     | 28.0 | CoT (Weietal.,2022) |                   |                        | 0.08 |     |
|     |           | ReAct(bestofk)       |                   |     | 59.1   |     | 32.0 | Reflexion           | (Shinnetal.,2023) |                        | 0.12 |     |
|     | Reflexion |                      |                   |     | 64.2   |     | 35.0 | ToT                 |                   |                        | 0.20 |     |
|     |           |                      | (Shinnetal.,2023) |     |        |     |      | (Yaoetal.,2023a)    |                   |                        |      |     |
|     |           | LATS(ReAct)          |                   |     | 75.9   |     | 38.0 | RAP (Haoetal.,2023) |                   |                        | 0.40 |     |
|     |           |                      |                   |     |        |     |      | LATS(CoT)           |                   |                        | 0.44 |     |
|     |           | IL(Yaoetal.,2022)    |                   |     | 59.9   |     | 29.1 |                     |                   |                        |      |     |
|     |           | IL+RL(Yaoetal.,2022) |                   |     | 62.4   |     | 28.7 |                     |                   |                        |      |     |
Table7.ResultsonGameof24withGPT-3.5.Wesamplen=5
|     | Fine-tuning |     | (Furutaetal.,2024) |     | 67.5 |     | 45.0 |     |     |     |     |     |
| --- | ----------- | --- | ------------------ | --- | ---- | --- | ---- | --- | --- | --- | --- | --- |
nodesandk=30trajectories.
|              |     |     | Expert  |           | 82.1        |     | 59.6        |              |     |     |               |     |
| ------------ | --- | --- | ------- | --------- | ----------- | --- | ----------- | ------------ | --- | --- | ------------- | --- |
|              |     |     |         |           |             |     |             | PromptMethod |     |     | HotPotQA(EM)↑ |     |
| Table6.Score |     | and | success | rate (SR) | on WebShop. |     | Results are |              |     |     |               |     |
organizedintoprompting,RL-basedtraining,andhumanperfor- ToT(ReAct) 0.39
mance.Forthesamenumberofiterations,LATSimprovesboth RAP(ReAct) 0.54
scoreandSRandsurpassesRL-basedtraining. LATS(NoLMHeuristic) 0.37
|     |     |     |     |     |     |     |     | LATS(DFS)          |     |     | 0.42 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | ---- | --- |
|     |     |     |     |     |     |     |     | LATS(NoReflection) |     |     | 0.58 |     |
|     |     |     |     |     |     |     |     | LATS(ReAct)        |     |     | 0.63 |     |
5.3.WebShop
For a complex decision-making environment with practi- Table8.AblationresultsonLATSandbaselinevariantsinHot-
calapplications,weconsiderWebShop(Yaoetal.,2022), PotQA. We use ReAct as the base prompt and sample n = 5
childrenandk=50trajectories.LATSrequireseverycomponent
| an  | online | shopping | environment |     | composed | of  | a website |     |     |     |     |     |
| --- | ------ | -------- | ----------- | --- | -------- | --- | --------- | --- | --- | --- | --- | --- |
with1.18Mreal-worldproductsand12khumaninstructions. andoperationforoptimalperformance.
Agentsmustnavigateawebsitethroughavarietyofcom-
| mands | to  | purchase | an  | item matching | a   | user specification. |     |                |                                    |     |     |     |
| ----- | --- | -------- | --- | ------------- | --- | ------------------- | --- | -------------- | ---------------------------------- | --- | --- | --- |
|       |     |          |     |               |     |                     |     | showninTab.8). | Moreablationsfortokenconsumptionon |     |     |     |
Weusethepreconstructedactionspaceofsearchandclick
HotPotQAareinTab.9inAppendixSec.C.
| commands |     | and | browser | feedback | and | reflections | for the |     |     |     |     |     |
| -------- | --- | --- | ------- | -------- | --- | ----------- | ------- | --- | --- | --- | --- | --- |
observation. Theperformanceisgaugedusingtwometrics: Reasoning on Game of 24. To show how LATS can be
anaveragescore,reflectingthepercentageofuser-specified
appliedtopurelyinternalreasoningtasks,weadditionally
attributesmetbytheselectedproduct,andasuccessrate, evaluateonGameof24(Yaoetal.,2023a),amathematical
indicatingthefrequencywithwhichthechosenproductful- reasoningtaskwheretheagentmustconstruct24outofa
| fillsallgivenconditions. |     |     |     | Wecompareagainstacting-based |     |     |     |                |           |             |            |        |
| ------------------------ | --- | --- | --- | ---------------------------- | --- | --- | --- | -------------- | --------- | ----------- | ---------- | ------ |
|                          |     |     |     |                              |     |     |     | set of numbers | and basic | operations. | We use CoT | as the |
promptingmethodsandRL-basedapproaches. Weevaluate basepromptingdesignandemploythesameoperationsas
on50instructions,expandn=5childrenforLATS,andset
|     |     |     |     |     |     |     |     | inothersettings. | WefindinTab.7thatLATSoutperforms |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | -------------------------------- | --- | --- | --- |
k =30forLATS,ReAct(bestofk),andReflexion. More previousmethodsproposedspecificallyforreasoning. This
detailsandpromptsareinAppendixSec.DandSec.G. isduetoourproposedvaluefunction,whichincorporates
self-consistencyasanadditionalheuristic.
| Results. |     | We find | in Tab. | 6   | that GPT-3.5 | with | ReAct is |     |     |     |     |     |
| -------- | --- | ------- | ------- | --- | ------------ | ---- | -------- | --- | --- | --- | --- | --- |
competitive to imitation learning (IL) and can exceed re- Self-reflection. LATSusesself-reflectiontoprovideaddi-
inforcementlearningtechniqueswithstrongerprompting
|     |     |     |     |     |     |     |     | tionalsemanticsignalsfortheagent. |     |     | InTab.8(Row5,6), |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | ---------------- | --- |
strategies. Sampling k = 30 trajectories with ReAct and weobservea0.05performancedropwhenself-reflection
Reflexionresultsinasimilarperformance,suggestingthese-
|     |     |     |     |     |     |     |     | isremovedfromLATS,validatingitsusefulness. |     |     |     | Thisisa |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | ------- |
manticfeedbackisnotashelpfulincomplexenvironments smallergainthanthe0.19gainthatReflexionhasoverRe-
likeWebShop. SimilartoShinnetal.(2023),wefindthat ActasshowninTab.3,suggestingoverlapbetweentheques-
generatedreflectionsareoftengenericanddonotprovide
tionswhereananswercanbeimprovedbyself-reflection
useful feedback, resulting in a tendency for the agent to andsearch. ThisvariantoutperformsRAP(ReAct),reflect-
| becomestuckinlocalminima. |     |     |     |     | However, | usingLATSin- |     |     |     |     |     |     |
| ------------------------- | --- | --- | --- | --- | -------- | ------------ | --- | --- | --- | --- | --- | --- |
ingourimprovementstoMCTS.
deedresultsinanoticeableimprovement,indicatingamore
|     |     |     |     |     |     |     |     | Searchalgorithm. | MCTSisamoreprincipledsearchalgo- |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | -------------------------------- | --- | --- | --- |
effectiveexplorationforthesamenumberofiterations.
rithmthanvariantslikeA*(Zhuangetal.,2023)orDFSand
|     |     |     |     |     |     |     |     | is the basis | for observed | performance | gains. We | observe |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ------------ | ----------- | --------- | ------- |
5.4.AblationStudyandAdditionalAnalysis
|     |     |     |     |     |     |     |     | the effects | of using DFS, | and incorporate | the | LM-based |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ------------- | --------------- | --- | -------- |
WefurthertestthereasoningabilityofLATSonGameof24, heuristicusedinToTinwhichbrancheswithlowvaluesare
andalsoconductadditionalexperimentsonHotPotQAto pruned. This removes the selection and backpropagation
demonstratetheeffectofeachcomponentofLATS(results operations,andweobservea0.21dropinperformancein
8

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
|     |                     | Method |     | Performance↑ | Samplecomplexity↓ |       | TokenConsumption↓ |         |     |     |     |
| --- | ------------------- | ------ | --- | ------------ | ----------------- | ----- | ----------------- | ------- | --- | --- | --- |
|     | ReAct(Bestk=250)    |        |     | 0.42         |                   | O(k)  |                   |         | -   |     |     |
|     | CoT-SC(n=1,k=250)   |        |     | 0.40         |                   | O(k)  |                   |         | -   |     |     |
|     | LATS(n=1,k=50)      |        |     | 0.48         |                   | O(k)  |                   |         | -   |     |     |
|     | ToT(ReAct,n=5,k=50) |        |     | 0.49         |                   | O(kn) |                   | 210,215 |     |     |     |
|     | RAP(ReAct,n=5,k=50) |        |     | 0.54         |                   | O(kn) |                   | 176,500 |     |     |     |
|     | LATS(n=5,k=50)      |        |     | 0.63         |                   | O(kn) |                   | 173,290 |     |     |     |
Table9.Performance,samplecomplexityofdifferentmethods,averagenumberofnodesexpanded,andtokenconsumptionuponsuccess
bymethodswithtree-basedsearch.nisthenumberofchildrennodesexpandedateverystepandkisthenumberoftrajectories.LATS
hasthesamesamplecomplexityasothermethodswithtree-basedsearchandexpandslessnodesuponsuccess,whichindicateslower
tokencost.
Method k HotPotQA↑ #ofNodes↓ RAPand12.12fewernodesthanToT.Thesefindingsun-
derscoreourimprovementstoMCTSandadaptationtoLM
| ToT | 10  | 0.34 | 33.97 |     |     |     |     |     |     |     |     |
| --- | --- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
agents,resultinginamoreprincipledandefficientsearch
| RAP | 10  | 0.44 | 31.53 |     |     |     |     |     |     |     |     |
| --- | --- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
mechanism.
| LATS | 10  | 0.44 | 28.42 |     |     |     |     |     |     |     |     |
| ---- | --- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
| ToT  | 30  | 0.39 | 47.54 |     |     |     |     |     |     |     |     |
6.Conclusion
| RAP  | 30  | 0.50 | 37.71 |     |     |     |     |     |     |     |     |
| ---- | --- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
| LATS | 30  | 0.52 | 34.12 |     |     |     |     |     |     |     |     |
ThisworkintroducesLanguageAgentTreeSearch(LATS),
ToT 50 0.49 84.05 the first framework to unify reasoning, acting, and plan-
|     |     |      |       |     | ningforenhancedLMproblem-solving. |     |     |     |     | LATSaddresses |     |
| --- | --- | ---- | ----- | --- | --------------------------------- | --- | --- | --- | --- | ------------- | --- |
| RAP | 50  | 0.54 | 70.60 |     |                                   |     |     |     |     |               |     |
LATS 50 0.61 66.65 key limitations of prior prompting techniques by deliber-
|     |     |     |     |     | ately | constructing | trajectories |     | with search | algorithms, | in- |
| --- | --- | --- | --- | --- | ----- | ------------ | ------------ | --- | ----------- | ----------- | --- |
Table10.Comparison of the cost of different methods on Hot- corporatingexternalfeedback,andenablingagentstolearn
PotQA.LATSachievesthehighestaccuracyandthelowestav- fromexperience. Ourevaluationdemonstratestheability
erage number of nodes/states required for success at various k of LATS to harness LM capabilities for various decision-
trajectoriessampled.
makingtaskswhilemaintainingitsreasoningabilitywithout
additionaltraining.Theproposedsynergiesbetweensearch,
Tab.8(Row4)whensamplingthesamenumberofnodes interaction,andreflectionofferaversatileapproachtoau-
|                           |     |                           |     |     | tonomous | decision-making, |     | highlighting |     | the potential | of  |
| ------------------------- | --- | ------------------------- | --- | --- | -------- | ---------------- | --- | ------------ | --- | ------------- | --- |
| butoutperformsToT(ReAct). |     | Despitealsobenefitingfrom |     |     |          |                  |     |              |     |               |     |
LMsasgeneralistagents.
| ground-truthfeedback,            |     | LATSusesitbetterthanToTand |              |     |                                 |     |     |     |     |                |     |
| -------------------------------- | --- | -------------------------- | ------------ | --- | ------------------------------- | --- | --- | --- | --- | -------------- | --- |
| RAPandcanoutperformthesemethods. |     |                            | Wealsofindin |     |                                 |     |     |     |     |                |     |
|                                  |     |                            |              |     | Limitationsandfuturedirections. |     |     |     |     | LATShastwomain |     |
Tab.8(Row3)thatLMscoring,themaincomponentofour
limitationsthatshouldbeconsideredbeforeitsapplication.
valuefunction,iscrucialforleveragingexternalfeedback
First,ithasahighercomputationalcostcomparedtosimpler
andstrongperformance.
|     |     |     |     |     | prompting | methods | like | ReAct | or Reflexion, | which | may |
| --- | --- | --- | --- | --- | --------- | ------- | ---- | ----- | ------------- | ----- | --- |
Sample complexity and token consumption. One pos- limit its practicality in certain situations. Second, LATS
sible concern of LATS is that the tree-structured search assumes the ability to revert to earlier states in decision-
mightconsumemuchmoretokensthanexistingmethods. making environments, which may not be universally ap-
TofurtherstudythecomputationalcostofLATScompared plicable in all possible environments. Despite these limi-
topriormethods,weexaminethesamplecomplexity(i.e., tations, it is worth noting that LATS still achieves better
asymptotic token cost) of all methods considered in this performanceandefficiencycomparedtosimilarmethods,
paper and count the average number of nodes expanded andthenumberofnodesexpandedateachstepprovidesa
byourmethodandothertree-structuredmethods(ToTand trade-offbetweenperformanceandefficiency. Additionally,
RAP)uponsuccessfulsearchonHotPotQA.Wepresentthe we expect inference-time compute costs to decrease over
resultsinTab.9andTab.10,whichshowthatourmethod time,therebyincreasingtheusefulnessofLATSandother
hasthesamesamplecomplexityasothertree-basedsearch “System-2” LM approaches. Finally, the reversion prop-
methodsandrequiresfeweroveralltokensandstates. The ertyisfeasibleinmanyreal-worldapplications,openingup
tokencostgapwillbeevenlargerwhentakingfailedtrajec- newopportunitiesintheLMdecision-makingcommunity.
toriesintoaccount,sinceourmethodhasahighersuccess Futuredirectionsinclude scalingLATStomore complex
rateandreachesthecomputationalbudgetlimitlessoften. environmentsormulti-agentframeworksandimprovingef-
Thisisalsotruewhensamplingasmallernumberoftrajec- ficiencytoreducecosts. Amoredetaileddiscussionabout
tories; on average, LATS requires 3.55 fewer nodes than thelimitationsofLATScanbefoundinAppendixSec.B.
9

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
ImpactStatement stenberger, Lukas Gianinazzi, Joanna Gajda, Tomasz
Lehmann,MichalPodstawski,HubertNiewiadomski,Pi-
| LATS is | a framework  | that | enhances        |     | LM performance |          |             |     |             |     |          |       |              |
| ------- | ------------ | ---- | --------------- | --- | -------------- | -------- | ----------- | --- | ----------- | --- | -------- | ----- | ------------ |
|         |              |      |                 |     |                |          | otr Nyczyk, |     | and Torsten |     | Hoefler. | Graph | of thoughts: |
| through | interactions | with | an environment. |     | This           | improve- |             |     |             |     |          |       |              |
Solvingelaborateproblemswithlargelanguagemodels.
mentinautonomousdecision-makingmayfacilitateharm-
arXiv:2308.09687,2023.
| ful uses | of LMs. | On the | other | hand, LATS |     | enhances in- |     |     |     |     |     |     |     |
| -------- | ------- | ------ | ----- | ---------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
terpretabilityandthepotentialforgreateralignment,asit SamuelRBowman,GaborAngeli,ChristopherPotts,and
involveshigh-levellinguisticreasoningandactionsthrough Christopher D Manning. A large annotated corpus for
severalroundsofdecision-makingandreflectionratherthan learningnaturallanguageinference. InEMNLP,2015.
| relyingonautoregressivegeneration. |     |     |     | Finally,enhancingthe |     |     |        |        |          |     |            |        |         |
| ---------------------------------- | --- | --- | --- | -------------------- | --- | --- | ------ | ------ | -------- | --- | ---------- | ------ | ------- |
|                                    |     |     |     |                      |     |     | Tom B. | Brown, | Benjamin |     | Mann, Nick | Ryder, | Melanie |
capabilitiesofLMagentsmayraisesecurityrisks,suchas
Subbiah,JaredKaplan,PrafullaDhariwal,ArvindNee-
| executingmalware. |     | Weencouragefurtherresearchtofully |     |     |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
lakantan,PranavShyam,GirishSastry,AmandaAskell,
understandandmitigatetherisksofLMs.
SandhiniAgarwal,ArielHerbert-Voss,GretchenKrueger,
TomHenighan,RewonChild,AdityaRamesh,DanielM.
Acknowledgements
Ziegler,JeffreyWu,ClemensWinter,ChristopherHesse,
|     |     |     |     |     |     |     | Mark | Chen, | Eric Sigler, |     | Mateusz Litwin, |     | Scott Gray, |
| --- | --- | --- | --- | --- | --- | --- | ---- | ----- | ------------ | --- | --------------- | --- | ----------- |
WethankDanielCamposforusefulfeedbackonearlierver-
|                   |     |                                 |     |     |     |     | Benjamin    | Chess, | Jack | Clark,   | Christopher     |     | Berner, Sam |
| ----------------- | --- | ------------------------------- | --- | --- | --- | --- | ----------- | ------ | ---- | -------- | --------------- | --- | ----------- |
| sionsofthispaper. |     | ThisworkwassupportedinpartbyNSF |     |     |     |     |             |        |      |          |                 |     |             |
|                   |     |                                 |     |     |     |     | McCandlish, |        | Alec | Radford, | Ilya Sutskever, |     | and Dario   |
Grant2106825,NIFAAward2020-67021-32799,theJump
|     |     |     |     |     |     |     | Amodei. | Language |     | models | are few-shot |     | learners. In |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------- | --- | ------ | ------------ | --- | ------------ |
ARCHESendowmentthroughtheHealthCareEngineering
NeurIPS,2020.
SystemsCenteratIllinoisandtheOSFFoundation,andthe
| IBM-Illinois | Discovery | Accelerator |     | Institute. |     | This work |        |           |     |        |           |     |             |
| ------------ | --------- | ----------- | --- | ---------- | --- | --------- | ------ | --------- | --- | ------ | --------- | --- | ----------- |
|              |           |             |     |            |     |           | Murray | Campbell, | A   | Joseph | Hoane Jr, | and | Feng-hsiung |
used NVIDIA GPUs at NCSA Delta through allocations Hsu. Deepblue. Artificialintelligence,2002.
CIS220014,CIS230012,andCIS230218fromtheACCESS
| program. |     |     |     |     |     |     | BeiChen,FengjiZhang,AnhNguyen,DaoguangZan,Zeqi |     |     |     |               |            |     |
| -------- | --- | --- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- | ------------- | ---------- | --- |
|          |     |     |     |     |     |     | Lin,Jian-GuangLou,andWeizhuChen.               |     |     |     |               | CodeT:Code |     |
|          |     |     |     |     |     |     | generationwithgeneratedtests.                  |     |     |     | InICLR,2023a. |            |     |
References
|     |     |     |     |     |     |     | Mark Chen, | Jerry | Tworek, |     | Heewoo Jun, | Qiming | Yuan, |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ----- | ------- | --- | ----------- | ------ | ----- |
MichaelAhn,AnthonyBrohan,NoahBrown,YevgenCheb-
HenriquePonde,JaredKaplan,HarrisonEdwards,Yura
otar,OmarCortes,ByronDavid,ChelseaFinn,Chuyuan
|               |        |                 |       |             |          |              | Burda,  | Nicholas | Joseph,  |          | Greg Brockman, |         | Alex Ray, |
| ------------- | ------ | --------------- | ----- | ----------- | -------- | ------------ | ------- | -------- | -------- | -------- | -------------- | ------- | --------- |
| Fu, Keerthana |        | Gopalakrishnan, |       | Karol       | Hausman, | Alex         |         |          |          |          |                |         |           |
|               |        |                 |       |             |          |              | Raul    | Puri,    | Gretchen | Krueger, | Michael        | Petrov, | Heidy     |
| Herzog,       | Daniel | Ho, Jasmine     |       | Hsu, Julian |          | Ibarz, Brian |         |          |          |          |                |         |           |
|               |        |                 |       |             |          |              | Khlaaf, | Girish   | Sastry,  | Pamela   | Mishkin,       | Brooke  | Chan,     |
| Ichter,       | Alex   | Irpan, Eric     | Jang, | Rosario     | Jauregui | Ruano,       |         |          |          |          |                |         |           |
ScottGray,NickRyder,MikhailPavlov,AletheaPower,
KyleJeffrey,SallyJesmonth,NikhilJJoshi,RyanJulian,
LukaszKaiser,MohammadBavarian,ClemensWinter,
DmitryKalashnikov,YuhengKuang,Kuang-HueiLee,
|     |     |     |     |     |     |     | Philippe | Tillet, | Felipe | Petroski | Such, | David | W. Cum- |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------- | ------ | -------- | ----- | ----- | ------- |
SergeyLevine,YaoLu,LindaLuu,CarolinaParada,Peter
|     |     |     |     |     |     |     | mings, | Matthias | Plappert, |     | Fotios Chantzis, |     | Elizabeth |
| --- | --- | --- | --- | --- | --- | --- | ------ | -------- | --------- | --- | ---------------- | --- | --------- |
Pastor,JornellQuiambao,KanishkaRao,JarekRetting-
|        |       |               |           |     |         |          | Barnes, | Ariel           | Herbert-Voss, |     | William       | H.            | Guss, Alex |
| ------ | ----- | ------------- | --------- | --- | ------- | -------- | ------- | --------------- | ------------- | --- | ------------- | ------------- | ---------- |
| house, | Diego | Reyes, Pierre | Sermanet, |     | Nicolas | Sievers, |         |                 |               |     |               |               |            |
|        |       |               |           |     |         |          | Nichol, | IgorBabuschkin, |               |     | SuchirBalaji, | ShantanuJain, |            |
ClaytonTan,AlexanderToshev,VincentVanhoucke,Fei
AndrewCarr,JanLeike,JoshuaAchiam,VedantMisra,
Xia,TedXiao,PengXu,SichunXu,MengyuanYan,and
|     |     |     |     |     |     |     | Evan | Morikawa, | Alec | Radford, | Matthew |     | M. Knight, |
| --- | --- | --- | --- | --- | --- | --- | ---- | --------- | ---- | -------- | ------- | --- | ---------- |
AndyZeng.DoasIcan,notasIsay:Groundinglanguage
MilesBrundage,MiraMurati,KatieMayer,PeterWelin-
| inroboticaffordances. |     |     | InCoRL,2022. |     |     |     |     |     |     |     |     |     |     |
| --------------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
der,BobMcGrew,DarioAmodei,SamMcCandlish,Ilya
Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Sutskever,andWojciechZaremba. Evaluatinglargelan-
Bosma,HenrykMichalewski,DavidDohan,EllenJiang, guagemodelstrainedoncode. arXiv:2107.03374,2021.
| Carrie | Cai, | Michael Terry, | Quoc | Le, | and | Charles Sut- |     |     |     |     |     |     |     |
| ------ | ---- | -------------- | ---- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
WenhuChen,XueguangMa,XinyiWang,andWilliamW.
| ton. Programsynthesiswithlargelanguagemodels. |     |     |     |     |     | In  |        |                             |     |     |     |               |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | ------ | --------------------------- | --- | --- | --- | ------------- | --- |
|                                               |     |     |     |     |     |     | Cohen. | Programofthoughtsprompting: |     |     |     | disentangling |     |
NeurIPS,2022.
|     |     |     |     |     |     |     | computation |     | from | reasoning | for numerical |     | reasoning |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ---- | --------- | ------------- | --- | --------- |
BowenBaker,IlgeAkkaya,PeterZhokhov,JoostHuizinga, tasks. TMLR,2023b. ISSN2835-8856.
| Jie Tang,                                     | Adrien | Ecoffet,        | Brandon |       | Houghton,   | Raul   |           |            |        |        |              |          |         |
| --------------------------------------------- | ------ | --------------- | ------- | ----- | ----------- | ------ | --------- | ---------- | ------ | ------ | ------------ | -------- | ------- |
|                                               |        |                 |         |       |             |        | Aakanksha | Chowdhery, |        | Sharan | Narang,      | Jacob    | Devlin, |
| Sampedro,                                     |        | and Jeff Clune. |         | Video | pretraining | (VPT): |           |            |        |        |              |          |         |
|                                               |        |                 |         |       |             |        | Maarten   | Bosma,     | Gaurav |        | Mishra, Adam | Roberts, | Paul    |
| Learningtoactbywatchingunlabeledonlinevideos. |        |                 |         |       |             | In     |           |            |        |        |              |          |         |
|                                               |        |                 |         |       |             |        | Barham,   | Hyung      | Won    | Chung, | Charles      | Sutton,  | Sebas-  |
NeurIPS,2022.
|     |     |     |     |     |     |     | tian | Gehrmann, | Parker |     | Schuh, Kensen |     | Shi, Sasha |
| --- | --- | --- | --- | --- | --- | --- | ---- | --------- | ------ | --- | ------------- | --- | ---------- |
Maciej Besta, Nils Blach, Ales Kubicek, Robert Ger- Tsvyashchenko,JoshuaMaynez,AbhishekRao,Parker
10

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
Barnes,YiTay,NoamShazeer,VinodkumarPrabhakaran, LuyuGao,AmanMadaan,ShuyanZhou,UriAlon,Pengfei
Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, Liu, Yiming Yang, Jamie Callan, and Graham Neubig.
JamesBradbury,JacobAustin,MichaelIsard,GuyGur- PAL:Program-aidedlanguagemodels. InICML,2023.
Ari,PengchengYin,TojuDuke,AnselmLevskaya,San-
jayGhemawat,SunipaDev,HenrykMichalewski,Xavier JiaxianGuo,SidiLu,HanCai,WeinanZhang,YongYu,and
|         |        |        |       |           |     |      |        | JunWang.               | Longtextgenerationviaadversarialtraining |     |              |     |     |     |
| ------- | ------ | ------ | ----- | --------- | --- | ---- | ------ | ---------------------- | ---------------------------------------- | --- | ------------ | --- | --- | --- |
| Garcia, | Vedant | Misra, | Kevin | Robinson, |     | Liam | Fedus, |                        |                                          |     |              |     |     |     |
|         |        |        |       |           |     |      |        | withleakedinformation. |                                          |     | InAAAI,2018. |     |     |     |
DennyZhou,DaphneIppolito,DavidLuan,Hyeontaek
| Lim,       | Barret | Zoph, Alexander |     | Spiridonov, |      | Ryan      | Sepa- |         |          |         |           |          |     |        |
| ---------- | ------ | --------------- | --- | ----------- | ---- | --------- | ----- | ------- | -------- | ------- | --------- | -------- | --- | ------ |
|            |        |                 |     |             |      |           |       | William | H. Guss, | Brandon | Houghton, | Nicholay |     | Topin, |
| ssi, David | Dohan, | Shivani         |     | Agrawal,    | Mark | Omernick, |       |         |          |         |           |          |     |        |
PhillipWang,CaydenCodel,ManuelaVeloso,andRus-
AndrewM.Dai,ThanumalayanSankaranarayanaPillai,
|     |     |     |     |     |     |     |     | lan Salakhutdinov. |     | MineRL: |     | A large-scale | dataset | of  |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | ------- | --- | ------------- | ------- | --- |
MariePellat,AitorLewkowycz,EricaMoreira,Rewon
|     |     |     |     |     |     |     |     | Minecraftdemonstrations. |     |     | InIJCAI,2019. |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | ------------- | --- | --- | --- |
Child,OleksandrPolozov,KatherineLee,ZongweiZhou,
XuezhiWang,BrennanSaeta,MarkDiaz,OrhanFirat, DanijarHafner,TimothyLillicrap,IanFischer,RubenVille-
MicheleCatasta,JasonWei,KathyMeier-Hellstern,Dou- gas,DavidHa,HonglakLee,andJamesDavidson.Learn-
| glasEck,JeffDean,SlavPetrov,andNoahFiedel. |     |     |     |     |     |     | PaLM: |     |     |     |     |     | InICML, |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | ------- | --- |
inglatentdynamicsforplanningfrompixels.
| Scaling | language | modeling |     | with | pathways. | JMLR, | 24  | 2019. |     |     |     |     |     |     |
| ------- | -------- | -------- | --- | ---- | --------- | ----- | --- | ----- | --- | --- | --- | --- | --- | --- |
(240):1–113,2023.
|     |     |     |     |     |     |     |     | Danijar | Hafner, | Jurgis Pasukonis, |     | Jimmy | Ba, and | Timo- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------- | ----------------- | --- | ----- | ------- | ----- |
KarlCobbe,VineetKosaraju,MohammadBavarian,Mark thyLillicrap. Masteringdiversedomainsthroughworld
| Chen, | Heewoo | Jun, | Lukasz | Kaiser, | Matthias | Plappert, |     |         |                        |     |     |     |     |     |
| ----- | ------ | ---- | ------ | ------- | -------- | --------- | --- | ------- | ---------------------- | --- | --- | --- | --- | --- |
|       |        |      |        |         |          |           |     | models. | arXiv:2301.04104,2023. |     |     |     |     |     |
JerryTworek,JacobHilton,ReiichiroNakano,Christo-
pher Hesse, and John Schulman. Training verifiers to ShiboHao,YiGu,HaodiMa,JoshuaJiahuaHong,Zhen
|                        |     |     |     |                        |     |     |     | Wang,                                      | Daisy | Zhe Wang, | and | Zhiting Hu. | Reasoning |     |
| ---------------------- | --- | --- | --- | ---------------------- | --- | --- | --- | ------------------------------------------ | ----- | --------- | --- | ----------- | --------- | --- |
| solvemathwordproblems. |     |     |     | arXiv:2110.14168,2021. |     |     |     |                                            |       |           |     |             |           |     |
|                        |     |     |     |                        |     |     |     | withlanguagemodelisplanningwithworldmodel. |       |           |     |             |           | In  |
XiangDeng,YuGu,BoyuanZheng,ShijieChen,Samuel
EMNLP,2023.
| Stevens,BoshiWang,HuanSun,andYuSu. |     |     |     |     |     | Mind2Web: |     |     |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
Towards a generalist agent for the web. In NeurIPS JieHuang,XinyunChen,SwaroopMishra,HuaixiuSteven
Zheng,AdamsWeiYu,XinyingSong,andDennyZhou.
DatasetsandBenchmarksTrack,2023.
Largelanguagemodelscannotself-correctreasoningyet.
DannyDriess,FeiXia,MehdiS.M.Sajjadi,CoreyLynch,
InICLR,2024.
| Aakanksha |     | Chowdhery, | Brian | Ichter, | Ayzaan |     | Wahid, |     |     |     |     |     |     |     |
| --------- | --- | ---------- | ----- | ------- | ------ | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
JonathanTompson, QuanVuong, TianheYu, Wenlong Wenlong Huang, F. Xia, Ted Xiao, Harris Chan, Jacky
Huang,YevgenChebotar,PierreSermanet,DanielDuck- Liang,PeterR.Florence,AndyZeng,JonathanTompson,
worth,SergeyLevine,VincentVanhoucke,KarolHaus- IgorMordatch,YevgenChebotar,PierreSermanet,Noah
man,MarcToussaint,KlausGreff,AndyZeng,IgorMor- Brown,TomasJackson,LindaLuu,SergeyLevine,Karol
datch,andPeteFlorence. PaLM-E:Anembodiedmulti- Hausman,andBrianIchter. Innermonologue: Embodied
modallanguagemodel. InICML,2023. reasoning through planning with language models. In
CoRL,2022.
| Yilun Du, | Mengjiao | Yang, |     | Bo Dai, | Hanjun | Dai, | Ofir |     |     |     |     |     |     |     |
| --------- | -------- | ----- | --- | ------- | ------ | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
Nachum,JoshuaB.Tenenbaum,DaleSchuurmans,and
|     |     |     |     |     |     |     |     | LeventeKocsisandCsabaSzepesva´ri. |     |     |     | Banditbasedmonte- |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --- | ----------------- | --- | --- |
PieterAbbeel.Learninguniversalpoliciesviatext-guided carloplanning. InECML,2006.
| videogeneration. |     | InNeurIPS,2023. |     |     |     |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
TakeshiKojima,ShixiangShaneGu,MachelReid,Yutaka
| Jonathan | St BT | Evans. | Intuition | and | reasoning: |     | A dual- |                          |     |     |     |                     |     |     |
| -------- | ----- | ------ | --------- | --- | ---------- | --- | ------- | ------------------------ | --- | --- | --- | ------------------- | --- | --- |
|          |       |        |           |     |            |     |         | Matsuo,andYusukeIwasawa. |     |     |     | Largelanguagemodels |     |     |
processperspective. PsychologicalInquiry,pages313– arezero-shotreasoners. InNeurIPS,2022.
326,2010.
|     |     |     |     |     |     |     |     | Steven M. | LaValle. | Rapidly-exploring |     | random | trees | : A |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | -------- | ----------------- | --- | ------ | ----- | --- |
LinxiFan,GuanzhiWang,YunfanJiang,AjayMandlekar, newtoolforpathplanning. TheAnnualResearchReport,
YuncongYang,HaoyiZhu,AndrewTang,De-AnHuang,
1998.
| YukeZhu,andAnimaAnandkumar. |     |     |     |     | MineDojo: | Building |     |     |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | --- | --------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
open-endedembodiedagentswithinternet-scaleknowl- EvanZheranLiu,KelvinGuu,PanupongPasupat,Tianlin
edge. InNeurIPSDatasetsandBenchmarksTrack,2022. Shi, andPercyLiang. Reinforcementlearningonweb
|     |     |     |     |     |     |     |     | interfacesusingworkflow-guidedexploration. |     |     |     |     |     | InICLR, |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | ------- |
HirokiFuruta,OfirNachum,Kuang-HueiLee,YutakaMat-
2018.
| suo,ShixiangShaneGu,andIzzeddinGur. |     |     |     |     |     | Multimodal |     |     |     |     |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
web navigation with instruction-finetuned foundation Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu
models. InICLR,2024. Lei,HanyuLai,YuGu,HangliangDing,KaiwenMen,
11

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
KejuanYang,ShudanZhang,XiangDeng,AohanZeng, DavidSilver,AjaHuang,ChrisJ.Maddison,ArthurGuez,
Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun L.Sifre,GeorgevandenDriessche,JulianSchrittwieser,
Zhang,YuSu,HuanSun,MinlieHuang,YuxiaoDong, Ioannis Antonoglou, Vedavyas Panneershelvam, Marc
andJieTang. AgentBench: EvaluatingLLMsasagents. Lanctot,SanderDieleman,DominikGrewe,JohnNham,
InICLR,2024. NalKalchbrenner,IlyaSutskever,TimothyP.Lillicrap,
MadeleineLeach,KorayKavukcuoglu,ThoreGraepel,
| ZhihanLiu, | HaoHu, | ShenaoZhang, |     | HongyiGuo, |     | Shuqi |     |     |     |     |     |     |     |
| ---------- | ------ | ------------ | --- | ---------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
andDemisHassabis.MasteringthegameofGowithdeep
| Ke, Boyi | Liu,    | and  | Zhaoran      | Wang.     | Reason | for fu- |                              |     |     |     |                     |     |     |
| -------- | ------- | ---- | ------------ | --------- | ------ | ------- | ---------------------------- | --- | --- | --- | ------------------- | --- | --- |
|          |         |      |              |           |        |         | neuralnetworksandtreesearch. |     |     |     | Nature,529:484–489, |     |     |
| ture,    | act for | now: | A principled | framework |        | for au- |                              |     |     |     |                     |     |     |
2016.
tonomousLLMagentswithprovablesampleefficiency.
arXiv:2309.17382,2023. DavidSilver,AjaHuang,ChrisJ.Maddison,ArthurGuez,
L.Sifre,GeorgevandenDriessche,JulianSchrittwieser,
AmanMadaan,NiketTandon,PrakharGupta,SkylerHal-
|        |      |            |            |     |           |       | Ioannis | Antonoglou, |     | Vedavyas | Panneershelvam, |     | Marc |
| ------ | ---- | ---------- | ---------- | --- | --------- | ----- | ------- | ----------- | --- | -------- | --------------- | --- | ---- |
| linan, | Luyu | Gao, Sarah | Wiegreffe, |     | Uri Alon, | Nouha |         |             |     |          |                 |     |      |
Lanctot,SanderDieleman,DominikGrewe,JohnNham,
| Dziri, | Shrimai | Prabhumoye, |     | Yiming | Yang, | Shashank |     |     |     |     |     |     |     |
| ------ | ------- | ----------- | --- | ------ | ----- | -------- | --- | --- | --- | --- | --- | --- | --- |
Gupta, Bodhisattwa Prasad Majumder, Katherine Her- NalKalchbrenner,IlyaSutskever,TimothyP.Lillicrap,
MadeleineLeach,KorayKavukcuoglu,ThoreGraepel,
| mann, | Sean | Welleck, | Amir | Yazdanbakhsh, |     | and Peter |                   |     |                               |     |     |     |     |
| ----- | ---- | -------- | ---- | ------------- | --- | --------- | ----------------- | --- | ----------------------------- | --- | --- | --- | --- |
|       |      |          |      |               |     |           | andDemisHassabis. |     | MasteringchessandShogibyself- |     |     |     |     |
Clark.Self-refine:Iterativerefinementwithself-feedback.
|     |     |     |     |     |     |     | play with | a general | reinforcement |     | learning |     | algorithm. |
| --- | --- | --- | --- | --- | --- | --- | --------- | --------- | ------------- | --- | -------- | --- | ---------- |
InNeurIPS,2023.
arXiv:1712.01815,2017.
RameshNallapati,BowenZhou,CicerodosSantos,Caglar
|                        |     |     |     |                           |     |     | StevenA.Sloman. |     | Theempiricalcasefortwosystemsof |     |     |     |     |
| ---------------------- | --- | --- | --- | ------------------------- | --- | --- | --------------- | --- | ------------------------------- | --- | --- | --- | --- |
| Gulcehre,andBingXiang. |     |     |     | Abstractivetextsummariza- |     |     |                 |     |                                 |     |     |     |     |
tionusingsequence-to-sequenceRNNsandbeyond. In reasoning. PsychologicalBulletin,119:3–22,1996.
SpecialInterestGrouponNaturalLanguageLearning,
HaotianSun,YuchenZhuang,LingkaiKong,BoDai,and
2016.
|     |     |     |     |     |     |     | ChaoZhang. | AdaPlanner: |     | Adaptiveplanningfromfeed- |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ----------- | --- | ------------------------- | --- | --- | --- |
OpenAI. GPT-4technicalreport. arXiv:2303.08774,2023. backwithlanguagemodels. InNeurIPS,2023.
| Yujia Qin, | Shihao | Liang, | Yining | Ye, | Kunlun | Zhu, Lan |                                           |     |     |     |     |           |     |
| ---------- | ------ | ------ | ------ | --- | ------ | -------- | ----------------------------------------- | --- | --- | --- | --- | --------- | --- |
|            |        |        |        |     |        |          | D´ıdacSur´ıs,SachitMenon,andCarlVondrick. |     |     |     |     | ViperGPT: |     |
Yan,YaxiLu,YankaiLin,XinCong,XiangruTang,Bill VisualinferenceviaPythonexecutionforreasoning. In
Qian,SihanZhao,RunchuTian,RuobingXie,JieZhou,
ICCV,2023.
MarkGerstein,DahaiLi,ZhiyuanLiu,andMaosongSun.
ToolLLM:Facilitatinglargelanguagemodelstomaster MaciejSwiechowski,KonradGodlewski,BartoszSawicki,
16000+real-worldAPIs. InICLR,2024. and Jacek Ma’ndziuk. Monte Carlo tree search: A re-
|                         |     |     |     |                         |     |     | viewofrecentmodificationsandapplications. |     |     |     |     |     | Artificial |
| ----------------------- | --- | --- | --- | ----------------------- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | ---------- |
| AbulhairSaparovandHeHe. |     |     |     | Languagemodelsaregreedy |     |     |                                           |     |     |     |     |     |            |
IntelligenceReview,56:2497–2562,2021.
| reasoners: | A   | systematic | formal | analysis | of  | chain-of- |     |     |     |     |     |     |     |
| ---------- | --- | ---------- | ------ | -------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
thought. InICLR,2023. Hugo Touvron, Louis Martin, Kevin R. Stone, Peter Al-
bert,AmjadAlmahairi,YasmineBabaei,NikolayBash-
| Timo Schick, | Jane | Dwivedi-Yu, |     | Roberto | Dess`ı, | Roberta |               |     |        |          |           |        |       |
| ------------ | ---- | ----------- | --- | ------- | ------- | ------- | ------------- | --- | ------ | -------- | --------- | ------ | ----- |
|              |      |             |     |         |         |         | lykov, Soumya |     | Batra, | Prajjwal | Bhargava, | Shruti | Bhos- |
Raileanu,MariaLomeli,LukeZettlemoyer,NicolaCan-
|        |            |     |          |             |            |          | ale, Daniel  | M.    | Bikel,  | Lukas Blecher, |     | Cristian | Canto´n |
| ------ | ---------- | --- | -------- | ----------- | ---------- | -------- | ------------ | ----- | ------- | -------------- | --- | -------- | ------- |
| cedda, | and Thomas |     | Scialom. | Toolformer: |            | Language |              |       |         |                |     |          |         |
|        |            |     |          |             | InNeurIPS, |          | Ferrer, Moya | Chen, | Guillem | Cucurull,      |     | David    | Esiobu, |
modelscanteachthemselvestousetools.
|     |     |     |     |     |     |     | Jude Fernandes, |     | Jeremy | Fu, Wenyin |     | Fu, Brian | Fuller, |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------ | ---------- | --- | --------- | ------- |
2023.
|     |     |     |     |     |     |     | Cynthia | Gao, Vedanuj |     | Goswami, | Naman | Goyal, | An- |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------ | --- | -------- | ----- | ------ | --- |
Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, thony S. Hartshorn, Saghar Hosseini, Rui Hou, Hakan
WeimingLu,andYuetingZhuang.HuggingGPT:Solving Inan,MarcinKardas,ViktorKerkez,MadianKhabsa,Is-
AItaskswithChatGPTanditsfriendsinHuggingFace.
|     |     |     |     |     |     |     | abelM.Kloumann, |     | A.V.Korenev, |     | PunitSinghKoura, |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------------ | --- | ---------------- | --- | --- |
InNeurIPS,2023. Marie-AnneLachaux,ThibautLavril,JenyaLee,Diana
|             |          |     |          |      |         |        | Liskovich, | Yinghai | Lu, | Yuning | Mao, | Xavier | Martinet, |
| ----------- | -------- | --- | -------- | ---- | ------- | ------ | ---------- | ------- | --- | ------ | ---- | ------ | --------- |
| Noah Shinn, | Federico |     | Cassano, | Beck | Labash, | Ashwin |            |         |     |        |      |        |           |
TodorMihaylov,PushkarMishra,IgorMolybog,Yixin
| Gopinath,KarthikNarasimhan,andShunyuYao. |     |     |     |     |     | Reflex- |     |     |     |     |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
Nie,AndrewPoulton,JeremyReizenstein,RashiRungta,
ion: Languageagentswithverbalreinforcementlearning.
KalyanSaladi,AlanSchelten,RuanSilva,EricMichael
InNeurIPS,2023.
|     |     |     |     |     |     |     | Smith, | R. Subramanian, |     | Xia | Tan, Binh | Tang, | Ross |
| --- | --- | --- | --- | --- | --- | --- | ------ | --------------- | --- | --- | --------- | ----- | ---- |
Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Coˆte´, Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu,
YonatanBisk,AdamTrischler,andMatthewHausknecht. ZhengxuYan,IliyanZarov,YuchenZhang,AngelaFan,
ALFWorld: Aligning text and embodied environments MelanieKambadur,SharanNarang,AurelienRodriguez,
forinteractivelearning. InICLR,2020. Robert Stojnic, Sergey Edunov, and Thomas Scialom.
12

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
Llama2: Openfoundationandfine-tunedchatmodels. DennyZhou,NathanaelScha¨rli,LeHou,JasonWei,Nathan
arXiv:2307.09288,2023. Scales,XuezhiWang,DaleSchuurmans,OlivierBous-
|                |     |          |              |     |     |        |       | quet, Quoc                                    | Le, and Ed Chi. | Least-to-most | prompting |
| -------------- | --- | -------- | ------------ | --- | --- | ------ | ----- | --------------------------------------------- | --------------- | ------------- | --------- |
| Tom Vodopivec, |     | Spyridon | Samothrakis, |     | and | Branko | Ster. |                                               |                 |               |           |
|                |     |          |              |     |     |        |       | enablescomplexreasoninginlargelanguagemodels. |                 |               | In        |
OnMonteCarlotreesearchandreinforcementlearning.
ICLR,2022.
JournalofArtificialIntelligenceResearch,60:881–936,
| 2017. |     |     |     |     |     |     |     | YuchenZhuang,XiangChen,TongYu,SaayanMitra,Victor |           |                 |          |
| ----- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --------- | --------------- | -------- |
|       |     |     |     |     |     |     |     | Bursztyn, Ryan                                   | A. Rossi, | Somdeb Sarkhel, | and Chao |
GuanzhiWang,YuqiXie,YunfanJiang,AjayMandlekar,
|     |     |     |     |     |     |     |     | Zhang. ToolChain*: | Efficientactionspacenavigationin |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | -------------------------------- | --- | --- |
ChaoweiXiao,YukeZhu,LinxiFan,andAnimaAnand-
|                                          |          |                               |                        |                  |     |          |     | largelanguagemodelswithA*search. |     | InICLR,2023. |     |
| ---------------------------------------- | -------- | ----------------------------- | ---------------------- | ---------------- | --- | -------- | --- | -------------------------------- | --- | ------------ | --- |
| kumar.                                   | Voyager: | Anopen-endedembodiedagentwith |                        |                  |     |          |     |                                  |     |              |     |
| largelanguagemodels.                     |          |                               | arXiv:2305.16291,2023. |                  |     |          |     |                                  |     |              |     |
| Xuezhi                                   | Wang,    | Jason Wei,                    | Dale                   | Schuurmans,      |     | Quoc     | Le, |                                  |     |              |     |
| Ed Chi,                                  | and      | Denny                         | Zhou.                  | Self-consistency |     | improves |     |                                  |     |              |     |
| chainofthoughtreasoninginlanguagemodels. |          |                               |                        |                  |     | InICLR,  |     |                                  |     |              |     |
2022.
| Jason Wei,                             | Xuezhi          | Wang,   | Dale      | Schuurmans, |          | Maarten     |     |     |     |     |     |
| -------------------------------------- | --------------- | ------- | --------- | ----------- | -------- | ----------- | --- | --- | --- | --- | --- |
| Bosma,                                 | Ed Chi,         | Quoc    | Le, and   | Denny       | Zhou.    | Chain       | of  |     |     |     |     |
| thought                                | prompting       | elicits | reasoning |             | in large | language    |     |     |     |     |     |
| models.                                | InNeurIPS,2022. |         |           |             |          |             |     |     |     |     |     |
| MichaelWooldridgeandNicholasRJennings. |                 |         |           |             |          | Intelligent |     |     |     |     |     |
agents:Theoryandpractice.TheKnowledgeEngineering
Review,10:115–152,1995.
PhilippWu,AlejandroEscontrela,DanijarHafner,Pieter
| Abbeel,andKenGoldberg.    |         |            |              | Daydreamer: | Worldmodels   |       |      |     |     |     |     |
| ------------------------- | ------- | ---------- | ------------ | ----------- | ------------- | ----- | ---- | --- | --- | --- | --- |
| forphysicalrobotlearning. |         |            | InCoRL,2023. |             |               |       |      |     |     |     |     |
| Yuxi Xie,                 | Kenji   | Kawaguchi, | Yiran        | Zhao,       | Xu            | Zhao, | Min- |     |     |     |     |
| Yen Kan,                  | Junxian | He,        | and Qizhe    | Xie.        | Decomposition |       |      |     |     |     |     |
enhancesreasoningviaself-evaluationguideddecoding.
arXiv:2305.00633,2023.
| Zhilin Yang,   | Peng      | Qi,                             | Saizheng | Zhang,     | Yoshua | Bengio,     |     |     |     |     |     |
| -------------- | --------- | ------------------------------- | -------- | ---------- | ------ | ----------- | --- | --- | --- | --- | --- |
| WilliamWCohen, |           | RuslanSalakhutdinov,            |          |            |        | andChristo- |     |     |     |     |     |
| pherDManning.  |           | HotpotQA:Adatasetfordiverse,ex- |          |            |        |             |     |     |     |     |     |
| plainable      | multi-hop |                                 | question | answering. |        | In EMNLP,   |     |     |     |     |     |
2018.
| Shunyu                                 | Yao, Howard | Chen,                                |     | John Yang, | and | Karthik    | R   |     |     |     |     |
| -------------------------------------- | ----------- | ------------------------------------ | --- | ---------- | --- | ---------- | --- | --- | --- | --- | --- |
| Narasimhan.                            |             | WebShop:Towardsscalablereal-worldweb |     |            |     |            |     |     |     |     |     |
| interactionwithgroundedlanguageagents. |             |                                      |     |            |     | InNeurIPS, |     |     |     |     |     |
2022.
| Shunyu | Yao, | Dian Yu, | Jeffrey | Zhao, | Izhak | Shafran, |     |     |     |     |     |
| ------ | ---- | -------- | ------- | ----- | ----- | -------- | --- | --- | --- | --- | --- |
ThomasL.Griffiths,YuanCao,andKarthikNarasimhan.
| Treeofthoughts: |     | deliberateproblemsolvingwithlarge |     |     |     |     |     |     |     |     |     |
| --------------- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| languagemodels. |     | InNeurIPS,2023a.                  |     |     |     |     |     |     |     |     |     |
ShunyuYao,JeffreyZhao,DianYu,NanDu,IzhakShafran,
| KarthikNarasimhan,andYuanCao. |     |     |     |     | ReAct: | Synergizing |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | --- | ------ | ----------- | --- | --- | --- | --- | --- |
reasoningandactinginlanguagemodels.InICLR,2023b.
WeiruiYe,ShaohuaiLiu,ThanardKurutach,PieterAbbeel,
| andYangGao. |     | MasteringAtarigameswithlimiteddata. |     |     |     |     |     |     |     |     |     |
| ----------- | --- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
InNeurIPS,2021.
13

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
AppendixofLATS noting that this is cheaper than the inference cost associ-
atedwithusingLMsasworldmodels,asinprevioussearch
| Theappendixisorganizedasfollows. |     | FirstinSec.A,we |     |     |     |     |     |     |     |     |
| -------------------------------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
approaches(Haoetal.,2023;Liuetal.,2023).
showthepseudocodeofourproposedalgorithm,LATS.In
Sec.B,weprovidefurtherdiscussionofthelimitationsof Assumption of environment reversion in decision-
ourmethod. InSec.C,wepresentadditionalexperimental making. Since our method is based on Monte Carlo
results. InSec.D,wespecifytheenvironmentdetailsinour TreeSearchandismodel-free,onelimitationofLATSon
|                                                      |     |     |     | decision-making | tasks | is  | that it requires |     | the agent | to be |
| ---------------------------------------------------- | --- | --- | --- | --------------- | ----- | --- | ---------------- | --- | --------- | ----- |
| experiments. Finally,welistourpromptsusedforthethree |     |     |     |                 |       |     |                  |     |           |       |
environmentsinSec.E(HotPotQA),Sec.F(Programming), able to revert to earlier states in the environments. How-
andSec.G(WebShop),respectively. ever,thisreversionpropertyisfeasibleinmanyreal-world
|     |     |     |     | environments     | and applications |              | (despite       |     | being not | univer-   |
| --- | --- | --- | --- | ---------------- | ---------------- | ------------ | -------------- | --- | --------- | --------- |
|     |     |     |     | sally applicable | in               | all possible | environments), |     |           | including |
A.LATSPseudocode
programming(HumanEval(Chenetal.,2021)),websearch
Alg.1showsthepseudocodeofouralgorithmLATS.Nodes (WebShop(Yaoetal.,2022)),text-basedmanipulationtasks
arestoredexplicitlyinthememory. Unlessotherwisespeci- (Alfworld(Shridharetal.,2020)),andLMswithtooluse
fied,inallexperiments,wesetthenumberofsamplednodes (ToolBench(Qinetal.,2024)). Therefore,webelievethat
to n = 5 and the exploration weight to w = 1. We use leveragingthereversionpropertyisnotashortcomingbut
|                    |           |                      |     | rather a feature | that | has not | been | explicitly | given | notice |
| ------------------ | --------- | -------------------- | --- | ---------------- | ---- | ------- | ---- | ---------- | ----- | ------ |
| a self-consistency | weight of | λ = 0.5 for HotPotQA | and |                  |      |         |      |            |       |        |
Gameof24,andλ=0.8forProgrammingandWebShop. bytheLMdecision-makingcommunity–itopensupnew
opportunitiesintheemergingLMagentcommunity.
B.MoreDiscussiononLimitations
Additionally,thebenchmarksweuseinthispaperarerel-
ativelysimpleandfocusedondecision-makingcompared
AsstatedinSec.6,LATShastwomainlimitations: to the complexity of real-world interactive environments.
Computational cost. Although LATS can improve rea- Moreover,someenvironmentsmightnoteasilysupportroll-
|     |     |     |     | backstopreviousstates. |     | However,thedesignofLATSis |     |     |     |     |
| --- | --- | --- | --- | ---------------------- | --- | ------------------------- | --- | --- | --- | --- |
soninganddecision-making,thisarrivesatahighercom-
putationalcostrelativetosimplerpromptingmethodslike flexibleandcanbeadjustedtovariousresourceconstraints.
ReActorReflexion. However,thefollowingfactsserveas Using planning-based prompting methods like LATS in
environmentslikeMinecraft(Fanetal.,2022)andmorerea-
mitigationstothisissue:
soningbenchmarkswouldbeinterestingavenuesforfuture
work.
• Asymptotically,ourmethodhasthesamesamplecom-
plexityasToT(Yaoetal.,2023a)andRAP(Haoetal.,
2023),butachievesbetterperformance,expandsfewer C.AdditionalAblations
nodes,andusesfewertokensonaverageuponsuccess.
|                                              |          |                    |          | In this section, | we            | ablate | various  | designs | of LATS. | Ex-     |
| -------------------------------------------- | -------- | ------------------ | -------- | ---------------- | ------------- | ------ | -------- | ------- | -------- | ------- |
| This suggests                                | that our | method is not only | stronger |                  |               |        |          |         |          |         |
|                                              |          |                    |          | periments        | are conducted | on     | HotPotQA |         | with a   | maximum |
| inproblem-solvingbutalsohashigherefficiency. |          |                    | A        |                  |               |        |          |         |          |         |
|                                              |          |                    |          | of k = 50        | trajectories  | and    | sampling | size    | of n     | = 5 and |
fullanalysisofthecostcanbefoundinTab.9inAp-
|     |     |     |     | HumanEvalwithamaximumofk |     |     |     | =8trajectoriesandsam- |     |     |
| --- | --- | --- | --- | ------------------------ | --- | --- | --- | --------------------- | --- | --- |
pendixC.
|     |     |     |     | plingsizeofn=5. |     | TheresultforHotPotQAisshownin |     |     |     |     |
| --- | --- | --- | --- | --------------- | --- | ----------------------------- | --- | --- | --- | --- |
Tab.8andHumanEvalinFig.3.
• Thenumberofnodesnexpandedateverystepprovides
anaturaltrade-offbetweenperformanceandefficiency. Exploration weight. We find that there is lower perfor-
In fact, setting n = 1 makes the method as efficient manceonHotPotQAwhentheexplorationweightwinthe
as ReAct (Yao et al., 2023b) with multiple trials or selectionformulaisdecreasedto0.5,suggestingthatthis
CoT-SC(Wangetal.,2022). reducestheeffectivenessofthesearch. Increasingwto2.0
doesnotleadtoaperformanceimprovement,butwetend
|     |     |     |     | toobservefasterconvergence. |     |     | Theoptimalsettingdepends |     |     |     |
| --- | --- | --- | --- | --------------------------- | --- | --- | ------------------------ | --- | --- | --- |
Ingeneral,werecommendusingLATSfordifficulttasks
ontheparticularenvironmentandcomplexityofthestate
| like programming | or for situations | where performance | is  |     |     |     |     |     |     |     |
| ---------------- | ----------------- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
space.
| prioritizedoverefficiencyinpractice. |     | Wehopethatcontin- |     |     |     |     |     |     |     |     |
| ------------------------------------ | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
uedadvancementsinLMswillreducecostsandincrease
|     |     |     |     | Depth. Inourmainexperimentsweuseamaximumdepth |     |     |     |     |     |     |
| --- | --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- | --- |
theapplicabilityofLATS. ofd=7onHotPotQAforallmethods,followingprevious
|     |     |     |     | work(Yaoetal.,2023b). |     | WeablatetheeffectonLATSafter |     |     |     |     |
| --- | --- | --- | --- | --------------------- | --- | ---------------------------- | --- | --- | --- | --- |
Additionally,thereexistsaminorcostfromqueryingtheen-
|     |     |     |     | reducingittod | =   | 4. Thisresultsinonlyaslightdropin |     |     |     |     |
| --- | --- | --- | --- | ------------- | --- | --------------------------------- | --- | --- | --- | --- |
vironment,whichwefindtobetrivialfortheenvironments
|     |     |     |     | performance. | Wefindthatmostquestionscanbeanswered |     |     |     |     |     |
| --- | --- | --- | --- | ------------ | ------------------------------------ | --- | --- | --- | --- | --- |
westudy. MostLM-basedenvironmentsinvolveAPI-based
tools,whichareinexpensiveandfasttouse. Itisalsoworth withinfoursteps,andusingagreaternumberofstepstends
14

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
| Algorithm1LATS(s,p |     |     | ,p  | ,p ,d,k,n,w,a,b) |     |     |     |     |     |     |     |     |
| ------------------ | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|                    |     |     | θ   | V ref            |     |     |     |     |     |     |     |     |
Require: Initialstates,actiongeneratorp θ ,valuefunctionp V ,reflectiongeneratorp ref ,numberofgeneratedactionsn,
depthlimitL,numberofroll-outsK,contextc,explorationweightw,andvaluefunctionweightλ
InitializeactionspaceA,observationspaceO
|     |                                         |     |     |     | :S×A(cid:55)→RandvisitcounterN |     |     |     | (cid:55)→Ntoone |     |     |     |
| --- | --------------------------------------- | --- | --- | --- | ------------------------------ | --- | --- | --- | --------------- | --- | --- | --- |
|     | Initializethestate-actionvaluefunctionp |     |     |     | V                              |     |     |     | :S              |     |     |     |
fork←0,...,K−1do
fort←0,...,L−1do
|     |     | ifs | t notterminalthen |     |     |     |     |     |     | ▷Expansion&Simulation |     |     |
| --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- |
fori←1,...,ndo
|     |     |     | Samplea(i)                  | ∼p (s | )                     |                        |       |     |              |     |             |     |
| --- | --- | --- | --------------------------- | ----- | --------------------- | ---------------------- | ----- | --- | ------------ | --- | ----------- | --- |
|     |     |     |                             | t θ t |                       |                        |       |     |              |     |             |     |
|     |     |     | Geto(i)fromenvironment,s(i) |       |                       | ←(c(i),o(i),a(i)),c(i) |       |     | ←(o(i),a(i)) |     |             |     |
|     |     |     |                             | t     | t+1                   |                        | t t t | t+1 | t t          |     |             |     |
|     |     |     | EvaluateV(i)                | ∼λ∗p  | (s(i))+(1−λ)∗SC(s(i)) |                        |       |     |              |     | ▷Evaluation |     |
|     |     |     |                             | t     | V t                   |                        | t     |     |              |     |             |     |
|     |     |     | V(s )←V(i)                  |       |                       |                        |       |     |              |     |             |     |
|     |     |     | t                           | t     |                       |                        |       |     |              |     |             |     |
Adds(i)tochildren
t
endfor
endif
|     |     | ifs | isterminalthen |     |     |     |     |     |     |     | ▷Reflection |     |
| --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- |
t
Getrfromenvironment
ifrnotsuccessthen
|     |     |     | reflection←p | (c ) |     |     |     |     |     |     |     |     |
| --- | --- | --- | ------------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
ref t
c←reflection
endif
endif
|     |     |                   |                           | (cid:104)    | (cid:113) |         | (cid:105) |     |      |     |            |     |
| --- | --- | ----------------- | ------------------------- | ------------ | --------- | ------- | --------- | --- | ---- | --- | ---------- | --- |
|     |     | a                 | ←argmax                   | V(s          | )+w       | lnN(st) |           |     |      |     | ▷Selection |     |
|     |     | t                 |                           | a∈e(st) t    |           | N(st+1) |           |     |      |     |            |     |
|     |     | Getcorrespondingo |                           | frommemory,s |           | ←(c     | ,o ,a ),c | ←(o | ,a ) |     |            |     |
|     |     |                   |                           | t            |           | t+1     | t t t     | t+1 | t t  |     |            |     |
|     |     | N(s               | )←N(s                     | )+1          |           |         |           |     |      |     |            |     |
|     |     |                   | t+1                       | t+1          |           |         |           |     |      |     |            |     |
|     |     | ifa               | isanoutputactionthenbreak |              |           |         |           |     |      |     |            |     |
t
endfor
T ←theactualnumberofsteps
|     |     | fort←T | −1,...,0do          |       |     |     |     |     |     |     | ▷Backpropagation |     |
| --- | --- | ------ | ------------------- | ----- | --- | --- | --- | --- | --- | --- | ---------------- | --- |
|     |     | V(s    | )← V(st)(N(st)−1)+r |       |     |     |     |     |     |     |                  |     |
|     |     |        | t                   | N(st) |     |     |     |     |     |     |                  |     |
endfor
endfor
to force the agent into local minima and rarely improves based question-answer pairs crafted by crowdworkers to
| success. |     |     |     |     |     |     | bediverse,multi-hop,andexplainable. |     |     |     | Questionscovera |     |
| -------- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | --------------- | --- |
rangeoftypeslikeentities,locations,dates,andcomparison
| LMvaluefunction. |             |     | TheLMvaluefunctionscoresstates |                 |      |            |                                       |     |     |     |              |     |
| ---------------- | ----------- | --- | ------------------------------ | --------------- | ---- | ---------- | ------------------------------------- | --- | --- | --- | ------------ | --- |
|                  |             |     |                                |                 |      |            | ofsharedpropertiesbetweentwoentities. |     |     |     | Crowdworkers |     |
| based            | on expected |     | future                         | reward. Without | this | heuristic, |                                       |     |     |     |              |     |
alsoprovidesupportingfactsfromthedocumentsthatjustify
theonlysignaltoguidesearchwouldbefromenvironment
|              |     |                                       |               |       |            |     | theanswer.                                |     | WeusetheHotPotQAbenchmarksettingwith |     |            |     |
| ------------ | --- | ------------------------------------- | ------------- | ----- | ---------- | --- | ----------------------------------------- | --- | ------------------------------------ | --- | ---------- | --- |
| rewards      | for | completed                             | trajectories, | which | are scarce | and |                                           |     |                                      |     |            |     |
|              |     |                                       |               |       |            |     | alltheWikipediaparagraphstotestretrieval. |     |                                      |     | Weusearan- |     |
| oftenbinary. |     | Whenweremovetheevaluationoperation,we |               |       |            |     |                                           |     |                                      |     |            |     |
domlyselectedsubsetof100questionsforourexperiments
observeadramatic0.26dropinperformance.
|     |     |     |     |     |     |     | and | a maximum | depth limit | of 6. | Fig. 4 illustrates | how |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ----------- | ----- | ------------------ | --- |
Performanceovertime. Toseetheeffectsofincreasing ReActandLATSworkonanexampletaskofHotPotQA,
thenumberoftrajectoriessampled,wechangektodifferent andgivesaqualitativeexampleonhowLATSoutperforms
values. WeconductthisexperimentonHumanEval,which ReActonthetask. Forvaluefunctionhyperparameters,we
hasamorenoticeabledifferenceduetosamplinglesstra- useλ=0.5fortheLMscoreandself-consistencyscore.
| jectories. |     | TheresultsareshowninFig. |     | 3,inwhichLATS |     |     |              |     |                                   |     |     |     |
| ---------- | --- | ------------------------ | --- | ------------- | --- | --- | ------------ | --- | --------------------------------- | --- | --- | --- |
|            |     |                          |     |               |     |     | ActionSpace. |     | WeadopttheWikipediawebAPIproposed |     |     |     |
scalesbetterwithmoreiterationsthanReflexion.
inYaoetal.(2023b),withthreetypesofactionstosupport
interactiveinformationretrieval:
D.EnvironmentDetails
(1)search[entity],whichreturnsthefirst5sentences
D.1.HotPotQA from the corresponding entity wiki page if it exists,
orelsesuggeststop-5similarentitiesfromtheWikipedia
| HotPotQA |     | (Yang | et al., 2018) | is a question-answering |     |     |     |     |     |     |     |     |
| -------- | --- | ----- | ------------- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
searchengine,
| dataset | that | requires | reasoning | over multiple | supporting |     |     |     |     |     |     |     |
| ------- | ---- | -------- | --------- | ------------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
(2)lookup[string],whichreturnsthenextsentencein
| documentstoanswerquestions. |     |     |     | Itcontains113kWikipedia- |     |     |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
15

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
|              |     |               |     |     | ifanysamplepassesalltests.              |     |     | Weuseall164problemsfor |     |     |        |
| ------------ | --- | ------------- | --- | --- | --------------------------------------- | --- | --- | ---------------------- | --- | --- | ------ |
|              |     |               |     |     | ourexperimentsandamaximumdepthlimitof8. |     |     |                        |     |     | Forthe |
| PromptMethod |     | HotpotQA(EM)↑ |     |     |                                         |     |     |                        |     |     |        |
threequestionswithoutsampletestcases,wewriteourown.
| LATS(w | =0.5) |     | 0.55 |     |     |     |     |     |     |     |     |
| ------ | ----- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
Forvaluefunctionhyperparameters,weuseλ=0.8forthe
| LATS(w    | =2.0) |     | 0.63 |     |                                  |     |     |     |     |                 |     |
| --------- | ----- | --- | ---- | --- | -------------------------------- | --- | --- | --- | --- | --------------- | --- |
|           |       |     |      |     | LMscoreandself-consistencyscore. |     |     |     |     | ForGPT-3.5weuse |     |
| LATS(d=4) |       |     | 0.58 |     |                                  |     |     |     |     |                 |     |
sixinternaltests,whileforGPT-4weusefourinternaltests.
| LATS(CoT) |     |     | 0.62 |     |     |     |     |     |     |     |     |
| --------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
TheMostlyBasicProgrammingProblems(MBPP)(Austin
| LATS(NoLMHeuristic) |     |     | 0.37 |     |     |     |     |     |     |     |     |
| ------------------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
LATS(w =1.0,d=7) 0.63 etal.,2022)benchmarkcontains974shortPythonfunctions
|     |     |     |     |     | designed | to evaluate | program |     | synthesis | techniques. | The |
| --- | --- | --- | --- | --- | -------- | ----------- | ------- | --- | --------- | ----------- | --- |
Table11.AblationresultsonLATSandbaselinevariantsinHot- dataset was constructed by crowdsourcing from workers
PotQAmeasuredbyExactMatch(EM).Wetestdifferentdepthd, withbasicPythonknowledge. Eachdatapointconsistsof
explorationfactorw,andversionsofLATSusingCoTandwithout a natural language description of a programming task, a
theLMvaluefunction.Wesamplen=5andk=50trajectories.
referencesolutionimplementation,andthreetestcasesfor
|     |     |     |     |     | functionalcorrectness.                   |     |     | Thenaturallanguagepromptsare |     |                |     |
| --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | ---------------------------- | --- | -------------- | --- |
|     |     |     |     |     | typicallyshort,one-sentencedescriptions. |     |     |                              |     | Solutionscover |     |
commonprogrammingconstructsincludingmathematical
operations,listprocessing,stringmanipulation,andusage
|     |     |     |     |     | ofthePythonstandardlibrary. |                                       |     | Onaverage,solutionsare6.8 |     |     |     |
| --- | --- | --- | --- | --- | --------------------------- | ------------------------------------- | --- | ------------------------- | --- | --- | --- |
|     |     |     |     |     | linesofcode.                | Thedatasetisalsosupplementedwithanad- |     |                           |     |     |     |
ditionalsetof426problemsthatweremanuallyverifiedfor
unambiguousspecifications,standardfunctionsignatures,
|     |     |     |     |     | andaccuratetestcases.           |     |        | Weusearandomlyselectedsubset |         |                  |              |
| --- | --- | --- | --- | --- | ------------------------------- | --- | ------ | ---------------------------- | ------- | ---------------- | ------------ |
|     |     |     |     |     | of397problemsforourexperiments. |     |        |                              |         | Forvaluefunction |              |
|     |     |     |     |     | hyperparameters,                |     | we use | λ =                          | 0.8 for | the              | LM score and |
self-consistencyscore.
D.3.WebShop
|     |     |     |     |     | WebShop     | (Yao     | et al., | 2022) is    | an interactive |        | web-based   |
| --- | --- | --- | --- | --- | ----------- | -------- | ------- | ----------- | -------------- | ------ | ----------- |
|     |     |     |     |     | environment | designed |         | to evaluate |                | agents | on grounded |
Figure3.PerformanceoversuccessiveiterationsonHumanEval
|     |     |     |     |     | languageunderstandinganddecision-making. |     |     |     |     |     | Itsimulates |
| --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- | ----------- |
withGPT-3.5.
|     |     |     |     |     | an e-commerce |     | shopping | task | by providing |     | agents with |
| --- | --- | --- | --- | --- | ------------- | --- | -------- | ---- | ------------ | --- | ----------- |
over1millionreal-worldproductsscrapedfromAmazon,
|     |     |     |     |     | spanning | 5 categories |     | and 113 | subcategories. |     | These |
| --- | --- | --- | --- | --- | -------- | ------------ | --- | ------- | -------------- | --- | ----- |
thepagecontainingstring,
|     |     |     |     |     | products | contain | rich | linguistic | information, |     | with an |
| --- | --- | --- | --- | --- | -------- | ------- | ---- | ---------- | ------------ | --- | ------- |
(3)finish[answer],whichfinishesthecurrenttaskwith average text length of 262 words and a vocabulary size
answer. of 224k. In addition, there are over 800k unique product
|           |                     |          |      |            | options | available | for    | customization. |      | The  | environment |
| --------- | ------------------- | -------- | ---- | ---------- | ------- | --------- | ------ | -------------- | ---- | ---- | ----------- |
| These API | calls and free-form | thoughts | form | the action |         |           |        |                |      |      |             |
|           |                     |          |      |            | renders | webpages  | in two | modes:         | HTML | mode | provides    |
spaceforthisenvironment.
|     |     |     |     |     | pixel-level | observations |     | with | interactive | elements, | while |
| --- | --- | --- | --- | --- | ----------- | ------------ | --- | ---- | ----------- | --------- | ----- |
simplemodeconvertstherawHTMLintoastructuredtext
D.2.Programming
|     |     |     |     |     | observationmoreamenablefortrainingagents. |     |     |     |     |     | Theaction |
| --- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | --------- |
TheHumanEvaldataset(Chenetal.,2021)isacollection spaceconsistsofquerysearchesandbuttonclicks,which
|     |     |     |     |     | transitionbetween4-pagetypes: |     |     |     | search,results,item,and |     |     |
| --- | --- | --- | --- | --- | ----------------------------- | --- | --- | --- | ----------------------- | --- | --- |
of164handwrittenprogrammingproblemsintroducedto
|          |                            |     |           |             | itemdetail. | Instructionsarecrowdsourcednaturallanguage |     |     |     |     |     |
| -------- | -------------------------- | --- | --------- | ----------- | ----------- | ------------------------------------------ | --- | --- | --- | --- | --- |
| evaluate | the functional correctness |     | of models | for synthe- |             |                                            |     |     |     |     |     |
sizingprogramsfromnaturallanguagedescriptions. Each specifyingproductattributesandoptions,withatotalof12k
|         |                     |            |           |          | collected. | Automaticrewardsarecomputedbycomparing |     |     |     |     |     |
| ------- | ------------------- | ---------- | --------- | -------- | ---------- | -------------------------------------- | --- | --- | --- | --- | --- |
| problem | includes a function | signature, | docstring | descrip- |            |                                        |     |     |     |     |     |
tion,referenceimplementation,andmultipleunittests,with the product purchased by the agent against the attributes
an average of 7.7 tests per problem. The programming andoptionsspecifiedintheinstruction,usingbothlexical
matchingandsemanticsimilaritymetrics.
tasksassesscomprehensionofnaturallanguage,reasoning,
algorithms,andbasicmathematics,atadifficultylevelcom-
parabletosimplesoftwareinterviewquestions. Passrates TherearetwoevaluationmetricsusedinWebShop:(1)Task
areevaluatedwiththepass@kmetric,whereksamplesare
|     |     |     |     |     | Scoredefinedas(100×avg. |     |     |     | reward),whichcapturesthe |     |     |
| --- | --- | --- | --- | --- | ----------------------- | --- | --- | --- | ------------------------ | --- | --- |
generatedperproblemandaproblemisconsideredsolved
16

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
Figure4.ExampletrajectoriesonHotPotQAforReAct(left)andLATS(right).LATScansamplemoreactionsandavoidfailurefrom
previousmistakesbyevaluatingstateswithanLMtoguidethesearchtowardpromisingareasofthetree.
Type Argument State→NextState PromptMethod Gameof24(SuccessRate)↑
search
|        | [Query]       | Search→Results  |     | LATS(CoT,λ=1) |     | 0.40 |
| ------ | ------------- | --------------- | --- | ------------- | --- | ---- |
| choose | Backtosearch  | ∗→Search        |     | LATS(CoT)     |     | 0.44 |
| choose | Prev/Nextpage | Results→Results |     |               |     |      |
choose [Producttitle] Results→Item Table13.AblationsonλinGameof24withGPT-3.5. λ = 0.5
choose [Option] Item→Item usedinthemainpaperoutperformsλ=1,equivalenttoremoving
choose self-consistency,whichindicatesthattheself-consistencyscore
|     | Desc/Overview | Item→Item-Detail |     |     |     |     |
| --- | ------------- | ---------------- | --- | --- | --- | --- |
improvestheperformanceofLATS.
| choose | Previous | Item-Detail→Item |     |     |     |     |
| ------ | -------- | ---------------- | --- | --- | --- | --- |
| choose | Buy      | Item→EpisodeEnd  |     |     |     |     |
correctequationthatequals24anduseseachinputnumber
onlyonce. Wereportsuccessrateover50games. Weuse
Table12. ActionspaceofWebShop.
k =30iterationsandamaximumdepthlimitof5.Forvalue
functionhyperparameters,weuseλ=0.5fortheLMscore
|     |     |     |     | andself-consistencyscore. | Tab.13showstheperformance |     |
| --- | --- | --- | --- | ------------------------- | ------------------------- | --- |
averagerewardobtainedacrossepisodes;and(2)Success
|                                                 |     |     |     | comparisonbetweenλ | = 0.5andλ | = 1,whichvalidates |
| ----------------------------------------------- | --- | --- | --- | ------------------ | --------- | ------------------ |
| Rate(SR)definedastheportionofinstructionswherer |     |     | =1. |                    |           |                    |
ourdesignofself-consistencyterm.
Therewardiscalculatedbasedonthenumberofattributes
| satisfiedbytheselecteditem. |     | Weuse50environmentsfor |     |     |     |     |
| --------------------------- | --- | ---------------------- | --- | --- | --- | --- |
E.HotPotQAPrompts
| our experiments | and a maximum | depth limit | of 15. For |     |     |     |
| --------------- | ------------- | ----------- | ---------- | --- | --- | --- |
valuefunctionhyperparameters,weuseλ=0.8fortheLM
E.1.BaseActingPrompt
scoreandself-consistencyscore.
SolveaquestionansweringtaskwithinterleavingThought,
D.4.Gameof24 Action,Observationsteps. Thoughtcanreasonaboutthe
currentsituation,andActioncanbethreetypes:
Gameof24isamathematicalreasoningchallengewhere
thegoalistousebasicarithmeticoperationstoconstruct (1) Search[entity], which searches the exact entity on
24outof4numbers. WefollowthesetupfromYaoetal. Wikipedia and returns the first paragraph if it exists. If
(2023a),wherewemeasuresuccessiftheagentproducesa not,itwillreturnsomesimilarentitiestosearch.
17

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
(2)Lookup[keyword],whichreturnsthenextsentencecon- witheitherActionoranindexedThought
tainingkeywordinthecurrentpassage.
Herearesomeexamples:
(3)Finish[answer],whichreturnstheanswerandfinishes
|     |     |     |     | Question: | Whatistheelevationrangefortheareathatthe |     |     |     |
| --- | --- | --- | --- | --------- | ---------------------------------------- | --- | --- | --- |
thetask.
easternsectoroftheColoradoorogenyextendsinto?
Aftereachobservation,providethenextThoughtandnext
Let’sthinkstepbystep.
Action.
|     |     |     |     | Thought1: | TheeasternsectorofColoradoorogenyextends |     |     |     |
| --- | --- | --- | --- | --------- | ---------------------------------------- | --- | --- | --- |
Herearesomeexamples:
intotheHighPlains.
| Question: | WhichmagazinewasstartedfirstArthur’sMaga- |     |     |           |                                          |     |     |     |
| --------- | ----------------------------------------- | --- | --- | --------- | ---------------------------------------- | --- | --- | --- |
|           |                                           |     |     | Thought2: | HighPlainsriseinelevationfromaround1,800 |     |     |     |
zineorFirstforWomen?
to7,000ft
| Thought1: | IneedtosearchArthur’sMagazineandFirstfor |     |     |           |                            |     |     |     |
| --------- | ---------------------------------------- | --- | --- | --------- | -------------------------- | --- | --- | --- |
|           |                                          |     |     | Thought3: | Theansweris1,800to7,000ft. |     |     |     |
Women,andfindwhichwasstartedfirst.
|          |                          |     |     | Action: | Finish[1,800to7,000ft] |     |     |     |
| -------- | ------------------------ | --- | --- | ------- | ---------------------- | --- | --- | --- |
| Action1: | Search[Arthur’sMagazine] |     |     |         |                        |     |     |     |
(examples)
| Observation1: | Arthur’sMagazinewasanAmericanliterary |     |     |     |     |     |     |     |
| ------------- | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
periodical published in Philadelphia in the 19th century. Previoustrial: (trajectories)
EditedbyTimothyShayArthur,itfeaturedworkbyEdgar
(input)
| A. Poe,    | J.H. Ingraham, | Sarah Josepha | Hale, Thomas  | G.   |     |     |     |     |
| ---------- | -------------- | ------------- | ------------- | ---- | --- | --- | --- | --- |
| Spear, and | others.[1][2]  | In May 1846   | it was merged | into |     |     |     |     |
E.3.ValueFunctionPrompt
Godey’sLady’sBook.[3]
Thought2: Arthur’sMagazinewasstartedin1844. Ineed Analyzethetrajectoriesofasolutiontoaquestionanswering
|     |     |     |     | task. ThetrajectoriesarelabeledbyenvironmentalObser- |     |     |     |     |
| --- | --- | --- | --- | ---------------------------------------------------- | --- | --- | --- | --- |
tosearchFirstforWomennext.
vationsaboutthesituation,Thoughtsthatcanreasonabout
| Action2: | Search[FirstforWomen] |     |     |     |     |     |     |     |
| -------- | --------------------- | --- | --- | --- | --- | --- | --- | --- |
thecurrentsituation,andActionsthatcanbethreetypes:
Observation 2: First for Women is a woman’s magazine (1) Search[entity], which searches the exact entity on
publishedbyBauerMediaGroupintheUSA.[1]Themag-
|     |     |     |     | Wikipedia | and returns the | first paragraph | if it exists. | If  |
| --- | --- | --- | --- | --------- | --------------- | --------------- | ------------- | --- |
azinewasstartedin1989. ItisbasedinEnglewoodCliffs, not,itwillreturnsomesimilarentitiestosearch.
NewJersey.[2]In2011thecirculationofthemagazinewas
(2)Lookup[keyword],whichreturnsthenextsentencecon-
1,310,696copies.[3]
tainingkeywordinthecurrentpassage.
| Thought | 3: First for | Women was | started in 1989. | 1844 |     |     |     |     |
| ------- | ------------ | --------- | ---------------- | ---- | --- | --- | --- | --- |
(3)Finish[answer],whichreturnstheanswerandfinishes
(Arthur’sMagazine)<1989(FirstforWomen),soArthur’s
thetask.
Magazinewasstartedfirst.
Givenaquestionandatrajectory,evaluateitscorrectness
| Action3: | Finish[Arthur’sMagazine] |     |     |             |                |              |            |       |
| -------- | ------------------------ | --- | --- | ----------- | -------------- | ------------ | ---------- | ----- |
|          |                          |     |     | and provide | your reasoning | and analysis | in detail. | Focus |
(examples)
|     |     |     |     | onthelatestthought,action,andobservation. |                |                 | Incomplete  |     |
| --- | --- | --- | --- | ----------------------------------------- | -------------- | --------------- | ----------- | --- |
|     |     |     |     | trajectories                              | can be correct | if the thoughts | and actions | so  |
Youhaveattemptedtoanswerthefollowingquestionbefore
|            |                                           |     |     | fararecorrect,eveniftheanswerisnotfoundyet. |     |     |     | Donot |
| ---------- | ----------------------------------------- | --- | --- | ------------------------------------------- | --- | --- | --- | ----- |
| andfailed. | Thefollowingreflection(s)giveaplantoavoid |     |     |                                             |     |     |     |       |
failing to answer the question in the same way you did generateadditionalthoughtsoractions. Thenatthelastline
|             |                                         |     |     | conclude“Thusthecorrectnessscoreiss”, |     |     | wheresisan |     |
| ----------- | --------------------------------------- | --- | --- | ------------------------------------- | --- | --- | ---------- | --- |
| previously. | Usethemtoimproveyourstrategyofcorrectly |     |     |                                       |     |     |            |     |
integerfrom1to10.
answeringthegivenquestion.
|     |     |     |     | Question: | WhichmagazinewasstartedfirstArthur’sMaga- |     |     |     |
| --- | --- | --- | --- | --------- | ----------------------------------------- | --- | --- | --- |
(trajectories)
zineorFirstforWomen?
(input)
|     |     |     |     | Thought1: | IneedtosearchArthur’sMagazineandFirstfor |     |     |     |
| --- | --- | --- | --- | --------- | ---------------------------------------- | --- | --- | --- |
Women,andfindwhichwasstartedfirst.
E.2.BaseReasoningPrompt
|     |     |     |     | Action1: | Search[Arthur’sMagazine] |     |     |     |
| --- | --- | --- | --- | -------- | ------------------------ | --- | --- | --- |
SolveaquestionansweringtaskbyhavingaThought,then
Finish with your answer. Thought can reason about the Observation1: Arthur’sMagazinewasanAmericanliterary
current situation. Finish[answer] returns the answer and periodical published in Philadelphia in the 19th century.
finishesthetask. Youwillbegivencontextthatyoushould EditedbyTimothyShayArthur,itfeaturedworkbyEdgar
usetohelpyouanswerthequestion. Startyourresponse A. Poe, J.H. Ingraham, Sarah Josepha Hale, Thomas G.
18

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
Spear, and others.[1][2] In May 1846 it was merged into makingthisthebestaction.
Godey’sLady’sBook.[3]
Thusthecorrectnessscoreis10
| This trajectory |     | is correct | as it is | reasonable | to search | for |     |     |     |     |     |     |
| --------------- | --- | ---------- | -------- | ---------- | --------- | --- | --- | --- | --- | --- | --- | --- |
(otherexamples)
| thefirstmagazineprovidedinthequestion. |        |          |               |     | Itisalsobetter |         |                      |     |     |     |     |     |
| -------------------------------------- | ------ | -------- | ------------- | --- | -------------- | ------- | -------------------- | --- | --- | --- | --- | --- |
| to have                                | simple | searches | corresponding |     | to a single    | entity, | (failedtrajectories) |     |     |     |     |     |
makingthisthebestaction.
(context)
Thusthecorrectnessscoreis10
| (otherexamples) |     |     |     |     |     |     | F.ProgrammingPrompts |     |     |     |     |     |
| --------------- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | --- | --- | --- |
(failedtrajectories) F.1.HumanEvalfunctionimplementationexample
(context)
Samplefunctionsignature:
E.4.ReflectionPrompt
|     |     |     |     |     |     |     | def | minSubArraySum(nums): |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- |
Analyze the trajectories of a solution to a question- Given an array of integers nums,
| answering | task. | The trajectories |     | are labeled | by  | environ- |     |      |             |     |        |     |
| --------- | ----- | ---------------- | --- | ----------- | --- | -------- | --- | ---- | ----------- | --- | ------ | --- |
|           |       |                  |     |             |     |          |     | find | the minimum | sum | of any |     |
mentalObservationsaboutthesituation,Thoughtsthatcan non−empty sub−array of nums.
| reasonaboutthecurrentsituation,andActionsthatcanbe |     |       |          |     |              |     |     | Example             |     |     |          |       |
| -------------------------------------------------- | --- | ----- | -------- | --- | ------------ | --- | --- | ------------------- | --- | --- | -------- | ----- |
| threetypes:                                        |     |       |          |     |              |     |     | minSubArraySum([−1, |     |     | −2, −3]) | == −6 |
| (1) Search[entity],                                |     | which | searches | the | exact entity | on  |     |                     |     |     |          |       |
Samplefunctionbodyimplementation:
| Wikipedia | and | returns the | first paragraph |     | if it exists. | If  |     |     |     |     |     |     |
| --------- | --- | ----------- | --------------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
not,itwillreturnsomesimilarentitiestosearch.
|     |     |     |     |     |     |     |     | min sum | = float | (’inf | ’)  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------- | ----- | --- | --- |
(2)Lookup[keyword],whichreturnsthenextsentencecon-
|     |     |     |     |     |     |     |     | for | i in range(len(nums)): |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- |
tainingkeywordinthecurrentpassage.
|     |     |     |     |     |     |     |     |     | current sum | = 0 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- |
(3)Finish[answer],whichreturnstheanswerandfinishes for j in range(i , len(nums)):
thetask.
|     |     |     |     |     |     |     |     |     | current    | sum | += nums[j] |      |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ---------- | ---- |
|     |     |     |     |     |     |     |     |     | if current | sum | < min      | sum: |
Givenaquestionandatrajectory,evaluateitscorrectness
|             |      |           |     |          |            |       |     |     | min | sum | = current | sum |
| ----------- | ---- | --------- | --- | -------- | ---------- | ----- | --- | --- | --- | --- | --------- | --- |
| and provide | your | reasoning | and | analysis | in detail. | Focus |     |     |     |     |           |     |
onthelatestthought,action,andobservation. Incomplete return min sum
| trajectories                                | can | be correct | if the | thoughts | and actions | so    |     |     |     |     |     |     |
| ------------------------------------------- | --- | ---------- | ------ | -------- | ----------- | ----- | --- | --- | --- | --- | --- | --- |
| fararecorrect,eveniftheanswerisnotfoundyet. |     |            |        |          |             | Donot |     |     |     |     |     |     |
F.2.BaseActing/ReasoningPrompt
| generateadditionalthoughtsoractions. |     |     |     | Thenatthelastline |     |     |     |     |     |     |     |     |
| ------------------------------------ | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
conclude“Thusthecorrectnessscoreiss”, wheresisan You are an AI Python assistant. You will be given your
integerfrom1to10. previousimplementationofafunction,aseriesofunittests
results,andyourself-reflectiononyourpreviousimplemen-
| Question: | WhichmagazinewasstartedfirstArthur’sMaga- |     |     |     |     |     |         |                                                |     |     |     |     |
| --------- | ----------------------------------------- | --- | --- | --- | --- | --- | ------- | ---------------------------------------------- | --- | --- | --- | --- |
|           |                                           |     |     |     |     |     | tation. | Writeyourfullimplementation(restatethefunction |     |     |     |     |
zineorFirstforWomen?
signature).
| Thought1: | IneedtosearchArthur’sMagazineandFirstfor |     |     |     |     |     |     |     |     |     |     |     |
| --------- | ---------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Example1:
Women,andfindwhichwasstartedfirst.
[previousimpl]:
| Action1:      | Search[Arthur’sMagazine]              |     |              |     |          |          |     |         |           |       |        |            |
| ------------- | ------------------------------------- | --- | ------------ | --- | -------- | -------- | --- | ------- | --------- | ----- | ------ | ---------- |
|               |                                       |     |              |     |          |          | def | add(a:  | int , b:  | int ) | −> int | :          |
| Observation1: | Arthur’sMagazinewasanAmericanliterary |     |              |     |          |          |     |         |           |       |        |            |
|               |                                       |     |              |     |          |          |     | ‘‘Given | integers  | a and | b,     |            |
| periodical    | published                             | in  | Philadelphia | in  | the 19th | century. |     |         |           |       |        |            |
|               |                                       |     |              |     |          |          |     | return  | the total | value | of     | a and b.’’ |
EditedbyTimothyShayArthur,itfeaturedworkbyEdgar
|                       |                |     |               |         |              |      |                                    | return | a − b |     |     |     |
| --------------------- | -------------- | --- | ------------- | ------- | ------------ | ---- | ---------------------------------- | ------ | ----- | --- | --- | --- |
| A. Poe,               | J.H. Ingraham, |     | Sarah Josepha |         | Hale, Thomas | G.   |                                    |        |       |     |     |     |
| Spear, and            | others.[1][2]  |     | In May        | 1846 it | was merged   | into |                                    |        |       |     |     |     |
| Godey’sLady’sBook.[3] |                |     |               |         |              |      | [unittestresultsfrompreviousimpl]: |        |       |     |     |     |
Testedpassed:
| This trajectory                        |     | is correct | as it is | reasonable | to search      | for |     |     |     |     |     |     |
| -------------------------------------- | --- | ---------- | -------- | ---------- | -------------- | --- | --- | --- | --- | --- | --- | --- |
| thefirstmagazineprovidedinthequestion. |     |            |          |            | Itisalsobetter |     |     |     |     |     |     |     |
Testsfailed:
| to have | simple | searches | corresponding |     | to a single | entity, |                           |     |     |     |     |     |
| ------- | ------ | -------- | ------------- | --- | ----------- | ------- | ------------------------- | --- | --- | --- | --- | --- |
|         |        |          |               |     |             |         | assertadd(1,2)==3#output: |     |     | -1  |     |     |
19

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
assertadd(1,2)==4#output: -1 Thiswillensurethatthefunctionreturnsthecorrectoutput
forthegiveninput.
[reflectiononpreviousimpl]:
The implementation failed the test cases where the input F.4.TestCaseGenerationPrompt
| integersare1and2. |     | Theissuearisesbecausethecodedoes |     |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
YouareanAIcodingassistantthatcanwriteunique,diverse,
notaddthetwointegerstogether,butinsteadsubtractsthe
andintuitiveunittestsforfunctionsgiventhesignatureand
| secondintegerfromthefirst. |     |     | Tofixthisissue,weshould |     |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
docstring.
changetheoperatorfrom‘-’to‘+’inthereturnstatement.
| Thiswillensurethatthefunctionreturnsthecorrectoutput |     |     |     |     |     |     | (input) |     |     |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
forthegiveninput.
| [improvedimpl]: |        |       |        |      |       |     | G.WebShopPrompts |     |     |     |     |     |
| --------------- | ------ | ----- | ------ | ---- | ----- | --- | ---------------- | --- | --- | --- | --- | --- |
| def             | add(a: | int , | b: int | ) −> | int : |     | G.1.ActingPrompt |     |     |     |     |     |
‘‘
Webshop
|     | Given  | integers  | a   | and b, |          |     |              |     |     |     |     |     |
| --- | ------ | --------- | --- | ------ | -------- | --- | ------------ | --- | --- | --- | --- | --- |
|     | return | the total |     | value  | of a and | b.  | Instruction: |     |     |     |     |     |
’’
iwouldlikea3ouncebottleofbrightcitrusdeodorantfor
|     | return | a + b |     |     |     |     |     |     |     |     |     |     |
| --- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sensitiveskin,andpricelowerthan50.00dollars
[Search]
F.3.ReflectionPrompt
| YouareaPythonprogrammingassistant.                  |     |     |     |     | Youwillbegiven |     |         |                |        |                  |     |           |
| --------------------------------------------------- | --- | --- | --- | --- | -------------- | --- | ------- | -------------- | ------ | ---------------- | --- | --------- |
|                                                     |     |     |     |     |                |     | Action: | search[3 ounce | bright | citrus deodorant |     | sensitive |
| afunctionimplementationandaseriesofunittestresults. |     |     |     |     |                |     | skin]   |                |        |                  |     |           |
Yourgoalistowriteafewsentencestoexplainwhyyour
| implementation                              |     | is wrong, | as indicated |     | by the tests. | You  | Observation:   |     |     |     |     |     |
| ------------------------------------------- | --- | --------- | ------------ | --- | ------------- | ---- | -------------- | --- | --- | --- | --- | --- |
| willneedthisasguidancewhenyoutryagainlater. |     |           |              |     |               | Only | [BacktoSearch] |     |     |     |     |     |
providethefewsentencedescriptioninyouranswer,notthe
|                 |     |                                 |     |     |     |     | Page1(Totalresults: | 50) |     |     |     |     |
| --------------- | --- | ------------------------------- | --- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- |
| implementation. |     | Youwillbegivenafewexamplesbythe |     |     |     |     |                     |     |     |     |     |     |
user.
[Next][B078GWRC1J]
| Example1: |     |     |     |     |     |     | BrightCitrusDeodorantbyEarthMama—NaturalandSafe |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | ----------------------------------------------- | --- | --- | --- | --- | --- |
[previousimpl]: forSensitiveSkin,PregnancyandBreastfeeding,Contains
OrganicCalendula3-Ounce
|     | def | add(a: int | , b: | int | ) −> int | :   |     |     |     |     |     |     |
| --- | --- | ---------- | ---- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
$10.99
‘‘
|     |     | Given integers |       | a and | b,  |       | [B078GTKVXY] |     |     |     |     |     |
| --- | --- | -------------- | ----- | ----- | --- | ----- | ------------ | --- | --- | --- | --- | --- |
|     |     | return the     | total | value | of  | a and | b.           |     |     |     |     |     |
GingerFreshDeodorantbyEarthMama—NaturalandSafe
’’
forSensitiveSkin,PregnancyandBreastfeeding,Contains
|     | return | a − b |     |     |     |     |     |     |     |     |     |     |
| --- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
OrganicCalendula3-Ounce
| [unittestresultsfrompreviousimpl]: |     |     |     |     |     |     | $10.99       |                     |     |            |           |     |
| ---------------------------------- | --- | --- | --- | --- | --- | --- | ------------ | ------------------- | --- | ---------- | --------- | --- |
| Testedpassed:                      |     |     |     |     |     |     | [B08KBVJ4XN] |                     |     |            |           |     |
|                                    |     |     |     |     |     |     | Barrel and   | Oak - Aluminum-Free |     | Deodorant, | Deodorant |     |
Testsfailed:
forMen,EssentialOil-BasedScent,24-HourOdorProtec-
| assertadd(1,2)==3#output: |     |     | -1  |     |     |     |             |             |        |           |           |      |
| ------------------------- | --- | --- | --- | --- | --- | --- | ----------- | ----------- | ------ | --------- | --------- | ---- |
|                           |     |     |     |     |     |     | tion, Cedar | & Patchouli | Blend, | Gentle on | Sensitive | Skin |
(MountainSage,2.7oz,2-Pack)
| assertadd(1,2)==4#output:   |                |        | -1  |            |       |           |        |     |     |     |     |     |
| --------------------------- | -------------- | ------ | --- | ---------- | ----- | --------- | ------ | --- | --- | --- | --- | --- |
| [reflectiononpreviousimpl]: |                |        |     |            |       |           | $15.95 |     |     |     |     |     |
| The                         | implementation | failed | the | test cases | where | the input |        |     |     |     |     |     |
integersare1and2. Theissuearisesbecausethecodedoes Action: think[B078GWRC1J and B078GTKVXY are
|     |     |     |     |     |     |     | bright citrus | deodorant | less then | 50 dollars. | I can | check |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --------- | --------- | ----------- | ----- | ----- |
notaddthetwointegerstogether,butinsteadsubtractsthe
| secondintegerfromthefirst. |     |     | Tofixthisissue,weshould |     |     |     | B078GWRC1Jfirst.] |     |     |     |     |     |
| -------------------------- | --- | --- | ----------------------- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- |
changetheoperatorfrom‘-’to‘+’inthereturnstatement.
20

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
Observation: OK. iamlookingfordairyfreeandapplevarietypackofchips,
andpricelowerthan30.00dollars
Action: click[B078GWRC1J] [Search]
Observation:
Action: search[dairyfreeandapplevarietypackofchips]
[BacktoSearch]
Observation:
[Prev]
[BacktoSearch]
scent [assorted scents][bright citrus][calming laven-
der][ginger fresh][simply non-scents] size [travel set (4- Page1(Totalresults: 50)
pack)][3ounce(packof1)][3-ounce(2-pack)]BrightCitrus
[Next]
DeodorantbyEarthMama—NaturalandSafeforSensi-
tiveSkin,PregnancyandBreastfeeding,ContainsOrganic [B07HRFJWP8]
Calendula3-Ounce
EnjoyLifeFoodsSoftBakedOvals, BreakfastBars, Nut
Price: $10.99 FreeBars,SoyFree,DairyFree,NonGMO,GlutenFree,
Vegan,VarietyPack,4Boxes(20BarsTotal)
Rating: N.A.
$100.0
[Description]
[B01KMHY5PG]
[Features]
EnjoyLifeSoftBakedChewyBars,VarietyPack,NutFree
[Reviews]
Bars,SoyFree,DairyFree,GlutenFree,6Boxes(30Total
[BuyNow] Bars)
$21.49
Action: think[For3ouncebottleofbrightcitrusdeodorant
[B008D2X8C4]
forsensitiveskin,theitemhasoptions‘brightcitrus’and‘3
ounce(packof1)’andseemsgoodtobuy.] EnjoyLifeLentilChipsVarietyPack,DairyFreeChips,Soy
Free, NutFree, NonGMO,Vegan, GlutenFree, 24Bags
Observation: OK.
(0.8oz)
$100.0
Action: click[brightcitrus]
Observation: Youhaveclickedbrightcitrus.
Action: think[ThefirsttwoitemsarenotwhatIwant. The
thirditemisthedairyfreeandapplevarietypackofchipsI
Action: click[3ounce(packof1)] want.]
Observation: Youhaveclicked3ounce(packof1). Observation: OK.
Action: click[BuyNow] Action: click[B008D2X8C4]
Observation:
G.2.ValueFunctionPrompt
[BacktoSearch]
Givenanitemtopurchaseandatrajectorythataimstobuy
anitemthatexactlymatchesthespecification,whichcor- [Prev]
responds to the ideal score of 1.0, analyze the following
flavorname[dillandsourcream][garlic&parmesan][light
trajectory,thenatthelastlineconclude,“Thusthecorrect-
seasalt][margheritapizza][thaichililime][varietypack]size
nessscoreiss”,wheresisanintegerfrom1to10.
[0.8ounce(packof24)][4ounce(packof12)]
Herearesomeexamples
Price: $100.0
Rating: N.A.
Webshop
[Description]
Instruction:
[Features]
21

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
| [Reviews] |     |     |     | (20BarsTotal)$100.0[B01KMHY5PG]EnjoyLifeSoft |     |     |     |
| --------- | --- | --- | --- | -------------------------------------------- | --- | --- | --- |
BakedChewyBars,VarietyPack,NutFreeBars,SoyFree,
[BuyNow]
|     |     |     |     | Dairy Free, | Gluten Free, | 6 Boxes (30 | Total Bars) $21.49 |
| --- | --- | --- | --- | ----------- | ------------ | ----------- | ------------------ |
[B008D2X8C4]EnjoyLifeLentilChipsVarietyPack,Dairy
Action: think[Theitemhasoptions‘varietypack’and‘0.8 FreeChips,SoyFree,NutFree,NonGMO,Vegan,Gluten
| ounce(packof24)’andseemsgoodtobuy.] |     |     |     | Free,24Bags(0.8oz)$100.0 |     |     |     |
| ----------------------------------- | --- | --- | --- | ------------------------ | --- | --- | --- |
Observation: OK. Action: think[ThefirsttwoitemsarenotwhatIwant. The
thirditemisthedairyfreeandapplevarietypackofchipsI
|     |     |     |     | want.] Observation: | OK. |     |     |
| --- | --- | --- | --- | ------------------- | --- | --- | --- |
Action: click[varietypack]
Action:click[B008D2X8C4]Observation:[BacktoSearch]
| Observation: | Youhaveclickedvarietypack. |     |     |     |     |     |     |
| ------------ | -------------------------- | --- | --- | --- | --- | --- | --- |
[<Prev]flavorname[dillandsourcream][garlic&parme-
san][lightseasalt][margheritapizza][thaichililime][variety
Action: click[0.8ounce(packof24)] pack]size[0.8ounce(packof24)][4ounce(packof12)]
|              |                                   |     |     | Price: $100.0 | Rating: N.A. | [Description] | [Features] [Re- |
| ------------ | --------------------------------- | --- | --- | ------------- | ------------ | ------------- | --------------- |
| Observation: | Youhaveclicked0.8ounce(packof24). |     |     |               |              |               |                 |
views][BuyNow]
Action: think[Theitemhasoptions‘varietypack’and‘0.8
Action: click[BuyNow]
|     |     |     |     | ounce(packof24)’andseemsgoodtobuy.] |     |     | Observation: |
| --- | --- | --- | --- | ----------------------------------- | --- | --- | ------------ |
OK.
| Reflection: | Inthisattempt,Iwasunsuccessful. |     | Iacciden- |                                        |     |     |                |
| ----------- | ------------------------------- | --- | --------- | -------------------------------------- | --- | --- | -------------- |
|             |                                 |     |           | Action: click[varietypack]Observation: |     |     | Youhaveclicked |
tallyboughtaproductthatwas$100,whichismorethanmy
varietypack.
| budgetof$30. | Eitherway,theinitialsearchresultswerenot |     |     |     |     |     |     |
| ------------ | ---------------------------------------- | --- | --- | --- | --- | --- | --- |
good. Nexttime,Iwilldosearch[“varietypackofchip”;] Action: click[0.8 ounce (pack of 24)] Observation: You
andthencheckiftheresultsmeetthedairyfreeandthe$30 haveclicked0.8ounce(packof24).
| budgetconstraints. | Iwillcontinuetorefinemysearchesso |     |     |     |     |     |     |
| ------------------ | --------------------------------- | --- | --- | --- | --- | --- | --- |
Action: click[BuyNow]
thatIcanfindmoreproducts.
STATUS:FAIL
Thusthecorrectnessscoreis5
|     |     |     |     | Reflection: | Inthisattempt,Iwasunsuccessful. |     | Iacciden- |
| --- | --- | --- | --- | ----------- | ------------------------------- | --- | --------- |
tallyboughtaproductthatwas$100,whichismorethanmy
(input)
|     |     |     |     | budgetof$30. | Eitherway,theinitialsearchresultswerenot |     |     |
| --- | --- | --- | --- | ------------ | ---------------------------------------- | --- | --- |
good. Nexttime,Iwilldosearch[“varietypackofchips”]
G.3.ReflectionPrompt
andthencheckiftheresultsmeetthedairyfreeandthe$30
Youareanadvancedreasoningagentthatcanimprovebased budgetconstraints. Iwillcontinuetorefinemysearchesso
thatIcanfindmoreproducts.
| onself-reflection. | Youwillbegivenapreviousreasoning |     |     |     |     |     |     |
| ------------------ | -------------------------------- | --- | --- | --- | --- | --- | --- |
trialinwhichyouweregivenaccesstoashoppingwebsite
|                                       |     |                    |            | Previous Trial  | Instruction: | i need gluten   | free vegetarian  |
| ------------------------------------- | --- | ------------------ | ---------- | --------------- | ------------ | --------------- | ---------------- |
| andaspecifictypeofitemtobuy.          |     | Youweregivenaccess |            |                 |              |                 |                  |
|                                       |     |                    |            | smoked peppered | bacon        | - 4 ounce (pack | of 2), and price |
| torelevantcontextandanitemtopurchase. |     |                    | Youwereun- |                 |              |                 |                  |
lowerthan40.00dollars[Search]
successfulinbuyingthecorrectitemeitherbecauseyoudid
notfindanitemmeetingalloftherequiredspecifications Action: search[glutenfreevegetariansmokedpepperedba-
|            |             |                    |                 | con4ouncepackof2]Observation: |     | [BacktoSearch]Page |     |
| ---------- | ----------- | ------------------ | --------------- | ----------------------------- | --- | ------------------ | --- |
| or because | you did not | select the correct | item. The ideal |                               |     |                    |     |
score is 1.0, and anything less is incorrect. In a few sen- 1 (Total results: 50) [Next >] [B06Y96MXJV] Smoked
|     |     |     |     | BaconSeaSalt3-Pack: |     | SmokedBaconChipotle,Smoked |     |
| --- | --- | --- | --- | ------------------- | --- | -------------------------- | --- |
tences,Diagnoseapossiblereasonforfailureanddevisea
new,concise,high-levelplanthataimstomitigatethesame BaconandOnion,SmokedPepperedBacon-All-Natural
failure. Usecompletesentences. Herearesomeexamples: SeaSaltsSlowlySmokedOverAlderwood-NoGluten,No
|                           |         |                           |                  | MSG, Non-GMO                 | (12 total | oz.) $29.99           | [B06Y96N1KG] |
| ------------------------- | ------- | ------------------------- | ---------------- | ---------------------------- | --------- | --------------------- | ------------ |
| PreviousTrialInstruction: |         | iamlookingfordairyfreeand |                  |                              |           |                       |              |
|                           |         |                           |                  | SpicyHotPepperSeaSalt3-Pack: |           | GhostPepper,Jalapeno, |              |
| apple variety             | pack of | chips, and price          | lower than 30.00 |                              |           |                       |              |
Habanero-AllNatural,DeliciousBlendsofPeppers&Sea
dollars[Search]
Salt-Gluten-Free,Kosher,NoMSG,Non-GMO(12total
Action: search[dairyfreeandapplevarietypackofchips] oz.) $29.99 [B07GJTKYJQ] Louisville Vegan Jerky - 5
FlavorVarietyPack,Non-GMOSoyProtein,Gluten-Free
| Observation: | [Back to | Search] Page 1 | (Total results: 50) |     |     |     |     |
| ------------ | -------- | -------------- | ------------------- | --- | --- | --- | --- |
[Next >] [B07HRFJWP8] Enjoy Life Foods Soft Baked (BlackPepper,BuffaloDill,Pepperoni,MapleBacon,and
CarolinaBBQ,3Ounces)$42.99
Ovals,BreakfastBars,NutFreeBars,SoyFree,DairyFree,
| Non GMO, | Gluten Free, | Vegan, Variety | Pack, 4 Boxes |     |     |     |     |
| -------- | ------------ | -------------- | ------------- | --- | --- | --- | --- |
22

LanguageAgentTreeSearchUnifiesReasoning,Acting,andPlanninginLanguageModels
| Action:      | think[ThefirsttwoitemsarenotwhatIwant. |              |              |        | The           |
| ------------ | -------------------------------------- | ------------ | ------------ | ------ | ------------- |
| third item   | is not                                 | what I want, | but it       | is the | closest one.] |
| Observation: | OK.                                    |              |              |        |               |
| Action:      | click[B07GJTKYJQ]                      |              | Observation: |        | [Back to      |
Search][<Prev]LouisvilleVeganJerky-5FlavorVariety
Pack,Non-GMOSoyProtein,Gluten-Free(BlackPepper,
BuffaloDill,Pepperoni,MapleBacon,andCarolinaBBQ,
| 3Ounces)Price: |     | $42.99Rating: | N.A.[Description][Fea- |     |     |
| -------------- | --- | ------------- | ---------------------- | --- | --- |
tures][Reviews][BuyNow]
Action:think[ThepriceistoohighanditisnotwhatIwant.]
| Observation:        | OK.                      |                            |                    |     |        |
| ------------------- | ------------------------ | -------------------------- | ------------------ | --- | ------ |
| Action:             | click[<Prev]Observation: |                            | [BacktoSearch]Page |     |        |
| 1 (Total            | results:                 | 50) [Next                  | >] [B06Y96MXJV]    |     | Smoked |
| BaconSeaSalt3-Pack: |                          | SmokedBaconChipotle,Smoked |                    |     |        |
BaconandOnion,SmokedPepperedBacon-All-Natural
| Sea Salts                    | Slowly | Smoked             | Over Alderwood        |        | - No Gluten, |
| ---------------------------- | ------ | ------------------ | --------------------- | ------ | ------------ |
| NoMSG,Non-GMO(12totaloz.)    |        |                    | 29.99[B06Y96N1KG]     |        |              |
| SpicyHotPepperSeaSalt3-Pack: |        |                    | GhostPepper,Jalapeno, |        |              |
| Habanero                     | - All  | Natural, Delicious |                       | Blends | of Peppers & |
SeaSalt-Gluten-Free,Kosher,NoMSG,Non-GMO(12
totaloz.) 29.99[B07GJTKYJQ]LouisvilleVeganJerky-5
FlavorVarietyPack,Non-GMOSoyProtein,Gluten-Free
(BlackPepper,BuffaloDill,Pepperoni,MapleBacon,and
CarolinaBBQ,3Ounces)42.99
| Action:      | think[The                        | first two | items are      | not          | what I want.] |
| ------------ | -------------------------------- | --------- | -------------- | ------------ | ------------- |
| Observation: | OK.                              |           |                |              |               |
| Action:      | click[Next>]Observation:         |           | Invalidaction! |              |               |
| Action:      | think[Ineedtorefinemysearch.]    |           |                | Observation: | OK.           |
| Action:      | click[<BacktoSearch]Observation: |           |                |              | Invalidac-    |
tion!
Action: click[BacktoSearch]
STATUS:FAIL
| Reflection: | Inthisattempt,Iwasunsuccessful. |     |     |     | Theinitial |
| ----------- | ------------------------------- | --- | --- | --- | ---------- |
searchresultswerenottheproductsthatIwaslookingfor.
Nexttime,Iwilldosearch[“vegetarianbacon”]forabroader
search.Iwillcheckthatthenewresultswillfulfillthegluten
| freeand4ouncepackof2constraints. |     |     |     | Iwillcontinueto |     |
| -------------------------------- | --- | --- | --- | --------------- | --- |
refinemysearchessothatIcanfindmoreproducts.
| Previoustrial: | trajectoryReflection:”’ |     |     |     |     |
| -------------- | ----------------------- | --- | --- | --- | --- |
23