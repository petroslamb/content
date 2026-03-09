ChatDev: Communicative Agents for Software Development
ChenQian⋆ WeiLiu⋆ HongzhangLiu♠ NuoChen⋆ YufanDang⋆
JiahaoLi⋆ ChengYang♣ WeizeChen⋆ YushengSu⋆ XinCong⋆
JuyuanXu⋆ DahaiLi♦ ZhiyuanLiu⋆(cid:66) MaosongSun⋆(cid:66)
⋆TsinghuaUniversity ♠TheUniversityofSydney ♣BUPT ♦ModelbestInc.
qianc62@gmail.com liuzy@tsinghua.edu.cn sms@tsinghua.edu.cn
Abstract Develop a Software
Gomoku game
Codes Docs
Softwaredevelopmentisacomplextaskthat
necessitatescooperationamongmultiplemem-
berswithdiverseskills.Numerousstudiesused
deeplearningtoimprovespecificphasesina
waterfall model, such as design, coding, and
testing. However, the deep learning model
in each phase requires unique designs, lead-
ingtotechnicalinconsistenciesacrossvarious
phases,whichresultsinafragmentedandin-
effective development process. In this paper,
we introduce ChatDev, a chat-powered soft-
waredevelopmentframeworkinwhichspecial-
ized agents driven by large language models
main()
(LLMs) are guided in what to communicate
(viachatchain)andhowtocommunicate(via
communicativedehallucination). Theseagents
Figure 1: ChatDev, a chat-powered software
activelycontributetothedesign,coding,and (cid:58)(cid:58)(cid:58)
developmentframework, integratesLLMagentswith
testingphasesthroughunifiedlanguage-based (cid:58)(cid:58)(cid:58)
varioussocialroles,workingautonomouslytodevelop
communication, with solutions derived from
comprehensivesolutionsviamulti-agentcollaboration.
theirmulti-turndialogues. Wefoundtheiruti-
lization of natural language is advantageous
forsystemdesign,andcommunicatinginpro-
diverse downstream applications. Furthermore,
gramming language proves helpful in debug-
ging. Thisparadigmdemonstrateshowlinguis- autonomous agents (Richards, 2023; Zhou et al.,
ticcommunicationfacilitatesmulti-agentcol- 2023a)havegainedattentionforenhancingtheca-
laboration, establishing language as a unify- pabilitiesofLLMswithadvancedfeaturessuchas
ingbridgeforautonomoustask-solvingamong context-awarememory(Sumersetal.,2023),multi-
LLMagents. Thecodeanddataareavailable
stepplanning(Liuetal.,2023),andstrategictool
athttps://github.com/OpenBMB/ChatDev.
using(Schicketal.,2023).
Softwaredevelopmentisacomplextaskthatne-
1 Introduction cessitates cooperation among multiple members
with diverse skills (e.g., architects, programmers,
Large language models (LLMs) have led to sub-
and testers) (Basili, 1989; Sawyer and Guinan,
stantial transformations due to their ability to ef-
1998). This entails extensive communication
fortlesslyintegrateextensiveknowledgeexpressed
among different roles to understand and analyze
in language (Brown et al., 2020; Bubeck et al.,
requirementsthroughnaturallanguage,whilealso
2023),combinedwiththeirstrongcapacityforrole-
encompassingdevelopmentanddebuggingusing
playingwithindesignatedroles(Parketal.,2023;
programminglanguages(Ernst,2017;Bankeretal.,
Hua et al., 2023; Chen et al., 2023b). This ad-
1998). Numerousstudiesusedeeplearningtoim-
vancementeliminatestheneedformodel-specific
provespecificphasesofthewaterfallmodelinsoft-
designs and delivers impressive performance in
waredevelopment,suchasdesign,coding,andtest-
(cid:66):CorrespondingAuthor. ing(Pudlitzetal.,2019;MartínandAbran,2015;
4202
nuJ
5
]ES.sc[
5v42970.7032:viXra

Gaoetal.,2019;Wangetal.,2016). Duetothese softwarerequirementdescriptionsandconducted
technical inconsistencies, methods employed in comprehensiveanalyses. Theresultsindicatethat
differentphasesremainisolateduntilnow. Every ChatDevnotablyimprovesthequalityofsoftware,
phase,fromdatacollectionandlabelingtomodel leading to improved completeness, executability,
trainingandinference,requiresitsuniquedesigns, andbetterconsistencywithrequirements. Further
leading to a fragmented and less efficient devel- investigations reveal that natural-language com-
opmentprocessinthefield(Freemanetal.,2001; munications contribute to comprehensive system
Ernst,2017;Winkleretal.,2020). design,whileprogramming-languagecommunica-
Motivated by the expert-like potential of au- tionsdrivesoftwareoptimization. Insummary,the
tonomousagents,weaimtoestablishlanguageasa proposed paradigm demonstrates how linguistic
unifyingbridge—utilizingmultipleLLM-powered communication facilitates multi-agent collabora-
agentswithspecializedrolesforcooperativesoft- tion,establishinglanguageasaunifyingbridgefor
ware development through language-based com- autonomoustask-solvingamongLLMagents.
munication across different phases; solutions in
differentphasesarederivedfromtheirmulti-turn 2 RelatedWork
dialogues,whetherdealingwithtextorcode. Nev-
ertheless, due to the tendency of LLM hallucina- Trained on vast datasets to comprehend and ma-
tions(Dhuliawalaetal.,2023;Zhangetal.,2023b), nipulate billions of parameters, LLMs have be-
the strategy of generating software through com- come pivotal in natural language processing due
municativeagentscouldleadtothenon-trivialchal- to their seamless integration of extensive knowl-
lengeofcodinghallucinations,whichinvolvesthe edge (Brown et al., 2020; Bubeck et al., 2023;
generationofsourcecodethatisincomplete,unex- Vaswanietal.,2017;Radfordetal.;Touvronetal.,
ecutable,orinaccurate,ultimatelyfailingtofulfill 2023; Wei et al., 2022a; Shanahan et al., 2023;
the intended requirements (Agnihotri and Chug, Chenetal.,2021;Brantsetal.,2007;Chenetal.,
2020). Thefrequentoccurrenceofcodinghalluci- 2021; Ouyang et al., 2022; Yang et al., 2023a;
nationinturnreflectstheconstrainedautonomyof Qin et al., 2023b; Kaplan et al., 2020). Further-
agents in task completion, inevitably demanding more,LLMshavedemonstratedstrongrole-playing
additionalmanualinterventionandtherebyhinder- abilities (Li et al., 2023a; Park et al., 2023; Hua
ing the immediate usability and reliability of the etal.,2023;Chanetal.,2023;Zhouetal.,2023b;
generatedsoftware(Jietal.,2023). Chenetal.,2023b,a;Cohenetal.,2023;Lietal.,
Inthispaper,weproposeChatDev(seeFigure1), 2023b). Recentprogress, particularly inthe field
achat-poweredsoftware-developmentframework of autonomous agents (Zhou et al., 2023a; Wang
(cid:58)(cid:58)(cid:58) (cid:58)(cid:58)(cid:58)
integrating multiple "software agents" for active etal.,2023a;Parketal.,2023;Wangetal.,2023e;
involvement in three core phases of the software Richards,2023;Osika,2023;Wangetal.,2023d),
lifecycle: design,coding,andtesting. Technically, is largely attributed to the foundational advances
ChatDev uses a chat chain to divide each phase in LLMs. These agents utilize the robust capa-
into smaller subtasks further, enabling agents’ bilities of LLMs, displaying remarkable skills in
multi-turn communications to cooperatively pro- memory (Park et al., 2023; Sumers et al., 2023),
pose and develop solutions (e.g., creative ideas planning(Chenetal.,2023b;Liuetal.,2023)and
or source code). The chain-structured workflow tooluse(Schicketal.,2023;Caietal.,2023;Qin
guides agents on what to communicate, foster- etal.,2023a;Ruanetal.,2023;Yangetal.,2023b),
ingcooperationandsmoothlylinkingnatural-and enablingthemtoreasonincomplexscenarios(Wei
programming-languagesubtaskstopropelproblem- etal.,2022b;Zhaoetal.,2023;Zhouetal.,2023a;
solving. Additionally,tominimizecodinghalluci- Ma et al., 2023; Zhang et al., 2023a; Wang et al.,
nations, ChatDev includes an communicative de- 2023b;Dingetal.,2023;Weng,2023).
hallucination mechanism, enabling agents to ac- Softwaredevelopmentisamultifacetedandin-
tively request more specific details before giving tricateprocessthatrequiresthecooperationofmul-
direct responses. The communication pattern in- tiple experts from various fields (Yilmaz et al.,
structs agents on how to communicate, enabling 2012; Acuna et al., 2006; Basili, 1989; Sawyer
precise information exchange for effective solu- and Guinan, 1998; Banker et al., 1998; France
tionoptimizationwhilereducingcodinghallucina- and Rumpe, 2007), encompassing the require-
tions. Webuiltacomprehensivedatasetcontaining ment analysis and system design in natural lan-

|     |     |     | Design |     |     | Coding |     |     |     | Testing |     |     |     |
| --- | --- | --- | ------ | --- | --- | ------ | --- | --- | --- | ------- | --- | --- | --- |
Phases
|     | Subtasks |     | Design |     | Coding |     | Code     |     | Code     |     | Testing |     |     |
| --- | -------- | --- | ------ | --- | ------ | --- | -------- | --- | -------- | --- | ------- | --- | --- |
|     |          |     |        |     |        |     | Complete |     | Review   |     |         |     |     |
|     |          |     | CEO    |     | CTO    |     | CTO      |     | Reviewer |     | Tester  |     |     |
Instructor
|     | Chat Chain | {task} |     | {ideas} |     | {code} |     | {code} |     | {code} |     | {code} |     |
| --- | ---------- | ------ | --- | ------- | --- | ------ | --- | ------ | --- | ------ | --- | ------ | --- |
Assistant
|     |     |     | CTO |     | Programmer |     | Programmer |     | Programmer |     | Programmer |     |     |
| --- | --- | --- | --- | --- | ---------- | --- | ---------- | --- | ---------- | --- | ---------- | --- | --- |
Figure 2: Upon receiving a preliminary task requirement (e.g., “develop a Gomoku game”), these software
agentsengageinmulti-turncommunicationandperforminstruction-followingalongachain-structuredworkflow,
collaboratingtoexecuteaseriesofsubtasksautonomouslytocraftacomprehensivesolution.
guages (Pudlitz et al., 2019; Martín and Abran, formingtextualrequirementsintofunctionalsoft-
2015; Nahar et al., 2022), along with system de- wareinasinglestepremainsasignificantchallenge.
velopment and debugging in programming lan- ChatDevthusadoptsthecoreprinciplesofthewa-
guages(Gaoetal.,2019;Wangetal.,2016;Wan terfallmodel,usingachatchain(C)withsequential
et al., 2022). Numerous studies employ the wa- phases (P), each comprising sequential subtasks
terfall model, a particular software development (T). Specifically,ChatDevsegmentsthesoftware
life cycle, to segment the process into discrete developmentprocessintothreesequentialphases:
phases (e.g., design, coding, testing) and apply design, coding, and testing. The coding phase is
deeplearningtoimprovetheeffectivenessofcer- further subdivided into subtasks of code writing
tainphases(Winkleretal.,2020;Ezzinietal.,2022; andcompletion,andthetestingphaseissegmented
Thaller et al., 2019; Zhao et al., 2021; Nijkamp intocodereview(statictesting)andsystemtesting
etal.,2023;Wanetal.,2018;Wangetal.,2021). (dynamic testing), as illustrated in Figure 2. In
everysubtask,twoagents,eachwiththeirownspe-
3 ChatDev
cializedroles(e.g.,areviewerskilledatidentifying
endlessloopsandaprogrammeradeptinGUIde-
| We  | introduce | ChatDev, | a chat-powered |     | software- |     |     |     |     |     |     |     |     |
| --- | --------- | -------- | -------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:58)(cid:58)(cid:58)(cid:58)
|             |     |           |      |            |          |     | sign), | perform | the | functions | of  | an instructor | (I) |
| ----------- | --- | --------- | ---- | ---------- | -------- | --- | ------ | ------- | --- | --------- | --- | ------------- | --- |
| development |     | framework | that | integrates | multiple |     |        |         |     |           |     |               |     |
(cid:58)(cid:58)(cid:58)
"software agents" with various social roles (e.g., andanassistant(A). Theinstructoragentinitiates
requirementsanalysts,professionalprogrammers instructions,instructing(→)thediscoursetoward
thecompletionofthesubtask,whiletheassistant
andtestengineers)collaboratinginthecorephases
|                                    |     |     |     |     |              |     | agent | adheres | to these | instructions |     | and | responds |
| ---------------------------------- | --- | --- | --- | --- | ------------ | --- | ----- | ------- | -------- | ------------ | --- | --- | -------- |
| ofthesoftwarelifecycle,seeFigure1. |     |     |     |     | Technically, |     |       |         |          |              |     |     |          |
((cid:59))
tofacilitatecooperativecommunication,ChatDev with appropriate solutions. They engage in
|     |     |     |     |     |     |     | a multi-turn |     | dialogue | (C), | working | cooperatively |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | -------- | ---- | ------- | ------------- | --- |
introduceschatchaintofurtherbreakdowneach
|     |     |     |     |     |     |     | until | they | achieve | consensus, | extracting |     | (τ) solu- |
| --- | --- | --- | --- | --- | --- | --- | ----- | ---- | ------- | ---------- | ---------- | --- | --------- |
phaseintosmallerandmanageablesubtasks,which
guidesmulti-turncommunicationsbetweendiffer- tionsthatcanrangefromthetext(e.g.,defininga
softwarefunctionpoint)tocode(e.g.,creatingthe
entrolestoproposeandvalidatesolutionsforeach
initialversionofsourcecode),ultimatelyleading
subtask. Inaddition,toalleviateunexpectedhallu-
cinations,acommunicativepatternnamedcommu- tothecompletionofthesubtask. Theentiretask-
nicativedehallucinationisdevised,whereinagents solvingprocessalongtheagenticworkflowcanbe
formulatedas:
requestmoredetailedinformationbeforerespond-
| ing                               | directly | and then | continue | the | next round | of  |     |     |                    |     |     |     |     |
| --------------------------------- | -------- | -------- | -------- | --- | ---------- | --- | --- | --- | ------------------ | --- | --- | --- | --- |
| communicationbasedonthesedetails. |          |          |          |     |            |     |     | C   | = ⟨P1,P2,...,P|C|⟩ |     |     |     |     |
Pi = ⟨T1,T2,...,T|Pi|⟩
3.1 ChatChain
(1)
|                                          |     |     |     |     |     |     |     | Tj  | (cid:0)    |     | (cid:1) |     |     |
| ---------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ------- | --- | --- |
| AlthoughLLMsshowagoodunderstandingofnat- |     |     |     |     |     |     |     |     | = τ C(I,A) |     |         |     |     |
uralandprogramminglanguages,efficientlytrans- C(I,A) = ⟨I → A, A (cid:59) I⟩
⟲

The dual-agent communication design simplifies maintainacompletecommunicationhistoryamong
communicationsbyavoidingcomplexmulti-agent all agents and phases. To tackle this issue, based
topologies,effectivelystreamliningtheconsensus- onthenatureofthechatchain,weaccordinglyseg-
reaching process (Yin et al., 2023; Chen et al., menttheagents’contextmemoriesbasedontheir
2023b). Subsequently, the solutions from previ- sequentialphases,resultingintwofunctionallydis-
oustasksserveasbridgestothenextphase,allow- tinct types of memory: short-term memory and
ing a smooth transition between subtasks. This long-termmemory. Short-termmemoryisutilized
approach continues until all subtasks are com- to sustain the continuity of the dialogue within a
pleted. It’s worth noting that the conceptually singlephase,whilelong-termmemoryisleveraged
simplebutempiricallypowerfulchain-stylestruc- topreservecontextualawarenessacrossdifferent
| tureguidesagentsonwhattocommunicate,foster- |     |     |     |     |     |     | phases. |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
ingcooperationandsmoothlylinkingnatural-and Formally,short-termmemoryrecordsanagent’s
programming-language subtasks. It also offers a current phase utterances, aiding context-aware
transparentviewoftheentiresoftwaredevelopment decision-making. At the time t during phase Pi,
weuseIi
process,allowingfortheexaminationofintermedi- torepresenttheinstructor’sinstruction
t
atesolutionsandassistinginidentifyingpossible andAi fortheassistant’sresponse. Theshort-term
t
| problems. |     |     |     |     |     |     | memoryMcollectsutterancesuptotimetas: |     |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --- |
Agentization Toenhancethequalityandreduce Mi ⟨(Ii,Ai),(Ii,Ai),...,(Ii,Ai)⟩
|     |     |     |     |     |     |     |     | =   |     |     |     |     | (3) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     | t   | 1   | 1 2 | 2   | t   | t   |
humanintervention,ChatDevimplementsprompt
engineering that only takes place at the start of Inthenexttimestept+1,theinstructorutilizes
each subtask round. As soon as the communica- thecurrentmemorytogenerateanewinstruction
Ii
tionphasebegins,theinstructorandtheassistant ,whichisthenconveyedtotheassistanttopro-
t+1
|                                           |     |     |     |     |     |     | duceanewresponseAi |     |     |     | . Theshort-termmemory |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --------------------- | --- | --- |
| willcommunicatewitheachotherinanautomated |     |     |     |     |     |     |                    |     |     | t+1 |                       |     |     |
loop,continuingthisexchangeuntilthetaskcon- iterativelyupdatesuntilthenumberofcommunica-
cludes. However, simply exchanging responses tionsreachestheupperlimit|Mi|:
cannotachieveeffectivemulti-roundtask-oriented
|     |     |     |     |     |     |     |     | Ii  | =I(Mi), | Ai  | = A(Mi,Ii |     | )   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --------- | --- | --- |
communication,sinceitinevitablyfacessignificant
|     |     |     |     |     |     |     |     | t+1 |     | t   | t+1 | t   | t+1 (4) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- |
challenges including role flipping, instruction re- Mi = Mi ∪(Ii ,Ai )
|          |          |          |     |           |       |      |     |     | t+1 |     | t t+1 | t+1 |     |
| -------- | -------- | -------- | --- | --------- | ----- | ---- | --- | --- | --- | --- | ----- | --- | --- |
| peating, | and fake | replies. | As  | a result, | there | is a |     |     |     |     |       |     |     |
Toperceivedialoguesthroughpreviousphases,
| failure to | advance | the | progression |     | of productive |     |     |     |     |     |     |     |     |
| ---------- | ------- | --- | ----------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
thechatchainonlytransmitsthesolutionsfrompre-
| communications |     | and | hinders | the achievement |     | of  |     |     |     |     |     |     |     |
| -------------- | --- | --- | ------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
viousphasesaslong-termmemoriesM˜,integrat-
| meaningful | solutions. |     | ChatDev | thus | employs | in- |     |     |     |     |     |     |     |
| ---------- | ---------- | --- | ------- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
ingthematthestartofthenextphaseandenabling
| ception | prompting | mechanism |     | (Li | et al., | 2023a) |     |     |     |     |     |     |     |
| ------- | --------- | --------- | --- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- |
thecross-phasetransmissionoflongdialogues:
| for initiating, | sustaining, |     | and | concluding |     | agents’ |     |     |     |     |     |     |     |
| --------------- | ----------- | --- | --- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
communicationtoguaranteearobustandefficient
i
|           |                                 |     |     |     |     |     |     | M˜i∪Pi+1, |     |     | M˜i (cid:91) | τ(Mj |       |
| --------- | ------------------------------- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | ------------ | ---- | ----- |
| workflow. | Thismechanismiscomposedofthein- |     |     |     |     |     |     | Ii+1 =    |     |     | =            |      | ) (5) |
|           |                                 |     |     |     |     |     |     | 1         |     | I   |              |      | |Mj|  |
structorsystempromptP
|        |         |        | I andtheassistantsystem |     |          |       |     |     |     |     | j=1 |     |     |
| ------ | ------- | ------ | ----------------------- | --- | -------- | ----- | --- | --- | --- | --- | --- | --- | --- |
| prompt | P . The | system | prompts                 |     | for both | roles |     |     |     |     |     |     |     |
A
wherePsymbolizesapredeterminedpromptthat
aremostlysymmetrical,coveringtheoverviewand
appearsexclusivelyatthestartofeachphase.
objectivesofthecurrentsubtask,specializedroles,
|     |     |     |     |     |     |     |     | By sharing | only | the | solutions | of each | subtask |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ---- | --- | --------- | ------- | ------- |
accessibleexternaltools,communicationprotocols,
ratherthantheentirecommunicationhistory,Chat-
terminationconditions,andconstraintsorrequire-
Devminimizestheriskofbeingoverwhelmedby
| ments to | avoid | undesirable |     | behaviors. | Then, | an  |     |     |     |     |     |     |     |
| -------- | ----- | ----------- | --- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
toomuchinformation,enhancingconcentrationon
| instructorI | andanassistantAareinstantiatedby |     |     |     |     |     |     |     |     |     |     |     |     |
| ----------- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
eachtaskandencouragingmoretargetedcoopera-
| hypnotizingLLMsviaP |     |     | andP | :   |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|                     |     |     | I    | A   |     |     |     |     |     |     |     |     |     |
tion,whilesimultaneouslyfacilitatingcross-phase
| I = | ρ(LLM,P |     | ), A | = ρ(LLM,P |     | ) (2) |                    |     |     |     |     |     |     |
| --- | ------- | --- | ---- | --------- | --- | ----- | ------------------ | --- | --- | --- | --- | --- | --- |
|     |         | I   |      |           | A   |       | contextcontinuity. |     |     |     |     |     |     |
whereρistherolecustomizationoperation,imple-
|     |     |     |     |     |     |     | 3.2 | CommunicativeDehallucination |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- |
mentedviasystemmessageassignment.
|     |     |     |     |     |     |     | LLM | hallucinations |     | manifest | when | models | gen- |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | -------- | ---- | ------ | ---- |
Memory Notethatthelimitedcontextlengthof erateoutputsthatarenonsensical,factuallyincor-
common LLMs typically restricts the ability to rect,orinaccurate(Dhuliawalaetal.,2023;Zhang

et al., 2023b). This issue is particularly concern- MetaGPT(Hongetal.,2023)isanadvancedframe-
inginsoftwaredevelopment,whereprogramming workthatallocatesspecificrolestovariousLLM-
languagesdemandprecisesyntax—theabsenceof drivensoftwareagentsandincorporatesstandard-
even a single line can lead to system failure. We ized operating procedures to enable multi-agent
haveobservedthatLLMsoftenproducecodinghal- participation. Ineachstepagentswithspecificroles
lucinations,whichencompasspotentialissueslike generatesolutionsbyadheringtostaticinstructions
incomplete implementations, unexecutable code, predefinedbyhumanexperts.
andinconsistenciesthatdon’tmeetrequirements.
|     |     |     |     |     |     |     | Datasets | Notethat,asofnow,thereisn’tapub- |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | -------------------------------- | --- | --- | --- | --- |
Codinghallucinationsfrequentlyappearwhenthe
liclyaccessibledatasetcontainingtextualdescrip-
assistantstrugglestopreciselyfollowinstructions,
|           |        |           |     |            |     |         | tions of     | software | requirements |              | in the | context of |
| --------- | ------ | --------- | --- | ---------- | --- | ------- | ------------ | -------- | ------------ | ------------ | ------ | ---------- |
| often due | to the | vagueness | and | generality |     | of cer- |              |          |              |              |        |            |
|           |        |           |     |            |     |         | agent-driven | software |              | development. | To     | this end,  |
taininstructionsthatrequiremultipleadjustments,
weareactivelyworkingtowardsdevelopingacom-
| making      | it challenging |     | for agents | to           | achieve | full |            |         |     |          |             |     |
| ----------- | -------------- | --- | ---------- | ------------ | ------- | ---- | ---------- | ------- | --- | -------- | ----------- | --- |
|             |                |     |            |              |         |      | prehensive | dataset | for | software | requirement | de- |
| compliance. | Inspired       |     | by this,   | we introduce |         | com- |            |         |     |          |             |     |
scriptions,whichwerefertoasSRDD(Software
municativedehallucination,whichencouragesthe
|     |     |     |     |     |     |     | Requirement |     | Description | Dataset). | Drawing | on  |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ----------- | --------- | ------- | --- |
assistanttoactivelyseekmoredetailedsuggestions
previouswork(Lietal.,2023a),weutilizeexisting
| from the | instructor | before | delivering |     | a formal | re- |          |              |     |            |           |       |
| -------- | ---------- | ------ | ---------- | --- | -------- | --- | -------- | ------------ | --- | ---------- | --------- | ----- |
|          |            |        |            |     |          |     | software | descriptions |     | as initial | examples, | which |
sponse.
arethenfurtherdevelopedthroughaprocessthat
| Specifically, |     | a vanilla | communication |     |     | pattern |          |           |     |           |            |      |
| ------------- | --- | --------- | ------------- | --- | --- | ------- | -------- | --------- | --- | --------- | ---------- | ---- |
|               |     |           |               |     |     |         | combines | LLM-based |     | automatic | generation | with |
betweentheassistantandtheinstructorfollowsa
|     |     |     |     |     |     |     | post-processingrefinementguidedbyhumans. |     |     |     |     | As  |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------------------- | --- | --- | --- | --- | --- |
straightforwardinstruction-responseformat:
|     |     |     |     |     |     |     | a result, | this dataset | includes |     | important | software |
| --- | --- | --- | --- | --- | --- | --- | --------- | ------------ | -------- | --- | --------- | -------- |
⟨I → A, A (cid:59) I⟩⟲ (6) categoriesfrompopularplatformssuchasUbuntu,
|              |          |               |              |                 |            |     | GooglePlay,MicrosoftStore,andAppleStore. |       |          |      |         | It        |
| ------------ | -------- | ------------- | ------------ | --------------- | ---------- | --- | ---------------------------------------- | ----- | -------- | ---- | ------- | --------- |
| In contrast, | our      | communicative |              | dehallucination |            |     |                                          |       |          |      |         |           |
|              |          |               |              |                 |            |     | comprises                                | 1,200 | software | task | prompts | that have |
| mechanism    | features |               | a deliberate | "role           | reversal", |     |                                          |       |          |      |         |           |
|              |          |               |              |                 |            |     | beencarefullycategorizedinto5mainareas:  |       |          |      |         | Edu-      |
wheretheassistanttakesonaninstructor-likerole,
|     |     |     |     |     |     |     | cation,Work,Life,Game,andCreation. |     |     |     |     | Allthese |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --- | --- | -------- |
proactivelyseekingmorespecificinformation(e.g.,
areasarefurtherdividedinto40subcategories,and
| the precise | name | of an | external | dependency |     | and |     |     |     |     |     |     |
| ----------- | ---- | ----- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
eachsubcategorycontains30uniquetaskprompts.
itsrelatedclass)beforedeliveringaconclusivere-
sponse. After the instructor provides a specific Metrics Evaluatingsoftwareisalsoachallenging
modificationsuggestion,theassistantproceedsto
task,especiallywhentryingtoassessitonaholistic
performpreciseoptimization: level. Underthecurrentlimitationofscarcebench-
markresources,traditionalfunction-orientedcode
| ⟨I → | A, ⟨A | → I, | I (cid:59) A⟩⟲, | A   | (cid:59) I⟩⟲ | (7) |                 |         |                    |          |            |       |
| ---- | ----- | ---- | --------------- | --- | ------------ | --- | --------------- | ------- | ------------------ | -------- | ---------- | ----- |
|      |       |      |                 |     |              |     | generation      | metrics | (e.g.,             | pass@k), | cannot     | seam- |
|      |       |      |                 |     |              |     | lessly transfer |         | to a comprehensive |          | evaluation | of    |
Sincethismechanismtacklesoneconcreteissueat
atime,itrequiresmultipleroundsofcommunica- entiresoftwaresystems. Themainreasonforthis
tion to optimize various potential problems. The isthatitisoftenimpracticaltodevelopmanualor
communicationpatterninstructsagentsonhowto automatedtestcasesforvarioustypesofsoftware,
communicate,enablingfiner-grainedinformation especiallythoseinvolvingcomplexinterfaces,fre-
exchangeforeffectivesolutionoptimization,which quentuserinteractions,ornon-deterministicfeed-
practicallyaidsinreducingcodinghallucinations. back. Asaninitialstrategy,weapplythreefunda-
mentalandobjectivedimensionsthatreflectdiffer-
4 Evaluation
entaspectsofcodinghallucinationstoevaluatethe
agent-generatedsoftware,andthenintegratethem
| Baselines | We  | chose | some representative |     |     | LLM- |     |     |     |     |     |     |
| --------- | --- | ----- | ------------------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
tofacilitateamoreholisticevaluation:
basedsoftwaredevelopmentmethodsasourbase-
lines. GPT-Engineer(Osika,2023)isafundamen- • Completenessmeasuresthesoftware’sabilityto
talsingle-agentapproachinLLM-drivensoftware fulfillcodecompletioninsoftwaredevelopment,
agentswithapreciseunderstandingoftaskrequire- quantified as the percentage of software with-
ments and the application of one-step reasoning, out any "placeholder" code snippets. A higher
which highlights its efficiency in generating de- scoreindicatesahigherprobabilityofautomated
| tailed software |     | solutions | at the | repository |     | level. | completion. |     |     |     |     |     |
| --------------- | --- | --------- | ------ | ---------- | --- | ------ | ----------- | --- | --- | --- | --- | --- |

Method Paradigm Completeness Executability Consistency Quality
|     | GPT-Engineer |     |     |     |     | 0.5022† |     | 0.3583† |     | 0.7887† |     | 0.1419† |     |
| --- | ------------ | --- | --- | --- | --- | ------- | --- | ------- | --- | ------- | --- | ------- | --- |
|     | MetaGPT      |     |     |     |     | 0.4834† |     | 0.4145† |     | 0.7601† |     | 0.1523† |     |
|     | ChatDev      |     |     |     |     | 0.5600  |     | 0.8800  |     | 0.8021  |     | 0.3953  |     |
Table1: OverallperformanceoftheLLM-poweredsoftwaredevelopmentmethods,encompassingbothsingle-agent
( )andmulti-agent( )paradigms. Performancemetricsareaveragedforalltasks. Thetopscoresareinbold,
withsecond-highestunderlined. †indicatessignificantstatisticaldifferences(p≤0.05)betweenabaselineandours.
Method Evaluator BaselineWins ChatDevWins Draw Method Duration(s) #Tokens #Files #Lines
|              |     | GPT-4 |     | 22.50% |     | 77.08% | 00.42% |              |          |     |             |        |          |
| ------------ | --- | ----- | --- | ------ | --- | ------ | ------ | ------------ | -------- | --- | ----------- | ------ | -------- |
| GPT-Engineer |     |       |     |        |     |        |        | GPT-Engineer | 15.6000  |     | 7,182.5333  | 3.9475 | 70.2041  |
|              |     | Human |     | 09.18% |     | 90.16% | 00.66% |              |          |     |             |        |          |
|              |     |       |     |        |     |        |        | MetaGPT      | 154.0000 |     | 29,278.6510 | 4.4233 | 153.3000 |
MetaGPT GPT-4 37.50% 57.08% 05.42% ChatDev 148.2148 22,949.4450 4.3900 144.3450
|     |         | Human |                            | 07.92% |     | 88.00% | 04.08% |         |                                            |     |     |     |     |
| --- | ------- | ----- | -------------------------- | ------ | --- | ------ | ------ | ------- | ------------------------------------------ | --- | --- | --- | --- |
|     |         |       |                            |        |     |        |        | Table3: | SoftwarestatisticsincludeDuration(timecon- |     |     |     |     |
|     | Table2: |       | Pairwiseevaluationresults. |        |     |        |        |         |                                            |     |     |     |     |
sumed),#Tokens(numberoftokensused),#Files(num-
berofcodefilesgenerated),and#Lines(totallinesof
codeacrossallfiles)inthesoftwaregenerationprocess.
| • Executability |     |     | assesses | the | software’s | ability | to  |     |     |     |     |     |     |
| --------------- | --- | --- | -------- | --- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- |
runcorrectlywithinacompilationenvironment,
quantifiedasthepercentageofsoftwarethatcom- aconsensusisreached. WeusedChatGPT-3.5with
| pilessuccessfullyandcanrundirectly. |     |     |     |     |     | Ahigher |     |     |     |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
atemperatureof0.2andintegratedPython-3.11.4
scoreindicatesahigherprobabilityofsuccessful
|     |     |     |     |     |     |     |     | forfeedback. | Allbaselinesintheevaluationshare |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | -------------------------------- | --- | --- | --- | --- |
execution.
thesamehyperparametersandsettingsforfairness.
• Consistencymeasureshowcloselythegenerated
| software |              | code | aligns     | with | the original | require-   |      |                        |     |       |            |             |     |
| -------- | ------------ | ---- | ---------- | ---- | ------------ | ---------- | ---- | ---------------------- | --- | ----- | ---------- | ----------- | --- |
|          |              |      |            |      |              |            |      | 4.1 OverallPerformance |     |       |            |             |     |
| ment     | description, |      | quantified |      | as           | the cosine | dis- |                        |     |       |            |             |     |
|          |              |      |            |      |              |            |      | As illustrated         | in  | Table | 1, ChatDev | outperforms |     |
tancebetweenthesemanticembeddingsofthe
textualrequirementsandthegeneratedsoftware all baseline methods across all metrics, showing
|        |     |                                     |     |     |     |     |     | a considerable | margin |     | of improvement. |     | Firstly, |
| ------ | --- | ----------------------------------- | --- | --- | --- | --- | --- | -------------- | ------ | --- | --------------- | --- | -------- |
| code1. |     | Ahigherscoreindicatesagreaterdegree |     |     |     |     |     |                |        |     |                 |     |          |
theimprovementofChatDevandMetaGPTover
ofconsistencywiththerequirements.
• Qualityisacomprehensivemetricthatintegrates GPT-Engineerdemonstratesthatcomplextasksare
|         |     |         |           |     |             |         |     | difficult | to solve | in a single-step |     | solution. | There- |
| ------- | --- | ------- | --------- | --- | ----------- | ------- | --- | --------- | -------- | ---------------- | --- | --------- | ------ |
| various |     | factors | to assess |     | the overall | quality | of  |           |          |                  |     |           |        |
fore,explicitlydecomposingthedifficultproblem
| software, |     | quantified |     | by multiplying2 |     | complete- |     |     |     |     |     |     |     |
| --------- | --- | ---------- | --- | --------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
intoseveralsmaller,moremanageablesubtasksen-
| ness, | executability, |     |     | and consistency. |     | A   | higher |     |     |     |     |     |     |
| ----- | -------------- | --- | --- | ---------------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
qualityscoresuggestsahigheroverallsatisfac- hancestheeffectivenessoftaskcompletion. Addi-
tionally,incomparisontoMetaGPT,ChatDevsig-
| tion | with | the | software | generated, |     | implying | a   |     |     |     |     |     |     |
| ---- | ---- | --- | -------- | ---------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
nificantlyraisestheQualityfrom0.1523to0.3953.
lowerneedforfurthermanualintervention.
Thisadvancementislargelyattributedtotheagents
employingacooperativecommunicationmethod,
| Implementation |     |     | Details |     | We divided | software |     |     |     |     |     |     |     |
| -------------- | --- | --- | ------- | --- | ---------- | -------- | --- | --- | --- | --- | --- | --- | --- |
whichinvolvesautonomouslyproposingandcon-
| development |     | into | 5 subtasks |     | within | 3 phases, | as- |     |     |     |     |     |     |
| ----------- | --- | ---- | ---------- | --- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- |
tinuouslyrefiningsourcecodethroughablendof
signingspecificroleslikeCEO,CTO,programmer,
|           |               |                                    |     |         |           |               |     | natural                 | and programming |           | languages,             |            | as opposed |
| --------- | ------------- | ---------------------------------- | --- | ------- | --------- | ------------- | --- | ----------------------- | --------------- | --------- | ---------------------- | ---------- | ---------- |
| reviewer, |               | and tester.                        | A   | subtask | would     | terminate     |     |                         |                 |           |                        |            |            |
|           |               |                                    |     |         |           |               |     | to merely               | delivering      | responses |                        | based      | on human-  |
| and       | get a         | conclusion                         |     | either  | after     | two unchanged |     |                         |                 |           |                        |            |            |
|           |               |                                    |     |         |           |               |     | predefinedinstructions. |                 |           | Thecommunicativeagents |            |            |
| code      | modifications |                                    | or  | after   | 10 rounds | of commu-     |     |                         |                 |           |                        |            |            |
|           |               |                                    |     |         |           |               |     | guide each              | subtask         | towards   |                        | integrated | and auto-  |
| nication. |               | Duringthecodecompletion,review,and |     |         |           |               |     |                         |                 |           |                        |            |            |
matedsolutions,efficientlyovercomingtherestric-
| testing, | a   | communicative |     | dehallucination |     |     | is acti- |     |     |     |     |     |     |
| -------- | --- | ------------- | --- | --------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
tionstypicallylinkedtomanuallyestablishedop-
vated. Foreaseofidentifyingsolutions,theassis-
timizationrules,andofferingamoreversatileand
tantbeginsresponseswith"<SOLUTION>"when
adaptableframeworkforproblem-solving.
1Commentsshouldbeexcludedfromthecodetoavoid Tofurtherunderstanduserpreferencesinpracti-
potentialinformationleakageduringevaluations.
calsettings,weusethesettingadoptedbyLietal.
2Onecanalsochoosetoaveragethesub-metrics,which
yieldssimilartrends. (2023a),whereagent-generatedsolutionsarecom-

V a r i a n t Com p l e te ness Exe c u t a b ility Co n s i st e ncy Q u a l it y 3 2.51% 2.24% 1.39% T a r g e t  U s e r
|     |     |     |     |     |     |     | 3 .15% |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
C h a t D e v 0 .5 6 0 0 0 . 8 8 0 0 0 . 8 0 2 1 0. 3 9 5 3 .4 6 D a t a   M a n a gement
|         |     |        |        |        |        | 5.4   | %   | 21.44% |     |              |     |     |
| ------- | --- | ------ | ------ | ------ | ------ | ----- | --- | ------ | --- | ------------ | --- | --- |
|         |     |        |        |        |        |       | 1 % |        |     | U I  &   U X |     |     |
| ≤Coding |     | 0.4100 | 0.7700 | 0.7958 | 0.2512 | 5.92% |     |        |     |              |     |     |
Customization
| ≤Complete |     | 0.6250 | 0.7400 | 0.7978 | 0.3690 |       |     |        |     |             |     |     |
| --------- | --- | ------ | ------ | ------ | ------ | ----- | --- | ------ | --- | ----------- | --- | --- |
| ≤Review   |     | 0.5750 | 0.8100 | 0.7980 | 0.3717 | 6.93% |     |        |     | Performance |     |     |
|           |     |        |        |        |        |       | %   | 20.55% |     |             |     |     |
≤Testing 0.5600 0.8800 0.8021 0.3953 7.78 I n te g r a t io n
|     |     |     |     |     |     |     |     |     |     | R e a l- T i | m e  Update |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ----------- | --- |
⧹CDH
|        |     | 0.4700 | 0.8400 | 0.7983 | 0.3094 |     | 19.23% |     |     | Recommendation |     |     |
| ------ | --- | ------ | ------ | ------ | ------ | --- | ------ | --- | --- | -------------- | --- | --- |
| ⧹Roles |     | 0.5400 | 0.5800 | 0.7385 | 0.2212 |     |        |     |     |                |     |     |
Platform
Collaboration
Table4: Ablationstudyonmaincomponentsormech- Security & Privacy
anisms. ≤ x denotes halting the chat chain after the 57.20% Scalability & Maintenance
completionofthexphrase,and⧹denotestheremoving
| operation. |     | CDHdenotesthecommunicativedehalluci- |     |     |     |     |     |     |     |     |     |     |
| ---------- | --- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Natural-Language
nationmechanism.
|     |     |     |     |     |     |     | 42.80% |     |     | Programming-Language |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | -------------------- | --- | --- |
paredinpairsbybothhumanparticipantsandthe
|           |     |             |             |     |               |     | 10.19% 18.53% |     |     |     |     |     |
| --------- | --- | ----------- | ----------- | --- | ------------- | --- | ------------- | --- | --- | --- | --- | --- |
| prevalent |     | GPT-4 model | to identify |     | the preferred |     |               |     |     |     |     |     |
Coding
one.3
|                                            | Table2showsChatDevconsistentlyoutper- |     |     |     |     | 10.19% |     |        |     | Code Complete  |     |     |
| ------------------------------------------ | ------------------------------------- | --- | --- | --- | --- | ------ | --- | ------ | --- | -------------- | --- | --- |
| formingotherbaselines,withhigheraveragewin |                                       |     |     |     |     |        |     |        |     | Code Review    |     |     |
|                                            |                                       |     |     |     |     |        |     | 61.09% |     | System Testing |     |     |
ratesinbothGPT-4andhumanevaluations.
|     | Furthermore, | the software | statistics |     | presented |     |     |     |     |     |     |     |
| --- | ------------ | ------------ | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
inTable3indicatesthatthemulti-agentparadigm,
Figure3: Theutterancedistributionofagentcommuni-
despitebeingslowerandconsumingmoretokens
cationsthroughouttheentiredevelopmentprocess.
thanthesingle-agentmethod,yieldsagreaternum-
berofcodefilesandalargercodebase,whichmay
enhancethesoftware’sfunctionalityandintegrity.
|           |     |               |           |     |               | tionsamongintelligentagents. |               |     |                 | Meanwhile,elim- |     |            |
| --------- | --- | ------------- | --------- | --- | ------------- | ---------------------------- | ------------- | --- | --------------- | --------------- | --- | ---------- |
| Analyzing |     | the dialogues | of agents |     | suggests that |                              |               |     |                 |                 |     |            |
|           |     |               |           |     |               | inating                      | communicative |     | dehallucination |                 |     | results in |
themulti-agentcommunicationmethodoftenleads
|     |     |     |     |     |     | a decrease | across | all | metrics, | indicating |     | its effec- |
| --- | --- | --- | --- | --- | --- | ---------- | ------ | --- | -------- | ---------- | --- | ---------- |
agentstoautonomouslyofferfunctionalenhance-
|     |     |     |     |     |     | tivenessinaddressingcodinghallucinations. |     |     |     |     |     | Most |
| --- | --- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | ---- |
ments(e.g.,GUIcreationorincreasinggamediffi-
|     |     |     |     |     |     | interestingly, |     | the most | substantial |     | impact | on per- |
| --- | --- | --- | --- | --- | --- | -------------- | --- | -------- | ----------- | --- | ------ | ------- |
culty),therebypotentiallyresultingintheincorpo-
|     |     |     |     |     |     | formance | occurs | when | the | roles | of all agents | are |
| --- | --- | --- | --- | --- | --- | -------- | ------ | ---- | --- | ----- | ------------- | --- |
rationofbeneficialfeaturesthatwerenotexplicitly removedfromtheirsystemprompts. Detaileddia-
| specifiedinrequirements. |     |     | Takingallthesefactors |     |     |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
logueanalysisshowsthatassigninga"preferGUI
together,wepositthatthefundamentalcharacter-
design"roletoaprogrammerresultsingenerated
istics of multi-agent software development take sourcecodewithrelevantGUIimplementations;in
ongreatersignificance,surpassingshort-termcon-
theabsenceofsuchroleindications,itdefaultsto
cernsliketimeandeconomiccostsinthecurrent
implementunfriendcommand-line-onlyprograms
landscape.
only. Likewise,assigningrolessuchasa"careful
reviewerforbugdetection"enhancesthechances
4.2 AblationStudy
|      |         |          |                |     |          | of discovering |          | code  | vulnerabilities; |             | without | such |
| ---- | ------- | -------- | -------------- | --- | -------- | -------------- | -------- | ----- | ---------------- | ----------- | ------- | ---- |
| This | section | examines | key components |     | or mech- |                |          |       |                  |             |         |      |
|      |         |          |                |     |          | roles,         | feedback | tends | to be            | high-level, | leading | to   |
anismswithinourmulti-agentcooperationframe- limitedadjustmentsbytheprogrammer. Thisfind-
work by removing particular phases in the chat ingunderscorestheimportanceofassigningroles
chain,communicativedehallucination,ortheroles
inelicitingresponsesfromLLMs,underscoringthe
| assignedtoallagentsintheirsystemprompts. |     |     |     |     | Fig- |     |     |     |     |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
significantinfluenceofmulti-agentcooperationon
| ure4showsthatthecodecompletephaseenhances |     |     |     |     |     | softwarequality. |     |     |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- |
Completeness,withtestingcriticalforExecutabil-
ity. Qualitysteadilyriseswitheachstep,suggesting
4.3 CommunicationAnalysis
thatsoftwaredevelopmentoptimizationisprogres-
Ouragent-drivensoftwaredevelopmentparadigm
| sively | attained | through | multi-phase |     | communica- |     |     |     |     |     |     |     |
| ------ | -------- | ------- | ----------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
promotescooperativeagentsthrougheffectivecom-
3Forfairness,GPT-4’sevaluationmitigatedpossiblepo- munication for automated solution optimization.
sitionalbias(Wangetal.,2023c),andhumanexpertsinde-
Phasesinthechatchainhavevaryinglevelsofen-
pendentlyassessedthetasksolutions,randomizedtoprevent
| orderbias. |     |     |     |     |     | gagementinnaturalandprogramminglanguages. |     |     |     |     |     |     |
| ---------- | --- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | --- |

|     |     | Modules Not Imported | Method Not Implemented | Method Not Implemented |     |
| --- | --- | -------------------- | ---------------------- | ---------------------- | --- |
Modules Not Imported
|     |     | Method Not Implemented | Modules Not Imported |     |     |
| --- | --- | ---------------------- | -------------------- | --- | --- |
Input Output
Missing Code Segments
Missing Code Segments
Missing Code Segments
|     |     |     | No Further Suggestions | No Further Suggestions |     |
| --- | --- | --- | ---------------------- | ---------------------- | --- |
Not Configure Layout
|     |     |     | Not Configure Layout | Missing Comments |     |
| --- | --- | --- | -------------------- | ---------------- | --- |
Missing Initialization
|     |     | Class Not Used     | Not Correctly Processing Data | Not Configure Layout          |     |
| --- | --- | ------------------ | ----------------------------- | ----------------------------- | --- |
|     |     | Missing Comments   | Missing Comments              | Not Correctly Processing Data |     |
|     |     | Methods Not Called | Missing Exception Handling    | Methods Not Called            |     |
|     |     | Missing Files      | Missing Files                 |                               |     |
Missing Files
|     |     | Missing Exception Handling | Missing Initialization | Missing Exception Handling |     |
| --- | --- | -------------------------- | ---------------------- | -------------------------- | --- |
Missing Imports
|     |     | No Further Suggestions            |                                   | Class Not Used                    |     |
| --- | --- | --------------------------------- | --------------------------------- | --------------------------------- | --- |
|     |     | Not Correctly Processing Data     | Calling without Correct Arguments | Missing Imports                   |     |
|     |     | Calling without Correct Arguments | Methods Not Called                | Calling without Correct Arguments |     |
|     |     | Class Defined Twice               | Class Not Used                    | Missing Initialization            |     |
|     |     |                                   | Class Defined Twice               | Not Handle Cases                  |     |
Not Handle Cases
|     |     | Missing Imports | Not Handle Cases | Class Defined Twice |     |
| --- | --- | --------------- | ---------------- | ------------------- | --- |
Figure4: Thechartdemonstratesthedistributionofsuggestionsmadebyarevieweragentduringamulti-round
reviewingprocess,whereeachsectorinthechartrepresentsadifferentcategoryofsuggestion.
We now analyze the content of their communica- andtheuseof"placeholder"tagsinPythoncode,
tionstounderstandlinguisticeffects. necessitatingadditionalmanualadjustments. Fur-
Figure 3 depicts a communication breakdown, thermore,the"Module Not Imported"issueoften
with natural language at 57.20%. In the natural- arisesduetocodegenerationomittingcrucialde-
|     |     |     | tails. Apart | from common | problems, reviewers |
| --- | --- | --- | ------------ | ----------- | ------------------- |
languagephase(i.e.,design),naturallanguagecom-
munication plays a crucial role in the thorough oftenfocusonenhancingcoderobustnessbyiden-
design of the system, with agents autonomously tifyingrareexceptions,unusedclasses,orpotential
| discussing | and designing | aspects like target user, | infiniteloops. |     |     |
| ---------- | ------------- | ------------------------- | -------------- | --- | --- |
datamanagement,anduserinterface. Post-design
|     |     |     | Likewise, | we analyze | the tester-programmer |
| --- | --- | --- | --------- | ---------- | --------------------- |
phasesshowabalancedmixofcoding,codecom- communication during the testing phase, illus-
pletion,andtestingactivities,withmostcommuni- trating the dynamic debugging dynamics in their
cationoccurringduringcodereviews. Thistrendis multi-turn interactions with compiler feedback,
duetoagents’self-reviewsandcodefixesconsis- as depicted in Figure 5. The likelihood of
tentlypropellingsoftwaredevelopment;otherwise, successful compilation at each step is generally
progresshaltswhensuccessiveupdatesdon’tshow higher than encountering errors, with most er-
significantchanges,leadingtoanaturaldecrease rors persisting and a lower probability of trans-
incodereviewcommunications. forming into different errors. The most fre-
We explore the properties of static debugging quent error is "ModuleNotFound" (45.76%), fol-
dynamicsincodereviewsresultingfromcommu- lowedby"NameError"and"ImportError"(each
nication between reviewers and programmers, as at15.25%). Theobservationhighlightsthemodel’s
depicted in Figure 4. The data uncovers that dur- tendency to overlook basic elements like an "im-
ingthereviewphase,reviewersmayspotdifferent port"statement,underscoringitsdifficultyinman-
issuesthroughlanguageinteractions. Theprogram- agingintricatedetailsduringcodegeneration. Be-
mer’sinterventioncantransformcertainissuesinto sides, the tester also detects rarer errors like im-
different ones or a state where no further sugges- properlyinitializedGUIs,incorrectmethodcalls,
tionsareneeded;theincreasingproportionofthe missing file dependencies, and unused modules.
latter indicates successful software optimization. Thecommunicativedehallucinationmechanismef-
Particularly, the "Method Not Implemented" is- fectivelyresolvescertainerrors,frequentlyresult-
sue is most common in communication between ing in "compilation success" after code changes.
reviewersandprogrammersduringcodereviews, There’sasignificantlylowchanceofreturningto
accountingfor34.85%ofdiscussions. Thisprob- anerrorstatefromasuccessfulcompilation. Over
lemusuallyarisesfromuncleartextrequirements time,themulti-turncommunicationprocessstatisti-

|     |     |     | Success |     |     | Success |     | Success |     |     |     |     |
| --- | --- | --- | ------- | --- | --- | ------- | --- | ------- | --- | --- | --- | --- |
Success
| Input |     |     |                     |     |     |                     |     |                     |     |                     | Output |     |
| ----- | --- | --- | ------------------- | --- | --- | ------------------- | --- | ------------------- | --- | ------------------- | ------ | --- |
|       |     |     | ModuleNotFoundError |     |     | ModuleNotFoundError |     | ModuleNotFoundError |     |                     |        |     |
|       |     |     | EOFError            |     |     | EOFError            |     | EOFError            |     |                     |        |     |
|       |     |     | KeyError            |     |     | KeyError            |     | KeyError            |     | ModuleNotFoundError |        |     |
|       |     |     | SSLError            |     |     | SSLError            |     | SSLError            |     |                     |        |     |
NameError
|     |     |     | NameError |     |     | NameError |     | NameError |     | SyntaxError |     |     |
| --- | --- | --- | --------- | --- | --- | --------- | --- | --------- | --- | ----------- | --- | --- |
|     |     |     | TclError  |     |     | TclError  |     | TclError  |     | ImportError |     |     |
ImportError
|     |     |     |                   |     |     | ImportError       |     | ImportError       |     | AttributeError    |     |     |
| --- | --- | --- | ----------------- | --- | --- | ----------------- | --- | ----------------- | --- | ----------------- | --- | --- |
|     |     |     | AttributeError    |     |     | AttributeError    |     | AttributeError    |     | TclError          |     |     |
|     |     |     | JSONDecodeError   |     |     | JSONDecodeError   |     | JSONDecodeError   |     | JSONDecodeError   |     |     |
|     |     |     | Others            |     |     | Others            |     | Others            |     | Others            |     |     |
|     |     |     | SyntaxError       |     |     | SyntaxError       |     | SyntaxError       |     | FileNotFoundError |     |     |
|     |     |     | FileNotFoundError |     |     | FileNotFoundError |     | FileNotFoundError |     | IndentationError  |     |     |
|     |     |     | IndentationError  |     |     | IndentationError  |     | IndentationError  |     | TypeError         |     |     |
|     |     |     | TypeError         |     |     | TypeError         |     | TypeError         |     | DatabaseError     |     |     |
|     |     |     | DatabaseError     |     |     | DatabaseError     |     | DatabaseError     |     | OperationalError  |     |     |
|     |     |     | OperationalError  |     |     | OperationalError  |     | OperationalError  |     | RuntimeError      |     |     |
|     |     |     | RuntimeError      |     |     | RuntimeError      |     | RuntimeError      |     | ValueError        |     |     |
|     |     |     | ValueError        |     |     | ValueError        |     | ValueError        |     |                   |     |     |
Figure5: Thediagramillustratestheprogressionofiterationsinamulti-roundtestingprocess,whereeachcolored
columnrepresentsadialogueround,showcasingtheevolutionofthesolutionthroughsuccessivestagesoftesting.
callyshowsaconsistentdecreaseinerrors,steadily tions;ininformationmanagementsystems,agents
movingtowardssuccessfulsoftwareexecution. mightretrievestatickey-valueplaceholdersinstead
|              |     |     |     |     |     |     | of external                                | databases. | Therefore, | it  | is crucial | to   |
| ------------ | --- | --- | --- | --- | --- | --- | ------------------------------------------ | ---------- | ---------- | --- | ---------- | ---- |
| 5 Conclusion |     |     |     |     |     |     | clearlydefinedetailedsoftwarerequirements. |            |            |     |            | Cur- |
rently,thesetechnologiesaremoresuitableforpro-
WehaveintroducedChatDev,aninnovativemulti-
totypesystemsratherthancomplexreal-worldap-
agentcollaborationframeworkforsoftwaredevel-
|     |     |     |     |     |     |     | plications. | Secondly, | unlike | traditional | function- |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --------- | ------ | ----------- | --------- | --- |
opmentthatutilizesmultipleLLM-poweredagents
levelcodegeneration,automatingtheevaluationof
| to integrate | fragmented |     | phases        | of  | the waterfall |     |                                         |              |         |          |          |       |
| ------------ | ---------- | --- | ------------- | --- | ------------- | --- | --------------------------------------- | ------------ | ------- | -------- | -------- | ----- |
|              |            |     |               |     |               |     | general-purposesoftwareishighlycomplex. |              |         |          |          | While |
| model into   | a cohesive |     | communication |     | system.       | It  |                                         |              |         |          |          |       |
|              |            |     |               |     |               |     | some                                    | efforts have | focused | on Human | Revision |       |
featureschatchainorganizingcommunicationtar-
|     |     |     |     |     |     |     | Cost | (Hong et al., 2023), |     | manual verification |     | for |
| --- | --- | --- | --- | --- | --- | --- | ---- | -------------------- | --- | ------------------- | --- | --- |
getsanddehallucinationforresolvingcodinghal-
|              |                                     |     |     |     |     |     | largedatasetsisimpractical. |     |     | Ourpaperemphasizes |     |     |
| ------------ | ----------------------------------- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | ------------------ | --- | --- |
| lucinations. | Theresultsdemonstrateitssuperiority |     |     |     |     |     |                             |     |     |                    |     |     |
completeness,executability,consistency,andover-
andhighlightthebenefitsofmulti-turncommuni-
allquality,butfutureresearchshouldconsiderad-
| cations | in software | optimization. |     | We  | aim | for the |     |     |     |     |     |     |
| ------- | ----------- | ------------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
ditionalfactorssuchasfunctionalities,robustness,
insightstoadvanceLLMagentstowardsincreased
|          |                |     |     |          |         |     | safety,anduser-friendliness. |             |     | Thirdly,comparedto |     |         |
| -------- | -------------- | --- | --- | -------- | ------- | --- | ---------------------------- | ----------- | --- | ------------------ | --- | ------- |
| autonomy | and illuminate |     | the | profound | effects | of  |                              |             |     |                    |     |         |
|          |                |     |     |          |         |     | single-agent                 | approaches, |     | multiple agents    |     | require |
"language"anditsempoweringroleacrossaneven
moretokensandtime,increasingcomputationalde-
broaderspectrumofapplications.
|               |     |     |     |     |     |     | mandsandenvironmentalimpact.                 |                                   |     | Futureresearch |     |     |
| ------------- | --- | --- | --- | --- | --- | --- | -------------------------------------------- | --------------------------------- | --- | -------------- | --- | --- |
| 6 Limitations |     |     |     |     |     |     | shouldaimtoenhanceagentcapabilitieswithfewer |                                   |     |                |     |     |
|               |     |     |     |     |     |     | interactions.                                | Despitetheselimitations,webelieve |     |                |     |     |
Our study explores the potential of cooperative thatengagingabroader,technicallyproficientau-
autonomousagentsinsoftwaredevelopment,but
diencecanunlockadditionalpotentialdirectionsin
certainlimitationsandrisksmustbeconsideredby LLM-poweredmulti-agentcollaboration.
| researchersandpractitioners.               |                |     |       | Firstly,thecapabili- |         |     |                 |     |     |     |     |     |
| ------------------------------------------ | -------------- | --- | ----- | -------------------- | ------- | --- | --------------- | --- | --- | --- | --- | --- |
| tiesofautonomousagentsinsoftwareproduction |                |     |       |                      |         |     | Acknowledgments |     |     |     |     |     |
| might be                                   | overestimated. |     | While | they                 | enhance | de- |                 |     |     |     |     |     |
velopmentquality,agentsoftenimplementsimple TheworkwassupportedbytheNationalKeyR&D
logic,resultinginlowinformationdensity. With- ProgramofChina(No.2022ZD0116312),thePost-
outclear,detailedrequirements,agentsstruggleto doctoralFellowshipProgramofCPSFunderGrant
grasptaskideas. Forinstance,vagueguidelinesin NumberGZB20230348,andTencentRhino-Bird
developingaSnakegameleadtobasicrepresenta- FocusedResearchProgram.

References
|     |     |     |     |     |     | CollaborativeFrameworkforGameDevelopment. |     |     |     |     |     | In  |
| --- | --- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- | --- | --- |
arXivpreprintarXiv:2310.08067.
| Silvia T Acuna, | Natalia | Juristo, | and | Ana | M Moreno. |     |     |     |     |     |     |     |
| --------------- | ------- | -------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
2006. EmphasizingHumanCapabilitiesinSoftware
MarkChen,JerryTworek,HeewooJun,QimingYuan,
| Development. | InIEEESoftware,volume23,pages |     |     |     |     |          |       |     |          |        |       |         |
| ------------ | ----------------------------- | --- | --- | --- | --- | -------- | ----- | --- | -------- | ------ | ----- | ------- |
|              |                               |     |     |     |     | Henrique | Ponde | de  | Oliveira | Pinto, | Jared | Kaplan, |
94–101.
HarriEdwards,YuriBurda,NicholasJoseph,Greg
|                 |     |          |       |       |        | Brockman,                 |     | et al. 2021. |     | Evaluating | Large           | Lan- |
| --------------- | --- | -------- | ----- | ----- | ------ | ------------------------- | --- | ------------ | --- | ---------- | --------------- | ---- |
| Mansi Agnihotri | and | Anuradha | Chug. | 2020. | A Sys- |                           |     |              |     |            |                 |      |
|                 |     |          |       |       |        | guageModelsTrainedonCode. |     |              |     |            | InarXivpreprint |      |
tematicLiteratureSurveyofSoftwareMetrics,Code
| SmellsandRefactoringTechniques. |     |     |     | Inbooktitleof |     | arXiv:2107.03374. |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | ------------- | --- | ----------------- | --- | --- | --- | --- | --- | --- |
InformationProcessingSystems,volume16,pages
|     |     |     |     |     |     | Weize Chen, | Yusheng |     | Su, Jingwei | Zuo, | Cheng | Yang, |
| --- | --- | --- | --- | --- | --- | ----------- | ------- | --- | ----------- | ---- | ----- | ----- |
915–934.
ChenfeiYuan,ChenQian,Chi-MinChan,YujiaQin,
RajivDBanker,GordonBDavis,andSandraASlaugh- Yaxi Lu, Ruobing Xie, et al. 2023b. AgentVerse:
ter.1998. SoftwareDevelopmentPractices,Software Facilitating Multi-agent Collaboration and Explor-
Complexity,andSoftwareMaintenancePerformance: ingEmergentBehaviorsinAgents. InInternational
AFieldStudy. InManagementscience,volume44, ConferenceonLearningRepresentations(ICLR).
pages433–450.
RoiCohen,MayHamri,MorGeva,andAmirGlober-
| Victor R Basili. | 1989. |     | Software | Development: | A   |            |     |       |     |           |         |     |
| ---------------- | ----- | --- | -------- | ------------ | --- | ---------- | --- | ----- | --- | --------- | ------- | --- |
|                  |       |     |          |              |     | son. 2023. |     | LM vs | LM: | Detecting | Factual | Er- |
ParadigmforTheFuture. InProceedingsoftheAn- rors via Cross Examination. In ArXiv, volume
| nualInternationalComputerSoftwareandApplica- |     |     |     |     |     | abs/2305.13281. |     |     |     |     |     |     |
| -------------------------------------------- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- | --- |
tionsConference,pages471–485.IEEE.
|     |     |     |     |     |     | Shehzaad | Dhuliawala, |     | Mojtaba | Komeili, |     | Jing Xu, |
| --- | --- | --- | --- | --- | --- | -------- | ----------- | --- | ------- | -------- | --- | -------- |
ThorstenBrants,AshokCPopat,PengXu,FranzJOch,
|                      |              |     |                       |     |             | Roberta           | Raileanu, | Xian | Li,                          | Asli | Celikyilmaz, | and |
| -------------------- | ------------ | --- | --------------------- | --- | ----------- | ----------------- | --------- | ---- | ---------------------------- | ---- | ------------ | --- |
| andJeffreyDean.2007. |              |     | LargeLanguageModelsin |     |             |                   |           |      |                              |      |              |     |
|                      |              |     |                       |     |             | JasonWeston.2023. |           |      | Chain-of-VerificationReduces |      |              |     |
| Machine              | Translation. |     | In Proceedings        |     | of the 2007 |                   |           |      |                              |      |              |     |
InarXiv
HallucinationinLargeLanguageModels.
JointConferenceonEmpiricalMethodsinNatural
preprintarXiv:2309.11495.
| Language | Processing |                | and Computational |     | Natural   |     |     |     |     |     |     |     |
| -------- | ---------- | -------------- | ----------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
| Language | Learning   | (EMNLP-CoNLL), |                   |     | pages858– |     |     |     |     |     |     |     |
ShiyingDing,XinyiChen,YanFang,WenruiLiu,Yiwu
867.
|     |     |     |     |     |     | Qiu, and | Chunlei | Chai. | 2023. | DesignGPT: |     | Multi- |
| --- | --- | --- | --- | --- | --- | -------- | ------- | ----- | ----- | ---------- | --- | ------ |
Tom Brown, Benjamin Mann, Nick Ryder, Melanie Agent Collaboration in Design. In arXiv preprint
| Subbiah,JaredDKaplan,PrafullaDhariwal,Arvind |     |     |     |     |     | arXiv:2311.11591. |     |     |     |     |     |     |
| -------------------------------------------- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- |
Neelakantan,PranavShyam,GirishSastry,Amanda
Askell, Sandhini Agarwal, Ariel Herbert-Voss, Michael D. Ernst. 2017. Natural Language is a Pro-
Gretchen Krueger, Tom Henighan, Rewon Child, gramming Language: Applying Natural Language
AdityaRamesh,DanielZiegler,JeffreyWu,Clemens ProcessingtoSoftwareDevelopment. InAdvances
Winter, Chris Hesse, Mark Chen, Eric Sigler, Ma- in Programming Languages (SNAPL), volume 71,
pages4:1–4:14.
| teusz Litwin,             | Scott | Gray, | Benjamin       |     | Chess, Jack |     |     |     |     |     |     |     |
| ------------------------- | ----- | ----- | -------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
| Clark, ChristopherBerner, |       |       | SamMcCandlish, |     | Alec        |     |     |     |     |     |     |     |
Radford, Ilya Sutskever, and Dario Amodei. 2020. Saad Ezzini, Sallam Abualhaija, Chetan Arora, and
Language Models are Few-Shot Learners. In Ad- Mehrdad Sabetzadeh. 2022. Automated Handling
vances in Neural Information Processing Systems ofAnaphoricAmbiguityinRequirements: AMulti-
(NeurIPS),volume33,pages1877–1901. solutionStudy. InInternationalConferenceonSoft-
wareEngineering(ICSE),pages187–199.
| Sébastien Bubeck, |     | Varun | Chandrasekaran, |     | Ronen El- |     |     |     |     |     |     |     |
| ----------------- | --- | ----- | --------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
dan,JohannesGehrke,EricHorvitz,EceKamar,Pe- Robert France and Bernhard Rumpe. 2007. Model-
ter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, driven Development of Complex Software: A Re-
HarshaNori,HamidPalangi,MarcoTulioRibeiro,
|                  |     |                              |     |     |     | searchRoadmap. |     | InFutureofSoftwareEngineering |     |     |     |     |
| ---------------- | --- | ---------------------------- | --- | --- | --- | -------------- | --- | ----------------------------- | --- | --- | --- | --- |
| andYiZhang.2023. |     | Sparksofartificialgeneralin- |     |     |     |                |     |                               |     |     |     |     |
(FOSE),pages37–54.
| telligence: | Earlyexperimentswithgpt-4. |     |     |     | InarXiv |     |     |     |     |     |     |     |
| ----------- | -------------------------- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
preprintarXiv:2303.12712. Peter Freeman, Donald J. Bagert, Hossein Saiedian,
MaryShaw,RobertDupuis,andJ.BarrieThompson.
| TianleCai, XuezhiWang, |                                  |     | TengyuMa,             | XinyunChen, |     |           |          |                |     |      |                   |     |
| ---------------------- | -------------------------------- | --- | --------------------- | ----------- | --- | --------- | -------- | -------------- | --- | ---- | ----------------- | --- |
|                        |                                  |     |                       |             |     | 2001.     | Software | Engineering    |     | Body | of Knowledge      |     |
| andDennyZhou.2023.     |                                  |     | LargeLanguageModelsas |             |     |           |          |                |     |      |                   |     |
|                        |                                  |     |                       |             |     | (SWEBOK). |          | In Proceedings |     | of   | the International |     |
| ToolMakers.            | InarXivpreprintarXiv:2305.17126. |     |                       |             |     |           |          |                |     |      |                   |     |
ConferenceonSoftwareEngineering(ICSE),pages
693–696.
Chi-MinChan,WeizeChen,YushengSu,JianxuanYu,
| Wei Xue, | Shanghang | Zhang, | Jie | Fu, and | Zhiyuan |     |     |     |     |     |     |     |
| -------- | --------- | ------ | --- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- |
Liu. 2023. ChatEval: Towards Better LLM-based SaGao,ChunyangChen,ZhenchangXing,YukunMa,
|            |         |             |     |         |          | Wen Song, | and | Shang-Wei |     | Lin. | 2019. | A Neural |
| ---------- | ------- | ----------- | --- | ------- | -------- | --------- | --- | --------- | --- | ---- | ----- | -------- |
| Evaluators | through | Multi-Agent |     | Debate. | In arXiv |           |     |           |     |      |       |          |
ModelforMethodNameGenerationfromFunctional
preprintarXiv:2308.07201.
|     |     |     |     |     |     | Description. |     | In26thIEEEInternationalConference |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------ | --- | --------------------------------- | --- | --- | --- | --- |
Dake Chen, Hanbin Wang, Yunhao Huo, Yuzhao Li, onSoftwareAnalysis,EvolutionandReengineering
andHaoyangZhang.2023a. GameGPT:Multi-agent (SANER),pages411–421.

SiruiHong,MingchenZhuge,JonathanChen,Xiawu ErikNijkamp,BoPang,HiroakiHayashi,LifuTu,Huan
Zheng,YuhengCheng,CeyaoZhang,JinlinWang, Wang,YingboZhou,SilvioSavarese,andCaiming
ZiliWang,StevenKaShingYau,ZijuanLin,Liyang Xiong.2023. CodeGen: AnOpenLargeLanguage
Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, Model for Code with Multi-Turn Program Synthe-
andJürgenSchmidhuber.2023. MetaGPT:MetaPro- sis. In The International Conference on Learning
grammingforAMulti-AgentCollaborativeFrame- Representations(ICLR).
work. InInternationalConferenceonLearningRep-
| resentations(ICLR). |     |     |     |     |     |     | Anton Osika. |     | 2023. | GPT-Engineer. |     |     | In  |
| ------------------- | --- | --- | --- | --- | --- | --- | ------------ | --- | ----- | ------------- | --- | --- | --- |
https://github.com/AntonOsika/gpt-engineer.
| Wenyue   | Hua, | Lizhou    | Fan, | Lingyao | Li, Kai   | Mei, |              |      |     |           |       |          |     |
| -------- | ---- | --------- | ---- | ------- | --------- | ---- | ------------ | ---- | --- | --------- | ----- | -------- | --- |
| Jianchao | Ji,  | Yingqiang | Ge,  | Libby   | Hemphill, | and  |              |      |     |           |       |          |     |
|          |      |           |      |         |           |      | Long Ouyang, | Jeff | Wu, | Xu Jiang, | Diogo | Almeida, |     |
Yongfeng Zhang. 2023. War and Peace (WarA- Carroll L. Wainwright, Pamela Mishkin, Chong
gent): Large Language Model-based Multi-Agent Zhang, Sandhini Agarwal, Katarina Slama, Alex
Simulation of World Wars. In arXiv preprint Ray, John Schulman, Jacob Hilton, Fraser Kelton,
arXiv:2311.17227.
|     |     |     |     |     |     |     | Luke Miller, | Maddie | Simens, |     | Amanda | Askell, | Pe- |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ------ | ------- | --- | ------ | ------- | --- |
terWelinder,PaulChristiano,JanLeike,andRyan
ZiweiJi,NayeonLee,RitaFrieske,TiezhengYu,Dan
|     |     |     |     |     |     |     | Lowe.2022. | TrainingLanguageModelstoFollow |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------------------------------ | --- | --- | --- | --- | --- |
Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea InstructionswithHumanFeedback. InarXivpreprint
| Madotto,                               | and | Pascale | Fung. | 2023. | Survey | of Hal- | arXiv:2203.02155. |     |     |     |     |     |     |
| -------------------------------------- | --- | ------- | ----- | ----- | ------ | ------- | ----------------- | --- | --- | --- | --- | --- | --- |
| lucinationinNaturalLanguageGeneration. |     |         |       |       |        | InACM   |                   |     |     |     |     |     |     |
ComputingSurveys,volume55,pages1–38.
JoonSungPark,JosephO’Brien,CarrieJunCai,Mered-
ithRingelMorris,PercyLiang,andMichaelS.Bern-
JaredKaplan,SamMcCandlish,TomHenighan,TomB.
|     |     |     |     |     |     |     | stein. 2023. | Generative |     | Agents: | Interactive |     | Simu- |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ---------- | --- | ------- | ----------- | --- | ----- |
Brown,BenjaminChess,RewonChild,ScottGray, lacraofHumanBehavior. InProceedingsofthe36th
AlecRadford,JeffreyWu,andDarioAmodei.2020. AnnualACMSymposiumonUserInterfaceSoftware
| ScalingLawsforNeuralLanguageModels. |     |     |     |     |     | InarXiv |     |     |     |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
andTechnology(UIST).
preprintarXiv:2001.08361.
FlorianPudlitz,FlorianBrokhausen,andAndreasVo-
| Guohao | Li, Hasan                          | Abed        | Al  | Kader Hammoud, |         | Hani |                              |       |            |     |                |        |      |
| ------ | ---------------------------------- | ----------- | --- | -------------- | ------- | ---- | ---------------------------- | ----- | ---------- | --- | -------------- | ------ | ---- |
|        |                                    |             |     |                |         |      | gelsang.                     | 2019. | Extraction | of  | System         | States | from |
| Itani, | Dmitrii                            | Khizbullin, |     | and Bernard    | Ghanem. |      |                              |       |            |     |                |        |      |
|        |                                    |             |     |                |         |      | NaturalLanguageRequirements. |       |            |     | InIEEEInterna- |        |      |
| 2023a. | CAMEL:CommunicativeAgentsfor"Mind" |             |     |                |         |      |                              |       |            |     |                |        |      |
tionalRequirementsEngineeringConference(RE),
ExplorationofLargeScaleLanguageModelSociety.
pages211–222.
InThirty-seventhConferenceonNeuralInformation
ProcessingSystems(NeurIPS).
YujiaQin,ShihaoLiang,YiningYe,KunlunZhu,Lan
Yan,YaxiLu,YankaiLin,XinCong,XiangruTang,
| Yuan Li,    | Yixuan | Zhang,     | and | Lichao       | Sun. | 2023b. |                      |        |     |                           |        |            |     |
| ----------- | ------ | ---------- | --- | ------------ | ---- | ------ | -------------------- | ------ | --- | ------------------------- | ------ | ---------- | --- |
|             |        |            |     |              |      |        | BillQian,etal.2023a. |        |     | ToolLLM:FacilitatingLarge |        |            |     |
| MetaAgents: |        | Simulating |     | Interactions | of   | Human  |                      |        |     |                           |        |            |     |
|             |        |            |     |              |      |        | Language             | Models | to  | Master                    | 16000+ | Real-World |     |
BehaviorsforLLM-basedTask-orientedCoordina-
APIs. InarXivpreprintarXiv:2307.16789.
| tionviaCollaborativeGenerativeAgents. |     |     |     |     |     | InarXiv |     |     |     |     |     |     |     |
| ------------------------------------- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
preprintarXiv:2310.06500.
|     |     |     |     |     |     |     | Zhen Qin, | Rolf Jagerman, |     | Kai | Hui, Honglei | Zhuang, |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | -------------- | --- | --- | ------------ | ------- | --- |
Zhiwei Liu, Weiran Yao, Jianguo Zhang, Le Xue, JunruWu,JiamingShen,TianqiLiu,JialuLiu,Don-
Shelby Heinecke, Rithesh Murthy, Yihao Feng, aldMetzler,XuanhuiWang,andMichaelBendersky.
|     |     |     |     |     |     |     | 2023b. LargeLanguageModelsareEffectiveText |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | --- |
ZeyuanChen,JuanCarlosNiebles,DevanshArpit,
|     |     |     |     |     |     |     | RankerswithPairwiseRankingPrompting. |     |     |     |     | InarXiv |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | ------- | --- |
RanXu,PhilMui,HuanWang,CaimingXiong,and
preprintarXiv:2306.17563.
| SilvioSavarese.2023. |     |     | BOLAA:Benchmarkingand |     |     |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
OrchestratingLLM-augmentedAutonomousAgents.
InarXivpreprintarXiv:2308.05960. AlecRadford,JeffreyWu,RewonChild,DavidLuan,
|           |                |     |     |              |     |       | DarioAmodei,IlyaSutskever,etal.      |     |     |     | LanguageMod- |          |     |
| --------- | -------------- | --- | --- | ------------ | --- | ----- | ------------------------------------ | --- | --- | --- | ------------ | -------- | --- |
|           |                |     |     |              |     |       | elsareUnsupervisedMultitaskLearners. |     |     |     |              | InOpenAI |     |
| KaixinMa, | HongmingZhang, |     |     | HongweiWang, |     | Xiao- |                                      |     |     |     |              |          |     |
Blog,volume1,page9.
| manPan,andDongYu.2023.                      |     |     |     | LASER:LLMAgent |     |     |     |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| withState-SpaceExplorationforWebNavigation. |     |     |     |                |     | In  |     |     |     |     |     |     |     |
arXivpreprintarXiv:2309.08172. Toran Bruce Richards. 2023. AutoGPT. In
https://github.com/Significant-Gravitas/AutoGPT.
| CuauhtémocLópezMartínandAlainAbran.2015. |     |     |     |     |     | Neu- |     |     |     |     |     |     |     |
| ---------------------------------------- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
JingqingRuan,YihongChen,BinZhang,ZhiweiXu,
ralnetworksforpredictingthedurationofnewsoft-
|               |     |                                 |     |     |     |     | Tianpeng                                | Bao, | Guoqing | Du, | Shiwei | Shi, Hangyu |     |
| ------------- | --- | ------------------------------- | --- | --- | --- | --- | --------------------------------------- | ---- | ------- | --- | ------ | ----------- | --- |
| wareprojects. |     | InJ.Syst.Softw.,volume101,pages |     |     |     |     |                                         |      |         |     |        |             |     |
| 127–135.      |     |                                 |     |     |     |     | Mao,ZiyueLi,XingyuZeng,andRuiZhao.2023. |      |         |     |        |             |     |
TPTU:LargeLanguageModel-basedAIAgentsfor
Nadia Nahar, Shurui Zhou, Grace A. Lewis, and Task Planning and Tool Usage. In arXiv preprint
| ChristianKästner.2022. |     |            |     | CollaborationChallenges |            |     | arXiv:2308.03427. |     |     |     |     |     |     |
| ---------------------- | --- | ---------- | --- | ----------------------- | ---------- | --- | ----------------- | --- | --- | --- | --- | --- | --- |
| in Building            |     | ML-Enabled |     | Systems:                | Communica- |     |                   |     |     |     |     |     |     |
tion,Documentation,Engineering,andProcess. In SteveSawyerandPatriciaJ.Guinan.1998. Software
IEEE/ACM International Conference on Software development: ProcessesandPerformance. InIBM
Engineering(ICSE),pages413–425. SystemsJournal,volume37,pages552–569.

TimoSchick,JaneDwivedi-Yu,RobertoDessì,Roberta SongWang,TaiyueLiu,andLinTan.2016. Automati-
Raileanu,MariaLomeli,LukeZettlemoyer,Nicola callyLearningSemanticFeaturesforDefectPredic-
Cancedda,andThomasScialom.2023. ToolFormer: tion. InProceedingsoftheInternationalConference
Language Models Can Teach Themselves to Use onSoftwareEngineering(ICSE),pages297–308.
Tools. InarXivpreprintarXiv:2302.04761.
SongWang,NishthaShrestha,AbarnaKucheriSubbu-
MurrayShanahan,KyleMcDonell,andLariaReynolds.
|       |                                  |     |     |     |     |     | raman,    | Junjie | Wang,     | Moshi | Wei, and  | Nachiappan |
| ----- | -------------------------------- | --- | --- | --- | --- | --- | --------- | ------ | --------- | ----- | --------- | ---------- |
| 2023. | RolePlaywithLargeLanguageModels. |     |     |     |     | In  |           |        |           |       |           |            |
|       |                                  |     |     |     |     |     | Nagappan. | 2021.  | Automatic |       | Unit Test | Generation |
Nature,volume623,pages493–498. forMachineLearningLibraries: HowFarAreWe?
InIEEE/ACMInternationalConferenceonSoftware
TheodoreR.Sumers,ShunyuYao,KarthikNarasimhan,
Engineering(ICSE),pages1548–1560.
| and Thomas |     | L. Griffiths. | 2023. | Cognitive |     | Archi- |     |     |     |     |     |     |
| ---------- | --- | ------------- | ----- | --------- | --- | ------ | --- | --- | --- | --- | --- | --- |
tectures for Language Agents. In arXiv preprint XinyuanWang,ChenxiLi,ZhenWang,FanBai,Hao-
arXiv:2309.02427.
tianLuo,JiayouZhang,NebojsaJojic,EricP.Xing,
|     |     |     |     |     |     |     | and Zhiting | Hu. | 2023d. | PromptAgent: |     | Strategic |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------ | ------------ | --- | --------- |
HannesThaller,LukasLinsbauer,andAlexanderEgyed.
|                |              |            |                         |     |            |     | Planning     | with | Language      | Models | Enables  | Expert-  |
| -------------- | ------------ | ---------- | ----------------------- | --- | ---------- | --- | ------------ | ---- | ------------- | ------ | -------- | -------- |
| 2019.          | FeatureMaps: |            | AComprehensibleSoftware |     |            |     |              |      |               |        |          |          |
|                |              |            |                         |     |            |     | level Prompt |      | Optimization. |        | In arXiv | preprint |
| Representation |              | for Design | Pattern                 |     | Detection. | In  |              |      |               |        |          |          |
arXiv:2310.16427.
| IEEE | International | Conference |     | on  | Software | Anal- |     |     |     |     |     |     |
| ---- | ------------- | ---------- | --- | --- | -------- | ----- | --- | --- | --- | --- | --- | --- |
ysis,EvolutionandReengineering(SANER),pages
|          |     |     |     |     |     |     | Zhilin Wang, | Yu              | Ying | Chiu,                 | and Yu Cheung | Chiu. |
| -------- | --- | --- | --- | --- | --- | --- | ------------ | --------------- | ---- | --------------------- | ------------- | ----- |
| 207–217. |     |     |     |     |     |     | 2023e.       | HumanoidAgents: |      | PlatformforSimulating |               |       |
HugoTouvron,ThibautLavril,GautierIzacard,Xavier Human-like Generative Agents. In arXiv preprint
arXiv:2310.05418.
Martinet,Marie-AnneLachaux,TimothéeLacroix,
BaptisteRozière,NamanGoyal,EricHambro,Faisal
|            |          |              |         |      |                |     | Jason Wei,   | Yi Tay, | Rishi     | Bommasani, |      | Colin Raffel, |
| ---------- | -------- | ------------ | ------- | ---- | -------------- | --- | ------------ | ------- | --------- | ---------- | ---- | ------------- |
| Azhar,     | et al.   | 2023. LLaMA: |         | Open | and Efficient  |     |              |         |           |            |      |               |
|            |          |              |         |      |                |     | Barret Zoph, |         | Sebastian | Borgeaud,  | Dani | Yogatama,     |
| Foundation | Language |              | Models. | In   | arXiv preprint |     |              |         |           |            |      |               |
MaartenBosma,DennyZhou,DonaldMetzler,etal.
arXiv:2302.13971.
|     |     |     |     |     |     |     | 2022a. | EmergentAbilitiesofLargeLanguageMod- |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------ | ------------------------------------ | --- | --- | --- | --- |
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob els. InarXivpreprintarXiv:2206.07682.
| Uszkoreit, | Llion | Jones, | Aidan | N Gomez, | Łukasz |     |     |     |     |     |     |     |
| ---------- | ----- | ------ | ----- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- |
JasonWei,XuezhiWang,DaleSchuurmans,Maarten
| Kaiser,andIlliaPolosukhin.2017. |     |     |     |     | AttentionisAll |     |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
Bosma,FeiXia,EdChi,QuocVLe,DennyZhou,
| YouNeed. | InAdvancesinNeuralInformationPro- |     |     |     |     |     |               |     |                  |     |           |         |
| -------- | --------------------------------- | --- | --- | --- | --- | --- | ------------- | --- | ---------------- | --- | --------- | ------- |
|          |                                   |     |     |     |     |     | et al. 2022b. |     | Chain-of-Thought |     | Prompting | Elicits |
cessingSystems(NeurIPS),volume30.
|     |     |     |     |     |     |     | ReasoninginLargeLanguageModels. |     |     |     |     | InAdvances |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | ---------- |
inNeuralInformationProcessingSystems(NeurIPS),
| Chengcheng | Wan, | Shicheng | Liu, | Sophie | Xie, | Yifan |     |     |     |     |     |     |
| ---------- | ---- | -------- | ---- | ------ | ---- | ----- | --- | --- | --- | --- | --- | --- |
Liu,HenryHoffmann,MichaelMaire,andShanLu. volume35,pages24824–24837.
2022. AutomatedTestingofSoftwarethatUsesMa-
chine Learning APIs. In IEEE/ACM International LilianWeng.2023. LLM-poweredAutonomousAgents.
ConferenceonSoftwareEngineering(ICSE),pages Inlilianweng.github.io.
212–224.
|     |     |     |     |     |     |     | Jonas Winkler, | Jannis | Grönberg, |     | and Andreas | Vogel- |
| --- | --- | --- | --- | --- | --- | --- | -------------- | ------ | --------- | --- | ----------- | ------ |
Yao Wan, Zhou Zhao, Min Yang, Guandong Xu, sang.2020. PredictingHowtoTestRequirements:
|                                        |     |     |     |     |     |     | AnAutomatedApproach. |     |     | InSoftwareEngineering, |     |     |
| -------------------------------------- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | ---------------------- | --- | --- |
| HaochaoYing,JianWu,andPhilipS.Yu.2018. |     |     |     |     |     | Im- |                      |     |     |                        |     |     |
volumeP-300ofLNI,pages141–142.
provingAutomaticSourceCodeSummarizationvia
| DeepReinforcementLearning. |     |     |     | InProceedingsofthe |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
ChengrunYang,XuezhiWang,YifengLu,HanxiaoLiu,
ACM/IEEEInternationalConferenceonAutomated
SoftwareEngineering(ASE),pages397–407. QuocV.Le,DennyZhou,andXinyunChen.2023a.
|     |     |     |     |     |     |     | Large Language |     | Models | as  | Optimizers. | In arXiv |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------ | --- | ----------- | -------- |
Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Man- preprintarXiv:2309.03409.
dlekar,ChaoweiXiao,YukeZhu,LinxiFan,andAn-
imaAnandkumar.2023a. Voyager: AnOpen-ended Rui Yang, Lin Song, Yanwei Li, Sijie Zhao, Yixiao
|                                       |     |     |     |     |     |     | Ge, Xiu  | Li, and | Ying     | Shan. | 2023b. | GPT4Tools: |
| ------------------------------------- | --- | --- | --- | --- | --- | --- | -------- | ------- | -------- | ----- | ------ | ---------- |
| EmbodiedAgentwithLargeLanguageModels. |     |     |     |     |     | In  |          |         |          |       |        |            |
|                                       |     |     |     |     |     |     | Teaching | Large   | Language | Model | to Use | Tools via  |
arXivpreprintarXiv:2305.16291.
|     |     |     |     |     |     |     | Self-instruction. |     | InAdvancesinNeuralInformation |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | ----------------------------- | --- | --- | --- |
Lei Wang, Jingsen Zhang, Hao Yang, Zhiyuan Chen, ProcessingSystems(NeurIPS).
JiakaiTang,ZeyuZhang,XuChen,YankaiLin,Rui-
huaSong,WayneXinZhao,JunXu,ZhichengDou, MuratYilmaz,RoryVO’Connor,andPaulClarke.2012.
Jun Wang, and Ji-Rong Wen. 2023b. When Large ASystematicApproachtotheComparisonofRoles
LanguageModelbasedAgentMeetsUserBehavior in the Software Development Processes. In Inter-
Analysis: A Novel User Simulation Paradigm. In nationalConferenceonSoftwareProcessImprove-
mentandCapabilityDetermination,pages198–209.
arXivpreprintarXiv:2306.02552.
Springer.
PeiyiWang,LeiLi,LiangChen,ZefanCai,DaweiZhu,
BinghuaiLin,YunboCao,QiLiu,TianyuLiu,and ZhangyueYin,QiushiSun,ChengChang,QipengGuo,
ZhifangSui.2023c. LargeLanguageModelsarenot JunqiDai,XuanjingHuang,andXipengQiu.2023.
FairEvaluators. InarXivpreprintarXiv:2305.17926. Exchange-of-Thought: EnhancingLargeLanguage

ModelCapabilitiesthroughCross-ModelCommuni-
cation. In Proceedings of the 2023 Conference on
EmpiricalMethodsinNaturalLanguageProcessing
(EMNLP),pages15135–15153.
AnZhang,LehengSheng,YuxinChen,HaoLi,Yang
Deng,XiangWang,andTat-SengChua.2023a. On
Generative Agents in Recommendation. In arXiv
preprintarXiv:2310.10108.
YueZhang,YafuLi,LeyangCui,DengCai,LemaoLiu,
TingchenFu,XintingHuang,EnboZhao,YuZhang,
YulongChen, etal.2023b. Siren’sSongintheAI
Ocean: A Survey on Hallucination in Large Lan-
guageModels. InarXivpreprintarXiv:2309.01219.
Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu
Lin, Yong-Jin Liu, and Gao Huang. 2023. ExpeL:
LLM Agents Are Experiential Learners. In AAAI
ConferenceonArtificialIntelligence(AAAI).
Tianming Zhao, Chunyang Chen, Yuanning Liu, and
XiaodongZhu.2021. GUIGAN:LearningtoGener-
ateGUIDesignsUsingGenerativeAdversarialNet-
works. InIEEE/ACMInternationalConferenceon
SoftwareEngineering(ICSE),pages748–760.
Shuyan Zhou, Frank F Xu, Hao Zhu, Xuhui Zhou,
RobertLo,AbishekSridhar,XianyiCheng,Yonatan
Bisk, Daniel Fried, Uri Alon, et al. 2023a. We-
bArena: A Realistic Web Environment for Build-
ing Autonomous Agents. In arXiv preprint
arXiv:2307.13854.
Wangchunshu Zhou, Yuchen Eleanor Jiang, Long Li,
JialongWu,TiannanWang,ShiQiu,JintianZhang,
JingChen,RuipuWu,ShuaiWang,ShidingZhu,Jiyu
Chen,WentaoZhang,NingyuZhang,HuajunChen,
PengCui,andMrinmayaSachan.2023b. Agents:An
Open-sourceFrameworkforAutonomousLanguage
Agents. InarXivpreprintarXiv:2309.07870.