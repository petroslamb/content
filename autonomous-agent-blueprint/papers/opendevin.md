<!-- AGENT BLUEPRINT METADATA START -->
# OpenHands: An Open Platform for AI Software Developers as Generalist Agents

- Year: 2025
- Primary chapter: Action Systems and Tool Use
- Method category: coding-agent platform
- Practical role: generalist developer-agent platform reference
- Key contribution: Pushes the coding-agent idea toward a broader developer platform.
- Major limitation: The local filename is an alias mismatch and should not be treated as the paper title.
- Confidence: Medium
- Canonical link: https://arxiv.org/abs/2407.16741

## Local Note Body

<!-- AGENT BLUEPRINT METADATA END -->

PublishedasaconferencepaperatICLR2025
| OPENHANDS: |     | AN OPEN | PLATFORM |     |     |
| ---------- | --- | ------- | -------- | --- | --- |
FOR
| AI SOFTWARE | DEVELOPERS |     | GENERALIST |     | AGENTS |
| ----------- | ---------- | --- | ---------- | --- | ------ |
AS
XingyaoWang1,10,BoxuanLi2,YufanSong2,FrankF.Xu2,XiangruTang3,
MingchenZhuge6,JiayiPan4,YueqiSong2,BowenLi,JaskiratSingh7,
HoangH.Tran8,FuqiangLi,RenMa,MingzhangZheng,BillQian3,YanjunShao3,
NiklasMuennighoff5,YizheZhang,BinyuanHui9,JunyangLin9,
RobertBrennan10,HaoPeng1,HengJi1,GrahamNeubig2,10
| 1UIUC 2CMU      | 3Yale 4UCBerkeley | 5ContextualAI | 6KAUST | 7ANU |     |
| --------------- | ----------------- | ------------- | ------ | ---- | --- |
| 8HCMUT 9Alibaba | 10AllHandsAI      |               |        |      |     |
5202 rpA 81  ]ES.sc[  3v14761.7042:viXra
| xingyao6@illinois.edu, |     | gneubig@cs.cmu.edu |     |     |     |
| ---------------------- | --- | ------------------ | --- | --- | --- |
ABSTRACT
Softwareisoneofthemostpowerfultoolsthatwehumanshaveatourdisposal;
| it allows  | a skilled programmer                                    | to interact | with the world | in complex | and pro- |
| ---------- | ------------------------------------------------------- | ----------- | -------------- | ---------- | -------- |
| foundways. | Atthesametime,thankstoimprovementsinlargelanguagemodels |             |                |            |          |
(LLMs),therehasalsobeenarapiddevelopmentinAIagentsthatinteractwith
| andaffectchangeintheirsurroundingenvironments. |                                                    |     | Inthispaper,weintroduce |     |     |
| ---------------------------------------------- | -------------------------------------------------- | --- | ----------------------- | --- | --- |
| OpenHands(f.k.a.                               | OpenDevin),aplatformforthedevelopmentofpowerfuland |     |                         |     |     |
flexibleAIagentsthatinteractwiththeworldinsimilarwaystothoseofahuman
| developer:                                                    | bywritingcode,interactingwithacommandline,andbrowsingthe       |     |     |              |         |
| ------------------------------------------------------------- | -------------------------------------------------------------- | --- | --- | ------------ | ------- |
| web.                                                          | Wedescribehowtheplatformallowsfortheimplementationofnewagents, |     |     |              |         |
| safeinteractionwithsandboxedenvironmentsforcodeexecution,     |                                                                |     |     | coordination |         |
| betweenmultipleagents,andincorporationofevaluationbenchmarks. |                                                                |     |     |              | Basedon |
ourcurrentlyincorporatedbenchmarks,weperformanevaluationofagentsover
15challengingtasks,includingsoftwareengineering(e.g.,SWE-BENCH)andweb
| browsing(e.g.,WEBARENA),amongothers. |     |     | ReleasedunderthepermissiveMIT |     |     |
| ------------------------------------ | --- | --- | ----------------------------- | --- | --- |
license,OpenHandsisacommunityprojectspanningacademiaandindustrywith
morethan2.1Kcontributionsfromover188contributors.
|     | Code  | https://github.com/All-Hands-AI/OpenHands |     |     |     |
| --- | ----- | ----------------------------------------- | --- | --- | --- |
|     | Slack | http://bit.ly/OpenHands-Slack             |     |     |     |
1 INTRODUCTION
Powered by large language models (LLMs; OpenAI 2024b; Team et al. 2023; Jiang et al. 2024;
Changetal.2024),user-facingAIsystems(suchasChatGPT)havebecomeincreasinglycapable
ofperformingcomplextaskssuchasaccuratelyrespondingtouserqueries,solvingmathproblems,
Inparticular,AIagents,systemsthatcanperceiveandactupontheexternal
andgeneratingcode.
environment, have recently received ever-increasing research focus. They are moving towards
performingcomplextaskssuchasdevelopingsoftware(Jimenezetal.,2024),navigatingreal-world
websites(Zhouetal.,2023a),doinghouseholdchores(Ahnetal.,2022),orevenperformingscientific
research(Boikoetal.,2023;Tangetal.,2024a).
AsAIagentsbecomecapableoftacklingcomplexproblems,theirdevelopmentandevaluationhave
alsobecomechallenging. Therearenumerousrecenteffortsincreatingopen-sourceframeworksthat
facilitatethedevelopmentofagents(Hongetal.,2023;Chenetal.,2024;Wuetal.,2023). These
agent frameworks generally include: 1) interfaces through which agents interact with the world
(suchasJSON-basedfunctioncallsorcodeexecution),2)environmentsinwhichagentsoperate,
and3)interactionmechanismsforhuman-agentoragent-agentcommunication. Theseframeworks
streamlineandeasethedevelopmentprocessinvariousways(Tab.1,§C).
WhendesigningAIagents, wecanalsoconsiderhowhumaninteractswiththeworld. Themost
powerful way in which humans currently interact with the world is through software – software
1

PublishedasaconferencepaperatICLR2025
Figure 1: OpenHands User Interface (UI, §D) allows users to view files, check executed bash
commands/Pythoncode,observetheagent’sbrowseractivity,anddirectlyinteractwiththeagent.
powers every aspect of our life, supporting everything from the logistics for basic needs to the
advancement of science, technology, and AI itself. Given the power of software, as well as the
existingtoolingarounditsefficientdevelopment,use,anddeployment,itprovidestheidealinterface
forAIagentstointeractwiththeworldincomplexways.However,buildingagentsthatcaneffectively
developsoftwarecomeswithitsownuniquechallenges. Howcanweenableagentstoeffectively
createandmodifycodeincomplexsoftwaresystems? Howcanweprovidethemwithtoolstogather
informationon-the-flytodebugproblemsorgathertask-requisiteinformation? Howcanweensure
thatdevelopmentissafeandavoidsnegativesideeffectsontheusers’systems?
Inthispaper,weintroduceOpenHands(f.k.a.OpenDevin),acommunity-drivenplatformdesignedfor
thedevelopmentofgeneralistandspecialistAIagentsthatinteractwiththeworldthroughsoftware.1
Itfeatures:
(1) Aninteractionmechanismwhichallowsuserinterfaces,agents,andenvironmentstointeract
throughaneventstreamarchitecturethatispowerfulandflexible(§2.1).
(2) Aruntimeenvironmentthatconsistsofadocker-sandboxedoperatingsystemwithabashshell,
awebbrowser,andIPythonserverthattheagentscaninteractwith(§2.2).
(3) Aninterfaceallowingtheagenttointeractwiththeenvironmentinamannersimilartoactual
softwareengineers(§2.3). Weprovidethecapabilityforagentstoa)createandeditcomplex
software,b)executearbitrarycodeinthesandbox,andc)browsewebsitestocollectinformation.
(4) Multi-agentdelegation,allowingmultiplespecializedagentstoworktogether(§2.4).
(5) Evaluationframework,facilitatingtheevaluationofagentsacrossawiderangeoftasks(§4).
Importantly,OpenHandsisnotjustaconceptualframework,butitalsoincludesacomprehensive
andimmediatelyusableimplementationofagents,environments,andevaluations. Asofthiswriting,
OpenHandsincludesanagenthubwithover10implementedagents(§3),includingastronggeneralist
agentimplementedbasedontheCodeActarchitecture(Wangetal.,2024a),withadditionsforweb
browsing(ServiceNow)andcodeeditingspecialists(Yangetal.,2024). Interactionwithusersis
implementedthroughachat-baseduserinterfacethatvisualizestheagent’scurrentactionsandallows
1WhileinitiallyinspiredbyAIsoftwareengineerDevin(Cognition.ai),OpenHandshasquicklyevolvedto
supportmuchwiderrangeofapplicationsbeyondsoftwareengineeringthroughdiversecommunitycontributions.
2

PublishedasaconferencepaperatICLR2025
| User Interface |     | Event Stream                                |     |     | Agent Runtime |     |
| -------------- | --- | ------------------------------------------- | --- | --- | ------------- | --- |
| Command Line   |     | where all Action-Observation(s) are tracked |     |     |               |     |
where each Action execution
| Web UI                   |                                     |                                                      |                                  |                                                    | leads to an Observation |     |
| ------------------------ | ----------------------------------- | ---------------------------------------------------- | -------------------------------- | -------------------------------------------------- | ----------------------- | --- |
| IDE Plugins Multi-turn
 | [1] Message (source=user)
          |                                                      | [6] CmdRunAction (source=agent)
 |                                                    |                         |     |
| U s e r - A g e n t
     | C a n   y o u   cr e a t e  a   lis | t  o f  n u m b e rs   fro m  1  t o   1 0 ,  a n d  | I  h a v e   c r e a t e d  a  P | y th o n  f il e   `a p p .p y `   th a t  w il l  |                         |     |
[...] In t e r a c ti o n cr e a t e  a   w e b   p a g e  t o  d i sp l ay   th e m  a t p o r t   5 0 0 0 ? d is p l a y   a  l is t  o f  n u m b e rs  f r o m   1  to  1 0   w h e n  y o u run  Docker Sandbox
it. Let me run the server for you:

|                                   |                                 |                                     | < e x e c u t e _ b a s h >
 |                       | O p e n H a n d s   a u t o m      | a t i c a l l y   i n s t a ll   |
| --------------------------------- | ------------------------------- | ----------------------------------- | ---------------------------- | --------------------- | ---------------------------------- | -------------------------------- |
|                                   | [ 2 ]   I P y t h o n R u n C e | ll A c t i o n   ( s o urce=agent)
 | p y t h o n 3   a p p . p y  |  > server.log 2>&1 &
 | “ a c t i o n   e x e c u t i o n  |   A P I ”   i n t o   u s e r -  |
|                                   | S u r e !   L e t  m e   c re a | t e  a  f i l e  fi r s t :
        |                              |                       | pr o v i d e d  a r b i t r a r y  | d o c k e r   i m a g e s        |
| Event History
                    | < e x e c u t e _ i p y t h     | o n >

                             | c a t   s e r v e r . l o g
 |                       |                                    |                                  |
| [Past Action(s) & Observation(s)] | create_file('app.py')           |                                     | </execute_bash>              |                       | Action                             |                                  |
</execute_ipython>
|                    |                                                      |                                                            | [ 7 ]   C m d R u n O b s e                     | r v a t io n
                                             | O pe n H an d s - | m a i n t a in e d
   |
| ------------------ | ---------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------- | ----------------- | --------------------- |
| Agent              | [ 3 ]  IP y t h o n R u n C e                        | ll O b s e r v a t io n
                                   | [ 1 ]   1 2 4
                                  |                                                           |                   |                       |
|                    | [ Fi l e:   / w o r ks p a c e/                      | a p p .p y   ( 1   l ines total)]
                         | *   S e r v i n g  F l as k   a                 | p p   ' ap p'
                                            | A c ti on  E x e  | c ut i o n   A P I    |
|                    | 1|
                                                  |                                                            |  * Debug mode: off
                             |                                                           |                   |                       |
| produce new action | [File app.py created.]                               |                                                            | W A R N I N G :   T h i s   i s                 | a   d e v e l o p m e n t   s e r v e r .  D o  not       |                   |                       |
|                    |                                                      |                                                            | u s e   i t   i n   a   p r o d u               | c t i o n   d e p l o y m e n t .  U s e   a              | I n te r          | ac t iv e  P y th on  |
|                    |                                                      |                                                            | p r o d u c t i o n  W S G I   s                | e r v e r   i n s t e a d .
                              | ( IP y th         | o n )  S er v er      |
|                    | [4] IPythonRunCellAction (source=agent)
             |                                                            |  * Running on http://127.0.0.1:5000
            |                                                           |                   |                       |
|                    | I will write the Python code for starting a server.
 |                                                            | Press CTRL+C to quit                            |                                                           |                   |                       |
| Action             | < e x e c u t e _ i p y t h                          | o n >

                                                    |                                                 |                                                           |                   |                       |
|                    | E D I T E D _ C O D E = \ " \ " \ "                  | [ O m i tt e d   f o r   B r e v i t y ] \ " \ " \ "       |                                                 |                                                           | Bash Shell        |                       |
|                    | e d i t _ f i l e ( s t a ir t p= y1 t,              | h  e on nd >= 1,   c o n t e n t = E D I T E D _ C O D E ) | [ 8 ]  B r o w s e I n t e r a c                | t i ve A c ti o n   (s o u r c e = a g e n t )
           |                   |                       |
|                    | < / e x e c u t e _                                  |                                                            | T h e  s e r ve r   is   r u n n                | i n g  o n  p o r t  5 0 0 0   w i th   P ID   1 24. Let  |                   |                       |
| Abstraction        |                                                      |                                                            | me browse to the page at http://127.0.0.1:5000
 |                                                           |                   |                       |
|                    | [5] IPythonRunCellObservation
                       |                                                            | <execute_browse>
                               |                                                           | Browser
          |                       |
|                    | [... Omitted for Brevity ...]
                       |                                                            | goto("http://127.0.0.1:5000")
                  |                                                           |                   |                       |
Event Stream: List[Action_1,  4|@app.route('/')
 </execute_browse> Playwright Chromium
5|def index():

| Observation_1, Action_2, ...]
 | 6|    numbers = list(range(1, 11))
 |     |     |     |     |     |
| ------------------------------ | ----------------------------------- | --- | --- | --- | --- | --- |
Agent: Event History -> Action
 7|    return str(numbers)
  [9] BrowserOutputObservation
 Observation
| Runtime: Action -> Observation | [... Omitted for Brevity ...] [File updated.] |     |  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] |     |     |     |
| ------------------------------ | --------------------------------------------- | --- | -------------------------------- | --- | --- | --- |
Figure2: OpenHandsconsistsof3maincomponents: 1)Agentabstractionwherecommunitycan
contributedifferentimplementationofagents(§2.1)intoagenthub(§3);2)Eventstreamfortracking
historyofactionsandobservations;3)Runtimetoexecuteallactionsintoobservations(§2.2).
forreal-timefeedback(Fig.1,§D).Furthermore,theevaluationframeworkcurrentlysupports15
benchmarks,whichweusetoevaluateouragents(§4).
ReleasedunderapermissiveMITlicenseallowingcommercialuse,OpenHandsispoisedtosupport
adiversearrayofresearchandreal-worldapplicationsacrossacademiaandindustry. OpenHands
hasgainedsignificanttraction,with32KGitHubstarsandmorethan2.1Kcontributionsfromover
188contributors. WeenvisionOpenHandsasacatalystforfutureresearchinnovationsanddiverse
applicationsdrivenbyabroadcommunityofpractitioners.
| 2 OPENHANDS | ARCHITECTURE |     |     |     |     |     |
| ----------- | ------------ | --- | --- | --- | --- | --- |
WenextdescribeusingOpenHandsindetail.Inparticular,wediscuss1)howtodefineandimplement
an agent (§2.1), 2) how each action execution leads to an observation (§2.2), 3) how to reliably
manageandextendcommonlyusedskillsforagents(§2.3),and4)howtocomposemultipleagents
| togetherfortasksolving(§2.4). |     | Fig.2providesanoverview. |     |     |     |     |
| ----------------------------- | --- | ------------------------ | --- | --- | --- | --- |
2.1 AGENTDEFINITIONANDIMPLEMENTATION
Anagentcanperceivethestateoftheenvironment(e.g.,prioractionsandobservations)andproduce
anactionforexecutionwhilesolvingauser-specifiedtask.
The State and Event Stream. In OpenHands, the state is a data structure that encapsulates all
relevantinformationfortheagent’sexecution. Akeycomponentofthisstateistheeventstream,
which is a chronological collection of past actions and observations, including the agent’s own
actionsanduserinteractions(e.g.,instructions,feedback). Inadditiontotheeventstream,thestate
incorporatesauxiliaryinformationforagent’soperation,suchastheaccumulativecostofLLMcalls,
metadatatotrackmulti-agentdelegation(§2.4),andotherexecution-relatedparameters.
Actions. Inspired by CodeAct (Wang et al., 2024a), OpenHands connects an agent with
the environment through a core set of general actions. Actions IPythonRunCellAction
and CmdRunAction enable the agent to execute arbitrary Python code and bash com-
mands inside the sandbox environment (e.g., a securely isolated Linux operating system).
BrowserInteractiveActionenablesinteractionwithawebbrowserwithadomain-specific
languageforbrowsingintroducedbyBrowserGym(Drouinetal.,2024). Theseactionswerechosen
toprovideacomprehensiveyetflexiblesetofprimitivescoveringmosttasksperformedbyhuman
softwareengineersandanalysts. Theactionspacebasedonprogramminglanguages(PL)ispowerful
3

PublishedasaconferencepaperatICLR2025
andflexibleenoughtoperformanytaskwithtoolsindifferentforms(e.g.,Pythonfunction,REST
API,etc.)whilebeingreliableandeasytomaintain(Wangetal.,2024a).
| This design | is also      | compatible | with |                |            |            |              |             |
| ----------- | ------------ | ---------- | ---- | -------------- | ---------- | ---------- | ------------ | ----------- |
|             |              |            |      | Figure         | 3: Minimal | example of | implementing | an agent in |
| existing    | tool-calling | agents     | that | re- OpenHands. |            |            |              |             |
quirealistofpre-definedtools(Chase,
class MinimalAgent:
| 2022). | That is, users | can | easily de- |     |                 |          |     |     |
| ------ | -------------- | --- | ---------- | --- | --------------- | -------- | --- | --- |
|        |                |     |            |     | def reset(self) | -> None: |     |     |
finetoolsusingPLsupportedinprimi- self.system_message = "You are a helpful assistant ..."
tiveactions(e.g.,writeaPythonfunc-
|                 |                  |           |            |     | def step(self,                  | state: State):                    |                      |     |
| --------------- | ---------------- | --------- | ---------- | --- | ------------------------------- | --------------------------------- | -------------------- | --- |
|                 |                  |           |            |     | messages:                       | list[dict[str, str]]              | = [                  |     |
| tion for        | calculator)      | and       | make those |     |                                 |                                   |                      |     |
|                 |                  |           |            |     | {'role':                        | 'system', 'content':              | self.system_message} |     |
| tools available | to               | the agent | through    |     | ]                               |                                   |                      |     |
|                 |                  |           |            |     | for prev_action,                | obs in state.history:             |                      |     |
| JSON-style      | function-calling |           | experi-    |     |                                 |                                   |                      |     |
|                 |                  |           |            |     | action_message                  | = get_action_message(prev_action) |                      |     |
| ences (Qin      | et al.,          | 2023).    | Moreover,  |     | messages.append(action_message) |                                   |                      |     |
the framework’s powerful PL-based obs_message = get_observation_message(obs)
messages.append(obs_message)
primitivesfurthermakeitpossiblefor
|     |     |     |     |     | # use llm | to generate response | (e.g., thought, | action) |
| --- | --- | --- | --- | --- | --------- | -------------------- | --------------- | ------- |
the agents to create tools by them- response = self.llm.do_completion(messages)
| selves (e.g.,                   | by  | generating | Python       |     |                                        |                   |             |     |
| ------------------------------- | --- | ---------- | ------------ | --- | -------------------------------------- | ----------------- | ----------- | --- |
|                                 |     |            |              |     | # parse and                            | execute action in | the runtime |     |
| functions,Yuanetal.2023)whenAPI |     |            |              |     | action = self.parse_response(response) |                   |             |     |
| to complete                     | the | task is    | unavailable. |     | if self.is_finish_command(action):     |                   |             |     |
return AgentFinishAction()
Referto§2.3forhowthesecorePL-
|     |     |     |     |     | elif self.is_bash_command(action): |     |     |     |
| --- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --- |
return CmdRunAction(command=action.command)
| basedactionscanbecomposedintoa |     |     |     |     | elif self.is_python_code(action): |     |     |     |
| ------------------------------ | --- | --- | --- | --- | --------------------------------- | --- | --- | --- |
diversesetoftools. return IPythonRunCellAction(code=action.code)
|     |     |     |     |     | elif self.is_browser_action(action): |     |     |     |
| --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- |
Observations. Observationsdescribe return BrowseInteractiveAction(code=action.code)
else:
theenvironmentalchanges(e.g.,exe- return MessageAction(content=action.message)
cutionresultofprioractions,textmessagesfromthehumanuseretc.)thattheagentobserves.
ImplementaNewAgent. Theagentabstractionisdesignedtobesimpleyetpowerful,allowing
userstocreateandcustomizeagentsforvarioustaskseasily. Thecoreoftheagentabstractionliesin
thestepfunction,whichtakesthecurrentstateasinputandgeneratesanappropriateactionbased
ontheagent’slogic. SimplifiedexamplecodefortheagentabstractionisillustratedinFig.3. By
providingthisabstraction,OpenHandsallowstheuserstofocusondefiningdesiredagentbehavior
andlogicwithoutworryingaboutthelow-leveldetailsofhowactionsareexecuted(§2.2).
| 2.2 AGENTRUNTIME: |     |     | HOWEXECUTIONOFACTIONSRESULTSINOBSERVATIONS |     |     |     |     |     |
| ----------------- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- |
AgentRuntimeprovidesageneralenvironmentthatequipstheagentwithanactionspacecomparable
tothatofhumansoftwaredevelopers,enablingOpenHandsagentstotackleawiderangeofsoftware
developmentandweb-basedtasks,includingcomplexsoftwaredevelopmentworkflows,dataanalysis
projects,webbrowsingtasks,andmore. Itallowstheagenttoaccessabashterminaltoruncodeand
commandlinetools,utilizeaJupyternotebookforwritingandexecutingcodeon-the-fly,andinteract
withawebbrowserforweb-basedtasks(e.g.,informationseeking).
DockerSandbox. Foreachtasksession,OpenHandsspinsupasecurelyisolateddockercontainer
sandbox, where all the actions from the event stream are executed. OpenHands connects to the
sandboxthroughaRESTAPIserverrunninginsideit(i.e.,theOpenHandsactionexecutionAPI),
executesarbitraryactions(e.g.,bashcommand,pythoncode)fromtheeventstream,andreturnsthe
executionresultsasobservations. Aconfigurableworkspacedirectorycontainingfilestheuserwants
theagenttoworkonismountedintothatsecuresandboxforOpenHandsagentstoaccess.
OpenHandsActionExecutionAPI.OpenHandsmaintainsanAPIserverthatrunsinsidethedocker
sandboxtolistenforactionexecutionrequestsfromtheeventstream. TheAPIservermaintains:
(1) Abashshellthatconnectswiththeoperatingsystemenvironment(specifiedbythedockerimage)
forcommandexecution.
(2) AJupyterIPythonservertohandleinteractivepython(IPython)codeexecutionrequestsand
returntheexecutionresultsbacktotheeventstream.
(3) AChromiumbrowserbasedonPlaywright. Theproviderprovidesasetofactionprimitives
definedbyBrowserGym(ServiceNow;Drouinetal.,2024),suchasnavigation,clicking,typing,
andscrolling. Thefullsetofactionsisdetailedin§J.Afterexecutingtheseactions,thebrowser
4

PublishedasaconferencepaperatICLR2025
runtime provides a rich set of observations about the current state of the browser, including
HTML,DOM,accessibilitytree(Mozilla),screenshot,openedtabs,etc.
ArbitraryDockerImageSupport. OpenHandsallowsagentstorunonarbitraryoperatingsystems
with different software environments by supporting runtime based on arbitrary docker images.
OpenHandsimplementsabuildmechanismthattakesauser-providedarbitrarydockerimageand
installsOpenHandsactionexecutionAPIintothatimagetoallowforagentinteractions. Weinclude
adetaileddescriptionofOpenHandsagentruntimein§F.
2.3 AGENTSKILLS: THEEXTENSIBLEAGENT-COMPUTERINTERFACE
SWE-Agent(Yangetal.,2024)highlightstheimportanceofacarefullycraftedAgent-Computer
Interface (ACI, i.e., specialized tools for particular tasks) in successfully solving complex tasks.
However,creating,maintaining,anddistributingawidearrayoftoolscanbeadauntingengineering
challenge,especiallywhenwewanttomakethesetoolsavailabletodifferentagentimplementations
(§3). Totacklethese,webuildanAgentSkillslibrary,atoolboxdesignedtoenhancethecapabilities
ofagents,offeringutilitiesnotreadilyavailablethroughbasicbashcommandsorpythoncode.
Easy to create and extend tools. AgentSkills is designed as a Python package consisting of
different utility functions (i.e., tools) that are automatically imported into the Jupyter IPython
environment(§2.2). TheeaseofdefiningaPythonfunctionasatoollowersthebarrierforcom-
munity members to contribute new tools to the library. The generality of Python packages also
allowsdifferentagentimplementationstoeasilyleveragethesetoolsthroughoneofourcoreaction
IPythonRunCellAction(§2.1).
Inclusioncriteriaandphilosophy. IntheAgentSkillslibrary,wedonotaimtowrapeverypossible
Pythonpackageandre-teachagentstheirusage(e.g.,LLMalreadyknowspandaslibrarythatcan
readCSVfile,sowedon’tneedtore-createatoolthatteachestheagenttoreadthesamefileformat).
Weonlyaddanewskillwhen: (1)itisnotreadilyachievableforLLMtowritecodedirectly(e.g.,
editcodeandreplacecertainlines),and/or(2)itinvolvescallinganexternalmodel(e.g.,callinga
speech-to-textmodel,ormodelforcodeediting(Sanger)).
Currentlysupportedskills. AgentSkillslibraryincludesfileeditingutilitiesadaptedfromSWE-
Agent (Yang et al., 2024) and Aider (Gauthier) like edit_file, which allows modifying an
existingfilefromaspecifiedline;scrollingfunctionsscroll_upandscroll_downforviewing
a different part of files. It also contains tools that support reading multi-modal documents, like
parse_imageandparse_pdfforextractinginformationfromimagesusingvision-language
models(e.g.,GPT-4V)andreadingtextfromPDFs,respectively. Acompletelistofsupportedskills
canbefoundin§I.
2.4 AGENTDELEGATION: COOPERATIVEMULTI-AGENTINTERACTION
OpenHandsallowsinteractionsbetweenmultipleagentsaswell. Tothisend,weuseaspecialaction
typeAgentDelegateAction,whichenablesanagenttodelegateaspecificsubtasktoanother
agent. Forexample,thegeneralistCodeActAgent,withlimitedsupportforweb-browsing,canuse
AgentDelegateActiontodelegatewebbrowsingtaskstothespecializedBrowsingAgentto
performmorecomplexbrowsingactivity(e.g.,navigatetheweb,clickbuttons,submitforms,etc.).
3 AGENTHUB: A HUB OF COMMUNITY-CONTRIBUTED AGENTS
Basedonouragentabstraction(§2.1),OpenHandssupportsawiderangeofcommunity-contributed
agentimplementationsforenduserstochoosefromandactasbaselinesfordifferentagenttasks.
CodeActAgent. CodeActAgentisthedefaultgeneralistagentbasedontheCodeActframework
(Wangetal.,2024a). Ateachstep,theagentcan(1)conversetocommunicatewithhumansinnatural
languagetoaskforclarification,confirmation,etc.,or(2)toperformthetaskbyexecutingcode(a.k.a.,
CodeAct), including executing bash commands, Python code, or browser-specific programming
language(§2.2). Thisgeneralactionspaceallowstheagent(v1.5andabove)toperformvarioustasks,
includingeditingfiles,browsingtheweb,runningprograms,etc.
5

PublishedasaconferencepaperatICLR2025
Table1: ComparisonofdifferentAIagentframeworks(§C).SWErefersto‘softwareengineering’.
Standardizedtoollibrary: ifframeworkcontainsreusabletoolsfordifferentagentimplementations
(§2.3);Built-insandbox&codeexecution: ifitsupportssandboxedexecutionofarbitraryagent-
generated code; Built-in web browser: if it provides agents access to a fully functioning web
browser;Human-AIcollaboration: ifitenablesmulti-turnhuman-AIcollaboration(e.g.,human
caninterrupttheagentduringtaskexecutionand/orprovideadditionalfeedbackandinstructions);
AgentHub: ifithostsimplementationsofvariousagents(§3);EvaluationFramework: ifitoffers
systematicevaluationofimplementedagentsonchallengingbenchmarks(§4);AgentQC(Quality
Control): iftheframeworkintegratestests(§E)toensureoverallframeworksoftwarequality.
|     |     | G r a p h ic | S t a n d a r d i z e d | Bu il t -i n S a n | d b o x Bu il t -i n W eb | M u lt i- a g e n t H u m a | n -A I | E v a lu a | ti o n A ge nt |
| --- | --- | ------------ | ----------------------- | ------------------ | ------------------------- | --------------------------- | ------ | ---------- | -------------- |
Framework Domain Use r I n te r face T o o l L i b r a r y & C o d e E x e c u ti o n B r o w s er C ol la b o r a t io n C ol la b o ra tio n AgentHub F r a m e w o r k Q C
AutoGPTGravitas(2023) General (cid:34) (cid:37) (cid:37) (cid:37) (cid:37) (cid:37) (cid:34) (cid:37) (cid:34)
LangChain(Chase,2022) General (cid:37) (cid:34) (cid:37)∗ (cid:37)∗ (cid:37) (cid:37) (cid:34) (cid:37) (cid:37)
MetaGPT(Hongetal.,2023) General (cid:37) (cid:34) (cid:37) (cid:34) (cid:34) (cid:37) (cid:34) (cid:37) (cid:34)
AutoGen(Wuetal.,2023) General (cid:37) (cid:34) (cid:34) (cid:34) (cid:34) (cid:34) (cid:34) (cid:34) (cid:37)
AutoAgents(Chenetal.,2024) General (cid:37) (cid:37) (cid:37) (cid:37) (cid:34) (cid:37) (cid:37) (cid:37) (cid:37)
Agents(Zhouetal.,2023b) General (cid:37) (cid:37) (cid:37) (cid:37) (cid:34) (cid:34) (cid:37) (cid:37) (cid:37)
|                    |         | (cid:34) | (cid:34) | (cid:37) | (cid:34) | (cid:34) (cid:37) | (cid:34) | (cid:37) | (cid:37) |
| ------------------ | ------- | -------- | -------- | -------- | -------- | ----------------- | -------- | -------- | -------- |
| Xagents(Team,2023) | General |          |          |          |          |                   |          |          |          |
OpenAgents(Xieetal.,2023) General (cid:34) (cid:37) (cid:34) (cid:34) (cid:37) (cid:37) (cid:34) (cid:37) (cid:37)
GPTSwarm(Zhugeetal.,2024) General (cid:37) (cid:34) (cid:37) (cid:37) (cid:34) (cid:34) (cid:37) (cid:37) (cid:37)
AutoCodeRover(Zhangetal.,2024b) SWE (cid:37) (cid:37) (cid:34) (cid:37) (cid:37) (cid:37) (cid:37) (cid:37) (cid:37)
SWE-Agent(Yangetal.,2024) SWE (cid:37) (cid:37) (cid:34) (cid:37) (cid:37) (cid:37) (cid:37) (cid:37) (cid:37)
OpenHands General (cid:34) (cid:34) (cid:34) (cid:34) (cid:34) (cid:34) (cid:34) (cid:34) (cid:34)
*Nonativesupport.Third-partycommercialoptionsareavailable.
Browsing Agent. We implemented a generalist web agent called Browsing Agent, to serve as a
simpleyeteffectivebaselineforwebagenttasks. TheagentissimilartothatinWebArena(Zhou
et al., 2023a), but with improved observations and actions, with only zero-shot prompting. Full
promptsarein§K.
GPTSwarm Agent. GPTSwarm (Zhuge et al., 2024) pioneers the use of optimizable graphs to
construct agent systems, unifying language agent frameworks through modularity. Each node
represents a distinct operation, while edges define collaboration and communication pathways.
Thisdesignallowsautomaticoptimizationofnodesandedges,drivingadvancementsincreating
multi-agentsystems.
MicroAgent(s). Inaddition,OpenHandsenablesthecreationofmicroagent,anagentspecialized
towardsaparticulartask. Amicroagentre-usesmostimplementationsfromanexistinggeneralist
agent (e.g., CodeAct Agent). It is designed to lower the barrier to agent development, where
communitymemberscansharespecializedpromptsthatworkwellfortheirparticularusecases.
4 EVALUATION
| To systematically   | track   | progress  | in       |         |                                  |     |                    |     |     |
| ------------------- | ------- | --------- | -------- | ------- | -------------------------------- | --- | ------------------ | --- | --- |
|                     |         |           |          | Table2: | EvaluationbenchmarksinOpenHands. |     |                    |     |     |
| building generalist | digital | agents,   | as       |         |                                  |     |                    |     |     |
|                     |         |           | Category |         | Benchmark                        |     | RequiredCapability |     |     |
| listed in Tab.      | 2, we   | integrate | 15 es-   |         |                                  |     |                    |     |     |
|                     |         |           |          |         | SWE-Bench(Jimenezetal.,2024)     |     | FixingGithubissues |     |     |
tablishedbenchmarksintoOpenHands. HumanEvalFix(Muennighoffetal.,2024) FixingBugs
|     |     |     |     |     | BIRD(Lietal.,2023b) |     | Text-to-SQL |     |     |
| --- | --- | --- | --- | --- | ------------------- | --- | ----------- | --- | --- |
These benchmarks cover software en- Software BioCoder(Tangetal.,2024c) Bioinformaticscoding
gineering, web browsing, and miscel- ML-Bench(Tangetal.,2024b) Machinelearningcoding
|                    |                  |     |     |     | GorillaAPIBench(Patiletal.,2023) |                             | SoftwareAPIcalling |                             |                  |
| ------------------ | ---------------- | --- | --- | --- | -------------------------------- | --------------------------- | ------------------ | --------------------------- | ---------------- |
|                    |                  |     |     |     | ToolQA(Zhuangetal.,2024)         |                             | Tooluse            |                             |                  |
| laneousassistance. | Inthissection,we |     |     |     |                                  |                             |                    |                             |                  |
|                    |                  |     | Web |     | W e b A r en a ( Z h             | o u e t a l . , 2 0 2 3 a ) | G o a l p          | l a n n i n g & r e a li st | ic b r o w s ing |
compareOpenHandstoopen-sourcere- M in i W o B + + ( L i u e t a l . , 2 0 1 8 ) Sh o r t t r a je c t o ry o n s y n th et i c w e b
produciblebaselinesthatdonotperform GAIA(Mialonetal.,2023) Tool-use,browsing,multi-modality
|     |     |     |     |     | GPQA(Reinetal.,2023) |     | Graduate-levelGoogle-proofQ&A |     |     |
| --- | --- | --- | --- | --- | -------------------- | --- | ----------------------------- | --- | --- |
manualpromptengineeringspecifically A g e n tB e n c h (L iu e t al . , 2 0 23) O p e r a t i n g s ys t e m in te r a c ti o n ( b a sh )
|     |     |     | Misc.Assistance |     | M I N T ( W a n g | et al ., 2 0 2 4 b ) | M u l ti - t | u r n m a t h an d c o | d e p r o b le m s |
| --- | --- | --- | --------------- | --- | ----------------- | -------------------- | ------------ | ---------------------- | ------------------ |
basedonthebenchmarkcontent. Please EntityDeductionArena(Zhangetal.,2024a) Statetracking&strategicplanning
|     |     |     |     |     | ProofWriter(Tafjordetal.,2021) |     | DeductiveLogicReasoning |     |     |
| --- | --- | --- | --- | --- | ------------------------------ | --- | ----------------------- | --- | --- |
notethatweuse‘OH’asshorthandfor
OpenHandsfortherestofthissection
forbrevityreasons.
4.1 RESULTOVERVIEW
InOpenHands,ourgoalistodevelopgeneraldigitalagentscapableofinteractingwiththeworld
throughsoftwareinterfaces(asexemplifiedbythecodeactionsdescribedin§2.1). Werecognizethat
asoftwareagentshouldexcelnotonlyincodeeditingbutalsoinwebbrowsingandvariousauxiliary
tasks,suchasansweringquestionsaboutcoderepositoriesorconductingonlineresearch.
6

PublishedasaconferencepaperatICLR2025
Table3: SelectedevaluationresultsforOpenHandsagents(§4). SeeTab.4(software),Tab.5(web),
Tab.6(miscellaneousassistance)forfullresultsacrossbenchmarks.
|       |       | Software(§4.2) | Web(§4.3) | Misc.(§4.4) |      |
| ----- | ----- | -------------- | --------- | ----------- | ---- |
| Agent | Model | SWE-BenchLite  | WebArena  | GPQA        | GAIA |
SoftwareEngineeringAgents
| SWE-Agent(Yangetal.,2024) | gpt-4-1106-preview |     | 18.0 | −   | − − |
| ------------------------- | ------------------ | --- | ---- | --- | --- |
AutoCodeRover(Zhangetal.,2024b) gpt-4-0125-preview 19.0 − − −
| Aider(Gauthier)          | gpt-4o&claude-3-opus |     | 26.3 | −   | − − |
| ------------------------ | -------------------- | --- | ---- | --- | --- |
| MoatlessTools(Örwall)    | claude-3.5-sonnet    |     | 26.7 | −   | − − |
| Agentless(Xiaetal.,2024) | gpt-4o               |     | 27.3 | −   | − − |
WebBrowsingAgents
| Lemur(Xuetal.,2023) | Lemur-chat-70b            |     | −   | 5.3 | − − |
| ------------------- | ------------------------- | --- | --- | --- | --- |
| Pateletal.(2024)    | Trained72Bw/syntheticdata |     | −   | 9.4 | − − |
AutoWebGLM(Laietal.,2024) Trained7Bw/human/agentannotation − 18.2 − −
AutoEval&Refine(Panetal.,2024) GPT-4+Reflexionw/GPT-4V − 20.2 − −
| WebArenaAgent(Zhouetal.,2023a) | gpt-4-turbo |     | −   | 14.4 | − − |
| ------------------------------ | ----------- | --- | --- | ---- | --- |
Misc.AssistanceAgents
| AutoGPT(Gravitas,2023) | gpt-4-turbo      |     | −   | −      | − 13.2 |
| ---------------------- | ---------------- | --- | --- | ------ | ------ |
|                        | Llama-2-70b-chat |     | −   | − 28.1 | −      |
Few-shotPrompting
|                                   | gpt-3.5-turbo-16k |     | −   | − 29.6 | −   |
| --------------------------------- | ----------------- | --- | --- | ------ | --- |
| +Chain-of-Thought(Reinetal.,2023) | gpt-4             |     |     | − 38.8 | −   |
OpenHandsAgents
|                  | gpt-4o-mini-2024-07-18 |     | 6.3  | 8.3        | − −    |
| ---------------- | ---------------------- | --- | ---- | ---------- | ------ |
| CodeActAgentv1.8 | gpt-4o-2024-05-13      |     | 22.0 | 14.5 ∗53.1 | −      |
|                  | claude-3-5-sonnet      |     | 26.0 | 15.3 52.0  | −      |
| GPTSwarmv1.0     | gpt-4o-2024-05-13      |     | −    | −          | − 32.1 |
*NumbersarereportedfromCodeActAgentv1.5.
Tab.3showcasesacuratedsetofevaluationresults. WhileOpenHandsagentsmaynotachievetop
performanceineverycategory,theyaredesignedwithgeneralityinmind. Notably,thesameCodeAct
agent,withoutanymodificationstoitssystemprompt,demonstratescompetitiveperformanceacross
threemajortaskcategories: softwaredevelopment,webinteraction,andmiscellaneoustasks. This
isparticularlysignificantwhencomparedtothebaselineagents,whicharetypicallydesignedand
optimizedforspecifictaskcategories.
4.2 SOFTWAREENGINEERING
Next,wereportresultsspecificallyforsoftwareengineeringbenchmarksinTab.4.
SWE-Bench (Jimenez et al., 2024) is designed to assess agents’ abilities in solving real-world
GitHubissues,suchasbugreportsorfeaturerequests. Theagentinteractswiththerepositoryand
attemptstofixtheissueprovidedthroughfileeditingandcodeexecution. Theagent-modifiedcode
repositoryistestedagainstatestsuiteincorporatingnewtestsaddedfromhumandevelopers’fixes
forthesameissue. Eachtestinstanceaccompaniesapieceof“hinttext”thatconsistsofnatural
language suggestions for how to solve the problem. Throughout this paper, we report all results
withoutusinghinttext. Acanonicalsubset,SWE-benchLite,iscreatedtofacilitateaccessibleand
efficienttesting. Wedefaulttousethissubsetfortestingforcost-savingconsideration.2 Result. As
showninTab.4,ourmostrecentversionofCodeActAgentv1.8,usingclaude-3.5-sonnet,
achievesacompetitiveresolverateof26%comparedtootheropen-sourceSWEspecialists.
4.2.1 HUMANEVALFIX
HumanEvalFix(Muennighoffetal.,2024)tasksagentstofixabuginaprovidedfunctionwiththe
helpofprovidedtestcases. Thebugsarecreatedtoensureoneormoretestcasesfail. Wefocuson
thePythonsubsetofthebenchmarkandallowmodelstosolvethebugsbyself-debugovermultiple
turns, incorporating feedback from test execution. We follow the setup from Muennighoff et al.
(2024)usingpass@k(Chenetal.,2021). Results. InTab.4,OpenHandsCodeActAgentsuccessfully
fixes79.3%ofbugsinthePythonsplit. Thisissignificantlybetterthanallnon-agenticapproaches,
almostdoublingtheperformanceofStarCoder2-15B(Lozhkovetal.,2024;Lietal.,2023c).
While SWE-Agent achieves 87.7%, Yang et al. (2024) provides the model a full demonstration
ofasuccessfulsampletrajectoryfixingoneofthebugsinthetestdataset(“1-shot”),whereasour
evaluationofOpenHandsis0-shot. AsHumanEvalFixhasbeencreatedbyhumansandallbugs
2Runningthecompletesetof2294instancescosts$6.9k,usingaconservativeestimateof$3perinstance.
7

PublishedasaconferencepaperatICLR2025
Table4: OpenHandsSoftwareEngineeringevaluationresults(§4.2).
| Agent | Model | SuccessRate(%) | $Avg.Cost |
| ----- | ----- | -------------- | --------- |
SWE-BenchLite(Jimenezetal.,2024),300instances,w/oHint
| SWE-Agent(Yangetal.,2024) | gpt-4-1106-preview |     | 18.0 1.67 |
| ------------------------- | ------------------ | --- | --------- |
gpt-4-0125-preview
| AutoCodeRover(Zhangetal.,2024b) |                            |     | 19.0 −    |
| ------------------------------- | -------------------------- | --- | --------- |
| Aider(Gauthier)                 | gpt-4o&claude-3-opus       |     | 26.3 −    |
|                                 | gpt-4o-mini-2024-07-18     |     | 7.0 0.01  |
| OHCodeActAgentv1.8              | gpt-4o-2024-05-13          |     | 22.0 1.72 |
|                                 | claude-3-5-sonnet@20240620 |     | 26.0 1.10 |
HumanEvalFix(Muennighoffetal.,2024),164instances
|                                  | BLOOMZ-176B                |     | 16.6 −    |
| -------------------------------- | -------------------------- | --- | --------- |
|                                  | OctoCoder-15B              |     | 30.4 −    |
| Prompting,0-shot                 | DeepSeekCoder-33B-Instruct |     |           |
|                                  |                            |     | 47.5 −    |
|                                  | StarCoder2-15B             |     | 48.6 −    |
| SWE-agent,1-shot(Yangetal.,2024) | gpt-4-turbo                |     | 87.7 −    |
|                                  | gpt-3.5-turbo-16k-0613     |     | 20.1 0.11 |
OHCodeActAgentv1.5,Generalist,0-shot. gpt-4o-2024-05-13 79.3 0.14
BIRD(Lietal.,2023b),300instances
|                    | CodeLlama-7B-Instruct |     | 18.3      |
| ------------------ | --------------------- | --- | --------- |
| Prompting,0-shot   |                       |     | -         |
|                    | CodeQwen-7B-Chat      |     | 31.3 -    |
|                    | gpt-4-1106-preview    |     | 42.7 0.19 |
| OHCodeActAgentv1.5 | gpt-4o-2024-05-13     |     | 47.3 0.11 |
ML-Bench(Tangetal.,2024b),68instances
|     | gpt-3.5-turbo |     | 11.0 - |
| --- | ------------- | --- | ------ |
prompting+BM25,0-shot
|                           | gpt-4-1106-preview     |     | 22.1 -    |
| ------------------------- | ---------------------- | --- | --------- |
|                           | gpt-4o-2024-05-13      |     | 26.2 -    |
| SWE-Agent(Yangetal.,2024) | gpt-4-1106-preview     |     | 42.6 1.91 |
|                           | gpt-4o                 |     | 64.4      |
| Aider(Gauthier)           |                        |     | -         |
|                           | gpt-4o-2024-05-13      |     | 76.5 0.25 |
| OHCodeActAgentv1.5        | gpt-4-1106-preview     |     | 58.8 1.22 |
|                           | gpt-3.5-turbo-16k-0613 |     | 13.2 0.12 |
BioCoder(Python)(Tangetal.,2024b),157instances
|     | gpt-3.5-turbo |     | 11.0 - |
| --- | ------------- | --- | ------ |
prompting,0-shot
|                    | gpt-4-1106-preview |     | 12.7 -    |
| ------------------ | ------------------ | --- | --------- |
| OHCodeActAgentv1.5 | gpt-4o-2024-05-13  |     | 27.5 0.13 |
GorillaAPIBench(Patiletal.,2023),1775instances
|                  | claude-v1          |     | 8.7 -  |
| ---------------- | ------------------ | --- | ------ |
| Prompting,0-shot | gpt-4-0314         |     | 21.2 - |
|                  | gpt-3.5-turbo-0301 |     | 29.7 - |
Gorilla,finetunedforAPIcalls,0-shot(Patiletal.,2023;Touvronetal.,2023) llama-7b 75.0 -
| OHCodeActAgentv1.5 | gpt-3.5-turbo-0125 |     | 21.6 0.002 |
| ------------------ | ------------------ | --- | ---------- |
|                    | gpt-4o-2024-05-13  |     | 36.4 0.04  |
ToolQA(Zhuangetal.,2024),800instances
|                                          | ChatGPT + CoT      |     | 5.1 -    |
| ---------------------------------------- | ------------------ | --- | -------- |
| Prompting,0-shot                         | ChatGPT            |     | 5.6 -    |
|                                          | Chameleon          |     | 10.6 -   |
|                                          | gpt-3.5-turbo      |     | 36.8 -   |
| ReAct,0-shot(Yaoetal.,2023;OpenAI,2024a) | gpt-3              |     | 43.1 -   |
|                                          | gpt-3.5-turbo-0125 |     | 2.3 0.03 |
OHCodeActAgentv1.5
|     | gpt-4o-2024-05-13 |     | 47.2 0.91 |
| --- | ----------------- | --- | --------- |
carefullyvalidated,achieving100%onthisbenchmarkisentirelyfeasible,whichweseektodoin
futureiterationsofOpenHands.
ML-Bench(Tangetal.,2024b)evaluatesagents’abilitytosolvemachinelearningtasksacross18
GitHub repositories. The benchmark comprises 9,641 tasks spanning 169 diverse ML problems,
requiring agents to generate bash scripts or Python code in response to user instructions. In the
sandboxenvironment,agentscaniterativelyexecutecommandsandreceivefeedback,allowingthem
tounderstandtherepositorycontextandfulfilluserrequirementsprogressively. Followingthesetup
fromtheoriginalpaper,weperformagentevaluationonthequartersubsetofML-Bench.
GorillaAPIBench(Patiletal.,2023)evaluatesagents’abilitiestouseAPIs. itincorporatestaskson
TorchHub,TensorHub,andHuggingFace. Duringtheevaluation,modelsaregivenaquestionrelated
toAPIusage,suchas"identifyanAPIcapableofconvertingspokenlanguageinarecordingtotext."
Correctnessisevaluatedbasedonwhetherthemodel’sAPIcallisinthecorrectdomain.
ToolQA (Zhuang et al., 2024) evaluates agents’ abilities to use external tools. This benchmark
includestasksonvarioustopicslikeflightstatus,coffeeprice,Yelpdata,andAirbnbdata,requiring
theuseofvarioustoolssuchastexttools,databasetools,mathtools,graphtools,codetools,and
systemtools. Itfeaturestwolevels: easyandhard. Easyquestionsfocusmoreonsingle-toolusage,
| whilehardquestionsemphasizereasoning. Weadopttheeasysubsetforevaluation. |     |     |     |
| ------------------------------------------------------------------------ | --- | --- | --- |
BioCoder(Tangetal.,2024c)isarepository-levelcodegenerationbenchmarkthatevaluatesagents’
performanceonbioinformatics-relatedtasks,specificallytheabilitytoretrieveandaccuratelyutilize
context. The original prompts contain the relevant context of the code; however, in this study,
wehaveremovedthemtodemonstratethecapabilityofOpenHandstoperformcontextretrieval,
8

PublishedasaconferencepaperatICLR2025
Table5: OpenHandsWebBrowsingEvaluationResults(§4.3).
| Agent | Model | SuccessRate(%) | $Avg.Cost |
| ----- | ----- | -------------- | --------- |
WebArena(Zhouetal.,2023a),812instances
| Lemur(Xuetal.,2023) | Lemur-chat-70b |     | 5.3 − |
| ------------------- | -------------- | --- | ----- |
Pateletal.(2024) Trained72Bwithself-improvementsyntheticdata 9.4 −
AutoWebGLM(Laietal.,2024) Trained7Bwithhuman/agenthybridannotation 18.2 −
AutoEval&Refine(Panetal.,2024) GPT-4+Reflexionw/GPT-4Vrewardmodel 20.2 −
|                                | gpt-3.5-turbo |     | 6.2 −  |
| ------------------------------ | ------------- | --- | ------ |
| WebArenaAgent(Zhouetal.,2023a) | gpt-4-turbo   |     | 14.4 − |
gpt-4o-mini-2024-07-18
|                                  |                            |     | 8.5 0.01  |
| -------------------------------- | -------------------------- | --- | --------- |
| OHBrowsingAgentv1.0              | gpt-4o-2024-05-13          |     | 14.8 0.15 |
|                                  | claude-3-5-sonnet-20240620 |     | 15.5 0.10 |
| OHCodeActAgentv1.8               | gpt-4o-mini-2024-07-18     |     | 8.3 −     |
|                                  | gpt-4o-2024-05-13          |     | 14.5 −    |
| viadelegationtoBrowsingAgentv1.0 | claude-3-5-sonnet-20240620 |     |           |
|                                  |                            |     | 15.3 −    |
MiniWoB++(Liuetal.,2018),125environments
WorkflowGuidedExploration(Liuetal.,2018) Trainedspecialistmodelwithenvironmentexploration 34.6 −
CC-NET(Humphreysetal.,2022) TrainedspecialistmodelwithRLandhumanannotatedBC 91.1 −
gpt-3.5-turbo-0125
| OHBrowsingAgentv1.0 |                   |     | 27.2 0.01 |
| ------------------- | ----------------- | --- | --------- |
|                     | gpt-4o-2024-05-13 |     | 40.8 0.05 |
OHCodeActAgentv1.8
|     | gpt-4o-2024-05-13 |     | 39.8 − |
| --- | ----------------- | --- | ------ |
viadelegationtoBrowsingAgentv1.0
self-debugging,andreasoninginmulti-turninteractions. BioCoderconsistsof157Pythonand50
Javafunctions,eachtargetingaspecificareainbioinformatics,suchasproteomics,genomics,and
otherspecializeddomains. Thebenchmarktargetsreal-worldcodebygeneratingcodeinexisting
repositorieswheretherelevantcodehasbeenmaskedout.
BIRD(Lietal.,2023b)isabenchmarkfortext-to-SQLtasks(i.e.,translatenaturallanguageinto
executableSQL)aimedatrealisticandlarge-scaledatabaseenvironments. Weselect300samples
fromthedevsettointegrateintoOpenHandsandevaluateonexecutionaccuracy. Additionally,we
extendthesettingbyallowingtheagenttoengageinmulti-turninteractionstoarriveatthefinalSQL
query,enablingittocorrecthistoricalresultsbyobservingtheresultsofSQLexecution.
4.3 WEBBROWSING
WereportevaluationresultsforwebbrowsingbenchmarksinTab.5.
WebArena (Zhou et al., 2023a) is a self-hostable, execution-based web agent benchmark that
allows agents to freely choose which path to take in completing their given tasks. WebArena
comprises812human-curatedtaskinstructionsacrossvariousdomains,includingshopping,forums,
developerplatforms,andcontentmanagementsystems. Results. FromTab.5,wecanseethatour
BrowsingAgentachievescompetitiveperformanceamongagentsthatuseLLMswithdomain-general
promptingtechniques.
MiniWoB++(Liuetal.,2018)isaninteractivewebbenchmark,withbuilt-inrewardfunctions. The
tasks are synthetically initialized on 125 different minimalist web interfaces. Unlike WebArena,
tasksareeasierwithoutpagechanges,requirefewersteps,andprovidelow-levelstep-by-steptask
directions. Notethatitcontainsaportionofenvironmentsthatrequirevisioncapabilitytotackle
successfully,andmanyexistingworkchoosetofocusonlyonasubsetofthetasks(Kimetal.,2024;
Lietal.,2023d;Shawetal.,2023). Still,wereporttheperformanceonthefullsetandonlyinclude
baselinesthatareevaluatedonthefullset.
4.4 MISCELLANEOUSASSISTANCE
ResultsformiscellaneousassistancebenchmarksarereportedinTab.6.
GAIA(Mialonetal.,2023)evaluatesagents’generaltask-solvingskills,coveringdifferentreal-world
scenarios. Itrequiresvariousagentcapabilities,includingreasoning,multi-modalunderstanding,
webbrowsing,andcoding. GAIAconsistsof466curatedtasksacrossthreelevels. SettingupGAIA
istraditionallychallengingduetothecomplexityofintegratingvarioustoolswiththeagent, but
OpenHands’sinfrastructure(e.g.,runtime§2.2,tools§2.3)simplifiestheintegrationsignificantly.
GPQA(Reinetal.,2023)evaluatesagents’abilityforcoordinatedtoolusewhensolvingchallenging
graduate-levelproblems. Tooluse(e.g.,python)andwebsearchareoftenusefultoassistagentsin
answeringthesequestionssincetheyprovideaccuratecalculationsthatLLMsareoftenincapableof
andaccesstoinformationoutsideoftheLLM’sparametricknowledgebase.
9

PublishedasaconferencepaperatICLR2025
Table6: OpenHandsmiscellaneousassistanceevaluationresults(§4.4).
| Agent | Model |     | SuccessRate(%) | $Avg.Cost |
| ----- | ----- | --- | -------------- | --------- |
GAIA(Mialonetal.,2023),L1validationset,53instances
|     | gpt-4-turbo |     | 13.2 | −   |
| --- | ----------- | --- | ---- | --- |
AutoGPT(Gravitas,2023)
|                | gpt-4-0125-preview |     | 30.2 | 0.110 |
| -------------- | ------------------ | --- | ---- | ----- |
| OHGPTSwarmv1.0 | gpt-4o-2024-05-13  |     | 32.1 | 0.050 |
GPQA(Reinetal.,2023),diamondset,198instances(referto§G,Tab.7forothersubsets)
|                       | Experthuman       |     | 81.3 | −   |
| --------------------- | ----------------- | --- | ---- | --- |
| Human(Reinetal.,2023) | Non-experthuman   |     | 21.9 | −   |
|                       | gpt-3.5-turbo-16k |     | 29.6 | −   |
Few-shotPrompting+Chain-of-Thought(Reinetal.,2023) gpt-4 38.8 −
claude-3-5-sonnet-20240620
| OHCodeActAgentv1.8 |     |     | 52.0 | 0.065 |
| ------------------ | --- | --- | ---- | ----- |
AgentBench(Liuetal.,2023),OS(bash)subset,144instances
|     | gpt-4 |     | 42.4 | −   |
| --- | ----- | --- | ---- | --- |
AgentBenchBaselineAgent(Liuetal.,2023)
|                    | gpt-3.5-turbo      |     | 32.6 | −     |
| ------------------ | ------------------ | --- | ---- | ----- |
|                    | gpt-4o-2024-05-13  |     | 57.6 | 0.085 |
| OHCodeActAgentv1.5 | gpt-3.5-turbo-0125 |     | 11.8 | 0.006 |
MINT(Wangetal.,2024b):mathsubset,225instances
| MINTBaselineAgent | gpt-4-0613        |     | 65.8 | −     |
| ----------------- | ----------------- | --- | ---- | ----- |
|                   | gpt-4o-2024-05-13 |     | 77.3 | 0.070 |
OHCodeActAgentv1.5
|     | gpt-3.5-turbo-16k-0613 |     | 33.8 | 0.048 |
| --- | ---------------------- | --- | ---- | ----- |
MINT(Wangetal.,2024b):codesubset,136instances
gpt-4-0613
| MINTBaselineAgent  |                        |     | 59.6 | −         |
| ------------------ | ---------------------- | --- | ---- | --------- |
|                    | gpt-4o-2024-05-13      |     | 50.0 | 0.087     |
| OHCodeActAgentv1.5 | gpt-3.5-turbo-16k-0613 |     |      | 5.2 0.030 |
ProofWriter(Tafjordetal.,2021),600instances
Few-shotPrompting+Chain-of-Thought(Panetal.,2023) gpt4 68.1 −
| Logic-LM(Panetal.,2023) | gpt4 + symbolic   | solver | 79.6 | −   |
| ----------------------- | ----------------- | ------ | ---- | --- |
| OHCodeActAgentv1.5      | gpt-4o-2024-05-13 |        | 78.8 | −   |
EntityDeductionArena(Zhangetal.,2024a),200instances
|     | gpt-4-0314 |     | 40.0 | −   |
| --- | ---------- | --- | ---- | --- |
Zero-shotPrompting(Zhangetal.,2024a)
|                    | gpt-3.5-turbo-0613     |     | 27.0 | −   |
| ------------------ | ---------------------- | --- | ---- | --- |
|                    | gpt-4o-2024-05-13      |     | 38.0 | −   |
| OHCodeActAgentv1.5 | gpt-3.5-turbo-16k-0613 |     | 24.0 | −   |
AgentBench(Liuetal.,2023)evaluatesagents’reasoninganddecision-makingabilitiesinamulti-
turn,open-endedgenerationsetting. Weselectedthecode-groundedoperatingsystem(OS)subset
with 144 tasks. Agents from OpenHands interact directly with the task-specific OS using bash
commandsinamulti-turnmanner,combininginteractionandreasoningtoautomatetaskcompletion.
MINT(Wangetal.,2024b)isabenchmarkdesignedtoevaluateagents’abilitytosolvechallenging
tasksthroughmulti-turninteractionsusingtoolsandnaturallanguagefeedbacksimulatedbyGPT-4.
WeusecodingandmathsubsetsusedinYuanetal.(2024). Wefollowtheoriginalpaperandallow
theagenttointeractwithuptofiveiterationswithtwochancestoproposesolutions.
ProofWriter(Tafjordetal.,2021)isasyntheticdatasetcreatedtoassessdeductivereasoningabilities
ofLLMs. SameasLogic-LM(Panetal.,2023),wefocusonthemostchallengingsubset,which
contains 600 instances requiring 5-hop reasoning. To minimize the impact of potential errors in
semanticparsing,weusethelogicalformsprovidedbyLogic-LM.
EntityDeductionArena(EDA)(Zhangetal.,2024a)evaluatesagents’abilitytodeduceunknown
entities through strategic questioning, akin to the 20 Questions game. This benchmark tests the
agent’s state tracking, strategic planning, and inductive reasoning capabilities over multi-turn
conversations. Weevaluatetwodatasets“Things”and“Celebrities”,eachcomprising100instances,
andreporttheaveragesuccessrateoverthesetwodatasets.
5 CONCLUSION
WeintroduceOpenHands,acommunity-drivenplatformthatenablesthedevelopmentofagentsthat
interactwiththeworldthroughsoftwareinterfaces. Byprovidingapowerfulinteractionmechanism,
asafesandboxedenvironment,essentialagentskills,multi-agentcollaborationcapabilities,anda
comprehensiveevaluationframework,OpenHandsacceleratesresearchinnovationsandreal-world
applicationsofagenticAIsystems. Despitechallengesindevelopingsafeandreliableagents(§A),
weareexcitedaboutourvibrantcommunityandlookforwardtoOpenHands’scontinuedevolution.
10

PublishedasaconferencepaperatICLR2025
REFERENCES
MichaelAhn,AnthonyBrohan,NoahBrown,YevgenChebotar,OmarCortes,ByronDavid,Chelsea
Finn,ChuyuanFu,KeerthanaGopalakrishnan,KarolHausman,etal. Doasican,notasisay:
Groundinglanguageinroboticaffordances. arXivpreprintarXiv:2204.01691,2022. 1
DaniilABoiko,RobertMacKnight,BenKline,andGabeGomes. Autonomouschemicalresearch
| withlargelanguagemodels. |     | Nature,624(7992):570–578,2023. |     |     | 1   |     |     |
| ------------------------ | --- | ------------------------------ | --- | --- | --- | --- | --- |
YupengChang,XuWang,JindongWang,YuanWu,LinyiYang,KaijieZhu,HaoChen,Xiaoyuan
Yi,CunxiangWang,YidongWang,etal. Asurveyonevaluationoflargelanguagemodels. ACM
| TransactionsonIntelligentSystemsandTechnology,15(3):1–45,2024. |     |     |     |     |     | 1   |     |
| -------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
HarrisonChase. LangChain,October2022. URLhttps://github.com/langchain-ai/langchain. 4,6,18
GuangyaoChen,SiweiDong,YuShu,GeZhang,JawardSesay,BörjeF.Karlsson,JieFu,andYemin
| Shi. Autoagents: | Aframeworkforautomaticagentgeneration,2024. |     |     |     |     | 1,6,18 |     |
| ---------------- | ------------------------------------------- | --- | --- | --- | --- | ------ | --- |
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared
Kaplan,HarriEdwards, YuriBurda, NicholasJoseph, GregBrockman, etal. Evaluatinglarge
| languagemodelstrainedoncode. |     | arXivpreprintarXiv:2107.03374,2021. |     |     |     |     | 7   |
| ---------------------------- | --- | ----------------------------------- | --- | --- | --- | --- | --- |
Cognition.ai. Introducingdevin,thefirstaisoftwareengineer. URLhttps://www.cognition.ai/blog/
| introducing-devin.          | 2   |                                         |     |     |     |     |     |
| --------------------------- | --- | --------------------------------------- | --- | --- | --- | --- | --- |
| CrewAI. CrewAI,October2024. |     | URLhttps://github.com/crewAIInc/crewAI. |     |     |     |     | 18  |
Jiaxi Cui, Zongjian Li, Yang Yan, Bohua Chen, and Li Yuan. Chatlaw: Open-source legal large
| languagemodelwithintegratedexternalknowledgebases,2023. |     |     |     |     |     | 18  |     |
| ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
AlexandreDrouin, MaximeGasse, MassimoCaccia, IssamH.Laradji, ManuelDelVerme, Tom
Marty,LéoBoisvert,MeghThakkar,QuentinCappart,DavidVazquez,NicolasChapados,and
AlexandreLacoste. Workarena: Howcapablearewebagentsatsolvingcommonknowledgework
| tasks?,2024. | 3,4 |     |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | --- |
PaulGauthier. Howaiderscoredsota26.3%onswebenchlite|aider. https://aider.chat/2024/05/22/
| swe-bench-lite.html. | Accessed: | 2024-06-05. | 5,7,8 |     |     |     |     |
| -------------------- | --------- | ----------- | ----- | --- | --- | --- | --- |
Significant Gravitas. Auto-gpt: An autonomous gpt-4 experiment, 2023. URL https://github.
| com/Significant-Gravitas/Auto-GPT,2023. |     |     | 6,7,10,18 |     |     |     |     |
| --------------------------------------- | --- | --- | --------- | --- | --- | --- | --- |
SiruiHong,MingchenZhuge,JonathanChen,XiawuZheng,YuhengCheng,JinlinWang,Ceyao
Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, et al. Metagpt: Meta programming for
a multi-agent collaborative framework. In The Twelfth International Conference on Learning
| Representations,2023. | 1,6,18 |     |     |     |     |     |     |
| --------------------- | ------ | --- | --- | --- | --- | --- | --- |
DongHuang,QingwenBu,JieM.Zhang,MichaelLuck,andHemingCui. Agentcoder: Multi-agent-
| basedcodegenerationwithiterativetestingandoptimisation,2024. |     |     |     |     |     | 19  |     |
| ------------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
PeterCHumphreys,DavidRaposo,TobiasPohlen,GregoryThornton,RachitaChhaparia,Alistair
Muldal,JoshAbramson,PetkoGeorgiev,AdamSantoro,andTimothyLillicrap. Adata-driven
approachforlearningtocontrolcomputers. InInternationalConferenceonMachineLearning,pp.
| 9466–9482.PMLR,2022.                           |     | 9   |     |                         |     |     |     |
| ---------------------------------------------- | --- | --- | --- | ----------------------- | --- | --- | --- |
| IPython. JupyterandthefutureofIPython—IPython. |     |     |     | URLhttps://ipython.org. |     |     | 4   |
Albert Q Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris
Bamford,DevendraSinghChaplot,DiegodelasCasas,EmmaBouHanna,FlorianBressand,etal.
| Mixtralofexperts. | arXivpreprintarXiv:2401.04088,2024. |     |     |     | 1   |     |     |
| ----------------- | ----------------------------------- | --- | --- | --- | --- | --- | --- |
CarlosEJimenez,JohnYang,AlexanderWettig,ShunyuYao,KexinPei,OfirPress,andKarthikR
Narasimhan. SWE-bench: CanLanguageModelsResolveReal-worldGithubIssues? InThe
TwelfthInternationalConferenceonLearningRepresentations,2024. URLhttps://openreview.net/
| forum?id=VTF8yNQM66. |     | 1,6,7,8,17,19 |     |     |     |     |     |
| -------------------- | --- | ------------- | --- | --- | --- | --- | --- |
11

PublishedasaconferencepaperatICLR2025
OmarKhattab,ArnavSinghvi,ParidhiMaheshwari,ZhiyuanZhang,KeshavSanthanam,SriVard-
hamanan, Saiful Haq, Ashutosh Sharma, Thomas T. Joshi, Hanna Moazam, Heather Miller,
MateiZaharia,andChristopherPotts. Dspy: Compilingdeclarativelanguagemodelcallsinto
self-improvingpipelines. 2024. 18
GeunwooKim, PierreBaldi, andStephenMcAleer. Languagemodelscansolvecomputertasks.
AdvancesinNeuralInformationProcessingSystems,36,2024. 9
HanyuLai,XiaoLiu,IatLongIong,ShuntianYao,YuxuanChen,PengboShen,HaoYu,Hanchen
Zhang,XiaohanZhang,YuxiaoDong,etal.Autowebglm:Bootstrapandreinforcealargelanguage
model-basedwebnavigatingagent. arXivpreprintarXiv:2404.03648,2024. 7,9
HaretonK.N.LeungandLeeJ.White. Astudyofintegrationtestingandsoftwareregressionat
theintegrationlevel. InProceedingsoftheConferenceonSoftwareMaintenance,ICSM1990,
SanDiego,CA,USA,26-29November,1990,pp.290–301.IEEE,1990. doi: 10.1109/ICSM.1990.
131377. URLhttps://doi.org/10.1109/ICSM.1990.131377. 19
GuohaoLi,HasanAbedAlKaderHammoud,HaniItani,DmitriiKhizbullin,andBernardGhanem.
Camel:Communicativeagentsfor"mind"explorationoflargescalelanguagemodelsociety. arXiv
preprintarXiv:2303.17760,2023a. 18
Jinyang Li, Binyuan Hui, GE QU, Jiaxi Yang, Binhua Li, Bowen Li, Bailin Wang, Bowen Qin,
RuiyingGeng, NanHuo, Xuanhe Zhou, ChenhaoMa, GuoliangLi, KevinChang, FeiHuang,
ReynoldCheng,andYongbinLi. CanLLMalreadyserveasadatabaseinterface? aBIgbenchfor
large-scaledatabasegroundedtext-to-SQLs. InThirty-seventhConferenceonNeuralInformation
ProcessingSystemsDatasetsandBenchmarksTrack,2023b. 6,8,9,17
RaymondLi,LoubnaBenAllal,YangtianZi,NiklasMuennighoff,DenisKocetkov,ChenghaoMou,
MarcMarone,ChristopherAkiki,JiaLi,JennyChim,QianLiu,EvgeniiZheltonozhskii,TerryYue
Zhuo, Thomas Wang, Olivier Dehaene, Mishig Davaadorj, Joel Lamy-Poirier, João Monteiro,
OlehShliazhko,NicolasGontier,NicholasMeade,ArmelZebaze,Ming-HoYee,LogeshKumar
Umapathi,JianZhu,BenjaminLipkin,MuhtashamOblokulov,ZhiruoWang,RudraMurthy,Jason
Stillerman,SivaSankalpPatel,DmitryAbulkhanov,MarcoZocca,MananDey,ZhihanZhang,
NourFahmy,UrvashiBhattacharyya,WenhaoYu,SwayamSingh,SashaLuccioni,PauloVillegas,
MaximKunakov,FedorZhdanov,ManuelRomero,TonyLee,NadavTimor,JenniferDing,Claire
Schlesinger,HaileySchoelkopf,JanEbert,TriDao,MayankMishra,AlexGu,JenniferRobinson,
Carolyn Jane Anderson, Brendan Dolan-Gavitt, Danish Contractor, Siva Reddy, Daniel Fried,
DzmitryBahdanau,YacineJernite,CarlosMuñozFerrandis,SeanHughes,ThomasWolf,Arjun
Guha,LeandrovonWerra,andHarmdeVries. Starcoder: maythesourcebewithyou!,2023c.
URLhttps://arxiv.org/abs/2305.06161. 7
TaoLi,GangLi,ZhiweiDeng,BryanWang,andYangLi. Azero-shotlanguageagentforcomputer
controlwithstructuredreflection. arXivpreprintarXiv:2310.08740,2023d. 9
EvanZheranLiu, KelvinGuu, PanupongPasupat, TianlinShi, andPercyLiang. Reinforcement
learningonwebinterfacesusingworkflow-guidedexploration. InInternationalConferenceon
LearningRepresentations(ICLR),2018. URLhttps://arxiv.org/abs/1802.08802. 6,9,17
XiaoLiu, HaoYu, HanchenZhang, YifanXu, XuanyuLei, HanyuLai, YuGu, HangliangDing,
KaiwenMen,KejuanYang,ShudanZhang,XiangDeng,AohanZeng,ZhengxiaoDu,Chenhui
Zhang,ShengShen,TianjunZhang,YuSu,HuanSun,MinlieHuang,YuxiaoDong,andJieTang.
Agentbench: Evaluatingllmsasagents. arXivpreprintarXiv: 2308.03688,2023. 6,10,17
AntonLozhkov,RaymondLi,LoubnaBenAllal,FedericoCassano,JoelLamy-Poirier,Nouamane
Tazi,AoTang,DmytroPykhtar,JiaweiLiu,YuxiangWei,TianyangLiu,MaxTian,DenisKocetkov,
Arthur Zucker, Younes Belkada, Zijian Wang, Qian Liu, Dmitry Abulkhanov, Indraneil Paul,
ZhuangLi,Wen-DingLi,MeganRisdal,JiaLi,JianZhu,TerryYueZhuo,EvgeniiZheltonozhskii,
Nii Osae Osae Dade, Wenhao Yu, Lucas Krauß, Naman Jain, Yixuan Su, Xuanli He, Manan
Dey, EdoardoAbati, YekunChai, NiklasMuennighoff, XiangruTang, MuhtashamOblokulov,
ChristopherAkiki,MarcMarone,ChenghaoMou,MayankMishra,AlexGu,BinyuanHui,Tri
Dao,ArmelZebaze,OlivierDehaene,NicolasPatry,CanwenXu,JulianMcAuley,HanHu,Torsten
Scholak,SebastienPaquet,JenniferRobinson,CarolynJaneAnderson,NicolasChapados,Mostofa
12

PublishedasaconferencepaperatICLR2025
Patwary,NimaTajbakhsh,YacineJernite,CarlosMuñozFerrandis,LingmingZhang,SeanHughes,
ThomasWolf,ArjunGuha,LeandrovonWerra,andHarmdeVries. Starcoder2andthestackv2:
Thenextgeneration,2024. URLhttps://arxiv.org/abs/2402.19173. 7
Grégoire Mialon, Clémentine Fourrier, Craig Swift, Thomas Wolf, Yann LeCun, and Thomas
Scialom. GAIA: a benchmark for general AI assistants. CoRR, abs/2311.12983, 2023. doi:
10.48550/ARXIV.2311.12983. URLhttps://doi.org/10.48550/arXiv.2311.12983. 6,9,10,17
Mozilla. Accessibilitytree-MDNWebDocsGlossary: DefinitionsofWeb-relatedterms|MDN.
URLhttps://developer.mozilla.org/en-US/docs/Glossary/Accessibility_tree. 5
NiklasMuennighoff,QianLiu,ArmelZebaze,QinkaiZheng,BinyuanHui,TerryYueZhuo,Swayam
Singh,XiangruTang,LeandrovonWerra,andShayneLongpre. Octopack: Instructiontuningcode
largelanguagemodels,2024. 6,7,8,17
YNakajima. Babyagi. URLhttps://github.com/yoheinakajima/babyagi,2023. 18
OpenAI. Chatgpt: May2024version. https://www.openai.com/chatgpt,2024a. Accessed: 2024-05-
29. 8,18
OpenAI. Hellogpt-4o. https://openai.com/index/hello-gpt-4o/,2024b. Accessed: 2024-05-15. 1
OpenAI,JoshAchiam,StevenAdler,SandhiniAgarwal,LamaAhmad,IlgeAkkaya,FlorenciaLeoni
Aleman,DiogoAlmeida,JankoAltenschmidt,SamAltman,ShyamalAnadkat,RedAvila,Igor
Babuschkin,SuchirBalaji,ValerieBalcom,PaulBaltescu,HaimingBao,MohammadBavarian,
JeffBelgum,IrwanBello,JakeBerdine,GabrielBernadett-Shapiro,ChristopherBerner,Lenny
Bogdonoff,OlegBoiko,MadelaineBoyd,Anna-LuisaBrakman,GregBrockman,TimBrooks,
MilesBrundage,KevinButton,TrevorCai,RosieCampbell,AndrewCann,BrittanyCarey,Chelsea
Carlson,RoryCarmichael,BrookeChan,CheChang,FotisChantzis,DerekChen,SullyChen,
RubyChen,JasonChen,MarkChen,BenChess,ChesterCho,CaseyChu,HyungWonChung,
DaveCummings,JeremiahCurrier,YunxingDai,CoryDecareaux,ThomasDegry,NoahDeutsch,
DamienDeville,ArkaDhar,DavidDohan,SteveDowling,SheilaDunning,AdrienEcoffet,Atty
Eleti,TynaEloundou,DavidFarhi,LiamFedus,NikoFelix,SimónPosadaFishman,JustonForte,
IsabellaFulford,LeoGao,ElieGeorges,ChristianGibson,VikGoel,TarunGogineni,Gabriel
Goh,RaphaGontijo-Lopes,JonathanGordon,MorganGrafstein,ScottGray,RyanGreene,Joshua
Gross,ShixiangShaneGu,YufeiGuo,ChrisHallacy,JesseHan,JeffHarris,YuchenHe,Mike
Heaton,JohannesHeidecke,ChrisHesse,AlanHickey,WadeHickey,PeterHoeschele,Brandon
Houghton,KennyHsu,ShengliHu,XinHu,JoostHuizinga,ShantanuJain,ShawnJain,Joanne
Jang,AngelaJiang,RogerJiang,HaozhunJin,DennyJin,ShinoJomoto,BillieJonn,Heewoo
Jun, Tomer Kaftan, Łukasz Kaiser, Ali Kamali, Ingmar Kanitscheider, Nitish Shirish Keskar,
Tabarak Khan, Logan Kilpatrick, Jong Wook Kim, Christina Kim, Yongjik Kim, Jan Hendrik
Kirchner,JamieKiros,MattKnight,DanielKokotajlo,ŁukaszKondraciuk,AndrewKondrich,
ArisKonstantinidis,KyleKosic,GretchenKrueger,VishalKuo,MichaelLampe,IkaiLan,Teddy
Lee, Jan Leike, Jade Leung, Daniel Levy, Chak Ming Li, Rachel Lim, Molly Lin, Stephanie
Lin,MateuszLitwin,TheresaLopez,RyanLowe,PatriciaLue,AnnaMakanju,KimMalfacini,
SamManning,TodorMarkov,YanivMarkovski,BiancaMartin,KatieMayer,AndrewMayne,
BobMcGrew,ScottMayerMcKinney,ChristineMcLeavey,PaulMcMillan,JakeMcNeil,David
Medina,AalokMehta,JacobMenick,LukeMetz,AndreyMishchenko,PamelaMishkin,Vinnie
Monaco, Evan Morikawa, Daniel Mossing, Tong Mu, Mira Murati, Oleg Murk, David Mély,
AshvinNair,ReiichiroNakano,RajeevNayak,ArvindNeelakantan,RichardNgo,Hyeonwoo
Noh,LongOuyang,CullenO’Keefe,JakubPachocki,AlexPaino,JoePalermo,AshleyPantuliano,
GiambattistaParascandolo,JoelParish,EmyParparita,AlexPassos,MikhailPavlov,AndrewPeng,
AdamPerelman,FilipedeAvilaBelbutePeres,MichaelPetrov,HenriquePondedeOliveiraPinto,
Michael,Pokorny,MichellePokrass,VitchyrH.Pong,TollyPowell,AletheaPower,BorisPower,
ElizabethProehl,RaulPuri,AlecRadford,JackRae,AdityaRamesh,CameronRaymond,Francis
Real,KendraRimbach,CarlRoss,BobRotsted,HenriRoussez,NickRyder,MarioSaltarelli,Ted
Sanders,ShibaniSanturkar,GirishSastry,HeatherSchmidt,DavidSchnurr,JohnSchulman,Daniel
Selsam,KylaSheppard,TokiSherbakov,JessicaShieh,SarahShoker,PranavShyam,Szymon
Sidor,EricSigler,MaddieSimens,JordanSitkin,KatarinaSlama,IanSohl,BenjaminSokolowsky,
YangSong,NatalieStaudacher,FelipePetroskiSuch,NatalieSummers,IlyaSutskever,JieTang,
NikolasTezak,MadeleineB.Thompson,PhilTillet,AminTootoonchian,ElizabethTseng,Preston
13

PublishedasaconferencepaperatICLR2025
Tuggle,NickTurley,JerryTworek,JuanFelipeCerónUribe,AndreaVallone,ArunVijayvergiya,
ChelseaVoss,CarrollWainwright,JustinJayWang,AlvinWang,BenWang,JonathanWard,Jason
Wei,CJWeinmann,AkilaWelihinda,PeterWelinder,JiayiWeng,LilianWeng,MattWiethoff,
DaveWillner,ClemensWinter,SamuelWolrich,HannahWong,LaurenWorkman,SherwinWu,
JeffWu,MichaelWu,KaiXiao,TaoXu,SarahYoo,KevinYu,QimingYuan,WojciechZaremba,
RowanZellers,ChongZhang,MarvinZhang,ShengjiaZhao,TianhaoZheng,JuntangZhuang,
| WilliamZhuk,andBarretZoph. |     | Gpt-4technicalreport,2024. | 18  |     |
| -------------------------- | --- | -------------------------- | --- | --- |
JiayiPan,YichiZhang,NicholasTomlin,YifeiZhou,SergeyLevine,andAlaneSuhr. Autonomous
evaluationandrefinementofdigitalagents. arXivpreprintarXiv:2404.06474,2024. 7,9,18
Liangming Pan, Alon Albalak, Xinyi Wang, and William Yang Wang. Logic-lm: Empowering
large language models with symbolic solvers for faithful logical reasoning. arXiv preprint
| arXiv:2305.12295,2023. |     | 10  |     |     |
| ---------------------- | --- | --- | --- | --- |
Joon Sung Park, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and
MichaelS.Bernstein. Generativeagents: Interactivesimulacraofhumanbehavior,2023. 18
AjayPatel,MarkusHofmarcher,ClaudiuLeoveanu-Condrei,Marius-ConstantinDinu,ChrisCallison-
Burch,andSeppHochreiter. Largelanguagemodelscanself-improveatwebagenttasks. arXiv
| preprintarXiv:2405.20309,2024. |     | 7,9 |     |     |
| ------------------------------ | --- | --- | --- | --- |
ShishirG.Patil,TianjunZhang,XinWang,andJosephE.Gonzalez. Gorilla: Largelanguagemodel
| connectedwithmassiveapis. |     | arXivpreprintarXiv:2305.15334,2023. |     | 6,8,17 |
| ------------------------- | --- | ----------------------------------- | --- | ------ |
Playwright. Fast and reliable end-to-end testing for modern web apps | Playwright. URL https:
| //playwright.dev/. | 4   |     |     |     |
| ------------------ | --- | --- | --- | --- |
Chen Qian, Xin Cong, Wei Liu, Cheng Yang, Weize Chen, Yusheng Su, Yufan Dang, Jiahao Li,
Juyuan Xu, Dahai Li, Zhiyuan Liu, and Maosong Sun. Communicative agents for software
| development,2023. | 18,19 |     |     |     |
| ----------------- | ----- | --- | --- | --- |
Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong,
Xiangru Tang, Bill Qian, Sihan Zhao, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein,
DahaiLi,ZhiyuanLiu,andMaosongSun. Toolllm: Facilitatinglargelanguagemodelstomaster
16000+real-worldapis. CoRR,abs/2307.16789,2023. doi: 10.48550/ARXIV.2307.16789. URL
| https://doi.org/10.48550/arXiv.2307.16789. |     | 4   |     |     |
| ------------------------------------------ | --- | --- | --- | --- |
David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien
Dirani,JulianMichael,andSamuelRBowman. GPQA:AGraduate-LevelGoogle-ProofQ&A
| Benchmark. | arXivpreprintarXiv:2311.12022,2023. |     | 6,7,9,10,17,23 |     |
| ---------- | ----------------------------------- | --- | -------------- | --- |
AmanSanger. Near-instantfull-fileedits. https://www.cursor.com/blog/instant-apply. Accessed:
| 2024-06-05. | 5   |     |     |     |
| ----------- | --- | --- | --- | --- |
ServiceNow. BrowserGym: aGymEnvironmentforWebTaskAutomation. URLhttps://github.com/
| ServiceNow/BrowserGym. |     | 2,4,18 |     |     |
| ---------------------- | --- | ------ | --- | --- |
PeterShaw,MandarJoshi,JamesCohan,JonathanBerant,PanupongPasupat,HexiangHu,Urvashi
Khandelwal,KentonLee,andKristinaNToutanova. Frompixelstouiactions: Learningtofollow
instructionsviagraphicaluserinterfaces. AdvancesinNeuralInformationProcessingSystems,36:
| 34354–34370,2023. | 9   |     |     |     |
| ----------------- | --- | --- | --- | --- |
NoahShinn,FedericoCassano,AshwinGopinath,KarthikNarasimhan,andShunyuYao. Reflexion:
AdvancesinNeuralInformationProcessing
Languageagentswithverbalreinforcementlearning.
| Systems,36,2024. | 18  |     |     |     |
| ---------------- | --- | --- | --- | --- |
Oyvind Tafjord, Bhavana Dalvi, and Peter Clark. ProofWriter: Generating implications, proofs,
and abductive statements over natural language. In Chengqing Zong, Fei Xia, Wenjie Li, and
RobertoNavigli(eds.),FindingsoftheAssociationforComputationalLinguistics: ACL-IJCNLP
2021, pp. 3621–3634, Online, August 2021. Association for Computational Linguistics. doi:
10.18653/v1/2021.findings-acl.317. URLhttps://aclanthology.org/2021.findings-acl.317. 6,10,17
14

PublishedasaconferencepaperatICLR2025
XiangruTang,QiaoJin,KunlunZhu,TongxinYuan,YichiZhang,WangchunshuZhou,MengQu,
YilunZhao,JianTang,ZhuoshengZhang,etal. Prioritizingsafeguardingoverautonomy: Risksof
| llmagentsforscience. |     | arXivpreprintarXiv:2402.04247,2024a. |     |     | 1   |     |
| -------------------- | --- | ------------------------------------ | --- | --- | --- | --- |
XiangruTang,YuliangLiu,ZefanCai,YanjunShao,JunjieLu,YichiZhang,ZexuanDeng,Helan
Hu,KaikaiAn,RuijunHuang,ShuzhengSi,ShengChen,HaozheZhao,LiangChen,YanWang,
TianyuLiu,ZhiweiJiang,BaobaoChang,YinFang,YujiaQin,WangchunshuZhou,YilunZhao,
ArmanCohan,andMarkGerstein. ML-Bench: Evaluatinglargelanguagemodelsandagentsfor
machinelearningtasksonrepository-levelcode,2024b. URLhttps://arxiv.org/abs/2311.09835. 6,
8,17
XiangruTang,BillQian,RickGao,JiakangChen,XinyunChen,andMarkBGerstein. BioCoder: a
benchmarkforbioinformaticscodegenerationwithlargelanguagemodels. Bioinformatics,40
| (Supplement_1):i266–i276,062024c. |     |     | ISSN1367-4811. |     | 6,8,17 |     |
| --------------------------------- | --- | --- | -------------- | --- | ------ | --- |
XiangruTang,AnniZou,ZhuoshengZhang,ZimingLi,YilunZhao,XingyaoZhang,ArmanCohan,
andMarkGerstein. Medagents: Largelanguagemodelsascollaboratorsforzero-shotmedical
| reasoning,2024d. |     | 18  |     |     |     |     |
| ---------------- | --- | --- | --- | --- | --- | --- |
GeminiTeam,RohanAnil,SebastianBorgeaud,YonghuiWu,Jean-BaptisteAlayrac,JiahuiYu,Radu
Soricut,JohanSchalkwyk,AndrewMDai,AnjaHauth,etal. Gemini: afamilyofhighlycapable
| multimodalmodels. |         | arXivpreprintarXiv:2312.11805,2023.          |     |     | 1   |      |
| ----------------- | ------- | -------------------------------------------- | --- | --- | --- | ---- |
| XAgentTeam.       | Xagent: | Anautonomousagentforcomplextasksolving,2023. |     |     |     | 6,18 |
HugoTouvron,ThibautLavril,GautierIzacard,XavierMartinet,Marie-AnneLachaux,Timothée
Lacroix,BaptisteRozière,NamanGoyal,EricHambro,FaisalAzhar,AurelienRodriguez,Armand
Joulin,EdouardGrave,andGuillaumeLample. Llama: Openandefficientfoundationlanguage
| models. | arXivpreprintarXiv:2302.13971,2023. |     |     | 8   |     |     |
| ------- | ----------------------------------- | --- | --- | --- | --- | --- |
Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li, Hao Peng, and Heng Ji.
| ExecutableCodeActionsElicitBetterLLMAgents. |     |     |     | InICML,2024a. |     | 2,3,4,5,17 |
| ------------------------------------------- | --- | --- | --- | ------------- | --- | ---------- |
XingyaoWang,ZihanWang,JiatengLiu,YangyiChen,LifanYuan,HaoPeng,andHengJi. MINT:
EvaluatingLLMsinMulti-turnInteractionwithToolsandLanguageFeedback. InICLR,2024b. 6,
10,17
Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Shaokun Zhang, Erkang Zhu, Beibin Li,
Li Jiang, Xiaoyun Zhang, and Chi Wang. Autogen: Enabling next-gen llm applications via
multi-agentconversationframework. arXivpreprintarXiv:2308.08155,2023. 1,6,18
ChunqiuStevenXia, YinlinDeng, SorenDunn, andLingmingZhang. Agentless: Demystifying
| llm-basedsoftwareengineeringagents. |     |     | arXivpreprint,2024. |     | 7   |     |
| ----------------------------------- | --- | --- | ------------------- | --- | --- | --- |
TianbaoXie,FanZhou,ZhoujunCheng,PengShi,LuoxuanWeng,YitaoLiu,TohJingHua,Junning
Zhao,QianLiu,CheLiu,etal. Openagents: Anopenplatformforlanguageagentsinthewild.
| arXivpreprintarXiv:2310.10634,2023. |     |     | 6   |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | --- | --- |
YihengXu,HongjinSu,ChenXing,BoyuMi,QianLiu,WeijiaShi,BinyuanHui,FanZhou,Yitao
Liu,TianbaoXie,etal. Lemur:Harmonizingnaturallanguageandcodeforlanguageagents. arXiv
| preprintarXiv:2310.06830,2023. |     |     | 7,9 |     |     |     |
| ------------------------------ | --- | --- | --- | --- | --- | --- |
JohnYang,CarlosE.Jimenez,AlexanderWettig,KilianLieret,ShunyuYao,KarthikNarasimhan,
andOfirPress. Swe-agent: Agent-computerinterfacesenableautomatedsoftwareengineering,
2024. 2,5,6,7,8,19
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan
Cao. React: Synergizingreasoningandactinginlanguagemodels. InTheEleventhInternational
Conference on Learning Representations, 2023. URL https://openreview.net/forum?id=WE_
| vluYUL-X. | 8   |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- |
YiningYe,XinCong,ShizuoTian,JiannanCao,HaoWang,YujiaQin,YaxiLu,HeyangYu,Huadong
Wang,YankaiLin,etal. Proagent: Fromroboticprocessautomationtoagenticprocessautomation.
| arXivpreprintarXiv:2311.10751,2023. |     |     | 18  |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | --- | --- |
15

PublishedasaconferencepaperatICLR2025
LifanYuan,YangyiChen,XingyaoWang,YiR.Fung,HaoPeng,andHengJi. CRAFT:customizing
llms by creating and retrieving from specialized toolsets. CoRR, abs/2309.17428, 2023. doi:
10.48550/ARXIV.2309.17428. URLhttps://doi.org/10.48550/arXiv.2309.17428. 4
LifanYuan,GanquCui,HanbinWang,NingDing,XingyaoWang,JiaDeng,BojiShan,HuiminChen,
RuobingXie,YankaiLin,ZhenghaoLiu,BowenZhou,HaoPeng,ZhiyuanLiu,andMaosongSun.
Advancingllmreasoninggeneralistswithpreferencetrees,2024. 10
YizheZhang,JiaruiLu,andNavdeepJaitly. Probingthemulti-turnplanningcapabilitiesofllmsvia
20questiongames. 2024a. 6,10,17
YuntongZhang,HaifengRuan,ZhiyuFan,andAbhikRoychoudhury. Autocoderover: Autonomous
programimprovement,2024b. 6,7,8,19
Shuyan Zhou, Frank F Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng,
TianyueOu,YonatanBisk,DanielFried,etal. Webarena: Arealisticwebenvironmentforbuilding
autonomousagents. InTheTwelfthInternationalConferenceonLearningRepresentations,2023a.
1,6,7,9,17
WangchunshuZhou,YuchenEleanorJiang,LongLi,JialongWu,TiannanWang,ShiQiu,Jintian
Zhang, Jing Chen, Ruipu Wu, Shuai Wang, Shiding Zhu, Jiyu Chen, Wentao Zhang, Xiangru
Tang,NingyuZhang,HuajunChen,PengCui,andMrinmayaSachan. Agents: Anopen-source
frameworkforautonomouslanguageagents,2023b. 6,18
YuchenZhuang, YueYu, KuanWang, HaotianSun, andChaoZhang. Toolqa: Adatasetforllm
questionansweringwithexternaltools. AdvancesinNeuralInformationProcessingSystems,36,
2024. 6,8,17
MingchenZhuge,HaozheLiu,FrancescoFaccio,DylanRAshley,RóbertCsordás,AnandGopalakr-
ishnan,AbdullahHamdi,HasanAbedAlKaderHammoud,VincentHerrmann,KazukiIrie,etal.
Mindstormsinnaturallanguage-basedsocietiesofmind. arXivpreprintarXiv:2305.17066,2023.
18
MingchenZhuge, WenyiWang, LouisKirsch, FrancescoFaccio, DmitriiKhizbullin, andJurgen
Schmidhuber. Languageagentsasoptimizablegraphs. arXivpreprintarXiv:2402.16823,2024. 6,
17,18
AlbertÖrwall. Moatlesstools. URLhttps://github.com/aorwall/moatless-tools. 7
16

PublishedasaconferencepaperatICLR2025
AUTHOR CONTRIBUTIONS
This work was an open-source collaborative effort across multiple institutions. We employed a
point-basedsystemtodeterminecontributionsandawardauthorships,withtechnicalcontributions
trackedandmeasuredinunitsofpullrequests(PRs)3. XingyaoWangledtheproject,coordinating
overalldevelopmentandpaperwritingefforts. Detailedcontributionswereasfollows:
• Agent Development (§3): Xingyao Wang led the implementation of CodeAct Wang et al.
(2024a)andCodeActSWEagents. FrankF.Xuledthedevelopmentofwebbrowsingagents
Zhouetal.(2023a).MingchenZhugeorchestratedtheintegrationoftheGPTSwarmagentZhuge
etal.(2024). RobertBrennanandBoxuanLileadthedevelopmentoftheMicroAgent.
• ArchitecturalDevelopment(Fig.2): RobertBrennaninitiatedthearchitecturedesign. Boxuan
Li,FrankF.Xu,XingyaoWang,YufanSong,andMingzhangZhengfurtherrefinedandexpanded
thearchitecture. BoxuanLiimplementedtheinitialversionofintegrationtests(§E),maintained
theagentskillslibrary(§2.3),managedconfigurations,andresolvedresourceleaksinevaluation.
FrankF.Xudevelopedthewebbrowsingenvironment(§J)forbothagentexecutionandevalua-
tionandintegrateditwithbothagentandfront-enduserinterfaces. XingyaoWangauthoredthe
initialcodefortheagentskillslibraryandtheDockersandbox. YufanSongimplementedcost
trackingforevaluation,whileMingzhangZhengdevelopedanimage-agnosticdockersandbox
formorestableSWE-Benchevaluation.
• Benchmarking,Integration,andCodeReview: BoxuanLiandYufanSongledbenchmark
integrationefforts,includingcoordination,evaluation,andcodereview. YufanSongalsohelped
trackPRcontributions. GrahamNeubig,XingyaoWang,MingzhangZheng,RobertBrennan,
HoangH.Tran,FrankF.Xu,XiangruTang,FuqiangLi,andYanjunShaoprovidedadditional
| supportinintegrationandcodereviews. |     | Specificbenchmarkcontributionsincluded: |
| ----------------------------------- | --- | --------------------------------------- |
| – SWE-BenchJimenezetal.(2024):      |     | BowenLiandXingyaoWang                   |
– WebArenaZhouetal.(2023a)andMiniWob++Liuetal.(2018): FrankF.Xu
– GAIA Mialon et al. (2023): Jiayi Pan (integration) and Mingchen Zhuge (GPTSwarm
evaluation)
– API-BenchPatiletal.(2023)andToolQAZhuangetal.(2024): YueqiSong
– HumanEvalFixMuennighoffetal.(2024): NiklasMuennighoffandXiangruTang
| – ProofWriterTafjordetal.(2021): |            | RenMa                    |
| -------------------------------- | ---------- | ------------------------ |
| – MINTWangetal.(2024b):          |            | HoangH.Tran              |
| – AgentBenchLiuetal.(2023):      |            | FuqiangLi                |
| – BIRDLietal.(2023b):            | BinyuanHui |                          |
| – GPQAReinetal.(2023):           |            | JaskiratSingh            |
| – BioCoderTangetal.(2024c):      |            | XiangruTangandBillQian   |
| – ML-BenchTangetal.(2024b):      |            | XiangruTangandYanjunShao |
– Entity-Deduction-ArenaZhangetal.(2024a): YizheZhang
• Advising: GrahamNeubigadvisedtheproject,providingguidance,resources,andsubstantial
paperedits. HengJiandHaoPengofferedadditionalprojectadviceandassistedwithpaper
writing. JunyangLincontributedadvisorysupportandsponsoredresources.
| A LIMITATIONS | AND FUTURE | WORK |
| ------------- | ---------- | ---- |
WeareexcitedaboutthefoundationsourvibrantcommunityhaslaidinOpenHandsandlookforward
| toitscontinuedevolution. | Weidentifyseveraldirectionsforfuturework: |     |
| ------------------------ | ----------------------------------------- | --- |
Enhancedmulti-modalitysupport. Whileourcurrentimplementationalready supportsawide
rangeoffileformatsthroughpredefinedagentskills,weareinterestedinenablingmulti-modality
inaprincipledwaythroughstandardIPythonandbrowserintegration,suchasviewingimagesand
videosusingvision-languagemodelthroughabrowserorprocessingXLSXfileswithcode.
Strongeragents. Currentagentsstillstrugglewithcomplextasks,andweareinterestedinbuilding
betteragentsthroughbothtrainingandinferencetimetechniques.
3Formoredetails,pleaserefertohttps://github.com/All-Hands-AI/OpenHands/pull/1917.
17

PublishedasaconferencepaperatICLR2025
Agent editing improvements. Current agent suffers a lot when editing long files, and we are
interestedinexploringdifferentapproachestoimprovethefileeditingperformanceofagents.
Webbrowsingimprovements. DuetotheextensiblenatureofOpenHands,orthogonalcomponents
thatcouldimproveagentscanbeintegratedeasily. Forexample,thankstoOpenHands’sextensible
architecture, Auto Eval & Refine Pan et al. (2024), an agent retry-on-error strategy with Reflex-
ionShinnetal.(2024)promptsandtaskcompletionrewardmodels,willbeintegratedasanoptional
componentattachedtoourbrowsingagent.
Automaticworkflowgeneration. Currently,OpenHands’sworkflowstillrequiresasubstantialhand-
craftedworkload. Webelievethatgraph-basedframeworkssuchasGPTSwarmZhugeetal.(2024)
andLangGraphChase(2022)couldserveasalternativesolutionsforbuildingagents. Particularly
inGPTSwarm,whenagentsareconstructedusinggraphs,itbecomeseasiertoincorporatevarious
optimizationmethods(e.g.,reinforcementlearning,meta-prompting). OpenHandsconsidersthese
methodstolaythegroundworkforpromisingsolutionsinautomaticworkflowgenerationinfuture
versions.
B ETHICS STATEMENT
MostAIagentstodayarestillresearchartifactsandlacktheabilitytoperformcomplex,long-horizon
tasksintherealworldreliably. However,astheirperformancecontinuestoimproveandtheyare
increasinglydeployedinrealworld,theyhavethepotentialtoboostproductivitywhilealsoposing
securityriskstosocietysignificantly. OpenHandshelpsmitigaterisksby:
(1) Enablingsystematicevaluationoftheseagents,whichcanidentifyandaddressrisksbeforethey
arewidelydeployed.
(2) Facilitatinghuman-agentinteractionratherthanallowingagentstooperateautonomouslywithout
oversight.
(3) Moreimportantly,wehopeOpenHandsallowsresearchersworldwidetoaccessthebestsuitesof
agentstoconductfrontiersafetyresearchtowardsbuildingsafeandhelpfulagents.
C RELATED WORK
The breakthroughs in large language models (LLMs) like ChatGPT OpenAI (2024a) and GPT-
4OpenAIetal.(2024)havesignificantlyenhancedthecapabilitiesofautonomousagentsacross
variousdomainsYeetal.(2023);Tangetal.(2024d);Parketal.(2023);Cuietal.(2023). These
advanceshavespurredamultitudeofgeneralistagentproposalsGravitas(2023);Nakajima(2023);
Wuetal.(2023)aimedatperformingdiverseusertasksandhavegainedattentionfrombothdevelopers
andbroaderaudiences. NotableworkssuchasAuto-GPTGravitas(2023)harnessLLMsfortask
completion by decomposing user goals into executable steps. Multi-agent collaboration systems
leverageLLMsforelementslikerole-playingandtask-solvingcapabilitiesZhugeetal.(2023);Li
etal.(2023a);Zhouetal.(2023b);Team(2023),withMetaGPTHongetal.(2023)emphasizing
standardizedoperatingprocedures,andAutoGenWuetal.(2023)providingaconversationframework
forinteractivesystems. AGENTSZhouetal.(2023b)andAutoAgentsChenetal.(2024)offernew
paradigmsforcustomizableagentarchitecture,whileXAgentTeam(2023)andGPTSwarmZhuge
et al. (2024) introduce complex management systems and optimizable graphs, respectively, for
enhancedagentoperations.
This surge in agent development has led to specialized frameworks aimed at streamlining agent
implementation. LangChain and LangGraph Chase (2022) provide foundational building blocks
with basic runtime support, while CrewAI CrewAI (2024) focuses on orchestrating multi-agent
communications. BrowserGym ServiceNow specifically targets web browsing capabilities, and
DSPyKhattabetal.(2024)emphasizesend-to-endpromptoptimization. AutoGenWuetal.(2023)
advancesbeyondbasicframeworksbyimplementingPythonandbashexecutioncapabilities,though
withstatelesscommandexecution,whileframeworkslikeCrewAIoffersandboxedbutlimitedcode
interpreterfeatures.
Software development, a front-runner in applying LLM-based agents, has seen advancements in
frameworksforfacilitatingthedevelopmentprocessesHongetal.(2023);Qianetal.(2023). In-
18

PublishedasaconferencepaperatICLR2025
novationssuchasChatDevQianetal.(2023)automatethesoftwaredevelopmentlifecycleakinto
thewaterfallmodel, andAutoCodeRoverZhangetal.(2024b)addressesGitHubissuesviacode
searchandabstractsyntaxtreemanipulation. AgentCoderHuangetal.(2024)iterativelyrefines
codegenerationwithintegratedtestingandfeedback,whileSWE-AgentYangetal.(2024)integrates
LLMsforautomatedGithubissuefixing,streamliningsoftwareengineering.
D GRAPHICAL USER INTERFACE
Besidesrunningfromthecommandline,OpenHandsfeaturesarichgraphicaluserinterfacethat
visualizestheagent’scurrentactions(e.g.,browsingtheweb,executingbasecommandsorPython
code, etc.) and allows for real-time feedback from the user. Screenshots of the UI are shown in
Fig.1. Theusermayinterrupttheagentatanymomenttoprovideadditionalfeedback,comments,or
instructionwhiletheagentisworking. Thisuserinterfacedirectlyconnectswiththeeventstreams
(§2.1)tocontrolandvisualizetheagentsandruntime,makingitagentandruntimeagnostic.
E QUALITY CONTROL: INTEGRATION TESTS FOR AGENTS
Integration tests Leung & White (1990) have long been used by software developers to ensure
softwarequality. Unlikelargelanguagemodelswithsimpleinput-outputschema,agentsaretypically
complexpiecesofsoftwarewhereminorerrorscanbeeasilyintroducedduringthedevelopment
processandhurtfinaltaskperformance. Whilerunningafullsuiteevaluation(§4)istheultimate
measure of performance degradation, running them for every code changes can be prohibitively
slowandexpensive. 4. InOpenHands, wepioneeranend-to-endagenttestframeworkthattests
promptregression,actions,andsandboxenvironments. Itcombinesintegrationtestingfromsoftware
engineering and foundation model mocking for deterministic behavior to prevent the accidental
introductionofbugsduringagentdevelopment.
Defininganintegrationtest. TheintegrationtestframeworkforOpenHandsisstructuredtovalidate
end-to-end functionality by automating task execution and result verification. Developers define
tasksandexpectedresults;forinstance,ataskmightinvolvecorrectingtyposinadocumentnamed
"bad.txt". UpontaskexecutionthroughOpenHands,outputsarecomparedagainstapredefined"gold
file"toensureaccuracy.
MockingLLMfordeterministicbehavior. Addressingthechallengeofnon-determinisminlarge
language models (LLMs) and the associated high costs, the framework intercepts all LLM calls
andsuppliespredefinedresponsesbasedonexactpromptmatches. Thismethodnotonlyensures
consistencyintestoutcomesbutalsoreducesoperationalcostsbyminimizingtherelianceonreal
LLMs.
RegenerateLLMresponsesonbreakingchanges. Prompt-responsepairsaremanagedthrough
ascriptthatgeneratesandstoresthesepairswhennewtestsareintroducedorexistingpromptsare
modified. Forroutinetests, theframeworkattemptstoreuseexistingLLMresponsesbyslightly
adjustingtheprompts. Substantialchangesthataffecttaskhandlingrequireregenerationofthese
pairsusingrealLLMs.
Benefitsofintegrationtests. Theframeworkoffersseveraladvantages,including1)Promptregres-
siontesting: Storedprompt-responsepairsfacilitatechangetrackingandprovideareferencefornew
teammemberstounderstandLLMinteractions,2)Multi-platformsupport: Testsareautomatically
scheduledforeverypullrequestandcommitonthemainbranch,runningacrossmultipleplatforms,
environments,andagents,includingLinuxandMac,andinlocal,SSH,andexecsandboxes,and
3)Comprehensiveerrordetection: Itcaptureserrorsinpromptgeneration,messagepassing,and
sandboxexecution,therebymaintainingahightestcoverage.
4RunningaSWE-BenchLiteJimenezetal.(2024)evaluationwithgpt-4ocostsaround600USD.
19

PublishedasaconferencepaperatICLR2025
Figure4: OpenHandsruntimeworkflow.
F HOW OPENHANDS RUNTIME WORK
F.1 WORKFLOW
TheOpenHandsRuntimesystemusesaclient-serverarchitectureimplementedwithDockercontain-
ers. SeeFig.4foranoverviewofhowitworks.
(1) UserInput: TheuserprovidesacustombaseDockerimage.
(2) ImageBuilding:OpenHandsbuildsanewDockerimage(the"OHruntimeimage")basedonthe
user-providedimage. ThisnewimageincludesOpenHands-specificcode,primarilythe"runtime
client"(i.e.,runtimeAPIserverdescribedin§2.2).
(3) Container Launch: When OpenHands starts, it launches a Docker container using the OH
runtimeimage.
(4) Communication: TheOpenHandsbackend(runtime.py)communicateswiththeruntime
clientoverRESTfulAPI,sendingactionsandreceivingobservations
(5) ActionExecution: Theruntimeclientreceivesactionsfromthebackend,executestheminthe
sandboxedenvironment,andsendsbackobservations
(6) ObservationReturn: TheclientsendsexecutionresultsbacktotheOpenHandsbackendevent
streamasobservations.
Theroleoftheclient:
• ItactsasanintermediarybetweentheOpenHandsbackendandthesandboxedenvironment
• Itexecutesvarioustypesofactions(shellcommands, fileoperations, Pythoncode, etc.)
safelywithinthecontainer
• Itmanagesthestateofthesandboxedenvironment,includingthecurrentworkingdirectory
andloadedplugins
20

PublishedasaconferencepaperatICLR2025
• It formats and returns observations to the backend, ensuring a consistent interface for
processingresults
F.2 HOWOPENHANDSBUILDSANDMAINTAINSRUNTIMEIMAGES
OpenHands’ approach to building and managing runtime images ensures efficiency, consistency,
and flexibility in creating and maintaining Docker images for both production and development
environments.
F.2.1 IMAGETAGGINGSYSTEM
OpenHands uses a dual-tagging system for its runtime images to balance reproducibility with
flexibility:
(1) Hash-based tag: {target_image_repo}:{target_image_hash_tag}. Example:
runtime:abc123def456
– ThistagisbasedontheMD5hashoftheDockerbuildfolder,whichincludesthesource
code(ofruntimeclientandrelateddependencies)andDockerfile
– Identicalhashtagsguaranteethattheimageswerebuiltwithexactlythesamesourcecode
andDockerfile
– Thisensuresreproducibility;thesamehashalwaysmeansthesameimagecontents
(2) Generic tag: {target_image_repo}:{target_image_tag}. Example:
runtime:oh_v0.9.3_ubuntu_tag_22.04
– Thistagfollowstheformat:runtime:oh_v{VERSION}_{BASE_IMAGE}_tag_{IMAGE_TAG}
– ItrepresentsthelatestbuildforaparticularbaseimageandOpenHandsversioncombination
– Thistagisupdatedwheneveranewimageisbuiltfromthesamebaseimage,evenifthe
sourcecodechanges
The hash-based tag ensures reproducibility, while the generic tag provides a stable reference to
thelatestversionofaparticularconfiguration. Thisdual-taggingapproachallowsOpenHandsto
efficientlymanagebothdevelopmentandproductionenvironments.
F.2.2 BUILDPROCESS
(1) ImageNamingConvention:
– Hash-based tag: target_image_repo:target_image_hash_tag. Example:
runtime:abc123def456
– Generic tag: target_image_repo:target_image_tag. Example:
runtime:oh_v0.9.3_ubuntu_tag_22.04
(2) BuildProcess:
a. ConvertthebaseimagenametoanOHruntimeimagenameExample: ubuntu:22.04
->runtime:oh_v0.9.3_ubuntu_tag_22.04
b. Generateabuildcontext(DockerfileandOpenHandssourcecode)andcalculateitshash
c. Checkforanexistingimagewiththecalculatedhash
d. Ifnotfound,checkforarecentcompatibleimagetouseasabase
e. Ifnocompatibleimageexists,buildfromscratchusingtheoriginalbaseimage
f. Tagthenewimagewithbothhash-basedandgenerictags
(3) ImageReuse and RebuildingLogic: Thesystem follows thesesteps todetermine whether
to build a new image or use an existing one from a user-provided (base) image (e.g.,
ubuntu:22.04):
a. Ifanimageexistswiththesamehash(e.g.,runtime:abc123def456),itwillbereused
asis
b. Iftheexacthashisnotfound,thesystemwilltrytorebuildusingthelatestgenericimage
(e.g., runtime:oh_v0.9.3_ubuntu_tag_22.04) as a base. This saves time by
leveragingexistingdependencies
21

PublishedasaconferencepaperatICLR2025
Figure5: OpenHandsRuntimeImageBuildWorkflow.
c. Ifneitherthehash-taggednorthegeneric-taggedimageisfound,thesystemwillbuildthe
imagecompletelyfromscratch
CachingandEfficiency. Thesystemattemptstoreuseexistingimageswhenpossibletosavebuild
time. Ifanexactmatch(byhash)isfound,it’susedwithoutrebuilding. Ifacompatibleimageis
found,it’susedasabaseforrebuilding,savingtimeondependencyinstallation.
AflowchartillustratingthebuildprocessisshowninFig.5
G ADDITIONAL RESULTS FOR GPQA BENCHMARK
Weshowcasemoredetailedresults,includingperformanceonothersubsetsforGPQAbenchmark
inTab.7.
22

PublishedasaconferencepaperatICLR2025
Table7: FullEvaluationResultsontheGPQABenchmarkReinetal.(2023)(§4.4).
Accuracybysubset(%)
EvaluationMethodandModel AvgCost($)
DiamondSet MainSet ExtendedSet
ExpertHumanValidators 81.2 72.5 65.4 N/A
Non-ExpertHumanValidators 21.9 30.5 33.9 N/A
Few-ShotCoTLlama-2-70B-chat 28.1 29.1 30.4 N/A
Few-ShotCoTGPT-3.5-turbo-16k 29.6 28.0 28.2 N/A
Few-ShotCoTGPT-4 38.8 39.7 38.7 N/A
GPT-4withsearch(backofftoCoTonabstention) 38.8 41.0 39.4 N/A
OpenHands+CodeActAgentv1.5+GPT3.5-turbo 27.9 23.4 26.1 0.012
OpenHands+CodeActAgentv1.5+GPT4-turbo 51.8 47.4 42.4 0.501
OpenHands+CodeActAgentv1.5+GPT4o 53.1 49.3 52.8 0.054
H IN-CONTEXT DEMONSTRATION FOR CODEACTSWEAGENT
Thepromptisre-adoptedfromtheSWE-agent’sreleasedtrajectory(https://github.com/princeton-nlp/
SWE-agent/tree/main/trajectories/demonstrations). Thepromptcanbefoundathttps://github.com/
All-Hands-AI/OpenHands/blob/main/agenthub/codeact_swe_agent/prompt.py.
I SUPPORTED AGENTSKILLS
AsofOpenHandsv0.6,wesupportthefollowinglistofskills. Pleaserefertothesourcecodeforthe
mostup-to-datelistofskills: https://github.com/All-Hands-AI/OpenHands/blob/main/OpenHands/
runtime/plugins/agent_skills/agentskills.py
def open_file(path: str, line_number: Optional[int] = None) ->
None:
(cid:44)→
"""
Opens the file at the given path in the editor. If line_number
is provided, the window will be moved to include that
(cid:44)→
line.
(cid:44)→
Args:
path: str: The path to the file to open.
line_number: Optional[int]: The line number to move to.
"""
pass
def goto_line(line_number: int) -> None:
"""
Moves the window to show the specified line number.
Args:
line_number: int: The line number to move to.
"""
pass
def scroll_down() -> None:
"""Moves the window down by 100 lines.
Args:
None
"""
pass
23

PublishedasaconferencepaperatICLR2025
def scroll_up() -> None:
"""Moves the window up by 100 lines.
Args:
None
"""
pass
def create_file(filename: str) -> None:
"""Creates and opens a new file with the given name.
Args:
filename: str: The name of the file to create.
"""
pass
def edit_file(start: int, end: int, content: str) -> None:
"""Edit a file.
It replaces lines `start` through `end` (inclusive) with the
given text `content` in the open file. Remember, the file
(cid:44)→
must be open before editing.
(cid:44)→
Args:
start: int: The start line number. Must satisfy start >=
1.
(cid:44)→
end: int: The end line number. Must satisfy start <= end
<= number of lines in the file.
(cid:44)→
content: str: The content to replace the lines with.
"""
pass
def search_dir(search_term: str, dir_path: str = './') -> None:
"""Searches for search_term in all files in dir. If dir is not
provided, searches in the current directory.
(cid:44)→
Args:
search_term: str: The term to search for.
dir_path: Optional[str]: The path to the directory to
search.
(cid:44)→
"""
pass
def search_file(search_term: str, file_path: Optional[str] = None)
-> None:
(cid:44)→
"""Searches for search_term in file. If file is not provided,
searches in the current open file.
(cid:44)→
Args:
search_term: str: The term to search for.
file_path: Optional[str]: The path to the file to search.
"""
pass
def find_file(file_name: str, dir_path: str = './') -> None:
"""Finds all files with the given name in the specified
directory.
(cid:44)→
Args:
24

PublishedasaconferencepaperatICLR2025
| file_name: |     | str:           | The name | of  | the file | to     | find.     |     |
| ---------- | --- | -------------- | -------- | --- | -------- | ------ | --------- | --- |
| dir_path:  |     | Optional[str]: |          | The | path     | to the | directory | to  |
search.
(cid:44)→
"""
pass
| def parse_pdf(file_path: |     |         | str) | -> None: |          |        |     |     |
| ------------------------ | --- | ------- | ---- | -------- | -------- | ------ | --- | --- |
| """Parses                | the | content | of a | PDF      | file and | prints | it. |     |
Args:
| file_path: |     | str: | The path | to  | the file | to  | open. |     |
| ---------- | --- | ---- | -------- | --- | -------- | --- | ----- | --- |
"""
pass
| def parse_docx(file_path: |     |     | str) | -> None: |     |     |     |     |
| ------------------------- | --- | --- | ---- | -------- | --- | --- | --- | --- |
"""
| Parses | the | content | of a DOCX | file | and | prints | it. |     |
| ------ | --- | ------- | --------- | ---- | --- | ------ | --- | --- |
Args:
| file_path: |     | str: | The path | to  | the file | to  | open. |     |
| ---------- | --- | ---- | -------- | --- | -------- | --- | ----- | --- |
"""
pass
| def parse_latex(file_path: |     |     | str) | ->  | None: |     |     |     |
| -------------------------- | --- | --- | ---- | --- | ----- | --- | --- | --- |
"""
| Parses | the | content | of a LaTex | file | and | prints | it. |     |
| ------ | --- | ------- | ---------- | ---- | --- | ------ | --- | --- |
Args:
| file_path: |     | str: | The path | to  | the file | to  | open. |     |
| ---------- | --- | ---- | -------- | --- | -------- | --- | ----- | --- |
"""
pass
def parse_audio(file_path: str, model: str = 'whisper-1') -> None:
"""
| Parses | the | content | of an audio |     | file and | prints | it. |     |
| ------ | --- | ------- | ----------- | --- | -------- | ------ | --- | --- |
Args:
| file_path: |                | str:           | The path | to        | the audio       |     | file to transcribe. |     |
| ---------- | -------------- | -------------- | -------- | --------- | --------------- | --- | ------------------- | --- |
| model:     |                | Optional[str]: |          | The audio | model           |     | to use for          |     |
|            | transcription. |                | Defaults |           | to 'whisper-1'. |     |                     |     |
(cid:44)→
"""
pass
def parse_image(
file_path: str, task: str = 'Describe this image as detail as
possible.'
(cid:44)→
) -> None:
"""
| Parses | the | content | of an image |     | file and | prints | the |     |
| ------ | --- | ------- | ----------- | --- | -------- | ------ | --- | --- |
description.
(cid:44)→
Args:
| file_path: |                | str:     | The path | to        | the file    | to    | open.     |     |
| ---------- | -------------- | -------- | -------- | --------- | ----------- | ----- | --------- | --- |
| task:      | Optional[str]: |          | The      | task      | description |       | for the   | API |
|            | call.          | Defaults | to       | 'Describe | this        | image | as detail | as  |
(cid:44)→
possible.'.
(cid:44)→
"""
pass
25

PublishedasaconferencepaperatICLR2025
def parse_video(
| file_path:      | str,  |           |     |            |     |           |     |             |     |
| --------------- | ----- | --------- | --- | ---------- | --- | --------- | --- | ----------- | --- |
| task:           | str = | 'Describe |     | this image |     | as detail | as  | possible.', |     |
| frame_interval: |       | int       | =   | 30,        |     |           |     |             |     |
) -> None:
"""
| Parses | the content |     | of  | an image | file | and | prints | the |     |
| ------ | ----------- | --- | --- | -------- | ---- | --- | ------ | --- | --- |
description.
(cid:44)→
Args:
| file_path: |                | str:     | The | path         | to the | video       | file  | to open.  |     |
| ---------- | -------------- | -------- | --- | ------------ | ------ | ----------- | ----- | --------- | --- |
| task:      | Optional[str]: |          |     | The          | task   | description |       | for the   | API |
|            | call.          | Defaults |     | to 'Describe |        | this        | image | as detail | as  |
(cid:44)→
| (cid:44)→       | possible.'. |     |                |     |        |     |          |         |        |
| --------------- | ----------- | --- | -------------- | --- | ------ | --- | -------- | ------- | ------ |
| frame_interval: |             |     | Optional[int]: |     |        | The | interval | between | frames |
|                 | to analyze. |     | Defaults       |     | to 30. |     |          |         |        |
(cid:44)→
"""
pass
| def parse_pptx(file_path: |     |     |     | str) -> | None: |     |     |     |     |
| ------------------------- | --- | --- | --- | ------- | ----- | --- | --- | --- | --- |
"""
| Parses | the content |     | of  | a pptx | file | and prints |     | it. |     |
| ------ | ----------- | --- | --- | ------ | ---- | ---------- | --- | --- | --- |
Args:
| file_path: |     | str: | The | path | to the | file | to  | open. |     |
| ---------- | --- | ---- | --- | ---- | ------ | ---- | --- | ----- | --- |
"""
pass
| J BROWSERGYM |     | ACTIONS |     |     |     |     |     |     |     |
| ------------ | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
ThefollowingareallthesupportedactionsdefinedinBrowserGym5asofv0.3.4.
Theactionscan
be categorized into several types and can be configured to use only a subset of the functionality.
Thereareagentcontrolactions,navigationactions,pageelement-basedactions,coordinate-based
actions,aswellastab-relatedactions. WeusetheseactionsfromtheBrowserGymlibraryasour
mainbrowsingactionprimitives.
| def send_msg_to_user(text: |     |     |     | str): |     |     |     |     |     |
| -------------------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
"""
| Sends | a message | to  | the | user. |     |     |     |     |     |
| ----- | --------- | --- | --- | ----- | --- | --- | --- | --- | --- |
Examples:
| send_msg_to_user("Based |      |     |       |            | on the | results | of  | my search, | the |
| ----------------------- | ---- | --- | ----- | ---------- | ------ | ------- | --- | ---------- | --- |
|                         | city | was | built | in 1751.") |        |         |     |            |     |
(cid:44)→
"""
pass
| def report_infeasible(reason: |     |     |     | str): |     |     |     |     |     |
| ----------------------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
"""
| Notifies | the | user | that | their | instructions |     | are | infeasible. |     |
| -------- | --- | ---- | ---- | ----- | ------------ | --- | --- | ----------- | --- |
Examples:
| report_infeasible("I |         |       |     | cannot | follow |       | these   | instructions |     |
| -------------------- | ------- | ----- | --- | ------ | ------ | ----- | ------- | ------------ | --- |
|                      | because | there |     | is no  | email  | field | in this | form.")      |     |
(cid:44)→
"""
5https://github.com/ServiceNow/BrowserGym/blob/main/core/src/browsergym/core/action/functions.py
26

PublishedasaconferencepaperatICLR2025
pass
| def noop(wait_ms: |     |     | float | = 1000): |     |     |     |     |
| ----------------- | --- | --- | ----- | -------- | --- | --- | --- | --- |
"""
| Do  | nothing, | and | optionally |     | wait | for | the given | time (in |
| --- | -------- | --- | ---------- | --- | ---- | --- | --------- | -------- |
milliseconds).
(cid:44)→
Examples:
noop()
noop(500)
"""
pass
# https://playwright.dev/docs/input#text-input
| def fill(bid: |     | str, | value: | str): |     |     |     |     |
| ------------- | --- | ---- | ------ | ----- | --- | --- | --- | --- |
"""
Fill out a form field. It focuses the element and triggers an
|     | input | event | with | the | entered | text. |     |     |
| --- | ----- | ----- | ---- | --- | ------- | ----- | --- | --- |
(cid:44)→
| It        | works     | for | <input>, | <textarea> |     | and | [contenteditable] |     |
| --------- | --------- | --- | -------- | ---------- | --- | --- | ----------------- | --- |
| (cid:44)→ | elements. |     |          |            |     |     |                   |     |
Examples:
|     | fill('237', |     | 'example                |     | value') |                |     |     |
| --- | ----------- | --- | ----------------------- | --- | ------- | -------------- | --- | --- |
|     | fill('45',  |     | "multi-line\\nexample") |     |         |                |     |     |
|     | fill('a12', |     | "example                |     | with    | \\"quotes\\"") |     |     |
"""
pass
#
https://playwright.dev/python/docs/api/class-locator#locator-check
(cid:44)→
| def check(bid: |     | str): |     |     |     |     |     |     |
| -------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
"""
| Ensure |     | a checkbox | or  | radio | element |     | is checked. |     |
| ------ | --- | ---------- | --- | ----- | ------- | --- | ----------- | --- |
Examples:
check('55')
"""
pass
#
https://playwright.dev/python/docs/api/class-locator#locator-uncheck
(cid:44)→
| def uncheck(bid: |     |     | str): |     |     |     |     |     |
| ---------------- | --- | --- | ----- | --- | --- | --- | --- | --- |
"""
| Ensure |     | a checkbox | or  | radio | element |     | is unchecked. |     |
| ------ | --- | ---------- | --- | ----- | ------- | --- | ------------- | --- |
Examples:
uncheck('a5289')
"""
pass
# https://playwright.dev/docs/input#select-options
| def select_option(bid: |     |     |     | str, | options: | str | | list[str]): |     |
| ---------------------- | --- | --- | --- | ---- | -------- | --- | ------------- | --- |
"""
27

PublishedasaconferencepaperatICLR2025
Select one or multiple options in a <select> element. You can
specify
(cid:44)→
| option value | or label |     | to select. | Multiple | options can | be  |
| ------------ | -------- | --- | ---------- | -------- | ----------- | --- |
selected.
(cid:44)→
Examples:
| select_option('a48', |     |     | "blue") |          |          |     |
| -------------------- | --- | --- | ------- | -------- | -------- | --- |
| select_option('c48', |     |     | ["red", | "green", | "blue"]) |     |
"""
pass
#
https://playwright.dev/python/docs/api/class-locator#locator-click
(cid:44)→
def click(
bid: str,
| button: Literal["left", |     |     | "middle", | "right"] | = "left", |     |
| ----------------------- | --- | --- | --------- | -------- | --------- | --- |
modifiers: list[Literal["Alt", "Control", "Meta", "Shift"]] =
[],
(cid:44)→
):
"""
| Click an element. |     |     |     |     |     |     |
| ----------------- | --- | --- | --- | --- | --- | --- |
Examples:
click('a51')
| click('b22', |                  | button="right") |     |                      |     |     |
| ------------ | ---------------- | --------------- | --- | -------------------- | --- | --- |
| click('48',  | button="middle", |                 |     | modifiers=["Shift"]) |     |     |
"""
pass
#
https://playwright.dev/python/docs/api/class-locator#locator-dblclick
(cid:44)→
def dblclick(
bid: str,
| button: Literal["left", |     |     | "middle", | "right"] | = "left", |     |
| ----------------------- | --- | --- | --------- | -------- | --------- | --- |
modifiers: list[Literal["Alt", "Control", "Meta", "Shift"]] =
(cid:44)→ [],
):
"""
| Double click | an element. |     |     |     |     |     |
| ------------ | ----------- | --- | --- | --- | --- | --- |
Examples:
dblclick('12')
| dblclick('ca42', |     | button="right")  |     |                      |     |     |
| ---------------- | --- | ---------------- | --- | -------------------- | --- | --- |
| dblclick('178',  |     | button="middle", |     | modifiers=["Shift"]) |     |     |
"""
pass
#
https://playwright.dev/python/docs/api/class-locator#locator-hover
(cid:44)→
| def hover(bid: | str): |     |     |     |     |     |
| -------------- | ----- | --- | --- | --- | --- | --- |
"""
| Hover over | an element. |     |     |     |     |     |
| ---------- | ----------- | --- | --- | --- | --- | --- |
Examples:
hover('b8')
"""
28

PublishedasaconferencepaperatICLR2025
pass
# https://playwright.dev/python/docs/input#keys-and-shortcuts
| def press(bid: | str, | key_comb: |     | str): |     |     |     |     |
| -------------- | ---- | --------- | --- | ----- | --- | --- | --- | --- |
"""
Focus the matching element and press a combination of keys. It
accepts
(cid:44)→
| the logical       | key | names | that     | are | emitted |     | in the |     |
| ----------------- | --- | ----- | -------- | --- | ------- | --- | ------ | --- |
| keyboardEvent.key |     |       | property |     |         |     |        |     |
(cid:44)→
| of the | keyboard | events: |     | Backquote, |     | Minus, | Equal, | Backslash, |
| ------ | -------- | ------- | --- | ---------- | --- | ------ | ------ | ---------- |
Backspace,
(cid:44)→
| Tab, Delete, |     | Escape, | ArrowDown, |     | End, | Enter, | Home, | Insert, |
| ------------ | --- | ------- | ---------- | --- | ---- | ------ | ----- | ------- |
PageDown, PageUp,
(cid:44)→
| ArrowRight,    | ArrowUp, |     | F1  | - F12, | Digit0 | -   | Digit9, | KeyA - KeyZ, |
| -------------- | -------- | --- | --- | ------ | ------ | --- | ------- | ------------ |
| (cid:44)→ etc. | You      | can |     |        |        |     |         |              |
alternatively specify a single character you'd like to produce
such as "a"
(cid:44)→
| or "#". | Following |     | modification |     | shortcuts |     | are also | supported: |
| ------- | --------- | --- | ------------ | --- | --------- | --- | -------- | ---------- |
Shift, Control,
(cid:44)→
| Alt, Meta. |     |     |     |     |     |     |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
Examples:
press('88', 'Backspace')
| press('a26', |     | 'Control+a')    |     |     |     |     |     |     |
| ------------ | --- | --------------- | --- | --- | --- | --- | --- | --- |
| press('a61', |     | 'Meta+Shift+t') |     |     |     |     |     |     |
"""
pass
#
(cid:44)→ https://playwright.dev/python/docs/api/class-locator#locator-focus
| def focus(bid: | str): |     |     |     |     |     |     |     |
| -------------- | ----- | --- | --- | --- | --- | --- | --- | --- |
"""
| Focus the | matching |     | element. |     |     |     |     |     |
| --------- | -------- | --- | -------- | --- | --- | --- | --- | --- |
Examples:
focus('b455')
"""
pass
#
https://playwright.dev/python/docs/api/class-locator#locator-clear
(cid:44)→
| def clear(bid: | str): |     |     |     |     |     |     |     |
| -------------- | ----- | --- | --- | --- | --- | --- | --- | --- |
"""
| Clear the | input | field. |     |     |     |     |     |     |
| --------- | ----- | ------ | --- | --- | --- | --- | --- | --- |
Examples:
clear('996')
"""
pass
# https://playwright.dev/python/docs/input#drag-and-drop
| def drag_and_drop(from_bid: |     |     |     | str, | to_bid: | str): |     |     |
| --------------------------- | --- | --- | --- | ---- | ------- | ----- | --- | --- |
"""
Perform a drag & drop. Hover the element that will be dragged.
Press
(cid:44)→
29

PublishedasaconferencepaperatICLR2025
left mouse button. Move mouse to the element that will receive
the
(cid:44)→
|     | drop. | Release | left | mouse | button. |     |     |     |     |     |
| --- | ----- | ------- | ---- | ----- | ------- | --- | --- | --- | --- | --- |
Examples:
|     | drag_and_drop('56', |     |     |     | '498') |     |     |     |     |     |
| --- | ------------------- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
"""
pass
# https://playwright.dev/python/docs/api/class-mouse#mouse-wheel
| def | scroll(delta_x: |     |     | float, | delta_y: | float): |     |     |     |     |
| --- | --------------- | --- | --- | ------ | -------- | ------- | --- | --- | --- | --- |
"""
|     | Scroll   | horizontally |     | and   | vertically. |                 | Amounts |          | in pixels, |     |
| --- | -------- | ------------ | --- | ----- | ----------- | --------------- | ------- | -------- | ---------- | --- |
|     | positive |              | for | right | or          | down scrolling, |         | negative | for left   | or  |
(cid:44)→
|     | (cid:44)→ up | scrolling. |     | Dispatches |     | a wheel | event. |     |     |     |
| --- | ------------ | ---------- | --- | ---------- | --- | ------- | ------ | --- | --- | --- |
Examples:
|     | scroll(0,     |     | 200) |         |     |     |     |     |     |     |
| --- | ------------- | --- | ---- | ------- | --- | --- | --- | --- | --- | --- |
|     | scroll(-50.2, |     |      | -100.5) |     |     |     |     |     |     |
"""
pass
# https://playwright.dev/python/docs/api/class-mouse#mouse-move
| def | mouse_move(x: |     | float, |     | y: float): |     |     |     |     |     |
| --- | ------------- | --- | ------ | --- | ---------- | --- | --- | --- | --- | --- |
"""
Move the mouse to a location. Uses absolute client coordinates
in pixels.
(cid:44)→
|     | Dispatches |     | a mousemove |     | event. |     |     |     |     |     |
| --- | ---------- | --- | ----------- | --- | ------ | --- | --- | --- | --- | --- |
Examples:
|     | mouse_move(65.2, |     |     |     | 158.5) |     |     |     |     |     |
| --- | ---------------- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
"""
pass
# https://playwright.dev/python/docs/api/class-mouse#mouse-up
def mouse_up(x: float, y: float, button: Literal["left", "middle",
|     | "right"] | =   | "left"): |     |     |     |     |     |     |     |
| --- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
(cid:44)→
"""
|     | Move the             | mouse | to      | a location |         | then | release | a   | mouse button. |     |
| --- | -------------------- | ----- | ------- | ---------- | ------- | ---- | ------- | --- | ------------- | --- |
|     | (cid:44)→ Dispatches |       |         |            |         |      |         |     |               |     |
|     | mousemove            | and   | mouseup |            | events. |      |         |     |               |     |
Examples:
|     | mouse_up(250, |     |     | 120) |          |     |     |     |     |     |
| --- | ------------- | --- | --- | ---- | -------- | --- | --- | --- | --- | --- |
|     | mouse_up(47,  |     |     | 252, | 'right') |     |     |     |     |     |
"""
pass
# https://playwright.dev/python/docs/api/class-mouse#mouse-down
| def | mouse_down(x: |          | float, |     | y: float, | button: |     | Literal["left", |     |     |
| --- | ------------- | -------- | ------ | --- | --------- | ------- | --- | --------------- | --- | --- |
|     | "middle",     | "right"] |        | =   | "left"):  |         |     |                 |     |     |
(cid:44)→
"""
|     | Move the          | mouse | to         | a location |         | then | press | and | hold a mouse |     |
| --- | ----------------- | ----- | ---------- | ---------- | ------- | ---- | ----- | --- | ------------ | --- |
|     | (cid:44)→ button. |       | Dispatches |            |         |      |       |     |              |     |
|     | mousemove         | and   | mousedown  |            | events. |      |       |     |              |     |
30

PublishedasaconferencepaperatICLR2025
Examples:
|     | mouse_down(140.2, |     |     | 580.1) |           |     |     |     |     |
| --- | ----------------- | --- | --- | ------ | --------- | --- | --- | --- | --- |
|     | mouse_down(458,   |     |     | 254.5, | 'middle') |     |     |     |     |
"""
pass
# https://playwright.dev/python/docs/api/class-mouse#mouse-click
| def mouse_click(x:  |     |          | float, | y: float,  |     | button: | Literal["left", |     |     |
| ------------------- | --- | -------- | ------ | ---------- | --- | ------- | --------------- | --- | --- |
| (cid:44)→ "middle", |     | "right"] |        | = "left"): |     |         |                 |     |     |
"""
| Move | the        | mouse | to         | a location | and | click | a mouse | button. |     |
| ---- | ---------- | ----- | ---------- | ---------- | --- | ----- | ------- | ------- | --- |
|      | Dispatches |       | mousemove, |            |     |       |         |         |     |
(cid:44)→
| mousedown |     | and | mouseup | events. |     |     |     |     |     |
| --------- | --- | --- | ------- | ------- | --- | --- | --- | --- | --- |
Examples:
|     | mouse_click(887.2, |     |     | 68)     |          |     |     |     |     |
| --- | ------------------ | --- | --- | ------- | -------- | --- | --- | --- | --- |
|     | mouse_click(56,    |     |     | 712.56, | 'right') |     |     |     |     |
"""
pass
#
https://playwright.dev/python/docs/api/class-mouse#mouse-dblclick
(cid:44)→
def mouse_dblclick(x: float, y: float, button: Literal["left",
| (cid:44)→ "middle", |     | "right"] |     | = "left"): |     |     |     |     |     |
| ------------------- | --- | -------- | --- | ---------- | --- | --- | --- | --- | --- |
"""
Move the mouse to a location and double click a mouse button.
Dispatches
(cid:44)→
| mousemove, |     | mousedown |     | and mouseup |     | events. |     |     |     |
| ---------- | --- | --------- | --- | ----------- | --- | ------- | --- | --- | --- |
Examples:
|     | mouse_dblclick(5,    |     |     | 236) |          |     |     |     |     |
| --- | -------------------- | --- | --- | ---- | -------- | --- | --- | --- | --- |
|     | mouse_dblclick(87.5, |     |     | 354, | 'right') |     |     |     |     |
"""
pass
def mouse_drag_and_drop(from_x: float, from_y: float, to_x: float,
| to_y: |     | float): |     |     |     |     |     |     |     |
| ----- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
(cid:44)→
"""
| Drag | and | drop | from | a location | to  | a location. |     | Uses absolute |     |
| ---- | --- | ---- | ---- | ---------- | --- | ----------- | --- | ------------- | --- |
client
(cid:44)→
| coordinates |     |     | in pixels. | Dispatches |     | mousemove, |     | mousedown | and |
| ----------- | --- | --- | ---------- | ---------- | --- | ---------- | --- | --------- | --- |
mouseup
(cid:44)→
events.
Examples:
|     | mouse_drag_and_drop(10.7, |     |     |     | 325, | 235.6, |     | 24.54) |     |
| --- | ------------------------- | --- | --- | --- | ---- | ------ | --- | ------ | --- |
"""
pass
#
https://playwright.dev/python/docs/api/class-keyboard#keyboard-press
(cid:44)→
| def keyboard_press(key: |     |     |     | str): |     |     |     |     |     |
| ----------------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
"""
31

PublishedasaconferencepaperatICLR2025
| Press | a combination | of  | keys. | Accepts |     | the logical |     | key names |
| ----- | ------------- | --- | ----- | ------- | --- | ----------- | --- | --------- |
| that  | are           |     |       |         |     |             |     |           |
(cid:44)→
| emitted | in the keyboardEvent.key |     |     |     | property | of  | the | keyboard |
| ------- | ------------------------ | --- | --- | --- | -------- | --- | --- | -------- |
events:
(cid:44)→
| Backquote, | Minus, | Equal, | Backslash, |     | Backspace, |     | Tab, | Delete, |
| ---------- | ------ | ------ | ---------- | --- | ---------- | --- | ---- | ------- |
(cid:44)→ Escape,
| ArrowDown, | End, | Enter, | Home, | Insert, |     | PageDown, | PageUp, |     |
| ---------- | ---- | ------ | ----- | ------- | --- | --------- | ------- | --- |
ArrowRight,
(cid:44)→
ArrowUp, F1 - F12, Digit0 - Digit9, KeyA - KeyZ, etc. You can
alternatively specify a single character you'd like to produce
(cid:44)→ such
| as "a" | or "#". Following |     | modification |     |     | shortcuts | are | also |
| ------ | ----------------- | --- | ------------ | --- | --- | --------- | --- | ---- |
supported:
(cid:44)→
| Shift, | Control, | Alt, Meta. |     |     |     |     |     |     |
| ------ | -------- | ---------- | --- | --- | --- | --- | --- | --- |
Examples:
keyboard_press('Backspace')
keyboard_press('Control+a')
keyboard_press('Meta+Shift+t')
page.keyboard.press("PageDown")
"""
pass
#
https://playwright.dev/python/docs/api/class-keyboard#keyboard-up
(cid:44)→
| def keyboard_up(key: |     | str): |     |     |     |     |     |     |
| -------------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
"""
Release a keyboard key. Dispatches a keyup event. Accepts the
logical
(cid:44)→
| key names    | that are | emitted    |     | in the | keyboardEvent.key |            |     | property |
| ------------ | -------- | ---------- | --- | ------ | ----------------- | ---------- | --- | -------- |
| (cid:44)→ of | the      |            |     |        |                   |            |     |          |
| keyboard     | events:  | Backquote, |     | Minus, | Equal,            | Backslash, |     |          |
| Backspace,   | Tab,     |            |     |        |                   |            |     |          |
(cid:44)→
Delete, Escape, ArrowDown, End, Enter, Home, Insert, PageDown,
PageUp,
(cid:44)→
| ArrowRight, | ArrowUp, | F1  | - F12, | Digit0 |     | - Digit9, | KeyA | - KeyZ, |
| ----------- | -------- | --- | ------ | ------ | --- | --------- | ---- | ------- |
(cid:44)→ etc.
You can alternatively specify a single character you'd like to
produce
(cid:44)→
| such as | "a" or "#". |     |     |     |     |     |     |     |
| ------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
Examples:
keyboard_up('Shift')
keyboard_up('c')
"""
pass
#
https://playwright.dev/python/docs/api/class-keyboard#keyboard-down
(cid:44)→
| def keyboard_down(key: |     | str): |     |     |     |     |     |     |
| ---------------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
"""
| Press   | and holds | a keyboard |     | key. | Dispatches |     | a keydown | event. |
| ------- | --------- | ---------- | --- | ---- | ---------- | --- | --------- | ------ |
| Accepts | the       |            |     |      |            |     |           |        |
(cid:44)→
| logical  | key names | that | are | emitted | in  | the keyboardEvent.key |     |     |
| -------- | --------- | ---- | --- | ------- | --- | --------------------- | --- | --- |
| property | of        |      |     |         |     |                       |     |     |
(cid:44)→
| the keyboard | events: | Backquote, |     |     | Minus, | Equal, | Backslash, |     |
| ------------ | ------- | ---------- | --- | --- | ------ | ------ | ---------- | --- |
| Backspace,   | Tab,    |            |     |     |        |        |            |     |
(cid:44)→
32

PublishedasaconferencepaperatICLR2025
Delete, Escape, ArrowDown, End, Enter, Home, Insert, PageDown,
PageUp,
(cid:44)→
| ArrowRight, |     | ArrowUp, |     | F1 - F12, | Digit0 | - Digit9, | KeyA | - KeyZ, |
| ----------- | --- | -------- | --- | --------- | ------ | --------- | ---- | ------- |
| etc.        | You | can      |     |           |        |           |      |         |
(cid:44)→
| alternatively |     | specify |     | a single | character | such | as "a" | or "#". |
| ------------- | --- | ------- | --- | -------- | --------- | ---- | ------ | ------- |
Examples:
keyboard_up('Shift')
keyboard_up('c')
"""
pass
#
https://playwright.dev/python/docs/api/class-keyboard#keyboard-type
(cid:44)→
| def keyboard_type(text: |     |     | str): |     |     |     |     |     |
| ----------------------- | --- | --- | ----- | --- | --- | --- | --- | --- |
"""
Types a string of text through the keyboard. Sends a keydown,
keypress/input,
(cid:44)→
and keyup event for each character in the text. Modifier keys
| (cid:44)→ DO   | NOT   | affect  |     |      |            |          |     |         |
| -------------- | ----- | ------- | --- | ---- | ---------- | -------- | --- | ------- |
| keyboard_type. |       | Holding |     | down | Shift will | not type | the | text in |
| upper          | case. |         |     |      |            |          |     |         |
(cid:44)→
Examples:
| keyboard_type('Hello |     |     |     | world!') |     |     |     |     |
| -------------------- | --- | --- | --- | -------- | --- | --- | --- | --- |
"""
pass
#
(cid:44)→ https://playwright.dev/python/docs/api/class-keyboard#keyboard-insert-text
| def keyboard_insert_text(text: |     |     |     | str): |     |     |     |     |
| ------------------------------ | --- | --- | --- | ----- | --- | --- | --- | --- |
"""
| Insert     | a string |      | of text | in the | currently | focused | element. |     |
| ---------- | -------- | ---- | ------- | ------ | --------- | ------- | -------- | --- |
| Dispatches |          | only | input   |        |           |         |          |     |
(cid:44)→
| event,             | does | not  | emit | the keydown, | keyup | or keypress |     | events. |
| ------------------ | ---- | ---- | ---- | ------------ | ----- | ----------- | --- | ------- |
| (cid:44)→ Modifier |      | keys | DO   | NOT          |       |             |     |         |
affect keyboard_insert_text. Holding down Shift will not type
| the | text | in  | upper |     |     |     |     |     |
| --- | ---- | --- | ----- | --- | --- | --- | --- | --- |
(cid:44)→
case.
Examples:
| keyboard_insert_text('Hello |     |     |     |     | world!') |     |     |     |
| --------------------------- | --- | --- | --- | --- | -------- | --- | --- | --- |
"""
pass
# https://playwright.dev/python/docs/api/class-page#page-goto
| def goto(url: | str): |     |     |     |     |     |     |     |
| ------------- | ----- | --- | --- | --- | --- | --- | --- | --- |
"""
| Navigate | to  | a url. |     |     |     |     |     |     |
| -------- | --- | ------ | --- | --- | --- | --- | --- | --- |
Examples:
goto('http://www.example.com')
"""
pass
33

PublishedasaconferencepaperatICLR2025
# https://playwright.dev/python/docs/api/class-page#page-go-back
def go_back():
"""
Navigate to the previous page in history.
Examples:
go_back()
"""
pass
#
https://playwright.dev/python/docs/api/class-page#page-go-forward
(cid:44)→
def go_forward():
"""
Navigate to the next page in history.
Examples:
go_forward()
"""
pass
#
https://playwright.dev/python/docs/api/class-browsercontext#browser-context-new-page
(cid:44)→
def new_tab():
"""
Open a new tab. It will become the active one.
Examples:
new_tab()
"""
global page
# set the new page as the active page
page = page.context.new_page()
# trigger the callback that sets this page as active in
browsergym
(cid:44)→
pass
# https://playwright.dev/python/docs/api/class-page#page-close
def tab_close():
"""
Close the current tab.
Examples:
tab_close()
"""
pass
#
https://playwright.dev/python/docs/api/class-page#page-bring-to-front
(cid:44)→
def tab_focus(index: int):
"""
Bring tab to front (activate tab).
Examples:
tab_focus(2)
34

PublishedasaconferencepaperatICLR2025
"""
pass
# https://playwright.dev/python/docs/input#upload-files
| def upload_file(bid: |     | str, | file: | str | | list[str]): |     |     |
| -------------------- | --- | ---- | ----- | --- | ------------- | --- | --- |
"""
| Click | an element | and | wait for | a   | "filechooser" | event, | then |
| ----- | ---------- | --- | -------- | --- | ------------- | ------ | ---- |
select one
(cid:44)→
| or multiple        | input  | files   | for     | upload. | Relative   | file     | paths are |
| ------------------ | ------ | ------- | ------- | ------- | ---------- | -------- | --------- |
| (cid:44)→ resolved |        |         |         |         |            |          |           |
| relative           | to the | current | working |         | directory. | An empty | list      |
clears the
(cid:44)→
| selected | files. |     |     |     |     |     |     |
| -------- | ------ | --- | --- | --- | --- | --- | --- |
Examples:
| upload_file("572", |     |     | "my_receipt.pdf")                 |     |     |     |     |
| ------------------ | --- | --- | --------------------------------- | --- | --- | --- | --- |
| upload_file("63",  |     |     | ["/home/bob/Documents/image.jpg", |     |     |     |     |
"/home/bob/Documents/file.zip"])
(cid:44)→
"""
pass
# https://playwright.dev/python/docs/input#upload-files
def mouse_upload_file(x: float, y: float, file: str | list[str]):
"""
| Click | a location | and | wait for | a   | "filechooser" | event, | then |
| ----- | ---------- | --- | -------- | --- | ------------- | ------ | ---- |
select one
(cid:44)→
| or multiple | input | files | for | upload. | Relative | file | paths are |
| ----------- | ----- | ----- | --- | ------- | -------- | ---- | --------- |
resolved
(cid:44)→
| relative         | to the | current | working |     | directory. | An empty | list |
| ---------------- | ------ | ------- | ------- | --- | ---------- | -------- | ---- |
| (cid:44)→ clears | the    |         |         |     |            |          |      |
| selected         | files. |         |         |     |            |          |      |
Examples:
| mouse_upload_file(132.1, |     |     |     | 547, | "my_receipt.pdf") |     |     |
| ------------------------ | --- | --- | --- | ---- | ----------------- | --- | --- |
| mouse_upload_file(328,   |     |     |     | 812, |                   |     |     |
(cid:44)→ ["/home/bob/Documents/image.jpg",
"/home/bob/Documents/file.zip"])
(cid:44)→
"""
pass
| K BROWSING | AGENT | DETAILS |     |     |     |     |     |
| ---------- | ----- | ------- | --- | --- | --- | --- | --- |
Thefollowingshowsanexamplepromptcontainingalltheinformationrequiredforthecurrentstep
tomakeapredictionaboutthenextbrowsingactions. Notethatwealsoinstructtheagenttopredict
multipleactionsinoneturniftheagentthinkstheyaremeanttobeexecutedsequentiallywithoutany
feedbackfromthepage. Thiscouldsaveturnsforcommonworkflowsthatconsistofasequenceof
actionsonthesamepagewithoutanyobservationchange,suchasfillingtheusernameandpassword
andsubmitinaloginpage.
# Instructions
Review the current state of the page and all other information to
(cid:44)→ find the best possible next action to accomplish your goal.
| Your answer | will | be interpreted |     |     | and executed | by a | program, |
| ----------- | ---- | -------------- | --- | --- | ------------ | ---- | -------- |
(cid:44)→
| make sure | to follow | the | formatting |     | instructions. |     |     |
| --------- | --------- | --- | ---------- | --- | ------------- | --- | --- |
(cid:44)→
35

PublishedasaconferencepaperatICLR2025
# Goal:
Browse localhost:8000, and tell me the ultimate answer to life. Do
| not | ask | me for | confirmation |     |     | at any | point. |     |     |     |
| --- | --- | ------ | ------------ | --- | --- | ------ | ------ | --- | --- | --- |
(cid:44)→
| # Action      | Space |       |     |         |     |            |     |     |     |     |
| ------------- | ----- | ----- | --- | ------- | --- | ---------- | --- | --- | --- | --- |
| 16 different  |       | types | of  | actions | are | available. |     |     |     |     |
| noop(wait_ms: |       | float | =   | 1000)   |     |            |     |     |     |     |
Examples:
noop()
noop(500)
| send_msg_to_user(text: |     |     |     | str) |     |     |     |     |     |     |
| ---------------------- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
Examples:
|     | send_msg_to_user('Based |      |     |       |            | on the | results |     | of my search, | the |
| --- | ----------------------- | ---- | --- | ----- | ---------- | ------ | ------- | --- | ------------- | --- |
|     |                         | city | was | built | in 1751.') |        |         |     |               |     |
(cid:44)→
| scroll(delta_x: |     |     | float, | delta_y: |     | float) |     |     |     |     |
| --------------- | --- | --- | ------ | -------- | --- | ------ | --- | --- | --- | --- |
Examples:
|           | scroll(0,     |             | 200) |         |     |     |     |     |     |     |
| --------- | ------------- | ----------- | ---- | ------- | --- | --- | --- | --- | --- | --- |
|           | scroll(-50.2, |             |      | -100.5) |     |     |     |     |     |     |
| fill(bid: |               | str, value: |      | str)    |     |     |     |     |     |     |
Examples:
|                    | fill('237', |     | 'example               |          | value') |            |              |     |     |     |
| ------------------ | ----------- | --- | ---------------------- | -------- | ------- | ---------- | ------------ | --- | --- | --- |
|                    | fill('45',  |     | 'multi-line\nexample') |          |         |            |              |     |     |     |
|                    | fill('a12', |     | 'example               |          | with    | "quotes"') |              |     |     |     |
| select_option(bid: |             |     | str,                   | options: |         | str        | | list[str]) |     |     |     |
Examples:
|            | select_option('48', |            |         |                            | 'blue') |          |           |          |            |     |
| ---------- | ------------------- | ---------- | ------- | -------------------------- | ------- | -------- | --------- | -------- | ---------- | --- |
|            | select_option('48', |            |         |                            | ['red', | 'green', |           | 'blue']) |            |     |
| click(bid: |                     | str,       | button: | Literal['left',            |         |          | 'middle', |          | 'right']   | =   |
| 'left',    |                     | modifiers: |         | list[typing.Literal['Alt', |         |          |           |          | 'Control', |     |
(cid:44)→
| (cid:44)→ 'Meta', |     | 'Shift']] |     | = []) |     |     |     |     |     |     |
| ----------------- | --- | --------- | --- | ----- | --- | --- | --- | --- | --- | --- |
Examples:
click('51')
|     | click('b22', |     |                  | button='right') |     |     |                      |     |     |     |
| --- | ------------ | --- | ---------------- | --------------- | --- | --- | -------------------- | --- | --- | --- |
|     | click('48',  |     | button='middle', |                 |     |     | modifiers=['Shift']) |     |     |     |
dblclick(bid: str, button: Literal['left', 'middle', 'right'] =
| 'left', |     | modifiers: |     | list[typing.Literal['Alt', |     |     |     |     | 'Control', |     |
| ------- | --- | ---------- | --- | -------------------------- | --- | --- | --- | --- | ---------- | --- |
(cid:44)→
| 'Meta', |     | 'Shift']] |     | = []) |     |     |     |     |     |     |
| ------- | --- | --------- | --- | ----- | --- | --- | --- | --- | --- | --- |
(cid:44)→
Examples:
dblclick('12')
|     | dblclick('ca42', |     |     | button='right')  |     |     |                      |     |     |     |
| --- | ---------------- | --- | --- | ---------------- | --- | --- | -------------------- | --- | --- | --- |
|     | dblclick('178',  |     |     | button='middle', |     |     | modifiers=['Shift']) |     |     |     |
36

PublishedasaconferencepaperatICLR2025
| hover(bid: |     | str) |     |     |     |     |     |     |     |
| ---------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
Examples:
hover('b8')
| press(bid: |     | str, key_comb: |     | str) |     |     |     |     |     |
| ---------- | --- | -------------- | --- | ---- | --- | --- | --- | --- | --- |
Examples:
|            | press('88',  |      | 'Backspace')    |     |     |     |     |     |     |
| ---------- | ------------ | ---- | --------------- | --- | --- | --- | --- | --- | --- |
|            | press('a26', |      | 'Control+a')    |     |     |     |     |     |     |
|            | press('a61', |      | 'Meta+Shift+t') |     |     |     |     |     |     |
| focus(bid: |              | str) |                 |     |     |     |     |     |     |
Examples:
focus('b455')
| clear(bid: |     | str) |     |     |     |     |     |     |     |
| ---------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
Examples:
clear('996')
| drag_and_drop(from_bid: |     |     |     | str, | to_bid: | str) |     |     |     |
| ----------------------- | --- | --- | --- | ---- | ------- | ---- | --- | --- | --- |
Examples:
|                  | drag_and_drop('56', |     |            | '498') |     |            |     |     |     |
| ---------------- | ------------------- | --- | ---------- | ------ | --- | ---------- | --- | --- | --- |
| upload_file(bid: |                     |     | str, file: | str    | |   | list[str]) |     |     |     |
Examples:
|     | upload_file('572', |     |     | 'my_receipt.pdf')                 |     |     |     |     |     |
| --- | ------------------ | --- | --- | --------------------------------- | --- | --- | --- | --- | --- |
|     | upload_file('63',  |     |     | ['/home/bob/Documents/image.jpg', |     |     |     |     |     |
'/home/bob/Documents/file.zip'])
(cid:44)→
go_back()
Examples:
go_back()
go_forward()
Examples:
go_forward()
| goto(url: |     | str) |     |     |     |     |     |     |     |
| --------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
Examples:
goto('http://www.example.com')
| Multiple    | actions |          | can be | provided   | at  | once. | Example: |     |     |
| ----------- | ------- | -------- | ------ | ---------- | --- | ----- | -------- | --- | --- |
| fill('a12', |         | 'example | with   | "quotes"') |     |       |          |     |     |
click('51')
| click('48', |     | button='middle', |     |     | modifiers=['Shift']) |     |     |     |     |
| ----------- | --- | ---------------- | --- | --- | -------------------- | --- | --- | --- | --- |
Multiple actions are meant to be executed sequentially without any
| feedback |     | from | the page. |     |     |     |     |     |     |
| -------- | --- | ---- | --------- | --- | --- | --- | --- | --- | --- |
(cid:44)→
Don't execute multiple actions at once if you need feedback from
| the | page. |     |     |     |     |     |     |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:44)→
| # Current   |      | Accessibility |          | Tree:    |               |            |     |               |        |
| ----------- | ---- | ------------- | -------- | -------- | ------------- | ---------- | --- | ------------- | ------ |
| RootWebArea |      | 'The          | Ultimate | Answer', |               | focused    |     |               |        |
|             | [8]  | heading       | 'The     | Ultimate |               | Answer'    |     |               |        |
|             | [9]  | paragraph     | ''       |          |               |            |     |               |        |
|             |      | StaticText    |          | 'Click   |               | the button |     | to reveal the | answer |
|             |      | (cid:44)→     | to       | life,    | the universe, |            | and | everything.'  |        |
|             | [10] | button        | 'Click   | me',     | clickable     |            |     |               |        |
37

PublishedasaconferencepaperatICLR2025
# Previous Actions
goto('http://localhost:8000')
Here is an example with chain of thought of a valid action when
clicking on a button:
(cid:44)→
"
In order to accomplish my goal I need to click on the button with
bid 12
(cid:44)→
```click("12")```
Andanexampleresponsetotheabovepromptis:
In order to accomplish my goal, I need to click on the button with
bid 10 to reveal the answer to life, the universe, and
(cid:44)→
everything.
(cid:44)→
```click("10")```
FortheevaluationonWebArenabenchmark,sincesomeofthetasksrequirecheckingforanswer
exactmatchontheagent’smessagebacktotheuser,weaddthefollowinginstructiontolettheagent
replywithonlyaconciseanswerstringwhenmessagingtheusertopreventtheagentfromfailingthe
testduetoextratext:
Here is another example with chain of thought of a valid action
when providing a concise answer to user:
(cid:44)→
"
In order to accomplish my goal I need to send the information
asked back to the user. This page list the information of HP
(cid:44)→
Inkjet Fax Machine, which is the product identified in the
(cid:44)→
objective. Its price is $279.49. I will send a message back to
(cid:44)→
user with the answer.
(cid:44)→
```send_msg_to_user("$279.49")```
"
38