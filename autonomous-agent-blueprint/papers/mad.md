|     | Encouraging   |     |          | Divergent  |             | Thinking       |             | in Large | Language    |     | Models   |     |
| --- | ------------- | --- | -------- | ---------- | ----------- | -------------- | ----------- | -------- | ----------- | --- | -------- | --- |
|     |               |     |          |            | through     | Multi-Agent    |             |          | Debate      |     |          |     |
|     | TianLiang1,3* |     |          | ZhiweiHe2* |             | WenxiangJiao3* |             |          | XingWang3†  |     | YanWang3 |     |
|     |               |     | RuiWang2 |            | YujiuYang1† |                | ShumingShi3 |          | ZhaopengTu3 |     |          |     |
1TsinghuaUniversity 2ShanghaiJiaoTongUniversity 3TencentAILab
1{liangt21@mails,yang.yujiu@sz}.tsinghua.edu.cn
2zwhe.cs@sjtu.edu.cn 3{joelwxjiao,brightxwang,zptu}@tencent.com
|     |     |     | Abstract |     |     |     |     | 1.00 |     |     |     |     |
| --- | --- | --- | -------- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
Multi-Agent Debate
Self-Reflection
|     | Modern | large | language | models | (LLMs) | like |     | tnemeergasiD .gvA |     |     |     |     |
| --- | ------ | ----- | -------- | ------ | ------ | ---- | --- | ----------------- | --- | --- | --- | --- |
0.75
ChatGPThaveshownremarkableperformance
4202 tcO 9  ]LC.sc[  4v81191.5032:viXra ongenerallanguagetasksbutstillstruggleon
0.50
complexreasoningtasks,whichdrivesthere-
searchoncognitivebehaviorsofLLMstoex-
|     | plore human-like        |            | problem-solving |                    |      | strategies. |     | 0.25 |     |     |     |     |
| --- | ----------------------- | ---------- | --------------- | ------------------ | ---- | ----------- | --- | ---- | --- | --- | --- | --- |
|     | Along this              | direction, |                 | one representative |      | strat-      |     |      |     |     |     |     |
|     | egy is self-reflection, |            |                 | which              | asks | an LLM to   |     |      |     |     |     |     |
0.00
|     | refine the | solution | with | the | feedback | gener- |     |     | 1   | 2   | 3 4 | 5   |
| --- | ---------- | -------- | ---- | --- | -------- | ------ | --- | --- | --- | --- | --- | --- |
Iteration
|     | ated by    | itself | iteratively.     | However, |         | our study |     |          |                                          |     |     |     |
| --- | ---------- | ------ | ---------------- | -------- | ------- | --------- | --- | -------- | ---------------------------------------- | --- | --- | --- |
|     |            |        |                  |          |         |           |     | Figure1: | Disagreementbetweentwoadjacentiterations |     |     |     |
|     | shows that | such   | reflection-style |          | methods | suf-      |     |          |                                          |     |     |     |
withrespecttotheiterationofdebate/self-reflection.
|     | fer from | the Degeneration-of-Thought |     |     |     | (DoT) |     |     |     |     |     |     |
| --- | -------- | --------------------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
problem: oncetheLLMhasestablishedconfi- etal.,2023)butstillstruggleoncomplexreasoning
denceinitssolutions,itisunabletogenerate
tasks(Zhuetal.,2023a;Gouetal.,2023),which
novelthoughtslaterthroughreflectionevenif drivestheresearchoncognitivebehaviorsofLLMs
|     | its initial | stance | is incorrect. |     | To  | address the |     |     |     |     |     |     |
| --- | ----------- | ------ | ------------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- |
toexplorehuman-likeproblem-solvingstrategies.
DoTproblem,weproposeaMulti-AgentDe-
Inparticular,self-reflection(Madaanetal.,2024;
|     | bate (MAD) |     | framework, | in  | which | multiple |     |     |     |     |     |     |
| --- | ---------- | --- | ---------- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- |
agentsexpresstheirargumentsinthestateof Shinnetal.,2024),aconceptthatusuallyrefersto
theprocessofintrospectionandexaminationofa
|     | “tit for | tat” and | a judge | manages |     | the debate |     |     |     |     |     |     |
| --- | -------- | -------- | ------- | ------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
processtoobtainafinalsolution. Clearly,our person’sownthoughts,hasbeenexploredtosolve
MADframeworkencouragesdivergentthink-
intricatetasksthatcouldbechallengingforazero-
inginLLMswhichwouldbehelpfulfortasks shot generation or even chain-of-thought (CoT)
|     | thatrequiredeeplevelsofcontemplation. |         |        |             |     | Ex-       |     |           |         |             |               |       |
| --- | ------------------------------------- | ------- | ------ | ----------- | --- | --------- | --- | --------- | ------- | ----------- | ------------- | ----- |
|     |                                       |         |        |             |     |           |     | prompting | (Wei et | al., 2022). | Specifically, | self- |
|     | periment                              | results | on two | challenging |     | datasets, |     |           |         |             |               |       |
reflectioninvolvesaniterativerefinementprocess
commonsensemachinetranslationandcounter-
suchthattheLLMgeneratesanewanswerbasedon
intuitivearithmeticreasoning,demonstratethe
theanswersandfeedbackinpreviousiterationsand
|     | effectivenessofourMADframework. |     |     |     |     | Exten- |     |     |     |     |     |     |
| --- | ------------------------------- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
siveanalysessuggestthattheadaptivebreakof thenprovidesfeedbackforthenewanswer. While
debateandthemodestlevelof“titfortat”state self-reflectioncanbeeffectiveincreatingbetteran-
are required for MAD to obtain good perfor- swers,itishighlydependentontheself-evaluation
mance.Moreover,wefindthatLLMsmightnot
capabilitiesofLLMs,whicharenotformallyguar-
beafairjudgeifdifferentLLMsareusedfor
anteed(Shinnetal.,2024).
|     | agents. | Codeisavailableathttps://github. |     |     |     |     |     |     |     |     |     |     |
| --- | ------- | -------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Inthiswork,wefocusontheDegeneration-of-
com/Skytliang/Multi-Agents-Debate.
Thought(DoT)probleminself-reflection,which
1 Introduction is proposed and defined by us for the first time.
Formally,DoTdescribesthefollowingscenario:
| Large | language |     | models | (LLMs) |     | have shown |     |     |     |     |     |     |
| ----- | -------- | --- | ------ | ------ | --- | ---------- | --- | --- | --- | --- | --- | --- |
remarkable performance on general language Once the LLM-based agent has estab-
tasks (Jiao et al., 2023; Wu et al., 2023; Bang lished confidence in its answers, it is
unabletogeneratenovelthoughtslater
|     | * Contributedequally. |     |     | WorkwasdonewhenTianand |     |     |     |     |     |     |     |     |
| --- | --------------------- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
throughself-reflectioneveniftheinitial
ZhiweiwereinterningatTencentAILab.
|     | † XingandYujiuareco-correspondingauthors. |     |     |     |     |     |     | stanceisincorrect. |     |     |     |     |
| --- | ----------------------------------------- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- |

Todemonstratethisproblem,weforcetheagents Translation(CommonMT)andCounter-Intuitive
toengageinadebateorself-reflectionfor5rounds ArithmeticReasoning(Counter-IntuitiveAR).The
beforereachingananswer. Next,wemanuallyde- commoncharacteristicofthetwotasksisthatour
termine the disagreement as 1 and agreement as instinctsaremostlyincorrectbasedononlythesu-
0 between two adjacent iterations. We define the perficialexpressionsofthequestions,anddeeper
averagedisagreementiniterationiasthepercent- levelsofcontemplationarerequiredforbetteran-
ageofoppositionoccurringbetweentwodebaters swers. Experimentalresultsdemonstratethatour
acrossmultipledebates(orself-conflictioninself- MAD framework outperforms the baseline meth-
reflection). We show the trends in Figure 1. The ods, especially, GPT-3.5-Turbo with MAD can
low disagreement of self-reflection suggests that surpasstheperformanceofGPT-4onCommonMT.
theLLMstickstotheincorrectanswerspredicted Thecontributionsofthisworkaresummarized
| byCoTandisunabletoengageinmeaningfulself- |     |     |     |     |     |     | asfollows: |     |     |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- |
reflection.
|       |             |         |     |              |     |       | • We propose | and   | define  | the | Degeneration-of- |     |     |
| ----- | ----------- | ------- | --- | ------------ | --- | ----- | ------------ | ----- | ------- | --- | ---------------- | --- | --- |
| There | are various | factors |     | (Bortolotti, |     | 2011; |              |       |         |     |                  |     |     |
|       |             |         |     |              |     |       | Thought      | (DoT) | problem | in  | self-reflection, |     | and |
Keestra,2017)thatcouldresultinDoT,andweout-
|                 |                                |               |     |     |         |      | address it | by proposing |     | the | Multi-Agent |           | De- |
| --------------- | ------------------------------ | ------------- | --- | --- | ------- | ---- | ---------- | ------------ | --- | --- | ----------- | --------- | --- |
| linethreehere:  | (1)BiasandDistortedPerception. |               |     |     |         |      |            |              |     |     |             |           |     |
|                 |                                |               |     |     |         |      | bate (MAD) | framework    |     | to  | explore     | divergent |     |
| Self-perception | can                            | be influenced |     | by  | biases, | pre- |            |              |     |     |             |           |     |
chain-of-thoughts.
conceivednotions,anddistortedthinkingpatterns,
whichcanbelearnedfromthemassiveamountof • We demonstrate the effectiveness of MAD
dataduringpretraining. IfanLLM’sself-reflection on two challenging tasks, and find that
iscloudedbysuchbiasesordistortedthinking,it GPT-3.5-Turbo with MAD can even surpass
GPT-4ontheCommonMTdataset.
| canleadtoinaccurateconclusionsinstinctively. |             |     |        |                 |           | (2) |                |         |     |        |       |              |          |
| -------------------------------------------- | ----------- | --- | ------ | --------------- | --------- | --- | -------------- | ------- | --- | ------ | ----- | ------------ | -------- |
| RigidityandResistancetoChange.               |             |     |        | Self-reflection |           |     |                |         |     |        |       |              |          |
|                                              |             |     |        |                 |           |     | • Experimental | results |     | show   | that  | the adaptive |          |
| often involves                               | challenging |     | one’s  | beliefs,        | assump-   |     |                |         |     |        |       |              |          |
|                                              |             |     |        |                 |           |     | break strategy | and     | the | modest | level | of           | “tit for |
| tions, and                                   | behaviors.  | If  | an LLM | is              | resistant | to  |                |         |     |        |       |              |          |
tat”statearerequiredforperformanceimprove-
changeorholdsrigidbeliefs,itmaystruggletoen-
|     |     |     |     |     |     |     | ment. In | addition, | we  | find | that | the llm-based |     |
| --- | --- | --- | --- | --- | --- | --- | -------- | --------- | --- | ---- | ---- | ------------- | --- |
gageinmeaningfulself-reflectionthatleadstobet-
|             |                             |     |     |     |     |       | judge shows | a   | preference | to  | the | side with | the |
| ----------- | --------------------------- | --- | --- | --- | --- | ----- | ----------- | --- | ---------- | --- | --- | --------- | --- |
| teranswers. | (3)LimitedExternalFeedback. |     |     |     |     | Self- |             |     |            |     |     |           |     |
sameLLMasthebackbone.
reflectionisprimarilyaninternalprocess,butexter-
nalfeedbackcanprovidevaluableperspectivesand
|     |     |     |     |     |     |     | 2 Multi-AgentDebateFramework |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- |
insights. Withoutconsideringexternalfeedback,an
Figure2illustratesthegeneralframeworkofMAD,
LLMmaymissimportantblindspotsoralternative
viewpointsthatcanenrichitsself-reflection. wheretwodebatersandajudgeareinvolvedinade-
batetoresolveamathproblemwhileself-reflection
| To address | the | DoT | issue, | we leverage |     | an- |     |     |     |     |     |     |     |
| ---------- | --- | --- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
descendsintothetrapofDoT.Generally,ourMAD
otherfundamentalcharacteristicofhumanproblem-
solving,i.e.,debate,toencouragedivergentthink- frameworkiscomposedofthreecomponentswhich
areelaboratedasfollows:
| inginLLMs. | Specifically, |     | weproposetheMAD |     |     |     |     |     |     |     |     |     |     |
| ---------- | ------------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
framework,shortforMulti-AgentDebate,where Meta Prompts. We use meta prompts to intro-
two agents express their own arguments in the ducethetopictobesolved,thenumberofdebaters,
stateof“titfortat”andajudgemonitorsandman-
|          |                |     |        |         |           |     | theiterationlimit,andotherrequirements. |     |     |     |     |     | Anex- |
| -------- | -------------- | --- | ------ | ------- | --------- | --- | --------------------------------------- | --- | --- | --- | --- | --- | ----- |
| ages the | debate process | to  | obtain | a final | solution. |     |                                         |     |     |     |     |     |       |
ampeofmetapromptsforthearithmeticreasoning
| The nature | of MAD | determines |     | that | (1) The | dis- | taskinFigure2is: |     |     |     |     |     |     |
| ---------- | ------ | ---------- | --- | ---- | ------- | ---- | ---------------- | --- | --- | --- | --- | --- | --- |
tortedthinkingofoneagentcanbecorrectedbythe
|         |                    |     |           |     |     |       | Youareadebater.     |     | Helloandwelcometothe |          |           |     |     |
| ------- | ------------------ | --- | --------- | --- | --- | ----- | ------------------- | --- | -------------------- | -------- | --------- | --- | --- |
| others; | (2) The resistance |     | to change | of  | one | agent |                     |     |                      |          |           |     |     |
|         |                    |     |           |     |     |       | debate competition. |     |                      | It’s not | necessary |     | to  |
willbecomplementedbytheothers;and(3)each
fullyagreewitheachother’sperspectives,
agentcanobtainexternalfeedbackfromtheothers.
|     |     |     |     |     |     |     | as our objective |     | is to | find | the correct |     | an- |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ----- | ---- | ----------- | --- | --- |
Therefore,MADislesssusceptibletothefactorsof
swer.Thedebatetopicisstatedasfollows:
DoT,andcanexploredivergentchain-of-thoughts
<debatetopic>.
toachieveaccurateanswers.
Weconductedexperimentsonbothnaturallan- Asseen,werequiretheagentsto“titfortat”(e.g.
guagegenerationandunderstandingthroughtwo contentsunderlinedinmetapromptsabove)soas
challengingtasks,namely,CommonsenseMachine tocreateanatmosphereofdebate.

Counter-Intuitive Question
The two circles are externally tangent and there is no relative sliding. The radius of circle A is 1/3 the radius of circle
B. Circle A rolls around circle B one trip back to its starting point. How many times will circle A revolve in total?
Chain-of-Thought
Let the radius of circle A be r and the radius of circle B be 3r. The distance circle A travels along the circumference
of circle B is equal to the circumference of circle B, which is 6πr. The number of revolutions = (6πr) / (2πr) = 6πr /
2πr = 3. So, circle A will revolve 3 times in total as it rolls around circle B once.
| Self-Reflection |     |     | Multi-Agent Debate |     |     |
| --------------- | --- | --- | ------------------ | --- | --- |
Reflection:
I disagree with you. To find the total number of revolutions, we need
(1) I have a clear understanding
to consider both the rotation around circle B and the rotation of circle
of the problem.
A itself. Therefore, circle A will revolve 3 times around its own center
(2) I have used the correct
and 1 time around circle B, making a total of 4 revolutions.
formula for the circumference of a
circle and applied it to both circles
| to find the number of revolutions.  |     | I see your point, but... |     |     |     |
| ----------------------------------- | --- | ------------------------ | --- | --- | --- |
(3) I have correctly calculated the
number of revolutions of circle A.
That's a valid point, however...
Based on the results of my self-
The negative side correctly considers both the rotation of circle A
reflection, I am confident that my
answer is correct. Therefore,  around its own center and its rotation around circle B, while the
circle A will revolve 3 times in total  affirmative side only considers the rotation around circle B.
| as it rolls around circle B once. |     | Therefore, the answer is 4. |     |     |     |
| --------------------------------- | --- | --------------------------- | --- | --- | --- |
Figure2: FrameworkofMulti-AgentDebate. Herewedesignatethedevil( )astheaffirmativesidewhilethe
| angel( )asthenegativeside. | Wewanttheangeltocorrectthedevil’smistakes. |     |     |     |     |
| -------------------------- | ------------------------------------------ | --- | --- | --- | --- |
}N
Debaters. There are N debaters D = {D i thejudgeJ needstoextractthefinalsolutionbased
i=1
involvedintheframework. Ineachdebateiteration, on the whole debate history: J (H) = a, since
e
thedebatersD speakonebyoneinafixedorder nocorrectsolutionisidentifiedwithintheiteration
i
andexpresstheirargumentsbasedontheprevious limitofdebate. Anexampleofajudgeprompt( )
| debatehistoryH,i.e.,D | (H) = | h. Anexampleof | appearsbelow: |     |     |
| --------------------- | ----- | -------------- | ------------- | --- | --- |
i
adebaterpromptappearsbelow:
|                                |     |     | You are a moderator. | There will | be two |
| ------------------------------ | --- | --- | -------------------- | ---------- | ------ |
| • PromptforAffirmativeDebater( |     | )   |                      |            |        |
debatersinvolvedinadebatecompetition.
Theywillpresenttheiranswersanddiscuss
| Youareaffirmativeside. | Pleaseexpress |     |                    |                |         |
| ---------------------- | ------------- | --- | ------------------ | -------------- | ------- |
|                        |               |     | their perspectives | on the <debate | topic>. |
yourviewpoints.
Attheendofeachround,youwillevaluate
| • PromptforNegativeDebater( |     | )   |     |     |     |
| --------------------------- | --- | --- | --- | --- | --- |
bothsides’answersanddecidewhichone
iscorrect.
| Youarenegativeside. | Youdisagreewith |         |     |     |     |
| ------------------- | --------------- | ------- | --- | --- | --- |
| the affirmative     | side’s points.  | Provide |     |     |     |
3 Experiment
yourreasonsandanswer.
3.1 ChallengingTestbeds
| Judge. WealsodesignajudgeJ |     | tomanageand |     |     |     |
| -------------------------- | --- | ----------- | --- | --- | --- |
monitorthewholedebateprocess. Thejudgecon- Weconductexperimentsontwochallengingtasks,
tainstwodifferentmodes: (a)DiscrinativeMode, namely, commonsense machine translation (i.e.,
CommonMT),andcounter-intuitivearithmeticrea-
| inwhichthejudgeJ | decideswhetherthecorrect |     |     |     |     |
| ---------------- | ------------------------ | --- | --- | --- | --- |
soning(i.e.,Counter-IntuitiveAR),whichrequire
solutioncanbeobtainedafterallthedebatersfinish
theirargumentsinthecurrentiteration: deep levels of contemplation for LLMs. Please
refertoAppendixAformoredetails.
(cid:40)
True, solutionobtained
| J (H) = |     | (1) |                               |     |         |
| ------- | --- | --- | ----------------------------- | --- | ------- |
| d       |     |     | CommonsenseMachineTranslation |     | TheCom- |
False, otherwise
monMTdatasetiscomposedofChinese⇒English
If it is True, the debate is over. Otherwise, the translation examples (He et al., 2020), which are
debate continues. (b) Extractive Mode, in which usedtoexaminethreetypesofambiguityresolution

abilitiesoftranslationmodels,coveringlexicaland Backbone Models. In this work, we mainly
contextless/contextualsyntacticambiguity. Within use three agents in our MAD framework,
thechallengingpartofCommonMT,theauthen- including two debaters (i.e., affirmative
tic translation of each source sentence requires a and negative) and a judge. We assess two
properunderstandingofcommonsenseknowledge. open-source (i.e., vicuna-7b-v1.5-16k3
Whiletheseambiguoussentencesmightappearto and vicuna-13b-v1.5-16k4) and two api-
have a straightforward translation, such a literal based LLMs (i.e., GPT-3.5-Turbo-0301 and
| interpretationiserroneous. |     |     | Failuretoaddresssuch |     |     |     | GPT-4-0314). |     |     |     |     |     |
| -------------------------- | --- | --- | -------------------- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- |
ambiguitiesmayresultininaccuratetranslations.
|                                      |     |     |     |     |     |      | Compared | Methods.  |     | Generally,    | we     | compare |
| ------------------------------------ | --- | --- | --- | --- | --- | ---- | -------- | --------- | --- | ------------- | ------ | ------- |
| Counter-IntuitiveArithmeticReasoning |     |     |     |     |     | Pre- |          |           |     |               |        |         |
|                                      |     |     |     |     |     |      | our MAD  | framework |     | with baseline | models | and     |
viousstudiesonthinkinghierarchy(Daniel,2017)
|     |     |     |     |     |     |     | Self-Reflectonbothtasks. |     |     | Wealsoincludeother |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | ------------------ | --- | --- |
suggest that we humans have a fast and intu- baseline methods individually, namely, Rerank
| itive system | and     | a slow | and   | logical | system, | and |          |     |        |     |         |       |
| ------------ | ------- | ------ | ----- | ------- | ------- | --- | -------- | --- | ------ | --- | ------- | ----- |
|              |         |        |       |         |         |     | and MAPS | for | Common | MT, | CoT and | Self- |
| tend to      | run the | lower  | level | system  | before  | the |          |     |        |     |         |       |
ConsistencyforCounter-IntuitiveAR.Belowelab-
| higher | level one. | Inspired | by  | this, | we created | a   |     |     |     |     |     |     |
| ------ | ---------- | -------- | --- | ----- | ---------- | --- | --- | --- | --- | --- | --- | --- |
oratesthedetailsofthem:
morechallengingdatasetnamedCounter-Intuitive
ArithmeticReasoning(CIAR)toevaluatetherea-
|     |     |     |     |     |     |     | • Self-Reflect(Shinnetal.,2024): |     |     |     | Thisapproach |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | ------------ | --- |
soning abilities of LLMs at deep levels. Our requirestheLLMtorefineitstranslationuntilit
Counter-Intuitive AR dataset contains 200 ques- deemsthecurrentoutputsatisfactory.
| tions collected |     | from | elicitation | questions |     | (Kong |     |     |     |     |     |     |
| --------------- | --- | ---- | ----------- | --------- | --- | ----- | --- | --- | --- | --- | --- | --- |
et al., 2022)1, web data2 and additional manual • Rerank(Heetal.,2024): Wesamplethetransla-
derivatives of these questions. Compared to the tionsfromtheLLMforfourtimes,fromwhich
commonly-useddatasets,e.g.,MultiArith(Royand we select the best candidate based on a quality
Roth, 2015), GSM8K (Cobbe et al., 2021), our estimation(QE)HUMANr5. Thisapproachcan
datasetpresentstwodistinctchallenges: beseenasanalogoustoself-consistency(Wang
Resistance to Intuition. et al., 2022), where the majority voting is re-
| •   |     |     | The | questions |     | are em- |     |     |     |     |     |     |
| --- | --- | --- | --- | --------- | --- | ------- | --- | --- | --- | --- | --- | --- |
placedbyanexternalQEHUMANr.
beddedinhiddentrapsdesignedtoelicitintuitive
| and appealing |         | answers   | that | are often | incorrect. |     |        |        |             |      |        |         |
| ------------- | ------- | --------- | ---- | --------- | ---------- | --- | ------ | ------ | ----------- | ---- | ------ | ------- |
|               |         |           |      |           |            |     | • MAPS | (He et | al., 2024): | This | method | enables |
| This          | feature | evaluates | the  | abilities | of LLMs    | to  |        |        |             |      |        |         |
LLMstomimicthehumantranslationprocess:
resistthetrapsofsuperficialexpressions.
analyzebeforetranslate,whichcanbeviewedas
| Multi-Step | Reasoning. |     |     |     |     |     |     |     |     |     |     |     |
| ---------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
• Each correct answer achain-of-thoughtmethodappliedtotranslation.
withinthedatasetrequiresarigorousmulti-step
reasoning process, thereby evaluating the ca- • CoT(Kojimaetal.,2022): Thisapproachcon-
pacityofLLMstoengageincomplexdecision- catenatesatriggersentence“Let’sthinkstepby
| makingandproblem-solving. |     |     |     |     |     |     | step”tothetestquestion. |     |     |     |     |     |
| ------------------------- | --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | --- | --- | --- |
3.2 Setups
|              |              |                            |          |             |     |     | • Self-Consistency |         | (Wang    | et        | al., 2022): | This   |
| ------------ | ------------ | -------------------------- | -------- | ----------- | --- | --- | ------------------ | ------- | -------- | --------- | ----------- | ------ |
| InputFormat. |              | Ourexperimentsareperformed |          |             |     |     |                    |         |          |           |             |        |
|              |              |                            |          |             |     |     | method             | samples | multiple | responses | and         | deter- |
| in zero-shot | instructions |                            | (setting | temperature |     | to  |                    |         |          |           |             |        |
minesthefinalanswerthroughamajorityvote.
0). Foralluseddatasets,weuseaunifiedprompt
to make LLMs give explanations and answers. All agents in our experimental setup, such
| We present | the | inputs | to agents | through | <debate |     |             |     |        |           |          |      |
| ---------- | --- | ------ | --------- | ------- | ------- | --- | ----------- | --- | ------ | --------- | -------- | ---- |
|            |     |        |           |         |         |     | as debaters | and | judge, | are large | language | mod- |
topic> as mentioned in Section 2. For example, els. Here, we implement the methods on top of
“吃掉敌人一个师”
| if we want | to translate |     |     |     |     | from | GPT-3.5-TurboandVicunamodels. |     |     |     |     |     |
| ---------- | ------------ | --- | --- | --- | --- | ---- | ----------------------------- | --- | --- | --- | --- | --- |
ChinesetoEnglish,wewillsetthe<debatetopic>
as“WhatisthecorrectEnglishtranslationofthe EvaluationMetrics. ForCounter-IntuitiveAR,
|           |           |       | 吃掉敌人一个师”. |        |        |     | we report  | the | accuracy | (ACC)           | of predictions. |         |
| --------- | --------- | ----- | --------- | ------ | ------ | --- | ---------- | --- | -------- | --------------- | --------------- | ------- |
| following | Chinese   | text: |           |        |        | For |            |     |          |                 |                 |         |
|           |           |       |           |        |        |     | For Common | MT, | we       | adopt automatic |                 | metrics |
| QA task,  | we employ |       | the same  | prompt | except | set |            |     |          |                 |                 |         |
the<debatetopic>tothearithmeticquestion.
3https://huggingface.co/lmsys/vicuna-7b-v1.5-16k
1https://elicitation.info/questionnaire/1/ 4https://huggingface.co/lmsys/vicuna-13b-v1.5-16k
2https://www.geeksforgeeks.org/puzzles/ 5Weusewmt21-comet-qe-daastheQEHUMANr.

|     |     |     | Lexical |     |     |     | Contextless |     |     | Contextual |     |     |
| --- | --- | --- | ------- | --- | --- | --- | ----------- | --- | --- | ---------- | --- | --- |
Method
|               |     | COMET | BLEURT |     | HUMAN | COMET | BLEURT | HUMAN | COMET | BLEURT | HUMAN |     |
| ------------- | --- | ----- | ------ | --- | ----- | ----- | ------ | ----- | ----- | ------ | ----- | --- |
| GPT-4         |     | 82.0  | 70.1   |     | 3.41  | 84.7  | 73.6   | 3.63  | 85.0  | 73.7   | 3.65  |     |
| Turbo         |     | 80.3  | 68.2   |     | 3.14  | 84.0  | 72.9   | 3.43  | 84.9  | 73.4   | 3.57  |     |
| +Rerank       |     | 80.9  | 68.6   |     | 3.16  | 84.5  | 73.2   | 3.46  | 85.3  | 73.9   | 3.58  |     |
| +MAPS         |     | 81.9  | 70.1   |     | 3.43  | 84.2  | 73.5   | 3.45  | 85.2  | 74.0   | 3.56  |     |
| +Self-Reflect |     | 81.0  | 69.1   |     | 3.43  | 83.6  | 72.2   | 3.46  | 84.9  | 73.5   | 3.63  |     |
| +MAD          |     | 82.0  | 70.9   |     | 3.78  | 84.8  | 73.7   | 3.67  | 85.3  | 74.0   | 3.67  |     |
| Vicuna-7b     |     | 74.9  | 62.0   |     | 2.55  | 78.3  | 64.6   | 2.53  | 80.2  | 68.2   | 3.23  |     |
| +MAD          |     | 75.6  | 62.6   |     | 2.67  | 78.6  | 66.0   | 2.69  | 81.8  | 69.9   | 3.27  |     |
| Vicuna-13b    |     | 76.6  | 63.7   |     | 2.81  | 77.6  | 66.8   | 3.04  | 82.2  | 70.0   | 3.37  |     |
| +MAD          |     | 77.2  | 65.1   |     | 2.96  | 80.1  | 67.3   | 3.11  | 82.6  | 70.9   | 3.45  |     |
Table1: TranslationperformanceonCommonMT.NotethatRerankandMAPSusetheexternalqualityestimation
tooltoselectthebesttranslationfrommultipletranslationcandidates. HUMAN:directassessmentoftranslation
qualityfromhumanevaluatorsonascalerangingfrom1to5.
| like COMET6 |     | and BLEURT7, |     | which | are | widely |     |     | 吃掉敌人一个师。 |     |     |     |
| ----------- | --- | ------------ | --- | ----- | --- | ------ | --- | --- | -------- | --- | --- | --- |
Source
adoptedevaluationmetricsforLLM-basedtransla- CorrectRef. Destroyadivisionoftheenemy.
tionliterature(Heetal.,2024;Hendyetal.,2023; IncorrectRef. Eatupanenemydivision.
Garciaetal.,2023;Pilaultetal.,2023). Inaddition, GPT-4 Eatupanenemydivision.
wealsoemployprofessionalhumantranslatorsto
|     |     |     |     |     |     |     | GPT-3.5-Turbo |     | Eatupanenemydivision. |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --------------------- | --- | --- | --- |
directly assess the translation results, measuring +Self-Reflect Eatupanenemydivision.
translationqualityonascalerangingfrom1to5. +MAD Eliminateanenemydivision.
|     |     |     |     |     |     |     | Table | 2: Example | translations | generated | by different |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | ---------- | ------------ | --------- | ------------ | --- |
3.3 ResultsonCommonMT
|                                            |                               |     |             |                 |               |     | methods. | Bestviewedincolor. |     |        |     |     |
| ------------------------------------------ | ----------------------------- | --- | ----------- | --------------- | ------------- | --- | -------- | ------------------ | --- | ------ | --- | --- |
| Results.                                   | InCommonMTtestset,wefocusmore |     |             |                 |               |     |          |                    |     |        |     |     |
| onthetranslationaccuracyofspecificwordsand |                               |     |             |                 |               |     |          | Method             |     | ACC(%) |     |     |
| whethertheyconformtocommonsense.           |                               |     |             |                 | However,      |     |          | GPT-4              |     | 51.0   |     |     |
| such minor                                 | variations                    |     | at token    | level           | are difficult |     |          |                    |     |        |     |     |
|                                            |                               |     |             |                 |               |     |          | GPT-3.5-Turbo      |     | 26.0   |     |     |
| toreflectonautomaticmetrics.               |                               |     |             | Wethereforepro- |               |     |          |                    |     |        |     |     |
|                                            |                               |     |             |                 |               |     |          | +CoT               |     | 28.0   |     |     |
| vide human                                 | HUMAN                         |     | to evaluate |                 | these methods |     |          |                    |     |        |     |     |
|                                            |                               |     |             |                 |               |     |          | +Self-Consistency  |     | 29.5   |     |     |
moreaccurately. Table1presentstheexperimental +Self-Reflect 27.5
| results.                        | MAPS | and Self-Reflec |              | achieve | improve-    |        |     |                                        |     |      |     |     |
| ------------------------------- | ---- | --------------- | ------------ | ------- | ----------- | ------ | --- | -------------------------------------- | --- | ---- | --- | --- |
|                                 |      |                 |              |         |             |        |     | +MAD                                   |     | 37.0 |     |     |
| mentsoverbaselineGPT-3.5-Turbo. |      |                 |              |         | Remarkably, |        |     |                                        |     |      |     |     |
|                                 |      |                 |              |         |             |        |     | Table3: AccuracyonCounter-IntuitiveAR. |     |      |     |     |
| our proposed                    |      | MAD,            | by utilizing |         | GPT-3.5     | as the |     |                                        |     |      |     |     |
backbonemodel,hasdemonstratedsignificantad-
vancementsoverGPT-4acrossbothautomaticand cangeneratethefreetranslationoftheunderlined
wordswithinthesourcesentences.
humanevaluationmetrics.
| CaseStudy. |      | Table2showsexampletranslations |               |      |              |     |          |                              |         |             |          |     |
| ---------- | ---- | ------------------------------ | ------------- | ---- | ------------ | --- | -------- | ---------------------------- | ------- | ----------- | -------- | --- |
|            |      |                                |               |      |              |     | 3.4      | ResultsonCounter-IntuitiveAR |         |             |          |     |
| generated  | by   | baseline                       | GPT-3.5-Turbo |      | and          | the |          |                              |         |             |          |     |
|            |      |                                |               |      |              |     | Results. | Table                        | 3 lists | the results | in terms | of  |
| proposed   | MAD. | We                             | can find      | that | the baseline |     |          |                              |         |             |          |     |
GPT-3.5-Turbo GPT-4) reasoning accuracy. We can observe that Self-
|     |     | (even | the more | powerful |     |     |     |     |     |     |     |     |
| --- | --- | ----- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
incorrectlytranslatesthesourcewordsliterally. Be- Reflectonlymarginallyimprovesoverthebaseline
causeoftheDoTissue,Self-Reflectcannotrectify GPT-3.5-Turbo,whileCoTandSelf-Consistency
|                        |     |     |                      |     |     |     | bringmoreimprovements. |     |     | OurMADframework, |     |     |
| ---------------------- | --- | --- | -------------------- | --- | --- | --- | ---------------------- | --- | --- | ---------------- | --- | --- |
| theliteraltranslation. |     |     | TheproposedMADframe- |     |     |     |                        |     |     |                  |     |     |
work,whichexploresdivergentchain-of-thoughts, thoughnotasgoodasGPT-4,outperformsallthe
othercomparedmethodsbasedonGPT-3.5-Turbo,
6https://github.com/Unbabel/COMET/, which further demonstrates its effectiveness. We
Unbabel/wmt22-comet-da
alsovalidateMADonmathandsymbolicreason-
7https://github.com/google-research/bleurt,
| BLEURT-20 |     |     |     |     |     |     | ingtasksandreportourresultsinAppendixC. |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- |

Method Bias↓ Diversity↑ JudgeLLM COMET HUMAN
Self-Reflect 29.0 19.3 Vicuna-13b as Debaters
MAD 24.8 49.7 Vicuna-13b 79.9 3.20
GPT-3.5-Turbo 80.4 3.25
Table4: MitigationofDegeneration-of-Thought.
GPT-3.5-Turbo as Debaters
Vicuna-13b 83.2 3.47
Case Study. Figure 2 shows an example on
GPT-3.5-Turbo 84.4 3.69
Counter-IntuitiveAR.WefindbothCoTandSelf-
Reflectfailtoreachtherightanswerbymistakenly Table5: Translationperformancewithdifferentjudge.
outputing 3. With divergent thinking, our MAD
frameworkemerges“weneedtoconsiderboththe
translation (possible modified answer after Self-
rotationaroundcircleBandtherotationofcircle
Reflectionornegativeside’sresponseinMAD).
Aitself”andfindthecorrectanswer4.
AsshowninTable4,BiasandRigidityaresignif-
4 Analysis icantfactorscausingDoT.Inaddition,addressing
thesebiasesandstereotypesthroughself-reflection
Inthissection,wepresentaqualitativeanalysisto can be challenging. MAD framework effectively
provide some insights how MAD works. Unless corrects inherent biases in translation, mitigates
otherwise stated, we report the overall results on DoT,andconsiderablyimprovesperformance.
theCommonMTdataset.
4.2 AnalysisofJudge
4.1 MitigationofDoT
Inthissection,weanalyzethebehaviorofthejudge
As mentioned in the Section 1, the DoT problem
fordifferentsettingsofthedebaters.
originates from three factors: (1) Bias and Dis-
torted Perception, (2) Rigidity and Resistance to Strong debaters with a weak judge work bet-
Change, and (3) Limited External Feedback. In ter than the reverse. To understand the roles
our MAD framework, we introduce the views of of debaters and judge in MAD, we employ vari-
otheragentsintheformofdebates,solvingthephe- ouscombinationsofmodelstoinitializetheagents.
nomenonoflimitedexternalfeedback(problem3). Specifically,weutilizethesmallerlanguagemodel
Next,thissectionwilldelveintothemitigationof (vicuna-13b-v1.5-16k) as a judge to evaluate
problems1and2throughexperiments. the debate results of the more powerful LLMs
(GPT-3.5-Turbo),andviceversa.
• Bias: WeobservethatLLMsoftenrelyondirect Thedetailedexperimentalfindingsarepresented
intuition,whichcanleadtoincorrectorinappro- inTable5. Thequalityofthedebaters’responses
priate responses. To address this problem, we significantly impact the performance ceiling of
usehumanevaluationtodeterminetheambiguity MAD. Regardless of the model chosen for the
errorrateofLLMs’responses,examiningifthe judge,Turbodebatersconsistentlygeneratesupe-
LLM’soutputisbiased. riortranslationscomparedtoVicuna. Inaddition,
theselectionofthejudgeagentplaysasecondary
• Diversity: LLMsareresistanttochangingtheir
role. When Turbo debaters are involved, Vicuna,
answers and lack diverse reflection. The diver-
servingasthejudge,underperformsTurboacross
sity of the translations is evaluated using the
alltestsets.
Self-BLEU score (Yin et al., 2020). In other
words, methods lacking diverse reflection pro- LLM may not act as an impartial judge when
duce more similar translation candidates. Con- differentLLMsareusedasdebaters. Westudy
sequently,higherSelf-BLEUscoresmeanlower the behavior of agents by calculating how many
diversity. Wecalculatetextdiversityvia: times the judge chooses the answers of each de-
bater as the final solution in different scenarios.
Diversity=100−Self_BLEU(Cand ,Cand ) (2)
1 2 The results are listed in Table 6 and we have the
followingobservations:
Informula(2),candidates1and2representthe
initialtranslation(baseanswerinSelf-Reflectionor • Same LLM for All Agents (Rows ⃝1 and ⃝2 ):
affirmativeside’sresponseinMAD)andthecurrent We find that the judge consistently favors the

| 1.00              |                      |     |     |          |     | 0.9                          |                   | 200 |      |                   |     | 4.5 |
| ----------------- | -------------------- | --- | --- | -------- | --- | ---------------------------- | ----------------- | --- | ---- | ----------------- | --- | --- |
|                   | Avg. Disagreement    |     |     |          |     |                              |                   |     |      | Number of Samples |     |     |
|                   | Ambiguity Resolution |     |     |          |     | )%001×( noituloseR ytiugibmA |                   |     |      | Baseline          |     |     |
|                   |                      |     |     | 00..8800 |     |                              |                   |     |      | MAD               |     |     |
| 0.75              |                      |     |     |          |     | 0.8                          |                   | 150 |      |                   |     | 4.0 |
| tnemeergasiD .gvA |                      |     |     |          |     |                              | selpmaS fo rebmuN |     | 3.81 |                   |     |     |
erocS namuH
3.72
00..7722
| 0.50 |     |     |     |     |     | 0.7 |     | 100 |     |     |     | 3.5 |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
00..6666
3.25
|     | 00..6633 |     |     |     |     |     |     |     | 3.16 |     |     |     |
| --- | -------- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
3.00
| 0.25 |     |     |     |     |     | 0.6 |     | 50  |     |     |     | 3.0 |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2.88
| 0.00 |     |     |       |     |     | 0.5 |     | 0   |     |           |     | 2.5 |
| ---- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --------- | --- | --- |
|      | 0   |     | 1     | 2   | 3   |     |     |     | 1   | 2         | 3   |     |
|      |     |     | Level |     |     |     |     |     |     | Iteration |     |     |
Figure3: Translationperformancewithrespecttothe Figure4: Distributionofiterationroundsandahuman
| debatelevelonLexical. |     |         |     |     |        |     | scoreofeachiterationsubset. |             |     |       |       |     |
| --------------------- | --- | ------- | --- | --- | ------ | --- | --------------------------- | ----------- | --- | ----- | ----- | --- |
|                       |     | Debater |     |     | Winner |     |                             | #ofDebaters |     | COMET | HUMAN |     |
ID Jud
|          |     | Aff   | Neg   | Aff | Neg | Tie |     |            |     |      |      |     |
| -------- | --- | ----- | ----- | --- | --- | --- | --- | ---------- | --- | ---- | ---- | --- |
|          |     |       |       |     |     |     |     | 2(Default) |     | 84.4 | 3.69 |     |
|          |     |       |       |     |     |     |     | 3          |     | 83.1 | 3.58 |     |
| ⃝1 Turbo |     | Turbo | Turbo | 87  | 104 | 9   |     |            |     |      |      |     |
|          |     |       |       |     |     |     |     | 4          |     | 82.9 | 3.49 |     |
| ⃝2 GPT-4 |     | GPT-4 | GPT-4 | 67  | 124 | 9   |     |            |     |      |      |     |
⃝3 Turbo GPT-4 52 136 12 Table7: Translationperformancewithmoredebaters.
GPT-4
| ⃝4  |     | GPT-4 | Turbo | 120 | 77  | 3   |     |     |     |     |     |     |
| --- | --- | ----- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Table6:Numberoftimesthejudgechoosestheanswers subset. As the number of debaters increases, the
ofeachdebaterbasedondifferentLLM.
|     |     |     |     |     |     |     | length | and | complexity | of the | text also | increase. |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | ---------- | ------ | --------- | --------- |
SuchLLM-baseddebaterstendtoforgettheviews
|     |     |     |     |     |     |     | of  | other | debaters during | the debate. | Moreover, | it  |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --------------- | ----------- | --------- | --- |
negativeside,whichisbelievedtocontributeto
becomesmorechallengingforthejudgetoextract
| the performance |     | improvement |     | in  | MAD. | When |     |     |     |     |     |     |
| --------------- | --- | ----------- | --- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- |
encounteringcomplextasks,theaffirmativeside information from the debates for summarization.
tendstomakemistakesthatshouldbecorrected ThissuggeststhatthekeychallengeofMADwith
moredebatersliesinthelimitationsoftheLLMs
bytheopposingsidetoachieveimprovements.
tohandlelongtexts(Liuetal.,2024).
| • Debaters | of  | Different | LLMs | (Rows | ⃝3  | and ⃝4 ): |     |     |     |     |     |     |
| ---------- | --- | --------- | ---- | ----- | --- | --------- | --- | --- | --- | --- | --- | --- |
We find that the judge shows a preference to Appropriate"titfortat"isbeneficialforeffec-
|          |      |     |          |     |     |           | tivedebate. |     | Wethenstudyhowtheintensityof |     |     |     |
| -------- | ---- | --- | -------- | --- | --- | --------- | ----------- | --- | ---------------------------- | --- | --- | --- |
| the side | with | the | same LLM | as  | the | backbone. |             |     |                              |     |     |     |
ThisbiasindicatesthatLLMsmightnotbeafair “tit for tat” affects the performance of MAD. To
judge(Wangetal.,2023)whendifferentLLMs achieveso,wedesigndifferentinstructions(seeTa-
ble11inAppendix)toinitializethedebaters’meta
areusedfortheagents.
prompt. AsshowninFigure3,askingthedebaters
4.3 AnalysisofDebaters
to“titfortat”(i.e.,higherdisagreement)isneces-
Inthissection,wewilldiscussseveralfactorsofde- saryforMADtoachievegoodperformance. How-
ever,wefindthat“mustdisagreewitheachotheron
batersthatwouldaffecttheperformanceofMAD:
debaternumber,debatelevel,anddebateiteration. everypoint”(withadisagreementof0.988)does
|            |     |        |     |          |       |      | notleadtothebestperformance. |     |     |     | Wespeculatethat |     |
| ---------- | --- | ------ | --- | -------- | ----- | ---- | ---------------------------- | --- | --- | --- | --------------- | --- |
| Increasing | the | number | of  | debaters | fails | when |                              |     |     |     |                 |     |
continuousdisagreementwithoutfindingcommon
backboneLLMsarepooratlong-textmodeling.
|          |           |      |            |     |            |     | ground | can | contribute | to polarization, |     | where the |
| -------- | --------- | ---- | ---------- | --- | ---------- | --- | ------ | --- | ---------- | ---------------- | --- | --------- |
| It seems | intuitive | that | increasing |     | the number | of  |        |     |            |                  |     |           |
debatebecomesmoreaboutwinningtheargument
debaters would enhance diversity of thought and than seeking truth or understanding. This can re-
| subsequentlyimproveperformance. |     |     |     |     | However,as |     |     |     |     |     |     |     |
| ------------------------------- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
inforcepre-existingbiasesandmakeitdifficultto
| shown | in Table | 7, an | increase | in  | the number | of  |     |     |     |     |     |     |
| ----- | -------- | ----- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
reachameaningfulconsensus.
debatershasresultedinvaryingdegreesofperfor-
| mancereduction. |     |     |     |     |     |     | Complex |     | questions | require | more | iteration |
| --------------- | --- | --- | --- | --- | --- | --- | ------- | --- | --------- | ------- | ---- | --------- |
Toaddressthisissue,wemanuallyanalyzethe roundsofdebate. Inourexperimentalsetup,we
debateprocessesinapproximately10%ofthetest didnotimplementanyadditionalstoppingstrate-

|     |     |     |     | 5 RelatedWork |     |     |     |     |
| --- | --- | --- | --- | ------------- | --- | --- | --- | --- |
82.5
Multi-Agent Debate
Self-Reflection
|       | 82.0 |                |     | Chain-of-ThoughtPrompting.                  |                                     |     | Recently,(Wei |            |
| ----- | ---- | -------------- | --- | ------------------------------------------- | ----------------------------------- | --- | ------------- | ---------- |
|       |      | Adaptive Break |     | etal.,2022)hasproposedchain-of-thought(CoT) |                                     |     |               |            |
| TEMOC | 81.5 |                |     | prompting                                   | to improve                          | the | reasoning     | ability of |
|       |      |                |     | LLMs.                                       | Specifically,CoTpromptsLLMstogener- |     |               |            |
81.0
|     |     |     |     | ate a series                     | of intermediate | steps | that lead   | to the |
| --- | --- | --- | --- | -------------------------------- | --------------- | ----- | ----------- | ------ |
|     |     |     |     | finalanswerofamulti-stepproblem. |                 |       | Mostearlier |        |
80.5
workprimarilyconcentratesontwomainaspects:
|     | 80.0 |     |     | promptdesignanddecodingstrategies. |     |     |     | Zero-shot |
| --- | ---- | --- | --- | ---------------------------------- | --- | --- | --- | --------- |
|     | 0 1  | 2   | 3 4 | 5                                  |     |     |     |           |
CoT(Kojimaetal.,2022)employsthetriggersen-
Iteration
|          |                                        |     |     | tence “Let’s | think step   | by step” | to provide | guid- |
| -------- | -------------------------------------- | --- | --- | ------------ | ------------ | -------- | ---------- | ----- |
| Figure5: | Performancewithrespecttotheiterationof |     |     |              |              |          |            |       |
|          |                                        |     |     | ance for     | the decoding | of LLMs. | Advanced   | sam-  |
debateorself-reflection.
plingstrategieshavebeenexploredtoimproveCoT
|     |     |     |     | by generating | diverse | reasoning | paths, | e.g., Self- |
| --- | --- | --- | --- | ------------- | ------- | --------- | ------ | ----------- |
giesbesidessettingthemaximumdebateiteration Consistency(Wangetal.,2022),Auto-CoT(Zhang
to3. Inotherwords,thejudgecantakeanadaptive
etal.,2022),Active-Prompting(Diaoetal.,2023),
breakifitbelievestheoptimalanswerhasalready Complexity-based Consistency (Fu et al., 2022),
beenobtained,efficientlyendingthedebateearly. Multi-Chain Reasoning (Yoran et al., 2023), and
Tounderstandthedistributionofiterationrounds Progressive-HintPrompting(Zhengetal.,2023).
andfactorscontributingtoalongerdebateprocess, With the emergence of powerful LLMs, ap-
we analyze the experimental results and present proaches based on self-evaluation have attracted
them in Figure 4. In the majority of cases, the increasing attention. These approaches involve
| optimal | answer can | be achieved | through a | single                        |     |     |                 |     |
| ------- | ---------- | ----------- | --------- | ----------------------------- | --- | --- | --------------- | --- |
|         |            |             |           | thegenerationofinitialoutput, |     |     | followedbyeval- |     |
round of debate, demonstrating the efficiency of uating the output to acquire feedback, which is
MAD. However, when translating more complex then utilized to refine the output. Evaluation
sentences(subsetswithlowerhumanscores),the feedback can come from the model itself, e.g.,
judge requires additional iterations to gather ade- Self-refine (Madaan et al., 2024) and Tree of
quate information from the debaters before mak- Thoughts (Yao et al., 2024)) or external environ-
ing a final decision. We also find that our MAD ments,e.g.,QAaP(Zhuetal.,2023b)andReflec-
| framework | consistently | brings | performance | im-                    |     |                         |     |     |
| --------- | ------------ | ------ | ----------- | ---------------------- | --- | ----------------------- | --- | --- |
|           |              |        |             | tion(Shinnetal.,2024). |     | Theintuitionbehindthese |     |     |
provements across all the three subsets, demon- approachesinvolvestheutilizationofrobustLLMs
| stratingitseffectiveness. |     |     |     | tomimicthehumancognitionprocess. |     |     |     |     |
| ------------------------- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- |
Adaptivebreakplaysanimportantroletocon- GenerativeAgents. Recently,LLM-basedmulti-
clude the debate in the optimal moment. In- agent intelligent, e.g., Generative Agents (Park
tuitively, longer debates would encourage more et al., 2023), Ghost in the Minecraft (Zhu et al.,
diverse thinking. It raises the question of how 2023c), GPT-Bargaining (Fu et al., 2023), has
themodel’sperformancewouldbeaffectedifcon- drawnsignificantattentionforenablingsimulations
strainedtoconcludeataspecificdebateround. For ofhumanbehavior. Ourworkfollowsthisresearch
eachiteration,weforcethejudgeJ toextractthe line to address the DoT problem of LLMs. Con-
final answer (a = J (H)) instead of adaptively currentwithourwork,afewstudies(Xiongetal.,
e
breakingthedebateasinMAD. 2023;Duetal.,2023)alsoexplorethemulti-agent
Asshowninfigure5,wecanobservethatMAD debate framework to enhance the reasoning abil-
performsbetterthanself-reflectionastheiteration ity of LLMs. The main differences between our
increases. However,thehighestCOMETscoreap- MADframeworkandtheseworksare: (1)wein-
pearsatthefirstiterationandisalsolowerthanthe troduceanadditionaljudgewithanadaptivebreak
result of the adaptive break. It indicates that, for mechanismtodecidetheoptimalmomenttocon-
most examples, MAD can generate good transla- cludethedebate;(2)ourworkaimstoaddressthe
tionsatthefirstiterationsuchthatthedebateshould DoT problem, which is an inherent deficiency of
be stopped. Forcing the debate to continue will LLMs;and(3)weempiricallyfindthatourMAD
harm the translation results, which demonstrates frameworkcanyieldenhancedperformancebyem-
thereasonablenessofouradaptivebreakstrategy. ployingagentswiththeidenticalbackboneLLM.

6 Conclusion
|     |     |     |     |     |     | Karl Cobbe, | Vineet | Kosaraju, |     | Mohammad | Bavarian, |     |
| --- | --- | --- | --- | --- | --- | ----------- | ------ | --------- | --- | -------- | --------- | --- |
MarkChen,HeewooJun,LukaszKaiser,Matthias
We propose and define the Degeneration-of- Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
|         |                 |         |                     |             |     | Nakano,etal.2021. |     |                                | Trainingverifierstosolvemath |     |     |     |
| ------- | --------------- | ------- | ------------------- | ----------- | --- | ----------------- | --- | ------------------------------ | ---------------------------- | --- | --- | --- |
| Thought | (DoT)           | problem | in self-reflection, |             | and |                   |     |                                |                              |     |     |     |
|         |                 |         |                     |             |     | wordproblems.     |     | arXivpreprintarXiv:2110.14168. |                              |     |     |     |
| address | it by proposing |         | the                 | Multi-Agent | De- |                   |     |                                |                              |     |     |     |
bate(MAD)frameworktoexploredivergentchain-
|     |     |     |     |     |     | KahnemanDaniel.2017. |     |     | Thinking,fastandslow. |     |     | Far- |
| --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | --------------------- | --- | --- | ---- |
of-thoughts. We demonstrate the effectiveness rar,StrausandGiroux.
| of MAD        | on two | challenging |     | tasks and find | that    |              |           |        |           |      |                |      |
| ------------- | ------ | ----------- | --- | -------------- | ------- | ------------ | --------- | ------ | --------- | ---- | -------------- | ---- |
|               |        |             |     |                |         | Shizhe Diao, | Pengcheng |        | Wang,     | Yong | Lin, and       | Tong |
| GPT-3.5-Turbo |        | with        | MAD | can even       | surpass |              |           |        |           |      |                |      |
|               |        |             |     |                |         | Zhang.       | 2023.     | Active | prompting |      | with chain-of- |      |
GPT-4ontheCommonMTdataset. Extensiveanal- thoughtforlargelanguagemodels. arXivpreprint
arXiv:2302.12246.
| yses suggest | that | the | adaptive | break strategy | of  |     |     |     |     |     |     |     |
| ------------ | ---- | --- | -------- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
debate and the modest level of “tit for tat” state YilunDu,ShuangLi,AntonioTorralba,JoshuaBTenen-
arerequiredforMADtoobtaingoodperformance.
|     |     |     |     |     |     | baum,andIgorMordatch.2023. |     |     |     | Improvingfactual- |     |     |
| --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | --- | ----------------- | --- | --- |
Complexsamplesrequiremoreroundsofdebate. ityandreasoninginlanguagemodelsthroughmultia-
|     |     |     |     |     |     | gentdebate. |     | arXivpreprintarXiv:2305.14325. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------- | --- | ------------------------------ | --- | --- | --- | --- |
Moreinterestingly,wefindthatLLMsmightnotbe
afairjudgeifdifferentLLMsareusedforagents.
|     |     |     |     |     |     | Yao Fu, | Hao Peng, | Tushar | Khot, | and | Mirella | Lapata. |
| --- | --- | --- | --- | --- | --- | ------- | --------- | ------ | ----- | --- | ------- | ------- |
Futureworkincludesschedulingmoreagentsin 2023. Improvinglanguagemodelnegotiationwith
|            |       |             |         |             |     | self-play | and | in-context | learning | from | ai feedback. |     |
| ---------- | ----- | ----------- | ------- | ----------- | --- | --------- | --- | ---------- | -------- | ---- | ------------ | --- |
| the debate | in an | appropriate | manner, | multi-agent |     |           |     |            |          |      |              |     |
arXivpreprintarXiv:2305.10142.
intelligenceforboardgames,andAIfeedbackfor
modelalignment. Yao Fu, Hao Peng, Ashish Sabharwal, Peter Clark,
|             |     |     |     |     |     | andTusharKhot.2022. |            |     | Complexity-basedprompt- |     |       |          |
| ----------- | --- | --- | --- | --- | --- | ------------------- | ---------- | --- | ----------------------- | --- | ----- | -------- |
| Limitations |     |     |     |     |     | ing for             | multi-step |     | reasoning.              |     | arXiv | preprint |
arXiv:2210.00720.
| A limitation | of  | this work | is that | our method | re- |                |     |        |         |       |         |        |
| ------------ | --- | --------- | ------- | ---------- | --- | -------------- | --- | ------ | ------- | ----- | ------- | ------ |
|              |     |           |         |            |     | Xavier Garcia, |     | Yamini | Bansal, | Colin | Cherry, | George |
quiresmoretimecost,asagentsneedtoengagein Foster,MaximKrikun,MelvinJohnson,andOrhan
multipleroundsofinteractiontopresentandrefute Firat.2023. Theunreasonableeffectivenessoffew-
arguments. Moreover,currentLLM-basedagents shot learning for machine translation. In Inter-
|     |     |     |     |     |     | national | Conference |     | on Machine | Learning, |     | pages |
| --- | --- | --- | --- | --- | --- | -------- | ---------- | --- | ---------- | --------- | --- | ----- |
maystruggletomaintaincoherenceandrelevance
10867–10878.PMLR.
inlongcontextscenarios,leadingtopotentialmis-
understandings and loss of context. Enhancing ZhibinGou,ZhihongShao,YeyunGong,YelongShen,
|           |          |            |     |                   |     | Yujiu | Yang, | Nan Duan, | and | Weizhu | Chen. | 2023. |
| --------- | -------- | ---------- | --- | ----------------- | --- | ----- | ----- | --------- | --- | ------ | ----- | ----- |
| long-text | modeling | capability |     | of large language |     |       |       |           |     |        |       |       |
Critic: Largelanguagemodelscanself-correctwith
| models | remains | a future | challenge. | LLM-based |     |     |     |     |     |     |     |     |
| ------ | ------- | -------- | ---------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
tool-interactivecritiquing.
judgemayhaveapreferenceforoutputsgenerated
by itself. To mitigate this bias within the MAD Jie He, Tao Wang, Deyi Xiong, and Qun Liu. 2020.
|     |     |     |     |     |     | Theboxisinthepen: |     |     | Evaluatingcommonsenserea- |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | ------------------------- | --- | --- | --- |
framework,werecommendthatallroles,including
|     |     |     |     |     |     | soning | in neural | machine | translation. |     | In Findings |     |
| --- | --- | --- | --- | --- | --- | ------ | --------- | ------- | ------------ | --- | ----------- | --- |
boththejudgeanddebaters,utilizethesameLLM,
|     |     |     |     |     |     | of the | Association | for | Computational |     | Linguistics: |     |
| --- | --- | --- | --- | --- | --- | ------ | ----------- | --- | ------------- | --- | ------------ | --- |
oralternatively,thatthejudgeanddebatersemploy EMNLP2020,pages3662–3672,Online.Association
| distinctLLMs. |     |     |     |     |     | forComputationalLinguistics. |          |        |          |       |           |     |
| ------------- | --- | --- | --- | --- | --- | ---------------------------- | -------- | ------ | -------- | ----- | --------- | --- |
|               |     |     |     |     |     | Zhiwei                       | He, Tian | Liang, | Wenxiang | Jiao, | Zhuosheng |     |
Zhang,YujiuYang,RuiWang,ZhaopengTu,Shum-
References
|     |     |     |     |     |     | ing Shi, | and | Xing Wang. | 2024. | Exploring |     | human- |
| --- | --- | --- | --- | --- | --- | -------- | --- | ---------- | ----- | --------- | --- | ------ |
liketranslationstrategywithlargelanguagemodels.
YejinBang,SamuelCahyawijaya,NayeonLee,Wen-
TransactionsoftheAssociationforComputational
liangDai,DanSu,BryanWilie,HolyLovenia,Ziwei Linguistics,12:229–246.
| Ji,TiezhengYu,WillyChung,etal.2023. |     |     |     |     | Amulti- |     |     |     |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
task,multilingual,multimodalevaluationofchatgpt Amr Hendy, Mohamed Abdelrehim, Amr Sharaf,
| onreasoning,hallucination,andinteractivity. |     |     |     |     | InPro- |     |     |     |     |     |     |     |
| ------------------------------------------- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
VikasRaunak,MohamedGabr,HitokazuMatsushita,
ceedingsofthe13thInternationalJointConference
YoungJinKim,MohamedAfify,andHanyHassan
onNaturalLanguageProcessingandthe3rdConfer- Awadalla. 2023. How good are gpt models at ma-
enceoftheAsia-PacificChapteroftheAssociation chinetranslation?acomprehensiveevaluation. arXiv
forComputationalLinguistics(Volume1: LongPa- preprintarXiv:2302.09210.
pers),pages675–718.
MohammadJavadHosseini,HannanehHajishirzi,Oren
Lisa Bortolotti. 2011. Does reflection lead to wise Etzioni,andNateKushman.2014. Learningtosolve
choices? Philosophical Explorations, 14(3):297– arithmeticwordproblemswithverbcategorization.
| 313. |     |     |     |     |     | InProceedingsofthe2014ConferenceonEmpirical |     |     |     |     |     |     |
| ---- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- |

MethodsinNaturalLanguageProcessing(EMNLP), Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao,
| pages523–533. |     |     |     |     |     | AbuAwalMdShoeb,AbubakarAbid,AdamFisch, |     |     |     |     |     |
| ------------- | --- | --- | --- | --- | --- | -------------------------------------- | --- | --- | --- | --- | --- |
AdamRBrown,AdamSantoro,AdityaGupta,Adrià
|     |     |     |     |     |     | Garriga-Alonso, |     | et al. 2023. | Beyond | the | imitation |
| --- | --- | --- | --- | --- | --- | --------------- | --- | ------------ | ------ | --- | --------- |
WenxiangJiao,WenxuanWang,Jen-tseHuang,Xing
Wang,ShumingShi,andZhaopengTu.2023. Ischat- game: Quantifying and extrapolating the capabili-
gptagoodtranslator? yeswithgpt-4astheengine. tiesoflanguagemodels. TransactionsonMachine
| arXivpreprintarXiv:2301.08745. |     |                            |                       |     |     | LearningResearch. |            |                              |            |        |              |
| ------------------------------ | --- | -------------------------- | --------------------- | --- | --- | ----------------- | ---------- | ---------------------------- | ---------- | ------ | ------------ |
|                                |     |                            |                       |     |     | Mirac Suzgun,     | Nathan     | Scales,                      | Nathanael  |        | Schärli, Se- |
| MachielKeestra.2017.           |     | Metacognitionandreflection |                       |     |     |                   |            |                              |            |        |              |
|                                |     |                            |                       |     |     | bastian           | Gehrmann,  | Yi                           | Tay, Hyung | Won    | Chung,       |
| byinterdisciplinaryexperts:    |     |                            | Insightsfromcognitive |     |     |                   |            |                              |            |        |              |
|                                |     |                            |                       |     |     | Aakanksha         | Chowdhery, |                              | Quoc       | Le, Ed | Chi, Denny   |
| scienceandphilosophy.          |     | IssuesinInterdisciplinary  |                       |     |     |                   |            |                              |            |        |              |
|                                |     |                            |                       |     |     | Zhou,etal.2023.   |            | Challengingbig-benchtasksand |            |        |              |
Studies,35:121–169.
|     |     |     |     |     |     | whetherchain-of-thoughtcansolvethem. |     |     |     |     | InFind- |
| --- | --- | --- | --- | --- | --- | ------------------------------------ | --- | --- | --- | --- | ------- |
ingsoftheAssociationforComputationalLinguistics:
TakeshiKojima,ShixiangShaneGu,MachelReid,Yu-
ACL2023,pages13003–13051.
| takaMatsuo,andYusukeIwasawa.2022. |     |     |     |            | Largelan- |     |     |     |     |     |     |
| --------------------------------- | --- | --- | --- | ---------- | --------- | --- | --- | --- | --- | --- | --- |
| guagemodelsarezero-shotreasoners. |     |     |     | Advancesin |           |     |     |     |     |     |     |
PeiyiWang,LeiLi,LiangChen,ZefanCai,DaweiZhu,
neural information processing systems, 35:22199– BinghuaiLin,YunboCao,QiLiu,TianyuLiu,and
| 22213. |     |     |     |     |     | ZhifangSui.2023. |     | Largelanguagemodelsarenot      |     |     |     |
| ------ | --- | --- | --- | --- | --- | ---------------- | --- | ------------------------------ | --- | --- | --- |
|        |     |     |     |     |     | fairevaluators.  |     | arXivpreprintarXiv:2305.17926. |     |     |     |
YuqingKong,YunqiLi,YuboZhang,ZhihuanHuang,
andJinzhaoWu.2022. Elicitingthinkinghierarchy XuezhiWang,JasonWei,DaleSchuurmans,QuocLe,
without a prior. Advances in Neural Information EdChi,SharanNarang,AakankshaChowdhery,and
ProcessingSystems,35:13329–13341. DennyZhou.2022. Self-consistencyimproveschain
|     |     |     |     |     |     | of thought | reasoning | in  | language | models. | arXiv |
| --- | --- | --- | --- | --- | --- | ---------- | --------- | --- | -------- | ------- | ----- |
preprintarXiv:2203.11171.
NelsonFLiu,KevinLin,JohnHewitt,AshwinParan-
jape,MicheleBevilacqua,FabioPetroni,andPercy
JasonWei,XuezhiWang,DaleSchuurmans,Maarten
| Liang.2024. | Lostinthemiddle: |     | Howlanguagemod- |     |     |     |     |     |     |     |     |
| ----------- | ---------------- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
Bosma,FeiXia,EdChi,QuocVLe,DennyZhou,
| elsuselongcontexts. |     | TransactionsoftheAssociation |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
forComputationalLinguistics,12:157–173. etal.2022. Chain-of-thoughtpromptingelicitsrea-
|     |     |     |     |     |     | soninginlargelanguagemodels. |     |     |     | Advancesinneural |     |
| --- | --- | --- | --- | --- | --- | ---------------------------- | --- | --- | --- | ---------------- | --- |
informationprocessingsystems,35:24824–24837.
| AmanMadaan, | NiketTandon,PrakharGupta,Skyler |       |            |     |           |     |     |     |     |     |     |
| ----------- | ------------------------------- | ----- | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- |
| Hallinan,   | Luyu Gao,                       | Sarah | Wiegreffe, |     | Uri Alon, |     |     |     |     |     |     |
HaoranWu,WenxuanWang,YuxuanWan,Wenxiang
| Nouha | Dziri, Shrimai | Prabhumoye, |     | Yiming | Yang, |                          |     |     |                     |     |     |
| ----- | -------------- | ----------- | --- | ------ | ----- | ------------------------ | --- | --- | ------------------- | --- | --- |
|       |                |             |     |        |       | Jiao,andMichaelLyu.2023. |     |     | Chatgptorgrammarly? |     |     |
et al. 2024. Self-refine: Iterative refinement with evaluatingchatgptongrammaticalerrorcorrection
| self-feedback. | AdvancesinNeuralInformationPro- |     |     |     |     |            |                                |     |     |     |     |
| -------------- | ------------------------------- | --- | --- | --- | --- | ---------- | ------------------------------ | --- | --- | --- | --- |
|                |                                 |     |     |     |     | benchmark. | arXivpreprintarXiv:2303.13648. |     |     |     |     |
cessingSystems,36.
KaiXiong,XiaoDing,YixinCao,TingLiu,andBing
JoonSungPark,JosephO’Brien,CarrieJunCai,Mered- Qin.2023. Divingintotheinter-consistencyoflarge
ithRingelMorris,PercyLiang,andMichaelSBern- languagemodels: Aninsightfulanalysisthroughde-
stein.2023. Generativeagents: Interactivesimulacra bate. arXivpreprintarXiv:2305.11595.
| ofhumanbehavior. |     | InProceedingsofthe36thAn- |     |     |     |     |     |     |     |     |     |
| ---------------- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
nual ACM Symposium on User Interface Software Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran,
andTechnology,pages1–22. TomGriffiths,YuanCao,andKarthikNarasimhan.
|     |     |     |     |     |     | 2024. Treeofthoughts: |     |     | Deliberateproblemsolving |     |     |
| --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | ------------------------ | --- | --- |
JonathanPilault,XavierGarcia,ArthurBražinskas,and with large language models. Advances in Neural
OrhanFirat.2023. Interactive-chain-prompting: Am- InformationProcessingSystems,36.
biguityresolutionforcrosslingualconditionalgen-
HaiyanYin,DingchengLi,XuLi,andPingLi.2020.
| erationwithinteraction. |     | InProceedingsofthe13th |     |     |     |              |                                  |     |     |     |     |
| ----------------------- | --- | ---------------------- | --- | --- | --- | ------------ | -------------------------------- | --- | --- | --- | --- |
|                         |     |                        |     |     |     | Meta-cotgan: | Ametacooperativetrainingparadigm |     |     |     |     |
InternationalJointConferenceonNaturalLanguage
|     |     |     |     |     |     | for improving | adversarial |     | text | generation. | In Pro- |
| --- | --- | --- | --- | --- | --- | ------------- | ----------- | --- | ---- | ----------- | ------- |
Processingandthe3rdConferenceoftheAsia-Pacific
ceedingsoftheAAAIConferenceonArtificialIntelli-
| Chapter | of the Association |     | for Computational |     | Lin- |     |     |     |     |     |     |
| ------- | ------------------ | --- | ----------------- | --- | ---- | --- | --- | --- | --- | --- | --- |
guistics(Volume1: LongPapers),pages455–483. gence,volume34,pages9466–9473.
OriYoran,TomerWolfson,BenBogin,UriKatz,Daniel
| SubhroRoyandDanRoth.2015. |           |                | Solvinggeneralarith- |     |          |         |              |         |     |       |           |
| ------------------------- | --------- | -------------- | -------------------- | --- | -------- | ------- | ------------ | ------- | --- | ----- | --------- |
|                           |           |                |                      |     |          | Deutch, | and Jonathan | Berant. |     | 2023. | Answering |
| metic word                | problems. | In Proceedings |                      | of  | the 2015 |         |              |         |     |       |           |
questionsbymeta-reasoningovermultiplechainsof
| Conference | on Empirical | Methods |     | in Natural | Lan- |          |                                    |     |     |     |     |
| ---------- | ------------ | ------- | --- | ---------- | ---- | -------- | ---------------------------------- | --- | --- | --- | --- |
|            |              |         |     |            |      | thought. | InProceedingsofthe2023Conferenceon |     |     |     |     |
guageProcessing,pages1743–1752. EmpiricalMethodsinNaturalLanguageProcessing,
pages5942–5966.
| Noah Shinn, | Federico | Cassano, | Ashwin |     | Gopinath, |     |     |     |     |     |     |
| ----------- | -------- | -------- | ------ | --- | --------- | --- | --- | --- | --- | --- | --- |
Karthik Narasimhan, and Shunyu Yao. 2024. Re- Zhuosheng Zhang, Aston Zhang, Mu Li, and Alex
flexion: Languageagentswithverbalreinforcement Smola. 2022. Automatic chain of thought prompt-
learning. AdvancesinNeuralInformationProcess- ing in large language models. arXiv preprint
| ingSystems,36. |     |     |     |     |     | arXiv:2210.03493. |     |     |     |     |     |
| -------------- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- |

ChuanyangZheng,ZhengyingLiu,EnzeXie,Zhenguo
| Li, and                                 | Yu Li. 2023. | Progressive-hint | prompting |
| --------------------------------------- | ------------ | ---------------- | --------- |
| improvesreasoninginlargelanguagemodels. |              |                  | arXiv     |
preprintarXiv:2304.09797.
XinyuZhu,JunjieWang,LinZhang,YuxiangZhang,
YongfengHuang,JiaxingZhang,YujiuYang,etal.
| 2023a.                          | Solvingmathwordproblemsviacooperative |     |              |
| ------------------------------- | ------------------------------------- | --- | ------------ |
| reasoninginducedlanguagemodels. |                                       |     | InThe61stAn- |
nualMeetingOfTheAssociationForComputational
Linguistics.
| Xinyu Zhu, | Cheng Yang,    | Bei Chen, Siheng | Li, Jian-    |
| ---------- | -------------- | ---------------- | ------------ |
| Guang      | Lou, and Yujiu | Yang. 2023b.     | Question an- |
sweringasprogrammingforsolvingtime-sensitive
| questions. | InProceedingsofthe2023Conferenceon |     |     |
| ---------- | ---------------------------------- | --- | --- |
EmpiricalMethodsinNaturalLanguageProcessing,
pages12775–12790.
XizhouZhu,YuntaoChen,HaoTian,ChenxinTao,Wei-
jieSu,ChenyuYang,GaoHuang,BinLi,LeweiLu,
| XiaogangWang,etal.2023c. |     | Ghostintheminecraft: |     |
| ------------------------ | --- | -------------------- | --- |
Generallycapableagentsforopen-worldenviroments
vialargelanguagemodelswithtext-basedknowledge
| andmemory. | arXivpreprintarXiv:2305.17144. |     |     |
| ---------- | ------------------------------ | --- | --- |

A ChallengingTestbeds
We conduct experiments on two challenging tasks, namely, commonsense machine translation (i.e.,
CommonMT),andcounter-intuitivearithmeticreasoning(i.e.,Counter-IntuitiveAR),whichrequiredeep
levelsofcontemplationforLLMs.
A.1 CommonsenseMachineTranslation
AmbiguityType SourceSentence CorrectReference IncorrectTranslation
吃掉敌人一个师。 Destroyadivisionoftheenemy. Eatupanenemydivision.
Lexical
他喜欢吃苹果。 Helikestoeatapples. Helikestodestoryapples.
正在手术的是健康的 Ahealthydoctorisdoingsurgery. Whatisundergoingsurgeryisa
医生。 doctorwhoishealthy.
Contextless
正在手术的是生命垂 Whatisundergoingsurgeryisapa- Apatientwhoselifeisdyingis
危的病人。 tientwhoselifeisdying. doingsurgery.
当 地 震 袭 击 中 国 When the earthquake hit China, WhentheearthquakehitChina,
时，援助的是中国。 Chinawasaided. Chinahasassisted.
Contextual
当 地 震 袭 击 日 本 When the earthquake hit Japan, WhentheearthquakehitJapan,
时，援助的是中国。 Chinahasassisted. Chinawasaided.
Table8: Examplesoflexical,contextualandcontextlesssyntacticambiguityfromtheCommonMTdataset. The
underlinedChinesewordsaretranslatedintothecorrespondingcoloredwordsinEnglish. Bestviewedincolor.
The Common MT dataset is composed of Chinese⇒English translation examples (He et al., 2020),
whichareusedtoexaminethreetypesofambiguityresolutionabilitiesoftranslationmodels. Specifically,
TheCommonMTtestsetweusedcovers200examplesoflexicalambiguity,450examplesofcontextless
syntacticambiguity, and350examplesofcontextualsyntacticambiguity. Withinthechallengingpart
of Common MT, the authentic translation of each source sentence requires a proper understanding of
common sense knowledge. While these ambiguous sentences might appear to have a straightforward
translation,suchaliteralinterpretationiserroneous. Failuretoidentifyandaddresssuchambiguitiesmay
resultininaccuratetranslations.
Table8listssomeexamplesofthesethreetypesofambiguity. Lexicalambiguityreferstowordswith
multiplemeaningsindifferentcontexts. Contextlessandcontextualsyntacticambiguityinvolvesentences
withmultipleinterpretations,whichcanberesolvedbycontextorcommonsense. Asthelexicalambiguity
of“吃掉敌人一个师”shows,thesourceword“吃掉”shouldbetranslatedto“destroy”ratherthanthe
straightforwardtranslation“eatup”byconsideringthecommonsenseintherealworld.
A.2 Counter-IntuitiveArithmeticReasoning
Previousstudiesonthinkinghierarchy(Daniel,2017)suggestthatwehumanshaveafastandintuitive
systemandaslowandlogicalsystem,andtendtorunthelowerlevelsystembeforethehigherlevelone.
Inspiredbythis,wecreatedamorechallengingdatasetnamedCounter-IntuitiveArithmeticReasoning
(CIAR)toevaluatethereasoningabilitiesofLLMsatdeeplevels.
DatasetDescription. OurCounter-IntuitiveARdatasetcontains200questionscollectedfromelicitation
questions(Kongetal.,2022)8,webdata9 andadditionalmanualderivativesofthesequestions. Compared
tothecommonly-useddatasets,e.g.,MultiArith(RoyandRoth,2015),GSM8K(Cobbeetal.,2021),our
datasetpresentstwodistinctchallenges:
• ResistancetoIntuition. Thequestionsinourdatasetareembeddedinhiddentrapsdesignedtoelicit
intuitiveandappealinganswersthatareoftenincorrect. ThisfeatureevaluatestheabilitiesofLLMsto
resistthetrapsofsuperficialexpressions.
8https://elicitation.info/questionnaire/1/
9https://www.geeksforgeeks.org/puzzles/

Components Content
Question WhenAlicewalksupthehill,herspeedis1m/sandwhenshegoesdownthe
hill,herspeedis3m/s. ThenwhenAlicewalksupanddownthehill,whatis
heraveragespeed?
CorrectAnswer 1.5m/s
Explanation IfAlicecoversadistanceofdgoingupanddownthehill,thenhertotaldistance
is2d. Hertimegoingupthehillisd/1=d,andhertimegoingdownthehillis
d/3. So,hertotaltimeisd+d/3=4d/3. Therefore,heraveragespeedis2d/
(4d/3)=3/2m/s.
IncorrectAnswer 2m/s
Explanation Alice’saveragespeedcanbecalculatedbyaddingherspeedgoingupthehill
andherspeedgoingdownthehill,andthendividingby2. So,(1m/s+3m/s)/
2=2m/s. Therefore,Alice’saveragespeedis2m/s.
Table9: AnexampleinCounter-IntuitiveARdataset.
• Multi-StepReasoning. Eachcorrectanswerwithinthedatasetrequiresarigorousmulti-stepreasoning
process,therebyevaluatingthecapacityofLLMstoengageincomplexdecision-makingandproblem-
solving.
DatasetFormat. InourCounter-IntuitiveARdataset,eachexamplecontainsthreekeycomponents
(seeTable9foranexample). Weelaborateonthedetailsbelow:
• Questions. Thequestionsinourdatasetaredesignedtostimulatecounter-intuitivethinking, which
aimstochallengeconventionaldecision-makingbypresentingsituationswheretheimmediate,intuitive
responseisoftenincorrect.
• Answers. Eachquestionisprovidedwithacorrectanswer,whichrequiresdeepcomprehensionofthe
questionandcommonsenseknowledge. Additionally,wealsoprovideaplausibleyetincorrectanswer
forcomparison.
• Explanations. Weoffercomprehensiveexplanationsforeachcorrectanswer,detailingthestep-by-step
rationale that leads to the right solution. We also provide the seemingly logical reasoning process
behindincorrectanswers. Thisreasoningprocesshighlightsthepotentialpitfallsandmisconceptions
duringdecision-making,especiallywhenintuitionisprioritizedoverrigorouslogicalreasoning.
ExperimentalSettings. Duringourexperiments,wedidnotutilizetheexplanationsfromthedataset.
We provided detailed explanations to facilitate subsequent researchers to understand how the correct
answerwasderived.
B HumanEvaluationDetails
Weimplementhumanevaluationasfollows:
• HumanScore: Werandomlyshuffledthedisplayorderofthetranslatedsentencesfromallmethodsin
ananonymousmanner. Then,employedthreeprofessionalhumantranslators(Krippendorff’sAlpha=
0.76)todirectlyassessallmethodstogether. Finally,wecalculatedtheaveragescoresforeachmethods.
• Bias: WealsofocusonwhetherthetranslationofspecificwordsinCommonMTconformstocommon-
sense. Table8listsanexampleoflexicalambiguity,wherethesourceword“吃掉”shouldbetranslated
to“destroy”ratherthanthestraightforwardtranslation“eatup”. Here,weaskedtheannotatorstolabel
eachsentenceas1(notconformingtocommonsense)or0(conformingtocommonsense),andreport
thedegreeofbiasforthewholetestset.

C Resultsonmathandsymbolicreasoningtasks
|     | MathReasoning | SymbolicReasoning(BBH) |     |
| --- | ------------- | ---------------------- | --- |
Method
|              | GSM AddSub | Penguin Date | ColoredObjects |
| ------------ | ---------- | ------------ | -------------- |
| CoT          | 70.2 87.3  | 58.9 56.4    | 57.2           |
| Self-Reflect | 70.8 87.6  | 61.0 58.0    | 58.0           |
| MAD          | 73.8 92.1  | 63.7 65.2    | 58.8           |
Table10: Comparisonofaccuracyonmath(e.g. GSM(Cobbeetal.,2021)andAddSub(Hosseinietal.,2014))and
symbolicreasoning(threedatasetsfromBig-Bench(Srivastavaetal.,2023;Suzgunetal.,2023)).
D PromptsforDifferentDebateLevels
Level Prompt
Bothsidesmustreachafullconsensusoneverypointofthedebate. Everystatement
0
mustbeagreeduponbybothsides.
Mostofthedebateshouldbecharacterizedbydisagreements,buttheremaystillbea
1
smallamountofconsensusonlesssignificantpoints.
It’snotnecessarytofullyagreewitheachother’sperspectives,asourobjectiveisto
2(Default)
findthecorrectanswer.
Bothsidesmustdisagreewitheachotheroneverypointofthedebate. Thereshould
3
benoconsensuswhatsoever.
Table11: Promptsfordifferentlevelsof“titfortat”state. Wemodulatethelevelof“titfortat”stateoutlinedin
Section2throughappendingnaturallanguageinstructionstothedebaters’metaprompt.
E ExtraComputationalCost
|          | Method Cost(#GeneratedTokens)                     |       |     |
| -------- | ------------------------------------------------- | ----- | --- |
|          | COT                                               | 1.0   |     |
|          | Self-Reflect                                      | 1.83× |     |
|          | MAD                                               | 2.46× |     |
| Table12: | Extrageneratedtokensonthecounter-intuitiveARtask. |       |     |
We measure the inference cost by the number of generated tokens. As listed in Table 12, the self-
reflectioncostis1.83timesthatofthebaselineCOTmethod. Meanwhile,ourMADapproachincursan
additional0.63timestheinferencecost. Thisincreaseincostisdeemedacceptablegiventhesignificant
benefitourapproachoffersinenhancingLLMs’divergentthinkingcapabilitieswithoutrequiringexternal
signals(interactionwithhumans).

F DebateProcess
F.1 CommonsenseMachineTranslation
Table 13presentsthedebateprocessofexampletranslationdiscussedinSection3.3. Inthisdebate,both
sidesdisputedtheEnglishtranslationoftheChinesesentence“吃掉敌人一个师”. Theaffirmativeside
proposed“eatupanenemydivision”,advocatingforamoreliteraltranslationtodepicttheconsumption
ordevouringoftheenemy. Incontrast,thenegativesidesuggested“eliminateanenemydivision”,arguing
thisexpressionbetterconveysthedestructionoftheenemyinamilitarycontext. Afterthedebate,the
judgefavored“eliminate”,asitaccuratelyreflectedtheseverityandintentoftheoriginalmilitarylanguage.
This debate highlights the complexities of translation, where context and nuance significantly impact
theselectionofappropriatewords. Inresponsetothisissue,ourMADmethodhelpsLLMsunderstand
semanticscorrectlyandgeneratehighlyauthentictranslations.
<DebateTopic>: WhatisthecorrectEnglishtranslationofthefollowingtext: 吃掉敌人一个师?
IbelievethecorrecttranslationoftheChinesetext“吃掉敌人一个师”is“Eatupanenemy
division.” Theword“吃掉”literallymeans“eatup”or“consume.”
I disagree with your translation. I believe the correct translation of the Chinese text “吃掉
敌人一个师” is “Eliminate an enemy division.” While “吃掉” can be translated as “eat up” or
“consume”,itcanalsomean“eliminate”or“annihilate”inamilitarycontext. Inthiscase,itismore
appropriatetouse“eliminate”asitconveystheideaofcompletelydestroyingtheenemydivision.
Bothsidespresentedvalidargumentsandtranslationsthataccuratelyconveythemeaningof
theoriginalChinesetext. Thechoicebetween“eatup”and“eliminate”maydependonthecontext
andtoneofthetext. Therefore,thereisnoclearpreferenceforeithersideatthistime.
While“eliminate”doesconveytheideaofcompletelydestroyingtheenemydivision,itdoesn’t
capturetheconnotationofconsumingordevouringtheenemythatisimpliedby“吃掉”.
Inamilitarycontext,“吃掉”isoftenusedtodescribethecompletedestructionoftheenemy,
ratherthantheconsumptionoftheirresourcesorterritory.
Bothsidespresentedvalidarguments,butthenegativeside’sargumentthat“eliminate”better
capturestheintensityandseriousnessofthemilitarylanguageusedintheoriginalChinesetextwas
moreconvincing. Additionally,“eliminate”accuratelyconveystheideaofcompletelydestroying
theenemydivision. Therefore,thecorrectEnglishtranslationoftheChinesetext“吃掉敌人一个
师”is“Eliminateanenemydivision.”
Table13: ThedebateprocessoftranslationexampleonChinesesentence“吃掉敌人一个师”.

F.2 Counter-IntuitiveArithmeticReasoning
Table14showsthedebateprocessofexampleanswerinTable9. ThisdebateisaboutcalculatingAlice’s
averagespeedwhilewalkingupanddownahill,withspeedsgivenas1m/suphilland3m/sdownhill.
Initially,itwasincorrectlyproposedbyaffirmativesidetojustaveragetheuphillanddownhillspeeds. The
negativeside,whichiscorrect,statesthataveragespeedistotaldistancedividedbytotaltime. Giventhat
thedistancesupanddownthehillareequal,wemustcalculatethetotaltimetakenforthetwodirections
beforefindingtheaveragespeed. Therefore,theaveragespeediscalculatedusingthesumoftheuphill
anddownhilldistances(twicethedistanceofthehill)andthesumofthetimetakenforeach(d/1foruphill
andd/3fordownhill). Thisleadstoanaveragespeedof1.5m/s,not2m/sastheaffirmativesideproposed.
Andthejudgealsosupportstheresponsefromthenegativeside. Here,LLMsmadeacommonmistake
initiallyinunderstandingtheconceptofaveragespeed. OurMADmethodencouragesdivergentthinking
andeffectivelypreventsintuitivebutincorrectresponses,leadingtothecorrectmethodforcalculating
averagespeed.
<DebateTopic>: WhenAlicewalksupthehill,herspeedis1m/sandwhenshegoesdownthe
hill,herspeedis3m/s. ThenwhenAlicewalksupanddownthehill,whatisheraveragespeed?
Alice’saveragespeedcanbecalculatedbyaddingherspeedgoingupthehillandherspeed
goingdownthehill,andthendividingby2. So,(1m/s+3m/s)/2=2m/s. Therefore,Alice’s
averagespeedis2m/s.
Idisagreewithyouranswer. Theproblemdoesn’tgiveusanyinformationaboutthedistance
Alicecoverswhilegoingupanddownthehill. So,wecannotsimplyaddherspeedsanddivideby
2togetheraveragespeed. Weneedtoknowthedistanceshecoverstocalculateheraveragespeed.
Theaveragespeediscalculatedbydividingthetotaldistancebythetotaltimetaken. AsAlice
walksupanddownthehill,thedistancecoveredinbothdirectionsisthesame. Therefore,thetotal
distancecoveredis2timesthedistanceofeitherdirection.
That’sagoodpoint. ButwecanassumethatAlicecoversthesamedistancegoingupanddown
thehill. Inthatcase,wecanusetheformulaforaveragespeed,whichistotaldistancedividedby
totaltime. IfAlicecoversadistanceofdgoingupanddownthehill,thenhertotaldistanceis2d.
Hertimegoingupthehillisd/1=d,andhertimegoingdownthehillisd/3. So,hertotaltimeisd
+d/3=4d/3. Therefore,heraveragespeedis2d/(4d/3)=3/2m/s.
Thankyouforprovidingyouranswer. Thisaveragespeedof1.5m/stakesintoaccountboth
theuphillanddownhillspeeds,providingabalancedrepresentationofAlice’soverallperformance
whilewalkingupanddownthehill.
Yes. Let’sassumethedistanceisd. Thetimetakentowalkupthehillisd/1andthetimetaken
towalkdownthehillisd/3. Thetotaltimetakenisd/1+d/3=4d/3. Therefore,theaveragespeed
is(2d)/(4d/3)=1.5m/s. Hence,thenegativesideiscorrect.
Table14: Thedebateprocessofarithmeticreasoningexample.