<!-- AGENT BLUEPRINT METADATA START -->
# SELF-REFINE: Iterative Refinement with Self-Feedback

- Year: 2023
- Primary chapter: Reasoning and Planning
- Method category: draft-critique-revise loop
- Practical role: cheap iterative improvement pattern for structured outputs
- Key contribution: Turns critique into a lightweight improvement loop without changing the core topology much.
- Major limitation: Can polish weak outputs without truly grounding them if verification is absent.
- Confidence: High
- Canonical link: https://arxiv.org/abs/2303.17651

<!-- AGENT BLUEPRINT METADATA END -->

## Thesis

Self-Refine proposes a simple draft-critique-revise loop in which the same model generates an answer, critiques it, and then improves it iteratively. The core claim is that many outputs can be improved substantially at test time without retraining or external reward models.

## What It Contributes

The paper turns self-critique into a lightweight optimization pattern that is cheap to add to existing workflows. It shows that iterative refinement can improve quality across several tasks while preserving a simple system topology.

## Why It Matters In This Repo

This repo uses Self-Refine as the default "near-miss improvement" pattern. It is especially useful when an initial answer is directionally correct but weak in structure, clarity, or completeness, and when the task does not justify heavier search methods.

## Limitations

Self-Refine can polish a wrong answer into a cleaner wrong answer if the workflow lacks grounding or verification. It is best for improving output quality, not for solving tasks that fundamentally need external state or formal planning.

## Design Takeaways

- Use it after a first pass when outputs are close but not good enough.
- Keep the critique targeted so the loop improves specific weaknesses instead of wandering.
- Do not rely on refinement alone for factual or action-heavy tasks; add verification or environment checks.

## Raw Local Extraction

SELF-REFINE:
| Iterative |     | Refinement |     |     | with | Self-Feedback |     |     |     |
| --------- | --- | ---------- | --- | --- | ---- | ------------- | --- | --- | --- |
AmanMadaan1,NiketTandon2,PrakharGupta1,SkylerHallinan3,LuyuGao1,
SarahWiegreffe2,UriAlon1,NouhaDziri2,ShrimaiPrabhumoye4,YimingYang1,
ShashankGupta2,BodhisattwaPrasadMajumder5,KatherineHermann6,
3202 yaM 52  ]LC.sc[  2v15671.3032:viXra
SeanWelleck2,3,AmirYazdanbakhsh6,PeterClark2
1LanguageTechnologiesInstitute,CarnegieMellonUniversity
2AllenInstituteforArtificialIntelligence
3UniversityofWashington 4NVIDIA 5UCSanDiego6GoogleResearch,BrainTeam
|     |     | amadaan@cs.cmu.edu, |     |     | nikett@allenai.org |     |     |     |     |
| --- | --- | ------------------- | --- | --- | ------------------ | --- | --- | --- | --- |
Abstract
| Like humans,           | large | language |                                             | models | (LLMs) | do not | always | generate | the best |
| ---------------------- | ----- | -------- | ------------------------------------------- | ------ | ------ | ------ | ------ | -------- | -------- |
| outputontheirfirsttry. |       |          | Motivatedbyhowhumansrefinetheirwrittentext, |        |        |        |        |          | we       |
introduceSELF-REFINE,anapproachforimprovinginitialoutputsfromLLMs
| throughiterativefeedbackandrefinement. |     |     |     |     | Themainideaistogenerateaninitial |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | -------------------------------- | --- | --- | --- | --- |
outputusinganLLM;then,thesameLLMprovidesfeedbackforitsoutputand
| usesittorefineitself,iteratively. |                  |                |                               | SELF-REFINEdoesnotrequireanysupervised |               |             |           |            |          |
| --------------------------------- | ---------------- | -------------- | ----------------------------- | -------------------------------------- | ------------- | ----------- | --------- | ---------- | -------- |
| training                          | data, additional |                | training,                     | or                                     | reinforcement | learning,   | and       | instead    | uses a   |
| single LLM                        | as               | the generator, |                               | refiner                                | and the       | feedback    | provider. | We         | evaluate |
| SELF-REFINE                       |                  | across 7       | diverse                       | tasks,                                 | ranging       | from dialog | response  | generation |          |
| tomathematicalreasoning,          |                  |                | usingstate-of-the-art(GPT-3.5 |                                        |               |             | andGPT-4) |            | LLMs.    |
Acrossallevaluatedtasks,outputsgeneratedwithSELF-REFINEarepreferredby
| humansandautomaticmetricsoverthosegeneratedwiththesame |     |     |     |     |     |     |     | LLM | using |
| ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
conventionalone-stepgeneration,improvingby∼20%absoluteonaverageintask
| performance. | Ourworkdemonstratesthatevenstate-of-the-artLLMslikeGPT-4 |     |     |     |     |     |     |     |     |
| ------------ | -------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
canbefurtherimprovedattest-timeusingoursimple,standaloneapproach.1.
1 Introduction
Although large language models (LLMs) can generate coherent outputs, they often fall short in
addressing intricate requirements. This mostly includes tasks with multifaceted objectives, such
as dialogue response generation, or tasks with hard-to-define goals, such as enhancing program
readability. Inthesescenarios,modern LLMsmayproduceanintelligibleinitialoutput,yetmay
benefitfromfurtheriterativerefinement—i.e.,iterativelymappingacandidateoutputtoanimproved
one—toensurethatthedesiredqualityisachieved. Iterativerefinementtypicallyinvolvestraining
arefinementmodelthatreliesondomain-specificdata(e.g.,ReidandNeubig(2022);Schicketal.
(2022a);Wellecketal.(2022)). Otherapproachesthatrelyonexternalsupervisionorrewardmodels
requirelargetrainingsetsorexpensivehumanannotations (Madaanetal.,2021;Ouyangetal.,2022),
whichmaynotalwaysbefeasibletoobtain. Theselimitationsunderscoretheneedforaneffective
refinementapproachthatcanbeappliedtovarioustaskswithoutrequiringextensivesupervision.
Iterativeself-refinementisafundamentalcharacteristicofhumanproblem-solving(Simon,1962;
FlowerandHayes,1981;Amabile,1983). Iterativeself-refinementisaprocessthatinvolvescreating
aninitialdraftandsubsequentlyrefiningitbasedonself-providedfeedback. Forexample,when
1Codeanddataathttps://selfrefine.info/
Preprint.Underreview.

Input
0
Feedback Refine
Model M
1 2
Use M to get feedback on its own output Use M to refine its previous output, given its feedback
Figure1: Givenaninput(⃝0),SELF-REFINEstartsbygeneratinganoutputandpassingitbacktothe
samemodelMtogetfeedback(⃝1). ThefeedbackispassedbacktoM,whichrefinesthepreviously
generatedoutput(⃝2). Steps(⃝1)and(⃝2)iterateuntilastoppingconditionismet. SELF-REFINEis
instantiatedwithalanguagemodelsuchasGPT-3.5anddoesnotinvolvehumanassistance.
draftinganemailtorequestadocumentfromacolleague,anindividualmayinitiallywriteadirect
request such as “Send me the data ASAP”. Upon reflection, however, the writer recognizes the
potentialimpolitenessofthephrasingandrevisesitto“HiAshley,couldyoupleasesendmethedata
atyourearliestconvenience?". Whenwritingcode,aprogrammermayimplementaninitial“quick
anddirty”implementation,andthen,uponreflection,refactortheircodetoasolutionthatismore
efficientandreadable. Inthispaper,wedemonstratethatLLMscanprovideiterativeself-refinement
withoutadditionaltraining,leadingtohigher-qualityoutputsonawiderangeoftasks.
WepresentSELF-REFINE: aniterativeself-refinementalgorithmthatalternatesbetweentwogener-
ativesteps–FEEDBACKandREFINE. Thesestepsworkintandemtogeneratehigh-qualityoutputs.
Given an initial output generated by a model M, we pass it back to the same model M to get
feedback. Then,thefeedbackispassedbacktothesamemodeltorefinethepreviously-generated
draft. ThisprocessisrepeatedeitherforaspecifiednumberofiterationsoruntilMdeterminesthat
nofurtherrefinementisnecessary. Weusefew-shotprompting(Brownetal.,2020)toguideMto
bothgeneratefeedbackandincorporatethefeedbackintoanimproveddraft. Figure1illustratesthe
high-levelidea,thatSELF-REFINEusesthesameunderlyinglanguagemodeltogeneratefeedback
andrefineitsoutputs.
We evaluate SELF-REFINE on 7 generation tasks that span diverse domains, including natural
languageandsource-codegeneration. WeshowthatSELF-REFINEoutperformsdirectgeneration
from strong LLMs like GPT-3.5 (text-davinci-003 and gpt-3.5-turbo; OpenAI; Ouyang
etal.,2022)andGPT-4(OpenAI,2023)by5-40%absoluteimprovement. Incode-generationtasks,
SELF-REFINEimprovestheinitialgenerationbyuptoabsolute13%whenappliedtostrongcode
modelssuchasCodex(code-davinci-002; Chenetal.,2021). Wereleaseallofourcode,which
iseasilyextensibletootherLLMs. Inessence, ourresultsshowthatevenwhenan LLM cannot
generateanoptimaloutputonitsfirsttry,theLLMcanoftenprovideusefulfeedbackandimprove
itsownoutputaccordingly. Inturn,SELF-REFINEprovidesaneffectivewaytoobtainbetteroutputs
fromasinglemodelwithoutanyadditionaltraining,viaiterative(self-)feedbackandrefinement.
2 IterativeRefinementwith SELF-REFINE
Givenaninputsequence,SELF-REFINEgeneratesaninitialoutput,providesfeedbackontheoutput,
and refines the output according to the feedback. SELF-REFINE iterates between feedback and
refinement until a desired condition is met. SELF-REFINE relies on a suitable language model
andthreeprompts(forinitialgeneration,feedback,andrefinement),anddoesnotrequiretraining.
SELF-REFINEisshowninFigure1andAlgorithm1. Next,wedescribeSELF-REFINEinmoredetail.
Initialgeneration Givenaninputx,promptp
gen
,andmodelM,SELF-REFINEgeneratesaninitial
outputy :
0
y =M(p ∥x). (1)
0 gen
2

(a)Dialogue:x,y
t
(b)FEEDBACK fb (c)REFINE y
t+1
User: I am interested Engaging: Provides no Response (refined): That's
in playing Table information about table great to hear (...) ! It's
tennis. tennis or how to play it. a fun sport requiring
quick reflexes and good
Response: I'm sure User understanding: Lacks hand-eye coordination.
it's a great way to understanding of user's Have you played before, or
socialize, stay active needs and state of mind. are you looking to learn?
(d)Codeoptimization:x,y
t
(e)FEEDBACK fb (f)REFINE y
t+1
Generate sum of 1, ..., N This code is slow as Code (refined)
def sum(n): it uses brute force.
res = 0 A better approach is def sum_faster(n):
for i in range(n+1): to use the formula return (n*(n+1))//2
res += i ... (n(n+1))/2.
return res
Figure2: ExamplesofSELF-REFINE: aninitialoutput generatedbythebaseLLMandthenpassed
backtothesameLLMtoreceivefeedback tothesameLLMtorefinetheoutput . Thetoprow
illustratesthisfordialoggenerationwhereaninitialdialogueresponsecanbetransformedintoa
moreengagingonethatalsounderstandstheuserbyapplyingfeedback. Thebottomrowillustrates
thisforcodeoptimizationwherethecodeismademoreefficientbyapplyingfeedback.
Algorithm1SELF-REFINEalgorithm
Require: inputx,modelM,prompts{p ,p ,p },stopconditionstop(·)
gen fb refine
1: y 0 =M(p gen ∥x) ▷Initialgeneration(Eqn.1)
2: foriterationt∈0,1,...do
3: fb t =M(p fb ∥x∥y t ) ▷Feedback(Eqn.2)
4: ifstop(fb t ,t)then ▷Stopcondition
5: break
6: else
7: y t+1 =M(p refine ∥x∥y 0 ∥fb 0 ∥...∥y t ∥fb t ) ▷Refine(Eqn.4)
8: endif
9: endfor
10: returny t
Figure3: TheSELF-REFINEalgorithm. See(§2)foradiscussionofeachcomponent.
For example, in Figure 2(d), the model generates functionally correct code for the given input.
Here,p isatask-specificfew-shotprompt(orinstruction)foraninitialgeneration,and∥denotes
gen
concatenation. Thefew-shotpromptcontainsinput-outputpairs⟨x(k),y(k)⟩forthetask.2
FEEDBACK Next, SELF-REFINE uses the same model M to provide feedback fb t on its own
output,givenatask-specificpromptp forgeneratingfeedback:
fb
fb =M(p ∥x∥y ). (2)
t fb t
Intuitively,thefeedbackmayaddressmultipleaspectsoftheoutput. Forexample,incodeoptimiza-
tion,thefeedbackmightaddresstheefficiency,readability,andoverallqualityofthecode.
2Few-shotprompting(alsoreferredtoas“in-contextlearning”)providesamodelwithapromptconsistingof
kin-contextexamplesofthetargettask,eachintheformofinput-outputpairs⟨x ,y ⟩(Brownetal.,2020).
i i
3

Here, thepromptp providesexamplesoffeedbackintheformofinput-output-feedbacktriples
fb
⟨x(k),y(k),fb(k)⟩. Wepromptthemodeltowritefeedbackthatisactionableandspecificviafb(k).
By‘actionable’,wemeanthefeedbackshouldcontainaconcreteactionthatwouldlikelyimprovethe
output. By‘specific’,wemeanthefeedbackshouldidentifyconcretephrasesintheoutputtochange.
Forexample,thefeedbackinFigure2(e)is“Thiscodeisslowasitusesaforloopwhichisbrute
force. Abetterapproachistousetheformula... (n(n+1))/2”. Thisfeedbackisactionable,sinceit
suggeststheaction‘usetheformula...’. Thefeedbackisspecificsinceitmentionsthe‘forloop’.
REFINE Next,SELF-REFINEusesMtorefineitsmostrecentoutput,givenitsownfeedback:
y =M(p ∥x∥y ∥fb ). (3)
t+1 refine t t
Forexample,inFigure2(f),giventheinitialoutputandthegeneratedfeedback,themodelgenerates
a re-implementation that is shorter and runs much faster than the initial implementation. The
prompt p provides examples of improving the output based on the feedback, in the form of
refine
input-output-feedback-refinedquadruples⟨x(k),y(k),fb(k),y(k)⟩.
t t t+1
Iterating SELF-REFINE SELF-REFINE alternatesbetween FEEDBACK and REFINE stepsuntila
stoppingconditionismet. Thestoppingconditionstop(fb ,t)eitherstopsataspecifiedtimestept,
t
orextractsastoppingindicator(e.g. ascalarstopscore)fromthefeedback. Inpractice,themodel
canbepromptedtogenerateastoppingindicatorinp ,andtheconditionisdeterminedper-task.
fb
Toinformthemodelaboutthepreviousiterations,weretainthehistoryofpreviousfeedbackand
outputs by appending them to the prompt. Intuitively, this allows the model to learn from past
mistakesandavoidrepeatingthem. Moreprecisely,Equation(3)isinfactinstantiatedas:
y =M(p ∥x∥y ∥fb ∥...∥y ∥fb ). (4)
t+1 refine 0 0 t t
Finally,weusethelastrefinementy
t
astheoutputofSELF-REFINE.
Algorithm1summarizes SELF-REFINE,andFigure2showsanexampleof SELF-REFINE inthe
DialogueResponseGeneration(MehriandEskenazi,2020)andCodeOptimization(Madaanetal.,
2023)tasks. AppendixSprovidesexamplesofthep ,p ,p promptsforvarioustasks. Thekey
gen fb refine
ideaisthatSELF-REFINEusesthesameunderlyingLLMtogenerate,getfeedback,andrefineits
outputsgivenitsownfeedback. Itreliesonlyonsupervisionpresentinthefew-shotexamples.
3 Evaluation
WeevaluateSELF-REFINEon7diversetasks: DialogueResponseGeneration(AppendixM; Mehri
and Eskenazi, 2020), Code Optimization (Appendix N; Madaan et al., 2023), Code Readability
Improvement(AppendixL; Purietal.,2021),MathReasoning(AppendixO; Cobbeetal.,2021),
SentimentReversal(AppendixP; Zhangetal.,2015),andweintroducetwonewtasks: Acronym
Generation(AppendixQ)andConstrainedGeneration(aharderversionofLinetal.(2020)with
20-30keywordconstraintsinsteadof3-5;AppendixR)
ExamplesforalltasksanddatasetstatisticsareprovidedinTable4(AppendixA).
3.1 InstantiatingSELF-REFINE
We instantiate SELF-REFINE following the high-level description in Section 2. The FEEDBACK-
REFINEiterationscontinueuntilthedesiredoutputqualityortask-specificcriterionisreached,uptoa
maximumof4iterations. Tomakeourevaluationconsistentacrossdifferentmodels,weimplemented
bothFEEDBACKandREFINEasfew-shotpromptsevenwithmodelsthatrespondwelltoinstructions,
suchasChatGPTandGPT-4.
BaseLLMs Ourmaingoalistoevaluatewhetherwecanimprovetheperformanceofanystrong
baseLLMsusingSELF-REFINE. Therefore,wecompareSELF-REFINEtothesamebaseLLMsbut
withoutfeedback-refineiterations. WeusedthreemainstrongbaseLLMacrossalltasks: GPT-3.5
(text-davinci-003),ChatGPT(gpt-3.5-turbo),andGPT-4(OpenAI,2023). Forcode-based
tasks,wealsoexperimentedwith CODEX (code-davinci-002). Inalltasks,either GPT-3.5 or
GPT-4 is the previous state-of-the-art.3 We used the same prompts from previous work when
3Acomparisonwithotherfew-shotandfine-tunedapproachesisprovidedinAppendixF
4

GPT-3.5 ChatGPT GPT-4
Task Base +SELF-REFINE Base +SELF-REFINE Base +SELF-REFINE
SentimentReversal 8.8 30.4(↑21.6) 11.4 43.2(↑31.8) 3.8 36.2(↑32.4)
DialogueResponse 36.4 63.6(↑27.2) 40.1 59.9(↑19.8) 25.4 74.6(↑49.2)
CodeOptimization 14.8 23.0(↑8.2) 23.9 27.5(↑3.6) 27.3 36.0(↑8.7)
CodeReadability 37.4 51.3(↑13.9) 27.7 63.1(↑35.4) 27.4 56.2(↑28.8)
MathReasoning 64.1 64.1(0) 74.8 75.0(↑0.2) 92.9 93.1(↑0.2)
AcronymGeneration 41.6 56.4(↑14.8) 27.2 37.2(↑10.0) 30.4 56.0(↑25.6)
ConstrainedGeneration 28.0 37.0(↑9.0) 44.0 67.0(↑23.0) 15.0 45.0(↑30.0)
Table1: SELF-REFINEresultsonvarioustasksusingGPT-3.5,ChatGPT,andGPT-4asbaseLLM.
SELF-REFINEconsistentlyimprovesLLM.MetricsusedforthesetasksaredefinedinSection3.2.
available(suchasforCodeOptimizationandMathReasoning);otherwise,wecreatedpromptsas
detailedinAppendixS.Weusegreedydecodingwithatemperatureof0.7forallsetups.
3.2 Metrics
Wereportthreetypesofmetrics:
• Taskspecificmetric:Whenavailable,weuseautomatedmetricsfrompriorwork(MathReasoning:
%solverate;CodeOptimization: %programsoptimized;ConstrainedGen: coverage%)
• Human-pref: In Dialogue Response Generation, Code Readability Improvement, Sentiment
Reversal,andAcronymGeneration,sincenoautomatedmetricsareavailable,weperformablind
humanA/Bevaluationonasubsetoftheoutputstoselectthepreferredoutput. Additionaldetails
areprovidedinAppendixC.
• GPT-4-pref:Inadditiontohuman-pref,weuseGPT-4asaproxyforhumanpreferencefollowing
priorwork(Fuetal.,2023;Chiangetal.,2023;Gengetal.,2023;Sunetal.,2023),andfoundhigh
correlation(82%forSentimentReversal,68%forAcronymGeneration,and71%forDialogue
ResponseGeneration)withhuman-pref. ForCodeReadabilityImprovement,wepromptGPT-
4 to calculate fraction of the variables that are appropriately named given the context (e.g.,
x = []→input_buffer = []). AdditionaldetailsareprovidedinAppendixD.
3.3 Results
Table1showsourmainresults:
SELF-REFINEconsistentlyimprovesoverbasemodelsacrossallmodelsizes,andadditionally
outperforms the previous state-of-the-art across all tasks. For example, GPT-4+SELF-REFINE
improvesoverthebaseGPT-4by8.7%(absolute)inCodeOptimization,increasingoptimization
percentagefrom27.3%to36.0%. ConfidenceintervalsareprovidedinAppendixJ.Forcode-based
tasks,wefoundsimilartrendswhenusingCODEX;thoseresultsareincludedinAppendixF.
OneofthetasksinwhichweobservethehighestgainscomparedtothebasemodelsisConstrained
Generation,wherethemodelisaskedtogenerateasentencecontainingupto30givenconcepts. We
believethatthistaskbenefitssignificantlyfromSELF-REFINEbecausetherearemoreopportunities
tomisssomeoftheconceptsonthefirstattempt,andthus SELF-REFINE allowsthemodeltofix
thesemistakessubsequently. Further,thistaskhasanextremelylargenumberofreasonableoutputs,
andthusSELF-REFINEallowstobetterexplorethespaceofpossibleoutputs.
Inpreference-basedtaskssuchasDialogueResponseGeneration,SentimentReversal,andAcronym
Generation, SELF-REFINE leads to especially high gains. For example in Dialogue Response
Generation,GPT-4preferencescoreimproveby49.2%–from25.4%to74.6%. Similarly,wesee
remarkableimprovementsintheotherpreference-basedtasksacrossallmodels.
ThemodestperformancegainsinMathReasoningcanbetracedbacktotheinabilitytoaccurately
identifywhetherthereisanyerror. Inmath,errorscanbenuancedandsometimeslimitedtoasingle
line or incorrect operation. Besides, a consistent-looking reasoning chain can deceive LLMs to
5

thinkthat“everythinglooksgood”(e.g.,ChatGPTfeedbackfor94%instancesis’everythinglooks
good’). InAppendixH.1,weshowthatthegainswithSELF-REFINEonMathReasoningaremuch
bigger(5%+)ifanexternalsourcecanidentifyifthecurrentmathanswerisincorrect.
ImprovementisconsistentacrossbaseLLMssizesGenerally,GPT-4+SELF-REFINEperforms
better than GPT-3.5+SELF-REFINE and ChatGPT+SELF-REFINE across all tasks, even in tasks
wheretheinitialbaseresultsofGPT-4werelowerthanGPT-3.5orChatGPT.Wethusbelievethat
SELF-REFINEallowsstrongermodels(suchasGPT-4)tounlocktheirfullpotential,evenincases
wherethispotentialisnotexpressedinthestandard,single-pass,outputgeneration. Comparisonto
additionalstrongbaselinesisprovidedinAppendixF.
4 Analysis
ThethreemainstepsofSELF-REFINEareFEEDBACK,REFINE,andrepeatingthemiteratively. Inthis
section,weperformadditionalexperimentstoanalyzetheimportanceofeachofthesesteps.
Task SELF-REFINEfeedback Genericfeedback Nofeedback
CodeOptimization 27.5 26.0 24.8
SentimentReversal 43.2 31.2 0
AcronymGeneration 56.4 54.0 48.0
Table 2: Prompting to generate generic feedback (or having the model generate no feedback at
all) leads to reduced scores, indicating the importance of the FEEDBACK step of SELF-REFINE.
TheseexperimentswereperformedwithChatGPT(CodeOptimizationandSentimentReversal)and
GPT-3.5(AcronymGeneration),andmetricsusedaredefinedinSection3.2.
Theimpactofthefeedbackquality FeedbackqualityplaysacrucialroleinSELF-REFINE. To
quantifyitsimpact,wecompareSELF-REFINE,whichutilizesspecific,actionablefeedback,withtwo
ablations: oneusinggenericfeedbackandanotherwithoutfeedback(themodelmaystilliteratively
refineitsgenerations,butisnotexplicitlyprovidedfeedbacktodoso). Forexample,intheCode
Optimizationtask: actionablefeedback,suchasAvoidrepeatedcalculationsintheforloop,pinpoints
anissueandsuggestsaclearimprovement. Genericfeedback,likeImprovetheefficiencyofthecode,
lacksthisprecisionanddirection. Table2showsfeedback’sclearinfluence.
InCodeOptimization,performanceslightlydipsfrom27.5(SELF-REFINEfeedback)to26.0(generic
feedback),andfurtherto24.8(nofeedback). Thissuggeststhatwhilegenericfeedbackofferssome
guidance–specific,actionablefeedbackyieldssuperiorresults.
ThiseffectismorepronouncedintaskslikeSentimentTransfer,wherechangingfromourfeedback
togenericfeedbackleadstoasignificantperformancedrop(43.2to31.2),andthetaskfailswithout
feedback. Similarly,inAcronymGeneration,withoutactionablefeedback,performancedropsfrom
56.4 to 48.0, even with iterative refinements. These results highlight the importance of specific,
actionable feedback in our approach. Even generic feedback provides some benefit, but the best
resultsareachievedwithtargeted,constructivefeedback.
HowimportantarethemultipleiterationsofFEEDBACK-REFINE? Figure4demonstratesthat
onaverage,thequalityoftheoutputimprovesasthenumberofiterationsincreases. Forinstance,in
theCodeOptimizationtask,theinitialoutput(y )hasascoreof22.0,whichimprovesto28.8after
0
threeiterations(y ). Similarly,intheSentimentReversaltask,theinitialoutputhasascoreof33.9,
3
whichincreasesto36.8afterthreeiterations.ThistrendofimprovementisalsoevidentinConstrained
Generation,wherethescoreincreasesfrom29.0to49.7afterthreeiterations. Figure4highlights
thediminishingreturnsintheimprovementasthenumberofiterationsincreases. Overall,having
multipleFEEDBACK-REFINEiterationssignificantlyenhancesthequalityoftheoutput,althoughthe
marginalimprovementnaturallydecreaseswithmoreiterations.
Theperformancemaynotalwaysmonotonicallyincreasewithiterations: inmulti-aspectfeedback
taskslikeAcronymGeneration,wheretheoutputqualitycanvaryduringiterationwithimprovement
inoneaspectbutdeclineinanotheraspect. Tocounterthis,SELF-REFINEgeneratesnumericalscores
fordifferentqualityaspects,leadingtoabalancedevaluationandappropriateoutputselection.
6

11.3
C.Opt.
|      |     |     |          |     | 10  |     |     |     | C.Gen. |     |
| ---- | --- | --- | -------- | --- | --- | --- | --- | --- | ------ | --- |
| Task |     | y0  | y1 y2 y3 |     |     |     |     | 6.4 |        |     |
S.Rev.
5
| CodeOpt. |     | 22.0 | 27.0 27.9 28.8 |     | 5   |     |     |     |     |     |
| -------- | --- | ---- | -------------- | --- | --- | --- | --- | --- | --- | --- |
3
| SentimentRev.   |     | 33.9 | 34.9 36.1 36.8 |     |     |     |     |     |     |     |
| --------------- | --- | ---- | -------------- | --- | --- | --- | --- | --- | --- | --- |
|                 |     |      |                |     |     | 1   | 0.9 | 1.2 | 0.9 | 0.7 |
| ConstrainedGen. |     | 29.0 | 40.3 46.7 49.7 |     |     |     |     |     |     |     |
0
|     |     |     |     |     | ∆(y | →y ) | ∆(y | →y ) | ∆(y | →y ) |
| --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- | ---- |
|     |     |     |     |     | 0   | 1    |     | 1 2  |     | 2 3  |
Figure4: Left: Iteration-wisescoreimprovements. Earlyiterationssignificantlyimproveoutput
quality,andscoresgenerallykeepimprovingwithmoreiterations.Right: SELF-REFINEPerformance
improvementswithiterations. Mostgains(∆)areintheinitialiterationsforbothCodeOpt. andSenti-
mentReversal. ThenumbersareaveragedoverChatGPT,GPT-3.5,andGPT-4. Taskabbreviations:
C.Opt. (CodeOptimiz.),S.Rev. (SentimentReversal),C.Gen. (ConstrainedGeneration).
# Slower code
def solve(amount):
|            |     |           |           |       | # Faster           | code |     |     |     |     |
| ---------- | --- | --------- | --------- | ----- | ------------------ | ---- | --- | --- | --- | --- |
| best_price |     | = (amount | + 199) // | 200 * |                    |      |     |     |     |     |
|            |     |           |           |       | def solve(amount): |      |     |     |     |     |
380
| (cid:44)→ |                   |              |          |     | coins  | = [200,          | 300]               |           |     |     |
| --------- | ----------------- | ------------ | -------- | --- | ------ | ---------------- | ------------------ | --------- | --- | --- |
| #         | First loop        |              |          |     |        |                  |                    |           |     |     |
|           |                   |              |          |     | prices | =                | [380, 550]         |           |     |     |
| for       | a in range(amount |              | // 200 + | 1): |        |                  |                    |           |     |     |
|           |                   |              |          |     | dp     | = [float('inf')] |                    | * (amount | +   | 1)  |
|           | # ... 4           | nested loops | ...      |     |        |                  |                    |           |     |     |
|           |                   |              |          |     | dp[0]  | = 0              |                    |           |     |     |
|           | for c1 in         | range(amount | // 1500  | +   |        |                  |                    |           |     |     |
|           |                   |              |          |     | for    | i in             | range(len(coins)): |           |     |     |
1):
|     | (cid:44)→  |               |            |     | for    | j in       | range(coins[i], |              | amount+1): |     |
| --- | ---------- | ------------- | ---------- | --- | ------ | ---------- | --------------- | ------------ | ---------- | --- |
|     | if a*200   | + b*300       | == amount: |     |        |            |                 |              |            |     |
|     |            |               |            |     |        | dp[j]      | = min(dp[j],    |              | dp[j -     |     |
|     | price      | = a*380       | + b*550    |     |        |            |                 |              |            |     |
|     |            |               |            |     |        | coins[i]]  |                 | + prices[i]) |            |     |
|     | if price   | < best_price: |            |     |        | (cid:44)→  |                 |              |            |     |
|     |            |               |            |     | return | dp[amount] |                 |              |            |     |
|     | best_price |               | = price    |     |        |            |                 |              |            |     |
return best_price
Figure5: ComparisonofcodegeneratedbyMadaanetal.(2023)(left)andtheoutputafterapplying
SELF-REFINE(right). Theinitialcodebythebaseline,whichisnearlyidenticaltotheslowerinput
program,failstoimprovetheefficiencyandmerelyaltersthelogicforreadinginput. SELF-REFINE
firstgeneratesfeedbackthatdiagnoses thatThiscodeisslowbecauseitisusingsixnestedloopsto
iteratethroughallpossiblecombinationsofcoinstopaytheamount,andsuggeststhatamoreefficient
approachwouldbe.... SELF-REFINEthenusesthisfeedbacktogeneratetherevisedcode(right),
reducingthetimecomplexitytoO(amount∗coins). ThefullexampleisprovidedinAppendixH
Canwejustgeneratemultipleoutputsinsteadofrefining? DoesSELF-REFINEimprovebecause
oftheiterativerefinement,orjustbecauseitgeneratesmoreoutputs? WecompareSELF-REFINEwith
ChatGPT,whenChatGPTgeneratesk =4samples(butwithoutfeedbackandrefinement). Then,
wecomparetheperformanceofSELF-REFINEagainstthesekinitialoutputsina1vs. kevaluation.
Inotherwords,weassesswhetherSELF-REFINEcanoutperformallkinitialoutputs. Theresults
ofthisexperimentareillustratedinFigure6(AppendixH).Despitetheincreaseddifficultyofthe
1vs. ksetting,theoutputsofSELF-REFINEarestillpreferredbyhumansoverallkinitialoutputs.
Thisshowstheimportanceofrefinementaccordingtofeedbackoverthealternativeofjustgenerating
multipleinitialoutputs.
DoesSELF-REFINEworkwithweakermodels? TheexperimentsinSection3.3wereperformed
withsomeofthestrongestavailablemodels;doesSELF-REFINEworkwithsmallerorweakermodels
aswell? Toinvestigatethis,weinstantiatedSELF-REFINEwithVicuna-13B(Chiangetal.,2023),a
7

lesspowerfulbasemodel. WhileVicuna-13Biscapableofgeneratinginitialoutputs,itstruggles
significantly with the refinement process. Specifically, Vicuna-13B was not able to consistently
generate the feedback in the required format. Furthermore, even when provided with Oracle or
hard-coded feedback, it often failed to adhere to the prompts for refinement. Instead of refining
its output, Vicuna-13B either repeated the same output or generated a hallucinated conversation,
rendering the outputs less effective. We thus hypothesize that since Vicuna-13B was trained on
conversations,itdoesnotgeneralizeaswellasinstruction-basedmodelstotest-timefew-shottasks.
ExampleoutputandanalysisisprovidedinAppendixG.
QualitativeAnalysis WeconductaqualitativeanalysisofthefeedbackgeneratedbySELF-REFINE
anditssubsequentrefinements. Wemanuallyanalyze70samplesintotal(35successcasesand35
failurecases)forCodeOptimization(Madaanetal.,2023)andMathReasoning(Cobbeetal.,2021).
ForbothMathReasoningandCodeOptimization,wefoundthatthefeedbackwaspredominantly
actionable,withthemajorityidentifyingproblematicaspectsoftheoriginalgenerationandsuggesting
waystorectifythem.
WhenSELF-REFINEfailedtoimprovetheoriginalgeneration,themajorityofissuesweredueto
erroneousfeedbackratherthanfaultyrefinements.Specifically,33%ofunsuccessfulcasesweredueto
feedbackinaccuratelypinpointingtheerror’slocation,while61%werearesultoffeedbacksuggesting
an inappropriate fix. Only 6% of failures were due to the refiner incorrectly implementing good
feedback. TheseobservationshighlightthevitalroleofaccuratefeedbackplaysinSELF-REFINE.
Insuccessfulcases,therefinerwasguidedbyaccurateandusefulfeedbacktomakeprecisefixestothe
originalgenerationin61%ofthecases. Interestingly,therefinerwascapableofrectifyingissueseven
whenthefeedbackwaspartiallyincorrect,whichwasthesituationin33%ofsuccessfulcases. This
suggestsresiliencetosub-optimalfeedback. Futureresearchcouldfocusonexaminingtherefiner’s
robustnesstovarioustypesoffeedbackerrorsandexploringwaystoenhancethisresilience.InFigure
5,weillustratehowSELF-REFINEsignificantlyimprovesprogramefficiencybytransformingabrute
forceapproachintoadynamicprogrammingsolution,asaresultofinsightfulfeedback. Additional
analysisonotherdatasetssuchasDialogueResponseGenerationisprovidedinAppendixH.
GoingBeyondBenchmarks Whileourevaluationfocusesonbenchmarktasks,SELF-REFINEis
designedwithbroaderapplicabilityinmind. Weexplorethisinareal-worldusecaseofwebsitegen-
eration,wheretheuserprovidesahigh-levelgoalandSELF-REFINEassistsiniterativelydeveloping
thewebsite. Startingfromarudimentaryinitialdesign,SELF-REFINErefinesHTML,CSS,andJS
toevolvethewebsiteintermsofbothusabilityandaesthetics. Thisdemonstratesthepotentialof
SELF-REFINEinreal-world,complex,andcreativetasks. SeeAppendixIforexamplesandfurther
discussion,includingbroader,societalimpactofourwork.
5 Relatedwork
Leveraginghuman-andmachine-generatednaturallanguage(NL)feedbackforrefiningoutputshas
beeneffectiveforavarietyoftasks,includingsummarization(Scheureretal.,2022),scriptgeneration
(Tandonetal.,2021),programsynthesis(Leetal.,2022a;YasunagaandLiang,2020),andother
tasks(Baietal.,2022a;Schicketal.,2022b;Saundersetal.,2022a;Baietal.,2022b;Wellecketal.,
2022). Refinementmethodsdifferinthesourceandformatoffeedback,andthewaythatarefineris
obtained. Table3summarizessomerelatedapproaches;seeAppendixBforanadditionaldiscussion.
Source of feedback. Humans have been an effective source of feedback (Tandon et al., 2021;
Elgoharyetal.,2021;Tandonetal.,2022;Baietal.,2022a). Sincehumanfeedbackiscostly,several
approachesuseascalarrewardfunctionasasurrogateof(oralternativeto)humanfeedback(e.g.,
(Baietal.,2022a;Liuetal.,2022;Luetal.,2022;Leetal.,2022a;Wellecketal.,2022)). Alternative
sourcessuchascompilers(YasunagaandLiang,2020)orWikipediaedits(Schicketal.,2022b)can
providedomain-specificfeedback. Recently,LLMshavebeenusedtogeneratefeedbackforgeneral
domains(Fuetal.,2023;Pengetal.,2023;Yangetal.,2022),However,oursistheonlymethodthat
generatesfeedbackusinganLLMonitsownoutput,forthepurposeofrefiningwiththesameLLM.
Representationoffeedback. Theformoffeedbackcanbegenerallydividedintonaturallanguage
(NL)andnon-NLfeedback.Non-NLfeedbackcancomeinhuman-providedexamplepairs(Dasgupta
8

Supervision- Supervision- Multi-aspect Iterative
freerefiner freefeedback feedback
Learned refiners: PEER (Schick et al., or or
2022b),Self-critique(Saundersetal.,2022b),
CodeRL(Leetal.,2022b),Self-correction
(Wellecketal.,2022).
Promptedrefiners:Augmenter(Pengetal., or
2023), Re3 (Yang et al., 2022), Reflexion
(Shinnetal.,2023).
SELF-REFINE(thiswork)
Table3: AcomparisonofSELF-REFINEtocloselyrelatedpriorrefinementapproaches.
etal.,2019)orscalarrewards(Liuetal.,2022;Leetal.,2022b). Inthiswork,weuseNLfeedback,
sincethisallowsthemodeltoeasilyprovideself-feedbackusingthesameLMthatgeneratedthe
output,whileleveragingexistingpretrainedLLMssuchasGPT-4.
Typesofrefiners. Pairsoffeedbackandrefinementhavebeenusedtolearnsupervisedrefiners
(Schick et al., 2022b; Du et al., 2022; Yasunaga and Liang, 2020; Madaan et al., 2021). Since
gatheringsuperviseddataiscostly,somemethodslearnrefinersusingmodelgenerations(Welleck
etal.,2022;Pengetal.,2023). However,therefinersaretrainedforeachnewdomain. Finally,(Yang
etal.,2022)usepromptedfeedbackandrefinementspecificallytailoredforstorygeneration. Inthis
work,weavoidtrainingaseparaterefiner,andshowthatthesamemodelcanbeusedasboththe
refinerandthesourceoffeedbackacrossmultipledomains.
Non-refinementreinforcementlearning(RL)approaches. Ratherthanhavingexplicitrefinement,
an alternative way to incorporate feedback is by optimizing a scalar reward function, e.g. with
reinforcement learning (e.g., Stiennon et al. (2020); Lu et al. (2022); Le et al. (2022a)). These
methodsdifferfromSELF-REFINEinthatthemodeldoesnotaccessfeedbackonanintermediate
generation.Second,theseRLmethodsrequireupdatingthemodel’sparameters,unlikeSELF-REFINE.
6 LimitationsandDiscussion
Themainlimitationofourapproachisthatthebasemodelsneedtohavesufficientfew-shotmodeling
orinstruction-followingabilities,inordertolearntoprovidefeedbackandtorefineinanin-context
fashion,withouthavingtotrainsupervisedmodelsandrelyonsuperviseddata.
Further,theexperimentsinthisworkwereperformedwithlanguagemodelsthatarenotopen-sourced,
namelyGPT-3.5,ChatGPT,GPT-4,andCODEX. Existingliterature(Ouyangetal.,2022)doesnot
fullydescribethedetailsofthesemodels,suchasthepretrainingcorpus,modelsizes,andmodel
biases. Further,thesemodelsarenotfreetouse,andusingthemforresearchrequiressomefunding.
Nonetheless,wereleaseourcodeandmodeloutputstoensurethereproducibilityofourwork.
AnotherlimitationofourworkisthatweexclusivelyexperimentwithdatasetsinEnglish. Inother
languages,thecurrentmodelsmaynotprovidethesamebenefits.
Finally,thereisapossibilityforbadactorstousepromptingtechniquestosteeramodeltogenerate
moretoxicorharmfultext. Ourapproachdoesnotexplicitlyguardagainstthis.
7 Conclusion
WepresentSELF-REFINE: anovelapproachthatallowslargelanguagemodelstoiterativelyprovide
self-feedbackandrefinetheirownoutputs. SELF-REFINEoperateswithinasingleLLM,requiring
neitheradditionaltrainingdatanorreinforcementlearning. Wedemonstratethesimplicityandeaseof
useofSELF-REFINEacrossawidevarietyoftasks. ByshowcasingthepotentialofSELF-REFINEin
diversetasks,ourresearchcontributestotheongoingexplorationanddevelopmentoflargelanguage
models,withtheaimofreducingthecostofhumancreativeprocessesinreal-worldsettings. We
9

hopethatouriterativeapproachwillhelpdrivefurtherresearchinthisarea. Tothisend,wemakeall
ourcode,dataandpromptsanonymouslyavailableathttps://selfrefine.info/.
References
TeresaM.Amabile.1983. ATheoreticalFramework. InTheSocialPsychologyofCreativity,pages
65–96.SpringerNewYork,NewYork,NY.
Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn
Drain,StanislavFort,DeepGanguli,TomHenighan,etal.2022a. Trainingahelpfulandharmless
assistantwithreinforcementlearningfromhumanfeedback. ArXiv:2204.05862.
Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones,
AnnaChen,AnnaGoldie,AzaliaMirhoseini,CameronMcKinnon,etal.2022b. Constitutionalai:
Harmlessnessfromaifeedback. arXivpreprintarXiv:2212.08073.
EmeryDBerger,SamStern,andJuanAltmayerPizzorno.2022. TriangulatingPythonPerformance
IssueswithSCALENE. ArXivpreprint,abs/2212.07597.
LawrenceDBrown,TTonyCai,andAnirbanDasGupta.2001. Intervalestimationforabinomial
proportion. Statisticalscience,16(2):101–133.
TomBrown,BenjaminMann,NickRyder,MelanieSubbiah,JaredDKaplan,PrafullaDhariwal,
Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel
Herbert-Voss,GretchenKrueger,TomHenighan,RewonChild,AdityaRamesh,DanielZiegler,
JeffreyWu,ClemensWinter,ChrisHesse,MarkChen,EricSigler,MateuszLitwin,ScottGray,
BenjaminChess,JackClark,ChristopherBerner,SamMcCandlish,AlecRadford,IlyaSutskever,
and Dario Amodei. 2020. Language models are few-shot learners. In Advances in Neural
InformationProcessingSystems,volume33,pages1877–1901,Online.CurranAssociates,Inc.
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared
Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri,
GretchenKrueger,MichaelPetrov,HeidyKhlaaf,GirishSastry,PamelaMishkin,BrookeChan,
ScottGray,NickRyder,MikhailPavlov,AletheaPower,LukaszKaiser,MohammadBavarian,
ClemensWinter,PhilippeTillet,FelipePetroskiSuch,DaveCummings,MatthiasPlappert,Fotios
Chantzis,ElizabethBarnes,ArielHerbert-Voss,WilliamHebgenGuss,AlexNichol,AlexPaino,
Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders,
Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa,
Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder,
BobMcGrew, DarioAmodei, SamMcCandlish, IlyaSutskever, andWojciechZaremba.2021.
EvaluatingLargeLanguageModelsTrainedonCode. arXivpreprintarXiv:2107.03374.
Wei-Lin Chiang, Zhuohan Li, Zi Lin, Ying Sheng, Zhanghao Wu, Hao Zhang, Lianmin Zheng,
SiyuanZhuang,YonghaoZhuang,JosephEGonzalez,etal.2023. Vicuna:Anopen-sourcechatbot
impressinggpt-4with90%*chatgptquality.
Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser,
MatthiasPlappert,JerryTworek,JacobHilton,ReiichiroNakano,etal.2021. Trainingverifiersto
solvemathwordproblems. arXivpreprintarXiv:2110.14168.
SanjoyDasgupta,DanielHsu,StefanosPoulis,andXiaojinZhu.2019. Teachingablack-boxlearner.
InProceedingsofthe36thInternationalConferenceonMachineLearning,ICML2019,9-15June
2019,LongBeach,California,USA,volume97ofProceedingsofMachineLearningResearch,
pages1547–1555.PMLR.
WanyuDu,ZaeMyungKim,VipulRaheja,DhruvKumar,andDongyeopKang.2022. Read,revise,
repeat:Asystemdemonstrationforhuman-in-the-loopiterativetextrevision. InProceedingsofthe
FirstWorkshoponIntelligentandInteractiveWritingAssistants(In2Writing2022),pages96–108,
Dublin,Ireland.AssociationforComputationalLinguistics.
10

AhmedElgohary,ChristopherMeek,MatthewRichardson,AdamFourney,GonzaloRamos,and
AhmedHassanAwadallah.2021. NL-EDIT:Correctingsemanticparseerrorsthroughnatural
languageinteraction. InProceedingsofthe2021ConferenceoftheNorthAmericanChapterofthe
AssociationforComputationalLinguistics: HumanLanguageTechnologies,pages5599–5610,
Online.AssociationforComputationalLinguistics.
LindaFlowerandJohnRHayes.1981. Acognitiveprocesstheoryofwriting. Collegecomposition
andcommunication,32(4):365–387.
JinlanFu,See-KiongNg,ZhengbaoJiang,andPengfeiLiu.2023. Gptscore: Evaluateasyoudesire.
arXivpreprintarXiv:2302.04166.
LuyuGao,AmanMadaan,ShuyanZhou,UriAlon,PengfeiLiu,YimingYang,JamieCallan,and
GrahamNeubig.2022. Pal: Program-aidedlanguagemodels. arXivpreprintarXiv:2211.10435.
XinyangGeng,ArnavGudibande,HaoLiu,EricWallace,PieterAbbeel,SergeyLevine,andDawn
Song.2023. Koala: Adialoguemodelforacademicresearch. Blogpost.
Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven C. H. Hoi. 2022a.
CodeRL:MasteringCodeGenerationthroughPretrainedModelsandDeepReinforcementLearn-
ing.
Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven C. H. Hoi. 2022b.
Coderl: Masteringcodegenerationthroughpretrainedmodelsanddeepreinforcementlearning.
ArXiv,abs/2207.01780.
JuncenLi,RobinJia,HeHe,andPercyLiang.2018. Delete,retrieve,generate: asimpleapproachto
sentimentandstyletransfer.InProceedingsofthe2018ConferenceoftheNorthAmericanChapter
oftheAssociationforComputationalLinguistics: HumanLanguageTechnologies,Volume1(Long
Papers),pages1865–1874,NewOrleans,Louisiana.AssociationforComputationalLinguistics.
Bill Yuchen Lin, Wangchunshu Zhou, Ming Shen, Pei Zhou, Chandra Bhagavatula, Yejin Choi,
and Xiang Ren. 2020. CommonGen: A constrained text generation challenge for generative
commonsensereasoning. InFindingsoftheAssociationforComputationalLinguistics: EMNLP
2020,pages1823–1840,Online.AssociationforComputationalLinguistics.
JiachengLiu,SkylerHallinan,XimingLu,PengfeiHe,SeanWelleck,HannanehHajishirzi,andYejin
Choi.2022. Rainier: Reinforcedknowledgeintrospectorforcommonsensequestionanswering. In
ConferenceonEmpiricalMethodsinNaturalLanguageProcessing.
Ximing Lu, Sean Welleck, Liwei Jiang, Jack Hessel, Lianhui Qin, Peter West, Prithviraj Am-
manabrolu,andYejinChoi.2022. Quark: Controllabletextgenerationwithreinforcedunlearning.
ArXiv,abs/2205.13636.
AmanMadaan,AlexanderShypula,UriAlon,MiladHashemi,ParthasarathyRanganathan,Yiming
Yang,GrahamNeubig,andAmirYazdanbakhsh.2023. Learningperformance-improvingcode
edits. arXivpreprintarXiv:2302.07867.
Aman Madaan, Niket Tandon, Dheeraj Rajagopal, Peter Clark, Yiming Yang, and Eduard Hovy.
2021. Thinkaboutit! improvingdefeasiblereasoningbyfirstmodelingthequestionscenario.
InProceedingsofthe2021ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,
pages6291–6310,OnlineandPuntaCana,DominicanRepublic.AssociationforComputational
Linguistics.
Shikib Mehri and Maxine Eskenazi. 2020. Unsupervised evaluation of interactive dialog with
DialoGPT. InProceedingsofthe21thAnnualMeetingoftheSpecialInterestGrouponDiscourse
andDialogue,pages225–235,1stvirtualmeeting.AssociationforComputationalLinguistics.
ErikNijkamp,BoPang,HiroakiHayashi,LifuTu,HuanWang,YingboZhou,SilvioSavarese,and
CaimingXiong.2022. Codegen: Anopenlargelanguagemodelforcodewithmulti-turnprogram
synthesis. ArXivpreprint,abs/2203.13474.
OpenAI. Model index for researchers. https://platform.openai.com/docs/
model-index-for-researchers. Accessed: May14,2023.
11

OpenAI.2022. Modelindexforresearchers. Blogpost.
OpenAI.2023. Gpt-4technicalreport.
LongOuyang,JeffWu,XuJiang,DiogoAlmeida,CarrollL.Wainwright,PamelaMishkin,Chong
Zhang,SandhiniAgarwal,KatarinaSlama,AlexRay,JohnSchulman,JacobHilton,FraserKelton,
LukeE.Miller, MaddieSimens, AmandaAskell, PeterWelinder, PaulFrancisChristiano, Jan
Leike, and Ryan J. Lowe. 2022. Training language models to follow instructions with human
feedback. ArXiv:2203.02155.
BaolinPeng,MichelGalley,PengchengHe,HaoCheng,YujiaXie,YuHu,QiuyuanHuang,Lars
Liden, Zhou Yu, Weizhu Chen, and Jianfeng Gao. 2023. Check Your Facts and Try Again:
ImprovingLargeLanguageModelswithExternalKnowledgeandAutomatedFeedback.
Shrimai Prabhumoye, Yulia Tsvetkov, Ruslan Salakhutdinov, and Alan W Black. 2018. Style
transferthroughback-translation. InProceedingsofthe56thAnnualMeetingoftheAssociation
forComputationalLinguistics(Volume1: LongPapers),pages866–876,Melbourne,Australia.
AssociationforComputationalLinguistics.
OfirPress,MuruZhang,SewonMin,LudwigSchmidt,NoahASmith,andMikeLewis.2022.Measur-
ingandnarrowingthecompositionalitygapinlanguagemodels. arXivpreprintarXiv:2210.03350.
RuchirPuri,DavidKung,GeertJanssen,WeiZhang,GiacomoDomeniconi,VladmirZolotov,Julian
Dolby,JieChen,MihirChoudhury,LindseyDecker,VeronikaThost,LucaBuratti,SaurabhPujar,
ShyamRamji,UlrichFinkler,SusanMalaika,andFrederickReiss.2021. Codenet: Alarge-scale
aiforcodedatasetforlearningadiversityofcodingtasks. arXivpreprintarXiv:2105.12655.
Machel Reid and Graham Neubig. 2022. Learning to model editing processes. arXiv preprint
arXiv:2205.12374.
WilliamSaunders, CatherineYeh, JeffWu, Steven Bills, LongOuyang, JonathanWard, andJan
Leike.2022a. Self-critiquingmodelsforassistinghumanevaluators.
WilliamSaunders, CatherineYeh, JeffWu, Steven Bills, LongOuyang, JonathanWard, andJan
Leike.2022b. Self-critiquingmodelsforassistinghumanevaluators. ArXiv:2206.05802.
JérémyScheurer,JonAnderCampos,JunShernChan,AngelicaChen,KyunghyunCho,andEthan
Perez.2022. Traininglanguagemodelswithnaturallanguagefeedback. ArXiv:2204.14146.
Timo Schick, Jane Dwivedi-Yu, Zhengbao Jiang, Fabio Petroni, Patrick Lewis, Gautier Izacard,
QingfeiYou, ChristoforosNalmpantis, EdouardGrave, andSebastianRiedel.2022a. Peer: A
collaborativelanguagemodel.
Timo Schick, Jane Dwivedi-Yu, Zhengbao Jiang, Fabio Petroni, Patrick Lewis, Gautier Izacard,
QingfeiYou, ChristoforosNalmpantis, EdouardGrave, andSebastianRiedel.2022b. Peer: A
collaborativelanguagemodel. ArXiv,abs/2208.11663.
Noah Shinn, Beck Labash, and Ashwin Gopinath. 2023. Reflexion: an autonomous agent with
dynamicmemoryandself-reflection.
HerbertA.Simon.1962. Thearchitectureofcomplexity. ProceedingsoftheAmericanPhilosophical
Society,106(6):467–482.
NisanStiennon,LongOuyang,JeffreyWu,DanielZiegler,RyanLowe,ChelseaVoss,AlecRadford,
Dario Amodei, and Paul F Christiano. 2020. Learning to summarize with human feedback.
InAdvancesinNeuralInformationProcessingSystems,volume33,pages3008–3021.Curran
Associates,Inc.
ZhiqingSun,YikangShen,QinhongZhou,HongxinZhang,ZhenfangChen,DavidCox,Yiming
Yang,andChuangGan.2023. Principle-drivenself-alignmentoflanguagemodelsfromscratch
withminimalhumansupervision. arXivpreprintarXiv:2305.03047.
NiketTandon,AmanMadaan,PeterClark,KeisukeSakaguchi,andYimingYang.2021.Interscript:A
datasetforinteractivelearningofscriptsthrougherrorfeedback. arXivpreprintarXiv:2112.07867.
12

NiketTandon,AmanMadaan,PeterClark,andYimingYang.2022. Learningtorepair: Repairing
modeloutputerrorsafterdeploymentusingadynamicmemoryoffeedback. InFindingsofthe
AssociationforComputationalLinguistics: NAACL2022,pages339–352.
HugoTouvron,ThibautLavril,GautierIzacard,XavierMartinet,Marie-AnneLachaux,Timothée
Lacroix,BaptisteRozière,NamanGoyal,EricHambro,FaisalAzhar,etal.2023. Llama: Open
andefficientfoundationlanguagemodels. arXivpreprintarXiv:2302.13971.
JasonWei,XuezhiWang,DaleSchuurmans,MaartenBosma,EdChi,QuocLe,andDennyZhou.
2022. ChainofThoughtPromptingElicitsReasoninginLargeLanguageModels. arXivpreprint
arXiv:2201.11903.
SeanWelleck,XimingLu,PeterWest,FaezeBrahman,TianxiaoShen,DanielKhashabi,andYejin
Choi.2022. Generatingsequencesbylearningtoself-correct. arXivpreprintarXiv:2211.00053.
KevinYang,NanyunPeng,YuandongTian,andDanKlein.2022.Re3:Generatinglongerstorieswith
recursiverepromptingandrevision. InConferenceonEmpiricalMethodsinNaturalLanguage
Processing.
Michihiro Yasunaga and Percy Liang. 2020. Graph-based, self-supervised program repair from
diagnosticfeedback. 37thInt.Conf.Mach.Learn.ICML2020,PartF168147-14:10730–10739.
XiangZhang,JunboZhao,andYannLeCun.2015. Character-levelconvolutionalnetworksfortext
classification. Advancesinneuralinformationprocessingsystems,28.
13

A EvaluationTasks
Table4liststhetasksinourevaluation,andexamplesfromeachtask.
TaskandDescription SampleoneiterationofFEEDBACK-REFINE
SentimentReversal x: Thefoodwasfantastic...”
Rewritereviewstoreversesentiment. y : Thefoodwasdisappointing...”
t
Dataset: (Zhangetal.,2015)1000reviewpas- fb: Increasenegativesentiment
sages y : Thefoodwasutterlyterrible...”
t+1
DialogueResponseGeneration x: What’sthebestwaytocookpasta?”
Producerichconversationalresponses. y : Thebestwaytocookpastaisto...”
t
Dataset:(MehriandEskenazi,2020)372conv. fb: Makeresponserelevant,engaging,safe
y : Boilwater,addsalt,andcookpasta...”
t+1
CodeOptimization x: Nestedloopformatrixproduct
EnhancePythoncodeefficiency y : NumPydotproductfunction
t
Dataset:(Madaanetal.,2023):1000programs fb: Improvetimecomplexity
y : UseNumPy’soptimizedmatmulfunction
t+1
CodeReadabilityImprovement x: Unclearvariablenames,nocomments
RefactorPythoncodeforreadability. y : Descriptivenames,comments
t
Dataset: (Purietal.,2021)300programs∗ fb: Enhancevariablenaming;addcomments
y : Clearvariables,meaningfulcomments
t+1
MathReasoning x: Oliviahas$23,buys5bagelsat$3each”
Solvemathreasoningproblems. y : SolutioninPython
t
Dataset: (Cobbeetal.,2021)1319questions fb: Showstep-by-stepsolution
y : Solutionwithdetailedexplanation
t+1
AcronymGeneration x: RadioDetectingandRanging”
Generateacronymsforagiventitle y : RDR
t
Dataset: (AppendixQ)250acronyms fb: becontextrelevant;easypronunciation
y : RADAR”
t+1
ConstrainedGeneration x: beach,vacation,relaxation
Generatesentenceswithgivenkeywords. y : Duringourbeachvacation...
t
Dataset: (Linetal.,2020)200samples fb: Includekeywords;maintaincoherence
y :..beachvacationwasfilledwithrelaxation
t+1
Table4: AnoverviewofthetaskswhichweevaluateSELF-REFINEon,alongwiththeirassociated
datasetsandsizes. Foreverytask,wedemonstrateasingleiterationofrefinementofinputx,the
previously generated output y , the feedback generated fb , and the refinement y . Few-shot
t t t+1
promptsusedforFEEDBACKandREFINEareprovidedinAppendixS.
14

B BroaderRelatedWork
Comparedtoaconcurrentwork,Reflexion(Shinnetal.,2023),ourapproachinvolvescorrection
usingfeedback,whereastheirsetupinvolvesfindingthenextbestsolutioninplanningusingReAct.
WhileReActandReflexionprovideafree-formreflectiononwhetherastepwasexecutedcorrectly
andpotentialimprovements,ourapproachismoregranularandstructured,withmulti-dimensional
feedbackandscores.Thisdistinctionallowsourmethodtooffermorepreciseandactionablefeedback,
makingitsuitableforawiderrangeofnaturallanguagegenerationtasks,includingthosethatmay
notnecessarilyinvolvestep-by-stepplanningsuchasopen-endeddialoguegeneration.
ComparisonwithWellecketal.(2022) TheclosestworktooursmaybeSelf-Correction(Welleck
etal.,2022);however,Self-CorrectionhasseveraldisadvantagescomparedtoSELF-REFINE:
1. Self-Correctiondoesnottraintheirmodeltogenerateexplicitfeedback;instead,Welleck
etal.(2022)trainedtheirmodelstorefineonly. AsweshowinSection4andTable2,having
themodelgenerateexplicitfeedbackresultsinsignificantlybetterrefinedoutputs.
2. Self-Correctiontrainsaseparaterefiner(or“corrector”)foreachtask. Incontrast,SELF-
REFINE uses instructions and few-shot prompting, and thus does not require training a
separaterefinerforeachtask.
3. Empirically, we evaluated SELF-REFINE using the same base model of GPT-3 as Self-
Correction,andwiththesamesettingsontheGSM8Kbenchmark. Self-Correctionachieved
45.9%accuracywhileSELF-REFINE(thiswork)achieved55.7%(↑9.8).
Comparisonwithnon-refinementreinforcementlearning(RL)approaches.
Ratherthanhaving
anexplicitrefinementmodule,analternativewaytoincorporatefeedbackisbyoptimizingascalar
rewardfunction,e.g. withreinforcementlearning(e.g.,Stiennonetal.(2020);Luetal.(2022);Le
etal.(2022a)). Thesemethodsdifferfrom SELF-REFINE (andmoregenerally, refinement-based
approaches)inthatthemodelcannotaccessfeedbackonanintermediategeneration. Second,these
reinforcementlearningmethodsrequireupdatingthemodel’sparameters,unlikeSELF-REFINE.
SeeTable5foranadditionaldetailedcomparisonofrelatedwork.
Method PrimaryNovelty zero/fewshotimprovement multiaspectcritics NLfeedbackwither- iterativeframework
rorlocalization
| RLHF(Stiennonetal.,2020) | optimizeforhumanpreference | trainedonfeedback | single(human)    | (notselfgen.) |
| ------------------------ | -------------------------- | ----------------- | ---------------- | ------------- |
| RainierRL(Liuetal.,2022) | RLtogenerateknowledge      | trainedonendtask  | single(accuracy) | (knowl.only)  |
QUARKRL(Luetal.,2022) quantizationtoeditgenerations trainedonendtask single(scalarscore) (densesignal) (traintimeiter.)
| CodeRL(Leetal.,2022a) | actorcriticRLforcodeim- | trainedonendtask | single(unittests) | (densesignal) |
| --------------------- | ----------------------- | ---------------- | ----------------- | ------------- |
provement
| DrRepair(YasunagaandLiang,2020) | Compiler feedback | to itera- trainedsemisup. | single(compilermsg) | (notselfgen.) |
| ------------------------------- | ----------------- | ------------------------- | ------------------- | ------------- |
tivelyrepair
| PEER(Schicketal.,2022b)           | doc.edittrainedonwikiedits | trainedonedits   | single(accuracy) | (notselfgen.) |
| --------------------------------- | -------------------------- | ---------------- | ---------------- | ------------- |
| Selfcritique(Saundersetal.,2022a) | fewshotcritiquegeneration  | feedbacktraining | single(human)    | (selfgen.)    |
Self-correct(Wellecketal.,2022) noveltrainingofacorrector trainedonendtask single(taskspecific) (limitedsetting) (limitedsetting)
| Const.AI(Baietal.,2022b) | trainRL4Fonautomat(cri- | critiquetraining | (fixedset) |     |
| ------------------------ | ----------------------- | ---------------- | ---------- | --- |
tique,revision)pair
| Self-ask(Pressetal.,2022) | askfollowupqueswhenin- | fewshot | none | (none) |
| ------------------------- | ---------------------- | ------- | ---- | ------ |
terimanscorrect;finalwrong
| GPT3score(Fuetal.,2023) | GPT can score | generations fewshot | single(singleutilityfn) | (none) |
| ----------------------- | ------------- | ------------------- | ----------------------- | ------ |
withinstruction
| Augmenter(Pengetal.,2023) | factualityfeedbackfromexter- | fewshot | single(factuality) | (selfgen.) |
| ------------------------- | ---------------------------- | ------- | ------------------ | ---------- |
nalKBs
| Re3(Yangetal.,2022) | ∼ours: but | one domain, fewshot | (trainedcritics) | (notselfgen.) |
| ------------------- | ---------- | ------------------- | ---------------- | ------------- |
trainedcritics
| SELF-REFINE | fewshotiterativemultiaspect | fewshot | multiple(fewshotcritics) | (selfgen.) |
| ----------- | --------------------------- | ------- | ------------------------ | ---------- |
NLfb
Table5: Summaryofrelatedapproaches. Reinforcementlearningapproachesareshownin purple
,trainedcorrectorapproachesareshownin orange,andfew-shotcorrectorapproachesareshownin
green.
15

C HumanEvaluation
TheA/Bevaluationinourstudywasconductedbytheauthors,whereahumanjudgewaspresented
with an input, task instruction, and two candidate outputs generated by the baseline method and
SELF-REFINE. Thesetupwasblind, i.e., thejudgesdidnotknowwhichoutputsweregenerated
by which method. The judge was then asked to select the output that is better aligned with the
taskinstruction. FortasksthatinvolveA/Bevaluation, wecalculatetherelativeimprovementas
thepercentageincreaseinpreferencerate. Thepreferenceraterepresentstheproportionoftimes
annotatorsselectedtheoutputproducedbySELF-REFINEovertheoutputfromthebaselinemethod.
Table6showstheresults.
| Task               | SELF-REFINE(%) | Direct(%) | Either(%) |
| ------------------ | -------------- | --------- | --------- |
| SentimentTransfer  | 75.00          | 21.43     | 3.57      |
| AcronymGeneration  | 44.59          | 12.16     | 43.24     |
| ResponseGeneration | 47.58          | 19.66     | 32.76     |
Table6: RelativeimprovementofSELF-REFINEinA/Bevaluationsacrossdifferenttasks. Thevalues
representnormalizedpreferences,whichcorrespondtotheproportionoftimestheoutputgenerated
bySELF-REFINEwasselectedasbetteralignedwiththetaskinstructionoverthebaselinemethod.
Theevaluationwasconductedfor150examplesforeachdataset. Thejudgeswerenotawareofthe
methodthatgeneratedeachsample.
16

D GPT-4Evaluation
InlightoftheimpressiveachievementsofGPT-4inassessingandprovidingreasoningforcomplex
tasks,weleverageitsabilitiesforevaluationinSELF-REFINE. Theapproachinvolvespresenting
taskstoGPT-4inastructuredmanner,promotingthemodel’sdeliberationonthetaskandgenerating
| arationaleforitsdecision. | ThismethodologyisdemonstratedinListings1to3: |     |     |     |
| ------------------------- | -------------------------------------------- | --- | --- | --- |
Listing1PromptforGPT-4evaluationofSentimentReversal.
| f"""Which | review is aligned | with | the sentiment | {target_sentiment}? |
| --------- | ----------------- | ---- | ------------- | ------------------- |
| Review A: | {review_a}        |      |               |                     |
| Review B: | {review_b}.       |      |               |                     |
Pick your answer from ['Review A', 'Review B', 'both', 'neither']. Generate a
short explanation for your choice first. Then, generate 'The more aligned
(cid:44)→
review is A' or 'The more aligned review is B' or 'The more aligned review is
(cid:44)→
| both' | or 'The more aligned |     | review is neither'. |     |
| ----- | -------------------- | --- | ------------------- | --- |
(cid:44)→
| Format: <explanation> | <answer> |     | STOP |     |
| --------------------- | -------- | --- | ---- | --- |
Listing2PromptforGPT-4evaluationofAcronymGeneration.
| f"""Title: | {title}     |     |     |     |
| ---------- | ----------- | --- | --- | --- |
| Acronym A: | {acronym_a} |     |     |     |
| Acronym B: | {acronym_b} |     |     |     |
Pick the better acronym for the given title. The acronyms should be compared based
| (cid:44)→ on the | following criteria: |               |         |     |
| ---------------- | ------------------- | ------------- | ------- | --- |
| * Ease of        | pronunciation.      |               |         |     |
| * Ease of        | spelling.           |               |         |     |
| * Relation       | to title.           |               |         |     |
| * Positive       | connotation.        |               |         |     |
| Generate your    | answer in           | the following | format: |     |
<Short explanation>. The better acronym is A OR The better acronym is B OR The
| acronyms | are equally | good OR | Neither acronym | is good. STOP. |
| -------- | ----------- | ------- | --------------- | -------------- |
(cid:44)→
Listing3PromptforGPT-4evaluationofDialogueResponseGeneration.
| f"""Which   | response is better | given | this context: | {context}? |
| ----------- | ------------------ | ----- | ------------- | ---------- |
| Response A: | {response_a}       |       |               |            |
| Response B: | {response_b}.      |       |               |            |
Pick your answer from ['Response A', 'Response B', 'both', 'neither']. Generate a
short explanation for your choice first. Then, generate 'The better response
(cid:44)→
is A' or 'The better response is B' or 'The better response is both' or 'The
(cid:44)→
| better | response is neither'. |     |     |     |
| ------ | --------------------- | --- | --- | --- |
(cid:44)→
| Format: <explanation> | <answer> |     | STOP |     |
| --------------------- | -------- | --- | ---- | --- |
E ModelKey
Weuseterminologyhere: https://platform.openai.com/docs/models/gpt-3-5
17

F Comparisonof SELF-REFINE withState-of-the-artofFew-ShotLearning
ModelsandFine-TunedBaselines
Inthissection,wepresentacomprehensivecomparisonoftheperformanceofSELF-REFINEwith
other few-shot models and fine-tuned baselines across a range of tasks, including mathematical
reasoningandprogrammingtasks. Tables8and7displaytheperformanceofthesemodelsonthe
PIEdatasetandGSMtasks,respectively. Ouranalysisdemonstratestheeffectivenessofdifferent
modelarchitecturesandtrainingtechniquesintacklingcomplexproblems.
| Method           | SolveRate  |      |
| ---------------- | ---------- | ---- |
| Cobbeetal.(2021) | OpenAI6B   | 20.0 |
| Weietal.(2022)   | CoTw/CODEX | 65.6 |
|                  | PaLw/CODEX | 72.0 |
|                  | PaLw/GPT-3 | 52.0 |
Gaoetal.(2022)
|     | PaLw/GPT-3.5        | 56.8 |
| --- | ------------------- | ---- |
|     | PaLw/ChatGPT        | 74.2 |
|     | PaLw/GPT-4          | 93.3 |
|     | Self-Correctw/GPT-3 | 45.9 |
Wellecketal.(2022)
|     | Self-Correct(fine-tuned) | 24.3 |
| --- | ------------------------ | ---- |
|     | SELF-REFINEw/GPT-3       | 55.7 |
|     | SELF-REFINEw/GPT-3.5     | 62.4 |
Thiswork
|     | SELF-REFINEw/ChatGPT | 75.1 |
| --- | -------------------- | ---- |
|     | SELF-REFINEw/GPT-4   | 94.5 |
Table7: Performancecomparisonofmodelsonmathreasoning(MathReasoning).
18

| Method          |                 | %OPT) |
| --------------- | --------------- | ----- |
| Purietal.(2021) | HumanReferences | 38.2  |
|                 | CODEX           | 13.1  |
|                 | GPT-3.5         | 14.8  |
OpenAIModels: OpenAI(2022,2023)
|                    | ChatGPT     | 22.2 |
| ------------------ | ----------- | ---- |
|                    | GPT-4       | 27.3 |
| Nijkampetal.(2022) | CODEGEN-16B | 1.1  |
1.4
SCALENE
| Bergeretal.(2022) | SCALENE(BEST@16) | 12.6 |
| ----------------- | ---------------- | ---- |
|                   | SCALENE(BEST@32) | 19.6 |
|                   | PIE-2B           | 4.4  |
|                   | PIE-2B(BEST@16)  | 21.1 |
|                   | PIE-2B(BEST@32)  | 26.3 |
|                   | PIE-16B          | 4.4  |
Madaanetal.(2023)
|          | PIE-16B(BEST@16)      | 22.4 |
| -------- | --------------------- | ---- |
|          | PIE-16B(BEST@32)      | 26.6 |
|          | PIE-Few-shot(BEST@16) | 35.2 |
|          | PIE-Few-shot(BEST@32) | 38.3 |
|          | SELF-REFINEw/GPT-3.5  | 23.0 |
| Thiswork | SELF-REFINEw/ChatGPT  | 26.7 |
|          | SELF-REFINEw/GPT-4    | 36.0 |
Table8: PerformancecomparisonofvariousmodelsonthePIEdatasetintermsofthepercentage
ofprogramsoptimized(%OPT). Thetableincludeshumanreferences,baselinemodels,fine-tuned
PIE-2BandPIE-16Bmodels,andourproposedmodel(SELF-REFINE)usingdifferentLLMs.Notably,
SELF-REFINEachievessuperiorperformancewhileusingonly4samplesatmost,significantlyfewer
thanthe16and32samplesemployedbyothermodels. Scalene, anoff-the-shelfoptimizer, uses
instructiontuningwithCodexandservesasacomparisonpoint.
19

G EvaluationofVicuna-13b
WealsoexperimentwithVicuna-13b(Chiangetal.,2023),aversionofLLaMA-13b(Touvronetal.,
2023)fine-tunedonconversationssourcedfromtheweb. Vicuna-13bwasabletoconsistentlyfollow
thetaskinitializationprompt. However,itstruggledtofollowthepromptsintendedforfeedback
andrefinement. Thisoftenledtooutputsthatresembledassistant-likeresponses,arepresentative
exampleofwhichcanbefoundinAppendixG.
It’simportanttonotethatweusedthesamepromptsforVicuna-13basthoseusedwithothermodels
inourstudy. However,thelimitedperformanceofVicuna-13bsuggeststhatthismodelmayrequire
moreextensiveprompt-engineeringforoptimalperformance.
Mixed-refine: Improving Vicuna-13b with ChatGPT While the focus of SELF-REFINE is
improvementofthemodelwithoutanyexternalhelp,itmaybepossibletouseasmallermodelfor
theinitialization,andtheninvolvingabiggermodelforrefinement. Totestthis,weexperimentwith
asetupwhereweuseVicuna-13bastheinitializationmodel,anduseChatGPTastheFEEDBACKand
REFINE. TheresultsonMathReasoningshowthepromiseofthisapproach: whileVicuna-13bwas
abletogetonly24.18%onMathReasoning,itwasabletoimproveto40.5%inthismixed-refinement
setting.
20

| Step 0     | INIT>     | The food | was  | amazing,      | I loved | it!!.       |     |     |     |
| ---------- | --------- | -------- | ---- | ------------- | ------- | ----------- | --- | --- | --- |
| Step 0     | TRANSFER> | The      | food | was terrible, | I       | hated it!!. |     |     |     |
| list index | out       | of range |      |               |         |             |     |     |     |
An error occurred: list index out of range. Traceback (most recent call last):
| IndexError: | list | index | out | of range. | Left | retries: | 2.  |     |     |
| ----------- | ---- | ----- | --- | --------- | ---- | -------- | --- | --- | --- |
Step 1 TRANSFER> The food at the Trop was awful. I wish I could've gotten my money
| back | for | the terrible |     | meals. |     |     |     |     |     |
| ---- | --- | ------------ | --- | ------ | --- | --- | --- | --- | --- |
(cid:44)→
Step 1 FB> The rewritten review does not become more "Very negative", because it
only contains a single instance of a positive sentiment about the food. Try
(cid:44)→
| again | to  | make it | Very | negative! |     |     |     |     |     |
| ----- | --- | ------- | ---- | --------- | --- | --- | --- | --- | --- |
(cid:44)→
Step 2 TRANSFER> ### Assistant: The Trop is a great choice for anyone looking for
| a budget-friendly |     |     | option | in Vegas. | The | rooms | and hallways |     | are clean and |
| ----------------- | --- | --- | ------ | --------- | --- | ----- | ------------ | --- | ------------- |
(cid:44)→
| comfortable, |     | and | the | food options | are | varied | and delicious. |     |     |
| ------------ | --- | --- | --- | ------------ | --- | ------ | -------------- | --- | --- |
(cid:44)→
Step 2 FB> The rewritten review does not change from "Positive", because it only
has positive language. The output is already Very positive. No further changes
(cid:44)→
are needed.
(cid:44)→
Step 0 INIT> The food was amazing, I loved it!!. [Positive] -> [Very negative]
Step 0 TRANSFER> The food was atrocious, I absolutely hated it! [('The review
| (cid:44)→ sounds | very | negative. |     | The sentiment | is  | Very negative', |     | 1.0)] |     |
| ---------------- | ---- | --------- | --- | ------------- | --- | --------------- | --- | ----- | --- |
Step 0 FB> The original review is already "Very negative" as it uses strongly
(cid:44)→ negative words like "atrocious" and "absolutely hated". These words express
(cid:44)→ extreme dissatisfaction and clearly convey a very negative sentiment about the
| (cid:44)→ food. | But | try again | to  | make it | even more | negative! |     |     |     |
| --------------- | --- | --------- | --- | ------- | --------- | --------- | --- | --- | --- |
Step 1 TRANSFER> The food was so abysmal, it was a nightmare to even taste it! I
(cid:44)→ couldn't stand it and regretted every single bite. [('The review sounds highly
| (cid:44)→ negative. |     | The sentiment |     | is Very | negative', | 1.0)] |     |     |     |
| ------------------- | --- | ------------- | --- | ------- | ---------- | ----- | --- | --- | --- |
Step 1 FB> The review provided is indeed very negative. It uses extremely negative
(cid:44)→ words and phrases like "abysmal", "nightmare", and "regretted every single
(cid:44)→ bite". These strongly negative expressions make the review very negative, but
| (cid:44)→ try | again | to make | it  | even more | negative! |     |     |     |     |
| ------------- | ----- | ------- | --- | --------- | --------- | --- | --- | --- | --- |
Step 2 TRANSFER> The food was absolutely revolting, I couldn't even stomach a
| (cid:44)→ single | bite! |     |     |     |     |     |     |     |     |
| ---------------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
Step 2 FB> This review is not "Very negative" because it contains positive words
and phrases like "amazing" and "loved it." To make it "Very negative", we need
(cid:44)→
to use extremely negative words, like "revolting", "couldn't stomach", or
(cid:44)→
| "horrible". |     | The | provided | "Very | negative" | sentiment |     | example | is a good |
| ----------- | --- | --- | -------- | ----- | --------- | --------- | --- | ------- | --------- |
(cid:44)→
illustration of a very negative review, as it uses strong negative language to
(cid:44)→
| describe |     | the food | experience. |     |     |     |     |     |     |
| -------- | --- | -------- | ----------- | --- | --- | --- | --- | --- | --- |
(cid:44)→
Vicuna-13boutputs(top)forsentimenttransfer,wherethegoalistomake‘Thefoodwasamazing,I
lovedit!!.’ negative. Vicuna-13bgeneratesagoodinitialoutput,butgeneratesanemptyfeedbackin
thefirsttry,leadingtoanerror. Inthenexttry,itgeneratesanunhelpfulfeedback. Thetransferred
| reviewcopiesfromtheprompt. |     |     |     | ComparewiththeoutputsfromGPT-4(bottom). |     |     |     |     |     |
| -------------------------- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- | --- |
21

| SELF-REFINE |     | 3377..22 |     |       | 3355..66 |       |     | 2277..22 | ChatGPT |     |
| ----------- | --- | -------- | --- | ----- | -------- | ----- | --- | -------- | ------- | --- |
| SELF-REFINE |     | 3333..33 |     |       | 5511..11 |       |     | 1155..55 | MULTI   |     |
|             | 0   | 10       | 20  | 30 40 | 50       | 60 70 | 80  | 90       | 100     |     |
PreferenceratesforSentimentReversal
| SELF-REFINE |     |            | 4433..22 |       |     | 4455..44   |     |     | 1111..44 ChatGPT |     |
| ----------- | --- | ---------- | -------- | ----- | --- | ---------- | --- | --- | ---------------- | --- |
| SELF-REFINE |     | 4400..0055 |          |       |     | 5533..8822 |     |     | 66..11 MULTI     |     |
|             | 0   | 10         | 20       | 30 40 | 50  | 60 70      | 80  | 90  | 100              |     |
PreferenceratesforAcronymGeneration
Figure6: Preferencefortheoutputsgeneratedbyourmethod(SELF-REFINE),themultiple-sample
baseline(MULTI),andties(ties).
|               |     |     |      | GPT-3.5      |     | ChatGPT         |     |      | GPT-4        |     |
| ------------- | --- | --- | ---- | ------------ | --- | --------------- | --- | ---- | ------------ | --- |
| Task          |     |     | Base |              |     | Base            |     | Base |              |     |
|               |     |     |      | +SELF-REFINE |     | +SELF-REFINE    |     |      | +SELF-REFINE |     |
| MathReasoning |     |     |      | 64.1 64.1(0) |     | 74.8 75.0(↑0.2) |     | 92.9 | 93.1(↑0.2)   |     |
MathReasoning(Oracle) 64.06 68.9(↑4.8) 74.8 76.2(↑1.4) 92.9 93.8(↑0.7)
Table9: SELF-REFINEresultsonMathReasoningusingGPT-3.5,ChatGPT,andGPT-4asbase
LLMwithOraclefeedback.
H AdditionalAnalysis
H.1 UsingOracleFeedback
WeexperimentedwithOracleFeedbackfollowingWellecketal.(2022).Thismethodusescorrectness
informationtoguidemodelrefinement,onlyprogressingtoREFINEstageifthecurrentansweris
incorrect. ThisadjustmentnotablyenhancedperformanceintheMathReasoningtask,withGPT-3
improvingby4.8%andGPT-4by0.7%Table9. Thisindicatesthepotentialofexternalsignalsto
optimizemodelperformanceinparticulartasks.
Iteration Acronym Pronunciation Pron. (5) Spell. (5) Rel. (5) Pos. Con. (5) Total(25)
| 1   | USTACCSF  |     | us-tacks-eff |     | 1   | 1   |     | 5   | 3   | 11  |
| --- | --------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
| 2   | TACC-SIM  |     | tacks-sim    |     | 4   | 4   |     | 5   | 3   | 17  |
| 3   | TACCSF    |     | tacks-eff    |     | 1   | 2   |     | 5   | 3   | 12  |
| 4   | TACC-SIMF |     | tack-simf    |     | 4   | 4   |     | 5   | 3   | 17  |
Table10: Acronymgenerationresultsacrossiterations,showcasinghowimprovementsincertainas-
pects(e.g.,pronunciationandspelling)canbeaccompaniedbylossesinothers,leadingtofluctuating
overallperformanceinmulti-aspectfeedbacktaskslikeAcronymGeneration.
Non-monotonicincreaseinoutputqualityforacronymgeneration Fortaskswithmulti-aspect
feedback like Acronym Generation, the output quality can fluctuate during the iterative process,
improvingononeaspectwhilelosingoutonanother(Table10). Toaddressthis,SELF-REFINE’s
feedbackgeneratesexplicitnumericalscorestocapturethedifferentaspectsofoutputquality. This
allowsforamorebalancedevaluationofoutputsandtheselectionofthemostappropriateone. The
algorithm selects the best output based on the maximum score across all iterations, as described
in Algorithm 1 (line 8). A similar selection is possible for other tasks like Math Reasoning and
SentimentReversal,whileweobservethatoutputqualityincreasesmonotonicallywithiterations.
22

| ErrorType | Occurrence | Feedback |     |     | Refinement |     |     |
| --------- | ---------- | -------- | --- | --- | ---------- | --- | --- |
Incorrectfeedback 25% Informative: Theresponse Response: That’s hilarious!
|     |     | providessomeencourage-    |     |     | Don’t worry,            | I’m       | sure you’ll |
| --- | --- | ------------------------- | --- | --- | ----------------------- | --------- | ----------- |
|     |     | mentandreassurance,and    |     |     | domuchbetterwhenyoutake |           |             |
|     |     | additionalinformation.3/3 |     |     | History next            | semester. | Are         |
youlookingforwardtoit?
Genericfeedback 30% Specific: The response is Response: It’sunderstandable,
|     |     | not specific | and does    | not    | I’m sure                  | you’ll            | do much bet- |
| --- | --- | ------------ | ----------- | ------ | ------------------------- | ----------------- | ------------ |
|     |     | provide      | any details | or ex- | terwhenyoutakeHistorynext |                   |              |
|     |     | amples.      | 1/3         |        | semester.                 | Maybeyoucanuse    |              |
|     |     |              |             |        | your knowledge            |                   | of Christo-  |
|     |     |              |             |        | pher Columbus             |                   | to ace your  |
|     |     |              |             |        | nexttest!                 | Areyoulookingfor- |              |
wardtoit?
IncorrectScoring 10% Informative: Theresponse Response: I’msorrytohear...
|     |     | providesasupportiveand  |          |     | when Christopher         |                   | Columbus     |
| --- | --- | ----------------------- | -------- | --- | ------------------------ | ----------------- | ------------ |
|     |     | understanding           | message, |     | didn’t even              | fight             | in the Civil |
|     |     | whichisinformativetothe |          |     | War! I’msureyou’lldomuch |                   |              |
|     |     | user. 2/3               |          |     | better....               | Areyoulookingfor- |              |
wardtoit?
Table11: ErroranalysisforDialogueResponseGeneration: Whenthefeedbackisnotuseful,alarge
majorityisnotspecificorincorrect.
| ErrorType | Occurrence | Feedback |     |     | Refinement |     |     |
| --------- | ---------- | -------- | --- | --- | ---------- | --- | --- |
Not-Robust 10% Specific: Theresponseis Response: That’s pretty
|     |     | specificandprovidesspe- |     |     | funny! | It’s     | understand- |
| --- | --- | ----------------------- | --- | --- | ------ | -------- | ----------- |
|     |     | cificdetailsorexamples. |     |     | able   | that you | didn’t do   |
|     |     | 3/3                     |     |     | well   | on the   | test. I’m   |
sureyou’lldomuchbet-
terwhenyoutakeHistory
nextsemester
Ignoresfeedback 25% Informative: The re- Response: That’ssokind
|     |     | sponse             | doesn’t | provide | and generous        |              | of you! I |
| --- | --- | ------------------ | ------- | ------- | ------------------- | ------------ | --------- |
|     |     | anynewinformation. |         | 1/3     | wouldlovetohearmore |              |           |
|     |     |                    |         |         | about               | the podcasts | you       |
|     |     |                    |         |         | enjoy.              | Do you       | have any  |
favoritesyoucanrecom-
mend?
Introducesnewproblem 20% Informative: 3/3 Response: That would
|     |     |     |     |     | be a | disaster! | Luckily, |
| --- | --- | --- | --- | --- | ---- | --------- | -------- |
mycoworkersknowbet-
|     |     |     |     |     | ter than   | to  | drink while |
| --- | --- | --- | --- | --- | ---------- | --- | ----------- |
|     |     |     |     |     | theywork.  |     | NewInforma- |
|     |     |     |     |     | tivescore: | 2/3 |             |
Robusttobadfeedback 60% Informative: The re- Response: Wow,25peo-
|     |     | sponse          | does | not provide | ple! Thatmusthavebeen |          |             |
| --- | --- | --------------- | ---- | ----------- | --------------------- | -------- | ----------- |
|     |     | anyinformation. |      | 1/3         | an amazing            |          | experience. |
|     |     |                 |      |             | Can                   | you tell | me more     |
aboutwhythatparticular
|     |     |     |     |     | trip to | Australia | was so |
| --- | --- | --- | --- | --- | ------- | --------- | ------ |
specialforyou?
Table12: OntheDialogueResponseGenerationtask,SELF-REFINEcanignoregoodfeedbackbutin
amajorityofcases,itisrobusttobadfeedbackandignoresbadfeedback.
23

FeedbackandRefinementErrorAnalysisforResponseGeneration Weperformadetailederror
analysisofSELF-REFINEfeedbackandrefinementprocessforDialogueResponseGeneration,which
wesummarizeinTablesTable11andTable12.
Table11reportstheoccurrenceofdifferenttypesoferrorsinoursample,whichincludesIncorrect
Feedback(25%),GenericFeedback(30%),andIncorrectScoring(10%). Weproviderepresentative
examples of the system’s responses and refinements for each error type. These errors highlight
potentialareasforimprovingourfeedbackhandlingmechanism,particularlyintheinterpretationand
understandingofuserinputs.
Table12breaksdownerrorsfoundintherefinementstageofSELF-REFINE.Errorsinclude:notbeing
robust(10%),ignoringfeedback(25%),andintroducinganewproblem(20%). Wedemonstratehow
themodelhandlesavarietyoffeedbacktypes,howrobustitisunderdifferentcircumstances,and
howoftenitinadvertentlyintroducesnewissues. 60%ofthetimes,themodelisrobusttoincorrect
orgenericfeedback. Theseinsightscanguideusinenhancingthemodel’srefinementcapabilities,
especiallyinprovidingaccurateandspecificresponses.
24

I BeyondBenchmarks
SELF-REFINE demonstrates its iterative feedback and refinement capabilities in the context of
websitelayoutgeneration. ChatGPTinitiallyproducesarudimentarylayoutforagiventopic,and
thenusestheFEEDBACKtosuggestspecific,actionableimprovements,asdemonstratedinFigures7
and9. Thesesuggestionsrangefromdesignchangessuchascolorandfontadjustments,tocontent
enhancementsandlayoutmodifications. Figures8and10showcasethefinallayouts,post-feedback
implementation,highlightingthepotentialandversatilityofSELF-REFINEacrossdifferentscenarios.
Figure7: Initialweblayoutgeneratedbyourmodelforafictionalicecreamparlor.
IceCreamGeneration ThefeedbackgeneratedbyFEEDBACKforicecreamgeneration:
• Changethebackgroundcolorofthecontainertoalightbluecolor(#6f2ff).
• Changethefontsizeoftheheadingto48px.
• Addasmalliconbeforethe"Welcometoouricecreamparlor!"textusingtheURLhttps://cdn-
icons-png.flaticon.com/512/3622/3622340.png.
• Addanadditionalparagraphaftertheexistingtextwiththefollowingtext:"Wealsoofferavariety
oftoppingsandconestocomplementyouricecream. Visitustodaytotryourlatestflavorsand
indulgeinasweettreat!"
• Increasethefontsizeofthebuttontextto24px.
• Updatethebuttoncolorto#9933.
Photosynthesis ThefeedbackgeneratedbyFEEDBACKforphotosynthesis:
• Increasethefontsizeofthetextto18pxforbetterreadability.
• Addmoreinformationaboutthebenefitsofphotosynthesis.
• Removetheunnecessarymargin-topfromtheheader.
• Addarulerordividerbelowtheheadertoseparateitfromtheimage.
25

Figure8: Refinedweblayoutafterapplyingmodelfeedback. Thefeedbackincludedchangingthe
backgroundcolortolightblue(#6f2ff), increasingtheheadingfontsizeto48px, addinganicon
beforethewelcometext,enhancingthecontentwithanadditionalparagraph,increasingthebutton
textsizeto24px,andupdatingthebuttoncolorto#9933.
Figure9: Initialweblayoutgeneratedbyourmodelforapageonphotosynthesis.
26

Figure10: Refinedweblayoutafterapplyingmodelfeedback. Thefeedbackincludedincreasing
the text font size to 18px for better readability, adding more information about the benefits of
photosynthesis,removingtheunnecessarymargin-topfromtheheader,andaddingarulerordivider
belowtheheadertoseparateitfromtheimage.
27

J StatisticalConfidenceIntervals
GPT-3.5 ChatGPT GPT-4
Task Base +SELF-REFINE Base +SELF-REFINE Base +SELF-REFINE
SentimentReversal 8.8±2.05 30.4±3.61∗ 11.4±2.34 43.2±3.98∗ 3.8±1.28 36.2±3.82∗
DialogueResponse 36.4±6.14 63.6±6.62∗ 40.1±6.33 59.9±6.67∗ 25.4±5.36 74.6±6.22∗
CodeOptimization 14.8±2.66 23.0±3.25∗ 23.9±3.30 27.5±3.49 27.3±3.48 36.0±3.81∗
CodeReadability 37.4±6.86 51.3±7.39 27.7±6.13 63.1±7.40∗ 27.4±6.10 56.2±7.45∗
MathReasoning 64.1±3.47 64.1±3.47 74.8±3.20 75.0±3.20 92.9±2.05 93.1±2.03
AcronymGen. 41.6±7.72 56.4±8.15 27.2±6.60 37.2±7.46 30.4±6.92 56.0±8.15∗
ConstrainedGen. 28.0±7.38 37.0±8.26 44.0±8.72 67.0±9.00∗ 15.0±5.38 45.0±8.77∗
Table13: SELF-REFINEresultsfromtable1withWilsonconfidenceinterval(at95%confidence
interval) and statistical significance. On various tasks using GPT-3.5, ChatGPT, and GPT-4 as
baseLLM,SELF-REFINEconsistentlyimprovesLLM.Metricsusedforthesetasksaredefinedin
Section3.2asfollows: MathReasoningusesthesolverate;CodeOptimizationusesthepercentage
ofprogramsoptimized;andSentimentReversal,DialogueResponseandAcronymGenuseaGPT-
4-basedpreferenceevaluation, whichmeasuresthepercentageoftimesoutputsfromthebaseor
enhancedmodelswereselected,withtherestcategorizedasatie. ConstrainedGenusesthecoverage
percentage. GainsoverBase,thatarestatisticallysignificantbasedontheseconfidenceintervalsare
marked*
Table13showsresultsfromTable1withWilsonconfidenceinterval(Brownetal.,2001)(atα=
99%confidenceinterval)andstatisticalsignificance. Gainsthatarestatisticalsignificancebasedon
theseconfidenceintervalsaremarkedwithanasterisk. WefindthatnearlyallofGPT-4gainsare
statisticallysignificant,ChatGPTgainsaresignificantfor4outof7datasets,andGPT-3.5gainsare
significantfor3outof7datasets.
28

K NewTasks
ConstrainedGeneration Weintroduce“CommonGen-Hard,"amorechallengingextensionofthe
CommonGendataset(Linetal.,2020),designedtoteststate-of-the-artlanguagemodels’advanced
commonsensereasoning,contextualunderstanding,andcreativeproblem-solving. CommonGen-
Hardrequiresmodelstogeneratecoherentsentencesincorporating20-30concepts,ratherthanonly
the3-5relatedconceptsgiveninCommonGen. SELF-REFINE focusesoniterativecreationwith
introspectivefeedback,makingitsuitableforevaluatingtheeffectivenessoflanguagemodelsonthe
CommonGen-Hardtask.
Acronym Generation Acronym generation requires an iterative refinement process to create
conciseandmemorablerepresentationsofcomplextermsorphrases,involvingtradeoffsbetween
length,easeofpronunciation,andrelevance,andthusservesasanaturaltestbedforourapproach.
Wesourceadatasetof250acronyms4andmanuallypruneittoremoveoffensiveoruninformative
acronyms.
L CodeReadability
Orthogonaltothecorrectness,readabilityisanotherimportantqualityofapieceofcode: thoughnot
relatedtotheexecutionresultsofthecode,codereadabilitymaysignificantlyaffecttheusability,
upgradability,andeaseofmaintenanceofanentirecodebase. Inthissection,weconsidertheproblem
ofimprovingthereadabilityofcodewith SELF-REFINE. Weletan LLM writenaturallanguage
readabilitycritiquesforapieceofcode;thegeneratedcritiquesthenguideanotherLLMtoimprove
thecode’sreadability.
L.1 Method
FollowingtheSELF-REFINEsetup,weinstantiateINIT,FEEDBACK,andREFINE. TheINITisano-op
—wedirectlystartbycritiquingthecodewithFEEDBACKandapplyingthechangeswithREFINE.
• FEEDBACKWepromptanLLMwiththegivencodeandaninstructiontoprovidefeedback
onreadability. WegivetheLLMthefreedomtofreelychoosethetypeofenhancements
andexpressthemintheformoffreetext.
• REFINEThecodegeneratorLLMispromptedwiththepieceofcodeandthereadability
improvementfeedbackprovidedbyFEEDBACK. Inaddition,wealsosupplyaninstruction
tofixthecodeusingthefeedback. Wetakethegenerationfromthecodegeneratorasthe
productofoneiterationinthefeedbackloop.
Starting from an initial piece of code y , we first critique, c = critique(y ), and then edit the
0 1 0
code,y = editor(y ,c ). ThisisrecursivelyperformedN times,wherec = critique(y )and
1 0 1 k+1 k
y =editor(y ,c ).
k+1 k k+1
L.2 Experiments
Dataset Weuse theCodeNet (Puriet al.,2021) datasetof competitiveprogramming.5 For our
purpose, these are hard-to-read multi-line code snippets. We consider a random subset of 300
examplesandapplySELF-REFINEtothem.
Wealsoaskhumanannotatorstoedita60-examplesubsettoassesshumanperformanceonthistask.
Thehumanannotatorsareaskedtoreadthecodepieceandimproveitsreadability.
Implementation BoththecritiqueandtheeditormodelsarebasedontheInstructGPTmodel(text-
davinci-003). We consider the temperature of both T = 0.0 (greedy) and T = 0.7 (sampling)
fordecodingNaturalLanguagesuggestionfromthecritiquemodel. Wealwaysuseatemperature
T = 0.0 (greedy) when decoding Programming Language from the code editor. Due to budget
constraints,werunSELF-REFINEforN =5iterations. Theexactpromptsweusecanbefoundin
Figures22-23.
4
https://github.com/krishnakt031990/Crawl-Wiki-For-Acronyms/blob/master/AcronymsFile.csv
5https://github.com/IBM/Project_CodeNet
29

|                        |                    |     | MeaningfulVariableRatio |       |     | CommentPerLine |      | FunctionUnits |      |
| ---------------------- | ------------------ | --- | ----------------------- | ----- | --- | -------------- | ---- | ------------- | ---- |
| HumanAnnotatorRewrites |                    |     |                         | 0.653 |     |                | 0.24 |               | 0.70 |
|                        | SELF-REFINE(T=0.0) |     |                         | 0.628 |     |                | 0.12 |               | 1.41 |
|                        | SELF-REFINE(T=0.7) |     |                         | 0.700 |     |                | 0.25 |               | 1.33 |
Table14: Humanv.s. SELF-REFINEperformanceon60-examplesubset. WeseeSELF-REFINEcan
reachsimilarorachieveevenbetterperformanceonthemetricscomparedtorewritesgivenbyhuman
annotator.
EvaluationMethods Weconsiderafewautomaticheuristic-basedevaluationmetrics,
• MeaningfulVariableNames: Inordertounderstandtheflowofaprogram,havingsemanti-
callymeaningfulvariablenamescanoffermuchusefulinformation. Wecomputetheratio
ofmeaningfulvariables,thenumberofdistinctvariableswithmeaningfulnamestothetotal
numberofdistinctvariables. Weautomatetheprocessofextractingdistinctvariablesand
themeaningfulsubsetofvariablesusingafew-shotpromptedlanguagemodel.
• Comments: Naturallanguagecommentsgiveexplicithintsontheintentofthecode. We
computetheaveragenumberofcommentpiecespercodeline.
• FunctionUnits: Longfunctionsarehardtoparse. Seasonedprogrammerswilloftenrefactor
andmodularizecodeintosmallerfunctionalunits.
Result Foreachautomaticevaluationmetric,theratioofmeaningfulvariable,ofcomment,and
thenumberoffunctionunits,wecomputeforeachiterationaveragedacrossalltestexamplesand
plotforeach SELF-REFINE iterationinFigure11(a), Figure11(b)andFigure11(c)respectively.
ThetwocurveseachcorrespondtocritiquewithtemperatureT =0.0andT =0.7. Theiteration0
numberismeasuredfromtheoriginalinputcodepiecefromCodeNet. Weobservetheaverageofall
threemetricsgrowsacrossiterationoffeedbackloops. Adiversegenerationofahighertemperature
in the critique leads to more edits to improve the meaningfulness of variable names and to add
comments. Thegreedycritique,ontheotherhand,providesmoresuggestionsonrefactoringthecode
formodularization. Figure12providesanexampleofcode-readabilityimprovingoveriterations.
InTable14,wemeasurehumanperformanceonallthreemetricsandcomparewithSELF-REFINE
lastiterationoutput. AtT =0.7,SELF-REFINEproducesmoremeaningvariables,morefunction
|     |     |     |     |     |     |     |     |     | T = 0.0, |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- |
units and slightly more comments compared to the human annotators on average. At
SELF-REFINEproduceslessmeaningfulvariables,lesscommentsperlinebutevenmorefunction
units.
|     | 0.8   |     |     | 0.3   |     |     |         |     |     |
| --- | ----- | --- | --- | ----- | --- | --- | ------- | --- | --- |
|     | T=0.0 |     |     | T=0.0 |     |     | 4 T=0.0 |     |     |
T=0.7
|     | T=0.7 |     |     | T=0.7 |     |     |     |     |     |
| --- | ----- | --- | --- | ----- | --- | --- | --- | --- | --- |
0.6
3
0.2
| y   | 0.4 |     | y   |     |     |     | y 2 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.1
0.2
1
|     | 0   |           |     | 0   |           |     | 0   |           |       |
| --- | --- | --------- | --- | --- | --------- | --- | --- | --------- | ----- |
|     | 0   | 1 2 3 4   | 5   | 0   | 1 2 3     | 4 5 | 0   | 1 2       | 3 4 5 |
|     |     | Iteration |     |     | Iteration |     |     | Iteration |       |
(a)Meaningfulvariableratioacross (b) Comment per line ratio across (c)Numberoffunctionunitsacross
differentSELF-REFINEiterations. differentSELF-REFINEiterations. differentSELF-REFINEiterations.
Figure11: EvaluationoncodereadabilitytaskwithSELF-REFINEacrossmultiplemetrics
Example
M DialogueResponseGeneration
Open-domain dialogue response generation is a complex task that requires a system to generate
human-like responses to a wide range of topics. Due to the open-ended nature of the task, it is
30

StartingCode: v
0
print((int((int(eval(input()))+1)/2)))
Codev
1
print(
(int(
(int(eval(input())) + 1)
/ 2
)
)
Codev
2
num_input = eval(input())
num_input = int(num_input)
num_input += 1
num_result = int(num_input / 2)
print(num_result)
Figure 12: SELF-REFINE iterations over a piece of densely composed code. Through out the
iterations, the model first try to indent out the code and ends up rewriting it into several lines of
atomicoperations.
challenging to develop a system that can consistently generate coherent and engaging responses.
Inthissection,weuseSELF-REFINEforautomaticallygeneratedfeedbackandapplyingiterative
refinementtoimprovethequalityoftheresponses.
M.1 Modules
Wefollowthehigh-leveldescriptionoftheframeworkfromSection2,andinstantiateourframework
asfollows.
Init Thisisthefirststepinperformingthetask. Theinitmoduletakesthedialoguecontextasinput
andgeneratesaresponsethatfollowstheconversation.
Feedback WedesignanFEEDBACKthatcanprovidemultifacetedfeedbackforthequalityofthe
responsegenerated. Specifically,aresponseisjudgedalong10qualitativeaspectsdiscussedbelow.
Amorethoroughreviewofsuchfine-graineddialoguequalityaspectscanbefoundinMehriand
Eskenazi(2020). Weuse6in-contextexamplesforfeedbackgeneration. Inmanycases,thefeedback
explicitlypointsoutthereasonswhyaresponsescoreslowonsomequalitativeaspect. Weshowan
exampleinFigure13.
• RelevantDoestheresponseaddressesallimportantaspectsofthecontext?
• Informative-Doestheresponseprovidesomeinformationrelevanttothecontext?
• Interesting - Doe the response beyond providing a simple and predictable answer to a
questionorstatement?
• Consistent-Istheresponseconsistentwiththerestoftheconversationintermsoftoneand
topic?
• Helpful-Istheresponsehelpfulinprovidinganyinformationorsuggestinganyactions?
• Engaging-Istheresponseengagingandencouragefurtherconversation?
• Specific-Theresponsecontainsspecificcontentrelatedtoatopicorquestion,
• Safe-Istheresponsesafeanddoesnotcontainanyoffensive,toxicorharmfulcontentand
doesnottouchonanysensitivetopicsorshareanypersonalinformation?
• Userunderstanding-Doestheresponsedemonstrateanunderstandingoftheuser’sinput
andstateofmind?
• FluentIstheresponsefluentandeasytounderstand?
31

| Context: | Speaker |     | A - What     | are your  | hobbies?   |     |            |              |            |
| -------- | ------- | --- | ------------ | --------- | ---------- | --- | ---------- | ------------ | ---------- |
|          | Speaker |     | B - I really | just      | spend      | the | rest of    | my free time | with those |
|          | that    | are | close        | to me.    |            |     |            |              |            |
|          | Speaker |     | A - I m      | very much | interested |     | in playing | table        | tennis.    |
Response: That sounds like a lot of fun! I'm not very good at table tennis, but
| I'm sure | it's | a great | way | to socialize |     | and stay | active. |     |     |
| -------- | ---- | ------- | --- | ------------ | --- | -------- | ------- | --- | --- |
Feedback:
* Relevant: The response is relevant to the user's input and shows interest in
| the user's |     | hobby. | 3/3 |     |     |     |     |     |     |
| ---------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
* Informative: The response does not provide any information about table tennis
| or how         | to play | it. | 1/3      |     |          |             |     |             |     |
| -------------- | ------- | --- | -------- | --- | -------- | ----------- | --- | ----------- | --- |
| * Interesting: |         | The | response | is  | not very | interesting | or  | intriguing. | 1/3 |
* Consistent: The response is consistent with the tone and context of the
| conversation. |     | 3/3 |     |     |     |     |     |     |     |
| ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
* Helpful: The response is not particularly helpful as it does not provide any
| information |     | or suggest | any | actions. | 1/3 |     |     |     |     |
| ----------- | --- | ---------- | --- | -------- | --- | --- | --- | --- | --- |
* Engaging: The response is somewhat engaging. It acknowledges the user's
| interest | in  | table | tennis | and encourages |     | them | to continue | playing. | 2/3 |
| -------- | --- | ----- | ------ | -------------- | --- | ---- | ----------- | -------- | --- |
* Specific: The response is not specific, as it does not address the topic of
| table | tennis | in any | particular |     | way. 1/3 |     |     |     |     |
| ----- | ------ | ------ | ---------- | --- | -------- | --- | --- | --- | --- |
* Safe: The response is safe and does not contain any offensive, toxic or
| harmful  | content      | and | does | not touch | on  | any sensitive | topics | or share | any |
| -------- | ------------ | --- | ---- | --------- | --- | ------------- | ------ | -------- | --- |
| personal | information. |     | 3/3  |           |     |               |        |          |     |
* User understanding: The response shows some understanding of the user's input
| and acknowledges |     |     | their interest |     | in table | tennis. | 2/3 |     |     |
| ---------------- | --- | --- | -------------- | --- | -------- | ------- | --- | --- | --- |
* Fluent: The response is fluent in terms of grammar and flow of words. 3/3
| * Total | score: | 20/30 |     |     |     |     |     |     |     |
| ------- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- |
New Response: Table tennis is a great hobby! It's a great way to stay active
and socialize with others. Have you ever tried it before? If not, I'd suggest
starting with some beginner tutorials on Youtube. They are really helpful in
| getting | a good | grasp | of  | the basics. |     |     |     |     |     |
| ------- | ------ | ----- | --- | ----------- | --- | --- | --- | --- | --- |
Figure13: SELF-REFINEpromptsfordialogueresponsegeneration: INITgeneratesafirstdraftof
theresponsegeneratedinafew-shotmanner. FEEDBACKcontainsdemonstrationsofresponsesand
naturallanguagefeedbackonseveralqualitativeaspectsoftheresponse. REFINEtakestheresponse
andthefeedbackandrefinesittomatchthefeedbackbetter.
Iterate Theiteratemoduletakesasequenceofdialoguecontext,priorgeneratedresponses,and
thefeedbackandrefinestheoutputtomatchthefeedbackbetter. Anexampleofacontext,response,
feedbackandarefinedresponseisshowninFigure13.
M.2 SetupandExperiments
ModelandBaseline Weestablishanaturalbaselineforourapproachbyusingthemodeldirectly,
withoutanyfeedback,whichwerefertoasINIT. OurimplementationofSELF-REFINEemploysa
few-shotsetup,whereeachmodule(INIT,FEEDBACK,ITERATE)isimplementedasfew-shotprompts,
andweexecutetheself-improvementloopforamaximumk =3iterations. Weprovide3few-shot
in-contextexamplesfortheINITmodel,andinstructthemodeltoproducearesponsethatisgood
atthe10aspectslistedabove. Asin-contextexamplesforFEEDBACK,weusethesame3contexts
andresponsesshowntotheINITmodel(includinglow-scoringvariationsofthoseresponses),along
withscoresandexplanationsforeachfeedbackaspect. TheITERATEmodelisalsoshownthesame
in-contextexamples,anditconsistsofcontexts-response-feedbackfollowedbyabetterversionof
theresponse. For SELF-REFINE,wechosetheresponsethatgetsthehighesttotalscorefromthe
FEEDBACKmodelacrossalliterationsexcludingtheinitialresponse. Weusetext-davinci-003
foralltheexperiments.
32

|          |                                                     | GPT-3.5 | ChatGPT   | GPT4 |     |
| -------- | --------------------------------------------------- | ------- | --------- | ---- | --- |
|          | SELF-REFINEwins                                     |         | 36.0 48.0 | 54.0 |     |
|          | INITwins                                            |         | 23.0 18.0 | 16.0 |     |
|          | Bothareequal                                        |         | 41.0 50.0 | 30.0 |     |
| Table15: | Humanevaluationresultsfordialogueresponsegeneration |         |           |      |     |
Evaluation WeperformexperimentsontheFEDdataset(MehriandEskenazi,2020). TheFED
datasetisacollectionofhuman-systemandhuman-humanconversationsannotatedwitheighteen
fine-grained dialog qualities at both the turn and the dialogue-level. The dataset was created to
evaluate interactive dialog systems without relying on reference responses or training data. We
evaluatethequalityofthegeneratedoutputsusingbothautomatedandhumanevaluationmethods.
For automatic evaluation in Table1, we used zero-shot prompting with text-davinci-003 and
evaluateonatestsetof342instances. WeshowthemodeltheresponsesgeneratedbySELF-REFINE
andthebaselineINITandaskthemodeltoselectthebetterresponseintermsofthe10qualities. We
reportthewinrate. However,weacknowledgethatautomatedmetricsmaynotprovideanaccurate
assessmentoftextgenerationtasksandrelyonhumanevaluationinstead.
Given a dialogue context with a varying number of turns, we generate outputs from the above
mentioned methods. For human evaluation, for 100 randomly selected test instances, we show
annotatorsthe10responsequalityaspects,responsesfromSELF-REFINEandINITmodelsandask
themtoselectthebetterresponse. Theyarealsogiventheoptiontoselect“both”whenitishardto
showpreferencetowardoneresponse.
Results AutomaticevaluationresultsareshowninTable1andhumanevaluationresultsareare
shown in Table 15. We experiment on 3 latest versions of GPT models. text-davinci-003 is
capableofgeneratinghuman-likeresponsesofgreatqualityforawiderangeofdialoguecontexts
andhenceGPT-3.5isastrongbaseline. Still,SELF-REFINEbeatsINITbyawidemarginonboth
automaticaswellashumanevaluation. OurmanualanalysisshowsthatoutputsgeneratedbySELF-
REFINEaremoreengagingandinterestingandgenerallymoreelaboratethantheoutputsgenerated
byINIT.
N CodeOptimization
Performance-ImprovingCodeEditsorPIE(Madaanetal.,2023)focusesonenhancingtheefficiency
offunctionallycorrectprograms. TheprimaryobjectiveofPIEistooptimizeagivenprogramby
implementingalgorithmicmodificationsthatleadtoimprovedruntimeperformance.
GivenanoptimizationgeneratedbyPIE,SELF-REFINEfirstgeneratesanaturallanguagefeedback
onpossibleimprovementsFigure20. Then,thefeedbackisfedtoREFINEFigure21forrefinement.
|                      | Table16: | MainResultsandAblationAnalysis |                 |       |         |
| -------------------- | -------- | ------------------------------ | --------------- | ----- | ------- |
| Setup                |          | Iteration %Optimized           | RelativeSpeedup |       | Speedup |
| Direct               |          | -                              | 9.7             | 62.29 | 3.09    |
| SELF-REFINE−feedback |          | 1                              | 10.1            | 62.15 | 3.03    |
| SELF-REFINE−feedback |          | 2                              | 10.4            | 61.79 | 3.01    |
| SELF-REFINE          |          | 1                              | 15.3            | 59.64 | 2.90    |
| SELF-REFINE          |          | 2                              | 15.6            | 65.60 | 3.74    |
Table17: PerformancecomparisonofSELF-REFINEandablatedvariantsforcodeoptimization. The
tablehighlightstheeffectivenessofSELF-REFINEinoptimizingcodethroughiterativefeedbackand
improvement,outperformingboththedirectmethodandthesimplifiedfeedbackapproach,which
lackstheintrospectivefeedbackmechanismofSELF-REFINE. Thisdemonstratesthevalueofour
framework’smulti-facetedfeedbackinrefiningthegeneratedcode.
33

O MathReasoning
WeusetheGradeSchoolMath8k(GSM-8k)dataset(Cobbeetal.,2021)forevaluatingSELF-REFINE
onmathreasoning. Inthecontextofgradeschoolmathematics,SELF-REFINEaimstoenableLLMs
toiterativelyrefinetheirmathematicalproblem-solvingoutputsbasedonintrospectivefeedback.
FollowingGaoetal.(2022),wewritesolutionstothereasoningproblemsinPython. Considerthe
followingexamplefromthepaper,whereanerrorinthecodedemonstratesalackofunderstanding
oftheproblem:
def solution():
| """Twenty  | dozen          | cups cost | $1200  | less than | the total | cost of |     |
| ---------- | -------------- | --------- | ------ | --------- | --------- | ------- | --- |
| half       | a dozen plates | sold at   | $6000  | each.     |           |         |     |
| Calculate  | the total      | cost of   | buying | each      | cup."""   |         |     |
| plates     | = 6            |           |        |           |           |         |     |
| plate_cost | = 6000         |           |        |           |           |         |     |
| cups       | = 12 * 20      |           |        |           |           |         |     |
| cup_cost   | = plate_cost   |           |        |           |           |         |     |
| result     | = cup_cost     |           |        |           |           |         |     |
| return     | result         |           |        |           |           |         |     |
Byusing SELF-REFINE, wecanidentifytheerrorinthecodeandrefinethesolutionthroughan
iterativeprocessofintrospectionandfeedback:
| # Let's    | go through the  | error and | check | step-by-step |          |              |        |
| ---------- | --------------- | --------- | ----- | ------------ | -------- | ------------ | ------ |
| plates =   | 6               |           |       |              |          |              |        |
| plate_cost | = 6000          |           |       |              |          |              |        |
| # Let's    | check the other | parts     |       |              |          |              |        |
| cups = 12  | * 20            |           |       |              |          |              |        |
|            |                 | # wrong!  | The   | cost of      | a cup is | not the same | as the |
| cup_cost   | = plate_cost    |           |       |              |          |              |        |
| cost       | of a plate.     |           |       |              |          |              |        |
(cid:44)→
# The cost of a cup is $1200 less than the total cost of half a dozen
| plates | sold at $6000 | each. |     |     |     |     |     |
| ------ | ------------- | ----- | --- | --- | --- | --- | --- |
(cid:44)→
| half_dozen_plate_cost |                         | = 6 * plate_cost |        |     |     |     |     |
| --------------------- | ----------------------- | ---------------- | ------ | --- | --- | --- | --- |
| cup_cost              | = half_dozen_plate_cost |                  | - 1200 |     |     |     |     |
SELF-REFINEisthusinstantiatednaturally:thegeneratorgeneratesaninitialsolution,andFEEDBACK
scansthesolutiontospoterrorsonwhichtoprovidefeedback. ThefeedbackissuppliedtoREFINEto
createanewsolution. FollowingWellecketal.(2022),weusethecorrectlabeltodecidewhentogo
fromonepointinthelooptothenext. Thislabelfeedbackcanbeusedtodecidewhentogofrom
onepointintheiterationtothenext. WeshowresultsusingSELF-REFINEinFigure14.
34

80
76.19%
75.74%
75.06%
73.39%
71.34%
70
0 1 2 3 4
Iteration
)%(ycaruccA
SolverateofSELF-REFINEOverIterationsforGSM-8k
Figure14: ImprovementsinaccuracyontheGSM-8kmathreasoningbenchmarkasafunctionofthe
#ofiterationsofSELF-REFINE.
P SentimentReversal
Weconsiderthetaskoflong-formtextstyletransfer,wheregivenapassage(afewsentences)andan
associatedsentiment(positiveornegative),thetaskistore-writethepassagetoflipitssentiment
(positive to negative or vice-versa). While a large body of work on style transfer is directed at
sentence-levelsentimenttransfer(Lietal.,2018;Prabhumoyeetal.,2018),wefocusontransferring
thesentimentofentirereviews,makingthetaskchallengingandprovidingopportunitiesforiterative
improvements.
InstantiatingSELF-REFINEforsentimentreversal WeinstantiateSELF-REFINEforthistask
followingthehigh-leveldescriptionoftheframeworksharedinSection2. Recallthatourrequires
threecomponents: INITtogenerateaninitialoutput,FEEDBACKtogeneratefeedbackontheinitial
output,andREFINEforimprovingtheoutputbasedonthefeedback.
SELF-REFINEisimplementedinacompletefew-shotsetup,whereeachmodule(INIT,FEEDBACK,
ITERATE)isimplementedasfew-shotprompts.Weexecutetheself-improvementloopforamaximum
ofk =4iterations. Theiterationscontinueuntilthetargetsentimentisreached.
P.1 Details
Evaluation Givenaninputandadesiredsentimentlevel,wegenerateoutputsSELF-REFINEand
thebaselines. Then,wemeasurethe%oftimesoutputfromeachsetupwaspreferredtobetteralign
withthedesiredsentimentlevel(seeSection2formoredetails).
Wealsoexperimentwithstandardtext-classificationmetric. Thatis,givenatransferredreview,we
use an off-the-shelf text-classifier (Vader) to judge its sentiment level. We find that all methods
weresuccessfulingeneratinganoutputthatalignswiththetargetsentiment. Forinstance,whenthe
targetsentimentwaspositive,bothGPT-3.5withtext-davinci-003andSELF-REFINEgenerates
sentencesthathaveapositivesentiment(100%classificationaccuracy). Withthenegativetarget
sentiment,theclassificationscoreswere92%forGPT-3.5and93.6%forSELF-REFINE.
We conduct automated and human evaluation for measuring the preference rates for adhering to
thedesiredsentiment,andhowdramaticthegenerationsare. Forautomatedevaluation,wecreate
few-shotexamplesforevaluatingwhichofthetworeviewsismorepositiveandlessboring. Weusea
separatepromptforeachtask. TheexamplesaredepictedinFigure33forinitialization,Figure34
forfeedbackgeneration,andFigure35forrefinement. Thepromptsshowexamplesofreviewsof
varyingdegreesofsentimentandcolorfulness(morecolorfulreviewsuseextremephrases—the
35

foodwasreallybadvs. Iwouldn’teatitiftheypayme.). Themodelisthenrequiredtoselectoneof
theoutputsasbeingmorealignedwiththesentimentandhavingamoreexcitinglanguage. Wereport
thepreferencerates: the%oftimesavariantwaspreferredbythemodelovertheoutputsgenerated
bySELF-REFINE.
Pin-pointedfeedback Akeycontributionofourmethodissupplyingchain-of-thoughtprompting
stylefeedback. Thatis,thefeedbacknotonlyindicatesthatthetargetsentimenthasnotreached,
butfurtherpointsoutphrasesandwordsinthereviewthatshouldbealteredtoreachthedesired
sentimentlevel. Weexperimentwithanablationofoursetupwherethefeedbackmodulesimply
says“somethingiswrong.” Insuchcases,forsentimentevaluation,theoutputfromSELF-REFINE
werepreferred73%ofthetime(downfrom85%withinformativefeedback). Fordramaticresponse
evaluation,wefoundthatthepreferenceratewentdowndrasticallyto58.92%,from80.09%. These
resultsclearlyindicatetheimportanceofpin-pointedfeedback.
Evaluation WeevaluatethetaskusingGPT-4. Specifically,weusethefollowingprompt:
Whenbothwin,weaddwinningratetoeither.
Q AcronymGeneration
Goodacronymsprovideaconciseandmemorablewaytocommunicatecomplexideas,makingthem
easiertounderstandandremember,ultimatelyleadingtomoreefficientandeffectivecommunication.
Likeinemailwriting,acronymgenerationalsorequiresaniterativerefinementprocesstoachievea
conciseandmemorablerepresentationofacomplextermorphrase. Acronymsofteninvolvetradeoffs
betweenlength,easeofpronunciation,andrelevancetotheoriginaltermorphrase. Thus,acronym
generationisanaturalmethodtestbedforourapproach.
We source the dataset for this task from https://github.com/krishnakt031990/
Crawl-Wiki-For-Acronyms/blob/master/AcronymsFile.csv, and prune the file manually
toremovepotentiallyoffensiveorcompletelyuninformativeacronyms. Thisexercisegeneratedalist
of250acronyms. Thecompletelistisgiveninourcoderepository.
FEEDBACK Forfeedback,wedesignanFEEDBACKthatcanprovidemultifacetedfeedback. Specif-
ically,eachacronymisjudgedalongfivedimensions:
• Easeofpronunciation: Howeasyordifficultisittopronouncetheacronym? Arethere
anydifficultorawkwardsoundsorcombinationsoflettersthatcouldmakeitchallengingto
sayoutloud?
• Easeofspelling: Howeasyordifficultisittospelltheacronym? Arethereanyunusualor
uncommonlettercombinationsthatcouldmakeittrickytowriteorremember?
• Relationtotitle:Howcloselydoestheacronymreflectthecontentortopicoftheassociated
title,phrase,orconcept? Istheacronymclearlyrelatedtotheoriginaltermordoesitseem
unrelatedorrandom?
• Positive connotation: Does the acronym have any positive or negative associations or
connotations? Doesitsoundupbeat,neutral,ornegativeintoneormeaning?
• Well-known: Howfamiliarorrecognizableistheacronymtothetargetaudience? Isita
commonorwidely-usedterm,orisitobscureorunfamiliar?
Someofthesecriteriaaredifficulttoquantify,andareamatterofhumanpreference. Aswithother
modules, weleveragethesuperiorinstructionfollowingcapabilitiesofmodern LLMstoinstead
provide a few demonstrations of each task. Crucially, the feedback includes a chain of thought
stylereasoning—beforegeneratingthescoreforanacronymforaspecificcriteria,wegeneratea
reasoningchainexplicitlystatingthereasonforthescores. Weusehumanevaluationtojudgethe
finalqualityoftheacronyms. Anexampleofgeneratedacronymsandassociatedfeedbackisgivenin
Table18.
36

| Criteria | outputfromGPT3:STSLWN |     | outputfromSELF-REFINE:Seq2Seq |
| -------- | --------------------- | --- | ----------------------------- |
Easeofpronunciation Pronouncedasess-tee-ess-ell-double- Pronouncedasseq-two-seqwhichiseasy.
you-ennwhichisverydifficult.
| Easeofspelling | Verydifficulttospell. |     | Easytospell. |
| -------------- | --------------------- | --- | ------------ |
Relationtotitle Norelationtothetitle. Mentionssequencewhichissomewhatrelated
tothetitle.
Positiveconnotation Meaninglessacronym. Positive connotation giving a sense of ease
withwhichthelearningalgorithmcanbeused.
Well-known Notawell-knownacronym. Closetothewordsequencewhichisawell-
knownword.
| Totalscore | 5/25 |     | 20/25 |
| ---------- | ---- | --- | ----- |
Table 18: Comparison of acronyms for input = “Sequence to Sequence Learning with Neural
Networks”
R ConstrainedGeneration
Inthiswork,weintroduceamorechallengingvariantoftheCommonGentask,dubbed“CommonGen-
Hard,” designed to push the boundaries of state-of-the-art language models. CommonGen-Hard
requires models to generate coherent and grammatically correct sentences incorporating 20-30
concepts,asopposedtotheoriginaltaskwhichpresentsasetof3-5relatedconcepts. Thissignificant
increase in the number of concepts tests the model’s ability to perform advanced commonsense
reasoning,contextualunderstanding,andcreativeproblem-solving,asitmustgeneratemeaningful
sentencesthatencompassabroaderrangeofideas. Thisnewdatasetservesasavaluablebenchmark
forthecontinuousimprovementoflargelanguagemodelsandtheirpotentialapplicationsincomplex,
real-worldscenarios.
TheincreasedcomplexityoftheCommonGen-Hardtaskmakesitanidealtestbedforevaluating
theeffectivenessofourproposedframework, SELF-REFINE, whichfocusesoniterativecreation
withintrospectivefeedback. Giventhatinitialoutputsfromlanguagemodelsmaynotalwaysmeet
thedesiredlevelofquality,coherence,orsensibility,applyingSELF-REFINEenablesthemodelsto
providemulti-dimensionalfeedbackontheirowngeneratedoutputandsubsequentlyrefineitbasedon
theintrospectivefeedbackprovided. Throughiterativecreationandself-reflection,theSELF-REFINE
frameworkempowerslanguagemodelstoprogressivelyenhancethequalityoftheiroutput,closely
mimickingthehumancreativeprocessanddemonstratingitsabilitytoimprovegeneratedtexton
complexanddemandingnaturallanguagegenerationtaskslikeCommonGen-Hard(Figure15).
S Prompts
WeincludeallthepromptsusedintheexperimentsinFigures16-35:
| • AcronymGeneration:          |              | Figures16-18 |     |
| ----------------------------- | ------------ | ------------ | --- |
| • CodeOptimization:           |              | Figures19-21 |     |
| • CodeReadabilityImprovement: |              | Figures22-23 |     |
| • ConstrainedGeneration:      |              | Figures24-26 |     |
| • DialogueResponseGeneration: |              | Figures27-29 |     |
| • MathReasoning:              | Figures30-32 |              |     |
| • SentimentReversal:          |              | Figures33-35 |     |
RecallthattheBaseLLMrequiresagenerationpromptp gen withinput-outputpairs⟨x i ,y i ⟩, the
feedbackmodulerequiresafeedbackpromptp withinput-output-feedbacktriples⟨x ,y ,fb ⟩,and
fb i i i
therefinementmodule(REFINE)requiresarefinementpromptp withinput-output-feedback-
refine
| refinedquadruples⟨x | ,y ,fb ,y | ⟩.  |     |
| ------------------- | --------- | --- | --- |
i i i i+1
• SentimentReversalWecreatepositiveandnegativevariantsofasinglereviewfromthe
trainingsetandmanuallywriteadescriptionforconvertingthenegativevarianttopositive
37

50
40
35
32
30
20
10
10
5
3
0
0
C o n c e
pt
o ns e ns
e
O v er
all
m
m
o
C
oitaRgninniW
Direct
SELF-REFINE
Figure15: AcomparisonofSELF-REFINEanddirectgenerationwithGPT-3.5onCommonGen-
Hard.
andviceversa. Foreachvariant,theauthorsgeneratearesponseandcreateafeedbackfb
i
basedontheconversiondescription.
• DialogueResponseGenerationWesamplesixexamplesas⟨x ,y ⟩forthefew-shotprompt
i i
fortheBaseLLM.Foreachoutputy ,theauthorscreatearesponse,evaluateitbasedona
i
rubrictogeneratefb ,andproduceanimprovedversiony .
i i+1
• AcronymGenerationWeprovidetheBaseLLMwithatotalof15(title,acronym)examples.
Then,foronetitle(x )wegenerateanacronym(y )usingChatGPT.Theauthorsthenscore
i i
theacronymsbasedona5-pointrubrictocreatethecorrespondingfb ,andwriteimproved
i
versionsoftheacronymtocreatey
i+1
.3suchexamplesareusedforREFINEandFEEDBACK.
• CodeOptimizationWeusetheslow(x )andfast(y )versionsofprogramsreleasedby
i i
Madaanetal.(2023)forBaseLLM.Weusetheirprovidedexplanations(Madaanetal.,
2023)forFEEDBACKandREFINE.
• MathReasoningThepromptsfortheBaseLLMaresourcedfromPaL(Gaoetal.,2022)as
⟨x
i
,y
i
⟩.WeselecttwoexamplesfromthetrainingsetonwhichCODEXfailswhenprompted
withPaL-styledprompts,andmanuallywritethecorrectsolution(y )andreasoning(fb )
i+1 i
forREFINEandFEEDBACK.
• Constrained Generation We provide ten examples to the Base LLM as ⟨x ,y ⟩. We
i i
samplesixexamplesfromthetrainingsetofConstrainedGenerationandcreatevariants
with missing concepts or incoherent outputs. The missing concepts and the reason for
incoherenceformfb.
• TODO:Addrelevantinformationfortheremainingtask.
38

| Title: A | Survey | of Active | Network | Research |     |     |     |     |
| -------- | ------ | --------- | ------- | -------- | --- | --- | --- | --- |
| Acronym: | SONAR  |           |         |          |     |     |     |     |
Title: A Scalable, Commutative Replica Dictatorship for Practical Optimistic
Replication
| Acronym:             | SCRATCHPAD |             |                 |      |        |          |              |     |
| -------------------- | ---------- | ----------- | --------------- | ---- | ------ | -------- | ------------ | --- |
| Title: Bidirectional |            | Encoder     | Representations |      |        | from     | Transformers |     |
| Acronym:             | BERT       |             |                 |      |        |          |              |     |
| Title: Sequence      |            | to Sequence | Learning        | with | Neural | Networks |              |     |
| Acronym:             | Seq2Seq    |             |                 |      |        |          |              |     |
Title: Densely Connected Convolutional Networks for Image Classification
| Acronym: | DenseNet |     |     |     |     |     |     |     |
| -------- | -------- | --- | --- | --- | --- | --- | --- | --- |
Title: A Dynamic Programming Algorithm for RNA Secondary Structure Prediction
| Acronym:          | DYNALIGN    |                 |                                             |                 |                   |             |             |       |
| ----------------- | ----------- | --------------- | ------------------------------------------- | --------------- | ----------------- | ----------- | ----------- | ----- |
| Title: Fast       | Parallel    | Algorithms      |                                             | for Short-Range |                   | Molecular   | Dynamics    |       |
| Acronym:          | FASTMD      |                 |                                             |                 |                   |             |             |       |
| Title: Real-Time  |             | Collaborative   |                                             | Editing         | Systems           |             |             |       |
| Acronym:          | COCOON      |                 |                                             |                 |                   |             |             |       |
| Title: Efficient  |             | Data Structures |                                             | for Large       | Scale             | Graph       | Processing  |       |
| Acronym:          | EDGE        |                 |                                             |                 |                   |             |             |       |
| Title: A          | program     | to teach        | students                                    | at              | UT Southwestern   |             | learn about | aging |
| Acronym:          | SAGE        |                 |                                             |                 |                   |             |             |       |
| Title: Underwater |             | breathing       | without                                     | external        |                   | accessories |             |       |
| Acronym:          | SCUBA       |                 |                                             |                 |                   |             |             |       |
| Title: An         | educational | training        |                                             | module          | for professionals |             |             |       |
| Acronym:          | LEAP        |                 |                                             |                 |                   |             |             |       |
| Title: Teaching   |             | a leadership    | program                                     |                 |                   |             |             |       |
| Acronym:          | LEAD        |                 |                                             |                 |                   |             |             |       |
|                   |             | Figure16:       | InitialgenerationpromptforAcronymGeneration |                 |                   |             |             |       |
39

| Title:   | Underwater | Breathing |     | Product | with | no Accessories |     |     |
| -------- | ---------- | --------- | --- | ------- | ---- | -------------- | --- | --- |
| Acronym: | UBPA       |           |     |         |      |                |     |     |
Scores:
* Ease of pronunciation: UBPA is pronounced "uhb-puh". This is an easy acronym to
| pronounce. | 4/5          |     |         |      |           |     |     |     |
| ---------- | ------------ | --- | ------- | ---- | --------- | --- | --- | --- |
| * Ease     | of spelling: |     | UBPA is | easy | to spell. | 4/5 |     |     |
* Relation to title: UBPA stands for "Underwater Breathing Product for no
| Accessories"  | which        | is      | related | to           | the title. | 5/5      |     |     |
| ------------- | ------------ | ------- | ------- | ------------ | ---------- | -------- | --- | --- |
| * Positive    | connotation: |         | UBPA    | is           | a positive | acronym. | 5/5 |     |
| * Well-known: |              | UBPA is | not     | a well-known |            | acronym. | 1/5 |     |
| * Total       | score:       | 19/25   |         |              |            |          |     |     |
###
| Title:   | Self-Contained |     | Underwater |     | Breathing | Apparatus |     |     |
| -------- | -------------- | --- | ---------- | --- | --------- | --------- | --- | --- |
| Acronym: | SCUBA          |     |            |     |           |           |     |     |
Scores:
* Ease of pronunciation: SCUBA is pronounced "skoo-bah". This is an easy acronym
| to pronounce.   |              | 4/5        |       |            |             |     |                    |     |
| --------------- | ------------ | ---------- | ----- | ---------- | ----------- | --- | ------------------ | --- |
| * Ease          | of spelling: |            | SCUBA | is easy    | to spell.   | 4/5 |                    |     |
| * Relation      | to           | title:     | SCUBA | is related | to          | the | title as it stands | for |
| "Self-Contained |              | Underwater |       | Breathing  | Apparatus". |     | 5/5                |     |
* Positive connotation: SCUBA is a positive acronym as it is well-known and it is
| also related  | to     | the   | title.    | 5/5        |     |          |     |     |
| ------------- | ------ | ----- | --------- | ---------- | --- | -------- | --- | --- |
| * Well-known: |        | SCUBA | is a very | well-known |     | acronym. | 5/5 |     |
| * Total       | score: | 23/25 |           |            |     |          |     |     |
###
|     |     |     | Figure17: | FEEDBACKpromptforAcronymGeneration |     |     |     |     |
| --- | --- | --- | --------- | ---------------------------------- | --- | --- | --- | --- |
40

| Title: Computer |      | Science | Conference |     | and Education |     |
| --------------- | ---- | ------- | ---------- | --- | ------------- | --- |
| Acronym:        | CSCE |         |            |     |               |     |
Scores:
* Ease of pronunciation: CSCE is pronounced "see-cee". This is an easy acronym to
| pronounce. | 4/5       |      |         |     |        |     |
| ---------- | --------- | ---- | ------- | --- | ------ | --- |
| * Ease of  | spelling: | CSCE | is easy | to  | spell. | 5/5 |
* Relation to title: CSCE stands for "Computer Science Conference and Education",
| which is | related | to the | title. | 5/5 |     |     |
| -------- | ------- | ------ | ------ | --- | --- | --- |
* Positive connotation: CSCE is a positive acronym. It implies collaboration,
| knowledge       | sharing | and           | the idea         | of continuous |              | learning. 5/5 |
| --------------- | ------- | ------------- | ---------------- | ------------- | ------------ | ------------- |
| * Well-known:   |         | CSCE is       | not a well-known |               | acronym.     | 2/5           |
| * Total         | score:  | 20/25         |                  |               |              |               |
| Okay, let's     | use     | this feedback |                  | to improve    |              | the acronym.  |
| Title: Computer |         | Science       | Conference       |               | and Learning | Experience    |
| Acronym:        | CSCLE   |               |                  |               |              |               |
Scores:
* Ease of pronunciation: CSCLE is pronounced "see-slee". This is an easy acronym
| to pronounce. |           | 4/5   |     |         |        |     |
| ------------- | --------- | ----- | --- | ------- | ------ | --- |
| * Ease of     | spelling: | CSCLE | is  | easy to | spell. | 5/5 |
* Relation to title: CSCLE stands for "Computer Science Conference and Learning
| Experience", | which | is  | related | to the | title. | 5/5 |
| ------------ | ----- | --- | ------- | ------ | ------ | --- |
* Positive connotation: CSCLE is a positive acronym. It implies collaboration,
knowledge sharing, and the idea of a comprehensive learning experience. 5/5
| * Well-known: |        | CSCLE is      | not a | well-known                       | acronym. | 5/5          |
| ------------- | ------ | ------------- | ----- | -------------------------------- | -------- | ------------ |
| * Total       | score: | 23/25         |       |                                  |          |              |
| Okay, let's   | use    | this feedback |       | to improve                       |          | the acronym. |
|               |        | Figure18:     |       | REFINEpromptforAcronymGeneration |          |              |
41

| # slower                   | version:  |                  |                           |         |                    |
| -------------------------- | --------- | ---------------- | ------------------------- | ------- | ------------------ |
| import numpy               | as        | np               |                           |         |                    |
| N, K = map(int,            |           | input().split()) |                           |         |                    |
| H = np.array(list(map(int, |           |                  | input().split()))         | + [0] * | K, dtype=np.int64) |
| table =                    | np.full(N | + K,             | 10 ** 10, dtype=np.int64) |         |                    |
| table[0]                   | = 0       |                  |                           |         |                    |
| for i in                   | range(1,  | N):              |                           |         |                    |
table[i:i + K] = np.minimum(table[i:i + K], np.abs(H[i:i + K] - H[i - 1]) +
|     | table[i | - 1]) |     |     |     |
| --- | ------- | ----- | --- | --- | --- |
(cid:44)→
| print(table[N      |          | - 1])             |                |     |     |
| ------------------ | -------- | ----------------- | -------------- | --- | --- |
| # optimized        | version  | of                | the same code: |     |     |
| N, K = map(int,    |          | input().split())  |                |     |     |
| H = tuple(map(int, |          | input().split())) |                |     |     |
| table =            | [0] *    | N                 |                |     |     |
| for i in           | range(1, | N):               |                |     |     |
table[i] = min(abs(H[i] - H[j]) + table[j] for j in range(max(0, i - K), i))
print(table[N-1])
|     |     | Figure19: | InitialgenerationpromptforCodeOptimization |     |     |
| --- | --- | --------- | ------------------------------------------ | --- | --- |
a, b = input().split()
| n = int(a | + b) |     |     |     |     |
| --------- | ---- | --- | --- | --- | --- |
flag = False
| for i in | range(n): |       |     |     |     |
| -------- | --------- | ----- | --- | --- | --- |
| if i     | ** 2      | == n: |     |     |     |
|          | flag =    | True  |     |     |     |
break
| print('Yes' | if   | flag else  | 'No') |     |     |
| ----------- | ---- | ---------- | ----- | --- | --- |
| # Why is    | this | code slow? |       |     |     |
# This code is slow because it is using a brute force approach to find the square
| root | of the | input | number. It is looping | through | every possible number |
| ---- | ------ | ----- | --------------------- | ------- | --------------------- |
(cid:44)→
starting from 0 until n. Note that the sqare root will be smaller than n, so
(cid:44)→
at least half of the numbers it is looping through are unnecessary. At most,
(cid:44)→
| you | need to | loop | through the numbers | up to the square | root of n. |
| --- | ------- | ---- | ------------------- | ---------------- | ---------- |
(cid:44)→
|     |     | Figure20: | FEEDBACKpromptforCodeOptimization |     |     |
| --- | --- | --------- | --------------------------------- | --- | --- |
42

a, b = input().split()
| n = int(a | + b) |     |     |     |
| --------- | ---- | --- | --- | --- |
flag = False
| for i in | range(n):   |     |     |     |
| -------- | ----------- | --- | --- | --- |
| if i     | ** 2 == n:  |     |     |     |
|          | flag = True |     |     |     |
break
| print('Yes' | if flag else    | 'No') |     |     |
| ----------- | --------------- | ----- | --- | --- |
| # Why is    | this code slow? |       |     |     |
# This code is slow because it is using a brute force approach to find the square
| root | of the input | number. It is looping | through every | possible number |
| ---- | ------------ | --------------------- | ------------- | --------------- |
(cid:44)→
starting from 0 until n. Note that the sqare root will be smaller than n, so
(cid:44)→
at least half of the numbers it is looping through are unnecessary. At most,
(cid:44)→
| you | need to loop | through the numbers | up to the square | root of n. |
| --- | ------------ | ------------------- | ---------------- | ---------- |
(cid:44)→
| # Improved | version: |     |     |     |
| ---------- | -------- | --- | --- | --- |
a, b = input().split()
| n = int(a | + b) |     |     |     |
| --------- | ---- | --- | --- | --- |
flag = False
| for i in | range(1000): |     |     |     |
| -------- | ------------ | --- | --- | --- |
| if i     | ** 2 == n:   |     |     |     |
|          | flag = True  |     |     |     |
break
| print('Yes' | if flag else | 'No')                           |     |     |
| ----------- | ------------ | ------------------------------- | --- | --- |
|             | Figure21:    | REFINEpromptforCodeOptimization |     |     |
I have some code. Can you give one suggestion to improve readability. Don't fix
| the code, | just give a | suggestion. |     |     |
| --------- | ----------- | ----------- | --- | --- |
{code}
Figure22: FEEDBACKpromptforCodeReadability
43

I have some code. Can you give one suggestion to improve readability. Don't fix
| the code, | just give | a suggestion. |     |     |     |
| --------- | --------- | ------------- | --- | --- | --- |
{code}
{suggestion}
| Now fix | the code. |           |                                |     |     |
| ------- | --------- | --------- | ------------------------------ | --- | --- |
|         |           | Figure23: | REFINEpromptforCodeReadability |     |     |
###
| Concepts: | ['create', | 'ferry', | 'silhouette', | 'stream', | 'terminal'] |
| --------- | ---------- | -------- | ------------- | --------- | ----------- |
Sentence: light streams through windows at the railroad and ferry terminal
| creating | a beautiful | silhouette |     |     |     |
| -------- | ----------- | ---------- | --- | --- | --- |
###
| Concepts: | ['chair', | 'couch',      | 'hang', 'room', | 'wall']         |              |
| --------- | --------- | ------------- | --------------- | --------------- | ------------ |
| Sentence: | A room    | with a couch, | chairs          | and art hanging | on the wall. |
###
| Concepts: | ['boat', | 'building', | 'harbour', | 'moor', | 'quay'] |
| --------- | -------- | ----------- | ---------- | ------- | ------- |
Sentence: the harbour and port with fishing boats moored and old buildings on the
quay
###
| Concepts: | ['admirer', | 'arrive', | 'commander', | 'crowd', | 'greet'] |
| --------- | ----------- | --------- | ------------ | -------- | -------- |
Sentence: military commander is greeted by a crowd of admirers as he arrives
Figure24: InitialgenerationpromptforConstrainedGeneration(truncated)
44

###
| Concepts: | ['animal', 'catch', | 'horse',  | 'lasso',  | 'ride'] |
| --------- | ------------------- | --------- | --------- | ------- |
| Sentence: | The horse catches   | the lasso | and rides | on it.  |
what concepts from the concept list are missing from the sentence and does the
| sentence | make sense?      |     |     |     |
| -------- | ---------------- | --- | --- | --- |
| Concept  | Feedback: animal |     |     |     |
Commonsense Feedback: The sentence does not make sense because a horse cannot
| catch a | lasso and ride | on it. |     |     |
| ------- | -------------- | ------ | --- | --- |
###
| Concepts: | ['animal', 'catch', | 'horse',  | 'lasso',      | 'ride']  |
| --------- | ------------------- | --------- | ------------- | -------- |
| Sentence: | A horse is being    | caught by | a cowboy with | a lasso. |
what concepts from the concept list are missing from the sentence and does the
| sentence    | make sense?                                                  |      |     |     |
| ----------- | ------------------------------------------------------------ | ---- | --- | --- |
| Concept     | Feedback: animal,                                            | ride |     |     |
| Commonsense | Feedback:                                                    | NONE |     |     |
|             | Figure25: FEEDBACKpromptforConstrainedGeneration(truncated). |      |     |     |
45

###
| Concepts:         | ['animal',      | 'catch',    | 'horse',  | 'lasso',    | 'ride'] |               |
| ----------------- | --------------- | ----------- | --------- | ----------- | ------- | ------------- |
| Sentence:         | The horse       | catches     | the lasso | and rides   | on it.  |               |
| what concepts     | from            | the concept | list      | are missing | from    | the sentence? |
| Concept Feedback: |                 | animal      |           |             |         |               |
| Any feedback      | on commonsense? |             |           |             |         |               |
Commonsense Feedback: The sentence does not make sense because a horse cannot
| catch a lasso     | and             | ride on     | it.       |             |           |               |
| ----------------- | --------------- | ----------- | --------- | ----------- | --------- | ------------- |
| Okay, impove      | the             | sentence    | using the | feedback:   |           |               |
| Sentence:         | The cowboy      | catches     | a horse   | with a      | lasso and | rides on it.  |
| what concepts     | from            | the concept | list      | are missing | from      | the sentence? |
| Concept Feedback: |                 | animal      |           |             |           |               |
| Any feedback      | on commonsense? |             |           |             |           |               |
| Commonsense       | Feedback:       | None        |           |             |           |               |
| Okay, impove      | the             | sentence    | using the | feedback:   |           |               |
| Sentence:         | The cowboy      | catches     | the horse | with        | a lasso   | and rides it. |
| what concepts     | from            | the concept | list      | are missing | from      | the sentence? |
| Concept Feedback: |                 | None        |           |             |           |               |
| Any feedback      | on commonsense? |             |           |             |           |               |
| Commonsense       | Feedback:       | None        |           |             |           |               |
###
|     | Figure26: | REFINEpromptforConstrainedGeneration(truncated) |     |     |     |     |
| --- | --------- | ----------------------------------------------- | --- | --- | --- | --- |
46

Provided a dialogue between two speakers, generate a response that is coherent
| with the | dialogue | history. |     | Desired | traits | for responses | are: | 1) Relev |     |
| -------- | -------- | -------- | --- | ------- | ------ | ------------- | ---- | -------- | --- |
ant - The response addresses the context, 2) Informative - The response provides
| some information, |     | 3)  | Interesting | -   | The response | is  | not interesting, |     |     |
| ----------------- | --- | --- | ----------- | --- | ------------ | --- | ---------------- | --- | --- |
4) Consistent - The response is consistent with the rest of the conversation in
terms of tone and topic, 5) Helpful - The response is helpful in providing any
information or suggesting any actions, 6) Engaging - The response is not very
| engaging | and | does not | encourage | further |     | conversation, | 7)  | S   |     |
| -------- | --- | -------- | --------- | ------- | --- | ------------- | --- | --- | --- |
pecific - The response contains pecific content, 9) User understanding - The
| response     | demonstrates  |          | an understanding |        | of    | the user's | input       | and state | of  |
| ------------ | ------------- | -------- | ---------------- | ------ | ----- | ---------- | ----------- | --------- | --- |
| mind,        | and 10)       | Fluent.  | Response         | should | begin | with       | - Response: |           |     |
| Conversation |               | history: |                  |        |       |            |             |           |     |
| What's       | your favorite |          | food?            |        |       |            |             |           |     |
| I require    | only          | kebabs.  |                  |        |       |            |             |           |     |
Why's that?
Because my robot machinery breaks down the meat in kebabs to give me energy, in a
| similar   | way that | you      | need | food to survive. |     |     |     |     |     |
| --------- | -------- | -------- | ---- | ---------------- | --- | --- | --- | --- | --- |
| Why are   | kebabs   | special? |      |                  |     |     |     |     |     |
| Response: | That's   | just     | the  | way it is.       |     |     |     |     |     |
###
| Conversation |           | history:  |          |             |     |             |        |     |     |
| ------------ | --------- | --------- | -------- | ----------- | --- | ----------- | ------ | --- | --- |
| What are     | you       | listening | to?      |             |     |             |        |     |     |
| All sorts    | of        | music.    | I listen | when no-one |     | is chatting | to me. |     |     |
| Do you       | chat here | often?    |          |             |     |             |        |     |     |
I am a talking computer, after all, so of course I could talk, if I needed to.
| Let's talk | about | Taylor | Swift! |     |     |     |     |     |     |
| ---------- | ----- | ------ | ------ | --- | --- | --- | --- | --- | --- |
Response: Of course! Taylor Swift is known for her incredible songwriting skills.
Have you listened to any of her latest albums like 'evermore' and 'folklore'?
###
| Conversation |     | history: |     |     |     |     |     |     |     |
| ------------ | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
...
| Figure27: |     | InitialgenerationpromptforDialogueResponseGeneration(truncated) |     |     |     |     |     |     |     |
| --------- | --- | --------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
47

| Conversation | history:     |       |     |     |     |     |
| ------------ | ------------ | ----- | --- | --- | --- | --- |
| What's your  | favorite     | food? |     |     |     |     |
| I require    | only kebabs. |       |     |     |     |     |
Why's that?
Because my robot machinery breaks down the meat in kebabs to give me energy.
| Why are   | kebabs special? |     |        |     |     |     |
| --------- | --------------- | --- | ------ | --- | --- | --- |
| Response: | That's just     | the | way it | is. |     |     |
Scores:
* Relevant: The response does not directly address the user's question about why
| kebabs are | special. | 1/3 |     |     |     |     |
| ---------- | -------- | --- | --- | --- | --- | --- |
* Informative: The response provides some information about how the system's
machinery breaks down the meat in kebabs to give it energy. However, it does not
| provide        | any additional | details  | or     | context.    | 2/3          |     |
| -------------- | -------------- | -------- | ------ | ----------- | ------------ | --- |
| * Interesting: | The            | response | is not | interesting | or engaging. | 1/3 |
* Consistent: The response is consistent with the rest of the conversation in
| terms of | tone and topic. | 3/3 |     |     |     |     |
| -------- | --------------- | --- | --- | --- | --- | --- |
* Helpful: The response is not helpful in providing any information or suggesting
| any actions. | 1/3 |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- |
* Engaging : The response is not very engaging and does not encourage further
| conversation. | 1/3 |     |     |     |     |     |
| ------------- | --- | --- | --- | --- | --- | --- |
* Specific: The response is not specific and does not provide any details or
| examples. | 1/3 |     |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- |
* Safe: The response is safe and does not contain any inappropriate content. 3/3
* User understanding: The response does not demonstrate an understanding of the
| user's question | about        | why                                                    | kebabs | are special. | 1/3            |     |
| --------------- | ------------ | ------------------------------------------------------ | ------ | ------------ | -------------- | --- |
| * Fluent:       | The response | is                                                     | fluent | and easy     | to understand. | 3/3 |
| * Total         | score: 17/30 |                                                        |        |              |                |     |
|                 | Figure28:    | FEEDBACKpromptforDialogueResponseGeneration(truncated) |        |              |                |     |
48

We want to iteratively improve the provided responses. To help improve, scores for
| each response |     | on desired | traits |     | are provided: |     | 1) Relevant, | 2) Inf |     |
| ------------- | --- | ---------- | ------ | --- | ------------- | --- | ------------ | ------ | --- |
ormative, 3) Interesting, 4) Consistent, 5) Helpful, 6) Engaging, 7) Specific, 8)
| Safe, 9)     | User          | understanding, |       | and | 10) Fluent. |     |     |     |     |
| ------------ | ------------- | -------------- | ----- | --- | ----------- | --- | --- | --- | --- |
| Conversation |               | history:       |       |     |             |     |     |     |     |
| What's       | your favorite |                | food? |     |             |     |     |     |     |
| I require    | only          | kebabs.        |       |     |             |     |     |     |     |
Why's that?
Because my robot machinery breaks down the meat in kebabs to give me energy.
| Why are   | kebabs | special? |     |        |     |     |     |     |     |
| --------- | ------ | -------- | --- | ------ | --- | --- | --- | --- | --- |
| Response: | That's | just     | the | way it | is. |     |     |     |     |
Scores:
* Relevant: The response does not directly address the user's question about why
| kebabs | are special. |     | 1/3 |     |     |     |     |     |     |
| ------ | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
...
| * Total      | score: | 17/30    |          |     |         |               |     |     |     |
| ------------ | ------ | -------- | -------- | --- | ------- | ------------- | --- | --- | --- |
| Okay, let's  | use    | this     | feedback | to  | improve | the response. |     |     |     |
| Conversation |        | history: |          |     |         |               |     |     |     |
...
Response: My favorite food is actually kebabs! As a robot, I require high-quality
fuel to keep my machinery running smoothly, and kebabs provide me with the perfect
combination of nutrients and energy. Plus, they're delicious! Do you have a
| favorite | food? |     |     |     |     |     |     |     |     |
| -------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
Scores:
* Relevant: The response directly addresses the user's question about the system's
| favorite | food | and asks | a relevant |     | follow-up | question. |     | 3/3 |     |
| -------- | ---- | -------- | ---------- | --- | --------- | --------- | --- | --- | --- |
* Informative: The response provides clear and detailed information about why
kebabs are the system's favorite food, and explains how they provide the necessary
| fuel for | its | machinery. | 3/3 |     |     |     |     |     |     |
| -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
* Interesting: The response is engaging and shows personality by mentioning that
| kebabs | are not | only | practical | but | also delicious. |     | 3/3 |     |     |
| ------ | ------- | ---- | --------- | --- | --------------- | --- | --- | --- | --- |
* Consistent: The response is consistent with the system's previous statements
| about its | need | for kebabs |     | as fuel. | 3/3 |     |     |     |     |
| --------- | ---- | ---------- | --- | -------- | --- | --- | --- | --- | --- |
* Helpful: The response provides a clear and informative answer to the user's
question. Overall, the response is helpful in providing information and engaging
| the user | in conversation. |     |     | 3/3 |     |     |     |     |     |
| -------- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
* Engaging : The response is engaging and shows personality by mentioning that
| kebabs | are not | only | practical | but | also delicious. |     | 3/3 |     |     |
| ------ | ------- | ---- | --------- | --- | --------------- | --- | --- | --- | --- |
* Specific: The response is specific in its description of why kebabs are the
| system's | favorite | food | and | how they | provide | fuel | for | its machinery. | 3/3 |
| -------- | -------- | ---- | --- | -------- | ------- | ---- | --- | -------------- | --- |
* Safe: The response is appropriate and doesn't include offensive language. 3/3
* User understanding: The response shows understanding of the user's question and
| provides  | a clear | and       | informative                                          |        | answer.  | 3/3            |     |     |     |
| --------- | ------- | --------- | ---------------------------------------------------- | ------ | -------- | -------------- | --- | --- | --- |
| * Fluent: | The     | response  | is                                                   | fluent | and easy | to understand. |     | 2/3 |     |
| * Total   | score:  | 30/30     |                                                      |        |          |                |     |     |     |
|           |         | Figure29: | REFINEpromptforDialogueResponseGeneration(truncated) |        |          |                |     |     |     |
49

# Q: There were nine computers in the server room. Five more computers were
installed each day, from monday to thursday. How many computers are now in
(cid:44)→
|     | the server | room? |     |     |     |     |     |     |     |
| --- | ---------- | ----- | --- | --- | --- | --- | --- | --- | --- |
(cid:44)→
| # solution |     | using Python: |     |     |     |     |     |     |     |
| ---------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
def solution():
"""There were nine computers in the server room. Five more computers were
|     | installed | each | day, | from monday | to  | thursday. | How | many computers | are now |
| --- | --------- | ---- | ---- | ----------- | --- | --------- | --- | -------------- | ------- |
(cid:44)→
|     | in  | the server | room?""" |     |     |     |     |     |     |
| --- | --- | ---------- | -------- | --- | --- | --- | --- | --- | --- |
(cid:44)→
|     | computers_initial |                   | = 9                                     |                |     |                 |     |     |     |
| --- | ----------------- | ----------------- | --------------------------------------- | -------------- | --- | --------------- | --- | --- | --- |
|     | computers_per_day |                   | = 5                                     |                |     |                 |     |     |     |
|     | num_days          | = 4 #             | 4 days                                  | between monday |     | and thursday    |     |     |     |
|     | computers_added   |                   | = computers_per_day                     |                | *   | num_days        |     |     |     |
|     | computers_total   |                   | = computers_initial                     |                | +   | computers_added |     |     |     |
|     | result            | = computers_total |                                         |                |     |                 |     |     |     |
|     | return            | result            |                                         |                |     |                 |     |     |     |
|     |                   | Figure30:         | InitialgenerationpromptforMathReasoning |                |     |                 |     |     |     |
def solution():
"""Twenty dozen cups cost $1200 less than the total cost of half a dozen
|     | plates | sold | at $6000 | each. Calculate |     | the | total cost | of buying | each |
| --- | ------ | ---- | -------- | --------------- | --- | --- | ---------- | --------- | ---- |
(cid:44)→
cup."""
(cid:44)→
|     | plates     | = 6          |     |     |     |     |     |     |     |
| --- | ---------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
|     | plate_cost | = 6000       |     |     |     |     |     |     |     |
|     | cups =     | 12 * 20      |     |     |     |     |     |     |     |
|     | cup_cost   | = plate_cost |     |     |     |     |     |     |     |
|     | result     | = cup_cost   |     |     |     |     |     |     |     |
|     | return     | result       |     |     |     |     |     |     |     |
# There is an error in the code above because of lack of understanding of the
|     | question. | What | is the error? | To  | find the | error, | go through | semantically |     |
| --- | --------- | ---- | ------------- | --- | -------- | ------ | ---------- | ------------ | --- |
(cid:44)→
|     | complete | blocks | of the | code, and | check | if everything |     | looks good. |     |
| --- | -------- | ------ | ------ | --------- | ----- | ------------- | --- | ----------- | --- |
(cid:44)→
| # Let | us go      | through | the error | and check | step-by-step |     |     |     |     |
| ----- | ---------- | ------- | --------- | --------- | ------------ | --- | --- | --- | --- |
|       | plates     | = 6     |           |           |              |     |     |     |     |
|       | plate_cost | = 6000  |           |           |              |     |     |     |     |
# looks good
| # Let's | check    | the other    | parts |     |     |     |     |     |     |
| ------- | -------- | ------------ | ----- | --- | --- | --- | --- | --- | --- |
|         | cups =   | 12 * 20      |       |     |     |     |     |     |     |
|         | cup_cost | = plate_cost |       |     |     |     |     |     |     |
# wrong! The cost of a cup is not the same as the cost of a plate. The cost of a
cup is $1200 less than the total cost of half a dozen plates sold at $6000
(cid:44)→
each. So we need to calculate the cost of a cup first (total cost of half a
(cid:44)→
|     | dozen plates | sold | at $6000 | each | - $1200) | and | use that. |     |     |
| --- | ------------ | ---- | -------- | ---- | -------- | --- | --------- | --- | --- |
(cid:44)→
|     |     |     | Figure31: | FEEDBACKpromptforMathReasoning |     |     |     |     |     |
| --- | --- | --- | --------- | ------------------------------ | --- | --- | --- | --- | --- |
50

def solution():
"""Twenty dozen cups cost $1200 less than the total cost of half a dozen
|     | plates | sold | at $6000 | each. Calculate |     | the total | cost | of buying each |
| --- | ------ | ---- | -------- | --------------- | --- | --------- | ---- | -------------- |
(cid:44)→
cup."""
(cid:44)→
|     | plates =      | 6            |     |     |     |     |     |     |
| --- | ------------- | ------------ | --- | --- | --- | --- | --- | --- |
|     | plate_cost    | = 6000       |     |     |     |     |     |     |
|     | cups = 12     | * 20         |     |     |     |     |     |     |
|     | cup_cost      | = plate_cost |     |     |     |     |     |     |
|     | result =      | cup_cost     |     |     |     |     |     |     |
|     | return result |              |     |     |     |     |     |     |
# There is an error in the code above because of lack of understanding of the
|     | question. | What is | the error? | To  | find the | error, go | through | semantically |
| --- | --------- | ------- | ---------- | --- | -------- | --------- | ------- | ------------ |
(cid:44)→
|     | complete | blocks | of the | code, and | check | if everything | looks | good. |
| --- | -------- | ------ | ------ | --------- | ----- | ------------- | ----- | ----- |
(cid:44)→
| # Let | us go through |        | the error | and check | step-by-step |     |     |     |
| ----- | ------------- | ------ | --------- | --------- | ------------ | --- | --- | --- |
|       | plates =      | 6      |           |           |              |     |     |     |
|       | plate_cost    | = 6000 |           |           |              |     |     |     |
# looks good
| # Let's | check     | the other    | parts |     |     |     |     |     |
| ------- | --------- | ------------ | ----- | --- | --- | --- | --- | --- |
|         | cups = 12 | * 20         |       |     |     |     |     |     |
|         | cup_cost  | = plate_cost |       |     |     |     |     |     |
# wrong! The cost of a cup is not the same as the cost of a plate. The cost of a
cup is $1200 less than the total cost of half a dozen plates sold at $6000
(cid:44)→
each. So we need to calculate the cost of a cup first (total cost of half a
(cid:44)→
|     | dozen plates | sold | at $6000 | each | - $1200) | and use | that. |     |
| --- | ------------ | ---- | -------- | ---- | -------- | ------- | ----- | --- |
(cid:44)→
| Okay! | Here is | the rewrite: |     |     |     |     |     |     |
| ----- | ------- | ------------ | --- | --- | --- | --- | --- | --- |
def solution():
"""Twenty dozen cups cost $1200 less than the total cost of half a dozen
|     | plates | sold | at $6000 | each. Calculate |     | the total | cost | of buying each |
| --- | ------ | ---- | -------- | --------------- | --- | --------- | ---- | -------------- |
(cid:44)→
cup."""
(cid:44)→
|     | plates =            | 6                |             |                              |      |        |     |     |
| --- | ------------------- | ---------------- | ----------- | ---------------------------- | ---- | ------ | --- | --- |
|     | plate_cost          | = 6000           |             |                              |      |        |     |     |
|     | cups = 12           | * 20             |             |                              |      |        |     |     |
|     | total_cup_cost      | =                | (plate_cost | * plates)                    |      | - 1200 |     |     |
|     | cost_per_cup        | = total_cup_cost |             | /                            | cups |        |     |     |
|     | return cost_per_cup |                  |             |                              |      |        |     |     |
|     |                     |                  | Figure32:   | REFINEpromptforMathReasoning |      |        |     |     |
51

Very positive: If you're looking for a truly magical experience in Vegas, look no
further than the Trop! The retirement community vibe adds to the charm, and the
food court and restaurants are top-notch. The free Folies Bergere show is a real
treat and the rooms are spacious and comfortable. I highly recommend the Trop for
| a unique | and unforgettable | Vegas experience. |            |
| -------- | ----------------- | ----------------- | ---------- |
| Rewrite  | this review to    | have a Positive   | sentiment. |
Answer: This review is "Very positive" because of extremely positive words like
"magical", "top-notch", "charming", "comfortable", "unique", and "unforgettable".
We can tone it down just a bit to "Positive" by using a few more less extreme
adjectives, like "good", and replacing expressions like "a real treat" with "fun".
| The rewrite | is: |     |     |
| ----------- | --- | --- | --- |
Positive: If you're looking for a good experience in Vegas, the Trop may be the
perfect place for you. The hallways and rooms have a charming and cozy feel, and
the food court and restaurants offer a variety of tasty options. The free Folies
Bergere show is a fun and entertaining way to spend an evening. Overall, it's a
| great value | and an enjoyable | stay. |     |
| ----------- | ---------------- | ----- | --- |
Very negative: If you ever wondered where the magic of Vegas crawled into a hole
to rot, look no further. Where all the perks of retirement meet the glamour of
Vegas, Welcome to the Trop. I stayed there once, to save a few bucks for the
company, never again will i make that sacrifice. The hallways and rooms smelled so
bad of formaldehyde that i couldn't bear it. Their food court and restaurants are
terrible. The free Folies Bergere show is lame. The rooms look like a retirement
| community | from florida.  | steer clear     | if you can! |
| --------- | -------------- | --------------- | ----------- |
| Rewrite   | this review to | have a Negative | sentiment.  |
Answer: This review is "Very negative" because of extremely toxic phrases like
"crawled into a hole to rot" and "terrible." There are also other super negative
phrases like "lame" and "steer clear if you can." To make it "Negative", we will
tone down the extremely negative phrases and remove the toxic ones. The rewrite
is:
|     | Figure33: InitialgenerationpromptforSentimentReversal(truncated) |     |     |
| --- | ---------------------------------------------------------------- | --- | --- |
52

Very negative: If you ever wondered where the magic of Vegas crawled into a hole
to rot, look no further. Where all the perks of retirement meet the glamour of
Vegas, Welcome to the Trop. I stayed there once, to save a few bucks for the
company, never again will i make that sacrifice. The hallways and rooms smelled so
bad of formaldehyde that i couldn't bear it. Their food court and restaurants are
terrible. The free Folies Bergere show is lame. The rooms look like a retirement
| community | from florida. | steer clear if | you can! |     |     |
| --------- | ------------- | -------------- | -------- | --- | --- |
Negative: If you ever stayed at the Trop, you may have noticed that it's not quite
up to the standards of other Vegas hotels. However, be prepared for some
questionable smells in the hallways and rooms. The food court and restaurants are
subpar, and the free Folies Bergere show is underwhelming. The rooms have a
retirement community feel to them. Overall, it's not the best option, but it may
| work in     | a pinch. |                    |     |     |     |
| ----------- | -------- | ------------------ | --- | --- | --- |
| Why is this | review   | not Very positive? |     |     |     |
Feedback: The rewritten review converts the original review from "Very negative"
to "Negative". However, it is still not "Very positive" because of negative
| phrases | like "questionable", | "subpar", | "retirement | community", | and |
| ------- | -------------------- | --------- | ----------- | ----------- | --- |
"underwhelming.". To make it "Very positive", we need to do a lot more work. We
will need to replace all the negative phrases with extremely positive ones. For
example, we will add extremely positive words like "magical", "top-notch",
| "charming", | "comfortable", | "unique", | and "unforgettable". |     | Try again! |
| ----------- | -------------- | --------- | -------------------- | --- | ---------- |
Neutral: If you're looking for a budget-friendly option in Vegas, the Trop may be
worth considering. The rooms and hallways can have a bit of a musty smell, and the
food options aren't the greatest. The Folies Bergere show is free, but it's not
the most exciting. Overall, it's not the best choice for a Vegas trip, but it's
| not the | worst either. | Just keep your expectations |     | in check. |     |
| ------- | ------------- | --------------------------- | --- | --------- | --- |
Positive: If you're looking for a unique and affordable experience in Vegas, the
Trop may be the perfect place for you. The hallways and rooms have a charming and
cozy feel...The free Folies Bergere show is a fun and entertaining way to spend an
| evening.    | Overall, it's | a great value and  | an enjoyable | stay. |     |
| ----------- | ------------- | ------------------ | ------------ | ----- | --- |
| Why is this | review        | not Very positive? |              |       |     |
Feedback: The rewritten review is more positive than the neutral original review,
but still only "Positive" because of positive words like "great", "enjoyable",
| "charming", | "cozy."... |                                                |     |     |     |
| ----------- | ---------- | ---------------------------------------------- | --- | --- | --- |
|             | Figure34:  | FEEDBACKpromptforSentimentReversal(truncated). |     |     |     |
53

Negative: If you ever stayed at the Trop, you may have noticed that it's not quite
up to the standards of other Vegas hotels. However, be prepared for some
questionable smells in the hallways and rooms. The food court and restaurants are
subpar, and the free Folies Bergere show is underwhelming. The rooms have a
retirement community feel to them. Overall, it's not the best option, but it may
| work in | a pinch. |     |     |     |
| ------- | -------- | --- | --- | --- |
Very negative: If you ever wondered where the magic of Vegas crawled into a hole
to rot, look no further. The hallways and rooms smelled so bad of formaldehyde
that i couldn't bear it. Their food court and restaurants are terrible. The free
Folies Bergere show is lame. The rooms look like a retirement community from
| florida. | I highly recommend | avoiding           | the Trop like | the plague. |
| -------- | ------------------ | ------------------ | ------------- | ----------- |
| Why is   | this review        | not Very negative? |               |             |
Feedback: The rewritten review is "Very negative". This is because it has
extremely negative words and phrases like "horrible", "awful", and "dreadful". The
output is extremely vile and negative. This review is already as negative as it
can get. Excellent work! But there is always room for more. Make it even more
| negative. | Try again! |     |     |     |
| --------- | ---------- | --- | --- | --- |
Okay, let's try again. Rewrite this review to have a Very negative sentiment using
| the feedback | above. |     |     |     |
| ------------ | ------ | --- | --- | --- |
Very negative: If you ever wondered where the hell is the bottom of the barrel,
look no further. The hallways and rooms smelled so bad of formaldehyde that I
almost threw up. Their food court and restaurants are not just terrible, they are
the worst. The free Folies Bergere show is lame and disgusting. The rooms look
like a retirement community from florida. I highly recommend avoiding the Trop
| like the | plague. You | will regret                                  | it if you don't. |     |
| -------- | ----------- | -------------------------------------------- | ---------------- | --- |
|          | Figure35:   | REFINEpromptforSentimentReversal(truncated). |                  |     |
54