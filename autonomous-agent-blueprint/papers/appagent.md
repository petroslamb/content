<!-- AGENT BLUEPRINT METADATA START -->
# AppAgent: Multimodal Agents as Smartphone Users

- Year: 2023
- Primary chapter: Action Systems and Tool Use
- Method category: GUI action
- Practical role: smartphone interaction reference when APIs are unavailable
- Key contribution: Shows how multimodal agents can operate through app interfaces instead of typed APIs.
- Major limitation: Highly interface-specific and not a default action surface for most systems.
- Confidence: Medium
- Canonical link: https://arxiv.org/abs/2312.13771

## Local Note Body

<!-- AGENT BLUEPRINT METADATA END -->

|     |           | AppAgent: | Multimodal  | Agents      |       | as Smartphone |     | Users   |     |     |
| --- | --------- | --------- | ----------- | ----------- | ----- | ------------- | --- | ------- | --- | --- |
|     | ChiZhang∗ |           | ZhaoYang∗   | JiaxuanLiu∗ |       | YuchengHan    |     | XinChen |     |     |
|     |           |           | ZebiaoHuang |             | BinFu | GangYu†       |     |         |     |     |
Tencent
{johnczhang,jayzyang,jiaxuanliu,yuchenghan,shingxchen,zebiaohuang,brianfu,skicyyu}@tencent.com
https://appagent-official.github.io/
|     |     | Chatwith the user  |     |     | Searchmusic video song  |     |     |     | Send an email to      |     |
| --- | --- | ------------------ | --- | --- | ----------------------- | --- | --- | --- | --------------------- | --- |
|     |     | Agent Liu and      |     |     | Wonderful Tonightand    |     |     |     | janedoe@email.com to  |     |
answerhis question leave a praising comment  askher about her new job
3202 ceD 22  ]VC.sc[  2v17731.2132:viXra
Observation:The screenshot shows the Telegram app,  Observation:The screenshot shows a YouTube search  Observation:The screenshot shows a smartphone's
a conversation from "Agent Liu" with a message... result for "Wonderful Tonight"... email application ...
Thought: To complete this task, I should input the text with  Thought: To complete this task, I should insert a  Thought: To complete this task, I should type the
this answer into the input field labeled with the tag ‘7’ praising comment into the text input field labeled ‘2’. content of the email asking Jane Doe about her new job.
Action:text("The Toronto Raptors won the 2019 NBA ... ") Action:text(“This is such a timeless piece...") Action:text(“Dear Jane Doe,\n\nIam writing to ...")
Improvethe quality of  Clock Setan alarm at 12:30 pm  TEMU Searchfor a gaming
this image until it looks  every Friday and Sunday,  headset and addit to my
|     |     | good to you |     |     | and disablethe vibration |     |     |     | shopping cart. |     |
| --- | --- | ----------- | --- | --- | ------------------------ | --- | --- | --- | -------------- | --- |
Observation:The screenshot shows a photo editing app on  Observation:The image shows a screenshot of an  Observation: The screenshot displays a shopping app
|     |     |     |     | alarm application on a smartphone... |     |     | with a variety of headsets listed ... |     |     |     |
| --- | --- | --- | --- | ------------------------------------ | --- | --- | ------------------------------------- | --- | --- | --- |
a smartphone with an image displayed on the screen...
Thought: To complete this task, I should adjust the noise  Thought: To complete this task, I should disable the  Thought: To complete this task, I should add the
reduction levelusing the slider.  vibrationfeature by tapping on the UI element.  selected headset into my shopping cart.
Action:Action: swipe(23, "right", "medium") Action:tap(17) Action:tap(14)
Figure 1: Diverse applications of our multimodal agent framework for smartphone App operation. We
evaluatetheeffectivenessofouragentmodelon50tasksacross10differentApps,highlightingitsadaptabilityand
effectivenessinareal-worldcontext.
|     |     | Abstract |     |     | tionsthroughasimplifiedactionspace,mim- |     |     |     |     |     |
| --- | --- | -------- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- |
ickinghuman-likeinteractionssuchastapping
Recentadvancementsinlargelanguagemodels
|     |     |     |     |     | and | swiping. | This novel | approach | bypasses |     |
| --- | --- | --- | --- | --- | --- | -------- | ---------- | -------- | -------- | --- |
(LLMs)haveledtothecreationofintelligent
theneedforsystemback-endaccess,thereby
| agents | capable | of performing | complex | tasks. |     |     |     |     |     |     |
| ------ | ------- | ------------- | ------- | ------ | --- | --- | --- | --- | --- | --- |
broadeningitsapplicabilityacrossdiverseapps.
ThispaperintroducesanovelLLM-basedmul-
|     |     |     |     |     | Central |     | to our agent’s | functionality | is  | its in- |
| --- | --- | --- | --- | --- | ------- | --- | -------------- | ------------- | --- | ------- |
timodalagentframeworkdesignedtooperate
|            |     |               |               |     | novative |          | learning method. |          | The agent | learns  |
| ---------- | --- | ------------- | ------------- | --- | -------- | -------- | ---------------- | -------- | --------- | ------- |
| smartphone |     | applications. | Our framework | en- |          |          |                  |          |           |         |
|            |     |               |               |     | to       | navigate | and use          | new apps | either    | through |
ablestheagenttooperatesmartphoneapplica-
|     |     |     |     |     | autonomous |     | exploration | or  | by observing | hu- |
| --- | --- | --- | --- | --- | ---------- | --- | ----------- | --- | ------------ | --- |
*Equalcontributions. man demonstrations. This process generates
†CorrespondingAuthor.
1

a knowledge base that the agent refers to for ingapplicationthatbuildsanagenttooperateany
executingcomplextasksacrossdifferentappli- smartphoneapplication(App)inthemobileoper-
cations. Todemonstratethepracticalityofour ating system. Our approach differs significantly
agent,weconductedextensivetestingover50
fromexistingintelligentphoneassistantslikeSiri,
tasksin10differentapplications,includingso-
whichoperatethroughsystemback-endaccessand
cialmedia,email,maps,shopping,andsophis-
|                           |         |             |     |                  |     |         | function   | calls. Instead,      | our agent | interacts | with  |
| ------------------------- | ------- | ----------- | --- | ---------------- | --- | ------- | ---------- | -------------------- | --------- | --------- | ----- |
| ticatedimageeditingtools. |         |             |     | Theresultsaffirm |     |         |            |                      |           |           |       |
|                           |         |             |     |                  |     |         | smartphone | apps in a human-like |           | manner,   | using |
| our                       | agent’s | proficiency | in  | handling         | a   | diverse |            |                      |           |           |       |
arrayofhigh-leveltasks. low-leveloperationssuchastappingandswiping
onthegraphicaluserinterface(GUI).Theproposed
1 Introduction agentoffersmultipleadvantages. Firstly,itelimi-
natestheneedforsystemback-endaccess,making
Theemergenceoflargelanguagemodels(LLMs), ouragentuniversallyapplicableacrossvariousap-
suchasChatGPT(OpenAI,2021)andGPT-4(Ope- plications. Additionally, this approach enhances
| nAI, 2023), | marks | a   | significant |     | milestone | in the |     |     |     |     |     |
| ----------- | ----- | --- | ----------- | --- | --------- | ------ | --- | --- | --- | --- | --- |
securityandprivacy,astheagentdoesnotrequire
fieldofartificialintelligenceandnaturallanguage
|     |     |     |     |     |     |     | deepsystemintegration. | Furthermore,byoperating |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | ----------------------- | --- | --- | --- |
processing. These advanced models represent a ontheGUIlevel, ouragentcanadapttochanges
fundamentalchangeinhowmachinesunderstand
inappinterfacesandupdates,ensuringlong-term
andgeneratehumanlanguage,exhibitingalevelof
applicabilityandflexibility.
sophisticationandversatilitypreviouslyunattain-
However,creatingamultimodalagentcapable
| able. One | of  | the most | exciting |     | developments | in  |     |     |     |     |     |
| --------- | --- | -------- | -------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
ofoperatingdiversesmartphoneappspresentssig-
thisfieldisthecapabilityofLLMstofunctionnot
|     |     |     |     |     |     |     | nificantchallenges. | Existingresearchindicatesthat |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------- | ----------------------------- | --- | --- | --- |
justaslanguageprocessors,butasagentscapable
|                           |     |     |     |                    |     |     | adapting | current models | for embodied |     | tasks ne- |
| ------------------------- | --- | --- | --- | ------------------ | --- | --- | -------- | -------------- | ------------ | --- | --------- |
| ofperformingcomplextasks. |     |     |     | Thisevolutionisev- |     |     |          |                |              |     |           |
cessitatesextensivetrainingdata,andcollectinga
| identin | initiatives | suchasAutoGPT |     |     | (Yangetal., |     |     |     |     |     |     |
| ------- | ----------- | ------------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- |
largedatasetofappdemonstrationsfortrainingis
| 2023a)   | and MetaGPT |           | (Hong        | et al., | 2023), | which   |                  |                            |     |     |     |
| -------- | ----------- | --------- | ------------ | ------- | ------ | ------- | ---------------- | -------------------------- | --- | --- | --- |
|          |             |           |              |         |        |         | aformidabletask. | Moreover,differentappshave |     |     |     |
| showcase | the         | practical | applications |         | of     | LLMs in |                  |                            |     |     |     |
uniqueGUIswithvaryingiconmeaningsandop-
tasksrequiringadvancedcognitivefunctionslike
|                                      |     |     |     |     |             |     | erational | logic, and it remains |     | uncertain | whether |
| ------------------------------------ | --- | --- | --- | --- | ----------- | --- | --------- | --------------------- | --- | --------- | ------- |
| reasoning,planning,andcollaboration. |     |     |     |     | Thesignifi- |     |           |                       |     |           |         |
theseadaptedmodelscaneffectivelygeneralizeto
canceofthesedevelopmentscannotbeoverstated,
unseenapps.
astheyextendtheutilityofLLMsbeyondsimple
languagetasks,revolutionizingvariousaspectsof Inthispaper,weintroduceamultimodalagent
technologyanddailylife. frameworkaimedatoperatinganysmartphoneapp
|     |     |     |     |     |     |     | likehumanusers. | Thelearningofourframework |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | ------------------------- | --- | --- | --- |
However,akeylimitationoftheseLLM-based
involvesanexplorationphasewheretheagentin-
agentshasbeentheirreliancesolelyontext-based
information. This restriction has historically cur- teracts autonomously with apps through a set of
pre-definedactionsandlearnsfromtheiroutcomes.
| tailed their | perception |     | and | interaction |     | with their |     |     |     |     |     |
| ------------ | ---------- | --- | --- | ----------- | --- | ---------- | --- | --- | --- | --- | --- |
Theseinteractionsaredocumented,whichassists
| environment. | Theintroductionofmodelsequipped |     |     |     |     |     |     |     |     |     |     |
| ------------ | ------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
with vision capabilities, such as the latest itera- theagentinnavigatingandoperatingtheapps. This
learningprocesscanbeacceleratedbyobserving
| tion of     | GPT-4, | marks   | a pivotal  | breakthrough. |               | By  |             |                 |     |           |          |
| ----------- | ------ | ------- | ---------- | ------------- | ------------- | --- | ----------- | --------------- | --- | --------- | -------- |
|             |        |         |            |               |               |     | a few human | demonstrations. |     | Following | this ex- |
| integrating | the    | ability | to process |               | and interpret | vi- |             |                 |     |           |          |
ploratoryphase,theagentcanoperatetheappby
sualinformation,thesemodelscannowunderstand
aspects of their surroundings that are difficult or consultingtheconstructeddocumentbasedonits
currentstate,eliminatingtheneedtoadaptthepa-
| impossibletoconveythroughtextalone. |     |     |     |     |     | Thisex- |     |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
rametersoftheLLMsorcollectextensivetraining
| tended                                         | capability | enables | LLMs |     | to interpret | con- |                 |     |     |     |     |
| ---------------------------------------------- | ---------- | ------- | ---- | --- | ------------ | ---- | --------------- | --- | --- | --- | --- |
| text,recognizepatterns,andrespondtovisualcues, |            |         |      |     |              |      | dataforeachapp. |     |     |     |     |
thusprovidingamoreholisticandinteractiveexpe- Tovalidateitseffectiveness,wetestedouragent
riencewiththeworld. on50tasksacross10differentapps,rangingfrom
Inourwork,wefocusonbuildingamultimodal socialmediaandmessagingtoemail,maps,shop-
agent leveraging the vision capabilities of multi- ping,andevencompleximageeditingapps. Both
modal large language models to undertake tasks quantitativeresultsanduserstudiesunderscorethe
previously unachievable by text-only agents. In advantages of our design, particularly its adapt-
particular,weexploreaninterestingbutchalleng- ability,user-friendliness,andefficientlearningand
2

operatingcapabilitiesacrossawiderangeofappli- 2023b,a),ChartLlama(Hanetal.,2023),andSta-
cations. Thisunderlinesthepotentialofouragent bleLLaVA(Lietal.,2023),alsodemonstratevision
as a versatile and effective tool in the realm of understandingcapabilitiesakintothoseofGPT-4V.
smartphoneappoperation. Nevertheless,aperformancegappersistsbetween
Insummary,thispapermakesthefollowingcon- theseopen-sourcemodelsandGPT-4V,suggesting
| tributions:      |              |            |        | potentialareasforfurtherdevelopment. |     |     |     |     |
| ---------------- | ------------ | ---------- | ------ | ------------------------------------ | --- | --- | --- | --- |
| • We open-source | a multimodal | agent      | frame- |                                      |     |     |     |     |
|                  |              |            |        | 2.2 LLMsasagents                     |     |     |     |     |
| work, focusing   | on operating | smartphone | ap-    |                                      |     |     |     |     |
plicationswithourdevelopedactionspace. The use of LLMs as agents for executing com-
|     |     |     |     | plex tasks | has gained | increasing | attention. | Ini- |
| --- | --- | --- | --- | ---------- | ---------- | ---------- | ---------- | ---- |
• Weproposeaninnovativeexplorationstrategy,
|     |     |     |     | tiatives | like AutoGPT | (Yang | et al., | 2023a), Hug- |
| --- | --- | --- | --- | -------- | ------------ | ----- | ------- | ------------ |
whichenablestheagenttolearntousenovel
gingGPT(Shenetal.,2023),andMetaGPT(Hong
apps.
etal.,2023)illustratethistrend,andmanyprojects
• Throughextensiveexperimentsacrossmulti- demonstrate impressive capabilities, moving be-
ple apps, we validate the advantages of our yond basic language tasks to engaging in activi-
framework,demonstratingitspotentialinthe ties requiring higher cognitive functions, such as
realm of AI-assisted smartphone app opera- software development (Qian et al., 2023; Chen
| tion. |     |     |     | etal.,2021)andgaming(FAIRetal.,2022;Park |                  |                 |     |               |
| ----- | --- | --- | --- | ---------------------------------------- | ---------------- | --------------- | --- | ------------- |
|       |     |     |     | et al.,                                  | 2023; Xu et      | al., 2023).     | In  | this context, |
|       |     |     |     | Yao et                                   | al. (Yao et al., | 2023) introduce |     | an innova-    |
2 RelatedWork
tiveapproachthatsynergizesreasoningandacting
2.1 Largelanguagemodels
|     |     |     |     | in LLMs, | significantly   | enhancing     | their | decision- |
| --- | --- | --- | --- | -------- | --------------- | ------------- | ----- | --------- |
|     |     |     |     | making   | and interactive | capabilities. |       | LLM-based |
ThedevelopmentofChatGPT(OpenAI,2021)and
GPT-4 (OpenAI, 2023) represents a crucial ad- agents are designed to utilize the advanced lan-
vancementinnaturallanguageprocessing. Unlike guage and reasoning skills of LLMs to interact
withandmanipulatetheirenvironment(Liuetal.,
earlierlargelanguagemodels(LLMs),thesenew
models(Touvronetal.,2023a,b;Zengetal.,2022; 2023c;Guretal.,2023;Xieetal.,2023). Thisin-
Taorietal.,2023;Zhengetal.,2023)enablemulti- cludesperformingtasksthatrequireunderstanding
context,makingdecisions,andlearningfrominter-
roundconversationsandhavetheimpressiveability
|                              |     |                  |     | actions(Xietal.,2023;HuandShu,2023). |     |     |     | Such |
| ---------------------------- | --- | ---------------- | --- | ------------------------------------ | --- | --- | --- | ---- |
| tofollowcomplexinstructions. |     | Theintegrationof |     |                                      |     |     |     |      |
visioncapabilitiesinGPT-4V(Yangetal.,2023b) agentsarepivotalinapplicationswherehuman-like
isafurthermilestone,enablingthelanguagemodel cognitiveabilitiesareessential.
toprocessandinterpretvisualdata. Thisaddition The emergence of multimodal LLM
has broadened the scope of potential AI applica- agents (Wang et al., 2023; Furuta et al., 2023;
tions, allowing GPT-4 to undertake diverse tasks Brohan et al., 2022, 2023; Reed et al., 2022),
such as problem-solving, logical reasoning, tool capableofprocessingvariousinputsincludingtext,
usage,APIcalls,andcoding. Recentstudies(Yang images, audio, and video, has further broadened
et al., 2023c; Yan et al., 2023) have shown that the scope of LLM applications. This versatility
GPT-4V can understand various types of images, is particularly beneficial for LLM-based agents,
including simple user interfaces (UIs) in popular enabling them to interact more effectively with
smartphoneapps. However,challengesarisewhen their environment and complete more complex
the apps are new and their UIs are less typical, tasks, be it completing household tasks in a
which highlights a major problem that our work physical world (Ahn et al., 2022), generating 3D
aimstoaddress. Amongopen-sourceeffortsfrom assetsviaproceduraltooluse(Sunetal.,2023),or
theindustryandresearchcommunity,theLLaMA masteringover600tasksacrossdifferentdomains
series(Touvronetal.,2023a,b)arethemostpop- atthesametime(Reedetal.,2022). Ourresearch
ular equivalents and have been fine-tuned to ac- contributes to this area by focusing on an agent
quireconversationalabilities,employingadecoder- designedtooperatesmartphoneapplications. This
onlyarchitecturesimilartoChatGPT(Taorietal., agent’s ability to interpret screenshots from the
2023;Zhengetal.,2023). BuildinguponLLaMA, operating system demonstrates its flexibility and
manymultimodalLLMs,suchasLLaVA(Liuetal., adaptability, making it a valuable tool in a wide
3

| ExplorationPhase |     |                                   |                      |                                     |                           |     | DeploymentPhase:“beautifythisphotoforme…” |     |     |     |     |     |
| ---------------- | --- | --------------------------------- | -------------------- | ----------------------------------- | ------------------------- | --- | ----------------------------------------- | --- | --- | --- | --- | --- |
|                  | …   |                                   |                      |                                     |                           | … … |                                           |     |     |     |     | …   |
|                  |     |                                   | Tap                  |                                     | Swipe                     |     |                                           |     |     |     |     |     |
|                  |     |                                   | 👀                    |                                     | 👀                         |     |                                           |     |     |     |     |     |
|                  | 🤔   | “Tappingthis UI elementopens      |                      | “Swipingthis UI element allows the  |                           |     |                                           |     |     |     |     |     |
|                  |     | the color settings to adjust the  |                      |                                     | user to adjust the color  |     |                                           |     |     |     |     |     |
|                  |     |                                   | color of the image.” | temperatureof the image.”           |                           |     |                                           |     |     |     |     |     |
DocforApp
Observe,Think,Act,andSummarize
Figure2: Overviewofourmultimodalagentframeworkdesignedtooperatesmartphoneapplications. The
figureillustratesthetwo-phaseapproachofourframework. Intheexplorationphase,theagentinteractswitha
smartphone application and learns from their outcomes to create a comprehensive reference document. In the
deploymentphase,theagentutilizestheinformationcompiledinthisdocumenttooperateandnavigatetheapps
effectively.
rangeofapplications. Thishelpstheagenttointeractaccuratelywithout
|          |     |     |     |     |     | needing         | to specify |                  | exact positions |     | on the         | screen |
| -------- | --- | --- | --- | --- | --- | --------------- | ---------- | ---------------- | --------------- | --- | -------------- | ------ |
| 3 Method |     |     |     |     |     | and enhancesthe |            | agent’sprecision |                 |     | in controlling |        |
thephone.
Thissectiondetailsthemethodologybehindourin-
|                                   |     |     |     |            |     | Action | Space: | Our | agent’s | action | space | mir- |
| --------------------------------- | --- | --- | --- | ---------- | --- | ------ | ------ | --- | ------- | ------ | ----- | ---- |
| novativemultimodalagentframework. |     |     |     | Thisframe- |     |        |        |     |         |        |       |      |
rorscommonhumaninteractionswithsmartphones:
workenablesanagenttointeractwithsmartphone
|     |     |     |     |     |     | tapsandswipes. |     | Wedesignedfourbasicfunctions: |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------- | --- | ----------------------------- | --- | --- | --- | --- |
applicationsinamannerakintohumanbehavior.
Wefirstdescribetheexperimentalenvironmentand • Tap(element : int) : This function simu-
|     |     |     |     |     |     | lates | a tap | on  | the UI | element | numbered | on  |
| --- | --- | --- | --- | --- | --- | ----- | ----- | --- | ------ | ------- | -------- | --- |
actionspace,whicharefoundationalelementsof
oursystem. Next,wediscusstheexplorationphase, the screen. For example, tap(5) would tap
where the agent learns app functionalities either theelementlabeled‘5’.
throughautonomousinteractionsorbyobserving
|                      |     |     |                         |     |     | • Long_press(element |     |     |     | : int) | : This | func- |
| -------------------- | --- | --- | ----------------------- | --- | --- | -------------------- | --- | --- | --- | ------ | ------ | ----- |
| humandemonstrations. |     |     | Finally,weoutlinethede- |     |     |                      |     |     |     |        |        |       |
tionemulatesalongpress(for1second)ona
ploymentphase,explaininghowtheagentapplies
UIelement.
itsacquiredknowledgetoexecutehigh-leveltasks.
|                               |     |     |     |     |     | • Swipe | (       | element                   | : int, | direction |     | : str, |
| ----------------------------- | --- | --- | --- | --- | --- | ------- | ------- | ------------------------- | ------ | --------- | --- | ------ |
| 3.1 EnvironmentandActionSpace |     |     |     |     |     |         | : str): |                           |        |           |     |        |
|                               |     |     |     |     |     | dist    |         | Itallowstheagenttoswipeon |        |           |     |        |
anelementinaspecifieddirection(up,down,
| Experimental |     | Environment: |     | Our experimental |     |     |     |     |     |     |     |     |
| ------------ | --- | ------------ | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
environmentisbuiltonacommand-lineinterface left,right)anddistance(short,medium,long).
(CLI), allowing the agent to interact with smart- For instance, swipe(21,“up”,“medium”)
wouldswipeuponelement‘21’foramedium
| phoneapps.         | WechosetheAndroidoperatingsys- |                            |            |                |         |             |          |        |                          |               |       |        |
| ------------------ | ------------------------------ | -------------------------- | ---------- | -------------- | ------- | ----------- | -------- | ------ | ------------------------ | ------------- | ----- | ------ |
| tem for            | our experiments.               |                            | The        | agent receives | two     | distance.   |          |        |                          |               |       |        |
| key inputs:        | a                              | real-time                  | screenshot | showing        | the     |             |          |        |                          |               |       |        |
|                    |                                |                            |            |                |         | • Text(text |          | : str) | :Tobypassinefficientvir- |               |       |        |
| app’s interface    |                                | and an                     | XML        | file detailing | the in- |             |          |        |                          |               |       |        |
|                    |                                |                            |            |                |         | tual        | keyboard |        | typing,                  | this function |       | inputs |
| teractiveelements. |                                | Toenhancetheagent’sability |            |                |         |             |          |        |                          |               |       |        |
|                    |                                |                            |            |                |         | text        | directly | into   | an                       | input         | field | when a |
toidentifyandinteractwiththeseelementsseam-
|     |     |     |     |     |     | virtual | keyboard |     | is  | visible. | For | exam- |
| --- | --- | --- | --- | --- | --- | ------- | -------- | --- | --- | -------- | --- | ----- |
lessly,weassigneachelementauniqueidentifier.
ple,text(“Hello,world!”)inputsthestring
| These identifiers |     | are | derived | either from | the re- |     |     |     |     |     |     |     |
| ----------------- | --- | --- | ------- | ----------- | ------- | --- | --- | --- | --- | --- | --- | --- |
“Hello,world!".
sourceIDintheXMLfile(ifprovided)orarecon-
structed by combining the class name, size, and • Back() : A system-level function that helps
content of the element. These elements are over- theagentreturntothepreviousUIpage,espe-
laidassemi-transparentnumbersonthescreenshot. ciallyusefulforexitingirrelevantpages.
4

• Exit() :Aspecializedfunctionisemployed Thisstrategynarrowsdowntheexplorationspace
toconcludeprocesses,typicallyinvokedupon andpreventstheagentfromengagingwithirrele-
successfultaskcompletion. vantapppages,makingitamorestreamlinedand
efficientapproachcomparedtoautonomousinter-
| These | predefined | actions |     | are designed | to  | sim- | actions. |     |     |     |     |     |     |
| ----- | ---------- | ------- | --- | ------------ | --- | ---- | -------- | --- | --- | --- | --- | --- | --- |
plifytheagent’sinteractions,particularlybyelim-
inating the need for precise screen coordinates, 3.3 DeploymentPhase
| which | can pose | challenges |     | for language | models |     |     |     |     |     |     |     |     |
| ----- | -------- | ---------- | --- | ------------ | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
Followingtheexplorationphase,theagentiswell-
inaccuratelypredicting.
|     |     |     |     |     |     |     | equipped | to execute  | complex |       | tasks   | based | on its  |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | ------- | ----- | ------- | ----- | ------- |
|     |     |     |     |     |     |     | accrued  | experience. | The     | agent | adheres | to    | a step- |
3.2 ExplorationPhase
by-stepapproachwhengivenatask,witheachstep
| Exploringbyautonomousinteractions. |     |     |     |     | TheEx- |     |     |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
encompassingaccesstoascreenshotofthecurrent
| plorationPhaseiscentraltoourframework. |     |     |     |     |     | Here, |     |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
UIandadynamicallygenerateddocumentdetail-
theagentlearnsaboutthefunctionalitiesandfea-
|                                            |           |     |          |        |     |        | ing the functions |             | of UI        | elements | and    | the actions’ |      |
| ------------------------------------------ | --------- | --- | -------- | ------ | --- | ------ | ----------------- | ----------- | ------------ | -------- | ------ | ------------ | ---- |
| turesofsmartphoneappsthroughtrialanderror. |           |     |          |        |     | In     |                   |             |              |          |        |              |      |
|                                            |           |     |          |        |     |        | effects on        | the current | UI           | page.    | The    | prompts      | also |
| this phase,                                | the agent | is  | assigned | a task | and | starts |                   |             |              |          |        |              |      |
|                                            |           |     |          |        |     |        | provide detailed  |             | explanations |          | of all | available    | ac-  |
interactingautonomouslywiththeUIelements. It tions. In each step, the agent is first tasked with
| uses different | actions    |           | and observes |               | the resulting |     |           |                  |     |     |             |     |      |
| -------------- | ---------- | --------- | ------------ | ------------- | ------------- | --- | --------- | ---------------- | --- | --- | ----------- | --- | ---- |
|                |            |           |              |               |               |     | providing | its observations |     | of  | the current | UI, | fol- |
| changes        | in the app | interface |              | to understand |               | how |           |                  |     |     |             |     |      |
lowedbyarticulatingitsthoughtprocessconcern-
| it works. | The agent, | driven    |     | by a large    | language |       |                                   |     |     |     |     |               |     |
| --------- | ---------- | --------- | --- | ------------- | -------- | ----- | --------------------------------- | --- | --- | --- | --- | ------------- | --- |
|           |            |           |     |               |          |       | ingthetaskandcurrentobservations. |     |     |     |     | Subsequently, |     |
| model,    | attempts   | to figure | out | the functions |          | of UI |                                   |     |     |     |     |               |     |
theagentproceedstoexecuteactionsbyinvoking
elementsandtheeffectsofspecificactionsbyan-
|         |             |        |     |       |      |         | available | functions. | After | each | action, | the | agent |
| ------- | ----------- | ------ | --- | ----- | ---- | ------- | --------- | ---------- | ----- | ---- | ------- | --- | ----- |
| alyzing | screenshots | before | and | after | each | action. |           |            |       |      |         |     |       |
summarizestheinteractionhistoryandtheactions
Thisinformationiscompiledintoadocumentthat takenduringthecurrentstep. Thisinformationis
recordstheeffectsofactionsappliedtodifferentel-
incorporatedintothenextprompt,whichprovides
ements. WhenaUIelementisacteduponmultiple
|        |           |             |     |              |     |       | theagentwithaformofmemory. |     |     |     | Thismeticulous |     |     |
| ------ | --------- | ----------- | --- | ------------ | --- | ----- | -------------------------- | --- | --- | --- | -------------- | --- | --- |
| times, | the agent | will update |     | the document |     | based |                            |     |     |     |                |     |     |
approachenhancesthereliabilityandinterpretabil-
onpastdocumentsandcurrentobservationstoim-
ityoftheagent’sactions,therebyfacilitatingmore
| provequality. | Tomakeexplorationmoreefficient, |     |     |     |     |     |                          |     |     |                    |     |     |     |
| ------------- | ------------------------------- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | ------------------ | --- | --- | --- |
|               |                                 |     |     |     |     |     | informeddecision-making. |     |     | Thedeploymentphase |     |     |     |
theagentstopsfurtherexploringUIelementsifthe
stopswhentheagentdeterminesthatthetaskhas
currentUIpageseemsunrelatedtothemaintasks beenaccomplished,atwhichpointitcanexitthe
| oftheapp,likeadvertisementpages. |     |     |     |     | Insuchcases, |     |     |     |     |     |     |     |     |
| -------------------------------- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
processbytakingtheExit()action.
| it uses | the Android     | system’s |          | Back()      | function | to   |               |     |     |     |     |     |     |
| ------- | --------------- | -------- | -------- | ----------- | -------- | ---- | ------------- | --- | --- | --- | --- | --- | --- |
| return  | to the previous |          | UI page. | Compared    |          | with | 4 Experiments |     |     |     |     |     |     |
| random  | exploration,    | such     | as       | Depth-First | Search   |      |               |     |     |     |     |     |     |
andBreadth-FirstSearch,thisgoal-orientedexplo- In this section, we will present our evaluation of
themultimodalagentframeworkthroughacombi-
rationapproachensuresthattheagentfocuseson
elementscrucialfortheeffectiveoperationofthe nationofquantitativeandqualitativeexperiments.
app. The agent also utilizes the LLM’s existing Our primary goal is to assess the agent’s perfor-
knowledgeaboutuserinterfacestoimproveexplo- mance and its ability to operate a diverse set of
smartphoneapplicationseffectively.
| rationefficiency. |     | Theexplorationstopswhenthe |     |     |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
agentcompletestheassignedtask.
|                           |     |     |     |     |               |     | 4.1 ExperimentalSetup |     |     |     |     |     |     |
| ------------------------- | --- | --- | --- | --- | ------------- | --- | --------------------- | --- | --- | --- | --- | --- | --- |
| Exploringbywatchingdemos. |     |     |     |     | Analternative |     |                       |     |     |     |     |     |     |
and often more effective exploration method in- Tocomprehensivelyevaluateourmethod,wecon-
volvestheagentobservinghumandemonstrations. structabenchmarkthatincludes10popularappli-
These demonstrations provide the agent with ex- cations,eachservingvariouspurposes. Theseap-
amples of efficient app usage, especially for un- plicationsincludeGoogleMaps,Twitter,Telegram,
derstandingcomplexfunctionalitiesthatmightbe YouTube,Spotify,Yelp,Gmail,TEMU,Clock,and
challengingtodiscoverthroughautonomousinter- Lightroom. Wehaveintentionallychosenthisdi-
actions. In this method, a human user operates verse set of apps to test the agent’s adaptability
theappswhiletheagentobserves,recordingonly acrossvariousfunctionsandinterfaces. Inparticu-
theelementsandactionsemployedbythehuman. lar,togainamorecomprehensiveinsightintothe
5

Google Maps: navigate to Tencent Shanghai Branch
|     | Observation |     |     |     | Observation |     |     |     |     | Observation |     |
| --- | ----------- | --- | --- | --- | ----------- | --- | --- | --- | --- | ----------- | --- |
The search field is focused and a keyboard is  A keyboardand a search resultfor "Tencent Shanghai  The screenshot shows a map application with the
present on the lower half of the screen. UI  Branch" with address detailsand a distance measurement  location "Tencent Shanghai Branch" pinpointed
element labeled '6' appears to be the search input  field where text can be input to find locations,  are displayed. with a red marker. There are two buttons at the  bottom of the screen, one labeled "Directions" and
addresses, or points of interest. the other labeled "Start", with numeric tags 1 and
3respectively.
|     | Thought |     |     |     | Thought |     |     |     |     | Thought |     |
| --- | ------- | --- | --- | --- | ------- | --- | --- | --- | --- | ------- | --- |
To complete the given task, I should enter the  To complete the given task, I should confirm the search  To complete the given task, which is to
text"Tencent Shanghai Branch" in the search  for "Tencent Shanghai Branch". In this screenshot, the  navigate to Tencent Shanghai Branch, I should
field to proceed with the search for the  search confirm buttonis represented by the blue button tap the "Directions" buttonto initiate the
destination. with the text “\u641c\u7d22” (“Search” in Chinese) on it. route finding process.
|     | Action                          |     |     |     | Action |        |     |     |     | Action |     |
| --- | ------------------------------- | --- | --- | --- | ------ | ------ | --- | --- | --- | ------ | --- |
|     | text("Tencent Shanghai Branch") |     |     |     |        | tap(1) |     |     |     | tap(2) |     |
Gmail: send an email to janedoe@email.comto ask her about her new job
Observation
Observation Observation T h e   e m a i l   b o d y   i s   t y p e d   w i t h   a   m e s s a g e   a s k i n g
T h e   r e c i p i e n t 's   e m a i l   a d d r e s s i s   a l r e a d y   f i l l e d   T h e   re c i p i e n t 's   e m a i l   a d d r e s s   i s  a l r e a d y   f i l l e d  i n   a s   J a n e   D o e   a b o u t   h e r   r e c e n t   j o b   a n d   e x p r e s s i n g
i n ,   a n d   t h e   s u b j e ct   l i n e  r e a d s   " I n q u i r y   A b o u t   j a n e d o e @ e m a i l . c o m a n d  t h e   s u b j e c t   l i n e   i s   " I n q u i r y   e a g e r n e s s   t o   h e a r   f r o m   h e r .   T h e r e   i s   a   s e n d
Y o u r   N e w   P o s i t i o n . "   T h e   b o d y   o f   t h e  e m a i l   i s A b o u t   Y o u r   N e w   P o s i t i o n . "   T h e   c u r s o r   i s   b l i n k i n g   i n   b u t t o n   l a b e l e d   w i t h   t h e   n u m e r i c   t a g   ' 3 ’ .
|     | n o t   v i s i b                           | l e ,  a n d   t h e r e ' s   a   U I   e | l e m e n t   l a b e l e d   |     | t                                                                     | h e   m a i n   b o d y   a r e a o | f   t h e   e m a i l ,   i n d i c a t i n | g   t h a t   i t   i s   |     |     |     |
| --- | ------------------------------------------- | ------------------------------------------ | ----------------------------- | --- | --------------------------------------------------------------------- | ----------------------------------- | ------------------------------------------- | ------------------------- | --- | --- | --- |
|     | '11'which is used to collapse the keyboard. |                                            |                               |     | ready to receive text input. The on-screen keyboard is  also visible. |                                     |                                             |                           |     |     |     |
Thought
|     | Thought |     |     |     | Thought |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
T o   c o m p l e t e   th e  t a s k ,   t h e   n e x t  s t e p   s h o u l d   b e   T o   c o m p l e t e   th e   g iv e n   t a s k ,  th e   n e x t  s t e p   I  s h ou l d   d o  i s   T o  c o m p l e t e   t h e   g iv e n   t a sk ,  th e   n ex t  s t ep   I
t o   c o l l a p s e   t h e   k e y b o a r d s o   t h a t   I   c a n   a c c e s s   t o   t y p e   t h e   c o n t e n t o f   t h e  e m a i l  a s k i n g   J a n e  D o e   a b o u t   s h o u l d  t a k e  i s   t o   se n d   t h e  e m a i l  b y  t a p p i n g
|     | t h e   b o d y |   o f   t h e   e m a il   t o   t y p e   | t h e   m e s s a g e   t o   |     | h   | e r   n e w  j o b . |     |     |     | th e   s e n d   b u t t | o n . |
| --- | --------------- | ------------------------------------------ | ----------------------------- | --- | --- | -------------------- | --- | --- | --- | ------------------------ | ----- |
Jane Doe asking about her new job.
Action
|     | Action  |     |     |     | Action                                          |     |     |     |     |        |     |
| --- | ------- | --- | --- | --- | ----------------------------------------------- | --- | --- | --- | --- | ------ | --- |
|     | tap(11) |     |     |     | text("Dear Jane Doe,\n\nIam writing to inquire  |     |     |     |     | tap(3) |     |
about your new position that you recently started…")
Lightroom: improve the quality of this image until it looks good to you
|     | Observation |     |     |     | Observation |     |     |     |     | Observation                 |                                                                  |
| --- | ----------- | --- | --- | --- | ----------- | --- | --- | --- | --- | --------------------------- | ---------------------------------------------------------------- |
|     |             |     |     |     |             |     |     |     |     | T h e   e x p o s u r e   a | n d   c o n t r a s t   s l i d e r s   a r e   v is i b l e ,   |
T h e   s c r e e n s h o t   s h o w s   a   p h o t o   e d i t i n g   a p p l i c a t i o n   T h e   e x p o s u r e   l e v e l   h a s   b e e n   i n c r e a s e d ,   a s   i n d i c a t e d   b y   th e   w i t h   t h e   e x p o s u r e   i n c r e a s e d   t o   + 2 . 2 0 a n d   t h e
i n t e r f a c e   w i t h   v a r i o u s   a d j u s t m e n t   s e t t i n g s   f o r   s l i d e r   t a g g e d   w i t h  n u m b e r   2 0   b e i n g   t o   t h e   r i g h t .   T h e   c o n t r a s t   i n c r e a s e d   t o   + 2 4 .   T h e   h i g h l ig h t s   a n d
e x p o s u r e ,   c o n t r a s t ,   h i g h l i g h t s ,   a n d   s h a d o w s .   c o n t r a s t ,   h i g h l i g h t s ,   a n d   s h a d o w s a r e   y e t   t o   b e   a d j u s t e d ,   s h a d o w s s l i d e r s   a r e   a t   0 ,  i n d i c a t i n g   n o
T a n h d e s   2 e 3   a d r e j u s p s t e m c t e i v n e ts l   y h .   a T v h e e   n   s u e m t t i e n r g i s c     a t r a e g   s c   u 2 r 0 r e ,   n 2 t 1 l y ,     2 a 2 t  ,   w o t i h t h e r   t   a h d e j i u r   s s t l m i d e e n r t s     o a p t t   t i o h n e s   n   a e v u a t i r l a a b l   l p e o ,  s s i u t c i o h n   a . s   T   c h o e l r o e r     a a r n e d   a   d ls e o t a   i l ,  a d j u s t m e n t   h a s   b e e n   m a d e   t o   t h e m .
|     | their default values, and the image appears  |     |     |     | which could further improve the image quality if needed. |     |     |     |     |     |     |
| --- | -------------------------------------------- | --- | --- | --- | -------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
underexposed, needing improvement in lighting.
Thought
|     | Thought |     |     |     | Thought |     |     |     |     |     |     |
| --- | ------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
T o   i m p r o v e   t h e   i m a g e   q u a l i t y   a n d   c o r r e c t   t h e   T h e   n e x t   s t e p   t o   i m p r o v e   t h e   q u a l i t y   o f   t h e   i m a g e   c o u l d  b e   S i n c e   I   h a v e   p r e v i o u s l y   i n c r e a s e d   t h e   e x p o s u r e
u n d e r e x p o s u r e ,   I   n e e d   t o   i n c r e a s e   t h e   t o   a d j u s t   t h e   c o n t r a s t ,   a s   i n c r e a s i n g   c o n t r a s t   c a n   o f t e n   a c n o d u   l a d d   b j u e s   t t o e   d a   d t h j e u   s c t o   t n h t r e a   h s t i   g s h l i l g i h g t h l y t s ,    t o h r e   s   n h e a x d t   o s w t e s p     t o
e x p o s u r e .   T h e   s l i d e r   f o r   t h e   e x p o s u r e   s e t t i n g   m a k e   a n   i m a g e   a p p e a r  m o r e   v i v i d a n d   c a n   c o m p l e m e n t   f u r t h e r   i m p r o v e   t h e   i m a g e   q u a l i t y .   A d j u s t i n g
i s   l a b e l e d   w i t h   n u m e r i c   t a g   2 0 ,   w h i c h   I   c a n   t h e   i n c r e a s e d   e x p o s u r e .   B a s e d   o n   t h e   d o c u m e n t a t i o n ,   t h e   h i g h l i g h t s   m i g h t   h e l p   i n   b r i n g i n g   o u t   m o r e
i n t e r a c t   w i t h   t o   a d j u s t   t h e   e x p o s u r e   l e v e l .   I   w i l l   i n t e r a c t i n g   w i t h   U I   e l e m e n t   l a b e l e d   2 1   w i l l   a d j u s t   t h e   d e t a i l   i n   t h e   b r i g h t e r   p a r t s   o f   t h e   i m a g e
s e w x p i p o e s   u r r i g e . h t   o n   t h i s   s l i d e r   t o   i n c r e a s e   t h e   c o n t r a s t   l e v e l   o f   t h e   i m a g e . w i t h o u t   a f f e c t i n g   t h e   o v e r a l l   e x p o s u r e   t o o   m u c h .
Action
|     | Action                       |     |     |     | Action                      |     |     |     |     | tap(22) |     |
| --- | ---------------------------- | --- | --- | --- | --------------------------- | --- | --- | --- | --- | ------- | --- |
|     | swipe(20, "right", "medium") |     |     |     | swipe(21, "right", "short") |     |     |     |     |         |     |
Figure3: QualitativeTaskEvaluationAcrossThreeApps. Thisfigurepresentsqualitativeresultsforthree
distincttasksconductedonGoogleMaps,Gmail,andLightroom. ItshowcasesAppAgent’sabilitytoaccurately
perceive,reason,andexecutetasks,demonstratingitscompetenceinvariousapplicationcontexts. Duetospace
constraints,somelesscriticaldetailshavebeenomittedfromthedescription.
visioncapabilitiesofouragent,weconductedan 4.2 DesignandAnalysis
| in-depth                  | case study     | using | Adobe                 | Lightroom,   | an  |            |         |                                  |        |            |              |
| ------------------------- | -------------- | ----- | --------------------- | ------------ | --- | ---------- | ------- | -------------------------------- | ------ | ---------- | ------------ |
|                           |                |       |                       |              |     | Baselines. |         | Tocomprehensivelyevaluateourmul- |        |            |              |
| image-editingapplication. |                |       | Thisspecificcasestudy |              |     |            |         |                                  |        |            |              |
|                           |                |       |                       |              |     | timodal    | agent   | framework,                       | we     | considered | various      |
| allowed                   | us to evaluate | the   | agent’s               | proficiency  | in  |            |         |                                  |        |            |              |
|                           |                |       |                       |              |     | design     | choices | and their                        | impact | on         | performance. |
| handling                  | visual tasks   | and   | its ability           | to interpret |     |            |         |                                  |        |            |              |
Weconductedexperimentsusingdifferentconfigu-
| and manipulate | images | within | the | app. | For the |     |     |     |     |     |     |
| -------------- | ------ | ------ | --- | ---- | ------- | --- | --- | --- | --- | --- | --- |
rationstoprovidevaluableinsightsintotheagent’s
explorationphase,wecappedthemaximumnum-
|              |               |     |          |            |     | behavior. |     | WestartedwithGPT-4withoutanyref- |     |     |     |
| ------------ | ------------- | --- | -------- | ---------- | --- | --------- | --- | -------------------------------- | --- | --- | --- |
| ber of steps | at 40. During |     | testing, | we limited | the |           |     |                                  |     |     |     |
erencedocumentsduringtestingandexaminedits
| maximumnumberofstepsto10. |     |     | Fortheseexperi- |     |     |             |     |           |     |            |         |
| ------------------------- | --- | --- | --------------- | --- | --- | ----------- | --- | --------- | --- | ---------- | ------- |
|                           |     |     |                 |     |     | performance |     | both with | the | raw action | API and |
ments,weutilizedthestate-of-the-artmultimodal
|                           |     |     |                 |     |     | our | simplified | action | space. | Next, | we explored |
| ------------------------- | --- | --- | --------------- | --- | --- | --- | ---------- | ------ | ------ | ----- | ----------- |
| largelanguagemodel,GPT-4. |     |     | GPT-4isequipped |     |     |     |            |        |        |       |             |
differentwaystogenerateguidingdocumentsfor
toprocessinterleavedimage-and-textinputseffec-
|     |     |     |     |     |     | the | agent. | These included | documents |     | generated |
| --- | --- | --- | --- | --- | --- | --- | ------ | -------------- | --------- | --- | --------- |
tively. Thisuniquecapabilityenablesouragentto
throughautonomousexploration,watchinghuman
interpretandinteractwithbothvisualandtextual
|     |     |     |     |     |     | demonstrations, |     | and the | manually |     | crafted docu- |
| --- | --- | --- | --- | --- | --- | --------------- | --- | ------- | -------- | --- | ------------- |
informationseamlesslywithintheapplications.
mentasanoraclebenchmark.
Toeffectivelycomparetheperformanceofdif-
6

| Method |     | Document |     | ActionSpace | SR↑ Reward↑ | Avg. Steps |
| ------ | --- | -------- | --- | ----------- | ----------- | ---------- |
|        |     | None     |     | Raw         | 2.2% 0.6    | 4.0        |
GPT4(Baseline)
|          |     | None              |     | Ours | 48.9% 3.5 | 6.9 |
| -------- | --- | ----------------- | --- | ---- | --------- | --- |
|          |     | Auto. Exploration |     | Ours | 73.3% 5.1 | 4.4 |
| AppAgent |     | WatchingDemos     |     | Ours | 84.4% 4.7 | 5.1 |
|          |     | ManuallyCrafted   |     | Ours | 95.6% 5.5 | 5.5 |
Table1: EvaluatingDesignChoicesinAppAgentPerformance. Thistablecontrastsdifferentdesignelements
withinAppAgent. Keyfindingsinclude: ourcustom-developedactionspacesurpassestherawactionspaceineffi-
ciency;theexplorationphase,incorporatingbothautonomousinteractionandobservationofhumandemonstrations,
significantlyenhancesagentperformance;andtheauto-generateddocumentationyieldsoutcomesonparwiththose
derivedfrommanuallycrafteddocuments.
|     | Method         | Document      |     | ActionSpace | Avg. Rank↓ | Num. Tools |
| --- | -------------- | ------------- | --- | ----------- | ---------- | ---------- |
|     | GPT4(Baseline) | None          |     | Ours        | 2.30       | 2.4        |
|     |                | WatchingDemos |     | Ours        | 1.95       | 5.8        |
AppAgent
|     |     | ManuallyCrafted |     | Ours | 1.75 | 4.0 |
| --- | --- | --------------- | --- | ---- | ---- | --- |
Table2: CasestudyonimageeditingtaskswithLightroomApp. Weconductauserstudytoranktheimage
editingresultsofdifferentmethods. OuragentsproducebetterresultsthantheGPT-4baseline.
ferentmethods,weemployedthreekeymetrics: inghumandemonstrationsprovedtobehighlyef-
Successful Rate (SR): This metric measures the fective. Theirresultsconsistentlyoutperformedthe
averagerateatwhichtheagentsuccessfullycom- GPT-4baselineandarecomparabletotheresults
pletes tasks within an app. If the agent fails to ofhuman-writtendocuments,whichhighlightsthe
finishthetaskin10steps,itisconsideredafailure. efficacyofourdesigninenhancingtheagent’sper-
Reward: Toprovideamorefine-grainedmeasure- formanceacrossadiversesetofapplications.
ment,wedevelopedarewardmodeltoassessper- Qualitative results. In Fig. 3, we provide ex-
| formance. | Foreachtaskwithinanapp,wescored |     |     |     |     |     |
| --------- | ------------------------------- | --- | --- | --- | --- | --- |
amplesshowcasingtheagent’sexecutionprocess
differentUIpages. TheclosertheUIpagewasto forvarioustasks. Thisqualitativeanalysisserves
the objective, the higher the score received. This to demonstrate the agent’s capacity to accurately
meansthateveniftheagentfailedtocompletethe
perceive,reason,andactinresponsetogiventasks.
task,itwouldstillreceivecreditbasedonitsfinal For a more comprehensive understanding of our
| state. |     |     |     | agent’scapabilities,pleaserefertoourprojectpage, |     |     |
| ------ | --- | --- | --- | ------------------------------------------------ | --- | --- |
AverageSteps: Wealsoreportedtheaveragenum- whichincludesadditionaldemonstrationvideos.
| ber of steps                   | required | to successfully | finish | tasks         |     |     |
| ------------------------------ | -------- | --------------- | ------ | ------------- | --- | --- |
| acrosstheselectedapplications. |          |                 |        | 4.3 CaseStudy |     |     |
Results. Thecomparisonofourexperimentalre- To gain deeper insights into the vision capabili-
sultsispresentedinTable1. Wereporttheaverage tiesofouragent,weconductedanextensivecase
performanceof45taskson9ofthe10previously study using Adobe Lightroom, an image-editing
describedapps. Notably,weexcludedLightroom application. This specific case study allowed us
fromthisevaluation,asassessingtaskcompletion toevaluatetheagent’sproficiencyinhandlingvi-
inthisapplicationpresentedinherentambiguities. sual tasks, which was previously impossible for
Asdemonstrated,oursimplifiedactionspacesig- text-only agent models. Lightroom, as an image-
nificantlyimprovestheperformanceoftheGPT-4 editingappwithvariouseditingtools,demandsa
baseline. OurobservationsindicatethatLLMstrug- widerangeofoperations,suchasselectingappro-
gleswithproducingaccuratexycoordinates,while priate tools and manipulating image parameters.
oursimplifiedactionspaceeliminatesthischalleng- Thiscasestudyprovidesarobustevaluationofthe
ing requirement. Additionally, documents gener- agent’soverallcapabilities. Additionally,theopen-
atedthroughautonomousexplorationandobserv- ended nature of image editing tasks allows us to
7

assess the agent’s problem-solving abilities. We Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu,
prepared five images with visual issues, such as Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang,
|              |     |               |     |         |     |          | Rosario | Jauregui | Ruano,      | Kyle    | Jeffrey, | Sally Jes- |
| ------------ | --- | ------------- | --- | ------- | --- | -------- | ------- | -------- | ----------- | ------- | -------- | ---------- |
| low contrast | and | overexposure. |     | Various |     | variants |         |          |             |         |          |            |
|              |     |               |     |         |     |          | month,  | Nikhil   | Joshi, Ryan | Julian, | Dmitry   | Kalash-    |
ofourmodel,aspreviouslyillustrated,wereused
|                    |     |     |                        |     |     |     | nikov,  | Yuheng | Kuang,    | Kuang-Huei |          | Lee, Sergey |
| ------------------ | --- | --- | ---------------------- | --- | --- | --- | ------- | ------ | --------- | ---------- | -------- | ----------- |
| toedittheseimages. |     |     | Auserstudywasconducted |     |     |     |         |        |           |            |          |             |
|                    |     |     |                        |     |     |     | Levine, | Yao    | Lu, Linda | Luu,       | Carolina | Parada, Pe- |
to rank the editing results produced by different terPastor, JornellQuiambao, KanishkaRao, Jarek
Rettinghouse,DiegoReyes,PierreSermanet,Nico-
| methods. | Wealsoreportedtheaveragenumberof |     |     |     |     |     |     |     |     |     |     |     |
| -------- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
lasSievers,ClaytonTan,AlexanderToshev,Vincent
| tools used | for | image | editing, | providing |     | an addi- |     |     |     |     |     |     |
| ---------- | --- | ----- | -------- | --------- | --- | -------- | --- | --- | --- | --- | --- | --- |
Vanhoucke,FeiXia,TedXiao,PengXu,SichunXu,
tionalreferencetotheeditingprocess’scomplexity.
|     |     |     |     |     |     |     | MengyuanYan,andAndyZeng.2022. |     |     |     |     | Doasican |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------- | --- | --- | --- | --- | -------- |
Allmodelswereassignedthetaskof“fixthisimage andnotasisay: Groundinglanguageinroboticaf-
|     |     |     |     |     |     |     | fordances. | InarXivpreprintarXiv:2204.01691. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | -------------------------------- | --- | --- | --- | --- |
untilitlooksgoodtoyou”withoutspecifyingthe
| image’sproblems. |     | Thecomparisonoftheresults |     |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
AnthonyBrohan,NoahBrown,JusticeCarbajal,Yevgen
| ispresentedinTable2. |     |     | Aswecansee,ouragent |     |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Chebotar,XiChen,KrzysztofChoromanski,Tianli
model with documents yields consistently better Ding,DannyDriess,AvinavaDubey,ChelseaFinn,
|     |     |     |     |     |     |     | et al. 2023. |     | Rt-2: Vision-language-action |     |     | models |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ---------------------------- | --- | --- | ------ |
resultsthantheGPT-4baseline,whichemphasizes
|                                     |     |     |     |     |     |         | transfer | web | knowledge | to robotic | control. | arXiv |
| ----------------------------------- | --- | --- | --- | --- | --- | ------- | -------- | --- | --------- | ---------- | -------- | ----- |
| theinfluenceofdocumentsinourdesign. |     |     |     |     |     | Thegen- |          |     |           |            |          |       |
preprintarXiv:2307.15818.
erateddocumentsbywatchingthedemonstration
produced comparable results with the results of AnthonyBrohan,NoahBrown,JusticeCarbajal,Yev-
manually crafted documents, which suggests the genChebotar,JosephDabis,ChelseaFinn,Keerthana
Gopalakrishnan,KarolHausman,AlexHerzog,Jas-
| effectiveness |     | of the | exploration | phase. |     | We also |          |            |     |       |                     |     |
| ------------- | --- | ------ | ----------- | ------ | --- | ------- | -------- | ---------- | --- | ----- | ------------------- | --- |
|               |     |        |             |        |     |         | mineHsu, | etal.2022. |     | Rt-1: | Roboticstransformer |     |
find that with a document, the agent tends to use arXiv preprint
|                                            |     |     |     |     |     |     | for real-world    |     | control | at scale. |     |     |
| ------------------------------------------ | --- | --- | --- | --- | --- | --- | ----------------- | --- | ------- | --------- | --- | --- |
| varioustoolstoimprovetheimagequality,while |     |     |     |     |     |     | arXiv:2212.06817. |     |         |           |     |     |
theGPT-4baselineusesfewertools.
|     |     |     |     |     |     |     | Mark Chen, | Jerry | Tworek, | Heewoo | Jun, | Qiming |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ----- | ------- | ------ | ---- | ------ |
Yuan,HenriquePondedeOliveiraPinto,JaredKa-
5 Conclusion
|     |     |     |     |     |     |     | plan, HarriEdwards, |     | YuriBurda, |     | NicholasJoseph, |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | ---------- | --- | --------------- | --- |
In this paper, we have introduced a novel multi- Greg Brockman, et al. 2021. Evaluating large
|             |           |     |      |           |     |        | language | models | trained | on code. | arXiv | preprint |
| ----------- | --------- | --- | ---- | --------- | --- | ------ | -------- | ------ | ------- | -------- | ----- | -------- |
| modal agent | framework |     | that | leverages | the | vision |          |        |         |          |       |          |
arXiv:2107.03374.
| capabilities | of  | large | language | models | to  | operate |     |     |     |     |     |     |
| ------------ | --- | ----- | -------- | ------ | --- | ------- | --- | --- | --- | --- | --- | --- |
smartphoneapplicationsinahuman-likemanner. MetaFAIR,AntonBakhtin, NoamBrown, EmilyDi-
Ourapproacheliminatestheneedforsystemback- nan, Gabriele Farina, Colin Flaherty, Daniel Fried,
|            |     |        |           |               |     |     | Andrew | Goff, | Jonathan | Gray, | Hengyuan | Hu, et al. |
| ---------- | --- | ------ | --------- | ------------- | --- | --- | ------ | ----- | -------- | ----- | -------- | ---------- |
| end access | and | offers | security, | adaptability, |     | and |        |       |          |       |          |            |
2022. Human-levelplayinthegameofdiplomacy
| flexibilityadvantages. |     |     | Ourexploration-basedlearn- |     |     |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
bycombininglanguagemodelswithstrategicreason-
ing strategy allows the agent to quickly adapt to ing. Science,378(6624):1067–1074.
| new applications |     | with | unfamiliar |     | user interfaces, |     |     |     |     |     |     |     |
| ---------------- | --- | ---- | ---------- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
HirokiFuruta,Kuang-HueiLee,OfirNachum,Yutaka
| making | it a versatile |     | tool | for various | tasks. | Our |     |     |     |     |     |     |
| ------ | -------------- | --- | ---- | ----------- | ------ | --- | --- | --- | --- | --- | --- | --- |
Matsuo,AleksandraFaust,ShixiangShaneGu,and
| extensive | experiments |     | across | various | apps | high- |                   |     |                             |     |     |     |
| --------- | ----------- | --- | ------ | ------- | ---- | ----- | ----------------- | --- | --------------------------- | --- | --- | --- |
|           |             |     |        |         |      |       | IzzeddinGur.2023. |     | Multimodalwebnavigationwith |     |     |     |
lightouragent’sabilitytohandlediversehigh-level instruction-finetunedfoundationmodels.
tasksandunderscoreitsadaptabilityandlearning
efficiency. Izzeddin Gur, Hiroki Furuta, Austin Huang, Mustafa
Safdari,YutakaMatsuo,DouglasEck,andAleksan-
| Limitation. |     | Wehaveadoptedasimplifiedaction |     |     |     |     |                |     |                              |     |     |     |
| ----------- | --- | ------------------------------ | --- | --- | --- | --- | -------------- | --- | ---------------------------- | --- | --- | --- |
|             |     |                                |     |     |     |     | draFaust.2023. |     | Areal-worldwebagentwithplan- |     |     |     |
spaceforsmartphoneoperations,whichmeansthat ning,longcontextunderstanding,andprogramsyn-
thesis.
advancedcontrolssuchasmulti-touchandirregu-
| largesturesarenotsupported. |     |     |     | Thislimitationmay |     |     |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
YuchengHan,ChiZhang,XinChen,XuYang,Zhibin
restricttheagent’sapplicabilityinsomechalleng-
Wang,GangYu,BinFu,andHanwangZhang.2023.
ingscenarios. Nevertheless,werecognizethisas Chartllama: Amultimodalllmforchartunderstand-
| anavenueforfutureresearchanddevelopment. |     |     |     |     |     |     | ingandgeneration. |     |     |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- |
SiruiHong,MingchenZhuge,JonathanChen,Xiawu
| References |     |     |     |     |     |     | Zheng,YuhengCheng,CeyaoZhang,JinlinWang, |     |     |     |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- |
ZiliWang,StevenKaShingYau,ZijuanLin,Liyang
Michael Ahn, Anthony Brohan, Noah Brown, Yev- Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu,
genChebotar,OmarCortes,ByronDavid,Chelsea andJürgenSchmidhuber.2023. Metagpt: Metapro-
Finn,ChuyuanFu,KeerthanaGopalakrishnan,Karol grammingforamulti-agentcollaborativeframework.
8

Zhiting Hu and Tianmin Shu. 2023. Language mod- HugoTouvron,ThibautLavril,GautierIzacard,Xavier
els, agent models, and world models: The law for Martinet,Marie-AnneLachaux,TimothéeLacroix,
machine reasoning and planning. arXiv preprint BaptisteRozière,NamanGoyal,EricHambro,Faisal
arXiv:2312.05230. Azhar,AurelienRodriguez,ArmandJoulin,Edouard
|           |            |      |            |       |     | Grave,andGuillaumeLample.2023a. |     |     |     |     | Llama: | Open |
| --------- | ---------- | ---- | ---------- | ----- | --- | ------------------------------- | --- | --- | --- | --- | ------ | ---- |
| Yanda Li, | Chi Zhang, | Gang | Yu, Zhibin | Wang, | Bin |                                 |     |     |     |     |        |      |
andefficientfoundationlanguagemodels.
Fu,GuoshengLin,ChunhuaShen,LingChen,and
Yunchao Wei. 2023. Stablellava: Enhanced visual Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
instructiontuningwithsynthesizedimage-dialogue
|     |     |     |     |     |     | bert, Amjad | Almahairi, |     | Yasmine | Babaei, |     | Nikolay |
| --- | --- | --- | --- | --- | --- | ----------- | ---------- | --- | ------- | ------- | --- | ------- |
data.
Bashlykov,SoumyaBatra,PrajjwalBhargava,Shruti
Bhosale,DanBikel,LukasBlecher,CristianCanton
| Haotian | Liu, Chunyuan | Li, | Yuheng | Li, and Yong | Jae |     |     |     |     |     |     |     |
| ------- | ------------- | --- | ------ | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Ferrer,MoyaChen,GuillemCucurull,DavidEsiobu,
| Lee.2023a. | Improvedbaselineswithvisualinstruc- |     |     |     |     |     |     |     |     |     |     |     |
| ---------- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
JudeFernandes,JeremyFu,WenyinFu,BrianFuller,
tiontuning.
CynthiaGao,VedanujGoswami,NamanGoyal,An-
thonyHartshorn,SagharHosseini,RuiHou,Hakan
HaotianLiu,ChunyuanLi,QingyangWu,andYongJae
Inan,MarcinKardas,ViktorKerkez,MadianKhabsa,
| Lee.2023b. | Visualinstructiontuning. |     |     |     |     |     |     |     |     |     |     |     |
| ---------- | ------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
IsabelKloumann,ArtemKorenev,PunitSinghKoura,
Marie-AnneLachaux,ThibautLavril,JenyaLee,Di-
XiaoLiu,HaoYu,HanchenZhang,YifanXu,Xuanyu
Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen anaLiskovich,YinghaiLu,YuningMao,XavierMar-
Men,KejuanYang,ShudanZhang,XiangDeng,Ao- tinet,TodorMihaylov,PushkarMishra,IgorMoly-
han Zeng, Zhengxiao Du, Chenhui Zhang, Sheng bog, Yixin Nie, Andrew Poulton, Jeremy Reizen-
Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie stein,RashiRungta,KalyanSaladi,AlanSchelten,
|                                    |     |     |     |     |        | Ruan Silva, | Eric | Michael | Smith, | Ranjan | Subrama- |     |
| ---------------------------------- | --- | --- | --- | --- | ------ | ----------- | ---- | ------- | ------ | ------ | -------- | --- |
| Huang,YuxiaoDong,andJieTang.2023c. |     |     |     |     | Agent- |             |      |         |        |        |          |     |
Bench: EvaluatingLLMsasagents. arXivpreprint nian, Xiaoqing Ellen Tan, Binh Tang, Ross Tay-
arXiv: 2308.03688. lor, Adina Williams, Jian Xiang Kuan, Puxin Xu,
ZhengYan,IliyanZarov,YuchenZhang,AngelaFan,
OpenAI. 2021. Chatgpt. https://openai.com/ Melanie Kambadur, Sharan Narang, Aurelien Ro-
research/chatgpt. driguez,RobertStojnic,SergeyEdunov,andThomas
|              |                       |     |     |     |     | Scialom. | 2023b. | Llama | 2:  | Open foundation |     | and |
| ------------ | --------------------- | --- | --- | --- | --- | -------- | ------ | ----- | --- | --------------- | --- | --- |
| OpenAI.2023. | Gpt-4technicalreport. |     |     |     |     |          |        |       |     |                 |     |     |
fine-tunedchatmodels.
JoonSungPark,JosephO’Brien,CarrieJunCai,Mered-
ZihaoWang,ShaofeiCai,AnjiLiu,YonggangJin,Jin-
ithRingelMorris,PercyLiang,andMichaelSBern-
bingHou,BoweiZhang,HaoweiLin,ZhaofengHe,
| stein.2023.      | Generativeagents: |                           | Interactivesimulacra |          |     |              |        |         |           |            |     |        |
| ---------------- | ----------------- | ------------------------- | -------------------- | -------- | --- | ------------ | ------ | ------- | --------- | ---------- | --- | ------ |
|                  |                   |                           |                      |          |     | Zilong       | Zheng, | Yaodong | Yang,     | Xiaojian   | Ma, | and    |
| ofhumanbehavior. |                   | InProceedingsofthe36thAn- |                      |          |     |              |        |         |           |            |     |        |
|                  |                   |                           |                      |          |     | Yitao Liang. |        | 2023.   | Jarvis-1: | Open-world |     | multi- |
| nual ACM         | Symposium         | on                        | User Interface       | Software |     |              |        |         |           |            |     |        |
taskagentswithmemory-augmentedmultimodallan-
andTechnology,pages1–22.
guagemodels.
| Chen Qian, | Xin Cong, | Cheng | Yang, | Weize | Chen, |     |     |     |     |     |     |     |
| ---------- | --------- | ----- | ----- | ----- | ----- | --- | --- | --- | --- | --- | --- | --- |
YushengSu,JuyuanXu,ZhiyuanLiu,andMaosong ZhihengXi,WenxiangChen,XinGuo,WeiHe,Yiwen
|            |                                   |     |     |     |     | Ding, Boyang |          | Hong,    | Ming | Zhang,      | Junzhe  | Wang,    |
| ---------- | --------------------------------- | --- | --- | --- | --- | ------------ | -------- | -------- | ---- | ----------- | ------- | -------- |
| Sun.2023.  | Communicativeagentsforsoftwarede- |     |     |     |     |              |          |          |      |             |         |          |
|            |                                   |     |     |     |     | Senjie Jin,  | Enyu     | Zhou,    | et   | al. 2023.   | The     | rise and |
| velopment. | arXivpreprintarXiv:2307.07924.    |     |     |     |     |              |          |          |      |             |         |          |
|            |                                   |     |     |     |     | potential    | of large | language |      | model based | agents: | A        |
Scott Reed, Konrad Zolna, Emilio Parisotto, Ser- survey. arXivpreprintarXiv:2309.07864.
| gio Gomez | Colmenarejo, |     | Alexander | Novikov, |         |     |     |     |     |     |     |     |
| --------- | ------------ | --- | --------- | -------- | ------- | --- | --- | --- | --- | --- | --- | --- |
| Gabriel   | Barth-Maron, | Mai | Gimenez,  | Yury     | Sulsky, |     |     |     |     |     |     |     |
TianbaoXie,FanZhou,ZhoujunCheng,PengShi,Lu-
| JackieKay,JostTobiasSpringenberg,etal.2022. |     |     |     |     | A   |     |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
oxuanWeng,YitaoLiu,TohJingHua,JunningZhao,
arXivpreprintarXiv:2205.06175.
| generalistagent. |     |     |     |     |     | QianLiu,CheLiu,LeoZ.Liu,YihengXu,Hongjin |     |       |         |        |     |         |
| ---------------- | --- | --- | --- | --- | --- | ---------------------------------------- | --- | ----- | ------- | ------ | --- | ------- |
|                  |     |     |     |     |     | Su, Dongchan                             |     | Shin, | Caiming | Xiong, | and | Tao Yu. |
YongliangShen,KaitaoSong,XuTan,DongshengLi, 2023. Openagents: Anopenplatformforlanguage
| WeimingLu,andYuetingZhuang.2023. |                               |      |         | Hugging- |         | agentsinthewild. |          |       |      |           |     |          |
| -------------------------------- | ----------------------------- | ---- | ------- | -------- | ------- | ---------------- | -------- | ----- | ---- | --------- | --- | -------- |
| gpt: Solving                     | ai tasks                      | with | chatgpt | and its  | friends |                  |          |       |      |           |     |          |
| inhuggingface.                   | InAdvancesinNeuralInformation |      |         |          |         |                  |          |       |      |           |     |          |
|                                  |                               |      |         |          |         | Yuzhuang         | Xu, Shuo | Wang, | Peng | Li, Fuwen |     | Luo, Xi- |
ProcessingSystems.
|     |     |     |     |     |     | aolong | Wang, | Weidong | Liu, | and Yang | Liu. | 2023. |
| --- | --- | --- | --- | --- | --- | ------ | ----- | ------- | ---- | -------- | ---- | ----- |
ChunyiSun,JunlinHan,WeijianDeng,XinlongWang, Exploring large language models for communica-
ZishanQin,andStephenGould.2023. 3d-gpt:Proce- tiongames: Anempiricalstudyonwerewolf. arXiv
preprintarXiv:2309.04658.
| dural3dmodelingwithlargelanguagemodels. |     |     |     |     | arXiv |     |     |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
preprintarXiv:2310.12945.
|     |     |     |     |     |     | An Yan, Zhengyuan |     | Yang, | Wanrong | Zhu, | Kevin | Lin, |
| --- | --- | --- | --- | --- | --- | ----------------- | --- | ----- | ------- | ---- | ----- | ---- |
Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann LinjieLi,JianfengWang,JianweiYang,YiwuZhong,
Dubois,XuechenLi,CarlosGuestrin,PercyLiang, Julian McAuley, Jianfeng Gao, Zicheng Liu, and
andTatsunoriB.Hashimoto.2023. Stanfordalpaca: LijuanWang.2023. Gpt-4vinwonderland: Large
An instruction-following llama model. https:// multimodalmodelsforzero-shotsmartphoneguinav-
github.com/tatsu-lab/stanford_alpaca. igation. arXivpreprintarXiv: 2311.07562.
9

HuiYang,SifuYue,andYunzhongHe.2023a. Auto-
gpt for online decision making: Benchmarks and
additionalopinions.
Zhengyuan Yang, Linjie Li, Kevin Lin, Jianfeng
Wang, Chung-Ching Lin, Zicheng Liu, and Lijuan
Wang. 2023b. The dawn of lmms: Preliminary
explorations with gpt-4v (ision). arXiv preprint
arXiv:2309.17421.
ZhengyuanYang,LinjieLi,KevinLin,JianfengWang,
Chung-Ching Lin, Zicheng Liu, and Lijuan Wang.
2023c. The dawn of lmms: Preliminary explo-
rations with gpt-4v(ision). arXiv preprint arXiv:
2309.17421.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
Shafran,KarthikNarasimhan,andYuanCao.2023.
ReAct:Synergizingreasoningandactinginlanguage
models. InICLR.
Aohan Zeng, Xiao Liu, Zhengxiao Du, Zihan Wang,
Hanyu Lai, Ming Ding, Zhuoyi Yang, Yifan Xu,
Wendi Zheng, Xiao Xia, et al. 2022. Glm-130b:
Anopenbilingualpre-trainedmodel. arXivpreprint
arXiv:2210.02414.
LianminZheng,Wei-LinChiang,YingSheng,Siyuan
Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
ZhuohanLi,DachengLi,Eric.PXing,HaoZhang,
JosephE.Gonzalez,andIonStoica.2023. Judging
llm-as-a-judgewithmt-benchandchatbotarena.
10